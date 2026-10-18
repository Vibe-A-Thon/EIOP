"""Tests for dual-path answering, arbitration, calibration honesty, and text-labelled explanations (CRA-045.1, CRA-045.3, CRA-045.6, CRA-045.8, CRA-045.A)."""

import pytest

from eoip.contracts.canonical import (
    AgreementState,
    PrincipalType,
    ProducerClass,
    TrustedScope,
)
from eoip.ai.boundary import (
    DualPathOrchestrator,
    create_probabilistic_proposal,
)


@pytest.fixture
def scope():
    return TrustedScope(
        tenant_id="tenant_alpha",
        workspace_id="ws_1",
        principal_id="user_1",
        principal_type=PrincipalType.USER,
        roles=["analyst"],
    )


def test_dual_path_corroborated_on_exact_match(scope):
    """CRA-045.3: Known fixture question where deterministic and probabilistic paths agree returns CORROBORATED."""
    orchestrator = DualPathOrchestrator()

    # Exact deterministic query returns "CEO_42"
    def deterministic_solver(s, q):
        return "CEO_42"

    # Probabilistic LLM returns "CEO_42"
    def probabilistic_solver(s, q):
        return "CEO_42"

    res = orchestrator.execute_dual_path(
        question_id="q_ceo",
        question_text="Who is the CEO of Acme Corp?",
        scope=scope,
        deterministic_fn=deterministic_solver,
        probabilistic_fn=probabilistic_solver,
    )

    assert res.agreement == AgreementState.CORROBORATED
    assert res.deterministic_result == "CEO_42"
    assert res.probabilistic_result == "CEO_42"
    assert "[CORROBORATED]" in (res.explanation or "")


def test_dual_path_disputed_on_misleading_probabilistic_neighbour(scope):
    """CRA-045.3, CRA-045.A: Injecting a misleading embedding neighbour produces DISPUTED without silent override."""
    orchestrator = DualPathOrchestrator()

    # Deterministic ground truth from SPARQL / graph traversal
    def deterministic_solver(s, q):
        return "Department:Security"

    # Misleading embedding vector neighbour proposed by probabilistic model
    def probabilistic_solver(s, q):
        return "Department:Marketing"

    res = orchestrator.execute_dual_path(
        question_id="q_dept",
        question_text="Which department owns compliance?",
        scope=scope,
        deterministic_fn=deterministic_solver,
        probabilistic_fn=probabilistic_solver,
    )

    assert res.agreement == AgreementState.DISPUTED
    # Neither result is suppressed or silently overridden
    assert res.deterministic_result == "Department:Security"
    assert res.probabilistic_result == "Department:Marketing"
    assert "[DISPUTED]" in (res.explanation or "")
    # Text labels are present, not color alone (CRA-045.8)
    assert "Deterministic path returned" in (res.explanation or "")
    assert "Probabilistic AI proposed" in (res.explanation or "")


def test_dual_path_uncorroborated_when_probabilistic_only(scope):
    """CRA-045.3: Question with no exact deterministic path returns UNCORROBORATED."""
    orchestrator = DualPathOrchestrator()

    # No exact deterministic query exists for subjective summary
    res = orchestrator.execute_dual_path(
        question_id="q_summary",
        question_text="Summarize the company's culture strategy",
        scope=scope,
        deterministic_fn=None,
        probabilistic_fn=lambda s, q: "Collaborative, data-driven, agile",
    )

    assert res.agreement == AgreementState.UNCORROBORATED
    assert res.deterministic_result is None
    assert res.probabilistic_result == "Collaborative, data-driven, agile"
    assert "[PROBABILISTIC ONLY]" in (res.explanation or "")


def test_calibration_honesty_uncalibrated_score_never_claimed_as_probability():
    """CRA-045.6: Raw model output is never claimed as calibrated confidence without calibrator."""
    # Proposal without calibrator
    prop_uncal = create_probabilistic_proposal(
        subject="http://example.org/entity/E1",
        predicate="http://example.org/pred/riskLevel",
        object_value="HIGH",
        model_name="RiskGNN",
        model_version="1.0.0",
        raw_score=0.88,
        calibrator_ref=None,
        calibrated_confidence=0.88,  # Attempted false confidence claim
    )
    # Uncalibrated confidence MUST be None and confidence_calibrated MUST be False
    assert prop_uncal.confidence is None
    assert prop_uncal.confidence_calibrated is False
    assert prop_uncal.model_lineage.calibrator_id is None

    # Proposal with valid calibrator
    prop_cal = create_probabilistic_proposal(
        subject="http://example.org/entity/E1",
        predicate="http://example.org/pred/riskLevel",
        object_value="HIGH",
        model_name="RiskGNN",
        model_version="1.0.0",
        raw_score=0.88,
        calibrator_ref="PlattScaling_v1.0",
        calibrated_confidence=0.82,
    )
    assert prop_cal.confidence == 0.82
    assert prop_cal.confidence_calibrated is True
    assert prop_cal.model_lineage.calibrator_id == "PlattScaling_v1.0"
