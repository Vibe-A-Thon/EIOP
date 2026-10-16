"""Tests for EOIP Query Language (EQL)."""

from eoip.graph.memory import MemoryGraphStore
from eoip.query.eql import parse_and_execute
from fastapi.testclient import TestClient

from apps.api.app import create_app


def _store():
    store = MemoryGraphStore()
    svc = store.upsert_vertex("Service", {
        "canonical_id": "urn:svc:auth", "service_id": "auth", "name": "Auth Service",
        "created_at": "2026-01-01T00:00:00Z", "source_system": "manual",
    })
    f1 = store.upsert_vertex("File", {
        "canonical_id": "urn:f:auth", "repo_id": "r1", "path": "src/auth.py",
    })
    store.upsert_edge("DEPENDS_ON", f1["vid"], svc["vid"], {"fact_key": "dep:f:svc"})
    ev = store.upsert_vertex("Evidence", {
        "canonical_id": "urn:ev:1", "source_system": "github", "source_ref": "repo/main", "method": "api",
    })
    store.upsert_edge("EVIDENCED_BY", svc["vid"], ev["vid"], {"fact_key": "ev:1"})
    store.upsert_vertex("TestCase", {
        "canonical_id": "urn:tc:1", "name": "test_auth",
    })
    return store


def test_find_by_label():
    store = _store()
    result = parse_and_execute(store, "FIND Service")
    assert result["query"] == "FIND"
    assert result["total"] >= 1
    assert result["results"][0]["label"] == "Service"


def test_find_with_where():
    store = _store()
    result = parse_and_execute(store, "FIND Service WHERE name = Auth Service")
    assert result["total"] >= 1


def test_find_with_contains():
    store = _store()
    result = parse_and_execute(store, "FIND Service WHERE name CONTAINS auth")
    assert result["total"] >= 1


def test_find_with_limit():
    store = _store()
    result = parse_and_execute(store, "FIND Service LIMIT 1")
    assert result["total"] <= 1


def test_find_unknown_label():
    store = _store()
    result = parse_and_execute(store, "FIND Nonexistent")
    assert "error" in result


def test_find_all():
    store = _store()
    result = parse_and_execute(store, "FIND *")
    assert result["total"] >= 3


def test_path_found():
    store = _store()
    result = parse_and_execute(store, "PATH urn:f:auth TO urn:svc:auth")
    assert result["found"] is True
    assert result["length"] >= 2


def test_path_not_found():
    store = _store()
    result = parse_and_execute(store, "PATH urn:svc:auth TO urn:tc:1")
    assert result["found"] is False


def test_path_missing_entity():
    store = _store()
    result = parse_and_execute(store, "PATH urn:nonexistent TO urn:svc:auth")
    assert "error" in result


def test_neighbors():
    store = _store()
    result = parse_and_execute(store, "NEIGHBORS urn:svc:auth")
    assert result["total"] >= 1


def test_neighbors_with_label():
    store = _store()
    result = parse_and_execute(store, "NEIGHBORS urn:svc:auth LABEL DEPENDS_ON")
    assert all(n["via"] == "DEPENDS_ON" for n in result["neighbors"])


def test_impact():
    store = _store()
    result = parse_and_execute(store, "IMPACT urn:svc:auth")
    assert result["query"] == "IMPACT"
    cids = [a["canonical_id"] for a in result["affected"]]
    assert "urn:f:auth" in cids


def test_why():
    store = _store()
    result = parse_and_execute(store, "WHY urn:svc:auth")
    assert result["total_reasons"] >= 1


def test_why_not():
    store = _store()
    result = parse_and_execute(store, "WHY NOT urn:svc:auth urn:tc:1")
    assert result["connected"] is False


def test_what_changed():
    store = _store()
    result = parse_and_execute(store, "WHAT CHANGED urn:svc:auth")
    assert "changes" in result


def test_context():
    store = _store()
    result = parse_and_execute(store, "CONTEXT urn:svc:auth")
    assert "when" in result


def test_edges_from():
    store = _store()
    result = parse_and_execute(store, "EDGES FROM urn:svc:auth")
    assert result["query"] == "EDGES"
    assert result["total"] >= 1


def test_edges_to():
    store = _store()
    result = parse_and_execute(store, "EDGES TO urn:svc:auth")
    assert result["query"] == "EDGES"
    assert result["total"] >= 1


def test_count_label():
    store = _store()
    result = parse_and_execute(store, "COUNT Service")
    assert result["count"] >= 1


def test_count_vertices():
    store = _store()
    result = parse_and_execute(store, "COUNT VERTICES")
    assert result["count"] >= 3


def test_count_edges():
    store = _store()
    result = parse_and_execute(store, "COUNT EDGES")
    assert result["count"] >= 2


def test_domains():
    store = _store()
    result = parse_and_execute(store, "DOMAINS")
    assert "META" in result["domains"]


def test_labels():
    store = _store()
    result = parse_and_execute(store, "LABELS")
    assert "Service" in result["labels"]


def test_edge_labels():
    store = _store()
    result = parse_and_execute(store, "EDGE LABELS")
    assert "DEPENDS_ON" in result["labels"]


def test_help():
    store = _store()
    result = parse_and_execute(store, "HELP")
    assert "help" in result


def test_empty_query():
    store = _store()
    result = parse_and_execute(store, "")
    assert "error" in result


def test_unrecognised():
    store = _store()
    result = parse_and_execute(store, "SOMETHING WEIRD")
    assert "error" in result


# --- API Tests ---

def test_api_eql():
    store = _store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/query/eql", json={"query": "FIND Service"})
    assert resp.status_code == 200
    assert resp.json()["total"] >= 1


def test_api_eql_empty():
    store = _store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/query/eql", json={})
    assert resp.status_code == 400


def test_api_connectors_catalog():
    store = _store()
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/connectors/catalog")
    assert resp.status_code == 200
    assert len(resp.json()["connectors"]) >= 10


def test_api_pipeline_status():
    store = _store()
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/pipeline/status")
    assert resp.status_code == 200
    assert resp.json()["status"] == "operational"
    assert resp.json()["graph"]["vertices"] >= 3
