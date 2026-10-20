"""Universal surface inventory for 100% route-level coverage.

Discovers, at test-collection time:
  * every backend HTTP operation exposed by the FastAPI app (via its OpenAPI spec)
  * every frontend route declared in ``frontend/src/App.tsx``
  * every backend URL the frontend code calls (``frontend/src/lib``)

and synthesises schema-valid request payloads for each backend operation.
Because discovery happens at runtime, newly added routes are automatically
covered by the universal test suites -- nothing can silently go untested.
"""

from __future__ import annotations

import functools
import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from qa_bench.config import REPO_ROOT

HTTP_METHODS = ("get", "post", "put", "patch", "delete")
MUTATING = {"POST", "PUT", "PATCH", "DELETE"}

# Probe values that are syntactically valid but reference nothing real.
PROBE_STR = "qa-probe"
PROBE_INT = 1


@dataclass(frozen=True)
class Operation:
    method: str
    path: str
    operation_id: str
    tags: tuple[str, ...]
    path_params: tuple[tuple[str, dict], ...] = field(default_factory=tuple)
    query_params: tuple[tuple[str, dict, bool], ...] = field(default_factory=tuple)
    body_schema: dict | None = None
    body_required: bool = False
    body_media: str = "application/json"

    @property
    def id(self) -> str:
        return f"{self.method} {self.path}"

    @property
    def is_mutating(self) -> bool:
        return self.method in MUTATING


# --------------------------------------------------------------------------
# Backend discovery
# --------------------------------------------------------------------------

@functools.lru_cache(maxsize=1)
def build_app():
    """Build one in-process app instance (quiet logs) shared by the universal suites."""
    logging.disable(logging.WARNING)
    from apps.api.main import create_app

    return create_app()


@functools.lru_cache(maxsize=1)
def openapi_spec() -> dict:
    return build_app().openapi()


@functools.lru_cache(maxsize=1)
def discover_operations() -> tuple[Operation, ...]:
    spec = openapi_spec()
    ops: list[Operation] = []
    for path, item in sorted(spec.get("paths", {}).items()):
        shared_params = item.get("parameters", [])
        for method in HTTP_METHODS:
            op = item.get(method)
            if not op:
                continue
            params = list(shared_params) + list(op.get("parameters", []))
            path_params, query_params = [], []
            for p in params:
                p = resolve(p)
                schema = resolve(p.get("schema", {}))
                if p.get("in") == "path":
                    path_params.append((p["name"], schema))
                elif p.get("in") == "query":
                    query_params.append((p["name"], schema, bool(p.get("required"))))
            body_schema, body_required, media = None, False, "application/json"
            rb = op.get("requestBody")
            if rb:
                rb = resolve(rb)
                body_required = bool(rb.get("required"))
                content = rb.get("content", {})
                if "application/json" in content:
                    body_schema = content["application/json"].get("schema", {})
                elif content:
                    media, entry = next(iter(content.items()))
                    body_schema = entry.get("schema", {})
            ops.append(
                Operation(
                    method=method.upper(),
                    path=path,
                    operation_id=op.get("operationId", f"{method}_{path}"),
                    tags=tuple(op.get("tags", [])),
                    path_params=tuple(path_params),
                    query_params=tuple(query_params),
                    body_schema=body_schema,
                    body_required=body_required,
                    body_media=media,
                )
            )
    return tuple(ops)


# --------------------------------------------------------------------------
# Schema-driven payload synthesis
# --------------------------------------------------------------------------

def resolve(node: Any) -> Any:
    """Resolve a local ``$ref`` against the OpenAPI document."""
    seen = 0
    while isinstance(node, dict) and "$ref" in node and seen < 20:
        ref = node["$ref"]
        if not ref.startswith("#/"):
            return {}
        target: Any = openapi_spec()
        for part in ref[2:].split("/"):
            target = target.get(part, {})
        node = target
        seen += 1
    return node


def synth(schema: Any, depth: int = 0, name: str = "") -> Any:
    """Produce a minimal value that satisfies ``schema`` (best effort)."""
    schema = resolve(schema or {})
    if depth > 8:
        return None
    for key in ("example", "default", "const"):
        if key in schema and schema[key] is not None:
            return schema[key]
    if schema.get("examples"):
        ex = schema["examples"]
        return ex[0] if isinstance(ex, list) else next(iter(ex.values()), None)
    if schema.get("enum"):
        return schema["enum"][0]
    for combo in ("anyOf", "oneOf"):
        if combo in schema:
            options = [resolve(s) for s in schema[combo]]
            non_null = [s for s in options if s.get("type") != "null"] or options
            return synth(non_null[0], depth + 1, name)
    if "allOf" in schema:
        merged: dict = {}
        for part in schema["allOf"]:
            v = synth(part, depth + 1, name)
            if isinstance(v, dict):
                merged.update(v)
            elif v is not None:
                return v
        return merged

    typ = schema.get("type")
    if isinstance(typ, list):
        typ = next((t for t in typ if t != "null"), "string")
    if typ is None:
        typ = "object" if "properties" in schema else "string"

    if typ == "object":
        out: dict = {}
        props = schema.get("properties", {})
        required = set(schema.get("required", []))
        for key, sub in props.items():
            if key in required or depth == 0:
                out[key] = synth(sub, depth + 1, key)
        return out
    if typ == "array":
        item = synth(schema.get("items", {}), depth + 1, name)
        n = max(int(schema.get("minItems", 1)), 1)
        return [item] * n
    if typ == "integer":
        return max(int(schema.get("minimum", PROBE_INT)), PROBE_INT) if "maximum" not in schema else int(schema.get("minimum", 0))
    if typ == "number":
        return float(schema.get("minimum", 1.0))
    if typ == "boolean":
        return False
    # string
    fmt = schema.get("format", "")
    if fmt == "date-time":
        return "2026-01-01T00:00:00Z"
    if fmt == "date":
        return "2026-01-01"
    if fmt in ("uri", "url"):
        return "https://example.invalid/qa"
    if fmt == "email":
        return "qa@example.invalid"
    if fmt == "uuid":
        return "00000000-0000-4000-8000-000000000000"
    lowered = name.lower()
    if "tenant" in lowered:
        return "default"
    if lowered in ("query", "q", "question", "text", "eql", "sparql"):
        return "MATCH (n) RETURN n LIMIT 1" if lowered != "question" else "What systems exist?"
    min_len = int(schema.get("minLength", 0))
    value = PROBE_STR
    if len(value) < min_len:
        value = value + "x" * (min_len - len(value))
    if "maxLength" in schema:
        value = value[: int(schema["maxLength"])] or "q"
    return value


def concrete_path(op: Operation) -> str:
    path = op.path
    for name, schema in op.path_params:
        val = synth(schema, name=name)
        if name.lower().startswith("tenant"):
            val = "default"
        path = path.replace("{" + name + "}", str(val if val not in (None, "") else PROBE_STR))
    return path


def required_query(op: Operation) -> dict:
    return {n: synth(s, name=n) for n, s, req in op.query_params if req}


def request_kwargs(op: Operation, body_override: Any = ...) -> dict:
    kwargs: dict = {}
    q = required_query(op)
    if q:
        kwargs["params"] = q
    if op.body_schema is not None:
        body = synth(op.body_schema) if body_override is ... else body_override
        if op.body_media == "application/json":
            kwargs["json"] = body
        elif "form" in op.body_media:
            if isinstance(body, dict):
                files = {k: ("qa.txt", b"qa", "text/plain") for k, v in body.items() if isinstance(v, str) and k in ("file", "files", "upload")}
                data = {k: str(v) for k, v in body.items() if k not in files}
                kwargs["data"] = data
                if files:
                    kwargs["files"] = files
        else:
            kwargs["content"] = b"qa-probe"
            kwargs["headers"] = {"Content-Type": op.body_media}
    return kwargs


# --------------------------------------------------------------------------
# Frontend discovery
# --------------------------------------------------------------------------

FRONTEND_SRC = REPO_ROOT / "frontend" / "src"


@functools.lru_cache(maxsize=1)
def discover_frontend_routes() -> tuple[tuple[str, str], ...]:
    """Return ``(path, component)`` for every authenticated route in App.tsx."""
    app_tsx = (FRONTEND_SRC / "App.tsx").read_text(encoding="utf-8")
    shell_block = app_tsx.split("<AppShell>", 1)[-1]
    routes = re.findall(r'<Route\s+path="([^"]+)"\s+element=\{<(\w+)', shell_block)
    return tuple((p, c) for p, c in routes if c != "Navigate")


def concrete_ui_path(path: str) -> str:
    if path == "*":
        return "/qa-nonexistent-route-404"
    return re.sub(r":(\w+)", PROBE_STR, path)


@functools.lru_cache(maxsize=1)
def discover_frontend_api_calls() -> tuple[str, ...]:
    """Backend paths referenced by frontend source (string literals / templates)."""
    found: set[str] = set()
    pattern = re.compile(r"""[`'"](/(?:api/)?(?:v1/)?[a-z][a-z0-9_\-]*(?:/[^`'"\s?]*)?)""")
    for f in FRONTEND_SRC.rglob("*.ts*"):
        text = f.read_text(encoding="utf-8", errors="ignore")
        if "api" not in text.lower():
            continue
        for m in pattern.finditer(text):
            found.add(m.group(1))
    return tuple(sorted(found))


def screen_files() -> tuple[str, ...]:
    return tuple(sorted(p.stem for p in (FRONTEND_SRC / "screens").glob("*.tsx")))


def sandboxed() -> bool:
    data_dir = os.environ.get("EOIP_DATA_DIR", "")
    return "qa-sandbox" in data_dir.replace("\\", "/")
