"""Contradiction detection, multi-warrant conflict tracking, and resolution (T-305 / REVA-CV-006 / §6.7.2)."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field

from reva.core.ids import contradiction_id as compute_contradiction_id
from reva.core.time import format_ts, utc_now_ms
from reva.kernel.store import RevaStore
from reva.kernel.warrant import SealedWarrant, WarrantBody, WarrantEnvelope

ConflictKind = Literal["direct", "temporal", "subsumption"]
ContradictionStatus = Literal["open", "resolved", "dismissed"]


class ContradictionRecord(BaseModel):
    contradiction_id: str
    tenant_id: str
    status: ContradictionStatus = "open"
    conflict_kind: ConflictKind = "direct"
    subject_key: str
    predicate: str
    member_warrant_ids: List[str]
    opened_at: str
    resolved_at: Optional[str] = None
    resolution_warrant_id: Optional[str] = None
    rationale: Optional[str] = None


def detect_contradictions(
    store: RevaStore,
    tenant_id: str,
    new_warrant: SealedWarrant,
) -> List[ContradictionRecord]:
    """Scan existing active warrants about same subject/predicate for conflicting statements."""
    subject_key = "unknown"
    subj = new_warrant.body.subject
    if hasattr(subj, "sha256"):
        subject_key = f"artifact:{subj.sha256}"
    elif hasattr(subj, "record_key"):
        subject_key = f"source_record:{subj.system_instance_id}:{subj.record_key}"
    elif hasattr(subj, "entity_id"):
        subject_key = f"graph_entity:{subj.entity_type}:{subj.entity_id}"

    cur = store.conn.cursor()
    cur.execute(
        """
        SELECT warrant_id, body, envelope FROM reva_warrants
        WHERE tenant_id = ? AND subject_key = ? AND predicate = ? AND status = 'active' AND warrant_id != ?
        """,
        (tenant_id, subject_key, new_warrant.body.predicate, new_warrant.warrant_id),
    )
    rows = cur.fetchall()
    now = format_ts(utc_now_ms())
    contradictions: List[ContradictionRecord] = []

    for r in rows:
        existing_wid = r["warrant_id"]
        existing_body = json.loads(r["body"])

        # Check for direct conflicting statement payload
        if existing_body.get("statement") != new_warrant.body.statement:
            members = sorted([existing_wid, new_warrant.warrant_id])
            cid = compute_contradiction_id(tenant_id, f"{subject_key}:{new_warrant.body.predicate}", members)


            record = ContradictionRecord(
                contradiction_id=cid,
                tenant_id=tenant_id,
                status="open",
                conflict_kind="direct",
                subject_key=subject_key,
                predicate=new_warrant.body.predicate,
                member_warrant_ids=members,
                opened_at=now,
            )

            cur.execute(
                """
                INSERT OR IGNORE INTO reva_contradictions (
                    tenant_id, contradiction_id, record, status, conflict_kind, subject_key, predicate, opened_at
                ) VALUES (?, ?, ?, 'open', 'direct', ?, ?, ?)
                """,
                (tenant_id, cid, record.model_dump_json(), subject_key, new_warrant.body.predicate, now),
            )
            contradictions.append(record)

    store.conn.commit()
    return contradictions


def resolve_contradiction(
    store: RevaStore,
    tenant_id: str,
    contradiction_id: str,
    winning_warrant_id: Optional[str] = None,
    rationale: str = "",
    rule: str = "human_decision",
    winner_warrant_id: Optional[str] = None,
    decided_by: str = "system",
) -> ContradictionRecord:
    """Resolve an open contradiction in favor of a winning warrant or rule."""
    resolved_winner = winner_warrant_id or winning_warrant_id or ""
    cur = store.conn.cursor()
    row = cur.execute(
        "SELECT record FROM reva_contradictions WHERE tenant_id = ? AND contradiction_id = ?",
        (tenant_id, contradiction_id),
    ).fetchone()

    if not row:
        raise ValueError(f"Contradiction {contradiction_id} not found in tenant {tenant_id}")

    record = ContradictionRecord.model_validate_json(row["record"])
    now = format_ts(utc_now_ms())

    # Update record
    record.status = "resolved"
    record.resolved_at = now
    record.resolution_warrant_id = resolved_winner
    record.rationale = rationale

    cur.execute(
        "UPDATE reva_contradictions SET status = 'resolved', record = ? WHERE tenant_id = ? AND contradiction_id = ?",
        (record.model_dump_json(), tenant_id, contradiction_id),
    )

    # Supersede losing members
    for wid in record.member_warrant_ids:
        if wid != resolved_winner:
            w_row = store.get_warrant(tenant_id, wid)
            if w_row:
                b, env = w_row
                env["status"] = "superseded"
                env["status_changed_at"] = now
                store.update_warrant_envelope(tenant_id, wid, env, "superseded")

    store.conn.commit()
    return record


def list_contradictions(
    store: RevaStore,
    tenant_id: str,
    status: Optional[str] = None,
) -> List[ContradictionRecord]:
    """List contradictions with optional status filter."""
    cur = store.conn.cursor()
    if status is not None:
        rows = cur.execute(
            "SELECT record FROM reva_contradictions WHERE tenant_id = ? AND status = ? ORDER BY opened_at DESC",
            (tenant_id, status),
        ).fetchall()
    else:
        rows = cur.execute(
            "SELECT record FROM reva_contradictions WHERE tenant_id = ? ORDER BY opened_at DESC",
            (tenant_id,),
        ).fetchall()

    return [ContradictionRecord.model_validate_json(r["record"]) for r in rows]
