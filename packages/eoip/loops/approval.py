"""Human-participation / approval-gate framework (GAP-LOOP-033..047, §2).

The 15 human-participation patterns are gate *placements* over one
policy engine: **who** can approve **what** (permission/action) **under
which conditions** (ABAC-style attributes + required evidence) **with
what resume semantics** (allow / deny / park-awaiting-human).

Patterns (§2): Human-before-Execution, Human-at-Checkpoint,
Human-at-Decision, Human-at-Commit, Human-at-Handoff, Human-in-Review,
Human-in-Verification, Human-in-Validation, Human-in-Active-Learning,
Human-in-Feedback, Human-in-Escalation, Human-in-Override,
Human-in-Recovery, Human-in-Adversarial-Review, Multi-Human-Approval.

Integration with ``eoip.authz``: an ``AuthzGate`` adapts any
``eoip.authz.PolicyEnforcer`` decision into a gate verdict, so "who can
approve what" reuses the RBAC/ABAC catalog (``agents:approve``).

External gate: delivery of a parked approval request to a real human
(inbox/ticket/UI) is out of scope here; ``ApprovalQueue`` exposes the
interface and an in-memory reference implementation.
"""

from __future__ import annotations

import time
import uuid
from enum import Enum
from typing import Any, Protocol
from collections.abc import Callable, Iterable

from pydantic import BaseModel, ConfigDict, Field

from eoip.loops.core import ApprovalGateProtocol, GateVerdict


class HumanPattern(str, Enum):
    """The 15 human-participation patterns (GAP-LOOP-033..047, §2)."""

    BEFORE_EXECUTION = "human_before_execution"
    AT_CHECKPOINT = "human_at_checkpoint"
    AT_DECISION = "human_at_decision"
    AT_COMMIT = "human_at_commit"
    AT_HANDOFF = "human_at_handoff"
    IN_REVIEW = "human_in_review"
    IN_VERIFICATION = "human_in_verification"
    IN_VALIDATION = "human_in_validation"
    IN_ACTIVE_LEARNING = "human_in_active_learning"
    IN_FEEDBACK = "human_in_feedback"
    IN_ESCALATION = "human_in_escalation"
    IN_OVERRIDE = "human_in_override"
    IN_RECOVERY = "human_in_recovery"
    IN_ADVERSARIAL_REVIEW = "human_in_adversarial_review"
    MULTI_HUMAN_APPROVAL = "multi_human_approval"


class GateDecision(str, Enum):
    """Resume semantics of a human decision."""

    APPROVE = "approve"
    DENY = "deny"
    ESCALATE = "escalate"


# ---------------------------------------------------------------------------
# Policy: who can approve what, under which conditions, with what evidence
# ---------------------------------------------------------------------------


class ApprovalPolicy(BaseModel):
    """One approval rule (GAP-LOOP-034, §2 policy = who/what/conditions/evidence).

    ``allowed_roles`` — *who* (caller-provided identity roles).
    ``action`` — *what* (permission string, e.g. ``agents:approve``).
    ``conditions`` — *under which conditions*: flat attribute equality
    checks against the gate context (e.g. ``{"classification": "restricted"}``
    requires the context to carry that value, or a ``*`` wildcard).
    ``required_evidence`` — evidence keys the approver must supply.
    ``min_approvals`` — >1 realizes Multi-Human-Approval.
    """

    model_config = ConfigDict(extra="forbid")

    policy_id: str
    action: str
    pattern: HumanPattern = HumanPattern.AT_DECISION
    allowed_roles: list[str] = Field(default_factory=list)
    conditions: dict[str, str] = Field(default_factory=dict)
    required_evidence: list[str] = Field(default_factory=list)
    min_approvals: int = Field(default=1, ge=1)
    description: str | None = None


class Approver(BaseModel):
    """Identity presenting for approval (roles are caller-supplied)."""

    model_config = ConfigDict(extra="forbid")

    subject: str
    roles: list[str] = Field(default_factory=list)
    attributes: dict[str, str] = Field(default_factory=dict)


class ApprovalRequest(BaseModel):
    """A concrete approval ask (URN-identified, auditable)."""

    model_config = ConfigDict(extra="forbid")

    request_id: str
    policy_id: str
    action: str
    pattern: HumanPattern
    context: dict[str, Any] = Field(default_factory=dict)
    created_at: float = 0.0


class ApprovalRecord(BaseModel):
    """One recorded human decision with evidence (§48 auditability)."""

    model_config = ConfigDict(extra="forbid")

    request_id: str
    decision: GateDecision
    approver: str
    roles: list[str] = Field(default_factory=list)
    evidence: dict[str, Any] = Field(default_factory=dict)
    reason: str | None = None
    decided_at: float = 0.0


def new_request_id() -> str:
    return f"urn:eoip:loop:approval:{uuid.uuid4().hex[:16]}"


class PolicyGate(ApprovalGateProtocol):
    """Evaluates an ``ApprovalPolicy`` against a presented identity.

    Decisions: ``allow`` (policy satisfied + approvals recorded),
    ``deny`` (policy violated or human denied), ``park`` (needs a human;
    request is queued). This is the deterministic gate used by the loop
    driver; delivery to humans is via ``ApprovalQueue`` (External gate).
    """

    def __init__(
        self,
        policy: ApprovalPolicy,
        queue: ApprovalQueue | None = None,
        roles_of: Callable[[str], Iterable[str]] | None = None,
    ) -> None:
        self._policy = policy
        self._queue = queue or InMemoryApprovalQueue()
        self._roles_of = roles_of

    @property
    def policy(self) -> ApprovalPolicy:
        return self._policy

    def _roles(self, context: dict[str, Any]) -> set[str]:
        if "approver_roles" in context:
            return set(context["approver_roles"])
        if "approver" in context and self._roles_of is not None:
            return set(self._roles_of(context["approver"]))
        return set()

    def evaluate(self, *, gate: str, context: dict[str, Any]) -> GateVerdict:
        policy = self._policy
        # conditions: every required attribute must match the context
        for key, expected in policy.conditions.items():
            actual = context.get(key)
            if expected != "*" and str(actual) != expected:
                return GateVerdict(decision="allow", gate=gate, reason="condition not applicable")

        needs_recorded_human_decision = bool(policy.required_evidence) or policy.min_approvals > 1

        # look for recorded human decisions
        request_id = context.get("approval_request_id")
        records = self._queue.decisions_for(request_id) if request_id else []
        approvals = [
            r
            for r in records
            if (
                r.decision == GateDecision.APPROVE
                and self._evidence_ok(r)
                and self._approver_roles_ok(r.roles)
            )
        ]
        denials = [r for r in records if r.decision == GateDecision.DENY]
        if denials:
            return GateVerdict(decision="deny", gate=gate, reason=denials[-1].reason or "denied by human")
        if len(approvals) >= policy.min_approvals:
            return GateVerdict(
                decision="allow",
                gate=gate,
                approver=approvals[-1].approver,
                evidence=approvals[-1].evidence,
                reason="approved",
            )
        if request_id:
            return GateVerdict(decision="park", gate=gate, reason=f"awaiting:{request_id}")

        roles = self._roles(context)
        if policy.allowed_roles and not roles.intersection(policy.allowed_roles):
            if needs_recorded_human_decision:
                request = self.request(context)
                return GateVerdict(decision="park", gate=gate, reason=f"queued:{request.request_id}")
            return GateVerdict(decision="deny", gate=gate, reason="approver lacks required role")

        if not policy.allowed_roles:
            request = self.request(context)
            return GateVerdict(decision="park", gate=gate, reason=f"queued:{request.request_id}")

        if not needs_recorded_human_decision:
            return GateVerdict(decision="allow", gate=gate, reason="policy satisfied")

        # park: queue a request for a human (External gate: delivery)
        request = self.request(context)
        return GateVerdict(decision="park", gate=gate, reason=f"queued:{request.request_id}")

    def _evidence_ok(self, record: ApprovalRecord) -> bool:
        return all(key in record.evidence for key in self._policy.required_evidence)

    def _approver_roles_ok(self, roles: Iterable[str]) -> bool:
        return not self._policy.allowed_roles or bool(set(roles).intersection(self._policy.allowed_roles))

    def request(self, context: dict[str, Any]) -> ApprovalRequest:
        req = ApprovalRequest(
            request_id=new_request_id(),
            policy_id=self._policy.policy_id,
            action=self._policy.action,
            pattern=self._policy.pattern,
            context=dict(context),
            created_at=time.time(),
        )
        self._queue.submit(req)
        return req


class AuthzGate(ApprovalGateProtocol):
    """Adapts an ``eoip.authz.PolicyEnforcer`` into an approval gate.

    Deny propagates as ``deny``; allow propagates as ``allow``; a
    missing approver context parks the run (§2 human-interrupt gates).
    External gate: identity resolution is the caller's responsibility.
    """

    def __init__(self, enforcer: Any, *, permission: str = "agents:approve") -> None:
        self._enforcer = enforcer
        self._permission = permission

    def evaluate(self, *, gate: str, context: dict[str, Any]) -> GateVerdict:
        user = context.get("authz_user")
        if user is None:
            return GateVerdict(decision="park", gate=gate, reason="no authenticated approver")
        decision = self._enforcer.enforce(user, self._permission, context.get("resource") or {})
        if getattr(decision, "allow", False):
            return GateVerdict(decision="allow", gate=gate, approver=getattr(user, "user_id", None))
        return GateVerdict(decision="deny", gate=gate, reason=str(getattr(decision, "reasons", "denied")))


# ---------------------------------------------------------------------------
# Approval queue (External gate: human delivery channel is out of scope)
# ---------------------------------------------------------------------------


class ApprovalQueue(Protocol):
    """Interface for parked-approval delivery and decision collection."""

    def submit(self, request: ApprovalRequest) -> None: ...

    def decide(self, request_id: str, record: ApprovalRecord) -> None: ...

    def pending(self) -> list[ApprovalRequest]: ...

    def decisions_for(self, request_id: str | None) -> list[ApprovalRecord]: ...


class InMemoryApprovalQueue:
    """Reference implementation; swap for a ticket/inbox-backed queue."""

    def __init__(self) -> None:
        self._pending: dict[str, ApprovalRequest] = {}
        self._decisions: dict[str, list[ApprovalRecord]] = {}

    def submit(self, request: ApprovalRequest) -> None:
        self._pending[request.request_id] = request

    def decide(self, request_id: str, record: ApprovalRecord) -> None:
        self._decisions.setdefault(request_id, []).append(record)
        self._pending.pop(request_id, None)

    def pending(self) -> list[ApprovalRequest]:
        return list(self._pending.values())

    def decisions_for(self, request_id: str | None) -> list[ApprovalRecord]:
        if request_id is None:
            return []
        return list(self._decisions.get(request_id, []))


def make_decision(
    request: ApprovalRequest,
    approver: Approver,
    decision: GateDecision,
    *,
    evidence: dict[str, Any] | None = None,
    reason: str | None = None,
) -> ApprovalRecord:
    """Build an auditable decision record for ``queue.decide``."""
    return ApprovalRecord(
        request_id=request.request_id,
        decision=decision,
        approver=approver.subject,
        roles=list(approver.roles),
        evidence=dict(evidence or {}),
        reason=reason,
        decided_at=time.time(),
    )


def gates_for(pattern: HumanPattern, policies: Iterable[ApprovalPolicy], **kwargs: Any) -> list[PolicyGate]:
    """Instantiate gates for every policy bound to a participation pattern."""
    return [PolicyGate(p, **kwargs) for p in policies if p.pattern == pattern]
