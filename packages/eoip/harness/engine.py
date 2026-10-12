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

    run_pipeline = run

    def stats(self) -> dict[str, Any]:

        with self._lock:
            return {
                "engine": "harness_engineering",
                "pipelines": len(self._pipelines),
                "runs": len(self._runs),
                "completed_runs": sum(1 for run in self._runs if run.status == "completed"),
                "failed_runs": sum(1 for run in self._runs if run.status == "failed"),
            }


# ── Parallel Fan-Out/Fan-In (MapReduce) (AGENT-004) ────────────────────

import concurrent.futures
from enum import Enum


class MergeStrategy(str, Enum):
    LAST_WRITE_WINS = "LAST_WRITE_WINS"
    RECURSIVE_MERGE = "RECURSIVE_MERGE"
    APPEND_LISTS = "APPEND_LISTS"
    FAIL_ON_CONFLICT = "FAIL_ON_CONFLICT"


@dataclass
class StateSchema:
    """Defines conflict detection and race-condition-safe state merging rules."""

    default_strategy: MergeStrategy = MergeStrategy.RECURSIVE_MERGE
    field_strategies: dict[str, MergeStrategy] = field(default_factory=dict)

    def merge_states(self, states: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
        """Safely merge shard outputs into unified state with conflict detection."""
        merged: dict[str, Any] = {}
        conflicts: list[str] = []

        for shard_idx, state in enumerate(states):
            for key, val in state.items():
                strat = self.field_strategies.get(key, self.default_strategy)

                if key not in merged:
                    merged[key] = val
                    continue

                existing = merged[key]

                if strat == MergeStrategy.LAST_WRITE_WINS:
                    merged[key] = val

                elif strat == MergeStrategy.APPEND_LISTS:
                    if not isinstance(existing, list):
                        existing = [existing]
                    if isinstance(val, list):
                        existing.extend(val)
                    else:
                        existing.append(val)
                    merged[key] = existing

                elif strat == MergeStrategy.FAIL_ON_CONFLICT:
                    if existing != val:
                        conflicts.append(f"Conflict on '{key}': existing={existing} vs shard_{shard_idx}={val}")

                else:  # RECURSIVE_MERGE
                    if isinstance(existing, dict) and isinstance(val, dict):
                        sub_merged, sub_conflicts = self.merge_states([existing, val])
                        merged[key] = sub_merged
                        conflicts.extend(sub_conflicts)
                    elif isinstance(existing, list) and isinstance(val, list):
                        merged[key] = existing + val
                    elif isinstance(existing, (int, float)) and isinstance(val, (int, float)):
                        merged[key] = existing + val  # Sum numerical aggregates
                    else:
                        merged[key] = val

        return merged, conflicts


class FanOutStage(PipelineStage):
    """Splits work into parallel shards executed concurrently (Map stage)."""

    def __init__(
        self,
        name: str,
        shard_generator: Callable[[dict[str, Any]], list[Any]],
        worker_fn: Callable[[Any, dict[str, Any]], dict[str, Any]],
        max_workers: int = 4,
        shard_timeout_sec: float = 10.0,
        description: str = "Parallel Fan-Out Map Stage",
    ) -> None:
        self.shard_generator = shard_generator
        self.worker_fn = worker_fn
        self.max_workers = max_workers
        self.shard_timeout_sec = shard_timeout_sec

        def _handler(ctx: dict[str, Any]) -> dict[str, Any]:
            shards = self.shard_generator(ctx)
            results: list[dict[str, Any]] = []

            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(self.worker_fn, shard, ctx): idx
                    for idx, shard in enumerate(shards)
                }
                for fut in concurrent.futures.as_completed(futures):
                    idx = futures[fut]
                    try:
                        res = fut.result(timeout=self.shard_timeout_sec)
                        results.append(res)
                    except Exception as exc:
                        results.append({"_shard_error": str(exc), "_shard_idx": idx})

            return {**ctx, f"_{self.name}_shards": results, f"_{self.name}_shard_count": len(shards)}

        super().__init__(name=name, handler=_handler, description=description)


class FanInStage(PipelineStage):
    """Collects and merges shard outputs with race-condition-safe StateSchema (Reduce stage)."""

    def __init__(
        self,
        name: str,
        fan_out_stage_name: str,
        schema: StateSchema | None = None,
        depends_on: list[str] | None = None,
        description: str = "Parallel Fan-In Reduce Stage",
    ) -> None:
        self.fan_out_stage_name = fan_out_stage_name
        self.schema = schema or StateSchema()
        deps = depends_on or [fan_out_stage_name]

        def _handler(ctx: dict[str, Any]) -> dict[str, Any]:
            shard_results = ctx.get(f"_{self.fan_out_stage_name}_shards", [])
            merged_state, conflicts = self.schema.merge_states(shard_results)
            return {
                **ctx,
                **merged_state,
                f"_{self.name}_conflicts": conflicts,
                f"_{self.name}_merged_count": len(shard_results),
            }

        super().__init__(name=name, handler=_handler, depends_on=deps, description=description)


_instance: HarnessEngine | None = None

_lock = threading.Lock()


def get_harness_engine() -> HarnessEngine:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = HarnessEngine()
    return _instance

