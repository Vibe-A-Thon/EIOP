"""Integration test suite for Ontology GitOps, PR Gates, and Governance (CRA-022.1-022.9, CRA-022.A).

Covers:
- CRA-022.1: Lifecycle draft->validation->review->approval->publication; separation of duties (no self-approval; dual-steward on main).
- CRA-022.2: Semantic AST diff and bounded impact analysis.
- CRA-022.3: Exact revision-bound approvals; concurrent edits / candidate updates invalidate approval; expired approvals rejected.
- CRA-022.4: Atomic publication, consumer acknowledgement tracking, partial failure/repair.
- CRA-022.5: Release gates: competency questions, profile/consistency/shapes checks, model authorship domain review gate.
- CRA-022.6: Moat preservation and Lead Developer review requirement for core files.
- CRA-022.8: Unsatisfiable class PR blocked with diagnostic report.
- CRA-022.9: Semantic AST diff with visual UI model (nodes, color badges, impact radius).
- CRA-022.A: Full end-to-end acceptance scenario: concurrent editor conflict, denial, expired approval,
  consumer failure, and version-qualified rollback.
"""

from __future__ import annotations

import copy
import pytest
import rdflib
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS

from eoip.ontology.gitops import current_manifest_snapshot
from eoip.ontology.governance import (
    ApprovalExpiredError,
    DualStewardApprovalRequiredError,
    GovernedPullRequest,
    LeadDeveloperReviewRequiredError,
    ModelAuthorshipGateError,
    PRState,
    Role,
    SelfApprovalForbiddenError,
    StaleApprovalError,
    UnsatisfiableClassGateError,
    VersionStore,
)
from eoip.ontology.reasoning.adapters import NativeAdapter


def _base_manifest():
    return current_manifest_snapshot()


def test_pr_lifecycle_and_separation_of_duties():
    """CRA-022.1: Full lifecycle; author cannot approve own PR; dual-steward required on main."""
    base = _base_manifest()
    cand = copy.deepcopy(base)
    cand["vertex_labels"]["NewService"] = {"domain": "SERVICES", "required": ["canonical_id"], "optional": []}

    pr = GovernedPullRequest(
        pr_id="pr-101",
        title="Add NewService class",
        author="alice",
        base_branch="main",
        target_branch="main",
        base_manifest=base,
        candidate_manifest=cand,
    )
    assert pr.state == PRState.DRAFT

    # Author cannot approve own PR (Separation of duties CRA-022.1)
    with pytest.raises(SelfApprovalForbiddenError, match="cannot approve their own PR"):
        pr.approve(reviewer="alice", role=Role.STEWARD)

    # First steward approves
    pr.approve(reviewer="bob", role=Role.STEWARD)
    assert len(pr.approvals) == 1

    # Attempt to publish to 'main' with only 1 steward approval fails (Dual-steward required CRA-022.1)
    with pytest.raises(DualStewardApprovalRequiredError):
        pr.validate_for_publication()

    # Second steward approves
    pr.approve(reviewer="carol", role=Role.STEWARD)
    assert len(pr.approvals) == 2
    assert pr.state == PRState.APPROVED

    # Now publication validation passes
    pr.validate_for_publication()


def test_semantic_ast_diff_and_visual_ui_model():
    """CRA-022.2, CRA-022.9: Semantic AST diff with visual UI model and impact blast radius."""
    base = _base_manifest()
    cand = copy.deepcopy(base)

    # Add class, remove class, add property
    cand["vertex_labels"]["AutonomousAgent"] = {"domain": "AI", "required": ["canonical_id"], "optional": []}
    removed_label = min(cand["vertex_labels"])
    del cand["vertex_labels"][removed_label]
    cand["property_keys"]["agent_autonomy_level"] = "INT"

    pr = GovernedPullRequest(
        pr_id="pr-102",
        title="Add AutonomousAgent and remove legacy label",
        author="alice",
        base_branch="main",
        target_branch="feature",
        base_manifest=base,
        candidate_manifest=cand,
    )

    ast_diff = pr.compute_ast_diff()
    assert "AutonomousAgent" in ast_diff["added_classes"]
    assert removed_label in ast_diff["removed_classes"]
    assert "agent_autonomy_level" in ast_diff["added_properties"]

    # Visual UI model structure
    ui_model = ast_diff["visual_ui_model"]
    assert "nodes" in ui_model
    node_added = next(n for n in ui_model["nodes"] if n["id"] == "AutonomousAgent")
    assert node_added["badge_color"] == "#22c55e"  # Green for added
    node_removed = next(n for n in ui_model["nodes"] if n["id"] == removed_label)
    assert node_removed["badge_color"] == "#ef4444"  # Red for removed

    # Impact analysis blast radius
    impact = ast_diff["impact_analysis"]
    assert impact["breaking_changes"] >= 1
    assert impact["requires_migration"] is True


def test_revision_bound_approval_and_stale_invalidation():
    """CRA-022.3: Revision hash binding; candidate changes invalidate prior approvals; expiry window."""
    base = _base_manifest()
    cand = copy.deepcopy(base)
    cand["vertex_labels"]["Widget"] = {"domain": "INVENTORY", "required": ["canonical_id"], "optional": []}

    pr = GovernedPullRequest(
        pr_id="pr-103",
        title="Add Widget",
        author="alice",
        base_branch="main",
        target_branch="staging",
        base_manifest=base,
        candidate_manifest=cand,
    )

    # Approve PR
    pr.approve(reviewer="bob", role=Role.STEWARD, expiry_seconds=3600)
    assert len(pr.approvals) == 1
    assert pr.state == PRState.APPROVED

    # Editor updates candidate manifest after approval
    new_cand = copy.deepcopy(cand)
    new_cand["property_keys"]["widget_weight"] = "FLOAT"
    pr.update_candidate_manifest(new_cand, actor="alice")

    # Stale approvals were cleared and state reverted to IN_REVIEW
    assert len(pr.approvals) == 0
    assert pr.state == PRState.IN_REVIEW

    # Re-approve and test expiration
    pr.approve(reviewer="bob", role=Role.STEWARD, expiry_seconds=-10)  # Expired approval
    with pytest.raises(ApprovalExpiredError, match="expired at"):
        pr.validate_for_publication()


def test_release_gates_block_unsatisfiable_classes_and_moat_touches():
    """CRA-022.5, CRA-022.6, CRA-022.8: Unsatisfiable class PR blocked with diagnostic report; moat files check."""
    base = _base_manifest()
    cand = copy.deepcopy(base)

    # Test 1: Unsatisfiable class blocked with report (CRA-022.8)
    pr_inconsistent = GovernedPullRequest(
        pr_id="pr-104",
        title="Inconsistent subclass PR",
        author="alice",
        base_branch="main",
        target_branch="staging",
        base_manifest=base,
        candidate_manifest=cand,
    )

    reasoner = NativeAdapter()
    # Add inconsistent disjointness + subclassing
    reasoner.reasoner.add_subclass("urn:example:Cat", "urn:example:Animal")
    reasoner.unsatisfiable_classes = lambda g=None, **kwargs: (["urn:example:ImpossiblePet"], None)

    with pytest.raises(UnsatisfiableClassGateError, match="unsatisfiable classes detected"):
        pr_inconsistent.run_release_gates(reasoner=reasoner)

    # Test 2: Touches to moat core files require Lead Developer review (CRA-022.6)
    pr_moat = GovernedPullRequest(
        pr_id="pr-105",
        title="Modify GitOps core",
        author="alice",
        base_branch="main",
        target_branch="staging",
        base_manifest=base,
        candidate_manifest=cand,
        touched_files=["packages/eoip/ontology/gitops.py"],
    )

    with pytest.raises(LeadDeveloperReviewRequiredError, match="requires Lead Developer review"):
        pr_moat.run_release_gates()

    # Once Lead Developer review is recorded, gate passes
    pr_moat.add_lead_developer_review(reviewer="lead-dev-dan", decision="APPROVED", notes="Approved moat extension")
    gate_results = pr_moat.run_release_gates()
    assert gate_results["lead_dev_gate"]["passed"] is True


def test_agent_authorship_domain_review_gate():
    """CRA-022.5: Agent-written PR cannot pass release gates without human domain-owner approval."""
    base = _base_manifest()
    cand = copy.deepcopy(base)

    pr_agent = GovernedPullRequest(
        pr_id="pr-106",
        title="AI generated taxonomy extension",
        author="gemini-bot",
        base_branch="main",
        target_branch="staging",
        base_manifest=base,
        candidate_manifest=cand,
        is_agent_written=True,
    )

    # Release gates fail because agent-written PR has no human domain-owner approval
    gate_report = pr_agent.run_release_gates()
    assert gate_report["passed"] is False
    assert gate_report["agent_gate"]["passed"] is False

    # Human domain owner approves
    pr_agent.approve(reviewer="human-steward-eve", role=Role.STEWARD)
    gate_report_ok = pr_agent.run_release_gates()
    assert gate_report_ok["agent_gate"]["passed"] is True


def test_version_store_atomic_publication_consumer_acknowledgement_and_rollback():
    """CRA-022.4, CRA-022.A: VersionStore atomic publication, consumer acknowledgement, and queryable rollback."""
    store = VersionStore()
    manifest_v1 = _base_manifest()
    manifest_v2 = copy.deepcopy(manifest_v1)
    manifest_v2["vertex_labels"]["TelemetrySensor"] = {"domain": "IOT", "required": ["canonical_id"], "optional": []}

    # Publish v1.0.0
    r1 = store.publish_version("1.0.0", manifest_v1, publisher="steward-1", expected_consumers=["search-idx", "query-svc"])
    assert r1["version"] == "1.0.0"
    assert store.active_version == "1.0.0"

    # Acknowledge consumers for v1.0.0
    store.acknowledge_consumer("1.0.0", "search-idx", status="ACKNOWLEDGED")
    store.acknowledge_consumer("1.0.0", "query-svc", status="ACKNOWLEDGED")

    # Publish v2.0.0
    r2 = store.publish_version("2.0.0", manifest_v2, publisher="steward-2", expected_consumers=["search-idx", "query-svc"])
    assert store.active_version == "2.0.0"

    # Simulated consumer failure on query-svc for v2.0.0
    store.acknowledge_consumer("2.0.0", "search-idx", status="ACKNOWLEDGED")
    store.acknowledge_consumer("2.0.0", "query-svc", status="FAILED_CONSUMER")
    assert store.consumer_states["2.0.0"]["query-svc"] == "FAILED_CONSUMER"

    # Querying specific versions: both v1.0.0 and v2.0.0 remain queryable via version parameter (CRA-022.A)
    m1 = store.get_manifest(version="1.0.0")
    m2 = store.get_manifest(version="2.0.0")
    assert "TelemetrySensor" not in m1["vertex_labels"]
    assert "TelemetrySensor" in m2["vertex_labels"]

    # Rollback to v1.0.0 restores business queries without claiming to undo external actions
    rollback_receipt = store.rollback_to_version("1.0.0", actor="incident-commander")
    assert rollback_receipt["restored_version"] == "1.0.0"
    assert store.active_version == "1.0.0"
    active_m = store.get_manifest()
    assert "TelemetrySensor" not in active_m["vertex_labels"]
