import json
from html import escape

import pytest
from eoip.agents.governed import DocumentationFreshnessAgent
from eoip.connectors.confluence import ConfluenceConnector
from eoip.connectors.sync import SyncBatch
from eoip.contracts.agent import AgentRequest
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.jira import FileEventCapture
from eoip.ingestion.source_sync import SourceSyncIngestionService
from eoip.validation.engine import ValidationEngine
from fastapi.testclient import TestClient

from apps.api.app import create_app


def setup(tmp_path):
    store = MemoryGraphStore()
    connector = ConfluenceConnector("https://wiki.example", token="fixture")
    service = SourceSyncIngestionService(
        store, connector, FileEventCapture(tmp_path / "raw"), str(tmp_path / "dlq"),
    )
    return store, connector, service


def page(connector, refs, day=1):
    body = "".join(f'<a href="{escape(ref, quote=True)}">Explicit reference</a>' for ref in refs)
    payload = {
        "id": "42", "title": "Runbook", "space": {"key": "ENG"},
        "version": {"number": day}, "body": {"storage": {"value": body}},
    }
    return connector.make_event("page", f"{connector.instance_id}:page:42", payload, day).model_copy(
        update={"event_time": f"2026-10-{day:02d}T00:00:00Z"}
    )


def ingest(service, event):
    assert service.ingest(SyncBatch([event], event.captured_at))["run_status"] == "SUCCEEDED"


def freshness(store):
    return [f for f in ValidationEngine(store).run()["findings"]
            if f["rule"] == "stale_document_reference"]


@pytest.mark.req("G2-SRC-CONF-004", "G2-T0405")
@pytest.mark.parametrize(("label", "properties"), [
    ("Service", {"service_id": "checkout", "name": "Checkout"}),
    ("APIService", {"name": "Checkout API"}),
    ("APIEndpoint", {"name": "Create order", "path": "/orders", "method": "POST"}),
    ("Project", {"name": "Checkout"}),
    ("WorkItem", {"issue_key": "EOIP-42", "summary": "Requirement", "issue_type": "Requirement"}),
    ("File", {"repo_id": "checkout", "path": "checkout.py", "content_hash": "v1"}),
    ("CodeSymbol", {"qualified_name": "checkout.create", "symbol_kind": "function"}),
])
def test_explicit_canonical_links_are_evidence_backed_and_temporal(tmp_path, label, properties):
    store, connector, service = setup(tmp_path)
    try:
        cid = f"urn:eoip:test:{label.lower()}:42"
        target = store.upsert_vertex(label, {"canonical_id": cid, **properties})
        event = page(connector, [cid, cid])
        ingest(service, event)
        links = store.find_edges(label="DOCUMENTS")
        assert len(links) == 1 and links[0]["in_v"] == target["vid"]
        edge = links[0]
        assert edge["properties"]["creation_status"] == "DETERMINISTIC"
        assert edge["properties"]["evidence_key"] == event.event_id
        assert json.loads(edge["properties"]["payload_json"])["matched_reference"] == cid
        assert edge["properties"]["is_current"] is True
        revisions = store.count_vertices("RelationshipRevision")
        ingest(service, event)
        assert store.count_vertices("RelationshipRevision") == revisions
        assert freshness(store) == []
    finally:
        connector.close()


@pytest.mark.req("G2-SRC-CONF-004")
def test_exact_url_resolution_refuses_ambiguous_titles_and_unknown_references(tmp_path):
    store, connector, service = setup(tmp_path)
    try:
        url = "https://api.example/orders"
        store.upsert_vertex("APIEndpoint", {
            "canonical_id": "urn:eoip:test:api:one", "name": "Deploy",
            "path": url, "method": "POST",
        })
        event = page(connector, [url, "https://unknown.example/Deploy"])
        ingest(service, event)
        assert [e["in_cid"] for e in store.find_edges(label="DOCUMENTS")] == ["urn:eoip:test:api:one"]
        store.upsert_vertex("APIEndpoint", {
            "canonical_id": "urn:eoip:test:api:two", "name": "Deploy",
            "path": url, "method": "GET",
        })
        ingest(service, page(connector, [url], 2))
        assert store.find_edges(label="DOCUMENTS") == []
    finally:
        connector.close()


@pytest.mark.req("G2-SRC-CONF-004", "G2-SRC-CONF-005", "FR-CONN-006")
def test_fact_changes_not_observations_trigger_staleness_and_replay_cannot_rebase(tmp_path):
    store, connector, service = setup(tmp_path)
    try:
        cid = "urn:eoip:test:service:checkout"
        store.upsert_vertex("Service", {"canonical_id": cid, "service_id": "checkout", "name": "Checkout"})
        original = page(connector, [cid])
        ingest(service, original)
        store.upsert_vertex("Service", {
            "canonical_id": cid, "last_seen": "2026-10-02T00:00:00Z",
            "modified_at": "2026-10-02T00:00:00Z", "ingestion_run_id": "another-run",
            "source_version": "2", "content_hash": "different-source-envelope",
        })
        assert freshness(store) == []
        store.upsert_vertex("Service", {"canonical_id": cid, "name": "Checkout v2"})
        assert len(freshness(store)) == 1
        assert freshness(store)[0]["target_id"] == cid
        assert freshness(store)[0]["reason"] == "target_changed"
        ingest(service, original)
        assert len(freshness(store)) == 1
        changed = page(connector, [cid], 2)
        ingest(service, changed)
        assert freshness(store) == []
        ingest(service, original)
        assert freshness(store) == []
        edge = store.find_edges(label="DOCUMENTS")[0]
        assert edge["properties"]["evidence_key"] == changed.event_id
        assert not edge["properties"].get("valid_to")
        ingest(service, page(connector, [], 3))
        assert store.find_edges(label="DOCUMENTS") == []
        ingest(service, original)
        assert store.find_edges(label="DOCUMENTS") == []
        assert store.find_edges(label="DOCUMENTS", include_historical=True)
    finally:
        connector.close()


@pytest.mark.req("G2-SRC-CONF-005")
def test_tombstone_staleness_is_exposed_by_existing_api_and_agent(tmp_path):
    store, connector, service = setup(tmp_path)
    try:
        cid = "urn:eoip:test:service:checkout"
        store.upsert_vertex("Service", {"canonical_id": cid, "service_id": "checkout", "name": "Checkout"})
        event = page(connector, [cid])
        ingest(service, event)
        store.tombstone_vertex(cid)
        assert freshness(store)[0]["reason"] == "target_deleted"
        ingest(service, event)
        assert freshness(store)[0]["reason"] == "target_deleted"
        client = TestClient(create_app(store))
        response = client.get("/api/v1/graph/stale")
        assert response.status_code == 200
        refs = [r for r in response.json()["stale"] if r["anomaly_type"] == "stale_document_reference"]
        assert len(refs) == 1 and refs[0]["details"]["target_id"] == cid
        document_id = f"urn:eoip:knowledge:document:{event.source_record_id}"
        assert refs[0]["canonical_id"] == document_id
        request = AgentRequest(request_id="freshness-test", agent_id="DocumentationFreshness", goal="Check documentation")
        result = DocumentationFreshnessAgent().execute(request, store)
        assert result.status == "PARTIAL" and document_id in result.evidence_refs
        assert freshness(store)[0]["severity"] == "WARNING"
    finally:
        connector.close()


@pytest.mark.req("G2-SRC-CONF-004", "G2-SRC-CONF-005", "G2-T0225")
def test_deleted_document_expires_links_and_old_replay_cannot_restore_it(tmp_path):
    store, connector, service = setup(tmp_path)
    try:
        cid = "urn:eoip:test:service:checkout"
        store.upsert_vertex("Service", {"canonical_id": cid, "service_id": "checkout", "name": "Checkout"})
        original = page(connector, [cid])
        ingest(service, original)
        deleted = page(connector, [cid], 2).model_copy(update={"operation": "DELETE"})
        ingest(service, deleted)
        assert store.find_edges(label="DOCUMENTS") == []
        ingest(service, original)
        document = store.get_vertex_by_canonical_id(f"urn:eoip:knowledge:document:{original.source_record_id}")
        assert document["properties"]["deleted_at"]
        assert store.find_edges(label="DOCUMENTS") == []
        assert freshness(store) == []
    finally:
        connector.close()
