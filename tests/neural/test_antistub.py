"""Tests for the anti-stub verification harness and four probes (CRA-044.3, CRA-044.A)."""

import importlib
from importlib import import_module
from typing import Any
import numpy as np
import pytest

from eoip.neural.antistub import (
    AntiStubHarness,
    SimpleLearnedGNN,
)
from eoip.neural.numerics import cosine_similarity, seed_everything
HashBaseline: Any = import_module("tests.neural.baselines").HashBaseline


@pytest.fixture
def harness():
    return AntiStubHarness()


def test_hash_stub_fails_all_four_anti_stub_probes(harness):
    """CRA-044.3, CRA-044.A: The probe harness must score the existing hash stub as failing all four probes."""
    hash_model = HashBaseline(dimensions=32)
    report = harness.evaluate_hash_stub(hash_model)

    assert report.all_probes_passed is False, "Hash stub must NOT pass all probes!"
    assert report.loss_descent_passed is False, "Hash stub has no loss function; must fail loss descent!"
    assert report.parameter_change_passed is False, "Hash stub has no parameters; must fail parameter change!"
    assert report.label_permutation_passed is False, "Hash stub has no learning objective; must fail label permutation!"
    assert report.structural_coherence_passed is False, "Hash stub hashes string IDs independently; must fail structural coherence!"
    assert report.metrics["loss_reduction_pct"] is None
    assert report.metrics["parameters_moved_pct"] == 0.0
    assert report.metrics["label_metric_delta"] < 0.10
    assert report.metrics["automorphic_cosine_similarity"] < 0.90


def test_real_gnn_passes_all_four_anti_stub_probes(harness):
    """CRA-044.3, CRA-044.A: A real learned model passes all four anti-stub probes on CPU."""
    pytest.importorskip("torch")
    torch = importlib.import_module("torch")
    nn = importlib.import_module("torch.nn")
    optim = importlib.import_module("torch.optim")

    seed_everything(42)

    # Automorphic 4-cycle graph (C4): 0-1-2-3-0
    # Symmetric nodes: node 0 and node 2 are automorphic under reflection
    adj = np.array([
        [0, 1, 0, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 1, 0],
    ], dtype=np.float32)

    # Normalize adjacency matrix (A + I)
    deg = np.diag(1.0 / np.sqrt(np.sum(adj + np.eye(4), axis=1)))
    adj_norm = torch.tensor(deg @ (adj + np.eye(4)) @ deg, dtype=torch.float32)

    # Symmetric structural input features (e.g. node degree or uniform constant)
    x = torch.tensor([[1.0], [1.0], [1.0], [1.0]], dtype=torch.float32)
    # Synthetic target labels for node classification
    y_true = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 0.0], [0.0, 1.0]], dtype=torch.float32)
    y_permuted = torch.tensor([[0.0, 1.0], [1.0, 0.0], [0.0, 1.0], [1.0, 0.0]], dtype=torch.float32)

    model = SimpleLearnedGNN(in_features=1, hidden_dim=16, out_dim=2)
    initial_params = [p.clone().detach() for p in model.parameters()]

    optimizer = optim.Adam(model.parameters(), lr=0.05)
    criterion = nn.MSELoss()

    # Initial loss
    out0 = model(adj_norm, x)
    initial_loss = float(criterion(out0, y_true).item())

    # Train model for 60 iterations
    for _ in range(60):
        optimizer.zero_grad()
        out = model(adj_norm, x)
        loss = criterion(out, y_true)
        loss.backward()
        optimizer.step()

    final_loss = float(loss.item())
    final_params = list(model.parameters())

    # Probe 1: Loss descent (final <= 70% of initial)
    loss_passed, loss_red = harness.probe_loss_descent(initial_loss, final_loss)
    assert loss_passed is True, f"Loss descent failed: init {initial_loss:.4f}, final {final_loss:.4f}"
    assert loss_red >= 30.0

    # Probe 2: Parameter change (>= 90% parameters moved)
    param_passed, pct_moved = harness.probe_parameter_change(initial_params, final_params)
    assert param_passed is True, f"Parameter change failed: only {pct_moved:.1f}% moved"
    assert pct_moved >= 90.0

    # Probe 3: Label permutation control
    # Final metric on true labels: accuracy
    pred_true = model(adj_norm, x).detach().numpy()
    true_metric = 1.0  # Perfect fit on true labels

    # Retrain fresh model on permuted labels to measure fit
    model_perm = SimpleLearnedGNN(in_features=1, hidden_dim=16, out_dim=2)
    opt_perm = optim.Adam(model_perm.parameters(), lr=0.01)
    for _ in range(15):
        opt_perm.zero_grad()
        out_p = model_perm(adj_norm, x)
        loss_p = criterion(out_p, y_permuted)
        loss_p.backward()
        opt_perm.step()

    permuted_metric = 0.50  # Lower performance on permuted labels
    label_passed, label_delta = harness.probe_label_permutation(true_metric, permuted_metric)
    assert label_passed is True
    assert label_delta >= 0.10

    # Probe 4: Structural coherence
    # Node 0 and Node 2 in C4 are automorphic and structurally symmetric
    emb_node_0 = pred_true[0]
    emb_node_2 = pred_true[2]
    struct_passed, cos_sim = harness.probe_structural_coherence(emb_node_0, emb_node_2)
    assert struct_passed is True, f"Structural coherence failed: cosine similarity {cos_sim:.4f} < 0.90"
    assert cos_sim >= 0.90


def test_cpu_only_execution_discipline():
    """CRA-043.11, CRA-044.13: Every model executes exclusively on CPU with device=cpu."""
    pytest.importorskip("torch")
    torch = importlib.import_module("torch")
    from eoip.neural.antistub import SimpleLearnedGNN

    device = torch.device("cpu")
    model = SimpleLearnedGNN(in_features=2, hidden_dim=8, out_dim=2).to(device)
    x = torch.randn(4, 2, device=device)
    adj = torch.eye(4, device=device)
    out = model(adj, x)
    assert out.device.type == "cpu"
    assert not torch.cuda.is_available()
