"""Unit Tests for Performance Regression Detection Framework (TEST-004)."""

import json
from pathlib import Path
import pytest

from eoip.testing.perf_regression import (
    PerformanceRegressionDetector,
    RegressionThresholds,
)


@pytest.mark.req("TEST-004")
class TestPerfRegressionDetector:
    def test_pass_within_thresholds(self):
        detector = PerformanceRegressionDetector(
            thresholds=RegressionThresholds(max_latency_regression_pct=15.0, max_throughput_drop_pct=10.0)
        )
        baseline = {"query_p95": 100.0, "query_rps": 500.0}
        current = {"query_p95": 108.0, "query_rps": 490.0}  # +8% latency, -2% rps

        report = detector.compare(current, baseline)
        assert report.passed is True
        assert len(report.regressed_metrics) == 0

        md = report.to_markdown()
        assert "PERFORMANCE GATES PASSED" in md
        assert "`query_p95`" in md
        assert "`query_rps`" in md

    def test_detect_latency_regression(self):
        detector = PerformanceRegressionDetector(
            thresholds=RegressionThresholds(max_latency_regression_pct=15.0)
        )
        baseline = {"graph_traversal_p99": 50.0}
        current = {"graph_traversal_p99": 75.0}  # +50% regression

        report = detector.compare(current, baseline)
        assert report.passed is False
        assert "graph_traversal_p99" in report.regressed_metrics

        md = report.to_markdown()
        assert "PERFORMANCE REGRESSION DETECTED" in md
        assert "Regressed" in md

    def test_detect_throughput_drop(self):
        detector = PerformanceRegressionDetector(
            thresholds=RegressionThresholds(max_throughput_drop_pct=10.0)
        )
        baseline = {"ingestion_rps": 1000.0}
        current = {"ingestion_rps": 800.0}  # -20% drop

        report = detector.compare(current, baseline)
        assert report.passed is False
        assert "ingestion_rps" in report.regressed_metrics

    def test_baseline_save_and_load(self, tmp_path: Path):
        detector = PerformanceRegressionDetector()
        metrics = {"p50": 12.5, "p99": 45.0, "rps": 120.0}
        file_path = tmp_path / "perf_baseline.json"

        detector.save_baseline(file_path, metrics)
        assert file_path.exists()

        loaded = detector.load_baseline(file_path)
        assert loaded == metrics
