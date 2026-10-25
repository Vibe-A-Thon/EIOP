"""Immutable per-call EgressManifest (SR-LLM-013).

Every egress call (allowed or denied, dry-run or executed) produces an
immutable manifest: who called, which data classes and orthogonal tags,
the sharing level applied, the fields/tokens sent, the endpoint and
region, byte counts in/out, the approval id (when required), the policy
rules matched, DLP findings, and a SHA-256 hash of the response.

Manifests are append-only in the gateway; the ``what left the building``
report is an export over a time range for auditors.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid

from pydantic import BaseModel, ConfigDict, Field, field_validator


class _FrozenList(list):
    """List that compares like a list but refuses in-place mutation (deep immutability)."""

    def _blocked(self, *args, **kwargs):
        raise TypeError("EgressManifest is immutable (SR-LLM-013)")

    append = extend = insert = remove = pop = clear = sort = reverse = _blocked
    __setitem__ = __delitem__ = __iadd__ = __imul__ = _blocked


class EgressManifest(BaseModel):
    """Immutable record of one egress call attempt (SR-LLM-013)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    manifest_id: str
    call_id: str
    tenant_id: str
    user_id: str
    role: str
    task: str
    endpoint_id: str
    endpoint_region: str
    data_classes: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    level: int = 0  # SharingLevel ordinal actually applied; set post-policy
    fields: list[str] = Field(default_factory=list, description="Top-level field names sent")
    tokens: list[str] = Field(default_factory=list, description="Vault tokens used (S4)")
    bytes_out: int = 0
    bytes_in: int = 0
    approval_id: str | None = None
    matched_rule_ids: list[str] = Field(default_factory=list)
    dlp_findings: list[str] = Field(default_factory=list)
    canary_blocked: bool = False
    denied: bool = False
    denial_reason: str = ""
    dry_run: bool = False
    request_hash: str = ""
    response_hash: str = ""
    created_at: float = Field(default_factory=time.time)

    @field_validator("data_classes", "tags", "fields", "tokens", "matched_rule_ids", "dlp_findings",
                     mode="after")
    @classmethod
    def _freeze_lists(cls, value: list[str]) -> list[str]:
        return _FrozenList(value)


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_payload(payload: dict) -> str:
    return hash_bytes(
        json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    )


def new_manifest(**kwargs) -> EgressManifest:
    call_id = f"urn:eoip:egress:call:{uuid.uuid4().hex[:16]}"
    return EgressManifest(
        manifest_id=f"urn:eoip:egress:manifest:{uuid.uuid4().hex[:16]}",
        call_id=call_id,
        **kwargs,
    )


def what_left_the_building(manifests: list[EgressManifest]) -> dict:
    """Auditor-facing export over a set of manifests (SR-LLM-013).

    Includes only calls where data actually left the boundary
    (not denied, not dry-run, level > S0).
    """
    egressed = [
        m for m in manifests
        if not m.denied and not m.dry_run and m.level > 0
    ]
    return {
        "manifest_count": len(egressed),
        "total_bytes_out": sum(m.bytes_out for m in egressed),
        "total_bytes_in": sum(m.bytes_in for m in egressed),
        "by_endpoint": _count_by(egressed, "endpoint_id"),
        "by_tenant": _count_by(egressed, "tenant_id"),
        "by_level": _count_by(egressed, "level"),
        "by_data_class": {
            cls: sum(1 for m in egressed if cls in m.data_classes)
            for cls in sorted({c for m in egressed for c in m.data_classes})
        },
        "manifests": [m.model_dump() for m in egressed],
    }


def _count_by(manifests: list[EgressManifest], attr: str) -> dict:
    counts: dict = {}
    for m in manifests:
        key = str(getattr(m, attr))
        counts[key] = counts.get(key, 0) + 1
    return counts
