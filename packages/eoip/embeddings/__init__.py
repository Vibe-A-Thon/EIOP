"""Embedding management package (AI-006)."""

from eoip.embeddings.engine import (
    DimensionReducer,
    DriftReport,
    EmbeddingDriftDetector,
    EmbeddingEngine,
    EmbeddingFusionStrategy,
    EmbeddingRegistry,
    EmbeddingVersion,
    FusionMethod,
    get_embedding_engine,
)

__all__ = [
    "DimensionReducer",
    "DriftReport",
    "EmbeddingDriftDetector",
    "EmbeddingEngine",
    "EmbeddingFusionStrategy",
    "EmbeddingRegistry",
    "EmbeddingVersion",
    "FusionMethod",
    "get_embedding_engine",
]
