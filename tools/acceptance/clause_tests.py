"""Map ledger clause IDs to the pytest node IDs that test them (FT-D08).

A test belongs to clause CRA-NNN.X when its function name starts with
``test_cra_NNN_X_`` or the first line of its docstring cites ``CRA-NNN.X``.
Pure AST scan; nothing is imported or executed.
"""
from __future__ import annotations

import ast
import re
from collections import defaultdict
from pathlib import Path

_NAME = re.compile(r"^test_cra_(\d{3})_([0-9a-z]+)_", re.I)
_DOC = re.compile(r"\bCRA-(\d{3})\.([0-9A-Za-z]+)\b")


def _clause(number: str, part: str) -> str:
    return f"CRA-{number}.{part.upper() if part.isalpha() else part}"


def clause_test_map(root: Path, tests_dir: str = "tests") -> dict[str, list[str]]:
    mapping: dict[str, set[str]] = defaultdict(set)
    for path in sorted((root / tests_dir).rglob("test_*.py")):
        rel = path.relative_to(root).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        scopes: list[tuple[str, ast.AST]] = [("", tree)]
        while scopes:
            prefix, scope = scopes.pop()
            for node in getattr(scope, "body", []):
                if isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
                    scopes.append((f"{prefix}{node.name}::", node))
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                    node_id = f"{rel}::{prefix}{node.name}"
                    clauses = set()
                    match = _NAME.match(node.name)
                    if match:
                        clauses.add(_clause(*match.groups()))
                    doc = (ast.get_docstring(node) or "").strip().splitlines()
                    if doc:
                        clauses.update(_clause(*m) for m in _DOC.findall(doc[0]))
                    for clause in clauses:
                        mapping[clause].add(node_id)
    return {clause: sorted(ids) for clause, ids in mapping.items()}


_ANY = re.compile(r"\bCRA-(\d{3})\.([0-9]+|A)\b")


def clause_file_map(root: Path, tests_dir: str = "tests") -> dict[str, list[str]]:
    """Fallback: test files that cite a clause ID anywhere (module docstring or section comment)."""
    mapping: dict[str, set[str]] = defaultdict(set)
    for path in sorted((root / tests_dir).rglob("test_*.py")):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in _ANY.findall(text):
            mapping[_clause(*match)].add(path.relative_to(root).as_posix())
    return {clause: sorted(files) for clause, files in mapping.items()}
