"""Tests for Multi-Tenant Isolation Hardening (WP-KG3-02, GAP-07, INV-SELF-02, CAP-47, CRA-003.6, CRA-003.11)."""

import pytest
from eoip.contracts.canonical import PrincipalType, TrustedScope
from eoip.authz.pdp import ScopeViolationError
from eoip.tenancy.isolation_hardened import (
    MultiTenantBarrierEnforcer,
    TenantNamespace,
    InvalidTenantNamespaceError,
)


@pytest.fixture
def tenant_alpha_scope():
    return TrustedScope(
        tenant_id="tenant_alpha",
        workspace_id="ws_1",
        principal_id="user_alpha",
        principal_type=PrincipalType.USER,
        roles=["analyst"],
        effective_acls=["tenant:tenant_alpha", "internal"],
        policy_epoch=1,
    )


@pytest.fixture
def tenant_beta_scope():
    return TrustedScope(
        tenant_id="tenant_beta",
        workspace_id="ws_2",
        principal_id="user_beta",
        principal_type=PrincipalType.USER,
        roles=["analyst"],
        effective_acls=["tenant:tenant_beta", "internal"],
        policy_epoch=1,
    )


def test_canonical_id_formatting_and_parsing():
    """Validates 100% canonical namespace prefixing: urn:eoip:{tenant_id}:{raw_id}."""
    formatted = TenantNamespace.format_canonical_id("tenant_alpha", "svc-catalog-42")
    assert formatted == "urn:eoip:tenant_alpha:svc-catalog-42"

    parsed_tenant = TenantNamespace.parse_tenant_id(formatted)
    assert parsed_tenant == "tenant_alpha"

    # Idempotent formatting
    reformatted = TenantNamespace.format_canonical_id("tenant_alpha", formatted)
    assert reformatted == formatted


def test_cross_tenant_id_injection_rejected():
    """Attempting to format or inject a foreign tenant's canonical ID raises ScopeViolationError."""
    with pytest.raises(ScopeViolationError) as exc_info:
        TenantNamespace.format_canonical_id("tenant_alpha", "urn:eoip:tenant_beta:secret-database")
    assert "Cross-tenant ID injection detected" in str(exc_info.value)


def test_invalid_tenant_format_rejected():
    """Tenant IDs with malicious punctuation or path traversal characters are strictly rejected."""
    with pytest.raises(InvalidTenantNamespaceError):
        TenantNamespace.format_canonical_id("tenant/../../root", "entity-1")

    with pytest.raises(InvalidTenantNamespaceError):
        TenantNamespace.parse_tenant_id("malformed-urn:unknown:123")


def test_multi_tenant_barrier_enforcement(tenant_alpha_scope, tenant_beta_scope):
    """Enforces that an alpha tenant cannot assert, read, or probe beta tenant resources."""
    enforcer = MultiTenantBarrierEnforcer()

    # Valid same-tenant access
    enforcer.assert_same_tenant(
        tenant_alpha_scope,
        "tenant_alpha",
        entity_canonical_id="urn:eoip:tenant_alpha:component-1",
    )

    # Cross-tenant target ID raises ScopeViolationError
    with pytest.raises(ScopeViolationError):
        enforcer.assert_same_tenant(tenant_alpha_scope, "tenant_beta")

    # Cross-tenant entity canonical ID raises ScopeViolationError
    with pytest.raises(ScopeViolationError):
        enforcer.assert_same_tenant(
            tenant_alpha_scope,
            "tenant_alpha",
            entity_canonical_id="urn:eoip:tenant_beta:component-99",
        )


def test_query_dataset_isolation(tenant_alpha_scope):
    """Querying named graphs from another tenant raises ScopeViolationError."""
    enforcer = MultiTenantBarrierEnforcer()
    alpha_graph = TenantNamespace.get_graph_iri("tenant_alpha")
    beta_graph = TenantNamespace.get_graph_iri("tenant_beta")

    assert alpha_graph == "urn:eoip:tenant:tenant_alpha"
    assert beta_graph == "urn:eoip:tenant:tenant_beta"

    # Allowed dataset containing own graph and public graph
    permitted = enforcer.filter_query_dataset(tenant_alpha_scope, [alpha_graph, "urn:eoip:public:graph"])
    assert permitted == [alpha_graph, "urn:eoip:public:graph"]

    # Probing beta graph must be blocked fail-closed
    with pytest.raises(ScopeViolationError) as exc:
        enforcer.filter_query_dataset(tenant_alpha_scope, [alpha_graph, beta_graph])
    assert "denied for tenant 'tenant_alpha'" in str(exc.value)


def test_cypher_tenant_predicate_injection(tenant_alpha_scope):
    """Cypher query AST/rewriter automatically injects tenant_id filter."""
    enforcer = MultiTenantBarrierEnforcer()

    # Query with existing WHERE
    q1 = "MATCH (n:Service) WHERE n.status = 'ACTIVE' RETURN n"
    rewritten1 = enforcer.inject_tenant_filter_cypher(tenant_alpha_scope, q1)
    assert "n.tenant_id = 'tenant_alpha' AND n.status = 'ACTIVE'" in rewritten1

    # Query without WHERE
    q2 = "MATCH (n:Database) RETURN n"
    rewritten2 = enforcer.inject_tenant_filter_cypher(tenant_alpha_scope, q2)
    assert "WHERE n.tenant_id = 'tenant_alpha' RETURN n" in rewritten2


def test_indistinguishable_404_format():
    """Cross-tenant probes return an indistinguishable 404 response body."""
    enforcer = MultiTenantBarrierEnforcer()
    resp = enforcer.handle_unauthorized_probe()
    assert resp["code"] == 404
    assert resp["error"] == "NOT_FOUND"
    assert resp["message"] == "The requested resource was not found"
