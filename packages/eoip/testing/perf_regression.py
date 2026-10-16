"""Performance Regression Detection Framework (TEST-004).

Enforces automated performance budgets in CI:
- Compares latency (p50, p90, p99), throughput (RPS), and memory footprint against baselines
- Configurable degradation thresholds per metric
- Generates Markdown diff report for PR comments and CI pipeline status
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("eoip.testing.perf_regression")


@dataclass
class BenchmarkMetric:
    metric_name: str
    current_value: float
    baseline_value: float
    unit: str = "ms"
    lower_is_better: bool = True

    @property
    def delta(self) -> float:
        return self.current_value - self.baseline_value

    @property
    def percentage_change(self) -> float:
        if self.baseline_value == 0:
            return 0.0
        return ((self.current_value - self.baseline_value) / self.baseline_value) * 100.0


@dataclass
class RegressionThresholds:
    max_latency_regression_pct: float = 15.0  # Allow up to 15% latency increase
    max_throughput_drop_pct: float = 10.0      # Allow up to 10% RPS decrease
    max_memory_regression_pct: float = 20.0    # Allow up to 20% memory increase


@dataclass
class PerformanceComparisonReport:
    passed: bool
    total_metrics: int
    regressed_metrics: list[str]
    metrics: list[BenchmarkMetric] = field(default_factory=list)
    evaluated_at: float = field(default_factory=time.time)

    def to_markdown(self) -> str:
        status_badge = "✅ **PERFORMANCE GATES PASSED**" if self.passed else "❌ **PERFORMANCE REGRESSION DETECTED**"
        lines = [
            f"### {status_badge}",
            "",
            "| Metric | Baseline | Current | Delta | Change (%) | Status |",
            "|---|---|---|---|---|---|",
        ]
        for m in self.metrics:
            is_regressed = m.metric_name in self.regressed_metrics
            status_str = "⚠️ Regressed" if is_regressed else "✅ OK"
            sign = "+" if m.percentage_change > 0 else ""
            lines.append(
                f"| `{m.metric_name}` | {m.baseline_value:.2f} {m.unit} | {m.current_value:.2f} {m.unit} | "
                f"{m.delta:+.2f} {m.unit} | {sign}{m.percentage_change:.1f}% | {status_str} |"
            )
        lines.append("")
        if self.regressed_metrics:
            lines.append(f"> **Warning**: Regressions detected in: {', '.join(self.regressed_metrics)}")
        return "\n".join(lines)


class PerformanceRegressionDetector:
    """Automated benchmark comparison and regression detector."""

    def __init__(self, thresholds: RegressionThresholds | None = None) -> None:
        self.thresholds = thresholds or RegressionThresholds()

    def compare(
        self,
        current_metrics: dict[str, float],
        baseline_metrics: dict[str, float],
    ) -> PerformanceComparisonReport:
        metrics_list: list[BenchmarkMetric] = []
        regressed: list[str] = []

        for name, curr_val in current_metrics.items():
            base_val = baseline_metrics.get(name, curr_val)
            # Determine metric characteristics
            is_throughput = "rps" in name.lower() or "throughput" in name.lower()
            unit = "req/s" if is_throughput else "ms"
            lower_is_better = not is_throughput

            metric = BenchmarkMetric(
                metric_name=name,
                current_value=curr_val,
                baseline_value=base_val,
                unit=unit,
                lower_is_better=lower_is_better,
            )
            metrics_list.append(metric)

            # Check threshold violation
            if is_throughput:
                # Throughput drop is bad
                if metric.percentage_change < -self.thresholds.max_throughput_drop_pct:
                    regressed.append(name)
            else:
                # Latency increase is bad
                if metric.percentage_change > self.thresholds.max_latency_regression_pct:
                    regressed.append(name)

        passed = len(regressed) == 0
        return PerformanceComparisonReport(
            passed=passed,
            total_metrics=len(metrics_list),
            regressed_metrics=regressed,
            metrics=metrics_list,
        )

    def load_baseline(self, filepath: str | Path) -> dict[str, float]:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("metrics", data)

    def save_baseline(self, filepath: str | Path, metrics: dict[str, float]) -> None:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"timestamp": time.time(), "metrics": metrics}, f, indent=2)
