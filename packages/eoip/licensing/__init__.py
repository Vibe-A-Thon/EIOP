"""Licensing: signed license files, entitlement checks, usage metering (SR-DEP-007, SR-COM-001, SR-TEN-009).

Public API:

* :class:`LicensePayload`, :func:`sign_license`, :func:`verify_license` — HMAC-SHA256
  signed license files (asymmetric-signature upgrade path is documented in
  ``license_file.py``; ADR-gated).
* :class:`EntitlementChecker`, :func:`build_entitlement_checker` — edition /
  module / size-tier / tenant / seat enforcement with grace-period handling.
  Enforcement is **read-only degrade with a visible notice**; it never deletes
  or locks customer data (SR-DEP-007).
* :class:`UsageMeter` — tamper-evident JSONL hash-chain usage meter compatible
  with the shared audit-sink JSONL conventions (SR-TEN-009).
* :func:`verify_license_cli` — offline license verification entry point.
* :func:`build_router` — FastAPI fragment mounted under ``/api/v1/licensing``
  (lazy fastapi import; wired by the apps/api wiring step, not here).
"""

from eoip.licensing.license_file import (
    LicensePayload,
    LicenseVerification,
    canonical_payload_bytes,
    generate_license_id,
    load_license_file,
    sign_license,
    verify_license,
)
from eoip.licensing.entitlements import (
    CheckOutcome,
    EntitlementChecker,
    build_entitlement_checker,
)
from eoip.licensing.meter import MeterEvent, MeterVerification, UsageMeter
from eoip.licensing.cli import verify_license_cli

__all__ = [
    "LicensePayload",
    "LicenseVerification",
    "canonical_payload_bytes",
    "generate_license_id",
    "load_license_file",
    "sign_license",
    "verify_license",
    "CheckOutcome",
    "EntitlementChecker",
    "build_entitlement_checker",
    "MeterEvent",
    "MeterVerification",
    "UsageMeter",
    "verify_license_cli",
    "build_router",
]


def build_router(*args, **kwargs):
    """Lazy delegate to :func:`eoip.licensing.api.build_router` (keeps fastapi import lazy)."""
    from eoip.licensing.api import build_router as _build_router

    return _build_router(*args, **kwargs)
