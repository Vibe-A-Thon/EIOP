"""OpenTelemetry trace/metric ingestion connector (G2-SRC-OTEL-001..005).

Ingests OpenTelemetry trace spans and metric data points as SourceEventV2
envelopes. Requires the ``opentelemetry-sdk`` package at runtime; when
unavailable, ``health()`` reports UNAVAILABLE and data methods raise
``ImportError``.
"""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import UTC, datetime
from typing import Any

from eoip.connectors.base import ConnectorHealth, DiscoveredResource, DiscoveryResult, DiscoveryScope
from eoip.contracts.source_event import SourceEventV2, utc_now_iso

logger = logging.getLogger(__name__)

_OTEL_AVAILABLE = False
try:
    from opentelemetry import trace as _otel_trace  # noqa: F401

    _OTEL_AVAILABLE = True
except ImportError:
    pass


class OpenTelemetryConnector:
    """OpenTelemetry trace/metric ingestion connector (G2-SRC-OTEL-001..005).

    Provides ``discover``, ``extract``, ``checkpoint`` and ``health`` methods
    following the common connector pattern. Requires ``opentelemetry-sdk`` to
    be installed; when it is not, ``health()`` returns ``UNAVAILABLE`` and data
    methods raise ``ImportError``.
    """

    source_system = "opentelemetry"
    mapper_version = "otel-sdk/1.0"

    def __init__(
        self,
        *,
        source_id: str = "otel-default",
        endpoint: str | None = None,
    ) -> None:
        self.source_id = source_id
        self.endpoint = endpoint
        self._checkpoint: str | None = None

    def _require_otel(self) -> None:
        if not _OTEL_AVAILABLE:
            raise ImportError(
                "opentelemetry-sdk is required for OpenTelemetryConnector. "
                "Install it with: pip install opentelemetry-sdk"
            )

    def discover(self, scope: DiscoveryScope | None = None) -> DiscoveryResult:
        """Discover available OTel resource types (traces, metrics, logs)."""
        resources = [
            DiscoveredResource(
                resource_id="traces",
                resource_type="trace",
                name="OpenTelemetry Traces",
                metadata={"available": _OTEL_AVAILABLE},
            ),
            DiscoveredResource(
                resource_id="metrics",
                resource_type="metric",
                name="OpenTelemetry Metrics",
                metadata={"available": _OTEL_AVAILABLE},
            ),
            DiscoveredResource(
                resource_id="logs",
                resource_type="log",
                name="OpenTelemetry Logs",
                metadata={"available": _OTEL_AVAILABLE},
            ),
        ]
        return DiscoveryResult(source_id=self.source_id, resources=resources)

    def extract(
        self,
        spans: list[dict[str, Any]] | None = None,
        metrics: list[dict[str, Any]] | None = None,
    ) -> list[SourceEventV2]:
        """Extract OTel spans and metrics into SourceEventV2 envelopes.

        Parameters
        ----------
        spans:
            List of span dicts with ``trace_id``, ``span_id``, ``name``, etc.
        metrics:
            List of metric data-point dicts with ``name``, ``value``, etc.

        Returns
        -------
        list[SourceEventV2]
            Extracted source events.
        """
        self._require_otel()
        events: list[SourceEventV2] = []
        captured_at = utc_now_iso()

        for span in spans or []:
            span_id = span.get("span_id", "")
            trace_id = span.get("trace_id", "")
            record_id = f"{self.source_id}:trace:{trace_id}:{span_id}"
            payload_json = json.dumps(span, sort_keys=True, separators=(",", ":"))
            content_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
            event_id = hashlib.sha256(
                f"{self.source_system}:span:{record_id}:{content_hash}".encode()
            ).hexdigest()
            events.append(
                SourceEventV2(
                    event_id=event_id,
                    source_system=self.source_system,
                    source_instance_id=self.source_id,
                    source_record_id=record_id,
                    operation="UPSERT",
                    source_version=span.get("end_time") or captured_at,
                    event_time=span.get("start_time") or captured_at,
                    captured_at=captured_at,
                    content_hash=content_hash,
                    payload=span,
                    metadata={
                        "mapper_version": self.mapper_version,
                        "record_kind": "span",
                    },
                )
            )

        for metric in metrics or []:
            metric_name = metric.get("name", "unknown")
            metric_ts = metric.get("timestamp") or captured_at
            record_id = f"{self.source_id}:metric:{metric_name}:{metric_ts}"
            payload_json = json.dumps(metric, sort_keys=True, separators=(",", ":"))
            content_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
            event_id = hashlib.sha256(
                f"{self.source_system}:metric:{record_id}:{content_hash}".encode()
            ).hexdigest()
            events.append(
                SourceEventV2(
                    event_id=event_id,
                    source_system=self.source_system,
                    source_instance_id=self.source_id,
                    source_record_id=record_id,
                    operation="UPSERT",
                    source_version=content_hash[:16],
                    event_time=metric_ts,
                    captured_at=captured_at,
                    content_hash=content_hash,
                    payload=metric,
                    metadata={
                        "mapper_version": self.mapper_version,
                        "record_kind": "metric",
                    },
                )
            )

        return events

    def checkpoint(self) -> str | None:
        """Return the current extraction checkpoint."""
        return self._checkpoint

    def health(self) -> ConnectorHealth:
        """Check connector health; returns UNAVAILABLE when OTel SDK is missing."""
        checked_at = utc_now_iso()
        if not _OTEL_AVAILABLE:
            return ConnectorHealth(
                status="UNAVAILABLE",
                checked_at=checked_at,
                detail="opentelemetry-sdk is not installed",
            )
        return ConnectorHealth(
            status="HEALTHY",
            checked_at=checked_at,
            detail="OpenTelemetry SDK available",
        )
