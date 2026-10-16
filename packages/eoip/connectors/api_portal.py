"""API Portal / Gateway connector emitting SourceEvents for API service definitions."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from eoip.connectors.errors import ConnectorError
from eoip.connectors.rest import RestConnector, parse_utc, utc_timestamp
from eoip.connectors.sync import SyncBatch


class APIPortalConnector(RestConnector):
    """Connector for a generic API portal or gateway exposing Swagger/OpenAPI service catalogs."""

    source_system = "api_portal"
    mapper_version = "api-portal/1.0"

    def __init__(
        self,
        portal_url: str,
        *,
        service_ids: list[str] | None = None,
        services_path: str = "/api/v1/services",
        endpoints_path: str = "/api/v1/services/{service_id}/endpoints",
        page_size: int = 100,
        **kwargs,
    ) -> None:
        if not 1 <= page_size <= 1000:
            raise ValueError("page_size must be between 1 and 1000")
        self.service_ids = list(service_ids) if service_ids else []
        self.services_path = services_path
        self.endpoints_path = endpoints_path
        super().__init__(portal_url, **kwargs)
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
            raise ValueError("invalid API portal watermark")
        next_checkpoint = utc_timestamp(watermark_dt)

        events = []

        # Fetch services (paginated)
        services = self._fetch_services(correlation_id)
        for service in services:
            if not isinstance(service, dict):
                continue
            service_id = service.get("id") or service.get("service_id")
            if service_id is None:
                self._log_failure("schema_drift", correlation_id)
                raise ConnectorError(self.source_system, "schema_drift", correlation_id)

            # If service_ids filter is set, skip services not in the list
            if self.service_ids and str(service_id) not in self.service_ids:
                continue

            version = service.get("updated_at") or service.get("version")
            events.append(
                self.make_event(
                    "service",
                    f"{self.instance_id}:service:{service_id}",
                    service,
                    version,
                )
            )

            # Fetch endpoints for each service
            endpoints = self._fetch_endpoints(str(service_id), correlation_id)
            for endpoint in endpoints:
                if not isinstance(endpoint, dict):
                    continue
                endpoint_id = endpoint.get("id") or endpoint.get("endpoint_id")
                if endpoint_id is None:
                    continue
                enriched = {**endpoint, "service_id": str(service_id)}
                ep_version = endpoint.get("updated_at") or endpoint.get("version")
                events.append(
                    self.make_event(
                        "endpoint",
                        f"{self.instance_id}:endpoint:{service_id}:{endpoint_id}",
                        enriched,
                        ep_version,
                    )
                )

        return SyncBatch(events=events, next_checkpoint=next_checkpoint)

    def _fetch_services(self, correlation_id: str) -> list[dict]:
        """Paginate through the services listing."""
        all_services: list[dict] = []
        page = 1
        while True:
            response = self.get_json(
                self.services_path,
                params={
                    "page": page,
                    "page_size": self.page_size,
                },
                correlation_id=correlation_id,
            )
            services = response.get("services", response.get("items", response.get("results", [])))
            if not isinstance(services, list):
                self._log_failure("invalid_response", correlation_id)
                raise ConnectorError(self.source_system, "invalid_response", correlation_id)

            if not services:
                break

            all_services.extend(services)
            total = response.get("total", 0)
            if page * self.page_size >= total:
                break
            page += 1
        return all_services

    def _fetch_endpoints(self, service_id: str, correlation_id: str) -> list[dict]:
        """Fetch endpoints for a specific service."""
        path = self.endpoints_path.format(service_id=service_id)
        response = self.get_json(
            path,
            correlation_id=correlation_id,
        )
        endpoints = response.get("endpoints", response.get("items", response.get("results", [])))
        if not isinstance(endpoints, list):
            return []
        return endpoints

    def map_event(self, event) -> dict[str, Any]:
        record = event.payload
        kind = (event.metadata or {}).get("record_kind")
        if kind == "service":
            service_id = record.get("id") or record.get("service_id")
            if service_id is None:
                raise ValueError("API portal service requires id")
            return {
                "kind": kind,
                "service_id": str(service_id),
                "api_name": record.get("name") or record.get("api_name"),
                "api_version": record.get("version") or record.get("api_version"),
                "swagger_url": record.get("swagger_url") or record.get("spec_url") or record.get("documentation_url"),
            }
        if kind == "endpoint":
            service_id = record.get("service_id")
            endpoint_id = record.get("id") or record.get("endpoint_id")
            if service_id is None or endpoint_id is None:
                raise ValueError("API portal endpoint requires service_id and id")
            return {
                "kind": kind,
                "service_id": str(service_id),
                "api_name": record.get("path") or record.get("name"),
                "api_version": record.get("version"),
                "swagger_url": record.get("swagger_url"),
            }
        raise ValueError("unsupported API portal record kind")
