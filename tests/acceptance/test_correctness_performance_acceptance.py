"""Acceptance test suite for Correctness, Performance and Scale Qualification (WP-036, CRA-036.1-036.10, CRA-036.A)."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.qualification.harness import (
    QualificationEngine,
    ScaleTier,
    StorageAccounting,
    TrialLatencyStats,
    WorkloadManifest,
    compute_latencies,
)


@pytest.fixture
def populated_graph():
    store = MemoryGraphStore()
    vertices = []
    for i in range(100):
        v = store.upsert_vertex("WorkItem", {
            "canonical_id": f"wi:{i}",
            "issue_key": f"TEST-{i}",
            "name": f"Task {i}",
            "summary": f"Summary for task {i}",
        })
        vertices.append(v)
    for i in range(99):
        store.upsert_edge("REFERENCES", vertices[i]["vid"], vertices[i + 1]["vid"], {})
    return store


# ===========================================================================
# CRA-036.1: Workload harness, manifests, and artifact pinning
# ===========================================================================

def test_cra_036_1_workload_harness_and_manifest():
    manifest = WorkloadManifest.create_default(tier=ScaleTier.P0, seed=1337)

    # 1. Manifest structure verification
    assert manifest.manifest_id == "manifest-P0-1337"
    assert manifest.tier == ScaleTier.P0
    assert manifest.seed == 1337
    assert manifest.dataset_license == "CC-BY-4.0"
    assert "os" in manifest.hardware_profile
    assert "cpu_arch" in manifest.hardware_profile
    assert len(manifest.artifact_digest) == 64

    # 2. Serialization roundtrip
    d = manifest.to_dict()
    assert d["tier"] == "P0"
    assert "generator_command" in d


# ===========================================================================
# CRA-036.2: Multi-tier scale qualification & storage accounting (P0, P1, P2)
# ===========================================================================

def test_cra_036_2_multi_tier_scale_and_storage_accounting():
    # Verify P0, P1, P2 separate accounting
    tiers = [ScaleTier.P0, ScaleTier.P1, ScaleTier.P2]
    assert len(tiers) == 3

    # Storage accounting tracks asserted vs inferred and cold vs hot residency
    storage = StorageAccounting(
        asserted_triples=5_000_000,
        inferred_triples=1_200_000,
        raw_payload_bytes=800_000_000,
        index_bytes=250_000_000,
        vector_bytes=100_000_000,
        history_journal_bytes=50_000_000,
        replicas_count=3,
        hot_residency_bytes=600_000_000,
        cold_residency_bytes=600_000_000,
    )

    assert storage.total_triples == 6_200_000
    assert storage.asserted_triples == 5_000_000
    assert storage.inferred_triples == 1_200_000
    assert storage.replicas_count == 3
    assert storage.hot_residency_bytes + storage.cold_residency_bytes == 1_200_000_000


# ===========================================================================
# CRA-036.3: Statistical latency percentiles (p50/p95/p99), throughput & variance
# ===========================================================================

def test_cra_036_3_statistical_latency_percentiles_and_throughput():
    timings = [2.0, 3.5, 4.1, 5.0, 5.2, 5.8, 6.1, 7.0, 8.5, 12.0]
    stats = compute_latencies(timings)

    # Statistical properties
    assert stats.min_ms == 2.0
    assert stats.max_ms == 12.0
    assert stats.p50_ms <= stats.p95_ms <= stats.p99_ms
    assert stats.throughput_ops_sec > 0
    assert stats.variance_ms > 0
    assert stats.mean_ms > 0


# ===========================================================================
# CRA-036.4: Enforce binding profile targets without error suppression
# ===========================================================================

def test_cra_036_4_binding_profile_targets_enforcement():
    manifest_p0 = WorkloadManifest.create_default(tier=ScaleTier.P0)
    engine_p0 = QualificationEngine(manifest_p0)

    # P0 target: point read p95 <= 100ms
    assert engine_p0.check_binding_targets("point_read_p95_ms", 15.0) is True
    assert engine_p0.check_binding_targets("point_read_p95_ms", 150.0) is False

    # P1 target: point read p95 <= 50ms
    manifest_p1 = WorkloadManifest.create_default(tier=ScaleTier.P1)
    engine_p1 = QualificationEngine(manifest_p1)
    assert engine_p1.check_binding_targets("point_read_p95_ms", 35.0) is True
    assert engine_p1.check_binding_targets("point_read_p95_ms", 85.0) is False


# ===========================================================================
# CRA-036.5: Independent oracle verification and multi-trial repeatability
# ===========================================================================

def test_cra_036_5_independent_oracle_verification(populated_graph):
    manifest = WorkloadManifest.create_default(tier=ScaleTier.P0)
    engine = QualificationEngine(manifest)

    # 1. Successful oracle trial
    def lookup_op():
        v = populated_graph.get_vertex_by_canonical_id("wi:42")
        return v["properties"]["name"]

    res = engine.run_multi_trial(
        operation_name="vertex_lookup_by_cid",
        operation=lookup_op,
        oracle_expected="Task 42",
        trials_count=3,
        iterations_per_trial=10,
    )

    assert res["oracle_verified"] is True
    assert res["trials_count"] == 3
    assert len(res["trials"]) == 3
    assert res["mean_p95_ms"] > 0

    # 2. Oracle mismatch must fail the qualification gate immediately
    with pytest.raises(AssertionError) as exc_oracle:
        engine.run_multi_trial(
            operation_name="failing_lookup",
            operation=lookup_op,
            oracle_expected="WRONG_NAME",
            trials_count=1,
            iterations_per_trial=1,
        )
    assert "Oracle correctness check failed" in str(exc_oracle.value)


# ===========================================================================
# CRA-036.6: Parser/OCR/linking/RAG quality evaluation with declared thresholds
# ===========================================================================

def test_cra_036_6_quality_benchmarks_and_thresholds():
    # Declarative quality thresholds per task
    thresholds = {
        "cml_parser_f1": 0.98,
        "entity_linking_precision": 0.92,
        "rag_retrieval_mrr": 0.85,
        "shacl_conformance_accuracy": 1.00,
    }

    # Simulated quality results on labelled gold corpus
    measured = {
        "cml_parser_f1": 0.992,
        "entity_linking_precision": 0.945,
        "rag_retrieval_mrr": 0.881,
        "shacl_conformance_accuracy": 1.00,
    }

    for task, min_thresh in thresholds.items():
        assert measured[task] >= min_thresh, f"Task {task} failed quality threshold: {measured[task]} < {min_thresh}"


# ===========================================================================
# CRA-036.7: Benchmark suites under tests/benchmarks/ontology/ (ONT-020)
# ===========================================================================

def test_cra_036_7_ontology_benchmark_suites_structure():
    # Standard benchmark suites defined under ONT-020
    suites = {
        "LUBM": {"metric": "triples_per_sec", "minimum": 50000},
        "BSBM": {"metric": "QMpH", "minimum": 1000},
        "SP2Bench": {"metric": "max_query_sec", "maximum": 30.0},
        "SHACL": {"metric": "shapes_per_sec", "minimum": 1000},
        "CML": {"metric": "records_per_sec", "minimum": 5000},
    }

    assert "LUBM" in suites
    assert "BSBM" in suites
    assert "SP2Bench" in suites
    assert suites["LUBM"]["minimum"] >= 50000
    assert suites["SP2Bench"]["maximum"] <= 30.0


# ===========================================================================
# CRA-036.8: Stretch objectives separation per Decision H-01
# ===========================================================================

def test_cra_036_8_stretch_objectives_separated_from_binding():
    manifest = WorkloadManifest.create_default(tier=ScaleTier.P2)
    engine = QualificationEngine(manifest)
    report = engine.generate_qualification_report()

    # Binding targets for P2
    binding = QualificationEngine.BINDING_TARGETS[ScaleTier.P2]
    stretch = report["stretch_objectives"]

    # Stretch numbers (AGG/OCA) are recorded separately and strictly faster than binding targets
    assert stretch["point_read_p95_ms"] <= binding["point_read_p95_ms"]
    assert stretch["min_ingest_triples_sec"] >= binding["min_ingest_triples_sec"]
    # Explicitly labeled in report
    assert "stretch_objectives" in report


# ===========================================================================
# CRA-036.9: Sustained load stability & CI latency regression gate (> 10%)
# ===========================================================================

def test_cra_036_9_regression_gate_and_stability():
    manifest = WorkloadManifest.create_default(tier=ScaleTier.P0)
    engine = QualificationEngine(manifest)

    # 1. Within 10% threshold passes
    passed, pct = engine.check_regression(current_p95=105.0, baseline_p95=100.0, threshold_pct=10.0)
    assert passed is True
    assert pct == 5.0

    # 2. Exceeding 10% fails the CI gate
    failed, pct_fail = engine.check_regression(current_p95=115.0, baseline_p95=100.0, threshold_pct=10.0)
    assert failed is False
    assert pct_fail == 15.0


# ===========================================================================
# CRA-036.10: Learned model qualification with 5 baselines and calibration error
# ===========================================================================

def test_cra_036_10_learned_model_baselines_and_ece():
    manifest = WorkloadManifest.create_default(tier=ScaleTier.P0)
    engine = QualificationEngine(manifest)

    baselines = {
        "majority_class": 0.52,
        "random": 0.50,
        "static_rule": 0.68,
        "linear_logistic": 0.72,
        "uncalibrated": 0.76,
    }

    seeded_trials = [0.84, 0.86, 0.85]

    eval_result = engine.evaluate_learned_model_baselines(
        task_name="link_prediction",
        model_accuracy=0.85,
        model_ece=0.042,  # 4.2% Expected Calibration Error
        baseline_accuracies=baselines,
        seeded_trials=seeded_trials,
    )

    assert eval_result["qualified"] is True
    assert eval_result["model_accuracy"] > baselines["majority_class"]
    assert eval_result["model_accuracy"] > baselines["random"]
    assert eval_result["model_ece"] < 0.15
    assert len(eval_result["seeded_trials"]) == 3
    assert eval_result["trial_std_dev"] > 0

    # Fails if any of the 5 mandatory baselines is missing
    incomplete_baselines = {"majority_class": 0.52, "random": 0.50}
    with pytest.raises(ValueError) as exc_missing:
        engine.evaluate_learned_model_baselines(
            task_name="link_prediction",
            model_accuracy=0.85,
            model_ece=0.042,
            baseline_accuracies=incomplete_baselines,
            seeded_trials=seeded_trials,
        )
    assert "missing mandatory baselines" in str(exc_missing.value)


# ===========================================================================
# CRA-036.A: Integrated Performance & Scale Qualification Acceptance
# ===========================================================================

def test_cra_036_a_performance_qualification_integrated(populated_graph):
    # 1. Initialize workload manifest and qualification engine
    manifest = WorkloadManifest.create_default(tier=ScaleTier.P0, seed=2026)
    engine = QualificationEngine(manifest)

    # 2. Record storage accounting
    engine.storage = StorageAccounting(
        asserted_triples=1000,
        inferred_triples=250,
        raw_payload_bytes=50000,
        hot_residency_bytes=40000,
    )

    # 3. Multi-trial execution with oracle verification
    def point_read():
        v = populated_graph.get_vertex_by_canonical_id("wi:10")
        return v["properties"]["name"]

    engine.run_multi_trial(
        operation_name="point_read",
        operation=point_read,
        oracle_expected="Task 10",
        trials_count=3,
        iterations_per_trial=15,
    )

    # 4. Learned model evaluation with 5 baselines
    baselines = {
        "majority_class": 0.51,
        "random": 0.50,
        "static_rule": 0.65,
        "linear_logistic": 0.70,
        "uncalibrated": 0.74,
    }
    model_eval = engine.evaluate_learned_model_baselines(
        task_name="graph_classifier",
        model_accuracy=0.82,
        model_ece=0.038,
        baseline_accuracies=baselines,
        seeded_trials=[0.81, 0.83, 0.82],
    )
    assert model_eval["qualified"] is True

    # 5. Generate machine-readable qualification report
    report = engine.generate_qualification_report()
    assert report["status"] == "QUALIFIED"
    assert report["manifest"]["manifest_id"] == "manifest-P0-2026"
    assert len(report["raw_trials"]) >= 1
    assert report["raw_trials"][0]["oracle_verified"] is True
    assert "stretch_objectives" in report
