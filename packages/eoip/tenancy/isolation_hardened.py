"""Multi-Tenant Isolation Hardening and Barrier Enforcement (WP-KG3-02, GAP-07, INV-SELF-02, CAP-47).

Enforces:
1. Canonical namespace prefixing across all graph entities: urn:eoip:{tenant_id}:{entity_id}.
2. TriG / N-Quads tenant graph IRI formatting: https://eoip.enterprise.internal/tenants/{tenant_id}/graph.
3. Query AST scope injection ensuring zero cross-tenant contamination.
4. Indistinguishable 404 responses for foreign tenant resource probes.
5. Fail-closed cross-tenant barrier verification.
"""

from __future__ import annotations

import re
import logging
from dataclasses import dataclass, field
from typing import Any
from collections.abc import Sequence

from eoip.contracts.canonical import PrincipalType, TrustedScope
from eoip.authz.pdp import (
    ScopeViolationError,
    format_indistinguishable_not_found,
    tenant_graph_iri,
)

logger = logging.getLogger(__name__)

TENANT_ID_REGEX = re.compile(r"^[a-zA-Z0-9_\-]+$")
CANONICAL_URN_REGEX = re.compile(r"^urn:eoip:([a-zA-Z0-9_\-]+):(.+)$")


class InvalidTenantNamespaceError(ValueError):
    """Raised when an IRI or tenant ID violates canonical isolation format."""


@dataclass(frozen=True)
class TenantPartitionSpec:
    tenant_id: str
    graph_iri: str
    urn_prefix: str
    isolation_tier: str = "SILO"  # SILO, BRIDGE, POOL


class TenantNamespace:
    """Manages canonical entity IRI formatting and parsing per tenant."""

    @classmethod
    def format_canonical_id(cls, tenant_id: str, raw_id: str) -> str:
        """Format an entity ID into canonical URN: urn:eoip:{tenant_id}:{raw_id}."""
        if not TENANT_ID_REGEX.match(tenant_id):
            raise InvalidTenantNamespaceError(f"Invalid characters in tenant_id: '{tenant_id}'")
        clean_raw = raw_id.strip()
        if clean_raw.startswith(f"urn:eoip:{tenant_id}:"):
            return clean_raw
        if clean_raw.startswith("urn:eoip:"):
            # Entity already has a different tenant prefix -> cross tenant violation
            match = CANONICAL_URN_REGEX.match(clean_raw)
            if match and match.group(1) != tenant_id:
                raise ScopeViolationError(
                    f"Cross-tenant ID injection detected: expected tenant '{tenant_id}', got '{match.group(1)}'"
                )
        return f"urn:eoip:{tenant_id}:{clean_raw}"

    @classmethod
    def parse_tenant_id(cls, canonical_id: str) -> str:
        """Extract tenant_id from a canonical URN. Raises error if invalid."""
        match = CANONICAL_URN_REGEX.match(canonical_id)
        if not match:
            raise InvalidTenantNamespaceError(
                f"ID '{canonical_id}' does not conform to canonical urn:eoip:{{tenant_id}}:{{raw_id}}"
            )
        return match.group(1)

    @classmethod
    def get_graph_iri(cls, tenant_id: str) -> str:
        """Return canonical named-graph IRI for tenant RDF datasets."""
        return tenant_graph_iri(tenant_id)


class MultiTenantBarrierEnforcer:
    """Enforces strict isolation barriers across storage, queries, and mutations."""

    def __init__(self) -> None:
        pass

    def validate_scope(self, scope: TrustedScope) -> None:
        """Verify scope tenant validity."""
        if not scope.tenant_id or not TENANT_ID_REGEX.match(scope.tenant_id):
            raise ScopeViolationError(f"Invalid or missing tenant_id in scope: '{scope.tenant_id}'")

    def assert_same_tenant(
        self, scope: TrustedScope, target_id: str, *, entity_canonical_id: str | None = None
    ) -> None:
        """Enforce that target resource belongs strictly to caller's tenant."""
        self.validate_scope(scope)
        if target_id != scope.tenant_id:
            logger.warning(
                "Tenant isolation breach attempt: scope tenant '%s' probed resource of tenant '%s'",
                scope.tenant_id,
                target_id,
            )
            raise ScopeViolationError("Cross-tenant access prohibited.")

        if entity_canonical_id:
            try:
                owner = TenantNamespace.parse_tenant_id(entity_canonical_id)
                if owner != scope.tenant_id:
                    raise ScopeViolationError(
                        f"Resource '{entity_canonical_id}' belongs to tenant '{owner}', not '{scope.tenant_id}'"
                    )
            except InvalidTenantNamespaceError:
                # If legacy ID format without urn:eoip:, ensure target_id was validated
                pass

    def filter_query_dataset(
        self, scope: TrustedScope, dataset_iris: Sequence[str]
    ) -> list[str]:
        """Ensure all queried named graphs belong to caller's tenant."""
        self.validate_scope(scope)
        allowed_graph_iri = TenantNamespace.get_graph_iri(scope.tenant_id)
        permitted: list[str] = []
        for iri in dataset_iris:
            if iri == allowed_graph_iri or iri in ("urn:eoip:public:graph", "default"):
                permitted.append(iri)
            else:
                logger.warning(
                    "Scope '%s' attempted to query unauthorized graph IRI '%s'",
                    scope.tenant_id,
                    iri,
                )
                raise ScopeViolationError(
                    f"Access to graph IRI '{iri}' denied for tenant '{scope.tenant_id}'"
                )
        return permitted

    def inject_tenant_filter_cypher(self, scope: TrustedScope, cypher_query: str) -> str:
        """Inject tenant scoping predicate into Cypher query."""
        self.validate_scope(scope)
        tid = scope.tenant_id
        # If query already contains MATCH, inject WHERE condition
        if "WHERE" in cypher_query.upper():
            return re.sub(
                r"(WHERE\s+)",
                f"\\1n.tenant_id = '{tid}' AND ",
                cypher_query,
                count=1,
                flags=re.IGNORECASE,
            )
        elif "RETURN" in cypher_query.upper():
            return re.sub(
                r"(\s+RETURN\s+)",
                f" WHERE n.tenant_id = '{tid}'\\1",
                cypher_query,
                count=1,
                flags=re.IGNORECASE,
            )
        return f"{cypher_query} WHERE n.tenant_id = '{tid}'"

    def handle_unauthorized_probe(self) -> dict[str, Any]:
        """Produce uniform indistinguishable 404 response to eliminate enumeration timing/content attacks."""
        return format_indistinguishable_not_found()
