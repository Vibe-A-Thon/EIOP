"""Unit tests for packages/eoip/query/intelligence.py (GAP-QI-001..008)."""

import pytest

from eoip.audit.sink import AuditSink
from eoip.contracts.query_plan import QueryPlan
from eoip.graph.memory import MemoryGraphStore
from eoip.query.intelligence import QueryIntelligence, TemplateBindingError


def _plan(intent="NEIGHBORHOOD", anchors=("urn:eoip:item:WorkItem:1",), **kw):
    defaults = dict(
        intent=intent,
        anchors=list(anchors),
        max_depth=2,
        result_limit=10,
        timeout_ms=5000,
        evidence_mode="SUMMARY",
    )
    defaults.update(kw)
    return QueryPlan(**defaults)


@pytest.fixture
def store():
    s = MemoryGraphStore()
    wi = s.upsert_vertex("WorkItem", {"canonical_id": "urn:eoip:item:WorkItem:1", "issue_key": "PROJ-1", "name": "Alpha"})
    for i in range(2, 8):
        other = s.upsert_vertex("WorkItem", {"canonical_id": f"urn:eoip:item:WorkItem:{i}", "issue_key": f"PROJ-{i}", "name": f"Item {i}"})
        s.upsert_edge("REFERENCES", wi["vid"], other["vid"], {"edge_key": f"e{i}"})
    return s


@pytest.fixture
def intel(store, tmp_path):
    return QueryIntelligence(store, audit_sink=AuditSink(tmp_path))


# -- GAP-QI-001: explain -----------------------------------------------------


def test_explain_returns_steps_and_indexes(intel):
    explained = intel.explain(_plan())
    assert explained.explain_id.startswith("urn:eoip:query:explain:")
    assert explained.steps[0].operation == "anchor_lookup"
    assert explained.total_estimated_vertices > 0
    assert explained.estimated_fanout > 0
    assert explained.policy_violations == []


def test_explain_search_lists_secondary_indexes(intel):
    explained = intel.explain(_plan("SEARCH", anchors=("PROJ-1",)))
    ops = [s.operation for s in explained.steps]
    assert ops == ["exact_index_lookup", "label_scan"]
    assert any(idx.startswith("secondary.WorkItem.issue_key") for idx in explained.indexes_used)


def test_explain_reports_policy_violations(store):
    from eoip.query.policy import QueryPolicy

    intel = QueryIntelligence(store, policy=QueryPolicy(max_depth=2))
    explained = intel.explain(_plan(max_depth=4))
    assert any("depth" in v for v in explained.policy_violations)


def test_explain_traversal_risks_without_allowlist(intel):
    explained = intel.explain(_plan("IMPACT", max_depth=8))
    assert any("allowlist" in r for r in explained.traversal_risks)


# -- GAP-QI-002: cost --------------------------------------------------------


def test_cost_estimate_bounded_and_graded(intel):
    cheap = intel.cost(_plan(max_depth=1, timeout_ms=100))
    pricey = intel.cost(_plan("SEARCH", max_depth=8, timeout_ms=30000))
    assert 0.0 <= cheap.score <= 1.0
    assert cheap.grade in {"LOW", "MODERATE", "HIGH", "SEVERE"}
    assert pricey.score >= cheap.score
    assert set(cheap.breakdown) == {"depth", "volume", "scan", "timeout"}


# -- GAP-QI-003: history + audit persistence ---------------------------------


def test_execute_records_history_and_audits(intel):
    result = intel.execute(_plan())
    assert result.nodes, "neighborhood should return anchor vertex"
    assert len(intel.history) == 1
    entry = intel.history[0]
    assert entry.query_id == result.query_id
    assert entry.intent == "NEIGHBORHOOD"
    assert entry.result_nodes >= 1
    assert entry.latency_ms >= 0
    events = intel._audit.read()
    assert len(events) == 1
    assert events[0]["event_type"] == "query.executed"
    assert events[0]["plan"]["estimated_cost"] == entry.cost_score


def test_history_is_bounded_ring_buffer(store):
    intel = QueryIntelligence(store, history_capacity=3)
    for _ in range(5):
        intel.execute(_plan())
    assert len(intel.history) == 3


def test_history_without_audit_sink(store):
    intel = QueryIntelligence(store)
    intel.execute(_plan())
    assert len(intel.history) == 1


# -- GAP-QI-004/005: slow-query analyzer --------------------------------------


def test_slow_query_report_with_suggestions(intel):
    from eoip.query.intelligence import QueryHistoryEntry

    intel.execute(_plan())
    intel._history.append(
        QueryHistoryEntry(
            history_id="urn:eoip:query:h:slow",
            query_id="q-slow",
            intent="SEARCH",
            anchors=["term"],
            latency_ms=2500.0,
            result_nodes=3,
            result_edges=0,
            partial=False,
            cost_score=0.5,
            explain_id="urn:eoip:query:explain:x",
        )
    )
    report = intel.slow_queries(threshold_ms=1000.0, top_n=5)
    assert report.slow_count == 1
    assert report.top[0].history_id == "urn:eoip:query:h:slow"
    assert any("secondary index" in s for s in report.suggestions)


def test_slow_query_report_empty(intel):
    intel.execute(_plan())
    report = intel.slow_queries(threshold_ms=10**9)
    assert report.slow_count == 0
    assert report.top == []
    assert report.suggestions


# -- GAP-QI-007/008: templates -------------------------------------------------


def test_template_crud(intel):
    t = intel.save_template("wi-by-key", "SEARCH", ["issue_key"], description="Find work item")
    assert t.template_id.startswith("urn:eoip:query:template:")
    assert intel.get_template(t.template_id).name == "wi-by-key"
    assert [x.template_id for x in intel.list_templates()] == [t.template_id]
    assert intel.delete_template(t.template_id) is True
    assert intel.delete_template(t.template_id) is False


def test_template_binding_builds_plan(intel):
    t = intel.save_template("impact", "IMPACT", ["anchor"], max_depth=2, result_limit=5)
    plan = intel.bind_template(t, {"anchor": "urn:eoip:item:WorkItem:1"})
    assert plan.anchors == ["urn:eoip:item:WorkItem:1"]
    assert plan.intent == "IMPACT"
    assert plan.result_limit == 5


def test_template_binding_rejects_mismatched_params(intel):
    t = intel.save_template("impact", "IMPACT", ["anchor"])
    with pytest.raises(TemplateBindingError):
        intel.bind_template(t, {})
    with pytest.raises(TemplateBindingError):
        intel.bind_template(t, {"anchor": "x", "extra": "y"})


def test_template_binding_rejects_injection_and_bad_types(intel):
    t = intel.save_template("impact", "IMPACT", ["anchor"])
    with pytest.raises(TemplateBindingError):
        intel.bind_template(t, {"anchor": "a}b{c"})
    with pytest.raises(TemplateBindingError):
        intel.bind_template(t, {"anchor": ""})
    with pytest.raises(TemplateBindingError):
        intel.bind_template(t, {"anchor": 42})


def test_save_template_rejects_policy_violating_shape(intel):
    with pytest.raises(TemplateBindingError):
        intel.save_template("bad", "NOT_AN_INTENT", ["a"])


def test_template_end_to_end_execution(intel):
    t = intel.save_template("nbr", "NEIGHBORHOOD", ["anchor"])
    plan = intel.bind_template(t, {"anchor": "urn:eoip:item:WorkItem:1"})
    result = intel.execute(plan)
    assert result.query_id
    assert len(intel.history) == 1
