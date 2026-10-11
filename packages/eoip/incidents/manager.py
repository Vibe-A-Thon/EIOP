"""Incident Management — state-machine-driven incident lifecycle.

Tracks incidents through OPEN → ACKNOWLEDGED → INVESTIGATING → MITIGATED → RESOLVED,
with escalation, timeline, and post-mortem support.
"""

from __future__ import annotations

import enum
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


class IncidentSeverity(str, enum.Enum):
    SEV1 = "SEV1"
    SEV2 = "SEV2"
    SEV3 = "SEV3"
    SEV4 = "SEV4"


class IncidentState(str, enum.Enum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    INVESTIGATING = "INVESTIGATING"
    MITIGATED = "MITIGATED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


VALID_TRANSITIONS: dict[IncidentState, set[IncidentState]] = {
    IncidentState.OPEN: {IncidentState.ACKNOWLEDGED, IncidentState.INVESTIGATING},
    IncidentState.ACKNOWLEDGED: {IncidentState.INVESTIGATING, IncidentState.MITIGATED},
    IncidentState.INVESTIGATING: {IncidentState.MITIGATED, IncidentState.RESOLVED},
    IncidentState.MITIGATED: {IncidentState.RESOLVED, IncidentState.INVESTIGATING},
    IncidentState.RESOLVED: {IncidentState.CLOSED, IncidentState.INVESTIGATING},
    IncidentState.CLOSED: set(),
}


@dataclass
class TimelineEntry:
    timestamp: float
    action: str
    actor: str
    details: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "action": self.action,
            "actor": self.actor,
            "details": self.details,
        }


@dataclass
class EscalationRule:
    from_severity: IncidentSeverity
    escalate_after_seconds: float
    notify_roles: list[str]
    auto_escalate_to: IncidentSeverity | None = None


@dataclass
class PostMortem:
    summary: str
    root_cause: str
    impact: str
    timeline_summary: str
    lessons_learned: list[str]
    action_items: list[dict[str, str]]
    created_by: str
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "root_cause": self.root_cause,
            "impact": self.impact,
            "timeline_summary": self.timeline_summary,
            "lessons_learned": self.lessons_learned,
            "action_items": self.action_items,
            "created_by": self.created_by,
            "created_at": self.created_at,
        }


@dataclass
class Incident:
    incident_id: str
    title: str
    description: str
    severity: IncidentSeverity
    state: IncidentState
    reporter: str
    assignee: str | None = None
    tenant_id: str | None = None
    affected_services: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    timeline: list[TimelineEntry] = field(default_factory=list)
    post_mortem: PostMortem | None = None
    escalation_count: int = 0
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    resolved_at: float | None = None
    closed_at: float | None = None

    @property
    def duration_seconds(self) -> float | None:
        if self.resolved_at:
            return self.resolved_at - self.created_at
        return None

    @property
    def mttr_seconds(self) -> float | None:
        return self.duration_seconds

    def to_dict(self) -> dict[str, Any]:
        return {
            "incident_id": self.incident_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "state": self.state.value,
            "reporter": self.reporter,
            "assignee": self.assignee,
            "tenant_id": self.tenant_id,
            "affected_services": self.affected_services,
            "tags": self.tags,
            "timeline": [t.to_dict() for t in self.timeline],
            "post_mortem": self.post_mortem.to_dict() if self.post_mortem else None,
            "escalation_count": self.escalation_count,
            "duration_seconds": self.duration_seconds,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "resolved_at": self.resolved_at,
        }


class IncidentManager:
    """Incident lifecycle manager with state machine, escalation, and post-mortem."""

    def __init__(self) -> None:
        self._incidents: dict[str, Incident] = {}
        self._escalation_rules: list[EscalationRule] = []
        self._lock = threading.Lock()

    def create(self, title: str, description: str, severity: IncidentSeverity,
               reporter: str, assignee: str | None = None,
               tenant_id: str | None = None,
               affected_services: list[str] | None = None,
               tags: list[str] | None = None) -> Incident:
        inc = Incident(
            incident_id=uuid.uuid4().hex[:12],
            title=title,
            description=description,
            severity=severity,
            state=IncidentState.OPEN,
            reporter=reporter,
            assignee=assignee,
            tenant_id=tenant_id,
            affected_services=affected_services or [],
            tags=tags or [],
        )
        inc.timeline.append(TimelineEntry(
            timestamp=inc.created_at,
            action="CREATED",
            actor=reporter,
            details=f"Incident opened: {title}",
        ))
        with self._lock:
            self._incidents[inc.incident_id] = inc
        return inc

    def transition(self, incident_id: str, new_state: IncidentState,
                   actor: str, details: str = "") -> Incident | None:
        with self._lock:
            inc = self._incidents.get(incident_id)
            if inc is None:
                return None
            valid = VALID_TRANSITIONS.get(inc.state, set())
            if new_state not in valid:
                return None
            old_state = inc.state
            inc.state = new_state
            inc.updated_at = time.time()
            inc.timeline.append(TimelineEntry(
                timestamp=inc.updated_at,
                action=f"STATE_CHANGE:{old_state.value}->{new_state.value}",
                actor=actor,
                details=details,
            ))
            if new_state == IncidentState.RESOLVED:
                inc.resolved_at = inc.updated_at
            elif new_state == IncidentState.CLOSED:
                inc.closed_at = inc.updated_at
            return inc

    def assign(self, incident_id: str, assignee: str, actor: str) -> bool:
        with self._lock:
            inc = self._incidents.get(incident_id)
            if inc is None:
                return False
            inc.assignee = assignee
            inc.updated_at = time.time()
            inc.timeline.append(TimelineEntry(
                timestamp=inc.updated_at,
                action="ASSIGNED",
                actor=actor,
                details=f"Assigned to {assignee}",
            ))
            return True

    def escalate(self, incident_id: str, new_severity: IncidentSeverity,
                 actor: str, reason: str = "") -> bool:
        with self._lock:
            inc = self._incidents.get(incident_id)
            if inc is None:
                return False
            old_sev = inc.severity
            inc.severity = new_severity
            inc.escalation_count += 1
            inc.updated_at = time.time()
            inc.timeline.append(TimelineEntry(
                timestamp=inc.updated_at,
                action=f"ESCALATED:{old_sev.value}->{new_severity.value}",
                actor=actor,
                details=reason,
            ))
            return True

    def add_update(self, incident_id: str, actor: str, details: str) -> bool:
        with self._lock:
            inc = self._incidents.get(incident_id)
            if inc is None:
                return False
            inc.updated_at = time.time()
            inc.timeline.append(TimelineEntry(
                timestamp=inc.updated_at,
                action="UPDATE",
                actor=actor,
                details=details,
            ))
            return True

    def attach_post_mortem(self, incident_id: str, summary: str,
                           root_cause: str, impact: str,
                           timeline_summary: str,
                           lessons_learned: list[str],
                           action_items: list[dict[str, str]],
                           created_by: str) -> bool:
        with self._lock:
            inc = self._incidents.get(incident_id)
            if inc is None:
                return False
            inc.post_mortem = PostMortem(
                summary=summary,
                root_cause=root_cause,
                impact=impact,
                timeline_summary=timeline_summary,
                lessons_learned=lessons_learned,
                action_items=action_items,
                created_by=created_by,
            )
            inc.updated_at = time.time()
            inc.timeline.append(TimelineEntry(
                timestamp=inc.updated_at,
                action="POST_MORTEM_ATTACHED",
                actor=created_by,
            ))
            return True

    def add_escalation_rule(self, rule: EscalationRule) -> None:
        with self._lock:
            self._escalation_rules.append(rule)

    def check_escalations(self) -> list[dict[str, Any]]:
        now = time.time()
        escalated = []
        with self._lock:
            for inc in self._incidents.values():
                if inc.state in (IncidentState.RESOLVED, IncidentState.CLOSED):
                    continue
                for rule in self._escalation_rules:
                    if inc.severity != rule.from_severity:
                        continue
                    age = now - inc.created_at
                    if age >= rule.escalate_after_seconds:
                        if rule.auto_escalate_to:
                            old_sev = inc.severity
                            inc.severity = rule.auto_escalate_to
                            inc.escalation_count += 1
                            inc.timeline.append(TimelineEntry(
                                timestamp=now,
                                action=f"AUTO_ESCALATED:{old_sev.value}->{rule.auto_escalate_to.value}",
                                actor="system",
                                details=f"Auto-escalated after {age:.0f}s",
                            ))
                        escalated.append({
                            "incident_id": inc.incident_id,
                            "severity": inc.severity.value,
                            "notify_roles": rule.notify_roles,
                            "age_seconds": round(age, 1),
                        })
        return escalated

    def get(self, incident_id: str) -> Incident | None:
        with self._lock:
            return self._incidents.get(incident_id)

    def list_incidents(self, state: IncidentState | None = None,
                       severity: IncidentSeverity | None = None,
                       assignee: str | None = None,
                       limit: int = 100) -> list[Incident]:
        with self._lock:
            candidates = list(self._incidents.values())
        results = []
        for inc in candidates:
            if state and inc.state != state:
                continue
            if severity and inc.severity != severity:
                continue
            if assignee and inc.assignee != assignee:
                continue
            results.append(inc)
        results.sort(key=lambda i: i.created_at, reverse=True)
        return results[:limit]

    def stats(self) -> dict[str, Any]:
        with self._lock:
            by_state: dict[str, int] = {}
            by_severity: dict[str, int] = {}
            resolved_durations: list[float] = []
            for inc in self._incidents.values():
                by_state[inc.state.value] = by_state.get(inc.state.value, 0) + 1
                by_severity[inc.severity.value] = by_severity.get(inc.severity.value, 0) + 1
                if inc.duration_seconds is not None:
                    resolved_durations.append(inc.duration_seconds)
            avg_mttr = (sum(resolved_durations) / len(resolved_durations)
                        if resolved_durations else None)
            return {
                "total_incidents": len(self._incidents),
                "by_state": by_state,
                "by_severity": by_severity,
                "total_escalations": sum(i.escalation_count for i in self._incidents.values()),
                "avg_mttr_seconds": round(avg_mttr, 1) if avg_mttr else None,
                "with_post_mortem": sum(1 for i in self._incidents.values() if i.post_mortem),
            }


_INSTANCE: IncidentManager | None = None
_LOCK = threading.Lock()


def get_incident_manager() -> IncidentManager:
    global _INSTANCE
    if _INSTANCE is None:
        with _LOCK:
            if _INSTANCE is None:
                _INSTANCE = IncidentManager()
    return _INSTANCE
