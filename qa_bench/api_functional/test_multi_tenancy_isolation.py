"""API Functional Test Suite: Multi-Tenant Boundary and Isolation Assurance."""

from __future__ import annotations

import pytest


@pytest.mark.api
class TestMultiTenantIsolation:
    """Verifies isolation of data and permissions between distinct tenants."""

    def test_superadmin_can_access_any_tenant(self, superadmin_client):
        """Verify superadmin with wildcard tenant can query with any X-Tenant-Id."""
        headers = {"X-Tenant-Id": "tenant_alpha"}
        response = superadmin_client.get("/auth/whoami", headers=headers)
        assert response.status_code == 200, f"Superadmin should access tenant_alpha, got {response.status_code}"

    def test_scoped_tenant_admin_forbidden_cross_tenant(self, admin_client):
        """Verify admin scoped to 'default' tenant is forbidden (403) from accessing 'tenant_alpha'."""
        headers = {"X-Tenant-Id": "tenant_alpha"}
        response = admin_client.get("/auth/whoami", headers=headers)
        assert response.status_code == 403, f"Scoped admin must be forbidden (403) on cross-tenant access, got {response.status_code}"

    def test_scoped_tenant_admin_allowed_own_tenant(self, admin_client):
        """Verify admin scoped to 'default' tenant succeeds on own tenant."""
        headers = {"X-Tenant-Id": "default"}
        response = admin_client.get("/auth/whoami", headers=headers)
        assert response.status_code == 200
