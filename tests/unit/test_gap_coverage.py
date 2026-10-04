"""Tests for executable GAP requirement coverage.

Requirement coverage:
- GAP-CP-009
- GAP-KGCI-001
- GAP-KGCI-002
- GAP-KGCI-003
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from eoip.gaps.coverage import build_gap_coverage_report, load_gap_requirements
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

from apps.api.app import create_app


@pytest.mark.req("GAP-CP-009", "GAP-KGCI-002")
def test_gap_docs_are_loaded_as_machine_readable_contracts():
    root = Path.cwd()
    requirements = load_gap_requirements(root)
    ids = {item.requirement_id for item in requirements}

    assert "GAP-SDT-001" in ids
    assert "GAP-KGCI-001" in ids
    assert "GAP-SEC-012" in ids
    assert len(requirements) > 286

    sdt = next(item for item in requirements if item.requirement_id == "GAP-SDT-001")
    assert sdt.phase and "Phase 1" in sdt.phase
    assert sdt.priority == "P0"
    assert "Every requirement must be linkable" in sdt.description


@pytest.mark.req("GAP-KGCI-002")
def test_gap_coverage_report_distinguishes_code_and_test_evidence():
    report = build_gap_coverage_report(Path.cwd()).to_dict()
    kgci = next(item for item in report["requirements"] if item["requirement_id"] == "GAP-KGCI-002")

    assert report["total"] > 286
    assert set(report["by_status"]).issubset({"done", "partial", "planned"})
    assert kgci["status"] == "done"
    assert any(ref["path"].endswith("packages/eoip/gaps/coverage.py") for ref in kgci["implementation_refs"])
    assert any(ref["path"].endswith("tests/unit/test_gap_coverage.py") for ref in kgci["test_refs"])


@pytest.mark.req("GAP-KGCI-001", "GAP-KGCI-002", "GAP-KGCI-003")
def test_gap_coverage_cli_writes_json_and_can_fail_planned_p0(tmp_path):
    output = tmp_path / "gap-coverage.json"
    ok = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.gap_coverage",
            "--project-root",
            ".",
            "--output",
            str(output),
        ],
        check=False,
        text=True,
        capture_output=True,
    )
    assert ok.returncode == 0, ok.stderr
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["total"] > 286
    assert data["requirements"]

    gate = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.gap_coverage",
            "--project-root",
            ".",
            "--output",
            str(tmp_path / "gate.json"),
            "--fail-on-planned-p0",
        ],
        check=False,
        text=True,
        capture_output=True,
    )
    assert gate.returncode == 1


@pytest.mark.req("GAP-CP-009", "GAP-KGCI-002")
def test_gap_coverage_api_exposes_filtered_report():
    client = TestClient(create_app(MemoryGraphStore()))

    summary = client.get("/api/v1/gaps/coverage?priority=P0&status=planned&include_requirements=false")
    assert summary.status_code == 200
    assert summary.json()["requirements"] == []
    assert summary.json()["filtered_total"] >= 1

    item = client.get("/api/v1/gaps/requirements/GAP-KGCI-002")
    assert item.status_code == 200
    assert item.json()["status"] == "done"

    missing = client.get("/api/v1/gaps/requirements/GAP-NOTREAL-999")
    assert missing.status_code == 404
