"""EOIP Enterprise — production-grade infrastructure for enterprise deployments.

Provides the enterprise foundation layer: structured exception hierarchy,
centralized configuration, correlated logging, observability metrics,
API middleware, typed response models, and universal OCI container-runtime
discovery.
"""

from eoip.enterprise.config import EnterpriseConfig, get_enterprise_config
from eoip.enterprise.container_runtime import ContainerRuntime, discover as discover_runtime
from eoip.enterprise.exceptions import EnterpriseError
from eoip.enterprise.logging import get_logger
from eoip.enterprise.observability import MetricsCollector, get_metrics

__all__ = [
    "ContainerRuntime",
    "EnterpriseConfig",
    "EnterpriseError",
    "MetricsCollector",
    "discover_runtime",
    "get_enterprise_config",
    "get_logger",
    "get_metrics",
]
