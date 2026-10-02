"""Graph quality metrics (FR-VALID-002)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QualityMetrics:
    total_vertices: int
    total_edges: int
    total_findings: int
    error_count: int
    warning_count: int
    evidence_coverage: float
    provenance_coverage: float

    @classmethod
    def compute(cls, vertices: list[dict], edges: list[dict], findings: list[dict]) -> QualityMetrics:
        evidence_required = {"IMPLEMENTS", "REFERENCES", "DOCUMENTS", "MODIFIES", "DECLARES"}
        requiring = [e for e in edges if e["label"] in evidence_required]
        covered = sum(1 for e in requiring if e["properties"].get("evidence_key"))
        evidence_cov = covered / len(requiring) if requiring else 1.0

        meta_labels = {"IngestionRun", "GraphDomain", "OntologyVersion", "ValidationRun", "ValidationFinding", "DataSource", "Evidence"}
        business = [v for v in vertices if v["label"] not in meta_labels]
        with_provenance = sum(1 for v in business if v["properties"].get("ingestion_run_id"))
        prov_cov = with_provenance / len(business) if business else 1.0

        return cls(
            total_vertices=len(vertices),
            total_edges=len(edges),
            total_findings=len(findings),
            error_count=sum(1 for f in findings if f.get("severity") == "ERROR"),
            warning_count=sum(1 for f in findings if f.get("severity") == "WARNING"),
            evidence_coverage=round(evidence_cov, 4),
            provenance_coverage=round(prov_cov, 4),
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
        }
