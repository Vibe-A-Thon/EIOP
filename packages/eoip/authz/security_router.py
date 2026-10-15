"""FastAPI REST router for Enterprise Security (GAP-SEC-008..012).

Endpoints:
- POST /api/v1/security/tokens/issue: Issue scoped bearer tokens
- POST /api/v1/security/tokens/verify: Verify bearer token integrity, scopes, and revocation status
- POST /api/v1/security/tokens/revoke: Revoke a token ID (jti) or token hash (CRL)
- GET  /api/v1/security/status: Current security posture, key rotation status, revocation list count
- GET  /api/v1/security/policy-matrix: RBAC/ABAC role hierarchy and policy coverage matrix
"""

from __future__ import annotations

import time
from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from eoip.authz.core import (
    KNOWN_PERMISSIONS,
    ROLE_HIERARCHY,
    RoleRegistry,
    role_inherited_roles,
    role_rank,
)
from eoip.authz.tokens import (
    TokenError,
    TokenRevocationStore,
    TokenSigner,
    global_revocation_store,
)


class IssueTokenRequest(BaseModel):
    subject: str = Field(..., description="Subject user/service id")
    roles: list[str] = Field(default_factory=lambda: ["viewer"])
    scopes: list[str] = Field(default_factory=lambda: ["graph:read"])
    tenant_id: str = Field(default="default")
    attributes: dict[str, Any] = Field(default_factory=dict)
    ttl_seconds: int = Field(default=3600, ge=1)


class VerifyTokenRequest(BaseModel):
    token: str = Field(...)
    required_scopes: list[str] | None = Field(default=None)


class RevokeTokenRequest(BaseModel):
    identifier: str = Field(..., description="jti, subject, or token string")
    reason: str = Field(default="revoked_by_admin")
    expires_at: int | None = Field(default=None)


def build_security_router(
    signer: TokenSigner | None = None,
    revocation_store: TokenRevocationStore | None = None,
    role_registry: RoleRegistry | None = None,
) -> APIRouter:
    router = APIRouter(prefix="/api/v1/security", tags=["security"])
    rev_store = revocation_store or global_revocation_store()
    active_signer = signer or TokenSigner(revocation_store=rev_store)
    roles = role_registry or RoleRegistry()

    @router.post("/tokens/issue")
    async def issue_token(req: IssueTokenRequest) -> dict[str, Any]:
        """Issue a scoped HMAC-SHA256 bearer token (GAP-SEC-009, GAP-SEC-011)."""
        token = active_signer.issue(
            subject=req.subject,
            roles=req.roles,
            scopes=req.scopes,
            tenant_id=req.tenant_id,
            attributes=req.attributes,
            ttl_seconds=req.ttl_seconds,
        )
        payload = active_signer.verify(token, enforce_revocation=False)
        return {
            "token": token,
            "jti": payload.get("jti"),
            "subject": payload.get("sub"),
            "roles": payload.get("roles"),
            "scopes": payload.get("scopes"),
            "tenant_id": payload.get("tenant_id"),
            "expires_at": payload.get("exp"),
        }

    @router.post("/tokens/verify")
    async def verify_token(req: VerifyTokenRequest) -> dict[str, Any]:
        """Verify token integrity, expiration, CRL revocation, and scopes (GAP-SEC-008, GAP-SEC-010)."""
        try:
            payload = active_signer.verify(
                req.token,
                required_scopes=req.required_scopes,
                enforce_revocation=True,
            )
            return {
                "valid": True,
                "payload": payload,
                "subject": payload.get("sub"),
                "roles": payload.get("roles"),
                "scopes": payload.get("scopes"),
            }
        except TokenError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(exc),
            ) from exc

    @router.post("/tokens/revoke")
    async def revoke_token(req: RevokeTokenRequest) -> dict[str, Any]:
        """Revoke a token identifier or jti into the CRL denylist (GAP-SEC-010)."""
        rev_store.revoke(
            identifier=req.identifier,
            reason=req.reason,
            expires_at=req.expires_at,
        )
        return {
            "revoked": True,
            "identifier": req.identifier,
            "reason": req.reason,
            "active_revocations": len(rev_store.list_revocations()),
        }

    @router.get("/status")
    async def security_status() -> dict[str, Any]:
        """Current enterprise security posture and configuration (GAP-SEC-012)."""
        rev_count = len(rev_store.list_revocations())
        return {
            "status": "OPERATIONAL",
            "enforcement_mode": "FAIL_CLOSED",
            "algorithm": "HMAC-SHA256",
            "key_rotation_supported": True,
            "active_revocations_count": rev_count,
            "roles_registered": len(roles.list_roles()),
            "permissions_known": len(KNOWN_PERMISSIONS),
            "timestamp": int(time.time()),
        }

    @router.get("/policy-matrix")
    async def policy_matrix() -> dict[str, Any]:
        """RBAC/ABAC role hierarchy and policy coverage matrix (GAP-SEC-012)."""
        matrix: dict[str, Any] = {}
        for role in ROLE_HIERARCHY:
            inherited = role_inherited_roles(role)
            rank = role_rank(role)
            role_def = roles.get_role(role)
            matrix[role] = {
                "rank": rank,
                "inherited_roles": inherited,
                "permissions": role_def.get("permissions", []) if role_def else [],
                "description": role_def.get("description", "") if role_def else "",
            }
        return {
            "roles_hierarchy": matrix,
            "all_permissions": sorted(KNOWN_PERMISSIONS),
        }

    return router
