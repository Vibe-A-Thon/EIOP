"""KG CI/CD pipeline implementation (requirements §30, GAP-KGCI-001..004).

Deterministic, offline pipeline. Stages (in order):

1. ``lint``               — ontology YAML syntax check (GAP-KGCI-001).
2. ``schema_validation``  — reuse ontology manifest validation (GAP-KGCI-001).
3. ``contract_checks``    — connector mapping contract checks, if available.
4. ``graph_invariants``   — run graphtest suites from a directory.
5. ``quality_gates``      — SLO checks via validation/quality.py metrics.
6. ``compatibility``      — ontology semantic diff vs installed baseline.
7. ``security``           — offline regex secret scan (no network).
8. ``migration``          — classify required migration from the same diff.
9. ``publish``            — emit versioned ontology artifact + JSON report.

Every stage returns :class:`StageResult` (pass/fail/skipped + findings);
:class:`KGCIReport` aggregates them into one machine-readable verdict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

STAGE_LINT = "lint"
STAGE_SCHEMA = "schema_validation"
STAGE_CONTRACTS = "contract_checks"
STAGE_INVARIANTS = "graph_invariants"
STAGE_QUALITY = "quality_gates"
STAGE_COMPAT = "compatibility"
STAGE_SECURITY = "security"
STAGE_MIGRATION = "migration"
STAGE_PUBLISH = "publish"

STAGE_ORDER = [
    STAGE_LINT,
    STAGE_SCHEMA,
    STAGE_CONTRACTS,
    STAGE_INVARIANTS,
    STAGE_QUALITY,
    STAGE_COMPAT,
    STAGE_SECURITY,
    STAGE_MIGRATION,
    STAGE_PUBLISH,
]

# Release-gate modes for --fail-on (§16).
FAIL_ON_ANY = "any"          # any failed stage fails the pipeline (default)
FAIL_ON_BREAKING = "breaking"  # fail only on breaking compatibility/migration
FAIL_ON_NEVER = "never"      # always exit 0 (report-only mode)
FAIL_ON_CHOICES = (FAIL_ON_ANY, FAIL_ON_BREAKING, FAIL_ON_NEVER)

# Quality SLO thresholds (release gates §16); a metric of None is N/A and
# never fails a gate (FR-VALID-003).
QUALITY_SLO_DEFAULTS: dict[str, float] = {
    "schema_compliance_min": 0.9,
    "evidence_coverage_min": 0.5,
    "provenance_coverage_min": 0.5,
    "orphan_rate_max": 0.25,
    "duplicate_rate_max": 0.1,
    "error_count_max": 0.0,
}

# Simple offline secret detectors (GAP-KGCI-003): pattern + human name.
SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private-key-block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("slack-token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b")),
    (
        "generic-secret-assignment",
        re.compile(
            r"(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"
        ),
    ),
]

# Files/extensions scanned by the security stage.
SCAN_EXTENSIONS = {".py", ".yaml", ".yml", ".json", ".toml", ".cfg", ".ini", ".md", ".txt"}
SCAN_SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules", "dist", "build", ".pytest_cache", ".ruff_cache"}

# Minimal shape expected of a connector mapping contract file.
CONTRACT_REQUIRED_KEYS = ("connector", "entity_type", "mapping")


class StageStatus(str):
    """String enum-ish statuses kept as plain constants for JSON stability."""

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class Finding(BaseModel):
    """One pipeline finding."""

    severity: str  # error | warning | info
    message: str
    subject: str = ""


class StageResult(BaseModel):
    """Outcome of a single pipeline stage (GAP-KGCI-002)."""

    stage: str
    status: str = StageStatus.PASSED
    findings: list[Finding] = Field(default_factory=list)
    details: dict[str, Any] = Field(default_factory=dict)
    duration_ms: int = 0

    @property
    def passed(self) -> bool:
        return self.status != StageStatus.FAILED


class KGCIReport(BaseModel):
    """Aggregate machine-readable pipeline report (GAP-KGCI-004)."""

    id: str
    ontology_version: str
    started_at: str
    finished_at: str = ""
    stages: list[StageResult] = Field(default_factory=list)
    fail_on: str = FAIL_ON_ANY

    @property
    def passed(self) -> bool:
        return all(s.status != StageStatus.FAILED for s in self.stages)

    @property
    def failed_stages(self) -> list[str]:
        return [s.stage for s in self.stages if s.status == StageStatus.FAILED]

    def exit_code(self) -> int:
        """0/1 per release gates §16, honouring the fail_on mode."""
        if self.fail_on == FAIL_ON_NEVER:
            return 0
        if self.fail_on == FAIL_ON_BREAKING:
            breaking = {STAGE_COMPAT, STAGE_MIGRATION}
            return 1 if any(s.stage in breaking and s.status == StageStatus.FAILED for s in self.stages) else 0
        return 0 if self.passed else 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "ontology_version": self.ontology_version,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "fail_on": self.fail_on,
            "passed": self.passed,
            "failed_stages": self.failed_stages,
            "stages": [s.model_dump() for s in self.stages],
        }


class KGCIPipeline:
    """Configurable KG CI/CD pipeline (GAP-KGCI-001..004).

    All paths are optional; stages whose inputs are absent report
    ``skipped`` rather than failing. No network access is performed.
    """

    def __init__(
        self,
        *,
        ontology_dir: str | Path | None = None,
        graphtest_dir: str | Path | None = None,
        contract_dir: str | Path | None = None,
        scan_dirs: list[str | Path] | None = None,
        baseline_manifest: str | Path | None = None,
        output_dir: str | Path | None = None,
        version: str | None = None,
        fail_on: str = FAIL_ON_ANY,
        quality_slos: dict[str, float] | None = None,
        graph_data: tuple[list[dict], list[dict], list[dict]] | None = None,
        store_factory: Callable[[], Any] | None = None,
    ) -> None:
        if fail_on not in FAIL_ON_CHOICES:
            raise ValueError(f"fail_on must be one of {FAIL_ON_CHOICES}")
        self.ontology_dir = Path(ontology_dir) if ontology_dir else None
        self.graphtest_dir = Path(graphtest_dir) if graphtest_dir else None
        self.contract_dir = Path(contract_dir) if contract_dir else None
        self.scan_dirs = [Path(d) for d in (scan_dirs or [])]
        self.baseline_manifest = Path(baseline_manifest) if baseline_manifest else None
        self.output_dir = Path(output_dir) if output_dir else None
        self.fail_on = fail_on
        self.quality_slos = {**QUALITY_SLO_DEFAULTS, **(quality_slos or {})}
        # (vertices, edges, findings) used by the quality-gate stage; empty by default.
        self.graph_data = graph_data or ([], [], [])
        self.store_factory = store_factory
        from eoip.ontology.manifest import ONTOLOGY_VERSION

        self.version = version or ONTOLOGY_VERSION

    # -- public API -------------------------------------------------------

    def run(self) -> KGCIReport:
        """Execute all stages in order and return the aggregate report."""
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        digest = hashlib.sha1(f"{stamp}:{self.version}".encode(), usedforsecurity=False).hexdigest()[:8]
        report = KGCIReport(
            id=f"urn:eoip:cicd:report:{digest}",
            ontology_version=self.version,
            started_at=datetime.now(UTC).isoformat(),
            fail_on=self.fail_on,
        )
        stage_methods = {
            STAGE_LINT: self._stage_lint,
            STAGE_SCHEMA: self._stage_schema,
            STAGE_CONTRACTS: self._stage_contracts,
            STAGE_INVARIANTS: self._stage_invariants,
            STAGE_QUALITY: self._stage_quality,
            STAGE_COMPAT: self._stage_compat,
            STAGE_SECURITY: self._stage_security,
            STAGE_MIGRATION: self._stage_migration,
            STAGE_PUBLISH: self._stage_publish,
        }
        for name in STAGE_ORDER:
            start = time.monotonic()
            result = stage_methods[name]()
            result.duration_ms = int((time.monotonic() - start) * 1000)
            report.stages.append(result)
        report.finished_at = datetime.now(UTC).isoformat()
        return report

    # -- stage implementations ---------------------------------------------

    def _stage_lint(self) -> StageResult:
        """GAP-KGCI-001: ontology YAML must parse."""
        result = StageResult(stage=STAGE_LINT)
        files = self._ontology_yaml_files()
        if not files:
            result.status = StageStatus.SKIPPED
            result.findings.append(Finding(severity="info", message="no ontology YAML files found"))
            return result
        for path in files:
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                if data is None:
                    result.findings.append(Finding(severity="warning", message="empty YAML document", subject=str(path)))
            except yaml.YAMLError as exc:
                result.status = StageStatus.FAILED
                result.findings.append(Finding(severity="error", message=f"YAML syntax error: {exc}", subject=str(path)))
        result.details["files_linted"] = len(files)
        return result

    def _stage_schema(self) -> StageResult:
        """GAP-KGCI-001: reuse ontology manifest validation."""
        result = StageResult(stage=STAGE_SCHEMA)
        from eoip.ontology.manifest import DOMAINS, EDGE_LABELS, VERTEX_LABELS, edge_endpoints_valid

        if not (VERTEX_LABELS or EDGE_LABELS):
            result.status = StageStatus.SKIPPED
            return result
        bad_domains = [
            f"vertex label {name!r} has unknown domain {spec[0]!r}"
            for name, spec in VERTEX_LABELS.items()
            if spec[0] not in DOMAINS
        ]
        unknown_endpoints = [
            label
            for label, spec in EDGE_LABELS.items()
            if not edge_endpoints_valid(label, spec[0][0], spec[1][0])  # representative pair
        ]
        for msg in bad_domains:
            result.findings.append(Finding(severity="error", message=msg, subject="ontology/manifest"))
        if unknown_endpoints:
            result.findings.append(Finding(
                severity="error",
                message=f"edge labels with undeclared endpoints: {sorted(unknown_endpoints)}",
                subject="ontology/manifest",
            ))
        if bad_domains or unknown_endpoints:
            result.status = StageStatus.FAILED
        result.details.update(
            vertex_labels=len(VERTEX_LABELS),
            edge_labels=len(EDGE_LABELS),
        )
        return result

    def _stage_contracts(self) -> StageResult:
        """GAP-KGCI-002: connector mapping contract checks (skipped if unavailable)."""
        result = StageResult(stage=STAGE_CONTRACTS)
        if not self.contract_dir or not self.contract_dir.is_dir():
            result.status = StageStatus.SKIPPED
            result.findings.append(Finding(severity="info", message="no contract directory configured"))
            return result
        files = sorted(
            p for p in self.contract_dir.rglob("*")
            if p.suffix in {".yaml", ".yml", ".json"} and p.is_file()
        )
        if not files:
            result.status = StageStatus.SKIPPED
            result.findings.append(Finding(severity="info", message="no mapping contract files found"))
            return result
        checked = 0
        for path in files:
            try:
                data = json.loads(path.read_text(encoding="utf-8")) if path.suffix == ".json" else yaml.safe_load(path.read_text(encoding="utf-8"))
            except (yaml.YAMLError, json.JSONDecodeError) as exc:
                result.status = StageStatus.FAILED
                result.findings.append(Finding(severity="error", message=f"unparseable contract: {exc}", subject=str(path)))
                continue
            if not isinstance(data, dict) or any(k not in data for k in CONTRACT_REQUIRED_KEYS):
                result.status = StageStatus.FAILED
                missing = [k for k in CONTRACT_REQUIRED_KEYS if not isinstance(data, dict) or k not in data]
                result.findings.append(Finding(severity="error", message=f"contract missing keys: {missing}", subject=str(path)))
                continue
            checked += 1
        result.details["contracts_checked"] = checked
        return result

    def _stage_invariants(self) -> StageResult:
        """Run graphtest suites from the configured directory."""
        result = StageResult(stage=STAGE_INVARIANTS)
        if not self.graphtest_dir or not self.graphtest_dir.is_dir():
            result.status = StageStatus.SKIPPED
            result.findings.append(Finding(severity="info", message="no graphtest directory configured"))
            return result
        suites = sorted(
            p for p in self.graphtest_dir.rglob("*")
            if p.suffix in {".yaml", ".yml", ".json"} and p.is_file()
        )
        if not suites:
            result.status = StageStatus.SKIPPED
            result.findings.append(Finding(severity="info", message="no graphtest suites found"))
            return result
        from eoip.graphtest.framework import run_suite_file

        store = self.store_factory() if self.store_factory else None
        total = passed = 0
        for path in suites:
            report = run_suite_file(store, str(path)) if store is not None else run_suite_file(_memory_store(), str(path))
            total += report.total
            passed += report.passed
            for r in report.results:
                if not r.passed:
                    result.findings.append(Finding(
                        severity="error",
                        message=f"{r.id}: {r.message or 'assertion failed'}",
                        subject=str(path),
                    ))
        if passed != total:
            result.status = StageStatus.FAILED
        result.details.update(suites=len(suites), assertions=total, assertions_passed=passed)
        return result

    def _stage_quality(self) -> StageResult:
        """Release gates §16: SLO checks over validation/quality.py metrics."""
        result = StageResult(stage=STAGE_QUALITY)
        from eoip.validation.quality import QualityMetrics

        vertices, edges, findings = self.graph_data
        metrics = QualityMetrics.compute(vertices, edges, findings)
        m = metrics.as_dict()
        slo = self.quality_slos

        def breach(key: str, value: float | None, op: str) -> bool:
            if value is None:
                return False  # N/A never fails (FR-VALID-003)
            return value < slo[key] if op == "min" else value > slo[key]

        checks = {
            "schema_compliance": ("schema_compliance_min", "min"),
            "evidence_coverage": ("evidence_coverage_min", "min"),
            "provenance_coverage": ("provenance_coverage_min", "min"),
            "orphan_rate": ("orphan_rate_max", "max"),
            "duplicate_rate": ("duplicate_rate_max", "max"),
        }
        for metric, (key, op) in checks.items():
            if breach(key, m[metric], op):
                result.status = StageStatus.FAILED
                result.findings.append(Finding(
                    severity="error",
                    message=f"SLO breach: {metric}={m[metric]} ({op} {slo[key]})",
                    subject="quality_gate",
                ))
        if m["error_count"] > slo["error_count_max"]:
            result.status = StageStatus.FAILED
            result.findings.append(Finding(severity="error", message=f"{m['error_count']} error-level findings", subject="quality_gate"))
        result.details["metrics"] = m
        result.details["slos"] = slo
        return result

    def _compat_diff(self) -> Any | None:
        if not self.baseline_manifest or not self.baseline_manifest.is_file():
            return None
        from eoip.ontology.gitops import current_manifest_snapshot, diff_manifests

        try:
            baseline = json.loads(self.baseline_manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return diff_manifests(baseline, current_manifest_snapshot())

    def _stage_compat(self) -> StageResult:
        """GAP-KGCI-003: ontology diff vs installed baseline; breaking = fail."""
        result = StageResult(stage=STAGE_COMPAT)
        diff = self._compat_diff()
        if diff is None:
            result.status = StageStatus.SKIPPED
            result.findings.append(Finding(severity="info", message="no baseline manifest configured"))
            return result
        result.details.update(diff.to_dict())
        for change in diff.breaking:
            result.findings.append(Finding(
                severity="error",
                message=f"breaking change: {change.change_type} on {change.subject}: {change.detail}",
                subject=change.subject,
            ))
        if not diff.safe:
            result.status = StageStatus.FAILED
        return result

    def _stage_security(self) -> StageResult:
        """GAP-KGCI-003: offline regex secret scan (no network)."""
        result = StageResult(stage=STAGE_SECURITY)
        if not self.scan_dirs:
            result.status = StageStatus.SKIPPED
            result.findings.append(Finding(severity="info", message="no scan directories configured"))
            return result
        files_scanned = 0
        for root in self.scan_dirs:
            if not root.is_dir():
                continue
            for path in sorted(root.rglob("*")):
                if not path.is_file() or path.suffix.lower() not in SCAN_EXTENSIONS:
                    continue
                if any(part in SCAN_SKIP_DIRS for part in path.parts):
                    continue
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                files_scanned += 1
                for name, pattern in SECRET_PATTERNS:
                    for match in pattern.finditer(text):
                        result.status = StageStatus.FAILED
                        result.findings.append(Finding(
                            severity="error",
                            message=f"possible secret ({name})",
                            subject=f"{path}:{text[:match.start()].count(chr(10)) + 1}",
                        ))
        result.details["files_scanned"] = files_scanned
        return result

    def _stage_migration(self) -> StageResult:
        """GAP-KGCI-003: classify required migration from the ontology diff."""
        result = StageResult(stage=STAGE_MIGRATION)
        diff = self._compat_diff()
        if diff is None:
            result.status = StageStatus.SKIPPED
            result.findings.append(Finding(severity="info", message="no baseline manifest configured"))
            return result
        counts = diff.to_dict()["counts"]
        if counts["breaking"]:
            classification = "major"
        elif counts["potentially_breaking"]:
            classification = "minor"
        elif counts["additive"]:
            classification = "patch"
        else:
            classification = "none"
        result.details.update(migration_required=classification != "none", classification=classification, counts=counts)
        result.findings.append(Finding(severity="info", message=f"migration classification: {classification}"))
        if classification == "major":
            result.status = StageStatus.FAILED
        return result

    def _stage_publish(self) -> StageResult:
        """GAP-KGCI-004: emit versioned ontology artifact + full JSON report."""
        result = StageResult(stage=STAGE_PUBLISH)
        from eoip.ontology.gitops import current_manifest_snapshot

        if self.output_dir is None:
            result.status = StageStatus.SKIPPED
            result.findings.append(Finding(severity="info", message="no output directory configured"))
            return result
        artifact = {
            "artifact_type": "urn:eoip:cicd:artifact:ontology",
            "ontology_version": self.version,
            "published_at": datetime.now(UTC).isoformat(),
            "manifest": current_manifest_snapshot(),
        }
        artifact_dir = self.output_dir / "ontology-artifacts"
        try:
            artifact_dir.mkdir(parents=True, exist_ok=True)
            (artifact_dir / f"ontology-{self.version}.json").write_text(
                json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8"
            )
        except OSError as exc:
            result.status = StageStatus.FAILED
            result.findings.append(Finding(severity="error", message=f"artifact write failed: {exc}"))
        result.details["artifact"] = str(artifact_dir / f"ontology-{self.version}.json")
        return result

    # -- helpers ----------------------------------------------------------

    def _ontology_yaml_files(self) -> list[Path]:
        if not self.ontology_dir or not self.ontology_dir.is_dir():
            return []
        return sorted(p for p in self.ontology_dir.rglob("*") if p.suffix in {".yaml", ".yml"} and p.is_file())


def _memory_store() -> Any:
    from eoip.graph.memory import MemoryGraphStore

    return MemoryGraphStore()


def run_pipeline(**kwargs: Any) -> KGCIReport:
    """One-shot convenience wrapper around :class:`KGCIPipeline`."""
    return KGCIPipeline(**kwargs).run()


def main(argv: list[str] | None = None) -> int:
    """CLI entry (GAP-KGCI-004): ``python -m packages.eoip.ci``."""
    parser = argparse.ArgumentParser(prog="eoip.ci", description=__doc__)
    parser.add_argument("--ontology-dir", default="config/ontology")
    parser.add_argument("--graphtest-dir", default=None)
    parser.add_argument("--contract-dir", default=None)
    parser.add_argument("--scan-dirs", nargs="*", default=None)
    parser.add_argument("--baseline-manifest", default=None)
    parser.add_argument("--output-dir", default=None, help="Enables the publish stage")
    parser.add_argument("--version", default=None)
    parser.add_argument("--fail-on", choices=FAIL_ON_CHOICES, default=FAIL_ON_ANY)
    parser.add_argument("--report", default=None, help="Write the full JSON report to this path")
    args = parser.parse_args(argv)

    pipeline = KGCIPipeline(
        ontology_dir=args.ontology_dir,
        graphtest_dir=args.graphtest_dir,
        contract_dir=args.contract_dir,
        scan_dirs=args.scan_dirs,
        baseline_manifest=args.baseline_manifest,
        output_dir=args.output_dir,
        version=args.version,
        fail_on=args.fail_on,
    )
    report = pipeline.run()
    payload = json.dumps(report.to_dict(), indent=2, sort_keys=True)
    print(payload)
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(payload, encoding="utf-8")
    return report.exit_code()


if __name__ == "__main__":
    sys.exit(main())
