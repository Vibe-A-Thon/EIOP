"""Retrieval evaluation metrics for the RAG extensions (gap analysis §4).

Extends ``eoip.retrieval.eval`` (FR-RAG-005) with ranking-quality metrics:
Recall@K, Precision@K, MRR, nDCG, citation accuracy and access-control
correctness. All metrics are pure functions over fixture rankings, so tests
and benchmarks need no model.
"""

from __future__ import annotations

from typing import Any, Iterable


def _as_ids(ranking: Iterable[Any]) -> list[str]:
    out = []
    for item in ranking:
        if isinstance(item, str):
            out.append(item)
        elif isinstance(item, dict):
            out.append(str(item.get("source_id") or item.get("canonical_id") or ""))
        else:
            out.append(str(getattr(item, "source_id", item)))
    return [i for i in out if i]


def recall_at_k(ranking: list[Any], relevant: set[str], k: int) -> float:
    """§4 Recall@K: share of relevant items present in the top-K."""
    if not relevant:
        return 1.0
    top = set(_as_ids(ranking)[:k])
    return len(top & relevant) / len(relevant)


def precision_at_k(ranking: list[Any], relevant: set[str], k: int) -> float:
    """§4 Precision@K: share of top-K items that are relevant."""
    top = _as_ids(ranking)[:k]
    if not top:
        return 0.0
    return len(set(top) & relevant) / len(top)


def mean_reciprocal_rank(rankings: list[list[Any]], relevant_sets: list[set[str]]) -> float:
    """§4 MRR: mean reciprocal rank of the first relevant item per query."""
    if not rankings:
        return 0.0
    total = 0.0
    for ranking, relevant in zip(rankings, relevant_sets):
        rr = 0.0
        for idx, cid in enumerate(_as_ids(ranking)):
            if cid in relevant:
                rr = 1.0 / (idx + 1)
                break
        total += rr
    return total / len(rankings)


def ndcg_at_k(ranking: list[Any], relevance: dict[str, float], k: int) -> float:
    """§4 nDCG@K: normalized discounted cumulative gain with graded relevance."""
    top = _as_ids(ranking)[:k]

    def dcg(ids: list[str]) -> float:
        return sum((2.0 ** relevance.get(cid, 0.0) - 1.0) / _log2(i + 2) for i, cid in enumerate(ids))

    ideal = sorted(relevance, key=lambda cid: -relevance[cid])[:k]
    denom = dcg(ideal)
    return dcg(top) / denom if denom > 0 else 0.0


def citation_accuracy(claims: list[dict[str, Any]]) -> float:
    """§4 citation accuracy: fraction of claims whose citation resolves to real evidence.

    Each claim dict: ``{"claim": str, "citation": str|None, "valid_citations": set/list | None}``.
    When ``valid_citations`` is provided, the citation must be a member; when
    omitted any non-empty citation counts as accurate.
    """
    if not claims:
        return 1.0
    accurate = 0
    for claim in claims:
        citation = claim.get("citation")
        if not citation:
            continue
        valid = claim.get("valid_citations")
        if valid is None or citation in valid:
            accurate += 1
    return accurate / len(claims)


def access_control_correctness(
    returned_ids: list[str],
    allowed_ids: set[str],
    denied_ids: set[str] | None = None,
) -> dict[str, Any]:
    """§4 access-control correctness: no denied leak + allowed coverage.

    ``denied_ids`` (items the requester must never see) must be absent from
    ``returned_ids``; ``allowed_ids`` (items they may see) measures coverage.
    """
    denied_ids = denied_ids or set()
    returned = set(returned_ids)
    leaked = sorted(returned & denied_ids)
    coverage = len(returned & allowed_ids) / len(allowed_ids) if allowed_ids else 1.0
    return {
        "leaked": leaked,
        "leak_count": len(leaked),
        "allowed_coverage": coverage,
        "correct": not leaked,
    }


def _log2(x: float) -> float:
    import math

    return math.log(x, 2)


METRICS = {
    "recall_at_k": recall_at_k,
    "precision_at_k": precision_at_k,
    "mrr": mean_reciprocal_rank,
    "ndcg_at_k": ndcg_at_k,
    "citation_accuracy": citation_accuracy,
    "access_control_correctness": access_control_correctness,
}
