"""Counsel synthesis service for Wisdom Graph (WG-WP-15..17)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional
from eoip.wisdom.decision_trace import DecisionTrace
from eoip.wisdom.precedent_engine import PrecedentEngine, PrecedentMatch
from eoip.wisdom.outcome_tracker import OutcomeTracker


@dataclass
class WisdomCounselReport:
    situation_query: str
    recommended_strategy: str
    confidence_score: float
    relevant_precedents: List[PrecedentMatch]
    risk_warnings: List[str]
    suggested_mitigations: List[str]


class CounselService:
    """Synthesizes actionable wisdom recommendations from historical precedents and outcomes."""

    def __init__(self, precedent_engine: PrecedentEngine, outcome_tracker: Optional[OutcomeTracker] = None) -> None:
        self.precedents = precedent_engine
        self.outcomes = outcome_tracker or OutcomeTracker()

    def generate_counsel(
        self,
        situation: str,
        context_tags: Optional[List[str]] = None,
        tenant_id: str = "acme-demo",
    ) -> WisdomCounselReport:
        matches = self.precedents.find_precedents(
            query_situation=situation,
            context_tags=context_tags,
            tenant_id=tenant_id,
            min_similarity=0.2,
            limit=3,
        )

        risk_warnings = []
        mitigations = []

        if not matches:
            return WisdomCounselReport(
                situation_query=situation,
                recommended_strategy="Novel decision situation with no close historical precedent. Recommend small-scale pilot and dual-control approval.",
                confidence_score=0.4,
                relevant_precedents=[],
                risk_warnings=["No historical precedent matches detected."],
                suggested_mitigations=["Require multi-stakeholder review and explicit rollback checkpoint."],
            )

        # Check outcomes from matched precedents
        top_match = matches[0]
        top_trace = top_match.trace

        has_negative_outcomes = False
        for out in top_trace.outcomes:
            for metric, diff in out.variance_analysis.items():
                if diff < -0.2:
                    has_negative_outcomes = True
                    risk_warnings.append(
                        f"Precedent '{top_trace.trace_id}' experienced unexpected underperformance in '{metric}': {diff}"
                    )
                    mitigations.append(f"Lessons learned from {top_trace.trace_id}: {out.lessons_learned}")

        if has_negative_outcomes:
            strategy = (
                f"Historical precedent '{top_trace.title}' was attempted but incurred variance. "
                "Recommend applying contingency mitigations before proceeding."
            )
            confidence = min(0.85, top_match.similarity_score * 0.9)
        else:
            strategy = (
                f"Adopt validated approach from precedent '{top_trace.title}' ({top_trace.selected_option_id}): "
                f"{top_trace.rationale}"
            )
            confidence = min(0.95, top_match.similarity_score)

        return WisdomCounselReport(
            situation_query=situation,
            recommended_strategy=strategy,
            confidence_score=round(confidence, 2),
            relevant_precedents=matches,
            risk_warnings=risk_warnings,
            suggested_mitigations=mitigations or ["Monitor leading outcome indicators weekly."],
        )
