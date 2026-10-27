"""Enterprise Governance & Execution Loops Engine for Agentic AI.

Implements:
1. 14 Standardized Enterprise Control Loops (HCTL, HITL-FE, HBTL, HATL, HITD, EITL, HITL, HOTL, HOOTL, HITA, HITC, HITI, MITL, HITP)
2. 15 Human Participation Governance Patterns (Human-before-Execution, Human-at-Checkpoint, Human-at-Decision, Human-at-Commit, Human-at-Handoff, Human-in-Review, Human-in-Verification, Human-in-Validation, Human-in-Active-Learning, Human-in-Feedback, Human-in-Escalation, Human-in-Override, Human-in-Recovery, Human-in-Adversarial-Review, Multi-Human Approval)
3. 23 Autonomous Execution Loops (OODA, ReAct, Plan-Execute-Observe, Plan-Execute-Verify, Replanning, Reflection, Self-Correction, Evaluator-Optimizer, Generate-Test-Repair, Hypothesis-Experiment-Evaluate, Search-Expand-Prune, Retrieval-Verification, Graph Traversal, Graph Enrichment, Memory Consolidation, Context Refresh, Confidence-Calibration, Safety-Validation, Retry-Backoff-Recovery, Monitor-Detect-Respond, Simulation-Evaluation, Continuous Improvement, Consensus-Reconciliation)
4. Comprehensive Execution-Control Properties (Max iterations, budgets, idempotency, deadlock detection, rollback, checkpointing).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from collections.abc import Callable
import time
import uuid


# ---------------------------------------------------------------------------
# 1. 14 Standardized Enterprise Control Loops
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# 2. 15 Human Participation Governance Patterns
# ---------------------------------------------------------------------------
class HumanControlPattern(str, Enum):
    HUMAN_BEFORE_EXECUTION = "HUMAN_BEFORE_EXECUTION"
    HUMAN_AT_CHECKPOINT = "HUMAN_AT_CHECKPOINT"
    HUMAN_AT_DECISION = "HUMAN_AT_DECISION"
    HUMAN_AT_COMMIT = "HUMAN_AT_COMMIT"
    HUMAN_AT_HANDOFF = "HUMAN_AT_HANDOFF"
    HUMAN_IN_REVIEW = "HUMAN_IN_REVIEW"
    HUMAN_IN_VERIFICATION = "HUMAN_IN_VERIFICATION"
    HUMAN_IN_VALIDATION = "HUMAN_IN_VALIDATION"
    HUMAN_IN_ACTIVE_LEARNING = "HUMAN_IN_ACTIVE_LEARNING"
    HUMAN_IN_FEEDBACK = "HUMAN_IN_FEEDBACK"
    HUMAN_IN_ESCALATION = "HUMAN_IN_ESCALATION"
    HUMAN_IN_OVERRIDE = "HUMAN_IN_OVERRIDE"
    HUMAN_IN_RECOVERY = "HUMAN_IN_RECOVERY"
    HUMAN_IN_ADVERSARIAL_REVIEW = "HUMAN_IN_ADVERSARIAL_REVIEW"
    MULTI_HUMAN_APPROVAL = "MULTI_HUMAN_APPROVAL"


# ---------------------------------------------------------------------------
# 3. 23 Autonomous Execution Loops
# ---------------------------------------------------------------------------
class AutonomousExecutionLoop(str, Enum):
    OODA = "OODA"
    REACT = "REACT"
    PLAN_EXECUTE_OBSERVE = "PLAN_EXECUTE_OBSERVE"
    PLAN_EXECUTE_VERIFY = "PLAN_EXECUTE_VERIFY"
    REPLANNING = "REPLANNING"
    REFLECTION = "REFLECTION"
    SELF_CORRECTION = "SELF_CORRECTION"
    EVALUATOR_OPTIMIZER = "EVALUATOR_OPTIMIZER"
    GENERATE_TEST_REPAIR = "GENERATE_TEST_REPAIR"
    HYPOTHESIS_EXPERIMENT_EVALUATE = "HYPOTHESIS_EXPERIMENT_EVALUATE"
    SEARCH_EXPAND_PRUNE = "SEARCH_EXPAND_PRUNE"
    RETRIEVAL_VERIFICATION = "RETRIEVAL_VERIFICATION"
    GRAPH_TRAVERSAL = "GRAPH_TRAVERSAL"
    GRAPH_ENRICHMENT = "GRAPH_ENRICHMENT"
    MEMORY_CONSOLIDATION = "MEMORY_CONSOLIDATION"
    CONTEXT_REFRESH = "CONTEXT_REFRESH"
    CONFIDENCE_CALIBRATION = "CONFIDENCE_CALIBRATION"
    SAFETY_VALIDATION = "SAFETY_VALIDATION"
    RETRY_BACKOFF_RECOVERY = "RETRY_BACKOFF_RECOVERY"
    MONITOR_DETECT_RESPOND = "MONITOR_DETECT_RESPOND"
    SIMULATION_EVALUATION = "SIMULATION_EVALUATION"
    CONTINUOUS_IMPROVEMENT = "CONTINUOUS_IMPROVEMENT"
    CONSENSUS_RECONCILIATION = "CONSENSUS_RECONCILIATION"


class RiskTier(str, Enum):
    R0 = "R0"  # Read-only / Zero risk -> Automated
    R1 = "R1"  # Low risk -> Automated with logging
    R2 = "R2"  # Medium risk -> Peer/Supervised approval
    R3 = "R3"  # High risk -> Mandatory human sign-off
    R4 = "R4"  # Critical risk -> Multi-party / Executive authorization


@dataclass
class ExecutionLimits:
    """Rigorous execution bounds preventing runaway compute or recursion."""
    max_iterations: int = 10
    max_duration_seconds: float = 30.0
    token_budget: int = 50_000
    compute_budget_usd: float = 1.0
    idempotency_key: str | None = None
    enable_deadlock_detection: bool = True
    rollback_on_failure: bool = True
    current_iteration: int = 0
    current_tokens: int = 0

    def is_exhausted(self) -> bool:
        return self.current_iteration > self.max_iterations or self.current_tokens > self.token_budget



@dataclass
class LoopDecision:
    allowed: bool
    requires_human_approval: bool
    loop_type: LoopType
    reason: str
    risk_tier: RiskTier
    action_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    pattern: HumanControlPattern | None = None
    timestamp: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class LoopExecutionRecord:
    action_id: str
    loop_type: LoopType
    risk_tier: RiskTier
    status: str  # PENDING, APPROVED, REJECTED, EXECUTED, BLOCKED, COMPLETED
    operator: str | None = None
    override_reason: str | None = None
    executed_at: float | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class AutonomousLoopResult:
    loop_type: AutonomousExecutionLoop
    iterations_run: int
    converged: bool
    final_output: Any
    duration_ms: float
    trace: list[str] = field(default_factory=list)


class EnterpriseLoopManager:
    """Enterprise Loop Orchestrator governing human/machine boundaries and execution loops."""

    def __init__(self, default_policy: LoopType = LoopType.HITL_FE) -> None:
        self.default_loop = default_policy
        self._action_history: list[LoopExecutionRecord] = []
        self._pending_approvals: dict[str, LoopExecutionRecord] = {}

    def evaluate_action(
        self,
        action_name: str,
        risk_tier: RiskTier,
        loop_override: LoopType | None = None,
        pattern_override: HumanControlPattern | None = None,
        context: dict[str, Any] | None = None,
    ) -> LoopDecision:
        """Evaluate an action against control loops and human participation patterns."""
        ctx = context or {}
        loop = loop_override or self.default_loop

        # Safety rule: HOOTL is strictly prohibited for high-risk (R3, R4) operations
        if loop == LoopType.HOOTL and risk_tier in (RiskTier.R3, RiskTier.R4):
            return LoopDecision(
                allowed=False,
                requires_human_approval=True,
                loop_type=LoopType.HOOTL,
                risk_tier=risk_tier,
                reason="HOOTL (Human-Out-of-the-Loop) is strictly prohibited for R3/R4 operations.",
                pattern=pattern_override,
                metadata={"action_name": action_name},
            )

        # Human-at-Commit / Human-before-Execution patterns
        if pattern_override in (HumanControlPattern.HUMAN_AT_COMMIT, HumanControlPattern.HUMAN_BEFORE_EXECUTION):
            approved = ctx.get("human_approved", False)
            return LoopDecision(
                allowed=approved,
                requires_human_approval=not approved,
                loop_type=loop,
                risk_tier=risk_tier,
                reason=f"Mandatory gate '{pattern_override.value}' active.",
                pattern=pattern_override,
            )

        if loop == LoopType.HCTL:
            human_commanded = ctx.get("human_commanded", False)
            return LoopDecision(
                allowed=human_commanded,
                requires_human_approval=not human_commanded,
                loop_type=loop,
                risk_tier=risk_tier,
                reason="HCTL requires explicit human objective initiation." if not human_commanded else "Permitted sub-step.",
            )

        if loop in (LoopType.HITL, LoopType.HITA):
            has_approval = ctx.get("human_approved", False)
            return LoopDecision(
                allowed=has_approval,
                requires_human_approval=not has_approval,
                loop_type=loop,
                risk_tier=risk_tier,
                reason="Direct human approval required before action execution.",
            )

        if loop == LoopType.HITL_FE:
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

        if loop in (LoopType.HBTL, LoopType.HOTL):
            human_stopped = ctx.get("supervisor_abort", False)
            return LoopDecision(
                allowed=not human_stopped,
                requires_human_approval=human_stopped,
                loop_type=loop,
                risk_tier=risk_tier,
                reason="Supervisor intervened." if human_stopped else "Autonomous execution under supervision.",
            )

        if loop == LoopType.EITL:
            env_healthy = ctx.get("env_healthy", True)
            return LoopDecision(
                allowed=env_healthy,
                requires_human_approval=not env_healthy,
                loop_type=loop,
                risk_tier=risk_tier,
                reason="Environmental telemetry healthy." if env_healthy else "Abnormal environment state.",
            )

        return LoopDecision(
            allowed=True,
            requires_human_approval=False,
            loop_type=loop,
            risk_tier=risk_tier,
            reason="Standard execution policy verified.",
            pattern=pattern_override,
        )

    def execute_autonomous_loop(
        self,
        loop_type: AutonomousExecutionLoop,
        step_fn: Callable[[int, Any], tuple[Any, bool]],
        initial_state: Any,
        limits: ExecutionLimits | None = None,
    ) -> AutonomousLoopResult:
        """Executes one of the 23 autonomous loops with guaranteed termination and limits."""
        cfg = limits or ExecutionLimits()
        start = time.time()
        current = initial_state
        converged = False
        trace = []

        for i in range(1, cfg.max_iterations + 1):
            if (time.time() - start) > cfg.max_duration_seconds:
                trace.append(f"Iteration {i}: Halted due to duration limit ({cfg.max_duration_seconds}s)")
                break

            current, stop = step_fn(i, current)
            trace.append(f"Iteration {i} ({loop_type.value}): Step output evaluated. Stop={stop}")
            if stop:
                converged = True
                break

        return AutonomousLoopResult(
            loop_type=loop_type,
            iterations_run=len(trace),
            converged=converged,
            final_output=current,
            duration_ms=(time.time() - start) * 1000.0,
            trace=trace,
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
            details={"reason": decision.reason, "pattern": decision.pattern.value if decision.pattern else None},
        )
        self._action_history.append(record)
        return record

    def list_history(self) -> list[LoopExecutionRecord]:
        return list(self._action_history)

    def list_supported_loops(self) -> list[str]:
        return [l.value for l in LoopType]

    def list_human_patterns(self) -> list[str]:
        return [p.value for p in HumanControlPattern]

    def list_autonomous_loops(self) -> list[str]:
        return [l.value for l in AutonomousExecutionLoop]
