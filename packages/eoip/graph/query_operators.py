"""Native graph query operators (G2-T0750..0753, G2-QOP-001..009).

Structured WHY, WHY NOT, WHAT CHANGED, WHEN/WHO/WHERE/HOW operators
that compose graph traversals into interpretable answers.
"""

from __future__ import annotations

from eoip.graph.store import GraphStore
from eoip.ontology.manifest import VERTEX_LABELS


def query_why(store: GraphStore, entity_cid: str) -> dict:
    """Structured WHY: explains why an entity exists via provenance and decision chains.

    Traces: entity <- EVIDENCED_BY -> Evidence, entity <- DECIDES <- Decision,
    entity <- IMPLEMENTS <- Commit, entity <- TRACES_TO <- BusinessObjective
    """
    entity = store.get_vertex_by_canonical_id(entity_cid)
    if not entity:
        return {"entity": entity_cid, "reasons": [], "error": "Entity not found"}

    reasons: list[dict] = []

    in_edges = store.find_edges(in_v=entity["vid"], limit=500)
    out_edges = store.find_edges(out_v=entity["vid"], limit=500)

    for edge in out_edges:
        if edge["label"] == "EVIDENCED_BY":
            ev = store.get_vertex(edge["in_v"])
            if ev:
                reasons.append({
                    "type": "evidence",
                    "source": ev["canonical_id"],
                    "method": ev["properties"].get("method", ""),
                    "description": f"Evidenced by {ev['properties'].get('source_system', '')} via {ev['properties'].get('method', '')}",
                })

    for edge in in_edges:
        src = store.get_vertex(edge["out_v"])
        if not src:
            continue
        if edge["label"] == "DECIDES" and src["label"] == "Decision":
            reasons.append({
                "type": "decision",
                "source": src["canonical_id"],
                "name": src["properties"].get("name", ""),
                "description": f"Architecture decision: {src['properties'].get('name', '')}",
                "rationale": src["properties"].get("rationale", ""),
            })
        elif edge["label"] == "IMPLEMENTS":
            reasons.append({
                "type": "implementation",
                "source": src["canonical_id"],
                "name": src["properties"].get("name", "") or src["properties"].get("commit_sha", ""),
                "description": f"Implemented by {src['label']} {src['canonical_id']}",
            })
        elif edge["label"] == "TRACES_TO":
            reasons.append({
                "type": "business_intent",
                "source": src["canonical_id"],
                "name": src["properties"].get("name", ""),
                "description": f"Traces to {src['label']}: {src['properties'].get('name', '')}",
            })

    return {
        "entity": entity_cid,
        "label": entity["label"],
        "name": entity["properties"].get("name", ""),
        "reasons": reasons,
        "total_reasons": len(reasons),
    }


def query_why_not(store: GraphStore, source_cid: str, target_cid: str) -> dict:
    """Structured WHY NOT: explains why two entities are not connected.

    Checks for missing edges, domain mismatches, validation blocks.
    """
    source = store.get_vertex_by_canonical_id(source_cid)
    target = store.get_vertex_by_canonical_id(target_cid)

    if not source or not target:
        missing = []
        if not source:
            missing.append(source_cid)
        if not target:
            missing.append(target_cid)
        return {"source": source_cid, "target": target_cid, "connected": False, "reasons": [{"type": "missing_entity", "entities": missing}]}

    src_edges = store.find_edges(out_v=source["vid"], limit=1000)
    store.find_edges(in_v=target["vid"], limit=1000)

    direct = [e for e in src_edges if e["in_v"] == target["vid"]]
    if direct:
        return {
            "source": source_cid,
            "target": target_cid,
            "connected": True,
            "edges": [{"label": e["label"], "eid": e["eid"]} for e in direct],
            "reasons": [],
        }

    reasons: list[dict] = []

    src_domain = VERTEX_LABELS.get(source["label"], ("",))[0]
    tgt_domain = VERTEX_LABELS.get(target["label"], ("",))[0]
    if src_domain != tgt_domain:
        reasons.append({
            "type": "domain_mismatch",
            "description": f"Source is in {src_domain} domain, target is in {tgt_domain} domain",
        })

    from eoip.ontology.manifest import EDGE_LABELS
    possible_edges = []
    for label, (outs, ins, _) in EDGE_LABELS.items():
        if source["label"] in outs and target["label"] in ins:
            possible_edges.append(label)
    if not possible_edges:
        reasons.append({
            "type": "no_valid_edge_type",
            "description": f"No edge label allows {source['label']} -> {target['label']}",
        })
    else:
        reasons.append({
            "type": "missing_edge",
            "description": f"Valid edge types exist ({', '.join(possible_edges)}) but none are present",
            "possible_edges": possible_edges,
        })

    return {
        "source": source_cid,
        "target": target_cid,
        "connected": False,
        "reasons": reasons,
    }


def query_what_changed(store: GraphStore, entity_cid: str) -> dict:
    """Structured WHAT CHANGED: returns revision history and recent changes.

    Looks at EntityRevision vertices linked to the entity.
    """
    entity = store.get_vertex_by_canonical_id(entity_cid)
    if not entity:
        return {"entity": entity_cid, "changes": [], "error": "Entity not found"}

    changes: list[dict] = []

    out_edges = store.find_edges(out_v=entity["vid"], limit=500)
    for edge in out_edges:
        if edge["label"] == "HAS_CHANGE":
            target = store.get_vertex(edge["in_v"])
            if target and target["label"] == "WorkItemChange":
                changes.append({
                    "type": "field_change",
                    "change_id": target["canonical_id"],
                    "field": target["properties"].get("field_name", ""),
                    "from": target["properties"].get("from_value", ""),
                    "to": target["properties"].get("to_value", ""),
                    "timestamp": target["properties"].get("created_at", ""),
                })

    edges = store.find_edges(in_v=entity["vid"], limit=500)
    for edge in edges:
        if edge["label"] in ("HAS_CHANGE", "MODIFIES"):
            src = store.get_vertex(edge["out_v"])
            if not src:
                continue
            if src["label"] == "WorkItemChange":
                changes.append({
                    "type": "field_change",
                    "change_id": src["canonical_id"],
                    "field": src["properties"].get("field_name", ""),
                    "from": src["properties"].get("from_value", ""),
                    "to": src["properties"].get("to_value", ""),
                    "timestamp": src["properties"].get("created_at", ""),
                })
            elif src["label"] == "Commit":
                changes.append({
                    "type": "code_change",
                    "commit": src["canonical_id"],
                    "sha": src["properties"].get("commit_sha", ""),
                    "message": src["properties"].get("message", ""),
                    "author": src["properties"].get("author_email", ""),
                    "timestamp": src["properties"].get("created_at", ""),
                })

    revisions = store.find_vertices(label="EntityRevision", limit=10_000)
    entity_revisions = [r for r in revisions if r["properties"].get("subject_id") == entity_cid]
    for rev in entity_revisions:
        changes.append({
            "type": "revision",
            "revision_id": rev["canonical_id"],
            "is_current": rev["properties"].get("is_current"),
            "observed_at": rev["properties"].get("observed_at", ""),
            "change_kind": rev["properties"].get("change_kind", ""),
        })

    changes.sort(key=lambda c: c.get("timestamp", c.get("observed_at", "")), reverse=True)

    return {
        "entity": entity_cid,
        "label": entity["label"],
        "name": entity["properties"].get("name", ""),
        "changes": changes,
        "total_changes": len(changes),
    }


def query_context(store: GraphStore, entity_cid: str) -> dict:
    """Structured WHEN/WHO/WHERE/HOW: contextual metadata for an entity.

    Returns temporal context (when), actor context (who),
    location context (where), and method context (how).
    """
    entity = store.get_vertex_by_canonical_id(entity_cid)
    if not entity:
        return {"entity": entity_cid, "error": "Entity not found"}

    props = entity["properties"]
    when = {
        "created_at": props.get("created_at"),
        "modified_at": props.get("modified_at"),
        "first_seen": props.get("first_seen"),
        "last_seen": props.get("last_seen"),
    }

    who: list[dict] = []
    edges = store.find_edges(out_v=entity["vid"], limit=500)
    for edge in edges:
        if edge["label"] in ("ASSIGNED_TO", "AUTHORED_BY", "REPORTED_BY"):
            person = store.get_vertex(edge["in_v"])
            if person:
                who.append({
                    "role": edge["label"].lower().replace("_", " "),
                    "canonical_id": person["canonical_id"],
                    "name": person["properties"].get("display_name", ""),
                    "email": person["properties"].get("email", ""),
                })
    if props.get("author_email"):
        who.append({"role": "author", "email": props["author_email"], "name": props.get("author_name", "")})

    where = {
        "source_system": props.get("source_system"),
        "source_uri": props.get("source_uri"),
        "path": props.get("path"),
        "repo_id": props.get("repo_id"),
        "domain": VERTEX_LABELS.get(entity["label"], ("",))[0],
    }

    how = {
        "creation_status": props.get("creation_status"),
        "ingestion_run_id": props.get("ingestion_run_id"),
        "mapper_version": props.get("mapper_version"),
        "parser_version": props.get("parser_version"),
    }

    return {
        "entity": entity_cid,
        "label": entity["label"],
        "name": props.get("name", ""),
        "when": {k: v for k, v in when.items() if v},
        "who": who,
        "where": {k: v for k, v in where.items() if v},
        "how": {k: v for k, v in how.items() if v},
    }
