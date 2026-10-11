"""Retry with Exponential Backoff & Jitter.

Enterprise-grade retry policy for external calls (graph backends, LLM
providers, webhook deliveries). Supports configurable max attempts,
backoff base/cap, jitter, and per-exception filtering.
"""

from __future__ import annotations

import logging
import random
import time
from dataclasses import dataclass, field
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class RetryPolicy:
    max_attempts: int = 3
    base_delay: float = 0.5
    max_delay: float = 30.0
    exponential_base: float = 2.0
    jitter: bool = True
    retryable_exceptions: tuple[type[Exception], ...] = (Exception,)


@dataclass
class RetryOutcome:
    success: bool
    attempts: int
    total_delay_ms: float
    last_error: str | None = None
    attempt_log: list[dict[str, Any]] = field(default_factory=list)


def compute_delay(attempt: int, policy: RetryPolicy) -> float:
    delay = min(
        policy.max_delay,
        policy.base_delay * (policy.exponential_base ** attempt),
    )
    if policy.jitter:
        delay = delay * (0.5 + random.random() * 0.5)
    return delay


def retry_sync(
    fn: Callable[..., T],
    *args: Any,
    policy: RetryPolicy | None = None,
    on_retry: Callable[[int, Exception, float], None] | None = None,
    **kwargs: Any,
) -> tuple[T, RetryOutcome]:
    pol = policy or RetryPolicy()
    outcome = RetryOutcome(success=False, attempts=0, total_delay_ms=0.0)

    for attempt in range(pol.max_attempts):
        outcome.attempts = attempt + 1
        try:
            result = fn(*args, **kwargs)
            outcome.success = True
            outcome.attempt_log.append({
                "attempt": attempt + 1,
                "status": "OK",
            })
            return result, outcome
        except pol.retryable_exceptions as exc:
            outcome.last_error = f"{type(exc).__name__}: {exc}"
            outcome.attempt_log.append({
                "attempt": attempt + 1,
                "status": "FAILED",
                "error": outcome.last_error,
            })

            if attempt + 1 >= pol.max_attempts:
                break

            delay = compute_delay(attempt, pol)
            outcome.total_delay_ms += delay * 1000
            if on_retry:
                on_retry(attempt + 1, exc, delay)
            logger.warning(
                "Retry %d/%d after %.2fs: %s",
                attempt + 1, pol.max_attempts, delay, exc,
            )
            time.sleep(delay)

    raise RetryExhausted(
        f"All {pol.max_attempts} attempts failed. Last error: {outcome.last_error}",
        outcome=outcome,
    )


class RetryExhausted(Exception):
    def __init__(self, message: str, outcome: RetryOutcome) -> None:
        super().__init__(message)
        self.outcome = outcome


class RetryableOperation:
    """Wraps a callable with a retry policy for reuse across the application."""

    def __init__(self, fn: Callable[..., Any], policy: RetryPolicy | None = None) -> None:
        self._fn = fn
        self._policy = policy or RetryPolicy()
        self._total_calls = 0
        self._total_retries = 0
        self._total_failures = 0

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        self._total_calls += 1
        try:
            result, outcome = retry_sync(self._fn, *args, policy=self._policy, **kwargs)
            self._total_retries += outcome.attempts - 1
            return result
        except RetryExhausted:
            self._total_failures += 1
            raise

    def stats(self) -> dict[str, Any]:
        return {
            "total_calls": self._total_calls,
            "total_retries": self._total_retries,
            "total_failures": self._total_failures,
            "policy": {
                "max_attempts": self._policy.max_attempts,
                "base_delay": self._policy.base_delay,
                "max_delay": self._policy.max_delay,
            },
        }
