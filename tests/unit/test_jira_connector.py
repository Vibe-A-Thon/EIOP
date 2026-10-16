import httpx
import pytest
from eoip.connectors.jira import JiraConnector


def make_jira_client(handler):
    return httpx.Client(
        base_url="https://jira.internal",
        transport=httpx.MockTransport(handler),
    )


def mock_jira_responses(request):
    path = request.url.path
    if path.endswith("/serverInfo"):
        return httpx.Response(200, json={"serverTitle": "Jira Internal", "version": "9.0"})
    if path.endswith("/project/PROJ"):
        return httpx.Response(200, json={"key": "PROJ", "name": "Test Project", "id": "1000"})
    if path.endswith("/project/PROJ/version"):
        return httpx.Response(200, json={"values": [{"id": "v101", "name": "v1.0.0", "released": True, "releaseDate": "2026-10-01"}]})
    if path.endswith("/project/PROJ/statuses"):
        return httpx.Response(200, json=[{
            "id": "it-1", "name": "Story",
            "statuses": [{"id": "st-1", "name": "Open"}, {"id": "st-2", "name": "In Progress"}]
        }])
    if "/board" in path and not path.endswith("/sprint"):
        return httpx.Response(200, json={"values": [{"id": 5, "location": {"projectKey": "PROJ"}}]})
    if path.endswith("/sprint"):
        return httpx.Response(200, json={"values": [{"id": 42, "name": "Sprint 1", "state": "active", "goal": "Deliver MVP"}]})
    if "/search" in path:
        return httpx.Response(200, json={
            "issues": [{
                "id": "10001",
                "key": "PROJ-1",
                "fields": {
                    "summary": "Implement acquisition connector",
                    "project": {"key": "PROJ"},
                    "issuetype": {"id": "it-1", "name": "Story"},
                    "status": {"id": "st-2", "name": "In Progress"},
                    "created": "2026-10-01T10:00:00.000+0000",
                    "updated": "2026-10-02T12:00:00.000+0000",
                    "fixVersions": [{"id": "v101", "name": "v1.0.0"}],
                }
            }]
        })
    if "/comment" in path:
        return httpx.Response(200, json={"comments": []})
    if "/issue/PROJ-1/changelog" in path:
        return httpx.Response(200, json={
            "values": [{
                "id": "hist-101",
                "created": "2026-10-02T11:00:00.000+0000",
                "items": [{
                    "field": "status",
                    "fieldtype": "jira",
                    "fromString": "Open",
                    "toString": "In Progress",
                }],
            }]
        })
    return httpx.Response(404, json={"error": "not found"})


@pytest.mark.req("CONN-03")
def test_jira_offline_fixtures_and_baseline():
    client = make_jira_client(mock_jira_responses)
    connector = JiraConnector(
        "jira-src",
        "https://jira.internal",
        projects=["PROJ"],
        token="mock-token",
        client=client,
        include_changelog=True,
        include_sprints=True,
    )
    events = list(connector.baseline())
    assert len(events) >= 5
    kinds = {e.metadata["record_kind"] for e in events}
    assert "project" in kinds
    assert "version" in kinds
    assert "issue" in kinds
    assert "changelog" in kinds
    assert "sprint" in kinds


@pytest.mark.req("G2-SRC-JIRA-002")
def test_jira_issue_extraction_with_fields():
    client = make_jira_client(mock_jira_responses)
    connector = JiraConnector(
        "jira-src",
        "https://jira.internal",
        projects=["PROJ"],
        token="mock-token",
        client=client,
        include_changelog=False,
    )
    events = list(connector.baseline())
    issue_events = [e for e in events if e.metadata["record_kind"] == "issue"]
    assert len(issue_events) == 1
    issue = issue_events[0]
    assert issue.source_record_id.endswith(":PROJ-1")
    assert issue.payload["fields"]["summary"] == "Implement acquisition connector"
    assert issue.payload["fields"]["status"]["name"] == "In Progress"


@pytest.mark.req("G2-SRC-JIRA-003")
def test_jira_changelog_streaming_and_history():
    client = make_jira_client(mock_jira_responses)
    connector = JiraConnector(
        "jira-src",
        "https://jira.internal",
        projects=["PROJ"],
        token="mock-token",
        client=client,
        include_changelog=True,
    )
    events = list(connector.baseline())
    cl_events = [e for e in events if e.metadata["record_kind"] == "changelog"]
    assert len(cl_events) >= 1
    cl = cl_events[0]
    assert "hist-101" in cl.source_record_id
    assert cl.payload["field"] == "status"
    assert cl.payload["fromString"] == "Open"
    assert cl.payload["toString"] == "In Progress"


@pytest.mark.req("G2-SRC-JIRA-004")
def test_jira_project_version_and_metadata_hierarchy():
    client = make_jira_client(mock_jira_responses)
    connector = JiraConnector(
        "jira-src",
        "https://jira.internal",
        projects=["PROJ"],
        token="mock-token",
        client=client,
    )
    events = list(connector.baseline())
    proj_events = [e for e in events if e.metadata["record_kind"] == "project"]
    assert len(proj_events) == 1
    assert proj_events[0].source_record_id.endswith(":PROJ")
    assert proj_events[0].payload["name"] == "Test Project"

    ver_events = [e for e in events if e.metadata["record_kind"] == "version"]
    assert len(ver_events) == 1
    assert ver_events[0].source_record_id.endswith(":v101")
    assert ver_events[0].payload["name"] == "v1.0.0"


@pytest.mark.req("G2-SRC-JIRA-005")
def test_jira_sprints_and_agile_metadata():
    client = make_jira_client(mock_jira_responses)
    connector = JiraConnector(
        "jira-src",
        "https://jira.internal",
        projects=["PROJ"],
        token="mock-token",
        client=client,
        include_sprints=True,
    )
    events = list(connector.baseline())
    sprint_events = [e for e in events if e.metadata["record_kind"] == "sprint"]
    assert len(sprint_events) == 1
    assert sprint_events[0].source_record_id.endswith(":42")
    assert sprint_events[0].payload["name"] == "Sprint 1"
    assert sprint_events[0].payload["state"] == "active"


@pytest.mark.req("G2-SRC-JIRA-006")
def test_jira_webhook_event_handling():
    client = make_jira_client(mock_jira_responses)
    connector = JiraConnector(
        "jira-src",
        "https://jira.internal",
        projects=["PROJ"],
        token="mock-token",
        client=client,
    )
    webhook_payload = {
        "webhookEvent": "jira:issue_updated",
        "issue": {
            "key": "PROJ-2",
            "fields": {"summary": "Webhook issue", "project": {"key": "PROJ"}}
        },
        "changelog": {
            "id": "ch-99",
            "created": "2026-10-02T15:00:00.000+0000",
            "items": [{"field": "priority", "fromString": "Medium", "toString": "High"}]
        }
    }
    events = list(connector.handle_event(webhook_payload))
    assert len(events) == 2  # changelog and issue
    assert events[0].metadata["record_kind"] == "changelog"
    assert events[1].metadata["record_kind"] == "issue"
    assert events[1].operation == "UPSERT"

    # Test delete webhook
    delete_payload = {
        "webhookEvent": "jira:issue_deleted",
        "issue": {
            "key": "PROJ-2",
            "fields": {"project": {"key": "PROJ"}}
        }
    }
    del_events = list(connector.handle_event(delete_payload))
    assert len(del_events) == 1
    assert del_events[0].operation == "DELETE"
