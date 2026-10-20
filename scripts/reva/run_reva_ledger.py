#!/usr/bin/env python3
"""Build the REVA Proof-of-Done ledger from a REAL test run (FT-F04 reva-ledger lane).

Replaces scripts/reva/build_reva_ledger.py, which synthesized passing runs and fabricated
review warrants. This runner:

1. runs ``pytest tests/reva`` with the REVA pytest plugin and records JUnit (the only source
   of test outcomes; nothing is synthesized);
2. builds one RunRecord per test depth at the current commit, with the real exit code,
   clean-tree flag, tree digest and environment fingerprint;
3. evaluates every obligation in docs/reva/obligations/reva.yaml with the closure engine.
   An obligation is reviewed only if docs/reva/obligations/reviews.yaml has a human review
   for it (the ``reviewed_warrant_id`` field in reva.yaml is ignored); bindings come only from
   docs/reva/obligations/bindings.yaml; mutation scores only from --mutation-report. Missing
   evidence leaves an obligation open: the ledger never auto-closes anything;
4. writes ledger.json / ledger.md / ledger.html, the run records and the JUnit file to --out
   (and, with --write-docs, regenerates docs/reva/reva-ledger.*).

Exit status is non-zero when the test run fails, produced no tests, or when any obligation
would close without a passing counted test from this run (defence in depth).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import yaml  # noqa: E402

from reva.core.ids import verifier_run_id  # noqa: E402
from reva.core.time import format_ts, utc_now_ms  # noqa: E402
from reva.kernel.authority import Depth  # noqa: E402
from reva.pd.bindings import load_bindings  # noqa: E402
from reva.pd.closure import ClosureContext, evaluate_closure  # noqa: E402
from reva.pd.export_html import render_ledger_html  # noqa: E402
from reva.pd.ledger import build_ledger  # noqa: E402
from reva.pd.obligations import load_obligations, validate_obligations_dag  # noqa: E402
from reva.pd.owner_digest import compute_owner_digest  # noqa: E402
from reva.pd.runs import RunRecord, get_environment_fingerprint  # noqa: E402
from reva.sandbox.collectors import parse_junit_xml  # noqa: E402

OBLIGATIONS = REPO_ROOT / "docs/reva/obligations/reva.yaml"
REVIEWS = REPO_ROOT / "docs/reva/obligations/reviews.yaml"
BINDINGS = REPO_ROOT / "docs/reva/obligations/bindings.yaml"
AUTOMATED_REVIEWERS = {"", "agent", "automation", "ci", "bot", "system", "lead_architect"}
DEPTH_DIRS = {d.value for d in Depth}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO_ROOT, check=True, capture_output=True, text=True).stdout.strip()


def load_reviews(path: Path) -> dict[str, dict]:
    """obligation_key -> review entry, only for reviews by a named human."""
    if not path.exists():
        return {}
    entries = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    reviews = {}
    for entry in entries:
        reviewer = str(entry.get("reviewer", "")).strip()
        if reviewer.lower() in AUTOMATED_REVIEWERS or not entry.get("reviewed_at"):
            continue
        reviews[entry["obligation_key"]] = entry
    return reviews


def test_depth(test_id: str) -> Depth:
    parts = test_id.replace("\\", "/").split("/")
    if len(parts) > 2 and parts[0] == "tests" and parts[1] == "reva" and parts[2] in DEPTH_DIRS:
        return Depth(parts[2])
    return Depth.UNIT  # unknown location: credit the lowest test depth, never more


def run_tests(out: Path, pytest_args: list[str]) -> tuple[int, Path, str, str]:
    junit = out / "reva-ledger-junit.xml"
    cmd = [sys.executable, "-m", "pytest", "tests/reva", "-p", "reva.pd.pytest_plugin",
           f"--junitxml={junit}", "-o", "junit_family=xunit2", *pytest_args]
    print("+", " ".join(cmd), flush=True)
    started = format_ts(utc_now_ms())
    rc = subprocess.call(cmd, cwd=REPO_ROOT)
    return rc, junit, started, format_ts(utc_now_ms())


def build_runs(junit: Path, rc: int, started: str, finished: str, argv: list[str]) -> list[RunRecord]:
    tests = parse_junit_xml(junit.read_bytes())
    commit, tree = git("rev-parse", "HEAD"), git("rev-parse", "HEAD^{tree}")
    clean = git("status", "--porcelain", "--untracked-files=no") == ""
    env = get_environment_fingerprint(REPO_ROOT)
    lock = REPO_ROOT / "requirements.lock"
    if lock.exists():
        env["lockfile_digests"]["requirements.lock"] = hashlib.sha256(lock.read_bytes()).hexdigest()
    artifact = {"name": junit.name, "sha256": hashlib.sha256(junit.read_bytes()).hexdigest()}
    by_depth: dict[Depth, list] = {}
    for t in tests:
        by_depth.setdefault(test_depth(t.test_id), []).append(t)
    runs = []
    for depth, group in sorted(by_depth.items(), key=lambda kv: kv[0].rank):
        body = {
            "argv": argv, "artifacts": [artifact], "binding_digest": "", "clean": clean, "commit": commit,
            "depth": depth.value, "environment": env, "exit_code": rc, "finished_at": finished, "lineage": {},
            "mutation": None, "network": "host", "profile": depth.value, "repo_id": "eiop", "reruns": 1,
            "started_at": started, "tests": [t.to_dict() for t in group], "timed_out": False,
            "tree_digest": tree, "verifier_id": "pytest-tests-reva",
        }
        runs.append(RunRecord(run_id=verifier_run_id(body), verifier_id="pytest-tests-reva", binding_digest="",
                              repo_id="eiop", commit=commit, tree_digest=tree, clean=clean, environment=env,
                              profile=depth.value, depth=depth, network="host", argv=argv, started_at=started,
                              finished_at=finished, exit_code=rc, timed_out=False, lineage={},
                              artifacts=[artifact], tests=group, reruns=1))
    return runs


def current_digests(bindings) -> dict[str, str]:
    digests = {}
    for b in bindings:
        for owner in b.owners:
            path = REPO_ROOT / owner.path
            if path.is_file():
                res = compute_owner_digest(path.read_text(encoding="utf-8"), symbol=owner.symbol)
                if res.digest:
                    digests[f"{owner.path}::{owner.symbol}"] = res.digest
    return digests


def evaluate(obligations, bindings, reviews, runs, commit, mutation_scores):
    by_key = {b.obligation_key: b for b in bindings}
    digests = current_digests(bindings)
    outcomes: dict[str, str] = {}
    decisions = []
    pending = list(obligations)
    while pending:  # dependencies first (the DAG was validated)
        progressed = False
        for ob in list(pending):
            if any(dep not in outcomes for dep in ob.dependencies if dep in {o.key for o in obligations}):
                continue
            review = reviews.get(ob.key)
            ob = ob.model_copy(update={"reviewed_warrant_id": review.get("warrant_id") or f"review:{review['reviewer']}"
                                       if review else None})
            ctx = ClosureContext(obligation=ob, binding=by_key.get(ob.key), commit=commit,
                                 current_owner_digests=digests, runs=runs,
                                 dependency_outcomes=dict(outcomes), mutation_scores=mutation_scores)
            decision = evaluate_closure(ctx)
            outcomes[ob.key] = decision.outcome
            decisions.append(decision)
            pending.remove(next(p for p in pending if p.key == ob.key))
            progressed = True
        if not progressed:
            raise SystemExit("obligation dependency cycle")
    return decisions


def assert_no_unearned_closure(decisions, runs) -> list[str]:
    """Defence in depth: a closed obligation must have a passing, marked test in THIS run."""
    passed_keys = {k for r in runs if r.exit_code == 0 for t in r.tests if t.outcome == "passed"
                   for k in t.obligation_keys}
    return [d.obligation_key for d in decisions if d.outcome == "closed" and d.obligation_key not in passed_keys]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "test-results" / "reva-ledger")
    parser.add_argument("--write-docs", action="store_true", help="regenerate docs/reva/reva-ledger.*")
    parser.add_argument("--mutation-report", type=Path, default=None,
                        help="JSON from scripts/reva/run_mutation.py; owner_digest -> score is used for AG-04")
    parser.add_argument("pytest_args", nargs="*")
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)

    rc, junit, started, finished = run_tests(args.out, args.pytest_args)
    if not junit.exists():
        print(f"::error::reva-ledger: pytest produced no JUnit report (exit {rc}); no ledger written")
        return rc or 1
    runs = build_runs(junit, rc, started, finished, ["pytest", "tests/reva", *args.pytest_args])
    commit = git("rev-parse", "HEAD")
    obligations = load_obligations(OBLIGATIONS)
    validate_obligations_dag(obligations)
    bindings = load_bindings(BINDINGS) if BINDINGS.exists() else []
    reviews = load_reviews(REVIEWS)
    mutation_scores = {}
    if args.mutation_report and args.mutation_report.exists():
        report = json.loads(args.mutation_report.read_text(encoding="utf-8"))
        mutation_scores = {k: float(v) for k, v in report.get("owner_scores", {}).items()}
    decisions = evaluate(obligations, bindings, reviews, runs, commit, mutation_scores)
    unearned = assert_no_unearned_closure(decisions, runs)

    ledger = build_ledger("eiop", "reva", commit, decisions)
    payload = ledger.canonical_dict()
    total_tests = sum(len(r.tests) for r in runs)
    outcome_counts = Counter(t.outcome for r in runs for t in r.tests)
    marked = sorted({k for r in runs for t in r.tests for k in t.obligation_keys})
    payload["evidence"] = {
        "source": "real pytest run (scripts/reva/run_reva_ledger.py); nothing synthesized",
        "pytest_exit_code": rc,
        "tests": total_tests,
        "test_outcomes": dict(sorted(outcome_counts.items())),
        "obligations_with_marked_tests": marked,
        "reviews_file": REVIEWS.relative_to(REPO_ROOT).as_posix() if REVIEWS.exists() else None,
        "human_reviews": len(reviews),
        "bindings": len(bindings),
        "mutation_scores": len(mutation_scores),
        "signed": False,
        "run_ids": [r.run_id for r in runs],
    }
    md = ledger.to_markdown()
    md = md.replace("# REVA Proof-of-Done Ledger", "# REVA Proof-of-Done Ledger\n\n"
                    "> Generated by `scripts/reva/run_reva_ledger.py` from a real `pytest tests/reva` run at "
                    f"`{commit}`: {total_tests} tests, exit code {rc}. An obligation closes only with a human "
                    "review, a binding, passing marked tests from this run and the anti-gaming checks; "
                    "otherwise it stays open. The ledger is unsigned.", 1)
    html = render_ledger_html(ledger)
    (args.out / "ledger.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.out / "ledger.md").write_text(md + "\n", encoding="utf-8")
    (args.out / "ledger.html").write_text(html, encoding="utf-8")
    (args.out / "runs.json").write_text(json.dumps([r.canonical_dict() | {"run_id": r.run_id} for r in runs],
                                                   indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_docs:
        docs = REPO_ROOT / "docs" / "reva"
        (docs / "reva-ledger.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (docs / "reva-ledger.md").write_text(md + "\n", encoding="utf-8")
        (docs / "reva-ledger.html").write_text(html, encoding="utf-8")

    print(f"reva-ledger: {total_tests} tests ({dict(outcome_counts)}), pytest exit {rc}")
    print(f"reva-ledger: obligations {dict(ledger.summary)} of {len(decisions)}; "
          f"{len(marked)} obligation key(s) have marked tests; {len(reviews)} human review(s); "
          f"{len(bindings)} binding(s)")
    problems = []
    if rc != 0:
        problems.append(f"the test run failed (pytest exit {rc})")
    if total_tests == 0:
        problems.append("the test run produced zero tests")
    if unearned:
        problems.append(f"closed without a passing marked test in this run: {unearned}")
    for problem in problems:
        print(f"::error::reva-ledger: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
