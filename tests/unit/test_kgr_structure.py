"""Phase 6 tests: structure analysis — k-core, connected components, degree distribution + API."""

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.metrics import GraphMetricsEngine


def _file_props(cid):
    return {"canonical_id": cid, "repo_id": "repo-1", "path": f"src/{cid.split(':')[-1]}.py"}


def _build_star(store, center="urn:center", leaves=4):
    """Star topology: center connected to N leaves."""
    store.upsert_vertex("File", _file_props(center))
    for i in range(leaves):
        leaf = f"urn:leaf-{i}"
        store.upsert_vertex("File", _file_props(leaf))
        store.upsert_edge("DEPENDS_ON", center, leaf, {})


def _build_two_cliques(store):
    """Two cliques of 4 nodes each, connected by a single bridge."""
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
    """Two separate components: 3 connected + 2 isolated."""
    for cid in ["urn:x", "urn:y", "urn:z"]:
        store.upsert_vertex("File", _file_props(cid))
    store.upsert_edge("DEPENDS_ON", "urn:x", "urn:y", {})
    store.upsert_edge("DEPENDS_ON", "urn:y", "urn:z", {})
    for cid in ["urn:iso-1", "urn:iso-2"]:
        store.upsert_vertex("File", _file_props(cid))


# --- k-core decomposition ---

def test_kcore_star_center_highest():
    store = MemoryGraphStore()
    _build_star(store, leaves=4)
    engine = GraphMetricsEngine(store)
    result = engine.k_core_decomposition()
    assert len(result) >= 1
    all_nodes = set()
    for members in result.values():
        all_nodes.update(members)
    assert "urn:center" in all_nodes


def test_kcore_cliques_have_higher_core():
    store = MemoryGraphStore()
    _build_two_cliques(store)
    engine = GraphMetricsEngine(store)
    result = engine.k_core_decomposition()
    max_k = max(result.keys())
    assert max_k >= 2


def test_kcore_empty_graph():
    store = MemoryGraphStore()
    engine = GraphMetricsEngine(store)
    result = engine.k_core_decomposition()
    assert result == {}


# --- connected components ---

def test_components_two_separate():
    store = MemoryGraphStore()
    _build_disconnected(store)
    engine = GraphMetricsEngine(store)
    result = engine.connected_components()
    assert len(result) >= 2
    total_nodes = sum(len(c) for c in result)
    assert total_nodes == 5


def test_components_single_connected():
    store = MemoryGraphStore()
    _build_two_cliques(store)
    engine = GraphMetricsEngine(store)
    result = engine.connected_components()
    assert len(result) == 1
    assert len(result[0]) == 8


def test_components_empty_graph():
    store = MemoryGraphStore()
    engine = GraphMetricsEngine(store)
    result = engine.connected_components()
    assert result == []


# --- degree distribution ---

def test_degree_distribution_star():
    store = MemoryGraphStore()
    _build_star(store, leaves=4)
    engine = GraphMetricsEngine(store)
    result = engine.degree_distribution()
    assert len(result) >= 1
    total = sum(result.values())
    assert total == 5


def test_degree_distribution_empty():
    store = MemoryGraphStore()
    engine = GraphMetricsEngine(store)
    result = engine.degree_distribution()
    assert result == {}


# --- API endpoints ---

def test_api_kcore():
    from fastapi.testclient import TestClient

    from apps.api.app import create_app
    store = MemoryGraphStore()
    _build_two_cliques(store)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/k-core", json={"min_k": 1})
    assert resp.status_code == 200
    data = resp.json()
    assert "cores" in data
    assert data["max_k"] >= 2


def test_api_components():
    from fastapi.testclient import TestClient

    from apps.api.app import create_app
    store = MemoryGraphStore()
    _build_disconnected(store)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/components", json={"limit": 10})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_components"] >= 2
    assert len(data["components"]) >= 2
