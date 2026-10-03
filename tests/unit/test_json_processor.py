"""Tests for JsonProcessor: entity inference, relationship extraction, batch processing."""

from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.json_processor import (
    JsonProcessor,
    ProcessingResult,
    _generate_canonical_id,
    _infer_entity_type,
)


def test_infer_entity_type_from_entity_type_field():
    assert _infer_entity_type({"entity_type": "Commit"}) == "Commit"


def test_infer_entity_type_from_type_field_mapped():
    assert _infer_entity_type({"type": "issue"}) == "Issue"
    assert _infer_entity_type({"type": "bug"}) == "Issue"
    assert _infer_entity_type({"type": "commit"}) == "Commit"
    assert _infer_entity_type({"type": "pipeline"}) == "Pipeline"
    assert _infer_entity_type({"type": "document"}) == "Document"
    assert _infer_entity_type({"type": "person"}) == "Person"


def test_infer_entity_type_falls_back_to_generic():
    assert _infer_entity_type({"type": "unknown_thing"}) == "GenericEntity"
    assert _infer_entity_type({}) == "GenericEntity"


def test_generate_canonical_id_uses_name():
    cid = _generate_canonical_id("WorkItem", {"name": "EOIP-1"})
    assert cid == "WorkItem:EOIP-1"


def test_generate_canonical_id_uses_hash_fallback():
    cid = _generate_canonical_id("WorkItem", {"description": "no name field"})
    assert cid.startswith("WorkItem:")
    assert len(cid) > len("WorkItem:")


def test_process_single_entity():
    store = MemoryGraphStore()
    processor = JsonProcessor(store)
    result = processor.process_json_data(
        {"entity_type": "Commit", "canonical_id": "commit:test1", "commit_sha": "abc"},
        source_label="test",
    )
    assert result.entities_created == 1
    assert result.files_processed == 1
    assert len(result.errors) == 0
    v = store.get_vertex_by_canonical_id("commit:test1")
    assert v is not None
    assert v["label"] == "Commit"


def test_process_array_of_entities():
    store = MemoryGraphStore()
    processor = JsonProcessor(store)
    data = [
        {"entity_type": "Commit", "canonical_id": "commit:a1", "commit_sha": "sha1"},
        {"entity_type": "Commit", "canonical_id": "commit:a2", "commit_sha": "sha2"},
    ]
    result = processor.process_json_data(data, source_label="batch")
    assert result.entities_created == 2


def test_process_nested_entities_and_relationships():
    store = MemoryGraphStore()
    processor = JsonProcessor(store)
    data = {
        "entities": [
            {"entity_type": "WorkItem", "canonical_id": "issue:n1", "issue_key": "N-1", "summary": "Test"},
            {"entity_type": "Commit", "canonical_id": "commit:n1", "commit_sha": "sha1"},
        ],
        "relationships": [
            {"from_id": "commit:n1", "to_id": "issue:n1", "type": "IMPLEMENTS"},
        ],
    }
    result = processor.process_json_data(data, source_label="nested")
    assert result.entities_created == 2
    assert result.relationships_created == 1
    edges = store.find_edges(label="IMPLEMENTS")
    assert len(edges) == 1


def test_process_entity_with_inline_relationships():
    store = MemoryGraphStore()
    processor = JsonProcessor(store)
    store.upsert_vertex("WorkItem", {"canonical_id": "issue:target", "issue_key": "T-1", "summary": "Target"})
    data = {
        "entity_type": "Commit",
        "canonical_id": "commit:rel1",
        "commit_sha": "sha1",
        "relationships": [
            {"to_id": "issue:target", "type": "IMPLEMENTS"},
        ],
    }
    result = processor.process_json_data(data, source_label="inline")
    assert result.entities_created == 1
    assert result.relationships_created == 1


def test_process_entity_with_depends_on():
    store = MemoryGraphStore()
    processor = JsonProcessor(store)
    store.upsert_vertex("File", {"canonical_id": "file:dep1", "repo_id": "r1", "path": "a.py"})
    data = {
        "entity_type": "File",
        "canonical_id": "file:dep2",
        "repo_id": "r1",
        "path": "b.py",
        "depends_on": ["file:dep1"],
    }
    result = processor.process_json_data(data, source_label="deps")
    assert result.entities_created == 1
    assert result.relationships_created == 1
    edges = store.find_edges(label="DEPENDS_ON")
    assert len(edges) == 1


def test_process_entity_with_parent():
    store = MemoryGraphStore()
    processor = JsonProcessor(store)
    store.upsert_vertex("Epic", {"canonical_id": "epic:parent1", "name": "Parent Epic"})
    data = {
        "entity_type": "Feature",
        "canonical_id": "feature:child1",
        "name": "Child Feature",
        "parent": "epic:parent1",
    }
    result = processor.process_json_data(data, source_label="parent")
    assert result.relationships_created == 1
    edges = store.find_edges(label="CHILD_OF")
    assert len(edges) == 1


def test_unknown_entity_type_falls_back_to_generic():
    store = MemoryGraphStore()
    processor = JsonProcessor(store)
    data = {"name": "widget", "color": "blue"}
    result = processor.process_json_data(data, source_label="generic")
    assert result.entities_created == 1
    v = store.get_vertex_by_canonical_id("GenericEntity:widget")
    assert v is not None
    assert v["label"] == "GenericEntity"


def test_metadata_vertex_created():
    store = MemoryGraphStore()
    processor = JsonProcessor(store)
    result = processor.process_json_data(
        {"entity_type": "Commit", "canonical_id": "commit:meta1", "commit_sha": "m1"},
        source_label="meta-test",
        pipeline_id="pipe-1",
    )
    assert result.metadata_vertices == 1
    runs = store.find_vertices(label="IngestionRun")
    assert len(runs) >= 1
    props = runs[-1]["properties"]
    assert props["run_kind"] == "json_ingestion"
    assert props["pipeline_id"] == "pipe-1"


def test_no_metadata_vertex_when_zero_entities():
    store = MemoryGraphStore()
    processor = JsonProcessor(store)
    result = processor.process_json_data("not a dict or list", source_label="bad")
    assert result.metadata_vertices == 0
    assert len(result.errors) > 0


def test_relationship_missing_endpoint_logs_error():
    store = MemoryGraphStore()
    processor = JsonProcessor(store)
    data = {
        "entities": [
            {"entity_type": "Commit", "canonical_id": "commit:orphan", "commit_sha": "o1"},
        ],
        "relationships": [
            {"from_id": "commit:orphan", "to_id": "nonexistent:target", "type": "LINKS"},
        ],
    }
    result = processor.process_json_data(data, source_label="orphan")
    assert result.entities_created == 1
    assert result.relationships_created == 0
    assert any("not found" in str(e.get("error", "")).lower() for e in result.errors)


def test_processing_result_to_dict():
    r = ProcessingResult()
    r.entities_created = 5
    r.relationships_created = 3
    r.files_processed = 1
    r.metadata_vertices = 1
    d = r.to_dict()
    assert d["entities_created"] == 5
    assert d["relationships_created"] == 3
    assert d["error_count"] == 0


def test_process_json_file(tmp_path):
    import json
    store = MemoryGraphStore()
    processor = JsonProcessor(store)
    file_path = tmp_path / "test.json"
    file_path.write_text(json.dumps([
        {"entity_type": "Commit", "canonical_id": "commit:file1", "commit_sha": "f1"},
        {"entity_type": "Commit", "canonical_id": "commit:file2", "commit_sha": "f2"},
    ]))
    result = processor.process_json_file(str(file_path), pipeline_id="file-pipe")
    assert result.entities_created == 2
    assert result.files_processed == 1


def test_process_json_directory(tmp_path):
    import json
    store = MemoryGraphStore()
    processor = JsonProcessor(store)
    (tmp_path / "a.json").write_text(json.dumps(
        {"entity_type": "Commit", "canonical_id": "commit:d1", "commit_sha": "d1"}
    ))
    (tmp_path / "b.json").write_text(json.dumps(
        {"entity_type": "Commit", "canonical_id": "commit:d2", "commit_sha": "d2"}
    ))
    (tmp_path / "skip.txt").write_text("not json")
    result = processor.process_json_directory(str(tmp_path), pipeline_id="dir-pipe")
    assert result.files_processed == 2
    assert result.entities_created == 2


def test_type_mapping_case_insensitive():
    assert _infer_entity_type({"type": "ISSUE"}) == "Issue"
    assert _infer_entity_type({"type": "Bug"}) == "Issue"
    assert _infer_entity_type({"type": "COMMIT"}) == "Commit"
