"""Grafana API connector emitting SourceEvents for dashboards and alert rules."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from eoip.connectors.errors import ConnectorError
from eoip.connectors.rest import RestConnector, parse_utc, utc_timestamp
from eoip.connectors.sync import SyncBatch


class GrafanaConnector(RestConnector):
    """Connector for Grafana via the HTTP API."""

    source_system = "grafana"
    mapper_version = "grafana-api/1.0"

    def __init__(
        self,
        base_url: str,
        *,
        page_size: int = 1000,
        fetch_alerts: bool = True,
        fetch_datasources: bool = True,
        **kwargs,
    ) -> None:
        if not 1 <= page_size <= 5000:
            raise ValueError("page_size must be between 1 and 5000")
        self.fetch_alerts = fetch_alerts
        self.fetch_datasources = fetch_datasources
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
            raise ValueError("invalid Grafana watermark")
        next_checkpoint = utc_timestamp(watermark_dt)

        events = []

        # Fetch dashboards via search API (paginated)
        page = 1
        while True:
            response = self.get_json(
                "/api/search",
                params={
                    "type": "dash-db",
                    "limit": self.page_size,
                    "page": page,
                },
                correlation_id=correlation_id,
            )
            # /api/search returns a list wrapped in a dict for get_json compatibility;
            # Grafana actually returns a JSON array, but RestConnector.get_json expects
            # a dict.  If the instance wraps it, handle both shapes.
            dashboards = response if isinstance(response, list) else response.get("results", [])
            if not isinstance(dashboards, list):
                self._log_failure("invalid_response", correlation_id)
                raise ConnectorError(self.source_system, "invalid_response", correlation_id)

            if not dashboards:
                break

            for dash in dashboards:
                if not isinstance(dash, dict):
                    continue
                uid = dash.get("uid")
                if uid is None:
                    self._log_failure("schema_drift", correlation_id)
                    raise ConnectorError(self.source_system, "schema_drift", correlation_id)
                version = dash.get("version") or dash.get("id")
                events.append(
                    self.make_event(
                        "dashboard",
                        f"{self.instance_id}:dashboard:{uid}",
                        dash,
                        version,
                    )
                )

            if len(dashboards) < self.page_size:
                break
            page += 1

        # Fetch alert rules
        if self.fetch_alerts:
            response = self.get_json(
                "/api/ruler/grafana/api/v1/rules",
                correlation_id=correlation_id,
            )
            if isinstance(response, dict):
                for namespace, groups in response.items():
                    if not isinstance(groups, list):
                        continue
                    for group in groups:
                        if not isinstance(group, dict):
                            continue
                        for rule in group.get("rules", []):
                            if not isinstance(rule, dict):
                                continue
                            grafana_alert = rule.get("grafana_alert", {})
                            if not isinstance(grafana_alert, dict):
                                grafana_alert = {}
                            rule_uid = grafana_alert.get("uid") or rule.get("uid")
                            if rule_uid is None:
                                continue
                            enriched = {**rule, "namespace": namespace}
                            version = grafana_alert.get("version") or grafana_alert.get("updated")
                            events.append(
                                self.make_event(
                                    "alert_rule",
                                    f"{self.instance_id}:alert:{rule_uid}",
                                    enriched,
                                    version,
                                )
                            )

        # Fetch data sources
        if self.fetch_datasources:
            response = self.get_json(
                "/api/datasources",
                correlation_id=correlation_id,
            )
            datasources = response if isinstance(response, list) else response.get("results", [])
            if isinstance(datasources, list):
                for ds in datasources:
                    if not isinstance(ds, dict):
                        continue
                    ds_id = ds.get("id") or ds.get("uid")
                    if ds_id is None:
                        continue
                    events.append(
                        self.make_event(
                            "datasource",
                            f"{self.instance_id}:datasource:{ds_id}",
                            ds,
                            ds.get("version"),
                        )
                    )

        return SyncBatch(events=events, next_checkpoint=next_checkpoint)

    def map_event(self, event) -> dict[str, Any]:
        record = event.payload
        kind = (event.metadata or {}).get("record_kind")
        if kind == "dashboard":
            uid = record.get("uid")
            if uid is None:
                raise ValueError("Grafana dashboard requires uid")
            return {
                "kind": kind,
                "dashboard_uid": str(uid),
                "title": record.get("title"),
                "url": record.get("url"),
                "panel_count": len(record.get("panels", [])) if isinstance(record.get("panels"), list) else None,
                "folder": record.get("folderTitle") or record.get("folderUid"),
            }
        if kind == "alert_rule":
            grafana_alert = record.get("grafana_alert", {}) if isinstance(record.get("grafana_alert"), dict) else {}
            rule_uid = grafana_alert.get("uid") or record.get("uid")
            if rule_uid is None:
                raise ValueError("Grafana alert rule requires uid")
            return {
                "kind": kind,
                "rule_uid": str(rule_uid),
                "title": grafana_alert.get("title") or record.get("alert"),
                "url": None,
                "panel_count": None,
                "folder": record.get("namespace"),
            }
        if kind == "datasource":
            ds_id = record.get("id") or record.get("uid")
            if ds_id is None:
                raise ValueError("Grafana datasource requires id")
            return {
                "kind": kind,
                "dashboard_uid": None,
                "title": record.get("name"),
                "url": record.get("url"),
                "panel_count": None,
                "folder": None,
            }
        raise ValueError("unsupported Grafana record kind")
