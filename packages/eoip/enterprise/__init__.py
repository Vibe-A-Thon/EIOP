"""EOIP Enterprise — production-grade infrastructure for enterprise deployments.

Provides the enterprise foundation layer: structured exception hierarchy,
centralized configuration, correlated logging, observability metrics,
API middleware, and typed response models.
"""

from eoip.enterprise.config import EnterpriseConfig, get_enterprise_config
from eoip.enterprise.exceptions import EnterpriseError
from eoip.enterprise.logging import get_logger
from eoip.enterprise.observability import MetricsCollector, get_metrics

__all__ = [
    "EnterpriseConfig",
    "EnterpriseError",
    "MetricsCollector",
    "get_enterprise_config",
    "get_logger",
    "get_metrics",
]
