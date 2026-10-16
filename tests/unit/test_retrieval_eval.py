"""Tests for the deterministic RAG evaluation harness (FR-RAG-005)."""

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.retrieval.eval import EvalCase, run_eval


def _store() -> MemoryGraphStore:
    store = MemoryGraphStore()
    issue = store.upsert_vertex(
        "WorkItem",
        {
            "canonical_id": "urn:demo:work:item:EOIP-1",
            "issue_key": "EOIP-1",
            "summary": "Trace a requirement to its implementation",
        },
    )
    commit = store.upsert_vertex(
        "Commit",
        {
            "canonical_id": "urn:demo:code:commit:abc123",
            "commit_sha": "abc123",
            "message": "Implement EOIP-1",
        },
    )
    evidence = store.upsert_vertex(
        "Evidence",
        {
            "canonical_id": "urn:demo:evidence:1",
            "source_system": "git",
            "source_ref": "git://demo/commit/abc123",
            "method": "SOURCE_EVENT",
            },
    )
    store.upsert_edge(
        "IMPLEMENTS",
        commit["vid"],
        issue["vid"],
        {"fact_key": "impl-1", "source_ref": "git://demo/commit/abc123"},
    )
    store.upsert_edge(
        "EVIDENCED_BY",
        issue["vid"],
        evidence["vid"],
        {"source_ref": "git://demo/commit/abc123"},
    )
    return store


def test_passing_case_scores_full_recall():
    results = run_eval(
        _store(),
        [
            EvalCase(
                id="trace",
                question="Trace EOIP-1 to its implementation",
                canonical_id="urn:demo:work:item:EOIP-1",
                expected_facts=[
                    "urn:demo:work:item:EOIP-1",
                    "urn:demo:code:commit:abc123",
                ],
            )
        ],
    )
    assert len(results) == 1
    result = results[0]
    assert result.passed
    assert result.facts_recall == 1.0
    assert result.facts_precision == 1.0
    assert result.evidence_coverage == 1.0
    assert result.grounded
    assert result.strategy_used == "code_context"
    assert result.latency_ms >= 0


def test_missing_expected_fact_fails_recall():
    results = run_eval(
        _store(),
        [
            EvalCase(
                id="miss",
                question="What implements EOIP-1?",
                canonical_id="urn:demo:work:item:EOIP-1",
                expected_facts=["urn:demo:work:item:EOIP-1", "urn:demo:code:symbol:missing"],
            )
        ],
    )
    result = results[0]
    assert not result.passed
    assert result.facts_recall == 0.5
    assert "matched 1/2" in result.detail


def test_not_found_case_records_failure_instead_of_raising():
    store = _store()
    with pytest.raises(ValueError, match="not found"):
        from eoip.retrieval.service import retrieve

        retrieve(store, "urn:demo:work:item:NOPE-9", "What blocks NOPE-9?")
    results = run_eval(
        store,
        [
            EvalCase(
                id="insufficient",
                question="What blocks NOPE-9?",
                canonical_id="urn:demo:work:item:NOPE-9",
                expected_facts=[],
                expected_evidence_min=0,
            )
        ],
    )
    result = results[0]
    assert result.case_id == "insufficient"
    assert not result.passed
    assert result.strategy_used == "none"
    assert result.facts_recall == 0.0
    assert "not found" in result.detail
