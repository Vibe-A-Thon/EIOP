from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.incremental_indexer import (
    GitHookInstaller,
    IncrementalIndexer,
    result_to_event,
    run_incremental_index,
)
from jsonschema import validate


def _init_repo(path):
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=path, check=True)


def _commit(path, message):
    subprocess.run(["git", "add", "."], cwd=path, check=True)
    subprocess.run(["git", "commit", "-m", message], cwd=path, check=True, capture_output=True)
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=path, check=True, capture_output=True, text=True).stdout.strip()


def _symbol_snapshot(store):
    return sorted(
        (vertex["properties"]["path"], vertex["properties"]["qualified_name"], vertex["properties"]["symbol_kind"])
        for vertex in store.find_vertices("CodeSymbol", limit=100_000)
    )


@pytest.mark.req("KGR-G-012")
def test_incremental_indexer_updates_only_changed_files_and_propagates_cross_file_impact(tmp_path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "a.py").write_text("def target(value: int) -> int:\n    return value + 1\n", encoding="utf-8")
    (repo / "b.py").write_text(
        "from a import target\n\n"
        "def caller(value: int) -> int:\n"
        "    return target(value)\n",
        encoding="utf-8",
    )
    store = MemoryGraphStore()
    indexer = IncrementalIndexer(store, str(repo), cache_path=tmp_path / "hashes.json")
    indexer.index_files(["a.py", "b.py"])

    (repo / "a.py").write_text("def renamed(value: int) -> int:\n    return value + 1\n", encoding="utf-8")
    result = indexer.index_files(["a.py"])

    assert result.files_processed == 1
    assert result.symbols_removed == 1
    assert result.symbols_added == 1
    assert any("b.py:caller" in dependent for impact in result.impacts for dependent in impact.affected_dependents)


@pytest.mark.req("KGR-G-012")
def test_incremental_indexer_matches_fresh_full_symbol_index_for_same_commit_set(tmp_path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "service.py").write_text("def alpha() -> int:\n    return 1\n", encoding="utf-8")
    incremental_store = MemoryGraphStore()
    incremental = IncrementalIndexer(incremental_store, str(repo), cache_path=tmp_path / "inc-hashes.json")
    incremental.index_files(["service.py"])

    (repo / "service.py").write_text(
        "def alpha() -> int:\n    return 1\n\n"
        "def beta() -> int:\n    return alpha()\n",
        encoding="utf-8",
    )
    incremental.index_files(["service.py"])

    fresh_store = MemoryGraphStore()
    fresh = IncrementalIndexer(fresh_store, str(repo), cache_path=tmp_path / "fresh-hashes.json")
    fresh.index_files(["service.py"])

    assert _symbol_snapshot(incremental_store) == _symbol_snapshot(fresh_store)


@pytest.mark.req("KGR-G-012")
def test_incremental_indexer_handles_hundred_file_diff_under_two_seconds(tmp_path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    for index in range(100):
        (repo / f"module_{index}.py").write_text(f"def f_{index}() -> int:\n    return {index}\n", encoding="utf-8")
    base = _commit(repo, "base")
    for index in range(100):
        (repo / f"module_{index}.py").write_text(f"def f_{index}() -> int:\n    return {index + 1}\n", encoding="utf-8")
    head = _commit(repo, "change")

    result = IncrementalIndexer(MemoryGraphStore(), str(repo), cache_path=tmp_path / "hashes.json").index_diff(base, head)

    assert result.files_processed == 100
    assert result.duration_ms < 2000


@pytest.mark.req("KGR-G-012")
def test_incremental_index_event_matches_schema(tmp_path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "service.py").write_text("def alpha() -> int:\n    return 1\n", encoding="utf-8")
    result = IncrementalIndexer(MemoryGraphStore(), str(repo)).index_files(["service.py"])
    event = result_to_event(result, commit_sha="a" * 40, trigger="MANUAL")
    schema = json.loads(
        (Path(__file__).resolve().parents[2] / "schemas" / "incremental_index_event.schema.json").read_text()
    )

    validate(event, schema)
    assert event["metadata"]["requirement_id"] == "KGR-G-012"
    assert event["files_changed"][0]["change_type"] == "MODIFIED"


@pytest.mark.req("KGR-G-012")
def test_install_hooks_command_writes_real_incremental_hook(tmp_path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)

    hook = GitHookInstaller.install(str(repo))

    assert hook.exists()
    content = hook.read_text(encoding="utf-8")
    assert "eoip.ingestion.incremental_indexer" in content
    assert "load_demo" not in content


@pytest.mark.req("KGR-G-012")
def test_run_incremental_index_writes_report_for_git_diff(tmp_path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    (repo / "service.py").write_text("def alpha() -> int:\n    return 1\n", encoding="utf-8")
    base = _commit(repo, "base")
    (repo / "service.py").write_text("def alpha() -> int:\n    return 2\n", encoding="utf-8")
    head = _commit(repo, "change")
    report = repo / ".eoip" / "incremental-index" / "last-event.json"

    event = run_incremental_index(repo_root=repo, base_ref=base, head_ref=head, trigger="POST_COMMIT", report=report)

    assert report.exists()
    assert event["commit_sha"] == head
    assert event["trigger"] == "POST_COMMIT"
    assert json.loads(report.read_text(encoding="utf-8"))["event_id"] == event["event_id"]
