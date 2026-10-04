"""Semantic query cache (GAP-CACHE-001..005).

Deterministic query results are cached by normalized QueryPlan (not by raw
prompt text). Each entry records the graph fingerprint it was computed against;
lookups evict stale entries when the fingerprint changes, so results are never
served from a different graph state. AI-response caching is intentionally
separate and out of scope: this cache is for deterministic query execution only
(GAP-CACHE-004).

Integration is opt-in (``EOIP_QUERY_CACHE=1``) so callers choose the
staleness/latency trade-off explicitly.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from typing import Any


def _hash(payload: dict) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


@dataclass
class CacheEntry:
    plan_key: str
    fingerprint: str
    result: Any
    hits: int = 0
    created_marker: dict = field(default_factory=dict)


class SemanticQueryCache:
    """Bounded fingerprint-validated cache for deterministic query results."""

    def __init__(self, max_entries: int = 256) -> None:
        self._max = max_entries
        self._entries: dict[str, CacheEntry] = {}
        self.misses = 0
        self.evictions = 0

    @staticmethod
    def plan_key(plan: dict) -> str:
        normalized = {
            "intent": plan.get("intent"),
            "anchors": sorted(str(a) for a in plan.get("anchors", [])),
            "max_depth": plan.get("max_depth"),
            "result_limit": plan.get("result_limit"),
            "evidence_mode": plan.get("evidence_mode"),
            "label_filter": plan.get("label_filter"),
            "relationship_allowlist": (
                sorted(plan["relationship_allowlist"])
                if plan.get("relationship_allowlist")
                else None
            ),
        }
        return _hash(normalized)

    @staticmethod
    def fingerprint(store) -> str:
        """Cheap graph-state fingerprint; any vertex/edge growth invalidates."""
        return _hash(
            {"vertices": store.count_vertices(), "edges": store.count_edges()}
        )

    def get(self, plan: dict, store):
        key = self.plan_key(plan)
        fingerprint = self.fingerprint(store)
        entry = self._entries.get(key)
        if entry is None:
            self.misses += 1
            return None
        if entry.fingerprint != fingerprint:
            self.evictions += 1
            del self._entries[key]
            self.misses += 1
            return None
        entry.hits += 1
        return entry.result

    def put(self, plan: dict, store, result) -> None:
        key = self.plan_key(plan)
        if len(self._entries) >= self._max and key not in self._entries:
            oldest = min(self._entries, key=lambda k: self._entries[k].hits)
            del self._entries[oldest]
            self.evictions += 1
        self._entries[key] = CacheEntry(
            plan_key=key,
            fingerprint=self.fingerprint(store),
            result=result,
            created_marker={"vertices": store.count_vertices(), "edges": store.count_edges()},
        )

    def stats(self) -> dict[str, int]:
        return {
            "entries": len(self._entries),
            "misses": self.misses,
            "evictions": self.evictions,
            "hits": sum(entry.hits for entry in self._entries.values()),
        }

    def clear(self) -> None:
        self._entries.clear()


def cache_enabled() -> bool:
    return os.environ.get("EOIP_QUERY_CACHE", "").lower() in {"1", "true", "yes"}
