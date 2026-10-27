"""Continuous Graph Health Intelligence Dashboard (MS-24).

Research basis: Data observability best practices (dbt, Monte Carlo),
EOIP 28-graph-quality.md specification.

Provides:
- 5-Dimension Graph Health Score (0–100):
  1. Freshness: recency of entity updates
  2. Coverage: presence of expected ontology types
  3. Consistency: absence of contradiction/cycle errors
  4. Completeness: presence of mandatory fields
  5. Accuracy: valid provenance and verification receipts
- Autonomous remediation triggers: orphan GC, index rebalancing, compaction recommendations.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from eoip.graph.store import GraphStore


@dataclass
class HealthDimensionScore:
    dimension: str
    score: float  # 0.0 - 100.0
    weight: float
    details: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "dimension": self.dimension,
            "score": round(self.score, 2),
            "weight": self.weight,
            "details": self.details,
        }


class ContinuousGraphHealthDashboard:
    """Computes continuous 5-dimension health scores and autonomous maintenance proposals."""

    def __init__(self, store: GraphStore) -> None:
        self.store = store

    def compute_health_metrics(self) -> dict[str, Any]:
        vertices = self.store.find_vertices(limit=5000)
        self.store.find_edges(limit=10000)
        total_v = max(len(vertices), 1)

        # 1. Freshness (entities updated within 90 days)
        now = time.time()
        recent = sum(1 for v in vertices if (now - float(v.get("properties", {}).get("updated_at_ts", now))) < 90 * 86400)
        freshness_pct = (recent / total_v) * 100.0
        d_fresh = HealthDimensionScore("Freshness", freshness_pct, 0.20, f"{recent}/{total_v} vertices refreshed recently")

        # 2. Coverage (fraction of expected core entity types present)
        core_types = {"Service", "APIService", "File", "CodeSymbol", "Document", "Requirement"}
        present_types = {v.get("label") for v in vertices}
        cov_pct = (len(core_types.intersection(present_types)) / len(core_types)) * 100.0
        d_cov = HealthDimensionScore("Coverage", cov_pct, 0.20, f"{len(core_types.intersection(present_types))}/{len(core_types)} core types present")

        # 3. Consistency (absence of orphaned vertices)
        orphans = 0
        for v in vertices:
            vid = v["vid"]
            out_e = self.store.find_edges(out_v=vid, limit=1)
            in_e = self.store.find_edges(in_v=vid, limit=1)
            if not out_e and not in_e:
                orphans += 1
        consistency_pct = max(0.0, 100.0 - (orphans / total_v) * 100.0)
        d_const = HealthDimensionScore("Consistency", consistency_pct, 0.25, f"{orphans} orphan nodes detected")

        # 4. Completeness (fraction with canonical_id and properties)
        complete = sum(1 for v in vertices if v.get("canonical_id") and v.get("properties"))
        comp_pct = (complete / total_v) * 100.0
        d_comp = HealthDimensionScore("Completeness", comp_pct, 0.15, f"{complete}/{total_v} entities contain mandatory schema properties")

        # 5. Accuracy (fraction with provenance evidence reference)
        with_prov = sum(1 for v in vertices if v.get("properties", {}).get("evidence_ref") != "NULL_RECEIPT")
        acc_pct = (with_prov / total_v) * 100.0
        d_acc = HealthDimensionScore("Accuracy", acc_pct, 0.20, f"{with_prov}/{total_v} entities possess valid provenance receipts")

        dimensions = [d_fresh, d_cov, d_const, d_comp, d_acc]
        overall_score = sum(d.score * d.weight for d in dimensions)

        # Autonomous maintenance recommendations
        maintenance_actions = []
        if orphans > 0:
            maintenance_actions.append({
                "action": "ORPHAN_GARBAGE_COLLECTION",
                "target_count": orphans,
                "priority": "HIGH",
                "rationale": "Prune disconnected vertices or attach to synthetic placeholder module",
            })
        if overall_score > 85.0:
            maintenance_actions.append({
                "action": "STORAGE_COMPACTION_SCHEDULED",
                "priority": "LOW",
                "rationale": "Compact indexes and prune dead tombstones",
            })

        return {
            "overall_health_score": round(overall_score, 2),
            "health_grade": "A" if overall_score >= 90 else ("B" if overall_score >= 80 else "C"),
            "dimensions": [d.to_dict() for d in dimensions],
            "autonomous_maintenance_actions": maintenance_actions,
            "computed_at": time.time(),
        }
