"""Autonomous Knowledge Maintenance — stale detection, auto-enrichment, decay scoring."""

from eoip.maintenance.autonomous import (
    DecayPolicy,
    EnrichmentAction,
    MaintenanceEngine,
    StalenessReport,
    get_maintenance_engine,
)

__all__ = [
    "DecayPolicy",
    "EnrichmentAction",
    "MaintenanceEngine",
    "StalenessReport",
    "get_maintenance_engine",
]
