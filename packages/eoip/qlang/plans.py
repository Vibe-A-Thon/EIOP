"""QLang plan IR: the shared intermediate representation all qlang front-ends compile to.

Every real parser in this package produces a ``QLangPlan``. Graph-shaped plans
(SEARCH / PATH / NEIGHBORHOOD / IMPACT) can be lowered to the platform
``QueryPlan`` contract (``eoip.contracts.query_plan``) for policy-checked
execution via ``eoip.query.executor.QueryExecutor``; payload-shaped plans
(PROJECT / FILTER / AGGREGATE) execute over caller-supplied fixtures via
``eoip.qlang.executor``.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from eoip.contracts.query_plan import QueryPlan as EOIPQueryPlan

PlanIntent = Literal[
    "SEARCH",       # find vertices matching filters
    "PATH",         # bounded path between two anchors
    "NEIGHBORHOOD", # 1..n hop traversal from anchors
    "IMPACT",       # downstream traversal
    "PROJECT",      # project fields over payload rows
    "FILTER",       # select payload rows
    "AGGREGATE",    # group + aggregate payload rows
]

_INTENT_TO_QUERY_PLAN = {
    "SEARCH": "SEARCH",
    "PATH": "PATH",
    "NEIGHBORHOOD": "NEIGHBORHOOD",
    "IMPACT": "IMPACT",
}


class QLangPlan(BaseModel):
    """Compiled query-language plan (front-end neutral IR)."""

    language: str
    intent: PlanIntent
    operation: str = Field(default="", description="front-end-specific operation name")
    source: str = Field(default="", description="original query text")
    projection: list[str] = Field(default_factory=list)
    filters: dict[str, Any] = Field(default_factory=dict)
    anchors: list[str] = Field(default_factory=list)
    edge_labels: list[str] = Field(default_factory=list)
    min_hops: int = Field(default=1, ge=0)
    max_hops: int = Field(default=1, ge=0, le=8)
    order_by: list[str] = Field(default_factory=list)
    group_by: list[str] = Field(default_factory=list)
    aggregates: dict[str, str] = Field(default_factory=dict, description="alias -> function")
    limit: int = Field(default=50, ge=1, le=500)
    extra: dict[str, Any] = Field(default_factory=dict, description="front-end-specific IR nodes")

    def to_query_plan(self) -> EOIPQueryPlan:
        """Lower a graph-shaped plan to the platform QueryPlan contract.

        Payload intents (PROJECT/FILTER/AGGREGATE over fixtures) are not
        graph traversals and raise ``QLangNotMappableError`` honestly.
        """
        if self.intent not in _INTENT_TO_QUERY_PLAN:
            raise QLangNotMappableError(
                f"intent {self.intent!r} is payload-shaped and has no QueryPlan mapping"
            )
        if self.intent == "PATH" and len(self.anchors) < 2:
            raise QLangNotMappableError("PATH intent requires exactly 2 anchors")
        intent = _INTENT_TO_QUERY_PLAN[self.intent]
        # An anchor-less traversal (e.g. g.V().hasLabel(...).out(...)) is a
        # label-scoped vertex search, not a seeded traversal — lower it
        # honestly to SEARCH rather than emitting an unexecutable plan.
        if intent in ("NEIGHBORHOOD", "IMPACT", "PATH") and not self.anchors:
            intent = "SEARCH"
        return EOIPQueryPlan(
            intent=intent,  # type: ignore[arg-type]
            anchors=list(self.anchors),
            relationship_allowlist=list(self.edge_labels) or None,
            max_depth=max(1, min(self.max_hops, 8)),
            result_limit=max(1, min(self.limit, 500)),
            evidence_mode="SUMMARY",
            filters=dict(self.filters) or None,
        )


class QLangParseError(ValueError):
    """Raised when a query cannot be parsed by a real front-end parser."""


class QLangNotMappableError(ValueError):
    """Raised when a plan cannot be lowered to the platform QueryPlan IR."""
