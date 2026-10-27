"""Scale, performance, and correctness qualification harness (WP-036 / CRA-036.1-036.10, CRA-036.A)."""

from __future__ import annotations

import copy
import hashlib
import json
import logging
import math
import os
import platform
import statistics
import sys
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any
from collections.abc import Callable

logger = logging.getLogger("eoip.qualification.harness")


class ScaleTier(str, Enum):
    P0 = "P0"  # Development / unit validation scale
    P1 = "P1"  # Production enterprise scale (10M - 50M triples)
    P2 = "P2"  # 500M-triple qualification target (Decision X-09)


@dataclass
class StorageAccounting:
    asserted_triples: int = 0
    inferred_triples: int = 0
    raw_payload_bytes: int = 0
    index_bytes: int = 0
    vector_bytes: int = 0
    history_journal_bytes: int = 0
    replicas_count: int = 1
    hot_residency_bytes: int = 0
    cold_residency_bytes: int = 0

    @property
    def total_triples(self) -> int:
        return self.asserted_triples + self.inferred_triples

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TrialLatencyStats:
    p50_ms: float
    p95_ms: float
    p99_ms: float
    min_ms: float
    max_ms: float
    mean_ms: float
    variance_ms: float
    throughput_ops_sec: float


def compute_latencies(timings_ms: list[float]) -> TrialLatencyStats:
    if not timings_ms:
        return TrialLatencyStats(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    sorted_times = sorted(timings_ms)
    n = len(sorted_times)

    def pct(p: float) -> float:
        rank = max(0, min(n - 1, math.ceil((p / 100.0) * n) - 1))
        return sorted_times[rank]

    total_time_sec = sum(sorted_times) / 1000.0
    throughput = (n / total_time_sec) if total_time_sec > 0 else 0.0
    mean_val = statistics.mean(sorted_times)
    var_val = statistics.variance(sorted_times) if n > 1 else 0.0

    return TrialLatencyStats(
        p50_ms=round(pct(50), 3),
        p95_ms=round(pct(95), 3),
        p99_ms=round(pct(99), 3),
        min_ms=round(sorted_times[0], 3),
        max_ms=round(sorted_times[-1], 3),
        mean_ms=round(mean_val, 3),
        variance_ms=round(var_val, 3),
        throughput_ops_sec=round(throughput, 2),
    )


@dataclass
class WorkloadManifest:
    manifest_id: str
    tier: ScaleTier
    dataset_name: str
    generator_command: str
    dataset_license: str
    seed: int
    hardware_profile: dict[str, Any]
    engine_config: dict[str, Any]
    artifact_digest: str
    created_at: float = field(default_factory=time.time)

    @classmethod
    def create_default(
        cls,
        tier: ScaleTier = ScaleTier.P0,
        dataset_name: str = "LUBM-Synthetic",
        seed: int = 42,
    ) -> WorkloadManifest:
        hw = {
            "os": platform.platform(),
            "cpu_arch": platform.machine(),
            "cpu_count": os.cpu_count() or 4,
            "python_version": sys.version.split()[0],
        }
        engine_cfg = {
            "graph_backend": "memory",
            "reasoner": "datalog-forward",
            "shacl_mode": "strict",
        }
        return cls(
            manifest_id=f"manifest-{tier.value}-{seed}",
            tier=tier,
            dataset_name=dataset_name,
            generator_command=f"python -m scripts.benchmark_data --scale {tier.value.lower()} --seed {seed}",
            dataset_license="CC-BY-4.0",
            seed=seed,
            hardware_profile=hw,
            engine_config=engine_cfg,
            artifact_digest=hashlib.sha256(f"{tier.value}:{seed}".encode()).hexdigest(),
        )

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["tier"] = self.tier.value
        return d


class QualificationEngine:
    """End-to-end performance qualification, regression testing, and oracle verification."""

    # Binding profile targets
    BINDING_TARGETS = {
        ScaleTier.P0: {"point_read_p95_ms": 100.0, "graph_2hop_p95_ms": 500.0, "min_ingest_triples_sec": 500.0},
        ScaleTier.P1: {"point_read_p95_ms": 50.0, "graph_2hop_p95_ms": 400.0, "min_ingest_triples_sec": 5_000.0},
        ScaleTier.P2: {"point_read_p95_ms": 30.0, "graph_2hop_p95_ms": 300.0, "min_ingest_triples_sec": 10_000.0},
    }

    # AGG/OCA Stretch Objectives (recorded separately, non-binding pending Decision H-01 per CRA-036.8)
    STRETCH_OBJECTIVES = {
        ScaleTier.P1: {"point_read_p95_ms": 20.0, "graph_2hop_p95_ms": 250.0, "min_ingest_triples_sec": 50_000.0},
        ScaleTier.P2: {"point_read_p95_ms": 20.0, "graph_2hop_p95_ms": 250.0, "min_ingest_triples_sec": 50_000.0},
    }

    def __init__(self, manifest: WorkloadManifest) -> None:
        self.manifest = manifest
        self.storage = StorageAccounting()
        self.raw_trials: list[dict[str, Any]] = []
        self.gate_failures: list[dict[str, Any]] = []
        self.required_artifacts: dict[str, str | None] = {}

    def run_multi_trial(
        self,
        operation_name: str,
        operation: Callable[[], Any],
        oracle_expected: Any,
        trials_count: int = 3,
        iterations_per_trial: int = 20,
    ) -> dict[str, Any]:
        """Runs multiple seeded trials measuring latency, verifying oracle correctness, and checking variability."""
        trial_stats: list[TrialLatencyStats] = []

        for trial_idx in range(trials_count):
            timings: list[float] = []
            for _ in range(iterations_per_trial):
                t0 = time.perf_counter()
                actual = operation()
                elapsed_ms = (time.perf_counter() - t0) * 1000.0
                timings.append(elapsed_ms)

                # CRA-036.5: Verify independent oracle answer correctness
                if actual != oracle_expected:
                    raise AssertionError(
                        f"Oracle correctness check failed in trial {trial_idx}: expected {oracle_expected}, got {actual}"
                    )

            stats = compute_latencies(timings)
            trial_stats.append(stats)

        # Aggregate across trials
        p95_values = [s.p95_ms for s in trial_stats]
        [s.p50_ms for s in trial_stats]
        mean_p95 = statistics.mean(p95_values)
        std_dev_p95 = statistics.stdev(p95_values) if len(p95_values) > 1 else 0.0

        result = {
            "operation": operation_name,
            "trials_count": trials_count,
            "iterations_per_trial": iterations_per_trial,
            "mean_p95_ms": round(mean_p95, 3),
            "std_dev_p95_ms": round(std_dev_p95, 3),
            "trials": [asdict(s) for s in trial_stats],
            "oracle_verified": True,
        }
        self.raw_trials.append(result)
        return result

    def check_binding_targets(self, operation: str, measured_p95_ms: float) -> bool:
        """Enforces selected profile binding latency gates (CRA-036.4, CRA-036.8)."""
        tier_targets = self.BINDING_TARGETS.get(self.manifest.tier, {})
        target = tier_targets.get(operation)
        if target is None:
            return True
        return measured_p95_ms <= target

    def check_regression(
        self,
        current_p95: float,
        baseline_p95: float,
        threshold_pct: float = 10.0,
    ) -> tuple[bool, float]:
        """CI regression gate: fails on > 10% p95 latency regression (CRA-036.9)."""
        if baseline_p95 <= 0:
            return True, 0.0
        pct_diff = ((current_p95 - baseline_p95) / baseline_p95) * 100.0
        passed = pct_diff <= threshold_pct
        return passed, round(pct_diff, 2)

    def evaluate_learned_model_baselines(
        self,
        task_name: str,
        model_accuracy: float,
        model_ece: float,
        baseline_accuracies: dict[str, float],
        seeded_trials: list[float],
    ) -> dict[str, Any]:
        """Learned model qualification with 5 mandatory baselines and calibration error (CRA-036.10)."""
        required_baselines = {"majority_class", "random", "static_rule", "linear_logistic", "uncalibrated"}
        missing = required_baselines - set(baseline_accuracies.keys())
        if missing:
            raise ValueError(f"Model benchmark missing mandatory baselines: {missing} (CRA-036.10)")

        # Verify model beats majority class and random baselines
        beats_majority = model_accuracy > baseline_accuracies["majority_class"]
        beats_random = model_accuracy > baseline_accuracies["random"]
        calibration_acceptable = model_ece < 0.15  # Expected Calibration Error < 15%

        if len(seeded_trials) < 3:
            raise ValueError("Model benchmark must provide at least three seeded trials with variability")

        stdev_trials = statistics.stdev(seeded_trials)

        return {
            "task_name": task_name,
            "model_accuracy": model_accuracy,
            "model_ece": model_ece,
            "baselines": baseline_accuracies,
            "seeded_trials": seeded_trials,
            "trial_std_dev": round(stdev_trials, 4),
            "qualified": beats_majority and beats_random and calibration_acceptable,
        }

    # CRA-036.A: gates that must fail independently of how fast the median is.
    GATES = ("correctness", "leakage", "timeout", "artifacts")
    MIN_TRIALS = 3

    def run_gated_trials(
        self,
        operation_name: str,
        operation: Callable[[], Any],
        oracle_expected: Any,
        *,
        trials_count: int = 3,
        iterations_per_trial: int = 20,
        required_timeout_ms: float | None = None,
        leakage_probe: Callable[[Any], Any] | None = None,
    ) -> dict[str, Any]:
        """Measured trials that record gate failures instead of stopping at the first one (CRA-036.A).

        Every call is checked against the independent oracle (wrong answer -> ``correctness``), against
        ``leakage_probe`` (returns the leaked items, e.g. rows of another tenant -> ``leakage``) and against
        ``required_timeout_ms`` (a call that exceeds it or raises ``TimeoutError`` -> ``timeout``). Any other
        exception is a ``correctness`` failure: an error is never a pass. Latency is still measured so the
        report shows that a fast median does not rescue a failed gate.
        """
        failures: list[dict[str, Any]] = []
        trial_stats: list[TrialLatencyStats] = []
        measured_trials = 0
        for trial_idx in range(trials_count):
            timings: list[float] = []
            for it in range(iterations_per_trial):
                where = {"operation": operation_name, "trial": trial_idx, "iteration": it}
                t0 = time.perf_counter()
                try:
                    actual = operation()
                except TimeoutError as exc:
                    failures.append({**where, "gate": "timeout", "detail": f"operation timed out: {exc}"})
                    continue
                except Exception as exc:  # noqa: BLE001 - an erroring operation fails the correctness gate
                    failures.append({**where, "gate": "correctness", "detail": f"operation raised {type(exc).__name__}: {exc}"})
                    continue
                elapsed_ms = (time.perf_counter() - t0) * 1000.0
                timings.append(elapsed_ms)
                if actual != oracle_expected:
                    failures.append({**where, "gate": "correctness",
                                     "detail": f"expected {oracle_expected!r}, got {actual!r}"[:500]})
                if leakage_probe is not None:
                    leaked = list(leakage_probe(actual) or [])
                    if leaked:
                        failures.append({**where, "gate": "leakage", "detail": f"{len(leaked)} leaked item(s)",
                                         "items": [repr(x)[:200] for x in leaked[:10]]})
                if required_timeout_ms is not None and elapsed_ms > required_timeout_ms:
                    failures.append({**where, "gate": "timeout",
                                     "detail": f"{elapsed_ms:.3f} ms exceeds required {required_timeout_ms} ms"})
            trial_stats.append(compute_latencies(timings))
            measured_trials += 1 if timings else 0
        p95_values = [s.p95_ms for s in trial_stats]
        result = {
            "operation": operation_name,
            "trials_count": trials_count,
            "iterations_per_trial": iterations_per_trial,
            "required_timeout_ms": required_timeout_ms,
            "measured_trials": measured_trials,
            "median_p50_ms": round(statistics.median([s.p50_ms for s in trial_stats]), 3) if trial_stats else None,
            "mean_p95_ms": round(statistics.mean(p95_values), 3) if p95_values else None,
            "std_dev_p95_ms": round(statistics.stdev(p95_values), 3) if len(p95_values) > 1 else 0.0,
            "trials": [asdict(s) for s in trial_stats],
            "oracle_verified": not any(f["gate"] == "correctness" for f in failures),
            "failures": failures,
        }
        self.raw_trials.append(result)
        self.gate_failures.extend(failures)
        return result

    def require_artifact(self, path: str, sha256: str | None = None) -> None:
        """Declares an artifact (raw results, oracle file, receipt) the gate must find, optionally by digest."""
        self.required_artifacts[str(path)] = sha256

    def evaluate_gates(self) -> dict[str, Any]:
        """Per-gate verdicts for CRA-036.A; the run qualifies only when every gate passes."""
        failures: dict[str, list[dict[str, Any]]] = {g: [] for g in self.GATES}
        for f in self.gate_failures:
            failures.setdefault(f["gate"], []).append(f)
        for trial in self.raw_trials:
            if not trial.get("oracle_verified", False) and not failures["correctness"]:
                failures["correctness"].append({"operation": trial.get("operation"), "gate": "correctness",
                                                "detail": "trial not verified against the oracle"})
        art = failures["artifacts"]
        if not self.raw_trials:
            art.append({"gate": "artifacts", "detail": "no raw trial results recorded"})
        for trial in self.raw_trials:
            measured = trial.get("measured_trials", len(trial.get("trials", [])))
            if measured < self.MIN_TRIALS:
                art.append({"gate": "artifacts", "operation": trial.get("operation"),
                            "detail": f"{measured} measured trial(s); at least {self.MIN_TRIALS} required"})
        manifest = self.manifest.to_dict()
        for key in ("manifest_id", "dataset_name", "generator_command", "dataset_license", "artifact_digest"):
            if not manifest.get(key):
                art.append({"gate": "artifacts", "detail": f"manifest field '{key}' missing"})
        for path, digest in sorted(self.required_artifacts.items()):
            try:
                data = open(path, "rb").read()  # noqa: SIM115 - small receipt files
            except OSError:
                art.append({"gate": "artifacts", "detail": f"required artifact missing: {path}"})
                continue
            if not data:
                art.append({"gate": "artifacts", "detail": f"required artifact empty: {path}"})
            elif digest is not None and hashlib.sha256(data).hexdigest() != digest:
                art.append({"gate": "artifacts", "detail": f"required artifact digest mismatch: {path}"})
        gates = {g: {"passed": not failures[g], "failures": failures[g][:50], "failure_count": len(failures[g])}
                 for g in failures}
        return {"status": "QUALIFIED" if all(v["passed"] for v in gates.values()) else "REJECTED",
                "gates": gates}

    def generate_qualification_report(self) -> dict[str, Any]:
        """Machine-readable benchmark and qualification report; status comes from the CRA-036.A gates."""
        verdict = self.evaluate_gates()
        return {
            "manifest": self.manifest.to_dict(),
            "storage_accounting": self.storage.to_dict(),
            "raw_trials": self.raw_trials,
            "stretch_objectives": self.STRETCH_OBJECTIVES.get(self.manifest.tier, {}),
            "status": verdict["status"],
            "gates": verdict["gates"],
            "timestamp": time.time(),
        }
