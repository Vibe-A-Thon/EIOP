"""ServiceNow Table API connector emitting SourceEvents for operations records."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any

from eoip.connectors.errors import ConnectorError
from eoip.connectors.rest import RestConnector, parse_utc, utc_timestamp
from eoip.connectors.sync import SyncBatch

DEFAULT_TABLES = {
    "incident": "incident",
    "problem": "problem",
    "change": "change_request",
    "knowledge": "kb_knowledge",
}

DEFAULT_FIELDS = {
    "record_id": "sys_id",
    "number": "number",
    "short_description": "short_description",
    "description": "description",
    "state": "state",
    "updated_at": "sys_updated_on",
}
TABLE_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


class ServiceNowConnector(RestConnector):
    source_system = "servicenow"
    mapper_version = "servicenow-table-api/1.0"

    def __init__(
        self,
        base_url: str,
        *,
        tables: dict[str, str] | None = None,
        field_mapping: dict[str, str] | None = None,
        page_size: int = 500,
        **kwargs,
    ) -> None:
        if not 1 <= page_size <= 10000:
            raise ValueError("page_size must be between 1 and 10000")
        self.tables = {**DEFAULT_TABLES, **(tables or {})}
        if not self.tables or any(not TABLE_NAME.fullmatch(table) for table in self.tables.values()):
            raise ValueError("ServiceNow table names must be simple identifiers")
        self.field_mapping = {**DEFAULT_FIELDS, **(field_mapping or {})}
        super().__init__(base_url, **kwargs)
        self.page_size = page_size

    def sync(
        self,
        *,
        checkpoint: str | None = None,
        watermark: str | None = None,
        correlation_id: str | None = None,
    ) -> SyncBatch:
        correlation_id = self.correlation_id(correlation_id)
        watermark_dt = parse_utc(watermark) if watermark else datetime.now(UTC)
        if watermark_dt is None:
            raise ValueError("invalid ServiceNow watermark")
        next_checkpoint = utc_timestamp(watermark_dt)
        checkpoint_dt = parse_utc(checkpoint)
        query_parts = []
        if checkpoint_dt:
            query_parts.append(f"sys_updated_on>={self._sn_time(checkpoint_dt)}")
        query_parts.extend(
            [
                f"sys_updated_on<={self._sn_time(watermark_dt)}",
                "ORDERBYsys_updated_on",
                "ORDERBYsys_id",
            ]
        )
        query = "^".join(query_parts)
        events = []
        for record_kind, table in self.tables.items():
            offset = 0
            while True:
                response = self.get_json(
                    f"/api/now/table/{table}",
                    params={
                        "sysparm_query": query,
                        "sysparm_limit": self.page_size,
                        "sysparm_offset": offset,
                        "sysparm_display_value": "false",
                        "sysparm_exclude_reference_link": "true",
                    },
                    correlation_id=correlation_id,
                )
                records = response.get("result")
                if not isinstance(records, list) or any(not isinstance(record, dict) for record in records):
                    self._log_failure("invalid_response", correlation_id)
                    raise ConnectorError(self.source_system, "invalid_response", correlation_id)
                if not records:
                    break
                for record in records:
                    record_id = record.get("sys_id")
                    if record_id is None or not str(record_id).strip():
                        self._log_failure("schema_drift", correlation_id)
                        raise ConnectorError(self.source_system, "schema_drift", correlation_id)
                    version = record.get("sys_updated_on") or record.get("sys_mod_count")
                    events.append(
                        self.make_event(
                            record_kind,
                            f"{self.instance_id}:{table}:{record_id}",
                            record,
                            version,
                        )
                    )
                offset += len(records)
                if len(records) < self.page_size:
                    break
        return SyncBatch(events=events, next_checkpoint=next_checkpoint)

    def map_event(self, event) -> dict[str, Any]:
        record = event.payload
        kind = (event.metadata or {}).get("record_kind")
        if kind not in self.tables:
            raise ValueError("unsupported ServiceNow record kind")
        record_id = record.get(self.field_mapping["record_id"])
        number = record.get(self.field_mapping["number"])
        if record_id is None or not str(record_id).strip():
            raise ValueError("ServiceNow record requires sys_id")
        if number is None or not str(number).strip():
            raise ValueError("ServiceNow record requires number")
        return {
            "kind": kind,
            "record_id": str(record_id),
            "number": str(number),
            "short_description": record.get(self.field_mapping["short_description"]),
            "description": record.get(self.field_mapping["description"]),
            "state": record.get(self.field_mapping["state"]),
            "updated_at": record.get(self.field_mapping["updated_at"]),
        }

    @staticmethod
    def _sn_time(value) -> str:
        return value.astimezone(UTC).strftime("%Y-%m-%d %H:%M:%S")
