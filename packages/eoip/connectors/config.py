"""Environment-backed configuration for on-prem REST connectors."""

from __future__ import annotations

import os
from collections.abc import Mapping
from uuid import uuid4

from eoip.connectors.confluence import ConfluenceConnector
from eoip.connectors.errors import ConnectorError
from eoip.connectors.github import GitHubConnector
from eoip.connectors.gitlab import GitLabConnector
from eoip.connectors.jira import JiraConnector
from eoip.connectors.servicenow import ServiceNowConnector
from eoip.contracts.source_registry import SourceRegistryEntry


def connector_from_environment(
    source_system: str,
    *,
    correlation_id: str | None = None,
    environ: Mapping[str, str] | None = None,
):
    """Build a source connector from environment values without serializing secrets."""
    variables = os.environ if environ is None else environ
    prefix = {"confluence": "EOIP_CONFLUENCE", "servicenow": "EOIP_SERVICENOW"}.get(source_system)
    correlation_id = correlation_id or str(uuid4())
    if prefix is None:
        raise ValueError(f"unsupported REST connector: {source_system}")

    base_url = variables.get(f"{prefix}_URL", "").strip()
    token = variables.get(f"{prefix}_TOKEN", "").strip() or None
    username = variables.get(f"{prefix}_USERNAME", "").strip() or None
    password = variables.get(f"{prefix}_PASSWORD", "") or None
    if not base_url or bool(username) != bool(password) or (token and username) or not (token or username):
        raise ConnectorError(source_system, "configuration_error", correlation_id)

    connector_class = {
        "confluence": ConfluenceConnector,
        "servicenow": ServiceNowConnector,
    }[source_system]
    try:
        return connector_class(base_url, token=token, username=username, password=password)
    except ValueError as exc:
        raise ConnectorError(source_system, "configuration_error", correlation_id) from exc


def connector_from_registry(
    entry: SourceRegistryEntry,
    *,
    correlation_id: str | None = None,
    environ: Mapping[str, str] | None = None,
):
    """Create a supported adapter from registry config and referenced environment secrets."""

    variables = os.environ if environ is None else environ
    correlation_id = correlation_id or str(uuid4())
    connector_class = {
        "confluence": ConfluenceConnector,
        "servicenow": ServiceNowConnector,
    }.get(entry.source_type)
    if entry.source_type == "github":
        token = _resolve_registry_secret(entry, "token", variables, correlation_id)
        if not token:
            raise ConnectorError(entry.source_type, "configuration_error", correlation_id)
        try:
            return GitHubConnector(
                entry.source_id,
                entry.base_url or "",
                token,
                repositories=list(entry.config.get("repositories", [])),
                organizations=list(entry.config.get("organizations", [])),
                api_version=str(entry.config.get("api_version", "2022-11-28")),
                include_pages=bool(entry.config.get("include_pages", False)),
                include_readme=bool(entry.config.get("include_readme", True)),
                page_size=int(entry.config.get("page_size", 100)),
                max_pages=int(entry.config.get("max_pages", 1000)),
                max_document_bytes=int(entry.config.get("max_document_bytes", 2_000_000)),
            )
        except (TypeError, ValueError) as exc:
            raise ConnectorError(entry.source_type, "configuration_error", correlation_id) from exc
    if entry.source_type == "gitlab":
        token = _resolve_registry_secret(entry, "token", variables, correlation_id)
        if not token:
            raise ConnectorError(entry.source_type, "configuration_error", correlation_id)
        try:
            return GitLabConnector(
                entry.source_id,
                entry.base_url or "",
                token,
                projects=list(entry.config.get("projects", [])),
                groups=list(entry.config.get("groups", [])),
                include_wikis=bool(entry.config.get("include_wikis", True)),
                include_pages=bool(entry.config.get("include_pages", True)),
                include_readme=bool(entry.config.get("include_readme", True)),
                include_merge_request_diffs=bool(
                    entry.config.get("include_merge_request_diffs", True)
                ),
                pages_scopes=dict(entry.config.get("pages_scopes", {})),
                page_size=int(entry.config.get("page_size", 100)),
                max_pages=int(entry.config.get("max_pages", 1000)),
                max_document_bytes=int(entry.config.get("max_document_bytes", 2_000_000)),
            )
        except (TypeError, ValueError) as exc:
            raise ConnectorError(entry.source_type, "configuration_error", correlation_id) from exc
    if entry.source_type == "jira":
        token = _resolve_registry_secret(entry, "token", variables, correlation_id)
        username = _resolve_registry_secret(entry, "username", variables, correlation_id)
        password = _resolve_registry_secret(entry, "password", variables, correlation_id)
        try:
            return JiraConnector(
                entry.source_id,
                entry.base_url or "",
                projects=list(entry.config.get("projects", [])),
                token=token,
                username=username,
                password=password,
                api_version=str(entry.config.get("api_version", "3")),
                search_mode=str(entry.config.get("search_mode", "enhanced")),
                fields=list(entry.config.get("fields", [])) or None,
                include_comments=bool(entry.config.get("include_comments", True)),
                include_changelog=bool(entry.config.get("include_changelog", True)),
                include_sprints=bool(entry.config.get("include_sprints", False)),
                page_size=int(entry.config.get("page_size", 100)),
                max_pages=int(entry.config.get("max_pages", 1000)),
            )
        except (TypeError, ValueError) as exc:
            raise ConnectorError(entry.source_type, "configuration_error", correlation_id) from exc
    if connector_class is None:
        raise ConnectorError(entry.source_type, "adapter_unavailable", correlation_id)

    token = _resolve_registry_secret(entry, "token", variables, correlation_id)
    username = _resolve_registry_secret(entry, "username", variables, correlation_id)
    password = _resolve_registry_secret(entry, "password", variables, correlation_id)
    if bool(username) != bool(password) or (token and username) or not (token or username):
        raise ConnectorError(entry.source_type, "configuration_error", correlation_id)
    try:
        return connector_class(
            entry.base_url or "",
            token=token,
            username=username,
            password=password,
            page_size=int(entry.config.get("page_size", 100)),
        )
    except (TypeError, ValueError) as exc:
        raise ConnectorError(entry.source_type, "configuration_error", correlation_id) from exc


def _resolve_registry_secret(
    entry: SourceRegistryEntry,
    name: str,
    variables: Mapping[str, str],
    correlation_id: str,
) -> str | None:
    reference = entry.secret_refs.get(name)
    if reference is None:
        return None
    if not reference.startswith("env://"):
        raise ConnectorError(entry.source_type, "secret_provider_unavailable", correlation_id)
    value = variables.get(reference.removeprefix("env://"), "")
    return value or None
