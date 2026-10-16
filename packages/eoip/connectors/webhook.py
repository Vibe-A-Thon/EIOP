"""Authenticated, durable and deduplicated webhook receipt gateway."""

from __future__ import annotations

import hashlib
import hmac
import json
import re
from base64 import b64decode, b64encode
from pathlib import Path
from time import time

from eoip.contracts.source_event import utc_now_iso
from eoip.jobs import write_json
from pydantic import BaseModel, ConfigDict


class WebhookReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str
    delivery_id: str
    received_at: str
    content_hash: str
    payload_ref: str
    duplicate: bool = False


class WebhookGateway:
    def __init__(self, root: str | Path, *, max_body_bytes: int = 2_000_000) -> None:
        self.root = Path(root)
        self.max_body_bytes = max_body_bytes

    def receive(
        self,
        source_id: str,
        body: bytes,
        *,
        signature: str,
        secret: str,
        delivery_id: str | None = None,
        metadata: dict | None = None,
        verification: str = "sha256",
        timestamp: str | None = None,
        max_age_seconds: int = 300,
    ) -> WebhookReceipt:
        if len(body) > self.max_body_bytes:
            raise ValueError("webhook body exceeds configured limit")
        if verification == "standard_webhooks":
            self._verify_standard_webhook(
                body,
                signature=signature,
                secret=secret,
                delivery_id=delivery_id,
                timestamp=timestamp,
                max_age_seconds=max_age_seconds,
            )
        elif verification == "plain_token":
            if not signature or not hmac.compare_digest(secret, signature):
                raise PermissionError("invalid webhook signature")
        elif verification == "sha256":
            expected = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
            supplied = signature.removeprefix("sha256=").lower()
            if not re.fullmatch(r"[a-f0-9]{64}", supplied) or not hmac.compare_digest(
                expected, supplied
            ):
                raise PermissionError("invalid webhook signature")
        else:
            raise ValueError("unsupported webhook verification mode")
        payload = json.loads(body)
        if not isinstance(payload, dict):
            raise TypeError("webhook payload must be a JSON object")
        content_hash = hashlib.sha256(body).hexdigest()
        delivery = delivery_id or content_hash
        safe_delivery = hashlib.sha256(delivery.encode("utf-8")).hexdigest()
        path = self.root / "receipts" / source_id / f"{safe_delivery}.json"
        if path.exists():
            existing = json.loads(path.read_text(encoding="utf-8"))
            return WebhookReceipt.model_validate({**existing["receipt"], "duplicate": True})
        receipt = WebhookReceipt(
            source_id=source_id,
            delivery_id=delivery,
            received_at=utc_now_iso(),
            content_hash=content_hash,
            payload_ref=str(path),
        )
        write_json(path, {"receipt": receipt.model_dump(), "payload": payload, "metadata": metadata or {}})
        return receipt

    @staticmethod
    def _verify_standard_webhook(
        body: bytes,
        *,
        signature: str,
        secret: str,
        delivery_id: str | None,
        timestamp: str | None,
        max_age_seconds: int,
    ) -> None:
        if not delivery_id or not timestamp or not signature or not secret.startswith("whsec_"):
            raise PermissionError("invalid webhook signature")
        try:
            numeric_timestamp = int(timestamp)
            key = b64decode(secret.removeprefix("whsec_"), validate=True)
        except (ValueError, TypeError) as exc:
            raise PermissionError("invalid webhook signature") from exc
        if max_age_seconds < 1 or abs(int(time()) - numeric_timestamp) > max_age_seconds:
            raise PermissionError("stale webhook timestamp")
        message = delivery_id.encode() + b"." + timestamp.encode() + b"." + body
        expected = "v1," + b64encode(hmac.new(key, message, hashlib.sha256).digest()).decode()
        if not any(hmac.compare_digest(expected, candidate) for candidate in signature.split()):
            raise PermissionError("invalid webhook signature")
