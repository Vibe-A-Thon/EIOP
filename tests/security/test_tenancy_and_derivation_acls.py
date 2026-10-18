"""Tenancy, derived-fact justification ACLs, and policy epoch tests (CRA-003.1 - CRA-003.12, CRA-003.A)."""

import pytest
from datetime import datetime, timezone

from eoip.contracts.canonical import PrincipalType, TrustedScope
from eoip.authz.pdp import (
    FactPremise,
    ScopeViolationError,
    can_read,
    format_indistinguishable_not_found,
    get_policy_epoch_registry,
    inject_and_validate_query_scope,
    tenant_graph_iri,
    visible_derived_fact,
)


@pytest.fixture
def tenant_alpha_scope():
    return TrustedScope(
        tenant_id="tenant_alpha",
        workspace_id="ws_1",
        principal_id="user_alpha",
        principal_type=PrincipalType.USER,
        roles=["analyst"],
        effective_acls=["tenant:tenant_alpha", "workspace:ws_1", "premise:A"],
        policy_epoch=1,
    )


@pytest.fixture
def tenant_beta_scope():
    return TrustedScope(
        tenant_id="tenant_beta",
        workspace_id="ws_1",
        principal_id="user_beta",
        principal_type=PrincipalType.USER,
        roles=["analyst"],
        effective_acls=["tenant:tenant_beta", "workspace:ws_1"],
        policy_epoch=1,
    )


def test_cross_tenant_isolation_and_indistinguishable_404(tenant_alpha_scope):
    """CRA-003.6, CRA-003.11: Probing another tenant's resource is denied and returns 404."""
    # Attempting to read tenant_beta resource using tenant_alpha scope
    allowed = can_read(
        tenant_alpha_scope,
        acl_vector=["tenant:tenant_beta"],
        classification="internal",
        target_tenant_id="tenant_beta",
    )
    assert allowed is False

    # 404 response shape is uniform and does not leak resource existence
    nf_body = format_indistinguishable_not_found()
    assert nf_body["code"] == 404
    assert nf_body["error"] == "NOT_FOUND"


def test_justification_aware_derived_fact_single_justification(tenant_alpha_scope):
    """CRA-003.8 (resolving X-11): User permitted premise A, denied premise B cannot see derived fact."""
    premise_a = FactPremise(
        premise_id="premise_A",
        acl_vector=["premise:A"],
        classification="internal",
        description="Publicly known merger talks",
    )
    premise_b = FactPremise(
        premise_id="premise_B",
        acl_vector=["premise:B_CONFIDENTIAL"],  # Not in tenant_alpha_scope effective_acls
        classification="confidential",
        description="Confidential board resolution",
    )

    # Derived fact derived strictly from A and B together
    justifications = [[premise_a, premise_b]]

    res = visible_derived_fact(tenant_alpha_scope, justifications)
    assert res.visible is False
    assert res.selected_justification is None
    assert res.hidden_justifications_count == 1


def test_justification_aware_derived_fact_alternate_permitted_justification(tenant_alpha_scope):
    """CRA-003.8: Alternate fully permitted justification makes fact visible without revealing restricted proof."""
    premise_a = FactPremise(
        premise_id="premise_A",
        acl_vector=["premise:A"],
        classification="internal",
        description="Merger filing",
    )
    premise_b_restricted = FactPremise(
        premise_id="premise_B_restr",
        acl_vector=["premise:RESTRICTED_SOURCE"],  # Denied
        classification="restricted",
        description="Private leak",
    )
    premise_c_public = FactPremise(
        premise_id="premise_C_pub",
        acl_vector=["premise:A"],  # Permitted
        classification="public",
        description="SEC Form 8-K disclosure",
    )

    # Justification 1: A and restricted B (denied)
    # Justification 2: A and public C (fully permitted!)
    justifications = [
        [premise_a, premise_b_restricted],
        [premise_a, premise_c_public],
    ]

    res = visible_derived_fact(tenant_alpha_scope, justifications)
    assert res.visible is True
    assert res.effective_classification == "internal"  # max(internal, public) = internal
    assert res.selected_justification is not None
    # Verify ONLY the permitted justification is selected; restricted premise B is NEVER exposed
    selected_ids = [p.premise_id for p in res.selected_justification]
    assert selected_ids == ["premise_A", "premise_C_pub"]
    assert "premise_B_restr" not in selected_ids
    assert res.hidden_justifications_count == 1


def test_tenant_policy_epoch_invalidation(tenant_alpha_scope):
    """CRA-003.9: Monotonically increasing tenant epoch invalidates stale access."""
    registry = get_policy_epoch_registry()
    assert registry.get_epoch("tenant_alpha") == 1

    # Permitted under epoch 1
    assert can_read(tenant_alpha_scope, ["tenant:tenant_alpha"], "internal") is True

    # ACL change occurs: increment tenant epoch
    new_epoch = registry.increment_epoch("tenant_alpha", reason="membership_revocation")
    assert new_epoch == 2

    # Old scope with epoch 1 is now stale and denied
    assert registry.is_stale(tenant_alpha_scope) is True
    assert can_read(tenant_alpha_scope, ["tenant:tenant_alpha"], "internal") is False

    # Scope refreshed with new epoch is allowed again
    refreshed_scope = tenant_alpha_scope.model_copy(update={"policy_epoch": new_epoch})
    assert can_read(refreshed_scope, ["tenant:tenant_alpha"], "internal") is True


def test_query_plan_scope_injection_and_rejection(tenant_alpha_scope):
    """CRA-003.10: Injects tenant graph and rejects unauthorized user-supplied named graph."""
    # Ordinary SPARQL query gets injected with tenant graph
    sparql_query = "SELECT ?s ?p ?o WHERE { ?s ?p ?o }"
    injected = inject_and_validate_query_scope(sparql_query, tenant_alpha_scope, dialect="SPARQL")
    assert "FROM <urn:eoip:tenant:tenant_alpha>" in injected

    # Malicious query trying to probe tenant_beta graph
    malicious_query = "SELECT * WHERE { GRAPH <urn:eoip:tenant:tenant_beta> { ?s ?p ?o } }"
    with pytest.raises(ScopeViolationError) as exc:
        inject_and_validate_query_scope(malicious_query, tenant_alpha_scope, dialect="SPARQL")
    assert "403 Forbidden" in str(exc.value)


def test_tenant_graph_iri_format():
    """CRA-003.12: TriG/N-Quads tenant graph IRI conforms to urn:eoip:tenant:{id}."""
    assert tenant_graph_iri("tenant_alpha") == "urn:eoip:tenant:tenant_alpha"
    assert tenant_graph_iri("acme_corp") == "urn:eoip:tenant:acme_corp"
