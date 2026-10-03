"""Tests for the validation engine and quality metrics."""

from eoip.graph.memory import MemoryGraphStore
from eoip.validation.engine import ValidationEngine
from eoip.validation.quality import QualityMetrics


def _seeded_store():
    store = MemoryGraphStore()
    project = store.upsert_vertex("Project", {"canonical_id": "urn:test:project:1", "name": "Test Project"})
    work_item = store.upsert_vertex("WorkItem", {
        "canonical_id": "urn:test:item:1", "issue_key": "TEST-1", "summary": "Test item",
        "ingestion_run_id": "run-1",
    })
    store.upsert_edge("CONTAINS", project["vid"], work_item["vid"], {
        "fact_key": "test-contains", "creation_status": "DETERMINISTIC",
    })
    return store


def test_valid_graph_passes_validation():
    store = _seeded_store()
    engine = ValidationEngine(store)
    result = engine.run()
    errors = [f for f in result["findings"] if f["severity"] == "ERROR"]
    assert not errors
    assert result["vertices_checked"] >= 2


def test_missing_required_property_detected():
    store = MemoryGraphStore()
    store.upsert_vertex("WorkItem", {"canonical_id": "urn:test:item:bad", "issue_key": "TEST-BAD"})
    engine = ValidationEngine(store)
    result = engine.run()
    errors = [f for f in result["findings"] if f["severity"] == "ERROR" and f["rule"] == "required_properties"]
    assert errors
    assert "summary" in errors[0]["missing"]


def test_orphan_vertex_detected():
    store = MemoryGraphStore()
    store.upsert_vertex("WorkItem", {
        "canonical_id": "urn:test:orphan:1", "issue_key": "ORPH-1", "summary": "Orphan",
        "ingestion_run_id": "run-1",
    })
    engine = ValidationEngine(store)
    result = engine.run()
    orphans = [f for f in result["findings"] if f["rule"] == "orphan_vertex"]
    assert orphans


def test_tombstoned_vertex_with_active_edge_reports_deletion_conflict():
    store = _seeded_store()
    assert store.tombstone_vertex("urn:test:item:1")

    result = ValidationEngine(store).run()

    conflicts = [f for f in result["findings"] if f["rule"] == "deletion_conflict"]
    assert conflicts == [
        {
            "canonical_id": "urn:test:item:1",
            "rule": "deletion_conflict",
            "severity": "WARNING",
            "detail": "Tombstoned entity is still referenced by an active relationship",
        }
    ]
    assert result["valid"] is True
    assert result["vertices_checked"] == 2


def test_ambiguous_vertex_creates_warning():
    store = MemoryGraphStore()
    project = store.upsert_vertex("Project", {"canonical_id": "urn:test:project:1", "name": "Test Project"})
    store.upsert_vertex("WorkItem", {
        "canonical_id": "urn:test:amb:1", "issue_key": "AMB-1", "summary": "Ambiguous item",
        "ingestion_run_id": "run-1", "creation_status": "AMBIGUOUS",
    })
    result = ValidationEngine(store).run()
    warnings = [f for f in result["findings"] if f["rule"] == "ambiguous_needs_review" and "canonical_id" in f]
    assert warnings
    assert "AMBIGUOUS" in warnings[0]["detail"]
    assert warnings[0]["severity"] == "WARNING"
    assert result["valid"] is True


def test_ambiguous_edge_creates_warning():
    store = _seeded_store()
    project = store.get_vertex_by_canonical_id("urn:test:project:1")
    item = store.get_vertex_by_canonical_id("urn:test:item:1")
    store.upsert_edge("CONTAINS", project["vid"], item["vid"], {
        "fact_key": "amb-edge", "creation_status": "AMBIGUOUS",
    })
    result = ValidationEngine(store).run()
    warnings = [f for f in result["findings"] if f["rule"] == "ambiguous_needs_review" and "edge_id" in f]
    assert warnings
    assert "AMBIGUOUS" in warnings[0]["detail"]
    assert warnings[0]["severity"] == "WARNING"


def test_invalid_creation_status_on_edge_is_error():
    store = _seeded_store()
    project = store.get_vertex_by_canonical_id("urn:test:project:1")
    item = store.get_vertex_by_canonical_id("urn:test:item:1")
    store.upsert_edge("CONTAINS", project["vid"], item["vid"], {
        "fact_key": "bad-status", "creation_status": "BOGUS_STATUS",
    })
    result = ValidationEngine(store).run()
    errors = [f for f in result["findings"] if f["rule"] == "invalid_creation_status"]
    assert errors
    assert "BOGUS_STATUS" in errors[0]["detail"]
    assert errors[0]["severity"] == "ERROR"
    assert result["valid"] is False


def test_missing_creation_status_on_edge_is_warning():
    store = MemoryGraphStore()
    project = store.upsert_vertex("Project", {"canonical_id": "urn:test:project:1", "name": "Test Project"})
    item = store.upsert_vertex("WorkItem", {
        "canonical_id": "urn:test:item:1", "issue_key": "TEST-1", "summary": "Test item",
        "ingestion_run_id": "run-1",
    })
    store.upsert_edge("CONTAINS", project["vid"], item["vid"], {
        "fact_key": "no-status",
    })
    edges = store.find_edges(limit=100)
    target = [e for e in edges if e["properties"].get("fact_key") == "no-status"][0]
    target["properties"].pop("creation_status", None)
    engine = ValidationEngine(store)
    result = engine.run()
    warnings = [f for f in result["findings"] if f["rule"] == "missing_creation_status"]
    assert warnings
    assert warnings[0]["severity"] == "WARNING"


def test_deterministic_creation_status_no_warning():
    store = _seeded_store()
    result = ValidationEngine(store).run()
    ambiguous = [f for f in result["findings"] if f["rule"] == "ambiguous_needs_review"]
    assert not ambiguous


def test_human_confirmed_and_manual_statuses_accepted():
    store = MemoryGraphStore()
    project = store.upsert_vertex("Project", {"canonical_id": "urn:test:project:1", "name": "Test Project"})
    item = store.upsert_vertex("WorkItem", {
        "canonical_id": "urn:test:item:1", "issue_key": "TEST-1", "summary": "Test item",
        "ingestion_run_id": "run-1", "creation_status": "MANUAL",
    })
    store.upsert_edge("CONTAINS", project["vid"], item["vid"], {
        "fact_key": "manual-edge", "creation_status": "HUMAN_CONFIRMED",
    })
    result = ValidationEngine(store).run()
    errors = [f for f in result["findings"] if f["rule"] == "invalid_creation_status"]
    assert not errors
    ambiguous = [f for f in result["findings"] if f["rule"] == "ambiguous_needs_review"]
    assert not ambiguous


def test_quality_metrics_computation():
    vertices = [
        {"canonical_id": "v1", "label": "WorkItem", "vid": "1", "properties": {"ingestion_run_id": "run-1"}},
        {"canonical_id": "v2", "label": "Evidence", "vid": "2", "properties": {}},
    ]
    edges = [
        {"eid": "e1", "label": "IMPLEMENTS", "out_v": "1", "in_v": "2", "properties": {"evidence_key": "ev1"}},
    ]
    findings = [{"severity": "WARNING", "rule": "test"}]
    quality = QualityMetrics.compute(vertices, edges, findings)
    assert quality.total_vertices == 2
    assert quality.evidence_coverage == 1.0
    assert quality.warning_count == 1
    assert quality.error_count == 0
