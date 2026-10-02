"""Jira JSON source adapter; it emits SourceEvents and never writes the graph."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from typing import Any

from eoip.contracts.source_event import SourceEvent

DEFAULT_MAPPING = {
    "issue_key": "key",
    "summary": "fields.summary",
    "description": "fields.description",
    "issue_type": "fields.issuetype.name",
    "status": "fields.status.name",
    "project_key": "fields.project.key",
    "project_name": "fields.project.name",
    "assignee_id": "fields.assignee.accountId",
    "assignee_name": "fields.assignee.displayName",
    "assignee_email": "fields.assignee.emailAddress",
    "parent_key": "fields.parent.key",
}


class JiraJsonConnector:
    mapper_version = "jira-json/1.0"

    def __init__(self, mapping: dict[str, str] | None = None) -> None:
        self.mapping = {**DEFAULT_MAPPING, **(mapping or {})}

    @classmethod
    def from_yaml(cls, path: str) -> JiraJsonConnector:
        import yaml

        with open(path, encoding="utf-8") as mapping_file:
            document = yaml.safe_load(mapping_file)
        if not isinstance(document, dict):
            raise TypeError("Jira mapping must be a YAML object")
        fields = document.get("fields")
        if fields is None:
            raise ValueError("Jira mapping must contain a fields object")
        if not isinstance(fields, dict):
            raise TypeError("Jira mapping fields must be an object")
        return cls(fields)

    def source_records(self, document: Any) -> list[dict]:
        if isinstance(document, list):
            records = document
        elif isinstance(document, dict):
            records = document.get("issues", document.get("values"))
        else:
            raise TypeError("Jira JSON must be a list or object")
        if records is None:
            raise ValueError("Jira JSON must be a list or contain an issues/values list")
        if not isinstance(records, list):
            raise TypeError("Jira issues/values must be a list")
        return [record if isinstance(record, dict) else {"_invalid_record": record} for record in records]

    def events(self, records: Iterable[dict]) -> list[SourceEvent]:
        events = []
        for index, record in enumerate(records):
            issue_key = self._value(record, "issue_key")
            source_id = str(issue_key) if issue_key else f"row-{index + 1}"
            payload_json = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            payload_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
            event_id = hashlib.sha256(f"jira:{source_id}:{payload_hash}".encode()).hexdigest()
            events.append(
                SourceEvent(
                    event_id=event_id,
                    source_system="jira",
                    source_record_id=source_id,
                    source_version=payload_hash,
                    payload_hash=payload_hash,
                    payload=record,
                    metadata={"mapper_version": self.mapper_version},
                )
            )
        return events

    def map_event(self, event: SourceEvent) -> dict[str, Any]:
        record = event.payload
        issue_key = self._value(record, "issue_key")
        summary = self._value(record, "summary")
        if not isinstance(issue_key, str) or not issue_key.strip():
            raise ValueError("missing required Jira issue key")
        if not isinstance(summary, str) or not summary.strip():
            raise ValueError(f"{issue_key}: missing required summary")
        project_key = self._value(record, "project_key") or issue_key.split("-", 1)[0]
        project_name = self._value(record, "project_name") or project_key
        return {
            "issue_key": issue_key.strip(),
            "summary": summary.strip(),
            "description": self._value(record, "description"),
            "issue_type": self._value(record, "issue_type"),
            "status": self._value(record, "status"),
            "project_key": str(project_key),
            "project_name": str(project_name),
            "assignee_id": self._value(record, "assignee_id"),
            "assignee_name": self._value(record, "assignee_name"),
            "assignee_email": self._value(record, "assignee_email"),
            "parent_key": self._value(record, "parent_key"),
        }

    def _value(self, record: dict, field: str) -> Any:
        value: Any = record
        for part in self.mapping[field].split("."):
            if not isinstance(value, dict):
                return None
            value = value.get(part)
        return value