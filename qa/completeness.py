"""Fail-closed inventory of developed surfaces and their QA evidence gaps."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

from qa.bench import BASELINE, ROOT, api_surface, offline_document
from qa.portfolio import manifest
from qa.probe_coverage import probe_operations

OUTPUT = ROOT / "test-results" / "qa-bench" / "completeness.json"
PYTHON_ROOTS = (
    "packages/eoip", "apps/api", "apps/mcp", "apps/worker", "backend",
    "reva", "scripts", "tools", "demo", "qa", "eoip-audit-kit",
)
WEB_ROOTS = ("apps/web/src", "frontend", "apps/vscode-extension")
WEB_SUFFIXES = {".js", ".jsx", ".ts", ".tsx", ".mjs"}
EXCLUDED_PARTS = {"node_modules", "dist", "build", "coverage", "__pycache__", "test", "tests"}


def source_files(root: Path = ROOT) -> tuple[list[str], list[str]]:
    python = []
    web = []
    for base in PYTHON_ROOTS:
        directory = root / base
        if directory.exists():
            python.extend(
                path.relative_to(root).as_posix()
                for path in directory.rglob("*.py")
                if not EXCLUDED_PARTS.intersection(path.relative_to(directory).parts)
                and not path.name.startswith("test_")
            )
    for base in WEB_ROOTS:
        directory = root / base
        if directory.exists():
            web.extend(
                path.relative_to(root).as_posix()
                for path in directory.rglob("*")
                if path.is_file()
                and path.suffix in WEB_SUFFIXES
                and not EXCLUDED_PARTS.intersection(path.relative_to(directory).parts)
                and not path.name.endswith((".test.js", ".spec.js", ".test.ts", ".spec.ts"))
            )
    return sorted(set(python)), sorted(set(web))


def mcp_tools(source: Path = ROOT / "apps/mcp/main.py") -> list[str]:
    tree = ast.parse(source.read_text(encoding="utf-8"))
    tools = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if any(
            isinstance(decorator, ast.Call)
            and isinstance(decorator.func, ast.Attribute)
            and decorator.func.attr == "tool"
            for decorator in node.decorator_list
        ):
            tools.append(node.name)
    if len(tools) != len(set(tools)):
        raise ValueError("Duplicate MCP tool registration")
    return sorted(tools)


def coverage_status(path: str, report: dict | None) -> dict:
    if report is None:
        return {"status": "unmeasured"}
    files = {name.replace("\\", "/"): data for name, data in report.get("files", {}).items()}
    file_data = files.get(path)
    if file_data is None:
        return {"status": "unmeasured"}
    summary = file_data.get("summary", {})
    statements = summary.get("num_statements", 0)
    missing = summary.get("missing_lines", 0)
    branches = summary.get("num_branches", 0)
    missing_branches = summary.get("missing_branches", 0)
    return {
        "status": (
            "line_only_measured" if not report.get("meta", {}).get("branch_coverage")
            else "line_and_branch_measured" if not missing and not missing_branches
            else "partially_measured"
        ),
        "statements": statements,
        "missing_lines": missing,
        "branches": branches,
        "missing_branches": missing_branches,
        "note": "Execution coverage is necessary but does not prove behavior or integration.",
    }


def inventory(root: Path = ROOT, coverage: dict | None = None) -> dict:
    surface = api_surface(offline_document())
    pinned = json.loads((root / BASELINE.relative_to(ROOT)).read_text(encoding="utf-8"))
    current_ops = {(item["method"], item["path"]) for item in surface["operations"]}
    pinned_ops = {(item["method"], item["path"]) for item in pinned["operations"]}
    probes = probe_operations()
    python, web = source_files(root)
    tools = mcp_tools(root / "apps/mcp/main.py")
    operations = [
        {
            "method": method,
            "path": path,
            "status": "dedicated_probe_exists_but_execution_unverified" if (method, path) in probes else "no_dedicated_qa_probe",
        }
        for method, path in sorted(current_ops)
    ]
    suites = [
        {"id": suite["id"], "state": suite["state"], "risk": suite["risk"], "status": "execution_unverified"}
        for suite in manifest()
    ]
    return {
        "schema_version": 1,
        "claim": "This is a gap inventory, not a certification of 100% testing.",
        "summary": {
            "api_operations": len(current_ops),
            "api_dedicated_probes": len(current_ops & probes),
            "api_without_dedicated_probe": len(current_ops - probes),
            "api_surface_added": len(current_ops - pinned_ops),
            "api_surface_removed": len(pinned_ops - current_ops),
            "mcp_tools": len(tools),
            "python_modules": len(python),
            "web_and_extension_modules": len(web),
            "python_modules_without_complete_line_branch_measurement": sum(
                coverage_status(path, coverage)["status"] != "line_and_branch_measured" for path in python
            ),
            "web_and_extension_modules_without_measured_coverage": len(web),
            "qa_suites": len(suites),
        },
        "api_operations": operations,
        "mcp_tools": [{"name": name, "status": "protocol_assertions_exist_execution_unverified"} for name in tools],
        "python_modules": [{"path": path, **coverage_status(path, coverage)} for path in python],
        "web_and_extension_modules": [{"path": path, "status": "unmeasured"} for path in web],
        "qa_suites": suites,
        "release_blockers": [
            "No per-operation passing functional evidence for the full API surface.",
            "MCP tool protocol assertions require current-revision execution receipts and end-to-end API behavior checks.",
            "All production Python and frontend modules require measured execution plus reviewed behavioral assertions.",
            "Infrastructure, external connector, restore, scale, security and human accessibility suites remain unverified.",
            "A passing static inventory or line/branch percentage alone never closes a requirement.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("report", "gate"))
    parser.add_argument("--coverage-json", type=Path, help="Optional fresh pytest-cov JSON; informational only")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args(argv)
    coverage = json.loads(args.coverage_json.read_text(encoding="utf-8")) if args.coverage_json else None
    report = inventory(coverage=coverage)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    print(f"Gap inventory: {args.output}")
    if args.command == "gate":
        print("BLOCKED: release completeness requires executed functional evidence and reviewed sign-off.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
