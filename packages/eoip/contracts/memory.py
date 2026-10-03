"""MemoryRecord v1.

Normative: EOIP-engg-doc-pkg/schemas/memory_record.schema.json
MVP persists only task/audit evidence needed for TraceImpact (FR-MEM-001).
"""

from eoip.contracts.source_event import utc_now_iso
from pydantic import BaseModel, Field


class MemoryRecord(BaseModel):
    memory_id: str
    kind: str
    scope: str
    owner: str
    source: str
    created_at: str = Field(default_factory=utc_now_iso)
    ttl_seconds: int | None = None
    provenance_refs: list
    confidence: float | None = None
    classification: str
    deletion_policy: str | None = None
    content: object | None = None
