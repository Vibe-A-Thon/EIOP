"""Autonomous Knowledge Maintenance — stale detection, confidence decay, auto-enrichment.

Monitors knowledge graph health over time, detects stale entities,
applies configurable decay curves, and suggests or performs enrichment.
"""

from __future__ import annotations

import math
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class DecayPolicy:
    policy_id: str
    name: str
    entity_type: str
    half_life_days: float
    min_confidence: float = 0.1
    decay_function: str = "exponential"
    enabled: bool = True

    def compute_decay(self, age_days: float) -> float:
        if self.decay_function == "exponential":
            return max(self.min_confidence,
                       math.exp(-0.693 * age_days / self.half_life_days))
        elif self.decay_function == "linear":
            return max(self.min_confidence,
                       1.0 - (age_days / (2 * self.half_life_days)))
        return 1.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "name": self.name,
            "entity_type": self.entity_type,
            "half_life_days": self.half_life_days,
            "min_confidence": self.min_confidence,
            "decay_function": self.decay_function,
            "enabled": self.enabled,
        }


@dataclass
class EntityHealth:
    entity_id: str
    entity_type: str
    last_verified_at: float
    last_modified_at: float
    original_confidence: float
    current_confidence: float
    staleness_days: float
    decay_applied: bool = False
    needs_review: bool = False
    enrichment_suggestions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "last_verified_at": self.last_verified_at,
            "last_modified_at": self.last_modified_at,
            "original_confidence": round(self.original_confidence, 3),
            "current_confidence": round(self.current_confidence, 3),
            "staleness_days": round(self.staleness_days, 1),
            "decay_applied": self.decay_applied,
            "needs_review": self.needs_review,
            "enrichment_suggestions": self.enrichment_suggestions,
        }


@dataclass
class StalenessReport:
    report_id: str
    scan_time: float
    total_entities: int
    stale_entities: int
    critical_entities: int
    avg_staleness_days: float
    entities_needing_review: list[EntityHealth]
    decay_policies_applied: int
    enrichments_suggested: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "scan_time": self.scan_time,
            "total_entities": self.total_entities,
            "stale_entities": self.stale_entities,
            "critical_entities": self.critical_entities,
            "avg_staleness_days": round(self.avg_staleness_days, 1),
            "entities_needing_review": [e.to_dict() for e in self.entities_needing_review[:50]],
            "decay_policies_applied": self.decay_policies_applied,
            "enrichments_suggested": self.enrichments_suggested,
        }


@dataclass
class EnrichmentAction:
    action_id: str
    entity_id: str
    action_type: str
    description: str
    priority: int = 0
    status: str = "PENDING"
    result: str | None = None
    created_at: float = field(default_factory=time.time)
    completed_at: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "entity_id": self.entity_id,
            "action_type": self.action_type,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "result": self.result,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }


class MaintenanceEngine:
    """Autonomous knowledge maintenance with decay, staleness scanning, and enrichment."""

    def __init__(self) -> None:
        self._decay_policies: dict[str, DecayPolicy] = {}
        self._entity_health: dict[str, EntityHealth] = {}
        self._enrichment_queue: list[EnrichmentAction] = []
        self._reports: list[StalenessReport] = []
        self._lock = threading.Lock()

    def add_decay_policy(self, name: str, entity_type: str,
                         half_life_days: float,
                         min_confidence: float = 0.1,
                         decay_function: str = "exponential") -> DecayPolicy:
        policy = DecayPolicy(
            policy_id=uuid.uuid4().hex[:12],
            name=name,
            entity_type=entity_type,
            half_life_days=half_life_days,
            min_confidence=min_confidence,
            decay_function=decay_function,
        )
        with self._lock:
            self._decay_policies[policy.policy_id] = policy
        return policy

    def register_entity(self, entity_id: str, entity_type: str,
                        confidence: float,
                        last_verified_at: float | None = None,
                        last_modified_at: float | None = None) -> EntityHealth:
        now = time.time()
        health = EntityHealth(
            entity_id=entity_id,
            entity_type=entity_type,
            last_verified_at=last_verified_at or now,
            last_modified_at=last_modified_at or now,
            original_confidence=confidence,
            current_confidence=confidence,
            staleness_days=0.0,
        )
        with self._lock:
            self._entity_health[entity_id] = health
        return health

    def apply_decay(self, entity_id: str) -> EntityHealth | None:
        with self._lock:
            health = self._entity_health.get(entity_id)
            if health is None:
                return None

            applicable_policies = [
                p for p in self._decay_policies.values()
                if p.enabled and p.entity_type == health.entity_type
            ]

            now = time.time()
            age_days = (now - health.last_verified_at) / 86400.0
            health.staleness_days = age_days

            if applicable_policies:
                best_policy = applicable_policies[0]
                decay_factor = best_policy.compute_decay(age_days)
                health.current_confidence = round(
                    health.original_confidence * decay_factor, 3
                )
                health.decay_applied = True
            else:
                health.current_confidence = health.original_confidence

            health.needs_review = health.current_confidence < 0.5
            return health

    def scan_staleness(self, stale_threshold_days: float = 30.0,
                       critical_threshold: float = 0.3) -> StalenessReport:
        now = time.time()
        stale = []
        critical = []
        all_staleness: list[float] = []
        policies_applied = 0
        enrichments = 0

        with self._lock:
            entities = list(self._entity_health.values())

        for health in entities:
            self.apply_decay(health.entity_id)
            age_days = (now - health.last_verified_at) / 86400.0
            all_staleness.append(age_days)

            if age_days >= stale_threshold_days:
                stale.append(health)
                suggestions = self._suggest_enrichments(health)
                health.enrichment_suggestions = suggestions
                enrichments += len(suggestions)

                if health.current_confidence < critical_threshold:
                    critical.append(health)

            if health.decay_applied:
                policies_applied += 1

        avg = sum(all_staleness) / max(len(all_staleness), 1)

        report = StalenessReport(
            report_id=uuid.uuid4().hex[:12],
            scan_time=now,
            total_entities=len(entities),
            stale_entities=len(stale),
            critical_entities=len(critical),
            avg_staleness_days=avg,
            entities_needing_review=stale,
            decay_policies_applied=policies_applied,
            enrichments_suggested=enrichments,
        )

        with self._lock:
            self._reports.append(report)
            if len(self._reports) > 100:
                self._reports = self._reports[-100:]

        return report

    def _suggest_enrichments(self, health: EntityHealth) -> list[str]:
        suggestions = []
        if health.staleness_days > 90:
            suggestions.append("re-verify from source system")
        if health.current_confidence < 0.3:
            suggestions.append("flag for manual review")
        if health.staleness_days > 30:
            suggestions.append("check for updated source data")
        return suggestions

    def queue_enrichment(self, entity_id: str, action_type: str,
                         description: str, priority: int = 0) -> EnrichmentAction:
        action = EnrichmentAction(
            action_id=uuid.uuid4().hex[:12],
            entity_id=entity_id,
            action_type=action_type,
            description=description,
            priority=priority,
        )
        with self._lock:
            self._enrichment_queue.append(action)
        return action

    def process_enrichment(self, action_id: str, result: str) -> bool:
        with self._lock:
            for action in self._enrichment_queue:
                if action.action_id == action_id:
                    action.status = "COMPLETED"
                    action.result = result
                    action.completed_at = time.time()
                    return True
        return False

    def verify_entity(self, entity_id: str) -> bool:
        with self._lock:
            health = self._entity_health.get(entity_id)
            if health is None:
                return False
            health.last_verified_at = time.time()
            health.staleness_days = 0.0
            health.current_confidence = health.original_confidence
            health.decay_applied = False
            health.needs_review = False
            return True

    def get_entity_health(self, entity_id: str) -> EntityHealth | None:
        self.apply_decay(entity_id)
        with self._lock:
            return self._entity_health.get(entity_id)

    def get_enrichment_queue(self, status: str | None = None,
                             limit: int = 50) -> list[dict[str, Any]]:
        with self._lock:
            queue = list(self._enrichment_queue)
        if status:
            queue = [a for a in queue if a.status == status]
        queue.sort(key=lambda a: a.priority, reverse=True)
        return [a.to_dict() for a in queue[:limit]]

    def stats(self) -> dict[str, Any]:
        with self._lock:
            total = len(self._entity_health)
            stale = sum(1 for h in self._entity_health.values()
                        if h.staleness_days > 30)
            avg_conf = (sum(h.current_confidence for h in self._entity_health.values())
                        / max(total, 1))
            pending_enrichments = sum(1 for a in self._enrichment_queue
                                      if a.status == "PENDING")
            return {
                "total_entities": total,
                "stale_entities": stale,
                "avg_confidence": round(avg_conf, 3),
                "decay_policies": len(self._decay_policies),
                "total_scans": len(self._reports),
                "pending_enrichments": pending_enrichments,
                "total_enrichments": len(self._enrichment_queue),
            }


_INSTANCE: MaintenanceEngine | None = None
_LOCK = threading.Lock()


def get_maintenance_engine() -> MaintenanceEngine:
    global _INSTANCE
    if _INSTANCE is None:
        with _LOCK:
            if _INSTANCE is None:
                _INSTANCE = MaintenanceEngine()
    return _INSTANCE
