"""Natural Language System Configuration — configure systems using plain English commands."""

from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class IntentType(str, Enum):
    REGISTER_SYSTEM = "REGISTER_SYSTEM"
    CONFIGURE_INGESTION = "CONFIGURE_INGESTION"
    SET_SCHEDULE = "SET_SCHEDULE"
    ENABLE_FEATURE = "ENABLE_FEATURE"
    DISABLE_FEATURE = "DISABLE_FEATURE"
    CREATE_PIPELINE = "CREATE_PIPELINE"
    SET_THRESHOLD = "SET_THRESHOLD"
    QUERY_STATUS = "QUERY_STATUS"
    CREATE_ALERT = "CREATE_ALERT"
    MODIFY_SCHEMA = "MODIFY_SCHEMA"
    UNKNOWN = "UNKNOWN"


@dataclass
class ParsedCommand:
    intent: IntentType
    confidence: float
    entities: dict[str, Any] = field(default_factory=dict)
    original_text: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    ambiguous: bool = False
    clarification_needed: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent": self.intent.value,
            "confidence": round(self.confidence, 2),
            "entities": self.entities,
            "parameters": self.parameters,
            "ambiguous": self.ambiguous,
            "clarification_needed": self.clarification_needed,
        }


@dataclass
class ConfigAction:
    action_type: str
    target: str
    params: dict[str, Any] = field(default_factory=dict)
    description: str = ""
    reversible: bool = True


class NLConfigEngine:
    """Parses natural language commands into system configuration actions."""

    _INTENT_PATTERNS: list[tuple[IntentType, list[str]]] = [
        (IntentType.REGISTER_SYSTEM, [
            r"(?:add|register|connect|set up|onboard)\s+(?:a\s+)?(?:new\s+)?(\w+)\s+(?:system|source|server|instance)",
            r"(?:connect|link)\s+(?:to\s+)?(\w+)",
        ]),
        (IntentType.CONFIGURE_INGESTION, [
            r"(?:set|configure|change)\s+(?:the\s+)?ingestion\s+(?:mode|type)\s+(?:to\s+)?(\w+)",
            r"(?:ingest|pull|sync)\s+(?:data\s+)?(?:from\s+)?(\w+)\s+(?:every|each)\s+(\d+)\s*(\w+)",
        ]),
        (IntentType.SET_SCHEDULE, [
            r"(?:schedule|run)\s+(?:\w+\s+)?(?:every|each)\s+(\d+)\s*(minutes?|hours?|days?)",
            r"(?:set|change)\s+(?:the\s+)?(?:sync\s+)?schedule\s+(?:to\s+)?(.+)",
        ]),
        (IntentType.ENABLE_FEATURE, [
            r"(?:enable|turn on|activate|start)\s+(.+)",
        ]),
        (IntentType.DISABLE_FEATURE, [
            r"(?:disable|turn off|deactivate|stop)\s+(.+)",
        ]),
        (IntentType.CREATE_PIPELINE, [
            r"(?:create|build|set up)\s+(?:a\s+)?(?:new\s+)?pipeline\s+(?:for\s+)?(\w+)",
        ]),
        (IntentType.SET_THRESHOLD, [
            r"(?:set|change|update)\s+(?:the\s+)?(\w+)\s+(?:threshold|limit)\s+(?:to\s+)?(\d+\.?\d*)",
            r"(?:alert|notify)\s+(?:me\s+)?(?:when|if)\s+(\w+)\s+(?:exceeds?|is above|goes over)\s+(\d+\.?\d*)",
        ]),
        (IntentType.QUERY_STATUS, [
            r"(?:show|get|what is|check)\s+(?:the\s+)?(?:status|health|state)\s+(?:of\s+)?(\w+)",
            r"(?:how is|is)\s+(\w+)\s+(?:doing|running|working)",
        ]),
        (IntentType.CREATE_ALERT, [
            r"(?:alert|notify|warn)\s+(?:me\s+)?(?:when|if)\s+(.+)",
            r"(?:create|add|set up)\s+(?:an?\s+)?alert\s+(?:for\s+)?(.+)",
        ]),
        (IntentType.MODIFY_SCHEMA, [
            r"(?:add|create)\s+(?:a\s+)?(?:new\s+)?(?:field|property|attribute)\s+(\w+)\s+(?:to\s+)?(\w+)",
            r"(?:rename|change)\s+(?:the\s+)?(?:field|property)\s+(\w+)\s+(?:to\s+)?(\w+)",
        ]),
    ]

    _SYSTEM_ALIASES: dict[str, str] = {
        "jira": "jira", "atlassian": "jira", "github": "github", "gh": "github",
        "gitlab": "gitlab", "gl": "gitlab", "confluence": "confluence",
        "slack": "slack", "postgres": "postgresql", "pg": "postgresql",
        "mysql": "mysql", "mongo": "mongodb", "mongodb": "mongodb",
        "elastic": "elasticsearch", "es": "elasticsearch", "jenkins": "jenkins",
        "sonar": "sonarqube", "grafana": "grafana", "pagerduty": "pagerduty",
        "servicenow": "servicenow", "snow": "servicenow", "splunk": "splunk",
    }

    _TIME_MULTIPLIERS: dict[str, int] = {
        "second": 1, "seconds": 1, "minute": 60, "minutes": 60,
        "hour": 3600, "hours": 3600, "day": 86400, "days": 86400,
    }

    def __init__(self, execute_fn: Callable[[ConfigAction], dict[str, Any]] | None = None) -> None:
        self._execute_fn = execute_fn
        self._command_history: list[ParsedCommand] = []
        self._lock = threading.Lock()

    def parse(self, text: str) -> ParsedCommand:
        text_lower = text.strip().lower()
        best_intent = IntentType.UNKNOWN
        best_confidence = 0.0
        best_match = None
        best_groups: tuple = ()

        for intent, patterns in self._INTENT_PATTERNS:
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    confidence = 0.7 + len(match.group()) / len(text_lower) * 0.3
                    if confidence > best_confidence:
                        best_intent = intent
                        best_confidence = confidence
                        best_match = match
                        best_groups = match.groups()

        entities = self._extract_entities(text_lower, best_groups)
        parameters = self._extract_parameters(best_intent, text_lower, best_groups)

        command = ParsedCommand(
            intent=best_intent, confidence=round(min(best_confidence, 1.0), 2),
            entities=entities, original_text=text,
            parameters=parameters,
            ambiguous=best_confidence < 0.5,
            clarification_needed=self._get_clarification(best_intent, entities) if best_confidence < 0.5 else "",
        )

        with self._lock:
            self._command_history.append(command)
        return command

    def execute(self, command: ParsedCommand) -> dict[str, Any]:
        if command.ambiguous:
            return {
                "success": False,
                "message": f"Command is ambiguous. {command.clarification_needed}",
            }

        action = self._to_action(command)
        if self._execute_fn:
            return self._execute_fn(action)

        return {
            "success": True,
            "action": action.action_type,
            "target": action.target,
            "params": action.params,
            "description": action.description,
            "dry_run": True,
        }

    def parse_and_execute(self, text: str) -> dict[str, Any]:
        command = self.parse(text)
        return {"parsed": command.to_dict(), "result": self.execute(command)}

    def get_history(self, limit: int = 20) -> list[dict[str, Any]]:
        return [c.to_dict() for c in self._command_history[-limit:]]

    def suggest_commands(self, partial: str) -> list[str]:
        suggestions = []
        partial_lower = partial.lower()
        templates = [
            "register a {system} system",
            "set ingestion mode to {mode}",
            "schedule sync every {n} hours",
            "enable {feature}",
            "show status of {system}",
            "create pipeline for {system}",
            "set {metric} threshold to {value}",
            "alert me when {condition}",
        ]
        for t in templates:
            if any(word in t for word in partial_lower.split()):
                suggestions.append(t)
        return suggestions[:5]

    def _extract_entities(self, text: str, groups: tuple) -> dict[str, Any]:
        entities: dict[str, Any] = {}
        for alias, system in self._SYSTEM_ALIASES.items():
            if alias in text:
                entities["system_type"] = system
                break
        for group in groups:
            if group and group in self._SYSTEM_ALIASES:
                entities["system_type"] = self._SYSTEM_ALIASES[group]
        numbers = re.findall(r"\b(\d+\.?\d*)\b", text)
        if numbers:
            entities["numeric_values"] = [float(n) for n in numbers]
        return entities

    def _extract_parameters(self, intent: IntentType, text: str,
                            groups: tuple) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if intent == IntentType.SET_SCHEDULE:
            for i, group in enumerate(groups):
                if group and group.isdigit():
                    params["interval"] = int(group)
                elif group:
                    unit = group.rstrip("s")
                    params["unit"] = unit
                    multiplier = self._TIME_MULTIPLIERS.get(group, 1)
                    if "interval" in params:
                        params["interval_seconds"] = params["interval"] * multiplier

        if intent == IntentType.SET_THRESHOLD:
            for group in groups:
                if group:
                    try:
                        params["threshold_value"] = float(group)
                    except ValueError:
                        params["metric_name"] = group

        if intent in (IntentType.ENABLE_FEATURE, IntentType.DISABLE_FEATURE):
            if groups:
                params["feature"] = groups[0].strip() if groups[0] else ""

        return params

    def _to_action(self, command: ParsedCommand) -> ConfigAction:
        intent = command.intent
        target = command.entities.get("system_type", "")

        if intent == IntentType.REGISTER_SYSTEM:
            return ConfigAction(
                action_type="register_system", target=target,
                params=command.parameters,
                description=f"Register new {target} system",
            )
        elif intent == IntentType.SET_SCHEDULE:
            return ConfigAction(
                action_type="set_schedule", target=target,
                params=command.parameters,
                description=f"Update sync schedule",
            )
        elif intent == IntentType.ENABLE_FEATURE:
            feature = command.parameters.get("feature", "")
            return ConfigAction(
                action_type="enable_feature", target=feature,
                description=f"Enable {feature}",
            )
        elif intent == IntentType.DISABLE_FEATURE:
            feature = command.parameters.get("feature", "")
            return ConfigAction(
                action_type="disable_feature", target=feature,
                description=f"Disable {feature}",
            )
        else:
            return ConfigAction(
                action_type=intent.value.lower(), target=target,
                params=command.parameters,
                description=command.original_text,
            )

    def _get_clarification(self, intent: IntentType,
                           entities: dict[str, Any]) -> str:
        if intent == IntentType.UNKNOWN:
            return "Could not determine intent. Try: 'register a jira system' or 'show status of github'"
        if not entities.get("system_type"):
            return "Which system are you referring to?"
        return "Please provide more details."
