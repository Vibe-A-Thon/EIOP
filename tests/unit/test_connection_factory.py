"""Unit tests for the Universal Connection Factory and extensible source connectors.

Validates:
- Universal ConnectionFactory / ConnectorFactory registry & discovery
- Pre-configured Agile Project Management tools (Jira, Rally, Azure DevOps, Asana, Linear, Trello, ClickUp, VersionOne)
- Universal GenericAgileConnector transforming any agile tool into canonical WorkItem SourceEventV2 envelopes
- Universal GenericRestApplicationConnector connecting arbitrary enterprise REST services
- Dynamic registration of third-party / custom applications
- Integration with SourceRegistryEntry and connector_from_registry
- Categorized application listing, metadata queries, and URL-based application detection
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from eoip.connectors.base import DiscoveryScope, SourceConnector
from eoip.connectors.config import connector_from_registry
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
from eoip.contracts.source_event import SourceEventV2
from eoip.contracts.source_registry import SourceRegistryEntry


def test_factory_singleton_and_aliases():
    """Verify singleton access and alias parity."""
    f1 = ConnectionFactory.get_instance()
    f2 = get_connection_factory()
    assert f1 is f2
    assert connection_factory is f1
    assert ConnectorFactory is ConnectionFactory


def test_list_applications_by_category():
    """Verify application discovery and filtering by category."""
    factory = ConnectionFactory.get_instance()
    all_apps = factory.list_applications()
    assert len(all_apps) >= 15

    agile_apps = factory.list_applications(ApplicationCategory.AGILE_PM)
    agile_ids = {a.app_id for a in agile_apps}

    expected_agile = {"jira", "rally", "azure_devops", "asana", "linear", "trello", "clickup", "versionone"}
    assert expected_agile.issubset(agile_ids), f"Missing agile applications: {expected_agile - agile_ids}"

    scm_apps = factory.list_applications(ApplicationCategory.SCM_CICD)
    scm_ids = {a.app_id for a in scm_apps}
    assert {"github", "gitlab"}.issubset(scm_ids)

    doc_apps = factory.list_applications(ApplicationCategory.DOCS_KNOWLEDGE)
    doc_ids = {a.app_id for a in doc_apps}
    assert {"confluence", "documents", "web"}.issubset(doc_ids)


def test_create_agile_connector_azure_devops():
    """Verify creating Azure DevOps agile connector via factory with alias."""
    factory = ConnectionFactory.get_instance()

    # Create via alias 'ado'
    connector = factory.create(
        "ado",
        base_url="https://dev.azure.com/my-org/my-project",
        token="pat-token-xyz",
    )
    assert isinstance(connector, GenericAgileConnector)
    assert connector.app_name == "azure_devops"
    assert connector.capabilities().baseline is True

    # Transform Azure DevOps item JSON
    ado_raw_item = {
        "id": 4201,
        "fields": {
            "System.Id": "4201",
            "System.Title": "Add user authentication flow",
            "System.State": "Active",
            "System.WorkItemType": "User Story",
            "System.ChangedDate": "2026-10-12T10:00:00Z",
        },
    }
    event = connector.transform_item(ado_raw_item)
    assert isinstance(event, SourceEventV2)
    assert event.source_record_type == "WorkItem"
    assert event.payload["canonical_id"] == "urn:eoip:work:item:azure_devops:4201"
    assert event.payload["summary"] == "Add user authentication flow"
    assert event.payload["status"] == "Active"
    assert event.payload["issue_type"] == "User Story"


def test_create_agile_connector_linear():
    """Verify creating Linear agile connector via factory."""
    factory = ConnectionFactory.get_instance()
    connector = factory.create(
        "linear",
        base_url="https://api.linear.app",
        token="lin_api_key_123",
    )
    assert isinstance(connector, GenericAgileConnector)
    assert connector.app_name == "linear"

    linear_raw = {
        "id": "lin-789",
        "identifier": "ENG-104",
        "title": "Fix memory leak in query executor",
        "state": {"name": "In Progress"},
    }
    event = connector.transform_item(linear_raw)
    assert event.source_record_type == "WorkItem"
    assert event.payload["canonical_id"] == "urn:eoip:work:item:linear:ENG-104"
    assert event.payload["issue_key"] == "ENG-104"
    assert event.payload["summary"] == "Fix memory leak in query executor"
    assert event.payload["status"] == "In Progress"


def test_create_agile_connector_asana():
    """Verify creating Asana agile connector via factory."""
    factory = ConnectionFactory.get_instance()
    connector = factory.create(
        "asana",
        base_url="https://app.asana.com",
        token="asana-token-xyz",
    )
    assert isinstance(connector, GenericAgileConnector)

    asana_raw = {
        "gid": "1200345",
        "name": "Design notification architecture",
        "completed": False,
        "resource_type": "task",
    }
    event = connector.transform_item(asana_raw)
    assert event.payload["canonical_id"] == "urn:eoip:work:item:asana:1200345"
    assert event.payload["summary"] == "Design notification architecture"
    assert event.payload["issue_type"] == "task"


def test_create_agile_connector_trello_and_clickup():
    """Verify creating Trello and ClickUp agile connectors."""
    factory = ConnectionFactory.get_instance()

    # Trello
    trello = factory.create("trello", base_url="https://api.trello.com", api_key="trellokey")
    assert isinstance(trello, GenericAgileConnector)
    trello_event = trello.transform_item({"id": "tr-1", "idShort": "CARD-42", "name": "Refactor router"})
    assert trello_event.payload["canonical_id"] == "urn:eoip:work:item:trello:CARD-42"
    assert trello_event.payload["summary"] == "Refactor router"

    # ClickUp
    clickup = factory.create("clickup", base_url="https://api.clickup.com", token="pk_clickup")
    assert isinstance(clickup, GenericAgileConnector)
    clickup_event = clickup.transform_item({
        "id": "cu-99",
        "custom_id": "TASK-99",
        "name": "Upgrade Cytoscape canvas",
        "status": {"status": "in review"},
    })
    assert clickup_event.payload["canonical_id"] == "urn:eoip:work:item:clickup:TASK-99"
    assert clickup_event.payload["summary"] == "Upgrade Cytoscape canvas"
    assert clickup_event.payload["status"] == "in review"


def test_generic_agile_connector_protocol():
    """Verify GenericAgileConnector implements complete SourceConnector protocol."""
    connector = GenericAgileConnector(
        source_id="agile-custom-1",
        base_url="https://agile.example.corp",
        app_name="custom_pm",
    )
    assert isinstance(connector, SourceConnector)

    # Capabilities
    caps = connector.capabilities()
    assert caps.baseline is True
    assert caps.polling is True

    # Discovery
    disc = connector.discover(DiscoveryScope())
    assert len(disc.resources) >= 1

    # Health
    health = connector.health()
    assert health.status == "HEALTHY"

    # Handle incoming webhook event
    events = list(connector.handle_event({
        "item": {"id": "1001", "key": "CP-1001", "summary": "Webhook created issue"}
    }))
    assert len(events) == 1
    assert events[0].payload["canonical_id"] == "urn:eoip:work:item:custom_pm:CP-1001"

    # Fetch record
    single = connector.fetch_record("1001")
    assert single.source_record_id == "1001"

    # Replay
    replayed = list(connector.replay(events))
    assert len(replayed) == 1


def test_generic_rest_application_connector():
    """Verify GenericRestApplicationConnector for arbitrary non-agile enterprise APIs."""
    factory = ConnectionFactory.get_instance()
    connector = factory.create(
        "custom_billing_system",
        base_url="https://billing.internal.corp",
        token="secret-token",
        config={"entity_type": "Invoice", "endpoint": "api/invoices"},
    )
    assert isinstance(connector, GenericRestApplicationConnector)
    assert isinstance(connector, SourceConnector)

    raw_item = {
        "id": "INV-2026-001",
        "amount": 45000.00,
        "currency": "USD",
        "customer": "Acme Corp",
    }
    event = connector.transform_item(raw_item)
    assert event.source_record_type == "Invoice"
    assert "INV-2026-001" in event.payload["canonical_id"]
    assert event.payload["amount"] == 45000.00


def test_dynamic_custom_application_registration():
    """Verify registering a brand new application dynamically at runtime."""
    factory = ConnectionFactory.get_instance()

    # Register custom agile tool
    factory.register_agile_app(
        app_id="acme_tracker",
        name="Acme In-House Tracker",
        endpoint="api/v1/tickets",
        field_mappings={"id": "ticket_id", "summary": "headline", "status": "lifecycle_state"},
        aliases=["acme_pm", "inhouse_tickets"],
    )

    spec = factory.get_spec("acme_pm")
    assert spec is not None
    assert spec.name == "Acme In-House Tracker"

    # Instantiate via factory
    conn = factory.create("acme_pm", base_url="https://acme.internal.corp")
    assert isinstance(conn, GenericAgileConnector)

    evt = conn.transform_item({
        "ticket_id": "TICK-77",
        "headline": "Deploy Kubernetes worker pool",
        "lifecycle_state": "RESOLVED",
    })
    assert evt.payload["canonical_id"] == "urn:eoip:work:item:acme_tracker:TICK-77"
    assert evt.payload["summary"] == "Deploy Kubernetes worker pool"
    assert evt.payload["status"] == "RESOLVED"


def test_detect_application_heuristics():
    """Verify application detection heuristics from URL or host string."""
    factory = ConnectionFactory.get_instance()
    assert factory.detect_application("https://acme.atlassian.net/jira") == "jira"
    assert factory.detect_application("https://dev.azure.com/acme-corp") == "azure_devops"
    assert factory.detect_application("https://rally1.rallydev.com/#/dashboard") == "rally"
    assert factory.detect_application("https://app.asana.com/0/projects") == "asana"
    assert factory.detect_application("https://linear.app/acme/team") == "linear"
    assert factory.detect_application("https://trello.com/b/xyz") == "trello"
    assert factory.detect_application("https://github.com/my-org/repo") == "github"
    assert factory.detect_application("https://gitlab.com/group/project") == "gitlab"
    assert factory.detect_application("https://custom-service.internal.corp") == "custom_rest"


def test_connector_from_registry_with_azure_devops():
    """Verify connector_from_registry dynamically instantiates extended agile apps."""
    entry = SourceRegistryEntry(
        source_id="ado-prod",
        source_type="azure_devops",
        name="Production Azure DevOps",
        base_url="https://dev.azure.com/my-enterprise",
        secret_refs={"token": "env://TEST_ADO_PAT"},
    )
    environ = {"TEST_ADO_PAT": "secure-ado-pat-12345"}
    connector = connector_from_registry(entry, environ=environ)
    assert isinstance(connector, GenericAgileConnector)
    assert connector.token == "secure-ado-pat-12345"
    assert connector.base_url == "https://dev.azure.com/my-enterprise"


def test_connector_from_registry_with_arbitrary_custom_app():
    """Verify connector_from_registry connects any arbitrary custom application without failure."""
    entry = SourceRegistryEntry(
        source_id="custom-erp-1",
        source_type="sap_inventory_service",
        name="SAP Inventory REST API",
        base_url="https://sap.internal.corp",
        secret_refs={"api_key": "env://SAP_API_KEY"},
        config={"entity_type": "InventoryItem", "endpoint": "api/v2/items"},
    )
    environ = {"SAP_API_KEY": "sap-key-abcdef"}
    connector = connector_from_registry(entry, environ=environ)
    assert isinstance(connector, GenericRestApplicationConnector)
    assert connector.api_key == "sap-key-abcdef"
    assert connector.entity_type == "InventoryItem"
