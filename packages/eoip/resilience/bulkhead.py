"""Bulkhead — isolates workloads to prevent one failing system from starving others."""

from __future__ import annotations

import threading
import time
from dataclasses import asdict, dataclass
from typing import Any
from collections.abc import Callable

from eoip.enterprise.logging import get_logger

_log = get_logger("resilience.bulkhead")


@dataclass
class BulkheadConfig:
    max_concurrent: int = 10
    max_queue_size: int = 50
    queue_timeout_seconds: float = 30.0


class Bulkhead:
    """Thread-safe bulkhead that limits concurrent access per partition."""

    def __init__(self, name: str, config: BulkheadConfig | None = None) -> None:
        self.name = name
        self._config = config or BulkheadConfig()
        self._semaphore = threading.Semaphore(self._config.max_concurrent)
        self._queue_count = 0
        self._lock = threading.Lock()
        self._active = 0
        self._total_accepted = 0
        self._total_rejected = 0
        self._total_queued = 0
        self._total_completed = 0
        self._total_timeouts = 0

    def execute(self, fn: Callable, *args, **kwargs) -> Any:
        with self._lock:
            if self._queue_count >= self._config.max_queue_size:
                self._total_rejected += 1
                raise BulkheadFullError(
                    f"Bulkhead {self.name}: queue full "
                    f"({self._queue_count}/{self._config.max_queue_size})"
                )
            self._queue_count += 1
            self._total_queued += 1

        acquired = self._semaphore.acquire(
            timeout=self._config.queue_timeout_seconds
        )

        with self._lock:
            self._queue_count -= 1

        if not acquired:
            with self._lock:
                self._total_timeouts += 1
            raise BulkheadTimeoutError(
                f"Bulkhead {self.name}: timed out waiting for slot"
            )

        with self._lock:
            self._active += 1
            self._total_accepted += 1

        try:
            return fn(*args, **kwargs)
        finally:
            self._semaphore.release()
            with self._lock:
                self._active -= 1
                self._total_completed += 1

    def try_execute(self, fn: Callable, *args, **kwargs) -> tuple[bool, Any]:
        acquired = self._semaphore.acquire(blocking=False)
        if not acquired:
            return False, None

        with self._lock:
            self._active += 1
            self._total_accepted += 1

        try:
            result = fn(*args, **kwargs)
            return True, result
        finally:
            self._semaphore.release()
            with self._lock:
                self._active -= 1
                self._total_completed += 1

    def get_metrics(self) -> dict[str, Any]:
        with self._lock:
            return {
                "name": self.name,
                "active": self._active,
                "queued": self._queue_count,
                "max_concurrent": self._config.max_concurrent,
                "max_queue_size": self._config.max_queue_size,
                "total_accepted": self._total_accepted,
                "total_rejected": self._total_rejected,
                "total_completed": self._total_completed,
                "total_timeouts": self._total_timeouts,
                "utilization": self._active / max(1, self._config.max_concurrent),
            }

    @property
    def available_slots(self) -> int:
        with self._lock:
            return self._config.max_concurrent - self._active


class BulkheadFullError(Exception):
    pass


class BulkheadTimeoutError(Exception):
    pass
