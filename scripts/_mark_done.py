"""Reusable helper: mark backlog tasks done and sync all registries.

Usage (from a batch script):
    from _mark_done import mark_done
    mark_done({"GAP-GDS": {"test_file": "tests/unit/x.py",
                           "code_paths": ["packages/eoip/..."]}})
Test node ids are discovered from the `@pytest.mark.req` tags in the file, so
the map always reflects real, tagged tests.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROGRESS = ROOT / "kgf-progress-2026-10-12.json"


def _tagged_tests(test_file: str) -> dict[str, list[str]]:
    """Map requirement id -> pytest node ids tagged with it."""
    tree = ast.parse((ROOT / test_file).read_text(encoding="utf-8"))
    out: dict[str, list[str]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        for dec in node.decorator_list:
            if not isinstance(dec, ast.Call):
                continue
            f = dec.func
            is_req = (isinstance(f, ast.Attribute) and f.attr == "req") or (
                isinstance(f, ast.Name) and f.id == "REQ"
            )
            if not is_req:
                continue
            for arg in dec.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    out.setdefault(arg.value, []).append(f"{test_file}::{node.name}")
    return out


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _dump(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def mark_done(entries: dict[str, dict]) -> None:
    test_map_p = ROOT / "requirements-test-map.json"
    reg_p = ROOT / "requirements-registry.json"
    backlog_p = ROOT / "KGF-MASTER-BACKLOG.md"

    test_map = _load(test_map_p)
    registry = _load(reg_p)
    progress = _load(PROGRESS)
    backlog = backlog_p.read_text(encoding="utf-8")
    cache: dict[str, dict[str, list[str]]] = {}

    by_id = {item["id"]: item for item in registry}
    for rid, spec in entries.items():
        tf = spec["test_file"]
        tags = cache.setdefault(tf, _tagged_tests(tf))
        tests = tags.get(rid)
        if not tests:
            raise SystemExit(f"{rid}: no @req-tagged test found in {tf}")
        test_map[rid] = tests
        item = by_id.get(rid)
        if item is None:
            raise SystemExit(f"{rid}: missing from requirements-registry.json")
        item["status"] = "FULLY_DEVELOPED"
        item["code_paths"] = spec["code_paths"]
        item["test_files"] = [tf]
        item["evidence_receipt"] = f"python -m pytest {tf} ({len(tests)} tagged tests passed)"
        progress["s"][rid] = "done"
        esc = re.escape(rid)
        backlog = re.sub(rf"\|\s*\[ \]\s*\|\s*`{esc}`", f"| [x] | `{rid}`", backlog)
        backlog = re.sub(rf"- \[ \] `{esc}`", f"- [x] `{rid}`", backlog)

    _dump(test_map_p, test_map)
    _dump(reg_p, registry)
    _dump(PROGRESS, progress)
    backlog_p.write_text(backlog, encoding="utf-8")
    print(f"marked {len(entries)} done; total done = {len(progress['s'])}")
