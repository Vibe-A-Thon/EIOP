"""Acceptance test suite for Observability & Operational-System Adapters (WP-008, CRA-008.1-008.9, CRA-008.A)."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from eoip.connectors.errors import ConnectorError
from eoip.connectors.factory import ConnectorFactory
from eoip.connectors.grafana import GrafanaConnector
from eoip.connectors.kibana import KibanaConnector
from eoip.connectors.servicenow import ServiceNowConnector
from eoip.connectors.splunk import RedactionReceipt, SearchBudget, SplunkConnector, redact_with_receipt
from eoip.contracts.source_event import SourceEventV2
from eoip.mapping import parse_and_compile_cml
from eoip.observability.telemetry_separation import (
    InferredCausality,
    ObservedTelemetry,
    TelemetryCausalityBoundary,
)

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures" / "connectors"
SNOW_FIXTURE = FIXTURES_DIR / "servicenow" / "cmdb_incidents.json"
SPLUNK_FIXTURE = FIXTURES_DIR / "splunk" / "saved_searches.json"
KIBANA_FIXTURE = FIXTURES_DIR / "kibana" / "saved_objects.json"
GRAFANA_FIXTURE = FIXTURES_DIR / "grafana" / "dashboards.json"


# ===========================================================================
# CRA-008.1: ServiceNow qualification and domain separation
# ===========================================================================

def test_cra_008_1_servicenow_qualification_and_domain_separation():
    snow = ServiceNowConnector("https://instance.service-now.com", token="sn-token")
    data = json.loads(SNOW_FIXTURE.read_text(encoding="utf-8"))

    # Global CI record
    global_ci = data["configuration_items"][0]
    evt_global = snow.make_event("cmdb_ci", f"cmdb_ci:{global_ci['sys_id']}", global_ci, "1")
    assert evt_global.permissions.visibility == "INTERNAL"
    assert "servicenow:domain:global" in evt_global.permissions.principal_refs
    assert "servicenow:role:cmdb_read" in evt_global.permissions.principal_refs

    # Domain-separated CI record (restricted partition)
    secret_ci = data["configuration_items"][2]
    evt_secret = snow.make_event("cmdb_ci", f"cmdb_ci:{secret_ci['sys_id']}", secret_ci, "1")
    assert evt_secret.permissions.visibility == "RESTRICTED"
    assert "servicenow:domain:domain-secret-finance" in evt_secret.permissions.principal_refs
    assert evt_secret.permissions.inherited_from == "servicenow:domain:domain-secret-finance"


# ===========================================================================
# CRA-008.2: Splunk search budgets and sensitive log authorization
# ===========================================================================

def test_cra_008_2_splunk_budget_and_sensitive_log_auth():
    budget = SearchBudget(max_results=50, timeout_seconds=5.0, max_search_span_hours=24)
    splunk = SplunkConnector("splunk-inst-1", "https://splunk.corp.internal:8089", budget=budget)

    # Within budget: succeeds
    splunk.validate_budget(result_count=40, execution_time_seconds=2.1)

    # Exceeding count budget raises ConnectorError
    with pytest.raises(ConnectorError) as exc_count:
        splunk.validate_budget(result_count=100, execution_time_seconds=2.0)
    assert exc_count.value.category == "budget_exceeded"

    # Exceeding time budget raises ConnectorError
    with pytest.raises(ConnectorError) as exc_time:
        splunk.validate_budget(result_count=30, execution_time_seconds=10.0)
    assert exc_time.value.category == "budget_exceeded"

    # Saved search event creation scrubbed
    evt, receipt = splunk.make_saved_search_event(
        search_name="test_search",
        search_query="index=main token=ghp_ABC123456789012345678 password=SecretPassword123",
    )
    assert "[REDACTED_TOKEN]" in evt.payload["search"]
    assert "[REDACTED_PASSWORD]" in evt.payload["search"]
    assert "ghp_ABC123" not in evt.payload["search"]
    assert "SecretPassword123" not in evt.payload["search"]
    assert receipt.total_redacted == 2


# ===========================================================================
# CRA-008.3: Kibana spaces vs index authority separation
# ===========================================================================

def test_cra_008_3_kibana_spaces_vs_index_authority():
    kibana = KibanaConnector("https://kibana.corp.internal:5601", token="kb-token", space_id="payments_space")
    data = json.loads(KIBANA_FIXTURE.read_text(encoding="utf-8"))
    obj = data["saved_objects"][0]

    evt = kibana.make_event("dashboard", f"dashboard:{obj['id']}", obj, obj["version"])
    assert evt.permissions.principal_refs == ["kibana:space:payments_space"]
    assert evt.metadata["space_id"] == "payments_space"
    # Strict index authority separation: dashboard auth != backing index authority
    assert evt.metadata["index_authority_separated"] is True
    assert evt.metadata["backing_indices_authorized"] is False


# ===========================================================================
# CRA-008.4: Grafana data-source secrets protection
# ===========================================================================

def test_cra_008_4_grafana_datasource_secrets_protection():
    grafana = GrafanaConnector("https://grafana.corp.internal:3000", token="gf-token", org_id=12)
    data = json.loads(GRAFANA_FIXTURE.read_text(encoding="utf-8"))
    raw_ds = data["datasources"][0]

    # Stored secrets must be thoroughly scrubbed
    scrubbed = grafana.scrub_datasource_secrets(raw_ds)
    assert "password" not in scrubbed
    assert "basicAuthPassword" not in scrubbed
    assert "secureJsonData" not in scrubbed
    assert scrubbed["jsonData"]["customAuthToken"] == "[REDACTED]"
    assert "super_secret_auth_password_do_not_leak" not in json.dumps(scrubbed)
    assert "another_db_secret_password" not in json.dumps(scrubbed)

    evt = grafana.make_event("datasource", f"datasource:{raw_ds['id']}", scrubbed, scrubbed["version"])
    assert "grafana:org:12" in evt.permissions.principal_refs
    assert "super_secret" not in json.dumps(evt.payload)


# ===========================================================================
# CRA-008.5: Observed telemetry separate from inferred causality
# ===========================================================================

def test_cra_008_5_telemetry_separate_from_inferred_causality():
    telemetry = ObservedTelemetry(
        telemetry_id="telem-001",
        metric_name="http_request_duration_seconds",
        timestamp="2026-10-18T10:00:00Z",
        value=3.45,
        source_sampling_rate=0.25,
        staleness_seconds=12.5,
        is_missing=False,
        uncertainty_margin=0.08,
        source_system="grafana",
        dimensions={"service": "payments-api-service", "status": "503"},
    )
    causality = InferredCausality(
        inference_id="infer-001",
        incident_id="INC009001",
        affected_ci="ci-101",
        root_cause_ci="ci-102",
        confidence=0.88,
        evidence_telemetry_ids=["telem-001"],
        hypothesis="Database connection pool exhaustion caused API latency degradation",
    )

    # Valid separation passes
    assert TelemetryCausalityBoundary.assert_separation(telemetry, causality) is True

    # Telemetry contaminated with causal assertion fails
    bad_telemetry = ObservedTelemetry(
        telemetry_id="telem-bad",
        metric_name="error_rate",
        timestamp="2026-10-18T10:00:00Z",
        value=0.9,
        dimensions={"root_cause": "database_deadlock"},
    )
    with pytest.raises(ValueError, match="contaminated with inferred causality"):
        TelemetryCausalityBoundary.assert_separation(bad_telemetry, causality)

    # Causality lacking evidence telemetry fails
    groundless_causality = InferredCausality(
        inference_id="infer-bad",
        incident_id="INC009001",
        affected_ci="ci-101",
        root_cause_ci="ci-102",
        confidence=0.5,
        evidence_telemetry_ids=[],
    )
    with pytest.raises(ValueError, match="must cite at least one evidence"):
        TelemetryCausalityBoundary.assert_separation(telemetry, groundless_causality)

    # Write-back without warrant is rejected
    with pytest.raises(PermissionError, match="GovernedAction warrant"):
        TelemetryCausalityBoundary.check_write_back_governance({"action": "restart_service"})


# ===========================================================================
# CRA-008.6: ServiceNow table profiles, roles, and write-back lock
# ===========================================================================

def test_cra_008_6_servicenow_table_profiles_and_roles():
    snow = ServiceNowConnector("https://instance.service-now.com", token="sn-token")
    assert "cmdb_ci" in snow.tables
    assert "cmdb_rel_ci" in snow.tables
    assert "incident" in snow.tables
    assert "change" in snow.tables
    assert "problem" in snow.tables
    assert "knowledge" in snow.tables

    # Role populating ACL
    ci_evt = snow.make_event("cmdb_ci", "cmdb_ci:101", {"sys_id": "101", "name": "srv1"}, "1")
    assert "servicenow:role:cmdb_read" in ci_evt.metadata["acl_vector"]

    inc_evt = snow.make_event("incident", "incident:901", {"sys_id": "901", "number": "INC901"}, "1")
    assert "servicenow:role:itil" in inc_evt.metadata["acl_vector"]


# ===========================================================================
# CRA-008.7: Dashboard panels linking to CMDB services as proposals
# ===========================================================================

def test_cra_008_7_dashboards_linking_to_cmdb_proposals():
    # Kibana proposal extraction
    kibana_data = json.loads(KIBANA_FIXTURE.read_text(encoding="utf-8"))
    k_obj = kibana_data["saved_objects"][0]
    k_proposals = KibanaConnector.extract_service_proposals(k_obj)
    assert any(p["proposed_target"] == "cmdb:service:payments-api-service" for p in k_proposals)
    assert all(p["status"] == "PROPOSED" for p in k_proposals)

    # Grafana proposal extraction
    grafana_data = json.loads(GRAFANA_FIXTURE.read_text(encoding="utf-8"))
    g_dash = grafana_data["dashboards"][0]
    g_proposals = GrafanaConnector.extract_service_proposals(g_dash)
    assert any("payments-api-service" in p["proposed_target"] for p in g_proposals)
    assert all(p["relationship"] == "tracksService" for p in g_proposals)


# ===========================================================================
# CRA-008.8: Secret and PII redaction receipts
# ===========================================================================

def test_cra_008_8_secret_and_pii_redaction_receipts():
    raw_query = (
        "search index=logs "
        "user_email=bob.smith@company.org "
        "api_key='ak_prod_998877665544332211' "
        "db_url='mongodb://user:superpass123@mongo.internal:27017/analytics' "
        "token='bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xyz' "
        "password=\"MyComplexP@ssw0rd!\""
    )
    cleaned, receipt = redact_with_receipt(raw_query, target_id="savedsearch:audit_query")

    # Removed values must NEVER appear in the receipt
    receipt_json = json.dumps(receipt.__dict__)
    assert "bob.smith@company.org" not in receipt_json
    assert "ak_prod_998877665544332211" not in receipt_json
    assert "superpass123" not in receipt_json
    assert "MyComplexP@ssw0rd!" not in receipt_json

    # Counts must accurately reflect sanitized tokens
    assert receipt.redaction_counts["email"] == 1
    assert receipt.redaction_counts["api_key"] == 1
    assert receipt.redaction_counts["connection_string"] == 1
    assert receipt.redaction_counts["token"] == 1
    assert receipt.redaction_counts["password"] == 1
    assert receipt.total_redacted >= 5

    # Target text is scrubbed
    assert "[REDACTED_EMAIL]" in cleaned
    assert "[REDACTED_API_KEY]" in cleaned
    assert "[REDACTED_CONNECTION_STRING]" in cleaned
    assert "[REDACTED_TOKEN]" in cleaned
    assert "[REDACTED_PASSWORD]" in cleaned


# ===========================================================================
# CRA-008.9: CMDB dependency structure as directed graph with cycle detection
# ===========================================================================

def test_cra_008_9_cmdb_dependency_cycle_detection():
    data = json.loads(SNOW_FIXTURE.read_text(encoding="utf-8"))
    relationships = data["ci_relationships"]

    # Graph contains ci-101 -> ci-102 -> ci-103 -> ci-101
    findings = ServiceNowConnector.detect_cmdb_cycles(relationships)
    assert len(findings) >= 1
    finding = findings[0]
    assert finding["type"] == "CMDB_DEPENDENCY_CYCLE"
    assert finding["severity"] == "HIGH"
    assert "ci-101" in finding["cycle_path"]
    assert "ci-102" in finding["cycle_path"]
    assert "ci-103" in finding["cycle_path"]
    # Edges are NOT dropped; original relationship count is preserved
    assert len(relationships) == 3


# ===========================================================================
# CRA-008.A: Evidence journey and secrets fixture sweep
# ===========================================================================

def test_cra_008_a_evidence_journey_and_secrets_fixture_sweep():
    # 1. Evidence journey: Incident -> Service -> Deployment -> Dashboard / Log
    snow_data = json.loads(SNOW_FIXTURE.read_text(encoding="utf-8"))
    grafana_data = json.loads(GRAFANA_FIXTURE.read_text(encoding="utf-8"))
    kibana_data = json.loads(KIBANA_FIXTURE.read_text(encoding="utf-8"))
    splunk_data = json.loads(SPLUNK_FIXTURE.read_text(encoding="utf-8"))

    inc = snow_data["incidents"][0]
    chg = snow_data["change_requests"][0]
    ci = snow_data["configuration_items"][0]

    # Linking assertions along the journey
    assert inc["cmdb_ci"] == ci["sys_id"]
    assert chg["cmdb_ci"] == ci["sys_id"]

    # Dashboards reference the service
    dash = grafana_data["dashboards"][0]
    g_props = GrafanaConnector.extract_service_proposals(dash)
    assert any(ci["name"] in p["proposed_target"] for p in g_props)

    k_obj = kibana_data["saved_objects"][0]
    k_props = KibanaConnector.extract_service_proposals(k_obj)
    assert any(ci["name"] in p["proposed_target"] for p in k_props)

    # 2. Universal Connection Factory validation
    factory = ConnectorFactory()
    splunk_conn = factory.create("splunk", "https://splunk.corp:8089", token="sp-tok")
    assert isinstance(splunk_conn, SplunkConnector)

    grafana_conn = factory.create("grafana", "https://grafana.corp:3000", token="gr-tok")
    assert isinstance(grafana_conn, GrafanaConnector)

    kibana_conn = factory.create("kibana", "https://kibana.corp:5601", token="kb-tok")
    assert isinstance(kibana_conn, KibanaConnector)

    # 3. CML compilation sweep
    cml_files = [
        "packages/eoip/mapping/cml/servicenow.cml",
        "packages/eoip/mapping/cml/splunk.cml",
        "packages/eoip/mapping/cml/kibana.cml",
        "packages/eoip/mapping/cml/grafana.cml",
    ]
    for cml_path in cml_files:
        content = Path(cml_path).read_text(encoding="utf-8")
        mapping = parse_and_compile_cml(content)
        assert mapping.mapping_id.startswith("cml_")
        assert mapping.source_type in ("servicenow", "splunk", "kibana", "grafana")

    # 4. Secrets fixture sweep: confirm connector outputs never leak plaintext passwords/tokens
    raw_grafana_ds = grafana_data["datasources"][0]
    clean_ds = grafana_conn.scrub_datasource_secrets(raw_ds := raw_grafana_ds)
    clean_json_str = json.dumps(clean_ds)
    assert "super_secret_auth_password_do_not_leak" not in clean_json_str
    assert "another_db_secret_password" not in clean_json_str
    assert "Bearer topSecretBearerToken12345" not in clean_json_str

    raw_splunk_search = splunk_data["saved_searches"][0]["search"]
    clean_search, receipt = redact_with_receipt(raw_splunk_search, "splunk_fixture")
    assert "ghp_ABC123456789012345678" not in clean_search
    assert receipt.total_redacted >= 1
