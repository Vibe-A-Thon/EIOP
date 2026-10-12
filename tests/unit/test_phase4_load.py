"""Unit Tests for Production-Scale Load Testing Runner (TEST-002)."""

import pytest
import asyncio
from tests.load.load_runner import LoadTestRunner


@pytest.mark.asyncio
async def test_load_test_runner_concurrent_queries():
    runner = LoadTestRunner()
    call_count = 0

    async def mock_query_task():
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.005)

    result = await runner.run_scenario(
        name="test_concurrent_queries",
        task_fn=mock_query_task,
        concurrency=10,
        total_requests=40,
    )

    assert result.total_requests == 40
    assert result.successful_requests == 40
    assert result.failed_requests == 0
    assert result.error_rate == 0.0
    assert result.rps > 0
    assert result.p50_ms > 0
    assert result.p99_ms > 0
    assert result.passes_slo(max_p99_ms=500.0, max_error_rate=0.01)


@pytest.mark.asyncio
async def test_load_test_runner_error_capture():
    runner = LoadTestRunner()

    def mock_failing_task():
        raise ConnectionResetError("Connection dropped by peer")

    result = await runner.run_scenario(
        name="test_failing_calls",
        task_fn=mock_failing_task,
        concurrency=5,
        total_requests=10,
    )

    assert result.failed_requests == 10
    assert result.error_rate == 1.0
    assert result.passes_slo() is False
    assert len(result.errors) > 0
    assert "Connection dropped" in result.errors[0]
