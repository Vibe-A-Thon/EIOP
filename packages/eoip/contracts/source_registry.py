"""Source registry and capability contracts (G2-T0004/G2-T0005)."""

from __future__ import annotations

from typing import Any, Literal

from eoip.contracts.source_event import utc_now_iso
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

SourceType = Literal[
    "api_portal",
    "confluence",
    "datadog",
    "documents",
    "figma",
    "fortuna",
    "github",
    "gitlab",
    "grafana",
    "jira",
    "kibana",
    "local_files",
    "qtest",
    "rally",
    "servicenow",
    "web",
]


class SourceCapabilities(BaseModel):
    model_config = ConfigDict(extra="forbid")

    baseline: bool = True
    polling: bool = False
    webhooks: bool = False
    deletion_events: bool = False
    permission_events: bool = False
    discovery: bool = True
    reconciliation: bool = False
    replay: bool = True


class SourceRegistryEntry(BaseModel):
    """Non-secret source configuration persisted by the local control plane."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"] = "1.0"
    source_id: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
    source_type: SourceType
    name: str = Field(min_length=1, max_length=256)
    base_url: str | None = Field(default=None, max_length=2048)
    enabled: bool = True
    capabilities: SourceCapabilities = Field(default_factory=SourceCapabilities)
    config: dict[str, Any] = Field(default_factory=dict)
    secret_refs: dict[str, str] = Field(default_factory=dict)
    created_at: str = Field(default_factory=utc_now_iso)
    updated_at: str = Field(default_factory=utc_now_iso)

    @field_validator("config")
    @classmethod
    def reject_inline_secrets(cls, value: dict[str, Any]) -> dict[str, Any]:
        secret_markers = ("password", "secret", "token", "credential", "api_key", "private_key")
        offenders = [key for key in value if any(marker in key.casefold() for marker in secret_markers)]
        if offenders:
            raise ValueError("config contains secret-like keys; use secret_refs")
        return value

    @field_validator("secret_refs")
    @classmethod
    def require_opaque_secret_references(cls, value: dict[str, str]) -> dict[str, str]:
        for key, reference in value.items():
            if not key.strip() or not reference.startswith(("env://", "file://", "vault://")):
                raise ValueError("secret_refs must use env://, file://, or vault:// references")
        return value

    @model_validator(mode="after")
    def require_remote_url(self) -> SourceRegistryEntry:
        if self.source_type not in {"local_files", "documents"} and not self.base_url:
            raise ValueError(f"base_url is required for {self.source_type}")
        return self


class SourceCheckpoint(BaseModel):
    """Committed resume point; only advanced after successful mutation."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"] = "1.0"
    source_id: str = Field(min_length=1, max_length=128)
    cursor: str = Field(min_length=1, max_length=4096)
    last_event_id: str | None = Field(default=None, max_length=512)
    committed_at: str = Field(default_factory=utc_now_iso)
    baseline_complete: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)
