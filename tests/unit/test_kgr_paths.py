"""Phase 3 tests: path finding — all-shortest and k-shortest paths."""

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.paths import GraphPathFinder


def _file_props(cid):
    return {"canonical_id": cid, "repo_id": "repo-1", "path": f"src/{cid.split(':')[-1]}.py"}


def _build_chain(store, length=5):
    ids = [f"urn:node-{i}" for i in range(length)]
    for cid in ids:
        store.upsert_vertex("File", _file_props(cid))
    for i in range(length - 1):
        store.upsert_edge("DEPENDS_ON", ids[i], ids[i + 1], {})
    return ids


def _build_diamond(store):
    """A→B, A→C, B→D, C→D (two paths from A to D)."""
    for cid in ["urn:a", "urn:b", "urn:c", "urn:d"]:
        store.upsert_vertex("File", _file_props(cid))
    store.upsert_edge("DEPENDS_ON", "urn:a", "urn:b", {})
    store.upsert_edge("DEPENDS_ON", "urn:a", "urn:c", {})
    store.upsert_edge("DEPENDS_ON", "urn:b", "urn:d", {})
    store.upsert_edge("DEPENDS_ON", "urn:c", "urn:d", {})


# --- All shortest paths ---

def test_all_shortest_paths_chain():
    store = MemoryGraphStore()
    ids = _build_chain(store, 4)
    finder = GraphPathFinder(store)
    paths = finder.all_shortest_paths(ids[0], ids[3])
    assert len(paths) == 1
    assert paths[0] == ids


def test_all_shortest_paths_diamond_two_paths():
    store = MemoryGraphStore()
    _build_diamond(store)
    finder = GraphPathFinder(store)
    paths = finder.all_shortest_paths("urn:a", "urn:d")
    assert len(paths) == 2
    for p in paths:
        assert p[0] == "urn:a" and p[-1] == "urn:d"
        assert len(p) == 3


def test_all_shortest_paths_unreachable():
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:x"))
    store.upsert_vertex("File", _file_props("urn:y"))
    finder = GraphPathFinder(store)
    assert finder.all_shortest_paths("urn:x", "urn:y") == []


def test_all_shortest_paths_same_node():
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:x"))
    finder = GraphPathFinder(store)
    paths = finder.all_shortest_paths("urn:x", "urn:x")
    assert paths == [["urn:x"]]


# --- K-shortest paths ---

def test_k_shortest_chain():
    store = MemoryGraphStore()
    ids = _build_chain(store, 4)
    finder = GraphPathFinder(store)
    paths = finder.k_shortest_paths(ids[0], ids[3], k=3)
    assert len(paths) >= 1
    assert paths[0] == ids


def test_k_shortest_diamond():
    store = MemoryGraphStore()
    _build_diamond(store)
    finder = GraphPathFinder(store)
    paths = finder.k_shortest_paths("urn:a", "urn:d", k=5)
    assert len(paths) >= 2


# --- API: /api/v1/graph/shortest-paths ---

def test_api_shortest_paths_returns_paths():
    from fastapi.testclient import TestClient

    from apps.api.app import create_app
    store = MemoryGraphStore()
    _build_chain(store, 3)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/shortest-paths", json={
        "source_id": "urn:node-0", "target_id": "urn:node-2", "max_paths": 5,
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] >= 1
    assert "urn:node-0" == data["paths"][0][0]


def test_api_shortest_paths_not_found():
    from fastapi.testclient import TestClient

    from apps.api.app import create_app
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:x"))
    store.upsert_vertex("File", _file_props("urn:y"))
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/shortest-paths", json={
        "source_id": "urn:x", "target_id": "urn:y", "max_paths": 5,
    })
    assert resp.status_code == 200
    assert resp.json()["count"] == 0
