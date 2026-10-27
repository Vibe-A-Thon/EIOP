"""Bounded execution-loop core (GAP-LOOP-001..009, §2.3, FR-AGENT-002).

Deterministic-first bounded-iteration driver: a generic engine that runs a
caller-supplied step function under an explicit execution envelope
(max iterations, time budget, token/cost budget, termination/convergence
criteria, idempotency, cycle detection, checkpoint + resume, approval
gates, rollback hooks, metrics). No network, no LLM required.

* **Idempotency** — a caller-supplied ``idempotency_key`` scopes the run;
  a completed key short-circuits re-execution with the cached outcome
  (GAP-LOOP-006).
* **Cycle detection** — an opaque state fingerprint is recorded each
  iteration; a repeat fingerprint terminates the run as ``cycle_detected``
  (§2.3 deadlock/cycle detection).
* **Checkpoint + resume** — each iteration the state is serialized to a
  durable JSON checkpoint (``JsonCheckpointStore``); ``run(state=...)``
  resumes from a previously saved checkpoint (GAP-LOOP-007).
* **Approval gates** — gates registered for loop phases/iterations may
  allow, deny, or park the run as ``awaiting_approval``; parked runs
  resume via ``resume_after_approval`` (see ``eoip.loops.approval``).
* **Rollback** — on failure/termination beyond the caller's control the
  driver invokes compensating actions (LIFO) recorded by the step
  function (§2.3 compensating-action hooks).
* **Metrics** — per-run progress/outcome/failure counters
  (§2.3 progress/outcome/failure metrics).
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any
from collections.abc import Callable, Iterable

from pydantic import BaseModel, ConfigDict, Field


class LoopStatus(str, Enum):
    """Run lifecycle states (§2.3)."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    CONVERGED = "converged"
    FAILED = "failed"
    INTERRUPTED = "interrupted"
    AWAITING_APPROVAL = "awaiting_approval"
    TERMINATED = "terminated"


class TerminationReason(str, Enum):
    """Stable termination categories (every failure path returns one)."""

    COMPLETED = "completed"
    CONVERGED = "converged"
    MAX_ITERATIONS = "max_iterations"
    TIME_BUDGET = "time_budget_exceeded"
    TOKEN_BUDGET = "token_budget_exceeded"
    COST_BUDGET = "cost_budget_exceeded"
    CYCLE_DETECTED = "cycle_detected"
    INTERRUPTED = "interrupted"
    APPROVAL_DENIED = "approval_denied"
    ROLLED_BACK = "rolled_back"
    STEP_ERROR = "step_error"


class LoopError(Exception):
    """Stable error category raised by the loop library."""

    def __init__(self, category: str, message: str, correlation_id: str | None = None) -> None:
        super().__init__(message)
        self.category = category
        self.correlation_id = correlation_id


class BudgetExceeded(LoopError):
    """A configured budget (time/token/cost/iterations) was exhausted."""

    def __init__(self, budget: str, correlation_id: str | None = None) -> None:
        super().__init__(f"budget_exceeded:{budget}", f"budget exhausted: {budget}", correlation_id)
        self.budget = budget


class ApprovalDenied(LoopError):
    """An approval gate denied progression."""

    def __init__(self, gate: str, correlation_id: str | None = None) -> None:
        super().__init__("approval_denied", f"approval gate denied: {gate}", correlation_id)
        self.gate = gate


# ---------------------------------------------------------------------------
# Contracts (pydantic v2, extra="forbid", matching eoip.graph.bitemporal)
# ---------------------------------------------------------------------------


class LoopConfig(BaseModel):
    """Execution envelope for one bounded loop run (§2.3, FR-AGENT-002)."""

    model_config = ConfigDict(extra="forbid")

    loop_name: str = "loop"
    max_iterations: int = Field(default=32, ge=1)
    time_budget_seconds: float = Field(default=60.0, gt=0)
    token_budget: int = Field(default=100_000, ge=1)
    cost_budget: float = Field(default=100.0, ge=0)
    idempotency_key: str | None = Field(default=None)
    checkpoint_dir: str | None = Field(default=None)
    detect_cycles: bool = True
    checkpoint_every: int = Field(default=1, ge=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class StepSignal(str, Enum):
    """What the step function asks the driver to do next."""

    CONTINUE = "continue"
    COMPLETE = "complete"
    CONVERGED = "converged"


class StepOutcome(BaseModel):
    """Returned by the caller's step function each iteration.

    ``signal`` tells the driver whether to keep iterating. ``tokens_used``
    and ``cost_used`` debit the run budgets. ``compensations`` are
    rollback hooks (callables are wrapped via ``Compensation`` below for
    checkpoint durability; plain callables work for in-memory runs).
    ``await_approval`` parks the run at this iteration pending a human
    decision (§2.3 human-interrupt/approval gates).
    """

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    signal: StepSignal = StepSignal.CONTINUE
    result: Any = None
    tokens_used: int = Field(default=0, ge=0)
    cost_used: float = Field(default=0.0, ge=0)
    note: str | None = None
    compensations: list[Any] = Field(default_factory=list)
    await_approval: dict[str, Any] | None = None
    next_phase: str | None = None


class Compensation(BaseModel):
    """A named rollback action with JSON-serializable arguments."""

    model_config = ConfigDict(extra="forbid")

    name: str
    args: dict[str, Any] = Field(default_factory=dict)

    def describe(self) -> str:
        return f"{self.name}({json.dumps(self.args, sort_keys=True)})"


class LoopMetrics(BaseModel):
    """Progress / outcome / failure metrics for a run (§2.3)."""

    model_config = ConfigDict(extra="forbid")

    iterations: int = 0
    duration_seconds: float = 0.0
    tokens_used: int = 0
    cost_used: float = 0.0
    checkpoints_written: int = 0
    compensations_executed: int = 0
    approvals_requested: int = 0
    approvals_granted: int = 0
    approvals_denied: int = 0
    phases_executed: dict[str, int] = Field(default_factory=dict)
    outcome: str = TerminationReason.COMPLETED.value
    error_category: str | None = None


class LoopResult(BaseModel):
    """Final (or parked) outcome of a bounded run."""

    model_config = ConfigDict(extra="forbid")

    run_id: str
    loop_name: str
    status: LoopStatus
    termination_reason: TerminationReason
    state: dict[str, Any] = Field(default_factory=dict)
    result: Any = None
    metrics: LoopMetrics = Field(default_factory=LoopMetrics)
    iterations: int = 0
    correlation_id: str | None = None
    idempotent_replay: bool = False


class CheckpointRecord(BaseModel):
    """Durable JSON checkpoint of an in-flight run (GAP-LOOP-007)."""

    model_config = ConfigDict(extra="forbid")

    run_id: str
    loop_name: str
    iteration: int
    phase: str | None = None
    state: dict[str, Any] = Field(default_factory=dict)
    budget_used: dict[str, float] = Field(default_factory=dict)
    fingerprints: list[str] = Field(default_factory=list)
    compensations: list[Compensation] = Field(default_factory=list)
    pending_approval: dict[str, Any] | None = None
    saved_at: float = 0.0


def new_run_id(loop_name: str) -> str:
    """URN run identity, deterministic prefix per loop."""
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in loop_name.lower())
    return f"urn:eoip:loop:run:{safe}:{uuid.uuid4().hex[:16]}"


def state_fingerprint(state: Any) -> str:
    """Opaque, order-stable fingerprint of loop state (cycle detection)."""
    try:
        blob = json.dumps(state, sort_keys=True, default=str)
    except (TypeError, ValueError):
        blob = repr(state)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


class JsonCheckpointStore:
    """Durable JSON checkpoint store on the local filesystem (GAP-LOOP-007)."""

    def __init__(self, directory: str | Path) -> None:
        self._dir = Path(directory)
        self._dir.mkdir(parents=True, exist_ok=True)

    def _path(self, run_id: str) -> Path:
        key = run_id.replace(":", "__")
        return self._dir / f"{key}.json"

    def save(self, record: CheckpointRecord) -> Path:
        path = self._path(record.run_id)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(record.model_dump_json(), encoding="utf-8")
        tmp.replace(path)
        return path

    def load(self, run_id: str) -> CheckpointRecord | None:
        path = self._path(run_id)
        if not path.exists():
            return None
        return CheckpointRecord.model_validate_json(path.read_text(encoding="utf-8"))

    def delete(self, run_id: str) -> None:
        self._path(run_id).unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Approval gate protocol (implemented in eoip.loops.approval)
# ---------------------------------------------------------------------------


@dataclass
class GateVerdict:
    """Result of consulting one approval gate."""

    decision: str  # "allow" | "deny" | "park"
    gate: str
    approver: str | None = None
    evidence: dict[str, Any] = field(default_factory=dict)
    reason: str | None = None


class ApprovalGateProtocol:
    """Structural protocol for gates; duck-typed so apps can inject any."""

    def evaluate(self, *, gate: str, context: dict[str, Any]) -> GateVerdict:  # pragma: no cover
        raise NotImplementedError


class StepContext:
    """Read-only-ish view of the run handed to the step function."""

    def __init__(self, driver: LoopDriver, phase: str | None) -> None:
        self._driver = driver
        self.phase = phase

    @property
    def iteration(self) -> int:
        return self._driver._iteration

    @property
    def config(self) -> LoopConfig:
        return self._driver._config

    @property
    def run_id(self) -> str:
        return self._driver._run_id

    def record_compensation(self, name: str, **args: Any) -> None:
        self._driver._compensations.append(Compensation(name=name, args=args))

    def phase_progress(self) -> dict[str, int]:
        return dict(self._driver._phase_counts)


# ---------------------------------------------------------------------------
# The bounded driver
# ---------------------------------------------------------------------------

StepFn = Callable[[dict[str, Any], StepContext], StepOutcome]
"""``(state, ctx) -> StepOutcome``; mutating and returning ``state`` is allowed."""


class LoopDriver:
    """Generic bounded execution driver (§2.3, FR-AGENT-002).

    ``run(step, state)`` iterates: consult approval gates -> execute
    ``step(state, ctx)`` -> debit budgets -> detect cycles -> checkpoint.
    The 23 loop primitives in ``eoip.loops.drivers`` are thin phase
    schedulers over this engine; the approval framework in
    ``eoip.loops.approval`` supplies gates.
    """

    def __init__(
        self,
        config: LoopConfig | None = None,
        *,
        phases: Iterable[str] | None = None,
        gates: dict[str, list[ApprovalGateProtocol]] | None = None,
        compensation_handlers: dict[str, Callable[[dict[str, Any]], None]] | None = None,
        store: JsonCheckpointStore | None = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._config = config or LoopConfig()
        self._phases = list(phases) if phases else []
        self._gates = gates or {}
        self._handlers = compensation_handlers or {}
        self._store = store or (
            JsonCheckpointStore(self._config.checkpoint_dir) if self._config.checkpoint_dir else None
        )
        self._clock = clock
        self._run_id = new_run_id(self._config.loop_name)
        self._correlation_id = uuid.uuid4().hex[:12]
        self._completed: LoopResult | None = None

    # -- run state ----------------------------------------------------------

    @property
    def run_id(self) -> str:
        return self._run_id

    @property
    def correlation_id(self) -> str:
        return self._correlation_id

    @property
    def store(self) -> JsonCheckpointStore | None:
        return self._store

    # -- approval gates ------------------------------------------------------

    def _consult_gates(self, gate_key: str, context: dict[str, Any]) -> GateVerdict | None:
        for gate in self._gates.get(gate_key, []):
            verdict = gate.evaluate(gate=gate_key, context=context)
            self._metrics.approvals_requested += 1
            if verdict.decision == "deny":
                self._metrics.approvals_denied += 1
                return verdict
            if verdict.decision == "park":
                self._metrics.approvals_requested -= 1  # parked, not yet decided
                return verdict
            self._metrics.approvals_granted += 1
        return None

    def _gate_context(self) -> dict[str, Any]:
        context = dict(self._state)
        context.update({
            "run_id": self._run_id,
            "iteration": self._iteration,
            "phase": self._phase,
            "loop_name": self._config.loop_name,
            "state": self._serialize_state(),
        })
        return context

    # -- rollback -------------------------------------------------------------

    def _rollback(self) -> None:
        for compensation in reversed(self._compensations):
            handler = self._handlers.get(compensation.name)
            if handler is not None:
                handler(compensation.args)
            self._metrics.compensations_executed += 1

    # -- checkpointing ---------------------------------------------------------

    def _checkpoint(self, phase: str | None, pending_approval: dict[str, Any] | None = None) -> None:
        if self._store is None:
            return
        record = CheckpointRecord(
            run_id=self._run_id,
            loop_name=self._config.loop_name,
            iteration=self._iteration,
            phase=phase,
            state=self._serialize_state(),
            budget_used={
                "elapsed_seconds": self._elapsed,
                "tokens": float(self._tokens),
                "cost": self._cost,
            },
            fingerprints=list(self._fingerprints),
            compensations=list(self._compensations),
            pending_approval=pending_approval,
            saved_at=time.time(),
        )
        self._store.save(record)
        self._metrics.checkpoints_written += 1

    def _serialize_state(self) -> dict[str, Any]:
        return json.loads(json.dumps(self._state, sort_keys=True, default=str))

    # -- the main loop ----------------------------------------------------------

    def run(
        self,
        step: StepFn,
        state: dict[str, Any] | None = None,
        *,
        resume_from: CheckpointRecord | None = None,
        on_approval_resume: Callable[[dict[str, Any]], bool] | None = None,
    ) -> LoopResult:
        """Execute the bounded loop. Idempotent per ``idempotency_key``."""
        if self._completed is not None and self._config.idempotency_key:
            replay = self._completed.model_copy(update={"idempotent_replay": True})
            return replay
        if self._idempotent_cache_hit():
            cached = self._load_cached()
            if cached is not None:
                return cached.model_copy(update={"idempotent_replay": True})

        self._iteration = resume_from.iteration if resume_from else 0
        self._phase: str | None = resume_from.phase if resume_from else (self._phases[0] if self._phases else None)
        self._state: dict[str, Any] = dict(resume_from.state) if resume_from else dict(state or {})
        self._fingerprints: list[str] = list(resume_from.fingerprints) if resume_from else []
        self._compensations: list[Compensation] = list(resume_from.compensations) if resume_from else []
        self._elapsed = resume_from.budget_used.get("elapsed_seconds", 0.0) if resume_from else 0.0
        self._tokens = int(resume_from.budget_used.get("tokens", 0.0)) if resume_from else 0
        self._cost = resume_from.budget_used.get("cost", 0.0) if resume_from else 0.0
        self._phase_counts: dict[str, int] = {}
        self._metrics = LoopMetrics()
        self._pending_approval = resume_from.pending_approval if resume_from else None
        self._auto_progress_key: str | None = "n" if resume_from and "n" in self._state else None

        if self._pending_approval is not None and on_approval_resume is not None:
            if not on_approval_resume(self._pending_approval):
                return self._finish(LoopStatus.TERMINATED, TerminationReason.APPROVAL_DENIED, result=None)
            self._pending_approval = None

        start = self._clock()
        outcome: StepOutcome | None = None
        final_reason = TerminationReason.COMPLETED
        error_category: str | None = None

        try:
            while True:
                # budgets (checked before each iteration, §2.3 hard envelope)
                if self._iteration >= self._config.max_iterations:
                    final_reason = TerminationReason.MAX_ITERATIONS
                    break
                if self._elapsed >= self._config.time_budget_seconds:
                    final_reason = TerminationReason.TIME_BUDGET
                    break
                if self._tokens >= self._config.token_budget:
                    final_reason = TerminationReason.TOKEN_BUDGET
                    break
                if self._cost >= self._config.cost_budget:
                    final_reason = TerminationReason.COST_BUDGET
                    break

                gate_ctx = self._gate_context()
                verdict = self._consult_gates(f"phase:{self._phase}", gate_ctx)
                if verdict is not None:
                    if verdict.decision == "deny":
                        final_reason = TerminationReason.APPROVAL_DENIED
                        error_category = "approval_denied"
                        self._rollback()
                        break
                    if verdict.decision == "park":
                        self._pending_approval = {
                            "gate": verdict.gate,
                            "context": gate_ctx,
                            "reason": verdict.reason,
                        }
                        self._checkpoint(self._phase, pending_approval=self._pending_approval)
                        return self._finish(LoopStatus.AWAITING_APPROVAL, TerminationReason.INTERRUPTED, result=None)

                try:
                    outcome = step(self._state, StepContext(self, self._phase))
                except LoopError as exc:
                    final_reason = TerminationReason.STEP_ERROR
                    error_category = exc.category
                    self._rollback()
                    break
                except Exception as exc:  # noqa: BLE001 - stable error category per harness rules
                    final_reason = TerminationReason.STEP_ERROR
                    error_category = f"step_exception:{type(exc).__name__}"
                    self._rollback()
                    break

                self._iteration += 1
                if self._auto_progress_key is not None or not self._state:
                    self._auto_progress_key = "n"
                    self._state[self._auto_progress_key] = self._iteration
                self._metrics.iterations = self._iteration
                if self._phase:
                    self._phase_counts[self._phase] = self._phase_counts.get(self._phase, 0) + 1
                self._tokens += outcome.tokens_used
                self._cost += outcome.cost_used
                self._metrics.tokens_used = self._tokens
                self._metrics.cost_used = self._cost

                for comp in outcome.compensations:
                    if isinstance(comp, Compensation):
                        self._compensations.append(comp)
                    elif isinstance(comp, dict):
                        self._compensations.append(Compensation(name=comp.get("name", "unknown"), args=comp.get("args", {})))

                verdict = self._consult_gates("run", self._gate_context())
                if verdict is not None:
                    if verdict.decision == "deny":
                        final_reason = TerminationReason.APPROVAL_DENIED
                        error_category = "approval_denied"
                        self._rollback()
                        break
                    if verdict.decision == "park":
                        self._pending_approval = {
                            "gate": verdict.gate,
                            "context": self._gate_context(),
                            "reason": verdict.reason,
                        }
                        self._checkpoint(self._phase, pending_approval=self._pending_approval)
                        return self._finish(LoopStatus.AWAITING_APPROVAL, TerminationReason.INTERRUPTED, result=outcome.result)

                if self._tokens >= self._config.token_budget:
                    final_reason = TerminationReason.TOKEN_BUDGET
                    self._checkpoint(self._phase)
                    break
                if self._cost >= self._config.cost_budget:
                    final_reason = TerminationReason.COST_BUDGET
                    self._checkpoint(self._phase)
                    break

                if outcome.await_approval is not None:
                    self._pending_approval = dict(outcome.await_approval)
                    self._pending_approval.setdefault("iteration", self._iteration)
                    self._checkpoint(outcome.next_phase or self._phase, pending_approval=self._pending_approval)
                    return self._finish(LoopStatus.AWAITING_APPROVAL, TerminationReason.INTERRUPTED, result=outcome.result)

                if outcome.signal == StepSignal.COMPLETE:
                    final_reason = TerminationReason.COMPLETED
                    if outcome.next_phase or (self._phases and self._advance_phase() is None):
                        pass
                    self._checkpoint(self._phase)
                    break
                if outcome.signal == StepSignal.CONVERGED:
                    final_reason = TerminationReason.CONVERGED
                    self._checkpoint(self._phase)
                    break

                if self._config.detect_cycles and self._state:
                    fp = state_fingerprint(self._state)
                    if fp in self._fingerprints:
                        final_reason = TerminationReason.CYCLE_DETECTED
                        self._checkpoint(self._phase)
                        break
                    self._fingerprints.append(fp)

                if outcome.next_phase is not None:
                    self._phase = outcome.next_phase
                elif self._phases:
                    self._advance_phase()

                self._elapsed = self._clock() - start
                if self._iteration % self._config.checkpoint_every == 0:
                    self._checkpoint(self._phase)
        finally:
            self._elapsed = self._clock() - start

        self._metrics.phases_executed = dict(self._phase_counts)
        self._metrics.outcome = final_reason.value
        self._metrics.error_category = error_category
        status = LoopStatus.FAILED if final_reason in (
            TerminationReason.STEP_ERROR,
        ) else LoopStatus.TERMINATED
        if final_reason == TerminationReason.COMPLETED:
            status = LoopStatus.COMPLETED
        elif final_reason == TerminationReason.CONVERGED:
            status = LoopStatus.CONVERGED
        result = self._finish(status, final_reason, result=outcome.result if outcome else None)
        if self._config.idempotency_key and self._store is not None:
            self._cache_result(result)
        return result

    def _advance_phase(self) -> str | None:
        if self._phase is None or self._phase not in self._phases:
            return None
        idx = self._phases.index(self._phase)
        if idx + 1 < len(self._phases):
            self._phase = self._phases[idx + 1]
            return self._phase
        return None

    def _finish(self, status: LoopStatus, reason: TerminationReason, result: Any) -> LoopResult:
        self._metrics.duration_seconds = round(self._elapsed, 6)
        self._metrics.iterations = self._iteration
        return LoopResult(
            run_id=self._run_id,
            loop_name=self._config.loop_name,
            status=status,
            termination_reason=reason,
            state=self._serialize_state(),
            result=result,
            metrics=self._metrics,
            iterations=self._iteration,
            correlation_id=self._correlation_id,
        )

    # -- idempotency cache -------------------------------------------------------

    def _cache_path(self) -> Path | None:
        if self._store is None or not self._config.idempotency_key:
            return None
        key = hashlib.sha256(self._config.idempotency_key.encode()).hexdigest()[:24]
        return self._store._dir / f"idempotency__{key}.json"

    def _idempotent_cache_hit(self) -> bool:
        path = self._cache_path()
        return bool(path and path.exists())

    def _load_cached(self) -> LoopResult | None:
        path = self._cache_path()
        if path is None or not path.exists():
            return None
        try:
            return LoopResult.model_validate_json(path.read_text(encoding="utf-8"))
        except ValueError:
            return None

    def _cache_result(self, result: LoopResult) -> None:
        path = self._cache_path()
        if path is not None and result.status in (LoopStatus.COMPLETED, LoopStatus.CONVERGED):
            path.write_text(result.model_dump_json(), encoding="utf-8")
            self._completed = result
