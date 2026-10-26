"""API tests for the pass-2 extended capability routes in apps/api/extended.py.

Covers GAP-SEC (authn/authz), model governance (§49), the marketplace
(GAP-MKT), domain packs (GAP-DP), KGCI (GAP-KGCI), ops tooling (§47),
request metrics (GAP-OBS-003), and embeddings health (GAP-SEARCH-001).
"""

import os
from pathlib import Path

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.marketplace import CapabilityKind, PackageManifest, build_package
from fastapi.testclient import TestClient

from apps.api.app import create_app


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("EOIP_REGISTRY_PATH", str(tmp_path / "registry.json"))
    monkeypatch.delenv("EOIP_INSTALL_KEY", raising=False)
    store = MemoryGraphStore()
    return TestClient(create_app(store))


def _package_bytes(name: str = "demo-ext") -> bytes:
    manifest = PackageManifest(
        id=f"urn:eoip:marketplace:package:{name}",
        name=name,
        version="1.0.0",
        description="demo extension package",
        provides={CapabilityKind.ONTOLOGIES: ["DemoEntity"]},
    )
    return build_package(manifest, {"demo/entity.yaml": b"name: DemoEntity\n"})


def test_auth_login_success_and_wrong_password(client: TestClient) -> None:
    app_state = client.app.state.extended_state
    app_state.identity_provider.add_user("alice", "s3cret", roles=("admin",))

    ok = client.post(
        "/api/v1/auth/login", json={"username": "alice", "password": "s3cret"}
    )
    assert ok.status_code == 200
    token = ok.json()["token"]
    payload = app_state.token_service.validate(token)
    assert payload["username"] == "alice"

    bad = client.post(
        "/api/v1/auth/login", json={"username": "alice", "password": "wrong"}
    )
    assert bad.status_code == 401


def test_auth_health(client: TestClient) -> None:
    response = client.get("/api/v1/auth/health")
    assert response.status_code == 200
    assert response.json()["provider"] == "local"


def test_authz_user_create_and_evaluate_allow_deny(client: TestClient) -> None:
    created = client.post(
        "/api/v1/authz/users",
        json={"user_id": "urn:eoip:authz:user:bob", "roles": ["viewer"]},
    )
    assert created.status_code == 201
    duplicate = client.post(
        "/api/v1/authz/users", json={"user_id": "urn:eoip:authz:user:bob"}
    )
    assert duplicate.status_code == 409

    admin = client.post(
        "/api/v1/authz/users",
        json={"user_id": "urn:eoip:authz:user:root", "roles": ["admin"]},
    )
    assert admin.status_code == 201

    allowed = client.post(
        "/api/v1/authz/evaluate",
        json={
            "user_id": "urn:eoip:authz:user:root",
            "action": "user:manage",
            "resource_attrs": {},
        },
    )
    assert allowed.status_code == 200
    assert allowed.json()["allow"] is True

    denied = client.post(
        "/api/v1/authz/evaluate",
        json={
            "user_id": "urn:eoip:authz:user:bob",
            "action": "user:manage",
            "resource_attrs": {},
        },
    )
    assert denied.status_code == 200
    assert denied.json()["allow"] is False

    decisions = client.get("/api/v1/authz/decisions")
    assert decisions.status_code == 200
    assert len(decisions.json()["decisions"]) == 2


def test_authz_roles_and_policies(client: TestClient) -> None:
    roles = client.get("/api/v1/authz/roles")
    assert roles.status_code == 200
    names = {r["name"] for r in roles.json()["roles"]}
    assert {"viewer", "analyst", "steward", "admin"} <= names

    export = client.get("/api/v1/authz/roles/export")
    assert export.status_code == 200
    assert "roles" in export.json()

    policies = client.get("/api/v1/authz/policies")
    assert policies.status_code == 200
    assert len(policies.json()["policies"]) >= 1

    reloaded = client.post(
        "/api/v1/authz/policies/reload",
        content="policies:\n  - id: tmp-grant\n    role: analyst\n    permission: audit:read\n",
        headers={"Content-Type": "application/yaml"},
    )
    assert reloaded.status_code == 200
    assert reloaded.json()["loaded"] == 1


def test_governance_model_register_approve_kill_switch(client: TestClient) -> None:
    registered = client.post(
        "/api/v1/governance/models",
        json={
            "model_id": "demo-llm",
            "version": "1.0.0",
            "provider": "local",
            "capabilities": ["chat"],
        },
    )
    assert registered.status_code == 201

    approved = client.post("/api/v1/governance/models/demo-llm/approval")
    assert approved.status_code == 200
    assert approved.json()["approved"] is True

    missing = client.post("/api/v1/governance/models/nope/approval")
    assert missing.status_code == 404

    revoked = client.request(
        "DELETE", "/api/v1/governance/models/demo-llm/approval"
    )
    assert revoked.status_code == 200
    assert revoked.json()["approved"] is False

    before = client.get("/api/v1/governance/kill-switch").json()
    assert before["global_enabled"] is True

    disabled = client.post(
        "/api/v1/governance/kill-switch", json={"enabled": False, "reason": "test"}
    )
    assert disabled.status_code == 200
    assert disabled.json()["global_enabled"] is False

    feature = client.post(
        "/api/v1/governance/kill-switch/features/rag", json={"enabled": False}
    )
    assert feature.status_code == 200

    re_enabled = client.post("/api/v1/governance/kill-switch", json={"enabled": True})
    assert re_enabled.json()["global_enabled"] is True
    rag = client.post(
        "/api/v1/governance/kill-switch/features/rag", json={"enabled": True}
    )
    assert rag.status_code == 200


def test_governance_evaluate_and_incidents(client: TestClient) -> None:
    verdict = client.post(
        "/api/v1/governance/evaluate",
        json={
            "response_id": "r1",
            "model_id": "demo-llm",
            "text": "answer",
            "groundedness_score": 0.95,
            "unsafe_action_score": 0.0,
        },
    )
    assert verdict.status_code == 200
    assert verdict.json()["passed"] is True

    failing = client.post(
        "/api/v1/governance/evaluate",
        json={
            "response_id": "r2",
            "model_id": "demo-llm",
            "text": "answer",
            "groundedness_score": 0.2,
            "unsafe_action_score": 0.5,
        },
    )
    assert failing.json()["passed"] is False
    assert len(failing.json()["reasons"]) == 2

    incidents = client.get("/api/v1/governance/incidents")
    assert incidents.status_code == 200
    assert incidents.json()["incidents"] == []


def test_marketplace_install_uninstall_round_trip(client: TestClient) -> None:
    archive = _package_bytes()

    installed = client.post(
        "/api/v1/marketplace/install",
        content=archive,
        headers={"Content-Type": "application/zip"},
    )
    assert installed.status_code == 201
    assert installed.json()["name"] == "demo-ext"

    duplicate = client.post(
        "/api/v1/marketplace/install",
        content=archive,
        headers={"Content-Type": "application/zip"},
    )
    # re-installing the same package is idempotent via the registry
    assert duplicate.status_code in (201, 409)

    listing = client.get("/api/v1/marketplace/installed")
    assert listing.status_code == 200
    assert [p["manifest"]["name"] for p in listing.json()["packages"]] == ["demo-ext"]

    search = client.get("/api/v1/marketplace/installed/search", params={"q": "demo"})
    assert [p["manifest"]["name"] for p in search.json()["packages"]] == ["demo-ext"]
    miss = client.get("/api/v1/marketplace/installed/search", params={"q": "zzz"})
    assert miss.json()["packages"] == []

    corrupted = client.post(
        "/api/v1/marketplace/install",
        content=b"not-a-zip",
        headers={"Content-Type": "application/zip"},
    )
    assert corrupted.status_code == 422

    removed = client.post("/api/v1/marketplace/uninstall/demo-ext")
    assert removed.status_code == 200
    assert removed.json()["uninstalled"] is True

    again = client.post("/api/v1/marketplace/uninstall/demo-ext")
    assert again.status_code == 404


def test_ontology_packs_list_and_detail(client: TestClient) -> None:
    listing = client.get("/api/v1/ontology/packs")
    assert listing.status_code == 200
    names = {p["name"] for p in listing.json()["packs"]}
    assert "bfsi" in names

    detail = client.get("/api/v1/ontology/packs/bfsi")
    assert detail.status_code == 200
    body = detail.json()
    assert body["name"] == "bfsi"
    assert body["valid"] is True

    missing = client.get("/api/v1/ontology/packs/no-such-pack")
    assert missing.status_code == 404


def test_kgci_run_returns_report_with_stages(client: TestClient) -> None:
    report = client.post("/api/v1/kgci/run", json={})
    assert report.status_code == 200
    body = report.json()
    assert body["stages"]
    assert {s["stage"] for s in body["stages"]} >= {
        "lint",
        "schema_validation",
        "security",
        "publish",
    }

    last = client.get("/api/v1/kgci/report")
    assert last.status_code == 200
    assert last.json()["id"] == body["id"]


def test_ops_preflight_and_support_bundle(client: TestClient) -> None:
    preflight = client.get("/api/v1/ops/preflight")
    assert preflight.status_code == 200
    body = preflight.json()
    assert body["checks"]
    assert any(c["name"] == "graph_store" for c in body["checks"])

    plan = client.post(
        "/api/v1/ops/upgrade-plan",
        json={"current_version": "1.0.0", "target_version": "1.1.0"},
    )
    assert plan.status_code == 200
    assert plan.json()["target_version"] == "1.1.0"

    bundle = client.get("/api/v1/ops/support-bundle")
    assert bundle.status_code == 200
    assert "versions" in bundle.json()


def test_metrics_endpoint_returns_prometheus_text(client: TestClient) -> None:
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert "# HELP http_requests_total" in response.text
    assert "http_request_duration_seconds" in response.text


def test_embeddings_health_reports_provider(client: TestClient) -> None:
    response = client.get("/api/v1/health/embeddings")
    assert response.status_code == 200
    body = response.json()
    assert body["provider"] in ("ollama", "test-hashing")
    assert isinstance(body["healthy"], bool)
    assert isinstance(body["dim"], int)
    if os.getenv("EOIP_OLLAMA_EMBED_MODEL"):
        assert body["provider"] == "ollama"
    else:
        # CRA-025.7: without a configured model the lexical embedder is reported as test-hashing.
        assert body["provider"] == "test-hashing" and body["family"] == "test-hashing"
        assert body["dim"] == 256
