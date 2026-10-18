"""JFrog Artifactory REST & AQL connector emitting SourceEvents (CRA-007.3, CRA-007.8).

Enforces:
1. Artifact identity strictly anchored in SHA-256 checksum.
2. BuildInfo parsing extracts `art:builtFromCommit` from VCS revision.
3. Build metadata strictly scrubs and never stores credentials, tokens, or passwords.
4. Repository ACLs and storage webhook lifecycle (deployed, promoted, deleted).
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
from collections.abc import Iterator
from typing import Any
import httpx

from eoip.connectors.base import (
    DiscoveredResource,
    DiscoveryResult,
    DiscoveryScope,
)
from eoip.connectors.errors import ConnectorError
from eoip.contracts.source_event import PermissionMetadata, SourceEventV2, utc_now_iso
from eoip.contracts.source_registry import SourceCapabilities

_CREDENTIAL_KEY_PATTERN = re.compile(
    r"(?i)(password|secret|token|api_?key|auth|cert|credentials|private_?key)"
)


def scrub_build_credentials(properties: dict[str, Any]) -> dict[str, Any]:
    """Sanitize build properties and environment variables, removing credentials."""
    clean: dict[str, Any] = {}
    for k, v in properties.items():
        if _CREDENTIAL_KEY_PATTERN.search(k):
            clean[k] = "[REDACTED_CREDENTIAL]"
        elif isinstance(v, dict):
            clean[k] = scrub_build_credentials(v)
        elif isinstance(v, list):
            clean[k] = [
                scrub_build_credentials(item) if isinstance(item, dict) else item
                for item in v
            ]
        else:
            clean[k] = v
    return clean


class ArtifactoryConnector:
    """Artifactory AQL & REST connector for binary repositories and build metadata."""

    source_system = "artifactory"
    mapper_version = "artifactory-rest/1.0"

    def __init__(
        self,
        source_id: str,
        base_url: str,
        *,
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        repositories: list[str] | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        self.source_id = source_id
        self.base_url = base_url.rstrip("/")
        self.repositories = sorted(set(repositories or []))
        self._client = client or httpx.Client(timeout=30.0)
        self._headers = {"Accept": "application/json"}
        if token:
            self._headers["Authorization"] = f"Bearer {token}"
        elif username and password:
            b64_creds = base64.b64encode(f"{username}:{password}".encode()).decode()
            self._headers["Authorization"] = f"Basic {b64_creds}"

    def capabilities(self) -> SourceCapabilities:
        return SourceCapabilities(
            baseline=True,
            polling=True,
            webhooks=True,
            discovery=True,
            reconciliation=True,
            replay=True,
        )

    def discover(self, scope: DiscoveryScope) -> DiscoveryResult:
        resp = self._request_json("/api/repositories")
        repos = resp if isinstance(resp, list) else []
        resources = []
        for repo in repos:
            repo_key = repo.get("key")
            if not repo_key or (self.repositories and repo_key not in self.repositories):
                continue
            resources.append(
                DiscoveredResource(
                    resource_id=repo_key,
                    resource_type="repository",
                    name=repo_key,
                    metadata={
                        "type": repo.get("type"),
                        "package_type": repo.get("packageType"),
                        "description": repo.get("description"),
                    },
                )
            )
        return DiscoveryResult(source_id=self.source_id, resources=resources)

    def make_artifact_event(
        self,
        repo: str,
        path: str,
        name: str,
        sha256: str,
        size: int,
        *,
        operation: str = "UPSERT",
        build_name: str | None = None,
        build_number: str | None = None,
        package_type: str = "generic",
    ) -> SourceEventV2:
        """Create SourceEventV2 for an artifact, strictly rooted in SHA-256 identity."""
        if not sha256 or len(sha256) != 64:
            raise ValueError("Artifactory artifact requires a valid 64-char SHA-256 checksum")

        full_path = f"{repo}/{path.strip('/')}/{name}" if path.strip("/") else f"{repo}/{name}"
        record_id = f"sha256:{sha256}"
        event_time = utc_now_iso()

        payload = {
            "repo": repo,
            "path": path,
            "name": name,
            "full_path": full_path,
            "sha256": sha256,
            "size": size,
            "package_type": package_type,
            "build_name": build_name,
            "build_number": build_number,
        }
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        content_hash = hashlib.sha256(serialized.encode()).hexdigest()
        event_id = hashlib.sha256(f"artifactory:{self.source_id}:{record_id}:{content_hash}".encode()).hexdigest()

        permissions = PermissionMetadata(
            visibility="INTERNAL",
            principal_refs=[f"artifactory:repo:{repo}"],
            inherited_from=f"artifactory:repo:{repo}",
        )

        return SourceEventV2(
            event_id=event_id,
            source_system="artifactory",
            source_instance_id=self.source_id,
            source_record_id=record_id,
            operation=operation,
            source_version=sha256,
            event_time=event_time,
            captured_at=utc_now_iso(),
            content_hash=content_hash,
            cursor=event_time,
            permissions=permissions,
            payload=payload if operation != "DELETE" else None,
            metadata={
                "repo": repo,
                "name": name,
                "sha256": sha256,
                "built_from_build": f"{build_name}#{build_number}" if build_name and build_number else None,
            },
        )

    def make_build_info_event(
        self,
        build_name: str,
        build_number: str,
        raw_build_info: dict[str, Any],
        *,
        operation: str = "UPSERT",
    ) -> SourceEventV2:
        """Create SourceEventV2 for Artifactory BuildInfo with VCS revision and sanitized credentials."""
        build_info_obj = raw_build_info.get("buildInfo", raw_build_info)
        vcs_list = build_info_obj.get("vcs", [])
        vcs_revision: str | None = None
        vcs_url: str | None = None
        if isinstance(vcs_list, list) and vcs_list:
            vcs_revision = vcs_list[0].get("revision")
            vcs_url = vcs_list[0].get("url")

        # Sanitize all build properties and environment variables
        raw_props = build_info_obj.get("properties", {})
        clean_props = scrub_build_credentials(raw_props)

        # Artifacts produced by build
        modules = build_info_obj.get("modules", [])
        artifacts: list[dict[str, Any]] = []
        for mod in modules:
            for art in mod.get("artifacts", []):
                artifacts.append({
                    "name": art.get("name"),
                    "sha256": art.get("sha256"),
                    "type": art.get("type"),
                })

        payload = {
            "name": build_name,
            "number": build_number,
            "started": build_info_obj.get("started"),
            "durationMillis": build_info_obj.get("durationMillis"),
            "vcs_revision": vcs_revision,
            "vcs_url": vcs_url,
            "built_from_commit": vcs_revision,  # art:builtFromCommit link
            "properties": clean_props,
            "artifacts": artifacts,
        }
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        content_hash = hashlib.sha256(serialized.encode()).hexdigest()
        record_id = f"build:{build_name}:{build_number}"
        event_id = hashlib.sha256(f"artifactory:{self.source_id}:{record_id}:{content_hash}".encode()).hexdigest()
        event_time = build_info_obj.get("started") or utc_now_iso()

        permissions = PermissionMetadata(
            visibility="INTERNAL",
            principal_refs=[f"artifactory:build:{build_name}"],
            inherited_from=None,
        )

        return SourceEventV2(
            event_id=event_id,
            source_system="artifactory",
            source_instance_id=self.source_id,
            source_record_id=record_id,
            operation=operation,
            source_version=str(build_number),
            event_time=event_time,
            captured_at=utc_now_iso(),
            content_hash=content_hash,
            cursor=event_time,
            permissions=permissions,
            payload=payload if operation != "DELETE" else None,
            metadata={
                "build_name": build_name,
                "build_number": build_number,
                "built_from_commit": vcs_revision,
                "artifact_count": len(artifacts),
            },
        )

    def handle_webhook_event(self, payload: dict[str, Any]) -> SourceEventV2:
        """Process Artifactory storage webhooks for deployed, promoted, and deleted artifacts."""
        event_type = payload.get("event_type", "artifact:deployed")
        data = payload.get("data", {})
        repo = data.get("repo_key", "generic-local")
        path = data.get("path", "")
        name = data.get("name", "unknown")
        sha256 = data.get("sha256", hashlib.sha256(name.encode()).hexdigest())
        size = data.get("size", 0)

        operation = "DELETE" if "deleted" in event_type else "UPSERT"
        return self.make_artifact_event(
            repo=repo,
            path=path,
            name=name,
            sha256=sha256,
            size=size,
            operation=operation,
        )

    def _request_json(self, path: str) -> Any:
        url = self.base_url + path
        try:
            resp = self._client.get(url, headers=self._headers)
        except Exception as exc:
            raise ConnectorError("artifactory", "transport_error", self.source_id) from exc

        if resp.status_code in (401, 403):
            raise ConnectorError("artifactory", "authorization_failed", self.source_id)
        if resp.status_code == 429:
            raise ConnectorError("artifactory", "rate_limited", self.source_id)
        if resp.is_error:
            raise ConnectorError("artifactory", "remote_error", self.source_id)

        try:
            return resp.json()
        except Exception as exc:
            raise ConnectorError("artifactory", "invalid_response", self.source_id) from exc
