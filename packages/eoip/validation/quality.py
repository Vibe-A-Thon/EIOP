"""Graph quality metrics (FR-VALID-002, FR-VALID-003).

Coverage-style metrics return None (N/A) when their denominator is empty —
never a false 0/100% (FR-VALID-003).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from eoip.ontology.manifest import EDGE_LABELS, VERTEX_LABELS, edge_endpoints_valid

FRESHNESS_WINDOW = timedelta(days=30)


@dataclass(frozen=True)
class QualityMetrics:
    total_vertices: int
    total_edges: int
    total_findings: int
    error_count: int
    warning_count: int
    evidence_coverage: float | None
    provenance_coverage: float | None
    orphan_rate: float | None
    duplicate_rate: float | None
    freshness: float | None
    completeness: float | None
    schema_compliance: float | None

    @classmethod
    def compute(
        cls,
        vertices: list[dict],
        edges: list[dict],
        findings: list[dict],
        *,
        now: datetime | None = None,
    ) -> QualityMetrics:
        now = now or datetime.now(UTC)

        evidence_required = {"IMPLEMENTS", "REFERENCES", "DOCUMENTS", "MODIFIES", "DECLARES"}
        requiring = [e for e in edges if e["label"] in evidence_required]
        covered = sum(1 for e in requiring if e["properties"].get("evidence_key"))
        evidence_cov = covered / len(requiring) if requiring else None

        meta_labels = {"IngestionRun", "GraphDomain", "OntologyVersion", "ValidationRun", "ValidationFinding", "DataSource", "Evidence"}
        business = [v for v in vertices if v["label"] not in meta_labels]
        with_provenance = sum(1 for v in business if v["properties"].get("ingestion_run_id"))
        prov_cov = with_provenance / len(business) if business else None

        total_vertices = len(vertices)
        referenced_vids = {vid for e in edges for vid in (e["out_v"], e["in_v"])}
        orphan_rate = (
            sum(1 for v in vertices if v["vid"] not in referenced_vids) / total_vertices
            if total_vertices
            else None
        )

        canonical_counts = Counter(v.get("canonical_id") for v in vertices)
        duplicate_rate = (
            sum(count - 1 for count in canonical_counts.values() if count > 1) / total_vertices
            if total_vertices
            else None
        )

        last_seen_values = [v["properties"].get("last_seen") for v in vertices]
        last_seen_values = [value for value in last_seen_values if value]
        seen_recently = sum(1 for value in last_seen_values if _within_window(value, now))
        freshness = seen_recently / len(last_seen_values) if last_seen_values else None

        known_vertices = [v for v in vertices if v["label"] in VERTEX_LABELS]
        complete = sum(
            1
            for v in known_vertices
            if all(v["properties"].get(key) is not None for key in VERTEX_LABELS[v["label"]][1])
        )
        completeness = complete / len(known_vertices) if known_vertices else None

        labels_by_vid = {v["vid"]: v["label"] for v in vertices}
        checkable_edges = [
            e
            for e in edges
            if e["out_v"] in labels_by_vid and e["in_v"] in labels_by_vid
        ]
        conformant = sum(
            1
            for e in checkable_edges
            if e["label"] in EDGE_LABELS
            and edge_endpoints_valid(e["label"], labels_by_vid[e["out_v"]], labels_by_vid[e["in_v"]])
        )
        schema_compliance = conformant / len(checkable_edges) if checkable_edges else None

        return cls(
            total_vertices=total_vertices,
            total_edges=len(edges),
            total_findings=len(findings),
            error_count=sum(1 for f in findings if f.get("severity") == "ERROR"),
            warning_count=sum(1 for f in findings if f.get("severity") == "WARNING"),
            evidence_coverage=None if evidence_cov is None else round(evidence_cov, 4),
            provenance_coverage=None if prov_cov is None else round(prov_cov, 4),
            orphan_rate=None if orphan_rate is None else round(orphan_rate, 4),
            duplicate_rate=None if duplicate_rate is None else round(duplicate_rate, 4),
            freshness=None if freshness is None else round(freshness, 4),
            completeness=None if completeness is None else round(completeness, 4),
            schema_compliance=None if schema_compliance is None else round(schema_compliance, 4),
        )

    def as_dict(self) -> dict:
        return {
            "total_vertices": self.total_vertices,
            "total_edges": self.total_edges,
            "total_findings": self.total_findings,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "evidence_coverage": self.evidence_coverage,
            "provenance_coverage": self.provenance_coverage,
            "orphan_rate": self.orphan_rate,
            "duplicate_rate": self.duplicate_rate,
            "freshness": self.freshness,
            "completeness": self.completeness,
            "schema_compliance": self.schema_compliance,
        }


def _within_window(value: str, now: datetime) -> bool:
    try:
        seen = datetime.fromisoformat(str(value))
    except ValueError:
        return False
    if seen.tzinfo is None:
        seen = seen.replace(tzinfo=UTC)
    return now - FRESHNESS_WINDOW <= seen <= now + FRESHNESS_WINDOW
