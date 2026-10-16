"""Dynamic Entity & Community Extraction Pipeline package (AGENT-002, AI-003)."""

from eoip.extraction.engine import (
    ChunkStrategy,
    CommunityDetector,
    DocumentChunk,
    DocumentChunker,
    EntityExtractor,
    ExtractionPipeline,
    ExtractionResult,
    ExtractedEntity,
    get_extraction_engine,
)
from eoip.extraction.relation_extractor import (
    ExtractedTriple,
    RelationExtractor,
    RelationPattern,
    TripleDeduplicator,
    TripleValidator,
)

__all__ = [
    "ChunkStrategy",
    "CommunityDetector",
    "DocumentChunk",
    "DocumentChunker",
    "EntityExtractor",
    "ExtractionPipeline",
    "ExtractionResult",
    "ExtractedEntity",
    "ExtractedTriple",
    "RelationExtractor",
    "RelationPattern",
    "TripleDeduplicator",
    "TripleValidator",
    "get_extraction_engine",
]
