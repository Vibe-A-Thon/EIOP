"""Cognitive copilot engine — multi-turn conversational AI assistant.

Provides multi-turn conversation memory with sliding context window,
proactive insight generation from knowledge graph patterns,
suggested follow-up questions based on conversation trajectory,
and natural-language automation rule engine.
"""

from __future__ import annotations

import hashlib
import math
import re
import threading
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from collections.abc import Callable


class InsightType(str, Enum):
    ANOMALY = "ANOMALY"
    TREND = "TREND"
    CORRELATION = "CORRELATION"
    RECOMMENDATION = "RECOMMENDATION"
    WARNING = "WARNING"
    OPPORTUNITY = "OPPORTUNITY"


class RuleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    TRIGGERED = "TRIGGERED"
    FAILED = "FAILED"


@dataclass
class ConversationTurn:
    turn_id: str
    role: str  # user, assistant, system
    content: str
    timestamp: float = field(default_factory=time.time)
    entities_mentioned: list[str] = field(default_factory=list)
    intent: str = ""
    confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "turn_id": self.turn_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
            "entities_mentioned": self.entities_mentioned,
            "intent": self.intent,
            "confidence": self.confidence,
        }


@dataclass
class ProactiveInsight:
    insight_id: str
    insight_type: InsightType
    title: str
    description: str
    relevance_score: float
    source_entities: list[str] = field(default_factory=list)
    suggested_action: str = ""
    timestamp: float = field(default_factory=time.time)
    dismissed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "insight_id": self.insight_id,
            "type": self.insight_type.value,
            "title": self.title,
            "description": self.description,
            "relevance_score": round(self.relevance_score, 4),
            "source_entities": self.source_entities,
            "suggested_action": self.suggested_action,
            "dismissed": self.dismissed,
        }


@dataclass
class SuggestedQuestion:
    question: str
    category: str
    relevance: float
    context_entities: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "category": self.category,
            "relevance": round(self.relevance, 4),
            "context_entities": self.context_entities,
        }


@dataclass
class AutomationRule:
    rule_id: str
    name: str
    trigger_pattern: str
    action_template: str
    status: RuleStatus = RuleStatus.ACTIVE
    trigger_count: int = 0
    last_triggered: float | None = None
    created_at: float = field(default_factory=time.time)
    cooldown_seconds: float = 60.0
    max_triggers_per_hour: int = 10
    _triggers_this_hour: int = 0
    _hour_start: float = field(default_factory=time.time)

    def can_trigger(self) -> bool:
        if self.status != RuleStatus.ACTIVE:
            return False
        now = time.time()
        if now - self._hour_start >= 3600:
            self._triggers_this_hour = 0
            self._hour_start = now
        if self._triggers_this_hour >= self.max_triggers_per_hour:
            return False
        if self.last_triggered and (now - self.last_triggered) < self.cooldown_seconds:
            return False
        return True

    def record_trigger(self) -> None:
        self.trigger_count += 1
        self._triggers_this_hour += 1
        self.last_triggered = time.time()
        self.status = RuleStatus.TRIGGERED

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "trigger_pattern": self.trigger_pattern,
            "action_template": self.action_template,
            "status": self.status.value,
            "trigger_count": self.trigger_count,
            "last_triggered": self.last_triggered,
            "cooldown_seconds": self.cooldown_seconds,
        }


class ConversationMemory:
    """Sliding-window multi-turn conversation memory with entity tracking."""

    def __init__(self, max_turns: int = 200) -> None:
        self._turns: deque[ConversationTurn] = deque(maxlen=max_turns)
        self._entity_frequency: dict[str, int] = {}
        self._intent_history: list[str] = []
        self._session_id: str = uuid.uuid4().hex[:12]

    @property
    def session_id(self) -> str:
        return self._session_id

    def add_turn(self, role: str, content: str,
                 entities: list[str] | None = None,
                 intent: str = "", confidence: float = 0.0) -> ConversationTurn:
        turn = ConversationTurn(
            turn_id=uuid.uuid4().hex[:8],
            role=role, content=content,
            entities_mentioned=entities or [],
            intent=intent, confidence=confidence,
        )
        self._turns.append(turn)
        for ent in turn.entities_mentioned:
            self._entity_frequency[ent] = self._entity_frequency.get(ent, 0) + 1
        if intent:
            self._intent_history.append(intent)
        return turn

    def get_context_window(self, last_n: int = 10) -> list[ConversationTurn]:
        return list(self._turns)[-last_n:]

    def get_recent_entities(self, last_n: int = 5) -> list[str]:
        entities: list[str] = []
        seen: set[str] = set()
        for turn in reversed(list(self._turns)[-last_n:]):
            for e in turn.entities_mentioned:
                if e not in seen:
                    entities.append(e)
                    seen.add(e)
        return entities

    def top_entities(self, limit: int = 10) -> list[tuple[str, int]]:
        sorted_ents = sorted(
            self._entity_frequency.items(),
            key=lambda x: -x[1],
        )
        return sorted_ents[:limit]

    def detect_topic_shift(self, window: int = 3) -> bool:
        if len(self._turns) < window * 2:
            return False
        turns = list(self._turns)
        recent = set()
        older = set()
        for t in turns[-window:]:
            recent.update(t.entities_mentioned)
        for t in turns[-(window * 2):-window]:
            older.update(t.entities_mentioned)
        if not older and not recent:
            return False
        if not older or not recent:
            return True
        overlap = len(recent & older) / max(len(recent | older), 1)
        return overlap < 0.2

    def summarize(self) -> dict[str, Any]:
        return {
            "session_id": self._session_id,
            "total_turns": len(self._turns),
            "unique_entities": len(self._entity_frequency),
            "intents_tracked": len(self._intent_history),
            "top_entities": self.top_entities(5),
            "topic_shifted": self.detect_topic_shift(),
        }

    def clear(self) -> None:
        self._turns.clear()
        self._entity_frequency.clear()
        self._intent_history.clear()
        self._session_id = uuid.uuid4().hex[:12]


def _extract_entities(text: str) -> list[str]:
    """Extract entity-like tokens from text (capitalized words, quoted terms)."""
    entities: list[str] = []
    for match in re.finditer(r'"([^"]+)"', text):
        entities.append(match.group(1))
    for match in re.finditer(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', text):
        entities.append(match.group(1))
    return list(dict.fromkeys(entities))


def _classify_intent(text: str) -> tuple[str, float]:
    """Simple rule-based intent classification."""
    text_lower = text.lower()
    patterns = [
        (r"\b(what|who|where|when|how|why)\b.*\?", "question", 0.8),
        (r"\b(show|list|get|find|search|look up)\b", "query", 0.75),
        (r"\b(create|add|insert|make|build)\b", "create", 0.7),
        (r"\b(update|change|modify|edit|set)\b", "update", 0.7),
        (r"\b(delete|remove|drop|clear)\b", "delete", 0.7),
        (r"\b(compare|diff|versus|vs)\b", "compare", 0.65),
        (r"\b(explain|describe|summarize|detail)\b", "explain", 0.7),
        (r"\b(alert|warn|notify|escalate)\b", "alert", 0.7),
        (r"\b(analyze|investigate|audit|review)\b", "analyze", 0.7),
    ]
    for pattern, intent, conf in patterns:
        if re.search(pattern, text_lower):
            return intent, conf
    return "general", 0.5


class CopilotEngine:
    """Cognitive copilot with proactive insights and NL automation."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._sessions: dict[str, ConversationMemory] = {}
        self._insights: deque[ProactiveInsight] = deque(maxlen=500)
        self._rules: dict[str, AutomationRule] = {}
        self._entity_knowledge: dict[str, dict[str, Any]] = {}
        self._question_templates: list[tuple[str, str, float]] = [
            ("What relationships does {entity} have?", "exploration", 0.8),
            ("How has {entity} changed recently?", "temporal", 0.7),
            ("Are there any anomalies related to {entity}?", "anomaly", 0.75),
            ("What depends on {entity}?", "dependency", 0.8),
            ("Who owns or maintains {entity}?", "ownership", 0.65),
            ("What is the trust level of {entity}?", "trust", 0.7),
            ("Show me the lineage of {entity}", "lineage", 0.7),
            ("Compare {entity} with similar entities", "comparison", 0.6),
        ]

    def get_or_create_session(self, session_id: str | None = None,
                              max_turns: int = 200) -> ConversationMemory:
        with self._lock:
            if session_id and session_id in self._sessions:
                return self._sessions[session_id]
            mem = ConversationMemory(max_turns=max_turns)
            sid = session_id or mem.session_id
            self._sessions[sid] = mem
            return mem

    def process_message(self, session_id: str, role: str,
                        content: str) -> dict[str, Any]:
        mem = self.get_or_create_session(session_id)
        entities = _extract_entities(content)
        intent, confidence = _classify_intent(content)

        turn = mem.add_turn(
            role=role, content=content,
            entities=entities, intent=intent,
            confidence=confidence,
        )

        triggered_rules = self._check_rules(content)

        return {
            "turn": turn.to_dict(),
            "detected_entities": entities,
            "intent": intent,
            "confidence": confidence,
            "topic_shifted": mem.detect_topic_shift(),
            "triggered_rules": [r.to_dict() for r in triggered_rules],
        }

    def suggest_questions(self, session_id: str,
                          limit: int = 5) -> list[SuggestedQuestion]:
        mem = self._sessions.get(session_id)
        if not mem:
            return []

        recent_entities = mem.get_recent_entities(last_n=3)
        if not recent_entities:
            return []

        suggestions: list[SuggestedQuestion] = []
        for entity in recent_entities[:3]:
            for template, category, base_relevance in self._question_templates:
                freq = mem._entity_frequency.get(entity, 1)
                relevance = base_relevance * (1.0 + math.log1p(freq) * 0.1)
                relevance = min(relevance, 1.0)
                suggestions.append(SuggestedQuestion(
                    question=template.format(entity=entity),
                    category=category,
                    relevance=relevance,
                    context_entities=[entity],
                ))

        suggestions.sort(key=lambda s: -s.relevance)
        seen: set[str] = set()
        unique: list[SuggestedQuestion] = []
        for s in suggestions:
            if s.category not in seen:
                unique.append(s)
                seen.add(s.category)
            if len(unique) >= limit:
                break
        return unique

    def generate_insights(self, entity_stats: dict[str, Any] | None = None,
                          graph_stats: dict[str, Any] | None = None) -> list[ProactiveInsight]:
        insights: list[ProactiveInsight] = []

        if entity_stats:
            total = entity_stats.get("total_entities", 0)
            stale = entity_stats.get("stale_count", 0)
            if total > 0 and stale / max(total, 1) > 0.3:
                insights.append(ProactiveInsight(
                    insight_id=uuid.uuid4().hex[:12],
                    insight_type=InsightType.WARNING,
                    title="High staleness ratio detected",
                    description=f"{stale} of {total} entities ({round(stale/total*100,1)}%) are stale. Consider running maintenance scan.",
                    relevance_score=0.9,
                    suggested_action="Run autonomous maintenance scan",
                ))

            orphan_count = entity_stats.get("orphan_count", 0)
            if orphan_count > 0:
                insights.append(ProactiveInsight(
                    insight_id=uuid.uuid4().hex[:12],
                    insight_type=InsightType.ANOMALY,
                    title="Orphaned entities detected",
                    description=f"{orphan_count} entities have no relationships. They may need linking or removal.",
                    relevance_score=0.7,
                    source_entities=entity_stats.get("orphan_ids", [])[:5],
                    suggested_action="Review and link or archive orphaned entities",
                ))

        if graph_stats:
            edge_count = graph_stats.get("edge_count", 0)
            node_count = graph_stats.get("node_count", 1)
            density = edge_count / max(node_count * (node_count - 1) / 2, 1)
            if density < 0.05 and node_count > 10:
                insights.append(ProactiveInsight(
                    insight_id=uuid.uuid4().hex[:12],
                    insight_type=InsightType.OPPORTUNITY,
                    title="Low graph density — enrichment opportunity",
                    description=f"Graph density is {round(density*100,2)}%. Knowledge reasoning could discover implicit relationships.",
                    relevance_score=0.65,
                    suggested_action="Run inference rules to discover implicit edges",
                ))

            hub_nodes = graph_stats.get("hub_nodes", [])
            if hub_nodes:
                insights.append(ProactiveInsight(
                    insight_id=uuid.uuid4().hex[:12],
                    insight_type=InsightType.TREND,
                    title="Hub node concentration",
                    description=f"{len(hub_nodes)} hub nodes concentrate graph connectivity. Monitor for single-point-of-failure risk.",
                    relevance_score=0.6,
                    source_entities=hub_nodes[:5],
                ))

        for ins in insights:
            self._insights.append(ins)
        return insights

    def get_insights(self, insight_type: InsightType | None = None,
                     include_dismissed: bool = False,
                     limit: int = 20) -> list[ProactiveInsight]:
        results = list(self._insights)
        if not include_dismissed:
            results = [i for i in results if not i.dismissed]
        if insight_type:
            results = [i for i in results if i.insight_type == insight_type]
        return results[-limit:]

    def dismiss_insight(self, insight_id: str) -> bool:
        for ins in self._insights:
            if ins.insight_id == insight_id:
                ins.dismissed = True
                return True
        return False

    def add_rule(self, name: str, trigger_pattern: str,
                 action_template: str,
                 cooldown_seconds: float = 60.0) -> AutomationRule:
        rule = AutomationRule(
            rule_id=uuid.uuid4().hex[:12],
            name=name,
            trigger_pattern=trigger_pattern,
            action_template=action_template,
            cooldown_seconds=cooldown_seconds,
        )
        with self._lock:
            self._rules[rule.rule_id] = rule
        return rule

    def remove_rule(self, rule_id: str) -> bool:
        with self._lock:
            return self._rules.pop(rule_id, None) is not None

    def enable_rule(self, rule_id: str) -> bool:
        rule = self._rules.get(rule_id)
        if not rule:
            return False
        rule.status = RuleStatus.ACTIVE
        return True

    def disable_rule(self, rule_id: str) -> bool:
        rule = self._rules.get(rule_id)
        if not rule:
            return False
        rule.status = RuleStatus.DISABLED
        return True

    def list_rules(self) -> list[AutomationRule]:
        return list(self._rules.values())

    def _check_rules(self, text: str) -> list[AutomationRule]:
        triggered: list[AutomationRule] = []
        for rule in self._rules.values():
            if not rule.can_trigger():
                continue
            try:
                if re.search(rule.trigger_pattern, text, re.IGNORECASE):
                    rule.record_trigger()
                    triggered.append(rule)
            except re.error:
                rule.status = RuleStatus.FAILED
        return triggered

    def register_entity_knowledge(self, entity_id: str,
                                  knowledge: dict[str, Any]) -> None:
        self._entity_knowledge[entity_id] = knowledge

    def list_sessions(self) -> list[dict[str, Any]]:
        return [
            {"session_id": sid, **mem.summarize()}
            for sid, mem in self._sessions.items()
        ]

    def end_session(self, session_id: str) -> bool:
        with self._lock:
            return self._sessions.pop(session_id, None) is not None

    def stats(self) -> dict[str, Any]:
        return {
            "active_sessions": len(self._sessions),
            "total_insights": len(self._insights),
            "active_insights": sum(1 for i in self._insights if not i.dismissed),
            "automation_rules": len(self._rules),
            "active_rules": sum(
                1 for r in self._rules.values()
                if r.status == RuleStatus.ACTIVE
            ),
        }


_instance: CopilotEngine | None = None
_lock = threading.Lock()


def get_copilot_engine() -> CopilotEngine:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = CopilotEngine()
    return _instance
