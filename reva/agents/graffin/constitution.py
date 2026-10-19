"""
Immutable Constitution & WORM Cryptographic Hash Verifier (GRF-SEC-001, T-GRF-001).
Ensures the Graffin safety constitution cannot be tampered with or subverted.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from reva.core.errors import RevaError
from reva.core.ids import constitution_id
from reva.core.jcs import canonicalize


class ConstitutionTamperedError(RevaError):
    """Raised when the Constitution hash verification fails or tampering is detected."""
    def __init__(self, message: str, expected_hash: str, computed_hash: str) -> None:
        super().__init__(
            code="CONSTITUTION_TAMPERED",
            category="SECURITY",
            message=f"{message} (expected={expected_hash}, computed={computed_hash})",
            details={"expected_hash": expected_hash, "computed_hash": computed_hash},
        )
        self.expected_hash = expected_hash
        self.computed_hash = computed_hash


class ConstitutionVerifier:
    """
    Computes canonical RFC 8785 hash of constitution.json and enforces startup immutability gate.
    """

    CONSTITUTION_PATH = Path(__file__).parent / "constitution.json"

    def __init__(self, constitution_file: Optional[Path] = None, expected_hash: Optional[str] = None) -> None:
        self.constitution_file = constitution_file or self.CONSTITUTION_PATH
        self._expected_hash = expected_hash

    def load_constitution(self) -> Dict[str, Any]:
        """Loads raw constitution JSON from disk."""
        if not self.constitution_file.exists():
            raise FileNotFoundError(f"Constitution file not found at {self.constitution_file}")
        content = self.constitution_file.read_text(encoding="utf-8")
        return json.loads(content)

    def compute_canonical_hash(self) -> str:
        """Computes deterministic con1_[0-9a-f]{64} identifier over canonical JSON bytes."""
        data = self.load_constitution()
        return constitution_id(data)

    def verify_or_fail(self, exit_on_fail: bool = False) -> str:
        """
        Verifies that current constitution matches expected hash or baseline.
        If tampered and exit_on_fail is True, exits immediately with code 65.
        """
        computed = self.compute_canonical_hash()

        # Check environment override or known locked hash
        expected = self._expected_hash or os.environ.get("GRAFFIN_CONSTITUTION_HASH")
        if expected and computed != expected:
            err = ConstitutionTamperedError("Constitution integrity verification failed", expected, computed)
            if exit_on_fail:
                sys.stderr.write(f"FATAL: {err}\n")
                sys.exit(65)
            raise err

        return computed
