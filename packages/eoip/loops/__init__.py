"""Composable bounded-execution-loop library (GAP-LOOP-001..047, §2, §34).

Public API:

* ``eoip.loops.core`` — ``LoopDriver`` bounded engine, ``LoopConfig``
  envelope, ``JsonCheckpointStore`` durable JSON checkpoints,
  ``StepOutcome``/``StepSignal``, ``LoopResult``/``LoopMetrics``,
  termination reasons, stable ``LoopError`` categories.
* ``eoip.loops.drivers`` — the 23 loop primitives (§2) as phase
  schedules: ``run_ooda_loop`` … ``run_consensus_reconciliation_loop``,
  plus ``LOOP_PHASES`` / ``LOOP_RUNNERS`` / ``run_loop`` dispatch.
* ``eoip.loops.approval`` — the 15 human-participation patterns
  (GAP-LOOP-033..047): ``HumanPattern``, ``ApprovalPolicy`` (who/what/
  conditions/evidence), ``PolicyGate``, ``AuthzGate`` (eoip.authz
  adapter), ``ApprovalQueue`` (External gate for human delivery),
  ``make_decision``, ``gates_for``.
* ``eoip.loops.router`` — ``build_router()`` FastAPI surface under
  ``/api/v1/loops`` (wired by apps/api, not registered here).

All loops are deterministic-first: no network, no mandatory LLM.
"""

from eoip.loops.approval import (
    ApprovalPolicy,
    ApprovalQueue,
    ApprovalRecord,
    ApprovalRequest,
    Approver,
    AuthzGate,
    GateDecision,
    HumanPattern,
    InMemoryApprovalQueue,
    PolicyGate,
    gates_for,
    make_decision,
)
from eoip.loops.core import (
    ApprovalDenied,
    BudgetExceeded,
    CheckpointRecord,
    Compensation,
    GateVerdict,
    JsonCheckpointStore,
    LoopConfig,
    LoopDriver,
    LoopError,
    LoopMetrics,
    LoopResult,
    LoopStatus,
    StepContext,
    StepOutcome,
    StepSignal,
    TerminationReason,
    new_run_id,
    state_fingerprint,
)
from eoip.loops.drivers import LOOP_PHASES, LOOP_RUNNERS, run_loop

__all__ = [
    "ApprovalDenied",
    "ApprovalPolicy",
    "ApprovalQueue",
    "ApprovalRecord",
    "ApprovalRequest",
    "Approver",
    "AuthzGate",
    "BudgetExceeded",
    "CheckpointRecord",
    "Compensation",
    "GateDecision",
    "GateVerdict",
    "HumanPattern",
    "InMemoryApprovalQueue",
    "JsonCheckpointStore",
    "LOOP_PHASES",
    "LOOP_RUNNERS",
    "LoopConfig",
    "LoopDriver",
    "LoopError",
    "LoopMetrics",
    "LoopResult",
    "LoopStatus",
    "PolicyGate",
    "StepContext",
    "StepOutcome",
    "StepSignal",
    "TerminationReason",
    "gates_for",
    "make_decision",
    "new_run_id",
    "run_loop",
    "state_fingerprint",
]
