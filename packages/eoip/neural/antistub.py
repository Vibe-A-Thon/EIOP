"""Anti-stub verification harness and probe suite (CRA-044.3, CRA-044.A).

Proves that learned models actually learn and rejects pseudo-random/hash stand-ins.
Enforces the 4 anti-stub probes:
1. Loss descent: final loss <= 70% of initial loss (>= 30% reduction).
2. Parameter change: >= 90% of model weight tensors move.
3. Label-permutation control: true-label primary metric beats permuted-label metric by >= 0.10 absolute.
4. Structural coherence: two automorphic nodes have embedding cosine >= 0.90.
"""

from __future__ import annotations

import hashlib
import importlib
import math
from dataclasses import dataclass, field
from typing import Any
from collections.abc import Callable

import numpy as np

try:
    torch = importlib.import_module("torch")
    nn = importlib.import_module("torch.nn")
except ImportError:
    torch = None
    nn = None

from eoip.neural.numerics import (
    cosine_similarity,
    ensure_float32,
    seed_everything,
)
from eoip.neural.runtime import NeuralTier, require_tier


@dataclass
class AntiStubReport:
    model_name: str
    loss_descent_passed: bool
    parameter_change_passed: bool
    label_permutation_passed: bool
    structural_coherence_passed: bool
    all_probes_passed: bool
    metrics: dict[str, Any] = field(default_factory=dict)


class HashBaseline:
    """Hash-based graph embedding stand-in fixture (CRA-044.1, CRA-044.5).

    Computes SHA-256 digests of node identifiers with no loss function,
    no optimizer, no parameters, and no graph structure learning.
    """

    def __init__(self, dimensions: int = 32) -> None:
        self.dimensions = dimensions

    def embed_node(self, node_id: str) -> np.ndarray:
        vec = []
        for i in range(self.dimensions):
            h = hashlib.sha256(f"{node_id}:{i}".encode()).hexdigest()
            val = (int(h[:8], 16) / 0xFFFFFFFF) * 2.0 - 1.0
            vec.append(val)
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return np.array([x / norm for x in vec], dtype=np.float32)

    def parameters(self) -> list[np.ndarray]:
        # Hash stub has no learned parameters
        return []

    def get_training_loss(self) -> None:
        """The hash baseline has no training objective or observed loss."""
        return


class AntiStubHarness:
    """The four-probe anti-stub verification harness (CRA-044.3)."""

    def probe_loss_descent(self, initial_loss: float, final_loss: float) -> tuple[bool, float]:
        """Probe 1: Final loss must be <= 70% of initial loss (>= 30% reduction)."""
        if initial_loss <= 0.0:
            return False, 0.0
        ratio = final_loss / initial_loss
        passed = (ratio <= 0.70)
        reduction = (1.0 - ratio) * 100.0
        return passed, reduction

    def probe_parameter_change(
        self,
        initial_params: list[Any],
        final_params: list[Any],
        threshold: float = 1e-4,
    ) -> tuple[bool, float]:
        """Probe 2: >= 90% of parameter tensors must move (norm diff > threshold)."""
        if not initial_params or not final_params or len(initial_params) != len(final_params):
            return False, 0.0

        moved_count = 0
        total_tensors = len(initial_params)

        for p_init, p_final in zip(initial_params, final_params):
            is_tensor = torch is not None and isinstance(p_init, torch.Tensor)
            arr_init = p_init.detach().cpu().numpy() if is_tensor else np.asarray(p_init)
            arr_final = p_final.detach().cpu().numpy() if is_tensor else np.asarray(p_final)
            diff_norm = float(np.linalg.norm(arr_final - arr_init))
            if diff_norm > threshold:
                moved_count += 1

        percent_moved = (moved_count / total_tensors) * 100.0
        passed = (percent_moved >= 90.0)
        return passed, percent_moved

    def probe_label_permutation(
        self,
        true_metric: float,
        permuted_metric: float,
    ) -> tuple[bool, float]:
        """Probe 3: True-label primary metric must beat permuted-label metric by >= 0.10 absolute."""
        diff = true_metric - permuted_metric
        passed = (diff >= 0.10)
        return passed, diff

    def probe_structural_coherence(
        self,
        emb_node_a: np.ndarray,
        emb_node_b: np.ndarray,
    ) -> tuple[bool, float]:
        """Probe 4: Two automorphic nodes must have embedding cosine similarity >= 0.90."""
        cos_sim = float(cosine_similarity(emb_node_a, emb_node_b))
        passed = (cos_sim >= 0.90)
        return passed, cos_sim

    def evaluate_hash_stub(self, hash_model: Any) -> AntiStubReport:
        """CRA-044.3: The probe harness must score the existing hash stub as failing all four probes."""
        loss_observations = hash_model.get_training_loss()
        if loss_observations is None:
            loss_passed, loss_red = False, None
        else:
            loss_passed, loss_red = self.probe_loss_descent(*loss_observations)

        param_passed, param_pct = self.probe_parameter_change([], [])

        # Compare held-out classifiers over actual identifier-hash vectors and permuted labels.
        from sklearn.linear_model import LogisticRegression

        sample_count = 4096
        node_ids = [f"node-{index}" for index in range(sample_count)]
        embeddings = np.stack([hash_model.embed_node(node_id) for node_id in node_ids])
        labels = np.arange(sample_count, dtype=np.int32) % 2
        permutation = np.random.default_rng(20261016).permutation(sample_count)
        train_ids, test_ids = permutation[:3072], permutation[3072:]
        permuted_labels = np.random.default_rng(20261017).permutation(labels)

        def held_out_accuracy(targets: np.ndarray) -> float:
            classifier = LogisticRegression(random_state=20261016, max_iter=200)
            classifier.fit(embeddings[train_ids], targets[train_ids])
            return float(np.mean(classifier.predict(embeddings[test_ids]) == targets[test_ids]))

        true_score = held_out_accuracy(labels)
        permuted_score = held_out_accuracy(permuted_labels)
        label_passed, label_diff = self.probe_label_permutation(true_score, permuted_score)

        emb_0 = hash_model.embed_node("node_0")
        emb_2 = hash_model.embed_node("node_2")
        struct_passed, struct_sim = self.probe_structural_coherence(emb_0, emb_2)

        all_passed = (loss_passed and param_passed and label_passed and struct_passed)

        return AntiStubReport(
            model_name="HashBaseline",
            loss_descent_passed=loss_passed,
            parameter_change_passed=param_passed,
            label_permutation_passed=label_passed,
            structural_coherence_passed=struct_passed,
            all_probes_passed=all_passed,
            metrics={
                "loss_reduction_pct": loss_red,
                "parameters_moved_pct": param_pct,
                "true_label_accuracy": true_score,
                "permuted_label_accuracy": permuted_score,
                "label_metric_delta": label_diff,
                "automorphic_cosine_similarity": struct_sim,
            },
        )


_TORCH_MODEL_CLASS: Any = None


class SimpleLearnedGNN:
    """Lazily construct the Torch-only reference encoder when N1 is installed."""

    def __new__(
        cls,
        in_features: int,
        hidden_dim: int = 16,
        out_dim: int = 8,
    ) -> Any:
        if torch is None or nn is None:
            require_tier(NeuralTier.NEURAL)
        global _TORCH_MODEL_CLASS
        if _TORCH_MODEL_CLASS is None:
            torch_module: Any = torch
            nn_module: Any = nn

            class TorchSimpleLearnedGNN(nn_module.Module):
                def __init__(self, in_feat: int, hidden: int, out: int) -> None:
                    super().__init__()
                    self.fc1 = nn_module.Linear(in_feat, hidden, bias=True)
                    self.fc2 = nn_module.Linear(hidden, out, bias=True)
                    self.relu = nn_module.ReLU()

                def forward(self, adj_norm: Any, x: Any) -> Any:
                    h1 = self.relu(torch_module.matmul(adj_norm, self.fc1(x)))
                    return torch_module.matmul(adj_norm, self.fc2(h1))

            _TORCH_MODEL_CLASS = TorchSimpleLearnedGNN
        return _TORCH_MODEL_CLASS(in_features, hidden_dim, out_dim)
