"""Integration tests for dormant and active REVA mounting (T-004 / OBL-REVA-IP-01)."""

import pytest
from fastapi.testclient import TestClient
from eoip.graph.memory import MemoryGraphStore
import apps.api.main as api_main
from tests.reva.support.settings import override_settings

pytestmark = pytest.mark.reva_depth("integration")


@pytest.fixture(autouse=True)
def setup_api_env(monkeypatch, tmp_path):
    monkeypatch.setattr(api_main, "api_token", lambda: "x" * 32)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)


@pytest.mark.reva_obligation("OBL-REVA-IP-01")
@pytest.mark.reva_case("positive")
def test_mount_disabled():
    with override_settings(enabled=False):
        app = api_main.create_app()
        client = TestClient(app)
        res = client.get("/api/reva/v1/health")
        assert res.status_code == 404


@pytest.mark.reva_obligation("OBL-REVA-IP-01")
@pytest.mark.reva_case("positive")
def test_mount_enabled():
    with override_settings(enabled=True):
        app = api_main.create_app()
        client = TestClient(app)
        res = client.get("/api/reva/v1/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "ok"
        assert data["version"] == "1.0.0"
