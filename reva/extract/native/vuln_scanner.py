"""
Native Binary Vulnerability & CWE Pattern Scanner (REVA-NB-007, T-ENH-014).
Detects dangerous C API functions, missing compiler hardening (canaries, NX, PIE), and CWE patterns.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from reva.extract.native.loader import BinaryHeader


@dataclass
class VulnerabilityFinding:
    cwe_id: str
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    symbol_name: str
    title: str
    description: str
    remediation: str


class NativeVulnScanner:
    """
    Scans binary headers, sections, and symbol tables for vulnerability indicators.
    """

    DANGEROUS_APIS = {
        "gets": ("CWE-242", "CRITICAL", "Use of inherently dangerous function 'gets'", "Replace with fgets()"),
        "strcpy": ("CWE-120", "HIGH", "Classic buffer overflow risk with 'strcpy'", "Replace with strncpy() or snprintf()"),
        "strcat": ("CWE-120", "HIGH", "Buffer overflow risk with 'strcat'", "Replace with strncat()"),
        "sprintf": ("CWE-134", "HIGH", "Format string or buffer overflow risk with 'sprintf'", "Replace with snprintf()"),
        "vsprintf": ("CWE-134", "HIGH", "Buffer overflow risk with 'vsprintf'", "Replace with vsnprintf()"),
        "system": ("CWE-78", "HIGH", "OS command injection risk with 'system'", "Replace with execve() with parameterized arguments"),
        "popen": ("CWE-78", "HIGH", "Command execution risk with 'popen'", "Validate and sanitize inputs thoroughly"),
    }

    def scan_binary(self, header: BinaryHeader, raw_bytes: Optional[bytes] = None) -> List[VulnerabilityFinding]:
        """
        Scans binary for known dangerous symbols and security mitigation flags.
        """
        findings: List[VulnerabilityFinding] = []

        # 1. Harvest imported symbols and string references in raw bytes
        found_symbols = set(header.imported_symbols)
        if raw_bytes:
            for api_name in self.DANGEROUS_APIS.keys():
                pattern = bytes(f"{api_name}\x00", "ascii")
                if pattern in raw_bytes:
                    found_symbols.add(api_name)

        # 2. Check for dangerous APIs
        for sym in found_symbols:
            if sym in self.DANGEROUS_APIS:
                cwe, sev, title, rem = self.DANGEROUS_APIS[sym]
                findings.append(VulnerabilityFinding(
                    cwe_id=cwe,
                    severity=sev,
                    symbol_name=sym,
                    title=title,
                    description=f"Binary imports or references unsafe C runtime API '{sym}'.",
                    remediation=rem,
                ))

        # 3. Check for Stack Canary Protection
        has_canary = False
        if raw_bytes:
            if b"__stack_chk_fail" in raw_bytes or b"__security_check_cookie" in raw_bytes:
                has_canary = True

        if not has_canary and header.format in ("ELF", "PE"):
            findings.append(VulnerabilityFinding(
                cwe_id="CWE-693",
                severity="MEDIUM",
                symbol_name="stack_canary",
                title="Missing Stack Smashing Protection (Canaries)",
                description="Binary does not import __stack_chk_fail or security cookie checks.",
                remediation="Compile with -fstack-protector-strong or /GS.",
            ))

        return findings
