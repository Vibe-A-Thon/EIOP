"""Tests for lens framework, graph playback, and production APIs (G2-P10)."""

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.lens import (
    KnowledgeContext, list_lenses, lens_data, LENS_CATALOG,
)
from eoip.graph.playback import build_event_stream, build_evidence_panel, export_timeline
from fastapi.testclient import TestClient
from apps.api.app import create_app


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _rich_store():
    store = MemoryGraphStore()
    svc = store.upsert_vertex("Service", {
        "canonical_id": "urn:svc:auth", "service_id": "auth", "name": "Auth Service",
        "created_at": "2026-01-01T00:00:00Z", "source_system": "manual",
    })
    ev = store.upsert_vertex("Evidence", {
        "canonical_id": "urn:ev:1", "source_system": "github", "source_ref": "repo/main",
        "method": "api_ingest",
    })
    store.upsert_edge("EVIDENCED_BY", svc["vid"], ev["vid"], {"fact_key": "ev:svc:1"})
    f1 = store.upsert_vertex("File", {
        "canonical_id": "urn:f:auth", "repo_id": "r1", "path": "src/auth.py",
        "created_at": "2026-01-02T00:00:00Z",
    })
    store.upsert_edge("DEPENDS_ON", f1["vid"], svc["vid"], {"fact_key": "dep:f:svc"})
    tc = store.upsert_vertex("TestCase", {
        "canonical_id": "urn:tc:1", "name": "test_auth",
        "created_at": "2026-01-03T00:00:00Z",
    })
    store.upsert_edge("TESTS", tc["vid"], f1["vid"], {"fact_key": "tests:tc:f"})
    deploy = store.upsert_vertex("Deployment", {
        "canonical_id": "urn:deploy:v1", "name": "v1.0",
        "created_at": "2026-01-10T08:00:00Z",
    })
    inc = store.upsert_vertex("Incident", {
        "canonical_id": "urn:inc:1", "incident_number": "INC-001",
        "summary": "Auth outage", "created_at": "2026-01-10T10:00:00Z",
    })
    store.upsert_edge("TRIGGERED_BY", inc["vid"], deploy["vid"], {"fact_key": "trig:inc:deploy"})
    commit = store.upsert_vertex("Commit", {
        "canonical_id": "urn:commit:abc", "commit_sha": "abc123",
        "message": "Fix auth", "created_at": "2026-01-10T07:00:00Z",
    })
    store.upsert_edge("RESOLVES", commit["vid"], inc["vid"], {"fact_key": "res:commit:inc"})
    wi = store.upsert_vertex("WorkItem", {
        "canonical_id": "urn:wi:1", "issue_key": "AUTH-1", "summary": "Implement auth",
    })
    c1 = store.upsert_vertex("WorkItemChange", {
        "canonical_id": "urn:change:1", "change_id": "ch1",
        "field_name": "status", "from_value": "Open", "to_value": "Done",
        "created_at": "2026-01-05T10:00:00Z",
    })
    store.upsert_edge("HAS_CHANGE", wi["vid"], c1["vid"], {"fact_key": "hc:1"})
    req = store.upsert_vertex("Requirement", {
        "canonical_id": "urn:req:1", "name": "Auth feature",
    })
    return store


# ---------------------------------------------------------------------------
# Lens Framework tests
# ---------------------------------------------------------------------------

def test_list_lenses():
    lenses = list_lenses()
    assert len(lenses) == 20
    ids = [l["id"] for l in lenses]
    assert "search" in ids
    assert "ontology" in ids


def test_lens_context_roundtrip():
    ctx = KnowledgeContext(root_entities=["urn:svc:auth"], domains=["CODE", "OPS"])
    d = ctx.to_dict()
    ctx2 = KnowledgeContext.from_dict(d)
    assert ctx2.root_entities == ["urn:svc:auth"]
    assert ctx2.domains == ["CODE", "OPS"]


def test_search_lens():
    store = _rich_store()
    ctx = KnowledgeContext(root_entities=["urn:svc:auth"])
    result = lens_data(store, "search", ctx)
    assert result["lens"] == "search"
    assert len(result["results"]) >= 1


def test_evidence_lens():
    store = _rich_store()
    ctx = KnowledgeContext(root_entities=["urn:svc:auth"])
    result = lens_data(store, "evidence", ctx)
    assert result["lens"] == "evidence"
    assert result["chains"][0]["count"] >= 1


def test_impact_lens():
    store = _rich_store()
    ctx = KnowledgeContext(root_entities=["urn:svc:auth"])
    result = lens_data(store, "impact", ctx)
    assert result["lens"] == "impact"
    assert result["impacts"][0]["dependent_count"] >= 1


def test_timeline_lens():
    store = _rich_store()
    ctx = KnowledgeContext(root_entities=["urn:wi:1"])
    result = lens_data(store, "timeline", ctx)
    assert result["lens"] == "timeline"
    assert len(result["events"]) >= 1


def test_architecture_lens():
    store = _rich_store()
    ctx = KnowledgeContext()
    result = lens_data(store, "architecture", ctx)
    assert result["lens"] == "architecture"
    assert len(result["services"]) >= 1


def test_trust_lens():
    store = _rich_store()
    ctx = KnowledgeContext()
    result = lens_data(store, "trust", ctx)
    assert result["lens"] == "trust"
    assert 0 <= result["evidence_coverage"] <= 1


def test_ontology_lens():
    store = _rich_store()
    ctx = KnowledgeContext()
    result = lens_data(store, "ontology", ctx)
    assert result["lens"] == "ontology"
    assert result["vertex_types"] > 0
    assert result["domains"]


def test_graph_lens():
    store = _rich_store()
    ctx = KnowledgeContext(root_entities=["urn:svc:auth"])
    result = lens_data(store, "graph", ctx)
    assert result["lens"] == "graph"
    assert len(result["nodes"]) >= 1


def test_runtime_lens():
    store = _rich_store()
    ctx = KnowledgeContext()
    result = lens_data(store, "runtime", ctx)
    assert result["lens"] == "runtime"
    assert len(result["incidents"]) >= 1


def test_requirement_lens():
    store = _rich_store()
    ctx = KnowledgeContext()
    result = lens_data(store, "requirement", ctx)
    assert result["lens"] == "requirement"
    assert len(result["requirements"]) >= 1


def test_decision_lens():
    store = _rich_store()
    ctx = KnowledgeContext()
    result = lens_data(store, "decision", ctx)
    assert result["lens"] == "decision"


def test_test_lens():
    store = _rich_store()
    ctx = KnowledgeContext()
    result = lens_data(store, "test", ctx)
    assert result["lens"] == "test"
    assert result["test_cases"] >= 1


def test_unknown_lens():
    store = _rich_store()
    ctx = KnowledgeContext()
    result = lens_data(store, "nonexistent", ctx)
    assert "error" in result


def test_change_lens():
    store = _rich_store()
    ctx = KnowledgeContext(root_entities=["urn:wi:1"])
    result = lens_data(store, "change", ctx)
    assert result["lens"] == "change"
    assert len(result["entities"]) >= 1


def test_knowledge_health_lens():
    store = _rich_store()
    ctx = KnowledgeContext()
    result = lens_data(store, "knowledge_health", ctx)
    assert result["lens"] == "knowledge_health"


def test_api_lens():
    store = _rich_store()
    ctx = KnowledgeContext()
    result = lens_data(store, "api", ctx)
    assert result["lens"] == "api"


def test_release_lens():
    store = _rich_store()
    ctx = KnowledgeContext()
    result = lens_data(store, "release", ctx)
    assert result["lens"] == "release"


def test_process_lens():
    store = _rich_store()
    ctx = KnowledgeContext()
    result = lens_data(store, "process", ctx)
    assert result["lens"] == "process"


def test_security_lens():
    store = _rich_store()
    ctx = KnowledgeContext()
    result = lens_data(store, "security", ctx)
    assert result["lens"] == "security"


def test_agent_lens():
    store = _rich_store()
    ctx = KnowledgeContext()
    result = lens_data(store, "agent", ctx)
    assert result["lens"] == "agent"


def test_simulation_lens():
    store = _rich_store()
    ctx = KnowledgeContext()
    result = lens_data(store, "simulation", ctx)
    assert result["lens"] == "simulation"
    assert result["available"]


# ---------------------------------------------------------------------------
# Playback tests
# ---------------------------------------------------------------------------

def test_playback_event_stream():
    store = _rich_store()
    result = build_event_stream(store, "urn:inc:1")
    assert result["root"] == "urn:inc:1"
    assert result["total_events"] >= 1
    cids = [e["canonical_id"] for e in result["events"]]
    assert "urn:inc:1" in cids


def test_playback_follows_edges():
    store = _rich_store()
    result = build_event_stream(store, "urn:inc:1", max_depth=2)
    cids = [e["canonical_id"] for e in result["events"]]
    assert "urn:deploy:v1" in cids or "urn:commit:abc" in cids


def test_playback_sorted_by_timestamp():
    store = _rich_store()
    result = build_event_stream(store, "urn:inc:1")
    timestamps = [e["timestamp"] for e in result["events"] if e["timestamp"]]
    assert timestamps == sorted(timestamps)


def test_playback_not_found():
    store = _rich_store()
    result = build_event_stream(store, "urn:nonexistent")
    assert "error" in result


def test_playback_max_events():
    store = _rich_store()
    result = build_event_stream(store, "urn:inc:1", max_events=2)
    assert result["total_events"] <= 2


def test_evidence_panel():
    store = _rich_store()
    result = build_evidence_panel(store, "urn:svc:auth")
    assert result["entity"] == "urn:svc:auth"
    assert len(result["evidence"]) >= 1
    assert result["evidence"][0]["source_system"] == "github"


def test_evidence_panel_not_found():
    store = _rich_store()
    result = build_evidence_panel(store, "urn:nonexistent")
    assert "error" in result


def test_export_timeline_json():
    store = _rich_store()
    result = export_timeline(store, "urn:inc:1", format="json")
    assert result["format"] == "json"
    assert "events" in result


def test_export_timeline_csv():
    store = _rich_store()
    result = export_timeline(store, "urn:inc:1", format="csv")
    assert result["format"] == "csv"
    assert "timestamp" in result["content"]


# ---------------------------------------------------------------------------
# API Endpoint tests
# ---------------------------------------------------------------------------

def test_api_lens_catalog():
    store = _rich_store()
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/lens/catalog")
    assert resp.status_code == 200
    assert len(resp.json()["lenses"]) == 20


def test_api_lens_view():
    store = _rich_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/lens/search", json={"root_entities": ["urn:svc:auth"]})
    assert resp.status_code == 200
    assert resp.json()["lens"] == "search"


def test_api_lens_evidence():
    store = _rich_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/lens/evidence", json={"root_entities": ["urn:svc:auth"]})
    assert resp.status_code == 200
    assert resp.json()["chains"]


def test_api_lens_ontology():
    store = _rich_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/lens/ontology", json={})
    assert resp.status_code == 200
    assert resp.json()["vertex_types"] > 0


def test_api_playback_stream():
    store = _rich_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/playback/stream", json={"root_cid": "urn:inc:1"})
    assert resp.status_code == 200
    assert resp.json()["total_events"] >= 1


def test_api_playback_evidence():
    store = _rich_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/playback/evidence", json={"root_cid": "urn:svc:auth"})
    assert resp.status_code == 200
    assert "evidence" in resp.json()


def test_api_playback_export():
    store = _rich_store()
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/playback/export", json={"root_cid": "urn:inc:1", "format": "csv"})
    assert resp.status_code == 200
    assert resp.json()["format"] == "csv"


def test_api_graph_health():
    store = _rich_store()
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/health/graph")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"
    assert resp.json()["vertices"] > 0


def test_api_admin_schema():
    store = _rich_store()
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/admin/schema")
    assert resp.status_code == 200
    assert resp.json()["vertex_types"] > 0
    assert resp.json()["domains"]
