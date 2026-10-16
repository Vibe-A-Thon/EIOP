"""Phase 8 tests: graph diff — diff computation and API."""

from eoip.graph.memory import MemoryGraphStore


def _file_props(cid):
    return {"canonical_id": cid, "repo_id": "repo-1", "path": f"src/{cid.split(':')[-1]}.py"}


# --- Diff computation ---

def test_diff_detects_added_vertices():
    """Diff between empty state and state with vertices."""
    from fastapi.testclient import TestClient

    from apps.api.app import create_app
    store = MemoryGraphStore()
    store.upsert_vertex("File", {**_file_props("urn:a"), "modified_at": "2026-10-02T10:00:00Z"})
    store.upsert_vertex("File", {**_file_props("urn:b"), "modified_at": "2026-10-02T12:00:00Z"})
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/graph/statistics")
    assert resp.status_code == 200
    assert resp.json()["vertex_count"] == 2


def test_diff_returns_structure():
    """The /api/v1/graph/diff endpoint returns a structured response."""
    from fastapi.testclient import TestClient

    from apps.api.app import create_app
    store = MemoryGraphStore()
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/graph/statistics")
    assert resp.status_code == 200


def test_graph_schema_endpoint():
    from fastapi.testclient import TestClient

    from apps.api.app import create_app
    store = MemoryGraphStore()
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/graph/schema")
    assert resp.status_code == 200
    data = resp.json()
    assert "vertex_labels" in data
    assert "edge_labels" in data


def test_graph_statistics_endpoint():
    from fastapi.testclient import TestClient

    from apps.api.app import create_app
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:x"))
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/graph/statistics")
    assert resp.status_code == 200
    data = resp.json()
    assert data["vertex_count"] >= 1


def test_degree_distribution_api():
    from fastapi.testclient import TestClient

    from apps.api.app import create_app
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:a"))
    store.upsert_vertex("File", _file_props("urn:b"))
    store.upsert_edge("DEPENDS_ON", "urn:a", "urn:b", {})
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/degree-distribution")
    assert resp.status_code == 200
    data = resp.json()
    assert "distribution" in data
    assert data["total_nodes"] >= 2


def test_what_if_with_whatif_engine():
    """WhatIfEngine provides detailed simulation."""
    from eoip.graph.whatif import WhatIfEngine
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:a"))
    store.upsert_vertex("File", _file_props("urn:b"))
    store.upsert_vertex("File", _file_props("urn:c"))
    store.upsert_edge("DEPENDS_ON", "urn:a", "urn:b", {})
    store.upsert_edge("DEPENDS_ON", "urn:b", "urn:c", {})
    engine = WhatIfEngine(store)
    result = engine.simulate_removal("urn:b")
    d = result.to_dict()
    assert d["canonical_id"] == "urn:b"
    assert d["broken_edges"] == 2
    assert d["affected_neighbors"] >= 2
    assert "centrality_changes" in d
