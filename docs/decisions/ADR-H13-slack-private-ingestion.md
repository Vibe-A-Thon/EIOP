# H-13 — Slack Private Channels and Direct Messages Governance

| Field | Value |
|---|---|
| Decision | H-13 (CRA-006) |
| Status | **Accepted — 2026-10-18** |
| Owner | Legal / Compliance |
| Governs | CRA-006 |
| Date | 2026-10-18 |

## Context
Privacy and compliance implications of ingesting private team communications.

## Decision
Strict deny-by-default posture. Ingestion of private channels and direct messages is prohibited unless explicit, signed compliance authorization is recorded in tenant configuration.

## Alternatives Considered
- Unconstrained public/runtime access: Rejected due to security, licensing, or compliance risk.
- Indefinite deferral: Rejected to ensure deterministic architectural baseline for 100% requirements closure.

## Consequences
- Clean governance enforcement in automated CI pipelines.
- Traceable audit records linked to ledger acceptance state.
