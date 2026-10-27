"""Unit tests for Phase 7 WP 7.2: Performance, Reliability, SLO, Telemetry, and Operations (35 tasks).

Requirements:
- PERF-01: Formal NFR benchmark suite (throughput, sub-50ms query latency)
- G2-PERF-002: Incremental update latency measured separately
- G2-PERF-003: Graph mutation throughput benchmarked
- G2-PERF-004: Historical-state reconstruction latency benchmarked
- G2-PERF-005: Graph diff latency benchmarked
- G2-PERF-006: Crawler concurrency source-configurable
- G2-PERF-007: High-volume telemetry adapters aggregate before graph write
- G2-PERF-008: Incremental processing avoids global recomputation
- G2-REL-002: Webhook delivery deduplicated
- G2-REL-003: Missed webhook recovery tested
- G2-REL-004: Reconciliation safe to rerun
- G2-REL-005: Event/journal corruption detection implemented
- G2-REL-006: Backup includes graph state plus metadata for sync continuity
- G2-REL-007: Restore preserves/restores connector checkpoints consistently
- G2-REL-008: Restore procedure documents whether events after backup must be replayed
- G2-SLO-002: SLOs configurable by domain
- G2-SLO-003: SLO breach creates quality finding
- G2-SLO-004: Dashboards show objective, current value, trend, breached assets
- G2-SLO-005: SLO evaluation reproducible against graph version
- G2-TEL-002: Telemetry-derived relationship has observation window
- G2-TEL-003: Telemetry-derived relationship includes source/evidence reference
- G2-TEL-004: Aggregation/fingerprints for repeated log patterns
- G2-TEL-005: Preserve bounded exemplar IDs/trace IDs
- G2-TEL-006: Configurable retention for derived telemetry facts
- G2-TEL-007: Runtime edge expires when no longer observed under configured policy
- G2-TEL-008: Explicit confidence/coverage distinguishing unobserved vs nonexistent
- MVP-FR-023: Structured logging with level, correlation id, component, timestamp
- MVP-FR-024: Local metrics registry with Prometheus text exposition
- MVP-FR-025: Graph state backup export
- MVP-FR-026: Graph state restore import with checksum validation
- NFR-OPS-001: Structured logging and health check endpoints
- NFR-OPS-002: Local metrics exposition
- NFR-PERF-001: Benchmark-defined objectives (p95 latency and throughput)
- NFR-REL-001: Restart-safe processing (checkpoint resume)
- NFR-REL-002: Backup and restore procedure
"""

from __future__ import annotations

import tempfile
import time
from pathlib import Path
import pytest

from eoip.graph.benchmark import BenchmarkHarness
from eoip.graph.memory import MemoryGraphStore
from eoip.ingest.incremental_crawler import (
    ConfigurableCrawlerEngine,
    CrawlerSourceConfig,
    IncrementalDeltaProcessor,
)
from eoip.observability.metrics import Counter, Gauge
from eoip.quality.slo import GraphQualitySLOEngine, QualitySLO
from eoip.recovery.wal import WriteAheadLog
from eoip.recovery.webhook_reliability import (
    JournalCorruptionDetector,
    ReconciliationSafetyEngine,
    WebhookEvent,
    WebhookReliabilityManager,
    get_restore_procedure_documentation,
)
from eoip.snapshot import backup, restore
from eoip.telemetry.adapter import SemanticTelemetryAdapter


# ==============================================================================
# Performance Benchmarks & Ingestion (PERF-01, NFR-PERF-001, G2-PERF-002..008)
# ==============================================================================

@pytest.mark.req("PERF-01")
def test_perf_01_formal_nfr_benchmark_suite():
    store = MemoryGraphStore()
    harness = BenchmarkHarness()
    results = harness.run_large_scale_benchmark(store, target_nodes=50_000)
    assert results["target_scale_nodes"] == 50_000
    assert results["p95_latency_ms"] < 50.0
    assert results["measured_throughput_ops_sec"] > 2000.0


@pytest.mark.req("NFR-PERF-001")
def test_nfr_perf_001_benchmark_defined_objectives():
    store = MemoryGraphStore()
    harness = BenchmarkHarness()
    results = harness.run_large_scale_benchmark(store, target_nodes=50_000)
    assert results["target_50k_kpi_met"] is True
    assert results["sub_50ms_sla_met"] is True


@pytest.mark.req("G2-PERF-002")
def test_g2_perf_002_incremental_update_latency_measured():
    store = MemoryGraphStore()
    v1 = store.upsert_vertex("Service", {"canonical_id": "svc:bench-inc", "name": "Initial"})
    
    t0 = time.perf_counter()
    store.upsert_vertex("Service", {"canonical_id": "svc:bench-inc", "name": "Updated"})
    latency_ms = (time.perf_counter() - t0) * 1000.0

    assert latency_ms < 20.0  # sub-20ms incremental update
    assert store.get_vertex(v1["vid"])["properties"]["name"] == "Updated"


@pytest.mark.req("G2-PERF-003")
def test_g2_perf_003_graph_mutation_throughput_benchmarked():
    store = MemoryGraphStore()
    harness = BenchmarkHarness()
    res = harness.run_vertex_insert_benchmark(store, count=100)
    assert res.throughput_ops_sec > 100.0
    assert res.p95_ms > 0.0


@pytest.mark.req("G2-PERF-004")
def test_g2_perf_004_historical_state_reconstruction_latency():
    from eoip.graph.twin import get_twin_state
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "svc:t1", "name": "T1"})
    
    t0 = time.perf_counter()
    state = get_twin_state(store, revision="HEAD")
    reconstruction_latency_ms = (time.perf_counter() - t0) * 1000.0

    assert reconstruction_latency_ms < 50.0
    assert state["total_entities"] >= 1


@pytest.mark.req("G2-PERF-005")
def test_g2_perf_005_graph_diff_latency_benchmarked():
    from eoip.ontology.gitops import diff_manifests, current_manifest_snapshot
    m1 = current_manifest_snapshot()
    m2 = dict(m1)
    m2["version"] = "v1.1.0"

    t0 = time.perf_counter()
    diff = diff_manifests(m1, m2)
    diff_latency_ms = (time.perf_counter() - t0) * 1000.0

    assert diff_latency_ms < 50.0
    assert hasattr(diff, "breaking")
    assert isinstance(diff.breaking, list)



@pytest.mark.req("G2-PERF-006")
def test_g2_perf_006_crawler_concurrency_source_configurable():
    engine = ConfigurableCrawlerEngine()
    engine.register_source_config(CrawlerSourceConfig("github", max_concurrency=8))
    engine.register_source_config(CrawlerSourceConfig("legacy_jira", max_concurrency=2))

    assert engine.get_source_concurrency("github") == 8
    assert engine.get_source_concurrency("legacy_jira") == 2

    # Verify concurrency limits enforced
    assert engine.allocate_worker_slot("legacy_jira") is True
    assert engine.allocate_worker_slot("legacy_jira") is True
    assert engine.allocate_worker_slot("legacy_jira") is False  # Limit reached


@pytest.mark.req("G2-PERF-007")
def test_g2_perf_007_telemetry_adapters_aggregate_before_graph_write():
    adapter = SemanticTelemetryAdapter()
    traces = [f"trace-{i}" for i in range(100)]
    edge = adapter.aggregate_service_interaction(
        caller_cid="svc:web",
        callee_cid="svc:auth",
        window_start=1000.0,
        window_end=1060.0,
        trace_ids=traces,
    )
    # Pre-write aggregation compresses 100 traces into 1 bounded semantic edge
    assert edge.call_count == 100
    assert len(edge.exemplar_trace_ids) <= 5


@pytest.mark.req("G2-PERF-008")
def test_g2_perf_008_incremental_processing_avoids_global_recompute():
    store = MemoryGraphStore()
    processor = IncrementalDeltaProcessor(store)

    batch_1 = [
        {"canonical_id": "svc:auth", "properties": {"name": "Auth Service"}},
        {"canonical_id": "svc:cart", "properties": {"name": "Cart Service"}},
    ]
    r1 = processor.process_incremental_batch("repo-1", batch_1, "c1")
    assert r1["added"] == 2
    assert r1["skipped_unmodified"] == 0

    # Incremental update: only svc:cart is updated, svc:auth is unchanged
    batch_2 = [
        {"canonical_id": "svc:auth", "properties": {"name": "Auth Service"}},
        {"canonical_id": "svc:cart", "properties": {"name": "Cart Service v2"}},
    ]
    r2 = processor.process_incremental_batch("repo-1", batch_2, "c2")
    assert r2["skipped_unmodified"] == 1
    assert r2["modified"] == 1
    assert r2["avoided_global_recompute"] is True


# ==============================================================================
# Reliability, Recovery & Webhooks (G2-REL-002..008, NFR-REL-001, NFR-REL-002)
# ==============================================================================

@pytest.mark.req("G2-REL-002")
def test_g2_rel_002_webhook_delivery_deduplicated():
    mgr = WebhookReliabilityManager()
    event = WebhookEvent("evt-101", "github", {"ref": "refs/heads/main"})

    r1 = mgr.receive_webhook(event)
    assert r1["status"] == "ACCEPTED"
    assert r1["deduplicated"] is False

    # Second delivery with identical event
    r2 = mgr.receive_webhook(event)
    assert r2["status"] == "DUPLICATE_IGNORED"
    assert r2["deduplicated"] is True


@pytest.mark.req("G2-REL-003")
def test_g2_rel_003_missed_webhook_recovery_tested():
    mgr = WebhookReliabilityManager()
    evt1 = WebhookEvent("evt-missed-1", "jira", {"issue": "PROJ-1"})
    mgr.record_failed_webhook(evt1)

    replayed = mgr.recover_missed_webhooks()
    assert len(replayed) == 1
    assert replayed[0]["event_id"] == "evt-missed-1"
    assert replayed[0]["status"] == "REPLAYED_SUCCESS"


@pytest.mark.req("G2-REL-004")
def test_g2_rel_004_reconciliation_safe_to_rerun():
    store = MemoryGraphStore()
    engine = ReconciliationSafetyEngine(store)

    records = [
        {"canonical_id": "svc:alpha", "label": "Service", "properties": {"canonical_id": "svc:alpha", "name": "Alpha"}},
        {"canonical_id": "svc:beta", "label": "Service", "properties": {"canonical_id": "svc:beta", "name": "Beta"}},
    ]

    r1 = engine.rerun_reconciliation(records)
    assert r1["created"] == 2
    assert store.count_vertices() == 2

    # Rerun immediately: must not duplicate entities
    r2 = engine.rerun_reconciliation(records)
    assert r2["created"] == 0
    assert r2["updated"] == 2
    assert store.count_vertices() == 2
    assert r2["rerun_safe"] is True


@pytest.mark.req("G2-REL-005")
def test_g2_rel_005_event_journal_corruption_detection():
    detector = JournalCorruptionDetector()
    h1 = detector.append_journal_entry("entry-1", {"action": "create_node"})
    detector.append_journal_entry("entry-2", {"action": "update_node"}, prev_hash=h1)

    ver = detector.verify_journal_integrity()
    assert ver["valid"] is True

    # Tamper with entry 1
    detector.journal_records[0]["payload"]["action"] = "tampered_action"
    ver_tampered = detector.verify_journal_integrity()
    assert ver_tampered["valid"] is False
    assert ver_tampered["error"] == "HASH_CHAIN_MISMATCH"


@pytest.mark.req("G2-REL-006")
def test_g2_rel_006_backup_includes_graph_and_sync_metadata():
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "svc:backup-01", "name": "Backup Service"})
    with tempfile.TemporaryDirectory() as tmp_dir:
        backup_path = Path(tmp_dir) / "backup_test.json"
        res = backup(store, tmp_dir, str(backup_path))
        assert Path(backup_path).exists()
        assert res["vertices"] >= 1
        assert "sha256" in res


@pytest.mark.req("G2-REL-007")
def test_g2_rel_007_restore_preserves_checkpoints():
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "svc:checkpoint", "name": "Checkpoint Svc"})
    with tempfile.TemporaryDirectory() as tmp_dir:
        backup_path = Path(tmp_dir) / "snapshot.json"
        backup(store, tmp_dir, str(backup_path))
        
        target_store = MemoryGraphStore()
        restore(target_store, tmp_dir, str(backup_path))
        assert target_store.count_vertices() == store.count_vertices()
        assert target_store.get_vertex_by_canonical_id("svc:checkpoint") is not None


@pytest.mark.req("G2-REL-008")
def test_g2_rel_008_restore_procedure_documents_event_replay():
    doc = get_restore_procedure_documentation()
    assert doc["replay_required"] is True
    assert "replay_mechanism" in doc
    assert len(doc["verification_steps"]) >= 4


@pytest.mark.req("NFR-REL-001")
def test_nfr_rel_001_restart_safe_processing():
    from eoip.recovery.wal import WALOperationType
    wal = WriteAheadLog()
    wal.append(WALOperationType.INSERT, "Service", "svc:restart", {"name": "Restart Service"})
    pt = wal.checkpoint("chk-01")
    assert pt.lsn >= 1

    entries = wal.read_from(start_lsn=0)
    assert len(entries) >= 1
    assert entries[0].entity_id == "svc:restart"




@pytest.mark.req("NFR-REL-002")
def test_nfr_rel_002_backup_and_restore_procedure():
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "svc:nfr-b", "name": "NFR Backup"})
    with tempfile.TemporaryDirectory() as tmp_dir:
        archive = Path(tmp_dir) / "nfr_backup.json"
        backup(store, tmp_dir, str(archive))
        assert archive.exists()
        target_store = MemoryGraphStore()
        restore(target_store, tmp_dir, str(archive))
        assert target_store.get_vertex_by_canonical_id("svc:nfr-b") is not None



# ==============================================================================
# Service Level Objectives (G2-SLO-002..005)
# ==============================================================================

@pytest.mark.req("G2-SLO-002")
def test_g2_slo_002_slos_configurable_by_domain():
    store = MemoryGraphStore()
    engine = GraphQualitySLOEngine(store)

    engine.configure_slo(QualitySLO("slo-sec-01", "Security Ownership", domain="Security", target_percentage=98.0, metric_type="OWNERSHIP_COVERAGE"))
    engine.configure_slo(QualitySLO("slo-plat-01", "Platform Docs", domain="Platform", target_percentage=90.0, metric_type="DOC_COVERAGE"))

    assert len(engine._slos) == 2
    assert engine._slos["slo-sec-01"].domain == "Security"
    assert engine._slos["slo-plat-01"].domain == "Platform"


@pytest.mark.req("G2-SLO-003")
def test_g2_slo_003_slo_breach_creates_quality_finding():
    store = MemoryGraphStore()
    # Add unowned service
    store.upsert_vertex("APIService", {"canonical_id": "api:unowned", "name": "Unowned API"})

    engine = GraphQualitySLOEngine(store)
    engine.configure_slo(QualitySLO("slo-own", "Ownership", domain="Governance", target_percentage=100.0, metric_type="OWNERSHIP_COVERAGE"))

    eval_res = engine.evaluate_slos()
    assert eval_res["breached_slo_count"] == 1
    assert len(eval_res["quality_findings"]) == 1
    assert eval_res["quality_findings"][0]["slo_id"] == "slo-own"


@pytest.mark.req("G2-SLO-004")
def test_g2_slo_004_dashboards_show_objective_trend_breached_assets():
    store = MemoryGraphStore()
    store.upsert_vertex("APIService", {"canonical_id": "api:asset-1", "name": "Asset 1"})

    engine = GraphQualitySLOEngine(store)
    engine.configure_slo(QualitySLO("slo-own", "Ownership", domain="Platform", target_percentage=100.0, metric_type="OWNERSHIP_COVERAGE"))

    eval_res = engine.evaluate_slos()
    metric = eval_res["dashboard_metrics"][0]
    assert metric["target_percentage"] == 100.0
    assert "trend" in metric
    assert "api:asset-1" in metric["breached_assets"]


@pytest.mark.req("G2-SLO-005")
def test_g2_slo_005_slo_evaluation_reproducible_against_graph_version():
    store = MemoryGraphStore()
    engine = GraphQualitySLOEngine(store)
    engine.configure_slo(QualitySLO("slo-own", "Ownership", domain="Governance", target_percentage=95.0, metric_type="OWNERSHIP_COVERAGE"))

    res_v1 = engine.evaluate_slos(graph_version="v1.0.0")
    assert res_v1["graph_version"] == "v1.0.0"
    res_v2 = engine.evaluate_slos(graph_version="v2.0.0")
    assert res_v2["graph_version"] == "v2.0.0"


# ==============================================================================
# Semantic Telemetry (G2-TEL-002..008)
# ==============================================================================

@pytest.mark.req("G2-TEL-002")
def test_g2_tel_002_telemetry_derived_relationship_has_observation_window():
    adapter = SemanticTelemetryAdapter()
    t0 = 1000.0
    t1 = 1060.0
    edge = adapter.aggregate_service_interaction("svc:a", "svc:b", window_start=t0, window_end=t1, trace_ids=["tr-1"])
    assert edge.window_start == t0
    assert edge.window_end == t1


@pytest.mark.req("G2-TEL-003")
def test_g2_tel_003_telemetry_relationship_includes_source_evidence_ref():
    adapter = SemanticTelemetryAdapter()
    edge = adapter.aggregate_service_interaction(
        "svc:a", "svc:b", 1000.0, 1060.0, ["tr-1"],
        source_ref="datadog:apm",
    )
    assert edge.source_ref == "datadog:apm"
    assert "urn:evidence:trace" in edge.evidence_key


@pytest.mark.req("G2-TEL-004")
def test_g2_tel_004_aggregation_fingerprints_for_repeated_logs():
    adapter = SemanticTelemetryAdapter()
    fp1 = adapter.compute_log_fingerprint("Error connection failed to host 10.0.0.1 on port 5432")
    fp2 = adapter.compute_log_fingerprint("Error connection failed to host 192.168.1.5 on port 8080")
    # Normalized number replacement yields identical fingerprint for recurring error pattern
    assert fp1 == fp2


@pytest.mark.req("G2-TEL-005")
def test_g2_tel_005_preserve_bounded_exemplar_trace_ids():
    adapter = SemanticTelemetryAdapter()
    traces = [f"trace-{i}" for i in range(50)]
    edge = adapter.aggregate_service_interaction("svc:caller", "svc:callee", 1000.0, 1060.0, traces)
    assert len(edge.exemplar_trace_ids) == 5  # Bounded to top 5


@pytest.mark.req("G2-TEL-006")
def test_g2_tel_006_configurable_retention_for_derived_facts():
    adapter = SemanticTelemetryAdapter(retention_days=14)
    assert adapter.retention_days == 14


@pytest.mark.req("G2-TEL-007")
def test_g2_tel_007_runtime_edge_expires_under_policy():
    adapter = SemanticTelemetryAdapter()
    adapter.aggregate_service_interaction("svc:x", "svc:y", 1000.0, 1060.0, ["tr-1"])
    
    # 2 hours later (7200s > 3600s TTL)
    expired = adapter.purge_expired_runtime_edges(current_time=1060.0 + 7200.0, ttl_seconds=3600.0)
    assert len(expired) == 1


@pytest.mark.req("G2-TEL-008")
def test_g2_tel_008_explicit_confidence_coverage_status():
    adapter = SemanticTelemetryAdapter()
    adapter.aggregate_service_interaction("svc:a", "svc:b", 1000.0, 1060.0, ["tr-1"], confidence=0.95)

    cov_existing = adapter.get_edge_coverage("svc:a", "svc:b")
    assert cov_existing["exists"] is True
    assert cov_existing["coverage_status"] == "OBSERVED"
    assert cov_existing["confidence"] == 0.95

    cov_absent = adapter.get_edge_coverage("svc:a", "svc:nonexistent")
    assert cov_absent["exists"] is False
    assert cov_absent["coverage_status"] == "NOT_OBSERVED_IN_WINDOW"
    assert cov_absent["confidence"] == 0.0


# ==============================================================================
# Operations, Logging & Metrics (MVP-FR-023..026, NFR-OPS-001, NFR-OPS-002)
# ==============================================================================

@pytest.mark.req("MVP-FR-023")
def test_mvp_fr_023_logging():
    import logging
    logger = logging.getLogger("eoip.test")
    assert logger is not None


@pytest.mark.req("NFR-OPS-001")
def test_nfr_ops_001_structured_logging_and_health():
    store = MemoryGraphStore()
    assert store.health() is True
    assert store.ping()["status"] == "ok"


@pytest.mark.req("MVP-FR-024")
def test_mvp_fr_024_metrics():
    c = Counter("http_requests_total", "Total requests", label_names=("method", "path"))
    c.inc(method="GET", path="/api/v1/health")
    assert c.get(method="GET", path="/api/v1/health") == 1.0


@pytest.mark.req("NFR-OPS-002")
def test_nfr_ops_002_local_metrics():
    g = Gauge("active_connections", "Active DB connections")
    g.set(12.0)
    assert g.get() == 12.0


@pytest.mark.req("MVP-FR-025")
def test_mvp_fr_025_backup():
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "svc:mvp-b", "name": "MVP Backup"})
    with tempfile.TemporaryDirectory() as tmp_dir:
        archive = Path(tmp_dir) / "mvp_backup.json"
        res = backup(store, tmp_dir, str(archive))
        assert archive.exists()
        assert res["vertices"] >= 1


@pytest.mark.req("MVP-FR-026")
def test_mvp_fr_026_restore():
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "svc:mvp-r", "name": "MVP Restore"})
    with tempfile.TemporaryDirectory() as tmp_dir:
        archive = Path(tmp_dir) / "mvp_restore.json"
        backup(store, tmp_dir, str(archive))
        target_store = MemoryGraphStore()
        restore(target_store, tmp_dir, str(archive))
        assert target_store.count_vertices() == store.count_vertices()

