"""Qiskit / Qiskit Aer quantum simulation backend (PUR-QPU-001..006).

* ``validate_circuit``: the only accepted input is a declarative JSON circuit — gates
  H/X/Y/Z/S/T/RX/RY/RZ/CX/CZ, finite angles, declared integer qubit indices, optional measurement
  only at the end. Anything else (unknown gates, control flow, mid-circuit measurement, QASM/code
  payloads, extra keys) is rejected *before* any simulator is touched; there is no executable upload.
* ``compile_to_qiskit``: builds a ``qiskit.QuantumCircuit`` from the validated spec.
* ``sample`` / ``expectation``: Qiskit Aer ``SamplerV2`` / ``EstimatorV2`` primitives (statevector or
  density-matrix method; optional bounded depolarizing noise model). Bitstrings are reported
  **q0-leftmost** (Qiskit's native order is reversed; the conversion is explicit and declared).
* ``qaoa_maxcut``: bounded, seeded QAOA (<=12 vertices, p<=2, <=50 objective evaluations) whose
  objective is evaluated with ``EstimatorV2`` and optimised with SciPy COBYLA; the result is compared
  with the exhaustive classical optimum (value, wall time, memory) and never claims an advantage.

Every result carries ``simulation=True, physical_qpu=False`` and the backend/primitive used.
"""

from __future__ import annotations

import itertools
import math
import time
from typing import Any

import numpy as np

SINGLE = {"H": "h", "X": "x", "Y": "y", "Z": "z", "S": "s", "T": "t"}
ROTATION = {"RX": "rx", "RY": "ry", "RZ": "rz"}
TWO = {"CX": "cx", "CZ": "cz"}
METHODS = {"statevector", "density_matrix"}
MAX_QUBITS = {"statevector": 20, "density_matrix": 10}
MAX_GATES = 2000
MAX_SHOTS = 100_000
MAX_PAULI_TERMS = 64
LABELS = {"simulation": True, "is_simulation": True, "physical_qpu": False, "is_physical_qpu": False}


class CircuitValidationError(ValueError):
    """The circuit spec is not an accepted declarative circuit."""


def available() -> bool:
    try:
        import qiskit  # noqa: F401
        import qiskit_aer  # noqa: F401
    except ImportError:
        return False
    return True


def memory_bytes(num_qubits: int, method: str) -> int:
    return (2 ** num_qubits) * 16 if method == "statevector" else (4 ** num_qubits) * 16


# ------------------------------------------------------------------------------------- validation
def validate_circuit(spec: Any, *, method: str = "statevector") -> dict:
    if not isinstance(spec, dict):
        raise CircuitValidationError("circuit must be a JSON object")
    extra = set(spec) - {"num_qubits", "gates", "measure"}
    if extra:
        raise CircuitValidationError(f"unsupported circuit keys (no executable/QASM upload): {sorted(extra)}")
    if method not in METHODS:
        raise CircuitValidationError(f"unsupported method {method!r}")
    n = spec.get("num_qubits")
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise CircuitValidationError("num_qubits must be a positive integer")
    if n > MAX_QUBITS[method]:
        raise CircuitValidationError(f"{n} qubits exceeds the {method} cap of {MAX_QUBITS[method]} "
                                     f"(would need {memory_bytes(n, method)} bytes)")
    gates = spec.get("gates", [])
    if not isinstance(gates, list) or len(gates) > MAX_GATES:
        raise CircuitValidationError(f"gates must be a list of at most {MAX_GATES} entries")

    def qubit(g: dict, key: str) -> int:
        q = g.get(key)
        if not isinstance(q, int) or isinstance(q, bool) or not 0 <= q < n:
            raise CircuitValidationError(f"gate {g.get('type')!r}: {key} must be a declared qubit index in [0,{n})")
        return q

    out: list[dict] = []
    measured = False
    for i, g in enumerate(gates):
        if not isinstance(g, dict) or not isinstance(g.get("type"), str):
            raise CircuitValidationError(f"gate #{i} must be an object with a string 'type'")
        t = g["type"].upper()
        if t in ("MEASURE", "M"):
            measured = True
            continue
        if measured:
            raise CircuitValidationError("measurement is only allowed at the end of the circuit")
        if t in SINGLE:
            allowed = {"type", "target"}
            out.append({"type": t, "target": qubit(g, "target")})
        elif t in ROTATION:
            allowed = {"type", "target", "theta"}
            theta = g.get("theta")
            if isinstance(theta, bool) or not isinstance(theta, (int, float)) or not math.isfinite(theta):
                raise CircuitValidationError(f"gate #{i} {t}: theta must be a finite number")
            out.append({"type": t, "target": qubit(g, "target"), "theta": float(theta)})
        elif t in TWO:
            allowed = {"type", "control", "target"}
            c, tg = qubit(g, "control"), qubit(g, "target")
            if c == tg:
                raise CircuitValidationError(f"gate #{i} {t}: control and target must differ")
            out.append({"type": t, "control": c, "target": tg})
        else:
            raise CircuitValidationError(f"unsupported gate or control-flow construct {g['type']!r}")
        if set(g) - allowed:
            raise CircuitValidationError(f"gate #{i} {t}: unexpected fields {sorted(set(g) - allowed)}")
    return {"num_qubits": n, "gates": out}


def compile_to_qiskit(spec: dict, *, method: str = "statevector", measure: bool = True):
    from qiskit import QuantumCircuit

    v = validate_circuit(spec, method=method)
    qc = QuantumCircuit(v["num_qubits"])
    for g in v["gates"]:
        t = g["type"]
        if t in SINGLE:
            getattr(qc, SINGLE[t])(g["target"])
        elif t in ROTATION:
            getattr(qc, ROTATION[t])(g["theta"], g["target"])
        else:
            getattr(qc, TWO[t])(g["control"], g["target"])
    if measure:
        qc.measure_all()
    return qc


# ------------------------------------------------------------------------------------- primitives
def _simulator(**opts):
    """Single construction point for Aer simulators (tests assert invalid input never reaches it)."""
    from qiskit_aer import AerSimulator

    return AerSimulator(**opts)


def _noise_model(noise_prob: float):
    from qiskit_aer.noise import NoiseModel, depolarizing_error

    model = NoiseModel()
    model.add_all_qubit_quantum_error(depolarizing_error(noise_prob, 1), ["h", "x", "y", "z", "s", "t", "rx", "ry", "rz"])
    model.add_all_qubit_quantum_error(depolarizing_error(noise_prob, 2), ["cx", "cz"])
    return model


def _backend_options(method: str, noise_prob: float, seed: int | None) -> dict:
    if not 0.0 <= noise_prob <= 1.0:
        raise CircuitValidationError("noise_prob must be in [0, 1]")
    if noise_prob and method != "density_matrix":
        raise CircuitValidationError("depolarizing noise requires method='density_matrix'")
    opts: dict[str, Any] = {"method": method}
    if noise_prob:
        opts["noise_model"] = _noise_model(noise_prob)
    if seed is not None:
        opts["seed_simulator"] = int(seed)
    return opts


def sample(spec: dict, *, shots: int = 1024, seed: int | None = 42, method: str = "statevector",
           noise_prob: float = 0.0) -> dict:
    """Run the circuit with Qiskit Aer SamplerV2; counts are q0-leftmost and sum to ``shots``."""
    from qiskit import transpile
    from qiskit_aer.primitives import SamplerV2

    if not isinstance(shots, int) or not 1 <= shots <= MAX_SHOTS:
        raise CircuitValidationError(f"shots must be an integer in [1, {MAX_SHOTS}]")
    v = validate_circuit(spec, method=method)
    qc = compile_to_qiskit(v, method=method)
    opts = _backend_options(method, noise_prob, seed)
    t0 = time.perf_counter()
    backend = _simulator(**opts)
    sampler = SamplerV2(options={"backend_options": opts})
    tqc = transpile(qc, backend, optimization_level=0, seed_transpiler=seed)
    job = sampler.run([tqc], shots=shots)
    raw = job.result()[0].data.meas.get_counts()
    counts = {k[::-1]: int(c) for k, c in sorted(raw.items(), key=lambda kv: kv[0][::-1])}
    # exact probabilities for the same circuit (noise-free statevector or density matrix with noise)
    probs = exact_probabilities(v, method=method, noise_prob=noise_prob)
    return {**LABELS, "backend": "qiskit-aer", "primitive": "SamplerV2", "method": method,
            "num_qubits": v["num_qubits"], "gate_count": len(v["gates"]), "shots": shots, "seed": seed,
            "endianness": "q0-leftmost", "counts": counts, "probabilities": probs,
            "noise_prob": noise_prob, "elapsed_s": time.perf_counter() - t0,
            "memory_bytes_estimate": memory_bytes(v["num_qubits"], method)}


def exact_probabilities(spec: dict, *, method: str = "statevector", noise_prob: float = 0.0) -> list[float]:
    """Exact basis-state probabilities, index i = q0-leftmost bitstring of i."""
    from qiskit import transpile

    v = validate_circuit(spec, method=method)
    qc = compile_to_qiskit(v, method=method, measure=False)
    n = v["num_qubits"]
    opts = _backend_options(method, noise_prob, None)
    backend = _simulator(**opts)
    if method == "statevector":
        qc.save_statevector()
        data = np.abs(np.asarray(backend.run(transpile(qc, backend, optimization_level=0)).result().get_statevector())) ** 2
    else:
        qc.save_density_matrix()
        data = np.real(np.diag(np.asarray(backend.run(transpile(qc, backend, optimization_level=0)).result().data()["density_matrix"])))
    out = [0.0] * (2 ** n)
    for idx, p in enumerate(data):  # Qiskit index: bit k = qubit k (little-endian)
        bits = format(idx, f"0{n}b")[::-1]  # q0-leftmost
        out[int(bits, 2)] = float(p)
    return out


def _pauli_op(observable: str | list, n: int):
    from qiskit.quantum_info import SparsePauliOp

    terms = [(observable, 1.0)] if isinstance(observable, str) else observable
    if not isinstance(terms, list) or not 1 <= len(terms) <= MAX_PAULI_TERMS:
        raise CircuitValidationError(f"observable must be a Pauli string or 1..{MAX_PAULI_TERMS} [label, coeff] terms")
    labels = []
    for term in terms:
        if not (isinstance(term, (list, tuple)) and len(term) == 2):
            raise CircuitValidationError("each observable term must be [pauli_label, real_coefficient]")
        label, coeff = term
        if not isinstance(label, str) or len(label) != n or set(label.upper()) - set("IXYZ"):
            raise CircuitValidationError(f"Pauli label {label!r} must have length {n} over I/X/Y/Z")
        if isinstance(coeff, bool) or not isinstance(coeff, (int, float)) or not math.isfinite(coeff):
            raise CircuitValidationError("Pauli coefficients must be finite real numbers (Hermitian observable)")
        labels.append((label.upper()[::-1], float(coeff)))  # q0-leftmost -> Qiskit little-endian
    return SparsePauliOp.from_list(labels)


def expectation(spec: dict, observable: str | list, *, method: str = "statevector", noise_prob: float = 0.0,
                seed: int | None = 42) -> dict:
    """<psi|O|psi> for a bounded real-weighted Pauli sum using Qiskit Aer EstimatorV2 (exact, no shots)."""
    from qiskit_aer.primitives import EstimatorV2

    v = validate_circuit(spec, method=method)
    qc = compile_to_qiskit(v, method=method, measure=False)
    op = _pauli_op(observable, v["num_qubits"])
    opts = _backend_options(method, noise_prob, seed)
    est = EstimatorV2(options={"backend_options": opts, "default_precision": 0.0})
    value = float(np.real(est.run([(qc, op)]).result()[0].data.evs))
    return {**LABELS, "backend": "qiskit-aer", "primitive": "EstimatorV2", "method": method,
            "observable": observable, "expectation": value}


# ------------------------------------------------------------------------------------- QAOA
def _cut(bs: str, edges: list[tuple[int, int]]) -> int:
    return sum(1 for u, v in edges if bs[u] != bs[v])


def qaoa_maxcut(edges: list, num_nodes: int, *, p: int = 1, max_evaluations: int = 50, shots: int = 1024,
                seed: int = 42, initial_point: list[float] | None = None) -> dict:
    """Seeded QAOA MaxCut using Qiskit primitives + SciPy COBYLA, compared with exhaustive search."""
    from qiskit import transpile
    from qiskit.circuit.library import QAOAAnsatz
    from qiskit.quantum_info import SparsePauliOp
    from qiskit_aer.primitives import EstimatorV2, SamplerV2
    from scipy.optimize import minimize

    if not isinstance(num_nodes, int) or not 2 <= num_nodes <= 12:
        raise CircuitValidationError("MaxCut experiment is bounded to 2..12 vertices")
    if not isinstance(p, int) or not 1 <= p <= 2:
        raise CircuitValidationError("QAOA depth p must be 1 or 2")
    if not isinstance(max_evaluations, int) or not 1 <= max_evaluations <= 50:
        raise CircuitValidationError("max_evaluations must be in [1, 50]")
    clean: list[tuple[int, int]] = []
    for e in edges:
        if not (isinstance(e, (list, tuple)) and len(e) == 2 and all(isinstance(x, int) and not isinstance(x, bool)
                                                                       and 0 <= x < num_nodes for x in e)
                and e[0] != e[1]):
            raise CircuitValidationError(f"invalid edge {e!r}")
        clean.append((int(e[0]), int(e[1])))
    if not clean:
        raise CircuitValidationError("graph has no edges")

    failures: list[str] = []
    # cost Hamiltonian: C = sum 0.5 (I - Z_u Z_v); we maximise <C> by minimising -<C>
    zz = []
    for u, v in clean:
        label = ["I"] * num_nodes
        label[u] = label[v] = "Z"
        zz.append(("".join(label)[::-1], -0.5))
    cost_zz = SparsePauliOp.from_list(zz)
    offset = 0.5 * len(clean)
    backend = _simulator(method="statevector", seed_simulator=seed)
    ansatz = transpile(QAOAAnsatz(cost_zz, reps=p), backend, optimization_level=0, seed_transpiler=seed)
    est = EstimatorV2(options={"backend_options": {"method": "statevector", "seed_simulator": seed},
                               "default_precision": 0.0})
    evaluations = 0
    history: list[float] = []
    best: dict[str, Any] = {"x": None, "val": -math.inf}

    class _BudgetExhausted(Exception):
        pass

    def objective(x: np.ndarray) -> float:
        nonlocal evaluations
        if evaluations >= max_evaluations:  # hard cap: COBYLA's maxiter alone may overshoot
            raise _BudgetExhausted
        evaluations += 1
        val = float(np.real(est.run([(ansatz, cost_zz, x)]).result()[0].data.evs)) + offset
        history.append(val)
        if val > best["val"]:
            best.update(x=np.array(x, dtype=float), val=val)
        return -val

    rng = np.random.default_rng(seed)
    x0 = np.asarray(initial_point if initial_point is not None else rng.uniform(0, np.pi, ansatz.num_parameters))
    t0 = time.perf_counter()
    try:
        opt = minimize(objective, x0, method="COBYLA", options={"maxiter": max_evaluations, "rhobeg": 0.5})
        if not opt.success:
            failures.append(f"COBYLA: {opt.message}")
    except _BudgetExhausted:
        failures.append(f"COBYLA: objective evaluation budget of {max_evaluations} exhausted before convergence")
    best_x = best["x"]
    measured = ansatz.assign_parameters(best_x)
    measured.measure_all()
    sampler = SamplerV2(options={"backend_options": {"method": "statevector", "seed_simulator": seed}})
    raw = sampler.run([transpile(measured, backend, optimization_level=1, seed_transpiler=seed)],
                      shots=shots).result()[0].data.meas.get_counts()
    counts = {k[::-1]: int(c) for k, c in raw.items()}
    qaoa_time = time.perf_counter() - t0
    best_bs = max(counts, key=lambda b: (_cut(b, clean), counts[b]))
    best_cut = _cut(best_bs, clean)

    t1 = time.perf_counter()
    classical_best, classical_bs = -1, ""
    for cand in itertools.product("01", repeat=num_nodes):
        s = "".join(cand)
        c = _cut(s, clean)
        if c > classical_best:
            classical_best, classical_bs = c, s
    classical_time = time.perf_counter() - t1
    if best_cut < classical_best:
        failures.append(f"QAOA best sampled cut {best_cut} < classical optimum {classical_best}")
    ratio = best_cut / classical_best if classical_best else 1.0
    expected_cut = history[-1] if history else None
    return {
        **LABELS, "backend": "qiskit-aer", "primitives": ["EstimatorV2", "SamplerV2"], "optimizer": "scipy.COBYLA",
        "num_nodes": num_nodes, "edge_count": len(clean), "qaoa_p": p, "seed": seed, "shots": shots,
        "objective_evaluations": evaluations, "max_evaluations": max_evaluations,
        "optimal_parameters": [float(x) for x in best_x], "expected_cut": float(best["val"]),
        "last_expected_cut": expected_cut, "objective_history": history,
        "best_sampled_cut": best_cut, "best_sampled_bitstring": best_bs, "endianness": "q0-leftmost",
        "classical_optimal_cut": classical_best, "classical_optimal_bitstring": classical_bs,
        "classical_optimum": {"max_cut_value": classical_best, "bitstring": classical_bs},
        "qaoa_best_cut": {"cut_value": best_cut, "bitstring": best_bs},
        "approximation_ratio": ratio, "qaoa_success_ratio": ratio,
        "comparison": {"qaoa_wall_time_s": qaoa_time, "classical_wall_time_s": classical_time,
                       "qaoa_memory_bytes_estimate": memory_bytes(num_nodes, "statevector"),
                       "classical_states_enumerated": 2 ** num_nodes,
                       "advantage_claimed": False,
                       "note": "simulated QAOA on a classical CPU; no quantum advantage is claimed"},
        "failures": failures, "counts": counts,
    }
