"""Plugin SDK — base classes and manifest for building EOIP extensions.

A plugin is a Python module that subclasses one of the base plugin types
(ConnectorPlugin, TransformPlugin, ValidatorPlugin, AgentPlugin) and ships
a manifest describing its capabilities, version, and permissions.
"""

from __future__ import annotations

import abc
import hashlib
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Protocol


class PluginCapability(str, Enum):
    CONNECTOR = "CONNECTOR"
    TRANSFORM = "TRANSFORM"
    VALIDATOR = "VALIDATOR"
    AGENT = "AGENT"
    RETRIEVAL_STRATEGY = "RETRIEVAL_STRATEGY"
    QUERY_DIALECT = "QUERY_DIALECT"
    EXPORT_FORMAT = "EXPORT_FORMAT"
    INGESTION_HOOK = "INGESTION_HOOK"
    SCHEMA_ENRICHER = "SCHEMA_ENRICHER"
    DASHBOARD_WIDGET = "DASHBOARD_WIDGET"


class PluginStatus(str, Enum):
    DISCOVERED = "DISCOVERED"
    LOADED = "LOADED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    ERROR = "ERROR"
    UNLOADED = "UNLOADED"


@dataclass
class PluginPermission:
    resource: str  # graph_read, graph_write, network, filesystem, secrets
    scope: str = "*"
    granted: bool = False


@dataclass
class PluginManifest:
    plugin_id: str
    name: str
    version: str
    author: str
    description: str
    capabilities: list[PluginCapability]
    entry_point: str  # module:ClassName
    permissions: list[PluginPermission] = field(default_factory=list)
    min_platform_version: str = "1.0.0"
    tags: list[str] = field(default_factory=list)
    config_schema: dict[str, Any] = field(default_factory=dict)
    homepage: str = ""
    license: str = "Proprietary"

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["capabilities"] = [c.value for c in self.capabilities]
        return d

    def fingerprint(self) -> str:
        content = f"{self.plugin_id}:{self.version}:{self.entry_point}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]


class PluginBase(abc.ABC):
    """Base class all plugins must extend."""

    manifest: PluginManifest

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self._config = config or {}
        self._status = PluginStatus.DISCOVERED
        self._loaded_at: str | None = None
        self._error: str | None = None
        self._metrics: dict[str, int] = {"invocations": 0, "errors": 0}

    @property
    def status(self) -> PluginStatus:
        return self._status

    @property
    def plugin_id(self) -> str:
        return self.manifest.plugin_id

    @abc.abstractmethod
    def activate(self) -> None:
        """Called when the plugin is loaded and ready to serve requests."""

    @abc.abstractmethod
    def deactivate(self) -> None:
        """Called before the plugin is unloaded."""

    def health_check(self) -> dict[str, Any]:
        return {
            "plugin_id": self.plugin_id,
            "status": self._status.value,
            "metrics": dict(self._metrics),
            "error": self._error,
        }

    def _record_invocation(self) -> None:
        self._metrics["invocations"] += 1

    def _record_error(self, error: str) -> None:
        self._metrics["errors"] += 1
        self._error = error


class ConnectorPlugin(PluginBase):
    """Plugin that connects to external systems and fetches data."""

    @abc.abstractmethod
    def connect(self, connection_config: dict[str, Any]) -> bool:
        """Establish connection to the external system."""

    @abc.abstractmethod
    def discover(self) -> list[dict[str, Any]]:
        """Discover available resources/entity types."""

    @abc.abstractmethod
    def fetch(self, entity_type: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Fetch records of the given entity type."""

    @abc.abstractmethod
    def test_connection(self) -> dict[str, Any]:
        """Test connectivity and return status."""

    def supports_incremental(self) -> bool:
        return False

    def supports_webhooks(self) -> bool:
        return False


class TransformPlugin(PluginBase):
    """Plugin that transforms data during ingestion."""

    @abc.abstractmethod
    def transform(self, records: list[dict[str, Any]], context: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Transform a batch of records."""

    def validate_config(self) -> list[str]:
        return []


class ValidatorPlugin(PluginBase):
    """Plugin that validates entities before graph insertion."""

    @abc.abstractmethod
    def validate(self, entity: dict[str, Any], schema: dict[str, Any] | None = None) -> tuple[bool, list[str]]:
        """Validate an entity. Returns (is_valid, list_of_errors)."""

    def severity(self) -> str:
        return "WARNING"


class AgentPlugin(PluginBase):
    """Plugin that provides custom agent behavior."""

    @abc.abstractmethod
    def execute(self, query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute the agent's logic given a query."""

    def capabilities(self) -> list[str]:
        return []
