"""Context engineering engine for ranked context-window construction."""

from __future__ import annotations

import hashlib
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

    @property
    def content_hash(self) -> str:
        return hashlib.sha256(self.content.strip().encode("utf-8")).hexdigest()[:16]

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "content": self.content,
            "priority": self.priority,
            "source": self.source,
            "tokens": self.tokens,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }


@dataclass
class ContextWindow:
    query: str
    items: list[ContextItem]
    token_budget: int
    tokens_used: int
    dropped: list[str] = field(default_factory=list)

    def render(self) -> str:
        """Render context items into prompt-ready structured markdown text."""
        sections = []
        for idx, item in enumerate(self.items, start=1):
            source_tag = f" [Source: {item.source}]" if item.source else ""
            sections.append(f"### [Context #{idx}{source_tag}]\n{item.content}")
        return "\n\n".join(sections)

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "items": [item.to_dict() for item in self.items],
            "token_budget": self.token_budget,
            "tokens_used": self.tokens_used,
            "dropped_count": len(self.dropped),
            "dropped_ids": self.dropped,
            "rendered": self.render(),
        }


class ContextEngine:
    """Rank, deduplicate, and pack context items within a strict token budget."""

    _PRIORITY_WEIGHT = {"CRITICAL": 5.0, "HIGH": 3.5, "MEDIUM": 2.0, "LOW": 1.0}

    def __init__(self, default_token_budget: int = 4096) -> None:
        self.default_token_budget = default_token_budget
        self._lock = threading.Lock()
        self._items: dict[str, ContextItem] = {}
        self._windows_built = 0

    def add_item(self, item: ContextItem) -> None:
        with self._lock:
            self._items[item.item_id] = item

    def add_items(self, items: list[ContextItem]) -> int:
        with self._lock:
            for item in items:
                self._items[item.item_id] = item
            return len(items)

    def list_items(self) -> list[ContextItem]:
        with self._lock:
            return list(self._items.values())

    def create_graph_item(
        self,
        node_id: str,
        label: str,
        properties: dict[str, Any],
        neighbors: list[str] | None = None,
        priority: str = "HIGH",
    ) -> ContextItem:
        """Helper to create a structured context item from a graph node."""
        props_str = ", ".join(f"{k}: {v}" for k, v in properties.items())
        nbrs_str = f" Connected to: {', '.join(neighbors)}" if neighbors else ""
        content = f"Entity '{node_id}' ({label}): {props_str}.{nbrs_str}"
        return ContextItem(
            item_id=f"graph-{node_id}",
            content=content,
            priority=priority,
            source="canonical_graph",
            metadata={"node_id": node_id, "label": label, "properties": properties},
        )

    def build_window(
        self,
        query: str,
        items: list[ContextItem] | None = None,
        *,
        token_budget: int | None = None,
        deduplicate: bool = True,
    ) -> ContextWindow:
        budget = token_budget or self.default_token_budget
        candidates = list(items) if items is not None else list(self._items.values())

        # Deduplication by exact content hash
        if deduplicate:
            seen_hashes: set[str] = set()
            unique_candidates: list[ContextItem] = []
            for c in candidates:
                h = c.content_hash
                if h not in seen_hashes:
                    seen_hashes.add(h)
                    unique_candidates.append(c)
            candidates = unique_candidates

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

        return ContextWindow(
            query=query,
            items=selected,
            token_budget=budget,
            tokens_used=used,
            dropped=dropped,
        )

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

