"""Connector Descriptors, Rate Limiting, and Conformance SDK.

Implements CRA-004.1, CRA-004.7, CRA-004.8, CRA-004.9, and CRA-004.12:
- ConnectorDescriptor with full capability matrix and derived is_certified state
- Token-bucket rate limiter with Retry-After and full jitter backoff (1s - 300s)
- Abstract BaseConnector conforming to the standard SDK
- Conformance harness runner for testing source adapters
"""
from __future__ import annotations

import abc
import random
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
from collections.abc import Iterator
from pydantic import BaseModel, Field

from eoip.connectors.errors import (
    ConnectorAuthFailedError,
    ConnectorSpecializationFailedError,
    ConnectorVersionUnsupportedError,
    RateLimitExceededError,
    UnsupportedCapabilityError,
)
from eoip.contracts.source_event import SourceEventV2


class ConnectorCapabilities(BaseModel):
    """Explicit per-capability descriptors per CRA-004.1 and CRA-004.7."""

    discovery: bool = True
    baseline_sync: bool = True
    polling_sync: bool = False
    webhook_push: bool = False
    cdc_stream: bool = False
    acl_preservation: bool = False
    attachments: bool = False
    delete: bool = False
    lineage: bool = False
    write_back: bool = False
    resumable_cursor: bool = True
    health: bool = True


class ConnectorDescriptor(BaseModel):
    """Universal Connector Descriptor per CRA-004.7."""

    provider_id: str
    display_name: str
    version: str
    supported_product_versions: List[str] = Field(default_factory=list)
    capabilities: ConnectorCapabilities = Field(default_factory=ConnectorCapabilities)
    auth_schemes: List[str] = Field(
        default_factory=lambda: ["oauth2", "bearer", "basic", "mtls", "app_installation"]
    )
    config_schema: Dict[str, Any] = Field(default_factory=dict)
    default_concurrency_limit: int = 2
    rate_limit_per_minute: int = 120
    receipt_refs: List[str] = Field(default_factory=list)

    @property
    def is_certified(self) -> bool:
        """Derived read-only attribute computed from valid qualification receipts (CRA-004.7)."""
        return len(self.receipt_refs) > 0


class TokenBucketRateLimiter:
    """Per-source-instance token-bucket rate limiter with full jitter backoff (CRA-004.8)."""

    def __init__(self, rate_limit_per_minute: int = 120, max_tokens: Optional[int] = None):
        self.rate_per_sec = rate_limit_per_minute / 60.0
        self.capacity = max_tokens or rate_limit_per_minute
        self.tokens = float(self.capacity)
        self.last_update = time.monotonic()
        self.retry_until: float = 0.0

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self.last_update
        self.last_update = now
        self.tokens = min(float(self.capacity), self.tokens + elapsed * self.rate_per_sec)

    def acquire(self, tokens: int = 1) -> bool:
        now = time.monotonic()
        if now < self.retry_until:
            return False
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def handle_response_headers(self, headers: Dict[str, str]) -> None:
        """Inspects Retry-After and vendor rate-limit headers (CRA-004.8)."""
        now = time.monotonic()
        # 1. Retry-After
        retry_after = headers.get("Retry-After") or headers.get("retry-after")
        if retry_after:
            try:
                seconds = float(retry_after)
                self.retry_until = now + seconds
            except ValueError:
                pass

        # 2. X-RateLimit-Remaining
        remaining = headers.get("X-RateLimit-Remaining") or headers.get("x-ratelimit-remaining")
        if remaining is not None:
            try:
                rem_val = int(remaining)
                if rem_val == 0:
                    reset_in = float(headers.get("X-RateLimit-Reset", 1.0))
                    self.retry_until = max(self.retry_until, now + min(reset_in, 300.0))
            except ValueError:
                pass

    def compute_backoff(self, attempt: int, base: float = 1.0, cap: float = 300.0) -> float:
        """Computes exponential backoff with full jitter: sleep = uniform(0, min(cap, base * 2 ** attempt))."""
        calculated_cap = min(cap, base * (2 ** attempt))
        return random.uniform(0.0, calculated_cap)


class BaseConnector(abc.ABC):
    """Abstract BaseConnector conforming to the standard SDK (CRA-004.9)."""

    def __init__(self, descriptor: ConnectorDescriptor, config: Dict[str, Any]):
        self.descriptor = descriptor
        self.config = config
        self.rate_limiter = TokenBucketRateLimiter(
            rate_limit_per_minute=descriptor.rate_limit_per_minute,
            max_tokens=descriptor.default_concurrency_limit * 10,
        )

    def validate_version(self, product_version: str) -> None:
        """Validates remote product version against supported_product_versions."""
        if self.descriptor.supported_product_versions:
            if product_version not in self.descriptor.supported_product_versions:
                raise ConnectorVersionUnsupportedError(
                    source_system=self.descriptor.provider_id,
                    version=product_version,
                    supported_versions=self.descriptor.supported_product_versions,
                )

    def require_capability(self, capability_name: str) -> None:
        """Ensures the connector declares the required capability before execution."""
        caps = self.descriptor.capabilities.model_dump()
        if not caps.get(capability_name, False):
            raise UnsupportedCapabilityError(
                source_system=self.descriptor.provider_id,
                capability=capability_name,
            )

    @abc.abstractmethod
    def discover(self, scope: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Discovers resources in the source."""
        pass

    @abc.abstractmethod
    def baseline(self, cursor: Optional[str] = None) -> Iterator[SourceEventV2]:
        """Performs initial baseline synchronization."""
        pass

    @abc.abstractmethod
    def poll(self, cursor: str) -> Iterator[SourceEventV2]:
        """Polls for incremental updates using a cursor."""
        pass

    def handle_webhook(self, event: Dict[str, Any]) -> Iterator[SourceEventV2]:
        self.require_capability("webhook_push")
        yield from []

    def fetch_acl(self, resource_id: str) -> Dict[str, Any]:
        self.require_capability("acl_preservation")
        return {"resource_id": resource_id, "permissions": []}

    def fetch_attachment(self, ref: str) -> bytes:
        self.require_capability("attachments")
        return b""

    def write(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Write-back execution; strictly denied if write_back is undeclared (CRA-004.9)."""
        self.require_capability("write_back")
        return {"status": "SUCCESS", "intent_id": intent.get("id")}

    def health(self) -> Dict[str, Any]:
        return {
            "status": "HEALTHY",
            "provider_id": self.descriptor.provider_id,
            "version": self.descriptor.version,
            "is_certified": self.descriptor.is_certified,
        }


class ConformanceRunner:
    """Conformance test runner verifying connector implementations (CRA-004.4, CRA-004.A)."""

    @classmethod
    def test_auth_failure(cls, connector_cls: type[BaseConnector], bad_config: Dict[str, Any]) -> bool:
        """Verifies that invalid credentials raise ConnectorAuthFailedError."""
        try:
            conn = connector_cls(config=bad_config)
            # Try operation
            list(conn.baseline())
            return False
        except ConnectorAuthFailedError:
            return True
        except Exception:
            return False

    @classmethod
    def test_version_check(cls, connector: BaseConnector, invalid_ver: str) -> bool:
        """Verifies that an unsupported product version raises ConnectorVersionUnsupportedError."""
        try:
            connector.validate_version(invalid_ver)
            return False
        except ConnectorVersionUnsupportedError:
            return True

    @classmethod
    def test_undeclared_write_back_rejected(cls, connector: BaseConnector) -> bool:
        """Verifies that undeclared write_back raises UnsupportedCapabilityError."""
        try:
            connector.write({"action": "UPDATE", "target": "task-1"})
            return False
        except UnsupportedCapabilityError:
            return True
