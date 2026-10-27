"""CRA-036.A negative gates: a wrong answer, leakage, a required timeout or a missing artifact each fail
the corresponding gate even when median latency is fast.

The expected answers are written here by hand (independent oracle), not derived from the code under test.
Each negative case breaks exactly one thing and checks that only that gate fails and the report is REJECTED.
"""

from __future__ import annotations

import hashlib
import json
import time

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.qualification.harness import QualificationEngine, ScaleTier, WorkloadManifest

pytestmark = pytest.mark.req("CRA-036")

FAST_MEDIAN_MS = 5.0


@pytest.fixture
def store():
    s = MemoryGraphStore()
    for tenant, n in (("alpha", 20), ("beta", 5)):
        for i in range(n):
            s.upsert_vertex("WorkItem", {"canonical_id": f"{tenant}:wi:{i}", "tenant_id": tenant, "name": f"Task {i}"})
    return s


def _engine() -> QualificationEngine:
    return QualificationEngine(WorkloadManifest.create_default(tier=ScaleTier.P0, seed=7))


def _alpha_names(store):
    return sorted(v["properties"]["name"] for v in store.find_vertices("WorkItem", {"tenant_id": "alpha"}, limit=1000))


# Hand-written oracle: tenant alpha has exactly Task 0 .. Task 19.
ALPHA_ORACLE = sorted(f"Task {i}" for i in range(20))


def _other_tenant_rows(rows_tenant):
    def probe(_result):
        return [t for t in rows_tenant() if t != "alpha"]
    return probe


def _failed(report):
    return {g for g, v in report["gates"].items() if not v["passed"]}


def test_correct_fast_run_qualifies(store):
    engine = _engine()
    res = engine.run_gated_trials("alpha_list", lambda: _alpha_names(store), ALPHA_ORACLE,
                                  iterations_per_trial=5, required_timeout_ms=1_000,
                                  leakage_probe=lambda rows: [r for r in rows if not r.startswith("Task ")])
    report = engine.generate_qualification_report()
    assert report["status"] == "QUALIFIED" and _failed(report) == set()
    assert res["oracle_verified"] and res["measured_trials"] == 3 and res["failures"] == []
    json.dumps(report)  # machine-readable


def test_wrong_answer_fails_correctness_even_when_median_is_fast(store):
    engine = _engine()

    def buggy():  # drops one row: a plausible off-by-one in a page boundary
        return _alpha_names(store)[:-1]

    res = engine.run_gated_trials("alpha_list", buggy, ALPHA_ORACLE, iterations_per_trial=5)
    report = engine.generate_qualification_report()
    assert res["median_p50_ms"] < FAST_MEDIAN_MS
    assert report["status"] == "REJECTED" and _failed(report) == {"correctness"}
    assert report["gates"]["correctness"]["failure_count"] == 15
    assert res["oracle_verified"] is False


def test_operation_error_is_a_correctness_failure_not_a_pass(store):
    engine = _engine()

    def broken():
        raise RuntimeError("backend unavailable")

    engine.run_gated_trials("alpha_list", broken, ALPHA_ORACLE, iterations_per_trial=2)
    report = engine.generate_qualification_report()
    assert report["status"] == "REJECTED"
    assert "correctness" in _failed(report) and "artifacts" in _failed(report)  # no measured trials either


def test_cross_tenant_leakage_fails_leakage_gate_even_with_correct_answer(store):
    engine = _engine()
    seen_tenants: list[str] = []

    def leaky():  # right names for alpha, but the read path also touched beta rows
        rows = store.find_vertices("WorkItem", limit=1000)
        seen_tenants[:] = [r["properties"]["tenant_id"] for r in rows]
        return sorted(r["properties"]["name"] for r in rows if r["properties"]["tenant_id"] == "alpha")

    res = engine.run_gated_trials("alpha_list", leaky, ALPHA_ORACLE, iterations_per_trial=4,
                                  leakage_probe=_other_tenant_rows(lambda: seen_tenants))
    report = engine.generate_qualification_report()
    assert res["median_p50_ms"] < FAST_MEDIAN_MS and res["oracle_verified"] is True
    assert report["status"] == "REJECTED" and _failed(report) == {"leakage"}
    assert report["gates"]["leakage"]["failures"][0]["detail"] == "5 leaked item(s)"


def test_required_timeout_exceeded_fails_timeout_gate(store):
    engine = _engine()
    calls = {"n": 0}

    def mostly_fast():  # 1 slow call in 10: the median stays fast, the required deadline is still missed
        calls["n"] += 1
        if calls["n"] % 10 == 0:
            time.sleep(0.06)
        return _alpha_names(store)

    res = engine.run_gated_trials("alpha_list", mostly_fast, ALPHA_ORACLE, iterations_per_trial=10,
                                  required_timeout_ms=50)
    report = engine.generate_qualification_report()
    assert res["median_p50_ms"] < FAST_MEDIAN_MS
    assert report["status"] == "REJECTED" and _failed(report) == {"timeout"}
    assert report["gates"]["timeout"]["failure_count"] == 3


def test_operation_raising_timeout_fails_timeout_gate(store):
    engine = _engine()
    calls = {"n": 0}

    def cancelled_once():
        calls["n"] += 1
        if calls["n"] == 2:
            raise TimeoutError("query cancelled at deadline")
        return _alpha_names(store)

    engine.run_gated_trials("alpha_list", cancelled_once, ALPHA_ORACLE, iterations_per_trial=3)
    report = engine.generate_qualification_report()
    assert _failed(report) == {"timeout"} and report["status"] == "REJECTED"


def test_missing_artifact_fails_artifacts_gate(store, tmp_path):
    engine = _engine()
    engine.run_gated_trials("alpha_list", lambda: _alpha_names(store), ALPHA_ORACLE, iterations_per_trial=3)
    engine.require_artifact(str(tmp_path / "raw-results.json"))
    report = engine.generate_qualification_report()
    assert report["status"] == "REJECTED" and _failed(report) == {"artifacts"}
    assert "required artifact missing" in report["gates"]["artifacts"]["failures"][0]["detail"]


def test_tampered_artifact_fails_and_intact_one_passes(store, tmp_path):
    raw = tmp_path / "raw-results.json"
    raw.write_text('{"rows": 20}', encoding="utf-8")
    good = hashlib.sha256(raw.read_bytes()).hexdigest()

    engine = _engine()
    engine.run_gated_trials("alpha_list", lambda: _alpha_names(store), ALPHA_ORACLE, iterations_per_trial=3)
    engine.require_artifact(str(raw), good)
    assert engine.generate_qualification_report()["status"] == "QUALIFIED"

    raw.write_text('{"rows": 21}', encoding="utf-8")
    report = engine.generate_qualification_report()
    assert report["status"] == "REJECTED" and _failed(report) == {"artifacts"}
    assert "digest mismatch" in report["gates"]["artifacts"]["failures"][0]["detail"]


def test_too_few_trials_and_no_results_fail_artifacts_gate(store):
    engine = _engine()
    assert engine.generate_qualification_report()["status"] == "REJECTED"  # nothing measured
    engine.run_gated_trials("alpha_list", lambda: _alpha_names(store), ALPHA_ORACLE,
                            trials_count=2, iterations_per_trial=3)
    report = engine.generate_qualification_report()
    assert _failed(report) == {"artifacts"}
    assert "at least 3 required" in report["gates"]["artifacts"]["failures"][0]["detail"]
