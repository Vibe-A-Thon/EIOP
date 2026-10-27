"""Graph-first evidence retrieval with deterministic strategy routing and optional local model synthesis.

Covers FR-RAG-001 (retrieval router), FR-RAG-002 (GraphRAG evidence retrieval),
and FR-RAG-003 (local model abstraction).
"""

from __future__ import annotations

import hashlib
import json
from enum import Enum
from uuid import uuid4

from eoip.contracts.canonical import TrustedScope
from eoip.authz.derivation_acl import get_derivation_evaluator
from eoip.contracts.retrieval import RetrievalContext, RetrievalResult
from eoip.graph.traversal import GraphTraversal
from eoip.models.port import generate_via_port
from eoip.models.provider import ModelUnavailable, create_model_provider
from eoip.provenance.evidence import EvidenceService
from eoip.retrieval.vectors import (
    InMemorySearchIndex,
    RetrievalTrace,
    build_search_index,
)


class RetrievalStrategy(str, Enum):
    DIRECT_GRAPH = "direct_graph"
    CODE_CONTEXT = "code_context"
    DOCUMENT_CONTEXT = "document_context"
    KEYWORD = "keyword"
    VECTOR = "vector"
    HYBRID = "hybrid"
    NONE = "none"


_CODE_LABELS = frozenset(
    {
        "File",
        "CodeSymbol",
        "Repository",
        "Branch",
        "Commit",
        "Dependency",
        "MergeRequest",
        "PipelineRun",
    }
)
_DOC_LABELS = frozenset({"Document", "DocumentSection"})


def _label_of(store, canonical_id: str) -> str | None:
    vertex = store.get_vertex_by_canonical_id(canonical_id)
    return vertex["label"] if vertex else None


def select_strategy(canonical_id: str, question: str, store) -> RetrievalStrategy:
    if not canonical_id:
        return RetrievalStrategy.NONE
    q = question.lower()
    code_keywords = (
        "code",
        "implement",
        "symbol",
        "function",
        "class",
        "method",
        "file",
        "module",
    )
    doc_keywords = ("doc", "document", "wiki", "readme", "confluence", "markdown")
    code_signals = any(keyword in q for keyword in code_keywords)
    doc_signals = any(keyword in q for keyword in doc_keywords)
    label = _label_of(store, canonical_id)
    if label in _CODE_LABELS:
        code_signals = True
    if label in _DOC_LABELS:
        doc_signals = True
    if code_signals and doc_signals:
        return RetrievalStrategy.HYBRID
    if code_signals:
        return RetrievalStrategy.CODE_CONTEXT
    if doc_signals:
        return RetrievalStrategy.DOCUMENT_CONTEXT
    return RetrievalStrategy.DIRECT_GRAPH


def _node_label(node: dict) -> str:
    props = node["properties"]
    return (
        props.get("issue_key")
        or props.get("name")
        or props.get("qualified_name")
        or props.get("path")
        or node["label"]
    )


def _build_contexts(
    nodes: list[dict], edges: list[dict], strategy: RetrievalStrategy
) -> list[RetrievalContext]:
    contexts: list[RetrievalContext] = []
    if strategy == RetrievalStrategy.CODE_CONTEXT:
        selected_nodes = [
            n for n in nodes if n["label"] in _CODE_LABELS or n["label"] == "WorkItem"
        ]
    elif strategy == RetrievalStrategy.DOCUMENT_CONTEXT:
        selected_nodes = [
            n for n in nodes if n["label"] in _DOC_LABELS or n["label"] == "WorkItem"
        ]
    else:
        selected_nodes = nodes
    selected_ids = {n["canonical_id"] for n in selected_nodes}
    for node in selected_nodes:
        contexts.append(
            RetrievalContext(
                kind="entity",
                ref=node["canonical_id"],
                text=f"[{node['label']}] {_node_label(node)}",
                citations=[node["canonical_id"]],
            )
        )
    for edge in edges:
        if edge["out_cid"] not in selected_ids or edge["in_cid"] not in selected_ids:
            continue
        props = edge["properties"]
        refs = [ref for ref in (props.get("source_ref"), props.get("evidence_key")) if ref]
        contexts.append(
            RetrievalContext(
                kind="relationship",
                ref=edge["eid"],
                text=f"{edge['out_cid']} -[{edge['label']}]-> {edge['in_cid']}",
                citations=refs,
            )
        )
    contexts.append(
        RetrievalContext(
            kind="summary",
            ref="summary",
            text=(
                f"Strategy {strategy.value} returned {len(selected_nodes)} entities "
                f"and {len(edges)} relationships."
            ),
            citations=[],
        )
    )
    return contexts


def _vertex_label_of(store, canonical_id: str) -> str | None:
    vertex = store.get_vertex_by_canonical_id(canonical_id)
    if not vertex:
        return None
    props = vertex.get("properties") or {}
    return (
        props.get("name")
        or props.get("qualified_name")
        or props.get("issue_key")
        or props.get("path")
        or vertex["label"]
    )


# -- GAP-RET-003: evidence-quality / recency / authority ranking --------------


def _quality_boost(props: dict) -> float:
    confidence = props.get("confidence")
    if isinstance(confidence, (int, float)):
        return max(0.0, min(1.0, float(confidence)))
    if props.get("source_ref") or props.get("evidence_key"):
        return 0.8
    return 0.5


def _recency_boost(props: dict) -> float:
    import time

    updated = props.get("updated_at") or props.get("created_at")
    if isinstance(updated, (int, float)) and updated > 0:
        age_days = max(0.0, (time.time() - float(updated)) / 86400.0)
        return 0.5 + 0.5 * pow(0.5, age_days / 30.0)  # half-life of 30 days
    return 0.5


def _authority_boost(props: dict) -> float:
    authority = props.get("authority_score")
    if isinstance(authority, (int, float)):
        return max(0.0, min(1.0, float(authority)))
    return 0.5


def _rank_fused(
    store,
    fused: dict[str, float],
    *,
    graph_scores: dict[str, float],
) -> list[tuple[str, float]]:
    """Re-rank fused candidates using evidence quality, recency and authority."""
    ranked = []
    for cid, score in fused.items():
        vertex = store.get_vertex_by_canonical_id(cid)
        props = (vertex or {}).get("properties") or {}
        ranking_signal = (
            0.45 * _quality_boost(props)
            + 0.35 * _recency_boost(props)
            + 0.20 * _authority_boost(props)
        )
        boosted = score * (0.25 + (1.5 * ranking_signal))  # keep base relevance dominant
        graph_bonus = 0.05 * graph_scores.get(cid, 0.0)
        ranked.append((cid, boosted + graph_bonus))
    ranked.sort(key=lambda kv: (-kv[1], kv[0]))
    return ranked


def _grounded_answer(provider, question: str, nodes: list, edges: list, scope, max_tokens: int):
    """CRA-026: synthesis goes through the evidence-bound GraphRAG pipeline: fenced/defused context, the
    model's own tokenizer budget, and a cited-span claim-support check on every generated sentence.
    Evidence is one assertion per graph entity (its properties as sentences) and per relationship."""
    from eoip.ai.graphrag import GraphRAGPipeline, ModelManifest
    from eoip.contracts.canonical import PrincipalType

    evidence = []
    for i, n in enumerate(nodes):
        props = n.get("properties") or {}
        facts = [f"{n['label']} {n['canonical_id']} {k.replace('_', ' ')} is {str(v).strip().rstrip('.')}."
                 for k, v in sorted(props.items())
                 if k not in ("canonical_id", "tenant_id") and isinstance(v, (str, int, float)) and str(v).strip()]
        if facts:
            evidence.append({"assertion_id": n["canonical_id"], "snippet": " ".join(facts),
                             "relevance_score": 1.0 / (1 + i), "locator": {"source_uri": n["canonical_id"]}})
    for e in edges:
        ref = (e.get("properties") or {}).get("source_ref")
        out_v, in_v = e.get("out_canonical_id") or e.get("out_v"), e.get("in_canonical_id") or e.get("in_v")
        evidence.append({"assertion_id": e.get("eid") or f"{out_v}-{e.get('label')}-{in_v}",
                         "snippet": f"{out_v} {e.get('label', '').replace('_', ' ').lower()} {in_v}.",
                         "relevance_score": 0.1, "locator": {"source_uri": ref or ""}})
    rag_scope = scope or TrustedScope(tenant_id="default", workspace_id="default", principal_id="retrieval",
                                      principal_type=PrincipalType.SERVICE_ACCOUNT)
    try:
        manifest = ModelManifest.from_provider(provider, max_output_tokens=max_tokens)
        return GraphRAGPipeline(model_manifest=manifest).answer_question(question, evidence, rag_scope,
                                                                       runtime=provider)
    except ModelUnavailable:
        return None


def _scoped(hits: list[tuple[str, float]], allow) -> list[tuple[str, float]]:
    """Permission filtering at candidate generation (CRA-025.3)."""
    return hits if allow is None else [h for h in hits if allow(h[0])]


def _normalize(scores: list[tuple[str, float]]) -> dict[str, float]:
    if not scores:
        return {}
    peak = max(score for _, score in scores) or 1.0
    return {cid: score / peak for cid, score in scores}


def _entity_context(store, cid: str) -> RetrievalContext:
    vertex = store.get_vertex_by_canonical_id(cid)
    label = vertex["label"] if vertex else "Entity"
    return RetrievalContext(
        kind="entity",
        ref=cid,
        text=f"[{label}] {_vertex_label_of(store, cid) or cid}",
        citations=[cid],
    )


def _stable_path_id(node_ids: list[str], edge_ids: list[str]) -> str:
    payload = json.dumps({"nodes": node_ids, "edges": edge_ids}, sort_keys=True, separators=(",", ":"))
    return "urn:eoip:rag:path:" + hashlib.sha256(payload.encode()).hexdigest()[:16]


def _node_source_refs(store, node: dict) -> list[str]:
    refs = set()
    props = node.get("properties") or {}
    for key in ("source_ref", "evidence_key", "source_id", "source_uri"):
        if props.get(key):
            refs.add(str(props[key]))
    try:
        for edge in store.edges_from(node["vid"], labels=["EVIDENCED_BY"], limit=100):
            edge_props = edge.get("properties") or {}
            if edge_props.get("source_ref"):
                refs.add(str(edge_props["source_ref"]))
            if edge_props.get("evidence_key"):
                refs.add(str(edge_props["evidence_key"]))
            if edge.get("in_cid"):
                refs.add(str(edge["in_cid"]))
    except (KeyError, TypeError, AttributeError, ValueError):
        pass
    return sorted(refs)


def _edge_source_refs(edge: dict) -> list[str]:
    refs = set()
    props = edge.get("properties") or {}
    for key in ("source_ref", "evidence_key", "source_system"):
        if props.get(key):
            refs.add(str(props[key]))
    return sorted(refs)


def _citation_chain_for_node(store, node: dict, *, path: dict | None = None) -> dict:
    path = path or {"vertices": [node], "edges": []}
    path_nodes = [vertex["canonical_id"] for vertex in path.get("vertices", []) if vertex.get("canonical_id")]
    path_edges = [edge["eid"] for edge in path.get("edges", []) if edge.get("eid")]
    source_refs = set(_node_source_refs(store, node))
    for vertex in path.get("vertices", []):
        source_refs.update(_node_source_refs(store, vertex))
    for edge in path.get("edges", []):
        source_refs.update(_edge_source_refs(edge))
    return {
        "chain_id": _stable_path_id(path_nodes or [node["canonical_id"]], path_edges),
        "node_ref": node["canonical_id"],
        "path_id": _stable_path_id(path_nodes or [node["canonical_id"]], path_edges),
        "path": {"node_ids": path_nodes or [node["canonical_id"]], "edge_ids": path_edges},
        "source_refs": sorted(source_refs),
    }


def _attach_evidence_addressing(
    store,
    result: RetrievalResult,
    *,
    node_ids: list[str] | None = None,
    edge_ids: list[str] | None = None,
    paths: list[dict] | None = None,
    query_plan: dict | None = None,
) -> RetrievalResult:
    nodes: list[dict] = []
    for cid in node_ids or []:
        vertex = store.get_vertex_by_canonical_id(cid) or store.get_vertex(cid)
        if vertex:
            nodes.append(vertex)
    edge_ids = edge_ids or []
    manifest = EvidenceService(store).build_manifest(
        answer_id=result.retrieval_id,
        node_ids=[node["canonical_id"] for node in nodes],
        edge_ids=edge_ids,
        evidence_refs=result.evidence_refs,
        query_plan=query_plan or {"strategy": result.strategy},
        confidence_inputs=[
            {"name": "context_count", "value": len(result.contexts)},
            {"name": "evidence_ref_count", "value": len(result.evidence_refs)},
        ],
    ).to_dict()
    chains = [_citation_chain_for_node(store, node) for node in nodes]
    for path in paths or []:
        vertices = path.get("vertices", [])
        if not vertices:
            continue
        chains.append(_citation_chain_for_node(store, vertices[-1], path=path))
    seen: set[str] = set()
    result.citation_chains = []
    for chain in chains:
        key = chain["chain_id"]
        if key in seen:
            continue
        seen.add(key)
        result.citation_chains.append(chain)
    result.evidence_manifest = manifest
    return result


def _result_from_candidates(
    store,
    strategy: RetrievalStrategy,
    question: str,
    ranked: list[tuple[str, float]],
    trace: RetrievalTrace,
) -> RetrievalResult:
    contexts = [_entity_context(store, cid) for cid, _ in ranked]
    contexts.append(
        RetrievalContext(
            kind="summary",
            ref="summary",
            text=(
                f"Strategy {strategy.value} returned {len(ranked)} ranked entities "
                f"for question: {question}"
            ),
            citations=[],
        )
    )
    retrieval_id = str(uuid4())
    result = RetrievalResult(
        retrieval_id=retrieval_id,
        strategy=strategy.value,
        contexts=contexts,
        evidence_refs=[cid for cid, _ in ranked],
        metrics={"entities": len(ranked), "ranking": "evidence-quality+recency+authority"},
        answer=(
            f"Ranked {len(ranked)} graph entities for '{question}' using strategy "
            f"{strategy.value}."
        ),
        warnings=[],
        generation="deterministic",
        partial=False,
        facts=[
            {
                "canonical_id": cid,
                "type": (store.get_vertex_by_canonical_id(cid) or {}).get("label"),
                "name": _vertex_label_of(store, cid),
                "score": round(score, 6),
            }
            for cid, score in ranked
        ],
        graph={"source": None, "impacted": [], "truncated": False},
        trace=trace.to_dict(),
    )
    return _attach_evidence_addressing(
        store,
        result,
        node_ids=[cid for cid, _ in ranked],
        query_plan={"strategy": strategy.value, "question": question, "ranking_trace": trace.to_dict()},
    )


def search_keyword(
    store,
    question: str,
    *,
    search_index: InMemorySearchIndex | None = None,
    top_k: int = 10,
    allow=None,
) -> RetrievalResult:
    """GAP-RET-002 keyword/full-text retrieval via the SearchIndex port."""
    index = search_index or build_search_index(store)
    trace = RetrievalTrace()
    hits = _scoped(index.keyword_search(question, top_k), allow)
    trace.record("keyword", hits, index=type(index).__name__)
    ranked = _rank_fused(store, dict(hits), graph_scores={cid: s for cid, s in hits})
    trace.record("ranked", ranked)
    return _result_from_candidates(store, RetrievalStrategy.KEYWORD, question, ranked, trace)


def search_vector(
    store,
    question: str,
    *,
    search_index: InMemorySearchIndex | None = None,
    top_k: int = 10,
    allow=None,
) -> RetrievalResult:
    """GAP-RET-002 vector retrieval via deterministic hashing embeddings."""
    index = search_index or build_search_index(store)
    trace = RetrievalTrace()
    hits = _scoped(index.vector_search(question, top_k), allow)
    trace.record("vector", hits, index=type(index).__name__)
    ranked = _rank_fused(store, dict(hits), graph_scores={cid: s for cid, s in hits})
    trace.record("ranked", ranked)
    return _result_from_candidates(store, RetrievalStrategy.VECTOR, question, ranked, trace)


def search_hybrid(
    store,
    question: str,
    *,
    canonical_id: str | None = None,
    search_index: InMemorySearchIndex | None = None,
    top_k: int = 10,
    allow=None,
) -> RetrievalResult:
    """GAP-SEARCH-001 hybrid fusion of graph, keyword and vector candidates.

    Keyword and vector candidates come from the SearchIndex port; graph
    candidates come from traversal around the seed entity (or the top keyword
    hit when no seed is given). Candidates are fused and re-ranked with
    evidence-quality / recency / authority signals (GAP-RET-003) and a
    retrieval trace is recorded (GAP-RET-006).
    """
    index = search_index or build_search_index(store)
    trace = RetrievalTrace()
    keyword_hits = _scoped(index.keyword_search(question, top_k), allow)
    vector_hits = _scoped(index.vector_search(question, top_k), allow)
    trace.record("keyword", keyword_hits, index=type(index).__name__)
    trace.record("vector", vector_hits)

    seed = canonical_id or (keyword_hits[0][0] if keyword_hits else None)
    graph_scores: dict[str, float] = {}
    if seed and allow is not None and not allow(seed):
        seed = None  # a seed outside the caller's scope is treated as absent (no existence oracle)
    if seed and store.get_vertex_by_canonical_id(seed):
        result = GraphTraversal(store, max_depth=2, max_results=top_k).impact(seed)
        graph_scores = {
            item["vertex"]["canonical_id"]: 1.0 / (1 + len(item["path"]["edges"]))
            for item in result["impacted"]
        }
        if canonical_id and result["source"]:
            graph_scores[result["source"]["canonical_id"]] = 1.0
    if allow is not None:
        graph_scores = {c: v for c, v in graph_scores.items() if allow(c)}
    trace.record("graph", sorted(graph_scores.items(), key=lambda kv: (-kv[1], kv[0])))

    fused: dict[str, float] = {}
    for cid, score in _normalize(keyword_hits).items():
        fused[cid] = fused.get(cid, 0.0) + 0.45 * score
    for cid, score in _normalize(vector_hits).items():
        fused[cid] = fused.get(cid, 0.0) + 0.35 * score
    for cid, score in graph_scores.items():
        fused[cid] = fused.get(cid, 0.0) + 0.20 * score
    if len(fused) < top_k:
        for cid in index.entity_ids():
            if cid not in fused:
                fused[cid] = 0.01
            if len(fused) >= top_k:
                break

    ranked = _rank_fused(store, fused, graph_scores=graph_scores)[:top_k]
    trace.record("ranked", ranked)
    return _result_from_candidates(store, RetrievalStrategy.HYBRID, question, ranked, trace)


def retrieve(
    store,
    canonical_id,
    question,
    *,
    scope: TrustedScope | None = None,
    synthesize=False,
    model_timeout: float = 90.0,
    max_model_tokens: int = 512,
    strategy: str | RetrievalStrategy | None = None,
    search_index=None,
    top_k: int = 10,
    allow=None,
) -> RetrievalResult:
    if allow is not None and canonical_id and not allow(canonical_id):
        raise ValueError("Entity not found")  # out-of-tenant seeds look absent (no existence oracle)
    if strategy is not None:
        requested = RetrievalStrategy(strategy)
        if requested == RetrievalStrategy.KEYWORD:
            return search_keyword(store, question, search_index=search_index, top_k=top_k, allow=allow)
        if requested == RetrievalStrategy.VECTOR:
            return search_vector(store, question, search_index=search_index, top_k=top_k, allow=allow)
        if requested == RetrievalStrategy.HYBRID:
            return search_hybrid(
                store,
                question,
                canonical_id=canonical_id or None,
                search_index=search_index,
                top_k=top_k,
                allow=allow,
            )
    strategy = select_strategy(canonical_id, question, store)
    if strategy == RetrievalStrategy.NONE:
        empty = RetrievalResult(
            retrieval_id=str(uuid4()),
            strategy=strategy.value,
            contexts=[],
            evidence_refs=[],
            metrics={"reason": "no canonical_id"},
            answer="No canonical ID provided; retrieval disabled.",
            warnings=["Missing canonical_id"],
            generation="deterministic",
            partial=False,
            facts=[],
            graph={"source": None, "impacted": [], "truncated": False},
        )
        return _attach_evidence_addressing(
            store,
            empty,
            query_plan={"strategy": strategy.value, "question": question, "reason": "no canonical_id"},
        )
    result = GraphTraversal(store, max_depth=4, max_results=30).impact(canonical_id)
    if not result["source"]:
        raise ValueError("Entity not found")
    if allow is not None:
        result = {**result, "impacted": [i for i in result["impacted"] if allow(i["vertex"]["canonical_id"])]}
    nodes = [result["source"], *[item["vertex"] for item in result["impacted"]]]
    edges = [e for item in result["impacted"] for e in item["path"]["edges"]]
    if scope is not None:
        nodes, edges = get_derivation_evaluator().filter_graph_contexts(scope, nodes, edges)
        allowed_cids = {n.get("canonical_id") for n in nodes}
        if canonical_id not in allowed_cids:
            nodes = []
            edges = []
    if not nodes:
        empty_acl = RetrievalResult(
            retrieval_id=str(uuid4()),
            strategy=strategy.value,
            contexts=[],
            evidence_refs=[],
            metrics={"reason": "acl_denied", "hidden_by_policy": True},
            answer="Access denied by derivation-aware policy or no accessible facts found.",
            warnings=["Derivation-aware ACL filtered all candidate paths."],
            generation="deterministic",
            partial=False,
            facts=[],
            graph={"source": None, "impacted": [], "truncated": False},
        )
        return _attach_evidence_addressing(
            store,
            empty_acl,
            query_plan={"strategy": strategy.value, "question": question, "reason": "acl_denied"},
        )
    contexts = _build_contexts(nodes, edges, strategy)
    refs = sorted({e["properties"]["source_ref"] for e in edges if e["properties"].get("source_ref")})
    facts = [
        {
            "canonical_id": n["canonical_id"],
            "type": n["label"],
            "name": _node_label(n),
        }
        for n in nodes
    ]
    answer = (
        f"Retrieved {len(nodes)} graph entities connected to {canonical_id} "
        f"using strategy {strategy.value}. Inspect contexts and evidence_refs for citations."
    )
    warnings: list[str] = []
    generation = "deterministic"
    answer_citations: list[dict] = []
    if synthesize:
        provider = create_model_provider(timeout=model_timeout)
        if not provider.available:
            warnings.append("No local model is configured; graph evidence remains available.")
        else:
            grounded = _grounded_answer(provider, question, nodes, edges, scope, max_model_tokens)
            if grounded is None:
                warnings.append("Local generation unavailable; graph evidence remains available.")
            else:
                answer = grounded.text
                answer_citations = grounded.citations
                generation = "local_model" if not grounded.degraded_reason else "extractive"
                if grounded.degraded_reason:
                    warnings.append(f"Generation degraded: {grounded.degraded_reason}")
                if grounded.unsupported_claims:
                    warnings.append(f"{len(grounded.unsupported_claims)} generated statement(s) removed: "
                                    "not supported by the cited evidence")
    retrieval_id = str(uuid4())
    retrieval_result = RetrievalResult(
        retrieval_id=retrieval_id,
        strategy=strategy.value,
        contexts=contexts,
        evidence_refs=refs,
        metrics={"entities": len(nodes), "edges": len(edges), "generation": generation},
        answer=answer,
        answer_citations=answer_citations,
        warnings=warnings,
        generation=generation,
        partial=result["truncated"],
        facts=facts,
        graph=result,
    )
    path_items = [item["path"] for item in result["impacted"]]
    edge_ids = sorted({edge["eid"] for edge in edges if edge.get("eid")})
    node_ids = [node["canonical_id"] for node in nodes]
    return _attach_evidence_addressing(
        store,
        retrieval_result,
        node_ids=node_ids,
        edge_ids=edge_ids,
        paths=path_items,
        query_plan={
            "strategy": strategy.value,
            "question": question,
            "canonical_id": canonical_id,
            "max_depth": 4,
            "entities": len(nodes),
            "edges": len(edges),
        },
    )
