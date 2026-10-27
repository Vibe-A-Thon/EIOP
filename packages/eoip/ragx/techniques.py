"""RAG extension techniques (gap analysis §4, table "RAG techniques").

All techniques are deterministic functions over :class:`~eoip.ragx.core.Candidate`
lists (plus query text). Model-backed variants (CrossEncoder, HyDE, FLARE)
define explicit deterministic fallbacks so they run with no external model;
an optional provider can be injected where a real scorer exists.
"""

from __future__ import annotations

import hashlib
import math
import re
from collections import defaultdict
from typing import Any
from collections.abc import Callable, Iterable

from eoip.ragx.core import Candidate, overlap_score
from eoip.retrieval.vectors import HashingEmbedder, tokenize

Retriever = Callable[[str, int], list[Candidate]]


# ---------------------------------------------------------------------------
# Query transformations
# ---------------------------------------------------------------------------


_EXPAND_SYNONYMS = {
    "bug": ["defect", "issue", "error"],
    "fix": ["patch", "resolve", "repair"],
    "deploy": ["release", "ship", "rollout"],
    "config": ["configuration", "settings"],
    "auth": ["authentication", "login", "authorization"],
    "error": ["failure", "exception", "fault"],
    "test": ["spec", "verification", "check"],
}


def query_expansion(query: str, max_variants: int = 4) -> list[str]:
    """§4 QueryExpansion: synonym-augmented query variants (deterministic)."""
    variants = [query]
    lowered = query.lower()
    for term, synonyms in _EXPAND_SYNONYMS.items():
        if term in lowered:
            for syn in synonyms[:2]:
                variants.append(re.sub(rf"\b{term}\b", syn, lowered, flags=re.IGNORECASE))
        if len(variants) > max_variants:
            break
    return variants[:max_variants]


def query_decomposition(query: str) -> list[str]:
    """§4 QueryDecomposition: split compound questions into sub-questions."""
    parts = [p.strip() for p in re.split(r"\?| and then |, and ", query) if p.strip()]
    parts = [re.sub(r"^(and|then|so)\s+", "", p, flags=re.IGNORECASE) for p in parts]
    return parts or [query]


def step_back(query: str) -> str:
    """§4 StepBack: derive the generic category question (strip specifics)."""
    tokens = [t for t in tokenize(query) if len(t) > 3]
    if not tokens:
        return query
    head = " ".join(tokens[:3])
    return f"What is known about {head} in general?"


def hyde_query(query: str, seed_candidates: list[Candidate] | None = None) -> str:
    """§4 HyDE fallback: build a hypothetical answer document from query + seeds."""
    hypo = list(query.split())
    for c in (seed_candidates or [])[:3]:
        for term in tokenize(c.text):
            if term not in hypo:
                hypo.append(term)
            if len(hypo) >= 24:
                break
        if len(hypo) >= 24:
            break
    return " ".join(hypo)


# ---------------------------------------------------------------------------
# Fusion & re-ranking
# ---------------------------------------------------------------------------


def reciprocal_rank_fusion(
    rankings: list[list[Candidate]], k: float = 60.0, top_n: int | None = None
) -> list[Candidate]:
    """§4 ReciprocalRankFusion / RAG-Fusion core: RRF over N rankings."""
    scores: dict[str, float] = defaultdict(float)
    best: dict[str, Candidate] = {}
    for ranking in rankings:
        seen: set[str] = set()
        for rank, cand in enumerate(ranking):
            key = cand.source_id
            if key in seen:
                continue
            seen.add(key)
            scores[key] += 1.0 / (k + rank + 1)
            if key not in best or cand.score > best[key].score:
                best[key] = cand
    merged = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    out = []
    for key, score in merged[: top_n or len(merged)]:
        c = best[key]
        out.append(Candidate(
            source_id=c.source_id, text=c.text, score=score,
            kind=c.kind, label=c.label, properties=dict(c.properties),
            citations=list(c.citations),
        ))
    return out


def rag_fusion(query: str, retrieve: Retriever, k: float = 60.0, top_n: int = 10) -> list[Candidate]:
    """§4 RAG-Fusion: multi-query expansion + RRF fusion."""
    rankings = [retrieve(variant, top_n) for variant in query_expansion(query)]
    return reciprocal_rank_fusion(rankings, k=k, top_n=top_n)


def cross_encoder_rerank(
    query: str,
    candidates: list[Candidate],
    scorer: Callable[[str, str], float] | None = None,
    top_n: int | None = None,
) -> list[Candidate]:
    """§4 CrossEncoderReranker: re-rank by query-passage affinity.

    ``scorer`` may be a real cross-encoder; the default is a deterministic
    feature fallback (token overlap + exact-phrase bonus + candidate priors).
    """
    if scorer is None:
        q_tokens = set(tokenize(query))

        def scorer(q: str, text: str) -> float:  # type: ignore[no-redef]
            t_tokens = set(tokenize(text))
            if not q_tokens or not t_tokens:
                return 0.0
            jaccard = len(q_tokens & t_tokens) / len(q_tokens | t_tokens)
            phrase = 0.2 if q.lower() in text.lower() else 0.0
            return jaccard + phrase

    out = []
    for c in candidates:
        out.append(Candidate(
            source_id=c.source_id, text=c.text,
            score=float(scorer(query, c.text)),
            kind=c.kind, label=c.label, properties=dict(c.properties),
            citations=list(c.citations),
        ))
    out.sort(key=lambda c: (-c.score, c.source_id))
    return out[: top_n or len(out)]


def late_interaction(
    query: str, candidates: list[Candidate], top_n: int | None = None
) -> list[Candidate]:
    """§4 LateInteraction: token-level MaxSim (ColBERT-style) fallback.

    Uses deterministic hashing embeddings per token; query token vectors
    MaxSim against passage token vectors.
    """
    embedder = HashingEmbedder(dimensions=128)

    def token_vectors(text: str) -> list[list[float]]:
        return [embedder.embed(t) for t in set(tokenize(text))] or [embedder.embed(text)]

    q_vecs = token_vectors(query)
    out = []
    for c in candidates:
        d_vecs = token_vectors(c.text)
        maxsim = sum(
            max(sum(x * y for x, y in zip(qv, dv)) for dv in d_vecs)
            for qv in q_vecs
        ) / max(1, len(q_vecs))
        out.append(Candidate(
            source_id=c.source_id, text=c.text, score=max(maxsim, 0.0),
            kind=c.kind, label=c.label, properties=dict(c.properties),
            citations=list(c.citations),
        ))
    out.sort(key=lambda c: (-c.score, c.source_id))
    return out[: top_n or len(out)]


def multi_vector_retrieve(
    query: str,
    fields_by_id: dict[str, dict[str, str]],
    top_n: int = 10,
) -> list[Candidate]:
    """§4 MultiVector: one vector per field; score = max over field vectors."""
    embedder = HashingEmbedder()
    q_vec = embedder.embed(query)
    scored = []
    for cid, fields in fields_by_id.items():
        best = 0.0
        for name, text in fields.items():
            d_vec = embedder.embed(text)
            sim = sum(x * y for x, y in zip(q_vec, d_vec))
            best = max(best, sim)
        scored.append((cid, best))
    scored.sort(key=lambda kv: (-kv[1], kv[0]))
    out = []
    for cid, score in scored[:top_n]:
        out.append(Candidate(source_id=cid, text=cid, score=max(score, 0.0)))
    return out


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def semantic_chunking(text: str, similarity_threshold: float = 0.3) -> list[str]:
    """§4 SemanticChunking: group adjacent sentences by token similarity."""
    sentences = [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]
    if len(sentences) <= 1:
        return [text]
    chunks: list[list[str]] = [[sentences[0]]]
    for prev, cur in zip(sentences, sentences[1:]):
        if overlap_score(prev, cur) >= similarity_threshold:
            chunks[-1].append(cur)
        else:
            chunks.append([cur])
    return [" ".join(c) for c in chunks]


def dynamic_chunking(text: str, target_tokens: int = 120) -> list[str]:
    """§4 DynamicChunking: chunk size adapts to document length."""
    tokens = text.split()
    n = len(tokens)
    if n <= target_tokens:
        return [text]
    # Longer documents get proportionally larger chunks (fewer boundaries).
    size = int(target_tokens * (1.0 + math.log10(n / target_tokens + 1.0)))
    return [" ".join(tokens[i : i + size]) for i in range(0, n, size)]


# ---------------------------------------------------------------------------
# Context processing
# ---------------------------------------------------------------------------


def contextual_retrieval(candidates: list[Candidate], context_fn: Callable[[str], str]) -> list[Candidate]:
    """§4 ContextualRetrieval: prepend entity-specific context to each chunk."""

    def wrap(c: Candidate) -> Candidate:
        context = context_fn(c.source_id)
        return Candidate(
            source_id=c.source_id,
            text=f"{context}\n{c.text}" if context else c.text,
            score=c.score, kind=c.kind, label=c.label,
            properties=dict(c.properties), citations=list(c.citations),
        )

    return [wrap(c) for c in candidates]


def context_compression(candidates: list[Candidate], token_budget: int = 200) -> list[Candidate]:
    """§4 ContextCompression: prune redundant evidence to fit a token budget."""
    out = []
    used = 0
    seen_tokens: set[str] = set()
    for c in sorted(candidates, key=lambda c: (-c.score, c.source_id)):
        tokens = c.text.split()
        novel = [t for t in tokens if t.lower() not in seen_tokens or len(t) > 6]
        if not novel:
            continue  # fully redundant with what we already kept
        cost = len(novel)
        if used + cost > token_budget:
            continue
        used += cost
        seen_tokens.update(t.lower() for t in tokens)
        out.append(Candidate(
            source_id=c.source_id, text=" ".join(novel), score=c.score,
            kind=c.kind, label=c.label, properties=dict(c.properties),
            citations=list(c.citations),
        ))
    return out


def _simhash(text: str, bits: int = 64) -> int:
    vector = [0] * bits
    for tok in set(tokenize(text)):
        digest = int(hashlib.md5(tok.encode(), usedforsecurity=False).hexdigest(), 16)
        for i in range(bits):
            vector[i] += 1 if (digest >> i) & 1 else -1
    out = 0
    for i in range(bits):
        if vector[i] > 0:
            out |= 1 << i
    return out


def _hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def evidence_deduplication(candidates: list[Candidate], threshold_bits: int = 8) -> list[Candidate]:
    """§4 EvidenceDeduplication: simhash near-duplicate removal."""
    out: list[Candidate] = []
    hashes: list[tuple[int, Candidate]] = []
    for c in sorted(candidates, key=lambda c: (-c.score, c.source_id)):
        h = _simhash(c.text)
        if any(_hamming(h, prev) <= threshold_bits for prev, _ in hashes):
            continue
        hashes.append((h, c))
        out.append(c)
    return out


def diversity_mmr(candidates: list[Candidate], top_n: int = 10, lambda_: float = 0.7) -> list[Candidate]:
    """§4 DiversityAware (MMR): relevance vs. novelty trade-off."""

    def sim(a: Candidate, b: Candidate) -> float:
        ta, tb = set(tokenize(a.text)), set(tokenize(b.text))
        if not ta or not tb:
            return 0.0
        return len(ta & tb) / len(ta | tb)

    remaining = list(candidates)
    selected: list[Candidate] = []
    while remaining and len(selected) < top_n:
        best, best_score = None, -math.inf
        for c in remaining:
            redundancy = max((sim(c, s) for s in selected), default=0.0)
            mmr = lambda_ * c.score - (1 - lambda_) * redundancy
            if mmr > best_score:
                best, best_score = c, mmr
        selected.append(best)  # type: ignore[arg-type]
        remaining.remove(best)  # type: ignore[arg-type]
    return selected


def parent_child(
    candidates: list[Candidate],
    parent_fn: Callable[[str], tuple[str, str] | None],
    top_n: int = 10,
) -> list[Candidate]:
    """§4 ParentChild: return parent context for the best matching children."""

    def key(c: Candidate) -> tuple[int, str]:
        return (0 if c.kind == "parent" else 1, c.source_id)

    out: dict[str, Candidate] = {}
    for c in sorted(candidates, key=key):
        link = parent_fn(c.source_id)
        if link is None:
            out.setdefault(c.source_id, c)
            continue
        parent_id, parent_text = link
        existing = out.get(parent_id)
        merged_score = max(existing.score if existing else 0.0, c.score)
        out[parent_id] = Candidate(
            source_id=parent_id, text=parent_text, score=merged_score,
            kind="parent", label=c.label,
            properties=dict(c.properties), citations=list(c.citations),
        )
    ranked = sorted(out.values(), key=lambda c: (-c.score, c.source_id))
    return ranked[:top_n]


# ---------------------------------------------------------------------------
# Metadata & iterative retrieval
# ---------------------------------------------------------------------------


def metadata_aware(
    query: str,
    candidates: list[Candidate],
    filters: dict[str, Any] | None = None,
    boost: dict[str, Any] | None = None,
) -> list[Candidate]:
    """§4 MetadataAware: pre-filter and boost by metadata attributes."""
    filters = filters or {}
    boost = boost or {}
    out = []
    for c in candidates:
        if any(c.properties.get(k) != v for k, v in filters.items()):
            continue
        score = c.score
        if all(c.properties.get(k) == v for k, v in boost.items()):
            score *= 1.5
        out.append(Candidate(
            source_id=c.source_id, text=c.text, score=score, kind=c.kind,
            label=c.label, properties=dict(c.properties), citations=list(c.citations),
        ))
    out.sort(key=lambda c: (-c.score, c.source_id))
    return out


def iterative_rag(
    query: str,
    retrieve: Retriever,
    max_iterations: int = 3,
    top_n: int = 10,
) -> list[Candidate]:
    """§4 IterativeRAG / ActiveRetrieval: reformulate until evidence stabilizes."""
    seen: set[str] = set()
    merged: dict[str, Candidate] = {}
    current = query
    for _ in range(max_iterations):
        batch = retrieve(current, top_n)
        new_ids = [c.source_id for c in batch if c.source_id not in seen]
        for c in batch:
            if c.source_id not in merged or c.score > merged[c.source_id].score:
                merged[c.source_id] = c
            seen.add(c.source_id)
        if not new_ids:
            break
        # Reformulate: add novel evidence terms to the query.
        novel_terms = sorted({t for c in batch[:3] for t in tokenize(c.text)})[:5]
        current = f"{query} {' '.join(novel_terms)}"
    return sorted(merged.values(), key=lambda c: (-c.score, c.source_id))[:top_n]


def ircot(
    query: str,
    retrieve: Retriever,
    steps: int = 3,
    top_n: int = 10,
) -> tuple[list[Candidate], list[str]]:
    """§4 IRCoT: interleaved retrieve / reason steps; returns (candidates, rationale)."""

    def answer_terms(question: str, evidence: list[Candidate]) -> str:
        terms = sorted({t for c in evidence[:2] for t in tokenize(c.text)})[:4]
        return " ".join(terms)

    rationale: list[str] = []
    current = query
    merged: dict[str, Candidate] = {}
    for step in range(steps):
        batch = retrieve(current, top_n)
        for c in batch:
            if c.source_id not in merged or c.score > merged[c.source_id].score:
                merged[c.source_id] = c
        if not batch:
            break
        answer = answer_terms(current, batch)
        rationale.append(f"Step {step + 1}: {answer}")
        current = f"{query} {answer}"
    return sorted(merged.values(), key=lambda c: (-c.score, c.source_id))[:top_n], rationale


def flare(
    query: str,
    retrieve: Retriever,
    confidence_fn: Callable[[list[Candidate]], float] | None = None,
    max_iterations: int = 4,
    threshold: float = 0.5,
    top_n: int = 10,
) -> list[Candidate]:
    """§4 FLARE: forward-looking retrieval re-triggered on low evidence confidence.

    Deterministic fallback confidence = normalized evidence count + score mass.
    """
    if confidence_fn is None:
        def confidence_fn(cands: list[Candidate]) -> float:  # type: ignore[no-redef]
            if not cands:
                return 0.0
            return min(1.0, (len(cands) / top_n) * 0.5 + sum(c.score for c in cands[:5]) * 0.1)

    current = query
    best: list[Candidate] = []
    for _ in range(max_iterations):
        batch = retrieve(current, top_n)
        if confidence_fn(batch) >= threshold:
            return batch
        if len(batch) > len(best):
            best = batch
        current = f"{query} " + " ".join(tokenize(" ".join(c.text for c in batch))[:6])
    return best


# ---------------------------------------------------------------------------
# Verification & trust
# ---------------------------------------------------------------------------


def verification_guided(
    query: str,
    retrieve: Retriever,
    policy: Any,
    store: Any,
    max_attempts: int = 2,
    top_n: int = 10,
) -> dict[str, Any]:
    """§4 VerificationGuided: re-retrieve while the abstention policy abstains.

    Reuses the GAP-KRAG-007/008 machinery (``RAGAbstentionPolicy``) to decide
    whether evidence is sufficient instead of trusting a generation.
    """
    from eoip.graph.rag_router import RAGResult

    attempts = 0
    current = query
    candidates: list[Candidate] = []
    while attempts < max_attempts:
        attempts += 1
        candidates = retrieve(current, top_n)
        result = RAGResult(
            answer="", pattern="verification_guided", confidence=0.5,
            sources=[c.source_id for c in candidates if c.source_id],
        )
        manifest = policy.build_manifest(store, result)
        decision = policy.evaluate(manifest)
        if not decision.abstained:
            return {"candidates": candidates, "verified": True, "attempts": attempts,
                    "confidence": policy.calibrate_confidence(manifest)}
        current = f"{query} " + " ".join(tokenize(" ".join(c.text for c in candidates))[:6])
    return {"candidates": candidates, "verified": False, "attempts": attempts, "confidence": 0.0}


def contradiction_aware(candidates: list[Candidate]) -> dict[str, Any]:
    """§4 ContradictionAware: surface conflicting claims across evidence.

    Deterministic conflict signals: negation polarity flip and same-key
    value disagreements within a fact group (shared source_id prefix).
    """
    _negations = ("not ", "no ", "never ", "fail", "missing", "without")
    conflicts: list[dict[str, Any]] = []
    groups: dict[str, list[Candidate]] = defaultdict(list)
    for c in candidates:
        base = re.sub(r"[:#]\d+$", "", c.source_id)
        groups[base].append(c)
    for base, items in groups.items():
        polarities = [any(n in c.text.lower() for n in _negations) for c in items]
        if len(items) > 1 and any(polarities) and not all(polarities):
            conflicts.append({
                "kind": "polarity",
                "subject": base,
                "sources": [c.source_id for c in items],
            })
        # value disagreement: same property key, differing scalar values
        values: dict[str, set[str]] = defaultdict(set)
        for c in items:
            for k, v in c.properties.items():
                if isinstance(v, (str, int, float)) and k in ("status", "state", "value", "verdict"):
                    values[k].add(str(v))
        for k, vs in values.items():
            if len(vs) > 1:
                conflicts.append({
                    "kind": "value_mismatch",
                    "subject": base,
                    "key": k,
                    "values": sorted(vs),
                })
    return {
        "conflict_count": len(conflicts),
        "conflicts": conflicts,
        "clean": not conflicts,
    }


def confidence_gated(candidates: list[Candidate], policy: Any, store: Any, pattern: str = "confidence_gated") -> dict[str, Any]:
    """§4 ConfidenceGated: abstention integration — gate the answer on evidence."""
    from eoip.graph.rag_router import RAGResult

    result = RAGResult(
        answer="", pattern=pattern, confidence=0.5,
        sources=[c.source_id for c in candidates if c.source_id],
    )
    manifest = policy.build_manifest(store, result)
    decision = policy.evaluate(manifest)
    if decision.abstained:
        return {
            "answer": "Abstained: insufficient evidence to answer reliably.",
            "abstained": True,
            "reasons": decision.reason_codes,
            "confidence": 0.0,
        }
    confidence = policy.calibrate_confidence(manifest)
    return {
        "answer": f"Evidence-backed answer over {len(candidates)} item(s).",
        "abstained": False,
        "confidence": confidence,
        "evidence_manifest": manifest.model_dump(),
    }


def citation_aware(candidates: list[Candidate], claims: list[str] | None = None) -> dict[str, Any]:
    """§4 CitationAware: bind claims to evidence citations; flag unsupported claims."""
    claims = claims or [c.text for c in candidates[:5]]
    supported, unsupported = [], []
    for claim in claims:
        citation = next(
            (c.citations[0] for c in candidates if c.citations and overlap_score(claim, c.text) > 0.05),
            None,
        )
        if citation:
            supported.append({"claim": claim, "citation": citation})
        else:
            unsupported.append(claim)
    return {
        "supported": supported,
        "unsupported": unsupported,
        "citation_accuracy": len(supported) / len(claims) if claims else 1.0,
    }


def cost_adaptive(
    query: str,
    retrieve: Retriever,
    token_budget: int = 400,
    depth_schedule: Iterable[int] = (3, 6, 12, 24),
) -> dict[str, Any]:
    """§4 CostAdaptive: grow retrieval depth while token budget remains."""
    spent = 0
    best: list[Candidate] = []
    depths = list(depth_schedule)
    for depth in depths:
        batch = retrieve(query, depth)
        cost = sum(max(1, len(c.text.split())) for c in batch)
        if spent + cost > token_budget and best:
            break
        spent += cost
        best = batch
    return {"candidates": best, "tokens_spent": spent, "depth": len(best)}


# Public alias (§4 table name)
multi_vector = multi_vector_retrieve


TECHNIQUES: dict[str, Callable[..., Any]] = {
    "rag_fusion": rag_fusion,
    "reciprocal_rank_fusion": reciprocal_rank_fusion,
    "parent_child": parent_child,
    "contextual_retrieval": contextual_retrieval,
    "query_expansion": query_expansion,
    "query_decomposition": query_decomposition,
    "step_back": step_back,
    "cross_encoder_rerank": cross_encoder_rerank,
    "late_interaction": late_interaction,
    "multi_vector": multi_vector_retrieve,
    "metadata_aware": metadata_aware,
    "semantic_chunking": semantic_chunking,
    "dynamic_chunking": dynamic_chunking,
    "context_compression": context_compression,
    "evidence_deduplication": evidence_deduplication,
    "diversity_mmr": diversity_mmr,
    "hyde": hyde_query,
    "flare": flare,
    "ircot": ircot,
    "iterative_rag": iterative_rag,
    "verification_guided": verification_guided,
    "contradiction_aware": contradiction_aware,
    "confidence_gated": confidence_gated,
    "citation_aware": citation_aware,
    "cost_adaptive": cost_adaptive,
}
