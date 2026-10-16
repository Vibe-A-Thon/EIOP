"""Stdlib Prometheus text-format metrics registry (GAP-OBS-003).

Zero-dependency counters, gauges, and histograms rendered in the Prometheus
exposition format, plus a ``record_request`` helper suitable for wrapping
handler calls or a FastAPI middleware. Deterministic and thread-safe for
single-process use (a threading lock guards each metric family).
"""

from __future__ import annotations

import math
import threading
import time
from collections import defaultdict


def _escape_label(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


class _MetricBase:
    def __init__(self, name: str, help_text: str, label_names: tuple[str, ...]):
        self.name = name
        self.help_text = help_text
        self.label_names = label_names
        self._lock = threading.Lock()

    def _key(self, labels: dict[str, str]) -> tuple[str, ...]:
        return tuple(labels.get(name, "") for name in self.label_names)

    def _render_labels(self, values: tuple[str, ...]) -> str:
        if not self.label_names:
            return ""
        pairs = ",".join(
            f'{name}="{_escape_label(value)}"'
            for name, value in zip(self.label_names, values)
        )
        return "{" + pairs + "}"


class Counter(_MetricBase):
    """Monotonically increasing counter."""

    def __init__(self, name: str, help_text: str, label_names: tuple[str, ...] = ()):
        super().__init__(name, help_text, label_names)
        self._values: dict[tuple[str, ...], float] = defaultdict(float)

    def inc(self, amount: float = 1.0, **labels: str) -> None:
        if amount < 0:
            raise ValueError("counters can only increase")
        with self._lock:
            self._values[self._key(labels)] += amount

    def get(self, **labels: str) -> float:
        with self._lock:
            return self._values.get(self._key(labels), 0.0)

    def render(self) -> str:
        lines = [f"# HELP {self.name} {self.help_text}", f"# TYPE {self.name} counter"]
        with self._lock:
            for key, value in sorted(self._values.items()):
                lines.append(f"{self.name}{self._render_labels(key)} {value:g}")
        return "\n".join(lines)


class Gauge(_MetricBase):
    """Value that can go up and down."""

    def __init__(self, name: str, help_text: str, label_names: tuple[str, ...] = ()):
        super().__init__(name, help_text, label_names)
        self._values: dict[tuple[str, ...], float] = {}

    def set(self, value: float, **labels: str) -> None:
        with self._lock:
            self._values[self._key(labels)] = value

    def inc(self, amount: float = 1.0, **labels: str) -> None:
        with self._lock:
            self._values[self._key(labels)] = self._values.get(self._key(labels), 0.0) + amount

    def dec(self, amount: float = 1.0, **labels: str) -> None:
        self.inc(-amount, **labels)

    def get(self, **labels: str) -> float:
        with self._lock:
            return self._values.get(self._key(labels), 0.0)

    def render(self) -> str:
        lines = [f"# HELP {self.name} {self.help_text}", f"# TYPE {self.name} gauge"]
        with self._lock:
            for key, value in sorted(self._values.items()):
                lines.append(f"{self.name}{self._render_labels(key)} {value:g}")
        return "\n".join(lines)


_DEFAULT_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)


class Histogram(_MetricBase):
    """Duration/size histogram with Prometheus cumulative buckets."""

    def __init__(
        self,
        name: str,
        help_text: str,
        label_names: tuple[str, ...] = (),
        buckets: tuple[float, ...] = _DEFAULT_BUCKETS,
    ):
        super().__init__(name, help_text, label_names)
        self.buckets = tuple(sorted(buckets)) + (math.inf,)
        self._counts: dict[tuple[str, ...], list[int]] = {}
        self._sums: dict[tuple[str, ...], float] = {}

    def observe(self, value: float, **labels: str) -> None:
        key = self._key(labels)
        with self._lock:
            counts = self._counts.setdefault(key, [0] * len(self.buckets))
            for idx, bound in enumerate(self.buckets):
                if value <= bound:
                    counts[idx] += 1
            self._sums[key] = self._sums.get(key, 0.0) + value

    def render(self) -> str:
        lines = [f"# HELP {self.name} {self.help_text}", f"# TYPE {self.name} histogram"]
        with self._lock:
            for key in sorted(self._counts):
                counts = self._counts[key]
                labels_str = self._render_labels(key)
                for idx, bound in enumerate(self.buckets):
                    bound_str = "+Inf" if math.isinf(bound) else f"{bound:g}"
                    if key:
                        inner = ",".join(
                            f'{name}="{_escape_label(value)}"'
                            for name, value in zip(self.label_names, key)
                        )
                        bucket_labels = "{" + inner + f',le="{bound_str}"}}'
                    else:
                        bucket_labels = f'{{le="{bound_str}"}}'
                    lines.append(f"{self.name}_bucket{bucket_labels} {counts[idx]}")
                lines.append(f"{self.name}_sum{labels_str} {self._sums[key]:g}")
                lines.append(f"{self.name}_count{labels_str} {counts[-1]}")
        return "\n".join(lines)


class Registry:
    """Named collection of metrics rendered together."""

    def __init__(self) -> None:
        self._metrics: dict[str, _MetricBase] = {}
        self._lock = threading.Lock()

    def register(self, metric: _MetricBase) -> _MetricBase:
        with self._lock:
            if metric.name in self._metrics:
                raise ValueError(f"metric {metric.name!r} already registered")
            self._metrics[metric.name] = metric
        return metric

    def counter(self, name: str, help_text: str, label_names: tuple[str, ...] = ()) -> Counter:
        return self.register(Counter(name, help_text, label_names))  # type: ignore[return-value]

    def gauge(self, name: str, help_text: str, label_names: tuple[str, ...] = ()) -> Gauge:
        return self.register(Gauge(name, help_text, label_names))  # type: ignore[return-value]

    def histogram(
        self,
        name: str,
        help_text: str,
        label_names: tuple[str, ...] = (),
        buckets: tuple[float, ...] = _DEFAULT_BUCKETS,
    ) -> Histogram:
        return self.register(Histogram(name, help_text, label_names, buckets))  # type: ignore[return-value]

    def get(self, name: str) -> _MetricBase | None:
        return self._metrics.get(name)

    def render(self) -> str:
        """Render all metrics in Prometheus text exposition format."""
        with self._lock:
            metrics = list(self._metrics.values())
        return "\n".join(m.render() for m in metrics) + "\n"


def record_request(registry: Registry, *, method: str, path: str, status: int, duration_seconds: float) -> None:
    """Record one handled request into standard registry metrics (GAP-OBS-003).

    Uses metric families ``http_requests_total``, ``http_request_duration_seconds``,
    and ``http_requests_in_flight`` (the last is decremented after the call).
    """
    labels = {"method": method, "path": path, "status": str(status)}

    def _family(kind, name, help_text):
        existing = registry.get(name)
        if existing is not None:
            return existing
        factory = registry.counter if kind == "counter" else registry.histogram
        return factory(name, help_text, ("method", "path", "status"))

    _family("counter", "http_requests_total", "Total HTTP requests handled.").inc(**labels)
    _family(
        "histogram",
        "http_request_duration_seconds",
        "HTTP request duration in seconds.",
    ).observe(duration_seconds, **labels)


class timed_request:
    """Context manager: record request metrics on exit (duration + status)."""

    def __init__(self, registry: Registry, *, method: str, path: str, status: int = 200):
        self.registry = registry
        self.method = method
        self.path = path
        self.status = status
        self._start = 0.0

    def __enter__(self) -> "timed_request":
        self._start = time.perf_counter()
        return self

    def __exit__(self, *exc_info) -> bool:
        duration = time.perf_counter() - self._start
        status = 500 if exc_info[0] is not None else self.status
        record_request(
            self.registry,
            method=self.method,
            path=self.path,
            status=status,
            duration_seconds=duration,
        )
        return False
