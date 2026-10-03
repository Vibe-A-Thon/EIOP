"""Knowledge debt catalog and SLO evaluator (G2-KD-001..006, G2-SLO-001..005).

Detects knowledge debt (unowned components, undocumented APIs, stale docs,
missing tests, broken provenance) and evaluates knowledge health SLOs.
"""

from __future__ import annotations

from dataclasses import dataclass

from eoip.graph.store import GraphStore
from eoip.ontology.manifest import VERTEX_LABELS


@dataclass
class DebtFinding:
    category: str
    canonical_id: str
    label: str
    name: str
    description: str
    severity: str = "WARNING"

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "canonical_id": self.canonical_id,
            "label": self.label,
            "name": self.name,
            "description": self.description,
            "severity": self.severity,
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


def detect_knowledge_debt(store: GraphStore) -> dict:
    """Run all knowledge debt detection rules against the graph."""
    findings: list[DebtFinding] = []

    findings.extend(_detect_unowned_services(store))
    findings.extend(_detect_undocumented_apis(store))
    findings.extend(_detect_unlinked_requirements(store))
    findings.extend(_detect_missing_tests(store))
    findings.extend(_detect_low_confidence(store))
    findings.extend(_detect_broken_provenance(store))

    by_category: dict[str, int] = {}
    for f in findings:
        by_category[f.category] = by_category.get(f.category, 0) + 1

    return {
        "findings": [f.to_dict() for f in findings],
        "total_debt": len(findings),
        "by_category": by_category,
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
                    name=v["properties"].get("name", ""),
                    description=f"{label} has no test coverage link",
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
