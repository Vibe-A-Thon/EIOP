"""Access control list (ACL) semantics and token evaluation (T-113 / §6.3.2 / REVA-SEC-002)."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Set
from pydantic import BaseModel, Field


class Principal(BaseModel):
    """Authenticated principal executing a REVA request."""

    id: str
    tenant_id: str
    tokens: Set[str] = Field(default_factory=set)
    groups: Set[str] = Field(default_factory=set)
    roles: Set[str] = Field(default_factory=set)
    is_admin: bool = False


def extract_acl(envelope: Dict[str, Any]) -> Dict[str, Any]:
    """Extract the ACL block from an envelope dictionary."""
    return envelope.get("acl") or {}


def required_tokens(envelope: Dict[str, Any]) -> Set[str]:
    """Compute required tokens that a principal must possess to view this warrant."""
    acl = extract_acl(envelope)
    req = acl.get("source_acl_refs") or acl.get("required_tokens") or []
    return set(req)



def is_authorized(envelope: Dict[str, Any], principal: Principal) -> bool:
    """Evaluate whether principal is permitted to access the warrant per §6.3.2."""
    if principal.is_admin:
        return True

    acl = extract_acl(envelope)
    req_tokens = required_tokens(envelope)

    # 1. Principal must possess all required tokens
    if not req_tokens.issubset(principal.tokens):
        return False

    deny = set(acl.get("deny") or [])
    # 2. Principal must not be explicitly denied
    if principal.id in deny:
        return False

    allow = set(acl.get("allow") or [])
    # 3. If allow list is non-empty, principal id or one of their groups must match
    if allow:
        matches = {principal.id}.union(principal.groups)
        if not allow.intersection(matches):
            return False

    return True


def derive_acl(input_envelopes: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Derive most restrictive ACL from a set of input warrants (§6.3.2)."""
    merged_tokens: Set[str] = set()
    combined_allow: Optional[Set[str]] = None
    merged_deny: Set[str] = set()

    for env in input_envelopes:
        acl = extract_acl(env)
        req = set(acl.get("required_tokens") or [])
        merged_tokens.update(req)

        allow = set(acl.get("allow") or [])
        if allow:
            if combined_allow is None:
                combined_allow = set(allow)
            else:
                combined_allow = combined_allow.intersection(allow)

        deny = set(acl.get("deny") or [])
        merged_deny.update(deny)

    return {
        "required_tokens": sorted(list(merged_tokens)),
        "allow": sorted(list(combined_allow)) if combined_allow is not None else [],
        "deny": sorted(list(merged_deny)),
    }
