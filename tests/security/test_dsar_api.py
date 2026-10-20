"""SR-PRV-002 over HTTP: DSAR locate/export/rectify/erase run on the tenant's stores, the tenant is
taken from the authenticated principal, and only administrators may run them."""
from __future__ import annotations

import pytest
from eoip.authn import Principal, TokenService
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

import apps.api.main as api_main
from _principals import ProvisioningTokenService, provision_login_user

pytestmark = pytest.mark.req("SR-PRV-002", "SR-TEN-003")

ALICE = "alice@corp.example"


@pytest.fixture
def api(tmp_path, monkeypatch):
    secret = b"k" * 32
    provision_login_user(None, tmp_path, "contract-admin", roles=("superadmin",))
    svc = ProvisioningTokenService(TokenService(secret, issuer="eoip-authn", audience="eoip-api"), tmp_path)
    monkeypatch.setenv("EOIP_SESSION_SECRET", secret.decode())
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)
    app = api_main.create_app()
    with TestClient(app, raise_server_exceptions=False) as client:
        layers = app.state.extended_state.tenant_layers
        store = app.state.graph_store
        store.upsert_vertex("Person", {"canonical_id": "p-alpha", "email": ALICE, "display_name": "Alice Smyth"})
        a, b = layers.ensure_tenant("alpha"), layers.ensure_tenant("beta")
        a.vector_upsert("e1", [1.0], {"text": "Alice Smyth on-call", "subject_ids": [ALICE]})
        a.search_add("s1", f"incident by Alice Smyth {ALICE}", {"subject_ids": [ALICE]})
        a.cache_set("q:owners", [ALICE])
        a.put_object("raw/jira/1.json", f'{{"reporter": "{ALICE}"}}'.encode())
        a.backup("nightly", {"people": [ALICE]})
        b.vector_upsert("x1", [1.0], {"text": ALICE, "subject_ids": [ALICE]})
        yield client, svc, a, b


def _h(svc, role, tenant="alpha"):
    token = svc.issue(Principal(f"u-{role}", f"u-{role}", (role,), tenant_id=tenant))
    return {"Authorization": f"Bearer {token}"}


def test_only_admins_run_subject_requests(api):
    client, svc, *_ = api
    for verb in ("locate", "export", "rectify", "erase"):
        body = {"subject_id": ALICE, "old_value": "a", "new_value": "b"}
        assert client.post(f"/api/v1/privacy/dsar/{verb}", json=body, headers=_h(svc, "steward")).status_code == 403


def test_locate_export_rectify_erase_on_the_principals_tenant(api):
    client, svc, a, b = api
    admin = _h(svc, "admin")
    loc = client.post("/api/v1/privacy/dsar/locate", json={"subject_id": ALICE}, headers=admin)
    assert loc.status_code == 200, loc.text
    surfaces = {h["surface"] for h in loc.json()["hits"]}
    assert {"graph", "vector", "search", "cache", "raw_capture", "backup"} <= surfaces
    assert loc.json()["tenant_id"] == "alpha"

    exp = client.post("/api/v1/privacy/dsar/export", json={"subject_id": ALICE}, headers=admin).json()
    assert exp["bundle"]["data"]["vector"][0]["payload"]["text"] == "Alice Smyth on-call" and exp["proof"]["verified"]

    rect = client.post("/api/v1/privacy/dsar/rectify", headers=admin,
                       json={"subject_id": ALICE, "old_value": "Smyth", "new_value": "Smith"}).json()
    assert rect["verified"] and a.vector_items()["e1"][1]["text"] == "Alice Smith on-call"

    er = client.post("/api/v1/privacy/dsar/erase", json={"subject_id": ALICE}, headers=admin).json()
    assert er["verified"] and er["flagged"] == ["backup:nightly.bak"]
    assert a.vector_items() == {} and a.search_docs() == {} and a.cache_items() == {}
    assert "x1" in b.vector_items()  # beta's data is outside alpha's request


def test_tenant_comes_from_the_principal(api):
    client, svc, *_ = api
    spoof = client.post("/api/v1/privacy/dsar/erase", json={"subject_id": ALICE, "tenant_id": "beta"},
                        headers=_h(svc, "admin"))
    assert spoof.status_code == 403


def test_graph_events_and_logs_reach_only_the_declaring_tenants_layers(api):
    import logging

    from eoip.events.emitter import GraphEvent

    client, svc, a, b = api
    app = client.app
    app.state.event_emitter.emit_sync(GraphEvent("vertex_upserted", {"tenant_id": "alpha", "canonical_id": "p-1"}))
    app.state.event_emitter.emit_sync(GraphEvent("vertex_upserted", {"canonical_id": "untenanted"}))
    got_a = [e["data"]["canonical_id"] for e in a.layers.topics[a._p("event_topic")]]
    assert got_a == ["p-1"] and not list(b.layers.topics[b._p("event_topic")])

    logging.getLogger("eoip.test").warning("alpha secret op", extra={"tenant_id": "alpha"})
    assert [r["message"] for r in a.read_logs()] == ["alpha secret op"] and b.read_logs() == []
