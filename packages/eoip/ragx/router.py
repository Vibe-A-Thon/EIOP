"""HTTP surface for the RAG extensions (wired by apps/api; not registered here).

Follows the lazy ``build_router(store)`` pattern from
``eoip.graph.bitemporal``: the API wiring step calls ``build_router(store)``
and includes the returned router; no apps/api changes happen in this module.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from eoip.graph.rag_router import RAGAbstentionPolicy
from eoip.graph.store import GraphStore
from eoip.ragx import metrics as ragx_metrics
from eoip.ragx import techniques as ragx_techniques
from eoip.ragx.architectures import ARCHITECTURES, build_architecture
from eoip.ragx.core import Candidate


class RagxQueryRequest(BaseModel):
    query: str = Field(..., description="Natural-language question")
    architecture: str | None = Field(default=None, description="Named §4 architecture; default: adaptive pick")
    context: dict[str, Any] = Field(default_factory=dict, description="Architecture-specific context")


class RagxQueryResponse(BaseModel):
    architecture: str
    answer: str
    confidence: float
    abstained: bool
    abstention_reasons: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    highlight_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    evidence_manifest: dict[str, Any] | None = None


class CandidateIn(BaseModel):
    source_id: str
    text: str = ""
    score: float = 1.0
    kind: str = "entity"
    label: str = ""
    properties: dict[str, Any] = Field(default_factory=dict)
    citations: list[str] = Field(default_factory=list)

    def to_candidate(self) -> Candidate:
        return Candidate(
            source_id=self.source_id, text=self.text, score=self.score,
            kind=self.kind, label=self.label,
            properties=dict(self.properties), citations=list(self.citations),
        )


class TechniqueRequest(BaseModel):
    technique: str = Field(..., description="Named §4 technique")
    query: str = ""
    candidates: list[CandidateIn] = Field(default_factory=list)
    params: dict[str, Any] = Field(default_factory=dict)


class MetricsRequest(BaseModel):
    metric: str = Field(..., description="recall_at_k | precision_at_k | mrr | ndcg_at_k | citation_accuracy | access_control_correctness")
    ranking: list[str] = Field(default_factory=list)
    rankings: list[list[str]] = Field(default_factory=list)
    relevant: list[str] = Field(default_factory=list)
    relevance: dict[str, float] = Field(default_factory=dict)
    claims: list[dict[str, Any]] = Field(default_factory=list)
    allowed: list[str] = Field(default_factory=list)
    denied: list[str] = Field(default_factory=list)
    k: int = 10


_ADAPTIVE_HINTS = [
    ("event", "event_aware"),
    ("symbol", "coderag"),
    ("provenance", "provenance_aware"),
    ("version", "version_aware"),
    ("community", "hierarchical"),
    ("overview", "global_search"),
    ("path", "pathrag"),
    ("record", "structured"),
]


def _adaptive_architecture(query: str, context: dict[str, Any]) -> str:
    q = query.lower()
    for hint, name in _ADAPTIVE_HINTS:
        if hint in q:
            return name
    if context.get("event_id"):
        return "event_aware"
    if context.get("valid_at") or context.get("known_at"):
        return "temporal"
    if context.get("version") or context.get("doc_version"):
        return "version_aware"
    return "local_search"


def build_router(store: GraphStore):
    """Construct the FastAPI router bound to a GraphStore (lazy pattern, §4)."""
    from fastapi import APIRouter, HTTPException

    router = APIRouter(prefix="/api/v1/ragx", tags=["ragx"])
    policy = RAGAbstentionPolicy()

    @router.get("/architectures")
    def list_architectures() -> dict[str, Any]:
        return {
            "architectures": [
                {"name": name, "description": cls.description}
                for name, cls in sorted(ARCHITECTURES.items())
            ],
            "techniques": sorted(ragx_techniques.TECHNIQUES),
            "metrics": sorted(ragx_metrics.METRICS),
        }

    @router.post("/query", response_model=RagxQueryResponse)
    def query_(body: RagxQueryRequest) -> RagxQueryResponse:
        name = body.architecture or _adaptive_architecture(body.query, body.context)
        if name not in ARCHITECTURES:
            raise HTTPException(status_code=404, detail=f"unknown architecture: {name}")
        engine = build_architecture(name, store, policy=policy)
        result = engine.execute(body.query, dict(body.context))
        return RagxQueryResponse(
            architecture=name,
            answer=result.answer,
            confidence=round(result.confidence, 3),
            abstained=result.abstained,
            abstention_reasons=list(result.abstention_reasons),
            sources=list(result.sources),
            highlight_ids=list(result.highlight_ids),
            metadata=dict(result.metadata),
            evidence_manifest=result.evidence_manifest,
        )

    @router.post("/techniques/apply")
    def apply_technique(body: TechniqueRequest) -> dict[str, Any]:
        technique = ragx_techniques.TECHNIQUES.get(body.technique)
        if technique is None:
            raise HTTPException(status_code=404, detail=f"unknown technique: {body.technique}")
        candidates = [c.to_candidate() for c in body.candidates]
        params = dict(body.params)
        try:
            if body.technique in (
                "reciprocal_rank_fusion", "cross_encoder_rerank", "late_interaction",
                "metadata_aware", "context_compression", "evidence_deduplication",
                "diversity_mmr", "parent_child", "contextual_retrieval",
                "contradiction_aware", "confidence_gated", "citation_aware",
                "semantic_chunking", "dynamic_chunking",
            ):
                if body.technique == "reciprocal_rank_fusion":
                    result = technique([candidates], **params)
                elif body.technique in ("semantic_chunking", "dynamic_chunking"):
                    result = technique(body.query or " ".join(c.text for c in candidates), **params)
                elif body.technique == "confidence_gated":
                    result = technique(candidates, policy, store, **params)
                elif body.technique in ("contradiction_aware", "citation_aware"):
                    result = technique(candidates, **params)
                elif body.technique == "contextual_retrieval":
                    ctx = params.pop("contexts", {})
                    result = technique(candidates, lambda cid: ctx.get(cid, ""))
                elif body.technique == "parent_child":
                    parents = params.pop("parents", {})
                    result = technique(candidates, lambda cid: tuple(parents[cid]) if cid in parents else None, **params)
                elif body.technique == "metadata_aware":
                    result = technique(body.query, candidates, **params)
                else:
                    result = technique(candidates, **params)
            elif body.technique in ("query_expansion", "query_decomposition", "step_back", "hyde"):
                result = technique(body.query, **params) if body.technique == "hyde" else technique(body.query, **params)
            elif body.technique in ("recall_at_k",):
                raise HTTPException(status_code=400, detail="metric, not technique")
            else:
                # retriever-callable techniques need a store-backed retriever
                if body.technique in ("rag_fusion", "iterative_rag", "flare", "ircot", "cost_adaptive", "verification_guided", "multi_vector"):
                    engine = build_architecture("local_search", store, policy=policy)

                    def retrieve(q: str, top_k: int) -> list[Candidate]:
                        return engine.search(q, top_k)

                    if body.technique == "verification_guided":
                        result = technique(body.query, retrieve, policy, store, **params)
                    elif body.technique == "multi_vector":
                        fields = params.pop("fields", {})
                        result = technique(body.query, fields, **params)
                    else:
                        result = technique(body.query, retrieve, **params)
                else:
                    raise HTTPException(status_code=400, detail=f"technique '{body.technique}' needs a retriever; not invocable over HTTP")
        except HTTPException:
            raise
        except Exception as exc:  # noqa: BLE001 - surface as 400 with message
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if isinstance(result, list) and result and isinstance(result[0], Candidate):
            return {"technique": body.technique, "candidates": [c.to_dict() for c in result]}
        if isinstance(result, tuple):
            cands, extra = result
            return {
                "technique": body.technique,
                "candidates": [c.to_dict() for c in cands] if isinstance(cands, list) else cands,
                "extra": extra,
            }
        if isinstance(result, list):
            return {"technique": body.technique, "result": result}
        return {"technique": body.technique, "result": result}

    @router.post("/metrics/compute")
    def compute_metric(body: MetricsRequest) -> dict[str, Any]:
        metric = ragx_metrics.METRICS.get(body.metric)
        if metric is None:
            raise HTTPException(status_code=404, detail=f"unknown metric: {body.metric}")
        if body.metric in ("recall_at_k", "precision_at_k"):
            value = metric(body.ranking, set(body.relevant), body.k)
        elif body.metric == "mrr":
            value = metric(body.rankings, [set(r) for r in [set(body.relevant)] * len(body.rankings)])
        elif body.metric == "ndcg_at_k":
            value = metric(body.ranking, body.relevance, body.k)
        elif body.metric == "citation_accuracy":
            value = metric(body.claims)
        else:  # access_control_correctness
            value = metric(body.ranking, set(body.allowed), set(body.denied))
        return {"metric": body.metric, "value": value}

    return router
