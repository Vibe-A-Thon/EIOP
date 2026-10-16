from __future__ import annotations

import json
from pathlib import Path

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.retrieval.service import retrieve, search_keyword
from jsonschema import validate


def _store_with_traceable_answer() -> tuple[MemoryGraphStore, str]:
    store = MemoryGraphStore()
    issue = store.upsert_vertex(
        "WorkItem",
        {
            "canonical_id": "urn:work:PROJ-101",
            "issue_key": "PROJ-101",
            "summary": "Checkout latency regression",
            "source_ref": "jira://PROJ-101",
            "captured_at": "2026-10-12T00:00:00+00:00",
        },
    )
    commit = store.upsert_vertex(
        "Commit",
        {
            "canonical_id": "urn:commit:abc123",
            "commit_sha": "abc123",
            "message": "Reduce checkout latency by caching inventory lookups",
            "source_ref": "git://payments/commit/abc123",
            "captured_at": "2026-10-12T00:05:00+00:00",
        },
    )
    evidence = store.upsert_vertex(
        "Evidence",
        {
            "canonical_id": "urn:evidence:jira:PROJ-101",
            "source_system": "jira",
            "source_ref": "jira://PROJ-101",
            "source_id": "PROJ-101",
            "evidence_key": "jira-event-PROJ-101",
            "content_hash": "sha256:project101",
        },
    )
    store.upsert_edge(
        "EVIDENCED_BY",
        issue["vid"],
        evidence["vid"],
        {
            "fact_key": "issue-source",
            "source_ref": "jira://PROJ-101",
            "evidence_key": "jira-event-PROJ-101",
            "source_system": "jira",
        },
    )
    edge = store.upsert_edge(
        "IMPLEMENTS",
        commit["vid"],
        issue["vid"],
        {
            "fact_key": "commit-implements-issue",
            "source_ref": "git://payments/commit/abc123",
            "evidence_key": "git-event-abc123",
            "source_system": "git",
        },
    )
    return store, edge["eid"]


@pytest.mark.req("GAP-AI")
def test_graph_rag_answer_is_addressable_to_nodes_paths_and_source_records() -> None:
    store, edge_id = _store_with_traceable_answer()

    result = retrieve(store, "urn:work:PROJ-101", "Which change fixed checkout latency?")

    manifest = result.evidence_manifest
    assert manifest["answer_id"] == result.retrieval_id
    assert "urn:work:PROJ-101" in manifest["node_refs"]
    assert "urn:commit:abc123" in manifest["node_refs"]
    assert edge_id in manifest["edge_refs"]
    assert "jira://PROJ-101" in manifest["source_refs"]
    assert "git://payments/commit/abc123" in manifest["source_refs"]
    assert "urn:evidence:jira:PROJ-101" in manifest["evidence_refs"]
    assert "git-event-abc123" in manifest["evidence_refs"]
    assert manifest["query_plan"]["strategy"] == result.strategy

    path_chains = [chain for chain in result.citation_chains if edge_id in chain["path"]["edge_ids"]]
    assert path_chains
    assert path_chains[0]["path"]["node_ids"] == ["urn:work:PROJ-101", "urn:commit:abc123"]
    assert "git://payments/commit/abc123" in path_chains[0]["source_refs"]


@pytest.mark.req("GAP-AI")
def test_ranked_retrieval_answers_also_emit_evidence_manifest() -> None:
    store, _edge_id = _store_with_traceable_answer()

    result = search_keyword(store, "checkout latency")

    assert result.evidence_manifest["answer_id"] == result.retrieval_id
    assert result.evidence_manifest["node_refs"]
    assert result.citation_chains
    assert any(chain["node_ref"] == result.evidence_manifest["node_refs"][0] for chain in result.citation_chains)


@pytest.mark.req("GAP-AI")
def test_retrieval_result_schema_accepts_evidence_address_fields() -> None:
    store, _edge_id = _store_with_traceable_answer()
    result = retrieve(store, "urn:work:PROJ-101", "trace the fix")
    schema = json.loads((Path(__file__).resolve().parents[2] / "schemas" / "retrieval_result.schema.json").read_text())

    validate(result.model_dump(), schema)
