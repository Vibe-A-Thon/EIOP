"""Evidence v1.

Normative: EOIP-engg-doc-pkg/schemas/evidence.schema.json
Required: evidence_id, source_system, source_ref, captured_at, method.
"""

from eoip.contracts.source_event import utc_now_iso
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    evidence_id: str
    source_system: str
    source_ref: str
    captured_at: str = Field(default_factory=utc_now_iso)
    method: str
    parser_version: str | None = None
    mapper_version: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
