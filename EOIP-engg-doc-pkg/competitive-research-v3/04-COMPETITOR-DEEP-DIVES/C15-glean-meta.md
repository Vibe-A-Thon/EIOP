# C15 — Glean (Meta's open-source code-fact system)

| Field | Value |
|---|---|
| Registry ID | T-C15-glean-meta |
| Tier | B — OSS code fact store; name collision with Glean enterprise search (C07-glean-enterprise.md) resolved |
| Versions examined | `facebookincubator/Glean` `main` (pushed 2026-10-25); CHANGELOG.md top entry 0.2.0.0 undated; no GitHub release or tag returned by the API |
| Verified on | 2026-10-26 (brief date 2026-10-18; fetches ran 2026-10-26) |
| Worker | V28 (W27 scope) |

## 1. Identity, current status, tier, and sources

| Item | Finding | Claim |
|---|---|---|
| Identity | System for collecting, deriving and querying facts about source code (symbols, types, cross-references, call and type hierarchies); GitHub org `facebookincubator`; site glean.software | [CLAIM-glean-meta-01] |
| Collision | Distinct from Glean (glean.com) enterprise search/work graph, researched in C07. The placeholder `C15-glean-code-intelligence.md` is not touched | [CLAIM-glean-meta-01] |
| Status | Active: last push 2026-10-25, ~5,091 commits, 1.4k stars; no tagged releases, CHANGELOG has only 0.1.0.0 and 0.2.0.0 with placeholder/no dates | [CLAIM-glean-meta-02] |
| Licence | BSD (LICENSE headed "BSD License"; GitHub reports NOASSERTION; exact clause count not read) | [CLAIM-glean-meta-03] |
| Language support | "Full support": C/C++, Hack, Haskell, JS/Flow, Python; Rust, Go, TypeScript, Java, .NET via SCIP/LSIF ingestion; further indexers (Java, Kotlin, Swift, Bazel...) "exist internally", not open-sourced | [CLAIM-glean-meta-01] |

## 2. Primary problem, target workloads, example workflows

Problem: precise, schema-defined code facts for a very large monorepo with incremental updates. Workloads: IDE navigation (Glass symbol server, Glean-based LSP server), xref, impact and dead-code analysis. EOIP J1/J10: index at commit; Angle query symbol to referencing files; join to Jira/PR nodes by file/symbol id.

## 3. Feature inventory

| Feature | Status | Claim |
|---|---|---|
| Fact store (RocksDB), immutable typed facts forming a DAG, dedup | present | [CLAIM-glean-meta-04] |
| User-defined schemas | present | [CLAIM-glean-meta-04] |
| Angle query language (Datalog-like, non-recursive) | present | [CLAIM-glean-meta-04] |
| Derived facts via Angle rules | present | [CLAIM-glean-meta-04] |
| Incremental indexing: ownership units, slices, stacked DBs | present; derived-fact gap in stacked DBs "not implemented yet" | [CLAIM-glean-meta-05] |
| Server (Thrift), shell, CLI | present | [CLAIM-glean-meta-04] |
| Glass symbol server / LSP server | present | [CLAIM-glean-meta-04] |
| SCIP/LSIF import | partial (listed per language) | [CLAIM-glean-meta-01] |
| UI | absent (shell only) | [CLAIM-glean-meta-04] |
| Auth, multi-tenancy, ACLs | NOT PUBLICLY VERIFIED | |

## 4. Architecture diagram

```
 indexers (flow/clang/hack/python/scip->glean) --facts batch(JSON/binary + ownership)--> Glean server (Thrift)
                                                                  |  RocksDB DB per repo+rev; stacked DBs for increments
                                  Angle rules -> derived facts <--+--> shell / CLI / Glass symbol server -> LSP clients
```

## 5. Under-the-hood reconstruction

- Data model: predicates defined in schemas; a fact = predicate + key + optional value; facts immutable, deduplicated, referencing other facts (DAG) [CLAIM-glean-meta-04].
- Storage: RocksDB; several databases on disk managed by the server; replicated databases served to many clients [CLAIM-glean-meta-04].
- Incrementality: each fact has an ownership set built from units (strings, e.g. file/module) with `||` and `&&`; a bitmap slice marks visible sets; when fact F (owner A) references B (owner B) F's owner becomes `A||B`, propagated by one reverse pass, O(facts) time and space; derived fact owner = intersection of sources. Stacked DB lets a new layer add owners to lower facts. Coarse units recommended (10-100x fewer sets than facts) [CLAIM-glean-meta-05].
- Query: Angle, Datalog-like, non-recursive; planning internals NOT PUBLICLY VERIFIED.
- Concurrency, transactions, security: NOT PUBLICLY VERIFIED. Caching: ownership pages cached in memory [CLAIM-glean-meta-05].

## 6. Requirements inferred

Per-file ownership tags on facts; hide-and-replace without full re-index; schema-defined derived views.

## 7. Performance and resource model

Docs claim large-scale deployment but give no figures [CLAIM-glean-meta-04]. No benchmark retrieved: NOT PUBLICLY VERIFIED. Failure modes: ownership propagation O(facts) memory; fine-grained units blow up set count; stacked-DB derived-fact visibility gap [CLAIM-glean-meta-05].

## 8. Strengths

| Strength | How to match or exceed |
|---|---|
| Ownership-unit model: exact incremental hide/replace, no dangling references | adopt, keyed by file blob hash |
| Schema-defined derivable facts | CML mapping (BL-33) can describe indexer output |

## 9. Limitations and root causes

| Class | Finding |
|---|---|
| Algorithmic | Angle non-recursive: no transitive closure in-query [CLAIM-glean-meta-04] |
| Operational | Haskell/C++ server; Thrift protocol; no tagged releases or dates, so version pinning is by commit [CLAIM-glean-meta-02] |
| Friction | Best indexers (Java, Kotlin, Swift, Bazel) not open [CLAIM-glean-meta-01]; schema authoring is Glean-specific |
| Governance | Corporate-led repo under `facebookincubator`, CLA required [CLAIM-glean-meta-01] |

## 10. Deployment, licensing, viability

Self-hosted, no cloud dependency stated; air-gap likely (untested). BSD text and any patent grant need legal read (GitHub shows NOASSERTION) [CLAIM-glean-meta-03]. One-node plausible; footprint unmeasured.

## 11. Competitive delta against EOIP baseline

BL-42: EOIP has Python/TS symbols and an incremental indexer with polyglot linking; Glean offers exact ownership-based incrementality and many-language facts. BL-01/BL-23: Glean is a separate store; connect only through governed SourceEvents. BL-18: no source-ACL concept evidenced. See C15-scip-lsif.md and C15-tree-sitter.md for formats and parsers; C15-sourcegraph.md for the UI-bearing alternative.

## 12. Cards

`STR-glean-meta-01 | Glean | ownership-set incrementality | CLAIM-05 | cheap exact re-index for J1 | match | per-file owner ids on code nodes with tombstone on change (BL-25) | edit one file in a 10k-file repo: only its facts replaced, no dangling edges`

INV-glean-meta-01: target Glean main; workload cross-repo dependency closure. Limitation: Angle is non-recursive (proven, CLAIM-04). Root cause: query-language design (hypothesis). Alternative: closure in the graph backend; worse beyond backend capacity. Options: (a) Glean beside EOIP, (b) derived edges in graph, (c) native incremental closure. Selected (b). POC: closure of imports on a 5k-file repo; metric: p95 < backend baseline. Decision: DEFER. Seed hypotheses in Master Prompt §10.5 do not target Glean.

## 13. Decisions

| Capability | Decision |
|---|---|
| CAP-66 precise code graph | REFERENCE pattern; INTEGRATE only via SCIP, not Glean store: DEFER |
| CAP-67 incremental re-index | EXPERIMENT (ownership-unit pattern) |
| CAP-69 digital thread | BUILD in EOIP graph |

## 14. Tests and acceptance

Build offline; index one repo via SCIP; replay a one-file change; accept if no dangling references and cost scales with changed files.

## 15. Risks and open questions

Licence text; per-tenant isolation.

## Appendix A — Dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,9 | Active, BSD, no releases |
| D2 | 2 | Code nav at monorepo scale |
| D3 | 4 | Indexers, server, Glass |
| D4 | 5 | RocksDB facts DAG |
| D5 | 5 | User schemas |
| D6 | 5,9 | Angle, non-recursive |
| D7 | 5 | Derived facts only |
| D8 | 5,7 | Replicated DBs; no txn detail |
| D9 | 5 | Indexer batches |
| D10 | N/A | Not evidenced |
| D11 | 5 | Revision DBs, stacks |
| D12 | N/A | Not in scope |
| D13 | 3 | LSP/Glass only |
| D14 | N/A | Absent |
| D15 | N/A | Schemas only |
| D16 | 3 | Shell/CLI |
| D17 | 3,9 | Thrift, schemas |
| D18 | 3 | NOT PUBLICLY VERIFIED |
| D19 | N/A | Not evidenced |
| D20 | 7 | No figures |
| D21 | 10 | BSD, OSS only |
| D22 | 3,11 | SCIP ingest |
| D23 | N/A | None checked |
| D24 | 15 | Docs-level evidence only |

## Appendix B — Capability mapping

| CAP | Technology | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-66 | native | 01,04 | BL-42 Partial | EXPERIMENT | P2 |
| CAP-67 | native | 05 | BL-42 Implemented | EXPERIMENT | P2 |
| CAP-69 | partial | 04 | BL-42 Partial | BUILD | P1 |
| CAP-50 | likely | 04 | BL-45 | REUSE | P3 |

## Appendix C — Evidence records

| CLAIM | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| 01 | Glean main 2026-10-26 | purpose, language list, internal indexers unreleased | Officially documented | GitHub README https://github.com/facebookincubator/Glean | n/a / 2026-10-26 | 0.85 | none |
| 02 | same | pushed 2026-10-25; no releases/tags; CHANGELOG 0.2.0.0 undated | Observed | GitHub API; CHANGELOG | 2026-10-26 | 0.8 | none |
| 03 | same | LICENSE "BSD License", Facebook copyright | Observed | https://raw.githubusercontent.com/facebookincubator/Glean/main/LICENSE | 2026-10-26 | 0.7 (clauses unread) | API NOASSERTION |
| 04 | same | RocksDB, immutable DAG facts, Angle non-recursive, Thrift server, Glass/LSP | Officially documented | https://glean.software/docs/introduction | 2026-10-26 | 0.85 | none |
| 05 | same | ownership units, slices, O(facts) propagation, stacked-DB gap | Officially documented | https://glean.software/docs/implementation/incrementality | 2026-10-26 | 0.85 | none |

## Appendix D — Assumptions

Air-gap inferred; BSD assumed permissive.
