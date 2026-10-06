"""Distributed Redis-backed semantic query cache (G2-SCALE-CACHE).

Drop-in distributed variant of :class:`eoip.query.cache.SemanticQueryCache`
with identical key normalization and graph-fingerprint semantics: lookups are
keyed by the normalized QueryPlan hash and validated against the graph
fingerprint stored with the entry, so a result is never served from a
different graph state even when the cache is shared across API replicas.

Redis is optional. When the ``redis`` package is not installed, ``EOIP_REDIS_URL``
is unset, or the server is unreachable, the cache degrades transparently to
the existing in-memory :class:`SemanticQueryCache` (a one-line warning is
logged once) so the base install and all existing tests are unaffected.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

from eoip.query.cache import SemanticQueryCache

logger = logging.getLogger(__name__)

KEY_PREFIX = "eoip:qcache:"
_warned = False


def _connect(redis_url: str | None) -> Any | None:
    """Build a Redis client, or ``None`` to signal in-memory fallback."""
    global _warned
    if not redis_url:
        return None
    try:
        import redis
    except ImportError:
        if not _warned:
            logger.warning(
                "redis package not installed; using in-memory query cache "
                "(pip install eoip[redis] to enable, G2-SCALE-CACHE)"
            )
            _warned = True
        return None
    try:
        client = redis.Redis.from_url(redis_url, socket_timeout=2, socket_connect_timeout=2)
        client.ping()
    except Exception as exc:  # noqa: BLE001 - unreachable server falls back
        logger.warning("Redis at %s unreachable (%s); using in-memory query cache", redis_url, exc)
        return None
    return client


class DistributedQueryCache:
    """Redis-backed cache with fingerprint validation and in-memory fallback.

    Mirrors the ``SemanticQueryCache`` public interface: ``get``, ``put``,
    ``stats``, ``clear``, plus the ``plan_key`` / ``fingerprint`` statics with
    byte-for-byte identical semantics. Entries carry a TTL (default 300s) so
    abandoned keys expire; staleness is still governed by the fingerprint, not
    the TTL. (G2-SCALE-CACHE)
    """

    def __init__(
        self,
        max_entries: int = 256,
        *,
        ttl_seconds: int = 300,
        redis_url: str | None = None,
        client: Any | None = None,
    ) -> None:
        self._fallback = SemanticQueryCache(max_entries=max_entries)
        self._ttl = ttl_seconds
        self._client = client if client is not None else _connect(
            redis_url if redis_url is not None else os.environ.get("EOIP_REDIS_URL")
        )
        self.redis_hits = 0
        self.redis_misses = 0

    @property
    def backend(self) -> str:
        return "redis" if self._client is not None else "memory"

    # Identical normalization/fingerprint semantics to SemanticQueryCache.
    plan_key = staticmethod(SemanticQueryCache.plan_key)
    fingerprint = staticmethod(SemanticQueryCache.fingerprint)

    def _redis_key(self, plan: dict) -> str:
        return KEY_PREFIX + self.plan_key(plan)

    def get(self, plan: dict, store):
        if self._client is None:
            return self._fallback.get(plan, store)
        key = self._redis_key(plan)
        try:
            raw = self._client.get(key)
        except Exception as exc:  # noqa: BLE001 - degrade to memory on errors
            self._disable(exc)
            return self._fallback.get(plan, store)
        if raw is None:
            self.redis_misses += 1
            return None
        try:
            entry = json.loads(raw)
        except (TypeError, ValueError):
            self._client.delete(key)
            self.redis_misses += 1
            return None
        if entry.get("fingerprint") != self.fingerprint(store):
            try:
                self._client.delete(key)
            except Exception as exc:  # noqa: BLE001
                self._disable(exc)
                return None
            self._fallback.evictions += 1
            return None
        self.redis_hits += 1
        return entry.get("result")

    def put(self, plan: dict, store, result) -> None:
        if self._client is None:
            self._fallback.put(plan, store, result)
            return
        try:
            payload = json.dumps(
                {"fingerprint": self.fingerprint(store), "result": result},
                sort_keys=True,
                separators=(",", ":"),
            )
        except (TypeError, ValueError):
            self._fallback.put(plan, store, result)  # non-JSON results stay local
            return
        try:
            self._client.setex(self._redis_key(plan), self._ttl, payload)
        except Exception as exc:  # noqa: BLE001
            self._disable(exc)
            self._fallback.put(plan, store, result)

    def stats(self) -> dict[str, int]:
        stats = self._fallback.stats()
        stats["backend"] = self.backend  # type: ignore[dict-item]
        stats["redis_hits"] = self.redis_hits
        stats["redis_misses"] = self.redis_misses
        return stats

    def clear(self) -> None:
        self._fallback.clear()
        if self._client is None:
            return
        try:
            for key in self._client.scan_iter(f"{KEY_PREFIX}*"):
                self._client.delete(key)
        except Exception as exc:  # noqa: BLE001
            self._disable(exc)

    def _disable(self, exc: Exception) -> None:
        logger.warning("Redis query cache error (%s); falling back to in-memory cache", exc)
        self._client = None
