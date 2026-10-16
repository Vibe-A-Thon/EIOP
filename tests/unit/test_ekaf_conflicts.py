from __future__ import annotations

import pytest
from eoip.connectors.conflicts import SourceFactAssertion, preserve_source_claims
from eoip.truth import TruthStore


@pytest.mark.req("G2-EKAF-022")
def test_acquisition_preserves_conflicting_source_claims_without_resolution() -> None:
    store = TruthStore()
    assertions = [
        SourceFactAssertion(
            source_id="jira-prod",
            subject_id="urn:eoip:service:checkout",
            predicate="owner",
            value="payments",
            source_authority=0.7,
            evidence_ref="raw/jira/PAY-1.json",
        ),
        SourceFactAssertion(
            source_id="servicenow-prod",
            subject_id="urn:eoip:service:checkout",
            predicate="owner",
            value="platform",
            source_authority=0.9,
            evidence_ref="raw/servicenow/CI-1.json",
        ),
    ]

    preserved = preserve_source_claims(store, assertions)

    assert len(preserved) == 1
    assert preserved[0].conflicting is True
    assert {claim.source_id for claim in preserved[0].claims} == {"jira-prod", "servicenow-prod"}
    assert {claim.value for claim in preserved[0].claims} == {"payments", "platform"}
    assert {claim.status for claim in preserved[0].claims} == {"pending"}
    assert store.get_assertion("urn:eoip:service:checkout", "owner") is None


@pytest.mark.req("G2-EKAF-022")
def test_acquisition_marks_non_conflicting_claim_sets_as_preserved_not_conflicting() -> None:
    store = TruthStore()

    preserved = preserve_source_claims(
        store,
        [
            SourceFactAssertion(
                source_id="jira-prod",
                subject_id="urn:eoip:service:checkout",
                predicate="tier",
                value="critical",
            ),
            SourceFactAssertion(
                source_id="catalog-prod",
                subject_id="urn:eoip:service:checkout",
                predicate="tier",
                value="critical",
            ),
        ],
    )

    assert preserved[0].conflicting is False
    assert len(preserved[0].claims) == 2
    assert {claim.status for claim in preserved[0].claims} == {"pending"}
