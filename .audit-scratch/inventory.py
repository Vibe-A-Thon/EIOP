from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".audit-scratch"

TEXT_EXTENSIONS = {
    "", ".bat", ".conf", ".css", ".csv", ".example", ".html", ".js",
    ".json", ".jsx", ".md", ".properties", ".ps1", ".py", ".rules",
    ".sh", ".toml", ".tpl", ".ts", ".txt", ".yaml", ".yml",
}
BINARY_EXTENSIONS = {".docx", ".pptx", ".xlsx", ".sha256"}
LOCK_EXTENSIONS = {".lock"}
REQ_RE = re.compile(
    r"\b(?:REQ|G2|GAP|SR|TASK|SDLC|FR|AC|TEST|WP|AIDLC|UI|CORE|AI|INFRA|"
    r"GRAPH|MVP|NFR|MS|AGENT|KGR|FRD|COMPLY|REL|CG|PRE|BASE|MULTI|H|CONN|PERF)"
    r"(?:-[A-Z0-9]+)*-(?:[A-Z]+)?\d{1,5}(?:\.\d+)?\b"
)
NORMATIVE_RE = re.compile(
    r"(?:\b(?:must|shall|required|requires|acceptance criteria|should)\b|^\s*[-*]\s+\[[ xX~!]\])",
    re.IGNORECASE,
)
ENV_RE = re.compile(r"\b(?:EOIP|HUGEGRAPH|NEO4J|OTEL|REDIS|AWS|AZURE|OLLAMA)_[A-Z0-9_]+\b")
ROUTE_METHODS = {"get", "post", "put", "patch", "delete", "websocket", "options", "head"}


def repo_names() -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return sorted({name.decode("utf-8") for name in proc.stdout.split(b"\0") if name})


def exclusion(path: Path) -> str | None:
    posix = path.as_posix()
    if path.name in {"gaps-audit-cp.md", "GUI-UIX-requirements.md", "audit-coverage-ledger.md"}:
        return "current audit deliverable; generated and verified after source inventory"
    if path.parts and path.parts[0] == ".audit-scratch":
        return "temporary audit machinery; deleted before delivery"
    if path.parts and path.parts[0] in {"demo", "data"}:
        return "user-excluded demo/example/data content"
    if posix.startswith("EOIP-engg-doc-pkg/examples/"):
        return "user-excluded example content"
    if any(part in {"test-results", ".data", ".hypothesis", ".tmp"} for part in path.parts):
        return "generated runtime, test, or prior audit artifact"
    if path.suffix.lower() in BINARY_EXTENSIONS:
        return "binary office/checksum artifact; metadata inventoried, content not line-readable"
    if path.suffix.lower() in LOCK_EXTENSIONS or path.name == "package-lock.json":
        return "generated dependency lockfile"
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return "unsupported or binary file type"
    return None


def decorator_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{decorator_name(node.value)}.{node.attr}".lstrip(".")
    if isinstance(node, ast.Call):
        return decorator_name(node.func)
    return ""


def literal_string(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def route_rows(path: str, text: str) -> list[dict]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    rows: list[dict] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for deco in node.decorator_list:
            if not isinstance(deco, ast.Call):
                continue
            name = decorator_name(deco.func)
            method = name.rsplit(".", 1)[-1]
            if method not in ROUTE_METHODS:
                continue
            route_path = literal_string(deco.args[0]) if deco.args else None
            kwargs = {kw.arg: literal_string(kw.value) for kw in deco.keywords if kw.arg}
            rows.append({
                "source": path,
                "line": getattr(deco, "lineno", node.lineno),
                "end_line": getattr(node, "end_lineno", node.lineno),
                "method": method.upper(),
                "path": route_path,
                "function": node.name,
                "summary": kwargs.get("summary"),
                "tags": kwargs.get("tags"),
                "parameters": [arg.arg for arg in node.args.args],
            })
    return rows


def main() -> None:
    inventory: list[dict] = []
    requirement_refs: dict[str, list[dict]] = defaultdict(list)
    normative_lines: list[dict] = []
    code_req_refs: dict[str, list[dict]] = defaultdict(list)
    env_refs: dict[str, list[dict]] = defaultdict(list)
    routes: list[dict] = []
    todos: list[dict] = []
    totals = Counter()

    for name in repo_names():
        relative = Path(name)
        full = ROOT / relative
        raw = full.read_bytes()
        reason = exclusion(relative)
        row = {
            "path": relative.as_posix(),
            "type": relative.suffix.lower() or "[none]",
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "status": "EXCLUDED" if reason else "FULLY_READ",
            "reason": reason,
            "lines": None,
            "requirement_ids": [],
            "implementation_ids": [],
        }
        if reason:
            inventory.append(row)
            totals["excluded_files"] += 1
            totals["excluded_bytes"] += len(raw)
            continue

        text = raw.decode("utf-8-sig", errors="replace")
        lines = text.splitlines()
        row["lines"] = len(lines)
        totals["read_files"] += 1
        totals["read_bytes"] += len(raw)
        totals["read_lines"] += len(lines)
        ids_in_file: set[str] = set()
        impl_ids: set[str] = set()

        for line_no, line in enumerate(lines, 1):
            ids = set(REQ_RE.findall(line))
            for req_id in ids:
                ref = {"path": relative.as_posix(), "line": line_no, "text": line.strip()[:500]}
                if relative.suffix.lower() == ".md":
                    requirement_refs[req_id].append(ref)
                    ids_in_file.add(req_id)
                else:
                    code_req_refs[req_id].append(ref)
                    impl_ids.add(req_id)
            if relative.suffix.lower() == ".md" and NORMATIVE_RE.search(line):
                normative_lines.append({
                    "path": relative.as_posix(), "line": line_no,
                    "text": line.strip()[:1000], "explicit_ids": sorted(ids),
                })
            for env_name in set(ENV_RE.findall(line)):
                env_refs[env_name].append({"path": relative.as_posix(), "line": line_no})
            if re.search(r"\b(?:TODO|FIXME|NotImplementedError)\b", line):
                todos.append({"path": relative.as_posix(), "line": line_no, "text": line.strip()[:500]})

        row["requirement_ids"] = sorted(ids_in_file)
        row["implementation_ids"] = sorted(impl_ids)
        inventory.append(row)
        if relative.suffix.lower() == ".md":
            totals["markdown_files"] += 1
            totals["markdown_lines"] += len(lines)
        if relative.suffix.lower() == ".py" and relative.parts[0] in {"apps", "packages"}:
            routes.extend(route_rows(relative.as_posix(), text))

    data = {
        "totals": dict(totals),
        "inventory": inventory,
        "requirement_refs": requirement_refs,
        "normative_lines": normative_lines,
        "code_requirement_refs": code_req_refs,
        "environment_refs": env_refs,
        "routes": routes,
        "todos": todos,
    }
    (OUT / "inventory.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(json.dumps({
        "totals": data["totals"],
        "requirements": len(requirement_refs),
        "normative_lines": len(normative_lines),
        "code_requirement_ids": len(code_req_refs),
        "environment_variables": len(env_refs),
        "routes": len(routes),
        "todos": len(todos),
        "status_counts": Counter(row["status"] for row in inventory),
    }, indent=2, default=dict))


if __name__ == "__main__":
    main()
