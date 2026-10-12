from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def names() -> list[str]:
    raw = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT, check=True, capture_output=True,
    ).stdout
    return sorted(p.decode() for p in raw.split(b"\0") if p and p.endswith(b".py"))


def is_protocol_class(node: ast.ClassDef) -> bool:
    return any(
        isinstance(base, ast.Name) and base.id in {"Protocol", "ABC"}
        or isinstance(base, ast.Attribute) and base.attr in {"Protocol", "ABC"}
        for base in node.bases
    )


def substantive_body(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[ast.stmt]:
    return [stmt for stmt in node.body if not (
        isinstance(stmt, ast.Expr)
        and isinstance(stmt.value, ast.Constant)
        and isinstance(stmt.value.value, str)
    )]


def main() -> None:
    rows = []
    for name in names():
        if name.startswith(("demo/", "data/", ".audit-scratch/")):
            continue
        path = ROOT / name
        try:
            tree = ast.parse(path.read_text(encoding="utf-8-sig", errors="replace"))
        except SyntaxError:
            continue
        parents: dict[ast.AST, ast.AST] = {}
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                parents[child] = parent
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            body = substantive_body(node)
            kind = None
            if not body:
                kind = "empty"
            elif len(body) == 1 and isinstance(body[0], ast.Pass):
                kind = "pass-only"
            elif len(body) == 1 and isinstance(body[0], ast.Raise):
                call = body[0].exc
                if isinstance(call, ast.Call) and getattr(call.func, "id", "") == "NotImplementedError":
                    kind = "not-implemented-only"
            if not kind:
                continue
            parent = parents.get(node)
            protocol = isinstance(parent, ast.ClassDef) and is_protocol_class(parent)
            decorators = [
                ast.unparse(item) if hasattr(ast, "unparse") else ""
                for item in node.decorator_list
            ]
            rows.append({
                "path": name.replace("\\", "/"),
                "line": node.lineno,
                "end_line": getattr(node, "end_lineno", node.lineno),
                "name": node.name,
                "class": parent.name if isinstance(parent, ast.ClassDef) else None,
                "kind": kind,
                "protocol_or_abc": protocol,
                "abstractmethod": any("abstractmethod" in item for item in decorators),
                "scope": "test" if name.startswith("tests/") else "production",
            })
    out = ROOT / ".audit-scratch" / "stubs.json"
    out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    prod = [r for r in rows if r["scope"] == "production"]
    concrete = [r for r in prod if not r["protocol_or_abc"] and not r["abstractmethod"]]
    print(json.dumps({
        "all": len(rows), "production": len(prod), "concrete_production": len(concrete),
        "concrete": concrete,
    }, indent=2))


if __name__ == "__main__":
    main()
