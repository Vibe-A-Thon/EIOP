from __future__ import annotations

import json
import subprocess

import pytest
from eoip.verification.behavioral_gate import (
    BehavioralGate,
    RiskProfile,
    VerdictStatus,
    main,
    verdict_to_report,
)


@pytest.mark.req("KGR-G-011")
def test_behavioral_gate_fails_public_signature_break() -> None:
    before = {"packages/eoip/query/operators.py": "def plan(query: str) -> str:\n    return query\n"}
    after = {"packages/eoip/query/operators.py": "def plan(query: str, limit: int) -> str:\n    return query\n"}

    verdict = BehavioralGate(risk_profile=RiskProfile.R1).verify_files(before, after)

    assert verdict.status == VerdictStatus.FAIL
    assert verdict.breaking_changes == 1
    assert verdict.diffs[0].change_type == "signature_changed"
    assert verdict.diffs[0].scope == "public"


@pytest.mark.req("KGR-G-011")
def test_behavioral_gate_supports_r0_and_r1_blocking_thresholds() -> None:
    before = {
        "packages/eoip/query/internal.py": (
            "class Planner:\n"
            "    @staticmethod\n"
            "    def shape(value: int) -> int:\n"
            "        return value\n"
        )
    }
    after = {
        "packages/eoip/query/internal.py": (
            "class Planner:\n"
            "    @staticmethod\n"
            "    def shape(value: int, scale: int) -> int:\n"
            "        return value\n"
        )
    }

    r1 = BehavioralGate(risk_profile=RiskProfile.R1).verify_files(before, after)
    r0 = BehavioralGate(risk_profile=RiskProfile.R0).verify_files(before, after)

    assert r1.status == VerdictStatus.FAIL
    assert r0.status == VerdictStatus.PASS


@pytest.mark.req("KGR-G-011")
def test_behavioral_gate_detects_observable_pure_function_change() -> None:
    before = {"packages/eoip/ingestion/normalize.py": "def normalize(value: int) -> int:\n    return value + 1\n"}
    after = {"packages/eoip/ingestion/normalize.py": "def normalize(value: int) -> int:\n    return value + 2\n"}

    verdict = BehavioralGate().verify_files(before, after)

    assert verdict.status == VerdictStatus.FAIL
    assert any(diff.change_type == "behavior_changed" for diff in verdict.diffs)
    assert any(check.status == VerdictStatus.FAIL for check in verdict.property_checks)


@pytest.mark.req("KGR-G-011")
def test_behavioral_gate_abstains_with_unverified_symbols_and_coverage() -> None:
    before = {
        "packages/eoip/ontology/rules.py": (
            "def check(value: CustomOntologyContract) -> CustomOntologyContract:\n"
            "    return value\n"
        )
    }
    after = before.copy()

    verdict = BehavioralGate().verify_files(before, after)
    report = verdict_to_report(verdict, commit_sha="a" * 40, base_sha="b" * 40, duration_ms=1.5)

    assert verdict.status == VerdictStatus.ABSTAIN
    assert verdict.unverified_symbols == ["check"]
    assert verdict.coverage_percent == 0.0
    assert report["decision"] == "ABSTAIN"
    assert report["metadata"]["unverified_symbols"] == ["check"]
    assert report["metadata"]["coverage_percent"] == 0.0
    assert "unsupported_property_signature" in report["abstain_reason"]


@pytest.mark.req("KGR-G-011")
def test_behavioral_gate_cli_writes_ci_report_for_git_diff(tmp_path, monkeypatch) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    package_path = repo / "packages" / "eoip" / "query"
    package_path.mkdir(parents=True)
    target = package_path / "planner.py"
    target.write_text("def plan(value: int) -> int:\n    return value + 1\n", encoding="utf-8")

    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "base"], cwd=repo, check=True, capture_output=True)
    base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()

    target.write_text("def plan(value: int) -> int:\n    return value + 2\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "change"], cwd=repo, check=True, capture_output=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()
    output = repo / "test-results" / "behavioral-gate.json"

    monkeypatch.chdir(repo)
    code = main([
        "--repo-root", str(repo),
        "--base-ref", base,
        "--head-ref", head,
        "--output", str(output),
        "--risk-profile", "R1",
    ])

    assert code == 1
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["decision"] == "FAIL"
    assert report["metadata"]["requirement_id"] == "KGR-G-011"
    assert report["breaking_changes"][0]["change_type"] == "BEHAVIOR_CHANGED"
