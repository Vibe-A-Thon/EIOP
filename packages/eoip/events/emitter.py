"""Graph event emitter: pub/sub for real-time graph change notifications."""

from __future__ import annotations

import asyncio
from collections import deque
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class EventType(str, Enum):
    VERTEX_UPSERTED = "vertex_upserted"
    EDGE_UPSERTED = "edge_upserted"
    VERTEX_DELETED = "vertex_deleted"
    EDGE_DELETED = "edge_deleted"
    INGESTION_COMPLETED = "ingestion_completed"
    VALIDATION_COMPLETED = "validation_completed"


class GraphEvent:
    __slots__ = ("data", "event_id", "timestamp", "type")

    _counter = 0

    def __init__(self, type: str, data: dict[str, Any], timestamp: str | None = None):
        GraphEvent._counter += 1
        self.event_id = GraphEvent._counter
        self.type = type
        self.data = data
        self.timestamp = timestamp or datetime.now(UTC).isoformat()

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "type": self.type,
            "data": self.data,
            "timestamp": self.timestamp,
        }


class GraphEventEmitter:
    def __init__(self, buffer_size: int = 1000):
        self._subscribers: list[asyncio.Queue] = []
        self._ring_buffer: deque[GraphEvent] = deque(maxlen=buffer_size)

    def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue(maxsize=1000)
        self._subscribers.append(q)
        return q

    def unsubscribe(self, q: asyncio.Queue) -> None:
        try:
            self._subscribers.remove(q)
        except ValueError:
            pass

    @property
    def subscriber_count(self) -> int:
        return len(self._subscribers)

    async def emit(self, event: GraphEvent) -> None:
        self._ring_buffer.append(event)
        for q in self._subscribers:
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                pass

    def emit_sync(self, event: GraphEvent) -> None:
        self._ring_buffer.append(event)

    def events_since(self, since_timestamp: str, limit: int = 100) -> list[dict]:
        results = []
        for event in self._ring_buffer:
            if event.timestamp > since_timestamp:
                results.append(event.to_dict())
                if len(results) >= limit:
                    break
        return results

    def events_since_id(self, since_id: int, limit: int = 100) -> list[dict]:
        results = []
        for event in self._ring_buffer:
            if event.event_id > since_id:
                results.append(event.to_dict())
                if len(results) >= limit:
                    break
        return results

    def recent_events(self, limit: int = 50) -> list[dict]:
        events = list(self._ring_buffer)[-limit:]
        return [e.to_dict() for e in events]
