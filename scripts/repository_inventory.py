"""Build a content-free repository map; static inspection is not runtime evidence."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

OUTPUT = "docs/generated/repository-inventory.json"
MAX_BYTES = 16 * 1024 * 1024
EXCLUDED_PARTS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".audit-scratch",
    ".data", ".eoip-data", ".tmp", ".cache", ".pytest_cache", ".ruff_cache",
    "dist", "build", "test-results", "test_reports", "secrets", ".vscode-test",
}


def exclusion(name: str) -> str | None:
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name:
        return "unsafe_path"
    if any(part.casefold() in EXCLUDED_PARTS for part in path.parts):
        return "runtime_dependency_or_secret_directory"
    if path.suffix.casefold() in {".key", ".keys", ".pem", ".pfx", ".p12"}:
        return "potential_secret"
    if path.name.casefold().startswith(".env") or path.name.casefold() in {
        ".envrc", ".credentials", "credentials.json",
    }:
        return "potential_secret"
    if name == OUTPUT:
        return "inventory_self_reference"
    if name == "memory/test_credentials.md":
        return "potential_secret"
    return None


def python_summary(text: str) -> dict:
    try:
        tree = ast.parse(text)
    except SyntaxError as error:
        return {"parse_status": "syntax_error", "error_line": error.lineno}
    definitions = []
    imports = set()
    routes = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definitions.append({"name": node.name, "line": node.lineno, "kind": type(node).__name__})
            for decorator in node.decorator_list:
                if not isinstance(decorator, ast.Call) or not isinstance(decorator.func, ast.Attribute):
                    continue
                if decorator.func.attr not in {"get", "post", "put", "patch", "delete", "websocket"}:
                    continue
                if decorator.args and isinstance(decorator.args[0], ast.Constant):
                    value = decorator.args[0].value
                    if isinstance(value, str) and value.startswith("/"):
                        routes.append({"method": decorator.func.attr.upper(), "path": value, "line": node.lineno})
        elif isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add("." * node.level + node.module)
    return {"parse_status": "ok", "definitions": definitions, "imports": sorted(imports), "route_candidates": routes}


def inspect_file(root: Path, name: str) -> dict:
    record = {"path": name, "semantic_review": "not_asserted"}
    reason = exclusion(name)
    if reason:
        return {**record, "status": "excluded", "reason": reason}
    path = root.joinpath(*PurePosixPath(name).parts)
    if any(part.is_symlink() for part in (path, *path.parents) if part != root):
        return {**record, "status": "excluded", "reason": "symlink"}
    if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
        return {**record, "status": "unread", "reason": "missing_or_nonregular"}
    size = path.stat().st_size
    if size > MAX_BYTES:
        return {**record, "status": "excluded", "reason": "size_limit", "bytes": size}
    raw = path.read_bytes()
    record.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    if b"\0" in raw:
        return {**record, "status": "binary_hashed"}
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return {**record, "status": "non_utf8_hashed"}
    record.update(status="text_read", lines=len(text.splitlines()))
    if path.suffix == ".py":
        record["python"] = python_summary(text)
    elif path.name == "package.json":
        try:
            package = json.loads(text)
            record["package"] = {
                "name": package.get("name"), "version": package.get("version"),
                "script_names": sorted(package.get("scripts", {})),
                "dependency_names": sorted(package.get("dependencies", {})),
                "dev_dependency_names": sorted(package.get("devDependencies", {})),
            }
        except (ValueError, AttributeError, TypeError):
            record["package"] = {"parse_status": "invalid_manifest"}
    return record


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True,
        encoding="utf-8",
    ).stdout


def build_inventory(root: Path) -> dict:
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel").strip()).resolve() != root:
        raise ValueError("Use the Git repository root")
    names = sorted(set(git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard").split("\0")) - {""})
    records = [inspect_file(root, name) for name in names]
    counts = Counter(record["status"] for record in records)
    areas = Counter(record["path"].split("/")[0] for record in records)
    return {
        "schema_version": 1, "generated_at": datetime.now(UTC).isoformat(),
        "head": git(root, "rev-parse", "HEAD").strip(),
        "working_tree_dirty": bool(git(root, "status", "--porcelain")),
        "scope": "Git-listed tracked and nonignored untracked files; explicit exclusions recorded per path",
        "limitations": [
            "Mechanical full-content reads and Python AST discovery are not full semantic review or acceptance evidence.",
            "Secrets, ignored files, dependency/runtime directories, symlinks and oversized files are not inspected.",
            "Route candidates omit dynamic registration and prefixes; deployed OpenAPI is authoritative for HTTP contracts.",
            "JavaScript/TypeScript are read and hashed, not parsed or executed; binary/non-UTF8 files are hashed only.",
            "No credentials, source bodies, environment values or test completion claims are emitted.",
        ],
        "counts": {"files": len(records), "by_status": dict(counts), "by_top_level": dict(sorted(areas.items())),
                   "text_lines": sum(record.get("lines", 0) for record in records)},
        "files": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--write", action="store_true", help=f"Write {OUTPUT}; otherwise print counts only")
    args = parser.parse_args()
    report = build_inventory(args.root)
    if args.write:
        target = args.root.resolve() / OUTPUT
        if any(path.is_symlink() for path in (target, *target.parents)):
            raise ValueError("Refusing symlink output")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(report["counts"], indent=2))
    return 1 if report["counts"]["by_status"].get("unread") else 0


if __name__ == "__main__":
    raise SystemExit(main())
