"""SPARQL 1.1 Protocol endpoint ``/api/v1/sparql`` through the real app and auth middleware
(CRA-024.7; decisions D-CRA-024-02 interface, D-CRA-024-04 auth/tenancy).

Covers: no anonymous access (401), deny-by-default role policy (unknown role 403, viewer and above
allowed, GET and POST), tenant taken from the verified identity only (headers/params ignored),
read-only (updates 400), 405 for other methods, 415 for other content types, one ``query`` only,
strict UTF-8, content negotiation (JSON/XML/CSV/TSV, q-values, 406), protocol dataset parameters.
"""
from __future__ import annotations

import hashlib
import json
import os
import urllib.parse

import pytest
from eoip.authn import Principal, TokenService
from eoip.graph.memory import MemoryGraphStore
from eoip.query import sparql_router
from eoip.query.sparql_backend import RdflibSparqlBackend
from eoip.query.sparql_protocol import negotiate
from fastapi.testclient import TestClient

import apps.api.main as api_main
from _principals import ProvisioningTokenService, provision_login_user
from apps.api import route_policy

pytestmark = pytest.mark.req("CRA-024", "SR-CON-011")
URL = "/api/v1/sparql"
TOKENS = [("tok-viewer-0123456789", "viewer", "beta")]
DATA = {"alpha": "<urn:a1> a <urn:T> ; <urn:name> \"alpha-one\" .", "beta": "<urn:b1> a <urn:T> ."}


@pytest.fixture(scope="module")
def api(tmp_path_factory):
    root = tmp_path_factory.mktemp("sparqlep")
    secret = b"s" * 32
    provision_login_user(None, root, "sparql-admin", roles=("superadmin",))
    svc = ProvisioningTokenService(TokenService(secret, issuer="eoip-authn", audience="eoip-api"), root)
    seen: list[str] = []

    def backend(tenant: str):
        seen.append(tenant)
        b = RdflibSparqlBackend()
        b.load_turtle(DATA.get(tenant, ""))
        return b

    mp = pytest.MonkeyPatch()
    asg = root / "asg.txt"  # API tokens: the ASG file is loaded when the app is built
    asg.write_text("".join(f"sha256:{hashlib.sha256(t.encode()).hexdigest()} | {role} | {ten} | {t}\n"
                           for t, role, ten in TOKENS), encoding="utf-8")
    os.chmod(asg, 0o400)
    mp.setenv("EOIP_ASG_FILE", str(asg))
    mp.setenv("EOIP_SESSION_SECRET", secret.decode())
    mp.setattr(api_main, "create_store", MemoryGraphStore)
    mp.setattr(api_main, "data_root", lambda: root)
    mp.setattr(sparql_router, "_configured_backend", backend)
    app = api_main.create_app()
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client, svc, seen
    mp.undo()


def _auth(svc, role="viewer", tenant="alpha"):
    uid = f"u-{role}-{tenant}"
    return {"Authorization": f"Bearer {svc.issue(Principal(uid, uid, (role,), tenant_id=tenant))}"}


Q = "SELECT ?s WHERE { ?s a <urn:T> }"


def test_anonymous_is_refused_for_get_and_post(api):
    client, _, _ = api
    assert client.get(URL, params={"query": Q}).status_code == 401
    assert client.post(URL, content=Q, headers={"Content-Type": "application/sparql-query"}).status_code == 401
    assert client.get(URL, params={"query": Q}, headers={"Authorization": "Bearer forged"}).status_code == 401


@pytest.mark.parametrize("roles", [("guest",), ("nobody", "contractor"), ()])
def test_unknown_roles_are_denied_by_default(roles):
    # The identity layer only issues known roles (credential store and ASG refuse others), so a principal
    # with an unknown or empty role set is injected directly: the route's own policy check must deny it.
    from fastapi import FastAPI

    app = FastAPI()

    @app.middleware("http")
    async def _inject(request, call_next):
        if request.headers.get("x-test-principal"):
            request.state.principal = Principal("u-x", "u-x", roles, tenant_id="alpha")
        return await call_next(request)

    app.include_router(sparql_router.build_sparql_router(route_policy.allowed, lambda t: RdflibSparqlBackend()))
    with TestClient(app) as c:
        h = {"x-test-principal": "1"}
        assert c.get(URL, params={"query": Q}, headers=h).status_code == 403
        assert c.post(URL, data={"query": Q}, headers=h).status_code == 403
        assert c.get(URL, params={"query": Q}).status_code == 401  # no principal: never anonymous


def test_api_token_viewer_can_query(api):
    client, _, seen = api
    seen.clear()
    r = client.get(URL, params={"query": Q}, headers={"Authorization": "Bearer tok-viewer-0123456789"})
    assert r.status_code == 200 and seen == ["beta"]


@pytest.mark.parametrize("role", ["viewer", "analyst", "steward", "admin"])
def test_viewer_and_above_can_query(api, role):
    client, svc, _ = api
    r = client.get(URL, params={"query": Q}, headers={**_auth(svc, role), "Accept": "application/sparql-results+json"})
    assert r.status_code == 200, r.text
    assert [b["s"]["value"] for b in r.json()["results"]["bindings"]] == ["urn:a1"]
    assert route_policy.classify("POST", URL) == "read"


def test_platform_superadmin_without_tenant_gets_the_default_dataset(api):
    client, svc, seen = api
    seen.clear()
    r = client.get(URL, params={"query": Q}, headers=_auth(svc, "superadmin", None))
    assert r.status_code == 200 and seen == ["default"]


def test_tenant_comes_from_identity_never_the_request(api):
    client, svc, seen = api
    seen.clear()
    r = client.post(URL + "?tenant=beta", data={"query": Q, "tenant": "beta"},
                    headers={**_auth(svc, "viewer", "alpha"), "X-EOIP-Tenant": "beta"})
    assert r.status_code == 200
    assert seen == ["alpha"]
    assert [b["s"]["value"] for b in r.json()["results"]["bindings"]] == ["urn:a1"]
    seen.clear()  # a conflicting X-Tenant-Id is refused by the tenancy guard or ignored, never honoured
    r = client.get(URL, params={"query": Q}, headers={**_auth(svc, "viewer", "alpha"), "X-Tenant-Id": "beta"})
    assert "beta" not in seen and (r.status_code == 403 or seen == ["alpha"])
    seen.clear()
    r = client.get(URL, params={"query": Q}, headers=_auth(svc, "viewer", "beta"))
    assert seen == ["beta"] and [b["s"]["value"] for b in r.json()["results"]["bindings"]] == ["urn:b1"]


def test_post_forms(api):
    client, svc, _ = api
    h = _auth(svc)
    assert client.post(URL, data={"query": Q}, headers=h).status_code == 200
    r = client.post(URL, content=Q.encode(), headers={**h, "Content-Type": "application/sparql-query; charset=utf-8"})
    assert r.status_code == 200
    assert client.post(URL, content=Q, headers={**h, "Content-Type": "text/plain"}).status_code == 415
    assert client.post(URL, content=Q, headers={**h, "Content-Type": "application/json"}).status_code == 415


@pytest.mark.parametrize("call", [
    lambda c, h: c.get(URL, params={"update": "INSERT DATA { <urn:x> <urn:p> 1 }"}, headers=h),
    lambda c, h: c.post(URL, data={"update": "CLEAR ALL"}, headers=h),
    lambda c, h: c.post(URL, content="DROP ALL", headers={**h, "Content-Type": "application/sparql-update"}),
    lambda c, h: c.post(URL, data={"query": "INSERT DATA { <urn:x> <urn:p> 1 }"}, headers=h),
])
def test_endpoint_is_read_only(api, call):
    client, svc, _ = api
    assert call(client, _auth(svc, "admin")).status_code == 400


def test_other_methods_are_not_allowed(api):
    client, svc, _ = api
    r = client.request("PUT", URL, content=Q, headers=_auth(svc, "admin"))
    assert r.status_code == 405 and r.headers["allow"] == "GET, POST"
    assert client.request("DELETE", URL, headers=_auth(svc, "viewer")).status_code in (403, 405)


def test_malformed_requests(api):
    client, svc, _ = api
    h = _auth(svc)
    assert client.get(URL, headers=h).status_code == 400
    two = urllib.parse.urlencode([("query", Q), ("query", Q)])
    assert client.get(f"{URL}?{two}", headers=h).status_code == 400
    assert client.post(URL, content=two, headers={**h, "Content-Type": "application/x-www-form-urlencoded"}
                       ).status_code == 400
    assert client.get(URL, params={"query": "SELECT ?s WHERE { ?s ?p }"}, headers=h).status_code == 400
    assert client.get(f"{URL}?query=SELECT%FF", headers=h).status_code == 400
    assert client.post(URL, content=b"SELECT * { ?s ?p \xff }",
                       headers={**h, "Content-Type": "application/sparql-query"}).status_code == 400


@pytest.mark.parametrize("accept, ctype", [
    (None, "application/sparql-results+json"), ("*/*", "application/sparql-results+json"),
    ("application/sparql-results+json", "application/sparql-results+json"),
    ("application/sparql-results+xml", "application/sparql-results+xml"),
    ("text/csv", "text/csv"), ("text/tab-separated-values", "text/tab-separated-values"),
    ("text/csv;q=0.2, application/sparql-results+xml;q=0.9", "application/sparql-results+xml"),
    ("application/sparql-results+json;q=0, text/tab-separated-values", "text/tab-separated-values"),
])
def test_content_negotiation(api, accept, ctype):
    client, svc, _ = api
    h = _auth(svc) | ({"Accept": accept} if accept else {})
    r = client.get(URL, params={"query": Q}, headers=h)
    assert r.status_code == 200 and r.headers["content-type"].startswith(ctype)
    if ctype.endswith("json"):
        assert json.loads(r.text)["head"]["vars"] == ["s"]
    elif ctype.endswith("xml"):
        assert "<sparql" in r.text and "urn:a1" in r.text
    else:
        assert "urn:a1" in r.text


def test_not_acceptable(api):
    client, svc, _ = api
    r = client.get(URL, params={"query": Q}, headers={**_auth(svc), "Accept": "image/png"})
    assert r.status_code == 406
    r = client.get(URL, params={"query": "ASK { ?s ?p ?o }"}, headers={**_auth(svc), "Accept": "text/csv"})
    assert r.status_code == 406
    r = client.get(URL, params={"query": "ASK { ?s ?p ?o }"}, headers={**_auth(svc), "Accept": "application/sparql-results+xml"})
    assert r.status_code == 200 and "<boolean>true</boolean>" in r.text


def test_negotiate_unit():
    assert negotiate("") == "json" and negotiate("text/*") == "csv" and negotiate("application/*") == "json"
    assert negotiate("text/csv", ask=True) is None and negotiate("text/*", ask=True) == "xml"
    assert negotiate("application/xml;q=0.5, application/json;q=0.5") == "xml"


def test_dataset_parameters_need_a_server_backend(api):
    client, svc, _ = api
    r = client.get(URL, params={"query": Q, "default-graph-uri": "urn:g"}, headers=_auth(svc))
    assert r.status_code == 400 and "DATASET_NOT_SUPPORTED" in r.text


def test_unconfigured_engine_is_503(monkeypatch):
    for k in ("EOIP_SPARQL_BACKEND", "EOIP_SPARQL_ENDPOINT"):
        monkeypatch.delenv(k, raising=False)
    assert sparql_router.backend_from_env("alpha") is None
    with pytest.raises(ValueError):
        sparql_router.backend_from_env("alpha", {"EOIP_SPARQL_BACKEND": "fuseki", "EOIP_SPARQL_ENDPOINT": "http://x/ds"})
    b = sparql_router.backend_from_env("alpha", {"EOIP_SPARQL_BACKEND": "graphdb",
                                                 "EOIP_SPARQL_ENDPOINT": "http://g:7200/repositories/{tenant}"})
    assert "alpha" in repr(vars(b))
