# C13 — Dolt

| Field | Value |
|---|---|
| Registry ID | T-C13-dolt |
| Tier | B (Git-for-data reference) |
| Versions examined | Dolt 2.6.0 (release page "23 Oct", year not shown, 2026 inferred); Doltgres (Postgres flavour) Beta |
| Verified on | 2026-10-26 |
| Worker | V26 |

## 1. Identity, status, sources
Dolt (DoltHub Inc.): SQL database with Git semantics (branch, merge, push/pull, diff), MySQL-compatible server `dolt sql-server`; Apache-2.0 [CLAIM-dolt-01]. Doltgres is a separate Postgres-flavoured project, "now in Beta" [CLAIM-dolt-01]. Active (release within 3 days of verification). Sources: GitHub dolthub/dolt, releases, DoltHub docs.

## 2. Problem, workloads
Versioned tabular data: collaborative datasets, reference data, ML training sets, config-as-data, test fixtures. Example: branch production reference data, run a migration, diff, merge or discard.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Commit, branch, merge, push/pull, Git-style CLI [CLAIM-dolt-01] | present |
| MySQL wire compatibility (8.4 clients recommended; 9.0 needs auth config) [CLAIM-dolt-01] | present |
| System tables: `dolt_log`, `dolt_commits`, `dolt_diff`, `dolt_history_<table>` [CLAIM-dolt-02] | present |
| Cell-level three-way merge with `dolt_conflicts_<table>` (base/our/their), schema conflicts [CLAIM-dolt-02] | present |
| `AS OF` queries | believed present; not in fetched page (conf 0.6) |
| Postgres compatibility | Beta (Doltgres) |
| Graph model / traversal | absent (relational) |
| Row-level security, tenant isolation | NOT PUBLICLY VERIFIED |
| Valid time (business time) | absent natively |

## 4. Architecture
```
 MySQL clients / CLI
     v
 SQL engine (go-mysql-server) -> versioned storage engine
     working set --commit--> commit DAG (branches/tags/remotes)
     content-addressed chunks (prolly trees) <-> remotes (DoltHub, S3, file)
```

## 5. Reconstruction
Hypothesis (public engineering blogs, not re-fetched; conf 0.6): tables are stored as prolly trees — content-addressed, history-independent B-tree-like structures — so identical contents share chunks and diff/merge cost is proportional to changes, not table size. Commits form a Merkle DAG; branches are refs. Diff = tree-walk of differing chunks; merge = three-way cell merge with conflict tables [CLAIM-dolt-02]. Transactions at SQL level with commit-on-demand. Security: SQL users/grants (MySQL style; verified only at documentation level: NOT VERIFIED).

## 6. Inferred requirements
Version-control semantics for tabular exports of ontology/reference data; commit signing; conflict workflow; remotes under customer control.

## 7. Performance
No benchmark gathered; vendor claims not collected. Expectation: storage dedupe for similar versions; diff scales with change size (hypothesis). Failure mode: merge conflicts on high-churn rows; large binary blobs.

## 8. Strengths
Real branch/merge/diff of data with SQL; Apache-2.0; self-hosted; cell-level diffs. Match for ontology/reference tables; exceed: semantic (graph-aware) merge.

## 9. Limitations
| Class | Item |
|---|---|
| Intentional | table-oriented; commit granularity coarse vs streaming ingest |
| Friction | MySQL client/auth quirks [CLAIM-dolt-01]; Postgres side Beta |
| Semantic | merges rows not graph semantics (dangling edges, ontology constraints) — hypothesis |
| Hypothesis | high-frequency writes create many commits/chunks |

## 10. Deployment/licensing
Single Go binary / Docker, no cloud dependency, air-gap viable; Apache-2.0 permissive, no legal trigger recorded.

## 11. Delta vs baseline
BL-38 diff/snapshots/playback and BL-32 gitops for ontology give Git-like workflow at app level; no data-level merge of graph branches (CAP-35 partial). Dolt could store versioned ontology/mapping tables or serve as an export format for BL-38 snapshots. EOIP lacks: three-way merge with conflict resolution for graph data; Dolt lacks graph semantics. Compare TerminusDB (C01-terminusdb.md) which is graph-native; Dolt is the cheaper tabular path.

## 12. Cards
STR-dolt-01 | Dolt 2.6 | three-way cell merge with queryable conflict tables | CLAIM-dolt-02 | review workflow for reference data/ontology tables | match | conflict records modeled on base/our/their for BL-32 semantic changes | conflicting ontology edits yield a reviewable conflict set.
STR-dolt-02 | Dolt | SQL-queryable history (`dolt_history_*`) | CLAIM-dolt-02 | analysts audit changes in SQL | integrate | optional Dolt sink for exported snapshots | diff of two BL-38 snapshots equals `dolt_diff`.
INV-dolt-01 | Dolt | tabular merge ignores graph/ontology semantics | root cause: data model (hypothesis) | semantic-aware merge: run SHACL (BL-29) and edge-integrity checks post-merge | options: Dolt for tables / TerminusDB / native graph merge | choose native semantic merge over BL-38 diff, Dolt as test oracle | POC: 1k conflicting edits; metric: invalid-graph merges = 0 | deps BL-28 gate | defensibility: ontology-aware merge + permissions | EXPERIMENT. Seed §10.5: none target Dolt.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-35 branch/merge/diff (graph) | BUILD semantic merge on BL-38; REFERENCE Dolt/TerminusDB |
| CAP-41 ontology release workflow | REFERENCE (gitops) |
| Dolt as versioned export sink | EXPERIMENT |
| CAP-74 backup | REJECT |

## 14. Tests
Round-trip BL-38 snapshot→Dolt→diff equivalence; conflict scenario suite; tenant data in separate databases; air-gap sql-server start.

## 15. Risks / open questions
Year of 2.6.0 inferred; `AS OF` and prolly-tree claims unverified in this session; ACL model unknown.

## Appendix A — Dimensions
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | active, Apache-2.0 |
| D2 | 2 | versioned data |
| D3 | 4 | SQL engine + commit DAG |
| D4 | 5 | prolly trees (hypothesis) |
| D5 | 3 | SQL schema; schema conflicts |
| D6 | 3 | MySQL SQL |
| D7 | N/A | |
| D8 | 5,9 | SQL tx; merge |
| D9 | 3 | CSV/import; push/pull |
| D10 | N/A | |
| D11 | 3,5 | commit-time versioning, no valid time |
| D12–D14 | N/A | |
| D15 | 12 | review via conflicts |
| D16 | N/A | |
| D17 | 3 | CLI, SQL |
| D18 | 3 | UNVERIFIED |
| D19 | 14 | DB per tenant (proposal) |
| D20 | 7 | none |
| D21 | 10 | permissive |
| D22 | 11 | SQL export |
| D23 | N/A | |
| D24 | App C | |

## Appendix B — Capability mapping
| CAP | Native | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-35 | native (tables) | dolt-02 | BL-38 Implemented/partial merge | BUILD+REFERENCE | P2 |
| CAP-36 | partial | dolt-02 | BL-37 | REFERENCE | P3 |
| CAP-16 | native SQL | dolt-01 | BL-59 Absent | REFERENCE | P3 |
| CAP-41 | partial | dolt-02 | BL-32 Partial | REFERENCE | P2 |

## Appendix C — Evidence
| ID | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| dolt-01 | repo | Apache-2.0; MySQL server; Doltgres Beta; releases show 2.6.0 on 23 Oct | Officially documented | https://github.com/dolthub/dolt (+/releases) | 2026-10-26 | 0.85; year inferred | none |
| dolt-02 | docs | dolt_log/commits/diff/history tables; conflict tables | Officially documented | https://www.dolthub.com/docs/sql-reference/version-control/dolt-system-tables | 2026-10-26 | 0.9 | none |

## Appendix D — Assumptions
Prolly-tree storage from prior knowledge; no code read.
