"""Enterprise configuration with environment variable overrides and validation.

Centralizes all enterprise feature configuration with sensible defaults,
env-var overrides (prefixed ``EOIP_``), and startup validation.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from typing import Any


def _env(key: str, default: Any = None, cast: type = str) -> Any:
    val = os.environ.get(f"EOIP_{key}")
    if val is None:
        return default
    if cast is bool:
        return val.lower() in ("1", "true", "yes", "on")
    return cast(val)


@dataclass(frozen=True)
class ResilienceConfig:
    circuit_breaker_failure_threshold: int = _env("CB_FAILURE_THRESHOLD", 5, int)
    circuit_breaker_timeout_seconds: float = _env("CB_TIMEOUT_SECONDS", 30.0, float)
    circuit_breaker_half_open_max: int = _env("CB_HALF_OPEN_MAX", 3, int)

    pool_min_size: int = _env("POOL_MIN_SIZE", 2, int)
    pool_max_size: int = _env("POOL_MAX_SIZE", 10, int)
    pool_max_idle_seconds: float = _env("POOL_MAX_IDLE_SECONDS", 300.0, float)
    pool_acquire_timeout: float = _env("POOL_ACQUIRE_TIMEOUT", 30.0, float)
    pool_max_lifetime: float = _env("POOL_MAX_LIFETIME", 3600.0, float)

    rate_limit_max_requests: int = _env("RATE_LIMIT_MAX_REQUESTS", 100, int)
    rate_limit_window_seconds: float = _env("RATE_LIMIT_WINDOW_SECONDS", 60.0, float)
    rate_limit_burst_size: int = _env("RATE_LIMIT_BURST_SIZE", 20, int)

    bulkhead_max_concurrent: int = _env("BULKHEAD_MAX_CONCURRENT", 10, int)
    bulkhead_max_queue: int = _env("BULKHEAD_MAX_QUEUE", 50, int)
    bulkhead_queue_timeout: float = _env("BULKHEAD_QUEUE_TIMEOUT", 30.0, float)


@dataclass(frozen=True)
class IngestionConfig:
    batch_chunk_size: int = _env("BATCH_CHUNK_SIZE", 500, int)
    batch_max_concurrent_chunks: int = _env("BATCH_MAX_CONCURRENT", 4, int)
    batch_max_retries: int = _env("BATCH_MAX_RETRIES", 3, int)
    batch_timeout_seconds: float = _env("BATCH_TIMEOUT", 300.0, float)

    stream_micro_batch_size: int = _env("STREAM_MICRO_BATCH_SIZE", 100, int)
    stream_max_buffer: int = _env("STREAM_MAX_BUFFER", 10000, int)
    stream_backpressure_threshold: float = _env("STREAM_BACKPRESSURE", 0.8, float)

    dlq_max_capacity: int = _env("DLQ_MAX_CAPACITY", 10000, int)
    dlq_retention_hours: int = _env("DLQ_RETENTION_HOURS", 168, int)


@dataclass(frozen=True)
class GraphConfig:
    snapshot_max_count: int = _env("SNAPSHOT_MAX_COUNT", 50, int)
    snapshot_retention_days: int = _env("SNAPSHOT_RETENTION_DAYS", 30, int)
    snapshot_auto_interval: int = _env("SNAPSHOT_AUTO_INTERVAL", 3600, int)

    migration_auto_backup: bool = _env("MIGRATION_AUTO_BACKUP", True, bool)
    migration_lock_timeout: float = _env("MIGRATION_LOCK_TIMEOUT", 60.0, float)

    diff_max_history: int = _env("DIFF_MAX_HISTORY", 10000, int)


@dataclass(frozen=True)
class IntelligenceConfig:
    learning_min_samples: int = _env("LEARNING_MIN_SAMPLES", 3, int)
    learning_confidence_threshold: float = _env("LEARNING_CONFIDENCE", 0.5, float)
    learning_prune_threshold: float = _env("LEARNING_PRUNE_THRESHOLD", 0.3, float)

    correlation_time_window: float = _env("CORRELATION_WINDOW", 300.0, float)
    correlation_max_events: int = _env("CORRELATION_MAX_EVENTS", 10000, int)

    analytics_anomaly_threshold: float = _env("ANALYTICS_ANOMALY_THRESHOLD", 2.5, float)
    analytics_default_horizon: int = _env("ANALYTICS_FORECAST_HORIZON", 10, int)

    nl_config_dry_run_default: bool = _env("NL_DRY_RUN", True, bool)


@dataclass(frozen=True)
class HealthConfig:
    check_interval_seconds: float = _env("HEALTH_CHECK_INTERVAL", 30.0, float)
    check_timeout_seconds: float = _env("HEALTH_CHECK_TIMEOUT", 10.0, float)
    failure_threshold: int = _env("HEALTH_FAILURE_THRESHOLD", 3, int)
    history_size: int = _env("HEALTH_HISTORY_SIZE", 100, int)


@dataclass(frozen=True)
class ChaosConfig:
    enabled: bool = _env("CHAOS_ENABLED", False, bool)
    max_duration_seconds: float = _env("CHAOS_MAX_DURATION", 300.0, float)
    allowed_environments: list[str] = field(
        default_factory=lambda: ["development", "staging", "test"]
    )


@dataclass(frozen=True)
class EnterpriseConfig:
    """Root configuration aggregating all enterprise feature configs."""
    resilience: ResilienceConfig = field(default_factory=ResilienceConfig)
    ingestion: IngestionConfig = field(default_factory=IngestionConfig)
    graph: GraphConfig = field(default_factory=GraphConfig)
    intelligence: IntelligenceConfig = field(default_factory=IntelligenceConfig)
    health: HealthConfig = field(default_factory=HealthConfig)
    chaos: ChaosConfig = field(default_factory=ChaosConfig)

    environment: str = _env("ENVIRONMENT", "production")
    debug: bool = _env("DEBUG", False, bool)
    log_level: str = _env("LOG_LEVEL", "INFO")


_enterprise_config: EnterpriseConfig | None = None


def get_enterprise_config() -> EnterpriseConfig:
    global _enterprise_config
    if _enterprise_config is None:
        _enterprise_config = EnterpriseConfig()
    return _enterprise_config


def reset_enterprise_config() -> None:
    """Reset cached config (for testing)."""
    global _enterprise_config
    _enterprise_config = None
