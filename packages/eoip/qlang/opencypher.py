"""openCypher front-end — MATCH / WHERE / RETURN subset with optional hops.

Supported subset:
  MATCH (a:Label)-[r:REL]->(b:Label)          fixed hop
  MATCH (a:Label)-[r:REL*1..3]->(b:Label)     variable hops (cap enforced)
  WHERE a.prop = 'v' AND b.other != 'w'
  RETURN a, b | RETURN a.prop, b.other

Execution runs a bounded BFS over the GraphStore. Variable-length hops are
capped (default 8) mirroring the platform traversal policy. Labels and
relationships may be omitted (``(a)-[r]->(b)``) but at least one bound is
required to keep execution deterministic.
"""

from __future__ import annotations

import re
from typing import Any

from eoip.graph.store import GraphStore
from eoip.qlang.plans import QLangParseError, QLangPlan

_MATCH = re.compile(
    r"^MATCH\s*\(\s*(?P<src>[A-Za-z_]\w*)\s*(?::\s*(?P<src_label>\w+)\s*)?\)"
    r"\s*-\s*\[\s*(?P<rel>[A-Za-z_]\w*)?\s*(?::\s*(?P<rel_label>[A-Za-z_]\w*)\s*)?"
    r"(?:\*\s*(?P<min>\d+)?\s*\.\.\s*(?P<max>\d+)?)?\]\s*->\s*"
    r"\(\s*(?P<dst>[A-Za-z_]\w*)\s*(?::\s*(?P<dst_label>\w+)\s*)?\)",
    re.IGNORECASE,
)
_RETURN_ITEM = re.compile(r"^([A-Za-z_]\w*)(?:\.([A-Za-z_]\w*))?$")


def parse(query: str) -> QLangPlan:
    """Parse an openCypher subset statement into a QLangPlan."""
    q = re.sub(r"\s+", " ", query.strip().rstrip(";"))
    mm = _MATCH.match(q)
    if not mm:
        raise QLangParseError(
            "Invalid openCypher MATCH. Supported: MATCH (a[:L])-[r[:R][*min..max]]->(b[:L])"
        )
    pos = mm.end()
    where_clause = ""
    wm = re.match(r"\s*WHERE\s+(.+?)(?=\s+RETURN\s+|$)", q[pos:], re.IGNORECASE)
    if wm:
        where_clause = wm.group(1).strip()
        pos += wm.end()
    rm = re.match(r"\s*RETURN\s+(.+?)\s*$", q[pos:], re.IGNORECASE)
    if not rm:
        raise QLangParseError("openCypher subset requires a RETURN clause")
    return_items = [item.strip() for item in rm.group(1).split(",")]
    parsed_return = []
    for item in return_items:
        im = _RETURN_ITEM.match(item)
        if not im:
            raise QLangParseError(f"Unsupported openCypher RETURN item: {item!r}")
        parsed_return.append({"var": im.group(1), "prop": im.group(2)})

    min_hops = int(mm.group("min")) if mm.group("min") else (0 if mm.group("max") else 1)
    max_hops = int(mm.group("max")) if mm.group("max") else min_hops
    if not mm.group("min") and not mm.group("max") and not mm.group("rel_label") and not mm.group("rel"):
        max_hops = 1
    if max_hops > 8:
        raise QLangParseError("openCypher variable hops are capped at 8 by query policy")

    conditions = []
    if where_clause:
        for cond in re.split(r"\s+AND\s+", where_clause, flags=re.IGNORECASE):
            cm = re.fullmatch(
                r"([A-Za-z_]\w*)\.([A-Za-z_]\w*)\s*(=|!=)\s*'([^']*)'", cond.strip()
            )
            if not cm:
                raise QLangParseError(f"Unsupported openCypher WHERE condition: {cond!r}")
            conditions.append(
                {"var": cm.group(1), "prop": cm.group(2), "op": cm.group(3), "value": cm.group(4)}
            )

    src_bound = bool(mm.group("src_label"))
    dst_bound = bool(mm.group("dst_label"))
    if not src_bound and not dst_bound and not mm.group("rel_label"):
        raise QLangParseError(
            "openCypher subset requires at least one label or relationship bound"
        )

    return QLangPlan(
        language="opencypher",
        intent="NEIGHBORHOOD",
        operation="openCypher-MATCH",
        source=q,
        edge_labels=[mm.group("rel_label")] if mm.group("rel_label") else [],
        min_hops=min_hops,
        max_hops=max(1, max_hops),
        extra={
            "src_var": mm.group("src"),
            "src_label": mm.group("src_label"),
            "rel_var": mm.group("rel"),
            "rel_label": mm.group("rel_label"),
            "dst_var": mm.group("dst"),
            "dst_label": mm.group("dst_label"),
            "where": conditions,
            "return": parsed_return,
        },
    )


def _props_ok(store_vertex: dict[str, Any], plan: QLangPlan, var: str) -> bool:
    for cond in plan.extra["where"]:
        if cond["var"] != var:
            continue
        actual = store_vertex["properties"].get(cond["prop"])
        ok = str(actual) == cond["value"] if cond["op"] == "=" else str(actual) != cond["value"]
        if not ok:
            return False
    return True


def execute(plan: QLangPlan, store: GraphStore, *, limit: int = 100) -> dict[str, Any]:
    """Execute a parsed openCypher MATCH against the GraphStore."""
    x = plan.extra
    src_label = x["src_label"] or x["dst_label"]
    seeds = store.find_vertices(label=src_label, limit=500)

    rows: list[dict[str, Any]] = []
    for seed in seeds:
        frontier: list[tuple[dict[str, Any], int]] = [(seed, 0)]
        seen = {seed["vid"]}
        while frontier:
            node, depth = frontier.pop()
            if plan.min_hops <= depth <= plan.max_hops and depth > 0 or (
                depth == 0 and plan.min_hops == 0
            ):
                if depth > 0 or plan.min_hops == 0:
                    if _props_ok(node, plan, x["dst_var"]) and _props_ok(seed, plan, x["src_var"]):
                        rows.append({x["src_var"]: seed, x["dst_var"]: node})
                        if len(rows) >= limit:
                            frontier = []
                            break
            if depth >= plan.max_hops:
                continue
            for edge in store.edges_from(node["vid"], labels=plan.edge_labels or None, limit=100):
                if x["rel_label"] and edge.get("label") != x["rel_label"]:
                    continue
                nxt = store.get_vertex(edge["in_v"])
                if nxt and nxt["vid"] not in seen:
                    seen.add(nxt["vid"])
                    frontier.append((nxt, depth + 1))

    projected = []
    for row in rows:
        out: dict[str, Any] = {}
        for item in x["return"]:
            vertex = row.get(item["var"])
            if vertex is None:
                continue
            if item["prop"]:
                out[f"{item['var']}.{item['prop']}"] = vertex["properties"].get(item["prop"])
            else:
                out[item["var"]] = {
                    "canonical_id": vertex["properties"].get("canonical_id", vertex["vid"]),
                    "label": vertex["label"],
                    "properties": vertex["properties"],
                }
        projected.append(out)
    return {
        "language": "opencypher",
        "rows": projected,
        "count": len(projected),
    }


def parse_and_execute(query: str, store: GraphStore) -> dict[str, Any]:
    return execute(parse(query), store)
