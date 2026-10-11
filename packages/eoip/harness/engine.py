"""Harness engineering engine for deterministic pipeline execution."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class PipelineStage:
    name: str
    handler: Callable[[dict[str, Any]], dict[str, Any]]
    retries: int = 0


@dataclass
class HarnessRun:
    run_id: str
    pipeline: str
    status: str
    stages: list[dict[str, Any]]
    started_at: float = field(default_factory=time.time)
    finished_at: float | None = None


class HarnessEngine:
    """Register and run named pipelines with retry-aware stage tracking."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._pipelines: dict[str, list[PipelineStage]] = {}
        self._runs: list[HarnessRun] = []
        self.register_pipeline(
            "default",
            [
                PipelineStage("load", lambda ctx: {**ctx, "loaded": True}),
                PipelineStage("validate", lambda ctx: {**ctx, "valid": True}),
                PipelineStage("analyze", lambda ctx: {**ctx, "analysis_complete": True}),
                PipelineStage("report", lambda ctx: {**ctx, "reported": True}),
            ],
        )

    def register_pipeline(self, name: str, stages: list[PipelineStage]) -> None:
        with self._lock:
            self._pipelines[name] = list(stages)

    def run(self, pipeline: str = "default", context: dict[str, Any] | None = None) -> HarnessRun:
        with self._lock:
            stages = list(self._pipelines.get(pipeline, []))
            run_id = f"harness-run-{len(self._runs) + 1:08d}"
        ctx = dict(context or {})
        records: list[dict[str, Any]] = []
        status = "completed"
        for stage in stages:
            attempts = 0
            while True:
                attempts += 1
                try:
                    ctx = stage.handler(ctx)
                    records.append({"stage": stage.name, "status": "passed", "attempts": attempts})
                    break
                except Exception as exc:  # noqa: BLE001 - stage harness records failures.
                    if attempts > stage.retries + 1:
                        status = "failed"
                        records.append({"stage": stage.name, "status": "failed", "attempts": attempts, "error": str(exc)})
                        break
            if status == "failed":
                break
        run = HarnessRun(run_id=run_id, pipeline=pipeline, status=status, stages=records, finished_at=time.time())
        with self._lock:
            self._runs.append(run)
        return run

    def stats(self) -> dict[str, Any]:
        with self._lock:
            return {
                "engine": "harness_engineering",
                "pipelines": len(self._pipelines),
                "runs": len(self._runs),
                "completed_runs": sum(1 for run in self._runs if run.status == "completed"),
            }


_instance: HarnessEngine | None = None
_lock = threading.Lock()


def get_harness_engine() -> HarnessEngine:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = HarnessEngine()
    return _instance
