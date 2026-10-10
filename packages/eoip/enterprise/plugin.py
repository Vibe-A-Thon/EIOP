"""Plugin system for extending EOIP with custom capabilities.

Provides a discovery-based plugin architecture where plugins are registered
by name and capability. Supports lifecycle hooks (on_load, on_unload),
dependency declaration, and version compatibility checks.
"""

from __future__ import annotations

import enum
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


class PluginCapability(str, enum.Enum):
    GRAPH_BACKEND = "GRAPH_BACKEND"
    RAG_STRATEGY = "RAG_STRATEGY"
    QUERY_DIALECT = "QUERY_DIALECT"
    AGENT_ARCHETYPE = "AGENT_ARCHETYPE"
    INGESTION_SOURCE = "INGESTION_SOURCE"
    EXPORT_FORMAT = "EXPORT_FORMAT"
    AUTH_PROVIDER = "AUTH_PROVIDER"
    NOTIFICATION_CHANNEL = "NOTIFICATION_CHANNEL"
    ANALYTICS_EXTENSION = "ANALYTICS_EXTENSION"
    CUSTOM = "CUSTOM"


class PluginStatus(str, enum.Enum):
    REGISTERED = "REGISTERED"
    LOADED = "LOADED"
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    ERROR = "ERROR"


@runtime_checkable
class PluginInterface(Protocol):
    @property
    def name(self) -> str: ...
    @property
    def version(self) -> str: ...
    @property
    def capabilities(self) -> list[PluginCapability]: ...
    def on_load(self, config: dict[str, Any]) -> None: ...
    def on_unload(self) -> None: ...


@dataclass
class PluginMetadata:
    name: str
    version: str
    author: str
    description: str
    capabilities: list[PluginCapability]
    dependencies: list[str] = field(default_factory=list)
    min_eoip_version: str = "1.0.0"


@dataclass
class PluginRecord:
    metadata: PluginMetadata
    instance: PluginInterface | None
    status: PluginStatus
    loaded_at: float | None = None
    error: str | None = None


class PluginRegistry:
    """Central plugin registry with lifecycle management."""

    def __init__(self) -> None:
        self._plugins: dict[str, PluginRecord] = {}
        self._lock = threading.Lock()

    def register(self, metadata: PluginMetadata, instance: PluginInterface | None = None) -> None:
        with self._lock:
            self._plugins[metadata.name] = PluginRecord(
                metadata=metadata,
                instance=instance,
                status=PluginStatus.REGISTERED,
            )

    def load(self, name: str, config: dict[str, Any] | None = None) -> bool:
        with self._lock:
            record = self._plugins.get(name)
            if not record:
                return False

            for dep in record.metadata.dependencies:
                dep_rec = self._plugins.get(dep)
                if not dep_rec or dep_rec.status not in (PluginStatus.LOADED, PluginStatus.ACTIVE):
                    record.status = PluginStatus.ERROR
                    record.error = f"Missing dependency: {dep}"
                    return False

            if record.instance is not None:
                try:
                    record.instance.on_load(config or {})
                    record.status = PluginStatus.ACTIVE
                    record.loaded_at = time.time()
                    return True
                except Exception as exc:
                    record.status = PluginStatus.ERROR
                    record.error = str(exc)
                    return False

            record.status = PluginStatus.LOADED
            record.loaded_at = time.time()
            return True

    def unload(self, name: str) -> bool:
        with self._lock:
            record = self._plugins.get(name)
            if not record:
                return False
            if record.instance is not None:
                try:
                    record.instance.on_unload()
                except Exception:
                    pass
            record.status = PluginStatus.DISABLED
            return True

    def get(self, name: str) -> PluginRecord | None:
        with self._lock:
            return self._plugins.get(name)

    def find_by_capability(self, capability: PluginCapability) -> list[PluginRecord]:
        with self._lock:
            return [
                r for r in self._plugins.values()
                if capability in r.metadata.capabilities
                and r.status in (PluginStatus.LOADED, PluginStatus.ACTIVE)
            ]

    def list_all(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {
                    "name": r.metadata.name,
                    "version": r.metadata.version,
                    "author": r.metadata.author,
                    "description": r.metadata.description,
                    "capabilities": [c.value for c in r.metadata.capabilities],
                    "status": r.status.value,
                    "loaded_at": r.loaded_at,
                    "error": r.error,
                }
                for r in self._plugins.values()
            ]

    def get_stats(self) -> dict[str, Any]:
        with self._lock:
            status_counts: dict[str, int] = {}
            for r in self._plugins.values():
                status_counts[r.status.value] = status_counts.get(r.status.value, 0) + 1
            return {
                "total_plugins": len(self._plugins),
                "status_distribution": status_counts,
                "capabilities_available": list(set(
                    c.value
                    for r in self._plugins.values()
                    for c in r.metadata.capabilities
                    if r.status in (PluginStatus.LOADED, PluginStatus.ACTIVE)
                )),
            }


_registry: PluginRegistry | None = None
_reg_lock = threading.Lock()


def get_plugin_registry() -> PluginRegistry:
    global _registry
    if _registry is None:
        with _reg_lock:
            if _registry is None:
                _registry = PluginRegistry()
    return _registry
