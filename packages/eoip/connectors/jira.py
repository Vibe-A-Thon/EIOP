"""Jira Cloud/Data Center REST connector emitting SourceEvent v2 records."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Iterator
from datetime import datetime
from time import monotonic
from typing import Any
from urllib.parse import quote, urlsplit

import httpx
from eoip.connectors.base import (
    ConnectorHealth,
    DiscoveredResource,
    DiscoveryResult,
    DiscoveryScope,
)
from eoip.connectors.errors import ConnectorError
from eoip.contracts.source_event import SourceEventV2, utc_now_iso
from eoip.contracts.source_registry import SourceCapabilities

DEFAULT_FIELDS = [
    "summary",
    "description",
    "issuetype",
    "status",
    "project",
    "assignee",
    "reporter",
    "parent",
    "labels",
    "issuelinks",
    "fixVersions",
    "created",
    "updated",
    "resolutiondate",
]


class JiraConnector:
    """Bounded, read-only connector for scoped Jira projects."""

    mapper_version = "jira-rest/1.0"

    def __init__(
        self,
        source_id: str,
        base_url: str,
        *,
        projects: list[str],
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        api_version: str = "3",
        search_mode: str = "enhanced",
        fields: list[str] | None = None,
        include_comments: bool = True,
        include_changelog: bool = True,
        include_sprints: bool = False,
        page_size: int = 100,
        max_pages: int = 1000,
        client: httpx.Client | None = None,
    ) -> None:
        parsed = urlsplit(base_url)
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
            raise ValueError("base_url must be an HTTPS URL without embedded credentials")
        if not projects:
            raise ValueError("at least one Jira project key is required")
        if bool(username) != bool(password) or (token and username) or not (token or username):
            raise ValueError("configure either bearer token or username/password authentication")
        if api_version not in {"2", "3"}:
            raise ValueError("api_version must be 2 or 3")
        if search_mode not in {"enhanced", "offset"}:
            raise ValueError("search_mode must be enhanced or offset")
        if search_mode == "enhanced" and api_version != "3":
            raise ValueError("enhanced search requires Jira REST API v3")
        if not 1 <= page_size <= 100 or not 1 <= max_pages <= 10_000:
            raise ValueError("invalid Jira pagination limits")
        self.source_id = source_id
        self.base_url = base_url.rstrip("/")
        self.projects = sorted(set(projects))
        self.api_version = api_version
        self.search_mode = search_mode
        self.fields = sorted(set(fields or DEFAULT_FIELDS))
        self.include_comments = include_comments
        self.include_changelog = include_changelog
        self.include_sprints = include_sprints
        self.page_size = page_size
        self.max_pages = max_pages
        self._headers = {"Accept": "application/json", "User-Agent": "EOIP-Jira-Connector/1.0"}
        auth = None
        if token:
            self._headers["Authorization"] = f"Bearer {token}"
        else:
            auth = httpx.BasicAuth(username or "", password or "")
        self._client = client or httpx.Client(
            timeout=30,
            follow_redirects=False,
            trust_env=False,
            auth=auth,
        )
        self._owns_client = client is None

    @property
    def api_root(self) -> str:
        return f"/rest/api/{self.api_version}"

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def capabilities(self) -> SourceCapabilities:
        return SourceCapabilities(
            polling=True,
            webhooks=True,
            deletion_events=True,
            discovery=True,
            reconciliation=True,
            replay=True,
        )

    def discover(self, scope: DiscoveryScope) -> DiscoveryResult:
        selected = set(scope.include or self.projects)
        resources = []
        for project_key in self.projects:
            if project_key not in selected or project_key in scope.exclude:
                continue
            project = self._project(project_key)
            resources.append(
                DiscoveredResource(
                    resource_id=str(project.get("key") or project_key),
                    resource_type="project",
                    name=str(project.get("name") or project_key),
                    metadata={
                        "id": str(project.get("id", "")),
                        "project_type": project.get("projectTypeKey"),
                        "simplified": project.get("simplified"),
                    },
                )
            )
        return DiscoveryResult(source_id=self.source_id, resources=resources)

    def baseline(self, checkpoint: str | None = None) -> Iterator[SourceEventV2]:
        return iter(self._collect(checkpoint))

    def poll_changes(self, checkpoint: str) -> Iterator[SourceEventV2]:
        if not checkpoint:
            raise ValueError("Jira polling requires a checkpoint")
        datetime.fromisoformat(checkpoint)
        return iter(self._collect(checkpoint))

    def handle_event(self, event: dict[str, Any]) -> Iterator[SourceEventV2]:
        issue = event.get("issue")
        webhook_event = str(event.get("webhookEvent") or event.get("issue_event_type_name") or "")
        if not isinstance(issue, dict):
            raise TypeError("Jira webhook payload requires an issue object")
        issue_key = str(issue.get("key") or issue.get("id") or "unknown")
        project_key = str((issue.get("fields") or {}).get("project", {}).get("key") or issue_key.split("-")[0])
        events = []
        changelog = event.get("changelog")
        if isinstance(changelog, dict):
            events.extend(self._changelog_events(project_key, issue_key, changelog))
        operation = "DELETE" if "deleted" in webhook_event.casefold() else "UPSERT"
        events.append(self._event(project_key, "issue", issue_key, issue, operation=operation))
        return iter(events)

    def fetch_record(self, ref: str) -> SourceEventV2:
        issue = self._request_json(f"{self.api_root}/issue/{quote(ref, safe='')}", params={"fields": "*all"})
        if not isinstance(issue, dict):
            raise ConnectorError("jira", "invalid_response", self.source_id)
        project_key = str((issue.get("fields") or {}).get("project", {}).get("key") or ref.split("-")[0])
        return self._event(project_key, "issue", str(issue.get("key") or ref), issue)

    def health(self) -> ConnectorHealth:
        started = monotonic()
        try:
            self._request_json(f"{self.api_root}/serverInfo")
            return ConnectorHealth(
                status="HEALTHY",
                checked_at=utc_now_iso(),
                latency_ms=(monotonic() - started) * 1000,
            )
        except ConnectorError as exc:
            return ConnectorHealth(status="UNAVAILABLE", checked_at=utc_now_iso(), detail=exc.category)

    def replay(self, events: Iterable[SourceEventV2]) -> Iterator[SourceEventV2]:
        return iter(events)

    def _collect(self, checkpoint: str | None) -> list[SourceEventV2]:
        events = []
        for project_key in self.projects:
            project = self._project(project_key)
            canonical_key = str(project.get("key") or project_key)
            events.append(self._event(canonical_key, "project", canonical_key, project))
            for version in self._paginate_offset(
                f"{self.api_root}/project/{quote(canonical_key, safe='')}/version",
                collection_keys=("values", "versions"),
                allow_list=True,
                allow_not_found=True,
            ):
                events.append(
                    self._event(canonical_key, "version", str(version.get("id")), version, cursor=checkpoint)
                )
            statuses = self._request_json(
                f"{self.api_root}/project/{quote(canonical_key, safe='')}/statuses",
                allow_not_found=True,
            )
            if isinstance(statuses, list):
                for issue_type in statuses:
                    if not isinstance(issue_type, dict) or issue_type.get("id") is None:
                        continue
                    events.append(
                        self._event(
                            canonical_key,
                            "issue_type",
                            str(issue_type["id"]),
                            issue_type,
                            cursor=checkpoint,
                        )
                    )
                    for status in issue_type.get("statuses") or []:
                        if isinstance(status, dict) and status.get("id") is not None:
                            prepared = {**status, "issue_type_id": str(issue_type["id"])}
                            events.append(
                                self._event(
                                    canonical_key,
                                    "status",
                                    str(status["id"]),
                                    prepared,
                                    cursor=checkpoint,
                                )
                            )
            if self.include_sprints:
                events.extend(self._sprint_events(canonical_key, checkpoint))

        for issue in self._search_issues(checkpoint):
            issue_key = str(issue.get("key") or issue.get("id"))
            fields = issue.get("fields") if isinstance(issue.get("fields"), dict) else {}
            project_key = str((fields.get("project") or {}).get("key") or issue_key.split("-")[0])
            if self.include_changelog:
                histories = list(
                    self._paginate_offset(
                        f"{self.api_root}/issue/{quote(issue_key, safe='')}/changelog",
                        collection_keys=("values", "histories"),
                        allow_list=False,
                    )
                )
                histories.sort(key=lambda item: str(item.get("created", "")))
                for history in histories:
                    events.extend(
                        self._changelog_events(
                            project_key,
                            issue_key,
                            history,
                            cursor=checkpoint,
                        )
                    )
            if self.include_comments:
                for comment in self._paginate_offset(
                    f"{self.api_root}/issue/{quote(issue_key, safe='')}/comment",
                    collection_keys=("comments", "values"),
                    allow_list=False,
                ):
                    prepared = {**comment, "issue_key": issue_key}
                    events.append(
                        self._event(
                            project_key,
                            "comment",
                            f"{issue_key}:{comment.get('id')}",
                            prepared,
                            cursor=checkpoint,
                        )
                    )
            events.append(self._event(project_key, "issue", issue_key, issue, cursor=checkpoint))
        return events

    def _project(self, project_key: str) -> dict[str, Any]:
        project = self._request_json(f"{self.api_root}/project/{quote(project_key, safe='')}")
        if not isinstance(project, dict) or project.get("id") is None or not project.get("key"):
            raise ConnectorError("jira", "schema_drift", self.source_id)
        return project

    def _search_issues(self, checkpoint: str | None):
        quoted = ",".join(f'"{key}"' for key in self.projects)
        clauses = [f"project in ({quoted})"]
        if checkpoint:
            clauses.append(f'updated >= "{checkpoint}"')
        jql = " AND ".join(clauses) + " ORDER BY updated ASC, key ASC"
        if self.search_mode == "enhanced":
            token = None
            for _page in range(self.max_pages):
                body = {
                    "jql": jql,
                    "fields": self.fields,
                    "maxResults": self.page_size,
                }
                if token:
                    body["nextPageToken"] = token
                document = self._request_json(
                    f"{self.api_root}/search/jql",
                    method="POST",
                    body=body,
                )
                issues = document.get("issues") if isinstance(document, dict) else None
                if not isinstance(issues, list) or any(not isinstance(item, dict) for item in issues):
                    raise ConnectorError("jira", "invalid_response", self.source_id)
                yield from issues
                token = document.get("nextPageToken")
                if document.get("isLast") is True or not token:
                    return
            raise ConnectorError("jira", "pagination_limit", self.source_id)
        start_at = 0
        for _page in range(self.max_pages):
            document = self._request_json(
                f"{self.api_root}/search",
                method="POST",
                body={
                    "jql": jql,
                    "fields": self.fields,
                    "maxResults": self.page_size,
                    "startAt": start_at,
                },
            )
            issues = document.get("issues") if isinstance(document, dict) else None
            if not isinstance(issues, list) or any(not isinstance(item, dict) for item in issues):
                raise ConnectorError("jira", "invalid_response", self.source_id)
            yield from issues
            start_at += len(issues)
            if not issues or start_at >= int(document.get("total", start_at)):
                return
        raise ConnectorError("jira", "pagination_limit", self.source_id)

    def _sprint_events(self, project_key: str, checkpoint: str | None) -> list[SourceEventV2]:
        events = []
        for board in self._paginate_offset(
            "/rest/agile/1.0/board",
            collection_keys=("values",),
            params={"projectKeyOrId": project_key, "type": "scrum"},
            allow_list=False,
            allow_not_found=True,
        ):
            board_id = board.get("id")
            if board_id is None:
                continue
            for sprint in self._paginate_offset(
                f"/rest/agile/1.0/board/{quote(str(board_id), safe='')}/sprint",
                collection_keys=("values",),
                params={"state": "active,closed,future"},
                allow_list=False,
                allow_not_found=True,
            ):
                prepared = {**sprint, "board_id": board_id, "project_key": project_key}
                events.append(
                    self._event(
                        project_key,
                        "sprint",
                        str(sprint.get("id")),
                        prepared,
                        cursor=checkpoint,
                    )
                )
        return events

    def _changelog_events(
        self,
        project_key: str,
        issue_key: str,
        history: dict[str, Any],
        *,
        cursor: str | None = None,
    ) -> list[SourceEventV2]:
        events = []
        history_id = str(history.get("id") or "webhook")
        for index, item in enumerate(history.get("items") or []):
            if not isinstance(item, dict):
                continue
            prepared = {
                **item,
                "issue_key": issue_key,
                "history_id": history_id,
                "item_index": index,
                "author": history.get("author"),
                "created": history.get("created") or utc_now_iso(),
            }
            events.append(
                self._event(
                    project_key,
                    "changelog",
                    f"{issue_key}:{history_id}:{index}",
                    prepared,
                    cursor=cursor,
                )
            )
        return events

    def _paginate_offset(
        self,
        path: str,
        *,
        collection_keys: tuple[str, ...],
        params: dict[str, Any] | None = None,
        allow_list: bool,
        allow_not_found: bool = False,
    ):
        start_at = 0
        for _page in range(self.max_pages):
            document = self._request_json(
                path,
                params={**(params or {}), "startAt": start_at, "maxResults": self.page_size},
                allow_not_found=allow_not_found,
            )
            if document is None:
                return
            if allow_list and isinstance(document, list):
                records = document
                total = len(records)
            elif isinstance(document, dict):
                records = next((document.get(key) for key in collection_keys if key in document), None)
                total = int(document.get("total", start_at + len(records or [])))
            else:
                records, total = None, 0
            if not isinstance(records, list) or any(not isinstance(item, dict) for item in records):
                raise ConnectorError("jira", "invalid_response", self.source_id)
            yield from records
            start_at += len(records)
            if allow_list or not records or start_at >= total or document.get("isLast") is True:
                return
        raise ConnectorError("jira", "pagination_limit", self.source_id)

    def _request_json(
        self,
        path: str,
        *,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        allow_not_found: bool = False,
    ) -> Any:
        url = self.base_url + path
        try:
            response = self._client.request(
                method,
                url,
                params=params,
                json=body,
                headers={**self._headers, **({"Content-Type": "application/json"} if body else {})},
            )
        except httpx.TimeoutException as exc:
            raise ConnectorError("jira", "timeout", self.source_id) from exc
        except httpx.RequestError as exc:
            raise ConnectorError("jira", "transport_error", self.source_id) from exc
        if allow_not_found and response.status_code == 404:
            return None
        categories = {
            401: "authentication_failed",
            403: "authorization_failed",
            404: "not_found",
            429: "rate_limited",
        }
        if response.is_error:
            raise ConnectorError("jira", categories.get(response.status_code, "remote_error"), self.source_id)
        try:
            return response.json()
        except ValueError as exc:
            raise ConnectorError("jira", "invalid_response", self.source_id) from exc

    def _event(
        self,
        project: str,
        kind: str,
        record_id: str,
        payload: dict[str, Any],
        *,
        operation: str = "UPSERT",
        cursor: str | None = None,
    ) -> SourceEventV2:
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        content_hash = hashlib.sha256(serialized.encode()).hexdigest()
        event_id = hashlib.sha256(
            f"jira:{self.source_id}:{project}:{kind}:{record_id}:{content_hash}:{operation}".encode()
        ).hexdigest()
        event_time = self._record_time(payload)
        return SourceEventV2(
            event_id=event_id,
            source_system="jira",
            source_instance_id=self.source_id,
            source_record_id=f"{project}:{kind}:{record_id}",
            operation=operation,
            source_version=str(payload.get("updated") or payload.get("id") or content_hash),
            event_time=event_time,
            captured_at=utc_now_iso(),
            content_hash=content_hash,
            cursor=cursor or event_time,
            payload=payload if operation != "DELETE" else None,
            metadata={
                "mapper_version": self.mapper_version,
                "record_kind": kind,
                "project": project,
                "record_id": record_id,
            },
        )

    @staticmethod
    def _record_time(record: dict[str, Any]) -> str:
        fields = record.get("fields") if isinstance(record.get("fields"), dict) else {}
        for source in (record, fields):
            for key in ("updated", "updated_at", "created", "created_at", "releaseDate", "startDate"):
                value = source.get(key)
                if isinstance(value, str) and value:
                    return value
        return utc_now_iso()
