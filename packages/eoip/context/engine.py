"""Context engineering engine for ranked context-window construction."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ContextItem:
    item_id: str
    content: str
    priority: str = "MEDIUM"
    source: str = ""
    tokens: int = 0
    created_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.tokens <= 0:
            self.tokens = max(1, len(self.content.split()) * 4 // 3)


@dataclass
class ContextWindow:
    query: str
    items: list[ContextItem]
    token_budget: int
    tokens_used: int
    dropped: list[str] = field(default_factory=list)


class ContextEngine:
    """Rank and pack context items within a token budget."""

    _PRIORITY_WEIGHT = {"CRITICAL": 4.0, "HIGH": 3.0, "MEDIUM": 2.0, "LOW": 1.0}

    def __init__(self, default_token_budget: int = 4096) -> None:
        self.default_token_budget = default_token_budget
        self._lock = threading.Lock()
        self._items: dict[str, ContextItem] = {}
        self._windows_built = 0

    def add_item(self, item: ContextItem) -> None:
        with self._lock:
            self._items[item.item_id] = item

    def build_window(
        self,
        query: str,
        items: list[ContextItem] | None = None,
        *,
        token_budget: int | None = None,
    ) -> ContextWindow:
        budget = token_budget or self.default_token_budget
        candidates = list(items) if items is not None else list(self._items.values())
        ranked = sorted(candidates, key=lambda item: self._score(query, item), reverse=True)
        selected: list[ContextItem] = []
        dropped: list[str] = []
        used = 0
        for item in ranked:
            if used + item.tokens <= budget:
                selected.append(item)
                used += item.tokens
            else:
                dropped.append(item.item_id)
        with self._lock:
            self._windows_built += 1
        return ContextWindow(query=query, items=selected, token_budget=budget, tokens_used=used, dropped=dropped)

    def stats(self) -> dict[str, Any]:
        with self._lock:
            return {
                "engine": "context_engineering",
                "items": len(self._items),
                "windows_built": self._windows_built,
                "default_token_budget": self.default_token_budget,
            }

    def _score(self, query: str, item: ContextItem) -> float:
        query_terms = set(query.lower().split())
        content_terms = set(item.content.lower().split())
        overlap = len(query_terms & content_terms) / max(len(query_terms), 1)
        priority = self._PRIORITY_WEIGHT.get(item.priority.upper(), 2.0)
        recency = 1.0 / (1.0 + (time.time() - item.created_at) / 86400.0)
        return overlap * 10.0 + priority + recency


_instance: ContextEngine | None = None
_lock = threading.Lock()


def get_context_engine() -> ContextEngine:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = ContextEngine()
    return _instance
