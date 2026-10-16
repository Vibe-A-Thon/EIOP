"""Plugin Loader — discovers and loads plugins from directories and registries."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from eoip.plugins.sdk import PluginCapability, PluginManifest, PluginPermission

logger = logging.getLogger(__name__)


class PluginDiscovery:
    """Discovers plugin manifests from filesystem directories."""

    MANIFEST_FILENAME = "plugin.json"

    def __init__(self, plugin_dirs: list[str | Path] | None = None) -> None:
        self._dirs = [Path(d) for d in (plugin_dirs or [])]

    def add_directory(self, path: str | Path) -> None:
        self._dirs.append(Path(path))

    def discover(self) -> list[tuple[PluginManifest, str]]:
        results: list[tuple[PluginManifest, str]] = []
        for d in self._dirs:
            if not d.is_dir():
                continue
            for manifest_path in d.rglob(self.MANIFEST_FILENAME):
                try:
                    manifest, module_path = self._parse_manifest(manifest_path)
                    results.append((manifest, module_path))
                except Exception as e:
                    logger.warning("Failed to parse %s: %s", manifest_path, e)
        return results

    def _parse_manifest(self, manifest_path: Path) -> tuple[PluginManifest, str]:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        capabilities = [PluginCapability(c) for c in data.get("capabilities", [])]
        permissions = [
            PluginPermission(resource=p["resource"], scope=p.get("scope", "*"))
            for p in data.get("permissions", [])
        ]

        manifest = PluginManifest(
            plugin_id=data["plugin_id"],
            name=data["name"],
            version=data["version"],
            author=data.get("author", "Unknown"),
            description=data.get("description", ""),
            capabilities=capabilities,
            entry_point=data["entry_point"],
            permissions=permissions,
            min_platform_version=data.get("min_platform_version", "1.0.0"),
            tags=data.get("tags", []),
            config_schema=data.get("config_schema", {}),
            homepage=data.get("homepage", ""),
            license=data.get("license", "Proprietary"),
        )

        plugin_dir = manifest_path.parent
        entry_module = data["entry_point"].split(":")[0]
        module_path = str(plugin_dir / entry_module.replace(".", "/")) + ".py"
        if not Path(module_path).exists():
            module_path = str(plugin_dir / (entry_module.split(".")[-1] + ".py"))

        return manifest, module_path


class PluginLoader:
    """High-level loader that combines discovery with runtime loading."""

    def __init__(self, runtime, discovery: PluginDiscovery | None = None) -> None:
        self._runtime = runtime
        self._discovery = discovery or PluginDiscovery()

    def load_from_directory(self, path: str | Path,
                            configs: dict[str, dict[str, Any]] | None = None) -> list[str]:
        self._discovery.add_directory(path)
        discovered = self._discovery.discover()
        loaded_ids: list[str] = []

        for manifest, module_path in discovered:
            try:
                config = (configs or {}).get(manifest.plugin_id, {})
                self._runtime.load_plugin(manifest, module_path, config)
                loaded_ids.append(manifest.plugin_id)
            except Exception as e:
                logger.error("Failed to load plugin %s: %s", manifest.plugin_id, e)

        return loaded_ids

    def load_single(self, manifest_path: str | Path,
                    config: dict[str, Any] | None = None) -> str:
        manifest, module_path = self._discovery._parse_manifest(Path(manifest_path))
        self._runtime.load_plugin(manifest, module_path, config)
        return manifest.plugin_id
