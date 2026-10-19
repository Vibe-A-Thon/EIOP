"""Logical identity and bitemporal entity version registry (T-119 / REVA-AB-008 / §1.4)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from reva.core.ids import entity_id as compute_entity_id, entity_version_id as compute_version_id
from reva.core.time import format_ts, utc_now_ms
from reva.kernel.store import RevaStore


class EntityRecord(BaseModel):
    entity_id: str
    tenant_id: str
    entity_type: str
    logical_key: str
    current_version_id: Optional[str] = None
    first_seen: str
    last_seen: str


class EntityVersionRecord(BaseModel):
    version_id: str
    tenant_id: str
    entity_id: str
    version_basis: str
    version_digest: str
    repo_id: Optional[str] = None
    commit_sha: Optional[str] = None
    valid_from: str
    valid_to: Optional[str] = None
    warrant_id: str


class EntityRegistry:
    """Manages canonical logical identities and temporal version branches."""

    def __init__(self, store: RevaStore) -> None:
        self.store = store

    def upsert_entity(self, tenant_id: str, entity_type: str, logical_key: str) -> str:
        """Upsert a logical entity by canonical identity and return ent1_ ID."""
        eid = compute_entity_id(tenant_id, entity_type, logical_key)
        now = format_ts(utc_now_ms())
        cur = self.store.conn.cursor()

        cur.execute(
            """
            INSERT INTO reva_entities (tenant_id, entity_id, entity_type, logical_key, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(tenant_id, entity_type, logical_key) DO UPDATE SET last_seen = ?
            """,
            (tenant_id, eid, entity_type, logical_key, now, now, now),
        )
        self.store.conn.commit()
        return eid

    def record_version(
        self,
        tenant_id: str,
        entity_id: str,
        version_basis: str,
        version_digest: str,
        warrant_id: str,
        repo_id: Optional[str] = None,
        commit_sha: Optional[str] = None,
        valid_from: Optional[str] = None,
    ) -> str:
        """Record an immutable version snapshot, closing previous version's valid_to."""
        vid = compute_version_id(entity_id, version_basis, version_digest)
        now = valid_from or format_ts(utc_now_ms())
        cur = self.store.conn.cursor()

        # Fetch current version
        ent_row = cur.execute(
            "SELECT current_version_id FROM reva_entities WHERE tenant_id = ? AND entity_id = ?",
            (tenant_id, entity_id),
        ).fetchone()

        prev_vid = ent_row["current_version_id"] if ent_row else None
        if prev_vid and prev_vid != vid:
            # Close previous valid_to
            cur.execute(
                "UPDATE reva_entity_versions SET valid_to = ? WHERE tenant_id = ? AND version_id = ? AND valid_to IS NULL",
                (now, tenant_id, prev_vid),
            )

        # Insert new version record
        cur.execute(
            """
            INSERT OR REPLACE INTO reva_entity_versions (
                tenant_id, version_id, entity_id, version_basis, version_digest, repo_id, commit_sha, valid_from, warrant_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (tenant_id, vid, entity_id, version_basis, version_digest, repo_id, commit_sha, now, warrant_id),
        )

        # Update entity current_version_id and last_seen
        cur.execute(
            "UPDATE reva_entities SET current_version_id = ?, last_seen = ? WHERE tenant_id = ? AND entity_id = ?",
            (vid, now, tenant_id, entity_id),
        )
        self.store.conn.commit()
        return vid

    def get_entity(self, tenant_id: str, entity_id: str) -> Optional[EntityRecord]:
        cur = self.store.conn.cursor()
        row = cur.execute(
            "SELECT * FROM reva_entities WHERE tenant_id = ? AND entity_id = ?",
            (tenant_id, entity_id),
        ).fetchone()
        if not row:
            return None
        return EntityRecord(**dict(row))

    def get_entity_by_key(self, tenant_id: str, entity_type: str, logical_key: str) -> Optional[EntityRecord]:
        cur = self.store.conn.cursor()
        row = cur.execute(
            "SELECT * FROM reva_entities WHERE tenant_id = ? AND entity_type = ? AND logical_key = ?",
            (tenant_id, entity_type, logical_key),
        ).fetchone()
        if not row:
            return None
        return EntityRecord(**dict(row))

    def list_versions(self, tenant_id: str, entity_id: str) -> List[EntityVersionRecord]:
        cur = self.store.conn.cursor()
        rows = cur.execute(
            "SELECT * FROM reva_entity_versions WHERE tenant_id = ? AND entity_id = ? ORDER BY valid_from DESC",
            (tenant_id, entity_id),
        ).fetchall()
        return [EntityVersionRecord(**dict(r)) for r in rows]
