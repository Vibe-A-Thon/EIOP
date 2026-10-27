"""Scheduled Task Executor — cron-style job scheduler with execution history.

Supports interval-based and one-shot tasks with execution tracking,
retry on failure, and history retention.
"""

from __future__ import annotations

import enum
import threading
import time
import traceback
import uuid
from dataclasses import dataclass, field
from typing import Any
from collections.abc import Callable


class TaskStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    DISABLED = "DISABLED"
    CANCELLED = "CANCELLED"


@dataclass
class TaskResult:
    run_id: str
    task_id: str
    status: TaskStatus
    started_at: float
    finished_at: float
    duration_ms: float
    output: Any = None
    error: str | None = None
    attempt: int = 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "task_id": self.task_id,
            "status": self.status.value,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_ms": round(self.duration_ms, 2),
            "output": str(self.output) if self.output else None,
            "error": self.error,
            "attempt": self.attempt,
        }


@dataclass
class ScheduledTask:
    task_id: str
    name: str
    description: str
    callable_fn: Callable[[], Any]
    interval_seconds: float | None = None
    max_retries: int = 0
    retry_delay_seconds: float = 5.0
    timeout_seconds: float | None = None
    enabled: bool = True
    tags: list[str] = field(default_factory=list)
    total_runs: int = 0
    total_successes: int = 0
    total_failures: int = 0
    last_run_at: float | None = None
    last_status: TaskStatus | None = None
    next_run_at: float | None = None
    history: list[TaskResult] = field(default_factory=list)
    max_history: int = 100
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "interval_seconds": self.interval_seconds,
            "max_retries": self.max_retries,
            "enabled": self.enabled,
            "tags": self.tags,
            "total_runs": self.total_runs,
            "total_successes": self.total_successes,
            "total_failures": self.total_failures,
            "last_run_at": self.last_run_at,
            "last_status": self.last_status.value if self.last_status else None,
            "next_run_at": self.next_run_at,
            "success_rate": round(self.total_successes / max(self.total_runs, 1), 3),
            "created_at": self.created_at,
        }


class TaskExecutor:
    """Scheduled task executor with history and retry support."""

    def __init__(self, max_history_per_task: int = 100) -> None:
        self._tasks: dict[str, ScheduledTask] = {}
        self._lock = threading.Lock()
        self._max_history = max_history_per_task

    def register(self, name: str, fn: Callable[[], Any],
                 description: str = "",
                 interval_seconds: float | None = None,
                 max_retries: int = 0,
                 retry_delay_seconds: float = 5.0,
                 tags: list[str] | None = None) -> ScheduledTask:
        task = ScheduledTask(
            task_id=uuid.uuid4().hex[:12],
            name=name,
            description=description,
            callable_fn=fn,
            interval_seconds=interval_seconds,
            max_retries=max_retries,
            retry_delay_seconds=retry_delay_seconds,
            tags=tags or [],
            max_history=self._max_history,
        )
        if interval_seconds:
            task.next_run_at = time.time() + interval_seconds
        with self._lock:
            self._tasks[task.task_id] = task
        return task

    def execute(self, task_id: str) -> TaskResult:
        with self._lock:
            task = self._tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task {task_id} not found")

        attempt = 0
        last_error = None

        while attempt <= task.max_retries:
            attempt += 1
            start = time.time()
            run_id = uuid.uuid4().hex[:12]

            try:
                output = task.callable_fn()
                end = time.time()
                result = TaskResult(
                    run_id=run_id,
                    task_id=task_id,
                    status=TaskStatus.COMPLETED,
                    started_at=start,
                    finished_at=end,
                    duration_ms=(end - start) * 1000,
                    output=output,
                    attempt=attempt,
                )
                with self._lock:
                    task.total_runs += 1
                    task.total_successes += 1
                    task.last_run_at = end
                    task.last_status = TaskStatus.COMPLETED
                    if task.interval_seconds:
                        task.next_run_at = end + task.interval_seconds
                    task.history.append(result)
                    if len(task.history) > task.max_history:
                        task.history = task.history[-task.max_history:]
                return result

            except Exception:
                last_error = traceback.format_exc()
                if attempt <= task.max_retries:
                    time.sleep(task.retry_delay_seconds)

        end = time.time()
        result = TaskResult(
            run_id=uuid.uuid4().hex[:12],
            task_id=task_id,
            status=TaskStatus.FAILED,
            started_at=start,
            finished_at=end,
            duration_ms=(end - start) * 1000,
            error=last_error,
            attempt=attempt,
        )
        with self._lock:
            task.total_runs += 1
            task.total_failures += 1
            task.last_run_at = end
            task.last_status = TaskStatus.FAILED
            if task.interval_seconds:
                task.next_run_at = end + task.interval_seconds
            task.history.append(result)
            if len(task.history) > task.max_history:
                task.history = task.history[-task.max_history:]
        return result

    def run_due_tasks(self) -> list[TaskResult]:
        now = time.time()
        due: list[str] = []
        with self._lock:
            for task in self._tasks.values():
                if (task.enabled and task.interval_seconds
                        and task.next_run_at and task.next_run_at <= now):
                    due.append(task.task_id)

        results = []
        for tid in due:
            results.append(self.execute(tid))
        return results

    def enable(self, task_id: str) -> bool:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return False
            task.enabled = True
            if task.interval_seconds:
                task.next_run_at = time.time() + task.interval_seconds
            return True

    def disable(self, task_id: str) -> bool:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return False
            task.enabled = False
            task.next_run_at = None
            return True

    def get(self, task_id: str) -> ScheduledTask | None:
        with self._lock:
            return self._tasks.get(task_id)

    def get_history(self, task_id: str, limit: int = 20) -> list[TaskResult]:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return []
            return list(reversed(task.history[-limit:]))

    def list_tasks(self, tag: str | None = None,
                   enabled_only: bool = False) -> list[dict[str, Any]]:
        with self._lock:
            tasks = list(self._tasks.values())
        results = []
        for t in tasks:
            if enabled_only and not t.enabled:
                continue
            if tag and tag not in t.tags:
                continue
            results.append(t.to_dict())
        return results

    def remove(self, task_id: str) -> bool:
        with self._lock:
            return self._tasks.pop(task_id, None) is not None

    def stats(self) -> dict[str, Any]:
        with self._lock:
            total_runs = sum(t.total_runs for t in self._tasks.values())
            total_successes = sum(t.total_successes for t in self._tasks.values())
            total_failures = sum(t.total_failures for t in self._tasks.values())
            enabled = sum(1 for t in self._tasks.values() if t.enabled)
            return {
                "total_tasks": len(self._tasks),
                "enabled_tasks": enabled,
                "disabled_tasks": len(self._tasks) - enabled,
                "total_runs": total_runs,
                "total_successes": total_successes,
                "total_failures": total_failures,
                "overall_success_rate": round(total_successes / max(total_runs, 1), 3),
            }


_INSTANCE: TaskExecutor | None = None
_LOCK = threading.Lock()


def get_task_executor() -> TaskExecutor:
    global _INSTANCE
    if _INSTANCE is None:
        with _LOCK:
            if _INSTANCE is None:
                _INSTANCE = TaskExecutor()
    return _INSTANCE


# ============================================================================
# Distributed Scheduling & HA Leader Election (INFRA-005)
# ============================================================================

class LeaderElection:
    """Distributed leader election for HA scheduling coordinator."""

    _cluster_state: dict[str, tuple[str, float]] = {}  # cluster_name -> (leader_id, expires_at)
    _cluster_lock = threading.Lock()

    def __init__(self, node_id: str, lease_duration: float = 10.0, cluster_name: str = "default") -> None:
        self.node_id = node_id
        self.lease_duration = lease_duration
        self.cluster_name = cluster_name

    def try_acquire(self) -> bool:
        with self._cluster_lock:
            now = time.time()
            current = self._cluster_state.get(self.cluster_name)
            if current is None or now > current[1]:
                self._cluster_state[self.cluster_name] = (self.node_id, now + self.lease_duration)
                return True
            return current[0] == self.node_id

    def renew(self) -> bool:
        with self._cluster_lock:
            current = self._cluster_state.get(self.cluster_name)
            if current and current[0] == self.node_id:
                self._cluster_state[self.cluster_name] = (self.node_id, time.time() + self.lease_duration)
                return True
            return False

    def step_down(self) -> None:
        with self._cluster_lock:
            current = self._cluster_state.get(self.cluster_name)
            if current and current[0] == self.node_id:
                del self._cluster_state[self.cluster_name]

    @property
    def is_leader(self) -> bool:
        with self._cluster_lock:
            current = self._cluster_state.get(self.cluster_name)
            return bool(current and current[0] == self.node_id and time.time() < current[1])


class DistributedLock:
    """Distributed mutual exclusion lock for task scheduling across replicas."""

    _global_locks: dict[str, tuple[str, float]] = {}  # lock_name -> (owner, expires_at)
    _global_fencing_tokens: dict[str, int] = {}  # lock_name -> monotonic token
    _lock_mutex = threading.Lock()

    def __init__(self, lock_name: str, owner_id: str, ttl_seconds: float = 30.0) -> None:
        self.lock_name = lock_name
        self.owner_id = owner_id
        self.ttl_seconds = ttl_seconds
        self.fencing_token: int = 0

    def acquire(self) -> bool:
        with self._lock_mutex:
            now = time.time()
            current = self._global_locks.get(self.lock_name)
            if current is None or now > current[1]:
                self._global_locks[self.lock_name] = (self.owner_id, now + self.ttl_seconds)
                self._global_fencing_tokens[self.lock_name] = self._global_fencing_tokens.get(self.lock_name, 0) + 1
                self.fencing_token = self._global_fencing_tokens[self.lock_name]
                return True
            if current[0] == self.owner_id:
                return True
            return False

    def release(self) -> bool:
        with self._lock_mutex:
            current = self._global_locks.get(self.lock_name)
            if current and current[0] == self.owner_id:
                del self._global_locks[self.lock_name]
                return True
            return False


class TaskDAG:
    """Dependency graph for task execution ordering."""

    def __init__(self) -> None:
        self._dependencies: dict[str, set[str]] = {}  # task -> parents
        self._tasks: set[str] = set()

    def add_task(self, task_id: str) -> None:
        self._tasks.add(task_id)
        self._dependencies.setdefault(task_id, set())

    def add_dependency(self, child_task_id: str, parent_task_id: str) -> None:
        self.add_task(child_task_id)
        self.add_task(parent_task_id)
        self._dependencies[child_task_id].add(parent_task_id)

    def execution_order(self) -> list[str]:
        """Topological sort of tasks using Kahn's algorithm."""
        in_degree = {t: len(self._dependencies[t]) for t in self._tasks}
        queue = [t for t, deg in in_degree.items() if deg == 0]
        order = []

        # Build reverse adjacency (parent -> children)
        children: dict[str, list[str]] = {t: [] for t in self._tasks}
        for child, parents in self._dependencies.items():
            for p in parents:
                children[p].append(child)

        while queue:
            curr = queue.pop(0)
            order.append(curr)
            for ch in children.get(curr, []):
                in_degree[ch] -= 1
                if in_degree[ch] == 0:
                    queue.append(ch)

        if len(order) < len(self._tasks):
            raise ValueError("Cycle detected in TaskDAG")

        return order

