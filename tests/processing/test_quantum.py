"""Tests for Quantum Simulation Backend and QPU Operators (PUR-QPU-001..005).

Verifies resource-bounded classical simulation (statevector and density matrix),
Pauli expectation calculation, MaxCut QAOA vs classical exhaustive comparison,
and strict requirement that physical_qpu=false and simulation=true on all receipts and results.
"""

from __future__ import annotations

import pytest

from eoip.processing.backends import quantum_sim
from eoip.processing.contracts import ExecutionContext, LogicalUnit, ProcessingRequest
from eoip.processing.service import ProcessingService


@pytest.fixture
def service() -> ProcessingService:
    return ProcessingService()


@pytest.fixture
def context() -> ExecutionContext:
    return ExecutionContext(
        tenant_id="quantum_tenant",
        principal_id="quantum_researcher",
    )


@pytest.mark.req("PUR-QPU-001")
def test_bell_state_simulation_statevector():
    """PUR-QPU-001: 2-qubit Bell state (|00> + |11>) / sqrt(2) statevector simulation."""
    circuit = {
        "num_qubits": 2,
        "gates": [
            {"type": "H", "target": 0},
            {"type": "CX", "control": 0, "target": 1},
        ],
    }
    res = quantum_sim.run_circuit_simulation(circuit, method="statevector", shots=2048, seed=42)
    assert res["is_simulation"] is True
    assert res["is_physical_qpu"] is False
    assert res["num_qubits"] == 2
    counts = res["counts"]
    # Only "00" and "11" should appear with significant frequency
    assert "00" in counts
    assert "11" in counts
    assert counts.get("01", 0) == 0
    assert counts.get("10", 0) == 0
    total_shots = sum(counts.values())
    assert total_shots == 2048


@pytest.mark.req("PUR-QPU-002")
def test_density_matrix_with_depolarizing_noise():
    """PUR-QPU-002: Density matrix simulation with depolarizing noise introduces mixed states."""
    circuit = {
        "num_qubits": 2,
        "gates": [
            {"type": "H", "target": 0},
            {"type": "CX", "control": 0, "target": 1},
        ],
    }
    res = quantum_sim.run_circuit_simulation(circuit, method="density_matrix", shots=1024, seed=42, noise_prob=0.1)
    assert res["is_simulation"] is True
    assert res["is_physical_qpu"] is False
    counts = res["counts"]
    # With 10% depolarizing noise, "01" and "10" should appear with non-zero probability
    assert counts.get("01", 0) > 0 or counts.get("10", 0) > 0


@pytest.mark.req("PUR-QPU-003")
def test_qpu_bounds_and_limits():
    """PUR-QPU-003: Strict resource bounds: max 20 statevector qubits, max 10 density-matrix qubits."""
    # Statevector with >20 qubits must fail closed
    bad_sv_circuit = {"num_qubits": 21, "gates": []}
    with pytest.raises(ValueError, match=r"capped at 20 qubits"):
        quantum_sim.run_circuit_simulation(bad_sv_circuit, method="statevector")

    # Density matrix with >10 qubits must fail closed
    bad_dm_circuit = {"num_qubits": 11, "gates": []}
    with pytest.raises(ValueError, match=r"capped at 10 qubits"):
        quantum_sim.run_circuit_simulation(bad_dm_circuit, method="density_matrix")



@pytest.mark.req("PUR-QPU-004")
def test_pauli_expectation():
    """PUR-QPU-004: Calculate observable expectation values for Pauli operators."""
    # |0> has <Z> = 1.0, <X> = 0.0
    circuit_zero = {"num_qubits": 1, "gates": []}
    exp_z = quantum_sim.calculate_pauli_expectation(circuit_zero, "Z")
    assert abs(exp_z - 1.0) < 1e-4

    # |+> has <X> = 1.0, <Z> = 0.0
    circuit_plus = {"num_qubits": 1, "gates": [{"type": "H", "target": 0}]}
    exp_x = quantum_sim.calculate_pauli_expectation(circuit_plus, "X")
    assert abs(exp_x - 1.0) < 1e-4


@pytest.mark.req("PUR-QPU-005")
def test_maxcut_qaoa_vs_classical():
    """PUR-QPU-005: MaxCut experiment comparing simulated QAOA vs classical exhaustive search."""
    edges = [(0, 1), (1, 2), (2, 0)]  # Triangle graph
    res = quantum_sim.maxcut_experiment(edges, num_nodes=3, p=1, shots=1024, seed=42)
    assert res["is_simulation"] is True
    assert res["is_physical_qpu"] is False
    assert res["classical_optimum"]["max_cut_value"] == 2  # Triangle max cut is 2
    assert "qaoa_best_cut" in res
    assert res["qaoa_best_cut"]["cut_value"] == 2
    assert res["qaoa_success_ratio"] > 0.0


@pytest.mark.req("PUR-QPU-001")
def test_qpu_receipt_simulation_flags(service: ProcessingService, context: ExecutionContext):
    """PUR-QPU-001: ExecutionReceipt for QPU operations must assert is_simulation=True and is_physical_qpu=False."""
    req = ProcessingRequest(
        logical_unit=LogicalUnit.QPU,
        operator_id="quantum.simulate",
        inputs={
            "circuit": {
                "num_qubits": 1,
                "gates": [{"type": "H", "target": 0}],
            }
        },
        parameters={"shots": 1024},
    )
    result, receipt = service.execute_direct(req, context)
    assert result["is_simulation"] is True
    assert result["is_physical_qpu"] is False
    assert receipt.is_simulation is True
    assert receipt.is_physical_qpu is False
    assert receipt.actual_provider == "qiskit_aer_simulation"
