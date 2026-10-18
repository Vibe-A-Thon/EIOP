"""EOIP Catalog — Enterprise Context Layer & Data Catalog Projections (CRA-029.1-029.8, CRA-029.A)."""

from __future__ import annotations

from eoip.catalog.classification_propagation import (
    ClassificationPropagationEngine,
    PropagatedTag,
)
from eoip.catalog.layered_metadata import (
    BaseMetadataEntry,
    FieldConflict,
    HumanEditEntry,
    LayeredAssetMetadata,
)
from eoip.catalog.lineage_parser import (
    LineageEdge,
    LineageParseResult,
    LineageParser,
)
from eoip.catalog.multi_graph_views import (
    GraphViewProjection,
    MultiGraphViewEngine,
)
from eoip.catalog.projections import (
    CatalogProjectionEngine,
    FederatedCatalogSource,
)

__all__ = [
    "BaseMetadataEntry",
    "CatalogProjectionEngine",
    "ClassificationPropagationEngine",
    "FederatedCatalogSource",
    "FieldConflict",
    "GraphViewProjection",
    "HumanEditEntry",
    "LayeredAssetMetadata",
    "LineageEdge",
    "LineageParseResult",
    "LineageParser",
    "MultiGraphViewEngine",
    "PropagatedTag",
]
