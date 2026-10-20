"""Epistemic gap lifecycle state machine, registry, and impact scoring (T-304 / §6.8 / REVA-CV-002..004)."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field

from reva.core.ids import gap_id as compute_gap_id, normalize_question
from reva.core.time import format_ts, utc_now_ms
from reva.core.errors import ConflictError, NotFoundError, ValidationError
from reva.kernel.store import RevaStore

GapStatus = Literal["open", "assigned", "addressed", "closed", "waived"]
GapSeverity = Literal["blocker", "high", "medium", "low"]


class GapTransition(BaseModel):
    from_status: str
    to_status: str
    rationale: str
    actor: str
    timestamp: str


class GapRecord(BaseModel):
    gap_id: str
    tenant_id: str
    revision: int = 1
    status: GapStatus = "open"
    severity: GapSeverity = "medium"
    impact_score_bp: int = Field(default=0, ge=0, le=10000)
    owner: Optional[str] = None
    due_at: Optional[str] = None
    domain: str
    question: str
    scope: str
    history: List[GapTransition] = Field(default_factory=list)
    supporting_warrant_ids: List[str] = Field(default_factory=list)
    contradicting_warrant_ids: List[str] = Field(default_factory=list)
    resolution: Optional[Dict[str, Any]] = None


# Normative gap state machine (REVA-KG-003). Same-status updates only change fields.
ALLOWED_TRANSITIONS: Dict[str, set] = {
    "open": {"assigned", "addressed", "waived"},
    "assigned": {"open", "addressed", "waived"},
    "addressed": {"assigned", "closed"},
    "closed": set(),
    "waived": {"open"},
}


def open_gap(
    store: RevaStore,
    tenant_id: str,
    domain: str,
    question: str,
    scope: str,
    severity: GapSeverity = "medium",
    impact_score_bp: int = 0,
    owner: Optional[str] = None,
    due_at: Optional[str] = None,
) -> GapRecord:
    """Open or retrieve an epistemic gap, idempotently identified by question/scope hash."""
    gid = compute_gap_id(tenant_id, domain, question, scope)
    now = format_ts(utc_now_ms())

    cur = store.conn.cursor()
    row = cur.execute(
        "SELECT * FROM reva_gap_heads WHERE tenant_id = ? AND gap_id = ?",
        (tenant_id, gid),
    ).fetchone()

    if row:
        rec_data = json.loads(row["record"])
        return GapRecord(**rec_data)

    initial_record = GapRecord(
        gap_id=gid,
        tenant_id=tenant_id,
        revision=1,
        status="open",
        severity=severity,
        impact_score_bp=impact_score_bp,
        owner=owner,
        due_at=due_at,
        domain=domain,
        question=question,
        scope=scope,
        history=[
            GapTransition(
                from_status="none",
                to_status="open",
                rationale="Gap discovered",
                actor="system",
                timestamp=now,
            )
        ],
    )

    cur.execute(
        """
        INSERT INTO reva_gap_heads (
            tenant_id, gap_id, revision, status, severity, impact_score_bp, owner, due_at, domain, record
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            tenant_id,
            gid,
            1,
            "open",
            severity,
            impact_score_bp,
            owner,
            due_at,
            domain,
            initial_record.model_dump_json(),
        ),
    )
    store.conn.commit()
    return initial_record


def _load_gap(store: RevaStore, tenant_id: str, gap_id: str) -> GapRecord:
    row = store.conn.execute(
        "SELECT record FROM reva_gap_heads WHERE tenant_id = ? AND gap_id = ?",
        (tenant_id, gap_id),
    ).fetchone()
    if not row:
        raise NotFoundError(f"Gap {gap_id} not found in tenant {tenant_id}")
    return GapRecord.model_validate_json(row["record"])


def _save_gap(store: RevaStore, gap: GapRecord) -> None:
    store.conn.execute(
        """
        UPDATE reva_gap_heads
        SET revision = ?, status = ?, severity = ?, impact_score_bp = ?, owner = ?, due_at = ?, record = ?
        WHERE tenant_id = ? AND gap_id = ?
        """,
        (gap.revision, gap.status, gap.severity, gap.impact_score_bp, gap.owner, gap.due_at,
         gap.model_dump_json(), gap.tenant_id, gap.gap_id),
    )
    store.conn.commit()


def _apply_transition(gap: GapRecord, to_status: str, rationale: str, actor: str) -> None:
    if to_status == gap.status:
        return
    if to_status not in ALLOWED_TRANSITIONS.get(gap.status, set()):
        raise ValidationError(f"Gap transition {gap.status} -> {to_status} is not allowed")
    if to_status == "closed" and not gap.supporting_warrant_ids:
        raise ValidationError("A gap closes only with at least one supporting warrant (resolution evidence)")
    gap.history.append(
        GapTransition(from_status=gap.status, to_status=to_status, rationale=rationale, actor=actor,
                      timestamp=format_ts(utc_now_ms()))
    )
    gap.status = to_status  # type: ignore[assignment]


def transition_gap(
    store: RevaStore,
    tenant_id: str,
    gap_id: str,
    to_status: GapStatus,
    rationale: str,
    actor: str,
) -> GapRecord:
    """Transition gap state per the normative FSM (open -> assigned -> addressed -> closed / waived)."""
    gap = _load_gap(store, tenant_id, gap_id)
    _apply_transition(gap, to_status, rationale, actor)
    gap.revision += 1
    _save_gap(store, gap)
    return gap


def list_gaps(
    store: RevaStore,
    tenant_id: str,
    status: Optional[str] = None,
    domain: Optional[str] = None,
) -> List[GapRecord]:
    """List gaps with optional status or domain filter."""
    clauses = ["tenant_id = ?"]
    params: List[Any] = [tenant_id]

    if status is not None:
        clauses.append("status = ?")
        params.append(status)
    if domain is not None:
        clauses.append("domain = ?")
        params.append(domain)

    sql = f"SELECT record FROM reva_gap_heads WHERE {' AND '.join(clauses)} ORDER BY impact_score_bp DESC"
    cur = store.conn.cursor()
    rows = cur.execute(sql, params).fetchall()

    return [GapRecord.model_validate_json(r["record"]) for r in rows]


def record_gap(
    store: RevaStore,
    tenant_id: str,
    domain: str,
    question: str,
    scope: Any,
    severity: str = "medium",
    actor: str = "system",
) -> Dict[str, Any]:
    """Record a gap, returning its dictionary representation."""
    scope_str = json.dumps(scope) if isinstance(scope, (dict, list)) else str(scope)
    rec = open_gap(
        store=store,
        tenant_id=tenant_id,
        domain=domain,
        question=question,
        scope=scope_str,
        severity=severity,  # type: ignore
    )
    return rec.model_dump()


def update_gap(
    store: RevaStore,
    tenant_id: str,
    gap_id: str,
    expected_revision: int,
    patch: Dict[str, Any],
    actor: str = "system",
) -> Dict[str, Any]:
    """Apply a patch to the gap head with optimistic concurrency (expected_revision) and FSM checks."""
    gap = _load_gap(store, tenant_id, gap_id)
    if gap.revision != expected_revision:
        raise ConflictError(
            f"Gap {gap_id} is at revision {gap.revision}, not {expected_revision}",
            details={"current_revision": gap.revision},
        )
    for field_name in ("severity", "owner", "due_at", "resolution"):
        if field_name in patch:
            setattr(gap, field_name, patch[field_name])
    for field_name in ("supporting_warrant_ids", "contradicting_warrant_ids"):
        if patch.get(field_name):
            merged = list(getattr(gap, field_name))
            merged.extend(w for w in patch[field_name] if w not in merged)
            setattr(gap, field_name, merged)
    if "status" in patch and patch["status"] is not None:
        _apply_transition(gap, patch["status"], patch.get("rationale") or "Updated revision", actor)
    gap.revision += 1
    _save_gap(store, gap)
    return gap.model_dump()
