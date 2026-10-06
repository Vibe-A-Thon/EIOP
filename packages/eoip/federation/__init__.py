"""Federated query layer (GAP-FABRIC-001..008).

Splits a semantic query into per-source fragments, pushes filters and
projections where sources support it, merges results locally with per-row
provenance, routes cost-aware across materialized/local/live sources, and
degrades gracefully when sources are offline.
"""

from eoip.federation.planner import (
    DataSourceAdapter,
    FederatedQueryPlanner,
    FragmentResult,
    HugeGraphLocalAdapter,
    InMemoryDemoAdapter,
    LocalGraphStoreAdapter,
    RoutingPlan,
    SourceCapability,
    SourceMode,
)

__all__ = [
    "DataSourceAdapter",
    "FederatedQueryPlanner",
    "FragmentResult",
    "HugeGraphLocalAdapter",
    "InMemoryDemoAdapter",
    "LocalGraphStoreAdapter",
    "RoutingPlan",
    "SourceCapability",
    "SourceMode",
]
