"""Scoped plugin state repository and lifecycle operations (CRA-002.5).

Persists plugin state scoped by tenant/workspace, manages schema migrations,
and enforces clean uninstall/disable semantics.
"""

from __future__ import annotations

import json
import logging
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from collections.abc import Callable

from eoip.plugins.manifest import PluginUninstallPolicy

logger = logging.getLogger(__name__)


@dataclass
class PluginStateEntry:
    tenant_id: str
    workspace_id: str
    plugin_id: str
    version: str
    enabled: bool = True
    permissions_revoked: bool = False
    state_data: dict[str, Any] = field(default_factory=dict)
    migration_history: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PluginStateRepository:
    """Thread-safe, tenant-and-workspace scoped repository for plugin state."""

    def __init__(self, persistence_file: Path | None = None) -> None:
        self._lock = threading.RLock()
        self._persistence_file = persistence_file
        # key: (tenant_id, workspace_id, plugin_id) -> PluginStateEntry
        self._entries: dict[tuple[str, str, str], PluginStateEntry] = {}
        if self._persistence_file and self._persistence_file.is_file():
            self._load()

    def _make_key(self, tenant_id: str, workspace_id: str, plugin_id: str) -> tuple[str, str, str]:
        return (tenant_id, workspace_id, plugin_id)

    def register_plugin(
        self,
        tenant_id: str,
        workspace_id: str,
        plugin_id: str,
        version: str,
    ) -> PluginStateEntry:
        with self._lock:
            key = self._make_key(tenant_id, workspace_id, plugin_id)
            if key not in self._entries:
                self._entries[key] = PluginStateEntry(
                    tenant_id=tenant_id,
                    workspace_id=workspace_id,
                    plugin_id=plugin_id,
                    version=version,
                )
                self._save()
            return self._entries[key]

    def get_state(self, tenant_id: str, workspace_id: str, plugin_id: str, key: str) -> Any:
        with self._lock:
            entry_key = self._make_key(tenant_id, workspace_id, plugin_id)
            entry = self._entries.get(entry_key)
            if not entry or not entry.enabled:
                return None
            return entry.state_data.get(key)

    def set_state(self, tenant_id: str, workspace_id: str, plugin_id: str, key: str, value: Any) -> None:
        with self._lock:
            entry_key = self._make_key(tenant_id, workspace_id, plugin_id)
            entry = self._entries.get(entry_key)
            if not entry:
                entry = self.register_plugin(tenant_id, workspace_id, plugin_id, "1.0.0")
            if not entry.enabled:
                raise PermissionError(f"Plugin {plugin_id} is disabled in workspace {workspace_id}")
            entry.state_data[key] = value
            entry.updated_at = datetime.now(timezone.utc).isoformat()
            self._save()

    def disable_plugin(self, tenant_id: str, workspace_id: str, plugin_id: str) -> None:
        """CRA-002.5: Disable revokes permissions and marks inactive."""
        with self._lock:
            entry_key = self._make_key(tenant_id, workspace_id, plugin_id)
            entry = self._entries.get(entry_key)
            if entry:
                entry.enabled = False
                entry.permissions_revoked = True
                entry.updated_at = datetime.now(timezone.utc).isoformat()
                self._save()

    def uninstall_plugin(
        self,
        tenant_id: str,
        workspace_id: str,
        plugin_id: str,
        policy: PluginUninstallPolicy,
    ) -> dict[str, Any]:
        """CRA-002.5: Uninstall revokes permissions, cleans/migrates data per policy."""
        with self._lock:
            entry_key = self._make_key(tenant_id, workspace_id, plugin_id)
            entry = self._entries.get(entry_key)
            if not entry:
                return {"status": "NOT_FOUND"}

            entry.enabled = False
            entry.permissions_revoked = True

            if policy.retention == "delete":
                # Clean up stored data
                entry.state_data.clear()
                self._entries.pop(entry_key, None)
            elif policy.retention == "archive":
                entry.state_data = {"_archived": True, "archive_time": datetime.now(timezone.utc).isoformat()}
            # if policy.retention == "retain", state remains preserved

            self._save()
            return {
                "status": "UNINSTALLED",
                "retention_policy": policy.retention,
                "plugin_id": plugin_id,
                "tenant_id": tenant_id,
                "workspace_id": workspace_id,
            }

    def apply_migration(
        self,
        tenant_id: str,
        workspace_id: str,
        plugin_id: str,
        target_version: str,
        migration_fn: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> None:
        """Versioned schema migration on owned plugin state."""
        with self._lock:
            entry_key = self._make_key(tenant_id, workspace_id, plugin_id)
            entry = self._entries.get(entry_key)
            if not entry:
                raise KeyError(f"Plugin {plugin_id} not registered in {tenant_id}/{workspace_id}")

            from_version = entry.version
            migrated_data = migration_fn(entry.state_data)
            entry.state_data = migrated_data
            entry.version = target_version
            entry.migration_history.append({
                "from_version": from_version,
                "to_version": target_version,
                "applied_at": datetime.now(timezone.utc).isoformat(),
            })
            entry.updated_at = datetime.now(timezone.utc).isoformat()
            self._save()

    def _save(self) -> None:
        if not self._persistence_file:
            return
        data = {}
        for (t, w, p), entry in self._entries.items():
            k = f"{t}:{w}:{p}"
            data[k] = {
                "tenant_id": entry.tenant_id,
                "workspace_id": entry.workspace_id,
                "plugin_id": entry.plugin_id,
                "version": entry.version,
                "enabled": entry.enabled,
                "permissions_revoked": entry.permissions_revoked,
                "state_data": entry.state_data,
                "migration_history": entry.migration_history,
                "created_at": entry.created_at,
                "updated_at": entry.updated_at,
            }
        self._persistence_file.parent.mkdir(parents=True, exist_ok=True)
        self._persistence_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def _load(self) -> None:
        if not self._persistence_file or not self._persistence_file.is_file():
            return
        try:
            data = json.loads(self._persistence_file.read_text(encoding="utf-8"))
            for k, v in data.items():
                entry = PluginStateEntry(
                    tenant_id=v["tenant_id"],
                    workspace_id=v["workspace_id"],
                    plugin_id=v["plugin_id"],
                    version=v["version"],
                    enabled=v.get("enabled", True),
                    permissions_revoked=v.get("permissions_revoked", False),
                    state_data=v.get("state_data", {}),
                    migration_history=v.get("migration_history", []),
                    created_at=v.get("created_at", ""),
                    updated_at=v.get("updated_at", ""),
                )
                self._entries[(entry.tenant_id, entry.workspace_id, entry.plugin_id)] = entry
        except Exception as e:
            logger.warning(f"Failed to load plugin state repository: {e}")
