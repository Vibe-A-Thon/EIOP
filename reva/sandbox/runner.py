"""Subprocess sandbox runner with isolation, limits, and output caps (T-203 / REVA-VS-003 / REVA-VS-005)."""

from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from reva.sandbox.limits import SandboxLimits, apply_rlimits
from reva.sandbox.lineage import LineageRecord, LineageTracker


@dataclass
class RunSpec:
    """Invocation specification for sandboxed execution."""

    argv: List[str]
    cwd: str = "."
    env_allow: List[str] = field(default_factory=list)
    extra_env: Dict[str, str] = field(default_factory=dict)
    limits: SandboxLimits = field(default_factory=SandboxLimits)
    network: str = "none"  # none | loopback | compose
    timeout_s: int = 900
    stdout_cap: int = 16 * 1024 * 1024
    stderr_cap: int = 16 * 1024 * 1024
    cancel_token: Optional[threading.Event] = None


@dataclass
class RunOutcome:
    """Execution results and evidence."""

    exit_code: int
    timed_out: bool
    cancelled: bool
    stdout: bytes
    stderr: bytes
    stdout_truncated: bool
    stderr_truncated: bool
    lineage: LineageRecord
    duration_ms: int


class StreamCapper(threading.Thread):
    """Reads a stream up to max_bytes, dropping subsequent bytes and tracking truncation."""

    def __init__(self, stream, max_bytes: int):
        super().__init__()
        self.stream = stream
        self.max_bytes = max_bytes
        self.buffer = bytearray()
        self.truncated = False
        self.dropped_bytes = 0

    def run(self):
        try:
            while True:
                chunk = self.stream.read(65536)
                if not chunk:
                    break
                remaining = self.max_bytes - len(self.buffer)
                if remaining > 0:
                    self.buffer.extend(chunk[:remaining])
                    if len(chunk) > remaining:
                        self.truncated = True
                        self.dropped_bytes += len(chunk) - remaining
                else:
                    self.truncated = True
                    self.dropped_bytes += len(chunk)
        except Exception:
            pass
        finally:
            try:
                self.stream.close()
            except Exception:
                pass


class ProcessSandbox:
    """Executes commands in an isolated subprocess with resource bounds."""

    @staticmethod
    def build_sanitized_env(spec: RunSpec, run_root: Path) -> Dict[str, str]:
        """Construct sanitized environment with minimal standard variables."""
        home_dir = run_root / "home"
        tmp_dir = run_root / "tmp"
        home_dir.mkdir(parents=True, exist_ok=True)
        tmp_dir.mkdir(parents=True, exist_ok=True)

        env: Dict[str, str] = {
            "HOME": str(home_dir),
            "TMPDIR": str(tmp_dir),
            "TEMP": str(tmp_dir),
            "TMP": str(tmp_dir),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PATH": os.environ.get("PATH", ""),
            "PYTHONUNBUFFERED": "1",
        }

        # Pass through allowed variables from parent
        for k in spec.env_allow:
            if k in os.environ:
                env[k] = os.environ[k]

        # Apply explicitly provided extra variables
        env.update(spec.extra_env)
        return env

    @classmethod
    def run(cls, spec: RunSpec) -> RunOutcome:
        """Run the specified command under process isolation."""
        run_root = Path(spec.cwd) / ".reva_run"
        run_root.mkdir(parents=True, exist_ok=True)
        clean_env = cls.build_sanitized_env(spec, run_root)

        preexec = None
        creationflags = 0
        if sys.platform != "win32":
            def _preexec():
                os.setsid()
                apply_rlimits(spec.limits)

            preexec = _preexec
        else:
            # CREATE_NEW_PROCESS_GROUP
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

        start_time = time.monotonic()
        proc = subprocess.Popen(
            spec.argv,
            cwd=spec.cwd,
            env=clean_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=preexec,
            creationflags=creationflags,
        )

        tracker = LineageTracker(proc.pid)
        stdout_capper = StreamCapper(proc.stdout, spec.stdout_cap)
        stderr_capper = StreamCapper(proc.stderr, spec.stderr_cap)
        stdout_capper.start()
        stderr_capper.start()

        timed_out = False
        cancelled = False
        deadline = start_time + spec.timeout_s

        while proc.poll() is None:
            if spec.cancel_token and spec.cancel_token.is_set():
                cancelled = True
                tracker.terminate_group()
                break

            if time.monotonic() > deadline:
                timed_out = True
                tracker.terminate_group()
                break

            time.sleep(0.05)

        try:
            proc.wait(timeout=2.0)
        except subprocess.TimeoutExpired:
            tracker.terminate_group()

        stdout_capper.join(timeout=2.0)
        stderr_capper.join(timeout=2.0)

        duration_ms = int((time.monotonic() - start_time) * 1000)
        exit_code = proc.returncode if proc.returncode is not None else -1

        lineage_record = tracker.build_record()

        return RunOutcome(
            exit_code=exit_code,
            timed_out=timed_out,
            cancelled=cancelled,
            stdout=bytes(stdout_capper.buffer),
            stderr=bytes(stderr_capper.buffer),
            stdout_truncated=stdout_capper.truncated,
            stderr_truncated=stderr_capper.truncated,
            lineage=lineage_record,
            duration_ms=duration_ms,
        )
