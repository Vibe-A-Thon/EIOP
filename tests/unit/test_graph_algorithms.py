"""Tests for graph algorithm modules: community, similarity, paths, anomaly."""

from eoip.graph.anomaly import AnomalyDetector, AnomalyResult
from eoip.graph.community import CommunityDetectionEngine, CommunityResult
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.paths import GraphPathFinder
from eoip.graph.similarity import SimilarityEngine, SimilarityResult


def _vertex(store, label, canonical_id, **props):
    return store.upsert_vertex(label, {"canonical_id": canonical_id, "name": canonical_id, **props})


def _build_graph():
    store = MemoryGraphStore()
    a = _vertex(store, "WorkItem", "item:A", issue_key="A-1", summary="A")
    b = _vertex(store, "WorkItem", "item:B", issue_key="B-1", summary="B")
    c = _vertex(store, "Commit", "commit:C", commit_sha="abc123")
    d = _vertex(store, "File", "file:D", repo_id="repo1", path="d.py")
    e = _vertex(store, "File", "file:E", repo_id="repo1", path="e.py")
    f = _vertex(store, "CodeSymbol", "symbol:F", qualified_name="f.run", symbol_kind="function")
    store.upsert_edge("IMPLEMENTS", c["vid"], a["vid"], {})
    store.upsert_edge("IMPLEMENTS", c["vid"], b["vid"], {})
    store.upsert_edge("MODIFIES", c["vid"], d["vid"], {})
    store.upsert_edge("MODIFIES", c["vid"], e["vid"], {})
    store.upsert_edge("DECLARES", d["vid"], f["vid"], {})
    store.upsert_edge("DECLARES", e["vid"], f["vid"], {})
    return store


def _build_disconnected_graph():
    store = MemoryGraphStore()
    a = _vertex(store, "WorkItem", "item:A", issue_key="A-1", summary="A")
    b = _vertex(store, "WorkItem", "item:B", issue_key="B-1", summary="B")
    store.upsert_edge("PARENT_OF", a["vid"], b["vid"], {})
    _vertex(store, "File", "file:isolated", repo_id="repo1", path="isolated.py")
    return store


# --- Community detection ---

def test_label_propagation_returns_result():
    store = _build_graph()
    engine = CommunityDetectionEngine(store)
    result = engine.label_propagation()
    assert isinstance(result, CommunityResult)
    assert result.community_count >= 1
    assert result.algorithm == "label_propagation"
    assert isinstance(result.modularity, float)


def test_label_propagation_assigns_all_nodes():
    store = _build_graph()
    engine = CommunityDetectionEngine(store)
    result = engine.label_propagation()
    all_members = set()
    for c in result.communities:
        all_members.update(c["members"])
    assert len(all_members) == store.count_vertices()


def test_louvain_returns_result():
    store = _build_graph()
    engine = CommunityDetectionEngine(store)
    result = engine.louvain(resolution=1.0)
    assert isinstance(result, CommunityResult)
    assert result.community_count >= 1
    assert result.algorithm == "louvain"


def test_community_to_dict():
    store = _build_graph()
    engine = CommunityDetectionEngine(store)
    result = engine.label_propagation()
    d = result.to_dict()
    assert "communities" in d
    assert "community_count" in d
    assert "modularity" in d
    assert "algorithm" in d
    assert d["community_count"] == len(d["communities"])


def test_community_empty_graph():
    store = MemoryGraphStore()
    engine = CommunityDetectionEngine(store)
    result = engine.label_propagation()
    assert result.community_count == 0
    assert result.communities == []


# --- Similarity ---

def test_jaccard_returns_results():
    store = _build_graph()
    engine = SimilarityEngine(store)
    results = engine.jaccard("commit:C", limit=5)
    assert isinstance(results, list)
    for r in results:
        assert isinstance(r, SimilarityResult)
        assert r.score >= 0


def test_adamic_adar_returns_results():
    store = _build_graph()
    engine = SimilarityEngine(store)
    results = engine.adamic_adar("commit:C", limit=5)
    assert isinstance(results, list)


def test_common_neighbors_returns_results():
    store = _build_graph()
    engine = SimilarityEngine(store)
    results = engine.common_neighbors("file:D", limit=5)
    assert isinstance(results, list)


def test_similarity_nonexistent_node():
    store = _build_graph()
    engine = SimilarityEngine(store)
    results = engine.jaccard("nonexistent:x", limit=5)
    assert results == []


def test_similarity_to_dict():
    r = SimilarityResult(canonical_id="item:A", score=0.75, common_neighbors=3)
    d = r.to_dict()
    assert d["canonical_id"] == "item:A"
    assert d["score"] == 0.75
    assert d["common_neighbors"] == 3


def test_similarity_sorted_descending():
    store = _build_graph()
    engine = SimilarityEngine(store)
    results = engine.jaccard("commit:C", limit=10)
    scores = [r.score for r in results]
    assert scores == sorted(scores, reverse=True)


# --- Path finding ---

def test_all_shortest_paths_finds_path():
    store = _build_graph()
    finder = GraphPathFinder(store)
    paths = finder.all_shortest_paths("commit:C", "symbol:F", max_paths=5)
    assert len(paths) >= 1
    for path in paths:
        assert path[0] == "commit:C"
        assert path[-1] == "symbol:F"


def test_all_shortest_paths_no_path():
    store = _build_disconnected_graph()
    finder = GraphPathFinder(store)
    paths = finder.all_shortest_paths("item:A", "file:isolated", max_paths=5)
    assert paths == []


def test_all_shortest_paths_same_node():
    store = _build_graph()
    finder = GraphPathFinder(store)
    paths = finder.all_shortest_paths("commit:C", "commit:C", max_paths=5)
    assert len(paths) == 1
    assert paths[0] == ["commit:C"]


def test_shortest_paths_nonexistent():
    store = _build_graph()
    finder = GraphPathFinder(store)
    paths = finder.all_shortest_paths("nonexistent:x", "commit:C", max_paths=5)
    assert paths == []


def test_shortest_paths_length():
    store = _build_graph()
    finder = GraphPathFinder(store)
    paths = finder.all_shortest_paths("commit:C", "symbol:F", max_paths=10)
    if len(paths) > 1:
        lengths = [len(p) for p in paths]
        assert all(l == lengths[0] for l in lengths)


# --- Anomaly detection ---

def test_degree_zscore_outliers():
    store = MemoryGraphStore()
    hub = _vertex(store, "WorkItem", "hub:node", issue_key="HUB-1", summary="Hub")
    for i in range(20):
        leaf = _vertex(store, "File", f"leaf:{i}", repo_id="repo1", path=f"leaf{i}.py")
        store.upsert_edge("REFERENCES", hub["vid"], leaf["vid"], {})
    _vertex(store, "File", "isolated:x", repo_id="repo1", path="iso.py")
    detector = AnomalyDetector(store)
    results = detector.degree_zscore_outliers(threshold=1.5)
    assert isinstance(results, list)
    if results:
        assert isinstance(results[0], AnomalyResult)
        hub_found = any(r.canonical_id == "hub:node" for r in results)
        assert hub_found


def test_anomaly_to_dict():
    r = AnomalyResult(canonical_id="x:1", anomaly_type="degree_outlier", score=3.5, details={"degree": 20})
    d = r.to_dict()
    assert d["canonical_id"] == "x:1"
    assert d["anomaly_type"] == "degree_outlier"
    assert d["score"] == 3.5
    assert d["details"]["degree"] == 20


def test_anomaly_empty_graph():
    store = MemoryGraphStore()
    detector = AnomalyDetector(store)
    results = detector.degree_zscore_outliers(threshold=2.0)
    assert results == []


def test_anomaly_uniform_graph():
    store = MemoryGraphStore()
    nodes = [_vertex(store, "File", f"file:{i}", repo_id="repo1", path=f"f{i}.py") for i in range(5)]
    for i in range(4):
        store.upsert_edge("DEPENDS_ON", nodes[i]["vid"], nodes[i + 1]["vid"], {})
    detector = AnomalyDetector(store)
    results = detector.degree_zscore_outliers(threshold=3.0)
    assert len(results) == 0


# --- Full centrality ---

def test_full_centrality_betweenness():
    from eoip.graph.metrics import GraphMetricsEngine
    store = _build_graph()
    engine = GraphMetricsEngine(store)
    results = engine.full_centrality(["commit:C"], ["betweenness", "closeness", "pagerank"])
    assert "commit:C" in results
    m = results["commit:C"]
    assert m.betweenness >= 0
    assert m.closeness >= 0
    assert m.page_rank >= 0


def test_full_centrality_degree_only():
    from eoip.graph.metrics import GraphMetricsEngine
    store = _build_graph()
    engine = GraphMetricsEngine(store)
    results = engine.full_centrality(["commit:C"], ["degree"])
    assert "commit:C" in results
    assert results["commit:C"].degree >= 4


# --- Extended algorithms ---

def _build_cycle_graph():
    store = MemoryGraphStore()
    nodes = {}
    for n in ["A", "B", "C", "D", "E", "F"]:
        nodes[n] = _vertex(store, "WorkItem", f"item:{n}", issue_key=f"{n}-1")
    store.upsert_edge("PARENT_OF", nodes["A"]["vid"], nodes["B"]["vid"], {})
    store.upsert_edge("PARENT_OF", nodes["B"]["vid"], nodes["C"]["vid"], {})
    store.upsert_edge("PARENT_OF", nodes["C"]["vid"], nodes["D"]["vid"], {})
    store.upsert_edge("PARENT_OF", nodes["D"]["vid"], nodes["A"]["vid"], {})
    store.upsert_edge("PARENT_OF", nodes["B"]["vid"], nodes["E"]["vid"], {})
    store.upsert_edge("PARENT_OF", nodes["E"]["vid"], nodes["F"]["vid"], {})
    return store


def test_extended_ring_detection():
    from eoip.graph.algorithms import GraphAlgorithms
    store = _build_cycle_graph()
    algo = GraphAlgorithms(store)
    rings = algo.detect_rings(max_length=6, limit=10)
    assert isinstance(rings, list)
    for r in rings:
        assert r.length >= 2
        assert r.cycle[0] == r.cycle[-1]


def test_extended_intersection_detection():
    from eoip.graph.algorithms import GraphAlgorithms
    store = _build_cycle_graph()
    algo = GraphAlgorithms(store)
    result = algo.detect_intersection("item:A", "item:E", max_depth=3)
    assert result.subgraph_a_root == "item:A"
    assert isinstance(result.intersection_nodes, list)


def test_extended_weighted_shortest_path():
    from eoip.graph.algorithms import GraphAlgorithms
    store = _build_cycle_graph()
    algo = GraphAlgorithms(store)
    result = algo.weighted_shortest_path("item:A", "item:F")
    assert result is not None
    assert result.path[0] == "item:A"
    assert result.path[-1] == "item:F"
    assert result.hop_count == len(result.path) - 1


def test_extended_single_source_weighted():
    from eoip.graph.algorithms import GraphAlgorithms
    store = _build_cycle_graph()
    algo = GraphAlgorithms(store)
    results = algo.single_source_weighted_paths("item:A", limit=10)
    assert isinstance(results, dict)
    assert "item:A" not in results


def test_extended_k_step_neighbors():
    from eoip.graph.algorithms import GraphAlgorithms
    store = _build_cycle_graph()
    algo = GraphAlgorithms(store)
    result = algo.k_step_neighbors("item:A", k=2, limit=100)
    assert result.center == "item:A"
    assert result.total_count > 0


def test_extended_k_jump():
    from eoip.graph.algorithms import GraphAlgorithms
    store = _build_cycle_graph()
    algo = GraphAlgorithms(store)
    result = algo.k_jump("item:A", k=3, walks=20, seed=42)
    assert isinstance(result, dict)


def test_extended_custom_path():
    from eoip.graph.algorithms import GraphAlgorithms
    store = _build_cycle_graph()
    algo = GraphAlgorithms(store)
    paths = algo.custom_path("item:A", "item:F", max_depth=5, max_paths=3)
    assert isinstance(paths, list)
    for p in paths:
        assert p[0] == "item:A"
        assert p[-1] == "item:F"


def test_extended_ray_detection():
    from eoip.graph.algorithms import GraphAlgorithms
    store = _build_cycle_graph()
    algo = GraphAlgorithms(store)
    result = algo.ray_detection("item:A", direction="outgoing", max_depth=5)
    assert result.source == "item:A"
    assert result.direction == "outgoing"
    assert result.depth_reached >= 0


def test_extended_co_neighbors():
    from eoip.graph.algorithms import GraphAlgorithms
    store = _build_cycle_graph()
    algo = GraphAlgorithms(store)
    result = algo.co_neighbors("item:A", "item:C")
    assert result.source == "item:A"
    assert result.target == "item:C"


def test_extended_personal_rank():
    from eoip.graph.algorithms import GraphAlgorithms
    store = _build_cycle_graph()
    algo = GraphAlgorithms(store)
    results = algo.personal_rank("item:A", limit=5)
    assert isinstance(results, list)


def test_extended_neighbor_rank():
    from eoip.graph.algorithms import GraphAlgorithms
    store = _build_cycle_graph()
    algo = GraphAlgorithms(store)
    results = algo.neighbor_rank("item:A", limit=5)
    assert isinstance(results, list)


def test_extended_model_similarity():
    from eoip.graph.algorithms import GraphAlgorithms
    store = _build_cycle_graph()
    algo = GraphAlgorithms(store)
    result = algo.model_similarity(["item:A", "item:B"], ["item:C", "item:D"])
    assert "node_jaccard" in result
    assert "combined_score" in result
