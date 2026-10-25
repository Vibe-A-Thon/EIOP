"""Plugin Runtime — sandboxed execution environment with hot-reload support."""

from __future__ import annotations

import importlib
import importlib.util
import logging
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from eoip.plugins.sdk import (
    PluginBase, PluginCapability, PluginManifest, PluginStatus,
)

logger = logging.getLogger(__name__)


@dataclass
class PluginSandboxConfig:
    max_memory_mb: int = 256
    max_cpu_seconds: int = 30
    allowed_imports: set[str] = field(default_factory=lambda: {
        "json", "re", "hashlib", "uuid", "time", "datetime", "math",
        "collections", "itertools", "functools", "dataclasses", "typing",
        "pathlib", "urllib.parse", "base64", "csv", "io", "copy",
    })
    network_access: bool = False
    filesystem_access: bool = False
    max_result_size_bytes: int = 10 * 1024 * 1024


class PluginSandbox:
    """Restricted execution environment for plugins."""

    def __init__(self, config: PluginSandboxConfig | None = None) -> None:
        self._config = config or PluginSandboxConfig()
        self._restricted_builtins = {
            "__import__", "exec", "eval", "compile", "open",
            "breakpoint", "exit", "quit",
        }

    def check_permissions(self, manifest: PluginManifest) -> list[str]:
        violations: list[str] = []
        for perm in manifest.permissions:
            if perm.resource == "network" and not self._config.network_access:
                violations.append(f"Network access denied for {manifest.plugin_id}")
            if perm.resource == "filesystem" and not self._config.filesystem_access:
                violations.append(f"Filesystem access denied for {manifest.plugin_id}")
        return violations

    def wrap_execution(self, func, *args, timeout: float | None = None, **kwargs) -> Any:
        timeout = timeout or self._config.max_cpu_seconds
        result_holder: list[Any] = []
        error_holder: list[Exception] = []

        import contextvars

        ctx = contextvars.copy_context()  # the worker thread keeps the caller's tenant scope

        def _run():
            try:
                result_holder.append(ctx.run(func, *args, **kwargs))
            except Exception as e:
                error_holder.append(e)

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        thread.join(timeout=timeout)

        if thread.is_alive():
            raise TimeoutError(f"Plugin execution exceeded {timeout}s limit")
        if error_holder:
            raise error_holder[0]
        return result_holder[0] if result_holder else None


@dataclass
class LoadedPlugin:
    manifest: PluginManifest
    instance: PluginBase
    module_path: str
    loaded_at: str
    file_mtime: float = 0.0
    reload_count: int = 0


class PluginRuntime:
    """Manages plugin lifecycle: discovery, loading, hot-reload, and execution."""

    def __init__(self, sandbox: PluginSandbox | None = None) -> None:
        self._sandbox = sandbox or PluginSandbox()
        self.invocations: list[dict[str, Any]] = []  # tenant-tagged invocation log (SR-TEN-001)
        self._plugins: dict[str, LoadedPlugin] = {}
        self._lock = threading.RLock()
        self._hooks: dict[str, list[str]] = {}  # capability -> [plugin_ids]

    def load_plugin(self, manifest: PluginManifest, module_path: str,
                    config: dict[str, Any] | None = None) -> LoadedPlugin:
        with self._lock:
            violations = self._sandbox.check_permissions(manifest)
            if violations:
                raise PermissionError(f"Plugin {manifest.plugin_id} denied: {violations}")

            instance = self._instantiate(manifest.entry_point, module_path, config)
            instance.manifest = manifest

            try:
                instance.activate()
                instance._status = PluginStatus.ACTIVE
                instance._loaded_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            except Exception as e:
                instance._status = PluginStatus.ERROR
                instance._record_error(str(e))
                raise

            loaded = LoadedPlugin(
                manifest=manifest,
                instance=instance,
                module_path=module_path,
                loaded_at=instance._loaded_at,
                file_mtime=self._get_mtime(module_path),
            )
            self._plugins[manifest.plugin_id] = loaded

            for cap in manifest.capabilities:
                self._hooks.setdefault(cap.value, []).append(manifest.plugin_id)

            logger.info("Loaded plugin %s v%s", manifest.plugin_id, manifest.version)
            return loaded

    def unload_plugin(self, plugin_id: str) -> bool:
        with self._lock:
            loaded = self._plugins.get(plugin_id)
            if not loaded:
                return False

            try:
                loaded.instance.deactivate()
            except Exception:
                logger.warning("Error deactivating plugin %s", plugin_id)

            loaded.instance._status = PluginStatus.UNLOADED

            for cap_list in self._hooks.values():
                if plugin_id in cap_list:
                    cap_list.remove(plugin_id)

            del self._plugins[plugin_id]
            logger.info("Unloaded plugin %s", plugin_id)
            return True

    def reload_plugin(self, plugin_id: str) -> LoadedPlugin:
        with self._lock:
            loaded = self._plugins.get(plugin_id)
            if not loaded:
                raise ValueError(f"Plugin {plugin_id} not loaded")

            config = loaded.instance._config
            manifest = loaded.manifest
            module_path = loaded.module_path
            reload_count = loaded.reload_count

            self.unload_plugin(plugin_id)

            module_name = manifest.entry_point.split(":")[0]
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])

            new_loaded = self.load_plugin(manifest, module_path, config)
            new_loaded.reload_count = reload_count + 1
            logger.info("Hot-reloaded plugin %s (reload #%d)", plugin_id, new_loaded.reload_count)
            return new_loaded

    def check_for_changes(self) -> list[str]:
        changed: list[str] = []
        with self._lock:
            for pid, loaded in self._plugins.items():
                current_mtime = self._get_mtime(loaded.module_path)
                if current_mtime > loaded.file_mtime:
                    changed.append(pid)
        return changed

    def hot_reload_changed(self) -> list[str]:
        changed = self.check_for_changes()
        reloaded: list[str] = []
        for pid in changed:
            try:
                self.reload_plugin(pid)
                reloaded.append(pid)
            except Exception as e:
                logger.error("Failed to hot-reload %s: %s", pid, e)
        return reloaded

    def get_plugin(self, plugin_id: str) -> PluginBase | None:
        loaded = self._plugins.get(plugin_id)
        return loaded.instance if loaded else None

    def get_plugins_by_capability(self, capability: PluginCapability) -> list[PluginBase]:
        with self._lock:
            pids = self._hooks.get(capability.value, [])
            return [self._plugins[pid].instance for pid in pids if pid in self._plugins]

    def list_plugins(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {
                    "plugin_id": loaded.manifest.plugin_id,
                    "name": loaded.manifest.name,
                    "version": loaded.manifest.version,
                    "status": loaded.instance.status.value,
                    "capabilities": [c.value for c in loaded.manifest.capabilities],
                    "loaded_at": loaded.loaded_at,
                    "reload_count": loaded.reload_count,
                    "health": loaded.instance.health_check(),
                }
                for loaded in self._plugins.values()
            ]

    def execute_plugin(self, plugin_id: str, method: str, *args,
                       timeout: float | None = None, invocation_tenant: str | None = None,
                       **kwargs) -> Any:
        """Run a plugin method inside the tenant scope (SR-TEN-001).

        ``invocation_tenant`` defaults to the caller's ambient scope (``current_tenant()``); every
        invocation is recorded in ``self.invocations`` with its tenant and the plugin can read
        ``current_tenant()``.
        """
        from eoip.contracts.tenant_scope import current_tenant, tenant_scope

        tenant = invocation_tenant if invocation_tenant is not None else current_tenant()
        with tenant_scope(tenant):
            self.invocations.append({"plugin_id": plugin_id, "method": method, "tenant_id": tenant,
                                     "at": time.time()})
            return self._execute_plugin(plugin_id, method, *args, timeout=timeout, **kwargs)

    def _execute_plugin(self, plugin_id: str, method: str, *args,
                        timeout: float | None = None, **kwargs) -> Any:
        loaded = self._plugins.get(plugin_id)
        if not loaded:
            raise ValueError(f"Plugin {plugin_id} not loaded")
        if loaded.instance.status != PluginStatus.ACTIVE:
            raise RuntimeError(f"Plugin {plugin_id} is {loaded.instance.status.value}")

        func = getattr(loaded.instance, method, None)
        if func is None:
            raise AttributeError(f"Plugin {plugin_id} has no method '{method}'")

        loaded.instance._record_invocation()
        try:
            return self._sandbox.wrap_execution(func, *args, timeout=timeout, **kwargs)
        except Exception as e:
            loaded.instance._record_error(str(e))
            raise

    def _instantiate(self, entry_point: str, module_path: str,
                     config: dict[str, Any] | None) -> PluginBase:
        module_name, class_name = entry_point.rsplit(":", 1)

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if not spec or not spec.loader:
            raise ImportError(f"Cannot load module from {module_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        cls = getattr(module, class_name, None)
        if cls is None:
            raise ImportError(f"Class {class_name} not found in {module_path}")

        if not (isinstance(cls, type) and issubclass(cls, PluginBase)):
            raise TypeError(f"{class_name} must subclass PluginBase")

        return cls(config=config)

    def _get_mtime(self, path: str) -> float:
        try:
            return Path(path).stat().st_mtime
        except OSError:
            return 0.0
