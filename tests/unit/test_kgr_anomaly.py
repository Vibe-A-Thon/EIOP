"""Phase 8 tests: anomaly detection — degree z-score, dense subgraph + API."""

from eoip.graph.anomaly import AnomalyDetector
from eoip.graph.memory import MemoryGraphStore


def _file_props(cid):
    return {"canonical_id": cid, "repo_id": "repo-1", "path": f"src/{cid.split(':')[-1]}.py"}


def _build_star_with_outlier(store, spoke_count=5):
    """One hub with many spokes, plus several isolated nodes = hub is outlier."""
    store.upsert_vertex("File", _file_props("urn:hub"))
    for i in range(spoke_count):
        store.upsert_vertex("File", _file_props(f"urn:spoke-{i}"))
        store.upsert_edge("DEPENDS_ON", "urn:hub", f"urn:spoke-{i}", {})
    for i in range(10):
        store.upsert_vertex("File", _file_props(f"urn:iso-{i}"))


def _build_dense_clique(store):
    """A dense 5-node clique plus some loosely connected nodes."""
    for i in range(5):
        store.upsert_vertex("File", _file_props(f"urn:cliq-{i}"))
    for i in range(5):
        for j in range(i + 1, 5):
            store.upsert_edge("DEPENDS_ON", f"urn:cliq-{i}", f"urn:cliq-{j}", {})
    for i in range(8):
        store.upsert_vertex("File", _file_props(f"urn:loose-{i}"))
    store.upsert_edge("DEPENDS_ON", "urn:loose-0", "urn:loose-1", {})


# --- Degree z-score ---

def test_degree_zscore_finds_hub_outlier():
    store = MemoryGraphStore()
    _build_star_with_outlier(store, spoke_count=8)
    detector = AnomalyDetector(store)
    results = detector.degree_zscore_outliers(threshold=1.5)
    assert len(results) >= 1
    assert results[0].canonical_id == "urn:hub"
    assert results[0].anomaly_type == "degree_outlier"


def test_degree_zscore_empty_graph():
    store = MemoryGraphStore()
    detector = AnomalyDetector(store)
    results = detector.degree_zscore_outliers()
    assert results == []


def test_degree_zscore_uniform_graph():
    store = MemoryGraphStore()
    for i in range(4):
        store.upsert_vertex("File", _file_props(f"urn:n-{i}"))
    for i in range(4):
        store.upsert_edge("DEPENDS_ON", f"urn:n-{i}", f"urn:n-{(i+1)%4}", {})
    detector = AnomalyDetector(store)
    results = detector.degree_zscore_outliers(threshold=2.0)
    assert results == []


# --- Dense subgraph ---

def test_dense_subgraph_detects_clique():
    store = MemoryGraphStore()
    _build_dense_clique(store)
    detector = AnomalyDetector(store)
    results = detector.dense_subgraph_detection()
    assert len(results) >= 1
    assert results[0].anomaly_type == "dense_subgraph"
    assert results[0].details["cluster_size"] >= 3


def test_dense_subgraph_empty():
    store = MemoryGraphStore()
    detector = AnomalyDetector(store)
    results = detector.dense_subgraph_detection()
    assert results == []


# --- API ---

def test_api_anomalies():
    from apps.api.app import create_app
    from fastapi.testclient import TestClient
    store = MemoryGraphStore()
    _build_star_with_outlier(store, spoke_count=8)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/anomalies", json={"algorithms": ["degree_zscore"], "threshold": 1.5})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1
