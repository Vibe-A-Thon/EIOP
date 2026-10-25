"""GitHub/GitHub Enterprise REST connector emitting SourceEvent v2 records."""

from __future__ import annotations

import base64
import binascii
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
from eoip.contracts.source_event import PermissionMetadata, SourceEventV2, utc_now_iso
from eoip.contracts.source_registry import SourceCapabilities
import hmac
import time


class GitHubConnector:
    mapper_version = "github-rest/1.0"

    def __init__(
        self,
        source_id: str,
        api_url: str,
        token: str,
        *,
        repositories: list[str] | None = None,
        organizations: list[str] | None = None,
        api_version: str = "2022-11-28",
        include_pages: bool = False,
        include_readme: bool = True,
        page_size: int = 100,
        max_pages: int = 1000,
        max_document_bytes: int = 2_000_000,
        client: httpx.Client | None = None,
    ) -> None:
        parsed = urlsplit(api_url)
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
            raise ValueError("api_url must be an HTTPS URL without embedded credentials")
        if not token:
            raise ValueError("GitHub token is required")
        if not repositories and not organizations:
            raise ValueError("at least one repository or organization scope is required")
        if not 1 <= page_size <= 100 or not 1 <= max_pages <= 10_000:
            raise ValueError("invalid GitHub pagination limits")
        if not 1024 <= max_document_bytes <= 10_000_000:
            raise ValueError("max_document_bytes must be between 1024 and 10000000")
        self.source_id = source_id
        self.api_url = api_url.rstrip("/")
        self.repositories = sorted(set(repositories or []))
        self.organizations = sorted(set(organizations or []))
        self.include_pages = include_pages
        self.include_readme = include_readme
        self.page_size = page_size
        self.max_pages = max_pages
        self.max_document_bytes = max_document_bytes
        self._headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": api_version,
            "User-Agent": "EOIP-GitHub-Connector/1.0",
        }
        self._client = client or httpx.Client(timeout=30, follow_redirects=False, trust_env=False)
        self._owns_client = client is None
        self._seen_deliveries: dict[str, float] = {}

    @staticmethod
    def verify_webhook_signature(payload_bytes: bytes, signature_header: str, secret: str) -> bool:
        """Verify GitHub HMAC-SHA256 signature (X-Hub-Signature-256) per CRA-007.2."""
        if not signature_header or not signature_header.startswith("sha256="):
            return False
        expected = "sha256=" + hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature_header)

    def check_replay_protection(
        self,
        delivery_id: str,
        timestamp_epoch: float | None = None,
        max_age_seconds: float = 300.0,
    ) -> bool:
        """Check delivery ID against cache and reject replays or expired requests (CRA-007.2)."""
        now = time.time()
        ts = timestamp_epoch if timestamp_epoch is not None else now
        if abs(now - ts) > max_age_seconds:
            return False
        if delivery_id in self._seen_deliveries:
            return False
        self._seen_deliveries[delivery_id] = ts
        cutoff = now - max_age_seconds
        self._seen_deliveries = {k: v for k, v in self._seen_deliveries.items() if v >= cutoff}
        return True

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
        selected = set(scope.include or self.repositories)
        repositories = self._repositories()
        resources = []
        for repository in repositories:
            full_name = str(repository.get("full_name", ""))
            if selected and full_name not in selected:
                continue
            if full_name in scope.exclude:
                continue
            resources.append(
                DiscoveredResource(
                    resource_id=full_name,
                    resource_type="repository",
                    name=str(repository.get("name") or full_name),
                    metadata={
                        "private": bool(repository.get("private")),
                        "archived": bool(repository.get("archived")),
                        "default_branch": repository.get("default_branch"),
                        "owner": (repository.get("owner") or {}).get("login"),
                    },
                )
            )
        return DiscoveryResult(source_id=self.source_id, resources=resources)

    def baseline(self, checkpoint: str | None = None) -> Iterator[SourceEventV2]:
        return iter(self._collect(checkpoint))

    def poll_changes(self, checkpoint: str) -> Iterator[SourceEventV2]:
        if not checkpoint:
            raise ValueError("GitHub polling requires a checkpoint")
        datetime.fromisoformat(checkpoint)
        return iter(self._collect(checkpoint))

    def handle_event(self, event: dict[str, Any]) -> Iterator[SourceEventV2]:
        event_name = str(event.get("_event_name") or "").lower()
        repository = event.get("repository") if isinstance(event.get("repository"), dict) else {}
        repo = repository.get("full_name")
        records: list[tuple[str, str, dict]] = []
        mapping = {
            "pull_request": ("pull_request", "pull_request"),
            "issues": ("issue", "issue"),
            "workflow_run": ("workflow_run", "workflow_run"),
            "release": ("release", "release"),
            "create": ("ref", "ref"),
            "delete": ("ref", "ref"),
        }
        if event_name == "push":
            records.extend(("commit", str(item.get("id")), item) for item in event.get("commits", []))
        elif event_name in mapping:
            kind, field = mapping[event_name]
            record = event.get(field) if isinstance(event.get(field), dict) else event
            records.append((kind, self._record_id(kind, record), record))
        elif event_name in {"repository", "ping"} and repository:
            records.append(("repository", str(repository.get("id")), repository))
        else:
            raise ValueError(f"unsupported GitHub webhook event: {event_name or 'missing'}")
        operation = "DELETE" if event_name == "delete" or event.get("action") == "deleted" else "UPSERT"
        return iter(
            self._event(repo or "unknown/unknown", kind, record_id, record, operation=operation)
            for kind, record_id, record in records
        )

    def fetch_record(self, ref: str) -> SourceEventV2:
        parts = ref.split(":", 2)
        if len(parts) != 3:
            raise ValueError("GitHub record reference must be repository:kind:id")
        repository, kind, record_id = parts
        paths = {
            "repository": f"/repos/{repository}",
            "pull_request": f"/repos/{repository}/pulls/{quote(record_id, safe='')}",
            "issue": f"/repos/{repository}/issues/{quote(record_id, safe='')}",
            "commit": f"/repos/{repository}/commits/{quote(record_id, safe='')}",
            "release": f"/repos/{repository}/releases/{quote(record_id, safe='')}",
            "workflow_run": f"/repos/{repository}/actions/runs/{quote(record_id, safe='')}",
        }
        if kind not in paths:
            raise ValueError(f"unsupported GitHub record kind: {kind}")
        record = self._request_json(paths[kind])
        if not isinstance(record, dict):
            raise ConnectorError("github", "invalid_response", self.source_id)
        return self._event(repository, kind, record_id, record)

    def health(self) -> ConnectorHealth:
        started = monotonic()
        try:
            self._request_json("/rate_limit")
            latency = (monotonic() - started) * 1000
            return ConnectorHealth(status="HEALTHY", checked_at=utc_now_iso(), latency_ms=latency)
        except ConnectorError as exc:
            return ConnectorHealth(status="UNAVAILABLE", checked_at=utc_now_iso(), detail=exc.category)

    def replay(self, events: Iterable[SourceEventV2]) -> Iterator[SourceEventV2]:
        return iter(events)

    def _collect(self, checkpoint: str | None) -> list[SourceEventV2]:
        events: list[SourceEventV2] = []
        for repository in self._repositories():
            repo = str(repository["full_name"])
            events.append(self._event(repo, "repository", str(repository["id"]), repository))
            endpoints: list[tuple[str, str, str | None]] = [
                ("branch", f"/repos/{repo}/branches", None),
                ("tag", f"/repos/{repo}/tags", None),
                ("commit", f"/repos/{repo}/commits", "since"),
                ("pull_request", f"/repos/{repo}/pulls", None),
                ("issue", f"/repos/{repo}/issues", "since"),
                ("release", f"/repos/{repo}/releases", None),
                ("workflow_run", f"/repos/{repo}/actions/runs", None),
            ]
            for kind, path, since_parameter in endpoints:
                params: dict[str, Any] = {"per_page": self.page_size}
                if kind in {"pull_request", "issue"}:
                    params["state"] = "all"
                if checkpoint and since_parameter:
                    params[since_parameter] = checkpoint
                key = "workflow_runs" if kind == "workflow_run" else None
                for record in self._paginate(path, params=params, collection_key=key):
                    if kind == "issue" and record.get("pull_request"):
                        continue
                    if checkpoint and not since_parameter and self._record_time(record) <= checkpoint:
                        continue
                    events.append(
                        self._event(repo, kind, self._record_id(kind, record), record, cursor=checkpoint)
                    )
            if self.include_pages and repository.get("has_pages"):
                pages = self._request_json(f"/repos/{repo}/pages", allow_not_found=True)
                if isinstance(pages, dict):
                    events.append(self._event(repo, "pages", repo, pages, cursor=checkpoint))
            if self.include_readme:
                readme = self._request_json(f"/repos/{repo}/readme", allow_not_found=True)
                if isinstance(readme, dict):
                    readme = self._prepare_readme(readme)
                    events.append(self._event(repo, "readme", str(readme.get("path", "README")), readme, cursor=checkpoint))
        return events

    def _repositories(self) -> list[dict[str, Any]]:
        found: dict[str, dict[str, Any]] = {}
        for repository in self.repositories:
            record = self._request_json(f"/repos/{repository}")
            if not isinstance(record, dict) or not record.get("full_name"):
                raise ConnectorError("github", "schema_drift", self.source_id)
            found[str(record["full_name"])] = record
        for organization in self.organizations:
            path = f"/orgs/{quote(organization, safe='')}/repos"
            for record in self._paginate(path, params={"type": "all", "per_page": self.page_size}):
                if not record.get("full_name"):
                    raise ConnectorError("github", "schema_drift", self.source_id)
                found[str(record["full_name"])] = record
        return [found[key] for key in sorted(found)]

    def _paginate(self, path: str, *, params: dict, collection_key: str | None = None):
        for page in range(1, self.max_pages + 1):
            document = self._request_json(path, params={**params, "page": page})
            records = document.get(collection_key) if collection_key and isinstance(document, dict) else document
            if not isinstance(records, list) or any(not isinstance(item, dict) for item in records):
                raise ConnectorError("github", "invalid_response", self.source_id)
            yield from records
            if len(records) < self.page_size:
                return
        raise ConnectorError("github", "pagination_limit", self.source_id)

    def _request_json(self, path: str, *, params: dict | None = None, allow_not_found: bool = False):
        try:
            response = self._client.get(self.api_url + path, params=params, headers=self._headers)
        except httpx.TimeoutException as exc:
            raise ConnectorError("github", "timeout", self.source_id) from exc
        except httpx.RequestError as exc:
            raise ConnectorError("github", "transport_error", self.source_id) from exc
        if allow_not_found and response.status_code == 404:
            return None
        categories = {
            401: "authentication_failed",
            403: "authorization_or_rate_limit",
            404: "not_found",
            429: "rate_limited",
        }
        if response.is_error:
            raise ConnectorError("github", categories.get(response.status_code, "remote_error"), self.source_id)
        try:
            return response.json()
        except ValueError as exc:
            raise ConnectorError("github", "invalid_response", self.source_id) from exc

    def _prepare_readme(self, record: dict[str, Any]) -> dict[str, Any]:
        prepared = dict(record)
        encoded = prepared.pop("content", None)
        if encoded is None:
            return prepared
        if prepared.get("encoding") != "base64" or not isinstance(encoded, str):
            raise ConnectorError("github", "unsupported_document_encoding", self.source_id)
        try:
            content = base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ConnectorError("github", "invalid_document_encoding", self.source_id) from exc
        if len(content) > self.max_document_bytes:
            raise ConnectorError("github", "document_too_large", self.source_id)
        prepared["text"] = content.decode("utf-8", errors="replace")
        return prepared

    def _event(
        self,
        repository: str,
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
            f"github:{self.source_id}:{repository}:{kind}:{record_id}:{content_hash}:{operation}".encode()
        ).hexdigest()
        event_time = self._record_time(payload)

        # Determine visibility and ACL vector (CRA-007.6)
        is_private = payload.get("private", True)
        if isinstance(payload.get("repository"), dict):
            is_private = payload["repository"].get("private", is_private)
        visibility_str = str(payload.get("visibility") or ("private" if is_private else "public")).lower()

        if visibility_str == "public":
            visibility = "PUBLIC"
            acl_vector = ["role:everyone"]
        elif visibility_str == "internal":
            visibility = "INTERNAL"
            acl_vector = [f"github:org:{repository.split('/')[0]}"]
        else:
            visibility = "RESTRICTED"
            acl_vector = [f"github:repo:{repository}"]

        permissions = PermissionMetadata(
            visibility=visibility,
            principal_refs=acl_vector,
            inherited_from=f"github:repo:{repository}",
        )

        metadata = {
            "mapper_version": self.mapper_version,
            "record_kind": kind,
            "repository": repository,
            "record_id": record_id,
            "ref_type": payload.get("ref_type"),
            "acl_vector": acl_vector,
            "visibility": visibility,
        }
        # Separate immutable commit references from moving-branch observations (CRA-007.1)
        if kind == "commit":
            metadata["immutable"] = True
            metadata["commit_sha"] = record_id
        elif kind == "branch":
            metadata["moving_ref"] = True
            metadata["branch_name"] = record_id
            metadata["target_commit"] = (payload.get("commit") or {}).get("sha")

        return SourceEventV2(
            event_id=event_id,
            source_system="github",
            source_instance_id=self.source_id,
            source_record_id=f"{repository}:{kind}:{record_id}",
            operation=operation,
            source_version=str(payload.get("node_id") or payload.get("sha") or content_hash),
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
            "commit": "sha",
            "pull_request": "number",
            "issue": "number",
            "release": "id",
            "workflow_run": "id",
            "ref": "ref",
        }
        value = record.get(keys.get(kind, "id"))
        if value is None:
            raise ConnectorError("github", "schema_drift", "record-identity")
        return str(value)

    @staticmethod
    def _record_time(record: dict[str, Any]) -> str:
        for key in ("updated_at", "published_at", "pushed_at", "created_at", "timestamp"):
            value = record.get(key)
            if isinstance(value, str) and value:
                return value
        commit = record.get("commit")
        if isinstance(commit, dict):
            author = commit.get("author")
            if isinstance(author, dict) and isinstance(author.get("date"), str):
                return author["date"]
        return utc_now_iso()
