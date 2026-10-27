"""Production-Scale Load Testing Runner (TEST-002).

Executes reproducible, concurrent load scenarios:
- Concurrent Graph Queries
- Bulk Entity & Edge Ingestion
- Agent Swarm Execution
- RAG Retrieval under Load

Computes p50, p90, p99 latencies, throughput (RPS), error rates,
and asserts against strict performance SLOs.
"""

from __future__ import annotations

import asyncio
import logging
import statistics
import time
from dataclasses import dataclass, field
from typing import Any
from collections.abc import Callable

logger = logging.getLogger("eoip.tests.load")


@dataclass
class ScenarioResult:
    scenario_name: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    duration_seconds: float
    rps: float
    p50_ms: float
    p90_ms: float
    p99_ms: float
    errors: list[str] = field(default_factory=list)

    @property
    def error_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.failed_requests / self.total_requests

    def passes_slo(self, max_p99_ms: float = 250.0, max_error_rate: float = 0.01) -> bool:
        return self.p99_ms <= max_p99_ms and self.error_rate <= max_error_rate


class LoadTestRunner:
    """Async concurrent load generator for system performance testing."""

    async def run_scenario(
        self,
        name: str,
        task_fn: Callable[[], Any],
        concurrency: int = 10,
        total_requests: int = 100,
        ramp_up_seconds: float = 0.0,
    ) -> ScenarioResult:
        latencies_ms: list[float] = []
        errors: list[str] = []
        semaphore = asyncio.Semaphore(concurrency)
        start_time = time.perf_counter()

        async def worker(idx: int) -> None:
            if ramp_up_seconds > 0:
                await asyncio.sleep((idx / total_requests) * ramp_up_seconds)
            async with semaphore:
                t0 = time.perf_counter()
                try:
                    if asyncio.iscoroutinefunction(task_fn):
                        await task_fn()
                    else:
                        task_fn()
                    lat_ms = (time.perf_counter() - t0) * 1000.0
                    latencies_ms.append(lat_ms)
                except Exception as exc:
                    lat_ms = (time.perf_counter() - t0) * 1000.0
                    latencies_ms.append(lat_ms)
                    errors.append(str(exc))

        tasks = [asyncio.create_task(worker(i)) for i in range(total_requests)]
        await asyncio.gather(*tasks)

        duration = time.perf_counter() - start_time
        latencies_ms.sort()

        if latencies_ms:
            p50 = latencies_ms[int(len(latencies_ms) * 0.50)]
            p90 = latencies_ms[min(int(len(latencies_ms) * 0.90), len(latencies_ms) - 1)]
            p99 = latencies_ms[min(int(len(latencies_ms) * 0.99), len(latencies_ms) - 1)]
        else:
            p50 = p90 = p99 = 0.0

        success = total_requests - len(errors)
        rps = total_requests / duration if duration > 0 else 0.0

        return ScenarioResult(
            scenario_name=name,
            total_requests=total_requests,
            successful_requests=success,
            failed_requests=len(errors),
            duration_seconds=duration,
            rps=rps,
            p50_ms=p50,
            p90_ms=p90,
            p99_ms=p99,
            errors=errors[:10],
        )
