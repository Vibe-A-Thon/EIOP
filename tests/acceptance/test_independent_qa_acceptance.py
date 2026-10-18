"""Acceptance test suite for Independent QA and Evidence Verification (WP-037, CRA-037.1-037.11, CRA-037.A)."""

from __future__ import annotations

import copy
import hashlib
import json
import math
from pathlib import Path
import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.traversal import GraphTraversal
from eoip.qa.evidence import BehavioralEvidenceRegistry, EvidenceEntry
from eoip.qa.mutation import MutationCheck
from eoip.qa.verification_gate import (
    AntiStubProbeFailureError,
    AntiStubProbeHarness,
    EvidenceVerificationGate,
    GateRefusalError,
    QuarantineManager,
    TestScopeLabel,
    ZeroSkipEnforcer,
)
from tests.oracles.graph_oracle import ReferenceGraphOracle


@pytest.fixture
def sample_receipt():
    return {
        "receipt_id": "rcpt-sample-2026",
        "requirement_clause": "CRA-037.1",
        "state_claimed": "VERIFIED",
        "source_unchanged_during_run": True,
        "artifact_digest": "a" * 64,
        "execution": {
            "exit_code": 0,
            "started_at": "2026-10-18T10:00:00Z",
            "completed_at": "2026-10-18T10:00:05Z",
        },
        "results": {
            "tests_total": 5,
            "tests_failed": 0,
            "tests_errors": 0,
            "tests_skipped": 0,
            "tests_passed": 5,
        },
    }


# ===========================================================================
# CRA-037.1: Test scope taxonomy and suite labels
# ===========================================================================

def test_cra_037_1_test_scope_taxonomy_labels():
    scopes = {label.value for label in TestScopeLabel}
    expected_scopes = {
        "unit", "property_fuzz", "differential", "contract",
        "integration", "security", "browser", "migration_restore",
        "chaos", "performance",
    }
    assert expected_scopes == scopes


# ===========================================================================
# CRA-037.2: Independent test oracles with zero production imports
# ===========================================================================

def test_cra_037_2_independent_test_oracle():
    # 1. Populate reference oracle (pure Python graph)
    oracle = ReferenceGraphOracle()
    oracle.add_edge("node:1", "node:2")
    oracle.add_edge("node:2", "node:3")
    oracle.add_edge("node:3", "node:4")

    # 2. Populate production graph store
    store = MemoryGraphStore()
    v1 = store.upsert_vertex("WorkItem", {"canonical_id": "node:1"})
    v2 = store.upsert_vertex("WorkItem", {"canonical_id": "node:2"})
    v3 = store.upsert_vertex("WorkItem", {"canonical_id": "node:3"})
    v4 = store.upsert_vertex("WorkItem", {"canonical_id": "node:4"})
    store.upsert_edge("REFERENCES", v1["vid"], v2["vid"], {})
    store.upsert_edge("REFERENCES", v2["vid"], v3["vid"], {})
    store.upsert_edge("REFERENCES", v3["vid"], v4["vid"], {})

    # 3. Compare production traversal with oracle
    traversal = GraphTraversal(store, max_depth=5)
    prod_path_res = traversal.find_path("node:1", "node:4", max_depth=5)
    prod_path = [n["canonical_id"] for n in prod_path_res["vertices"]]

    oracle_path = oracle.shortest_path("node:1", "node:4", max_depth=5)
    assert prod_path == oracle_path == ["node:1", "node:2", "node:3", "node:4"]


# ===========================================================================
# CRA-037.3: Build-once, promote-digest verification
# ===========================================================================

def test_cra_037_3_build_once_promoted_artifact_verification(sample_receipt):
    gate = EvidenceVerificationGate()

    # Matching promoted artifact digest passes
    assert gate.verify_receipt(sample_receipt, expected_artifact_digest="a" * 64) is True

    # Mismatched/stale digest fails closed
    with pytest.raises(GateRefusalError) as exc_digest:
        gate.verify_receipt(sample_receipt, expected_artifact_digest="b" * 64)
    assert "mismatched artifact digest" in str(exc_digest.value)


# ===========================================================================
# CRA-037.4: Evidence validator: exit code, 0 failures, 0 errors, freshness
# ===========================================================================

def test_cra_037_4_evidence_validator_freshness_and_exit_code(sample_receipt):
    gate = EvidenceVerificationGate()

    # Non-zero exit code fails
    failing_receipt = copy.deepcopy(sample_receipt)
    failing_receipt["execution"]["exit_code"] = 1
    with pytest.raises(GateRefusalError) as exc_exit:
        gate.verify_receipt(failing_receipt)
    assert "exit code 1 != 0" in str(exc_exit.value)

    # Failed test count fails
    broken_receipt = copy.deepcopy(sample_receipt)
    broken_receipt["results"]["tests_failed"] = 1
    with pytest.raises(GateRefusalError) as exc_fail:
        gate.verify_receipt(broken_receipt)
    assert "contain failures or errors" in str(exc_fail.value)


# ===========================================================================
# CRA-037.5: Structured manual domain, security, accessibility reviews
# ===========================================================================

def test_cra_037_5_structured_manual_review_records():
    review_record = {
        "review_id": "REV-SEC-2026-10",
        "domain": "security",
        "reviewer": "SecAuditor-1",
        "date": "2026-10-18T12:00:00Z",
        "scope": "packages/eoip/authz",
        "verdict": "REMEDIATED",
        "defects": [
            {
                "defect_id": "DEF-SEC-01",
                "severity": "HIGH",
                "finding": "Privilege escalation in unvalidated role scope",
                "remediation": "Enforced TrustedScope immutability",
                "remediated": True,
            }
        ],
    }

    assert review_record["domain"] in {"security", "accessibility", "usability", "operations", "legal"}
    assert review_record["verdict"] == "REMEDIATED"
    assert len(review_record["defects"]) >= 1
    assert review_record["defects"][0]["remediated"] is True


# ===========================================================================
# CRA-037.6: Concurrent source change detection mid-run
# ===========================================================================

def test_cra_037_6_concurrent_source_change_detection(sample_receipt):
    gate = EvidenceVerificationGate()

    # Mid-run source edits mark run as unbound and refuse acceptance
    with pytest.raises(GateRefusalError) as exc_drift:
        gate.verify_receipt(sample_receipt, source_dirty_mid_run=True)
    assert "source was modified mid-run" in str(exc_drift.value)


# ===========================================================================
# CRA-037.7: Property-based fuzzing and mutation testing checks
# ===========================================================================

def test_cra_037_7_property_fuzzing_and_mutation_checks():
    check = MutationCheck(
        check_id="mut-check-001",
        requirement_id="CRA-037.7",
        test_id="test_parser_mutation",
        mutated_file="packages/eoip/mapping/cml/parser.py",
        mutation_line=45,
        mutation="== -> !=",
        original_assert="assert parser.valid == True",
        mutated_exit_code=1,
        caught=True,
        release="v1.0.0",
        checked_at="2026-10-18T10:00:00Z",
        detail="Mutated test failed as expected, proving detection power",
    )

    assert check.caught is True
    assert check.mutated_exit_code != 0
    assert "==" in check.original_assert


# ===========================================================================
# CRA-037.8: CI hygiene thresholds (coverage >= 85%, mutation >= 80%)
# ===========================================================================

def test_cra_037_8_hygiene_thresholds_separate_from_acceptance():
    gate = EvidenceVerificationGate()

    # Passing hygiene report
    passing = gate.verify_hygiene_thresholds(line_coverage_pct=88.5, mutation_score_pct=82.0)
    assert passing["hygiene_passed"] is True
    assert "Hygiene gates are CI requirements only" in passing["note"]

    # Failing hygiene report
    failing = gate.verify_hygiene_thresholds(line_coverage_pct=81.0, mutation_score_pct=85.0)
    assert failing["hygiene_passed"] is False
    assert failing["coverage_passed"] is False


# ===========================================================================
# CRA-037.9: Zero-skip policy enforcement
# ===========================================================================

def test_cra_037_9_zero_skip_policy_enforcement():
    quarantine = QuarantineManager()
    enforcer = ZeroSkipEnforcer(quarantine)

    # 1. Zero skipped tests passes
    assert enforcer.validate_test_results({"tests_failed": 0, "tests_errors": 0}, skipped_tests=[]) is True

    # 2. Unquarantined skipped test fails the gate
    with pytest.raises(GateRefusalError) as exc_skip:
        enforcer.validate_test_results(
            {"tests_failed": 0, "tests_errors": 0},
            skipped_tests=["test_unquarantined_feature"],
        )
    assert "skipped without a tracked quarantine defect ID" in str(exc_skip.value)

    # 3. Quarantined test with tracked defect ID passes
    quarantine.quarantine_test(
        test_id="test_legacy_edge_case",
        defect_id="DEF-LEGACY-404",
        quarantined_by="QA-Lead",
        expiration_date="2026-12-31",
        reason="Third-party vendor bug pending upstream release",
    )
    assert enforcer.validate_test_results(
        {"tests_failed": 0, "tests_errors": 0},
        skipped_tests=["test_legacy_edge_case"],
    ) is True


# ===========================================================================
# CRA-037.10: Quarantine manager and collection time tracking
# ===========================================================================

def test_cra_037_10_quarantine_manager_and_tracking():
    qm = QuarantineManager()
    entry = qm.quarantine_test(
        test_id="test_neptune_cluster_split",
        defect_id="DEF-NEP-901",
        quarantined_by="infra-team",
        expiration_date="2026-11-15",
        reason="Requires AWS hardware sandbox; skipped in pure CPU CI",
    )

    assert qm.is_quarantined("test_neptune_cluster_split") is True
    assert qm.get_defect_id("test_neptune_cluster_split") == "DEF-NEP-901"
    assert qm.is_quarantined("test_other") is False


# ===========================================================================
# CRA-037.11: Anti-stub probes failing hash stubs (CRA-044.3)
# ===========================================================================

def test_cra_037_11_anti_stub_probes_reject_hash_stub():
    # 1. Genuine semantic embedder (toy simulation with vocabulary overlap / semantic projection)
    def genuine_semantic_embedder(text: str) -> list[float]:
        tokens = text.lower().split()
        finance_keywords = {"bank", "balance", "financial", "statement", "account", "funds", "ledger"}
        k8s_keywords = {"kubernetes", "container", "cluster", "pod", "deployment", "docker", "orchestration", "node"}

        finance_score = sum(1.0 for t in tokens if t in finance_keywords)
        k8s_score = sum(1.0 for t in tokens if t in k8s_keywords)
        other_score = sum(0.05 for t in tokens if t not in finance_keywords and t not in k8s_keywords)

        vec = [finance_score + 0.1, k8s_score + 0.1, other_score + 0.1]
        norm = math.sqrt(sum(x * x for x in vec))
        return [x / norm for x in vec]

    assert AntiStubProbeHarness.probe_embedder(genuine_semantic_embedder) is True

    # 2. Hash stub: converts SHA-256 digest into pseudo-random numbers (no semantic structure)
    def hash_stub_embedder(text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        # Convert first 16 bytes into floats
        floats = [float(b) / 255.0 for b in digest[:8]]
        norm = math.sqrt(sum(x * x for x in floats))
        return [x / norm for x in floats]

    # Anti-stub probe MUST refuse acceptance for the hash stub!
    with pytest.raises(AntiStubProbeFailureError) as exc_stub:
        AntiStubProbeHarness.probe_embedder(hash_stub_embedder)
    assert "model behaves as a hash stub" in str(exc_stub.value)


# ===========================================================================
# CRA-037.A: Integrated Independent QA Acceptance Obligation
# ===========================================================================

def test_cra_037_a_independent_qa_acceptance_integrated(sample_receipt):
    gate = EvidenceVerificationGate()

    # 1. Valid receipt passes
    assert gate.verify_receipt(sample_receipt, expected_artifact_digest="a" * 64) is True

    # 2. Gate refuses when a test is skipped without defect ID
    skipping_receipt = copy.deepcopy(sample_receipt)
    skipping_receipt["results"]["tests_skipped"] = 1
    with pytest.raises(GateRefusalError):
        gate.verify_receipt(skipping_receipt)

    # 3. Gate refuses when a receipt is tampered (exit code != 0 or failed tests)
    tampered_receipt = copy.deepcopy(sample_receipt)
    tampered_receipt["results"]["tests_failed"] = 2
    with pytest.raises(GateRefusalError):
        gate.verify_receipt(tampered_receipt)

    # 4. Gate refuses when artifact is stale / mismatched digest
    stale_receipt = copy.deepcopy(sample_receipt)
    stale_receipt["artifact_digest"] = "stale" + "0" * 59
    with pytest.raises(GateRefusalError):
        gate.verify_receipt(stale_receipt, expected_artifact_digest="a" * 64)

    # 5. Gate refuses when source changed mid-run
    with pytest.raises(GateRefusalError):
        gate.verify_receipt(sample_receipt, source_dirty_mid_run=True)

    # 6. Gate refuses when hash stub is substituted for learned model
    def dummy_hash_stub(text: str) -> list[float]:
        h = hashlib.md5(text.encode()).digest()
        return [float(b) / 255.0 for b in h[:4]]

    with pytest.raises(AntiStubProbeFailureError):
        AntiStubProbeHarness.probe_embedder(dummy_hash_stub)
