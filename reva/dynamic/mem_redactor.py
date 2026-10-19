"""
Dynamic Memory Dump Slice Redactor (REVA-DI-003, T-ENH-027).
Bounds memory read sizes to <= 64 KiB and sanitizes confidential credentials from memory dumps.
"""

from __future__ import annotations

import re
from typing import Tuple

from reva.core.errors import RevaResourceLimitError


class MemorySliceRedactor:
    """
    Sanitizes dynamic memory slices inspected during controlled debugging.
    """

    MAX_SLICE_BYTES = 64 * 1024  # 64 KiB cap

    # Binary credential patterns
    PATTERNS = [
        re.compile(rb"AKIA[0-9A-Z]{16}"),
        re.compile(rb"eyJ[a-zA-Z0-9_\-]{10,}\.[a-zA-Z0-9_\-]{10,}\.[a-zA-Z0-9_\-]{10,}"),
        re.compile(rb"-----BEGIN (?:RSA )?PRIVATE KEY-----"),
    ]

    def sanitize_slice(self, raw_bytes: bytes) -> Tuple[bytes, int]:
        """
        Bounds size and scrubs credentials from raw memory dump.
        Returns (scrubbed_bytes, redactions_count).
        """
        if len(raw_bytes) > self.MAX_SLICE_BYTES:
            raise RevaResourceLimitError(
                f"Memory slice exceeds maximum allowed size of {self.MAX_SLICE_BYTES} bytes."
            )

        result = bytearray(raw_bytes)
        count = 0
        for pat in self.PATTERNS:
            for match in pat.finditer(raw_bytes):
                start, end = match.span()
                result[start:end] = b"X" * (end - start)
                count += 1

        return bytes(result), count
