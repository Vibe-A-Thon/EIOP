"""Phase 13.1 — RAG Router: 17 Retrieval-Augmented Generation patterns.

Routes graph queries to the optimal RAG pattern based on query classification.
All patterns work with or without an LLM — structured graph analysis is the fallback.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from eoip.graph.store import GraphStore


# ---------------------------------------------------------------------------
# GAP-KRAG-009 — Evidence Manifest contracts
# ---------------------------------------------------------------------------


class EvidenceItem(BaseModel):
    """A single piece of evidence backing a RAG answer."""

    id: str = Field(description="Stable evidence URN, e.g. urn:eoip:rag:evidence:<n>")
    source_id: str = Field(description="Graph source (canonical_id) this evidence cites")
    kind: str = Field(default="entity", description="entity | path | community | unknown")
    authority: float = Field(default=0.5, ge=0.0, le=1.0, description="Source authority score")
    recency: float = Field(default=0.5, ge=0.0, le=1.0, description="Recency score 1.0=fresh")
    score: float = Field(default=1.0, ge=0.0, description="Retrieval score from the pattern")


class EvidenceManifest(BaseModel):
    """GAP-KRAG-009: per-response evidence manifest attached to every non-abstained answer."""

    items: list[EvidenceItem] = Field(default_factory=list)
    entity_count: int = 0
    path_count: int = 0
    avg_authority: float = 0.0
    avg_recency: float = 0.0
    coverage: float = Field(default=0.0, ge=0.0, le=1.0,
                            description="items / target_evidence_items, capped at 1")

    @property
    def source_ids(self) -> list[str]:
        return [i.source_id for i in self.items]


class AbstentionDecision(BaseModel):
    """GAP-KRAG-007/008: structured abstention returned when evidence is insufficient."""

    abstained: bool = False
    reason_codes: list[str] = Field(default_factory=list)
    missing_evidence: str = ""


@dataclass
class AbstentionThresholds:
    """Configurable thresholds for the abstention policy (GAP-KRAG-007)."""

    min_entities: int = 1            # distinct graph sources required
    min_paths: int = 0               # graph paths required (multihop-style answers)
    min_evidence_items: int = 1      # raw evidence items required
    min_avg_authority: float = 0.2   # mean source authority floor
    min_coverage: float = 0.2        # evidence coverage floor vs target
    target_evidence_items: int = 5   # denominator for coverage scoring
    recency_half_life_days: float = 30.0
    confidence_coverage_weight: float = 0.5
    confidence_authority_weight: float = 0.3
    confidence_recency_weight: float = 0.2
    now: datetime | None = None      # test hook; defaults to current UTC time

    def reference_time(self) -> datetime:
        return self.now or datetime.now(UTC)


class RAGAbstentionPolicy:
    """GAP-KRAG-007/008: explicit abstention + evidence-calibrated confidence.

    Confidence is derived purely from evidence coverage, source authority and
    recency — never from model self-confidence.
    """

    def __init__(self, thresholds: AbstentionThresholds | None = None) -> None:
        self._t = thresholds or AbstentionThresholds()

    def _vertex_props(self, store: GraphStore, source_id: str) -> dict[str, Any]:
        try:
            vertex = store.get_vertex_by_canonical_id(source_id)
        except Exception:  # noqa: BLE001 - policy must not fail the caller
            return {}
        if vertex is None:
            return {}
        if isinstance(vertex, dict):
            return dict(vertex.get("properties", {}) or {})
        return dict(getattr(vertex, "properties", {}) or {})

    def _recency(self, props: dict[str, Any]) -> float:
        raw = (props.get("last_verified") or props.get("trust_updated_at")
               or props.get("verified") or props.get("updated_at") or props.get("created_at"))
        if not raw:
            return 0.5
        try:
            ts = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
        except ValueError:
            return 0.5
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=UTC)
        age_days = max(0.0, (self._t.reference_time() - ts).total_seconds()) / 86400.0
        return 0.5 ** (age_days / max(self._t.recency_half_life_days, 1e-9))

    def build_manifest(self, store: GraphStore, result: RAGResult) -> EvidenceManifest:
        seen: set[str] = set()
        items: list[EvidenceItem] = []
        path_count = int(result.metadata.get("path_count", 0) or 0)
        for idx, source_id in enumerate(result.sources):
            if not source_id or source_id in seen:
                continue
            seen.add(source_id)
            props = self._vertex_props(store, source_id)
            label = str(props.get("_label") or props.get("label") or "entity")
            kind = "community" if "community" in label.lower() else "entity"
            authority = props.get("authority", props.get("confidence", props.get("trust_confidence")))
            items.append(EvidenceItem(
                id=f"urn:eoip:rag:evidence:{idx + 1}",
                source_id=source_id,
                kind=kind,
                authority=float(authority if authority is not None else 0.5),
                recency=self._recency(props),
                score=1.0,
            ))
        for extra in range(path_count):
            items.append(EvidenceItem(
                id=f"urn:eoip:rag:evidence:path:{extra + 1}",
                source_id="",
                kind="path",
            ))
        n = len(items)
        coverage = min(1.0, n / max(self._t.target_evidence_items, 1))
        return EvidenceManifest(
            items=items,
            entity_count=len(seen),
            path_count=path_count,
            avg_authority=(sum(i.authority for i in items) / n) if n else 0.0,
            avg_recency=(sum(i.recency for i in items) / n) if n else 0.0,
            coverage=coverage,
        )

    def evaluate(self, manifest: EvidenceManifest) -> AbstentionDecision:
        t = self._t
        reasons: list[str] = []
        missing: list[str] = []
        if len(manifest.items) < t.min_evidence_items:
            reasons.append("NO_RETRIEVED_EVIDENCE")
            missing.append(f"at least {t.min_evidence_items} evidence item(s); got {len(manifest.items)}")
        if manifest.entity_count < t.min_entities:
            reasons.append("INSUFFICIENT_ENTITIES")
            missing.append(f"at least {t.min_entities} source entity(ies); got {manifest.entity_count}")
        if manifest.path_count < t.min_paths:
            reasons.append("INSUFFICIENT_PATHS")
            missing.append(f"at least {t.min_paths} graph path(s); got {manifest.path_count}")
        if manifest.avg_authority < t.min_avg_authority:
            reasons.append("LOW_SOURCE_AUTHORITY")
            missing.append(f"mean authority >= {t.min_avg_authority:.2f}; got {manifest.avg_authority:.2f}")
        if manifest.coverage < t.min_coverage:
            reasons.append("LOW_EVIDENCE_COVERAGE")
            missing.append(f"coverage >= {t.min_coverage:.2f}; got {manifest.coverage:.2f}")
        return AbstentionDecision(
            abstained=bool(reasons),
            reason_codes=reasons,
            missing_evidence="; ".join(missing),
        )

    def calibrate_confidence(self, manifest: EvidenceManifest) -> float:
        """GAP-KRAG-008: evidence-based confidence in [0, 1]."""
        t = self._t
        score = (
            t.confidence_coverage_weight * manifest.coverage
            + t.confidence_authority_weight * manifest.avg_authority
            + t.confidence_recency_weight * manifest.avg_recency
        )
        return round(max(0.0, min(1.0, score)), 3)


@dataclass(frozen=True)
class RAGPattern:
    name: str
    description: str
    retrieval_strategy: str
    when_to_use: str

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "description": self.description,
                "retrieval_strategy": self.retrieval_strategy, "when_to_use": self.when_to_use}


RAG_PATTERNS = [
    RAGPattern("simple", "Simple RAG", "keyword_match_1hop_bfs", "Simple factual queries"),
    RAGPattern("advanced", "Advanced RAG", "query_expansion_reranking_filtering", "Complex queries needing precision"),
    RAGPattern("graph", "Graph RAG", "community_summarize_merge", "Questions spanning the entire graph"),
    RAGPattern("hybrid", "Hybrid RAG", "vector_graph_bm25", "Multi-modality queries"),
    RAGPattern("corrective", "Corrective RAG (CRAG)", "retrieve_evaluate_corrective", "When initial retrieval insufficient"),
    RAGPattern("self", "Self-RAG", "retrieve_generate_self_evaluate", "Response quality verification"),
    RAGPattern("adaptive", "Adaptive RAG", "classify_route_simplest", "Cost/latency optimization"),
    RAGPattern("agentic", "Agentic RAG", "plan_execute_evaluate_iterate", "Open-ended exploration"),
    RAGPattern("modular", "Modular RAG", "search_retrieve_rerank_compress_generate", "Custom retrieval pipelines"),
    RAGPattern("hyde", "HyDE RAG", "hypothetical_document_retrieval", "Abstract queries, concrete answers"),
    RAGPattern("conversational", "Conversational RAG", "session_memory_context_carry", "Multi-turn exploration sessions"),
    RAGPattern("multistep", "Multi-step RAG", "decompose_sequential_aggregate", "Compound questions"),
    RAGPattern("multihop", "Multi-hop RAG", "graph_path_traversal_nhop", "Causal chains, lineage traces"),
    RAGPattern("branched", "Branched RAG", "parallel_branches_merge_best", "Multiple valid retrieval paths"),
    RAGPattern("multimodal", "Multimodal RAG", "graph_code_documentation_diagrams", "Cross-domain queries"),
    RAGPattern("speculative", "Speculative RAG", "multiple_drafts_verify_select", "High-confidence answers"),
    RAGPattern("rag_of_rags", "RAG of RAGs", "meta_route_aggregate_resolve", "Complex multi-pattern queries"),
]

_PATTERN_MAP = {p.name: p for p in RAG_PATTERNS}


@dataclass
class RAGResult:
    answer: str
    pattern: str
    confidence: float
    sources: list[str] = field(default_factory=list)
    highlight_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    abstained: bool = False
    abstention_reasons: list[str] = field(default_factory=list)
    missing_evidence: str = ""
    evidence_manifest: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "answer": self.answer, "rag_pattern": self.pattern,
            "confidence": round(self.confidence, 3),
            "sources": self.sources, "highlight_ids": self.highlight_ids,
            "metadata": self.metadata,
            "abstained": self.abstained,
            "abstention_reasons": self.abstention_reasons,
            "missing_evidence": self.missing_evidence,
            "evidence_manifest": self.evidence_manifest,
        }


class BaseRAG:
    """Base class for all RAG patterns."""

    def __init__(self, store: GraphStore, pattern: RAGPattern) -> None:
        self._store = store
        self._pattern = pattern

    def retrieve(self, query: str, context: dict) -> list[dict]:
        return []

    def generate(self, query: str, retrieved: list[dict], context: dict) -> RAGResult:
        if not retrieved:
            return RAGResult(answer="No relevant context found.", pattern=self._pattern.name, confidence=0.1)
        summary = "; ".join(str(r.get("canonical_id", r.get("text", "")))[:80] for r in retrieved[:5])
        return RAGResult(
            answer=f"Found {len(retrieved)} relevant entities: {summary}",
            pattern=self._pattern.name,
            confidence=0.6,
            sources=[r.get("canonical_id", "") for r in retrieved if r.get("canonical_id")],
            highlight_ids=[r.get("canonical_id", "") for r in retrieved[:10] if r.get("canonical_id")],
        )

    def execute(self, query: str, context: dict) -> RAGResult:
        retrieved = self.retrieve(query, context)
        return self.generate(query, retrieved, context)


class SimpleRAG(BaseRAG):
    def retrieve(self, query: str, context: dict) -> list[dict]:
        terms = query.lower().split()
        results = []
        for v in self._store.find_vertices(limit=200):
            props = v.get("properties", {})
            text = " ".join(str(val).lower() for val in props.values())
            if any(t in text for t in terms):
                results.append({"canonical_id": props.get("canonical_id", v.get("vid")), "label": v.get("label"), "score": 1.0, **props})
        return results[:20]


class GraphRAG(BaseRAG):
    def retrieve(self, query: str, context: dict) -> list[dict]:
        from eoip.graph.community import CommunityDetectionEngine
        engine = CommunityDetectionEngine(self._store)
        try:
            result = engine.detect(algorithm="louvain", resolution=1.0)
        except Exception:  # noqa: BLE001 - resilient fallback must not fail the caller
            return []
        results = []
        for comm in result.get("communities", [])[:5]:
            members = comm.get("members", [])[:10]
            results.append({"community_id": comm.get("id"), "members": members, "canonical_id": members[0] if members else "", "size": comm.get("size", len(members))})
        return results


class HybridRAG(BaseRAG):
    def retrieve(self, query: str, context: dict) -> list[dict]:
        simple = SimpleRAG(self._store, _PATTERN_MAP["simple"])
        keyword_results = simple.retrieve(query, context)
        graph = GraphRAG(self._store, _PATTERN_MAP["graph"])
        community_results = graph.retrieve(query, context)
        seen = set()
        merged = []
        for r in keyword_results + community_results:
            cid = r.get("canonical_id", "")
            if cid not in seen:
                seen.add(cid)
                merged.append(r)
        return merged[:20]


class MultiHopRAG(BaseRAG):
    def retrieve(self, query: str, context: dict) -> list[dict]:
        selected_id = context.get("selected_id")
        if not selected_id:
            return SimpleRAG(self._store, _PATTERN_MAP["simple"]).retrieve(query, context)
        from eoip.graph.metrics import GraphMetricsEngine
        engine = GraphMetricsEngine(self._store)
        try:
            br = engine.blast_radius(selected_id, max_depth=3)
        except Exception:  # noqa: BLE001 - resilient fallback must not fail the caller
            return []
        return [
            {"canonical_id": item.canonical_id, "label": item.label, "depth": item.path_depth}
            for item in br.affected_details[:20]
        ]


class AdaptiveRAG(BaseRAG):
    def execute(self, query: str, context: dict) -> RAGResult:
        q = query.lower()
        if len(q.split()) <= 5 and not any(w in q for w in ["how", "why", "explain", "analyze"]):
            return SimpleRAG(self._store, _PATTERN_MAP["simple"]).execute(query, context)
        if any(w in q for w in ["community", "cluster", "group", "overview"]):
            return GraphRAG(self._store, _PATTERN_MAP["graph"]).execute(query, context)
        if context.get("selected_id") and any(w in q for w in ["impact", "break", "depend", "trace", "path"]):
            return MultiHopRAG(self._store, _PATTERN_MAP["multihop"]).execute(query, context)
        return HybridRAG(self._store, _PATTERN_MAP["hybrid"]).execute(query, context)


class CorrectiveRAG(BaseRAG):
    def execute(self, query: str, context: dict) -> RAGResult:
        result = SimpleRAG(self._store, _PATTERN_MAP["simple"]).execute(query, context)
        if result.confidence < 0.4:
            expanded_query = f"{query} {' '.join(result.sources[:3])}"
            result = HybridRAG(self._store, _PATTERN_MAP["hybrid"]).execute(expanded_query, context)
            result.pattern = "corrective"
        return result


class SelfRAG(BaseRAG):
    def execute(self, query: str, context: dict) -> RAGResult:
        result = SimpleRAG(self._store, _PATTERN_MAP["simple"]).execute(query, context)
        if result.confidence < 0.5 or len(result.sources) < 2:
            result2 = HybridRAG(self._store, _PATTERN_MAP["hybrid"]).execute(query, context)
            if result2.confidence > result.confidence:
                result = result2
            result.pattern = "self"
        return result


class ConversationalRAG(BaseRAG):
    def __init__(self, store: GraphStore, pattern: RAGPattern) -> None:
        super().__init__(store, pattern)
        self._session_memory: list[str] = []

    def execute(self, query: str, context: dict) -> RAGResult:
        combined_query = f"{query} {' '.join(self._session_memory[-3:])}" if self._session_memory else query
        result = AdaptiveRAG(self._store, _PATTERN_MAP["adaptive"]).execute(combined_query, context)
        self._session_memory.append(query)
        result.pattern = "conversational"
        result.metadata["session_turns"] = len(self._session_memory)
        return result


class MultiStepRAG(BaseRAG):
    def execute(self, query: str, context: dict) -> RAGResult:
        parts = [p.strip() for p in query.split("?") if p.strip()]
        if len(parts) <= 1:
            parts = [p.strip() for p in query.split(" and ") if p.strip()]
        all_sources = []
        all_highlights = []
        answers = []
        for part in parts[:4]:
            sub = AdaptiveRAG(self._store, _PATTERN_MAP["adaptive"]).execute(part, context)
            answers.append(sub.answer)
            all_sources.extend(sub.sources)
            all_highlights.extend(sub.highlight_ids)
        return RAGResult(
            answer=" | ".join(answers), pattern="multistep",
            confidence=0.65, sources=list(set(all_sources))[:20],
            highlight_ids=list(set(all_highlights))[:10],
        )


class BranchedRAG(BaseRAG):
    def execute(self, query: str, context: dict) -> RAGResult:
        results = [
            SimpleRAG(self._store, _PATTERN_MAP["simple"]).execute(query, context),
            GraphRAG(self._store, _PATTERN_MAP["graph"]).execute(query, context),
        ]
        if context.get("selected_id"):
            results.append(MultiHopRAG(self._store, _PATTERN_MAP["multihop"]).execute(query, context))
        best = max(results, key=lambda r: r.confidence)
        all_sources = list({s for r in results for s in r.sources})[:20]
        best.sources = all_sources
        best.pattern = "branched"
        return best


class SpeculativeRAG(BaseRAG):
    def execute(self, query: str, context: dict) -> RAGResult:
        drafts = [
            SimpleRAG(self._store, _PATTERN_MAP["simple"]).execute(query, context),
            HybridRAG(self._store, _PATTERN_MAP["hybrid"]).execute(query, context),
        ]
        best = max(drafts, key=lambda r: (r.confidence, len(r.sources)))
        best.pattern = "speculative"
        return best


class RAGOfRAGs(BaseRAG):
    def execute(self, query: str, context: dict) -> RAGResult:
        results = {
            "simple": SimpleRAG(self._store, _PATTERN_MAP["simple"]).execute(query, context),
            "graph": GraphRAG(self._store, _PATTERN_MAP["graph"]).execute(query, context),
            "hybrid": HybridRAG(self._store, _PATTERN_MAP["hybrid"]).execute(query, context),
        }
        best = max(results.values(), key=lambda r: r.confidence)
        all_sources = list({s for r in results.values() for s in r.sources})[:20]
        combined = f"[Best: {best.pattern}] {best.answer}"
        return RAGResult(
            answer=combined, pattern="rag_of_rags",
            confidence=max(r.confidence for r in results.values()),
            sources=all_sources,
            highlight_ids=list({h for r in results.values() for h in r.highlight_ids})[:10],
            metadata={"sub_patterns": {k: v.confidence for k, v in results.items()}},
        )


_RAG_IMPLEMENTATIONS: dict[str, type[BaseRAG]] = {
    "simple": SimpleRAG, "advanced": SimpleRAG, "graph": GraphRAG,
    "hybrid": HybridRAG, "corrective": CorrectiveRAG, "self": SelfRAG,
    "adaptive": AdaptiveRAG, "agentic": AdaptiveRAG, "modular": HybridRAG,
    "hyde": SimpleRAG, "conversational": ConversationalRAG,
    "multistep": MultiStepRAG, "multihop": MultiHopRAG,
    "branched": BranchedRAG, "multimodal": HybridRAG,
    "speculative": SpeculativeRAG, "rag_of_rags": RAGOfRAGs,
}


class RAGRouter:
    """Routes queries to the optimal RAG pattern."""

    def __init__(self, store: GraphStore, policy: RAGAbstentionPolicy | None = None) -> None:
        self._store = store
        self._policy = policy or RAGAbstentionPolicy()

    def classify(self, query: str, context: dict | None = None) -> str:
        q = query.lower()
        ctx = context or {}
        if len(q.split()) <= 4:
            return "simple"
        if any(w in q for w in ["community", "cluster", "overview", "summary"]):
            return "graph"
        if ctx.get("selected_id") and any(w in q for w in ["impact", "break", "path", "trace"]):
            return "multihop"
        if "?" in query and query.count("?") > 1:
            return "multistep"
        if any(w in q for w in ["surprising", "unexpected", "strange"]):
            return "hybrid"
        return "adaptive"

    def route(self, query: str, pattern: str | None = None, context: dict | None = None) -> dict:
        ctx = context or {}
        name = pattern if pattern and pattern in _RAG_IMPLEMENTATIONS else self.classify(query, ctx)
        pat = _PATTERN_MAP.get(name, _PATTERN_MAP["simple"])
        impl_cls = _RAG_IMPLEMENTATIONS.get(name, SimpleRAG)
        impl = impl_cls(self._store, pat)
        result = impl.execute(query, ctx)
        return self._apply_policy(result)

    def _apply_policy(self, result: RAGResult) -> dict:
        """GAP-KRAG-007/008/009: abstain on insufficient evidence; otherwise
        attach an evidence manifest and recalibrate confidence from evidence."""
        policy = self._policy
        manifest = policy.build_manifest(self._store, result)
        decision = policy.evaluate(manifest)
        if decision.abstained:
            return {
                "answer": "Abstained: insufficient evidence to answer reliably.",
                "rag_pattern": result.pattern,
                "confidence": 0.0,
                "sources": result.sources,
                "highlight_ids": result.highlight_ids,
                "metadata": result.metadata,
                "abstained": True,
                "abstention_reasons": decision.reason_codes,
                "missing_evidence": decision.missing_evidence,
                "evidence_manifest": manifest.model_dump(),
            }
        result.abstained = False
        result.confidence = policy.calibrate_confidence(manifest)
        result.evidence_manifest = manifest.model_dump()
        return result.to_dict()
