import pytest
from datetime import datetime, timezone, timedelta
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.causal import (
    CausalHypothesis,
    find_temporal_correlations,
    check_causal_prerequisites,
    generate_hypotheses,
    review_hypothesis,
)


@pytest.fixture
def causal_store():
    store = MemoryGraphStore()
    now = datetime(2026, 10, 11, 12, 0, 0, tzinfo=timezone.utc)
    t_deploy = (now - timedelta(hours=2)).isoformat()
    t_metric = (now - timedelta(hours=1)).isoformat()
    t_incident = now.isoformat()

    # Create vertices
    dep = store.upsert_vertex("Deployment", {
        "canonical_id": "dep:v2.1",
        "name": "Deployment v2.1",
        "created_at": t_deploy,
    })
    metric = store.upsert_vertex("AlertEvent", {
        "canonical_id": "alert:latency-spike",
        "name": "Latency Spike Alert",
        "created_at": t_metric,
    })
    inc = store.upsert_vertex("Incident", {
        "canonical_id": "inc:outage-01",
        "incident_number": "INC-001",
        "summary": "Checkout Outage",
        "created_at": t_incident,
    })

    # Edges between incident, deployment, and alert
    store.upsert_edge("TRIGGERED_BY", inc["vid"], dep["vid"], {})
    store.upsert_edge("CORRELATES_WITH", inc["vid"], metric["vid"], {})
    return store


@pytest.mark.req("G2-CAUSE-002")
def test_causal_relationship_classes_and_hypotheses(causal_store):
    prereq = check_causal_prerequisites(causal_store, "dep:v2.1", "inc:outage-01")
    assert prereq["valid"] is True
    assert prereq["has_evidence"] is True
    assert prereq["confidence"] >= 0.7
    assert len(prereq["evidence_chain"]) > 0


@pytest.mark.req("G2-CAUSE-003")
def test_causal_hypotheses_no_silent_promotion_to_confirmed(causal_store):
    result = generate_hypotheses(causal_store, "inc:outage-01", time_window_hours=24.0)
    assert result["incident"] == "inc:outage-01"
    assert result["total_hypotheses"] >= 1
    for hyp in result["hypotheses"]:
        # Status must never be HUMAN_CONFIRMED_CAUSE automatically
        assert hyp["status"] in ("CORRELATION", "HYPOTHESIS")
        assert hyp["status"] != "HUMAN_CONFIRMED_CAUSE"
    assert "HUMAN_CONFIRMED_CAUSE is never emitted automatically" in result["status_note"]


@pytest.mark.req("G2-CAUSE-004")
def test_causal_hypothesis_structure_and_alternatives(causal_store):
    result = generate_hypotheses(causal_store, "inc:outage-01", time_window_hours=24.0)
    hyp = result["hypotheses"][0]
    assert "evidence" in hyp
    assert "temporal_distance_seconds" in hyp
    assert hyp["temporal_distance_seconds"] > 0
    assert "alternatives" in hyp
    assert "confidence" in hyp
    assert "status" in hyp


@pytest.mark.req("G2-CAUSE-005")
def test_temporal_correlations_and_time_ordering(causal_store):
    corrs = find_temporal_correlations(causal_store, "inc:outage-01", time_window_hours=12.0)
    assert len(corrs) >= 2
    # Check that events before the incident have direction "before"
    before_cids = [c["canonical_id"] for c in corrs if c["direction"] == "before"]
    assert "dep:v2.1" in before_cids
    assert "alert:latency-spike" in before_cids


@pytest.mark.req("G2-CAUSE-006")
def test_human_confirmation_and_rejection_preserved():
    hyp = CausalHypothesis(
        hypothesis_id="hyp-test",
        cause_cid="dep:v2.1",
        effect_cid="inc:outage-01",
        status="HYPOTHESIS",
    )
    # Confirm
    reviewed = review_hypothesis(hyp, "HUMAN_CONFIRMED_CAUSE", notes="Root cause confirmed by SRE team")
    assert reviewed.status == "HUMAN_CONFIRMED_CAUSE"
    assert reviewed.reviewer_notes == "Root cause confirmed by SRE team"

    # Reject
    rejected = review_hypothesis(hyp, "REJECTED", notes="Disproven by canary rollback")
    assert rejected.status == "REJECTED"
    assert rejected.reviewer_notes == "Disproven by canary rollback"
