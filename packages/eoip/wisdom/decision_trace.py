"""Decision Trace schema and entities for Wisdom Graph (WG-WP-01..05)."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DecisionOption(BaseModel):
    option_id: str
    description: str
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)
    projected_impact: Dict[str, float] = Field(default_factory=dict)  # metric -> expected value


class DecisionOutcome(BaseModel):
    outcome_id: str
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actual_metrics: Dict[str, float] = Field(default_factory=dict)
    lessons_learned: str
    evaluated_by: str
    variance_analysis: Dict[str, float] = Field(default_factory=dict)


class DecisionTrace(BaseModel):
    trace_id: str
    tenant_id: str = "acme-demo"
    title: str
    situation: str
    context_tags: List[str] = Field(default_factory=list)
    options: List[DecisionOption] = Field(default_factory=list)
    selected_option_id: str
    rationale: str
    precedent_ids: List[str] = Field(default_factory=list)
    decided_by: str
    decided_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    warrant_refs: List[str] = Field(default_factory=list)
    status: str = "RECORDED"  # RECORDED, OUTCOME_EVALUATED, SUPERSEDED, REFUTED
    outcomes: List[DecisionOutcome] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def digest(self) -> str:
        data = {
            "trace_id": self.trace_id,
            "tenant_id": self.tenant_id,
            "title": self.title,
            "situation": self.situation,
            "selected_option_id": self.selected_option_id,
            "rationale": self.rationale,
            "decided_by": self.decided_by,
            "decided_at": self.decided_at.isoformat(),
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()
