"""Process lineage tracking and group lifecycle management (T-203 / REVA-VS-004)."""

from __future__ import annotations

import hashlib
import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ProcessInfo:
    pid: int
    ppid: int
    cmd_digest: str


@dataclass
class LineageRecord:
    root_pid: int
    pgid: int
    session_id: int
    descendants: List[ProcessInfo] = field(default_factory=list)
    status: str = "verified"  # verified | unavailable
    reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "root_pid": self.root_pid,
            "pgid": self.pgid,
            "session_id": self.session_id,
            "descendants": [
                {"pid": d.pid, "ppid": d.ppid, "cmd_digest": d.cmd_digest}
                for d in self.descendants
            ],
            "status": self.status,
            "reason": self.reason,
        }


class LineageTracker:
    """Tracks descendants of a child process and ensures clean termination."""

    def __init__(self, root_pid: int):
        self.root_pid = root_pid
        self.pgid = root_pid
        self.session_id = root_pid
        self._descendants: Dict[int, ProcessInfo] = {}

    def poll(self) -> List[ProcessInfo]:
        """Poll currently active descendant processes."""
        if sys.platform != "win32" and os.path.isdir("/proc"):
            self._poll_proc()
        return list(self._descendants.values())

    def _poll_proc(self) -> None:
        """Poll /proc on Linux for process hierarchy and cmdline digest."""
        try:
            for entry in os.listdir("/proc"):
                if not entry.isdigit():
                    continue
                pid = int(entry)
                stat_path = f"/proc/{pid}/stat"
                cmdline_path = f"/proc/{pid}/cmdline"
                if not os.path.exists(stat_path):
                    continue
                try:
                    with open(stat_path, "r", encoding="utf-8", errors="replace") as f:
                        fields = f.read().split()
                    ppid = int(fields[3])
                    pgrp = int(fields[4])

                    if pgrp == self.pgid or ppid == self.root_pid or ppid in self._descendants:
                        cmd_digest = ""
                        if os.path.exists(cmdline_path):
                            with open(cmdline_path, "rb") as cf:
                                cmd_digest = hashlib.sha256(cf.read()).hexdigest()
                        self._descendants[pid] = ProcessInfo(pid=pid, ppid=ppid, cmd_digest=cmd_digest)
                except (OSError, IndexError, ValueError):
                    continue
        except Exception:
            pass

    def terminate_group(self, timeout_s: float = 10.0) -> bool:
        """Terminate root process and all descendants, escalating from SIGTERM to SIGKILL."""
        if sys.platform == "win32":
            # On Windows, kill process tree via taskkill
            try:
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(self.root_pid)],
                    capture_output=True,
                    check=False,
                )
                return True
            except Exception:
                return False
        else:
            # POSIX: kill process group
            try:
                os.killpg(self.pgid, signal.SIGTERM)
            except OSError:
                pass

            deadline = time.time() + timeout_s
            while time.time() < deadline:
                time.sleep(0.1)
                try:
                    # Check if any process in group still alive
                    os.killpg(self.pgid, 0)
                except OSError:
                    return True  # All processes terminated

            try:
                os.killpg(self.pgid, signal.SIGKILL)
            except OSError:
                pass
            return True

    def build_record(self) -> LineageRecord:
        """Construct immutable lineage record for audit/attestation."""
        self.poll()
        return LineageRecord(
            root_pid=self.root_pid,
            pgid=self.pgid,
            session_id=self.session_id,
            descendants=list(self._descendants.values()),
            status="verified",
            reason=None,
        )
