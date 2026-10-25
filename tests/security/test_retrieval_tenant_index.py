"""SR-TEN-003 / SR-PRV-002 / CRA-025.3: retrieval search runs on the tenant's own index layers.

Keyword and vector candidates come from the tenant's search-index and vector-collection layers, graph
expansion and seeds are limited to the tenant's entities, another tenant's ids look absent, and the documents
retrieval serves are exactly the ones the HTTP DSAR workflow locates and erases."""
from __future__ import annotations

import pytest
from eoip.authn import Principal, TokenService
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

import apps.api.main as api_main
from _principals import ProvisioningTokenService, provision_login_user

pytestmark = pytest.mark.req("SR-TEN-003", "SR-PRV-002", "CRA-025")

ALICE = "alice@corp.example"


@pytest.fixture
def api(tmp_path, monkeypatch):
    secret = b"k" * 32
    provision_login_user(None, tmp_path, "contract-admin", roles=("superadmin",))
    svc = ProvisioningTokenService(TokenService(secret, issuer="eoip-authn", audience="eoip-api"), tmp_path)
    monkeypatch.setenv("EOIP_SESSION_SECRET", secret.decode())
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path / "data"))  # tenant layers isolated per test
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)
    app = api_main.create_app()
    with TestClient(app, raise_server_exceptions=False) as client:
        store = app.state.graph_store
        layers = app.state.extended_state.tenant_layers
        for t in ("alpha", "beta"):
            store.upsert_vertex("Service", {"canonical_id": f"svc-{t}", "tenant_id": t,
                                            "name": f"payments gateway {t}", "description": "payment outage runbook"})
        store.upsert_vertex("Person", {"canonical_id": "p-alice", "tenant_id": "alpha", "email": ALICE,
                                       "display_name": "Alice Smyth", "description": "payment outage on-call"})
        store.upsert_vertex("Service", {"canonical_id": "svc-unowned", "name": "payments gateway legacy",
                                        "description": "payment outage runbook"})
        store.upsert_edge("DEPENDS_ON", "svc-alpha", "svc-beta", {})  # a cross-tenant edge must not leak
        yield client, svc, store, layers


def _h(svc, role="analyst", tenant="alpha", **extra):
    token = svc.issue(Principal(f"u-{role}-{tenant}", f"u-{role}-{tenant}", (role,), tenant_id=tenant))
    return {"Authorization": f"Bearer {token}", **extra}


def _ids(resp):
    assert resp.status_code == 200, resp.text
    body = resp.json()
    ids = {c.get("canonical_id") for c in body.get("contexts", [])}
    ids |= {c for c in body.get("evidence_refs", []) if isinstance(c, str) and c.startswith(("svc-", "p-"))}
    return ids - {None}


@pytest.mark.parametrize("strategy", ["keyword", "vector", "hybrid"])
def test_each_tenant_only_sees_its_own_entities(api, strategy):
    client, svc, *_ = api
    q = {"question": "payment outage runbook payments gateway", "strategy": strategy, "top_k": 10}
    alpha = _ids(client.post("/api/v1/retrieval/search", json=q, headers=_h(svc, tenant="alpha")))
    beta = _ids(client.post("/api/v1/retrieval/search", json=q, headers=_h(svc, tenant="beta")))
    assert alpha and alpha <= {"svc-alpha", "p-alice"}
    assert beta == {"svc-beta"}


def test_index_lives_in_the_tenant_layers(api):
    client, svc, store, layers = api
    client.post("/api/v1/retrieval/search", json={"question": "payment", "strategy": "hybrid"}, headers=_h(svc))
    a, b = layers.ensure_tenant("alpha"), layers.ensure_tenant("beta")
    assert set(a.search_docs()) == {"svc-alpha", "p-alice"} and set(a.vector_items()) == {"svc-alpha", "p-alice"}
    assert set(b.search_docs()) == set()  # beta has not searched yet; nothing of alpha's is in beta's layers
    payload = a.vector_items()["svc-alpha"][1]
    assert payload["embedder"].startswith("HashingEmbedder") and payload["dimension"] > 0  # CRA-025.1 metadata


def test_other_tenant_seed_looks_absent_and_header_spoof_is_refused(api):
    client, svc, *_ = api
    foreign = client.post("/api/v1/retrieval/search", headers=_h(svc),
                          json={"question": "payment", "canonical_id": "svc-beta", "strategy": "hybrid"})
    missing = client.post("/api/v1/retrieval/search", headers=_h(svc),
                          json={"question": "payment", "canonical_id": "svc-nope", "strategy": "hybrid"})
    assert foreign.status_code == missing.status_code == 422 and foreign.json() == missing.json()
    graph = client.post("/api/v1/retrieval/search", headers=_h(svc), json={"question": "x", "canonical_id": "svc-beta"})
    assert graph.status_code == 422
    spoof = client.post("/api/v1/retrieval/search", json={"question": "payment"},
                        headers=_h(svc, **{"X-Tenant-Id": "beta"}))
    assert spoof.status_code == 403


def test_dsar_reaches_what_retrieval_indexed_and_erasure_sticks(api):
    client, svc, store, layers = api
    q = {"question": "Alice Smyth on-call", "strategy": "keyword"}
    assert "p-alice" in _ids(client.post("/api/v1/retrieval/search", json=q, headers=_h(svc)))
    admin = _h(svc, role="admin")
    loc = client.post("/api/v1/privacy/dsar/locate", json={"subject_id": ALICE}, headers=admin).json()
    surfaces = {(h["surface"], h["ref"]) for h in loc["hits"]}
    assert ("search", "p-alice") in surfaces and ("vector", "p-alice") in surfaces
    er = client.post("/api/v1/privacy/dsar/erase", json={"subject_id": ALICE}, headers=admin).json()
    assert er["verified"]
    a = layers.ensure_tenant("alpha")
    assert "p-alice" not in a.search_docs() and "p-alice" not in a.vector_items()
    assert "p-alice" not in _ids(client.post("/api/v1/retrieval/search", json=q, headers=_h(svc)))
    assert ALICE not in client.post("/api/v1/retrieval/search", json=q, headers=_h(svc)).text
