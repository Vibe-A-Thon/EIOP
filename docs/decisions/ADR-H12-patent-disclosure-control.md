# H-12 — Patent Candidate Disclosure Control

| Field | Value |
|---|---|
| Decision | H-12 (CRA-041.6, OCA Section 8.3) |
| Status | **Accepted — 2026-10-18** |
| Owner | Legal / IP |
| Governs | CRA-041.6, OCA Section 8.3 |
| Date | 2026-10-18 |

## Context
Five patent candidates identified in OCA section 8.3 requiring protection from inadvertent public disclosure.

## Decision
All 5 candidates placed in restricted register (`docs/restricted/patent-candidates.yaml`). Public disclosure is blocked by automated CI scanners until formal patent provisional filing decisions are executed.

## Alternatives Considered
- Unconstrained public/runtime access: Rejected due to security, licensing, or compliance risk.
- Indefinite deferral: Rejected to ensure deterministic architectural baseline for 100% requirements closure.

## Consequences
- Clean governance enforcement in automated CI pipelines.
- Traceable audit records linked to ledger acceptance state.
