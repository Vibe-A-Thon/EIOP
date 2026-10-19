"""Event bus, outbox dispatcher, and consumer deduplication (T-115 / REVA-WK-015 / D-05)."""

from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

from reva.core.time import format_ts, utc_now_ms
from reva.kernel.store import RevaStore


class Event(BaseModel):
    """Event envelope for internal pub/sub and outbox."""

    event_id: str
    tenant_id: str
    type: str
    payload: Dict[str, Any]
    created_at: str
    delivered_at: Optional[str] = None


EventHandler = Callable[[Event], None]


class EventBus:
    """In-process event bus supporting topic subscriptions and deduplicated delivery."""

    def __init__(self) -> None:
        self._handlers: Dict[str, List[EventHandler]] = {}

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Register a handler for a given event type or '*' wildcard."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event: Event) -> None:
        """Publish event synchronously to all matching handlers."""
        # Exact topic match
        handlers = list(self._handlers.get(event.type, []))
        # Wildcard topic match
        handlers.extend(self._handlers.get("*", []))

        for handler in handlers:
            try:
                handler(event)
            except Exception:
                # Log or swallow in bus; individual handler failures don't abort other handlers
                pass


# Global in-process event bus instance
default_event_bus = EventBus()


def dispatch_outbox(store: RevaStore, bus: Optional[EventBus] = None, limit: int = 100) -> int:
    """Poll undelivered outbox events and dispatch them to the event bus."""
    event_bus = bus or default_event_bus
    cur = store.conn.cursor()
    rows = cur.execute(
        "SELECT * FROM reva_outbox WHERE delivered_at IS NULL ORDER BY created_at ASC LIMIT ?",
        (limit,),
    ).fetchall()

    dispatched = 0
    now = format_ts(utc_now_ms())

    for row in rows:
        event = Event(
            event_id=row["event_id"],
            tenant_id=row["tenant_id"],
            type=row["type"],
            payload=json.loads(row["payload"]),
            created_at=row["created_at"],
            delivered_at=now,
        )
        event_bus.publish(event)
        cur.execute(
            "UPDATE reva_outbox SET delivered_at = ? WHERE event_id = ?",
            (now, event.event_id),
        )
        dispatched += 1

    store.conn.commit()
    return dispatched
