"""Acquisition-layer conflict preservation helpers (G2-EKAF-022)."""

from __future__ import annotations

import hashlib

from eoip.contracts.source_event import utc_now_iso
from eoip.truth import Claim, TruthStore
from pydantic import BaseModel, ConfigDict, Field


class SourceFactAssertion(BaseModel):
    """A source-owned fact assertion awaiting truth-layer resolution."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1, max_length=128)
    subject_id: str = Field(min_length=1, max_length=512)
    predicate: str = Field(min_length=1, max_length=256)
    value: str = Field(min_length=1, max_length=4096)
    source_authority: float = Field(default=0.5, ge=0.0, le=1.0)
    extraction_confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    validation_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    observed_at: str = Field(default_factory=utc_now_iso)
    evidence_ref: str | None = Field(default=None, max_length=2048)


class PreservedConflictSet(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject_id: str
    predicate: str
    claims: list[Claim]
    conflicting: bool


def preserve_source_claims(
    truth_store: TruthStore,
    assertions: list[SourceFactAssertion],
) -> list[PreservedConflictSet]:
    """Store all source assertions as claims and leave canonical choice to truth policies."""

    groups: dict[tuple[str, str], list[Claim]] = {}
    for assertion in assertions:
        claim = Claim(
            claim_id=_claim_id(assertion),
            subject_id=assertion.subject_id,
            predicate=assertion.predicate,
            value=assertion.value,
            source_id=assertion.source_id,
            source_authority=assertion.source_authority,
            extraction_confidence=assertion.extraction_confidence,
            validation_confidence=assertion.validation_confidence,
            asserted_at=assertion.observed_at,
        )
        truth_store.add_claim(claim)
        groups.setdefault((claim.subject_id, claim.predicate), []).append(claim)

    preserved: list[PreservedConflictSet] = []
    for subject_id, predicate in sorted(groups):
        claims = truth_store.claims_for(subject_id, predicate)
        preserved.append(
            PreservedConflictSet(
                subject_id=subject_id,
                predicate=predicate,
                claims=claims,
                conflicting=bool(truth_store.find_contradictions(subject_id, predicate)),
            )
        )
    return preserved


def _claim_id(assertion: SourceFactAssertion) -> str:
    digest = hashlib.sha256(
        "|".join(
            (
                assertion.source_id,
                assertion.subject_id,
                assertion.predicate,
                assertion.value,
                assertion.observed_at,
                assertion.evidence_ref or "",
            )
        ).encode("utf-8")
    ).hexdigest()[:32]
    return f"urn:eoip:truth:claim:{digest}"
