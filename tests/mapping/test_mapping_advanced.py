"""Advanced tests for CRA-017.2, CRA-017.3, CRA-017.4, CRA-017.5, CRA-017.10, CRA-017.11, CRA-017.A.

Covers:
1. R2RML/RML adapter, construct validation, and lossy coercion blocking (CRA-017.2, CRA-017.3, CRA-017.7).
2. Virtual mapping vs Materialized ingestion, transaction freshness, and OBDA SQL pushdown < 50ms (CRA-017.4, CRA-017.11).
3. Dry-run sample preview, field diagnostics, schema drift detection (CRA-017.5).
4. AI-suggested mappings proposal with confidence and non-auto-activation (CRA-017.10).
5. Parity across Jira, Confluence, and ServiceNow CML mappings (CRA-017.A).
"""

import time
import pytest

from eoip.mapping.cml import parse_and_compile_cml, safe_apply_template
from eoip.mapping.diagnostics import (
    detect_schema_drift,
    propose_cml_mapping,
    run_dry_run_preview,
)
from eoip.mapping.executor import execute_mapping
from eoip.mapping.r2rml import R2RMLAdapter
from eoip.mapping.virtualization import (
    FreshnessModel,
    MappingExecutionMode,
    OBDAPushdownEngine,
    VirtualContext,
)

# Complete Confluence and ServiceNow CML manifests for parity validation (CRA-017.A)
CONFLUENCE_CML = """
source: confluence
version: 1.0.0
id: cml_confluence_page_v1
governance:
  classification: INTERNAL
  pii_fields:
    - author_email

subject_map:
  template: "eoip:entity/Page/{iri_safe(page_id)}"
  class: "eoip:class/Page"

property_maps:
  - path: title
    predicate: "http://purl.org/dc/terms/title"
    datatype: "http://www.w3.org/2001/XMLSchema#string"
    required: true
  - path: author_email
    predicate: "eoip:property/authorEmail"
    datatype: "http://www.w3.org/2001/XMLSchema#string"
    pii: true
  - path: space_key
    predicate: "eoip:property/spaceKey"
    datatype: "http://www.w3.org/2001/XMLSchema#string"

relation_maps:
  - path: parent_id
    predicate: "eoip:relation/childOfPage"
    object_template: "eoip:entity/Page/{parent_id}"
    object_class: "eoip:class/Page"
    properties:
      weight: sort_order

provenance:
  emit: true
  agent: "urn:eoip:agent:confluence_connector"
"""

SERVICENOW_CML = """
source: servicenow
version: 1.0.0
id: cml_servicenow_incident_v1
governance:
  classification: RESTRICTED
  pii_fields:
    - caller_id
    - caller_phone

subject_map:
  template: "eoip:entity/Incident/{iri_safe(sys_id)}"
  class: "eoip:class/Incident"

property_maps:
  - path: number
    predicate: "eoip:property/ticketNumber"
    datatype: "http://www.w3.org/2001/XMLSchema#string"
    required: true
  - path: short_description
    predicate: "http://purl.org/dc/terms/title"
    datatype: "http://www.w3.org/2001/XMLSchema#string"
  - path: caller_id
    predicate: "eoip:property/callerId"
    datatype: "http://www.w3.org/2001/XMLSchema#string"
    pii: true
  - path: priority
    predicate: "eoip:property/priority"
    datatype: "http://www.w3.org/2001/XMLSchema#integer"

relation_maps:
  - path: cmdb_ci
    predicate: "eoip:relation/affectsCI"
    object_template: "eoip:entity/ConfigurationItem/{cmdb_ci}"
    object_class: "eoip:class/ConfigurationItem"

provenance:
  emit: true
  agent: "urn:eoip:agent:servicenow_connector"
"""


def test_r2rml_adapter_and_loss_reporting():
    """CRA-017.2, CRA-017.3, CRA-017.7: R2RML translation and lossy coercion blocking."""
    adapter = R2RMLAdapter()

    # Valid R2RML definition
    valid_def = {
        "id": "triples_map_tickets",
        "version": "1.0.0",
        "source_type": "postgresql",
        "logicalTable": {"tableName": "support_tickets"},
        "subjectMap": {
            "template": "eoip:entity/Ticket/{ticket_id}",
            "class": "eoip:class/Ticket",
        },
        "predicateObjectMaps": [
            {
                "predicate": "http://purl.org/dc/terms/title",
                "objectMap": {"column": "title", "datatype": "http://www.w3.org/2001/XMLSchema#string"},
                "required": True,
            },
            {
                "predicate": "eoip:relation/assignedToAgent",
                "parentTriplesMap": "triples_map_agents",
                "joinCondition": {"child": "agent_id", "parent": "id"},
                "objectMap": {"template": "eoip:entity/Agent/{agent_id}", "class": "eoip:class/Agent"},
            },
        ],
    }

    ir, loss_report = adapter.import_r2rml_dict(valid_def)
    assert ir.mapping_id == "triples_map_tickets"
    assert ir.subject_map.target_class_iri == "eoip:class/Ticket"
    assert len(ir.property_maps) == 1
    assert len(ir.relation_maps) == 1
    assert loss_report.is_lossless is True

    # Defect/Lossy R2RML definition with unsupported procedural SQL and missing datatype
    lossy_def = {
        "id": "lossy_map",
        "logicalTable": {"sqlQuery": "EXEC GetTicketsWithCursor"},
        "subjectMap": {"template": "eoip:entity/Ticket/{id}", "termType": "BlankNode"},
        "predicateObjectMaps": [
            {
                "predicate": "eoip:property/raw_field",
                "objectMap": {"column": "raw_field", "function": "unapproved_crypto_hash"},
            }
        ],
    }

    _, defect_report = adapter.import_r2rml_dict(lossy_def)
    assert defect_report.is_lossless is False
    assert len(defect_report.unsupported_constructs) >= 2  # procedural SQL + unapproved function
    assert len(defect_report.lossy_coercions) >= 1  # BlankNode subject


def test_virtual_mapping_separation_and_obda_sql_pushdown():
    """CRA-017.4, CRA-017.11: Virtual vs Materialized mapping and OBDA point query latency < 50ms."""
    cml_ir = parse_and_compile_cml(CONFLUENCE_CML)
    ctx = VirtualContext(
        mode=MappingExecutionMode.VIRTUAL,
        freshness=FreshnessModel.SNAPSHOT_ISOLATION,
        source_table="confluence_pages",
        rows_copied=0,
    )

    engine = OBDAPushdownEngine(cml_ir, ctx)
    sql = engine.rewrite_point_query(
        entity_id="PAGE-9021",
        requested_predicates=["http://purl.org/dc/terms/title", "eoip:property/spaceKey"],
    )

    assert "SELECT title, space_key FROM confluence_pages" in sql
    assert "WHERE id = 'PAGE-9021' LIMIT 1;" in sql

    # Mock database point lookup test measuring pushdown speed
    mock_db = {"PAGE-9021": {"title": "Architecture Overview", "space_key": "ENG"}}
    res = engine.execute_point_query_mock("PAGE-9021", mock_db)

    assert res["mode"] == "VIRTUAL"
    assert res["rows_copied"] == 0
    assert res["record"]["title"] == "Architecture Overview"
    assert res["latency_ms"] < 50.0  # OBDA benchmark threshold < 50ms


def test_dry_run_preview_field_diagnostics_and_schema_drift():
    """CRA-017.5: Dry-run preview, field null rates, missing required fields, and schema drift."""
    ir = parse_and_compile_cml(SERVICENOW_CML)

    records = [
        {"sys_id": "inc01", "number": "INC0001", "short_description": "VPN issue", "priority": 1, "caller_id": "usr1"},
        {"sys_id": "inc02", "number": "INC0002", "short_description": None, "priority": 2, "caller_id": "usr2"},
        {"sys_id": "inc03", "number": "INC0003", "short_description": "Password reset", "priority": 3, "caller_id": "usr3"},
    ]

    dry_run = run_dry_run_preview(ir, records, tenant_id="tenant_sn")
    assert dry_run.total_records == 3
    assert dry_run.triples_generated > 0
    assert len(dry_run.validation_errors) == 0

    # Field diagnostics: short_description had 1 null out of 3 (null rate 33.3%)
    sd_diag = dry_run.field_diagnostics["short_description"]
    assert sd_diag.total_seen == 3
    assert sd_diag.null_count == 1
    assert abs(sd_diag.null_rate - (1.0 / 3.0)) < 0.01

    # Missing required field error
    invalid_records = [{"sys_id": "inc04", "short_description": "No number"}]
    dry_run_invalid = run_dry_run_preview(ir, invalid_records, tenant_id="tenant_sn")
    assert len(dry_run_invalid.validation_errors) == 1
    assert "Missing required field 'number'" in dry_run_invalid.validation_errors[0]

    # Schema drift detection: incoming record has unexpected 'new_vendor_field'
    incoming_drifted = [
        {"sys_id": "inc05", "number": "INC0005", "new_vendor_field": "AzureAD", "another_unknown": 123}
    ]
    drift_report = detect_schema_drift(ir, incoming_drifted)
    assert drift_report.is_drifted is True
    assert "new_vendor_field" in drift_report.unexpected_new_fields
    assert "another_unknown" in drift_report.unexpected_new_fields


def test_ai_suggested_mappings_proposal():
    """CRA-017.10: AI-suggested CML mapping proposal with confidence scores and non-auto-activation."""
    jira_sample_payloads = [
        {
            "id": "10001",
            "summary": "Fix connection timeout in client",
            "description": "Client drops socket after 15s",
            "created_at": "2026-10-18T04:00:00Z",
            "status": "OPEN",
            "reporter_email": "dev@corp.internal",
            "custom_score": 42,
        }
    ]

    proposal = propose_cml_mapping(
        source_name="jira",
        target_class="eoip:class/Issue",
        id_field="id",
        sample_records=jira_sample_payloads,
    )

    assert proposal.status == "PROPOSED"
    assert proposal.requires_human_approval is True

    # Check high-confidence mappings for standard terms
    predicates = {s.source_field: s.suggested_predicate for s in proposal.suggestions}
    confidences = {s.source_field: s.confidence for s in proposal.suggestions}

    assert predicates["summary"] == "http://purl.org/dc/terms/title"
    assert confidences["summary"] >= 0.90
    assert predicates["description"] == "http://purl.org/dc/terms/description"
    assert predicates["reporter_email"] == "http://xmlns.com/foaf/0.1/mbox"

    # PII flag on email
    email_sugg = [s for s in proposal.suggestions if s.source_field == "reporter_email"][0]
    assert email_sugg.is_pii is True

    # Converts into valid, parseable CML YAML
    cml_text = proposal.to_cml_yaml()
    compiled_ir = parse_and_compile_cml(cml_text)
    assert compiled_ir.source_type == "jira"
    assert "reporter_email" in compiled_ir.pii_fields


def test_cml_parity_and_projection_jira_confluence_servicenow():
    """CRA-017.A: Parity across Jira, Confluence, and ServiceNow mappings."""
    # 1. Confluence test
    conf_ir = parse_and_compile_cml(CONFLUENCE_CML)
    conf_records = [
        {
            "page_id": "PAGE-10",
            "title": "Architecture Specification",
            "author_email": "author@corp.internal",
            "space_key": "ARCH",
            "parent_id": "PAGE-01",
            "sort_order": "5",
        }
    ]
    conf_res = execute_mapping(conf_ir, conf_records, tenant_id="tenant_conf", redact_pii=True)
    assert conf_res["total_records_processed"] == 1
    # PII author_email must be redacted
    preds = [t["predicate"] for t in conf_res["triples"]]
    assert "eoip:property/authorEmail" not in preds
    assert "http://purl.org/dc/terms/title" in preds
    assert "eoip:relation/childOfPage" in preds

    # 2. ServiceNow test
    sn_ir = parse_and_compile_cml(SERVICENOW_CML)
    sn_records = [
        {
            "sys_id": "SN-999",
            "number": "INC999",
            "short_description": "Database High Latency",
            "caller_id": "vip_user",
            "priority": 1,
            "cmdb_ci": "db_server_cluster_01",
        }
    ]
    sn_res = execute_mapping(sn_ir, sn_records, tenant_id="tenant_sn", redact_pii=True)
    assert sn_res["total_records_processed"] == 1
    sn_preds = [t["predicate"] for t in sn_res["triples"]]
    assert "eoip:property/callerId" not in sn_preds
    assert "eoip:property/ticketNumber" in sn_preds
    assert "eoip:relation/affectsCI" in sn_preds


def test_cml_execution_throughput():
    """CRA-017.11: CML execution throughput benchmark test."""
    conf_ir = parse_and_compile_cml(CONFLUENCE_CML)
    batch = [
        {
            "page_id": f"PAGE-{i}",
            "title": f"Doc {i}",
            "author_email": f"user{i}@corp.internal",
            "space_key": "KB",
        }
        for i in range(1000)
    ]

    start = time.perf_counter()
    res = execute_mapping(conf_ir, batch, tenant_id="bench_tenant", redact_pii=False)
    elapsed = time.perf_counter() - start

    rate = len(batch) / elapsed
    assert res["total_records_processed"] == 1000
    assert rate > 5000  # High throughput records/second on CPU
