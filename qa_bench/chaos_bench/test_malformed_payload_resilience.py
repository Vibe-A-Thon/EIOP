"""Chaos & Fault Injection Suite: Malformed Payloads and Protocol Abuse."""

from __future__ import annotations

import pytest


@pytest.mark.chaos
class TestChaosMalformedPayloads:
    """Chaos tests ensuring server stability when bombarded with corrupt or malformed inputs."""

    def test_truncated_json_payload(self, admin_client):
        """Verify truncated JSON returns 400/422 without server panic."""
        headers = {"Content-Type": "application/json"}
        # Truncated JSON
        corrupt_body = b'{"query": "find all", "limit": '
        response = admin_client.post("/query/eql", content=corrupt_body, headers=headers)
        assert response.status_code in (400, 422)

    def test_deeply_nested_json_object(self, admin_client):
        """Verify extremely deep nested JSON payload does not cause stack overflow recursion crash."""
        deep_obj: dict = {"val": "bottom"}
        for _ in range(60):
            deep_obj = {"nested": deep_obj}

        response = admin_client.post("/query/eql", json=deep_obj)
        assert response.status_code != 500

    def test_unsupported_content_type_handling(self, admin_client):
        """Verify server returns 415 or 422 on unsupported content types."""
        headers = {"Content-Type": "application/x-custom-binary"}
        response = admin_client.post("/query/eql", content=b"\x00\xFF\xAA\x55", headers=headers)
        assert response.status_code in (415, 422, 400)
