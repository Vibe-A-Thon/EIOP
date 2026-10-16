from services.checkout.risk import authorize_order


def test_low_risk_order_is_authorized():
    decision = authorize_order(amount_minor=4_999, account_age_days=365)
    assert decision.approved is True
    assert decision.reason == "risk_below_threshold"


def test_high_risk_order_requires_review():
    decision = authorize_order(amount_minor=500_000, account_age_days=1)
    assert decision.approved is False
    assert decision.reason == "manual_review_required"
