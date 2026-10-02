from eoip.connectors.gitlab_json import GitLabJsonConnector
from eoip.connectors.jira_json import JiraJsonConnector
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.gitlab import GitLabIngestionService
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService

from apps.worker.main import execute_job


def test_gitlab_metadata_links_only_existing_issue_and_commit_anchors(tmp_path) -> None:
    store = MemoryGraphStore()
    jira = JiraIngestionService(
        store,
        JiraJsonConnector(),
        FileEventCapture(tmp_path / "raw"),
        tmp_path / "dlq",
    )
    jira.ingest({"issues": [{"key": "EOIP-1", "fields": {"summary": "Trace"}}]})
    repo = store.upsert_vertex(
        "Repository",
        {"canonical_id": "urn:eoip:code:repository:demo", "repo_id": "demo", "name": "demo"},
    )
    commit = store.upsert_vertex(
        "Commit",
        {
            "canonical_id": "urn:eoip:code:commit:demo:0123456789abcdef0123456789abcdef01234567",
            "commit_sha": "0123456789abcdef0123456789abcdef01234567",
            "name": "Trace endpoint change",
            "repo_id": "demo",
        },
    )
    gitlab = GitLabIngestionService(
        store,
        "demo",
        GitLabJsonConnector(),
        FileEventCapture(tmp_path / "raw"),
        tmp_path / "dlq",
    )
    fixture = {
        "merge_requests": [
            {
                "iid": 17,
                "title": "EOIP-1 Trace endpoint",
                "state": "merged",
                "source_branch": "feature/EOIP-1",
                "merge_commit_sha": "0123456789abcdef0123456789abcdef01234567",
            },
            {
                "iid": 18,
                "title": "EOIP-404 Missing references",
                "state": "opened",
                "source_branch": "feature/EOIP-404",
                "merge_commit_sha": "not-imported",
            },
        ],
        "pipelines": [
            {
                "id": 204,
                "name": "build",
                "status": "success",
                "sha": "0123456789abcdef0123456789abcdef01234567",
                "ref": "main",
                "work_item_keys": ["EOIP-1"],
            }
        ],
    }

    result = gitlab.ingest(fixture)

    assert result["records_accepted"] == 3
    assert store.count_vertices("MergeRequest") == 2
    assert store.count_vertices("PipelineRun") == 1
    assert store.count_edges("IMPLEMENTS") == 1
    assert store.count_edges("PRODUCED_BY") == 1
    assert store.count_edges("REFERENCES") == 2
    references = store.find_edges(label="REFERENCES")
    assert {(edge["out_cid"], edge["in_cid"]) for edge in references} == {
        (
            "urn:eoip:cicd:merge-request:gitlab:demo:17",
            "urn:eoip:code:commit:demo:0123456789abcdef0123456789abcdef01234567",
        ),
        (
            "urn:eoip:cicd:pipeline:gitlab:demo:204",
            "urn:eoip:work:item:jira:EOIP-1",
        ),
    }
    assert store.get_vertex(commit["vid"]) is not None
    assert store.get_vertex(repo["vid"]) is not None


def test_worker_executes_queued_gitlab_ingestion(tmp_path) -> None:
    store = MemoryGraphStore()
    job = {
        "kind": "GITLAB_JSON",
        "correlation_id": "test-correlation",
        "payload": {
            "repository_id": "platform/api",
            "document": {
                "merge_requests": [{"iid": 7, "title": "Implement EOIP-7"}],
                "pipelines": [{"id": 9, "name": "test", "status": "success"}],
            },
        },
    }

    result = execute_job(store, tmp_path, job)

    assert result["run_status"] == "SUCCEEDED"
    assert result["records_accepted"] == 2
    assert store.get_vertex_by_canonical_id("urn:eoip:code:repository:platform/api")
    assert store.count_vertices("MergeRequest") == 1
    assert store.count_vertices("PipelineRun") == 1
