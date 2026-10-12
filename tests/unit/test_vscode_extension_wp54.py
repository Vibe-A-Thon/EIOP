"""Unit tests for Phase 5 WP 5.4: VS Code Extension (10 tasks).

Requirements:
- FR-VSCODE-001: VS Code context extension (sidebar/webview showing file/symbol, Jira, commits, dependencies, docs, provenance)
- FR-VSCODE-002: VS Code trace/impact commands (eoip.path, eoip.impact)
- G2-VSC-002: Connected runtime services/deployments for current code
- G2-VSC-003: Architecture conformance findings inline/panel
- G2-VSC-004: Impacted tests for current change
- G2-VSC-005: Relevant incidents/error signatures
- G2-VSC-006: Decision/ADR rationale
- G2-VSC-007: WHY, WHAT CHANGED, IMPACT, WHERE USED quick actions
- G2-VSC-008: Bounded semantic telemetry summary; raw unrestricted telemetry disallowed
- MVP-FR-019: VS Code extension delivery and exact symbol location / range verification
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[2]
EXT_DIR = ROOT / "apps" / "vscode-extension"
PKG_JSON_PATH = EXT_DIR / "package.json"
EXT_JS_PATH = EXT_DIR / "extension.js"


@pytest.fixture(scope="module")
def pkg_data() -> dict:
    assert PKG_JSON_PATH.exists(), "package.json missing"
    return json.loads(PKG_JSON_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def ext_code() -> str:
    assert EXT_JS_PATH.exists(), "extension.js missing"
    return EXT_JS_PATH.read_text(encoding="utf-8")


@pytest.mark.req("FR-VSCODE-001")
def test_fr_vscode_001_context_extension(pkg_data: dict, ext_code: str):
    """FR-VSCODE-001: Sidebar context provider showing symbol, Jira, commits, dependencies, docs, and provenance."""
    # Context Tree view contribution
    views = pkg_data.get("contributes", {}).get("views", {}).get("explorer", [])
    view_ids = [v.get("id") for v in views]
    assert "eoip.contextView" in view_ids

    # ContextProvider implementation
    assert "class ContextProvider" in ext_code
    assert "locationFor" in ext_code
    assert "contextTree" in ext_code
    assert "Provenance and evidence" in ext_code


@pytest.mark.req("FR-VSCODE-002")
def test_fr_vscode_002_trace_impact_commands(pkg_data: dict, ext_code: str):
    """FR-VSCODE-002: VS Code trace/impact commands answer why code exists and what change affects."""
    commands = [c["command"] for c in pkg_data.get("contributes", {}).get("commands", [])]
    assert "eoip.path" in commands
    assert "eoip.impact" in commands
    assert "eoip.lineage" in commands

    # Implementation registers commands
    assert "command('eoip.path'" in ext_code
    assert "command('eoip.impact'" in ext_code
    assert "command('eoip.lineage'" in ext_code


@pytest.mark.req("G2-VSC-002")
def test_g2_vsc_002_runtime_services(pkg_data: dict, ext_code: str):
    """G2-VSC-002: Display runtime services/deployments connected to current code."""
    commands = [c["command"] for c in pkg_data.get("contributes", {}).get("commands", [])]
    assert "eoip.services" in commands
    assert "command('eoip.services'" in ext_code
    assert "RUNTIME_SERVICES" in ext_code
    assert "'Service'" in ext_code and "'Deployment'" in ext_code


@pytest.mark.req("G2-VSC-003")
def test_g2_vsc_003_architecture_conformance(pkg_data: dict, ext_code: str):
    """G2-VSC-003: Display architecture conformance findings inline/panel."""
    commands = [c["command"] for c in pkg_data.get("contributes", {}).get("commands", [])]
    assert "eoip.conformance" in commands
    assert "command('eoip.conformance'" in ext_code
    assert "ARCHITECTURE_CONFORMANCE" in ext_code
    assert "ArchitectureRule" in ext_code or "ConformanceViolation" in ext_code


@pytest.mark.req("G2-VSC-004")
def test_g2_vsc_004_impacted_tests(pkg_data: dict, ext_code: str):
    """G2-VSC-004: Display impacted tests for current change."""
    commands = [c["command"] for c in pkg_data.get("contributes", {}).get("commands", [])]
    assert "eoip.impactedTests" in commands
    assert "command('eoip.impactedTests'" in ext_code
    assert "IMPACTED_TESTS" in ext_code
    assert "TestCase" in ext_code


@pytest.mark.req("G2-VSC-005")
def test_g2_vsc_005_relevant_incidents(pkg_data: dict, ext_code: str):
    """G2-VSC-005: Display relevant incidents and error signatures."""
    commands = [c["command"] for c in pkg_data.get("contributes", {}).get("commands", [])]
    assert "eoip.incidents" in commands
    assert "command('eoip.incidents'" in ext_code
    assert "RELEVANT_INCIDENTS" in ext_code
    assert "Incident" in ext_code or "ErrorSignature" in ext_code


@pytest.mark.req("G2-VSC-006")
def test_g2_vsc_006_adr_rationale(pkg_data: dict, ext_code: str):
    """G2-VSC-006: Display decision and ADR rationale."""
    commands = [c["command"] for c in pkg_data.get("contributes", {}).get("commands", [])]
    assert "eoip.adrRationale" in commands
    assert "command('eoip.adrRationale'" in ext_code
    assert "DECISION_RATIONALE" in ext_code
    assert "ArchitectureDecisionRecord" in ext_code or "ADR" in ext_code


@pytest.mark.req("G2-VSC-007")
def test_g2_vsc_007_quick_actions(pkg_data: dict, ext_code: str):
    """G2-VSC-007: Support WHY, WHAT CHANGED, IMPACT, WHERE USED quick actions."""
    commands = [c["command"] for c in pkg_data.get("contributes", {}).get("commands", [])]
    assert "eoip.why" in commands
    assert "eoip.whatChanged" in commands
    assert "eoip.impact" in commands
    assert "eoip.whereUsed" in commands

    assert "command('eoip.why'" in ext_code
    assert "command('eoip.whatChanged'" in ext_code
    assert "command('eoip.whereUsed'" in ext_code
    assert "action: 'WHY'" in ext_code
    assert "action: 'WHAT_CHANGED'" in ext_code
    assert "action: 'WHERE_USED'" in ext_code


@pytest.mark.req("G2-VSC-008")
def test_g2_vsc_008_bounded_telemetry_semantics(pkg_data: dict, ext_code: str):
    """G2-VSC-008: Never require unrestricted raw telemetry access in editor; enforce bounded summaries."""
    commands = [c["command"] for c in pkg_data.get("contributes", {}).get("commands", [])]
    assert "eoip.telemetrySummary" in commands
    assert "command('eoip.telemetrySummary'" in ext_code
    assert "EOIP_RAW_TELEMETRY_REFUSED" in ext_code
    assert "SEMANTIC_TELEMETRY_SUMMARY" in ext_code
    assert "is_bounded: true" in ext_code


@pytest.mark.req("MVP-FR-019")
def test_mvp_fr_019_extension_delivery(pkg_data: dict, ext_code: str):
    """MVP-FR-019: VS Code extension integration and exact source range retrieval."""
    assert pkg_data.get("name") == "eoip-context"
    assert "main" in pkg_data
    assert "eoip.openSource" in [c["command"] for c in pkg_data.get("contributes", {}).get("commands", [])]
    assert "command('eoip.openSource'" in ext_code
    assert "startLine" in ext_code and "endLine" in ext_code
    assert "revealRange" in ext_code
