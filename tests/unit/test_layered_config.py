"""Unit tests for the layered configuration framework (SR-CFG-001..006)."""

from __future__ import annotations

import json

import pytest
from eoip.config.ascode import (
    ConfigArchive,
    apply_archive,
    diff_configs,
    export_config,
    import_config,
    rollback,
)
from eoip.config.layered import (
    ConfigStore,
    FeatureFlag,
    FeatureFlagStore,
    HotReloadHandle,
    LayerRef,
    SettingDef,
    SettingScope,
)
from eoip.config.router import build_router
from fastapi import FastAPI
from fastapi.testclient import TestClient
from jsonschema import ValidationError

TENANT = SettingScope(tenant="acme")


def _store() -> ConfigStore:
    return ConfigStore()


def _ttl_def(**kwargs) -> SettingDef:
    return SettingDef(
        key="security.session.ttl_seconds",
        description="Session TTL",
        domain="security",
        schema={"type": "integer", "minimum": 60, "maximum": 86400},
        default=3600,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# SR-CFG-001: layers, typing, validation, versioning, audit
# ---------------------------------------------------------------------------


def test_layers_precedence_higher_wins() -> None:
    store = _store()
    store.register(_ttl_def())
    store.set("security.session.ttl_seconds", LayerRef(kind="tenant", instance="acme"), 7200)
    eff = store.get("security.session.ttl_seconds", TENANT)
    assert eff.value == 7200
    assert eff.layer and eff.layer.kind == "tenant"


def test_user_layer_overrides_tenant() -> None:
    store = _store()
    store.register(_ttl_def())
    store.set("security.session.ttl_seconds", LayerRef(kind="tenant", instance="acme"), 7200)
    store.set("security.session.ttl_seconds", LayerRef(kind="user", instance="u1"), 900)
    eff = store.get("security.session.ttl_seconds", TENANT, user_id="u1")
    assert eff.value == 900
    assert eff.layer and eff.layer.kind == "user"


def test_schema_validation_rejects_bad_value() -> None:
    store = _store()
    store.register(_ttl_def())
    with pytest.raises(ValidationError):
        store.set("security.session.ttl_seconds", LayerRef(kind="tenant", instance="acme"), "soon")
    with pytest.raises(ValidationError):
        store.set("security.session.ttl_seconds", LayerRef(kind="tenant", instance="acme"), 10)


def test_versioning_and_audit_trail() -> None:
    store = _store()
    store.register(_ttl_def())
    tenant = LayerRef(kind="tenant", instance="acme")
    c1 = store.set("security.session.ttl_seconds", tenant, 7200, actor="alice")
    c2 = store.set("security.session.ttl_seconds", tenant, 4800, actor="bob")
    assert c1.new_version == 1 and c2.new_version == 2
    assert c2.old_value == 7200 and c2.old_version == 1
    trail = store.audit_trail("security.session.ttl_seconds")
    assert [c.change_id for c in trail] == [c1.change_id, c2.change_id]
    assert trail[1].actor == "bob"
    prev = store.get_version("security.session.ttl_seconds", tenant, 1)
    assert prev is not None and prev.value == 7200


def test_persistence_roundtrip() -> None:
    from eoip.config.layered import MemoryPersistence

    persistence = MemoryPersistence()
    store = ConfigStore(persistence)
    store.register(_ttl_def())
    store.set("security.session.ttl_seconds", LayerRef(kind="tenant", instance="acme"), 7200)
    restored = ConfigStore(persistence)
    restored.restore()
    assert restored.get("security.session.ttl_seconds", TENANT).value == 7200


# ---------------------------------------------------------------------------
# SR-CFG-002: floors / ceilings, most-restrictive-wins
# ---------------------------------------------------------------------------


def test_ceiling_at_partner_blocks_looser_tenant_value() -> None:
    store = _store()
    store.register(_ttl_def())
    store.set_bound(
        "security.session.ttl_seconds",
        LayerRef(kind="partner", instance="reseller1"),
        ceiling=3600,
    )
    with pytest.raises(ValueError, match="bound"):
        store.set("security.session.ttl_seconds", LayerRef(kind="tenant", instance="acme"), 7200)
    store.set("security.session.ttl_seconds", LayerRef(kind="tenant", instance="acme"), 3600)
    assert store.get("security.session.ttl_seconds", TENANT).value == 3600


def test_floor_at_tenant_blocks_looser_workspace_value() -> None:
    store = _store()
    store.register(_ttl_def())
    store.set_bound(
        "security.session.ttl_seconds",
        LayerRef(kind="tenant", instance="acme"),
        floor=1800,
    )
    scope = SettingScope(tenant="acme", business_unit="bu1", workspace="ws1")
    with pytest.raises(ValueError):
        store.set("security.session.ttl_seconds", LayerRef(kind="workspace", instance="ws1"), 600)
    store.set("security.session.ttl_seconds", LayerRef(kind="workspace", instance="ws1"), 2400)
    assert store.get("security.session.ttl_seconds", scope).value == 2400


def test_most_restrictive_wins_across_layers() -> None:
    store = _store()
    store.register(
        SettingDef(
            key="security.egress.allowed_levels",
            schema={"type": "integer"},
            default=0,
            restrictive_direction="high",
        )
    )
    store.set_bound("security.egress.allowed_levels", LayerRef(kind="edition", instance="pro"), ceiling=1)
    store.set_bound("security.egress.allowed_levels", LayerRef(kind="partner", instance="p1"), ceiling=0)
    # partner ceiling (0) is more restrictive than edition ceiling (1)
    with pytest.raises(ValueError):
        store.set("security.egress.allowed_levels", LayerRef(kind="tenant", instance="acme"), 1)


def test_low_direction_most_restrictive_is_largest() -> None:
    store = _store()
    store.register(
        SettingDef(
            key="security.password.min_length",
            schema={"type": "integer"},
            default=8,
            restrictive_direction="low",  # larger = more restrictive
        )
    )
    store.set_bound("security.password.min_length", LayerRef(kind="partner", instance="p1"), floor=12)
    with pytest.raises(ValueError):
        store.set("security.password.min_length", LayerRef(kind="tenant", instance="acme"), 8)
    store.set("security.password.min_length", LayerRef(kind="tenant", instance="acme"), 16)
    assert store.get("security.password.min_length", TENANT).value == 16


# ---------------------------------------------------------------------------
# SR-CFG-003: effective-config explain
# ---------------------------------------------------------------------------


def test_explain_shows_layer_chain_and_last_change() -> None:
    store = _store()
    store.register(_ttl_def())
    tenant = LayerRef(kind="tenant", instance="acme")
    change = store.set("security.session.ttl_seconds", tenant, 7200, actor="alice", reason="policy")
    result = store.explain("security.session.ttl_seconds", TENANT)
    kinds = [c.layer.kind for c in result.chain]
    assert kinds == ["product-default", "tenant"]
    assert result.chain[0].present is False  # nothing at product default
    assert result.chain[1].present and result.chain[1].value == 7200
    assert result.effective.value == 7200
    assert result.effective.layer == tenant
    assert result.last_change is not None and result.last_change.change_id == change.change_id


def test_explain_reports_default_when_unset() -> None:
    store = _store()
    store.register(_ttl_def())
    result = store.explain("security.session.ttl_seconds", TENANT)
    assert result.effective.value == 3600
    assert result.effective.version == 0
    assert all(not c.present for c in result.chain)


# ---------------------------------------------------------------------------
# SR-CFG-004: config as code
# ---------------------------------------------------------------------------


def _seeded_store() -> ConfigStore:
    store = _store()
    store.register(_ttl_def())
    store.set("security.session.ttl_seconds", LayerRef(kind="tenant", instance="acme"), 7200)
    return store


def test_export_import_roundtrip_json_and_yaml() -> None:
    store = _seeded_store()
    layer = LayerRef(kind="tenant", instance="acme")
    archive = export_config(store, layer)
    payload_json = archive.to_json()
    payload_yaml = archive.to_yaml()

    target = _store()
    target.register(_ttl_def())
    result = import_config(target, payload_json)
    assert result["ok"] and not result["dry_run"]
    assert target.get("security.session.ttl_seconds", TENANT).value == 7200

    target2 = _store()
    target2.register(_ttl_def())
    assert import_config(target2, payload_yaml, fmt="yaml")["ok"]
    assert target2.get("security.session.ttl_seconds", TENANT).value == 7200


def test_import_dry_run_writes_nothing() -> None:
    store = _seeded_store()
    layer = LayerRef(kind="tenant", instance="acme")
    archive = export_config(store, layer)
    archive.entries[0].value = 4800

    target = _store()
    target.register(_ttl_def())
    result = apply_archive(target, archive, dry_run=True)
    assert result["ok"] and result["dry_run"]
    assert len(result["applied"]) == 1
    assert "dry-run" in result["applied"][0].reason
    # nothing written
    assert target.get("security.session.ttl_seconds", TENANT).value == 3600


def test_import_validates_schema() -> None:
    store = _seeded_store()
    archive = export_config(store, LayerRef(kind="tenant", instance="acme"))
    archive.entries[0].value = "not-an-int"
    target = _store()
    target.register(_ttl_def())
    result = apply_archive(target, archive)
    assert not result["ok"]
    assert result["errors"] and "not-an-int" in json.dumps(result["errors"])


def test_diff_detects_added_removed_changed() -> None:
    store = _store()
    store.register(_ttl_def())
    store.register(SettingDef(key="observability.log_level", schema={"type": "string"}, default="info"))
    layer = LayerRef(kind="tenant", instance="acme")
    a = ConfigArchive(
        layer=layer,
        definitions=list(store.definitions()),
        entries=[
            {"key": "security.session.ttl_seconds", "value": 7200},
            {"key": "observability.log_level", "value": "info"},
        ],
    )
    b = ConfigArchive(
        layer=layer,
        definitions=list(store.definitions()),
        entries=[
            {"key": "security.session.ttl_seconds", "value": 7200},
            {"key": "observability.log_level", "value": "debug"},
        ],
    )
    diff = diff_configs(a, b)
    assert diff.added == [] and diff.removed == []
    assert len(diff.changed) == 1
    assert diff.changed[0].key == "observability.log_level"
    assert diff.changed[0].old_value == "info" and diff.changed[0].new_value == "debug"
    b2 = ConfigArchive(
        layer=layer,
        definitions=list(store.definitions()),
        entries=[
            {"key": "security.session.ttl_seconds", "value": 4800},
        ],
    )
    diff2 = diff_configs(a, b2)
    assert sorted(diff2.added) == [] and sorted(diff2.removed) == ["observability.log_level"]
    assert len(diff2.changed) == 1 and diff2.changed[0].new_value == 4800
    diff3 = diff_configs(a, a)
    assert diff3.changed_count == 0


def test_rollback_restores_previous_version_audited() -> None:
    store = _seeded_store()
    layer = LayerRef(kind="tenant", instance="acme")
    rec = rollback(store, "security.session.ttl_seconds", layer, 0 + 1, actor="carol")
    # version 1 did not exist (first set was version 1 -> value 7200)... verify:
    assert rec.old_value == 7200
    assert store.get("security.session.ttl_seconds", TENANT).value == 7200
    # actually set a second value then roll back to version 1
    store.set("security.session.ttl_seconds", layer, 4800)
    rec2 = rollback(store, "security.session.ttl_seconds", layer, 1, actor="carol")
    assert rec2.new_value == 7200
    assert "rollback" in rec2.reason
    assert store.get("security.session.ttl_seconds", TENANT).value == 7200


def test_import_respects_upper_layer_bounds() -> None:
    source = _seeded_store()
    archive = export_config(source, LayerRef(kind="tenant", instance="acme"))
    target = _store()
    target.register(_ttl_def())
    target.set_bound(
        "security.session.ttl_seconds",
        LayerRef(kind="partner", instance="p1"),
        ceiling=3600,
    )
    result = import_config(target, archive.to_json())
    assert not result["ok"]


# ---------------------------------------------------------------------------
# SR-CFG-005: feature flags distinct from config
# ---------------------------------------------------------------------------


def test_feature_flags_are_separate_and_audited() -> None:
    store = _store()
    flags = FeatureFlagStore(store)
    flags.register(FeatureFlag(key="new-console", enabled=False, owner="team-a"))
    assert flags.get("new-console").enabled is False
    flags.set("new-console", True, actor="dave")
    assert flags.get("new-console").enabled is True
    assert flags.get("new-console").never_bypasses_policy is True
    history = flags.history("new-console")
    assert history[-1]["actor"] == "dave"
    # flags do not appear in config definitions
    assert all(d.key != "new-console" for d in store.definitions())


# ---------------------------------------------------------------------------
# SR-CFG-006: hot reload
# ---------------------------------------------------------------------------


def test_hot_reload_notifies_subscribers() -> None:
    store = _store()
    store.register(_ttl_def())
    seen: list[int] = []
    handle = store.hot_reload("security.session.ttl_seconds", lambda eff: seen.append(eff.value))
    assert isinstance(handle, HotReloadHandle)
    store.set("security.session.ttl_seconds", LayerRef(kind="tenant", instance="acme"), 7200)
    assert seen == [7200]
    handle.close()
    store.set("security.session.ttl_seconds", LayerRef(kind="tenant", instance="acme"), 4800)
    assert seen == [7200]


def test_structural_settings_reject_hot_reload() -> None:
    store = _store()
    store.register(
        SettingDef(
            key="storage.graph.backend",
            schema={"type": "string"},
            structural=True,
        )
    )
    with pytest.raises(ValueError, match="structural"):
        store.hot_reload("storage.graph.backend", lambda eff: None)


# ---------------------------------------------------------------------------
# Router (wired by apps/api later; smoke-tested here)
# ---------------------------------------------------------------------------


def _client() -> TestClient:
    store = _store()
    store.register(_ttl_def())
    flags = FeatureFlagStore(store)
    flags.register(FeatureFlag(key="new-console", enabled=False))
    app = FastAPI()
    app.include_router(build_router(store, flags))
    return TestClient(app)


def test_router_end_to_end() -> None:
    client = _client()
    assert client.get("/api/v1/config/definitions").status_code == 200

    r = client.post(
        "/api/v1/config/set",
        json={
            "key": "security.session.ttl_seconds",
            "layer": {"kind": "tenant", "instance": "acme"},
            "value": 7200,
            "actor": "erin",
        },
    )
    assert r.status_code == 200, r.text
    assert r.json()["new_version"] == 1

    r = client.get("/api/v1/config/effective", params={"key": "security.session.ttl_seconds", "tenant": "acme"})
    assert r.status_code == 200 and r.json()["value"] == 7200

    r = client.get("/api/v1/config/explain", params={"key": "security.session.ttl_seconds", "tenant": "acme"})
    assert r.status_code == 200
    body = r.json()
    assert body["effective"]["value"] == 7200
    assert [c["layer"]["kind"] for c in body["chain"]] == ["product-default", "tenant"]

    r = client.get("/api/v1/config/audit", params={"key": "security.session.ttl_seconds"})
    assert r.status_code == 200 and len(r.json()) == 1

    r = client.post(
        "/api/v1/config/export",
        json={"layer": {"kind": "tenant", "instance": "acme"}},
    )
    assert r.status_code == 200
    archive_payload = r.json()

    r = client.post("/api/v1/config/import", json={"payload": archive_payload, "dry_run": True})
    assert r.status_code == 200 and r.json()["ok"] and r.json()["dry_run"]

    r = client.post("/api/v1/config/rollback", json={
        "key": "security.session.ttl_seconds",
        "layer": {"kind": "tenant", "instance": "acme"},
        "to_version": 1,
    })
    assert r.status_code == 200

    r = client.post("/api/v1/config/diff", json={"from": archive_payload, "to": archive_payload})
    assert r.status_code == 200 and r.json()["changed_count"] == 0

    assert client.get("/api/v1/config/flags").json()[0]["key"] == "new-console"
    r = client.post("/api/v1/config/flags", json={"key": "new-console", "enabled": True})
    assert r.status_code == 200 and r.json()["enabled"] is True

    r = client.post("/api/v1/config/reload-subscribe", json={"key": "security.session.ttl_seconds"})
    assert r.status_code == 200 and r.json()["reloadable"] is True

    # SR-CFG-002: partner ceiling then a looser tenant write must be rejected
    r = client.post(
        "/api/v1/config/bounds",
        json={
            "key": "security.session.ttl_seconds",
            "layer": {"kind": "partner", "instance": "p1"},
            "ceiling": 3600,
        },
    )
    assert r.status_code == 200
    r = client.post(
        "/api/v1/config/set",
        json={
            "key": "security.session.ttl_seconds",
            "layer": {"kind": "tenant", "instance": "acme"},
            "value": 9999,
        },
    )
    assert r.status_code == 422
