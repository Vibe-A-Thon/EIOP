"""Brain learning save/load cannot write or read arbitrary paths (security fix, chunk 7)."""
from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from eoip.brain import router as brain

pytestmark = pytest.mark.req("SR-CON-011", "CRA-003")


@pytest.fixture
def api(tmp_path, monkeypatch):
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path / "data"))
    app = FastAPI()
    app.include_router(brain.build_brain_router(), prefix="/api/v1")
    return TestClient(app), tmp_path


def test_state_is_written_only_under_the_data_dir_and_round_trips(api):
    client, tmp = api
    r = client.post("/api/v1/brain/learning/save", params={"slot": "nightly"})
    assert r.status_code == 200 and r.json() == {"status": "SAVED", "slot": "nightly"}
    assert (tmp / "data" / "learning" / "nightly" / "q_learning.json").exists()
    assert client.post("/api/v1/brain/learning/load", params={"slot": "nightly"}).json()["status"] == "LOADED"
    assert client.post("/api/v1/brain/learning/load", params={"slot": "never"}).json()["status"] == "NOT_FOUND"


@pytest.mark.parametrize("params", [
    {"directory": "/etc/eoip"}, {"directory": "data/learning"}, {"slot": "../../etc"}, {"slot": "a/b"},
    {"slot": ".."}, {"slot": ""}, {"slot": "x" * 65},
])
@pytest.mark.parametrize("verb", ["save", "load"])
def test_paths_and_traversal_rejected(api, params, verb):
    client, tmp = api
    r = client.post(f"/api/v1/brain/learning/{verb}", params=params)
    assert r.status_code == 400
    assert not (tmp / "etc").exists()


def test_routes_are_admin_only_in_the_route_policy():
    from apps.api import route_policy

    for verb in ("save", "load"):
        assert route_policy.classify("POST", f"/api/v1/brain/learning/{verb}") == "admin"
