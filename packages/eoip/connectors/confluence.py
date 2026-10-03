"""On-prem Confluence Data Center connector emitting SourceEvents."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from typing import Any
from urllib.parse import quote

from eoip.connectors.confluence_metadata import (
    MAX_PAGE_VERSIONS,
    extract_page_history,
    extract_page_metadata,
)
from eoip.connectors.errors import ConnectorError
from eoip.connectors.rest import RestConnector, parse_utc, utc_timestamp
from eoip.connectors.sync import SyncBatch


class ConfluenceConnector(RestConnector):
    source_system = "confluence"
    mapper_version = "confluence-dc/1.2"

    def __init__(self, base_url: str, *, page_size: int = 100, **kwargs) -> None:
        if not 1 <= page_size <= 1000:
            raise ValueError("page_size must be between 1 and 1000")
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
            raise ValueError("invalid Confluence watermark")
        next_checkpoint = utc_timestamp(watermark_dt)
        checkpoint_dt = parse_utc(checkpoint)
        start_dt = checkpoint_dt - timedelta(minutes=2) if checkpoint_dt else None
        events = []

        for space in self._pages(
            "/rest/api/space",
            {"expand": "description.plain"},
            correlation_id,
            result_key="results",
        ):
            self._required_id(space, "key", "space", correlation_id)
            events.append(
                self.make_event(
                    "space",
                    f"{self.instance_id}:space:{space['key']}",
                    space,
                    space.get("version"),
                )
            )
            space_key = str(space["key"]).replace("\\", "\\\\").replace('"', '\\"')
            for record_kind in ("page", "attachment"):
                clauses = [f'space = "{space_key}"', f"type = {record_kind}"]
                if start_dt:
                    clauses.append(f'lastModified >= "{start_dt.strftime("%Y-%m-%d %H:%M")}"')
                clauses.append(f'lastModified <= "{watermark_dt.strftime("%Y-%m-%d %H:%M")}"')
                params: dict[str, str | int] = {
                    "cql": " AND ".join(clauses),
                    "expand": (
                        "space,version,body.storage,ancestors,metadata.labels,history"
                        if record_kind == "page"
                        else "space,version,container,extensions"
                    ),
                }
                for record in self._pages(
                    "/rest/api/content/search",
                    params,
                    correlation_id,
                    result_key="results",
                ):
                    self._required_id(record, "id", record_kind, correlation_id)
                    if record_kind == "page":
                        record = self._complete_labels(record, correlation_id)
                        record = self._complete_history(record, correlation_id)
                    version = record.get("version")
                    version_value = version.get("number") if isinstance(version, dict) else None
                    if version_value is None and isinstance(version, dict):
                        version_value = version.get("when")
                    events.append(
                        self.make_event(
                            record_kind,
                            f"{self.instance_id}:{record_kind}:{record['id']}",
                            record,
                            version_value,
                        )
                    )

        return SyncBatch(events=events, next_checkpoint=next_checkpoint)

    def map_event(self, event) -> dict[str, Any]:
        record = event.payload
        kind = (event.metadata or {}).get("record_kind")
        if kind == "space":
            self._required_value(record, "key", "space key")
            self._required_value(record, "name", "space name")
            description = record.get("description")
            if isinstance(description, dict):
                description = description.get("plain", {}).get("value")
            return {
                "kind": "space",
                "space_key": str(record["key"]),
                "name": record["name"],
                "description": description,
            }
        if kind == "page":
            space_key = self._nested(record, "space.key")
            self._required_value(record, "id", "page id")
            self._required_value(record, "title", "page title")
            self._required_value({"space_key": space_key}, "space_key", "page space key")
            version = record.get("version")
            body = self._nested(record, "body.storage.value")
            ancestors = record.get("ancestors", [])
            return {
                "kind": "page",
                "content_id": str(record["id"]),
                "title": record["title"],
                "space_key": str(space_key),
                "status": record.get("status"),
                "version": version.get("number") if isinstance(version, dict) else None,
                "updated_at": version.get("when") if isinstance(version, dict) else None,
                "body": body,
                "parent_ids": [str(item["id"]) for item in ancestors if isinstance(item, dict) and item.get("id")],
                "url": self._nested(record, "_links.webui"),
                "source_metadata": extract_page_metadata(record),
                "source_history": extract_page_history(record, self.base_url),
            }
        if kind == "attachment":
            space_key = self._nested(record, "space.key")
            container_id = self._nested(record, "container.id")
            self._required_value(record, "id", "attachment id")
            self._required_value(record, "title", "attachment filename")
            self._required_value({"space_key": space_key}, "space_key", "attachment space key")
            self._required_value({"container_id": container_id}, "container_id", "attachment page id")
            extensions = record.get("extensions") if isinstance(record.get("extensions"), dict) else {}
            return {
                "kind": "attachment",
                "content_id": str(record["id"]),
                "filename": record["title"],
                "page_id": str(container_id),
                "space_key": str(space_key),
                "media_type": extensions.get("mediaType"),
                "file_size": extensions.get("fileSize"),
                "version": self._nested(record, "version.number"),
            }
        raise ValueError("unsupported Confluence record kind")

    def _complete_history(self, record: dict, correlation_id: str) -> dict:
        version = record.get("version")
        number = version.get("number") if isinstance(version, dict) else None
        if isinstance(number, bool) or not isinstance(number, int) or not 1 <= number <= MAX_PAGE_VERSIONS:
            self._log_failure("invalid_response", correlation_id)
            raise ConnectorError(self.source_system, "invalid_response", correlation_id)
        versions = [version]
        path = f"/rest/api/content/{quote(str(record['id']), safe='')}"
        for previous in range(number - 1, 0, -1):
            historical = self.get_json(
                path, params={"status": "historical", "version": previous, "expand": "version"},
                correlation_id=correlation_id,
            )
            historical_version = historical.get("version")
            if (
                str(historical.get("id")) != str(record["id"])
                or not isinstance(historical_version, dict)
                or not isinstance(historical_version.get("number"), int)
                or isinstance(historical_version.get("number"), bool)
                or historical_version.get("number") != previous
            ):
                self._log_failure("invalid_response", correlation_id)
                raise ConnectorError(self.source_system, "invalid_response", correlation_id)
            versions.append(historical_version)
        return {**record, "version_history": {"complete": True, "results": versions}}

    def _complete_labels(self, record: dict, correlation_id: str) -> dict:
        continuation = self._nested(record, "metadata.labels._links.next")
        if not isinstance(continuation, str) or not continuation:
            return record
        # Never follow a response-provided URL with authenticated credentials.
        path = f"/rest/api/content/{quote(str(record['id']), safe='')}/label"
        labels: list[dict] = []
        seen_pages: set[str] = set()
        while True:
            response = self.get_json(
                path, params={"start": len(labels), "limit": self.page_size},
                correlation_id=correlation_id,
            )
            rows = response.get("results")
            links = response.get("_links", {})
            if (
                not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows)
                or not isinstance(links, dict)
                or (links.get("next") is not None and not isinstance(links["next"], str))
            ):
                self._log_failure("invalid_response", correlation_id)
                raise ConnectorError(self.source_system, "invalid_response", correlation_id)
            signature = json.dumps(rows, sort_keys=True)
            if (not rows and links.get("next")) or (rows and signature in seen_pages) or len(labels) + len(rows) > 10_000:
                self._log_failure("invalid_response", correlation_id)
                raise ConnectorError(self.source_system, "invalid_response", correlation_id)
            seen_pages.add(signature)
            labels.extend(rows)
            if not rows or (len(rows) < self.page_size and not links.get("next")):
                break
        metadata = {**record["metadata"], "labels": {"results": labels}}
        return {**record, "metadata": metadata}

    def _pages(self, path: str, params: dict, correlation_id: str, *, result_key: str):
        start = 0
        while True:
            response = self.get_json(
                path,
                params={**params, "start": start, "limit": self.page_size},
                correlation_id=correlation_id,
            )
            records = response.get(result_key)
            if not isinstance(records, list) or any(not isinstance(record, dict) for record in records):
                self._log_failure("invalid_response", correlation_id)
                raise ConnectorError(self.source_system, "invalid_response", correlation_id)
            if not records:
                return
            yield from records
            start += len(records)
            if len(records) < self.page_size:
                return

    def _required_id(self, record: dict, key: str, kind: str, correlation_id: str) -> None:
        if record.get(key) is None or not str(record[key]).strip():
            self._log_failure("schema_drift", correlation_id)
            raise ConnectorError(self.source_system, "schema_drift", correlation_id)

    @staticmethod
    def _required_value(record: dict, key: str, label: str) -> None:
        value = record.get(key)
        if value is None or not str(value).strip():
            raise ValueError(f"missing required {label}")

    @staticmethod
    def _nested(record: dict, path: str):
        value: Any = record
        for part in path.split("."):
            if not isinstance(value, dict):
                return None
            value = value.get(part)
        return value
