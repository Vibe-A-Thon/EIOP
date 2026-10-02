from eoip.graph.memory import MemoryGraphStore
from eoip.retrieval.service import retrieve


def test_model_unavailable_retains_independent_graph_evidence(monkeypatch):
    monkeypatch.delenv("EOIP_OLLAMA_MODEL", raising=False)
    store = MemoryGraphStore()
    issue = store.upsert_vertex(
        "WorkItem", {"canonical_id": "issue:1", "issue_key": "EOIP-1", "summary": "Trace"}
    )
    commit = store.upsert_vertex("Commit", {"canonical_id": "commit:1", "commit_sha": "abc"})
    store.upsert_edge("IMPLEMENTS", commit["vid"], issue["vid"], {"source_ref": "git://demo/abc"})
    result = retrieve(store, "issue:1", "Explain the trace", synthesize=True)
    assert result["generation"] == "deterministic"
    assert result["evidence_refs"] == ["git://demo/abc"]
    assert len(result["facts"]) == 2
    assert result["warnings"]
