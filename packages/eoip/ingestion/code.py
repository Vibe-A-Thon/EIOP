"""Capture-first local code ingestion into the typed code graph."""

from __future__ import annotations

import json
from pathlib import Path

from eoip.codegraph.parser import PARSER_VERSION, CodeParser
from eoip.connectors.local_code import LocalCodeConnector
from eoip.contracts.source_event import utc_now_iso
from eoip.graph.store import GraphStore
from eoip.ingestion.jira import FileEventCapture
from eoip.ontology.manifest import ONTOLOGY_VERSION, SCHEMA_VERSION


class CodeIngestionService:
    def __init__(
        self,
        store: GraphStore,
        connector: LocalCodeConnector,
        parser: CodeParser,
        capture: FileEventCapture,
        dlq_root: str | Path,
    ) -> None:
        self.store = store
        self.connector = connector
        self.parser = parser
        self.capture = capture
        self.dlq_root = Path(dlq_root)

    def ingest(self, source_root: str | Path, repo_id: str) -> dict:
        root = Path(source_root).resolve(strict=True)
        events = self.connector.events(root, repo_id)
        parsed = []
        rejected = []
        for event in events:
            self.capture.capture(event)
            source = event.payload["content"]
            result = self.parser.parse(repo_id, event.payload["path"], source)
            if result.parse_errors:
                rejected.append({"event_id": event.event_id, "path": result.path, "errors": result.parse_errors})
                self._write_dlq(event, result.parse_errors)
            else:
                parsed.append((event, result))

        run_id = __import__("uuid").uuid4().hex
        started_at = utc_now_iso()
        run = self.store.upsert_vertex(
            "IngestionRun",
            {
                "canonical_id": f"urn:eoip:meta:ingestion-run:{run_id}",
                "run_status": "PARTIAL" if rejected else "SUCCEEDED",
                "run_kind": "LOCAL_CODE",
                "source_system": "git",
                "ingestion_run_id": run_id,
                "started_at": started_at,
                "finished_at": utc_now_iso(),
                "counts": json.dumps({"files": len(parsed), "rejected": len(rejected)}, sort_keys=True),
                "ontology_version": ONTOLOGY_VERSION,
                "schema_version": SCHEMA_VERSION,
            },
        )
        root_name = root.name or "repository"
        repository = self.store.upsert_vertex(
            "Repository",
            {
                "canonical_id": f"urn:eoip:code:repository:{repo_id}",
                "repo_id": repo_id,
                "name": root_name,
                "source_system": "git",
                "source_id": repo_id,
                "source_uri": f"file:///{root_name}",
                "ontology_version": ONTOLOGY_VERSION,
                "schema_version": SCHEMA_VERSION,
                "ingestion_run_id": run_id,
                "first_seen": started_at,
                "last_seen": started_at,
                "valid_from": started_at,
            },
        )
        self.store.upsert_edge(
            "INGESTED_IN",
            repository["vid"],
            run["vid"],
            {"fact_key": f"code-repository-run:{run_id}:{repo_id}", "ingestion_run_id": run_id},
        )
        counts = {"files": 0, "symbols": 0, "dependencies": 0, "calls": 0}
        for event, parsed_file in parsed:
            now = event.captured_at
            file_cid = f"urn:eoip:code:file:{repo_id}:{parsed_file.path}"
            evidence_cid = f"urn:eoip:evidence:source-event:git:{event.event_id}"
            shared = {
                "source_system": "git",
                "source_id": event.source_record_id,
                "source_version": event.source_version,
                "parser_version": PARSER_VERSION,
                "ontology_version": ONTOLOGY_VERSION,
                "schema_version": SCHEMA_VERSION,
                "ingestion_run_id": run_id,
                "first_seen": now,
                "last_seen": now,
                "valid_from": now,
            }
            file_vertex = self.store.upsert_vertex(
                "File",
                {
                    **shared,
                    "canonical_id": file_cid,
                    "repo_id": repo_id,
                    "path": parsed_file.path,
                    "name": Path(parsed_file.path).name,
                    "language": parsed_file.language,
                    "content_hash": parsed_file.content_hash,
                },
            )
            evidence = self.store.upsert_vertex(
                "Evidence",
                {
                    "canonical_id": evidence_cid,
                    "source_system": "git",
                    "source_ref": f"git://{repo_id}/{parsed_file.path}",
                    "source_id": event.source_record_id,
                    "source_version": event.source_version,
                    "method": "TREE_SITTER_AST",
                    "captured_at": now,
                    "evidence_key": event.event_id,
                    "content_hash": event.payload_hash,
                    "parser_version": PARSER_VERSION,
                    "ontology_version": ONTOLOGY_VERSION,
                    "schema_version": SCHEMA_VERSION,
                },
            )
            evidence_props = {
                "evidence_key": event.event_id,
                "source_ref": evidence["properties"]["source_ref"],
                "source_system": "git",
                "ingestion_run_id": run_id,
                "creation_status": "DETERMINISTIC",
            }
            self.store.upsert_edge(
                "CONTAINS",
                repository["vid"],
                file_vertex["vid"],
                {"fact_key": f"repository-file:{repo_id}:{parsed_file.path}", **evidence_props},
            )
            self.store.upsert_edge(
                "EVIDENCED_BY",
                file_vertex["vid"],
                evidence["vid"],
                {"fact_key": f"file-evidence:{event.event_id}", **evidence_props},
            )
            self.store.upsert_edge(
                "INGESTED_IN",
                file_vertex["vid"],
                run["vid"],
                {"fact_key": f"code-file-run:{run_id}:{parsed_file.path}", **evidence_props},
            )
            counts["files"] += 1
            symbol_vertices = {}
            for symbol in parsed_file.symbols:
                symbol_vertex = self.store.upsert_vertex(
                    "CodeSymbol",
                    {
                        **shared,
                        "canonical_id": symbol.canonical_id,
                        "name": symbol.name,
                        "qualified_name": symbol.qualified_name,
                        "symbol_kind": symbol.kind,
                        "repo_id": repo_id,
                        "path": parsed_file.path,
                        "start_line": symbol.start_line,
                        "end_line": symbol.end_line,
                        "start_column": symbol.start_column,
                        "end_column": symbol.end_column,
                        "language": parsed_file.language,
                    },
                )
                symbol_vertices[symbol.canonical_id] = symbol_vertex
                self.store.upsert_edge(
                    "DECLARES",
                    file_vertex["vid"],
                    symbol_vertex["vid"],
                    {"fact_key": f"declares:{symbol.canonical_id}", **evidence_props},
                )
                self.store.upsert_edge(
                    "EVIDENCED_BY",
                    symbol_vertex["vid"],
                    evidence["vid"],
                    {"fact_key": f"symbol-evidence:{symbol.canonical_id}:{event.event_id}", **evidence_props},
                )
                self.store.upsert_edge(
                    "INGESTED_IN",
                    symbol_vertex["vid"],
                    run["vid"],
                    {"fact_key": f"code-symbol-run:{run_id}:{symbol.canonical_id}", **evidence_props},
                )
                counts["symbols"] += 1
            dependency_vertices = {}
            for imported_module in parsed_file.imports:
                dependency_cid = f"urn:eoip:code:dependency:{parsed_file.language}:{imported_module}"
                dependency = self.store.upsert_vertex(
                    "Dependency",
                    {
                        **shared,
                        "canonical_id": dependency_cid,
                        "name": imported_module,
                        "language": parsed_file.language,
                        "resolved": False,
                    },
                )
                dependency_vertices[dependency_cid] = dependency
                self.store.upsert_edge(
                    "IMPORTS",
                    file_vertex["vid"],
                    dependency["vid"],
                    {"fact_key": f"imports:{parsed_file.path}:{imported_module}", **evidence_props},
                )
                self.store.upsert_edge(
                    "EVIDENCED_BY",
                    dependency["vid"],
                    evidence["vid"],
                    {
                        "fact_key": f"dependency-evidence:{event.event_id}:{dependency_cid}",
                        **evidence_props,
                    },
                )
                self.store.upsert_edge(
                    "INGESTED_IN",
                    dependency["vid"],
                    run["vid"],
                    {"fact_key": f"code-dependency-run:{run_id}:{dependency_cid}", **evidence_props},
                )
                counts["dependencies"] += 1
            for call in parsed_file.calls:
                caller = symbol_vertices.get(call.caller_id) or self.store.get_vertex_by_canonical_id(call.caller_id)
                callee = symbol_vertices.get(call.target_id) or self.store.get_vertex_by_canonical_id(call.target_id)
                if caller is None or callee is None:
                    continue
                self.store.upsert_edge(
                    "CALLS",
                    caller["vid"],
                    callee["vid"],
                    {"fact_key": f"calls:{call.caller_id}:{call.target_id}", **evidence_props},
                )
                counts["calls"] += 1
        return {
            "run_id": run_id,
            "run_status": "PARTIAL" if rejected else "SUCCEEDED",
            "counts": counts,
            "rejected": rejected,
        }

    def _write_dlq(self, event, errors: list[str]) -> None:
        self.dlq_root.mkdir(parents=True, exist_ok=True)
        record = {
            "event_id": event.event_id,
            "source_system": event.source_system,
            "source_record_id": event.source_record_id,
            "payload_hash": event.payload_hash,
            "errors": errors,
        }
        destination = self.dlq_root / f"{event.event_id}.json"
        if not destination.exists():
            destination.write_text(json.dumps(record, sort_keys=True, indent=2), encoding="utf-8")
