from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

from apps.api import main


def client(monkeypatch, tmp_path):
    store = MemoryGraphStore()
    store.close = lambda: None
    monkeypatch.setenv("EOIP_API_TOKEN", "test-token-with-at-least-24-characters")
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    monkeypatch.setattr(main, "create_store", lambda: store)
    return TestClient(main.create_app())


def test_admin_and_read_routes_require_token_and_jobs_are_durable(monkeypatch, tmp_path):
    api = client(monkeypatch, tmp_path)
    assert api.get("/health/live").status_code == 200
    assert api.get("/api/v1/admin/jobs").status_code == 401
    headers = {"Authorization": "Bearer test-token-with-at-least-24-characters"}
    response = api.post("/api/v1/admin/ingestion/jira", headers=headers, json={"document": {"issues": []}})
    assert response.status_code == 202
    job_id = response.json()["job_id"]
    result = api.get(f"/api/v1/admin/jobs/{job_id}", headers=headers).json()
    assert result["status"] == "PENDING"
    assert "payload" not in result
    assert (tmp_path / "jobs" / f"{job_id}.json").exists()
    assert api.get("/api/v1/admin/jobs/not-a-uuid", headers=headers).status_code == 404
    assert "HTTPBearer" in api.get("/openapi.json").json()["components"]["securitySchemes"]


def test_body_limit_applies_before_json_parsing(monkeypatch, tmp_path):
    api = client(monkeypatch, tmp_path)
    response = api.post(
        "/api/v1/admin/ingestion/jira",
        headers={"Authorization": "Bearer test-token-with-at-least-24-characters"},
        content=b"x" * 4_000_001,
    )
    assert response.status_code == 413
    assert not list((tmp_path / "jobs").glob("*.json"))
