#!/usr/bin/env python3
"""Standalone Multi-Threaded Stress Test Runner for KnowGridFlow / EOIP."""

from __future__ import annotations

import argparse
import sys
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from qa_bench.config import TEST_ROLES, BACKEND_URL, API_PREFIX


def run_stress_test(
    concurrency: int = 15,
    duration_seconds: int = 10,
    target_endpoint: str = "/graph/schema",
) -> dict:
    import httpx

    role = TEST_ROLES["admin"]
    headers = {
        "Authorization": f"Bearer {role.token}",
        "X-Tenant-Id": role.tenant,
        "Accept": "application/json",
    }

    # Check if remote server is online
    url = f"{BACKEND_URL}{API_PREFIX}{target_endpoint}"
    use_inprocess = False
    try:
        with httpx.Client(timeout=1.0) as probe:
            probe.get(f"{BACKEND_URL}/healthz")
    except Exception:
        use_inprocess = True

    if use_inprocess:
        from apps.api.main import create_app
        from fastapi.testclient import TestClient
        app = create_app()
        print(f"\n[*] Starting In-Process Fast Stress Run against endpoint: {target_endpoint}")
    else:
        print(f"\n[*] Starting Remote Stress Run against: {url}")

    print(f"    Concurrency : {concurrency} workers")
    print(f"    Duration    : {duration_seconds}s\n")

    latencies: list[float] = []
    success_count = 0
    failure_count = 0
    start_time = time.time()
    end_time = start_time + duration_seconds

    def _worker():
        nonlocal success_count, failure_count
        if use_inprocess:
            client = TestClient(app, base_url="http://testserver/api/v1")
            client.headers.update(headers)
            while time.time() < end_time:
                t0 = time.perf_counter()
                try:
                    res = client.get(target_endpoint)
                    t_req = time.perf_counter() - t0
                    if res.status_code == 200:
                        success_count += 1
                        latencies.append(t_req)
                    else:
                        failure_count += 1
                except Exception:
                    failure_count += 1
        else:
            with httpx.Client(timeout=10.0, headers=headers) as client:
                while time.time() < end_time:
                    t0 = time.perf_counter()
                    try:
                        res = client.get(url)
                        t_req = time.perf_counter() - t0
                        if res.status_code == 200:
                            success_count += 1
                            latencies.append(t_req)
                        else:
                            failure_count += 1
                    except Exception:
                        failure_count += 1

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(_worker) for _ in range(concurrency)]
        for f in as_completed(futures):
            f.result()

    total_requests = success_count + failure_count
    actual_duration = time.time() - start_time
    rps = total_requests / actual_duration if actual_duration > 0 else 0

    print("=" * 60)
    print("  STRESS BENCHMARK RESULTS")
    print("=" * 60)
    print(f"  Duration         : {actual_duration:.2f} s")
    print(f"  Total Requests   : {total_requests}")
    print(f"  Successful (200) : {success_count}")
    print(f"  Failures         : {failure_count} (Error rate: {(failure_count/max(total_requests,1))*100:.2f}%)")
    print(f"  Throughput (RPS) : {rps:.2f} req/s")

    if latencies:
        latencies_ms = [l * 1000.0 for l in sorted(latencies)]
        p50 = statistics.median(latencies_ms)
        p95 = latencies_ms[int(len(latencies_ms) * 0.95)]
        p99 = latencies_ms[int(len(latencies_ms) * 0.99)]
        print(f"  P50 Latency      : {p50:.2f} ms")
        print(f"  P95 Latency      : {p95:.2f} ms")
        print(f"  P99 Latency      : {p99:.2f} ms")
    print("=" * 60 + "\n")

    return {
        "total_requests": total_requests,
        "rps": rps,
        "error_rate": failure_count / max(total_requests, 1),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KnowGridFlow Stress Bench Runner")
    parser.add_argument("-c", "--concurrency", type=int, default=10)
    parser.add_argument("-d", "--duration", type=int, default=5)
    parser.add_argument("-e", "--endpoint", type=str, default="/graph/schema")
    args = parser.parse_args()

    run_stress_test(
        concurrency=args.concurrency,
        duration_seconds=args.duration,
        target_endpoint=args.endpoint,
    )
