"""Automated scanner for claims, competitive positioning, and disclosure governance (CRA-041.A)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from eoip.claims.registry import (
    ClaimsRegistry,
    STANDARDS_CLAUSE_MAP,
    SEVEN_INVERSIONS,
    PATENT_CANDIDATE_TITLES,
)


class ScanViolation(BaseModel):
    file_path: str
    line_number: int
    violation_type: str
    matched_text: str
    message: str


# Regex triggers
STANDARDS_PATTERNS = {
    "SHACL": re.compile(r"\bSHACL(?:\s+Core|\s+compliant|\s+conformance|\s+validation)?\b", re.IGNORECASE),
    "RDF 1.1": re.compile(r"\bRDF\s+1\.1\b", re.IGNORECASE),
    "JSON-LD 1.1": re.compile(r"\bJSON-LD\s+1\.1\b", re.IGNORECASE),
    "OWL 2": re.compile(r"\bOWL\s+2(?:\s+DL)?\b", re.IGNORECASE),
    "SPARQL 1.1": re.compile(r"\bSPARQL\s+1\.1\b", re.IGNORECASE),
    "WCAG 2.2 AA": re.compile(r"\bWCAG\s+2\.2(?:\s+AA)?\b", re.IGNORECASE),
}

SUPERIORITY_PATTERN = re.compile(
    r"\b(no competitor(?:\s+has this)?|unique in the industry|unrivaled|infinitely superior)\b",
    re.IGNORECASE,
)

INVERSION_PATTERN = re.compile(
    r"\b(inversion\s+(?:I1|I3|I6|I13|I15|I16|I17)|already won)\b",
    re.IGNORECASE,
)

COMPETITOR_TCO_PATTERN = re.compile(
    r"\b([0-9]+%\s+lower\s+TCO|competitor\s+TCO|vendor\s+TCO|negotiation-consultancy\s+TCO)\b",
    re.IGNORECASE,
)

SCORECARD_PATTERN = re.compile(
    r"\b(ontology-comparison-matrix\.csv|aggregated master matrix|self-score[s]?\s*(?:2\.9|3\.6|4\.2))\b",
    re.IGNORECASE,
)

CLAIM_ID_TAG_PATTERN = re.compile(r"\[claim:\s*([A-Za-z0-9_-]+)\]", re.IGNORECASE)


class ClaimsScanner:
    """Scans repository documentation and sources for unauthorized claims or disclosures."""

    def __init__(
        self,
        registry: ClaimsRegistry,
        ledger_path: Optional[Path | str] = None,
        ledger_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.registry = registry
        self.ledger_path = Path(ledger_path) if ledger_path else None
        self.ledger_data = ledger_data
        self.ledger_items: Dict[str, Dict[str, Any]] = {}

        if self.ledger_data:
            self.ledger_items = {it["id"]: it for it in self.ledger_data.get("items", [])}
        elif self.ledger_path and self.ledger_path.exists():
            try:
                raw = json.loads(self.ledger_path.read_text(encoding="utf-8"))
                self.ledger_items = {it["id"]: it for it in raw.get("items", [])}
            except Exception:
                pass

    def scan_text(self, text: str, filename: str = "document.md") -> List[ScanViolation]:
        violations: List[ScanViolation] = []
        lines = text.splitlines()

        for idx, line in enumerate(lines, start=1):
            # Check for claim tag on this line
            claim_tag_match = CLAIM_ID_TAG_PATTERN.search(line)
            claim_id = claim_tag_match.group(1) if claim_tag_match else None
            referenced_claim = self.registry.get_claim(claim_id) if claim_id else None

            # 1. Check standards triggers (CRA-041.2, CRA-041.A case a)
            for std_name, pat in STANDARDS_PATTERNS.items():
                m = pat.search(line)
                if m:
                    req_clause = STANDARDS_CLAUSE_MAP.get(std_name, "CRA-020.1")
                    clause_item = self.ledger_items.get(req_clause)
                    clause_state = clause_item.get("state") if clause_item else "NOT_FOUND"

                    # If clause is not ACCEPTED in ledger, block immediately
                    if clause_state != "ACCEPTED":
                        violations.append(
                            ScanViolation(
                                file_path=filename,
                                line_number=idx,
                                violation_type="UNACCEPTED_STANDARDS_PREREQUISITE",
                                matched_text=m.group(0),
                                message=(
                                    f"Standards claim '{m.group(0)}' published while prerequisite "
                                    f"clause '{req_clause}' is {clause_state} (must be ACCEPTED; closes risk OR6)."
                                ),
                            )
                        )
                    elif referenced_claim:
                        # If a specific claim ID was tagged, verify that claim's approvals & status
                        publishable, reasons = self.registry.evaluate_claim(
                            referenced_claim.id,
                            ledger_data={"items": list(self.ledger_items.values())},
                        )
                        if not publishable:
                            violations.append(
                                ScanViolation(
                                    file_path=filename,
                                    line_number=idx,
                                    violation_type="UNAPPROVED_CLAIM",
                                    matched_text=m.group(0),
                                    message=f"Claim '{referenced_claim.id}' is not publishable: {'; '.join(reasons)}",
                                )
                            )

            # 2. Check 'already won' inversions and superiority claims (CRA-041.3, CRA-041.A case b)
            m_inv = INVERSION_PATTERN.search(line)
            if m_inv:
                # Must reference an approved claim with verified receipt evidence
                has_receipt = False
                if referenced_claim:
                    has_receipt = any(
                        ev.kind == "ledger_clause" and self.ledger_items.get(ev.ref_id, {}).get("state") == "ACCEPTED"
                        for ev in referenced_claim.evidence_refs
                    )
                if not has_receipt:
                    violations.append(
                        ScanViolation(
                            file_path=filename,
                            line_number=idx,
                            violation_type="UNVERIFIED_INVERSION",
                            matched_text=m_inv.group(0),
                            message=(
                                f"Inversion claim '{m_inv.group(0)}' treated as hypothesis; "
                                "publication blocked without ACCEPTED receipt evidence."
                            ),
                        )
                    )

            m_sup = SUPERIORITY_PATTERN.search(line)
            if m_sup:
                # Requires Legal approval + dated competitor review
                has_legal = referenced_claim.has_approval("Legal") if referenced_claim else False
                has_comp_review = any(
                    ev.kind == "competitor_review" for ev in (referenced_claim.evidence_refs if referenced_claim else [])
                )
                if not has_legal or not has_comp_review:
                    violations.append(
                        ScanViolation(
                            file_path=filename,
                            line_number=idx,
                            violation_type="UNAPPROVED_SUPERIORITY_CLAIM",
                            matched_text=m_sup.group(0),
                            message=(
                                f"Competitive claim '{m_sup.group(0)}' requires dated competitor "
                                "review (CRA-042) and recorded Legal approval."
                            ),
                        )
                    )

            # 3. Check Competitor TCO / performance figures (CRA-041.5, CRA-041.A case c)
            m_tco = COMPETITOR_TCO_PATTERN.search(line)
            if m_tco:
                # Block if unverified or vendor-sourced without independent verification
                is_independently_verified = False
                if referenced_claim and referenced_claim.metadata.get("verification_status") == "INDEPENDENTLY_VERIFIED":
                    is_independently_verified = True
                if not is_independently_verified or "unverified" in line.lower():
                    violations.append(
                        ScanViolation(
                            file_path=filename,
                            line_number=idx,
                            violation_type="UNVERIFIED_COMPETITOR_FIGURE",
                            matched_text=m_tco.group(0),
                            message=(
                                f"Competitor figure '{m_tco.group(0)}' is UNVERIFIED; "
                                "blocked from customer-facing material."
                            ),
                        )
                    )

            # 4. Check Patent Candidate disclosures (CRA-041.6, CRA-041.A case d)
            for cand_title in PATENT_CANDIDATE_TITLES:
                if cand_title.lower() in line.lower():
                    # Check if legal decision H-12 has approved disclosure
                    cand_permitted = False
                    for p in self.registry.patent_candidates.values():
                        if p.title.lower() == cand_title.lower() and p.public_disclosure_permitted:
                            cand_permitted = True
                            break
                    if not cand_permitted:
                        violations.append(
                            ScanViolation(
                                file_path=filename,
                                line_number=idx,
                                violation_type="PATENT_DISCLOSURE_PROHIBITED",
                                matched_text=cand_title,
                                message=(
                                    f"Patent-candidate mechanism '{cand_title}' disclosed without "
                                    "recorded Legal decision H-12 authorization."
                                ),
                            )
                        )

            # 5. Check Scorecards and self-scores (CRA-041.7)
            m_sc = SCORECARD_PATTERN.search(line)
            if m_sc:
                # If marked internal or not rescored under CRA-042, block external publication
                if not referenced_claim or not referenced_claim.metadata.get("cra_042_rescored", False):
                    violations.append(
                        ScanViolation(
                            file_path=filename,
                            line_number=idx,
                            violation_type="INTERNAL_SCORECARD_LEAK",
                            matched_text=m_sc.group(0),
                            message=(
                                f"Scorecard item '{m_sc.group(0)}' is an internal planning aid; "
                                "external use prohibited without CRA-042 rescoring."
                            ),
                        )
                    )

        return violations

    def scan_file(self, file_path: Path | str) -> List[ScanViolation]:
        p = Path(file_path)
        if not p.exists() or not p.is_file():
            return []
        try:
            content = p.read_text(encoding="utf-8")
        except Exception:
            return []
        return self.scan_text(content, filename=str(p))

    def scan_directory(
        self,
        dir_path: Path | str,
        extensions: Optional[List[str]] = None,
    ) -> List[ScanViolation]:
        valid_exts = set(extensions or [".md", ".html", ".txt", ".rst"])
        p = Path(dir_path)
        if not p.exists():
            return []

        # Internal directories that are not external publications
        skip_dirs = {"restricted", "decisions", "baseline", ".audit-scratch"}

        all_violations: List[ScanViolation] = []
        for file in p.rglob("*"):
            if file.is_file() and file.suffix in valid_exts:
                # Skip internal directories
                if any(skip_part in file.parts for skip_part in skip_dirs) or any(part.startswith("audit-") for part in file.parts):
                    continue
                all_violations.extend(self.scan_file(file))

        return all_violations
