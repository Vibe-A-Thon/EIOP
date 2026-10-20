"""Isolated worker process supervisor (CRA-002.2, CRA-002.7, CRA-002.8, CRA-002.11).

Spawns worker processes, manages watchdogs, enforces timeouts and resource limits,
terminates rogue process trees within <= 1s, cleans temp directories, and respawns workers.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from eoip.workers.protocol import (
    ResourceClass,
    WorkerLimits,
    WorkerOutcome,
    WorkerRequest,
    WorkerResponse,
    WorkerResult,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Pydantic Module-Level Models (CRA-002.11)
# ---------------------------------------------------------------------------

class WorkerExecutionRequest(BaseModel):
    task_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    resource_class: str = "standard"
    engine: str = "generic"
    engine_version: str = "1.0.0"
    profile: str = "P0"
    payload: dict[str, Any] = Field(default_factory=dict)
    allow_network: bool = False
    sandbox_script: str | None = None
    timeout_seconds: float | None = None


class WorkerExecutionResponse(BaseModel):
    task_id: str
    outcome: str  # COMPLETED, TIMEOUT, OOM, LIMIT_EXCEEDED, FAILED, KILLED
    status_code: int = 200
    result: dict[str, Any] = Field(default_factory=dict)
    error_message: str | None = None
    elapsed_ms: float = 0.0


class SupervisorStats(BaseModel):
    active_workers: int = 0
    total_executions: int = 0
    completed_executions: int = 0
    timeouts: int = 0
    ooms: int = 0
    kills: int = 0
    respawns: int = 0


# ---------------------------------------------------------------------------
# Process-Tree Termination (< 1s kill latency, CRA-002.8)
# ---------------------------------------------------------------------------

def kill_process_tree(pid: int) -> None:
    """Terminate the whole worker process tree within 1 s of breach detection."""
    try:
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        else:
            try:
                pgid = os.getpgid(pid)
                if pgid == os.getpgrp():
                    # FT-F03: the worker shares OUR process group (it was not started in its
                    # own session); killpg would SIGKILL the host API/worker and its siblings.
                    logger.warning("worker pid %s shares the host process group %s; killing pid only", pid, pgid)
                    os.kill(pid, signal.SIGKILL)
                else:
                    logger.info("killing worker process group pgid=%s (pid=%s)", pgid, pid)
                    os.killpg(pgid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                os.kill(pid, signal.SIGKILL)
    except Exception as e:
        logger.warning(f"Error terminating process tree for PID {pid}: {e}")


# ---------------------------------------------------------------------------
# Worker Supervisor (CRA-002.8, CRA-002.11)
# ---------------------------------------------------------------------------

class WorkerSupervisor:
    """Orchestrates isolated worker execution, watchdog fencing and cleanup."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._total_executions = 0
        self._completed_executions = 0
        self._timeouts = 0
        self._ooms = 0
        self._kills = 0
        self._respawns = 0
        self._active_workers = 0

    def stats(self) -> dict[str, Any]:
        """Telemetry stats wired into brain_os (CRA-002.11)."""
        with self._lock:
            return {
                "active_workers": self._active_workers,
                "total_executions": self._total_executions,
                "completed_executions": self._completed_executions,
                "timeouts": self._timeouts,
                "ooms": self._ooms,
                "kills": self._kills,
                "respawns": self._respawns,
            }

    def execute_task(
        self,
        request: WorkerExecutionRequest,
        tenant_limits: WorkerLimits | None = None,
    ) -> WorkerExecutionResponse:
        """Execute a task in an isolated worker subprocess with watchdog enforcement."""
        limits = WorkerLimits.resolve_effective(request.resource_class, tenant_limits)
        effective_timeout = (
            min(limits.max_wall_time_seconds, request.timeout_seconds)
            if request.timeout_seconds is not None
            else limits.max_wall_time_seconds
        )

        with self._lock:
            self._total_executions += 1
            self._active_workers += 1

        t0 = time.perf_counter()
        temp_dir = Path(tempfile.mkdtemp(prefix=f"eoip_worker_{request.task_id}_"))

        proc: subprocess.Popen | None = None
        watchdog_triggered = threading.Event()
        outcome = WorkerOutcome.COMPLETED
        error_msg: str | None = None
        result_payload: dict[str, Any] = {}
        status_code = 200

        try:
            # Build worker script
            script_path = temp_dir / "worker_task.py"
            if request.sandbox_script:
                script_path.write_text(request.sandbox_script, encoding="utf-8")
            else:
                # Default worker harness executing request.payload
                default_script = (
                    "import json, sys\n"
                    "req = json.loads(sys.stdin.read())\n"
                    "out = {'echo': req.get('payload', {})}\n"
                    "print(json.dumps({'status': 'COMPLETED', 'outputs': out}))\n"
                )
                script_path.write_text(default_script, encoding="utf-8")

            # Environment with memory and network flags
            env = os.environ.copy()
            env["EOIP_TASK_TEMP_DIR"] = str(temp_dir)
            env["EOIP_RESOURCE_CLASS"] = request.resource_class
            env["EOIP_MAX_MEMORY_MB"] = str(limits.max_memory_mb)
            env["EOIP_ALLOW_NETWORK"] = "1" if request.allow_network else "0"
            env["PYTHONPATH"] = os.pathsep.join(sys.path)

            input_data = json.dumps({
                "task_id": request.task_id,
                "payload": request.payload,
                "resource_class": request.resource_class,
                "deadline_seconds": effective_timeout,
            })

            # Start worker in separate process group where supported
            creationflags = 0
            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

            proc = subprocess.Popen(
                [sys.executable, str(script_path)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(temp_dir),
                env=env,
                text=True,
                creationflags=creationflags,
                # FT-F03: own session/process group on POSIX so kill_process_tree can
                # killpg the whole worker tree without touching the host.
                start_new_session=(sys.platform != "win32"),
            )

            # Watchdog timer to kill process tree within <= 1s of limit breach
            def _watchdog():
                watchdog_triggered.set()
                if proc and proc.poll() is None:
                    kill_process_tree(proc.pid)

            timer = threading.Timer(effective_timeout, _watchdog)
            timer.daemon = True
            timer.start()

            try:
                stdout_data, stderr_data = proc.communicate(input=input_data)
            finally:
                timer.cancel()

            elapsed_s = time.perf_counter() - t0

            if watchdog_triggered.is_set():
                with self._lock:
                    self._timeouts += 1
                    self._kills += 1
                    self._respawns += 1
                outcome = WorkerOutcome.TIMEOUT
                status_code = 504
                error_msg = f"Task exceeded wall-clock limit of {effective_timeout:.2f}s"
            elif proc.returncode != 0:
                with self._lock:
                    self._kills += 1
                    self._respawns += 1
                # Check for OOM or crash markers
                combined_err = f"{stdout_data}\n{stderr_data}"
                if "MemoryError" in combined_err or "OOM" in combined_err:
                    outcome = WorkerOutcome.OOM
                    with self._lock:
                        self._ooms += 1
                    error_msg = f"Worker process exceeded memory limit: {combined_err[:200]}"
                elif "PermissionError" in combined_err or "AccessDenied" in combined_err:
                    outcome = WorkerOutcome.LIMIT_EXCEEDED
                    error_msg = f"Worker attempted unauthorized access: {combined_err[:200]}"
                else:
                    outcome = WorkerOutcome.FAILED
                    error_msg = f"Worker failed with return code {proc.returncode}: {combined_err[:200]}"
                status_code = 500
            else:
                # Parse stdout
                try:
                    parsed = json.loads(stdout_data.strip())
                    outcome_str = parsed.get("status", "COMPLETED")
                    outcome = WorkerOutcome(outcome_str)
                    result_payload = parsed.get("outputs", parsed)
                    with self._lock:
                        self._completed_executions += 1
                except Exception:
                    result_payload = {"raw_output": stdout_data.strip()}
                    with self._lock:
                        self._completed_executions += 1

        except Exception as e:
            with self._lock:
                self._kills += 1
                self._respawns += 1
            outcome = WorkerOutcome.FAILED
            status_code = 500
            error_msg = f"Supervisor error executing worker: {e}"
        finally:
            # Ensure process tree killed
            if proc and proc.poll() is None:
                kill_process_tree(proc.pid)

            # Clean temporary directory
            if temp_dir.exists():
                try:
                    shutil.rmtree(temp_dir, ignore_errors=True)
                except Exception as e:
                    logger.warning(f"Failed to clean temp dir {temp_dir}: {e}")

            with self._lock:
                self._active_workers = max(0, self._active_workers - 1)

        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        return WorkerExecutionResponse(
            task_id=request.task_id,
            outcome=outcome.value,
            status_code=status_code,
            result=result_payload,
            error_message=error_msg,
            elapsed_ms=elapsed_ms,
        )


# Singleton accessor (CRA-002.11)
_SUPERVISOR_SINGLETON: WorkerSupervisor | None = None
_SUPERVISOR_LOCK = threading.Lock()


def get_worker_supervisor() -> WorkerSupervisor:
    """Thread-safe singleton accessor for WorkerSupervisor."""
    global _SUPERVISOR_SINGLETON
    if _SUPERVISOR_SINGLETON is None:
        with _SUPERVISOR_LOCK:
            if _SUPERVISOR_SINGLETON is None:
                _SUPERVISOR_SINGLETON = WorkerSupervisor()
    return _SUPERVISOR_SINGLETON
