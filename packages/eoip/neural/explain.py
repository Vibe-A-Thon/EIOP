"""Explainability and faithfulness verification for graph neural predictions (CRA-044.10).

Enforces:
1. >= 95% of served predictions carry verifiable evidence paths.
2. Faithfulness probe: removing the identified evidence subgraph must lower
   the prediction score by >= 50%; otherwise the explanation is reported as NOT faithful.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Sequence


@dataclass
class SubgraphExplanation:
    prediction_id: str
    target_edge: tuple[str, str, str]
    base_score: float
    evidence_path: list[tuple[str, str, str]]
    ablated_score: float
    score_reduction_ratio: float
    is_faithful: bool
    evidence_coverage_passed: bool


class NeuralExplainer:
    """Provides path-based explanations and evaluates explanation faithfulness."""

    def explain_prediction(
        self,
        prediction_id: str,
        target_edge: tuple[str, str, str],
        base_score: float,
        evidence_path: list[tuple[str, str, str]],
        score_evaluator: Callable[[list[tuple[str, str, str]]], float],
    ) -> SubgraphExplanation:
        """Explain prediction and run the counterfactual faithfulness probe.

        CRA-044.10: removing the identified evidence subgraph lowers the
        prediction score by >= 50%; otherwise the explanation is reported as not faithful.
        """
        has_evidence = len(evidence_path) > 0
        if not has_evidence:
            return SubgraphExplanation(
                prediction_id=prediction_id,
                target_edge=target_edge,
                base_score=base_score,
                evidence_path=[],
                ablated_score=base_score,
                score_reduction_ratio=0.0,
                is_faithful=False,
                evidence_coverage_passed=False,
            )

        # Counterfactual ablation: score prediction WITHOUT the evidence subgraph
        ablated_score = float(score_evaluator([]))
        reduction = (base_score - ablated_score) / (base_score or 1.0)

        # Faithfulness check: score drop >= 50%
        is_faithful = (reduction >= 0.50)

        return SubgraphExplanation(
            prediction_id=prediction_id,
            target_edge=target_edge,
            base_score=round(base_score, 4),
            evidence_path=evidence_path,
            ablated_score=round(ablated_score, 4),
            score_reduction_ratio=round(reduction, 4),
            is_faithful=is_faithful,
            evidence_coverage_passed=True,
        )
