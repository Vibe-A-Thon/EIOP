"""Retrieval: graph-first RAG router, vector similarity, and hybrid search."""

from eoip.retrieval.hybrid_vector_service import (
    DimensionMismatchError,
    EmbeddingProviderUnavailableError,
    HybridVectorIndexManager,
    IncompatibleEmbeddingFamilyError,
    IndexFamily,
    IndexMetadata,
    IndexState,
    ProductionConfigurationError,
    RealSemanticProvider,
    SearchEvaluationHarness,
    TenantVectorIndex,
    TestHashingEmbedder,
    VectorDocument,
)

__all__ = [
    "DimensionMismatchError",
    "EmbeddingProviderUnavailableError",
    "HybridVectorIndexManager",
    "IncompatibleEmbeddingFamilyError",
    "IndexFamily",
    "IndexMetadata",
    "IndexState",
    "ProductionConfigurationError",
    "RealSemanticProvider",
    "SearchEvaluationHarness",
    "TenantVectorIndex",
    "TestHashingEmbedder",
    "VectorDocument",
]
