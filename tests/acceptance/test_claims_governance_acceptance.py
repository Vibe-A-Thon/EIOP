"""Acceptance test suite for Truthful Positioning, Competitive Claims & Disclosure Governance.
Implements WP-041: CRA-041.1 - CRA-041.7 and acceptance obligation CRA-041.A.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import pytest
import yaml

from eoip.claims.schema import (
    ClaimRecord,
    ClaimStatus,
    ClaimScope,
    ClaimApproval,
    EvidenceReference,
    PatentCandidateRecord,
    CompetitorDataPoint,
    ScorecardRecord,
)
from eoip.claims.registry import (
    ClaimsRegistry,
    STANDARDS_CLAUSE_MAP,
    SEVEN_INVERSIONS,
    PATENT_CANDIDATE_TITLES,
)
from eoip.claims.positioning_pack import generate_ontology_as_code_pack
from eoip.claims.scanner import ClaimsScanner


@pytest.fixture
def test_claims_register_path() -> Path:
    return Path("docs/claims/claims-register.yaml")


@pytest.fixture
def test_patent_register_path() -> Path:
    return Path("docs/restricted/patent-candidates.yaml")


@pytest.fixture
def real_ledger_path() -> Path:
    return Path(".audit-scratch/ledger.json")


def test_cra_041_1_claims_register_schema_and_versioning(test_claims_register_path, test_patent_register_path):
    """CRA-041.1: Maintain a versioned Claims Register in docs/claims/claims-register.yaml.
    Validates claim ID, exact wording, scope, evidence refs, owner, approval, and expiry date.
    """
    assert test_claims_register_path.exists(), "Claims register YAML file must exist"
    registry = ClaimsRegistry.load_from_yaml(test_claims_register_path, test_patent_register_path)
    assert len(registry.claims) >= 3, "Claims register must contain registered claims"

    # Verify each claim adheres strictly to typed schema
    for cid, claim in registry.claims.items():
        assert claim.id.startswith("CLM-"), f"Claim ID '{cid}' must follow naming convention"
        assert len(claim.wording) > 10, "Claim wording must be exact non-trivial statement"
        assert claim.scope.profile in ("P0", "P1", "P2", "all")
        assert claim.owner, "Claim must have an explicit owner"
        assert claim.expiry > datetime(2026, 1, 1, tzinfo=timezone.utc), "Expiry date must be valid future timestamp"
        assert claim.status in [ClaimStatus.APPROVED, ClaimStatus.DRAFT, ClaimStatus.BLOCKED]

    # Test programmatic construction, serialization, and round-trip
    new_claim = ClaimRecord(
        id="CLM-TEST-001",
        wording="Pure CPU deterministic vector indexing benchmark target achieved.",
        scope=ClaimScope(profile="P0", edition="enterprise", deployment="all"),
        evidence_refs=[EvidenceReference(kind="ledger_clause", ref_id="CRA-036.1")],
        owner="Performance Team Lead",
        approvals=[
            ClaimApproval(role="Legal", reviewer="Legal Officer", status="APPROVED"),
            ClaimApproval(role="Marketing", reviewer="Marketing Director", status="APPROVED"),
        ],
        expiry=datetime.now(timezone.utc) + timedelta(days=365),
        status=ClaimStatus.APPROVED,
    )
    assert not new_claim.is_expired()
    assert new_claim.has_approval("Legal")
    assert new_claim.has_approval("Marketing")


def test_cra_041_2_standards_conformance_claim_gating(real_ledger_path):
    """CRA-041.2: Standards-conformance claims (RDF 1.1, JSON-LD 1.1, OWL 2, SHACL Core, SPARQL 1.1, WCAG 2.2 AA)
    blocked until prerequisite requirement clauses are ACCEPTED (closes risk OR6 / Decision H-05).
    """
    # Create mock unaccepted ledger state where SHACL is OPEN
    unaccepted_ledger = {
        "items": [
            {"id": "CRA-020.1", "kind": "clause", "state": "OPEN", "receipts": []},
            {"id": "CRA-016.1", "kind": "clause", "state": "ACCEPTED", "receipts": [{"path": "fake"}]},
        ]
    }

    claim_shacl = ClaimRecord(
        id="CLM-SHACL-TEST",
        wording="Complete SHACL Core conformance validation.",
        category="standards",
        owner="Ontology Lead",
        approvals=[
            ClaimApproval(role="Legal", reviewer="Legal", status="APPROVED"),
            ClaimApproval(role="Marketing", reviewer="Marketing", status="APPROVED"),
        ],
        expiry=datetime.now(timezone.utc) + timedelta(days=365),
        status=ClaimStatus.APPROVED,
    )

    registry = ClaimsRegistry(claims=[claim_shacl])

    # 1. Blocked when CRA-020.1 is OPEN in unaccepted ledger
    publishable, reasons = registry.evaluate_claim("CLM-SHACL-TEST", ledger_data=unaccepted_ledger)
    assert not publishable, "SHACL claim must be blocked when CRA-020.1 is not ACCEPTED"
    assert any("CRA-020.1" in r and "OR6" in r for r in reasons)

    # 2. Blocked if missing Legal or Marketing approval
    claim_no_legal = claim_shacl.model_copy(update={"approvals": [ClaimApproval(role="Marketing", reviewer="M", status="APPROVED")]})
    registry.add_claim(claim_no_legal)
    publishable, reasons = registry.evaluate_claim(claim_no_legal.id, ledger_path=real_ledger_path)
    assert not publishable, "Must be blocked when missing Legal approval"
    assert any("Legal" in r for r in reasons)

    # 3. Authorized when prerequisite is ACCEPTED in real ledger and approvals exist
    registry.add_claim(claim_shacl)
    publishable, reasons = registry.evaluate_claim("CLM-SHACL-TEST", ledger_path=real_ledger_path)
    assert publishable, f"SHACL claim must pass when CRA-020.1 is ACCEPTED: {reasons}"


def test_cra_041_3_inversions_hypothesis_and_competitive_claims(real_ledger_path):
    """CRA-041.3: Inversions labelled 'already won' (I1, I3, I6, I13, I15, I16, I17) are hypotheses
    until re-verified on the pinned baseline commit with receipts; 'no competitor' requires dated review and Legal approval.
    """
    # 1. Inversion without verified receipts in ledger is blocked as a hypothesis
    inv_claim_no_receipt = ClaimRecord(
        id="CLM-INV-TEST-HYPOTHESIS",
        wording="Inversion I3: Traversal-native graph paths outperforming all competitors.",
        category="inversion",
        metadata={"inversions": ["I3"]},
        evidence_refs=[],  # No evidence
        owner="Graph Lead",
        approvals=[ClaimApproval(role="Legal", reviewer="Legal", status="APPROVED")],
        expiry=datetime.now(timezone.utc) + timedelta(days=100),
        status=ClaimStatus.APPROVED,
    )
    registry = ClaimsRegistry(claims=[inv_claim_no_receipt])
    pub, reasons = registry.evaluate_claim(inv_claim_no_receipt.id, ledger_path=real_ledger_path)
    assert not pub, "Inversion claim without evidence must be blocked as a hypothesis"
    assert any("hypothesis" in r for r in reasons)

    # 2. "No competitor has this" requires dated competitor review evidence + Legal approval
    inv_superiority_no_review = ClaimRecord(
        id="CLM-INV-SUPERIORITY",
        wording="No competitor has this native GitOps semantic diff capability.",
        category="inversion",
        metadata={"inversions": ["I15"]},
        evidence_refs=[EvidenceReference(kind="ledger_clause", ref_id="CRA-022.1")],
        owner="Lead Developer",
        approvals=[ClaimApproval(role="Marketing", reviewer="Marketing", status="APPROVED")],
        expiry=datetime.now(timezone.utc) + timedelta(days=100),
        status=ClaimStatus.APPROVED,
    )
    registry.add_claim(inv_superiority_no_review)
    pub, reasons = registry.evaluate_claim(inv_superiority_no_review.id, ledger_path=real_ledger_path)
    assert not pub, "Superiority claim without competitor review and Legal approval must be blocked"
    assert any("competitor review" in r for r in reasons)
    assert any("Legal" in r for r in reasons)

    # 3. Passing superiority claim with dated competitor review and Legal approval
    inv_superiority_valid = inv_superiority_no_review.model_copy(
        update={
            "evidence_refs": [
                EvidenceReference(kind="ledger_clause", ref_id="CRA-022.1"),
                EvidenceReference(kind="competitor_review", ref_id="CRA-042.1", notes="Dated 2026-10-18"),
            ],
            "approvals": [
                ClaimApproval(role="Legal", reviewer="Legal Counsel", status="APPROVED"),
                ClaimApproval(role="Marketing", reviewer="Marketing Lead", status="APPROVED"),
            ],
        }
    )
    registry.add_claim(inv_superiority_valid)
    pub, reasons = registry.evaluate_claim(inv_superiority_valid.id, ledger_path=real_ledger_path)
    assert pub, f"Valid superiority claim should be publishable: {reasons}"


def test_cra_041_4_ontology_as_code_positioning_pack(real_ledger_path):
    """CRA-041.4: Ontology-as-Code positioning package (ONT-012) comparison against
    TopBraid EDG, Protégé/WebProtégé, Chowlk/OnToology, published only after CRA-022 acceptance.
    """
    # 1. Blocked when CRA-022 is missing or unaccepted
    fake_ledger = {"items": [{"id": "CRA-022.1", "kind": "clause", "state": "OPEN"}]}
    blocked_pack = generate_ontology_as_code_pack(ledger_data=fake_ledger)
    assert not blocked_pack["authorized"]
    assert len(blocked_pack["reasons"]) > 0
    assert blocked_pack["content"] is None

    # 2. Authorized against real ledger where CRA-022 clauses are ACCEPTED
    valid_pack = generate_ontology_as_code_pack(ledger_path=real_ledger_path)
    assert valid_pack["authorized"], f"ONT-012 pack must be authorized: {valid_pack['reasons']}"
    content = valid_pack["content"]
    assert "Ontology-as-Code Positioning Package (ONT-012)" in content
    assert "TopBraid EDG" in content
    assert "Protégé / WebProtégé" in content
    assert "Chowlk / OnToology" in content
    assert "Current Limitations" in content
    assert "Pure CPU execution" in content


def test_cra_041_5_competitor_performance_and_tco_gating():
    """CRA-041.5: Competitor performance, TCO, pricing or revenue figures marked UNVERIFIED
    blocked from customer-facing material; requires independent verification and Legal approval.
    """
    registry = ClaimsRegistry()

    # Vendor-sourced consultancy TCO claim marked UNVERIFIED
    unverified_dp = CompetitorDataPoint(
        competitor="Palantir Foundry",
        metric="TCO",
        value="4x lower total cost of ownership",
        source="Vendor negotiation consultancy report",
        is_vendor_source=True,
        verification_status="UNVERIFIED",
        legal_approved=False,
        permitted_for_external_use=False,
    )
    authorized, reasons = registry.check_competitor_data_point(unverified_dp)
    assert not authorized, "UNVERIFIED competitor TCO figure must be blocked"
    assert any("UNVERIFIED" in r for r in reasons)
    assert any("Legal" in r for r in reasons)

    # Independently verified and legal-approved data point
    verified_dp = CompetitorDataPoint(
        competitor="Apache Jena Fuseki",
        metric="point_lookup_latency",
        value="1.8ms p95 on BSBM 100k",
        source="Independent benchmark reproduction receipt",
        is_vendor_source=False,
        verification_status="INDEPENDENTLY_VERIFIED",
        legal_approved=True,
        permitted_for_external_use=True,
    )
    authorized, reasons = registry.check_competitor_data_point(verified_dp)
    assert authorized, f"Independently verified data point must be authorized: {reasons}"


def test_cra_041_6_patent_candidate_disclosure_control(test_patent_register_path):
    """CRA-041.6: Patent-candidate disclosure control for the 5 candidates listed in OCA section 8.3;
    public disclosure blocked until a recorded Legal decision exists for each (decision H-12).
    """
    assert test_patent_register_path.exists(), "Restricted patent register must exist"
    pat_data = yaml.safe_load(test_patent_register_path.read_text(encoding="utf-8"))
    candidates = pat_data.get("patent_candidates", [])
    assert len(candidates) == 5, "Must list all 5 patent candidates from OCA section 8.3"

    titles = [c["title"] for c in candidates]
    for required_title in PATENT_CANDIDATE_TITLES:
        assert required_title in titles, f"Missing candidate: {required_title}"

    # Verify each has legal decision H-12 recorded and public disclosure is blocked
    for c in candidates:
        assert c.get("legal_decision_id") == "H-12"
        assert c.get("public_disclosure_permitted") is False, (
            f"Candidate '{c['title']}' must have public disclosure blocked pending H-12"
        )


def test_cra_041_7_indicative_scorecards_planning_aids_only():
    """CRA-041.7: Indicative scorecards (matrix CSVs, self-scores 2.9/3.6/4.2) are internal planning aids;
    external use requires evidence-qualified rescoring under CRA-042.
    """
    registry = ClaimsRegistry()

    # Internal planning aid scorecard
    sc_internal = ScorecardRecord(
        matrix_name="ontology-comparison-matrix.csv",
        self_score="2.9",
        purpose="INTERNAL_PLANNING_ONLY",
        cra_042_rescored=False,
    )
    pub, reasons = registry.check_scorecard_publication(sc_internal)
    assert not pub, "Internal scorecard must be blocked from external publication"
    assert any("INTERNAL_PLANNING_ONLY" in r for r in reasons)
    assert any("CRA-042" in r for r in reasons)

    # Valid external publication with CRA-042 rescoring and confidence
    sc_external = ScorecardRecord(
        matrix_name="certified-capability-matrix",
        self_score="4.0",
        purpose="EXTERNAL_PUBLICATION",
        cra_042_rescored=True,
        scoring_method="W3C standards test suite pass-rate",
        scoring_date="2026-10-18",
        evidence_confidence="HIGH_AUTOMATED_RECEIPTS",
    )
    pub, reasons = registry.check_scorecard_publication(sc_external)
    assert pub, f"Rescored scorecard with methodology must be permitted: {reasons}"


def test_cra_041_a_claims_scanner_ci_gate_blocks_four_cases(test_claims_register_path, test_patent_register_path):
    """CRA-041.A: Claims check CI scanner blocks the four publication attempts:
    (a) a SHACL conformance claim while CRA-020 is not ACCEPTED,
    (b) an 'already won' inversion without a receipt,
    (c) a competitor TCO figure marked UNVERIFIED,
    (d) a patent-candidate mechanism without Legal decision H-12.
    And passes on a fully evidenced claim.
    """
    registry = ClaimsRegistry.load_from_yaml(test_claims_register_path, test_patent_register_path)

    # Case A: SHACL claim when CRA-020 is not ACCEPTED in simulated ledger
    simulated_unaccepted_ledger = {
        "items": [
            {"id": "CRA-020.1", "kind": "clause", "state": "OPEN", "receipts": []},
            {"id": "CRA-016.1", "kind": "clause", "state": "ACCEPTED", "receipts": [{"path": "fake"}]},
        ]
    }
    scanner_unaccepted = ClaimsScanner(registry=registry, ledger_data=simulated_unaccepted_ledger)

    doc_case_a = "Our product guarantees full SHACL Core conformance."
    violations_a = scanner_unaccepted.scan_text(doc_case_a, "announcement.md")
    assert any(v.violation_type == "UNACCEPTED_STANDARDS_PREREQUISITE" and "CRA-020.1" in v.message for v in violations_a), (
        "Scanner must block SHACL claim when CRA-020 is unaccepted"
    )

    # Case B: 'already won' inversion without a receipt
    doc_case_b = "We have already won inversion I6: the ontology comes to data directly."
    violations_b = scanner_unaccepted.scan_text(doc_case_b, "blog.md")
    assert any(v.violation_type == "UNVERIFIED_INVERSION" for v in violations_b), (
        "Scanner must block 'already won' inversion without receipt"
    )

    # Case C: Competitor TCO figure marked UNVERIFIED
    doc_case_c = "Independent analyses claim 50% lower TCO compared to Palantir."
    violations_c = scanner_unaccepted.scan_text(doc_case_c, "pricing.md")
    assert any(v.violation_type == "UNVERIFIED_COMPETITOR_FIGURE" for v in violations_c), (
        "Scanner must block unverified competitor TCO claims"
    )

    # Case D: Patent-candidate mechanism disclosure without Legal decision H-12
    doc_case_d = "Here is our new mechanism for semver from semantic diff across graph ontologies."
    violations_d = scanner_unaccepted.scan_text(doc_case_d, "whitepaper.md")
    assert any(v.violation_type == "PATENT_DISCLOSURE_PROHIBITED" and "H-12" in v.message for v in violations_d), (
        "Scanner must block patent-candidate mechanism disclosure without H-12"
    )

    # Passing case: Fully evidenced claim tagged with approved claim ID and accepted ledger
    clean_ledger = {
        "items": [
            {"id": "CRA-016.1", "kind": "clause", "state": "ACCEPTED", "receipts": [{"path": "fake"}]},
        ]
    }
    scanner_clean = ClaimsScanner(registry=registry, ledger_data=clean_ledger)
    doc_passing = "We support standard RDF 1.1 graph data ingestion [claim: CLM-RDF-001]."
    violations_clean = scanner_clean.scan_text(doc_passing, "clean.md")
    assert len(violations_clean) == 0, f"Evidenced approved claim must produce 0 violations: {violations_clean}"
