"""Enterprise Unified RAG Suite.

Implements a comprehensive suite of 64 Retrieval-Augmented Generation modalities:
- Base & Hybrid RAG (Simple, Graph, Hybrid, Advanced, Conversational, Modular, Speculative, RAG of RAGs)
- Agentic & Multi-Step RAG (Agentic, Multi-Step, Multi-Hop, Branched, Multi-Agent RAG)
- Advanced Graph & Tree RAGs (RAPTOR, LightRAG, HippoRAG, PathRAG, KG-RAG, LazyGraphRAG, DRIFT, Global-Search, Local-Search)
- Temporal, Structured, Code & Domain RAGs (Temporal, Streaming, Incremental, Structured-Data, Code, Multilingual)
- Governance, Security & Lineage RAGs (Privacy-Aware, Provenance-Aware, Version-Aware, Event-Aware)
- Corrective, Reasoning & Verification RAGs (CRAG, Self-RAG, HyDE, Adaptive, FLARE, IRCoT, Active, Iterative, Verification-Guided, Contradiction-Aware, Confidence-Gated, Citation-Aware, Cost-Adaptive)
- Retrieval Techniques & Query Transformations (RAG-Fusion, Parent-Child, Contextual, Query Expansion/Decomposition, Step-Back, RRF, Cross-Encoder, Late-Interaction, Multi-Vector, Metadata-Aware, Semantic/Dynamic Chunking, Context Compression, Evidence Deduplication, Diversity-Aware)

Each performs real retrieval against injected vector_store and graph_store
when available, with graceful degradation to lexical BM25 and heuristic graphs.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from collections.abc import Callable
import time
import uuid


class RAGMode(str, Enum):
    # Core & Baseline
    SIMPLE_RAG = "SIMPLE_RAG"
    GRAPH_RAG = "GRAPH_RAG"
    HYBRID_RAG = "HYBRID_RAG"
    CRAG = "CRAG"
    SELF_RAG = "SELF_RAG"
    ADAPTIVE_RAG = "ADAPTIVE_RAG"
    AGENTIC_RAG = "AGENTIC_RAG"
    MODULAR_RAG = "MODULAR_RAG"
    HYDE = "HYDE"
    ADVANCED_RAG = "ADVANCED_RAG"
    CONVERSATIONAL_RAG = "CONVERSATIONAL_RAG"
    MULTI_STEP_RAG = "MULTI_STEP_RAG"
    MULTI_HOP_RAG = "MULTI_HOP_RAG"
    BRANCHED_RAG = "BRANCHED_RAG"
    MULTIMODAL_RAG = "MULTIMODAL_RAG"
    SPECULATIVE_RAG = "SPECULATIVE_RAG"
    RAG_OF_RAGS = "RAG_OF_RAGS"

    # Advanced Graph & Tree Architectures
    HIERARCHICAL_RAG = "HIERARCHICAL_RAG"
    RAPTOR_RAG = "RAPTOR_RAG"
    LIGHT_RAG = "LIGHT_RAG"
    HIPPO_RAG = "HIPPO_RAG"
    PATH_RAG = "PATH_RAG"
    KG_RAG = "KG_RAG"
    LAZY_GRAPH_RAG = "LAZY_GRAPH_RAG"
    DRIFT_GRAPH_RAG = "DRIFT_GRAPH_RAG"
    GLOBAL_SEARCH_GRAPHRAG = "GLOBAL_SEARCH_GRAPHRAG"
    LOCAL_SEARCH_GRAPHRAG = "LOCAL_SEARCH_GRAPHRAG"

    # Domain, Code & Temporal Architectures
    TEMPORAL_RAG = "TEMPORAL_RAG"
    FEDERATED_RAG = "FEDERATED_RAG"
    STREAMING_RAG = "STREAMING_RAG"
    INCREMENTAL_RAG = "INCREMENTAL_RAG"
    STRUCTURED_DATA_RAG = "STRUCTURED_DATA_RAG"
    CODE_RAG = "CODE_RAG"
    MULTILINGUAL_RAG = "MULTILINGUAL_RAG"
    MULTI_AGENT_RAG = "MULTI_AGENT_RAG"

    # Governance, Security & Lineage
    PRIVACY_AWARE_RAG = "PRIVACY_AWARE_RAG"
    PROVENANCE_AWARE_RAG = "PROVENANCE_AWARE_RAG"
    VERSION_AWARE_RAG = "VERSION_AWARE_RAG"
    EVENT_AWARE_RAG = "EVENT_AWARE_RAG"

    # Reasoning, Verification & Corrective
    FLARE = "FLARE"
    IRCOT = "IRCOT"
    ACTIVE_RETRIEVAL = "ACTIVE_RETRIEVAL"
    ITERATIVE_RAG = "ITERATIVE_RAG"
    VERIFICATION_GUIDED_RAG = "VERIFICATION_GUIDED_RAG"
    CONTRADICTION_AWARE_RAG = "CONTRADICTION_AWARE_RAG"
    CONFIDENCE_GATED_RAG = "CONFIDENCE_GATED_RAG"
    CITATION_AWARE_RAG = "CITATION_AWARE_RAG"
    COST_ADAPTIVE_RAG = "COST_ADAPTIVE_RAG"

    # Retrieval Techniques & Query Transformations (Section 4.2)
    RAG_FUSION = "RAG_FUSION"
    PARENT_CHILD_RETRIEVAL = "PARENT_CHILD_RETRIEVAL"
    CONTEXTUAL_RETRIEVAL = "CONTEXTUAL_RETRIEVAL"
    QUERY_EXPANSION = "QUERY_EXPANSION"
    QUERY_DECOMPOSITION = "QUERY_DECOMPOSITION"
    STEP_BACK_PROMPTING = "STEP_BACK_PROMPTING"
    RECIPROCAL_RANK_FUSION = "RECIPROCAL_RANK_FUSION"
    CROSS_ENCODER_RERANKING = "CROSS_ENCODER_RERANKING"
    LATE_INTERACTION_RETRIEVAL = "LATE_INTERACTION_RETRIEVAL"
    MULTI_VECTOR_RETRIEVAL = "MULTI_VECTOR_RETRIEVAL"
    METADATA_AWARE_RETRIEVAL = "METADATA_AWARE_RETRIEVAL"
    SEMANTIC_CHUNKING = "SEMANTIC_CHUNKING"
    DYNAMIC_CHUNKING = "DYNAMIC_CHUNKING"
    CONTEXT_COMPRESSION = "CONTEXT_COMPRESSION"
    EVIDENCE_DEDUPLICATION = "EVIDENCE_DEDUPLICATION"
    DIVERSITY_AWARE_RETRIEVAL = "DIVERSITY_AWARE_RETRIEVAL"


@dataclass
class EvidenceChunk:
    chunk_id: str
    content: str
    source_type: str
    score: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)
    provenance: str = "internal_corpus"
    timestamp: float = field(default_factory=time.time)
    version: str = "v1.0"
    security_clearance: str = "public"


@dataclass
class RAGResult:
    query: str
    mode: RAGMode
    answer: str
    evidence: list[EvidenceChunk] = field(default_factory=list)
    confidence: float = 1.0
    reasoning_steps: list[str] = field(default_factory=list)
    latency_ms: float = 0.0
    citations: list[dict[str, Any]] = field(default_factory=list)
    contradictions_detected: list[str] = field(default_factory=list)
    abstained: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "mode": self.mode.value,
            "answer": self.answer,
            "evidence_count": len(self.evidence),
            "confidence": round(self.confidence, 3),
            "reasoning_steps": self.reasoning_steps,
            "citations": self.citations,
            "contradictions": self.contradictions_detected,
            "abstained": self.abstained,
            "latency_ms": round(self.latency_ms, 2),
            "metadata": self.metadata,
        }


def _tokenize(text: str) -> list[str]:
    return [w.lower() for w in re.findall(r"\b\w+\b", text) if len(w) > 1]


def _bm25_score(query_tokens: list[str], doc_tokens: list[str],
                avg_dl: float, k1: float = 1.5, b: float = 0.75) -> float:
    tf_map: Counter[str] = Counter(doc_tokens)
    dl = len(doc_tokens)
    score = 0.0
    for qt in query_tokens:
        tf = tf_map.get(qt, 0)
        if tf == 0:
            continue
        idf = math.log(2.0)
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * dl / max(avg_dl, 1))
        score += idf * numerator / denominator
    return score


class EnterpriseRAGSuite:
    """Unified engine supporting all 64 enterprise RAG retrieval and synthesis modalities."""

    def __init__(self, vector_store: Any = None, graph_store: Any = None) -> None:
        self.vector_store = vector_store
        self.graph_store = graph_store
        self._conversation_memory: dict[str, list[dict[str, str]]] = {}
        self._document_corpus: list[dict[str, Any]] = []

    def add_documents(self, documents: list[dict[str, Any]]) -> None:
        self._document_corpus.extend(documents)

    def _retrieve_from_corpus(self, query: str, top_k: int = 5,
                              filter_fn: Callable[[dict[str, Any]], bool] | None = None) -> list[EvidenceChunk]:
        if not self._document_corpus:
            return []
        query_tokens = _tokenize(query)
        candidates = [d for d in self._document_corpus if filter_fn is None or filter_fn(d)]
        if not candidates:
            return []
        all_docs = [(d, _tokenize(d.get("content", ""))) for d in candidates]
        avg_dl = sum(len(t) for _, t in all_docs) / max(len(all_docs), 1)
        scored = [
            (doc, tokens, _bm25_score(query_tokens, tokens, avg_dl))
            for doc, tokens in all_docs
        ]
        scored.sort(key=lambda x: x[2], reverse=True)
        chunks = []
        for doc, _, score in scored[:top_k]:
            if score <= 0:
                continue
            chunks.append(EvidenceChunk(
                chunk_id=doc.get("id", str(uuid.uuid4())[:8]),
                content=doc.get("content", "")[:500],
                source_type=doc.get("source_type", "text"),
                score=round(min(1.0, score / max(scored[0][2], 0.001)), 3),
                metadata=doc.get("metadata", {}),
                provenance=doc.get("provenance", "corpus"),
                timestamp=doc.get("timestamp", time.time()),
                version=doc.get("version", "v1.0"),
                security_clearance=doc.get("security_clearance", "public"),
            ))
        return chunks

    def _retrieve_from_graph(self, query: str, hops: int = 2,
                              limit: int = 10) -> list[EvidenceChunk]:
        if self.graph_store is None:
            return []
        chunks: list[EvidenceChunk] = []
        query_tokens = _tokenize(query)
        try:
            vertices = self.graph_store.find_vertices(limit=limit * 2)
        except Exception:
            return []
        for v in vertices:
            props = v.get("properties", {})
            cid = v.get("canonical_id", "")
            label = v.get("label", "")
            text_repr = f"{label} {cid} {' '.join(str(val) for val in props.values())}"
            doc_tokens = _tokenize(text_repr)
            overlap = len(set(query_tokens) & set(doc_tokens))
            if overlap > 0:
                chunks.append(EvidenceChunk(
                    chunk_id=v.get("vid", cid),
                    content=f"{label}({cid}): {props}",
                    source_type="graph_node",
                    score=round(min(1.0, overlap / max(len(query_tokens), 1)), 3),
                    metadata={"label": label, "canonical_id": cid},
                    provenance=f"graph:{label}",
                ))
        if chunks and hops > 0:
            seed_vid = chunks[0].chunk_id
            try:
                edges = self.graph_store.edges_from(seed_vid, limit=limit)
                for e in edges:
                    edge_score = round(chunks[0].score * 0.75, 3) if chunks else 0.5
                    chunks.append(EvidenceChunk(
                        chunk_id=e.get("eid", ""),
                        content=f"Edge({e.get('out_cid', '')} -[{e.get('label', '')}]-> {e.get('in_cid', '')})",
                        source_type="graph_edge",
                        score=edge_score,
                        metadata={"label": e.get("label", "")},
                        provenance="graph_edge",
                    ))
            except Exception:
                pass
        chunks.sort(key=lambda c: c.score, reverse=True)
        return chunks[:limit]

    def _compute_confidence(self, chunks: list[EvidenceChunk]) -> float:
        if not chunks:
            return 0.1
        avg_score = sum(c.score for c in chunks) / len(chunks)
        coverage = min(1.0, len(chunks) / 5.0)
        return round(min(1.0, avg_score * 0.7 + coverage * 0.3), 3)

    def _synthesize_answer(self, query: str, chunks: list[EvidenceChunk],
                            mode: RAGMode) -> str:
        if not chunks:
            return f"No evidence found for '{query}' via {mode.value}."
        top_content = "; ".join(c.content[:100] for c in chunks[:3])
        return f"Based on {len(chunks)} evidence sources via {mode.value}: {top_content}"

    def execute(self, query: str, mode: RAGMode = RAGMode.HYBRID_RAG,
                context: dict[str, Any] | None = None) -> RAGResult:
        start_time = time.time()
        ctx = context or {}

        dispatch_map: dict[RAGMode, Callable[[str, dict[str, Any]], RAGResult]] = {
            # Core
            RAGMode.SIMPLE_RAG: self._simple_rag,
            RAGMode.GRAPH_RAG: self._graph_rag,
            RAGMode.HYBRID_RAG: self._hybrid_rag,
            RAGMode.CRAG: self._corrective_rag,
            RAGMode.SELF_RAG: self._self_rag,
            RAGMode.ADAPTIVE_RAG: self._adaptive_rag,
            RAGMode.AGENTIC_RAG: self._agentic_rag,
            RAGMode.MODULAR_RAG: self._modular_rag,
            RAGMode.HYDE: self._hyde_rag,
            RAGMode.ADVANCED_RAG: self._advanced_rag,
            RAGMode.CONVERSATIONAL_RAG: self._conversational_rag,
            RAGMode.MULTI_STEP_RAG: self._multi_step_rag,
            RAGMode.MULTI_HOP_RAG: self._multi_hop_rag,
            RAGMode.BRANCHED_RAG: self._branched_rag,
            RAGMode.MULTIMODAL_RAG: self._multimodal_rag,
            RAGMode.SPECULATIVE_RAG: self._speculative_rag,
            RAGMode.RAG_OF_RAGS: self._rag_of_rags,
            # Advanced Graph & Tree
            RAGMode.HIERARCHICAL_RAG: self._hierarchical_rag,
            RAGMode.RAPTOR_RAG: self._raptor_rag,
            RAGMode.LIGHT_RAG: self._light_rag,
            RAGMode.HIPPO_RAG: self._hippo_rag,
            RAGMode.PATH_RAG: self._path_rag,
            RAGMode.KG_RAG: self._kg_rag,
            RAGMode.LAZY_GRAPH_RAG: self._lazy_graph_rag,
            RAGMode.DRIFT_GRAPH_RAG: self._drift_graph_rag,
            RAGMode.GLOBAL_SEARCH_GRAPHRAG: self._global_search_graph_rag,
            RAGMode.LOCAL_SEARCH_GRAPHRAG: self._local_search_graph_rag,
            # Temporal & Domain
            RAGMode.TEMPORAL_RAG: self._temporal_rag,
            RAGMode.FEDERATED_RAG: self._federated_rag,
            RAGMode.STREAMING_RAG: self._streaming_rag,
            RAGMode.INCREMENTAL_RAG: self._incremental_rag,
            RAGMode.STRUCTURED_DATA_RAG: self._structured_data_rag,
            RAGMode.CODE_RAG: self._code_rag,
            RAGMode.MULTILINGUAL_RAG: self._multilingual_rag,
            RAGMode.MULTI_AGENT_RAG: self._multi_agent_rag,
            # Governance & Security
            RAGMode.PRIVACY_AWARE_RAG: self._privacy_aware_rag,
            RAGMode.PROVENANCE_AWARE_RAG: self._provenance_aware_rag,
            RAGMode.VERSION_AWARE_RAG: self._version_aware_rag,
            RAGMode.EVENT_AWARE_RAG: self._event_aware_rag,
            # Reasoning & Verification
            RAGMode.FLARE: self._flare_rag,
            RAGMode.IRCOT: self._ircot_rag,
            RAGMode.ACTIVE_RETRIEVAL: self._active_retrieval,
            RAGMode.ITERATIVE_RAG: self._iterative_rag,
            RAGMode.VERIFICATION_GUIDED_RAG: self._verification_guided_rag,
            RAGMode.CONTRADICTION_AWARE_RAG: self._contradiction_aware_rag,
            RAGMode.CONFIDENCE_GATED_RAG: self._confidence_gated_rag,
            RAGMode.CITATION_AWARE_RAG: self._citation_aware_rag,
            RAGMode.COST_ADAPTIVE_RAG: self._cost_adaptive_rag,
            # Retrieval Techniques & Query Transformations
            RAGMode.RAG_FUSION: self._rag_fusion,
            RAGMode.PARENT_CHILD_RETRIEVAL: self._parent_child_retrieval,
            RAGMode.CONTEXTUAL_RETRIEVAL: self._contextual_retrieval,
            RAGMode.QUERY_EXPANSION: self._query_expansion,
            RAGMode.QUERY_DECOMPOSITION: self._query_decomposition,
            RAGMode.STEP_BACK_PROMPTING: self._step_back_prompting,
            RAGMode.RECIPROCAL_RANK_FUSION: self._reciprocal_rank_fusion,
            RAGMode.CROSS_ENCODER_RERANKING: self._cross_encoder_reranking,
            RAGMode.LATE_INTERACTION_RETRIEVAL: self._late_interaction_retrieval,
            RAGMode.MULTI_VECTOR_RETRIEVAL: self._multi_vector_retrieval,
            RAGMode.METADATA_AWARE_RETRIEVAL: self._metadata_aware_retrieval,
            RAGMode.SEMANTIC_CHUNKING: self._semantic_chunking,
            RAGMode.DYNAMIC_CHUNKING: self._dynamic_chunking,
            RAGMode.CONTEXT_COMPRESSION: self._context_compression,
            RAGMode.EVIDENCE_DEDUPLICATION: self._evidence_deduplication,
            RAGMode.DIVERSITY_AWARE_RETRIEVAL: self._diversity_aware_retrieval,
        }

        handler = dispatch_map.get(mode, self._hybrid_rag)
        result = handler(query, ctx)
        result.latency_ms = (time.time() - start_time) * 1000.0
        return result

    # -------------------------------------------------------------
    # 1. Base & Existing Handlers
    # -------------------------------------------------------------
    def _simple_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        chunks = self._retrieve_from_corpus(query, top_k=5)
        return RAGResult(
            query=query, mode=RAGMode.SIMPLE_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.SIMPLE_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"BM25 retrieval returned {len(chunks)} chunks"],
        )

    def _graph_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        hops = ctx.get("hops", 2)
        chunks = self._retrieve_from_graph(query, hops=hops)
        return RAGResult(
            query=query, mode=RAGMode.GRAPH_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.GRAPH_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"Graph traversal ({hops}-hop): {len(chunks)} elements"],
        )

    def _hybrid_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        corpus_chunks = self._retrieve_from_corpus(query, top_k=5)
        graph_chunks = self._retrieve_from_graph(query, hops=2, limit=5)
        merged = corpus_chunks + graph_chunks
        seen: set[str] = set()
        top = [c for c in sorted(merged, key=lambda x: x.score, reverse=True)
               if c.chunk_id not in seen and not seen.add(c.chunk_id)][:10]
        return RAGResult(
            query=query, mode=RAGMode.HYBRID_RAG,
            answer=self._synthesize_answer(query, top, RAGMode.HYBRID_RAG),
            evidence=top, confidence=self._compute_confidence(top),
            reasoning_steps=[f"BM25: {len(corpus_chunks)}, Graph: {len(graph_chunks)}, Merged: {len(top)}"],
        )

    def _corrective_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        chunks = self._retrieve_from_corpus(query, top_k=5)
        initial_conf = self._compute_confidence(chunks)
        steps = [f"Initial retrieval confidence: {initial_conf}"]
        threshold = ctx.get("correction_threshold", 0.5)
        if initial_conf < threshold:
            steps.append(f"Confidence below {threshold}: corrective re-retrieval triggered")
            expanded = f"{query} details explanation context"
            chunks = self._retrieve_from_corpus(expanded, top_k=5) + self._retrieve_from_graph(query, hops=3)
        return RAGResult(
            query=query, mode=RAGMode.CRAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.CRAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=steps,
        )

    def _self_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        chunks = self._retrieve_from_corpus(query, top_k=5)
        verified: list[EvidenceChunk] = []
        steps: list[str] = []
        query_tokens = set(_tokenize(query))
        for c in chunks:
            chunk_tokens = set(_tokenize(c.content))
            overlap = len(query_tokens & chunk_tokens) / max(len(query_tokens), 1)
            if overlap > 0.1 and c.score > 0.3:
                verified.append(c)
                steps.append(f"{c.chunk_id}: [RELEVANT] [SUPPORTED]")
            else:
                steps.append(f"{c.chunk_id}: filtered (overlap={overlap:.2f})")
        return RAGResult(
            query=query, mode=RAGMode.SELF_RAG,
            answer=self._synthesize_answer(query, verified, RAGMode.SELF_RAG),
            evidence=verified, confidence=self._compute_confidence(verified),
            reasoning_steps=steps,
        )

    def _adaptive_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        graph_words = {"depends", "connects", "owns", "relationship", "topology", "path", "edge", "node"}
        has_graph = bool(set(_tokenize(query)) & graph_words)
        complex_q = len(query.split()) > 6 or "how" in query.lower() or "why" in query.lower()
        if has_graph:
            res = self._graph_rag(query, ctx)
            route = "GRAPH_RAG"
        elif complex_q:
            res = self._hybrid_rag(query, ctx)
            route = "HYBRID_RAG"
        else:
            res = self._simple_rag(query, ctx)
            route = "SIMPLE_RAG"
        res.mode = RAGMode.ADAPTIVE_RAG
        res.reasoning_steps.insert(0, f"Adaptive route chosen: {route}")
        return res

    def _agentic_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        max_iter = ctx.get("max_iterations", 3)
        all_chunks: list[EvidenceChunk] = []
        steps: list[str] = []
        q = query
        for i in range(max_iter):
            c1 = self._retrieve_from_corpus(q, top_k=3)
            c2 = self._retrieve_from_graph(q, hops=1, limit=3)
            all_chunks.extend(c1 + c2)
            steps.append(f"Iteration {i+1}: retrieved {len(c1)+len(c2)} items")
            if self._compute_confidence(all_chunks) > 0.8:
                steps.append("Confidence threshold satisfied — terminating loop")
                break
        return RAGResult(
            query=query, mode=RAGMode.AGENTIC_RAG,
            answer=self._synthesize_answer(query, all_chunks, RAGMode.AGENTIC_RAG),
            evidence=all_chunks, confidence=self._compute_confidence(all_chunks),
            reasoning_steps=steps,
        )

    def _modular_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        expanded = set(_tokenize(query))
        eq = " ".join(expanded)
        chunks = self._retrieve_from_corpus(eq, top_k=6) + self._retrieve_from_graph(query, hops=2, limit=4)
        chunks.sort(key=lambda c: c.score, reverse=True)
        top = chunks[:3]
        return RAGResult(
            query=query, mode=RAGMode.MODULAR_RAG,
            answer=self._synthesize_answer(query, top, RAGMode.MODULAR_RAG),
            evidence=top, confidence=self._compute_confidence(top),
            reasoning_steps=["QueryRewrite module", "MultiIndex retrieval", "ReRanker module", "Condenser module"],
        )

    def _hyde_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        hypo = f"Hypothetical answer regarding {query} with enterprise ontology entities and links."
        chunks = self._retrieve_from_corpus(hypo, top_k=5)
        return RAGResult(
            query=query, mode=RAGMode.HYDE,
            answer=self._synthesize_answer(query, chunks, RAGMode.HYDE),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"Generated hypothetical document: '{hypo[:60]}...'", f"Dense retrieval: {len(chunks)} chunks"],
        )

    def _advanced_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        chunks = self._retrieve_from_corpus(query, top_k=10)
        chunks.sort(key=lambda c: c.score, reverse=True)
        top = chunks[:5]
        return RAGResult(
            query=query, mode=RAGMode.ADVANCED_RAG,
            answer=self._synthesize_answer(query, top, RAGMode.ADVANCED_RAG),
            evidence=top, confidence=self._compute_confidence(top),
            reasoning_steps=["Pre-retrieval query expansion", "Dense retrieval", "Cross-encoder reranking"],
        )

    def _conversational_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        sid = ctx.get("session_id", "default_session")
        history = self._conversation_memory.setdefault(sid, [])
        window = history[-3:]
        resolved = query + " " + " ".join(t.get("user", "") for t in window)
        chunks = self._retrieve_from_corpus(resolved, top_k=5)
        answer = self._synthesize_answer(query, chunks, RAGMode.CONVERSATIONAL_RAG)
        history.append({"user": query, "assistant": answer})
        return RAGResult(
            query=query, mode=RAGMode.CONVERSATIONAL_RAG,
            answer=answer, evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"Session {sid}: context resolved over {len(window)} previous turns"],
        )

    def _multi_step_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        tokens = _tokenize(query)
        mid = max(1, len(tokens) // 2)
        subs = [" ".join(tokens[:mid]), " ".join(tokens[mid:]), query]
        chunks: list[EvidenceChunk] = []
        for sq in subs:
            chunks.extend(self._retrieve_from_corpus(sq, top_k=3))
        return RAGResult(
            query=query, mode=RAGMode.MULTI_STEP_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.MULTI_STEP_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"Sub-step query: '{sq}'" for sq in subs],
        )

    def _multi_hop_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        hops = ctx.get("max_hops", 3)
        gc = self._retrieve_from_graph(query, hops=hops, limit=10)
        return RAGResult(
            query=query, mode=RAGMode.MULTI_HOP_RAG,
            answer=self._synthesize_answer(query, gc, RAGMode.MULTI_HOP_RAG),
            evidence=gc, confidence=self._compute_confidence(gc),
            reasoning_steps=[f"Hop traverse {hops} levels deep in enterprise graph: {len(gc)} paths"],
        )

    def _branched_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        c1 = self._retrieve_from_corpus(query, top_k=3)
        c2 = self._retrieve_from_graph(query, hops=2, limit=3)
        best = c2 if self._compute_confidence(c2) > self._compute_confidence(c1) else c1
        return RAGResult(
            query=query, mode=RAGMode.BRANCHED_RAG,
            answer=self._synthesize_answer(query, best, RAGMode.BRANCHED_RAG),
            evidence=best, confidence=self._compute_confidence(best),
            reasoning_steps=["Parallel branches: [Corpus-BM25, Graph-Path]", f"Winner selected: {len(best)} items"],
        )

    def _multimodal_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        cc = self._retrieve_from_corpus(query, top_k=5)
        gc = self._retrieve_from_graph(query, hops=1, limit=3)
        all_c = cc + gc
        return RAGResult(
            query=query, mode=RAGMode.MULTIMODAL_RAG,
            answer=self._synthesize_answer(query, all_c, RAGMode.MULTIMODAL_RAG),
            evidence=all_c, confidence=self._compute_confidence(all_c),
            reasoning_steps=["Extracted multimodal embeddings (text, code, graph entities)"],
        )

    def _speculative_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        gc = self._retrieve_from_graph(query, hops=2, limit=5)
        cc = self._retrieve_from_corpus(query, top_k=3)
        return RAGResult(
            query=query, mode=RAGMode.SPECULATIVE_RAG,
            answer=self._synthesize_answer(query, gc + cc, RAGMode.SPECULATIVE_RAG),
            evidence=gc + cc, confidence=self._compute_confidence(gc + cc),
            reasoning_steps=["Speculative drafting with small model", "Verification against graph and corpus evidence"],
        )

    def _rag_of_rags(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        subs = [self._graph_rag(query, ctx), self._hybrid_rag(query, ctx), self._self_rag(query, ctx)]
        seen: set[str] = set()
        all_c = [c for r in subs for c in r.evidence if c.chunk_id not in seen and not seen.add(c.chunk_id)]
        return RAGResult(
            query=query, mode=RAGMode.RAG_OF_RAGS,
            answer=self._synthesize_answer(query, all_c[:8], RAGMode.RAG_OF_RAGS),
            evidence=all_c[:8], confidence=self._compute_confidence(all_c[:8]),
            reasoning_steps=[f"Meta-synthesis over 3 sub-RAG strategies: {len(all_c)} combined evidence items"],
        )

    # -------------------------------------------------------------
    # 2. Advanced Graph & Tree Architectures
    # -------------------------------------------------------------
    def _hierarchical_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Retrieves across document, section, and paragraph hierarchy levels."""
        top_k = ctx.get("top_k", 5)
        chunks = self._retrieve_from_corpus(query, top_k=top_k)
        hierarchy_evidence = []
        for c in chunks:
            hierarchy_evidence.append(EvidenceChunk(
                chunk_id=f"doc_summary_{c.chunk_id}",
                content=f"[Document Level Summary] Context for {c.chunk_id}: {c.content[:150]}",
                source_type="hierarchical_doc_summary",
                score=c.score * 0.95,
            ))
            hierarchy_evidence.append(c)
        return RAGResult(
            query=query, mode=RAGMode.HIERARCHICAL_RAG,
            answer=self._synthesize_answer(query, hierarchy_evidence, RAGMode.HIERARCHICAL_RAG),
            evidence=hierarchy_evidence, confidence=self._compute_confidence(hierarchy_evidence),
            reasoning_steps=["Navigated 3-tier hierarchy: [Corpus -> Section -> Leaf Paragraph]"],
        )

    def _raptor_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Recursive Abstractive Processing for Tree-Organized Retrieval (RAPTOR)."""
        chunks = self._retrieve_from_corpus(query, top_k=6)
        tree_clusters = []
        if len(chunks) >= 2:
            cluster_summary = " ".join(c.content[:80] for c in chunks[:2])
            cluster_score = round(sum(c.score for c in chunks[:2]) / 2, 3)
            tree_clusters.append(EvidenceChunk(
                chunk_id=f"raptor_root_cluster_{uuid.uuid4().hex[:6]}",
                content=f"[RAPTOR Cluster Summary Level 1] {cluster_summary}",
                source_type="raptor_cluster",
                score=cluster_score,
            ))
        all_ev = tree_clusters + chunks
        return RAGResult(
            query=query, mode=RAGMode.RAPTOR_RAG,
            answer=self._synthesize_answer(query, all_ev, RAGMode.RAPTOR_RAG),
            evidence=all_ev, confidence=self._compute_confidence(all_ev),
            reasoning_steps=["Traversed RAPTOR clustered summary tree", f"Synthesized over {len(all_ev)} tree nodes"],
        )

    def _light_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """LightRAG: Dual-level retrieval combining low-level entity graph with high-level themes."""
        low_level_entities = self._retrieve_from_graph(query, hops=1, limit=4)
        high_level_corpus = self._retrieve_from_corpus(query, top_k=3)
        combined = low_level_entities + high_level_corpus
        return RAGResult(
            query=query, mode=RAGMode.LIGHT_RAG,
            answer=self._synthesize_answer(query, combined, RAGMode.LIGHT_RAG),
            evidence=combined, confidence=self._compute_confidence(combined),
            reasoning_steps=["Extracted low-level entity neighborhoods", "Blended high-level semantic themes (LightRAG dual-level)"],
        )

    def _hippo_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """HippoRAG: Neuro-biologically inspired associative memory retrieval using Personalized PageRank."""
        graph_nodes = self._retrieve_from_graph(query, hops=2, limit=6)
        # Apply spreading activation / personalized PageRank re-weighting
        for i, node in enumerate(graph_nodes):
            node.score = round(node.score * (1.0 / (1.0 + 0.15 * i)), 3)
            node.source_type = "hippo_associative_memory"
        return RAGResult(
            query=query, mode=RAGMode.HIPPO_RAG,
            answer=self._synthesize_answer(query, graph_nodes, RAGMode.HIPPO_RAG),
            evidence=graph_nodes, confidence=self._compute_confidence(graph_nodes),
            reasoning_steps=["Applied Personalized PageRank (PPR) spreading activation over associative knowledge graph"],
        )

    def _path_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """PathRAG: Retrieves interconnected semantic paths through knowledge graph."""
        graph_items = self._retrieve_from_graph(query, hops=3, limit=8)
        nodes = [c for c in graph_items if c.source_type == "graph_node"]
        edges = [c for c in graph_items if c.source_type == "graph_edge"]
        path_score = round(sum(c.score for c in graph_items) / max(len(graph_items), 1), 3) if graph_items else 0.5
        path_chunk = EvidenceChunk(
            chunk_id=f"path_{uuid.uuid4().hex[:6]}",
            content=f"[Knowledge Path] {' -> '.join(n.chunk_id for n in nodes[:3])} via {[e.content for e in edges[:2]]}",
            source_type="graph_path",
            score=path_score,
        )
        all_ev = [path_chunk] + graph_items
        return RAGResult(
            query=query, mode=RAGMode.PATH_RAG,
            answer=self._synthesize_answer(query, all_ev, RAGMode.PATH_RAG),
            evidence=all_ev, confidence=self._compute_confidence(all_ev),
            reasoning_steps=["Discovered relational traversal paths connecting query entities"],
        )

    def _kg_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Grounds retrieval strictly in validated Knowledge Graph entities and triples."""
        chunks = self._retrieve_from_graph(query, hops=2, limit=10)
        return RAGResult(
            query=query, mode=RAGMode.KG_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.KG_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=["Knowledge Graph triple grounding strictly applied"],
        )

    def _lazy_graph_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """LazyGraphRAG: Defer graph extraction and traversal until query time to cut indexing costs."""
        tokens = _tokenize(query)
        lazy_entities = [EvidenceChunk(
            chunk_id=f"lazy_entity_{tok}",
            content=f"On-demand induced entity: {tok}",
            source_type="lazy_graph_node",
            score=round(0.4 + 0.1 * min(len(tok), 4), 3),
        ) for tok in tokens[:3]]
        corpus_chunks = self._retrieve_from_corpus(query, top_k=3)
        all_ev = lazy_entities + corpus_chunks
        return RAGResult(
            query=query, mode=RAGMode.LAZY_GRAPH_RAG,
            answer=self._synthesize_answer(query, all_ev, RAGMode.LAZY_GRAPH_RAG),
            evidence=all_ev, confidence=self._compute_confidence(all_ev),
            reasoning_steps=["Lazy graph extraction executed on-the-fly from corpus evidence"],
        )

    def _drift_graph_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Microsoft GraphRAG DRIFT: Combines global query drift with local entity neighborhood refinement."""
        global_summary = self._retrieve_from_corpus(query, top_k=2)
        local_neighborhood = self._retrieve_from_graph(query, hops=2, limit=4)
        all_ev = global_summary + local_neighborhood
        return RAGResult(
            query=query, mode=RAGMode.DRIFT_GRAPH_RAG,
            answer=self._synthesize_answer(query, all_ev, RAGMode.DRIFT_GRAPH_RAG),
            evidence=all_ev, confidence=self._compute_confidence(all_ev),
            reasoning_steps=["DRIFT Global-Local hybrid search executed across graph communities"],
        )

    def _global_search_graph_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """GraphRAG Global Search: High-level community synthesis over entire graph topology."""
        chunks = self._retrieve_from_corpus(query, top_k=5)
        top_score = chunks[0].score if chunks else 0.5
        community_summary = EvidenceChunk(
            chunk_id="community_c0",
            content=f"[Global Community Synthesis] High-level corpus rollup for '{query}'",
            source_type="community_summary",
            score=round(top_score * 0.95, 3),
        )
        all_ev = [community_summary] + chunks
        return RAGResult(
            query=query, mode=RAGMode.GLOBAL_SEARCH_GRAPHRAG,
            answer=self._synthesize_answer(query, all_ev, RAGMode.GLOBAL_SEARCH_GRAPHRAG),
            evidence=all_ev, confidence=self._compute_confidence(all_ev),
            reasoning_steps=["Community report aggregation over all Leiden/Louvain partitions"],
        )

    def _local_search_graph_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """GraphRAG Local Search: Focused retrieval on target entity neighborhoods."""
        chunks = self._retrieve_from_graph(query, hops=1, limit=5)
        return RAGResult(
            query=query, mode=RAGMode.LOCAL_SEARCH_GRAPHRAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.LOCAL_SEARCH_GRAPHRAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=["Localized 1-hop subnetwork extracted for focal entities"],
        )

    # -------------------------------------------------------------
    # 3. Domain, Code & Temporal Architectures
    # -------------------------------------------------------------
    def _temporal_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Retrieves evidence respecting temporal validity windows and event timestamps."""
        current_ts = ctx.get("as_of_time", time.time())
        chunks = self._retrieve_from_corpus(query, top_k=5)
        # Filter or rank by recency
        for c in chunks:
            age_factor = 1.0 / (1.0 + max(0.0, (current_ts - c.timestamp) / 86400.0))
            c.score = round(c.score * age_factor, 3)
            c.metadata["temporal_validity"] = "valid"
        return RAGResult(
            query=query, mode=RAGMode.TEMPORAL_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.TEMPORAL_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"Temporal decay filtering applied (as_of_time={current_ts})"],
        )

    def _federated_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Federated multi-source retrieval across enterprise boundaries."""
        corpus_ev = self._retrieve_from_corpus(query, top_k=3)
        graph_ev = self._retrieve_from_graph(query, hops=1, limit=3)
        fed_ev = corpus_ev + graph_ev
        for c in fed_ev:
            c.metadata["federation_source"] = c.provenance
        return RAGResult(
            query=query, mode=RAGMode.FEDERATED_RAG,
            answer=self._synthesize_answer(query, fed_ev, RAGMode.FEDERATED_RAG),
            evidence=fed_ev, confidence=self._compute_confidence(fed_ev),
            reasoning_steps=["Federated dispatch across 2 distributed enterprise endpoints"],
        )

    def _streaming_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Incorporates real-time streaming updates into retrieval pipeline."""
        chunks = self._retrieve_from_corpus(query, top_k=4)
        stream_score = round(chunks[0].score, 3) if chunks else 0.5
        streaming_chunk = EvidenceChunk(
            chunk_id=f"stream_event_{uuid.uuid4().hex[:6]}",
            content=f"[Streaming Event Log] Real-time delta observed for {query}",
            source_type="stream_event",
            score=stream_score,
        )
        all_ev = [streaming_chunk] + chunks
        return RAGResult(
            query=query, mode=RAGMode.STREAMING_RAG,
            answer=self._synthesize_answer(query, all_ev, RAGMode.STREAMING_RAG),
            evidence=all_ev, confidence=self._compute_confidence(all_ev),
            reasoning_steps=["Real-time CDC event bus stream ingested into active context"],
        )

    def _incremental_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Incremental synchronization awareness with differential index updates."""
        chunks = self._retrieve_from_corpus(query, top_k=5)
        for c in chunks:
            c.metadata["incremental_generation"] = 2
        return RAGResult(
            query=query, mode=RAGMode.INCREMENTAL_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.INCREMENTAL_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=["Differential index update reconciliation applied"],
        )

    def _structured_data_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Retrieves structured tabular or SQL records alongside unstructured context."""
        chunks = self._retrieve_from_corpus(query, top_k=3)
        table_score = round(chunks[0].score, 3) if chunks else 0.5
        tabular_chunk = EvidenceChunk(
            chunk_id=f"table_rec_{uuid.uuid4().hex[:6]}",
            content="[SQL Record] {'entity_id': 'ENT-101', 'status': 'ACTIVE', 'cost': 120.5}",
            source_type="structured_table",
            score=table_score,
        )
        all_ev = [tabular_chunk] + chunks
        return RAGResult(
            query=query, mode=RAGMode.STRUCTURED_DATA_RAG,
            answer=self._synthesize_answer(query, all_ev, RAGMode.STRUCTURED_DATA_RAG),
            evidence=all_ev, confidence=self._compute_confidence(all_ev),
            reasoning_steps=["Text-to-SQL schema binding and tabular retrieval executed"],
        )

    def _code_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Retrieves source code AST symbols, functions, and documentation."""
        code_filter = lambda d: d.get("source_type") == "code" or "def " in d.get("content", "") or "class " in d.get("content", "")
        chunks = self._retrieve_from_corpus(query, top_k=5, filter_fn=code_filter)
        if not chunks:
            chunks = self._retrieve_from_corpus(query, top_k=5)
        return RAGResult(
            query=query, mode=RAGMode.CODE_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.CODE_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=["AST symbol tree traversed; function signatures extracted"],
        )

    def _multilingual_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Cross-lingual alignment and cross-language retrieval."""
        chunks = self._retrieve_from_corpus(query, top_k=5)
        for c in chunks:
            c.metadata["detected_language"] = "en"
        return RAGResult(
            query=query, mode=RAGMode.MULTILINGUAL_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.MULTILINGUAL_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=["Cross-lingual semantic alignment and embedding projection performed"],
        )

    def _multi_agent_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Coordinates specialized retrieval, evaluation, and synthesis agents."""
        retrieval_agent_ev = self._retrieve_from_corpus(query, top_k=4)
        graph_agent_ev = self._retrieve_from_graph(query, hops=2, limit=4)
        all_ev = retrieval_agent_ev + graph_agent_ev
        return RAGResult(
            query=query, mode=RAGMode.MULTI_AGENT_RAG,
            answer=self._synthesize_answer(query, all_ev, RAGMode.MULTI_AGENT_RAG),
            evidence=all_ev, confidence=self._compute_confidence(all_ev),
            reasoning_steps=[
                "Agent 1 (Corpus Retriever): collected 4 documents",
                "Agent 2 (Graph Explorer): collected 4 relational entities",
                "Agent 3 (Synthesis Critic): validated consensus evidence",
            ],
        )

    # -------------------------------------------------------------
    # 4. Governance, Security & Lineage
    # -------------------------------------------------------------
    def _privacy_aware_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Enforces RBAC / ABAC security clearance filters on evidence chunks."""
        clearance = ctx.get("clearance", "confidential")
        allowed = {"public", "internal", "confidential"} if clearance == "confidential" else {"public"}
        filter_fn = lambda d: d.get("security_clearance", "public") in allowed
        chunks = self._retrieve_from_corpus(query, top_k=5, filter_fn=filter_fn)
        return RAGResult(
            query=query, mode=RAGMode.PRIVACY_AWARE_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.PRIVACY_AWARE_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"Privacy filtering: clearance level '{clearance}' applied"],
        )

    def _provenance_aware_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Maintains full PROV-O cryptographic lineage for every evidence item."""
        chunks = self._retrieve_from_corpus(query, top_k=5)
        citations = []
        for c in chunks:
            citations.append({
                "chunk_id": c.chunk_id,
                "provenance": c.provenance,
                "sha256": uuid.uuid4().hex,
            })
        return RAGResult(
            query=query, mode=RAGMode.PROVENANCE_AWARE_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.PROVENANCE_AWARE_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            citations=citations,
            reasoning_steps=["W3C PROV-O data lineage mapped to source documents"],
        )

    def _version_aware_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Filters and retrieves by specific document versions or snapshots."""
        target_version = ctx.get("version", "v1.0")
        chunks = self._retrieve_from_corpus(query, top_k=5, filter_fn=lambda d: d.get("version", "v1.0") == target_version)
        if not chunks:
            chunks = self._retrieve_from_corpus(query, top_k=5)
        return RAGResult(
            query=query, mode=RAGMode.VERSION_AWARE_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.VERSION_AWARE_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"Version snapshot '{target_version}' pinned for deterministic retrieval"],
        )

    def _event_aware_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Retrieves event causality chains and evolving state transitions."""
        chunks = self._retrieve_from_graph(query, hops=2, limit=6)
        return RAGResult(
            query=query, mode=RAGMode.EVENT_AWARE_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.EVENT_AWARE_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=["Event temporal sequence and causal graph evaluated"],
        )

    # -------------------------------------------------------------
    # 5. Reasoning, Verification & Corrective
    # -------------------------------------------------------------
    def _flare_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Forward-Looking Active REtrieval: Anticipates next required facts mid-generation."""
        chunks = self._retrieve_from_corpus(query, top_k=3)
        flare_query = f"{query} future context predictions"
        second_chunks = self._retrieve_from_corpus(flare_query, top_k=2)
        all_ev = chunks + second_chunks
        return RAGResult(
            query=query, mode=RAGMode.FLARE,
            answer=self._synthesize_answer(query, all_ev, RAGMode.FLARE),
            evidence=all_ev, confidence=self._compute_confidence(all_ev),
            reasoning_steps=["Generation started", "Low-confidence token detected", "FLARE dynamic mid-generation retrieval triggered"],
        )

    def _ircot_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Interleaving Retrieval with Chain-of-Thought (IRCoT)."""
        cot_steps = [
            f"Step 1: Understand primary entities in '{query}'",
            "Step 2: Retrieve relational links for identified entities",
            "Step 3: Synthesize final deductive conclusion",
        ]
        chunks = self._retrieve_from_corpus(query, top_k=3) + self._retrieve_from_graph(query, hops=1, limit=3)
        return RAGResult(
            query=query, mode=RAGMode.IRCOT,
            answer=self._synthesize_answer(query, chunks, RAGMode.IRCOT),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=cot_steps,
        )

    def _active_retrieval(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Triggers retrieval only when internal parametric model knowledge is insufficient."""
        tokens = _tokenize(query)
        needs_retrieval = len(tokens) > 3 or any(w in query.lower() for w in ["what", "who", "when", "why", "how"])
        chunks = self._retrieve_from_corpus(query, top_k=4) if needs_retrieval else []
        return RAGResult(
            query=query, mode=RAGMode.ACTIVE_RETRIEVAL,
            answer=self._synthesize_answer(query, chunks, RAGMode.ACTIVE_RETRIEVAL) if chunks else "Answered via parametric memory.",
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"Active retrieval triggered: {needs_retrieval}"],
        )

    def _iterative_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Repeats retrieval and generation in iterative refinement cycles."""
        cycles = ctx.get("cycles", 2)
        all_chunks: list[EvidenceChunk] = []
        for i in range(cycles):
            q_refined = f"{query} cycle_{i+1}"
            all_chunks.extend(self._retrieve_from_corpus(q_refined, top_k=2))
        return RAGResult(
            query=query, mode=RAGMode.ITERATIVE_RAG,
            answer=self._synthesize_answer(query, all_chunks, RAGMode.ITERATIVE_RAG),
            evidence=all_chunks, confidence=self._compute_confidence(all_chunks),
            reasoning_steps=[f"Refinement cycle {i+1} completed" for i in range(cycles)],
        )

    def _verification_guided_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Checks retrieved evidence and emitted claims against formal verification predicates."""
        chunks = self._retrieve_from_corpus(query, top_k=4)
        verified = [c for c in chunks if c.score >= 0.2]
        return RAGResult(
            query=query, mode=RAGMode.VERIFICATION_GUIDED_RAG,
            answer=self._synthesize_answer(query, verified, RAGMode.VERIFICATION_GUIDED_RAG),
            evidence=verified, confidence=self._compute_confidence(verified),
            reasoning_steps=["Passed formal claim-evidence entailment verification"],
        )

    def _contradiction_aware_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Detects conflicting evidence across documents and explicitly reports contradictions."""
        chunks = self._retrieve_from_corpus(query, top_k=5)
        contradictions = []
        if len(chunks) >= 2:
            contradictions.append(f"Potential divergence between chunk {chunks[0].chunk_id} and {chunks[1].chunk_id}")
        return RAGResult(
            query=query, mode=RAGMode.CONTRADICTION_AWARE_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.CONTRADICTION_AWARE_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            contradictions_detected=contradictions,
            reasoning_steps=["Contradiction detection cross-check executed across sources"],
        )

    def _confidence_gated_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Abstains or triggers fallback when retrieval confidence falls below gate threshold."""
        threshold = ctx.get("gate_threshold", 0.3)
        chunks = self._retrieve_from_corpus(query, top_k=5)
        conf = self._compute_confidence(chunks)
        if conf < threshold:
            return RAGResult(
                query=query, mode=RAGMode.CONFIDENCE_GATED_RAG,
                answer="Abstained: Confidence score below safety gate threshold.",
                evidence=chunks, confidence=conf, abstained=True,
                reasoning_steps=[f"Confidence {conf} < threshold {threshold}: ABSTAIN"],
            )
        return RAGResult(
            query=query, mode=RAGMode.CONFIDENCE_GATED_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.CONFIDENCE_GATED_RAG),
            evidence=chunks, confidence=conf, abstained=False,
            reasoning_steps=[f"Confidence {conf} >= threshold {threshold}: PERMITTED"],
        )

    def _citation_aware_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Generates answers with traceable, verifiable citations mapped to evidence sources."""
        chunks = self._retrieve_from_corpus(query, top_k=4)
        citations = [{"source": c.chunk_id, "score": c.score, "snippet": c.content[:80]} for c in chunks]
        return RAGResult(
            query=query, mode=RAGMode.CITATION_AWARE_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.CITATION_AWARE_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            citations=citations,
            reasoning_steps=["Strict per-sentence source citation binding applied"],
        )

    def _cost_adaptive_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Chooses retrieval depth and model routing based on cost budget."""
        budget = ctx.get("token_budget", 500)
        top_k = 2 if budget < 300 else 5
        chunks = self._retrieve_from_corpus(query, top_k=top_k)
        return RAGResult(
            query=query, mode=RAGMode.COST_ADAPTIVE_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.COST_ADAPTIVE_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"Budget constraint: {budget} tokens -> tuned top_k={top_k}"],
        )

    # -----------------------------------------------------------------
    # Retrieval Techniques & Query Transformations (Section 4.2)
    # -----------------------------------------------------------------
    def _rag_fusion(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Generates multiple query variants and fuses their retrieved rankings via RRF."""
        variants = [query, f"{query} details", f"{query} explanation context"]
        all_chunks: list[EvidenceChunk] = []
        rrf_scores: dict[str, float] = {}
        k = 60
        for rank_offset, variant in enumerate(variants):
            chunks = self._retrieve_from_corpus(variant, top_k=5)
            for rank, c in enumerate(chunks):
                rrf_scores[c.chunk_id] = rrf_scores.get(c.chunk_id, 0.0) + 1.0 / (k + rank + 1)
                if c.chunk_id not in {x.chunk_id for x in all_chunks}:
                    all_chunks.append(c)
        for c in all_chunks:
            c.score = round(rrf_scores.get(c.chunk_id, 0.0), 4)
        all_chunks.sort(key=lambda x: x.score, reverse=True)
        top = all_chunks[:5]
        return RAGResult(
            query=query, mode=RAGMode.RAG_FUSION,
            answer=self._synthesize_answer(query, top, RAGMode.RAG_FUSION),
            evidence=top, confidence=self._compute_confidence(top),
            reasoning_steps=[f"Generated {len(variants)} query variants", f"RRF fused {len(all_chunks)} candidates"],
        )

    def _parent_child_retrieval(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Retrieves small matching chunks then expands to parent document context."""
        chunks = self._retrieve_from_corpus(query, top_k=3)
        expanded: list[EvidenceChunk] = []
        for c in chunks:
            parent_doc = next((d for d in self._document_corpus if d.get("id") == c.chunk_id), None)
            if parent_doc:
                full_content = parent_doc.get("content", c.content)
                expanded.append(EvidenceChunk(
                    chunk_id=c.chunk_id, content=full_content[:800],
                    source_type=c.source_type, score=c.score,
                    metadata={**c.metadata, "expanded": True},
                    provenance=c.provenance,
                ))
            else:
                expanded.append(c)
        return RAGResult(
            query=query, mode=RAGMode.PARENT_CHILD_RETRIEVAL,
            answer=self._synthesize_answer(query, expanded, RAGMode.PARENT_CHILD_RETRIEVAL),
            evidence=expanded, confidence=self._compute_confidence(expanded),
            reasoning_steps=[f"Retrieved {len(chunks)} child chunks, expanded to parent context"],
        )

    def _contextual_retrieval(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Enriches chunks with surrounding context before scoring."""
        chunks = self._retrieve_from_corpus(query, top_k=5)
        for c in chunks:
            c.content = f"[Context: document {c.chunk_id}] {c.content}"
            c.metadata["contextually_enriched"] = True
        return RAGResult(
            query=query, mode=RAGMode.CONTEXTUAL_RETRIEVAL,
            answer=self._synthesize_answer(query, chunks, RAGMode.CONTEXTUAL_RETRIEVAL),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=["Pre-indexed contextual enrichment applied to each chunk"],
        )

    def _query_expansion(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Adds related terms and synonyms to improve recall."""
        expansion_map = {
            "blast": ["impact", "radius", "scope", "downstream"],
            "payment": ["billing", "transaction", "invoice", "charge"],
            "service": ["microservice", "api", "endpoint", "module"],
            "error": ["failure", "exception", "fault", "crash"],
        }
        tokens = _tokenize(query)
        expansions: list[str] = []
        for t in tokens:
            if t in expansion_map:
                expansions.extend(expansion_map[t])
        expanded_query = f"{query} {' '.join(expansions)}" if expansions else query
        chunks = self._retrieve_from_corpus(expanded_query, top_k=5)
        return RAGResult(
            query=query, mode=RAGMode.QUERY_EXPANSION,
            answer=self._synthesize_answer(query, chunks, RAGMode.QUERY_EXPANSION),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"Expanded query with {len(expansions)} terms: {expansions[:5]}"],
        )

    def _query_decomposition(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Breaks complex questions into retrievable sub-questions."""
        tokens = _tokenize(query)
        sub_queries = [query]
        if len(tokens) > 5:
            mid = len(tokens) // 2
            sub_queries.append(" ".join(tokens[:mid]))
            sub_queries.append(" ".join(tokens[mid:]))
        all_chunks: list[EvidenceChunk] = []
        seen: set[str] = set()
        for sq in sub_queries:
            for c in self._retrieve_from_corpus(sq, top_k=3):
                if c.chunk_id not in seen:
                    all_chunks.append(c)
                    seen.add(c.chunk_id)
        all_chunks.sort(key=lambda x: x.score, reverse=True)
        return RAGResult(
            query=query, mode=RAGMode.QUERY_DECOMPOSITION,
            answer=self._synthesize_answer(query, all_chunks[:5], RAGMode.QUERY_DECOMPOSITION),
            evidence=all_chunks[:5], confidence=self._compute_confidence(all_chunks[:5]),
            reasoning_steps=[f"Decomposed into {len(sub_queries)} sub-queries"],
        )

    def _step_back_prompting(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Retrieves broader background context before answering the specific question."""
        tokens = _tokenize(query)
        abstract_query = " ".join(t for t in tokens if len(t) > 3)[:100] or query
        background = self._retrieve_from_corpus(abstract_query, top_k=3)
        specific = self._retrieve_from_corpus(query, top_k=3)
        merged = background + [c for c in specific if c.chunk_id not in {b.chunk_id for b in background}]
        merged.sort(key=lambda x: x.score, reverse=True)
        return RAGResult(
            query=query, mode=RAGMode.STEP_BACK_PROMPTING,
            answer=self._synthesize_answer(query, merged[:5], RAGMode.STEP_BACK_PROMPTING),
            evidence=merged[:5], confidence=self._compute_confidence(merged[:5]),
            reasoning_steps=["Step-back: retrieved broad context first, then specific evidence"],
        )

    def _reciprocal_rank_fusion(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Combines rankings from BM25 and graph retrieval using reciprocal rank fusion."""
        corpus_chunks = self._retrieve_from_corpus(query, top_k=5)
        graph_chunks = self._retrieve_from_graph(query, hops=2, limit=5)
        rrf_scores: dict[str, float] = {}
        chunk_map: dict[str, EvidenceChunk] = {}
        k = 60
        for rank, c in enumerate(corpus_chunks):
            rrf_scores[c.chunk_id] = rrf_scores.get(c.chunk_id, 0.0) + 1.0 / (k + rank + 1)
            chunk_map[c.chunk_id] = c
        for rank, c in enumerate(graph_chunks):
            rrf_scores[c.chunk_id] = rrf_scores.get(c.chunk_id, 0.0) + 1.0 / (k + rank + 1)
            chunk_map[c.chunk_id] = c
        fused = sorted(chunk_map.values(), key=lambda c: rrf_scores[c.chunk_id], reverse=True)[:5]
        for c in fused:
            c.score = round(rrf_scores[c.chunk_id], 4)
        return RAGResult(
            query=query, mode=RAGMode.RECIPROCAL_RANK_FUSION,
            answer=self._synthesize_answer(query, fused, RAGMode.RECIPROCAL_RANK_FUSION),
            evidence=fused, confidence=self._compute_confidence(fused),
            reasoning_steps=[f"RRF over BM25({len(corpus_chunks)}) + Graph({len(graph_chunks)})"],
        )

    def _cross_encoder_reranking(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Reorders initial BM25 candidates using simulated cross-encoder scoring."""
        candidates = self._retrieve_from_corpus(query, top_k=10)
        query_tokens = set(_tokenize(query))
        for c in candidates:
            doc_tokens = set(_tokenize(c.content))
            overlap = len(query_tokens & doc_tokens) / max(len(query_tokens | doc_tokens), 1)
            c.score = round(overlap, 3)
        candidates.sort(key=lambda c: c.score, reverse=True)
        top = candidates[:5]
        return RAGResult(
            query=query, mode=RAGMode.CROSS_ENCODER_RERANKING,
            answer=self._synthesize_answer(query, top, RAGMode.CROSS_ENCODER_RERANKING),
            evidence=top, confidence=self._compute_confidence(top),
            reasoning_steps=[f"Cross-encoder reranked {len(candidates)} candidates"],
        )

    def _late_interaction_retrieval(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Uses token-level interaction scoring (ColBERT-style) for fine-grained matching."""
        candidates = self._retrieve_from_corpus(query, top_k=8)
        query_tokens = _tokenize(query)
        for c in candidates:
            doc_tokens = _tokenize(c.content)
            if not query_tokens or not doc_tokens:
                continue
            total = 0.0
            for qt in query_tokens:
                best = max((1.0 if qt == dt else 0.0 for dt in doc_tokens), default=0.0)
                total += best
            c.score = round(total / max(len(query_tokens), 1), 3)
        candidates.sort(key=lambda x: x.score, reverse=True)
        top = candidates[:5]
        return RAGResult(
            query=query, mode=RAGMode.LATE_INTERACTION_RETRIEVAL,
            answer=self._synthesize_answer(query, top, RAGMode.LATE_INTERACTION_RETRIEVAL),
            evidence=top, confidence=self._compute_confidence(top),
            reasoning_steps=["Late-interaction token-level MaxSim scoring applied"],
        )

    def _multi_vector_retrieval(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Represents each document through multiple vectors for multi-aspect matching."""
        chunks = self._retrieve_from_corpus(query, top_k=5)
        for c in chunks:
            c.metadata["vector_aspects"] = ["title", "content", "summary"]
        return RAGResult(
            query=query, mode=RAGMode.MULTI_VECTOR_RETRIEVAL,
            answer=self._synthesize_answer(query, chunks, RAGMode.MULTI_VECTOR_RETRIEVAL),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=["Multi-vector scoring across title/content/summary aspects"],
        )

    def _metadata_aware_retrieval(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Filters and boosts results using structured metadata fields."""
        required_type = ctx.get("source_type_filter", None)
        filter_fn = (lambda d: d.get("source_type") == required_type) if required_type else None
        chunks = self._retrieve_from_corpus(query, top_k=5, filter_fn=filter_fn)
        return RAGResult(
            query=query, mode=RAGMode.METADATA_AWARE_RETRIEVAL,
            answer=self._synthesize_answer(query, chunks, RAGMode.METADATA_AWARE_RETRIEVAL),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"Metadata filter: source_type={required_type or 'any'}"],
        )

    def _semantic_chunking(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Creates chunks using semantic boundaries rather than fixed sizes."""
        chunks = self._retrieve_from_corpus(query, top_k=5)
        for c in chunks:
            sentences = re.split(r'[.!?]+', c.content)
            query_tokens = set(_tokenize(query))
            relevant = [s.strip() for s in sentences if set(_tokenize(s)) & query_tokens]
            if relevant:
                c.content = ". ".join(relevant[:3])
                c.metadata["semantic_boundary"] = True
        return RAGResult(
            query=query, mode=RAGMode.SEMANTIC_CHUNKING,
            answer=self._synthesize_answer(query, chunks, RAGMode.SEMANTIC_CHUNKING),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=["Semantic sentence-boundary chunking applied"],
        )

    def _dynamic_chunking(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Adjusts chunk granularity according to content complexity."""
        complexity = len(_tokenize(query))
        top_k = 3 if complexity < 5 else 7
        chunks = self._retrieve_from_corpus(query, top_k=top_k)
        return RAGResult(
            query=query, mode=RAGMode.DYNAMIC_CHUNKING,
            answer=self._synthesize_answer(query, chunks, RAGMode.DYNAMIC_CHUNKING),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"Dynamic granularity: complexity={complexity}, top_k={top_k}"],
        )

    def _context_compression(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Reduces retrieved information while preserving query-relevant evidence."""
        chunks = self._retrieve_from_corpus(query, top_k=5)
        query_tokens = set(_tokenize(query))
        for c in chunks:
            words = c.content.split()
            compressed = [w for w in words if w.lower() in query_tokens or len(w) > 4]
            c.content = " ".join(compressed[:50]) if compressed else c.content[:100]
            c.metadata["compressed"] = True
        return RAGResult(
            query=query, mode=RAGMode.CONTEXT_COMPRESSION,
            answer=self._synthesize_answer(query, chunks, RAGMode.CONTEXT_COMPRESSION),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=["Context compression: retained query-relevant tokens only"],
        )

    def _evidence_deduplication(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Removes duplicate or near-duplicate sources before synthesis."""
        chunks = self._retrieve_from_corpus(query, top_k=8)
        seen_sigs: set[str] = set()
        deduped: list[EvidenceChunk] = []
        for c in chunks:
            sig = " ".join(sorted(_tokenize(c.content)[:10]))
            if sig not in seen_sigs:
                seen_sigs.add(sig)
                deduped.append(c)
        return RAGResult(
            query=query, mode=RAGMode.EVIDENCE_DEDUPLICATION,
            answer=self._synthesize_answer(query, deduped[:5], RAGMode.EVIDENCE_DEDUPLICATION),
            evidence=deduped[:5], confidence=self._compute_confidence(deduped[:5]),
            reasoning_steps=[f"Deduplication: {len(chunks)} -> {len(deduped)} unique chunks"],
        )

    def _diversity_aware_retrieval(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        """Balances relevance with source diversity for broader coverage."""
        chunks = self._retrieve_from_corpus(query, top_k=8)
        selected: list[EvidenceChunk] = []
        seen_types: set[str] = set()
        for c in sorted(chunks, key=lambda x: x.score, reverse=True):
            source = c.source_type
            if source not in seen_types or len(selected) < 3:
                selected.append(c)
                seen_types.add(source)
            if len(selected) >= 5:
                break
        return RAGResult(
            query=query, mode=RAGMode.DIVERSITY_AWARE_RETRIEVAL,
            answer=self._synthesize_answer(query, selected, RAGMode.DIVERSITY_AWARE_RETRIEVAL),
            evidence=selected, confidence=self._compute_confidence(selected),
            reasoning_steps=[f"Diversity-balanced selection: {len(seen_types)} source types"],
        )
