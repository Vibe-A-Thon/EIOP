"""Connector SDK: source system adapters for Jira, Git, GitLab, and more."""

from eoip.connectors.base import (
    ConnectorHealth,
    DiscoveredResource,
    DiscoveryResult,
    DiscoveryScope,
    SourceConnector,
)
from eoip.connectors.factory import (
    ApplicationCategory,
    ApplicationSpec,
    ConnectionFactory,
    ConnectorFactory,
    GenericAgileConnector,
    GenericRestApplicationConnector,
    connection_factory,
    get_connection_factory,
)
from eoip.connectors.files import FileParsingConnector, FileParsingScope
from eoip.connectors.generic import LocalFileConnector, LocalFileScope, WebSourceConnector
from eoip.connectors.github import GitHubConnector
from eoip.connectors.gitlab import GitLabConnector
from eoip.connectors.jira import JiraConnector
from eoip.connectors.registry import SourceRegistry

__all__ = [
    "ApplicationCategory",
    "ApplicationSpec",
    "ConnectionFactory",
    "ConnectorFactory",
    "ConnectorHealth",
    "DiscoveredResource",
    "DiscoveryResult",
    "DiscoveryScope",
    "FileParsingConnector",
    "FileParsingScope",
    "GenericAgileConnector",
    "GenericRestApplicationConnector",
    "GitHubConnector",
    "GitLabConnector",
    "JiraConnector",
    "LocalFileConnector",
    "LocalFileScope",
    "SourceConnector",
    "SourceRegistry",
    "WebSourceConnector",
    "connection_factory",
    "get_connection_factory",
]
