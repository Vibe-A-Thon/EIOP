"""Code exports must ingest connected, typed facts rather than a generic wrapper."""

import json
from pathlib import Path

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.json_processor import JsonProcessor
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("mode", ["manual", "pipelines"])
def test_real_code_export_ingests_every_source_edge_and_replays(mode):
    data = json.loads((ROOT / "demo" / "demodata" / mode / "code-graph.json").read_text())
    store = MemoryGraphStore()
    processor = JsonProcessor(store)
    result = processor.process_json_data(data, source_label=mode)
    assert result.errors == []
    assert len(store.find_vertices(label="File")) == len(data["files"])
    assert len(store.find_vertices(label="CodeSymbol")) == len(data["symbols"])
    source_edges = [
        edge for edge in store.find_edges()
        if "payload_json" in edge["properties"]
    ]
    assert len(source_edges) == len(data["edges"])
    assert sorted(edge["properties"]["payload_json"] for edge in source_edges) == sorted(
        json.dumps(edge, sort_keys=True) for edge in data["edges"]
    )
    vertex_ids = {
        v["vid"] for v in store.find_vertices() if v["label"] != "IngestionRun"
    }
    edge_ids = {e["eid"] for e in store.find_edges()}
    replay = processor.process_json_data(data, source_label=mode)
    assert replay.errors == []
    assert vertex_ids == {
        v["vid"] for v in store.find_vertices() if v["label"] != "IngestionRun"
    }
    assert edge_ids == {e["eid"] for e in store.find_edges()}


def test_code_export_does_not_fabricate_missing_endpoint():
    store = MemoryGraphStore()
    result = JsonProcessor(store).process_json_data({
        "repository": "test-repo",
        "files": [],
        "symbols": [],
        "edges": [{"source": "test-repo", "target": "undeclared-host", "edge_type": "CONNECTS_TO"}],
    })
    assert result.errors
    assert result.relationships_created == 0
    assert store.get_vertex_by_canonical_id("undeclared-host") is None


def test_inline_forward_reference_is_resolved_after_all_entities():
    store = MemoryGraphStore()
    result = JsonProcessor(store).process_json_data([
        {
            "entity_type": "CodeSymbol", "canonical_id": "symbol:first",
            "qualified_name": "first", "symbol_kind": "function",
            "relationships": [{"to_id": "symbol:second", "type": "CALLS"}],
        },
        {
            "entity_type": "CodeSymbol", "canonical_id": "symbol:second",
            "qualified_name": "second", "symbol_kind": "function",
        },
    ])
    assert result.errors == []
    assert result.relationships_created == 1


@pytest.mark.parametrize("updates", [
    {"repository": {"repo_id": []}},
    {"files": [{"path": []}]},
    {"symbols": [{"qualified_name": [], "kind": "class", "path": []}]},
    {"dependencies": [{"name": []}]},
    {"runtime_dependencies": [{"id": [], "name": "invalid"}]},
    {"edges": [{"source": [], "target": "test-repo", "kind": "uses"}]},
    {"edges": [{"source": "test-repo", "target": "test-repo", "kind": "unknown"}]},
])
def test_malformed_export_returns_explicit_error_without_writes(updates):
    store = MemoryGraphStore()
    result = JsonProcessor(store).process_json_data({
        "repository": "test-repo", "files": [], "symbols": [], **updates,
    })
    assert result.errors
    assert result.entities_created == result.relationships_created == 0
    assert store.find_vertices() == []


def test_code_symbol_identity_is_namespaced_by_repository():
    store = MemoryGraphStore()
    processor = JsonProcessor(store)
    for repo in ("repo-a", "repo-b"):
        result = processor.process_json_data({
            "repository": repo,
            "files": [{"path": "main.py"}],
            "symbols": [{"qualified_name": "main.run", "kind": "function", "path": "main.py"}],
        })
        assert result.errors == []
    assert len(store.find_vertices(label="CodeSymbol")) == 2


@pytest.mark.parametrize("mode", ["manual", "pipelines"])
def test_authenticated_code_export_api_persists_and_replays(mode, tmp_path, monkeypatch):
    from apps.api import main

    token = "code-export-test-token-at-least-24-characters"
    monkeypatch.setenv("EOIP_API_TOKEN", token)
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    store = MemoryGraphStore()
    # The API lifespan closes real backends; this in-memory fixture owns no resources.
    monkeypatch.setattr(store, "close", lambda: None, raising=False)
    monkeypatch.setattr(main, "create_store", lambda: store)
    data = json.loads((ROOT / "demo" / "demodata" / mode / "code-graph.json").read_text())
    with TestClient(main.create_app()) as client:
        body = {"data": data, "source_label": mode, "pipeline_id": "code-api-test"}
        rejected = client.post("/api/v1/admin/ingestion/json", json=body)
        assert rejected.status_code in (401, 403)
        assert store.find_vertices(label="CodeSymbol") == []
        headers = {"Authorization": f"Bearer {token}"}
        imported = client.post("/api/v1/admin/ingestion/json", headers=headers, json=body)
        assert imported.status_code == 200
        assert imported.json()["error_count"] == 0
        assert len(store.find_vertices(label="CodeSymbol")) == len(data["symbols"])
        edge_ids = {e["eid"] for e in store.find_edges()}
        replay = client.post("/api/v1/admin/ingestion/json", headers=headers, json=body)
        assert replay.status_code == 200
        assert replay.json()["error_count"] == 0
        assert edge_ids == {e["eid"] for e in store.find_edges()}
