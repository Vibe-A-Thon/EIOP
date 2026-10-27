"""
Pure-Python AST Code Analyzer & Knowledge Graph Extractor (REVA-AB-014, T-ENH-004).
Performs deterministic static analysis of codebases to construct comprehensive Knowledge Graphs:
- Modules, Classes, Functions, and API Endpoints
- Call Graph & Cross-Module Dependencies
- Zero LLM required; 100% local, deterministic, and memory-safe.
"""

from __future__ import annotations

import ast
import hashlib
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class KnowledgeGraphEntity:
    id: str
    kind: str
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeGraphEdge:
    source_id: str
    target_id: str
    relation: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeGraph:
    repo_id: str
    root_path: str
    vertices: List[KnowledgeGraphEntity] = field(default_factory=list)
    edges: List[KnowledgeGraphEdge] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "repo_id": self.repo_id,
            "root_path": self.root_path,
            "metrics": self.metrics,
            "vertices_count": len(self.vertices),
            "edges_count": len(self.edges),
            "vertices": [
                {
                    "id": v.id,
                    "kind": v.kind,
                    "name": v.name,
                    "properties": v.properties,
                }
                for v in self.vertices
            ],
            "edges": [
                {
                    "source_id": e.source_id,
                    "target_id": e.target_id,
                    "relation": e.relation,
                    "properties": e.properties,
                }
                for e in self.edges
            ],
        }


class CodeASTVisitor(ast.NodeVisitor):
    """AST Visitor that traverses Python modules to discover functions, classes, calls, and endpoints."""

    def __init__(self, rel_path: str, mod_id: str) -> None:
        self.rel_path = rel_path
        self.mod_id = mod_id
        self.current_class: Optional[str] = None
        self.current_function: Optional[str] = None

        self.classes: List[Dict[str, Any]] = []
        self.functions: List[Dict[str, Any]] = []
        self.imports: List[Dict[str, Any]] = []
        self.calls: List[Tuple[str, str]] = []  # (caller_id, callee_name)
        self.endpoints: List[Dict[str, Any]] = []

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.imports.append({
                "module": alias.name,
                "asname": alias.asname,
                "lineno": node.lineno,
                "is_from": False,
            })
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module or ""
        for alias in node.names:
            self.imports.append({
                "module": module,
                "name": alias.name,
                "asname": alias.asname,
                "lineno": node.lineno,
                "is_from": True,
            })
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        cls_id = f"cls:{self.rel_path}::{node.name}"
        bases = [self._format_expr(b) for b in node.bases]
        decorators = [self._format_expr(d) for d in node.decorator_list]
        docstring = ast.get_docstring(node) or ""

        self.classes.append({
            "id": cls_id,
            "name": node.name,
            "bases": bases,
            "decorators": decorators,
            "docstring": docstring,
            "lineno": node.lineno,
            "end_lineno": getattr(node, "end_lineno", node.lineno),
        })

        prev_class = self.current_class
        self.current_class = cls_id
        self.generic_visit(node)
        self.current_class = prev_class

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._handle_func(node, is_async=False)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._handle_func(node, is_async=True)

    def _handle_func(self, node: ast.FunctionDef | ast.AsyncFunctionDef, is_async: bool) -> None:
        if self.current_class:
            func_id = f"{self.current_class}.{node.name}"
        else:
            func_id = f"fn:{self.rel_path}::{node.name}"

        decorators = [self._format_expr(d) for d in node.decorator_list]
        docstring = ast.get_docstring(node) or ""
        params = [arg.arg for arg in node.args.args]
        return_type = self._format_expr(node.returns) if node.returns else None

        # Calculate cyclomatic complexity
        complexity = 1
        for sub in ast.walk(node):
            if isinstance(sub, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler, ast.With, ast.AsyncWith)):
                complexity += 1
            elif isinstance(sub, ast.BoolOp):
                complexity += len(sub.values) - 1

        func_info = {
            "id": func_id,
            "name": node.name,
            "class_id": self.current_class,
            "is_async": is_async,
            "params": params,
            "return_type": return_type,
            "decorators": decorators,
            "docstring": docstring,
            "complexity": complexity,
            "lineno": node.lineno,
            "end_lineno": getattr(node, "end_lineno", node.lineno),
        }
        self.functions.append(func_info)

        # Detect REST API Endpoint decorators (FastAPI, Flask, etc.)
        for dec in decorators:
            for http_method in ("get", "post", "put", "delete", "patch", "options", "head", "route"):
                dec_low = dec.lower()
                if f".{http_method}(" in dec_low or dec_low.startswith((f"{http_method}(", f"@{http_method}(")) or f"api.{http_method}" in dec_low:
                    # Extract path if quoted string in decorator
                    path = "/"
                    import re
                    m = re.search(r"['\"](/[^'\"]*)['\"]", dec)
                    if m:
                        path = m.group(1)
                    endpoint_id = f"ep:{http_method.upper()}:{path}"
                    self.endpoints.append({
                        "id": endpoint_id,
                        "method": http_method.upper(),
                        "path": path,
                        "handler_id": func_id,
                        "handler_name": node.name,
                    })

        prev_func = self.current_function
        self.current_function = func_id
        self.generic_visit(node)
        self.current_function = prev_func

    def visit_Call(self, node: ast.Call) -> None:
        callee = self._format_expr(node.func)
        if self.current_function and callee:
            self.calls.append((self.current_function, callee))
        self.generic_visit(node)

    def _format_expr(self, node: Optional[ast.AST]) -> str:
        if node is None:
            return ""
        try:
            return ast.unparse(node)
        except Exception:
            if isinstance(node, ast.Name):
                return node.id
            elif isinstance(node, ast.Attribute):
                val = self._format_expr(node.value)
                return f"{val}.{node.attr}" if val else node.attr
            elif isinstance(node, ast.Constant):
                return repr(node.value) if isinstance(node.value, str) else str(node.value)
            elif isinstance(node, ast.Call):
                func = self._format_expr(node.func)
                args = [self._format_expr(a) for a in node.args]
                return f"{func}({', '.join(args)})"
            return ""


class CodeASTAnalyzer:
    """
    Main Code AST Analyzer: scans entire repository, extracts AST metrics,
    and synthesizes a connected Knowledge Graph.
    """

    EXCLUDED_DIRS = {
        ".git", ".venv", "venv", "env", "__pycache__", "node_modules",
        "dist", "build", ".pytest_cache", ".ruff_cache", ".hypothesis",
        ".egg-info", "eggs", "site-packages"
    }

    def __init__(self, max_file_bytes: int = 5 * 1024 * 1024) -> None:
        self.max_file_bytes = max_file_bytes

    def analyze_repository(self, root_path: str, repo_id: str) -> KnowledgeGraph:
        """
        Analyzes all source files in the repository and generates the Knowledge Graph.
        """
        abs_root = os.path.abspath(root_path)
        kg = KnowledgeGraph(repo_id=repo_id, root_path=abs_root)

        total_files = 0
        total_loc = 0
        python_files = []

        # 1. Discover all Python files
        for root, dirs, files in os.walk(abs_root):
            dirs[:] = [d for d in dirs if d not in self.EXCLUDED_DIRS]
            for f in files:
                if f.endswith(".py"):
                    full_p = os.path.join(root, f)
                    try:
                        sz = os.path.getsize(full_p)
                        if sz <= self.max_file_bytes:
                            python_files.append(full_p)
                    except OSError:
                        pass

        # Global lookup index for symbol resolution
        func_lookup: Dict[str, str] = {}  # name -> func_id
        class_lookup: Dict[str, str] = {} # name -> class_id

        # 2. Parse each Python file
        for file_path in python_files:
            rel_path = os.path.relpath(file_path, abs_root).replace("\\", "/")
            mod_id = f"mod:{rel_path}"

            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as fh:
                    source_content = fh.read()
            except Exception:
                continue

            lines = source_content.splitlines()
            loc = len(lines)
            total_loc += loc
            total_files += 1

            digest = hashlib.sha256(source_content.encode("utf-8")).hexdigest()

            # Create Module Vertex
            kg.vertices.append(KnowledgeGraphEntity(
                id=mod_id,
                kind="kg_Module",
                name=rel_path,
                properties={
                    "file_path": rel_path,
                    "loc": loc,
                    "sha256": digest,
                }
            ))

            # Parse AST
            try:
                tree = ast.parse(source_content, filename=rel_path)
            except SyntaxError:
                continue

            visitor = CodeASTVisitor(rel_path=rel_path, mod_id=mod_id)
            visitor.visit(tree)

            # Process Classes
            for cls_data in visitor.classes:
                cls_id = cls_data["id"]
                class_lookup[cls_data["name"]] = cls_id
                kg.vertices.append(KnowledgeGraphEntity(
                    id=cls_id,
                    kind="kg_Class",
                    name=cls_data["name"],
                    properties={
                        "module_id": mod_id,
                        "bases": cls_data["bases"],
                        "decorators": cls_data["decorators"],
                        "docstring": cls_data["docstring"],
                        "lineno": cls_data["lineno"],
                    }
                ))
                kg.edges.append(KnowledgeGraphEdge(
                    source_id=mod_id,
                    target_id=cls_id,
                    relation="CONTAINS",
                ))
                for base in cls_data["bases"]:
                    kg.edges.append(KnowledgeGraphEdge(
                        source_id=cls_id,
                        target_id=base,
                        relation="INHERITS_FROM",
                    ))

            # Process Functions
            for fn_data in visitor.functions:
                fn_id = fn_data["id"]
                func_lookup[fn_data["name"]] = fn_id
                kg.vertices.append(KnowledgeGraphEntity(
                    id=fn_id,
                    kind="kg_Function",
                    name=fn_data["name"],
                    properties={
                        "module_id": mod_id,
                        "class_id": fn_data["class_id"],
                        "is_async": fn_data["is_async"],
                        "params": fn_data["params"],
                        "return_type": fn_data["return_type"],
                        "decorators": fn_data["decorators"],
                        "complexity": fn_data["complexity"],
                        "lineno": fn_data["lineno"],
                    }
                ))
                parent_id = fn_data["class_id"] or mod_id
                kg.edges.append(KnowledgeGraphEdge(
                    source_id=parent_id,
                    target_id=fn_id,
                    relation="CONTAINS",
                ))

            # Process API Endpoints
            for ep in visitor.endpoints:
                ep_id = ep["id"]
                kg.vertices.append(KnowledgeGraphEntity(
                    id=ep_id,
                    kind="kg_Endpoint",
                    name=f"{ep['method']} {ep['path']}",
                    properties={
                        "method": ep["method"],
                        "path": ep["path"],
                        "handler_id": ep["handler_id"],
                    }
                ))
                kg.edges.append(KnowledgeGraphEdge(
                    source_id=ep["handler_id"],
                    target_id=ep_id,
                    relation="EXPOSES_ENDPOINT",
                ))

            # Process Imports
            for imp in visitor.imports:
                target_mod = imp["module"]
                if target_mod:
                    kg.edges.append(KnowledgeGraphEdge(
                        source_id=mod_id,
                        target_id=f"pkg:{target_mod}",
                        relation="IMPORTS",
                        properties={"asname": imp.get("asname"), "lineno": imp["lineno"]},
                    ))

            # Process Function Calls
            for caller_id, callee_name in visitor.calls:
                target_id = func_lookup.get(callee_name, callee_name)
                kg.edges.append(KnowledgeGraphEdge(
                    source_id=caller_id,
                    target_id=target_id,
                    relation="CALLS",
                ))

        kg.metrics = {
            "total_python_files": total_files,
            "total_loc": total_loc,
            "total_vertices": len(kg.vertices),
            "total_edges": len(kg.edges),
            "total_classes": len([v for v in kg.vertices if v.kind == "kg_Class"]),
            "total_functions": len([v for v in kg.vertices if v.kind == "kg_Function"]),
            "total_endpoints": len([v for v in kg.vertices if v.kind == "kg_Endpoint"]),
        }

        return kg
