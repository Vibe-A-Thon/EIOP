"""CORS configuration and preflights at the composed application boundary."""

from _principals import provision_api_token
import pytest
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

import apps.api.main as api_main
from apps.api.app import create_app

pytestmark = pytest.mark.security


@pytest.mark.parametrize("origin", ["*", "null", "https://example.test/path", "https://u:p@example.test",
                                   "https://example.test?x=1", "https://example.test#x", "https://example.test:99999"])
def test_invalid_cors_origin_prevents_startup(monkeypatch, origin):
    monkeypatch.setenv("EOIP_CORS_ORIGINS", origin)
    with pytest.raises(ValueError):
        create_app(MemoryGraphStore())


def test_production_has_no_implicit_localhost_origin(monkeypatch):
    monkeypatch.setenv("EOIP_ENV", "production")
    monkeypatch.delenv("EOIP_CORS_ORIGINS", raising=False)
    client = TestClient(create_app(MemoryGraphStore()))
    response = client.options("/api/v1/query", headers={
        "Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST",
    })
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_composed_api_allows_only_configured_preflight_without_bearer(monkeypatch, tmp_path):
    monkeypatch.setenv("EOIP_CORS_ORIGINS", "https://web.example.test")
    provision_api_token(monkeypatch, "test-bootstrap-key")
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    client = TestClient(api_main.create_app())
    headers = {"Origin": "https://web.example.test", "Access-Control-Request-Method": "POST",
               "Access-Control-Request-Headers": "authorization,content-type"}
    response = client.options("/api/v1/query", headers=headers)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == headers["Origin"]
    headers["Origin"] = "https://attacker.example.test"
    response = client.options("/api/v1/query", headers=headers)
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers
    assert client.post("/api/v1/query", json={}, headers={"Origin": "https://web.example.test"}).status_code == 401
