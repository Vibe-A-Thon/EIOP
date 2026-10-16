"""Package manifest contracts for the EOIP marketplace (GAP-MKT-001, GAP-MKT-002).

A package manifest describes an installable extension: name, SemVer version,
platform compatibility, provided capabilities (ontologies, mappings, query
templates, validators, agent workflows, dashboards), and dependency version
ranges.
"""

from __future__ import annotations

import re
from enum import Enum

from pydantic import BaseModel, Field, field_validator

_SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


class CapabilityKind(str, Enum):
    ONTOLOGIES = "ontologies"
    MAPPINGS = "mappings"
    QUERY_TEMPLATES = "query_templates"
    VALIDATORS = "validators"
    AGENT_WORKFLOWS = "agent_workflows"
    DASHBOARDS = "dashboards"


class PackageDependency(BaseModel):
    """A dependency on another EOIP package with a SemVer range (GAP-MKT-004)."""

    name: str = Field(min_length=1)
    range: str = Field(min_length=1, description="SemVer range, e.g. '>=1.0.0,<2.0.0'")

    @field_validator("range")
    @classmethod
    def _check_range(cls, value: str) -> str:
        from eoip.marketplace.semver import parse_range

        parse_range(value)
        return value


class PackageManifest(BaseModel):
    """Manifest embedded in every .eoipkg archive as ``manifest.json``."""

    id: str = Field(description="Stable package ID, e.g. urn:eoip:marketplace:package:<name>")
    name: str = Field(min_length=1, max_length=128, pattern=r"^[a-z0-9][a-z0-9_-]*$")
    version: str
    description: str = ""
    author: str = ""
    platforms: list[str] = Field(default_factory=lambda: ["any"])
    provides: dict[CapabilityKind, list[str]] = Field(default_factory=dict)
    dependencies: list[PackageDependency] = Field(default_factory=list)

    @field_validator("version")
    @classmethod
    def _check_version(cls, value: str) -> str:
        from eoip.marketplace.semver import parse_version

        parse_version(value)
        return value

    @field_validator("id")
    @classmethod
    def _check_id(cls, value: str) -> str:
        if not value.startswith("urn:eoip:marketplace:package:"):
            raise ValueError("package id must start with urn:eoip:marketplace:package:")
        return value

    def satisfies_platform(self, platform: str) -> bool:
        return "any" in self.platforms or platform in self.platforms
