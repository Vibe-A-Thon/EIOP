import os
import subprocess

from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.jira import FileEventCapture
from eoip.ingestion.repository import RepositoryIngestionService


def _git(root, *args):
    environment = {
        **os.environ,
        "GIT_AUTHOR_NAME": "EOIP Test",
        "GIT_AUTHOR_EMAIL": "eoip-test@example.invalid",
        "GIT_COMMITTER_NAME": "EOIP Test",
        "GIT_COMMITTER_EMAIL": "eoip-test@example.invalid",
    }
    subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )


def test_repository_ingestion_links_entities_to_evidence_and_run(tmp_path):
    repository = tmp_path / "repository"
    repository.mkdir()
    (repository / "service.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
    (repository / "README.md").write_text("# EOIP demo\n", encoding="utf-8")
    _git(repository, "init", "--quiet")
    _git(repository, "add", "service.py", "README.md")
    _git(repository, "commit", "--quiet", "-m", "EOIP-1 demo implementation")

    store = MemoryGraphStore()
    result = RepositoryIngestionService(store, FileEventCapture(tmp_path / "raw")).ingest(
        repository,
        metadata={
            "merge_requests": [
                {
                    "iid": 17,
                    "title": "EOIP-1 demo implementation",
                    "source_branch": "feature/demo",
                    "target_branch": "main",
                    "merge_commit_sha": "HEAD",
                }
            ],
            "pipelines": [{"id": 42, "name": "build", "status": "success", "sha": "HEAD"}],
        },
    )

    run = store.get_vertex_by_canonical_id(f"urn:eoip:meta:ingestion-run:{result['run_id']}")
    assert run is not None
    ingested = store.find_vertices(filters={"ingestion_run_id": result["run_id"]}, limit=100)
    assert {
        "Repository",
        "Branch",
        "Commit",
        "File",
        "CodeSymbol",
        "Document",
        "MergeRequest",
        "PipelineRun",
    }.issubset({vertex["label"] for vertex in ingested})
    for vertex in ingested:
        run_edges = store.edges_from(vertex["vid"], labels=["INGESTED_IN"])
        assert any(edge["in_v"] == run["vid"] for edge in run_edges), vertex["canonical_id"]
        if vertex["label"] in {"Repository", "Branch", "Commit", "File", "CodeSymbol", "Document", "MergeRequest", "PipelineRun"}:
            assert store.edges_from(vertex["vid"], labels=["EVIDENCED_BY"])

    domain_edges = store.find_edges(label="BELONGS_TO_DOMAIN")
    assert len(domain_edges) >= 3
    domain_vids = {e["in_v"] for e in domain_edges}
    for vid in domain_vids:
        assert store.get_vertex(vid)["label"] == "GraphDomain"


def test_multi_commit_ingestion_creates_succeeds_edges(tmp_path):
    """P1-18: multi-commit ingestion walks history and links parents."""
    repository = tmp_path / "repo"
    repository.mkdir()
    (repository / "main.py").write_text("x = 1\n", encoding="utf-8")
    _git(repository, "init", "--quiet")
    _git(repository, "add", "main.py")
    _git(repository, "commit", "--quiet", "-m", "first commit")

    (repository / "main.py").write_text("x = 2\n", encoding="utf-8")
    _git(repository, "add", "main.py")
    _git(repository, "commit", "--quiet", "-m", "second commit")

    (repository / "main.py").write_text("x = 3\n", encoding="utf-8")
    _git(repository, "add", "main.py")
    _git(repository, "commit", "--quiet", "-m", "third commit")

    store = MemoryGraphStore()
    result = RepositoryIngestionService(store, FileEventCapture(tmp_path / "raw")).ingest(repository)

    assert result["commits_ingested"] == 3
    commits = store.find_vertices(label="Commit", limit=10)
    assert len(commits) == 3

    succeeds_edges = store.find_edges(label="SUCCEEDS")
    assert len(succeeds_edges) == 2
    for edge in succeeds_edges:
        parent = store.get_vertex(edge["in_v"])
        child = store.get_vertex(edge["out_v"])
        assert parent["label"] == "Commit"
        assert child["label"] == "Commit"


def test_diff_hunk_links_commits_to_symbols(tmp_path):
    """P1-18: diff hunks link commits to the CodeSymbols they modify."""
    repository = tmp_path / "repo"
    repository.mkdir()
    (repository / "app.py").write_text(
        "def hello():\n    return 'hi'\n\ndef goodbye():\n    return 'bye'\n",
        encoding="utf-8",
    )
    _git(repository, "init", "--quiet")
    _git(repository, "add", "app.py")
    _git(repository, "commit", "--quiet", "-m", "initial")

    (repository / "app.py").write_text(
        "def hello():\n    return 'hello world'\n\ndef goodbye():\n    return 'bye'\n",
        encoding="utf-8",
    )
    _git(repository, "add", "app.py")
    _git(repository, "commit", "--quiet", "-m", "update hello")

    store = MemoryGraphStore()
    result = RepositoryIngestionService(store, FileEventCapture(tmp_path / "raw")).ingest(repository)

    assert result["commits_ingested"] == 2
    ref_edges = store.find_edges(label="REFERENCES")
    commit_to_symbol = [
        e for e in ref_edges
        if store.get_vertex(e["out_v"])["label"] == "Commit"
        and store.get_vertex(e["in_v"])["label"] == "CodeSymbol"
    ]
    assert len(commit_to_symbol) >= 1
