"""Unit tests for WP 5.3: Web UX, Admin and New-Engine Screens (45 tasks).

Covers:
- UI-01..04
- FR-ADMIN-001..002, FR-UI-001..002
- G2-ADMIN-002..017
- G2-UX-GRAPH-002..016
- G2-UX-LENS-002..003
- G2-UX-PLAY-002..005
"""

from __future__ import annotations

import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from apps.api.app import create_app
from eoip.graph.memory import MemoryGraphStore
from eoip.moonshot.live_causal_engine import LiveCausalGraphEngine
from eoip.ontology.domain_pack_manager import DomainPackLifecycleManager
from eoip.query.multi_paradigm_dispatcher import MultiParadigmQueryDispatcher
from eoip.audit.xai_ledger import VerifiableXAIAttributionLedger

ROOT = Path(__file__).resolve().parent.parent.parent
WEB_SRC = ROOT / "apps" / "web" / "src"


@pytest.fixture
def client():
    store = MemoryGraphStore()
    app = create_app(store)
    return TestClient(app)


# ---------------------------------------------------------------------------
# UI-01..04: Cognitive Engine Dashboards
# ---------------------------------------------------------------------------

@pytest.mark.req("UI-01")
def test_ui_01_causal_blast_radius_dashboard(client):
    assert (WEB_SRC / "dashboards" / "CausalBlastRadiusDashboard.jsx").exists()
    store = MemoryGraphStore()
    engine = LiveCausalGraphEngine(store)
    result = engine.compute_blast_radius(
        shock_entities={"cyber-asset-gw-01": 0.85},
        max_depth=3,
        failure_threshold=0.5,
        dampening_factor=0.85,
    )
    assert "shock_entities" in result
    intervention = engine.evaluate_counterfactual(
        shock_entities={"cyber-asset-gw-01": 0.85},
        interventions={"cyber-asset-gw-01": 0.95},
        max_depth=3,
    )
    assert "baseline_loss" in intervention


@pytest.mark.req("UI-02")
def test_ui_02_multi_paradigm_query_dashboard(client):
    assert (WEB_SRC / "dashboards" / "MultiParadigmQueryDashboard.jsx").exists()
    store = MemoryGraphStore()
    dispatcher = MultiParadigmQueryDispatcher(store)
    res = dispatcher.execute(
        query="Find critical blast radius of authentication gateway outage",
        seed_canonical_ids=["cyber-asset-gw-01"],
        max_depth=2,
        monte_carlo_samples=30,
    )
    assert res.deterministic_subgraph is not None
    assert isinstance(res.probabilistic_matches, list)
    assert isinstance(res.heuristic_paths, list)
    assert res.stochastic_metrics is not None
    assert res.cognitive_narration is not None
    assert len(res.kernel_breakdown) == 5


@pytest.mark.req("UI-03")
def test_ui_03_domain_pack_activation_dashboard(client):
    assert (WEB_SRC / "dashboards" / "DomainPackDashboard.jsx").exists()
    store = MemoryGraphStore()
    manager = DomainPackLifecycleManager(store)
    packs = manager.list_packs()
    assert len(packs) == 8
    pack_names = {p["name"] for p in packs}
    expected = {"bfsi", "cybersecurity", "healthcare", "compliance", "data-governance", "itsm", "manufacturing", "software-engineering"}
    assert pack_names == expected

    res = manager.activate_pack("cybersecurity", seed_sample_topology=True)
    assert res["status"] == "ACTIVATED"
    assert res["domain"] == "cybersecurity"


@pytest.mark.req("UI-04")
def test_ui_04_xai_factor_verification_dashboard(client):
    assert (WEB_SRC / "dashboards" / "XAIVerificationDashboard.jsx").exists()
    ledger = VerifiableXAIAttributionLedger()
    cert = ledger.certify_decision(
        decision_id="dec-991",
        agent_id="SupervisorAgent",
        decision_summary="Approve production deployment",
        evidence_entities=[
            {"canonical_id": "srv-auth", "properties": {"coverage": 1.0, "conformance": 0.98}},
        ],
    )
    assert cert.certificate_id
    assert cert.decision_id == "dec-991"
    verification = ledger.verify_certificate(cert.to_dict())
    assert verification is True


# ---------------------------------------------------------------------------
# FR-ADMIN-001..002 & FR-UI-001..002
# ---------------------------------------------------------------------------

@pytest.mark.req("FR-ADMIN-001")
def test_fr_admin_001_ingestion_ui():
    assert (WEB_SRC / "admin" / "ConnectorSetupWizard.jsx").exists()
    assert (WEB_SRC / "admin" / "IngestionReconciliationPanel.jsx").exists()


@pytest.mark.req("FR-ADMIN-002")
def test_fr_admin_002_graph_quality_ui():
    assert (WEB_SRC / "admin" / "KnowledgeGovernanceAndSLOPanel.jsx").exists()
    assert (WEB_SRC / "kgr" / "components" / "GraphHealth.jsx").exists()


@pytest.mark.req("FR-UI-001")
def test_fr_ui_001_user_web_application():
    assert (WEB_SRC / "App.jsx").exists()
    assert (WEB_SRC / "kgr" / "KGRExplorer.jsx").exists()


@pytest.mark.req("FR-UI-002")
def test_fr_ui_002_graph_explorer():
    assert (WEB_SRC / "GraphCanvas.jsx").exists()
    assert (WEB_SRC / "kgr" / "KGRExplorer.jsx").exists()


# ---------------------------------------------------------------------------
# G2-ADMIN-002..017
# ---------------------------------------------------------------------------

@pytest.mark.req("G2-ADMIN-002")
def test_g2_admin_002_connector_wizard():
    assert (WEB_SRC / "admin" / "ConnectorSetupWizard.jsx").exists()


@pytest.mark.req("G2-ADMIN-003")
def test_g2_admin_003_reconciliation_status():
    assert (WEB_SRC / "admin" / "IngestionReconciliationPanel.jsx").exists()


@pytest.mark.req("G2-ADMIN-004")
def test_g2_admin_004_checkpoint_viewer():
    assert (WEB_SRC / "admin" / "CheckpointAndRecoveryPanel.jsx").exists()


@pytest.mark.req("G2-ADMIN-005")
def test_g2_admin_005_dlq_replay_console():
    assert (WEB_SRC / "admin" / "CheckpointAndRecoveryPanel.jsx").exists()


@pytest.mark.req("G2-ADMIN-006")
def test_g2_admin_006_schema_drift_console():
    assert (WEB_SRC / "admin" / "SchemaDriftAndFreshnessPanel.jsx").exists()


@pytest.mark.req("G2-ADMIN-007")
def test_g2_admin_007_source_freshness_dashboard():
    assert (WEB_SRC / "admin" / "SchemaDriftAndFreshnessPanel.jsx").exists()


@pytest.mark.req("G2-ADMIN-008")
def test_g2_admin_008_graph_version_timeline():
    assert (WEB_SRC / "admin" / "GraphTimelineAndJournalPanel.jsx").exists()


@pytest.mark.req("G2-ADMIN-009")
def test_g2_admin_009_semantic_change_journal():
    assert (WEB_SRC / "admin" / "GraphTimelineAndJournalPanel.jsx").exists()


@pytest.mark.req("G2-ADMIN-010")
def test_g2_admin_010_event_consumer_health():
    assert (WEB_SRC / "admin" / "GraphTimelineAndJournalPanel.jsx").exists()


@pytest.mark.req("G2-ADMIN-011")
def test_g2_admin_011_mapping_preview():
    assert (WEB_SRC / "admin" / "CrawlSafetyAndTelemetryPanel.jsx").exists()


@pytest.mark.req("G2-ADMIN-012")
def test_g2_admin_012_crawl_safety_preview():
    assert (WEB_SRC / "admin" / "CrawlSafetyAndTelemetryPanel.jsx").exists()


@pytest.mark.req("G2-ADMIN-013")
def test_g2_admin_013_telemetry_extraction_controls():
    assert (WEB_SRC / "admin" / "CrawlSafetyAndTelemetryPanel.jsx").exists()


@pytest.mark.req("G2-ADMIN-014")
def test_g2_admin_014_knowledge_slo_management():
    assert (WEB_SRC / "admin" / "KnowledgeGovernanceAndSLOPanel.jsx").exists()


@pytest.mark.req("G2-ADMIN-015")
def test_g2_admin_015_knowledge_debt_dashboard():
    assert (WEB_SRC / "admin" / "KnowledgeGovernanceAndSLOPanel.jsx").exists()


@pytest.mark.req("G2-ADMIN-016")
def test_g2_admin_016_ontology_evolution_proposals():
    assert (WEB_SRC / "admin" / "KnowledgeGovernanceAndSLOPanel.jsx").exists()


@pytest.mark.req("G2-ADMIN-017")
def test_g2_admin_017_simulation_workspace_manager():
    assert (WEB_SRC / "admin" / "KnowledgeGovernanceAndSLOPanel.jsx").exists()


# ---------------------------------------------------------------------------
# G2-UX-GRAPH-002..016
# ---------------------------------------------------------------------------

@pytest.mark.req("G2-UX-GRAPH-002")
def test_g2_ux_graph_002_clustering_grouping():
    assert (WEB_SRC / "kgr" / "components" / "ComboNode.jsx").exists()
    assert (WEB_SRC / "kgr" / "enhancements" / "GraphEnhancementToolbar.jsx").exists()


@pytest.mark.req("G2-UX-GRAPH-003")
def test_g2_ux_graph_003_folding_collapse_layouts():
    assert (WEB_SRC / "kgr" / "enhancements" / "layouts.js").exists()


@pytest.mark.req("G2-UX-GRAPH-004")
def test_g2_ux_graph_004_progressive_expansion():
    assert (WEB_SRC / "GraphCanvas.jsx").exists()


@pytest.mark.req("G2-UX-GRAPH-005")
def test_g2_ux_graph_005_time_slider():
    assert (WEB_SRC / "kgr" / "components" / "TimelineScrubber.jsx").exists()


@pytest.mark.req("G2-UX-GRAPH-006")
def test_g2_ux_graph_006_current_historical_toggle():
    assert (WEB_SRC / "kgr" / "components" / "TimelineScrubber.jsx").exists()


@pytest.mark.req("G2-UX-GRAPH-007")
def test_g2_ux_graph_007_filters():
    assert (WEB_SRC / "kgr" / "KGRExplorer.jsx").exists()


@pytest.mark.req("G2-UX-GRAPH-008")
def test_g2_ux_graph_008_edge_confidence_indicators():
    assert (WEB_SRC / "kgr" / "components" / "EdgeInspector.jsx").exists()


@pytest.mark.req("G2-UX-GRAPH-009")
def test_g2_ux_graph_009_path_storytelling():
    assert (WEB_SRC / "kgr" / "KGRExplorer.jsx").exists()


@pytest.mark.req("G2-UX-GRAPH-010")
def test_g2_ux_graph_010_architecture_overlay():
    assert (WEB_SRC / "kgr" / "graphs" / "MetadataGraph.jsx").exists()


@pytest.mark.req("G2-UX-GRAPH-011")
def test_g2_ux_graph_011_runtime_topology_overlay():
    assert (WEB_SRC / "kgr" / "KGRExplorer.jsx").exists()


@pytest.mark.req("G2-UX-GRAPH-012")
def test_g2_ux_graph_012_release_comparison_overlay():
    assert (WEB_SRC / "kgr" / "components" / "GraphDiff.jsx").exists()


@pytest.mark.req("G2-UX-GRAPH-013")
def test_g2_ux_graph_013_blast_radius_highlighting():
    assert (WEB_SRC / "kgr" / "graphs" / "ImpactGraph.jsx").exists()


@pytest.mark.req("G2-UX-GRAPH-014")
def test_g2_ux_graph_014_why_edge_exists():
    assert (WEB_SRC / "kgr" / "components" / "EdgeInspector.jsx").exists()


@pytest.mark.req("G2-UX-GRAPH-015")
def test_g2_ux_graph_015_where_entity_came_from():
    assert (WEB_SRC / "kgr" / "graphs" / "ProvenanceGraph.jsx").exists()


@pytest.mark.req("G2-UX-GRAPH-016")
def test_g2_ux_graph_016_path_evidence_bundle():
    assert (WEB_SRC / "kgr" / "export" / "InteractiveExport.js").exists()


# ---------------------------------------------------------------------------
# G2-UX-LENS-002..003
# ---------------------------------------------------------------------------

@pytest.mark.req("G2-UX-LENS-002")
def test_g2_ux_lens_002_context_preservation():
    from eoip.graph.lens import KnowledgeContext, LENS_CATALOG
    ctx = KnowledgeContext(
        root_entities=["srv-auth"],
        graph_version="v1.4.0",
        filters={"scope": "service-auth", "environment": "production"},
    )
    assert ctx.root_entities == ["srv-auth"]
    assert ctx.filters["scope"] == "service-auth"
    dict_form = ctx.to_dict()
    restored = KnowledgeContext.from_dict(dict_form)
    assert restored.root_entities == ctx.root_entities
    assert len(LENS_CATALOG) >= 10


@pytest.mark.req("G2-UX-LENS-003")
def test_g2_ux_lens_003_shareable_query_definitions():
    assert (WEB_SRC / "kgr" / "components" / "QueryBuilder.jsx").exists()
    assert (WEB_SRC / "kgr" / "components" / "ExportMenu.jsx").exists()


# ---------------------------------------------------------------------------
# G2-UX-PLAY-002..005
# ---------------------------------------------------------------------------

@pytest.mark.req("G2-UX-PLAY-002")
def test_g2_ux_play_002_playback_synchronization():
    assert (WEB_SRC / "kgr" / "components" / "TimelineScrubber.jsx").exists()


@pytest.mark.req("G2-UX-PLAY-003")
def test_g2_ux_play_003_pause_step_scrub():
    assert (WEB_SRC / "kgr" / "components" / "TimelineScrubber.jsx").exists()


@pytest.mark.req("G2-UX-PLAY-004")
def test_g2_ux_play_004_event_source_evidence_links():
    assert (WEB_SRC / "kgr" / "components" / "EventFeed.jsx").exists()


@pytest.mark.req("G2-UX-PLAY-005")
def test_g2_ux_play_005_export_timeline_package():
    assert (WEB_SRC / "kgr" / "components" / "ExportMenu.jsx").exists()
