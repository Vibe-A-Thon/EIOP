"""Graph event emitter: pub/sub for real-time graph change notifications."""

from __future__ import annotations

import asyncio
import threading
from collections import deque
from datetime import UTC, datetime
from enum import Enum
from typing import Any


import json
from pathlib import Path


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
    def __init__(self, buffer_size: int = 1000, *, journal_path: str | Path | None = None):
        self._subscribers: list[asyncio.Queue] = []
        self._loops: dict[asyncio.Queue, asyncio.AbstractEventLoop | None] = {}
        self._lock = threading.RLock()
        self._ring_buffer: deque[GraphEvent] = deque(maxlen=buffer_size)
        self._listeners: list[Any] = []  # synchronous fan-out (e.g. per-tenant event topics, SR-TEN-003)
        self._journal_path = Path(journal_path) if journal_path else None
        if self._journal_path is not None:
            self._journal_path.parent.mkdir(parents=True, exist_ok=True)
            self._recover_journal()

    def _recover_journal(self) -> None:
        if not self._journal_path or not self._journal_path.exists():
            return
        highest_id = GraphEvent._counter
        try:
            with open(self._journal_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                        ev_id = rec.get("event_id", 0)
                        if ev_id > highest_id:
                            highest_id = ev_id
                        ev = GraphEvent(rec["type"], rec["data"], timestamp=rec.get("timestamp"))
                        ev.event_id = ev_id
                        self._ring_buffer.append(ev)
                    except Exception:
                        continue
            GraphEvent._counter = highest_id
        except Exception:
            pass

    def add_listener(self, fn) -> None:
        self._listeners.append(fn)

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
            if self._journal_path is not None:
                try:
                    with open(self._journal_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps(event.to_dict()) + "\n")
                except Exception:
                    pass
            subscribers = list(self._loops.items())
            listeners = list(self._listeners)
        for fn in listeners:
            try:
                fn(event)
            except Exception:  # noqa: BLE001 - a listener failure never blocks the graph event stream
                pass
        with self._lock:
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
        with self._lock:
            buffer_events = list(self._ring_buffer)

        # If journal exists and since_id predates current ring buffer, replay from journal
        oldest_buffer_id = buffer_events[0].event_id if buffer_events else None
        if (
            self._journal_path is not None
            and self._journal_path.exists()
            and (oldest_buffer_id is None or since_id < oldest_buffer_id)
        ):
            results = []
            try:
                with open(self._journal_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            rec = json.loads(line)
                        except Exception:
                            continue
                        ev_id = rec.get("event_id", 0)
                        if ev_id > since_id:
                            ev = GraphEvent(rec["type"], rec["data"], timestamp=rec.get("timestamp"))
                            ev.event_id = ev_id
                            if ev.visible_to_tenant(tenant_id):
                                results.append(rec)
                                if len(results) >= limit:
                                    break
                return results
            except Exception:
                pass

        results = []
        for event in buffer_events:
            if event.event_id > since_id and event.visible_to_tenant(tenant_id):
                results.append(event.to_dict())
                if len(results) >= limit:
                    break
        return results

    def oldest_event_id(self) -> int | None:
        with self._lock:
            if self._journal_path is not None and self._journal_path.exists():
                try:
                    with open(self._journal_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                return json.loads(line).get("event_id")
                except Exception:
                    pass
            return self._ring_buffer[0].event_id if self._ring_buffer else None

    def has_gap(self, since_id: int) -> bool:
        oldest = self.oldest_event_id()
        if oldest is None:
            return False
        return since_id < (oldest - 1)

    def recent_events(self, limit: int = 50, *, tenant_id: str | None = None) -> list[dict]:
        events = [event for event in self._snapshot() if event.visible_to_tenant(tenant_id)][-limit:]
        return [e.to_dict() for e in events]
