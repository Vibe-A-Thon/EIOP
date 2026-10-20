"""Human-attested waivers for obligations and equivalent mutants (T-215 / REVA-PD-012)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict

from reva.core.errors import RevaValidationError
from reva.core.ids import warrant_id
from reva.core.time import format_ts, parse_ts, utc_now_ms
from reva.kernel.store import RevaStore

WaiverKind = Literal["defer", "out_of_scope", "equivalent_mutant"]


class Waiver(BaseModel):
    """Formal waiver for an obligation or mutation test site."""

    model_config = ConfigDict(extra="forbid", strict=False)

    waiver_id: str
    tenant_id: str
    target: str  # Obligation key or owner_digest:site_id
    kind: WaiverKind
    rationale: str
    expires_at: str  # Strict ISO timestamp required
    warrant_id: str

    def is_expired(self, at_ts: Optional[Union[str, Any]] = None) -> bool:
        """Check if waiver is expired relative to current or given timestamp."""
        if at_ts is None:
            now = format_ts(utc_now_ms())
        elif hasattr(at_ts, "strftime"):
            now = format_ts(at_ts)
        else:
            now = str(at_ts)
        return self.expires_at < now


def create_waiver(
    store: RevaStore,
    tenant_id: str,
    target: str,
    kind: WaiverKind,
    rationale: str,
    expires_at: str,
    warrant_id_ref: str,
) -> Waiver:
    """Create and persist a new waiver with mandatory expiration check."""
    if not rationale.strip():
        raise RevaValidationError("Waiver requires non-empty rationale")

    # Validate timestamp format and ensure future expiration
    try:
        parse_ts(expires_at)
    except Exception as e:
        raise RevaValidationError(f"Invalid waiver expires_at timestamp: {e}") from e

    now = format_ts(utc_now_ms())
    if expires_at <= now:
        raise RevaValidationError(f"Waiver expiration ({expires_at}) must be in the future (current: {now})")

    wid = f"wav1_{warrant_id_ref.replace('wr1_', '')[:16]}_{hash(target) % 1000000:06d}"
    waiver = Waiver(
        waiver_id=wid,
        tenant_id=tenant_id,
        target=target,
        kind=kind,
        rationale=rationale,
        expires_at=expires_at,
        warrant_id=warrant_id_ref,
    )

    cur = store.conn.cursor()
    cur.execute(
        """
        INSERT OR REPLACE INTO reva_waivers (
            tenant_id, waiver_id, target, kind, rationale, expires_at, warrant_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            tenant_id,
            waiver.waiver_id,
            waiver.target,
            waiver.kind,
            waiver.rationale,
            waiver.expires_at,
            waiver.warrant_id,
        ),
    )
    store.conn.commit()
    return waiver


def get_active_waivers(store: RevaStore, tenant_id: str) -> List[Waiver]:
    """Retrieve all non-expired waivers for tenant."""
    cur = store.conn.cursor()
    rows = cur.execute(
        "SELECT waiver_id, tenant_id, target, kind, rationale, expires_at, warrant_id FROM reva_waivers WHERE tenant_id = ?",
        (tenant_id,),
    ).fetchall()

    now = format_ts(utc_now_ms())
    active = []
    for r in rows:
        w = Waiver(
            waiver_id=r["waiver_id"],
            tenant_id=r["tenant_id"],
            target=r["target"],
            kind=r["kind"],
            rationale=r["rationale"],
            expires_at=r["expires_at"],
            warrant_id=r["warrant_id"],
        )
        if not w.is_expired(now):
            active.append(w)

    return active
