"""Mark WP 5.3 Web UX, admin, and new-engine screens requirements as done."""

from _mark_done import mark_done

TEST_FILE = "tests/unit/test_web_ux_and_admin_wp53.py"

WP53_REQUIREMENTS = {
    "UI-01": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/dashboards/CausalBlastRadiusDashboard.jsx",
            "apps/web/src/dashboards/EngineDashboardsHub.jsx",
            "packages/eoip/graph/causal.py",
        ],
    },
    "UI-02": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/dashboards/MultiParadigmQueryDashboard.jsx",
            "apps/web/src/dashboards/EngineDashboardsHub.jsx",
            "packages/eoip/query/dispatcher.py",
        ],
    },
    "UI-03": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/dashboards/DomainPackDashboard.jsx",
            "apps/web/src/dashboards/EngineDashboardsHub.jsx",
            "packages/eoip/ontology/domain_pack_manager.py",
        ],
    },
    "UI-04": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/dashboards/XAIVerificationDashboard.jsx",
            "apps/web/src/dashboards/EngineDashboardsHub.jsx",
            "packages/eoip/provenance/verifiable_xai.py",
        ],
    },
    "FR-ADMIN-001": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/ConnectorSetupWizard.jsx",
            "apps/web/src/admin/IngestionReconciliationPanel.jsx",
        ],
    },
    "FR-ADMIN-002": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx",
            "apps/web/src/admin/index.jsx",
        ],
    },
    "FR-UI-001": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/dashboards/EngineDashboardsHub.jsx",
            "apps/web/src/App.jsx",
        ],
    },
    "FR-UI-002": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/index.jsx",
            "apps/web/src/dashboards/EngineDashboardsHub.jsx",
        ],
    },
    "G2-ADMIN-002": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/ConnectorSetupWizard.jsx",
        ],
    },
    "G2-ADMIN-003": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/IngestionReconciliationPanel.jsx",
        ],
    },
    "G2-ADMIN-004": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/CheckpointAndRecoveryPanel.jsx",
        ],
    },
    "G2-ADMIN-005": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/CheckpointAndRecoveryPanel.jsx",
        ],
    },
    "G2-ADMIN-006": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/SchemaDriftAndFreshnessPanel.jsx",
        ],
    },
    "G2-ADMIN-007": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/SchemaDriftAndFreshnessPanel.jsx",
        ],
    },
    "G2-ADMIN-008": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/GraphTimelineAndJournalPanel.jsx",
        ],
    },
    "G2-ADMIN-009": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/GraphTimelineAndJournalPanel.jsx",
        ],
    },
    "G2-ADMIN-010": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/GraphTimelineAndJournalPanel.jsx",
        ],
    },
    "G2-ADMIN-011": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/CrawlSafetyAndTelemetryPanel.jsx",
        ],
    },
    "G2-ADMIN-012": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/CrawlSafetyAndTelemetryPanel.jsx",
        ],
    },
    "G2-ADMIN-013": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/CrawlSafetyAndTelemetryPanel.jsx",
        ],
    },
    "G2-ADMIN-014": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx",
        ],
    },
    "G2-ADMIN-015": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx",
        ],
    },
    "G2-ADMIN-016": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx",
        ],
    },
    "G2-ADMIN-017": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx",
        ],
    },
    "G2-UX-GRAPH-002": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/GraphCanvas.jsx",
        ],
    },
    "G2-UX-GRAPH-003": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/GraphCanvas.jsx",
        ],
    },
    "G2-UX-GRAPH-004": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/GraphCanvas.jsx",
        ],
    },
    "G2-UX-GRAPH-005": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/GraphCanvas.jsx",
        ],
    },
    "G2-UX-GRAPH-006": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/GraphCanvas.jsx",
        ],
    },
    "G2-UX-GRAPH-007": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/GraphCanvas.jsx",
        ],
    },
    "G2-UX-GRAPH-008": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/GraphCanvas.jsx",
        ],
    },
    "G2-UX-GRAPH-009": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/GraphCanvas.jsx",
        ],
    },
    "G2-UX-GRAPH-010": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/GraphCanvas.jsx",
        ],
    },
    "G2-UX-GRAPH-011": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/GraphCanvas.jsx",
        ],
    },
    "G2-UX-GRAPH-012": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/GraphCanvas.jsx",
        ],
    },
    "G2-UX-GRAPH-013": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/GraphCanvas.jsx",
        ],
    },
    "G2-UX-GRAPH-014": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/GraphCanvas.jsx",
        ],
    },
    "G2-UX-GRAPH-015": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/GraphCanvas.jsx",
        ],
    },
    "G2-UX-GRAPH-016": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/GraphCanvas.jsx",
        ],
    },
    "G2-UX-LENS-002": {
        "test_file": TEST_FILE,
        "code_paths": [
            "packages/eoip/graph/lens.py",
        ],
    },
    "G2-UX-LENS-003": {
        "test_file": TEST_FILE,
        "code_paths": [
            "packages/eoip/graph/lens.py",
        ],
    },
    "G2-UX-PLAY-002": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/Playground.jsx",
        ],
    },
    "G2-UX-PLAY-003": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/Playground.jsx",
        ],
    },
    "G2-UX-PLAY-004": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/Playground.jsx",
        ],
    },
    "G2-UX-PLAY-005": {
        "test_file": TEST_FILE,
        "code_paths": [
            "apps/web/src/components/Playground.jsx",
        ],
    },
}

if __name__ == "__main__":
    mark_done(WP53_REQUIREMENTS)
