| Field | Value |
|---|---|
| Registry ID | T-C01-terminusdb |
| Tier | B (git-like versioned graph reference; cross-ref C13-terminusdb-bitemporal placeholder, not edited) |
| Versions examined | v12.0.8 (released 2026-10-12); README references v12.0.7 and a 12.1 release candidate |
| Verified on | 2026-10-26 (brief says 2026-10-18; actual access date used) |
| Worker | V14 |

## 1. Identity, current status, tier, and sources
TerminusDB is an open-source document and graph database with git-like revision control (commits, branches, diff, patch, push/pull/clone). Repo `terminusdb/terminusdb`, Apache-2.0, ~3.5k stars, latest release v12.0.8 (2026-10-12), pushed 2026-10-25 [CLAIM-terminus-01]. Maintenance: the README says v12 is maintained by the Gettier team (gettier.ai), and Wikipedia says Gettier (formerly DFRNT) has maintained TerminusDB since 2025; no acquisition announcement found [CLAIM-terminus-02]. The original company (TerminusDB/Data Chemist) history is not examined; status active. Placeholder note: [C13-terminusdb-bitemporal.md](C13-terminusdb-bitemporal.md) is untouched. Peer: [C01-neo4j](C01-neo4j.md) (no versioning).

## 2. Primary problem, target workloads, example workflows
Collaborative, auditable data with branch/merge semantics: data products, config-as-data, ML datasets. Example: branch `proposal-42` from `main`, run a bulk import on the branch, diff against `main` (JSON diff), then merge or discard. Relevant to EOIP BL-37/38 and CAP-35.

## 3. Feature inventory
| Feature | Status | Note |
|---|---|---|
| Commits, branches, diff, patch, merge/squash, time-travel | present | [CLAIM-terminus-02] |
| push/pull/clone between nodes | present | collaboration model |
| JSON/JSON-LD documents as linked data; document API | present | v12 adds raw JSON with dedup |
| WOQL (Datalog-style) + path queries | present | [CLAIM-terminus-02] |
| GraphQL | present | auto-generated from schema |
| Schema with types (JSON-document schema); constraints | present | |
| Vector search | preview (12.1-rc `vectorsearch/` folder) | not final |
| SPARQL / Cypher / Gremlin | absent | |
| OWL/SHACL reasoning | absent/partial (schema-level) | UNVERIFIED |
| Clustering/HA | unknown | single-server design |

## 4. Architecture
```
 clients (REST/WOQL/GraphQL/CLI) -> Prolog server (query, schema, auth)
     -> storage engine: immutable layers (succinct data structures) + delta layers
     -> repository: commits -> branches (refs) ; push/pull sync of layers
```

## 5. Under-the-hood reconstruction
Data is stored in immutable "layers"; a commit adds a delta layer over its parent, giving cheap branches, time travel and diff (the succinct-data-structure/layer design is described by the project; the README confirms succinct data and revision control but not layer internals, so layer mechanics are HYPOTHESIS from public design talks) [CLAIM-terminus-02]. Branch = named pointer to a layer stack; merge = apply patch with conflict reporting on JSON diff; diff/patch operate on documents. Concurrency: single-writer per branch (hypothesis). Security: capability-based roles per resource. Server core in Prolog, with a Rust storage component (README does not confirm; UNVERIFIED).

## 6. Requirements inferred
Immutable append-only layers; named refs; diff/patch format that is stable and signable; merge conflict model; sync protocol.

## 7. Performance and resource model
No benchmark verified. Hypothesis: delta layers add read-time cost until squashed; memory-resident indexes mean working set must fit RAM. Failure modes: long layer chains, merge conflicts on concurrent edits.

## 8. Strengths
First-class branch/diff/merge on data with provenance of changes; document+graph unification; Apache-2.0. Match: EOIP already has revisions (BL-37), diff (BL-38) and ontology gitops (BL-32); adopt branch-scoped "what-if" graphs and merge conflict policy from Terminus.

## 9. Limitations
| Class | Item |
|---|---|
| Maturity | small ecosystem; governance transition (DFRNT/Gettier) |
| Algorithmic | memory-resident succinct index; whole-database versioning granularity (hypothesis) |
| Friction | WOQL is a niche language; no Cypher/SPARQL/Gremlin |
| Semantics | versioning is transaction-time only; valid-time bitemporal not native (UNVERIFIED) |
| Licensing | Apache-2.0, none |

## 10. Deployment, licensing, redistribution
Apache-2.0, redistribution-safe. Docker/self-hosted; air-gap viable. No community/enterprise split verified; hosted TerminusX status UNVERIFIED. Not a drop-in `GraphStore` backend; candidate for a versioned side-store for ontology or reference data.

## 11. Competitive delta vs EOIP baseline
EOIP has application-layer bitemporal reads (BL-37) and diff/snapshots (BL-38); branching with merge/rollback (CAP-35) is not in the baseline for instance graphs. Terminus supplies branch/merge semantics natively. EOIP's valid-time axis exceeds Terminus's commit-time model if confirmed.

## 12. Strength cards and inversion cards
- STR-terminus-01 | TerminusDB | branch/diff/merge on data | CLAIM-terminus-02 | safe what-if, approval before merge | match | branch-scoped overlay on `GraphStore` using BL-37 revisions and BL-38 diff, merge only via validation gate (BL-28) | acceptance: branch with 10^5 edits, diff exact, merge rejected on policy violation, rollback restores byte-identical export.
- STR-terminus-02 | TerminusDB | push/pull sync of versioned data | CLAIM-terminus-02 | air-gapped site sync | experiment | signed diff bundles | acceptance: two-site round trip converges.
- INV-terminus-01 | v12.0.8, enterprise KG | commit-time only; whole-DB branch granularity | root cause data model (hypothesis) | alternative: bitemporal (valid + transaction) with scoped branches per tenant/subgraph; worse for tiny datasets where whole-DB branches are enough | options: (a) side-store for ontology data (b) native overlay branches (c) layered event-sourced graph | selected (b) | POC: 10^6-edge graph, 1k branches, success = branch create O(1) and diff time proportional to delta; baseline TerminusDB 12 | failure: cross-branch ACLs | defensibility: bitemporal + permission-aware | decision: EXPERIMENT.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-35 branching/diff/merge | BUILD (reference design) |
| CAP-34 bitemporal | BUILD (already BL-37) |
| CAP-36 event sourcing | REFERENCE-ONLY |
| CAP-01 as backend | REJECT |
| CAP-41 ontology release workflow | EXPERIMENT (as versioned side-store) |

## 14. Tests / PoC
Replicate branch-diff-merge scenario on TerminusDB 12 and on EOIP overlay; compare diff size and merge conflicts; measure memory per million triples.

## 15. Risks and open questions
Governance continuity (Gettier); layer internals unverified; 12.1 vector features unreleased; valid-time support unknown.

## Appendix A. Research-dimension coverage
| Dimension | Sections | Summary |
|---|---|---|
| D1-D4 | 1-4 | covered |
| D5 storage | 5 | layers (hypothesis) |
| D6 query | 3 | WOQL, GraphQL |
| D7 reasoning | 3 | limited |
| D8 concurrency | 5 | hypothesis |
| D9 performance | 7 | no numbers |
| D10 versioning | 3,5 | core strength |
| D11 security | 5 | capabilities |
| D12-D16 | N/A | not examined |
| D17 ops | 10 | docker |
| D18 UX | N/A | dashboard not examined |
| D19-D20 | 10 | Apache-2.0 |
| D21 ecosystem | 1,9 | small |
| D22-D24 | 12,15 | covered |

## Appendix B. Capability mapping
| CAP-ID | This tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-35 | native | 02 | BL-38 partial | BUILD | P1 |
| CAP-34 | partial (UNVERIFIED) | 02 | BL-37 implemented | BUILD | P2 |
| CAP-03 | native | 02 | BL-01 | REFERENCE | P3 |
| CAP-73 | unknown | - | BL-38 | EXPERIMENT | P3 |

## Appendix C. Evidence records
| CLAIM-ID | Product/version/date | Claim | Class | Source | Dates | Confidence | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-terminus-01 | v12.0.8 | Apache-2.0; release 2026-10-12; 3.5k stars | primary (API) | https://api.github.com/repos/terminusdb/terminusdb | 2026-10-26 | 0.85 | README cites 12.0.7 |
| CLAIM-terminus-02 | README | Gettier maintains v12; revision control; diff/patch; WOQL; GraphQL; JSON docs; 12.1-rc | vendor docs | https://github.com/terminusdb/terminusdb | 2026-10-26 | 0.75 | Wikipedia (secondary) agrees on maintainer, https://en.wikipedia.org/wiki/TerminusDB |

## Appendix D. Assumptions
Layer internals are public-talk-based hypotheses; no acquisition assumed.
