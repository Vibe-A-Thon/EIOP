"""Unit Tests for Continuous Compliance Dashboard (COMPLY-003) & Search Analytics (UI-008)."""

import json
import pytest
from eoip.compliance.dashboard import (
    AttestationStatus,
    AttestationWorkflow,
    ContinuousComplianceDashboard,
    EvidenceCollector,
    ReadinessTier,
    get_compliance_dashboard,
)
from eoip.graph.memory import MemoryGraphStore
from eoip.search.analytics import (
    SearchAnalyticsEngine,
    get_search_analytics_engine,
)


@pytest.mark.req("COMPLY-003")
class TestContinuousComplianceDashboard:
    def test_framework_scoring_and_audit_export(self):
        dashboard = ContinuousComplianceDashboard()
        store = MemoryGraphStore()

        # Add valid vertices
        store.upsert_vertex("Service", {"name": "AuthService", "service_id": "srv_auth", "canonical_id": "srv_auth", "criticality": "LOW"})
        store.upsert_vertex("Database", {"name": "UserDataDB", "canonical_id": "db_user", "description": "Customer DB encrypted"})

        # Collect evidence
        artifacts = dashboard.evidence_collector.collect_from_graph(store, control_id="SEC-01", framework="SOC2")
        assert len(artifacts) >= 2
        assert all(len(a.provenance_hash) == 64 for a in artifacts)

        # Compute scores
        scores = dashboard.compute_framework_scores(store)
        assert "GDPR" in scores
        assert "HIPAA" in scores
        assert "SOC2" in scores
        assert scores["SOC2"].passed_controls > 0

        # Export JSON and CSV packages
        json_export = dashboard.export_audit_package_json(store)
        parsed = json.loads(json_export)
        assert "framework_scores" in parsed
        assert parsed["evidence_count"] >= 2

        csv_export = dashboard.export_audit_package_csv(store)
        assert "Framework,Total Controls" in csv_export
        assert "SOC2" in csv_export

    def test_attestation_workflow(self):
        workflow = AttestationWorkflow()
        record = workflow.submit_attestation(
            framework="HIPAA",
            scope_period="2026-Q4",
            attester_id="auditor_jane",
            evidence_ids=["EV-SEC-01-srv_auth"],
        )
        assert record.status == AttestationStatus.PENDING

        signed = workflow.sign_attestation(
            record.attestation_id,
            reviewer_signature="SIG-RSA-99214A",
            comments="Verified encryption and logging controls",
        )
        assert signed.status == AttestationStatus.ATTESTED
        assert signed.reviewer_signature == "SIG-RSA-99214A"


@pytest.mark.req("UI-008")
class TestSearchAnalyticsEngine:
    def test_search_event_logging_and_summary(self):
        engine = SearchAnalyticsEngine()
        ev1 = engine.log_search(query="PaymentGateway latency", dialect="TEXT", latency_ms=12.5, result_count=4)
        engine.log_search(query="UnknownServiceX", dialect="CYPHER", latency_ms=8.0, result_count=0)
        engine.log_search(query="PaymentGateway latency", dialect="TEXT", latency_ms=15.0, result_count=6)

        # Record click
        engine.record_click(ev1.event_id, "srv_payment")

        summary = engine.compute_summary()
        assert summary.total_searches == 3
        assert summary.zero_result_searches == 1
        assert 0.30 <= summary.zero_result_rate <= 0.35
        assert summary.click_through_rate > 0.30
        assert summary.top_queries[0][0] == "paymentgateway latency"
        assert summary.top_queries[0][1] == 2

    def test_relevance_tuning_synonyms_and_boosts(self):
        engine = SearchAnalyticsEngine()
        engine.add_synonym("auth", "login")
        engine.set_term_boost("security", 2.0)

        # Query tokens: ["the", "auth", "security"]
        tokens = ["the", "auth", "security"]
        weighted = engine.apply_relevance_tuning(tokens)

        # "the" is a stopword -> filtered out
        token_names = [t[0] for t in weighted]
        assert "the" not in token_names
        assert "auth" in token_names
        assert "login" in token_names  # Expanded synonym
        assert "security" in token_names

        # Security boost check
        sec_weight = next(w for t, w in weighted if t == "security")
        assert sec_weight == 2.0
