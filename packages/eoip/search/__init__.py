"""Enterprise search: keyword search with semantic facet aggregation.

GAP-SEARCH-001 (faceted hybrid search) and GAP-SEARCH-002 (results preserve
graph identity and provenance). Tier 8: semantic vector search integration.
"""

from eoip.search.facets import (
    FacetBucket,
    FacetedSearch,
    SearchFacets,
    SearchHit,
    SearchRequest,
    SearchResponse,
    search,
)
from eoip.search.semantic import (
    DriftReport,
    DriftSeverity,
    EmbeddedEntity,
    HybridSearchResult,
    SemanticVectorIndex,
    SimilarityResult,
    get_semantic_index,
)
from eoip.search.hybrid_engine import (
    HybridSearchEngine,
    SearchModality,
    UnifiedSearchResult,
    UserContext,
    get_hybrid_search_engine,
)

__all__ = [
    "DriftReport",
    "DriftSeverity",
    "EmbeddedEntity",
    "FacetBucket",
    "FacetedSearch",
    "HybridSearchEngine",
    "HybridSearchResult",
    "SearchFacets",
    "SearchHit",
    "SearchModality",
    "SearchRequest",
    "SearchResponse",
    "SemanticVectorIndex",
    "SimilarityResult",
    "UnifiedSearchResult",
    "UserContext",
    "get_hybrid_search_engine",
    "get_semantic_index",
    "search",
]
