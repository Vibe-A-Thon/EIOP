"""Code introspection inventories (SR-QA-013).

SR-QA-013: generated inventories (API routes, MCP tools, VS Code commands,
algorithms, graph labels) come from CODE introspection; hand-written counts
fail the docs build.

:class:`CodeIntrospector` generates every inventory live from the real
sources:

- API routes: imports ``apps.api`` routers via importlib where safe and walks
  ``fastapi.APIRouter`` route tables; falls back to an AST scan of
  ``apps/api/*.py`` route decorators when import is unsafe (missing deps).
- MCP tools: AST parse of ``apps/mcp/main.py`` counting ``@mcp.tool()``
  decorated functions.
- VS Code commands: ``apps/vscode-extension/package.json``
  ``contributes.commands`` — read as data, never retyped.
- Algorithms / metrics: public callables of ``eoip.graph.algorithms.GraphAlgorithms``
  and ``eoip.graph.metrics.GraphMetricsEngine``.
- Vertex/edge labels: keys of ``VERTEX_LABELS`` / ``EDGE_LABELS`` in
  ``eoip.ontology.manifest``.

:meth:`CodeIntrospector.validate_snapshot` regenerates an inventory and
fails on any drift from a previously published snapshot — so a hand-edited
count in a docs artifact can never pass validation.

Lesson carried from ``eoip.gaps.coverage``: that gate trusted whatever a
human wrote next to a requirement ID; this gate trusts only what the code
actually declares, and validation diffs make drift visible.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import json
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[3]

ROUTE_DECORATOR_RE = ("get", "post", "put", "patch", "delete", "options", "head")


@dataclass
class InventorySnapshot:
    """Versioned inventory bundle; ``validate`` diffs it against live code."""

    api_routes: list[dict] = field(default_factory=list)
    mcp_tools: list[str] = field(default_factory=list)
    vscode_commands: list[dict] = field(default_factory=list)
    algorithms: list[str] = field(default_factory=list)
    metrics: list[str] = field(default_factory=list)
    vertex_labels: list[str] = field(default_factory=list)
    edge_labels: list[str] = field(default_factory=list)
    generated_by: str = "eoip.qa.introspection.CodeIntrospector"

    def to_dict(self) -> dict:
        return {
            "api_routes": self.api_routes,
            "mcp_tools": self.mcp_tools,
            "vscode_commands": self.vscode_commands,
            "algorithms": self.algorithms,
            "metrics": self.metrics,
            "vertex_labels": self.vertex_labels,
            "edge_labels": self.edge_labels,
            "generated_by": self.generated_by,
        }

    @classmethod
    def from_dict(cls, data: dict) -> InventorySnapshot:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__ and k != "generated_by"})

    def counts(self) -> dict[str, int]:
        return {
            "api_routes": len(self.api_routes),
            "mcp_tools": len(self.mcp_tools),
            "vscode_commands": len(self.vscode_commands),
            "algorithms": len(self.algorithms),
            "metrics": len(self.metrics),
            "vertex_labels": len(self.vertex_labels),
            "edge_labels": len(self.edge_labels),
        }


class InventoryValidationError(AssertionError):
    """Raised when a published inventory disagrees with live code (SR-QA-013)."""


class CodeIntrospector:
    """Generates all inventories from code; no hand-written counts."""

    def __init__(self, repo_root: str | Path | None = None) -> None:
        self.repo_root = Path(repo_root) if repo_root else DEFAULT_REPO_ROOT

    # -- public API --------------------------------------------------------
    def generate(self) -> InventorySnapshot:
        return InventorySnapshot(
            api_routes=self.api_route_inventory(),
            mcp_tools=self.mcp_tool_inventory(),
            vscode_commands=self.vscode_command_inventory(),
            algorithms=self.algorithm_inventory(),
            metrics=self.metric_inventory(),
            vertex_labels=self.vertex_label_inventory(),
            edge_labels=self.edge_label_inventory(),
        )

    def validate_snapshot(self, snapshot: InventorySnapshot | dict) -> dict:
        """Diff a published snapshot against live code.

        Hand-edited (hand-written) counts fail here: any route, tool, command,
        algorithm or label that exists in code but not in the snapshot (or
        vice versa) is reported, and the gate fails if drift is found.
        """
        expected = snapshot if isinstance(snapshot, InventorySnapshot) else InventorySnapshot.from_dict(snapshot)
        live = self.generate()
        diffs: dict[str, dict[str, list[str]]] = {}

        def _diff(name: str, live_items: list, snap_items: list) -> None:
            live_set, snap_set = set(live_items), set(snap_items)
            added = sorted(live_set - snap_set)
            removed = sorted(snap_set - live_set)
            if added or removed:
                diffs[name] = {"added_in_code": added, "removed_from_code": removed}

        _diff("api_routes",
              [f"{r['method']} {r['path']}" for r in live.api_routes],
              [f"{r['method']} {r['path']}" for r in expected.api_routes])
        _diff("mcp_tools", live.mcp_tools, expected.mcp_tools)
        _diff("vscode_commands",
              [c["command"] for c in live.vscode_commands],
              [c["command"] for c in expected.vscode_commands])
        _diff("algorithms", live.algorithms, expected.algorithms)
        _diff("metrics", live.metrics, expected.metrics)
        _diff("vertex_labels", live.vertex_labels, expected.vertex_labels)
        _diff("edge_labels", live.edge_labels, expected.edge_labels)
        return {
            "valid": not diffs,
            "message": (
                "inventory matches live code" if not diffs
                else "inventory drift detected — hand-written counts are prohibited (SR-QA-013)"
            ),
            "diffs": diffs,
            "live_counts": live.counts(),
        }

    def assert_snapshot_valid(self, snapshot: InventorySnapshot | dict) -> None:
        result = self.validate_snapshot(snapshot)
        if not result["valid"]:
            raise InventoryValidationError(json.dumps(result["diffs"], indent=2))

    # -- inventories --------------------------------------------------------
    def api_route_inventory(self) -> list[dict]:
        """API routes from the real apps.api routers (importlib where safe)."""
        try:
            return self._api_routes_via_import()
        except Exception:  # noqa: BLE001 -- any import failure falls back to AST
            return self._api_routes_via_ast()

    def _api_routes_via_import(self) -> list[dict]:
        routes: list[dict] = []
        app_module = importlib.import_module("apps.api.app")
        app = None
        for attr in ("app", "create_app"):
            candidate = getattr(app_module, attr, None)
            if candidate is not None:
                app = candidate() if callable(candidate) and attr == "create_app" else candidate
                break
        if app is None or not hasattr(app, "routes"):
            raise RuntimeError("apps.api exposes no FastAPI app")
        from eoip.api_routes import iter_effective_routes

        for route in iter_effective_routes(app.routes):
            methods = getattr(route, "methods", None)
            path = getattr(route, "path", None)
            if not methods or not path:
                continue
            for method in sorted(methods - {"HEAD"}):
                routes.append({"method": method, "path": path, "source": f"{app_module.__name__} (import)"})
        return sorted(routes, key=lambda r: (r["path"], r["method"]))

    def _api_routes_via_ast(self) -> list[dict]:
        """Fallback: AST scan of apps/api/*.py for @router.<method>(path)."""
        routes: list[dict] = []
        api_dir = self.repo_root / "apps" / "api"
        for path in sorted(api_dir.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            prefix = _ast_router_prefix(tree) or ""
            for node in ast.walk(tree):
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                for dec in node.decorator_list:
                    method, route_path = _ast_route_decorator(dec)
                    if method and route_path is not None:
                        routes.append({
                            "method": method.upper(),
                            "path": _join_prefix(prefix, route_path),
                            "source": f"{path.relative_to(self.repo_root).as_posix()}:{node.lineno} (ast)",
                        })
        return sorted(routes, key=lambda r: (r["path"], r["method"]))

    def mcp_tool_inventory(self) -> list[str]:
        """MCP tool names via AST of apps/mcp/main.py (@mcp.tool decorators)."""
        main_py = self.repo_root / "apps" / "mcp" / "main.py"
        if not main_py.exists():
            return []
        tree = ast.parse(main_py.read_text(encoding="utf-8"), filename=str(main_py))
        tools: list[str] = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for dec in node.decorator_list:
                if _is_mcp_tool_decorator(dec):
                    tools.append(node.name)
        return sorted(set(tools))

    def vscode_command_inventory(self) -> list[dict]:
        """VS Code commands from package.json contributes.commands (as data)."""
        pkg = self.repo_root / "apps" / "vscode-extension" / "package.json"
        if not pkg.exists():
            return []
        data = json.loads(pkg.read_text(encoding="utf-8"))
        commands = data.get("contributes", {}).get("commands", [])
        return [
            {"command": c.get("command", ""), "title": c.get("title", "")}
            for c in commands
            if c.get("command")
        ]

    def algorithm_inventory(self) -> list[str]:
        """Public callables of GraphAlgorithms = the algorithm registry."""
        from eoip.graph.algorithms import GraphAlgorithms

        return sorted(
            name for name, _ in inspect.getmembers(GraphAlgorithms, predicate=callable)
            if not name.startswith("_")
        )

    def metric_inventory(self) -> list[str]:
        """Public callables of GraphMetricsEngine = the metrics registry."""
        from eoip.graph.metrics import GraphMetricsEngine

        return sorted(
            name for name, _ in inspect.getmembers(GraphMetricsEngine, predicate=callable)
            if not name.startswith("_")
        )

    def vertex_label_inventory(self) -> list[str]:
        from eoip.ontology.manifest import VERTEX_LABELS

        return sorted(VERTEX_LABELS)

    def edge_label_inventory(self) -> list[str]:
        from eoip.ontology.manifest import EDGE_LABELS

        return sorted(EDGE_LABELS)


# -- AST helpers -------------------------------------------------------------

def _ast_router_prefix(tree: ast.Module) -> str | None:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _attr_name(node.func) == "APIRouter":
            for kw in node.keywords:
                if kw.arg == "prefix" and isinstance(kw.value, ast.Constant):
                    return kw.value.value
    return None


def _ast_route_decorator(dec: ast.AST) -> tuple[str | None, str | None]:
    """Decode @router.<method>("<path>") decorators."""
    if isinstance(dec, ast.Call):
        func = dec.func
        args = dec.args
    else:
        func, args = dec, []
    name = _attr_name(func)
    if not name:
        return None, None
    parts = name.split(".")
    if len(parts) == 2 and parts[1] in ROUTE_DECORATOR_RE and args and isinstance(args[0], ast.Constant):
        return parts[1], args[0].value
    return None, None


def _is_mcp_tool_decorator(dec: ast.AST) -> bool:
    """Match `@mcp.tool` and `@mcp.tool(...)` decorator shapes."""
    node = dec.func if isinstance(dec, ast.Call) else dec
    name = _attr_name(node)
    return bool(name and name.split(".")[-1] == "tool")


def _attr_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _attr_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return None


def _join_prefix(prefix: str, path: str) -> str:
    if not prefix:
        return path
    return f"{prefix.rstrip('/')}/{path.lstrip('/')}"
