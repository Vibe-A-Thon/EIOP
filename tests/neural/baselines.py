"""Explicit numerical baselines used only by neural verification tests."""

from __future__ import annotations

import hashlib
import math

import numpy as np


class HashBaseline:
    """Non-learning identifier-hash baseline used to prove the anti-stub gates fail."""

    profile = "test"

    def __init__(self, dimensions: int = 32) -> None:
        if dimensions < 1:
            raise ValueError("HashBaseline dimensions must be positive")
        self.dimensions = dimensions

    def embed_node(self, node_id: str) -> np.ndarray:
        values = []
        for index in range(self.dimensions):
            digest = hashlib.sha256(f"{node_id}:{index}".encode("utf-8")).hexdigest()
            values.append((int(digest[:8], 16) / 0xFFFFFFFF) * 2.0 - 1.0)
        norm = math.sqrt(sum(value * value for value in values)) or 1.0
        return np.asarray([value / norm for value in values], dtype=np.float32)

    def parameters(self) -> list[np.ndarray]:
        return []

    def get_training_loss(self) -> None:
        return None
