"""Fail-closed acceptance receipts, including failed collection and skipped journeys."""

import json
from subprocess import CompletedProcess

import pytest

from scripts import verify_live_dlq


@pytest.mark.parametrize(
    ("returncode", "case_tags", "expected"),
    [
        (0, [""] * len(verify_live_dlq.EXPECTED_JOURNEYS), "PASS"),
        (1, [""] * (len(verify_live_dlq.EXPECTED_JOURNEYS) - 1) + ["<failure/>"], "FAIL"),
        (0, [""] * (len(verify_live_dlq.EXPECTED_JOURNEYS) - 1) + ["<skipped/>"], "FAIL"),
        (0, [""] * (len(verify_live_dlq.EXPECTED_JOURNEYS) - 1) + ["<error/>"], "FAIL"),
        (0, [""] * 9, "FAIL"),
        (0, [""] * 6, "FAIL"),
        (0, [""] * 3, "FAIL"),
        (2, None, "FAIL"),
    ],
)
def test_acceptance_receipt_requires_all_named_journeys(
    monkeypatch, tmp_path, returncode, case_tags, expected
):
    report = tmp_path / "results" / "acceptance.json"
    monkeypatch.setenv("EOIP_LIVE_DLQ_ACCEPTANCE", "1")
    monkeypatch.setenv("EOIP_ACCEPTANCE_REPORT", str(report))

    def run(command, *, check):
        assert check is False
        assert "tests/runtime_dlq" in command
        junit = report.with_suffix(".xml")
        assert f"--junitxml={junit}" in command
        if case_tags is not None:
            cases = "".join(
                f'<testcase name="{sorted(verify_live_dlq.EXPECTED_JOURNEYS)[index]}">{tag}</testcase>'
                for index, tag in enumerate(case_tags)
            )
            junit.write_text(f"<testsuites><testsuite>{cases}</testsuite></testsuites>")
        return CompletedProcess(command, returncode)

    monkeypatch.setattr(verify_live_dlq.subprocess, "run", run)
    if expected == "PASS":
        verify_live_dlq.main()
    else:
        with pytest.raises(SystemExit) as exc:
            verify_live_dlq.main()
        assert exc.value.code == (returncode or 1)
    result = json.loads(report.read_text())
    assert result["status"] == expected
    assert result["pytest_exit_code"] == returncode
    assert result["exit_code"] == (0 if expected == "PASS" else returncode or 1)
    assert result["junit"] == "acceptance.xml"
    if case_tags is None:
        assert result["report_error"] == "JUnit evidence unavailable: FileNotFoundError"


def test_live_acceptance_requires_explicit_opt_in(monkeypatch):
    monkeypatch.delenv("EOIP_LIVE_DLQ_ACCEPTANCE", raising=False)
    with pytest.raises(RuntimeError, match="dlq-acceptance only"):
        verify_live_dlq.main()


@pytest.mark.parametrize("duplicate", [False, True])
def test_receipt_refuses_unexpected_or_duplicate_passes(monkeypatch, tmp_path, duplicate):
    report = tmp_path / "acceptance.json"
    monkeypatch.setenv("EOIP_LIVE_DLQ_ACCEPTANCE", "1")
    monkeypatch.setenv("EOIP_ACCEPTANCE_REPORT", str(report))
    names = sorted(verify_live_dlq.EXPECTED_JOURNEYS)
    names[-1] = names[0] if duplicate else "unrelated_test"

    def run(command, *, check):
        report.with_suffix(".xml").write_text(
            "<testsuites><testsuite>"
            + "".join(f'<testcase name="{name}"/>' for name in names)
            + "</testsuite></testsuites>"
        )
        return CompletedProcess(command, 0)

    monkeypatch.setattr(verify_live_dlq.subprocess, "run", run)
    with pytest.raises(SystemExit) as exc:
        verify_live_dlq.main()
    assert exc.value.code == 1
    assert json.loads(report.read_text())["status"] == "FAIL"
