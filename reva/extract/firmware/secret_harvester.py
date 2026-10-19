"""
Embedded Secret & Hardcoded Credential Harvester (REVA-FM-002, T-ENH-022).
Scans firmware, container images, and binary blobs for embedded credentials, keys, and tokens.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class HarvestedSecret:
    secret_type: str  # "PRIVATE_KEY", "AWS_ACCESS_KEY", "JWT_TOKEN", "DB_CONNECTION_STRING", "HIGH_ENTROPY_TOKEN"
    offset: int
    redacted_preview: str
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class SecretHarvester:
    """
    Pure-Python static scanner for hardcoded secrets embedded in binary or text streams.
    """

    PATTERNS: List[Tuple[str, re.Pattern[bytes], float]] = [
        ("PRIVATE_KEY", re.compile(rb"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"), 0.99),
        ("AWS_ACCESS_KEY", re.compile(rb"AKIA[0-9A-Z]{16}"), 0.95),
        ("JWT_TOKEN", re.compile(rb"eyJ[a-zA-Z0-9_\-]{10,}\.[a-zA-Z0-9_\-]{10,}\.[a-zA-Z0-9_\-]{10,}"), 0.90),
        ("DB_CONNECTION_STRING", re.compile(rb"(?:postgres|mysql|mongodb|redis)://[a-zA-Z0-9_\-\.]+:[^@\s]+@[a-zA-Z0-9_\-\.]+"), 0.95),
    ]

    def harvest_bytes(self, data: bytes) -> List[HarvestedSecret]:
        secrets: List[HarvestedSecret] = []

        # 1. Regex pattern scans
        for sec_type, pat, conf in self.PATTERNS:
            for match in pat.finditer(data):
                offset = match.start()
                raw_match = match.group(0)
                # Redact preview for safety
                if len(raw_match) > 8:
                    preview = (raw_match[:4] + b"..." + raw_match[-4:]).decode("ascii", errors="replace")
                else:
                    preview = "[REDACTED]"

                secrets.append(HarvestedSecret(
                    secret_type=sec_type,
                    offset=offset,
                    redacted_preview=preview,
                    confidence=conf,
                    metadata={"length": len(raw_match)},
                ))

        return secrets

    def harvest_file(self, file_path: str | Path) -> List[HarvestedSecret]:
        raw = Path(file_path).read_bytes()
        return self.harvest_bytes(raw)
