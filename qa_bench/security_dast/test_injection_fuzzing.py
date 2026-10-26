"""Security & DAST Automation Suite: Injection Fuzzing (SQLi, SPARQLi, Path Traversal, XSS)."""

from __future__ import annotations

import urllib.parse
import pytest

ADVERSARIAL_PAYLOADS = [
    # SQLi / Query injection
    "' OR 1=1 --",
    "'; DROP TABLE vertices; --",
    "1 UNION SELECT 1,2,3,4,5",
    "} UNION { ?s ?p ?o . FILTER (1=1) }",
    # Path Traversal
    "../../../../../../../../etc/passwd",
    "..\\..\\..\\..\\windows\\system32\\cmd.exe",
    "/proc/self/environ",
    # XSS Payloads
    "<script>alert(document.cookie)</script>",
    "<img src='x' onerror='alert(1)'>",
    "javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/\"/+/onmouseover=1/+/[*/[]/+alert(1)//'>",
    # Buffer / Format String
    "%s%s%s%s%s%s%s%s%s%s%s%s",
    "A" * 8192,
    "\x00\x01\x02\x03\x04\x05",
]


@pytest.mark.security
class TestInjectionFuzzing:
    """Fuzz testing API parameters against common injection patterns."""

    @pytest.mark.parametrize("payload", ADVERSARIAL_PAYLOADS)
    def test_query_eql_injection_resilience(self, admin_client, payload):
        """Verify adversarial payloads in query endpoint are safely rejected or handled without 500 error."""
        response = admin_client.post("/query/eql", json={"query": payload})
        # Server must not throw 500 Internal Server Error (must be 400, 422, or cleanly return empty)
        assert response.status_code != 500, f"Server crashed with 500 on payload: {payload[:30]!r}"

    @pytest.mark.parametrize("payload", ADVERSARIAL_PAYLOADS)
    def test_entity_id_traversal_resilience(self, admin_client, payload):
        """Verify entity route rejects or 404s on directory traversal attempts."""
        safe_path = urllib.parse.quote(payload, safe="")
        response = admin_client.get(f"/entities/{safe_path}")
        assert response.status_code != 500, f"Server crashed with 500 on entity traversal: {payload[:30]!r}"

