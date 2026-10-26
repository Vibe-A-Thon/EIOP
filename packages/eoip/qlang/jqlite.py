"""jq-lite front-end — subset of the jq expression language.

Supported subset: pipes ``a | b``, identity ``.``, field access ``.name``,
optional iterate ``.[]``, array indexing ``.name[0]``, and
``select(.field == "v" | .field != v)`` filters. Anything beyond the subset
(e.g. ``map``, ``reduce``, string interpolation) is rejected with
``QLangParseError`` — this is a subset, not a fake full jq.
"""

from __future__ import annotations

import re
from typing import Any

from eoip.qlang.plans import QLangParseError, QLangPlan

_STAGE = re.compile(
    r"^(?:\.?(?P<field>[A-Za-z_][A-Za-z0-9_-]*(?:\.[A-Za-z_][A-Za-z0-9_-]*)*)(?P<iterate>\[\])?(?P<index>\[-?\d+\])?|select\((?P<select>.+)\))$"
)


def _parse_stage(raw: str) -> dict[str, Any]:
    raw = raw.strip()
    if raw in (".[]", "[]"):
        return {"kind": "identity", "field": None, "iterate": True, "index": None}
    m = _STAGE.match(raw)
    if not m:
        raise QLangParseError(f"Unsupported jq-lite stage: {raw!r}")
    if m.group("select") is not None:
        cond = m.group("select").strip()
        cm = re.match(r"^\.([A-Za-z_][A-Za-z0-9_-]*)\s*(==|!=|>=|<=|>|<)\s*(.+?)$", cond)
        if not cm:
            raise QLangParseError(f"Unsupported jq-lite select condition: {cond!r}")
        field, op, raw_val = cm.groups()
        return {"kind": "select", "field": field, "op": op, "value": _literal(raw_val)}
    kind = "identity"
    if m.group("field"):
        kind = "field"
    elif raw not in (".", ".[]"):
        raise QLangParseError(f"Unsupported jq-lite stage: {raw!r}")
    return {
        "kind": kind,
        "field": m.group("field"),
        "iterate": bool(m.group("iterate")),
        "index": int(m.group("index")[1:-1]) if m.group("index") else None,
    }


def _literal(raw: str) -> Any:
    raw = raw.strip()
    if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
        return raw[1:-1]
    try:
        return int(raw)
    except ValueError:
        try:
            return float(raw)
        except ValueError:
            if raw in ("true", "false"):
                return raw == "true"
            if raw == "null":
                return None
            raise QLangParseError(f"Unsupported jq-lite literal: {raw!r}")


def parse(query: str) -> QLangPlan:
    """Parse a jq-lite pipeline into a QLangPlan."""
    q = query.strip()
    if q == ".":
        stages: list[dict[str, Any]] = []
    else:
        parts = [p.strip() for p in q.split("|")]
        if parts and parts[0] in (".", ""):
            parts = parts[1:]
        stages = [_parse_stage(p) for p in parts if p not in ("", ".")]
    return QLangPlan(
        language="jq",
        intent="PROJECT",
        operation="jq-lite",
        source=q,
        extra={"stages": stages},
    )


def evaluate(plan: QLangPlan, payload: Any) -> list[Any]:
    """Evaluate a jq-lite pipeline against a payload."""

    def _values(stage: dict[str, Any], node: Any) -> list[Any]:
        kind = stage["kind"]
        if kind == "identity":
            out = [node]
        elif kind == "field":
            out = [node]
            for part in stage["field"].split("."):
                out = [item[part] for item in out if isinstance(item, dict) and part in item]
        else:
            out = []
        if stage.get("iterate") and out:
            iterated: list[Any] = []
            for item in out:
                if isinstance(item, (list, tuple)):
                    iterated.extend(item)
                elif isinstance(item, dict):
                    iterated.extend(item.values())
            out = iterated
        if stage.get("index") is not None and out:
            idx = stage["index"]
            out = [
                item[idx]
                for item in out
                if isinstance(item, (list, tuple)) and -len(item) <= idx < len(item)
            ]
        return out

    current = [payload]
    for stage in plan.extra["stages"]:
        if stage["kind"] == "select":
            field, op, val = stage["field"], stage["op"], stage["value"]

            def _sel(node: Any) -> bool:
                if not isinstance(node, dict):
                    return False
                actual = node.get(field)
                if op in (">", "<", ">=", "<="):
                    try:
                        a, b = float(actual), float(val)
                    except (TypeError, ValueError):
                        return False
                    return {">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b}[op]
                return (actual == val) if op == "==" else (actual != val)

            current = [node for node in current if _sel(node)]
        else:
            nxt: list[Any] = []
            for node in current:
                nxt.extend(_values(stage, node))
            current = nxt
    return current


def parse_and_evaluate(query: str, payload: Any) -> list[Any]:
    return evaluate(parse(query), payload)
