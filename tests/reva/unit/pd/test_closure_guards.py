"""Boundary tests for every closure check (kills the mutants the reva-mutation lane found)."""

from __future__ import annotations

import pytest

from reva.kernel.authority import Depth
from reva.pd.bindings import Binding, OwnerRef, PerformanceBudget, VerifierSpec
from reva.pd.closure import ClosureContext, evaluate_closure
from reva.pd.obligations import Obligation
from reva.pd.runs import ParsedTest, RunRecord

pytestmark = pytest.mark.reva_depth("unit")


def _ob(**kw):
    base = dict(key="OBL-G", requirement_id="R", title="g", case_kinds=["positive"], reviewed_warrant_id="review:jane")
    base.update(kw)
    return Obligation(**base)


def _binding(language="python", digest="d1", **kw):
    return Binding(obligation_key="OBL-G", owners=[OwnerRef(repo_id="r", path="m.py", symbol="f", language=language,
                                                            owner_digest=digest)],
                   verifier=VerifierSpec(verifier_id="v", argv=["pytest"]), **kw)


def _run(tests=None, depth=Depth.UNIT, commit="c1"):
    tests = tests if tests is not None else [ParsedTest("t", "passed", 1, ["OBL-G"], ["positive"], {"d1": 2})]
    return RunRecord(run_id="vr1_g", verifier_id="v", binding_digest="", repo_id="r", commit=commit, tree_digest="t",
                     clean=True, environment={}, profile="unit", depth=depth, network="none", argv=["pytest"],
                     started_at="s", finished_at="f", exit_code=0, timed_out=False, lineage={}, artifacts=[],
                     tests=tests, reruns=1)


def _eval(ob=None, binding=None, runs=None, **kw):
    kw.setdefault("mutation_scores", {"d1": 0.9})
    return evaluate_closure(ClosureContext(obligation=ob or _ob(), binding=binding if binding is not None else _binding(),
                                           commit="c1", runs=runs if runs is not None else [_run()], **kw))


def test_baseline_closes():
    assert _eval().outcome == "closed"


@pytest.mark.parametrize("waiver,reviewed", [
    ({"target": "OBL-G", "kind": "defer"}, True),
    ({"target": "OBL-G", "kind": "out_of_scope"}, True),
    ({"target": "OBL-G", "kind": "accept_risk"}, False),
    ({"target": "OBL-OTHER", "kind": "defer"}, False),
])
def test_waiver_only_substitutes_review_for_its_own_target_and_kinds(waiver, reviewed):
    decision = _eval(ob=_ob(reviewed_warrant_id=None), waivers=[waiver])
    assert ("OBLIGATION_UNREVIEWED" not in decision.reasons) is reviewed


@pytest.mark.parametrize("dep_outcome,blocked", [("closed", False), ("open", True), ("stale", True)])
def test_dependencies_must_be_closed(dep_outcome, blocked):
    decision = _eval(ob=_ob(dependencies=["OBL-D"]), dependency_outcomes={"OBL-D": dep_outcome})
    assert ("DEPENDENCY_OPEN" in decision.reasons) is blocked


@pytest.mark.parametrize("status,blocks", [("open", True), ("investigating", True), ("blocked", True),
                                           ("contradicted", True), ("closed", False), ("waived", False)])
def test_gap_status_blocking(status, blocks):
    decision = _eval(linked_gaps=[{"gap_id": "g1", "status": status}])
    assert ("CLOSURE_BLOCKED_GAP" in decision.reasons) is blocks


@pytest.mark.parametrize("status,blocks", [("open", True), ("resolved", False)])
def test_contradiction_status_blocking(status, blocks):
    decision = _eval(linked_contradictions=[{"contradiction_id": "c", "status": status}])
    assert ("CLOSURE_BLOCKED_CONTRADICTION" in decision.reasons) is blocks


def test_owner_without_digest_counts_tests_without_coverage():
    no_cov = [ParsedTest("t", "passed", 1, ["OBL-G"], ["positive"], {})]
    assert _eval(binding=_binding(digest=None), runs=[_run(no_cov)]).outcome == "closed"
    assert _eval(binding=_binding(), runs=[_run(no_cov)]).outcome == "open"


@pytest.mark.parametrize("score,closed", [(0.70, True), (0.69, False)])
def test_mutation_threshold_is_inclusive(score, closed):
    decision = _eval(mutation_scores={"d1": score}, min_mutation_score=0.70)
    assert (decision.outcome == "closed") is closed
    if not closed:
        assert "AG04_MUTATION_SCORE_LOW" in decision.reasons


def test_mutation_applies_only_to_python_owners_with_digest():
    assert _eval(binding=_binding(language="java"), mutation_scores={}).outcome == "closed"
    assert _eval(binding=_binding(digest=None), mutation_scores={}).outcome == "closed"


def test_mutation_not_required_above_component_depth():
    ob = _ob(depth=Depth.INTEGRATION)
    assert _eval(ob=ob, runs=[_run(depth=Depth.INTEGRATION)], mutation_scores={}).outcome == "closed"


def test_case_kinds_must_all_be_covered():
    decision = _eval(ob=_ob(case_kinds=["positive", "negative"]))
    assert "CASE_KIND_UNCOVERED" in decision.reasons
    assert any(c.check == "9_case_kinds" and c.status == "pass" for c in _eval().checks)


def test_performance_check_recorded_only_with_budget_and_case_kind():
    tests = [ParsedTest("t", "passed", 1, ["OBL-G"], ["positive", "performance"], {"d1": 1})]
    ob = _ob(case_kinds=["positive", "performance"])
    with_budget = _eval(ob=ob, binding=_binding(performance_budget=PerformanceBudget(threshold=5)), runs=[_run(tests)])
    assert any(c.check == "10_performance_budget" for c in with_budget.checks)
    without_kind = _eval(binding=_binding(performance_budget=PerformanceBudget(threshold=5)))
    assert not any(c.check == "10_performance_budget" for c in without_kind.checks)
    without_budget = _eval(ob=ob, runs=[_run(tests)])
    assert not any(c.check == "10_performance_budget" for c in without_budget.checks)


@pytest.mark.parametrize("journey_runs,missing", [
    ([], True),
    ([{"journey_id": "RJ-X", "outcome": "failed"}], True),
    ([{"journey_id": "RJ-Y", "outcome": "passed"}], True),
    ([{"journey_id": "RJ-X", "outcome": "passed"}], False),
])
def test_acceptance_obligations_need_a_passing_journey(journey_runs, missing):
    ob = _ob(depth=Depth.ACCEPTANCE)
    decision = _eval(ob=ob, binding=_binding(journeys=["RJ-X"]), runs=[_run(depth=Depth.ACCEPTANCE)],
                     journeys_runs=journey_runs)
    assert ("JOURNEY_MISSING" in decision.reasons) is missing
    assert any(c.check == "11_acceptance_journeys" for c in decision.checks)


def test_journeys_ignored_below_acceptance_depth():
    decision = _eval(binding=_binding(journeys=["RJ-X"]))
    assert not any(c.check == "11_acceptance_journeys" for c in decision.checks)
