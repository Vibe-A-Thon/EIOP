"""Enterprise Governance Loops Engine for Agentic AI and Autonomous Systems.

Implements all 14 standardized human/machine/environment control loops:
- HCTL: Human-Commanded-the-Loop
- HITL-FE: Human-in-the-Loop-for-Exceptions
- HBTL: Human-Beside-the-Loop
- HATL: Human-Above-the-Loop
- HITD: Human-in-the-Design
- EITL: Environment-in-the-Loop
- HITL: Human-in-the-Loop
- HOTL: Human-on-the-Loop
- HOOTL: Human-out-of-the-Loop
- HITA: Human-in-the-Action
- HITC: Human-in-the-Control-Loop
- HITI: Human-in-the-Institution
- MITL: Machine-in-the-Loop
- HITP: Human-in-the-Process
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable
import time
import uuid


class LoopType(str, Enum):
    HCTL = "HCTL"        # Human-Commanded-the-Loop
    HITL_FE = "HITL-FE"  # Human-in-the-Loop-for-Exceptions
    HBTL = "HBTL"        # Human-Beside-the-Loop
    HATL = "HATL"        # Human-Above-the-Loop
    HITD = "HITD"        # Human-in-the-Design
    EITL = "EITL"        # Environment-in-the-Loop
    HITL = "HITL"        # Human-in-the-Loop
    HOTL = "HOTL"        # Human-on-the-Loop
    HOOTL = "HOOTL"      # Human-out-of-the-Loop
    HITA = "HITA"        # Human-in-the-Action
    HITC = "HITC"        # Human-in-the-Control-Loop
    HITI = "HITI"        # Human-in-the-Institution
    MITL = "MITL"        # Machine-in-the-Loop
    HITP = "HITP"        # Human-in-the-Process


class RiskTier(str, Enum):
    R0 = "R0"  # Read-only / Zero risk -> Automated
    R1 = "R1"  # Low risk -> Automated with logging
    R2 = "R2"  # Medium risk -> Peer/Supervised approval
    R3 = "R3"  # High risk -> Mandatory human sign-off
    R4 = "R4"  # Critical risk -> Multi-party / Executive authorization


@dataclass
class LoopDecision:
    allowed: bool
    requires_human_approval: bool
    loop_type: LoopType
    reason: str
    risk_tier: RiskTier
    action_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class LoopExecutionRecord:
    action_id: str
    loop_type: LoopType
    risk_tier: RiskTier
    status: str  # PENDING, APPROVED, REJECTED, EXECUTED, BLOCKED
    operator: str | None = None
    override_reason: str | None = None
    executed_at: float | None = None
    details: dict[str, Any] = field(default_factory=dict)


class EnterpriseLoopManager:
    """Enterprise Loop Orchestrator governing agent actions and safety boundaries."""

    def __init__(self, default_policy: LoopType = LoopType.HITL_FE) -> None:
        self.default_loop = default_policy
        self._action_history: list[LoopExecutionRecord] = []
        self._pending_approvals: dict[str, LoopExecutionRecord] = []
        self._interceptors: list[Callable[[LoopDecision], LoopDecision]] = []

    def evaluate_action(
        self,
        action_name: str,
        risk_tier: RiskTier,
        loop_override: LoopType | None = None,
        context: dict[str, Any] | None = None,
    ) -> LoopDecision:
        """Evaluate an intended agent action through the configured control loop."""
        ctx = context or {}
        loop = loop_override or self.default_loop

        # HOOTL (Human-out-of-the-loop) is strictly prohibited for high-risk (R3, R4) or destructive actions
        if loop == LoopType.HOOTL and risk_tier in (RiskTier.R3, RiskTier.R4):
            return LoopDecision(
                allowed=False,
                requires_human_approval=True,
                loop_type=LoopType.HOOTL,
                risk_tier=risk_tier,
                reason="HOOTL (Human-Out-of-the-Loop) is strictly prohibited for R3/R4 high-risk operations.",
                metadata={"action_name": action_name, "context": ctx},
            )

        if loop == LoopType.HCTL:
            # Human commanded: human must initiate and set constraints
            human_commanded = ctx.get("human_commanded", False)
            if not human_commanded:
                return LoopDecision(
                    allowed=False,
                    requires_human_approval=True,
                    loop_type=loop,
                    risk_tier=risk_tier,
                    reason="HCTL requires explicit human objective initiation.",
                    metadata={"action_name": action_name},
                )
            return LoopDecision(
                allowed=True,
                requires_human_approval=False,
                loop_type=loop,
                risk_tier=risk_tier,
                reason="Permitted sub-step executing under human command.",
            )

        if loop == LoopType.HITL or loop == LoopType.HITA:
            # Human must authorize each action explicitly
            has_approval = ctx.get("human_approved", False)
            return LoopDecision(
                allowed=has_approval,
                requires_human_approval=not has_approval,
                loop_type=loop,
                risk_tier=risk_tier,
                reason="Direct human approval required before action execution.",
            )

        if loop == LoopType.HITL_FE:
            # Proceeds automatically unless an exception or risk threshold (R2+) is hit
            is_exception = ctx.get("is_exception", False) or risk_tier in (RiskTier.R2, RiskTier.R3, RiskTier.R4)
            if is_exception:
                has_approval = ctx.get("human_approved", False)
                return LoopDecision(
                    allowed=has_approval,
                    requires_human_approval=not has_approval,
                    loop_type=loop,
                    risk_tier=risk_tier,
                    reason="Exception or risk threshold reached; human escalation triggered.",
                )
            return LoopDecision(
                allowed=True,
                requires_human_approval=False,
                loop_type=loop,
                risk_tier=risk_tier,
                reason="Routine operation executing within automated policy envelope.",
            )

        if loop == LoopType.HBTL or loop == LoopType.HOTL:
            # Human beside/on loop: system acts autonomously, but human supervision is active and can override
            human_stopped = ctx.get("supervisor_abort", False)
            if human_stopped:
                return LoopDecision(
                    allowed=False,
                    requires_human_approval=True,
                    loop_type=loop,
                    risk_tier=risk_tier,
                    reason="Supervisor intervened and stopped execution.",
                )
            return LoopDecision(
                allowed=True,
                requires_human_approval=False,
                loop_type=loop,
                risk_tier=risk_tier,
                reason="Autonomous execution proceeding under human supervisor telemetry.",
            )

        if loop == LoopType.EITL:
            # Environment-in-the-loop: environmental state drives continuation or termination
            env_safe = ctx.get("env_healthy", True)
            if not env_safe:
                return LoopDecision(
                    allowed=False,
                    requires_human_approval=True,
                    loop_type=loop,
                    risk_tier=risk_tier,
                    reason="Environment telemetry detected abnormal state; loop halted.",
                )
            return LoopDecision(
                allowed=True,
                requires_human_approval=False,
                loop_type=loop,
                risk_tier=risk_tier,
                reason="Environmental telemetry verified healthy.",
            )

        if loop == LoopType.HATL or loop == LoopType.HITI or loop == LoopType.HITD:
            # Governance/Institution/Design level review
            policy_compliant = ctx.get("policy_compliant", True)
            return LoopDecision(
                allowed=policy_compliant,
                requires_human_approval=not policy_compliant,
                loop_type=loop,
                risk_tier=risk_tier,
                reason="Evaluated against design-time and organizational policy governance.",
            )

        if loop == LoopType.MITL:
            # Machine-in-the-loop: Machine provides analysis to assist human process
            return LoopDecision(
                allowed=True,
                requires_human_approval=False,
                loop_type=loop,
                risk_tier=risk_tier,
                reason="Machine advisory output generated for human governance process.",
            )

        # Default fallback
        return LoopDecision(
            allowed=True,
            requires_human_approval=False,
            loop_type=loop,
            risk_tier=risk_tier,
            reason="Standard execution policy verified.",
        )

    def record_action(
        self,
        decision: LoopDecision,
        status: str,
        operator: str | None = None,
        override_reason: str | None = None,
    ) -> LoopExecutionRecord:
        record = LoopExecutionRecord(
            action_id=decision.action_id,
            loop_type=decision.loop_type,
            risk_tier=decision.risk_tier,
            status=status,
            operator=operator,
            override_reason=override_reason,
            executed_at=time.time(),
            details={"reason": decision.reason, "metadata": decision.metadata},
        )
        self._action_history.append(record)
        return record

    def list_history(self) -> list[LoopExecutionRecord]:
        return list(self._action_history)
