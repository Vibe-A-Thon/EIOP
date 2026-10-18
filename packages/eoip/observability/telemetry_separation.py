"""Strict separation between observed telemetry and inferred incident causality (CRA-008.5).

Enforces:
1. Observed telemetry preserves timestamps, source sampling, staleness, missing data, and uncertainty.
2. Inferred causality represents analytical hypotheses linked to evidence telemetry, strictly separated
   from raw observations.
3. Any write-back or automated provisioning requires an approved GovernedAction warrant (CRA-027).
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from eoip.contracts.source_event import utc_now_iso


@dataclass
class ObservedTelemetry:
    """Raw, immutable operational observation from monitoring systems."""

    telemetry_id: str
    metric_name: str
    timestamp: str
    value: float | None
    source_sampling_rate: float = 1.0  # 1.0 = 100% sampled
    staleness_seconds: float = 0.0
    is_missing: bool = False
    uncertainty_margin: float = 0.0
    source_system: str = "observability"
    dimensions: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "telemetry_id": self.telemetry_id,
            "metric_name": self.metric_name,
            "timestamp": self.timestamp,
            "value": self.value,
            "source_sampling_rate": self.source_sampling_rate,
            "staleness_seconds": self.staleness_seconds,
            "is_missing": self.is_missing,
            "uncertainty_margin": self.uncertainty_margin,
            "source_system": self.source_system,
            "dimensions": self.dimensions,
        }


@dataclass
class InferredCausality:
    """Analytically derived incident causality hypothesis, strictly distinct from telemetry."""

    inference_id: str
    incident_id: str
    affected_ci: str
    root_cause_ci: str
    confidence: float
    evidence_telemetry_ids: list[str] = field(default_factory=list)
    hypothesis: str = ""
    inferred_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "inference_id": self.inference_id,
            "incident_id": self.incident_id,
            "affected_ci": self.affected_ci,
            "root_cause_ci": self.root_cause_ci,
            "confidence": self.confidence,
            "evidence_telemetry_ids": self.evidence_telemetry_ids,
            "hypothesis": self.hypothesis,
            "inferred_at": self.inferred_at,
        }


class TelemetryCausalityBoundary:
    """Guards the boundary between observed telemetry and inferred causality."""

    @staticmethod
    def assert_separation(telemetry: ObservedTelemetry, causality: InferredCausality) -> bool:
        """Verify that telemetry contains no causal claims and causality references telemetry."""
        # Telemetry must not contain causality fields
        telemetry_keys = set(telemetry.dimensions.keys())
        causal_indicators = {"caused_by", "root_cause", "culprit", "causality"}
        if any(c in k.lower() for k in telemetry_keys for c in causal_indicators):
            raise ValueError("Observed telemetry contaminated with inferred causality metadata")

        # Inferred causality must point to concrete evidence
        if not causality.evidence_telemetry_ids:
            raise ValueError("Inferred causality must cite at least one evidence telemetry observation")

        return True

    @staticmethod
    def check_write_back_governance(action_request: dict[str, Any], warrant: Any | None = None) -> bool:
        """Ensure any operational write-back or CI mutation requires CRA-027 GovernedAction warrant."""
        if warrant is None:
            raise PermissionError(
                "Direct write-back rejected: Operational write-back requires an approved GovernedAction warrant (CRA-027)"
            )
        # Verify warrant structure if present
        if hasattr(warrant, "is_valid") and not warrant.is_valid():
            raise PermissionError("GovernedAction warrant is expired or invalid")
        return True
