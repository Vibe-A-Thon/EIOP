"""Predictive Graph Analytics — trend detection, anomaly prediction, and growth forecasting."""

from __future__ import annotations

import math
import statistics
import threading
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class TrendDirection(str, Enum):
    RISING = "RISING"
    FALLING = "FALLING"
    STABLE = "STABLE"
    VOLATILE = "VOLATILE"


class AnomalyType(str, Enum):
    SPIKE = "SPIKE"
    DROP = "DROP"
    DRIFT = "DRIFT"
    PATTERN_BREAK = "PATTERN_BREAK"
    OUTLIER = "OUTLIER"


class ForecastMethod(str, Enum):
    LINEAR = "LINEAR"
    EXPONENTIAL_SMOOTHING = "EXPONENTIAL_SMOOTHING"
    MOVING_AVERAGE = "MOVING_AVERAGE"


@dataclass
class TimeSeriesPoint:
    timestamp: str
    value: float
    label: str = ""


@dataclass
class TrendAnalysis:
    metric: str
    direction: TrendDirection
    slope: float
    r_squared: float
    data_points: int
    forecast_next: float
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["direction"] = self.direction.value
        return d


@dataclass
class Anomaly:
    anomaly_id: str
    metric: str
    anomaly_type: AnomalyType
    value: float
    expected_value: float
    deviation: float
    timestamp: str
    severity: float

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["anomaly_type"] = self.anomaly_type.value
        return d


@dataclass
class Forecast:
    metric: str
    method: ForecastMethod
    horizon_points: int
    predictions: list[dict[str, Any]] = field(default_factory=list)
    confidence_lower: list[float] = field(default_factory=list)
    confidence_upper: list[float] = field(default_factory=list)
    mape: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["method"] = self.method.value
        return d


@dataclass
class GrowthReport:
    metric: str
    current_value: float
    growth_rate: float
    projected_value_30d: float
    projected_value_90d: float
    capacity_threshold: float | None = None
    days_to_threshold: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class PredictiveAnalyticsEngine:
    """Detects trends, anomalies, and forecasts graph metrics."""

    def __init__(self) -> None:
        self._series: dict[str, list[TimeSeriesPoint]] = defaultdict(list)
        self._anomalies: list[Anomaly] = []
        self._lock = threading.Lock()
        self._max_series_length = 10000

    def record(self, metric: str, value: float,
               timestamp: str | None = None) -> None:
        ts = timestamp or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        with self._lock:
            series = self._series[metric]
            series.append(TimeSeriesPoint(timestamp=ts, value=value, label=metric))
            if len(series) > self._max_series_length:
                self._series[metric] = series[-self._max_series_length:]

    def analyze_trend(self, metric: str, window: int | None = None) -> TrendAnalysis:
        series = self._series.get(metric, [])
        if not series:
            return TrendAnalysis(
                metric=metric, direction=TrendDirection.STABLE,
                slope=0.0, r_squared=0.0, data_points=0,
                forecast_next=0.0, confidence=0.0,
            )

        values = [p.value for p in series]
        if window:
            values = values[-window:]
        n = len(values)

        if n < 2:
            return TrendAnalysis(
                metric=metric, direction=TrendDirection.STABLE,
                slope=0.0, r_squared=0.0, data_points=n,
                forecast_next=values[0] if values else 0.0, confidence=0.0,
            )

        xs = list(range(n))
        slope, intercept = self._linear_regression(xs, values)
        r_sq = self._r_squared(xs, values, slope, intercept)
        forecast = slope * n + intercept

        cv = statistics.stdev(values) / max(abs(statistics.mean(values)), 1e-9) if n > 1 else 0
        if cv > 0.5:
            direction = TrendDirection.VOLATILE
        elif slope > 0.01 * abs(statistics.mean(values)):
            direction = TrendDirection.RISING
        elif slope < -0.01 * abs(statistics.mean(values)):
            direction = TrendDirection.FALLING
        else:
            direction = TrendDirection.STABLE

        return TrendAnalysis(
            metric=metric, direction=direction,
            slope=round(slope, 6), r_squared=round(r_sq, 4),
            data_points=n, forecast_next=round(forecast, 4),
            confidence=round(min(r_sq, 1.0), 2),
        )

    def detect_anomalies(self, metric: str, z_threshold: float = 2.5) -> list[Anomaly]:
        series = self._series.get(metric, [])
        if len(series) < 5:
            return []

        values = [p.value for p in series]
        mean = statistics.mean(values)
        std = statistics.stdev(values) if len(values) > 1 else 0

        if std < 1e-9:
            return []

        anomalies: list[Anomaly] = []
        for i, point in enumerate(series):
            z_score = (point.value - mean) / std
            if abs(z_score) >= z_threshold:
                atype = AnomalyType.SPIKE if z_score > 0 else AnomalyType.DROP
                anomaly = Anomaly(
                    anomaly_id=f"{metric}-{i}",
                    metric=metric, anomaly_type=atype,
                    value=point.value, expected_value=round(mean, 4),
                    deviation=round(z_score, 4),
                    timestamp=point.timestamp,
                    severity=round(min(abs(z_score) / 5.0, 1.0), 2),
                )
                anomalies.append(anomaly)
                self._anomalies.append(anomaly)

        return anomalies

    def forecast(self, metric: str, horizon: int = 10,
                 method: ForecastMethod = ForecastMethod.LINEAR) -> Forecast:
        series = self._series.get(metric, [])
        values = [p.value for p in series]

        if len(values) < 3:
            return Forecast(
                metric=metric, method=method, horizon_points=horizon,
            )

        if method == ForecastMethod.LINEAR:
            predictions, lower, upper = self._forecast_linear(values, horizon)
        elif method == ForecastMethod.EXPONENTIAL_SMOOTHING:
            predictions, lower, upper = self._forecast_ema(values, horizon)
        else:
            predictions, lower, upper = self._forecast_ma(values, horizon)

        mape = self._compute_mape(values)

        return Forecast(
            metric=metric, method=method, horizon_points=horizon,
            predictions=[{"step": i + 1, "value": round(v, 4)} for i, v in enumerate(predictions)],
            confidence_lower=[round(v, 4) for v in lower],
            confidence_upper=[round(v, 4) for v in upper],
            mape=round(mape, 4),
        )

    def growth_report(self, metric: str,
                      capacity_threshold: float | None = None) -> GrowthReport:
        series = self._series.get(metric, [])
        values = [p.value for p in series]

        if len(values) < 2:
            return GrowthReport(
                metric=metric, current_value=values[-1] if values else 0,
                growth_rate=0.0, projected_value_30d=0.0, projected_value_90d=0.0,
            )

        current = values[-1]
        half = max(1, len(values) // 2)
        recent_avg = statistics.mean(values[-half:])
        older_avg = statistics.mean(values[:half])
        growth_rate = (recent_avg - older_avg) / max(abs(older_avg), 1e-9)

        trend = self.analyze_trend(metric)
        proj_30 = current + trend.slope * 30
        proj_90 = current + trend.slope * 90

        days_to_thresh = None
        if capacity_threshold and trend.slope > 0:
            remaining = capacity_threshold - current
            days_to_thresh = max(0, int(remaining / trend.slope)) if trend.slope > 0 else None

        return GrowthReport(
            metric=metric, current_value=round(current, 4),
            growth_rate=round(growth_rate, 4),
            projected_value_30d=round(proj_30, 4),
            projected_value_90d=round(proj_90, 4),
            capacity_threshold=capacity_threshold,
            days_to_threshold=days_to_thresh,
        )

    def get_metrics(self) -> dict[str, Any]:
        return {
            "tracked_metrics": len(self._series),
            "total_data_points": sum(len(s) for s in self._series.values()),
            "total_anomalies_detected": len(self._anomalies),
            "metrics": list(self._series.keys()),
        }

    def get_recent_anomalies(self, limit: int = 20) -> list[dict[str, Any]]:
        return [a.to_dict() for a in self._anomalies[-limit:]]

    def _linear_regression(self, xs: list[float], ys: list[float]) -> tuple[float, float]:
        n = len(xs)
        x_mean = sum(xs) / n
        y_mean = sum(ys) / n
        ss_xy = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
        ss_xx = sum((x - x_mean) ** 2 for x in xs)
        slope = ss_xy / max(ss_xx, 1e-9)
        intercept = y_mean - slope * x_mean
        return slope, intercept

    def _r_squared(self, xs: list[float], ys: list[float],
                   slope: float, intercept: float) -> float:
        y_mean = sum(ys) / len(ys)
        ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
        ss_tot = sum((y - y_mean) ** 2 for y in ys)
        if ss_tot < 1e-9:
            return 1.0
        return max(0.0, 1.0 - ss_res / ss_tot)

    def _forecast_linear(self, values: list[float],
                         horizon: int) -> tuple[list[float], list[float], list[float]]:
        n = len(values)
        xs = list(range(n))
        slope, intercept = self._linear_regression(xs, values)
        std = statistics.stdev(values) if n > 1 else 0
        preds = [slope * (n + i) + intercept for i in range(horizon)]
        lower = [p - 1.96 * std for p in preds]
        upper = [p + 1.96 * std for p in preds]
        return preds, lower, upper

    def _forecast_ema(self, values: list[float],
                      horizon: int, alpha: float = 0.3) -> tuple[list[float], list[float], list[float]]:
        ema = values[0]
        for v in values[1:]:
            ema = alpha * v + (1 - alpha) * ema
        std = statistics.stdev(values) if len(values) > 1 else 0
        preds = [ema] * horizon
        lower = [ema - 1.96 * std] * horizon
        upper = [ema + 1.96 * std] * horizon
        return preds, lower, upper

    def _forecast_ma(self, values: list[float],
                     horizon: int, window: int = 5) -> tuple[list[float], list[float], list[float]]:
        recent = values[-window:]
        ma = statistics.mean(recent)
        std = statistics.stdev(recent) if len(recent) > 1 else 0
        preds = [ma] * horizon
        lower = [ma - 1.96 * std] * horizon
        upper = [ma + 1.96 * std] * horizon
        return preds, lower, upper

    def _compute_mape(self, values: list[float], lookback: int = 5) -> float:
        if len(values) < lookback + 1:
            return 0.0
        errors = []
        for i in range(lookback, len(values)):
            actual = values[i]
            predicted = statistics.mean(values[i - lookback:i])
            if abs(actual) > 1e-9:
                errors.append(abs((actual - predicted) / actual))
        return statistics.mean(errors) if errors else 0.0
