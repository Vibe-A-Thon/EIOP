"""Acceptance tests for WP-027: Governed Actions and Write-Back (CRA-027.1-027.9, CRA-027.A)."""

import time
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from eoip.actions.contracts import (
    ActionError,
    ActionIntent,
    ActionState,
    ActionType,
    ApprovalExpiredError,
    ApprovalGrant,
    IdempotencyViolationError,
    IntentDigestMismatchError,
    InvalidApprovalError,
    ReadBackVerificationError,
    RiskClass,
    WriteBackDisabledError,
)
from eoip.actions.engine import ActionEngine
from eoip.actions.router import router
from eoip.intelligence_eng.engine import AutonomyLevel


# ---------------------------------------------------------------------------
# CRA-027.1: Declarative action types and argument schemas
# ---------------------------------------------------------------------------
def test_cra_027_1_declarative_action_types():
    engine = ActionEngine(write_back_enabled=True)
    custom_type = ActionType(
        type_id="act_custom_deploy",
        name="Deploy Artifact",
        target_connector="kubernetes",
        argument_schema={"type": "object", "properties": {"tag": {"type": "string"}}, "required": ["tag"]},
        preconditions=["cluster_healthy == True"],
        declared_effects=["DeploymentRevision", "ServiceEndpoint"],
        risk_class=RiskClass.HIGH,
        required_autonomy_level=AutonomyLevel.HITL,
        read_back_query="GET /apis/apps/v1/namespaces/{ns}/deployments/{name}",
    )
    engine.register_action_type(custom_type)
    registered = engine.get_action_type("act_custom_deploy")
    assert registered is not None
    assert registered.target_connector == "kubernetes"
    assert "DeploymentRevision" in registered.declared_effects
    assert registered.read_back_query is not None


# ---------------------------------------------------------------------------
# CRA-027.2: Default read-only and write-back disablement (Decision H-03)
# ---------------------------------------------------------------------------
def test_cra_027_2_read_only_default_and_write_back_disablement():
    # By default, write_back_enabled is False (CRA-027.2 / Decision H-03)
    engine = ActionEngine(write_back_enabled=False)

    # 1. Read-only actions succeed
    ro_intent = ActionIntent(
        action_type_id="act_lookup_readonly",
        target_instance="graph_primary",
        arguments={"entity_id": "service_123"},
        principal="analyst_alice",
        idempotency_key="idemp-key-read-only-001-abc",
    )
    staged_ro = engine.propose_action(ro_intent)
    assert staged_ro.state == ActionState.APPROVED

    # 2. Mutating write-back actions are rejected by default
    mutating_intent = ActionIntent(
        action_type_id="act_jira_create_issue",
        target_instance="jira_corp",
        arguments={"summary": "Fix compliance defect"},
        principal="analyst_alice",
        idempotency_key="idemp-key-mutating-002-xyz",
    )
    with pytest.raises(WriteBackDisabledError) as exc:
        engine.propose_action(mutating_intent)
    assert exc.value.code == "write_back_disabled"
    assert "H-03" in exc.value.message


# ---------------------------------------------------------------------------
# CRA-027.3: Digest-bound approvals and re-authorization before execution
# ---------------------------------------------------------------------------
def test_cra_027_3_digest_bound_approval_and_reauthorization():
    engine = ActionEngine(write_back_enabled=True)
    intent = ActionIntent(
        action_type_id="act_jira_create_issue",
        target_instance="jira_corp",
        arguments={"summary": "Initial summary before review"},
        principal="dev_bob",
        idempotency_key="idemp-key-jira-003-digest-test",
    )
    staged = engine.propose_action(intent)
    assert staged.state == ActionState.STAGED

    grant = engine.approve_action(staged.intent_id, approver="manager_carol")
    assert grant.intent_digest == staged.canonical_digest()
    assert grant.signature != ""

    # Tamper with arguments after approval
    intent.arguments["summary"] = "Malicious modified payload"

    # Execution must detect digest mismatch and reject
    with pytest.raises(IntentDigestMismatchError) as exc:
        engine.execute_action(
            intent.intent_id,
            idempotency_key="idemp-key-jira-003-digest-test",
            connector_executor=lambda i: {"issue_key": "PROJ-101"},
            read_back_verifier=lambda i, r: True,
        )
    assert exc.value.code == "digest_mismatch"
    assert intent.state == ActionState.FAILED


# ---------------------------------------------------------------------------
# CRA-027.4: Journals, idempotency, and unknown outcome on remote timeout
# ---------------------------------------------------------------------------
def test_cra_027_4_journals_idempotency_and_unknown_outcome_on_remote_timeout():
    engine = ActionEngine(write_back_enabled=True)
    intent = ActionIntent(
        action_type_id="act_jira_create_issue",
        target_instance="jira_corp",
        arguments={"summary": "Timeout incident test"},
        principal="operator_dan",
        idempotency_key="idemp-key-timeout-004-unique",
    )
    staged = engine.propose_action(intent)
    engine.approve_action(staged.intent_id, approver="manager_carol")

    def timeout_connector(i: ActionIntent):
        raise TimeoutError("Remote gateway socket timeout after commit")

    res = engine.execute_action(
        staged.intent_id,
        idempotency_key="idemp-key-timeout-004-unique",
        connector_executor=timeout_connector,
    )
    assert res.state == ActionState.UNKNOWN_OUTCOME

    journal = engine.get_journal(staged.intent_id)
    states = [e.state for e in journal]
    assert ActionState.STAGED in states
    assert ActionState.APPROVED in states
    assert ActionState.EXECUTING in states
    assert ActionState.UNKNOWN_OUTCOME in states


# ---------------------------------------------------------------------------
# CRA-027.5: Dry-run impact preview and cancellation before commit
# ---------------------------------------------------------------------------
def test_cra_027_5_dry_run_preview_and_cancellation_before_commit():
    engine = ActionEngine(write_back_enabled=True)

    # 1. Dry run preview
    dry_intent = ActionIntent(
        action_type_id="act_jira_create_issue",
        target_instance="jira_corp",
        arguments={"summary": "Preview dry run"},
        principal="analyst_alice",
        idempotency_key="idemp-key-dry-run-005-preview",
        dry_run=True,
    )
    preview = engine.propose_action(dry_intent)
    assert preview.state == ActionState.PROPOSED
    assert "dry_run_preview" in preview.details
    assert preview.details["dry_run_preview"]["target_connector"] == "jira"

    # 2. Cancellation before commit
    live_intent = ActionIntent(
        action_type_id="act_jira_create_issue",
        target_instance="jira_corp",
        arguments={"summary": "Will be cancelled"},
        principal="analyst_alice",
        idempotency_key="idemp-key-cancel-006-before-commit",
    )
    staged = engine.propose_action(live_intent)
    assert staged.state == ActionState.STAGED

    cancelled = engine.cancel_action(staged.intent_id, reason="Changed mind")
    assert cancelled.state == ActionState.FAILED
    assert cancelled.details["cancellation_reason"] == "Changed mind"


# ---------------------------------------------------------------------------
# CRA-027.6: Complete ActionIntent lifecycle
# ---------------------------------------------------------------------------
def test_cra_027_6_action_intent_lifecycle():
    engine = ActionEngine(write_back_enabled=True)
    intent = ActionIntent(
        action_type_id="act_servicenow_resolve_incident",
        target_instance="snow_instance",
        arguments={"sys_id": "inc_999", "close_code": "Solved"},
        principal="sre_frank",
        idempotency_key="idemp-key-lifecycle-007-complete",
    )

    # PROPOSED / STAGED
    staged = engine.propose_action(intent)
    assert staged.state == ActionState.STAGED

    # APPROVED
    engine.approve_action(staged.intent_id, approver="incident_commander")
    assert staged.state == ActionState.APPROVED

    # EXECUTING -> COMPLETED (with read-back confirmation)
    completed = engine.execute_action(
        staged.intent_id,
        idempotency_key="idemp-key-lifecycle-007-complete",
        connector_executor=lambda i: {"status": "Resolved", "sys_id": "inc_999"},
        read_back_verifier=lambda i, r: r.get("status") == "Resolved",
    )
    assert completed.state == ActionState.COMPLETED
    assert completed.details["remote_result"]["status"] == "Resolved"


# ---------------------------------------------------------------------------
# CRA-027.7: SHACL action shapes and AutonomyLevel HCTL requirement
# ---------------------------------------------------------------------------
def test_cra_027_7_shacl_action_shapes_and_autonomy_level_hctl():
    engine = ActionEngine(write_back_enabled=True)
    intent = ActionIntent(
        action_type_id="act_schema_drop_table",  # CRITICAL_DESTRUCTIVE
        target_instance="prod_db_cluster",
        arguments={"table_name": "customer_pii"},
        principal="db_admin_sam",
        idempotency_key="idemp-key-destructive-008-drop",
    )
    staged = engine.propose_action(intent)
    assert staged.state == ActionState.STAGED

    # Attempt approval with HITL (insufficient for destructive actions)
    with pytest.raises(ActionError) as exc:
        engine.approve_action(staged.intent_id, approver="auto_agent", approver_autonomy=AutonomyLevel.HITL)
    assert exc.value.code == "insufficient_autonomy_level"

    # Approval with HCTL succeeds
    grant = engine.approve_action(staged.intent_id, approver="security_officer", approver_autonomy=AutonomyLevel.HCTL)
    assert grant.approver_autonomy == AutonomyLevel.HCTL
    assert staged.state == ActionState.APPROVED


# ---------------------------------------------------------------------------
# CRA-027.8: Mandatory Idempotency-Key (16-128 chars) and 5-min expiry
# ---------------------------------------------------------------------------
def test_cra_027_8_mandatory_idempotency_key_and_expiry():
    engine = ActionEngine(write_back_enabled=True)

    # 1. Invalid short idempotency key (< 16 chars) rejected
    with pytest.raises(IdempotencyViolationError) as exc_short:
        engine.propose_action(ActionIntent(
            action_type_id="act_lookup_readonly",
            target_instance="graph",
            arguments={},
            principal="user",
            idempotency_key="short-key",
        ))
    assert exc_short.value.code == "invalid_idempotency_key"

    # 2. Expiry check: simulate execution 301 seconds later (> 300 s / 5 min limit)
    intent = ActionIntent(
        action_type_id="act_jira_create_issue",
        target_instance="jira",
        arguments={"summary": "Expiry test"},
        principal="user",
        idempotency_key="idemp-key-expiry-009-duration-test",
    )
    staged = engine.propose_action(intent)
    engine.approve_action(staged.intent_id, approver="lead")

    expired_time = time.time() + 301.0
    with pytest.raises(ApprovalExpiredError) as exc_exp:
        engine.execute_action(
            staged.intent_id,
            idempotency_key="idemp-key-expiry-009-duration-test",
            current_time=expired_time,
        )
    assert exc_exp.value.code == "approval_expired"


# ---------------------------------------------------------------------------
# CRA-027.9: Canonical routes and OCA aliases
# ---------------------------------------------------------------------------
def test_cra_027_9_canonical_routes_and_oca_aliases():
    # FT-D15: mount the router on an app; current FastAPI needs the app middleware stack.
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    # Propose via canonical route
    res_prop = client.post(
        "/api/v1/actions/propose",
        headers={"Idempotency-Key": "idemp-key-route-010-canonical"},
        json={
            "action_type_id": "act_lookup_readonly",
            "target_instance": "graph_primary",
            "arguments": {"entity_id": "cust_456"},
            "principal": "web_user",
        },
    )
    assert res_prop.status_code == 200
    intent_id = res_prop.json()["intent_id"]

    # List via canonical route
    res_list = client.get("/api/v1/actions")
    assert res_list.status_code == 200
    assert any(a["intent_id"] == intent_id for a in res_list.json())

    # List via OCA alias route
    res_oca_list = client.get("/ontology/actions")
    assert res_oca_list.status_code == 200
    assert any(a["intent_id"] == intent_id for a in res_oca_list.json())


# ---------------------------------------------------------------------------
# CRA-027.A: Acceptance Gate: Vendor read-back verification and timeout recovery
# ---------------------------------------------------------------------------
def test_cra_027_a_vendor_read_back_verification_and_timeout_recovery():
    """Demonstrates exactly one intended effect through vendor read-back, idempotency, and audit."""
    engine = ActionEngine(write_back_enabled=True)

    intent = ActionIntent(
        action_type_id="act_jira_create_issue",
        target_instance="jira_enterprise",
        arguments={"project": "LEGAL", "issue_type": "SubpoenaRecord", "id": "SUB-881"},
        principal="compliance_lead",
        idempotency_key="idemp-key-acceptance-gate-027-a",
    )
    staged = engine.propose_action(intent)
    engine.approve_action(staged.intent_id, approver="counsel_chief")

    vendor_database: dict[str, dict] = {}
    call_count = {"mutations": 0, "read_backs": 0}

    def remote_jira_mock(act_intent: ActionIntent):
        call_count["mutations"] += 1
        key = act_intent.arguments["id"]
        vendor_database[key] = {"id": key, "status": "CREATED", "timestamp": time.time()}
        return {"remote_key": key, "http_status": 200}

    def remote_jira_read_back(act_intent: ActionIntent, result: dict):
        call_count["read_backs"] += 1
        key = act_intent.arguments["id"]
        # Confirm that the vendor database actually contains the record
        record = vendor_database.get(key)
        return record is not None and record["status"] == "CREATED"

    # First execution: successfully commits and confirms via read-back
    res1 = engine.execute_action(
        staged.intent_id,
        idempotency_key="idemp-key-acceptance-gate-027-a",
        connector_executor=remote_jira_mock,
        read_back_verifier=remote_jira_read_back,
    )
    assert res1.state == ActionState.COMPLETED
    assert call_count["mutations"] == 1
    assert call_count["read_backs"] == 1

    # Idempotent retry: duplicate execution returns cached completed state WITHOUT invoking remote mutation again
    res2 = engine.execute_action(
        staged.intent_id,
        idempotency_key="idemp-key-acceptance-gate-027-a",
        connector_executor=remote_jira_mock,
        read_back_verifier=remote_jira_read_back,
    )
    assert res2.state == ActionState.COMPLETED
    assert call_count["mutations"] == 1  # Exactly ONE mutation executed!
    assert call_count["read_backs"] == 1

    # Audit verification
    journal = engine.get_journal(staged.intent_id)
    assert any(e.state == ActionState.COMPLETED and e.read_back_verified is True for e in journal)

    # Demonstrate that HTTP 200 alone without successful read-back is rejected
    fake_intent = ActionIntent(
        action_type_id="act_jira_create_issue",
        target_instance="jira_enterprise",
        arguments={"project": "LEGAL", "issue_type": "SubpoenaRecord", "id": "SUB-999-GHOST"},
        principal="compliance_lead",
        idempotency_key="idemp-key-acceptance-gate-027-a-ghost",
    )
    fake_staged = engine.propose_action(fake_intent)
    engine.approve_action(fake_staged.intent_id, approver="counsel_chief")

    with pytest.raises(ReadBackVerificationError):
        engine.execute_action(
            fake_staged.intent_id,
            idempotency_key="idemp-key-acceptance-gate-027-a-ghost",
            connector_executor=lambda i: {"http_status": 200},  # Returns 200
            read_back_verifier=lambda i, r: False,  # But read-back fails!
        )
    assert fake_staged.state == ActionState.FAILED
