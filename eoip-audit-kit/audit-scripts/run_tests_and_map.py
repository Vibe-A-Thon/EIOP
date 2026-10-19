#!/usr/bin/env python3
"""Detect and run tests safely; map results to requirements; write missing_tests.json."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def load_req_ids(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    reqs = data.get("requirements") or data
    if isinstance(reqs, dict):
        return list(reqs.keys())
    return [r["id"] for r in reqs]


def run_cmd(cmd: list[str], cwd: Path, timeout: int = 300) -> tuple[int, str]:
    try:
        r = subprocess.run(
            cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout
        )
        out = (r.stdout or "") + (r.stderr or "")
        return r.returncode, out
    except FileNotFoundError:
        return 127, f"command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, "timeout"


def parse_junit(junit: Path) -> list[dict]:
    if not junit.is_file():
        return []
    try:
        tree = ET.parse(junit)
    except ET.ParseError:
        return []
    cases = []
    for tc in tree.iter("testcase"):
        name = tc.get("name") or ""
        classname = tc.get("classname") or ""
        failed = tc.find("failure") is not None or tc.find("error") is not None
        skipped = tc.find("skipped") is not None
        status = "failed" if failed else ("skipped" if skipped else "passed")
        cases.append(
            {
                "name": name,
                "classname": classname,
                "status": status,
                "mapped_requirements": [],
            }
        )
    return cases


def map_cases(cases: list[dict], req_ids: list[str], root: Path) -> list[dict]:
    # search test file contents for REQ ids
    id_set = set(req_ids)
    file_index: dict[str, set[str]] = {}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if "test" not in str(p).lower() and "spec" not in str(p).lower():
            continue
        if p.suffix.lower() not in {".py", ".js", ".ts", ".tsx", ".java", ".go"}:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        found = set(re.findall(r"REQ-[A-Z]+-\d{4}", text)) & id_set
        if found:
            file_index[str(p.relative_to(root))] = found

    for c in cases:
        mapped = set()
        blob = f"{c['classname']} {c['name']}"
        for rid in id_set:
            if rid in blob:
                mapped.add(rid)
        for fpath, ids in file_index.items():
            base = Path(fpath).stem
            if base.replace("test_", "") in c["classname"] or base in c["name"]:
                mapped |= ids
            # classname often module path
            mod = c["classname"].replace(".", "/")
            if mod and mod in fpath.replace("\\", "/"):
                mapped |= ids
        c["mapped_requirements"] = sorted(mapped)
    return cases


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", required=True, type=Path)
    ap.add_argument("--requirements", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--commit", default="")
    args = ap.parse_args()

    root = args.repo_root.resolve()
    out_dir = args.out.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    req_ids = load_req_ids(args.requirements)

    summary = {
        "commit": args.commit or None,
        "runners_tried": [],
        "exit_codes": {},
        "notes": [],
    }
    junit_path = out_dir / "tests.xml"
    cases: list[dict] = []

    # pytest
    if (root / "pytest.ini").exists() or (root / "pyproject.toml").exists() or any(
        root.rglob("test_*.py")
    ):
        if shutil.which("pytest"):
            code, log = run_cmd(
                ["pytest", "-q", f"--junitxml={junit_path}"], root
            )
            summary["runners_tried"].append("pytest")
            summary["exit_codes"]["pytest"] = code
            (out_dir / "pytest.log").write_text(log, encoding="utf-8")
            cases = parse_junit(junit_path)
        else:
            summary["notes"].append("pytest not installed; skipped")
    else:
        summary["notes"].append("No pytest-style tests detected")

    # npm test
    if (root / "package.json").exists():
        if shutil.which("npm"):
            code, log = run_cmd(["npm", "test", "--silent"], root, timeout=300)
            summary["runners_tried"].append("npm test")
            summary["exit_codes"]["npm_test"] = code
            (out_dir / "npm_test.log").write_text(log, encoding="utf-8")
        else:
            summary["notes"].append("npm not installed; skipped")

    if not summary["runners_tried"]:
        summary["notes"].append("No test runners executed")

    cases = map_cases(cases, req_ids, root)
    mapped_ids = set()
    for c in cases:
        mapped_ids.update(c["mapped_requirements"])

    missing = sorted(set(req_ids) - mapped_ids)
    missing_doc = {
        "commit": args.commit or None,
        "missing_requirement_ids": missing,
        "suggestions": [
            {
                "requirement_id": rid,
                "suggested_test": f"tests/test_{rid.lower().replace('-', '_')}.py",
                "note": "Add automated test referencing this REQ id in a comment or docstring",
            }
            for rid in missing
        ],
    }

    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    (out_dir / "mapped_cases.json").write_text(
        json.dumps(cases, indent=2) + "\n", encoding="utf-8"
    )
    missing_path = out_dir.parent / "missing_tests.json"
    if out_dir.name == "test_results":
        missing_path = out_dir.parent / "missing_tests.json"
    else:
        missing_path = out_dir / "missing_tests.json"
    missing_path.write_text(json.dumps(missing_doc, indent=2) + "\n", encoding="utf-8")

    print(f"Runners: {summary['runners_tried'] or 'none'}")
    print(f"Cases: {len(cases)}; missing req coverage: {len(missing)}")
    print(f"Wrote {out_dir} and {missing_path}")
    return 0  # never hard-fail


if __name__ == "__main__":
    raise SystemExit(main())
