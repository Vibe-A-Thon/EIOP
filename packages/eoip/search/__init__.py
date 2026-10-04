"""Enterprise search: keyword search with semantic facet aggregation.

GAP-SEARCH-001 (faceted hybrid search) and GAP-SEARCH-002 (results preserve
graph identity and provenance).
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

__all__ = [
    "FacetBucket",
    "FacetedSearch",
    "SearchFacets",
    "SearchHit",
    "SearchRequest",
    "SearchResponse",
    "search",
]
