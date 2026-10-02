"""Temporal Jira engineering-knowledge ingestion (G2-SRC-JIRA-001..006)."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from eoip.connectors.acquisition import BaselineController
from eoip.connectors.jira import JiraConnector
from eoip.connectors.reconciliation import SourceReconciler
from eoip.contracts.source_event import SourceEventV2, utc_now_iso
from eoip.graph.evolution import ChangeJournal, GraphEvolutionEngine
from eoip.graph.store import GraphStore
from eoip.ingestion.jira import FileEventCapture
from eoip.jobs import write_json
from eoip.ontology.manifest import ONTOLOGY_VERSION, SCHEMA_VERSION


class JiraTemporalIngestionService:
    def __init__(
        self,
        store: GraphStore,
        connector: JiraConnector,
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
        project_key = str(event.metadata["project"])
        record_id = str(event.metadata.get("record_id") or event.source_record_id.rsplit(":", 1)[-1])
        record = event.payload or {}
        common = {
            "source_system": "jira",
            "registry_source_id": self.connector.source_id,
            "source_id": event.source_record_id,
            "source_version": event.source_version,
            "ontology_version": ONTOLOGY_VERSION,
            "schema_version": SCHEMA_VERSION,
        }
        if kind == "project":
            key = str(record.get("key") or project_key)
            return {
                "kind": kind,
                "label": "Project",
                "canonical_id": self._project_id(key),
                "properties": {
                    **common,
                    "name": record.get("name") or key,
                    "issue_key": key,
                    "project_key": key,
                    "external_id": str(record.get("id", key)),
                    "description": self._text(record.get("description")),
                    "url": record.get("self"),
                },
                "project_key": key,
            }
        if kind == "issue_type":
            issue_type_id = str(record.get("id") or record_id)
            return {
                "kind": kind,
                "label": "IssueType",
                "canonical_id": self._issue_type_id(project_key, issue_type_id),
                "properties": {
                    **common,
                    "issue_type_id": issue_type_id,
                    "name": record.get("name") or issue_type_id,
                    "description": record.get("description"),
                    "project_key": project_key,
                },
                "project_key": project_key,
            }
        if kind == "status":
            status_id = str(record.get("id") or record_id)
            return {
                "kind": kind,
                "label": "Status",
                "canonical_id": self._status_id(project_key, status_id),
                "properties": {
                    **common,
                    "status_id": status_id,
                    "name": record.get("name") or status_id,
                    "description": record.get("description"),
                    "project_key": project_key,
                },
                "project_key": project_key,
            }
        if kind == "version":
            version_id = str(record.get("id") or record_id)
            return {
                "kind": kind,
                "label": "Version",
                "canonical_id": self._version_id(project_key, version_id),
                "properties": {
                    **common,
                    "version_id": version_id,
                    "name": record.get("name") or version_id,
                    "description": record.get("description"),
                    "project_key": project_key,
                    "released": record.get("released"),
                    "release_date": record.get("releaseDate"),
                    "status": "released" if record.get("released") else "unreleased",
                },
                "project_key": project_key,
            }
        if kind == "sprint":
            sprint_id = str(record.get("id") or record_id)
            return {
                "kind": kind,
                "label": "Sprint",
                "canonical_id": self._sprint_id(project_key, sprint_id),
                "properties": {
                    **common,
                    "sprint_id": sprint_id,
                    "name": record.get("name") or sprint_id,
                    "description": record.get("goal"),
                    "project_key": project_key,
                    "status": record.get("state"),
                    "start_date": record.get("startDate"),
                    "end_date": record.get("endDate"),
                },
                "project_key": project_key,
            }
        if kind == "issue":
            issue_key = str(record.get("key") or record_id)
            fields = record.get("fields") if isinstance(record.get("fields"), dict) else {}
            project = fields.get("project") if isinstance(fields.get("project"), dict) else {}
            canonical_project = str(project.get("key") or project_key)
            issue_type = fields.get("issuetype") if isinstance(fields.get("issuetype"), dict) else {}
            status = fields.get("status") if isinstance(fields.get("status"), dict) else {}
            return {
                "kind": kind,
                "label": "WorkItem",
                "canonical_id": self._issue_id(issue_key),
                "properties": {
                    **common,
                    "issue_key": issue_key,
                    "summary": fields.get("summary") or issue_key,
                    "description": self._text(fields.get("description")),
                    "issue_type": issue_type.get("name"),
                    "status": status.get("name"),
                    "created_at": fields.get("created"),
                    "modified_at": fields.get("updated"),
                    "external_id": str(record.get("id", issue_key)),
                    "url": record.get("self"),
                },
                "project_key": canonical_project,
                "issue_key": issue_key,
                "issue_type": issue_type,
                "status": status,
                "assignee": fields.get("assignee"),
                "reporter": fields.get("reporter"),
                "parent_key": (fields.get("parent") or {}).get("key")
                if isinstance(fields.get("parent"), dict)
                else None,
                "versions": [item for item in fields.get("fixVersions") or [] if isinstance(item, dict)],
                "sprints": self._sprints(fields),
                "links": [item for item in fields.get("issuelinks") or [] if isinstance(item, dict)],
            }
        if kind == "comment":
            issue_key = str(record.get("issue_key") or record_id.split(":", 1)[0])
            comment_id = str(record.get("id") or record_id)
            return {
                "kind": kind,
                "label": "Comment",
                "canonical_id": f"urn:eoip:work:comment:jira:{self.connector.source_id}:{comment_id}",
                "properties": {
                    **common,
                    "comment_id": comment_id,
                    "content": self._text(record.get("body")),
                    "created_at": record.get("created"),
                    "modified_at": record.get("updated"),
                },
                "issue_key": issue_key,
                "author": record.get("author"),
            }
        if kind == "changelog":
            issue_key = str(record.get("issue_key") or record_id.split(":", 1)[0])
            change_id = f"{record.get('history_id', record_id)}:{record.get('item_index', 0)}"
            field_name = str(record.get("fieldId") or record.get("field") or "unknown")
            return {
                "kind": kind,
                "label": "WorkItemChange",
                "canonical_id": (
                    f"urn:eoip:work:change:jira:{self.connector.source_id}:{issue_key}:{change_id}"
                ),
                "properties": {
                    **common,
                    "change_id": change_id,
                    "field_name": field_name,
                    "from_value": self._string(record.get("fromString") or record.get("from")),
                    "to_value": self._string(record.get("toString") or record.get("to")),
                    "created_at": record.get("created"),
                },
                "issue_key": issue_key,
                "project_key": project_key,
                "field_name": field_name.casefold(),
                "from_id": record.get("from"),
                "from_name": record.get("fromString"),
                "to_id": record.get("to"),
                "to_name": record.get("toString"),
                "author": record.get("author"),
            }
        raise ValueError(f"unsupported Jira record kind: {kind}")

    def _write_graph(self, accepted, run_id: str, started_at: str, rejected_count: int) -> None:
        run = self.store.upsert_vertex(
            "IngestionRun",
            {
                "canonical_id": f"urn:eoip:meta:ingestion-run:{run_id}",
                "run_status": "PARTIAL" if rejected_count else "SUCCEEDED",
                "run_kind": "JIRA",
                "source_system": "jira",
                "ingestion_run_id": run_id,
                "started_at": started_at,
                "finished_at": utc_now_iso(),
                "counts": json.dumps({"accepted": len(accepted), "rejected": rejected_count}),
            },
        )
        linked = []
        for event, mapped in accepted:
            result = self.evolution.evolve_entity(
                mapped["label"], mapped["canonical_id"], mapped["properties"], event
            )
            if result["status"] == "DELETE":
                continue
            entity = self.store.get_vertex_by_canonical_id(mapped["canonical_id"])
            if entity is None:
                raise RuntimeError("Jira graph evolution did not produce current entity")
            evidence = self.store.upsert_vertex(
                "Evidence",
                {
                    "canonical_id": f"urn:eoip:evidence:source-event:jira:{event.event_id}",
                    "source_system": "jira",
                    "source_ref": f"jira://{event.source_record_id}",
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
                "source_system": "jira",
                "creation_status": "DETERMINISTIC",
            }
            self.store.upsert_edge(
                "EVIDENCED_BY",
                entity["vid"],
                evidence["vid"],
                {**edge_props, "fact_key": event.event_id, "ingestion_run_id": run_id},
            )
            self.store.upsert_edge(
                "INGESTED_IN",
                entity["vid"],
                run["vid"],
                {
                    **edge_props,
                    "fact_key": f"{run_id}:{mapped['canonical_id']}",
                    "ingestion_run_id": run_id,
                },
            )
            self._link_entity(mapped, entity, event, edge_props)
            if mapped["kind"] == "issue":
                linked.append((mapped, entity, event, edge_props))
        for mapped, entity, event, edge_props in linked:
            self._link_issue_dependencies(mapped, entity, event, edge_props)

    def _link_entity(self, mapped: dict, entity: dict, event: SourceEventV2, props: dict) -> None:
        kind = mapped["kind"]
        project_key = mapped.get("project_key")
        project = self.store.get_vertex_by_canonical_id(self._project_id(project_key)) if project_key else None
        project_relation = {
            "issue_type": "HAS_ISSUE_TYPE",
            "status": "HAS_STATUS",
            "version": "HAS_VERSION",
            "sprint": "HAS_SPRINT",
            "issue": "CONTAINS",
        }.get(kind)
        if project and project_relation:
            self._relationship(
                f"jira:{project_relation}:{project['canonical_id']}:{entity['canonical_id']}",
                project_relation,
                project["canonical_id"],
                entity["canonical_id"],
                props,
                event,
            )
        if kind in {"comment", "changelog"}:
            issue_id = self._issue_id(mapped["issue_key"])
            if not self.store.get_vertex_by_canonical_id(issue_id):
                self.evolution.evolve_entity(
                    "WorkItem",
                    issue_id,
                    {
                        "issue_key": mapped["issue_key"],
                        "summary": mapped["issue_key"],
                        "source_system": "jira",
                        "registry_source_id": self.connector.source_id,
                    },
                    event,
                )
            if self.store.get_vertex_by_canonical_id(issue_id):
                relation = "HAS_COMMENT" if kind == "comment" else "HAS_CHANGE"
                self._relationship(
                    f"jira:{relation}:{issue_id}:{entity['canonical_id']}",
                    relation,
                    issue_id,
                    entity["canonical_id"],
                    props,
                    event,
                )
            author_id = self._ensure_person(mapped.get("author"), event)
            if author_id:
                self._relationship(
                    f"jira:authored:{entity['canonical_id']}",
                    "AUTHORED_BY",
                    entity["canonical_id"],
                    author_id,
                    props,
                    event,
                )
        if kind == "changelog":
            self._apply_change(mapped, event, props)
        if kind == "issue":
            self._apply_current_state(mapped, event, props)

    def _link_issue_dependencies(
        self,
        mapped: dict,
        entity: dict,
        event: SourceEventV2,
        props: dict,
    ) -> None:
        issue_key = mapped["issue_key"]
        parent_key = mapped.get("parent_key")
        if parent_key and self.store.get_vertex_by_canonical_id(self._issue_id(parent_key)):
            self._relationship(
                f"jira:parent:{parent_key}:{issue_key}",
                "PARENT_OF",
                self._issue_id(parent_key),
                entity["canonical_id"],
                props,
                event,
            )
        issue_type = mapped.get("issue_type") or {}
        if issue_type.get("id"):
            target = self._issue_type_id(mapped["project_key"], str(issue_type["id"]))
            if self.store.get_vertex_by_canonical_id(target):
                self._relationship(
                    f"jira:issue-type:{issue_key}",
                    "OF_TYPE",
                    entity["canonical_id"],
                    target,
                    props,
                    event,
                )
        for version in mapped.get("versions", []):
            target = self._version_id(mapped["project_key"], str(version.get("id")))
            if self.store.get_vertex_by_canonical_id(target):
                self._relationship(
                    f"jira:fixed-in:{issue_key}:{version.get('id')}",
                    "FIXED_IN",
                    entity["canonical_id"],
                    target,
                    props,
                    event,
                )
        for sprint in mapped.get("sprints", []):
            target = self._sprint_id(mapped["project_key"], str(sprint.get("id")))
            if self.store.get_vertex_by_canonical_id(target):
                self._relationship(
                    f"jira:in-sprint:{issue_key}:{sprint.get('id')}",
                    "IN_SPRINT",
                    entity["canonical_id"],
                    target,
                    props,
                    event,
                )
        for link in mapped.get("links", []):
            self._link_issue_link(issue_key, link, event, props)

    def _apply_current_state(self, mapped: dict, event: SourceEventV2, props: dict) -> None:
        issue_id = mapped["canonical_id"]
        project_key = mapped["project_key"]
        status = mapped.get("status") or {}
        if status.get("id"):
            status_id = self._ensure_status(project_key, str(status["id"]), status.get("name"), event)
            self._relationship(
                f"jira:status:{mapped['issue_key']}",
                "HAS_STATUS",
                issue_id,
                status_id,
                props,
                event,
            )
        self._person_state(
            f"jira:assignment:{mapped['issue_key']}",
            "ASSIGNED_TO",
            issue_id,
            mapped.get("assignee"),
            event,
            props,
        )
        self._person_state(
            f"jira:reporter:{mapped['issue_key']}",
            "REPORTED_BY",
            issue_id,
            mapped.get("reporter"),
            event,
            props,
        )

    def _apply_change(self, mapped: dict, event: SourceEventV2, props: dict) -> None:
        issue_id = self._issue_id(mapped["issue_key"])
        if not self.store.get_vertex_by_canonical_id(issue_id):
            return
        field = mapped["field_name"]
        if field in {"status", "statusid"}:
            if mapped.get("to_id") or mapped.get("to_name"):
                status_id = str(mapped.get("to_id") or mapped.get("to_name"))
                target = self._ensure_status(
                    mapped["project_key"], status_id, mapped.get("to_name"), event
                )
                self._relationship(
                    f"jira:status:{mapped['issue_key']}",
                    "HAS_STATUS",
                    issue_id,
                    target,
                    props,
                    event,
                )
        elif field in {"assignee", "reporter"}:
            relation = "ASSIGNED_TO" if field == "assignee" else "REPORTED_BY"
            self._person_state(
                f"jira:{field}:{mapped['issue_key']}",
                relation,
                issue_id,
                {"accountId": mapped.get("to_id"), "displayName": mapped.get("to_name")}
                if mapped.get("to_id") or mapped.get("to_name")
                else None,
                event,
                props,
            )

    def _person_state(
        self,
        relationship_id: str,
        relation: str,
        issue_id: str,
        person: object,
        event: SourceEventV2,
        props: dict,
    ) -> None:
        target = self._ensure_person(person, event)
        if target:
            self._relationship(relationship_id, relation, issue_id, target, props, event)
            return
        deletion = event.model_copy(update={"operation": "DELETE"})
        self.evolution.evolve_relationship(
            relationship_id,
            relation,
            issue_id,
            "",
            props,
            deletion,
        )

    def _ensure_person(self, value: object, event: SourceEventV2) -> str | None:
        if not isinstance(value, dict):
            return None
        identifier = value.get("accountId") or value.get("key") or value.get("name")
        display_name = value.get("displayName") or value.get("name")
        if not identifier and not display_name:
            return None
        identity = str(identifier or display_name).strip().casefold()
        canonical_id = f"urn:eoip:identity:person:jira:{self.connector.source_id}:{identity}"
        self.evolution.evolve_entity(
            "Person",
            canonical_id,
            {
                "display_name": display_name or identity,
                "email": value.get("emailAddress"),
                "source_system": "jira",
                "external_id": str(identifier or identity),
            },
            event,
        )
        return canonical_id

    def _ensure_status(
        self,
        project_key: str,
        status_id: str,
        name: object,
        event: SourceEventV2,
    ) -> str:
        canonical_id = self._status_id(project_key, status_id)
        self.evolution.evolve_entity(
            "Status",
            canonical_id,
            {
                "status_id": status_id,
                "name": str(name or status_id),
                "project_key": project_key,
                "source_system": "jira",
            },
            event,
        )
        return canonical_id

    def _link_issue_link(
        self,
        issue_key: str,
        link: dict,
        event: SourceEventV2,
        props: dict,
    ) -> None:
        link_type = link.get("type") if isinstance(link.get("type"), dict) else {}
        outward = link.get("outwardIssue") if isinstance(link.get("outwardIssue"), dict) else None
        inward = link.get("inwardIssue") if isinstance(link.get("inwardIssue"), dict) else None
        if outward:
            from_key, to_key, direction = issue_key, str(outward.get("key")), "outward"
            description = link_type.get("outward") or link_type.get("name")
        elif inward:
            from_key, to_key, direction = str(inward.get("key")), issue_key, "inward"
            description = link_type.get("outward") or link_type.get("name")
        else:
            return
        if not to_key or not self.store.get_vertex_by_canonical_id(self._issue_id(from_key)):
            return
        if not self.store.get_vertex_by_canonical_id(self._issue_id(to_key)):
            return
        normalized = str(link_type.get("name") or description or "references").casefold()
        relation = (
            "BLOCKS"
            if "block" in normalized
            else "DUPLICATES"
            if "duplicate" in normalized
            else "CLONES"
            if "clone" in normalized
            else "REFERENCES"
        )
        relation_props = {
            **props,
            "link_type": str(link_type.get("name") or description or relation),
            "link_direction": direction,
        }
        relationship_id = str(link.get("id") or f"{relation}:{from_key}:{to_key}")
        self._relationship(
            f"jira:issue-link:{relationship_id}",
            relation,
            self._issue_id(from_key),
            self._issue_id(to_key),
            relation_props,
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

    def _sprints(self, fields: dict) -> list[dict]:
        candidates = []
        for key, value in fields.items():
            values = value if isinstance(value, list) else [value]
            for item in values:
                if not isinstance(item, dict):
                    continue
                if item.get("id") is not None and (
                    key.casefold() == "sprint"
                    or "sprint" in key.casefold()
                    or "originBoardId" in item
                ):
                    candidates.append(item)
        return candidates

    @staticmethod
    def _text(value: object) -> str | None:
        if value is None:
            return None
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            pieces = []
            if isinstance(value.get("text"), str):
                pieces.append(value["text"])
            for child in value.get("content") or []:
                text = JiraTemporalIngestionService._text(child)
                if text:
                    pieces.append(text)
            return " ".join(pieces) or json.dumps(value, sort_keys=True)
        if isinstance(value, list):
            return " ".join(filter(None, (JiraTemporalIngestionService._text(item) for item in value)))
        return str(value)

    @staticmethod
    def _string(value: object) -> str | None:
        return None if value is None else str(value)

    @staticmethod
    def _issue_id(key: str) -> str:
        return f"urn:eoip:work:item:jira:{key}"

    @staticmethod
    def _project_id(key: str) -> str:
        return f"urn:eoip:work:project:jira:{key}"

    def _issue_type_id(self, project: str, value: str) -> str:
        return f"urn:eoip:work:issue-type:jira:{self.connector.source_id}:{project}:{value}"

    def _status_id(self, project: str, value: str) -> str:
        return f"urn:eoip:work:status:jira:{self.connector.source_id}:{project}:{value}"

    def _version_id(self, project: str, value: str) -> str:
        return f"urn:eoip:work:version:jira:{self.connector.source_id}:{project}:{value}"

    def _sprint_id(self, project: str, value: str) -> str:
        return f"urn:eoip:work:sprint:jira:{self.connector.source_id}:{project}:{value}"

    def _write_dlq(self, event: SourceEventV2, error: str) -> None:
        self.dlq_root.mkdir(parents=True, exist_ok=True)
        path = self.dlq_root / f"{event.event_id}.json"
        if path.exists():
            return
        path.write_text(
            json.dumps(
                {
                    "event_id": event.event_id,
                    "source_system": "jira",
                    "source_record_id": event.source_record_id,
                    "payload_hash": event.payload_hash,
                    "error_category": "mapping_error",
                    "error": error,
                    "replay_ref": str(self.capture.root / "jira" / f"{event.event_id}.json"),
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )


def run_registered_jira_operation(entry, payload, store, data_root, correlation_id) -> dict:
    from eoip.connectors.config import connector_from_registry

    root = Path(data_root)
    connector = connector_from_registry(entry, correlation_id=correlation_id)
    if not isinstance(connector, JiraConnector):
        raise TypeError("registered Jira source did not create a Jira connector")
    operation = payload.get("operation")
    if operation not in {"BASELINE", "POLL", "RECONCILE", "REPLAY"}:
        raise ValueError(f"unsupported Jira source operation: {operation}")
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
                    "source_type": "jira",
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
                path = root / "raw" / "jira" / f"{event_id}.json"
                if not path.exists():
                    raise ValueError(f"captured Jira event is unavailable: {event_id}")
                events.append(SourceEventV2.model_validate_json(path.read_text(encoding="utf-8")))
        service = JiraTemporalIngestionService(
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
                    "source_system": "jira",
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
