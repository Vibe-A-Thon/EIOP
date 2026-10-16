"""Query policy enforcement tests (FR-QUERY-006, FR-QUERY-008)."""

from eoip.contracts.query_plan import QueryPlan
from eoip.query.policy import DEFAULT_POLICY, QueryPolicy


def _plan(**overrides) -> QueryPlan:
    data = {
        "intent": "IMPACT",
        "anchors": ["urn:test:item:1"],
        "max_depth": 4,
        "result_limit": 100,
        "evidence_mode": "SUMMARY",
    }
    data.update(overrides)
    return QueryPlan(**data)


def test_default_policy_allows_standard_intents() -> None:
    for intent in ("SEARCH", "PATH", "IMPACT", "NEIGHBORHOOD", "LINEAGE", "TRACEABILITY"):
        assert DEFAULT_POLICY.validate(_plan(intent=intent)) == []


def test_unknown_intent_is_rejected() -> None:
    plan = _plan().model_copy(update={"intent": "DELETE"})

    violations = DEFAULT_POLICY.validate(plan)

    assert any("not permitted" in violation for violation in violations)


def test_depth_result_and_timeout_bounds_are_enforced() -> None:
    policy = QueryPolicy(max_depth=2, max_results=10, max_timeout_ms=1000)

    violations = policy.validate(_plan(max_depth=4, result_limit=100, timeout_ms=5000))

    assert any("depth" in violation for violation in violations)
    assert any("result limit" in violation for violation in violations)
    assert any("timeout" in violation for violation in violations)


def test_clamp_reduces_plan_to_policy_bounds() -> None:
    policy = QueryPolicy(max_depth=2, max_results=10, max_timeout_ms=1000)

    clamped = policy.clamp(_plan(max_depth=8, result_limit=500, timeout_ms=30000))

    assert clamped.max_depth == 2
    assert clamped.result_limit == 10
    assert clamped.timeout_ms == 1000


def test_unknown_and_blocked_relationships_are_rejected() -> None:
    policy = QueryPolicy(blocked_edges=frozenset({"CALLS"}))

    violations = policy.validate(_plan(relationship_allowlist=["CALLS", "NOT_A_EDGE"]))

    assert any("Unknown relationship" in violation for violation in violations)
    assert any("Blocked relationship" in violation for violation in violations)


def test_missing_anchor_is_rejected() -> None:
    violations = DEFAULT_POLICY.validate(_plan(anchors=[]))

    assert any("anchor" in violation for violation in violations)
