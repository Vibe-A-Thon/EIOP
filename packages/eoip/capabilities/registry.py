"""Thread-safe runtime CapabilityRegistry conforming to CRA-001.6, CRA-001.7, and CRA-001.8."""
from __future__ import annotations
import json, os, threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

from eoip.capabilities.model import (
    CapabilityEntry,
    CapabilityState,
    UnsupportedCapabilityError,
    CapabilityUnavailableError,
    CapabilityNotEntitledError,
    CapabilityDisabledError,
)

ProbeFunc = Callable[[], bool]

class CapabilityRegistry:
    _instance: Optional[CapabilityRegistry] = None
    _lock = threading.Lock()

    def __new__(cls) -> CapabilityRegistry:
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        self._entries: dict[str, CapabilityEntry] = {}
        self._probes: dict[str, ProbeFunc] = {}
        self._registry_lock = threading.RLock()
        self._ledger_path = Path(".audit-scratch/ledger.json")
        self._initialized = True

    def reset(self) -> None:
        """Clear registry entries (used in tests)."""
        with self._registry_lock:
            self._entries.clear()
            self._probes.clear()

    def set_ledger_path(self, path: Path) -> None:
        self._ledger_path = path

    def register(
        self,
        capability_id: str,
        provider_id: str,
        provider_version: str,
        profile: str = "P0",
        probe: Optional[ProbeFunc] = None,
        qualifying_clauses: Optional[list[str]] = None,
        unsupported_constructs: Optional[list[str]] = None,
        initial_state: Optional[CapabilityState] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> CapabilityEntry:
        with self._registry_lock:
            clauses = qualifying_clauses or []
            state = initial_state or CapabilityState.SUPPORTED_UNQUALIFIED
            
            entry = CapabilityEntry(
                capability_id=capability_id,
                provider_id=provider_id,
                provider_version=provider_version,
                profile=profile,
                state=state,
                qualifying_clauses=clauses,
                unsupported_constructs=unsupported_constructs or [],
                details=details or {},
            )
            self._entries[capability_id] = entry
            if probe is not None:
                self._probes[capability_id] = probe
            
            self._evaluate_qualification(entry)
            return entry

    def configure_state(self, capability_id: str, state: CapabilityState) -> None:
        with self._registry_lock:
            if state == CapabilityState.SUPPORTED_QUALIFIED:
                raise ValueError("CRA-001.7 violation: SUPPORTED_QUALIFIED cannot be authored in configuration; it requires an ACCEPTED ledger receipt")
            if capability_id not in self._entries:
                raise KeyError(f"Capability '{capability_id}' not registered")
            self._entries[capability_id].state = state

    def probe_all(self, timeout_s: float = 5.0) -> dict[str, bool]:
        """Probe all registered capabilities with timeout, never raising."""
        results: dict[str, bool] = {}
        with self._registry_lock:
            for cap_id, probe in list(self._probes.items()):
                entry = self._entries.get(cap_id)
                if not entry:
                    continue
                if entry.state in (CapabilityState.DISABLED, CapabilityState.UNLICENSED):
                    continue
                try:
                    ok = bool(probe())
                except Exception:
                    ok = False
                now = datetime.now(timezone.utc)
                entry.last_probe_at = now
                if not ok:
                    entry.state = CapabilityState.UNAVAILABLE
                results[cap_id] = ok
        return results

    def _evaluate_qualification(self, entry: CapabilityEntry) -> None:
        """Check if all qualifying clauses are ACCEPTED in the ledger."""
        if entry.state in (CapabilityState.DISABLED, CapabilityState.UNLICENSED, CapabilityState.UNSUPPORTED):
            return

        if not entry.qualifying_clauses:
            entry.state = CapabilityState.SUPPORTED_UNQUALIFIED
            return

        if not self._ledger_path.exists():
            entry.state = CapabilityState.SUPPORTED_UNQUALIFIED
            return

        try:
            ledger_data = json.loads(self._ledger_path.read_text(encoding="utf-8"))
            items_by_id = {i["id"]: i for i in ledger_data.get("items", [])}
            all_accepted = True
            latest_receipt = None
            for clause in entry.qualifying_clauses:
                item = items_by_id.get(clause)
                if not item or item.get("state") != "ACCEPTED":
                    all_accepted = False
                    break
                receipts = item.get("receipts", [])
                if receipts:
                    latest_receipt = receipts[-1].get("path")

            if all_accepted:
                entry.state = CapabilityState.SUPPORTED_QUALIFIED
                entry.receipt_ref = latest_receipt
            else:
                entry.state = CapabilityState.SUPPORTED_UNQUALIFIED
        except Exception:
            entry.state = CapabilityState.SUPPORTED_UNQUALIFIED

    def refresh_qualifications(self) -> None:
        with self._registry_lock:
            for entry in self._entries.values():
                self._evaluate_qualification(entry)

    def get(self, capability_id: str) -> Optional[CapabilityEntry]:
        with self._registry_lock:
            return self._entries.get(capability_id)

    def get_all(self) -> list[CapabilityEntry]:
        with self._registry_lock:
            return list(self._entries.values())

    def require(self, capability_id: str, construct: Optional[str] = None) -> CapabilityEntry:
        """Enforce capability readiness per CRA-001.8. Never returns empty success."""
        with self._registry_lock:
            entry = self._entries.get(capability_id)
            if entry is None or entry.state == CapabilityState.UNSUPPORTED:
                raise UnsupportedCapabilityError(capability_id, construct)

            if construct and construct in entry.unsupported_constructs:
                raise UnsupportedCapabilityError(capability_id, construct)

            if entry.state == CapabilityState.DISABLED:
                raise CapabilityDisabledError(capability_id)

            if entry.state == CapabilityState.UNLICENSED:
                raise CapabilityNotEntitledError(capability_id)

            if entry.state == CapabilityState.UNAVAILABLE:
                raise CapabilityUnavailableError(capability_id)

            return entry

_registry = CapabilityRegistry()

def get_capability_registry() -> CapabilityRegistry:
    return _registry
