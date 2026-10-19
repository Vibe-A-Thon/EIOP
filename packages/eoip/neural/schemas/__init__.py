"""
Neural Schema Package (NS-REQ-*, NS-PLAN-v1).
Provides cognitive neural schemas, dual-pathway brain assimilation,
Clone-Structured Cognitive Graphs (CSCG), Attention Schema Theory (AST),
schema induction, SHACL synthesis, and multi-plane graph projection.
"""

from packages.eoip.neural.schemas.models import (
    SlotConstraint,
    NeuralSchema,
    AssimilationResult,
    EvaluationReport,
)
from packages.eoip.neural.schemas.assimilation import DualPathwayAssimilator
from packages.eoip.neural.schemas.cscg import CSCGNode, CSCGGraph
from packages.eoip.neural.schemas.ast_metacognitive import AttentionSchemaEngine
from packages.eoip.neural.schemas.consolidation import SchemaInductionEngine, SHACLShape
from packages.eoip.neural.schemas.planes_integration import GraphPlanesProjector

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
