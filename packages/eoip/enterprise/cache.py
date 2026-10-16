"""Intelligent result cache with TTL, LRU eviction, and semantic fingerprinting.

Caches expensive operations — report generation, graph analysis, LLM synthesis —
with configurable time-to-live. Cache keys include a semantic fingerprint of the
query parameters so that logically identical queries hit the cache even when
whitespace or parameter ordering differs.
"""

from __future__ import annotations

import copy
import hashlib
import json
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any


@dataclass
class CacheEntry:
    key: str
    value: Any
    created_at: float
    ttl_seconds: float
    hit_count: int = 0

    @property
    def expired(self) -> bool:
        return (time.monotonic() - self.created_at) > self.ttl_seconds


@dataclass
class CacheStats:
    hits: int
    misses: int
    evictions: int
    current_size: int
    max_size: int
    hit_rate: float


class IntelligentCache:
    """LRU cache with TTL eviction and semantic key fingerprinting."""

    def __init__(self, max_size: int = 1000, default_ttl: float = 300.0) -> None:
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._store: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0
        self._evictions = 0

    @staticmethod
    def fingerprint(query: str, **params: Any) -> str:
        normalized = query.strip().lower()
        key_data = json.dumps({"q": normalized, **params}, sort_keys=True, default=str)
        return hashlib.sha256(key_data.encode()).hexdigest()[:32]

    def get(self, key: str) -> Any | None:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                self._misses += 1
                return None
            if entry.expired:
                del self._store[key]
                self._misses += 1
                return None
            entry.hit_count += 1
            self._hits += 1
            self._store.move_to_end(key)
            return entry.value

    def put(self, key: str, value: Any, ttl: float | None = None) -> None:
        with self._lock:
            if key in self._store:
                del self._store[key]
            elif len(self._store) >= self._max_size:
                self._store.popitem(last=False)
                self._evictions += 1

            self._store[key] = CacheEntry(
                key=key,
                value=value,
                created_at=time.monotonic(),
                ttl_seconds=ttl or self._default_ttl,
            )

    def invalidate(self, key: str) -> bool:
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False

    def invalidate_pattern(self, prefix: str) -> int:
        with self._lock:
            keys = [k for k in self._store if k.startswith(prefix)]
            for k in keys:
                del self._store[k]
            return len(keys)

    def clear(self) -> int:
        with self._lock:
            count = len(self._store)
            self._store.clear()
            return count

    def stats(self) -> CacheStats:
        with self._lock:
            total = self._hits + self._misses
            return CacheStats(
                hits=self._hits,
                misses=self._misses,
                evictions=self._evictions,
                current_size=len(self._store),
                max_size=self._max_size,
                hit_rate=round(self._hits / total, 4) if total > 0 else 0.0,
            )


_global_cache: IntelligentCache | None = None
_cache_lock = threading.Lock()


def get_cache(max_size: int = 1000, default_ttl: float = 300.0) -> IntelligentCache:
    global _global_cache
    if _global_cache is None:
        with _cache_lock:
            if _global_cache is None:
                _global_cache = IntelligentCache(max_size=max_size, default_ttl=default_ttl)
    return _global_cache


# ============================================================================
# Multi-Level Caching (L1 + L2) Hierarchy (INFRA-001)
# ============================================================================

from enum import Enum


class WritePolicy(str, Enum):
    READ_THROUGH = "READ_THROUGH"
    WRITE_THROUGH = "WRITE_THROUGH"
    WRITE_BEHIND = "WRITE_BEHIND"


class L2Cache:
    """Simulated or distributed secondary cache (Redis-compatible interface)."""

    def __init__(self, default_ttl: float = 3600.0) -> None:
        self._store: dict[str, tuple[Any, float, float]] = {}  # key -> (value, created_at, ttl)
        self._default_ttl = default_ttl
        self._lock = threading.Lock()

    def get(self, key: str) -> Any | None:
        with self._lock:
            item = self._store.get(key)
            if not item:
                return None
            val, created_at, ttl = item
            if (time.monotonic() - created_at) > ttl:
                del self._store[key]
                return None
            return copy.deepcopy(val)

    def set(self, key: str, value: Any, ttl: float | None = None) -> None:
        with self._lock:
            self._store[key] = (copy.deepcopy(value), time.monotonic(), ttl or self._default_ttl)

    def delete(self, key: str) -> bool:
        with self._lock:
            return self._store.pop(key, None) is not None

    def clear(self) -> int:
        with self._lock:
            cnt = len(self._store)
            self._store.clear()
            return cnt


class CacheCoordinator:
    """Coordinates L1 (in-memory) and L2 (distributed) cache levels with distributed invalidation."""

    def __init__(
        self,
        l1_cache: IntelligentCache | None = None,
        l2_cache: L2Cache | None = None,
        policy: WritePolicy = WritePolicy.WRITE_THROUGH,
    ) -> None:
        self.l1 = l1_cache or IntelligentCache(max_size=2000, default_ttl=300.0)
        self.l2 = l2_cache or L2Cache(default_ttl=3600.0)
        self.policy = policy
        self._invalidation_subscribers: list[Any] = []
        self._lock = threading.Lock()
        self._write_behind_queue: list[tuple[str, Any, float | None]] = []

    def get(self, key: str) -> Any | None:
        """Hierarchical fetch: L1 -> L2 (with promotion to L1)."""
        # 1. Check L1
        val = self.l1.get(key)
        if val is not None:
            return val

        # 2. Check L2
        val_l2 = self.l2.get(key)
        if val_l2 is not None:
            # Promote to L1
            self.l1.put(key, val_l2)
            return val_l2

        return None

    def put(self, key: str, value: Any, ttl: float | None = None) -> None:
        """Write item according to coordination policy."""
        if self.policy == WritePolicy.WRITE_THROUGH:
            self.l1.put(key, value, ttl)
            self.l2.set(key, value, ttl)
        elif self.policy == WritePolicy.WRITE_BEHIND:
            self.l1.put(key, value, ttl)
            with self._lock:
                self._write_behind_queue.append((key, value, ttl))
                # Flush async queue
                for k, v, t in self._write_behind_queue:
                    self.l2.set(k, v, t)
                self._write_behind_queue.clear()
        else:  # READ_THROUGH
            self.l2.set(key, value, ttl)

    def invalidate(self, key: str) -> bool:
        """Invalidate key across L1, L2, and notify subscribers."""
        inv_l1 = self.l1.invalidate(key)
        inv_l2 = self.l2.delete(key)
        # Notify subscribers
        for sub in list(self._invalidation_subscribers):
            try:
                sub(key)
            except Exception:
                pass
        return inv_l1 or inv_l2

    def subscribe_invalidation(self, callback: Any) -> None:
        with self._lock:
            self._invalidation_subscribers.append(callback)

    def warm_cache(self, hot_items: dict[str, Any], ttl: float | None = None) -> int:
        """Pre-populate hot paths into both L1 and L2."""
        count = 0
        for k, v in hot_items.items():
            self.put(k, v, ttl=ttl)
            count += 1
        return count

    def stats(self) -> dict[str, Any]:
        l1_stats = self.l1.stats()
        return {
            "policy": self.policy.value,
            "l1_hits": l1_stats.hits,
            "l1_misses": l1_stats.misses,
            "l1_hit_rate": l1_stats.hit_rate,
            "l1_size": l1_stats.current_size,
            "l2_size": len(self.l2._store),
        }


_global_coordinator: CacheCoordinator | None = None
_coord_lock = threading.Lock()


def get_cache_coordinator() -> CacheCoordinator:
    global _global_coordinator
    if _global_coordinator is None:
        with _coord_lock:
            if _global_coordinator is None:
                _global_coordinator = CacheCoordinator()
    return _global_coordinator

