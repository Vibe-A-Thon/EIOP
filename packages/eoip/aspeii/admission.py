"""Admission controller for ASPEII governed actions (ASPEII-RQ-001..020)."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Tuple

from eoip.contracts.aspeii import (
    ASPEIIActionCertificate,
    ASPEIIActionIntent,
    ASPEIIApprovalDecision,
    ActionEffectClass,
    canonical_action_digest,
)
from eoip.aspeii.receipts import ASPEIIReceiptSigner, CertificateVerification


@dataclass
class AdmissionDecision:
    admitted: bool
    status_code: str
    reason: str
    action_digest: str
    certificate_id: Optional[str] = None
    admitted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ASPEIIAdmissionController:
    """Enforces policy admission gates, warrant leases, idempotency, and dual-control."""

    def __init__(
        self,
        *,
        allowed_tenants: Optional[Set[str]] = None,
        max_rate_per_sec: int = 100,
    ) -> None:
        self.allowed_tenants = allowed_tenants or {"acme-demo", "beta-demo", "default"}
        self.max_rate_per_sec = max_rate_per_sec
        self._consumed_idempotency_keys: Dict[str, Tuple[str, datetime]] = {}  # key -> (digest, timestamp)
        self._rate_counter: Dict[str, List[float]] = {}  # tenant -> [timestamps]

    def check_rate_limit(self, tenant_id: str, now: Optional[float] = None) -> bool:
        ts = now or time.time()
        window = ts - 1.0
        stamps = self._rate_counter.setdefault(tenant_id, [])
        # prune old timestamps
        stamps[:] = [t for t in stamps if t > window]
        if len(stamps) >= self.max_rate_per_sec:
            return False
        stamps.append(ts)
        return True

    def check_idempotency(self, intent: ASPEIIActionIntent) -> Tuple[bool, Optional[str]]:
        """Verify idempotency key.
        Returns (is_allowed, error_reason).
        """
        key = intent.logical_idempotency_key
        digest = canonical_action_digest(intent)
        if key in self._consumed_idempotency_keys:
            prev_digest, prev_time = self._consumed_idempotency_keys[key]
            if prev_digest != digest:
                return False, f"Idempotency conflict: key '{key}' was previously used for different action digest {prev_digest}"
            # Replay with identical action is safe idempotent repeat
            return True, None
        return True, None

    def record_execution(self, intent: ASPEIIActionIntent) -> None:
        key = intent.logical_idempotency_key
        digest = canonical_action_digest(intent)
        self._consumed_idempotency_keys[key] = (digest, datetime.now(timezone.utc))

    def evaluate_admission(
        self,
        intent: ASPEIIActionIntent,
        certificate: Optional[ASPEIIActionCertificate] = None,
        approvals: Optional[List[ASPEIIApprovalDecision]] = None,
        verifier: Optional[CertificateVerification] = None,
    ) -> AdmissionDecision:
        digest = canonical_action_digest(intent)
        now_dt = datetime.now(timezone.utc)

        # 1. Tenant validation
        if intent.tenant_id not in self.allowed_tenants:
            return AdmissionDecision(
                admitted=False,
                status_code="TENANT_DISALLOWED",
                reason=f"Tenant '{intent.tenant_id}' is not in allowed tenant registry",
                action_digest=digest,
            )

        # 2. Rate limit
        if not self.check_rate_limit(intent.tenant_id):
            return AdmissionDecision(
                admitted=False,
                status_code="RATE_LIMIT_EXCEEDED",
                reason=f"Rate limit exceeded for tenant '{intent.tenant_id}'",
                action_digest=digest,
            )

        # 3. Idempotency check
        idem_ok, idem_err = self.check_idempotency(intent)
        if not idem_ok:
            return AdmissionDecision(
                admitted=False,
                status_code="IDEMPOTENCY_VIOLATION",
                reason=idem_err or "Idempotency key collision with conflicting payload",
                action_digest=digest,
            )

        # 4. Effect class rules & required approvals (Dual Control)
        if intent.effect_class in ("EXTERNAL_WRITE", "IRREVERSIBLE"):
            if not approvals:
                return AdmissionDecision(
                    admitted=False,
                    status_code="APPROVAL_REQUIRED",
                    reason=f"Action with effect class {intent.effect_class} requires approved reviewer decision",
                    action_digest=digest,
                )
            # Verify approvers are distinct from requester
            for app in approvals:
                if app.decision != "APPROVE":
                    return AdmissionDecision(
                        admitted=False,
                        status_code="APPROVAL_REJECTED",
                        reason=f"Approval decision is {app.decision}",
                        action_digest=digest,
                    )
                if app.requester_principal_id == app.reviewer_principal_id:
                    return AdmissionDecision(
                        admitted=False,
                        status_code="SEPARATION_OF_DUTIES_FAIL",
                        reason="Requester cannot approve their own action intent",
                        action_digest=digest,
                    )
                if not app.separation_of_duties_passed:
                    return AdmissionDecision(
                        admitted=False,
                        status_code="SEPARATION_OF_DUTIES_FAIL",
                        reason="Separation of duties check failed for approval",
                        action_digest=digest,
                    )
                if app.expires_at <= now_dt:
                    return AdmissionDecision(
                        admitted=False,
                        status_code="APPROVAL_EXPIRED",
                        reason=f"Approval expired at {app.expires_at.isoformat()}",
                        action_digest=digest,
                    )

        # 5. Certificate signature check if certificate supplied
        if certificate:
            if certificate.action_digest != digest:
                return AdmissionDecision(
                    admitted=False,
                    status_code="CERTIFICATE_DIGEST_MISMATCH",
                    reason="Certificate action digest does not match intent digest",
                    action_digest=digest,
                    certificate_id=certificate.certificate_id,
                )
            if certificate.expires_at <= now_dt:
                return AdmissionDecision(
                    admitted=False,
                    status_code="CERTIFICATE_EXPIRED",
                    reason=f"Certificate expired at {certificate.expires_at.isoformat()}",
                    action_digest=digest,
                    certificate_id=certificate.certificate_id,
                )
            if verifier and not verifier.valid:
                return AdmissionDecision(
                    admitted=False,
                    status_code="SIGNATURE_INVALID",
                    reason=f"Cryptographic certificate verification failed: {verifier.reason_code}",
                    action_digest=digest,
                    certificate_id=certificate.certificate_id,
                )

        return AdmissionDecision(
            admitted=True,
            status_code="ADMITTED",
            reason="All admission checks, warranties, and policy constraints satisfied",
            action_digest=digest,
            certificate_id=certificate.certificate_id if certificate else None,
        )
