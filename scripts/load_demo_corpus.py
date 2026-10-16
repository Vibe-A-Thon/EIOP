"""Add the checked-in demo corpus to the existing graph without resetting data."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from eoip.connectors.files import file_event
from eoip.connectors.jira_json import JiraJsonConnector
from eoip.demo import load_demo
from eoip.demo_scenarios import read_demo_scenario_pack
from eoip.fileparse.contracts import PARSER_VERSION
from eoip.fileparse.engine import SUPPORTED_EXTENSIONS
from eoip.graph.store import GraphStore
from eoip.ingestion.files import FileIngestionService
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService
from eoip.jobs import write_json
from eoip.runtime import create_store, data_root

TEXT_SOURCE_EXTENSIONS = {".md", ".py", ".ts"}


def corpus_files(project_root: Path) -> list[Path]:
    root = project_root / "demo" / "demodata"
    if not root.is_dir():
        raise FileNotFoundError(f"Demo corpus directory is unavailable: {root}")
    return sorted(
        path for path in root.rglob("*")
        if path.is_file()
        and not {".git", "__pycache__"}.intersection(path.relative_to(root).parts)
        and path.name != "__init__.py"
    )


def load_demo_corpus(store: GraphStore, data_dir: Path, project_root: Path) -> dict:
    paths = corpus_files(project_root)
    if not paths:
        raise ValueError("Demo corpus must not be empty")
    for path in paths:
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS | TEXT_SOURCE_EXTENSIONS:
            raise ValueError(f"Unsupported demo asset: {path.relative_to(project_root)}")
    checkpoint_path = data_dir / "state" / "demo-corpus.json"
    checkpoint = (
        json.loads(checkpoint_path.read_text(encoding="utf-8"))
        if checkpoint_path.is_file() else {"schema_version": "1.0", "assets": {}, "jira": {}}
    )
    if checkpoint["schema_version"] != "1.0":
        raise ValueError("Unsupported demo corpus checkpoint version")
    pack = read_demo_scenario_pack(project_root)
    seed_ids = ["urn:eoip:code:repo:demo"] + [
        item["properties"]["canonical_id"] for item in pack["vertices"]
    ]
    seed_hash = hashlib.sha256()
    for path in paths:
        relative = path.relative_to(project_root / "demo" / "demodata")
        if relative.parts[0] == "core" or relative == Path("enterprise") / "scenario-pack.json":
            seed_hash.update(relative.as_posix().encode())
            seed_hash.update(path.read_bytes())
    seed_digest = seed_hash.hexdigest()
    if checkpoint.get("graph_seed_hash") != seed_digest or not all(
        store.get_vertex_by_canonical_id(canonical_id) for canonical_id in seed_ids
    ):
        result = load_demo(store, data_dir, project_root=project_root)
        if result["jira"]["records_rejected"] or result["git"].get("records_rejected", 0):
            raise RuntimeError("Core demo graph ingestion rejected records")
        checkpoint["graph_seed_hash"] = seed_digest
        write_json(checkpoint_path, checkpoint)

    jira = JiraIngestionService(
        store, JiraJsonConnector(), FileEventCapture(data_dir / "raw"), data_dir / "dlq"
    )
    for folder in ("manual", "pipelines"):
        path = project_root / "demo" / "demodata" / folder / "jira.json"
        document = json.loads(path.read_text(encoding="utf-8"))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        canonical_ids = [f"urn:eoip:work:item:jira:{item['key']}" for item in document["issues"]]
        if checkpoint["jira"].get(folder) != digest or not all(
            store.get_vertex_by_canonical_id(canonical_id) for canonical_id in canonical_ids
        ):
            result = jira.ingest(document)
            if result["records_rejected"] or result["records_accepted"] != len(canonical_ids):
                raise RuntimeError(f"Demo Jira ingestion incomplete: {folder}")
            checkpoint["jira"][folder] = digest
            write_json(checkpoint_path, checkpoint)

    service = FileIngestionService(store, data_dir)
    loaded = retained = documents = chunks = 0
    for path in paths:
        relative = path.relative_to(project_root / "demo" / "demodata").as_posix()
        content = path.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        previous = checkpoint["assets"].get(relative)
        bundle = data_dir / "fileparse" / previous["bundle_id"] if previous else None
        if (
            previous and previous["content_hash"] == digest and bundle
            and previous["parser_version"] == PARSER_VERSION
            and (bundle / "manifest.json").is_file()
            and all(store.get_vertex_by_canonical_id(cid) for cid in previous["canonical_ids"])
        ):
            retained += 1
            receipt = previous
        else:
            filename = path.name + ".txt" if path.suffix.lower() in TEXT_SOURCE_EXTENSIONS else path.name
            event = file_event(
                content, filename, "demo_corpus", source_uri=f"fixture://demo/demodata/{relative}"
            )
            result = service.ingest_event(event)
            if result["run_status"] != "SUCCEEDED" or not result["documents"]:
                raise RuntimeError(f"Demo asset ingestion incomplete: {relative} ({result['run_status']})")
            receipt = {
                "content_hash": digest, "bundle_id": result["bundle_id"], "parser_version": PARSER_VERSION,
                "documents": result["documents"], "chunks": result["chunks"],
                "canonical_ids": [
                    item["document_id"] for item in result["result"]["documents"]
                ] + [item["chunk_id"] for item in result["result"]["chunks"]],
            }
            checkpoint["assets"][relative] = receipt
            write_json(checkpoint_path, checkpoint)
            loaded += 1
        documents += receipt["documents"]
        chunks += receipt["chunks"]
        print(f"Demo asset ready: {relative}", flush=True)
    return {
        "run_status": "SUCCEEDED", "files": len(paths), "loaded": loaded, "retained": retained,
        "documents": documents, "chunks": chunks, "enterprise_scenarios": len(pack["scenarios"]),
        "jira_datasets": list(checkpoint["jira"]),
    }


def main() -> None:
    store = create_store()
    try:
        result = load_demo_corpus(store, data_root(), Path(__file__).resolve().parents[1])
        write_json(data_root() / "state" / "demo-corpus-result.json", result)
        print(json.dumps(result, indent=2))
    finally:
        store.close()


if __name__ == "__main__":
    main()
