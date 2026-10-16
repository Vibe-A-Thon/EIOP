"""EOIP Enterprise — production-grade infrastructure for enterprise deployments.

Provides the enterprise foundation layer: structured exception hierarchy,
centralized configuration, correlated logging, observability metrics,
API middleware, typed response models, universal OCI container-runtime
discovery, circuit breaker, rate limiting, audit logging, health probes,
intelligent caching, plugin extensibility, lifecycle management, feature
flags, retry with exponential backoff, and webhook event notifications.
"""

from eoip.enterprise.config import EnterpriseConfig, get_enterprise_config
from eoip.enterprise.container_runtime import ContainerRuntime, discover as discover_runtime
from eoip.enterprise.exceptions import EnterpriseError
from eoip.enterprise.logging import get_logger
from eoip.enterprise.observability import MetricsCollector, get_metrics
from eoip.enterprise.circuit_breaker import CircuitBreaker, CircuitBreakerRegistry, get_circuit_breaker_registry
from eoip.enterprise.rate_limiter import RateLimiter
from eoip.enterprise.audit import AuditLog, AuditCategory, get_audit_log
from eoip.enterprise.health import HealthProbe, HealthStatus, ComponentHealth
from eoip.enterprise.cache import IntelligentCache, get_cache
from eoip.enterprise.plugin import PluginRegistry, PluginCapability, get_plugin_registry
from eoip.enterprise.lifecycle import LifecycleManager, LifecyclePhase, LifecycleComponent, get_lifecycle_manager
from eoip.enterprise.feature_flags import FeatureFlagRegistry, FlagDefinition, get_feature_flags
from eoip.enterprise.retry import RetryPolicy, RetryableOperation, retry_sync, RetryExhausted
from eoip.enterprise.webhooks import WebhookManager, WebhookEventType, get_webhook_manager

__all__ = [
    "AuditCategory",
    "AuditLog",
    "CircuitBreaker",
    "CircuitBreakerRegistry",
    "ComponentHealth",
    "ContainerRuntime",
    "EnterpriseConfig",
    "EnterpriseError",
    "FeatureFlagRegistry",
    "FlagDefinition",
    "HealthProbe",
    "HealthStatus",
    "IntelligentCache",
    "LifecycleComponent",
    "LifecycleManager",
    "LifecyclePhase",
    "MetricsCollector",
    "PluginCapability",
    "PluginRegistry",
    "RateLimiter",
    "RetryExhausted",
    "RetryPolicy",
    "RetryableOperation",
    "WebhookEventType",
    "WebhookManager",
    "discover_runtime",
    "get_audit_log",
    "get_cache",
    "get_circuit_breaker_registry",
    "get_enterprise_config",
    "get_feature_flags",
    "get_lifecycle_manager",
    "get_logger",
    "get_metrics",
    "get_plugin_registry",
    "get_webhook_manager",
    "retry_sync",
]
