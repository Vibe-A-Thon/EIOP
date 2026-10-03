"""Phase 5 tests: similarity engine — Jaccard, Adamic-Adar, common neighbors + API."""

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.similarity import SimilarityEngine, SimilarityResult


def _file_props(cid):
    return {"canonical_id": cid, "repo_id": "repo-1", "path": f"src/{cid.split(':')[-1]}.py"}


def _build_triangle_with_extra(store):
    """A-B, A-C, B-C, plus D connected to B and C (shared neighbors with A)."""
    for cid in ["urn:a", "urn:b", "urn:c", "urn:d"]:
        store.upsert_vertex("File", _file_props(cid))
    store.upsert_edge("DEPENDS_ON", "urn:a", "urn:b", {})
    store.upsert_edge("DEPENDS_ON", "urn:a", "urn:c", {})
    store.upsert_edge("DEPENDS_ON", "urn:b", "urn:c", {})
    store.upsert_edge("DEPENDS_ON", "urn:d", "urn:b", {})
    store.upsert_edge("DEPENDS_ON", "urn:d", "urn:c", {})


# --- Jaccard ---

def test_jaccard_finds_similar_nodes():
    store = MemoryGraphStore()
    _build_triangle_with_extra(store)
    engine = SimilarityEngine(store)
    results = engine.jaccard("urn:a", limit=10)
    assert len(results) >= 1
    assert all(isinstance(r, SimilarityResult) for r in results)
    ids = [r.canonical_id for r in results]
    assert "urn:d" in ids


def test_jaccard_scores_between_0_and_1():
    store = MemoryGraphStore()
    _build_triangle_with_extra(store)
    engine = SimilarityEngine(store)
    results = engine.jaccard("urn:a")
    for r in results:
        assert 0.0 <= r.score <= 1.0


def test_jaccard_nonexistent_node():
    store = MemoryGraphStore()
    engine = SimilarityEngine(store)
    assert engine.jaccard("urn:missing") == []


# --- Adamic-Adar ---

def test_adamic_adar_finds_similar():
    store = MemoryGraphStore()
    _build_triangle_with_extra(store)
    engine = SimilarityEngine(store)
    results = engine.adamic_adar("urn:a")
    assert len(results) >= 1
    assert all(r.score > 0 for r in results)


def test_adamic_adar_scores_positive():
    store = MemoryGraphStore()
    _build_triangle_with_extra(store)
    engine = SimilarityEngine(store)
    results = engine.adamic_adar("urn:a")
    for r in results:
        assert r.score >= 0.0


def test_adamic_adar_nonexistent():
    store = MemoryGraphStore()
    engine = SimilarityEngine(store)
    assert engine.adamic_adar("urn:missing") == []


# --- Common neighbors ---

def test_common_neighbors_counts():
    store = MemoryGraphStore()
    _build_triangle_with_extra(store)
    engine = SimilarityEngine(store)
    results = engine.common_neighbors("urn:a")
    assert len(results) >= 1
    d_result = [r for r in results if r.canonical_id == "urn:d"]
    assert d_result
    assert d_result[0].common_neighbors >= 2


def test_common_neighbors_to_dict():
    store = MemoryGraphStore()
    _build_triangle_with_extra(store)
    engine = SimilarityEngine(store)
    results = engine.common_neighbors("urn:a")
    if results:
        d = results[0].to_dict()
        assert "canonical_id" in d and "score" in d and "common_neighbors" in d


# --- API ---

def test_api_similarity_jaccard():
    from apps.api.app import create_app
    from fastapi.testclient import TestClient
    store = MemoryGraphStore()
    _build_triangle_with_extra(store)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/similarity", json={
        "canonical_id": "urn:a", "algorithm": "jaccard", "limit": 10,
    })
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_api_similarity_adamic_adar():
    from apps.api.app import create_app
    from fastapi.testclient import TestClient
    store = MemoryGraphStore()
    _build_triangle_with_extra(store)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/similarity", json={
        "canonical_id": "urn:a", "algorithm": "adamic_adar", "limit": 10,
    })
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
