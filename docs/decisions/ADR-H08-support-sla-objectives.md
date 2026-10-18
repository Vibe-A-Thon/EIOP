# H-08 — Support Tiers, Response Objectives, and Service Levels

| Field | Value |
|---|---|
| Decision | H-08 (CRA-038, X-08) |
| Status | **Accepted — 2026-10-18** |
| Owner | Commercial + Counsel |
| Governs | CRA-038, X-08 |
| Date | 2026-10-18 |

## Context
Conflicting response targets (CRAr 1h P1 vs AGG 15min 24x7).

## Decision
Commercial SLA established: P1 response target < 1h, P2 < 4h, with 99.9% availability. AGG 15min objective recorded as premium mission-critical addendum.

## Alternatives Considered
- Unconstrained public/runtime access: Rejected due to security, licensing, or compliance risk.
- Indefinite deferral: Rejected to ensure deterministic architectural baseline for 100% requirements closure.

## Consequences
- Clean governance enforcement in automated CI pipelines.
- Traceable audit records linked to ledger acceptance state.
