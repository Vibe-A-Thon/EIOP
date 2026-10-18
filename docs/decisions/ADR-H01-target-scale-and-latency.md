# H-01 — Target Scale and Contractual Latency Objectives

| Field | Value |
|---|---|
| Decision | H-01 (CRA-036, X-05, X-06) |
| Status | **Accepted — 2026-10-18** |
| Owner | CTO |
| Governs | CRA-036, X-05, X-06 |
| Date | 2026-10-18 |

## Context
Contractual scale tiers and latency SLAs (point read <= 250ms P1, <= 500ms P2) versus stretch target of p95 < 20ms.

## Decision
Contractual binding targets remain p95 <= 250ms for P1 and <= 500ms for P2 on CPU reference hardware. The 20ms target is classified as an AGG stretch objective and reported separately in benchmark telemetry without failing promotion gates.

## Alternatives Considered
- Unconstrained public/runtime access: Rejected due to security, licensing, or compliance risk.
- Indefinite deferral: Rejected to ensure deterministic architectural baseline for 100% requirements closure.

## Consequences
- Clean governance enforcement in automated CI pipelines.
- Traceable audit records linked to ledger acceptance state.
