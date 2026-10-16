import pytest

from eoip.truth import Claim, ResolutionDecision, TruthStore
from eoip.truth.models import CanonicalAssertion


def _claim(
    cid: str,
    value: str,
    authority: float = 0.8,
    extraction: float = 0.9,
    validation: float | None = 0.8,
    source: str | None = None,
    asserted_at: str = "2026-01-01T00:00:00+00:00",
) -> Claim:
    return Claim(
        claim_id=f"urn:eoip:truth:claim:{cid}",
        subject_id="urn:eoip:entity:svc:orders",
        predicate="owner",
        value=value,
        source_id=source or f"urn:eoip:source:{cid}",
        source_authority=authority,
        extraction_confidence=extraction,
        validation_confidence=validation,
        asserted_at=asserted_at,
    )


@pytest.fixture
def store() -> TruthStore:
    return TruthStore()


@pytest.mark.req("GAP-TRUTH-002")
def test_claims_represented_separately_from_canonical_facts(store):
    c1 = _claim("c1", "alice")
    c2 = _claim("c2", "bob")
    store.add_claim(c1)
    store.add_claim(c2)

    # Claims exist independently in store
    assert store.get_claim(c1.claim_id) is not None
    assert store.get_claim(c2.claim_id) is not None
    assert store.get_assertion("urn:eoip:entity:svc:orders", "owner") is None

    # Resolution produces separate CanonicalAssertion referencing winning claim
    store.resolve("urn:eoip:entity:svc:orders", "owner")
    assertion = store.get_assertion("urn:eoip:entity:svc:orders", "owner")
    assert isinstance(assertion, CanonicalAssertion)
    assert assertion.chosen_claim_id in {c1.claim_id, c2.claim_id}
    # Original claims are preserved, not deleted
    assert store.get_claim(c1.claim_id) is not None
    assert store.get_claim(c2.claim_id) is not None


@pytest.mark.req("GAP-TRUTH-003")
def test_store_source_authority_score(store):
    c_high = _claim("c_high", "alice", authority=0.95, source="src:github:admin")
    c_low = _claim("c_low", "bob", authority=0.40, source="src:slack:channel")
    store.add_claim(c_high)
    store.add_claim(c_low)

    assert store.get_claim(c_high.claim_id).source_authority == 0.95
    assert store.get_claim(c_low.claim_id).source_authority == 0.40

    decision = store.resolve("urn:eoip:entity:svc:orders", "owner", policy="highest-authority")
    assert decision.chosen_claim_id == c_high.claim_id
    assert "0.95" in decision.rationale


@pytest.mark.req("GAP-TRUTH-004")
def test_store_extraction_confidence(store):
    c_conf = _claim("c_conf", "alice", extraction=0.99)
    c_weak = _claim("c_weak", "bob", extraction=0.20)
    store.add_claim(c_conf)
    store.add_claim(c_weak)

    assert store.get_claim(c_conf.claim_id).extraction_confidence == 0.99
    assert store.get_claim(c_weak.claim_id).extraction_confidence == 0.20
    assert c_conf.composite_score() > c_weak.composite_score()


@pytest.mark.req("GAP-TRUTH-005")
def test_store_validation_confidence(store):
    c_val = _claim("c_val", "alice", validation=0.95)
    c_noval = _claim("c_noval", "bob", validation=0.10)
    store.add_claim(c_val)
    store.add_claim(c_noval)

    assert store.get_claim(c_val.claim_id).validation_confidence == 0.95
    assert store.get_claim(c_noval.claim_id).validation_confidence == 0.10
    assert c_val.composite_score() > c_noval.composite_score()


@pytest.mark.req("GAP-TRUTH-006")
def test_detect_contradictory_claims(store):
    # Same value does not contradict
    store.add_claim(_claim("c1", "alice"))
    store.add_claim(_claim("c2", "alice"))
    assert store.find_contradictions("urn:eoip:entity:svc:orders", "owner") == []

    # Divergent values detected as conflict
    store.add_claim(_claim("c3", "bob"))
    conflicts = store.find_contradictions("urn:eoip:entity:svc:orders", "owner")
    assert len(conflicts) >= 2
    assert {c.value for c in conflicts} == {"alice", "bob"}

    indexed = store.contradictions()
    assert ("urn:eoip:entity:svc:orders", "owner") in indexed


@pytest.mark.req("GAP-TRUTH-007")
def test_configurable_truth_resolution_policies():
    def _conflict_store():
        s = TruthStore()
        s.add_claim(_claim("c_auth", "alice", authority=0.95, extraction=0.5, asserted_at="2026-01-01T00:00:00+00:00"))
        s.add_claim(_claim("c_comp", "bob", authority=0.70, extraction=0.95, validation=0.95, asserted_at="2026-02-01T00:00:00+00:00"))
        s.add_claim(_claim("c_new", "charlie", authority=0.60, extraction=0.6, asserted_at="2026-03-01T00:00:00+00:00"))
        return s

    s, p = "urn:eoip:entity:svc:orders", "owner"

    # Policy: highest-authority
    store1 = _conflict_store()
    d_auth = store1.resolve(s, p, policy="highest-authority")
    assert d_auth.chosen_claim_id == "urn:eoip:truth:claim:c_auth"

    # Policy: highest-confidence
    store2 = _conflict_store()
    d_conf = store2.resolve(s, p, policy="highest-confidence")
    assert d_conf.chosen_claim_id == "urn:eoip:truth:claim:c_comp"

    # Policy: newest
    store3 = _conflict_store()
    d_new = store3.resolve(s, p, policy="newest")
    assert d_new.chosen_claim_id == "urn:eoip:truth:claim:c_new"


@pytest.mark.req("GAP-TRUTH-008")
def test_permit_human_adjudication(store):
    store.add_claim(_claim("c1", "alice"))
    store.add_claim(_claim("c2", "bob"))

    s, p = "urn:eoip:entity:svc:orders", "owner"
    # Requires adjudicator
    with pytest.raises(ValueError):
        store.resolve(s, p, policy="manual", manual_choice="urn:eoip:truth:claim:c2")

    decision = store.resolve(
        s,
        p,
        policy="manual",
        adjudicator="lead-architect@example.com",
        manual_choice="urn:eoip:truth:claim:c2",
    )
    assert decision.policy == "manual"
    assert decision.adjudicator == "lead-architect@example.com"
    assert decision.chosen_claim_id == "urn:eoip:truth:claim:c2"
    assert store.get_assertion(s, p).value == "bob"


@pytest.mark.req("GAP-TRUTH-009")
def test_retain_rejected_and_obsolete_claims(store):
    s, p = "urn:eoip:entity:svc:orders", "owner"
    store.add_claim(_claim("c1", "alice", authority=0.9))
    store.add_claim(_claim("c2", "bob", authority=0.5))
    store.resolve(s, p, policy="highest-authority")

    # Rejected claim is retained with status 'rejected'
    assert store.get_claim("urn:eoip:truth:claim:c1").status == "accepted"
    assert store.get_claim("urn:eoip:truth:claim:c2").status == "rejected"
    assert len(store.claims_for(s, p)) == 2

    # A fresher assertion with same value marks previous as obsolete, retaining audit history
    store.add_claim(_claim("c3", "bob", asserted_at="2026-05-01T00:00:00+00:00"))
    assert store.get_claim("urn:eoip:truth:claim:c2").status == "obsolete"
    assert store.get_claim("urn:eoip:truth:claim:c3").status == "pending"


@pytest.mark.req("GAP-TRUTH-010")
def test_explain_why_canonical_fact_selected(store):
    s, p = "urn:eoip:entity:svc:orders", "owner"
    store.add_claim(_claim("c1", "alice", authority=0.9))
    store.add_claim(_claim("c2", "bob", authority=0.4))
    store.resolve(s, p, policy="highest-authority")

    explanation = store.explain(s, p)
    assert explanation["canonical"]["value"] == "alice"
    assert "highest authority" in explanation["explanation"]
    assert len(explanation["competing_claims"]) == 1
    assert explanation["decision"]["policy"] == "highest-authority"
    assert explanation["chosen_claim"]["source_authority"] == 0.9
