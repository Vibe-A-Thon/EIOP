"""EOIP Query Language (EQL) — structured graph query DSL.

Supports typed queries against the knowledge graph with operators:
  FIND <label> [WHERE <prop> <op> <value>] [LIMIT <n>]
  PATH <source_cid> TO <target_cid> [MAX_DEPTH <n>]
  NEIGHBORS <cid> [DEPTH <n>] [LABEL <edge_label>]
  IMPACT <cid> [DEPTH <n>]
  WHY <cid>
  WHY NOT <source_cid> <target_cid>
  WHAT CHANGED <cid>
  CONTEXT <cid>
  EDGES FROM <cid> | TO <cid> [LABEL <edge_label>]
  COUNT <label>
  DOMAINS
"""

from __future__ import annotations

import re
from collections import deque
from typing import Any

from eoip.graph.store import GraphStore
from eoip.ontology.manifest import DOMAINS, EDGE_LABELS, VERTEX_LABELS


def parse_and_execute(store: GraphStore, query: str) -> dict[str, Any]:
    """Parse an EQL query string and execute it against the graph store."""
    q = query.strip()
    if not q:
        return {"error": "Empty query", "help": _HELP}

    upper = q.upper()

    if upper.startswith("FIND "):
        return _exec_find(store, q)
    if upper.startswith("PATH "):
        return _exec_path(store, q)
    if upper.startswith(("NEIGHBORS ", "NEIGHBOURHOOD ")):
        return _exec_neighbors(store, q)
    if upper.startswith("IMPACT "):
        return _exec_impact(store, q)
    if upper.startswith("WHY NOT "):
        return _exec_why_not(store, q)
    if upper.startswith("WHY "):
        return _exec_why(store, q)
    if upper.startswith("WHAT CHANGED "):
        return _exec_what_changed(store, q)
    if upper.startswith("CONTEXT "):
        return _exec_context(store, q)
    if upper.startswith("EDGES "):
        return _exec_edges(store, q)
    if upper.startswith("COUNT "):
        return _exec_count(store, q)
    if upper == "DOMAINS":
        return {"domains": DOMAINS, "total": len(DOMAINS)}
    if upper == "LABELS" or upper == "VERTEX LABELS":
        return {"labels": sorted(VERTEX_LABELS.keys()), "total": len(VERTEX_LABELS)}
    if upper == "EDGE LABELS":
        return {"labels": sorted(EDGE_LABELS.keys()), "total": len(EDGE_LABELS)}
    if upper == "HELP":
        return {"help": _HELP}

    return {"error": f"Unrecognised query: {q}", "help": _HELP}


def _exec_find(store: GraphStore, q: str) -> dict[str, Any]:
    m = re.match(
        r"FIND\s+(\w+|\*)(?:\s+WHERE\s+(.+?))?(?:\s+LIMIT\s+(\d+))?\s*$",
        q, re.IGNORECASE,
    )
    if not m:
        return {"error": "Syntax: FIND <label> [WHERE <prop> <op> <value>] [LIMIT <n>]"}

    label = m.group(1)
    where_clause = m.group(2)
    limit = int(m.group(3)) if m.group(3) else 100

    if label not in VERTEX_LABELS and label != "*":
        return {"error": f"Unknown label: {label}", "available": sorted(VERTEX_LABELS.keys())}

    find_label = None if label == "*" else label
    vertices = store.find_vertices(label=find_label, limit=limit)

    if where_clause:
        vertices = _apply_where(vertices, where_clause)

    results = []
    for v in vertices[:limit]:
        results.append({
            "canonical_id": v["canonical_id"],
            "label": v["label"],
            "name": v["properties"].get("name", ""),
            "properties": {k: v2 for k, v2 in v["properties"].items()
                          if k not in ("canonical_id",) and v2 is not None},
        })
    return {"query": "FIND", "label": label, "results": results, "total": len(results)}


def _apply_where(vertices: list[dict], clause: str) -> list[dict]:
    parts = re.match(r"(\w+)\s*(=|!=|>|<|>=|<=|CONTAINS|LIKE)\s*(.+)", clause, re.IGNORECASE)
    if not parts:
        return vertices
    prop, op, value = parts.group(1), parts.group(2).upper(), parts.group(3).strip().strip("'\"")
    filtered = []
    for v in vertices:
        actual = v["properties"].get(prop)
        if actual is None:
            continue
        actual_str = str(actual)
        if op == "=" and actual_str == value or op == "!=" and actual_str != value or op == "CONTAINS" and value.lower() in actual_str.lower() or op == "LIKE" and re.search(value.replace("%", ".*"), actual_str, re.IGNORECASE):
            filtered.append(v)
        elif op in (">", "<", ">=", "<="):
            try:
                a, b = float(actual), float(value)
                if (op == ">" and a > b) or (op == "<" and a < b) or (op == ">=" and a >= b) or (op == "<=" and a <= b):
                    filtered.append(v)
            except (ValueError, TypeError):
                pass
    return filtered


def _exec_path(store: GraphStore, q: str) -> dict[str, Any]:
    m = re.match(r"PATH\s+(\S+)\s+TO\s+(\S+)(?:\s+MAX_DEPTH\s+(\d+))?\s*$", q, re.IGNORECASE)
    if not m:
        return {"error": "Syntax: PATH <source_cid> TO <target_cid> [MAX_DEPTH <n>]"}
    src_cid, tgt_cid = m.group(1), m.group(2)
    max_depth = int(m.group(3)) if m.group(3) else 6

    src = store.get_vertex_by_canonical_id(src_cid)
    tgt = store.get_vertex_by_canonical_id(tgt_cid)
    if not src:
        return {"error": f"Source not found: {src_cid}"}
    if not tgt:
        return {"error": f"Target not found: {tgt_cid}"}

    path = _bfs_path(store, src["vid"], tgt["vid"], max_depth)
    if path is None:
        return {"query": "PATH", "source": src_cid, "target": tgt_cid, "found": False, "path": []}

    result_path = []
    for vid in path:
        v = store.get_vertex(vid)
        if v:
            result_path.append({"canonical_id": v["canonical_id"], "label": v["label"], "name": v["properties"].get("name", "")})
    return {"query": "PATH", "source": src_cid, "target": tgt_cid, "found": True, "path": result_path, "length": len(result_path)}


def _bfs_path(store: GraphStore, src_vid: str, tgt_vid: str, max_depth: int) -> list[str] | None:
    if src_vid == tgt_vid:
        return [src_vid]
    visited: dict[str, str | None] = {src_vid: None}
    queue: deque[tuple[str, int]] = deque([(src_vid, 0)])
    while queue:
        vid, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for e in store.edges_from(vid, limit=100):
            nxt = e["in_v"]
            if nxt not in visited:
                visited[nxt] = vid
                if nxt == tgt_vid:
                    return _reconstruct(visited, src_vid, tgt_vid)
                queue.append((nxt, depth + 1))
        for e in store.edges_to(vid, limit=100):
            nxt = e["out_v"]
            if nxt not in visited:
                visited[nxt] = vid
                if nxt == tgt_vid:
                    return _reconstruct(visited, src_vid, tgt_vid)
                queue.append((nxt, depth + 1))
    return None


def _reconstruct(visited: dict[str, str | None], src: str, tgt: str) -> list[str]:
    path = [tgt]
    current = tgt
    while current != src:
        prev = visited[current]
        if prev is None:
            break
        path.append(prev)
        current = prev
    path.reverse()
    return path


def _exec_neighbors(store: GraphStore, q: str) -> dict[str, Any]:
    m = re.match(r"(?:NEIGHBORS|NEIGHBOURHOOD)\s+(\S+)(?:\s+DEPTH\s+(\d+))?(?:\s+LABEL\s+(\w+))?\s*$", q, re.IGNORECASE)
    if not m:
        return {"error": "Syntax: NEIGHBORS <cid> [DEPTH <n>] [LABEL <edge_label>]"}
    cid = m.group(1)
    int(m.group(2)) if m.group(2) else 1
    edge_label = m.group(3)

    v = store.get_vertex_by_canonical_id(cid)
    if not v:
        return {"error": f"Entity not found: {cid}"}

    neighbors: list[dict] = []
    labels_filter = [edge_label] if edge_label else None
    for e in store.edges_from(v["vid"], labels=labels_filter, limit=200):
        tgt = store.get_vertex(e["in_v"])
        if tgt:
            neighbors.append({"canonical_id": tgt["canonical_id"], "label": tgt["label"], "via": e["label"], "direction": "out"})
    for e in store.edges_to(v["vid"], labels=labels_filter, limit=200):
        src = store.get_vertex(e["out_v"])
        if src:
            neighbors.append({"canonical_id": src["canonical_id"], "label": src["label"], "via": e["label"], "direction": "in"})
    return {"query": "NEIGHBORS", "entity": cid, "neighbors": neighbors, "total": len(neighbors)}


def _exec_impact(store: GraphStore, q: str) -> dict[str, Any]:
    m = re.match(r"IMPACT\s+(\S+)(?:\s+DEPTH\s+(\d+))?\s*$", q, re.IGNORECASE)
    if not m:
        return {"error": "Syntax: IMPACT <cid> [DEPTH <n>]"}
    cid = m.group(1)
    depth = int(m.group(2)) if m.group(2) else 3

    v = store.get_vertex_by_canonical_id(cid)
    if not v:
        return {"error": f"Entity not found: {cid}"}

    affected: list[dict] = []
    visited: set[str] = {v["vid"]}
    queue: deque[tuple[str, int]] = deque([(v["vid"], 0)])
    while queue:
        vid, d = queue.popleft()
        if d >= depth:
            continue
        for e in store.edges_to(vid, limit=200):
            src = store.get_vertex(e["out_v"])
            if src and src["vid"] not in visited:
                visited.add(src["vid"])
                affected.append({"canonical_id": src["canonical_id"], "label": src["label"], "depth": d + 1, "via": e["label"]})
                queue.append((src["vid"], d + 1))
    return {"query": "IMPACT", "entity": cid, "affected": affected, "total": len(affected)}


def _exec_why(store: GraphStore, q: str) -> dict[str, Any]:
    m = re.match(r"WHY\s+(\S+)\s*$", q, re.IGNORECASE)
    if not m:
        return {"error": "Syntax: WHY <cid>"}
    from eoip.graph.query_operators import query_why
    return query_why(store, m.group(1))


def _exec_why_not(store: GraphStore, q: str) -> dict[str, Any]:
    m = re.match(r"WHY\s+NOT\s+(\S+)\s+(\S+)\s*$", q, re.IGNORECASE)
    if not m:
        return {"error": "Syntax: WHY NOT <source_cid> <target_cid>"}
    from eoip.graph.query_operators import query_why_not
    return query_why_not(store, m.group(1), m.group(2))


def _exec_what_changed(store: GraphStore, q: str) -> dict[str, Any]:
    m = re.match(r"WHAT\s+CHANGED\s+(\S+)\s*$", q, re.IGNORECASE)
    if not m:
        return {"error": "Syntax: WHAT CHANGED <cid>"}
    from eoip.graph.query_operators import query_what_changed
    return query_what_changed(store, m.group(1))


def _exec_context(store: GraphStore, q: str) -> dict[str, Any]:
    m = re.match(r"CONTEXT\s+(\S+)\s*$", q, re.IGNORECASE)
    if not m:
        return {"error": "Syntax: CONTEXT <cid>"}
    from eoip.graph.query_operators import query_context
    return query_context(store, m.group(1))


def _exec_edges(store: GraphStore, q: str) -> dict[str, Any]:
    m = re.match(r"EDGES\s+(FROM|TO)\s+(\S+)(?:\s+LABEL\s+(\w+))?\s*$", q, re.IGNORECASE)
    if not m:
        return {"error": "Syntax: EDGES FROM|TO <cid> [LABEL <edge_label>]"}
    direction, cid = m.group(1).upper(), m.group(2)
    label = m.group(3)

    v = store.get_vertex_by_canonical_id(cid)
    if not v:
        return {"error": f"Entity not found: {cid}"}

    labels_filter = [label] if label else None
    edges: list[dict] = []
    if direction == "FROM":
        for e in store.edges_from(v["vid"], labels=labels_filter, limit=500):
            tgt = store.get_vertex(e["in_v"])
            edges.append({"eid": e["eid"], "label": e["label"], "target": tgt["canonical_id"] if tgt else e["in_v"]})
    else:
        for e in store.edges_to(v["vid"], labels=labels_filter, limit=500):
            src = store.get_vertex(e["out_v"])
            edges.append({"eid": e["eid"], "label": e["label"], "source": src["canonical_id"] if src else e["out_v"]})
    return {"query": "EDGES", "direction": direction, "entity": cid, "edges": edges, "total": len(edges)}


def _exec_count(store: GraphStore, q: str) -> dict[str, Any]:
    m = re.match(r"COUNT\s+(\w+)\s*$", q, re.IGNORECASE)
    if not m:
        return {"error": "Syntax: COUNT <label|VERTICES|EDGES>"}
    label = m.group(1)
    if label.upper() == "VERTICES":
        return {"query": "COUNT", "target": "VERTICES", "count": store.count_vertices()}
    if label.upper() == "EDGES":
        return {"query": "COUNT", "target": "EDGES", "count": store.count_edges()}
    if label in VERTEX_LABELS:
        return {"query": "COUNT", "target": label, "count": store.count_vertices(label=label)}
    if label in EDGE_LABELS:
        return {"query": "COUNT", "target": label, "count": store.count_edges(label=label)}
    return {"error": f"Unknown label: {label}"}


_HELP = """EOIP Query Language (EQL) Reference:

FIND <label> [WHERE <prop> <op> <value>] [LIMIT <n>]
  Find vertices by label with optional property filter.
  Operators: =, !=, >, <, >=, <=, CONTAINS, LIKE

PATH <source_cid> TO <target_cid> [MAX_DEPTH <n>]
  Find shortest path between two entities.

NEIGHBORS <cid> [DEPTH <n>] [LABEL <edge_label>]
  List neighboring entities.

IMPACT <cid> [DEPTH <n>]
  Reverse dependency impact analysis.

WHY <cid>
  Explain why an entity exists (provenance, decisions, evidence).

WHY NOT <source_cid> <target_cid>
  Explain why two entities are not connected.

WHAT CHANGED <cid>
  Show change history for an entity.

CONTEXT <cid>
  Show when/who/where/how context for an entity.

EDGES FROM|TO <cid> [LABEL <edge_label>]
  List edges from or to an entity.

COUNT <label|VERTICES|EDGES>
  Count entities or edges.

DOMAINS
  List all graph domains.

LABELS / VERTEX LABELS
  List all vertex labels.

EDGE LABELS
  List all edge labels.
"""
