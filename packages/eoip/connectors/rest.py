"""Safe HTTP plumbing for on-prem source-system connectors."""

from __future__ import annotations

import hashlib
import json
import logging
from collections.abc import Mapping
from datetime import UTC, datetime
from urllib.parse import urlsplit
from uuid import uuid4

import httpx
from eoip.connectors.errors import ConnectorError
from eoip.contracts.source_event import SourceEventV2, utc_now_iso

logger = logging.getLogger(__name__)


def parse_utc(value: str | None) -> datetime | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        raise ValueError("checkpoint must not be empty")
    if "T" not in normalized and " " not in normalized:
        normalized += "T00:00:00"
    normalized = normalized.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError("checkpoint must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def utc_timestamp(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class RestConnector:
    source_system = ""

    def __init__(
        self,
        base_url: str,
        *,
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        timeout: float = 30.0,
        client: httpx.Client | None = None,
    ) -> None:
        parsed = urlsplit(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.username or parsed.password:
            raise ValueError("base_url must be an HTTP(S) URL without embedded credentials")
        if bool(username) != bool(password):
            raise ValueError("username and password must be provided together")
        if token and username:
            raise ValueError("choose either a bearer token or a username/password pair")
        if not token and not username:
            raise ValueError("provide a bearer token or a username/password pair")
        self.base_url = base_url.rstrip("/")
        self.instance_id = hashlib.sha256(self.base_url.encode()).hexdigest()[:16]
        self._token = token
        self._basic_auth = httpx.BasicAuth(username, password) if username and password else None
        self._client = client or httpx.Client(timeout=timeout, trust_env=False)
        self._owns_client = client is None

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def get_json(
        self,
        path: str,
        *,
        params: Mapping[str, str | int] | None = None,
        correlation_id: str,
    ) -> dict:
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = {"Authorization": f"Bearer {self._token}"} if self._token else {}
        try:
            response = self._client.get(url, params=params, headers=headers, auth=self._basic_auth)
        except httpx.TimeoutException as exc:
            self._log_failure("timeout", correlation_id)
            raise ConnectorError(self.source_system, "timeout", correlation_id) from exc
        except httpx.RequestError as exc:
            self._log_failure("transport_error", correlation_id)
            raise ConnectorError(self.source_system, "transport_error", correlation_id) from exc

        if response.status_code in (401, 403):
            category = "authentication_failed"
        elif response.status_code == 429:
            category = "rate_limited"
        elif response.is_error:
            category = "remote_error"
        else:
            category = ""
        if category:
            logger.warning(
                "source connector request failed",
                extra={
                    "source_system": self.source_system,
                    "error_category": category,
                    "correlation_id": correlation_id,
                    "http_status": response.status_code,
                },
            )
            raise ConnectorError(self.source_system, category, correlation_id)

        try:
            payload = response.json()
        except (ValueError, json.JSONDecodeError) as exc:
            self._log_failure("invalid_response", correlation_id, response.status_code)
            raise ConnectorError(self.source_system, "invalid_response", correlation_id) from exc
        if not isinstance(payload, dict):
            self._log_failure("invalid_response", correlation_id, response.status_code)
            raise ConnectorError(self.source_system, "invalid_response", correlation_id)
        return payload

    def make_event(
        self,
        record_kind: str,
        source_record_id: str,
        payload: dict,
        source_version: str | int | None,
    ) -> SourceEventV2:
        payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        payload_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
        event_id = hashlib.sha256(
            f"{self.source_system}:{record_kind}:{source_record_id}:{payload_hash}".encode()
        ).hexdigest()
        captured_at = utc_now_iso()
        return SourceEventV2(
            event_id=event_id,
            source_system=self.source_system,
            source_instance_id=self.instance_id,
            source_record_id=source_record_id,
            operation="UPSERT",
            source_version=str(source_version) if source_version is not None else payload_hash,
            event_time=captured_at,
            captured_at=captured_at,
            content_hash=payload_hash,
            payload=payload,
            metadata={
                "mapper_version": self.mapper_version,
                "record_kind": record_kind,
                "source_instance_id": self.instance_id,
            },
        )

    def _log_failure(self, category: str, correlation_id: str, status: int | None = None) -> None:
        logger.warning(
            "source connector request failed",
            extra={
                "source_system": self.source_system,
                "error_category": category,
                "correlation_id": correlation_id,
                "http_status": status,
            },
        )

    @staticmethod
    def correlation_id(value: str | None) -> str:
        return value or str(uuid4())
