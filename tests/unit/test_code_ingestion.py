from eoip.codegraph.parser import CodeParser
from eoip.connectors.local_code import LocalCodeConnector
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.code import CodeIngestionService
from eoip.ingestion.jira import FileEventCapture


def test_local_code_ingestion_builds_typed_graph_with_source_evidence(tmp_path) -> None:
    source_root = tmp_path / "repo"
    source_root.mkdir()
    (source_root / "service.py").write_text(
        "import math\n\ndef run():\n    return normalize()\n\ndef normalize():\n    return 'ok'\n",
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

    assert first["counts"] == {"files": 1, "symbols": 2, "dependencies": 1, "calls": 1}
    assert second["counts"] == first["counts"]
    assert store.count_vertices("Repository") == 1
    assert store.count_vertices("File") == 1
    assert store.count_vertices("CodeSymbol") == 2
    assert store.count_edges("CALLS") == 1
    assert store.count_edges("EVIDENCED_BY") == 4
    run = store.get_vertex_by_canonical_id(f"urn:eoip:meta:ingestion-run:{first['run_id']}")
    repository = store.get_vertex_by_canonical_id("urn:eoip:code:repository:repo-1")
    dependency = store.get_vertex_by_canonical_id("urn:eoip:code:dependency:python:math")
    assert run is not None and repository is not None and dependency is not None
    for vertex in (repository, dependency):
        assert any(
            edge["in_v"] == run["vid"]
            for edge in store.edges_from(vertex["vid"], labels=["INGESTED_IN"])
        )


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