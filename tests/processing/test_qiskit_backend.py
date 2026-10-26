"""Qiskit / Qiskit Aer quantum backend acceptance (PUR-QPU-001..006).

Each test names the acceptance clause it covers. Analytic values are derived independently of
Qiskit (closed-form amplitudes or a hand-written depolarizing channel), so these are oracle checks,
not self-comparisons.
"""
from __future__ import annotations

import math

import numpy as np
import pytest

qiskit = pytest.importorskip("qiskit")
pytest.importorskip("qiskit_aer")

from eoip.processing.backends import qiskit_backend as qb  # noqa: E402
from eoip.processing.backends.qiskit_backend import CircuitValidationError  # noqa: E402
from eoip.processing.contracts import ExecutionContext, LogicalUnit, ProcessingRequest  # noqa: E402
from eoip.processing.service import ProcessingService  # noqa: E402

BELL = {"num_qubits": 2, "gates": [{"type": "H", "target": 0}, {"type": "CX", "control": 0, "target": 1}]}
GHZ3 = {"num_qubits": 3, "gates": [{"type": "H", "target": 0}, {"type": "CX", "control": 0, "target": 1},
                                   {"type": "CX", "control": 1, "target": 2}, {"type": "MEASURE"}]}


def _no_simulator(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("invalid circuit reached compilation/simulation")
    monkeypatch.setattr(qb, "_simulator", boom)
    monkeypatch.setattr(qb, "compile_to_qiskit", boom)


# ------------------------------------------------------------------ PUR-QPU-001
@pytest.mark.req("PUR-QPU-001")
def test_compiles_validated_json_to_a_qiskit_circuit():
    qc = qb.compile_to_qiskit({"num_qubits": 2, "gates": [
        {"type": g, "target": 0} for g in ("H", "X", "Y", "Z", "S", "T")] + [
        {"type": r, "target": 1, "theta": 0.3} for r in ("RX", "RY", "RZ")] + [
        {"type": "CX", "control": 0, "target": 1}, {"type": "CZ", "control": 1, "target": 0}]})
    assert isinstance(qc, qiskit.QuantumCircuit)
    ops = qc.count_ops()
    assert all(ops[g] == 1 for g in ("h", "x", "y", "z", "s", "t", "rx", "ry", "rz", "cx", "cz"))
    assert ops["measure"] == 2  # end-of-circuit measurement


@pytest.mark.req("PUR-QPU-001")
@pytest.mark.parametrize("spec,theta", [(BELL, None), (GHZ3, None),
                                        ({"num_qubits": 1, "gates": [{"type": "RY", "target": 0, "theta": 1.1}]}, 1.1),
                                        ({"num_qubits": 1, "gates": [{"type": "RX", "target": 0, "theta": 2.0}]}, 2.0)])
def test_bell_ghz_rotation_match_analytic_probabilities(spec, theta):
    probs = qb.exact_probabilities(spec)
    if theta is not None:
        expected = [math.cos(theta / 2) ** 2, math.sin(theta / 2) ** 2]
    else:
        n = spec["num_qubits"]
        expected = [0.0] * 2 ** n
        expected[0] = expected[-1] = 0.5
    assert np.allclose(probs, expected, atol=1e-12)


@pytest.mark.req("PUR-QPU-001")
@pytest.mark.parametrize("spec,match", [
    ({"num_qubits": 2, "gates": [{"type": "CCX", "control": 0, "target": 1}]}, "unsupported gate"),
    ({"num_qubits": 2, "gates": [{"type": "IF_ELSE", "target": 0}]}, "control-flow"),
    ({"num_qubits": 2, "gates": [{"type": "WHILE", "target": 0}]}, "control-flow"),
    ({"num_qubits": 2, "gates": [{"type": "MEASURE"}, {"type": "H", "target": 0}]}, "end of the circuit"),
    ({"num_qubits": 2, "gates": [{"type": "RX", "target": 0, "theta": float("nan")}]}, "finite"),
    ({"num_qubits": 2, "gates": [{"type": "RX", "target": 0, "theta": float("inf")}]}, "finite"),
    ({"num_qubits": 2, "gates": [{"type": "H", "target": 2}]}, "declared qubit"),
    ({"num_qubits": 2, "gates": [{"type": "CX", "control": 1, "target": 1}]}, "must differ"),
    ({"num_qubits": 2, "gates": [{"type": "H", "target": 0, "matrix": [[1, 0], [0, 1]]}]}, "unexpected fields"),
    ({"num_qubits": 2, "qasm": "OPENQASM 3; qubit q; h q;"}, "no executable"),
    ({"num_qubits": 2, "gates": [], "code": "import os"}, "no executable"),
])
def test_invalid_circuits_fail_before_simulation(monkeypatch, spec, match):
    _no_simulator(monkeypatch)
    with pytest.raises(CircuitValidationError, match=match):
        qb.sample(spec, shots=8)


# ------------------------------------------------------------------ PUR-QPU-002
@pytest.mark.req("PUR-QPU-002")
@pytest.mark.parametrize("method", ["statevector", "density_matrix"])
def test_both_methods_are_normalised_and_match_noise_free(method):
    probs = qb.exact_probabilities(BELL, method=method)
    assert math.isclose(sum(probs), 1.0, abs_tol=1e-12)
    assert np.allclose(probs, [0.5, 0, 0, 0.5], atol=1e-12)


@pytest.mark.req("PUR-QPU-002")
@pytest.mark.parametrize("lam", [0.0, 0.1, 0.2, 1.0])
def test_declared_depolarizing_case_matches_hand_derived_channel(lam):
    # Independent derivation: H on q0 then 1q depolarizing(lam); CX then 2q depolarizing(lam).
    # rho = (1-lam)[(1-lam)|Phi+><Phi+| + lam/2(|00><00|+|11><11|)] + lam I/4
    p_same = (1 - lam) * 0.5 + lam / 4
    p_diff = lam / 4
    probs = qb.exact_probabilities(BELL, method="density_matrix", noise_prob=lam)
    assert np.allclose(probs, [p_same, p_diff, p_diff, p_same], atol=1e-12)


@pytest.mark.req("PUR-QPU-002")
def test_noise_bounds_and_statevector_noise_rejected():
    for bad in (-0.01, 1.01):
        with pytest.raises(CircuitValidationError):
            qb.sample(BELL, method="density_matrix", noise_prob=bad)
    with pytest.raises(CircuitValidationError, match="density_matrix"):
        qb.sample(BELL, method="statevector", noise_prob=0.1)
    assert qb.sample(BELL, method="density_matrix", noise_prob=0.1, shots=16)["physical_qpu"] is False


# ------------------------------------------------------------------ PUR-QPU-003
@pytest.mark.req("PUR-QPU-003")
def test_counts_sum_to_shots_seeded_repeat_and_declared_endianness():
    a = qb.sample(GHZ3, shots=3000, seed=11)
    b = qb.sample(GHZ3, shots=3000, seed=11)
    assert sum(a["counts"].values()) == 3000 and a["counts"] == b["counts"]
    assert list(a["counts"]) == sorted(a["counts"])  # ordered bitstrings
    x0 = qb.sample({"num_qubits": 3, "gates": [{"type": "X", "target": 0}]}, shots=5, seed=1)
    assert a["endianness"] == "q0-leftmost" and x0["counts"] == {"100": 5}


@pytest.mark.req("PUR-QPU-003")
def test_sample_frequencies_pass_predeclared_statistical_rule():
    # Predeclared rule: every outcome's count lies within 5 binomial standard deviations of shots*p.
    spec = {"num_qubits": 2, "gates": [{"type": "RY", "target": 0, "theta": 1.0}, {"type": "H", "target": 1}]}
    shots = 20000
    res = qb.sample(spec, shots=shots, seed=5)
    c, s = math.cos(0.5) ** 2, math.sin(0.5) ** 2
    analytic = {"00": c / 2, "01": c / 2, "10": s / 2, "11": s / 2}
    for bs, p in analytic.items():
        assert abs(res["counts"].get(bs, 0) - shots * p) <= 5 * math.sqrt(shots * p * (1 - p)), bs


@pytest.mark.req("PUR-QPU-003")
def test_shot_bounds():
    for bad in (0, -1, 10**7, 1.5):
        with pytest.raises(CircuitValidationError):
            qb.sample(BELL, shots=bad)


# ------------------------------------------------------------------ PUR-QPU-004
@pytest.mark.req("PUR-QPU-004")
@pytest.mark.parametrize("spec,obs,expected", [
    (BELL, "ZZ", 1.0), (BELL, "XX", 1.0), (BELL, "YY", -1.0), (BELL, "ZI", 0.0),
    ({"num_qubits": 2, "gates": [{"type": "X", "target": 0}]}, "ZI", -1.0),
    ({"num_qubits": 2, "gates": [{"type": "X", "target": 0}]}, "IZ", 1.0),
    ({"num_qubits": 1, "gates": [{"type": "RY", "target": 0, "theta": 0.7}]}, "Z", math.cos(0.7)),
    ({"num_qubits": 1, "gates": [{"type": "RY", "target": 0, "theta": 0.7}]}, "X", math.sin(0.7)),
    (BELL, [["ZZ", 0.5], ["XX", 0.25], ["II", -1.0]], -0.25),
])
def test_known_expectations(spec, obs, expected):
    res = qb.expectation(spec, obs)
    assert res["primitive"] == "EstimatorV2" and math.isclose(res["expectation"], expected, abs_tol=1e-9)


@pytest.mark.req("PUR-QPU-004")
@pytest.mark.parametrize("obs", ["Z", "ZZZ", "ZQ", [["ZZ", 1j]], [["ZZ", float("nan")]], [[1, 0], [0, 1]],
                                 [["ZZ", 1.0]] * 65, []])
def test_observable_shape_and_hermiticity_constraints(obs):
    with pytest.raises(CircuitValidationError):
        qb.expectation(BELL, obs)


# ------------------------------------------------------------------ PUR-QPU-005
@pytest.mark.req("PUR-QPU-005")
def test_qaoa_uses_primitives_and_cobyla_within_bounds_and_compares_with_exhaustive():
    ring = [(0, 1), (1, 2), (2, 3), (3, 0)]
    res = qb.qaoa_maxcut(ring, 4, p=1, seed=3)
    assert res["primitives"] == ["EstimatorV2", "SamplerV2"] and res["optimizer"] == "scipy.COBYLA"
    assert 1 <= res["objective_evaluations"] <= 50 == res["max_evaluations"]
    assert len(res["objective_history"]) == res["objective_evaluations"]
    # p=1 QAOA on an even ring has optimal expected cut 3/4 * |E| = 3 (analytic); COBYLA must reach it
    assert math.isclose(res["expected_cut"], 3.0, abs_tol=1e-3)
    assert res["classical_optimal_cut"] == 4 and res["best_sampled_cut"] <= 4
    cmp_ = res["comparison"]
    assert cmp_["advantage_claimed"] is False and cmp_["classical_states_enumerated"] == 16
    assert cmp_["qaoa_wall_time_s"] > 0 and cmp_["classical_wall_time_s"] >= 0 and cmp_["qaoa_memory_bytes_estimate"] == 256
    assert res["physical_qpu"] is False and res["simulation"] is True
    again = qb.qaoa_maxcut(ring, 4, p=1, seed=3)
    assert again["optimal_parameters"] == res["optimal_parameters"] and again["counts"] == res["counts"]


@pytest.mark.req("PUR-QPU-005")
def test_qaoa_failures_are_reported_not_hidden():
    # 1 evaluation cannot converge and a triangle's p=1 sample may miss the optimum: both must surface
    res = qb.qaoa_maxcut([(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5), (5, 3)], 6, p=2, max_evaluations=1, seed=1)
    assert res["objective_evaluations"] == 1 and res["failures"]
    assert any("COBYLA" in f for f in res["failures"])


@pytest.mark.req("PUR-QPU-005")
@pytest.mark.parametrize("kw", [dict(num_nodes=13, edges=[(0, 1)]), dict(num_nodes=4, edges=[(0, 1)], p=3),
                                dict(num_nodes=4, edges=[(0, 1)], max_evaluations=51),
                                dict(num_nodes=4, edges=[(0, 4)]), dict(num_nodes=4, edges=[(1, 1)]),
                                dict(num_nodes=4, edges=[])])
def test_qaoa_bounds(kw):
    with pytest.raises(CircuitValidationError):
        qb.qaoa_maxcut(kw.pop("edges"), kw.pop("num_nodes"), **kw)


# ------------------------------------------------------------------ PUR-QPU-006
@pytest.mark.req("PUR-QPU-006")
@pytest.mark.parametrize("n,method", [(21, "statevector"), (11, "density_matrix")])
def test_oversized_rejected_before_allocation(monkeypatch, n, method):
    _no_simulator(monkeypatch)
    with pytest.raises(CircuitValidationError, match="exceeds"):
        qb.sample({"num_qubits": n, "gates": []}, method=method)


@pytest.mark.req("PUR-QPU-001", "PUR-QPU-005", "PUR-QPU-006")
@pytest.mark.parametrize("op,inputs,params", [
    ("quantum.simulate", {"circuit": BELL}, {"shots": 64}),
    ("quantum.sample", {"circuit": GHZ3}, {"shots": 64}),
    ("quantum.expectation", {"circuit": BELL, "observable": "ZZ"}, {}),
    ("quantum.maxcut_experiment", {"edges": [[0, 1], [1, 2], [2, 0]]}, {"num_nodes": 3, "max_evaluations": 20}),
])
def test_service_routes_to_qiskit_and_labels_every_result(op, inputs, params):
    svc = ProcessingService()
    req = ProcessingRequest(logical_unit=LogicalUnit.QPU, operator_id=op, inputs=inputs, parameters=params)
    result, receipt = svc.execute_direct(req, ExecutionContext(tenant_id="t", principal_id="p"))
    assert result["backend"] == "qiskit-aer" and receipt.actual_provider == "qiskit_aer_simulation"
    assert result["simulation"] is True and result["physical_qpu"] is False
    assert receipt.is_simulation is True and receipt.is_physical_qpu is False
    assert svc.probe_profile("qiskit_aer")["status"] == "QUALIFIED"
