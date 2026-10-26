"""End-to-End Enterprise Workflow Scenario."""

from __future__ import annotations

import pytest


@pytest.mark.e2e
class TestFullLifecycleWorkflow:
    """Verifies end-to-end user workflows spanning auth, schema inspection, and querying."""

    def test_complete_enterprise_investigation_lifecycle(self, admin_client):
        """Workflow: Authenticate -> Verify Schema -> Inspect Backend -> Query Graph -> Verify Identity."""
        # 1. Identity Verification
        auth_res = admin_client.get("/auth/whoami")
        assert auth_res.status_code == 200
        user = auth_res.json()
        assert "admin" in user["roles"]

        # 2. Schema Discovery
        schema_res = admin_client.get("/graph/schema")
        assert schema_res.status_code == 200

        # 3. Backend Operational Check
        backend_res = admin_client.get("/graph/backend")
        assert backend_res.status_code == 200

        # 4. Query Execution History Check
        history_res = admin_client.get("/query/history")
        assert history_res.status_code in (200, 204)
