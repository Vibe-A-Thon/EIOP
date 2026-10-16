"""MLOps Experiment Tracking Engine (AI-005).

Provides lightweight, production-grade tracking for prompt iterations, model evaluations,
and fine-tuning experiments:
- Experiment: Logical grouping of runs with tags and metadata
- RunTracker: Records parameters, time-series metrics, system tags, and status per run
- ArtifactStore: Stores and retrieves model configs, dataset snapshots, and outputs
- ExperimentComparison: Multi-run analysis with best-run selection and metric deltas
"""

from __future__ import annotations

import copy
import hashlib
import json
import logging
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger("eoip.mlops.tracker")


class RunStatus(str, Enum):
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    KILLED = "KILLED"


@dataclass
class MetricPoint:
    name: str
    value: float
    step: int
    timestamp: float = field(default_factory=time.time)


@dataclass
class Run:
    run_id: str
    experiment_id: str
    run_name: str
    status: RunStatus = RunStatus.STARTING
    parameters: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, list[MetricPoint]] = field(default_factory=dict)
    latest_metrics: dict[str, float] = field(default_factory=dict)
    tags: dict[str, str] = field(default_factory=dict)
    artifact_ids: list[str] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None

    def log_param(self, key: str, value: Any) -> None:
        self.parameters[key] = value

    def log_metric(self, key: str, value: float, step: int = 0) -> None:
        pt = MetricPoint(name=key, value=value, step=step)
        self.metrics.setdefault(key, []).append(pt)
        self.latest_metrics[key] = value

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "experiment_id": self.experiment_id,
            "run_name": self.run_name,
            "status": self.status.value,
            "parameters": self.parameters,
            "latest_metrics": self.latest_metrics,
            "tags": self.tags,
            "artifact_ids": self.artifact_ids,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_sec": round((self.end_time or time.time()) - self.start_time, 2),
        }


@dataclass
class Experiment:
    experiment_id: str
    name: str
    description: str = ""
    tags: dict[str, str] = field(default_factory=dict)
    runs: dict[str, Run] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "total_runs": len(self.runs),
            "created_at": self.created_at,
        }


class ArtifactStore:
    """Manages serialization and retrieval of model evaluation artifacts."""

    def __init__(self) -> None:
        self._artifacts: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()

    def log_artifact(
        self,
        name: str,
        data: Any,
        artifact_type: str = "json",
        run_id: str = "",
    ) -> str:
        with self._lock:
            payload = json.dumps(data, sort_keys=True) if isinstance(data, (dict, list)) else str(data)
            aid = f"art_{hashlib.sha256(payload.encode()).hexdigest()[:12]}"
            self._artifacts[aid] = {
                "artifact_id": aid,
                "name": name,
                "artifact_type": artifact_type,
                "run_id": run_id,
                "content": copy.deepcopy(data),
                "created_at": time.time(),
            }
            return aid

    def get_artifact(self, artifact_id: str) -> dict[str, Any] | None:
        with self._lock:
            art = self._artifacts.get(artifact_id)
            return copy.deepcopy(art) if art else None


class ExperimentComparison:
    """Performs cross-run comparative analysis."""

    @staticmethod
    def compare_runs(runs: list[Run]) -> dict[str, Any]:
        if not runs:
            return {"runs": [], "metric_summary": {}}

        comparison_table = []
        all_metric_keys: set[str] = set()
        for r in runs:
            comparison_table.append(r.to_dict())
            all_metric_keys.update(r.latest_metrics.keys())

        # Compute summary stats across runs
        metric_summary: dict[str, dict[str, float]] = {}
        for m_key in all_metric_keys:
            vals = [r.latest_metrics[m_key] for r in runs if m_key in r.latest_metrics]
            if vals:
                metric_summary[m_key] = {
                    "min": round(min(vals), 4),
                    "max": round(max(vals), 4),
                    "mean": round(sum(vals) / len(vals), 4),
                }

        return {
            "total_runs": len(runs),
            "metric_keys": sorted(all_metric_keys),
            "metric_summary": metric_summary,
            "runs": comparison_table,
        }

    @staticmethod
    def get_best_run(runs: list[Run], target_metric: str, higher_is_better: bool = True) -> Run | None:
        eligible = [r for r in runs if target_metric in r.latest_metrics and r.status == RunStatus.COMPLETED]
        if not eligible:
            eligible = [r for r in runs if target_metric in r.latest_metrics]
        if not eligible:
            return None

        if higher_is_better:
            return max(eligible, key=lambda r: r.latest_metrics[target_metric])
        return min(eligible, key=lambda r: r.latest_metrics[target_metric])


class ExperimentTracker:
    """Centralized MLOps Experiment Tracking Engine."""

    _instance: ExperimentTracker | None = None

    def __init__(self) -> None:
        self.experiments: dict[str, Experiment] = {}
        self.artifact_store = ArtifactStore()
        self._lock = threading.Lock()

    @classmethod
    def get_instance(cls) -> ExperimentTracker:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def create_experiment(self, name: str, description: str = "", tags: dict[str, str] | None = None) -> Experiment:
        with self._lock:
            eid = f"exp_{uuid.uuid4().hex[:8]}"
            exp = Experiment(
                experiment_id=eid,
                name=name,
                description=description,
                tags=tags or {},
            )
            self.experiments[eid] = exp
            return exp

    def get_experiment(self, experiment_id: str) -> Experiment | None:
        with self._lock:
            return self.experiments.get(experiment_id)

    def start_run(
        self,
        experiment_id: str,
        run_name: str = "",
        tags: dict[str, str] | None = None,
    ) -> Run:
        with self._lock:
            exp = self.experiments.get(experiment_id)
            if not exp:
                exp = self.create_experiment(f"Exp_{experiment_id}")

            rid = f"run_{uuid.uuid4().hex[:8]}"
            r_name = run_name or f"run-{len(exp.runs) + 1}"
            run = Run(
                run_id=rid,
                experiment_id=exp.experiment_id,
                run_name=r_name,
                status=RunStatus.RUNNING,
                tags=tags or {},
            )
            exp.runs[rid] = run
            return run

    def end_run(self, experiment_id: str, run_id: str, status: RunStatus = RunStatus.COMPLETED) -> Run | None:
        with self._lock:
            exp = self.experiments.get(experiment_id)
            if not exp or run_id not in exp.runs:
                return None
            run = exp.runs[run_id]
            run.status = status
            run.end_time = time.time()
            return run

    def log_metric(self, experiment_id: str, run_id: str, key: str, value: float, step: int = 0) -> None:
        with self._lock:
            exp = self.experiments.get(experiment_id)
            if exp and run_id in exp.runs:
                exp.runs[run_id].log_metric(key, value, step)

    def log_param(self, experiment_id: str, run_id: str, key: str, value: Any) -> None:
        with self._lock:
            exp = self.experiments.get(experiment_id)
            if exp and run_id in exp.runs:
                exp.runs[run_id].log_param(key, value)

    def log_artifact(
        self,
        experiment_id: str,
        run_id: str,
        name: str,
        data: Any,
        artifact_type: str = "json",
    ) -> str:
        aid = self.artifact_store.log_artifact(name, data, artifact_type=artifact_type, run_id=run_id)
        with self._lock:
            exp = self.experiments.get(experiment_id)
            if exp and run_id in exp.runs:
                exp.runs[run_id].artifact_ids.append(aid)
        return aid

    def compare_experiment_runs(self, experiment_id: str) -> dict[str, Any]:
        with self._lock:
            exp = self.experiments.get(experiment_id)
            if not exp:
                return {"runs": [], "metric_summary": {}}
            return ExperimentComparison.compare_runs(list(exp.runs.values()))

    def get_best_run(self, experiment_id: str, target_metric: str, higher_is_better: bool = True) -> Run | None:
        with self._lock:
            exp = self.experiments.get(experiment_id)
            if not exp:
                return None
            return ExperimentComparison.get_best_run(list(exp.runs.values()), target_metric, higher_is_better)


def get_experiment_tracker() -> ExperimentTracker:
    return ExperimentTracker.get_instance()
