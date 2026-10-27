"""Adaptive Learning Feedback Loop — learns from user corrections and system outcomes to improve over time."""

from __future__ import annotations

import threading
import time
import uuid
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any
from collections.abc import Callable

from eoip.enterprise.logging import get_logger

_log = get_logger("brain.adaptive_learning")


class FeedbackType(str, Enum):
    CORRECTION = "CORRECTION"
    APPROVAL = "APPROVAL"
    REJECTION = "REJECTION"
    RATING = "RATING"
    SUGGESTION = "SUGGESTION"
    OUTCOME = "OUTCOME"


class LearningDomain(str, Enum):
    SCHEMA_MAPPING = "SCHEMA_MAPPING"
    ENTITY_RESOLUTION = "ENTITY_RESOLUTION"
    RELATIONSHIP_EXTRACTION = "RELATIONSHIP_EXTRACTION"
    CLASSIFICATION = "CLASSIFICATION"
    PRIORITY_SCORING = "PRIORITY_SCORING"
    ANOMALY_DETECTION = "ANOMALY_DETECTION"
    QUERY_OPTIMIZATION = "QUERY_OPTIMIZATION"


@dataclass
class FeedbackEntry:
    feedback_id: str
    feedback_type: FeedbackType
    domain: LearningDomain
    context: dict[str, Any] = field(default_factory=dict)
    original_output: Any = None
    corrected_output: Any = None
    rating: float = 0.0
    user_id: str = ""
    created_at: str = ""
    applied: bool = False

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["feedback_type"] = self.feedback_type.value
        d["domain"] = self.domain.value
        return d


@dataclass
class LearningRule:
    rule_id: str
    domain: LearningDomain
    condition: dict[str, Any]
    action: dict[str, Any]
    confidence: float = 0.5
    times_applied: int = 0
    times_correct: int = 0
    created_from_feedback: str = ""

    @property
    def accuracy(self) -> float:
        if self.times_applied == 0:
            return 0.0
        return self.times_correct / self.times_applied

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["domain"] = self.domain.value
        d["accuracy"] = round(self.accuracy, 4)
        return d


class AdaptiveLearningEngine:
    """Learns from feedback to improve schema mapping, entity resolution, and classification."""

    def __init__(self) -> None:
        self._feedback: list[FeedbackEntry] = []
        self._rules: dict[str, LearningRule] = {}
        self._domain_rules: dict[LearningDomain, list[str]] = defaultdict(list)
        self._lock = threading.Lock()
        self._confidence_threshold = 0.6
        self._min_samples_for_rule = 3
        self._pattern_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    def submit_feedback(self, feedback_type: FeedbackType,
                        domain: LearningDomain,
                        context: dict[str, Any] | None = None,
                        original_output: Any = None,
                        corrected_output: Any = None,
                        rating: float = 0.0,
                        user_id: str = "") -> FeedbackEntry:
        fid = uuid.uuid4().hex[:10]
        entry = FeedbackEntry(
            feedback_id=fid, feedback_type=feedback_type, domain=domain,
            context=context or {}, original_output=original_output,
            corrected_output=corrected_output, rating=rating,
            user_id=user_id,
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        )
        with self._lock:
            self._feedback.append(entry)

            if feedback_type == FeedbackType.CORRECTION and corrected_output is not None:
                self._try_derive_rule(entry)

        return entry

    def apply_rules(self, domain: LearningDomain,
                    context: dict[str, Any], default_output: Any) -> Any:
        with self._lock:
            rule_ids = self._domain_rules.get(domain, [])
            best_rule: LearningRule | None = None
            best_confidence = 0.0

            for rid in rule_ids:
                rule = self._rules.get(rid)
                if not rule or rule.confidence < self._confidence_threshold:
                    continue
                if self._matches_condition(rule.condition, context):
                    if rule.confidence > best_confidence:
                        best_rule = rule
                        best_confidence = rule.confidence

            if best_rule:
                best_rule.times_applied += 1
                return best_rule.action.get("output", default_output)

            return default_output

    def record_outcome(self, domain: LearningDomain,
                       context: dict[str, Any], output: Any,
                       was_correct: bool) -> None:
        with self._lock:
            rule_ids = self._domain_rules.get(domain, [])
            for rid in rule_ids:
                rule = self._rules.get(rid)
                if rule and self._matches_condition(rule.condition, context):
                    if was_correct:
                        rule.times_correct += 1
                        rule.confidence = min(1.0, rule.confidence + 0.05)
                    else:
                        rule.confidence = max(0.0, rule.confidence - 0.1)

    def get_rules(self, domain: LearningDomain | None = None) -> list[dict[str, Any]]:
        rules = list(self._rules.values())
        if domain:
            rules = [r for r in rules if r.domain == domain]
        return [r.to_dict() for r in rules]

    def get_feedback_stats(self) -> dict[str, Any]:
        by_type: dict[str, int] = defaultdict(int)
        by_domain: dict[str, int] = defaultdict(int)
        for entry in self._feedback:
            by_type[entry.feedback_type.value] += 1
            by_domain[entry.domain.value] += 1

        return {
            "total_feedback": len(self._feedback),
            "total_rules": len(self._rules),
            "by_type": dict(by_type),
            "by_domain": dict(by_domain),
            "avg_rule_accuracy": self._avg_rule_accuracy(),
        }

    def prune_weak_rules(self, min_accuracy: float = 0.3,
                         min_applications: int = 5) -> int:
        pruned = 0
        with self._lock:
            to_remove: list[str] = []
            for rid, rule in self._rules.items():
                if rule.times_applied >= min_applications and rule.accuracy < min_accuracy:
                    to_remove.append(rid)
            for rid in to_remove:
                rule = self._rules.pop(rid)
                self._domain_rules[rule.domain] = [
                    r for r in self._domain_rules[rule.domain] if r != rid
                ]
                pruned += 1
        return pruned

    def _try_derive_rule(self, entry: FeedbackEntry) -> None:
        pattern_key = f"{entry.domain.value}:{str(sorted(entry.context.items()))}"
        self._pattern_counts[pattern_key][str(entry.corrected_output)] += 1

        count = self._pattern_counts[pattern_key][str(entry.corrected_output)]
        if count >= self._min_samples_for_rule:
            rid = uuid.uuid4().hex[:8]
            rule = LearningRule(
                rule_id=rid, domain=entry.domain,
                condition=dict(entry.context),
                action={"output": entry.corrected_output},
                confidence=min(0.9, 0.5 + count * 0.05),
                created_from_feedback=entry.feedback_id,
            )
            self._rules[rid] = rule
            self._domain_rules[entry.domain].append(rid)

    def _matches_condition(self, condition: dict[str, Any],
                           context: dict[str, Any]) -> bool:
        for key, value in condition.items():
            if context.get(key) != value:
                return False
        return True

    def _avg_rule_accuracy(self) -> float:
        rules_with_data = [r for r in self._rules.values() if r.times_applied > 0]
        if not rules_with_data:
            return 0.0
        return round(sum(r.accuracy for r in rules_with_data) / len(rules_with_data), 4)
