"""Lint/policy gate runner (SR-QA-014, report-only).

SR-QA-014: linters/type-checkers/security scanners run at zero-error policy
on main — the prior baseline carried 165 lint errors, mostly mechanical.

:func:`PolicyGate.run` executes ``ruff check`` in a subprocess over the
repository (tolerant when ruff is unavailable: reports ``skipped`` rather
than failing) and records whether the zero-error policy holds.  The gate is
report-only: it records and exposes status, it does not mutate code.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import threading
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass
class PolicyGateResult:
    """Result of one policy-gate run."""

    run_id: str
    tool: str
    command: list[str]
    available: bool
    skipped: bool
    exit_code: int
    error_count: int
    zero_error_policy_met: bool
    report_only: bool = True
    checked_at: str = ""
    summary: str = ""

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "tool": self.tool,
            "command": self.command,
            "available": self.available,
            "skipped": self.skipped,
            "exit_code": self.exit_code,
            "error_count": self.error_count,
            "zero_error_policy_met": self.zero_error_policy_met,
            "report_only": self.report_only,
            "checked_at": self.checked_at,
            "summary": self.summary,
        }


class PolicyGate:
    """Runs ``ruff check`` (subprocess, tolerant of absence) and records status."""

    def __init__(self, repo_root: str | Path | None = None,
                 path: str | Path | None = None, tool: str = "ruff") -> None:
        self.repo_root = Path(repo_root) if repo_root else Path(__file__).resolve().parents[3]
        self._lock = threading.RLock()
        self._path = Path(path) if path else Path(
            os.getenv("EOIP_DATA_DIR", ".data")
        ) / "state" / "qa-policy-gate.json"
        self.tool = tool
        self._history: list[PolicyGateResult] = []
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            return
        data = json.loads(self._path.read_text(encoding="utf-8"))
        self._history = [PolicyGateResult(**item) for item in data.get("runs", [])]

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"runs": [r.to_dict() for r in self._history[-100:]]}
        self._path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def run(self, *, paths: list[str] | None = None, run_id: str = "") -> PolicyGateResult:
        """Execute the policy tool and record zero-error status (report-only)."""
        exe = shutil.which(self.tool)
        checked_at = datetime.now(UTC).isoformat()
        if exe is None:
            result = PolicyGateResult(
                run_id=run_id or f"policy-{checked_at}",
                tool=self.tool,
                command=[],
                available=False,
                skipped=True,
                exit_code=0,
                error_count=0,
                zero_error_policy_met=False,  # not evaluated => not "met"
                checked_at=checked_at,
                summary=f"{self.tool} not available on PATH; gate skipped (tolerant mode)",
            )
        else:
            targets = paths or ["packages", "apps/api", "apps/mcp", "tests"]
            cmd = [exe, "check", "--output-format", "json", *targets]
            try:
                proc = subprocess.run(
                    cmd, cwd=str(self.repo_root), capture_output=True, text=True, timeout=300,
                    check=False,
                )
                error_count = _count_ruff_errors(proc.stdout)
                result = PolicyGateResult(
                    run_id=run_id or f"policy-{checked_at}",
                    tool=self.tool,
                    command=cmd,
                    available=True,
                    skipped=False,
                    exit_code=proc.returncode,
                    error_count=error_count,
                    zero_error_policy_met=proc.returncode == 0 and error_count == 0,
                    checked_at=checked_at,
                    summary=f"{self.tool}: {error_count} error(s), exit {proc.returncode}",
                )
            except subprocess.TimeoutExpired:
                result = PolicyGateResult(
                    run_id=run_id or f"policy-{checked_at}",
                    tool=self.tool,
                    command=cmd,
                    available=True,
                    skipped=True,
                    exit_code=-1,
                    error_count=0,
                    zero_error_policy_met=False,
                    checked_at=checked_at,
                    summary=f"{self.tool} timed out after 300s; gate skipped",
                )
        with self._lock:
            self._history.append(result)
            self._save()
            return result

    def latest(self) -> PolicyGateResult | None:
        with self._lock:
            return self._history[-1] if self._history else None

    def history(self) -> list[PolicyGateResult]:
        with self._lock:
            return list(self._history)


def _count_ruff_errors(stdout: str) -> int:
    """Count errors in ruff's JSON output (tolerant of empty/garbled output)."""
    text = (stdout or "").strip()
    if not text:
        return 0
    try:
        data: Any = json.loads(text)
    except json.JSONDecodeError:
        return 0
    if isinstance(data, list):
        return sum(1 for item in data if isinstance(item, dict))
    if isinstance(data, dict):
        # "ruff check --output-format json" can emit {"results": [...]} shapes
        results = data.get("results") or data.get("diagnostics") or []
        return len(results)
    return 0
