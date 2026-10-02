"""Tests for new API endpoints: neighborhood, traceability, DLQ, GitLab ingestion."""

import json
from pathlib import Path

import pytest
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient


def _make_api_app(store, tmp_path):
    import os
    os.environ.setdefault("EOIP_API_TOKEN", "test-token-minimum-24-characters!!")
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
