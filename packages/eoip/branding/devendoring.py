"""De-vendoring checklist data model (SR-WL-004, partial).

Lists the identifier *classes* a deployment must be able to override to
remove vendor branding: UI strings and logos, documentation, CLI binary
name, container/image names, package names, API hostnames, error pages,
and installers. The "powered by" attribution line is a licensed toggle.

This module is the checklist/override model only — the actual build-time
renaming of binaries, images and installers is External gate: it happens
in packaging/release tooling outside the runtime package.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class IdentifierClass(str, Enum):
    UI_STRINGS_AND_LOGOS = "ui_strings_and_logos"
    DOCUMENTATION = "documentation"
    CLI_BINARY_NAME = "cli_binary_name"
    CONTAINER_IMAGE_NAMES = "container_image_names"
    PACKAGE_NAMES = "package_names"
    API_HOSTNAMES = "api_hostnames"
    ERROR_PAGES = "error_pages"
    INSTALLERS = "installers"


class IdentifierOverride(BaseModel):
    """One override: replace the default vendor identifier with a tenant one."""

    model_config = ConfigDict(extra="forbid")

    identifier_class: IdentifierClass
    default_value: str = Field(min_length=1)
    override_value: str = Field(min_length=1)
    external_gate: bool = Field(
        default=False,
        description="True when the override is applied outside the runtime "
        "(build/release tooling) and this record only tracks intent",
    )


class PoweredByToggle(BaseModel):
    """Licensed 'powered by' attribution toggle (SR-WL-004)."""

    model_config = ConfigDict(extra="forbid")

    licensed: bool = False
    text: str = "Powered by EOIP"
    license_ref: str | None = None


class DeVendoringChecklist(BaseModel):
    """De-vendoring checklist for one deployment/tenant (SR-WL-004)."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="URN, e.g. urn:eoip:branding:devendor:<slug>")
    tenant_id: str = Field(min_length=1)
    overrides: list[IdentifierOverride] = Field(default_factory=list)
    powered_by: PoweredByToggle = Field(default_factory=PoweredByToggle)

    @field_validator("id")
    @classmethod
    def _urn(cls, value: str) -> str:
        if not value.startswith("urn:eoip:branding:devendor:"):
            raise ValueError("checklist id must be urn:eoip:branding:devendor:<slug>")
        return value

    def coverage(self) -> dict[str, bool]:
        """True for each identifier class that has an override recorded."""
        return {cls.value: any(o.identifier_class == cls for o in self.overrides) for cls in IdentifierClass}

    def complete(self) -> bool:
        """All identifier classes have at least one override recorded.

        Note: for ``external_gate`` classes this records intent only — the
        actual binary/image/installer rename is External gate (release
        tooling), so completeness here is a tracking statement, not proof
        the shipped artifacts are de-vendored.
        """
        return all(self.coverage().values())
