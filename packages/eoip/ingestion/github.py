"""Temporal GitHub engineering-knowledge ingestion (G2-SRC-GH-001..004)."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from eoip.connectors.acquisition import BaselineController
from eoip.connectors.github import GitHubConnector
from eoip.connectors.gitlab_json import ISSUE_KEY_PATTERN
from eoip.connectors.reconciliation import SourceReconciler
from eoip.contracts.source_event import SourceEventV2, utc_now_iso
from eoip.graph.evolution import ChangeJournal, GraphEvolutionEngine
from eoip.graph.meta import link_domains
from eoip.graph.store import GraphStore
from eoip.ingestion.dlq import write_dlq_record
from eoip.ingestion.jira import FileEventCapture
from eoip.ingestion.pipeline import IngestionGraphStore
from eoip.jobs import write_json
from eoip.ontology.manifest import ONTOLOGY_VERSION, SCHEMA_VERSION


class GitHubIngestionService:
    def __init__(
        self,
        store: GraphStore,
        connector: GitHubConnector,
        capture: FileEventCapture,
        dlq_root: str | Path,
    ) -> None:
        self.store = IngestionGraphStore(store)
        self.connector = connector
        self.capture = capture
        self.dlq_root = Path(dlq_root)
        self.evolution = GraphEvolutionEngine(
            self.store,
            ChangeJournal(self.dlq_root.parent / "journal" / "semantic-changes.ndjson"),
        )

    def ingest(self, events: list[SourceEventV2], *, dry_run: bool = False) -> dict:
        run_id, started_at = str(uuid4()), utc_now_iso()
        accepted, rejected = [], []
        for event in events:
            if not dry_run:
                self.capture.capture(event)
            try:
                accepted.append((event, self._map(event)))
            except (KeyError, TypeError, ValueError) as exc:
                rejected.append(
                    {
                        "event_id": event.event_id,
                        "source_record_id": event.source_record_id,
                        "error_category": "mapping_error",
                        "error": str(exc),
                    }
                )
                if not dry_run:
                    self._write_dlq(event, str(exc))
        if not dry_run:
            self.store.begin_run(run_id)
            self._write_graph(accepted, run_id, started_at, len(rejected))
        return {
            "run_id": run_id,
            "run_status": "DRY_RUN" if dry_run else ("PARTIAL" if rejected else "SUCCEEDED"),
            "records_seen": len(events),
            "records_accepted": len(accepted),
            "records_rejected": len(rejected),
            "rejected": rejected,
        }

    def _map(self, event: SourceEventV2) -> dict:
        kind = event.metadata["record_kind"]
        repo = event.metadata["repository"]
        record = event.payload or {}
        repo_id = f"github:{self.connector.source_id}:{repo}"
        record_id = str(event.metadata.get("record_id") or event.source_record_id.rsplit(":", 1)[-1])
        common = {
            "source_system": "github",
            "registry_source_id": self.connector.source_id,
            "source_id": event.source_record_id,
            "source_version": event.source_version,
            "ontology_version": ONTOLOGY_VERSION,
            "schema_version": SCHEMA_VERSION,
        }
        if kind == "repository":
            owner = record.get("owner") or {}
            return {
                "kind": kind,
                "label": "Repository",
                "canonical_id": f"urn:eoip:code:repository:{repo_id}",
                "properties": {
                    **common,
                    "repo_id": repo_id,
                    "name": record.get("name") or repo,
                    "source_uri": record.get("html_url"),
                    "description": record.get("description"),
                    "visibility": record.get("visibility") or ("private" if record.get("private") else "public"),
                    "default_branch": record.get("default_branch"),
                    "external_id": str(record.get("id", record_id)),
                },
                "owner": owner if owner.get("login") else None,
                "repo_id": repo_id,
            }
        if kind in {"branch", "ref"} and (kind == "branch" or event.metadata.get("ref_type") == "branch"):
            name = record.get("name") or record.get("ref") or record_id
            return {
                "kind": "branch",
                "label": "Branch",
                "canonical_id": f"urn:eoip:code:branch:{repo_id}:{name}",
                "properties": {**common, "repo_id": repo_id, "branch_name": name, "name": name},
                "repo_id": repo_id,
            }
        if kind in {"tag", "ref"}:
            name = record.get("name") or record.get("ref") or record_id
            commit = record.get("commit") or {}
            return {
                "kind": "tag",
                "label": "Tag",
                "canonical_id": f"urn:eoip:code:tag:{repo_id}:{name}",
                "properties": {
                    **common,
                    "repo_id": repo_id,
                    "tag_name": name,
                    "name": name,
                    "commit_sha": commit.get("sha") if isinstance(commit, dict) else None,
                },
                "repo_id": repo_id,
            }
        if kind == "commit":
            detail = record.get("commit") or {}
            author = detail.get("author") or {}
            sha = record.get("sha") or record_id
            return {
                "kind": kind,
                "label": "Commit",
                "canonical_id": f"urn:eoip:code:commit:{repo_id}:{sha}",
                "properties": {
                    **common,
                    "commit_sha": sha,
                    "repo_id": repo_id,
                    "message": detail.get("message") or record.get("message"),
                    "author_name": author.get("name") or (record.get("author") or {}).get("login"),
                    "author_email": author.get("email"),
                    "created_at": author.get("date") or event.event_time,
                    "parent_shas": json.dumps([item.get("sha") for item in record.get("parents", [])]),
                },
                "repo_id": repo_id,
                "issue_keys": sorted(set(ISSUE_KEY_PATTERN.findall(str(detail.get("message", ""))))),
            }
        if kind == "pull_request":
            number = int(record.get("number", record_id))
            head, base = record.get("head") or {}, record.get("base") or {}
            text = f"{record.get('title', '')} {record.get('body', '')}"
            return {
                "kind": kind,
                "label": "MergeRequest",
                "canonical_id": f"urn:eoip:cicd:merge-request:github:{repo_id}:{number}",
                "properties": {
                    **common,
                    "mr_iid": number,
                    "mr_title": record.get("title") or f"PR #{number}",
                    "name": record.get("title") or f"PR #{number}",
                    "status": record.get("state"),
                    "source_branch": head.get("ref"),
                    "target_branch": base.get("ref"),
                    "commit_sha": head.get("sha"),
                    "url": record.get("html_url"),
                },
                "repo_id": repo_id,
                "commit_sha": head.get("sha"),
                "issue_keys": sorted(set(ISSUE_KEY_PATTERN.findall(text))),
            }
        if kind == "issue":
            number = str(record.get("number", record_id))
            return {
                "kind": kind,
                "label": "WorkItem",
                "canonical_id": f"urn:eoip:work:item:github:{repo_id}:{number}",
                "properties": {
                    **common,
                    "issue_key": f"GH:{repo}#{number}",
                    "summary": record.get("title") or f"Issue #{number}",
                    "description": record.get("body"),
                    "issue_type": "github_issue",
                    "status": record.get("state"),
                    "url": record.get("html_url"),
                    "external_id": str(record.get("id", number)),
                },
                "repo_id": repo_id,
            }
        if kind == "workflow_run":
            run_id = str(record.get("id", record_id))
            return {
                "kind": kind,
                "label": "PipelineRun",
                "canonical_id": f"urn:eoip:cicd:pipeline:github:{repo_id}:{run_id}",
                "properties": {
                    **common,
                    "name": record.get("name") or f"workflow-{run_id}",
                    "pipeline_status": record.get("status"),
                    "status": record.get("status"),
                    "conclusion": record.get("conclusion"),
                    "ref": record.get("head_branch"),
                    "commit_sha": record.get("head_sha"),
                    "created_at": record.get("created_at"),
                    "url": record.get("html_url"),
                },
                "repo_id": repo_id,
                "commit_sha": record.get("head_sha"),
            }
        if kind == "release":
            release_id = str(record.get("id", record_id))
            return {
                "kind": kind,
                "label": "Release",
                "canonical_id": f"urn:eoip:cicd:release:github:{repo_id}:{release_id}",
                "properties": {
                    **common,
                    "name": record.get("name") or record.get("tag_name") or release_id,
                    "tag_name": record.get("tag_name") or release_id,
                    "external_id": release_id,
                    "published_at": record.get("published_at"),
                    "url": record.get("html_url"),
                    "status": "draft" if record.get("draft") else "published",
                    "description": record.get("body"),
                    "repo_id": repo_id,
                },
                "repo_id": repo_id,
            }
        if kind in {"pages", "readme"}:
            path = "github-pages" if kind == "pages" else str(record.get("path", "README.md"))
            url = record.get("html_url")
            return {
                "kind": kind,
                "label": "Document",
                "canonical_id": f"urn:eoip:knowledge:document:github:{repo_id}:{path}",
                "properties": {
                    **common,
                    "name": "GitHub Pages" if kind == "pages" else path,
                    "path": url or f"github://{repo}/{path}",
                    "doc_format": kind,
                    "content_hash": event.content_hash,
                    "repo_id": repo_id,
                    "description": record.get("text") or json.dumps(record, sort_keys=True),
                },
                "repo_id": repo_id,
            }
        raise ValueError(f"unsupported GitHub record kind: {kind}")

    def _write_graph(self, accepted, run_id, started_at, rejected_count) -> None:
        run = self.store.upsert_vertex(
            "IngestionRun",
            {
                "canonical_id": f"urn:eoip:meta:ingestion-run:{run_id}",
                "run_status": "PARTIAL" if rejected_count else "SUCCEEDED",
                "run_kind": "GITHUB",
                "source_system": "github",
                "ingestion_run_id": run_id,
                "started_at": started_at,
                "finished_at": utc_now_iso(),
                "counts": json.dumps({"accepted": len(accepted), "rejected": rejected_count}),
            },
        )
        entities = {}
        for event, mapped in accepted:
            result = self.evolution.evolve_entity(
                mapped["label"], mapped["canonical_id"], mapped["properties"], event
            )
            if result["status"] == "DELETE":
                continue
            entity = self.store.get_vertex_by_canonical_id(mapped["canonical_id"])
            if entity is None:
                raise RuntimeError("GitHub graph evolution did not produce current entity")
            entities[mapped["canonical_id"]] = entity
            evidence = self.store.upsert_vertex(
                "Evidence",
                {
                    "canonical_id": f"urn:eoip:evidence:source-event:github:{event.event_id}",
                    "source_system": "github",
                    "source_ref": f"github://{event.source_record_id}",
                    "source_id": event.source_record_id,
                    "source_version": event.source_version,
                    "method": "SOURCE_EVENT",
                    "captured_at": event.captured_at,
                    "evidence_key": event.event_id,
                    "content_hash": event.content_hash,
                    "mapper_version": self.connector.mapper_version,
                    "ontology_version": ONTOLOGY_VERSION,
                    "schema_version": SCHEMA_VERSION,
                },
            )
            edge_props = {
                "evidence_key": event.event_id,
                "source_ref": evidence["properties"]["source_ref"],
                "source_system": "github",
                "ingestion_run_id": run_id,
                "creation_status": "DETERMINISTIC",
                "ontology_version": ONTOLOGY_VERSION,
                "schema_version": SCHEMA_VERSION,
            }
            self.store.upsert_edge(
                "EVIDENCED_BY", entity["vid"], evidence["vid"], {**edge_props, "fact_key": event.event_id}
            )
            self.store.upsert_edge(
                "INGESTED_IN", entity["vid"], run["vid"], {**edge_props, "fact_key": f"{run_id}:{mapped['canonical_id']}"}
            )
            self._link_entity(
                mapped,
                entity,
                event,
                {key: value for key, value in edge_props.items() if key != "ingestion_run_id"},
            )
        link_domains(self.store, list(entities.values()))

    def _link_entity(self, mapped, entity, event, edge_props) -> None:
        repo_cid = f"urn:eoip:code:repository:{mapped.get('repo_id')}"
        repo = self.store.get_vertex_by_canonical_id(repo_cid)
        kind = mapped["kind"]
        relation = {
            "branch": "HAS_BRANCH",
            "tag": "HAS_TAG",
            "commit": "HAS_COMMIT",
            "pull_request": "HAS_MERGE_REQUEST",
            "issue": "CONTAINS",
            "release": "HAS_RELEASE",
            "pages": "CONTAINS",
            "readme": "CONTAINS",
        }.get(kind)
        if repo and relation:
            self.evolution.evolve_relationship(
                f"github:{relation}:{mapped['canonical_id']}",
                relation,
                repo["canonical_id"],
                entity["canonical_id"],
                edge_props,
                event,
            )
        if kind == "repository" and mapped.get("owner"):
            owner = mapped["owner"]
            login = owner["login"]
            organization = self.evolution.evolve_entity(
                "Organization",
                f"urn:eoip:identity:organization:github:{self.connector.source_id}:{login}",
                {
                    "name": login,
                    "external_id": str(owner.get("id", login)),
                    "url": owner.get("html_url"),
                    "source_system": "github",
                },
                event,
            )
            if organization["status"] != "DELETE":
                self.evolution.evolve_relationship(
                    f"github:organization-repository:{login}:{entity['canonical_id']}",
                    "CONTAINS",
                    f"urn:eoip:identity:organization:github:{self.connector.source_id}:{login}",
                    entity["canonical_id"],
                    edge_props,
                    event,
                )
        commit_sha = mapped.get("commit_sha")
        if commit_sha:
            commit = self.store.get_vertex_by_canonical_id(
                f"urn:eoip:code:commit:{mapped['repo_id']}:{commit_sha}"
            )
            if commit and kind in {"pull_request", "workflow_run"}:
                rel = "REFERENCES" if kind == "pull_request" else "PRODUCED_BY"
                self.evolution.evolve_relationship(
                    f"github:{rel}:{mapped['canonical_id']}:{commit_sha}",
                    rel,
                    entity["canonical_id"],
                    commit["canonical_id"],
                    edge_props,
                    event,
                )
        for issue_key in mapped.get("issue_keys", []):
            work_item = self.store.get_vertex_by_canonical_id(f"urn:eoip:work:item:jira:{issue_key}")
            if work_item and kind in {"commit", "pull_request"}:
                self.evolution.evolve_relationship(
                    f"github:implements:{mapped['canonical_id']}:{issue_key}",
                    "IMPLEMENTS",
                    entity["canonical_id"],
                    work_item["canonical_id"],
                    edge_props,
                    event,
                )

    def _write_dlq(self, event: SourceEventV2, error: str) -> None:
        write_dlq_record(
            self.dlq_root,
            event,
            error,
            stage="mapping",
            error_category="mapping_error",
            replay_ref=str(self.capture.root / "github" / f"{event.event_id}.json"),
            extra={"registry_source_id": self.connector.source_id},
        )

def run_registered_github_operation(entry, payload, store, data_root, correlation_id) -> dict:
    from eoip.connectors.config import connector_from_registry

    root = Path(data_root)
    connector = connector_from_registry(entry, correlation_id=correlation_id)
    if not isinstance(connector, GitHubConnector):
        raise TypeError("registered GitHub source did not create a GitHub connector")
    operation = payload.get("operation")
    if operation not in {"BASELINE", "POLL", "RECONCILE", "REPLAY"}:
        raise ValueError(f"unsupported GitHub source operation: {operation}")
    checkpoint_path = root / "state" / "connectors" / f"{entry.source_id}.json"
    checkpoint_state = (
        json.loads(checkpoint_path.read_text(encoding="utf-8")) if checkpoint_path.exists() else {}
    )
    checkpoint = payload.get("checkpoint") or checkpoint_state.get("checkpoint")
    baseline = None
    try:
        if operation == "BASELINE":
            baseline = BaselineController(
                root / "state" / "baselines" / entry.source_id / f"{correlation_id}.json",
                entry.source_id,
                {
                    "source_type": "github",
                    "mapper_version": connector.mapper_version,
                    "ontology_version": ONTOLOGY_VERSION,
                    "schema_version": SCHEMA_VERSION,
                },
            )
            baseline.transition("DISCOVERING")
            baseline.transition("FETCHING")
            events = list(connector.baseline())
        elif operation in {"POLL", "RECONCILE"}:
            events = list(connector.baseline() if operation == "RECONCILE" else connector.poll_changes(checkpoint))
        else:
            events = []
            for event_id in payload.get("event_ids", []):
                if len(event_id) != 64 or any(char not in "0123456789abcdef" for char in event_id):
                    raise ValueError("replay event IDs must be lowercase SHA-256 values")
                path = root / "raw" / "github" / f"{event_id}.json"
                if not path.exists():
                    raise ValueError(f"captured GitHub event is unavailable: {event_id}")
                events.append(SourceEventV2.model_validate_json(path.read_text(encoding="utf-8")))
        service = GitHubIngestionService(
            store, connector, FileEventCapture(root / "raw"), root / "dlq"
        )
        if baseline:
            for stage in ("MAPPING", "VALIDATING", "MUTATING"):
                baseline.transition(stage)
        if operation == "RECONCILE":
            canonical = {event.event_id: service._map(event)["canonical_id"] for event in events}
            current = store.find_vertices(
                filters={"registry_source_id": entry.source_id}, limit=100_000
            )

            def repair(selected):
                outcome = service.ingest(list(selected), dry_run=False)
                rejected = {item["event_id"] for item in outcome["rejected"]}
                return [canonical[event.event_id] for event in selected if event.event_id not in rejected]

            report = SourceReconciler().reconcile(
                source_id=entry.source_id,
                events=events,
                current_vertices=current,
                canonical_id=lambda event: canonical[event.event_id],
                repair=None if payload.get("dry_run") else repair,
                checkpoint=max((event.cursor or "" for event in events), default=checkpoint),
            )
            write_json(
                root / "state" / "reconciliation" / entry.source_id / f"{report.reconciliation_id}.json",
                report.model_dump(mode="json"),
            )
            result = {
                "run_id": report.reconciliation_id,
                "run_status": "PARTIAL" if report.status == "PARTIAL" else "SUCCEEDED",
                "records_seen": report.source_records,
                "records_accepted": len(report.repaired),
                "records_rejected": 0,
                "rejected": [],
                "reconciliation": report.model_dump(mode="json"),
            }
        else:
            result = service.ingest(events, dry_run=payload.get("dry_run", False))
        next_checkpoint = max((event.cursor or event.event_time for event in events), default=checkpoint)
        result.update(source_id=entry.source_id, operation=operation, next_checkpoint=next_checkpoint)
        if baseline:
            baseline.transition("VERIFYING")
            baseline.transition(
                "COMPLETE",
                checkpoint=next_checkpoint,
                counts={"seen": len(events), "accepted": result["records_accepted"]},
                failures=result["rejected"],
            )
        if (
            operation != "REPLAY"
            and result["run_status"] == "SUCCEEDED"
            and not payload.get("dry_run", False)
            and next_checkpoint
        ):
            write_json(
                checkpoint_path,
                {
                    "schema_version": "1.0",
                    "source_id": entry.source_id,
                    "source_system": "github",
                    "checkpoint": next_checkpoint,
                    "baseline_complete": operation == "BASELINE"
                    or checkpoint_state.get("baseline_complete", False),
                    "updated_at": utc_now_iso(),
                },
            )
        return result
    except Exception as exc:
        if baseline and baseline.read()["stage"] not in {"COMPLETE", "FAILED"}:
            baseline.transition(
                "FAILED", failures=[{"error_category": type(exc).__name__, "message": str(exc)}]
            )
        raise
    finally:
        connector.close()
