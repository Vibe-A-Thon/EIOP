"""Knowledge Reasoning Engine — inference rules, temporal reasoning, counterfactual analysis.

Operates on graph structures to derive new facts, evaluate temporal consistency,
and explore counterfactual scenarios.
"""

from __future__ import annotations

import enum
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


class RuleType(str, enum.Enum):
    TRANSITIVE = "TRANSITIVE"
    SYMMETRIC = "SYMMETRIC"
    INVERSE = "INVERSE"
    COMPOSITION = "COMPOSITION"
    SUBSUMPTION = "SUBSUMPTION"
    TEMPORAL = "TEMPORAL"
    CUSTOM = "CUSTOM"


@dataclass
class InferenceRule:
    rule_id: str
    name: str
    rule_type: RuleType
    description: str
    antecedent_pattern: dict[str, Any]
    consequent_pattern: dict[str, Any]
    confidence_weight: float = 1.0
    priority: int = 0
    enabled: bool = True
    fire_count: int = 0
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "rule_type": self.rule_type.value,
            "description": self.description,
            "antecedent_pattern": self.antecedent_pattern,
            "consequent_pattern": self.consequent_pattern,
            "confidence_weight": self.confidence_weight,
            "priority": self.priority,
            "enabled": self.enabled,
            "fire_count": self.fire_count,
        }


@dataclass
class InferenceResult:
    result_id: str
    rule_id: str
    rule_name: str
    inferred_facts: list[dict[str, Any]]
    confidence: float
    supporting_evidence: list[str]
    reasoning_chain: list[str]
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "inferred_facts": self.inferred_facts,
            "confidence": self.confidence,
            "supporting_evidence": self.supporting_evidence,
            "reasoning_chain": self.reasoning_chain,
            "timestamp": self.timestamp,
        }


@dataclass
class TemporalFact:
    entity_id: str
    property_name: str
    value: Any
    valid_from: float
    valid_to: float | None = None
    source: str = ""

    @property
    def is_current(self) -> bool:
        now = time.time()
        return self.valid_from <= now and (self.valid_to is None or self.valid_to > now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "property_name": self.property_name,
            "value": self.value,
            "valid_from": self.valid_from,
            "valid_to": self.valid_to,
            "is_current": self.is_current,
            "source": self.source,
        }


@dataclass
class CounterfactualScenario:
    scenario_id: str
    hypothesis: str
    modifications: list[dict[str, Any]]
    original_state: dict[str, Any]
    projected_state: dict[str, Any]
    impact_score: float
    affected_entities: list[str]
    reasoning: str
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "hypothesis": self.hypothesis,
            "modifications": self.modifications,
            "impact_score": self.impact_score,
            "affected_entities": self.affected_entities,
            "reasoning": self.reasoning,
            "created_at": self.created_at,
        }


class KnowledgeReasoningEngine:
    """Graph-aware reasoning engine with inference, temporal, and counterfactual support."""

    def __init__(self) -> None:
        self._rules: dict[str, InferenceRule] = {}
        self._results: list[InferenceResult] = []
        self._temporal_facts: dict[str, list[TemporalFact]] = {}
        self._scenarios: dict[str, CounterfactualScenario] = {}
        self._lock = threading.Lock()

    def add_rule(self, name: str, rule_type: RuleType,
                 antecedent: dict[str, Any],
                 consequent: dict[str, Any],
                 description: str = "",
                 confidence_weight: float = 1.0,
                 priority: int = 0) -> InferenceRule:
        rule = InferenceRule(
            rule_id=uuid.uuid4().hex[:12],
            name=name,
            rule_type=rule_type,
            description=description,
            antecedent_pattern=antecedent,
            consequent_pattern=consequent,
            confidence_weight=confidence_weight,
            priority=priority,
        )
        with self._lock:
            self._rules[rule.rule_id] = rule
        return rule

    def run_inference(self, facts: list[dict[str, Any]],
                      max_depth: int = 5) -> list[InferenceResult]:
        with self._lock:
            enabled_rules = sorted(
                [r for r in self._rules.values() if r.enabled],
                key=lambda r: r.priority, reverse=True,
            )

        results = []
        current_facts = list(facts)

        for depth in range(max_depth):
            new_inferences = []
            for rule in enabled_rules:
                matched = self._match_rule(rule, current_facts)
                if matched:
                    inferred = []
                    evidence = []
                    for m in matched:
                        inferred_fact = self._apply_consequent(rule, m)
                        if inferred_fact and inferred_fact not in current_facts:
                            inferred.append(inferred_fact)
                            evidence.append(str(m))

                    if inferred:
                        base_conf = len(inferred) / max(len(current_facts), 1)
                        confidence = round(min(0.95, base_conf * rule.confidence_weight), 3)

                        result = InferenceResult(
                            result_id=uuid.uuid4().hex[:12],
                            rule_id=rule.rule_id,
                            rule_name=rule.name,
                            inferred_facts=inferred,
                            confidence=confidence,
                            supporting_evidence=evidence[:10],
                            reasoning_chain=[
                                f"depth={depth}",
                                f"rule={rule.name}",
                                f"matched={len(matched)} facts",
                                f"inferred={len(inferred)} new facts",
                            ],
                        )
                        new_inferences.append(result)
                        current_facts.extend(inferred)

                        with self._lock:
                            rule.fire_count += 1

            if not new_inferences:
                break
            results.extend(new_inferences)

        with self._lock:
            self._results.extend(results)
            if len(self._results) > 1000:
                self._results = self._results[-1000:]

        return results

    def _match_rule(self, rule: InferenceRule,
                    facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        pattern = rule.antecedent_pattern
        matched = []
        for fact in facts:
            if self._matches_pattern(fact, pattern):
                matched.append(fact)
        return matched

    def _matches_pattern(self, fact: dict[str, Any],
                         pattern: dict[str, Any]) -> bool:
        for key, value in pattern.items():
            if key not in fact:
                return False
            if isinstance(value, str) and value.startswith("?"):
                continue
            if fact[key] != value:
                return False
        return True

    def _apply_consequent(self, rule: InferenceRule,
                          matched_fact: dict[str, Any]) -> dict[str, Any] | None:
        result: dict[str, Any] = {}
        for key, value in rule.consequent_pattern.items():
            if isinstance(value, str) and value.startswith("?"):
                var_name = value[1:]
                if var_name in matched_fact:
                    result[key] = matched_fact[var_name]
                elif key in matched_fact:
                    result[key] = matched_fact[key]
                else:
                    result[key] = value
            else:
                result[key] = value
        result["_inferred_by"] = rule.rule_id
        return result if result else None

    def add_temporal_fact(self, entity_id: str, property_name: str,
                          value: Any, valid_from: float,
                          valid_to: float | None = None,
                          source: str = "") -> TemporalFact:
        fact = TemporalFact(
            entity_id=entity_id,
            property_name=property_name,
            value=value,
            valid_from=valid_from,
            valid_to=valid_to,
            source=source,
        )
        with self._lock:
            self._temporal_facts.setdefault(entity_id, []).append(fact)
        return fact

    def get_temporal_state(self, entity_id: str,
                           at_time: float | None = None) -> list[TemporalFact]:
        t = at_time or time.time()
        with self._lock:
            facts = self._temporal_facts.get(entity_id, [])
            return [f for f in facts
                    if f.valid_from <= t and (f.valid_to is None or f.valid_to > t)]

    def get_temporal_history(self, entity_id: str,
                             property_name: str | None = None) -> list[TemporalFact]:
        with self._lock:
            facts = self._temporal_facts.get(entity_id, [])
            if property_name:
                facts = [f for f in facts if f.property_name == property_name]
            return sorted(facts, key=lambda f: f.valid_from)

    def detect_temporal_conflicts(self, entity_id: str) -> list[dict[str, Any]]:
        with self._lock:
            facts = self._temporal_facts.get(entity_id, [])

        conflicts = []
        by_prop: dict[str, list[TemporalFact]] = {}
        for f in facts:
            by_prop.setdefault(f.property_name, []).append(f)

        for prop, prop_facts in by_prop.items():
            sorted_facts = sorted(prop_facts, key=lambda f: f.valid_from)
            for i in range(len(sorted_facts)):
                for j in range(i + 1, len(sorted_facts)):
                    a, b = sorted_facts[i], sorted_facts[j]
                    if a.valid_to is None or a.valid_to > b.valid_from:
                        if a.value != b.value:
                            conflicts.append({
                                "property": prop,
                                "fact_a": a.to_dict(),
                                "fact_b": b.to_dict(),
                                "overlap_start": b.valid_from,
                                "overlap_end": a.valid_to,
                            })
        return conflicts

    def counterfactual(self, hypothesis: str,
                       modifications: list[dict[str, Any]],
                       current_facts: list[dict[str, Any]]) -> CounterfactualScenario:
        modified_facts = list(current_facts)
        affected = set()

        for mod in modifications:
            action = mod.get("action", "modify")
            target_id = mod.get("entity_id", "")
            affected.add(target_id)

            if action == "remove":
                modified_facts = [f for f in modified_facts
                                  if f.get("entity_id") != target_id]
            elif action == "modify":
                for f in modified_facts:
                    if f.get("entity_id") == target_id:
                        for k, v in mod.get("changes", {}).items():
                            f[k] = v
            elif action == "add":
                modified_facts.append(mod.get("fact", {}))

        new_inferences = self.run_inference(modified_facts, max_depth=3)
        impact = len(new_inferences) / max(len(current_facts), 1)
        for r in new_inferences:
            for fact in r.inferred_facts:
                eid = fact.get("entity_id", "")
                if eid:
                    affected.add(eid)

        scenario = CounterfactualScenario(
            scenario_id=uuid.uuid4().hex[:12],
            hypothesis=hypothesis,
            modifications=modifications,
            original_state={"fact_count": len(current_facts)},
            projected_state={"fact_count": len(modified_facts),
                             "new_inferences": len(new_inferences)},
            impact_score=round(min(1.0, impact), 3),
            affected_entities=list(affected),
            reasoning=f"Applied {len(modifications)} modifications, "
                      f"derived {len(new_inferences)} new inferences",
        )

        with self._lock:
            self._scenarios[scenario.scenario_id] = scenario
        return scenario

    def get_rules(self) -> list[dict[str, Any]]:
        with self._lock:
            return [r.to_dict() for r in self._rules.values()]

    def get_recent_inferences(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._lock:
            return [r.to_dict() for r in reversed(self._results[-limit:])]

    def stats(self) -> dict[str, Any]:
        with self._lock:
            total_fires = sum(r.fire_count for r in self._rules.values())
            by_type: dict[str, int] = {}
            for r in self._rules.values():
                by_type[r.rule_type.value] = by_type.get(r.rule_type.value, 0) + 1
            return {
                "total_rules": len(self._rules),
                "enabled_rules": sum(1 for r in self._rules.values() if r.enabled),
                "total_inferences": len(self._results),
                "total_rule_fires": total_fires,
                "rules_by_type": by_type,
                "temporal_entities": len(self._temporal_facts),
                "scenarios_evaluated": len(self._scenarios),
            }


_INSTANCE: KnowledgeReasoningEngine | None = None
_LOCK = threading.Lock()


def get_knowledge_reasoning_engine() -> KnowledgeReasoningEngine:
    global _INSTANCE
    if _INSTANCE is None:
        with _LOCK:
            if _INSTANCE is None:
                _INSTANCE = KnowledgeReasoningEngine()
    return _INSTANCE
