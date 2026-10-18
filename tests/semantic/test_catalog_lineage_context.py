"""Comprehensive test suite for Catalog, Lineage and Enterprise Context (CRA-029.1-029.8, CRA-029.A).

Covers:
- CRA-029.1: Technical assets, business terms, owners, classifications, lineage as typed linked entities.
- CRA-029.2, CRA-029.6: Three metadata layers (Base, Edit, Merged), field-level precedence, reset-to-source,
  and human override survival with conflict indicator upon source drift.
- CRA-029.3: Lineage parser: deterministic static SQL parsing vs diagnostic uncertainty on dynamic statements.
- CRA-029.4: Distinct Data Graph, Schema/Meta Graph, and Provenance/Security Graph projections with stable links.
- CRA-029.5: Federated catalog integration with authoritative domain ownership and deduplication.
- CRA-029.7: Atlas-pattern classification propagation along lineage with atomic reversible removal.
- CRA-029.8: Projections compatible with OpenMetadata, LinkedIn DataHub, and Apache Atlas schemas.
- CRA-029.A:
  * Human description in edit layer survives subsequent crawler run while conflict indicator shows changed source truth.
  * Lineage parser emits uncertainty diagnostics on dynamic SQL rather than guessed edges.
"""

from __future__ import annotations

import json
import pytest

from eoip.catalog import (
    CatalogProjectionEngine,
    ClassificationPropagationEngine,
    FederatedCatalogSource,
    LayeredAssetMetadata,
    LineageParser,
    MultiGraphViewEngine,
)
from eoip.graph.memory import MemoryGraphStore


def test_layered_metadata_human_override_and_conflict_indicator():
    """CRA-029.2, CRA-029.6, CRA-029.A: 3 metadata layers, human override survival, drift detection, and reset-to-source."""
    meta = LayeredAssetMetadata(asset_id="urn:eoip:service:orders", entity_type="Service")

    # 1. Initial crawl: Base layer observed from Git/ServiceNow
    v1 = meta.record_crawl(
        properties={"description": "Orders processing backend microservice", "tier": "Tier-2", "owner": "Team Alpha"},
        source_system="gitlab-repo",
        source_revision="sha-001",
        observed_at="2026-01-01T10:00:00Z",
    )
    assert v1["effective_properties"]["description"] == "Orders processing backend microservice"
    assert v1["has_conflicts"] is False
    assert "base:gitlab-repo:sha-001" in v1["field_provenance"]["description"]

    # 2. Human Curation: Data steward overrides description in EditLayer
    v2 = meta.apply_human_edit(
        field_name="description",
        curated_value="Core Tier-1 revenue generation order checkout pipeline (PCI/SOX scope)",
        author="steward-alice",
        reason="Business glossary alignment and compliance qualification",
        edited_at="2026-01-15T12:00:00Z",
    )
    # Effective merged view reflects human edit (CRA-029.2)
    assert v2["effective_properties"]["description"] == "Core Tier-1 revenue generation order checkout pipeline (PCI/SOX scope)"
    assert "edit:steward-alice" in v2["field_provenance"]["description"]
    assert v2["has_conflicts"] is False

    # 3. Next Crawler Run (CRA-029.6, CRA-029.A): Source Git repo changed the description to something else
    v3 = meta.record_crawl(
        properties={"description": "Order processing system rewritten in Go v2", "tier": "Tier-1", "owner": "Team Alpha"},
        source_system="gitlab-repo",
        source_revision="sha-002",
        observed_at="2026-02-01T10:00:00Z",
    )
    # INVARIANT (CRA-029.A): Human description in EditLayer SURVIVES the next crawler run!
    assert v3["effective_properties"]["description"] == "Core Tier-1 revenue generation order checkout pipeline (PCI/SOX scope)"
    # BUT conflict indicator is raised so changed source truth is not silently hidden!
    assert v3["has_conflicts"] is True
    assert "description" in v3["conflicts"]
    assert v3["conflicts"]["description"]["observed_base_value"] == "Order processing system rewritten in Go v2"
    assert v3["conflicts"]["description"]["human_author"] == "steward-alice"

    # Non-overridden fields update cleanly from base crawl
    assert v3["effective_properties"]["tier"] == "Tier-1"

    # 4. Reset to Source (CRA-029.2): Steward removes human override
    v4 = meta.reset_to_source("description")
    assert v4["effective_properties"]["description"] == "Order processing system rewritten in Go v2"
    assert v4["has_conflicts"] is False


def test_lineage_parser_deterministic_and_dynamic_uncertainty():
    """CRA-029.3, CRA-029.A: Lineage parser emits deterministic edges for static SQL and diagnostics on dynamic SQL."""
    parser = LineageParser()

    # 1. Deterministic CREATE VIEW lineage
    sql_view = "CREATE VIEW analytics.daily_orders AS SELECT order_id, customer_id, total_amount FROM raw.orders"
    res_view = parser.parse_query_lineage(sql_view, query_id="q-view")
    assert res_view.status == "DETERMINISTIC"
    assert res_view.confidence == 1.0
    assert len(res_view.edges) == 1
    assert res_view.edges[0].source_table == "raw.orders"
    assert res_view.edges[0].target_table == "analytics.daily_orders"
    assert "total_amount" in res_view.edges[0].source_columns
    assert len(res_view.diagnostics) == 0

    # 2. Deterministic INSERT INTO ... SELECT
    sql_etl = "INSERT INTO dw.dim_customer (cust_id, email) SELECT id, email_address FROM crm.users"
    res_etl = parser.parse_query_lineage(sql_etl, query_id="q-etl")
    assert res_etl.status == "DETERMINISTIC"
    assert res_etl.edges[0].source_table == "crm.users"
    assert res_etl.edges[0].target_table == "dw.dim_customer"

    # 3. Dynamic SQL: EXEC statement (CRA-029.3, CRA-029.A)
    # INVARIANT: Must emit UNCERTAIN status and diagnostic, NEVER guessing edges!
    sql_dynamic = "EXEC (@sql_statement)"
    res_dyn = parser.parse_query_lineage(sql_dynamic, query_id="q-dyn")
    assert res_dyn.status == "UNCERTAIN"
    assert res_dyn.confidence == 0.0
    assert len(res_dyn.edges) == 0
    assert len(res_dyn.diagnostics) >= 1
    assert "Dynamic SQL statement detected" in res_dyn.diagnostics[0]

    # 4. Unsupported unparseable dialect syntax
    sql_complex = "ALTER TABLE foo COMPACT PARTITION ALL WITH NOOP OPTION"
    res_comp = parser.parse_query_lineage(sql_complex, query_id="q-comp")
    assert res_comp.status == "UNCERTAIN"
    assert len(res_comp.edges) == 0
    assert "refuses to guess edges" in res_comp.diagnostics[0]


def test_atlas_classification_propagation_and_reversal():
    """CRA-029.7: Atlas-pattern classification propagation along lineage and reversible retraction."""
    store = MemoryGraphStore()

    # Upstream -> Midstream -> Downstream services
    store.upsert_vertex("Service", {"canonical_id": "urn:eoip:service:customer-db", "service_id": "cust-db", "name": "Customer DB"})
    store.upsert_vertex("Service", {"canonical_id": "urn:eoip:service:auth-api", "service_id": "auth-api", "name": "Auth API"})
    store.upsert_vertex("Service", {"canonical_id": "urn:eoip:service:reporting-svc", "service_id": "rep-svc", "name": "Reporting Service"})

    store.upsert_edge("CALLS", "urn:eoip:service:customer-db", "urn:eoip:service:auth-api", {})
    store.upsert_edge("CALLS", "urn:eoip:service:auth-api", "urn:eoip:service:reporting-svc", {})

    engine = ClassificationPropagationEngine(store)

    # 1. Apply PII classification at upstream root Customer DB
    res_add = engine.add_classification("urn:eoip:service:customer-db", "PII")
    assert res_add["cascaded_count"] == 2
    assert "urn:eoip:service:auth-api" in res_add["cascaded_to"]
    assert "urn:eoip:service:reporting-svc" in res_add["cascaded_to"]

    # Verify downstream tags retain full provenance
    tags_rep = engine.get_classifications("urn:eoip:service:reporting-svc")
    assert len(tags_rep) == 1
    assert tags_rep[0]["tag_name"] == "PII"
    assert tags_rep[0]["is_direct"] is False
    assert tags_rep[0]["root_asset_id"] == "urn:eoip:service:customer-db"
    assert tags_rep[0]["hop_distance"] == 2

    # 2. Reversible removal at root (CRA-029.7)
    res_remove = engine.remove_classification("urn:eoip:service:customer-db", "PII")
    assert res_remove["removed"] is True
    assert res_remove["retracted_count"] == 2

    # Verify cascade is completely cleaned up
    assert len(engine.get_classifications("urn:eoip:service:reporting-svc")) == 0
    assert len(engine.get_classifications("urn:eoip:service:auth-api")) == 0
    assert len(engine.get_classifications("urn:eoip:service:customer-db")) == 0


def test_multi_graph_views_data_schema_provenance():
    """CRA-029.4: Distinct projections: Data Graph vs Schema/Meta Graph vs Provenance/Security Graph."""
    store = MemoryGraphStore()

    # 1. Data plane entity
    store.upsert_vertex("Service", {"canonical_id": "urn:eoip:service:billing", "service_id": "billing", "name": "Billing Service"})

    # 2. Schema plane entity
    store.upsert_vertex("GraphDomain", {"canonical_id": "urn:eoip:domain:finance", "name": "FINANCE"})

    # 3. Provenance/Security plane entity
    store.upsert_vertex("IngestionRun", {
        "canonical_id": "urn:eoip:run:run-100",
        "run_status": "COMPLETED",
        "run_kind": "BATCH",
    })

    view_engine = MultiGraphViewEngine(store)

    # Project 3 distinct graph planes (CRA-029.4)
    data_view = view_engine.get_data_graph_view()
    schema_view = view_engine.get_schema_meta_graph_view()
    prov_view = view_engine.get_provenance_security_graph_view()

    # Verify strict plane separation
    data_cids = [v["canonical_id"] for v in data_view.vertices]
    schema_cids = [v["canonical_id"] for v in schema_view.vertices]
    prov_cids = [v["canonical_id"] for v in prov_view.vertices]

    assert "urn:eoip:service:billing" in data_cids
    assert "urn:eoip:service:billing" not in schema_cids
    assert "urn:eoip:service:billing" not in prov_cids

    assert "urn:eoip:domain:finance" in schema_cids
    assert "urn:eoip:domain:finance" not in data_cids

    assert "urn:eoip:run:run-100" in prov_cids
    assert "urn:eoip:run:run-100" not in data_cids


def test_catalog_projections_and_federation():
    """CRA-029.5, CRA-029.8: Projections to OpenMetadata, DataHub, and Atlas; external catalog federation."""
    store = MemoryGraphStore()
    engine = CatalogProjectionEngine(store)

    asset = {
        "canonical_id": "urn:eoip:service:analytics-api",
        "label": "Service",
        "properties": {
            "name": "Analytics API",
            "description": "Public enterprise analytics query service",
            "owner": "data-team",
            "tags": ["Tier-1", "Analytics"],
            "classifications": ["INTERNAL_CONFIDENTIAL"],
        },
    }

    # 1. OpenMetadata projection (CRA-029.8)
    om_json = engine.to_openmetadata(asset)
    assert om_json["name"] == "Analytics API"
    assert "eoip.service" in om_json["fullyQualifiedName"]
    assert om_json["owners"][0]["name"] == "data-team"

    # 2. LinkedIn DataHub projection (CRA-029.8)
    dh_json = engine.to_datahub(asset)
    assert dh_json["entityType"] == "dataset"
    assert "urn:li:dataset:" in dh_json["entityUrn"]
    assert dh_json["aspect"]["name"] == "Analytics API"

    # 3. Apache Atlas projection (CRA-029.8)
    atlas_json = engine.to_apache_atlas(asset)
    assert atlas_json["typeName"] == "eoip_service"
    assert atlas_json["attributes"]["name"] == "Analytics API"
    assert atlas_json["classifications"][0]["typeName"] == "INTERNAL_CONFIDENTIAL"

    # 4. Catalog Federation (CRA-029.5)
    fed_source = FederatedCatalogSource(
        source_id="openmetadata-prod",
        catalog_type="OPENMETADATA",
        endpoint_url="https://openmetadata.corp.internal/api/v1",
        authoritative_domains={"FINANCE"},
    )
    engine.register_federated_source(fed_source)

    # Ingest external asset
    res_fed = engine.federate_external_asset(
        source_id="openmetadata-prod",
        external_asset={
            "canonical_id": "urn:eoip:service:ledger-db",
            "name": "General Ledger Database",
            "description": "SAP GL database mirror",
        },
        authoritative=True,
    )
    assert res_fed["status"] == "FEDERATED_UPSERT"
    assert store.get_vertex_by_canonical_id("urn:eoip:service:ledger-db") is not None
