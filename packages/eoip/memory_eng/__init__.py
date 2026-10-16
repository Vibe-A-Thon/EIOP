"""Memory Engineering engine — unified memory lifecycle, consolidation,
decay, and multi-tier memory management."""

from eoip.memory_eng.engine import (
    ConsolidationPolicy,
    DecayFunction,
    MemoryEngine,
    MemoryEntry,
    MemoryQuery,
    MemoryTier,
    MemoryStore,
    get_memory_engine,
)

__all__ = [
    "ConsolidationPolicy",
    "DecayFunction",
    "MemoryEngine",
    "MemoryEntry",
    "MemoryQuery",
    "MemoryStore",
    "MemoryTier",
    "get_memory_engine",
]
