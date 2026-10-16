"""EKAF schema and mapping drift helpers (G2-EKAF-017/G2-EKAF-018)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from eoip.contracts.source_event import utc_now_iso
from eoip.jobs import write_json
from pydantic import BaseModel, ConfigDict, Field

DriftClassification = Literal["compatible", "additive", "potentially_breaking", "breaking"]


class SchemaDriftReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    classification: DriftClassification
    added_paths: list[str] = Field(default_factory=list)
    removed_paths: list[str] = Field(default_factory=list)
    changed_type_paths: dict[str, dict[str, str]] = Field(default_factory=dict)


class MappingDriftRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    drift_id: str = Field(default_factory=lambda: str(uuid4()))
    source_id: str = Field(min_length=1, max_length=128)
    previous_mapping_version: str | None = Field(default=None, max_length=128)
    new_mapping_version: str = Field(min_length=1, max_length=128)
    changed_at: str = Field(default_factory=utc_now_iso)
    replay_from_checkpoint: str | None = Field(default=None, max_length=4096)
    event_ids: list[str] = Field(default_factory=list, max_length=1000)
    correlation_id: str | None = Field(default=None, max_length=128)
    note: str | None = Field(default=None, max_length=1024)


class MappingReplayPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str
    records: list[MappingDriftRecord]
    replay_from_checkpoint: str | None = None
    event_ids: list[str] = Field(default_factory=list)


def infer_payload_schema(payload: Any) -> dict[str, str]:
    """Return a stable JSON-path to kind map for a representative source payload."""

    paths: dict[str, str] = {}

    def visit(value: Any, path: str) -> None:
        paths[path] = _kind(value)
        if isinstance(value, dict):
            for key in sorted(value):
                visit(value[key], f"{path}.{_escape_path(key)}")
        elif isinstance(value, list):
            paths[f"{path}[]"] = "array_item" if value else "empty_array"
            for item in value:
                visit(item, f"{path}[]")

    visit(payload, "$")
    return dict(sorted(paths.items()))


def classify_schema_drift(previous_schema: dict[str, str], current_schema: dict[str, str]) -> SchemaDriftReport:
    """Classify source schema drift without promoting it to acceptance/completion."""

    previous_paths = set(previous_schema)
    current_paths = set(current_schema)
    added = sorted(current_paths - previous_paths)
    removed = sorted(previous_paths - current_paths)
    changed = {
        path: {"previous": previous_schema[path], "current": current_schema[path]}
        for path in sorted(previous_paths & current_paths)
        if previous_schema[path] != current_schema[path]
    }
    if removed:
        classification: DriftClassification = "breaking"
    elif any(_container_kind(item["previous"]) != _container_kind(item["current"]) for item in changed.values()):
        classification = "breaking"
    elif changed:
        classification = "potentially_breaking"
    elif added:
        classification = "additive"
    else:
        classification = "compatible"
    return SchemaDriftReport(
        classification=classification,
        added_paths=added,
        removed_paths=removed,
        changed_type_paths=changed,
    )


def classify_payload_drift(previous_payload: Any, current_payload: Any) -> SchemaDriftReport:
    return classify_schema_drift(
        infer_payload_schema(previous_payload),
        infer_payload_schema(current_payload),
    )


class MappingDriftLedger:
    """Durable local ledger for mapping-version transitions and replay planning."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def record(
        self,
        *,
        source_id: str,
        previous_mapping_version: str | None,
        new_mapping_version: str,
        replay_from_checkpoint: str | None = None,
        event_ids: list[str] | None = None,
        correlation_id: str | None = None,
        note: str | None = None,
    ) -> MappingDriftRecord | None:
        if previous_mapping_version == new_mapping_version:
            return None
        record = MappingDriftRecord(
            source_id=source_id,
            previous_mapping_version=previous_mapping_version,
            new_mapping_version=new_mapping_version,
            replay_from_checkpoint=replay_from_checkpoint,
            event_ids=event_ids or [],
            correlation_id=correlation_id,
            note=note,
        )
        records = self.list()
        records.append(record)
        self._write(records)
        return record

    def list(self, source_id: str | None = None) -> list[MappingDriftRecord]:
        if not self.path.exists():
            return []
        document = json.loads(self.path.read_text(encoding="utf-8"))
        if document.get("schema_version") != "1.0" or not isinstance(document.get("records"), list):
            raise ValueError("invalid mapping drift ledger")
        records = [MappingDriftRecord.model_validate(item) for item in document["records"]]
        if source_id is not None:
            records = [record for record in records if record.source_id == source_id]
        return records

    def replay_plan(self, source_id: str) -> MappingReplayPlan:
        records = self.list(source_id)
        checkpoints = [record.replay_from_checkpoint for record in records if record.replay_from_checkpoint]
        event_ids = sorted({event_id for record in records for event_id in record.event_ids})
        return MappingReplayPlan(
            source_id=source_id,
            records=records,
            replay_from_checkpoint=checkpoints[0] if checkpoints else None,
            event_ids=event_ids,
        )

    def _write(self, records: list[MappingDriftRecord]) -> None:
        write_json(
            self.path,
            {
                "schema_version": "1.0",
                "records": [record.model_dump(mode="json") for record in records],
            },
        )


def _kind(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    return type(value).__name__


def _container_kind(kind: str) -> str:
    return kind if kind in {"object", "array"} else "scalar"


def _escape_path(key: str) -> str:
    return key.replace("~", "~0").replace(".", "~1")
