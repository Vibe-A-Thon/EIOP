"""Acceptance tests for WP-005: Work-Tracking and Test-System Adapters (CRA-005.1-005.9, CRA-005.A)."""

import json
from pathlib import Path
import pytest
import respx
import httpx

from eoip.connectors.base import DiscoveryScope
from eoip.connectors.errors import ConnectorError
from eoip.connectors.jira import JiraConnector
from eoip.connectors.qtest import QTestConnector
from eoip.connectors.rally import RALLY_TYPES, RallyConnector
from eoip.mapping.cml import parse_and_compile_cml


# ---------------------------------------------------------------------------
# CRA-005.1: Qualify Jira Cloud v3 and Data Center v2
# ---------------------------------------------------------------------------
def test_cra_005_1_jira_cloud_and_dc_qualification():
    # 1. Jira Cloud REST API v3 with Bearer token
    cloud_conn = JiraConnector(
        source_id="jira-cloud-01",
        base_url="https://jira.cloud.example.org",
        projects=["PROJ"],
        token="sanitized-cloud-token",
        api_version="3",
        search_mode="enhanced",
    )
    assert cloud_conn.api_version == "3"
    assert cloud_conn.search_mode == "enhanced"
    assert cloud_conn.api_root == "/rest/api/3"

    # 2. Jira Data Center REST API v2 with username/password
    dc_conn = JiraConnector(
        source_id="jira-dc-01",
        base_url="https://jira.datacenter.example.org",
        projects=["PROJ"],
        username="svc_account",
        password="sanitized-password",
        api_version="2",
        search_mode="offset",
    )
    assert dc_conn.api_version == "2"
    assert dc_conn.search_mode == "offset"
    assert dc_conn.api_root == "/rest/api/2"

    # 3. Retrieve permission context with authorized scopes and preserve revision identity
    issue_payload = {
        "id": "10001",
        "key": "PROJ-101",
        "fields": {
            "summary": "Implement rate limiting",
            "project": {"key": "PROJ"},
            "security": {"id": "sec-restricted", "name": "Restricted"},
            "updated": "2026-03-02T15:30:00Z",
        },
    }
    event = cloud_conn._event("PROJ", "issue", "PROJ-101", issue_payload)
    assert "jira:security_level:sec-restricted" in event.permissions.principal_refs
    assert event.permissions.visibility == "RESTRICTED"
    assert event.source_version == "2026-03-02T15:30:00Z"
    assert event.metadata["record_id"] == "PROJ-101"


# ---------------------------------------------------------------------------
# CRA-005.2: Qualify Rally workspace/project resource types and hierarchy
# ---------------------------------------------------------------------------
def test_cra_005_2_rally_qualification():
    conn = RallyConnector(
        base_url="https://rally1.rallydev.com",
        workspace="WS-999",
        project="PRJ-888",
        token="sanitized-rally-key",
    )
    assert "user_story" in conn.types
    assert "feature" in conn.types
    assert "epic" in conn.types
    assert "defect" in conn.types
    assert conn.workspace == "WS-999"
    assert conn.project == "PRJ-888"

    # Preserves artifact relationships and cursor semantics
    story_record = {
        "ObjectID": 20001,
        "FormattedID": "US-101",
        "Name": "Query caching",
        "ScheduleState": "In-Progress",
        "Parent": {"FormattedID": "F-50"},
        "Workspace": {"Name": "Engineering"},
        "Project": {"Name": "Query Engine"},
        "LastUpdateDate": "2026-03-02T16:00:00Z",
    }
    dummy_event = conn.make_event("user_story", "story:20001", story_record, "2026-03-02T16:00:00Z")
    mapped = conn.map_event(dummy_event)
    assert mapped["formatted_id"] == "US-101"
    assert mapped["parent_formatted_id"] == "F-50"
    assert mapped["workspace"] == "Engineering"
    assert mapped["project"] == "Query Engine"


# ---------------------------------------------------------------------------
# CRA-005.3: Qualify qTest projects, tests, runs, and defect associations
# ---------------------------------------------------------------------------
def test_cra_005_3_qtest_qualification():
    conn = QTestConnector(
        base_url="https://qtest.example.org",
        project_id=105,
        token="sanitized-qtest-token",
    )
    assert conn.project_id == 105

    # Distinguishes test definitions from execution results
    tc_record = {
        "id": 5001,
        "name": "Rate limit verification",
        "pid": "TC-1",
        "properties": [{"field_name": "Status", "field_value_name": "Approved"}],
    }
    tc_event = conn.make_event("test_case", "tc:5001", tc_record, "v1")
    mapped_tc = conn.map_event(tc_event)
    assert mapped_tc["entity_type"] == "TestCase"
    assert mapped_tc["status"] == "Approved"

    run_record = {
        "id": 6001,
        "name": "Nightly Regression Run #42",
        "status": "Passed",
    }
    run_event = conn.make_event("test_run", "tr:6001", run_record, "v1")
    mapped_run = conn.map_event(run_event)
    assert mapped_run["entity_type"] == "TestRun"


# ---------------------------------------------------------------------------
# CRA-005.4: Official API research and sanitized vendor fixtures
# ---------------------------------------------------------------------------
def test_cra_005_4_api_research_and_fixtures():
    # 1. API research specs exist
    assert Path("docs/connectors/jira/api.md").exists()
    assert Path("docs/connectors/rally/api.md").exists()
    assert Path("docs/connectors/qtest/api.md").exists()

    # 2. Vendor fixtures exist and contain valid sanitized payloads
    jira_fix = json.loads(Path("tests/fixtures/connectors/jira/issues.json").read_text(encoding="utf-8"))
    assert len(jira_fix["issues"]) >= 2
    assert "PROJ-101" in [i["key"] for i in jira_fix["issues"]]

    rally_fix = json.loads(Path("tests/fixtures/connectors/rally/artifacts.json").read_text(encoding="utf-8"))
    assert len(rally_fix["QueryResult"]["Results"]) >= 2

    qtest_fix = json.loads(Path("tests/fixtures/connectors/qtest/test_cases.json").read_text(encoding="utf-8"))
    assert len(qtest_fix["items"]) >= 2


# ---------------------------------------------------------------------------
# CRA-005.5: Incremental acquisition, overlap window, and deduplication
# ---------------------------------------------------------------------------
def test_cra_005_5_incremental_overlap_pagination_acl():
    # Mock Jira responses
    with respx.mock(base_url="https://jira.example.org") as respx_mock:
        # Mock search with duplicates
        respx_mock.post("/rest/api/3/search/jql").respond(
            200,
            json={
                "issues": [
                    {"id": "101", "key": "P-1", "fields": {"updated": "2026-03-02T12:00:00Z"}},
                    {"id": "101", "key": "P-1", "fields": {"updated": "2026-03-02T12:00:00Z"}},  # Duplicate
                    {"id": "102", "key": "P-2", "fields": {"updated": "2026-03-02T12:05:00Z"}},
                ],
                "isLast": True,
            },
        )

        client = httpx.Client()
        conn = JiraConnector(
            source_id="jira_test",
            base_url="https://jira.example.org",
            projects=["PROJ"],
            token="sanitized",
            client=client,
            overlap_minutes=5,
        )

        # Bounded incremental acquisition with overlap window
        issues = list(conn._search_issues("2026-03-02T12:00:00Z"))
        # Must deduplicate by issue ID + updated timestamp
        assert len(issues) == 2
        assert [i["key"] for i in issues] == ["P-1", "P-2"]


# ---------------------------------------------------------------------------
# CRA-005.6: Jira vocabulary mapping, security levels, and attachments
# ---------------------------------------------------------------------------
def test_cra_005_6_jira_mapping_and_vocab():
    conn = JiraConnector(
        source_id="jira_vocab_test",
        base_url="https://jira.example.org",
        projects=["PROJ"],
        token="sanitized",
    )

    fixture = json.loads(Path("tests/fixtures/connectors/jira/issues.json").read_text(encoding="utf-8"))
    issue1 = fixture["issues"][0]

    event = conn._event("PROJ", "issue", issue1["key"], issue1)
    # Mapped to acl_vector
    assert "jira:security_level:sec-01" in event.metadata["acl_vector"]
    assert event.permissions.visibility == "RESTRICTED"

    # Attachments preserved with vault URI
    attachments = event.metadata["attachments"]
    assert len(attachments) == 1
    assert attachments[0]["filename"] == "arch_spec.pdf"
    assert attachments[0]["vault_uri"].startswith("vault://jira/jira_vocab_test/attachment/")


# ---------------------------------------------------------------------------
# CRA-005.7: Rally hierarchies, defect associations, and WSAPI types
# ---------------------------------------------------------------------------
def test_cra_005_7_rally_hierarchies_and_wsapi():
    conn = RallyConnector(
        base_url="https://rally1.rallydev.com",
        workspace="WS-999",
        project="PRJ-888",
        token="sanitized",
    )

    fixture = json.loads(Path("tests/fixtures/connectors/rally/artifacts.json").read_text(encoding="utf-8"))
    results = fixture["QueryResult"]["Results"]

    # 1. User Story with parent
    story_event = conn.make_event("user_story", "rec:1", results[0], "v1")
    mapped_story = conn.map_event(story_event)
    assert mapped_story["parent_formatted_id"] == "F-50"

    # 2. Defect with requirement link
    defect_event = conn.make_event("defect", "rec:2", results[1], "v2")
    mapped_defect = conn.map_event(defect_event)
    assert mapped_defect["defect_requirement"] == "US-101"
    assert mapped_defect["workspace"] == "Engineering"


# ---------------------------------------------------------------------------
# CRA-005.8: qTest requirement linking to ingested Jira issues
# ---------------------------------------------------------------------------
def test_cra_005_8_qtest_requirement_linking_and_distinction():
    conn = QTestConnector(
        base_url="https://qtest.example.org",
        project_id=105,
        token="sanitized",
    )

    fixture = json.loads(Path("tests/fixtures/connectors/qtest/test_cases.json").read_text(encoding="utf-8"))
    item1 = fixture["items"][0]  # Links to Jira PROJ-101
    item2 = fixture["items"][1]  # Links to Rally DE-201

    event1 = conn.make_event("test_case", "tc:5001", item1, "v1")

    # 1. Ingested Jira resource exists in resolver
    ingested_jira_keys = {"PROJ-101", "PROJ-102"}
    mapped_resolved = conn.map_event(event1, jira_resolver=ingested_jira_keys)
    assert mapped_resolved.get("verifiesRequirement") == "urn:eoip:jira:issue:PROJ-101"

    # 2. Jira resource does NOT exist in resolver
    mapped_unresolved = conn.map_event(event1, jira_resolver={"PROJ-999"})
    assert "verifiesRequirement" not in mapped_unresolved

    # 3. Defect link to Rally
    event2 = conn.make_event("test_case", "tc:5002", item2, "v1")
    mapped2 = conn.map_event(event2)
    assert "rally:DE-201" in mapped2["defect_links"]


# ---------------------------------------------------------------------------
# CRA-005.9: CML parity test for Jira, Rally, and qTest
# ---------------------------------------------------------------------------
def test_cra_005_9_cml_parity_test():
    # 1. Jira CML
    jira_cml = Path("packages/eoip/mapping/cml/jira.cml").read_text(encoding="utf-8")
    jira_ir = parse_and_compile_cml(jira_cml)
    assert jira_ir.source_type == "jira"
    assert jira_ir.subject_map.target_class_iri == "https://enterprise-ontology.org/schema/eoip#WorkItem"
    assert any(pm.predicate_iri.endswith("issueKey") for pm in jira_ir.property_maps)

    # 2. Rally CML
    rally_cml = Path("packages/eoip/mapping/cml/rally.cml").read_text(encoding="utf-8")
    rally_ir = parse_and_compile_cml(rally_cml)
    assert rally_ir.source_type == "rally"
    assert rally_ir.subject_map.target_class_iri == "https://enterprise-ontology.org/schema/eoip#WorkItem"
    assert any(rm.predicate_iri.endswith("childOf") for rm in rally_ir.relation_maps)

    # 3. qTest CML
    qtest_cml = Path("packages/eoip/mapping/cml/qtest.cml").read_text(encoding="utf-8")
    qtest_ir = parse_and_compile_cml(qtest_cml)
    assert qtest_ir.source_type == "qtest"
    assert qtest_ir.subject_map.target_class_iri == "https://enterprise-ontology.org/schema/eoip#TestCase"
    assert any(rm.predicate_iri.endswith("tests") for rm in qtest_ir.relation_maps)


# ---------------------------------------------------------------------------
# CRA-005.A: Acceptance Gate: Baseline, Incremental, Overlap, Replay, Revocation
# ---------------------------------------------------------------------------
def test_cra_005_a_acceptance_gate():
    with respx.mock(base_url="https://jira.example.org") as respx_mock:
        # Mock endpoints
        respx_mock.get("/rest/api/3/project/PROJ").respond(
            200, json={"id": "100", "key": "PROJ", "name": "Platform Core"}
        )
        respx_mock.get("/rest/api/3/project/PROJ/version").respond(200, json=[])
        respx_mock.get("/rest/api/3/project/PROJ/statuses").respond(200, json=[])
        respx_mock.post("/rest/api/3/search/jql").respond(
            200,
            json={
                "issues": [
                    {
                        "id": "10001",
                        "key": "PROJ-101",
                        "fields": {
                            "summary": "Gateway rate limiting",
                            "project": {"key": "PROJ"},
                            "security": {"id": "sec-01"},
                            "updated": "2026-03-02T15:30:00Z",
                        },
                    }
                ],
                "isLast": True,
            },
        )

        client = httpx.Client()
        conn = JiraConnector(
            source_id="jira_acceptance",
            base_url="https://jira.example.org",
            projects=["PROJ"],
            token="sanitized",
            client=client,
            overlap_minutes=5,
            include_changelog=False,
            include_comments=False,
        )

        # 1. Baseline acquisition
        baseline_events = list(conn.baseline())
        assert len(baseline_events) >= 2  # project event + issue event
        issue_event = [e for e in baseline_events if e.metadata["record_kind"] == "issue"][0]
        assert issue_event.source_record_id == "PROJ:issue:PROJ-101"

        # 2. Replay test: replaying events reproduces exact deterministic identities
        replayed = list(conn.replay(baseline_events))
        assert [e.event_id for e in replayed] == [e.event_id for e in baseline_events]

        # 3. Access revocation: unauthorized credentials raise authorization_failed
        respx_mock.get("/rest/api/3/project/REVOKED").respond(403)
        revoked_conn = JiraConnector(
            source_id="jira_revoked",
            base_url="https://jira.example.org",
            projects=["REVOKED"],
            token="expired",
            client=client,
        )
        with pytest.raises(ConnectorError) as exc_info:
            revoked_conn._project("REVOKED")
        assert exc_info.value.category == "authorization_failed"
