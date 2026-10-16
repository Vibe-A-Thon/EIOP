"""Capture-first file ingestion with RAG/graph exports and source-event evidence."""

from __future__ import annotations

import base64
import binascii
import hashlib
import json
import logging
import re
from pathlib import Path
from uuid import uuid4

from eoip.connectors.config import connector_from_registry
from eoip.connectors.files import file_event
from eoip.contracts.source_event import SourceEventV2, utc_now_iso
from eoip.fileparse.contracts import PARSER_VERSION, ParseError, ParseOptions, ParseResult
from eoip.fileparse.engine import FileParser
from eoip.fileparse.export import export_bundle, graph_data
from eoip.graph.store import GraphStore
from eoip.ingestion.dlq import write_dlq_record
from eoip.ingestion.jira import FileEventCapture
from eoip.ingestion.pipeline import IngestionGraphStore
from eoip.jobs import write_json
from eoip.ontology.manifest import ONTOLOGY_VERSION, SCHEMA_VERSION

logger = logging.getLogger(__name__)


class FileIngestionService:
    def __init__(self, store: GraphStore, root: str | Path, parser: FileParser | None = None) -> None:
        self.store = IngestionGraphStore(store)
        self.root = Path(root)
        self.parser = parser or FileParser()
        self.capture = FileEventCapture(self.root / "raw")

    def ingest(
        self, content: bytes, filename: str, *, source_id: str = "file_upload", dry_run: bool = False,
        correlation_id: str | None = None,
    ) -> dict:
        return self.ingest_event(
            file_event(content, filename, source_id), dry_run=dry_run, correlation_id=correlation_id,
        )

    def ingest_event(self, event: SourceEventV2, *, dry_run: bool = False, correlation_id: str | None = None) -> dict:
        run_id = str(uuid4())
        captured = None
        if event.source_system != "documents" or event.source_record_type != "binary_file":
            raise ParseError("invalid_event", "Expected a documents/binary_file source event")
        payload = event.payload or {}
        encoded = payload.get("content")
        filename = payload.get("filename")
        if not isinstance(encoded, str) or not isinstance(filename, str) or payload.get("encoding") != "base64":
            raise ParseError("invalid_event", "Binary file event requires filename and base64 content")
        if len(encoded) > 4 * ((self.parser.options.max_file_bytes + 2) // 3):
            raise ParseError("size_limit", "Source event exceeds max_file_bytes")
        try:
            content = base64.b64decode(encoded, validate=True)
        except (ValueError, binascii.Error) as exc:
            raise ParseError("invalid_event", "Invalid base64 source event") from exc
        if len(content) > self.parser.options.max_file_bytes:
            raise ParseError("size_limit", "Source event exceeds max_file_bytes")
        expected = file_event(content, filename, event.source_instance_id, source_uri=event.source_record_id)
        if expected.event_id != event.event_id or hashlib.sha256(content).hexdigest() != event.content_hash:
            raise ParseError("hash_mismatch", "Source event identity/content hash does not match the actual file")
        if not dry_run:
            captured = self.capture.capture(event)
        try:
            result = self.parser.parse_bytes(
                content, filename, source_id=event.source_instance_id, source_uri=event.source_record_id,
            )
            if not dry_run and result.errors:
                self._reject(event, run_id, "container_member_error", "One or more container members failed",
                             captured, correlation_id)
        except ParseError as exc:
            if not dry_run:
                self._reject(event, run_id, exc.code, str(exc), captured, correlation_id)
            raise
        destination = self.root / "fileparse" / run_id
        manifest = None
        if not dry_run:
            manifest = export_bundle(result, destination, vectors=True)
            try:
                self._write_graph(event, result, run_id)
            except (ValueError, TypeError, OSError, RuntimeError) as exc:
                self._reject(event, run_id, "graph_write_error", "File graph ingestion failed", captured, correlation_id)
                logger.error("File graph ingestion failed", extra={"run_id": run_id, "error_type": type(exc).__name__})
                raise
        return {
            "run_id": run_id, "run_status": "DRY_RUN" if dry_run else result.status,
            "event_id": event.event_id, "documents": len(result.documents), "chunks": len(result.chunks),
            "bundle_id": None if dry_run else run_id, "manifest": manifest,
            "result": result.model_dump(mode="json"),
        }

    def _reject(self, event, run_id, code, message, captured, correlation_id):
        write_dlq_record(
            self.root / "dlq", event, message, stage="file_parsing", error_category=code,
            run_id=run_id, correlation_id=correlation_id, replay_ref=str(captured) if captured else None,
        )
        logger.warning("File ingestion rejected", extra={"event_id": event.event_id, "error_category": code})

    def _write_graph(self, event: SourceEventV2, result: ParseResult, run_id: str) -> None:
        self.store.begin_run(run_id)
        common = {
            "source_system": "documents", "source_id": event.source_instance_id,
            "source_version": event.content_hash, "mapper_version": PARSER_VERSION,
            "ontology_version": ONTOLOGY_VERSION, "schema_version": SCHEMA_VERSION,
            "ingestion_run_id": run_id, "creation_status": "DETERMINISTIC",
            "source_ref": event.source_record_id,
        }
        run = self.store.upsert_vertex("IngestionRun", {
            "canonical_id": f"urn:eoip:meta:ingestion-run:{run_id}", "run_status": result.status,
            "run_kind": "FILE_PARSING", "source_system": "documents", "started_at": event.captured_at,
            "finished_at": utc_now_iso(), "ingestion_run_id": run_id,
        })
        evidence = self.store.upsert_vertex("Evidence", {
            **common, "canonical_id": f"urn:eoip:evidence:source-event:documents:{event.event_id}",
            "evidence_key": event.event_id, "content_hash": event.content_hash,
            "method": "SOURCE_EVENT", "captured_at": event.captured_at,
        })
        projected = graph_data(result)
        for entity in projected["entities"]:
            properties = {key: value for key, value in entity.items() if key != "entity_type"}
            vertex = self.store.upsert_vertex(entity["entity_type"], {**common, **properties})
            self.store.upsert_edge("EVIDENCED_BY", vertex["vid"], evidence["vid"], common)
            self.store.upsert_edge("INGESTED_IN", vertex["vid"], run["vid"], common)
        for relationship in projected["relationships"]:
            source = self.store.get_vertex_by_canonical_id(relationship["from_id"])
            target = self.store.get_vertex_by_canonical_id(relationship["to_id"])
            if source is None or target is None:
                raise RuntimeError("File graph relationship has a missing endpoint")
            self.store.upsert_edge(
                relationship["type"], source["vid"], target["vid"],
                {**common, **relationship["properties"]},
            )


def run_registered_file_operation(entry, payload, store: GraphStore, data_root: str, correlation_id: str) -> dict:
    operation = payload.get("operation")
    if operation not in {"BASELINE", "POLL", "REPLAY"}:
        raise ValueError(f"Unsupported file source operation: {operation}")
    root = Path(data_root)
    connector = connector_from_registry(entry, correlation_id=correlation_id)
    parser = FileParser(ParseOptions.model_validate(entry.config.get("parse_options", {})))
    service = FileIngestionService(store, root, parser)
    checkpoint_path = root / "state" / "connectors" / f"{entry.source_id}.json"
    checkpoint_state = json.loads(checkpoint_path.read_text(encoding="utf-8")) if checkpoint_path.exists() else {}
    checkpoint = payload.get("checkpoint") or checkpoint_state.get("checkpoint") or entry.checkpoint or ""
    next_checkpoint = utc_now_iso()
    if operation == "REPLAY":
        event_ids = payload.get("event_ids")
        if not event_ids:
            raise ValueError("event_ids are required for replay")
        events = []
        for event_id in dict.fromkeys(event_ids):
            if not isinstance(event_id, str) or not re.fullmatch(r"[a-f0-9]{64}", event_id):
                raise ValueError("replay event IDs must be lowercase SHA-256 values")
            path = root / "raw" / "documents" / f"{event_id}.json"
            if not path.is_file():
                raise ValueError(f"captured source event is unavailable: {event_id}")
            event = SourceEventV2.model_validate_json(path.read_text(encoding="utf-8"))
            if event.event_id != event_id or event.source_instance_id != entry.source_id:
                raise ValueError("captured source event identity or source instance mismatch")
            events.append(event)
    else:
        events = connector.baseline() if operation == "BASELINE" else connector.poll_changes(checkpoint)
    outcomes = []
    rejected = []
    for event in events:
        try:
            outcome = service.ingest_event(
                event, dry_run=payload.get("dry_run", False), correlation_id=correlation_id,
            )
        except ParseError as exc:
            outcome = {"run_status": "FAILED", "event_id": event.event_id,
                       "error": {"code": exc.code, "message": str(exc)}}
        outcomes.append(outcome)
        if outcome["run_status"] not in {"SUCCEEDED", "DRY_RUN"}:
            rejected.append({"event_id": event.event_id, "source_record_id": event.source_record_id,
                             "error": outcome.get("error") or outcome["result"]["errors"]})
    succeeded = all(item["run_status"] in {"SUCCEEDED", "DRY_RUN"} for item in outcomes)
    if succeeded and operation != "REPLAY" and not payload.get("dry_run", False):
        write_json(checkpoint_path, {
            "schema_version": "1.0", "source_system": "documents", "source_id": entry.source_id,
            "checkpoint": next_checkpoint, "operation": operation,
            "baseline_complete": operation == "BASELINE" or checkpoint_state.get("baseline_complete", False),
            "updated_at": next_checkpoint,
        })
    return {
        "run_status": "DRY_RUN" if payload.get("dry_run", False) else ("SUCCEEDED" if succeeded else "PARTIAL"),
        "source_id": entry.source_id, "operation": operation,
        "next_checkpoint": checkpoint if operation == "REPLAY" else next_checkpoint,
        "records_seen": len(outcomes), "records_accepted": sum(
            item["run_status"] in {"SUCCEEDED", "DRY_RUN"} for item in outcomes
        ), "records_rejected": len(rejected), "rejected": rejected, "results": outcomes,
    }
