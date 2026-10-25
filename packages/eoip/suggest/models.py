"""Contracts for the NL suggestion engine (SR-NLQ-002, SR-NLQ-003, SR-NLQ-004).

Every suggestion is a *candidate interpretation*: a deterministic parse of a
natural-language question into a ``QueryPlan`` preview plus UX metadata
(paraphrase, result shape, entity bindings with alternatives, cost/latency
tier, confidence, data-coverage note, permission pre-check). No candidate is
executed here — the user selects and fires one (SR-NLQ-002).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from eoip.contracts.query_plan import QueryPlan

AnswerMode = Literal["deterministic", "narrated", "exploratory", "report"]
CostTierName = Literal["fast", "moderate", "heavy", "expensive"]

COST_TIERS: dict[CostTierName, dict[str, Any]] = {
    "fast": {"estimated_latency_ms": 200, "max_depth": 1, "description": "point lookup or direct neighbor read"},
    "moderate": {"estimated_latency_ms": 800, "max_depth": 3, "description": "bounded traversal over a small neighborhood"},
    "heavy": {"estimated_latency_ms": 3000, "max_depth": 5, "description": "multi-hop impact or lineage traversal"},
    "expensive": {"estimated_latency_ms": 10000, "max_depth": 8, "description": "graph-wide similarity, coverage or aggregation scan"},
}

INTENT_PLAN_PERMISSIONS: dict[str, list[str]] = {
    "lookup": ["graph:read"],
    "traversal": ["graph:read"],
    "impact": ["graph:read"],
    "ownership": ["graph:read"],
    "change-history": ["graph:read"],
    "coverage": ["graph:read"],
    "temporal": ["graph:read"],
    "aggregation": ["graph:read"],
    "similarity": ["graph:read"],
    "explain-why": ["graph:read"],
}


class EntityAlternative(BaseModel):
    """One candidate entity for an ambiguous mention (SR-NLQ-003)."""

    model_config = ConfigDict(extra="forbid")

    entity_id: str
    display_name: str
    entity_type: str | None = None
    source_system: str | None = None
    environment: str | None = None
    match_basis: str = "name"  # name | alias | canonical_id | fuzzy
    match_score: float = Field(ge=0.0, le=1.0)


class EntityBinding(BaseModel):
    """Mention -> resolved entity plus the alternatives the user may pin."""

    model_config = ConfigDict(extra="forbid")

    mention: str
    role: str = "subject"  # subject | target | owner | scope
    resolved: EntityAlternative | None = None
    alternatives: list[EntityAlternative] = Field(default_factory=list)
    ambiguous: bool = False
    pinned: bool = False  # resolved from the user's session pin (SR-NLQ-003)


class PermissionNote(BaseModel):
    """Pre-check of the authz permissions a plan will need (SR-NLQ-002)."""

    model_config = ConfigDict(extra="forbid")

    permissions: list[str] = Field(default_factory=list)
    evaluated: bool = False
    allowed: bool | None = None
    note: str = ""


class CandidateInterpretation(BaseModel):
    """One ranked candidate interpretation of the question (SR-NLQ-002)."""

    model_config = ConfigDict(extra="forbid")

    candidate_id: str
    intent: str
    paraphrase: str
    plan_preview: QueryPlan
    result_shape: dict[str, Any]
    entity_bindings: list[EntityBinding] = Field(default_factory=list)
    cost_tier: CostTierName
    estimated_latency_ms: int
    confidence: float = Field(ge=0.0, le=1.0)
    data_coverage_note: str = ""
    permissions: PermissionNote = Field(default_factory=PermissionNote)
    answer_mode: AnswerMode = "deterministic"
    source: Literal["template", "llm_assist"] = "template"


class SuggestionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str = Field(min_length=1)
    session_id: str | None = None
    user_id: str | None = None
    roles: list[str] = Field(default_factory=list)
    limit: int = Field(default=5, ge=1, le=20)


class PinRequest(BaseModel):
    """Pin one candidate entity for a mention for the rest of the session (SR-NLQ-003)."""

    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(min_length=1)
    mention: str = Field(min_length=1)
    entity_id: str = Field(min_length=1)


class SuggestionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str
    candidates: list[CandidateInterpretation]
    llm_assist_used: bool = False
    parse: dict[str, Any] = Field(default_factory=dict)


def choose_answer_mode(intent: str, *, multi_step: bool = False, long_form: bool = False) -> AnswerMode:
    """Deterministic answer-mode labeling (SR-NLQ-004).

    Tier-1 deterministic intents compute straight from the graph; open-ended or
    multi-step intents are labeled exploratory; report mode is reserved for
    explicit long-form aggregation requests.
    """
    if long_form or intent in ("report",):
        return "report"
    if multi_step or intent in ("explain-why", "similarity"):
        return "exploratory"
    if intent in ("lookup", "traversal", "impact", "ownership", "change-history",
                  "temporal", "aggregation", "coverage"):
        return "deterministic"
    return "narrated"
