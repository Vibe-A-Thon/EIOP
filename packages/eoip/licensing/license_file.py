"""Signed license files for offline / air-gapped deployments (SR-DEP-007).

A license file is a JSON document with two top-level keys::

    {"payload": {...}, "signature": "<hex hmac-sha256>"}

The signature is computed as ``HMAC-SHA256(vendor_key, canonical_payload_bytes(payload))``
where the canonical form is UTF-8 JSON with sorted keys and compact separators
(same canonicalisation style used across eoip contracts). Verification uses
:func:`hmac.compare_digest` (constant time) so a forged or corrupted file is
rejected without timing side channels.

Key management and algorithm upgrade path:

* **Current baseline** — a single vendor-shared-secret HMAC key, delivered
  out-of-band to air-gapped installs (USB / sneakernet) or referenced by a
  path in ``EOIP_LICENSE_KEY_FILE``. This matches the air-gapped deployment
  profile (SR-DEP-007) where online key services are unavailable.
* **Asymmetric upgrade (ADR-gated, External gate)** — HMAC with a shared
  vendor key means any customer node can forge licenses. The upgrade path is
  Ed25519 (or RSA-PSS) vendor signatures so verification needs only the
  public key: ``payload["signature_algorithm"] = "ed25519"`` and signature
  over the same canonical payload bytes. Deferred behind an architecture
  decision record together with key rotation and revocation-list delivery;
  the payload schema already carries ``signature_algorithm`` so the upgrade
  is wire-compatible.

License models (SR-COM-001) are expressed through the payload fields:

* ``model="perpetual"`` — no expiry; ``support_expiry`` bounds support only.
* ``model="subscription"`` — annual (or shorter) term via ``expiry``.
* ``model="size_tier"`` / ``model="usage"`` — size-tier/usage-based via
  ``size_tier`` plus the :class:`eoip.licensing.meter.UsageMeter` export.
* ``model="per_tenant"`` — OEM/managed via ``max_tenants``.
* Seat-based add-ons via ``max_seats``.
* ``model="oem_revenue_share"`` — OEM revenue-share/royalty: signed ``royalty`` terms
  (basis, rate, minimum per period, reporting period); :func:`compute_royalty` produces the
  per-period statement from reported revenue or metered usage units. Payment collection
  itself stays an external billing integration.

All timestamps are ISO-8601 UTC strings.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SIGNATURE_ALGORITHM = "hmac-sha256"
LICENSE_ID_PREFIX = "urn:eoip:licensing:license:"

LicenseModel = Literal["perpetual", "subscription", "size_tier", "usage", "per_tenant", "evaluation",
                       "oem_revenue_share"]
Edition = Literal["community", "professional", "enterprise", "oem", "evaluation"]


def generate_license_id() -> str:
    """Mint a fresh license URN id."""
    return f"{LICENSE_ID_PREFIX}{uuid.uuid4()}"


class RoyaltyTerms(BaseModel):
    """Signed OEM revenue-share / royalty terms (SR-COM-001)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    basis: Literal["revenue", "usage_units"] = "revenue"
    rate_bps: int = Field(ge=1, le=10_000, description="Share in basis points of revenue, or price per 1,000 units in minor currency units")
    minimum_per_period: int = Field(default=0, ge=0, description="Minimum due per period, minor currency units")
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    period: Literal["monthly", "quarterly"] = "quarterly"


class LicensePayload(BaseModel):
    """The signed content of a license file (SR-DEP-007, SR-COM-001).

    ``expiry=None`` means unbounded (perpetual). ``grace_days`` is the number
    of days after expiry during which the installation keeps full function and
    only surfaces a warning (see ``eoip.licensing.entitlements``).
    """

    model_config = ConfigDict(extra="forbid")

    license_id: str = Field(default_factory=generate_license_id)
    customer: str = Field(description="Customer / licensee name")
    edition: Edition = "professional"
    model: LicenseModel = "subscription"
    modules: list[str] = Field(default_factory=list, description="Licensed module ids (empty = edition default)")
    size_tier: str = Field(default="small", description="Size tier id, e.g. small | medium | large | unlimited")
    max_tenants: int | None = Field(default=None, ge=1, description="None = unlimited")
    max_seats: int | None = Field(default=None, ge=1, description="None = unlimited")
    max_records: int | None = Field(default=None, ge=1, description="None = unlimited; metered record cap for size tiers")
    issued_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expiry: datetime | None = Field(default=None, description="None = perpetual (model=perpetual)")
    support_expiry: datetime | None = Field(default=None, description="Support entitlement end (perpetual + annual support)")
    grace_days: int = Field(default=14, ge=0, description="Read-only-degrade grace period after expiry (SR-DEP-007)")
    royalty: RoyaltyTerms | None = Field(default=None, description="Required for model=oem_revenue_share only")
    signature_algorithm: str = Field(default=SIGNATURE_ALGORITHM, description="Wire-compatible hook for the asymmetric upgrade")

    @model_validator(mode="after")
    def _defaults(self) -> "LicensePayload":
        if self.model == "perpetual" and self.expiry is not None:
            raise ValueError("perpetual licenses must not carry an expiry")
        if self.model == "oem_revenue_share":
            if self.royalty is None:
                raise ValueError("oem_revenue_share licenses must carry signed royalty terms")
            if self.edition != "oem":
                raise ValueError("oem_revenue_share requires edition 'oem'")
        elif self.royalty is not None:
            raise ValueError("royalty terms are only valid for model 'oem_revenue_share'")
        if self.support_expiry is not None and self.model != "perpetual":
            raise ValueError("support_expiry applies to perpetual licenses (perpetual + annual support)")
        return self

    @property
    def grace_until(self) -> datetime | None:
        """Grace-period end (expiry + grace_days), or None when perpetual."""
        if self.expiry is None:
            return None
        return self.expiry + timedelta(days=self.grace_days)


class LicenseVerification(BaseModel):
    """Result of verifying a signed license file."""

    model_config = ConfigDict(extra="forbid")

    ok: bool
    reason: str = "ok"
    payload: LicensePayload | None = None


def canonical_payload_bytes(payload: dict[str, Any] | LicensePayload) -> bytes:
    """Canonical serialisation covered by the signature: sorted-key compact JSON.

    ``payload`` may be a raw dict (as stored in the file) or a
    :class:`LicensePayload`; both serialise identically.
    """
    if isinstance(payload, LicensePayload):
        data = payload.model_dump(mode="json")
    else:
        data = payload
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _signing_key_bytes(key: str | bytes) -> bytes:
    return key.encode("utf-8") if isinstance(key, str) else key


def sign_license(payload: LicensePayload, vendor_key: str | bytes) -> dict[str, Any]:
    """Produce the signed license document: ``{"payload": {...}, "signature": hex}``."""
    digest = hmac.new(_signing_key_bytes(vendor_key), canonical_payload_bytes(payload), hashlib.sha256)
    return {"payload": payload.model_dump(mode="json"), "signature": digest.hexdigest()}


def verify_license(document: dict[str, Any], vendor_key: str | bytes) -> LicenseVerification:
    """Verify a signed license document (constant-time signature compare).

    Rejects malformed documents, wrong algorithms, and any payload/signature
    mismatch. Returns the parsed payload only when the signature is valid.
    """
    if not isinstance(document, dict) or "payload" not in document or "signature" not in document:
        return LicenseVerification(ok=False, reason="malformed_document")
    payload = document["payload"]
    if not isinstance(payload, dict):
        return LicenseVerification(ok=False, reason="malformed_payload")
    algorithm = payload.get("signature_algorithm", SIGNATURE_ALGORITHM)
    if algorithm != SIGNATURE_ALGORITHM:
        # External gate: ed25519/rsa-pss upgrade path (see module docstring).
        return LicenseVerification(ok=False, reason=f"unsupported_signature_algorithm:{algorithm}")
    expected = hmac.new(_signing_key_bytes(vendor_key), canonical_payload_bytes(payload), hashlib.sha256).hexdigest()
    provided = str(document["signature"])
    if not hmac.compare_digest(expected, provided):
        return LicenseVerification(ok=False, reason="invalid_signature")
    try:
        parsed = LicensePayload.model_validate(payload)
    except Exception as exc:  # pydantic ValidationError -> malformed payload
        return LicenseVerification(ok=False, reason=f"invalid_payload:{exc.__class__.__name__}")
    return LicenseVerification(ok=True, payload=parsed)


def save_license_file(document: dict[str, Any], path: str | Path) -> None:
    Path(path).write_text(json.dumps(document, indent=2, ensure_ascii=False), encoding="utf-8")


def load_license_file(path: str | Path, vendor_key: str | bytes) -> LicenseVerification:
    """Load and verify a license file from disk (offline path, SR-DEP-007)."""
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return LicenseVerification(ok=False, reason=f"unreadable:{exc.__class__.__name__}")
    return verify_license(document, vendor_key)


def generate_vendor_key() -> str:
    """Generate a random vendor signing key (hex). Deliver out-of-band for air-gapped installs."""
    return secrets.token_hex(32)


def compute_royalty(terms: RoyaltyTerms, *, period_label: str, gross_revenue_minor: int | None = None,
                    usage_units: int | None = None) -> dict[str, Any]:
    """Per-period OEM royalty statement (SR-COM-001). Integer minor currency units; rounds half up.

    ``basis="revenue"`` takes reported gross revenue; ``basis="usage_units"`` takes the metered
    unit count from the tamper-evident usage meter export. The other input must be absent.
    """
    if terms.basis == "revenue":
        if gross_revenue_minor is None or usage_units is not None:
            raise ValueError("revenue-based royalty needs gross_revenue_minor only")
        if gross_revenue_minor < 0:
            raise ValueError("gross revenue cannot be negative")
        computed = (gross_revenue_minor * terms.rate_bps + 5_000) // 10_000
        base = gross_revenue_minor
    else:
        if usage_units is None or gross_revenue_minor is not None:
            raise ValueError("usage-based royalty needs usage_units only")
        if usage_units < 0:
            raise ValueError("usage units cannot be negative")
        computed = (usage_units * terms.rate_bps + 500) // 1_000
        base = usage_units
    due = max(computed, terms.minimum_per_period)
    return {"period": period_label, "period_kind": terms.period, "basis": terms.basis, "base": base,
            "rate_bps": terms.rate_bps, "computed": computed, "minimum_applied": due > computed,
            "amount_due_minor": due, "currency": terms.currency}
