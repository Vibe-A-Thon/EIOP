"""Privacy governance, 8-plane erasure cascade, anti-resurrection tombstones, and no-egress network monitor (CRA-040).

Covers:
1. CRA-040.1: Classification, lawful handling policies, distinct licenses (code/model/dataset/content), residency, retention, and legal holds.
2. CRA-040.2, CRA-040.7: No-egress socket monitor recording zero external bytes at network boundary.
3. CRA-040.3, CRA-040.5, CRA-040.6: 8-plane erasure cascade (raw, canonical, schema, provenance, lineage, policy, temporal, vector) + caches, exports, backups under legal hold governance.
4. CRA-040.4: Anti-resurrection registry preventing replay, restore, or resync from resurrecting deleted content.
"""

from __future__ import annotations

import hashlib
import json
import socket
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from collections.abc import Callable


class LawfulBasis(str, Enum):
    CONSENT = "CONSENT"
    CONTRACTUAL = "CONTRACTUAL"
    LEGAL_OBLIGATION = "LEGAL_OBLIGATION"
    LEGITIMATE_INTEREST = "LEGITIMATE_INTEREST"


class LicenseKind(str, Enum):
    CODE = "CODE"
    MODEL = "MODEL"
    DATASET = "DATASET"
    CONTENT = "CONTENT"


class GraphPlane(str, Enum):
    RAW = "RAW"
    CANONICAL = "CANONICAL"
    SCHEMA = "SCHEMA"
    PROVENANCE = "PROVENANCE"
    LINEAGE = "LINEAGE"
    POLICY = "POLICY"
    TEMPORAL = "TEMPORAL"
    VECTOR = "VECTOR"


@dataclass
class HandlingPolicy:
    subject_id: str
    lawful_basis: LawfulBasis
    residence_region: str  # e.g., "EU", "US", "GLOBAL"
    retention_days: int
    license_kind: LicenseKind
    license_identifier: str  # e.g., "Apache-2.0", "CC-BY-4.0", "Proprietary"
    legal_hold: bool = False
    legal_hold_ref: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EgressViolationError(PermissionError):
    """Raised when an outbound connection to an unapproved external destination is attempted in no-egress mode."""


class NetworkSocketMonitor:
    """Socket-level network boundary monitor measuring outbound bytes and enforcing strict no-egress (CRA-040.2, CRA-040.7)."""

    def __init__(self, allowed_hosts: Optional[set[str]] = None, no_egress_mode: bool = True) -> None:
        self.allowed_hosts = allowed_hosts or {"localhost", "127.0.0.1", "::1"}
        self.no_egress_mode = no_egress_mode
        self.external_bytes_sent = 0
        self.internal_bytes_sent = 0
        self.recorded_connections: list[dict[str, Any]] = []

    def check_and_record_outbound(self, dest_host: str, dest_port: int, byte_count: int) -> None:
        """Inspect destination host before socket send. Rejects unapproved destinations in no-egress mode."""
        is_internal = (
            dest_host in self.allowed_hosts
            or dest_host.endswith(".internal")
            or dest_host.endswith(".local")
            or dest_host.startswith(("10.", "192.168."))
        )

        record = {
            "host": dest_host,
            "port": dest_port,
            "bytes": byte_count,
            "is_internal": is_internal,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.recorded_connections.append(record)

        if not is_internal:
            if self.no_egress_mode:
                raise EgressViolationError(
                    f"No-egress policy violation: blocked external connection to '{dest_host}:{dest_port}' ({byte_count} bytes)"
                )
            self.external_bytes_sent += byte_count
        else:
            self.internal_bytes_sent += byte_count


@dataclass
class PlanePurgeDetail:
    plane: str
    items_deleted: int
    held_items_skipped: int = 0
    details: list[str] = field(default_factory=list)


@dataclass
class ScopedErasureReport:
    subject_id: str
    tenant_id: str
    timestamp: str
    total_erased: int
    planes: dict[str, PlanePurgeDetail]
    caches_cleared: int
    exports_purged: int
    backups_marked: int
    legal_hold_exceptions: list[str]
    tombstone_hash: str


class AntiResurrectionRegistry:
    """Maintains cryptographic tombstones to prevent replay, restore, or resync from resurrecting deleted content (CRA-040.4)."""

    def __init__(self) -> None:
        self._tombstones: dict[str, dict[str, Any]] = {}

    def register_tombstone(self, subject_id: str, tenant_id: str, reason: str = "GDPR_PURGE") -> str:
        h = hashlib.sha256(f"{tenant_id}:{subject_id}:{time.time()}".encode("utf-8")).hexdigest()
        self._tombstones[subject_id] = {
            "subject_id": subject_id,
            "tenant_id": tenant_id,
            "tombstone_hash": h,
            "reason": reason,
            "registered_at": datetime.now(timezone.utc).isoformat(),
        }
        return h

    def is_tombstoned(self, subject_id: str) -> bool:
        return subject_id in self._tombstones

    def verify_admission(self, record: dict[str, Any], subject_id_key: str = "id") -> None:
        """Blocks admission of incoming payloads if subject has been tombstoned."""
        sid = record.get(subject_id_key)
        if sid and self.is_tombstoned(str(sid)):
            raise PermissionError(
                f"Resurrection blocked: subject '{sid}' has a registered erasure tombstone (CRA-040.4)"
            )


class ErasureCascadeEngine:
    """Executes deep 8-plane erasure cascade, caches/exports/backups purge, and legal hold checks (CRA-040.6, CRA-040.A)."""

    def __init__(
        self,
        tombstone_registry: Optional[AntiResurrectionRegistry] = None,
    ) -> None:
        self.tombstone_registry = tombstone_registry or AntiResurrectionRegistry()
        self.policies: dict[str, HandlingPolicy] = {}

    def set_handling_policy(self, policy: HandlingPolicy) -> None:
        self.policies[policy.subject_id] = policy

    def execute_erasure_cascade(
        self,
        subject_id: str,
        tenant_id: str,
        storage_planes: dict[str, list[dict[str, Any]]],
        caches: Optional[dict[str, Any]] = None,
        exports: Optional[list[dict[str, Any]]] = None,
        backups: Optional[list[dict[str, Any]]] = None,
    ) -> ScopedErasureReport:
        """Execute erasure across all 8 planes plus caches, exports, and backups under legal hold rules."""
        now_iso = datetime.now(timezone.utc).isoformat()
        policy = self.policies.get(subject_id)
        has_legal_hold = policy.legal_hold if policy else False

        plane_results: dict[str, PlanePurgeDetail] = {}
        total_erased = 0
        hold_exceptions: list[str] = []

        all_8_planes = [p.value for p in GraphPlane]

        for plane_name in all_8_planes:
            items = storage_planes.get(plane_name, [])
            items_to_keep = []
            deleted_count = 0
            held_count = 0
            details = []

            for it in items:
                matches_subject = it.get("subject_id") == subject_id or it.get("entity_id") == subject_id
                if matches_subject:
                    if has_legal_hold:
                        held_count += 1
                        items_to_keep.append(it)
                        hold_msg = f"Retained on plane {plane_name} under Legal Hold ref: {policy.legal_hold_ref}"
                        if hold_msg not in hold_exceptions:
                            hold_exceptions.append(hold_msg)
                    else:
                        deleted_count += 1
                        details.append(f"Deleted record {it.get('id', 'item')} from {plane_name}")
                else:
                    items_to_keep.append(it)

            storage_planes[plane_name] = items_to_keep
            total_erased += deleted_count
            plane_results[plane_name] = PlanePurgeDetail(
                plane=plane_name,
                items_deleted=deleted_count,
                held_items_skipped=held_count,
                details=details,
            )

        # Clear Caches
        caches_cleared = 0
        if caches is not None:
            keys_to_del = [k for k in caches if subject_id in k or subject_id in str(caches[k])]
            for k in keys_to_del:
                del caches[k]
                caches_cleared += 1

        # Purge Exports
        exports_purged = 0
        if exports is not None:
            orig_len = len(exports)
            exports[:] = [e for e in exports if e.get("subject_id") != subject_id]
            exports_purged = orig_len - len(exports)

        # Purge/Tombstone Backups
        backups_marked = 0
        if backups is not None:
            for b in backups:
                if b.get("subject_id") == subject_id:
                    if not has_legal_hold:
                        b["tombstoned"] = True
                        b["shredded_at"] = now_iso
                        backups_marked += 1

        # Register tombstone to prevent resurrection (CRA-040.4)
        tombstone_hash = self.tombstone_registry.register_tombstone(subject_id, tenant_id)

        return ScopedErasureReport(
            subject_id=subject_id,
            tenant_id=tenant_id,
            timestamp=now_iso,
            total_erased=total_erased,
            planes=plane_results,
            caches_cleared=caches_cleared,
            exports_purged=exports_purged,
            backups_marked=backups_marked,
            legal_hold_exceptions=hold_exceptions,
            tombstone_hash=tombstone_hash,
        )
