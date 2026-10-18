# H-14 — Durable Event Backbone Architecture

| Field | Value |
|---|---|
| Decision | H-14 (CRA-010, CRA-031, INV-44) |
| Status | **Accepted — 2026-10-18** |
| Owner | Architect |
| Governs | CRA-010, CRA-031, INV-44 |
| Date | 2026-10-18 |

## Context
Event durability across single-node CPU installations versus distributed enterprise scale.

## Decision
PostgreSQL / transactional outbox pattern adopted as the standard durable backbone for P0 pure-python; Kafka / Redpanda streaming enabled for P1/P2 distributed tiers.

## Alternatives Considered
- Unconstrained public/runtime access: Rejected due to security, licensing, or compliance risk.
- Indefinite deferral: Rejected to ensure deterministic architectural baseline for 100% requirements closure.

## Consequences
- Clean governance enforcement in automated CI pipelines.
- Traceable audit records linked to ledger acceptance state.
