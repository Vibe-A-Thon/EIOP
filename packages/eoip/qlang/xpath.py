"""XPath front-end — subset of XPath 1.0 over stored payloads.

Supported subset: absolute paths ``/a/b``, descendant-or-self ``//c``,
predicates ``[@attr='v']`` / ``[@attr="v"]`` on any step, and a trailing
text projection ``/text()``. Payloads are nested dicts (elements map to
child values; lists hold repeated elements). Steps resolve case-sensitively.
"""

from __future__ import annotations

import re
from typing import Any

from eoip.qlang.plans import QLangParseError, QLangPlan

_STEP_RE = re.compile(
    r"""(?P<desc>//|/)(?P<name>[A-Za-z_][\w.-]*|text\(\))(?:\[(?P<pred>@(?P<attr>[A-Za-z_][\w.-]*)\s*=\s*(?P<quote>['\"])(?P<value>.*?)(?P=quote))\])?""",
    re.VERBOSE,
)


def _tokenize(path: str) -> list[dict[str, Any]]:
    if not path.startswith("/"):
        raise QLangParseError("XPath must be an absolute path starting with '/'")
    steps: list[dict[str, Any]] = []
    pos = 0
    while pos < len(path):
        m = _STEP_RE.match(path, pos)
        if not m:
            raise QLangParseError(f"Invalid XPath segment at offset {pos}: {path[pos:]!r}")
        pos = m.end()
        pred = None
        if m.group("pred"):
            pred = {"attr": m.group("attr"), "value": m.group("value")}
        steps.append(
            {
                "axis": "descendant" if m.group("desc") == "//" else "child",
                "name": m.group("name"),
                "predicate": pred,
            }
        )
    return steps


def parse(path: str) -> QLangPlan:
    """Parse an XPath subset expression into a QLangPlan."""
    p = path.strip()
    steps = _tokenize(p)
    if any(s["predicate"] and s["name"] == "text()" for s in steps):
        raise QLangParseError("Predicates on text() steps are not supported in the XPath subset")
    return QLangPlan(
        language="xpath",
        intent="PROJECT",
        operation="XPath",
        source=p,
        extra={"steps": steps},
    )


def _children(node: Any) -> list[Any]:
    if isinstance(node, dict):
        return list(node.values())
    if isinstance(node, (list, tuple)):
        return list(node)
    return []


def evaluate(plan: QLangPlan, payload: Any) -> list[Any]:
    """Evaluate parsed XPath steps against a payload of nested dicts/lists."""

    def _matches(node: Any, step: dict[str, Any]) -> bool:
        name = step["name"]
        if name == "text()":
            return not isinstance(node, (dict, list, tuple))
        if not isinstance(node, dict) or name not in node:
            return False
        pred = step["predicate"]
        if pred is None:
            return True
        child = node[name]
        return (
            isinstance(child, dict)
            and str(child.get(pred["attr"])) == pred["value"]
        )

    def _descend(nodes: list[Any], step: dict[str, Any]) -> list[Any]:
        found: list[Any] = []

        def _walk(node: Any) -> None:
            if _matches(node, step):
                name = step["name"]
                found.append(node[name] if isinstance(node, dict) and name != "text()" else node)
            for child in _children(node):
                _walk(child)

        for n in nodes:
            _walk(n)
        return found

    first = plan.extra["steps"][0]
    if first["axis"] == "descendant":
        current = _descend([payload], first)
    else:
        current = [payload[first["name"]]] if _matches(payload, first) else []

    def _step(nodes: list[Any], step: dict[str, Any]) -> list[Any]:
        out: list[Any] = []
        for node in nodes:
            if isinstance(node, (list, tuple)):
                out.extend(_step(list(node), step))
                continue
            if _matches(node, step):
                name = step["name"]
                out.append(node[name] if isinstance(node, dict) and name != "text()" else node)
        return out

    for step in plan.extra["steps"][1:]:
        if step["axis"] == "descendant":
            current = _descend(current, step)
        else:
            current = _step(current, step)

    out: list[Any] = []
    for node in current:
        if isinstance(node, (list, tuple)):
            out.extend(node)
        else:
            out.append(node)
    return out


def parse_and_evaluate(path: str, payload: Any) -> list[Any]:
    return evaluate(parse(path), payload)
