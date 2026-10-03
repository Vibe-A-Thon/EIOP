"""Framework-neutral checkout handler used as ingestible sample code."""

from services.checkout.risk import authorize_order


def create_order(payload: dict) -> dict:
    decision = authorize_order(
        int(payload["amount_minor"]),
        int(payload["account_age_days"]),
    )
    return {
        "order_id": payload["order_id"],
        "authorized": decision.approved,
        "risk_score": decision.score,
        "decision_reason": decision.reason,
    }
