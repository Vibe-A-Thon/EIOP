"""FastAPI router for capabilities per CRA-001.4 and CRA-001.8."""
from __future__ import annotations
from typing import Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from eoip.capabilities.model import (
    CapabilityEntry,
    CapabilityError,
)
from eoip.capabilities.registry import get_capability_registry

router = APIRouter(prefix="/api/v1/capabilities", tags=["capabilities"])

class CapabilitiesResponse(BaseModel):
    capabilities: list[CapabilityEntry]

@router.get("", response_model=CapabilitiesResponse)
def list_capabilities() -> CapabilitiesResponse:
    reg = get_capability_registry()
    return CapabilitiesResponse(capabilities=reg.get_all())

@router.get("/{capability_id}", response_model=CapabilityEntry)
def get_capability(capability_id: str) -> CapabilityEntry:
    reg = get_capability_registry()
    entry = reg.get(capability_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "CAPABILITY_NOT_FOUND", "message": f"Capability '{capability_id}' not found"}},
        )
    return entry
