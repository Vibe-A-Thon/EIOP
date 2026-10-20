"""Deny-by-default role policy over every mutating route of the composed API (D-roles).

The 2026-10-20 authz sweep found ~340 POST/PUT/PATCH/DELETE routes that any authenticated principal,
including a viewer, could call (config set/import/rollback, migrations, recovery restore, DSAR
erase, marketplace install, QA evidence registration ...). apps/api/route_policy.py now classifies
every mutating route and the HTTP middleware enforces it. These tests walk the live route table.
"""

from __future__ import annotations

import re

import pytest
from eoip.authn import Principal, TokenService
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

import apps.api.main as api_main
from _principals import ProvisioningTokenService, provision_login_user
from apps.api import route_policy

pytestmark = pytest.mark.req("SR-CON-011", "CRA-003")

DESTRUCTIVE = re.compile(r"(erase|delete|restore|rollback|apply|install|import|register|reset|clear|"
                         r"drain|kill|approve|reject|decide|commit|train|save|load|replay|revoke)", re.I)


def _walk(routes, prefix=""):
    for r in routes:
        if type(r).__name__ == "_IncludedRouter":
            yield from _walk(r.original_router.routes, prefix + (getattr(r.include_context, "prefix", "") or ""))
        else:
            yield r, prefix


@pytest.fixture(scope="module")
def api(tmp_path_factory):
    root = tmp_path_factory.mktemp("authz")
    secret = b"k" * 32
    provision_login_user(None, root, "contract-admin", roles=("superadmin",))
    svc = ProvisioningTokenService(TokenService(secret, issuer="eoip-authn", audience="eoip-api"), root)
    mp = pytest.MonkeyPatch()
    mp.setenv("EOIP_SESSION_SECRET", secret.decode())
    mp.setattr(api_main, "create_store", MemoryGraphStore)
    mp.setattr(api_main, "data_root", lambda: root)
    app = api_main.create_app()
    routes = sorted({(m, pre + r.path) for r, pre in _walk(app.routes)
                     for m in (getattr(r, "methods", None) or set()) & route_policy.MUTATING})
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client, svc, routes
    mp.undo()


def _call(client, svc, method, path, role):
    token = svc.issue(Principal(f"u-{role}", f"u-{role}", (role,), tenant_id="alpha"))
    concrete = re.sub(r"\{[^}]+\}", "x", path)
    return client.request(method, concrete, json={}, headers={"Authorization": f"Bearer {token}"}).status_code


def test_route_table_is_large_and_every_route_is_classified(api):
    _, _, routes = api
    assert len(routes) > 300
    tiers = {route_policy.classify(m, p) for m, p in routes}
    assert tiers <= {"open", "read", "analyst", "write", "admin"}


def test_no_destructive_route_is_classified_as_read(api):
    _, _, routes = api
    offenders = [(m, p) for m, p in routes if route_policy.classify(m, p) == "read" and DESTRUCTIVE.search(p)]
    assert offenders == []


@pytest.mark.parametrize("role, may", [("viewer", {"open", "read"}), ("analyst", {"open", "read", "analyst"}),
                                       ("steward", {"open", "read", "analyst", "write"})])
def test_role_reaches_only_its_tiers(api, role, may):
    client, svc, routes = api
    wrong = []
    for m, p in routes:
        if p.endswith("/auth/logout") or re.search(r"/sources/[^/]+/webhooks$", p):
            continue
        tier = route_policy.classify(m, p)
        status = _call(client, svc, m, p, role)
        if (tier in may) == (status == 403):
            wrong.append((m, p, tier, status))
    assert wrong == []


@pytest.mark.parametrize("method, path", [
    ("POST", "/api/v1/config/set"), ("POST", "/api/v1/config/rollback"),
    ("POST", "/api/v1/enterprise/migrations/apply-all"), ("POST", "/api/v1/platform/recovery/restore/x"),
    ("POST", "/api/v1/privacy/dsar/erase"), ("POST", "/api/v1/qa/evidence/register"),
    ("POST", "/api/v1/governance/kill-switch"), ("POST", "/api/v1/platform/tools/register"),
])
def test_security_sensitive_mutations_need_an_administrator(api, method, path):
    client, svc, _ = api
    assert _call(client, svc, method, path, "steward") == 403
    assert _call(client, svc, method, path, "admin") != 403


def test_unknown_roles_get_no_mutating_access():
    assert route_policy.allowed("POST", "/api/v1/query", ["reader"]) is False
    assert route_policy.allowed("POST", "/api/v1/auth/login", []) is True
    assert route_policy.allowed("GET", "/api/v1/anything", ["viewer"]) is True
    assert route_policy.allowed("POST", "/api/v1/brand-new-route", ["analyst"]) is False  # default: steward
    assert route_policy.allowed("POST", "/api/v1/brand-new-route", ["steward"]) is True


@pytest.fixture
def reva_api(tmp_path, monkeypatch):
    from reva import config as reva_config

    root = tmp_path
    secret = b"k" * 32
    provision_login_user(None, root, "contract-admin", roles=("superadmin",))
    svc = ProvisioningTokenService(TokenService(secret, issuer="eoip-authn", audience="eoip-api"), root)
    monkeypatch.setenv("EOIP_SESSION_SECRET", secret.decode())
    reva_config.set_settings(reva_config.RevaSettings(enabled=True))
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: root)
    seen = {}
    import reva.api.routes_gaps as gaps

    monkeypatch.setattr(gaps, "get_kernel", lambda: type("K", (), {"store": None})())
    monkeypatch.setattr(gaps, "record_gap", lambda **kw: seen.update(kw) or {"gap_id": "g1"})
    app = api_main.create_app()
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client, svc, seen
    reva_config.set_settings(None)


def test_reva_writes_need_steward_and_bind_tenant_and_actor_to_the_session(reva_api):
    client, svc, seen = reva_api
    body = {"domain": "d", "question": "q?", "scope": {}, "severity": "low"}
    viewer = svc.issue(Principal("v1", "v1", ("viewer",), tenant_id="alpha"))
    assert client.post("/api/reva/v1/gaps", json=body,
                       headers={"Authorization": f"Bearer {viewer}"}).status_code == 403
    steward = svc.issue(Principal("s1", "s1", ("steward",), tenant_id="alpha"))
    r = client.post("/api/reva/v1/gaps", json=body,
                    headers={"Authorization": f"Bearer {steward}", "X-Principal-Id": "someone-else"})
    assert r.status_code == 200, r.text
    assert seen["tenant_id"] == "alpha" and seen["actor"] == "s1"
    spoof = client.post("/api/reva/v1/gaps", json=body,
                        headers={"Authorization": f"Bearer {steward}", "X-Tenant-Id": "beta"})
    assert spoof.status_code == 403
    assert route_policy.classify("POST", "/api/reva/v1/warrants/query") == "read"
    assert route_policy.classify("POST", "/api/reva/v1/warrants/w1/retract") == "write"
