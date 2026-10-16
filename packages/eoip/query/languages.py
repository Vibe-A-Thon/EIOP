"""Extended query language support: EOQL, OSQL, Semantic Query Language.

Each language parser produces a QueryPlan — never executable Gremlin.
Augments the existing EQL and NLQ parsers.
"""

from __future__ import annotations

import re
from typing import Any

from eoip.contracts.query_plan import QueryPlan
from eoip.graph.store import GraphStore
from eoip.ontology.manifest import DOMAINS, EDGE_LABELS, VERTEX_LABELS
from eoip.query.eql import parse_and_execute as eql_execute


def parse_eoql(store: GraphStore, query: str) -> dict[str, Any]:
    """Enterprise Object Query Language (EOQL).

    SQL-like syntax for enterprise objects:
      SELECT <fields> FROM <entity_type> [WHERE <condition>] [JOIN <relationship>] [LIMIT n]
      TRAVERSE FROM <cid> [VIA <edge_labels>] [DEPTH n]
      AGGREGATE <entity_type> BY <field>
    """
    q = query.strip()
    if not q:
        return {"error": "Empty query"}

    upper = q.upper()

    if upper.startswith("SELECT "):
        return _eoql_select(store, q)
    if upper.startswith("TRAVERSE "):
        return _eoql_traverse(store, q)
    if upper.startswith("AGGREGATE "):
        return _eoql_aggregate(store, q)

    return {"error": f"Unknown EOQL statement. Supported: SELECT, TRAVERSE, AGGREGATE", "query": q}


def _eoql_select(store: GraphStore, query: str) -> dict[str, Any]:
    m = re.match(
        r"SELECT\s+(.+?)\s+FROM\s+(\w+)"
        r"(?:\s+WHERE\s+(.+?))?"
        r"(?:\s+JOIN\s+(\w+))?"
        r"(?:\s+LIMIT\s+(\d+))?\s*$",
        query, re.IGNORECASE,
    )
    if not m:
        return {"error": "Invalid EOQL SELECT syntax", "help": "SELECT <fields> FROM <type> [WHERE <cond>] [JOIN <rel>] [LIMIT n]"}

    fields_str, entity_type, where_clause, join_rel, limit_str = m.groups()
    fields = [f.strip() for f in fields_str.split(",")]
    limit = int(limit_str) if limit_str else 50

    vertices = store.find_vertices(label=entity_type, limit=limit * 5)
    if where_clause:
        vertices = _apply_where(vertices, where_clause)

    results = []
    for v in vertices[:limit]:
        row: dict[str, Any] = {"canonical_id": v["properties"].get("canonical_id", v["vid"])}
        if "*" in fields:
            row.update(v["properties"])
        else:
            for f in fields:
                row[f] = v["properties"].get(f)

        if join_rel:
            related = []
            for edge in store.edges_from(v["vid"]):
                if edge.get("label") == join_rel:
                    tgt = store.get_vertex(edge["in_v"])
                    if tgt:
                        related.append(tgt["properties"].get("canonical_id", edge["in_v"]))
            row[f"joined_{join_rel}"] = related

        results.append(row)

    return {"language": "EOQL", "operation": "SELECT", "entity_type": entity_type, "count": len(results), "results": results}


def _eoql_traverse(store: GraphStore, query: str) -> dict[str, Any]:
    m = re.match(
        r"TRAVERSE\s+FROM\s+(\S+)"
        r"(?:\s+VIA\s+(\S+))?"
        r"(?:\s+DEPTH\s+(\d+))?\s*$",
        query, re.IGNORECASE,
    )
    if not m:
        return {"error": "Invalid EOQL TRAVERSE syntax", "help": "TRAVERSE FROM <cid> [VIA <edge_labels>] [DEPTH n]"}

    cid, via, depth_str = m.groups()
    depth = int(depth_str) if depth_str else 3
    allowed_labels = via.split(",") if via else None

    eql_q = f"NEIGHBORS {cid} DEPTH {depth}"
    if allowed_labels:
        eql_q += f" LABEL {allowed_labels[0]}"
    return {**eql_execute(store, eql_q), "language": "EOQL", "operation": "TRAVERSE"}


def _eoql_aggregate(store: GraphStore, query: str) -> dict[str, Any]:
    m = re.match(r"AGGREGATE\s+(\w+)\s+BY\s+(\w+)\s*$", query, re.IGNORECASE)
    if not m:
        return {"error": "Invalid EOQL AGGREGATE syntax", "help": "AGGREGATE <entity_type> BY <field>"}

    entity_type, field = m.groups()
    vertices = store.find_vertices(label=entity_type, limit=50_000)
    buckets: dict[str, int] = {}
    for v in vertices:
        val = str(v["properties"].get(field, "unknown"))
        buckets[val] = buckets.get(val, 0) + 1

    return {"language": "EOQL", "operation": "AGGREGATE", "entity_type": entity_type,
            "group_by": field, "buckets": dict(sorted(buckets.items(), key=lambda x: -x[1]))}


def parse_osql(store: GraphStore, query: str) -> dict[str, Any]:
    """Ontology SQL (OSQL) — SQL-like queries over the ontology schema.

      DESCRIBE <entity_type>
      LIST TYPES | LIST DOMAINS | LIST RELATIONSHIPS
      SCHEMA FOR <entity_type>
      INSTANCES OF <entity_type> [LIMIT n]
    """
    q = query.strip()
    upper = q.upper()

    if upper.startswith("DESCRIBE "):
        label = q[9:].strip()
        return _osql_describe(store, label)
    if upper.startswith("LIST TYPES"):
        return {"language": "OSQL", "operation": "LIST_TYPES",
                "types": sorted(VERTEX_LABELS.keys()),
                "count": len(VERTEX_LABELS)}
    if upper.startswith("LIST DOMAINS"):
        return {"language": "OSQL", "operation": "LIST_DOMAINS",
                "domains": DOMAINS, "count": len(DOMAINS)}
    if upper.startswith("LIST RELATIONSHIPS") or upper.startswith("LIST EDGES"):
        return {"language": "OSQL", "operation": "LIST_RELATIONSHIPS",
                "relationships": sorted(EDGE_LABELS.keys()),
                "count": len(EDGE_LABELS)}
    if upper.startswith("SCHEMA FOR "):
        label = q[11:].strip()
        return _osql_describe(store, label)
    if upper.startswith("INSTANCES OF "):
        m = re.match(r"INSTANCES\s+OF\s+(\w+)(?:\s+LIMIT\s+(\d+))?\s*$", q, re.IGNORECASE)
        if m:
            label, limit_str = m.groups()
            limit = int(limit_str) if limit_str else 50
            return _osql_instances(store, label, limit)

    return {"error": "Unknown OSQL command",
            "help": "DESCRIBE <type> | LIST TYPES | LIST DOMAINS | LIST RELATIONSHIPS | INSTANCES OF <type>"}


def _osql_describe(store: GraphStore, label: str) -> dict[str, Any]:
    spec = VERTEX_LABELS.get(label)
    if not spec:
        return {"error": f"Unknown entity type: {label}", "available": sorted(VERTEX_LABELS.keys())}

    domain = spec[0] if isinstance(spec, tuple) else spec.get("domain", "unknown")
    properties = list(spec[1]) + list(spec[2]) if isinstance(spec, tuple) else spec.get("properties", [])

    outgoing = []
    incoming = []
    for edge_name, edge_spec in EDGE_LABELS.items():
        if isinstance(edge_spec, tuple):
            sources, targets = edge_spec[0], edge_spec[1]
        else:
            sources = edge_spec.get("source_labels", [])
            targets = edge_spec.get("target_labels", [])
        if label in sources:
            outgoing.append({"relationship": edge_name, "targets": targets})
        if label in targets:
            incoming.append({"relationship": edge_name, "sources": sources})

    return {
        "language": "OSQL",
        "operation": "DESCRIBE",
        "type": label,
        "domain": domain,
        "properties": properties,
        "outgoing_relationships": outgoing,
        "incoming_relationships": incoming,
        "instance_count": store.count_vertices(label=label),
    }


def _osql_instances(store: GraphStore, label: str, limit: int) -> dict[str, Any]:
    vertices = store.find_vertices(label=label, limit=limit)
    return {
        "language": "OSQL",
        "operation": "INSTANCES",
        "type": label,
        "count": len(vertices),
        "instances": [
            {"canonical_id": v["properties"].get("canonical_id", v["vid"]),
             "name": v["properties"].get("name", v["properties"].get("display_name", ""))}
            for v in vertices
        ],
    }


def parse_semantic_query(store: GraphStore, query: str) -> dict[str, Any]:
    """Semantic Query Language — intent-aware queries with ontology context.

      MEANING OF <term>
      RELATED TO <cid> [BY <relationship_type>]
      EXPLAIN <cid>
      COMPARE <cid_a> AND <cid_b>
      CLASSIFY <cid>
    """
    q = query.strip()
    upper = q.upper()

    if upper.startswith("MEANING OF "):
        term = q[11:].strip()
        return _semantic_meaning(store, term)
    if upper.startswith("RELATED TO "):
        m = re.match(r"RELATED\s+TO\s+(\S+)(?:\s+BY\s+(\w+))?\s*$", q, re.IGNORECASE)
        if m:
            cid, rel_type = m.groups()
            return _semantic_related(store, cid, rel_type)
    if upper.startswith("EXPLAIN "):
        cid = q[8:].strip()
        return _semantic_explain(store, cid)
    if upper.startswith("COMPARE "):
        m = re.match(r"COMPARE\s+(\S+)\s+AND\s+(\S+)\s*$", q, re.IGNORECASE)
        if m:
            return _semantic_compare(store, m.group(1), m.group(2))
    if upper.startswith("CLASSIFY "):
        cid = q[9:].strip()
        return _semantic_classify(store, cid)

    return {"error": "Unknown Semantic Query",
            "help": "MEANING OF <term> | RELATED TO <cid> | EXPLAIN <cid> | COMPARE <a> AND <b> | CLASSIFY <cid>"}


def _semantic_meaning(store: GraphStore, term: str) -> dict[str, Any]:
    term_lower = term.lower()
    matches = []
    if term in VERTEX_LABELS:
        spec = VERTEX_LABELS[term]
        domain = spec[0] if isinstance(spec, tuple) else spec.get("domain")
        matches.append({"kind": "entity_type", "name": term, "domain": domain})
    if term in EDGE_LABELS:
        matches.append({"kind": "relationship_type", "name": term})
    if term.upper() in DOMAINS:
        matches.append({"kind": "domain", "name": term.upper()})

    vertices = store.find_vertices(limit=100)
    for v in vertices:
        name = v["properties"].get("name", "").lower()
        if term_lower in name:
            matches.append({
                "kind": "entity",
                "canonical_id": v["properties"].get("canonical_id"),
                "name": v["properties"].get("name"),
                "label": v["label"],
            })
            if len(matches) >= 20:
                break

    return {"language": "SemanticQL", "operation": "MEANING", "term": term,
            "matches": matches, "count": len(matches)}


def _semantic_related(store: GraphStore, cid: str, rel_type: str | None) -> dict[str, Any]:
    v = store.get_vertex_by_canonical_id(cid)
    if not v:
        return {"error": f"Entity not found: {cid}"}

    related = []
    for edge in store.edges_from(v["vid"]):
        if rel_type and edge.get("label") != rel_type:
            continue
        tgt = store.get_vertex(edge["in_v"])
        if tgt:
            related.append({
                "canonical_id": tgt["properties"].get("canonical_id"),
                "name": tgt["properties"].get("name", ""),
                "label": tgt["label"],
                "via": edge.get("label"),
                "direction": "outgoing",
            })
    for edge in store.edges_to(v["vid"]):
        if rel_type and edge.get("label") != rel_type:
            continue
        src = store.get_vertex(edge["out_v"])
        if src:
            related.append({
                "canonical_id": src["properties"].get("canonical_id"),
                "name": src["properties"].get("name", ""),
                "label": src["label"],
                "via": edge.get("label"),
                "direction": "incoming",
            })

    return {"language": "SemanticQL", "operation": "RELATED", "source": cid,
            "filter": rel_type, "related": related, "count": len(related)}


def _semantic_explain(store: GraphStore, cid: str) -> dict[str, Any]:
    v = store.get_vertex_by_canonical_id(cid)
    if not v:
        return {"error": f"Entity not found: {cid}"}

    out_edges = store.edges_from(v["vid"])
    in_edges = store.edges_to(v["vid"])
    out_types: dict[str, int] = {}
    in_types: dict[str, int] = {}
    for e in out_edges:
        lbl = e.get("label", "unknown")
        out_types[lbl] = out_types.get(lbl, 0) + 1
    for e in in_edges:
        lbl = e.get("label", "unknown")
        in_types[lbl] = in_types.get(lbl, 0) + 1

    label_spec = VERTEX_LABELS.get(v["label"])
    domain = label_spec[0] if isinstance(label_spec, tuple) else (label_spec.get("domain", "unknown") if label_spec else "unknown")
    return {
        "language": "SemanticQL", "operation": "EXPLAIN",
        "canonical_id": cid,
        "label": v["label"],
        "domain": domain,
        "properties": v["properties"],
        "outgoing_relationship_counts": out_types,
        "incoming_relationship_counts": in_types,
        "total_connections": len(out_edges) + len(in_edges),
    }


def _semantic_compare(store: GraphStore, cid_a: str, cid_b: str) -> dict[str, Any]:
    va = store.get_vertex_by_canonical_id(cid_a)
    vb = store.get_vertex_by_canonical_id(cid_b)
    if not va or not vb:
        return {"error": "One or both entities not found"}

    props_a = set(va.get("properties", {}).keys())
    props_b = set(vb.get("properties", {}).keys())
    shared_props = props_a & props_b

    def _neighbors(v: dict) -> set[str]:
        nbrs: set[str] = set()
        for e in store.edges_from(v["vid"]):
            t = store.get_vertex(e["in_v"])
            if t:
                nbrs.add(t["properties"].get("canonical_id", ""))
        for e in store.edges_to(v["vid"]):
            s = store.get_vertex(e["out_v"])
            if s:
                nbrs.add(s["properties"].get("canonical_id", ""))
        return nbrs

    nbrs_a = _neighbors(va)
    nbrs_b = _neighbors(vb)
    shared_nbrs = nbrs_a & nbrs_b

    return {
        "language": "SemanticQL", "operation": "COMPARE",
        "entity_a": {"canonical_id": cid_a, "label": va["label"]},
        "entity_b": {"canonical_id": cid_b, "label": vb["label"]},
        "same_type": va["label"] == vb["label"],
        "shared_properties": sorted(shared_props),
        "shared_neighbors": sorted(shared_nbrs),
        "shared_neighbor_count": len(shared_nbrs),
        "neighborhood_overlap": len(shared_nbrs) / max(len(nbrs_a | nbrs_b), 1),
    }


def _semantic_classify(store: GraphStore, cid: str) -> dict[str, Any]:
    v = store.get_vertex_by_canonical_id(cid)
    if not v:
        return {"error": f"Entity not found: {cid}"}

    label = v["label"]
    label_spec = VERTEX_LABELS.get(label)
    domain = label_spec[0] if isinstance(label_spec, tuple) else (label_spec.get("domain", "unknown") if label_spec else "unknown")

    out_edges = store.edges_from(v["vid"])
    in_edges = store.edges_to(v["vid"])
    edge_types = set()
    for e in out_edges:
        edge_types.add(e.get("label", ""))
    for e in in_edges:
        edge_types.add(e.get("label", ""))

    return {
        "language": "SemanticQL", "operation": "CLASSIFY",
        "canonical_id": cid,
        "entity_type": label,
        "domain": domain,
        "connection_types": sorted(edge_types),
        "degree": len(out_edges) + len(in_edges),
    }


def _apply_where(vertices: list[dict], clause: str) -> list[dict]:
    m = re.match(r"(\w+)\s*(=|!=|LIKE|>|<|>=|<=)\s*['\"]?(.+?)['\"]?\s*$", clause, re.IGNORECASE)
    if not m:
        return vertices
    field, op, value = m.groups()
    result = []
    for v in vertices:
        actual = v["properties"].get(field)
        if actual is None:
            continue
        actual_str = str(actual)
        if op == "=":
            if actual_str == value:
                result.append(v)
        elif op == "!=":
            if actual_str != value:
                result.append(v)
        elif op.upper() == "LIKE":
            pattern = value.replace("%", ".*").replace("_", ".")
            if re.match(pattern, actual_str, re.IGNORECASE):
                result.append(v)
        elif op in (">", "<", ">=", "<="):
            try:
                a, b = float(actual_str), float(value)
                if (op == ">" and a > b) or (op == "<" and a < b) or \
                   (op == ">=" and a >= b) or (op == "<=" and a <= b):
                    result.append(v)
            except ValueError:
                pass
    return result
