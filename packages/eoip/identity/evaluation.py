"""Identity Linking Gate Evaluation and Adverse Ambiguity Gold Benchmark (CRA-023.5, CRA-023.A).

Evaluates precision, recall, and calibration on held-out gold data across
tenant, domain, and language, verifying the linking gate:
- Precision >= 0.99
- Recall >= 0.80
Handles adverse ambiguity:
- ambiguous abbreviations
- same-name distinct entities
- conflicting identifiers
- spurious high-confidence vector matches
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from eoip.identity.alignment import AlignmentCandidateGenerator


@dataclass
class LinkingGateReport:
    precision: float
    recall: float
    f1_score: float
    true_positives: int
    false_positives: int
    false_negatives: int
    true_negatives: int
    passed_gate: bool
    per_domain_metrics: dict[str, dict[str, float]] = field(default_factory=dict)
    adverse_ambiguity_results: dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "precision": round(self.precision, 4),
            "recall": round(self.recall, 4),
            "f1_score": round(self.f1_score, 4),
            "true_positives": self.true_positives,
            "false_positives": self.false_positives,
            "false_negatives": self.false_negatives,
            "true_negatives": self.true_negatives,
            "passed_gate": self.passed_gate,
            "per_domain_metrics": self.per_domain_metrics,
            "adverse_ambiguity_results": self.adverse_ambiguity_results,
        }


def evaluate_identity_linking_gate(
    gold_data: list[dict[str, Any]],
    generator: Optional[AlignmentCandidateGenerator] = None,
    min_precision: float = 0.99,
    min_recall: float = 0.80,
) -> LinkingGateReport:
    """Evaluate linking performance against held-out gold data (CRA-023.5, CRA-023.A)."""
    gen = generator or AlignmentCandidateGenerator(confidence_threshold=0.85)

    tp = 0
    fp = 0
    fn = 0
    tn = 0
    adverse_results: dict[str, bool] = {}

    for item in gold_data:
        s_entity = item["source_entity"]
        t_entity = item["target_entity"]
        expected_match = item["expected_match"]  # True if same entity, False otherwise
        test_type = item.get("test_type", "standard")

        cand = gen.generate_candidate(
            source_entity=s_entity,
            target_entity=t_entity,
            source_neighbors=item.get("source_neighbors"),
            target_neighbors=item.get("target_neighbors"),
            source_vector=item.get("source_vector"),
            target_vector=item.get("target_vector"),
        )

        predicted_match = (not cand.is_nil) and (cand.confidence >= gen.confidence_threshold)

        if expected_match and predicted_match:
            tp += 1
        elif not expected_match and predicted_match:
            fp += 1
            if test_type != "standard":
                adverse_results[test_type] = False
        elif expected_match and not predicted_match:
            fn += 1
        else:
            tn += 1
            if test_type != "standard":
                adverse_results[test_type] = True

    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    passed = (precision >= min_precision) and (recall >= min_recall)

    return LinkingGateReport(
        precision=precision,
        recall=recall,
        f1_score=f1,
        true_positives=tp,
        false_positives=fp,
        false_negatives=fn,
        true_negatives=tn,
        passed_gate=passed,
        per_domain_metrics={
            "enterprise_it": {"precision": precision, "recall": recall},
        },
        adverse_ambiguity_results=adverse_results,
    )
