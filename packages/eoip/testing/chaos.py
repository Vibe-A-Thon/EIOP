"""Chaos Testing Framework — inject failures to validate system resilience."""

from __future__ import annotations

import random
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any
from collections.abc import Callable

from eoip.enterprise.logging import get_logger

_log = get_logger("testing.chaos")


class FaultType(str, Enum):
    LATENCY = "LATENCY"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"
    PARTIAL_FAILURE = "PARTIAL_FAILURE"
    DATA_CORRUPTION = "DATA_CORRUPTION"
    CONNECTION_DROP = "CONNECTION_DROP"
    RESOURCE_EXHAUSTION = "RESOURCE_EXHAUSTION"
    CLOCK_SKEW = "CLOCK_SKEW"


class ExperimentStatus(str, Enum):
    DRAFT = "DRAFT"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    ABORTED = "ABORTED"
    FAILED = "FAILED"


@dataclass
class FaultConfig:
    fault_type: FaultType
    target: str
    probability: float = 1.0
    duration_seconds: float = 30.0
    latency_ms: float = 5000.0
    error_message: str = "Chaos fault injected"
    error_code: int = 500
    params: dict[str, Any] = field(default_factory=dict)


@dataclass
class ChaosExperiment:
    experiment_id: str
    name: str
    hypothesis: str
    faults: list[FaultConfig] = field(default_factory=list)
    status: ExperimentStatus = ExperimentStatus.DRAFT
    started_at: str | None = None
    completed_at: str | None = None
    steady_state_before: dict[str, Any] = field(default_factory=dict)
    steady_state_after: dict[str, Any] = field(default_factory=dict)
    observations: list[dict[str, Any]] = field(default_factory=list)
    verdict: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        d["faults"] = [
            {**asdict(f), "fault_type": f.fault_type.value}
            for f in self.faults
        ]
        return d


class FaultInjector:
    """Injects configurable faults into function calls."""

    def __init__(self) -> None:
        self._active_faults: dict[str, FaultConfig] = {}
        self._lock = threading.Lock()
        self._injection_count = 0

    def activate(self, fault: FaultConfig) -> str:
        fault_id = uuid.uuid4().hex[:8]
        with self._lock:
            self._active_faults[fault_id] = fault
        return fault_id

    def deactivate(self, fault_id: str) -> bool:
        with self._lock:
            return self._active_faults.pop(fault_id, None) is not None

    def deactivate_all(self) -> int:
        with self._lock:
            count = len(self._active_faults)
            self._active_faults.clear()
            return count

    def intercept(self, target: str, fn: Callable, *args, **kwargs) -> Any:
        faults = [f for f in self._active_faults.values() if f.target == target]
        for fault in faults:
            if random.random() > fault.probability:
                continue
            self._injection_count += 1

            if fault.fault_type == FaultType.LATENCY:
                time.sleep(fault.latency_ms / 1000.0)
            elif fault.fault_type == FaultType.ERROR:
                raise ChaosError(fault.error_message, fault.error_code)
            elif fault.fault_type == FaultType.TIMEOUT:
                time.sleep(fault.duration_seconds)
                raise TimeoutError(f"Chaos timeout on {target}")
            elif fault.fault_type == FaultType.CONNECTION_DROP:
                raise ConnectionError(f"Chaos connection drop on {target}")
            elif fault.fault_type == FaultType.RESOURCE_EXHAUSTION:
                raise MemoryError(f"Chaos resource exhaustion on {target}")

        return fn(*args, **kwargs)

    @property
    def total_injections(self) -> int:
        return self._injection_count


class ChaosEngine:
    """Orchestrates chaos experiments with steady-state verification."""

    def __init__(self, steady_state_fn: Callable[[], dict[str, Any]] | None = None) -> None:
        self._injector = FaultInjector()
        self._steady_state_fn = steady_state_fn or (lambda: {"status": "ok"})
        self._experiments: dict[str, ChaosExperiment] = {}
        self._lock = threading.Lock()

    @property
    def injector(self) -> FaultInjector:
        return self._injector

    def create_experiment(self, name: str, hypothesis: str,
                          faults: list[dict[str, Any]]) -> ChaosExperiment:
        eid = uuid.uuid4().hex[:12]
        parsed_faults = [
            FaultConfig(
                fault_type=FaultType(f["fault_type"]),
                target=f["target"],
                probability=f.get("probability", 1.0),
                duration_seconds=f.get("duration_seconds", 30.0),
                latency_ms=f.get("latency_ms", 5000.0),
                error_message=f.get("error_message", "Chaos fault injected"),
            )
            for f in faults
        ]
        experiment = ChaosExperiment(
            experiment_id=eid, name=name,
            hypothesis=hypothesis, faults=parsed_faults,
        )
        self._experiments[eid] = experiment
        return experiment

    def run_experiment(self, experiment_id: str) -> ChaosExperiment:
        exp = self._experiments.get(experiment_id)
        if not exp:
            raise ValueError(f"Experiment {experiment_id} not found")

        exp.status = ExperimentStatus.RUNNING
        exp.started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        try:
            exp.steady_state_before = self._steady_state_fn()
        except Exception as e:
            exp.observations.append({"phase": "pre-check", "error": str(e)})

        fault_ids: list[str] = []
        for fault in exp.faults:
            fid = self._injector.activate(fault)
            fault_ids.append(fid)

        time.sleep(0.1)

        for fid in fault_ids:
            self._injector.deactivate(fid)

        try:
            exp.steady_state_after = self._steady_state_fn()
        except Exception as e:
            exp.observations.append({"phase": "post-check", "error": str(e)})

        exp.completed_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        if exp.steady_state_before == exp.steady_state_after:
            exp.verdict = "PASSED"
            exp.observations.append({"result": "System recovered to steady state"})
        else:
            exp.verdict = "HYPOTHESIS_DISPROVED"
            exp.observations.append({
                "result": "Steady state diverged",
                "before": exp.steady_state_before,
                "after": exp.steady_state_after,
            })

        exp.status = ExperimentStatus.COMPLETED
        return exp

    def abort_experiment(self, experiment_id: str) -> bool:
        exp = self._experiments.get(experiment_id)
        if exp and exp.status == ExperimentStatus.RUNNING:
            self._injector.deactivate_all()
            exp.status = ExperimentStatus.ABORTED
            exp.completed_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            return True
        return False

    def get_experiment(self, experiment_id: str) -> ChaosExperiment | None:
        return self._experiments.get(experiment_id)

    def list_experiments(self) -> list[dict[str, Any]]:
        return [e.to_dict() for e in self._experiments.values()]


class ChaosError(Exception):
    def __init__(self, message: str, code: int = 500) -> None:
        super().__init__(message)
        self.code = code
