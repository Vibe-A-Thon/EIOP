# C15 — CodeQL

| Field | Value |
|---|---|
| Registry ID | T-C15-codeql |
| Tier | B — code-as-data query engine; licence is the decisive question |
| Versions examined | CodeQL CLI v2.27.3 (2026-10-20), v2.27.2 (2026-10-07), v2.27.1 (2026-09-22); `github/codeql` queries/libraries (MIT) pushed 2026-10-26 |
| Verified on | 2026-10-26 (brief date 2026-10-18) |
| Worker | V28 (W27 scope) |

## 1. Identity, current status, tier, and sources

| Item | Finding | Claim |
|---|---|---|
| Identity | GitHub's "language and toolchain for code analysis": extractors build a per-language database; queries in QL | [CLAIM-codeql-01] |
| Status | Active; CLI releases about every 2 weeks | [CLAIM-codeql-02] |
| Languages | C/C++, C#, GitHub Actions, Go, Java, Kotlin, JavaScript, Python, Ruby, Rust, Swift, TypeScript | [CLAIM-codeql-03] |
| Licence split | (a) Queries/libraries repo `github/codeql`: MIT. (b) CLI/engine binaries: GitHub CodeQL Terms and Conditions, proprietary | [CLAIM-codeql-04][CLAIM-codeql-05] |
| Licence terms for use | See section 10: free only for academic research, demos, testing OSI-licensed queries, and analysis of OSI-licensed ("Open Source Codebase"); creating DBs in CI/CD, or analysing any non-open-source codebase, is not authorised unless under a paid GitHub Advanced Security licence | [CLAIM-codeql-05] |

## 2. Primary problem, workloads, workflows

Variant analysis and security queries over code treated as data. Workflow: build DB, run query suites, emit SARIF. EOIP J9/J10: results enter the graph as proposed facts (BL-40).

## 3. Feature inventory

| Feature | Status | Claim |
|---|---|---|
| Extractors (build-tracing for compiled, source-direct for interpreted) | present | [CLAIM-codeql-01] |
| DB holds AST, data-flow graph, control-flow graph, source copy | present | [CLAIM-codeql-01] |
| QL object-oriented Datalog-like language | present | [CLAIM-codeql-01] |
| CLI, VS Code extension | present | [CLAIM-codeql-01] |
| SARIF output | present (recalled, UNVERIFIED here) | |
| Incremental DB update | NOT PUBLICLY VERIFIED (release notes read show none) | [CLAIM-codeql-02] |
| Hosted service | GitHub code scanning (separate product) | [CLAIM-codeql-05] |

## 4. Architecture diagram

```
 source --(build tracing / extractor per language)--> CodeQL DB dir (relations + src copy + schema)
 .ql queries + qlpacks --(CLI compile -> evaluator)--> results (BQRS/SARIF)
```

## 5. Under-the-hood reconstruction

- Data model: per-language relational schema; a table per language construct, wrapped by QL classes (e.g. Java `Expr`, `Stmt`) [CLAIM-codeql-01].
- Build capture: compiled languages monitor compiler invocations; interpreted languages parsed directly [CLAIM-codeql-01].
- Query pipeline: QL compiled to relational plans (hypothesis based on Datalog-like semantics; internals of evaluator, optimiser and storage are proprietary): NOT PUBLICLY VERIFIED.
- Reasoning: recursion via QL predicates (recalled, UNVERIFIED). Versioning/security: DB is immutable per commit; no ACL model.
- Concurrency, partitioning, caching: NOT PUBLICLY VERIFIED.

## 6. Requirements inferred

Working build for compiled languages; per-commit DB.

## 7. Performance and resource model

No independent benchmark retrieved: NOT PUBLICLY VERIFIED. Failure modes: build fails means no DB; macOS 27/Xcode 27 autobuild unsupported in 2.27.3 [CLAIM-codeql-02]; DB per commit is a full rebuild (no incremental evidence).

## 8. Strengths

| Strength | Match or exceed |
|---|---|
| Deep data-flow and taint queries across a code base | integrate results as evidence; do not rebuild solver |
| Large open query library (MIT) | reuse rule ideas, subject to per-file check |

## 9. Limitations

| Class | Finding | Claim |
|---|---|---|
| Licensing | Proprietary CLI; no use on private/commercial code outside GHAS; no hosted-service rights; no redistribution; no reverse engineering | [CLAIM-codeql-05] |
| Operational | Requires buildable project for compiled languages | [CLAIM-codeql-01] |
| Algorithmic | Whole-DB rebuild per commit (hypothesis) | |

## 10. Deployment, licensing, redistribution

Exact terms (LICENSE.md in `github/codeql-cli-binaries`, read 2026-10-26) [CLAIM-codeql-05]: licensed per user. Permitted: academic research; demonstration; testing OSI-licensed queries. Additionally, only with an Open Source Codebase (OSI-licensed): analysis, and DB creation for GitHub.com-hosted open-source codebases during automated analysis/CI/CD. Not authorised: generating a DB for automated analysis/CI/CD in any other context; use with any codebase that is not an Open Source Codebase (e.g. private repo); working around limits; reverse engineering; sharing, publishing, distributing, lending, or providing the Software as a hosted solution, alone or integrated in other software; transfer. Carve-out: a paid GitHub Advanced Security licence lifts the automation and non-open-source restrictions. The setup page says users without a GitHub Enterprise licence accept these terms by downloading [CLAIM-codeql-06]. Consequence for EOIP: the CLI cannot be bundled, white-labelled, or run as part of a product for customers; each customer would need own GHAS rights. Legal-review trigger: yes. Air-gap: CLI runs offline once downloaded (recalled, UNVERIFIED). The MIT queries repo does not grant rights to the engine.

## 11. Competitive delta against EOIP baseline

BL-42: EOIP has symbol/diff-hunk graph, no data-flow. CodeQL would add CAP-66/68-style security facts but cannot be shipped. Alternatives for the same need: C15-joern.md (Apache-2.0 CPG), C15-semgrep.md (LGPL engine). See C15-scip-lsif.md for precise references.

## 12. Cards

`STR-codeql-01 | CodeQL | interprocedural taint and variant queries | CLAIM-01 | security blast-radius evidence (J9) | integrate as customer-optional import | SARIF-to-SourceEvent adapter, results marked PROPOSED (BL-40) | import SARIF from customer-run CodeQL; each finding has file/line span and BL-41 manifest`

INV-codeql-01: target CLI 2.27.3; workload commercial private-code analysis in a shipped product. Limitation: terms forbid it (proven, CLAIM-05). Root cause: licensing. Alternative: Joern/Semgrep CE; worse when CodeQL's query depth is needed. Options: (a) customer-run SARIF import, (b) native tree-sitter plus Joern CPG for data-flow, (c) differentiated: governed code-fact graph with evidence-linked queries. Selected: (a) now, (b) experiment. POC: same 3 CWE-style cases on a test repo across CodeQL (customer licence) vs Joern; metric: recall on seeded flaws. Defensibility: governance and joins to Jira/CI. Decision: EXPERIMENT (import only); REJECT bundling.

## 13. Decisions

| Capability | Decision |
|---|---|
| CAP-66 engine bundling | REJECT (licence) |
| SARIF import as evidence | INTEGRATE (customer-supplied) |
| Query-library ideas | REFERENCE-ONLY, review per file |

## 14. Tests and acceptance

Legal sign-off first; SARIF import with provenance; product build contains no CodeQL binaries.

## 15. Risks and open questions

Terms can change; GHAS pricing unverified.

## Appendix A — Dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Active, mixed licence |
| D2 | 2 | Security variant analysis |
| D3 | 4 | Extractor, DB, evaluator |
| D4 | 5 | Relational DB per language |
| D5 | 5 | Per-language schema |
| D6 | 5 | QL; internals unverified |
| D7 | 5 | Recursion only |
| D8 | N/A | Batch tool |
| D9 | 5 | Build tracing |
| D10 | N/A | Not in scope |
| D11 | 9 | Per commit DB |
| D12 | N/A | Not in scope |
| D13 | 2 | SARIF to agents |
| D14 | N/A | Absent |
| D15 | N/A | Not in scope |
| D16 | 3 | VS Code ext |
| D17 | 3 | CLI, qlpacks |
| D18 | 10 | No ACL model |
| D19 | N/A | Per user licence |
| D20 | 7 | No figures |
| D21 | 10 | Exact terms quoted |
| D22 | 3 | SARIF |
| D23 | N/A | Not checked |
| D24 | 15 | Official sources |

## Appendix B — Capability mapping

| CAP | Technology | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-66 | native | 01 | BL-42 Partial | INTEGRATE (import) | P2 |
| CAP-68 | partial | 03 | Absent | DEFER | P3 |
| CAP-77 | n/a | 05 | BL-22 | REJECT bundling | P1 |

## Appendix C — Evidence records

| CLAIM | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| 01 | CodeQL docs 2026 | extractors, DB contents, QL | Officially documented | https://codeql.github.com/docs/codeql-overview/about-codeql/ | n/a / 2026-10-26 | 0.85 | none |
| 02 | CLI 2.27.3 | releases 2.27.1-2.27.3 dates and notes | Officially documented | https://github.com/github/codeql-cli-binaries/releases | 2026-10-20 / 2026-10-26 | 0.9 | none |
| 03 | latest | supported language list | Officially documented | https://codeql.github.com/docs/codeql-overview/supported-languages-and-frameworks/ | 2026-10-26 | 0.85 | none |
| 04 | github/codeql | MIT licence | Observed | https://raw.githubusercontent.com/github/codeql/main/LICENSE | 2026-10-26 | 0.9 | none |
| 05 | CLI binaries | GitHub CodeQL Terms and Conditions as paraphrased in sec 10 | Observed | https://github.com/github/codeql-cli-binaries/blob/main/LICENSE.md | 2026-10-26 | 0.9 | docs.github.com may add GHAS terms |
| 06 | setup docs | non-Enterprise users accept Terms by download | Officially documented | https://docs.github.com/en/code-security/codeql-cli/getting-started-with-the-codeql-cli/setting-up-the-codeql-cli | 2026-10-26 | 0.8 | none |

## Appendix D — Assumptions

Terms read via fetch; SARIF and offline operation UNVERIFIED.
