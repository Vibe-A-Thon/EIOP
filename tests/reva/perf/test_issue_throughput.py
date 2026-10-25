"""NFR-001 / NFR-002 / NFR-003 on SQLite: issue throughput, issue latency, verified read latency."""

from __future__ import annotations

import statistics
import time

import pytest

from tests.reva.perf.conftest import p95, record

pytestmark = [pytest.mark.reva_depth("component"), pytest.mark.reva_perf]


@pytest.mark.reva_case("performance")
def test_nfr001_issue_throughput_sqlite(perf_kernel):
    kernel, store, log, draft = perf_kernel
    rates = []
    for run in range(5):  # 5 runs, median reported (NFR-001 method)
        start = time.perf_counter()
        for i in range(300):
            kernel.issue("t1", draft(run * 1000 + i))
        rates.append(300 / (time.perf_counter() - start))
    median = statistics.median(rates)
    record("nfr001_issue_per_s_sqlite", median, 300, "warrants/s")
    assert median >= 300
    assert log.size() == 1500 and store.conn.execute("SELECT COUNT(*) FROM reva_warrants").fetchone()[0] == 1500


@pytest.mark.reva_case("performance")
def test_nfr002_issue_latency_p95(perf_kernel):
    kernel, _, _, draft = perf_kernel
    samples = []
    for i in range(400):
        start = time.perf_counter()
        kernel.issue("t1", draft(i))
        samples.append((time.perf_counter() - start) * 1000)
    value = p95(samples)
    record("nfr002_issue_p95_ms", value, 25, "ms")
    assert value <= 25


@pytest.mark.reva_case("performance")
def test_nfr003_verified_read_p95(perf_kernel):
    kernel, _, _, draft = perf_kernel
    ids = [kernel.issue("t1", draft(i)).warrant_id for i in range(300)]
    samples = []
    for wid in ids:
        start = time.perf_counter()
        kernel.get("t1", "system", wid)  # verifies ID digest and signature
        samples.append((time.perf_counter() - start) * 1000)
    value = p95(samples)
    record("nfr003_read_verify_p95_ms", value, 10, "ms")
    assert value <= 10
