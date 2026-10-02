"""SourceEvent v1 — immutable raw capture envelope.

Normative: EOIP-engg-doc-pkg/schemas/source_event.schema.json
"All externally ingested facts first become immutable SourceEvent envelopes
with content hashes." (FR-INGEST-001)
"""

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")

SCHEMA_VERSION: Literal["1.0"] = "1.0"


class SourceEvent(BaseModel):
    schema_version: Literal["1.0"] = "1.0"
    event_id: str
    source_system: str
    source_record_id: str
    source_version: str | None = None
    captured_at: str = Field(default_factory=utc_now_iso)
    payload_hash: str
    payload: dict
    metadata: dict | None = None


SourceOperation = Literal[
    "CREATE",
    "UPDATE",
    "UPSERT",
    "DELETE",
    "RELATIONSHIP_UPDATE",
    "PERMISSION_UPDATE",
]


class PermissionMetadata(BaseModel):
    """Source ACL metadata; it contains identifiers, never credentials."""

    model_config = ConfigDict(extra="forbid")

    visibility: Literal["PUBLIC", "INTERNAL", "RESTRICTED", "UNKNOWN"] = "UNKNOWN"
    principal_refs: list[str] = Field(default_factory=list, max_length=10_000)
    inherited_from: str | None = Field(default=None, max_length=2048)
    acl_hash: str | None = Field(default=None, max_length=128)


class SourceEventV2(BaseModel):
    """G2 canonical source event for baseline, delta, webhook and replay flows."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["2.0"] = "2.0"
    event_id: str = Field(min_length=1, max_length=512)
    source_system: str = Field(min_length=1, max_length=128)
    source_instance_id: str = Field(min_length=1, max_length=256)
    source_record_id: str = Field(min_length=1, max_length=2048)
    operation: SourceOperation = "UPSERT"
    source_version: str | None = Field(default=None, max_length=512)
    event_time: str
    captured_at: str = Field(default_factory=utc_now_iso)
    content_hash: str = Field(min_length=1, max_length=128)
    payload_hash: str | None = Field(default=None, min_length=1, max_length=128)
    cursor: str | None = Field(default=None, max_length=4096)
    permissions: PermissionMetadata = Field(default_factory=PermissionMetadata)
    payload: dict[str, Any] | None = None
    payload_ref: str | None = Field(default=None, max_length=4096)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def require_payload_or_reference(self) -> "SourceEventV2":
        if self.payload is None and self.payload_ref is None and self.operation != "DELETE":
            raise ValueError("payload or payload_ref is required unless operation is DELETE")
        if self.payload_hash is not None and self.payload_hash != self.content_hash:
            raise ValueError("payload_hash must equal content_hash")
        self.payload_hash = self.content_hash
        return self


def upgrade_source_event(
    event: SourceEvent | SourceEventV2 | dict[str, Any],
    *,
    source_instance_id: str | None = None,
    operation: SourceOperation = "UPSERT",
    event_time: str | None = None,
    cursor: str | None = None,
    permissions: PermissionMetadata | dict[str, Any] | None = None,
    payload_ref: str | None = None,
) -> SourceEventV2:
    """Upgrade v1 without changing event identity or the immutable payload hash."""

    if isinstance(event, SourceEventV2):
        return event
    legacy = event if isinstance(event, SourceEvent) else SourceEvent.model_validate(event)
    metadata = dict(legacy.metadata or {})
    instance = source_instance_id or str(metadata.get("source_instance_id") or "default")
    return SourceEventV2(
        event_id=legacy.event_id,
        source_system=legacy.source_system,
        source_instance_id=instance,
        source_record_id=legacy.source_record_id,
        operation=operation,
        source_version=legacy.source_version,
        event_time=event_time or legacy.captured_at,
        captured_at=legacy.captured_at,
        content_hash=legacy.payload_hash,
        cursor=cursor,
        permissions=permissions or PermissionMetadata(),
        payload=legacy.payload,
        payload_ref=payload_ref,
        metadata=metadata,
    )
