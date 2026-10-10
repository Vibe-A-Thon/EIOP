"""Rate Limiter — token-bucket and sliding-window rate limiting per system/tenant."""

from __future__ import annotations

import threading
import time
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class RateLimitStrategy(str, Enum):
    TOKEN_BUCKET = "TOKEN_BUCKET"
    SLIDING_WINDOW = "SLIDING_WINDOW"
    FIXED_WINDOW = "FIXED_WINDOW"


@dataclass
class RateLimitConfig:
    strategy: RateLimitStrategy = RateLimitStrategy.TOKEN_BUCKET
    max_requests: int = 100
    window_seconds: float = 60.0
    burst_size: int = 20
    refill_rate: float = 10.0


class RateLimiter:
    """Thread-safe rate limiter with multiple strategies."""

    def __init__(self, name: str, config: RateLimitConfig | None = None) -> None:
        self.name = name
        self._config = config or RateLimitConfig()
        self._lock = threading.RLock()

        self._tokens = float(self._config.burst_size)
        self._last_refill = time.monotonic()

        self._window_requests: list[float] = []
        self._fixed_window_start = time.monotonic()
        self._fixed_window_count = 0

        self._total_allowed = 0
        self._total_rejected = 0

    def allow(self) -> bool:
        with self._lock:
            strategy = self._config.strategy
            if strategy == RateLimitStrategy.TOKEN_BUCKET:
                return self._token_bucket_allow()
            elif strategy == RateLimitStrategy.SLIDING_WINDOW:
                return self._sliding_window_allow()
            else:
                return self._fixed_window_allow()

    def acquire(self) -> None:
        if not self.allow():
            raise RateLimitExceeded(
                f"Rate limit exceeded for {self.name}: "
                f"{self._config.max_requests}/{self._config.window_seconds}s"
            )

    def remaining(self) -> int:
        with self._lock:
            strategy = self._config.strategy
            if strategy == RateLimitStrategy.TOKEN_BUCKET:
                self._refill_tokens()
                return int(self._tokens)
            elif strategy == RateLimitStrategy.SLIDING_WINDOW:
                now = time.monotonic()
                cutoff = now - self._config.window_seconds
                self._window_requests = [t for t in self._window_requests if t > cutoff]
                return max(0, self._config.max_requests - len(self._window_requests))
            else:
                now = time.monotonic()
                if now - self._fixed_window_start >= self._config.window_seconds:
                    return self._config.max_requests
                return max(0, self._config.max_requests - self._fixed_window_count)

    def reset(self) -> None:
        with self._lock:
            self._tokens = float(self._config.burst_size)
            self._last_refill = time.monotonic()
            self._window_requests.clear()
            self._fixed_window_start = time.monotonic()
            self._fixed_window_count = 0

    def get_metrics(self) -> dict[str, Any]:
        with self._lock:
            return {
                "name": self.name,
                "strategy": self._config.strategy.value,
                "total_allowed": self._total_allowed,
                "total_rejected": self._total_rejected,
                "remaining": self.remaining(),
                "rejection_rate": (
                    self._total_rejected / max(1, self._total_allowed + self._total_rejected)
                ),
            }

    def _token_bucket_allow(self) -> bool:
        self._refill_tokens()
        if self._tokens >= 1.0:
            self._tokens -= 1.0
            self._total_allowed += 1
            return True
        self._total_rejected += 1
        return False

    def _refill_tokens(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(
            float(self._config.burst_size),
            self._tokens + elapsed * self._config.refill_rate,
        )
        self._last_refill = now

    def _sliding_window_allow(self) -> bool:
        now = time.monotonic()
        cutoff = now - self._config.window_seconds
        self._window_requests = [t for t in self._window_requests if t > cutoff]

        if len(self._window_requests) < self._config.max_requests:
            self._window_requests.append(now)
            self._total_allowed += 1
            return True
        self._total_rejected += 1
        return False

    def _fixed_window_allow(self) -> bool:
        now = time.monotonic()
        if now - self._fixed_window_start >= self._config.window_seconds:
            self._fixed_window_start = now
            self._fixed_window_count = 0

        if self._fixed_window_count < self._config.max_requests:
            self._fixed_window_count += 1
            self._total_allowed += 1
            return True
        self._total_rejected += 1
        return False


class RateLimitExceeded(Exception):
    pass
