"""W3C SPARQL 1.1 Protocol test suite against EOIP's ``/api/v1/sparql`` on live engines (CRA-024.7).

Every request goes through the real app: auth middleware, route policy (a viewer session token),
tenant-from-identity dataset selection (tenant ``w3cproto`` -> a disposable engine dataset), then the
engine. Needs the pinned suite (``EOIP_W3C_SUITE``) and ``EOIP_LIVE_FUSEKI_URL`` /
``EOIP_LIVE_GRAPHDB_URL``; CI runs it in the ``sparql-fuseki`` job and fails when it is skipped.
Failures must be fixed or recorded in ``w3c_sparql11_protocol_known_gaps.json`` (stale entries fail).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from eoip.authn import Principal, TokenService
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

import apps.api.main as api_main
from _principals import ProvisioningTokenService
from eoip.query.w3c_conformance import _Store
from eoip.query.w3c_protocol import load_protocol_tests, run_protocol_tests, summarize

pytestmark = pytest.mark.req("CRA-024")
SUITE = Path(os.environ.get("EOIP_W3C_SUITE", ".cache/rdf-tests/sparql/sparql11"))
GAPS = json.loads(Path(__file__).with_name("w3c_sparql11_protocol_known_gaps.json").read_text(encoding="utf-8"))
OUT = Path(os.environ.get("EOIP_W3C_REPORT_DIR", "test-results"))
TENANT = "w3cproto"


def _backends():
    out = {}
    if os.environ.get("EOIP_LIVE_FUSEKI_URL"):
        server = os.environ["EOIP_LIVE_FUSEKI_URL"].rstrip("/").rsplit("/", 1)[0]
        out["fuseki"] = (server, (os.environ.get("EOIP_LIVE_FUSEKI_USER", "admin"),
                                  os.environ.get("EOIP_LIVE_FUSEKI_PASSWORD", "")))
    if os.environ.get("EOIP_LIVE_GRAPHDB_URL"):
        out["graphdb"] = (os.environ["EOIP_LIVE_GRAPHDB_URL"].rstrip("/"), None)
    return out


def test_manifest_parses_offline():
    if not (SUITE / "protocol" / "manifest.ttl").exists():
        pytest.skip("W3C suite not fetched")
    tests = load_protocol_tests(SUITE)
    assert len(tests) == 34 and all(t.requests for t in tests)


def test_manifest_parses_from_a_relative_suite_path(monkeypatch):
    """CI passes EOIP_W3C_SUITE as a relative path; file URIs need an absolute one."""
    if not (SUITE / "protocol" / "manifest.ttl").exists():
        pytest.skip("W3C suite not fetched")
    monkeypatch.chdir(SUITE.resolve().parent)
    assert len(load_protocol_tests(Path(SUITE.resolve().name))) == 34


@pytest.mark.skipif(not (SUITE / "protocol" / "manifest.ttl").exists(), reason="W3C suite not fetched")
@pytest.mark.parametrize("backend", sorted(_backends()) or ["none"])
def test_w3c_sparql11_protocol_suite(backend, tmp_path, monkeypatch):
    conf = _backends()
    if backend not in conf:
        pytest.skip("no live Fuseki/GraphDB configured")
    server, auth = conf[backend]
    store = _Store(backend, server, TENANT, auth)
    store.create()
    store.clear()
    secret = b"p" * 32
    svc = ProvisioningTokenService(TokenService(secret, issuer="eoip-authn", audience="eoip-api"), tmp_path)
    monkeypatch.setenv("EOIP_SESSION_SECRET", secret.decode())
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)
    monkeypatch.setenv("EOIP_SPARQL_BACKEND", backend)
    monkeypatch.setenv("EOIP_SPARQL_ENDPOINT", store.query_endpoint.replace(f"/{TENANT}", "/{tenant}"))
    monkeypatch.setenv("EOIP_SPARQL_USER", (auth or ("", ""))[0])
    monkeypatch.setenv("EOIP_SPARQL_PASSWORD", (auth or ("", ""))[1])
    token = svc.issue(Principal("w3c-viewer", "w3c-viewer", ("viewer",), tenant_id=TENANT))
    app = api_main.create_app()
    with TestClient(app, raise_server_exceptions=False) as client:
        def call(method, path, headers, body):
            r = client.request(method, path, headers={**headers, "Authorization": f"Bearer {token}"}, content=body)
            return r.status_code, dict(r.headers), r.text

        tests = load_protocol_tests(SUITE)
        outcomes = run_protocol_tests(tests, call, lambda p, iri: store.load(p, iri, iri))
    by_id = {o.id: o for o in outcomes}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"w3c-sparql11-protocol-{backend}.json").write_text(json.dumps(
        {"backend": backend, "summary": summarize(outcomes), "outcomes": [o.__dict__ for o in outcomes]},
        indent=2), encoding="utf-8")
    assert len(outcomes) == len(tests) == 34
    known = GAPS["known_gaps"].get(backend, {})
    unexpected = [f"{o.id}: {o.detail}" for o in outcomes if o.outcome == "fail" and o.id not in known]
    assert not unexpected, "new protocol failures:\n" + "\n".join(unexpected)
    stale = [t for t in known if by_id[t].outcome != "fail"]
    assert not stale, f"recorded gaps that now pass (remove them): {stale}"
    for o in outcomes:
        if o.outcome == "rejected_by_design":
            assert o.statuses[-1] in (400, 422)
