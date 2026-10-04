"""Phase 10 tests: orphaned entity detection, stale entity detection, dead code."""

from eoip.graph.anomaly import AnomalyDetector
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

from apps.api.app import create_app


def _file_props(cid, **extra):
    return {"canonical_id": cid, "repo_id": "repo-1", "path": f"src/{cid.split(':')[-1]}.py", **extra}


def _svc_props(cid, **extra):
    return {"canonical_id": cid, "service_id": cid.split(":")[-1], "name": cid, **extra}


# --- Orphaned entity detection ---

def test_orphaned_entities_detected():
    store = MemoryGraphStore()
    a = store.upsert_vertex("File", _file_props("urn:connected"))
    store.upsert_vertex("File", _file_props("urn:orphan"))  # orphan: intentionally unreferenced
    c = store.upsert_vertex("File", _file_props("urn:source"))
    store.upsert_edge("DEPENDS_ON", c["vid"], a["vid"], {})
    detector = AnomalyDetector(store)
    results = detector.orphaned_entities()
    orphan_cids = [r.canonical_id for r in results]
    assert "urn:orphan" in orphan_cids
    assert "urn:source" in orphan_cids
    assert "urn:connected" not in orphan_cids


def test_orphaned_entities_filter_by_type():
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:orphan-file"))
    store.upsert_vertex("Service", _svc_props("urn:orphan-svc"))
    detector = AnomalyDetector(store)
    results = detector.orphaned_entities(entity_types=["File"])
    cids = [r.canonical_id for r in results]
    assert "urn:orphan-file" in cids
    assert "urn:orphan-svc" not in cids


def test_orphaned_excludes_meta_labels():
    store = MemoryGraphStore()
    store.upsert_vertex("GraphDomain", {"canonical_id": "urn:domain:CODE", "name": "CODE"})
    store.upsert_vertex("File", _file_props("urn:orphan"))
    detector = AnomalyDetector(store)
    results = detector.orphaned_entities()
    cids = [r.canonical_id for r in results]
    assert "urn:domain:CODE" not in cids
    assert "urn:orphan" in cids


def test_orphaned_api_endpoint():
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:orphan-1"))
    store.upsert_vertex("File", _file_props("urn:orphan-2"))
    a = store.upsert_vertex("File", _file_props("urn:connected"))
    b = store.upsert_vertex("File", _file_props("urn:source"))
    store.upsert_edge("DEPENDS_ON", b["vid"], a["vid"], {})
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/graph/orphaned")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] >= 2
    cids = [r["canonical_id"] for r in data["orphaned"]]
    assert "urn:orphan-1" in cids


def test_orphaned_api_with_type_filter():
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:orphan-file"))
    store.upsert_vertex("Service", _svc_props("urn:orphan-svc"))
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/graph/orphaned?entity_types=File")
    assert resp.status_code == 200
    cids = [r["canonical_id"] for r in resp.json()["orphaned"]]
    assert "urn:orphan-file" in cids
    assert "urn:orphan-svc" not in cids


def test_stale_entities_detected():
    store = MemoryGraphStore()
    store.upsert_vertex("File", {**_file_props("urn:stale"), "modified_at": "2020-01-01T00:00:00Z"})
    store.upsert_vertex("File", {**_file_props("urn:fresh"), "modified_at": "2099-01-01T00:00:00Z"})
    detector = AnomalyDetector(store)
    results = detector.stale_entities(threshold_hours=24)
    stale_cids = [r.canonical_id for r in results if r.anomaly_type == "stale"]
    assert "urn:stale" in stale_cids
    assert "urn:fresh" not in stale_cids


def test_stale_api_endpoint():
    store = MemoryGraphStore()
    store.upsert_vertex("File", {**_file_props("urn:old"), "modified_at": "2020-01-01T00:00:00Z"})
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/graph/stale?threshold_hours=24")
    assert resp.status_code == 200
    assert resp.json()["count"] >= 1
