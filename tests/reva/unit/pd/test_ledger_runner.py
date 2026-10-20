"""FT-F04: the REVA ledger records only real test runs and never auto-closes."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

from reva.kernel.authority import Depth
from reva.pd.bindings import Binding, OwnerRef, VerifierSpec
from reva.pd.obligations import Obligation
from reva.pd.runs import ParsedTest, RunRecord

ROOT = Path(__file__).resolve().parents[4]
pytestmark = pytest.mark.reva_depth("unit")


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / "reva" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runner = _load("run_reva_ledger")


def _run(outcome="passed", keys=("OBL-X",), hits=None, exit_code=0):
    test = ParsedTest("tests/reva/unit/test_x.py::test_x", outcome, 1, list(keys), ["positive"],
                      {"dig": 3} if hits is None else hits)
    return RunRecord(run_id="vr1_x", verifier_id="pytest-tests-reva", binding_digest="", repo_id="eiop",
                     commit="c1", tree_digest="t", clean=True, environment={}, profile="unit", depth=Depth.UNIT,
                     network="host", argv=["pytest"], started_at="s", finished_at="f", exit_code=exit_code,
                     timed_out=False, lineage={}, artifacts=[], tests=[test], reruns=1)


OB = Obligation(key="OBL-X", requirement_id="REQ-X", title="x", case_kinds=["positive"])
BINDING = Binding(obligation_key="OBL-X", owners=[OwnerRef(repo_id="eiop", path="nope.py", symbol="f",
                                                           owner_digest="dig")],
                  verifier=VerifierSpec(verifier_id="pytest-tests-reva", argv=["pytest"]))
REVIEW = {"OBL-X": {"obligation_key": "OBL-X", "reviewer": "Jane Reviewer", "reviewed_at": "2026-10-20"}}


def test_reviews_by_automation_or_without_date_are_ignored(tmp_path):
    path = tmp_path / "reviews.yaml"
    path.write_text(
        "- {obligation_key: OBL-A, reviewer: agent, reviewed_at: '2026-10-20'}\n"
        "- {obligation_key: OBL-B, reviewer: lead_architect, reviewed_at: '2026-10-20'}\n"
        "- {obligation_key: OBL-C, reviewer: Jane Reviewer}\n"
        "- {obligation_key: OBL-D, reviewer: Jane Reviewer, reviewed_at: '2026-10-20'}\n", encoding="utf-8")
    assert list(runner.load_reviews(path)) == ["OBL-D"]
    assert runner.load_reviews(tmp_path / "missing.yaml") == {}


def test_obligation_stays_open_without_review_binding_or_mutation_evidence():
    (no_review,) = runner.evaluate([OB], [BINDING], {}, [_run()], "c1", {"dig": 0.9})
    assert no_review.outcome == "open" and "OBLIGATION_UNREVIEWED" in no_review.reasons
    (no_binding,) = runner.evaluate([OB], [], REVIEW, [_run()], "c1", {"dig": 0.9})
    assert no_binding.outcome == "open" and "BINDING_INVALID" in no_binding.reasons
    (no_mutation,) = runner.evaluate([OB], [BINDING], REVIEW, [_run()], "c1", {})
    assert no_mutation.outcome == "open" and "AG04_MUTATION_SCORE_MISSING" in no_mutation.reasons
    (no_run,) = runner.evaluate([OB], [BINDING], REVIEW, [], "c1", {"dig": 0.9})
    assert no_run.outcome == "unknown"
    (skipped,) = runner.evaluate([OB], [BINDING], REVIEW, [_run(outcome="skipped")], "c1", {"dig": 0.9})
    assert skipped.outcome == "open" and "AG13_NO_COUNTED_TESTS" in skipped.reasons
    (failed,) = runner.evaluate([OB], [BINDING], REVIEW, [_run(outcome="failed")], "c1", {"dig": 0.9})
    assert failed.outcome == "failed"


def test_obligation_closes_only_with_complete_real_evidence():
    (decision,) = runner.evaluate([OB], [BINDING], REVIEW, [_run()], "c1", {"dig": 0.9})
    assert decision.outcome == "closed", decision.reasons
    assert runner.assert_no_unearned_closure([decision], [_run()]) == []
    assert runner.assert_no_unearned_closure([decision], [_run(exit_code=1)]) == ["OBL-X"]
    assert runner.assert_no_unearned_closure([decision], [_run(keys=())]) == ["OBL-X"]


def test_dependencies_are_evaluated_first_and_block():
    child = Obligation(key="OBL-Y", requirement_id="REQ-Y", title="y", dependencies=["OBL-X"])
    decisions = {d.obligation_key: d for d in runner.evaluate([child, OB], [], {}, [_run()], "c1", {})}
    assert decisions["OBL-X"].outcome == "open"
    assert decisions["OBL-Y"].outcome == "blocked" and "DEPENDENCY_OPEN" in decisions["OBL-Y"].reasons


def test_retired_self_certifying_builder_refuses_to_run():
    result = subprocess.run([sys.executable, str(ROOT / "scripts/reva/build_reva_ledger.py")],
                            capture_output=True, text=True, cwd=ROOT, timeout=60)
    assert result.returncode == 2
    assert "run_reva_ledger.py" in result.stderr


def test_committed_obligations_carry_no_fabricated_reviews():
    text = (ROOT / "docs/reva/obligations/reva.yaml").read_text(encoding="utf-8")
    assert "reviewed_warrant_id: wr1_" not in text


def test_committed_ledger_is_from_a_real_run_and_closes_nothing_unearned():
    import json

    ledger = json.loads((ROOT / "docs/reva/reva-ledger.json").read_text(encoding="utf-8"))
    evidence = ledger.get("evidence", {})
    assert evidence.get("source", "").startswith("real pytest run")
    assert evidence["tests"] > 0
    marked = set(evidence["obligations_with_marked_tests"])
    closed = {c["obligation_key"] for c in ledger["closures"] if c["outcome"] == "closed"}
    assert closed <= marked
    if evidence["human_reviews"] == 0:
        assert closed == set()
