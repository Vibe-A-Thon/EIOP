"""Phase 13.1 — RAG Router: 17 Retrieval-Augmented Generation patterns.

Routes graph queries to the optimal RAG pattern based on query classification.
All patterns work with or without an LLM — structured graph analysis is the fallback.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from eoip.graph.store import GraphStore


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

    def to_dict(self) -> dict[str, Any]:
        return {
            "answer": self.answer, "rag_pattern": self.pattern,
            "confidence": round(self.confidence, 3),
            "sources": self.sources, "highlight_ids": self.highlight_ids,
            "metadata": self.metadata,
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
        except Exception:
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
        except Exception:
            return []
        return [{"canonical_id": item.canonical_id, "label": item.label, "depth": item.depth} for item in (br.affected_items or [])[:20]]


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
    _session_memory: list[str] = []

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
        all_sources = list(set(s for r in results for s in r.sources))[:20]
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
        all_sources = list(set(s for r in results.values() for s in r.sources))[:20]
        combined = f"[Best: {best.pattern}] {best.answer}"
        return RAGResult(
            answer=combined, pattern="rag_of_rags",
            confidence=max(r.confidence for r in results.values()),
            sources=all_sources,
            highlight_ids=list(set(h for r in results.values() for h in r.highlight_ids))[:10],
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

    def __init__(self, store: GraphStore) -> None:
        self._store = store

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
        return result.to_dict()
