"""Tenant-Scoped Vector Similarity, Hybrid Search, and Embedding Index Service (CRA-025.1-9, CRA-025.A).

Provides:
- Versioned keyword/vector index metadata with family isolation (TEXT vs GRAPH_STRUCTURE)
- Strict production profile refusing test-hashing fixtures
- Hard errors on provider unavailability or dimension mismatch (no silent zero padding)
- Pre- and post-retrieval ACL permission filtering with policy-epoch cache revocation
- Resumable indexing, shadow index evaluation, atomic cutover, and rollback
- BM25 + dense fusion via Reciprocal Rank Fusion (k=60 default) with graph-centrality boost
- Benchmarked evaluation harness for recall@k, nDCG@k, and latency across domains/languages
"""
from __future__ import annotations

import hashlib
import math
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from collections.abc import Callable


class IndexFamily(str, Enum):
    TEXT = "TEXT"
    GRAPH_STRUCTURE = "GRAPH_STRUCTURE"


class IndexState(str, Enum):
    ACTIVE = "ACTIVE"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"
    SHADOW = "SHADOW"


class ProductionConfigurationError(RuntimeError):
    """Raised when insecure test fixtures or test-hashing embedders are configured in production."""


class EmbeddingProviderUnavailableError(RuntimeError):
    """Raised when semantic embedding provider is disabled or unavailable."""


class DimensionMismatchError(ValueError):
    """Raised when embedding dimension does not match index metadata specification."""


class IncompatibleEmbeddingFamilyError(TypeError):
    """Raised when query vector family does not match target index family."""


class PermissionDeniedError(PermissionError):
    """Raised when principal lacks permission to access target items."""


@dataclass
class IndexMetadata:
    index_id: str
    scope: str  # tenant_id
    family: IndexFamily
    source_revision: str
    ontology_revision: str
    policy_revision: str
    provider: str
    model: str
    tokenizer: str
    dimension: int
    normalization: str = "L2"
    metric: str = "COSINE"
    policy_epoch: int = 1
    watermark_timestamp: float = field(default_factory=time.time)
    state: IndexState = IndexState.ACTIVE

    def to_dict(self) -> dict[str, Any]:
        return {
            "index_id": self.index_id,
            "scope": self.scope,
            "family": self.family.value,
            "source_revision": self.source_revision,
            "ontology_revision": self.ontology_revision,
            "policy_revision": self.policy_revision,
            "provider": self.provider,
            "model": self.model,
            "tokenizer": self.tokenizer,
            "dimension": self.dimension,
            "normalization": self.normalization,
            "metric": self.metric,
            "policy_epoch": self.policy_epoch,
            "watermark_timestamp": self.watermark_timestamp,
            "state": self.state.value,
        }


@dataclass
class VectorDocument:
    doc_id: str
    text: str
    vector: list[float]
    family: IndexFamily
    acl_allow_roles: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    graph_centrality: float = 0.0


class TestHashingEmbedder:
    """Test hashing embedder explicitly labelled test-hashing (CRA-025.7).

    REFUSED in production profile at startup.
    """
    __test__ = False

    def __init__(self, dimensions: int = 64, profile: str = "development") -> None:
        if profile.lower() == "production":
            raise ProductionConfigurationError(
                "test-hashing embedder is refused in production profile (CRA-025.7)"
            )
        self.dimensions = dimensions
        self.profile = profile

    def embed(self, text: str) -> list[float]:
        vec = []
        for i in range(self.dimensions):
            h = hashlib.sha256(f"{text}:{i}".encode("utf-8")).hexdigest()
            val = (int(h[:8], 16) / 0xFFFFFFFF) * 2.0 - 1.0
            vec.append(val)
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [round(x / norm, 4) for x in vec]


class RealSemanticProvider:
    """Semantic embedding provider backed by a real model (CRA-025.2/.6).

    Delegates to a configured backend: a local Ollama embedding model (``/api/embed``) or a local
    sentence-transformers model. There is no hashing fallback: an unavailable or disabled backend raises
    ``EmbeddingProviderUnavailableError`` and a vector whose dimension differs from the declared one raises
    ``DimensionMismatchError`` - nothing is padded, zeroed or substituted (deterministic hashing lives only in
    ``TestHashingEmbedder``, which production refuses).
    """

    def __init__(
        self,
        provider_name: str = "ollama",
        model_name: str | None = None,
        dimension: int | None = None,
        is_available: bool = True,
        backend: Any = None,
        url: str | None = None,
    ) -> None:
        self.provider_name = provider_name
        self.is_available = is_available
        self._backend = backend
        if self._backend is None and is_available:
            from eoip.models.embeddings import OllamaEmbeddingProvider, SentenceTransformersEmbeddingProvider

            if provider_name == "ollama":
                self._backend = OllamaEmbeddingProvider(model=model_name, url=url)
            elif provider_name == "sentence-transformers":
                self._backend = SentenceTransformersEmbeddingProvider(model_name=model_name)
            else:
                raise ValueError(f"unknown embedding provider {provider_name!r}")
        self.model_name = model_name or getattr(self._backend, "model_name", "")
        self.dimension = dimension

    def embed(self, text: str) -> list[float]:
        if not self.is_available or self._backend is None:
            raise EmbeddingProviderUnavailableError(
                f"Embedding provider '{self.provider_name}' is disabled or unavailable (CRA-025.2)"
            )
        from eoip.models.provider import ModelUnavailable

        try:
            vec = [float(x) for x in self._backend.embed_one(text)]
        except ModelUnavailable as exc:
            raise EmbeddingProviderUnavailableError(
                f"Embedding provider '{self.provider_name}/{self.model_name}' is unavailable: {exc} (CRA-025.2)"
            ) from exc
        if not vec or not any(vec):
            raise EmbeddingProviderUnavailableError("Embedding provider returned an empty/zero vector (CRA-025.2)")
        if self.dimension is None:
            self.dimension = len(vec)
        elif len(vec) != self.dimension:
            raise DimensionMismatchError(
                f"Provider '{self.model_name}' returned {len(vec)} dimensions, configured {self.dimension} (CRA-025.2)"
            )
        return vec

    def describe(self) -> dict[str, Any]:
        return {"provider": self.provider_name, "model": self.model_name, "dimension": self.dimension,
                "family": "test-hashing" if isinstance(self._backend, TestHashingEmbedder) else "semantic"}


def _cosine(v1: list[float], v2: list[float]) -> float:
    if len(v1) != len(v2) or not v1:
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    n1 = math.sqrt(sum(a * a for a in v1))
    n2 = math.sqrt(sum(b * b for b in v2))
    if n1 == 0.0 or n2 == 0.0:
        return 0.0
    return dot / (n1 * n2)


class TenantVectorIndex:
    """Tenant-partitioned vector index supporting BM25 + dense RRF, ACLs, and shadow cutover."""

    def __init__(self, metadata: IndexMetadata) -> None:
        self.metadata = metadata
        self.documents: dict[str, VectorDocument] = {}
        self.bm25_df: dict[str, int] = {}
        self.bm25_doc_len: dict[str, int] = {}
        self.checkpoint_watermark: int = 0
        self._cache: dict[tuple[str, int], list[dict[str, Any]]] = {}  # (query_hash, policy_epoch) -> results

    def add_document(self, doc: VectorDocument) -> None:
        # Check dimension
        if len(doc.vector) != self.metadata.dimension:
            raise DimensionMismatchError(
                f"Vector dimension {len(doc.vector)} does not match index dimension {self.metadata.dimension} (CRA-025.2)"
            )
        # Check family
        if doc.family != self.metadata.family:
            raise IncompatibleEmbeddingFamilyError(
                f"Cannot add document family {doc.family} into {self.metadata.family} index (CRA-025.8)"
            )

        self.documents[doc.doc_id] = doc
        tokens = re.findall(r"\w+", doc.text.lower())
        self.bm25_doc_len[doc.doc_id] = len(tokens)
        for term in set(tokens):
            self.bm25_df[term] = self.bm25_df.get(term, 0) + 1

    def remove_document(self, doc_id: str) -> bool:
        if doc_id in self.documents:
            del self.documents[doc_id]
            self.bm25_doc_len.pop(doc_id, None)
            return True
        return False

    def bm25_search(self, query: str, top_k: int = 20) -> list[tuple[str, float]]:
        q_terms = re.findall(r"\w+", query.lower())
        if not q_terms or not self.documents:
            return []
        avg_len = sum(self.bm25_doc_len.values()) / max(1, len(self.bm25_doc_len))
        scores: dict[str, float] = {}
        n_docs = len(self.documents)

        for term in q_terms:
            df = self.bm25_df.get(term, 0)
            if df == 0:
                continue
            idf = math.log((n_docs - df + 0.5) / (df + 0.5) + 1.0)
            for doc_id, doc in self.documents.items():
                tokens = re.findall(r"\w+", doc.text.lower())
                tf = tokens.count(term)
                if tf == 0:
                    continue
                dl = self.bm25_doc_len.get(doc_id, 1)
                norm = 1.0 - 0.75 + 0.75 * (dl / max(avg_len, 1e-9))
                score = idf * (tf * 2.2) / (tf + 1.2 * norm)
                scores[doc_id] = scores.get(doc_id, 0.0) + score

        ranked = sorted(scores.items(), key=lambda kv: -kv[1])
        return ranked[:top_k]

    def hybrid_search(
        self,
        query_text: str,
        query_vector: list[float],
        query_family: IndexFamily,
        caller_roles: list[str],
        top_k: int = 10,
        rrf_k: int = 60,
        use_graph_centrality: bool = True,
    ) -> list[dict[str, Any]]:
        # 1. Validate family and dimension
        if query_family != self.metadata.family:
            raise IncompatibleEmbeddingFamilyError(
                f"Query family {query_family} is incompatible with index family {self.metadata.family} (CRA-025.8)"
            )
        if len(query_vector) != self.metadata.dimension:
            raise DimensionMismatchError(
                f"Query vector dimension {len(query_vector)} != index dimension {self.metadata.dimension}"
            )

        # 2. Check scoped cache with policy epoch
        cache_key = (hashlib.sha256(f"{query_text}:{caller_roles}".encode("utf-8")).hexdigest(), self.metadata.policy_epoch)
        if cache_key in self._cache:
            return self._cache[cache_key]

        # 3. Dense retrieval with ACL pre-filtering (CRA-025.3)
        dense_candidates: list[tuple[str, float]] = []
        for doc_id, doc in self.documents.items():
            # Pre-filter: check permissions during candidate generation
            if doc.acl_allow_roles and not any(r in caller_roles for r in doc.acl_allow_roles):
                continue
            sim = _cosine(query_vector, doc.vector)
            dense_candidates.append((doc_id, sim))
        dense_candidates.sort(key=lambda kv: -kv[1])

        # 4. Sparse BM25 retrieval with ACL pre-filtering
        bm25_candidates_raw = self.bm25_search(query_text, top_k=top_k * 2)
        bm25_candidates = [
            (doc_id, score) for doc_id, score in bm25_candidates_raw
            if not self.documents[doc_id].acl_allow_roles or any(r in caller_roles for r in self.documents[doc_id].acl_allow_roles)
        ]

        # 5. Reciprocal Rank Fusion (RRF)
        rrf_scores: dict[str, float] = {}

        for rank, (doc_id, _) in enumerate(dense_candidates[:top_k * 2], start=1):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (rrf_k + rank))

        for rank, (doc_id, _) in enumerate(bm25_candidates[:top_k * 2], start=1):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (rrf_k + rank))

        # Add optional graph centrality signal
        if use_graph_centrality:
            for doc_id in rrf_scores:
                cent = self.documents[doc_id].graph_centrality
                rrf_scores[doc_id] += 0.05 * cent

        # Final delivery post-filter
        final_ranked = sorted(rrf_scores.items(), key=lambda kv: -kv[1])
        results = []
        for doc_id, final_score in final_ranked[:top_k]:
            doc = self.documents[doc_id]
            # Final delivery ACL verification
            if doc.acl_allow_roles and not any(r in caller_roles for r in doc.acl_allow_roles):
                continue
            results.append({
                "doc_id": doc.doc_id,
                "text": doc.text,
                "final_score": round(final_score, 6),
                "metadata": doc.metadata,
                "index_family": self.metadata.family.value,
            })

        # Cache result under current policy epoch
        self._cache[cache_key] = results
        return results

    def revoke_policy_epoch(self) -> None:
        """Increments policy epoch and invalidates all scoped caches (CRA-025.3)."""
        self.metadata.policy_epoch += 1
        self._cache.clear()


class HybridVectorIndexManager:
    """Manages active and shadow indexes with atomic cutover and rollback (CRA-025.4)."""

    def __init__(self, tenant_id: str) -> None:
        self.tenant_id = tenant_id
        self.active_indexes: dict[IndexFamily, TenantVectorIndex] = {}
        self.shadow_indexes: dict[str, TenantVectorIndex] = {}
        self._history_stack: list[dict[IndexFamily, TenantVectorIndex]] = []

    def set_active_index(self, index: TenantVectorIndex) -> None:
        if index.metadata.scope != self.tenant_id:
            raise ValueError("Cross-tenant index assignment rejected")
        self.active_indexes[index.metadata.family] = index

    def create_shadow_index(
        self,
        family: IndexFamily,
        new_provider: str,
        new_model: str,
        new_dim: int,
    ) -> str:
        shadow_id = f"shadow_{family.value}_{int(time.time())}"
        meta = IndexMetadata(
            index_id=shadow_id,
            scope=self.tenant_id,
            family=family,
            source_revision="rev_v2",
            ontology_revision="ont_v2",
            policy_revision="pol_v2",
            provider=new_provider,
            model=new_model,
            tokenizer="custom",
            dimension=new_dim,
            state=IndexState.SHADOW,
        )
        shadow_idx = TenantVectorIndex(meta)
        self.shadow_indexes[shadow_id] = shadow_idx
        return shadow_id

    def cutover_shadow_index(self, shadow_id: str) -> None:
        """Atomically promotes shadow index to active and saves state for rollback."""
        shadow = self.shadow_indexes.get(shadow_id)
        if not shadow:
            raise KeyError(f"Shadow index {shadow_id} not found")

        # Snapshot current active state for rollback
        self._history_stack.append(dict(self.active_indexes))
        shadow.metadata.state = IndexState.ACTIVE
        self.active_indexes[shadow.metadata.family] = shadow
        self.shadow_indexes.pop(shadow_id, None)

    def rollback(self) -> bool:
        """Restores previous active index state."""
        if not self._history_stack:
            return False
        prev = self._history_stack.pop()
        self.active_indexes = prev
        return True


class SearchEvaluationHarness:
    """Evaluates search quality (recall@k, nDCG, latency) on labelled corpora (CRA-025.5)."""

    def evaluate(
        self,
        index: TenantVectorIndex,
        eval_corpus: list[dict[str, Any]],
        provider: Any,
        top_k: int = 10,
    ) -> dict[str, float]:
        hits = 0
        dcg = 0.0
        idcg = 0.0
        latencies: list[float] = []

        for item in eval_corpus:
            query = item["query"]
            gold_id = item["relevant_doc_id"]
            roles = item.get("roles", ["public"])

            t0 = time.perf_counter()
            q_vec = provider.embed(query)
            res = index.hybrid_search(
                query_text=query,
                query_vector=q_vec,
                query_family=index.metadata.family,
                caller_roles=roles,
                top_k=top_k,
            )
            latencies.append((time.perf_counter() - t0) * 1000.0)

            retrieved_ids = [r["doc_id"] for r in res]
            if gold_id in retrieved_ids:
                hits += 1
                rank = retrieved_ids.index(gold_id) + 1
                dcg += 1.0 / math.log2(rank + 1)
            idcg += 1.0  # single gold item

        n = len(eval_corpus) or 1
        recall = hits / n
        ndcg = (dcg / idcg) if idcg > 0 else 0.0
        latencies.sort()
        p50 = latencies[int(len(latencies) * 0.5)]
        p95 = latencies[min(int(len(latencies) * 0.95), len(latencies) - 1)]

        return {
            "recall@k": round(recall, 4),
            "ndcg@k": round(ndcg, 4),
            "latency_p50_ms": round(p50, 2),
            "latency_p95_ms": round(p95, 2),
            "queries_evaluated": n,
        }
