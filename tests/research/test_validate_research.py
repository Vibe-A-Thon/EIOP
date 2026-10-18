"""Unit tests for research validation rules per CRA-042.A."""
from __future__ import annotations
from datetime import date
import pytest
from tools.research.validate_research import validate_record, validate_all

@pytest.fixture
def base_record():
    return {
        "id": "C99",
        "tool_family": "Custom Tool",
        "category": "authoring",
        "reviewed_at": "2026-10-18",
        "pinned_artifact": "v1.0.0",
        "scores": {
            "D01": {"score": 4, "rationale": "documented"},
            "D02": {"score": "ND", "rationale": "gap"},
        },
    }

def test_valid_record_passes(base_record):
    errors = validate_record(base_record, ref_date=date(2026, 10, 18))
    assert errors == []

def test_blank_score_rejected(base_record):
    base_record["scores"]["D01"]["score"] = ""
    errors = validate_record(base_record, ref_date=date(2026, 10, 18))
    assert any("blank score" in e for e in errors)

def test_averaged_score_rejected(base_record):
    # Float scores like 3.5 are forbidden per CRA-042.A
    base_record["scores"]["D01"]["score"] = 3.5
    errors = validate_record(base_record, ref_date=date(2026, 10, 18))
    assert any("must be integer 1..5" in e for e in errors)

def test_unpinned_dependency_rejected(base_record):
    base_record["tool_family"] = "Apache Jena / Fuseki"
    base_record["pinned_artifact"] = "unpinned"
    errors = validate_record(base_record, ref_date=date(2026, 10, 18))
    assert any("lacks pinned_artifact" in e for e in errors)

def test_missing_reviewed_date_rejected(base_record):
    base_record["reviewed_at"] = None
    errors = validate_record(base_record, ref_date=date(2026, 10, 18))
    assert any("missing required 'reviewed_at'" in e for e in errors)

def test_stale_record_rejected(base_record):
    # More than 183 days ago from ref_date
    base_record["reviewed_at"] = "2026-01-01"
    errors = validate_record(base_record, ref_date=date(2026, 10, 18))
    assert any("STALE" in e for e in errors)
