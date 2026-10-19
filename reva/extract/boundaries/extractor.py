"""Application boundary and resource extraction across Python, JS/TS, and Java (T-501 / REVA-AB-001..013)."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

BoundaryKind = Literal[
    "http_route",
    "http_call",
    "message_publish",
    "message_consume",
    "ipc_channel",
    "rpc_operation",
    "graphql_operation",
    "scheduled_job",
    "cli_command",
]

ResourceKind = Literal[
    "file",
    "db_table",
    "db_view",
    "cache_key",
    "queue",
    "topic",
    "secret",
    "env_var",
    "service_account",
    "config_key",
    "bucket",
]


@dataclass
class BoundaryEndpoint:
    service: str
    kind: BoundaryKind
    method: Optional[str] = None
    path_template: Optional[str] = None
    topic: Optional[str] = None
    source_file: str = ""
    start_line: int = 1
    end_line: int = 1
    logical_key: str = ""
    resolution: str = "complete"  # complete | partial | ambiguous


@dataclass
class ResourceAccess:
    service: str
    resource_kind: ResourceKind
    canonical_name: str
    access_mode: Literal["read", "write", "delete"]
    source_file: str = ""
    start_line: int = 1
    logical_key: str = ""


class PythonBoundaryVisitor(ast.NodeVisitor):
    """AST visitor extracting inbound routes, outbound calls, and resource access from Python code."""

    def __init__(self, service: str, file_path: str):
        self.service = service
        self.file_path = file_path
        self.boundaries: List[BoundaryEndpoint] = []
        self.resources: List[ResourceAccess] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._inspect_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._inspect_function(node)
        self.generic_visit(node)

    def _inspect_function(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]):
        # Check decorators for FastAPI / Flask routes
        for d in node.decorator_list:
            if isinstance(d, ast.Call):
                func = d.func
                method_name = ""
                if isinstance(func, ast.Attribute):
                    method_name = func.attr.upper()
                elif isinstance(func, ast.Name):
                    method_name = func.id.upper()

                if method_name in ("GET", "POST", "PUT", "DELETE", "PATCH", "ROUTE"):
                    path_str = "/"
                    if d.args and isinstance(d.args[0], ast.Constant) and isinstance(d.args[0].value, str):
                        path_str = d.args[0].value
                    elif "path" in [k.arg for k in d.keywords]:
                        for kw in d.keywords:
                            if kw.arg == "path" and isinstance(kw.value, ast.Constant):
                                path_str = str(kw.value.value)

                    route_method = "ANY" if method_name == "ROUTE" else method_name
                    # Check methods=['GET', 'POST'] for Flask
                    for kw in d.keywords:
                        if kw.arg == "methods" and isinstance(kw.value, ast.List):
                            methods = [elt.value for elt in kw.value.elts if isinstance(elt, ast.Constant)]
                            if methods:
                                route_method = ",".join(methods)

                    logical_key = f"bnd:{self.service}/http_route:{route_method} {path_str}"
                    self.boundaries.append(
                        BoundaryEndpoint(
                            service=self.service,
                            kind="http_route",
                            method=route_method,
                            path_template=path_str,
                            source_file=self.file_path,
                            start_line=node.lineno,
                            end_line=getattr(node, "end_lineno", node.lineno),
                            logical_key=logical_key,
                        )
                    )

    def visit_Call(self, node: ast.Call):
        # 1. Outbound HTTP calls (requests, httpx)
        func = node.func
        if isinstance(func, ast.Attribute):
            attr_name = func.attr.lower()
            obj_name = ""
            if isinstance(func.value, ast.Name):
                obj_name = func.value.id.lower()

            if obj_name in ("requests", "httpx", "client", "http") and attr_name in ("get", "post", "put", "delete", "patch"):
                url_str = ""
                if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    url_str = node.args[0].value
                logical_key = f"bnd:{self.service}/http_call:{attr_name.upper()} {url_str}"
                self.boundaries.append(
                    BoundaryEndpoint(
                        service=self.service,
                        kind="http_call",
                        method=attr_name.upper(),
                        path_template=url_str,
                        source_file=self.file_path,
                        start_line=node.lineno,
                        end_line=getattr(node, "end_lineno", node.lineno),
                        logical_key=logical_key,
                    )
                )

            # 2. File and Environment resources
            if attr_name in ("getenv", "get") and obj_name in ("os", "environ"):
                if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    var_name = node.args[0].value
                    self.resources.append(
                        ResourceAccess(
                            service=self.service,
                            resource_kind="env_var",
                            canonical_name=var_name,
                            access_mode="read",
                            source_file=self.file_path,
                            start_line=node.lineno,
                            logical_key=f"res:env_var:{var_name}",
                        )
                    )

        elif isinstance(func, ast.Name):
            # open("filename", "r/w")
            if func.id == "open" and node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                fn = node.args[0].value
                mode = "read"
                if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, str):
                    if any(m in node.args[1].value for m in ("w", "a", "+")):
                        mode = "write"
                self.resources.append(
                    ResourceAccess(
                        service=self.service,
                        resource_kind="file",
                        canonical_name=fn,
                        access_mode=mode,  # type: ignore
                        source_file=self.file_path,
                        start_line=node.lineno,
                        logical_key=f"res:file:{fn}",
                    )
                )

        self.generic_visit(node)


def extract_python_boundaries(
    code_text: str,
    service_name: str,
    file_path: str,
) -> Tuple[List[BoundaryEndpoint], List[ResourceAccess]]:
    """Extract boundaries and resource access from Python source code."""
    try:
        tree = ast.parse(code_text)
    except SyntaxError:
        return [], []

    visitor = PythonBoundaryVisitor(service=service_name, file_path=file_path)
    visitor.visit(tree)
    return visitor.boundaries, visitor.resources


def match_client_server_endpoints(
    outbound_calls: List[BoundaryEndpoint],
    inbound_routes: List[BoundaryEndpoint],
) -> List[Dict[str, Any]]:
    """Match client outbound HTTP calls to server inbound routes (REVA-AB-009)."""
    matches: List[Dict[str, Any]] = []

    for call in outbound_calls:
        if call.kind != "http_call" or not call.path_template:
            continue

        call_path = call.path_template
        # Normalize template segments: /users/{id} or /users/123
        call_method = (call.method or "GET").upper()

        best_match = None
        best_score = 0.0

        for route in inbound_routes:
            if route.kind != "http_route" or not route.path_template:
                continue

            # Method check
            route_methods = [m.strip().upper() for m in (route.method or "GET").split(",")]
            if call_method not in route_methods and "ANY" not in route_methods:
                continue

            route_path = route.path_template
            # Exact path match
            if call_path == route_path or call_path.endswith(route_path):
                score = 0.95
            elif len(call_path.strip("/").split("/")) == len(route_path.strip("/").split("/")):
                score = 0.75
            else:
                score = 0.0

            if score > best_score:
                best_score = score
                best_match = route

        if best_match and best_score >= 0.70:
            matches.append({
                "client_call": call.logical_key,
                "confidence_score": best_score,
                "server_route": best_match.logical_key,
                "service_client": call.service,
                "service_server": best_match.service,
            })

    return matches
