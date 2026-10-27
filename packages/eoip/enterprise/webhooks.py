"""Webhook Event Notification System.

Enterprise event-driven architecture for notifying external systems about
graph mutations, query events, health changes, and audit-worthy actions.
Supports per-subscriber filtering, HMAC-SHA256 signature verification,
delivery retry with backoff, and dead-letter tracking.
"""

from __future__ import annotations

import enum
import hashlib
import hmac
import json
import logging
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any
from collections.abc import Callable

logger = logging.getLogger(__name__)


class WebhookEventType(str, enum.Enum):
    GRAPH_MUTATION = "graph.mutation"
    GRAPH_QUERY = "graph.query"
    ENTITY_CREATED = "entity.created"
    ENTITY_UPDATED = "entity.updated"
    ENTITY_DELETED = "entity.deleted"
    HEALTH_DEGRADED = "health.degraded"
    HEALTH_RECOVERED = "health.recovered"
    CIRCUIT_OPEN = "circuit.open"
    CIRCUIT_CLOSED = "circuit.closed"
    AUDIT_ALERT = "audit.alert"
    LEARNING_UPDATED = "learning.updated"
    PLUGIN_LOADED = "plugin.loaded"
    TENANT_PROVISIONED = "tenant.provisioned"
    SCHEMA_CHANGED = "schema.changed"


@dataclass
class WebhookSubscription:
    subscription_id: str
    url: str
    events: set[WebhookEventType]
    secret: str = ""
    active: bool = True
    created_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)
    max_retries: int = 3


@dataclass
class WebhookDelivery:
    delivery_id: str
    subscription_id: str
    event_type: str
    payload: dict[str, Any]
    status: str = "PENDING"
    attempts: int = 0
    last_attempt_at: float | None = None
    response_code: int | None = None
    error: str | None = None
    created_at: float = field(default_factory=time.time)


class WebhookManager:
    """Manages webhook subscriptions, event dispatch, and delivery tracking."""

    def __init__(self, delivery_fn: Callable[[str, dict[str, str], str], int] | None = None) -> None:
        self._subscriptions: dict[str, WebhookSubscription] = {}
        self._deliveries: list[WebhookDelivery] = []
        self._dead_letters: list[WebhookDelivery] = []
        self._lock = threading.Lock()
        self._delivery_fn = delivery_fn
        self._total_dispatched = 0
        self._total_delivered = 0
        self._total_failed = 0

    def subscribe(
        self,
        url: str,
        events: list[WebhookEventType],
        secret: str = "",
        headers: dict[str, str] | None = None,
        max_retries: int = 3,
        metadata: dict[str, Any] | None = None,
    ) -> WebhookSubscription:
        sub = WebhookSubscription(
            subscription_id=uuid.uuid4().hex[:12],
            url=url,
            events=set(events),
            secret=secret,
            headers=headers or {},
            max_retries=max_retries,
            metadata=metadata or {},
        )
        with self._lock:
            self._subscriptions[sub.subscription_id] = sub
        return sub

    def unsubscribe(self, subscription_id: str) -> bool:
        with self._lock:
            return self._subscriptions.pop(subscription_id, None) is not None

    def list_subscriptions(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {
                    "subscription_id": s.subscription_id,
                    "url": s.url,
                    "events": [e.value for e in s.events],
                    "active": s.active,
                    "created_at": s.created_at,
                }
                for s in self._subscriptions.values()
            ]

    def dispatch(self, event_type: WebhookEventType, payload: dict[str, Any]) -> int:
        with self._lock:
            matching = [
                s for s in self._subscriptions.values()
                if s.active and event_type in s.events
            ]

        delivered = 0
        for sub in matching:
            delivery = WebhookDelivery(
                delivery_id=uuid.uuid4().hex[:12],
                subscription_id=sub.subscription_id,
                event_type=event_type.value,
                payload=payload,
            )
            self._total_dispatched += 1
            success = self._deliver(sub, delivery)
            with self._lock:
                if success:
                    delivery.status = "DELIVERED"
                    self._total_delivered += 1
                    delivered += 1
                else:
                    delivery.status = "DEAD_LETTER"
                    self._dead_letters.append(delivery)
                    self._total_failed += 1
                self._deliveries.append(delivery)
                if len(self._deliveries) > 10000:
                    self._deliveries = self._deliveries[-5000:]

        return delivered

    def _deliver(self, sub: WebhookSubscription, delivery: WebhookDelivery) -> bool:
        body = json.dumps({
            "event": delivery.event_type,
            "delivery_id": delivery.delivery_id,
            "timestamp": time.time(),
            "payload": delivery.payload,
        })

        headers = dict(sub.headers)
        headers["Content-Type"] = "application/json"
        headers["X-Webhook-Event"] = delivery.event_type
        headers["X-Webhook-Delivery"] = delivery.delivery_id
        if sub.secret:
            sig = hmac.new(sub.secret.encode(), body.encode(), hashlib.sha256).hexdigest()
            headers["X-Webhook-Signature"] = f"sha256={sig}"

        if self._delivery_fn is None:
            delivery.attempts = 1
            delivery.last_attempt_at = time.time()
            delivery.response_code = 200
            return True

        for attempt in range(sub.max_retries):
            delivery.attempts = attempt + 1
            delivery.last_attempt_at = time.time()
            try:
                code = self._delivery_fn(sub.url, headers, body)
                delivery.response_code = code
                if 200 <= code < 300:
                    return True
            except Exception as exc:
                delivery.error = str(exc)
            if attempt + 1 < sub.max_retries:
                time.sleep(min(30, 0.5 * (2 ** attempt)))

        return False

    def get_dead_letters(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {
                    "delivery_id": d.delivery_id,
                    "subscription_id": d.subscription_id,
                    "event_type": d.event_type,
                    "attempts": d.attempts,
                    "error": d.error,
                    "created_at": d.created_at,
                }
                for d in self._dead_letters[-limit:]
            ]

    def stats(self) -> dict[str, Any]:
        with self._lock:
            return {
                "subscriptions": len(self._subscriptions),
                "active_subscriptions": sum(1 for s in self._subscriptions.values() if s.active),
                "total_dispatched": self._total_dispatched,
                "total_delivered": self._total_delivered,
                "total_failed": self._total_failed,
                "dead_letter_count": len(self._dead_letters),
            }


_INSTANCE: WebhookManager | None = None
_INSTANCE_LOCK = threading.Lock()


def get_webhook_manager() -> WebhookManager:
    global _INSTANCE
    if _INSTANCE is None:
        with _INSTANCE_LOCK:
            if _INSTANCE is None:
                _INSTANCE = WebhookManager()
    return _INSTANCE
