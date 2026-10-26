"""Discover and run EOIP QA suites with explicit safety and evidence states."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from qa.bench import ROOT, exit_code, newman_executable, validated_base_url, write_evidence

MANIFEST = ROOT / "qa" / "manifest.json"
CATALOG = ROOT / "qa" / "test-catalog.json"


def manifest() -> list[dict]:
    suites = json.loads(MANIFEST.read_text(encoding="utf-8"))["suites"]
    ids = [suite["id"] for suite in suites]
    if len(ids) != len(set(ids)):
        raise ValueError("QA suite IDs must be unique")
    for suite in suites:
        command = suite.get("command")
        if command and not isinstance(command, list):
            raise ValueError(f"Invalid command for {suite['id']}")
        if suite.get("cwd") and not (ROOT / suite["cwd"]).is_dir():
            raise ValueError(f"Unknown suite directory: {suite['id']}")
    return suites


def category(path: Path) -> str:
    parts = path.relative_to(ROOT).parts
    if parts[0] == "tests":
        return parts[1] if len(parts) > 2 else "root"
    if parts[:3] == ("apps", "web", "tests"):
        return "web-unit" if "unit" in parts else "web-browser"
    return "unmapped"


def test_definitions(path: Path) -> int:
    content = path.read_text(encoding="utf-8")
    if path.suffix == ".py":
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return 0
        return sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_") for node in ast.walk(tree))
    return len(re.findall(r"\btest(?:\.skip|\.fixme|\.only)?\s*\(", content))


def build_catalog() -> dict:
    files = []
    patterns = ("tests/**/test_*.py", "apps/web/tests/**/*.spec.js", "apps/web/tests/**/*.test.mjs")
    seen = set()
    for pattern in patterns:
        for path in sorted(ROOT.glob(pattern)):
            relative = path.relative_to(ROOT).as_posix()
            if relative in seen:
                continue
            seen.add(relative)
            files.append({"path": relative, "category": category(path), "test_definitions": test_definitions(path)})
    files.sort(key=lambda item: item["path"])
    groups: dict[str, dict[str, int]] = {}
    for item in files:
        group = groups.setdefault(item["category"], {"files": 0, "test_definitions": 0})
        group["files"] += 1
        group["test_definitions"] += item["test_definitions"]
    return {
        "schema_version": 1,
        "interpretation": "Static test definitions, not collected/parametrized test cases or product coverage",
        "totals": {"files": len(files), "test_definitions": sum(item["test_definitions"] for item in files)},
        "categories": dict(sorted(groups.items())),
        "files": files,
    }


def catalog_command(write: bool) -> int:
    current = build_catalog()
    if write:
        CATALOG.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {CATALOG.relative_to(ROOT)}: {current['totals']}")
        return 0
    if not CATALOG.exists():
        print("QA catalog absent; run python -m qa.portfolio catalog --write")
        return 2
    pinned = json.loads(CATALOG.read_text(encoding="utf-8"))
    if pinned != current:
        old = {item["path"] for item in pinned.get("files", [])}
        new = {item["path"] for item in current["files"]}
        print(f"QA catalog drift: added={sorted(new-old)} removed={sorted(old-new)}")
        return 1
    print(f"QA catalog current: {current['totals']}; {len(current['categories'])} categories")
    return 0


def run_suite(suite: dict, args: argparse.Namespace) -> dict:
    name = suite["id"]
    risk = suite["risk"]
    if not suite.get("command"):
        return {"name": name, "status": "blocked", "detail": suite.get("blocker", "No automated command")}
    if risk == "expensive" and not args.allow_expensive:
        return {"name": name, "status": "blocked", "detail": "Explicit --allow-expensive required"}
    if risk == "infrastructure" and not args.allow_infrastructure:
        return {"name": name, "status": "blocked", "detail": "Explicit --allow-infrastructure required"}
    command = [sys.executable if item == "{python}" else item for item in suite["command"]]
    executable = command[0]
    resolved = str(Path(executable).resolve()) if Path(executable).exists() else shutil.which(executable)
    if not resolved:
        return {"name": name, "status": "blocked", "detail": f"Executable unavailable: {executable}"}
    command[0] = resolved
    if name in {"postman", "postman-workflow"} and not newman_executable():
        return {"name": name, "status": "blocked", "detail": "Newman unavailable"}
    if name in {"postman", "live-api", "live-schema"} and not (os.environ.get("QA_TOKEN") or os.environ.get("EOIP_API_TOKEN")):
        return {"name": name, "status": "blocked", "detail": "QA_TOKEN or EOIP_API_TOKEN required"}
    if name in {"postman", "live-api", "live-schema"}:
        command.extend(["--base-url", args.base_url])
        if args.allow_remote:
            command.append("--allow-remote")
    start = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="eoip-qa-suite-") as tmp:
        env = os.environ.copy()
        env.update({"EOIP_DATA_DIR": tmp, "EOIP_GRAPH_BACKEND": "memory", "REVA_ENABLED": "false"})
        if name not in {"postman", "live-api", "live-schema"}:
            env["EOIP_API_TOKEN"] = secrets.token_urlsafe(32)
            from qa._principal import provision

            env.update(provision(tmp, env["EOIP_API_TOKEN"]))
        if name == "bounded-load":
            env["QA_BASE_URL"] = args.base_url
            env["QA_ALLOW_REMOTE"] = "true" if args.allow_remote else "false"
        if name == "browser-quality":
            env["EOIP_GUI_WEB_SERVER"] = "1"
            env["PLAYWRIGHT_BASE_URL"] = "http://127.0.0.1:5173"
        with tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as output:
            try:
                result = subprocess.run(
                    command, cwd=ROOT / suite.get("cwd", "."), env=env,
                    stdout=output, stderr=subprocess.STDOUT,
                    timeout=suite["timeout_s"], check=False,
                )
                code = result.returncode
                output.flush()
                output.seek(0)
                checksum = hashlib.sha256()
                for chunk in iter(lambda: output.read(65536), ""):
                    checksum.update(chunk.encode("utf-8"))
                digest = checksum.hexdigest()
                detail = f"exit={code}; output_sha256={digest}; raw output discarded"
                status = "pass" if code == 0 else ("blocked" if code == 2 and name in {"postman", "postman-workflow", "live-api", "live-schema"} else "fail")
            except subprocess.TimeoutExpired:
                status, detail = "fail", f"Timed out after {suite['timeout_s']}s; raw output discarded"
    return {"name": name, "status": status, "detail": detail, "duration_s": round(time.perf_counter() - start, 2)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="Show automated, blocked, and manual QA suites")
    cat = sub.add_parser("catalog", help="Check or explicitly regenerate the static test inventory")
    cat.add_argument("--write", action="store_true")
    run = sub.add_parser("run", help="Run named suites or a QA profile")
    run.add_argument("--profile", choices=["quick", "extended"], default="quick")
    run.add_argument("--suite", action="append", default=[])
    run.add_argument("--allow-expensive", action="store_true")
    run.add_argument("--allow-infrastructure", action="store_true")
    run.add_argument("--base-url", default="http://127.0.0.1:8000")
    run.add_argument("--allow-remote", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "catalog":
        return catalog_command(args.write)
    suites = manifest()
    if args.command == "list":
        for suite in suites:
            print(f"{suite['id']:<26} {suite['kind']:<18} {suite['state']:<13} {suite['risk']}")
        return 0
    try:
        validated_base_url(args.base_url, args.allow_remote)
    except ValueError as exc:
        parser.error(str(exc))
    by_id = {suite["id"]: suite for suite in suites}
    unknown = set(args.suite) - by_id.keys()
    if unknown:
        parser.error(f"Unknown suite IDs: {sorted(unknown)}")
    selected = [by_id[key] for key in args.suite] if args.suite else [suite for suite in suites if args.profile in suite["profiles"]]
    checks = []
    for suite in selected:
        result = run_suite(suite, args)
        checks.append(result)
        print(f"{result['status'].upper():7} {result['name']}: {result['detail']}", flush=True)
    path = write_evidence("portfolio", checks, {"profile": args.profile, "selected": [s["id"] for s in selected]})
    print(f"Evidence: {path.relative_to(ROOT)}")
    return exit_code(checks)


if __name__ == "__main__":
    raise SystemExit(main())
