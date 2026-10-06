"""Operational excellence tooling (requirements §47).

Submodules:
- preflight: startup/operational preflight checks.
- upgrade: version-to-version upgrade planner reusing ontology diff machinery.
- bundle: redacted health / support bundle collector.

Stable IDs use the ``urn:eoip:ops:<type>:<id>`` scheme.
"""

from eoip.ops.bundle import collect_support_bundle
from eoip.ops.preflight import CheckResult, PreflightReport, run_preflight
from eoip.ops.production import CacheTopology, HighAvailabilityTopology, build_shard_plan, default_ha_topology, helm_release_summary
from eoip.ops.upgrade import plan_upgrade

__all__ = [
    "CheckResult",
    "PreflightReport",
    "run_preflight",
    "plan_upgrade",
    "collect_support_bundle",
    "CacheTopology",
    "HighAvailabilityTopology",
    "default_ha_topology",
    "build_shard_plan",
    "helm_release_summary",
]
