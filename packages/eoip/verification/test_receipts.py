"""Execution receipts are evidence of tests, never application certification."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from eoip.verification.cp_registry import digest, local_file

SOURCE_DIRS = ("apps", "packages", "scripts", "tests", "config", "deploy", ".github")
SOURCE_SUFFIXES = {".py", ".js", ".jsx", ".mjs", ".ts", ".tsx", ".json", ".yaml", ".yml", ".toml", ".lock", ".css", ".html", ".sh", ".ps1"}
ROOT_INPUTS = ("pyproject.toml", "requirements.lock", "requirements.txt")


def source_manifest(root: Path) -> dict[str, str]:
    paths = []
    for directory in SOURCE_DIRS:
        base = root / directory
        if not base.is_dir():
            continue
        # Prune generated/dependency trees before recursion rather than hashing their contents.
        import os
        for current, directories, files in os.walk(base, followlinks=False):
            directories[:] = sorted(d for d in directories if d not in {
                "node_modules", "__pycache__", "dist", "build", ".venv", ".git", ".pytest_cache",
                "test-results", "playwright-report", "vendor",
            } and not (Path(current) / d).is_symlink())
            paths.extend(Path(current) / name for name in sorted(files)
                         if Path(name).suffix in SOURCE_SUFFIXES or name.startswith("Dockerfile"))
    paths.extend(root / name for name in ROOT_INPUTS if (root / name).is_file())
    result = {}
    for path in sorted(set(paths)):
        relative = path.relative_to(root).as_posix()
        checked = local_file(root, relative)
        result[relative] = digest(checked.read_bytes())
    return result


def revision(root: Path) -> str | None:
    try:
        result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True,
                                text=True, timeout=10, check=True)
        return result.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


def seal_receipt(receipt: dict) -> dict:
    payload = dict(receipt)
    payload.pop("receipt_sha256", None)
    payload["receipt_sha256"] = digest(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    return payload


def validate_receipt(root: Path, receipt: dict) -> None:
    if receipt.get("schema_version") != "cp-test-run-v1":
        raise ValueError("unsupported test receipt schema")
    if receipt.get("receipt_sha256") != seal_receipt(receipt)["receipt_sha256"]:
        raise ValueError("test receipt digest mismatch")
    if receipt.get("exit_code") != 0 or receipt.get("collect_only") or receipt.get("collection_errors"):
        raise ValueError("run did not execute successfully")
    if not receipt.get("source_unchanged") or receipt.get("source_manifest") != source_manifest(root):
        raise ValueError("tested source has changed")
    selected = receipt.get("selected_node_ids", [])
    tests = receipt.get("tests", [])
    nodeids = [case.get("nodeid") for case in tests]
    if not selected or len(selected) != len(set(selected)) or sorted(nodeids) != sorted(selected):
        raise ValueError("incomplete or duplicate test execution")
    if any(case.get("outcome") != "PASSED" for case in tests):
        raise ValueError("failed, skipped, xfailed or incomplete test cannot establish passing evidence")
    if receipt.get("counts", {}).get("passed") != len(selected):
        raise ValueError("test counts do not match results")
    for case in tests:
        if case.get("phases") != {"setup": "passed", "call": "passed", "teardown": "passed"}:
            raise ValueError("test setup/call/teardown did not all pass")
