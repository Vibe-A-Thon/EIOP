"""KGR-G-019: Calibrated Uncertainty & Honest Abstain MCP Protocol.

Every MCP response includes: confidence_score, uncertainty_reason,
abstain flag, evidence_chain, and coverage_percent.  Implements
calibrated uncertainty estimation based on evidence coverage, staleness,
contradictions, and source reliability.
"""

from __future__ import annotations

import logging
import math
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

log = logging.getLogger("eoip.agents.uncertainty_protocol")


class UncertaintyReason(str, Enum):
    HIGH_CONFIDENCE = "HIGH_CONFIDENCE"
    PARTIAL_EVIDENCE = "PARTIAL_EVIDENCE"
    STALE_DATA = "STALE_DATA"
    CONTRADICTORY_SOURCES = "CONTRADICTORY_SOURCES"
    LOW_COVERAGE = "LOW_COVERAGE"
    INFERRED_NOT_ASSERTED = "INFERRED_NOT_ASSERTED"
    SINGLE_SOURCE = "SINGLE_SOURCE"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    AMBIGUOUS_QUERY = "AMBIGUOUS_QUERY"
    MODEL_UNCERTAINTY = "MODEL_UNCERTAINTY"


class ConfidenceTier(str, Enum):
    CERTAIN = "CERTAIN"          # >= 0.9
    CONFIDENT = "CONFIDENT"      # >= 0.7
    PROBABLE = "PROBABLE"        # >= 0.5
    UNCERTAIN = "UNCERTAIN"      # >= 0.3
    SPECULATIVE = "SPECULATIVE"  # >= 0.1
    ABSTAIN = "ABSTAIN"          # < 0.1


@dataclass(frozen=True)
class EvidenceLink:
    """A single piece of evidence supporting a claim."""
    source_id: str
    source_type: str  # graph_vertex, graph_edge, document, inference
    relevance_score: float
    freshness_days: float = 0.0
    is_contradictory: bool = False
    provenance: str = ""


@dataclass
class EvidenceChain:
    """The full chain of evidence backing an answer."""
    links: list[EvidenceLink]
    total_sources: int = 0
    contradictions: int = 0
    avg_freshness_days: float = 0.0
    coverage_percent: float = 0.0

    @property
    def has_contradictions(self) -> bool:
        return self.contradictions > 0

    @property
    def is_single_source(self) -> bool:
        return self.total_sources <= 1


@dataclass
class UncertaintyEnvelope:
    """The uncertainty metadata attached to every MCP response."""
    confidence_score: float
    confidence_tier: ConfidenceTier
    uncertainty_reasons: list[UncertaintyReason]
    abstain: bool
    evidence_chain: EvidenceChain
    coverage_percent: float
    staleness_indicator: str  # fresh, aging, stale, expired
    recommendation: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "confidence_score": round(self.confidence_score, 4),
            "confidence_tier": self.confidence_tier.value,
            "uncertainty_reasons": [r.value for r in self.uncertainty_reasons],
            "abstain": self.abstain,
            "evidence_chain": {
                "total_sources": self.evidence_chain.total_sources,
                "contradictions": self.evidence_chain.contradictions,
                "avg_freshness_days": round(self.evidence_chain.avg_freshness_days, 1),
                "coverage_percent": round(self.evidence_chain.coverage_percent, 1),
                "links": [
                    {
                        "source_id": link.source_id,
                        "source_type": link.source_type,
                        "relevance_score": round(link.relevance_score, 3),
                        "is_contradictory": link.is_contradictory,
                    }
                    for link in self.evidence_chain.links[:10]
                ],
            },
            "coverage_percent": round(self.coverage_percent, 1),
            "staleness_indicator": self.staleness_indicator,
            "recommendation": self.recommendation,
        }


class CoverageEstimator:
    """Estimates how much of the query scope is covered by available evidence."""

    def __init__(
        self,
        *,
        min_sources_for_full_coverage: int = 3,
        staleness_threshold_days: float = 30.0,
    ) -> None:
        self.min_sources = min_sources_for_full_coverage
        self.staleness_threshold = staleness_threshold_days

    def estimate(self, evidence: list[EvidenceLink], query_scope_size: int = 1) -> float:
        if not evidence:
            return 0.0

        relevant = [e for e in evidence if e.relevance_score > 0.3]
        if not relevant:
            return 5.0

        source_coverage = min(1.0, len(relevant) / max(self.min_sources, query_scope_size))
        freshness_penalty = self._freshness_penalty(relevant)
        contradiction_penalty = self._contradiction_penalty(relevant)

        coverage = source_coverage * 100.0 * (1 - freshness_penalty) * (1 - contradiction_penalty)
        return max(0.0, min(100.0, coverage))

    def _freshness_penalty(self, evidence: list[EvidenceLink]) -> float:
        if not evidence:
            return 0.0
        avg_age = sum(e.freshness_days for e in evidence) / len(evidence)
        if avg_age <= 7:
            return 0.0
        if avg_age <= self.staleness_threshold:
            return 0.1
        return min(0.5, avg_age / (self.staleness_threshold * 4))

    @staticmethod
    def _contradiction_penalty(evidence: list[EvidenceLink]) -> float:
        contradictions = sum(1 for e in evidence if e.is_contradictory)
        if contradictions == 0:
            return 0.0
        return min(0.5, contradictions / len(evidence))


class StalenessSensor:
    """Determines data staleness based on last-update timestamps."""

    def __init__(
        self,
        *,
        fresh_threshold_days: float = 7.0,
        aging_threshold_days: float = 30.0,
        stale_threshold_days: float = 90.0,
    ) -> None:
        self.fresh = fresh_threshold_days
        self.aging = aging_threshold_days
        self.stale = stale_threshold_days

    def classify(self, avg_freshness_days: float) -> str:
        if avg_freshness_days <= self.fresh:
            return "fresh"
        if avg_freshness_days <= self.aging:
            return "aging"
        if avg_freshness_days <= self.stale:
            return "stale"
        return "expired"

    def staleness_penalty(self, classification: str) -> float:
        return {
            "fresh": 0.0,
            "aging": 0.05,
            "stale": 0.15,
            "expired": 0.30,
        }.get(classification, 0.0)


class UncertaintySchemaEnforcer:
    """Computes calibrated uncertainty scores and enforces the abstain protocol."""

    def __init__(
        self,
        *,
        abstain_threshold: float = 0.15,
        coverage_estimator: CoverageEstimator | None = None,
        staleness_sensor: StalenessSensor | None = None,
    ) -> None:
        self.abstain_threshold = abstain_threshold
        self._coverage = coverage_estimator or CoverageEstimator()
        self._staleness = staleness_sensor or StalenessSensor()

    def evaluate(
        self,
        evidence: list[EvidenceLink],
        *,
        query_scope_size: int = 1,
        model_confidence: float | None = None,
    ) -> UncertaintyEnvelope:
        chain = self._build_chain(evidence)
        coverage = self._coverage.estimate(evidence, query_scope_size)
        staleness = self._staleness.classify(chain.avg_freshness_days)
        reasons = self._identify_reasons(chain, coverage, staleness, model_confidence)
        confidence = self._compute_confidence(chain, coverage, staleness, model_confidence, reasons)
        tier = self._classify_tier(confidence)
        should_abstain = confidence < self.abstain_threshold

        return UncertaintyEnvelope(
            confidence_score=confidence,
            confidence_tier=tier,
            uncertainty_reasons=reasons,
            abstain=should_abstain,
            evidence_chain=chain,
            coverage_percent=coverage,
            staleness_indicator=staleness,
            recommendation=self._recommend(tier, reasons, should_abstain),
        )

    def wrap_mcp_response(self, result: Any, envelope: UncertaintyEnvelope) -> dict[str, Any]:
        """Wrap any MCP tool result with the uncertainty envelope."""
        return {
            "result": result,
            "uncertainty": envelope.to_dict(),
        }

    def _build_chain(self, evidence: list[EvidenceLink]) -> EvidenceChain:
        if not evidence:
            return EvidenceChain(links=[], total_sources=0)

        unique_sources = set(e.source_id for e in evidence)
        contradictions = sum(1 for e in evidence if e.is_contradictory)
        avg_freshness = sum(e.freshness_days for e in evidence) / len(evidence)

        return EvidenceChain(
            links=evidence,
            total_sources=len(unique_sources),
            contradictions=contradictions,
            avg_freshness_days=avg_freshness,
        )

    def _identify_reasons(
        self,
        chain: EvidenceChain,
        coverage: float,
        staleness: str,
        model_confidence: float | None,
    ) -> list[UncertaintyReason]:
        reasons: list[UncertaintyReason] = []

        if not chain.links:
            reasons.append(UncertaintyReason.OUT_OF_SCOPE)
            return reasons

        if chain.has_contradictions:
            reasons.append(UncertaintyReason.CONTRADICTORY_SOURCES)
        if chain.is_single_source:
            reasons.append(UncertaintyReason.SINGLE_SOURCE)
        if coverage < 50.0:
            reasons.append(UncertaintyReason.LOW_COVERAGE)
        if coverage >= 50.0 and coverage < 80.0:
            reasons.append(UncertaintyReason.PARTIAL_EVIDENCE)
        if staleness in ("stale", "expired"):
            reasons.append(UncertaintyReason.STALE_DATA)

        inferred = sum(1 for e in chain.links if e.source_type == "inference")
        if inferred > len(chain.links) * 0.5:
            reasons.append(UncertaintyReason.INFERRED_NOT_ASSERTED)

        if model_confidence is not None and model_confidence < 0.5:
            reasons.append(UncertaintyReason.MODEL_UNCERTAINTY)

        if not reasons:
            reasons.append(UncertaintyReason.HIGH_CONFIDENCE)

        return reasons

    def _compute_confidence(
        self,
        chain: EvidenceChain,
        coverage: float,
        staleness: str,
        model_confidence: float | None,
        reasons: list[UncertaintyReason],
    ) -> float:
        if not chain.links:
            return 0.0

        base = coverage / 100.0

        relevance_factor = sum(e.relevance_score for e in chain.links) / len(chain.links)
        base *= relevance_factor

        staleness_pen = self._staleness.staleness_penalty(staleness)
        base -= staleness_pen

        if chain.has_contradictions:
            contradiction_ratio = chain.contradictions / max(len(chain.links), 1)
            base -= contradiction_ratio * 0.3

        if chain.is_single_source:
            base *= 0.7

        if model_confidence is not None:
            base = base * 0.6 + model_confidence * 0.4

        return max(0.0, min(1.0, base))

    @staticmethod
    def _classify_tier(score: float) -> ConfidenceTier:
        if score >= 0.9:
            return ConfidenceTier.CERTAIN
        if score >= 0.7:
            return ConfidenceTier.CONFIDENT
        if score >= 0.5:
            return ConfidenceTier.PROBABLE
        if score >= 0.3:
            return ConfidenceTier.UNCERTAIN
        if score >= 0.1:
            return ConfidenceTier.SPECULATIVE
        return ConfidenceTier.ABSTAIN

    @staticmethod
    def _recommend(tier: ConfidenceTier, reasons: list[UncertaintyReason], abstain: bool) -> str:
        if abstain:
            return "Insufficient evidence to provide a reliable answer. Recommend manual investigation."
        if tier == ConfidenceTier.CERTAIN:
            return "High confidence answer backed by multiple corroborating sources."
        if tier in (ConfidenceTier.CONFIDENT, ConfidenceTier.PROBABLE):
            reason_strs = [r.value.lower().replace("_", " ") for r in reasons if r != UncertaintyReason.HIGH_CONFIDENCE]
            if reason_strs:
                return f"Moderate confidence. Caveats: {', '.join(reason_strs[:3])}."
            return "Moderate confidence answer."
        return "Low confidence answer. Verify independently before acting."
