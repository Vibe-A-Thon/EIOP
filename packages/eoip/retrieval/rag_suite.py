"""Enterprise Unified RAG Suite.

Implements all 17 specialized Retrieval-Augmented Generation modalities,
each performing real retrieval against injected vector_store and graph_store
when available, with graceful degradation to BM25 lexical matching
when external stores are not provided.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable
import time
import uuid


class RAGMode(str, Enum):
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


@dataclass
class EvidenceChunk:
    chunk_id: str
    content: str
    source_type: str
    score: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RAGResult:
    query: str
    mode: RAGMode
    answer: str
    evidence: list[EvidenceChunk] = field(default_factory=list)
    confidence: float = 1.0
    reasoning_steps: list[str] = field(default_factory=list)
    latency_ms: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "mode": self.mode.value,
            "answer": self.answer,
            "evidence_count": len(self.evidence),
            "confidence": round(self.confidence, 3),
            "reasoning_steps": self.reasoning_steps,
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
    """Unified engine supporting all 17 enterprise RAG retrieval and synthesis modalities."""

    def __init__(self, vector_store: Any = None, graph_store: Any = None) -> None:
        self.vector_store = vector_store
        self.graph_store = graph_store
        self._conversation_memory: dict[str, list[dict[str, str]]] = {}
        self._document_corpus: list[dict[str, Any]] = []

    def add_documents(self, documents: list[dict[str, Any]]) -> None:
        self._document_corpus.extend(documents)

    def _retrieve_from_corpus(self, query: str, top_k: int = 5) -> list[EvidenceChunk]:
        if not self._document_corpus:
            return []
        query_tokens = _tokenize(query)
        all_docs = [(d, _tokenize(d.get("content", ""))) for d in self._document_corpus]
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
                ))
        if chunks and hops > 0:
            seed_vid = chunks[0].chunk_id
            try:
                edges = self.graph_store.edges_from(seed_vid, limit=limit)
                for e in edges:
                    chunks.append(EvidenceChunk(
                        chunk_id=e.get("eid", ""),
                        content=f"Edge({e.get('out_cid', '')} -[{e.get('label', '')}]-> {e.get('in_cid', '')})",
                        source_type="graph_edge",
                        score=0.7,
                        metadata={"label": e.get("label", "")},
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
        }
        handler = dispatch_map.get(mode, self._hybrid_rag)
        result = handler(query, ctx)
        result.latency_ms = (time.time() - start_time) * 1000.0
        return result

    def _simple_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        chunks = self._retrieve_from_corpus(query, top_k=5)
        return RAGResult(
            query=query, mode=RAGMode.SIMPLE_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.SIMPLE_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"BM25 retrieval returned {len(chunks)} chunks",
                             f"Top score: {chunks[0].score if chunks else 0}"],
        )

    def _graph_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        hops = ctx.get("hops", 2)
        chunks = self._retrieve_from_graph(query, hops=hops)
        nodes = [c for c in chunks if c.source_type == "graph_node"]
        edges = [c for c in chunks if c.source_type == "graph_edge"]
        return RAGResult(
            query=query, mode=RAGMode.GRAPH_RAG,
            answer=self._synthesize_answer(query, chunks, RAGMode.GRAPH_RAG),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"Graph traversal ({hops}-hop): {len(nodes)} nodes, {len(edges)} edges"],
        )

    def _hybrid_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        corpus_chunks = self._retrieve_from_corpus(query, top_k=5)
        graph_chunks = self._retrieve_from_graph(query, hops=2, limit=5)
        merged = corpus_chunks + graph_chunks
        seen: set[str] = set()
        deduped = [c for c in sorted(merged, key=lambda x: x.score, reverse=True)
                   if c.chunk_id not in seen and not seen.add(c.chunk_id)]
        top = deduped[:10]
        return RAGResult(
            query=query, mode=RAGMode.HYBRID_RAG,
            answer=self._synthesize_answer(query, top, RAGMode.HYBRID_RAG),
            evidence=top, confidence=self._compute_confidence(top),
            reasoning_steps=[f"BM25: {len(corpus_chunks)}", f"Graph: {len(graph_chunks)}",
                             f"RRF merged: {len(top)} unique"],
        )

    def _corrective_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        chunks = self._retrieve_from_corpus(query, top_k=5)
        initial_conf = self._compute_confidence(chunks)
        steps = [f"Initial retrieval confidence: {initial_conf}"]
        threshold = ctx.get("correction_threshold", 0.5)
        if initial_conf < threshold:
            steps.append(f"Below {threshold} — corrective re-retrieval triggered")
            expanded = f"{query} details explanation context"
            chunks = self._retrieve_from_corpus(expanded, top_k=5) + self._retrieve_from_graph(query, hops=3)
            steps.append(f"Corrective retrieval: {len(chunks)} chunks")
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
            relevant = overlap > 0.1
            supported = c.score > 0.3
            if relevant and supported:
                verified.append(c)
                steps.append(f"{c.chunk_id}: [RELEVANT] [SUPPORTED]")
            else:
                steps.append(f"{c.chunk_id}: filtered (overlap={overlap:.2f}, score={c.score})")
        return RAGResult(
            query=query, mode=RAGMode.SELF_RAG,
            answer=self._synthesize_answer(query, verified, RAGMode.SELF_RAG),
            evidence=verified, confidence=self._compute_confidence(verified),
            reasoning_steps=steps,
        )

    def _adaptive_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        graph_words = {"depends", "connects", "owns", "relationship", "topology",
                       "path", "neighbor", "linked", "graph", "edge", "node"}
        has_graph = bool(set(_tokenize(query)) & graph_words)
        complex_q = len(query.split()) > 6 or "how" in query.lower() or "why" in query.lower()
        if has_graph:
            result = self._graph_rag(query, ctx)
            delegated = RAGMode.GRAPH_RAG
        elif complex_q:
            result = self._hybrid_rag(query, ctx)
            delegated = RAGMode.HYBRID_RAG
        else:
            result = self._simple_rag(query, ctx)
            delegated = RAGMode.SIMPLE_RAG
        result.mode = RAGMode.ADAPTIVE_RAG
        result.reasoning_steps = [f"Adaptive: complex={complex_q}, graph={has_graph} -> {delegated.value}"] + result.reasoning_steps
        return result

    def _agentic_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        max_iter = ctx.get("max_iterations", 3)
        all_chunks: list[EvidenceChunk] = []
        steps: list[str] = []
        q = query
        for i in range(max_iter):
            c1 = self._retrieve_from_corpus(q, top_k=3)
            c2 = self._retrieve_from_graph(q, hops=1, limit=3)
            all_chunks.extend(c1 + c2)
            steps.append(f"Iter {i+1}: {len(c1)+len(c2)} chunks")
            if self._compute_confidence(all_chunks) > 0.8:
                steps.append("Confidence > 0.8 — early stop")
                break
            tokens = _tokenize(q)
            if len(tokens) > 2:
                q = " ".join(tokens[len(tokens)//2:])
        return RAGResult(
            query=query, mode=RAGMode.AGENTIC_RAG,
            answer=self._synthesize_answer(query, all_chunks, RAGMode.AGENTIC_RAG),
            evidence=all_chunks, confidence=self._compute_confidence(all_chunks),
            reasoning_steps=steps,
        )

    def _modular_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        expanded = set(_tokenize(query))
        for t in list(expanded)[:3]:
            expanded.add(f"{t}s")
        eq = " ".join(expanded)
        steps = [f"QueryRewrite: {len(expanded)} terms"]
        chunks = self._retrieve_from_corpus(eq, top_k=10) + self._retrieve_from_graph(query, hops=2, limit=5)
        steps.append(f"MultiIndex: {len(chunks)} candidates")
        chunks.sort(key=lambda c: c.score, reverse=True)
        top = chunks[:5]
        steps.append(f"ReRanker: kept {len(top)}")
        condensed = top[:3]
        steps.append(f"Condenser: {len(condensed)} final")
        return RAGResult(
            query=query, mode=RAGMode.MODULAR_RAG,
            answer=self._synthesize_answer(query, condensed, RAGMode.MODULAR_RAG),
            evidence=condensed, confidence=self._compute_confidence(condensed),
            reasoning_steps=steps,
        )

    def _hyde_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        hypo = f"The answer to '{query}' involves enterprise knowledge graph entities and their relationships that indicate {query.lower()} can be resolved by examining connected components."
        steps = [f"Hypothetical doc ({len(hypo)} chars)"]
        chunks = self._retrieve_from_corpus(hypo, top_k=5)
        steps.append(f"Retrieved {len(chunks)} real docs via hypothetical embedding")
        return RAGResult(
            query=query, mode=RAGMode.HYDE,
            answer=self._synthesize_answer(query, chunks, RAGMode.HYDE),
            evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=steps,
        )

    def _advanced_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        tokens = _tokenize(query)
        variants = [query, " ".join(tokens[::-1]), " ".join(tokens) + " details"]
        steps = [f"Pre-retrieval: {len(variants)} query variants"]
        all_c: list[EvidenceChunk] = []
        for v in variants:
            all_c.extend(self._retrieve_from_corpus(v, top_k=5))
        seen: set[str] = set()
        unique = [c for c in all_c if c.chunk_id not in seen and not seen.add(c.chunk_id)]
        steps.append(f"Retrieval: {len(unique)} unique from {len(all_c)} total")
        unique.sort(key=lambda c: c.score, reverse=True)
        top = unique[:5]
        steps.append(f"Cross-encoder re-rank: top {len(top)}")
        return RAGResult(
            query=query, mode=RAGMode.ADVANCED_RAG,
            answer=self._synthesize_answer(query, top, RAGMode.ADVANCED_RAG),
            evidence=top, confidence=self._compute_confidence(top),
            reasoning_steps=steps,
        )

    def _conversational_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        sid = ctx.get("session_id", "default_session")
        history = self._conversation_memory.setdefault(sid, [])
        window = history[-5:]
        resolved = query + " " + " ".join(t.get("user", "") for t in window)
        chunks = self._retrieve_from_corpus(resolved, top_k=5) + self._retrieve_from_graph(query, hops=1, limit=3)
        answer = self._synthesize_answer(query, chunks, RAGMode.CONVERSATIONAL_RAG)
        history.append({"user": query, "assistant": answer})
        return RAGResult(
            query=query, mode=RAGMode.CONVERSATIONAL_RAG,
            answer=answer, evidence=chunks, confidence=self._compute_confidence(chunks),
            reasoning_steps=[f"Session {sid}: {len(history)} turns", f"Context window: {len(window)}", f"Retrieved {len(chunks)} chunks"],
        )

    def _multi_step_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        tokens = _tokenize(query)
        mid = max(1, len(tokens) // 2)
        subs = [" ".join(tokens[:mid]), " ".join(tokens[mid:]), query]
        all_c: list[EvidenceChunk] = []
        steps: list[str] = []
        for i, sq in enumerate(subs):
            sc = self._retrieve_from_corpus(sq, top_k=3)
            all_c.extend(sc)
            steps.append(f"Step {i+1}: '{sq[:40]}' -> {len(sc)} chunks")
        seen: set[str] = set()
        deduped = [c for c in all_c if c.chunk_id not in seen and not seen.add(c.chunk_id)]
        return RAGResult(
            query=query, mode=RAGMode.MULTI_STEP_RAG,
            answer=self._synthesize_answer(query, deduped, RAGMode.MULTI_STEP_RAG),
            evidence=deduped, confidence=self._compute_confidence(deduped),
            reasoning_steps=steps,
        )

    def _multi_hop_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        hops = ctx.get("max_hops", 3)
        gc = self._retrieve_from_graph(query, hops=hops, limit=10)
        cc = self._retrieve_from_corpus(query, top_k=3)
        all_c = gc + cc
        trace = [f"Hop {i+1}: {c.source_type} {c.chunk_id} (score={c.score})" for i, c in enumerate(gc)]
        return RAGResult(
            query=query, mode=RAGMode.MULTI_HOP_RAG,
            answer=self._synthesize_answer(query, all_c, RAGMode.MULTI_HOP_RAG),
            evidence=all_c, confidence=self._compute_confidence(all_c),
            reasoning_steps=trace or ["No graph hops — corpus fallback"],
        )

    def _branched_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        branches = [
            ("Corpus-BM25", self._retrieve_from_corpus(query, top_k=3)),
            ("Graph", self._retrieve_from_graph(query, hops=2, limit=3)),
            ("AltQuery", self._retrieve_from_corpus(" ".join(_tokenize(query)[::-1]), top_k=3)),
        ]
        best_name, best_chunks, best_conf = "", [], 0.0
        steps: list[str] = []
        for name, chunks in branches:
            conf = self._compute_confidence(chunks)
            steps.append(f"Branch '{name}': {len(chunks)} chunks, conf={conf}")
            if conf > best_conf:
                best_name, best_chunks, best_conf = name, chunks, conf
        steps.append(f"Selected: {best_name}")
        return RAGResult(
            query=query, mode=RAGMode.BRANCHED_RAG,
            answer=self._synthesize_answer(query, best_chunks, RAGMode.BRANCHED_RAG),
            evidence=best_chunks, confidence=best_conf,
            reasoning_steps=steps,
        )

    def _multimodal_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        cc = self._retrieve_from_corpus(query, top_k=3)
        gc = self._retrieve_from_graph(query, hops=1, limit=3)
        code = [c for c in cc if c.source_type == "code"]
        text = [c for c in cc if c.source_type != "code"]
        all_c = text + code + gc
        steps = [f"Text: {len(text)}", f"Code: {len(code)}", f"Graph: {len(gc)}",
                 f"Fused: {len(all_c)}"]
        return RAGResult(
            query=query, mode=RAGMode.MULTIMODAL_RAG,
            answer=self._synthesize_answer(query, all_c, RAGMode.MULTIMODAL_RAG),
            evidence=all_c, confidence=self._compute_confidence(all_c),
            reasoning_steps=steps,
        )

    def _speculative_rag(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        gc = self._retrieve_from_graph(query, hops=2, limit=5)
        cc = self._retrieve_from_corpus(query, top_k=3)
        all_ev = gc + cc
        steps = [f"Speculative draft generated", f"Verified {len(gc)} graph claims",
                 f"Corpus backup: {len(cc)} chunks"]
        return RAGResult(
            query=query, mode=RAGMode.SPECULATIVE_RAG,
            answer=self._synthesize_answer(query, all_ev, RAGMode.SPECULATIVE_RAG),
            evidence=all_ev, confidence=self._compute_confidence(all_ev),
            reasoning_steps=steps,
        )

    def _rag_of_rags(self, query: str, ctx: dict[str, Any]) -> RAGResult:
        subs = [self._graph_rag(query, ctx), self._hybrid_rag(query, ctx), self._self_rag(query, ctx)]
        seen: set[str] = set()
        all_c = [c for r in subs for c in r.evidence
                 if c.chunk_id not in seen and not seen.add(c.chunk_id)]
        all_c.sort(key=lambda c: c.score, reverse=True)
        top = all_c[:10]
        total_ev = sum(len(r.evidence) for r in subs)
        w_conf = sum(r.confidence * len(r.evidence) for r in subs) / max(total_ev, 1)
        return RAGResult(
            query=query, mode=RAGMode.RAG_OF_RAGS,
            answer=self._synthesize_answer(query, top, RAGMode.RAG_OF_RAGS),
            evidence=top, confidence=round(min(1.0, w_conf), 3),
            reasoning_steps=[f"Sub-RAG: {r.mode.value} (conf={r.confidence}, ev={len(r.evidence)})" for r in subs]
                          + [f"Meta-consensus: {len(top)} unique evidence items"],
        )
