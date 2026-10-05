"""Embedding space drift detection (GAP-DRIFT-005).

Computes cosine distance between baseline and current mean embedding vectors
per label and flags labels whose drift exceeds a configurable threshold.
Requires only the standard library (``math``).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class EmbeddingDriftReport:
    """Summary of embedding drift between baseline and current vector sets."""

    baseline_count: int
    current_count: int
    drift_score: float
    drifted_labels: list[str]
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "baseline_count": self.baseline_count,
            "current_count": self.current_count,
            "drift_score": round(self.drift_score, 6),
            "drifted_labels": self.drifted_labels,
            "timestamp": self.timestamp,
        }


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors.

    Returns a value in [-1, 1]. Returns 0.0 if either vector has zero
    magnitude.
    """
    if len(a) != len(b):
        raise ValueError(
            f"Vector dimension mismatch: {len(a)} vs {len(b)}"
        )
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0
    return dot / (mag_a * mag_b)


def _mean_vector(vectors: list[list[float]]) -> list[float]:
    """Compute the element-wise mean of a list of vectors."""
    if not vectors:
        return []
    dim = len(vectors[0])
    sums = [0.0] * dim
    for vec in vectors:
        for i in range(dim):
            sums[i] += vec[i]
    n = len(vectors)
    return [s / n for s in sums]


def _group_vectors_by_label(
    labeled_vectors: dict[str, list[float]],
) -> dict[str, list[list[float]]]:
    """Group vectors by their label prefix (label::id -> label)."""
    groups: dict[str, list[list[float]]] = {}
    for key, vec in labeled_vectors.items():
        label = key.split("::", 1)[0] if "::" in key else key
        groups.setdefault(label, []).append(vec)
    return groups


def detect_embedding_drift(
    baseline_vectors: dict[str, list[float]],
    current_vectors: dict[str, list[float]],
    threshold: float = 0.1,
) -> EmbeddingDriftReport:
    """Detect drift between baseline and current embedding vector sets.

    Each dict maps ``label::id`` keys to embedding vectors. Vectors are
    grouped by label prefix, and the cosine distance between mean vectors
    per label is computed. Labels exceeding ``threshold`` are reported as
    drifted. The overall drift score is the maximum per-label distance.

    Parameters
    ----------
    baseline_vectors:
        Reference embedding vectors keyed by ``label::id``.
    current_vectors:
        Current embedding vectors keyed by ``label::id``.
    threshold:
        Cosine distance threshold above which a label is considered drifted.

    Returns
    -------
    EmbeddingDriftReport
        Report with drift score, drifted labels and timestamp.
    """
    baseline_groups = _group_vectors_by_label(baseline_vectors)
    current_groups = _group_vectors_by_label(current_vectors)

    all_labels = sorted(set(baseline_groups) | set(current_groups))
    drifted_labels: list[str] = []
    max_distance = 0.0

    for label in all_labels:
        baseline_vecs = baseline_groups.get(label, [])
        current_vecs = current_groups.get(label, [])
        if not baseline_vecs or not current_vecs:
            # Label present in one set but not the other counts as full drift
            drifted_labels.append(label)
            max_distance = max(max_distance, 1.0)
            continue

        baseline_mean = _mean_vector(baseline_vecs)
        current_mean = _mean_vector(current_vecs)
        similarity = cosine_similarity(baseline_mean, current_mean)
        distance = 1.0 - similarity
        max_distance = max(max_distance, distance)
        if distance > threshold:
            drifted_labels.append(label)

    return EmbeddingDriftReport(
        baseline_count=len(baseline_vectors),
        current_count=len(current_vectors),
        drift_score=max_distance,
        drifted_labels=drifted_labels,
        timestamp=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    )
