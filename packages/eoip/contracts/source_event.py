"""SourceEvent v1 — immutable raw capture envelope.

Normative: EOIP-engg-doc-pkg/schemas/source_event.schema.json
"All externally ingested facts first become immutable SourceEvent envelopes
with content hashes." (FR-INGEST-001)
"""

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field


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
