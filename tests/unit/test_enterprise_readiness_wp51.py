"""Tests for Phase 5 WP 5.1: Enterprise Readiness (7 tasks).

Requirements:
- GAP-APP: Knowledge app builder
- GAP-CATALOG: Knowledge catalog
- GAP-GOV: Semantic stewardship workflow
- GAP-HA: High availability patterns
- GAP-IDE: VS Code extension completion
- GAP-NOCODE: Visual ontology studio
- GAP-TEMPLATE: Industry templates
"""

import json
from pathlib import Path
import pytest

from eoip.catalog.products import KnowledgeProduct, KnowledgeProductCatalog, ProductState
from eoip.dashboards.builder import DashboardBuilder, WidgetDataSource, WidgetType
from eoip.graph.memory import MemoryGraphStore
from eoip.ha import LeaderLease
from eoip.ontology.industry_templates import (
    INDUSTRY_TEMPLATES,
    get_industry_template,
    list_industry_templates,
)
from eoip.ontology.stewardship import (
    GovernanceState,
    OntologyBranch,
    SemanticStewardshipManager,
)
from eoip.ontology.studio import OntologyStudioProject, StudioMode


# --- 1. GAP-APP: Knowledge App Builder ---

@pytest.mark.req("GAP-APP")
def test_gap_app_dashboard_builder():
    builder = DashboardBuilder()
    dashboard = builder.new_dashboard("Executive Knowledge Twin", description="Executive view")
    # Add KPI gauge / metric card
    builder.add_metric_card(
        dashboard.dashboard_id,
        title="Knowledge Health Score",
        metric_query="SELECT health_score FROM knowledge_health",
        unit="%",
        threshold=90.0,
    )
    # Add Graph Topology panel
    builder.add_topology_view(
        dashboard.dashboard_id,
        title="Service Dependency Mesh",
        entity_types=["Service", "APIService"],
    )
    # Add Table panel
    builder.add_chart(
        dashboard.dashboard_id,
        title="Knowledge Debt Catalog",
        chart_type=WidgetType.TABLE,
        query="SELECT * FROM knowledge_debt",
    )
    # Add Timeline panel
    builder.add_chart(
        dashboard.dashboard_id,
        title="Incident Timeline",
        chart_type=WidgetType.TIMELINE,
        query="SELECT * FROM incident_events ORDER BY timestamp",
    )

    d = builder.store.get(dashboard.dashboard_id)
    assert d is not None
    assert len(d.widgets) == 4
    types = {w.widget_type for w in d.widgets}
    assert WidgetType.METRIC_CARD in types
    assert WidgetType.GRAPH_TOPOLOGY in types
    assert WidgetType.TABLE in types
    assert WidgetType.TIMELINE in types


# --- 2. GAP-CATALOG: Knowledge Catalog ---

@pytest.mark.req("GAP-CATALOG")
def test_gap_catalog_products_and_lineage():
    store = MemoryGraphStore()
    catalog = KnowledgeProductCatalog(store)

    product = catalog.create(
        KnowledgeProduct(
            name="Customer 360 Knowledge Product",
            owner="data-steward@enterprise.local",
            domain="COMMERCE",
            description="Unified view of customers, contracts, and interaction history",
            source_graphs=["crm_graph", "billing_graph"],
            consumers=["support_copilot", "executive_bi"],
            state=ProductState.DRAFT,
        )
    )
    assert product.canonical_id
    assert product.state == ProductState.DRAFT

    # Transition certification state: DRAFT -> EXPERIMENTAL -> TRUSTED -> CERTIFIED
    updated = catalog.transition(product.canonical_id, ProductState.EXPERIMENTAL)
    assert updated.state == ProductState.EXPERIMENTAL
    updated = catalog.transition(product.canonical_id, ProductState.TRUSTED)
    assert updated.state == ProductState.TRUSTED
    updated = catalog.transition(product.canonical_id, ProductState.CERTIFIED)
    assert updated.state == ProductState.CERTIFIED

    # Check lineage navigation
    lineage = catalog.lineage(product.canonical_id)
    source_names = [g["source_graph"] for g in lineage["source_graphs"]]
    consumer_names = [c["consumer"] for c in lineage["consumers"]]
    assert "crm_graph" in source_names
    assert "support_copilot" in consumer_names
    assert lineage["product_id"] == product.canonical_id


# --- 3. GAP-GOV: Semantic Stewardship Workflow ---

@pytest.mark.req("GAP-GOV")
def test_gap_gov_stewardship_workflow():
    manager = SemanticStewardshipManager()
    branch = manager.create_branch("feature/billing-v2", author="lead_steward")
    assert branch.state == GovernanceState.DRAFT

    # Add a new vertex label to branch manifest
    branch.manifest.setdefault("vertex_labels", {})["CryptocurrencyPayment"] = (
        "FINANCE",
        ("canonical_id", "wallet_address"),
        ("currency", "tx_hash"),
    )

    # Transition through governance states: DRAFT -> IN_REVIEW -> APPROVED
    manager.transition_state("feature/billing-v2", GovernanceState.IN_REVIEW, actor="lead_steward", comment="Ready for review")
    assert branch.state == GovernanceState.IN_REVIEW

    manager.transition_state("feature/billing-v2", GovernanceState.APPROVED, actor="chief_architect", comment="Approved for merge")
    assert branch.state == GovernanceState.APPROVED

    # Check diff with main
    diff = manager.diff_with_main("feature/billing-v2")
    assert diff.safe is True
    assert any(c.change_type == "vertex_label_added" for c in diff.changes)

    # Merge to main
    merge_result = manager.merge_to_main("feature/billing-v2", approver="chief_architect")
    assert merge_result["status"] == "MERGED"
    assert branch.state == GovernanceState.PUBLISHED


# --- 4. GAP-HA: High Availability Patterns ---

@pytest.mark.req("GAP-HA")
def test_gap_ha_leader_lease_failover(tmp_path):
    lock_file = tmp_path / "worker.lock"
    primary = LeaderLease(lock_file, ttl_seconds=1.0)
    secondary = LeaderLease(lock_file, ttl_seconds=1.0)

    # Primary acquires lease
    assert primary.acquire() is True
    assert primary.renew() is True

    # Secondary cannot acquire while primary holds valid lease
    assert secondary.acquire() is False

    # Primary releases lease
    primary.release()

    # Secondary can now acquire lease (failover)
    assert secondary.acquire() is True
    assert secondary.renew() is True
    secondary.release()


# --- 5. GAP-IDE: VS Code Extension Completion ---

@pytest.mark.req("GAP-IDE")
def test_gap_ide_extension_manifest_and_mcp_bridge():
    root = Path(__file__).resolve().parents[2]
    ext_js = root / "apps" / "vscode-extension" / "extension.js"
    pkg_json = root / "apps" / "vscode-extension" / "package.json"
    mcp_js = root / "apps" / "vscode-extension" / "mcp-client.js"

    assert ext_js.exists()
    assert pkg_json.exists()
    assert mcp_js.exists()

    ext_content = ext_js.read_text(encoding="utf-8")
    assert "vscode" in ext_content
    assert "createWebviewPanel" in ext_content or "registerCommand" in ext_content

    pkg_data = json.loads(pkg_json.read_text(encoding="utf-8"))
    assert "contributes" in pkg_data
    commands = [c["command"] for c in pkg_data["contributes"].get("commands", [])]
    assert len(commands) >= 1


# --- 6. GAP-NOCODE: Visual Ontology Studio ---

@pytest.mark.req("GAP-NOCODE")
def test_gap_nocode_visual_ontology_studio():
    project = OntologyStudioProject("RetailOntology", mode=StudioMode.ANALYST)
    assert project.mode == StudioMode.ANALYST

    # Add class nodes
    order_node = project.add_class("Order", domain="SALES", description="Customer orders", x=100, y=200)
    customer_node = project.add_class("Customer", domain="CRM", description="Client profiles", x=400, y=200)

    # Add properties
    project.add_property_to_class("Order", "total_amount", property_type="DOUBLE", required=True)
    project.add_property_to_class("Order", "order_date", property_type="DATE")
    project.add_property_to_class("Customer", "email", property_type="TEXT", required=True)

    # Add relationship edge
    rel_edge = project.add_relationship("PLACED_BY", source_class="Order", target_class="Customer", cardinality="N:1")
    assert rel_edge.cardinality == "N:1"

    # Validate canvas
    validation = project.validate()
    assert validation["valid"] is True
    assert validation["class_count"] == 2
    assert validation["relationship_count"] == 1

    # Export schema
    schema = project.export_schema()
    assert "Order" in schema["classes"]
    assert "Customer" in schema["classes"]
    assert "PLACED_BY" in schema["relationships"]


# --- 7. GAP-TEMPLATE: Industry Templates ---

@pytest.mark.req("GAP-TEMPLATE")
def test_gap_template_industry_templates():
    templates = list_industry_templates()
    assert len(templates) == 6
    categories = {t["category"] for t in templates}
    assert {"engineering", "audit", "risk", "incident", "architecture", "compliance"} <= categories

    for cat in ("engineering", "audit", "risk", "incident", "architecture", "compliance"):
        tmpl = get_industry_template(cat)
        assert tmpl.name
        assert len(tmpl.classes) >= 2
        assert len(tmpl.relationships) >= 1
        assert len(tmpl.recommended_queries) >= 1
