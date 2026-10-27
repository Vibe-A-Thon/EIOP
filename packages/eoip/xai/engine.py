"""Advanced Explainable AI (XAI) Engine (AI-001).

Implements model-derived explainability and interpretability:
- FeatureImportanceAnalyzer: Model-agnostic Shapley-value estimation via permutation
- DecisionTraceGraph: Directed acyclic reasoning graph with attribution tracking
- ConfidenceCalibrator: Expected Calibration Error (ECE) and reliability diagrams
- ExplanationRenderer: Human-interpretable rendering (plain text, markdown, structured JSON)
"""

from __future__ import annotations

import itertools
import logging
import math
import random
import threading
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from typing import Any
from collections.abc import Callable

logger = logging.getLogger("eoip.xai.engine")


@dataclass
class FeatureAttribution:
    """Attribution score for an individual input feature."""

    feature_name: str
    importance_score: float  # Marginal Shapley value
    direction: str  # "POSITIVE", "NEGATIVE", "NEUTRAL"
    confidence: float = 1.0
    baseline_value: Any = None
    actual_value: Any = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class FeatureImportanceAnalyzer:
    """Computes model-agnostic feature attributions using permutation Shapley values."""

    def __init__(self, random_seed: int = 42) -> None:
        self.rng = random.Random(random_seed)

    def analyze(
        self,
        predict_fn: Callable[[dict[str, Any]], float],
        inputs: dict[str, Any],
        baseline: dict[str, Any] | None = None,
        max_samples: int = 48,
    ) -> list[FeatureAttribution]:
        """Compute Shapley feature attributions.

        For each feature i, estimates the marginal contribution across feature coalitions:
        phi_i = E[f(S U {i}) - f(S)].
        """
        keys = list(inputs.keys())
        n = len(keys)
        if n == 0:
            return []

        base = baseline or {k: 0.0 if isinstance(inputs[k], (int, float)) else "" for k in keys}
        base_val = predict_fn(base)
        actual_val = predict_fn(inputs)
        delta_val = actual_val - base_val

        # If 1 feature, entire delta belongs to it
        if n == 1:
            k = keys[0]
            direction = "POSITIVE" if delta_val > 0.001 else ("NEGATIVE" if delta_val < -0.001 else "NEUTRAL")
            return [
                FeatureAttribution(
                    feature_name=k,
                    importance_score=round(delta_val, 4),
                    direction=direction,
                    actual_value=inputs[k],
                    baseline_value=base.get(k),
                )
            ]

        shapley_values: dict[str, float] = {k: 0.0 for k in keys}
        counts: dict[str, int] = {k: 0 for k in keys}

        # Exact calculation if small number of features (<= 5)
        if n <= 5:
            # 2^n subsets
            for subset_mask in range(1 << n):
                subset = {keys[j]: inputs[keys[j]] if (subset_mask & (1 << j)) else base.get(keys[j]) for j in range(n)}
                val_s = predict_fn(subset)

                for j in range(n):
                    if not (subset_mask & (1 << j)):
                        # S without j
                        s_with_j = dict(subset)
                        s_with_j[keys[j]] = inputs[keys[j]]
                        val_s_with_j = predict_fn(s_with_j)
                        marginal = val_s_with_j - val_s

                        # Subset size |S|
                        s_size = bin(subset_mask).count("1")
                        weight = 1.0 / (n * math.comb(n - 1, s_size))
                        shapley_values[keys[j]] += weight * marginal
                        counts[keys[j]] += 1
        else:
            # Monte Carlo permutation sampling
            num_perms = min(max_samples, 64)
            for _ in range(num_perms):
                perm = list(keys)
                self.rng.shuffle(perm)

                curr_state = dict(base)
                curr_val = predict_fn(curr_state)

                for feat in perm:
                    next_state = dict(curr_state)
                    next_state[feat] = inputs[feat]
                    next_val = predict_fn(next_state)

                    marginal = next_val - curr_val
                    shapley_values[feat] += marginal
                    counts[feat] += 1

                    curr_state = next_state
                    curr_val = next_val

            for k in keys:
                if counts[k] > 0:
                    shapley_values[k] /= counts[k]

        results: list[FeatureAttribution] = []
        for k in keys:
            score = round(shapley_values[k], 4)
            direction = "POSITIVE" if score > 0.001 else ("NEGATIVE" if score < -0.001 else "NEUTRAL")
            results.append(
                FeatureAttribution(
                    feature_name=k,
                    importance_score=score,
                    direction=direction,
                    actual_value=inputs[k],
                    baseline_value=base.get(k),
                )
            )

        # Sort descending by absolute attribution score
        results.sort(key=lambda item: abs(item.importance_score), reverse=True)
        return results


@dataclass
class DecisionStepNode:
    """A node in a neuro-symbolic reasoning trace."""

    step_id: str
    step_type: str  # "PREMISE", "INFERENCE", "VERIFICATION", "CONCLUSION"
    content: str
    confidence: float
    attribution_weight: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class DecisionTraceGraph:
    """Directed graph representing an explainable cognitive chain of inference."""

    def __init__(self) -> None:
        self.nodes: dict[str, DecisionStepNode] = {}
        self.edges: list[dict[str, Any]] = []

    def add_step(
        self,
        step_id: str,
        step_type: str,
        content: str,
        confidence: float,
        attribution_weight: float = 1.0,
    ) -> DecisionStepNode:
        node = DecisionStepNode(
            step_id=step_id,
            step_type=step_type,
            content=content,
            confidence=confidence,
            attribution_weight=attribution_weight,
        )
        self.nodes[step_id] = node
        return node

    def add_edge(self, source_step_id: str, target_step_id: str, relation: str = "DERIVES") -> None:
        self.edges.append({
            "source": source_step_id,
            "target": target_step_id,
            "relation": relation,
        })

    def find_critical_path(self) -> list[str]:
        """Find the chain of steps with the lowest confidence bottleneck."""
        if not self.nodes:
            return []

        # Find entry nodes (in-degree == 0)
        target_ids = {e["target"] for e in self.edges}
        entry_ids = [nid for nid in self.nodes if nid not in target_ids]
        if not entry_ids:
            entry_ids = list(self.nodes.keys())[:1]

        # BFS trace to conclusions
        adj: dict[str, list[str]] = defaultdict(list)
        for e in self.edges:
            adj[e["source"]].append(e["target"])

        # Trace paths
        all_paths: list[list[str]] = []
        queue: list[list[str]] = [[start] for start in entry_ids]

        while queue:
            curr_path = queue.pop(0)
            u = curr_path[-1]
            nbrs = adj.get(u, [])
            if not nbrs:
                all_paths.append(curr_path)
            else:
                for v in nbrs:
                    if v not in curr_path:
                        queue.append(curr_path + [v])

        if not all_paths:
            return list(self.nodes.keys())

        # Path with lowest minimum confidence (weakest link)
        all_paths.sort(key=lambda p: min(self.nodes[nid].confidence for nid in p))
        return all_paths[0]

    def export_mermaid(self) -> str:
        """Export graph to Mermaid flowchart diagram."""
        lines = ["flowchart TD"]
        for node in self.nodes.values():
            safe_text = node.content.replace('"', "'")
            lines.append(f'    {node.step_id}["[{node.step_type}] {safe_text} (p={node.confidence:.2f})"]')
        for edge in self.edges:
            lines.append(f"    {edge['source']} -->|{edge['relation']}| {edge['target']}")
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": self.edges,
            "critical_path": self.find_critical_path(),
        }


@dataclass
class CalibrationBin:
    """Bin statistics for calibration reliability curves."""

    bin_index: int
    bin_lower: float
    bin_upper: float
    mean_predicted: float
    observed_frequency: float
    count: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ConfidenceCalibrationReport:
    """Quantitative confidence calibration metrics."""

    expected_calibration_error: float  # ECE: lower is better (0.0 is perfect)
    maximum_calibration_error: float   # MCE
    brier_score: float                 # Mean squared error of probabilities
    total_samples: int
    bins: list[CalibrationBin] = field(default_factory=list)
    is_well_calibrated: bool = True     # ECE < 0.15

    def to_dict(self) -> dict[str, Any]:
        return {
            "expected_calibration_error": round(self.expected_calibration_error, 4),
            "maximum_calibration_error": round(self.maximum_calibration_error, 4),
            "brier_score": round(self.brier_score, 4),
            "total_samples": self.total_samples,
            "is_well_calibrated": self.is_well_calibrated,
            "bins": [b.to_dict() for b in self.bins],
        }


class ConfidenceCalibrator:
    """Evaluates whether model confidence scores align with empirical true rates."""

    def evaluate(
        self,
        predicted_probs: list[float],
        ground_truth: list[int | bool],
        num_bins: int = 10,
    ) -> ConfidenceCalibrationReport:
        n = len(predicted_probs)
        if n == 0 or len(ground_truth) != n:
            return ConfidenceCalibrationReport(0.0, 0.0, 0.0, 0, [], True)

        # Brier Score
        brier = sum((p - (1.0 if y else 0.0)) ** 2 for p, y in zip(predicted_probs, ground_truth)) / n

        # Reliability Bins
        bins: list[CalibrationBin] = []
        total_ece = 0.0
        max_ce = 0.0
        bin_width = 1.0 / num_bins

        for b_idx in range(num_bins):
            lower = b_idx * bin_width
            upper = (b_idx + 1) * bin_width
            bin_preds = []
            bin_actuals = []

            for p, y in zip(predicted_probs, ground_truth):
                # Put in bin: [lower, upper) or [lower, upper] for final bin
                if lower <= p < upper or (b_idx == num_bins - 1 and p >= upper):
                    bin_preds.append(p)
                    bin_actuals.append(1.0 if y else 0.0)

            cnt = len(bin_preds)
            if cnt > 0:
                mean_pred = sum(bin_preds) / cnt
                obs_freq = sum(bin_actuals) / cnt
                gap = abs(mean_pred - obs_freq)
                total_ece += (cnt / n) * gap
                max_ce = max(max_ce, gap)

                bins.append(
                    CalibrationBin(
                        bin_index=b_idx,
                        bin_lower=round(lower, 2),
                        bin_upper=round(upper, 2),
                        mean_predicted=round(mean_pred, 3),
                        observed_frequency=round(obs_freq, 3),
                        count=cnt,
                    )
                )

        return ConfidenceCalibrationReport(
            expected_calibration_error=round(total_ece, 4),
            maximum_calibration_error=round(max_ce, 4),
            brier_score=round(brier, 4),
            total_samples=n,
            bins=bins,
            is_well_calibrated=total_ece <= 0.15,
        )


class ExplanationRenderer:
    """Produces multi-format human-readable and executive explanations."""

    def render(
        self,
        attributions: list[FeatureAttribution],
        trace: DecisionTraceGraph | None = None,
        calibration: ConfidenceCalibrationReport | None = None,
        format_type: str = "markdown",
    ) -> str:
        if format_type == "markdown":
            lines = ["# Cognitive Decision Explanation", ""]
            lines.append("## Top Contributing Features")
            lines.append("| Feature | Impact (Shapley) | Direction | Actual Value |")
            lines.append("|---|---|---|---|")
            for attr in attributions[:5]:
                sign = "+" if attr.importance_score > 0 else ""
                lines.append(f"| `{attr.feature_name}` | {sign}{attr.importance_score:.4f} | {attr.direction} | `{attr.actual_value}` |")

            if trace and trace.nodes:
                lines.append("")
                lines.append("## Reasoning Trace Graph")
                lines.append("```mermaid")
                lines.append(trace.export_mermaid())
                lines.append("```")
                lines.append(f"**Critical Weak-Link Path**: `{' -> '.join(trace.find_critical_path())}`")

            if calibration:
                lines.append("")
                lines.append("## Calibration Metrics")
                lines.append(f"- **Expected Calibration Error (ECE)**: `{calibration.expected_calibration_error:.4f}`")
                lines.append(f"- **Brier Score**: `{calibration.brier_score:.4f}`")
                lines.append(f"- **Calibrated**: `{'YES' if calibration.is_well_calibrated else 'UNCALIBRATED'}`")

            return "\n".join(lines)

        # Plain text
        summary = [f"{a.feature_name} ({a.direction}: {a.importance_score})" for a in attributions[:3]]
        return f"Decision primarily driven by: {', '.join(summary)}."


class AdvancedXAIEngine:
    """Centralized Explainable AI (XAI) Engine."""

    _instance: AdvancedXAIEngine | None = None

    def __init__(self) -> None:
        self.feature_analyzer = FeatureImportanceAnalyzer()
        self.calibrator = ConfidenceCalibrator()
        self.renderer = ExplanationRenderer()
        self._lock = threading.Lock()

    @classmethod
    def get_instance(cls) -> AdvancedXAIEngine:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def explain(
        self,
        predict_fn: Callable[[dict[str, Any]], float],
        inputs: dict[str, Any],
        baseline: dict[str, Any] | None = None,
        trace: DecisionTraceGraph | None = None,
    ) -> dict[str, Any]:
        """Produce full explanation with feature importance, trace, and rendered output."""
        attributions = self.feature_analyzer.analyze(predict_fn, inputs, baseline)
        md_explanation = self.renderer.render(attributions, trace=trace)

        return {
            "attributions": [a.to_dict() for a in attributions],
            "trace": trace.to_dict() if trace else None,
            "rendered_markdown": md_explanation,
            "top_positive_feature": next((a.feature_name for a in attributions if a.direction == "POSITIVE"), None),
            "top_negative_feature": next((a.feature_name for a in attributions if a.direction == "NEGATIVE"), None),
        }


def get_xai_engine() -> AdvancedXAIEngine:
    return AdvancedXAIEngine.get_instance()
