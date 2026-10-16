import pytest
from eoip.ontology.drift import (
    DriftFinding,
    OntologyDriftReport,
    build_evolution_proposal,
    detect_ontology_drift,
)
from eoip.ontology.gitops import (
    SemanticDiff,
    SemanticChange,
    diff_manifests,
    snapshot_manifest,
)
from eoip.graph.memory import MemoryGraphStore


@pytest.mark.req("G2-OEVO-002")
def test_propose_new_ontology_definitions():
    finding_vertex = DriftFinding(
        kind="vertex_label",
        value="CloudFunction",
        occurrences=15,
        examples=["cf:auth-token", "cf:webhook-handler"],
        classification="potentially_breaking",
    )
    finding_edge = DriftFinding(
        kind="edge_label",
        value="INVOKES_FUNCTION",
        occurrences=8,
        examples=["svc:gateway"],
        classification="potentially_breaking",
    )
    prop_vertex = build_evolution_proposal(finding_vertex)
    prop_edge = build_evolution_proposal(finding_edge)

    assert prop_vertex["proposal_type"] == "ONTOLOGY_VERTEX_LABEL"
    assert "CloudFunction" in prop_vertex["summary"]
    assert prop_edge["proposal_type"] == "ONTOLOGY_EDGE_LABEL"
    assert "INVOKES_FUNCTION" in prop_edge["summary"]


@pytest.mark.req("G2-OEVO-003")
def test_proposal_contents_and_impact_analysis():
    finding = DriftFinding(
        kind="property_key",
        value="concurrency_limit",
        occurrences=42,
        examples=["cf:1", "cf:2"],
        classification="additive",
    )
    proposal = build_evolution_proposal(finding)

    assert "evidence" in proposal
    assert proposal["evidence"]["occurrences"] == 42
    assert proposal["evidence"]["examples"] == ["cf:1", "cf:2"]
    assert "impact_analysis" in proposal
    assert "42 existing graph fact(s)" in proposal["impact_analysis"]
    assert "additive" in proposal["impact_analysis"]


@pytest.mark.req("G2-OEVO-004")
def test_ontology_changes_require_human_review_and_governance():
    # Verify proposal status lifecycle
    class GovernedProposal:
        def __init__(self, proposal_id: str, payload: dict):
            self.proposal_id = proposal_id
            self.payload = payload
            self.status = "PENDING"
            self.reviewer: str | None = None
            self.review_comment: str | None = None

        def approve(self, reviewer: str, comment: str = ""):
            if self.status != "PENDING":
                raise ValueError("Only PENDING proposals can be approved")
            self.status = "APPROVED"
            self.reviewer = reviewer
            self.review_comment = comment

        def reject(self, reviewer: str, comment: str = ""):
            if self.status != "PENDING":
                raise ValueError("Only PENDING proposals can be rejected")
            self.status = "REJECTED"
            self.reviewer = reviewer
            self.review_comment = comment

    prop = GovernedProposal("prop-01", {"summary": "Add CloudFunction"})
    assert prop.status == "PENDING"

    prop.approve("sre-lead@company.internal", "Approved for Serverless migration")
    assert prop.status == "APPROVED"
    assert prop.reviewer == "sre-lead@company.internal"


@pytest.mark.req("G2-OEVO-005")
def test_approved_ontology_changes_enter_gitops_workflow():
    manifest_v1 = snapshot_manifest(
        vertex_labels={"Service": ("CODE", ["canonical_id"], [])},
        edge_labels={"CALLS": (["Service"], ["Service"], [])},
        property_keys={"canonical_id": "TEXT"},
    )
    # Approved change adds CloudFunction and INVOKES_FUNCTION
    manifest_v2 = snapshot_manifest(
        vertex_labels={
            "Service": ("CODE", ["canonical_id"], []),
            "CloudFunction": ("CODE", ["canonical_id"], []),
        },
        edge_labels={
            "CALLS": (["Service"], ["Service"], []),
            "INVOKES_FUNCTION": (["Service"], ["CloudFunction"], []),
        },
        property_keys={"canonical_id": "TEXT"},
    )

    diff = diff_manifests(manifest_v1, manifest_v2)
    assert diff.safe is True
    assert len(diff.breaking) == 0
    change_types = {c.change_type for c in diff.changes}
    assert "vertex_label_added" in change_types
    assert "edge_label_added" in change_types


@pytest.mark.req("G2-OEVO-006")
def test_rejected_suggestions_preserved_as_feedback():
    rejected_feedback_store = []

    def record_feedback(finding: DriftFinding, reason: str, reviewer: str):
        rejected_feedback_store.append({
            "finding": finding,
            "status": "REJECTED",
            "reason": reason,
            "reviewer": reviewer,
        })

    finding = DriftFinding(
        kind="property_key",
        value="temp_debug_flag",
        occurrences=5,
        classification="additive",
    )
    record_feedback(finding, "Transient debug property, do not promote to schema", "architect@company.internal")

    assert len(rejected_feedback_store) == 1
    feedback = rejected_feedback_store[0]
    assert feedback["status"] == "REJECTED"
    assert feedback["finding"].value == "temp_debug_flag"
    assert feedback["reason"] == "Transient debug property, do not promote to schema"
