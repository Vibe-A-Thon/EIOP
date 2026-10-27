"""Memory Engineering engine — unified memory lifecycle, consolidation,
decay, multi-tier memory management, and retrieval."""

from __future__ import annotations

import hashlib
import math
import threading
import time
import uuid
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any
from collections.abc import Callable


class MemoryTier(Enum):
    WORKING = "working"
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"


class DecayFunction(Enum):
    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    STEP = "step"
    NONE = "none"


@dataclass
class MemoryEntry:
    entry_id: str
    content: str
    tier: MemoryTier
    relevance: float = 1.0
    access_count: int = 0
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    ttl_seconds: float | None = None
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    source: str = ""

    @property
    def age_seconds(self) -> float:
        return time.time() - self.created_at

    @property
    def is_expired(self) -> bool:
        if self.ttl_seconds is None:
            return False
        return self.age_seconds > self.ttl_seconds

    def touch(self) -> None:
        self.last_accessed = time.time()
        self.access_count += 1


@dataclass
class MemoryQuery:
    text: str = ""
    tier: MemoryTier | None = None
    tags: list[str] = field(default_factory=list)
    min_relevance: float = 0.0
    limit: int = 10
    include_expired: bool = False


class MemoryStore:
    def __init__(self, decay: DecayFunction = DecayFunction.EXPONENTIAL,
                 decay_rate: float = 0.01) -> None:
        self._lock = threading.Lock()
        self._entries: dict[str, MemoryEntry] = {}
        self._by_tier: dict[MemoryTier, list[str]] = defaultdict(list)
        self._by_tag: dict[str, list[str]] = defaultdict(list)
        self._decay = decay
        self._decay_rate = decay_rate
        self._capacity: dict[MemoryTier, int] = {
            MemoryTier.WORKING: 50,
            MemoryTier.SHORT_TERM: 200,
            MemoryTier.LONG_TERM: 10000,
            MemoryTier.EPISODIC: 5000,
            MemoryTier.SEMANTIC: 10000,
            MemoryTier.PROCEDURAL: 2000,
        }

    def store(self, entry: MemoryEntry) -> None:
        with self._lock:
            self._entries[entry.entry_id] = entry
            self._by_tier[entry.tier].append(entry.entry_id)
            for tag in entry.tags:
                self._by_tag[tag].append(entry.entry_id)
            self._enforce_capacity(entry.tier)

    def get(self, entry_id: str) -> MemoryEntry | None:
        with self._lock:
            entry = self._entries.get(entry_id)
            if entry and not entry.is_expired:
                entry.touch()
                return entry
            return None

    def query(self, q: MemoryQuery) -> list[MemoryEntry]:
        with self._lock:
            candidates = list(self._entries.values())

        if q.tier:
            candidates = [e for e in candidates if e.tier == q.tier]
        if not q.include_expired:
            candidates = [e for e in candidates if not e.is_expired]
        if q.tags:
            tag_set = set(q.tags)
            candidates = [e for e in candidates if tag_set & set(e.tags)]
        if q.min_relevance > 0:
            candidates = [e for e in candidates
                          if self._effective_relevance(e) >= q.min_relevance]

        if q.text:
            query_tokens = set(q.text.lower().split())
            for entry in candidates:
                content_tokens = set(entry.content.lower().split())
                overlap = len(query_tokens & content_tokens) / max(len(query_tokens), 1)
                entry.relevance = max(entry.relevance, overlap)

        candidates.sort(key=lambda e: self._effective_relevance(e), reverse=True)
        return candidates[:q.limit]

    def _effective_relevance(self, entry: MemoryEntry) -> float:
        base = entry.relevance
        age = entry.age_seconds

        if self._decay == DecayFunction.EXPONENTIAL:
            factor = math.exp(-self._decay_rate * age / 3600)
        elif self._decay == DecayFunction.LINEAR:
            factor = max(0, 1.0 - self._decay_rate * age / 3600)
        elif self._decay == DecayFunction.STEP:
            if age < 3600:
                factor = 1.0
            elif age < 86400:
                factor = 0.5
            else:
                factor = 0.1
        else:
            factor = 1.0

        recency_boost = min(0.2, 1.0 / (1 + (time.time() - entry.last_accessed) / 60))
        frequency_boost = min(0.1, entry.access_count * 0.01)

        return base * factor + recency_boost + frequency_boost

    def _enforce_capacity(self, tier: MemoryTier) -> None:
        cap = self._capacity.get(tier, 10000)
        tier_ids = self._by_tier.get(tier, [])
        if len(tier_ids) <= cap:
            return
        tier_entries = [(eid, self._entries[eid])
                        for eid in tier_ids if eid in self._entries]
        tier_entries.sort(key=lambda x: self._effective_relevance(x[1]))
        to_remove = len(tier_entries) - cap
        for eid, _ in tier_entries[:to_remove]:
            del self._entries[eid]
            self._by_tier[tier] = [i for i in self._by_tier[tier] if i != eid]

    def evict_expired(self) -> int:
        with self._lock:
            expired = [eid for eid, e in self._entries.items() if e.is_expired]
            for eid in expired:
                entry = self._entries.pop(eid)
                self._by_tier[entry.tier] = [
                    i for i in self._by_tier[entry.tier] if i != eid]
            return len(expired)

    def promote(self, entry_id: str, to_tier: MemoryTier) -> bool:
        with self._lock:
            entry = self._entries.get(entry_id)
            if not entry:
                return False
            old_tier = entry.tier
            self._by_tier[old_tier] = [
                i for i in self._by_tier[old_tier] if i != entry_id]
            entry.tier = to_tier
            self._by_tier[to_tier].append(entry_id)
            return True

    def stats(self) -> dict[str, Any]:
        with self._lock:
            return {
                "total_entries": len(self._entries),
                "by_tier": {t.value: len(ids) for t, ids in self._by_tier.items()},
                "decay_function": self._decay.value,
            }


@dataclass
class ConsolidationPolicy:
    source_tier: MemoryTier
    target_tier: MemoryTier
    min_access_count: int = 3
    min_relevance: float = 0.5
    min_age_seconds: float = 3600.0

    def should_consolidate(self, entry: MemoryEntry) -> bool:
        return (entry.tier == self.source_tier
                and entry.access_count >= self.min_access_count
                and entry.relevance >= self.min_relevance
                and entry.age_seconds >= self.min_age_seconds)


class MemoryEngine:
    """Top-level Memory Engineering orchestrator."""

    def __init__(self, decay: DecayFunction = DecayFunction.EXPONENTIAL) -> None:
        self._store = MemoryStore(decay)
        self._policies: list[ConsolidationPolicy] = [
            ConsolidationPolicy(MemoryTier.WORKING, MemoryTier.SHORT_TERM, 2, 0.3, 60),
            ConsolidationPolicy(MemoryTier.SHORT_TERM, MemoryTier.LONG_TERM, 5, 0.5, 3600),
        ]
        self._lock = threading.Lock()
        self._counter = 0

    @property
    def store(self) -> MemoryStore:
        return self._store

    def remember(self, content: str, tier: MemoryTier = MemoryTier.WORKING,
                 tags: list[str] | None = None, ttl: float | None = None,
                 source: str = "", **metadata: Any) -> MemoryEntry:
        with self._lock:
            self._counter += 1
            entry_id = hashlib.sha256(
                f"{content}:{self._counter}:{time.time()}".encode()
            ).hexdigest()[:16]

        entry = MemoryEntry(
            entry_id=entry_id, content=content, tier=tier,
            tags=tags or [], ttl_seconds=ttl, source=source,
            metadata=metadata,
        )
        self._store.store(entry)
        return entry

    def recall(self, query: str, tier: MemoryTier | None = None,
               limit: int = 10) -> list[MemoryEntry]:
        q = MemoryQuery(text=query, tier=tier, limit=limit)
        return self._store.query(q)

    def forget(self, entry_id: str) -> bool:
        with self._lock:
            entry = self._store._entries.get(entry_id)
            if entry:
                del self._store._entries[entry_id]
                return True
            return False

    def consolidate(self) -> int:
        promoted = 0
        for policy in self._policies:
            entries = self._store.query(MemoryQuery(
                tier=policy.source_tier, limit=1000, include_expired=False,
            ))
            for entry in entries:
                if policy.should_consolidate(entry):
                    if self._store.promote(entry.entry_id, policy.target_tier):
                        promoted += 1
        return promoted

    def add_consolidation_policy(self, policy: ConsolidationPolicy) -> None:
        self._policies.append(policy)

    def cleanup(self) -> int:
        return self._store.evict_expired()

    def stats(self) -> dict[str, Any]:
        return {
            "engine": "memory_engineering",
            "store": self._store.stats(),
            "consolidation_policies": len(self._policies),
        }


_instance: MemoryEngine | None = None
_lock = threading.Lock()


def get_memory_engine() -> MemoryEngine:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = MemoryEngine()
    return _instance


# ============================================================================
# Knowledge & Memory Graph Engineering (MULTI-002)
# ============================================================================

@dataclass
class MemoryNode:
    node_id: str
    content: str
    memory_type: str  # EPISODIC, SEMANTIC, PROCEDURAL
    importance: float = 1.0
    access_count: int = 1
    timestamp: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)


class MemoryGraph:
    """Graph-native memory representation with temporal and causal links."""

    def __init__(self) -> None:
        self.nodes: dict[str, MemoryNode] = {}
        self.edges: list[dict[str, Any]] = []  # source, target, relation, weight
        self._lock = threading.Lock()

    def add_node(
        self,
        node_id: str,
        content: str,
        memory_type: str = "EPISODIC",
        importance: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ) -> MemoryNode:
        with self._lock:
            node = MemoryNode(
                node_id=node_id,
                content=content,
                memory_type=memory_type,
                importance=importance,
                metadata=metadata or {},
            )
            self.nodes[node_id] = node
            return node

    def link_nodes(self, source_id: str, target_id: str, relation: str = "TEMPORAL", weight: float = 1.0) -> None:
        with self._lock:
            self.edges.append({
                "source": source_id,
                "target": target_id,
                "relation": relation,
                "weight": weight,
            })

    def query_subgraph(self, memory_type: str | None = None, min_importance: float = 0.0) -> dict[str, Any]:
        with self._lock:
            matched_nodes = [
                n for n in self.nodes.values()
                if (memory_type is None or n.memory_type == memory_type) and n.importance >= min_importance
            ]
            matched_ids = {n.node_id for n in matched_nodes}
            matched_edges = [
                e for e in self.edges
                if e["source"] in matched_ids and e["target"] in matched_ids
            ]
            return {
                "nodes": [asdict(n) for n in matched_nodes],
                "edges": matched_edges,
            }


class EpisodicMemoryGraph(MemoryGraph):
    """Session-based chronological event graph linked with FOLLOWED_BY edges."""

    def __init__(self) -> None:
        super().__init__()
        self._last_event_id: str | None = None

    def record_episode_step(self, step_name: str, payload: dict[str, Any], importance: float = 1.0) -> str:
        step_id = f"ep_{uuid.uuid4().hex[:8]}" if 'uuid' in globals() else f"ep_{time.time()}"
        self.add_node(
            node_id=step_id,
            content=step_name,
            memory_type="EPISODIC",
            importance=importance,
            metadata=payload,
        )
        if self._last_event_id:
            self.link_nodes(self._last_event_id, step_id, relation="FOLLOWED_BY")
        self._last_event_id = step_id
        return step_id


class MemoryConsolidationGraph:
    """Consolidates episodic experience traces into distilled semantic knowledge."""

    def __init__(self, episodic_graph: MemoryGraph, long_term_graph: MemoryGraph | None = None) -> None:
        self.episodic_graph = episodic_graph
        self.long_term_graph = long_term_graph or MemoryGraph()

    def consolidate(self, frequency_threshold: int = 2) -> int:
        """Promote recurring episodic patterns to semantic memory nodes."""
        content_counts: dict[str, int] = defaultdict(int)
        for n in self.episodic_graph.nodes.values():
            content_counts[n.content] += 1

        consolidated_count = 0
        for content, count in content_counts.items():
            if count >= frequency_threshold:
                sem_id = f"sem_{hashlib.sha256(content.encode()).hexdigest()[:8]}"
                if sem_id not in self.long_term_graph.nodes:
                    self.long_term_graph.add_node(
                        node_id=sem_id,
                        content=f"Consolidated Rule: {content}",
                        memory_type="SEMANTIC",
                        importance=min(2.0, 1.0 + (count * 0.2)),
                        metadata={"origin_count": count},
                    )
                    consolidated_count += 1
        return consolidated_count

