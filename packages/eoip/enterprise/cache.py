"""Intelligent result cache with TTL, LRU eviction, and semantic fingerprinting.

Caches expensive operations — report generation, graph analysis, LLM synthesis —
with configurable time-to-live. Cache keys include a semantic fingerprint of the
query parameters so that logically identical queries hit the cache even when
whitespace or parameter ordering differs.
"""

from __future__ import annotations

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
