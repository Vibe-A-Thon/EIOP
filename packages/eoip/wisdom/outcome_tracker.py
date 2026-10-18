"""Outcome tracking, variance analysis, and calibration for Wisdom Graph (WG-WP-11..14)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional
from eoip.wisdom.decision_trace import DecisionOutcome, DecisionTrace


@dataclass
class CalibrationMetric:
    decided_by: str
    total_decisions_evaluated: int
    mean_absolute_error: float
    brier_score: float
    tendency: str  # OVERESTIMATING, UNDERESTIMATING, WELL_CALIBRATED


class OutcomeTracker:
    """Tracks longitudinal decision outcomes and calculates calibration."""

    def __init__(self) -> None:
        self._history: Dict[str, DecisionTrace] = {}

    def track(self, trace: DecisionTrace) -> None:
        self._history[trace.trace_id] = trace

    def record_outcome(
        self,
        trace_id: str,
        actual_metrics: Dict[str, float],
        lessons_learned: str,
        evaluated_by: str,
    ) -> DecisionOutcome:
        trace = self._history.get(trace_id)
        if not trace:
            raise KeyError(f"DecisionTrace '{trace_id}' not found in outcome tracker")

        # Find projected impact for selected option
        projected = {}
        for opt in trace.options:
            if opt.option_id == trace.selected_option_id:
                projected = opt.projected_impact
                break

        # Calculate variance = actual - projected
        variance = {}
        for metric, actual_val in actual_metrics.items():
            proj_val = projected.get(metric, 0.0)
            variance[metric] = round(actual_val - proj_val, 4)

        outcome = DecisionOutcome(
            outcome_id=f"out-{trace_id}-{len(trace.outcomes)+1}",
            observed_at=datetime.now(timezone.utc),
            actual_metrics=actual_metrics,
            lessons_learned=lessons_learned,
            evaluated_by=evaluated_by,
            variance_analysis=variance,
        )

        trace.outcomes.append(outcome)
        trace.status = "OUTCOME_EVALUATED"
        return outcome

    def compute_person_calibration(self, decided_by: str) -> CalibrationMetric:
        user_traces = [t for t in self._history.values() if t.decided_by == decided_by and t.outcomes]
        if not user_traces:
            return CalibrationMetric(
                decided_by=decided_by,
                total_decisions_evaluated=0,
                mean_absolute_error=0.0,
                brier_score=0.0,
                tendency="WELL_CALIBRATED",
            )

        errors = []
        for t in user_traces:
            for outcome in t.outcomes:
                for metric, diff in outcome.variance_analysis.items():
                    errors.append(diff)

        if not errors:
            mae = 0.0
            tendency = "WELL_CALIBRATED"
        else:
            mae = sum(abs(e) for e in errors) / len(errors)
            mean_signed = sum(errors) / len(errors)
            if mean_signed > 0.1:
                tendency = "UNDERESTIMATING"  # outcomes were higher than projected
            elif mean_signed < -0.1:
                tendency = "OVERESTIMATING"  # outcomes were lower than projected
            else:
                tendency = "WELL_CALIBRATED"

        return CalibrationMetric(
            decided_by=decided_by,
            total_decisions_evaluated=len(user_traces),
            mean_absolute_error=round(mae, 4),
            brier_score=round(mae ** 2, 4),
            tendency=tendency,
        )
