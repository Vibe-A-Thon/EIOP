"""Tests for GraphMetricsEngine and KGR API endpoints."""

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.metrics import BlastRadiusResult, CentralityMetrics, GraphMetricsEngine


def _vertex(store, label, canonical_id, **props):
    return store.upsert_vertex(label, {"canonical_id": canonical_id, "name": canonical_id, **props})


def _build_chain_store():
    store = MemoryGraphStore()
    a = _vertex(store, "WorkItem", "item:A", issue_key="A-1")
    b = _vertex(store, "Commit", "commit:B", commit_sha="abc")
    c = _vertex(store, "File", "file:C", path="c.py")
    d = _vertex(store, "CodeSymbol", "symbol:D", qualified_name="d.run")
    e = _vertex(store, "Evidence", "evidence:E", source_system="git", method="SOURCE_EVENT", evidence_key="ek:E")
    store.upsert_edge("IMPLEMENTS", b["vid"], a["vid"], {})
    store.upsert_edge("MODIFIES", b["vid"], c["vid"], {})
    store.upsert_edge("DECLARES", c["vid"], d["vid"], {})
    store.upsert_edge("EVIDENCED_BY", d["vid"], e["vid"], {})
    return store


def test_blast_radius_finds_downstream():
    store = _build_chain_store()
    engine = GraphMetricsEngine(store)
    result = engine.blast_radius("commit:B", max_depth=4)
    assert isinstance(result, BlastRadiusResult)
    assert result.total_affected >= 2
    assert result.target_id == "commit:B"
    assert "item:A" in result.affected_ids or "file:C" in result.affected_ids
    assert sum(result.by_depth.values()) == result.total_affected
    assert result.risk in ("LOW", "MEDIUM", "HIGH")


def test_blast_radius_unknown_entity():
    store = MemoryGraphStore()
    engine = GraphMetricsEngine(store)
    result = engine.blast_radius("nonexistent:x")
    assert result.total_affected == 0
    assert result.risk == "NONE"


def test_reverse_impact_finds_upstream():
    store = _build_chain_store()
    engine = GraphMetricsEngine(store)
    result = engine.reverse_impact("evidence:E", max_depth=4)
    assert isinstance(result, BlastRadiusResult)
    assert result.total_affected >= 1
    assert result.target_id == "evidence:E"


def test_centrality_computes_degree():
    store = _build_chain_store()
    engine = GraphMetricsEngine(store)
    metrics = engine.centrality(["commit:B", "file:C"])
    assert "commit:B" in metrics
    assert "file:C" in metrics
    m = metrics["commit:B"]
    assert isinstance(m, CentralityMetrics)
    assert m.out_degree >= 2
    assert m.degree == m.in_degree + m.out_degree


def test_centrality_missing_entity():
    store = MemoryGraphStore()
    engine = GraphMetricsEngine(store)
    metrics = engine.centrality(["nonexistent:x"])
    assert metrics == {}


def test_graph_statistics():
    store = _build_chain_store()
    engine = GraphMetricsEngine(store)
    stats = engine.graph_statistics()
    assert stats["vertex_count"] == 5
    assert stats["edge_count"] == 4
    assert 0 <= stats["density"] <= 1
    assert stats["vertex_label_count"] > 0
    assert stats["edge_label_count"] > 0


def test_graph_schema_returns_structure():
    store = MemoryGraphStore()
    engine = GraphMetricsEngine(store)
    schema = engine.graph_schema()
    assert "ontology_version" in schema
    assert "schema_version" in schema
    assert "vertex_labels" in schema
    assert "edge_labels" in schema
    assert "domains" in schema
    assert isinstance(schema["domains"], list)
    assert len(schema["vertex_labels"]) > 0


def test_blast_radius_to_dict():
    result = BlastRadiusResult("x:1", 3, {1: 2, 2: 1}, {"File": 2, "Commit": 1}, "LOW", ["a", "b", "c"])
    d = result.to_dict()
    assert d["target_id"] == "x:1"
    assert d["total_affected"] == 3
    assert d["by_depth"] == {1: 2, 2: 1}
    assert d["risk"] == "LOW"


def test_centrality_to_dict():
    m = CentralityMetrics("x:1", degree=5, in_degree=2, out_degree=3, betweenness=0.123456789, closeness=0.5, page_rank=0.01)
    d = m.to_dict()
    assert d["canonical_id"] == "x:1"
    assert d["degree"] == 5
    assert d["betweenness"] == 0.123457
    assert d["closeness"] == 0.5
