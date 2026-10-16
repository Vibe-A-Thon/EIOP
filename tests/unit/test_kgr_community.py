"""Phase 4 tests: community detection — Leiden, Louvain, Label Propagation + API."""

from eoip.graph.community import CommunityDetectionEngine, CommunityResult
from eoip.graph.memory import MemoryGraphStore


def _file_props(cid):
    return {"canonical_id": cid, "repo_id": "repo-1", "path": f"src/{cid.split(':')[-1]}.py"}


def _build_two_cliques(store):
    """Two File cliques connected by a single bridge edge."""
    for i in range(4):
        store.upsert_vertex("File", _file_props(f"urn:a-{i}"))
    for i in range(4):
        for j in range(i + 1, 4):
            store.upsert_edge("DEPENDS_ON", f"urn:a-{i}", f"urn:a-{j}", {})

    for i in range(4):
        store.upsert_vertex("File", _file_props(f"urn:b-{i}"))
    for i in range(4):
        for j in range(i + 1, 4):
            store.upsert_edge("DEPENDS_ON", f"urn:b-{i}", f"urn:b-{j}", {})

    store.upsert_edge("DEPENDS_ON", "urn:a-0", "urn:b-0", {})


def _build_disconnected(store):
    """Three isolated nodes — no edges."""
    for cid in ["urn:x", "urn:y", "urn:z"]:
        store.upsert_vertex("File", _file_props(cid))


# --- Leiden ---

def test_leiden_detects_two_cliques():
    store = MemoryGraphStore()
    _build_two_cliques(store)
    engine = CommunityDetectionEngine(store)
    result = engine.leiden(resolution=1.0)
    assert isinstance(result, CommunityResult)
    assert result.algorithm == "leiden"
    assert result.community_count >= 2


def test_leiden_empty_graph():
    store = MemoryGraphStore()
    engine = CommunityDetectionEngine(store)
    result = engine.leiden()
    assert result.community_count == 0
    assert result.modularity == 0.0


def test_leiden_disconnected_nodes():
    store = MemoryGraphStore()
    _build_disconnected(store)
    engine = CommunityDetectionEngine(store)
    result = engine.leiden()
    assert result.community_count >= 1


def test_leiden_result_has_all_nodes():
    store = MemoryGraphStore()
    _build_two_cliques(store)
    engine = CommunityDetectionEngine(store)
    result = engine.leiden()
    all_members = set()
    for c in result.communities:
        all_members.update(c["members"])
    expected = {f"urn:a-{i}" for i in range(4)} | {f"urn:b-{i}" for i in range(4)}
    assert all_members == expected


# --- Louvain ---

def test_louvain_detects_two_cliques():
    store = MemoryGraphStore()
    _build_two_cliques(store)
    engine = CommunityDetectionEngine(store)
    result = engine.louvain(resolution=1.0)
    assert result.algorithm == "louvain"
    assert result.community_count >= 2


def test_louvain_empty_graph():
    store = MemoryGraphStore()
    engine = CommunityDetectionEngine(store)
    result = engine.louvain()
    assert result.community_count == 0


def test_louvain_single_node():
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:solo"))
    engine = CommunityDetectionEngine(store)
    result = engine.louvain()
    assert result.community_count == 1


def test_louvain_modularity_nonnegative():
    store = MemoryGraphStore()
    _build_two_cliques(store)
    engine = CommunityDetectionEngine(store)
    result = engine.louvain()
    assert result.modularity >= 0.0


# --- Label Propagation ---

def test_label_propagation_detects_communities():
    store = MemoryGraphStore()
    _build_two_cliques(store)
    engine = CommunityDetectionEngine(store)
    result = engine.label_propagation()
    assert result.algorithm == "label_propagation"
    assert result.community_count >= 1


def test_label_propagation_empty():
    store = MemoryGraphStore()
    engine = CommunityDetectionEngine(store)
    result = engine.label_propagation()
    assert result.community_count == 0


# --- API: /api/v1/graph/cluster ---

def test_api_cluster_leiden():
    from fastapi.testclient import TestClient

    from apps.api.app import create_app
    store = MemoryGraphStore()
    _build_two_cliques(store)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/cluster", json={"algorithm": "leiden", "resolution": 1.0})
    assert resp.status_code == 200
    data = resp.json()
    assert data["algorithm"] == "leiden"
    assert data["community_count"] >= 2


def test_api_cluster_default_algorithm():
    from fastapi.testclient import TestClient

    from apps.api.app import create_app
    store = MemoryGraphStore()
    _build_two_cliques(store)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/cluster", json={})
    assert resp.status_code == 200
    assert resp.json()["algorithm"] == "label_propagation"
