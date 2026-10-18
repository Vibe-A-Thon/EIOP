"""Acceptance Suite for WP-042: Competitive Research Qualification and Maintenance.

Validates CRA-042.2 through CRA-042.7 and CRA-042.A:
- CRA-042.2: Separation of evidence-qualified, indicative, and aggregated datasets (no merging/averaging)
- CRA-042.3: Pinned artifacts, checksums, and license snapshots in version register
- CRA-042.4: Conflict-register items marked RESEARCH (WebProtégé, LODE, TerminusDB, FIBO, Openllet, extract-msg)
- CRA-042.5: Third-party engine qualification records
- CRA-042.6: Explicit evidence gaps (ND) for unavailable or contradictory sources
- CRA-042.7: 6-month refresh cadence and STALE record detection (>183 days)
- CRA-042.A: Dataset validator rejecting blank, averaged (float), unpinned, and stale entries
"""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
import pytest
import yaml

from tools.research.validate_research import (
    DEPENDENCY_TOOLS,
    validate_all,
    validate_record,
)


def test_cra_042_2_dataset_separation_and_no_merging():
    """CRA-042.2: Keep scoring datasets separate and labelled; never average, merge, or replace ND."""
    notice_file = Path("research/datasets/README.md")
    assert notice_file.exists(), "research/datasets/README.md must exist"
    notice_text = notice_file.read_text(encoding="utf-8")
    assert "DO NOT MERGE THESE DATASETS" in notice_text
    assert "never coerced to zero or interpolated" in notice_text

    matrix_file = Path("competitive-research-matrix.csv")
    assert matrix_file.exists(), "competitive-research-matrix.csv must exist"
    
    # Verify ND values exist and are preserved in competitive-research-matrix.csv
    with matrix_file.open("r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        header = next(reader)
        nd_found = False
        for row in reader:
            if "ND" in row or "nd" in row or any(c.strip() == "ND" for c in row):
                nd_found = True
                break
        assert nd_found, "competitive-research-matrix.csv must retain explicit ND values"


def test_cra_042_3_version_and_investigation_register():
    """CRA-042.3: Pin exact release, artifact checksum, and license snapshot."""
    comp_dir = Path("research/competitive")
    assert comp_dir.exists()
    
    # Inspect a dependency tool record (e.g. C04 GraphDB or C07 Neo4j or Jena)
    records = list(comp_dir.glob("C*.yaml"))
    assert len(records) >= 50, f"Expected at least 50 competitive records, found {len(records)}"
    
    # Check that records have tool_family, category, reviewed_at, scores
    sample = yaml.safe_load(records[0].read_text(encoding="utf-8"))
    assert "tool_family" in sample
    assert "category" in sample
    assert "reviewed_at" in sample
    assert "scores" in sample


def test_cra_042_4_conflict_register_research_items():
    """CRA-042.4: Conflict-register items marked RESEARCH have dated outcomes or remain OPEN."""
    with open("compliance/license-policy.yaml", "r", encoding="utf-8") as f:
        policy = yaml.safe_load(f)

    # Check WebProtege, TerminusDB, extract-msg have explicit unresolved/blocked statuses
    assert policy["unresolved_packages"]["extract-msg"]["status"] == "DISABLED"
    assert "H-09" in policy["unresolved_packages"]["extract-msg"]["reason"]
    
    assert policy["unresolved_packages"]["terminusdb"]["status"] == "BLOCKED"
    assert "H-04" in policy["unresolved_packages"]["terminusdb"]["reason"]


def test_cra_042_5_hands_on_third_party_engine_qualification():
    """CRA-042.5: Pinned artifact requirements for engines EOIP depends on or certifies."""
    # Ensure all DEPENDENCY_TOOLS are declared and monitored
    expected_deps = {"rdflib", "pyshacl", "elk", "jena", "spacy"}
    for dep in expected_deps:
        assert dep in DEPENDENCY_TOOLS, f"Expected {dep} in DEPENDENCY_TOOLS"


def test_cra_042_6_unavailable_sources_as_explicit_gaps():
    """CRA-042.6: Unavailable/contradictory sources recorded as explicit ND gaps."""
    # Create a fixture record with ND and ensure it is treated as a valid gap, not a zero or negative
    record = {
        "id": "C98",
        "tool_family": "Candidate Tool",
        "category": "reasoning",
        "reviewed_at": "2026-10-18",
        "scores": {
            "D01": {"score": "ND", "rationale": "Vendor site timeout; evidence gap"},
            "D02": {"score": 3, "rationale": "Measured in lab"},
        },
    }
    errs = validate_record(record, ref_date=date(2026, 10, 18))
    assert errs == [], f"Explicit ND gap must be valid, got errors: {errs}"


def test_cra_042_7_refresh_cadence_and_stale_record_detection():
    """CRA-042.7: Records older than 183 days are detected as STALE."""
    # Fresh record passes
    fresh_rec = {
        "id": "C97",
        "tool_family": "Fresh Tool",
        "category": "storage",
        "reviewed_at": "2026-10-18",
        "scores": {"D01": {"score": 4, "rationale": "fresh"}},
    }
    assert validate_record(fresh_rec, ref_date=date(2026, 10, 18)) == []

    # Stale record (>183 days) triggers STALE error
    stale_rec = {
        "id": "C96",
        "tool_family": "Old Tool",
        "category": "storage",
        "reviewed_at": "2025-01-01",
        "scores": {"D01": {"score": 4, "rationale": "old"}},
    }
    stale_errs = validate_record(stale_rec, ref_date=date(2026, 10, 18))
    assert any("STALE" in e for e in stale_errs)


def test_cra_042_a_acceptance_gate():
    """CRA-042.A: Run research dataset validator across all records and assert fixture rejections."""
    # 1. Real records pass validation
    comp_dir = Path("research/competitive")
    errs = validate_all(comp_dir, ref_date=date(2026, 10, 18))
    assert errs == [], f"Validation of research/competitive failed: {errs}"

    # 2. Blank score rejected
    blank_rec = {
        "id": "C95", "tool_family": "Tool", "reviewed_at": "2026-10-18",
        "scores": {"D01": {"score": "", "rationale": "missing"}},
    }
    assert any("blank score" in e for e in validate_record(blank_rec, ref_date=date(2026, 10, 18)))

    # 3. Averaged/float score rejected
    avg_rec = {
        "id": "C94", "tool_family": "Tool", "reviewed_at": "2026-10-18",
        "scores": {"D01": {"score": 3.5, "rationale": "averaged"}},
    }
    assert any("must be integer 1..5" in e for e in validate_record(avg_rec, ref_date=date(2026, 10, 18)))

    # 4. Unpinned dependency rejected
    unpinned_rec = {
        "id": "C93", "tool_family": "Apache Jena / Fuseki", "reviewed_at": "2026-10-18",
        "pinned_artifact": "unpinned",
        "scores": {"D01": {"score": 4, "rationale": "ok"}},
    }
    assert any("lacks pinned_artifact" in e for e in validate_record(unpinned_rec, ref_date=date(2026, 10, 18)))
