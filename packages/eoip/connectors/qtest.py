"""qTest Manager REST connector emitting SourceEvents for test management artifacts."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from eoip.connectors.errors import ConnectorError
from eoip.connectors.rest import RestConnector, parse_utc, utc_timestamp
from eoip.connectors.sync import SyncBatch

QTEST_RESOURCE_TYPES = {
    "test_case": "test-cases",
    "test_run": "test-runs",
    "test_suite": "test-suites",
    "test_cycle": "test-cycles",
}


class QTestConnector(RestConnector):
    """Connector for qTest Manager via the REST API v3."""

    source_system = "qtest"
    mapper_version = "qtest-api/1.0"

    def __init__(
        self,
        base_url: str,
        *,
        project_id: int,
        resource_types: dict[str, str] | None = None,
        page_size: int = 100,
        **kwargs,
    ) -> None:
        if not isinstance(project_id, int) or project_id <= 0:
            raise ValueError("project_id must be a positive integer")
        if not 1 <= page_size <= 1000:
            raise ValueError("page_size must be between 1 and 1000")
        self.project_id = project_id
        self.resource_types = {**QTEST_RESOURCE_TYPES, **(resource_types or {})}
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
            raise ValueError("invalid qTest watermark")
        next_checkpoint = utc_timestamp(watermark_dt)

        events = []
        for record_kind, resource_path in self.resource_types.items():
            page = 1
            while True:
                response = self.get_json(
                    f"/api/v3/projects/{self.project_id}/{resource_path}",
                    params={
                        "page": page,
                        "pageSize": self.page_size,
                    },
                    correlation_id=correlation_id,
                )

                # qTest returns items directly or under a wrapper key
                records = response.get("items", response.get("results", []))
                if isinstance(response, list):
                    records = response
                if not isinstance(records, list):
                    self._log_failure("invalid_response", correlation_id)
                    raise ConnectorError(self.source_system, "invalid_response", correlation_id)

                if not records:
                    break

                for record in records:
                    if not isinstance(record, dict):
                        continue
                    record_id = record.get("id")
                    if record_id is None:
                        self._log_failure("schema_drift", correlation_id)
                        raise ConnectorError(self.source_system, "schema_drift", correlation_id)
                    version = record.get("last_modified_date") or record.get("created_date")
                    events.append(
                        self.make_event(
                            record_kind,
                            f"{self.instance_id}:{self.project_id}:{resource_path}:{record_id}",
                            record,
                            version,
                        )
                    )

                total = response.get("total", 0) if isinstance(response, dict) else len(records)
                if page * self.page_size >= total:
                    break
                page += 1

        return SyncBatch(events=events, next_checkpoint=next_checkpoint)

    def map_event(self, event, jira_resolver: Any | None = None) -> dict[str, Any]:
        record = event.payload or {}
        kind = (event.metadata or {}).get("record_kind") or "test_case"
        if kind not in self.resource_types and kind not in ("test_case", "test-cases", "test_run", "test-runs"):
            raise ValueError(f"unsupported qTest record kind: {kind}")
        record_id = record.get("id")
        if record_id is None:
            raise ValueError("qTest record requires id")

        # Distinguish test definition vs execution entity type (CRA-005.3, CRA-005.8)
        if kind in ("test_case", "test-cases"):
            entity_type = "TestCase"
        elif kind in ("test_run", "test-runs"):
            entity_type = "TestRun"
        elif kind in ("test_suite", "test-suites"):
            entity_type = "TestSuite"
        else:
            entity_type = "TestCycle"

        result: dict[str, Any] = {
            "kind": kind,
            "entity_type": entity_type,
            "test_case_id": str(record_id),
            "name": record.get("name"),
            "status": record.get("status") or _nested_status(record),
            "automation_status": record.get("automation") or record.get("automation_status"),
            "pid": record.get("pid"),
            "description": record.get("description"),
        }

        # Cross-system requirement & defect links (CRA-005.8)
        defect_links: list[str] = []
        links = record.get("links") or []
        for lnk in links:
            if isinstance(lnk, dict):
                rel = lnk.get("rel")
                target_id = str(lnk.get("id", ""))
                target_type = str(lnk.get("type", "")).lower()
                if rel == "defect":
                    defect_links.append(f"{target_type}:{target_id}")
                elif rel == "requirement" and target_type == "jira":
                    # Links to Jira issues ONLY when identifier resolves to an ingested Jira resource
                    if jira_resolver and (callable(jira_resolver) and jira_resolver(target_id) or hasattr(jira_resolver, "__contains__") and target_id in jira_resolver):
                        result["verifiesRequirement"] = f"urn:eoip:jira:issue:{target_id}"

        result["defect_links"] = defect_links
        return result


def _nested_status(record: dict) -> str | None:
    """Extract status from qTest's nested properties structure."""
    properties = record.get("properties")
    if isinstance(properties, list):
        for prop in properties:
            if isinstance(prop, dict) and prop.get("field_name") == "Status":
                return prop.get("field_value_name") or prop.get("field_value")
    return None
