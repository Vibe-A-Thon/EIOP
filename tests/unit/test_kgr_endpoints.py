"""Tests for KGR API endpoints (blast-radius, reverse-impact, metrics, schema, statistics)."""

from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

from apps.api.app import create_app


def _vertex(store, label, canonical_id, **props):
    return store.upsert_vertex(label, {"canonical_id": canonical_id, "name": canonical_id, **props})


def _demo_store():
    store = MemoryGraphStore()
    a = _vertex(store, "WorkItem", "item:A", issue_key="A-1")
    b = _vertex(store, "Commit", "commit:B", commit_sha="abc")
    c = _vertex(store, "File", "file:C", path="c.py")
    d = _vertex(store, "CodeSymbol", "symbol:D", qualified_name="d.run")
    e = _vertex(store, "Evidence", "evidence:E", source_system="git", method="SOURCE_EVENT", evidence_key="ek:E")
    store.upsert_edge("IMPLEMENTS", b["vid"], a["vid"], {})
    store.upsert_edge("MODIFIES", b["vid"], c["vid"], {})
    store.upsert_edge("DECLARES", c["vid"], d["vid"], {})
    store.upsert_edge("EVIDENCED_BY", d["vid"], e["vid"], {})
    return store


def test_blast_radius_endpoint():
    client = TestClient(create_app(_demo_store()))
    r = client.post("/api/v1/graph/blast-radius", json={"canonical_id": "commit:B", "max_depth": 3})
    assert r.status_code == 200
    data = r.json()
    assert data["target_id"] == "commit:B"
    assert data["total_affected"] >= 2
    assert "by_depth" in data
    assert "by_type" in data
    assert data["risk"] in ("LOW", "MEDIUM", "HIGH")


def test_blast_radius_404_unknown():
    client = TestClient(create_app(MemoryGraphStore()))
    r = client.post("/api/v1/graph/blast-radius", json={"canonical_id": "unknown:x"})
    assert r.status_code == 404


def test_reverse_impact_endpoint():
    client = TestClient(create_app(_demo_store()))
    r = client.post("/api/v1/graph/reverse-impact", json={"canonical_id": "evidence:E", "max_depth": 4})
    assert r.status_code == 200
    data = r.json()
    assert data["target_id"] == "evidence:E"
    assert data["total_affected"] >= 1


def test_reverse_impact_404_unknown():
    client = TestClient(create_app(MemoryGraphStore()))
    r = client.post("/api/v1/graph/reverse-impact", json={"canonical_id": "unknown:x"})
    assert r.status_code == 404


def test_metrics_endpoint():
    client = TestClient(create_app(_demo_store()))
    r = client.post("/api/v1/graph/metrics", json={"canonical_ids": ["commit:B", "file:C"]})
    assert r.status_code == 200
    data = r.json()
    assert "commit:B" in data
    assert data["commit:B"]["degree"] >= 2
    assert data["commit:B"]["out_degree"] >= 2


def test_metrics_empty_for_unknown():
    client = TestClient(create_app(MemoryGraphStore()))
    r = client.post("/api/v1/graph/metrics", json={"canonical_ids": ["unknown:x"]})
    assert r.status_code == 200
    assert r.json() == {}


def test_schema_endpoint():
    store = _demo_store()
    client = TestClient(create_app(store))
    r = client.get("/api/v1/graph/schema")
    assert r.status_code == 200
    data = r.json()
    assert "ontology_version" in data
    assert "schema_version" in data
    assert "vertex_labels" in data
    assert "edge_labels" in data
    assert "domains" in data
    assert data["vertex_labels"]["CodeSymbol"]["domain"]
    assert data["vertex_labels"]["CodeSymbol"]["required_properties"]
    assert data["vertex_labels"]["WorkItem"]["instance_count"] == 1
    assert data["edge_labels"]["DECLARES"]["source_labels"]
    assert data["edge_labels"]["DECLARES"]["target_labels"]
    assert data["indexes"]
    assert all(index["name"] and index["fields"] for index in data["indexes"])


def test_statistics_endpoint():
    store = _demo_store()
    client = TestClient(create_app(store))
    r = client.get("/api/v1/graph/statistics")
    assert r.status_code == 200
    data = r.json()
    assert data["vertex_count"] == 5
    assert data["edge_count"] == 4
    assert 0 <= data["density"] <= 1


def test_blast_radius_validation():
    client = TestClient(create_app(MemoryGraphStore()))
    r = client.post("/api/v1/graph/blast-radius", json={"canonical_id": "", "max_depth": 0})
    assert r.status_code == 422


def test_metrics_validation_empty_list():
    client = TestClient(create_app(MemoryGraphStore()))
    r = client.post("/api/v1/graph/metrics", json={"canonical_ids": []})
    assert r.status_code == 422
