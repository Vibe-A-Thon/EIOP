"""Policy Decision Point (PDP) and Justification-Aware Derivation Authorization (CRA-003.1 - CRA-003.12).

Enforces:
1. Deny-by-default access control (can_read).
2. Justification-aware derived-fact visibility (CRA-003.8, resolving X-11).
3. Monotonically increasing tenant policy_epoch management (CRA-003.9).
4. Plan-level query scope injection and cross-tenant named-graph rejection (CRA-003.10).
5. Indistinguishable 404 responses for cross-tenant probes (CRA-003.11).
6. TriG / N-Quads tenant graph IRI formatting (CRA-003.12).
"""

from __future__ import annotations

import logging
import re
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from eoip.contracts.canonical import PrincipalType, TrustedScope

logger = logging.getLogger(__name__)

# Classification hierarchy: public < internal < confidential < restricted
CLASSIFICATION_LEVELS: dict[str, int] = {
    "public": 1,
    "internal": 2,
    "confidential": 3,
    "restricted": 4,
}


class ScopeViolationError(PermissionError):
    """Raised when an operation violates tenancy or authorization boundaries."""


@dataclass(frozen=True)
class FactPremise:
    premise_id: str
    acl_vector: list[str]  # Required ACL tags, e.g. ["tenant:alpha", "dept:finance"]
    classification: str = "internal"  # public, internal, confidential, restricted
    description: str = ""


# ---------------------------------------------------------------------------
# Monotonically Increasing Tenant Policy Epoch Registry (CRA-003.9)
# ---------------------------------------------------------------------------

class PolicyEpochRegistry:
    """Thread-safe registry managing monotonically increasing policy epochs per tenant."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._epochs: dict[str, int] = {}
        self._history: dict[str, list[dict[str, Any]]] = {}

    def get_epoch(self, tenant_id: str) -> int:
        with self._lock:
            return self._epochs.get(tenant_id, 1)

    def increment_epoch(self, tenant_id: str, reason: str = "") -> int:
        """Increment tenant policy epoch on any ACL/membership/policy update."""
        with self._lock:
            cur = self._epochs.get(tenant_id, 1)
            new_epoch = cur + 1
            self._epochs[tenant_id] = new_epoch
            self._history.setdefault(tenant_id, []).append({
                "from_epoch": cur,
                "to_epoch": new_epoch,
                "reason": reason,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return new_epoch

    def is_stale(self, scope: TrustedScope) -> bool:
        """Return True if scope's policy_epoch is older than current tenant epoch."""
        with self._lock:
            current = self.get_epoch(scope.tenant_id)
            return scope.policy_epoch < current

    def reset(self, tenant_id: str | None = None) -> None:
        """Reset epochs and history for a tenant or globally."""
        with self._lock:
            if tenant_id is not None:
                self._epochs.pop(tenant_id, None)
                self._history.pop(tenant_id, None)
            else:
                self._epochs.clear()
                self._history.clear()


_EPOCH_REGISTRY = PolicyEpochRegistry()


def get_policy_epoch_registry() -> PolicyEpochRegistry:
    return _EPOCH_REGISTRY


# ---------------------------------------------------------------------------
# Policy Decision Point (PDP) — can_read (CRA-003.2)
# ---------------------------------------------------------------------------

def can_read(
    scope: TrustedScope,
    acl_vector: list[str],
    classification: str = "internal",
    target_tenant_id: str | None = None,
) -> bool:
    """CRA-003.2: Deny-by-default access decision.

    Checks:
    1. Tenant isolation: target_tenant_id must match scope.tenant_id (if specified).
    2. Classification clearance: principal must have clearance >= resource classification.
    3. ACL matching: principal's effective_acls or roles must intersect with acl_vector.
    4. Policy epoch validity: rejects stale access if tenant epoch has incremented.
    """
    # 1. Tenant boundary check (CRA-003.6)
    if target_tenant_id and target_tenant_id != scope.tenant_id:
        return False

    # 2. Check policy epoch freshness (CRA-003.9)
    current_epoch = _EPOCH_REGISTRY.get_epoch(scope.tenant_id)
    if scope.policy_epoch < current_epoch:
        # Stale epoch must be re-checked or denied
        return False

    # 3. Check classification clearance
    req_level = CLASSIFICATION_LEVELS.get(classification.lower(), 4)
    # Determine principal max clearance
    user_clearance = 1  # public by default
    if "admin" in scope.roles:
        user_clearance = 4
    elif "confidential_clearance" in scope.effective_acls or "steward" in scope.roles:
        user_clearance = 3
    elif "analyst" in scope.roles or "internal" in scope.effective_acls:
        user_clearance = 2

    if req_level > user_clearance:
        return False

    # If classification is public and no strict ACLs required, grant
    if req_level == 1 and not acl_vector:
        return True

    # 4. Deny by default if no ACLs match
    if not acl_vector:
        return False

    # Check ACL intersection
    principal_grants = set(scope.effective_acls) | set(scope.roles)
    # Admin role grants tenant-scoped access
    if "admin" in scope.roles or f"tenant:{scope.tenant_id}:admin" in principal_grants:
        return True

    # Must contain tenant scope tag
    tenant_tag = f"tenant:{scope.tenant_id}"
    workspace_tag = f"workspace:{scope.workspace_id}"

    # Must match at least one required grant in acl_vector
    for acl in acl_vector:
        if acl in principal_grants or acl == tenant_tag or acl == workspace_tag:
            return True

    return False


# ---------------------------------------------------------------------------
# Justification-Aware Derivation Authorization (CRA-003.8, Resolves X-11)
# ---------------------------------------------------------------------------

@dataclass
class DerivationVisibilityResult:
    visible: bool
    effective_classification: str
    selected_justification: list[FactPremise] | None
    hidden_justifications_count: int


def visible_derived_fact(
    scope: TrustedScope,
    justifications: list[list[FactPremise]],
) -> DerivationVisibilityResult:
    """CRA-003.8: Determine if an inferred fact is visible to scope.

    Rule:
    - For one justification: visible only if principal satisfies ACL of EVERY premise (intersection).
    - For multiple justifications: visible if AT LEAST ONE complete justification is fully visible.
    - Explanations select ONLY a fully visible justification. Never reveal restricted premises.
    - Effective classification is the maximum classification among the premises of the chosen justification.
    """
    if not justifications:
        return DerivationVisibilityResult(
            visible=False,
            effective_classification="restricted",
            selected_justification=None,
            hidden_justifications_count=0,
        )

    permitted_justifications: list[list[FactPremise]] = []
    hidden_count = 0

    for just in justifications:
        # Every premise in this justification must be readable by scope
        all_readable = True
        for premise in just:
            if not can_read(scope, premise.acl_vector, premise.classification):
                all_readable = False
                break
        if all_readable:
            permitted_justifications.append(just)
        else:
            hidden_count += 1

    if not permitted_justifications:
        return DerivationVisibilityResult(
            visible=False,
            effective_classification="restricted",
            selected_justification=None,
            hidden_justifications_count=hidden_count,
        )

    # Select the first fully permitted justification
    chosen = permitted_justifications[0]

    # Calculate maximum classification of chosen justification premises
    max_level = 1
    max_label = "public"
    for p in chosen:
        lvl = CLASSIFICATION_LEVELS.get(p.classification.lower(), 1)
        if lvl > max_level:
            max_level = lvl
            max_label = p.classification.lower()

    return DerivationVisibilityResult(
        visible=True,
        effective_classification=max_label,
        selected_justification=chosen,
        hidden_justifications_count=hidden_count,
    )


# ---------------------------------------------------------------------------
# Plan-Level Scope Injection & Graph Protection (CRA-003.10)
# ---------------------------------------------------------------------------

_FORBIDDEN_GRAPH_PATTERNS = [
    re.compile(r"GRAPH\s+<(?P<iri>[^>]+)>", re.IGNORECASE),
    re.compile(r"FROM\s+<(?P<iri>[^>]+)>", re.IGNORECASE),
    re.compile(r"FROM\s+NAMED\s+<(?P<iri>[^>]+)>", re.IGNORECASE),
]


def tenant_graph_iri(tenant_id: str) -> str:
    """CRA-003.12: Formats tenant graph IRI as urn:eoip:tenant:{id}."""
    return f"urn:eoip:tenant:{tenant_id}"


def inject_and_validate_query_scope(
    query_text: str,
    scope: TrustedScope,
    dialect: str = "SPARQL",
) -> str:
    """CRA-003.10: Injects tenant scope and rejects user-supplied graph/index outside scope."""
    expected_graph = tenant_graph_iri(scope.tenant_id)

    # Check for unauthorized graph access attempts
    for pat in _FORBIDDEN_GRAPH_PATTERNS:
        for match in pat.finditer(query_text):
            found_iri = match.group("iri")
            if found_iri != expected_graph:
                raise ScopeViolationError(
                    f"403 Forbidden: Unauthorized access to named graph '{found_iri}'. "
                    f"Principal scope is confined to '{expected_graph}'"
                )

    # If SPARQL query does not contain FROM or GRAPH, bind to tenant graph
    if dialect.upper() == "SPARQL" and "FROM" not in query_text.upper():
        # Insert FROM <tenant_graph_iri> after SELECT/CONSTRUCT/DESCRIBE/ASK
        m = re.match(r"^(SELECT|CONSTRUCT|DESCRIBE|ASK)\b(?P<rest>.*)", query_text.strip(), re.IGNORECASE | re.DOTALL)
        if m:
            verb = m.group(1)
            rest = m.group("rest")
            return f"{verb} FROM <{expected_graph}> {rest}"

    return query_text


# ---------------------------------------------------------------------------
# Cross-Tenant Probe Indistinguishable 404 Helper (CRA-003.11)
# ---------------------------------------------------------------------------

class NotFoundResponse(BaseModel):
    """Uniform 404 response shape indistinguishable between non-existent and forbidden cross-tenant resources."""
    error: str = "NOT_FOUND"
    message: str = "The requested resource was not found"
    code: int = 404


def format_indistinguishable_not_found() -> dict[str, Any]:
    """CRA-003.11: Returns HTTP 404 response body indistinguishable from non-existence."""
    return NotFoundResponse().model_dump()
