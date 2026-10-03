"""Lens framework — shared knowledge context and lens-specific data (G2-P10, G2-UX-LENS-001..003).

A lens provides a focused view of the knowledge graph from a particular
perspective (evidence, impact, timeline, architecture, etc.). All lenses
share a KnowledgeContext so switching between them preserves scope.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from eoip.graph.store import GraphStore
from eoip.ontology.manifest import VERTEX_LABELS, EDGE_LABELS, DOMAINS


@dataclass
class KnowledgeContext:
    root_entities: list[str] = field(default_factory=list)
    graph_version: str | None = None
    as_of: str | None = None
    domains: list[str] = field(default_factory=lambda: list(DOMAINS))
    trust_threshold: str | None = None
    filters: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "root_entities": self.root_entities,
            "graph_version": self.graph_version,
            "as_of": self.as_of,
            "domains": self.domains,
            "trust_threshold": self.trust_threshold,
            "filters": self.filters,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> KnowledgeContext:
        return cls(
            root_entities=d.get("root_entities", []),
            graph_version=d.get("graph_version"),
            as_of=d.get("as_of"),
            domains=d.get("domains", list(DOMAINS)),
            trust_threshold=d.get("trust_threshold"),
            filters=d.get("filters", {}),
        )


LENS_CATALOG = [
    {"id": "search", "name": "Search", "description": "Full-text and structured search across the knowledge graph"},
    {"id": "graph", "name": "Graph", "description": "Visual graph exploration with level-of-detail rendering"},
    {"id": "evidence", "name": "Evidence", "description": "Provenance chain and evidence trail for any entity"},
    {"id": "impact", "name": "Impact", "description": "Blast radius and dependency impact analysis"},
    {"id": "timeline", "name": "Timeline", "description": "Temporal view of entity changes and events"},
    {"id": "change", "name": "Change", "description": "Change history and revision comparison"},
    {"id": "architecture", "name": "Architecture", "description": "Architecture conformance and dependency view"},
    {"id": "runtime", "name": "Runtime", "description": "Runtime services, deployments, and incident correlation"},
    {"id": "requirement", "name": "Requirement", "description": "Requirements traceability from objective to deployment"},
    {"id": "trust", "name": "Trust", "description": "Evidence coverage and confidence scoring"},
    {"id": "security", "name": "Security", "description": "Vulnerability and access pattern analysis"},
    {"id": "release", "name": "Release", "description": "Release pipeline and deployment tracking"},
    {"id": "process", "name": "Process", "description": "Process mining and workflow deviation analysis"},
    {"id": "knowledge_health", "name": "Knowledge Health", "description": "Knowledge debt and SLO monitoring"},
    {"id": "simulation", "name": "Simulation", "description": "What-if simulation and counterfactual analysis"},
    {"id": "agent", "name": "Agent", "description": "AI agent run history and governance"},
    {"id": "decision", "name": "Decision", "description": "Architecture decision records and rationale"},
    {"id": "api", "name": "API", "description": "API service catalog and connectivity"},
    {"id": "test", "name": "Test", "description": "Test coverage and test-to-code mapping"},
    {"id": "ontology", "name": "Ontology", "description": "Ontology schema explorer and validation"},
]


def list_lenses() -> list[dict[str, str]]:
    return list(LENS_CATALOG)


def lens_data(store: GraphStore, lens_id: str, context: KnowledgeContext) -> dict[str, Any]:
    """Return lens-specific data scoped by the knowledge context."""
    handler = _LENS_HANDLERS.get(lens_id)
    if not handler:
        return {"error": f"Unknown lens: {lens_id}", "available": [l["id"] for l in LENS_CATALOG]}
    return handler(store, context)


def _search_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    results: list[dict] = []
    for cid in ctx.root_entities:
        v = store.get_vertex_by_canonical_id(cid)
        if v:
            domain = VERTEX_LABELS.get(v["label"], ("",))[0]
            if ctx.domains and domain not in ctx.domains:
                continue
            results.append({"canonical_id": cid, "label": v["label"], "name": v["properties"].get("name", ""), "domain": domain})
    if not ctx.root_entities:
        for domain in ctx.domains[:5]:
            for lbl, (d, _, _) in VERTEX_LABELS.items():
                if d == domain:
                    for v in store.find_vertices(label=lbl, limit=10):
                        results.append({"canonical_id": v["canonical_id"], "label": v["label"], "name": v["properties"].get("name", ""), "domain": d})
                    break
    return {"lens": "search", "results": results[:100], "total": len(results)}


def _evidence_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    evidence_chains: list[dict] = []
    for cid in ctx.root_entities:
        v = store.get_vertex_by_canonical_id(cid)
        if not v:
            continue
        out_edges = store.find_edges(out_v=v["vid"], limit=500)
        ev_edges = [e for e in out_edges if e["label"] == "EVIDENCED_BY"]
        evidence_list: list[dict] = []
        for e in ev_edges:
            ev = store.get_vertex(e["in_v"])
            if ev:
                evidence_list.append({
                    "evidence_id": ev["canonical_id"],
                    "source_system": ev["properties"].get("source_system", ""),
                    "method": ev["properties"].get("method", ""),
                    "confidence": ev["properties"].get("confidence"),
                })
        evidence_chains.append({"entity": cid, "evidence": evidence_list, "count": len(evidence_list)})
    return {"lens": "evidence", "chains": evidence_chains}


def _impact_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    impacts: list[dict] = []
    for cid in ctx.root_entities:
        v = store.get_vertex_by_canonical_id(cid)
        if not v:
            continue
        out_edges = store.find_edges(out_v=v["vid"], limit=200)
        in_edges = store.find_edges(in_v=v["vid"], limit=200)
        dependents: list[dict] = []
        for e in in_edges:
            src = store.get_vertex(e["out_v"])
            if src:
                dependents.append({"canonical_id": src["canonical_id"], "label": src["label"], "via": e["label"]})
        dependencies: list[dict] = []
        for e in out_edges:
            tgt = store.get_vertex(e["in_v"])
            if tgt:
                dependencies.append({"canonical_id": tgt["canonical_id"], "label": tgt["label"], "via": e["label"]})
        impacts.append({
            "entity": cid, "label": v["label"],
            "dependents": dependents[:50], "dependencies": dependencies[:50],
            "dependent_count": len(dependents), "dependency_count": len(dependencies),
        })
    return {"lens": "impact", "impacts": impacts}


def _timeline_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    events: list[dict] = []
    for cid in ctx.root_entities:
        v = store.get_vertex_by_canonical_id(cid)
        if not v:
            continue
        props = v["properties"]
        for field in ("created_at", "modified_at", "started_at", "finished_at", "resolved_at"):
            ts = props.get(field)
            if ts:
                events.append({"entity": cid, "label": v["label"], "event": field, "timestamp": ts})
        out_edges = store.find_edges(out_v=v["vid"], limit=200)
        for e in out_edges:
            if e["label"] == "HAS_CHANGE":
                change = store.get_vertex(e["in_v"])
                if change:
                    events.append({
                        "entity": cid, "label": "WorkItemChange",
                        "event": f"field_change:{change['properties'].get('field_name', '')}",
                        "timestamp": change["properties"].get("created_at", ""),
                        "from_value": change["properties"].get("from_value", ""),
                        "to_value": change["properties"].get("to_value", ""),
                    })
    events.sort(key=lambda e: e.get("timestamp", ""))
    return {"lens": "timeline", "events": events}


def _architecture_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    services = store.find_vertices(label="Service", limit=200)
    apis = store.find_vertices(label="APIService", limit=200)
    deps: list[dict] = []
    for svc in services:
        domain = VERTEX_LABELS.get(svc["label"], ("",))[0]
        if ctx.domains and domain not in ctx.domains:
            continue
        out = store.find_edges(out_v=svc["vid"], limit=100)
        for e in out:
            if e["label"] in ("DEPENDS_ON", "CONNECTS_TO"):
                tgt = store.get_vertex(e["in_v"])
                if tgt:
                    deps.append({"from": svc["canonical_id"], "to": tgt["canonical_id"], "via": e["label"]})
    return {
        "lens": "architecture",
        "services": [{"canonical_id": s["canonical_id"], "name": s["properties"].get("name", "")} for s in services],
        "api_services": [{"canonical_id": a["canonical_id"], "name": a["properties"].get("api_name", "")} for a in apis],
        "dependencies": deps,
    }


def _trust_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    all_vertices = store.find_vertices(limit=10_000)
    business = [v for v in all_vertices if VERTEX_LABELS.get(v["label"], ("META",))[0] != "META"]
    evidenced = 0
    for v in business:
        ev_edges = store.find_edges(out_v=v["vid"], label="EVIDENCED_BY", limit=1)
        if ev_edges:
            evidenced += 1
    total = max(len(business), 1)
    low_confidence: list[dict] = []
    for v in business:
        conf = v["properties"].get("confidence")
        status = v["properties"].get("creation_status", "DETERMINISTIC")
        if status == "INFERRED" or (conf is not None and float(conf) < 0.5):
            low_confidence.append({"canonical_id": v["canonical_id"], "label": v["label"], "confidence": conf, "creation_status": status})
    return {
        "lens": "trust",
        "evidence_coverage": evidenced / total,
        "total_entities": len(business),
        "evidenced_entities": evidenced,
        "low_confidence_entities": low_confidence[:50],
    }


def _ontology_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    label_counts: dict[str, int] = {}
    for lbl in VERTEX_LABELS:
        count = store.count_vertices(label=lbl)
        if count > 0:
            label_counts[lbl] = count
    edge_counts: dict[str, int] = {}
    for lbl in EDGE_LABELS:
        count = store.count_edges(label=lbl)
        if count > 0:
            edge_counts[lbl] = count
    return {
        "lens": "ontology",
        "vertex_types": len(VERTEX_LABELS),
        "edge_types": len(EDGE_LABELS),
        "domains": DOMAINS,
        "active_vertex_labels": label_counts,
        "active_edge_labels": edge_counts,
    }


def _graph_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    nodes: list[dict] = []
    edges: list[dict] = []
    seen_vids: set[str] = set()
    for cid in ctx.root_entities[:20]:
        v = store.get_vertex_by_canonical_id(cid)
        if not v:
            continue
        if v["vid"] not in seen_vids:
            nodes.append({"vid": v["vid"], "canonical_id": cid, "label": v["label"], "name": v["properties"].get("name", "")})
            seen_vids.add(v["vid"])
        for e in store.edges_from(v["vid"], limit=50):
            tgt = store.get_vertex(e["in_v"])
            if tgt and tgt["vid"] not in seen_vids:
                nodes.append({"vid": tgt["vid"], "canonical_id": tgt["canonical_id"], "label": tgt["label"], "name": tgt["properties"].get("name", "")})
                seen_vids.add(tgt["vid"])
            edges.append({"source": v["vid"], "target": e["in_v"], "label": e["label"]})
        for e in store.edges_to(v["vid"], limit=50):
            src = store.get_vertex(e["out_v"])
            if src and src["vid"] not in seen_vids:
                nodes.append({"vid": src["vid"], "canonical_id": src["canonical_id"], "label": src["label"], "name": src["properties"].get("name", "")})
                seen_vids.add(src["vid"])
            edges.append({"source": e["out_v"], "target": v["vid"], "label": e["label"]})
    return {"lens": "graph", "nodes": nodes[:200], "edges": edges[:500]}


def _change_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    from eoip.graph.query_operators import query_what_changed
    changes: list[dict] = []
    for cid in ctx.root_entities:
        changes.append(query_what_changed(store, cid))
    return {"lens": "change", "entities": changes}


def _runtime_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    deployments = store.find_vertices(label="Deployment", limit=100)
    incidents = store.find_vertices(label="Incident", limit=100)
    alerts = store.find_vertices(label="AlertEvent", limit=100)
    return {
        "lens": "runtime",
        "deployments": [{"canonical_id": d["canonical_id"], "name": d["properties"].get("name", ""), "status": d["properties"].get("status", "")} for d in deployments],
        "incidents": [{"canonical_id": i["canonical_id"], "number": i["properties"].get("incident_number", ""), "summary": i["properties"].get("summary", "")} for i in incidents],
        "alerts": [{"canonical_id": a["canonical_id"], "name": a["properties"].get("name", "")} for a in alerts],
    }


def _requirement_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    requirements = store.find_vertices(label="Requirement", limit=200)
    objectives = store.find_vertices(label="BusinessObjective", limit=100)
    items: list[dict] = []
    for r in requirements:
        linked_edges = store.find_edges(in_v=r["vid"], limit=100)
        traces = [e for e in linked_edges if e["label"] == "TRACES_TO"]
        items.append({
            "canonical_id": r["canonical_id"], "name": r["properties"].get("name", ""),
            "status": r["properties"].get("status", ""), "trace_count": len(traces),
        })
    return {"lens": "requirement", "requirements": items, "objectives": [{"canonical_id": o["canonical_id"], "name": o["properties"].get("name", "")} for o in objectives]}


def _process_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    from eoip.graph.process_mining import extract_cases_from_graph, discover_process_paths
    cases = extract_cases_from_graph(store)
    paths = discover_process_paths(cases) if cases else {"total_cases": 0, "unique_paths": 0, "paths": [], "transitions": []}
    return {"lens": "process", "cases": len(cases), "paths": paths}


def _knowledge_health_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    from eoip.graph.knowledge_debt import detect_knowledge_debt
    return {"lens": "knowledge_health", **detect_knowledge_debt(store)}


def _simulation_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    return {"lens": "simulation", "available": True, "description": "Use /api/v1/simulation/* endpoints to create and run simulations"}


def _decision_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    decisions = store.find_vertices(label="Decision", limit=200)
    return {
        "lens": "decision",
        "decisions": [{
            "canonical_id": d["canonical_id"], "name": d["properties"].get("name", ""),
            "status": d["properties"].get("decision_status", ""), "date": d["properties"].get("decision_date", ""),
        } for d in decisions],
    }


def _api_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    services = store.find_vertices(label="APIService", limit=200)
    endpoints = store.find_vertices(label="APIEndpoint", limit=500)
    return {
        "lens": "api",
        "services": [{"canonical_id": s["canonical_id"], "name": s["properties"].get("api_name", "")} for s in services],
        "endpoints": [{
            "canonical_id": e["canonical_id"], "method": e["properties"].get("api_method", ""),
            "path": e["properties"].get("api_path", ""),
        } for e in endpoints],
    }


def _test_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    test_cases = store.find_vertices(label="TestCase", limit=500)
    test_runs = store.find_vertices(label="TestRun", limit=100)
    return {
        "lens": "test",
        "test_cases": len(test_cases),
        "test_runs": len(test_runs),
        "cases": [{"canonical_id": t["canonical_id"], "name": t["properties"].get("name", ""), "status": t["properties"].get("test_status", "")} for t in test_cases[:50]],
    }


def _release_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    releases = store.find_vertices(label="Release", limit=100)
    deployments = store.find_vertices(label="Deployment", limit=100)
    return {
        "lens": "release",
        "releases": [{"canonical_id": r["canonical_id"], "name": r["properties"].get("name", ""), "tag": r["properties"].get("tag_name", "")} for r in releases],
        "deployments": [{"canonical_id": d["canonical_id"], "name": d["properties"].get("name", ""), "environment": d["properties"].get("environment", "")} for d in deployments],
    }


def _security_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    findings = store.find_vertices(label="ValidationFinding", limit=500)
    security_findings = [f for f in findings if f["properties"].get("rule_id", "").startswith("SEC")]
    return {
        "lens": "security",
        "total_findings": len(security_findings),
        "findings": [{"canonical_id": f["canonical_id"], "rule_id": f["properties"].get("rule_id", ""), "severity": f["properties"].get("severity", "")} for f in security_findings[:50]],
    }


def _agent_lens(store: GraphStore, ctx: KnowledgeContext) -> dict[str, Any]:
    agent_runs = store.find_vertices(label="AgentRun", limit=200)
    return {
        "lens": "agent",
        "total_runs": len(agent_runs),
        "runs": [{"canonical_id": a["canonical_id"], "agent_id": a["properties"].get("agent_id", ""), "status": a["properties"].get("run_status", ""), "goal": a["properties"].get("goal", "")} for a in agent_runs[:50]],
    }


_LENS_HANDLERS: dict[str, Any] = {
    "search": _search_lens,
    "graph": _graph_lens,
    "evidence": _evidence_lens,
    "impact": _impact_lens,
    "timeline": _timeline_lens,
    "change": _change_lens,
    "architecture": _architecture_lens,
    "runtime": _runtime_lens,
    "requirement": _requirement_lens,
    "trust": _trust_lens,
    "security": _security_lens,
    "release": _release_lens,
    "process": _process_lens,
    "knowledge_health": _knowledge_health_lens,
    "simulation": _simulation_lens,
    "agent": _agent_lens,
    "decision": _decision_lens,
    "api": _api_lens,
    "test": _test_lens,
    "ontology": _ontology_lens,
}
