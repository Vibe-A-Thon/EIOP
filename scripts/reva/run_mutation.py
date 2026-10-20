#!/usr/bin/env python3
"""REVA mutation lane (FT-F04, REVA-PD-005 / AG-04 / NFR-019).

For each target (file, symbol, tests) the REVA AST mutation engine generates deterministic
mutants of that symbol. Each mutant is written into a scratch copy of the repository (the
checkout is never modified) and the target's tests run against it: a failing run kills the
mutant, a passing run means it survived, a timeout counts as killed-by-timeout. The lane fails
when any target scores below --threshold, when a target produced no mutants, or when the
unmutated baseline fails (a red baseline would make every mutant look killed).

Writes test-results/reva-mutation.json with per-target results, surviving mutant ids and
``owner_scores`` (owner digest -> score) for scripts/reva/run_reva_ledger.py --mutation-report.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from reva.pd.mutation import generate_mutants  # noqa: E402
from reva.pd.owner_digest import compute_owner_digest  # noqa: E402

# (path, symbol, tests that own it). Kept small and strong: these are the guards the
# remediation relies on (closure never auto-closes, gap FSM, valid-time split, proofs, inventory).
TARGETS = [
    ("reva/pd/closure.py", "evaluate_closure", ["tests/reva/unit/pd", "tests/reva/acceptance"]),
    ("reva/kernel/gaps.py", "_apply_transition", ["tests/reva/acceptance"]),
    ("reva/kernel/gaps.py", "update_gap", ["tests/reva/acceptance", "tests/reva/unit/kernel/test_guard_boundaries.py"]),
    ("reva/kernel/contradictions.py", "_valid_times_overlap", ["tests/reva/acceptance", "tests/reva/unit/kernel"]),
    ("reva/kernel/translog.py", "verify_inclusion", ["tests/reva/component", "tests/reva/unit/kernel"]),
    ("reva/kernel/translog.py", "_path", ["tests/reva/component", "tests/reva/perf/test_tl.py"]),
    ("reva/extract/artifacts/inventory.py", "validate_member_path", ["tests/reva/integration/test_archive_fixtures.py",
                                                                      "tests/reva/unit/kernel/test_guard_boundaries.py"]),
]
COPY_DIRS = ["reva", "tests/reva", "packages", "apps", "scripts/reva"]
COPY_FILES = ["pyproject.toml", "tests/_principals.py", "tests/__init__.py"]


def make_scratch() -> Path:
    scratch = Path(tempfile.mkdtemp(prefix="reva-mutation-"))
    for d in COPY_DIRS:
        if (REPO_ROOT / d).exists():
            shutil.copytree(REPO_ROOT / d, scratch / d, ignore=shutil.ignore_patterns("__pycache__"))
    for f in COPY_FILES:
        if (REPO_ROOT / f).exists():
            (scratch / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO_ROOT / f, scratch / f)
    return scratch


def run_tests(scratch: Path, tests: list[str], timeout: int) -> str:
    env = dict(os.environ, PYTHONPATH=f"{scratch}{os.pathsep}{scratch / 'packages'}{os.pathsep}{scratch / 'tests'}",
               PYTHONDONTWRITEBYTECODE="1", REVA_PERF_RESULTS=str(scratch / "perf.json"))
    cmd = [sys.executable, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", "-o", "addopts=",
           "--rootdir", str(scratch), *tests]
    try:
        rc = subprocess.run(cmd, cwd=scratch, env=env, capture_output=True, timeout=timeout).returncode
    except subprocess.TimeoutExpired:
        return "timeout"
    return "passed" if rc == 0 else "failed"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=0.75, help="NFR-019 minimum score per target")
    parser.add_argument("--max-mutants", type=int, default=40)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "test-results" / "reva-mutation.json")
    args = parser.parse_args(argv)

    scratch = make_scratch()
    results, owner_scores, problems = [], {}, []
    try:
        for path, symbol, tests in TARGETS:
            original = (REPO_ROOT / path).read_text(encoding="utf-8")
            target = scratch / path
            baseline = run_tests(scratch, tests, args.timeout)
            if baseline != "passed":
                problems.append(f"{path}::{symbol}: baseline tests did not pass ({baseline})")
                continue
            mutants = generate_mutants(original, symbol, max_mutants=args.max_mutants, seed="reva")
            killed, survived, timeouts = 0, [], 0
            for site_id, mutated in mutants:
                target.write_text(mutated, encoding="utf-8")
                outcome = run_tests(scratch, tests, args.timeout)
                if outcome == "failed":
                    killed += 1
                elif outcome == "timeout":
                    timeouts += 1
                else:
                    survived.append(site_id)
            target.write_text(original, encoding="utf-8")
            total = len(mutants)
            score = (killed + timeouts) / total if total else 0.0
            digest = compute_owner_digest(original, symbol=symbol).digest
            if digest:
                owner_scores[digest] = round(score, 4)
            results.append({"path": path, "symbol": symbol, "tests": tests, "generated": total, "killed": killed,
                            "timeout": timeouts, "survived": survived, "score": round(score, 4),
                            "owner_digest": digest})
            print(f"{path}::{symbol}: {killed + timeouts}/{total} killed, score {score:.2f}"
                  + (f", survivors {survived}" if survived else ""), flush=True)
            if total == 0:
                problems.append(f"{path}::{symbol}: no mutants generated (symbol not found?)")
            elif score < args.threshold:
                problems.append(f"{path}::{symbol}: score {score:.2f} < {args.threshold}")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"threshold": args.threshold, "targets": results, "owner_scores": owner_scores,
                                    "problems": problems}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for problem in problems:
        print(f"::error::reva-mutation: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
