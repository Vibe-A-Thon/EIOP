"""GAP-SEARCH-001/§7.3: embedding provider integration tests.

Uses a fake Ollama-compatible HTTP server (http.server in-thread) to cover
success, dimension handling, unavailable-provider fallback to hashing, and
index construction with real embeddings.
"""

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from eoip.models.embeddings import (
    EmbeddingProvider,
    OllamaEmbeddingProvider,
    build_embedding_provider,
)
from eoip.models.provider import ModelUnavailable
from eoip.graph.memory import MemoryGraphStore
from eoip.retrieval.vectors import (
    HashingEmbedder,
    VectorIndex,
    build_search_index,
    build_vector_index,
)

_DIM = 8


def _fake_vector(seed: int) -> list[float]:
    return [float((seed + i) % 3) for i in range(_DIM)]


class _Handler(BaseHTTPRequestHandler):
    vectors = staticmethod(lambda text: _fake_vector(len(text)))  # per-test override
    fail = False

    def log_message(self, *args):  # silence test output
        pass

    def do_GET(self):
        if self.fail:
            self.send_response(503)
            self.end_headers()
            return
        body = json.dumps({"models": []}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.fail:
            self.send_response(503)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(length))
        vectors = [self.vectors(text) for text in payload["input"]]
        body = json.dumps({"embeddings": vectors}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


@pytest.fixture
def server():
    _Handler.fail = False
    _Handler.vectors = staticmethod(lambda text: _fake_vector(len(text)))
    httpd = HTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()
    thread.join(timeout=5)


def _provider(url: str) -> OllamaEmbeddingProvider:
    return OllamaEmbeddingProvider(model="test-embed", url=url, timeout=2.0)


# -- provider protocol --------------------------------------------------------


def test_ollama_provider_success_and_dim(server):
    provider = _provider(server)
    assert isinstance(provider, EmbeddingProvider)
    vecs = provider.embed(["alpha", "longer-text"])
    assert len(vecs) == 2
    assert all(len(v) == _DIM for v in vecs)
    assert provider.dim == _DIM
    assert provider.health() is True


def test_ollama_provider_embed_one(server):
    provider = _provider(server)
    vec = provider.embed_one("alpha")
    assert len(vec) == _DIM
    assert provider.embed([]) == []


def test_ollama_provider_unavailable_raises_model_unavailable():
    provider = OllamaEmbeddingProvider(model="m", url="http://127.0.0.1:1", timeout=0.5)
    with pytest.raises(ModelUnavailable):
        provider.embed(["x"])
    assert provider.health() is False


def test_ollama_provider_server_error_raises_model_unavailable(server):
    _Handler.fail = True
    provider = _provider(server)
    with pytest.raises(ModelUnavailable):
        provider.embed(["x"])
    assert provider.health() is False


def test_ollama_provider_malformed_response_raises_model_unavailable(server):
    _Handler.vectors = staticmethod(lambda text: "not-a-vector")
    provider = _provider(server)
    with pytest.raises(ModelUnavailable):
        provider.embed(["x"])


# -- vector index integration --------------------------------------------------


def test_vector_index_with_real_embeddings_ranking(server):
    # Vectors keyed by first token so semantically similar texts are closer.
    table = {"payment": _fake_vector(1), "dashboard": _fake_vector(50)}
    _Handler.vectors = staticmethod(lambda text: table[text.split()[0]])
    index = VectorIndex(_provider(server))
    index.add("a", "payment reconciliation")
    index.add("b", "dashboard rendering")
    hits = index.vector_search("payment pipeline", top_k=5)
    assert hits[0][0] == "a"


def test_dimension_mismatch_between_add_and_query_falls_back(server):
    provider = _provider(server)
    index = VectorIndex(provider)
    index.add("a", "short")  # dim _DIM
    # Shrink subsequent embeddings to simulate a model/dim change.
    _Handler.vectors = staticmethod(lambda text: [0.5, 0.5])
    index.add("b", "some other text")
    # Query embeds at dim 2 while stored "a" is dim _DIM; cosine zips to the
    # shorter length — no crash, deterministic result.
    hits = index.vector_search("some other", top_k=5)
    assert hits[0][0] == "b"


def test_unavailable_provider_falls_back_to_hashing():
    provider = OllamaEmbeddingProvider(model="m", url="http://127.0.0.1:1", timeout=0.5)
    index = VectorIndex(provider)
    with pytest.raises(ModelUnavailable):
        index.add("a", "payment reconciliation pipeline")
    # Caller falls back to the deterministic hashing embedder.
    fallback = VectorIndex()
    assert isinstance(fallback.embedder, HashingEmbedder)
    fallback.add("a", "payment reconciliation pipeline")
    fallback.add("b", "dashboard rendering chart glitch")
    hits = fallback.vector_search("payment pipeline reconciliation", top_k=5)
    assert hits[0][0] == "a"


def test_build_vector_index_defaults_to_hashing():
    index = build_vector_index()
    assert isinstance(index.embedder, HashingEmbedder)


def test_build_search_index_with_embedder_uses_provider(server):
    _Handler.vectors = staticmethod(lambda text: _fake_vector(len(text)))
    store = MemoryGraphStore()
    store.upsert_vertex(
        "Document",
        {
            "canonical_id": "urn:eoip:doc:1",
            "name": "Payments runbook",
            "description": "Operational runbook for the payment reconciliation service.",
        },
    )
    index = build_search_index(store, embedder=_provider(server))
    assert "urn:eoip:doc:1" in index.entity_ids()
    hits = index.vector_search("payments runbook", top_k=5)
    assert hits and hits[0][0] == "urn:eoip:doc:1"


# -- environment-based construction --------------------------------------------


def test_build_embedding_provider_requires_env(monkeypatch):
    monkeypatch.delenv("EOIP_OLLAMA_EMBED_MODEL", raising=False)
    assert build_embedding_provider() is None
    monkeypatch.setenv("EOIP_OLLAMA_EMBED_MODEL", "nomic-embed-text")
    provider = build_embedding_provider()
    assert isinstance(provider, OllamaEmbeddingProvider)
    assert provider.model_name == "nomic-embed-text"
