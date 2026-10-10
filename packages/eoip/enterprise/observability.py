"""Enterprise observability: metrics collection, performance tracking, and SLI instrumentation.

Wraps enterprise operations with timing, counters, and histogram instrumentation
without requiring external dependencies — falls back to in-process counters
when Prometheus client is unavailable.
"""

from __future__ import annotations

import functools
import threading
import time
from collections import defaultdict
from typing import Any, Callable


class MetricsCollector:
    """In-process metrics collector for enterprise features.

    Thread-safe counters, gauges, and histograms that can be scraped
    by the existing Prometheus endpoint or queried via the health API.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counters: dict[str, int] = defaultdict(int)
        self._gauges: dict[str, float] = defaultdict(float)
        self._histograms: dict[str, list[float]] = defaultdict(list)

    def increment(self, name: str, value: int = 1, **labels: str) -> None:
        key = self._key(name, labels)
        with self._lock:
            self._counters[key] += value

    def gauge_set(self, name: str, value: float, **labels: str) -> None:
        key = self._key(name, labels)
        with self._lock:
            self._gauges[key] = value

    def observe(self, name: str, value: float, **labels: str) -> None:
        key = self._key(name, labels)
        with self._lock:
            hist = self._histograms[key]
            hist.append(value)
            if len(hist) > 10000:
                self._histograms[key] = hist[-5000:]

    def get_counter(self, name: str, **labels: str) -> int:
        key = self._key(name, labels)
        with self._lock:
            return self._counters.get(key, 0)

    def get_gauge(self, name: str, **labels: str) -> float:
        key = self._key(name, labels)
        with self._lock:
            return self._gauges.get(key, 0.0)

    def get_histogram_summary(self, name: str, **labels: str) -> dict[str, float]:
        key = self._key(name, labels)
        with self._lock:
            values = self._histograms.get(key, [])
            if not values:
                return {"count": 0, "min": 0, "max": 0, "avg": 0, "p50": 0, "p95": 0, "p99": 0}
            sorted_vals = sorted(values)
            n = len(sorted_vals)
            return {
                "count": n,
                "min": sorted_vals[0],
                "max": sorted_vals[-1],
                "avg": sum(sorted_vals) / n,
                "p50": sorted_vals[int(n * 0.5)],
                "p95": sorted_vals[min(int(n * 0.95), n - 1)],
                "p99": sorted_vals[min(int(n * 0.99), n - 1)],
            }

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "histograms": {
                    k: {"count": len(v), "sum": sum(v)} for k, v in self._histograms.items()
                },
            }

    def reset(self) -> None:
        with self._lock:
            self._counters.clear()
            self._gauges.clear()
            self._histograms.clear()

    @staticmethod
    def _key(name: str, labels: dict[str, str]) -> str:
        if not labels:
            return name
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"


_metrics = MetricsCollector()


def get_metrics() -> MetricsCollector:
    return _metrics


def timed(metric_name: str, **labels: str) -> Callable:
    """Decorator that records execution time of a function as a histogram observation."""
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            t0 = time.monotonic()
            try:
                result = fn(*args, **kwargs)
                _metrics.increment(f"{metric_name}.success", **labels)
                return result
            except Exception:
                _metrics.increment(f"{metric_name}.error", **labels)
                raise
            finally:
                elapsed_ms = (time.monotonic() - t0) * 1000
                _metrics.observe(f"{metric_name}.duration_ms", elapsed_ms, **labels)
        return wrapper
    return decorator
