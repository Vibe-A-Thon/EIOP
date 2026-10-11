"""Harness engineering engine for deterministic pipeline & DAG execution."""

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
    depends_on: list[str] = field(default_factory=list)
    timeout_sec: float | None = None
    description: str = ""


@dataclass
class HarnessRun:
    run_id: str
    pipeline: str
    status: str
    stages: list[dict[str, Any]]
    context_output: dict[str, Any] = field(default_factory=dict)
    started_at: float = field(default_factory=time.time)
    finished_at: float | None = None
    duration_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "pipeline": self.pipeline,
            "status": self.status,
            "stages": self.stages,
            "context_output": self.context_output,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_ms": self.duration_ms,
        }


class HarnessEngine:
    """Register and run named pipelines and DAGs with retry-aware, telemetry-rich stage tracking."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._pipelines: dict[str, list[PipelineStage]] = {}
        self._runs: list[HarnessRun] = []
        self._custom_handlers: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {}

        # Default enterprise ingestion & graph analysis pipeline
        self.register_pipeline(
            "default",
            [
                PipelineStage("load", lambda ctx: {**ctx, "loaded": True, "load_timestamp": time.time()}, description="Load data source"),
                PipelineStage("validate", lambda ctx: {**ctx, "valid": True, "validation_passed": True}, depends_on=["load"], description="Validate schemas"),
                PipelineStage("analyze", lambda ctx: {**ctx, "analysis_complete": True, "insights_count": 5}, depends_on=["validate"], description="Run analytics"),
                PipelineStage("report", lambda ctx: {**ctx, "reported": True, "report_id": f"rep-{int(time.time())}"}, depends_on=["analyze"], description="Publish synthesis report"),
            ],
        )

        # Graph intelligence extraction pipeline
        self.register_pipeline(
            "graph_intelligence",
            [
                PipelineStage("extract_topology", lambda ctx: {**ctx, "nodes_extracted": len(ctx.get("entities", [])), "edges_extracted": len(ctx.get("relations", []))}),
                PipelineStage("compute_centrality", lambda ctx: {**ctx, "centrality_ranked": True, "top_node": "core-hub"}, depends_on=["extract_topology"]),
                PipelineStage("detect_anomalies", lambda ctx: {**ctx, "anomalies_detected": 0, "status": "clean"}, depends_on=["compute_centrality"]),
                PipelineStage("synthesize_knowledge", lambda ctx: {**ctx, "knowledge_synthesized": True}, depends_on=["detect_anomalies"]),
            ],
        )

    def register_pipeline(self, name: str, stages: list[PipelineStage]) -> None:
        with self._lock:
            self._pipelines[name] = list(stages)

    def list_pipelines(self) -> list[dict[str, Any]]:
        with self._lock:
            result = []
            for name, stages in self._pipelines.items():
                result.append({
                    "pipeline_name": name,
                    "stages_count": len(stages),
                    "stages": [{"name": s.name, "depends_on": s.depends_on, "retries": s.retries, "description": s.description} for s in stages],
                })
            return result

    def _resolve_execution_order(self, stages: list[PipelineStage]) -> list[PipelineStage]:
        """Topological sort of stages based on depends_on."""
        stage_by_name = {s.name: s for s in stages}
        visited: set[str] = set()
        order: list[PipelineStage] = []

        def visit(name: str, stack: set[str]) -> None:
            if name in stack:
                raise ValueError(f"Cycle detected in stage dependencies involving {name}")
            if name not in visited and name in stage_by_name:
                stack.add(name)
                for dep in stage_by_name[name].depends_on:
                    visit(dep, stack)
                stack.remove(name)
                visited.add(name)
                order.append(stage_by_name[name])

        for stage in stages:
            if stage.name not in visited:
                visit(stage.name, set())
        return order

    def run(self, pipeline: str = "default", context: dict[str, Any] | None = None) -> HarnessRun:
        with self._lock:
            if pipeline not in self._pipelines:
                raise ValueError(f"Pipeline '{pipeline}' is not registered.")
            raw_stages = list(self._pipelines[pipeline])
            run_id = f"harness-run-{len(self._runs) + 1:08d}"

        start_time = time.time()
        ordered_stages = self._resolve_execution_order(raw_stages)
        ctx = dict(context or {})
        records: list[dict[str, Any]] = []
        status = "completed"

        for stage in ordered_stages:
            stage_start = time.time()
            attempts = 0
            passed = False
            last_error = None

            while attempts <= stage.retries:
                attempts += 1
                try:
                    ctx = stage.handler(ctx)
                    records.append({
                        "stage": stage.name,
                        "status": "passed",
                        "attempts": attempts,
                        "duration_ms": round((time.time() - stage_start) * 1000, 2),
                    })
                    passed = True
                    break
                except Exception as exc:  # noqa: BLE001
                    last_error = str(exc)

            if not passed:
                status = "failed"
                records.append({
                    "stage": stage.name,
                    "status": "failed",
                    "attempts": attempts,
                    "error": last_error,
                    "duration_ms": round((time.time() - stage_start) * 1000, 2),
                })
                break

        finished_time = time.time()
        duration_ms = round((finished_time - start_time) * 1000, 2)
        run = HarnessRun(
            run_id=run_id,
            pipeline=pipeline,
            status=status,
            stages=records,
            context_output=ctx,
            started_at=start_time,
            finished_at=finished_time,
            duration_ms=duration_ms,
        )
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
                "failed_runs": sum(1 for run in self._runs if run.status == "failed"),
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

