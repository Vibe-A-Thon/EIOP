"""Contract tests: QueryPlan and policy validation."""

import pytest
from eoip.contracts.query_plan import QueryPlan
from eoip.query.policy import DEFAULT_POLICY, QueryPolicy


def test_valid_query_plan():
    plan = QueryPlan(
        intent="SEARCH",
        anchors=["test"],
        max_depth=4,
        result_limit=100,
        evidence_mode="SUMMARY",
    )
    violations = DEFAULT_POLICY.validate(plan)
    assert not violations


def test_policy_rejects_excessive_depth():
    plan = QueryPlan(intent="PATH", anchors=["a", "b"], max_depth=8, result_limit=100, evidence_mode="NONE")
    strict = QueryPolicy(max_depth=4)
    violations = strict.validate(plan)
    assert any("depth" in v.lower() for v in violations)


def test_policy_rejects_unknown_intent():
    policy = QueryPolicy(allowed_intents=frozenset({"SEARCH"}))
    plan = QueryPlan(intent="IMPACT", anchors=["a"], max_depth=4, result_limit=100, evidence_mode="NONE")
    violations = policy.validate(plan)
    assert any("intent" in v.lower() for v in violations)


def test_policy_rejects_empty_anchors():
    plan = QueryPlan(intent="SEARCH", anchors=[], max_depth=4, result_limit=100, evidence_mode="NONE")
    violations = DEFAULT_POLICY.validate(plan)
    assert any("anchor" in v.lower() for v in violations)


def test_policy_clamp():
    plan = QueryPlan(intent="IMPACT", anchors=["a"], max_depth=8, result_limit=500, timeout_ms=30000, evidence_mode="FULL")
    strict = QueryPolicy(max_depth=4, max_results=50, max_timeout_ms=5000)
    clamped = strict.clamp(plan)
    assert clamped.max_depth == 4
    assert clamped.result_limit == 50
    assert clamped.timeout_ms == 5000
