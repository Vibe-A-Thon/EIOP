"""Executable G2 observability contract.

Implements G2-OBS-001..006 as a structured contract for source traces,
per-source metrics, graph-evolution metrics, event-bus lag, graph publication
time and knowledge-SLO latency.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RequiredMetric:
    requirement_id: str
    path: str
    description: str

    def to_dict(self) -> dict[str, str]:
        return {
            "requirement_id": self.requirement_id,
            "path": self.path,
            "description": self.description,
        }


REQUIRED_G2_OBSERVABILITY_METRICS: tuple[RequiredMetric, ...] = (
    RequiredMetric("G2-OBS-001", "source_trace.fetch_to_source_event_to_mapping_to_mutation", "Trace source fetch through SourceEvent, mapping and graph mutation."),
    RequiredMetric("G2-OBS-002", "per_source.fetch_latency_seconds", "Per-source fetch latency."),
    RequiredMetric("G2-OBS-002", "per_source.records_per_second", "Per-source accepted/rejected record throughput."),
    RequiredMetric("G2-OBS-002", "per_source.errors_total", "Per-source error count."),
    RequiredMetric("G2-OBS-002", "per_source.lag_seconds", "Per-source synchronization lag."),
    RequiredMetric("G2-OBS-002", "per_source.retries_total", "Per-source retry count."),
    RequiredMetric("G2-OBS-002", "per_source.dlq_count", "Per-source dead-letter count."),
    RequiredMetric("G2-OBS-003", "graph_evolution.added_facts", "Graph evolution added-fact count."),
    RequiredMetric("G2-OBS-003", "graph_evolution.changed_facts", "Graph evolution changed-fact count."),
    RequiredMetric("G2-OBS-003", "graph_evolution.expired_facts", "Graph evolution expired-fact count."),
    RequiredMetric("G2-OBS-003", "graph_evolution.mutation_latency_seconds", "Graph mutation latency."),
    RequiredMetric("G2-OBS-003", "graph_evolution.validation_failures", "Graph validation failure count."),
    RequiredMetric("G2-OBS-004", "event_bus.consumer_lag", "Semantic event bus consumer lag by consumer."),
    RequiredMetric("G2-OBS-005", "graph_version.publication_time", "Graph version publication timestamp or duration."),
    RequiredMetric("G2-OBS-006", "knowledge_slo.evaluation_latency_seconds", "Knowledge SLO evaluation latency."),
)


def g2_observability_contract() -> dict[str, Any]:
    by_requirement: dict[str, list[dict[str, str]]] = {}
    for metric in REQUIRED_G2_OBSERVABILITY_METRICS:
        by_requirement.setdefault(metric.requirement_id, []).append(metric.to_dict())
    return {
        "requirements": sorted(by_requirement),
        "metrics": [metric.to_dict() for metric in REQUIRED_G2_OBSERVABILITY_METRICS],
        "by_requirement": by_requirement,
    }


def validate_g2_observability_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Validate a concrete observability snapshot against G2-OBS-001..006."""
    results = []
    for metric in REQUIRED_G2_OBSERVABILITY_METRICS:
        present = _has_path(snapshot, metric.path)
        results.append({
            "requirement_id": metric.requirement_id,
            "path": metric.path,
            "passed": present,
            "description": metric.description,
        })
    passed = sum(1 for item in results if item["passed"])
    return {
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "conformant": passed == len(results),
        "results": results,
    }


def _has_path(document: dict[str, Any], dotted_path: str) -> bool:
    current: Any = document
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return False
        current = current[part]
    return current is not None


def link_runtime_evidence(
    store: Any,
    target_cid: str,
    evidence_cid: str,
    *,
    window_start: str,
    window_end: str,
    source_ref: str = "",
) -> dict[str, Any]:
    """Links runtime evidence to Deployments, Incidents or Services with a bounded observation window (G2-GRAPH-OBS-002, 003)."""
    target = store.get_vertex_by_canonical_id(target_cid)
    if not target:
        raise ValueError(f"Target entity not found: {target_cid}")
    if target["label"] not in ("Deployment", "Incident", "Service", "APIService"):
        raise ValueError(f"Target must be Deployment, Incident, or Service, got {target['label']}")

    ev = store.get_vertex_by_canonical_id(evidence_cid)
    if not ev:
        raise ValueError(f"Evidence vertex not found: {evidence_cid}")

    fact_key = f"runtime_ev:{target_cid}:{evidence_cid}:{window_start}_{window_end}"
    edge = store.upsert_edge(
        "EVIDENCED_BY",
        target["vid"],
        ev["vid"],
        {
            "fact_key": fact_key,
            "observed_at": window_start,
            "source_ref": source_ref or f"window:{window_start}..{window_end}",
            "creation_status": "DETERMINISTIC",
        },
    )
    return {
        "edge_id": edge["eid"],
        "target": target_cid,
        "evidence": evidence_cid,
        "window_start": window_start,
        "window_end": window_end,
        "bounded_window": True,
    }
