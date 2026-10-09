"""Connection Pool — per-system connection pooling with health checks."""

from __future__ import annotations

import queue
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Protocol


class Connectable(Protocol):
    def connect(self) -> Any: ...
    def close(self) -> None: ...
    def is_alive(self) -> bool: ...


@dataclass
class PoolConfig:
    min_size: int = 2
    max_size: int = 10
    max_idle_seconds: float = 300.0
    acquire_timeout_seconds: float = 30.0
    health_check_interval_seconds: float = 60.0
    max_lifetime_seconds: float = 3600.0


@dataclass
class PoolMetrics:
    pool_size: int = 0
    active: int = 0
    idle: int = 0
    waiting: int = 0
    total_acquired: int = 0
    total_released: int = 0
    total_created: int = 0
    total_destroyed: int = 0
    total_timeouts: int = 0
    total_health_failures: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PooledConnection:
    conn_id: str
    connection: Any
    created_at: float
    last_used: float
    in_use: bool = False


class ConnectionPool:
    """Thread-safe connection pool with health checking and idle eviction."""

    def __init__(self, name: str, factory: Callable[[], Any],
                 config: PoolConfig | None = None) -> None:
        self.name = name
        self._factory = factory
        self._config = config or PoolConfig()
        self._pool: list[PooledConnection] = []
        self._lock = threading.Lock()
        self._semaphore = threading.Semaphore(self._config.max_size)
        self._metrics = PoolMetrics()
        self._closed = False

    def acquire(self, timeout: float | None = None) -> Any:
        timeout = timeout or self._config.acquire_timeout_seconds
        if not self._semaphore.acquire(timeout=timeout):
            with self._lock:
                self._metrics.total_timeouts += 1
            raise TimeoutError(f"Pool {self.name}: acquire timed out after {timeout}s")

        with self._lock:
            now = time.time()
            for pc in self._pool:
                if not pc.in_use and not self._is_expired(pc, now):
                    pc.in_use = True
                    pc.last_used = now
                    self._metrics.total_acquired += 1
                    self._metrics.active += 1
                    self._metrics.idle -= 1
                    return pc.connection

            if len(self._pool) < self._config.max_size:
                pc = self._create_connection()
                pc.in_use = True
                self._pool.append(pc)
                self._metrics.total_acquired += 1
                self._metrics.active += 1
                self._metrics.pool_size = len(self._pool)
                return pc.connection

        self._semaphore.release()
        raise RuntimeError(f"Pool {self.name}: no connections available")

    def release(self, connection: Any) -> None:
        with self._lock:
            for pc in self._pool:
                if pc.connection is connection and pc.in_use:
                    pc.in_use = False
                    pc.last_used = time.time()
                    self._metrics.total_released += 1
                    self._metrics.active -= 1
                    self._metrics.idle += 1
                    break
        self._semaphore.release()

    def close(self) -> None:
        with self._lock:
            self._closed = True
            for pc in self._pool:
                self._destroy_connection(pc)
            self._pool.clear()

    def evict_idle(self) -> int:
        evicted = 0
        now = time.time()
        with self._lock:
            remaining: list[PooledConnection] = []
            for pc in self._pool:
                if not pc.in_use and self._is_expired(pc, now):
                    self._destroy_connection(pc)
                    evicted += 1
                else:
                    remaining.append(pc)
            self._pool = remaining
            self._metrics.pool_size = len(self._pool)
            self._metrics.idle -= evicted
        return evicted

    def health_check(self) -> dict[str, Any]:
        healthy = 0
        unhealthy = 0
        with self._lock:
            for pc in self._pool:
                if not pc.in_use:
                    try:
                        if hasattr(pc.connection, "is_alive") and not pc.connection.is_alive():
                            self._destroy_connection(pc)
                            unhealthy += 1
                            self._metrics.total_health_failures += 1
                        else:
                            healthy += 1
                    except Exception:
                        unhealthy += 1
                        self._metrics.total_health_failures += 1
        return {"healthy": healthy, "unhealthy": unhealthy}

    def get_metrics(self) -> PoolMetrics:
        with self._lock:
            return PoolMetrics(**asdict(self._metrics))

    def _create_connection(self) -> PooledConnection:
        conn = self._factory()
        now = time.time()
        self._metrics.total_created += 1
        return PooledConnection(
            conn_id=uuid.uuid4().hex[:8], connection=conn,
            created_at=now, last_used=now,
        )

    def _destroy_connection(self, pc: PooledConnection) -> None:
        try:
            if hasattr(pc.connection, "close"):
                pc.connection.close()
        except Exception:
            pass
        self._metrics.total_destroyed += 1

    def _is_expired(self, pc: PooledConnection, now: float) -> bool:
        if now - pc.created_at > self._config.max_lifetime_seconds:
            return True
        if now - pc.last_used > self._config.max_idle_seconds:
            return True
        return False
