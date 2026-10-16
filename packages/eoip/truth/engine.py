"""Truth-resolution engine: claim intake, contradiction detection, policy-based
resolution, retention, and explanation (GAP-TRUTH-001..010).

In-memory store with JSON export/import; no external dependencies. Suitable
for later persistence via the graph store.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any

from eoip.contracts.source_event import utc_now_iso
from eoip.truth.models import CanonicalAssertion, Claim, ResolutionDecision

SUPPORTED_POLICIES = ("highest-authority", "highest-confidence", "newest", "manual")


def _urn(prefix: str, *parts: str) -> str:
    digest = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:12]
    return f"urn:eoip:truth:{prefix}:{digest}-{uuid.uuid4().hex[:8]}"


class TruthStore:
    """Holds claims, canonical assertions, and resolution decisions.

    GAP-TRUTH-001/002: conflicting claims are kept side by side; resolution
    produces a new CanonicalAssertion/ResolutionDecision and marks losing
    claims as rejected — never deletes or overwrites.
    """

    def __init__(self, policies: list[str] | None = None) -> None:
        unknown = [p for p in (policies or []) if p not in SUPPORTED_POLICIES]
        if unknown:
            raise ValueError(f"unsupported truth-resolution policies: {unknown}")
        self._policies = policies or list(SUPPORTED_POLICIES)
        self._claims: dict[str, Claim] = {}
        self._assertions: dict[tuple[str, str], CanonicalAssertion] = {}
        self._decisions: dict[str, ResolutionDecision] = {}

    # -- intake -----------------------------------------------------------

    def add_claim(self, claim: Claim) -> Claim:
        """Register a claim; returns the stored claim.

        Marks any previously accepted claim for the same (subject, predicate,
        value) as obsolete (TRUTH-009) — a fresher assertion replaces it
        without destroying history.
        """
        for existing in self._claims.values():
            if (
                existing.subject_id == claim.subject_id
                and existing.predicate == claim.predicate
                and existing.value == claim.value
                and existing.status in ("accepted", "rejected")
                and existing.claim_id != claim.claim_id
            ):
                existing.status = "obsolete"
        self._claims[claim.claim_id] = claim
        return claim

    # -- contradiction detection (TRUTH-006) ------------------------------

    def find_contradictions(self, subject_id: str, predicate: str) -> list[Claim]:
        """Claims on the same subject+predicate whose values differ (TRUTH-006)."""
        group = [
            c
            for c in self._claims.values()
            if c.subject_id == subject_id and c.predicate == predicate and c.status in ("pending", "accepted")
        ]
        if not group:
            return []
        values = {c.value for c in group}
        if len(values) <= 1:
            return []
        return sorted(group, key=lambda c: c.composite_score(), reverse=True)

    def contradictions(self) -> dict[tuple[str, str], list[Claim]]:
        """All contradictory (subject, predicate) groups in the store."""
        keys = {(c.subject_id, c.predicate) for c in self._claims.values()}
        return {
            k: group
            for k in keys
            if (group := self.find_contradictions(k[0], k[1]))
        }

    # -- resolution (TRUTH-007/008) ---------------------------------------

    def resolve(
        self,
        subject_id: str,
        predicate: str,
        policy: str = "highest-authority",
        adjudicator: str | None = None,
        manual_choice: str | None = None,
    ) -> ResolutionDecision:
        """Resolve conflicting claims into a canonical assertion."""
        if policy not in SUPPORTED_POLICIES:
            raise ValueError(f"unknown policy {policy!r}; supported: {SUPPORTED_POLICIES}")
        if policy not in self._policies:
            raise ValueError(f"policy {policy!r} not enabled in this store")
        group = self.find_contradictions(subject_id, predicate)
        if not group:
            raise ValueError(f"no contradictory claims for {subject_id} {predicate}")

        if policy == "manual":
            if not adjudicator:
                raise ValueError("manual adjudication requires an adjudicator (TRUTH-008)")
            if manual_choice not in {c.claim_id for c in group}:
                raise ValueError("manual_choice must be one of the competing claim ids")
            chosen = next(c for c in group if c.claim_id == manual_choice)
            rationale = f"Manually adjudicated by {adjudicator}."
        elif policy == "highest-authority":
            chosen = max(group, key=lambda c: (c.source_authority, c.composite_score()))
            rationale = (
                f"Selected claim from source with highest authority "
                f"({chosen.source_authority:.2f}): {chosen.source_id}."
            )
        elif policy == "highest-confidence":
            chosen = max(group, key=lambda c: c.composite_score())
            rationale = (
                f"Selected claim with highest combined confidence "
                f"({chosen.composite_score():.3f})."
            )
        else:  # newest
            chosen = max(group, key=lambda c: c.asserted_at)
            rationale = f"Selected most recently asserted claim ({chosen.asserted_at})."

        decision = ResolutionDecision(
            decision_id=_urn("decision", subject_id, predicate, utc_now_iso()),
            subject_id=subject_id,
            predicate=predicate,
            policy=policy,
            chosen_claim_id=chosen.claim_id,
            competing_claim_ids=[c.claim_id for c in group if c.claim_id != chosen.claim_id],
            rationale=rationale,
            adjudicator=adjudicator if policy == "manual" else None,
        )
        self._decisions[decision.decision_id] = decision

        for c in group:
            c.status = "accepted" if c.claim_id == chosen.claim_id else "rejected"
        assertion = CanonicalAssertion(
            assertion_id=_urn("assertion", subject_id, predicate, chosen.value),
            subject_id=subject_id,
            predicate=predicate,
            value=chosen.value,
            chosen_claim_id=chosen.claim_id,
            decision_id=decision.decision_id,
        )
        self._assertions[(subject_id, predicate)] = assertion
        return decision

    # -- explanation (TRUTH-010) ------------------------------------------

    def explain(self, subject_id: str, predicate: str) -> dict[str, Any]:
        """Why was this fact selected? (TRUTH-010)"""
        assertion = self._assertions.get((subject_id, predicate))
        if assertion is None:
            return {
                "subject_id": subject_id,
                "predicate": predicate,
                "canonical": None,
                "explanation": "No canonical assertion exists for this fact.",
            }
        decision = self._decisions.get(assertion.decision_id)
        chosen = self._claims.get(assertion.chosen_claim_id)
        competitors = [
            self._claims[cid]
            for cid in decision.competing_claim_ids
            if cid in self._claims
        ]
        explanation = decision.rationale
        if chosen is not None:
            explanation += (
                f" Winning claim {chosen.claim_id} (value={chosen.value!r}) scored "
                f"authority={chosen.source_authority:.2f}, "
                f"extraction={chosen.extraction_confidence:.2f}, "
                f"composite={chosen.composite_score():.3f}."
            )
        return {
            "subject_id": subject_id,
            "predicate": predicate,
            "canonical": assertion.model_dump(),
            "decision": decision.model_dump(),
            "chosen_claim": chosen.model_dump() if chosen else None,
            "competing_claims": [c.model_dump() for c in competitors],
            "explanation": explanation,
        }

    # -- queries ----------------------------------------------------------

    def get_assertion(self, subject_id: str, predicate: str) -> CanonicalAssertion | None:
        return self._assertions.get((subject_id, predicate))

    def get_claim(self, claim_id: str) -> Claim | None:
        return self._claims.get(claim_id)

    def claims_for(self, subject_id: str, predicate: str) -> list[Claim]:
        return [
            c
            for c in self._claims.values()
            if c.subject_id == subject_id and c.predicate == predicate
        ]

    def list_decisions(self) -> list[ResolutionDecision]:
        return list(self._decisions.values())

    # -- persistence ------------------------------------------------------

    def export(self) -> str:
        """Deterministic JSON snapshot (in-memory persistence fallback)."""
        return json.dumps(
            {
                "policies": self._policies,
                "claims": sorted(
                    (c.model_dump() for c in self._claims.values()),
                    key=lambda d: d["claim_id"],
                ),
                "assertions": sorted(
                    (a.model_dump() for a in self._assertions.values()),
                    key=lambda d: d["assertion_id"],
                ),
                "decisions": sorted(
                    (d.model_dump() for d in self._decisions.values()),
                    key=lambda d: d["decision_id"],
                ),
            },
            indent=2,
            sort_keys=True,
        )

    @classmethod
    def load(cls, payload: str) -> "TruthStore":
        """Rebuild a TruthStore from export() output."""
        data = json.loads(payload)
        store = cls(policies=data.get("policies"))
        for raw in data.get("claims", []):
            claim = Claim(**raw)
            store._claims[claim.claim_id] = claim
        for raw in data.get("assertions", []):
            a = CanonicalAssertion(**raw)
            store._assertions[(a.subject_id, a.predicate)] = a
        for raw in data.get("decisions", []):
            d = ResolutionDecision(**raw)
            store._decisions[d.decision_id] = d
        return store
