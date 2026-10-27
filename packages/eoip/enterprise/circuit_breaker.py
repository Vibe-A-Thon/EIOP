"""Thread-safe circuit breaker with half-open probe and exponential backoff.

Wraps any callable with fail-fast protection. When failures exceed the
configured threshold, the circuit opens and rejects calls immediately.
After a cooldown, a limited number of probe calls are allowed through
(half-open); if they succeed the circuit closes, otherwise it reopens.
"""

from __future__ import annotations

import enum
import threading
import time
from dataclasses import dataclass, field
from typing import Any, TypeVar
from collections.abc import Callable

from eoip.enterprise.config import get_enterprise_config

T = TypeVar("T")


class CircuitState(str, enum.Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitOpenError(Exception):
    def __init__(self, name: str, retry_after: float) -> None:
        self.name = name
        self.retry_after = retry_after
        super().__init__(f"Circuit '{name}' is OPEN. Retry after {retry_after:.1f}s.")


@dataclass
class CircuitMetrics:
    name: str
    state: CircuitState
    failure_count: int
    success_count: int
    total_calls: int
    last_failure_time: float | None
    last_state_change: float
    consecutive_successes_in_half_open: int


class CircuitBreaker:
    """Production circuit breaker with configurable thresholds."""

    def __init__(
        self,
        name: str,
        failure_threshold: int | None = None,
        timeout_seconds: float | None = None,
        half_open_max: int | None = None,
    ) -> None:
        cfg = get_enterprise_config().resilience
        self.name = name
        self.failure_threshold = failure_threshold if failure_threshold is not None else cfg.circuit_breaker_failure_threshold
        self.timeout_seconds = timeout_seconds if timeout_seconds is not None else cfg.circuit_breaker_timeout_seconds
        self.half_open_max = half_open_max if half_open_max is not None else cfg.circuit_breaker_half_open_max

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._total_calls = 0
        self._last_failure_time: float | None = None
        self._last_state_change = time.monotonic()
        self._half_open_successes = 0
        self._lock = threading.Lock()

    @property
    def state(self) -> CircuitState:
        with self._lock:
            if self._state == CircuitState.OPEN:
                elapsed = time.monotonic() - self._last_state_change
                if elapsed >= self.timeout_seconds:
                    self._transition(CircuitState.HALF_OPEN)
            return self._state

    def call(self, fn: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        current = self.state
        if current == CircuitState.OPEN:
            retry_after = self.timeout_seconds - (time.monotonic() - self._last_state_change)
            raise CircuitOpenError(self.name, max(0.0, retry_after))

        with self._lock:
            self._total_calls += 1

        try:
            result = fn(*args, **kwargs)
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise

    def _on_success(self) -> None:
        with self._lock:
            self._success_count += 1
            if self._state == CircuitState.HALF_OPEN:
                self._half_open_successes += 1
                if self._half_open_successes >= self.half_open_max:
                    self._transition(CircuitState.CLOSED)
            elif self._state == CircuitState.CLOSED:
                self._failure_count = 0

    def _on_failure(self) -> None:
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.monotonic()
            if self._state == CircuitState.HALF_OPEN:
                self._transition(CircuitState.OPEN)
            elif self._failure_count >= self.failure_threshold:
                self._transition(CircuitState.OPEN)

    def _transition(self, new_state: CircuitState) -> None:
        self._state = new_state
        self._last_state_change = time.monotonic()
        if new_state == CircuitState.CLOSED:
            self._failure_count = 0
            self._half_open_successes = 0
        elif new_state == CircuitState.HALF_OPEN:
            self._half_open_successes = 0

    def reset(self) -> None:
        with self._lock:
            self._transition(CircuitState.CLOSED)
            self._failure_count = 0
            self._success_count = 0

    def get_metrics(self) -> CircuitMetrics:
        with self._lock:
            return CircuitMetrics(
                name=self.name,
                state=self._state,
                failure_count=self._failure_count,
                success_count=self._success_count,
                total_calls=self._total_calls,
                last_failure_time=self._last_failure_time,
                last_state_change=self._last_state_change,
                consecutive_successes_in_half_open=self._half_open_successes,
            )


class CircuitBreakerRegistry:
    """Manages named circuit breakers across subsystems."""

    def __init__(self) -> None:
        self._breakers: dict[str, CircuitBreaker] = {}
        self._lock = threading.Lock()

    def get_or_create(
        self,
        name: str,
        failure_threshold: int | None = None,
        timeout_seconds: float | None = None,
    ) -> CircuitBreaker:
        with self._lock:
            if name not in self._breakers:
                self._breakers[name] = CircuitBreaker(
                    name=name,
                    failure_threshold=failure_threshold,
                    timeout_seconds=timeout_seconds,
                )
            return self._breakers[name]

    def all_metrics(self) -> list[CircuitMetrics]:
        with self._lock:
            return [cb.get_metrics() for cb in self._breakers.values()]

    def reset_all(self) -> None:
        with self._lock:
            for cb in self._breakers.values():
                cb.reset()


_registry: CircuitBreakerRegistry | None = None
_reg_lock = threading.Lock()


def get_circuit_breaker_registry() -> CircuitBreakerRegistry:
    global _registry
    if _registry is None:
        with _reg_lock:
            if _registry is None:
                _registry = CircuitBreakerRegistry()
    return _registry
