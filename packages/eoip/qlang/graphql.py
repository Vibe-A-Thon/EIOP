"""GraphQL query-subset front-end — typed selection over the ontology schema.

Supported subset:
  query { Label { scalarField relatedField { field ... } ... } }

* Root field names are validated against ``VERTEX_LABELS`` (typed selection).
* Nested object fields resolve through outgoing edges whose label matches the
  field name (case-insensitive); nested scalars project vertex properties.
* ``__typename`` and ``__count`` meta fields are supported.

Execution runs against the GraphStore. Deterministic — no external GraphQL
server or resolver engine.
"""

from __future__ import annotations

import re
from typing import Any

from eoip.graph.store import GraphStore
from eoip.ontology.manifest import EDGE_LABELS, VERTEX_LABELS
from eoip.qlang.plans import QLangParseError, QLangPlan

_TOKEN = re.compile(r"\s*(?:(?P<name>[_A-Za-z][_A-Za-z0-9]*)|(?P<lbrace>\{)|(?P<rbrace>\}))")


def _parse_selection(text: str, pos: int = 0) -> tuple[list[dict[str, Any]], int]:
    selections: list[dict[str, Any]] = []
    while True:
        m = _TOKEN.match(text, pos)
        if not m:
            if text[pos:].strip() == "":
                raise QLangParseError("Unbalanced braces in GraphQL selection")
            raise QLangParseError(f"Unexpected GraphQL token at offset {pos}: {text[pos:]!r}")
        pos = m.end()
        if m.group("lbrace") is not None:
            raise QLangParseError("Unexpected '{' in GraphQL selection")
        if m.group("rbrace") is not None:
            return selections, pos
        name = m.group("name")
        nxt = _TOKEN.match(text, pos)
        if nxt and nxt.group("lbrace") is not None:
            children, pos = _parse_selection(text, nxt.end())
            selections.append({"name": name, "children": children})
        else:
            selections.append({"name": name, "children": []})


def parse(query: str) -> QLangPlan:
    """Parse a GraphQL query subset into a QLangPlan."""
    q = query.strip()
    if q.startswith("query"):
        rest = q[5:].strip()
        if rest and not rest.startswith("{"):
            raise QLangParseError("Named/anonymous GraphQL operation names are outside the subset")
        q = rest
    if not q.startswith("{"):
        raise QLangParseError("GraphQL subset expects a selection set starting with '{'")
    selections, pos = _parse_selection(q, 1)
    if q[pos:].strip():
        raise QLangParseError(f"Trailing GraphQL content: {q[pos:]!r}")
    if len(selections) != 1:
        raise QLangParseError("GraphQL subset expects exactly one root field")
    root = selections[0]
    if root["children"] is not None and root["name"] not in VERTEX_LABELS:
        raise QLangParseError(
            f"Unknown GraphQL root type: {root['name']!r}; known types: {sorted(VERTEX_LABELS)}"
        )
    return QLangPlan(
        language="graphql",
        intent="SEARCH",
        operation="GraphQL",
        source=query.strip(),
        projection=[s["name"] for s in root["children"] if not s["children"]],
        extra={"root": root},
    )


def _edge_label_for(field: str) -> str | None:
    for label in EDGE_LABELS:
        if label.casefold() == field.casefold():
            return label
    return None


def _resolve(store: GraphStore, vertex: dict[str, Any], selections: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    props = vertex["properties"]
    for sel in selections:
        name = sel["name"]
        if name == "__typename":
            out[name] = vertex["label"]
            continue
        if sel["children"]:
            edge_label = _edge_label_for(name)
            if edge_label is None:
                raise QLangParseError(f"No edge type matches GraphQL field: {name!r}")
            related = []
            for edge in store.edges_from(vertex["vid"], labels=[edge_label], limit=100):
                target = store.get_vertex(edge["in_v"])
                if target:
                    related.append(_resolve(store, target, sel["children"]))
            out[name] = related
        else:
            out[name] = props.get(name)
    return out


def execute(plan: QLangPlan, store: GraphStore, *, limit: int = 50) -> dict[str, Any]:
    """Execute a parsed GraphQL query against the GraphStore."""
    root = plan.extra["root"]
    vertices = store.find_vertices(label=root["name"], limit=limit)
    data = [
        _resolve(store, v, root["children"])
        for v in vertices
    ]
    return {"data": {root["name"]: data}, "count": len(data)}


def parse_and_execute(query: str, store: GraphStore) -> dict[str, Any]:
    return execute(parse(query), store)
