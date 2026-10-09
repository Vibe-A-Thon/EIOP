"""JSONPath front-end — RFC 9535 subset over stored payloads.

Supported subset: root ``$``, child ``.name`` / ``['name']``, wildcard
``.`` / ``[*]``, index ``[n]``, slice ``[a:b]``, descendant ``..name``.

Parses to a ``QLangPlan`` (PROJECT/FILTER intent with path steps in
``extra['steps']``) and can evaluate directly against a payload fixture.
"""

from __future__ import annotations

import re
from typing import Any

from eoip.qlang.plans import QLangParseError, QLangPlan

_TOKEN = re.compile(
    r"""
    (?P<name>\.[A-Za-z_][A-Za-z0-9_-]*)
    |(?P<desc>\.\.[A-Za-z_][A-Za-z0-9_-]*)
    |(?P<wcard>\.\*|\[\*\])
    |(?P<bracket>\[(?:'[^']*'|"[^"]*"|-?\d+|-?\d*:-?\d*)\])
    """,
    re.VERBOSE,
)


def _tokenize(path: str) -> list[tuple[str, Any]]:
    if not path.startswith("$"):
        raise QLangParseError("JSONPath must start with '$'")
    pos, steps = 1, []
    while pos < len(path):
        m = _TOKEN.match(path, pos)
        if not m:
            raise QLangParseError(f"Invalid JSONPath segment at offset {pos}: {path[pos:]!r}")
        pos = m.end()
        if m.lastgroup == "name":
            steps.append(("child", m.group()[1:]))
        elif m.lastgroup == "desc":
            steps.append(("descend", m.group()[2:]))
        elif m.lastgroup == "wcard":
            steps.append(("wildcard", None))
        else:
            inner = m.group()[1:-1].strip()
            if (inner.startswith("'") and inner.endswith("'")) or (
                inner.startswith('"') and inner.endswith('"')
            ):
                steps.append(("child", inner[1:-1]))
            elif ":" in inner:
                a, _, b = inner.partition(":")
                steps.append(
                    ("slice", (int(a) if a else None, int(b) if b else None))
                )
            else:
                steps.append(("index", int(inner)))
    return steps


def parse(path: str) -> QLangPlan:
    """Parse a JSONPath expression into a QLangPlan (RFC 9535 subset)."""
    steps = _tokenize(path.strip())
    return QLangPlan(
        language="jsonpath",
        intent="PROJECT",
        operation="JSONPath",
        source=path.strip(),
        projection=[s[1] for s in steps if s[0] == "child" and s[1] is not None],
        extra={"steps": steps},
    )


def evaluate(plan: QLangPlan, payload: Any) -> list[Any]:
    """Evaluate parsed steps against a payload; always returns a list of matches."""

    def _children(node: Any) -> list[Any]:
        if isinstance(node, dict):
            return list(node.values())
        if isinstance(node, (list, tuple)):
            return list(node)
        return []

    current = [payload]
    for kind, arg in plan.extra["steps"]:
        nxt: list[Any] = []
        if kind == "child":
            for node in current:
                if isinstance(node, dict) and arg in node:
                    nxt.append(node[arg])
        elif kind == "index":
            for node in current:
                if isinstance(node, (list, tuple)) and -len(node) <= arg < len(node):
                    nxt.append(node[arg])
        elif kind == "slice":
            for node in current:
                if isinstance(node, (list, tuple)):
                    nxt.extend(node[arg[0]:arg[1]])
        elif kind == "wildcard":
            for node in current:
                nxt.extend(_children(node))
        elif kind == "descend":
            stack = list(current)
            while stack:
                node = stack.pop()
                if isinstance(node, dict) and arg in node:
                    nxt.append(node[arg])
                stack.extend(_children(node))
        current = nxt
    return current


def parse_and_evaluate(path: str, payload: Any) -> list[Any]:
    """Convenience: parse + evaluate in one call."""
    return evaluate(parse(path), payload)
