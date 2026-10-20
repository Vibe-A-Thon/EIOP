"""
Unit Tests for Graffin Core: Constitution, Kill Switch, Autonomy, and Evaluators (GRF-REQ-*).
"""

import os
import pytest

from reva.agents.graffin.constitution import ConstitutionVerifier, ConstitutionTamperedError
from reva.agents.graffin.kill_switch import KillSwitchController
from reva.agents.graffin.autonomy import (
    AutonomyStateMachine,
    AutonomyLevel,
    RiskTier,
    ConsequenceBudget,
    BudgetDepletedError,
    AuthorizationRequiredError,
)
from reva.agents.graffin.evaluators import CalibrationJudge, RegressionSentinel

pytestmark = pytest.mark.reva_depth("unit")


def test_constitution_verifier():
    verifier = ConstitutionVerifier()
    digest = verifier.compute_canonical_hash()
    assert digest.startswith("con1_")
    assert len(digest) == 5 + 64

    # Verify matching hash passes
    verified = verifier.verify_or_fail()
    assert verified == digest

    # Verify tampered hash raises ConstitutionTamperedError
    tampered_verifier = ConstitutionVerifier(expected_hash="con1_" + "0" * 64)
    with pytest.raises(ConstitutionTamperedError):
        tampered_verifier.verify_or_fail()


def test_kill_switch_controller():
    controller = KillSwitchController(emergency_token="valid_secret_token")
    assert not controller.is_killed

    # Feed watchdog
    controller.heartbeat()

    # Trigger emergency kill via REST channel
    assert not controller.trigger_kill(channel="REST", reason="test", token="wrong_token")
    assert not controller.is_killed

    assert controller.trigger_kill(channel="REST", reason="emergency test", token="valid_secret_token")
    assert controller.is_killed
    assert controller.kill_metadata["channel"] == "REST"
    assert controller.kill_metadata["reason"] == "emergency test"


def test_autonomy_state_machine_and_budget():
    budget = ConsequenceBudget(total_budget=100.0)
    machine = AutonomyStateMachine(initial_level=AutonomyLevel.L3_CONDITIONAL, budget=budget)

    # R1 operation (costs 1.0)
    rec1 = machine.authorize_and_execute(RiskTier.R1_READ_ONLY, "scan_files")
    assert rec1["remaining_budget"] == 99.0

    # R2 operation (costs 10.0)
    rec2 = machine.authorize_and_execute(RiskTier.R2_LOCAL_MUTATION, "write_cache")
    assert rec2["remaining_budget"] == 89.0

    # R3 requires dual keys
    with pytest.raises(AuthorizationRequiredError):
        machine.authorize_and_execute(RiskTier.R3_GRAPH_MUTATION, "alter_graph")

    # With dual keys (costs 50.0)
    rec3 = machine.authorize_and_execute(
        RiskTier.R3_GRAPH_MUTATION,
        "alter_graph",
        dual_keys=["key_operator_1", "key_auditor_2"],
    )
    assert rec3["remaining_budget"] == 39.0

    # Exceeding budget raises BudgetDepletedError (R3 costs 50, but only 39 remain)
    with pytest.raises(BudgetDepletedError):
        machine.authorize_and_execute(
            RiskTier.R3_GRAPH_MUTATION,
            "another_alteration",
            dual_keys=["key_operator_1", "key_auditor_2"],
        )


def test_evaluators_calibration_and_regression():
    judge = CalibrationJudge(num_bins=5)
    # Well-calibrated predictions: prob matches outcome
    preds = [(0.1, 0), (0.2, 0), (0.8, 1), (0.9, 1), (0.95, 1)]
    report = judge.evaluate(preds)
    assert report.is_calibrated
    assert report.expected_calibration_error <= 0.15
    assert report.brier_score < 0.10

    sentinel = RegressionSentinel(regression_threshold=0.05)
    reg_report = sentinel.check_regression(baseline_score=0.90, current_score=0.82)
    assert reg_report.has_regression
    assert "Regression detected" in reg_report.details

    ok_report = sentinel.check_regression(baseline_score=0.90, current_score=0.91)
    assert not ok_report.has_regression
