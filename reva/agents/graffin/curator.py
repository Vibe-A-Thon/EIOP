"""
Graffin Knowledge Curation & Contradiction Quarantine Engine (GRF-CUR-*, T-GRF-011..013).
Hunts for structural knowledge gaps, quarantines conflicting claims, and synthesizes probe queries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence

from reva.core.ids import contradiction_id, gap_id


@dataclass
class KnowledgeGapItem:
    gap_id: str
    target_entity: str
    question: str
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"


@dataclass
class QuarantinedContradiction:
    contradiction_id: str
    conflict_key: str
    conflicting_warrants: List[str]
    is_active: bool = True


class GraffinCurator:
    """
    Scans the Knowledge and Wisdom graphs for incompleteness and logical contradictions.
    """

    def __init__(self, tenant_id: str = "default") -> None:
        self.tenant_id = tenant_id
        self._quarantined: Dict[str, QuarantinedContradiction] = {}

    def scan_for_gaps(self, graph_dict: Dict[str, Any]) -> List[KnowledgeGapItem]:
        """
        Scans graph vertices for missing metadata, documentation gaps, or unlinked endpoints.
        """
        gaps: List[KnowledgeGapItem] = []
        for v in graph_dict.get("vertices", []):
            props = v.get("properties", {})
            v_id = v.get("id", "")
            kind = v.get("kind", "")

            # Gap check 1: Class or Function with missing docstrings in critical components
            if kind in ("kg_Class", "kg_Function") and not props.get("docstring"):
                if "auth" in v_id or "crypto" in v_id or "security" in v_id:
                    q = f"Missing API documentation or security contract for critical component: {v_id}"
                    g_id = gap_id(self.tenant_id, "documentation", q, {"entity_id": v_id})
                    gaps.append(KnowledgeGapItem(
                        gap_id=g_id,
                        target_entity=v_id,
                        question=q,
                        severity="MEDIUM",
                    ))

            # Gap check 2: Endpoints without documented handler
            if kind == "kg_Endpoint" and not props.get("handler_id"):
                q = f"Orphaned API endpoint with no identified controller handler: {v_id}"
                g_id = gap_id(self.tenant_id, "architecture", q, {"entity_id": v_id})
                gaps.append(KnowledgeGapItem(
                    gap_id=g_id,
                    target_entity=v_id,
                    question=q,
                    severity="HIGH",
                ))

        return gaps

    def quarantine_contradiction(
        self,
        conflict_key: str,
        conflicting_warrant_ids: Sequence[str],
    ) -> QuarantinedContradiction:
        """
        Isolates mutually contradictory claims until human or evidence resolution occurs.
        """
        c_id = contradiction_id(
            tenant_id=self.tenant_id,
            conflict_key=conflict_key,
            member_warrant_ids=conflicting_warrant_ids,
        )
        item = QuarantinedContradiction(
            contradiction_id=c_id,
            conflict_key=conflict_key,
            conflicting_warrants=sorted(list(set(conflicting_warrant_ids))),
            is_active=True,
        )
        self._quarantined[c_id] = item
        return item
