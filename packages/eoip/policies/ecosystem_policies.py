"""Ecosystem policies: contribution, vulnerability disclosure, ownership, and anti-leak guards (CRA-039.5)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


class CustomerDataLeakViolationError(Exception):
    """Raised when an example or marketplace submission contains customer proprietary models or data."""


@dataclass
class PolicySummary:
    policy_id: str
    title: str
    status: str
    summary: str


class EcosystemPolicyRegistry:
    """Central policy definitions for developer contributions, vulnerability reporting, and IP protection."""

    CONTRIBUTION_POLICY = {
        "policy_id": "POL-CONTRIB-001",
        "title": "Developer Contribution & Licensing Policy",
        "status": "ACTIVE",
        "rules": [
            "All contributors must execute the EOIP Contributor License Agreement (CLA).",
            "Proprietary semantic core modules (packages/eoip/ontology, packages/eoip/actions) are closed to unauthorized external derivative re-licensing.",
            "Plugins and external connectors remain under contributor copyright subject to SDK compatibility terms.",
            "Submissions must pass automated conformance tests before inclusion in the marketplace.",
        ],
    }

    VULNERABILITY_DISCLOSURE_POLICY = {
        "policy_id": "POL-CVD-001",
        "title": "Coordinated Vulnerability Disclosure (CVD)",
        "status": "ACTIVE",
        "contact": "security@eoip.internal",
        "embargo_days": 90,
        "rules": [
            "Vulnerabilities must be reported confidentially without public disclosure during the 90-day embargo.",
            "Reporters are eligible for recognition upon verification and remediation.",
            "Zero-day exploits against active customer deployments are prohibited.",
        ],
    }

    MARKETPLACE_OWNERSHIP_POLICY = {
        "policy_id": "POL-MKT-OWN-001",
        "title": "Marketplace IP & Content Governance",
        "status": "ACTIVE",
        "rules": [
            "Marketplace submissions must never embed customer schemas, proprietary ontologies, or internal graphs.",
            "Examples must use synthetic data only (e.g. example.com, Acme Corp).",
            "Plugins requesting unapproved high-privilege scopes will be rejected during certification.",
        ],
    }

    @classmethod
    def get_all_policies(cls) -> list[dict[str, Any]]:
        return [
            cls.CONTRIBUTION_POLICY,
            cls.VULNERABILITY_DISCLOSURE_POLICY,
            cls.MARKETPLACE_OWNERSHIP_POLICY,
        ]


class CustomerContentSanitizer:
    """Validates public examples and sample packages to guarantee zero customer proprietary model leaks."""

    # Patterns indicating customer data or proprietary leaks
    CUSTOMER_INDICATORS = [
        re.compile(r"tenant[-_]id\s*[:=]\s*['\"]?(cust[-_]|client[-_]|enterprise[-_][0-9a-f]{8})", re.IGNORECASE),
        re.compile(r"@(?!example\.com|eoip\.io)[a-zA-Z0-9_\-\.]+\.(com|org|net|internal|corp)", re.IGNORECASE),
        re.compile(r"(mongodb|postgres|snowflake|mysql):\/\/[^:\/\s]+:[^@\/\s]+@", re.IGNORECASE),
        re.compile(r"BEGIN\s+(RSA|EC|PRIVATE)\s+KEY", re.IGNORECASE),
        re.compile(r"urn:customer:[a-zA-Z0-9_\-\.:]+", re.IGNORECASE),
    ]

    @classmethod
    def validate_public_example(cls, content: str, source_label: str = "example") -> bool:
        """Inspects text content of examples, plugins, or docs. Raises if customer leaks found."""
        for pattern in cls.CUSTOMER_INDICATORS:
            match = pattern.search(content)
            if match:
                raise CustomerDataLeakViolationError(
                    f"Publication blocked: {source_label} contains forbidden customer data or private credential: '{match.group(0)[:30]}...'"
                )
        return True
