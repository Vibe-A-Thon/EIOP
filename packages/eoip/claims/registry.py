"""Claims Register implementation and validation engine (CRA-041.1 - CRA-041.7)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
import yaml

from eoip.claims.schema import (
    ClaimRecord,
    ClaimStatus,
    PatentCandidateRecord,
    CompetitorDataPoint,
    ScorecardRecord,
)

# Standard to requirement clause mapping (CRA-041.2 / OR6 / Decision H-05)
STANDARDS_CLAUSE_MAP: Dict[str, str] = {
    "RDF 1.1": "CRA-016.1",
    "JSON-LD 1.1": "CRA-016.3",
    "OWL 2": "CRA-016.9",
    "SHACL": "CRA-020.1",
    "SHACL Core": "CRA-020.1",
    "SPARQL 1.1": "CRA-024.1",
    "WCAG 2.2 AA": "CRA-030.1",
}

# The 7 inversions tracked under CRA-041.3
SEVEN_INVERSIONS: Set[str] = {"I1", "I3", "I6", "I13", "I15", "I16", "I17"}

# The 5 patent candidates listed in OCA section 8.3 (CRA-041.6)
PATENT_CANDIDATE_TITLES: List[str] = [
    "semver from semantic diff",
    "migration-script generation from ontology diff",
    "hybrid per-rule materialize/virtualize reasoning with a cost model",
    "AI-suggested declarative source-to-ontology mappings",
    "combined structural plus embedding drift driving evolution proposals",
]


class ClaimsRegistry:
    """Manages the versioned Claims Register and enforces disclosure governance."""

    def __init__(
        self,
        claims: Optional[List[ClaimRecord]] = None,
        patent_candidates: Optional[List[PatentCandidateRecord]] = None,
        competitor_data: Optional[List[CompetitorDataPoint]] = None,
        scorecards: Optional[List[ScorecardRecord]] = None,
        version: str = "1.0.0",
    ) -> None:
        self.claims: Dict[str, ClaimRecord] = {c.id: c for c in (claims or [])}
        self.patent_candidates: Dict[str, PatentCandidateRecord] = {
            p.candidate_id: p for p in (patent_candidates or [])
        }
        self.competitor_data: List[CompetitorDataPoint] = competitor_data or []
        self.scorecards: List[ScorecardRecord] = scorecards or []
        self.version = version

    @classmethod
    def load_from_yaml(
        cls,
        claims_yaml_path: Path | str,
        patent_yaml_path: Optional[Path | str] = None,
    ) -> "ClaimsRegistry":
        claims_p = Path(claims_yaml_path)
        if not claims_p.exists():
            return cls()

        data = yaml.safe_load(claims_p.read_text(encoding="utf-8")) or {}
        version = str(data.get("version", "1.0.0"))
        raw_claims = data.get("claims", [])
        claims = [ClaimRecord.model_validate(c) for c in raw_claims]

        raw_comp = data.get("competitor_data", [])
        competitor_data = [CompetitorDataPoint.model_validate(c) for c in raw_comp]

        raw_scorecards = data.get("scorecards", [])
        scorecards = [ScorecardRecord.model_validate(s) for s in raw_scorecards]

        patent_candidates: List[PatentCandidateRecord] = []
        if patent_yaml_path and Path(patent_yaml_path).exists():
            pat_data = yaml.safe_load(Path(patent_yaml_path).read_text(encoding="utf-8")) or {}
            patent_candidates = [
                PatentCandidateRecord.model_validate(p)
                for p in pat_data.get("patent_candidates", [])
            ]
        elif "patent_candidates" in data:
            patent_candidates = [
                PatentCandidateRecord.model_validate(p)
                for p in data.get("patent_candidates", [])
            ]

        return cls(
            claims=claims,
            patent_candidates=patent_candidates,
            competitor_data=competitor_data,
            scorecards=scorecards,
            version=version,
        )

    def add_claim(self, claim: ClaimRecord) -> None:
        self.claims[claim.id] = claim

    def get_claim(self, claim_id: str) -> Optional[ClaimRecord]:
        return self.claims.get(claim_id)

    def evaluate_claim(
        self,
        claim_id: str,
        ledger_path: Optional[Path | str] = None,
        ledger_data: Optional[Dict[str, Any]] = None,
        current_time: Optional[datetime] = None,
    ) -> Tuple[bool, List[str]]:
        """Evaluate whether a claim is authorized for external publication.
        
        Returns:
            (is_publishable, list_of_reasons_if_blocked)
        """
        claim = self.claims.get(claim_id)
        if not claim:
            return False, [f"Claim ID '{claim_id}' not found in Claims Register."]

        reasons: List[str] = []
        now = current_time or datetime.now(timezone.utc)

        # 1. Status check
        if claim.status != ClaimStatus.APPROVED:
            reasons.append(f"Claim '{claim_id}' status is {claim.status}, must be APPROVED.")

        # 2. Expiry check
        if claim.is_expired(now):
            reasons.append(f"Claim '{claim_id}' expired at {claim.expiry.isoformat()}.")

        # 3. Load ledger if provided to check evidence clauses
        ledger_items: Dict[str, Dict[str, Any]] = {}
        if ledger_data:
            ledger_items = {it["id"]: it for it in ledger_data.get("items", [])}
        elif ledger_path and Path(ledger_path).exists():
            try:
                raw_ledger = json.loads(Path(ledger_path).read_text(encoding="utf-8"))
                ledger_items = {it["id"]: it for it in raw_ledger.get("items", [])}
            except Exception as e:
                reasons.append(f"Could not load ledger from {ledger_path}: {e}")

        # 4. Standards-conformance gating (CRA-041.2 / OR6 / Decision H-05)
        for std_name, req_clause in STANDARDS_CLAUSE_MAP.items():
            if std_name.lower() in claim.wording.lower():
                # Check underlying clause is ACCEPTED
                if ledger_items:
                    clause_item = ledger_items.get(req_clause)
                    if not clause_item or clause_item.get("state") != "ACCEPTED":
                        reasons.append(
                            f"Standards claim '{std_name}' blocked: prerequisite requirement "
                            f"clause '{req_clause}' is not ACCEPTED in ledger (closes risk OR6)."
                        )
                # Verify Legal and Marketing approvals exist
                if not claim.has_approval("Legal"):
                    reasons.append(f"Standards claim '{claim_id}' lacks Legal approval.")
                if not claim.has_approval("Marketing"):
                    reasons.append(f"Standards claim '{claim_id}' lacks Marketing approval.")

        # 5. Inversion hypothesis check (CRA-041.3)
        is_inversion = any(inv in claim.metadata.get("inversions", []) for inv in SEVEN_INVERSIONS)
        if is_inversion:
            # Must have receipts / evidence refs in ledger
            clause_refs = [
                ev.ref_id for ev in claim.evidence_refs if ev.kind == "ledger_clause"
            ]
            if not clause_refs:
                reasons.append(
                    f"Inversion claim '{claim_id}' is a hypothesis: lacks verified receipt evidence."
                )
            elif ledger_items:
                for cr in clause_refs:
                    it = ledger_items.get(cr)
                    if not it or it.get("state") != "ACCEPTED" or not it.get("receipts"):
                        reasons.append(
                            f"Inversion claim '{claim_id}' lacks ACCEPTED receipt for clause '{cr}'."
                        )

            # Check competitive superiority phrasing
            lower_wording = claim.wording.lower()
            if "no competitor" in lower_wording or "unique" in lower_wording:
                # Requires dated competitor review (CRA-042) + Legal approval
                has_competitor_review = any(
                    ev.kind == "competitor_review" for ev in claim.evidence_refs
                )
                if not has_competitor_review:
                    reasons.append(
                        f"Competitive superiority claim '{claim_id}' lacks dated, sourced "
                        f"competitor review evidence (CRA-042)."
                    )
                if not claim.has_approval("Legal"):
                    reasons.append(
                        f"Competitive superiority claim '{claim_id}' lacks required Legal approval."
                    )

        # 6. Competitor performance / TCO figures (CRA-041.5)
        if claim.category == "competitor" or "tco" in claim.wording.lower():
            if claim.metadata.get("verification_status") == "UNVERIFIED":
                reasons.append(
                    f"Competitor performance/TCO claim '{claim_id}' is marked UNVERIFIED; "
                    "blocked from customer-facing material."
                )
            if not claim.has_approval("Legal"):
                reasons.append(
                    f"Competitor performance/TCO claim '{claim_id}' lacks Legal approval."
                )

        # 7. Patent-candidate disclosure check (CRA-041.6 / H-12)
        if claim.category == "patent" or any(
            cand.lower() in claim.wording.lower() for cand in PATENT_CANDIDATE_TITLES
        ):
            cand_id = claim.metadata.get("patent_candidate_id")
            cand = self.patent_candidates.get(cand_id) if cand_id else None
            if not cand or not cand.public_disclosure_permitted:
                reasons.append(
                    f"Patent-candidate mechanism in '{claim_id}' blocked: public disclosure "
                    "requires recorded Legal decision H-12 approval."
                )

        # 8. Scorecard / self-scores check (CRA-041.7)
        if claim.category == "scorecard" or any(
            s in claim.wording for s in ["2.9", "3.6", "4.2", "comparison matrix"]
        ):
            if not claim.metadata.get("cra_042_rescored", False):
                reasons.append(
                    f"Scorecard claim '{claim_id}' is an internal planning aid only; "
                    "external use requires evidence-qualified rescoring under CRA-042."
                )

        return len(reasons) == 0, reasons

    def check_competitor_data_point(self, dp: CompetitorDataPoint) -> Tuple[bool, List[str]]:
        """Check if a competitor data point can appear in customer-facing material (CRA-041.5)."""
        reasons = []
        if dp.verification_status == "UNVERIFIED":
            reasons.append(
                f"Competitor data point '{dp.competitor} {dp.metric}' is UNVERIFIED "
                f"(source: {dp.source}); prohibited from customer-facing material."
            )
        if dp.is_vendor_source and not dp.legal_approved:
            reasons.append(
                f"Vendor-sourced data point '{dp.competitor} {dp.metric}' lacks Legal approval."
            )
        if not dp.permitted_for_external_use:
            reasons.append(
                f"Data point '{dp.competitor} {dp.metric}' is not permitted for external use."
            )
        return len(reasons) == 0, reasons

    def check_scorecard_publication(self, sc: ScorecardRecord) -> Tuple[bool, List[str]]:
        """Check if scorecard or self-scores can be published externally (CRA-041.7)."""
        reasons = []
        if sc.purpose == "INTERNAL_PLANNING_ONLY":
            reasons.append(
                f"Scorecard '{sc.matrix_name}' (score {sc.self_score}) is designated "
                "INTERNAL_PLANNING_ONLY."
            )
        if not sc.cra_042_rescored:
            reasons.append(
                f"Scorecard '{sc.matrix_name}' lacks evidence-qualified rescoring under CRA-042."
            )
        if not sc.scoring_method or not sc.scoring_date or not sc.evidence_confidence:
            reasons.append(
                f"Scorecard '{sc.matrix_name}' missing mandatory methodology, date, or confidence fields."
            )
        return len(reasons) == 0, reasons
