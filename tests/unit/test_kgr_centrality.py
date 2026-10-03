"""Phase 3 tests: full centrality suite — 8 algorithms plus API."""

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.metrics import GraphMetricsEngine


def _file_props(cid):
    return {"canonical_id": cid, "repo_id": "repo-1", "path": f"src/{cid.split(':')[-1]}.py"}


def _build_star(store, center_id="urn:center", n_leaves=5):
    store.upsert_vertex("File", _file_props(center_id))
    for i in range(n_leaves):
        leaf_id = f"urn:leaf-{i}"
        store.upsert_vertex("File", _file_props(leaf_id))
        store.upsert_edge("DEPENDS_ON", center_id, leaf_id, {})


def _build_chain(store, length=5):
    ids = [f"urn:node-{i}" for i in range(length)]
    for cid in ids:
        store.upsert_vertex("File", _file_props(cid))
    for i in range(length - 1):
        store.upsert_edge("DEPENDS_ON", ids[i], ids[i + 1], {})
    return ids


# --- Betweenness centrality ---

def test_betweenness_star_center_has_highest():
    store = MemoryGraphStore()
    _build_star(store)
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(["urn:center"], ["betweenness"])
    assert result["urn:center"].betweenness >= 0.0


def test_betweenness_chain_middle_highest():
    store = MemoryGraphStore()
    ids = _build_chain(store, 5)
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(ids, ["betweenness"])
    mid = result[ids[2]].betweenness
    end = result[ids[0]].betweenness
    assert mid >= end


def test_betweenness_isolated_node_is_zero():
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:alone"))
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(["urn:alone"], ["betweenness"])
    assert result["urn:alone"].betweenness == 0.0


def test_betweenness_normalized():
    store = MemoryGraphStore()
    ids = _build_chain(store, 4)
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(ids, ["betweenness"])
    for cid in ids:
        assert 0.0 <= result[cid].betweenness <= 1.0


# --- Closeness centrality ---

def test_closeness_star_center_highest():
    store = MemoryGraphStore()
    _build_star(store, n_leaves=4)
    engine = GraphMetricsEngine(store)
    all_ids = ["urn:center"] + [f"urn:leaf-{i}" for i in range(4)]
    result = engine.full_centrality(all_ids, ["closeness"])
    assert result["urn:center"].closeness >= result["urn:leaf-0"].closeness


def test_closeness_chain_center_higher_than_end():
    store = MemoryGraphStore()
    ids = _build_chain(store, 5)
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(ids, ["closeness"])
    assert result[ids[2]].closeness >= result[ids[0]].closeness


def test_closeness_isolated_is_zero():
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:alone"))
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(["urn:alone"], ["closeness"])
    assert result["urn:alone"].closeness == 0.0


def test_closeness_nonnegative():
    store = MemoryGraphStore()
    ids = _build_chain(store, 3)
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(ids, ["closeness"])
    for cid in ids:
        assert result[cid].closeness >= 0.0


# --- PageRank ---

def test_pagerank_star_all_positive():
    store = MemoryGraphStore()
    _build_star(store, n_leaves=5)
    all_ids = ["urn:center"] + [f"urn:leaf-{i}" for i in range(5)]
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(all_ids, ["pagerank"])
    for cid in all_ids:
        assert result[cid].page_rank > 0


def test_pagerank_chain_all_nonzero():
    store = MemoryGraphStore()
    ids = _build_chain(store, 4)
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(ids, ["pagerank"])
    total = sum(r.page_rank for r in result.values())
    assert total > 0


def test_pagerank_positive():
    store = MemoryGraphStore()
    ids = _build_chain(store, 3)
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(ids, ["pagerank"])
    for cid in ids:
        assert result[cid].page_rank > 0


def test_pagerank_empty_graph():
    store = MemoryGraphStore()
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality([], ["pagerank"])
    assert result == {}


# --- Eigenvector centrality ---

def test_eigenvector_star_center_highest():
    store = MemoryGraphStore()
    _build_star(store, n_leaves=4)
    all_ids = ["urn:center"] + [f"urn:leaf-{i}" for i in range(4)]
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(all_ids, ["eigenvector"])
    assert result["urn:center"].eigenvector >= result["urn:leaf-0"].eigenvector


def test_eigenvector_nonnegative():
    store = MemoryGraphStore()
    ids = _build_chain(store, 4)
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(ids, ["eigenvector"])
    for cid in ids:
        assert result[cid].eigenvector >= 0.0


def test_eigenvector_isolated_nonzero():
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:alone"))
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(["urn:alone"], ["eigenvector"])
    assert result["urn:alone"].eigenvector >= 0.0


def test_eigenvector_in_to_dict():
    store = MemoryGraphStore()
    _build_star(store, n_leaves=2)
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(["urn:center"], ["eigenvector"])
    d = result["urn:center"].to_dict()
    assert "eigenvector" in d


# --- Katz centrality ---

def test_katz_star_center_highest():
    store = MemoryGraphStore()
    _build_star(store, n_leaves=4)
    all_ids = ["urn:center"] + [f"urn:leaf-{i}" for i in range(4)]
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(all_ids, ["katz"])
    assert result["urn:center"].katz >= result["urn:leaf-0"].katz


def test_katz_nonnegative():
    store = MemoryGraphStore()
    ids = _build_chain(store, 3)
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(ids, ["katz"])
    for cid in ids:
        assert result[cid].katz >= 0.0


# --- HITS ---

def test_hits_hub_authority_nonnegative():
    store = MemoryGraphStore()
    ids = _build_chain(store, 4)
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(ids, ["hits"])
    for cid in ids:
        assert result[cid].hits_hub >= 0.0
        assert result[cid].hits_authority >= 0.0


def test_hits_in_to_dict():
    store = MemoryGraphStore()
    _build_star(store, n_leaves=2)
    engine = GraphMetricsEngine(store)
    result = engine.full_centrality(["urn:center"], ["hits"])
    d = result["urn:center"].to_dict()
    assert "hits_hub" in d and "hits_authority" in d


# --- API: /api/v1/graph/centrality/full ---

def test_api_centrality_full_returns_all_algorithms():
    from fastapi.testclient import TestClient

    from apps.api.app import create_app
    store = MemoryGraphStore()
    _build_star(store, n_leaves=3)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/centrality/full", json={
        "canonical_ids": ["urn:center"],
        "algorithms": ["degree", "betweenness", "closeness", "pagerank", "eigenvector", "katz", "hits", "harmonic"],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "urn:center" in data
    m = data["urn:center"]
    for key in ["degree", "betweenness", "closeness", "page_rank", "eigenvector", "katz", "hits_hub", "hits_authority", "harmonic"]:
        assert key in m, f"Missing {key}"


def test_api_centrality_full_default_algorithms():
    from fastapi.testclient import TestClient

    from apps.api.app import create_app
    store = MemoryGraphStore()
    _build_star(store, n_leaves=2)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/centrality/full", json={"canonical_ids": ["urn:center"]})
    assert resp.status_code == 200
    data = resp.json()
    assert "urn:center" in data
