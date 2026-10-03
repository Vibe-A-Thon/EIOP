"""Digital twin view service (G2-T0630..0632, G2-TWIN-001..005).

Meta-query classification (intended/implemented/observed/inferred),
digital-thread coverage metrics, and missing-link detection.
"""

from __future__ import annotations

from eoip.graph.store import GraphStore

FACT_CLASSES = {
    "intended": {
        "labels": {"BusinessObjective", "BusinessCapability", "Requirement", "Epic", "Feature", "UserStory", "Decision", "Alternative", "ProcessFlow", "ProcessStep"},
        "description": "Facts representing planned/desired state",
    },
    "implemented": {
        "labels": {"File", "CodeSymbol", "Service", "APIService", "APIEndpoint", "Commit", "MergeRequest", "Repository", "Branch", "Tag", "Document", "DocumentSection", "Dependency"},
        "description": "Facts representing built/delivered artifacts",
    },
    "observed": {
        "labels": {"PipelineRun", "Job", "Deployment", "TestRun", "Incident", "AlertEvent", "Dashboard", "MonitorRule", "Metric", "LogAggregate", "ProcessEvent", "BuildRecord"},
        "description": "Facts representing runtime observations",
    },
    "inferred": {
        "labels": set(),
        "description": "Facts derived by AI/analysis (creation_status=INFERRED or AMBIGUOUS)",
    },
}

THREAD_CHAIN = [
    "BusinessObjective", "BusinessCapability", "Requirement",
    "Decision", "WorkItem", "Epic", "Feature", "UserStory",
    "File", "CodeSymbol", "APIService", "APIEndpoint", "Service",
    "TestCase", "TestRun", "PipelineRun", "BuildRecord",
    "Deployment", "Incident",
]


def classify_facts(store: GraphStore) -> dict:
    """Classify all vertices into intended/implemented/observed/inferred categories."""
    vertices = store.find_vertices(limit=50_000)
    classified: dict[str, list[dict]] = {
        "intended": [],
        "implemented": [],
        "observed": [],
        "inferred": [],
    }
    summary: dict[str, int] = {"intended": 0, "implemented": 0, "observed": 0, "inferred": 0}

    for v in vertices:
        label = v["label"]
        cs = v["properties"].get("creation_status", "")

        if cs in ("INFERRED", "AMBIGUOUS"):
            category = "inferred"
        elif label in FACT_CLASSES["intended"]["labels"]:
            category = "intended"
        elif label in FACT_CLASSES["observed"]["labels"]:
            category = "observed"
        elif label in FACT_CLASSES["implemented"]["labels"]:
            category = "implemented"
        else:
            category = "implemented"

        classified[category].append({
            "canonical_id": v["canonical_id"],
            "label": label,
            "name": v["properties"].get("name", ""),
        })
        summary[category] += 1

    return {
        "classification": {k: v[:100] for k, v in classified.items()},
        "summary": summary,
        "total": sum(summary.values()),
    }


def digital_thread_coverage(store: GraphStore) -> dict:
    """Compute coverage metrics across the intent-to-runtime digital thread.

    Measures what percentage of each thread stage has connections to adjacent stages.
    """
    coverage: dict[str, dict] = {}

    for label in THREAD_CHAIN:
        vertices = store.find_vertices(label=label, limit=10_000)
        total = len(vertices)
        connected = 0

        for v in vertices:
            out_edges = store.find_edges(out_v=v["vid"], limit=100)
            in_edges = store.find_edges(in_v=v["vid"], limit=100)
            if out_edges or in_edges:
                connected += 1

        coverage[label] = {
            "total": total,
            "connected": connected,
            "coverage": connected / total if total > 0 else None,
        }

    present_stages = [l for l in THREAD_CHAIN if coverage[l]["total"] > 0]
    thread_completeness = len(present_stages) / len(THREAD_CHAIN) if THREAD_CHAIN else 0

    return {
        "per_stage": coverage,
        "stages_present": present_stages,
        "stages_missing": [l for l in THREAD_CHAIN if coverage[l]["total"] == 0],
        "thread_completeness": thread_completeness,
    }


def detect_missing_links(store: GraphStore) -> dict:
    """Detect entities missing expected relationships in the digital thread.

    For each thread stage, checks if entities lack connections to adjacent stages.
    """
    findings: list[dict] = []

    expected_connections: dict[str, list[str]] = {
        "BusinessObjective": ["BusinessCapability"],
        "BusinessCapability": ["BusinessObjective", "Service", "Project"],
        "Requirement": ["WorkItem", "TestCase"],
        "Decision": ["File", "CodeSymbol", "Service"],
        "WorkItem": ["Commit", "MergeRequest", "TestCase"],
        "File": ["CodeSymbol", "TestCase"],
        "CodeSymbol": ["TestCase"],
        "Service": ["Deployment", "MonitorRule", "Dashboard"],
        "APIService": ["APIEndpoint", "TestCase"],
        "Deployment": ["PipelineRun"],
        "TestCase": ["TestRun"],
    }

    for source_label, target_labels in expected_connections.items():
        vertices = store.find_vertices(label=source_label, limit=10_000)
        for v in vertices:
            out_edges = store.find_edges(out_v=v["vid"], limit=500)
            in_edges = store.find_edges(in_v=v["vid"], limit=500)
            all_edges = out_edges + in_edges

            connected_labels: set[str] = set()
            for edge in all_edges:
                peer_vid = edge["in_v"] if edge["out_v"] == v["vid"] else edge["out_v"]
                peer = store.get_vertex(peer_vid)
                if peer:
                    connected_labels.add(peer["label"])

            missing = [t for t in target_labels if t not in connected_labels]
            if missing:
                findings.append({
                    "canonical_id": v["canonical_id"],
                    "label": source_label,
                    "name": v["properties"].get("name", ""),
                    "missing_connections": missing,
                    "severity": "WARNING",
                })

    critical = [f for f in findings if f["label"] in ("BusinessObjective", "Service", "Deployment")]
    return {
        "findings": findings,
        "total_gaps": len(findings),
        "critical_gaps": len(critical),
        "by_label": {
            label: len([f for f in findings if f["label"] == label])
            for label in expected_connections
            if any(f["label"] == label for f in findings)
        },
    }
