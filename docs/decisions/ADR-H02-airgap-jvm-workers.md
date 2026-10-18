# H-02 — Air-Gap JVM Worker Sidecars

| Field | Value |
|---|---|
| Decision | H-02 (CRA-019, CRA-035) |
| Status | **Accepted — 2026-10-18** |
| Owner | CTO / Security |
| Governs | CRA-019, CRA-035 |
| Date | 2026-10-18 |

## Context
Customer requirements for air-gapped environments that restrict Java runtimes or external dependencies for ELK / OWL API / ROBOT.

## Decision
JVM worker sidecars are permitted in air-gapped deployments via self-contained container images containing pre-packaged offline JARs. Pure-Python EL reasoner provides fallback when JVM sidecars are disabled.

## Alternatives Considered
- Unconstrained public/runtime access: Rejected due to security, licensing, or compliance risk.
- Indefinite deferral: Rejected to ensure deterministic architectural baseline for 100% requirements closure.

## Consequences
- Clean governance enforcement in automated CI pipelines.
- Traceable audit records linked to ledger acceptance state.
