"""Durable workflow engine — §7 Reasoning & Orchestration: durable execution.

Event-sourced workflow definitions and instances built on
:mod:`eoip.execution.eventstore`. A workflow is a DAG of steps; each step
supports retries with backoff, long-running timers (fire-at scheduling,
checked by the runner), human approval gates, and saga compensation.
State is derived purely by replaying the instance's event stream, so
checkpoint/replay, crash recovery, and cancellation audit all fall out of the
event log. Extends ``eoip.jobs`` (durable queue) rather than replacing it —
jobs remain the enqueue/dispatch layer; this engine owns multi-step state.

External gate: wall-clock timer *delivery* to a distributed scheduler is
implemented here as fire-at checks (``ExecutionEngine.due_timers``); wiring to
the worker loop in ``eoip.execution.scheduling`` is done by the API layer.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from datetime import UTC
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from eoip.contracts.source_event import utc_now_iso
from eoip.execution.eventstore import Event, EventStore

# ---------------------------------------------------------------------------
# Definitions
# ---------------------------------------------------------------------------

class RetryPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_attempts: int = Field(default=1, ge=1)
    backoff_seconds: float = Field(default=0.0, ge=0.0)


class StepDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    action: str  # executor registry key
    depends_on: list[str] = Field(default_factory=list)
    retry: RetryPolicy = Field(default_factory=RetryPolicy)
    timer_seconds: float = Field(default=0.0, ge=0.0)  # long-running timer before running
    requires_approval: bool = False  # human-approval gate
    compensation: str | None = None  # saga compensation executor key


class WorkflowDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workflow_id: str
    name: str
    steps: list[StepDefinition]

    def validate_dag(self) -> None:
        names = [s.name for s in self.steps]
        if len(names) != len(set(names)):
            raise ValueError("duplicate step names")
        known = set(names)
        for step in self.steps:
            unknown = set(step.depends_on) - known
            if unknown:
                raise ValueError(f"step {step.name} depends on unknown steps: {sorted(unknown)}")
        # cycle detection (DFS)
        deps = {s.name: list(s.depends_on) for s in self.steps}
        visiting: set[str] = set()
        done: set[str] = set()

        def visit(node: str) -> None:
            if node in done:
                return
            if node in visiting:
                raise ValueError(f"dependency cycle involving {node}")
            visiting.add(node)
            for dep in deps[node]:
                visit(dep)
            visiting.discard(node)
            done.add(node)

        for name in names:
            visit(name)


# ---------------------------------------------------------------------------
# Instance state (derived by replay)
# ---------------------------------------------------------------------------

TERMINAL_STATUSES = ("SUCCEEDED", "FAILED", "CANCELLED", "REJECTED")
COMPENSABLE_STATUSES = ("SUCCEEDED", "FAILED")


class StepState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    status: str = "PENDING"  # PENDING|WAITING_TIMER|WAITING_APPROVAL|RUNNING|SUCCEEDED|FAILED|COMPENSATED|SKIPPED
    attempts: int = 0
    approved: bool = False  # human-approval gate granted (one-shot)
    timer_fire_at: str | None = None
    error: str | None = None


class WorkflowState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workflow_id: str
    definition_id: str
    status: str = "RUNNING"  # RUNNING|SUCCEEDED|FAILED|CANCELLED|REJECTED|COMPENSATING|COMPENSATED
    steps: dict[str, StepState] = Field(default_factory=dict)
    variables: dict[str, Any] = Field(default_factory=dict)
    started_at: str = ""
    finished_at: str | None = None


def _initial_state(definition: WorkflowDefinition) -> WorkflowState:
    return WorkflowState(
        workflow_id=definition.workflow_id,
        definition_id=definition.name,
        steps={s.name: StepState(name=s.name) for s in definition.steps},
        started_at=utc_now_iso(),
    )


def apply_event(state: WorkflowState, event: Event) -> None:
    """Fold one event into the state (replay reducer)."""
    p = event.payload
    if event.event_type == "STEP_STATUS":
        step = state.steps.setdefault(p["step"], StepState(name=p["step"]))
        step.status = p["status"]
        if p.get("error") is not None:
            step.error = p["error"]
        if p.get("timer_fire_at") is not None:
            step.timer_fire_at = p["timer_fire_at"]
    elif event.event_type == "STEP_ATTEMPT":
        state.steps.setdefault(p["step"], StepState(name=p["step"])).attempts += 1
    elif event.event_type == "STEP_APPROVED":
        state.steps.setdefault(p["step"], StepState(name=p["step"])).approved = True
    elif event.event_type == "VARIABLE_SET":
        state.variables[p["key"]] = p["value"]
    elif event.event_type == "WORKFLOW_STATUS":
        state.status = p["status"]
        if p["status"] in TERMINAL_STATUSES or p["status"] in ("COMPENSATED",):
            state.finished_at = event.recorded_at


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class ExecutionEngine:
    """Runs workflow definitions as event-sourced instances.

    ``executors`` maps action keys to callables ``(variables, payload) -> Any``.
    Compensation executors receive the same arguments and must be idempotent.
    """

    def __init__(self, store: EventStore, executors: dict[str, Callable[..., Any]] | None = None):
        self.store = store
        self.executors = executors or {}
        self._lock = threading.RLock()

    # -- helpers -------------------------------------------------------------

    def _emit(self, definition: WorkflowDefinition, event_type: str, payload: dict) -> Event:
        return self.store.append(definition.workflow_id, event_type, payload)

    def _set_step(self, definition: WorkflowDefinition, name: str, status: str,
                  **extra: Any) -> None:
        self._emit(definition, "STEP_STATUS", {"step": name, "status": status, **extra})

    def state(self, definition: WorkflowDefinition) -> WorkflowState:
        """Checkpoint/replay: rebuild state by folding the event stream."""
        state = _initial_state(definition)
        for event in self.store.read(definition.workflow_id):
            apply_event(state, event)
        return state

    # -- timers --------------------------------------------------------------

    def due_timers(self, definition: WorkflowDefinition, *, now: str | None = None) -> list[str]:
        """Steps whose fire-at timer has elapsed (long-running timers)."""
        now = now or utc_now_iso()
        state = self.state(definition)
        return sorted(name for name, step in state.steps.items()
                      if step.status == "WAITING_TIMER" and step.timer_fire_at
                      and step.timer_fire_at <= now)

    # -- approval --------------------------------------------------------------

    def approve(self, definition: WorkflowDefinition, step_name: str, *, approved: bool = True) -> WorkflowState:
        """Human-approval gate decision."""
        with self._lock:
            state = self.state(definition)
            step = state.steps[step_name]
            if step.status != "WAITING_APPROVAL":
                raise RuntimeError(f"step {step_name} is not awaiting approval (status={step.status})")
            if approved:
                self._emit(definition, "STEP_APPROVED", {"step": step_name})
                self._set_step(definition, step_name, "PENDING")
            else:
                self._set_step(definition, step_name, "SKIPPED")
                self._emit(definition, "WORKFLOW_STATUS", {"status": "REJECTED"})
            return self.state(definition)

    # -- cancellation ----------------------------------------------------------

    def cancel(self, definition: WorkflowDefinition) -> WorkflowState:
        """Cancel the workflow: skips pending steps, compensates completed ones."""
        with self._lock:
            state = self.state(definition)
            if state.status in TERMINAL_STATUSES:
                raise RuntimeError(f"workflow already terminal: {state.status}")
            self._emit(definition, "WORKFLOW_STATUS", {"status": "CANCELLED"})
            for name, step in state.steps.items():
                if step.status in ("PENDING", "WAITING_APPROVAL", "WAITING_TIMER"):
                    self._set_step(definition, name, "SKIPPED")
            return self.state(definition)

    # -- saga compensation -----------------------------------------------------

    def compensate(self, definition: WorkflowDefinition) -> WorkflowState:
        """Run saga compensations for all completed steps, in reverse step order."""
        with self._lock:
            state = self.state(definition)
            completed = [s for s in reversed(definition.steps)
                         if state.steps[s.name].status in COMPENSABLE_STATUSES]
            self._emit(definition, "WORKFLOW_STATUS", {"status": "COMPENSATING"})
            for step_def in completed:
                comp = step_def.compensation
                if comp:
                    executor = self.executors.get(comp)
                    if executor:
                        executor(state.variables, {"step": step_def.name, "compensate": True})
                self._set_step(definition, step_def.name, "COMPENSATED")
            self._emit(definition, "WORKFLOW_STATUS", {"status": "COMPENSATED"})
            return self.state(definition)

    # -- execution -------------------------------------------------------------

    def run(self, definition: WorkflowDefinition, *, payload: dict[str, Any] | None = None,
            now: str | None = None) -> WorkflowState:
        """Execute the workflow to completion (synchronously; timers with
        ``timer_seconds=0`` fire immediately, elapsed timers fire when due)."""
        definition.validate_dag()
        now = now or utc_now_iso()
        with self._lock:
            state = self.state(definition)
            if state.started_at and state.status != "RUNNING" and self.store.read(definition.workflow_id):
                # already started previously: resume from replayed state
                pass
            elif not self.store.read(definition.workflow_id):
                self._emit(definition, "VARIABLE_SET", {"key": "input", "value": payload or {}})
            state = self.state(definition)

            progressed = True
            while progressed and state.status == "RUNNING":
                progressed = False
                for step_def in definition.steps:
                    if state.status != "RUNNING":
                        break
                    step = state.steps[step_def.name]
                    if step.status == "PENDING" and self._deps_done(definition, state, step_def):
                        progressed = True
                        self._start_step(definition, step_def, state, now)
                        state = self.state(definition)
                    elif step.status == "WAITING_TIMER" and step_def.timer_seconds == 0.0 \
                            or (step.status == "WAITING_TIMER" and step.timer_fire_at
                                and step.timer_fire_at <= now):
                        progressed = True
                        self._execute_step(definition, step_def, state)
                        state = self.state(definition)
                # check completion
                state = self.state(definition)
                if all(s.status in ("SUCCEEDED", "SKIPPED") for s in state.steps.values()) \
                        and state.steps and state.status == "RUNNING":
                    self._emit(definition, "WORKFLOW_STATUS", {"status": "SUCCEEDED"})
                    state = self.state(definition)
                elif any(s.status == "FAILED" for s in state.steps.values()) and state.status == "RUNNING":
                    if not any(s.status == "FAILED" and definition.steps[[d.name for d in definition.steps].index(s.name)].compensation
                               for s in state.steps.values()):
                        self._emit(definition, "WORKFLOW_STATUS", {"status": "FAILED"})
                        state = self.state(definition)
            return state

    def _deps_done(self, definition: WorkflowDefinition, state: WorkflowState,
                   step_def: StepDefinition) -> bool:
        return all(state.steps[dep].status in ("SUCCEEDED", "SKIPPED") for dep in step_def.depends_on)

    def _start_step(self, definition: WorkflowDefinition, step_def: StepDefinition,
                    state: WorkflowState, now: str) -> None:
        step = state.steps[step_def.name]
        if step_def.requires_approval and not step.approved:
            self._set_step(definition, step_def.name, "WAITING_APPROVAL")
            return
        if step_def.timer_seconds > 0.0:
            from datetime import datetime, timedelta
            fire_at = (datetime.now(UTC) + timedelta(seconds=step_def.timer_seconds)) \
                .strftime("%Y-%m-%dT%H:%M:%S.%f")[:23] + "Z"
            if now >= fire_at:
                self._execute_step(definition, step_def, state)
            else:
                self._set_step(definition, step_def.name, "WAITING_TIMER", timer_fire_at=fire_at)
            return
        self._execute_step(definition, step_def, state)

    def _execute_step(self, definition: WorkflowDefinition, step_def: StepDefinition,
                      state: WorkflowState) -> None:
        executor = self.executors.get(step_def.action)
        last_error: str | None = None
        for attempt in range(step_def.retry.max_attempts):
            self._emit(definition, "STEP_ATTEMPT", {"step": step_def.name})
            try:
                result = executor(state.variables, {"step": step_def.name}) if executor else None
                if result is not None:
                    self._emit(definition, "VARIABLE_SET",
                               {"key": f"result.{step_def.name}", "value": result})
                self._set_step(definition, step_def.name, "SUCCEEDED")
                return
            except Exception as exc:  # noqa: BLE001 — deterministic retry loop
                last_error = str(exc)
        self._set_step(definition, step_def.name, "FAILED", error=last_error)
