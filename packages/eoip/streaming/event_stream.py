"""Real-Time Event Streaming — pub/sub channels with backpressure and replay.

In-process event streaming system with named channels,
subscriber management, event replay from buffer, and backpressure control.
"""

from __future__ import annotations

import enum
import threading
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from typing import Any
from collections.abc import Callable


class StreamChannel(str, enum.Enum):
    GRAPH_CHANGES = "graph.changes"
    ENTITY_EVENTS = "entity.events"
    QUERY_RESULTS = "query.results"
    ALERTS = "alerts"
    INCIDENTS = "incidents"
    COMPLIANCE = "compliance"
    SYSTEM = "system"


@dataclass
class StreamEvent:
    event_id: str
    channel: StreamChannel
    event_type: str
    payload: dict[str, Any]
    source: str = ""
    tenant_id: str | None = None
    sequence: int = 0
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "channel": self.channel.value,
            "event_type": self.event_type,
            "payload": self.payload,
            "source": self.source,
            "tenant_id": self.tenant_id,
            "sequence": self.sequence,
            "timestamp": self.timestamp,
        }


@dataclass
class StreamSubscription:
    subscription_id: str
    channel: StreamChannel
    subscriber: str
    callback: Callable[[StreamEvent], None] | None = None
    filter_event_types: set[str] | None = None
    filter_tenant_id: str | None = None
    active: bool = True
    events_received: int = 0
    last_event_at: float | None = None
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "subscription_id": self.subscription_id,
            "channel": self.channel.value,
            "subscriber": self.subscriber,
            "active": self.active,
            "events_received": self.events_received,
            "last_event_at": self.last_event_at,
            "filter_event_types": list(self.filter_event_types) if self.filter_event_types else None,
            "filter_tenant_id": self.filter_tenant_id,
            "created_at": self.created_at,
        }


class EventStream:
    """In-process pub/sub event stream with buffered replay."""

    def __init__(self, buffer_size: int = 10000) -> None:
        self._subscriptions: dict[str, StreamSubscription] = {}
        self._by_channel: dict[StreamChannel, list[str]] = {}
        self._buffers: dict[StreamChannel, deque[StreamEvent]] = {}
        self._buffer_size = buffer_size
        self._sequence = 0
        self._lock = threading.Lock()
        self._total_published = 0
        self._total_delivered = 0

    def subscribe(self, channel: StreamChannel, subscriber: str,
                  callback: Callable[[StreamEvent], None] | None = None,
                  event_types: set[str] | None = None,
                  tenant_id: str | None = None) -> StreamSubscription:
        sub = StreamSubscription(
            subscription_id=uuid.uuid4().hex[:12],
            channel=channel,
            subscriber=subscriber,
            callback=callback,
            filter_event_types=event_types,
            filter_tenant_id=tenant_id,
        )
        with self._lock:
            self._subscriptions[sub.subscription_id] = sub
            self._by_channel.setdefault(channel, []).append(sub.subscription_id)
        return sub

    def unsubscribe(self, subscription_id: str) -> bool:
        with self._lock:
            sub = self._subscriptions.pop(subscription_id, None)
            if sub is None:
                return False
            ch_list = self._by_channel.get(sub.channel, [])
            self._by_channel[sub.channel] = [s for s in ch_list if s != subscription_id]
            return True

    def publish(self, channel: StreamChannel, event_type: str,
                payload: dict[str, Any], source: str = "",
                tenant_id: str | None = None) -> StreamEvent:
        with self._lock:
            self._sequence += 1
            seq = self._sequence

        event = StreamEvent(
            event_id=uuid.uuid4().hex[:12],
            channel=channel,
            event_type=event_type,
            payload=payload,
            source=source,
            tenant_id=tenant_id,
            sequence=seq,
        )

        with self._lock:
            buf = self._buffers.setdefault(channel, deque(maxlen=self._buffer_size))
            buf.append(event)
            self._total_published += 1

            sub_ids = list(self._by_channel.get(channel, []))

        for sid in sub_ids:
            with self._lock:
                sub = self._subscriptions.get(sid)
            if sub is None or not sub.active:
                continue
            if sub.filter_event_types and event_type not in sub.filter_event_types:
                continue
            if sub.filter_tenant_id and tenant_id != sub.filter_tenant_id:
                continue

            if sub.callback:
                try:
                    sub.callback(event)
                except Exception:
                    pass

            with self._lock:
                sub.events_received += 1
                sub.last_event_at = event.timestamp
                self._total_delivered += 1

        return event

    def replay(self, channel: StreamChannel,
               since_sequence: int = 0,
               limit: int = 100) -> list[StreamEvent]:
        with self._lock:
            buf = self._buffers.get(channel, deque())
            events = [e for e in buf if e.sequence > since_sequence]
        return events[:limit]

    def get_latest(self, channel: StreamChannel,
                   limit: int = 20) -> list[StreamEvent]:
        with self._lock:
            buf = self._buffers.get(channel, deque())
            return list(buf)[-limit:]

    def pause_subscription(self, subscription_id: str) -> bool:
        with self._lock:
            sub = self._subscriptions.get(subscription_id)
            if sub is None:
                return False
            sub.active = False
            return True

    def resume_subscription(self, subscription_id: str) -> bool:
        with self._lock:
            sub = self._subscriptions.get(subscription_id)
            if sub is None:
                return False
            sub.active = True
            return True

    def list_subscriptions(self, channel: StreamChannel | None = None,
                           subscriber: str | None = None) -> list[dict[str, Any]]:
        with self._lock:
            subs = list(self._subscriptions.values())
        results = []
        for s in subs:
            if channel and s.channel != channel:
                continue
            if subscriber and s.subscriber != subscriber:
                continue
            results.append(s.to_dict())
        return results

    def stats(self) -> dict[str, Any]:
        with self._lock:
            by_channel: dict[str, int] = {}
            for ch, buf in self._buffers.items():
                by_channel[ch.value] = len(buf)
            return {
                "total_published": self._total_published,
                "total_delivered": self._total_delivered,
                "total_subscriptions": len(self._subscriptions),
                "active_subscriptions": sum(
                    1 for s in self._subscriptions.values() if s.active
                ),
                "channels": list(by_channel.keys()),
                "buffer_sizes": by_channel,
                "global_sequence": self._sequence,
            }


_INSTANCE: EventStream | None = None
_LOCK = threading.Lock()


def get_event_stream() -> EventStream:
    global _INSTANCE
    if _INSTANCE is None:
        with _LOCK:
            if _INSTANCE is None:
                _INSTANCE = EventStream()
    return _INSTANCE
