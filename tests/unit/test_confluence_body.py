import json

import pytest
from eoip.connectors.confluence import ConfluenceConnector
from eoip.connectors.confluence_body import extract_storage_body
from eoip.connectors.sync import SyncBatch
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.jira import FileEventCapture
from eoip.ingestion.replay import logical_graph_output, logical_output_diff
from eoip.ingestion.source_sync import SourceSyncIngestionService

BODY = """<h2 id="deploy">Deploy <strong>safely</strong></h2>
<ac:structured-macro ac:name="anchor"><ac:parameter ac:name="">checks</ac:parameter></ac:structured-macro>
<p>Check&nbsp;<a href="#deploy">deployment</a> and
<a href="https://example.org/check?q=1&amp;x=2">external checks</a>.</p>
<ac:link ac:anchor="overview"><ri:page ri:content-title="Runbook" ri:space-key="OPS"/>
<ac:plain-text-link-body><![CDATA[Operations]]></ac:plain-text-link-body></ac:link>
<ac:link><ri:attachment ri:filename="diagram.png"/></ac:link>
<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">python</ac:parameter>
<ac:plain-text-body><![CDATA[if a < b:\n    print("ready")\n]]></ac:plain-text-body></ac:structured-macro>
<pre><code>echo &lt;ready&gt;</code></pre>
<table><tbody><tr><th>Service</th><th>Status</th></tr>
<tr><td rowspan="2">Payments</td><td>Ready</td></tr></tbody></table>"""


@pytest.mark.req("G2-SRC-CONF-003")
def test_storage_body_extracts_exact_structure():
    result = extract_storage_body(BODY, "https://confluence.example/wiki/pages/42")
    assert result["headings"] == [{"level": 2, "text": "Deploy safely", "anchor": "deploy"}]
    assert result["anchors"] == ["deploy", "checks"]
    assert result["links"] == [
        {"kind": "anchor", "target": "https://confluence.example/wiki/pages/42#deploy",
         "text": "deployment"},
        {"kind": "external", "target": "https://example.org/check?q=1&x=2",
         "text": "external checks"},
        {"kind": "page", "title": "Runbook", "space_key": "OPS", "anchor": "overview",
         "text": "Operations"},
        {"kind": "attachment", "filename": "diagram.png", "text": ""},
    ]
    assert result["code_snippets"] == [
        {"language": "python", "text": 'if a < b:\n    print("ready")\n'},
        {"language": "", "text": "echo <ready>"},
    ]
    assert result["tables"] == [{"rows": [
        [{"text": "Service", "header": True, "rowspan": 1, "colspan": 1},
         {"text": "Status", "header": True, "rowspan": 1, "colspan": 1}],
        [{"text": "Payments", "header": False, "rowspan": 2, "colspan": 1},
         {"text": "Ready", "header": False, "rowspan": 1, "colspan": 1}],
    ]}]


@pytest.mark.req("G2-SRC-CONF-003")
def test_storage_body_preserves_code_entities_and_ignores_active_content():
    result = extract_storage_body(
        '<script><a href="https://bad.example">bad</a></script>'
        '<ac:structured-macro ac:name="code"><ac:plain-text-body>'
        '<![CDATA[&nbsp; <a href="x">literal</a>]]>'
        '</ac:plain-text-body></ac:structured-macro>'
        '<a href="javascript:alert(1)">unsafe</a><a href="/wiki/pages/2">local</a>',
        "https://confluence.example/wiki/pages/1",
    )
    assert result["links"] == [
        {"kind": "internal", "target": "https://confluence.example/wiki/pages/2", "text": "local"}
    ]
    assert result["code_snippets"][0]["text"] == '&nbsp; <a href="x">literal</a>'


@pytest.mark.req("G2-SRC-CONF-003")
@pytest.mark.parametrize("body", [
    "<p>unclosed", "<!DOCTYPE x><p>x</p>", "<p>&unknown;</p>",
    '<table><tr><td colspan="zero">x</td></tr></table>',
])
def test_invalid_storage_body_is_explicitly_rejected(body):
    with pytest.raises(ValueError, match="Confluence"):
        extract_storage_body(body, "https://confluence.example/pages/1")


@pytest.mark.req("G2-SRC-CONF-003")
@pytest.mark.parametrize("body, message", [
    ("x" * 2_000_001, "characters"),
    ("<p/>" * 50_000, "elements"),
    ("<div>" * 130 + "</div>" * 130, "nesting"),
], ids=["body-size", "element-count", "nesting-depth"])
def test_storage_extraction_limits_fail_explicitly(body, message):
    with pytest.raises(ValueError, match=message):
        extract_storage_body(body, "https://confluence.example/pages/1")


@pytest.mark.req("G2-SRC-CONF-003")
def test_xhtml_namespace_empty_body_and_nested_tables():
    assert extract_storage_body("", "https://confluence.example/pages/1")["headings"] == []
    result = extract_storage_body(
        '<div xmlns="http://www.w3.org/1999/xhtml"><h1>Runbook</h1>'
        '<table><tr><td>Outer<table><tr><td>Inner</td></tr></table></td></tr></table></div>',
        "https://confluence.example/pages/1",
    )
    assert result["headings"][0]["text"] == "Runbook"
    assert len(result["tables"]) == 2
    assert [len(table["rows"]) for table in result["tables"]] == [1, 1]


@pytest.mark.req("G2-SRC-CONF-003", "FR-CONF-001")
def test_structure_is_persisted_versioned_and_replayable(tmp_path):
    with ConfluenceConnector("https://confluence.example/wiki", token="fixture") as connector:
        event = connector.make_event("page", f"{connector.instance_id}:page:42", {
            "id": "42", "title": "Deploy", "space": {"key": "ENG"},
            "version": {"number": 1, "when": "2026-10-01T00:00:00Z"},
            "body": {"storage": {"value": BODY}}, "_links": {"webui": "/pages/42"},
        }, 1)
        store = MemoryGraphStore()
        service = SourceSyncIngestionService(
            store, connector, FileEventCapture(tmp_path / "raw"), str(tmp_path / "dlq")
        )
        batch = SyncBatch([event], event.captured_at)
        assert service.ingest(batch)["run_status"] == "SUCCEEDED"
        cid = f"urn:eoip:knowledge:document:{event.source_record_id}"
        page = store.get_vertex_by_canonical_id(cid)
        assert page["properties"]["description"] == BODY
        structure = json.loads(page["properties"]["payload_json"])
        assert structure == extract_storage_body(BODY, page["properties"]["path"])
        revision = store.find_vertices(label="EntityRevision", filters={"subject_id": cid})[0]
        assert json.loads(revision["properties"]["payload_json"])["properties"]["payload_json"] == (
            page["properties"]["payload_json"]
        )
        evidence = store.find_vertices(label="Evidence")[0]
        assert evidence["properties"]["parser_version"] == structure["parser_version"]
        before = logical_graph_output(store)
        assert service.ingest(batch)["run_status"] == "SUCCEEDED"
        assert logical_output_diff(before, logical_graph_output(store))["equivalent"]
        assert json.loads(next((tmp_path / "raw" / "confluence").glob("*.json")).read_text(
            encoding="utf-8"
        ))["payload"]["body"]["storage"]["value"] == BODY


@pytest.mark.req("G2-SRC-CONF-003", "G2-ARCH-007")
def test_body_removal_clears_current_structure_without_destroying_history(tmp_path):
    with ConfluenceConnector("https://confluence.example", token="fixture") as connector:
        payload = {"id": "42", "title": "Deploy", "space": {"key": "ENG"},
                   "version": {"number": 1, "when": "2026-10-01T00:00:00Z"},
                   "body": {"storage": {"value": "<h1>Old heading</h1>"}}}
        original = connector.make_event("page", f"{connector.instance_id}:page:42", payload, 1)
        original = original.model_copy(update={
            "captured_at": "2026-10-01T01:00:00Z", "event_time": "2026-10-01T00:00:00Z",
        })
        changed = connector.make_event("page", original.source_record_id, {
            **payload, "body": {}, "version": {"number": 2, "when": "2026-10-02T00:00:00Z"},
        }, 2).model_copy(update={
            "captured_at": "2026-10-02T01:00:00Z", "event_time": "2026-10-02T00:00:00Z",
        })
        store = MemoryGraphStore()
        service = SourceSyncIngestionService(
            store, connector, FileEventCapture(tmp_path / "raw"), str(tmp_path / "dlq")
        )
        for event in (original, changed):
            assert service.ingest(SyncBatch([event], event.captured_at))["run_status"] == "SUCCEEDED"
        cid = f"urn:eoip:knowledge:document:{original.source_record_id}"
        page = store.get_vertex_by_canonical_id(cid)
        assert json.loads(page["properties"]["payload_json"])["headings"] == []
        assert page["properties"]["description"] == ""
        revisions = store.find_vertices(label="EntityRevision", filters={"subject_id": cid})
        assert len(revisions) == 2
        old = next(item for item in revisions if not item["properties"]["is_current"])
        state = json.loads(old["properties"]["payload_json"])
        assert json.loads(state["properties"]["payload_json"])["headings"][0]["text"] == "Old heading"
        assert state["properties"]["description"] == payload["body"]["storage"]["value"]
        latest = store.get_vertex_by_canonical_id(cid)["properties"]["payload_json"]
        assert service.ingest(SyncBatch([original], changed.captured_at))["run_status"] == "SUCCEEDED"
        assert store.get_vertex_by_canonical_id(cid)["properties"]["payload_json"] == latest
        assert store.get_vertex_by_canonical_id(cid)["properties"]["description"] == ""


@pytest.mark.req("G2-SRC-CONF-003", "FR-CONF-001")
def test_invalid_body_is_captured_and_dlq_before_business_writes(tmp_path):
    with ConfluenceConnector("https://confluence.example", token="fixture") as connector:
        event = connector.make_event("page", f"{connector.instance_id}:page:42", {
            "id": "42", "title": "Deploy", "space": {"key": "ENG"},
            "body": {"storage": {"value": "<p>unclosed"}},
        }, 1)
        store = MemoryGraphStore()
        service = SourceSyncIngestionService(
            store, connector, FileEventCapture(tmp_path / "raw"), str(tmp_path / "dlq")
        )
        result = service.ingest(SyncBatch([event], event.captured_at))
        assert result["run_status"] == "PARTIAL"
        assert result["records_rejected"] == 1
        assert store.count_vertices("Document") == 0
        assert store.count_vertices("Evidence") == 0
        assert (tmp_path / "raw" / "confluence" / f"{event.event_id}.json").exists()
        assert len(list((tmp_path / "dlq").rglob("*.json"))) == 1
