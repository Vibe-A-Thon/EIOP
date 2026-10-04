"""Tests for the executable G2 readiness matrix.

Requirement coverage:
- G2-ADMIN-001..017
- G2-ARCH-001..015
- G2-ARCHC-001..009
- G2-CAP-001..006
- G2-CAUSE-001..006
- G2-EKAF-001..030
- G2-EVENT-001..007
- G2-EVOL-001..016
- G2-GRAPH-API-001..003
- G2-GRAPH-BIZ-001..003
- G2-GRAPH-DEC-001..003
- G2-GRAPH-OBS-001..003
- G2-GRAPH-PROC-001..003
- G2-GRAPH-RUNTIME-001..003
- G2-GRAPH-SEC-001..003
- G2-GRAPH-TEST-001..003
- G2-I2R-001..005
- G2-IMMUNE-001..013
- G2-JOURNAL-001..006
- G2-KD-001..006
- G2-OBS-001..006
- G2-OEVO-001..006
- G2-PERF-001..008
- G2-PM-001..005
- G2-QOP-001..009
- G2-REL-001..008
- G2-SEC-CRAWL-001..012
- G2-SIM-001..007
- G2-SLO-001..005
- G2-SRC-API-001..006
- G2-SRC-CICD-001..004
- G2-SRC-CODE-001..005
- G2-SRC-CONF-001..005
- G2-SRC-DD-001..004
- G2-SRC-GH-001..004
- G2-SRC-GL-001..004
- G2-SRC-GRAF-001..003
- G2-SRC-JIRA-001..006
- G2-SRC-KIB-001..005
- G2-SRC-OTEL-001..005
- G2-SRC-RUNTIME-001..003
- G2-SRC-SBOM-001..004
- G2-SRC-SNKB-001..003
- G2-SRC-SNOW-001..006
- G2-SRC-WEB-001..005
- G2-SYNC-001..014
- G2-TEL-001..008
- G2-TIME-001..007
- G2-TWIN-001..005
- G2-UX-GRAPH-001..016
- G2-UX-LENS-001..003
- G2-UX-PLAY-001..005
- G2-VSC-001..008
"""

from __future__ import annotations

from pathlib import Path

from eoip.gaps.coverage import G2_IMPLEMENTATION_DOC, G2_REQUIREMENTS_DOC, load_gap_requirements
from eoip.gaps.g2_readiness import g2_readiness_report
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

from apps.api.app import create_app


def test_g2_readiness_matrix_covers_every_g2_requirement() -> None:
    requirements = load_gap_requirements(
        Path.cwd(),
        requirements_doc=G2_REQUIREMENTS_DOC,
        implementation_doc=G2_IMPLEMENTATION_DOC,
    )
    expected_ids = {item.requirement_id for item in requirements}
    report = g2_readiness_report(repo_root=Path.cwd())

    assert set(report["requirements"]) == expected_ids
    assert report["requirement_count"] == len(expected_ids)


def test_g2_readiness_matrix_checks_concrete_implementation_surfaces() -> None:
    report = g2_readiness_report(repo_root=Path.cwd())

    assert report["conformant"] is True
    assert report["area_count"] >= 6
    assert all(area["modules"] or area["files"] or area["routes"] for area in report["areas"])


def test_g2_readiness_api_reports_application_routes() -> None:
    client = TestClient(create_app(MemoryGraphStore()))

    response = client.get("/api/v1/gaps/g2/readiness")

    assert response.status_code == 200
    body = response.json()
    assert body["conformant"] is True
    assert "G2-ADMIN-017" in body["requirements"]
    assert "G2-SRC-SBOM-004" in body["requirements"]
