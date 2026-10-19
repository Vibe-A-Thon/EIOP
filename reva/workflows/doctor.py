"""System integrity auditor and readiness diagnosis (T-802 / DR-001..005)."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal

from reva.kernel.store import RevaStore
from reva.kernel.translog import MerkleLog


@dataclass
class DoctorCheck:
    name: str
    status: Literal["ok", "warning", "error"]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DoctorReport:
    healthy: bool
    status: Literal["healthy", "degraded", "failing"]
    checks: List[DoctorCheck] = field(default_factory=list)


def run_doctor(
    store: RevaStore,
    translog: MerkleLog,
    tenant_id: str = "default",
) -> DoctorReport:
    """Execute complete health and cryptographic audit of REVA instance."""
    checks: List[DoctorCheck] = []

    # 1. SQLite database integrity check
    try:
        cur = store.conn.cursor()
        cur.execute("PRAGMA integrity_check")
        rows = cur.fetchall()
        if rows and rows[0][0] == "ok":
            checks.append(DoctorCheck(name="db_integrity", status="ok", message="Database integrity verified"))
        else:
            checks.append(DoctorCheck(name="db_integrity", status="error", message=f"Integrity check failed: {rows}"))
    except Exception as e:
        checks.append(DoctorCheck(name="db_integrity", status="error", message=str(e)))

    # 2. Merkle transparency log consistency
    log_id = f"{tenant_id}:warrants"
    try:
        cur = store.conn.cursor()
        cur.execute("SELECT count(*) FROM reva_warrants WHERE tenant_id = ?", (tenant_id,))
        warrant_count = cur.fetchone()[0]
        log_size = translog.size(log_id)

        if warrant_count == log_size:
            checks.append(
                DoctorCheck(
                    name="translog_sync",
                    status="ok",
                    message="Transparency log size matches warrant count",
                    details={"log_size": log_size, "warrants": warrant_count},
                )
            )
        else:
            checks.append(
                DoctorCheck(
                    name="translog_sync",
                    status="warning",
                    message="Log size differs from warrant count (uncommitted or unindexed)",
                    details={"log_size": log_size, "warrants": warrant_count},
                )
            )
    except Exception as e:
        checks.append(DoctorCheck(name="translog_sync", status="error", message=str(e)))

    # 3. Fault injection safety check (must be off in production)
    faults_enabled = os.environ.get("REVA_TEST_FAULTS", "").lower() in ("1", "true", "yes")
    if faults_enabled:
        checks.append(
            DoctorCheck(
                name="fault_injection_guard",
                status="warning",
                message="REVA_TEST_FAULTS is enabled in environment",
            )
        )
    else:
        checks.append(
            DoctorCheck(
                name="fault_injection_guard",
                status="ok",
                message="Fault injection hooks safely disabled",
            )
        )

    # 4. Blob store reachability
    try:
        bref = store.blobs.put(tenant_id, b"reva_health_ping")
        read_back = store.blobs.get(tenant_id, bref.blob_id)
        if read_back == b"reva_health_ping":
            checks.append(DoctorCheck(name="blob_store", status="ok", message="CAS blob store operational"))
        else:
            checks.append(DoctorCheck(name="blob_store", status="error", message="Blob store readback corruption"))
    except Exception as e:
        checks.append(DoctorCheck(name="blob_store", status="error", message=str(e)))

    has_error = any(c.status == "error" for c in checks)
    has_warning = any(c.status == "warning" for c in checks)

    overall_status: Literal["healthy", "degraded", "failing"]
    if has_error:
        overall_status = "failing"
    elif has_warning:
        overall_status = "degraded"
    else:
        overall_status = "healthy"

    return DoctorReport(
        healthy=(overall_status == "healthy"),
        status=overall_status,
        checks=checks,
    )
