"""EOIP Plugin SDK — sandboxed hot-reload extension framework for custom connectors, transforms, agents, and validators."""

from eoip.plugins.sdk import (
    PluginBase, ConnectorPlugin, TransformPlugin, ValidatorPlugin,
    AgentPlugin, PluginManifest, PluginCapability, PluginStatus,
)
from eoip.plugins.runtime import PluginRuntime, PluginSandbox
from eoip.plugins.loader import PluginLoader, PluginDiscovery
from eoip.plugins.contracts import (
    ConnectorContract,
    ParserContract,
    MapperContract,
    GraphStoreContract,
    SemanticEngineContract,
    SearchVectorIndexContract,
    ModelProviderContract,
    WorkflowActionContract,
    UIContributionContract,
    ContractNegotiationResult,
    negotiate_contracts,
)
from eoip.plugins.manifest import (
    SignedPluginManifest,
    PluginPermission,
    PluginUninstallPolicy,
    ManifestValidationError,
    load_signed_manifest,
)
from eoip.plugins.state import (
    PluginStateEntry,
    PluginStateRepository,
)

__all__ = [
    "PluginBase", "ConnectorPlugin", "TransformPlugin", "ValidatorPlugin",
    "AgentPlugin", "PluginManifest", "PluginCapability", "PluginStatus",
    "PluginRuntime", "PluginSandbox", "PluginLoader", "PluginDiscovery",
    "ConnectorContract", "ParserContract", "MapperContract", "GraphStoreContract",
    "SemanticEngineContract", "SearchVectorIndexContract", "ModelProviderContract",
    "WorkflowActionContract", "UIContributionContract", "ContractNegotiationResult",
    "negotiate_contracts", "SignedPluginManifest", "PluginPermission",
    "PluginUninstallPolicy", "ManifestValidationError", "load_signed_manifest",
    "PluginStateEntry", "PluginStateRepository",
]

