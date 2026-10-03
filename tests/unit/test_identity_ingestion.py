"""Identity resolution across ingestion sources (FR-ID-001).

The same human ingested from Jira and from Git must become ONE Person vertex
keyed by the shared email namespace, with both source identities preserved in
source_aliases.
"""

import os
import subprocess

from eoip.connectors.jira_json import JiraJsonConnector
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService
from eoip.ingestion.repository import RepositoryIngestionService

EMAIL = "Alice@Example.com"


def _git(root, *args):
    environment = {
        **os.environ,
        "GIT_AUTHOR_NAME": "Alice",
        "GIT_AUTHOR_EMAIL": EMAIL,
        "GIT_COMMITTER_NAME": "Alice",
        "GIT_COMMITTER_EMAIL": EMAIL,
    }
    subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )


def _jira_service(tmp_path):
    store = MemoryGraphStore()
    service = JiraIngestionService(
        store,
        JiraJsonConnector(),
        FileEventCapture(tmp_path / "raw"),
        tmp_path / "dlq",
    )
    return service, store


def test_jira_and_git_persons_merge_into_one_email_identity(tmp_path):
    jira, store = _jira_service(tmp_path)
    jira.ingest(
        {
            "issues": [
                {
                    "key": "EOIP-9",
                    "fields": {
                        "summary": "Shared identity",
                        "project": {"key": "EOIP", "name": "EOIP"},
                        "assignee": {
                            "accountId": "engineer-1",
                            "displayName": "Alice",
                            "emailAddress": EMAIL,
                        },
                    },
                }
            ]
        }
    )

    repository = tmp_path / "repository"
    repository.mkdir()
    (repository / "service.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
    _git(repository, "init", "--quiet")
    _git(repository, "add", "service.py")
    _git(repository, "commit", "--quiet", "-m", "EOIP-9 implementation")
    RepositoryIngestionService(store, FileEventCapture(tmp_path / "raw")).ingest(repository)

    persons = store.find_vertices(label="Person", limit=100)
    assert len(persons) == 1, f"expected exactly one Person, got: {[p['canonical_id'] for p in persons]}"
    person = persons[0]
    assert person["canonical_id"] == "urn:eoip:identity:person:email:alice@example.com"

    aliases = set(person["properties"].get("source_aliases", "").split(","))
    assert aliases == {"jira:alice@example.com", "git:alice@example.com"}

    assigned = store.find_edges(label="ASSIGNED_TO")
    authored = store.find_edges(label="AUTHORED_BY")
    assert len(assigned) == 1 and assigned[0]["in_v"] == person["vid"]
    assert len(authored) == 1 and authored[0]["in_v"] == person["vid"]


def test_jira_person_without_email_uses_source_scoped_alias(tmp_path):
    jira, store = _jira_service(tmp_path)
    jira.ingest(
        {
            "issues": [
                {
                    "key": "EOIP-10",
                    "fields": {
                        "summary": "Alias identity",
                        "project": {"key": "EOIP", "name": "EOIP"},
                        "assignee": {"accountId": "engineer-7", "displayName": "Bob"},
                    },
                }
            ]
        }
    )

    person = store.get_vertex_by_canonical_id("urn:eoip:identity:person:alias:jira:engineer-7")
    assert person is not None
    assert person["properties"]["source_aliases"] == "jira:engineer-7"
