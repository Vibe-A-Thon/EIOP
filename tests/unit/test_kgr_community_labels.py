"""Phase 10 tests: community auto-labeling, detect_with_labels, label override."""

from eoip.graph.community import CommunityDetectionEngine
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

from apps.api.app import create_app


def _file_props(cid, name=None):
    return {"canonical_id": cid, "repo_id": "repo-1", "path": f"src/{cid.split(':')[-1]}.py",
            "name": name or cid.split(":")[-1]}


def _build_labeled_cliques(store):
    for i in range(4):
        store.upsert_vertex("File", _file_props(f"urn:auth-{i}", name=f"auth-module-{i}"))
    for i in range(4):
        for j in range(i + 1, 4):
            store.upsert_edge("DEPENDS_ON", f"urn:auth-{i}", f"urn:auth-{j}", {})
    for i in range(3):
        store.upsert_vertex("Service", {
            "canonical_id": f"urn:svc-{i}", "service_id": f"svc-{i}",
            "name": f"api-gateway-{i}",
        })
    for i in range(3):
        for j in range(i + 1, 3):
            store.upsert_edge("DEPENDS_ON", f"urn:svc-{i}", f"urn:svc-{j}", {})


# --- Community auto-labeling ---

def test_label_community_generates_label():
    store = MemoryGraphStore()
    _build_labeled_cliques(store)
    engine = CommunityDetectionEngine(store)
    label = engine.label_community([f"urn:auth-{i}" for i in range(4)])
    assert isinstance(label, str)
    assert len(label) > 0
    assert "File" in label


def test_label_community_with_names():
    store = MemoryGraphStore()
    _build_labeled_cliques(store)
    engine = CommunityDetectionEngine(store)
    label = engine.label_community([f"urn:svc-{i}" for i in range(3)])
    assert "Service" in label


def test_label_community_empty():
    store = MemoryGraphStore()
    engine = CommunityDetectionEngine(store)
    label = engine.label_community([])
    assert label == "Unknown"


def test_detect_with_labels_adds_auto_label():
    store = MemoryGraphStore()
    _build_labeled_cliques(store)
    engine = CommunityDetectionEngine(store)
    result = engine.detect_with_labels(algorithm="label_propagation")
    assert result.community_count >= 1
    for comm in result.communities:
        assert "auto_label" in comm
        assert isinstance(comm["auto_label"], str)
        assert len(comm["auto_label"]) > 0


def test_detect_with_labels_louvain():
    store = MemoryGraphStore()
    _build_labeled_cliques(store)
    engine = CommunityDetectionEngine(store)
    result = engine.detect_with_labels(algorithm="louvain")
    assert result.algorithm == "louvain"
    for comm in result.communities:
        assert "auto_label" in comm


# --- API endpoint for cluster with labels ---

def test_api_cluster_includes_labels():
    store = MemoryGraphStore()
    _build_labeled_cliques(store)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/cluster", json={"algorithm": "label_propagation"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["community_count"] >= 1
