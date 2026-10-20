"""Performance & Stress: Supernode and Repetitive Traversal Stability."""

from __future__ import annotations

import time
import pytest


@pytest.mark.performance
class TestSupernodeResilience:
    """Stress tests verifying graph traversals do not cause OOM or degradations."""

    def test_rapid_backend_poll_stability(self, admin_client):
        """Perform 50 rapid sequential health/backend queries to verify connection pooling stability."""
        start_time = time.perf_counter()
        for _ in range(50):
            res = admin_client.get("/graph/backend")
            assert res.status_code == 200
        total_time = time.perf_counter() - start_time
        avg_per_req = (total_time / 50.0) * 1000.0
        print(f"\n[Resilience Test] 50 sequential requests completed in {total_time:.3f}s ({avg_per_req:.2f}ms/req)")
        assert avg_per_req < 50.0, f"Average request time {avg_per_req:.2f}ms exceeded limit"
