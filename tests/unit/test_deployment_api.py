import json
import os

from eoip.graph.memory import MemoryGraphStore
from eoip.jobs import write_json
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
    api.headers.update({"X-Correlation-ID": "request-123"})
    headers = {"Authorization": "Bearer test-token-with-at-least-24-characters"}
    response = api.post("/api/v1/admin/ingestion/jira", headers=headers, json={"document": {"issues": []}})
    assert response.status_code == 202
    assert response.headers["X-Correlation-ID"] == "request-123"
    assert response.headers["X-Audit-ID"]
    assert response.headers["X-Correlation-ID"] == "request-123"
    assert response.headers["X-Audit-ID"]
    job_id = response.json()["job_id"]
    result = api.get(f"/api/v1/admin/jobs/{job_id}", headers=headers).json()
    assert result["status"] == "PENDING"
    assert result["correlation_id"] == "request-123"
    assert result["correlation_id"] == "request-123"
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


def test_metrics_include_operation_counts_failures_and_latency(monkeypatch, tmp_path):
    api = client(monkeypatch, tmp_path)
    headers = {"Authorization": "Bearer test-token-with-at-least-24-characters"}

    assert api.get("/api/v1/search?q=demo", headers=headers).status_code == 200
    assert (
        api.post(
            "/api/v1/admin/ingestion/jira",
            headers=headers,
            json={"document": {"issues": []}},
        ).status_code
        == 202
    )
    assert (
        api.post(
            "/api/v1/rag",
            headers=headers,
            json={"canonical_id": "missing", "synthesize": True},
        ).status_code
        == 404
    )
    assert (
        api.post(
            "/api/v1/agents/trace-impact",
            headers=headers,
            json={"canonical_id": "missing"},
        ).status_code
        == 404
    )

    metrics = api.get("/metrics").text
    assert 'eoip_operations_total{operation="query",status="200"} 1.0' in metrics
    assert 'eoip_operations_total{operation="ingestion",status="202"} 1.0' in metrics
    assert 'eoip_operations_total{operation="model",status="404"} 1.0' in metrics
    assert 'eoip_operations_total{operation="agent",status="404"} 1.0' in metrics
    assert 'eoip_failures_total{operation="model",status="404"} 1.0' in metrics
    assert 'eoip_operation_duration_seconds_count{operation="query"} 1.0' in metrics


def test_metrics_include_ingestion_job_status_and_runtime(monkeypatch, tmp_path):
    api = client(monkeypatch, tmp_path)
    response = api.post(
        "/api/v1/admin/ingestion/jira",
        headers={"Authorization": f"Bearer {os.environ['EOIP_API_TOKEN']}"},
        json={"document": {"issues": []}},
    )
    job_id = response.json()["job_id"]

    pending_metrics = api.get("/metrics").text
    assert (
        'eoip_ingestion_job_status_transitions_total{kind="JIRA_JSON",status="PENDING"} 1.0'
        in pending_metrics
    )

    job_path = tmp_path / "jobs" / f"{job_id}.json"
    job = json.loads(job_path.read_text(encoding="utf-8"))
    job.update(
        status="SUCCEEDED",
        started_at="2026-01-01T00:00:00Z",
        finished_at="2026-01-01T00:00:02Z",
    )
    write_json(job_path, job)

    completed_metrics = api.get("/metrics").text
    assert (
        'eoip_ingestion_job_status_transitions_total{kind="JIRA_JSON",status="SUCCEEDED"} 1.0'
        in completed_metrics
    )
    assert 'eoip_ingestion_job_duration_seconds_count{kind="JIRA_JSON"} 1.0' in completed_metrics
    repeated_metrics = api.get("/metrics").text
    assert 'eoip_ingestion_job_duration_seconds_count{kind="JIRA_JSON"} 1.0' in repeated_metrics


def test_pending_ingestion_job_can_be_cancelled(monkeypatch, tmp_path):
    api = client(monkeypatch, tmp_path)
    headers = {"Authorization": "Bearer test-token-with-at-least-24-characters"}
    submitted = api.post(
        "/api/v1/admin/ingestion/jira",
        headers=headers,
        json={"document": {"issues": []}},
    ).json()

    cancelled = api.post(f"/api/v1/admin/jobs/{submitted['job_id']}/cancel", headers=headers)

    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "CANCELLED"
    assert "payload" not in cancelled.json()
    persisted = json.loads((tmp_path / "jobs" / f"{submitted['job_id']}.json").read_text())
    assert persisted["status"] == "CANCELLED"
    assert persisted["finished_at"].endswith("Z")


def test_running_ingestion_job_cannot_be_cancelled(monkeypatch, tmp_path):
    api = client(monkeypatch, tmp_path)
    headers = {"Authorization": "Bearer test-token-with-at-least-24-characters"}
    submitted = api.post(
        "/api/v1/admin/ingestion/jira",
        headers=headers,
        json={"document": {"issues": []}},
    ).json()
    job_path = tmp_path / "jobs" / f"{submitted['job_id']}.json"
    job = json.loads(job_path.read_text())
    job["status"] = "RUNNING"
    write_json(job_path, job)

    response = api.post(f"/api/v1/admin/jobs/{submitted['job_id']}/cancel", headers=headers)

    assert response.status_code == 409
    assert response.json()["detail"] == "Running jobs cannot be cancelled safely"
