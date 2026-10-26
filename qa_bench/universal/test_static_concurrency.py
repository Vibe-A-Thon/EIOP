"""Static concurrency analysis: detect self-deadlocking lock re-entry.

Pattern detected (found twice in production code by the universal API sweep):

    self._lock = threading.Lock()          # non-reentrant
    def outer(self):
        with self._lock:
            self.inner()                   # inner() also does `with self._lock:` -> hangs forever

The scan is AST-based over ``packages/`` and ``apps/``; it follows direct
``self.method()`` calls (one level, plus transitive closure within the class).
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from qa_bench.config import REPO_ROOT

SCAN_ROOTS = [REPO_ROOT / "packages", REPO_ROOT / "apps"]


def _lock_attrs(cls: ast.ClassDef) -> set[str]:
    """Attributes assigned ``threading.Lock()`` / ``Lock()`` (non-reentrant)."""
    attrs = set()
    for node in ast.walk(cls):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            fn = node.value.func
            name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
            if name != "Lock":
                continue
            for tgt in node.targets:
                if isinstance(tgt, ast.Attribute) and isinstance(tgt.value, ast.Name) and tgt.value.id == "self":
                    attrs.add(tgt.attr)
    return attrs


def _with_lock_bodies(fn: ast.FunctionDef, locks: set[str]):
    for node in ast.walk(fn):
        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if (isinstance(ctx, ast.Attribute) and isinstance(ctx.value, ast.Name)
                        and ctx.value.id == "self" and ctx.attr in locks):
                    yield ctx.attr, node


def _self_calls(node: ast.AST) -> set[str]:
    out = set()
    for n in ast.walk(node):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and isinstance(n.func.value, ast.Name) and n.func.value.id == "self"):
            out.add(n.func.attr)
    return out


def find_reentrant_deadlocks() -> list[str]:
    findings = []
    for root in SCAN_ROOTS:
        for path in root.rglob("*.py"):
            try:
                tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
            except SyntaxError:
                continue
            for cls in (n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)):
                locks = _lock_attrs(cls)
                if not locks:
                    continue
                methods = {f.name: f for f in cls.body if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))}
                acquires = {name: {l for l, _ in _with_lock_bodies(f, locks)} for name, f in methods.items()}

                def transitive_acquires(name: str, seen: frozenset = frozenset()) -> set[str]:
                    if name in seen or name not in methods:
                        return set()
                    got = set(acquires.get(name, set()))
                    for callee in _self_calls(methods[name]):
                        got |= transitive_acquires(callee, seen | {name})
                    return got

                for name, fn in methods.items():
                    for lock, block in _with_lock_bodies(fn, locks):
                        for callee in _self_calls(block):
                            if lock in transitive_acquires(callee):
                                rel = path.relative_to(REPO_ROOT)
                                findings.append(
                                    f"{rel}:{block.lineno} {cls.name}.{name}() holds self.{lock} "
                                    f"and calls self.{callee}() which re-acquires it"
                                )
    return sorted(set(findings))


@pytest.mark.static
@pytest.mark.universal
def test_no_self_deadlocking_locks():
    findings = find_reentrant_deadlocks()
    assert not findings, (
        "Non-reentrant threading.Lock re-acquired by the same thread (guaranteed hang). "
        "Use threading.RLock or move the call outside the critical section:\n  " + "\n  ".join(findings)
    )


if __name__ == "__main__":  # handy for ad-hoc runs
    for f in find_reentrant_deadlocks():
        print(f)
