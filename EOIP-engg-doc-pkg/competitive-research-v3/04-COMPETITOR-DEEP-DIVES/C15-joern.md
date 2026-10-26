# C15 — Joern

| Field | Value |
|---|---|
| Registry ID | T-C15-joern |
| Tier | B — open code property graph (CPG) platform |
| Versions examined | v4.0.665 (2026-10-23); repo pushed 2026-10-26 |
| Verified on | 2026-10-26 (brief date 2026-10-18) |
| Worker | V28 (W27 scope) |

## 1. Identity, current status, tier, and sources

| Item | Finding | Claim |
|---|---|---|
| Identity | Open-source platform building code property graphs from source, bytecode and binaries; Scala-based query language; `joernio/joern` | [CLAIM-joern-01] |
| Owner | joern.io says "Maintained by Whirly Labs"; sponsors listed Qwiet AI, Privado, TU Braunschweig, Stellenbosch; README names no maintainers | [CLAIM-joern-02] |
| Status | Active; automatic release once per day (v4.0.665 on 2026-10-23); stars 3.6k | [CLAIM-joern-01][CLAIM-joern-03] |
| Licence | Apache-2.0 | [CLAIM-joern-01] |
| Name check | Pinned to `joernio/joern` (Whirly Labs / joern.io); no collision investigated beyond this | |

## 2. Primary problem, workloads, workflows

Vulnerability discovery and program-analysis research: build CPG once, query data-flow and call structure. EOIP use (J9/J10): "which sinks does config key X reach", "which callers of rule function R", export slices as graph facts. Needs JDK 21.

## 3. Feature inventory

| Feature | Status | Claim |
|---|---|---|
| Frontends (maturity per docs): C/C++ and Java very high; JS, Python, x86 (Ghidra) high; JVM bytecode (Soot), Kotlin, PHP, Go, Swift medium; Ruby, C# medium-low | present | [CLAIM-joern-04] |
| Interactive shell, scripts, scanner (`joern-scan`), slicing (`joern-slice`), export (`joern-export`), parse (`joern-parse`) | present | [CLAIM-joern-01] |
| Server mode (`joern --server`) | present | [CLAIM-joern-01] |
| Query DB / queries repository | present (queries.joern.io) | [CLAIM-joern-02] |
| Incremental CPG update | NOT PUBLICLY VERIFIED | |
| Web UI | absent in evidence | |
| ACL / multi-tenant | absent | |

## 4. Architecture diagram

```
 source/bytecode/binary --frontend (per language)--> CPG (flatgraph, in-memory + file)
 CPG --passes (call graph, data flow, type recovery)--> enhanced CPG
 shell / server / scanners / export (GraphML, etc., recalled UNVERIFIED) <-- queries (Scala DSL)
```

## 5. Under-the-hood reconstruction

- Data model: code property graph merging AST, control-flow and data-flow/dependence (CPG spec at cpg.joern.io; spec content not read, hypothesis). Typed schema, nodes and edges with properties [CLAIM-joern-01][CLAIM-joern-04].
- Storage: custom in-memory graph store; v4.0.0 migrated from OverflowDB to flatgraph (changelog note via README) [CLAIM-joern-01]. On-disk layout NOT PUBLICLY VERIFIED.
- Pipeline: frontend produces base CPG; "passes" enrich it (inferred; names recalled, UNVERIFIED). Query DSL is Scala on top of traversal steps (docs say built on Gremlin-Scala lineage; flatgraph era may differ) [CLAIM-joern-04].
- Concurrency/transactions: single-process analysis; NOT PUBLICLY VERIFIED.
- Security: runs analysers on untrusted code only as parsers; sandbox guidance not read.

## 6. Requirements inferred

JVM runtime (JDK 21), memory proportional to CPG, per-language frontends of unequal maturity.

## 7. Performance and resource model

No benchmark retrieved: NOT PUBLICLY VERIFIED. In-memory CPG implies RAM grows with program size (reasoned). Failure modes: low-maturity frontends yield incomplete flows; JDK mismatch untested.

## 8. Strengths

| Strength | Match or exceed |
|---|---|
| Apache-2.0 CPG with data flow, redistributable | INTEGRATE as optional analyser sidecar |
| Many frontends incl. binaries | reuse frontends selectively |
| Slicing/export for pipelines | map CPG slices to EOIP SourceEvents |

## 9. Limitations

| Class | Finding | Claim |
|---|---|---|
| Friction | Scala DSL; JDK 21; daily releases make pin discipline necessary | [CLAIM-joern-01][CLAIM-joern-03] |
| Maturity | Ruby, C# medium-low; maturity ratings are vendor-stated | [CLAIM-joern-04] |
| Operational | In-memory graph; whole-program rebuild (hypothesis) | [CLAIM-joern-01] |
| Governance | Company-backed (Whirly Labs), sponsor-funded; roadmap unpublished | [CLAIM-joern-02] |

## 10. Deployment, licensing, redistribution

Self-hosted CLI/Docker; Apache-2.0 (patent grant included in licence text; confirm bundled dependencies such as Ghidra (Apache-2.0, recalled), Soot (LGPL, recalled), Eclipse CDT (EPL, recalled): all UNVERIFIED, legal review for any bundled frontend). Air-gap: yes in principle (no cloud dependency evidenced). One-node: yes, RAM-bound.

## 11. Competitive delta against EOIP baseline

BL-42: EOIP has symbol/diff graph for Python/TS; no data-flow, no C/Java depth. Joern fills data-flow without CodeQL's licence. Precise cross-reference from SCIP (C15-scip-lsif.md) is complementary; tree-sitter (C15-tree-sitter.md) is cheaper but syntactic. Ingestion must obey BL-23 (never write graph directly) and BL-40 (flows are PROPOSED).

## 12. Cards

`STR-joern-01 | Joern | open CPG with data-flow | CLAIM-01,04 | blast radius J9 | integrate | run in container, export slices, ingest as proposed facts with code spans | seeded flow in Java fixture found; finding has file:line evidence`

INV-joern-01: Joern v4.0.665, large monorepo; limitation: in-memory CPG and no evidenced incremental update (hypothesis; storage). Alternative: per-changed-module CPG on demand, store only slices in EOIP graph; worse when whole-program flows needed. Options: (a) nightly full CPG, (b) module-scoped CPG keyed by blob hash, (c) native incremental data-flow. Selected (b). POC: 2M-LOC repo, edit one file, measure rebuild RAM/time vs full; success: >5x less than full on touched-module scope (target, unmeasured baseline). Defensibility: governance and ownership joins. Decision: EXPERIMENT. Seed hypotheses in §10.5 do not target Joern.

## 13. Decisions

| Capability | Decision |
|---|---|
| CAP-66 data-flow code graph | INTEGRATE (optional sidecar) |
| CAP-67 incremental | EXPERIMENT |
| CAP-68 | DEFER |

## 14. Tests and acceptance

Container build offline; index 3 fixture repos; export slice; ingest via SourceEvent; verify tenant-scoped storage and span evidence; licence scan of container.

## 15. Risks and open questions

Dependency licences; JVM footprint on one node; stability across daily releases; graph-export schema stability.

## Appendix A — Dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Apache-2.0, daily releases |
| D2 | 2 | Vuln discovery |
| D3 | 4 | Frontends, passes, shell |
| D4 | 5 | flatgraph |
| D5 | 5 | CPG schema |
| D6 | 5 | Scala traversal DSL |
| D7 | N/A | Not logic reasoning |
| D8 | 5,7 | Single process |
| D9 | 5 | Frontends parse |
| D10 | N/A | None |
| D11 | 9 | Not evidenced |
| D12 | N/A | Mentions vectors tool only |
| D13 | 3 | Server/REST |
| D14 | N/A | Absent |
| D15 | N/A | None |
| D16 | 3 | Shell |
| D17 | 3 | Scripts |
| D18 | 5 | No ACL |
| D19 | N/A | None |
| D20 | 7 | No figures |
| D21 | 10 | Apache-2.0 |
| D22 | 3 | Export |
| D23 | N/A | Not checked |
| D24 | 15 | Docs/README only |

## Appendix B — Capability mapping

| CAP | Technology | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-66 | native | 01,04 | BL-42 Partial | INTEGRATE | P2 |
| CAP-67 | unknown | 01 | BL-42 | EXPERIMENT | P2 |
| CAP-69 | partial | 01 | BL-42 | INTEGRATE | P2 |

## Appendix C — Evidence records

| CLAIM | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| 01 | README 2026-10-26 | CPG platform, JDK 21, Apache-2.0, flatgraph migration, daily release, launchers | Officially documented | https://github.com/joernio/joern | n/a / 2026-10-26 | 0.85 | joern.io lists fewer languages |
| 02 | joern.io | maintained by Whirly Labs; sponsors; query DB | Officially documented | https://joern.io | 2026-10-26 | 0.7 | site language list outdated vs docs |
| 03 | v4.0.665 | release 2026-10-23 | Observed | GitHub API releases/latest | 2026-10-26 | 0.9 | none |
| 04 | docs | frontend maturity table, Scala query language | Officially documented | https://docs.joern.io/ | 2026-10-26 | 0.8 | joern.io says Python/Java "coming soon" (stale) |

## Appendix D — Assumptions

Dependency licences are recalled, not verified. Query language lineage taken from docs text; flatgraph-era detail unverified.
