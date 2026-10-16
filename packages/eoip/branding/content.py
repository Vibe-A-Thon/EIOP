"""Custom legal and onboarding content records (SR-WL-007).

Tenants supply their own terms-of-service, privacy notices, welcome
tours, and help links so a white-label deployment carries the partner's
legal identity, not the vendor's. Records are versioned: acceptance is
pinned to a specific version elsewhere (ADR-gated; acceptance tracking
lives in a future consent/compliance store).

Content bodies are storage keys (object store) or inline markdown —
this module validates structure, not legal text.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class LegalContentKind(str, Enum):
    TERMS_OF_SERVICE = "terms_of_service"
    PRIVACY_NOTICE = "privacy_notice"
    COOKIE_NOTICE = "cookie_notice"
    ACCEPTABLE_USE = "acceptable_use"
    WELCOME_TOUR = "welcome_tour"
    HELP_LINK = "help_link"
    ONBOARDING_DOC = "onboarding_doc"


class LegalContentRecord(BaseModel):
    """A versioned legal/onboarding content item for a tenant (SR-WL-007)."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="URN, e.g. urn:eoip:branding:legal:<slug>")
    tenant_id: str = Field(min_length=1)
    kind: LegalContentKind
    title: str = Field(min_length=1, max_length=256)
    version: str = Field(default="1.0.0")
    body_markdown: str | None = None
    body_key: str | None = Field(default=None, description="Object-storage key when the body is too large to inline")
    url: str | None = Field(default=None, description="External URL (e.g. help links)")
    published: bool = False
    required: bool = Field(default=False, description="Must be accepted before product use")

    @field_validator("id")
    @classmethod
    def _urn(cls, value: str) -> str:
        if not value.startswith("urn:eoip:branding:legal:"):
            raise ValueError("legal record id must be urn:eoip:branding:legal:<slug>")
        return value

    @field_validator("url")
    @classmethod
    def _url_scheme(cls, value: str | None) -> str | None:
        if value is not None and not value.startswith(("https://", "mailto:")):
            raise ValueError("url must be https:// or mailto:")
        return value

    def body(self) -> str | None:
        """Inline markdown, or None when the body lives in object storage (body_key)."""
        return self.body_markdown


class LegalContentRegistry:
    """Per-tenant legal/onboarding content lookup (SR-WL-007)."""

    def __init__(self) -> None:
        self._records: dict[tuple[str, str], LegalContentRecord] = {}

    def register(self, record: LegalContentRecord) -> None:
        self._records[(record.tenant_id, record.id)] = record

    def published(self, tenant_id: str, kind: LegalContentKind | None = None) -> list[LegalContentRecord]:
        records = [r for (tid, _), r in self._records.items() if tid == tenant_id and r.published]
        if kind is not None:
            records = [r for r in records if r.kind == kind]
        return sorted(records, key=lambda r: (r.kind.value, r.version))

    def required_pending(self, tenant_id: str) -> list[LegalContentRecord]:
        """Published records marked required — acceptance tracking is ADR-gated."""
        return [r for r in self.published(tenant_id) if r.required]
