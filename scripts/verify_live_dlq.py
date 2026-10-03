"""Run opt-in live replay journeys and persist a machine-readable verdict."""

import json
import os
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree

from eoip.jobs import write_json

EXPECTED_JOURNEYS = {
    "test_worker_rejection_and_replay_remain_partial",
    "test_mapper_recovery_replays_immutable_capture_idempotently",
    "test_replay_refusals_do_not_enqueue_jobs",
    "test_registered_v2_invalid_replay_remains_partial",
    "test_registered_v2_mapper_recovery_is_persistent_and_idempotent",
    "test_registered_v2_registry_refusals_enqueue_nothing",
    "test_servicenow_http_baseline_incremental_and_replay",
    "test_servicenow_fetched_rejection_and_admission_controls",
    "test_servicenow_upstream_authentication_failure_is_persistent",
}


def main():
    if os.getenv("EOIP_LIVE_DLQ_ACCEPTANCE") != "1":
        raise RuntimeError("Run through scripts/docker.ps1 dlq-acceptance only")
    report = Path(os.environ["EOIP_ACCEPTANCE_REPORT"])
    report.parent.mkdir(parents=True, exist_ok=True)
    junit = report.with_suffix(".xml")
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/runtime_dlq", "-q", f"--junitxml={junit}"],
        check=False,
    )
    report_error = None
    try:
        suites = ElementTree.parse(junit).getroot()
        cases = list(suites.iter("testcase"))
    except (OSError, ElementTree.ParseError) as exc:
        cases = []
        report_error = f"JUnit evidence unavailable: {type(exc).__name__}"
    failures = sum(case.find("failure") is not None for case in cases)
    errors = sum(case.find("error") is not None for case in cases)
    skipped = sum(case.find("skipped") is not None for case in cases)
    passed = len(cases) - failures - errors - skipped
    journeys = [case.attrib.get("name", "") for case in cases]
    success = (
        completed.returncode == 0
        and passed == len(EXPECTED_JOURNEYS)
        and set(journeys) == EXPECTED_JOURNEYS
        and not (failures or errors or skipped or report_error)
    )
    gate_exit_code = 0 if success else completed.returncode or 1
    result = {
        "status": "PASS" if success else "FAIL",
        "exit_code": gate_exit_code,
        "pytest_exit_code": completed.returncode,
        "passed": passed, "failed": failures, "errors": errors, "skipped": skipped,
        "journeys": journeys,
        "junit": junit.name,
        "report_error": report_error,
        "infra": "isolated HugeGraph 1.7.0 + real HTTP API + independent durable worker",
        "scope": "Jira v1 and Confluence v2 replay; ServiceNow fixture HTTP acquisition, replay and admission",
        "excluded": ["live upstream tenants", "other registered adapters", "browser UI", "worker crash recovery"],
    }
    write_json(report, result)
    print(json.dumps(result, indent=2), flush=True)
    if not success:
        raise SystemExit(gate_exit_code)


if __name__ == "__main__":
    main()
