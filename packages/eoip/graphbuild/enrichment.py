"""Incremental enrichment loop: apply validated additions only.

An ``EnrichmentLoop`` takes builder deltas (co-change, similarity, link
prediction, hierarchy, mentions, inclusion dependencies), runs each proposed
edge through a validator, and applies only approved additions to an
in-memory graph view. Unvalidated proposals stay in the review queue with
their rejection reasons. Deterministic ordering; no mandatory LLM — a
validator callable is optional and defaults to score-threshold approval.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, ConfigDict

from eoip.graphbuild.models import GraphDelta, ProposedEdge

Validator = Callable[[ProposedEdge], bool]
"""Approval predicate; default accepts score >= min_score."""


class ReviewItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    edge: ProposedEdge
    status: str = "pending"  # pending | applied | rejected
    reason: str = ""


class EnrichmentLoop:
    """Validated-only incremental enrichment over a graph view."""

    def __init__(self, validator: Validator | None = None, *, min_score: float = 0.0):
        self._validator = validator
        self._min_score = min_score
        self._vertices: dict[str, dict[str, Any]] = {}
        self._edges: dict[str, ProposedEdge] = {}
        self._review: list[ReviewItem] = []

    # -- graph view ------------------------------------------------------------
    def add_vertex(self, vertex_id: str, **properties: Any) -> None:
        self._vertices[vertex_id] = properties

    def snapshot(self) -> dict[str, Any]:
        return {
            "vertices": sorted(self._vertices),
            "edges": [edge.model_dump() for _, edge in sorted(self._edges.items())],
            "review_queue": len(self._review),
        }

    # -- validation --------------------------------------------------------------
    def _approve(self, edge: ProposedEdge) -> tuple[bool, str]:
        if edge.from_id == edge.to_id:
            return False, "self-loop"
        if edge.edge_id in self._edges:
            return False, "duplicate"
        if self._validator is not None:
            return (True, "validator-approved") if self._validator(edge) else (False, "validator-rejected")
        if edge.score < self._min_score:
            return False, f"score {edge.score} below threshold {self._min_score}"
        return True, "threshold-approved"

    # -- loop ---------------------------------------------------------------------
    def submit(self, delta: GraphDelta) -> dict[str, int]:
        """Submit one builder delta; validated additions apply immediately."""
        applied = rejected = 0
        for edge in sorted(delta.edges, key=lambda e: (e.from_id, e.to_id, e.method)):
            ok, reason = self._approve(edge)
            if ok:
                self._edges[edge.edge_id] = edge
                self._review.append(ReviewItem(edge=edge, status="applied", reason=reason))
                applied += 1
            else:
                self._review.append(ReviewItem(edge=edge, status="rejected", reason=reason))
                rejected += 1
        return {"applied": applied, "rejected": rejected}

    def review_queue(self) -> list[ReviewItem]:
        return list(self._review)

    def pending(self) -> list[ReviewItem]:
        return [item for item in self._review if item.status == "pending"]
