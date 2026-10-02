"""Capture-first graph ingestion for REST SourceEvent batches."""

from __future__ import annotations

import json
import logging
from typing import Any
from urllib.parse import urljoin
from uuid import uuid4

from eoip.connectors.confluence import ConfluenceConnector
from eoip.connectors.servicenow import ServiceNowConnector
from eoip.connectors.sync import SyncBatch
from eoip.contracts.source_event import SourceEvent, utc_now_iso
from eoip.graph.store import GraphStore
from eoip.ingestion.jira import FileEventCapture
from eoip.jobs import write_json
from eoip.ontology.manifest import ONTOLOGY_VERSION, SCHEMA_VERSION

logger = logging.getLogger(__name__)


class SourceSyncIngestionService:
    def __init__(
        self,
        store: GraphStore,
        connector: ConfluenceConnector | ServiceNowConnector,
        capture: FileEventCapture,
        dlq_root: str,
    ) -> None:
        self.store = store
        self.connector = connector
        self.capture = capture
        self.dlq_root = dlq_root

    def sync(
        self,
        *,
        checkpoint: str | None = None,
        watermark: str | None = None,
        dry_run: bool = False,
        correlation_id: str | None = None,
    ) -> dict:
        batch = self.connector.sync(
            checkpoint=checkpoint, watermark=watermark, correlation_id=correlation_id
        )
        return self.ingest(batch, dry_run=dry_run, correlation_id=correlation_id)

    def ingest(
        self,
        batch: SyncBatch,
        *,
        dry_run: bool = False,
        correlation_id: str | None = None,
    ) -> dict:
        run_id = str(uuid4())
        correlation_id = correlation_id or str(uuid4())
        started_at = utc_now_iso()
        accepted: list[tuple[SourceEvent, dict[str, Any]]] = []
        rejected: list[dict[str, str]] = []

        # Capture every source record before any canonical graph mutation.
        for event in batch.events:
            if not dry_run:
                self.capture.capture(event)
            try:
                accepted.append((event, self._map_event(event)))
            except (ValueError, TypeError, KeyError) as exc:
                rejected.append(
                    {
                        "event_id": event.event_id,
                        "source_record_id": event.source_record_id,
                        "error_category": "mapping_error",
                        "error": str(exc),
                    }
                )
                if not dry_run:
                    self._write_dlq(event, str(exc), correlation_id)
                    logger.warning(
                        "source record mapping failed",
                        extra={
                            "event": "source.record.mapping_failed",
                            "operation": "ingestion",
                            "correlation_id": correlation_id,
                            "source_system": event.source_system,
                            "error_category": "mapping_error",
                            "event_id": event.event_id,
                        },
                    )

        if not dry_run:
            self._write_graph(accepted, run_id, started_at, len(rejected))
        return {
            "run_id": run_id,
            "run_status": "DRY_RUN" if dry_run else ("PARTIAL" if rejected else "SUCCEEDED"),
            "records_seen": len(batch.events),
            "records_accepted": len(accepted),
            "records_rejected": len(rejected),
            "rejected": rejected,
            "next_checkpoint": batch.next_checkpoint,
            "correlation_id": correlation_id,
        }

    def _map_event(self, event: SourceEvent) -> dict[str, Any]:
        mapped = self.connector.map_event(event)
        source = event.source_system
        instance = (event.metadata or {}).get("source_instance_id", "default")
        identity = event.source_record_id
        if source == "servicenow":
            if mapped["kind"] == "knowledge":
                label = "Document"
                canonical_id = f"urn:eoip:knowledge:document:servicenow:{identity}"
                properties = {
                    "name": mapped["short_description"] or mapped["number"],
                    "path": f"servicenow://knowledge/{mapped['number']}",
                    "doc_format": "servicenow-knowledge",
                    "content_hash": event.payload_hash,
                    "description": mapped["description"],
                    "modified_at": mapped["updated_at"] or event.captured_at,
                }
                source_ref = properties["path"]
            else:
                label = "WorkItem"
                canonical_id = f"urn:eoip:work:item:servicenow:{identity}"
                properties = {
                    "issue_key": mapped["number"],
                    "summary": mapped["short_description"] or mapped["number"],
                    "description": mapped["description"],
                    "issue_type": mapped["kind"],
                    "status": mapped["state"],
                    "modified_at": mapped["updated_at"] or event.captured_at,
                }
                source_ref = f"servicenow://{mapped['kind']}/{mapped['number']}"
            parents: list[str] = []
        else:
            kind = mapped["kind"]
            if kind == "space":
                label = "KnowledgeSpace"
                canonical_id = f"urn:eoip:knowledge:space:{identity}"
                properties = {
                    "name": mapped["name"],
                    "space_key": mapped["space_key"],
                    "description": mapped["description"],
                }
                source_ref = f"confluence://space/{mapped['space_key']}"
                parents = []
            elif kind in {"page", "attachment"}:
                label = "Document"
                canonical_id = f"urn:eoip:knowledge:document:{identity}"
                if kind == "page":
                    content = mapped["body"]
                    if content is not None and not isinstance(content, str):
                        raise ValueError("Confluence page body must be text")
                    source_ref = (
                        urljoin(self.connector.base_url + "/", mapped["url"].lstrip("/"))
                        if mapped["url"]
                        else f"confluence://{mapped['space_key']}/page/{mapped['content_id']}"
                    )
                    properties = {
                        "name": mapped["title"],
                        "path": source_ref,
                        "doc_format": "confluence-storage",
                        "content_hash": event.payload_hash,
                        "description": content,
                        "modified_at": mapped["updated_at"] or event.captured_at,
                    }
                    parents = [
                        f"urn:eoip:knowledge:document:{instance}:page:{parent_id}"
                        for parent_id in mapped["parent_ids"]
                    ]
                else:
                    source_ref = (
                        f"confluence://{mapped['space_key']}/attachment/{mapped['content_id']}"
                    )
                    file_size = mapped["file_size"]
                    if file_size is not None:
                        try:
                            file_size = int(file_size)
                        except (TypeError, ValueError) as exc:
                            raise ValueError("Confluence attachment file size must be an integer") from exc
                    properties = {
                        "name": mapped["filename"],
                        "path": source_ref,
                        "doc_format": "attachment",
                        "content_hash": event.payload_hash,
                        "media_type": mapped["media_type"],
                        "file_size": file_size,
                    }
                    parents = [
                        f"urn:eoip:knowledge:document:{instance}:page:{mapped['page_id']}"
                    ]
            else:
                raise ValueError("unsupported Confluence record kind")
            if kind in {"page", "attachment"}:
                parents.append(
                    f"urn:eoip:knowledge:space:{instance}:space:{mapped['space_key']}"
                )

        return {
            "label": label,
            "canonical_id": canonical_id,
            "properties": properties,
            "source_ref": source_ref,
            "parents": parents,
        }

    def _write_graph(
        self,
        accepted: list[tuple[SourceEvent, dict[str, Any]]],
        run_id: str,
        started_at: str,
        rejected_count: int,
    ) -> None:
        source_system = self.connector.source_system
        run = self.store.upsert_vertex(
            "IngestionRun",
            {
                "canonical_id": f"urn:eoip:meta:ingestion-run:{run_id}",
                "run_status": "PARTIAL" if rejected_count else "SUCCEEDED",
                "run_kind": source_system.upper(),
                "source_system": source_system,
                "ingestion_run_id": run_id,
                "started_at": started_at,
                "finished_at": utc_now_iso(),
                "counts": json.dumps(
                    {"accepted": len(accepted), "rejected": rejected_count}, sort_keys=True
                ),
                "ontology_version": ONTOLOGY_VERSION,
                "schema_version": SCHEMA_VERSION,
            },
        )
        run_edge_props = {
            "ingestion_run_id": run_id,
            "source_system": source_system,
            "creation_status": "DETERMINISTIC",
        }
        nodes_by_cid: dict[str, dict] = {}
        records = []
        for event, mapped in accepted:
            existing = self.store.get_vertex_by_canonical_id(mapped["canonical_id"])
            shared = {
                "source_system": source_system,
                "source_id": event.source_record_id,
                "source_version": event.source_version,
                "mapper_version": self.connector.mapper_version,
                "ontology_version": ONTOLOGY_VERSION,
                "schema_version": SCHEMA_VERSION,
                "ingestion_run_id": run_id,
                "first_seen": (
                    existing["properties"].get("first_seen", event.captured_at)
                    if existing
                    else event.captured_at
                ),
                "last_seen": event.captured_at,
                "valid_from": event.captured_at,
                "modified_at": event.captured_at,
            }
            node = self.store.upsert_vertex(
                mapped["label"],
                {**shared, **mapped["properties"], "canonical_id": mapped["canonical_id"]},
            )
            evidence = self.store.upsert_vertex(
                "Evidence",
                {
                    "canonical_id": (
                        f"urn:eoip:evidence:source-event:{source_system}:{event.event_id}"
                    ),
                    "source_system": source_system,
                    "source_ref": mapped["source_ref"],
                    "source_id": event.source_record_id,
                    "source_version": event.source_version,
                    "method": "SOURCE_EVENT",
                    "captured_at": event.captured_at,
                    "evidence_key": event.event_id,
                    "content_hash": event.payload_hash,
                    "mapper_version": self.connector.mapper_version,
                    "ontology_version": ONTOLOGY_VERSION,
                    "schema_version": SCHEMA_VERSION,
                },
            )
            evidence_props = {
                "fact_key": f"source-event:{event.event_id}",
                "evidence_key": event.event_id,
                "source_ref": mapped["source_ref"],
                **run_edge_props,
            }
            self.store.upsert_edge("EVIDENCED_BY", node["vid"], evidence["vid"], evidence_props)
            self.store.upsert_edge(
                "INGESTED_IN",
                node["vid"],
                run["vid"],
                {
                    "fact_key": f"source-run:{run_id}:{mapped['canonical_id']}",
                    **run_edge_props,
                },
            )
            nodes_by_cid[mapped["canonical_id"]] = node
            records.append((event, mapped, evidence_props))

        for _event, mapped, edge_properties in records:
            for parent_cid in mapped["parents"]:
                parent = nodes_by_cid.get(parent_cid) or self.store.get_vertex_by_canonical_id(
                    parent_cid
                )
                if parent is not None:
                    self.store.upsert_edge(
                        "CONTAINS",
                        parent["vid"],
                        nodes_by_cid[mapped["canonical_id"]]["vid"],
                        {
                            **edge_properties,
                            "fact_key": (
                                f"source-contains:{parent_cid}:{mapped['canonical_id']}"
                            ),
                        },
                    )

    def _write_dlq(self, event: SourceEvent, error: str, correlation_id: str) -> None:
        from pathlib import Path

        root = Path(self.dlq_root)
        root.mkdir(parents=True, exist_ok=True)
        destination = root / f"{event.event_id}.json"
        if destination.exists():
            return
        destination.write_text(
            json.dumps(
                {
                    "event_id": event.event_id,
                    "source_system": event.source_system,
                    "source_record_id": event.source_record_id,
                    "payload_hash": event.payload_hash,
                    "error_category": "mapping_error",
                    "error": error,
                    "correlation_id": correlation_id,
                    "replay_ref": str(
                        self.capture.root / event.source_system / f"{event.event_id}.json"
                    ),
                },
                sort_keys=True,
                indent=2,
            ),
            encoding="utf-8",
        )


def run_configured_source_sync(
    source_system: str,
    payload: dict[str, Any],
    store: GraphStore,
    data_root: str,
    correlation_id: str,
) -> dict:
    from pathlib import Path

    from eoip.connectors.config import connector_from_environment

    connector = connector_from_environment(source_system, correlation_id=correlation_id)
    try:
        root = Path(data_root)
        checkpoint_path = root / "state" / "connectors" / f"{source_system}.json"
        checkpoint_state = (
            json.loads(checkpoint_path.read_text(encoding="utf-8"))
            if checkpoint_path.exists()
            else {}
        )
        service = SourceSyncIngestionService(
            store, connector, FileEventCapture(root / "raw"), str(root / "dlq")
        )
        result = service.sync(
            checkpoint=payload.get("checkpoint") or checkpoint_state.get("checkpoint"),
            watermark=payload.get("watermark"),
            dry_run=payload.get("dry_run", False),
            correlation_id=correlation_id,
        )
        if result["run_status"] == "SUCCEEDED" and not payload.get("dry_run", False):
            write_json(
                checkpoint_path,
                {
                    "checkpoint": result["next_checkpoint"],
                    "updated_at": utc_now_iso(),
                    "source_system": source_system,
                },
            )
        return result
    finally:
        connector.close()
