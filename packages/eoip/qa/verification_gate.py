"""Independent QA, verification gates, anti-stub probes, and test oracle harness (WP-037 / CRA-037.1-037.11, CRA-037.A)."""

from __future__ import annotations

import copy
import hashlib
import json
import logging
import math
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any
from collections.abc import Callable

logger = logging.getLogger("eoip.qa.verification_gate")


class TestScopeLabel(str, Enum):
    __test__ = False
    UNIT = "unit"
    PROPERTY_FUZZ = "property_fuzz"
    DIFFERENTIAL = "differential"
    CONTRACT = "contract"
    INTEGRATION = "integration"
    SECURITY = "security"
    BROWSER = "browser"
    MIGRATION_RESTORE = "migration_restore"
    CHAOS = "chaos"
    PERFORMANCE = "performance"


class GateRefusalError(Exception):
    """Raised when an acceptance or verification gate refuses acceptance."""


class AntiStubProbeFailureError(GateRefusalError):
    """Raised when an anti-stub probe detects a hash stub or non-learning dummy model."""


@dataclass
class QuarantineEntry:
    test_id: str
    defect_id: str
    quarantined_by: str
    created_at: float
    expiration_date: str
    reason: str


class QuarantineManager:
    """Manages quarantined pre-existing test failures with tracked defect IDs (CRA-037.10)."""

    def __init__(self) -> None:
        self._entries: dict[str, QuarantineEntry] = {}

    def quarantine_test(
        self,
        test_id: str,
        defect_id: str,
        quarantined_by: str,
        expiration_date: str,
        reason: str,
    ) -> QuarantineEntry:
        entry = QuarantineEntry(
            test_id=test_id,
            defect_id=defect_id,
            quarantined_by=quarantined_by,
            created_at=time.time(),
            expiration_date=expiration_date,
            reason=reason,
        )
        self._entries[test_id] = entry
        return entry

    def is_quarantined(self, test_id: str) -> bool:
        return test_id in self._entries

    def get_defect_id(self, test_id: str) -> str | None:
        entry = self._entries.get(test_id)
        return entry.defect_id if entry else None


class ZeroSkipEnforcer:
    """Enforces zero-skip policy in CI runs (CRA-037.9)."""

    def __init__(self, quarantine_manager: QuarantineManager | None = None) -> None:
        self.quarantine_manager = quarantine_manager or QuarantineManager()

    def validate_test_results(self, junit_counts: dict[str, int], skipped_tests: list[str]) -> bool:
        """Validates that no required tests are skipped without an active quarantine defect ID."""
        tests_failed = junit_counts.get("tests_failed", 0)
        tests_errors = junit_counts.get("tests_errors", 0)

        if tests_failed > 0:
            raise GateRefusalError(f"Gate refused: test suite reported {tests_failed} failed tests")
        if tests_errors > 0:
            raise GateRefusalError(f"Gate refused: test suite reported {tests_errors} errors")

        for test_id in skipped_tests:
            if not self.quarantine_manager.is_quarantined(test_id):
                raise GateRefusalError(
                    f"Gate refused: test '{test_id}' was skipped without a tracked quarantine defect ID (CRA-037.9)"
                )
        return True


class AntiStubProbeHarness:
    """Probes learned model components and fails hash stubs or uniform dummy representations (CRA-037.11)."""

    # Semantic contrast pairs: high similarity synonyms vs low similarity antonyms/unrelated
    PROBE_CASES = [
        ("bank balance financial statement", "account funds ledger statement", True),
        ("bank balance financial statement", "quantum gravitational singularity physics", False),
        ("kubernetes container cluster pod deployment", "docker orchestration cluster node replica", True),
        ("kubernetes container cluster pod deployment", "french poetry renaissance romanticism literature", False),
    ]

    @classmethod
    def probe_embedder(cls, embedder_func: Callable[[str], list[float]]) -> bool:
        """Probes embedding model to verify genuine semantic discrimination. Rejects hash stubs."""
        # 1. Check for deterministic hash stubs (e.g. md5 / sha256 output hashes converted to floats)
        # Hash stubs have near-zero semantic correlation between synonyms and antonyms
        vec_base = embedder_func("bank balance financial statement")
        vec_synonym = embedder_func("account funds ledger statement")
        vec_unrelated = embedder_func("quantum gravitational singularity physics")

        def cosine_sim(a: list[float], b: list[float]) -> float:
            dot = sum(x * y for x, y in zip(a, b))
            norm_a = math.sqrt(sum(x * x for x in a))
            norm_b = math.sqrt(sum(y * y for y in b))
            if norm_a == 0 or norm_b == 0:
                return 0.0
            return dot / (norm_a * norm_b)

        sim_synonym = cosine_sim(vec_base, vec_synonym)
        sim_unrelated = cosine_sim(vec_base, vec_unrelated)

        # Genuine semantic models show significantly higher similarity for synonyms than unrelated concepts
        # Hash stubs produce random orthogonal distributions (sim ~ 0.0 for all pairs)
        if sim_synonym - sim_unrelated < 0.15:
            raise AntiStubProbeFailureError(
                f"Anti-stub probe failed: model behaves as a hash stub (synonym sim: {sim_synonym:.3f}, unrelated sim: {sim_unrelated:.3f}, delta < 0.15)"
            )

        return True


class EvidenceVerificationGate:
    """Core acceptance gate evaluating test evidence, artifact freshness, source stability and manual reviews."""

    def __init__(self) -> None:
        self.quarantine_manager = QuarantineManager()
        self.zero_skip = ZeroSkipEnforcer(self.quarantine_manager)

    def verify_receipt(
        self,
        receipt: dict[str, Any],
        expected_artifact_digest: str | None = None,
        source_dirty_mid_run: bool = False,
    ) -> bool:
        """Evaluates whether an acceptance receipt meets all non-negotiable verification invariants."""
        # 1. Source stability check (CRA-037.4, CRA-037.6)
        if source_dirty_mid_run or not receipt.get("source_unchanged_during_run", True):
            raise GateRefusalError("Gate refused: source was modified mid-run; run is unbound (CRA-037.6)")

        # 2. Exit code check
        execution = receipt.get("execution", {})
        if execution.get("exit_code") != 0:
            raise GateRefusalError(f"Gate refused: execution exit code {execution.get('exit_code')} != 0")

        # 3. Artifact freshness and digest match (CRA-037.3, CRA-037.4)
        receipt_digest = receipt.get("artifact_digest")
        if expected_artifact_digest and receipt_digest != expected_artifact_digest:
            raise GateRefusalError(
                f"Gate refused: stale or mismatched artifact digest {receipt_digest} != {expected_artifact_digest}"
            )

        # 4. Zero-skip & error validation (CRA-037.9)
        results = receipt.get("results", {})
        if results.get("tests_failed", 0) > 0 or results.get("tests_errors", 0) > 0:
            raise GateRefusalError("Gate refused: test results contain failures or errors")

        if results.get("tests_skipped", 0) > 0:
            raise GateRefusalError("Gate refused: tests were skipped in verified receipt")

        return True

    def verify_hygiene_thresholds(
        self,
        line_coverage_pct: float,
        mutation_score_pct: float,
    ) -> dict[str, Any]:
        """CI hygiene gate: coverage >= 85%, mutation >= 80% (CRA-037.8 / Decision X-18)."""
        coverage_ok = line_coverage_pct >= 85.0
        mutation_ok = mutation_score_pct >= 80.0
        all_passed = coverage_ok and mutation_ok

        return {
            "coverage_pct": line_coverage_pct,
            "mutation_score_pct": mutation_score_pct,
            "coverage_passed": coverage_ok,
            "mutation_passed": mutation_ok,
            "hygiene_passed": all_passed,
            "note": "Hygiene gates are CI requirements only; meeting them never constitutes acceptance evidence (X-18)",
        }
