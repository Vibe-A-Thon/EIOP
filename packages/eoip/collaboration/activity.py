"""Activity Feed — tracks who did what across the platform.

Provides a per-workspace and per-user activity stream with structured
events. Uses a ring buffer for memory-bounded operation.
"""

from __future__ import annotations

import enum
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


class ActivityAction(str, enum.Enum):
    ENTITY_CREATED = "entity.created"
    ENTITY_UPDATED = "entity.updated"
    ENTITY_DELETED = "entity.deleted"
    EDGE_CREATED = "edge.created"
    EDGE_DELETED = "edge.deleted"
    QUERY_EXECUTED = "query.executed"
    QUERY_SAVED = "query.saved"
    REPORT_GENERATED = "report.generated"
    ANNOTATION_ADDED = "annotation.added"
    ANNOTATION_RESOLVED = "annotation.resolved"
    WORKSPACE_CREATED = "workspace.created"
    MEMBER_ADDED = "member.added"
    MEMBER_REMOVED = "member.removed"
    SCHEMA_CHANGED = "schema.changed"
    IMPORT_COMPLETED = "import.completed"
    COMPLIANCE_SCAN = "compliance.scan"
    INCIDENT_OPENED = "incident.opened"
    INCIDENT_RESOLVED = "incident.resolved"


@dataclass
class ActivityEvent:
    event_id: str
    action: ActivityAction
    actor: str
    resource_type: str
    resource_id: str
    summary: str
    workspace_id: str | None = None
    tenant_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "action": self.action.value,
            "actor": self.actor,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "summary": self.summary,
            "workspace_id": self.workspace_id,
            "tenant_id": self.tenant_id,
            "details": self.details,
            "timestamp": self.timestamp,
        }


class ActivityFeed:
    """Ring-buffered activity feed with workspace/user filtering."""

    def __init__(self, max_events: int = 50000) -> None:
        self._events: list[ActivityEvent] = []
        self._max = max_events
        self._lock = threading.Lock()

    def record(
        self,
        action: ActivityAction,
        actor: str,
        resource_type: str,
        resource_id: str,
        summary: str,
        workspace_id: str | None = None,
        tenant_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> ActivityEvent:
        event = ActivityEvent(
            event_id=uuid.uuid4().hex[:12],
            action=action,
            actor=actor,
            resource_type=resource_type,
            resource_id=resource_id,
            summary=summary,
            workspace_id=workspace_id,
            tenant_id=tenant_id,
            details=details or {},
        )
        with self._lock:
            self._events.append(event)
            if len(self._events) > self._max:
                self._events = self._events[-self._max:]
        return event

    def get_feed(
        self,
        workspace_id: str | None = None,
        actor: str | None = None,
        action: ActivityAction | None = None,
        resource_type: str | None = None,
        since: float | None = None,
        limit: int = 50,
    ) -> list[ActivityEvent]:
        with self._lock:
            candidates = self._events

        results = []
        for ev in reversed(candidates):
            if workspace_id and ev.workspace_id != workspace_id:
                continue
            if actor and ev.actor != actor:
                continue
            if action and ev.action != action:
                continue
            if resource_type and ev.resource_type != resource_type:
                continue
            if since and ev.timestamp < since:
                continue
            results.append(ev)
            if len(results) >= limit:
                break
        return results

    def get_user_activity(self, actor: str, limit: int = 50) -> list[ActivityEvent]:
        return self.get_feed(actor=actor, limit=limit)

    def get_workspace_feed(self, workspace_id: str, limit: int = 50) -> list[ActivityEvent]:
        return self.get_feed(workspace_id=workspace_id, limit=limit)

    def stats(self) -> dict[str, Any]:
        with self._lock:
            by_action: dict[str, int] = {}
            actors: set[str] = set()
            for ev in self._events:
                by_action[ev.action.value] = by_action.get(ev.action.value, 0) + 1
                actors.add(ev.actor)
            return {
                "total_events": len(self._events),
                "unique_actors": len(actors),
                "by_action": by_action,
                "buffer_capacity": self._max,
            }


_INSTANCE: ActivityFeed | None = None
_LOCK = threading.Lock()


def get_activity_feed() -> ActivityFeed:
    global _INSTANCE
    if _INSTANCE is None:
        with _LOCK:
            if _INSTANCE is None:
                _INSTANCE = ActivityFeed()
    return _INSTANCE
