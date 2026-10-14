"""Opt-in, run-scoped pytest maps and source-bound outcome receipts."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import pytest

from eoip.jobs import write_json
from eoip.verification.test_receipts import revision, seal_receipt, source_manifest


def pytest_addoption(parser):
    group = parser.getgroup("eoip-evidence")
    group.addoption("--requirements-map", help="Replace this file with this run's collected requirement map")
    group.addoption("--run-evidence", help="Write exact outcomes and tested source hashes to this JSON file")


def pytest_configure(config):
    if config.getoption("requirements_map") or config.getoption("run_evidence"):
        if getattr(config.option, "numprocesses", None):
            raise pytest.UsageError("Execution evidence currently requires a single pytest coordinator (-n 0)")
        config.pluginmanager.register(ExecutionCollector(config), "eoip-execution-evidence")


class ExecutionCollector:
    def __init__(self, config):
        self.config = config
        self.root = Path(config.rootpath)
        self.started_at = datetime.now(UTC).isoformat()
        self.selected = {}
        self.outcomes = {}
        self.collection_errors = []
        self.receipt_path = config.getoption("run_evidence")
        self.map_path = config.getoption("requirements_map")
        self.sources = source_manifest(self.root) if self.receipt_path else {}
        self.commit = revision(self.root) if self.receipt_path else None

    def pytest_collectreport(self, report):
        if report.failed:
            self.collection_errors.append(report.nodeid)

    def pytest_collection_finish(self, session):
        for item in session.items:
            ids = set()
            for name in ("req", "eoip_requirement"):
                for mark in item.iter_markers(name=name):
                    for arg in mark.args:
                        values = arg if isinstance(arg, (list, tuple)) else [arg]
                        ids.update(value.strip() for value in values if isinstance(value, str) and value.strip())
            self.selected[item.nodeid] = sorted(ids)

    def pytest_runtest_logreport(self, report):
        case = self.outcomes.setdefault(report.nodeid, {"phases": {}, "xfail": False})
        case["phases"][report.when] = report.outcome
        case["xfail"] |= hasattr(report, "wasxfail")

    @pytest.hookimpl(trylast=True)
    def pytest_sessionfinish(self, session, exitstatus):
        # An incomplete collection must not overwrite a previously useful inventory.
        if self.map_path and not self.collection_errors and int(exitstatus) not in {2, 3, 4}:
            mapping = {}
            for nodeid, requirements in sorted(self.selected.items()):
                for requirement in requirements:
                    mapping.setdefault(requirement, []).append(nodeid)
            write_json(Path(self.map_path), dict(sorted(mapping.items())), indent=2)
        if not self.receipt_path:
            return
        tests = []
        for nodeid, requirements in sorted(self.selected.items()):
            case = self.outcomes.get(nodeid, {"phases": {}, "xfail": False})
            phases = case["phases"]
            if "failed" in phases.values():
                outcome = "FAILED"
            elif case["xfail"]:
                outcome = "XFAIL"
            elif "skipped" in phases.values():
                outcome = "SKIPPED"
            elif phases == {"setup": "passed", "call": "passed", "teardown": "passed"}:
                outcome = "PASSED"
            else:
                outcome = "NOT_EXECUTED"
            tests.append({"nodeid": nodeid, "requirements": requirements, "phases": phases, "outcome": outcome})
        counts = Counter(case["outcome"].lower() for case in tests)
        receipt = {"schema_version": "cp-test-run-v1", "started_at": self.started_at,
                   "finished_at": datetime.now(UTC).isoformat(), "code_commit": self.commit,
                   "arguments": list(self.config.invocation_params.args), "exit_code": int(exitstatus),
                   "collect_only": self.config.option.collectonly, "collection_errors": self.collection_errors,
                   "selected_node_ids": sorted(self.selected), "source_manifest": self.sources,
                   "source_unchanged": self.sources == source_manifest(self.root), "tests": tests,
                   "counts": {"collected": len(self.selected), **dict(sorted(counts.items()))},
                   "application_completion_percent": None,
                   "limitations": ["Selected tests only; passing does not certify all acceptance clauses or live infrastructure",
                                   "Local hashes establish integrity, not independent CI attestation"]}
        write_json(Path(self.receipt_path), seal_receipt(receipt))
