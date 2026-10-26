# C03 — TopBraid EDG (TopQuadrant; now documented as "TQ Data Foundation")

| Field | Value |
|---|---|
| Registry ID | T-C03-topbraid-edg |
| Tier | A — leading enterprise ontology/vocabulary governance platform; target of Master Prompt §10.5 seed inversion #2 |
| Versions examined | EDG 9.0 (9.0.0–9.0.4), 9.1, 9.2 (9.2.0 change log under `/2026/05/`), 9.3 (9.3.0–9.3.2; 9.3.0 change log under `/2026/08/`); exact release dates NOT PUBLICLY VERIFIED on release pages |
| Verified on | 2026-10-26 (actual access date; brief said 2026-10-18 — see Appendix D) |
| Worker | V03 |

## 1. Identity, current status, tier, and sources

TopBraid EDG is a proprietary, server-side enterprise data-governance platform from **TopQuadrant** (Raleigh, North Carolina; founded 2001; TopBraid Suite 2007; staff co-authored W3C SHACL) [CLAIM-edg-09]. Registry resolution: no acquisition or merger of TopQuadrant by Graphwise/Semantic Web Company or anyone else was found [CLAIM-edg-09] (the Graphwise merger belongs to PoolParty, see C03-poolparty). Naming drift: the 9.2 documentation is titled **"TQ Data Foundation"**, TQ Data Foundation was launched in February 2026 as a context layer for AI agents, and TopBraid Composer was replaced by EDG Studio [CLAIM-edg-09]; whether "EDG" persists as a separate product name is NOT PUBLICLY VERIFIED.

| Item | Verified state |
|---|---|
| Latest line | 9.3 (patches 9.3.0–9.3.2); 9.2 completed RDF 1.2 reification and SHACL 1.2 features [CLAIM-edg-02][CLAIM-edg-04] |
| Cadence | 9.0, 9.1, 9.2 (change log 2026-05), 9.3 (change log 2026-08): about one minor per quarter in 2026; dates inferred from file paths, LOW confidence |
| Platform | Java 21 and Tomcat 11 [CLAIM-edg-01][CLAIM-edg-07] |
| Licence | Proprietary subscription; pricing NOT PUBLICLY VERIFIED |
| Open parts | **TopBraid SHACL API**: Apache-2.0, Jena-based, pushed 2026-06-30, not archived; same code used in commercial products [CLAIM-edg-10] |
| Ownership | Privately held; ownership not published on About page [CLAIM-edg-09] |

## 2. Primary problem, target workloads, concrete example workflows

Governed management of enterprise vocabularies, taxonomies, ontologies, reference data, business glossaries and metadata catalogs, modelled as RDF/SHACL "asset collections", with workflow-governed change. Workflows:

1. **Glossary term change**: a user starts a workflow, edits in an isolated working copy, freezes for review, SME and approver review, a production editor commits; SHACL shapes tagged to the workflow check the change set before commit [CLAIM-edg-05].
2. **Ontology in Git**: asset collection saved as sorted Turtle, pushed to Git from a server-local clone [CLAIM-edg-08]; 9.3 adds GitHub App authentication, partial-commit and "time travel" workflows from Change History [CLAIM-edg-03].
3. **Data catalog / metadata**: automated catalog creation from Databricks (9.3 headline), crosswalks and auto-tagging (8.0) [CLAIM-edg-02].
4. **AI context**: 9.0 GraphRAG (chunking, vector search plus SPARQL in SPARQL/GraphQL APIs, Python SDK); 9.3 MCP server [CLAIM-edg-01][CLAIM-edg-02].

## 3. Feature inventory

| Capability | State | Notes |
|---|---|---|
| Vocabulary/ontology/taxonomy editors (forms, tree) | present | SHACL-driven forms |
| Visual ontology editor | present (new in 9.3) | details NOT PUBLICLY VERIFIED [CLAIM-edg-02] |
| SHACL validation (Core, SPARQL) | present | TopBraid SHACL/Jena [CLAIM-edg-10]; SHACL 1.2 features in 9.2 [CLAIM-edg-04] |
| Workflows with working copies, roles, templates | present | [CLAIM-edg-05] |
| Change history; undo from history | present | [CLAIM-edg-04] |
| Time-travel workflow; partial commit | present (9.3.0) | [CLAIM-edg-03] |
| Git import/reload/commit | present; branch switching outside UI (7.8 docs) | [CLAIM-edg-08] |
| Concurrent editing in one working copy | UNKNOWN | no doc found |
| Merge/conflict resolution between workflows | not documented; report lists affected workflows | [CLAIM-edg-05] |
| SKOS / reference data / glossaries / metadata packages | present | vendor pages |
| External graph DBs (read/write) | present: GraphDB, Neptune from 7.8; remote SPARQL from 7.7 | [CLAIM-edg-06] |
| API | SPARQL, GraphQL, REST, Python SDK `tq-client-lib` (renamed from `edg-sdk` in 9.2) | [CLAIM-edg-01][CLAIM-edg-04] |
| MCP | present (9.3) | [CLAIM-edg-02] |
| Notifications | present (9.0, off by default) | [CLAIM-edg-01] |
| Accessibility | WCAG 2.2 AA minimum (9.3) | [CLAIM-edg-02] |
| Auth/SSO | UNKNOWN this session | — |
| HA/clustering | not on platform page | [CLAIM-edg-07] |
| OWL reasoning | UNKNOWN; SHACL rules/inferencing present | [CLAIM-edg-10] |

## 4. Architecture diagram

```
 browser (EDG UI, SHACL-generated forms)     EDG Studio (dev tool)      Python/tq-client-lib, MCP clients
        └──────────────────────────────── HTTPS ───────────────────────────────────┘
                              Tomcat 11 / Java 21  (single web application)
   ┌──────────────────────────────────────────────────────────────────────────────────────────┐
   │ UI + API layer (SPARQL, GraphQL, REST, MCP)                                              │
   │ Governance layer: workflows(working copies) · roles · notifications · change history     │
   │ SHACL engine (TopBraid SHACL / Jena): forms, validation, rules                           │
   │ Jena-based RDF store (TDB; shared-graph or per-graph) + text/vector search               │
   └───────────────┬──────────────────────────────────┬───────────────────────────────────────┘
                   │ Git (local clone on server)       │ remote SPARQL 1.1 / GraphDB / Neptune (RW)
              sorted Turtle files                  external triple stores
```

State: working copies, change-history graphs and asset collections live in the internal TDB store (documented as Jena TDB-based) [CLAIM-edg-06]. Control plane: workflow templates are themselves RDF in the Governance collection [CLAIM-edg-05].

## 5. Under-the-hood reconstruction

**Data model.** Everything is RDF. An *asset collection* is a graph typed by a SHACL-defined model; instances (glossary terms etc.) are resources whose forms, tables and constraints derive from node/property shapes (SHACL-as-UI-schema). RDF 1.2 reification was added in 9.0 beside the native model and the legacy `tosh:reificationURI` form removed in 9.2 [CLAIM-edg-04]. Workflow templates use the `teamwork:` vocabulary (`teamwork:tagShape`, `teamwork:blockOnValidationSeverity`) [CLAIM-edg-05].

**Storage layout.** Internal database "based on Jena TDB"; shared-graph layout (a `_Data` folder) or per-graph TDB with many files (hence ulimit guidance); storage type fixed after workspace creation; an older in-memory+RDBMS option was dropped by 8.3. Docs remark backend choice matters mainly beyond about 30M triples, with external stores for "billions" [CLAIM-edg-06]. Full-text and vector search are integrated; index structure NOT PUBLICLY VERIFIED.

**Query pipeline.** SPARQL 1.1 (Jena ARQ) plus SPARQL/GraphQL APIs; 9.0 adds vector search combined with SPARQL [CLAIM-edg-01]. Planner is Jena's (reasoned inference); EDG-specific optimisation NOT PUBLICLY VERIFIED.

**Reasoning.** SHACL rules and inferencing (SHACL-AF via TopBraid SHACL), not OWL DL; OWL profile reasoning in EDG UNKNOWN [CLAIM-edg-10].

**Concurrency/transactions.** Isolation by working copy: each workflow edits a copy of production state; production changes only at commit by an authorised role; several workflows can be active; a report shows other workflows touched by a change; no merge algorithm documented [CLAIM-edg-05]. This is *branching with manual coordination* — not locking, not CRDT. Hypothesis: working copy = delta graphs recorded in the change-history graph and applied at commit; overlapping edits resolve triple-wise (NOT PUBLICLY VERIFIED).

**Partitioning/consistency.** Single-server TDB; scale-out by pushing collections to external stores [CLAIM-edg-06]. Cluster/HA not on the platform page [CLAIM-edg-07].

**Versioning.** Three layers: workflow transition history (archiving deletes detailed change records and keeps transitions) [CLAIM-edg-05]; change-history graph with undo and, from 9.3.0, "time travel workflow" to before a chosen change [CLAIM-edg-03]; Git sync of sorted Turtle with one-line diffs per triple [CLAIM-edg-08].

**Semantic diff.** The Workflow Report shows before/after triples filtered by predicate, asset, asset type, change type [CLAIM-edg-05]: triple-level, without additive/breaking classification like EOIP's `diff_manifests`.

**Security.** Roles and permission levels (viewer, editor, manager) per collection; workflow roles per transition. Tenant isolation: NOT PUBLICLY VERIFIED.

**Pseudocode (hypothesis from documented behaviour).**
```
start_workflow(collection, template): wc = copy_on_write(production); record in change_history(wc)
freeze(wc) -> "Frozen for Review"
commit(wc): report = shacl_validate(wc.changes, template.tagShape)
            if report.severity >= template.blockOnValidationSeverity: refuse
            else warn; apply(wc.changes -> production); archive?(wc)
```

## 6. Functional and non-functional requirements inferred

| ID | Requirement | Basis |
|---|---|---|
| FR-1 | Isolated change sets with review states and role-gated commit | [CLAIM-edg-05] |
| FR-2 | Pre-commit SHACL conformance check with configurable blocking severity | [CLAIM-edg-05] |
| FR-3 | Changes reversible (undo, time-travel, Git reload) | [CLAIM-edg-03][CLAIM-edg-08] |
| FR-4 | Models defined as shapes that also drive the UI | [CLAIM-edg-10] |
| NFR-1 | Java 21 / Tomcat 11; Linux or Windows Server 2022+; raised open-file limits | [CLAIM-edg-07] |
| NFR-2 | Sizing from a vendor-supplied document, not public | [CLAIM-edg-07] |
| NFR-3 | Storage engine choice immutable per workspace | [CLAIM-edg-06] |

## 7. Performance and resource model

No independent benchmark was found; documentation gives only qualitative scale guidance (internal TDB adequate to roughly tens of millions of triples, external stores beyond) [CLAIM-edg-06] and defers sizing to a guide "provided at purchase" [CLAIM-edg-07]. RAM, CPU and disk figures are **NOT PUBLICLY VERIFIED**. Failure modes: file-handle exhaustion without ulimit tuning; archive-on-commit discards detailed change records; fixed storage type forces re-import to change. A one-node footprint is a single Tomcat JVM plus TDB files — structurally modest but unmeasured.

## 8. Strengths and use-case-specific advantages

| ID | Strength | Route |
|---|---|---|
| STR-edg-01 | Governance workflow with isolated working copies, role-gated stages, templates stored as data | match: configurable per-tenant templates over `OntologyPullRequest` stages |
| STR-edg-02 | SHACL gate bound to the workflow, severity-based blocking | exceed: semantic-diff + SHACL gate in CI and review |
| STR-edg-03 | Shapes drive forms and UI (one schema artefact) | match later: generate Studio forms from the ontology manifest |
| STR-edg-04 | Sorted-Turtle Git round trip with minimal diffs | match immediately: canonical serialization is cheap and valuable |
| STR-edg-05 | External store support (GraphDB, Neptune), remote SPARQL | integrate: aligns with BL-04/BL-06 |
| STR-edg-06 | Time-travel and partial commit from change history (9.3.0) | match: BL-38 snapshots/playback is the substrate |

## 9. Limitations with root causes

| Class | Item | Root cause | Evidence |
|---|---|---|---|
| Intentional | Single-server Tomcat + TDB application | Monolith design | [CLAIM-edg-06][CLAIM-edg-07] |
| Op/hardware | Many TDB files; ulimit tuning; sizing gated | TDB layout | [CLAIM-edg-06][CLAIM-edg-07] |
| Op | Storage type immutable | TDB layout choice | [CLAIM-edg-06] |
| Algorithmic | No documented merge of overlapping workflows | Isolation without a merge model | [CLAIM-edg-05] |
| User friction | Branch switching outside UI (7.8 docs; 9.3 not shown to change it) | Git integration is file sync | [CLAIM-edg-08] |
| Licensing | Proprietary; no public pricing | Commercial model | — |
| Hypothesis | Slow time-to-value | Modelling and configuration burden | no evidence either way |

**Seed hypothesis §10.5 #2 — verdict: PARTIALLY VALIDATED; "slow time-to-value" NOT SUPPORTED.** "Monolithic server stack": supported — one Java/Tomcat application with embedded TDB [CLAIM-edg-06][CLAIM-edg-07]. "Heavy enterprise footprint": **not demonstrable** — no public sizing, and install requirements (Tomcat, Java, nofile limits) are modest; NOT PUBLICLY VERIFIED. "Complex configuration/slow time-to-value": no independent evidence collected. **Inversion premise "GitOps-native ontology-as-code with CI SHACL tests, semantic diff, release, rollback, plus visual editor on the same source":** EDG already ships Git sync with sorted Turtle, SHACL-gated workflows, rollback paths and (9.3) a visual ontology editor [CLAIM-edg-02][CLAIM-edg-03][CLAIM-edg-08]. EOIP's differentiator must be *Git as source of truth (not a sync target)*, CI-native, open formats, air-gap, white-label, backend-neutral — not the mere presence of Git.

## 10. Deployment, licensing, redistribution, operational viability

Self-hosted WAR on Tomcat; Linux or Windows Server; air-gap viable in principle (no mandatory cloud evidenced; GraphRAG/embedding provider egress NOT VERIFIED). Proprietary subscription: **cannot be embedded or white-labelled** without an OEM agreement — legal-review trigger. Reuse path: Apache-2.0 TopBraid SHACL API is redistributable (NOTICE obligations) [CLAIM-edg-10] and Jena-based, a JVM-sidecar candidate for CAP-10. Backend neutrality: RDF-only; labelled-property-graph backends (HugeGraph, Neo4j) unsupported. Multi-tenancy: UNKNOWN. HA: undocumented.

## 11. Competitive delta against EOIP baseline

| Topic | EDG | EOIP | Delta |
|---|---|---|---|
| SHACL (BL-29) | Complete engine, SHACL 1.2 features [CLAIM-edg-04] | Subset on in-memory store; pySHACL dependency absent | Deficit on conformance; REUSE TopBraid SHACL or pySHACL |
| Governance (BL-32) | Working copies, review, roles, templates, time-travel | `OntologyGitOpsWorkflow` branches/PRs/review/merge/rollback/SemVer (`gitops.py:220-735`) | Comparable stage coverage; EOIP keeps state in in-process dicts, no persistence or per-tenant templates; EDG is production-hardened |
| Semantic diff | triple-level report | additive/potentially_breaking/breaking classification of manifest changes | EOIP richer in classification, narrower in scope (label manifest, not RDF/OWL) |
| Rollback | undo, time travel, Git reload | `OntologyVersionStore.rollback_to_version` with receipts | Parity on concept; data-aware rollback not evidenced in EOIP |
| Git | sorted Turtle sync | no Git binding found in `gitops.py` | EOIP gap: persist as canonical files |
| Visual editing | present (9.3) | Studio redesign pending (BL-54) | Gap |
| Backend neutrality | RDF stores only | LPG + RDF adapters | EOIP ahead |

## 12. Strength-adoption cards and inversion cards

STR cards: section 8 (acceptance tests in section 14).

**INV-edg-01 — "Governance state locked in a proprietary server store; Git is a sync target."** Target EDG 9.3. Evidence [CLAIM-edg-08][CLAIM-edg-06]. Root cause: storage/governance coupling (*proven* by docs: collections live in internal TDB, Git needs a server-local clone). Alternative: Git (or a Git-like content-addressed store) as source of truth, review as PR, EOIP gate as CI check; worse when non-technical stewards need point-and-click without Git literacy. Options: (a) quick — canonical sorted-Turtle/YAML export plus `git` CLI wrapper; (b) pragmatic — persist `OntologyGitOpsWorkflow` as a real repository with signed commits and per-tenant branches; (c) long-term — visual editor producing commits with tenant-specific templates. Selected (b). Sketch: `edit → PR → CI(parse, SHACL, diff classify, impact report) → review gate → merge → SemVer tag → deploy`. POC: replay 200 changes of a public vocabulary; success = 100% of breaking changes flagged, CI under 60 s on one node; baseline = manual EDG-style cycle time (to be measured, licence needed). Risks: Git-hostile users; large-Turtle merge conflicts (mitigate with sorted serialization); per-tenant file permissions. Defensibility: tenancy, evidence and backend-neutral gates around the files. Decision: **ADOPT**.

**INV-edg-02 — "No documented merge model between concurrent workflows."** Evidence [CLAIM-edg-05]. Root cause: isolation without algorithmic merge (docs *proven*, mechanism hypothesis). Option (b): three-way semantic merge on parsed axioms using `diff_manifests`; auto-merge additive, escalate breaking. Metric: false-merge rate 0 on synthetic conflicts; resolution time versus manual. Decision: **EXPERIMENT**.

**INV-edg-03 — "Heavy footprint / slow time-to-value" (seed).** Evidence none. Decision: **REJECT as stated**; keep a measurable POC: time from empty install to first governed vocabulary published, EOIP versus an EDG trial (licence needed; not done).

## 13. Per-capability decisions

| CAP | Decision | Note |
|---|---|---|
| CAP-10 SHACL | REUSE | TopBraid SHACL API (Apache-2.0) or pySHACL; retire custom subset after W3C test suite |
| CAP-41 governance workflow | BUILD | Templates stored as data |
| CAP-35 branching/diff/merge | BUILD | Git-backed (INV-edg-01/02) |
| CAP-37 evolution/migration | BUILD | Already in `gitops.py`; extend |
| CAP-12 taxonomy/SKOS | INTEGRATE (see PoolParty, VocBench) | EDG proprietary |
| CAP-72 visual editing | EXPERIMENT | After UX study |
| CAP-59 MCP | DEFER | Compare read-only posture with BL-47 |
| CAP-02 RDF storage | REJECT | Do not copy a Jena-store monolith |

## 14. Tests, POC, acceptance

1. Run the W3C SHACL Core test suite against `ontology/shacl_validator.py` and TopBraid SHACL/pySHACL; publish pass rates.
2. Git round trip: 10k-triple vocabulary; canonical serialization gives single-line diffs for single-triple edits.
3. Workflow gate: SHACL violation blocks merge; warning permits with audit entry.
4. Concurrent edit: two branches touching one entity; merge classifier correct on 20 curated cases.
5. Rollback: publish v1.1.0, roll back to v1.0.0 with receipt; graph facts still validate or a migration script is produced.

## 15. Risks, trade-offs, open questions

- 9.x release dates inferred from file paths; confirm with vendor.
- 9.3 visual editor and Git behaviour verified only from headlines; a trial is needed (licence).
- Possible rename to TQ Data Foundation changes how buyers search for the competitor.
- Open: does EDG offer OWL reasoning, multi-tenancy, HA?
- Only patterns are adopted, never code.

## Appendix A — Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Private vendor, 9.3, proprietary |
| D2 | 2 | Enterprise vocab/ref-data/metadata governance |
| D3 | 4 | Single Tomcat app + TDB |
| D4 | 5 | Jena TDB, two layouts |
| D5 | 3, 5 | RDF 1.2, SHACL 1.2 |
| D6 | 5 | SPARQL/GraphQL; planner N/A (Jena) |
| D7 | 5 | SHACL rules; OWL unknown |
| D8 | 5, 7 | Single node; HA undocumented |
| D9 | 3 | External stores, Databricks catalog |
| D10 | — | N/A (governance, not entity resolution) |
| D11 | 5 | Change history, time-travel, Git |
| D12 | — | N/A |
| D13 | 2, 3 | GraphRAG, MCP |
| D14 | — | NOT ASSESSED |
| D15 | 2, 5 | Core strength |
| D16 | 3 | Forms, visual editor (9.3), WCAG |
| D17 | 3 | SDK, APIs |
| D18 | 5, 10 | Roles; tenancy unknown |
| D19 | 10 | Unknown |
| D20 | 7 | NOT PUBLICLY VERIFIED |
| D21 | 10 | Proprietary subscription |
| D22 | 10 | Standards-native, RDF-only |
| D23 | — | Not assessed |
| D24 | App C | Vendor docs; no independent benchmarks |

## Appendix B — Capability mapping

| CAP | Technology | Evidence | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-10 | native | edg-10 | BL-29 partial | REUSE | P1 |
| CAP-12 | native | edg-01 | absent | INTEGRATE | P2 |
| CAP-35 | partial | edg-05, 08 | BL-32 partial | BUILD | P1 |
| CAP-37 | partial | edg-04 | BL-32 partial | BUILD | P1 |
| CAP-41 | native | edg-05 | BL-32 partial | BUILD | P1 |
| CAP-72 | native (9.3) | edg-02 | BL-54 | EXPERIMENT | P2 |
| CAP-59 | native | edg-02 | BL-47 impl. | DEFER | P3 |
| CAP-56 | partial | edg-01 | BL-16 impl. | DEFER | P3 |

## Appendix C — Evidence records

| CLAIM-ID | product/version/date | exact claim | class | source + URL | pub / access | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-edg-01 | EDG 9.0 | GraphRAG chunking, vector+SPARQL in SPARQL/GraphQL APIs, Python SDK; notifications (off by default); RDF 1.2 reification; requires Java 21 and Tomcat 11 | Officially documented | https://www.topquadrant.com/release-note/9-0 | undated / 2026-10-26 | 0.85 | none |
| CLAIM-edg-02 | EDG 9.3 | Visual ontology editor, enterprise-ready Git integration, production MCP server, WCAG 2.2 AA, human-in-loop approval, Databricks catalog; change logs 9.3.0–9.3.2 | Officially documented | https://www.topquadrant.com/release-note/9-3/ | undated / 2026-10-26 | 0.8 | page gave no date |
| CLAIM-edg-03 | EDG 9.3.0 | GitHub App auth for Git (DEV-124); Change History button creates workflow from selected changes (DEV-332); "time travel workflow" (DEV-429) | Officially documented (via search summary of change log) | https://www.topquadrant.com/wp-content/uploads/2026/08/changes-9.3.0.txt | 2026-08 (path) / 2026-10-26 | 0.55 | direct fetch returned 404 |
| CLAIM-edg-04 | EDG 9.2 | Legacy reification removed; SHACL 1.2 features incl. `sh:unit`; migration automatic and undoable from change history; `edg-sdk` renamed `tq-client-lib` | Officially documented (via search summary) | https://topquadrant.com/release-note/9-2 ; https://www.topquadrant.com/wp-content/uploads/2026/05/changes-9.2.0.txt | 2026-05 (path) / 2026-10-26 | 0.6 | none |
| CLAIM-edg-05 | EDG 9.2 docs | Isolated working copies; Uncommitted → Frozen for Review → commit by production editor; templates by role/permission; SHACL via `teamwork:tagShape`, blocking via `teamwork:blockOnValidationSeverity`; no merge mechanism described; report shows affected workflows; archive removes detailed changes | Officially documented | https://docs.topquadrant.com/9.2/user_guide/workflows/index.html | undated / 2026-10-26 | 0.85 | none |
| CLAIM-edg-06 | EDG 7.2–8.4 docs | Internal DB based on Jena TDB; storage type fixed after selection; shared-graph vs per-graph TDB; about 30M triples remark; remote SPARQL from 7.7; GraphDB/Neptune RW from 7.8 | Officially documented | https://www.topquadrant.com/doc/8.3/administrator_guide/edg_installation_and_authentication/database_type_app_data_storage.html ; https://www.topquadrant.com/release-note/7-8/ | older / 2026-10-26 | 0.7 | may have changed in 9.x |
| CLAIM-edg-07 | EDG latest platform page | Java 21, Tomcat 11, Linux or Windows Server 2022+; no RAM figures (sizing guide at purchase); nofile soft 2048/hard 8192; HA not covered | Officially documented | https://docs.topquadrant.com/latest/administrator_guide/edg_installation_and_authentication/edg_server_platform_considerations.html | undated / 2026-10-26 | 0.85 | an older cached snippet said Java 17/Tomcat 10.1 |
| CLAIM-edg-08 | EDG 7.x docs | Git integration: import, reload, commit via server-local clone; sorted Turtle; branch switching outside UI | Officially documented (via search summary) | https://www.topquadrant.com/doc/7.8/reference/Manage_InGitRepository.html ; https://www.topquadrant.com/resources/feature-focus-git-integration/ | older / 2026-10-26 | 0.6 | 9.3 "enterprise-ready Git" may extend |
| CLAIM-edg-09 | TopQuadrant | Raleigh NC; founded 2001; TopBraid Suite 2007; co-authored SHACL; no acquisitions listed; owner not stated; TQ Data Foundation launched Feb 2026; EDG docs titled TQ Data Foundation; Composer replaced by EDG Studio | Officially documented | https://www.topquadrant.com/about-us/ ; search results for TQ Data Foundation | / 2026-10-26 | 0.7 | no press release on rename |
| CLAIM-edg-10 | TopBraid SHACL API | Apache-2.0, "SHACL API in Java based on Apache Jena", pushed 2026-06-30, not archived; same code used in TopBraid commercial products | Observed | https://api.github.com/repos/TopQuadrant/shacl ; https://github.com/TopQuadrant/shacl | 2026-06-30 / 2026-10-26 | 0.85 | none |

## Appendix D — Assumptions

- Access date is the actual 2026-10-26, not the brief's 2026-10-18.
- 9.2/9.3 dates are inferred from upload paths of change logs; low confidence.
- No trial instance available; all behaviour is from documentation.
- Entry treated as covering "TopBraid EDG / TQ Data Foundation / EDG Studio / TopBraid SHACL API".
