"""Runtime Feature Flag System.

Provides per-tenant, per-environment feature toggles with percentage-based
rollout, override stacking (env < global < tenant), and an audit trail for
flag changes. Designed for zero-downtime configuration changes.
"""

from __future__ import annotations

import hashlib
import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class FlagDefinition:
    name: str
    description: str
    default_enabled: bool = False
    rollout_percentage: float = 100.0
    allowed_tenants: set[str] = field(default_factory=set)
    blocked_tenants: set[str] = field(default_factory=set)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


@dataclass
class FlagEvaluation:
    flag_name: str
    enabled: bool
    reason: str
    tenant_id: str | None = None
    rollout_hash: int | None = None


class FeatureFlagRegistry:
    """Thread-safe feature flag registry with percentage-based rollout support."""

    def __init__(self) -> None:
        self._flags: dict[str, FlagDefinition] = {}
        self._overrides: dict[str, dict[str, bool]] = {}
        self._lock = threading.Lock()
        self._change_log: list[dict[str, Any]] = []

    def define(self, flag: FlagDefinition) -> None:
        with self._lock:
            self._flags[flag.name] = flag
            self._log_change(flag.name, "DEFINED", {"default": flag.default_enabled})

    def remove(self, name: str) -> bool:
        with self._lock:
            if name in self._flags:
                del self._flags[name]
                self._overrides.pop(name, None)
                self._log_change(name, "REMOVED", {})
                return True
            return False

    def set_override(self, name: str, tenant_id: str, enabled: bool) -> None:
        with self._lock:
            self._overrides.setdefault(name, {})[tenant_id] = enabled
            self._log_change(name, "OVERRIDE_SET", {"tenant": tenant_id, "enabled": enabled})

    def clear_override(self, name: str, tenant_id: str) -> None:
        with self._lock:
            if name in self._overrides:
                self._overrides[name].pop(tenant_id, None)
                self._log_change(name, "OVERRIDE_CLEARED", {"tenant": tenant_id})

    def is_enabled(self, name: str, tenant_id: str | None = None, attributes: dict[str, Any] | None = None) -> FlagEvaluation:
        with self._lock:
            flag = self._flags.get(name)
            if flag is None:
                return FlagEvaluation(flag_name=name, enabled=False, reason="FLAG_NOT_DEFINED", tenant_id=tenant_id)

            if tenant_id and tenant_id in flag.blocked_tenants:
                return FlagEvaluation(flag_name=name, enabled=False, reason="TENANT_BLOCKED", tenant_id=tenant_id)

            if tenant_id and name in self._overrides and tenant_id in self._overrides[name]:
                enabled = self._overrides[name][tenant_id]
                return FlagEvaluation(flag_name=name, enabled=enabled, reason="TENANT_OVERRIDE", tenant_id=tenant_id)

            if tenant_id and flag.allowed_tenants and tenant_id not in flag.allowed_tenants:
                return FlagEvaluation(flag_name=name, enabled=False, reason="TENANT_NOT_ALLOWED", tenant_id=tenant_id)

            if flag.rollout_percentage < 100.0:
                hash_key = f"{name}:{tenant_id or 'global'}"
                hash_val = int(hashlib.sha256(hash_key.encode()).hexdigest()[:8], 16)
                bucket = hash_val % 100
                enabled = bucket < flag.rollout_percentage
                return FlagEvaluation(
                    flag_name=name, enabled=enabled,
                    reason="ROLLOUT_PERCENTAGE",
                    tenant_id=tenant_id, rollout_hash=bucket,
                )

            return FlagEvaluation(
                flag_name=name, enabled=flag.default_enabled,
                reason="DEFAULT", tenant_id=tenant_id,
            )

    def list_flags(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {
                    "name": f.name,
                    "description": f.description,
                    "default_enabled": f.default_enabled,
                    "rollout_percentage": f.rollout_percentage,
                    "overrides": dict(self._overrides.get(f.name, {})),
                }
                for f in self._flags.values()
            ]

    def stats(self) -> dict[str, Any]:
        with self._lock:
            return {
                "total_flags": len(self._flags),
                "enabled_by_default": sum(1 for f in self._flags.values() if f.default_enabled),
                "total_overrides": sum(len(v) for v in self._overrides.values()),
                "change_log_size": len(self._change_log),
            }

    def _log_change(self, name: str, action: str, details: dict[str, Any]) -> None:
        self._change_log.append({
            "flag": name,
            "action": action,
            "details": details,
            "timestamp": time.time(),
        })
        if len(self._change_log) > 10000:
            self._change_log = self._change_log[-5000:]


_INSTANCE: FeatureFlagRegistry | None = None
_INSTANCE_LOCK = threading.Lock()


def get_feature_flags() -> FeatureFlagRegistry:
    global _INSTANCE
    if _INSTANCE is None:
        with _INSTANCE_LOCK:
            if _INSTANCE is None:
                _INSTANCE = FeatureFlagRegistry()
    return _INSTANCE
