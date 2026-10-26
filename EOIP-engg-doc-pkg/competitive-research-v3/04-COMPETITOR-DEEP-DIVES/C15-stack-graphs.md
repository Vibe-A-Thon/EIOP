# C15 — GitHub stack-graphs

| Field | Value |
|---|---|
| Registry ID | T-C15-stack-graphs |
| Tier | B — incremental, zero-config name resolution; archived reference design |
| Versions examined | `tree-sitter-stack-graphs` v0.10.0 (2024-12-13, last release seen); repo archived 2025-09-09 (last push 2025-09-09) |
| Verified on | 2026-10-26 (brief date 2026-10-18) |
| Worker | V28 (W27 scope) |

## 1. Identity, current status, tier, and sources

| Item | Finding | Claim |
|---|---|---|
| Identity | Rust implementation of stack graphs (name-resolution framework from scope-graph research at TU Delft); crates `stack-graphs` and `tree-sitter-stack-graphs`; used for GitHub's precise code navigation | [CLAIM-stack-graphs-01][CLAIM-stack-graphs-02] |
| Status | ARCHIVED, read-only, "archived by the owner on Sep 9, 2025"; banner: "no longer supported or updated by GitHub... we recommend you fork it" | [CLAIM-stack-graphs-01] |
| Successor/forks | None found in this run: UNVERIFIED; no maintained fork identified | [CLAIM-stack-graphs-03] |
| Licence | Apache-2.0 OR MIT (dual, README); API reports Apache-2.0 | [CLAIM-stack-graphs-01] |
| Languages in repo | Java, JavaScript, Python, TypeScript (language dirs) | [CLAIM-stack-graphs-04] |
| Whether GitHub.com still uses it | NOT PUBLICLY VERIFIED | |

## 2. Primary problem, workloads, workflows

Jump-to-definition and find-references on every commit, for any repo, without build setup, CI, or per-repo config. Workflow: on push, analyse changed files only and store each file's graph; at query time stitch paths from the reference to definitions [CLAIM-stack-graphs-02].

## 3. Feature inventory

| Feature | Status | Claim |
|---|---|---|
| Per-file graph construction, incremental by file | present | [CLAIM-stack-graphs-02] |
| Query-time path stitching with symbol stack | present | [CLAIM-stack-graphs-02] |
| Graph construction language mapping tree-sitter matches to nodes/edges | present | [CLAIM-stack-graphs-02] |
| CLI (`tree-sitter-stack-graphs` index/query/test, recalled) | present, UNVERIFIED exact commands | |
| Languages | 4 only | [CLAIM-stack-graphs-04] |
| Data-flow, generics, inheritance | limited/open per author | [CLAIM-stack-graphs-02] |
| Persistent store | SQLite in CLI (recalled, UNVERIFIED) | |

## 4. Architecture diagram

```
 file --tree-sitter parse--> syntax tree --stack-graph DSL rules--> per-file stack graph --> store (per blob)
 query: reference node -> merge graphs of commit -> path stitching (push symbol at ref, pop at def; precedence = shadowing) -> definitions
```

## 5. Under-the-hood reconstruction

- Data model: nodes (scope, push-symbol, pop-symbol, jump/drop) and edges with precedence; one graph per file with exported/imported boundary nodes (reasoned from the blog and scope-graph literature; node-type names recalled, UNVERIFIED) [CLAIM-stack-graphs-02].
- Indexing: files analysed in isolation, so a commit re-indexes only changed files [CLAIM-stack-graphs-02].
- Query: path search from a reference node to definitions subject to a symbol stack; shadowing via edge precedence; Rust top-level conflicts via shared node [CLAIM-stack-graphs-02]. Author notes a full path search per lookup may be wasteful and asks about more precomputation [CLAIM-stack-graphs-02].
- Concurrency/transactions/partitioning: per-file independence gives trivially parallel indexing (reasoned). Caching, security: NOT PUBLICLY VERIFIED.
- Reasoning: none beyond name binding.

Pseudocode (hypothesis, from description): `defs(ref) = { d | path(ref -> d) valid under stack discipline, highest precedence per shadowing }`.

## 6. Requirements inferred

Per-file deterministic graph from syntax alone; rules per language in a DSL; stitched graphs fit memory per query.

## 7. Performance and resource model

Blog describes the approach; no benchmark numbers retrieved. NOT PUBLICLY VERIFIED. Failure modes: syntax-only resolution cannot see types, generics, macros or build-config effects; each language needs hand-authored rules; four languages only [CLAIM-stack-graphs-02][CLAIM-stack-graphs-04].

## 8. Strengths

| Strength | Match or exceed |
|---|---|
| Per-file incrementality without a build | adopt the invariant "file blob hash is the unit of indexing" in BL-42 |
| Zero-config on arbitrary repos | EXPERIMENT as fallback when SCIP indexers cannot build |
| Dual Apache-2.0/MIT, Rust library | REFERENCE; do not depend (archived) |

## 9. Limitations

| Class | Finding | Claim |
|---|---|---|
| Maintenance | Archived 2025-09-09; no named successor | [CLAIM-stack-graphs-01][CLAIM-stack-graphs-03] |
| Algorithmic | Syntax-level resolution; dataflow/generics open | [CLAIM-stack-graphs-02] |
| Friction | Hand-written rules per language | [CLAIM-stack-graphs-02] |
| Coverage | 4 languages (Java, JS, Python, TS) | [CLAIM-stack-graphs-04] |

## 10. Deployment, licensing, redistribution

Library/CLI, fully local, air-gap yes. Apache-2.0 or MIT: redistribution-safe (no legal trigger beyond normal notice duties). Operational risk is maintenance: any use means owning a fork of an archived Rust codebase.

## 11. Competitive delta against EOIP baseline

BL-42 uses tree-sitter for Python/TS symbols and an incremental indexer, but no cross-file name resolution (polyglot_linker exists for linking, depth unverified). stack-graphs offers cross-file resolution without builds, the middle tier between tree-sitter (C15-tree-sitter.md) and compiler-grade SCIP (C15-scip-lsif.md). Sourcegraph (C15-sourcegraph.md) takes the SCIP route; stack-graphs' own origin was GitHub.

## 12. Cards

`STR-stack-graphs-01 | stack-graphs | build-free cross-file resolution, per-file incremental | CLAIM-02 | J1 exact function impact on repos with no build | match | per-file resolution table (symbol, scope, imports) keyed by blob hash, stitched at query | on 5 Python/TS repos, definition resolution agreement vs SCIP >= target set after baseline run`

INV-stack-graphs-01: target archived 2025-09 repo; workload production dependence. Limitation: archived (proven, CLAIM-01). Root cause: maturity/governance. Alternative: implement a minimal scope-graph resolver in Python for the two BL-42 languages, or use SCIP; alternative worse for languages needing types. Options: (a) fork and maintain, (b) native import-resolution layer over tree-sitter, (c) SCIP-first with tree-sitter fallback. Selected (c) with (b) as experiment. POC: resolution agreement with SCIP on fixtures; cost: engineer-weeks unmeasured. Decision: EXPERIMENT (b); REJECT (a). Seed hypotheses in §10.5 do not target stack-graphs.

## 13. Decisions

| Capability | Decision |
|---|---|
| CAP-66 build-free name resolution | EXPERIMENT (native, pattern only) |
| CAP-67 per-blob incrementality | BUILD |
| Library dependency | REJECT (archived) |

## 14. Tests and acceptance

Fixture repos for shadowing, re-exports, wildcard imports; compare to SCIP; touch one file and verify only its table rebuilds and no stale cross-file edges remain (tombstones, BL-25).

## 15. Risks and open questions

Hidden maintained forks; whether GitHub.com still depends on it; ceiling of syntax-only resolution on dynamic languages.

## Appendix A — Dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Archived 2025-09-09, dual licence |
| D2 | 2 | Code navigation |
| D3 | 4 | Parse, DSL, stitch |
| D4 | 5 | Per-file graphs |
| D5 | 5 | Scope graph |
| D6 | 5 | Path stitching |
| D7 | 5 | None |
| D8 | 5 | File-parallel |
| D9 | 2 | Push-time index |
| D10 | N/A | None |
| D11 | 2 | Per commit |
| D12 | N/A | None |
| D13 | N/A | None |
| D14 | N/A | Absent |
| D15 | N/A | None |
| D16 | N/A | GitHub UI only |
| D17 | 3 | DSL, crates |
| D18 | N/A | Not described |
| D19 | N/A | None |
| D20 | 7 | No figures |
| D21 | 10 | Permissive |
| D22 | N/A | None |
| D23 | N/A | Not checked |
| D24 | 15 | Blog plus repo |

## Appendix B — Capability mapping

| CAP | Technology | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-66 | partial | 02 | BL-42 Partial | EXPERIMENT | P2 |
| CAP-67 | native | 02 | BL-42 Implemented | BUILD | P2 |
| CAP-69 | absent | 02 | BL-42 | DEFER | P3 |

## Appendix C — Evidence records

| CLAIM | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| 01 | repo 2026-10-26 | archived 2025-09-09; unsupported; Apache-2.0/MIT; crates | Officially documented | https://github.com/github/stack-graphs | 2025-09-09 / 2026-10-26 | 0.9 | API lists Apache-2.0 only |
| 02 | GitHub blog | per-file incremental, path stitching, zero config, tree-sitter, open issues | Officially documented | https://github.blog/open-source/introducing-stack-graphs/ | n/a / 2026-10-26 | 0.85 | none |
| 03 | search 2026-10-26 | no successor or fork named | Reasoned inference | web search | 2026-10-26 | 0.4 | absence of evidence only |
| 04 | repo tree | language dirs java, javascript, python, typescript | Observed | https://github.com/github/stack-graphs/tree/main/languages | 2026-10-26 | 0.9 | none |

## Appendix D — Assumptions

Last release v0.10.0 (2024-12-13) taken from API release list on the first check; node-type names and CLI storage recalled, flagged UNVERIFIED.
