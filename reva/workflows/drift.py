"""Source to deployed drift detection and anomaly verification (T-703 / DV-001..005)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


@dataclass
class DriftAnomaly:
    anomaly_type: str  # undeclared_runtime_call | dead_code_route | missing_deployed_artifact | dirty_build
    description: str
    target_identifier: str
    severity: str = "medium"


@dataclass
class DriftReport:
    tenant_id: str
    scope: str
    anomalies: List[DriftAnomaly] = field(default_factory=list)
    has_drift: bool = False


def verify_system_drift(
    tenant_id: str,
    scope: str,
    static_routes: Set[str],
    runtime_observed_calls: Set[str],
    is_dirty_build: bool = False,
) -> DriftReport:
    """Compare declared static architecture against runtime evidence."""
    anomalies: List[DriftAnomaly] = []

    if is_dirty_build:
        anomalies.append(
            DriftAnomaly(
                anomaly_type="dirty_build",
                description="Deployed build contains uncommitted working tree modifications",
                target_identifier=scope,
                severity="high",
            )
        )

    # 1. Undeclared runtime calls (observed in traffic but not declared in static boundaries)
    for call in sorted(list(runtime_observed_calls)):
        if call not in static_routes:
            anomalies.append(
                DriftAnomaly(
                    anomaly_type="undeclared_runtime_call",
                    description=f"Runtime traffic observed for endpoint '{call}' with no declared static boundary",
                    target_identifier=call,
                    severity="medium",
                )
            )

    # 2. Dead code routes (declared in static code but never observed in runtime traffic)
    for route in sorted(list(static_routes)):
        if route not in runtime_observed_calls:
            anomalies.append(
                DriftAnomaly(
                    anomaly_type="dead_code_route",
                    description=f"Static route '{route}' has zero observed runtime traffic",
                    target_identifier=route,
                    severity="low",
                )
            )

    return DriftReport(
        tenant_id=tenant_id,
        scope=scope,
        anomalies=anomalies,
        has_drift=len(anomalies) > 0,
    )
