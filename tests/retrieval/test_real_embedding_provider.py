"""CRA-025.2/.6/.7: the semantic embedding provider on a real model (nomic-embed-text v1.5 Q8 GGUF on CPU Ollama).

Live tests run when ``EOIP_LIVE_OLLAMA_EMBED_MODEL`` names a model served at ``EOIP_LIVE_OLLAMA_URL`` (CI job
``llm-cpu-reference``); the contract tests below always run.
"""

from __future__ import annotations

import json
import os

import httpx
import pytest

from eoip.models.embeddings import (
    OllamaEmbeddingProvider,
    TestHashingRefused,
    embedder_family,
    semantic_embedder,
)
from eoip.retrieval.hybrid_vector_service import (
    DimensionMismatchError,
    EmbeddingProviderUnavailableError,
    RealSemanticProvider,
)
from eoip.retrieval.vectors import HashingEmbedder, VectorIndex, cosine_similarity

LIVE_MODEL = os.getenv("EOIP_LIVE_OLLAMA_EMBED_MODEL")
LIVE_URL = os.getenv("EOIP_LIVE_OLLAMA_URL", "http://localhost:11434")
live = pytest.mark.skipif(not LIVE_MODEL, reason="EOIP_LIVE_OLLAMA_EMBED_MODEL not set (runs in llm-cpu-reference)")

_CLEAR = ("EOIP_OLLAMA_EMBED_MODEL", "EOIP_EMBEDDING_PROVIDER", "EOIP_SENTENCE_TRANSFORMER_MODEL", "EOIP_ENV", "APP_ENV")


def _clear(monkeypatch):
    for name in _CLEAR:
        monkeypatch.delenv(name, raising=False)


# --- contract (always) -------------------------------------------------------------------------------------------

@pytest.mark.req("CRA-025")
def test_test_hashing_is_labelled_and_refused_in_production(monkeypatch):
    _clear(monkeypatch)
    emb = semantic_embedder()
    assert isinstance(emb, HashingEmbedder) and embedder_family(emb) == "test-hashing"
    monkeypatch.setenv("EOIP_ENV", "production")
    with pytest.raises(TestHashingRefused):
        semantic_embedder()
    with pytest.raises(TestHashingRefused):
        HashingEmbedder()


@pytest.mark.req("CRA-025")
def test_configured_model_is_used_in_production(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("EOIP_ENV", "production")
    monkeypatch.setenv("EOIP_OLLAMA_EMBED_MODEL", "nomic-embed-text-v1.5-q8")
    emb = semantic_embedder()
    assert isinstance(emb, OllamaEmbeddingProvider) and embedder_family(emb) == "semantic"


@pytest.mark.req("CRA-025")
def test_ollama_provider_contract_against_api_shape(monkeypatch):
    """Request/response contract of Ollama /api/embed, checked against a recorded-shape mock."""
    seen = {}

    class _Resp:
        def __init__(self, body):
            self._b = body

        def read(self):
            return self._b

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(request, timeout):
        seen["url"], seen["body"] = request.full_url, json.loads(request.data)
        return _Resp(json.dumps({"model": "m", "embeddings": [[0.1, 0.2, 0.3], [0.3, 0.2, 0.1]]}).encode())

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    provider = OllamaEmbeddingProvider(model="m", url="http://ollama.test")
    assert provider.embed(["a", "b"]) == [[0.1, 0.2, 0.3], [0.3, 0.2, 0.1]]
    assert seen == {"url": "http://ollama.test/api/embed", "body": {"model": "m", "input": ["a", "b"]}}
    assert provider.dim == 3


@pytest.mark.req("CRA-025")
def test_unreachable_model_is_a_hard_error():
    provider = RealSemanticProvider(model_name="nomic-embed-text-v1.5-q8", url="http://127.0.0.1:9")
    with pytest.raises(EmbeddingProviderUnavailableError):
        provider.embed("anything")


# --- live model --------------------------------------------------------------------------------------------------

def _provider(dimension=None):
    return RealSemanticProvider(provider_name="ollama", model_name=LIVE_MODEL, url=LIVE_URL, dimension=dimension)


@live
@pytest.mark.req("CRA-025")
def test_live_model_dimension_and_mismatch():
    vec = _provider().embed("search_query: invoice approval workflow")
    assert len(vec) == 768
    with pytest.raises(DimensionMismatchError):
        _provider(dimension=384).embed("search_query: anything")


@live
@pytest.mark.req("CRA-025")
def test_live_model_is_semantic_not_lexical():
    """Paraphrases with few shared words outrank lexically-overlapping unrelated sentences.

    A hashing embedder cannot do this (it only sees shared tokens), which is the fake this replaces.
    """
    triples = [
        ("How do I reset my password?", "Steps to recover account credentials after forgetting them",
         "Password-protected PDF attachments are skipped by the crawler"),
        ("The car would not start this morning", "My vehicle's engine failed to turn over at dawn",
         "The morning standup will start at nine"),
        ("Revenue grew strongly last quarter", "Sales increased significantly in the previous three months",
         "The quarter-final match was postponed"),
        ("A cat is sleeping on the sofa", "A kitten naps on the couch",
         "The sofa factory is hiring sleeping-bag designers"),
    ]
    p, h = _provider(), HashingEmbedder()
    model_wins = hash_wins = 0
    for query, paraphrase, distractor in triples:
        q = _norm(p.embed("search_query: " + query))
        a = _norm(p.embed("search_document: " + paraphrase))
        b = _norm(p.embed("search_document: " + distractor))
        model_wins += cosine_similarity(q, a) > cosine_similarity(q, b)
        hash_wins += cosine_similarity(h.embed(query), h.embed(paraphrase)) > cosine_similarity(
            h.embed(query), h.embed(distractor))
    assert model_wins == len(triples)
    assert hash_wins <= 1  # the lexical fixture fails the same check


@live
@pytest.mark.req("CRA-025")
def test_live_vector_index_recall_on_paraphrase_corpus():
    corpus = {
        "inc-1": "Database server ran out of disk space and stopped accepting writes",
        "inc-2": "Users cannot sign in because the identity provider certificate expired",
        "inc-3": "Monthly invoice totals were wrong due to a currency rounding bug",
        "inc-4": "The nightly backup job failed because the storage bucket was unreachable",
        "inc-5": "Web page load times spiked after a CDN configuration change",
    }
    queries = {
        "storage volume full, inserts rejected": "inc-1",
        "login broken after TLS cert lapsed": "inc-2",
        "billing amounts incorrect from FX precision": "inc-3",
        "scheduled snapshot could not reach object store": "inc-4",
        "site slow following edge cache settings update": "inc-5",
    }
    provider = OllamaEmbeddingProvider(model=LIVE_MODEL, url=LIVE_URL, timeout=60)
    index = VectorIndex(provider)
    for doc_id, text in corpus.items():
        index.add(doc_id, text)
    hits = sum(index.search(q, top_k=1)[0][0] == want for q, want in queries.items())
    assert hits >= 4, f"semantic recall@1 {hits}/5"


@live
@pytest.mark.req("CRA-025")
def test_live_processing_text_embed_uses_the_shared_model(monkeypatch):
    from eoip.processing.contracts import LogicalUnit, ProcessingRequest
    from eoip.processing.service import ProcessingService

    _clear(monkeypatch)
    monkeypatch.setenv("EOIP_ENV", "production")
    monkeypatch.setenv("EOIP_OLLAMA_EMBED_MODEL", LIVE_MODEL)
    monkeypatch.setenv("EOIP_OLLAMA_URL", LIVE_URL)
    from eoip.processing.contracts import ExecutionContext

    req = ProcessingRequest(logical_unit=LogicalUnit.NPU, operator_id="text.embed",
                            inputs={"texts": ["search_query: reset password", "search_document: recover credentials"]})
    result, receipt = ProcessingService().execute_direct(req, ExecutionContext(tenant_id="t", principal_id="p"))
    assert result["embedding_family"] == "semantic" and result["model"] == LIVE_MODEL
    assert result["dimensions"] == 768 and result["count"] == 2
    assert receipt.actual_provider == "embedding_model"
    direct = OllamaEmbeddingProvider(model=LIVE_MODEL, url=LIVE_URL, timeout=60).embed(["search_query: reset password"])[0]
    assert cosine_similarity(_norm(direct), _norm(result["embeddings"][0])) > 0.999


def _norm(v):
    n = sum(x * x for x in v) ** 0.5
    return [x / n for x in v]


@live
def test_live_url_reachable_when_configured():
    assert httpx.get(f"{LIVE_URL}/api/version", timeout=5).status_code == 200
