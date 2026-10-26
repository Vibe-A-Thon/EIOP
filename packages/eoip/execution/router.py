"""HTTP surface for the §7 execution layer (wired by apps/api; not here).

Routes under ``/api/v1/execution/*``:

* ``POST /workflows``                 — register/validate a workflow definition.
* ``GET  /workflows/{id}/state``      — replayed instance state.
* ``POST /workflows/{id}/run``        — execute to completion.
* ``POST /workflows/{id}/cancel``     — cancel + skip pending steps.
* ``POST /workflows/{id}/compensate`` — saga compensation run.
* ``POST /workflows/{id}/approve``    — human-approval decision.
* ``GET  /workflows/{id}/timers``     — due long-running timers.
* ``POST /queue/items``               — enqueue prioritized work.
* ``POST /queue/claim``               — lease-based claim.
* ``POST /queue/items/{id}/complete`` — complete a leased item.
* ``GET  /streams/{id}/reconcile``    — event-stream consistency report.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import APIRouter

from eoip.execution.eventstore import EventStore
from eoip.execution.scheduling import PriorityWorkQueue
from eoip.execution.workflows import ExecutionEngine, WorkflowDefinition


def build_router(executors: dict | None = None) -> APIRouter:
    """Construct the execution router bound to in-process stores."""
    from fastapi import APIRouter, HTTPException

    router = APIRouter(prefix="/api/v1/execution", tags=["execution"])
    store = EventStore()
    queue = PriorityWorkQueue()
    engine = ExecutionEngine(store, executors or {})
    definitions: dict[str, WorkflowDefinition] = {}

    @router.post("/workflows")
    def register_workflow(definition: WorkflowDefinition) -> dict:
        try:
            definition.validate_dag()
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        definitions[definition.workflow_id] = definition
        return {"workflow_id": definition.workflow_id, "steps": len(definition.steps), "valid": True}

    def _get(workflow_id: str) -> WorkflowDefinition:
        if workflow_id not in definitions:
            raise HTTPException(status_code=404, detail=f"unknown workflow {workflow_id}")
        return definitions[workflow_id]

    @router.get("/workflows/{workflow_id}/state")
    def workflow_state(workflow_id: str) -> dict:
        return engine.state(_get(workflow_id)).model_dump()

    @router.post("/workflows/{workflow_id}/run")
    def run_workflow(workflow_id: str, body: dict | None = None) -> dict:
        return engine.run(_get(workflow_id), payload=body or {}).model_dump()

    @router.post("/workflows/{workflow_id}/cancel")
    def cancel_workflow(workflow_id: str) -> dict:
        try:
            return engine.cancel(_get(workflow_id)).model_dump()
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @router.post("/workflows/{workflow_id}/compensate")
    def compensate_workflow(workflow_id: str) -> dict:
        return engine.compensate(_get(workflow_id)).model_dump()

    @router.post("/workflows/{workflow_id}/approve")
    def approve_step(workflow_id: str, body: dict) -> dict:
        try:
            return engine.approve(_get(workflow_id), str(body.get("step", "")),
                                  approved=bool(body.get("approved", True))).model_dump()
        except (RuntimeError, KeyError) as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @router.get("/workflows/{workflow_id}/timers")
    def due_timers(workflow_id: str) -> dict:
        return {"due": engine.due_timers(_get(workflow_id))}

    @router.post("/queue/items")
    def enqueue_item(body: dict) -> dict:
        item = queue.enqueue(str(body.get("kind", "task")), body.get("payload") or {},
                             priority=int(body.get("priority", 0)))
        return item.model_dump()

    @router.post("/queue/claim")
    def claim_item(body: dict) -> dict:
        item = queue.claim(str(body.get("owner", "worker")))
        if item is None:
            return {"item": None}
        return item.model_dump()

    @router.post("/queue/items/{item_id}/complete")
    def complete_item(item_id: str, body: dict) -> dict:
        try:
            return queue.complete(item_id, owner=str(body.get("owner", ""))).model_dump()
        except (RuntimeError, KeyError) as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @router.get("/streams/{stream_id}/reconcile")
    def reconcile_stream(stream_id: str) -> dict:
        return store.reconcile(stream_id).model_dump()

    return router
