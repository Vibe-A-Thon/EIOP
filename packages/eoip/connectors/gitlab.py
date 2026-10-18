"""GitLab.com and self-managed REST connector emitting SourceEvent v2 records."""

from __future__ import annotations

import base64
import binascii
import hashlib
import json
from collections.abc import Iterable, Iterator
from datetime import datetime
from time import monotonic
from typing import Any
from urllib.parse import quote, urljoin, urlsplit

import httpx
from eoip.connectors.base import (
    ConnectorHealth,
    DiscoveredResource,
    DiscoveryResult,
    DiscoveryScope,
)
from eoip.connectors.crawler import ControlledWebCrawler, CrawlScope
from eoip.connectors.errors import ConnectorError
from eoip.contracts.source_event import PermissionMetadata, SourceEventV2, utc_now_iso
from eoip.contracts.source_registry import SourceCapabilities


class GitLabConnector:
    """Read-only, bounded GitLab REST adapter for repositories and delivery metadata."""

    mapper_version = "gitlab-rest/1.0"

    def __init__(
        self,
        source_id: str,
        api_url: str,
        token: str,
        *,
        projects: list[str] | None = None,
        groups: list[str] | None = None,
        include_wikis: bool = True,
        include_pages: bool = True,
        include_readme: bool = True,
        include_merge_request_diffs: bool = True,
        pages_scopes: dict[str, dict[str, Any]] | None = None,
        page_size: int = 100,
        max_pages: int = 1000,
        max_document_bytes: int = 2_000_000,
        client: httpx.Client | None = None,
        pages_client: httpx.Client | None = None,
        pages_resolver=None,
    ) -> None:
        parsed = urlsplit(api_url)
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
            raise ValueError("api_url must be an HTTPS URL without embedded credentials")
        if not parsed.path.rstrip("/").endswith("/api/v4"):
            raise ValueError("api_url must end with /api/v4")
        if not token:
            raise ValueError("GitLab token is required")
        if not projects and not groups:
            raise ValueError("at least one project or group scope is required")
        if not 1 <= page_size <= 100 or not 1 <= max_pages <= 10_000:
            raise ValueError("invalid GitLab pagination limits")
        if not 1024 <= max_document_bytes <= 10_000_000:
            raise ValueError("max_document_bytes must be between 1024 and 10000000")
        self.source_id = source_id
        self.api_url = api_url.rstrip("/")
        self.projects = sorted(set(projects or []))
        self.groups = sorted(set(groups or []))
        self.include_wikis = include_wikis
        self.include_pages = include_pages
        self.include_readme = include_readme
        self.include_merge_request_diffs = include_merge_request_diffs
        self.pages_scopes = {
            project: CrawlScope.model_validate(scope)
            for project, scope in (pages_scopes or {}).items()
        }
        self.page_size = page_size
        self.max_pages = max_pages
        self.max_document_bytes = max_document_bytes
        self._headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "EOIP-GitLab-Connector/1.0",
        }
        self._client = client or httpx.Client(timeout=30, follow_redirects=False, trust_env=False)
        self._owns_client = client is None
        self._pages_client = pages_client
        self._pages_resolver = pages_resolver

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
        _groups, projects = self._scoped_projects()
        resources = []
        for project in projects:
            path = str(project.get("path_with_namespace", ""))
            if selected and path not in selected:
                continue
            if path in scope.exclude:
                continue
            resources.append(
                DiscoveredResource(
                    resource_id=path,
                    resource_type="project",
                    name=str(project.get("name") or path),
                    metadata={
                        "visibility": project.get("visibility"),
                        "archived": bool(project.get("archived")),
                        "default_branch": project.get("default_branch"),
                        "namespace": (project.get("namespace") or {}).get("full_path"),
                    },
                )
            )
        return DiscoveryResult(source_id=self.source_id, resources=resources)

    def baseline(self, checkpoint: str | None = None) -> Iterator[SourceEventV2]:
        return iter(self._collect(checkpoint))

    def poll_changes(self, checkpoint: str) -> Iterator[SourceEventV2]:
        if not checkpoint:
            raise ValueError("GitLab polling requires a checkpoint")
        datetime.fromisoformat(checkpoint)
        return iter(self._collect(checkpoint))

    def handle_event(self, event: dict[str, Any]) -> Iterator[SourceEventV2]:
        event_name = str(event.get("_event_name") or event.get("object_kind") or "").lower()
        project = event.get("project") if isinstance(event.get("project"), dict) else {}
        project_path = str(
            project.get("path_with_namespace")
            or project.get("path_with_namespace_slug")
            or event.get("project_id")
            or "unknown/project"
        )
        kind = str(event.get("object_kind") or "").lower()
        records: list[tuple[str, str, dict[str, Any], str]] = []
        if kind == "push" or "push hook" in event_name:
            for commit in event.get("commits", []):
                if isinstance(commit, dict):
                    records.append(("commit", self._record_id("commit", commit), commit, "UPSERT"))
        elif kind == "tag_push" or "tag push" in event_name:
            ref = str(event.get("ref", "")).removeprefix("refs/tags/")
            operation = "DELETE" if self._zero_sha(event.get("after")) else "UPSERT"
            records.append(("tag", ref, {"name": ref, "commit": {"id": event.get("after")}}, operation))
        else:
            aliases = {
                "merge_request": "merge_request",
                "issue": "issue",
                "pipeline": "pipeline",
                "build": "job",
                "job": "job",
                "deployment": "deployment",
                "release": "release",
                "wiki_page": "wiki",
            }
            record_kind = aliases.get(kind)
            record = event.get("object_attributes")
            if record_kind == "release" and not isinstance(record, dict):
                record = event.get("release")
            if record_kind == "wiki" and not isinstance(record, dict):
                record = event.get("wiki")
            if record_kind is None or not isinstance(record, dict):
                raise ValueError(f"unsupported GitLab webhook event: {kind or event_name or 'missing'}")
            record = dict(record)
            if record_kind == "pipeline" and isinstance(event.get("commit"), dict):
                record.setdefault("sha", event["commit"].get("id"))
            operation = "DELETE" if record.get("action") in {"delete", "destroy"} else "UPSERT"
            records.append((record_kind, self._record_id(record_kind, record), record, operation))
        return iter(
            self._event(project_path, record_kind, record_id, record, operation=operation)
            for record_kind, record_id, record, operation in records
        )

    def fetch_record(self, ref: str) -> SourceEventV2:
        parts = ref.split(":", 2)
        if len(parts) != 3:
            raise ValueError("GitLab record reference must be project:kind:id")
        project, kind, record_id = parts
        project_ref = quote(project, safe="")
        paths = {
            "project": f"/projects/{project_ref}",
            "commit": f"/projects/{project_ref}/repository/commits/{quote(record_id, safe='')}",
            "merge_request": f"/projects/{project_ref}/merge_requests/{quote(record_id, safe='')}",
            "issue": f"/projects/{project_ref}/issues/{quote(record_id, safe='')}",
            "pipeline": f"/projects/{project_ref}/pipelines/{quote(record_id, safe='')}",
            "job": f"/projects/{project_ref}/jobs/{quote(record_id, safe='')}",
            "deployment": f"/projects/{project_ref}/deployments/{quote(record_id, safe='')}",
            "release": f"/projects/{project_ref}/releases/{quote(record_id, safe='')}",
            "wiki": f"/projects/{project_ref}/wikis/{quote(record_id, safe='')}",
        }
        if kind not in paths:
            raise ValueError(f"unsupported GitLab record kind: {kind}")
        record = self._request_json(paths[kind])
        if not isinstance(record, dict):
            raise ConnectorError("gitlab", "invalid_response", self.source_id)
        return self._event(project, kind, record_id, record)

    def health(self) -> ConnectorHealth:
        started = monotonic()
        try:
            self._request_json("/version")
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
        events: list[SourceEventV2] = []
        groups, projects = self._scoped_projects()
        for group in groups:
            full_path = str(group.get("full_path") or group.get("path") or group.get("id"))
            events.append(self._event(full_path, "group", str(group.get("id", full_path)), group))
        for project in projects:
            project_path = str(project["path_with_namespace"])
            project_ref = quote(str(project.get("id") or project_path), safe="")
            events.append(self._event(project_path, "project", str(project["id"]), project))
            endpoints: list[tuple[str, str, dict[str, Any], str | None]] = [
                ("branch", f"/projects/{project_ref}/repository/branches", {}, None),
                ("tag", f"/projects/{project_ref}/repository/tags", {}, None),
                ("commit", f"/projects/{project_ref}/repository/commits", {}, "since"),
                ("merge_request", f"/projects/{project_ref}/merge_requests", {"state": "all"}, "updated_after"),
                ("issue", f"/projects/{project_ref}/issues", {"state": "all"}, "updated_after"),
                ("pipeline", f"/projects/{project_ref}/pipelines", {}, "updated_after"),
                ("job", f"/projects/{project_ref}/jobs", {}, None),
                ("deployment", f"/projects/{project_ref}/deployments", {}, "updated_after"),
                ("release", f"/projects/{project_ref}/releases", {}, None),
            ]
            for kind, path, params, incremental_parameter in endpoints:
                if checkpoint and incremental_parameter:
                    params[incremental_parameter] = checkpoint
                for record in self._paginate(path, params=params):
                    if checkpoint and not incremental_parameter and self._record_time(record) <= checkpoint:
                        continue
                    record_id = self._record_id(kind, record)
                    events.append(self._event(project_path, kind, record_id, record, cursor=checkpoint))
                    if kind == "merge_request" and self.include_merge_request_diffs:
                        iid = quote(record_id, safe="")
                        diff_path = f"/projects/{project_ref}/merge_requests/{iid}/diffs"
                        head_sha = (record.get("diff_refs") or {}).get("head_sha") or record.get("sha")
                        for index, diff in enumerate(self._paginate(diff_path, params={}), start=1):
                            prepared = {
                                **diff,
                                "merge_request_iid": record_id,
                                "commit_sha": head_sha,
                            }
                            diff_id = str(diff.get("new_path") or diff.get("old_path") or index)
                            events.append(
                                self._event(
                                    project_path,
                                    "file_change",
                                    f"{record_id}:{diff_id}",
                                    prepared,
                                    cursor=checkpoint,
                                )
                            )
                    if kind == "job":
                        for index, artifact in enumerate(record.get("artifacts") or [], start=1):
                            if not isinstance(artifact, dict):
                                continue
                            prepared = {**artifact, "job_id": record_id, "pipeline": record.get("pipeline")}
                            artifact_id = str(artifact.get("filename") or artifact.get("file_type") or index)
                            events.append(
                                self._event(
                                    project_path,
                                    "artifact",
                                    f"{record_id}:{artifact_id}",
                                    prepared,
                                    cursor=checkpoint,
                                )
                            )
            if self.include_wikis and project.get("wiki_enabled", True):
                for wiki in self._paginate(
                    f"/projects/{project_ref}/wikis", params={"with_content": True}, allow_not_found=True
                ):
                    if checkpoint and self._record_time(wiki) <= checkpoint:
                        continue
                    events.append(
                        self._event(project_path, "wiki", self._record_id("wiki", wiki), wiki, cursor=checkpoint)
                    )
            if self.include_pages and project.get("pages_access_level") != "disabled":
                pages = self._request_json(f"/projects/{project_ref}/pages", allow_not_found=True)
                if isinstance(pages, dict):
                    events.append(self._event(project_path, "pages", project_path, pages, cursor=checkpoint))
                for domain in self._paginate(
                    f"/projects/{project_ref}/pages/domains", params={}, allow_not_found=True
                ):
                    events.append(
                        self._event(
                            project_path,
                            "pages_domain",
                            str(domain.get("domain") or domain.get("url")),
                            domain,
                            cursor=checkpoint,
                        )
                    )
            pages_scope = self.pages_scopes.get(project_path)
            if pages_scope is not None:
                crawler = ControlledWebCrawler(
                    f"{self.source_id}:gitlab-pages:{project_path}",
                    pages_scope,
                    client=self._pages_client,
                    resolver=self._pages_resolver,
                )
                try:
                    for page in crawler.crawl():
                        events.append(
                            self._event(
                                project_path,
                                "pages_content",
                                page.source_record_id,
                                page.payload or {},
                                cursor=checkpoint,
                            )
                        )
                finally:
                    crawler.close()
            if self.include_readme:
                readme = self._request_json(
                    f"/projects/{project_ref}/repository/files/{quote('README.md', safe='')}",
                    params={"ref": project.get("default_branch") or "HEAD"},
                    allow_not_found=True,
                )
                if isinstance(readme, dict):
                    events.append(
                        self._event(
                            project_path,
                            "readme",
                            str(readme.get("file_path", "README.md")),
                            self._prepare_document(readme),
                            cursor=checkpoint,
                        )
                    )
        return events

    def _scoped_projects(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        found_groups: dict[str, dict[str, Any]] = {}
        found_projects: dict[str, dict[str, Any]] = {}
        for project in self.projects:
            record = self._request_json(f"/projects/{quote(project, safe='')}")
            self._validate_project(record)
            found_projects[str(record["path_with_namespace"])] = record
        for group in self.groups:
            group_ref = quote(group, safe="")
            group_record = self._request_json(f"/groups/{group_ref}")
            if not isinstance(group_record, dict):
                raise ConnectorError("gitlab", "schema_drift", self.source_id)
            full_path = str(group_record.get("full_path") or group_record.get("path") or group)
            found_groups[full_path] = group_record
            for record in self._paginate(
                f"/groups/{group_ref}/projects",
                params={"include_subgroups": True, "with_shared": False},
            ):
                self._validate_project(record)
                found_projects[str(record["path_with_namespace"])] = record
        return (
            [found_groups[key] for key in sorted(found_groups)],
            [found_projects[key] for key in sorted(found_projects)],
        )

    def _validate_project(self, record: Any) -> None:
        if not isinstance(record, dict) or record.get("id") is None or not record.get("path_with_namespace"):
            raise ConnectorError("gitlab", "schema_drift", self.source_id)

    def _paginate(self, path: str, *, params: dict[str, Any], allow_not_found: bool = False):
        url = self.api_url + path
        next_params: dict[str, Any] | None = {**params, "per_page": self.page_size, "page": 1}
        for _page in range(self.max_pages):
            response = self._request(url, params=next_params, allow_not_found=allow_not_found)
            if response is None:
                return
            try:
                records = response.json()
            except ValueError as exc:
                raise ConnectorError("gitlab", "invalid_response", self.source_id) from exc
            if not isinstance(records, list) or any(not isinstance(item, dict) for item in records):
                raise ConnectorError("gitlab", "invalid_response", self.source_id)
            yield from records
            next_url = response.links.get("next", {}).get("url")
            next_page = response.headers.get("x-next-page")
            if next_url:
                parsed_next = urlsplit(next_url)
                parsed_api = urlsplit(self.api_url)
                api_path = parsed_api.path.rstrip("/") + "/"
                if (
                    parsed_next.scheme != "https"
                    or parsed_next.netloc != parsed_api.netloc
                    or not parsed_next.path.startswith(api_path)
                ):
                    raise ConnectorError("gitlab", "unsafe_pagination_url", self.source_id)
                url, next_params = next_url, None
            elif next_page:
                url = self.api_url + path
                next_params = {**params, "per_page": self.page_size, "page": next_page}
            elif len(records) == self.page_size:
                # GitLab.com may omit pagination headers. Continue conservatively.
                current = int((next_params or {}).get("page", 1))
                url = self.api_url + path
                next_params = {**params, "per_page": self.page_size, "page": current + 1}
            else:
                return
        raise ConnectorError("gitlab", "pagination_limit", self.source_id)

    def _request_json(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        allow_not_found: bool = False,
    ) -> Any:
        response = self._request(self.api_url + path, params=params, allow_not_found=allow_not_found)
        if response is None:
            return None
        try:
            return response.json()
        except ValueError as exc:
            raise ConnectorError("gitlab", "invalid_response", self.source_id) from exc

    def _request(
        self,
        url: str,
        *,
        params: dict[str, Any] | None,
        allow_not_found: bool,
    ) -> httpx.Response | None:
        if not url.startswith(self.api_url + "/"):
            url = urljoin(self.api_url + "/", url)
        parsed_url = urlsplit(url)
        parsed_api = urlsplit(self.api_url)
        if (
            parsed_url.scheme != "https"
            or parsed_url.netloc != parsed_api.netloc
            or not parsed_url.path.startswith(parsed_api.path.rstrip("/") + "/")
        ):
            raise ConnectorError("gitlab", "unsafe_request_url", self.source_id)
        try:
            response = self._client.get(url, params=params, headers=self._headers)
        except httpx.TimeoutException as exc:
            raise ConnectorError("gitlab", "timeout", self.source_id) from exc
        except httpx.RequestError as exc:
            raise ConnectorError("gitlab", "transport_error", self.source_id) from exc
        if allow_not_found and response.status_code == 404:
            return None
        categories = {
            401: "authentication_failed",
            403: "authorization_failed",
            404: "not_found",
            429: "rate_limited",
        }
        if response.is_error:
            raise ConnectorError("gitlab", categories.get(response.status_code, "remote_error"), self.source_id)
        return response

    def _prepare_document(self, record: dict[str, Any]) -> dict[str, Any]:
        prepared = dict(record)
        encoded = prepared.pop("content", None)
        if encoded is None:
            return prepared
        if prepared.get("encoding") != "base64" or not isinstance(encoded, str):
            raise ConnectorError("gitlab", "unsupported_document_encoding", self.source_id)
        try:
            content = base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ConnectorError("gitlab", "invalid_document_encoding", self.source_id) from exc
        if len(content) > self.max_document_bytes:
            raise ConnectorError("gitlab", "document_too_large", self.source_id)
        prepared["text"] = content.decode("utf-8", errors="replace")
        return prepared

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
            f"gitlab:{self.source_id}:{project}:{kind}:{record_id}:{content_hash}:{operation}".encode()
        ).hexdigest()
        event_time = self._record_time(payload)

        # Determine visibility and ACL vector (CRA-007.6)
        visibility_val = str(payload.get("visibility") or ("private" if payload.get("private", True) else "public")).lower()
        if visibility_val == "public":
            visibility = "PUBLIC"
            acl_vector = ["role:everyone"]
        elif visibility_val == "internal":
            visibility = "INTERNAL"
            acl_vector = [f"gitlab:group:{project.split('/')[0]}"]
        else:
            visibility = "RESTRICTED"
            acl_vector = [f"gitlab:project:{project}"]

        permissions = PermissionMetadata(
            visibility=visibility,
            principal_refs=acl_vector,
            inherited_from=f"gitlab:project:{project}",
        )

        metadata = {
            "mapper_version": self.mapper_version,
            "record_kind": kind,
            "project": project,
            "record_id": record_id,
            "acl_vector": acl_vector,
            "visibility": visibility,
        }
        if kind == "commit":
            metadata["immutable"] = True
            metadata["commit_sha"] = record_id
        elif kind == "branch":
            metadata["moving_ref"] = True
            metadata["branch_name"] = record_id
            metadata["target_commit"] = (payload.get("commit") or {}).get("id")

        return SourceEventV2(
            event_id=event_id,
            source_system="gitlab",
            source_instance_id=self.source_id,
            source_record_id=f"{project}:{kind}:{record_id}",
            operation=operation,
            source_version=str(
                payload.get("updated_at")
                or payload.get("sha")
                or payload.get("id")
                or payload.get("commit_sha")
                or content_hash
            ),
            event_time=event_time,
            captured_at=utc_now_iso(),
            content_hash=content_hash,
            cursor=cursor or event_time,
            permissions=permissions,
            payload=payload if operation != "DELETE" else None,
            metadata=metadata,
        )

    @staticmethod
    def _record_id(kind: str, record: dict[str, Any]) -> str:
        keys = {
            "branch": "name",
            "tag": "name",
            "commit": "id",
            "merge_request": "iid",
            "issue": "iid",
            "pipeline": "id",
            "job": "id",
            "deployment": "id",
            "release": "tag_name",
            "wiki": "slug",
        }
        value = record.get(keys.get(kind, "id"))
        if value is None:
            raise ConnectorError("gitlab", "schema_drift", "record-identity")
        return str(value)

    @staticmethod
    def _record_time(record: dict[str, Any]) -> str:
        for key in (
            "updated_at",
            "released_at",
            "finished_at",
            "committed_date",
            "authored_date",
            "created_at",
            "timestamp",
        ):
            value = record.get(key)
            if isinstance(value, str) and value:
                return value
        commit = record.get("commit")
        if isinstance(commit, dict):
            for key in ("committed_date", "created_at", "authored_date"):
                if isinstance(commit.get(key), str):
                    return commit[key]
        return utc_now_iso()

    @staticmethod
    def _zero_sha(value: Any) -> bool:
        return isinstance(value, str) and value and set(value) == {"0"}
