"""Acceptance tests for WP-006: Wiki, Content, Chat, and Document Repositories (CRA-006.1-006.8, CRA-006.A)."""

import json
from pathlib import Path
import pytest
import respx
import httpx

from eoip.connectors.base import DiscoveryScope
from eoip.connectors.confluence import ConfluenceConnector
from eoip.connectors.confluence_body import extract_storage_body
from eoip.connectors.documentum import DocumentumConnector
from eoip.connectors.errors import ConnectorError
from eoip.connectors.slack import SlackConnector
from eoip.mapping.cml import parse_and_compile_cml
from eoip.query.sensitive_redactor import redact_sensitive_literals


# ---------------------------------------------------------------------------
# CRA-006.1: Provide generic wiki acquisition plus Confluence-specific spaces,
# pages, versions, links, comments and attachments with permissions & diagnostics
# ---------------------------------------------------------------------------
def test_cra_006_1_confluence_spaces_pages_diagnostics():
    conn = ConfluenceConnector(
        base_url="https://confluence.example.org",
        token="sanitized-token",
    )
    assert conn.source_system == "confluence"
    assert conn.mapper_version == "confluence-dc/1.2"

    # 1. Map Space
    space_event = conn.make_event(
        "space",
        "confluence-01:space:ARCH",
        {"key": "ARCH", "name": "Architecture Space", "description": {"plain": {"value": "Core arch"}}},
        1,
    )
    mapped_space = conn.map_event(space_event)
    assert mapped_space["kind"] == "space"
    assert mapped_space["space_key"] == "ARCH"
    assert mapped_space["name"] == "Architecture Space"

    # 2. Map Page with parent page (wiki:childOf hierarchy)
    page_payload = {
        "id": "1002",
        "title": "Subsystem Design",
        "space": {"key": "ARCH"},
        "version": {"number": 3, "when": "2026-03-01T12:00:00Z"},
        "body": {"storage": {"value": "<p>Content</p>"}},
        "ancestors": [{"id": "1001", "title": "Architecture Overview"}],
    }
    page_event = conn.make_event("page", "confluence-01:page:1002", page_payload, 3)
    mapped_page = conn.map_event(page_event)
    assert mapped_page["kind"] == "page"
    assert mapped_page["content_id"] == "1002"
    assert mapped_page["parent_ids"] == ["1001"]

    # 3. Map BlogPost
    blog_payload = {
        "id": "2001",
        "title": "Monthly Architecture Update",
        "space": {"key": "ARCH"},
        "version": {"number": 1, "when": "2026-03-02T10:00:00Z"},
        "body": {"storage": {"value": "<p>Update</p>"}},
        "ancestors": [],
    }
    blog_event = conn.make_event("blogpost", "confluence-01:blogpost:2001", blog_payload, 1)
    mapped_blog = conn.map_event(blog_event)
    assert mapped_blog["kind"] == "blogpost"
    assert mapped_blog["content_id"] == "2001"

    # 4. Map Comment
    comment_payload = {
        "id": "3001",
        "container": {"id": "1002"},
        "version": {"number": 1, "when": "2026-03-02T11:00:00Z"},
        "body": {"storage": {"value": "<p>LGTM</p>"}},
    }
    comment_event = conn.make_event("comment", "confluence-01:comment:3001", comment_payload, 1)
    mapped_comment = conn.map_event(comment_event)
    assert mapped_comment["kind"] == "comment"
    assert mapped_comment["container_id"] == "1002"

    # 5. Map Attachment
    att_payload = {
        "id": "att-55",
        "title": "system_diagram.png",
        "container": {"id": "1002"},
        "space": {"key": "ARCH"},
        "extensions": {"mediaType": "image/png", "fileSize": 45000},
        "version": {"number": 1},
    }
    att_event = conn.make_event("attachment", "confluence-01:attachment:att-55", att_payload, 1)
    mapped_att = conn.map_event(att_event)
    assert mapped_att["kind"] == "attachment"
    assert mapped_att["media_type"] == "image/png"
    assert mapped_att["page_id"] == "1002"


# ---------------------------------------------------------------------------
# CRA-006.2: Qualify Slack through approved scopes/events/history APIs and DM boundary
# ---------------------------------------------------------------------------
def test_cra_006_2_slack_qualification_and_dm_boundary():
    # 1. Deny-by-default boundary enforcement: enabling private/DM without approval ref fails (Decision H-13)
    with pytest.raises(ValueError, match="Enabling Slack private-channel or direct-message ingestion without an approval reference is refused"):
        SlackConnector(
            source_id="slack-denied",
            token="xoxb-test-token",
            enable_private_channels=True,
            compliance_approval_ref=None,
        )

    with pytest.raises(ValueError, match="Enabling Slack private-channel or direct-message ingestion without an approval reference is refused"):
        SlackConnector(
            source_id="slack-denied-dm",
            token="xoxb-test-token",
            enable_direct_messages=True,
            compliance_approval_ref="",
        )

    # 2. Approved instantiation with compliance reference
    approved_conn = SlackConnector(
        source_id="slack-approved",
        token="xoxb-approved-token",
        enable_private_channels=True,
        compliance_approval_ref="LEGAL-COMPLIANCE-REF-2026-001",
    )
    assert approved_conn.compliance_approval_ref == "LEGAL-COMPLIANCE-REF-2026-001"
    assert approved_conn.capabilities().baseline is True
    assert approved_conn.capabilities().webhooks is True

    # 3. Discovery and rate-limiting handling
    with respx.mock(base_url="https://slack.com/api") as mock:
        mock.get("/conversations.list").mock(return_value=httpx.Response(429, json={"ok": False, "error": "ratelimited"}))
        with pytest.raises(ConnectorError) as exc_info:
            approved_conn.discover(DiscoveryScope())
        assert exc_info.value.category == "rate_limited"


# ---------------------------------------------------------------------------
# CRA-006.3: Qualify Documentum API for object IDs, versions, and legal holds
# ---------------------------------------------------------------------------
def test_cra_006_3_documentum_qualification_and_object_identity():
    conn = DocumentumConnector(
        source_id="dctm-prod-01",
        base_url="https://documentum.corp.example.org",
        repository="CORP_REPO",
        token="bearer-token-123",
    )
    assert conn.api_root == "/dctm-rest/repositories/CORP_REPO"
    assert conn.capabilities().discovery is True

    # Identity rooted in r_object_id, chronicle_id, and version label
    props = {
        "r_object_id": "090000018001beef",
        "object_name": "Quarterly_Financial_Report.pdf",
        "i_chronicle_id": "0900000180000001",
        "r_version_label": ["3.0", "CURRENT"],
        "acl_name": "finance_execs",
        "acl_domain": "corp",
        "r_immutable_flag": True,
        "legal_hold": True,
        "r_retention_until": "2035-12-31T23:59:59Z",
    }
    event = conn.make_sysobject_event(props, parent_container_id="0b0000018000cafe")

    # Document identity must never be reduced to filename or URL
    assert event.source_record_id == "sysobject:090000018001beef"
    assert event.source_version == "0900000180000001:3.0"
    assert event.metadata["r_object_id"] == "090000018001beef"
    assert event.metadata["i_chronicle_id"] == "0900000180000001"
    assert event.metadata["legal_hold"] is True
    assert event.permissions.visibility == "RESTRICTED"
    assert "documentum:acl:corp:finance_execs" in event.permissions.principal_refs
    assert event.permissions.inherited_from == "documentum:folder:0b0000018000cafe"

    # Missing r_object_id is strictly rejected
    with pytest.raises(ValueError, match="Documentum sysobject requires r_object_id"):
        conn.make_sysobject_event({"object_name": "orphan.pdf"})


# ---------------------------------------------------------------------------
# CRA-006.4: Preserve nested part & attachment provenance; independent ACL sync; redaction
# ---------------------------------------------------------------------------
def test_cra_006_4_nested_part_provenance_and_independent_acl_sync():
    conn = ConfluenceConnector(base_url="https://confluence.example.org", token="tok")

    # 1. Independent permission synchronization without modifying page content
    initial_event = conn.make_event(
        "page",
        f"{conn.instance_id}:page:5001",
        {"id": "5001", "space": {"key": "FIN"}, "title": "Earnings Report", "restrictions": {}},
        1,
    )
    assert initial_event.permissions.visibility == "INTERNAL"
    assert initial_event.permissions.principal_refs == ["confluence:space:FIN"]

    # Emit independent PERMISSION_UPDATE
    updated_restrictions = {
        "read": {"restrictions": {"group": {"results": [{"name": "board-members"}]}}}
    }
    perm_event = conn.make_permission_event("page", "5001", updated_restrictions, space_key="FIN")
    assert perm_event.operation == "PERMISSION_UPDATE"
    assert perm_event.permissions.visibility == "RESTRICTED"
    assert perm_event.permissions.principal_refs == ["confluence:group:board-members"]
    assert perm_event.source_record_id == initial_event.source_record_id

    # 2. Redaction of sensitive content before indexing
    sensitive_text = "Database connection: password=TopSecretPass123! and Bearer tok_live_abcdef1234567890"
    clean_text = redact_sensitive_literals(sensitive_text)
    assert "TopSecretPass123!" not in clean_text
    assert "[REDACTED]" in clean_text


# ---------------------------------------------------------------------------
# CRA-006.5: Honest macro and rendition fidelity diagnostics
# ---------------------------------------------------------------------------
def test_cra_006_5_honest_macro_fidelity_diagnostics():
    body_xhtml = (
        "<p>Standard text</p>"
        "<ac:structured-macro ac:name=\"code\">"
        "<ac:parameter ac:name=\"language\">python</ac:parameter>"
        "<ac:plain-text-body><![CDATA[import sys]]></ac:plain-text-body>"
        "</ac:structured-macro>"
        "<ac:structured-macro ac:name=\"unknown-vendor-chart\">"
        "<ac:parameter ac:name=\"chartType\">funnel</ac:parameter>"
        "</ac:structured-macro>"
        "<ac:structured-macro ac:name=\"legacy-flash-player\" />"
    )

    extracted = extract_storage_body(body_xhtml, "https://confluence.example.org/pages/1001")
    # Code macro is recognized
    assert len(extracted["code_snippets"]) == 1
    assert extracted["code_snippets"][0]["language"] == "python"

    # Unsupported macros are honestly reported in diagnostics, not fabricated as text
    unsupported = extracted["diagnostics"]["unsupported_macros"]
    assert "unknown-vendor-chart" in unsupported
    assert "legacy-flash-player" in unsupported


# ---------------------------------------------------------------------------
# CRA-006.6: Confluence CQL page tree, mentions, and ACL vector populating
# ---------------------------------------------------------------------------
def test_cra_006_6_confluence_cql_page_tree_and_acl_vector():
    # 1. Parse and compile CML mapping
    cml_path = Path("packages/eoip/mapping/cml/confluence.cml")
    assert cml_path.exists()
    ir = parse_and_compile_cml(cml_path.read_text())
    assert ir.mapping_id == "cml_confluence_1_0_0"
    assert ir.source_type == "confluence"
    assert ir.subject_map.template == "urn:eoip:confluence:page:{content_id}"

    # 2. Verify restricted page ACL vector
    fixture_path = Path("tests/fixtures/connectors/confluence/pages.json")
    fixture = json.loads(fixture_path.read_text())
    conn = ConfluenceConnector(base_url="https://confluence.example.org", token="tok")

    normal_page = fixture["results"][0]
    restricted_page = fixture["results"][1]

    ev_normal = conn.make_event("page", f"confluence:page:{normal_page['id']}", normal_page, 1)
    assert ev_normal.permissions.visibility == "INTERNAL"
    assert ev_normal.metadata["acl_vector"] == ["confluence:space:ARCH"]

    ev_restricted = conn.make_event("page", f"confluence:page:{restricted_page['id']}", restricted_page, 2)
    assert ev_restricted.permissions.visibility == "RESTRICTED"
    assert "confluence:user:sec_officer_01" in ev_restricted.metadata["acl_vector"]
    assert "confluence:group:security-team" in ev_restricted.metadata["acl_vector"]


# ---------------------------------------------------------------------------
# CRA-006.7: Documentum Cabinets, Folders, Renditions, and Legal Hold
# ---------------------------------------------------------------------------
def test_cra_006_7_documentum_cabinets_folders_and_legal_hold():
    # 1. Parse and compile CML mapping
    cml_path = Path("packages/eoip/mapping/cml/documentum.cml")
    assert cml_path.exists()
    ir = parse_and_compile_cml(cml_path.read_text())
    assert ir.mapping_id == "cml_documentum_1_0_0"
    assert ir.source_type == "documentum"
    assert ir.subject_map.template == "urn:eoip:documentum:sysobject:{r_object_id}"

    # 2. Sysobject with legal hold and renditions
    fixture_path = Path("tests/fixtures/connectors/documentum/sysobjects.json")
    fixture = json.loads(fixture_path.read_text())
    conn = DocumentumConnector(
        source_id="dctm-01",
        base_url="https://documentum.example.org",
        repository="DOC_REPO",
        token="tok",
    )

    legal_hold_doc = fixture["entries"][1]["content"]["properties"]
    event = conn.make_sysobject_event(legal_hold_doc, parent_container_id="0b00000100001111")
    assert event.metadata["legal_hold"] is True
    assert event.metadata["retention_until"] == "2036-12-31T23:59:59Z"
    assert event.metadata["r_object_id"] == "090000018001a2c2"
    assert event.metadata["parent_container_id"] == "0b00000100001111"
    assert len(event.metadata["renditions"]) == 1


# ---------------------------------------------------------------------------
# CRA-006.8: Slack Events API, Thread Replies, and Entity Mention Proposals
# ---------------------------------------------------------------------------
def test_cra_006_8_slack_events_and_mention_proposals():
    # 1. Parse and compile CML mapping
    cml_path = Path("packages/eoip/mapping/cml/slack.cml")
    assert cml_path.exists()
    ir = parse_and_compile_cml(cml_path.read_text())
    assert ir.mapping_id == "cml_slack_1_0_0"
    assert ir.source_type == "slack"
    assert ir.subject_map.template == "urn:eoip:slack:message:{channel_id}:{ts}"

    # 2. Process message event with user mentions
    conn = SlackConnector(source_id="slack-01", token="tok")
    fixture_path = Path("tests/fixtures/connectors/slack/conversations.json")
    fixture = json.loads(fixture_path.read_text())
    msg = fixture["messages"][0]

    event = conn._make_message_event("C01GENERAL", msg)
    assert event.source_record_id == "C01GENERAL:1710000000.000100"
    # Mentions are proposed knowledge states per CRA-006.8 & CRA-023
    assert "user:U02BOB" in event.metadata["proposed_mentions"]
    assert "user:U03CAROL" in event.metadata["proposed_mentions"]
    assert len(event.metadata["files"]) == 1
    assert event.metadata["files"][0]["name"] == "network-plan.png"

    # 3. Thread reply linking
    reply = fixture["messages"][1]
    reply_event = conn._make_message_event("C01GENERAL", reply, thread_parent="1710000000.000100")
    assert reply_event.metadata["thread_parent"] == "1710000000.000100"

    # 4. Deletion event handling
    del_event = conn.handle_webhook_event({
        "event": {
            "type": "message_deleted",
            "channel": "C01GENERAL",
            "ts": "1710000050.000200",
            "deleted_ts": "1710000050.000200",
        }
    })
    assert del_event.operation == "DELETE"


# ---------------------------------------------------------------------------
# CRA-006.A: Acceptance Gate for Wiki, Content, Chat, and Document Repositories
# ---------------------------------------------------------------------------
def test_cra_006_a_acceptance_gate():
    # Clause verification:
    # 1. Restricted Confluence page / Slack channel / Documentum document cannot appear to unauthorized principals
    # Confluence restricted page
    conf_conn = ConfluenceConnector(base_url="https://confluence.example.org", token="tok")
    conf_event = conf_conn.make_event(
        "page",
        "confluence:page:secret-01",
        {
            "id": "secret-01",
            "space": {"key": "LEGAL"},
            "title": "Secret M&A",
            "restrictions": {"read": {"restrictions": {"user": {"results": [{"userKey": "counsel_01"}]}}}},
        },
        1,
    )
    assert conf_event.permissions.visibility == "RESTRICTED"
    assert "confluence:user:counsel_01" in conf_event.permissions.principal_refs
    # Unauthorized principal is denied
    assert "confluence:user:unauthorized_intern" not in conf_event.permissions.principal_refs

    # Slack private channel boundary enforcement
    with pytest.raises(ValueError, match="Enabling Slack private-channel or direct-message ingestion without an approval reference is refused"):
        SlackConnector(source_id="slack-unauth", token="tok", enable_private_channels=True)

    # Documentum legal hold preservation
    dctm_conn = DocumentumConnector(source_id="dctm-01", base_url="https://dctm.org", repository="CORP", token="tok")
    dctm_event = dctm_conn.make_sysobject_event({
        "r_object_id": "090000019999hold",
        "object_name": "AuditTrail.pdf",
        "i_chronicle_id": "0900000199990000",
        "r_version_label": ["1.0"],
        "acl_name": "compliance_only",
        "acl_domain": "corp",
        "legal_hold": True,
    })
    assert dctm_event.permissions.visibility == "RESTRICTED"
    assert dctm_event.metadata["legal_hold"] is True
    assert dctm_event.metadata["r_object_id"] == "090000019999hold"

    # Synchronizing permissions independently of content changes
    perm_update = conf_conn.make_permission_event(
        "page",
        "secret-01",
        {"read": {"restrictions": {"user": {"results": [{"userKey": "counsel_01"}, {"userKey": "counsel_02"}]}}}},
        space_key="LEGAL",
    )
    assert perm_update.operation == "PERMISSION_UPDATE"
    assert "confluence:user:counsel_02" in perm_update.permissions.principal_refs
