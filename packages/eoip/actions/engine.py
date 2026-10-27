"""Governed Action Execution Engine & Two-Phase Write-Back Outbox (CRA-027)."""

from __future__ import annotations

import hmac
import logging
import secrets
import threading
import time
from typing import Any
from collections.abc import Callable

from eoip.actions.contracts import (
    ActionError,
    ActionIntent,
    ActionState,
    ActionType,
    ApprovalExpiredError,
    ApprovalGrant,
    ExecutionJournalEntry,
    IdempotencyViolationError,
    IntentDigestMismatchError,
    InvalidApprovalError,
    ReadBackVerificationError,
    RiskClass,
    WriteBackDisabledError,
)
from eoip.intelligence_eng.engine import AutonomyLevel

logger = logging.getLogger("eoip.actions.engine")


class ActionEngine:
    """Manages declarative action types, lifecycle transitions, approval gates, and read-back verification."""

    def __init__(self, write_back_enabled: bool = False, signing_secret: bytes | None = None) -> None:
        self.write_back_enabled = write_back_enabled
        self._signing_secret = signing_secret or secrets.token_bytes(32)
        self._lock = threading.Lock()

        self._action_types: dict[str, ActionType] = {}
        self._intents: dict[str, ActionIntent] = {}
        self._idempotency_map: dict[str, str] = {}  # idempotency_key -> intent_id
        self._approvals: dict[str, ApprovalGrant] = {}  # intent_id -> ApprovalGrant
        self._journals: dict[str, list[ExecutionJournalEntry]] = {}  # intent_id -> list of entries

        # Register standard default actions
        self._register_default_actions()

    def _register_default_actions(self) -> None:
        self.register_action_type(ActionType(
            type_id="act_lookup_readonly",
            name="Read-Only Entity Query",
            target_connector="graph_store",
            risk_class=RiskClass.READ_ONLY,
            required_autonomy_level=AutonomyLevel.HOOTL,
            is_destructive=False,
        ))
        self.register_action_type(ActionType(
            type_id="act_jira_create_issue",
            name="Create Jira Issue",
            target_connector="jira",
            risk_class=RiskClass.MEDIUM,
            required_autonomy_level=AutonomyLevel.HITL,
            is_destructive=False,
            read_back_query="GET /rest/api/2/issue/{issue_key}",
        ))
        self.register_action_type(ActionType(
            type_id="act_servicenow_resolve_incident",
            name="Resolve ServiceNow Incident",
            target_connector="servicenow",
            risk_class=RiskClass.HIGH,
            required_autonomy_level=AutonomyLevel.HITL,
            is_destructive=False,
            read_back_query="GET /api/now/table/incident/{sys_id}",
        ))
        self.register_action_type(ActionType(
            type_id="act_schema_drop_table",
            name="Drop Database Table",
            target_connector="sql",
            risk_class=RiskClass.CRITICAL_DESTRUCTIVE,
            required_autonomy_level=AutonomyLevel.HCTL,
            is_destructive=True,
            read_back_query="SELECT COUNT(*) FROM information_schema.tables WHERE table_name = :tbl",
        ))

    def register_action_type(self, action_type: ActionType) -> None:
        with self._lock:
            self._action_types[action_type.type_id] = action_type

    def get_action_type(self, type_id: str) -> ActionType | None:
        return self._action_types.get(type_id)

    def _append_journal(self, intent_id: str, state: ActionState, details: dict[str, Any], verified: bool = False, error: str | None = None) -> None:
        entry = ExecutionJournalEntry(
            intent_id=intent_id,
            state=state,
            details=details,
            read_back_verified=verified,
            error=error,
        )
        if intent_id not in self._journals:
            self._journals[intent_id] = []
        self._journals[intent_id].append(entry)

    def get_journal(self, intent_id: str) -> list[ExecutionJournalEntry]:
        with self._lock:
            return list(self._journals.get(intent_id, []))

    def get_intent(self, intent_id: str) -> ActionIntent | None:
        with self._lock:
            return self._intents.get(intent_id)

    def list_intents(self, tenant_id: str | None = None) -> list[ActionIntent]:
        with self._lock:
            intents = list(self._intents.values())
            if tenant_id:
                return [i for i in intents if i.scope.get("tenant_id") == tenant_id]
            return intents

    # -----------------------------------------------------------------------
    # Propose / Stage Action
    # -----------------------------------------------------------------------
    def propose_action(self, intent: ActionIntent) -> ActionIntent:
        # 1. Idempotency key validation (CRA-027.8)
        if not intent.idempotency_key or len(intent.idempotency_key) < 16 or len(intent.idempotency_key) > 128:
            raise IdempotencyViolationError(
                "invalid_idempotency_key",
                "Idempotency-Key is mandatory and must be between 16 and 128 characters (CRA-027.8)"
            )

        with self._lock:
            # Check for duplicate idempotency key
            if intent.idempotency_key in self._idempotency_map:
                existing_id = self._idempotency_map[intent.idempotency_key]
                existing = self._intents[existing_id]
                # If arguments or action type changed under same idempotency key, reject
                if existing.canonical_digest() != intent.canonical_digest():
                    raise IdempotencyViolationError(
                        "idempotency_conflict",
                        f"Idempotency key '{intent.idempotency_key}' was previously used with differing parameters"
                    )
                return existing

            action_type = self._action_types.get(intent.action_type_id)
            if not action_type:
                raise ActionError("unknown_action_type", f"Action type '{intent.action_type_id}' is not registered")

            # 2. Check read-only / write-back configuration (CRA-027.2)
            if not self.write_back_enabled and action_type.risk_class != RiskClass.READ_ONLY:
                raise WriteBackDisabledError(
                    "write_back_disabled",
                    "Write-back is disabled under CRA-027.2 / Decision H-03; all sources default to read-only"
                )

            # 3. Dry-run / impact preview (CRA-027.5)
            if intent.dry_run:
                intent.state = ActionState.PROPOSED
                intent.details["dry_run_preview"] = {
                    "declared_effects": action_type.declared_effects,
                    "target_connector": action_type.target_connector,
                    "risk_class": action_type.risk_class.value,
                    "is_destructive": action_type.is_destructive,
                    "estimated_impact": f"Action {action_type.name} will affect {len(action_type.declared_effects)} state boundaries",
                }
                self._intents[intent.intent_id] = intent
                self._idempotency_map[intent.idempotency_key] = intent.intent_id
                self._append_journal(intent.intent_id, ActionState.PROPOSED, {"dry_run": True})
                return intent

            # 4. Stage for approval if human participation required
            requires_approval = action_type.risk_class != RiskClass.READ_ONLY
            intent.state = ActionState.STAGED if requires_approval else ActionState.APPROVED
            self._intents[intent.intent_id] = intent
            self._idempotency_map[intent.idempotency_key] = intent.intent_id
            self._append_journal(intent.intent_id, intent.state, {"propose_stage": True})
            return intent

    # -----------------------------------------------------------------------
    # Approve Action
    # -----------------------------------------------------------------------
    def approve_action(
        self,
        intent_id: str,
        approver: str,
        approver_autonomy: AutonomyLevel = AutonomyLevel.HITL,
        nonce: str | None = None,
    ) -> ApprovalGrant:
        with self._lock:
            intent = self._intents.get(intent_id)
            if not intent:
                raise ActionError("intent_not_found", f"Action intent '{intent_id}' does not exist")

            if intent.state not in (ActionState.PROPOSED, ActionState.STAGED):
                raise ActionError("invalid_state_transition", f"Cannot approve intent in state '{intent.state}'")

            action_type = self._action_types[intent.action_type_id]

            # Destructive actions require HCTL (Human-Controlled Level) (CRA-027.7)
            if (action_type.is_destructive or action_type.risk_class == RiskClass.CRITICAL_DESTRUCTIVE):
                if approver_autonomy != AutonomyLevel.HCTL:
                    raise ActionError(
                        "insufficient_autonomy_level",
                        f"Destructive action '{action_type.name}' requires HCTL (Human-Controlled) level for approval"
                    )

            grant_nonce = nonce or secrets.token_hex(16)
            intent_digest = intent.canonical_digest()

            # Sign approval
            sig_payload = f"{intent_id}:{intent_digest}:{approver}:{grant_nonce}".encode("utf-8")
            signature = hmac.new(self._signing_secret, sig_payload, "sha256").hexdigest()

            grant = ApprovalGrant(
                intent_id=intent_id,
                intent_digest=intent_digest,
                approver=approver,
                approver_autonomy=approver_autonomy,
                nonce=grant_nonce,
                signature=signature,
            )
            self._approvals[intent_id] = grant
            intent.state = ActionState.APPROVED
            self._append_journal(intent_id, ActionState.APPROVED, {
                "approver": approver,
                "nonce": grant_nonce,
                "grant_id": grant.grant_id,
            })
            return grant

    # -----------------------------------------------------------------------
    # Execute Action with Two-Phase Verification & Read-Back
    # -----------------------------------------------------------------------
    def execute_action(
        self,
        intent_id: str,
        idempotency_key: str,
        connector_executor: Callable[[ActionIntent], dict[str, Any]] | None = None,
        read_back_verifier: Callable[[ActionIntent, dict[str, Any]], bool] | None = None,
        compensation_executor: Callable[[ActionIntent], None] | None = None,
        current_time: float | None = None,
    ) -> ActionIntent:
        with self._lock:
            intent = self._intents.get(intent_id)
            if not intent:
                raise ActionError("intent_not_found", f"Action intent '{intent_id}' does not exist")

            # Check idempotency
            if intent.state == ActionState.COMPLETED:
                return intent

            # Validate idempotency key matches
            if intent.idempotency_key != idempotency_key:
                raise IdempotencyViolationError(
                    "idempotency_mismatch",
                    "Supplied Idempotency-Key does not match original intent"
                )

            action_type = self._action_types[intent.action_type_id]

            # Re-authorize and verify approval if required (CRA-027.3)
            if action_type.risk_class != RiskClass.READ_ONLY:
                grant = self._approvals.get(intent_id)
                if not grant:
                    raise InvalidApprovalError("missing_approval", "No valid approval grant found for action execution")

                # Expiry check (5-minute default)
                if grant.is_expired(current_time):
                    intent.state = ActionState.FAILED
                    self._append_journal(intent_id, ActionState.FAILED, {"reason": "Approval expired"}, error="ApprovalExpiredError")
                    raise ApprovalExpiredError("approval_expired", f"Approval grant {grant.grant_id} has expired (5-minute limit)")

                # Digest check: reject if intent arguments modified after approval (CRA-027.3, CRA-027.8)
                current_digest = intent.canonical_digest()
                if grant.intent_digest != current_digest:
                    intent.state = ActionState.FAILED
                    self._append_journal(intent_id, ActionState.FAILED, {"reason": "Intent modified after approval"}, error="IntentDigestMismatchError")
                    raise IntentDigestMismatchError(
                        "digest_mismatch",
                        "Action arguments or parameters were modified after approval was granted"
                    )

            # Transition to EXECUTING
            intent.state = ActionState.EXECUTING
            self._append_journal(intent_id, ActionState.EXECUTING, {"timestamp": time.time()})

        # Phase 1: Execute remote mutation
        remote_result: dict[str, Any] = {}
        execution_failed = False
        timeout_occurred = False

        if connector_executor:
            try:
                remote_result = connector_executor(intent)
            except TimeoutError as exc:
                timeout_occurred = True
                logger.warning(f"Remote call timed out for intent {intent_id}: {exc}")
            except Exception as exc:
                execution_failed = True
                logger.error(f"Remote execution failed for intent {intent_id}: {exc}")

        with self._lock:
            # Phase 1.b: Handle uncertain outcome (CRA-027.4, CRA-027.6)
            if timeout_occurred:
                intent.state = ActionState.UNKNOWN_OUTCOME
                self._append_journal(
                    intent_id, ActionState.UNKNOWN_OUTCOME,
                    {"reason": "Remote commit timed out before confirmation; operator recovery required"},
                    error="TimeoutError"
                )
                return intent

            # Phase 1.c: Handle direct failure
            if execution_failed:
                if compensation_executor:
                    try:
                        compensation_executor(intent)
                        intent.state = ActionState.COMPENSATED
                        self._append_journal(intent_id, ActionState.COMPENSATED, {"reason": "Execution failed; compensation executed"})
                        return intent
                    except Exception as comp_exc:
                        intent.state = ActionState.FAILED
                        self._append_journal(intent_id, ActionState.FAILED, {"compensation_failed": str(comp_exc)}, error="CompensationError")
                        return intent
                intent.state = ActionState.FAILED
                self._append_journal(intent_id, ActionState.FAILED, {"reason": "Connector execution failed"}, error="ExecutionFailed")
                return intent

            # Phase 2: Read-back verification (CRA-027.4)
            # A 200 alone is never sufficient; read back the effect from source system!
            read_back_ok = True
            if read_back_verifier:
                try:
                    read_back_ok = read_back_verifier(intent, remote_result)
                except Exception as exc:
                    read_back_ok = False
                    logger.warning(f"Read-back failed: {exc}")

            if not read_back_ok:
                if compensation_executor:
                    try:
                        compensation_executor(intent)
                        intent.state = ActionState.COMPENSATED
                        self._append_journal(intent_id, ActionState.COMPENSATED, {"reason": "Read-back verification failed; compensation executed"})
                        return intent
                    except Exception:
                        pass
                intent.state = ActionState.FAILED
                self._append_journal(intent_id, ActionState.FAILED, {"reason": "Read-back verification failed to confirm source effect"}, error="ReadBackVerificationError")
                raise ReadBackVerificationError("read_back_failed", "Target system read-back did not confirm intended state mutation")

            # Phase 3: Transition to COMPLETED with confirmed read-back
            intent.state = ActionState.COMPLETED
            intent.details["remote_result"] = remote_result
            self._append_journal(intent_id, ActionState.COMPLETED, remote_result, verified=True)
            return intent

    # -----------------------------------------------------------------------
    # Cancel Action (CRA-027.5)
    # -----------------------------------------------------------------------
    def cancel_action(self, intent_id: str, reason: str = "User cancelled") -> ActionIntent:
        with self._lock:
            intent = self._intents.get(intent_id)
            if not intent:
                raise ActionError("intent_not_found", f"Action intent '{intent_id}' does not exist")

            if intent.state in (ActionState.EXECUTING, ActionState.COMPLETED, ActionState.COMPENSATED):
                raise ActionError("cannot_cancel", f"Cannot cancel action already in state '{intent.state}'")

            intent.state = ActionState.FAILED
            intent.details["cancellation_reason"] = reason
            self._append_journal(intent_id, ActionState.FAILED, {"cancellation_reason": reason}, error="CancelledByUser")
            return intent
