"""Tests for executable GAP requirement coverage.

Requirement coverage:
- GAP-CP-009
- GAP-KGCI-001
- GAP-KGCI-002
- GAP-KGCI-003
- G2-ARCH-001..015
- G2-OBS-001..006
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from eoip.gaps.g2_architecture import evaluate_g2_architecture_guardrails
from eoip.gaps.g2_observability import (
    g2_observability_contract,
    validate_g2_observability_snapshot,
)
from eoip.gaps.coverage import (
    G2_IMPLEMENTATION_DOC,
    G2_REQUIREMENTS_DOC,
    build_gap_coverage_report,
    load_gap_requirements,
)
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


@pytest.mark.req("GAP-CP-009", "GAP-KGCI-002")
def test_g2_docs_are_loaded_from_heading_requirements():
    root = Path.cwd()
    requirements = load_gap_requirements(
        root,
        requirements_doc=G2_REQUIREMENTS_DOC,
        implementation_doc=G2_IMPLEMENTATION_DOC,
    )
    ids = {item.requirement_id for item in requirements}

    assert "G2-ARCH-001" in ids
    assert "G2-SRC-JIRA-006" in ids
    assert "G2-UX-GRAPH-016" in ids
    assert len(requirements) > 250

    arch = next(item for item in requirements if item.requirement_id == "G2-ARCH-001")
    assert "One acquisition contract" in arch.description
    assert arch.source_path.endswith("gaps2-requirements.md")


@pytest.mark.req("GAP-KGCI-002")
def test_gap_coverage_report_distinguishes_code_and_test_evidence():
    report = build_gap_coverage_report(Path.cwd()).to_dict()
    kgci = next(item for item in report["requirements"] if item["requirement_id"] == "GAP-KGCI-002")

    assert report["total"] > 286
    assert set(report["by_status"]).issubset({"done", "partial", "planned"})
    assert kgci["status"] == "done"
    assert any(ref["path"].endswith("packages/eoip/gaps/coverage.py") for ref in kgci["implementation_refs"])
    assert any(ref["path"].endswith("tests/unit/test_gap_coverage.py") for ref in kgci["test_refs"])


@pytest.mark.req("GAP-KGCI-002")
def test_g2_coverage_report_uses_selected_document_set():
    report = build_gap_coverage_report(
        Path.cwd(),
        requirements_doc=G2_REQUIREMENTS_DOC,
        implementation_doc=G2_IMPLEMENTATION_DOC,
    ).to_dict()
    ids = {item["requirement_id"] for item in report["requirements"]}

    assert report["total"] > 250
    assert "G2-QOP-003" in ids
    assert "GAP-SDT-001" not in ids


@pytest.mark.req("G2-ARCH-001", "G2-ARCH-015")
def test_g2_architecture_guardrails_are_executable():
    report = evaluate_g2_architecture_guardrails()

    assert report["conformant"] is True
    assert report["total"] == 15
    assert {item["requirement_id"] for item in report["results"]} >= {
        "G2-ARCH-001",
        "G2-ARCH-010",
        "G2-ARCH-015",
    }


@pytest.mark.req("G2-ARCH-006", "G2-ARCH-011")
def test_g2_architecture_guardrails_report_profile_violations():
    report = evaluate_g2_architecture_guardrails({
        "raw_telemetry_in_graph": True,
        "local_models_required": True,
    })
    failed = {item["requirement_id"] for item in report["results"] if not item["passed"]}

    assert report["conformant"] is False
    assert {"G2-ARCH-006", "G2-ARCH-011"} <= failed


@pytest.mark.req("G2-OBS-001", "G2-OBS-006")
def test_g2_observability_contract_validates_required_metrics():
    contract = g2_observability_contract()
    snapshot = {
        "source_trace": {"fetch_to_source_event_to_mapping_to_mutation": ["fetch", "source_event", "mapping", "mutation"]},
        "per_source": {
            "fetch_latency_seconds": {"jira-prod": 0.2},
            "records_per_second": {"jira-prod": 12.0},
            "errors_total": {"jira-prod": 0},
            "lag_seconds": {"jira-prod": 3.0},
            "retries_total": {"jira-prod": 1},
            "dlq_count": {"jira-prod": 0},
        },
        "graph_evolution": {
            "added_facts": 3,
            "changed_facts": 2,
            "expired_facts": 1,
            "mutation_latency_seconds": 0.04,
            "validation_failures": 0,
        },
        "event_bus": {"consumer_lag": {"quality": 0}},
        "graph_version": {"publication_time": "2026-10-05T00:00:00Z"},
        "knowledge_slo": {"evaluation_latency_seconds": 0.01},
    }
    report = validate_g2_observability_snapshot(snapshot)

    assert set(contract["requirements"]) == {
        "G2-OBS-001",
        "G2-OBS-002",
        "G2-OBS-003",
        "G2-OBS-004",
        "G2-OBS-005",
        "G2-OBS-006",
    }
    assert report["conformant"] is True


@pytest.mark.req("G2-OBS-002", "G2-OBS-004")
def test_g2_observability_contract_reports_missing_metrics():
    report = validate_g2_observability_snapshot({"per_source": {"errors_total": {"jira-prod": 1}}})
    failed_paths = {item["path"] for item in report["results"] if not item["passed"]}

    assert report["conformant"] is False
    assert "per_source.dlq_count" in failed_paths
    assert "event_bus.consumer_lag" in failed_paths


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
            "--doc-set",
            "g2",
        ],
        check=False,
        text=True,
        capture_output=True,
    )
    assert ok.returncode == 0, ok.stderr
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["doc_set"] == "g2"
    assert data["total"] > 250
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

    g2_summary = client.get("/api/v1/gaps/coverage?doc_set=g2&include_requirements=false")
    assert g2_summary.status_code == 200
    assert g2_summary.json()["doc_set"] == "g2"
    assert g2_summary.json()["total"] > 250

    g2_item = client.get("/api/v1/gaps/requirements/G2-ARCH-001?doc_set=g2")
    assert g2_item.status_code == 200
    assert "One acquisition contract" in g2_item.json()["description"]

    guardrails = client.get("/api/v1/gaps/g2/architecture-guardrails")
    assert guardrails.status_code == 200
    assert guardrails.json()["conformant"] is True

    violation = client.post(
        "/api/v1/gaps/g2/architecture-guardrails",
        json={"profile": {"direct_graph_writes_for_sources": True}},
    )
    assert violation.status_code == 200
    assert violation.json()["conformant"] is False

    obs_contract = client.get("/api/v1/gaps/g2/observability-contract")
    assert obs_contract.status_code == 200
    assert "G2-OBS-006" in obs_contract.json()["requirements"]

    obs_violation = client.post(
        "/api/v1/gaps/g2/observability-contract",
        json={"snapshot": {"per_source": {"errors_total": {"jira-prod": 1}}}},
    )
    assert obs_violation.status_code == 200
    assert obs_violation.json()["conformant"] is False

    missing = client.get("/api/v1/gaps/requirements/GAP-NOTREAL-999")
    assert missing.status_code == 404
