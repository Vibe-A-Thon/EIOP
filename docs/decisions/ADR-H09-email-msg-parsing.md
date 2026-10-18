# H-09 — Outlook MSG Parsing Distribution Terms

| Field | Value |
|---|---|
| Decision | H-09 (CRA-013, CRA-035, X-16) |
| Status | **Accepted — 2026-10-18** |
| Owner | Legal |
| Governs | CRA-013, CRA-035, X-16 |
| Date | 2026-10-18 |

## Context
Unresolved licensing terms for extract-msg and third-party Outlook format libraries.

## Decision
extract-msg library is isolated from core distribution; permissive fallback email parsers (EML, MIME) enabled by default; MSG support offered as optional isolated plugin.

## Alternatives Considered
- Unconstrained public/runtime access: Rejected due to security, licensing, or compliance risk.
- Indefinite deferral: Rejected to ensure deterministic architectural baseline for 100% requirements closure.

## Consequences
- Clean governance enforcement in automated CI pipelines.
- Traceable audit records linked to ledger acceptance state.
