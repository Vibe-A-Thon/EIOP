from __future__ import annotations

import json

import pytest
from eoip.authn import Principal, TokenService
from eoip.enterprise.middleware import install_enterprise_middleware
from eoip.events.emitter import GraphEvent, GraphEventEmitter
from eoip.graph.memory import MemoryGraphStore
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

import apps.api.main as api_main
from _principals import ProvisioningTokenService, provision_login_user

pytestmark = [pytest.mark.security, pytest.mark.req("GAP-SEC-004", "SR-TEN-001")]


@pytest.fixture
def auth_setup(tmp_path):
    secret = b"k" * 32
    secret_str = secret.decode("ascii")
    provision_login_user(None, tmp_path, "contract-admin", roles=("superadmin",))  # the API needs >= 1 principal
    token_service = ProvisioningTokenService(
        TokenService(secret, issuer="eoip-authn", audience="eoip-api"), tmp_path)
    return secret_str, token_service, tmp_path


def test_http_boundary_accepts_signed_token_and_emits_dynamic_audit_actor(auth_setup, monkeypatch):
    secret_str, token_service, tmp_path = auth_setup
    monkeypatch.setenv("EOIP_SESSION_SECRET", secret_str)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)

    app = api_main.create_app()
    client = TestClient(app)

    principal = Principal(
        id="urn:eoip:authn:principal:alice",
        username="alice",
        roles=("admin", "developer"),
        provider="local",
        tenant_id="tenant-alpha",
    )
    token = token_service.issue(principal)

    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/api/v1/ontology/export?limit=5", headers=headers)
    assert resp.status_code == 200

    # Verify audit event emitted with actor="alice" instead of "local-user"
    audit_files = list((tmp_path / "audit").glob("*.jsonl"))
    assert len(audit_files) > 0
    records = []
    for f in audit_files:
        for line in f.read_text(encoding="utf-8").strip().splitlines():
            if line:
                records.append(json.loads(line))
    actors = [r.get("actor") for r in records]
    assert "alice" in actors
    assert "local-user" not in actors


def test_http_boundary_rejects_tampered_or_expired_token(auth_setup, monkeypatch):
    secret_str, token_service, tmp_path = auth_setup
    monkeypatch.setenv("EOIP_SESSION_SECRET", secret_str)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)

    client = TestClient(api_main.create_app())

    principal = Principal(id="p1", username="bob")
    valid_token = token_service.issue(principal)
    tampered_token = valid_token[:-4] + "wxyz"

    res = client.get("/api/v1/ontology/export", headers={"Authorization": f"Bearer {tampered_token}"})
    assert res.status_code == 401
    assert "valid Bearer token" in res.json().get("detail", "")

    # Expired token
    expired_token = token_service.issue(principal, ttl_seconds=-10)
    res_exp = client.get("/api/v1/ontology/export", headers={"Authorization": f"Bearer {expired_token}"})
    assert res_exp.status_code == 401


def test_websocket_unauthenticated_handshake_rejects_without_500(auth_setup, monkeypatch):
    secret_str, _, tmp_path = auth_setup
    monkeypatch.setenv("EOIP_SESSION_SECRET", secret_str)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)

    client = TestClient(api_main.create_app())

    # Connecting with no credentials should be closed with code 1008
    with pytest.raises(WebSocketDisconnect) as exc, client.websocket_connect("/ws/graph/events"):
        pass
    assert exc.value.code == 1008


def test_websocket_authenticated_and_tenant_isolated(auth_setup, monkeypatch):
    secret_str, token_service, tmp_path = auth_setup
    monkeypatch.setenv("EOIP_SESSION_SECRET", secret_str)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)

    app = api_main.create_app()
    client = TestClient(app)

    principal_alpha = Principal(
        id="urn:eoip:authn:principal:alice",
        username="alice",
        roles=("viewer",),
        tenant_id="tenant-alpha",
    )
    token_alpha = token_service.issue(principal_alpha)

    # Attempting to connect with mismatched tenant header/param should fail with 1008
    with (
        pytest.raises(WebSocketDisconnect) as exc,
        client.websocket_connect(f"/ws/graph/events?token={token_alpha}&tenant_id=tenant-beta"),
    ):
        pass
    assert exc.value.code == 1008

    # Connecting with matching tenant succeeds
    with client.websocket_connect(f"/ws/graph/events?token={token_alpha}") as ws:
        emitter: GraphEventEmitter = app.state.event_emitter
        # Emit an event belonging to tenant-beta (should be ignored by alice)
        emitter.emit_sync(GraphEvent("vertex_upserted", {"canonical_id": "g:tenant-beta:CodeSymbol:foo", "tenant_id": "tenant-beta"}))
        # Emit an event belonging to tenant-alpha
        emitter.emit_sync(GraphEvent("vertex_upserted", {"canonical_id": "g:tenant-alpha:CodeSymbol:bar", "tenant_id": "tenant-alpha"}))

        # Alice should only receive tenant-alpha's event
        data = ws.receive_json()
        assert data["data"]["tenant_id"] == "tenant-alpha"
        assert "g:tenant-alpha" in data["data"]["canonical_id"]


def test_brain_llm_stream_incremental_sse(auth_setup, monkeypatch):
    secret_str, token_service, tmp_path = auth_setup
    monkeypatch.setenv("EOIP_SESSION_SECRET", secret_str)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)

    client = TestClient(api_main.create_app())
    headers = {
        "Authorization": "Bearer " + token_service.issue(
            Principal("urn:eoip:authn:principal:sse", "sse-user", ("analyst",), tenant_id="default")),
        "Accept": "text/event-stream",
    }
    resp = client.post(
        "/api/v1/brain/llm/stream",
        json={"prompt": "Streaming test", "tier": "HAIKU_REALTIME", "stream": True},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/event-stream")
    lines = [line for line in resp.text.split("\n") if line.strip()]
    assert any(line.startswith("data: {") for line in lines)
    assert lines[-1] == "data: [DONE]"


def test_enterprise_middleware_tenant_isolation_cross_tenant_denial():
    # Calling with principal set to tenant-alpha but requesting tenant-beta
    # Simulate a request where principal has tenant_id="tenant-alpha"
    from starlette.requests import Request

    app_sim = FastAPI()
    install_enterprise_middleware(app_sim)

    @app_sim.middleware("http")
    async def inject_principal(request: Request, call_next):
        request.state.principal = Principal(
            id="p1",
            username="user1",
            roles=("viewer",),
            tenant_id="tenant-alpha",
        )
        return await call_next(request)

    @app_sim.get("/data")
    def data_endpoint():
        return {"data": 123}

    client_sim = TestClient(app_sim)
    
    # Matching tenant should succeed
    resp_ok = client_sim.get("/data", headers={"X-Tenant-ID": "tenant-alpha"})
    assert resp_ok.status_code == 200

    # Cross-tenant spoofing attempt should be forbidden with 403
    resp_spoof = client_sim.get("/data", headers={"X-Tenant-ID": "tenant-beta"})
    assert resp_spoof.status_code == 403
    assert resp_spoof.json()["error"]["code"] == "EOIP-AUTHZ-003"
    assert "Cross-tenant access forbidden" in resp_spoof.json()["error"]["message"]


@pytest.fixture
def composed_app(auth_setup, monkeypatch):
    secret, service, root = auth_setup
    monkeypatch.setenv("EOIP_SESSION_SECRET", secret)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: root)
    app = api_main.create_app()
    with TestClient(app) as client:
        yield app, client, service


@pytest.mark.parametrize("tenant", ["tenant-alpha", "default"])
def test_stream_and_poll_hide_unscoped_and_other_tenant_events(composed_app, tenant):
    app, client, service = composed_app
    token = service.issue(Principal("alice", "alice", ("viewer",), tenant_id=tenant))
    headers = {"Authorization": f"Bearer {token}"}
    emitter = app.state.event_emitter
    with client.websocket_connect("/ws/graph/events", headers=headers) as ws:
        for data in ({}, {"tenant_id": "tenant-beta"},
                     {"tenant_id": tenant, "canonical_id": "g:tenant-beta:node:1"}):
            emitter.emit_sync(GraphEvent("vertex_upserted", data))
        emitter.emit_sync(GraphEvent("vertex_upserted", {"tenant_id": tenant, "value": "allowed"}))
        assert ws.receive_json()["data"]["value"] == "allowed"
    for params in ({}, {"since": "2000"}, {"since_id": 1}):
        response = client.get("/api/v1/graph/events", params=params, headers=headers)
        assert response.status_code == 200
        assert [e["data"]["value"] for e in response.json()["events"]] == ["allowed"]
    assert emitter.subscriber_count == 0


@pytest.mark.parametrize("tenant,roles", [(None, ("viewer",)), ("tenant-alpha", ("admin",))])
def test_unbound_viewer_and_tenant_admin_cannot_choose_another_tenant(composed_app, tenant, roles):
    _, client, service = composed_app
    token = service.issue(Principal("alice", "alice", roles, tenant_id=tenant))
    headers = {"Authorization": f"Bearer {token}", "X-Tenant-ID": "tenant-beta"}
    assert client.get("/api/v1/graph/events", headers=headers).status_code == 403
    with (
        pytest.raises(WebSocketDisconnect) as exc,
        client.websocket_connect("/ws/graph/events", headers=headers),
    ):
        pass
    assert exc.value.code == 1008


@pytest.mark.parametrize("path", ["/api/v1/admin/demo", "/api/v1/authz/roles",
                                  "/api/v1/security/tokens/issue", "/api/v1/sources"])
def test_viewer_cannot_mutate_administrative_surfaces(composed_app, path):
    _, client, service = composed_app
    token = service.issue(Principal("alice", "alice", ("viewer",), tenant_id="alpha"))
    response = client.post(path, json={}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Administrative role required"


def test_idle_websocket_disconnect_releases_subscription(composed_app):
    import time
    app, client, service = composed_app
    token = service.issue(Principal("alice", "alice", ("viewer",), tenant_id="alpha"))
    with client.websocket_connect("/ws/graph/events", headers={"Authorization": f"Bearer {token}"}):
        assert app.state.event_emitter.subscriber_count == 1
    for _ in range(50):
        if app.state.event_emitter.subscriber_count == 0:
            break
        time.sleep(0.01)
    assert app.state.event_emitter.subscriber_count == 0


def test_tenancy_dependency_uses_signed_identity_not_spoofed_principal_header(composed_app):
    _, client, service = composed_app
    token = service.issue(Principal("signed-alice", "alice", ("viewer",), tenant_id="alpha"))
    response = client.get("/api/v1/tenancy/context", headers={
        "Authorization": f"Bearer {token}", "X-Principal": "forged-admin",
    })
    assert response.status_code == 200
    assert response.json()["principal"] == "signed-alice"
    assert response.json()["tenant_id"] == "alpha"


def test_websocket_closes_when_authenticated_token_expires(composed_app, monkeypatch):
    app, client, service = composed_app
    token = service.issue(Principal("alice", "alice", ("viewer",), tenant_id="alpha"))
    claims = service.validate(token)
    monkeypatch.setattr(api_main, "time", lambda: claims["exp"] + 1)
    with client.websocket_connect("/ws/graph/events", headers={"Authorization": f"Bearer {token}"}) as ws:
        with pytest.raises(WebSocketDisconnect) as exc:
            ws.receive_json()
        assert exc.value.code == 1008
    assert app.state.event_emitter.subscriber_count == 0


def test_cross_tenant_isolation_on_entity_and_ontology_routes(composed_app):
    from eoip.ontology.rdf import export_jsonld

    app, client, service = composed_app
    token_alpha = service.issue(Principal("alice", "alice", ("admin", "developer"), tenant_id="tenant-alpha"))
    token_beta = service.issue(Principal("bob", "bob", ("admin", "developer"), tenant_id="tenant-beta"))

    headers_alpha = {"Authorization": f"Bearer {token_alpha}"}
    headers_beta = {"Authorization": f"Bearer {token_beta}"}

    # Generate test JSON-LD payload with 1 WorkItem
    source = MemoryGraphStore()
    source.upsert_vertex("WorkItem", {"canonical_id": "item-101", "issue_key": "ALPHA-101", "summary": "Tenant Alpha WorkItem"})
    doc = export_jsonld(source)

    # 1. Tenant-alpha imports data
    imp_resp = client.post("/api/v1/ontology/import", json=doc, headers=headers_alpha)
    assert imp_resp.status_code == 200
    assert imp_resp.json()["vertices"] == 1

    # 2. Tenant-alpha can access the entity
    get_alpha = client.get("/api/v1/entities/item-101", headers=headers_alpha)
    assert get_alpha.status_code == 200
    assert get_alpha.json()["entity"]["properties"]["issue_key"] == "ALPHA-101"

    # 3. Tenant-beta CANNOT access the entity (404 Not Found)
    get_beta = client.get("/api/v1/entities/item-101", headers=headers_beta)
    assert get_beta.status_code == 404

    # 4. Tenant-beta export does NOT include tenant-alpha's entity
    export_beta = client.get("/api/v1/ontology/export", headers=headers_beta)
    assert export_beta.status_code == 200
    beta_nodes = [n for n in export_beta.json().get("@graph", []) if "eoip:entity/WorkItem" in n.get("@type", [])]
    assert len(beta_nodes) == 0

    # 5. Tenant-alpha export DOES include the entity
    export_alpha = client.get("/api/v1/ontology/export", headers=headers_alpha)
    assert export_alpha.status_code == 200
    alpha_nodes = [n for n in export_alpha.json().get("@graph", []) if "eoip:entity/WorkItem" in n.get("@type", [])]
    assert len(alpha_nodes) == 1

    # 6. Tenant-beta cannot delete tenant-alpha's entity
    del_beta = client.post("/api/v1/admin/entities/item-101/delete", headers=headers_beta)
    assert del_beta.status_code == 404

    # 7. Tenant-alpha can delete their entity
    del_alpha = client.post("/api/v1/admin/entities/item-101/delete", headers=headers_alpha)
    assert del_alpha.status_code == 200
    assert del_alpha.json()["status"] == "DELETED"


def test_admin_jobs_and_runs_cross_tenant_isolation(composed_app):
    app, client, service = composed_app
    token_alpha = service.issue(Principal("alice", "alice", ("admin",), tenant_id="tenant-alpha"))
    token_beta = service.issue(Principal("bob", "bob", ("admin",), tenant_id="tenant-beta"))

    headers_alpha = {"Authorization": f"Bearer {token_alpha}"}
    headers_beta = {"Authorization": f"Bearer {token_beta}"}

    # 1. Tenant-alpha submits an ingestion job
    submit_resp = client.post(
        "/api/v1/admin/ingestion/jira",
        json={"document": {"issues": [{"key": "A-1"}]}},
        headers=headers_alpha,
    )
    assert submit_resp.status_code == 202
    job_id = submit_resp.json()["job_id"]
    assert submit_resp.json()["tenant_id"] == "tenant-alpha"

    # 2. Tenant-alpha lists jobs -> sees own job
    jobs_alpha = client.get("/api/v1/admin/jobs", headers=headers_alpha)
    assert jobs_alpha.status_code == 200
    assert len([j for j in jobs_alpha.json() if j["job_id"] == job_id]) == 1

    # 3. Tenant-beta lists jobs -> does NOT see tenant-alpha's job
    jobs_beta = client.get("/api/v1/admin/jobs", headers=headers_beta)
    assert jobs_beta.status_code == 200
    assert len([j for j in jobs_beta.json() if j["job_id"] == job_id]) == 0

    # 4. Tenant-beta tries to inspect tenant-alpha's job -> 403
    job_get_beta = client.get(f"/api/v1/admin/jobs/{job_id}", headers=headers_beta)
    assert job_get_beta.status_code == 403
    assert "Cross-tenant" in job_get_beta.json()["detail"]

    # 5. Tenant-beta tries to cancel tenant-alpha's job -> 403
    cancel_beta = client.post(f"/api/v1/admin/jobs/{job_id}/cancel", headers=headers_beta)
    assert cancel_beta.status_code == 403

    # 6. Tenant-alpha cancels own job -> 200
    cancel_alpha = client.post(f"/api/v1/admin/jobs/{job_id}/cancel", headers=headers_alpha)
    assert cancel_alpha.status_code == 200
    assert cancel_alpha.json()["status"] == "CANCELLED"


