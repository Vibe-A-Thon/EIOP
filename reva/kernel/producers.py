"""Producer registry and key attachment (T-118 / REVA-WK-013 / REVA-WK-014)."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from reva.core.ids import producer_id as compute_producer_id
from reva.core.time import format_ts, utc_now_ms
from reva.kernel.keys import generate_key
from reva.kernel.store import RevaStore


class ProducerRecord(BaseModel):
    """Registered warrant producer."""

    producer_id: str
    tenant_id: str
    producer_type: str
    name: str
    version: str
    build_digest: Optional[str] = None
    owner: Optional[str] = None
    active: bool = True
    created_at: str = Field(default_factory=lambda: format_ts(utc_now_ms()))
    active_key_id: Optional[str] = None


def register_producer(
    store: RevaStore,
    tenant_id: str,
    producer_type: str,
    name: str,
    version: str,
    build_digest: Optional[str] = None,
    owner: Optional[str] = None,
) -> ProducerRecord:
    """Register a producer and provision its dedicated Ed25519 signing key."""
    pid = compute_producer_id(tenant_id, producer_type, name, version)


    cur = store.conn.cursor()
    row = cur.execute(
        "SELECT * FROM reva_producers WHERE tenant_id = ? AND producer_id = ?",
        (tenant_id, pid),
    ).fetchone()

    if row:
        # Find active key for existing producer
        key_row = cur.execute(
            "SELECT key_id FROM reva_keys WHERE tenant_id = ? AND owner_id = ? AND status = 'active'",
            (tenant_id, pid),
        ).fetchone()
        return ProducerRecord(
            producer_id=row["producer_id"],
            tenant_id=row["tenant_id"],
            producer_type=row["producer_type"],
            name=row["name"],
            version=row["version"],
            build_digest=row["build_digest"],
            owner=row["owner"],
            active=bool(row["active"]),
            created_at=row["created_at"],
            active_key_id=key_row["key_id"] if key_row else None,
        )

    # Provision key
    key_record = generate_key(store, tenant_id, "producer", pid)
    now = format_ts(utc_now_ms())

    cur.execute(
        """
        INSERT INTO reva_producers (
            producer_id, tenant_id, producer_type, name, version, build_digest, owner, active, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)
        """,
        (pid, tenant_id, producer_type, name, version, build_digest, owner, now),
    )
    store.conn.commit()

    return ProducerRecord(
        producer_id=pid,
        tenant_id=tenant_id,
        producer_type=producer_type,
        name=name,
        version=version,
        build_digest=build_digest,
        owner=owner,
        active=True,
        created_at=now,
        active_key_id=key_record.key_id,
    )


def get_producer(store: RevaStore, tenant_id: str, producer_id: str) -> Optional[ProducerRecord]:
    """Retrieve producer record with its active signing key ID."""
    cur = store.conn.cursor()
    row = cur.execute(
        "SELECT * FROM reva_producers WHERE tenant_id = ? AND producer_id = ?",
        (tenant_id, producer_id),
    ).fetchone()
    if not row:
        return None

    key_row = cur.execute(
        "SELECT key_id FROM reva_keys WHERE tenant_id = ? AND owner_id = ? AND status = 'active'",
        (tenant_id, producer_id),
    ).fetchone()

    return ProducerRecord(
        producer_id=row["producer_id"],
        tenant_id=row["tenant_id"],
        producer_type=row["producer_type"],
        name=row["name"],
        version=row["version"],
        build_digest=row["build_digest"],
        owner=row["owner"],
        active=bool(row["active"]),
        created_at=row["created_at"],
        active_key_id=key_row["key_id"] if key_row else None,
    )


def get_or_create_human_producer(store: RevaStore, tenant_id: str, principal_id: str) -> ProducerRecord:
    """Ensure a human reviewer/operator principal has a registered producer identity and key."""
    return register_producer(
        store=store,
        tenant_id=tenant_id,
        producer_type="human",
        name=f"human:{principal_id}",
        version="1.0.0",
        owner=principal_id,
    )
