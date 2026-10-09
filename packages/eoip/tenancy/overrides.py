"""Tenant-Scoped Configuration Overrides — per-tenant customization cascading.

Allows each tenant to override schemas, ingestion policies, branding,
agent behaviors, query policies, quality rules, and feature flags.
Overrides cascade: global defaults → tenant defaults → entity-type overrides.
"""

from __future__ import annotations

import copy
import threading
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class OverrideScope(str, Enum):
    SCHEMA = "SCHEMA"
    INGESTION = "INGESTION"
    BRANDING = "BRANDING"
    AGENT_BEHAVIOR = "AGENT_BEHAVIOR"
    QUERY_POLICY = "QUERY_POLICY"
    QUALITY_RULES = "QUALITY_RULES"
    FEATURE_FLAGS = "FEATURE_FLAGS"
    SECURITY = "SECURITY"
    NOTIFICATION = "NOTIFICATION"
    PIPELINE = "PIPELINE"
    RAG = "RAG"


@dataclass
class TenantOverride:
    override_id: str
    tenant_id: str
    scope: OverrideScope
    entity_type: str | None = None  # None = tenant-wide
    key: str = ""
    value: Any = None
    description: str = ""
    created_at: str = ""
    created_by: str = ""
    expires_at: str | None = None
    enabled: bool = True
    priority: int = 0  # higher = wins

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["scope"] = self.scope.value
        return d


@dataclass
class TenantConfig:
    tenant_id: str
    overrides: dict[str, TenantOverride] = field(default_factory=dict)
    inherited_from: str | None = None  # parent tenant for hierarchy

    def get_effective(self, scope: OverrideScope, key: str,
                      entity_type: str | None = None) -> Any | None:
        candidates = [
            o for o in self.overrides.values()
            if o.scope == scope and o.key == key and o.enabled
        ]
        if entity_type:
            specific = [c for c in candidates if c.entity_type == entity_type]
            if specific:
                return max(specific, key=lambda o: o.priority).value

        generic = [c for c in candidates if c.entity_type is None]
        if generic:
            return max(generic, key=lambda o: o.priority).value

        return None


class TenantOverrideManager:
    """Manages tenant-scoped configuration overrides with inheritance cascading."""

    def __init__(self, global_defaults: dict[str, Any] | None = None) -> None:
        self._global: dict[str, Any] = global_defaults or {}
        self._tenants: dict[str, TenantConfig] = {}
        self._lock = threading.RLock()

    def set_global_default(self, scope: str, key: str, value: Any) -> None:
        with self._lock:
            self._global.setdefault(scope, {})[key] = value

    def get_global_default(self, scope: str, key: str) -> Any | None:
        return self._global.get(scope, {}).get(key)

    def create_tenant_config(self, tenant_id: str,
                             parent_tenant: str | None = None) -> TenantConfig:
        with self._lock:
            config = TenantConfig(tenant_id=tenant_id, inherited_from=parent_tenant)
            self._tenants[tenant_id] = config
            return config

    def set_override(self, tenant_id: str, override: TenantOverride) -> TenantOverride:
        with self._lock:
            config = self._tenants.setdefault(tenant_id, TenantConfig(tenant_id=tenant_id))
            override.created_at = override.created_at or time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            config.overrides[override.override_id] = override
            return override

    def remove_override(self, tenant_id: str, override_id: str) -> bool:
        with self._lock:
            config = self._tenants.get(tenant_id)
            if config:
                return config.overrides.pop(override_id, None) is not None
            return False

    def get_effective_config(self, tenant_id: str, scope: OverrideScope,
                             entity_type: str | None = None) -> dict[str, Any]:
        result: dict[str, Any] = copy.deepcopy(self._global.get(scope.value, {}))

        chain = self._get_inheritance_chain(tenant_id)
        for tid in chain:
            config = self._tenants.get(tid)
            if not config:
                continue
            for override in config.overrides.values():
                if override.scope != scope or not override.enabled:
                    continue
                if override.entity_type and override.entity_type != entity_type:
                    continue
                result[override.key] = override.value

        return result

    def get_effective_value(self, tenant_id: str, scope: OverrideScope,
                            key: str, entity_type: str | None = None,
                            default: Any = None) -> Any:
        config = self.get_effective_config(tenant_id, scope, entity_type)
        return config.get(key, default)

    def list_overrides(self, tenant_id: str,
                       scope: OverrideScope | None = None) -> list[TenantOverride]:
        config = self._tenants.get(tenant_id)
        if not config:
            return []
        overrides = list(config.overrides.values())
        if scope:
            overrides = [o for o in overrides if o.scope == scope]
        return overrides

    def list_tenants(self) -> list[str]:
        return list(self._tenants.keys())

    def export_tenant_config(self, tenant_id: str) -> dict[str, Any]:
        config = self._tenants.get(tenant_id)
        if not config:
            return {}
        return {
            "tenant_id": tenant_id,
            "inherited_from": config.inherited_from,
            "overrides": [o.to_dict() for o in config.overrides.values()],
        }

    def import_tenant_config(self, data: dict[str, Any]) -> TenantConfig:
        tenant_id = data["tenant_id"]
        config = self.create_tenant_config(tenant_id, data.get("inherited_from"))
        for o_data in data.get("overrides", []):
            override = TenantOverride(
                override_id=o_data["override_id"],
                tenant_id=tenant_id,
                scope=OverrideScope(o_data["scope"]),
                entity_type=o_data.get("entity_type"),
                key=o_data.get("key", ""),
                value=o_data.get("value"),
                description=o_data.get("description", ""),
                enabled=o_data.get("enabled", True),
                priority=o_data.get("priority", 0),
            )
            self.set_override(tenant_id, override)
        return config

    def _get_inheritance_chain(self, tenant_id: str) -> list[str]:
        chain: list[str] = []
        visited: set[str] = set()
        current = tenant_id
        while current and current not in visited:
            visited.add(current)
            chain.append(current)
            config = self._tenants.get(current)
            current = config.inherited_from if config else None
        chain.reverse()
        return chain
