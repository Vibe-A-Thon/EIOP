# ADR-KG3-06: Epistemic Planes as a Storage-Level Guarantee

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-26 |
| Supersedes | The 2026-10-19 placeholder of this file (same path, different topic) |
| Based on | `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-06 |
| Gap | GAP-07 (`07-GAP-REGISTER.md`, forced P0, High severity) |
| Capability | CAP-43 (Epistemic separation: observed/inferred/predicted/approved) |

## Context

`ai/boundary.py` implements PROPOSED-until-promoted semantics (BL-40, "Implemented (contract)") and the capability matrix marks CAP-43 a differentiator candidate precisely because no researched competitor provides epistemic separation natively (`06-MASTER-CAPABILITY-MATRIX.md` §2). But the guarantee lives entirely in application code: the boundary module enforces the rule within its own call path, and nothing at the storage layer stops a write that bypasses `ai/boundary.py` from landing as an "observed" fact on any backend. This is the same structural pattern as GAP-02 and GAP-03 — a real mechanism that is optional rather than mandatory — applied to a different guarantee. It also interacts directly with GAP-34 (agent memory lacks the same fields): INV-SELF-09 names GAP-07 as a dependency, because memory records need the same observed/inferred/predicted distinction and inherit the fix built here.

## Options considered

1. **Quick integration** — add a required `epistemic_state` property enforced by `validation/gate.py` (the existing mutation-gateway validator, BL-28) so no mutation can omit it.
2. **Pragmatic native enhancement** — per-backend namespace or label separation (distinct vertex labels, or a graph partition) for PROPOSED vs. CORROBORATED facts, so the distinction is visible and queryable at the storage layer, not just a property value that a careless query could ignore.
3. **Long-term** — a promotion workflow with an audit trail and reviewer sign-off, feeding the existing `provenance/warrant_composition.py` so promotion from PROPOSED to CORROBORATED is itself an evidenced, attributable act.

## Options rejected and why

Relying on option 1 alone (a required property with no structural separation) is rejected as the end state, because a required property is still just a column value — any query that forgets to filter on it (exactly the GAP-02 failure mode) would mix planes silently. The whole point of calling this a "storage-level guarantee" rather than "a contract" is that the separation must survive a careless caller, not merely penalize one that forgot a check.

## Decision

Adopt option 1 immediately as the first, mandatory gate (the mutation gateway refuses any write lacking `epistemic_state`), with options 2 and 3 as the target architecture that actually delivers the storage-level guarantee: per-backend label/namespace separation so PROPOSED and CORROBORATED facts are structurally distinguishable even to a query that forgets to filter, and a promotion workflow that produces an auditable trail rather than a silent property update.

## Consequences

**Positive:** closes a High-severity forced P0 (score 3.8) and converts CAP-43 from "a contract that could be proven wrong by one missed check" to a storage-level property verifiable by BM-15 (attempt to write an "approved" fact through every ingestion path without going through promotion — all attempts must fail). Supports J8 (predictions without fact contamination) directly: GNN/link-prediction output (CAP-64, EXPERIMENT per GAP-38) has an actual quarantine to land in rather than a convention to respect.

**Negative:** per-backend label/namespace separation is not free — it changes the schema shape on every backend (HugeGraph schema, Neo4j labels, Neptune's schemaless model needs an equivalent convention, RDF named graphs) and must be done consistently or the "storage-level" claim becomes backend-dependent, which undercuts the point. Leakage between planes remains a named risk (CAP-43's own risk column) even after this fix, if the promotion workflow itself has a bug.

## Reversibility

Medium. The required-property gate (option 1) is cheap to add and remove. The per-backend label/namespace separation (option 2) is a schema-level change that, once facts exist under the new labelling, is not a config-level revert — reversing it means a data migration back to an undifferentiated label space, which is exactly the state this ADR is designed to leave behind.
