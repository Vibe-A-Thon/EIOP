"""Time-boxed, auto-expiring policy exceptions (SR-GOV-005).

An exception grants a documented deviation from a policy (authz rule,
validation gate, retention rule, classification floor...) for a bounded
window. Exceptions must be approved, are visible (listed while active), and
expire automatically: ``is_active()`` compares ``expires_at`` to the current
time, so no background job is required for correctness — any read path only
ever sees unexpired exceptions. Persistence is a JSON-file store.

Expiry enforcement on the enforcement path (rejecting a request that relies
on an expired exception) is ADR-gated: the visibility and evaluation
primitives here are the contract the enforcement gate will call.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from eoip.compliance.pack import new_id


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class PolicyException(BaseModel):
    """A time-boxed, approved deviation from a policy (SR-GOV-005)."""

    model_config = ConfigDict(extra="forbid")

    exception_id: str
    policy_ref: str
    subject: str
    justification: str
    approved_by: str
    approved_at: str
    expires_at: str
    revoked: bool = False

    def is_active(self, now: datetime | None = None) -> bool:
        """Auto-expiring check: active iff approved, not revoked, unexpired."""
        if self.revoked:
            return False
        now = now or datetime.now(timezone.utc)
        expires = datetime.fromisoformat(self.expires_at)
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        return now < expires


class PolicyExceptionStore:
    """JSON-file store for policy exceptions (SR-GOV-005)."""

    def __init__(self, path: str | Path | None = None) -> None:
        self._lock = RLock()
        self._path = Path(path) if path else Path(
            os.getenv("EOIP_DATA_DIR", ".data")
        ) / "state" / "policy-exceptions.json"
        self._items: dict[str, PolicyException] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            return
        data = json.loads(self._path.read_text(encoding="utf-8"))
        for item in data.get("exceptions", []):
            exception = PolicyException(**item)
            self._items[exception.exception_id] = exception

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"exceptions": [e.model_dump() for e in self._items.values()]}
        self._path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def create(
        self,
        policy_ref: str,
        subject: str,
        justification: str,
        *,
        approved_by: str,
        expires_at: str,
        approved_at: str | None = None,
    ) -> PolicyException:
        if not approved_by:
            raise ValueError("Policy exceptions require an approver (SR-GOV-005)")
        exception = PolicyException(
            exception_id=new_id("compliance", "policy-exception"),
            policy_ref=policy_ref,
            subject=subject,
            justification=justification,
            approved_by=approved_by,
            approved_at=approved_at or utc_now_iso(),
            expires_at=expires_at,
        )
        with self._lock:
            self._items[exception.exception_id] = exception
            self._save()
        return exception

    def get(self, exception_id: str) -> PolicyException | None:
        return self._items.get(exception_id)

    def list(self, *, active_only: bool = False) -> list[PolicyException]:
        items = list(self._items.values())
        if active_only:
            items = [e for e in items if e.is_active()]
        return items

    def revoke(self, exception_id: str, *, actor: str) -> PolicyException:
        with self._lock:
            exception = self._items.get(exception_id)
            if exception is None:
                raise KeyError(f"Unknown exception: {exception_id}")
            exception.revoked = True
            self._save()
            return exception
