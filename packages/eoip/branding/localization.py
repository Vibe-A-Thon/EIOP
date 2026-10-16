"""Localization packs: strings, formats, RTL (SR-WL-006).

A localization pack carries UI string overrides, date/number formats, an
RTL flag, and a glossary for terminology translation. Packs are supplied
by partners and validated on registration. Locale fallback is a simple
chain (exact locale → language-only → pack default).

Machine-translation quality assurance and glossary enforcement in
deployed UIs are UI concerns; this module is the data model + resolution.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

_LOCALE_RE = __import__("re").compile(r"^[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")


class DateNumberFormats(BaseModel):
    model_config = ConfigDict(extra="forbid")

    date_format: str = "YYYY-MM-DD"
    time_format: str = "HH:mm:ss"
    datetime_format: str | None = None
    number_decimal: str = "."
    number_thousands: str = ","
    currency_code: str = Field(default="USD", min_length=3, max_length=3)
    first_day_of_week: int = Field(default=1, ge=0, le=6, description="0 = Sunday")


class LocalizationPack(BaseModel):
    """One locale's strings and formats for a tenant (SR-WL-006)."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="URN, e.g. urn:eoip:branding:locale:<locale>")
    tenant_id: str = Field(min_length=1)
    locale: str = Field(description="BCP-47-ish tag, e.g. 'fr-CA'")
    rtl: bool = False
    strings: dict[str, str] = Field(default_factory=dict, description="message-key -> localized text")
    formats: DateNumberFormats = Field(default_factory=DateNumberFormats)
    glossary: dict[str, str] = Field(default_factory=dict, description="source term -> localized term")

    @field_validator("id")
    @classmethod
    def _urn(cls, value: str) -> str:
        if not value.startswith("urn:eoip:branding:locale:"):
            raise ValueError("locale pack id must be urn:eoip:branding:locale:<slug>")
        return value

    @field_validator("locale")
    @classmethod
    def _locale_tag(cls, value: str) -> str:
        if not _LOCALE_RE.match(value):
            raise ValueError(f"invalid locale tag {value!r}")
        return value

    def message(self, key: str) -> str | None:
        return self.strings.get(key)


class LocalizationRegistry:
    """Per-tenant locale resolution with fallback chain (SR-WL-006)."""

    def __init__(self) -> None:
        self._packs: dict[tuple[str, str], LocalizationPack] = {}

    def register(self, pack: LocalizationPack) -> None:
        self._packs[(pack.tenant_id, pack.locale.lower())] = pack

    def resolve(self, tenant_id: str, locale: str) -> LocalizationPack | None:
        """Exact locale, then language-only, then any pack for the tenant."""
        key = locale.lower()
        if (tenant_id, key) in self._packs:
            return self._packs[(tenant_id, key)]
        language = key.split("-", 1)[0]
        if (tenant_id, language) in self._packs:
            return self._packs[(tenant_id, language)]
        for (tid, _), pack in self._packs.items():
            if tid == tenant_id:
                return pack
        return None

    def message(self, tenant_id: str, locale: str, key: str, default: str | None = None) -> str | None:
        pack = self.resolve(tenant_id, locale)
        if pack is None:
            return default
        return pack.message(key) or default
