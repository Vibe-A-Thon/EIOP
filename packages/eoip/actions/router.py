"""FastAPI routes for Governed Actions & Write-Back (CRA-027.9)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from pydantic import BaseModel, Field

from eoip.actions.contracts import (
    ActionError,
    ActionIntent,
    ActionState,
    ApprovalExpiredError,
    ApprovalGrant,
    IdempotencyViolationError,
    IntentDigestMismatchError,
    InvalidApprovalError,
    ReadBackVerificationError,
    WriteBackDisabledError,
)
from eoip.actions.engine import ActionEngine
from eoip.intelligence_eng.engine import AutonomyLevel

# Shared engine singleton
_action_engine = ActionEngine(write_back_enabled=False)


def get_action_engine() -> ActionEngine:
    return _action_engine


router = APIRouter(tags=["Governed Actions"])


class ProposeActionRequest(BaseModel):
    action_type_id: str
    target_instance: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    principal: str = "system"
    scope: dict[str, Any] = Field(default_factory=dict)
    dry_run: bool = False


class ApproveActionRequest(BaseModel):
    approver: str
    approver_autonomy: AutonomyLevel = AutonomyLevel.HITL
    nonce: str | None = None


class ExecuteActionRequest(BaseModel):
    intent_id: str


# ---------------------------------------------------------------------------
# Canonical Routes (CRA-027.9)
# ---------------------------------------------------------------------------
@router.post("/api/v1/actions/propose", response_model=ActionIntent)
def propose_action(
    req: ProposeActionRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    engine: ActionEngine = Depends(get_action_engine),
) -> ActionIntent:
    intent = ActionIntent(
        action_type_id=req.action_type_id,
        target_instance=req.target_instance,
        arguments=req.arguments,
        principal=req.principal,
        scope=req.scope,
        idempotency_key=idempotency_key,
        dry_run=req.dry_run,
    )
    try:
        return engine.propose_action(intent)
    except WriteBackDisabledError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message)
    except IdempotencyViolationError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message)
    except ActionError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)


@router.get("/api/v1/actions", response_model=list[ActionIntent])
def list_actions(
    tenant_id: str | None = Query(None),
    engine: ActionEngine = Depends(get_action_engine),
) -> list[ActionIntent]:
    return engine.list_intents(tenant_id)


@router.get("/api/v1/actions/{id}", response_model=ActionIntent)
def get_action(
    id: str,
    engine: ActionEngine = Depends(get_action_engine),
) -> ActionIntent:
    intent = engine.get_intent(id)
    if not intent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Action intent '{id}' not found")
    return intent


@router.post("/api/v1/actions/{id}/approve", response_model=ApprovalGrant)
def approve_action(
    id: str,
    req: ApproveActionRequest,
    engine: ActionEngine = Depends(get_action_engine),
) -> ApprovalGrant:
    try:
        return engine.approve_action(
            intent_id=id,
            approver=req.approver,
            approver_autonomy=req.approver_autonomy,
            nonce=req.nonce,
        )
    except ActionError as exc:
        if exc.code == "insufficient_autonomy_level":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message)
        elif exc.code == "intent_not_found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message)


@router.post("/api/v1/actions/execute", response_model=ActionIntent)
def execute_action(
    req: ExecuteActionRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    engine: ActionEngine = Depends(get_action_engine),
) -> ActionIntent:
    try:
        return engine.execute_action(
            intent_id=req.intent_id,
            idempotency_key=idempotency_key,
        )
    except ApprovalExpiredError as exc:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail=exc.message)
    except (IntentDigestMismatchError, InvalidApprovalError) as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message)
    except IdempotencyViolationError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message)
    except ReadBackVerificationError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=exc.message)
    except ActionError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)


# ---------------------------------------------------------------------------
# Aliases for OCA / Ontology compatibility (CRA-027.9)
# ---------------------------------------------------------------------------
@router.post("/ontology/actions/{id}/invoke", response_model=ActionIntent)
def invoke_action_alias(
    id: str,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    engine: ActionEngine = Depends(get_action_engine),
) -> ActionIntent:
    return execute_action(ExecuteActionRequest(intent_id=id), idempotency_key=idempotency_key, engine=engine)


@router.get("/ontology/actions", response_model=list[ActionIntent])
def list_actions_alias(
    engine: ActionEngine = Depends(get_action_engine),
) -> list[ActionIntent]:
    return list_actions(tenant_id=None, engine=engine)
