"""
Core Neural Schema Models & Contracts (NS-P0, T-NS-001).
Implements Pydantic v2 schema models with extra="forbid", deterministic sch1_... IDs,
and epistemic state tracking.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

from reva.core.ids import schema_id


class SlotConstraint(BaseModel):
    """Defines a slot in a neural schema with structural constraints."""
    model_config = ConfigDict(extra="forbid")

    name: str
    required: bool = True
    allowed_types: List[str] = Field(default_factory=lambda: ["str", "int", "float", "bool", "dict", "list"])
    regex_pattern: Optional[str] = None
    epistemic_default: str = "inferred"

    def validate_value(self, val: Any) -> bool:
        """Validates that a provided value conforms to slot constraints."""
        py_type = type(val).__name__
        if py_type not in self.allowed_types:
            return False
        if self.regex_pattern and isinstance(val, str):
            if not re.search(self.regex_pattern, val):
                return False
        return True


class NeuralSchema(BaseModel):
    """
    Cognitive neural schema representing an abstract structural template.
    Carries deterministic sch1_[0-9a-f]{64} identifier.
    """
    model_config = ConfigDict(extra="forbid")

    schema_id: str
    name: str
    domain: str
    slots: Dict[str, SlotConstraint] = Field(default_factory=dict)
    planes: List[str] = Field(default_factory=lambda: ["GL0", "GL1", "GL2", "GL3", "GW"])
    warrant_ref: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @classmethod
    def create(
        cls,
        name: str,
        domain: str,
        slots: Dict[str, SlotConstraint],
        planes: Optional[List[str]] = None,
        warrant_ref: Optional[str] = None,
    ) -> NeuralSchema:
        """Factory method that computes canonical sch1_... ID deterministically."""
        body = {
            "name": name,
            "domain": domain,
            "slots": {k: s.model_dump(mode="json") for k, s in sorted(slots.items())},
            "planes": sorted(planes or ["GL0", "GL1", "GL2", "GL3", "GW"]),
        }
        sch_id = schema_id(body)
        return cls(
            schema_id=sch_id,
            name=name,
            domain=domain,
            slots=slots,
            planes=planes or ["GL0", "GL1", "GL2", "GL3", "GW"],
            warrant_ref=warrant_ref,
        )


class AssimilationResult(BaseModel):
    """Outcome of attempting to assimilate an entity instance into a neural schema."""
    model_config = ConfigDict(extra="forbid")

    schema_id: str
    status: str  # "assimilated", "novel_gap_routed", "rejected"
    confidence: float
    filled_slots: Dict[str, Any]
    missing_slots: List[str] = Field(default_factory=list)
    latency_ms: float
    epistemic_state: str = "inferred"
    gap_id: Optional[str] = None


class EvaluationReport(BaseModel):
    """Statistical verification report for a Neural Schema benchmark."""
    model_config = ConfigDict(extra="forbid")

    schema_id: str
    benchmark_queries: int
    p_value: float
    accuracy: float
    verified: bool
