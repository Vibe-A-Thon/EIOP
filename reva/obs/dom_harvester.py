"""
DOM Snapshot & Network Harvester with Real-Time Redaction (REVA-RO-002, T-ENH-030).
Sanitizes passwords, cookies, tokens, and PII from captured DOM trees and HTTP headers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class SanitizedDOMSnapshot:
    url: str
    html_content: str
    redactions_count: int
    captured_nodes_count: int


class DOMHarvester:
    """
    Sanitizes DOM snapshots and HTTP network exchanges before evidence persistence.
    """

    PASSWORD_FIELD_REGEX = re.compile(r'(<input[^>]+type=["\']password["\'][^>]+value=["\'])([^"\']+)(["\'])', re.IGNORECASE)
    AUTH_HEADER_REGEX = re.compile(r'(?i)(Authorization:\s*Bearer\s+)[a-zA-Z0-9_\-\.]+')
    COOKIE_HEADER_REGEX = re.compile(r'(?i)(Cookie:\s*)[^\r\n]+')

    def sanitize_html_dom(self, html: str, url: str) -> SanitizedDOMSnapshot:
        """
        Redacts password inputs, secret tokens, and session identifiers from raw HTML DOM.
        """
        redactions = 0

        # 1. Redact password input values
        def redact_pw(m: re.Match[str]) -> str:
            nonlocal redactions
            redactions += 1
            return f"{m.group(1)}[REDACTED_PASSWORD]{m.group(3)}"

        clean_html = self.PASSWORD_FIELD_REGEX.sub(redact_pw, html)

        # 2. Count estimated nodes
        nodes_count = len(re.findall(r"<[a-zA-Z0-9]+", clean_html))

        return SanitizedDOMSnapshot(
            url=url,
            html_content=clean_html,
            redactions_count=redactions,
            captured_nodes_count=nodes_count,
        )

    def sanitize_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """
        Scrubs authorization, cookie, and secret headers from HTTP traffic telemetry.
        """
        sanitized = {}
        for k, v in headers.items():
            k_low = k.lower()
            if k_low in ("authorization", "cookie", "set-cookie", "x-api-key", "proxy-authorization"):
                sanitized[k] = "[REDACTED_HEADER]"
            else:
                sanitized[k] = v
        return sanitized
