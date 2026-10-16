"""HTTP surface for the loops library (wired by apps/api; not registered here).

``build_router()`` exposes the loop catalog, a bounded run endpoint, and
the approval queue. Execution is in-process and deterministic; callers
provide the step script via the run request envelope.

Routes (all under ``/api/v1/loops``):

* ``GET  /catalog``            — the 23 loop primitives + phases (§2)
* ``POST /run/{loop_name}``    — execute one scripted bounded run
* ``GET  /approvals/pending``  — parked approval requests (External gate)
* ``POST /approvals/decide``   — record a human decision (allow/deny)
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from eoip.loops.approval import (
    ApprovalRequest,
    GateDecision,
    HumanPattern,
    InMemoryApprovalQueue,
    make_decision,
    Approver,
)
from eoip.loops.core import (
    CheckpointRecord,
    JsonCheckpointStore,
    LoopConfig,
    LoopResult,
    StepOutcome,
    StepSignal,
)
from eoip.loops.drivers import LOOP_PHASES, LOOP_RUNNERS


class LoopCatalogEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    loop_name: str
    phases: list[str]
    runner: str


class LoopCatalog(BaseModel):
    model_config = ConfigDict(extra="forbid")

    loops: list[LoopCatalogEntry] = Field(default_factory=list)
    human_patterns: list[str] = Field(default_factory=list)


class ScriptStep(BaseModel):
    """One deterministic script step: mutate state, then signal."""

    model_config = ConfigDict(extra="forbid")

    set_state: dict[str, Any] = Field(default_factory=dict)
    increment: str | None = Field(default=None, description="State counter key to increment")
    signal: StepSignal = StepSignal.CONTINUE
    tokens_used: int = 0
    cost_used: float = 0.0
    note: str | None = None
    goto_phase: str | None = Field(default=None, description="Override phase for next iteration")
    await_approval: dict[str, Any] | None = None


class RunLoopRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    config: LoopConfig = Field(default_factory=LoopConfig)
    initial_state: dict[str, Any] = Field(default_factory=dict)
    script: list[ScriptStep] = Field(default_factory=list)
    resume_run_id: str | None = None
    resume_approved: bool | None = Field(
        default=None,
        description="When resuming a parked run: True = proceed, False = deny",
    )


class DecideRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    approver: str
    roles: list[str] = Field(default_factory=list)
    decision: GateDecision
    evidence: dict[str, Any] = Field(default_factory=dict)
    reason: str | None = None


def build_router(store: JsonCheckpointStore | None = None, queue: InMemoryApprovalQueue | None = None):
    """Construct the FastAPI router for the loops library.

    The API wiring step (apps/api/app.py) calls
    ``build_router(store=None, queue=None)`` — no apps/api changes
    required in this module. Routes documented in the module docstring.
    """
    from fastapi import APIRouter, HTTPException
    from starlette.responses import JSONResponse

    router = APIRouter(prefix="/api/v1/loops", tags=["loops"])
    checkpoint_store = store or JsonCheckpointStore(".data/loops")
    approval_queue = queue or InMemoryApprovalQueue()

    @router.get("/catalog", response_model=LoopCatalog)
    def catalog() -> LoopCatalog:
        return LoopCatalog(
            loops=[
                LoopCatalogEntry(loop_name=name, phases=phases, runner=f"run_{name}_loop")
                for name, phases in sorted(LOOP_PHASES.items())
            ],
            human_patterns=[p.value for p in HumanPattern],
        )

    @router.post("/run/{loop_name}", response_model=LoopResult)
    def run_loop_http(loop_name: str, body: RunLoopRequest) -> LoopResult:
        if loop_name not in LOOP_RUNNERS:
            return JSONResponse({"detail": f"unknown loop: {loop_name}"}, status_code=404)
        script = list(body.script)
        cursor = {"i": 0}

        def step(state: dict[str, Any], ctx: Any) -> StepOutcome:
            if cursor["i"] >= len(script):
                state.setdefault("steps", 0)
                state["steps"] += 1
                if state["steps"] > len(script) + 1:
                    return StepOutcome(signal=StepSignal.COMPLETE, note="script exhausted")
                return StepOutcome(signal=StepSignal.COMPLETE if state["steps"] > 1 else StepSignal.CONTINUE)
            item = script[cursor["i"]]
            cursor["i"] += 1
            if item.increment:
                state[item.increment] = state.get(item.increment, 0) + 1
            elif "n" in state:
                state["n"] += 1
            state.update(item.set_state)
            return StepOutcome(
                signal=item.signal,
                note=item.note,
                tokens_used=item.tokens_used,
                cost_used=item.cost_used,
                next_phase=item.goto_phase,
                await_approval=item.await_approval,
            )

        config = body.config.model_copy(update={"loop_name": loop_name})
        checkpoint: CheckpointRecord | None = None
        if body.resume_run_id:
            checkpoint = checkpoint_store.load(body.resume_run_id)
            if checkpoint is None:
                raise HTTPException(status_code=404, detail=f"no checkpoint for {body.resume_run_id}")

        def on_resume(pending: dict[str, Any]) -> bool:
            return bool(body.resume_approved)

        if checkpoint is None:
            result = LOOP_RUNNERS[loop_name](
                step,
                dict(body.initial_state),
                config,
                store=checkpoint_store,
            )
        else:
            from eoip.loops.core import LoopDriver

            driver = LoopDriver(config, phases=LOOP_PHASES[loop_name], store=checkpoint_store)
            result = driver.run(step, resume_from=checkpoint, on_approval_resume=on_resume)
        if result.status.value == "failed":
            raise HTTPException(status_code=409, detail=result.metrics.error_category or "loop failed")
        return result

    @router.get("/approvals/pending", response_model=list[ApprovalRequest])
    def pending_approvals() -> list[ApprovalRequest]:
        return approval_queue.pending()

    @router.post("/approvals/decide")
    def decide(body: DecideRequest) -> dict[str, Any]:
        record = make_decision(
            ApprovalRequest(
                request_id=body.request_id,
                policy_id="api",
                action="agents:approve",
                pattern=HumanPattern.AT_DECISION,
            ),
            Approver(subject=body.approver, roles=body.roles),
            body.decision,
            evidence=body.evidence,
            reason=body.reason,
        )
        approval_queue.decide(body.request_id, record)
        return {"recorded": True, "request_id": body.request_id, "decision": body.decision.value}

    return router
