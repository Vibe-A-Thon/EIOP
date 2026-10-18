"""Grafana API connector emitting SourceEvents for dashboards and alert rules."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from eoip.connectors.errors import ConnectorError
from eoip.connectors.rest import RestConnector, parse_utc, utc_timestamp
from eoip.connectors.sync import SyncBatch
from eoip.contracts.source_event import PermissionMetadata, SourceEventV2, utc_now_iso


class GrafanaConnector(RestConnector):
    """Connector for Grafana via the HTTP API."""

    source_system = "grafana"
    mapper_version = "grafana-api/1.0"

    def __init__(
        self,
        base_url: str,
        *,
        org_id: int | str = 1,
        page_size: int = 1000,
        fetch_alerts: bool = True,
        fetch_datasources: bool = True,
        **kwargs,
    ) -> None:
        if not 1 <= page_size <= 5000:
            raise ValueError("page_size must be between 1 and 5000")
        self.org_id = org_id
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

        events.extend(self._sync_datasources(correlation_id))
        return SyncBatch(events=events, next_checkpoint=next_checkpoint)

    @staticmethod
    def scrub_datasource_secrets(ds: dict[str, Any]) -> dict[str, Any]:
        """Never retrieve or expose stored data-source secrets as ordinary metadata (CRA-008.4)."""
        clean = dict(ds)
        clean.pop("secureJsonData", None)
        clean.pop("password", None)
        clean.pop("basicAuthPassword", None)
        if "jsonData" in clean and isinstance(clean["jsonData"], dict):
            clean_json = dict(clean["jsonData"])
            for k in list(clean_json.keys()):
                if any(sec in k.lower() for sec in ("secret", "token", "password", "key", "auth")):
                    clean_json[k] = "[REDACTED]"
            clean["jsonData"] = clean_json
        return clean

    def _sync_datasources(self, correlation_id: str) -> list[SourceEventV2]:
        events = []
        if not self.fetch_datasources:
            return events
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
                clean_ds = self.scrub_datasource_secrets(ds)
                events.append(
                    self.make_event(
                        "datasource",
                        f"{self.instance_id}:datasource:{ds_id}",
                        clean_ds,
                        clean_ds.get("version"),
                    )
                )
        return events

    def make_event(
        self,
        record_kind: str,
        source_record_id: str,
        payload: dict,
        source_version: str | int | None,
        *,
        operation: str = "UPSERT",
        permissions: PermissionMetadata | None = None,
    ) -> SourceEventV2:
        import hashlib
        import json
        payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        payload_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
        event_id = hashlib.sha256(
            f"{self.source_system}:{record_kind}:{source_record_id}:{payload_hash}:{operation}".encode()
        ).hexdigest()
        captured_at = utc_now_iso()

        org_ref = f"grafana:org:{self.org_id}"
        if permissions is None:
            principals = [org_ref]
            folder_uid = payload.get("folderUid") or payload.get("folder")
            if folder_uid:
                principals.append(f"grafana:folder:{folder_uid}")
            permissions = PermissionMetadata(
                visibility="INTERNAL",
                principal_refs=principals,
                inherited_from=org_ref,
            )

        return SourceEventV2(
            event_id=event_id,
            source_system=self.source_system,
            source_instance_id=self.instance_id,
            source_record_id=source_record_id,
            operation=operation,
            source_version=str(source_version) if source_version is not None else payload_hash,
            event_time=captured_at,
            captured_at=captured_at,
            content_hash=payload_hash,
            permissions=permissions,
            payload=payload if operation != "DELETE" else None,
            metadata={
                "mapper_version": self.mapper_version,
                "record_kind": record_kind,
                "org_id": str(self.org_id),
                "acl_vector": list(permissions.principal_refs),
            },
        )

    @staticmethod
    def extract_service_proposals(record: dict[str, Any]) -> list[dict[str, Any]]:
        """Extract proposals linking dashboard panels to CMDB services with evidence (CRA-008.7)."""
        import re
        import json
        text = json.dumps(record, default=str)
        proposals = []
        for pat in [r"\b(?:service|svc|cmdb_ci)[:=\s]+([a-zA-Z0-9_\-\.]+)\b", r"\b([a-zA-Z0-9_\-]+-service)\b"]:
            for m in re.finditer(pat, text, re.IGNORECASE):
                svc_name = m.group(1).lower()
                proposals.append({
                    "proposed_target": f"cmdb:service:{svc_name}",
                    "relationship": "tracksService",
                    "evidence_snippet": text[max(0, m.start() - 20) : min(len(text), m.end() + 20)],
                    "status": "PROPOSED",
                })
        return proposals

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
                "service_proposals": self.extract_service_proposals(record),
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
                "service_proposals": self.extract_service_proposals(record),
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
