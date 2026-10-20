#!/usr/bin/env python3
"""Run one REVA CI lane's pytest selection and refuse zero-test success (FT-F04).

Usage: python scripts/reva/run_lane.py <lane> [--min-passed N] -- <pytest args...>

Writes test-results/reva-<lane>.xml (JUnit) and test-results/reva-<lane>-summary.json. The lane
fails when pytest fails, when nothing passed (an empty or fully skipped selection is not
evidence), or when fewer than --min-passed tests passed. Every skip is listed with its reason
so unavailable authority is named instead of silently counted as green.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def summarize_junit(path: Path) -> dict:
    """Count outcomes per test case from a JUnit XML file."""
    passed, failed, skipped = [], [], []
    root = ET.parse(path).getroot()
    for case in root.iter("testcase"):
        name = f"{case.get('classname', '')}::{case.get('name', '')}"
        if case.find("failure") is not None or case.find("error") is not None:
            failed.append(name)
        elif case.find("skipped") is not None:
            reason = case.find("skipped").get("message", "")
            skipped.append({"test": name, "reason": reason})
        else:
            passed.append(name)
    return {"passed": passed, "failed": failed, "skipped": skipped}


def evaluate(summary: dict, pytest_rc: int, min_passed: int) -> list[str]:
    """Return the reasons the lane must fail (empty list means the lane passed)."""
    problems = []
    if pytest_rc not in (0, 5):
        problems.append(f"pytest exited with {pytest_rc}")
    if summary["failed"]:
        problems.append(f"{len(summary['failed'])} test(s) failed or errored")
    if not summary["passed"]:
        problems.append("zero tests passed: an empty or fully skipped lane is not evidence")
    elif len(summary["passed"]) < min_passed:
        problems.append(f"only {len(summary['passed'])} test(s) passed; the lane requires {min_passed}")
    return problems


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--" not in argv:
        print("usage: run_lane.py <lane> [--min-passed N] -- <pytest args>", file=sys.stderr)
        return 2
    split = argv.index("--")
    parser = argparse.ArgumentParser()
    parser.add_argument("lane")
    parser.add_argument("--min-passed", type=int, default=1)
    args = parser.parse_args(argv[:split])
    pytest_args = argv[split + 1:]

    out_dir = REPO_ROOT / "test-results"
    out_dir.mkdir(exist_ok=True)
    junit = out_dir / f"reva-{args.lane}.xml"
    if junit.exists():
        junit.unlink()
    cmd = [sys.executable, "-m", "pytest", *pytest_args, f"--junitxml={junit}", "-o", "junit_family=xunit2"]
    print("+", " ".join(cmd), flush=True)
    rc = subprocess.call(cmd, cwd=REPO_ROOT)
    if not junit.exists():
        print(f"::error::reva-{args.lane}: pytest produced no JUnit report (exit {rc})")
        return rc or 1
    summary = summarize_junit(junit)
    problems = evaluate(summary, rc, args.min_passed)
    summary.update({"lane": args.lane, "pytest_exit_code": rc, "problems": problems})
    (out_dir / f"reva-{args.lane}-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"reva-{args.lane}: {len(summary['passed'])} passed, {len(summary['failed'])} failed, "
          f"{len(summary['skipped'])} skipped")
    for skip in summary["skipped"]:
        print(f"  SKIPPED {skip['test']}: {skip['reason']}")
    for problem in problems:
        print(f"::error::reva-{args.lane}: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
