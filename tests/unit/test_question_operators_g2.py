import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.query_operators import (
    execute_question_operator,
    query_how,
    query_what_changed,
    query_what_if,
    query_when,
    query_where,
    query_who,
    query_why,
    query_why_not,
)


@pytest.fixture
def store():
    s = MemoryGraphStore()
    svc_auth = s.upsert_vertex("Service", {
        "canonical_id": "urn:svc:auth",
        "service_id": "auth",
        "name": "Auth Service",
        "source_system": "kubernetes",
        "source_uri": "k8s://cluster/auth",
        "created_at": "2026-01-01T00:00:00Z",
        "modified_at": "2026-02-01T12:00:00Z",
        "creation_status": "DETERMINISTIC",
        "ingestion_run_id": "run-42",
        "mapper_version": "v2.1",
    })
    svc_billing = s.upsert_vertex("Service", {
        "canonical_id": "urn:svc:billing",
        "service_id": "billing",
        "name": "Billing Service",
        "source_system": "kubernetes",
        "created_at": "2026-01-05T00:00:00Z",
    })
    person = s.upsert_vertex("Person", {
        "canonical_id": "urn:person:alice",
        "display_name": "Alice Engineer",
        "email": "alice@example.com",
    })
    file_v = s.upsert_vertex("File", {
        "canonical_id": "urn:file:auth_py",
        "repo_id": "repo-core",
        "path": "services/auth.py",
    })
    commit = s.upsert_vertex("Commit", {
        "canonical_id": "urn:commit:c101",
        "commit_sha": "c101abc",
        "message": "Update auth token validation",
        "author_email": "alice@example.com",
        "created_at": "2026-02-01T11:00:00Z",
    })

    # Edges
    s.upsert_edge("CALLS", svc_billing["vid"], svc_auth["vid"], {})
    s.upsert_edge("MODIFIES", commit["vid"], file_v["vid"], {})
    s.upsert_edge("AUTHORED_BY", commit["vid"], person["vid"], {})
    s.upsert_edge("ASSIGNED_TO", file_v["vid"], person["vid"], {})

    return s


@pytest.mark.req("G2-QOP-002")
def test_operator_why_not(store):
    # Billing calls Auth, but Auth does NOT call Billing
    res = query_why_not(store, "urn:svc:auth", "urn:svc:billing")
    assert res["connected"] is False
    assert len(res["reasons"]) > 0
    assert any("missing_edge" in r["type"] for r in res["reasons"])

    # Direct connection exists Billing -> Auth
    res_connected = query_why_not(store, "urn:svc:billing", "urn:svc:auth")
    assert res_connected["connected"] is True


@pytest.mark.req("G2-QOP-003")
def test_operator_what_if_simulation(store):
    # Simulates outage of auth service: billing depends on it via CALLS
    res = query_what_if(store, "urn:svc:auth", {"action": "NODE_FAILURE"})
    assert res["simulated"] is True
    assert res["hypothesis"]["action"] == "NODE_FAILURE"
    assert res["impacted_count"] >= 1
    assert any(ent["canonical_id"] == "urn:svc:billing" for ent in res["impacted_entities"])
    assert res["blast_radius_score"] > 0
    assert len(res["evidence"]) > 0


@pytest.mark.req("G2-QOP-004")
def test_operator_what_changed(store):
    res = query_what_changed(store, "urn:file:auth_py")
    assert res["total_changes"] >= 1
    code_changes = [c for c in res["changes"] if c["type"] == "code_change"]
    assert len(code_changes) >= 1
    assert code_changes[0]["sha"] == "c101abc"
    assert code_changes[0]["author"] == "alice@example.com"


@pytest.mark.req("G2-QOP-005")
def test_operator_when(store):
    res = query_when(store, "urn:svc:auth")
    assert "when" in res
    assert res["when"]["created_at"] == "2026-01-01T00:00:00Z"
    assert res["when"]["modified_at"] == "2026-02-01T12:00:00Z"
    assert len(res["evidence"]) >= 2


@pytest.mark.req("G2-QOP-006")
def test_operator_who(store):
    res = query_who(store, "urn:file:auth_py")
    assert "who" in res
    assert len(res["who"]) >= 1
    assert any(w["name"] == "Alice Engineer" for w in res["who"])
    assert len(res["evidence"]) >= 1


@pytest.mark.req("G2-QOP-007")
def test_operator_where(store):
    res = query_where(store, "urn:svc:auth")
    assert "where" in res
    assert res["where"]["source_system"] == "kubernetes"
    assert res["where"]["source_uri"] == "k8s://cluster/auth"
    assert res["where"]["domain"] == "CODE"


@pytest.mark.req("G2-QOP-008")
def test_operator_how(store):
    res = query_how(store, "urn:svc:auth")
    assert "how" in res
    assert res["how"]["creation_status"] == "DETERMINISTIC"
    assert res["how"]["ingestion_run_id"] == "run-42"
    assert res["how"]["mapper_version"] == "v2.1"


@pytest.mark.req("G2-QOP-009")
def test_operator_dispatch_and_structured_evidence(store):
    # Dispatches each question operator and verifies structured result + evidence
    for op, args in [
        ("WHY", ("urn:svc:billing",)),
        ("WHY_NOT", ("urn:svc:auth", "urn:svc:billing")),
        ("WHAT_IF", ("urn:svc:auth",)),
        ("WHAT_CHANGED", ("urn:file:auth_py",)),
        ("WHEN", ("urn:svc:auth",)),
        ("WHO", ("urn:file:auth_py",)),
        ("WHERE", ("urn:svc:auth",)),
        ("HOW", ("urn:svc:auth",)),
    ]:
        dispatched = execute_question_operator(store, op, *args)
        assert dispatched["operator"] == op
        assert dispatched["status"] == "ok"
        assert "result" in dispatched
        assert "evidence" in dispatched
