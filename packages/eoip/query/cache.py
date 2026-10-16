"""Semantic query cache (GAP-CACHE-001..005).

Deterministic query results are cached by normalized QueryPlan (not by raw
prompt text). Each entry records the graph fingerprint, graph version, and
source freshness dependencies it was computed against; lookups evict stale entries
when the graph changes, version advances, or freshness expires (GAP-CACHE-002).
CDC events invalidate fine-grained dependent cache entries (GAP-CACHE-003).
Stale results are never served beyond configured staleness policy (GAP-CACHE-005).
AI-response caching is handled by a strictly separate AIResponseCache (GAP-CACHE-004).

Integration is opt-in (``EOIP_QUERY_CACHE=1``) so callers choose the
staleness/latency trade-off explicitly.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
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
    created_at: float = field(default_factory=time.time)
    graph_version: str = "v1"
    source_freshness: dict[str, int] = field(default_factory=dict)
    touched_entities: set[str] = field(default_factory=set)
    max_staleness_seconds: float = 3600.0
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

    def get(
        self,
        plan: dict,
        store,
        *,
        current_graph_version: str = "v1",
        current_source_freshness: dict[str, int] | None = None,
        max_staleness_seconds: float | None = None,
        now: float | None = None,
    ):
        key = self.plan_key(plan)
        fingerprint = self.fingerprint(store)
        entry = self._entries.get(key)
        if entry is None:
            self.misses += 1
            return None

        # Fingerprint invalidation
        if entry.fingerprint != fingerprint:
            self.evictions += 1
            del self._entries[key]
            self.misses += 1
            return None

        # Graph version mismatch invalidation (GAP-CACHE-002)
        if entry.graph_version != current_graph_version:
            self.evictions += 1
            del self._entries[key]
            self.misses += 1
            return None

        # Source freshness invalidation (GAP-CACHE-002)
        if current_source_freshness:
            for src, recorded_freshness in entry.source_freshness.items():
                if current_source_freshness.get(src, recorded_freshness) > recorded_freshness:
                    self.evictions += 1
                    del self._entries[key]
                    self.misses += 1
                    return None

        # Max staleness policy check (GAP-CACHE-005)
        effective_max_staleness = (
            max_staleness_seconds
            if max_staleness_seconds is not None
            else entry.max_staleness_seconds
        )
        current_time = now if now is not None else time.time()
        if (current_time - entry.created_at) > effective_max_staleness:
            self.evictions += 1
            del self._entries[key]
            self.misses += 1
            return None

        entry.hits += 1
        return entry.result

    def put(
        self,
        plan: dict,
        store,
        result,
        *,
        graph_version: str = "v1",
        source_freshness: dict[str, int] | None = None,
        touched_entities: set[str] | list[str] | None = None,
        max_staleness_seconds: float = 3600.0,
        created_at: float | None = None,
    ) -> None:
        key = self.plan_key(plan)
        if len(self._entries) >= self._max and key not in self._entries:
            oldest = min(self._entries, key=lambda k: self._entries[k].hits)
            del self._entries[oldest]
            self.evictions += 1

        self._entries[key] = CacheEntry(
            plan_key=key,
            fingerprint=self.fingerprint(store),
            result=result,
            graph_version=graph_version,
            source_freshness=dict(source_freshness or {}),
            touched_entities=set(touched_entities or []),
            max_staleness_seconds=max_staleness_seconds,
            created_at=created_at if created_at is not None else time.time(),
            created_marker={"vertices": store.count_vertices(), "edges": store.count_edges()},
        )

    def invalidate_cdc(self, events: list[Any]) -> int:
        """Evict entries affected by CDC events (GAP-CACHE-003)."""
        changed_entities = set()
        for ev in events:
            if hasattr(ev, "entity_id"):
                changed_entities.add(ev.entity_id)
            elif isinstance(ev, dict) and "entity_id" in ev:
                changed_entities.add(ev["entity_id"])

        if not changed_entities:
            return 0

        to_evict = []
        for key, entry in self._entries.items():
            if entry.touched_entities and (entry.touched_entities & changed_entities):
                to_evict.append(key)

        for k in to_evict:
            del self._entries[k]
            self.evictions += 1
        return len(to_evict)

    def stats(self) -> dict[str, int]:
        return {
            "entries": len(self._entries),
            "misses": self.misses,
            "evictions": self.evictions,
            "hits": sum(entry.hits for entry in self._entries.values()),
        }

    def clear(self) -> None:
        self._entries.clear()


@dataclass
class AICacheEntry:
    prompt_hash: str
    model: str
    temperature: float
    response: Any
    created_at: float = field(default_factory=time.time)
    ttl_seconds: float = 3600.0
    hits: int = 0


class AIResponseCache:
    """Separate cache for AI responses (GAP-CACHE-004).

    Maintains distinct boundaries from deterministic QueryPlan cache:
    keyed on prompt + model parameters with independent TTL and eviction.
    """

    def __init__(self, max_entries: int = 256, default_ttl_seconds: float = 3600.0) -> None:
        self._max = max_entries
        self._default_ttl = default_ttl_seconds
        self._entries: dict[str, AICacheEntry] = {}
        self.misses = 0
        self.evictions = 0

    @staticmethod
    def prompt_key(prompt: str, model: str = "default", temperature: float = 0.0, **params: Any) -> str:
        normalized = {
            "prompt": prompt.strip(),
            "model": model,
            "temperature": round(temperature, 2),
            "params": {k: params[k] for k in sorted(params)},
        }
        return _hash(normalized)

    def get(
        self,
        prompt: str,
        model: str = "default",
        temperature: float = 0.0,
        now: float | None = None,
        **params: Any,
    ) -> Any | None:
        key = self.prompt_key(prompt, model, temperature, **params)
        entry = self._entries.get(key)
        if entry is None:
            self.misses += 1
            return None
        current_time = now if now is not None else time.time()
        if (current_time - entry.created_at) > entry.ttl_seconds:
            del self._entries[key]
            self.evictions += 1
            self.misses += 1
            return None
        entry.hits += 1
        return entry.response

    def put(
        self,
        prompt: str,
        response: Any,
        model: str = "default",
        temperature: float = 0.0,
        ttl_seconds: float | None = None,
        created_at: float | None = None,
        **params: Any,
    ) -> None:
        key = self.prompt_key(prompt, model, temperature, **params)
        if len(self._entries) >= self._max and key not in self._entries:
            oldest = min(self._entries, key=lambda k: self._entries[k].hits)
            del self._entries[oldest]
            self.evictions += 1
        self._entries[key] = AICacheEntry(
            prompt_hash=key,
            model=model,
            temperature=temperature,
            response=response,
            created_at=created_at if created_at is not None else time.time(),
            ttl_seconds=ttl_seconds if ttl_seconds is not None else self._default_ttl,
        )

    def stats(self) -> dict[str, int]:
        return {
            "entries": len(self._entries),
            "misses": self.misses,
            "evictions": self.evictions,
            "hits": sum(e.hits for e in self._entries.values()),
        }

    def clear(self) -> None:
        self._entries.clear()


def cache_enabled() -> bool:
    return os.environ.get("EOIP_QUERY_CACHE", "").lower() in {"1", "true", "yes"}
