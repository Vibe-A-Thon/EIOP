"""Data Quality Rules Engine — user-definable quality policies per entity type.

Measures six dimensions: completeness, accuracy, freshness, conformity,
uniqueness, and consistency. Produces per-entity and aggregate scores,
triggers alerts when thresholds are breached, and optionally blocks ingestion.
"""

from __future__ import annotations

import re
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable


class QualityDimension(str, Enum):
    COMPLETENESS = "COMPLETENESS"
    ACCURACY = "ACCURACY"
    FRESHNESS = "FRESHNESS"
    CONFORMITY = "CONFORMITY"
    UNIQUENESS = "UNIQUENESS"
    CONSISTENCY = "CONSISTENCY"


class QualitySeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class QualityRule:
    rule_id: str
    name: str
    dimension: QualityDimension
    entity_type: str  # "*" for all
    field_name: str | None = None  # None = entity-level rule
    rule_type: str = "not_null"  # not_null, regex, range, enum, custom, freshness, unique, cross_field
    params: dict[str, Any] = field(default_factory=dict)
    severity: QualitySeverity = QualitySeverity.WARNING
    enabled: bool = True
    description: str = ""
    block_on_failure: bool = False

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["dimension"] = self.dimension.value
        d["severity"] = self.severity.value
        return d


@dataclass
class RuleViolation:
    rule_id: str
    rule_name: str
    dimension: QualityDimension
    severity: QualitySeverity
    entity_id: str
    field_name: str | None
    message: str
    actual_value: Any = None
    expected: str = ""


@dataclass
class QualityScore:
    entity_id: str
    entity_type: str
    overall_score: float  # 0.0 - 1.0
    dimension_scores: dict[str, float] = field(default_factory=dict)
    violations: list[RuleViolation] = field(default_factory=list)
    rules_evaluated: int = 0
    rules_passed: int = 0
    evaluated_at: str = ""

    @property
    def is_acceptable(self) -> bool:
        return not any(v.severity in (QualitySeverity.ERROR, QualitySeverity.CRITICAL)
                       for v in self.violations)


@dataclass
class QualityReport:
    entity_type: str
    total_entities: int
    average_score: float
    dimension_averages: dict[str, float]
    violation_counts: dict[str, int]
    severity_counts: dict[str, int]
    blocked_count: int
    top_violations: list[dict[str, Any]]
    generated_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class QualityPolicy:
    policy_id: str
    name: str
    entity_type: str
    min_acceptable_score: float = 0.7
    block_below_score: float = 0.3
    alert_below_score: float = 0.5
    rules: list[QualityRule] = field(default_factory=list)
    enabled: bool = True


class DataQualityEngine:
    """Evaluates entities against configurable quality rules and policies."""

    def __init__(self) -> None:
        self._rules: dict[str, QualityRule] = {}
        self._policies: dict[str, QualityPolicy] = {}
        self._custom_validators: dict[str, Callable] = {}
        self._builtin_checks = {
            "not_null": self._check_not_null,
            "regex": self._check_regex,
            "range": self._check_range,
            "enum": self._check_enum,
            "type": self._check_type,
            "length": self._check_length,
            "freshness": self._check_freshness,
            "unique": self._check_unique,
            "cross_field": self._check_cross_field,
            "custom": self._check_custom,
        }
        self._seen_values: dict[str, set] = {}

    # ── Rule Management ──────────────────────────────────

    def add_rule(self, rule: QualityRule) -> None:
        self._rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        return self._rules.pop(rule_id, None) is not None

    def get_rules(self, entity_type: str | None = None) -> list[QualityRule]:
        rules = list(self._rules.values())
        if entity_type:
            rules = [r for r in rules if r.entity_type in (entity_type, "*")]
        return [r for r in rules if r.enabled]

    def add_policy(self, policy: QualityPolicy) -> None:
        self._policies[policy.policy_id] = policy
        for rule in policy.rules:
            self._rules[rule.rule_id] = rule

    def get_policy(self, entity_type: str) -> QualityPolicy | None:
        for p in self._policies.values():
            if p.entity_type == entity_type and p.enabled:
                return p
        return None

    def register_custom_validator(self, name: str, fn: Callable) -> None:
        self._custom_validators[name] = fn

    # ── Evaluation ───────────────────────────────────────

    def evaluate_entity(self, entity: dict[str, Any], entity_type: str) -> QualityScore:
        entity_id = str(entity.get("id", entity.get("canonical_id", "unknown")))
        rules = self.get_rules(entity_type)
        violations: list[RuleViolation] = []
        dimension_passed: dict[str, list[bool]] = {}

        for rule in rules:
            if rule.field_name:
                value = entity.get(rule.field_name)
                ok, msg = self._evaluate_rule(rule, value, entity)
                dim = rule.dimension.value
                dimension_passed.setdefault(dim, []).append(ok)
                if not ok:
                    violations.append(RuleViolation(
                        rule_id=rule.rule_id, rule_name=rule.name,
                        dimension=rule.dimension, severity=rule.severity,
                        entity_id=entity_id, field_name=rule.field_name,
                        message=msg, actual_value=value,
                        expected=str(rule.params),
                    ))
            else:
                ok, msg = self._evaluate_rule(rule, entity, entity)
                dim = rule.dimension.value
                dimension_passed.setdefault(dim, []).append(ok)
                if not ok:
                    violations.append(RuleViolation(
                        rule_id=rule.rule_id, rule_name=rule.name,
                        dimension=rule.dimension, severity=rule.severity,
                        entity_id=entity_id, field_name=None,
                        message=msg,
                    ))

        dim_scores: dict[str, float] = {}
        for dim, results in dimension_passed.items():
            dim_scores[dim] = sum(results) / len(results) if results else 1.0

        all_results = [v for vals in dimension_passed.values() for v in vals]
        overall = sum(all_results) / len(all_results) if all_results else 1.0

        return QualityScore(
            entity_id=entity_id,
            entity_type=entity_type,
            overall_score=round(overall, 4),
            dimension_scores=dim_scores,
            violations=violations,
            rules_evaluated=len(all_results),
            rules_passed=sum(all_results),
            evaluated_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        )

    def evaluate_batch(self, entities: list[dict[str, Any]], entity_type: str) -> list[QualityScore]:
        self._seen_values.clear()
        return [self.evaluate_entity(e, entity_type) for e in entities]

    def generate_report(self, scores: list[QualityScore], entity_type: str) -> QualityReport:
        if not scores:
            return QualityReport(
                entity_type=entity_type, total_entities=0, average_score=0.0,
                dimension_averages={}, violation_counts={}, severity_counts={},
                blocked_count=0, top_violations=[],
                generated_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            )

        avg = sum(s.overall_score for s in scores) / len(scores)
        dim_totals: dict[str, list[float]] = {}
        violation_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}

        for s in scores:
            for dim, val in s.dimension_scores.items():
                dim_totals.setdefault(dim, []).append(val)
            for v in s.violations:
                violation_counts[v.rule_name] = violation_counts.get(v.rule_name, 0) + 1
                severity_counts[v.severity.value] = severity_counts.get(v.severity.value, 0) + 1

        dim_avgs = {d: sum(vals) / len(vals) for d, vals in dim_totals.items()}

        policy = self.get_policy(entity_type)
        block_threshold = policy.block_below_score if policy else 0.3
        blocked = sum(1 for s in scores if s.overall_score < block_threshold)

        top = sorted(violation_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return QualityReport(
            entity_type=entity_type,
            total_entities=len(scores),
            average_score=round(avg, 4),
            dimension_averages={k: round(v, 4) for k, v in dim_avgs.items()},
            violation_counts=violation_counts,
            severity_counts=severity_counts,
            blocked_count=blocked,
            top_violations=[{"rule": r, "count": c} for r, c in top],
            generated_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        )

    def should_block(self, score: QualityScore) -> bool:
        if any(v.block_on_failure for v in score.violations
               if hasattr(v, "block_on_failure")):
            return True
        policy = self.get_policy(score.entity_type)
        if policy and score.overall_score < policy.block_below_score:
            return True
        return any(v.severity == QualitySeverity.CRITICAL for v in score.violations)

    # ── Rule Evaluators ──────────────────────────────────

    def _evaluate_rule(self, rule: QualityRule, value: Any,
                       entity: dict[str, Any]) -> tuple[bool, str]:
        check_fn = self._builtin_checks.get(rule.rule_type)
        if check_fn:
            return check_fn(rule, value, entity)
        return True, ""

    def _check_not_null(self, rule: QualityRule, value: Any, entity: dict) -> tuple[bool, str]:
        if value is None or value == "" or value == []:
            return False, f"{rule.field_name} is null or empty"
        return True, ""

    def _check_regex(self, rule: QualityRule, value: Any, entity: dict) -> tuple[bool, str]:
        pattern = rule.params.get("pattern", "")
        if value is None:
            return False, f"{rule.field_name} is null"
        if not re.match(pattern, str(value)):
            return False, f"{rule.field_name} does not match pattern {pattern}"
        return True, ""

    def _check_range(self, rule: QualityRule, value: Any, entity: dict) -> tuple[bool, str]:
        if value is None:
            return False, f"{rule.field_name} is null"
        try:
            num = float(value)
        except (ValueError, TypeError):
            return False, f"{rule.field_name} is not numeric"
        lo = rule.params.get("min")
        hi = rule.params.get("max")
        if lo is not None and num < lo:
            return False, f"{rule.field_name}={num} below minimum {lo}"
        if hi is not None and num > hi:
            return False, f"{rule.field_name}={num} above maximum {hi}"
        return True, ""

    def _check_enum(self, rule: QualityRule, value: Any, entity: dict) -> tuple[bool, str]:
        allowed = rule.params.get("values", [])
        if value not in allowed:
            return False, f"{rule.field_name}={value} not in {allowed}"
        return True, ""

    def _check_type(self, rule: QualityRule, value: Any, entity: dict) -> tuple[bool, str]:
        expected = rule.params.get("expected_type", "str")
        type_map = {"str": str, "int": int, "float": (int, float), "bool": bool, "list": list, "dict": dict}
        expected_type = type_map.get(expected, str)
        if not isinstance(value, expected_type):
            return False, f"{rule.field_name} expected {expected}, got {type(value).__name__}"
        return True, ""

    def _check_length(self, rule: QualityRule, value: Any, entity: dict) -> tuple[bool, str]:
        if value is None:
            return False, f"{rule.field_name} is null"
        length = len(str(value))
        lo = rule.params.get("min_length", 0)
        hi = rule.params.get("max_length", float("inf"))
        if length < lo:
            return False, f"{rule.field_name} length {length} below minimum {lo}"
        if length > hi:
            return False, f"{rule.field_name} length {length} above maximum {hi}"
        return True, ""

    def _check_freshness(self, rule: QualityRule, value: Any, entity: dict) -> tuple[bool, str]:
        max_age_hours = rule.params.get("max_age_hours", 24)
        if value is None:
            return False, f"{rule.field_name} has no timestamp"
        try:
            ts = time.strptime(str(value)[:19], "%Y-%m-%dT%H:%M:%S")
            age_hours = (time.time() - time.mktime(ts)) / 3600
            if age_hours > max_age_hours:
                return False, f"{rule.field_name} is {age_hours:.1f}h old (max {max_age_hours}h)"
        except (ValueError, OverflowError):
            return False, f"{rule.field_name} has unparseable timestamp"
        return True, ""

    def _check_unique(self, rule: QualityRule, value: Any, entity: dict) -> tuple[bool, str]:
        key = f"{rule.rule_id}:{rule.field_name}"
        seen = self._seen_values.setdefault(key, set())
        val_str = str(value)
        if val_str in seen:
            return False, f"{rule.field_name}={value} is a duplicate"
        seen.add(val_str)
        return True, ""

    def _check_cross_field(self, rule: QualityRule, value: Any, entity: dict) -> tuple[bool, str]:
        field_a = rule.params.get("field_a", "")
        field_b = rule.params.get("field_b", "")
        op = rule.params.get("operator", "==")
        val_a = entity.get(field_a)
        val_b = entity.get(field_b)
        from eoip.workflows.engine import _OPS
        op_fn = _OPS.get(op)
        if op_fn and not op_fn(val_a, val_b):
            return False, f"{field_a}({val_a}) {op} {field_b}({val_b}) failed"
        return True, ""

    def _check_custom(self, rule: QualityRule, value: Any, entity: dict) -> tuple[bool, str]:
        fn_name = rule.params.get("validator", "")
        fn = self._custom_validators.get(fn_name)
        if not fn:
            return True, ""
        try:
            ok = fn(value, entity, rule.params)
            return (True, "") if ok else (False, f"Custom validator '{fn_name}' failed")
        except Exception as e:
            return False, f"Custom validator error: {e}"
