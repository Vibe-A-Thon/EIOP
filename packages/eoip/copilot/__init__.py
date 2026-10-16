"""Cognitive copilot engine (Tier 11).

Multi-turn conversational memory, proactive insight engine,
suggested questions, and NL automation rules.
"""

from eoip.copilot.engine import (
    AutomationRule,
    ConversationMemory,
    ConversationTurn,
    CopilotEngine,
    InsightType,
    ProactiveInsight,
    SuggestedQuestion,
    get_copilot_engine,
)

__all__ = [
    "AutomationRule",
    "ConversationMemory",
    "ConversationTurn",
    "CopilotEngine",
    "InsightType",
    "ProactiveInsight",
    "SuggestedQuestion",
    "get_copilot_engine",
]
