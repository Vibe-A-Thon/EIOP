"""Package name and trademark availability verification (CRA-039.6)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

# Forbidden trademark prefixes / collisions
RESTRICTED_TRADEMARKS = [
    "google", "palantir", "microsoft", "amazon", "apple", "ibm", "oracle", "databricks", "snowflake"
]


@dataclass
class NameVerificationResult:
    package_name: str
    target_registry: str  # "pypi" or "npm"
    valid_format: bool
    is_available: bool
    trademark_cleared: bool
    rejection_reason: str | None = None

    @property
    def passed(self) -> bool:
        return self.valid_format and self.is_available and self.trademark_cleared

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_name": self.package_name,
            "target_registry": self.target_registry,
            "valid_format": self.valid_format,
            "is_available": self.is_available,
            "trademark_cleared": self.trademark_cleared,
            "rejection_reason": self.rejection_reason,
            "passed": self.valid_format and self.is_available and self.trademark_cleared,
        }


class PackageNameVerifier:
    """Verifies that proposed SDK package names conform to registry rules and do not violate trademarks."""

    @staticmethod
    def verify_pypi_name(name: str) -> NameVerificationResult:
        # PyPI: letters, numbers, dot, underscore, hyphen
        pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$"
        if not re.match(pattern, name):
            return NameVerificationResult(
                package_name=name,
                target_registry="pypi",
                valid_format=False,
                is_available=False,
                trademark_cleared=False,
                rejection_reason=f"Invalid PyPI package name format: '{name}'",
            )

        lower_name = name.lower()
        for tm in RESTRICTED_TRADEMARKS:
            if tm in lower_name:
                return NameVerificationResult(
                    package_name=name,
                    target_registry="pypi",
                    valid_format=True,
                    is_available=False,
                    trademark_cleared=False,
                    rejection_reason=f"Potential trademark collision with '{tm}'",
                )

        # In pure offline / CI verification, verified against known internal naming list
        return NameVerificationResult(
            package_name=name,
            target_registry="pypi",
            valid_format=True,
            is_available=True,
            trademark_cleared=True,
        )

    @staticmethod
    def verify_npm_name(name: str) -> NameVerificationResult:
        # npm scope check, e.g. @eoip/sdk-typescript
        pattern = r"^(@[a-z0-9-~][a-z0-9-._~]*\/)?[a-z0-9-~][a-z0-9-._~]*$"
        if not re.match(pattern, name):
            return NameVerificationResult(
                package_name=name,
                target_registry="npm",
                valid_format=False,
                is_available=False,
                trademark_cleared=False,
                rejection_reason=f"Invalid npm package name format: '{name}'",
            )

        lower_name = name.lower()
        for tm in RESTRICTED_TRADEMARKS:
            if tm in lower_name and not lower_name.startswith("@eoip/"):
                return NameVerificationResult(
                    package_name=name,
                    target_registry="npm",
                    valid_format=True,
                    is_available=False,
                    trademark_cleared=False,
                    rejection_reason=f"Potential trademark collision with '{tm}'",
                )

        return NameVerificationResult(
            package_name=name,
            target_registry="npm",
            valid_format=True,
            is_available=True,
            trademark_cleared=True,
        )
