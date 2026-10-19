"""Resource-Bounded Quantum Simulator Backend (PUR-QPU-001..006).

Classical statevector and density-matrix quantum circuit simulation.
Every output is explicitly labelled:
    simulation=True, physical_qpu=False
"""

from __future__ import annotations

import cmath
import itertools
import math
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


# Standard single-qubit quantum gate unitaries
GATES: Dict[str, np.ndarray] = {
    "H": (1.0 / math.sqrt(2)) * np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex),
    "X": np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex),
    "Y": np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex),
    "Z": np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex),
    "S": np.array([[1.0, 0.0], [0.0, 1.0j]], dtype=complex),
    "T": np.array([[1.0, 0.0], [0.0, cmath.exp(1.0j * math.pi / 4)]], dtype=complex),
}

PAULI_MATRICES = {
    "I": np.array([[1, 0], [0, 1]], dtype=complex),
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
    "Z": np.array([[1, 0], [0, -1]], dtype=complex),
}


def rotation_gate(axis: str, theta: float) -> np.ndarray:
    """Parametric single-qubit rotation gate."""
    c = math.cos(theta / 2.0)
    s = math.sin(theta / 2.0)
    if axis.upper() == "RX":
        return np.array([[c, -1.0j * s], [-1.0j * s, c]], dtype=complex)
    elif axis.upper() == "RY":
        return np.array([[c, -s], [s, c]], dtype=complex)
    elif axis.upper() == "RZ":
        return np.array([[cmath.exp(-1.0j * theta / 2.0), 0.0], [0.0, cmath.exp(1.0j * theta / 2.0)]], dtype=complex)
    else:
        raise ValueError(f"Unknown rotation axis: {axis}")


def estimate_quantum_memory_bytes(num_qubits: int, method: str = "statevector") -> int:
    """Estimate memory requirement before allocation (PUR-QPU-006)."""
    if method == "statevector":
        state_dim = 2 ** num_qubits
        # 16 bytes per complex128 * workspace factor of 4
        return state_dim * 16 * 4
    elif method == "density_matrix":
        state_dim = 2 ** num_qubits
        return (state_dim * state_dim) * 16 * 4
    else:
        raise ValueError(f"Unknown quantum simulation method: {method}")


class QuantumCircuitSimulator:
    """Deterministic, resource-bounded classical simulator for quantum circuits."""

    def __init__(self, num_qubits: int, method: str = "statevector", max_qubits: int = 20):
        if num_qubits < 1:
            raise ValueError("Circuit must have at least 1 qubit")
        if method == "statevector" and num_qubits > max_qubits:
            raise ValueError(f"Statevector simulation capped at {max_qubits} qubits, requested {num_qubits}")
        if method == "density_matrix" and num_qubits > 10:
            raise ValueError(f"Density matrix simulation capped at 10 qubits, requested {num_qubits}")

        self.num_qubits = num_qubits
        self.method = method
        self.dim = 2 ** num_qubits

        # Initialize state |0...0>
        if self.method == "statevector":
            self.state = np.zeros(self.dim, dtype=complex)
            self.state[0] = 1.0 + 0.0j
        else:
            self.state = np.zeros((self.dim, self.dim), dtype=complex)
            self.state[0, 0] = 1.0 + 0.0j

    def apply_single_qubit_gate(self, gate_matrix: np.ndarray, target_qubit: int) -> None:
        """Apply a 2x2 unitary gate to target_qubit."""
        if not (0 <= target_qubit < self.num_qubits):
            raise ValueError(f"Target qubit {target_qubit} out of range [0, {self.num_qubits})")

        if self.method == "statevector":
            # Reshape into tensor of shape (2, 2, ..., 2)
            state_tensor = self.state.reshape([2] * self.num_qubits)
            # Contract gate with target qubit index
            # target_qubit in statevector: index 0 is qubit 0 (left-to-right)
            state_tensor = np.tensordot(gate_matrix, state_tensor, axes=(1, target_qubit))
            # Move the new axis back to target_qubit position
            state_tensor = np.moveaxis(state_tensor, 0, target_qubit)
            self.state = state_tensor.reshape(self.dim)
        else:
            # Density matrix: rho' = U rho U^\dagger
            u_full = self._expand_single_qubit_gate(gate_matrix, target_qubit)
            self.state = u_full @ self.state @ u_full.conj().T

    def _expand_single_qubit_gate(self, gate_matrix: np.ndarray, target_qubit: int) -> np.ndarray:
        mats = []
        for q in range(self.num_qubits):
            if q == target_qubit:
                mats.append(gate_matrix)
            else:
                mats.append(np.eye(2, dtype=complex))
        res = mats[0]
        for m in mats[1:]:
            res = np.kron(res, m)
        return res

    def apply_controlled_gate(self, control_qubit: int, target_qubit: int, gate_2x2: np.ndarray) -> None:
        """Apply a controlled 2-qubit gate (e.g. CX, CZ)."""
        if control_qubit == target_qubit:
            raise ValueError("Control and target qubits cannot be identical")
        if not (0 <= control_qubit < self.num_qubits and 0 <= target_qubit < self.num_qubits):
            raise ValueError("Qubit indices out of range")

        if self.method == "statevector":
            # For statevector, iterate over all basis states where control is 1
            state_tensor = self.state.reshape([2] * self.num_qubits)
            # Slices where control_qubit == 1
            idx_1 = [slice(None)] * self.num_qubits
            idx_1[control_qubit] = 1
            sub_tensor = state_tensor[tuple(idx_1)]

            # Map target_qubit to sub_tensor index
            sub_target = target_qubit if target_qubit < control_qubit else target_qubit - 1
            sub_tensor = np.tensordot(gate_2x2, sub_tensor, axes=(1, sub_target))
            sub_tensor = np.moveaxis(sub_tensor, 0, sub_target)

            state_tensor[tuple(idx_1)] = sub_tensor
            self.state = state_tensor.reshape(self.dim)
        else:
            # Build full controlled unitary
            proj_0 = np.array([[1, 0], [0, 0]], dtype=complex)
            proj_1 = np.array([[0, 0], [0, 1]], dtype=complex)
            mats_0 = [proj_0 if q == control_qubit else np.eye(2, dtype=complex) for q in range(self.num_qubits)]
            mats_1 = [proj_1 if q == control_qubit else (gate_2x2 if q == target_qubit else np.eye(2, dtype=complex)) for q in range(self.num_qubits)]

            def k(lst):
                r = lst[0]
                for x in lst[1:]:
                    r = np.kron(r, x)
                return r

            u_full = k(mats_0) + k(mats_1)
            self.state = u_full @ self.state @ u_full.conj().T

    def apply_depolarizing_noise(self, p: float) -> None:
        """Apply depolarizing noise in density matrix mode: rho = (1-p) rho + p * I / 2^n."""
        if self.method != "density_matrix":
            raise ValueError("Noise can only be applied in density_matrix mode")
        p = max(0.0, min(1.0, float(p)))
        identity = np.eye(self.dim, dtype=complex) / self.dim
        self.state = (1.0 - p) * self.state + p * identity

    def probabilities(self) -> np.ndarray:
        """Compute measurement probability distribution across all 2^n bitstrings."""
        if self.method == "statevector":
            probs = np.abs(self.state) ** 2
        else:
            probs = np.real(np.diag(self.state))
        # Ensure non-negative and normalized
        probs = np.clip(probs, 0.0, 1.0)
        total = np.sum(probs)
        if total > 0:
            probs = probs / total
        return probs

    def sample_shots(self, shots: int = 1024, seed: Optional[int] = None) -> Dict[str, int]:
        """Sample classical bitstrings from probability distribution."""
        probs = self.probabilities()
        rng = np.random.default_rng(seed)
        samples = rng.choice(self.dim, size=shots, p=probs)
        counts: Dict[str, int] = {}
        for s in samples:
            # Bitstring format: qubit 0 is most significant or least significant
            # Format as binary string with self.num_qubits digits
            bitstring = format(s, f"0{self.num_qubits}b")
            counts[bitstring] = counts.get(bitstring, 0) + 1
        return dict(sorted(counts.items()))

    def expectation_pauli(self, pauli_string: str) -> float:
        """Compute expectation value of a tensor product of Pauli operators."""
        if len(pauli_string) != self.num_qubits:
            raise ValueError(f"Pauli string length {len(pauli_string)} must equal qubit count {self.num_qubits}")

        mats = [PAULI_MATRICES[ch.upper()] for ch in pauli_string]
        obs = mats[0]
        for m in mats[1:]:
            obs = np.kron(obs, m)

        if self.method == "statevector":
            exp_val = np.vdot(self.state, obs @ self.state)
        else:
            exp_val = np.trace(self.state @ obs)
        return float(np.real(exp_val))


def run_circuit_simulation(
    circuit_spec: Dict[str, Any],
    method: str = "statevector",
    shots: int = 1024,
    seed: Optional[int] = 42,
    noise_prob: float = 0.0,
) -> Dict[str, Any]:
    """Execute complete quantum circuit simulation per PUR-QPU-001..004."""
    num_qubits = circuit_spec.get("num_qubits", 2)
    gates = circuit_spec.get("gates", [])

    sim = QuantumCircuitSimulator(num_qubits=num_qubits, method=method)

    for g in gates:
        gate_type = g["type"].upper()
        if gate_type in ("H", "X", "Y", "Z", "S", "T"):
            target = g["target"]
            sim.apply_single_qubit_gate(GATES[gate_type], target)
        elif gate_type in ("RX", "RY", "RZ"):
            target = g["target"]
            theta = float(g.get("theta", 0.0))
            sim.apply_single_qubit_gate(rotation_gate(gate_type, theta), target)
        elif gate_type == "CX":
            sim.apply_controlled_gate(g["control"], g["target"], GATES["X"])
        elif gate_type == "CZ":
            sim.apply_controlled_gate(g["control"], g["target"], GATES["Z"])
        else:
            raise ValueError(f"Unsupported quantum gate type: {gate_type}")

    if method == "density_matrix" and noise_prob > 0.0:
        sim.apply_depolarizing_noise(noise_prob)

    counts = sim.sample_shots(shots=shots, seed=seed)
    probs = sim.probabilities().tolist()

    return {
        "simulation": True,
        "is_simulation": True,
        "physical_qpu": False,
        "is_physical_qpu": False,
        "method": method,
        "num_qubits": num_qubits,
        "gate_count": len(gates),
        "shots": shots,
        "counts": counts,
        "probabilities": probs,
    }



def maxcut_experiment(
    edges: List[Tuple[int, int]],
    num_nodes: int,
    p: int = 1,
    gamma: float = 0.5,
    beta: float = 0.5,
    shots: int = 1024,
    seed: Optional[int] = 42,
) -> Dict[str, Any]:
    """Bounded QAOA MaxCut experiment (<=12 vertices, p<=2) compared with classical solver (PUR-QPU-005)."""
    if num_nodes > 12:
        raise ValueError(f"MaxCut simulation restricted to <= 12 vertices, got {num_nodes}")
    if p > 2:
        raise ValueError(f"QAOA depth p restricted to <= 2, got {p}")

    # Build QAOA circuit
    sim = QuantumCircuitSimulator(num_qubits=num_nodes, method="statevector")

    # 1. Uniform superposition |+> on all qubits
    for q in range(num_nodes):
        sim.apply_single_qubit_gate(GATES["H"], q)

    # 2. QAOA layers
    for layer in range(p):
        # Problem unitary e^{-i \gamma C}
        for u, v in edges:
            sim.apply_controlled_gate(u, v, GATES["X"])
            sim.apply_single_qubit_gate(rotation_gate("RZ", 2.0 * gamma), v)
            sim.apply_controlled_gate(u, v, GATES["X"])
        # Mixer unitary e^{-i \beta B}
        for q in range(num_nodes):
            sim.apply_single_qubit_gate(rotation_gate("RX", 2.0 * beta), q)

    counts = sim.sample_shots(shots=shots, seed=seed)

    # Calculate MaxCut value for each bitstring
    def cut_value(bs: str) -> int:
        return sum(1 for u, v in edges if bs[u] != bs[v])

    best_sampled_cut = 0
    best_sampled_bs = ""
    for bs in counts:
        c = cut_value(bs)
        if c > best_sampled_cut:
            best_sampled_cut = c
            best_sampled_bs = bs

    # Classical exhaustive solution for comparison
    classical_max_cut = 0
    classical_best_bs = ""
    for cand in itertools.product("01", repeat=num_nodes):
        cand_str = "".join(cand)
        val = cut_value(cand_str)
        if val > classical_max_cut:
            classical_max_cut = val
            classical_best_bs = cand_str

    return {
        "simulation": True,
        "is_simulation": True,
        "physical_qpu": False,
        "is_physical_qpu": False,
        "num_nodes": num_nodes,
        "edge_count": len(edges),
        "qaoa_p": p,
        "best_sampled_cut": best_sampled_cut,
        "best_sampled_bitstring": best_sampled_bs,
        "classical_optimal_cut": classical_max_cut,
        "classical_optimal_bitstring": classical_best_bs,
        "classical_optimum": {"max_cut_value": classical_max_cut, "bitstring": classical_best_bs},
        "qaoa_best_cut": {"cut_value": best_sampled_cut, "bitstring": best_sampled_bs},
        "qaoa_success_ratio": (best_sampled_cut / classical_max_cut) if classical_max_cut > 0 else 1.0,
        "approximation_ratio": (best_sampled_cut / classical_max_cut) if classical_max_cut > 0 else 1.0,
        "shots": shots,
        "counts": counts,
    }


def calculate_pauli_expectation(
    circuit_spec: Dict[str, Any],
    observable: str = "Z",
    method: str = "statevector",
) -> float:
    """Calculate Pauli expectation value for an arbitrary circuit specification (PUR-QPU-004)."""
    num_qubits = circuit_spec.get("num_qubits", len(observable))
    gates = circuit_spec.get("gates", [])
    sim = QuantumCircuitSimulator(num_qubits=num_qubits, method=method)
    for g in gates:
        gate_type = g["type"].upper()
        if gate_type in ("H", "X", "Y", "Z", "S", "T"):
            sim.apply_single_qubit_gate(GATES[gate_type], g["target"])
        elif gate_type in ("RX", "RY", "RZ"):
            theta = float(g.get("theta", 0.0))
            sim.apply_single_qubit_gate(rotation_gate(gate_type, theta), g["target"])
        elif gate_type == "CX":
            sim.apply_controlled_gate(g["control"], g["target"], GATES["X"])
        elif gate_type == "CZ":
            sim.apply_controlled_gate(g["control"], g["target"], GATES["Z"])
    return sim.expectation_pauli(observable)

