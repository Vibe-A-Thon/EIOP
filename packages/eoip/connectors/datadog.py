"""Datadog API connector emitting SourceEvents for dashboards and monitors."""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlsplit

import httpx
from eoip.connectors.errors import ConnectorError
from eoip.connectors.rest import parse_utc, utc_timestamp
from eoip.connectors.sync import SyncBatch
from eoip.contracts.source_event import SourceEventV2, utc_now_iso

logger = logging.getLogger(__name__)


class DatadogConnector:
    """Standalone connector for Datadog using DD-API-KEY / DD-APPLICATION-KEY auth."""

    source_system = "datadog"
    mapper_version = "datadog-api/1.0"

    def __init__(
        self,
        base_url: str,
        *,
        api_key: str,
        app_key: str,
        page_size: int = 100,
        timeout: float = 30.0,
        client: httpx.Client | None = None,
    ) -> None:
        parsed = urlsplit(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("base_url must be an HTTP(S) URL")
        if not api_key or not app_key:
            raise ValueError("api_key and app_key are required")
        if not 1 <= page_size <= 1000:
            raise ValueError("page_size must be between 1 and 1000")

        self.base_url = base_url.rstrip("/")
        self.instance_id = hashlib.sha256(self.base_url.encode()).hexdigest()[:16]
        self.page_size = page_size
        self._headers = {
            "DD-API-KEY": api_key,
            "DD-APPLICATION-KEY": app_key,
            "Accept": "application/json",
        }
        self._client = client or httpx.Client(timeout=timeout, trust_env=False)
        self._owns_client = client is None

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def _get_json(
        self,
        path: str,
        *,
        params: dict[str, str | int] | None = None,
        correlation_id: str,
    ) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            response = self._client.get(url, params=params, headers=self._headers)
        except httpx.TimeoutException as exc:
            logger.warning("datadog request timeout", extra={"correlation_id": correlation_id})
            raise ConnectorError(self.source_system, "timeout", correlation_id) from exc
        except httpx.RequestError as exc:
            logger.warning("datadog transport error", extra={"correlation_id": correlation_id})
            raise ConnectorError(self.source_system, "transport_error", correlation_id) from exc

        if response.status_code in (401, 403):
            raise ConnectorError(self.source_system, "authentication_failed", correlation_id)
        if response.status_code == 429:
            raise ConnectorError(self.source_system, "rate_limited", correlation_id)
        if response.is_error:
            raise ConnectorError(self.source_system, "remote_error", correlation_id)

        try:
            return response.json()
        except (ValueError, json.JSONDecodeError) as exc:
            raise ConnectorError(self.source_system, "invalid_response", correlation_id) from exc

    def _make_event(
        self,
        record_kind: str,
        source_record_id: str,
        payload: dict,
        source_version: str | int | None,
    ) -> SourceEventV2:
        payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        payload_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
        event_id = hashlib.sha256(
            f"{self.source_system}:{record_kind}:{source_record_id}:{payload_hash}".encode()
        ).hexdigest()
        captured_at = utc_now_iso()
        return SourceEventV2(
            event_id=event_id,
            source_system=self.source_system,
            source_instance_id=self.instance_id,
            source_record_id=source_record_id,
            operation="UPSERT",
            source_version=str(source_version) if source_version is not None else payload_hash,
            event_time=captured_at,
            captured_at=captured_at,
            content_hash=payload_hash,
            payload=payload,
            metadata={
                "mapper_version": self.mapper_version,
                "record_kind": record_kind,
                "source_instance_id": self.instance_id,
            },
        )

    @staticmethod
    def _correlation_id(value: str | None) -> str:
        from uuid import uuid4
        return value or str(uuid4())

    def sync(
        self,
        *,
        checkpoint: str | None = None,
        watermark: str | None = None,
        correlation_id: str | None = None,
    ) -> SyncBatch:
        correlation_id = self._correlation_id(correlation_id)
        watermark_dt = parse_utc(watermark) if watermark else datetime.now(UTC)
        if watermark_dt is None:
            raise ValueError("invalid Datadog watermark")
        next_checkpoint = utc_timestamp(watermark_dt)

        events = []

        # Fetch dashboards (v1 list endpoint)
        dash_response = self._get_json(
            "/api/v1/dashboard",
            correlation_id=correlation_id,
        )
        dashboards = dash_response.get("dashboards", []) if isinstance(dash_response, dict) else []
        if not isinstance(dashboards, list):
            raise ConnectorError(self.source_system, "invalid_response", correlation_id)

        for dash in dashboards:
            if not isinstance(dash, dict):
                continue
            dash_id = dash.get("id")
            if dash_id is None:
                raise ConnectorError(self.source_system, "schema_drift", correlation_id)
            version = dash.get("modified_at") or dash.get("created_at")
            events.append(
                self._make_event(
                    "dashboard",
                    f"{self.instance_id}:dashboard:{dash_id}",
                    dash,
                    version,
                )
            )

        # Fetch monitors (v1 list endpoint, paginated)
        page = 0
        while True:
            monitor_response = self._get_json(
                "/api/v1/monitor",
                params={
                    "page": page,
                    "page_size": self.page_size,
                },
                correlation_id=correlation_id,
            )
            monitors = monitor_response if isinstance(monitor_response, list) else monitor_response.get("monitors", [])
            if not isinstance(monitors, list):
                raise ConnectorError(self.source_system, "invalid_response", correlation_id)

            if not monitors:
                break

            for monitor in monitors:
                if not isinstance(monitor, dict):
                    continue
                monitor_id = monitor.get("id")
                if monitor_id is None:
                    raise ConnectorError(self.source_system, "schema_drift", correlation_id)
                version = monitor.get("modified") or monitor.get("created")
                events.append(
                    self._make_event(
                        "monitor",
                        f"{self.instance_id}:monitor:{monitor_id}",
                        monitor,
                        version,
                    )
                )

            if len(monitors) < self.page_size:
                break
            page += 1

        return SyncBatch(events=events, next_checkpoint=next_checkpoint)

    def map_event(self, event) -> dict[str, Any]:
        record = event.payload
        kind = (event.metadata or {}).get("record_kind")
        if kind == "dashboard":
            dash_id = record.get("id")
            if dash_id is None:
                raise ValueError("Datadog dashboard requires id")
            return {
                "kind": kind,
                "dashboard_id": str(dash_id),
                "title": record.get("title"),
                "url": record.get("url"),
                "type": record.get("layout_type"),
            }
        if kind == "monitor":
            monitor_id = record.get("id")
            if monitor_id is None:
                raise ValueError("Datadog monitor requires id")
            return {
                "kind": kind,
                "monitor_id": str(monitor_id),
                "title": record.get("name"),
                "url": None,
                "type": record.get("type"),
            }
        raise ValueError("unsupported Datadog record kind")
