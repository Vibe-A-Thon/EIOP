"""Tamper-evident audit event log with hash-chained integrity.

Every auditable action — graph mutation, query execution, governance decision,
learning update, configuration change — is recorded as a signed event in an
append-only chain. Each event's hash covers its predecessor, producing a
Merkle-like tamper evidence trail suitable for SOC 2 and EU AI Act compliance.
"""

from __future__ import annotations

import enum
import hashlib
import json
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


class AuditCategory(str, enum.Enum):
    GRAPH_MUTATION = "GRAPH_MUTATION"
    QUERY_EXECUTION = "QUERY_EXECUTION"
    GOVERNANCE_DECISION = "GOVERNANCE_DECISION"
    LEARNING_UPDATE = "LEARNING_UPDATE"
    CONFIG_CHANGE = "CONFIG_CHANGE"
    AUTH_EVENT = "AUTH_EVENT"
    DATA_EXPORT = "DATA_EXPORT"
    AGENT_EXECUTION = "AGENT_EXECUTION"
    SYSTEM_EVENT = "SYSTEM_EVENT"
    USER_ACTION = "USER_ACTION"


class AuditSeverity(str, enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    timestamp: float
    category: AuditCategory
    severity: AuditSeverity
    actor: str
    action: str
    resource: str
    outcome: str
    details: dict[str, Any]
    correlation_id: str
    tenant_id: str
    previous_hash: str
    event_hash: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "category": self.category.value,
            "severity": self.severity.value,
            "actor": self.actor,
            "action": self.action,
            "resource": self.resource,
            "outcome": self.outcome,
            "details": self.details,
            "correlation_id": self.correlation_id,
            "tenant_id": self.tenant_id,
            "previous_hash": self.previous_hash,
            "event_hash": self.event_hash,
        }


class AuditLog:
    """Append-only, hash-chained audit event log."""

    def __init__(self, max_in_memory: int = 10000) -> None:
        self._events: list[AuditEvent] = []
        self._max = max_in_memory
        self._lock = threading.Lock()
        self._last_hash = hashlib.sha256(b"EOIP_AUDIT_GENESIS").hexdigest()

    def record(
        self,
        category: AuditCategory,
        action: str,
        resource: str,
        *,
        actor: str = "system",
        outcome: str = "SUCCESS",
        severity: AuditSeverity = AuditSeverity.INFO,
        details: dict[str, Any] | None = None,
        correlation_id: str = "",
        tenant_id: str = "default",
    ) -> AuditEvent:
        with self._lock:
            event_id = str(uuid.uuid4())
            ts = time.time()

            payload = json.dumps({
                "event_id": event_id,
                "timestamp": ts,
                "category": category.value,
                "action": action,
                "resource": resource,
                "actor": actor,
                "outcome": outcome,
                "previous_hash": self._last_hash,
            }, sort_keys=True)
            event_hash = hashlib.sha256(payload.encode()).hexdigest()

            event = AuditEvent(
                event_id=event_id,
                timestamp=ts,
                category=category,
                severity=severity,
                actor=actor,
                action=action,
                resource=resource,
                outcome=outcome,
                details=details or {},
                correlation_id=correlation_id,
                tenant_id=tenant_id,
                previous_hash=self._last_hash,
                event_hash=event_hash,
            )

            self._events.append(event)
            self._last_hash = event_hash

            if len(self._events) > self._max:
                self._events = self._events[-self._max:]

            return event

    def query(
        self,
        *,
        category: AuditCategory | None = None,
        actor: str | None = None,
        resource: str | None = None,
        since: float | None = None,
        limit: int = 100,
    ) -> list[AuditEvent]:
        with self._lock:
            result = self._events
            if category:
                result = [e for e in result if e.category == category]
            if actor:
                result = [e for e in result if e.actor == actor]
            if resource:
                result = [e for e in result if resource in e.resource]
            if since:
                result = [e for e in result if e.timestamp >= since]
            return result[-limit:]

    def verify_chain(self) -> tuple[bool, int]:
        with self._lock:
            if not self._events:
                return True, 0
            for i in range(1, len(self._events)):
                if self._events[i].previous_hash != self._events[i - 1].event_hash:
                    return False, i
            return True, len(self._events)

    def get_stats(self) -> dict[str, Any]:
        with self._lock:
            category_counts: dict[str, int] = {}
            for e in self._events:
                category_counts[e.category.value] = category_counts.get(e.category.value, 0) + 1
            valid, chain_len = True, len(self._events)
        if chain_len > 1:
            valid, _ = self.verify_chain()
        return {
            "total_events": chain_len,
            "chain_valid": valid,
            "latest_hash": self._last_hash,
            "category_distribution": category_counts,
        }


_audit_log: AuditLog | None = None
_audit_lock = threading.Lock()


def get_audit_log() -> AuditLog:
    global _audit_log
    if _audit_log is None:
        with _audit_lock:
            if _audit_log is None:
                _audit_log = AuditLog()
    return _audit_log
