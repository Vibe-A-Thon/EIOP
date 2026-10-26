"""CRA-025.5 search evaluation and CRA-025.6 RRF fusion: oracle tests with hand-computed values.

Vectors and texts are constructed so dense and BM25 rankings are known in advance; expected RRF
scores, recall and graded nDCG are computed here by hand, independently of the implementation. The
live test runs the harness on the real CPU embedding model (llm-cpu-reference job).
"""
from __future__ import annotations

import math
import os

import pytest

from eoip.retrieval.hybrid_vector_service import (IndexFamily, IndexMetadata, SearchEvaluationHarness,
                                                  TenantVectorIndex, VectorDocument)

pytestmark = pytest.mark.req("CRA-025")


def _index(dim: int, model: str = "m") -> TenantVectorIndex:
    return TenantVectorIndex(IndexMetadata(index_id="i", scope="t", family=IndexFamily.TEXT, source_revision="1",
                                           ontology_revision="1", policy_revision="1", provider="p", model=model,
                                           tokenizer="tok", dimension=dim))


def _e(i: int, dim: int = 6) -> list[float]:
    v = [0.0] * dim
    v[i] = 1.0
    return v


# ------------------------------------------------------------------ CRA-025.6 RRF
def test_rrf_scores_match_hand_computed_formula_and_order():
    idx = _index(3)
    # dense ranking for q=(1,0.5,0): a(cos .894) > b(cos .447)... c orthogonal-ish
    idx.add_document(VectorDocument("a", "alpha", [1.0, 0.0, 0.0], IndexFamily.TEXT))
    idx.add_document(VectorDocument("b", "pod crash pod", [0.0, 1.0, 0.0], IndexFamily.TEXT))
    idx.add_document(VectorDocument("c", "pod", [0.0, 0.0, 1.0], IndexFamily.TEXT))
    res = idx.hybrid_search(query_text="pod crash", query_vector=[1.0, 0.5, 0.0], query_family=IndexFamily.TEXT,
                            caller_roles=["public"], top_k=3, rrf_k=60, use_graph_centrality=False)
    # dense: a(1) b(2) c(3);  bm25: b(1) c(2); a absent
    expected = {"a": 1 / 61, "b": 1 / 62 + 1 / 61, "c": 1 / 63 + 1 / 62}
    got = {r["doc_id"]: r["final_score"] for r in res}
    assert [r["doc_id"] for r in res] == sorted(expected, key=lambda k: -expected[k]) == ["b", "c", "a"]
    assert all(math.isclose(got[k], round(v, 6), abs_tol=1e-6) for k, v in expected.items())


def test_rrf_k_and_graph_centrality_signal_are_applied_exactly():
    idx = _index(2)
    idx.add_document(VectorDocument("x", "kafka", [1.0, 0.0], IndexFamily.TEXT, graph_centrality=0.0))
    idx.add_document(VectorDocument("y", "other", [0.0, 1.0], IndexFamily.TEXT, graph_centrality=1.0))
    plain = idx.hybrid_search(query_text="kafka", query_vector=[1.0, 0.0], query_family=IndexFamily.TEXT,
                              caller_roles=["public"], top_k=2, rrf_k=10, use_graph_centrality=False)
    assert {r["doc_id"]: r["final_score"] for r in plain} == {"x": round(1 / 11 + 1 / 11, 6), "y": round(1 / 12, 6)}
    boosted = idx.hybrid_search(query_text="kafka", query_vector=[1.0, 0.0], query_family=IndexFamily.TEXT,
                                caller_roles=["public"], top_k=2, rrf_k=10, use_graph_centrality=True)
    assert {r["doc_id"]: r["final_score"] for r in boosted}["y"] == round(1 / 12 + 0.05, 6)


def test_cache_key_distinguishes_top_k_and_vector():
    idx = _index(2)
    for i, v in enumerate(([1.0, 0.0], [0.0, 1.0], [0.7, 0.7])):
        idx.add_document(VectorDocument(f"d{i}", "same text", v, IndexFamily.TEXT))
    one = idx.hybrid_search(query_text="q", query_vector=[1.0, 0.0], query_family=IndexFamily.TEXT,
                            caller_roles=["public"], top_k=1)
    three = idx.hybrid_search(query_text="q", query_vector=[1.0, 0.0], query_family=IndexFamily.TEXT,
                              caller_roles=["public"], top_k=3)
    other = idx.hybrid_search(query_text="q", query_vector=[0.0, 1.0], query_family=IndexFamily.TEXT,
                              caller_roles=["public"], top_k=1)
    assert len(one) == 1 and len(three) == 3 and one[0]["doc_id"] == "d0" and other[0]["doc_id"] == "d1"


# ------------------------------------------------------------------ CRA-025.5 evaluation harness
class StubProvider:
    def __init__(self, table):
        self.table = table

    def embed(self, text):
        return self.table[text]


def _eval_fixture():
    idx = _index(6)
    docs = [("ops-en", "disk full alert", 0, []), ("ops-de", "festplatte voll", 1, []),
            ("fin-en", "invoice overdue", 2, []), ("fin-de", "rechnung ueberfaellig", 3, []),
            ("secret-1", "board minutes", 4, ["board"]), ("secret-2", "merger memo", 5, ["board"])]
    for did, text, axis, roles in docs:
        idx.add_document(VectorDocument(did, text, _e(axis), IndexFamily.TEXT, acl_allow_roles=roles))
    prov = StubProvider({"q-ops-en": _e(0), "q-ops-de": _e(1), "q-fin-en": _e(2), "q-fin-de": _e(4),
                         "q-board": _e(4)})
    corpus = [
        {"query": "q-ops-en", "relevant_doc_id": "ops-en", "domain": "ops", "language": "en", "split": "test"},
        {"query": "q-ops-de", "relevant_doc_id": "ops-de", "domain": "ops", "language": "de", "split": "test"},
        {"query": "q-fin-en", "relevant_doc_ids": {"fin-en": 3, "fin-de": 1}, "domain": "finance", "language": "en",
         "split": "dev"},
        # wrong embedding axis (points at a board-only doc the caller cannot see): miss
        {"query": "q-fin-de", "relevant_doc_id": "fin-de", "domain": "finance", "language": "de", "split": "test"},
        {"query": "q-board", "relevant_doc_id": "secret-1", "domain": "governance", "language": "en",
         "split": "test", "roles": ["board"]},
    ]
    return idx, prov, corpus


def test_metrics_by_domain_language_and_acl_selectivity_match_hand_values():
    idx, prov, corpus = _eval_fixture()
    rep = SearchEvaluationHarness().evaluate(idx, corpus, prov, top_k=1, config={"rrf_k": 60, "fusion": "rrf"})
    # top_k=1: ops-en hit, ops-de hit, fin-en hit (gain 3 of ideal [3]) => ndcg 1, recall 1/2; fin-de miss; board hit
    assert rep["queries_evaluated"] == 5
    assert rep["recall@k"] == round((1 + 1 + 0.5 + 0 + 1) / 5, 4)
    assert rep["ndcg@k"] == round((1 + 1 + 1 + 0 + 1) / 5, 4)
    assert rep["by_domain"]["ops"]["recall@k"] == 1.0 and rep["by_domain"]["finance"]["recall@k"] == 0.25
    assert rep["by_language"]["de"]["recall@k"] == 0.5 and rep["by_language"]["en"]["queries_evaluated"] == 3
    # public callers see 4/6 docs (high), board caller sees 6/6 (high); restrict further to get a medium bucket
    assert set(rep["by_acl_selectivity"]) == {"high"}


def test_graded_ndcg_oracle_at_k2():
    idx, prov, corpus = _eval_fixture()
    item = [{"query": "q-fin-en", "relevant_doc_ids": {"fin-de": 3, "fin-en": 1}, "split": "test"}]
    rep = SearchEvaluationHarness().evaluate(idx, item, prov, top_k=2)
    # ranking: fin-en first (dense+bm25? no bm25 terms) then something else; fin-de not in top-2 by dense
    res = idx.hybrid_search(query_text="q-fin-en", query_vector=_e(2), query_family=IndexFamily.TEXT,
                            caller_roles=["public"], top_k=2)
    ids = [r["doc_id"] for r in res]
    gains = {"fin-de": 3, "fin-en": 1}
    dcg = sum(gains.get(d, 0) / math.log2(i + 2) for i, d in enumerate(ids))
    idcg = 3 / math.log2(2) + 1 / math.log2(3)
    assert rep["ndcg@k"] == round(dcg / idcg, 4)


def test_acl_selectivity_buckets():
    idx = _index(6)
    for i in range(6):
        idx.add_document(VectorDocument(f"d{i}", f"doc {i}", _e(i), IndexFamily.TEXT,
                                        acl_allow_roles=[] if i == 0 else (["a"] if i < 3 else ["b"])))
    prov = StubProvider({"q": _e(0)})
    corpus = [{"query": "q", "relevant_doc_id": "d0", "roles": ["none"]},       # 1/6 visible -> low
              {"query": "q", "relevant_doc_id": "d0", "roles": ["a"]},          # 3/6 -> medium
              {"query": "q", "relevant_doc_id": "d0", "roles": ["a", "b"]}]     # 6/6 -> high
    rep = SearchEvaluationHarness().evaluate(idx, corpus, prov, top_k=1)
    assert set(rep["by_acl_selectivity"]) == {"low", "medium", "high"}


def test_provenance_records_splits_model_and_config_and_changes_with_them():
    idx, prov, corpus = _eval_fixture()
    h = SearchEvaluationHarness()
    rep = h.evaluate(idx, corpus, prov, top_k=1, config={"rrf_k": 60})
    p = rep["provenance"]
    assert p["splits"] == {"dev": 1, "test": 4} and p["model"] == "m" and p["dimension"] == 6
    assert p["config"] == {"rrf_k": 60} and p["distance_metric"] == "COSINE" and len(p["corpus_sha256"]) == 64
    changed = h.evaluate(idx, corpus[:-1], prov, top_k=1, config={"rrf_k": 10})["provenance"]
    assert changed["corpus_sha256"] != p["corpus_sha256"] and changed["config"] == {"rrf_k": 10}


def test_graph_proximity_gold_is_refused_and_empty_corpus_rejected():
    idx, prov, corpus = _eval_fixture()
    bad = [dict(corpus[0], gold_source="graph_proximity")]
    with pytest.raises(ValueError, match="graph proximity"):
        SearchEvaluationHarness().evaluate(idx, bad, prov)
    with pytest.raises(ValueError):
        SearchEvaluationHarness().evaluate(idx, [], prov)


# ------------------------------------------------------------------ live: real CPU embedding model
EMBED = os.getenv("EOIP_LIVE_OLLAMA_EMBED_MODEL", "")


@pytest.mark.skipif(not EMBED, reason="no live embedding model (set EOIP_LIVE_OLLAMA_EMBED_MODEL)")
def test_live_harness_on_real_embedding_model_by_domain():
    from eoip.models.embeddings import OllamaEmbeddingProvider

    provider = OllamaEmbeddingProvider(model=EMBED, url=os.getenv("EOIP_LIVE_OLLAMA_URL", "http://localhost:11434"),
                                       timeout=60)

    class Emb:  # nomic task prefixes; the harness embeds queries one at a time
        def embed(self, text, prefix="search_query: "):
            return provider.embed([prefix + text])[0]

    emb = Emb()
    docs = {"ops-1": "The database server ran out of disk space and stopped accepting writes.",
            "ops-2": "Kubernetes pods keep restarting because the container exceeds its memory limit.",
            "fin-1": "The customer has not paid the invoice that was due last month.",
            "fin-2": "Quarterly revenue grew because of higher subscription renewals."}
    vecs = {k: emb.embed(v, "search_document: ") for k, v in docs.items()}
    idx = _index(len(next(iter(vecs.values()))), model=EMBED)
    for k, v in docs.items():
        idx.add_document(VectorDocument(k, v, vecs[k], IndexFamily.TEXT))
    corpus = [{"query": "storage volume is full", "relevant_doc_id": "ops-1", "domain": "ops", "split": "test"},
              {"query": "pod crash loop out of memory", "relevant_doc_id": "ops-2", "domain": "ops", "split": "test"},
              {"query": "unpaid bill overdue", "relevant_doc_id": "fin-1", "domain": "finance", "split": "test"},
              {"query": "sales went up thanks to renewals", "relevant_doc_id": "fin-2", "domain": "finance",
               "split": "test"}]
    rep = SearchEvaluationHarness().evaluate(idx, corpus, emb, top_k=2, config={"provider": "ollama"})
    assert rep["recall@k"] >= 0.75 and set(rep["by_domain"]) == {"ops", "finance"}
    assert rep["provenance"]["model"] == EMBED
