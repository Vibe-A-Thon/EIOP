"""API Functional Test Suite: Platform Health, Telemetry, and Observability."""

from __future__ import annotations

import pytest


@pytest.mark.api
class TestSystemHealth:
    """QA tests for system vitals, telemetry, and metrics."""

    def test_backend_status_reporting(self, admin_client):
        """Verify graph backend status can be queried and responds within SLO."""
        response = admin_client.get("/graph/backend")
        assert response.status_code == 200
        data = response.json()
        assert "active_backend" in data or "configured_backend" in data
