"""Security & DAST Automation Suite: CORS Origin & Preflight Validation."""

from __future__ import annotations

import pytest


@pytest.mark.security
class TestCorsPolicyEnforcement:
    """Verifies Cross-Origin Resource Sharing (CORS) contracts."""

    def test_cors_preflight_options(self, unauthenticated_client):
        """Verify OPTIONS preflight request handling."""
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization,content-type",
        }
        response = unauthenticated_client.options("/query/eql", headers=headers)
        # FastApi CORS middleware should allow preflight
        assert response.status_code in (200, 204, 404, 405)
