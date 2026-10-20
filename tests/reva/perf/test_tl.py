"""NFR-008: transparency-log append p95 <= 5 ms; inclusion proof generation <= 20 ms (simulated size)."""

from __future__ import annotations

import time

import pytest

from reva.kernel.translog import leaf_hash, verify_inclusion
from tests.reva.perf.conftest import p95, record

pytestmark = [pytest.mark.reva_depth("component"), pytest.mark.reva_perf]


@pytest.mark.reva_case("performance")
def test_nfr008_append_p95(perf_kernel):
    _, _, log, _ = perf_kernel
    samples = []
    for i in range(1000):
        start = time.perf_counter()
        log.append(f"leaf-{i}")
        samples.append((time.perf_counter() - start) * 1000)
    value = p95(samples)
    record("nfr008_tl_append_p95_ms", value, 5, "ms")
    assert value <= 5


@pytest.mark.reva_case("performance")
def test_nfr008_inclusion_proof_generation(perf_kernel):
    _, store, log, _ = perf_kernel
    size = 20_000  # simulated size; the 100M-leaf target needs the node cache (not claimed here)
    store.conn.executemany(
        "INSERT INTO reva_log_leaves (log_id, leaf_index, leaf_data, leaf_hash, appended_at) VALUES (?, ?, ?, ?, ?)",
        [(log.log_id, i, f"leaf-{i}", leaf_hash(f"leaf-{i}".encode()), "2026-01-01T00:00:00.000Z")
         for i in range(size)])
    store.conn.commit()
    root = log.root(size)
    samples = []
    for index in (0, size // 3, size // 2, size - 1):
        start = time.perf_counter()
        proof = log.inclusion_proof(index, size)
        samples.append((time.perf_counter() - start) * 1000)
        assert verify_inclusion(leaf_hash(f"leaf-{index}".encode()), index, size,
                                [bytes.fromhex(p) for p in proof], root)
    worst = max(samples)
    record("nfr008_inclusion_proof_ms_at_20k", worst, 20, "ms")
    assert worst <= 20
