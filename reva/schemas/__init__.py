"""
Proxy package mapping reva.schemas to packages.eoip.neural.schemas.
"""

from packages.eoip.neural.schemas import (
    SlotConstraint,
    NeuralSchema,
    AssimilationResult,
    EvaluationReport,
    DualPathwayAssimilator,
    CSCGNode,
    CSCGGraph,
    AttentionSchemaEngine,
    SchemaInductionEngine,
    SHACLShape,
    GraphPlanesProjector,
)

__all__ = [
    "SlotConstraint",
    "NeuralSchema",
    "AssimilationResult",
    "EvaluationReport",
    "DualPathwayAssimilator",
    "CSCGNode",
    "CSCGGraph",
    "AttentionSchemaEngine",
    "SchemaInductionEngine",
    "SHACLShape",
    "GraphPlanesProjector",
]
