"""Connector SDK: source system adapters for Jira, Git, GitLab, and more."""

from eoip.connectors.base import (
    ConnectorHealth,
    DiscoveredResource,
    DiscoveryResult,
    DiscoveryScope,
    SourceConnector,
)
from eoip.connectors.files import FileParsingConnector, FileParsingScope
from eoip.connectors.generic import LocalFileConnector, LocalFileScope, WebSourceConnector
from eoip.connectors.github import GitHubConnector
from eoip.connectors.gitlab import GitLabConnector
from eoip.connectors.jira import JiraConnector
from eoip.connectors.registry import SourceRegistry

__all__ = [
    "ConnectorHealth",
    "DiscoveredResource",
    "DiscoveryResult",
    "DiscoveryScope",
    "FileParsingConnector",
    "FileParsingScope",
    "GitHubConnector",
    "GitLabConnector",
    "JiraConnector",
    "LocalFileConnector",
    "LocalFileScope",
    "SourceConnector",
    "SourceRegistry",
    "WebSourceConnector",
]
