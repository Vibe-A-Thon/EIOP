"""Tests for native graph query operators (G2-P7)."""

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.query_operators import query_context, query_what_changed, query_why, query_why_not
from fastapi.testclient import TestClient

from apps.api.app import create_app


def _rich_store():
    store = MemoryGraphStore()
    svc = store.upsert_vertex("Service", {
        "canonical_id": "urn:svc:auth", "service_id": "auth", "name": "Auth Service",
        "source_system": "manual", "created_at": "2026-01-01T00:00:00Z",
        "ingestion_run_id": "run-1", "creation_status": "DETERMINISTIC",
    })
    ev = store.upsert_vertex("Evidence", {
        "canonical_id": "urn:ev:1", "source_system": "github", "source_ref": "repo/main",
        "method": "api_ingest",
    })
    store.upsert_edge("EVIDENCED_BY", svc["vid"], ev["vid"], {"fact_key": "ev:svc:1"})
    person = store.upsert_vertex("Person", {
        "canonical_id": "urn:person:dev1", "display_name": "Dev One", "email": "dev1@example.com",
    })
    wi = store.upsert_vertex("WorkItem", {
        "canonical_id": "urn:wi:1", "issue_key": "AUTH-1", "summary": "Implement auth",
        "ingestion_run_id": "run-1",
    })
    commit = store.upsert_vertex("Commit", {
        "canonical_id": "urn:commit:abc", "commit_sha": "abc123",
        "message": "Add auth handler", "author_email": "dev1@example.com",
        "created_at": "2026-01-15T10:00:00Z",
    })
    f1 = store.upsert_vertex("File", {"canonical_id": "urn:f:auth", "repo_id": "r1", "path": "src/auth.py"})
    store.upsert_edge("IMPLEMENTS", commit["vid"], wi["vid"], {"fact_key": "impl:1"})
    store.upsert_edge("MODIFIES", commit["vid"], f1["vid"], {"fact_key": "mod:1"})
    store.upsert_edge("AUTHORED_BY", commit["vid"], person["vid"], {"fact_key": "auth:1"})
    c1 = store.upsert_vertex("WorkItemChange", {
        "canonical_id": "urn:change:1", "change_id": "ch1",
        "field_name": "status", "from_value": "Open", "to_value": "In Progress",
        "created_at": "2026-01-10T00:00:00Z",
    })
    store.upsert_edge("HAS_CHANGE", wi["vid"], c1["vid"], {"fact_key": "hc:1"})
    return store


def test_query_why_evidence():
    store = _rich_store()
    result = query_why(store, "urn:svc:auth")
    assert result["total_reasons"] >= 1
    evidence = [r for r in result["reasons"] if r["type"] == "evidence"]
    assert evidence
    assert evidence[0]["method"] == "api_ingest"


def test_query_why_implementation():
    store = _rich_store()
    result = query_why(store, "urn:wi:1")
    impl = [r for r in result["reasons"] if r["type"] == "implementation"]
    assert impl


def test_query_why_not_found():
    store = _rich_store()
    result = query_why(store, "urn:nonexistent")
    assert "error" in result


def test_query_why_not_connected():
    store = _rich_store()
    result = query_why_not(store, "urn:svc:auth", "urn:wi:1")
    assert result["connected"] is False
    assert result["reasons"]


def test_query_why_not_direct_connection():
    store = _rich_store()
    result = query_why_not(store, "urn:commit:abc", "urn:wi:1")
    assert result["connected"] is True


def test_query_why_not_missing_entity():
    store = _rich_store()
    result = query_why_not(store, "urn:nonexistent", "urn:wi:1")
    assert result["connected"] is False
    assert any(r["type"] == "missing_entity" for r in result["reasons"])


def test_query_what_changed_field():
    store = _rich_store()
    result = query_what_changed(store, "urn:wi:1")
    field_changes = [c for c in result["changes"] if c["type"] == "field_change"]
    assert field_changes
    assert field_changes[0]["field"] == "status"


def test_query_what_changed_code():
    store = _rich_store()
    result = query_what_changed(store, "urn:f:auth")
    code_changes = [c for c in result["changes"] if c["type"] == "code_change"]
    assert code_changes
    assert code_changes[0]["sha"] == "abc123"


def test_query_what_changed_not_found():
    store = _rich_store()
    result = query_what_changed(store, "urn:nonexistent")
    assert "error" in result


def test_query_context_when():
    store = _rich_store()
    result = query_context(store, "urn:svc:auth")
    assert result["when"]["created_at"]


def test_query_context_who():
    store = _rich_store()
    result = query_context(store, "urn:commit:abc")
    assert result["who"]
    assert any(w.get("email") == "dev1@example.com" for w in result["who"])


def test_query_context_where():
    store = _rich_store()
    result = query_context(store, "urn:f:auth")
    assert result["where"]["path"] == "src/auth.py"
    assert result["where"]["domain"] == "CODE"


def test_query_context_how():
    store = _rich_store()
    result = query_context(store, "urn:svc:auth")
    assert result["how"]["creation_status"] == "DETERMINISTIC"


def test_query_context_not_found():
    store = _rich_store()
    result = query_context(store, "urn:nonexistent")
    assert "error" in result


# --- API Tests ---

def test_api_query_why():
    store = _rich_store()
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/query/why/urn:svc:auth")
    assert resp.status_code == 200
    assert resp.json()["total_reasons"] >= 1


def test_api_query_why_not():
    store = _rich_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/query/why-not", json={
        "source_cid": "urn:svc:auth", "target_cid": "urn:wi:1"
    })
    assert resp.status_code == 200


def test_api_query_why_not_missing_params():
    store = _rich_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/query/why-not", json={})
    assert resp.status_code == 400


def test_api_query_what_changed():
    store = _rich_store()
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/query/what-changed/urn:wi:1")
    assert resp.status_code == 200
    assert "changes" in resp.json()


def test_api_query_context():
    store = _rich_store()
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/query/context/urn:svc:auth")
    assert resp.status_code == 200
    assert "when" in resp.json()
    assert "who" in resp.json()
    assert "where" in resp.json()
    assert "how" in resp.json()
