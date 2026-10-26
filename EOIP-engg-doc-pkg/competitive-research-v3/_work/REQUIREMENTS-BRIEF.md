# Requirements and contracts brief — read fully before starting

You write `11-REQUIREMENTS-FINAL.md`, `12-DATA-ONTOLOGY-EVENT-CONTRACTS.md` and `13-API-QUERY-AGENT-SECURITY-CONTRACTS.md` for the KnowGridFlow/EOIP competitive research package. Repository root: `F:\code\EIP\EIOP`. Package: `EOIP-engg-doc-pkg/competitive-research-v3/`.

## Inputs (read in this order)

1. `KNOWLEDGE_GRAPH_COMPETITIVE_RESEARCH_MASTER_PROMPT_v3.md` lines 429–448 (§13 — priority formula, REQ fields, ADR fields) and lines 450–470 (§14, journeys J1–J16 — every requirement should trace to at least one).
2. `07-GAP-REGISTER.md` in full — this is your primary source. Every gap row already has a priority, score inputs, root cause, options, dependencies, tests (BM-IDs) and effort. **One or more REQ-IDs per gap; never invent a requirement with no gap, strength or inversion behind it.**
3. `06-MASTER-CAPABILITY-MATRIX.md` for the CAP-ID each gap maps to (user problem, backend applicability).
4. `08-STRENGTH-ADOPTION-REGISTER.md` §1 and `09-CON-TO-PRO-INVERSION-REGISTER.md` §3 (self-inversion cards) for design detail behind the P0 requirements.
5. `10-TARGET-REFERENCE-ARCHITECTURE.md` and `18-ADRS/*.md` if they exist yet (check `04-COMPETITOR-DEEP-DIVES` directory's sibling folders for freshness; if not yet written, proceed from the gap register and matrix alone — do not wait).
6. `01-SYSTEM-BASELINE.md` / `01a-BASELINE-DELTA-HEAD.md` for existing module names (owning module field) and current contract files under `packages/eoip/contracts/` and `schemas/*.schema.json` (skim file names only, don't re-derive the baseline).

Note: a prior, non-evidence-based pass on 2026-10-19 wrote placeholder files at these three paths with no GAP/CLAIM traceability (e.g. invented requirements with no source). **Overwrite each completely** (Read then Write); do not reuse their content.

## What to write

### `11-REQUIREMENTS-FINAL.md` (one row per requirement, expect 55–75 requirements; target 5,000–8,000 words)

For every gap in `07-GAP-REGISTER.md` (46 gaps), derive 1–2 requirements (split a gap into multiple requirements only when it has genuinely separable deliverables, e.g. GAP-02 → one REQ for write-path ACL tagging, one for read-path enforcement). Also derive requirements for undisputed STR-ID adoptions in the §1 shortlist that are not already covered by a gap (e.g. STR-rebac-01 consistency tokens). Structure:

1. A short intro restating the priority formula and P0/P1/P2/P3 definitions (Master Prompt §13), and that scores/priorities are inherited from the gap register, not recomputed.
2. One table per priority tier (P0, P1, P2, P3), columns: `REQ-ID | Title | Use case / value | Source (GAP/STR/INV-ID) | Functional behaviour (1-2 sentences) | NFRs | Owning module | Backend applicability | Dependencies (REQ-IDs) | Tests (BM-ID) | Effort | Release phase | Out of scope`.
3. For the 11 P0 requirements specifically, expand each into its full field set (data contracts touched, API/UI surface, threat considerations, observability) in a short subsection below the table — these are the ones implementers will read first.
4. A traceability footnote: every REQ-ID must appear at least once in the P0–P3 tables; count and state total requirements, and confirm every GAP-ID from the register appears in at least one REQ's Source column (list any gap you deliberately did not turn into a requirement, with a one-line reason — e.g. already fully speced in an ADR).
5. Release phases: align with Master Prompt phases - P0 reqs = "Phase 0 (foundation/correctness)", P1 = "Phase 1", P2 = "Phase 2", P3 = "Research track" (not phase-gated).

REQ-ID format: `REQ-<area>-NN` where area is a short 3-4 letter code (SEC, TEN, ING, QRY, GOV, MEM, OPS, VIZ, ML, STD, etc. — pick sensibly per gap's dimension).

### `12-DATA-ONTOLOGY-EVENT-CONTRACTS.md` (3,000–5,000 words)

Canonical types, identity, temporal, provenance, inference, versioning and tenancy schemas needed by the P0/P1 requirements. For each: field list (name: type, required/optional, one-line meaning), which REQ-IDs need it, which existing EOIP contract it extends/replaces (cite `packages/eoip/contracts/*.py` or `schemas/*.schema.json` filenames from the baseline if you know them, else mark NEW). Cover at minimum: ACL-principal-bearing fact/chunk/edge envelope (GAP-02), tenant-scoped envelope (GAP-03), epistemic-state envelope (GAP-07), agent-memory record with ACL/tenant/evidence/validity (GAP-34), typed mutation-gateway constraint schema (GAP-12), QueryPlan/AST node schema (GAP-04/05). Use JSON-Schema-like pseudocode in fenced blocks, not full JSON Schema files.

### `13-API-QUERY-AGENT-SECURITY-CONTRACTS.md` (3,000–5,000 words)

Typed query AST/IR, backend compilers, parameterized query gateway, REST/MCP, NL-query and suggestion contracts, policy hooks, error contracts. Structure around: (1) the QueryPlan→AST→{gremlin-lang, openCypher, SPARQL} compiler interface (GAP-04/05) with per-backend compiler contract; (2) the MCP tool contract with OAuth 2.1 resource-server auth and per-tool ACL/annotation schema (GAP-09); (3) the AuthzPort interface (check/expand/list-objects pattern from STR-rebac-01) used by both retrieval and MCP; (4) error/abstention contract for NL query and GraphRAG (GAP-35, "typed plan candidates not raw queries"); (5) policy-hook points (where ACL/tenant checks are mandatory, not optional, per the self-inversion cards).

## Rules

- Every requirement traces to a GAP-ID (and through it to CAP/STR/INV-IDs); never fabricate a requirement.
- Respect backend neutrality: a requirement's "backend applicability" column must say native/emulated/unavailable per backend, consistent with the matrix.
- Do not re-decide priorities; inherit them from `07-GAP-REGISTER.md` exactly (including the three coordinator overrides noted there).
- Never delete, move or rename files; never run git commands that change state. Write only the three named files.

## Final reply (≤200 words)

Requirement count per priority tier, the P0 requirement IDs in full, any gap you did not convert to a requirement and why, and any inconsistency found between the gap register and the matrix while writing.
