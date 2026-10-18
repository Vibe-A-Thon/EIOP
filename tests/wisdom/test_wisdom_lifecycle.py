"""Tests for Wisdom Graph decision traces, precedent search, outcome tracking, and counsel."""

from datetime import datetime, timezone
import pytest

from eoip.wisdom.decision_trace import DecisionTrace, DecisionOption
from eoip.wisdom.precedent_engine import PrecedentEngine
from eoip.wisdom.outcome_tracker import OutcomeTracker
from eoip.wisdom.counsel import CounselService


def test_decision_trace_creation_and_digest():
    trace = DecisionTrace(
        trace_id="DT-2026-001",
        tenant_id="acme-demo",
        title="Database Migration from Legacy Store to Native RocksDB LPG",
        situation="High latency under concurrency on SPARQL triplestore during graph traversal queries.",
        context_tags=["database", "migration", "rocksdb", "performance", "traversal"],
        options=[
            DecisionOption(
                option_id="opt-rocksdb",
                description="Migrate to RocksDB LPG engine",
                projected_impact={"p95_latency_ms": 15.0, "throughput_qps": 2000.0},
            ),
            DecisionOption(
                option_id="opt-scale-triplestore",
                description="Scale triplestore hardware",
                projected_impact={"p95_latency_ms": 80.0, "throughput_qps": 500.0},
            ),
        ],
        selected_option_id="opt-rocksdb",
        rationale="RocksDB LPG provides direct edge property addressing without reification tax.",
        decided_by="Chief Architect",
    )
    digest = trace.digest()
    assert len(digest) == 64
    assert trace.status == "RECORDED"


def test_precedent_engine_indexing_and_search():
    engine = PrecedentEngine()
    t1 = DecisionTrace(
        trace_id="DT-001",
        tenant_id="acme-demo",
        title="Adopt RocksDB for Graph Traversal",
        situation="Need low-latency graph pathfinding under high concurrent query loads.",
        context_tags=["graph", "traversal", "rocksdb", "latency"],
        selected_option_id="opt-rocksdb",
        rationale="Benchmark showed 10x throughput improvement.",
        decided_by="Architect",
    )
    t2 = DecisionTrace(
        trace_id="DT-002",
        tenant_id="acme-demo",
        title="Implement Air-Gap JVM Sidecar",
        situation="Customer requires offline air-gapped ELK reasoner without cloud connectivity.",
        context_tags=["airgap", "security", "reasoning", "sidecar"],
        selected_option_id="opt-container",
        rationale="Self-contained container avoids security violations.",
        decided_by="Security Officer",
    )
    engine.index_trace(t1)
    engine.index_trace(t2)

    # Search with overlapping tags and query
    matches = engine.find_precedents(
        query_situation="traversal query latency scaling",
        context_tags=["graph", "latency"],
    )
    assert len(matches) >= 1
    assert matches[0].trace.trace_id == "DT-001"
    assert matches[0].similarity_score > 0.3


def test_outcome_tracking_and_calibration():
    tracker = OutcomeTracker()
    trace = DecisionTrace(
        trace_id="DT-003",
        tenant_id="acme-demo",
        title="Cache Optimization",
        situation="Hot node lookup latency spike",
        context_tags=["cache", "memory"],
        options=[
            DecisionOption(
                option_id="opt-lru",
                description="LRU cache layer",
                projected_impact={"hit_rate": 0.85, "speedup": 3.0},
            )
        ],
        selected_option_id="opt-lru",
        rationale="In-memory cache absorbs 80% read volume",
        decided_by="Performance Engineer",
    )
    tracker.track(trace)

    # Record actual outcome
    outcome = tracker.record_outcome(
        trace_id="DT-003",
        actual_metrics={"hit_rate": 0.88, "speedup": 3.2},
        lessons_learned="LRU cache performed even better than projected on real traffic.",
        evaluated_by="Site Reliability Lead",
    )
    assert outcome.variance_analysis["hit_rate"] == pytest.approx(0.03, abs=0.01)
    assert outcome.variance_analysis["speedup"] == pytest.approx(0.2, abs=0.01)

    # Person calibration
    cal = tracker.compute_person_calibration("Performance Engineer")
    assert cal.total_decisions_evaluated == 1
    assert cal.tendency in ("WELL_CALIBRATED", "UNDERESTIMATING")


def test_counsel_service_recommendation():
    engine = PrecedentEngine()
    tracker = OutcomeTracker()
    trace = DecisionTrace(
        trace_id="DT-004",
        tenant_id="acme-demo",
        title="Rate Limiter Implementation",
        situation="External API abuse causing denial of service.",
        context_tags=["api", "rate_limit", "security"],
        options=[
            DecisionOption(
                option_id="opt-token-bucket",
                description="Token bucket per tenant",
                projected_impact={"blocked_abuse": 0.99},
            )
        ],
        selected_option_id="opt-token-bucket",
        rationale="Token bucket smooths bursty requests fairly.",
        decided_by="Security Architect",
    )
    engine.index_trace(trace)
    tracker.track(trace)

    service = CounselService(engine, tracker)
    report = service.generate_counsel(
        situation="Need API rate limiting defense against DDoS bursts",
        context_tags=["api", "security"],
    )
    assert report.confidence_score > 0.3
    assert len(report.relevant_precedents) >= 1
    assert "Token bucket" in report.recommended_strategy
