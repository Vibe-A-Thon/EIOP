"""Integration tests for dormant and active REVA mounting (T-004 / OBL-REVA-IP-01)."""

from _principals import provision_api_token
import pytest
from fastapi.testclient import TestClient
from eoip.graph.memory import MemoryGraphStore
import apps.api.main as api_main
from tests.reva.support.settings import override_settings

pytestmark = pytest.mark.reva_depth("integration")


@pytest.fixture(autouse=True)
def setup_api_env(monkeypatch, tmp_path):
    provision_api_token(monkeypatch, "x" * 32)
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


@pytest.mark.reva_obligation("OBL-REVA-IP-01")
@pytest.mark.reva_case("negative")
def test_mounted_router_maps_reva_errors_to_http_status(tmp_path):
    """A REVA domain error (here: unknown warrant) is a 404 problem, not an unhandled 500."""
    from reva.api import set_api_kernel
    from reva.kernel.kernel import WarrantKernel
    from reva.kernel.store import RevaStore

    set_api_kernel(WarrantKernel(store=RevaStore(str(tmp_path / "reva.db"))))
    with override_settings(enabled=True):
        client = TestClient(api_main.create_app(), raise_server_exceptions=False)
        res = client.get("/api/reva/v1/warrants/wr1_" + "0" * 64, headers={"Authorization": "Bearer " + "x" * 32})
        assert res.status_code == 404, res.text
