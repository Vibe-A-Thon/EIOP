"""Unified Hybrid Search Engine — orchestrates all 7 search modalities.

Combines and reranks results from:
1. Keyword/Lexical (BM25 via KeywordIndex)
2. Vector/Similarity (cosine via SemanticVectorIndex + VectorIndex)
3. Contextual (user profile, history, preference boosting)
4. Multimodal (text + image + audio embedding unification)
5. Hybrid (weighted keyword+vector fusion)
6. Graph-Based/Traversal (multi-hop entity/relationship expansion)
7. Structured/Relational (Cypher/SQL-style filter queries)

Each modality produces scored candidates.  The engine applies Reciprocal
Rank Fusion (RRF) to merge heterogeneous score distributions into a single
unified ranking.
"""

from __future__ import annotations

import hashlib
import math
import re
import threading
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol


# ── Search Modalities ────────────────────────────────────────────────


class SearchModality(str, Enum):
    KEYWORD = "KEYWORD"
    VECTOR = "VECTOR"
    CONTEXTUAL = "CONTEXTUAL"
    MULTIMODAL = "MULTIMODAL"
    HYBRID = "HYBRID"
    GRAPH = "GRAPH"
    STRUCTURED = "STRUCTURED"


# ── Data Models ──────────────────────────────────────────────────────


@dataclass
class UserContext:
    """User-specific context for contextual search personalization."""
    user_id: str
    role: str = ""
    team: str = ""
    recent_entities: list[str] = field(default_factory=list)
    preferred_types: list[str] = field(default_factory=list)
    search_history: list[str] = field(default_factory=list)
    region: str = ""
    expertise_domains: list[str] = field(default_factory=list)


@dataclass
class MultimodalInput:
    """Multi-format query input."""
    text: str = ""
    image_embedding: list[float] | None = None
    audio_transcript: str = ""
    structured_filters: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchCandidate:
    """A single candidate from any modality."""
    entity_id: str
    score: float
    modality: SearchModality
    text: str = ""
    entity_type: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    explanation: str = ""


@dataclass
class UnifiedSearchResult:
    """Final merged result after RRF fusion across modalities."""
    entity_id: str
    text: str
    entity_type: str
    final_score: float
    modality_scores: dict[str, float] = field(default_factory=dict)
    modalities_matched: list[str] = field(default_factory=list)
    explanations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "text": self.text,
            "entity_type": self.entity_type,
            "final_score": round(self.final_score, 6),
            "modality_scores": {k: round(v, 6) for k, v in self.modality_scores.items()},
            "modalities_matched": self.modalities_matched,
            "explanations": self.explanations,
        }


@dataclass
class SearchPlan:
    """Execution plan showing which modalities will be used and why."""
    plan_id: str
    query: str
    active_modalities: list[SearchModality]
    reasoning: dict[str, str] = field(default_factory=dict)
    estimated_candidates: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "query": self.query,
            "active_modalities": [m.value for m in self.active_modalities],
            "reasoning": self.reasoning,
            "estimated_candidates": self.estimated_candidates,
        }


@dataclass
class SearchMetrics:
    """Per-query search performance metrics."""
    query_id: str
    total_candidates: int
    candidates_per_modality: dict[str, int]
    fusion_time_ms: float
    modality_times_ms: dict[str, float]
    result_count: int
    query_text: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "query_id": self.query_id,
            "total_candidates": self.total_candidates,
            "candidates_per_modality": self.candidates_per_modality,
            "fusion_time_ms": round(self.fusion_time_ms, 2),
            "modality_times_ms": {k: round(v, 2) for k, v in self.modality_times_ms.items()},
            "result_count": self.result_count,
        }


# ── Helper: Reciprocal Rank Fusion ───────────────────────────────────


def reciprocal_rank_fusion(
    ranked_lists: list[list[SearchCandidate]],
    k: int = 60,
    modality_weights: dict[str, float] | None = None,
) -> dict[str, float]:
    """Merge multiple ranked lists via RRF with optional modality weighting.

    RRF score = Σ weight_m / (k + rank_m) for each modality m where entity appears.
    """
    scores: dict[str, float] = defaultdict(float)
    weights = modality_weights or {}

    for ranked in ranked_lists:
        for rank, candidate in enumerate(ranked, start=1):
            w = weights.get(candidate.modality.value, 1.0)
            scores[candidate.entity_id] += w / (k + rank)

    return dict(scores)


# ── Keyword Search Adapter ───────────────────────────────────────────


class KeywordSearchAdapter:
    """Wraps BM25 KeywordIndex for the unified engine."""

    def __init__(self) -> None:
        self._docs: dict[str, dict[str, Any]] = {}
        self._index_data: dict[str, str] = {}

    def index(self, entity_id: str, text: str,
              entity_type: str = "", metadata: dict[str, Any] | None = None) -> None:
        self._index_data[entity_id] = text
        self._docs[entity_id] = {
            "text": text, "entity_type": entity_type,
            "metadata": metadata or {},
        }

    def remove(self, entity_id: str) -> None:
        self._index_data.pop(entity_id, None)
        self._docs.pop(entity_id, None)

    def search(self, query: str, top_k: int = 50) -> list[SearchCandidate]:
        token_re = re.compile(r"[a-z0-9_]+")
        query_tokens = token_re.findall(query.lower())
        if not query_tokens:
            return []

        n = len(self._index_data)
        if n == 0:
            return []

        df: dict[str, int] = defaultdict(int)
        doc_tokens: dict[str, list[str]] = {}
        for eid, text in self._index_data.items():
            tokens = token_re.findall(text.lower())
            doc_tokens[eid] = tokens
            for t in set(tokens):
                df[t] += 1

        avg_dl = sum(len(t) for t in doc_tokens.values()) / max(n, 1)
        k1, b = 1.5, 0.75
        scored: list[tuple[str, float]] = []

        for eid, tokens in doc_tokens.items():
            score = 0.0
            dl = len(tokens)
            for qt in query_tokens:
                if df[qt] == 0:
                    continue
                tf = tokens.count(qt)
                if tf == 0:
                    continue
                idf = math.log((n - df[qt] + 0.5) / (df[qt] + 0.5) + 1.0)
                norm = 1.0 - b + b * dl / max(avg_dl, 1e-9)
                score += idf * (tf * (k1 + 1.0)) / (tf + k1 * norm)
            if score > 0:
                scored.append((eid, score))

        scored.sort(key=lambda x: -x[1])

        results: list[SearchCandidate] = []
        for eid, sc in scored[:top_k]:
            doc = self._docs.get(eid, {})
            results.append(SearchCandidate(
                entity_id=eid, score=sc,
                modality=SearchModality.KEYWORD,
                text=doc.get("text", ""),
                entity_type=doc.get("entity_type", ""),
                explanation=f"BM25 keyword match (score={sc:.4f})",
            ))
        return results

    def count(self) -> int:
        return len(self._index_data)


# ── Vector Search Adapter ────────────────────────────────────────────


def _hash_embed(text: str, dim: int = 128) -> list[float]:
    h = hashlib.sha256(text.lower().encode()).digest()
    raw = [(h[i % len(h)] + i * 7) % 256 - 128 for i in range(dim)]
    norm = math.sqrt(sum(x * x for x in raw)) or 1.0
    return [x / norm for x in raw]


def _cosine(a: list[float], b: list[float]) -> float:
    if len(a) != len(b) or not a:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    return dot / (na * nb)


class VectorSearchAdapter:
    """Embedding-based similarity search."""

    def __init__(self, dim: int = 128) -> None:
        self._dim = dim
        self._vectors: dict[str, list[float]] = {}
        self._docs: dict[str, dict[str, Any]] = {}

    def index(self, entity_id: str, text: str,
              vector: list[float] | None = None,
              entity_type: str = "", metadata: dict[str, Any] | None = None) -> None:
        v = vector if vector and len(vector) == self._dim else _hash_embed(text, self._dim)
        self._vectors[entity_id] = v
        self._docs[entity_id] = {
            "text": text, "entity_type": entity_type,
            "metadata": metadata or {},
        }

    def remove(self, entity_id: str) -> None:
        self._vectors.pop(entity_id, None)
        self._docs.pop(entity_id, None)

    def search(self, query: str, top_k: int = 50,
               query_vector: list[float] | None = None) -> list[SearchCandidate]:
        qv = query_vector if query_vector and len(query_vector) == self._dim else _hash_embed(query, self._dim)

        scored: list[tuple[str, float]] = []
        for eid, vec in self._vectors.items():
            sim = _cosine(qv, vec)
            if sim > 0:
                scored.append((eid, sim))

        scored.sort(key=lambda x: -x[1])
        results: list[SearchCandidate] = []
        for eid, sc in scored[:top_k]:
            doc = self._docs.get(eid, {})
            results.append(SearchCandidate(
                entity_id=eid, score=sc,
                modality=SearchModality.VECTOR,
                text=doc.get("text", ""),
                entity_type=doc.get("entity_type", ""),
                explanation=f"Vector similarity (cosine={sc:.4f})",
            ))
        return results

    def count(self) -> int:
        return len(self._vectors)


# ── Contextual Search Adapter ────────────────────────────────────────


class ContextualSearchAdapter:
    """Reranks candidates using user context signals."""

    def __init__(self) -> None:
        self._user_profiles: dict[str, UserContext] = {}

    def register_user(self, ctx: UserContext) -> None:
        self._user_profiles[ctx.user_id] = ctx

    def get_user(self, user_id: str) -> UserContext | None:
        return self._user_profiles.get(user_id)

    def boost(self, candidates: list[SearchCandidate],
              user_id: str) -> list[SearchCandidate]:
        ctx = self._user_profiles.get(user_id)
        if not ctx:
            return candidates

        boosted: list[SearchCandidate] = []
        for c in candidates:
            boost_factor = 1.0
            reasons: list[str] = []

            if c.entity_id in ctx.recent_entities:
                boost_factor += 0.15
                reasons.append("recently accessed")

            if ctx.preferred_types and c.entity_type in ctx.preferred_types:
                boost_factor += 0.1
                reasons.append(f"preferred type: {c.entity_type}")

            if ctx.expertise_domains:
                text_lower = c.text.lower()
                for domain in ctx.expertise_domains:
                    if domain.lower() in text_lower:
                        boost_factor += 0.08
                        reasons.append(f"expertise domain: {domain}")
                        break

            if ctx.search_history:
                history_tokens = set()
                for h in ctx.search_history[-5:]:
                    history_tokens.update(h.lower().split())
                entity_tokens = set(c.text.lower().split())
                overlap = len(history_tokens & entity_tokens)
                if overlap > 0:
                    boost_factor += min(overlap * 0.03, 0.12)
                    reasons.append(f"history overlap ({overlap} terms)")

            new_score = c.score * boost_factor
            explanation = c.explanation
            if reasons:
                explanation += f"; contextual boost: {', '.join(reasons)}"

            boosted.append(SearchCandidate(
                entity_id=c.entity_id, score=new_score,
                modality=SearchModality.CONTEXTUAL,
                text=c.text, entity_type=c.entity_type,
                metadata=c.metadata, explanation=explanation,
            ))

        boosted.sort(key=lambda x: -x.score)
        return boosted


# ── Multimodal Search Adapter ────────────────────────────────────────


class MultimodalSearchAdapter:
    """Combines text, image embeddings, and audio transcripts into unified search."""

    def __init__(self, dim: int = 128) -> None:
        self._dim = dim
        self._text_vectors: dict[str, list[float]] = {}
        self._image_vectors: dict[str, list[float]] = {}
        self._audio_vectors: dict[str, list[float]] = {}
        self._docs: dict[str, dict[str, Any]] = {}

    def index(self, entity_id: str, text: str = "",
              image_embedding: list[float] | None = None,
              audio_text: str = "",
              entity_type: str = "") -> None:
        self._docs[entity_id] = {"text": text, "entity_type": entity_type}
        if text:
            self._text_vectors[entity_id] = _hash_embed(text, self._dim)
        if image_embedding and len(image_embedding) == self._dim:
            self._image_vectors[entity_id] = image_embedding
        if audio_text:
            self._audio_vectors[entity_id] = _hash_embed(audio_text, self._dim)

    def search(self, query: MultimodalInput,
               top_k: int = 50) -> list[SearchCandidate]:
        all_scores: dict[str, list[tuple[float, str]]] = defaultdict(list)

        if query.text:
            qv = _hash_embed(query.text, self._dim)
            for eid, vec in self._text_vectors.items():
                sim = _cosine(qv, vec)
                if sim > 0:
                    all_scores[eid].append((sim, "text"))

        if query.image_embedding and len(query.image_embedding) == self._dim:
            for eid, vec in self._image_vectors.items():
                sim = _cosine(query.image_embedding, vec)
                if sim > 0:
                    all_scores[eid].append((sim, "image"))

        if query.audio_transcript:
            qv = _hash_embed(query.audio_transcript, self._dim)
            for eid, vec in self._audio_vectors.items():
                sim = _cosine(qv, vec)
                if sim > 0:
                    all_scores[eid].append((sim, "audio"))

        scored: list[tuple[str, float, list[str]]] = []
        for eid, score_list in all_scores.items():
            combined = sum(s for s, _ in score_list) / max(len(score_list), 1)
            modality_bonus = len(score_list) * 0.05
            modals = [m for _, m in score_list]
            scored.append((eid, combined + modality_bonus, modals))

        scored.sort(key=lambda x: -x[1])

        results: list[SearchCandidate] = []
        for eid, sc, modals in scored[:top_k]:
            doc = self._docs.get(eid, {})
            results.append(SearchCandidate(
                entity_id=eid, score=sc,
                modality=SearchModality.MULTIMODAL,
                text=doc.get("text", ""),
                entity_type=doc.get("entity_type", ""),
                explanation=f"Multimodal match across {', '.join(modals)} (score={sc:.4f})",
            ))
        return results

    def count(self) -> int:
        return len(self._docs)


# ── Graph Search Adapter ─────────────────────────────────────────────


class GraphSearchAdapter:
    """Traverses graph relationships to find connected entities."""

    def __init__(self) -> None:
        self._adjacency: dict[str, list[tuple[str, str, float]]] = {}
        self._docs: dict[str, dict[str, Any]] = {}

    def add_entity(self, entity_id: str, text: str = "",
                   entity_type: str = "") -> None:
        self._docs[entity_id] = {"text": text, "entity_type": entity_type}
        if entity_id not in self._adjacency:
            self._adjacency[entity_id] = []

    def add_edge(self, source: str, target: str,
                 label: str = "RELATED", weight: float = 1.0) -> None:
        self._adjacency.setdefault(source, []).append((target, label, weight))
        self._adjacency.setdefault(target, []).append((source, label, weight))

    def search(self, seed_entities: list[str], max_hops: int = 2,
               top_k: int = 50) -> list[SearchCandidate]:
        if not seed_entities:
            return []

        visited: dict[str, tuple[int, float, list[str]]] = {}

        from collections import deque
        queue: deque[tuple[str, int, float, list[str]]] = deque()

        for seed in seed_entities:
            if seed in self._adjacency:
                visited[seed] = (0, 1.0, ["seed"])
                queue.append((seed, 0, 1.0, ["seed"]))

        while queue:
            node, depth, score, path = queue.popleft()
            if depth >= max_hops:
                continue
            for neighbor, label, weight in self._adjacency.get(node, []):
                next_score = score * weight * (0.7 ** depth)
                next_path = path + [f"--{label}-->", neighbor]
                if neighbor not in visited or visited[neighbor][1] < next_score:
                    visited[neighbor] = (depth + 1, next_score, next_path)
                    queue.append((neighbor, depth + 1, next_score, next_path))

        for seed in seed_entities:
            visited.pop(seed, None)

        scored = sorted(visited.items(), key=lambda x: -x[1][1])

        results: list[SearchCandidate] = []
        for eid, (hops, sc, path) in scored[:top_k]:
            doc = self._docs.get(eid, {})
            results.append(SearchCandidate(
                entity_id=eid, score=sc,
                modality=SearchModality.GRAPH,
                text=doc.get("text", ""),
                entity_type=doc.get("entity_type", ""),
                explanation=f"Graph traversal: {hops} hop(s), path={' '.join(path[:7])}",
            ))
        return results

    def count(self) -> int:
        return len(self._docs)


# ── Structured Search Adapter ────────────────────────────────────────


class StructuredSearchAdapter:
    """Filter-based structured search using field matching (SQL/Cypher-style)."""

    def __init__(self) -> None:
        self._records: dict[str, dict[str, Any]] = {}

    def index(self, entity_id: str, fields: dict[str, Any]) -> None:
        self._records[entity_id] = fields

    def remove(self, entity_id: str) -> None:
        self._records.pop(entity_id, None)

    def search(self, filters: dict[str, Any],
               sort_by: str | None = None,
               top_k: int = 50) -> list[SearchCandidate]:
        results: list[SearchCandidate] = []

        for eid, fields in self._records.items():
            match = True
            match_count = 0

            for key, value in filters.items():
                field_val = fields.get(key)

                if isinstance(value, dict):
                    op = value.get("op", "eq")
                    cmp_val = value.get("value")
                    if op == "gt" and not (field_val is not None and field_val > cmp_val):
                        match = False; break
                    elif op == "lt" and not (field_val is not None and field_val < cmp_val):
                        match = False; break
                    elif op == "gte" and not (field_val is not None and field_val >= cmp_val):
                        match = False; break
                    elif op == "lte" and not (field_val is not None and field_val <= cmp_val):
                        match = False; break
                    elif op == "contains" and not (isinstance(field_val, str) and str(cmp_val).lower() in field_val.lower()):
                        match = False; break
                    elif op == "in" and field_val not in cmp_val:
                        match = False; break
                    elif op == "eq" and field_val != cmp_val:
                        match = False; break
                    else:
                        match_count += 1
                elif field_val != value:
                    match = False
                    break
                else:
                    match_count += 1

            if match and match_count > 0:
                score = match_count / max(len(filters), 1)
                text = fields.get("name", fields.get("text", eid))
                results.append(SearchCandidate(
                    entity_id=eid, score=score,
                    modality=SearchModality.STRUCTURED,
                    text=str(text),
                    entity_type=fields.get("type", fields.get("entity_type", "")),
                    explanation=f"Structured filter match ({match_count}/{len(filters)} fields)",
                ))

        if sort_by and results:
            results.sort(key=lambda c: self._records.get(c.entity_id, {}).get(sort_by, ""), reverse=True)
        else:
            results.sort(key=lambda c: -c.score)

        return results[:top_k]

    def count(self) -> int:
        return len(self._records)


# ── Unified Hybrid Search Engine ─────────────────────────────────────


class HybridSearchEngine:
    """Orchestrates all 7 search modalities with Reciprocal Rank Fusion."""

    def __init__(self, vector_dim: int = 128) -> None:
        self._lock = threading.Lock()
        self.keyword = KeywordSearchAdapter()
        self.vector = VectorSearchAdapter(dim=vector_dim)
        self.contextual = ContextualSearchAdapter()
        self.multimodal = MultimodalSearchAdapter(dim=vector_dim)
        self.graph = GraphSearchAdapter()
        self.structured = StructuredSearchAdapter()

        self._modality_weights: dict[str, float] = {
            SearchModality.KEYWORD.value: 1.0,
            SearchModality.VECTOR.value: 1.2,
            SearchModality.CONTEXTUAL.value: 1.1,
            SearchModality.MULTIMODAL.value: 1.0,
            SearchModality.HYBRID.value: 1.3,
            SearchModality.GRAPH.value: 0.9,
            SearchModality.STRUCTURED.value: 1.0,
        }
        self._metrics_log: list[SearchMetrics] = []
        self._max_metrics: int = 500

    def index_entity(self, entity_id: str, text: str,
                     entity_type: str = "",
                     fields: dict[str, Any] | None = None,
                     image_embedding: list[float] | None = None,
                     audio_text: str = "") -> None:
        """Index an entity across all applicable modalities."""
        meta = fields or {}
        self.keyword.index(entity_id, text, entity_type=entity_type)
        self.vector.index(entity_id, text, entity_type=entity_type)
        self.multimodal.index(entity_id, text=text,
                              image_embedding=image_embedding,
                              audio_text=audio_text,
                              entity_type=entity_type)
        self.graph.add_entity(entity_id, text=text, entity_type=entity_type)

        struct_fields = {"name": text, "type": entity_type, **meta}
        self.structured.index(entity_id, struct_fields)

    def add_edge(self, source: str, target: str,
                 label: str = "RELATED", weight: float = 1.0) -> None:
        self.graph.add_edge(source, target, label=label, weight=weight)

    def remove_entity(self, entity_id: str) -> None:
        self.keyword.remove(entity_id)
        self.vector.remove(entity_id)
        self.structured.remove(entity_id)

    def set_modality_weights(self, weights: dict[str, float]) -> None:
        self._modality_weights.update(weights)

    def plan_search(self, query: str,
                    modalities: list[SearchModality] | None = None,
                    user_context: UserContext | None = None,
                    multimodal_input: MultimodalInput | None = None,
                    structured_filters: dict[str, Any] | None = None,
                    graph_seeds: list[str] | None = None) -> SearchPlan:
        """Determine which modalities to activate based on query signals."""
        active: list[SearchModality] = []
        reasoning: dict[str, str] = {}

        if modalities:
            active = list(modalities)
            for m in active:
                reasoning[m.value] = "explicitly requested"
        else:
            active.append(SearchModality.KEYWORD)
            reasoning["KEYWORD"] = "always active for lexical recall"

            active.append(SearchModality.VECTOR)
            reasoning["VECTOR"] = "semantic similarity for concept matching"

            active.append(SearchModality.HYBRID)
            reasoning["HYBRID"] = "fusion of keyword+vector for best coverage"

            if user_context:
                active.append(SearchModality.CONTEXTUAL)
                reasoning["CONTEXTUAL"] = f"user context available (user={user_context.user_id})"

            if multimodal_input and (multimodal_input.image_embedding or multimodal_input.audio_transcript):
                active.append(SearchModality.MULTIMODAL)
                reasoning["MULTIMODAL"] = "non-text input detected"

            if graph_seeds:
                active.append(SearchModality.GRAPH)
                reasoning["GRAPH"] = f"graph seeds provided ({len(graph_seeds)} entities)"

            if structured_filters:
                active.append(SearchModality.STRUCTURED)
                reasoning["STRUCTURED"] = f"structured filters: {list(structured_filters.keys())}"

        return SearchPlan(
            plan_id=uuid.uuid4().hex[:12],
            query=query,
            active_modalities=active,
            reasoning=reasoning,
            estimated_candidates=self.keyword.count(),
        )

    def search(self, query: str,
               top_k: int = 20,
               modalities: list[SearchModality] | None = None,
               user_context: UserContext | None = None,
               multimodal_input: MultimodalInput | None = None,
               structured_filters: dict[str, Any] | None = None,
               graph_seeds: list[str] | None = None,
               graph_hops: int = 2,
               rrf_k: int = 60) -> list[UnifiedSearchResult]:
        """Execute unified search across all active modalities."""
        if not query.strip() and not graph_seeds and not structured_filters and not multimodal_input:
            return []

        start = time.time()
        plan = self.plan_search(
            query, modalities=modalities, user_context=user_context,
            multimodal_input=multimodal_input,
            structured_filters=structured_filters,
            graph_seeds=graph_seeds,
        )

        all_candidates: list[list[SearchCandidate]] = []
        candidate_pool: dict[str, SearchCandidate] = {}
        modality_times: dict[str, float] = {}
        candidates_per_modality: dict[str, int] = {}

        for mod in plan.active_modalities:
            t0 = time.time()
            candidates: list[SearchCandidate] = []

            if mod == SearchModality.KEYWORD:
                candidates = self.keyword.search(query, top_k=top_k * 3)

            elif mod == SearchModality.VECTOR:
                qv = None
                if multimodal_input and multimodal_input.image_embedding:
                    qv = multimodal_input.image_embedding
                candidates = self.vector.search(query, top_k=top_k * 3, query_vector=qv)

            elif mod == SearchModality.HYBRID:
                kw = self.keyword.search(query, top_k=top_k * 2)
                vec = self.vector.search(query, top_k=top_k * 2)
                hybrid_scores: dict[str, tuple[float, float]] = {}
                for c in kw:
                    hybrid_scores[c.entity_id] = (c.score, 0.0)
                for c in vec:
                    kw_score = hybrid_scores.get(c.entity_id, (0.0, 0.0))[0]
                    hybrid_scores[c.entity_id] = (kw_score, c.score)

                for eid, (kws, vecs) in hybrid_scores.items():
                    combined = 0.3 * kws + 0.7 * vecs
                    doc_text = ""
                    etype = ""
                    for c in kw + vec:
                        if c.entity_id == eid:
                            doc_text = c.text
                            etype = c.entity_type
                            break
                    candidates.append(SearchCandidate(
                        entity_id=eid, score=combined,
                        modality=SearchModality.HYBRID,
                        text=doc_text, entity_type=etype,
                        explanation=f"Hybrid: kw={kws:.4f} + vec={vecs:.4f} → {combined:.4f}",
                    ))
                candidates.sort(key=lambda c: -c.score)
                candidates = candidates[:top_k * 3]

            elif mod == SearchModality.CONTEXTUAL:
                base = self.keyword.search(query, top_k=top_k * 2)
                if user_context:
                    candidates = self.contextual.boost(base, user_context.user_id)
                else:
                    candidates = base

            elif mod == SearchModality.MULTIMODAL:
                if multimodal_input:
                    candidates = self.multimodal.search(multimodal_input, top_k=top_k * 2)
                else:
                    mi = MultimodalInput(text=query)
                    candidates = self.multimodal.search(mi, top_k=top_k * 2)

            elif mod == SearchModality.GRAPH:
                seeds = graph_seeds or []
                candidates = self.graph.search(seeds, max_hops=graph_hops, top_k=top_k * 2)

            elif mod == SearchModality.STRUCTURED:
                if structured_filters:
                    candidates = self.structured.search(structured_filters, top_k=top_k * 2)

            if candidates:
                all_candidates.append(candidates)
                for c in candidates:
                    if c.entity_id not in candidate_pool:
                        candidate_pool[c.entity_id] = c

            modality_times[mod.value] = (time.time() - t0) * 1000
            candidates_per_modality[mod.value] = len(candidates)

        if not all_candidates:
            return []

        fusion_start = time.time()
        rrf_scores = reciprocal_rank_fusion(
            all_candidates, k=rrf_k, modality_weights=self._modality_weights,
        )

        per_entity_modalities: dict[str, dict[str, float]] = defaultdict(dict)
        per_entity_explanations: dict[str, list[str]] = defaultdict(list)
        for ranked in all_candidates:
            for c in ranked:
                per_entity_modalities[c.entity_id][c.modality.value] = c.score
                if c.explanation:
                    per_entity_explanations[c.entity_id].append(c.explanation)

        merged = sorted(rrf_scores.items(), key=lambda x: -x[1])

        results: list[UnifiedSearchResult] = []
        for eid, final_score in merged[:top_k]:
            c = candidate_pool.get(eid)
            if not c:
                continue
            mod_scores = per_entity_modalities.get(eid, {})
            results.append(UnifiedSearchResult(
                entity_id=eid,
                text=c.text,
                entity_type=c.entity_type,
                final_score=final_score,
                modality_scores=mod_scores,
                modalities_matched=list(mod_scores.keys()),
                explanations=per_entity_explanations.get(eid, [])[:5],
            ))

        fusion_time = (time.time() - fusion_start) * 1000

        metrics = SearchMetrics(
            query_id=uuid.uuid4().hex[:12],
            total_candidates=sum(candidates_per_modality.values()),
            candidates_per_modality=candidates_per_modality,
            fusion_time_ms=fusion_time,
            modality_times_ms=modality_times,
            result_count=len(results),
            query_text=query,
        )
        with self._lock:
            self._metrics_log.append(metrics)
            if len(self._metrics_log) > self._max_metrics:
                self._metrics_log = self._metrics_log[-self._max_metrics:]

        return results

    def get_metrics(self, limit: int = 20) -> list[dict[str, Any]]:
        return [m.to_dict() for m in self._metrics_log[-limit:]]

    def stats(self) -> dict[str, Any]:
        return {
            "keyword_index_size": self.keyword.count(),
            "vector_index_size": self.vector.count(),
            "multimodal_index_size": self.multimodal.count(),
            "graph_entity_count": self.graph.count(),
            "structured_record_count": self.structured.count(),
            "modality_weights": dict(self._modality_weights),
            "total_searches": len(self._metrics_log),
            "registered_users": len(self.contextual._user_profiles),
        }


_instance: HybridSearchEngine | None = None
_lock = threading.Lock()


def get_hybrid_search_engine(vector_dim: int = 128) -> HybridSearchEngine:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = HybridSearchEngine(vector_dim=vector_dim)
    return _instance
