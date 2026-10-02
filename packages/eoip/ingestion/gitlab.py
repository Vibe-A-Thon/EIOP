"""Capture-first GitLab MR and pipeline metadata ingestion."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from eoip.connectors.gitlab_json import GitLabJsonConnector
from eoip.contracts.source_event import SourceEvent, utc_now_iso
from eoip.graph.store import GraphStore
from eoip.ingestion.jira import FileEventCapture
from eoip.ontology.manifest import ONTOLOGY_VERSION, SCHEMA_VERSION


class GitLabIngestionService:
    def __init__(
        self,
        store: GraphStore,
        repo_id: str,
        connector: GitLabJsonConnector,
        capture: FileEventCapture,
        dlq_root: str | Path,
    ) -> None:
        self.store = store
        self.repo_id = repo_id
        self.connector = connector
        self.capture = capture
        self.dlq_root = Path(dlq_root)

    def ingest(self, document: object, *, dry_run: bool = False) -> dict:
        events = self.connector.events(self.connector.records(document))
        mapped = []
        rejected = []
        for event in events:
            try:
                record = self.connector.map_event(event)
                if not dry_run:
                    self.capture.capture(event)
                mapped.append((event, record))
            except (ValueError, TypeError) as exc:
                rejected.append({"event_id": event.event_id, "source_record_id": event.source_record_id, "error": str(exc)})
                if not dry_run:
                    self.capture.capture(event)
                    self._write_dlq(event, str(exc))
        run_id = uuid4().hex
        if not dry_run:
            self._write_graph(mapped, run_id, len(rejected))
        return {
            "run_id": run_id,
            "run_status": "DRY_RUN" if dry_run else ("PARTIAL" if rejected else "SUCCEEDED"),
            "records_seen": len(events),
            "records_accepted": len(mapped),
            "records_rejected": len(rejected),
            "rejected": rejected,
        }

    def _write_graph(self, mapped: list[tuple[SourceEvent, dict]], run_id: str, rejected_count: int) -> None:
        now = utc_now_iso()
        run = self.store.upsert_vertex(
            "IngestionRun",
            {
                "canonical_id": f"urn:eoip:meta:ingestion-run:{run_id}",
                "run_status": "PARTIAL" if rejected_count else "SUCCEEDED",
                "run_kind": "GITLAB_JSON",
                "source_system": "gitlab",
                "ingestion_run_id": run_id,
                "started_at": now,
                "finished_at": utc_now_iso(),
                "counts": json.dumps({"accepted": len(mapped), "rejected": rejected_count}, sort_keys=True),
                "ontology_version": ONTOLOGY_VERSION,
                "schema_version": SCHEMA_VERSION,
            },
        )
        repo = self.store.get_vertex_by_canonical_id(f"urn:eoip:code:repository:{self.repo_id}")
        if repo is None:
            repo = self.store.upsert_vertex(
                "Repository",
                {
                    "canonical_id": f"urn:eoip:code:repository:{self.repo_id}",
                    "repo_id": self.repo_id,
                    "name": self.repo_id,
                    "source_system": "gitlab",
                    "ontology_version": ONTOLOGY_VERSION,
                    "schema_version": SCHEMA_VERSION,
                    "ingestion_run_id": run_id,
                },
            )
        for event, record in mapped:
            mr_kind = record["kind"] == "merge_request"
            entity_type = "MergeRequest" if mr_kind else "PipelineRun"
            canonical_id = f"urn:eoip:cicd:{'merge-request' if mr_kind else 'pipeline'}:gitlab:{self.repo_id}:{record['source_id']}"
            props = {
                "canonical_id": canonical_id,
                "source_system": "gitlab",
                "source_id": record["source_id"],
                "source_version": event.source_version,
                "ingestion_run_id": run_id,
                "ontology_version": ONTOLOGY_VERSION,
                "schema_version": SCHEMA_VERSION,
                "first_seen": event.captured_at,
                "last_seen": event.captured_at,
                "valid_from": event.captured_at,
            }
            if mr_kind:
                props.update(
                    {
                        "mr_iid": int(record["source_id"]),
                        "mr_title": record["title"],
                        "source_branch": record["source_branch"],
                        "target_branch": record["target_branch"],
                        "status": record["status"],
                        "name": record["title"],
                    }
                )
            else:
                props.update(
                    {
                        "name": record["name"],
                        "pipeline_status": record["status"],
                        "ref": record["ref"],
                        "commit_sha": record["commit_sha"],
                    }
                )
            entity = self.store.upsert_vertex(entity_type, props)
            evidence = self.store.upsert_vertex(
                "Evidence",
                {
                    "canonical_id": f"urn:eoip:evidence:source-event:gitlab:{event.event_id}",
                    "source_system": "gitlab",
                    "source_ref": f"gitlab://{self.repo_id}/{event.source_record_id}",
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
                "evidence_key": event.event_id,
                "source_ref": evidence["properties"]["source_ref"],
                "source_system": "gitlab",
                "ingestion_run_id": run_id,
                "creation_status": "DETERMINISTIC",
            }
            self.store.upsert_edge(
                "EVIDENCED_BY",
                entity["vid"],
                evidence["vid"],
                {"fact_key": f"gitlab-evidence:{event.event_id}", **evidence_props},
            )
            self.store.upsert_edge(
                "INGESTED_IN",
                entity["vid"],
                run["vid"],
                {"fact_key": f"gitlab-run:{run_id}:{canonical_id}", **evidence_props},
            )
            if mr_kind:
                self.store.upsert_edge(
                    "HAS_MERGE_REQUEST",
                    repo["vid"],
                    entity["vid"],
                    {"fact_key": f"gitlab-mr:{self.repo_id}:{record['source_id']}", **evidence_props},
                )
                if record["source_branch"]:
                    branch = self.store.upsert_vertex(
                        "Branch",
                        {
                            "canonical_id": f"urn:eoip:code:branch:{self.repo_id}:{record['source_branch']}",
                            "branch_name": record["source_branch"],
                            "repo_id": self.repo_id,
                            "source_system": "gitlab",
                            "ingestion_run_id": run_id,
                            "ontology_version": ONTOLOGY_VERSION,
                            "schema_version": SCHEMA_VERSION,
                        },
                    )
                    self.store.upsert_edge(
                        "HAS_BRANCH",
                        repo["vid"],
                        branch["vid"],
                        {"fact_key": f"branch:{self.repo_id}:{record['source_branch']}", **evidence_props},
                    )
                if record["commit_sha"]:
                    commit = self.store.get_vertex_by_canonical_id(
                        f"urn:eoip:code:commit:{self.repo_id}:{record['commit_sha']}"
                    )
                    if commit is not None:
                        self.store.upsert_edge(
                            "REFERENCES",
                            entity["vid"],
                            commit["vid"],
                            {"fact_key": f"merge-request-commit:{canonical_id}:{record['commit_sha']}", **evidence_props},
                        )
                for issue_key in record["work_item_keys"]:
                    work_item = self.store.get_vertex_by_canonical_id(f"urn:eoip:work:item:jira:{issue_key}")
                    if work_item is not None:
                        self.store.upsert_edge(
                            "IMPLEMENTS",
                            entity["vid"],
                            work_item["vid"],
                            {"fact_key": f"merge-request-issue:{canonical_id}:{issue_key}", **evidence_props},
                        )
            else:
                if record["commit_sha"]:
                    commit = self.store.get_vertex_by_canonical_id(
                        f"urn:eoip:code:commit:{self.repo_id}:{record['commit_sha']}"
                    )
                    if commit is not None:
                        self.store.upsert_edge(
                            "PRODUCED_BY",
                            entity["vid"],
                            commit["vid"],
                            {"fact_key": f"pipeline-commit:{canonical_id}:{record['commit_sha']}", **evidence_props},
                        )
                for issue_key in record["work_item_keys"]:
                    work_item = self.store.get_vertex_by_canonical_id(f"urn:eoip:work:item:jira:{issue_key}")
                    if work_item is not None:
                        self.store.upsert_edge(
                            "REFERENCES",
                            entity["vid"],
                            work_item["vid"],
                            {"fact_key": f"pipeline-issue:{canonical_id}:{issue_key}", **evidence_props},
                        )

    def _write_dlq(self, event: SourceEvent, error: str) -> None:
        self.dlq_root.mkdir(parents=True, exist_ok=True)
        destination = self.dlq_root / f"{event.event_id}.json"
        record = {
            "event_id": event.event_id,
            "source_system": event.source_system,
            "source_record_id": event.source_record_id,
            "repository_id": self.repo_id,
            "payload_hash": event.payload_hash,
            "error": error,
            "replay_ref": str(self.capture.root / event.source_system / f"{event.event_id}.json"),
        }
        if not destination.exists():
            destination.write_text(json.dumps(record, sort_keys=True, indent=2), encoding="utf-8")
