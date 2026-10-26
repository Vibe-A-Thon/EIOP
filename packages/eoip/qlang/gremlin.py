"""Gremlin traversal-builder front-end (fluent subset).

Supported steps: ``g.V()`` / ``g.V(id)``, ``hasLabel('L')``,
``has('k','v')``, ``out('E')`` / ``in('E')``, ``limit(n)``, ``path()``,
``count()``. Parses a fluent traversal string into a QLangPlan whose
``extra['steps']`` drive deterministic execution against the GraphStore.
Variable bindings, lambdas, and side-effects are outside the subset and are
rejected — never silently faked.
"""

from __future__ import annotations

import re
from typing import Any

from eoip.graph.store import GraphStore
from eoip.qlang.plans import QLangParseError, QLangPlan

_STEP = re.compile(
    r"^(V|hasLabel|has|out|in|limit|path|count|values)\s*(?:\((.*?)\))?$", re.DOTALL
)


def _args(raw: str | None) -> list[str]:
    if raw is None or not raw.strip():
        return []
    out = []
    for part in raw.split(","):
        part = part.strip()
        if (part.startswith("'") and part.endswith("'")) or (part.startswith('"') and part.endswith('"')):
            out.append(part[1:-1])
        else:
            out.append(part)
    return out


def _split_steps(text: str) -> list[str]:
    """Split a traversal body on dots that are outside quoted strings."""
    parts, current, quote = [], [], None
    for ch in text:
        if quote:
            current.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
            current.append(ch)
        elif ch == ".":
            parts.append("".join(current))
            current = []
        else:
            current.append(ch)
    if current:
        parts.append("".join(current))
    return [p for p in parts if p]


def parse(query: str) -> QLangPlan:
    """Parse a fluent Gremlin traversal string into a QLangPlan."""
    q = re.sub(r"\s+", "", query.strip())
    if not q.startswith("g."):
        raise QLangParseError("Gremlin traversal must start with 'g.'")
    steps: list[dict[str, Any]] = []
    for raw in _split_steps(q[2:]):
        m = _STEP.match(raw)
        if not m:
            raise QLangParseError(f"Unsupported Gremlin step: {raw!r}")
        steps.append({"name": m.group(1), "args": _args(m.group(2))})
    if not steps or steps[0]["name"] != "V":
        raise QLangParseError("Gremlin traversal must start with g.V()")
    labels = [s["args"][0] for s in steps if s["name"] == "hasLabel" and s["args"]]
    edge_labels = [a for s in steps if s["name"] in ("out", "in") for a in s["args"]]
    anchors = list(steps[0]["args"])
    limit = next(
        (int(s["args"][0]) for s in reversed(steps) if s["name"] == "limit" and s["args"]), 50
    )
    return QLangPlan(
        language="gremlin",
        intent="NEIGHBORHOOD",
        operation="Gremlin",
        source=query.strip(),
        anchors=anchors,
        edge_labels=edge_labels,
        limit=limit,
        extra={"steps": steps},
    )


def execute(plan: QLangPlan, store: GraphStore) -> dict[str, Any]:
    """Execute a parsed Gremlin traversal against the GraphStore."""
    steps = plan.extra["steps"]
    current: list[dict[str, Any]] = []
    paths: list[list[str]] = []
    terminal = steps[-1]["name"]

    seed = steps[0]["args"]
    if seed:
        v = store.get_vertex_by_canonical_id(seed[0])
        current = [v] if v else []
    else:
        current = store.find_vertices(limit=500)
    paths = [[v["vid"]] for v in current]

    for step in steps[1:]:
        name, args = step["name"], step["args"]
        if name == "hasLabel":
            pairs = [(v, p) for v, p in zip(current, paths) if v["label"] in args]
            current = [v for v, _ in pairs]
            paths = [p for _, p in pairs]
        elif name == "has":
            if len(args) != 2:
                raise QLangParseError("Gremlin has() requires exactly (key, value)")
            pairs = [(v, p) for v, p in zip(current, paths)
                     if str(v["properties"].get(args[0])) == args[1]]
            current = [v for v, _ in pairs]
            paths = [p for _, p in pairs]
        elif name in ("out", "in"):
            nxt, nxt_paths = [], []
            for v, path in zip(current, paths):
                edges = (
                    store.edges_from(v["vid"], labels=args or None, limit=100)
                    if name == "out"
                    else store.edges_to(v["vid"], labels=args or None, limit=100)
                )
                for e in edges:
                    other_id = e["in_v"] if name == "out" else e["out_v"]
                    other = store.get_vertex(other_id)
                    if other:
                        nxt.append(other)
                        nxt_paths.append(path + [other["vid"]])
            current, paths = nxt, nxt_paths
        elif name == "limit":
            n = int(args[0]) if args else 0
            current, paths = current[:n], paths[:n]
        elif name in ("path", "count"):
            continue
        else:
            raise QLangParseError(f"Unsupported Gremlin step at execution: {name!r}")

    if terminal == "count":
        return {"language": "gremlin", "operation": "count", "result": len(current)}
    if terminal == "path":
        resolved = []
        for path in paths:
            nodes = []
            for vid in path:
                v = store.get_vertex(vid)
                if v:
                    nodes.append({
                        "canonical_id": v["properties"].get("canonical_id", vid),
                        "label": v["label"],
                        "name": v["properties"].get("name"),
                    })
            resolved.append(nodes)
        return {"language": "gremlin", "operation": "path", "result": resolved}
    return {
        "language": "gremlin",
        "operation": "traversal",
        "result": [
            {"canonical_id": v["properties"].get("canonical_id", v["vid"]),
             "label": v["label"], "properties": v["properties"]}
            for v in current
        ],
        "count": len(current),
    }


def parse_and_execute(query: str, store: GraphStore) -> dict[str, Any]:
    return execute(parse(query), store)
