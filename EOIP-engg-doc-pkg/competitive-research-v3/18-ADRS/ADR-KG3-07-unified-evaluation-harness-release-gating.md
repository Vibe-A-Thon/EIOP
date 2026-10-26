# ADR-KG3-07: Unified Evaluation Harness as Release-Gating Infrastructure

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-26 |
| Supersedes | The 2026-10-19 placeholder of this file (same path, different topic) |
| Based on | `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-07 |
| Gap | GAP-43 (`07-GAP-REGISTER.md`, forced P0, High severity) |
| Capability | CAP-78 (Evaluation and benchmark harness) |

## Context

Every quantitative claim this research package or any future EOIP release wants to make about its own behaviour — backend parity (BM-01), ACL leakage (BM-04), tenant isolation (BM-05), citation accuracy (BM-06), SHACL conformance (BM-08), large-graph rendering (BM-13) — is currently unverifiable at the platform level, because no harness runs the full BM-01 through BM-22 set together with pass/fail regression thresholds gating a release. `qa_bench/` and `retrieval/eval.py` exist and run deterministic retrieval evaluation, but this is one slice, not the cross-cutting infrastructure Master Prompt §12 describes. This gap is unusual among the eleven self-inversion cards: it is not a feature with its own user-facing value, it is the precondition for every other card's falsifiable benchmark actually being run rather than merely specified. INV-SELF-07's own text states this plainly: "every other self-inversion card's benchmark depends on this harness existing."

## Options considered

1. **Quick integration** — wire the existing ad hoc tests into one `pytest` marker set with explicit pass/fail thresholds, so at least today's scattered tests report against the BM-ID numbering consistently.
2. **Pragmatic native enhancement** — a dedicated harness project (extending `qa_bench`) with fixtures, data generators and reproducibility metadata (hardware, dataset, software versions, warm-up, cache state, repetitions, variance) captured per Master Prompt §12's explicit requirements, so that every run is comparable to every other run.
3. **Long-term** — a public benchmark dashboard, comparable in spirit to LDBC's audited runs but explicitly labelled "not LDBC Benchmark Results" (per LDBC's own trademark terms, as `STR-ldbc-01` already notes for the LDBC SNB workload generator), as a later credibility move once the internal harness is proven.

## Options rejected and why

Option 1 alone is rejected as sufficient because it does not capture reproducibility metadata — a `pytest` marker without recorded hardware, dataset and version information produces a pass/fail result that cannot be compared across runs or trusted months later, which is exactly the failure mode Master Prompt §12 calls out ("state hardware, workload generator, dataset license, query mix, warm-up, cache state, repetitions, variance, configuration, and versions").

## Decision

Adopt option 2 as the immediate build target, treating the harness itself as a first-class P0 deliverable rather than test-suite housekeeping. Option 3 is deferred to a later credibility phase, contingent on option 2 being proven and stable — publishing externally before the internal harness is trustworthy would be premature. Every BM-ID referenced throughout this architecture document and the other eleven ADRs (BM-01 conformance, BM-04 ACL leakage, BM-05 tenant isolation, and so on) is understood to execute inside this one harness, not as an independent one-off script per claim.

## Consequences

**Positive:** closes the highest-leverage forced P0 in the register — every other ADR in this set (ADR-KG3-01 through ADR-KG3-05 and ADR-KG3-08 through ADR-KG3-11) names a BM-ID as its falsifiable benchmark, and none of those benchmarks is currently runnable as a gated, reproducible artefact without this harness. Converts the entire research package's claims from "specified" to "verifiable."

**Negative:** this is M-effort infrastructure work with no standalone feature to show for it — it is explicitly "infrastructure, not a feature," per the self-inversion card's own defensibility note, which makes it an easy item to deprioritize against anything with direct customer-visible value. There is a real risk of "benchmark theatre" (the capability matrix's own named risk for CAP-78) — a harness that runs but measures the wrong thing, or whose thresholds are set to always pass, provides false confidence that is worse than no harness at all.

## Reversibility

High at the infrastructure level (a harness is additive and does not change production code paths by itself) but low in terms of organizational cost if skipped: every other ADR's "falsifiable benchmark" field becomes an unverifiable aspiration without it, and retrofitting reproducibility metadata after benchmarks have already been run informally is far more expensive than building it in from the start.
