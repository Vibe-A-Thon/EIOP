"""Unit tests for the claim/truth conflict model (GAP-TRUTH-001..010)."""

import pytest

from eoip.truth import Claim, ResolutionDecision, TruthStore
from eoip.truth.models import CanonicalAssertion


def _claim(cid: str, value: str, authority: float = 0.8, extraction: float = 0.9,
           validation: float | None = 0.8, source: str | None = None,
           asserted_at: str = "2026-01-01T00:00:00+00:00") -> Claim:
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


@pytest.fixture()
def store() -> TruthStore:
    return TruthStore()


class TestClaimModel:
    def test_claim_defaults(self):
        claim = _claim("c1", "alice")
        assert claim.status == "pending"
        assert claim.claim_id.startswith("urn:eoip:truth:claim:")

    def test_composite_score(self):
        claim = _claim("c1", "alice", authority=0.8, extraction=0.5, validation=0.6)
        assert claim.composite_score() == pytest.approx(0.8 * 0.5 * 0.8)


class TestContradictionDetection:
    def test_same_value_is_not_a_contradiction(self, store):
        store.add_claim(_claim("c1", "alice"))
        store.add_claim(_claim("c2", "alice"))
        assert store.find_contradictions("urn:eoip:entity:svc:orders", "owner") == []

    def test_differing_values_flagged_tr006(self, store):
        store.add_claim(_claim("c1", "alice"))
        store.add_claim(_claim("c2", "bob"))
        group = store.find_contradictions("urn:eoip:entity:svc:orders", "owner")
        assert {c.value for c in group} == {"alice", "bob"}

    def test_contradictions_index(self, store):
        store.add_claim(_claim("c1", "alice"))
        store.add_claim(_claim("c2", "bob"))
        assert len(store.contradictions()) == 1


class TestResolutionPolicies:
    def _conflict(self, store):
        store.add_claim(_claim("c1", "alice", authority=0.9, source="high"))
        store.add_claim(_claim("c2", "bob", authority=0.4, source="low"))
        return "urn:eoip:entity:svc:orders", "owner"

    def test_highest_authority_tr007(self, store):
        s, p = self._conflict(store)
        decision = store.resolve(s, p, policy="highest-authority")
        assert decision.policy == "highest-authority"
        chosen = store.get_claim(decision.chosen_claim_id)
        assert chosen.value == "alice"
        assertion = store.get_assertion(s, p)
        assert assertion.value == "alice"
        assert isinstance(assertion, CanonicalAssertion)

    def test_highest_confidence_tr007(self, store):
        s, p = self._conflict(store)
        decision = store.resolve(s, p, policy="highest-confidence")
        assert store.get_claim(decision.chosen_claim_id).value == "alice"

    def test_newest_tr007(self, store):
        store.add_claim(_claim("c1", "alice", asserted_at="2026-01-01T00:00:00+00:00"))
        store.add_claim(_claim("c2", "bob", asserted_at="2026-06-01T00:00:00+00:00"))
        s, p = "urn:eoip:entity:svc:orders", "owner"
        decision = store.resolve(s, p, policy="newest")
        assert store.get_claim(decision.chosen_claim_id).value == "bob"

    def test_manual_requires_adjudicator_tr008(self, store):
        s, p = self._conflict(store)
        with pytest.raises(ValueError):
            store.resolve(s, p, policy="manual", manual_choice="urn:eoip:truth:claim:c2")

    def test_manual_adjudication_tr008(self, store):
        s, p = self._conflict(store)
        decision = store.resolve(
            s, p, policy="manual", adjudicator="admin@example.com",
            manual_choice="urn:eoip:truth:claim:c2",
        )
        assert decision.adjudicator == "admin@example.com"
        assert store.get_assertion(s, p).value == "bob"

    def test_unknown_policy_rejected(self, store):
        with pytest.raises(ValueError):
            store.resolve("urn:eoip:entity:svc:orders", "owner", policy="coin-flip")

    def test_disabled_policy_rejected(self):
        store = TruthStore(policies=["highest-authority"])
        store.add_claim(_claim("c1", "alice"))
        store.add_claim(_claim("c2", "bob"))
        with pytest.raises(ValueError):
            store.resolve("urn:eoip:entity:svc:orders", "owner", policy="newest")


class TestRetentionTr009:
    def test_rejected_claims_retained(self, store):
        s, p = "urn:eoip:entity:svc:orders", "owner"
        store.add_claim(_claim("c1", "alice"))
        store.add_claim(_claim("c2", "bob"))
        store.resolve(s, p)
        statuses = {c.status for c in store.claims_for(s, p)}
        assert statuses == {"accepted", "rejected"}
        assert len(store.claims_for(s, p)) == 2

    def test_fresher_same_value_marks_obsolete(self, store):
        store.add_claim(_claim("c1", "alice", asserted_at="2026-01-01T00:00:00+00:00"))
        store.add_claim(_claim("c2", "bob", asserted_at="2026-01-02T00:00:00+00:00"))
        s, p = "urn:eoip:entity:svc:orders", "owner"
        store.resolve(s, p)
        rejected = store.get_claim("urn:eoip:truth:claim:c2")
        store.add_claim(_claim("c3", "bob", asserted_at="2026-06-01T00:00:00+00:00"))
        assert rejected.status == "obsolete"
        assert store.get_claim("urn:eoip:truth:claim:c3").status == "pending"


class TestExplanationTr010:
    def test_explain_selected_fact(self, store):
        store.add_claim(_claim("c1", "alice", authority=0.9))
        store.add_claim(_claim("c2", "bob", authority=0.3))
        s, p = "urn:eoip:entity:svc:orders", "owner"
        store.resolve(s, p)
        explanation = store.explain(s, p)
        assert explanation["canonical"]["value"] == "alice"
        assert "highest authority" in explanation["explanation"]
        assert len(explanation["competing_claims"]) == 1
        assert explanation["decision"]["policy"] == "highest-authority"

    def test_explain_missing_fact(self, store):
        explanation = store.explain("urn:eoip:entity:svc:orders", "owner")
        assert explanation["canonical"] is None


class TestExportImport:
    def test_round_trip(self, store):
        store.add_claim(_claim("c1", "alice"))
        store.add_claim(_claim("c2", "bob"))
        s, p = "urn:eoip:entity:svc:orders", "owner"
        store.resolve(s, p)
        payload = store.export()

        restored = TruthStore.load(payload)
        assert restored.get_assertion(s, p).value == "alice"
        assert {c.status for c in restored.claims_for(s, p)} == {"accepted", "rejected"}
        assert len(restored.list_decisions()) == 1
        assert isinstance(restored.list_decisions()[0], ResolutionDecision)
        assert restored.explain(s, p)["canonical"]["value"] == "alice"
