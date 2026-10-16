"""Circuit Breaker — prevents cascading failures with open/half-open/closed states."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

from eoip.enterprise.logging import get_logger
from eoip.enterprise.observability import get_metrics

_log = get_logger("resilience.circuit_breaker")
_obs = get_metrics()


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    success_threshold: int = 3
    timeout_seconds: float = 30.0
    half_open_max_calls: int = 3
    excluded_exceptions: tuple = ()


class CircuitBreaker:
    """Thread-safe circuit breaker with configurable thresholds."""

    def __init__(self, name: str, config: CircuitBreakerConfig | None = None) -> None:
        self.name = name
        self._config = config or CircuitBreakerConfig()
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._half_open_calls = 0
        self._last_failure_time: float = 0
        self._lock = threading.Lock()
        self._metrics = {"total_calls": 0, "total_failures": 0, "total_opens": 0, "total_resets": 0}
        _log.info("initialized circuit_breaker=%s failure_threshold=%d timeout=%.1fs",
                  name, self._config.failure_threshold, self._config.timeout_seconds)

    @property
    def state(self) -> CircuitState:
        with self._lock:
            if self._state == CircuitState.OPEN:
                if time.time() - self._last_failure_time >= self._config.timeout_seconds:
                    self._state = CircuitState.HALF_OPEN
                    self._half_open_calls = 0
                    self._success_count = 0
            return self._state

    def call(self, fn: Callable, *args, **kwargs) -> Any:
        state = self.state

        if state == CircuitState.OPEN:
            raise CircuitOpenError(f"Circuit {self.name} is OPEN")

        with self._lock:
            self._metrics["total_calls"] += 1
            if state == CircuitState.HALF_OPEN:
                if self._half_open_calls >= self._config.half_open_max_calls:
                    raise CircuitOpenError(f"Circuit {self.name} half-open limit reached")
                self._half_open_calls += 1

        try:
            result = fn(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            if not isinstance(e, self._config.excluded_exceptions):
                self._on_failure()
            raise

    def _on_success(self) -> None:
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._success_count += 1
                if self._success_count >= self._config.success_threshold:
                    self._state = CircuitState.CLOSED
                    self._failure_count = 0
                    self._metrics["total_resets"] += 1
            else:
                self._failure_count = 0

    def _on_failure(self) -> None:
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()
            self._metrics["total_failures"] += 1
            _obs.increment("circuit_breaker.failures", circuit=self.name)

            if self._state == CircuitState.HALF_OPEN:
                self._state = CircuitState.OPEN
                self._metrics["total_opens"] += 1
                _log.warning("circuit OPEN (half-open failure) circuit=%s", self.name)
            elif self._failure_count >= self._config.failure_threshold:
                self._state = CircuitState.OPEN
                self._metrics["total_opens"] += 1
                _log.warning("circuit OPEN (threshold reached) circuit=%s failures=%d",
                             self.name, self._failure_count)

    def reset(self) -> None:
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._metrics["total_resets"] += 1

    def get_metrics(self) -> dict[str, Any]:
        with self._lock:
            return {
                "name": self.name,
                "state": self._state.value,
                "failure_count": self._failure_count,
                **self._metrics,
            }


class CircuitOpenError(Exception):
    pass
