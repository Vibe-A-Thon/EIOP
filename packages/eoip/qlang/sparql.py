"""SPARQL SELECT front-end — triple patterns + FILTER subset.

Supported subset:
  PREFIX p: <urn:x>             (prefix declarations, optional)
  SELECT ?s ?o WHERE {
      ?s edgeLabel ?o .         (triple patterns; predicate may be a bare
      ?s <urn:cid> ?o .          label, prefixed name, or literal constant)
      FILTER(?o = "value")
      FILTER(?s != "value")
  } [LIMIT n]

Executed against the GraphStore: variables bind to vertex canonical ids,
predicates bind to edge labels, and constants bind to canonical ids or
literal property values. Serialization reuse: RDF/Turtle/SPARQL-INSERT
emitters live in ``eoip.graph.format_converter``; this module only covers
the query direction.
"""

from __future__ import annotations

import re
from typing import Any

from eoip.graph.store import GraphStore
from eoip.qlang.plans import QLangParseError, QLangPlan

_PREFIX = re.compile(r"^PREFIX\s+([A-Za-z][\w-]*)\s*:\s*<([^>]+)>\s*$", re.IGNORECASE)
_TRIPLE = re.compile(
    r"^(?P<s>\?\w+|<[^>]+>|[A-Za-z][\w:.-]*)\s+"
    r"(?P<p>\?\w+|[A-Za-z][\w:.-]*)\s+"
    r"(?P<o>\?\w+|<[^>]+>|\"[^\"]*\"|[A-Za-z0-9][\w:.-]*)\s*\.?$"
)
_FILTER = re.compile(
    r"^FILTER\s*\(\s*(\?\w+)\s*(=|!=)\s*(\"[^\"]*\"|<[^>]+>|[^\s)]+)\s*\)\s*\.?$",
    re.IGNORECASE,
)
_VAR = re.compile(r"^\?\w+$")


def _term(raw: str, prefixes: dict[str, str]) -> dict[str, Any]:
    raw = raw.strip()
    if _VAR.match(raw):
        return {"kind": "var", "value": raw[1:]}
    if raw.startswith('"'):
        return {"kind": "literal", "value": raw[1:-1]}
    if raw.startswith("<"):
        return {"kind": "iri", "value": raw[1:-1]}
    if ":" in raw:
        pfx, _, local = raw.partition(":")
        if pfx not in prefixes:
            raise QLangParseError(f"Unknown SPARQL prefix: {pfx!r}")
        return {"kind": "iri", "value": prefixes[pfx] + local}
    return {"kind": "const", "value": raw}


def parse(query: str) -> QLangPlan:
    """Parse a SPARQL SELECT subset query into a QLangPlan."""
    text = re.sub(r"#.*", "", query)  # comments
    # Extract the WHERE block first so prefixes/select parse cleanly.
    wm = re.search(r"WHERE\s*\{(?P<body>.*?)\}\s*(?:LIMIT\s+(\d+))?\s*$", text, re.DOTALL | re.IGNORECASE)
    if not wm:
        raise QLangParseError("SPARQL subset requires a WHERE { ... } block")
    head = text[: wm.start()].strip()
    body = wm.group("body").strip()
    limit = int(wm.group(2)) if wm.group(2) else 50

    prefixes: dict[str, str] = {}
    select_vars: list[str] = []
    for line in head.splitlines():
        line = line.strip()
        if not line:
            continue
        pm = _PREFIX.match(line)
        if pm:
            prefixes[pm.group(1)] = pm.group(2)
            continue
        sm = re.match(r"^SELECT\s+(DISTINCT\s+)?(.+)$", line, re.IGNORECASE)
        if sm:
            select_vars = [v.lstrip("?") for v in sm.group(2).split() if v.startswith("?")]
            continue
        raise QLangParseError(f"Unsupported SPARQL head clause: {line!r}")
    if not select_vars:
        raise QLangParseError("SPARQL subset requires a SELECT variable list")

    triples: list[list[dict[str, Any]]] = []
    filters: list[dict[str, Any]] = []
    for stmt in body.split("."):
        stmt = stmt.strip()
        if not stmt:
            continue
        fm = _FILTER.match(stmt)
        if fm:
            raw_val = fm.group(3)
            filters.append({
                "var": fm.group(1)[1:],
                "op": fm.group(2),
                "term": _term(raw_val, prefixes),
            })
            continue
        tm = _TRIPLE.match(stmt)
        if not tm:
            raise QLangParseError(f"Unsupported SPARQL pattern: {stmt!r}")
        triples.append([
            _term(tm.group("s"), prefixes),
            _term(tm.group("p"), prefixes),
            _term(tm.group("o"), prefixes),
        ])
    if not triples:
        raise QLangParseError("SPARQL subset requires at least one triple pattern")

    return QLangPlan(
        language="sparql",
        intent="SEARCH",
        operation="SPARQL-SELECT",
        source=query.strip(),
        limit=limit,
        extra={
            "prefixes": prefixes,
            "select": select_vars,
            "triples": triples,
            "filters": filters,
        },
    )


def execute(plan: QLangPlan, store: GraphStore) -> dict[str, Any]:
    """Execute a parsed SPARQL SELECT against the GraphStore."""
    x = plan.extra
    solutions: list[dict[str, str]] = [{}]

    for triple in x["triples"]:
        s_term, p_term, o_term = triple
        if p_term["kind"] not in ("var", "const"):
            raise QLangParseError(
                "SPARQL subset predicates must be edge labels, IRIs, or prefixed names"
            )
        edge_label = p_term["value"]
        next_solutions: list[dict[str, str]] = []
        for env in solutions:
            if s_term["kind"] == "iri":
                vertices = store.find_vertices(limit=500)
                seeds = [v for v in vertices if v["properties"].get("canonical_id") == s_term["value"]]
            else:
                seeds = store.find_vertices(label=None, limit=500)
            for vertex in seeds:
                env2 = dict(env)
                if s_term["kind"] == "var":
                    if s_term["value"] in env2 and env2[s_term["value"]] != vertex["properties"].get("canonical_id"):
                        continue
                    env2[s_term["value"]] = str(vertex["properties"].get("canonical_id"))
                elif vertex["properties"].get("canonical_id") != s_term["value"]:
                    continue
                matched = False
                for edge in store.edges_from(vertex["vid"], labels=[edge_label], limit=200):
                    target = store.get_vertex(edge["in_v"])
                    if target is None:
                        continue
                    env3 = dict(env2)
                    if o_term["kind"] == "var":
                        cid = str(target["properties"].get("canonical_id"))
                        if o_term["value"] in env3 and env3[o_term["value"]] != cid:
                            continue
                        env3[o_term["value"]] = cid
                        next_solutions.append(env3)
                        matched = True
                    elif o_term["kind"] == "literal":
                        if str(target["properties"].get("name")) == o_term["value"]:
                            next_solutions.append(env3)
                            matched = True
                    else:
                        if target["properties"].get("canonical_id") == o_term["value"]:
                            next_solutions.append(env3)
                            matched = True
                if not matched and o_term["kind"] == "literal":
                    if str(vertex["properties"].get("name")) == o_term["value"]:
                        next_solutions.append(env2)
        solutions = next_solutions

    filtered = []
    for env in solutions:
        ok = True
        for cond in x["filters"]:
            val = env.get(cond["var"])
            if cond["op"] == "=":
                ok = val == cond["term"]["value"]
            else:
                ok = val != cond["term"]["value"]
            if not ok:
                break
        if ok:
            filtered.append(env)
        if len(filtered) >= plan.limit:
            break

    rows = [{var: env.get(var) for var in x["select"]} for env in filtered]
    return {"language": "sparql", "head": x["select"], "rows": rows, "count": len(rows)}


def parse_and_execute(query: str, store: GraphStore) -> dict[str, Any]:
    return execute(parse(query), store)
