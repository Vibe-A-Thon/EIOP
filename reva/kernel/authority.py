"""Authority, epistemic states, confidence bands, verification depths and coverage status (T-104 / §6.6 / §6.7)."""

from __future__ import annotations

from enum import Enum


class Authority(str, Enum):
    SOURCE_SYSTEM_RECORD = "source_system_record"
    SOURCE_CODE_STATIC = "source_code_static"
    SHIPPED_ARTIFACT = "shipped_artifact"
    RUNTIME_OBSERVED = "runtime_observed"
    CONTROLLED_EXECUTION = "controlled_execution"
    HUMAN_ATTESTED = "human_attested"
    RULE_DERIVED = "rule_derived"
    MODEL_INFERRED = "model_inferred"
    HISTORICAL_REFERENCE = "historical_reference"
    EXTERNAL_SERVICE = "external_service"


class Epistemic(str, Enum):
    OBSERVED = "observed"
    DERIVED = "derived"
    INFERRED = "inferred"
    UNKNOWN = "unknown"
    UNAVAILABLE = "unavailable"


class ConfidenceBand(str, Enum):
    EXACT = "exact"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class Depth(str, Enum):
    STATIC = "static"
    UNIT = "unit"
    COMPONENT = "component"
    INTEGRATION = "integration"
    ACCEPTANCE = "acceptance"
    DEPLOYED = "deployed"
    PRODUCTION_OBSERVED = "production_observed"

    @property
    def rank(self) -> int:
        _order = {
            "static": 0,
            "unit": 1,
            "component": 2,
            "integration": 3,
            "acceptance": 4,
            "deployed": 5,
            "production_observed": 6,
        }
        return _order[self.value]

    def __ge__(self, other: Depth) -> bool:
        if not isinstance(other, Depth):
            return NotImplemented
        return self.rank >= other.rank

    def __gt__(self, other: Depth) -> bool:
        if not isinstance(other, Depth):
            return NotImplemented
        return self.rank > other.rank

    def __le__(self, other: Depth) -> bool:
        if not isinstance(other, Depth):
            return NotImplemented
        return self.rank <= other.rank

    def __lt__(self, other: Depth) -> bool:
        if not isinstance(other, Depth):
            return NotImplemented
        return self.rank < other.rank


class CoverageStatus(str, Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    UNKNOWN = "unknown"
    UNAVAILABLE = "unavailable"

    @property
    def rank(self) -> int:
        _order = {
            "unavailable": 0,
            "unknown": 1,
            "partial": 2,
            "complete": 3,
        }
        return _order[self.value]
