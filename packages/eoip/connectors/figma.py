"""Figma REST API connector emitting SourceEvents for files and components."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from eoip.connectors.errors import ConnectorError
from eoip.connectors.rest import RestConnector, parse_utc, utc_timestamp
from eoip.connectors.sync import SyncBatch


class FigmaConnector(RestConnector):
    """Connector for Figma via the REST API v1.

    Provide either ``team_id`` to discover projects and files automatically,
    or ``file_keys`` to sync a known set of files.
    """

    source_system = "figma"
    mapper_version = "figma-api/1.0"

    def __init__(
        self,
        base_url: str = "https://api.figma.com",
        *,
        team_id: str | None = None,
        file_keys: list[str] | None = None,
        **kwargs,
    ) -> None:
        if not team_id and not file_keys:
            raise ValueError("provide either team_id or file_keys")
        self.team_id = team_id
        self.file_keys = list(file_keys) if file_keys else []
        super().__init__(base_url, **kwargs)

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
            raise ValueError("invalid Figma watermark")
        next_checkpoint = utc_timestamp(watermark_dt)

        events = []

        # Discover file keys from team projects when team_id is provided
        file_keys = list(self.file_keys)
        if self.team_id:
            projects_response = self.get_json(
                f"/v1/teams/{self.team_id}/projects",
                correlation_id=correlation_id,
            )
            projects = projects_response.get("projects", [])
            if not isinstance(projects, list):
                self._log_failure("invalid_response", correlation_id)
                raise ConnectorError(self.source_system, "invalid_response", correlation_id)

            for project in projects:
                if not isinstance(project, dict):
                    continue
                project_id = project.get("id")
                if project_id is None:
                    continue

                files_response = self.get_json(
                    f"/v1/projects/{project_id}/files",
                    correlation_id=correlation_id,
                )
                files = files_response.get("files", [])
                if not isinstance(files, list):
                    continue

                for file_entry in files:
                    if not isinstance(file_entry, dict):
                        continue
                    key = file_entry.get("key")
                    if key and key not in file_keys:
                        file_keys.append(key)
                    # Emit file-level event from the listing
                    if key:
                        version = file_entry.get("last_modified")
                        events.append(
                            self.make_event(
                                "file",
                                f"{self.instance_id}:file:{key}",
                                file_entry,
                                version,
                            )
                        )

        # Fetch full file data and extract pages/components
        for file_key in file_keys:
            file_response = self.get_json(
                f"/v1/files/{file_key}",
                params={"depth": 1},
                correlation_id=correlation_id,
            )
            if not isinstance(file_response, dict):
                self._log_failure("invalid_response", correlation_id)
                raise ConnectorError(self.source_system, "invalid_response", correlation_id)

            # If this file was not already emitted via team discovery, emit it now
            if file_key not in [fk for fk in self.file_keys if self.team_id]:
                file_meta = {
                    "key": file_key,
                    "name": file_response.get("name"),
                    "lastModified": file_response.get("lastModified"),
                    "thumbnailUrl": file_response.get("thumbnailUrl"),
                    "version": file_response.get("version"),
                }
                already_emitted = any(
                    e.source_record_id == f"{self.instance_id}:file:{file_key}"
                    for e in events
                )
                if not already_emitted:
                    events.append(
                        self.make_event(
                            "file",
                            f"{self.instance_id}:file:{file_key}",
                            file_meta,
                            file_response.get("lastModified"),
                        )
                    )

            # Extract pages from the document
            document = file_response.get("document", {})
            if isinstance(document, dict):
                children = document.get("children", [])
                if isinstance(children, list):
                    for page in children:
                        if not isinstance(page, dict):
                            continue
                        page_id = page.get("id")
                        if page_id is None:
                            continue
                        page_data = {
                            "file_key": file_key,
                            "id": page_id,
                            "name": page.get("name"),
                            "type": page.get("type"),
                        }
                        events.append(
                            self.make_event(
                                "page",
                                f"{self.instance_id}:page:{file_key}:{page_id}",
                                page_data,
                                file_response.get("lastModified"),
                            )
                        )

            # Extract components
            components = file_response.get("components", {})
            if isinstance(components, dict):
                for comp_id, comp_data in components.items():
                    if not isinstance(comp_data, dict):
                        continue
                    enriched = {**comp_data, "file_key": file_key, "component_id": comp_id}
                    events.append(
                        self.make_event(
                            "component",
                            f"{self.instance_id}:component:{file_key}:{comp_id}",
                            enriched,
                            file_response.get("lastModified"),
                        )
                    )

        return SyncBatch(events=events, next_checkpoint=next_checkpoint)

    def map_event(self, event) -> dict[str, Any]:
        record = event.payload
        kind = (event.metadata or {}).get("record_kind")
        if kind == "file":
            file_key = record.get("key")
            if file_key is None:
                raise ValueError("Figma file requires key")
            return {
                "kind": kind,
                "file_key": str(file_key),
                "name": record.get("name"),
                "last_modified": record.get("last_modified") or record.get("lastModified"),
                "thumbnail_url": record.get("thumbnail_url") or record.get("thumbnailUrl"),
            }
        if kind == "page":
            file_key = record.get("file_key")
            if file_key is None:
                raise ValueError("Figma page requires file_key")
            return {
                "kind": kind,
                "file_key": str(file_key),
                "name": record.get("name"),
                "last_modified": None,
                "thumbnail_url": None,
            }
        if kind == "component":
            file_key = record.get("file_key")
            if file_key is None:
                raise ValueError("Figma component requires file_key")
            return {
                "kind": kind,
                "file_key": str(file_key),
                "name": record.get("name"),
                "last_modified": None,
                "thumbnail_url": None,
            }
        raise ValueError("unsupported Figma record kind")
