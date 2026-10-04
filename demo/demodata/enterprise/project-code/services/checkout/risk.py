"""Reference implementation used by the Northstar sales-demo graph."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskDecision:
    approved: bool
    score: int
    reason: str


def score_order(amount_minor: int, account_age_days: int) -> int:
    """Return a deterministic 0-100 demo score; higher means greater risk."""
    amount_component = min(60, max(0, amount_minor // 10_000))
    account_component = 30 if account_age_days < 7 else 0
    return min(100, amount_component + account_component)


def authorize_order(amount_minor: int, account_age_days: int) -> RiskDecision:
    """Authorize a low-risk order and retain an explainable decision reason."""
    score = score_order(amount_minor, account_age_days)
    if score >= 70:
        return RiskDecision(False, score, "manual_review_required")
    return RiskDecision(True, score, "risk_below_threshold")
