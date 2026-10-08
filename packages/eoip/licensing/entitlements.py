"""Entitlement enforcement for editions, modules, size tiers, tenants and seats.

Implements SR-COM-001 (licensing models) and the enforcement half of
SR-DEP-007. Hard rule: **no entitlement check may ever delete or lock customer
data**. Every check returns a :class:`CheckOutcome`; the ``degrade`` path
marks operations read-only and attaches a visible notice, but the data store
is never touched from this module. ``require_*`` helpers raise a refusal
(HTTP 402/403 at the API layer) for *new* writes over the limit; existing
data remains fully readable.

Grace periods (SR-DEP-007): after ``expiry`` the license is ``expired_grace``
until ``expiry + grace_days`` — full function plus a warning notice — and
``expired`` after that, which degrades to read-only with the notice
``license_expired_read_only``. Perpetual licenses (``expiry is None``) never
expire.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable

from pydantic import BaseModel, ConfigDict

from eoip.licensing.license_file import LicensePayload, LicenseVerification, verify_license

# Edition -> modules available when the license does not pin a module list.
EDITION_MODULES: dict[str, list[str]] = {
    "community": ["graph", "search", "ingest"],
    "professional": ["graph", "search", "ingest", "query", "nl", "benchmarks", "connectors"],
    "enterprise": ["graph", "search", "ingest", "query", "nl", "benchmarks", "connectors", "audit", "ml", "federation"],
    "oem": ["graph", "search", "ingest", "query", "nl", "benchmarks", "connectors", "audit", "ml", "federation"],
    "evaluation": ["graph", "search", "ingest", "query", "nl"],
}

# Edition ranking for "at least edition X" checks.
EDITION_RANK = {"evaluation": 0, "community": 1, "professional": 2, "enterprise": 3, "oem": 3}

SIZE_TIER_RANK = {"small": 0, "medium": 1, "large": 2, "unlimited": 3}

READ_ONLY_NOTICE = "license_expired_read_only"


class CheckOutcome(BaseModel):
    """Result of one entitlement check.

    ``allowed`` — the operation may proceed as requested.
    ``degraded`` — allowed, but read-only; ``notice`` explains why (always
    visible to the caller). ``notice`` is also set on allowed outcomes during
    the grace period (warning only).
    """

    model_config = ConfigDict(extra="forbid")

    allowed: bool
    check: str
    degraded: bool = False
    notice: str | None = None
    limit: int | None = None
    current: int | None = None


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class EntitlementChecker:
    """Evaluates a verified :class:`LicensePayload` against requested use.

    The checker is constructed from a :class:`LicenseVerification` so a
    tampered or unsigned license can never produce a permissive checker.
    """

    def __init__(self, verification: LicenseVerification, now: Callable[[], datetime] = _utcnow) -> None:
        if not verification.ok or verification.payload is None:
            raise ValueError(f"cannot build EntitlementChecker from failed verification: {verification.reason}")
        self.payload = verification.payload
        self._now = now

    # -- lifecycle ---------------------------------------------------------

    @property
    def license_state(self) -> str:
        """One of ``active`` | ``grace`` | ``expired`` | ``perpetual``."""
        expiry = self.payload.expiry
        if expiry is None:
            return "perpetual"
        now = self._now()
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
        if now <= expiry:
            return "active"
        grace_until = self.payload.grace_until
        if grace_until is not None and grace_until.tzinfo is None:
            grace_until = grace_until.replace(tzinfo=timezone.utc)
        if grace_until is not None and now <= grace_until:
            return "grace"
        return "expired"

    @property
    def expired(self) -> bool:
        """True only after the grace period has lapsed (read-only degrade)."""
        return self.license_state == "expired"

    @property
    def notice(self) -> str | None:
        """Visible warning notice for non-active states."""
        state = self.license_state
        if state == "grace":
            return "license_expired_in_grace_period"
        if state == "expired":
            return READ_ONLY_NOTICE
        return None

    # -- checks ------------------------------------------------------------

    def check_edition(self, minimum: str) -> CheckOutcome:
        """Require the licensed edition to rank at least ``minimum``."""
        ok = EDITION_RANK.get(self.payload.edition, -1) >= EDITION_RANK.get(minimum, 0)
        return CheckOutcome(
            allowed=ok and not self.expired,
            degraded=not ok,
            check="edition",
            notice=None if ok else f"edition_below_minimum:{minimum}",
            current=None,
            limit=None,
        )

    def licensed_modules(self) -> list[str]:
        if self.payload.modules:
            return list(self.payload.modules)
        return list(EDITION_MODULES.get(self.payload.edition, []))

    def check_module(self, module: str) -> CheckOutcome:
        ok = module in self.licensed_modules()
        return CheckOutcome(
            allowed=ok and not self.expired,
            degraded=not ok,
            check="module",
            notice=None if ok else f"module_not_licensed:{module}",
        )

    def check_size_tier(self, required: str) -> CheckOutcome:
        ok = SIZE_TIER_RANK.get(self.payload.size_tier, -1) >= SIZE_TIER_RANK.get(required, 0)
        return CheckOutcome(
            allowed=ok and not self.expired,
            degraded=not ok,
            check="size_tier",
            notice=None if ok else f"size_tier_below:{required}",
        )

    def _check_limit(self, check: str, current: int, maximum: int | None) -> CheckOutcome:
        if maximum is None:
            return CheckOutcome(allowed=True, check=check, current=current, limit=None)
        ok = current <= maximum
        return CheckOutcome(
            allowed=ok and not self.expired,
            degraded=not ok,
            check=check,
            notice=None if ok else f"{check}_limit_reached",
            limit=maximum,
            current=current,
        )

    def check_seats(self, current_seats: int) -> CheckOutcome:
        return self._check_limit("seats", current_seats, self.payload.max_seats)

    def check_tenants(self, current_tenants: int) -> CheckOutcome:
        return self._check_limit("tenants", current_tenants, self.payload.max_tenants)

    def check_records(self, current_records: int) -> CheckOutcome:
        return self._check_limit("records", current_records, self.payload.max_records)

    def degrade(self, outcome: CheckOutcome) -> CheckOutcome:
        """Attach the expiry notice; when expired, force read-only degrade (SR-DEP-007).

        Existing data is never deleted or locked — reads keep working and any
        caller sees ``notice``.
        """
        if self.expired:
            return CheckOutcome(
                allowed=False,
                degraded=True,
                check=outcome.check,
                notice=READ_ONLY_NOTICE,
                limit=outcome.limit,
                current=outcome.current,
            )
        if self.license_state == "grace" and outcome.notice is None:
            return outcome.model_copy(update={"notice": self.notice})
        return outcome

    # -- FastAPI dependency helpers (lazy fastapi import) -------------------

    def require_module(self, module: str) -> Callable[[], None]:
        """FastAPI dependency refusing requests for an unlicensed module."""

        def dependency() -> None:
            from fastapi import HTTPException

            outcome = self.degrade(self.check_module(module))
            if not outcome.allowed:
                status = 403 if outcome.notice and outcome.notice.startswith("module") else 402
                raise HTTPException(status_code=status, detail=outcome.notice)

        dependency.__name__ = f"require_module_{module.replace('-', '_')}"
        return dependency

    def require_seats(self, current_seats: Callable[[], int] | int) -> Callable[[], None]:
        """FastAPI dependency enforcing the seat cap (SR-COM-001 seat add-ons)."""

        def dependency() -> None:
            from fastapi import HTTPException

            current = current_seats() if callable(current_seats) else current_seats
            outcome = self.degrade(self.check_seats(current))
            if not outcome.allowed:
                raise HTTPException(status_code=402, detail=outcome.notice)

        dependency.__name__ = "require_seats"
        return dependency

    def require_edition(self, minimum: str) -> Callable[[], None]:
        """FastAPI dependency requiring at least edition ``minimum``."""

        def dependency() -> None:
            from fastapi import HTTPException

            outcome = self.degrade(self.check_edition(minimum))
            if not outcome.allowed:
                raise HTTPException(status_code=403, detail=outcome.notice)

        dependency.__name__ = f"require_edition_{minimum}"
        return dependency

    def summary(self) -> dict[str, Any]:
        """Machine-readable entitlement summary for the status endpoint."""
        return {
            "license_id": self.payload.license_id,
            "customer": self.payload.customer,
            "edition": self.payload.edition,
            "model": self.payload.model,
            "modules": self.licensed_modules(),
            "size_tier": self.payload.size_tier,
            "max_tenants": self.payload.max_tenants,
            "max_seats": self.payload.max_seats,
            "max_records": self.payload.max_records,
            "state": self.license_state,
            "expiry": self.payload.expiry,
            "grace_until": self.payload.grace_until,
            "notice": self.notice,
        }


def build_entitlement_checker(document: dict[str, Any], vendor_key: str | bytes) -> EntitlementChecker:
    """Verify a signed license document and build the checker in one step."""
    return EntitlementChecker(verify_license(document, vendor_key))
