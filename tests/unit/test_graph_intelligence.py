"""Tests for the Graph Intelligence Engine and unified intelligent query."""

from __future__ import annotations

import pytest

from eoip.brain.graph_intelligence import (
    GraphIntelligenceEngine,
    GraphEvidence,
    GraphTopologySnapshot,
    ApproachFindings,
)


class FakeGraphStore:
    """Minimal graph store for testing the intelligence engine."""

    def __init__(self):
        self._vertices = {
            "v1": {
                "vid": "v1", "canonical_id": "svc:auth", "label": "Service",
                "properties": {"title": "AuthenticationService", "status": "active"},
            },
            "v2": {
                "vid": "v2", "canonical_id": "svc:orders", "label": "Service",
                "properties": {"title": "OrderService", "status": "active"},
            },
            "v3": {
                "vid": "v3", "canonical_id": "jira:PROJ-101", "label": "JiraIssue",
                "properties": {"title": "Fix login timeout", "key": "PROJ-101"},
            },
            "v4": {
                "vid": "v4", "canonical_id": "doc:arch", "label": "Document",
                "properties": {"title": "Architecture Overview", "name": "Architecture Overview"},
            },
        }
        self._edges = {
            "v1": [
                {"label": "DEPENDS_ON", "in_v": "v2", "in_cid": "svc:orders"},
                {"label": "DOCUMENTED_BY", "in_v": "v4", "in_cid": "doc:arch"},
            ],
            "v2": [
                {"label": "TRACKS", "in_v": "v3", "in_cid": "jira:PROJ-101"},
            ],
            "v3": [],
            "v4": [],
        }
        self._inbound = {
            "v1": [],
            "v2": [{"label": "DEPENDS_ON", "out_v": "v1", "out_cid": "svc:auth"}],
            "v3": [{"label": "TRACKS", "out_v": "v2", "out_cid": "svc:orders"}],
            "v4": [{"label": "DOCUMENTED_BY", "out_v": "v1", "out_cid": "svc:auth"}],
        }

    def find_vertices(self, label, filters, limit):
        return [v for v in self._vertices.values() if label is None or v["label"] == label][:limit]

    def edges_from(self, vid):
        return self._edges.get(vid, [])

    def edges_to(self, vid):
        return self._inbound.get(vid, [])

    def count_vertices(self, label):
        if label is None:
            return len(self._vertices)
        return sum(1 for v in self._vertices.values() if v["label"] == label)

    def count_edges(self, label=None):
        total = sum(len(e) for e in self._edges.values())
        return total

    def get_vertex_by_canonical_id(self, cid):
        for v in self._vertices.values():
            if v["canonical_id"] == cid:
                return v
        return None

    def find_vertex_by_property(self, key, value):
        for v in self._vertices.values():
            if v["properties"].get(key) == value:
                return v
        return None


@pytest.fixture
def store():
    return FakeGraphStore()


@pytest.fixture
def engine(store):
    return GraphIntelligenceEngine(graph_store=store)


@pytest.fixture
def empty_engine():
    return GraphIntelligenceEngine(graph_store=None)


@pytest.mark.enterprise
class TestGatherEvidence:
    def test_gathers_from_keywords(self, engine):
        evidence = engine.gather_evidence("AuthenticationService dependencies")
        assert len(evidence) > 0
        titles = [e.title for e in evidence]
        assert "AuthenticationService" in titles

    def test_includes_edges(self, engine):
        evidence = engine.gather_evidence("AuthenticationService")
        auth_ev = [e for e in evidence if e.title == "AuthenticationService"]
        assert auth_ev
        assert len(auth_ev[0].outbound_edges) == 2

    def test_empty_store_returns_empty(self, empty_engine):
        assert empty_engine.gather_evidence("anything") == []


@pytest.mark.enterprise
class TestTopologySnapshot:
    def test_snapshot_counts(self, engine):
        snap = engine.get_topology_snapshot()
        assert snap.total_vertices == 4
        assert snap.total_edges == 3
        assert "Service" in snap.label_distribution
        assert snap.avg_degree > 0

    def test_empty_snapshot(self, empty_engine):
        snap = empty_engine.get_topology_snapshot()
        assert snap.total_vertices == 0


@pytest.mark.enterprise
class TestDeterministicApproach:
    def test_returns_findings(self, engine):
        result = engine.execute_deterministic("AuthenticationService OrderService dependencies")
        assert result.approach == "DETERMINISTIC"
        assert result.confidence == 1.0
        assert len(result.findings) > 0

    def test_has_entities(self, engine):
        result = engine.execute_deterministic("AuthenticationService schema")
        assert len(result.discovered_entities) > 0

    def test_empty_store_fallback(self, empty_engine):
        result = empty_engine.execute_deterministic("test")
        assert result.confidence == 0.5
        assert any("no graph" in f.lower() for f in result.findings)


@pytest.mark.enterprise
class TestProbabilisticApproach:
    def test_returns_bayesian_findings(self, engine):
        result = engine.execute_probabilistic("AuthenticationService failure risk")
        assert result.approach == "PROBABILISTIC"
        assert len(result.findings) > 0

    def test_has_metrics(self, engine):
        result = engine.execute_probabilistic("risk")
        assert "degree_scores" in result.metrics


@pytest.mark.enterprise
class TestHeuristicApproach:
    def test_returns_centrality_ranking(self, engine):
        result = engine.execute_heuristic("bottleneck services")
        assert result.approach == "HEURISTIC"
        assert len(result.findings) > 0
        assert any("centrality" in f.lower() or "ranking" in f.lower() for f in result.findings)


@pytest.mark.enterprise
class TestStochasticApproach:
    def test_returns_simulation_results(self, engine):
        result = engine.execute_stochastic("chaos resilience")
        assert result.approach == "STOCHASTIC"
        assert len(result.findings) > 0
        assert any("monte carlo" in f.lower() or "simulation" in f.lower() or "survival" in f.lower()
                    for f in result.findings)


@pytest.mark.enterprise
class TestNonDeterministicApproach:
    def test_returns_emergent_patterns(self, engine):
        result = engine.execute_non_deterministic("service patterns")
        assert result.approach == "NON_DETERMINISTIC"
        assert len(result.findings) > 0


@pytest.mark.enterprise
class TestHybridApproach:
    def test_combines_all_approaches(self, engine):
        result = engine.execute_hybrid("comprehensive analysis")
        assert result.approach == "HYBRID"
        assert len(result.findings) >= 3
        assert any("[Deterministic]" in f for f in result.findings)
        assert any("[Probabilistic]" in f for f in result.findings)

    def test_has_sub_approach_metrics(self, engine):
        result = engine.execute_hybrid("system overview")
        assert "sub_approaches" in result.metrics
        assert "deterministic" in result.metrics["sub_approaches"]
        assert "probabilistic" in result.metrics["sub_approaches"]


@pytest.mark.enterprise
class TestBrainOSIntelligentQuery:
    def test_intelligent_query_with_store(self, store):
        from eoip.brain.brain_os import BrainOSKernel
        kernel = BrainOSKernel(graph_store=store)
        result = kernel.intelligent_query("What services exist in the graph?")
        assert "query" in result
        assert "enhanced_formulation" in result
        assert "graph_findings" in result
        assert "topology" in result
        assert "complementary_questions" in result
        assert "llm_synthesis" in result
        assert "narrative_markdown" in result
        assert result["confidence_score"] > 0
        assert result["latency_ms"] > 0
        assert len(result["graph_findings"]["findings"]) > 0
        assert result["topology"]["total_vertices"] == 4

    def test_intelligent_query_approaches(self, store):
        from eoip.brain.brain_os import BrainOSKernel
        kernel = BrainOSKernel(graph_store=store)
        for approach in ["DETERMINISTIC", "PROBABILISTIC", "HEURISTIC", "STOCHASTIC", "NON_DETERMINISTIC", "HYBRID"]:
            result = kernel.intelligent_query("test query", approach=approach)
            assert result["approach"] == approach, f"Failed for approach {approach}"
            assert result["graph_findings"]["methodology"]

    def test_intelligent_query_no_store(self):
        from eoip.brain.brain_os import BrainOSKernel
        kernel = BrainOSKernel(graph_store=None)
        result = kernel.intelligent_query("anything")
        assert result["query"] == "anything"
        assert result["narrative_markdown"]
