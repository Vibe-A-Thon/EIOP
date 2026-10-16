"""Mark WP 7.2 (Performance, Reliability, SLO, Telemetry, and Operations) requirements as done."""

from _mark_done import mark_done

TEST_FILE = "tests/unit/test_performance_reliability_and_operations_wp72.py"

WP72_REQUIREMENTS = {
    "PERF-01": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/graph/benchmark.py"],
    },
    "G2-PERF-002": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/graph/memory.py"],
    },
    "G2-PERF-003": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/graph/benchmark.py"],
    },
    "G2-PERF-004": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/graph/twin.py"],
    },
    "G2-PERF-005": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/ontology/gitops.py"],
    },
    "G2-PERF-006": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/ingest/incremental_crawler.py"],
    },
    "G2-PERF-007": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/telemetry/adapter.py"],
    },
    "G2-PERF-008": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/ingest/incremental_crawler.py"],
    },
    "G2-REL-002": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/recovery/webhook_reliability.py"],
    },
    "G2-REL-003": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/recovery/webhook_reliability.py"],
    },
    "G2-REL-004": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/recovery/webhook_reliability.py"],
    },
    "G2-REL-005": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/recovery/webhook_reliability.py"],
    },
    "G2-REL-006": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/snapshot.py"],
    },
    "G2-REL-007": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/snapshot.py"],
    },
    "G2-REL-008": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/recovery/webhook_reliability.py"],
    },
    "G2-SLO-002": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/quality/slo.py"],
    },
    "G2-SLO-003": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/quality/slo.py"],
    },
    "G2-SLO-004": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/quality/slo.py"],
    },
    "G2-SLO-005": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/quality/slo.py"],
    },
    "G2-TEL-002": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/telemetry/adapter.py"],
    },
    "G2-TEL-003": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/telemetry/adapter.py"],
    },
    "G2-TEL-004": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/telemetry/adapter.py"],
    },
    "G2-TEL-005": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/telemetry/adapter.py"],
    },
    "G2-TEL-006": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/telemetry/adapter.py"],
    },
    "G2-TEL-007": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/telemetry/adapter.py"],
    },
    "G2-TEL-008": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/telemetry/adapter.py"],
    },
    "MVP-FR-023": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/observability/metrics.py"],
    },
    "MVP-FR-024": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/observability/metrics.py"],
    },
    "MVP-FR-025": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/snapshot.py"],
    },
    "MVP-FR-026": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/snapshot.py"],
    },
    "NFR-OPS-001": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/graph/memory.py"],
    },
    "NFR-OPS-002": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/observability/metrics.py"],
    },
    "NFR-PERF-001": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/graph/benchmark.py"],
    },
    "NFR-REL-001": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/recovery/wal.py"],
    },
    "NFR-REL-002": {
        "test_file": TEST_FILE,
        "code_paths": ["packages/eoip/snapshot.py"],
    },
}

if __name__ == "__main__":
    mark_done(WP72_REQUIREMENTS)
