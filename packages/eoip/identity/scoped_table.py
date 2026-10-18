"""Scoped Source Identity Table and Canonical Identity Resolution (CRA-023.1).

Guarantees:
- Strict tenant and source-instance boundaries: (tenant_id, source_instance, external_id) -> canonical_id.
- Same textual ID in different source instances or tenants resolves to distinct canonical IDs (no cross-tenant or cross-source collision).
- Deterministic idempotency: repeatedly resolving the same triple yields the exact same canonical ID.
- Source aliases and contributing source provenance are preserved.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
from typing import Any, Optional


@dataclass(frozen=True)
class ScopedSourceKey:
    tenant_id: str
    source_instance: str
    external_id: str

    def to_urn(self) -> str:
        t = self.tenant_id.strip().casefold()
        s = self.source_instance.strip().casefold()
        e = self.external_id.strip()
        return f"urn:eoip:identity:scoped:{t}:{s}:{e}"


@dataclass
class SourceIdentityRecord:
    canonical_id: str
    tenant_id: str
    source_instance: str
    external_id: str
    entity_type: str
    source_alias: str
    properties: dict[str, Any] = field(default_factory=dict)
    aliases: set[str] = field(default_factory=set)
    created_at: str = ""


class ScopedSourceIdentityTable:
    """Deterministic, tenant-isolated source identity resolution table (CRA-023.1)."""

    def __init__(self) -> None:
        self._table: dict[ScopedSourceKey, SourceIdentityRecord] = {}
        self._by_canonical: dict[str, SourceIdentityRecord] = {}
        self._aliases: dict[str, str] = {}  # alias -> canonical_id

    def resolve_or_create(
        self,
        tenant_id: str,
        source_instance: str,
        external_id: str,
        entity_type: str = "Entity",
        properties: Optional[dict[str, Any]] = None,
        deterministic_salt: str = "eoip-v1",
    ) -> SourceIdentityRecord:
        """Resolve an external identity to a canonical identity (CRA-023.1).

        Guarantees that identical external IDs in different source instances or tenants
        NEVER collide into the same canonical ID without explicit merge evidence.
        """
        key = ScopedSourceKey(
            tenant_id=tenant_id.strip(),
            source_instance=source_instance.strip(),
            external_id=str(external_id).strip(),
        )

        if key in self._table:
            rec = self._table[key]
            if properties:
                rec.properties.update(properties)
            return rec

        # Deterministic canonical ID computation
        seed = f"{deterministic_salt}:{key.tenant_id.casefold()}:{key.source_instance.casefold()}:{key.external_id}"
        cid_hash = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]
        canonical_id = f"urn:eoip:entity:{entity_type.lower()}:{cid_hash}"
        source_alias = f"{key.source_instance}:{key.external_id}"

        record = SourceIdentityRecord(
            canonical_id=canonical_id,
            tenant_id=key.tenant_id,
            source_instance=key.source_instance,
            external_id=key.external_id,
            entity_type=entity_type,
            source_alias=source_alias,
            properties=dict(properties or {}),
            aliases={source_alias},
        )

        self._table[key] = record
        self._by_canonical[canonical_id] = record
        self._aliases[(key.tenant_id, source_alias)] = canonical_id
        self._aliases[source_alias] = canonical_id
        return record

    def get_by_key(self, tenant_id: str, source_instance: str, external_id: str) -> Optional[SourceIdentityRecord]:
        key = ScopedSourceKey(tenant_id.strip(), source_instance.strip(), str(external_id).strip())
        return self._table.get(key)

    def get_by_canonical_id(self, canonical_id: str) -> Optional[SourceIdentityRecord]:
        return self._by_canonical.get(canonical_id)

    def get_by_alias(self, alias: str, tenant_id: Optional[str] = None) -> Optional[SourceIdentityRecord]:
        cid = None
        if tenant_id:
            cid = self._aliases.get((tenant_id.strip(), alias.strip()))
        if not cid:
            cid = self._aliases.get(alias.strip())
        return self._by_canonical.get(cid) if cid else None

    def add_alias(self, canonical_id: str, alias: str, tenant_id: Optional[str] = None) -> None:
        rec = self._by_canonical.get(canonical_id)
        if not rec:
            raise KeyError(f"Unknown canonical ID '{canonical_id}'")
        rec.aliases.add(alias)
        if tenant_id:
            self._aliases[(tenant_id.strip(), alias.strip())] = canonical_id
        self._aliases[alias.strip()] = canonical_id

    def all_records(self) -> list[SourceIdentityRecord]:
        return list(self._table.values())
