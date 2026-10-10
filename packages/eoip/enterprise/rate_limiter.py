"""Token-bucket rate limiter with per-client and global limits.

Enforces request rate boundaries to prevent abuse and ensure fair usage
across tenants. Supports burst allowance and sliding-window tracking.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Any

from eoip.enterprise.config import get_enterprise_config


@dataclass
class RateLimitResult:
    allowed: bool
    remaining: int
    limit: int
    retry_after: float | None
    client_id: str


class TokenBucket:
    """Classic token bucket with configurable rate and burst."""

    def __init__(self, max_tokens: int, refill_rate: float) -> None:
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        self._tokens = float(max_tokens)
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def try_acquire(self, tokens: int = 1) -> tuple[bool, int, float | None]:
        with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_refill
            self._tokens = min(self.max_tokens, self._tokens + elapsed * self.refill_rate)
            self._last_refill = now

            if self._tokens >= tokens:
                self._tokens -= tokens
                return True, int(self._tokens), None
            else:
                deficit = tokens - self._tokens
                retry_after = deficit / self.refill_rate if self.refill_rate > 0 else 0.0
                return False, 0, retry_after


class RateLimiter:
    """Per-client rate limiter using token buckets."""

    def __init__(
        self,
        max_requests: int | None = None,
        window_seconds: float | None = None,
        burst_size: int | None = None,
    ) -> None:
        cfg = get_enterprise_config().resilience
        self.max_requests = max_requests if max_requests is not None else cfg.rate_limit_max_requests
        self.window_seconds = window_seconds if window_seconds is not None else cfg.rate_limit_window_seconds
        self.burst_size = burst_size if burst_size is not None else cfg.rate_limit_burst_size

        self._refill_rate = self.max_requests / max(self.window_seconds, 0.001)
        self._global_bucket = TokenBucket(self.max_requests + self.burst_size, self._refill_rate)
        self._client_buckets: dict[str, TokenBucket] = {}
        self._lock = threading.Lock()

    def check(self, client_id: str = "global") -> RateLimitResult:
        g_ok, g_remaining, g_retry = self._global_bucket.try_acquire()
        if not g_ok:
            return RateLimitResult(
                allowed=False,
                remaining=0,
                limit=self.max_requests,
                retry_after=g_retry,
                client_id=client_id,
            )

        bucket = self._get_client_bucket(client_id)
        ok, remaining, retry = bucket.try_acquire()
        return RateLimitResult(
            allowed=ok,
            remaining=remaining,
            limit=self.max_requests,
            retry_after=retry,
            client_id=client_id,
        )

    def _get_client_bucket(self, client_id: str) -> TokenBucket:
        with self._lock:
            if client_id not in self._client_buckets:
                per_client_max = max(1, self.max_requests // 2)
                per_client_rate = per_client_max / max(self.window_seconds, 0.001)
                self._client_buckets[client_id] = TokenBucket(
                    per_client_max + self.burst_size, per_client_rate,
                )
            return self._client_buckets[client_id]

    def get_status(self) -> dict[str, Any]:
        with self._lock:
            return {
                "max_requests": self.max_requests,
                "window_seconds": self.window_seconds,
                "burst_size": self.burst_size,
                "active_clients": len(self._client_buckets),
            }
