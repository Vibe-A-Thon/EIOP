# Checkout risk architecture

Owner: Commerce Architecture  
Status: Approved  
Decision: ADR-COM-014  
Related delivery: PAY-142, FTR-42, release 2026.10.1

## Context

Northstar must reduce checkout abandonment while preventing high-risk orders from reaching payment authorization. The checkout API therefore asks the Risk Decision API for a bounded, explainable decision before calling the Payment Authorization API.

## Runtime flow

1. `POST /orders` validates the request and creates an order identifier.
2. Checkout calls `POST /v2/decisions` with non-card order signals.
3. Risk returns a score, an approve/review decision, and a reason code.
4. Approved orders proceed to tokenized payment authorization.
5. The decision reason and trace identifier are retained for audit; raw card data is never persisted in this graph.

## Reliability boundary

The synchronous risk call has a 250 ms budget. Retries are bounded to one attempt with jitter. The checkout API emits latency, timeout, fallback and authorization metrics tagged by deployment, but excludes customer secrets and payment details.

## Failure modes and safe fallback

- A timeout refuses high-value or new-account orders and routes them to manual review.
- A malformed response is treated as a refusal, never as an approval.
- Retry amplification is prevented by a single bounded retry.
- The approved emergency change is CHG0031088.
- Operators follow KB00192 and correlate alerts with the latest deployment before mitigation.

## Verification

TC-884 proves the low-risk contract and TC-901 proves timeout behavior. Pipeline 4815 must complete contract tests before the production deployment job can run.
