"""GAP-RET / GAP-SEARCH: keyword, vector and hybrid retrieval strategies."""

import time

from eoip.graph.memory import MemoryGraphStore
from eoip.retrieval.service import (
    RetrievalStrategy,
    retrieve,
    search_hybrid,
    search_keyword,
    search_vector,
)
from eoip.retrieval.vectors import (
    HashingEmbedder,
    InMemorySearchIndex,
    KeywordIndex,
    VectorIndex,
    build_search_index,
    cosine_similarity,
)


def _store() -> MemoryGraphStore:
    store = MemoryGraphStore()
    store.upsert_vertex(
        "WorkItem",
        {
            "canonical_id": "urn:eoip:work:1",
            "issue_key": "EOIP-1",
            "summary": "Payment reconciliation pipeline timeout",
            "description": "The nightly batch job times out reconciling payments.",
            "confidence": 0.9,
            "updated_at": time.time(),
        },
    )
    store.upsert_vertex(
        "WorkItem",
        {
            "canonical_id": "urn:eoip:work:2",
            "issue_key": "EOIP-2",
            "summary": "Dashboard rendering glitch",
            "description": "Charts flicker under load.",
            "confidence": 0.2,
            "updated_at": time.time() - 400 * 86400,
        },
    )
    store.upsert_vertex(
        "Document",
        {
            "canonical_id": "urn:eoip:doc:1",
            "name": "Payments runbook",
            "description": "Operational runbook for the payment reconciliation service.",
        },
    )
    return store


# -- keyword index -----------------------------------------------------------


def test_keyword_index_bm25_ranks_relevant_document_first():
    index = KeywordIndex()
    index.add("a", "payment reconciliation pipeline timeout nightly batch")
    index.add("b", "dashboard rendering chart glitch")
    index.add("c", "payment button styling glitch")
    hits = index.search("payment reconciliation timeout", top_k=5)
    assert [h[0] for h in hits] == ["a", "c"]
    assert hits[0][1] > hits[1][1]


def test_keyword_index_remove():
    index = KeywordIndex()
    index.add("a", "payment timeout")
    index.remove("a")
    assert index.search("payment") == []


def test_build_search_index_uses_canonical_ids():
    store = _store()
    index = build_search_index(store)
    ids = index.entity_ids()
    assert "urn:eoip:work:1" in ids
    assert "urn:eoip:doc:1" in ids


# -- vector index ------------------------------------------------------------


def test_hashing_embedder_is_deterministic_and_normalized():
    embedder = HashingEmbedder(dimensions=64)
    a = embedder.embed("payment reconciliation")
    b = embedder.embed("payment reconciliation")
    assert a == b
    assert abs(sum(x * x for x in a) - 1.0) < 1e-9


def test_vector_search_semantic_overlap_beats_disjoint():
    index = VectorIndex()
    index.add("a", "payment reconciliation pipeline timeout")
    index.add("b", "dashboard rendering chart glitch")
    hits = index.vector_search("payment pipeline reconciliation", top_k=5)
    assert hits[0][0] == "a"


def test_cosine_similarity_identical_text_is_one():
    embedder = HashingEmbedder(dimensions=32)
    vec = embedder.embed("same text")
    assert cosine_similarity(vec, vec) > 0.999


# -- strategies ---------------------------------------------------------------


def test_search_keyword_returns_trace_and_graph_identity():
    store = _store()
    result = search_keyword(store, "payment reconciliation")
    assert result.strategy == "keyword"
    assert result.trace and [s["stage"] for s in result.trace["steps"]] == [
        "keyword",
        "ranked",
    ]
    assert result.evidence_refs[0] == "urn:eoip:work:1"
    assert all(f["canonical_id"].startswith("urn:eoip:") for f in result.facts)


def test_search_vector_routes_to_deterministic_embeddings():
    store = _store()
    result = search_vector(store, "payment reconciliation")
    assert result.strategy == "vector"
    assert result.evidence_refs[0] in {"urn:eoip:work:1", "urn:eoip:doc:1"}
    assert result.generation == "deterministic"


def test_retrieve_accepts_explicit_strategy():
    store = _store()
    result = retrieve(store, "", "payment reconciliation", strategy="keyword")
    assert result.strategy == "keyword"
    result = retrieve(store, "", "payment", strategy=RetrievalStrategy.VECTOR)
    assert result.strategy == "vector"


def test_hybrid_fuses_keyword_vector_and_graph_with_trace():
    store = _store()
    issue = store.get_vertex_by_canonical_id("urn:eoip:work:1")
    doc = store.get_vertex_by_canonical_id("urn:eoip:doc:1")
    store.upsert_edge("DOCUMENTS", doc["vid"], issue["vid"], {"source_ref": "conf://runbook"})

    result = search_hybrid(
        store,
        "payment reconciliation runbook",
        canonical_id="urn:eoip:work:1",
        top_k=5,
    )
    assert result.strategy == "hybrid"
    stages = [s["stage"] for s in result.trace["steps"]]
    assert stages == ["keyword", "vector", "graph", "ranked"]
    ids = {c.ref for c in result.contexts if c.kind == "entity"}
    # graph neighbor fused with keyword/vector candidates
    assert "urn:eoip:doc:1" in ids


def test_hybrid_quality_recency_authority_boosts_better_evidence():
    store = _store()
    result = search_hybrid(store, "payment timeout", top_k=5)
    scores = {f["canonical_id"]: f["score"] for f in result.facts}
    assert scores["urn:eoip:work:1"] > scores["urn:eoip:work:2"]


def test_hybrid_falls_back_to_keyword_seed_without_canonical_id():
    store = _store()
    result = search_hybrid(store, "payment reconciliation", top_k=5)
    assert result.strategy == "hybrid"
    assert result.facts[0]["canonical_id"] == "urn:eoip:work:1"


def test_search_index_is_replaceable():
    class CountingIndex(InMemorySearchIndex):
        def __init__(self):
            super().__init__()
            self.keyword_calls = 0

        def keyword_search(self, query, top_k=10):
            self.keyword_calls += 1
            return super().keyword_search(query, top_k)

    store = _store()
    index = CountingIndex()
    build_search_index(store, index)
    result = search_keyword(store, "payment", search_index=index)
    assert result.strategy == "keyword"
    assert index.keyword_calls == 1
