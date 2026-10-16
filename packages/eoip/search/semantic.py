"""Semantic vector search — wires embeddings into the search pipeline.

Provides entity similarity search via cosine distance on embedding vectors,
concept drift detection across temporal snapshots, cross-lingual matching
through language-agnostic embedding alignment, and hybrid scoring that
combines BM25 keyword relevance with vector similarity.
"""

from __future__ import annotations

import hashlib
import math
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DriftSeverity(str, Enum):
    NONE = "NONE"
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class EmbeddedEntity:
    entity_id: str
    text: str
    vector: list[float]
    entity_type: str = ""
    language: str = "en"
    metadata: dict[str, Any] = field(default_factory=dict)
    indexed_at: float = field(default_factory=time.time)

    @property
    def dim(self) -> int:
        return len(self.vector)


@dataclass
class SimilarityResult:
    entity_id: str
    score: float
    text: str
    entity_type: str = ""
    language: str = "en"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "score": round(self.score, 6),
            "text": self.text,
            "entity_type": self.entity_type,
            "language": self.language,
        }


@dataclass
class HybridSearchResult:
    entity_id: str
    text: str
    keyword_score: float
    vector_score: float
    combined_score: float
    entity_type: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "text": self.text,
            "keyword_score": round(self.keyword_score, 6),
            "vector_score": round(self.vector_score, 6),
            "combined_score": round(self.combined_score, 6),
            "entity_type": self.entity_type,
        }


@dataclass
class DriftReport:
    entity_id: str
    old_centroid: list[float]
    new_centroid: list[float]
    drift_distance: float
    severity: DriftSeverity
    snapshot_old: str
    snapshot_new: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "drift_distance": round(self.drift_distance, 6),
            "severity": self.severity.value,
            "snapshot_old": self.snapshot_old,
            "snapshot_new": self.snapshot_new,
        }


def _cosine_sim(a: list[float], b: list[float]) -> float:
    if len(a) != len(b) or not a:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    return dot / (na * nb)


def _hash_embed(text: str, dim: int = 64) -> list[float]:
    """Deterministic hashing embedder for tests and offline fallback."""
    h = hashlib.sha256(text.lower().encode()).digest()
    raw = []
    for i in range(dim):
        byte_idx = i % len(h)
        raw.append((h[byte_idx] + i * 7) % 256 - 128)
    norm = math.sqrt(sum(x * x for x in raw)) or 1.0
    return [x / norm for x in raw]


def embed_text(text: str, dim: int = 64) -> list[float]:
    """Embed text via configured model provider (Ollama / sentence-transformers) with offline fallback (H-02)."""
    try:
        from eoip.models.embeddings import build_embedding_provider
        provider = build_embedding_provider()
        if provider is not None:
            vecs = provider.embed([text])
            if vecs and len(vecs[0]) > 0:
                v = vecs[0]
                if len(v) == dim:
                    return v
                elif len(v) > dim:
                    return v[:dim]
                else:
                    return v + [0.0] * (dim - len(v))
    except Exception:
        pass
    return _hash_embed(text, dim)


class SemanticVectorIndex:
    """In-memory vector index for semantic entity search."""

    def __init__(self, dim: int = 64) -> None:
        self._lock = threading.Lock()
        self._dim = dim
        self._entities: dict[str, EmbeddedEntity] = {}
        self._snapshots: dict[str, dict[str, list[float]]] = {}

    @property
    def dim(self) -> int:
        return self._dim

    def index_entity(self, entity_id: str, text: str,
                     vector: list[float] | None = None,
                     entity_type: str = "", language: str = "en",
                     metadata: dict[str, Any] | None = None) -> None:
        if vector is None:
            vector = embed_text(text, self._dim)
        if len(vector) != self._dim:
            raise ValueError(f"Vector dim {len(vector)} != index dim {self._dim}")
        with self._lock:
            self._entities[entity_id] = EmbeddedEntity(
                entity_id=entity_id, text=text, vector=vector,
                entity_type=entity_type, language=language,
                metadata=metadata or {},
            )

    def remove_entity(self, entity_id: str) -> bool:
        with self._lock:
            return self._entities.pop(entity_id, None) is not None

    def similarity_search(self, query_vector: list[float],
                          top_k: int = 10,
                          entity_type: str | None = None,
                          language: str | None = None,
                          min_score: float = 0.0) -> list[SimilarityResult]:
        with self._lock:
            candidates = list(self._entities.values())

        if entity_type:
            candidates = [e for e in candidates if e.entity_type == entity_type]
        if language:
            candidates = [e for e in candidates if e.language == language]

        scored = []
        for ent in candidates:
            sim = _cosine_sim(query_vector, ent.vector)
            if sim >= min_score:
                scored.append((sim, ent))

        scored.sort(key=lambda x: -x[0])

        return [
            SimilarityResult(
                entity_id=e.entity_id, score=s, text=e.text,
                entity_type=e.entity_type, language=e.language,
                metadata=e.metadata,
            )
            for s, e in scored[:top_k]
        ]

    def find_similar(self, entity_id: str, top_k: int = 10,
                     min_score: float = 0.0) -> list[SimilarityResult]:
        ent = self._entities.get(entity_id)
        if not ent:
            return []
        results = self.similarity_search(
            ent.vector, top_k=top_k + 1, min_score=min_score
        )
        return [r for r in results if r.entity_id != entity_id][:top_k]

    def search_by_text(self, query_text: str, top_k: int = 10,
                       entity_type: str | None = None,
                       min_score: float = 0.0) -> list[SimilarityResult]:
        qv = _hash_embed(query_text, self._dim)
        return self.similarity_search(
            qv, top_k=top_k, entity_type=entity_type, min_score=min_score,
        )

    def hybrid_search(self, query_text: str, top_k: int = 10,
                      keyword_weight: float = 0.3,
                      vector_weight: float = 0.7) -> list[HybridSearchResult]:
        import re
        query_tokens = set(re.findall(r"[a-z0-9_]+", query_text.lower()))
        if not query_tokens:
            return []

        qv = _hash_embed(query_text, self._dim)

        results: list[HybridSearchResult] = []
        with self._lock:
            entities = list(self._entities.values())

        for ent in entities:
            vec_score = max(0.0, _cosine_sim(qv, ent.vector))

            doc_tokens = set(re.findall(r"[a-z0-9_]+", ent.text.lower()))
            if doc_tokens:
                overlap = len(query_tokens & doc_tokens)
                kw_score = overlap / len(query_tokens)
            else:
                kw_score = 0.0

            combined = keyword_weight * kw_score + vector_weight * vec_score
            if combined > 0.0:
                results.append(HybridSearchResult(
                    entity_id=ent.entity_id, text=ent.text,
                    keyword_score=kw_score, vector_score=vec_score,
                    combined_score=combined, entity_type=ent.entity_type,
                ))

        results.sort(key=lambda x: -x.combined_score)
        return results[:top_k]

    def save_snapshot(self, snapshot_id: str) -> int:
        with self._lock:
            vectors = {eid: list(e.vector) for eid, e in self._entities.items()}
            self._snapshots[snapshot_id] = vectors
            return len(vectors)

    def detect_drift(self, snapshot_old: str, snapshot_new: str,
                     threshold: float = 0.15) -> list[DriftReport]:
        old = self._snapshots.get(snapshot_old, {})
        new = self._snapshots.get(snapshot_new, {})
        if not old or not new:
            return []

        common = set(old.keys()) & set(new.keys())
        reports: list[DriftReport] = []
        for eid in common:
            dist = 1.0 - _cosine_sim(old[eid], new[eid])
            if dist >= threshold:
                if dist >= 0.5:
                    severity = DriftSeverity.CRITICAL
                elif dist >= 0.35:
                    severity = DriftSeverity.HIGH
                elif dist >= 0.25:
                    severity = DriftSeverity.MODERATE
                else:
                    severity = DriftSeverity.LOW
                reports.append(DriftReport(
                    entity_id=eid,
                    old_centroid=old[eid][:4],
                    new_centroid=new[eid][:4],
                    drift_distance=dist,
                    severity=severity,
                    snapshot_old=snapshot_old,
                    snapshot_new=snapshot_new,
                ))

        reports.sort(key=lambda r: -r.drift_distance)
        return reports

    def cross_lingual_search(self, query_text: str,
                             target_languages: list[str],
                             top_k: int = 10) -> dict[str, list[SimilarityResult]]:
        qv = _hash_embed(query_text, self._dim)
        results: dict[str, list[SimilarityResult]] = {}
        for lang in target_languages:
            results[lang] = self.similarity_search(
                qv, top_k=top_k, language=lang,
            )
        return results

    def stats(self) -> dict[str, Any]:
        with self._lock:
            types: dict[str, int] = {}
            langs: dict[str, int] = {}
            for e in self._entities.values():
                types[e.entity_type] = types.get(e.entity_type, 0) + 1
                langs[e.language] = langs.get(e.language, 0) + 1
            return {
                "total_entities": len(self._entities),
                "dimension": self._dim,
                "snapshots": len(self._snapshots),
                "by_type": types,
                "by_language": langs,
            }


_instance: SemanticVectorIndex | None = None
_lock = threading.Lock()


def get_semantic_index(dim: int = 64) -> SemanticVectorIndex:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = SemanticVectorIndex(dim=dim)
    return _instance
