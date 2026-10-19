"""
Headless Browser CDP Controller & Domain Fencing (REVA-RO-001, T-ENH-029).
Coordinates Chromium DevTools Protocol (CDP) sessions with strict loopback/domain fencing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from reva.core.errors import RevaSecurityError


@dataclass
class CDPCommand:
    id: int
    method: str
    params: Dict[str, Any] = field(default_factory=dict)


class CDPController:
    """
    Manages headless browser observation with strict loopback domain controls.
    """

    DEFAULT_ALLOWED_DOMAINS = ("127.0.0.1", "localhost", "testapp.local")

    SAFE_CHROMIUM_FLAGS = [
        "--headless=new",
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--remote-debugging-port=9222",
    ]

    def __init__(self, allowed_domains: Optional[List[str]] = None) -> None:
        self.allowed_domains = tuple(allowed_domains) if allowed_domains else self.DEFAULT_ALLOWED_DOMAINS
        self._cmd_seq = 1

    def validate_target_url(self, url: str) -> None:
        """
        Validates that target URL belongs to allowed domains to prevent SSRF and data exfiltration.
        """
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()
        if not hostname:
            raise RevaSecurityError(f"Invalid URL structure: {url}")

        if not any(hostname == allowed or hostname.endswith(f".{allowed}") for allowed in self.allowed_domains):
            raise RevaSecurityError(
                f"Browser CDP domain fencing blocked navigation to untrusted external host: '{hostname}'"
            )

    def build_navigate_command(self, url: str) -> CDPCommand:
        self.validate_target_url(url)
        cmd = CDPCommand(
            id=self._cmd_seq,
            method="Page.navigate",
            params={"url": url},
        )
        self._cmd_seq += 1
        return cmd

    def build_snapshot_command(self) -> CDPCommand:
        cmd = CDPCommand(
            id=self._cmd_seq,
            method="DOMSnapshot.captureSnapshot",
            params={"computedStyles": []},
        )
        self._cmd_seq += 1
        return cmd
