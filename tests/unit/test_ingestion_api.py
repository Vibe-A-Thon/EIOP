"""Tests for JSON ingestion, format conversion, and graph health API endpoints."""

from _principals import provision_api_token
import os

from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

TOKEN = "test-token-minimum-24-characters!!"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def _make_app(store, tmp_path):
    os.environ["EOIP_API_TOKEN"] = TOKEN
    provision_api_token(None, TOKEN)
    os.environ["EOIP_DATA_DIR"] = str(tmp_path)
    from apps.api import main as api_main
    api_main.create_store = lambda: store
    return api_main.create_app()


# --- JSON Ingestion ---

def test_ingest_single_entity(tmp_path):
    store = MemoryGraphStore()
    client = TestClient(_make_app(store, tmp_path))
    r = client.post("/api/v1/admin/ingestion/json", headers=HEADERS, json={
        "data": {"entity_type": "Commit", "canonical_id": "commit:api1", "commit_sha": "abc"},
        "source_label": "api-test",
        "pipeline_id": "test-pipe",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["entities_created"] == 1
    assert body["error_count"] == 0
    assert store.get_vertex_by_canonical_id("commit:api1") is not None


def test_ingest_array_of_entities(tmp_path):
    store = MemoryGraphStore()
    client = TestClient(_make_app(store, tmp_path))
    r = client.post("/api/v1/admin/ingestion/json", headers=HEADERS, json={
        "data": [
            {"entity_type": "Commit", "canonical_id": "commit:b1", "commit_sha": "s1"},
            {"entity_type": "Commit", "canonical_id": "commit:b2", "commit_sha": "s2"},
        ],
    })
    assert r.status_code == 200
    assert r.json()["entities_created"] == 2


def test_ingest_batch(tmp_path):
    store = MemoryGraphStore()
    client = TestClient(_make_app(store, tmp_path))
    r = client.post("/api/v1/admin/ingestion/json/batch", headers=HEADERS, json={
        "files": [
            {"name": "file1.json", "data": {"entity_type": "Commit", "canonical_id": "commit:batch1", "commit_sha": "x1"}},
            {"name": "file2.json", "data": {"entity_type": "Commit", "canonical_id": "commit:batch2", "commit_sha": "x2"}},
        ],
        "pipeline_id": "batch-test",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["files_processed"] == 2
    assert body["entities_created"] == 2


def test_ingest_batch_missing_data_field(tmp_path):
    store = MemoryGraphStore()
    client = TestClient(_make_app(store, tmp_path))
    r = client.post("/api/v1/admin/ingestion/json/batch", headers=HEADERS, json={
        "files": [{"name": "bad.json"}],
    })
    assert r.status_code == 200
    body = r.json()
    assert body["error_count"] >= 1


# --- Format Conversion ---

def test_available_formats(tmp_path):
    store = MemoryGraphStore()
    client = TestClient(_make_app(store, tmp_path))
    r = client.get("/api/v1/graph/formats", headers=HEADERS)
    assert r.status_code == 200
    formats = r.json()["formats"]
    assert len(formats) == 11
    ids = [f["id"] for f in formats]
    assert "rdf" in ids
    assert "cypher" in ids
    assert "sparql" in ids
    assert "shacl" in ids
    assert "pgql" in ids


def test_convert_rdf(tmp_path):
    store = MemoryGraphStore()
    store.upsert_vertex("WorkItem", {
        "canonical_id": "issue:conv1", "issue_key": "C-1", "summary": "Convert test",
    })
    client = TestClient(_make_app(store, tmp_path))
    r = client.post("/api/v1/graph/convert", headers=HEADERS, json={
        "format_id": "rdf",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["format"] == "rdf"
    assert body["extension"] == ".ttl"
    assert "WorkItem" in body["content"]
    assert body["content_length"] > 0


def test_convert_cypher(tmp_path):
    store = MemoryGraphStore()
    store.upsert_vertex("Commit", {"canonical_id": "commit:cy1", "commit_sha": "cy1"})
    client = TestClient(_make_app(store, tmp_path))
    r = client.post("/api/v1/graph/convert", headers=HEADERS, json={"format_id": "cypher"})
    assert r.status_code == 200
    assert "MERGE" in r.json()["content"]


def test_process_and_convert(tmp_path):
    store = MemoryGraphStore()
    client = TestClient(_make_app(store, tmp_path))
    r = client.post("/api/v1/admin/ingestion/process-and-convert", headers=HEADERS, json={
        "data": {"entity_type": "Commit", "canonical_id": "commit:pac1", "commit_sha": "p1"},
        "source_label": "pac-test",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["ingestion"]["entities_created"] == 1
    assert "rdf" in body["formats"]
    assert "cypher" in body["formats"]
    assert "sparql" in body["formats"]
    for fmt_data in body["formats"].values():
        assert "label" in fmt_data
        if "error" not in fmt_data:
            assert len(fmt_data["content"]) > 0


# --- Orphaned & Stale Endpoints ---

def test_orphaned_entities_endpoint(tmp_path):
    store = MemoryGraphStore()
    store.upsert_vertex("Commit", {"canonical_id": "commit:orph1", "commit_sha": "o1"})
    store.upsert_vertex("WorkItem", {"canonical_id": "issue:orph1", "issue_key": "O-1", "summary": "Orphan"})
    client = TestClient(_make_app(store, tmp_path))
    r = client.get("/api/v1/graph/orphaned", headers=HEADERS)
    assert r.status_code == 200
    body = r.json()
    assert body["count"] >= 2
    cids = [o["canonical_id"] for o in body["orphaned"]]
    assert "commit:orph1" in cids


def test_orphaned_entities_with_type_filter(tmp_path):
    store = MemoryGraphStore()
    store.upsert_vertex("Commit", {"canonical_id": "commit:ft1", "commit_sha": "f1"})
    store.upsert_vertex("WorkItem", {"canonical_id": "issue:ft1", "issue_key": "F-1", "summary": "Filter"})
    client = TestClient(_make_app(store, tmp_path))
    r = client.get("/api/v1/graph/orphaned?entity_types=Commit", headers=HEADERS)
    assert r.status_code == 200
    cids = [o["canonical_id"] for o in r.json()["orphaned"]]
    assert "commit:ft1" in cids
    assert "issue:ft1" not in cids


def test_stale_entities_endpoint(tmp_path):
    store = MemoryGraphStore()
    store.upsert_vertex("Commit", {
        "canonical_id": "commit:stale1", "commit_sha": "s1",
        "modified_at": "2020-01-01T00:00:00Z",
    })
    client = TestClient(_make_app(store, tmp_path))
    r = client.get("/api/v1/graph/stale?threshold_hours=1", headers=HEADERS)
    assert r.status_code == 200
    body = r.json()
    assert body["count"] >= 1
    cids = [s["canonical_id"] for s in body["stale"]]
    assert "commit:stale1" in cids


# --- Files Endpoint ---

def test_files_endpoint_returns_404_for_missing(tmp_path):
    store = MemoryGraphStore()
    client = TestClient(_make_app(store, tmp_path))
    r = client.get("/api/v1/files/nonexistent.txt", headers=HEADERS)
    assert r.status_code == 404
