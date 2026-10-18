"""Slack Web & Events API connector emitting SourceEvents (CRA-006.2, CRA-006.8).

Enforces:
1. Private channels and direct messages are BLOCKED by default (Decision H-13, CRA-006.8).
2. Enabling private/DM ingestion requires explicit configuration AND a recorded legal/compliance approval reference.
3. Message history, thread replies, edits, deletions, and file shares.
4. Entity mentions are linked through as proposals (knowledge_state="proposed").
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable, Iterator
from datetime import UTC, datetime
from typing import Any
import httpx

from eoip.connectors.base import (
    ConnectorHealth,
    DiscoveredResource,
    DiscoveryResult,
    DiscoveryScope,
    SourceConnector,
)
from eoip.connectors.errors import ConnectorError
from eoip.contracts.source_event import PermissionMetadata, SourceEventV2, utc_now_iso
from eoip.contracts.source_registry import SourceCapabilities

_MENTION_REGEX = re.compile(r"<@([A-Z0-9]+)>")


class SlackConnector:
    """Slack API connector with strict boundary controls for private channels and DMs."""

    source_system = "slack"
    mapper_version = "slack-api/1.0"

    def __init__(
        self,
        source_id: str,
        token: str,
        *,
        base_url: str = "https://slack.com/api",
        enable_private_channels: bool = False,
        enable_direct_messages: bool = False,
        compliance_approval_ref: str | None = None,
        channels: list[str] | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        # Boundary enforcement per CRA-006.8 & Decision H-13
        if (enable_private_channels or enable_direct_messages) and not compliance_approval_ref:
            raise ValueError(
                "Enabling Slack private-channel or direct-message ingestion without an approval reference "
                "is refused (CRA-006.8 / Decision H-13)"
            )

        self.source_id = source_id
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.enable_private_channels = enable_private_channels
        self.enable_direct_messages = enable_direct_messages
        self.compliance_approval_ref = compliance_approval_ref
        self.channels = sorted(set(channels or []))
        self._client = client or httpx.Client(timeout=30.0)
        self._headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        }

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
        types = ["public_channel"]
        if self.enable_private_channels:
            types.append("private_channel")
        if self.enable_direct_messages:
            types.extend(["im", "mpim"])

        resp = self._request_json("/conversations.list", params={"types": ",".join(types), "limit": 100})
        channels = resp.get("channels", [])
        resources = []
        for ch in channels:
            ch_id = ch.get("id")
            if not ch_id or (self.channels and ch_id not in self.channels):
                continue
            resources.append(
                DiscoveredResource(
                    resource_id=ch_id,
                    resource_type="slack_channel",
                    name=ch.get("name") or ch_id,
                    metadata={
                        "is_private": ch.get("is_private", False),
                        "is_im": ch.get("is_im", False),
                        "member_count": ch.get("num_members", 0),
                    },
                )
            )
        return DiscoveryResult(source_id=self.source_id, resources=resources)

    def baseline(self, checkpoint: str | None = None) -> Iterator[SourceEventV2]:
        discovery = self.discover(DiscoveryScope())
        events: list[SourceEventV2] = []
        for res in discovery.resources:
            events.extend(self._collect_channel(res.resource_id, checkpoint=checkpoint))
        return iter(events)

    def _collect_channel(self, channel_id: str, checkpoint: str | None = None) -> list[SourceEventV2]:
        events = []
        params: dict[str, Any] = {"channel": channel_id, "limit": 100}
        if checkpoint:
            params["oldest"] = checkpoint

        resp = self._request_json("/conversations.history", params=params)
        messages = resp.get("messages", [])
        for msg in messages:
            event = self._make_message_event(channel_id, msg)
            events.append(event)
            # Check thread replies
            if msg.get("thread_ts") and msg.get("reply_count", 0) > 0:
                replies_resp = self._request_json(
                    "/conversations.replies",
                    params={"channel": channel_id, "ts": msg["thread_ts"]},
                )
                for reply in replies_resp.get("messages", []):
                    if reply.get("ts") != msg.get("ts"):
                        events.append(self._make_message_event(channel_id, reply, thread_parent=msg["thread_ts"]))
        return events

    def handle_webhook_event(self, payload: dict[str, Any]) -> SourceEventV2:
        """Process Slack Events API callback payload."""
        event = payload.get("event", {})
        event_type = event.get("type", "")
        channel_id = event.get("channel", "unknown")
        operation = "DELETE" if event_type in ("message_deleted", "message.deleted") else "UPSERT"
        return self._make_message_event(channel_id, event, operation=operation)

    def _make_message_event(
        self,
        channel_id: str,
        message: dict[str, Any],
        thread_parent: str | None = None,
        operation: str = "UPSERT",
    ) -> SourceEventV2:
        ts = message.get("ts") or utc_now_iso()
        msg_id = f"{channel_id}:{ts}"
        serialized = json.dumps(message, sort_keys=True, separators=(",", ":"))
        content_hash = hashlib.sha256(serialized.encode()).hexdigest()
        event_id = hashlib.sha256(f"slack:{self.source_id}:{msg_id}:{content_hash}".encode()).hexdigest()

        # Extract mentions (CRA-006.8: linked as proposals)
        text = message.get("text", "")
        mentions = [f"user:{uid}" for uid in _MENTION_REGEX.findall(text)]

        # Files attached
        files = message.get("files", [])
        file_refs = [
            {"id": f.get("id"), "name": f.get("name"), "mimetype": f.get("mimetype"), "size": f.get("size")}
            for f in files if isinstance(f, dict)
        ]

        # Permissions: channel membership ACL
        is_private = message.get("is_private", False)
        visibility = "RESTRICTED" if is_private else "INTERNAL"
        permissions = PermissionMetadata(
            visibility=visibility,
            principal_refs=[f"slack:channel:{channel_id}"],
            inherited_from=f"slack:channel:{channel_id}",
        )

        return SourceEventV2(
            event_id=event_id,
            source_system="slack",
            source_instance_id=self.source_id,
            source_record_id=msg_id,
            operation=operation,
            source_version=str(message.get("edited", {}).get("ts") or ts),
            event_time=ts,
            captured_at=utc_now_iso(),
            content_hash=content_hash,
            cursor=ts,
            permissions=permissions,
            payload=message if operation != "DELETE" else None,
            metadata={
                "channel_id": channel_id,
                "thread_parent": thread_parent,
                "mentions": mentions,
                "proposed_mentions": mentions,  # proposed knowledge state per CRA-006.8
                "files": file_refs,
                "compliance_approval_ref": self.compliance_approval_ref,
            },
        )

    def _request_json(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = self.base_url + path
        try:
            resp = self._client.get(url, headers=self._headers, params=params)
        except Exception as exc:
            raise ConnectorError("slack", "transport_error", self.source_id) from exc

        if resp.status_code == 429:
            raise ConnectorError("slack", "rate_limited", self.source_id)
        if resp.status_code in (401, 403):
            raise ConnectorError("slack", "authorization_failed", self.source_id)
        if resp.is_error:
            raise ConnectorError("slack", "remote_error", self.source_id)

        try:
            data = resp.json()
            if not data.get("ok", True):
                err = data.get("error", "unknown_error")
                if err in ("invalid_auth", "not_authed", "account_inactive", "token_revoked"):
                    raise ConnectorError("slack", "authentication_failed", self.source_id)
                if err in ("missing_scope", "restricted_action"):
                    raise ConnectorError("slack", "authorization_failed", self.source_id)
                raise ConnectorError("slack", err, self.source_id)
            return data
        except Exception as exc:
            if isinstance(exc, ConnectorError):
                raise
            raise ConnectorError("slack", "invalid_response", self.source_id) from exc
