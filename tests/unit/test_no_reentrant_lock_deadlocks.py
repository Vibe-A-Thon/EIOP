"""FT-D01: no method calls another lock-taking method while holding the same threading.Lock."""

from __future__ import annotations

import ast
import subprocess
import threading
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def _reentrant_lock_calls(source: bytes, path: str) -> list[str]:
    tree = ast.parse(source)
    found: list[str] = []
    for cls in (n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)):
        locks = set()
        for node in ast.walk(cls):
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                if ast.unparse(node.value.func) in ("threading.Lock", "Lock"):
                    for target in node.targets:
                        if isinstance(target, ast.Attribute) and ast.unparse(target.value) == "self":
                            locks.add(target.attr)
        if not locks:
            continue
        methods = {m.name: m for m in cls.body if isinstance(m, ast.FunctionDef)}

        def held_by(node: ast.With) -> set[str]:
            names = {ast.unparse(i.context_expr) for i in node.items}
            return {n[5:] for n in names if n.startswith("self.")} & locks

        takes = {name: set().union(*[held_by(w) for w in ast.walk(m) if isinstance(w, ast.With)] or [set()])
                 for name, m in methods.items()}
        for name, method in methods.items():
            for with_node in (w for w in ast.walk(method) if isinstance(w, ast.With)):
                held = held_by(with_node)
                if not held:
                    continue
                for call in (c for c in ast.walk(with_node) if isinstance(c, ast.Call)):
                    func = call.func
                    if (isinstance(func, ast.Attribute) and ast.unparse(func.value) == "self"
                            and takes.get(func.attr, set()) & held):
                        found.append(f"{path}:{call.lineno}: {cls.name}.{name} -> self.{func.attr}()")
    return found


def test_no_nested_acquisition_of_non_reentrant_locks():
    try:
        files = subprocess.run(["git", "ls-files", "-z", "--", "packages/*.py", "apps/*.py", "reva/*.py"],
                               cwd=REPO_ROOT, capture_output=True, check=True).stdout.decode().split("\0")
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("not a git checkout")
    found: list[str] = []
    for rel in filter(None, files):
        try:
            found += _reentrant_lock_calls((REPO_ROOT / rel).read_bytes(), rel)
        except SyntaxError:
            continue  # covered by test_python_sources_compile
    assert not found, "\n".join(found)


def _finishes(fn, timeout: float = 2.0):
    result = {}
    thread = threading.Thread(target=lambda: result.setdefault("value", fn()), daemon=True)
    thread.start()
    thread.join(timeout)
    assert not thread.is_alive(), "call deadlocked"
    return result["value"]


def test_execution_tracker_stats_no_deadlock():
    from eoip.intelligence_eng.engine import ExecutionTracker

    stats = _finishes(ExecutionTracker().stats)
    assert stats["total_executions"] == 0 and stats["success_rate"] == 0.0


def test_experiment_tracker_start_run_for_unknown_experiment_no_deadlock():
    from eoip.mlops.experiment_tracker import ExperimentTracker

    run = _finishes(lambda: ExperimentTracker().start_run("unknown-exp"))
    assert run.run_name == "run-1"
