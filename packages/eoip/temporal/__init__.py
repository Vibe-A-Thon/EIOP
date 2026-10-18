"""Temporal Knowledge, Impact and Simulation Package (CRA-028.1-028.9, CRA-028.A).

Exports clean contracts for bitemporal navigation, authorized as-of queries,
deterministic algorithms, and governed impact simulation.
"""

from __future__ import annotations

from eoip.temporal.authorized_as_of import (
    AuthorizedAsOfEngine,
    AuthorizedHistoricalSnapshot,
    HistoricalAccessDeniedError,
)
from eoip.temporal.deterministic_graph import (
    DeterministicGraphAlgorithms,
    HopEvidence,
    PathResult,
)
from eoip.temporal.impact_simulator import (
    DualPathImpactReport,
    ImpactCategory,
    ImpactSimulator,
    ImpactedEntity,
    ProductionAssertionBlockedError,
    SeverityLevel,
    SimulationProtocol,
    SimulationResult,
)
from eoip.temporal.models import (
    BitemporalEntityRecord,
    CorrectionRecord,
    RetentionPolicy,
    RetractionRecord,
    TimeRange,
    reconcile_late_event,
)

__all__ = [
    "AuthorizedAsOfEngine",
    "AuthorizedHistoricalSnapshot",
    "BitemporalEntityRecord",
    "CorrectionRecord",
    "DeterministicGraphAlgorithms",
    "DualPathImpactReport",
    "HistoricalAccessDeniedError",
    "HopEvidence",
    "ImpactCategory",
    "ImpactSimulator",
    "ImpactedEntity",
    "PathResult",
    "ProductionAssertionBlockedError",
    "RetentionPolicy",
    "RetractionRecord",
    "SeverityLevel",
    "SimulationProtocol",
    "SimulationResult",
    "TimeRange",
    "reconcile_late_event",
]
