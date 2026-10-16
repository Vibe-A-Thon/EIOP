"""Graph event emitter: pub/sub for real-time graph change notifications."""

from __future__ import annotations

import asyncio
import threading
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

    def visible_to_tenant(self, tenant_id: str | None) -> bool:
        if tenant_id is None:
            return True
        data = self.data
        declared = data.get("tenant_id")
        ids = [data.get(key) for key in ("canonical_id", "vid") if data.get(key)]
        scoped_ids = [value for value in ids if isinstance(value, str) and value.startswith("g:")]
        if declared is not None and declared != tenant_id:
            return False
        if any(not value.startswith(f"g:{tenant_id}:") for value in scoped_ids):
            return False
        return declared == tenant_id or bool(scoped_ids)


class GraphEventEmitter:
    def __init__(self, buffer_size: int = 1000):
        self._subscribers: list[asyncio.Queue] = []
        self._loops: dict[asyncio.Queue, asyncio.AbstractEventLoop | None] = {}
        self._lock = threading.RLock()
        self._ring_buffer: deque[GraphEvent] = deque(maxlen=buffer_size)

    def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue(maxsize=1000)
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        with self._lock:
            self._subscribers.append(q)
            self._loops[q] = loop
        return q

    def unsubscribe(self, q: asyncio.Queue) -> None:
        with self._lock:
            if q in self._subscribers:
                self._subscribers.remove(q)
            self._loops.pop(q, None)

    @property
    def subscriber_count(self) -> int:
        return len(self._subscribers)

    async def emit(self, event: GraphEvent) -> None:
        self.emit_sync(event)

    @staticmethod
    def _offer(q: asyncio.Queue, event: GraphEvent) -> None:
        try:
            q.put_nowait(event)
        except asyncio.QueueFull:
            pass

    def emit_sync(self, event: GraphEvent) -> None:
        with self._lock:
            self._ring_buffer.append(event)
            subscribers = list(self._loops.items())
        try:
            current_loop = asyncio.get_running_loop()
        except RuntimeError:
            current_loop = None
        for q, loop in subscribers:
            try:
                if loop is not None and loop is not current_loop:
                    loop.call_soon_threadsafe(self._offer, q, event)
                else:
                    self._offer(q, event)
            except RuntimeError:  # Subscriber's event loop closed after the snapshot.
                pass

    def _snapshot(self) -> list[GraphEvent]:
        with self._lock:
            return list(self._ring_buffer)

    def events_since(self, since_timestamp: str, limit: int = 100, *, tenant_id: str | None = None) -> list[dict]:
        results = []
        for event in self._snapshot():
            if event.timestamp > since_timestamp and event.visible_to_tenant(tenant_id):
                results.append(event.to_dict())
                if len(results) >= limit:
                    break
        return results

    def events_since_id(self, since_id: int, limit: int = 100, *, tenant_id: str | None = None) -> list[dict]:
        results = []
        for event in self._snapshot():
            if event.event_id > since_id and event.visible_to_tenant(tenant_id):
                results.append(event.to_dict())
                if len(results) >= limit:
                    break
        return results

    def recent_events(self, limit: int = 50, *, tenant_id: str | None = None) -> list[dict]:
        events = [event for event in self._snapshot() if event.visible_to_tenant(tenant_id)][-limit:]
        return [e.to_dict() for e in events]
