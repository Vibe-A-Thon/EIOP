"""Tests for Derivation-Aware Source-ACL Filtering (WP-KG3-01, GAP-01, INV-01, CAP-46)."""

import pytest
from eoip.contracts.canonical import PrincipalType, TrustedScope
from eoip.authz.derivation_acl import (
    DerivationACLEvaluator,
    TraversalHop,
    TraversalPath,
    get_derivation_evaluator,
)
from eoip.authz.pdp import get_policy_epoch_registry
from eoip.retrieval.service import retrieve
from eoip.graph.memory import MemoryGraphStore


@pytest.fixture
def clean_evaluator():
    registry = get_policy_epoch_registry()
    # Reset epoch to 1 for test tenant
    registry._epochs["tenant_alpha"] = 1
    evaluator = DerivationACLEvaluator(epoch_registry=registry)
    evaluator.clear_cache()
    return evaluator


@pytest.fixture
def alice_scope():
    return TrustedScope(
        tenant_id="tenant_alpha",
        workspace_id="ws_main",
        principal_id="alice",
        principal_type=PrincipalType.USER,
        roles=["analyst"],  # Level 2 internal clearance
        effective_acls=["tenant:tenant_alpha", "dept:engineering", "proj:aurora", "internal"],
        policy_epoch=1,
    )


@pytest.fixture
def bob_restricted_scope():
    return TrustedScope(
        tenant_id="tenant_alpha",
        workspace_id="ws_main",
        principal_id="bob",
        principal_type=PrincipalType.USER,
        roles=["guest"],  # Level 1 public clearance
        effective_acls=["tenant:tenant_alpha"],  # Missing proj:aurora and internal tags
        policy_epoch=1,
    )


def test_derivation_acl_multi_hop_single_path_permitted(clean_evaluator, alice_scope):
    """Alice with analyst role + proj:aurora ACLs can traverse all hops of an authorized path."""
    hop1 = TraversalHop(
        vertex_id="svc:aurora-api",
        vertex_label="Service",
        acl_vector=("tenant:tenant_alpha", "proj:aurora"),
        classification="internal",
        tenant_id="tenant_alpha",
    )
    hop2 = TraversalHop(
        vertex_id="db:aurora-postgres",
        vertex_label="Database",
        edge_id="edge:connects",
        edge_label="CONNECTS_TO",
        acl_vector=("tenant:tenant_alpha", "dept:engineering"),
        classification="internal",
        tenant_id="tenant_alpha",
    )
    path = TraversalPath(path_id="path_1", hops=(hop1, hop2))

    assert clean_evaluator.evaluate_path(alice_scope, path) is True
    res = clean_evaluator.filter_traversal_paths(alice_scope, [path])
    assert res.visible is True
    assert len(res.permitted_paths) == 1
    assert res.hidden_paths_count == 0


def test_derivation_acl_multi_hop_path_restricted_hop_denied(clean_evaluator, bob_restricted_scope):
    """Bob lacking proj:aurora tag and internal clearance is blocked fail-closed when a path traverses through a restricted hop."""
    hop1 = TraversalHop(
        vertex_id="svc:public-gateway",
        vertex_label="Service",
        acl_vector=("tenant:tenant_alpha",),
        classification="public",
        tenant_id="tenant_alpha",
    )
    hop2 = TraversalHop(
        vertex_id="vault:aurora-secrets",
        vertex_label="SecretVault",
        edge_id="edge:reads_secret",
        edge_label="READS_SECRET",
        acl_vector=("tenant:tenant_alpha", "proj:aurora"),  # Bob does not have this tag
        classification="restricted",
        tenant_id="tenant_alpha",
    )
    path = TraversalPath(path_id="path_restricted", hops=(hop1, hop2))

    assert clean_evaluator.evaluate_path(bob_restricted_scope, path) is False
    res = clean_evaluator.filter_traversal_paths(bob_restricted_scope, [path])
    assert res.visible is False
    assert len(res.permitted_paths) == 0
    assert res.hidden_paths_count == 1


def test_derivation_acl_justification_aware_alternate_path(clean_evaluator, alice_scope):
    """Fact derived from two alternate paths: one restricted and one permitted. Fact remains visible via permitted path."""
    # Path A has a restricted premise requiring executive clearance
    restricted_hop = TraversalHop(
        vertex_id="meeting:exec-minutes",
        vertex_label="Meeting",
        acl_vector=("tenant:tenant_alpha", "role:exec"),
        classification="restricted",
        tenant_id="tenant_alpha",
    )
    path_a = TraversalPath(path_id="path_a", hops=(restricted_hop,))

    # Path B has a public engineering premise Alice can see
    public_hop = TraversalHop(
        vertex_id="pr:public-announcement",
        vertex_label="PullRequest",
        acl_vector=("tenant:tenant_alpha", "dept:engineering"),
        classification="internal",
        tenant_id="tenant_alpha",
    )
    path_b = TraversalPath(path_id="path_b", hops=(public_hop,))

    res = clean_evaluator.filter_traversal_paths(alice_scope, [path_a, path_b])
    # Alice can see the fact because path_b is permitted, but path_a is pruned
    assert res.visible is True
    assert len(res.permitted_paths) == 1
    assert res.permitted_paths[0].path_id == "path_b"
    assert res.hidden_paths_count == 1


def test_derivation_acl_policy_epoch_stale_invalidation(clean_evaluator, alice_scope):
    """When tenant policy epoch increments, scopes with stale epochs are immediately invalidated fail-closed."""
    path = TraversalPath(
        path_id="path_p",
        hops=(
            TraversalHop(
                vertex_id="doc:spec",
                vertex_label="Doc",
                acl_vector=("tenant:tenant_alpha",),
                classification="internal",
                tenant_id="tenant_alpha",
            ),
        ),
    )
    # At epoch 1, evaluation passes
    assert clean_evaluator.evaluate_path(alice_scope, path) is True

    # Policy update occurs: tenant epoch increments to 2
    clean_evaluator.epoch_registry.increment_epoch("tenant_alpha", reason="Role membership revoked")
    assert clean_evaluator.epoch_registry.get_epoch("tenant_alpha") == 2

    # Alice's scope is still on epoch 1 -> must fail closed
    clean_evaluator.clear_cache()
    assert clean_evaluator.evaluate_path(alice_scope, path) is False
    res = clean_evaluator.filter_traversal_paths(alice_scope, [path])
    assert res.visible is False


def test_retrieval_service_derivation_acl_filtering():
    """Verify that retrieval service filters nodes and edges based on TrustedScope ACLs."""
    store = MemoryGraphStore()
    
    # Vertex 1: Public work item
    v1 = store.upsert_vertex("WorkItem", {
        "canonical_id": "issue:public-1",
        "issue_key": "EOIP-PUB",
        "summary": "Public feature",
        "tenant_id": "tenant_alpha",
        "acl_vector": ["tenant:tenant_alpha"],
        "classification": "internal",
    })
    # Vertex 2: Confidential commit
    v2 = store.upsert_vertex("Commit", {
        "canonical_id": "commit:private-1",
        "commit_sha": "def456",
        "tenant_id": "tenant_alpha",
        "acl_vector": ["tenant:tenant_alpha", "dept:finance"],
        "classification": "restricted",
    })
    # Edge between them
    store.upsert_edge("IMPLEMENTS", v2["vid"], v1["vid"], {
        "tenant_id": "tenant_alpha",
        "acl_vector": ["tenant:tenant_alpha", "dept:finance"],
        "classification": "restricted",
        "source_ref": "git://repo/def456",
    })

    # Scope 1: Engineer (clearance internal, but lacking dept:finance)
    current_ep = get_policy_epoch_registry().get_epoch("tenant_alpha")
    engineer_scope = TrustedScope(
        tenant_id="tenant_alpha",
        workspace_id="ws_1",
        principal_id="eng_user",
        principal_type=PrincipalType.USER,
        roles=["analyst"],
        effective_acls=["tenant:tenant_alpha", "dept:engineering", "internal"],
        policy_epoch=current_ep,
    )

    # Retrieval from commit:private-1 directly should be denied fail-closed
    result_denied = retrieve(
        store=store,
        canonical_id="commit:private-1",
        question="What does commit:private-1 implement?",
        scope=engineer_scope,
    )
    assert result_denied.contexts == []
    assert result_denied.metrics.get("hidden_by_policy") is True
    assert "Access denied" in result_denied.answer

    # Retrieval from issue:public-1: engineer can see issue:public-1, but commit:private-1 must be pruned
    result_filtered = retrieve(
        store=store,
        canonical_id="issue:public-1",
        question="What implements issue:public-1?",
        scope=engineer_scope,
    )
    context_texts = [c.text for c in result_filtered.contexts]
    assert any("EOIP-PUB" in t for t in context_texts)
    assert not any("def456" in t for t in context_texts)
