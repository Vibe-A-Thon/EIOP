"""API Functional Test Suite: Graph Store, Schema, and Query Engine."""

from __future__ import annotations

import pytest


@pytest.mark.api
class TestGraphAndQueryAPI:
    """Functional tests for graph operations and queries."""

    def test_graph_backend_status(self, admin_client):
        """Verify graph backend inspection endpoint returns operational status."""
        response = admin_client.get("/graph/backend")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        assert "active_backend" in data or "configured_backend" in data

    def test_schema_metadata_retrieval(self, admin_client):
        """Verify graph schema endpoint returns vertex labels and edge types."""
        response = admin_client.get("/graph/schema")
        assert response.status_code == 200
        data = response.json()
        assert "vertex_labels" in data or "domains" in data or "schema_version" in data

    def test_query_history_retrieval(self, analyst_client):
        """Verify query history endpoint returns user or tenant query logs."""
        response = analyst_client.get("/query/history")
        assert response.status_code in (200, 204)
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, (dict, list))
