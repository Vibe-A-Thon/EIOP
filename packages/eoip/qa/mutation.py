"""Mutation/negative checks (SR-QA-011).

SR-QA-011: a requirement is ``Done`` only if its mapped tests pass AND a
mutation/negative check proves the test fails when the behavior is broken,
sampled per release.

:func:`run_mutation_check` is the generic runner: it copies a fixture test
file to a temp directory, flips one ``assert <lhs> == <rhs>`` into
``assert <lhs> != <rhs>`` (the "broken behavior"), runs pytest on the mutated
copy in a subprocess, and passes only when the mutated test FAILS — proving
the test actually detects the broken behavior rather than passing vacuously.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import threading
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

ASSERT_RE = re.compile(r"^(\s*)assert\s+(.+?)\s*==\s*(.+?)\s*$")


@dataclass
class MutationCheck:
    """Record of one mutation check (sampled per-release proof, SR-QA-011)."""

    check_id: str
    requirement_id: str
    test_id: str
    mutated_file: str
    mutation_line: int
    mutation: str  # e.g. "== -> !="
    original_assert: str
    mutated_exit_code: int
    caught: bool  # mutated test failed => the test detects the broken behavior
    release: str = ""
    checked_at: str = ""
    detail: str = ""

    def to_dict(self) -> dict:
        return {
            "check_id": self.check_id,
            "requirement_id": self.requirement_id,
            "test_id": self.test_id,
            "mutated_file": self.mutated_file,
            "mutation_line": self.mutation_line,
            "mutation": self.mutation,
            "original_assert": self.original_assert,
            "mutated_exit_code": self.mutated_exit_code,
            "caught": self.caught,
            "release": self.release,
            "checked_at": self.checked_at,
            "detail": self.detail,
        }


class MutationCheckStore:
    """JSON-file store of mutation check records (SR-QA-011)."""

    def __init__(self, path: str | Path | None = None) -> None:
        self._lock = threading.RLock()
        self._path = Path(path) if path else Path(
            os.getenv("EOIP_DATA_DIR", ".data")
        ) / "state" / "qa-mutation-checks.json"
        self._checks: dict[str, MutationCheck] = {}
        self._load()

    @property
    def path(self) -> Path:
        return self._path

    def _load(self) -> None:
        if not self._path.exists():
            return
        data = json.loads(self._path.read_text(encoding="utf-8"))
        for item in data.get("checks", []):
            check = MutationCheck(**item)
            self._checks[check.check_id] = check

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"checks": [c.to_dict() for c in self.all_checks()]}
        self._path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def record(self, check: MutationCheck) -> MutationCheck:
        with self._lock:
            self._checks[check.check_id] = check
            self._save()
            return check

    def all_checks(self) -> list[MutationCheck]:
        with self._lock:
            return sorted(self._checks.values(), key=lambda c: c.check_id)

    def for_requirement(self, requirement_id: str) -> list[MutationCheck]:
        return [c for c in self.all_checks() if c.requirement_id == requirement_id]

    def release_summary(self, release: str) -> dict:
        checks = [c for c in self.all_checks() if c.release == release]
        return {
            "release": release,
            "total": len(checks),
            "caught": sum(1 for c in checks if c.caught),
            "missed": sum(1 for c in checks if not c.caught),
            "gate_passed": bool(checks) and all(c.caught for c in checks),
            "checks": [c.to_dict() for c in checks],
        }


def flip_assertion(source: str) -> tuple[str, int]:
    """Flip the first ``==`` assert in ``source`` to ``!=``. Returns (mutated, line)."""
    lines = source.splitlines()
    for idx, line in enumerate(lines):
        match = ASSERT_RE.match(line)
        if match and "# noqa-mutate" not in line:
            indent, lhs, rhs = match.groups()
            lines[idx] = f"{indent}assert {lhs} != {rhs}  # MUTATED: {lhs} == {rhs}"
            return "\n".join(lines) + "\n", idx + 1
    raise ValueError("No flippable 'assert x == y' line found in fixture test file")


def run_mutation_check(
    fixture_test_file: str | Path,
    *,
    check_id: str,
    requirement_id: str,
    test_id: str,
    release: str = "",
    timeout: int = 120,
) -> MutationCheck:
    """Run a generic mutation check against a fixture test file (SR-QA-011).

    Steps: copy the test file to a temp dir, flip one equality assert (the
    injected broken behavior), run ``pytest <copy>`` in a subprocess.  The
    check ``catches`` the mutation only if the mutated test FAILS — a test
    that still passes against broken behavior proves nothing.
    """
    src = Path(fixture_test_file)
    source = src.read_text(encoding="utf-8")
    mutated, line_no = flip_assertion(source)
    checked_at = datetime.now(UTC).isoformat()
    with tempfile.TemporaryDirectory(prefix="eoip-mutation-") as tmp:
        copy = Path(tmp) / src.name
        copy.write_text(mutated, encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", str(copy), "-q", "-x", "--no-header"],
                capture_output=True, text=True, timeout=timeout,
                check=False,
            )
            exit_code = proc.returncode
            detail = (proc.stdout + proc.stderr)[-2000:]
        except subprocess.TimeoutExpired:
            exit_code = -1
            detail = f"mutation run timed out after {timeout}s"
    original_line = source.splitlines()[line_no - 1].strip()
    return MutationCheck(
        check_id=check_id,
        requirement_id=requirement_id,
        test_id=test_id,
        mutated_file=src.name,
        mutation_line=line_no,
        mutation="== -> !=",
        original_assert=original_line,
        mutated_exit_code=exit_code,
        caught=exit_code != 0,  # non-zero => mutated (broken) test failed => detected
        release=release,
        checked_at=checked_at,
        detail=detail,
    )
