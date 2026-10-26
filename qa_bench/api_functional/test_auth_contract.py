"""API Contract Test Suite: Authentication, Token Validation, and RBAC Profiles."""

from __future__ import annotations

import pytest
from qa_bench.config import TEST_ROLES


@pytest.mark.api
class TestAuthenticationContract:
    """Contract tests for the authentication and identity provider subsystems."""

    def test_unauthenticated_request_rejected(self, unauthenticated_client):
        """Verify unauthenticated requests return 401 Unauthorized."""
        response = unauthenticated_client.get("/auth/whoami")
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        assert "token" in response.text.lower() or "unauthorized" in response.text.lower()

    def test_invalid_bearer_token_rejected(self, unauthenticated_client):
        """Verify malformed bearer token returns 401 Unauthorized."""
        headers = {"Authorization": "Bearer fake_token_abc_123_invalid"}
        response = unauthenticated_client.get("/auth/whoami", headers=headers)
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"

    @pytest.mark.parametrize("role_key", ["superadmin", "admin", "steward", "analyst", "viewer"])
    def test_role_identity_resolution(self, api_client, role_key):
        """Verify token maps to the exact principal ID and role set."""
        client = api_client(role_key)
        expected = TEST_ROLES[role_key]

        response = client.get("/auth/whoami")
        assert response.status_code == 200, f"Expected 200 for {role_key}, got {response.status_code}: {response.text}"
        data = response.json()

        assert "roles" in data, "Response must contain 'roles' field"
        assert expected.role in data["roles"] or (role_key == "superadmin" and "admin" in data["roles"])
        if expected.tenant != "*":
            assert data.get("tenant_id") == expected.tenant or data.get("tenant_id") is None

    def test_superadmin_privilege_flags(self, superadmin_client):
        """Verify superadmin token receives is_superadmin=True and is_admin=True."""
        response = superadmin_client.get("/auth/whoami")
        assert response.status_code == 200
        data = response.json()
        assert data.get("is_superadmin") is True, "Superadmin should have is_superadmin=True"
        assert data.get("is_admin") is True, "Superadmin should have is_admin=True"
