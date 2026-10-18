"""Tests for proposal promotion, SHACL constraint pre-filtering, and lineage preservation (CRA-045.2, CRA-045.4)."""

import pytest

from eoip.contracts.canonical import KnowledgeState, ProducerClass
from eoip.ai.boundary import (
    ConstraintViolationError,
    ProposalEvaluation,
    create_probabilistic_proposal,
    validate_and_promote_proposal,
)


def test_proposal_lifecycle_promotion_preserves_lineage_and_approver():
    """CRA-045.2: Probabilistic output enters as proposed; promotion to asserted keeps lineage and approver."""
    proposal = create_probabilistic_proposal(
        subject="http://example.org/entity/Emp101",
        predicate="http://example.org/pred/assignedProject",
        object_value="http://example.org/project/Apollo",
        model_name="ExtractionLLM",
        model_version="2.1.0",
        raw_score=0.94,
        prompt_text="Extract project assignments from executive memo",
        seed=42,
    )

    # Initial state is strictly PROPOSED
    assert proposal.knowledge_state == KnowledgeState.PROPOSED
    assert proposal.model_lineage.model_id == "ExtractionLLM"
    assert proposal.model_lineage.seed_bundle == {"seed": 42}
    assert proposal.approver is None

    # Dummy constraint validator that accepts
    def dummy_validator(prop):
        return ProposalEvaluation(accepted=True)

    # Promote proposal through human review
    promoted = validate_and_promote_proposal(
        proposal,
        approver="lead_data_steward_jane",
        constraint_validator=dummy_validator,
    )

    # Promoted assertion is now ASSERTED
    assert promoted.knowledge_state == KnowledgeState.ASSERTED
    # Probabilistic producer origin and lineage are preserved
    assert promoted.model_lineage.model_id == "ExtractionLLM"
    assert promoted.model_lineage.seed_bundle == {"seed": 42}
    # Approver recorded
    assert promoted.approver == "lead_data_steward_jane"


def test_proposal_violating_shacl_constraint_rejected():
    """CRA-045.4: Candidate violating SHACL constraint is rejected-by-constraint, never asserted."""
    # Proposal violating cardinality or disjointness (e.g. employee cannot report to self)
    invalid_proposal = create_probabilistic_proposal(
        subject="http://example.org/entity/Emp101",
        predicate="http://example.org/pred/reportsTo",
        object_value="http://example.org/entity/Emp101",
        model_name="ExtractionLLM",
        model_version="2.1.0",
        raw_score=0.91,
    )

    # Validator enforcing SHACL shape PersonReportsToDifferentPersonShape
    def shacl_validator(prop):
        if prop.subject.value == prop.object.value:
            return ProposalEvaluation(
                accepted=False,
                rejection_reason="Person cannot report to self (irreflexive property violation)",
                violated_constraint="PersonReportsToDifferentPersonShape",
            )
        return ProposalEvaluation(accepted=True)

    with pytest.raises(ConstraintViolationError) as exc:
        validate_and_promote_proposal(
            invalid_proposal,
            approver="lead_data_steward_jane",
            constraint_validator=shacl_validator,
        )

    assert "PersonReportsToDifferentPersonShape" in exc.value.violated_rule
    assert "rejected by deterministic constraint" in str(exc.value)
