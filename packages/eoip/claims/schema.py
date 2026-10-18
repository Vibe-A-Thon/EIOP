"""Typed schemas for claims, competitive positioning, and disclosure governance (CRA-041)."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class ClaimStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    BLOCKED = "BLOCKED"


class ClaimScope(BaseModel):
    profile: str = "P0"  # P0, P1, P2, all
    edition: str = "all"  # community, enterprise, all
    deployment: str = "all"  # cloud, on-prem, air-gap, all


class ClaimApproval(BaseModel):
    role: str  # Legal, Marketing, Engineering, Lead Developer
    reviewer: str
    status: str = "APPROVED"  # APPROVED, REJECTED, PENDING
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: Optional[str] = None

    @field_validator("timestamp", mode="before")
    def parse_timestamp(cls, v: Any) -> datetime:
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v


class EvidenceReference(BaseModel):
    kind: str  # ledger_clause, benchmark_receipt, competitor_review, legal_decision
    ref_id: str  # e.g. CRA-020.1, CRA-042.1, H-12
    sha256: Optional[str] = None
    notes: Optional[str] = None


class ClaimRecord(BaseModel):
    id: str
    wording: str
    category: str = "general"  # standards, inversion, positioning, competitor, patent, scorecard, general
    scope: ClaimScope = Field(default_factory=ClaimScope)
    evidence_refs: List[EvidenceReference] = Field(default_factory=list)
    owner: str
    approvals: List[ClaimApproval] = Field(default_factory=list)
    expiry: datetime
    status: ClaimStatus = ClaimStatus.DRAFT
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("expiry", mode="before")
    def parse_expiry(cls, v: Any) -> datetime:
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v

    def is_expired(self, current_time: Optional[datetime] = None) -> bool:
        now = current_time or datetime.now(timezone.utc)
        return self.expiry <= now

    def has_approval(self, role: str) -> bool:
        return any(
            app.role.lower() == role.lower() and app.status.upper() == "APPROVED"
            for app in self.approvals
        )


class PatentCandidateRecord(BaseModel):
    candidate_id: str  # PAT-001 .. PAT-005
    title: str
    mechanism_summary: str
    legal_decision_id: Optional[str] = "H-12"
    legal_decision_status: str = "PENDING"  # PENDING, APPROVED_PROVISIONAL, TRADE_SECRET_RESTRICTED, REJECTED
    public_disclosure_permitted: bool = False
    filing_reference: Optional[str] = None
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CompetitorDataPoint(BaseModel):
    competitor: str
    metric: str  # TCO, pricing, throughput, latency
    value: str
    source: str
    is_vendor_source: bool = True
    verification_status: str = "UNVERIFIED"  # UNVERIFIED, INDEPENDENTLY_VERIFIED
    legal_approved: bool = False
    permitted_for_external_use: bool = False


class ScorecardRecord(BaseModel):
    matrix_name: str
    self_score: str  # e.g. "2.9", "3.6", "4.2"
    purpose: str = "INTERNAL_PLANNING_ONLY"  # INTERNAL_PLANNING_ONLY, EXTERNAL_PUBLICATION
    cra_042_rescored: bool = False
    scoring_method: Optional[str] = None
    scoring_date: Optional[str] = None
    evidence_confidence: Optional[str] = None
