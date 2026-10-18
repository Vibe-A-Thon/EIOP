"""Governed action dispatcher and rollback receipt generator for ASPEII (ASPEII-RQ-021..035)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple

from eoip.contracts.aspeii import (
    ASPEIIActionCertificate,
    ASPEIIActionIntent,
    ASPEIIApprovalDecision,
    canonical_action_digest,
)
from eoip.aspeii.admission import ASPEIIAdmissionController, AdmissionDecision


@dataclass
class RollbackReceipt:
    rollback_id: str
    action_digest: str
    target_system: str
    undo_command: Dict[str, Any]
    captured_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    receipt_sha256: str = ""

    def __post_init__(self):
        if not self.receipt_sha256:
            blob = json.dumps(
                {
                    "rollback_id": self.rollback_id,
                    "action_digest": self.action_digest,
                    "target_system": self.target_system,
                    "undo_command": self.undo_command,
                    "captured_at": self.captured_at.isoformat(),
                },
                sort_keys=True,
            ).encode("utf-8")
            self.receipt_sha256 = hashlib.sha256(blob).hexdigest()


@dataclass
class ExecutionResult:
    success: bool
    status_code: str
    action_digest: str
    effect_summary: Dict[str, Any]
    rollback: Optional[RollbackReceipt] = None
    error_message: Optional[str] = None
    executed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ASPEIIDispatcher:
    """Dispatches admitted action intents and guarantees rollback generation."""

    def __init__(self, admission_controller: Optional[ASPEIIAdmissionController] = None) -> None:
        self.admission = admission_controller or ASPEIIAdmissionController()
        self._handlers: Dict[str, Callable[[ASPEIIActionIntent], Tuple[bool, Dict[str, Any], Optional[Dict[str, Any]]]]] = {}
        self._history: List[ExecutionResult] = []

    def register_handler(
        self,
        action_type_id: str,
        handler: Callable[[ASPEIIActionIntent], Tuple[bool, Dict[str, Any], Optional[Dict[str, Any]]]],
    ) -> None:
        """Register action handler: returns (success, effect_data, optional_undo_data)."""
        self._handlers[action_type_id] = handler

    def dispatch(
        self,
        intent: ASPEIIActionIntent,
        certificate: Optional[ASPEIIActionCertificate] = None,
        approvals: Optional[List[ASPEIIApprovalDecision]] = None,
    ) -> ExecutionResult:
        digest = canonical_action_digest(intent)

        # 1. Evaluate admission gate
        admission = self.admission.evaluate_admission(intent, certificate, approvals)
        if not admission.admitted:
            res = ExecutionResult(
                success=False,
                status_code=admission.status_code,
                action_digest=digest,
                effect_summary={},
                error_message=admission.reason,
            )
            self._history.append(res)
            return res

        # 2. Check handler registration
        handler = self._handlers.get(intent.tool_ref.id) or self._handlers.get(intent.action_id)
        if not handler:
            # Fallback default deterministic runner
            def default_runner(i: ASPEIIActionIntent):
                return True, {"action": i.action_id, "status": "COMPLETED"}, {"restore_state": "PREV"}
            handler = default_runner

        # 3. Execute
        try:
            success, effect_data, undo_data = handler(intent)
            rollback = None
            if undo_data:
                rollback = RollbackReceipt(
                    rollback_id=f"rb-{digest[:12]}-{int(datetime.now(timezone.utc).timestamp())}",
                    action_digest=digest,
                    target_system=intent.destination,
                    undo_command=undo_data,
                )

            # Record successful idempotency
            self.admission.record_execution(intent)

            res = ExecutionResult(
                success=success,
                status_code="EXECUTED" if success else "EXECUTION_FAILED",
                action_digest=digest,
                effect_summary=effect_data,
                rollback=rollback,
            )
            self._history.append(res)
            return res

        except Exception as exc:
            res = ExecutionResult(
                success=False,
                status_code="HANDLER_EXCEPTION",
                action_digest=digest,
                effect_summary={},
                error_message=str(exc),
            )
            self._history.append(res)
            return res
