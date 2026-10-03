"""Quality metrics N/A rules and new metric coverage (FR-VALID-003)."""

from datetime import UTC, datetime, timedelta

from eoip.graph.memory import MemoryGraphStore
from eoip.validation.engine import ValidationEngine
from eoip.validation.quality import QualityMetrics

NOW = datetime(2026, 10, 2, tzinfo=UTC)
RECENT = (NOW - timedelta(days=3)).isoformat()
STALE = (NOW - timedelta(days=90)).isoformat()

COVERAGE_KEYS = [
    "evidence_coverage",
    "provenance_coverage",
    "orphan_rate",
    "duplicate_rate",
    "freshness",
    "completeness",
    "schema_compliance",
]


def test_empty_graph_all_coverage_metrics_are_na():
    store = MemoryGraphStore()
    result = ValidationEngine(store).run()
    quality = result["quality"]
    for key in COVERAGE_KEYS:
        assert quality[key] is None, f"{key} should be N/A on an empty graph"
    assert quality["total_vertices"] == 0
    assert quality["total_edges"] == 0


def test_seeded_orphans_produce_orphan_rate():
    store = MemoryGraphStore()
    store.upsert_vertex("Project", {"canonical_id": "urn:test:project:1", "name": "P"})
    store.upsert_vertex("Project", {"canonical_id": "urn:test:project:2", "name": "Q"})
    connected = store.upsert_vertex(
        "WorkItem", {"canonical_id": "urn:test:item:1", "issue_key": "T-1", "summary": "S"}
    )
    project = store.get_vertex_by_canonical_id("urn:test:project:1")
    store.upsert_edge(
        "CONTAINS", project["vid"], connected["vid"], {"fact_key": "f-1", "creation_status": "DETERMINISTIC"}
    )
    result = ValidationEngine(store).run()
    assert result["quality"]["orphan_rate"] == round(1 / 3, 4)


def test_duplicate_canonical_ids_produce_duplicate_rate():
    vertices = [
        {"vid": "1", "canonical_id": "urn:dup:1", "label": "Project", "properties": {"name": "A"}},
        {"vid": "2", "canonical_id": "urn:dup:1", "label": "Project", "properties": {"name": "A"}},
        {"vid": "3", "canonical_id": "urn:dup:2", "label": "Project", "properties": {"name": "B"}},
    ]
    quality = QualityMetrics.compute(vertices, [], [], now=NOW)
    assert quality.duplicate_rate == round(1 / 3, 4)


def test_duplicate_rate_is_na_without_vertices():
    quality = QualityMetrics.compute([], [], [], now=NOW)
    assert quality.duplicate_rate is None
    assert quality.orphan_rate is None


def test_freshness_na_when_no_last_seen_values():
    vertices = [
        {"vid": "1", "canonical_id": "urn:a", "label": "Project", "properties": {"name": "A"}},
    ]
    quality = QualityMetrics.compute(vertices, [], [], now=NOW)
    assert quality.freshness is None


def test_freshness_counts_recent_last_seen():
    vertices = [
        {"vid": "1", "canonical_id": "urn:a", "label": "Project", "properties": {"name": "A", "last_seen": RECENT}},
        {"vid": "2", "canonical_id": "urn:b", "label": "Project", "properties": {"name": "B", "last_seen": STALE}},
        {"vid": "3", "canonical_id": "urn:c", "label": "Project", "properties": {"name": "C"}},
    ]
    quality = QualityMetrics.compute(vertices, [], [], now=NOW)
    assert quality.freshness == round(1 / 2, 4)


def test_completeness_and_schema_compliance():
    project = {"vid": "1", "canonical_id": "urn:p", "label": "Project", "properties": {"canonical_id": "urn:p", "name": "P"}}
    broken = {"vid": "2", "canonical_id": "urn:w", "label": "WorkItem", "properties": {"canonical_id": "urn:w", "issue_key": "T-1"}}
    edge_ok = {
        "eid": "e1", "label": "CONTAINS", "out_v": "1", "in_v": "2", "properties": {},
    }
    edge_bad = {
        "eid": "e2", "label": "PARENT_OF", "out_v": "1", "in_v": "2", "properties": {},
    }
    quality = QualityMetrics.compute([project, broken], [edge_ok, edge_bad], [], now=NOW)
    assert quality.completeness == 0.5
    assert quality.schema_compliance == 0.5


def test_completeness_and_schema_compliance_na_when_nothing_checked():
    quality = QualityMetrics.compute([], [], [], now=NOW)
    assert quality.completeness is None
    assert quality.schema_compliance is None
