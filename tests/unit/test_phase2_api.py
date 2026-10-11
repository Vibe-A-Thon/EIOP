import pytest
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

import apps.api.main as api_main


@pytest.mark.req("G2-SYNC-009")
def test_source_sync_admin_routes_enqueue_only_safe_sync_options(monkeypatch, tmp_path):
    monkeypatch.setattr(api_main, "api_token", lambda: "x" * 32)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)
    client = TestClient(api_main.create_app())
    headers = {"Authorization": "Bearer " + "x" * 32}
    request = {
        "checkpoint": "2026-10-01T00:00:00Z",
        "watermark": "2026-10-02T12:00:00Z",
        "dry_run": True,
    }

    confluence = client.post(
        "/api/v1/admin/ingestion/confluence", json=request, headers=headers
    )
    servicenow = client.post(
        "/api/v1/admin/ingestion/servicenow", json=request, headers=headers
    )
    denied = client.post("/api/v1/admin/ingestion/confluence", json=request)

    assert confluence.status_code == servicenow.status_code == 202
    assert denied.status_code == 401
    confluence_job = api_main.JobQueue(tmp_path).get(confluence.json()["job_id"])
    servicenow_job = api_main.JobQueue(tmp_path).get(servicenow.json()["job_id"])
    assert confluence_job["kind"] == "CONFLUENCE"
    assert servicenow_job["kind"] == "SERVICENOW"
    assert confluence_job["payload"] == request
    assert "token" not in confluence_job["payload"]


def test_ontology_export_requires_auth_and_returns_jsonld(monkeypatch, tmp_path):
    monkeypatch.setattr(api_main, "api_token", lambda: "x" * 32)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)
    client = TestClient(api_main.create_app())
    headers = {"Authorization": "Bearer " + "x" * 32}

    denied = client.get("/api/v1/ontology/export")
    response = client.get("/api/v1/ontology/export?limit=10", headers=headers)
    invalid_limit = client.get("/api/v1/ontology/export?limit=10001", headers=headers)

    assert denied.status_code == 401
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/ld+json")
    assert response.json()["export"]["format"] == "JSON-LD 1.1"
    assert invalid_limit.status_code == 422
