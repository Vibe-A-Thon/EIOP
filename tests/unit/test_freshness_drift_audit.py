import json
import pytest

from eoip.graph.expertise import (
    detect_contradictions,
    detect_deprecated_references,
    detect_ownership_drift,
    recommend_document_reviews,
)
from eoip.graph.memory import MemoryGraphStore


@pytest.fixture
def graph():
    store = MemoryGraphStore()
    store.ensure_schema({})

    # Persons
    p_alice = store.upsert_vertex("Person", {"canonical_id": "urn:person:alice", "display_name": "Alice Developer"})
    p_bob = store.upsert_vertex("Person", {"canonical_id": "urn:person:bob", "display_name": "Bob Architect"})

    # Services
    s_orders = store.upsert_vertex("Service", {
        "canonical_id": "urn:service:orders",
        "service_id": "orders",
        "name": "Orders Service",
        "status": "ACTIVE",
        "criticality": "TIER_1",
        "owner": "Bob Architect",
    })

    s_legacy = store.upsert_vertex("Service", {
        "canonical_id": "urn:service:legacy-auth",
        "service_id": "legacy-auth",
        "name": "Legacy Auth",
        "status": "DEPRECATED",
    })

    # Documents
    # Doc 1: Claims criticality is TIER_3 (contradicting TIER_1) and states owner is Alice (drifting from Bob)
    doc_orders = store.upsert_vertex("Document", {
        "canonical_id": "urn:doc:orders-guide",
        "name": "Orders Deployment Guide",
        "path": "docs/orders.md",
        "owner": "Alice Developer",
        "payload_json": json.dumps({"claims": {"criticality": "TIER_3"}}),
    })

    # Doc 2: References deprecated service
    doc_auth = store.upsert_vertex("Document", {
        "canonical_id": "urn:doc:auth-guide",
        "name": "Authentication Integration",
        "path": "docs/auth.md",
        "payload_json": json.dumps({"claims": {"status": "ACTIVE"}}),
    })

    # Edges
    store.upsert_edge("DOCUMENTS", doc_orders["vid"], s_orders["vid"], {})
    store.upsert_edge("DOCUMENTS", doc_auth["vid"], s_legacy["vid"], {})

    return store


@pytest.mark.req("GAP-FRESH-002")
def test_detect_docs_contradicted_by_code_config_runtime(graph):
    # doc_orders claims criticality TIER_3, but service has TIER_1
    contradictions = detect_contradictions(graph, document_cid="urn:doc:orders-guide")
    assert len(contradictions) >= 1
    c = contradictions[0]
    assert c["field"] == "criticality"
    assert c["doc_claimed"] == "TIER_3"
    assert c["actual_state"] == "TIER_1"
    assert c["contradiction_type"] == "config_contradiction"

    # doc_auth claims status ACTIVE, but legacy-auth has status DEPRECATED
    auth_contradictions = detect_contradictions(graph, document_cid="urn:doc:auth-guide")
    assert any(ac["field"] == "status" and ac["actual_state"] == "DEPRECATED" for ac in auth_contradictions)


@pytest.mark.req("GAP-FRESH-003")
def test_detect_ownership_changes(graph):
    drifts = detect_ownership_drift(graph, document_cid="urn:doc:orders-guide")
    assert len(drifts) == 1
    d = drifts[0]
    assert d["document_stated_owner"] == "Alice Developer"
    assert d["current_owner"] == "Bob Architect"
    assert d["drift_detected"] is True
    assert "owner of urn:service:orders" in d["evidence"]


@pytest.mark.req("GAP-FRESH-004")
def test_detect_deprecated_apis_still_referenced_in_docs(graph):
    deprecated = detect_deprecated_references(graph, document_cid="urn:doc:auth-guide")
    assert len(deprecated) == 1
    dep = deprecated[0]
    assert dep["api_cid"] == "urn:service:legacy-auth"
    assert dep["status"] == "DEPRECATED"
    assert "marked deprecated" in dep["evidence"]


@pytest.mark.req("GAP-FRESH-005")
def test_recommend_review_not_silently_rewrite_authoritative_docs(graph):
    reviews = recommend_document_reviews(graph)
    assert len(reviews) >= 2

    for r in reviews:
        # Governance constraint: silent rewrite is strictly disallowed
        assert r["silent_rewrite_permitted"] is False
        assert r["action"] == "HUMAN_REVIEW_RECOMMENDED"
        assert "Authoritative documentation must NOT be silently rewritten by AI" in r["governance_note"]
        assert len(r["reasons"]) > 0

    orders_rev = next(r for r in reviews if r["document_cid"] == "urn:doc:orders-guide")
    assert "config_contradiction" in [c["contradiction_type"] for c in orders_rev["findings"]["contradictions"]]
    assert orders_rev["findings"]["ownership_drift"][0]["current_owner"] == "Bob Architect"
