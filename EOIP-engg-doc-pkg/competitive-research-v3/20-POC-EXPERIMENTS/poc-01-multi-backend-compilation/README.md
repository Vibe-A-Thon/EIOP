# POC-01: Multi-Backend QueryPlan Compilation (specification — not executed)

| Field | Value |
|---|---|
| Status | **SPECIFICATION ONLY.** No compiler has been built or run against this spec. Nothing here passed. |
| Supersedes | A 2026-10-19 version of this file hardcoded three fixed output strings that ignored their input `plan` argument entirely, then printed `POC-01 PASS: All 3 dialects compiled deterministically.` regardless of input. That is a fabricated pass and is removed. See `run_poc.py` in this folder for the corrected, honest stub. |
| Traces to | `GAP-04` (portable query IR not on the production path), `GAP-05` (string-built Gremlin), `GAP-12` (no typed constraint layer), `ADR-KG3-12` (typed multi-backend query-IR compiler, `18-ADRS/ADR-KG3-12-typed-multi-backend-query-ir-compiler.md`), `ADR-KG3-08` (parameterised query IR, retire string-built Gremlin) |
| Current EOIP state | `packages/eoip/query/ast_compiler.py` exists at HEAD but is not on the production path (`01a-BASELINE-DELTA-HEAD.md` BL-09). This POC does not read or wrap that module; it specifies what a real compiler must satisfy before any claim of "compiles deterministically" can be made. |

## Objective

Specify a reproducible experiment proving (or falsifying) that a single structured `QueryPlan` compiles **deterministically, correctly and safely** into:

1. An Apache HugeGraph Gremlin payload (parameterised gremlin-lang, not a hand-built script — see `INV-SELF-08` in `09-CON-TO-PRO-INVERSION-REGISTER.md`).
2. A Neo4j Cypher 25 query string with bound parameters (never string-interpolated values).
3. A W3C SPARQL 1.1 query (only if the RDF sidecar, `CAP-02`, is enabled for that tenant).

"Compiles correctly" means: the same `QueryPlan` produces an equivalent answer set on every backend that supports the intent, verified by running the compiled query against a live instance of each backend and comparing results — not by inspecting the generated string.

## What would make this real (not yet done)

1. A `QueryPlan` fixture set covering every intent the typed AST compiler claims to support, including at least one adversarial case (an attacker-controlled property key or label value, per `GAP-05`).
2. Live HugeGraph, Neo4j and (optionally) Fuseki/GraphDB containers, each pre-loaded with the same fixture graph.
3. The actual compiler under test (`packages/eoip/query/ast_compiler.py` or its successor once mounted) — not a mock.
4. A result-equivalence check per fixture: same vertex/edge set returned (ignoring backend-specific identifiers), within a documented tolerance for intentional semantic differences (e.g. multigraph handling).
5. An injection check: the adversarial fixture must not alter the query's structure on any backend.

## Pass/fail condition (once actually run)

PASS requires all of: (a) every fixture compiles without error on every applicable backend; (b) result sets match within the documented tolerance; (c) the adversarial fixture produces no structural change in any compiled query. Partial success is reported as PARTIAL with the specific fixtures that failed, never rounded up to PASS.

## How to run (once the dependencies above exist)

```bash
python run_poc.py
```

`run_poc.py` in this folder is currently a stub: it prints the specification above and exits without claiming a result, because none of items 1–5 exist yet in an executable form. See `15-VALIDATION-BENCHMARK-PLAN.md` BM-01 for the full conformance-suite specification this POC is a minimal slice of.
