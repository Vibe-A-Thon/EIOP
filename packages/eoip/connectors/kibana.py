"""Kibana Saved Objects API connector emitting SourceEvents for dashboards and index patterns."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from eoip.connectors.errors import ConnectorError
from eoip.connectors.rest import RestConnector, parse_utc, utc_timestamp
from eoip.connectors.sync import SyncBatch

KIBANA_OBJECT_TYPES = {
    "dashboard": "dashboard",
    "search": "search",
    "index_pattern": "index-pattern",
}


class KibanaConnector(RestConnector):
    """Connector for Kibana via the Saved Objects API."""

    source_system = "kibana"
    mapper_version = "kibana-saved-objects/1.0"

    def __init__(
        self,
        base_url: str,
        *,
        object_types: dict[str, str] | None = None,
        page_size: int = 100,
        space_id: str | None = None,
        **kwargs,
    ) -> None:
        if not 1 <= page_size <= 10000:
            raise ValueError("page_size must be between 1 and 10000")
        self.object_types = {**KIBANA_OBJECT_TYPES, **(object_types or {})}
        self.space_id = space_id
        super().__init__(base_url, **kwargs)
        self.page_size = page_size

    @property
    def _api_prefix(self) -> str:
        if self.space_id:
            return f"/s/{self.space_id}/api"
        return "/api"

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
            raise ValueError("invalid Kibana watermark")
        next_checkpoint = utc_timestamp(watermark_dt)

        events = []
        for record_kind, kibana_type in self.object_types.items():
            page = 1
            while True:
                response = self.get_json(
                    f"{self._api_prefix}/saved_objects/_find",
                    params={
                        "type": kibana_type,
                        "per_page": self.page_size,
                        "page": page,
                        "sort_field": "updated_at",
                        "sort_order": "asc",
                    },
                    correlation_id=correlation_id,
                )

                saved_objects = response.get("saved_objects")
                if not isinstance(saved_objects, list):
                    self._log_failure("invalid_response", correlation_id)
                    raise ConnectorError(self.source_system, "invalid_response", correlation_id)

                if not saved_objects:
                    break

                for obj in saved_objects:
                    if not isinstance(obj, dict):
                        continue
                    object_id = obj.get("id")
                    if object_id is None or not str(object_id).strip():
                        self._log_failure("schema_drift", correlation_id)
                        raise ConnectorError(self.source_system, "schema_drift", correlation_id)
                    version = obj.get("version") or obj.get("updated_at")
                    events.append(
                        self.make_event(
                            record_kind,
                            f"{self.instance_id}:{kibana_type}:{object_id}",
                            obj,
                            version,
                        )
                    )

                total = response.get("total", 0)
                if page * self.page_size >= total:
                    break
                page += 1

        return SyncBatch(events=events, next_checkpoint=next_checkpoint)

    def map_event(self, event) -> dict[str, Any]:
        record = event.payload
        kind = (event.metadata or {}).get("record_kind")
        if kind not in self.object_types:
            raise ValueError("unsupported Kibana record kind")
        object_id = record.get("id")
        if object_id is None or not str(object_id).strip():
            raise ValueError("Kibana saved object requires id")
        attributes = record.get("attributes", {})
        if not isinstance(attributes, dict):
            attributes = {}
        return {
            "kind": kind,
            "object_id": str(object_id),
            "title": attributes.get("title") or record.get("title"),
            "type": record.get("type"),
        }
