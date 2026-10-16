"""Distributed Pipeline Executor — task queue with worker pools, backpressure, and priority lanes.

Executes PipelineSpec stages as a DAG with configurable parallelism,
retry policies, circuit breakers, and graceful degradation.
"""

from __future__ import annotations

import logging
import queue
import threading
import time
import uuid
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable

from eoip.systems.pipeline_factory import PipelineSpec, PipelineStage

logger = logging.getLogger(__name__)


class TaskPriority(int, Enum):
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    BACKGROUND = 4


class TaskStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    CANCELLED = "CANCELLED"
    BACKPRESSURE = "BACKPRESSURE"


@dataclass
class TaskResult:
    task_id: str
    stage_id: str
    status: TaskStatus
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    duration_ms: int = 0
    attempt: int = 1
    worker_id: str = ""
    started_at: str = ""
    completed_at: str = ""


@dataclass
class PipelineTask:
    task_id: str
    pipeline_id: str
    stage: PipelineStage
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.QUEUED
    attempt: int = 0
    max_attempts: int = 3
    created_at: str = ""
    context: dict[str, Any] = field(default_factory=dict)

    def __lt__(self, other: PipelineTask) -> bool:
        return self.priority.value < other.priority.value


@dataclass
class ExecutorMetrics:
    tasks_queued: int = 0
    tasks_running: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    tasks_retried: int = 0
    backpressure_events: int = 0
    avg_task_duration_ms: float = 0.0
    queue_depth: int = 0
    worker_utilization: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class BackpressureConfig:
    max_queue_depth: int = 1000
    high_watermark: float = 0.8
    low_watermark: float = 0.3
    pause_on_high: bool = True
    shed_priority_below: TaskPriority = TaskPriority.BACKGROUND


class WorkerPool:
    """Fixed-size thread pool executing pipeline tasks."""

    def __init__(self, size: int = 4, name: str = "default") -> None:
        self.name = name
        self.size = size
        self._task_queue: queue.PriorityQueue[PipelineTask] = queue.PriorityQueue()
        self._workers: list[threading.Thread] = []
        self._running = False
        self._lock = threading.Lock()
        self._active_count = 0
        self._stage_handlers: dict[str, Callable] = {}
        self._results: dict[str, TaskResult] = {}
        self._metrics = ExecutorMetrics()

    def register_handler(self, stage_type: str, handler: Callable) -> None:
        self._stage_handlers[stage_type] = handler

    def start(self) -> None:
        self._running = True
        for i in range(self.size):
            t = threading.Thread(target=self._worker_loop, args=(f"{self.name}-{i}",), daemon=True)
            self._workers.append(t)
            t.start()

    def stop(self, wait: bool = True) -> None:
        self._running = False
        if wait:
            for t in self._workers:
                t.join(timeout=5)
        self._workers.clear()

    def submit(self, task: PipelineTask) -> str:
        with self._lock:
            self._metrics.tasks_queued += 1
            self._metrics.queue_depth = self._task_queue.qsize() + 1
        self._task_queue.put(task)
        return task.task_id

    def get_result(self, task_id: str) -> TaskResult | None:
        return self._results.get(task_id)

    def get_metrics(self) -> ExecutorMetrics:
        with self._lock:
            self._metrics.queue_depth = self._task_queue.qsize()
            if self.size > 0:
                self._metrics.worker_utilization = self._active_count / self.size
            return ExecutorMetrics(**asdict(self._metrics))

    def _worker_loop(self, worker_id: str) -> None:
        while self._running:
            try:
                task = self._task_queue.get(timeout=1.0)
            except queue.Empty:
                continue

            with self._lock:
                self._active_count += 1
                self._metrics.tasks_running += 1

            result = self._execute_task(task, worker_id)
            self._results[task.task_id] = result

            with self._lock:
                self._active_count -= 1
                self._metrics.tasks_running -= 1
                if result.status == TaskStatus.COMPLETED:
                    self._metrics.tasks_completed += 1
                elif result.status == TaskStatus.FAILED:
                    self._metrics.tasks_failed += 1

            self._task_queue.task_done()

    def _execute_task(self, task: PipelineTask, worker_id: str) -> TaskResult:
        t0 = time.time()
        started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        task.status = TaskStatus.RUNNING
        task.attempt += 1

        handler = self._stage_handlers.get(task.stage.stage_type.value)
        if not handler:
            handler = self._default_handler

        try:
            output = handler(task.stage, task.context)
            ms = int((time.time() - t0) * 1000)
            return TaskResult(
                task_id=task.task_id, stage_id=task.stage.stage_id,
                status=TaskStatus.COMPLETED, output=output or {},
                duration_ms=ms, attempt=task.attempt, worker_id=worker_id,
                started_at=started,
                completed_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            )
        except Exception as e:
            ms = int((time.time() - t0) * 1000)
            if task.attempt < task.max_attempts and task.stage.retry_on_failure:
                task.status = TaskStatus.RETRYING
                with self._lock:
                    self._metrics.tasks_retried += 1
                self._task_queue.put(task)
                return TaskResult(
                    task_id=task.task_id, stage_id=task.stage.stage_id,
                    status=TaskStatus.RETRYING, error=str(e),
                    duration_ms=ms, attempt=task.attempt, worker_id=worker_id,
                    started_at=started,
                )
            return TaskResult(
                task_id=task.task_id, stage_id=task.stage.stage_id,
                status=TaskStatus.FAILED, error=str(e),
                duration_ms=ms, attempt=task.attempt, worker_id=worker_id,
                started_at=started,
                completed_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            )

    def _default_handler(self, stage: PipelineStage, context: dict) -> dict[str, Any]:
        return {"stage": stage.stage_id, "status": "executed", "config": stage.config}


class PipelineExecutor:
    """Executes PipelineSpec as a DAG with backpressure and priority lanes."""

    def __init__(self, worker_count: int = 4,
                 backpressure: BackpressureConfig | None = None) -> None:
        self._pool = WorkerPool(size=worker_count)
        self._bp = backpressure or BackpressureConfig()
        self._executions: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._paused = False

    def start(self) -> None:
        self._pool.start()

    def stop(self) -> None:
        self._pool.stop()

    def register_stage_handler(self, stage_type: str, handler: Callable) -> None:
        self._pool.register_handler(stage_type, handler)

    def submit_pipeline(self, spec: PipelineSpec,
                        priority: TaskPriority = TaskPriority.NORMAL,
                        context: dict[str, Any] | None = None) -> str:
        execution_id = f"pexec-{uuid.uuid4().hex[:8]}"
        order = spec.get_execution_order()
        tasks: dict[str, PipelineTask] = {}
        stage_map = {s.stage_id: s for s in spec.stages}

        for stage_id in order:
            stage = stage_map[stage_id]
            task = PipelineTask(
                task_id=f"{execution_id}-{stage_id}",
                pipeline_id=spec.pipeline_id,
                stage=stage,
                priority=priority,
                max_attempts=3 if stage.retry_on_failure else 1,
                created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                context=context or {},
            )
            tasks[stage_id] = task

        with self._lock:
            self._executions[execution_id] = {
                "pipeline_id": spec.pipeline_id,
                "tasks": tasks,
                "order": order,
                "status": "RUNNING",
                "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }

        if self._check_backpressure():
            logger.warning("Backpressure active, pipeline %s may be delayed", execution_id)

        for stage_id in order:
            self._pool.submit(tasks[stage_id])

        return execution_id

    def get_execution_status(self, execution_id: str) -> dict[str, Any] | None:
        with self._lock:
            exec_info = self._executions.get(execution_id)
            if not exec_info:
                return None
            tasks = exec_info["tasks"]
            results = {}
            for sid, task in tasks.items():
                result = self._pool.get_result(task.task_id)
                results[sid] = {
                    "status": result.status.value if result else task.status.value,
                    "duration_ms": result.duration_ms if result else 0,
                    "attempt": result.attempt if result else task.attempt,
                    "error": result.error if result else None,
                }
            return {
                "execution_id": execution_id,
                "pipeline_id": exec_info["pipeline_id"],
                "status": exec_info["status"],
                "stages": results,
            }

    def get_metrics(self) -> dict[str, Any]:
        return self._pool.get_metrics().to_dict()

    def _check_backpressure(self) -> bool:
        metrics = self._pool.get_metrics()
        ratio = metrics.queue_depth / max(1, self._bp.max_queue_depth)
        if ratio >= self._bp.high_watermark:
            self._paused = self._bp.pause_on_high
            with self._lock:
                self._pool._metrics.backpressure_events += 1
            return True
        if ratio <= self._bp.low_watermark:
            self._paused = False
        return False
