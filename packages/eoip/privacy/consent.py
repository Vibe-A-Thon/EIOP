"""Purpose and consent tracking (SR-PRV-004, partial).

Records the declared processing purpose for data collection and the
data subject's consent grants/revocations, per tenant. The engine answers
"may this source be used for this purpose right now?" — purpose
limitation is enforced here so query/policy layers can reject uses that
lack a valid grant.

Granular per-field consent, consent receipt generation to the subject,
and purpose-registry governance workflows are ADR-gated (they need a
compliance-store and notification decision). DP aggregates (SR-PRV-005)
are likewise ADR-gated.
"""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Purpose(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="URN, e.g. urn:eoip:privacy:purpose:<slug>")
    code: str = Field(min_length=1, pattern=r"^[a-z0-9][a-z0-9_-]*$")
    description: str = ""
    requires_consent: bool = True
    sensitivity: list[str] = Field(default_factory=list, description="Sensitivity labels this purpose may process")

    @field_validator("id")
    @classmethod
    def _urn(cls, value: str) -> str:
        if not value.startswith("urn:eoip:privacy:purpose:"):
            raise ValueError("purpose id must be urn:eoip:privacy:purpose:<slug>")
        return value


class ConsentRecord(BaseModel):
    """A consent grant or revocation by a data subject (SR-PRV-004)."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="URN, e.g. urn:eoip:privacy:consent:<slug>")
    tenant_id: str = Field(min_length=1)
    subject_id: str = Field(min_length=1)
    purpose_code: str = Field(min_length=1)
    granted: bool
    recorded_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    expires_at: str | None = None
    source: str | None = Field(default=None, description="Narrow the grant to one data source; None = all sources")

    @field_validator("id")
    @classmethod
    def _urn(cls, value: str) -> str:
        if not value.startswith("urn:eoip:privacy:consent:"):
            raise ValueError("consent id must be urn:eoip:privacy:consent:<slug>")
        return value


def _parse_ts(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=UTC)


class ConsentRegistry:
    """Stores purposes and consent records; enforces purpose limitation (SR-PRV-004)."""

    def __init__(self) -> None:
        self._purposes: dict[str, Purpose] = {}
        self._consents: list[ConsentRecord] = []

    def register_purpose(self, purpose: Purpose) -> None:
        self._purposes[purpose.code] = purpose

    def record(self, consent: ConsentRecord) -> None:
        if consent.purpose_code not in self._purposes:
            raise KeyError(f"unknown purpose {consent.purpose_code}")
        self._consents.append(consent)

    def latest(self, subject_id: str, purpose_code: str, source: str | None = None) -> ConsentRecord | None:
        """Latest consent record for the subject/purpose, optionally source-scoped."""
        matches = [
            c
            for c in self._consents
            if c.subject_id == subject_id
            and c.purpose_code == purpose_code
            and (c.source is None or source is None or c.source == source)
        ]
        if not matches:
            return None
        return matches[-1]  # last record wins (revocation overrides grant)

    def allowed(self, subject_id: str, purpose_code: str, source: str | None = None, now: datetime | None = None) -> bool:
        """Purpose limitation check: grant present, unexpired, and not revoked."""
        purpose = self._purposes.get(purpose_code)
        if purpose is None:
            return False
        if not purpose.requires_consent:
            return True
        consent = self.latest(subject_id, purpose_code, source)
        if consent is None or not consent.granted:
            return False
        now = now or datetime.now(UTC)
        return not (consent.expires_at and _parse_ts(consent.expires_at) <= now)
