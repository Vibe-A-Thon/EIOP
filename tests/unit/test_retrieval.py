import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.retrieval.service import RetrievalStrategy, retrieve, select_strategy


@pytest.mark.req("FR-RAG-003", "FR-RAG-004")
def test_model_unavailable_retains_independent_graph_evidence(monkeypatch):
    monkeypatch.delenv("EOIP_OLLAMA_MODEL", raising=False)
    store = MemoryGraphStore()
    issue = store.upsert_vertex(
        "WorkItem", {"canonical_id": "issue:1", "issue_key": "EOIP-1", "summary": "Trace"}
    )
    commit = store.upsert_vertex("Commit", {"canonical_id": "commit:1", "commit_sha": "abc"})
    store.upsert_edge("IMPLEMENTS", commit["vid"], issue["vid"], {"source_ref": "git://demo/abc"})
    result = retrieve(store, "issue:1", "Explain the trace", synthesize=True)
    assert result.strategy == "direct_graph"
    assert result.generation == "deterministic"
    assert result.evidence_refs == ["git://demo/abc"]
    assert len(result.facts) == 2
    assert result.warnings


@pytest.mark.req("FR-RAG-001")
def test_retrieval_router_selects_code_context_for_code_question():
    store = MemoryGraphStore()
    store.upsert_vertex(
        "CodeSymbol",
        {
            "canonical_id": "sym:1",
            "qualified_name": "svc.run",
            "symbol_kind": "function",
        },
    )
    assert (
        select_strategy("sym:1", "how is this function implemented", store)
        == RetrievalStrategy.CODE_CONTEXT
    )
    assert select_strategy("sym:1", "what depends on this", store) == RetrievalStrategy.CODE_CONTEXT
    store.upsert_vertex(
        "WorkItem", {"canonical_id": "issue:1", "issue_key": "EOIP-1", "summary": "Trace"}
    )
    assert (
        select_strategy("issue:1", "what depends on this", store)
        == RetrievalStrategy.DIRECT_GRAPH
    )


@pytest.mark.req("FR-RAG-002", "MVP-FR-020")
def test_code_context_preserves_relationship_evidence():
    store = MemoryGraphStore()
    source = store.upsert_vertex(
        "CodeSymbol",
        {
            "canonical_id": "sym:source",
            "qualified_name": "svc.source",
            "symbol_kind": "function",
        },
    )
    target = store.upsert_vertex(
        "CodeSymbol",
        {
            "canonical_id": "sym:target",
            "qualified_name": "svc.target",
            "symbol_kind": "function",
        },
    )
    store.upsert_edge(
        "CALLS",
        source["vid"],
        target["vid"],
        {"source_ref": "file://service.py#L10", "evidence_key": "call:10"},
    )

    result = retrieve(store, "sym:source", "How is this code implemented?")

    relationships = [context for context in result.contexts if context.kind == "relationship"]
    assert len(relationships) == 1
    assert relationships[0].citations == ["file://service.py#L10", "call:10"]


def test_retrieval_returns_empty_result_without_canonical_id():
    store = MemoryGraphStore()
    result = retrieve(store, "", "question")
    assert result.strategy == "none"
    assert result.contexts == []
