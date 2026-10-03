"""Temporal GitLab engineering-knowledge ingestion (G2-SRC-GL-001..004)."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from eoip.connectors.acquisition import BaselineController
from eoip.connectors.gitlab import GitLabConnector
from eoip.connectors.gitlab_json import ISSUE_KEY_PATTERN
from eoip.connectors.reconciliation import SourceReconciler
from eoip.contracts.source_event import SourceEventV2, utc_now_iso
from eoip.graph.evolution import ChangeJournal, GraphEvolutionEngine
from eoip.graph.meta import link_domains
from eoip.graph.store import GraphStore
from eoip.ingestion.dlq import write_dlq_record
from eoip.ingestion.jira import FileEventCapture
from eoip.jobs import write_json
from eoip.ontology.manifest import ONTOLOGY_VERSION, SCHEMA_VERSION


class GitLabTemporalIngestionService:
    """Map GitLab source events into revisioned, evidence-backed engineering facts."""

    def __init__(
        self,
        store: GraphStore,
        connector: GitLabConnector,
        capture: FileEventCapture,
        dlq_root: str | Path,
    ) -> None:
        self.store = store
        self.connector = connector
        self.capture = capture
        self.dlq_root = Path(dlq_root)
        self.evolution = GraphEvolutionEngine(
            store,
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
        kind = str(event.metadata["record_kind"])
        project = str(event.metadata["project"])
        record_id = str(event.metadata.get("record_id") or event.source_record_id.rsplit(":", 1)[-1])
        record = event.payload or {}
        repo_id = f"gitlab:{self.connector.source_id}:{project}"
        common = {
            "source_system": "gitlab",
            "registry_source_id": self.connector.source_id,
            "source_id": event.source_record_id,
            "source_version": event.source_version,
            "ontology_version": ONTOLOGY_VERSION,
            "schema_version": SCHEMA_VERSION,
        }
        if kind == "group":
            full_path = str(record.get("full_path") or record.get("path") or record_id)
            return {
                "kind": kind,
                "label": "Organization",
                "canonical_id": self._organization_id(full_path),
                "properties": {
                    **common,
                    "name": record.get("name") or full_path,
                    "external_id": str(record.get("id", record_id)),
                    "url": record.get("web_url"),
                },
            }
        if kind == "project":
            namespace = record.get("namespace") if isinstance(record.get("namespace"), dict) else {}
            namespace_path = namespace.get("full_path") or namespace.get("path")
            return {
                "kind": kind,
                "label": "Repository",
                "canonical_id": f"urn:eoip:code:repository:{repo_id}",
                "properties": {
                    **common,
                    "repo_id": repo_id,
                    "name": record.get("name") or project,
                    "source_uri": record.get("web_url"),
                    "description": record.get("description"),
                    "visibility": record.get("visibility"),
                    "default_branch": record.get("default_branch"),
                    "external_id": str(record.get("id", record_id)),
                },
                "repo_id": repo_id,
                "namespace": namespace_path,
                "namespace_name": namespace.get("name") or namespace_path,
                "namespace_id": namespace.get("id"),
            }
        if kind == "branch":
            name = str(record.get("name") or record_id)
            return {
                "kind": kind,
                "label": "Branch",
                "canonical_id": f"urn:eoip:code:branch:{repo_id}:{name}",
                "properties": {**common, "repo_id": repo_id, "branch_name": name, "name": name},
                "repo_id": repo_id,
            }
        if kind == "tag":
            name = str(record.get("name") or record_id)
            commit = record.get("commit") if isinstance(record.get("commit"), dict) else {}
            return {
                "kind": kind,
                "label": "Tag",
                "canonical_id": f"urn:eoip:code:tag:{repo_id}:{name}",
                "properties": {
                    **common,
                    "repo_id": repo_id,
                    "tag_name": name,
                    "name": name,
                    "commit_sha": commit.get("id") or commit.get("sha"),
                },
                "repo_id": repo_id,
            }
        if kind == "commit":
            sha = str(record.get("id") or record.get("sha") or record_id)
            message = str(record.get("message") or record.get("title") or "")
            return {
                "kind": kind,
                "label": "Commit",
                "canonical_id": f"urn:eoip:code:commit:{repo_id}:{sha}",
                "properties": {
                    **common,
                    "commit_sha": sha,
                    "repo_id": repo_id,
                    "message": message,
                    "author_name": record.get("author_name"),
                    "author_email": record.get("author_email"),
                    "created_at": record.get("authored_date") or record.get("created_at"),
                    "parent_shas": json.dumps(record.get("parent_ids") or []),
                    "url": record.get("web_url") or record.get("url"),
                },
                "repo_id": repo_id,
                "issue_keys": self._issue_keys(message),
            }
        if kind == "merge_request":
            iid = int(record.get("iid", record_id))
            title = str(record.get("title") or f"MR !{iid}")
            description = str(record.get("description") or "")
            diff_refs = record.get("diff_refs") if isinstance(record.get("diff_refs"), dict) else {}
            return {
                "kind": kind,
                "label": "MergeRequest",
                "canonical_id": f"urn:eoip:cicd:merge-request:gitlab:{repo_id}:{iid}",
                "properties": {
                    **common,
                    "mr_iid": iid,
                    "mr_title": title,
                    "name": title,
                    "status": record.get("state"),
                    "source_branch": record.get("source_branch"),
                    "target_branch": record.get("target_branch"),
                    "commit_sha": record.get("sha") or diff_refs.get("head_sha"),
                    "url": record.get("web_url") or record.get("url"),
                },
                "repo_id": repo_id,
                "commit_sha": record.get("sha") or diff_refs.get("head_sha"),
                "issue_keys": self._issue_keys(title, description, record.get("source_branch")),
            }
        if kind == "issue":
            iid = str(record.get("iid", record_id))
            return {
                "kind": kind,
                "label": "WorkItem",
                "canonical_id": f"urn:eoip:work:item:gitlab:{repo_id}:{iid}",
                "properties": {
                    **common,
                    "issue_key": f"GL:{project}#{iid}",
                    "summary": record.get("title") or f"Issue #{iid}",
                    "description": record.get("description"),
                    "issue_type": "gitlab_issue",
                    "status": record.get("state"),
                    "url": record.get("web_url") or record.get("url"),
                    "external_id": str(record.get("id", iid)),
                },
                "repo_id": repo_id,
            }
        if kind == "pipeline":
            pipeline_id = str(record.get("id", record_id))
            return {
                "kind": kind,
                "label": "PipelineRun",
                "canonical_id": f"urn:eoip:cicd:pipeline:gitlab:{repo_id}:{pipeline_id}",
                "properties": {
                    **common,
                    "name": record.get("name") or f"pipeline-{pipeline_id}",
                    "pipeline_status": record.get("status"),
                    "status": record.get("status"),
                    "ref": record.get("ref"),
                    "commit_sha": record.get("sha"),
                    "created_at": record.get("created_at"),
                    "url": record.get("web_url"),
                    "repo_id": repo_id,
                },
                "repo_id": repo_id,
                "commit_sha": record.get("sha"),
            }
        if kind == "job":
            job_id = str(record.get("id", record_id))
            pipeline = record.get("pipeline") if isinstance(record.get("pipeline"), dict) else {}
            duration = record.get("duration")
            return {
                "kind": kind,
                "label": "Job",
                "canonical_id": f"urn:eoip:cicd:job:gitlab:{repo_id}:{job_id}",
                "properties": {
                    **common,
                    "job_id": job_id,
                    "name": record.get("name") or f"job-{job_id}",
                    "status": record.get("status"),
                    "stage": record.get("stage"),
                    "ref": record.get("ref"),
                    "commit_sha": record.get("sha"),
                    "created_at": record.get("created_at"),
                    "duration_seconds": float(duration) if isinstance(duration, (int, float)) else None,
                    "url": record.get("web_url"),
                    "repo_id": repo_id,
                },
                "repo_id": repo_id,
                "pipeline_id": pipeline.get("id"),
                "commit_sha": record.get("sha"),
            }
        if kind == "artifact":
            job_id, _, artifact_id = record_id.partition(":")
            return {
                "kind": kind,
                "label": "Artifact",
                "canonical_id": f"urn:eoip:cicd:artifact:gitlab:{repo_id}:{job_id}:{artifact_id}",
                "properties": {
                    **common,
                    "name": record.get("filename") or artifact_id,
                    "artifact_type": record.get("file_type"),
                    "artifact_format": record.get("file_format"),
                    "file_size": record.get("size"),
                    "repo_id": repo_id,
                },
                "repo_id": repo_id,
                "job_id": str(record.get("job_id") or job_id),
            }
        if kind == "deployment":
            deployment_id = str(record.get("id", record_id))
            environment = record.get("environment")
            environment_name = environment.get("name") if isinstance(environment, dict) else environment
            deployable = record.get("deployable") if isinstance(record.get("deployable"), dict) else {}
            pipeline = deployable.get("pipeline") if isinstance(deployable.get("pipeline"), dict) else {}
            return {
                "kind": kind,
                "label": "Deployment",
                "canonical_id": f"urn:eoip:cicd:deployment:gitlab:{repo_id}:{deployment_id}",
                "properties": {
                    **common,
                    "name": environment_name or f"deployment-{deployment_id}",
                    "status": record.get("status"),
                    "environment": environment_name,
                    "ref": record.get("ref"),
                    "commit_sha": record.get("sha"),
                    "created_at": record.get("created_at"),
                    "deployable_id": str(record.get("deployable_id") or deployable.get("id") or ""),
                    "url": record.get("web_url") or deployable.get("web_url"),
                    "repo_id": repo_id,
                },
                "repo_id": repo_id,
                "pipeline_id": pipeline.get("id"),
                "job_id": record.get("deployable_id") or deployable.get("id"),
            }
        if kind == "release":
            tag_name = str(record.get("tag_name") or record_id)
            return {
                "kind": kind,
                "label": "Release",
                "canonical_id": f"urn:eoip:cicd:release:gitlab:{repo_id}:{tag_name}",
                "properties": {
                    **common,
                    "name": record.get("name") or tag_name,
                    "tag_name": tag_name,
                    "external_id": tag_name,
                    "published_at": record.get("released_at"),
                    "url": (record.get("_links") or {}).get("self"),
                    "status": "upcoming" if record.get("upcoming_release") else "published",
                    "description": record.get("description"),
                    "repo_id": repo_id,
                },
                "repo_id": repo_id,
            }
        if kind == "file_change":
            path = str(record.get("new_path") or record.get("old_path") or record_id)
            return {
                "kind": kind,
                "label": "File",
                "canonical_id": f"urn:eoip:code:file:{repo_id}:{path}",
                "properties": {
                    **common,
                    "repo_id": repo_id,
                    "path": path,
                    "name": path.rsplit("/", 1)[-1],
                },
                "repo_id": repo_id,
                "commit_sha": record.get("commit_sha"),
                "merge_request_iid": record.get("merge_request_iid"),
            }
        if kind in {"wiki", "pages", "pages_content", "pages_domain", "readme"}:
            if kind == "wiki":
                path = str(record.get("slug") or record_id)
                url = record.get("web_url")
                name = record.get("title") or path
                description = record.get("content")
            elif kind == "pages_domain":
                path = str(record.get("url") or record.get("domain") or record_id)
                url, name, description = path, record.get("domain") or path, json.dumps(record, sort_keys=True)
            elif kind == "pages":
                path = str(record.get("url") or record.get("html_url") or "gitlab-pages")
                url, name, description = path, "GitLab Pages", json.dumps(record, sort_keys=True)
            elif kind == "readme":
                path = str(record.get("file_path") or "README.md")
                url = f"gitlab://{project}/{path}"
                name, description = path, record.get("text")
            else:
                path = str(record.get("url") or record_id)
                url = path
                name = record.get("title") or path
                description = record.get("text")
            return {
                "kind": kind,
                "label": "Document",
                "canonical_id": f"urn:eoip:knowledge:document:gitlab:{repo_id}:{path}",
                "properties": {
                    **common,
                    "name": name,
                    "path": url or f"gitlab://{project}/{path}",
                    "doc_format": kind,
                    "content_hash": event.content_hash,
                    "repo_id": repo_id,
                    "description": description,
                    "verified": record.get("verified") if kind == "pages_domain" else None,
                },
                "repo_id": repo_id,
            }
        raise ValueError(f"unsupported GitLab record kind: {kind}")

    def _write_graph(self, accepted, run_id: str, started_at: str, rejected_count: int) -> None:
        run = self.store.upsert_vertex(
            "IngestionRun",
            {
                "canonical_id": f"urn:eoip:meta:ingestion-run:{run_id}",
                "run_status": "PARTIAL" if rejected_count else "SUCCEEDED",
                "run_kind": "GITLAB",
                "source_system": "gitlab",
                "ingestion_run_id": run_id,
                "started_at": started_at,
                "finished_at": utc_now_iso(),
                "counts": json.dumps({"accepted": len(accepted), "rejected": rejected_count}),
            },
        )
        ingested_vertices = []
        for event, mapped in accepted:
            result = self.evolution.evolve_entity(
                mapped["label"], mapped["canonical_id"], mapped["properties"], event
            )
            if result["status"] == "DELETE":
                continue
            entity = self.store.get_vertex_by_canonical_id(mapped["canonical_id"])
            if entity is None:
                raise RuntimeError("GitLab graph evolution did not produce current entity")
            evidence = self.store.upsert_vertex(
                "Evidence",
                {
                    "canonical_id": f"urn:eoip:evidence:source-event:gitlab:{event.event_id}",
                    "source_system": "gitlab",
                    "source_ref": f"gitlab://{event.source_record_id}",
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
                "source_system": "gitlab",
                "ingestion_run_id": run_id,
                "creation_status": "DETERMINISTIC",
                "ontology_version": ONTOLOGY_VERSION,
                "schema_version": SCHEMA_VERSION,
            }
            self.store.upsert_edge(
                "EVIDENCED_BY",
                entity["vid"],
                evidence["vid"],
                {**edge_props, "fact_key": event.event_id},
            )
            self.store.upsert_edge(
                "INGESTED_IN",
                entity["vid"],
                run["vid"],
                {**edge_props, "fact_key": f"{run_id}:{mapped['canonical_id']}"},
            )
            stable_edge_props = {
                key: value for key, value in edge_props.items() if key != "ingestion_run_id"
            }
            self._link_entity(mapped, entity, event, stable_edge_props)
            ingested_vertices.append(entity)
        link_domains(self.store, ingested_vertices)

    def _link_entity(self, mapped: dict, entity: dict, event: SourceEventV2, edge_props: dict) -> None:
        kind = mapped["kind"]
        repo = self.store.get_vertex_by_canonical_id(
            f"urn:eoip:code:repository:{mapped.get('repo_id')}"
        )
        relation = {
            "branch": "HAS_BRANCH",
            "tag": "HAS_TAG",
            "commit": "HAS_COMMIT",
            "merge_request": "HAS_MERGE_REQUEST",
            "issue": "CONTAINS",
            "release": "HAS_RELEASE",
            "wiki": "CONTAINS",
            "pages": "CONTAINS",
            "pages_domain": "CONTAINS",
            "pages_content": "CONTAINS",
            "readme": "CONTAINS",
            "file_change": "CONTAINS",
        }.get(kind)
        if repo and relation:
            self._relationship(
                f"gitlab:{relation}:{mapped['canonical_id']}",
                relation,
                repo["canonical_id"],
                entity["canonical_id"],
                edge_props,
                event,
            )
        if kind == "project" and mapped.get("namespace"):
            namespace = str(mapped["namespace"])
            organization_id = self._organization_id(namespace)
            self.evolution.evolve_entity(
                "Organization",
                organization_id,
                {
                    "name": mapped.get("namespace_name") or namespace,
                    "external_id": str(mapped.get("namespace_id") or namespace),
                    "source_system": "gitlab",
                },
                event,
            )
            self._relationship(
                f"gitlab:organization-repository:{namespace}:{entity['canonical_id']}",
                "CONTAINS",
                organization_id,
                entity["canonical_id"],
                edge_props,
                event,
            )
        commit_sha = mapped.get("commit_sha")
        if commit_sha:
            commit_id = f"urn:eoip:code:commit:{mapped['repo_id']}:{commit_sha}"
            commit = self.store.get_vertex_by_canonical_id(commit_id)
            if commit and kind in {"merge_request", "pipeline"}:
                relation_name = "REFERENCES" if kind == "merge_request" else "PRODUCED_BY"
                self._relationship(
                    f"gitlab:{relation_name}:{mapped['canonical_id']}:{commit_sha}",
                    relation_name,
                    entity["canonical_id"],
                    commit_id,
                    edge_props,
                    event,
                )
            if commit and kind == "file_change":
                self._relationship(
                    f"gitlab:commit-file:{commit_sha}:{mapped['canonical_id']}",
                    "MODIFIES",
                    commit_id,
                    entity["canonical_id"],
                    edge_props,
                    event,
                )
        if kind == "file_change" and mapped.get("merge_request_iid"):
            mr_id = (
                f"urn:eoip:cicd:merge-request:gitlab:{mapped['repo_id']}:"
                f"{mapped['merge_request_iid']}"
            )
            if self.store.get_vertex_by_canonical_id(mr_id):
                self._relationship(
                    f"gitlab:merge-request-file:{mr_id}:{mapped['canonical_id']}",
                    "MODIFIES",
                    mr_id,
                    entity["canonical_id"],
                    edge_props,
                    event,
                )
        if kind == "job" and mapped.get("pipeline_id"):
            pipeline_id = (
                f"urn:eoip:cicd:pipeline:gitlab:{mapped['repo_id']}:{mapped['pipeline_id']}"
            )
            if self.store.get_vertex_by_canonical_id(pipeline_id):
                self._relationship(
                    f"gitlab:pipeline-job:{pipeline_id}:{mapped['canonical_id']}",
                    "HAS_JOB",
                    pipeline_id,
                    entity["canonical_id"],
                    edge_props,
                    event,
                )
        if kind == "artifact" and mapped.get("job_id"):
            job_id = f"urn:eoip:cicd:job:gitlab:{mapped['repo_id']}:{mapped['job_id']}"
            if self.store.get_vertex_by_canonical_id(job_id):
                self._relationship(
                    f"gitlab:job-artifact:{job_id}:{mapped['canonical_id']}",
                    "PRODUCES",
                    job_id,
                    entity["canonical_id"],
                    edge_props,
                    event,
                )
        if kind == "deployment":
            producer_id = None
            if mapped.get("pipeline_id"):
                producer_id = (
                    f"urn:eoip:cicd:pipeline:gitlab:{mapped['repo_id']}:{mapped['pipeline_id']}"
                )
            if not producer_id and mapped.get("job_id"):
                producer_id = f"urn:eoip:cicd:job:gitlab:{mapped['repo_id']}:{mapped['job_id']}"
            if producer_id and self.store.get_vertex_by_canonical_id(producer_id):
                self._relationship(
                    f"gitlab:deployment:{producer_id}:{mapped['canonical_id']}",
                    "DEPLOYS",
                    producer_id,
                    entity["canonical_id"],
                    edge_props,
                    event,
                )
        for issue_key in mapped.get("issue_keys", []):
            work_item_id = f"urn:eoip:work:item:jira:{issue_key}"
            if self.store.get_vertex_by_canonical_id(work_item_id) and kind in {
                "commit",
                "merge_request",
            }:
                self._relationship(
                    f"gitlab:implements:{mapped['canonical_id']}:{issue_key}",
                    "IMPLEMENTS",
                    entity["canonical_id"],
                    work_item_id,
                    edge_props,
                    event,
                )

    def _relationship(
        self,
        relationship_id: str,
        label: str,
        out_id: str,
        in_id: str,
        properties: dict,
        event: SourceEventV2,
    ) -> None:
        self.evolution.evolve_relationship(
            relationship_id,
            label,
            out_id,
            in_id,
            properties,
            event,
        )

    def _organization_id(self, namespace: str) -> str:
        return f"urn:eoip:identity:organization:gitlab:{self.connector.source_id}:{namespace}"

    @staticmethod
    def _issue_keys(*values: object) -> list[str]:
        return sorted(
            {
                key
                for value in values
                if isinstance(value, str)
                for key in ISSUE_KEY_PATTERN.findall(value)
            }
        )

    def _write_dlq(self, event: SourceEventV2, error: str) -> None:
        write_dlq_record(
            self.dlq_root,
            event,
            error,
            stage="mapping",
            error_category="mapping_error",
            replay_ref=str(self.capture.root / "gitlab" / f"{event.event_id}.json"),
            extra={"registry_source_id": self.connector.source_id},
        )

def run_registered_gitlab_operation(entry, payload, store, data_root, correlation_id) -> dict:
    """Run baseline/poll/reconcile/replay through the common registered-source flow."""

    from eoip.connectors.config import connector_from_registry

    root = Path(data_root)
    connector = connector_from_registry(entry, correlation_id=correlation_id)
    if not isinstance(connector, GitLabConnector):
        raise TypeError("registered GitLab source did not create a GitLab connector")
    operation = payload.get("operation")
    if operation not in {"BASELINE", "POLL", "RECONCILE", "REPLAY"}:
        raise ValueError(f"unsupported GitLab source operation: {operation}")
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
                    "source_type": "gitlab",
                    "mapper_version": connector.mapper_version,
                    "ontology_version": ONTOLOGY_VERSION,
                    "schema_version": SCHEMA_VERSION,
                },
            )
            baseline.transition("DISCOVERING")
            baseline.transition("FETCHING")
            events = list(connector.baseline())
        elif operation in {"POLL", "RECONCILE"}:
            events = list(
                connector.baseline()
                if operation == "RECONCILE"
                else connector.poll_changes(checkpoint)
            )
        else:
            events = []
            for event_id in payload.get("event_ids", []):
                if len(event_id) != 64 or any(char not in "0123456789abcdef" for char in event_id):
                    raise ValueError("replay event IDs must be lowercase SHA-256 values")
                path = root / "raw" / "gitlab" / f"{event_id}.json"
                if not path.exists():
                    raise ValueError(f"captured GitLab event is unavailable: {event_id}")
                events.append(SourceEventV2.model_validate_json(path.read_text(encoding="utf-8")))
        service = GitLabTemporalIngestionService(
            store,
            connector,
            FileEventCapture(root / "raw"),
            root / "dlq",
        )
        if baseline:
            for stage in ("MAPPING", "VALIDATING", "MUTATING"):
                baseline.transition(stage)
        if operation == "RECONCILE":
            canonical = {event.event_id: service._map(event)["canonical_id"] for event in events}
            current = store.find_vertices(
                filters={"registry_source_id": entry.source_id},
                limit=100_000,
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
                root
                / "state"
                / "reconciliation"
                / entry.source_id
                / f"{report.reconciliation_id}.json",
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
        next_checkpoint = max(
            (event.cursor or event.event_time for event in events),
            default=checkpoint,
        )
        result.update(
            source_id=entry.source_id,
            operation=operation,
            next_checkpoint=next_checkpoint,
        )
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
                    "source_system": "gitlab",
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
                "FAILED",
                failures=[{"error_category": type(exc).__name__, "message": str(exc)}],
            )
        raise
    finally:
        connector.close()
