"""Acceptance test suite for Support, Service Objectives and Operator Readiness (WP-038, CRA-038.1-038.8, CRA-038.A)."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from eoip.ops.readiness import (
    IncidentRehearsalRunner,
    IncidentSeverity,
    OperationalPlaybookRegistry,
    ResponsibilityRegistry,
    SLAPerformanceProposal,
    SupportBundleEngine,
)


# ===========================================================================
# CRA-038.1: Service responsibility matrix and severity definitions
# ===========================================================================

def test_cra_038_1_service_responsibility_matrix():
    boundaries = ResponsibilityRegistry.get_boundaries()
    owners = {b["owner"] for b in boundaries}
    assert "CUSTOMER" in owners
    assert "VENDOR" in owners

    # Host & network belong to customer; runtime & ontology belong to vendor
    host_b = next(b for b in boundaries if b["boundary"] == "host_infrastructure")
    assert host_b["owner"] == "CUSTOMER"

    runtime_b = next(b for b in boundaries if b["boundary"] == "platform_runtime_engines")
    assert runtime_b["owner"] == "VENDOR"

    # Severity levels
    assert IncidentSeverity.P1.value == "P1"
    assert IncidentSeverity.P2.value == "P2"
    assert IncidentSeverity.P3.value == "P3"
    assert IncidentSeverity.P4.value == "P4"


# ===========================================================================
# CRA-038.2: Documented incident, scaling, upgrade, and recovery playbooks
# ===========================================================================

def test_cra_038_2_documented_incident_playbooks():
    # Verify presence of diagnostic prerequisites, stop conditions, rollback procedures
    rb = OperationalPlaybookRegistry.get_runbook("ingestion_backlog")
    assert len(rb.diagnostic_prerequisites) >= 1
    assert len(rb.mitigation_steps) >= 1
    assert len(rb.stop_conditions) >= 1
    assert len(rb.rollback_procedure) >= 1
    assert rb.target_recovery_time_min > 0


# ===========================================================================
# CRA-038.3: 99.9% availability and initial response as proposals
# ===========================================================================

def test_cra_038_3_availability_and_response_proposals():
    proposal = SLAPerformanceProposal.CRAR_PROPOSAL
    assert proposal["status"] == "PROPOSED_PENDING_H08"
    assert proposal["availability_target_pct"] == 99.9
    assert "Initial response is not resolution time" in proposal["disclaimer"]
    assert len(proposal["exclusions"]) >= 1


# ===========================================================================
# CRA-038.4: Redacted support bundles with consent and retention
# ===========================================================================

def test_cra_038_4_redacted_support_bundles_with_consent():
    engine = SupportBundleEngine()

    # 1. Fails without operator consent
    with pytest.raises(PermissionError) as exc_consent:
        engine.create_support_bundle(operator_consent=False, operator_id="admin-1")
    assert "Operator consent is required" in str(exc_consent.value)

    # 2. Generates bundle with consent, retention, and redacted secrets
    bundle_res = engine.create_support_bundle(
        operator_consent=True,
        operator_id="admin-1",
        retention_days=14,
        audit_events=[{"action": "LOGIN", "secret_token": "super_secret_12345"}],
    )

    bundle = bundle_res["bundle"]
    assert bundle["consent_granted"] is True
    assert bundle["retention_policy"]["retention_days"] == 14
    assert len(bundle_res["bundle_sha256"]) == 64
    assert "super_secret_12345" not in json.dumps(bundle)


# ===========================================================================
# CRA-038.5: Rehearsal with external operator recording observations
# ===========================================================================

def test_cra_038_5_incident_rehearsal_with_external_operator():
    res = IncidentRehearsalRunner.rehearse_credential_compromise("token-compromised-404")
    assert res["status"] == "RECOVERED"
    assert res["rehearsal_operator"] == "external-drills-operator"
    assert res["actual_duration_sec"] < res["target_recovery_sec"]
    assert res["unresolved_failures"] == []


# ===========================================================================
# CRA-038.6: All 7 required runbooks
# ===========================================================================

def test_cra_038_6_all_seven_mandatory_runbooks_registered():
    required_runbooks = {
        "ingestion_backlog",
        "memory_exhaustion",
        "compromised_credentials",
        "ontology_rollback",
        "stuck_publication",
        "split_brain",
        "policy_lag_index",
    }
    registered = set(OperationalPlaybookRegistry.RUNBOOKS.keys())
    assert required_runbooks.issubset(registered)

    for rb_name in required_runbooks:
        rb = OperationalPlaybookRegistry.get_runbook(rb_name)
        assert rb.runbook_id.startswith("RB-OPS-")
        assert len(rb.mitigation_steps) > 0


# ===========================================================================
# CRA-038.7: eoip-admin support-bundle tool producing encrypted bundle
# ===========================================================================

def test_cra_038_7_support_bundle_cli_engine():
    engine = SupportBundleEngine(signing_secret=b"TEST-SIGNING-SECRET-32-BYTES-MIN")
    res = engine.create_support_bundle(operator_consent=True, operator_id="operator-dev")

    assert res["status"] == "ENCRYPTED_SEALED"
    assert "hmac_signature" in res
    assert len(res["hmac_signature"]) == 64
    assert res["bundle"]["schema_version"] == "eoip-support-bundle/v1"


# ===========================================================================
# CRA-038.8: Severity response proposals side-by-side (CRAr vs AGG for H-08)
# ===========================================================================

def test_cra_038_8_severity_response_side_by_side_proposals():
    comparison = SLAPerformanceProposal.get_side_by_side_comparison()
    assert comparison["decision_record"] == "Decision H-08 / Conflict X-08"
    assert comparison["binding_state"] == "PROPOSAL_ONLY"

    proposals = comparison["proposals"]
    assert "crar" in proposals
    assert "agg" in proposals

    # Verify CRAr targets
    assert proposals["crar"]["targets"]["P1"]["initial_response_time"] == "1 hour"
    assert proposals["crar"]["targets"]["P2"]["initial_response_time"] == "4 business hours"

    # Verify AGG targets
    assert proposals["agg"]["targets"]["P1"]["initial_response_time"] == "< 15 minutes"
    assert proposals["agg"]["targets"]["P2"]["initial_response_time"] == "< 1 business hour"


# ===========================================================================
# CRA-038.A: Integrated Operator Readiness Acceptance
# ===========================================================================

def test_cra_038_a_operator_readiness_acceptance_integrated():
    # 1. Real drill of credential compromise
    comp_drill = IncidentRehearsalRunner.rehearse_credential_compromise("token-leak-001")
    assert comp_drill["status"] == "RECOVERED"
    assert comp_drill["actual_duration_sec"] <= comp_drill["target_recovery_sec"]

    # 2. Simulated split-brain recovery within 30 min target (AGG proposal)
    sb_drill = IncidentRehearsalRunner.rehearse_split_brain_recovery("partition-cluster-west")
    assert sb_drill["status"] == "RECOVERED"
    # Target 30 minutes = 1800s
    assert sb_drill["target_recovery_sec"] == 1800
    assert sb_drill["actual_duration_sec"] < 1800
    assert "fencing_token" in sb_drill
    assert sb_drill["unresolved_failures"] == []

    # 3. Generate sealed support bundle with consent and retention
    bundle_engine = SupportBundleEngine()
    bundle = bundle_engine.create_support_bundle(
        operator_consent=True,
        operator_id="lead-operator",
        retention_days=30,
    )
    assert bundle["status"] == "ENCRYPTED_SEALED"
    assert bundle["bundle"]["consent_granted"] is True
    assert bundle["bundle"]["retention_policy"]["retention_days"] == 30
