"""Claim/truth conflict model contracts.

Implements GAP-TRUTH-001..010: claims are immutable, conflicts are detected
between claims on the same subject+predicate with differing values, and a
resolution policy selects a canonical assertion. Rejected/obsolete claims are
retained for audit (TRUTH-009).
"""

from __future__ import annotations

from eoip.contracts.source_event import utc_now_iso
from pydantic import BaseModel, Field


class Claim(BaseModel):
    """A single asserted fact extracted or provided by one source (TRUTH-001).

    Claims are never mutated or overwritten; conflicts create a new
    resolution decision instead (TRUTH-002).
    """

    claim_id: str = Field(..., description="URN: urn:eoip:truth:claim:<id>")
    subject_id: str = Field(..., description="Canonical entity URN the claim is about")
    predicate: str = Field(..., description="Attribute/relationship name asserted")
    value: str = Field(..., description="Asserted value (string-serialised)")
    source_id: str = Field(..., description="URN of the source that produced the claim")
    source_authority: float = Field(..., ge=0.0, le=1.0, description="Trust in the source, 0..1")
    extraction_confidence: float = Field(..., ge=0.0, le=1.0)
    validation_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    asserted_at: str = Field(default_factory=utc_now_iso)
    status: str = Field(
        default="pending",
        description="pending | accepted | rejected | obsolete (TRUTH-009)",
    )

    def composite_score(self) -> float:
        """Combined confidence used by ranking policies."""
        validation = self.validation_confidence if self.validation_confidence is not None else 0.0
        return round(self.source_authority * self.extraction_confidence * (0.5 + 0.5 * validation), 6)


class CanonicalAssertion(BaseModel):
    """The currently resolved fact for a (subject, predicate) pair (TRUTH-003)."""

    assertion_id: str = Field(..., description="URN: urn:eoip:truth:assertion:<id>")
    subject_id: str
    predicate: str
    value: str
    chosen_claim_id: str
    decision_id: str
    resolved_at: str = Field(default_factory=utc_now_iso)


class ResolutionDecision(BaseModel):
    """Record of how a conflict was resolved (TRUTH-004/007/008/010)."""

    decision_id: str = Field(..., description="URN: urn:eoip:truth:decision:<id>")
    subject_id: str
    predicate: str
    policy: str = Field(
        ...,
        description="highest-authority | highest-confidence | newest | manual (TRUTH-007/008)",
    )
    chosen_claim_id: str
    competing_claim_ids: list[str] = Field(default_factory=list)
    rationale: str = Field(..., description="Human/machine readable justification (TRUTH-010)")
    adjudicator: str | None = Field(default=None, description="Human adjudicator id, if manual")
    decided_at: str = Field(default_factory=utc_now_iso)
