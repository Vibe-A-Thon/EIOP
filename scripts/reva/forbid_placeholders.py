#!/usr/bin/env python3
"""AST scanner enforcing no placeholders under reva/ (T-002 / OBL-REVA-P0-GUARDRAILS)."""

import ast
import re
import sys
from pathlib import Path

FORBIDDEN_TOKENS = re.compile(r"\b(TODO|FIXME|XXX|HACK)\b")

def is_protocol_or_overload(node: ast.FunctionDef | ast.AsyncFunctionDef, parents: list[ast.AST]) -> bool:
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id == "overload":
            return True
        if isinstance(decorator, ast.Attribute) and decorator.attr == "overload":
            return True
    # Check parent class for typing.Protocol
    for p in reversed(parents):
        if isinstance(p, ast.ClassDef):
            for base in p.bases:
                if isinstance(base, ast.Name) and base.id == "Protocol":
                    return True
                if isinstance(base, ast.Attribute) and base.attr == "Protocol":
                    return True
    return False

def check_file(path: Path) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8", errors="replace")

    # Check comments and strings for forbidden tokens
    for idx, line in enumerate(text.splitlines(), start=1):
        # Allow checking in strings that define the rule itself or test strings
        if FORBIDDEN_TOKENS.search(line):
            errors.append(f"{path}:{idx} contains forbidden token (TODO/FIXME/XXX/HACK)")

    try:
        tree = ast.parse(text, filename=str(path))
    except Exception as exc:
        return [f"{path}: SyntaxError during AST parsing: {exc}"]

    parents = []

    def visit(node: ast.AST):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            # Skip docstring if first statement
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, (ast.Constant, ast.Str)):
                body = body[1:]

            if not body:
                if not is_protocol_or_overload(node, parents):
                    errors.append(f"{path}:{node.lineno} empty function body '{node.name}'")
            elif len(body) == 1:
                stmt = body[0]
                if isinstance(stmt, ast.Pass):
                    if not is_protocol_or_overload(node, parents):
                        errors.append(f"{path}:{node.lineno} pass-only function '{node.name}'")
                elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis:
                    if not is_protocol_or_overload(node, parents):
                        errors.append(f"{path}:{node.lineno} ellipsis-only function '{node.name}'")
                elif isinstance(stmt, ast.Raise):
                    if isinstance(stmt.exc, ast.Call) and isinstance(stmt.exc.func, ast.Name) and stmt.exc.func.id == "NotImplementedError":
                        errors.append(f"{path}:{node.lineno} NotImplementedError in '{node.name}'")
                    elif isinstance(stmt.exc, ast.Name) and stmt.exc.id == "NotImplementedError":
                        errors.append(f"{path}:{node.lineno} NotImplementedError in '{node.name}'")

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            mod = getattr(node, "module", "") or ""
            names = [alias.name for alias in node.names]
            if mod.startswith("tests") or any(n.startswith("tests") for n in names):
                errors.append(f"{path}:{node.lineno} illegal import from tests: {mod or names}")

        parents.append(node)
        for child in ast.iter_child_nodes(node):
            visit(child)
        parents.pop()

    visit(tree)
    return errors

def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent.parent
    reva_dir = repo_root / "reva"
    if not reva_dir.exists():
        reva_dir = repo_root / "packages" / "reva"
        if not reva_dir.exists():
            print("No reva directory found yet.", file=sys.stderr)
            return 0

    all_errors = []
    for py_file in reva_dir.rglob("*.py"):
        all_errors.extend(check_file(py_file))

    if all_errors:
        print("Forbid placeholders check FAILED:", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("Forbid placeholders check: PASS (0 violations)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
