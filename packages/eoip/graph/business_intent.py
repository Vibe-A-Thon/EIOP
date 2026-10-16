"""Business intent and capability graph service (G2-T0620..0622, G2-GRAPH-BIZ-001..003).

Manages business objectives, capabilities, and the intent-to-runtime
traceability chain. Supports reverse traversal from runtime to business intent.
"""

from __future__ import annotations

from datetime import UTC, datetime

from eoip.graph.store import GraphStore


def ingest_objective(
    store: GraphStore,
    name: str,
    *,
    description: str = "",
    objective_type: str = "strategic",
    priority: str = "medium",
    kpi_target: str = "",
    owner_id: str = "",
    ingestion_run_id: str = "manual",
) -> dict:
    """Create or update a BusinessObjective vertex."""
    now = datetime.now(UTC).isoformat()
    cid = f"urn:eoip:objective:{name.lower().replace(' ', '-')}"
    return store.upsert_vertex("BusinessObjective", {
        "canonical_id": cid,
        "name": name,
        "description": description,
        "objective_type": objective_type,
        "strategic_priority": priority,
        "kpi_target": kpi_target,
        "owner_id": owner_id,
        "ingestion_run_id": ingestion_run_id,
        "created_at": now,
    })


def ingest_capability(
    store: GraphStore,
    name: str,
    *,
    description: str = "",
    level: int = 1,
    business_domain: str = "",
    owner_id: str = "",
    parent_cid: str | None = None,
    objective_cid: str | None = None,
    ingestion_run_id: str = "manual",
) -> dict:
    """Create or update a BusinessCapability vertex and its relationships."""
    now = datetime.now(UTC).isoformat()
    cid = f"urn:eoip:capability:{name.lower().replace(' ', '-')}"
    cap = store.upsert_vertex("BusinessCapability", {
        "canonical_id": cid,
        "name": name,
        "description": description,
        "capability_level": level,
        "business_domain": business_domain,
        "owner_id": owner_id,
        "ingestion_run_id": ingestion_run_id,
        "created_at": now,
    })

    if parent_cid:
        parent = store.get_vertex_by_canonical_id(parent_cid)
        if parent:
            store.upsert_edge("DECOMPOSES_INTO", parent["vid"], cap["vid"], {
                "fact_key": f"decompose:{parent_cid}:{cid}",
                "creation_status": "DETERMINISTIC",
            })

    if objective_cid:
        obj = store.get_vertex_by_canonical_id(objective_cid)
        if obj:
            store.upsert_edge("FULFILLS", cap["vid"], obj["vid"], {
                "fact_key": f"fulfills:{cid}:{objective_cid}",
                "creation_status": "DETERMINISTIC",
            })

    return cap


def link_to_capability(
    store: GraphStore,
    entity_cid: str,
    capability_cid: str,
) -> dict | None:
    """Link a technical entity (Service, Project, etc.) to a BusinessCapability via REALIZES."""
    entity = store.get_vertex_by_canonical_id(entity_cid)
    cap = store.get_vertex_by_canonical_id(capability_cid)
    if not entity or not cap:
        return None
    store.upsert_edge("REALIZES", entity["vid"], cap["vid"], {
        "fact_key": f"realizes:{entity_cid}:{capability_cid}",
        "creation_status": "DETERMINISTIC",
    })
    return {"entity": entity_cid, "capability": capability_cid, "edge": "REALIZES"}


def reverse_impact(store: GraphStore, service_cid: str) -> dict:
    """Traverse from a runtime entity backwards to affected business capabilities and objectives.

    Chain: Service/Deployment <- REALIZES <- BusinessCapability <- FULFILLS <- BusinessObjective
    Also: Service <- TRACES_TO <- BusinessObjective/BusinessCapability
    """
    service = store.get_vertex_by_canonical_id(service_cid)
    if not service:
        return {"entity": service_cid, "capabilities": [], "objectives": []}

    capabilities: list[dict] = []
    objectives: list[dict] = []
    seen_caps: set[str] = set()
    seen_objs: set[str] = set()

    edges = store.find_edges(out_v=service["vid"], limit=1000)
    for edge in edges:
        if edge["label"] == "REALIZES":
            cap = store.get_vertex(edge["in_v"])
            if cap and cap["canonical_id"] not in seen_caps:
                seen_caps.add(cap["canonical_id"])
                capabilities.append({
                    "canonical_id": cap["canonical_id"],
                    "name": cap["properties"].get("name", ""),
                    "level": cap["properties"].get("capability_level"),
                    "domain": cap["properties"].get("business_domain", ""),
                })
                cap_edges = store.find_edges(out_v=cap["vid"], limit=100)
                for ce in cap_edges:
                    if ce["label"] == "FULFILLS":
                        obj = store.get_vertex(ce["in_v"])
                        if obj and obj["canonical_id"] not in seen_objs:
                            seen_objs.add(obj["canonical_id"])
                            objectives.append({
                                "canonical_id": obj["canonical_id"],
                                "name": obj["properties"].get("name", ""),
                                "type": obj["properties"].get("objective_type", ""),
                                "priority": obj["properties"].get("strategic_priority", ""),
                            })

    in_edges = store.find_edges(in_v=service["vid"], limit=1000)
    for edge in in_edges:
        if edge["label"] == "TRACES_TO":
            src = store.get_vertex(edge["out_v"])
            if not src:
                continue
            if src["label"] == "BusinessCapability" and src["canonical_id"] not in seen_caps:
                seen_caps.add(src["canonical_id"])
                capabilities.append({
                    "canonical_id": src["canonical_id"],
                    "name": src["properties"].get("name", ""),
                    "level": src["properties"].get("capability_level"),
                    "domain": src["properties"].get("business_domain", ""),
                })
            elif src["label"] == "BusinessObjective" and src["canonical_id"] not in seen_objs:
                seen_objs.add(src["canonical_id"])
                objectives.append({
                    "canonical_id": src["canonical_id"],
                    "name": src["properties"].get("name", ""),
                    "type": src["properties"].get("objective_type", ""),
                    "priority": src["properties"].get("strategic_priority", ""),
                })

    return {
        "entity": service_cid,
        "capabilities": capabilities,
        "objectives": objectives,
        "total_affected": len(capabilities) + len(objectives),
    }


def intent_to_runtime_chain(store: GraphStore, objective_cid: str) -> dict:
    """Traverse the full intent-to-runtime chain from a business objective.

    Chain: BusinessObjective -> BusinessCapability -> Requirement/WorkItem ->
           Code/API -> Test -> Build -> Deployment -> Runtime
    """
    obj = store.get_vertex_by_canonical_id(objective_cid)
    if not obj:
        return {"objective": objective_cid, "chain": [], "depth": 0}

    chain: list[dict] = [{"canonical_id": obj["canonical_id"], "label": "BusinessObjective", "name": obj["properties"].get("name", "")}]
    visited: set[str] = {obj["canonical_id"]}

    frontier = [obj]

    for _ in range(10):
        next_frontier: list[dict] = []
        for node in frontier:
            for edge in store.find_edges(in_v=node["vid"], limit=500):
                target = store.get_vertex(edge["out_v"])
                if target and target["canonical_id"] not in visited:
                    visited.add(target["canonical_id"])
                    chain.append({
                        "canonical_id": target["canonical_id"],
                        "label": target["label"],
                        "name": target["properties"].get("name", ""),
                        "edge": edge["label"],
                    })
                    next_frontier.append(target)
            for edge in store.find_edges(out_v=node["vid"], limit=500):
                if edge["label"] in ("DECOMPOSES_INTO", "TRACES_TO", "FULFILLS", "REALIZES"):
                    continue
                target = store.get_vertex(edge["in_v"])
                if target and target["canonical_id"] not in visited:
                    visited.add(target["canonical_id"])
                    chain.append({
                        "canonical_id": target["canonical_id"],
                        "label": target["label"],
                        "name": target["properties"].get("name", ""),
                        "edge": edge["label"],
                    })
                    next_frontier.append(target)
        if not next_frontier:
            break
        frontier = next_frontier

    return {
        "objective": objective_cid,
        "chain": chain,
        "depth": max((c.get("edge") is not None for c in chain), default=0),
        "labels_present": sorted({c["label"] for c in chain}),
    }


reverse_traversal = reverse_impact


def flag_unowned_production_assets(store: GraphStore) -> list[dict]:
    """Flag critical production assets without business/requirement ownership (G2-I2R-004)."""
    findings: list[dict] = []
    for label in ("Deployment", "Service"):
        for v in store.find_vertices(label=label, limit=10_000):
            props = v.get("properties", {})
            is_prod = props.get("environment") == "production" or label == "Deployment"
            if not is_prod:
                continue
            impact = reverse_impact(store, v["canonical_id"])
            if not impact["capabilities"] and not impact["objectives"]:
                findings.append({
                    "canonical_id": v["canonical_id"],
                    "label": label,
                    "name": props.get("name") or v["canonical_id"],
                    "issue": "Production asset has no business capability or objective link",
                    "severity": "CRITICAL",
                })
    return findings


def flag_untraced_critical_requirements(store: GraphStore) -> list[dict]:
    """Flag business-critical requirements without runtime traceability (G2-I2R-005)."""
    findings: list[dict] = []
    for label in ("Requirement", "Feature", "UserStory"):
        for v in store.find_vertices(label=label, limit=10_000):
            props = v.get("properties", {})
            is_critical = (
                props.get("priority") in ("P0", "P1", "critical", "high")
                or props.get("severity") in ("CRITICAL", "HIGH")
                or props.get("strategic_priority") in ("P0", "P1", "critical", "high")
            )
            if not is_critical:
                continue
            edges = store.find_edges(out_v=v["vid"], limit=100) + store.find_edges(in_v=v["vid"], limit=100)
            has_runtime = False
            for e in edges:
                peer_vid = e["in_v"] if e["out_v"] == v["vid"] else e["out_v"]
                peer = store.get_vertex(peer_vid)
                if peer and peer["label"] in ("Service", "Deployment", "PipelineRun", "BuildRecord"):
                    has_runtime = True
                    break
            if not has_runtime:
                findings.append({
                    "canonical_id": v["canonical_id"],
                    "label": label,
                    "name": props.get("name", ""),
                    "priority": props.get("priority") or props.get("severity") or props.get("strategic_priority"),
                    "issue": "Critical requirement lacks runtime deployment or service traceability",
                    "severity": "CRITICAL",
                })
    return findings
