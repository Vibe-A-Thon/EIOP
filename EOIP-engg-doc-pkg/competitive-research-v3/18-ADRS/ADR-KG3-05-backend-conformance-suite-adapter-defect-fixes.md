# ADR-KG3-05: Backend Conformance Suite and Named Adapter-Defect Fixes

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-26 |
| Supersedes | The 2026-10-19 placeholder of this file (same path, different topic) |
| Based on | `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-05 |
| Gap | GAP-01 (`07-GAP-REGISTER.md`, forced P0, High severity) |
| Capability | CAP-01 (Property-graph storage and indexing) |

## Context

GAP-01 is proven by static code reading, not yet by a live run (`U-01` remains open in both baseline documents). Three concrete adapter defects were found: the JanusGraph adapter writes `p_`-prefixed property keys on write but reads them back unprefixed, which will silently break lookups that are not keyed by the canonical ID (`adapters/janusgraph.py`); the Neptune adapter has no SigV4/IAM signing path — confirmed negatively at HEAD (`U-03` resolved negative, no `sigv4|iam|botocore|aws` reference anywhere in the adapter, `boto3` not installed) — and filters edge labels *after* applying `LIMIT`, which silently truncates results rather than erroring; the HugeGraph adapter forces a Groovy closure in its traversal templates, which will not execute against a gremlin-lang-only backend once TinkerPop's 4.0 direction (currently beta, per C12-tinkerpop) becomes the deployment target. None of the five backend adapters (HugeGraph, Neo4j, Neptune, JanusGraph, Fuseki/GraphDB) has ever been exercised against a live engine in this research programme's runs — `tests/runtime_hubble` exists but was not executed, and the Fuseki/GraphDB live test cases exist and skip without environment variables set.

## Options considered

1. **Quick integration** — patch the three named defects directly: fix the JanusGraph key-prefix mismatch, add Neptune SigV4 signing (or document it as unsupported if not implemented), reorder the Neptune label filter before the `LIMIT`, and replace the HugeGraph Groovy closure with a parameterised template.
2. **Pragmatic native enhancement** — stand up a conformance suite (BM-01) that runs an identical read/write/traversal workload against live HugeGraph, Neo4j, Neptune and JanusGraph containers in CI, so regressions of this class are caught before release rather than found by static reading months later.
3. **Long-term** — the typed query-IR compiler (GAP-04, ADR-KG3-12) removes an entire class of per-backend string-building defects by construction, because no adapter builds a traversal by string interpolation once QueryPlan→AST→dialect is the only path to any backend.

## Options rejected and why

Relying on option 3 alone, without the near-term patches, is rejected: the query-IR compiler is an 8–12 week (L-effort) structural change, and the three named defects are live risks today in any deployment running against JanusGraph or Neptune right now. Waiting for the structural fix to also fix today's known bugs is not acceptable given the severity (silent truncation and silent lookup failures are worse than loud failures).

## Decision

Adopt all three, sequenced: (1) immediately — patch the three named defects as scoped, independent fixes; (2) as a standing CI gate — BM-01 runs against live containers of every backend before any backend-facing release, so the next JanusGraph-class defect is caught by a test, not by a research pass; (3) as the structural fix that this architecture is already committed to for GAP-04/05 (ADR-KG3-12, ADR-KG3-08) and that incidentally closes this class of defect for free once it ships.

## Consequences

**Positive:** closes a High-severity forced P0 (score 3.85). Converts three specific, named defects from "found by one static-reading pass" to "caught automatically on every future change" — this is the difference between a one-time fix and a durable guarantee. A passing, published cross-backend conformance suite is a stronger and more independently verifiable claim than any single competitor's single-backend guarantee (none of the researched backends — HugeGraph, Neo4j, Neptune, JanusGraph — publishes a cross-engine conformance result against the others).

**Negative:** requires live container access in CI, which this research run did not have (U-01 is explicitly still open) — building BM-01 is itself a non-trivial infrastructure investment (per CAP-78/GAP-43, the evaluation-harness gap), not a quick script. Defect severity in practice depends on live behaviour that remains unmeasured until BM-01 actually runs; the three named defects are proven by code reading, and their blast radius (how many existing deployments are actually affected, e.g. by non-canonical-ID JanusGraph lookups) is not yet known.

## Reversibility

High for the three point fixes (each is an isolated, independently revertible patch). The CI conformance gate is operationally cheap to keep once built. The dependency on GAP-04's structural fix is tracked, not blocking — this ADR's near-term fixes do not wait on ADR-KG3-12 to ship.
