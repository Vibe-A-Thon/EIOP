"""
External Tamper-Proof Evaluators (GRF-EVAL-*, T-GRF-004).
Implements Calibration Judge (ECE, Brier Score) and Regression Sentinel.
Runs out-of-process to evaluate Graffin without self-referential bias.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Sequence, Tuple


@dataclass
class CalibrationReport:
    expected_calibration_error: float
    brier_score: float
    bin_count: int
    sample_count: int
    is_calibrated: bool


class CalibrationJudge:
    """
    Computes statistical calibration metrics over agent probability predictions:
    - Expected Calibration Error (ECE)
    - Brier Score
    Threshold: ECE <= 0.15 is considered well-calibrated for operational batches.
    """

    def __init__(self, num_bins: int = 10, max_acceptable_ece: float = 0.15) -> None:
        self.num_bins = num_bins
        self.max_acceptable_ece = max_acceptable_ece

    def evaluate(self, predictions: Sequence[Tuple[float, int]]) -> CalibrationReport:
        """
        predictions: Sequence of (predicted_prob, ground_truth_binary: 0 or 1)
        """
        if not predictions:
            return CalibrationReport(
                expected_calibration_error=0.0,
                brier_score=0.0,
                bin_count=self.num_bins,
                sample_count=0,
                is_calibrated=True,
            )

        n = len(predictions)
        # Compute Brier score: mean((prob - actual)^2)
        brier = sum((p - y) ** 2 for p, y in predictions) / n

        # Compute Expected Calibration Error across bins
        bin_size = 1.0 / self.num_bins
        bins: List[List[Tuple[float, int]]] = [[] for _ in range(self.num_bins)]

        for p, y in predictions:
            bin_idx = min(int(p / bin_size), self.num_bins - 1)
            bins[bin_idx].append((p, y))

        ece = 0.0
        for b in bins:
            if not b:
                continue
            bin_len = len(b)
            avg_conf = sum(p for p, _ in b) / bin_len
            avg_acc = sum(y for _, y in b) / bin_len
            ece += (bin_len / n) * abs(avg_acc - avg_conf)

        return CalibrationReport(
            expected_calibration_error=ece,
            brier_score=brier,
            bin_count=self.num_bins,
            sample_count=n,
            is_calibrated=ece <= self.max_acceptable_ece,
        )


@dataclass
class RegressionReport:
    baseline_metric: float
    current_metric: float
    delta: float
    has_regression: bool
    details: str


class RegressionSentinel:
    """
    Monitors agent outputs against established empirical baselines
    to detect silent accuracy or performance regressions.
    """

    def __init__(self, regression_threshold: float = 0.05) -> None:
        self.regression_threshold = regression_threshold

    def check_regression(
        self,
        baseline_score: float,
        current_score: float,
        higher_is_better: bool = True,
    ) -> RegressionReport:
        delta = current_score - baseline_score
        if higher_is_better:
            has_regression = delta < -self.regression_threshold
        else:
            has_regression = delta > self.regression_threshold

        details = (
            f"Regression detected: baseline={baseline_score:.4f}, current={current_score:.4f}, delta={delta:.4f}"
            if has_regression else "Performance within acceptable bounds."
        )

        return RegressionReport(
            baseline_metric=baseline_score,
            current_metric=current_score,
            delta=delta,
            has_regression=has_regression,
            details=details,
        )
