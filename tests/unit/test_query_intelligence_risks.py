import pytest

from eoip.contracts.query_plan import QueryPlan
from eoip.graph.memory import MemoryGraphStore
from eoip.query.intelligence import QueryHistoryEntry, QueryIntelligence


@pytest.fixture
def store():
    s = MemoryGraphStore()
    wi = s.upsert_vertex("WorkItem", {"canonical_id": "urn:item:1", "issue_key": "PROJ-1", "name": "Item 1"})
    for i in range(2, 6):
        target = s.upsert_vertex("WorkItem", {"canonical_id": f"urn:item:{i}", "issue_key": f"PROJ-{i}", "name": f"Item {i}"})
        s.upsert_edge("REFERENCES", wi["vid"], target["vid"], {"edge_key": f"e:{i}"})
    return s


@pytest.fixture
def intel(store):
    return QueryIntelligence(store)


@pytest.mark.req("GAP-QI-005")
def test_suggested_indexes(intel):
    # Analyze query history with slow search
    history = [
        QueryHistoryEntry(
            history_id="urn:h:1",
            query_id="q1",
            intent="SEARCH",
            anchors=["unindexed_term"],
            latency_ms=1200.0,
            result_nodes=1,
            result_edges=0,
            partial=False,
            cost_score=0.7,
            explain_id="urn:exp:1",
        )
    ]
    suggestions = intel.suggest_indexes(history)
    assert len(suggestions) > 0
    assert any(s["label"] == "WorkItem" and s["property"] == "issue_key" for s in suggestions)
    assert suggestions[0]["index_type"] == "SECONDARY_EXACT"
    assert "Reduces SEARCH candidate scan" in suggestions[0]["reason"]


@pytest.mark.req("GAP-QI-006")
def test_traversal_risk_detector(intel):
    # Deep impact traversal without allowlist
    high_risk_plan = QueryPlan(
        intent="IMPACT",
        anchors=["urn:item:1"],
        max_depth=8,  # policy limit
        result_limit=500,
        timeout_ms=15000,
        evidence_mode="SUMMARY",
    )
    risks = intel.detect_traversal_risks(high_risk_plan)
    assert len(risks) >= 1
    assert any("allowlist" in r for r in risks)
    assert any("Traversal depth" in r for r in risks)


@pytest.mark.req("GAP-QI-008")
def test_nlq_produces_editable_plan_when_risk_is_high(intel):
    # High risk query plan: deep traversal without allowlist
    high_risk_plan = QueryPlan(
        intent="IMPACT",
        anchors=["urn:item:1"],
        max_depth=8,
        result_limit=500,
        timeout_ms=15000,
        evidence_mode="SUMMARY",
    )
    guard_res = intel.plan_with_risk_guard(high_risk_plan)
    assert guard_res["requires_confirmation"] is True
    assert guard_res["risk_level"] in {"HIGH", "SEVERE"}
    assert "editable_plan" in guard_res
    assert guard_res["editable_plan"]["max_depth"] == 8
    assert len(guard_res["traversal_risks"]) > 0

    # Low risk query plan: shallow bounded neighborhood
    low_risk_plan = QueryPlan(
        intent="NEIGHBORHOOD",
        anchors=["urn:item:1"],
        max_depth=1,
        result_limit=10,
        timeout_ms=1000,
        evidence_mode="SUMMARY",
    )
    low_guard = intel.plan_with_risk_guard(low_risk_plan)
    assert low_guard["requires_confirmation"] is False
    assert low_guard["risk_level"] in {"LOW", "MODERATE"}
    assert "plan" in low_guard
