"""Tests for the QueryPlan executor and policy enforcement."""

import pytest
from eoip.contracts.query_plan import QueryPlan
from eoip.graph.memory import MemoryGraphStore
from eoip.query.executor import PolicyViolation, QueryExecutor
from eoip.query.policy import QueryPolicy


def _loaded_store():
    store = MemoryGraphStore()
    wi = store.upsert_vertex("WorkItem", {
        "canonical_id": "urn:test:item:1", "issue_key": "TEST-1", "summary": "Test work item",
    })
    commit = store.upsert_vertex("Commit", {
        "canonical_id": "urn:test:commit:abc", "commit_sha": "abc123",
    })
    store.upsert_edge("IMPLEMENTS", commit["vid"], wi["vid"], {
        "fact_key": "test-impl", "creation_status": "DETERMINISTIC",
        "source_ref": "git://abc123", "evidence_key": "ev1",
    })
    return store


def test_search_via_executor():
    store = _loaded_store()
    executor = QueryExecutor(store)
    plan = QueryPlan(intent="SEARCH", anchors=["TEST-1"], max_depth=1, result_limit=10, evidence_mode="NONE")
    result = executor.execute(plan)
    assert result.nodes
    assert any(n.id == "urn:test:item:1" for n in result.nodes)


def test_path_via_executor():
    store = _loaded_store()
    executor = QueryExecutor(store)
    plan = QueryPlan(
        intent="PATH",
        anchors=["urn:test:item:1", "urn:test:commit:abc"],
        max_depth=4, result_limit=100, evidence_mode="FULL",
    )
    result = executor.execute(plan)
    assert result.paths


def test_impact_via_executor():
    store = _loaded_store()
    executor = QueryExecutor(store)
    plan = QueryPlan(intent="IMPACT", anchors=["urn:test:item:1"], max_depth=4, result_limit=100, evidence_mode="SUMMARY")
    result = executor.execute(plan)
    assert result.nodes


def test_policy_violation_raised():
    store = _loaded_store()
    policy = QueryPolicy(max_depth=2)
    executor = QueryExecutor(store, policy=policy)
    plan = QueryPlan(intent="IMPACT", anchors=["urn:test:item:1"], max_depth=4, result_limit=100, evidence_mode="NONE")
    with pytest.raises(PolicyViolation) as exc_info:
        executor.execute(plan)
    assert exc_info.value.violations
