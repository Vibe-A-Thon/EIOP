"""Status dashboard with three separate numbers (SR-QA-012).

SR-QA-012: dashboards MUST report, as three separate numbers:

1. tests passing,
2. requirements with behavioral evidence (explicit registry entries),
3. requirements with external-gate evidence (e.g. external attestations,
   pen tests, vendor certifications — recorded via :class:`ExternalGateRecord`).

A single "% complete" number is prohibited: the three axes measure different
things and averaging them recreates the exact gaming vulnerability the
``eoip.gaps.coverage`` string-matcher gate exhibited.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass
class TestRunSummary:
    """Structured result of one test run (input to the dashboard)."""

    run_id: str
    tests_total: int
    tests_passed: int
    recorded_at: str = ""

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "tests_total": self.tests_total,
            "tests_passed": self.tests_passed,
            "recorded_at": self.recorded_at,
        }


@dataclass
class ExternalGateRecord:
    """Evidence that an external gate (audit, pen test, certification) passed."""

    gate_id: str
    requirement_id: str
    gate_kind: str = "external"  # e.g. "audit", "pentest", "certification", "sbom"
    status: str = "passed"
    evidence_ref: str = ""
    recorded_at: str = ""

    def to_dict(self) -> dict:
        return {
            "gate_id": self.gate_id,
            "requirement_id": self.requirement_id,
            "gate_kind": self.gate_kind,
            "status": self.status,
            "evidence_ref": self.evidence_ref,
            "recorded_at": self.recorded_at,
        }


class StatusDashboard:
    """Produces the three mandated numbers; never a single "% complete".

    Combines the behavioral evidence registry (SR-QA-010), the mutation check
    store (SR-QA-011) and external gate records into one report where the
    three headline numbers stay separate (SR-QA-012).
    """

    def __init__(self, evidence_registry, mutation_store=None, path: str | Path | None = None) -> None:
        self._registry = evidence_registry
        self._mutation = mutation_store
        self._lock = threading.RLock()
        self._path = Path(path) if path else Path(
            os.getenv("EOIP_DATA_DIR", ".data")
        ) / "state" / "qa-external-gates.json"
        self._gates: dict[str, ExternalGateRecord] = {}
        self._runs: dict[str, TestRunSummary] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            return
        data = json.loads(self._path.read_text(encoding="utf-8"))
        for item in data.get("gates", []):
            gate = ExternalGateRecord(**item)
            self._gates[gate.gate_id] = gate
        for item in data.get("test_runs", []):
            run = TestRunSummary(**item)
            self._runs[run.run_id] = run

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "gates": [g.to_dict() for g in sorted(self._gates.values(), key=lambda g: g.gate_id)],
            "test_runs": [r.to_dict() for r in sorted(self._runs.values(), key=lambda r: r.run_id)],
        }
        self._path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def record_test_run(self, run: TestRunSummary) -> TestRunSummary:
        with self._lock:
            if not run.recorded_at:
                run.recorded_at = datetime.now(UTC).isoformat()
            self._runs[run.run_id] = run
            self._save()
            return run

    def record_external_gate(self, gate: ExternalGateRecord) -> ExternalGateRecord:
        with self._lock:
            if not gate.recorded_at:
                gate.recorded_at = datetime.now(UTC).isoformat()
            self._gates[gate.gate_id] = gate
            self._save()
            return gate

    def external_gates(self) -> list[ExternalGateRecord]:
        with self._lock:
            return sorted(self._gates.values(), key=lambda g: g.gate_id)

    def report(self, requirement_ids: list[str] | None = None) -> dict:
        """Three separate numbers — never a single percentage (SR-QA-012)."""
        coverage = self._registry.coverage_report(requirement_ids)
        behavioral_ids = {
            r["requirement_id"] for r in coverage["requirements"] if r["covered"]
        }
        gates = self.external_gates()
        external_ids = {g.requirement_id for g in gates if g.status == "passed"}
        latest_run = max(self._runs.values(), key=lambda r: r.recorded_at, default=None)
        mutation_summary = None
        if self._mutation is not None:
            checks = self._mutation.all_checks()
            mutation_summary = {
                "total": len(checks),
                "caught": sum(1 for c in checks if c.caught),
                "missed": sum(1 for c in checks if not c.caught),
            }
        return {
            # --- the three mandated numbers, reported separately ---
            "tests_passing": {
                "latest_run": latest_run.to_dict() if latest_run else None,
                "count": latest_run.tests_passed if latest_run else 0,
            },
            "requirements_with_behavioral_evidence": {
                "count": len(behavioral_ids),
                "requirement_ids": sorted(behavioral_ids),
            },
            "requirements_with_external_gate_evidence": {
                "count": len(external_ids),
                "requirement_ids": sorted(external_ids),
            },
            # SR-QA-012: intentionally NO "percent_complete" key. A single
            # merged number is prohibited; consumers must look at each axis.
            "coverage": coverage,
            "mutation_checks": mutation_summary,
            "definition_of_done": [
                "tests passing (latest recorded run)",
                "behavioral evidence: explicit registry entry per requirement (SR-QA-010)",
                "mutation check caught per requirement, sampled per release (SR-QA-011)",
                "external gate evidence where the requirement depends on one (SR-QA-012)",
            ],
        }
