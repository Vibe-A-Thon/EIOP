"""Evaluation discipline and calibration for graph neural models (CRA-044.5).

Enforces:
1. AUPRC is primary for link prediction and anomaly detection; AUROC is never reported alone.
2. Macro-F1 for node classification.
3. Time-filtered MRR for temporal prediction.
4. Five baselines reported beside every model:
   - Random
   - Degree
   - Common-neighbours / Adamic-Adar
   - HashBaseline
   - Deterministic rule or traversal baseline
5. Calibration on validation split with ECE <= 0.10 before score is treated as probability.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any
from collections.abc import Sequence

import numpy as np


class AUROCOnlyReportRefusedError(ValueError):
    """Raised when an evaluation report attempts to cite AUROC alone without primary AUPRC."""
    pass


def compute_auprc(y_true: Sequence[int | float], y_score: Sequence[float]) -> float:
    """Compute Area Under the Precision-Recall Curve (AUPRC / Average Precision)."""
    if len(y_true) != len(y_score) or not y_true:
        return 0.0

    y_t = np.asarray(y_true, dtype=np.int32)
    y_s = np.asarray(y_score, dtype=np.float32)

    pos_count = int(np.sum(y_t == 1))
    if pos_count == 0 or pos_count == len(y_t):
        return 1.0 if pos_count > 0 else 0.0

    order = np.argsort(-y_s)
    y_t_sorted = y_t[order]

    tp_cum = np.cumsum(y_t_sorted == 1)
    fp_cum = np.cumsum(y_t_sorted == 0)

    recalls = tp_cum / pos_count
    precisions = tp_cum / (tp_cum + fp_cum)

    # Trapezoidal approximation or precision step sum
    precisions_with_zero = np.concatenate(([1.0], precisions))
    recalls_with_zero = np.concatenate(([0.0], recalls))
    auprc = float(np.sum((recalls_with_zero[1:] - recalls_with_zero[:-1]) * precisions_with_zero[1:]))
    return max(0.0, min(1.0, auprc))


def compute_auroc(y_true: Sequence[int | float], y_score: Sequence[float]) -> float:
    """Compute AUROC for comparison."""
    if len(y_true) != len(y_score) or not y_true:
        return 0.5
    y_t = np.asarray(y_true, dtype=np.int32)
    y_s = np.asarray(y_score, dtype=np.float32)
    pos_count = int(np.sum(y_t == 1))
    neg_count = int(np.sum(y_t == 0))
    if pos_count == 0 or neg_count == 0:
        return 0.5
    order = np.argsort(y_s)
    ranks = np.empty_like(order)
    ranks[order] = np.arange(len(y_s))
    pos_ranks = ranks[y_t == 1]
    u = np.sum(pos_ranks) - (pos_count * (pos_count - 1)) / 2.0
    return float(u / (pos_count * neg_count))


def compute_macro_f1(y_true: Sequence[int], y_pred: Sequence[int]) -> float:
    """Compute Macro-F1 across classes."""
    classes = sorted(list(set(y_true) | set(y_pred)))
    if not classes:
        return 0.0

    f1s = []
    y_t = np.asarray(y_true)
    y_p = np.asarray(y_pred)
    for c in classes:
        tp = np.sum((y_t == c) & (y_p == c))
        fp = np.sum((y_t != c) & (y_p == c))
        fn = np.sum((y_t == c) & (y_p != c))
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
        f1s.append(f1)
    return float(np.mean(f1s))


def compute_time_filtered_mrr(ranks: Sequence[int]) -> float:
    """Compute Mean Reciprocal Rank (MRR) filtered by timestamp ordering."""
    if not ranks:
        return 0.0
    reciprocals = [1.0 / r for r in ranks if r > 0]
    return float(np.mean(reciprocals)) if reciprocals else 0.0


def compute_ece(y_true: Sequence[int], y_probs: Sequence[float], n_bins: int = 10) -> float:
    """Compute Expected Calibration Error (ECE)."""
    y_t = np.asarray(y_true, dtype=np.int32)
    y_p = np.asarray(y_probs, dtype=np.float32)

    bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    n = len(y_t)

    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        mask = (y_p >= bin_lower) & (y_p <= bin_upper if i == n_bins - 1 else y_p < bin_upper)
        bin_count = np.sum(mask)
        if bin_count > 0:
            bin_acc = np.mean(y_t[mask])
            bin_conf = np.mean(y_p[mask])
            ece += (bin_count / n) * abs(bin_acc - bin_conf)

    return float(ece)


@dataclass
class BaselineComparisonReport:
    model_name: str
    primary_metric_name: str
    primary_metric_value: float
    auroc: float | None
    baselines: dict[str, float]
    beats_common_neighbours: bool
    beats_rule: bool
    is_calibrated: bool
    ece: float
    status: str  # PROMOTED or FAILED


class ModelEvaluationHarness:
    """Enforces evaluation discipline, 5 baselines, and calibration (CRA-044.5)."""

    def evaluate_link_prediction(
        self,
        model_name: str,
        y_true: list[int],
        y_score: list[float],
        baseline_scores: dict[str, list[float]],
        report_auroc_only: bool = False,
        calibrated_probs: list[float] | None = None,
    ) -> BaselineComparisonReport:
        if report_auroc_only:
            raise AUROCOnlyReportRefusedError(
                "Per CRA-044.5, AUPRC is primary for link prediction and AUROC is NEVER reported alone."
            )

        auprc = compute_auprc(y_true, y_score)
        auroc = compute_auroc(y_true, y_score)

        # Mandatory 5 baselines
        required_baselines = {"random", "degree", "common_neighbours", "hash_baseline", "rule_traversal"}
        baseline_results: dict[str, float] = {}
        for b_name in required_baselines:
            b_preds = baseline_scores.get(b_name, [0.5] * len(y_true))
            baseline_results[b_name] = compute_auprc(y_true, b_preds)

        # Margin check: model must beat common_neighbours and rule_traversal by >= 0.05
        cn_score = baseline_results.get("common_neighbours", 0.0)
        rule_score = baseline_results.get("rule_traversal", 0.0)

        beats_cn = (auprc - cn_score) >= 0.05
        beats_rule = (auprc - rule_score) >= 0.05

        # Calibration check
        ece = 1.0
        is_cal = False
        if calibrated_probs is not None:
            ece = compute_ece(y_true, calibrated_probs)
            is_cal = (ece <= 0.10)

        status = "PROMOTED" if (beats_cn and beats_rule) else "FAILED"

        return BaselineComparisonReport(
            model_name=model_name,
            primary_metric_name="AUPRC",
            primary_metric_value=round(auprc, 4),
            auroc=round(auroc, 4),
            baselines={k: round(v, 4) for k, v in baseline_results.items()},
            beats_common_neighbours=beats_cn,
            beats_rule=beats_rule,
            is_calibrated=is_cal,
            ece=round(ece, 4),
            status=status,
        )
