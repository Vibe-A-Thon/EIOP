"""
Semantic Binary Change Impact Classifier (REVA-BD-004, T-ENH-035).
Classifies changes between binary functions into semantic impact tiers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DiffImpactReport:
    symbol_name: str
    impact_tier: str  # "UNCHANGED", "REFACTOR", "MODIFIED", "BREAKING", "SECURITY_PATCH"
    similarity_score: float
    summary: str
    is_breaking: bool = False
    details: Dict[str, Any] = field(default_factory=dict)


class BinaryDiffImpactClassifier:
    """
    Evaluates similarity metrics and CFG topology changes to classify semantic impact.
    """

    def classify_change(
        self,
        symbol_name: str,
        similarity_score: float,
        v1_blocks_count: int,
        v2_blocks_count: int,
        is_security_function: bool = False,
    ) -> DiffImpactReport:
        if similarity_score >= 0.99 and v1_blocks_count == v2_blocks_count:
            return DiffImpactReport(
                symbol_name=symbol_name,
                impact_tier="UNCHANGED",
                similarity_score=similarity_score,
                summary=f"Symbol '{symbol_name}' is semantically identical across versions.",
                is_breaking=False,
            )

        # Check for security patch: if security function gained additional branch blocks (bounds checks)
        if is_security_function and v2_blocks_count > v1_blocks_count and similarity_score >= 0.60:
            return DiffImpactReport(
                symbol_name=symbol_name,
                impact_tier="SECURITY_PATCH",
                similarity_score=similarity_score,
                summary=f"Security mitigation / validation branch added to '{symbol_name}'.",
                is_breaking=False,
                details={"added_blocks": v2_blocks_count - v1_blocks_count},
            )

        if similarity_score >= 0.80 and abs(v1_blocks_count - v2_blocks_count) <= 1:
            return DiffImpactReport(
                symbol_name=symbol_name,
                impact_tier="REFACTOR",
                similarity_score=similarity_score,
                summary=f"Internal register allocation / minor refactor in '{symbol_name}'.",
                is_breaking=False,
            )

        return DiffImpactReport(
            symbol_name=symbol_name,
            impact_tier="MODIFIED",
            similarity_score=similarity_score,
            summary=f"Structural modification in '{symbol_name}' with altered control flow.",
            is_breaking=False,
            details={"v1_blocks": v1_blocks_count, "v2_blocks": v2_blocks_count},
        )
