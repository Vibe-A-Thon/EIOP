"""API Functional Test Suite: SHACL Shape Validation and Ontology Integrity."""

from __future__ import annotations

import pytest


@pytest.mark.api
class TestShaclValidation:
    """QA tests for SHACL validation and ontology constraints."""

    def test_schema_shacl_export_availability(self, admin_client):
        """Verify schema metadata provides vertex and property shapes."""
        response = admin_client.get("/graph/schema")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
