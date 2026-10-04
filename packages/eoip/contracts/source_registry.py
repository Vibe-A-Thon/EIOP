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

AcquisitionMode = Literal["baseline", "poll", "webhook", "reconcile", "replay"]
SourceHealth = Literal["UNKNOWN", "HEALTHY", "DEGRADED", "UNAVAILABLE", "MISCONFIGURED"]
WebhookStatus = Literal["UNCONFIGURED", "CONFIGURED", "ACTIVE", "DISABLED", "FAILING"]


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
    acquisition_modes: list[AcquisitionMode] = Field(default_factory=list, max_length=16)
    allowed_scopes: list[str] = Field(default_factory=list, max_length=1000)
    excluded_scopes: list[str] = Field(default_factory=list, max_length=1000)
    polling_frequency_seconds: int | None = Field(default=None, ge=1, le=31_536_000)
    webhook_status: WebhookStatus = "UNCONFIGURED"
    mapping_version: str | None = Field(default=None, max_length=128)
    parser_version: str | None = Field(default=None, max_length=128)
    checkpoint: str | None = Field(default=None, max_length=4096)
    last_successful_baseline: str | None = Field(default=None, max_length=64)
    last_incremental_run: str | None = Field(default=None, max_length=64)
    reconciliation_schedule: str | None = Field(default=None, max_length=256)
    health: SourceHealth = "UNKNOWN"
    freshness_slo_seconds: int | None = Field(default=None, ge=1, le=31_536_000)
    compatibility: dict[str, Any] = Field(default_factory=dict)
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
        if not self.acquisition_modes:
            modes: list[AcquisitionMode] = []
            if self.capabilities.baseline:
                modes.append("baseline")
            if self.capabilities.polling:
                modes.append("poll")
            if self.capabilities.webhooks:
                modes.append("webhook")
            if self.capabilities.reconciliation:
                modes.append("reconcile")
            if self.capabilities.replay:
                modes.append("replay")
            self.acquisition_modes = modes
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
