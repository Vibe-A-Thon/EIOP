"""Tests for Connector Mapping Language (CML), safety parser, and LPG/RDF projection (CRA-017.1 - CRA-017.9, CRA-017.A)."""

import pytest

from eoip.mapping.cml import (
    CMLParseError,
    parse_and_compile_cml,
    safe_apply_template,
)
from eoip.mapping.executor import execute_mapping

# Sample valid Jira CML mapping
JIRA_CML_YAML = """
source: jira
version: 1.0.0
id: cml_jira_issue_v1
governance:
  classification: CONFIDENTIAL
  pii_fields:
    - reporter_email
    - assignee_email

subject_map:
  template: "eoip:entity/Issue/{iri_safe(key)}"
  class: "eoip:class/Issue"

property_maps:
  - path: summary
    predicate: "http://purl.org/dc/terms/title"
    datatype: "http://www.w3.org/2001/XMLSchema#string"
    required: true
  - path: reporter_email
    predicate: "eoip:property/reporterEmail"
    datatype: "http://www.w3.org/2001/XMLSchema#string"
    pii: true
  - path: status
    predicate: "eoip:property/status"
    datatype: "http://www.w3.org/2001/XMLSchema#string"

relation_maps:
  - path: project_key
    predicate: "eoip:relation/belongsToProject"
    object_template: "eoip:entity/Project/{project_key}"
    object_class: "eoip:class/Project"
  - path: parent_key
    predicate: "eoip:relation/subTaskOf"
    object_template: "eoip:entity/Issue/{parent_key}"
    object_class: "eoip:class/Issue"
    properties:
      weight: order_index

provenance:
  emit: true
  confidence: 0.95
  agent: "urn:eoip:agent:jira_connector"
"""


def test_cml_compiles_cleanly_into_ir():
    """CRA-017.6, CRA-017.7: CML YAML compiles into engine-neutral MappingIR."""
    ir = parse_and_compile_cml(JIRA_CML_YAML)
    assert ir.source_type == "jira"
    assert ir.version == "1.0.0"
    assert ir.subject_map.target_class_iri == "eoip:class/Issue"
    assert len(ir.property_maps) == 3
    assert len(ir.relation_maps) == 2
    assert "reporter_email" in ir.pii_fields
    assert ir.provenance.emit_prov_o is True


def test_cml_rejects_code_and_class_injection_attempts():
    """CRA-017.6, CRA-017.A: Templates with __import__ or {0.__class__} rejected at parse time."""
    malicious_templates = [
        "source: bad\nsubject_map:\n  template: '{0.__class__}'\n  class: 'A'",
        "source: bad\nsubject_map:\n  template: '{__import__(\"os\").system(\"id\")}'\n  class: 'A'",
        "source: bad\nsubject_map:\n  template: '{eval(\"1+1\")}'\n  class: 'A'",
    ]

    for bad_yaml in malicious_templates:
        with pytest.raises(CMLParseError):
            parse_and_compile_cml(bad_yaml)


def test_safe_template_functions():
    """CRA-017.6: Whitelisted functions iri_safe, lower, upper, trim."""
    record = {"id": "ISSUE 123/A", "user": "  Alice  "}
    assert safe_apply_template("entity/{iri_safe(id)}", record) == "entity/ISSUE%20123%2FA"
    assert safe_apply_template("user:{lower(trim(user))}", record) == "user:alice"


def test_lpg_and_rdf_projection_and_provenance():
    """CRA-017.8, CRA-017.9: LPG/RDF projection scheme and PROV-O provenance."""
    ir = parse_and_compile_cml(JIRA_CML_YAML)

    sample_record = {
        "id": "1001",
        "key": "PROJ-101",
        "summary": "Implement OAuth2",
        "status": "IN_PROGRESS",
        "reporter_email": "alice@corp.internal",
        "project_key": "PROJ",
        "parent_key": "PROJ-100",
        "order_index": "1",
    }

    res = execute_mapping(
        ir,
        records=[sample_record],
        tenant_id="tenant_alpha",
        run_id="run_42",
        redact_pii=False,
    )

    assert res["total_records_processed"] == 1
    assert len(res["vertices"]) == 1
    assert len(res["edges"]) == 2

    triples = res["triples"]
    predicates = [t["predicate"] for t in triples]

    # Type triple
    assert "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" in predicates
    # Properties
    assert "http://purl.org/dc/terms/title" in predicates
    assert "eoip:property/status" in predicates
    assert "eoip:property/reporterEmail" in predicates

    # Edge without properties (direct triple in tenant graph)
    direct_edge = [t for t in triples if t["predicate"] == "eoip:relation/belongsToProject"][0]
    assert direct_edge["graph"] == "urn:eoip:tenant:tenant_alpha"

    # Edge with properties (named graph per edge assertion CRA-017.8)
    assert any("urn:eoip:assertion:" in t["graph"] for t in triples)

    # PROV-O Triples (CRA-017.9)
    assert "http://www.w3.org/ns/prov#wasDerivedFrom" in predicates
    assert "http://www.w3.org/ns/prov#wasGeneratedBy" in predicates
    assert "http://www.w3.org/ns/prov#wasAttributedTo" in predicates


def test_pii_field_redaction_on_export():
    """CRA-017.A: PII fields declared in CML are removed by export filter."""
    ir = parse_and_compile_cml(JIRA_CML_YAML)

    sample_record = {
        "id": "1002",
        "key": "PROJ-102",
        "summary": "Fix Bug",
        "status": "DONE",
        "reporter_email": "secret_user@corp.internal",
    }

    # Execute with redact_pii=True
    res_redacted = execute_mapping(
        ir,
        records=[sample_record],
        tenant_id="tenant_alpha",
        redact_pii=True,
    )

    predicates = [t["predicate"] for t in res_redacted["triples"]]
    # reporter_email was declared as PII; must be omitted
    assert "eoip:property/reporterEmail" not in predicates
    # Non-PII fields remain
    assert "http://purl.org/dc/terms/title" in predicates
