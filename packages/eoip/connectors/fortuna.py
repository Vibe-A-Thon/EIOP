"""Fortuna connector state and governance contract (CRA-009.3, CRA-009.8).

Enforces:
1. Fortuna product-specific adapter remains strictly blocked until Decision H-06 resolves
   its product identity, interface/schema, and network/auth contract.
2. The connector refuses to invent or expose an unverified, imaginary Fortuna API.
3. Exposes the configured generic custom-system adapter as an alternative alongside
   the explicit missing-input reason.
"""

from __future__ import annotations

from typing import Any

from eoip.connectors.errors import ConnectorError

FORTUNA_DECISION_REF = "H-06"
FORTUNA_MISSING_INPUT_REASON = (
    "Product identity, interface/schema specifications, network endpoints, and "
    "authentication contracts for 'Fortuna' are unspecified pending Decision H-06. "
    "To connect arbitrary enterprise systems in the interim, use GenericCustomSystemConnector "
    "or GenericRestApplicationConnector with verified CML mapping IR."
)


class FortunaConnectorBlockedError(ConnectorError):
    """Raised when an operation attempts to instantiate or execute unverified Fortuna product adapter."""

    def __init__(self, message: str = FORTUNA_MISSING_INPUT_REASON) -> None:
        super().__init__(
            source_system="fortuna",
            category="adapter_blocked_pending_decision",
            code="FORTUNA_UNSPECIFIED_DECISION_H06",
            details={
                "decision_ref": FORTUNA_DECISION_REF,
                "missing_input_reason": FORTUNA_MISSING_INPUT_REASON,
                "recommended_alternative": "GenericCustomSystemConnector",
            },
        )


class FortunaConnector:
    """Placeholder representing the unverified Fortuna adapter."""

    is_blocked: bool = True
    blocked_by: str = FORTUNA_DECISION_REF
    missing_input_reason: str = FORTUNA_MISSING_INPUT_REASON
    recommended_alternative: str = "GenericCustomSystemConnector"

    def __init__(self, *args, **kwargs) -> None:
        raise FortunaConnectorBlockedError()

    @classmethod
    def get_adapter_status(cls) -> dict[str, Any]:
        """Return the current qualification status of the Fortuna adapter."""
        return {
            "source_system": "fortuna",
            "is_blocked": cls.is_blocked,
            "blocked_by": cls.blocked_by,
            "missing_input_reason": cls.missing_input_reason,
            "recommended_alternative": cls.recommended_alternative,
        }
