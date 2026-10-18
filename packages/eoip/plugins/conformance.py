"""Plugin conformance runner, templates, synthetic fixtures, and qualification governance (CRA-039.3)."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Type

from eoip.capabilities.model import CapabilityState
from eoip.marketplace.semver import parse_range, parse_version
from eoip.plugins.sdk import PluginBase, PluginCapability, PluginManifest, PluginPermission

logger = logging.getLogger("eoip.plugins.conformance")

# Documented platform compatibility matrix
SUPPORTED_PLATFORM_VERSIONS = {
    "1.0.0": {"status": "SUPPORTED", "min_python": "3.10"},
    "1.1.0": {"status": "SUPPORTED", "min_python": "3.10"},
    "1.2.0": {"status": "CURRENT", "min_python": "3.11"},
}


class ConnectorPluginTemplate:
    """Template for scaffolding compliant custom connectors."""

    @staticmethod
    def generate_scaffold(plugin_id: str, connector_name: str) -> dict[str, str]:
        manifest_code = f"""from eoip.plugins.sdk import PluginCapability, PluginManifest, PluginPermission

manifest = PluginManifest(
    plugin_id="{plugin_id}",
    name="{connector_name}",
    version="1.0.0",
    author="Community Contributor",
    description="Compliant custom connector plugin for {connector_name}",
    capabilities=[PluginCapability.CONNECTOR],
    entry_point="{plugin_id}.connector:CustomConnectorPlugin",
    permissions=[PluginPermission(resource="network", scope="https://api.{plugin_id}.example.com", granted=True)],
    min_platform_version="1.0.0",
)
"""
        impl_code = f"""from eoip.plugins.sdk import PluginBase, PluginStatus

class CustomConnectorPlugin(PluginBase):
    def activate(self) -> None:
        self._status = PluginStatus.ACTIVE

    def deactivate(self) -> None:
        self._status = PluginStatus.UNLOADED

    def poll_records(self) -> list[dict]:
        return [{{"id": "rec-1", "source": "{plugin_id}"}}]
"""
        return {
            "manifest.py": manifest_code,
            "connector.py": impl_code,
        }


@dataclass
class ConformanceCheckResult:
    check_name: str
    passed: bool
    details: str


@dataclass
class ConformanceReport:
    plugin_id: str
    passed: bool
    qualification_state: CapabilityState
    checks: list[ConformanceCheckResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "plugin_id": self.plugin_id,
            "passed": self.passed,
            "qualification_state": self.qualification_state.value,
            "checks": [
                {"name": c.check_name, "passed": c.passed, "details": c.details}
                for c in self.checks
            ],
            "errors": self.errors,
        }


class PluginConformanceRunner:
    """Automated qualification runner certifying custom plugins against security and lifecycle standards."""

    def __init__(self, certified_maintainers: set[str] | None = None) -> None:
        self.certified_maintainers = certified_maintainers or {"EOIP-Core-Team", "Certified-Partner"}

    def run_conformance(self, plugin_cls: Type[PluginBase], manifest: PluginManifest) -> ConformanceReport:
        checks: list[ConformanceCheckResult] = []
        errors: list[str] = []

        # 1. Manifest verification
        try:
            parse_version(manifest.version)
            manifest_ok = (
                bool(manifest.plugin_id)
                and bool(manifest.name)
                and len(manifest.capabilities) > 0
                and manifest.min_platform_version in SUPPORTED_PLATFORM_VERSIONS
            )
            checks.append(
                ConformanceCheckResult(
                    "manifest_specification",
                    manifest_ok,
                    "Manifest is valid and targets supported platform version" if manifest_ok else "Manifest fields missing",
                )
            )
            if not manifest_ok:
                errors.append("Invalid manifest metadata or unsupported min_platform_version")
        except Exception as exc:
            checks.append(ConformanceCheckResult("manifest_specification", False, str(exc)))
            errors.append(f"Manifest parse error: {exc}")

        # 2. Lifecycle hooks verification
        lifecycle_ok = False
        try:
            instance = plugin_cls({"mock_config": True})
            instance.activate()
            active = instance.status.value in ("ACTIVE", "LOADED")
            instance.deactivate()
            unloaded = instance.status.value in ("UNLOADED", "DISCOVERED", "PAUSED")
            lifecycle_ok = active and unloaded
            checks.append(
                ConformanceCheckResult(
                    "lifecycle_hooks",
                    lifecycle_ok,
                    "activate() and deactivate() transitions succeeded" if lifecycle_ok else "Lifecycle transitions failed",
                )
            )
            if not lifecycle_ok:
                errors.append("Plugin lifecycle failed to transition status correctly")
        except Exception as exc:
            checks.append(ConformanceCheckResult("lifecycle_hooks", False, str(exc)))
            errors.append(f"Lifecycle hook raised exception: {exc}")

        # 3. Security & Permission Bounds
        permissions_ok = True
        for perm in manifest.permissions:
            if not perm.resource or perm.resource not in {"network", "filesystem", "graph_read", "graph_write", "secrets"}:
                permissions_ok = False
                break
        checks.append(
            ConformanceCheckResult(
                "permission_bounds",
                permissions_ok,
                "All permissions are scoped to known resources" if permissions_ok else "Invalid permission resource requested",
            )
        )
        if not permissions_ok:
            errors.append("Manifest requests unknown or illegal permission resource")

        # 4. Error Isolation
        error_isolation_ok = True
        try:
            failing_instance = plugin_cls(None)
            failing_instance.activate()
            failing_instance.deactivate()
        except Exception:
            error_isolation_ok = False
        checks.append(
            ConformanceCheckResult(
                "error_isolation",
                error_isolation_ok,
                "Plugin gracefully handles empty configuration" if error_isolation_ok else "Plugin crashes on empty config",
            )
        )
        if not error_isolation_ok:
            errors.append("Plugin does not isolate errors on missing configuration")

        all_passed = len(errors) == 0 and all(c.passed for c in checks)

        # Qualification determination: uncertified community modules remain visibly UNQUALIFIED
        is_certified_author = manifest.author in self.certified_maintainers
        if all_passed and is_certified_author:
            qualification_state = CapabilityState.SUPPORTED_QUALIFIED
        elif all_passed:
            qualification_state = CapabilityState.SUPPORTED_UNQUALIFIED
        else:
            qualification_state = CapabilityState.UNSUPPORTED

        return ConformanceReport(
            plugin_id=manifest.plugin_id,
            passed=all_passed,
            qualification_state=qualification_state,
            checks=checks,
            errors=errors,
        )
