"""Rally (Broadcom) REST connector emitting SourceEvents for agile work items."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from eoip.connectors.errors import ConnectorError
from eoip.connectors.rest import RestConnector, parse_utc, utc_timestamp
from eoip.connectors.sync import SyncBatch

RALLY_TYPES = {
    "user_story": "HierarchicalRequirement",
    "feature": "PortfolioItem/Feature",
    "epic": "PortfolioItem/Epic",
}


class RallyConnector(RestConnector):
    """Connector for Rally (Broadcom Agile Central) via WSAPI v2.0."""

    source_system = "rally"
    mapper_version = "rally-wsapi/1.0"

    def __init__(
        self,
        base_url: str,
        *,
        workspace: str | None = None,
        project: str | None = None,
        types: dict[str, str] | None = None,
        page_size: int = 200,
        **kwargs,
    ) -> None:
        if not 1 <= page_size <= 2000:
            raise ValueError("page_size must be between 1 and 2000")
        self.workspace = workspace
        self.project = project
        self.types = {**RALLY_TYPES, **(types or {})}
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
            raise ValueError("invalid Rally watermark")
        next_checkpoint = utc_timestamp(watermark_dt)
        checkpoint_dt = parse_utc(checkpoint)

        events = []
        for record_kind, rally_type in self.types.items():
            start = 1  # Rally pagination is 1-based
            while True:
                query_parts = []
                if checkpoint_dt:
                    query_parts.append(
                        f"(LastUpdateDate >= {checkpoint_dt.strftime('%Y-%m-%dT%H:%M:%SZ')})"
                    )
                query_parts.append(
                    f"(LastUpdateDate <= {watermark_dt.strftime('%Y-%m-%dT%H:%M:%SZ')})"
                )
                query_filter = " AND ".join(query_parts) if query_parts else ""

                params: dict[str, str | int] = {
                    "start": start,
                    "pagesize": self.page_size,
                    "fetch": "true",
                    "order": "LastUpdateDate ASC",
                }
                if query_filter:
                    params["query"] = f"({query_filter})"
                if self.workspace:
                    params["workspace"] = self.workspace
                if self.project:
                    params["project"] = self.project

                response = self.get_json(
                    f"/slm/webservice/v2.0/{rally_type}",
                    params=params,
                    correlation_id=correlation_id,
                )

                query_result = response.get("QueryResult")
                if not isinstance(query_result, dict):
                    self._log_failure("invalid_response", correlation_id)
                    raise ConnectorError(self.source_system, "invalid_response", correlation_id)

                records = query_result.get("Results")
                if not isinstance(records, list):
                    self._log_failure("invalid_response", correlation_id)
                    raise ConnectorError(self.source_system, "invalid_response", correlation_id)

                if not records:
                    break

                for record in records:
                    if not isinstance(record, dict):
                        continue
                    object_id = record.get("ObjectID")
                    if object_id is None:
                        self._log_failure("schema_drift", correlation_id)
                        raise ConnectorError(self.source_system, "schema_drift", correlation_id)
                    version = record.get("VersionId") or record.get("LastUpdateDate")
                    events.append(
                        self.make_event(
                            record_kind,
                            f"{self.instance_id}:{rally_type}:{object_id}",
                            record,
                            version,
                        )
                    )

                total = int(query_result.get("TotalResultCount", 0))
                start += len(records)
                if start > total:
                    break

        return SyncBatch(events=events, next_checkpoint=next_checkpoint)

    def map_event(self, event) -> dict[str, Any]:
        record = event.payload
        kind = (event.metadata or {}).get("record_kind")
        if kind not in self.types:
            raise ValueError("unsupported Rally record kind")
        object_id = record.get("ObjectID")
        if object_id is None:
            raise ValueError("Rally record requires ObjectID")
        return {
            "kind": kind,
            "record_id": str(object_id),
            "name": record.get("Name"),
            "description": record.get("Description"),
            "schedule_state": record.get("ScheduleState"),
            "plan_estimate": record.get("PlanEstimate"),
            "formatted_id": record.get("FormattedID"),
            "iteration": record.get("Iteration", {}).get("_refObjectName") if isinstance(record.get("Iteration"), dict) else None,
            "release": record.get("Release", {}).get("_refObjectName") if isinstance(record.get("Release"), dict) else None,
        }
