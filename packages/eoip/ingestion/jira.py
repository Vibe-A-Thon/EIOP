"""Capture-first Jira ingestion into the canonical graph model."""

from __future__ import annotations

import json
import os
from pathlib import Path
from threading import Lock
from uuid import uuid4

from eoip.connectors.jira_json import JiraJsonConnector
from eoip.contracts.source_event import SourceEvent, utc_now_iso
from eoip.graph.store import GraphStore
from eoip.ontology.manifest import ONTOLOGY_VERSION, SCHEMA_VERSION


class FileEventCapture:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self._lock = Lock()

    def capture(self, event: SourceEvent) -> Path:
        event_dir = self.root / event.source_system
        event_dir.mkdir(parents=True, exist_ok=True)
        destination = event_dir / f"{event.event_id}.json"
        serialized = json.dumps(event.model_dump(mode="json"), sort_keys=True, ensure_ascii=False, indent=2)
        with self._lock:
            try:
                with destination.open("x", encoding="utf-8") as raw_file:
                    raw_file.write(serialized)
                    raw_file.flush()
                    os.fsync(raw_file.fileno())
            except FileExistsError:
                existing = json.loads(destination.read_text(encoding="utf-8"))
                if existing.get("payload_hash") != event.payload_hash:
                    raise RuntimeError("captured event ID conflicts with existing immutable payload")
        return destination


class JiraIngestionService:
    def __init__(
        self,
        store: GraphStore,
        connector: JiraJsonConnector,
        capture: FileEventCapture,
        dlq_root: str | Path,
    ) -> None:
        self.store = store
        self.connector = connector
        self.capture = capture
        self.dlq_root = Path(dlq_root)

    def ingest(self, document: object, *, dry_run: bool = False) -> dict:
        records = self.connector.source_records(document)
        events = self.connector.events(records)
        run_id = str(uuid4())
        started_at = utc_now_iso()
        accepted = []
        rejected = []

        for event in events:
            try:
                mapped = self.connector.map_event(event)
                if not dry_run:
                    self.capture.capture(event)
                accepted.append((event, mapped))
            except (ValueError, TypeError) as exc:
                rejected.append({"event_id": event.event_id, "source_record_id": event.source_record_id, "error": str(exc)})
                if not dry_run:
                    self.capture.capture(event)
                    self._write_dlq(event, str(exc))

        if not dry_run:
            self._write_graph(accepted, run_id, started_at, len(rejected))
        return {
            "run_id": run_id,
            "run_status": "DRY_RUN" if dry_run else ("PARTIAL" if rejected else "SUCCEEDED"),
            "records_seen": len(events),
            "records_accepted": len(accepted),
            "records_rejected": len(rejected),
            "rejected": rejected,
        }

    def _write_graph(self, accepted: list[tuple[SourceEvent, dict]], run_id: str, started_at: str, rejected_count: int) -> None:
        run_cid = f"urn:eoip:meta:ingestion-run:{run_id}"
        run = self.store.upsert_vertex(
            "IngestionRun",
            {
                "canonical_id": run_cid,
                "run_status": "PARTIAL" if rejected_count else "SUCCEEDED",
                "run_kind": "JIRA_JSON",
                "source_system": "jira",
                "ingestion_run_id": run_id,
                "started_at": started_at,
                "finished_at": utc_now_iso(),
                "counts": json.dumps({"accepted": len(accepted), "rejected": rejected_count}, sort_keys=True),
                "ontology_version": ONTOLOGY_VERSION,
                "schema_version": SCHEMA_VERSION,
            },
        )
        run_edge_props = {"ingestion_run_id": run_id, "creation_status": "DETERMINISTIC"}
        records = []
        for event, issue in accepted:
            project_cid = f"urn:eoip:work:project:jira:{issue['project_key']}"
            work_item_cid = f"urn:eoip:work:item:jira:{issue['issue_key']}"
            evidence_cid = f"urn:eoip:evidence:source-event:jira:{event.event_id}"
            shared = {
                "source_system": "jira",
                "source_id": event.source_record_id,
                "source_version": event.source_version,
                "mapper_version": self.connector.mapper_version,
                "ontology_version": ONTOLOGY_VERSION,
                "schema_version": SCHEMA_VERSION,
                "ingestion_run_id": run_id,
                "first_seen": event.captured_at,
                "last_seen": event.captured_at,
                "valid_from": event.captured_at,
                "modified_at": event.captured_at,
            }
            project = self.store.upsert_vertex(
                "Project",
                {
                    **shared,
                    "canonical_id": project_cid,
                    "name": issue["project_name"],
                    "issue_key": issue["project_key"],
                },
            )
            work_item = self.store.upsert_vertex(
                "WorkItem",
                {
                    **shared,
                    "canonical_id": work_item_cid,
                    "issue_key": issue["issue_key"],
                    "summary": issue["summary"],
                    "description": issue["description"],
                    "issue_type": issue["issue_type"],
                    "status": issue["status"],
                },
            )
            evidence = self.store.upsert_vertex(
                "Evidence",
                {
                    "canonical_id": evidence_cid,
                    "source_system": "jira",
                    "source_ref": f"jira://issue/{issue['issue_key']}",
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
            self.store.upsert_edge(
                "EVIDENCED_BY",
                project["vid"],
                evidence["vid"],
                {
                    "fact_key": f"jira-project-evidence:{event.event_id}:{issue['project_key']}",
                    "evidence_key": event.event_id,
                    "source_ref": evidence["properties"]["source_ref"],
                    "source_system": "jira",
                    **run_edge_props,
                },
            )
            self.store.upsert_edge(
                "INGESTED_IN",
                project["vid"],
                run["vid"],
                {"fact_key": f"jira-project-run:{run_id}:{issue['project_key']}", **run_edge_props},
            )
            person = None
            if issue["assignee_name"]:
                identity = issue["assignee_id"] or issue["assignee_email"] or f"{event.source_record_id}:{issue['assignee_name']}"
                person_key = str(identity).strip().casefold()
                person = self.store.upsert_vertex(
                    "Person",
                    {
                        **shared,
                        "canonical_id": f"urn:eoip:identity:person:jira:{person_key}",
                        "display_name": issue["assignee_name"],
                        "email": issue["assignee_email"],
                    },
                )
                self.store.upsert_edge(
                    "EVIDENCED_BY",
                    person["vid"],
                    evidence["vid"],
                    {
                        "fact_key": f"person-evidence:{event.event_id}:{person_key}",
                        "evidence_key": event.event_id,
                        "source_ref": evidence["properties"]["source_ref"],
                        "source_system": "jira",
                        **run_edge_props,
                    },
                )
                self.store.upsert_edge(
                    "INGESTED_IN",
                    person["vid"],
                    run["vid"],
                    {"fact_key": f"person-run:{run_id}:{person_key}", **run_edge_props},
                )
            records.append({"event": event, "issue": issue, "project": project, "work_item": work_item, "evidence": evidence, "person": person})

        work_items = {item["issue"]["issue_key"]: item["work_item"] for item in records}
        for item in records:
            event = item["event"]
            issue = item["issue"]
            project = item["project"]
            work_item = item["work_item"]
            evidence = item["evidence"]
            self.store.upsert_edge(
                "CONTAINS",
                project["vid"],
                work_item["vid"],
                {"fact_key": f"jira-project-contains:{issue['issue_key']}", **run_edge_props},
            )
            self.store.upsert_edge(
                "EVIDENCED_BY",
                work_item["vid"],
                evidence["vid"],
                {
                    "fact_key": f"source-event:{event.event_id}",
                    "evidence_key": event.event_id,
                    "source_ref": evidence["properties"]["source_ref"],
                    "source_system": "jira",
                    **run_edge_props,
                },
            )
            if item["person"] is not None:
                self.store.upsert_edge(
                    "ASSIGNED_TO",
                    work_item["vid"],
                    item["person"]["vid"],
                    {
                        "fact_key": f"jira-assigned-to:{issue['issue_key']}:{item['person']['canonical_id']}",
                        "evidence_key": event.event_id,
                        "source_ref": evidence["properties"]["source_ref"],
                        "source_system": "jira",
                        **run_edge_props,
                    },
                )
            if issue["parent_key"]:
                parent = work_items.get(issue["parent_key"]) or self.store.get_vertex_by_canonical_id(
                    f"urn:eoip:work:item:jira:{issue['parent_key']}"
                )
                if parent is not None:
                    self.store.upsert_edge(
                        "PARENT_OF",
                        parent["vid"],
                        work_item["vid"],
                        {
                            "fact_key": f"jira-parent-of:{issue['parent_key']}:{issue['issue_key']}",
                            "evidence_key": event.event_id,
                            "source_ref": evidence["properties"]["source_ref"],
                            "source_system": "jira",
                            **run_edge_props,
                        },
                    )
            self.store.upsert_edge(
                "INGESTED_IN",
                work_item["vid"],
                run["vid"],
                {"fact_key": f"run:{run_id}:{issue['issue_key']}", **run_edge_props},
            )

    def _write_dlq(self, event: SourceEvent, error: str) -> None:
        self.dlq_root.mkdir(parents=True, exist_ok=True)
        destination = self.dlq_root / f"{event.event_id}.json"
        record = {
            "event_id": event.event_id,
            "source_system": event.source_system,
            "source_record_id": event.source_record_id,
            "payload_hash": event.payload_hash,
            "error": error,
            "replay_ref": str(self.capture.root / event.source_system / f"{event.event_id}.json"),
        }
        if not destination.exists():
            destination.write_text(json.dumps(record, sort_keys=True, indent=2), encoding="utf-8")