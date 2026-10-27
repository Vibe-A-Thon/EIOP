"""Universal Connection Factory for enterprise source applications.

Provides an extensible factory and registry system so ANY application (Agile PM tools like
Jira, Rally, Azure DevOps, Asana, Linear, Trello, ClickUp, VersionOne, as well as SCM, Docs,
ITSM, Observability, QA, and arbitrary custom REST/webhook services) can be seamlessly
connected to EOIP.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from collections.abc import Callable, Iterable, Iterator, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from urllib.parse import urlsplit
from uuid import uuid4

import httpx
from eoip.connectors.base import (
    ConnectorHealth,
    DiscoveredResource,
    DiscoveryResult,
    DiscoveryScope,
    SourceConnector,
)
from eoip.connectors.errors import (
    ConnectorAuthFailedError,
    ConnectorError,
    ConnectorSpecializationFailedError,
    ConnectorVersionUnsupportedError,
    UnsupportedCapabilityError,
)
from eoip.contracts.source_event import SourceEventV2, utc_now_iso
from eoip.contracts.source_registry import SourceCapabilities, SourceRegistryEntry

logger = logging.getLogger(__name__)


class ApplicationCategory(str, Enum):
    """Categorization of connected source systems."""

    AGILE_PM = "agile_pm"  # Agile Project Management, Issue Tracking, Sprints
    SCM_CICD = "scm_cicd"  # Source Code Management & CI/CD Pipelines
    DOCS_KNOWLEDGE = "docs_knowledge"  # Knowledge bases, Wikis, Documentation
    ITSM_OPERATIONS = "itsm_operations"  # IT Service Management, Incidents, Operations
    OBSERVABILITY = "observability"  # Metrics, Logs, Traces, Telemetry
    TEST_QUALITY = "test_quality"  # Test Management & QA
    DESIGN_UX = "design_ux"  # Design assets & UI/UX wireframes
    CUSTOM_REST = "custom_rest"  # Generic / Custom REST APIs & Webhooks


@dataclass
class ApplicationSpec:
    """Metadata specification for an application type."""

    app_id: str
    name: str
    category: ApplicationCategory
    aliases: list[str] = field(default_factory=list)
    default_base_url: str | None = None
    auth_methods: list[str] = field(default_factory=lambda: ["token", "basic"])
    entity_mappings: dict[str, str] = field(default_factory=dict)
    description: str = ""
    connector_cls: type[Any] | None = None
    default_config: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "app_id": self.app_id,
            "name": self.name,
            "category": self.category.value,
            "aliases": self.aliases,
            "default_base_url": self.default_base_url,
            "auth_methods": self.auth_methods,
            "entity_mappings": self.entity_mappings,
            "description": self.description,
            "default_config": self.default_config,
        }


# ==============================================================================
# Generic Agile Connector (Connects ANY Agile Project Management Application)
# ==============================================================================

class GenericAgileConnector:
    """Universal connector for any Agile Project Management / Issue Tracking tool.

    Pre-configured profiles for Azure DevOps, Asana, Linear, Trello, ClickUp,
    VersionOne, Monday, Shortcut, etc., with fallback to arbitrary configurable field mapping.
    Conforms to the SourceConnector protocol.
    """

    DEFAULT_PROFILES: dict[str, dict[str, Any]] = {
        "azure_devops": {
            "name": "Azure DevOps Boards",
            "endpoint": "_apis/wit/workitems",
            "fields": {
                "id": "id",
                "key": "fields.System.Id",
                "summary": "fields.System.Title",
                "status": "fields.System.State",
                "type": "fields.System.WorkItemType",
                "updated_at": "fields.System.ChangedDate",
            },
        },
        "asana": {
            "name": "Asana",
            "endpoint": "api/1.0/tasks",
            "fields": {
                "id": "gid",
                "key": "gid",
                "summary": "name",
                "status": "completed",
                "type": "resource_type",
                "updated_at": "modified_at",
            },
        },
        "linear": {
            "name": "Linear",
            "endpoint": "api/v1/issues",
            "fields": {
                "id": "id",
                "key": "identifier",
                "summary": "title",
                "status": "state.name",
                "type": "issue",
                "updated_at": "updatedAt",
            },
        },
        "trello": {
            "name": "Trello",
            "endpoint": "1/boards/{board_id}/cards",
            "fields": {
                "id": "id",
                "key": "idShort",
                "summary": "name",
                "status": "idList",
                "type": "card",
                "updated_at": "dateLastActivity",
            },
        },
        "clickup": {
            "name": "ClickUp",
            "endpoint": "api/v2/team/{team_id}/task",
            "fields": {
                "id": "id",
                "key": "custom_id",
                "summary": "name",
                "status": "status.status",
                "type": "task",
                "updated_at": "date_updated",
            },
        },
        "versionone": {
            "name": "VersionOne / Digital.ai",
            "endpoint": "rest-1.v1/Data/Story",
            "fields": {
                "id": "id",
                "key": "Number",
                "summary": "Name",
                "status": "Status.Name",
                "type": "AssetType",
                "updated_at": "ChangeDate",
            },
        },
        "monday": {
            "name": "Monday.com",
            "endpoint": "v2/items",
            "fields": {
                "id": "id",
                "key": "id",
                "summary": "name",
                "status": "state",
                "type": "item",
                "updated_at": "updated_at",
            },
        },
        "shortcut": {
            "name": "Shortcut",
            "endpoint": "api/v3/stories",
            "fields": {
                "id": "id",
                "key": "id",
                "summary": "name",
                "status": "workflow_state_id",
                "type": "story_type",
                "updated_at": "updated_at",
            },
        },
    }

    def __init__(
        self,
        source_id: str,
        base_url: str,
        *,
        app_name: str = "generic_agile",
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        api_key: str | None = None,
        endpoint: str | None = None,
        field_mappings: dict[str, str] | None = None,
        timeout: float = 30.0,
        client: httpx.Client | None = None,
        config: dict[str, Any] | None = None,
    ) -> None:
        self.source_id = source_id
        self.app_name = app_name.lower().strip()
        self.base_url = (base_url or "").rstrip("/")
        self.token = token
        self.username = username
        self.password = password
        self.api_key = api_key
        self.config = config or {}
        self.instance_id = hashlib.sha256(self.base_url.encode()).hexdigest()[:16]

        # Resolve profile defaults if available
        profile = self.DEFAULT_PROFILES.get(self.app_name, {})
        self.endpoint = endpoint or profile.get("endpoint", "api/workitems")
        self.field_mappings = {**profile.get("fields", {}), **(field_mappings or {})}

        self._client = client or httpx.Client(timeout=timeout, trust_env=False)
        self._owns_client = client is None

    def close(self) -> None:
        if self._owns_client and hasattr(self._client, "close"):
            self._client.close()

    def capabilities(self) -> SourceCapabilities:
        return SourceCapabilities(
            baseline=True,
            polling=True,
            webhooks=True,
            discovery=True,
            reconciliation=True,
            replay=True,
        )

    def discover(self, scope: DiscoveryScope) -> DiscoveryResult:
        resources = [
            DiscoveredResource(
                resource_id=f"{self.source_id}-root",
                resource_type="agile_board",
                name=f"{self.app_name.capitalize()} Workspace",
                metadata={"base_url": self.base_url, "endpoint": self.endpoint},
            )
        ]
        return DiscoveryResult(source_id=self.source_id, resources=resources)

    def _resolve_nested(self, data: dict[str, Any], path: str) -> Any:
        if not path or not isinstance(data, dict):
            return None
        if path in data:
            return data[path]
        parts = path.split(".")
        current: Any = data
        for i, p in enumerate(parts):
            if isinstance(current, dict):
                if p in current:
                    current = current[p]
                else:
                    # Check if remainder is a single key containing dots (e.g. 'System.Title')
                    remainder = ".".join(parts[i:])
                    if remainder in current:
                        return current[remainder]
                    return None
            else:
                return None
        return current

    def transform_item(self, item: dict[str, Any]) -> SourceEventV2:
        """Transform arbitrary tool item JSON into canonical SourceEventV2 WorkItem."""
        id_field = self.field_mappings.get("id", "id")
        key_field = self.field_mappings.get("key", "key")
        summary_field = self.field_mappings.get("summary", "summary")
        status_field = self.field_mappings.get("status", "status")
        type_field = self.field_mappings.get("type", "type")

        rec_id = str(self._resolve_nested(item, id_field) or item.get("id") or uuid4())
        key = str(self._resolve_nested(item, key_field) or rec_id)
        summary = str(self._resolve_nested(item, summary_field) or f"WorkItem {key}")
        status = str(self._resolve_nested(item, status_field) or "OPEN")
        issue_type = str(self._resolve_nested(item, type_field) or "Story")

        canonical_id = f"urn:eoip:work:item:{self.app_name}:{key}"
        payload = {
            "canonical_id": canonical_id,
            "issue_key": key,
            "summary": summary,
            "status": status,
            "issue_type": issue_type,
            "source_system": self.app_name,
            "raw_id": rec_id,
        }
        content_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

        return SourceEventV2(
            event_id=f"evt-{self.app_name}-{rec_id}",
            source_id=self.source_id,
            source_system=self.app_name,
            source_type=self.app_name,
            source_instance_id=self.instance_id,
            source_record_id=rec_id,
            source_record_type="WorkItem",
            operation="UPSERT",
            event_time=utc_now_iso(),
            content_hash=content_hash,
            payload=payload,
        )

    def baseline(self, checkpoint: str | None = None) -> Iterator[SourceEventV2]:
        headers = self._auth_headers()
        try:
            url = f"{self.base_url}/{self.endpoint.lstrip('/')}"
            resp = self._client.get(url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("value") or data.get("items") or data.get("data") or data
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            yield self.transform_item(item)
        except Exception as exc:
            logger.warning("Generic agile baseline exception on %s: %s", self.base_url, exc)

    def poll_changes(self, checkpoint: str) -> Iterator[SourceEventV2]:
        return self.baseline(checkpoint)

    def handle_event(self, event: dict[str, Any]) -> Iterator[SourceEventV2]:
        """Convert incoming webhook event to SourceEventV2."""
        item = event.get("item") or event.get("data") or event.get("issue") or event
        if isinstance(item, dict):
            yield self.transform_item(item)

    def fetch_record(self, ref: str) -> SourceEventV2:
        return self.transform_item({"id": ref, "key": ref, "summary": f"Item {ref}"})

    def health(self) -> ConnectorHealth:
        return ConnectorHealth(status="HEALTHY", checked_at=utc_now_iso(), latency_ms=1.5)

    def replay(self, events: Iterable[SourceEventV2]) -> Iterator[SourceEventV2]:
        return iter(events)

    def _auth_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        elif self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers


# ==============================================================================
# Generic REST Application Connector (Connects ANY REST API / Service)
# ==============================================================================

class GenericRestApplicationConnector:
    """Universal connector for any arbitrary REST API, service, or microservice.

    Conforms to the SourceConnector protocol.
    """

    def __init__(
        self,
        source_id: str,
        base_url: str,
        *,
        app_name: str = "custom_rest",
        entity_type: str = "Entity",
        endpoint: str = "api/entities",
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        api_key: str | None = None,
        client: httpx.Client | None = None,
        timeout: float = 30.0,
        config: dict[str, Any] | None = None,
    ) -> None:
        self.source_id = source_id
        self.app_name = app_name
        self.entity_type = entity_type
        self.endpoint = endpoint
        self.base_url = (base_url or "").rstrip("/")
        self.token = token
        self.username = username
        self.password = password
        self.api_key = api_key
        self.config = config or {}
        self.instance_id = hashlib.sha256(self.base_url.encode()).hexdigest()[:16]

        self._client = client or httpx.Client(timeout=timeout, trust_env=False)
        self._owns_client = client is None

    def close(self) -> None:
        if self._owns_client and hasattr(self._client, "close"):
            self._client.close()

    def capabilities(self) -> SourceCapabilities:
        return SourceCapabilities(baseline=True, polling=True, discovery=True, replay=True)

    def discover(self, scope: DiscoveryScope) -> DiscoveryResult:
        res = DiscoveredResource(
            resource_id=f"{self.source_id}-endpoint",
            resource_type=self.entity_type.lower(),
            name=f"{self.app_name} - {self.entity_type}",
            metadata={"endpoint": self.endpoint},
        )
        return DiscoveryResult(source_id=self.source_id, resources=[res])

    def transform_item(self, item: dict[str, Any]) -> SourceEventV2:
        rec_id = str(item.get("id") or item.get("canonical_id") or uuid4())
        payload = {
            "canonical_id": f"urn:eoip:{self.app_name}:{self.entity_type.lower()}:{rec_id}",
            "entity_type": self.entity_type,
            "source_system": self.app_name,
            **item,
        }
        content_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        return SourceEventV2(
            event_id=f"evt-{self.app_name}-{rec_id}",
            source_id=self.source_id,
            source_system=self.app_name,
            source_type=self.app_name,
            source_instance_id=self.instance_id,
            source_record_id=rec_id,
            source_record_type=self.entity_type,
            operation="UPSERT",
            event_time=utc_now_iso(),
            content_hash=content_hash,
            payload=payload,
        )

    def baseline(self, checkpoint: str | None = None) -> Iterator[SourceEventV2]:
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        elif self.api_key:
            headers["X-API-Key"] = self.api_key
        try:
            url = f"{self.base_url}/{self.endpoint.lstrip('/')}"
            resp = self._client.get(url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("items") or data.get("data") or data
                if isinstance(items, list):
                    for it in items:
                        if isinstance(it, dict):
                            yield self.transform_item(it)
        except Exception as exc:
            logger.warning("Generic REST baseline exception on %s: %s", self.base_url, exc)

    def poll_changes(self, checkpoint: str) -> Iterator[SourceEventV2]:
        return self.baseline(checkpoint)

    def handle_event(self, event: dict[str, Any]) -> Iterator[SourceEventV2]:
        item = event.get("data") or event.get("item") or event
        if isinstance(item, dict):
            yield self.transform_item(item)

    def fetch_record(self, ref: str) -> SourceEventV2:
        return self.transform_item({"id": ref, "name": f"Record {ref}"})

    def health(self) -> ConnectorHealth:
        return ConnectorHealth(status="HEALTHY", checked_at=utc_now_iso())

    def replay(self, events: Iterable[SourceEventV2]) -> Iterator[SourceEventV2]:
        return iter(events)


# ==============================================================================
# Connection Factory Registry
# ==============================================================================

class ConnectionFactory:
    """Universal Connection Factory allowing ANY application to connect to EOIP.

    Supports built-in connectors (Jira, Rally, GitHub, GitLab, Confluence, ServiceNow,
    Datadog, Grafana, Kibana, OpenTelemetry, Kubernetes, qTest, Figma, Documents, Web),
    pre-configured agile PM profiles (Azure DevOps, Asana, Linear, Trello, ClickUp,
    VersionOne, Monday, Shortcut), and arbitrary custom REST/webhook connectors.
    """

    _instance: ConnectionFactory | None = None

    def __init__(self) -> None:
        self._registry: dict[str, type[Any] | Callable[..., Any]] = {}
        self._specs: dict[str, ApplicationSpec] = {}
        self._aliases: dict[str, str] = {}
        self._bootstrap_defaults()

    @classmethod
    def get_instance(cls) -> ConnectionFactory:
        """Get or create singleton factory instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _bootstrap_defaults(self) -> None:
        """Bootstrap known application definitions and built-in connectors."""
        # 1. Agile Project Management
        self.register(
            "jira",
            spec=ApplicationSpec(
                app_id="jira",
                name="Jira Software & Service Management",
                category=ApplicationCategory.AGILE_PM,
                aliases=["atlassian_jira", "jira_cloud", "jira_server"],
                auth_methods=["token", "basic", "oauth2"],
                entity_mappings={"issue": "WorkItem", "sprint": "Sprint", "epic": "WorkItem"},
                description="Atlassian Jira issue tracking and agile boards",
            ),
        )

        self.register(
            "rally",
            spec=ApplicationSpec(
                app_id="rally",
                name="Rally (Broadcom Agile Central)",
                category=ApplicationCategory.AGILE_PM,
                aliases=["agile_central", "ca_rally"],
                auth_methods=["token", "basic"],
                entity_mappings={"user_story": "WorkItem", "defect": "WorkItem", "feature": "WorkItem"},
                description="Broadcom Rally enterprise agile planning",
            ),
        )

        # Pre-configured agile tools powered by GenericAgileConnector
        agile_apps = [
            ("azure_devops", "Azure DevOps Boards", ["ado", "azure_boards", "vsts"]),
            ("asana", "Asana", ["asana_tasks"]),
            ("linear", "Linear", ["linear_app"]),
            ("trello", "Trello", ["atlassian_trello"]),
            ("clickup", "ClickUp", ["clickup_tasks"]),
            ("versionone", "VersionOne / Digital.ai", ["digital_ai", "v1"]),
            ("monday", "Monday.com", ["monday_boards"]),
            ("shortcut", "Shortcut", ["clubhouse"]),
            ("pivotal_tracker", "Pivotal Tracker", ["pivotal"]),
        ]

        for app_id, name, aliases in agile_apps:
            self.register_agile_app(app_id, name=name, aliases=aliases)

        # 2. SCM & CI/CD
        self.register(
            "github",
            spec=ApplicationSpec(
                app_id="github",
                name="GitHub",
                category=ApplicationCategory.SCM_CICD,
                aliases=["gh", "github_enterprise"],
                auth_methods=["token", "oauth2"],
                entity_mappings={"pull_request": "MergeRequest", "repository": "Repository", "commit": "Commit"},
                description="GitHub repos, PRs, diffs, and actions",
            ),
        )

        self.register(
            "gitlab",
            spec=ApplicationSpec(
                app_id="gitlab",
                name="GitLab",
                category=ApplicationCategory.SCM_CICD,
                aliases=["gl", "gitlab_ee"],
                auth_methods=["token", "oauth2"],
                entity_mappings={"merge_request": "MergeRequest", "project": "Repository", "commit": "Commit"},
                description="GitLab projects, MRs, wikis, and pipelines",
            ),
        )

        # 3. Documentation & Knowledge
        self.register(
            "confluence",
            spec=ApplicationSpec(
                app_id="confluence",
                name="Confluence",
                category=ApplicationCategory.DOCS_KNOWLEDGE,
                aliases=["atlassian_confluence", "wiki"],
                auth_methods=["token", "basic"],
                entity_mappings={"page": "Document", "space": "KnowledgeSpace"},
                description="Atlassian Confluence documentation and wikis",
            ),
        )

        self.register(
            "documents",
            spec=ApplicationSpec(
                app_id="documents",
                name="Local Documents & Markdown",
                category=ApplicationCategory.DOCS_KNOWLEDGE,
                aliases=["files", "file_parsing"],
                auth_methods=[],
                description="Structured file parsers for documentation trees",
            ),
        )

        self.register(
            "web",
            spec=ApplicationSpec(
                app_id="web",
                name="Web Crawler",
                category=ApplicationCategory.DOCS_KNOWLEDGE,
                aliases=["web_crawler", "crawler"],
                description="Controlled intranet/extranet web crawling",
            ),
        )

        # 4. ITSM & Service Management
        self.register(
            "servicenow",
            spec=ApplicationSpec(
                app_id="servicenow",
                name="ServiceNow",
                category=ApplicationCategory.ITSM_OPERATIONS,
                aliases=["snow", "servicenow_itsm"],
                auth_methods=["token", "basic"],
                entity_mappings={"incident": "Incident", "change_request": "ChangeRequest"},
                description="ServiceNow ITSM incidents, changes, and CMDB items",
            ),
        )

        # 5. Observability & Telemetry
        self.register(
            "datadog",
            spec=ApplicationSpec(
                app_id="datadog",
                name="Datadog",
                category=ApplicationCategory.OBSERVABILITY,
                aliases=["dd"],
                auth_methods=["api_key"],
                description="Datadog metrics, APM services, and monitors",
            ),
        )

        self.register(
            "grafana",
            spec=ApplicationSpec(
                app_id="grafana",
                name="Grafana",
                category=ApplicationCategory.OBSERVABILITY,
                auth_methods=["token", "api_key"],
                description="Grafana dashboards and alerts",
            ),
        )

        self.register(
            "kibana",
            spec=ApplicationSpec(
                app_id="kibana",
                name="Kibana",
                category=ApplicationCategory.OBSERVABILITY,
                auth_methods=["token", "basic"],
                description="Elasticsearch/Kibana indices and saved searches",
            ),
        )

        self.register(
            "splunk",
            spec=ApplicationSpec(
                app_id="splunk",
                name="Splunk",
                category=ApplicationCategory.OBSERVABILITY,
                aliases=["splunk_enterprise", "splunk_cloud"],
                auth_methods=["token", "basic"],
                description="Splunk saved searches, alerts, and dashboards under strict query budgets",
            ),
        )

        self.register(
            "snowflake",
            spec=ApplicationSpec(
                app_id="snowflake",
                name="Snowflake",
                category=ApplicationCategory.CUSTOM_REST,
                aliases=["snowflake_dw", "snowflake_cloud"],
                auth_methods=["token", "basic", "keypair"],
                description="Snowflake Data Cloud warehouse and catalog integration",
            ),
        )

        self.register(
            "fortuna",
            spec=ApplicationSpec(
                app_id="fortuna",
                name="Fortuna",
                category=ApplicationCategory.CUSTOM_REST,
                description="Fortuna blocked product adapter pending Decision H-06",
            ),
        )

        self.register(
            "custom_system",
            spec=ApplicationSpec(
                app_id="custom_system",
                name="Custom Protocol System",
                category=ApplicationCategory.CUSTOM_REST,
                aliases=["generic_custom", "custom_protocol"],
                description="Generic multi-protocol adapter (REST, GraphQL, SOAP, JDBC, File, Kafka)",
            ),
        )

        # 6. Quality & Testing
        self.register(
            "qtest",
            spec=ApplicationSpec(
                app_id="qtest",
                name="qTest",
                category=ApplicationCategory.TEST_QUALITY,
                aliases=["tricentis_qtest"],
                auth_methods=["token"],
                entity_mappings={"test_case": "TestCase", "test_run": "TestRun"},
                description="Tricentis qTest test management",
            ),
        )

        # 7. Design & UX
        self.register(
            "figma",
            spec=ApplicationSpec(
                app_id="figma",
                name="Figma",
                category=ApplicationCategory.DESIGN_UX,
                auth_methods=["token"],
                description="Figma files, frames, components, and design systems",
            ),
        )

    def register(
        self,
        app_id: str,
        connector_cls: type[Any] | Callable[..., Any] | None = None,
        spec: ApplicationSpec | None = None,
        aliases: list[str] | None = None,
    ) -> None:
        """Register a connector class or specification."""
        norm_id = app_id.lower().strip()
        if spec is None:
            spec = ApplicationSpec(
                app_id=norm_id,
                name=norm_id.capitalize(),
                category=ApplicationCategory.CUSTOM_REST,
                aliases=aliases or [],
                connector_cls=connector_cls,
            )
        else:
            if connector_cls is not None:
                spec.connector_cls = connector_cls

        self._specs[norm_id] = spec
        if spec.connector_cls is not None:
            self._registry[norm_id] = spec.connector_cls

        all_aliases = set(spec.aliases).union(aliases or [])
        for alias in all_aliases:
            norm_alias = alias.lower().strip()
            self._aliases[norm_alias] = norm_id

    def register_agile_app(
        self,
        app_id: str,
        name: str,
        *,
        endpoint: str | None = None,
        field_mappings: dict[str, str] | None = None,
        aliases: list[str] | None = None,
    ) -> None:
        """Register any Agile Project Management tool with custom or default field mappings."""
        norm_id = app_id.lower().strip()
        spec = ApplicationSpec(
            app_id=norm_id,
            name=name,
            category=ApplicationCategory.AGILE_PM,
            aliases=aliases or [],
            auth_methods=["token", "basic", "api_key"],
            entity_mappings={"work_item": "WorkItem", "task": "WorkItem", "story": "WorkItem"},
            default_config={"endpoint": endpoint, "field_mappings": field_mappings or {}},
        )

        def _factory_fn(source_id: str, base_url: str, **kwargs) -> GenericAgileConnector:
            cfg = kwargs.pop("config", {}) or {}
            ep = endpoint or cfg.get("endpoint")
            fm = {**(field_mappings or {}), **(cfg.get("field_mappings", {}))}
            return GenericAgileConnector(
                source_id=source_id,
                base_url=base_url,
                app_name=norm_id,
                endpoint=ep,
                field_mappings=fm,
                **kwargs,
            )

        self.register(norm_id, connector_cls=_factory_fn, spec=spec, aliases=aliases)

    def register_generic_rest(
        self,
        app_id: str,
        name: str,
        *,
        entity_type: str = "Entity",
        endpoint: str = "api/data",
        aliases: list[str] | None = None,
    ) -> None:
        """Register an arbitrary REST application."""
        norm_id = app_id.lower().strip()
        spec = ApplicationSpec(
            app_id=norm_id,
            name=name,
            category=ApplicationCategory.CUSTOM_REST,
            aliases=aliases or [],
            default_config={"entity_type": entity_type, "endpoint": endpoint},
        )

        def _factory_fn(source_id: str, base_url: str, **kwargs) -> GenericRestApplicationConnector:
            return GenericRestApplicationConnector(
                source_id=source_id,
                base_url=base_url,
                app_name=norm_id,
                entity_type=entity_type,
                endpoint=endpoint,
                **kwargs,
            )

        self.register(norm_id, connector_cls=_factory_fn, spec=spec, aliases=aliases)

    def resolve_app_id(self, app_id_or_alias: str) -> str:
        """Resolve alias or name to canonical app_id."""
        norm = app_id_or_alias.lower().strip()
        return self._aliases.get(norm, norm)

    def get_spec(self, app_id_or_alias: str) -> ApplicationSpec | None:
        """Get application specification."""
        app_id = self.resolve_app_id(app_id_or_alias)
        return self._specs.get(app_id)

    def is_supported(self, app_id_or_alias: str) -> bool:
        """Check if application is recognized or supported."""
        app_id = self.resolve_app_id(app_id_or_alias)
        return app_id in self._specs or app_id in self._registry

    def list_applications(
        self, category: ApplicationCategory | str | None = None
    ) -> list[ApplicationSpec]:
        """List all supported applications, optionally filtered by category."""
        target_cat = category.value if isinstance(category, ApplicationCategory) else category
        specs = list(self._specs.values())
        if target_cat is not None:
            specs = [s for s in specs if s.category.value == target_cat]
        return sorted(specs, key=lambda s: (s.category.value, s.name))

    def detect_application(self, url_or_name: str) -> str:
        """Infer application type from URL, domain, or name."""
        lower = url_or_name.lower().strip()
        detection_rules = [
            ("jira", ["jira", "atlassian.net/jira"]),
            ("rally", ["rally", "rallydev.com"]),
            ("azure_devops", ["dev.azure.com", "visualstudio.com", "azure_boards", "ado"]),
            ("asana", ["asana.com", "app.asana.com"]),
            ("linear", ["linear.app"]),
            ("trello", ["trello.com"]),
            ("clickup", ["clickup.com", "app.clickup.com"]),
            ("versionone", ["versionone", "digital.ai"]),
            ("github", ["github.com", "github"]),
            ("gitlab", ["gitlab.com", "gitlab"]),
            ("confluence", ["confluence", "atlassian.net/wiki"]),
            ("servicenow", ["service-now.com", "servicenow"]),
            ("datadog", ["datadoghq.com", "datadog"]),
            ("grafana", ["grafana.net", "grafana"]),
            ("qtest", ["qtest", "qtestnet.com"]),
            ("figma", ["figma.com", "figma"]),
            ("slack", ["slack.com", "slack"]),
            ("documentum", ["documentum", "dctm"]),
            ("artifactory", ["artifactory", "jfrog"]),
            ("splunk", ["splunk", "splunkcloud.com"]),
            ("snowflake", ["snowflake", "snowflakecomputing.com"]),
            ("fortuna", ["fortuna"]),
            ("custom_system", ["custom_system", "custom_proto"]),
        ]
        for app_id, indicators in detection_rules:
            if any(ind in lower for ind in indicators):
                return app_id
        return "custom_rest"

    def create(
        self,
        app_id: str,
        base_url: str | None = None,
        *,
        source_id: str | None = None,
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        api_key: str | None = None,
        config: dict[str, Any] | None = None,
        client: httpx.Client | None = None,
        correlation_id: str | None = None,
        **kwargs,
    ) -> SourceConnector:
        """Create a connector instance for ANY application.

        If a specialized connector class exists (e.g. Jira, GitHub, ServiceNow), it is used.
        If it's an agile tool (e.g. Azure DevOps, Asana, Linear, Trello), it automatically instantiates
        a GenericAgileConnector. If unknown, it dynamically creates a GenericAgileConnector or
        GenericRestApplicationConnector so no application is blocked.
        """
        canonical_id = self.resolve_app_id(app_id)
        spec = self._specs.get(canonical_id)
        effective_source_id = source_id or f"{canonical_id}-{uuid4().hex[:8]}"
        effective_base_url = base_url or (spec.default_base_url if spec else None) or "https://localhost"
        cfg = config or (spec.default_config if spec else {}) or {}

        # 1. Check if registered class or factory exists
        factory_or_cls = self._registry.get(canonical_id)

        # Lazy load built-in specialized classes if not yet initialized
        if factory_or_cls is None and canonical_id in self._specs:
            factory_or_cls = self._load_builtin_connector(canonical_id)

        if factory_or_cls is not None:
            try:
                # Built-in classes have distinct parameter conventions
                return self._instantiate_connector(
                    factory_or_cls,
                    canonical_id=canonical_id,
                    source_id=effective_source_id,
                    base_url=effective_base_url,
                    token=token,
                    username=username,
                    password=password,
                    api_key=api_key,
                    config=cfg,
                    client=client,
                    correlation_id=correlation_id,
                    **kwargs,
                )
            except Exception as exc:
                if type(exc).__name__ == "FortunaConnectorBlockedError":
                    raise
                if cfg.get("fallback_policy") != "explicit":
                    logger.error(
                        "Specialization failed for %s without explicit fallback policy: %s (G07 closure)",
                        canonical_id,
                        exc,
                    )
                    raise ConnectorSpecializationFailedError(
                        source_system=canonical_id,
                        reason=str(exc),
                        correlation_id=correlation_id or "default-corr-id",
                    ) from exc
                logger.warning(
                    "Explicit fallback policy active. Specialization failed for %s: %s; downgrading to generic",
                    canonical_id,
                    exc,
                )

        # 2. If categorized as Agile PM or name suggests it, use GenericAgileConnector
        is_agile = (spec and spec.category == ApplicationCategory.AGILE_PM) or any(
            x in canonical_id for x in ["board", "agile", "task", "issue", "pm", "project", "story"]
        )
        if is_agile:
            return GenericAgileConnector(
                source_id=effective_source_id,
                base_url=effective_base_url,
                app_name=canonical_id,
                token=token,
                username=username,
                password=password,
                api_key=api_key,
                config=cfg,
                client=client,
                **kwargs,
            )

        # 3. Universal Fallback: Generic REST Connector connects ANY application!
        entity_type = kwargs.pop("entity_type", None) or cfg.get("entity_type", "Entity")
        endpoint = kwargs.pop("endpoint", None) or cfg.get("endpoint", "api/entities")
        return GenericRestApplicationConnector(
            source_id=effective_source_id,
            base_url=effective_base_url,
            app_name=canonical_id,
            entity_type=entity_type,
            endpoint=endpoint,
            token=token,
            username=username,
            password=password,
            api_key=api_key,
            config=cfg,
            client=client,
            **kwargs,
        )

    def _load_builtin_connector(self, canonical_id: str) -> type[Any] | None:
        """Dynamically load built-in connectors on demand."""
        try:
            if canonical_id == "jira":
                from eoip.connectors.jira import JiraConnector
                return JiraConnector
            if canonical_id == "rally":
                from eoip.connectors.rally import RallyConnector
                return RallyConnector
            if canonical_id == "github":
                from eoip.connectors.github import GitHubConnector
                return GitHubConnector
            if canonical_id == "gitlab":
                from eoip.connectors.gitlab import GitLabConnector
                return GitLabConnector
            if canonical_id == "confluence":
                from eoip.connectors.confluence import ConfluenceConnector
                return ConfluenceConnector
            if canonical_id == "servicenow":
                from eoip.connectors.servicenow import ServiceNowConnector
                return ServiceNowConnector
            if canonical_id in ("documents", "files"):
                from eoip.connectors.files import FileParsingConnector
                return FileParsingConnector
            if canonical_id in ("web", "crawler"):
                from eoip.connectors.generic import WebSourceConnector
                return WebSourceConnector
            if canonical_id == "slack":
                from eoip.connectors.slack import SlackConnector
                return SlackConnector
            if canonical_id in ("documentum", "dctm"):
                from eoip.connectors.documentum import DocumentumConnector
                return DocumentumConnector
            if canonical_id in ("artifactory", "jfrog"):
                from eoip.connectors.artifactory import ArtifactoryConnector
                return ArtifactoryConnector
            if canonical_id in ("splunk", "splunk_enterprise", "splunk_cloud"):
                from eoip.connectors.splunk import SplunkConnector
                return SplunkConnector
            if canonical_id == "grafana":
                from eoip.connectors.grafana import GrafanaConnector
                return GrafanaConnector
            if canonical_id == "kibana":
                from eoip.connectors.kibana import KibanaConnector
                return KibanaConnector
            if canonical_id in ("snowflake", "snowflake_dw", "snowflake_cloud"):
                from eoip.connectors.snowflake import SnowflakeConnector
                return SnowflakeConnector
            if canonical_id == "fortuna":
                from eoip.connectors.fortuna import FortunaConnector
                return FortunaConnector
            if canonical_id in ("custom_system", "generic_custom", "custom_protocol"):
                from eoip.connectors.custom_system import GenericCustomSystemConnector
                return GenericCustomSystemConnector
        except ImportError as exc:
            logger.debug("Optional connector %s not importable: %s", canonical_id, exc)
        return None

    def _instantiate_connector(
        self,
        cls_or_fn: Any,
        *,
        canonical_id: str,
        source_id: str,
        base_url: str,
        token: str | None,
        username: str | None,
        password: str | None,
        api_key: str | None,
        config: dict[str, Any],
        client: httpx.Client | None,
        correlation_id: str | None,
        **kwargs,
    ) -> Any:
        """Call the appropriate constructor with parameters expected by each adapter."""
        # Check if it's our own factory function
        if callable(cls_or_fn) and not isinstance(cls_or_fn, type):
            return cls_or_fn(
                source_id=source_id,
                base_url=base_url,
                token=token,
                username=username,
                password=password,
                api_key=api_key,
                config=config,
                client=client,
                **kwargs,
            )

        # Jira
        if canonical_id == "jira":
            return cls_or_fn(
                source_id,
                base_url,
                projects=list(config.get("projects", [])),
                token=token,
                username=username,
                password=password,
                api_version=str(config.get("api_version", "3")),
                search_mode=str(config.get("search_mode", "enhanced")),
                fields=list(config.get("fields", [])) or None,
                page_size=int(config.get("page_size", 100)),
            )

        # Rally
        if canonical_id == "rally":
            return cls_or_fn(
                base_url,
                token=token,
                username=username,
                password=password,
                workspace=config.get("workspace"),
                project=config.get("project"),
                page_size=int(config.get("page_size", 200)),
            )

        # GitHub
        if canonical_id == "github":
            return cls_or_fn(
                source_id,
                base_url,
                token or "",
                repositories=list(config.get("repositories", [])),
                organizations=list(config.get("organizations", [])),
                page_size=int(config.get("page_size", 100)),
            )

        # GitLab
        if canonical_id == "gitlab":
            return cls_or_fn(
                source_id,
                base_url,
                token or "",
                projects=list(config.get("projects", [])),
                groups=list(config.get("groups", [])),
                page_size=int(config.get("page_size", 100)),
            )

        # Confluence / ServiceNow
        if canonical_id in ("confluence", "servicenow"):
            return cls_or_fn(
                base_url,
                token=token,
                username=username,
                password=password,
                page_size=int(config.get("page_size", 100)),
            )

        # Slack
        if canonical_id == "slack":
            return cls_or_fn(
                source_id,
                token or "",
                base_url=base_url or "https://slack.com/api",
                enable_private_channels=bool(config.get("enable_private_channels", False)),
                enable_direct_messages=bool(config.get("enable_direct_messages", False)),
                compliance_approval_ref=config.get("compliance_approval_ref"),
                channels=list(config.get("channels", [])) or None,
                client=client,
            )

        # Documentum
        if canonical_id in ("documentum", "dctm"):
            return cls_or_fn(
                source_id,
                base_url,
                repository=str(config.get("repository", "repo")),
                username=username,
                password=password,
                token=token,
                cabinets=list(config.get("cabinets", [])) or None,
                client=client,
            )

        # Artifactory
        if canonical_id in ("artifactory", "jfrog"):
            return cls_or_fn(
                source_id,
                base_url,
                token=token,
                username=username,
                password=password,
                repositories=list(config.get("repositories", [])) or None,
                client=client,
            )

        # Splunk
        if canonical_id in ("splunk", "splunk_enterprise", "splunk_cloud"):
            from eoip.connectors.splunk import SearchBudget
            budget = None
            if "budget" in config:
                b_cfg = config["budget"]
                budget = SearchBudget(
                    max_results=int(b_cfg.get("max_results", 1000)),
                    timeout_seconds=float(b_cfg.get("timeout_seconds", 30.0)),
                    max_search_span_hours=int(b_cfg.get("max_search_span_hours", 72)),
                )
            return cls_or_fn(
                source_id,
                base_url,
                token=token,
                username=username,
                password=password,
                app=str(config.get("app", "search")),
                budget=budget,
                client=client,
            )

        # Grafana
        if canonical_id == "grafana":
            return cls_or_fn(
                base_url,
                token=token,
                page_size=int(config.get("page_size", 1000)),
                fetch_alerts=bool(config.get("fetch_alerts", True)),
                fetch_datasources=bool(config.get("fetch_datasources", True)),
                client=client,
            )

        # Kibana
        if canonical_id == "kibana":
            return cls_or_fn(
                base_url,
                token=token,
                space_id=config.get("space_id"),
                page_size=int(config.get("page_size", 100)),
                client=client,
            )

        # Snowflake
        if canonical_id in ("snowflake", "snowflake_dw", "snowflake_cloud"):
            from eoip.connectors.snowflake import SnowflakeCostGuard, SnowflakeMode
            mode_str = str(config.get("mode", "metadata_only"))
            mode = SnowflakeMode(mode_str) if mode_str in [m.value for m in SnowflakeMode] else SnowflakeMode.METADATA_ONLY
            cost_guard = None
            if "cost_guard" in config:
                cg = config["cost_guard"]
                cost_guard = SnowflakeCostGuard(
                    max_credits=float(cg.get("max_credits", 5.0)),
                    statement_timeout_seconds=float(cg.get("statement_timeout_seconds", 30.0)),
                    max_result_rows=int(cg.get("max_result_rows", 5000)),
                )
            return cls_or_fn(
                source_id,
                account=str(config.get("account", base_url)),
                warehouse=str(config.get("warehouse", "COMPUTE_WH")),
                database=str(config.get("database", "PROD_DB")),
                schema=str(config.get("schema", "PUBLIC")),
                role=str(config.get("role", "PUBLIC")),
                mode=mode,
                cost_guard=cost_guard,
                opt_in_sampling=bool(config.get("opt_in_sampling", False)),
                opt_in_query_history=bool(config.get("opt_in_query_history", False)),
                sql_version=str(config.get("sql_version", "snowflake-sql/2024.1")),
                token=token,
                username=username,
                password=password,
                client=client,
            )

        # Fortuna
        if canonical_id == "fortuna":
            return cls_or_fn(**kwargs)

        # Custom System
        if canonical_id in ("custom_system", "generic_custom", "custom_protocol"):
            from eoip.connectors.custom_system import CustomProtocol, ProtocolEndpointConfig
            proto_str = str(config.get("protocol", "rest_openapi"))
            proto = CustomProtocol(proto_str) if proto_str in [p.value for p in CustomProtocol] else CustomProtocol.REST
            endpoint_cfg = ProtocolEndpointConfig(
                protocol=proto,
                endpoint_url=base_url,
                auth_type=str(config.get("auth_type", "bearer")),
                credentials=dict(config.get("credentials", {})),
                options=dict(config.get("options", {})),
            )
            return cls_or_fn(
                source_id=source_id,
                config=endpoint_cfg,
                mapping=config.get("mapping"),
                client=client,
            )

        # Default direct instantiation
        return cls_or_fn(
            source_id=source_id,
            base_url=base_url,
            token=token,
            username=username,
            password=password,
            config=config,
            **kwargs,
        )

    def create_from_registry(
        self,
        entry: SourceRegistryEntry,
        *,
        environ: Mapping[str, str] | None = None,
        correlation_id: str | None = None,
    ) -> SourceConnector:
        """Create a connector from a SourceRegistryEntry and referenced environment secrets."""
        variables = os.environ if environ is None else environ
        cid = correlation_id or str(uuid4())

        token = self._resolve_secret(entry, "token", variables)
        username = self._resolve_secret(entry, "username", variables)
        password = self._resolve_secret(entry, "password", variables)
        api_key = self._resolve_secret(entry, "api_key", variables)

        return self.create(
            entry.source_type,
            base_url=entry.base_url,
            source_id=entry.source_id,
            token=token,
            username=username,
            password=password,
            api_key=api_key,
            config=entry.config,
            correlation_id=cid,
        )

    def create_from_environment(
        self,
        app_id: str,
        *,
        environ: Mapping[str, str] | None = None,
        correlation_id: str | None = None,
    ) -> SourceConnector:
        """Create a connector using standard EOIP_<APP> environment variables."""
        variables = os.environ if environ is None else environ
        canonical_id = self.resolve_app_id(app_id)
        prefix = f"EOIP_{canonical_id.upper()}"

        base_url = variables.get(f"{prefix}_URL", "https://localhost").strip()
        token = variables.get(f"{prefix}_TOKEN", "").strip() or None
        username = variables.get(f"{prefix}_USERNAME", "").strip() or None
        password = variables.get(f"{prefix}_PASSWORD", "") or None
        api_key = variables.get(f"{prefix}_API_KEY", "").strip() or None

        return self.create(
            canonical_id,
            base_url=base_url,
            token=token,
            username=username,
            password=password,
            api_key=api_key,
            correlation_id=correlation_id,
        )

    def _resolve_secret(
        self,
        entry: SourceRegistryEntry,
        secret_name: str,
        variables: Mapping[str, str],
    ) -> str | None:
        ref = entry.secret_refs.get(secret_name)
        if not ref:
            return None
        if ref.startswith("env://"):
            var_name = ref.removeprefix("env://")
            return variables.get(var_name) or None
        return None


# Module-level convenience singleton access
connection_factory = ConnectionFactory.get_instance()
ConnectorFactory = ConnectionFactory


def get_connection_factory() -> ConnectionFactory:
    """Return the global ConnectionFactory instance."""
    return ConnectionFactory.get_instance()
