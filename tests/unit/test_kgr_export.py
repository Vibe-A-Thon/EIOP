"""Phase 5 tests: export formats, timeline scrubber, similarity API, and link prediction."""

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.similarity import SimilarityEngine
from fastapi.testclient import TestClient

from apps.api.app import create_app


def _file_props(cid):
    return {"canonical_id": cid, "repo_id": "repo-1", "path": f"src/{cid.split(':')[-1]}.py"}


def _build_triangle(store):
    """Three nodes forming a triangle with mutual edges."""
    for cid in ["urn:a", "urn:b", "urn:c"]:
        store.upsert_vertex("File", _file_props(cid))
    store.upsert_edge("DEPENDS_ON", "urn:a", "urn:b", {})
    store.upsert_edge("DEPENDS_ON", "urn:b", "urn:c", {})
    store.upsert_edge("DEPENDS_ON", "urn:c", "urn:a", {})


# --- Export component ---

def test_export_menu_file_exists():
    import os
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "components", "ExportMenu.jsx"))


def test_export_menu_has_7_formats():
    import os
    path = os.path.join("apps", "web", "src", "kgr", "components", "ExportMenu.jsx")
    with open(path) as f:
        content = f.read()
    assert "'png'" in content
    assert "'svg'" in content
    assert "'pdf'" in content
    assert "'json-ld'" in content
    assert "'graphml'" in content
    assert "'csv'" in content
    assert "'clipboard'" in content


# --- Timeline scrubber ---

def test_timeline_scrubber_file_exists():
    import os
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "components", "TimelineScrubber.jsx"))


# --- Similarity API ---

def test_similarity_jaccard():
    store = MemoryGraphStore()
    _build_triangle(store)
    engine = SimilarityEngine(store)
    results = engine.jaccard("urn:a", limit=5)
    assert isinstance(results, list)


def test_similarity_adamic_adar():
    store = MemoryGraphStore()
    _build_triangle(store)
    engine = SimilarityEngine(store)
    results = engine.adamic_adar("urn:a", limit=5)
    assert isinstance(results, list)


def test_similarity_common_neighbors():
    store = MemoryGraphStore()
    _build_triangle(store)
    engine = SimilarityEngine(store)
    results = engine.common_neighbors("urn:a", limit=5)
    assert isinstance(results, list)


def test_similarity_api_endpoint():
    store = MemoryGraphStore()
    _build_triangle(store)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/similarity", json={"canonical_id": "urn:a", "algorithm": "jaccard", "limit": 5})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# --- Link prediction ---

def test_link_prediction_engine():
    store = MemoryGraphStore()
    for cid in ["urn:a", "urn:b", "urn:c", "urn:d"]:
        store.upsert_vertex("File", _file_props(cid))
    store.upsert_edge("DEPENDS_ON", "urn:a", "urn:b", {})
    store.upsert_edge("DEPENDS_ON", "urn:a", "urn:c", {})
    store.upsert_edge("DEPENDS_ON", "urn:d", "urn:b", {})
    store.upsert_edge("DEPENDS_ON", "urn:d", "urn:c", {})
    engine = SimilarityEngine(store)
    predictions = engine.link_prediction("urn:a", algorithm="common_neighbors", limit=5)
    assert isinstance(predictions, list)
    if predictions:
        assert predictions[0]["source_id"] == "urn:a"
        assert "score" in predictions[0]


def test_link_prediction_api_endpoint():
    store = MemoryGraphStore()
    for cid in ["urn:a", "urn:b", "urn:c", "urn:d"]:
        store.upsert_vertex("File", _file_props(cid))
    store.upsert_edge("DEPENDS_ON", "urn:a", "urn:b", {})
    store.upsert_edge("DEPENDS_ON", "urn:a", "urn:c", {})
    store.upsert_edge("DEPENDS_ON", "urn:d", "urn:b", {})
    store.upsert_edge("DEPENDS_ON", "urn:d", "urn:c", {})
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/link-prediction", json={"canonical_id": "urn:a", "algorithm": "common_neighbors", "limit": 5})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# --- Diff API ---

def test_diff_api_endpoint():
    store = MemoryGraphStore()
    store.upsert_vertex("File", {**_file_props("urn:x"), "modified_at": "2026-10-02T10:00:00Z"})
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/diff", json={"snapshot_a": "2026-10-01T00:00:00Z", "snapshot_b": "2026-10-02T11:00:00Z"})
    assert resp.status_code == 200
    data = resp.json()
    assert "added_nodes" in data
    assert "removed_nodes" in data
    assert "modified_nodes" in data
