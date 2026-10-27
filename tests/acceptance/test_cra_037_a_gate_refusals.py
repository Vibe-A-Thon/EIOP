"""CRA-037.A: the evidence gate refuses acceptance when a run used memory instead of the production
backend, when a negative case failed, and when a sealed receipt was tampered with.

Negative cases are executed for real in the test (their outcome is observed, not typed in), and the
backend name is read from the store object the run actually used.
"""

from __future__ import annotations

import copy

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.qa.verification_gate import (
    EvidenceVerificationGate,
    GateRefusalError,
    receipt_digest,
    seal_receipt,
)

pytestmark = pytest.mark.req("CRA-037")


def _backend_of(store) -> str:
    return "memory" if isinstance(store, MemoryGraphStore) else type(store).__name__.lower()


def _run_negative_case(case_id: str, attempt) -> dict:
    """Executes ``attempt``; a correct system refuses it (raises). Returns the observed outcome."""
    try:
        attempt()
    except (GateRefusalError, PermissionError, ValueError):
        return {"id": case_id, "expected": "refused", "observed": "refused"}
    return {"id": case_id, "expected": "refused", "observed": "accepted"}


def _receipt(**over) -> dict:
    r = {
        "receipt_id": "rcpt-037a",
        "requirement_clause": "CRA-037.A",
        "state_claimed": "ACCEPTED",
        "scope_label": "integration",
        "source_unchanged_during_run": True,
        "artifact_digest": "a" * 64,
        "environment": {"backend": "postgresql", "required_backend": "postgresql"},
        "execution": {"exit_code": 0},
        "results": {"tests_total": 4, "tests_failed": 0, "tests_errors": 0, "tests_skipped": 0, "tests_passed": 4},
        "negative_cases": [],
    }
    r.update(over)
    return r


@pytest.fixture
def gate():
    return EvidenceVerificationGate()


@pytest.fixture
def real_negative(gate):
    skipped = _receipt(results={"tests_total": 1, "tests_failed": 0, "tests_errors": 0, "tests_skipped": 1})
    return _run_negative_case("skip-must-be-refused", lambda: gate.verify_receipt(skipped))


def test_sealed_production_receipt_with_passing_negative_case_is_accepted(gate, real_negative):
    assert real_negative["observed"] == "refused"
    receipt = seal_receipt(_receipt(negative_cases=[real_negative]))
    assert gate.verify_receipt(receipt, expected_artifact_digest="a" * 64) is True


def test_run_against_memory_instead_of_production_backend_is_refused(gate, real_negative):
    store = MemoryGraphStore()
    store.upsert_vertex("WorkItem", {"canonical_id": "wi:1"})
    env = {"backend": _backend_of(store), "required_backend": "postgresql"}
    receipt = seal_receipt(_receipt(environment=env, negative_cases=[real_negative]))
    with pytest.raises(GateRefusalError, match="non-production backend 'memory'"):
        gate.verify_receipt(receipt)


def test_memory_backend_without_required_backend_still_refused_for_integration_scope(gate, real_negative):
    receipt = seal_receipt(_receipt(environment={"backend": "memory"}, negative_cases=[real_negative]))
    with pytest.raises(GateRefusalError, match="non-production backend"):
        gate.verify_receipt(receipt)


def test_wrong_production_backend_is_refused(gate, real_negative):
    env = {"backend": "neo4j", "required_backend": "postgresql"}
    with pytest.raises(GateRefusalError, match="requires 'postgresql'"):
        gate.verify_receipt(seal_receipt(_receipt(environment=env, negative_cases=[real_negative])))


def test_memory_backend_allowed_for_unit_scope_but_never_accepted(gate):
    unit = _receipt(state_claimed="VERIFIED", scope_label="unit", environment={"backend": "memory"})
    assert gate.verify_receipt(unit) is True
    with pytest.raises(GateRefusalError):
        gate.verify_receipt(seal_receipt({**unit, "state_claimed": "ACCEPTED"}))


def test_failing_negative_case_is_refused(gate):
    def lenient_checker():  # a broken implementation that lets an unauthorised write through
        return "written"

    failed = _run_negative_case("unauthorised-write-must-be-refused", lenient_checker)
    assert failed["observed"] == "accepted"
    receipt = seal_receipt(_receipt(negative_cases=[failed]))
    with pytest.raises(GateRefusalError, match="negative case 'unauthorised-write-must-be-refused'"):
        gate.verify_receipt(receipt)


def test_accepted_without_negative_cases_is_refused(gate):
    with pytest.raises(GateRefusalError, match="at least one executed negative case"):
        gate.verify_receipt(seal_receipt(_receipt(negative_cases=[])))


def test_tampered_sealed_receipt_is_refused(gate, real_negative):
    receipt = seal_receipt(_receipt(negative_cases=[real_negative]))
    tampered = copy.deepcopy(receipt)
    tampered["results"]["tests_passed"] = 400
    tampered["results"]["tests_total"] = 400
    assert receipt_digest(tampered) != tampered["receipt_digest"]
    with pytest.raises(GateRefusalError, match="tampered"):
        gate.verify_receipt(tampered)


def test_unsealed_accepted_receipt_is_refused(gate, real_negative):
    with pytest.raises(GateRefusalError, match="receipt_digest"):
        gate.verify_receipt(_receipt(negative_cases=[real_negative]))


def test_each_refusal_is_independent(gate, real_negative):
    """Each defect alone is enough: start from an accepted receipt and break one field at a time."""
    good = _receipt(negative_cases=[real_negative])
    assert gate.verify_receipt(seal_receipt(good)) is True
    breakers = {
        "memory": lambda r: r["environment"].update(backend="memory"),
        "negative": lambda r: r["negative_cases"][0].update(observed="accepted"),
        "skip": lambda r: r["results"].update(tests_skipped=1),
        "stale": lambda r: r.update(artifact_digest="b" * 64),
        "source_edit": lambda r: r.update(source_unchanged_during_run=False),
    }
    for name, breaker in breakers.items():
        bad = copy.deepcopy(good)
        breaker(bad)
        with pytest.raises(GateRefusalError):
            gate.verify_receipt(seal_receipt(bad), expected_artifact_digest="a" * 64)
        assert gate.verify_receipt(seal_receipt(good), expected_artifact_digest="a" * 64) is True, name
