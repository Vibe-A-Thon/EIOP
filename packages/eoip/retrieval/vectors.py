"""Local keyword (BM25-style) and vector (hashing embeddings) search indexes.

Covers GAP-SEARCH-001 (full-text + vector + graph hybrid search),
GAP-SEARCH-002 (results preserve graph identity: every hit is keyed by the
canonical entity ID and maps back to the authoritative graph store — this
module never holds a second knowledge store), GAP-RET-002 (candidate
retrievers: keyword/full-text and vector) and GAP-RET-006 (retrieval trace).

Everything is deterministic, pure-Python, and dependency-free beyond stdlib.
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import Any, Protocol

_TOKEN_RE = re.compile(r"[a-z0-9_]+")


def tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


# -- keyword index (BM25-style scoring) -------------------------------------


class KeywordIndex:
    """In-memory BM25-style keyword index over entity text."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self._docs: dict[str, list[str]] = {}
        self._df: dict[str, int] = {}
        self._doc_len: dict[str, int] = {}

    def add(self, entity_id: str, text: str) -> None:
        tokens = tokenize(text)
        self.remove(entity_id)
        self._docs[entity_id] = tokens
        self._doc_len[entity_id] = len(tokens)
        for term in set(tokens):
            self._df[term] = self._df.get(term, 0) + 1

    def remove(self, entity_id: str) -> None:
        old = self._docs.pop(entity_id, None)
        self._doc_len.pop(entity_id, None)
        if old:
            for term in set(old):
                self._df[term] -= 1
                if self._df[term] <= 0:
                    del self._df[term]

    def _idf(self, term: str) -> float:
        n = len(self._docs)
        df = self._df.get(term, 0)
        return math.log((n - df + 0.5) / (df + 0.5) + 1.0)

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        q_terms = tokenize(query)
        if not q_terms or not self._docs:
            return []
        avg_len = sum(self._doc_len.values()) / max(1, len(self._doc_len))
        scores: dict[str, float] = {}
        for term in q_terms:
            idf = self._idf(term)
            if idf <= 0.0:
                continue
            for doc_id, tokens in self._docs.items():
                tf = tokens.count(term)
                if tf == 0:
                    continue
                dl = self._doc_len[doc_id]
                norm = 1.0 - self.b + self.b * dl / max(avg_len, 1e-9)
                scores[doc_id] = scores.get(doc_id, 0.0) + idf * (
                    tf * (self.k1 + 1.0) / (tf + self.k1 * norm)
                )
        ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
        return [(doc_id, score) for doc_id, score in ranked[:top_k] if score > 0.0]


# -- vector index (deterministic hashing embeddings) -------------------------


class HashingEmbedder:
    """Deterministic hashing-trick embedder (no external model), family ``test-hashing`` (CRA-025.7).

    Each token maps to a fixed dimension via md5 and a sign via a second
    hash; token weights are log-scaled term frequencies. Output vectors are
    L2-normalized so cosine similarity is a dot product. It is lexical, not
    semantic: it exists for tests and offline development and is refused when
    ``EOIP_ENV=production`` (use ``eoip.models.embeddings.semantic_embedder``).
    """

    family = "test-hashing"
    model_name = "test-hashing"

    def __init__(self, dimensions: int = 256):
        from eoip.models.embeddings import refuse_test_hashing_in_production

        refuse_test_hashing_in_production()
        self.dimensions = dimensions

    def _bucket(self, token: str) -> tuple[int, int]:
        digest = hashlib.md5(token.encode("utf-8"), usedforsecurity=False).hexdigest()
        index = int(digest[:8], 16) % self.dimensions
        sign = 1.0 if int(digest[8:16], 16) % 2 == 0 else -1.0
        return index, sign

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        tokens = tokenize(text)
        for term in set(tokens):
            tf = tokens.count(term)
            index, sign = self._bucket(term)
            vector[index] += sign * (1.0 + math.log(tf))
        norm = math.sqrt(sum(v * v for v in vector))
        if norm > 0.0:
            vector = [v / norm for v in vector]
        return vector


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        return 0.0
    return sum(x * y for x, y in zip(a, b))


class _BatchEmbedderAdapter:
    """Adapt a batch ``EmbeddingProvider`` to single-text embedding.

    GAP-SEARCH-001/§7.3: lets VectorIndex consume real embedding providers
    without changing its single-text calling convention.
    """

    def __init__(self, provider: Any):
        self._provider = provider

    @property
    def dimensions(self) -> int:
        return getattr(self._provider, "dim", 0) or 0

    def embed(self, text: str) -> list[float]:
        return self._provider.embed([text])[0]

    def embed_one(self, text: str) -> list[float]:
        return self._provider.embed([text])[0]


class VectorIndex:
    """In-memory vector index keyed by canonical entity ID."""

    def __init__(self, embedder: Any | None = None):
        # HashingEmbedder by default, or an EmbeddingProvider-compatible
        # backend (GAP-SEARCH-001/§7.3). Providers use a batch embed()
        # signature, so adapt them to single-text embedding.
        if embedder is None:
            from eoip.models.embeddings import semantic_embedder

            # CRA-025.2/.7: the shared backend (configured model; labelled test-hashing only outside production).
            self.embedder: Any = semantic_embedder()
        elif isinstance(embedder, HashingEmbedder) or callable(getattr(embedder, "embed_one", None)):
            self.embedder = embedder
        else:
            self.embedder = _BatchEmbedderAdapter(embedder)
        self._vectors: dict[str, list[float]] = {}

    def _embed(self, text: str) -> list[float]:
        embed_one = getattr(self.embedder, "embed_one", None)
        if callable(embed_one):
            return embed_one(text)
        return self.embedder.embed(text)

    def add(self, entity_id: str, text: str) -> None:
        self._vectors[entity_id] = self._embed(text)

    def remove(self, entity_id: str) -> None:
        self._vectors.pop(entity_id, None)

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        if not self._vectors:
            return []
        query_vec = self._embed(query)
        scores = [
            (entity_id, cosine_similarity(query_vec, vector))
            for entity_id, vector in self._vectors.items()
        ]
        scores.sort(key=lambda kv: (-kv[1], kv[0]))
        return [(entity_id, score) for entity_id, score in scores[:top_k] if score > 0.0]

    # SearchIndex port alias
    def vector_search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        return self.search(query, top_k)


# -- trace -------------------------------------------------------------------


class RetrievalTrace:
    """Debug trace for a retrieval request (GAP-RET-006)."""

    def __init__(self) -> None:
        self.steps: list[dict[str, Any]] = []

    def record(self, stage: str, candidates: list[tuple[str, float]], **detail: Any) -> None:
        self.steps.append(
            {
                "stage": stage,
                "candidates": [
                    {"entity_id": entity_id, "score": round(float(score), 6)}
                    for entity_id, score in candidates
                ],
                **detail,
            }
        )

    def to_dict(self) -> dict[str, Any]:
        return {"steps": self.steps}


# -- search index abstraction (replaceable per GAP-SEARCH-001/002) -----------


class SearchIndex(Protocol):
    """Port for replaceable search indexes (keyword, vector, or fused)."""

    def add(self, entity_id: str, text: str) -> None: ...

    def remove(self, entity_id: str) -> None: ...

    def keyword_search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]: ...

    def vector_search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]: ...

    def entity_ids(self) -> list[str]: ...


class InMemorySearchIndex:
    """Default in-memory SearchIndex combining keyword and vector indexes."""

    def __init__(self, keyword: KeywordIndex | None = None, vector: VectorIndex | None = None):
        self.keyword = keyword or KeywordIndex()
        self.vector = vector or VectorIndex()

    def add(self, entity_id: str, text: str) -> None:
        self.keyword.add(entity_id, text)
        self.vector.add(entity_id, text)

    def remove(self, entity_id: str) -> None:
        self.keyword.remove(entity_id)
        self.vector.remove(entity_id)

    def keyword_search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        return self.keyword.search(query, top_k)

    def vector_search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        return self.vector.search(query, top_k)

    def entity_ids(self) -> list[str]:
        return sorted(self.keyword._docs)


_TEXT_PROPERTIES = (
    "name",
    "summary",
    "title",
    "description",
    "qualified_name",
    "issue_key",
    "path",
    "content",
)


def entity_text(label: str, properties: dict) -> str:
    """Canonical text used for indexing: name/description/labels."""
    parts = [label]
    for key in _TEXT_PROPERTIES:
        value = properties.get(key)
        if isinstance(value, str) and value.strip():
            parts.append(value.strip())
    labels = properties.get("labels")
    if isinstance(labels, (list, tuple)):
        parts.extend(str(item) for item in labels)
    return " \n ".join(parts)


def build_vector_index(embedder: Any | None = None) -> VectorIndex:
    """Provider-aware VectorIndex construction (GAP-SEARCH-001/§7.3).

    Uses ``embedder`` (e.g. an OllamaEmbeddingProvider) when given, otherwise
    the deterministic hashing embedder.
    """
    return VectorIndex(embedder)


def build_search_index(
    store,
    index: InMemorySearchIndex | None = None,
    embedder: Any | None = None,
) -> InMemorySearchIndex:
    """Build a SearchIndex from the graph store. IDs are canonical entity IDs,
    so hits always resolve back to authoritative graph entities (GAP-SEARCH-002).
    Pass ``embedder`` to embed via a specific provider; by default the shared
    ``semantic_embedder`` is used (GAP-SEARCH-001/§7.3, CRA-025.7)."""
    index = index or InMemorySearchIndex(vector=VectorIndex(embedder))
    for vertex in store.find_vertices(limit=10_000, include_deleted=False):
        text = entity_text(vertex["label"], vertex.get("properties") or {})
        if text.strip():
            index.add(vertex["canonical_id"], text)
    return index
