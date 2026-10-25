"""Knowledge debt catalog and SLO evaluator (G2-KD-001..006, G2-SLO-001..005).

Detects knowledge debt (unowned components, undocumented APIs, stale docs,
missing tests, broken provenance) and evaluates knowledge health SLOs.
"""

from __future__ import annotations

from typing import Any

from dataclasses import dataclass

from eoip.graph.store import GraphStore
from eoip.ontology.manifest import VERTEX_LABELS


from dataclasses import field

REMEDIATION_MAP = {
    "unowned_component": "Assign an owning team or person via ASSIGNED_TO relationship.",
    "undocumented_api": "Link API documentation page via DOCUMENTS or DOCUMENTS_API edge.",
    "unlinked_requirement": "Link implementation artifacts or test cases via IMPLEMENTS / TESTS edge.",
    "unlinked_implementation": "Link code symbols to owning modules, files, or requirements.",
    "stale_document": "Review and update document freshness, archiving obsolete revisions.",
    "unresolved_identity": "Resolve person identity or merge conflicting profiles to canonical user record.",
    "broken_provenance": "Attach ingestion provenance or raw source reference via EVIDENCED_BY edge.",
    "low_confidence_inference": "Review inferred relationship and confirm or reject with human verification.",
    "missing_test": "Add automated test suite and link via TESTS edge.",
    "missing_architecture_mapping": "Link component to architecture diagram or system blueprint.",
    "unknown_production_owner": "Declare production on-call escalation policy and service owner.",
    "stale_runbook": "Update operational runbook and verify verification date.",
}


@dataclass
class DebtFinding:
    category: str
    canonical_id: str
    label: str
    name: str
    description: str
    severity: str = "WARNING"
    remediation_action: str = ""
    evidence_ref: str = ""
    dimension: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.remediation_action:
            self.remediation_action = REMEDIATION_MAP.get(
                self.category, "Investigate and remediate knowledge debt item."
            )

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "canonical_id": self.canonical_id,
            "label": self.label,
            "name": self.name,
            "description": self.description,
            "severity": self.severity,
            "remediation_action": self.remediation_action,
            "evidence_ref": self.evidence_ref,
            "dimension": self.dimension,
        }


DEBT_CATEGORIES = [
    "unowned_component",
    "undocumented_api",
    "unlinked_requirement",
    "unlinked_implementation",
    "stale_document",
    "unresolved_identity",
    "broken_provenance",
    "low_confidence_inference",
    "missing_test",
    "missing_architecture_mapping",
    "unknown_production_owner",
    "stale_runbook",
]


def _extract_dimensions(vertex: dict) -> dict[str, str]:
    props = vertex.get("properties", {})
    return {
        "project": props.get("project_id") or props.get("project") or "unspecified",
        "team": props.get("team_id") or props.get("team") or props.get("owner_team") or "unassigned",
        "service": props.get("service_id") or props.get("service") or (vertex.get("canonical_id") if vertex.get("label") == "Service" else "unspecified"),
        "application": props.get("app_id") or props.get("application") or "unspecified",
        "domain": props.get("graph_domain") or props.get("domain") or "default",
        "release": props.get("release_id") or props.get("release") or "unversioned",
    }


def compute_debt_by_dimensions(findings: list[DebtFinding]) -> dict[str, dict[str, int]]:
    """Compute debt grouped by dimensions (G2-KD-003): project, team, service, application, domain, release."""
    dimensions = ["project", "team", "service", "application", "domain", "release"]
    result: dict[str, dict[str, int]] = {dim: {} for dim in dimensions}
    for f in findings:
        for dim in dimensions:
            val = f.dimension.get(dim) or "unspecified"
            result[dim][val] = result[dim].get(val, 0) + 1
    return result


def compute_multidimensional_debt(findings: list[DebtFinding]) -> dict[str, Any]:
    """Exposes contributing dimensions and facets rather than a single opaque score (G2-KD-004)."""
    by_dim = compute_debt_by_dimensions(findings)
    by_category: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    for f in findings:
        by_category[f.category] = by_category.get(f.category, 0) + 1
        by_severity[f.severity] = by_severity.get(f.severity, 0) + 1

    dimensional_facets = {
        "ownership": by_category.get("unowned_component", 0) + by_category.get("unknown_production_owner", 0),
        "documentation": by_category.get("undocumented_api", 0) + by_category.get("stale_document", 0) + by_category.get("stale_runbook", 0),
        "traceability": by_category.get("unlinked_requirement", 0) + by_category.get("unlinked_implementation", 0) + by_category.get("missing_architecture_mapping", 0),
        "testing": by_category.get("missing_test", 0),
        "provenance_and_trust": by_category.get("broken_provenance", 0) + by_category.get("low_confidence_inference", 0) + by_category.get("unresolved_identity", 0),
    }

    return {
        "total_findings": len(findings),
        "by_dimension": by_dim,
        "by_category": by_category,
        "by_severity": by_severity,
        "dimensional_facets": dimensional_facets,
    }


class DebtTrendTracker:
    """Tracks knowledge debt trends across time (G2-KD-005)."""

    def __init__(self) -> None:
        self.snapshots: list[dict[str, Any]] = []

    def record_snapshot(
        self,
        findings: list[DebtFinding],
        timestamp: str | None = None,
        label: str | None = None,
    ) -> dict[str, Any]:
        from datetime import datetime, timezone
        ts = timestamp or datetime.now(timezone.utc).isoformat()
        categories: dict[str, int] = {}
        for f in findings:
            categories[f.category] = categories.get(f.category, 0) + 1
        snapshot = {
            "timestamp": ts,
            "label": label or f"snapshot-{len(self.snapshots) + 1}",
            "total_debt": len(findings),
            "by_category": categories,
        }
        self.snapshots.append(snapshot)
        return snapshot

    def get_trends(self) -> dict[str, Any]:
        if len(self.snapshots) < 2:
            return {"status": "insufficient_data", "snapshots": self.snapshots}
        first = self.snapshots[0]
        latest = self.snapshots[-1]
        delta_total = latest["total_debt"] - first["total_debt"]
        direction = "improving" if delta_total < 0 else ("degrading" if delta_total > 0 else "stable")

        category_deltas: dict[str, int] = {}
        all_cats = set(first["by_category"].keys()) | set(latest["by_category"].keys())
        for c in all_cats:
            category_deltas[c] = latest["by_category"].get(c, 0) - first["by_category"].get(c, 0)

        return {
            "direction": direction,
            "delta_total": delta_total,
            "category_deltas": category_deltas,
            "history_count": len(self.snapshots),
            "first_snapshot": first,
            "latest_snapshot": latest,
        }


def detect_knowledge_debt(store: GraphStore) -> dict:
    """Run all knowledge debt detection rules against the graph."""
    findings: list[DebtFinding] = []

    findings.extend(_detect_unowned_services(store))
    findings.extend(_detect_undocumented_apis(store))
    findings.extend(_detect_unlinked_requirements(store))
    findings.extend(_detect_unlinked_implementations(store))
    findings.extend(_detect_stale_documents(store))
    findings.extend(_detect_unresolved_identities(store))
    findings.extend(_detect_broken_provenance(store))
    findings.extend(_detect_low_confidence(store))
    findings.extend(_detect_missing_tests(store))
    findings.extend(_detect_missing_architecture_mapping(store))
    findings.extend(_detect_unknown_production_owner(store))
    findings.extend(_detect_stale_runbooks(store))

    by_category: dict[str, int] = {}
    for f in findings:
        by_category[f.category] = by_category.get(f.category, 0) + 1

    by_dim = compute_debt_by_dimensions(findings)
    multi = compute_multidimensional_debt(findings)

    return {
        "findings": [f.to_dict() for f in findings],
        "total_debt": len(findings),
        "by_category": by_category,
        "by_dimension": by_dim,
        "multidimensional": multi,
        "categories_checked": len(DEBT_CATEGORIES),
    }


def _detect_unowned_services(store: GraphStore) -> list[DebtFinding]:
    findings: list[DebtFinding] = []
    for label in ("Service", "APIService"):
        vertices = store.find_vertices(label=label, limit=10_000)
        for v in vertices:
            edges = store.find_edges(out_v=v["vid"], limit=200)
            in_edges = store.find_edges(in_v=v["vid"], limit=200)
            has_owner = any(
                e["label"] == "ASSIGNED_TO" for e in edges
            ) or any(
                e["label"] in ("REALIZES", "TRACES_TO") for e in in_edges
            )
            if not has_owner:
                findings.append(DebtFinding(
                    category="unowned_component",
                    canonical_id=v["canonical_id"],
                    label=v["label"],
                    name=v["properties"].get("name", ""),
                    description=f"{label} has no owner assignment or business capability link",
                    evidence_ref=f"vertex:{v['canonical_id']}",
                    dimension=_extract_dimensions(v),
                ))
    return findings


def _detect_undocumented_apis(store: GraphStore) -> list[DebtFinding]:
    findings: list[DebtFinding] = []
    apis = store.find_vertices(label="APIEndpoint", limit=10_000)
    for api in apis:
        edges = store.find_edges(in_v=api["vid"], limit=200)
        has_doc = any(e["label"] in ("DOCUMENTS", "DOCUMENTS_API") for e in edges)
        if not has_doc:
            findings.append(DebtFinding(
                category="undocumented_api",
                canonical_id=api["canonical_id"],
                label="APIEndpoint",
                name=api["properties"].get("api_name", ""),
                description="API endpoint has no documentation link",
                evidence_ref=f"vertex:{api['canonical_id']}",
                dimension=_extract_dimensions(api),
            ))
    return findings


def _detect_unlinked_requirements(store: GraphStore) -> list[DebtFinding]:
    findings: list[DebtFinding] = []
    for label in ("Requirement", "UserStory", "Feature"):
        vertices = store.find_vertices(label=label, limit=10_000)
        for v in vertices:
            edges = store.find_edges(in_v=v["vid"], limit=200)
            has_impl = any(e["label"] in ("IMPLEMENTS", "TRACES_TO", "TESTS", "REFERENCES") for e in edges)
            if not has_impl:
                findings.append(DebtFinding(
                    category="unlinked_requirement",
                    canonical_id=v["canonical_id"],
                    label=v["label"],
                    name=v["properties"].get("name", ""),
                    description=f"{label} has no implementation or test link",
                    evidence_ref=f"vertex:{v['canonical_id']}",
                    dimension=_extract_dimensions(v),
                ))
    return findings


def _detect_unlinked_implementations(store: GraphStore) -> list[DebtFinding]:
    findings: list[DebtFinding] = []
    symbols = store.find_vertices(label="CodeSymbol", limit=10_000)
    for sym in symbols:
        edges = store.find_edges(out_v=sym["vid"], limit=200)
        in_edges = store.find_edges(in_v=sym["vid"], limit=200)
        if not edges and not in_edges:
            findings.append(DebtFinding(
                category="unlinked_implementation",
                canonical_id=sym["canonical_id"],
                label="CodeSymbol",
                name=sym["properties"].get("qualified_name") or sym["properties"].get("name", ""),
                description="CodeSymbol is isolated without file containment, caller, or requirement link",
                evidence_ref=f"vertex:{sym['canonical_id']}",
                dimension=_extract_dimensions(sym),
            ))
    return findings


def _detect_stale_documents(store: GraphStore) -> list[DebtFinding]:
    findings: list[DebtFinding] = []
    docs = store.find_vertices(label="Document", limit=10_000)
    for doc in docs:
        props = doc["properties"]
        if props.get("is_stale") is True or props.get("status") in ("stale", "deprecated", "obsolete"):
            findings.append(DebtFinding(
                category="stale_document",
                canonical_id=doc["canonical_id"],
                label="Document",
                name=props.get("title") or props.get("name", ""),
                description="Document is flagged as stale or deprecated",
                evidence_ref=f"vertex:{doc['canonical_id']}",
                dimension=_extract_dimensions(doc),
            ))
    return findings


def _detect_unresolved_identities(store: GraphStore) -> list[DebtFinding]:
    findings: list[DebtFinding] = []
    for label in ("Person", "User"):
        people = store.find_vertices(label=label, limit=10_000)
        for p in people:
            props = p["properties"]
            if props.get("is_resolved") is False or p["canonical_id"].startswith("urn:unresolved:"):
                findings.append(DebtFinding(
                    category="unresolved_identity",
                    canonical_id=p["canonical_id"],
                    label=label,
                    name=props.get("name") or props.get("username", ""),
                    description=f"{label} has unresolved canonical identity",
                    severity="WARNING",
                    evidence_ref=f"vertex:{p['canonical_id']}",
                    dimension=_extract_dimensions(p),
                ))
    return findings


def _detect_missing_tests(store: GraphStore) -> list[DebtFinding]:
    findings: list[DebtFinding] = []
    for label in ("APIEndpoint", "Service"):
        vertices = store.find_vertices(label=label, limit=10_000)
        for v in vertices:
            edges = store.find_edges(in_v=v["vid"], limit=200)
            has_test = any(e["label"] == "TESTS" for e in edges)
            if not has_test:
                findings.append(DebtFinding(
                    category="missing_test",
                    canonical_id=v["canonical_id"],
                    label=v["label"],
                    name=v["properties"].get("name") or v["properties"].get("api_name", ""),
                    description=f"{label} has no test coverage link",
                    evidence_ref=f"vertex:{v['canonical_id']}",
                    dimension=_extract_dimensions(v),
                ))
    return findings


def _detect_low_confidence(store: GraphStore) -> list[DebtFinding]:
    findings: list[DebtFinding] = []
    vertices = store.find_vertices(limit=50_000)
    for v in vertices:
        cs = v["properties"].get("creation_status")
        if cs in ("INFERRED", "AMBIGUOUS"):
            conf = v["properties"].get("confidence")
            if conf is not None and conf < 0.5:
                findings.append(DebtFinding(
                    category="low_confidence_inference",
                    canonical_id=v["canonical_id"],
                    label=v["label"],
                    name=v["properties"].get("name", ""),
                    description=f"Low confidence ({conf}) {cs} entity",
                    severity="ERROR",
                    evidence_ref=f"vertex:{v['canonical_id']}",
                    dimension=_extract_dimensions(v),
                ))
    return findings


def _detect_broken_provenance(store: GraphStore) -> list[DebtFinding]:
    findings: list[DebtFinding] = []
    business_labels = {l for l, (d, _, _) in VERTEX_LABELS.items() if d not in ("META", "IDENTITY")}
    vertices = store.find_vertices(limit=50_000)
    for v in vertices:
        if v["label"] not in business_labels:
            continue
        edges = store.find_edges(out_v=v["vid"], limit=200)
        has_evidence = any(e["label"] == "EVIDENCED_BY" for e in edges)
        if not has_evidence and v["properties"].get("ingestion_run_id"):
            findings.append(DebtFinding(
                category="broken_provenance",
                canonical_id=v["canonical_id"],
                label=v["label"],
                name=v["properties"].get("name", ""),
                description=f"{v['label']} has ingestion run but no evidence link",
                evidence_ref=f"vertex:{v['canonical_id']}",
                dimension=_extract_dimensions(v),
            ))
    return findings


def _detect_missing_architecture_mapping(store: GraphStore) -> list[DebtFinding]:
    findings: list[DebtFinding] = []
    for label in ("Service", "DesignComponent"):
        services = store.find_vertices(label=label, limit=10_000)
        for s in services:
            edges = store.find_edges(out_v=s["vid"], limit=200)
            in_edges = store.find_edges(in_v=s["vid"], limit=200)
            has_arch = any(e["label"] in ("PART_OF", "MEMBER_OF") for e in edges) or any(e["label"] in ("REALIZES", "IMPLEMENTS") for e in in_edges)
            if not has_arch:
                findings.append(DebtFinding(
                    category="missing_architecture_mapping",
                    canonical_id=s["canonical_id"],
                    label=label,
                    name=s["properties"].get("name", ""),
                    description=f"{label} has no architecture component or domain mapping",
                    evidence_ref=f"vertex:{s['canonical_id']}",
                    dimension=_extract_dimensions(s),
                ))
    return findings


def _detect_unknown_production_owner(store: GraphStore) -> list[DebtFinding]:
    findings: list[DebtFinding] = []
    for label in ("Deployment", "Service"):
        items = store.find_vertices(label=label, limit=10_000)
        for it in items:
            props = it["properties"]
            is_prod = props.get("environment") == "production"
            if is_prod:
                has_owner = bool(props.get("owner_email") or props.get("actor_id"))
                if not has_owner:
                    findings.append(DebtFinding(
                        category="unknown_production_owner",
                        canonical_id=it["canonical_id"],
                        label=label,
                        name=props.get("name") or it["canonical_id"],
                        description=f"Production {label} has no configured owner or oncall team",
                        severity="ERROR",
                        evidence_ref=f"vertex:{it['canonical_id']}",
                        dimension=_extract_dimensions(it),
                    ))
    return findings


def _detect_stale_runbooks(store: GraphStore) -> list[DebtFinding]:
    findings: list[DebtFinding] = []
    docs = store.find_vertices(label="Document", limit=10_000)
    for doc in docs:
        props = doc["properties"]
        if "runbook" in props.get("name", "").lower() or props.get("doc_format") == "runbook":
            if props.get("status") in ("stale", "deprecated", "obsolete"):
                findings.append(DebtFinding(
                    category="stale_runbook",
                    canonical_id=doc["canonical_id"],
                    label="Document",
                    name=props.get("name", ""),
                    description="Runbook has expired review date or is flagged stale",
                    severity="WARNING",
                    evidence_ref=f"vertex:{doc['canonical_id']}",
                    dimension=_extract_dimensions(doc),
                ))
    return findings


# --- Knowledge SLO Evaluator ---

@dataclass
class SLORule:
    id: str
    metric: str
    threshold: float
    operator: str = "gte"
    description: str = ""

    def to_dict(self) -> dict:
        return {"id": self.id, "metric": self.metric, "threshold": self.threshold, "operator": self.operator, "description": self.description}


def parse_slo_rules(config: list[dict]) -> list[SLORule]:
    """Parse SLO rules from configuration dicts."""
    return [SLORule(
        id=c["id"],
        metric=c["metric"],
        threshold=c["threshold"],
        operator=c.get("operator", "gte"),
        description=c.get("description", ""),
    ) for c in config]


def evaluate_slos(store: GraphStore, rules: list[SLORule]) -> dict:
    """Evaluate knowledge SLOs and return breach findings."""
    metrics = _compute_slo_metrics(store)
    results: list[dict] = []

    for rule in rules:
        actual = metrics.get(rule.metric)
        if actual is None:
            results.append({
                "rule": rule.to_dict(),
                "status": "UNKNOWN",
                "actual": None,
                "message": f"Metric {rule.metric} not available",
            })
            continue

        met = _check_threshold(actual, rule.threshold, rule.operator)
        results.append({
            "rule": rule.to_dict(),
            "status": "MET" if met else "BREACHED",
            "actual": actual,
            "message": f"{rule.metric}: {actual:.2f} {'meets' if met else 'breaches'} {rule.operator} {rule.threshold}",
        })

    breaches = [r for r in results if r["status"] == "BREACHED"]
    return {
        "results": results,
        "total_rules": len(rules),
        "met": len([r for r in results if r["status"] == "MET"]),
        "breached": len(breaches),
        "unknown": len([r for r in results if r["status"] == "UNKNOWN"]),
        "health_score": len([r for r in results if r["status"] == "MET"]) / max(len(rules), 1),
    }


def _compute_slo_metrics(store: GraphStore) -> dict[str, float]:
    """Compute all SLO-relevant metrics from the graph."""
    vertices = store.find_vertices(limit=50_000)
    edges = store.find_edges(limit=50_000)

    total_v = len(vertices)
    if total_v == 0:
        return {}

    business_labels = {l for l, (d, _, _) in VERTEX_LABELS.items() if d not in ("META",)}
    business_v = [v for v in vertices if v["label"] in business_labels]

    evidenced = 0
    for v in business_v:
        v_edges = [e for e in edges if e["out_v"] == v["vid"] and e["label"] == "EVIDENCED_BY"]
        if v_edges:
            evidenced += 1

    orphans = set()
    connected_vids = set()
    for e in edges:
        connected_vids.add(e["out_v"])
        connected_vids.add(e["in_v"])
    for v in vertices:
        meta_def = VERTEX_LABELS.get(v["label"])
        if meta_def and meta_def[0] == "META":
            continue
        if v["vid"] not in connected_vids:
            orphans.add(v["vid"])

    return {
        "evidence_coverage": evidenced / max(len(business_v), 1),
        "orphan_rate": len(orphans) / max(total_v, 1),
        "connectivity": len(connected_vids) / max(total_v, 1),
        "edge_density": len(edges) / max(total_v, 1),
        "business_entity_count": len(business_v),
    }


def _check_threshold(actual: float, threshold: float, operator: str) -> bool:
    if operator == "gte":
        return actual >= threshold
    elif operator == "lte":
        return actual <= threshold
    elif operator == "gt":
        return actual > threshold
    elif operator == "lt":
        return actual < threshold
    elif operator == "eq":
        return abs(actual - threshold) < 1e-9
    return False
