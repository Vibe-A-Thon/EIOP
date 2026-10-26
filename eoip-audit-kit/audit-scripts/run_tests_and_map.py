#!/usr/bin/env python3
"""Detect and run tests safely; map junit results to requirements; write missing_tests.json.

Safety: --isolate copies the repo to a temp dir so tests never write into the audited clone.
Never hard-fails: a missing runner or failing suite is recorded, exit code is 0.
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

ID_RE = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d{1,5}\b")


def load_req_ids(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    reqs = data.get("requirements") or data
    if isinstance(reqs, dict):
        return list(reqs.keys())
    return [r["id"] for r in reqs]


def run_cmd(cmd: list[str], cwd: Path, timeout: int) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except FileNotFoundError:
        return 127, f"command not found: {cmd[0]}"
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b"")
        out = out.decode(errors="replace") if isinstance(out, bytes) else (out or "")
        return 124, out + f"\nTIMEOUT after {timeout}s"


def parse_junit(junit: Path) -> list[dict]:
    if not junit.is_file():
        return []
    try:
        tree = ET.parse(junit)
    except ET.ParseError:
        return []
    cases = []
    for tc in tree.iter("testcase"):
        failed = tc.find("failure") is not None or tc.find("error") is not None
        skipped = tc.find("skipped") is not None
        cases.append({
            "name": tc.get("name") or "",
            "classname": tc.get("classname") or "",
            "file": tc.get("file") or "",
            "status": "failed" if failed else ("skipped" if skipped else "passed"),
            "mapped_requirements": [],
        })
    return cases


def nodeid_to_key(nodeid: str) -> str:
    """tests/unit/test_x.py::Cls::test_fn[param] -> tests.unit.test_x.Cls::test_fn"""
    parts = nodeid.split("::")
    mod = parts[0].removesuffix(".py").replace("/", ".").replace("\\", ".")
    rest = parts[1:]
    if not rest:
        return mod
    fn = re.sub(r"\[.*\]$", "", rest[-1])
    cls = ".".join([mod] + rest[:-1])
    return f"{cls}::{fn}"


_PARAM_SUFFIX_RE = re.compile(r"\[.*\]$")


def case_key(c: dict) -> str:
    # Strip pytest parametrization ids. Kept outside the f-string: a backslash
    # inside an f-string expression is a SyntaxError before Python 3.12.
    name = _PARAM_SUFFIX_RE.sub("", c["name"])
    return f"{c['classname']}::{name}"


def build_marker_index(root: Path, id_set: set[str]) -> dict[str, set[str]]:
    """Map test module (dotted) -> REQ ids referenced in that file (markers, comments)."""
    idx: dict[str, set[str]] = {}
    tests_dir = root / "tests"
    base = tests_dir if tests_dir.is_dir() else root
    for p in base.rglob("test_*.py"):
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        found = set(ID_RE.findall(text)) & id_set
        if found:
            mod = str(p.relative_to(root)).removesuffix(".py").replace("/", ".")
            idx[mod] = found
    return idx


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", required=True, type=Path)
    ap.add_argument("--requirements", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--commit", default="")
    ap.add_argument("--python", default=sys.executable, help="Interpreter with the repo's deps installed")
    ap.add_argument("--pytest-args", default="-q -p no:cacheprovider", help="Extra pytest args (quoted string)")
    ap.add_argument("--timeout", type=int, default=900, help="Wall-clock seconds for the whole pytest run")
    ap.add_argument("--isolate", action="store_true", help="Run tests in a temp copy of the repo")
    ap.add_argument("--test-map", type=Path, default=None, help="JSON {req_id: [pytest nodeids]} from the repo")
    ap.add_argument("--reuse-junit", action="store_true", help="Skip running; re-map an existing <out>/tests.xml")
    ap.add_argument("--npm", action="store_true", help="Also run npm test if package.json exists (off by default)")
    args = ap.parse_args()

    root = args.repo_root.resolve()
    out_dir = args.out.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    req_ids = load_req_ids(args.requirements)
    id_set = set(req_ids)

    summary = {"commit": args.commit or None, "runners_tried": [], "exit_codes": {}, "notes": [],
               "python": args.python, "pytest_args": args.pytest_args, "isolated": args.isolate}
    junit_path = out_dir / "tests.xml"
    cases: list[dict] = []

    run_root = root
    tmp = None
    if args.isolate:
        tmp = Path(tempfile.mkdtemp(prefix="eoip-testrun-"))
        run_root = tmp / root.name
        shutil.copytree(root, run_root, ignore=shutil.ignore_patterns(".git", "node_modules", ".venv"))
        summary["notes"].append(f"Tests ran in isolated copy {run_root}")

    has_py_tests = (root / "pytest.ini").exists() or (root / "pyproject.toml").exists() or any(root.glob("tests/**/test_*.py"))
    if args.reuse_junit and junit_path.is_file():
        prev = out_dir / "summary.json"
        if prev.is_file():
            old = json.loads(prev.read_text(encoding="utf-8"))
            for k in ("runners_tried", "exit_codes", "command", "pytest_tail", "isolated"):
                if k in old:
                    summary[k] = old[k]
        summary["notes"].append("Re-mapped existing junit (no re-run)")
        cases = parse_junit(junit_path)
    elif has_py_tests:
        probe, _ = run_cmd([args.python, "-c", "import pytest"], run_root, 60)
        if probe == 0:
            cmd = [args.python, "-m", "pytest", *shlex.split(args.pytest_args), f"--junitxml={junit_path}"]
            summary["command"] = " ".join(cmd)
            code, log = run_cmd(cmd, run_root, args.timeout)
            summary["runners_tried"].append("pytest")
            summary["exit_codes"]["pytest"] = code
            (out_dir / "pytest.log").write_text(log, encoding="utf-8")
            tail = [ln for ln in log.splitlines() if re.search(r"\b(passed|failed|error)\b", ln)]
            summary["pytest_tail"] = tail[-3:]
            cases = parse_junit(junit_path)
        else:
            summary["notes"].append("pytest not importable by --python; skipped")
    else:
        summary["notes"].append("No pytest-style tests detected")

    if (root / "package.json").exists():
        if args.npm and shutil.which("npm"):
            code, log = run_cmd(["npm", "test", "--silent"], run_root, args.timeout)
            summary["runners_tried"].append("npm test")
            summary["exit_codes"]["npm_test"] = code
            (out_dir / "npm_test.log").write_text(log, encoding="utf-8")
        else:
            summary["notes"].append("npm test not run (pass --npm to enable)")

    # Mapping: (1) repo test map, (2) REQ ids referenced in test files, (3) id in test name
    test_map = {}
    if args.test_map and args.test_map.is_file():
        test_map = json.loads(args.test_map.read_text(encoding="utf-8"))
    key_to_reqs: dict[str, set[str]] = defaultdict(set)
    for rid, nodeids in test_map.items():
        for nid in nodeids or []:
            key_to_reqs[nodeid_to_key(nid)].add(rid)
    marker_idx = build_marker_index(root, id_set)

    for c in cases:
        mapped = set(key_to_reqs.get(case_key(c), set()))
        mod = c["classname"]
        while mod:
            if mod in marker_idx:
                mapped |= marker_idx[mod]
                break
            mod = mod.rpartition(".")[0]
        mapped |= set(ID_RE.findall(c["classname"] + " " + c["name"])) & id_set
        c["mapped_requirements"] = sorted(mapped)

    per_req: dict[str, dict] = {}
    for c in cases:
        for rid in c["mapped_requirements"]:
            s = per_req.setdefault(rid, {"passed": 0, "failed": 0, "skipped": 0, "tests": []})
            s[c["status"]] += 1
            if len(s["tests"]) < 10:
                s["tests"].append(case_key(c))
    covered = {r for r, s in per_req.items() if s["passed"] and not s["failed"]}
    missing = sorted(id_set - set(per_req))
    summary["counts"] = {
        "cases": len(cases),
        "passed": sum(c["status"] == "passed" for c in cases),
        "failed": sum(c["status"] == "failed" for c in cases),
        "skipped": sum(c["status"] == "skipped" for c in cases),
        "requirements_with_passing_tests_only": len(covered),
        "requirements_with_any_failure": sum(1 for s in per_req.values() if s["failed"]),
        "requirements_without_mapped_tests": len(missing),
        "test_map_entries": len(test_map),
    }

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (out_dir / "per_requirement.json").write_text(json.dumps(per_req, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "failed_cases.json").write_text(
        json.dumps([c for c in cases if c["status"] == "failed"], indent=2) + "\n", encoding="utf-8")
    missing_path = (out_dir.parent if out_dir.name == "test_results" else out_dir) / "missing_tests.json"
    missing_path.write_text(json.dumps({
        "commit": args.commit or None,
        "count": len(missing),
        "missing_requirement_ids": missing,
        "note": "No executed test case mapped to these ids (via test map, in-file id references, or test names).",
    }, indent=2) + "\n", encoding="utf-8")

    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"Runners: {summary['runners_tried'] or 'none'}; counts: {summary['counts']}")
    print(f"Wrote {out_dir} and {missing_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
