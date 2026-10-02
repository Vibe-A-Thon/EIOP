from eoip.codegraph.parser import CodeParser
from eoip.connectors.local_code import LocalCodeConnector
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.code import CodeIngestionService
from eoip.ingestion.jira import FileEventCapture


def test_local_code_ingestion_builds_typed_graph_with_source_evidence(tmp_path) -> None:
    source_root = tmp_path / "repo"
    source_root.mkdir()
    (source_root / "service.py").write_text(
        "def run():\n    return normalize()\n\ndef normalize():\n    return 'ok'\n",
        encoding="utf-8",
    )
    store = MemoryGraphStore()
    service = CodeIngestionService(
        store,
        LocalCodeConnector(),
        CodeParser(),
        FileEventCapture(tmp_path / "raw"),
        tmp_path / "dlq",
    )

    first = service.ingest(source_root, "repo-1")
    second = service.ingest(source_root, "repo-1")

    assert first["counts"] == {"files": 1, "symbols": 2, "dependencies": 0, "calls": 1}
    assert second["counts"] == first["counts"]
    assert store.count_vertices("Repository") == 1
    assert store.count_vertices("File") == 1
    assert store.count_vertices("CodeSymbol") == 2
    assert store.count_edges("CALLS") == 1
    assert store.count_edges("EVIDENCED_BY") == 3


def test_local_code_connector_rejects_oversized_source(tmp_path) -> None:
    source_root = tmp_path / "repo"
    source_root.mkdir()
    (source_root / "large.py").write_text("x" * 32, encoding="utf-8")

    connector = LocalCodeConnector(max_file_bytes=16)

    try:
        connector.events(source_root, "repo-1")
    except ValueError as exc:
        assert "exceeds" in str(exc)
    else:
        raise AssertionError("oversized source was accepted")