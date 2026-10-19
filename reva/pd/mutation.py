"""AST mutation testing engine for Python owners (T-211 / REVA-PD-005 / AG-04 / D-14)."""

from __future__ import annotations

import ast
import copy
import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

COMPARE_SWAPS = {
    ast.Lt: ast.LtE,
    ast.LtE: ast.Lt,
    ast.Gt: ast.GtE,
    ast.GtE: ast.Gt,
    ast.Eq: ast.NotEq,
    ast.NotEq: ast.Eq,
    ast.In: ast.NotIn,
    ast.NotIn: ast.In,
    ast.Is: ast.IsNot,
    ast.IsNot: ast.Is,
}

BINOP_SWAPS = {
    ast.Add: ast.Sub,
    ast.Sub: ast.Add,
    ast.Mult: ast.FloorDiv,
    ast.FloorDiv: ast.Mult,
    ast.Div: ast.Mult,
    ast.Mod: ast.Mult,
}

BOOLOP_SWAPS = {
    ast.And: ast.Or,
    ast.Or: ast.And,
}


@dataclass
class MutationSite:
    site_id: str
    operator_id: str
    lineno: int
    col_offset: int
    transform: Callable[[ast.AST], ast.AST]


class MutationFinder(ast.NodeVisitor):
    """Identifies and indexes applicable mutation sites inside an AST subtree."""

    def __init__(self):
        self.sites: List[MutationSite] = []

    def visit_Compare(self, node: ast.Compare):
        for idx, op in enumerate(node.ops):
            op_type = type(op)
            if op_type in COMPARE_SWAPS:
                target_op = COMPARE_SWAPS[op_type]

                def make_transform(o_idx, t_op):
                    def _tf(root):
                        new_ops = list(root.ops)
                        new_ops[o_idx] = t_op()
                        root.ops = new_ops
                        return root
                    return _tf

                self.sites.append(
                    MutationSite(
                        site_id=f"compare_{node.lineno}_{node.col_offset}_{idx}",
                        operator_id="CompareSwap",
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                        transform=make_transform(idx, target_op),
                    )
                )
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp):
        op_type = type(node.op)
        if op_type in BINOP_SWAPS:
            target_op = BINOP_SWAPS[op_type]

            def _tf(root):
                root.op = target_op()
                return root

            self.sites.append(
                MutationSite(
                    site_id=f"binop_{node.lineno}_{node.col_offset}",
                    operator_id="BinOpSwap",
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                    transform=_tf,
                )
            )
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp):
        op_type = type(node.op)
        if op_type in BOOLOP_SWAPS:
            target_op = BOOLOP_SWAPS[op_type]

            def _tf(root):
                root.op = target_op()
                return root

            self.sites.append(
                MutationSite(
                    site_id=f"boolop_{node.lineno}_{node.col_offset}",
                    operator_id="BoolOpSwap",
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                    transform=_tf,
                )
            )
        self.generic_visit(node)

    def visit_Return(self, node: ast.Return):
        if node.value is not None:
            def _tf(root):
                root.value = None
                return root

            self.sites.append(
                MutationSite(
                    site_id=f"return_{node.lineno}_{node.col_offset}",
                    operator_id="ReturnNone",
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                    transform=_tf,
                )
            )
        self.generic_visit(node)


@dataclass
class MutationResult:
    owner_digest: str
    generated: int
    killed: int
    survived: int
    timeout: int
    waived: int
    score: float


def generate_mutants(
    source_code: str,
    symbol_name: str,
    max_mutants: int = 60,
    seed: Optional[str] = None,
) -> List[Tuple[str, str]]:
    """Locate symbol in source, find mutation sites, and generate mutated source texts."""
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return []

    # Locate target node
    target_node = None
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name == symbol_name or symbol_name.endswith("." + node.name):
                target_node = node
                break

    if target_node is None:
        target_node = tree  # fallback to entire module

    finder = MutationFinder()
    finder.visit(target_node)
    sites = finder.sites

    # Sort deterministically
    sites.sort(key=lambda s: (s.lineno, s.col_offset, s.operator_id))

    if len(sites) > max_mutants:
        sites = sites[:max_mutants]

    mutants: List[Tuple[str, str]] = []
    for site in sites:
        tree_copy = copy.deepcopy(tree)
        # Find corresponding node in copy
        matched = False
        for node in ast.walk(tree_copy):
            if (
                getattr(node, "lineno", -1) == site.lineno
                and getattr(node, "col_offset", -1) == site.col_offset
            ):
                try:
                    site.transform(node)
                    mutants.append((site.site_id, ast.unparse(tree_copy)))
                    matched = True
                    break
                except Exception:
                    pass
        if not matched:
            pass

    return mutants
