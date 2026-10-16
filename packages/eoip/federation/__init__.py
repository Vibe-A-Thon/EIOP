"""Federated query layer (GAP-FABRIC-001..008, GRAPH-001).

Splits a semantic query into per-source fragments, pushes filters and
projections where sources support it, merges results locally with per-row
provenance, routes cost-aware across materialized/local/live sources, and
degrades gracefully when sources are offline.
"""

from eoip.federation.engine import (
    BackendMapping,
    CatalogService,
    FederatedGraph,
    FederationEngine,
    FederationPlanner,
    ResultMerger,
    get_federation_engine,
)
from eoip.federation.planner import (
    DataSourceAdapter,
    FederatedQueryPlanner,
    FileSourceAdapter,
    FragmentResult,
    HugeGraphLocalAdapter,
    InMemoryDemoAdapter,
    InMemoryRowAdapter,
    JdbcSourceAdapter,
    LocalGraphStoreAdapter,
    RestSourceAdapter,
    RoutingPlan,
    SourceCapability,
    SourceMode,
    SourcePolicy,
)

__all__ = [
    "BackendMapping",
    "CatalogService",
    "DataSourceAdapter",
    "FederatedGraph",
    "FederatedQueryPlanner",
    "FederationEngine",
    "FederationPlanner",
    "FileSourceAdapter",
    "FragmentResult",
    "HugeGraphLocalAdapter",
    "InMemoryDemoAdapter",
    "InMemoryRowAdapter",
    "JdbcSourceAdapter",
    "LocalGraphStoreAdapter",
    "RestSourceAdapter",
    "ResultMerger",
    "RoutingPlan",
    "SourceCapability",
    "SourceMode",
    "SourcePolicy",
    "get_federation_engine",
]
