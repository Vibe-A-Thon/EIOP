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


@pytest.mark.req("FR-QUERY-001", "FR-QUERY-004")
def test_search_via_executor():
    store = _loaded_store()
    executor = QueryExecutor(store)
    plan = QueryPlan(intent="SEARCH", anchors=["TEST-1"], max_depth=1, result_limit=10, evidence_mode="NONE")
    result = executor.execute(plan)
    assert result.nodes
    assert any(n.id == "urn:test:item:1" for n in result.nodes)


@pytest.mark.req("FR-QUERY-001", "FR-QUERY-002", "FR-QUERY-007")
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


@pytest.mark.req("FR-QUERY-001", "FR-QUERY-003", "FR-QUERY-007")
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


def test_search_rejects_single_character_queries():
    store = _loaded_store()
    executor = QueryExecutor(store)
    plan = QueryPlan(
        intent="SEARCH", anchors=["a"], max_depth=1, result_limit=10, evidence_mode="NONE"
    )
    with pytest.raises(PolicyViolation, match="at least 2 characters"):
        executor.execute(plan)


def test_search_prefers_indexed_exact_match_over_substring_matches():
    store = _loaded_store()
    store.upsert_vertex("Document", {
        "canonical_id": "urn:test:doc:1", "name": "aaa notes about TEST-1",
    })
    executor = QueryExecutor(store)
    plan = QueryPlan(
        intent="SEARCH", anchors=["TEST-1"], max_depth=1, result_limit=10, evidence_mode="NONE"
    )
    result = executor.execute(plan)
    assert result.nodes[0].id == "urn:test:item:1"
    assert any(node.id == "urn:test:doc:1" for node in result.nodes)


def test_search_resolves_file_by_path_lookup():
    store = _loaded_store()
    store.upsert_vertex("File", {
        "canonical_id": "urn:test:file:1", "repo_id": "demo", "path": "src/app.py",
    })
    executor = QueryExecutor(store)
    plan = QueryPlan(
        intent="SEARCH", anchors=["src/app.py"], max_depth=1, result_limit=10, evidence_mode="NONE"
    )
    result = executor.execute(plan)
    assert any(node.id == "urn:test:file:1" for node in result.nodes)


@pytest.mark.parametrize("query", ["TEST-1", "STRASSE", "urn:test:doc"])
def test_projected_search_preserves_matching_order_filters_and_full_properties(query):
    store = _loaded_store()
    store.upsert_vertex("Document", {
        "canonical_id": "urn:test:doc:1", "name": "Straße TEST-1",
        "description": "Full result properties must be hydrated",
    })
    plan = QueryPlan(
        intent="SEARCH", anchors=[query], max_depth=1, result_limit=10, evidence_mode="NONE",
    )
    expected = QueryExecutor(store).execute(plan)
    calls = []

    def project(*, properties, **kwargs):
        calls.append(kwargs)
        return [
            {**vertex, "properties": {
                key: value for key, value in vertex["properties"].items() if key in properties
            }}
            for vertex in store.find_vertices(**kwargs)
        ]

    store.find_search_candidates = project
    result = QueryExecutor(store).execute(plan)
    assert [node.model_dump() for node in result.nodes] == [
        node.model_dump() for node in expected.nodes
    ]
    assert result.partial == expected.partial
    assert calls == [{"label": None, "filters": None, "limit": 5000, "include_deleted": False}]


def test_impact_result_exposes_impact_rationale_meta():
    store = _loaded_store()
    executor = QueryExecutor(store)
    plan = QueryPlan(
        intent="IMPACT", anchors=["urn:test:item:1"], max_depth=4, result_limit=100,
        evidence_mode="SUMMARY",
    )
    result = executor.execute(plan)
    assert result.meta is not None
    assert result.meta["impact_rationale"] == {
        "urn:test:commit:abc": "1 hop(s) via IMPLEMENTS; evidence: 1 source ref(s)"
    }
