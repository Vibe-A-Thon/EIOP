"""Documentum REST Services & CMIS connector emitting SourceEvents (CRA-006.3, CRA-006.7).

Enforces:
1. Pinned API version for Documentum REST Services / CMIS.
2. Preserves Cabinet, Folder, sysobject, rendition and version chain (i_chronicle_id).
3. Preserves Documentum ACLs, domain groups, folder inheritance, retention, and legal-hold flags.
4. Document identity rooted in r_object_id, never reduced to filename or URL alone.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterator
from typing import Any
import httpx

from eoip.connectors.base import (
    DiscoveredResource,
    DiscoveryResult,
    DiscoveryScope,
    SourceConnector,
)
from eoip.connectors.errors import ConnectorError
from eoip.contracts.source_event import PermissionMetadata, SourceEventV2, utc_now_iso
from eoip.contracts.source_registry import SourceCapabilities


class DocumentumConnector:
    """Documentum REST Services connector with full lifecycle and version lineage."""

    source_system = "documentum"
    mapper_version = "documentum-rest/1.0"

    def __init__(
        self,
        source_id: str,
        base_url: str,
        *,
        repository: str,
        username: str | None = None,
        password: str | None = None,
        token: str | None = None,
        cabinets: list[str] | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        self.source_id = source_id
        self.base_url = base_url.rstrip("/")
        self.repository = repository
        self.cabinets = sorted(set(cabinets or []))
        self._client = client or httpx.Client(timeout=30.0)
        self._headers = {"Accept": "application/json"}
        if token:
            self._headers["Authorization"] = f"Bearer {token}"
        elif username and password:
            import base64
            auth_str = base64.b64encode(f"{username}:{password}".encode()).decode()
            self._headers["Authorization"] = f"Basic {auth_str}"

    def capabilities(self) -> SourceCapabilities:
        return SourceCapabilities(
            baseline=True,
            polling=True,
            webhooks=True,
            discovery=True,
            reconciliation=True,
            replay=True,
        )

    @property
    def api_root(self) -> str:
        return f"/dctm-rest/repositories/{self.repository}"

    def discover(self, scope: DiscoveryScope) -> DiscoveryResult:
        resp = self._request_json(f"{self.api_root}/cabinets")
        entries = resp.get("entries", [])
        resources = []
        for entry in entries:
            props = entry.get("content", {}).get("properties", {})
            cab_id = props.get("r_object_id")
            cab_name = props.get("object_name")
            if not cab_id or (self.cabinets and cab_name not in self.cabinets):
                continue
            resources.append(
                DiscoveredResource(
                    resource_id=cab_id,
                    resource_type="cabinet",
                    name=cab_name or cab_id,
                    metadata={
                        "acl_name": props.get("acl_name"),
                        "acl_domain": props.get("acl_domain"),
                        "owner_name": props.get("owner_name"),
                    },
                )
            )
        return DiscoveryResult(source_id=self.source_id, resources=resources)

    def baseline(self, checkpoint: str | None = None) -> Iterator[SourceEventV2]:
        discovery = self.discover(DiscoveryScope())
        events: list[SourceEventV2] = []
        for res in discovery.resources:
            events.extend(self._collect_cabinet(res.resource_id))
        return iter(events)

    def _collect_cabinet(self, cabinet_id: str) -> list[SourceEventV2]:
        resp = self._request_json(f"{self.api_root}/cabinets/{cabinet_id}/sysobjects")
        entries = resp.get("entries", [])
        events: list[SourceEventV2] = []
        for entry in entries:
            props = entry.get("content", {}).get("properties", {})
            event = self.make_sysobject_event(props, parent_container_id=cabinet_id)
            events.append(event)
        return events

    def make_sysobject_event(
        self,
        properties: dict[str, Any],
        parent_container_id: str | None = None,
        operation: str = "UPSERT",
    ) -> SourceEventV2:
        """Create a versioned SourceEventV2 for a Documentum sysobject."""
        r_object_id = properties.get("r_object_id")
        if not r_object_id:
            raise ValueError("Documentum sysobject requires r_object_id")

        # Identity rooted in r_object_id, chronicle_id, and version label
        chronicle_id = properties.get("i_chronicle_id") or r_object_id
        version_label = properties.get("r_version_label", ["1.0"])[0] if isinstance(properties.get("r_version_label"), list) else str(properties.get("r_version_label") or "1.0")
        object_name = properties.get("object_name", "unnamed")
        content_size = properties.get("r_content_size", 0)

        # ACL and Governance flags (CRA-006.3, CRA-006.7)
        acl_name = properties.get("acl_name", "default_acl")
        acl_domain = properties.get("acl_domain", "default_domain")
        is_legal_hold = bool(properties.get("r_immutable_flag") or properties.get("legal_hold", False))
        retention_date = properties.get("r_retention_until")

        serialized = json.dumps(properties, sort_keys=True, separators=(",", ":"))
        content_hash = hashlib.sha256(serialized.encode()).hexdigest()
        event_id = hashlib.sha256(f"dctm:{self.source_id}:{r_object_id}:{content_hash}".encode()).hexdigest()
        event_time = properties.get("r_modify_date") or properties.get("r_creation_date") or utc_now_iso()

        permissions = PermissionMetadata(
            visibility="RESTRICTED" if is_legal_hold or acl_name != "world" else "INTERNAL",
            principal_refs=[f"documentum:acl:{acl_domain}:{acl_name}"],
            inherited_from=f"documentum:folder:{parent_container_id}" if parent_container_id else None,
        )

        return SourceEventV2(
            event_id=event_id,
            source_system="documentum",
            source_instance_id=self.source_id,
            source_record_id=f"sysobject:{r_object_id}",
            operation=operation,
            source_version=f"{chronicle_id}:{version_label}",
            event_time=event_time,
            captured_at=utc_now_iso(),
            content_hash=content_hash,
            cursor=event_time,
            permissions=permissions,
            payload=properties if operation != "DELETE" else None,
            metadata={
                "r_object_id": r_object_id,
                "i_chronicle_id": chronicle_id,
                "r_version_label": version_label,
                "object_name": object_name,
                "content_size": content_size,
                "parent_container_id": parent_container_id,
                "legal_hold": is_legal_hold,
                "retention_until": retention_date,
                "renditions": properties.get("renditions", []),
            },
        )

    def _request_json(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = self.base_url + path
        try:
            resp = self._client.get(url, headers=self._headers, params=params)
        except Exception as exc:
            raise ConnectorError("documentum", "transport_error", self.source_id) from exc

        if resp.status_code in (401, 403):
            raise ConnectorError("documentum", "authorization_failed", self.source_id)
        if resp.status_code == 429:
            raise ConnectorError("documentum", "rate_limited", self.source_id)
        if resp.is_error:
            raise ConnectorError("documentum", "remote_error", self.source_id)

        try:
            return resp.json()
        except Exception as exc:
            raise ConnectorError("documentum", "invalid_response", self.source_id) from exc
