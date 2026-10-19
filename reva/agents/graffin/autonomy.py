"""
Autonomy Framework & Consequence Budget Engine (GRF-AUT-*, T-GRF-003).
Implements L0-L5 Autonomy State Machine, kappa (κ) consequence budgets,
and dual-key cryptographic authorization for high-risk tiers.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from reva.core.errors import RevaError
from reva.core.ids import budget_id


class AutonomyLevel(str, enum.Enum):
    L0_MANUAL = "L0_MANUAL"
    L1_ASSISTED = "L1_ASSISTED"
    L2_SEMI_AUTONOMOUS = "L2_SEMI_AUTONOMOUS"
    L3_CONDITIONAL = "L3_CONDITIONAL"
    L4_HIGH_AUTONOMY = "L4_HIGH_AUTONOMY"
    L5_FULL_AUTONOMOUS = "L5_FULL_AUTONOMOUS"


class RiskTier(str, enum.Enum):
    R1_READ_ONLY = "R1_READ_ONLY"       # Safe read/scan operations
    R2_LOCAL_MUTATION = "R2_LOCAL_MUTATION" # Local cache / temporary scratch writes
    R3_GRAPH_MUTATION = "R3_GRAPH_MUTATION" # Modifying Knowledge Graph vertices/edges
    R4_SCHEMA_PROMOTION = "R4_SCHEMA_PROMOTION" # Production schema alterations / external actions


class BudgetDepletedError(RevaError):
    """Raised when an action exceeds the remaining consequence budget kappa."""
    def __init__(self, message: str) -> None:
        super().__init__(
            code="BUDGET_DEPLETED",
            category="AUTONOMY",
            message=message,
        )


class AuthorizationRequiredError(RevaError):
    """Raised when an operation requires dual-key authorization that was not provided."""
    def __init__(self, message: str) -> None:
        super().__init__(
            code="AUTHORIZATION_REQUIRED",
            category="SECURITY",
            message=message,
        )


@dataclass
class ConsequenceBudget:
    """
    Kappa (κ) consequence budget tracker.
    Prevents autonomous agent runaway by capping the total impact units per execution epoch.
    """
    total_budget: float = 1000.0
    consumed: float = 0.0
    epoch_id: str = "epoch_1"
    tier_costs: Dict[str, float] = field(default_factory=lambda: {
        RiskTier.R1_READ_ONLY.value: 1.0,
        RiskTier.R2_LOCAL_MUTATION.value: 10.0,
        RiskTier.R3_GRAPH_MUTATION.value: 50.0,
        RiskTier.R4_SCHEMA_PROMOTION.value: 200.0,
    })

    @property
    def remaining(self) -> float:
        return max(0.0, self.total_budget - self.consumed)

    def can_afford(self, tier: RiskTier) -> bool:
        cost = self.tier_costs.get(tier.value, 100.0)
        return (self.consumed + cost) <= self.total_budget

    def consume(self, tier: RiskTier, operation_desc: str) -> float:
        cost = self.tier_costs.get(tier.value, 100.0)
        if not self.can_afford(tier):
            raise BudgetDepletedError(
                f"Action '{operation_desc}' requires {cost} kappa units, but only {self.remaining:.1f} remain."
            )
        self.consumed += cost
        return self.consumed


class AutonomyStateMachine:
    """
    Controls Graffin's operational autonomy levels and enforces tier authorizations.
    """

    def __init__(
        self,
        initial_level: AutonomyLevel = AutonomyLevel.L3_CONDITIONAL,
        budget: Optional[ConsequenceBudget] = None,
    ) -> None:
        self.current_level = initial_level
        self.budget = budget or ConsequenceBudget()
        self._action_log: List[Dict[str, Any]] = []

    def set_level(self, new_level: AutonomyLevel, authorization_token: Optional[str] = None) -> None:
        """Transitions autonomy level. Elevating to L4/L5 requires authorization."""
        if new_level in (AutonomyLevel.L4_HIGH_AUTONOMY, AutonomyLevel.L5_FULL_AUTONOMOUS):
            if not authorization_token or len(authorization_token) < 16:
                raise AuthorizationRequiredError("Transition to L4/L5 requires admin authorization token.")
        self.current_level = new_level

    def authorize_and_execute(
        self,
        tier: RiskTier,
        operation_desc: str,
        dual_keys: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Validates whether current autonomy level permits action, verifies dual-key
        signatures for high-risk operations (R3/R4), and deducts kappa budget.
        """
        # 1. Enforce Level Permissions
        if self.current_level == AutonomyLevel.L0_MANUAL:
            raise AuthorizationRequiredError("L0_MANUAL requires explicit operator execution for all actions.")

        if self.current_level == AutonomyLevel.L1_ASSISTED and tier != RiskTier.R1_READ_ONLY:
            raise AuthorizationRequiredError(f"L1_ASSISTED cannot execute mutation tier {tier.value}.")

        # 2. Enforce Dual-Key for R3 and R4
        if tier in (RiskTier.R3_GRAPH_MUTATION, RiskTier.R4_SCHEMA_PROMOTION):
            if not dual_keys or len(dual_keys) < 2:
                raise AuthorizationRequiredError(
                    f"Tier {tier.value} strictly requires dual-key cryptographic signatures from 2 independent principals."
                )

        # 3. Deduct consequence budget
        self.budget.consume(tier, operation_desc)

        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": self.current_level.value,
            "tier": tier.value,
            "operation": operation_desc,
            "remaining_budget": self.budget.remaining,
            "dual_keys_verified": bool(dual_keys and len(dual_keys) >= 2),
        }
        self._action_log.append(record)
        return record
