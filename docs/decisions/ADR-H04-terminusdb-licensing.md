# H-04 — TerminusDB License Verification and Core Disposition

| Field | Value |
|---|---|
| Decision | H-04 (CRA-035, X-21) |
| Status | **Accepted — 2026-10-18** |
| Owner | Legal |
| Governs | CRA-035, X-21 |
| Date | 2026-10-18 |

## Context
Disputed license terms across TerminusDB distributions (Apache 2.0 vs GPLv3 components).

## Decision
TerminusDB is excluded from core Apache 2.0 distribution artifacts. Native LPG (RocksDB/Memory) and RDF triplestores serve as standard backends, avoiding any copyleft contamination.

## Alternatives Considered
- Unconstrained public/runtime access: Rejected due to security, licensing, or compliance risk.
- Indefinite deferral: Rejected to ensure deterministic architectural baseline for 100% requirements closure.

## Consequences
- Clean governance enforcement in automated CI pipelines.
- Traceable audit records linked to ledger acceptance state.
