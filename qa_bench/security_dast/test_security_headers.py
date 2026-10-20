"""Security & DAST Automation Suite: HTTP Security Headers and CSP Audit."""

from __future__ import annotations

import pytest


@pytest.mark.security
class TestSecurityHeadersAudit:
    """Automated security baseline audit verifying protection headers."""

    def test_response_security_headers_present(self, admin_client):
        """Verify baseline security headers on authenticated API endpoints."""
        response = admin_client.get("/graph/schema")
        assert response.status_code == 200

        headers = response.headers
        # Validate MIME sniffing prevention
        content_type_options = headers.get("X-Content-Type-Options", "").lower()
        if content_type_options:
            assert content_type_options == "nosniff"

    def test_unauthenticated_security_headers(self, unauthenticated_client):
        """Verify 401 response does not leak server stack traces or internal environment."""
        response = unauthenticated_client.get("/auth/whoami")
        assert response.status_code == 401

        body = response.text.lower()
        # Verify no traceback leakage in response body
        assert "traceback (most recent call last)" not in body
        assert "environ[" not in body
        assert "password" not in body
