"""GitLab JSON fixture adapter emitting immutable SourceEvents."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable
from typing import Any

from eoip.contracts.source_event import SourceEvent

ISSUE_KEY_PATTERN = re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")


class GitLabJsonConnector:
    mapper_version = "gitlab-json/1.0"

    def records(self, document: Any) -> list[tuple[str, dict]]:
        if not isinstance(document, dict):
            raise TypeError("GitLab fixture must be a JSON object")
        records = []
        for key, kind in (("merge_requests", "merge_request"), ("pipelines", "pipeline")):
            values = document.get(key, [])
            if not isinstance(values, list):
                raise TypeError(f"GitLab {key} must be a list")
            records.extend((kind, value if isinstance(value, dict) else {"_invalid_record": value}) for value in values)
        return records

    def events(self, records: Iterable[tuple[str, dict]]) -> list[SourceEvent]:
        events = []
        for index, (kind, record) in enumerate(records):
            source_id = record.get("iid" if kind == "merge_request" else "id")
            stable_source_id = str(source_id) if source_id is not None else f"{kind}-row-{index + 1}"
            payload_json = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            payload_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
            event_id = hashlib.sha256(f"gitlab:{kind}:{stable_source_id}:{payload_hash}".encode()).hexdigest()
            events.append(
                SourceEvent(
                    event_id=event_id,
                    source_system="gitlab",
                    source_record_id=f"{kind}:{stable_source_id}",
                    source_version=payload_hash,
                    payload_hash=payload_hash,
                    payload=record,
                    metadata={"mapper_version": self.mapper_version, "record_kind": kind},
                )
            )
        return events

    def map_event(self, event: SourceEvent) -> dict:
        record = event.payload
        kind = (event.metadata or {}).get("record_kind")
        if kind == "merge_request":
            iid = record.get("iid")
            title = record.get("title")
            if iid is None or not isinstance(title, str) or not title.strip():
                raise ValueError("merge request requires iid and title")
            issue_keys = _issue_keys(
                record.get("work_item_keys", []),
                record.get("source_branch", ""),
                title,
                record.get("description", ""),
            )
            return {
                "kind": kind,
                "source_id": str(iid),
                "title": title.strip(),
                "status": record.get("state", record.get("status")),
                "source_branch": record.get("source_branch"),
                "target_branch": record.get("target_branch"),
                "commit_sha": record.get("merge_commit_sha") or record.get("sha") or record.get("commit_sha"),
                "work_item_keys": issue_keys,
            }
        if kind == "pipeline":
            pipeline_id = record.get("id")
            if pipeline_id is None:
                raise ValueError("pipeline requires id")
            issue_keys = _issue_keys(
                record.get("work_item_keys", []),
                record.get("ref", ""),
                record.get("name", ""),
            )
            return {
                "kind": kind,
                "source_id": str(pipeline_id),
                "name": str(record.get("name") or f"pipeline-{pipeline_id}"),
                "status": record.get("status"),
                "ref": record.get("ref"),
                "commit_sha": record.get("sha") or record.get("commit_sha"),
                "work_item_keys": issue_keys,
            }
        raise ValueError("unsupported GitLab record kind")


def _issue_keys(explicit: Any, *text_values: Any) -> list[str]:
    keys = set()
    if isinstance(explicit, list):
        keys.update(value for value in explicit if isinstance(value, str) and ISSUE_KEY_PATTERN.fullmatch(value))
    for value in text_values:
        if isinstance(value, str):
            keys.update(ISSUE_KEY_PATTERN.findall(value))
    return sorted(keys)
