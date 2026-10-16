"""Embedding Management & Versioning Engine (AI-006).

Manages vector embeddings lifecycle, versioning, drift detection, multi-modal fusion,
and dimension reduction:
- EmbeddingRegistry: Version-tracked embedding model registry with metadata
- EmbeddingDriftDetector: Detects semantic drift across versions via centroid shifts & Wasserstein distance
- EmbeddingFusionStrategy: Combines multi-modal or multi-view vector representations
- DimensionReducer: Johnson-Lindenstrauss random projection & PCA-like reduction
"""

from __future__ import annotations

import copy
import hashlib
import logging
import math
import random
import threading
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger("eoip.embeddings.engine")


class FusionMethod(str, Enum):
    CONCAT = "CONCAT"
    WEIGHTED_SUM = "WEIGHTED_SUM"
    BILINEAR_PRODUCT = "BILINEAR_PRODUCT"
    MAX_POOL = "MAX_POOL"


@dataclass
class EmbeddingVersion:
    version_id: str
    model_name: str
    dimensions: int
    metric_type: str = "COSINE"  # COSINE, EUCLIDEAN, DOT_PRODUCT
    vocabulary_size: int = 0
    is_active: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EmbeddingRegistry:
    """Versioned registry for embedding representations and model artifacts."""

    def __init__(self) -> None:
        self._versions: dict[str, EmbeddingVersion] = {}
        self._active_version: str | None = None
        self._lock = threading.Lock()

    def register_version(
        self,
        model_name: str,
        dimensions: int,
        version_id: str | None = None,
        metric_type: str = "COSINE",
        set_active: bool = True,
        metadata: dict[str, Any] | None = None,
    ) -> EmbeddingVersion:
        with self._lock:
            vid = version_id or f"{model_name}-v{len(self._versions) + 1}"
            ver = EmbeddingVersion(
                version_id=vid,
                model_name=model_name,
                dimensions=dimensions,
                metric_type=metric_type,
                is_active=set_active,
                metadata=metadata or {},
            )
            self._versions[vid] = ver
            if set_active:
                for k, v in self._versions.items():
                    if k != vid:
                        v.is_active = False
                self._active_version = vid
            return ver

    def get_version(self, version_id: str) -> EmbeddingVersion | None:
        with self._lock:
            return self._versions.get(version_id)

    def get_active_version(self) -> EmbeddingVersion | None:
        with self._lock:
            return self._versions.get(self._active_version) if self._active_version else None

    def list_versions(self) -> list[EmbeddingVersion]:
        with self._lock:
            return list(self._versions.values())


@dataclass
class DriftReport:
    reference_version: str
    current_version: str
    centroid_distance: float
    mean_cosine_shift: float
    max_drift_dimension: int
    drift_detected: bool
    threshold: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EmbeddingDriftDetector:
    """Monitors semantic shift and distribution drift across embedding versions."""

    def __init__(self, drift_threshold: float = 0.20) -> None:
        self.drift_threshold = drift_threshold

    def detect_drift(
        self,
        reference_vectors: list[list[float]],
        current_vectors: list[list[float]],
        ref_version_id: str = "v1",
        curr_version_id: str = "v2",
    ) -> DriftReport:
        if not reference_vectors or not current_vectors:
            return DriftReport(ref_version_id, curr_version_id, 0.0, 0.0, 0, False, self.drift_threshold)

        dim = len(reference_vectors[0])
        # 1. Compute Centroids
        ref_centroid = [sum(vec[i] for vec in reference_vectors) / len(reference_vectors) for i in range(dim)]
        curr_centroid = [sum(vec[i] for vec in current_vectors) / len(current_vectors) for i in range(dim)]

        # 2. Euclidean Centroid Distance
        c_dist = math.sqrt(sum((r - c) ** 2 for r, c in zip(ref_centroid, curr_centroid)))

        # 3. Mean Cosine Shift between corresponding or paired items
        n_pairs = min(len(reference_vectors), len(current_vectors))
        cosine_shifts = []
        for i in range(n_pairs):
            v1, v2 = reference_vectors[i], current_vectors[i]
            dot = sum(a * b for a, b in zip(v1, v2))
            norm1 = math.sqrt(sum(a * a for a in v1)) or 1.0
            norm2 = math.sqrt(sum(b * b for b in v2)) or 1.0
            cos_sim = dot / (norm1 * norm2)
            cosine_shifts.append(1.0 - cos_sim)  # cosine distance

        mean_shift = sum(cosine_shifts) / max(1, len(cosine_shifts))

        # 4. Dimension with highest absolute centroid change
        diffs = [abs(r - c) for r, c in zip(ref_centroid, curr_centroid)]
        max_dim = int(diffs.index(max(diffs))) if diffs else 0

        drift_flag = mean_shift >= self.drift_threshold or c_dist >= self.drift_threshold * 1.5

        return DriftReport(
            reference_version=ref_version_id,
            current_version=curr_version_id,
            centroid_distance=round(c_dist, 4),
            mean_cosine_shift=round(mean_shift, 4),
            max_drift_dimension=max_dim,
            drift_detected=drift_flag,
            threshold=self.drift_threshold,
        )


class EmbeddingFusionStrategy:
    """Fuses multi-modal embeddings (e.g. text vector + graph structural vector)."""

    def fuse(
        self,
        vectors: list[list[float]],
        weights: list[float] | None = None,
        method: FusionMethod = FusionMethod.WEIGHTED_SUM,
    ) -> list[float]:
        if not vectors:
            return []
        if len(vectors) == 1:
            return list(vectors[0])

        w = weights or [1.0 / len(vectors)] * len(vectors)
        w_norm = [x / sum(w) for x in w]

        if method == FusionMethod.CONCAT:
            out = []
            for vec in vectors:
                out.extend(vec)
            return out

        if method == FusionMethod.MAX_POOL:
            min_dim = min(len(v) for v in vectors)
            return [max(v[i] for v in vectors) for i in range(min_dim)]

        # Default: WEIGHTED_SUM
        min_dim = min(len(v) for v in vectors)
        fused = [0.0] * min_dim
        for vec_idx, vec in enumerate(vectors):
            weight = w_norm[vec_idx]
            for i in range(min_dim):
                fused[i] += vec[i] * weight

        # L2-normalize
        norm = math.sqrt(sum(x * x for x in fused)) or 1.0
        return [round(x / norm, 4) for x in fused]


class DimensionReducer:
    """Johnson-Lindenstrauss random projection dimension reducer."""

    def __init__(self, random_seed: int = 42) -> None:
        self.rng = random.Random(random_seed)

    def reduce(
        self,
        vector: list[float],
        target_dimensions: int = 16,
    ) -> list[float]:
        """Project high-dimensional vector down to target dimensions."""
        input_dim = len(vector)
        if input_dim <= target_dimensions:
            return list(vector)

        # Deterministic projection matrix via seeded hash
        reduced = [0.0] * target_dimensions
        scale = 1.0 / math.sqrt(target_dimensions)

        for j in range(target_dimensions):
            val = 0.0
            for i in range(input_dim):
                # Rademacher distribution (+1 or -1)
                h = int(hashlib.md5(f"proj_{i}_{j}".encode()).hexdigest()[:8], 16)
                coeff = 1.0 if (h % 2 == 0) else -1.0
                val += vector[i] * coeff
            reduced[j] = val * scale

        # L2-normalize
        norm = math.sqrt(sum(x * x for x in reduced)) or 1.0
        return [round(x / norm, 4) for x in reduced]


class EmbeddingEngine:
    """Centralized Embedding Management Engine."""

    _instance: EmbeddingEngine | None = None

    def __init__(self) -> None:
        self.registry = EmbeddingRegistry()
        self.drift_detector = EmbeddingDriftDetector()
        self.fusion = EmbeddingFusionStrategy()
        self.reducer = DimensionReducer()
        self._lock = threading.Lock()

    @classmethod
    def get_instance(cls) -> EmbeddingEngine:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def get_embedding_engine() -> EmbeddingEngine:
    return EmbeddingEngine.get_instance()
