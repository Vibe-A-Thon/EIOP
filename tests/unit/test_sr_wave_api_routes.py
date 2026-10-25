"""API tests for the pass-9 SR-wave routes wired in apps/api/extended.py.

Covers the Super-Requirements commercial baseline packages: tenancy
(SR-TEN-001/002/003/006/007/009), licensing (SR-DEP-007, SR-COM-001,
SR-TEN-009), layered config (SR-CFG-001..006), egress gateway
(SR-LLM-010..020, SR-CON-010/011), branding (SR-WL-*, SR-ONT-007),
privacy (SR-PRV-*), compliance packs (SR-GOV-001..005), report generator
(SR-NLQ-008), QA gate integrity (SR-QA-010..014), NL suggestion engine
(SR-NLQ-002/003/004), and the schema profiler (SR-ING-010/012/013).

These are route smoke tests: each test carries an explicit ``pytest.mark.req`` naming only the
requirement(s) its assertions actually exercise, so the section headers' ID ranges do not credit
every listed requirement.
"""

from pathlib import Path

import pytest
from eoip.config.layered import LayerRef, SettingDef
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

from apps.api.app import create_app

TENANT_HEADERS = {"X-Tenant-Id": "acme", "X-Principal": "alice"}


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.delenv("EOIP_LICENSE_PATH", raising=False)
    store = MemoryGraphStore()
    return TestClient(create_app(store))


# --- tenancy (SR-TEN-001/002/003/006/007/009) -------------------------------


@pytest.mark.req("SR-TEN-001")
def test_tenancy_context_fail_closed_and_resolve(client: TestClient) -> None:
    missing = client.get("/api/v1/tenancy/context")
    assert missing.status_code == 403

    ok = client.get("/api/v1/tenancy/context", headers=TENANT_HEADERS)
    assert ok.status_code == 200
    body = ok.json()
    assert body["tenant_id"] == "acme"
    assert body["principal"] == "alice"


@pytest.mark.req("SR-TEN-002", "SR-TEN-006")
def test_tenancy_isolation_and_quota_routes(client: TestClient) -> None:
    models = client.get("/api/v1/tenancy/isolation/models", headers=TENANT_HEADERS)
    assert models.status_code == 200
    assert models.json()["models"]

    quotas = client.get("/api/v1/tenancy/quotas", headers=TENANT_HEADERS)
    assert quotas.status_code == 200
    assert quotas.json()["tenant_id"] == "acme"
    assert "usage" in quotas.json()

    check = client.post(
        "/api/v1/tenancy/quotas/check",
        headers=TENANT_HEADERS,
        json={"dimension": "graph_size", "amount": 1},
    )
    assert check.status_code == 200


# --- licensing (SR-DEP-007, SR-COM-001, SR-TEN-009) -------------------------


@pytest.mark.req("SR-DEP-007", "SR-TEN-009")
def test_licensing_status_and_check_module(client: TestClient) -> None:
    status = client.get("/api/v1/licensing/status")
    assert status.status_code == 200
    assert status.json()["state"] in {"active", "perpetual", "grace"}

    ok = client.post("/api/v1/licensing/check-module", json={"module": "graph"})
    assert ok.status_code == 200
    assert ok.json()["allowed"] is True


# --- layered config (SR-CFG-001..006) ----------------------------------------


@pytest.mark.req("SR-CFG-001", "SR-CFG-003")
def test_config_set_and_explain(client: TestClient) -> None:
    store = client.app.state.extended_state.config_store
    store.register(
        SettingDef(
            key="security.session.ttl_seconds",
            description="Session TTL",
            domain="security",
            schema={"type": "integer", "minimum": 60, "maximum": 86400},
            default=3600,
        )
    )
    layer = {"kind": "tenant", "instance": "acme"}
    response = client.post(
        "/api/v1/config/set",
        json={
            "key": "security.session.ttl_seconds",
            "layer": layer,
            "value": 7200,
            "actor": "alice",
        },
    )
    assert response.status_code == 200
    assert response.json()["new_value"] == 7200

    explain = client.get(
        "/api/v1/config/explain",
        params={"key": "security.session.ttl_seconds", "tenant": "acme"},
    )
    assert explain.status_code == 200
    body = explain.json()
    assert body["effective"]["value"] == 7200


# --- egress gateway (SR-LLM-010..020, SR-CON-010/011) ------------------------


@pytest.mark.req("SR-LLM-011")
def test_egress_policy_rule_and_dry_run_call(client: TestClient) -> None:
    rule = client.post(
        "/api/v1/egress/policy/rules",
        json={
            "rule": {
                "rule_id": "r1",
                "classes": ["public"],
                "max_level": 2,
            }
        },
    )
    assert rule.status_code == 200

    rules = client.get("/api/v1/egress/policy/rules")
    assert rules.status_code == 200
    assert any(r["rule_id"] == "r1" for r in rules.json()["rules"])

    dry = client.post(
        "/api/v1/egress/call",
        json={
            "endpoint_id": "nonexistent",
            "task": "summarize",
            "payload": {"text": "hello"},
            "user_id": "alice",
            "role": "analyst",
            "data_classes": ["public"],
            "dry_run": True,
        },
    )
    # Dry-run exercises policy + manifest without a registered transport;
    # a disabled-by-default endpoint must not make a live call.
    assert dry.status_code in {200, 403, 404}


# --- branding (SR-WL-001/003/004-partial/006/007, SR-ONT-007) -----------------


@pytest.mark.req("SR-ONT-007", "SR-WL-001")
def test_branding_theme_and_terminology_rename(client: TestClient) -> None:
    theme = client.get("/api/v1/branding/theme")
    assert theme.status_code == 200
    assert theme.json()["app_name"] == "EOIP"

    rename = client.post(
        "/api/v1/branding/terminology/rename",
        params={"tenant_id": "acme"},
        json={"canonical_types": ["WorkItem"]},
    )
    assert rename.status_code == 200
    assert rename.json()["renames"]


# --- privacy (SR-PRV-001..004, 006 partials) ----------------------------------


@pytest.mark.req("SR-PRV-001", "SR-PRV-002")
def test_privacy_classify_and_dsar_locate(client: TestClient) -> None:
    classify = client.post(
        "/api/v1/privacy/classify",
        json={"payload": {"name": "Ada Lovelace", "email": "ada@example.com"}},
    )
    assert classify.status_code == 200

    store = client.app.state.graph_store
    store.upsert_vertex(
        "Person", {"canonical_id": "urn:eoip:person:1", "display_name": "Ada", "email": "ada@example.com"}
    )
    locate = client.post(
        "/api/v1/privacy/dsar/locate",
        json={
            "subject_id": "ada@example.com",
            "tenant_id": "acme",
            "subject_properties": ["email"],
        },
    )
    assert locate.status_code == 200
    body = locate.json()
    refs = [hit["ref"] for hit in body["hits"]]
    assert "urn:eoip:person:1" in refs


# --- compliance packs (SR-GOV-001..005) ---------------------------------------


@pytest.mark.req("SR-GOV-001")
def test_compliance_packs_list_and_gap_analysis(client: TestClient) -> None:
    packs = client.get("/api/v1/compliance/packs")
    assert packs.status_code == 200
    frameworks = {p["framework"] for p in packs.json()}
    assert "GDPR" in frameworks

    gap = client.post("/api/v1/compliance/packs/GDPR/gap-analysis")
    assert gap.status_code == 200
    assert gap.json()["total_controls"] > 0


# --- report generator (SR-NLQ-008) --------------------------------------------


@pytest.mark.req("SR-NLQ-008")
def test_reports_render_markdown(client: TestClient) -> None:
    response = client.post(
        "/api/v1/reports/render",
        params={"template_id": "executive-brief", "report_format": "markdown"},
        json={"title": "Weekly brief"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["format"] == "markdown"
    assert body["content"]


# --- QA gate integrity (SR-QA-010..014) ----------------------------------------


@pytest.mark.req("SR-QA-012", "SR-QA-013")
def test_qa_dashboard_three_numbers_and_inventory(client: TestClient) -> None:
    dashboard = client.get("/api/v1/qa/dashboard")
    assert dashboard.status_code == 200
    body = dashboard.json()
    assert "tests_passing" in body
    assert "requirements_with_behavioral_evidence" in body
    assert "requirements_with_external_gate_evidence" in body
    # SR-QA-012: a single merged percentage is prohibited.
    assert "percent_complete" not in body

    inventory = client.get("/api/v1/qa/inventory")
    assert inventory.status_code == 200


# --- NL suggestion engine (SR-NLQ-002/003/004-partial) --------------------------


@pytest.mark.req("SR-NLQ-002")
def test_suggest_interpret(client: TestClient) -> None:
    response = client.post(
        "/api/v1/suggest/interpret",
        json={"question": "show me all WorkItems"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["candidates"]


# --- schema profiler (SR-ING-010/012/013/016-hook) -------------------------------


@pytest.mark.req("SR-ING-010")
def test_ingest_profile(client: TestClient) -> None:
    response = client.post(
        "/api/v1/ingest/profile",
        json={
            "dataset": "people",
            "records": [
                {"id": 1, "name": "Ada"},
                {"id": 2, "name": "Grace"},
            ],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["record_count"] == 2
    assert body["fields"]
