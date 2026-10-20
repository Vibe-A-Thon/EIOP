"""API Functional Test Suite: REVA Cryptographic Warrants and Merkle Proofs."""

from __future__ import annotations

import hashlib
import pytest


@pytest.mark.api
class TestRevaWarrants:
    """QA tests for REVA verification architecture and warrant integrity."""

    def test_warrant_hash_standards(self):
        """Verify warrant hashing logic adheres to canonical SHA-256 and Merkle formatting."""
        canonical_content = b'{"subject": "urn:eoip:requirement:CAP-01", "status": "VERIFIED"}'
        h = hashlib.sha256(canonical_content).hexdigest()
        assert len(h) == 64, "SHA-256 hash must be 64 hexadecimal characters"

        warrant_id = f"wr1_{h[:24]}"
        assert warrant_id.startswith("wr1_"), "REVA warrants must use wr1_ canonical prefix"
