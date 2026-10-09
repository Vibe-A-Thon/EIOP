"""KGR-G-014: Streaming Temporal Agent Memory (Dual-Timeline).

Dual-timeline (event_time × ingestion_time) streaming updates to the
Adaptive Graph Attention Memory (AGAM).  Supports continuous ingestion
of memory events with automatic salience decay and conflict resolution.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

log = logging.getLogger("eoip.moonshot.streaming_agent_memory")


class MemoryEventType(str, Enum):
    OBSERVATION = "OBSERVATION"
    INFERENCE = "INFERENCE"
    ACTION = "ACTION"
    FEEDBACK = "FEEDBACK"
    CORRECTION = "CORRECTION"
    RETRACTION = "RETRACTION"


@dataclass
class TemporalMemoryEvent:
    event_id: str
    agent_id: str
    event_type: MemoryEventType
    content: dict[str, Any]
    event_time: float
    ingestion_time: float = 0.0
    salience: float = 1.0
    source_id: str = ""
    correlation_id: str = ""
    ttl_seconds: int = 86400 * 30

    def __post_init__(self) -> None:
        if self.ingestion_time == 0.0:
            self.ingestion_time = time.time()

    @property
    def age_seconds(self) -> float:
        return time.time() - self.event_time

    @property
    def is_expired(self) -> bool:
        return self.age_seconds > self.ttl_seconds


@dataclass
class DualTimelineIndex:
    """Indexes memory events on both event_time and ingestion_time axes."""
    _by_event_time: list[TemporalMemoryEvent] = field(default_factory=list)
    _by_ingestion_time: list[TemporalMemoryEvent] = field(default_factory=list)
    _by_id: dict[str, TemporalMemoryEvent] = field(default_factory=dict)
    _by_agent: dict[str, list[TemporalMemoryEvent]] = field(default_factory=dict)

    def insert(self, event: TemporalMemoryEvent) -> None:
        self._by_id[event.event_id] = event
        self._by_event_time.append(event)
        self._by_ingestion_time.append(event)
        self._by_agent.setdefault(event.agent_id, []).append(event)

    def query_event_time_range(self, start: float, end: float) -> list[TemporalMemoryEvent]:
        return [e for e in self._by_event_time if start <= e.event_time <= end]

    def query_ingestion_time_range(self, start: float, end: float) -> list[TemporalMemoryEvent]:
        return [e for e in self._by_ingestion_time if start <= e.ingestion_time <= end]

    def query_agent(self, agent_id: str, *, limit: int = 100) -> list[TemporalMemoryEvent]:
        events = self._by_agent.get(agent_id, [])
        return sorted(events, key=lambda e: e.event_time, reverse=True)[:limit]

    def get(self, event_id: str) -> TemporalMemoryEvent | None:
        return self._by_id.get(event_id)

    def remove(self, event_id: str) -> bool:
        event = self._by_id.pop(event_id, None)
        if event is None:
            return False
        self._by_event_time = [e for e in self._by_event_time if e.event_id != event_id]
        self._by_ingestion_time = [e for e in self._by_ingestion_time if e.event_id != event_id]
        if event.agent_id in self._by_agent:
            self._by_agent[event.agent_id] = [
                e for e in self._by_agent[event.agent_id] if e.event_id != event_id
            ]
        return True

    @property
    def size(self) -> int:
        return len(self._by_id)

    def prune_expired(self) -> int:
        expired = [eid for eid, e in self._by_id.items() if e.is_expired]
        for eid in expired:
            self.remove(eid)
        return len(expired)


class SalienceDecayFunction:
    """Exponential salience decay with configurable half-life."""

    def __init__(self, half_life_seconds: float = 86400.0, min_salience: float = 0.01) -> None:
        self.half_life = half_life_seconds
        self.min_salience = min_salience
        self._decay_rate = math.log(2) / half_life_seconds

    def compute(self, initial_salience: float, age_seconds: float) -> float:
        decayed = initial_salience * math.exp(-self._decay_rate * age_seconds)
        return max(decayed, self.min_salience)

    def should_evict(self, salience: float) -> bool:
        return salience <= self.min_salience


class ConflictResolver:
    """Resolves conflicts between memory events that contradict each other."""

    def resolve(self, existing: TemporalMemoryEvent, incoming: TemporalMemoryEvent) -> TemporalMemoryEvent:
        if incoming.event_type == MemoryEventType.CORRECTION:
            return incoming
        if incoming.event_type == MemoryEventType.RETRACTION:
            return incoming
        if incoming.event_time > existing.event_time:
            return incoming
        if incoming.salience > existing.salience:
            return incoming
        return existing


class StreamingMemoryIngester:
    """Continuously ingests memory events into the dual-timeline index."""

    def __init__(
        self,
        *,
        max_buffer_size: int = 10000,
        decay_function: SalienceDecayFunction | None = None,
        conflict_resolver: ConflictResolver | None = None,
        on_event: Callable[[TemporalMemoryEvent], None] | None = None,
    ) -> None:
        self._index = DualTimelineIndex()
        self._buffer: deque[TemporalMemoryEvent] = deque(maxlen=max_buffer_size)
        self._decay = decay_function or SalienceDecayFunction()
        self._resolver = conflict_resolver or ConflictResolver()
        self._on_event = on_event
        self._lock = threading.Lock()
        self._running = False
        self._ingested_count = 0
        self._conflict_count = 0

    @property
    def index(self) -> DualTimelineIndex:
        return self._index

    @property
    def stats(self) -> dict[str, Any]:
        return {
            "index_size": self._index.size,
            "buffer_size": len(self._buffer),
            "ingested_total": self._ingested_count,
            "conflicts_resolved": self._conflict_count,
        }

    def ingest(self, event: TemporalMemoryEvent) -> TemporalMemoryEvent:
        event.ingestion_time = time.time()
        event.salience = self._decay.compute(event.salience, event.age_seconds)

        with self._lock:
            existing = self._index.get(event.event_id)
            if existing:
                winner = self._resolver.resolve(existing, event)
                if winner is event:
                    self._index.remove(existing.event_id)
                    self._index.insert(event)
                    self._conflict_count += 1
                event = winner
            else:
                self._index.insert(event)

            self._buffer.append(event)
            self._ingested_count += 1

        if self._on_event:
            self._on_event(event)

        return event

    def ingest_batch(self, events: list[TemporalMemoryEvent]) -> list[TemporalMemoryEvent]:
        return [self.ingest(e) for e in events]

    def query_context(
        self,
        agent_id: str,
        *,
        max_events: int = 50,
        min_salience: float = 0.1,
        event_types: set[MemoryEventType] | None = None,
    ) -> list[TemporalMemoryEvent]:
        """Retrieve the most salient recent context for an agent."""
        raw = self._index.query_agent(agent_id, limit=max_events * 3)
        now = time.time()
        scored: list[tuple[float, TemporalMemoryEvent]] = []
        for e in raw:
            current_salience = self._decay.compute(e.salience, now - e.event_time)
            if current_salience < min_salience:
                continue
            if event_types and e.event_type not in event_types:
                continue
            scored.append((current_salience, e))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [e for _, e in scored[:max_events]]

    def decay_pass(self) -> int:
        """Run a decay pass, evicting events below minimum salience."""
        now = time.time()
        to_evict: list[str] = []
        with self._lock:
            for eid, event in list(self._index._by_id.items()):
                current = self._decay.compute(event.salience, now - event.event_time)
                if self._decay.should_evict(current):
                    to_evict.append(eid)
            for eid in to_evict:
                self._index.remove(eid)
        return len(to_evict)

    def prune(self) -> int:
        with self._lock:
            return self._index.prune_expired()
