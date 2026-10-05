"""Actual demo files become graph documents, RAG bundles and typed Jira records."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest
from eoip.graph.memory import MemoryGraphStore

from scripts.load_demo_corpus import corpus_files, load_demo_corpus

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def corpus(tmp_path_factory):
    project = tmp_path_factory.mktemp("demo-corpus")
    for directory in ("demo", "schemas", "config"):
        shutil.copytree(
            ROOT / directory, project / directory,
            ignore=shutil.ignore_patterns(".git", "__pycache__"),
        )
    repository = project / "demo" / "demodata" / "core" / "demo-repo"
    for arguments in (
        ["init", "-b", "main"], ["add", "."],
        ["-c", "user.name=Demo Test", "-c", "user.email=demo@example.invalid",
         "commit", "-m", "EOIP-1 implement impact calculation"],
    ):
        subprocess.run(["git", "-C", str(repository), *arguments], check=True, capture_output=True)
    store = MemoryGraphStore()
    marker = store.upsert_vertex(
        "Document", {"canonical_id": "urn:eoip:test:existing", "name": "Retained", "path": "test://existing"}
    )
    data = project / "data"
    result = load_demo_corpus(store, data, project)
    return project, data, store, marker, result


def test_entire_corpus_is_ingested_and_existing_data_is_preserved(corpus):
    project, data, store, marker, result = corpus
    checkpoint = json.loads((data / "state" / "demo-corpus.json").read_text(encoding="utf-8"))
    expected = {
        path.relative_to(project / "demo" / "demodata").as_posix()
        for path in corpus_files(project)
    }
    assert set(checkpoint["assets"]) == expected
    assert result["files"] == result["loaded"] == len(expected)
    assert result["retained"] == 0
    assert result["enterprise_scenarios"] == 11
    assert store.get_vertex_by_canonical_id(marker["canonical_id"]) == marker
    for folder in ("manual", "pipelines"):
        issues = json.loads((project / "demo" / "demodata" / folder / "jira.json").read_text())["issues"]
        assert all(store.get_vertex_by_canonical_id(f"urn:eoip:work:item:jira:{item['key']}") for item in issues)


def test_office_documents_and_every_rag_chunk_are_readable(corpus):
    _project, data, store, _marker, result = corpus
    checkpoint = json.loads((data / "state" / "demo-corpus.json").read_text(encoding="utf-8"))
    assert {Path(name).suffix for name in checkpoint["assets"]} >= {".docx", ".xlsx", ".pptx", ".json", ".py", ".ts"}
    assert result["documents"] > 0 and result["chunks"] > 0
    for receipt in checkpoint["assets"].values():
        bundle = data / "fileparse" / receipt["bundle_id"]
        manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["status"] == "SUCCEEDED"
        assert (bundle / "chunks.jsonl").is_file()
        assert (bundle / "vectors.jsonl").is_file()
        assert all(store.get_vertex_by_canonical_id(cid) for cid in receipt["canonical_ids"])


def test_rerun_retains_data_without_duplicate_runs_or_artifacts(corpus):
    project, data, store, _marker, original = corpus
    before = (store.count_vertices(), store.count_edges())
    result = load_demo_corpus(store, data, project)
    assert result["loaded"] == 0
    assert result["retained"] == original["files"]
    assert before == (store.count_vertices(), store.count_edges())


def test_missing_bundle_is_regenerated_without_resetting_graph(corpus):
    project, data, store, marker, original = corpus
    checkpoint = json.loads((data / "state" / "demo-corpus.json").read_text(encoding="utf-8"))
    name, receipt = next(iter(checkpoint["assets"].items()))
    (data / "fileparse" / receipt["bundle_id"] / "manifest.json").unlink()
    result = load_demo_corpus(store, data, project)
    assert result["loaded"] == 1
    assert result["retained"] == original["files"] - 1
    updated = json.loads((data / "state" / "demo-corpus.json").read_text(encoding="utf-8"))
    assert updated["assets"][name]["bundle_id"] != receipt["bundle_id"]
    assert store.get_vertex_by_canonical_id(marker["canonical_id"]) == marker


def test_unsupported_asset_fails_before_graph_mutation(tmp_path):
    directory = tmp_path / "demo" / "demodata"
    directory.mkdir(parents=True)
    (directory / "unrecognized.bin").write_bytes(b"unsupported")
    store = MemoryGraphStore()
    with pytest.raises(ValueError, match="Unsupported demo asset"):
        load_demo_corpus(store, tmp_path / "data", tmp_path)
    assert store.count_vertices() == 0


def test_invalid_json_is_reported_without_a_completed_asset_receipt(corpus):
    project, data, store, marker, _original = corpus
    (project / "demo" / "demodata" / "invalid.json").write_text("{invalid", encoding="utf-8")
    with pytest.raises(ValueError):
        load_demo_corpus(store, data, project)
    checkpoint = json.loads((data / "state" / "demo-corpus.json").read_text(encoding="utf-8"))
    assert "invalid.json" not in checkpoint["assets"]
    assert store.get_vertex_by_canonical_id(marker["canonical_id"]) == marker
