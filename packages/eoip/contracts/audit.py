"""AuditEvent v1.

Normative: EOIP-engg-doc-pkg/schemas/audit_event.schema.json
Audit events record ingestion, queries, agent/tool calls, admin operations,
backup/restore and policy denials. Hidden chain-of-thought is never stored.
"""

from eoip.contracts.source_event import utc_now_iso
from pydantic import BaseModel, Field


class AuditEvent(BaseModel):
    audit_id: str
    timestamp: str = Field(default_factory=utc_now_iso)
    event_type: str
    actor: str
    correlation_id: str
    resource_refs: list | None = None
    outcome: str
    reason_code: str | None = None
    safe_summary: str | None = None
