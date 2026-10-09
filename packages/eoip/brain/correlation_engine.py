"""Cross-System Correlation & Root Cause Engine — correlates events across systems to find root causes."""

from __future__ import annotations

import threading
import time
import uuid
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class EventSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class CorrelationMethod(str, Enum):
    TEMPORAL = "TEMPORAL"
    CAUSAL = "CAUSAL"
    ENTITY = "ENTITY"
    PATTERN = "PATTERN"


@dataclass
class SystemEvent:
    event_id: str
    system_id: str
    event_type: str
    severity: EventSeverity = EventSeverity.INFO
    entity_id: str = ""
    message: str = ""
    properties: dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["severity"] = self.severity.value
        return d


@dataclass
class Correlation:
    correlation_id: str
    method: CorrelationMethod
    events: list[str] = field(default_factory=list)
    systems: list[str] = field(default_factory=list)
    confidence: float = 0.0
    description: str = ""
    root_cause_event: str | None = None
    impact_score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["method"] = self.method.value
        return d


@dataclass
class RootCauseAnalysis:
    analysis_id: str
    trigger_event: str
    root_causes: list[dict[str, Any]] = field(default_factory=list)
    correlated_events: list[str] = field(default_factory=list)
    affected_systems: list[str] = field(default_factory=list)
    impact_summary: dict[str, Any] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class CorrelationEngine:
    """Correlates events across systems to identify patterns and root causes."""

    def __init__(self, temporal_window_seconds: float = 300.0) -> None:
        self._temporal_window = temporal_window_seconds
        self._events: list[SystemEvent] = []
        self._events_by_system: dict[str, list[SystemEvent]] = defaultdict(list)
        self._events_by_entity: dict[str, list[SystemEvent]] = defaultdict(list)
        self._correlations: dict[str, Correlation] = {}
        self._analyses: dict[str, RootCauseAnalysis] = {}
        self._lock = threading.Lock()
        self._max_events = 50000

    def ingest_event(self, system_id: str, event_type: str,
                     severity: EventSeverity = EventSeverity.INFO,
                     entity_id: str = "", message: str = "",
                     properties: dict[str, Any] | None = None) -> SystemEvent:
        eid = uuid.uuid4().hex[:10]
        event = SystemEvent(
            event_id=eid, system_id=system_id, event_type=event_type,
            severity=severity, entity_id=entity_id, message=message,
            properties=properties or {},
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        )
        with self._lock:
            self._events.append(event)
            self._events_by_system[system_id].append(event)
            if entity_id:
                self._events_by_entity[entity_id].append(event)
            if len(self._events) > self._max_events:
                self._events = self._events[-self._max_events:]
        return event

    def correlate_temporal(self, anchor_event_id: str) -> Correlation:
        anchor = self._find_event(anchor_event_id)
        if not anchor:
            raise ValueError(f"Event {anchor_event_id} not found")

        try:
            anchor_ts = time.mktime(
                time.strptime(anchor.timestamp, "%Y-%m-%dT%H:%M:%SZ"))
        except (ValueError, OverflowError):
            anchor_ts = time.time()

        related: list[str] = []
        systems: set[str] = {anchor.system_id}
        for event in self._events:
            if event.event_id == anchor_event_id:
                continue
            try:
                evt_ts = time.mktime(
                    time.strptime(event.timestamp, "%Y-%m-%dT%H:%M:%SZ"))
            except (ValueError, OverflowError):
                continue
            if abs(evt_ts - anchor_ts) <= self._temporal_window:
                related.append(event.event_id)
                systems.add(event.system_id)

        cid = uuid.uuid4().hex[:10]
        confidence = min(1.0, len(related) * 0.15) if related else 0.0
        correlation = Correlation(
            correlation_id=cid, method=CorrelationMethod.TEMPORAL,
            events=[anchor_event_id] + related, systems=list(systems),
            confidence=round(confidence, 2),
            description=f"Temporal correlation around {anchor.event_type}",
        )
        self._correlations[cid] = correlation
        return correlation

    def correlate_by_entity(self, entity_id: str) -> Correlation:
        events = self._events_by_entity.get(entity_id, [])
        systems = list({e.system_id for e in events})
        cid = uuid.uuid4().hex[:10]
        confidence = min(1.0, len(systems) * 0.2) if len(systems) > 1 else 0.1
        correlation = Correlation(
            correlation_id=cid, method=CorrelationMethod.ENTITY,
            events=[e.event_id for e in events], systems=systems,
            confidence=round(confidence, 2),
            description=f"Entity-based correlation for {entity_id}",
        )
        self._correlations[cid] = correlation
        return correlation

    def analyze_root_cause(self, trigger_event_id: str) -> RootCauseAnalysis:
        trigger = self._find_event(trigger_event_id)
        if not trigger:
            raise ValueError(f"Event {trigger_event_id} not found")

        correlation = self.correlate_temporal(trigger_event_id)
        correlated_events = [self._find_event(eid) for eid in correlation.events]
        correlated_events = [e for e in correlated_events if e]

        root_causes: list[dict[str, Any]] = []
        earliest = trigger
        for event in correlated_events:
            if event.timestamp < earliest.timestamp:
                earliest = event

        if earliest.event_id != trigger_event_id:
            root_causes.append({
                "event_id": earliest.event_id,
                "system": earliest.system_id,
                "type": earliest.event_type,
                "confidence": 0.7,
                "reason": "Earliest event in temporal window",
            })

        error_events = [e for e in correlated_events
                        if e.severity in (EventSeverity.ERROR, EventSeverity.CRITICAL)]
        for event in error_events:
            if event.event_id not in [rc["event_id"] for rc in root_causes]:
                root_causes.append({
                    "event_id": event.event_id,
                    "system": event.system_id,
                    "type": event.event_type,
                    "confidence": 0.5,
                    "reason": "High-severity event in correlation window",
                })

        recommendations: list[str] = []
        affected_systems = correlation.systems
        if len(affected_systems) > 1:
            recommendations.append(
                f"Investigate cross-system dependency between {', '.join(affected_systems)}")
        if error_events:
            recommendations.append(
                f"Review error logs in {error_events[0].system_id}")
        recommendations.append("Consider adding circuit breakers between affected systems")

        aid = uuid.uuid4().hex[:10]
        analysis = RootCauseAnalysis(
            analysis_id=aid, trigger_event=trigger_event_id,
            root_causes=root_causes,
            correlated_events=[e.event_id for e in correlated_events],
            affected_systems=affected_systems,
            impact_summary={
                "total_correlated": len(correlated_events),
                "systems_affected": len(affected_systems),
                "critical_events": len([e for e in correlated_events
                                        if e.severity == EventSeverity.CRITICAL]),
            },
            recommendations=recommendations,
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        )
        self._analyses[aid] = analysis
        return analysis

    def get_event_stream(self, system_id: str | None = None,
                         severity: EventSeverity | None = None,
                         limit: int = 50) -> list[dict[str, Any]]:
        events = self._events
        if system_id:
            events = self._events_by_system.get(system_id, [])
        if severity:
            events = [e for e in events if e.severity == severity]
        return [e.to_dict() for e in events[-limit:]]

    def get_correlation(self, correlation_id: str) -> Correlation | None:
        return self._correlations.get(correlation_id)

    def get_analysis(self, analysis_id: str) -> RootCauseAnalysis | None:
        return self._analyses.get(analysis_id)

    def get_stats(self) -> dict[str, Any]:
        by_system: dict[str, int] = defaultdict(int)
        by_severity: dict[str, int] = defaultdict(int)
        for event in self._events:
            by_system[event.system_id] += 1
            by_severity[event.severity.value] += 1
        return {
            "total_events": len(self._events),
            "total_correlations": len(self._correlations),
            "total_analyses": len(self._analyses),
            "by_system": dict(by_system),
            "by_severity": dict(by_severity),
        }

    def _find_event(self, event_id: str) -> SystemEvent | None:
        for event in reversed(self._events):
            if event.event_id == event_id:
                return event
        return None
