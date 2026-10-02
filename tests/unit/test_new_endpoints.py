"""Tests for new API endpoints: neighborhood, traceability, DLQ, GitLab ingestion."""

import json

from eoip.connectors.jira_json import JiraJsonConnector
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService
from fastapi.testclient import TestClient


def _make_api_app(store, tmp_path):
    import os
    os.environ["EOIP_API_TOKEN"] = "test-token-minimum-24-characters!!"
    os.environ["EOIP_DATA_DIR"] = str(tmp_path)

    from apps.api import main as api_main
    api_main.create_store = lambda: store
    return api_main.create_app()


def test_dlq_endpoint_returns_empty_list(tmp_path):
    store = MemoryGraphStore()
    app = _make_api_app(store, tmp_path)
    client = TestClient(app)
    r = client.get("/api/v1/admin/dlq", headers={"Authorization": "Bearer test-token-minimum-24-characters!!"})
    assert r.status_code == 200
    assert r.json() == []


def test_dlq_endpoint_returns_records(tmp_path):
    store = MemoryGraphStore()
    dlq_dir = tmp_path / "dlq"
    dlq_dir.mkdir(parents=True)
    record = {"event_id": "abc123", "error": "mapping failed", "stage": "canonicalize", "source_system": "jira"}
    (dlq_dir / "abc123.json").write_text(json.dumps(record), encoding="utf-8")

    app = _make_api_app(store, tmp_path)
    client = TestClient(app)
    r = client.get("/api/v1/admin/dlq", headers={"Authorization": "Bearer test-token-minimum-24-characters!!"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["event_id"] == "abc123"


def test_dlq_replay_queues_the_captured_source_event(tmp_path):
    store = MemoryGraphStore()
    service = JiraIngestionService(
        store,
        JiraJsonConnector(),
        FileEventCapture(tmp_path / "raw"),
        tmp_path / "dlq",
    )
    result = service.ingest({"issues": [{"fields": {"summary": "Missing key"}}]})
    event_id = result["rejected"][0]["event_id"]
    app = _make_api_app(store, tmp_path)
    client = TestClient(app)

    response = client.post(
        f"/api/v1/admin/dlq/{event_id}/replay",
        headers={"Authorization": "Bearer test-token-minimum-24-characters!!"},
    )

    assert response.status_code == 202
    job = json.loads((tmp_path / "jobs" / f"{response.json()['job_id']}.json").read_text())
    assert job["kind"] == "JIRA_JSON"
    assert job["payload"]["document"] == [{"fields": {"summary": "Missing key"}}]


def test_dlq_replay_rejects_invalid_or_missing_event_ids(tmp_path):
    app = _make_api_app(MemoryGraphStore(), tmp_path)
    client = TestClient(app)
    headers = {"Authorization": "Bearer test-token-minimum-24-characters!!"}

    assert client.post("/api/v1/admin/dlq/../escape/replay", headers=headers).status_code == 404
    assert client.post(f"/api/v1/admin/dlq/{'0' * 64}/replay", headers=headers).status_code == 404


def test_gitlab_ingestion_endpoint_accepts_request(tmp_path):
    store = MemoryGraphStore()
    app = _make_api_app(store, tmp_path)
    client = TestClient(app)
    r = client.post(
        "/api/v1/admin/ingestion/gitlab",
        json={"document": {"merge_requests": []}},
        headers={"Authorization": "Bearer test-token-minimum-24-characters!!"},
    )
    assert r.status_code == 202
    assert "job_id" in r.json()
    job = json.loads((tmp_path / "jobs" / f"{r.json()['job_id']}.json").read_text(encoding="utf-8"))
    assert job["payload"]["repository_id"] == "demo"


def test_gitlab_ingestion_endpoint_rejects_unsafe_repository_id(tmp_path):
    store = MemoryGraphStore()
    app = _make_api_app(store, tmp_path)
    client = TestClient(app)
    response = client.post(
        "/api/v1/admin/ingestion/gitlab",
        json={"document": {"merge_requests": []}, "repository_id": "../ escape?"},
        headers={"Authorization": "Bearer test-token-minimum-24-characters!!"},
    )
    assert response.status_code == 422


def test_ontology_export_returns_jsonld(tmp_path):
    store = MemoryGraphStore()
    store.upsert_vertex("WorkItem", {"canonical_id": "w1", "issue_key": "X-1", "summary": "Test"})
    app = _make_api_app(store, tmp_path)
    client = TestClient(app)
    r = client.get(
        "/api/v1/ontology/export?limit=10",
        headers={"Authorization": "Bearer test-token-minimum-24-characters!!"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "@context" in data
    assert "@graph" in data


def test_admin_system_status_reports_real_local_state(tmp_path, monkeypatch):
    monkeypatch.delenv("EOIP_OLLAMA_MODEL", raising=False)
    store = MemoryGraphStore()
    app = _make_api_app(store, tmp_path)
    client = TestClient(app)
    response = client.get(
        "/api/v1/admin/system",
        headers={"Authorization": "Bearer test-token-minimum-24-characters!!"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "graph": {"status": "ready"},
        "model": {"status": "disabled", "configured": False, "name": None},
        "backup": {"status": "not_created", "count": 0, "latest": None},
        "connectors": {"checkpoint_count": 0},
    }
