# ADR-KG3-12: Typed Multi-Backend Query-IR Compiler

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-26 |
| Supersedes | The 2026-10-19 placeholder of this file (same path, different topic) |
| Based on | `06-MASTER-CAPABILITY-MATRIX.md` CAP-20; not a self-inversion card — this is the structural decision the other eleven ADRs (notably ADR-KG3-05 and ADR-KG3-08) depend on, per the brief's explicit instruction to add one ADR here beyond the eleven self-inversion cards |
| Gap | GAP-04 (`07-GAP-REGISTER.md`, P1 by score but architecturally central; ties to GAP-05, forced P0) |
| Capability | CAP-20 (Portable query IR and translation) |

## Context

`contracts/query_plan.py` (BL-08, Implemented) and `query/executor.py` compile a typed, bounded `QueryPlan` to named templates — this is EOIP's actual production query path today, and it is real, policy-checked and tested. Separately, `query/ast_compiler.py` (BL-09) implements a genuinely typed AST compiler with `compile_cypher`/`compile_gremlin`/`compile_sparql` methods, typed filter/match/projection/order nodes and variable-length path support — and its tests pass. But BL-09's own evidence note is unambiguous: "nothing executes the Cypher/Gremlin output on Neo4j/HugeGraph; no caller in `apps/` or `packages/` outside `query/`." The compiler produces correct query text that no deployed code path ever sends to a backend. Meanwhile, production traversal happens by walking bounded templates in Python (BL-08), and two adapters build backend queries by direct string interpolation (`adapters/janusgraph.py`, `graph/hugegraph.py` — GAP-05, ADR-KG3-08). CAP-20 is explicitly flagged in the capability matrix as a "competitive deficit → differentiator": no researched competitor offers a portable query IR across Gremlin, Cypher and SPARQL natively (CAP-20's evidence row: "none native — assessed in 10 deep dives"), which means building this well is not just an internal fix, it is a claim no competitor can currently match.

## Options considered

1. **Narrow fix** — parameterise only the two string-building call sites named in GAP-05, leaving `QueryPlan`→bounded-templates as the permanent production path and `ast_compiler` as a permanently unused library.
2. **Mount the existing compiler as an alternative path** — wire `ast_compiler`'s output into each adapter as a second, opt-in execution route, used for specific query shapes the template system cannot express, while keeping the template system as the default.
3. **Make QueryPlan→AST→{gremlin-lang, openCypher, SPARQL} the only production path**, with a conformance suite (shared with ADR-KG3-05's BM-01) verifying semantic parity per backend, and retire the Python-template traversal and the two string-building adapters once the compiler path is proven.

## Options rejected and why

Option 1 is rejected as a final state (though its scoped patches are adopted immediately under ADR-KG3-08) because it leaves the compiler — real, tested, 8–12 weeks of built value — permanently unused, and leaves backend-native query optimisation permanently unavailable to the production path (the baseline's own assessment, §6 point 1 of `01-SYSTEM-BASELINE.md`, already names this as the core trade-off: "portability today means every backend implements the same CRUD/neighbourhood protocol, and traversal happens in Python... that gives up each engine's optimiser for deep multi-hop and analytics"). Option 2 is rejected as a permanent end state because running two parallel query-execution paths (templates and compiled AST) doubles the conformance-testing burden and creates exactly the kind of "mechanism exists but is optional" pattern that GAP-02, GAP-03 and GAP-07 show is unreliable — a query shape handled only by the legacy path would silently miss whatever guarantees the compiled path enforces (e.g., the parameterisation that closes GAP-05).

## Decision

Adopt option 3 as the target architecture, with option 2 as the necessary transition state (not a destination) during rollout — new query shapes and new backends are added via the compiler from day one of this work, while the existing bounded-template path is migrated incrementally and retired once BM-01 (ADR-KG3-05's conformance suite) shows parity. This is the structural decision every other backend-facing ADR in this set assumes: ADR-KG3-05's adapter-defect fixes are superseded by construction once no adapter builds a query string; ADR-KG3-08's Gremlin injection fix is the compiler's security side-effect, not a separate initiative.

## Consequences

**Positive:** removes the GAP-05 injection surface by construction rather than by patching known call sites one at a time (ADR-KG3-08 depends on this). Delivers on CAP-20's differentiator claim — "same question, any backend, safely" — which is independently a strong competitive position per the capability matrix's own "Competitive deficit → differentiator" classification. Converts BL-09's two engineering quarters of unused library code into the platform's actual production query path.

**Negative:** this is the largest single piece of engineering work in this architecture (L-effort, 8–12 weeks per CAP-20's own estimate). The named risk is real and structural: compiling to a lowest-common-denominator IR can produce lowest-common-denominator semantics, where a query that would run efficiently using one backend's native path degrades once forced through a shared AST. Backend-specific push-down optimisation (CAP-18) must be designed alongside this compiler, not treated as solved by it.

## Reversibility

Low once in production. The template-based path (BL-08) and the compiled path (BL-09) can coexist during migration (option 2), which gives a safe rollback window per query shape as it migrates. But once the template path is fully retired and adapters no longer accept hand-built queries, reverting would mean rebuilding the retired path from scratch — this is the one ADR in the full set of twelve where the end state is explicitly a one-way door, matching its status as "the structural decision the others depend on."
