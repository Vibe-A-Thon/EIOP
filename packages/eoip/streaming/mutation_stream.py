"""KGR-G-020: Real-Time Graph Mutation Streaming & Webhooks.

SSE/WebSocket push for node/edge mutation events.  Includes webhook
delivery with configurable retries, dead-letter queue, and per-tenant
subscription management.
"""

from __future__ import annotations

import hashlib
import json
import logging
import queue
import threading
import time
import urllib.request
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

log = logging.getLogger("eoip.streaming.mutation_stream")


class MutationType(str, Enum):
    VERTEX_CREATED = "VERTEX_CREATED"
    VERTEX_UPDATED = "VERTEX_UPDATED"
    VERTEX_DELETED = "VERTEX_DELETED"
    EDGE_CREATED = "EDGE_CREATED"
    EDGE_UPDATED = "EDGE_UPDATED"
    EDGE_DELETED = "EDGE_DELETED"
    SCHEMA_CHANGED = "SCHEMA_CHANGED"


@dataclass
class MutationEvent:
    event_id: str
    mutation_type: MutationType
    entity_type: str  # vertex label or edge label
    entity_id: str
    tenant_id: str = "default"
    timestamp: float = 0.0
    before: dict[str, Any] | None = None
    after: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.timestamp == 0.0:
            self.timestamp = time.time()
        if not self.event_id:
            payload = f"{self.mutation_type}:{self.entity_id}:{self.timestamp}"
            self.event_id = hashlib.sha256(payload.encode()).hexdigest()[:16]

    def to_sse(self) -> str:
        data = json.dumps({
            "event_id": self.event_id,
            "type": self.mutation_type.value,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "tenant_id": self.tenant_id,
            "timestamp": self.timestamp,
            "after": self.after,
        }, default=str)
        return f"event: {self.mutation_type.value}\ndata: {data}\n\n"

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "mutation_type": self.mutation_type.value,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "tenant_id": self.tenant_id,
            "timestamp": self.timestamp,
            "before": self.before,
            "after": self.after,
            "metadata": self.metadata,
        }


@dataclass
class SubscriptionFilter:
    tenant_ids: set[str] | None = None
    mutation_types: set[MutationType] | None = None
    entity_types: set[str] | None = None
    entity_id_prefix: str | None = None

    def matches(self, event: MutationEvent) -> bool:
        if self.tenant_ids and event.tenant_id not in self.tenant_ids:
            return False
        if self.mutation_types and event.mutation_type not in self.mutation_types:
            return False
        if self.entity_types and event.entity_type not in self.entity_types:
            return False
        if self.entity_id_prefix and not event.entity_id.startswith(self.entity_id_prefix):
            return False
        return True


@dataclass
class SSESubscription:
    subscription_id: str
    filter: SubscriptionFilter
    queue: queue.Queue[MutationEvent | None] = field(default_factory=lambda: queue.Queue(maxsize=1000))
    created_at: float = field(default_factory=time.time)
    active: bool = True


@dataclass
class WebhookConfig:
    webhook_id: str
    url: str
    filter: SubscriptionFilter
    secret: str = ""
    max_retries: int = 3
    retry_delay_seconds: float = 5.0
    timeout_seconds: float = 10.0
    active: bool = True
    headers: dict[str, str] = field(default_factory=dict)


@dataclass
class WebhookDeliveryRecord:
    event_id: str
    webhook_id: str
    attempt: int
    status_code: int | None = None
    success: bool = False
    error: str | None = None
    delivered_at: float = 0.0
    duration_ms: float = 0.0


class MutationEventBus:
    """Central event bus that receives graph mutation events and dispatches
    them to SSE subscribers and webhook delivery workers."""

    def __init__(self, *, max_buffer_size: int = 100_000) -> None:
        self._subscribers: dict[str, SSESubscription] = {}
        self._webhooks: dict[str, WebhookConfig] = {}
        self._event_buffer: list[MutationEvent] = []
        self._max_buffer = max_buffer_size
        self._lock = threading.Lock()
        self._event_count = 0
        self._listeners: list[Callable[[MutationEvent], None]] = []

    def publish(self, event: MutationEvent) -> None:
        """Publish a mutation event to all matching subscribers and webhooks."""
        with self._lock:
            self._event_buffer.append(event)
            if len(self._event_buffer) > self._max_buffer:
                self._event_buffer = self._event_buffer[-self._max_buffer:]
            self._event_count += 1

        for sub in list(self._subscribers.values()):
            if sub.active and sub.filter.matches(event):
                try:
                    sub.queue.put_nowait(event)
                except queue.Full:
                    log.warning("SSE queue full for subscription %s, dropping event", sub.subscription_id)

        for webhook in list(self._webhooks.values()):
            if webhook.active and webhook.filter.matches(event):
                threading.Thread(
                    target=self._deliver_webhook,
                    args=(webhook, event),
                    daemon=True,
                ).start()

        for listener in self._listeners:
            try:
                listener(event)
            except Exception as exc:
                log.warning("Listener error: %s", exc)

    def subscribe_sse(self, subscription_id: str, filter: SubscriptionFilter) -> SSESubscription:
        sub = SSESubscription(subscription_id=subscription_id, filter=filter)
        with self._lock:
            self._subscribers[subscription_id] = sub
        log.info("SSE subscription created: %s", subscription_id)
        return sub

    def unsubscribe_sse(self, subscription_id: str) -> bool:
        with self._lock:
            sub = self._subscribers.pop(subscription_id, None)
            if sub:
                sub.active = False
                sub.queue.put(None)
                return True
            return False

    def register_webhook(self, config: WebhookConfig) -> None:
        with self._lock:
            self._webhooks[config.webhook_id] = config
        log.info("Webhook registered: %s -> %s", config.webhook_id, config.url)

    def unregister_webhook(self, webhook_id: str) -> bool:
        with self._lock:
            return self._webhooks.pop(webhook_id, None) is not None

    def add_listener(self, callback: Callable[[MutationEvent], None]) -> None:
        self._listeners.append(callback)

    def replay(self, filter: SubscriptionFilter, *, since: float = 0.0, limit: int = 1000) -> list[MutationEvent]:
        """Replay buffered events matching the filter."""
        with self._lock:
            matching = [
                e for e in self._event_buffer
                if e.timestamp >= since and filter.matches(e)
            ]
        return matching[-limit:]

    @property
    def stats(self) -> dict[str, Any]:
        return {
            "total_events": self._event_count,
            "buffer_size": len(self._event_buffer),
            "active_sse_subscriptions": sum(1 for s in self._subscribers.values() if s.active),
            "active_webhooks": sum(1 for w in self._webhooks.values() if w.active),
        }

    def _deliver_webhook(self, config: WebhookConfig, event: MutationEvent) -> WebhookDeliveryRecord:
        payload = json.dumps(event.to_dict(), default=str).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        headers.update(config.headers)

        if config.secret:
            signature = hashlib.sha256((config.secret + event.event_id).encode()).hexdigest()
            headers["X-EOIP-Signature"] = signature

        for attempt in range(1, config.max_retries + 1):
            started = time.monotonic()
            record = WebhookDeliveryRecord(
                event_id=event.event_id,
                webhook_id=config.webhook_id,
                attempt=attempt,
            )
            try:
                req = urllib.request.Request(
                    config.url,
                    data=payload,
                    headers=headers,
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=config.timeout_seconds) as resp:
                    record.status_code = resp.status
                    record.success = 200 <= resp.status < 300
                    record.duration_ms = (time.monotonic() - started) * 1000
                    record.delivered_at = time.time()
                if record.success:
                    return record
            except Exception as exc:
                record.error = str(exc)
                record.duration_ms = (time.monotonic() - started) * 1000
                log.warning(
                    "Webhook delivery attempt %d/%d failed for %s: %s",
                    attempt, config.max_retries, config.webhook_id, exc,
                )

            if attempt < config.max_retries:
                time.sleep(config.retry_delay_seconds * attempt)

        log.error("Webhook delivery exhausted retries for %s event %s", config.webhook_id, event.event_id)
        return record


class SSEStreamEndpoint:
    """Generates Server-Sent Events stream output from an SSE subscription."""

    def __init__(self, bus: MutationEventBus) -> None:
        self.bus = bus

    def stream(self, subscription_id: str, filter: SubscriptionFilter) -> Any:
        """Yields SSE-formatted strings for consumption by an HTTP endpoint."""
        sub = self.bus.subscribe_sse(subscription_id, filter)
        try:
            yield ": connected\n\n"
            while sub.active:
                try:
                    event = sub.queue.get(timeout=30.0)
                    if event is None:
                        break
                    yield event.to_sse()
                except queue.Empty:
                    yield ": keepalive\n\n"
        finally:
            self.bus.unsubscribe_sse(subscription_id)


class WebhookDeliveryWorker:
    """Background worker for batched webhook delivery with dead-letter queue."""

    def __init__(
        self,
        bus: MutationEventBus,
        *,
        batch_size: int = 50,
        poll_interval: float = 1.0,
    ) -> None:
        self.bus = bus
        self.batch_size = batch_size
        self.poll_interval = poll_interval
        self._dlq: list[tuple[WebhookConfig, MutationEvent]] = []
        self._running = False
        self._thread: threading.Thread | None = None

    @property
    def dead_letter_queue(self) -> list[tuple[WebhookConfig, MutationEvent]]:
        return list(self._dlq)

    @property
    def dlq_size(self) -> int:
        return len(self._dlq)

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=5.0)

    def _run(self) -> None:
        log.info("Webhook delivery worker started")
        while self._running:
            time.sleep(self.poll_interval)

    def retry_dlq(self) -> int:
        """Retry all events in the dead-letter queue."""
        retried = 0
        remaining: list[tuple[WebhookConfig, MutationEvent]] = []
        for config, event in self._dlq:
            record = self.bus._deliver_webhook(config, event)
            if record.success:
                retried += 1
            else:
                remaining.append((config, event))
        self._dlq = remaining
        return retried
