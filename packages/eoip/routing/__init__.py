"""Intent router engineering (CORE-003)."""

from eoip.routing.engine import (
    FastIntentClassifier,
    IntentCategory,
    RouterEngine,
    RoutingDecision,
    get_router_engine,
)

__all__ = [
    "FastIntentClassifier",
    "IntentCategory",
    "RouterEngine",
    "RoutingDecision",
    "get_router_engine",
]
