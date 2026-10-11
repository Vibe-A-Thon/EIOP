"""Integration Bus — connector framework with health monitoring and sync tracking.

Manages external system connectors (databases, APIs, SaaS tools) with
health checks, sync history, and bidirectional data flow tracking.
"""

from __future__ import annotations

import enum
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable


class ConnectorStatus(str, enum.Enum):
    REGISTERED = "REGISTERED"
    CONNECTED = "CONNECTED"
    SYNCING = "SYNCING"
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DISCONNECTED = "DISCONNECTED"
    ERROR = "ERROR"


class SyncDirection(str, enum.Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"
    BIDIRECTIONAL = "BIDIRECTIONAL"


@dataclass
class ConnectorConfig:
    connector_type: str
    name: str
    endpoint: str = ""
    auth_method: str = "none"
    sync_direction: SyncDirection = SyncDirection.INBOUND
    sync_interval_seconds: float = 3600.0
    batch_size: int = 100
    retry_attempts: int = 3
    timeout_seconds: float = 30.0
    custom_settings: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "connector_type": self.connector_type,
            "name": self.name,
            "endpoint": self.endpoint,
            "auth_method": self.auth_method,
            "sync_direction": self.sync_direction.value,
            "sync_interval_seconds": self.sync_interval_seconds,
            "batch_size": self.batch_size,
            "retry_attempts": self.retry_attempts,
            "timeout_seconds": self.timeout_seconds,
        }


@dataclass
class SyncRecord:
    sync_id: str
    connector_id: str
    direction: SyncDirection
    status: str
    records_processed: int = 0
    records_failed: int = 0
    started_at: float = field(default_factory=time.time)
    completed_at: float | None = None
    duration_ms: float = 0.0
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "sync_id": self.sync_id,
            "connector_id": self.connector_id,
            "direction": self.direction.value,
            "status": self.status,
            "records_processed": self.records_processed,
            "records_failed": self.records_failed,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_ms": round(self.duration_ms, 2),
            "error": self.error,
        }


@dataclass
class IntegrationConnector:
    connector_id: str
    config: ConnectorConfig
    status: ConnectorStatus = ConnectorStatus.REGISTERED
    tenant_id: str | None = None
    last_health_check: float | None = None
    last_sync_at: float | None = None
    total_syncs: int = 0
    total_records_synced: int = 0
    total_errors: int = 0
    consecutive_failures: int = 0
    sync_history: list[SyncRecord] = field(default_factory=list)
    health_fn: Callable[[], bool] | None = None
    sync_fn: Callable[[int], tuple[int, int]] | None = None
    created_at: float = field(default_factory=time.time)
    max_history: int = 50

    def to_dict(self) -> dict[str, Any]:
        return {
            "connector_id": self.connector_id,
            "name": self.config.name,
            "connector_type": self.config.connector_type,
            "status": self.status.value,
            "endpoint": self.config.endpoint,
            "sync_direction": self.config.sync_direction.value,
            "last_health_check": self.last_health_check,
            "last_sync_at": self.last_sync_at,
            "total_syncs": self.total_syncs,
            "total_records_synced": self.total_records_synced,
            "total_errors": self.total_errors,
            "consecutive_failures": self.consecutive_failures,
            "created_at": self.created_at,
        }


class IntegrationBus:
    """Connector framework with health monitoring and sync tracking."""

    def __init__(self) -> None:
        self._connectors: dict[str, IntegrationConnector] = {}
        self._lock = threading.Lock()

    def register(self, config: ConnectorConfig,
                 tenant_id: str | None = None,
                 health_fn: Callable[[], bool] | None = None,
                 sync_fn: Callable[[int], tuple[int, int]] | None = None) -> IntegrationConnector:
        connector = IntegrationConnector(
            connector_id=uuid.uuid4().hex[:12],
            config=config,
            tenant_id=tenant_id,
            health_fn=health_fn,
            sync_fn=sync_fn,
        )
        with self._lock:
            self._connectors[connector.connector_id] = connector
        return connector

    def get(self, connector_id: str) -> IntegrationConnector | None:
        with self._lock:
            return self._connectors.get(connector_id)

    def check_health(self, connector_id: str) -> ConnectorStatus:
        with self._lock:
            conn = self._connectors.get(connector_id)
        if conn is None:
            return ConnectorStatus.ERROR

        now = time.time()
        if conn.health_fn:
            try:
                healthy = conn.health_fn()
                with self._lock:
                    conn.last_health_check = now
                    if healthy:
                        conn.status = ConnectorStatus.HEALTHY
                        conn.consecutive_failures = 0
                    else:
                        conn.consecutive_failures += 1
                        conn.status = (ConnectorStatus.DEGRADED
                                       if conn.consecutive_failures < 3
                                       else ConnectorStatus.ERROR)
            except Exception:
                with self._lock:
                    conn.consecutive_failures += 1
                    conn.status = ConnectorStatus.ERROR
                    conn.last_health_check = now
        else:
            with self._lock:
                conn.last_health_check = now
                conn.status = ConnectorStatus.CONNECTED

        return conn.status

    def sync(self, connector_id: str) -> SyncRecord | None:
        with self._lock:
            conn = self._connectors.get(connector_id)
        if conn is None:
            return None

        record = SyncRecord(
            sync_id=uuid.uuid4().hex[:12],
            connector_id=connector_id,
            direction=conn.config.sync_direction,
            status="RUNNING",
        )

        start = time.time()
        processed = 0
        failed = 0

        if conn.sync_fn:
            try:
                with self._lock:
                    conn.status = ConnectorStatus.SYNCING
                processed, failed = conn.sync_fn(conn.config.batch_size)
                record.status = "COMPLETED" if failed == 0 else "PARTIAL"
            except Exception as exc:
                record.status = "FAILED"
                record.error = str(exc)
                failed = 1
        else:
            record.status = "COMPLETED"

        end = time.time()
        record.records_processed = processed
        record.records_failed = failed
        record.completed_at = end
        record.duration_ms = (end - start) * 1000

        with self._lock:
            conn.total_syncs += 1
            conn.total_records_synced += processed
            conn.total_errors += failed
            conn.last_sync_at = end
            if record.status == "FAILED":
                conn.consecutive_failures += 1
                conn.status = ConnectorStatus.ERROR
            else:
                conn.consecutive_failures = 0
                conn.status = ConnectorStatus.HEALTHY
            conn.sync_history.append(record)
            if len(conn.sync_history) > conn.max_history:
                conn.sync_history = conn.sync_history[-conn.max_history:]

        return record

    def check_all_health(self) -> dict[str, str]:
        with self._lock:
            ids = list(self._connectors.keys())
        results = {}
        for cid in ids:
            results[cid] = self.check_health(cid).value
        return results

    def sync_due(self) -> list[SyncRecord]:
        now = time.time()
        due: list[str] = []
        with self._lock:
            for conn in self._connectors.values():
                if conn.status in (ConnectorStatus.ERROR, ConnectorStatus.DISCONNECTED):
                    continue
                interval = conn.config.sync_interval_seconds
                if conn.last_sync_at is None or (now - conn.last_sync_at) >= interval:
                    due.append(conn.connector_id)

        records = []
        for cid in due:
            rec = self.sync(cid)
            if rec:
                records.append(rec)
        return records

    def disconnect(self, connector_id: str) -> bool:
        with self._lock:
            conn = self._connectors.get(connector_id)
            if conn is None:
                return False
            conn.status = ConnectorStatus.DISCONNECTED
            return True

    def remove(self, connector_id: str) -> bool:
        with self._lock:
            return self._connectors.pop(connector_id, None) is not None

    def list_connectors(self, status: ConnectorStatus | None = None,
                        connector_type: str | None = None) -> list[dict[str, Any]]:
        with self._lock:
            connectors = list(self._connectors.values())
        results = []
        for c in connectors:
            if status and c.status != status:
                continue
            if connector_type and c.config.connector_type != connector_type:
                continue
            results.append(c.to_dict())
        return results

    def get_sync_history(self, connector_id: str,
                         limit: int = 20) -> list[dict[str, Any]]:
        with self._lock:
            conn = self._connectors.get(connector_id)
            if conn is None:
                return []
            return [r.to_dict() for r in reversed(conn.sync_history[-limit:])]

    def stats(self) -> dict[str, Any]:
        with self._lock:
            by_status: dict[str, int] = {}
            by_type: dict[str, int] = {}
            total_syncs = 0
            total_records = 0
            for c in self._connectors.values():
                by_status[c.status.value] = by_status.get(c.status.value, 0) + 1
                by_type[c.config.connector_type] = by_type.get(c.config.connector_type, 0) + 1
                total_syncs += c.total_syncs
                total_records += c.total_records_synced
            return {
                "total_connectors": len(self._connectors),
                "by_status": by_status,
                "by_type": by_type,
                "total_syncs": total_syncs,
                "total_records_synced": total_records,
            }


_INSTANCE: IntegrationBus | None = None
_LOCK = threading.Lock()


def get_integration_bus() -> IntegrationBus:
    global _INSTANCE
    if _INSTANCE is None:
        with _LOCK:
            if _INSTANCE is None:
                _INSTANCE = IntegrationBus()
    return _INSTANCE
