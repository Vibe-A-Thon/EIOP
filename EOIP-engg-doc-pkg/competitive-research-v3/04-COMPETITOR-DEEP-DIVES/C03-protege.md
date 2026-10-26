# C03 — Protégé (desktop) and WebProtégé

| Field | Value |
|---|---|
| Registry ID | T-C03-protege |
| Tier | A — market-reference ontology editor; target of Master Prompt §10.5 seed inversion #1 |
| Versions examined | Protégé Desktop 5.6.9 (2026-03-07, stable); Protégé 6.0.0-alpha-1 (2026-09-28, pre-release); WebProtégé GitHub release v4.0.2 (2020-07-31), `master` pom 5.0.0-SNAPSHOT; webprotege-deploy (no tags) |
| Verified on | 2026-10-26 (actual access date; brief said 2026-10-18 — see Appendix D) |
| Worker | V03 |

## 1. Identity, current status, tier, and sources

Two distinct products share a name and a team (Stanford BMIR). **Protégé Desktop** is a Java/Swing OWL 2 editor, BSD-2-Clause, with plugins [CLAIM-protege-01][CLAIM-protege-04]. **WebProtégé** is a separately deployed multi-user web ontology editor; the public GitHub release line stops at v4.0.2 (2020) while `master` carries 5.0.0-SNAPSHOT and the README says development moved to per-service repositories [CLAIM-protege-09]. Registry resolution: the registry row "Protégé and WebProtégé" means both; they are analysed separately where behaviour differs.

| Item | Verified state |
|---|---|
| Desktop cadence | 5.6.6 2025-05-23, 5.6.7 2025-08-09, 5.6.8 2025-09-03, 5.6.9 2026-03-07: maintenance-grade, bug-fix releases [CLAIM-protege-01] |
| Desktop next major | 6.0.0-alpha-1 (2026-09-28): OWL API 5.5.1, breaking for 5.x plugins, only a HermiT 1.5.0 snapshot bundled, no binary assets on the GitHub release [CLAIM-protege-02] |
| Runtime | 5.6.9 works with Java 11–25; platform builds still ship Java 11 [CLAIM-protege-01] |
| Activity | desktop repo pushed 2026-10-01, 446 open issues; webprotege repo pushed 2026-07-28, 359 open issues; neither archived [CLAIM-protege-05] |
| Licence | BSD-2-Clause, Stanford (both repos' `license.txt`); GitHub reports NOASSERTION only because it cannot classify the file name [CLAIM-protege-04] |
| Governance | Academic group; funding and bus-factor risk not verified (hypothesis only) |

## 2. Primary problem, target workloads, concrete example workflows

Authoring and inspection of OWL 2 ontologies (class hierarchies, axioms, annotations, imports) with DL reasoner feedback, dominated by biomedical and academic users. Workflows:

1. **Author-reason-fix** (desktop): open `.owl`/Turtle, edit axioms, run HermiT or ELK, read the unsatisfiable-class report, use the explanation service to find justifications.
2. **Community curation** (WebProtégé): project with roles, entity-attached threaded comments, watch lists, email notifications; edits visible to other users as they happen [CLAIM-protege-11].
3. **Git-centric curation** (desktop): ontology files in Git; Protégé 5.5+ displays branch/status; merge and diff happen in Git/ROBOT tooling, not Protégé [CLAIM-protege-08].

Not the target: enterprise taxonomy governance with approval states, SKOS-first thesaurus management, application serving, runtime validation.

## 3. Feature inventory

| Capability | Desktop 5.6.x | WebProtégé |
|---|---|---|
| OWL 2 editing (classes, properties, individuals, annotations, imports) | present | present |
| Reasoners | HermiT, ELK (bundled since 5.6.0) [CLAIM-protege-03]; others via plugin (Pellet/Openllet NOT VERIFIED) | UNKNOWN |
| Entailment explanation | present (explanation-service setting added 5.6.4) [CLAIM-protege-03] | UNKNOWN |
| SHACL authoring/validation | absent in core; plugin existence UNKNOWN | absent (UNKNOWN) |
| SKOS/taxonomy UI | absent (generic annotations) | absent |
| Multi-user concurrent editing | absent (single-file, single-user) | present: shared projects, live-visible edits; conflict mechanism undocumented [CLAIM-protege-11] |
| Comments/discussion | absent in core | present: entity-level threads, issue open/close, mentions, email [CLAIM-protege-11] |
| Revision history | via VCS only | present: change tracking, download of past revisions; revert not evidenced [CLAIM-protege-11] |
| Git integration | light: branch/status display (5.5+) [CLAIM-protege-08] | absent |
| Semantic diff / merge | absent | absent |
| Approval workflow / release | absent | absent |
| Plugin API | OSGi bundles over `protege-editor-owl`; 5.x plugins incompatible with 6.x [CLAIM-protege-02] | portlet UI extension on GWT [CLAIM-protege-09] |
| API/CLI/SDK | Java plugin API only | gateway + backend services; `webprotege-cli` for admin account [CLAIM-protege-09] |
| Auth | local desktop | Keycloak in the new deployment [CLAIM-protege-10] |
| Air-gap | yes | yes if self-hosted (operator pulls images) |

## 4. Architecture diagram

```
 DESKTOP                                        WEBPROTEGE (next-gen deployment, webprotege-deploy)
 ┌────────────────────────────┐                 browser (GWT UI)
 │ Swing UI + workspace tabs  │                    │
 │ plugins (OSGi bundles)     │                 nginx ─► keycloak (auth realm)
 │ protege-editor-owl         │                    │
 │   OWLModelManager          │                 gwt-ui-server ─► gwt-api-gateway ─(RabbitMQ IPC)─►
 │ OWL API (in-process        │                    ┌─ backend-service (core edit/commands)
 │  OWLOntology objects)      │                    ├─ authorization-service
 │ reasoner (HermiT/ELK)      │                    ├─ user-management-service
 │ JVM heap (jvm.conf)        │                    ├─ event-history-service
 └──────────┬─────────────────┘                    ├─ ontology-processing-service
            │ files (RDF/XML, Turtle, OBO…)        └─ initial-revision-history-service
            ▼                                       state: MongoDB (project/change data), MinIO (objects)
   local FS / optional Git working tree
```

Desktop has no control/data plane split. WebProtégé's control plane is the broker-mediated service bus plus Keycloak; data plane is MongoDB plus object storage [CLAIM-protege-10]. Message names and exact data placement are NOT PUBLICLY VERIFIED beyond the compose service table.

## 5. Under-the-hood reconstruction

**Data model.** The editing model is the OWL API object graph (`OWLOntology`, immutable `OWLAxiom` values, annotations as axioms). Protégé 5.6.x sits on OWL API 4.5.x; 6.0 migrates to 5.5.1 [CLAIM-protege-02][CLAIM-protege-03]. An ontology is a set of axioms, not a record store; the class tree is a derived view over `SubClassOf` axioms plus the reasoner's inferred hierarchy. Hypothesis (reasoned inference): the default OWL API implementation holds axioms and indexes in JVM memory, which is why heap is the scaling lever.

**Storage layout.** Desktop: whole-file load/save through OWL API parsers/serializers (RDF/XML, Turtle, OBO, Manchester, functional); XML catalogs resolve imports. WebProtégé: project state plus a change-set revision history; MongoDB confirmed in the README, revision and event services confirmed by name only [CLAIM-protege-09][CLAIM-protege-10]. Reconstruction (hypothesis): event sourcing, each edit a typed change (add/remove axiom, rename IRI) stored as an ordered revision; revision N = replay.

**Query pipeline.** No planner. Navigation uses OWL API indexes; DL queries are class expressions evaluated by the reasoner; SPARQL/SPARQL-DL via plugins (UNVERIFIED).

**Reasoning.** Open-world DL via pluggable `OWLReasoner`. HermiT (tableau, OWL 2 DL) and ELK (consequence-based, OWL 2 EL) are bundled in 5.6 [CLAIM-protege-03]; 6.0-alpha bundles HermiT only [CLAIM-protege-02]. Invoked on demand, results cached for the session. Complexity bounds follow the OWL 2 DL / EL profile definitions (derived, not measured).

**Concurrency/transactions.** Desktop: single writer. WebProtégé: live-visible edits [CLAIM-protege-11]; no locking, OT or CRDT documentation found. Inference: per-project serialised change application with revision numbers — NOT PUBLICLY VERIFIED. Documented collaboration style is a shared mutable project with an audit log, i.e. neither document locking, branching, nor CRDT by design.

**Partitioning/consistency.** None; one project is one logical ontology plus imports with a linear revision history.

**Caching.** Desktop: in-heap indexes and reasoner state. WebProtégé: undocumented.

**Versioning.** Desktop: delegated to Git [CLAIM-protege-08]. WebProtégé: revision history with downloadable snapshots [CLAIM-protege-11].

**Security.** Desktop: OS file permissions. WebProtégé: role-based project sharing; Keycloak and an authorization service in the new stack [CLAIM-protege-10]. Hosted service has tens of thousands of projects and accounts [CLAIM-protege-12], implying project-level not tenant-level separation (inference).

**Memory control.** 5.6+ picks a maximum heap from system RAM; override via `~/.Protege/conf/jvm.conf` (`max_heap_size=…`) [CLAIM-protege-06].

## 6. Functional and non-functional requirements inferred

| ID | Requirement | Basis |
|---|---|---|
| FR-1 | Author OWL 2 axioms with annotation and import management | [CLAIM-protege-01] |
| FR-2 | Pluggable DL reasoner with explanation | [CLAIM-protege-03] |
| FR-3 | Project sharing with roles, comments, watches, notifications | [CLAIM-protege-11] |
| FR-4 | Revision history with snapshot download | [CLAIM-protege-11] |
| NFR-1 | Whole ontology addressable in one process's memory (desktop) | [CLAIM-protege-06][CLAIM-protege-07] |
| NFR-2 | Plugin ABI stability across majors (broken at 6.0) | [CLAIM-protege-02] |
| NFR-3 | Self-hostable stack of about 14 containers for WebProtégé | [CLAIM-protege-10] |

## 7. Performance and resource model

No current benchmark with workload and hardware was found. The only scale statement on the Protégé wiki ("Scalability and Tuning") concerns the **frames-era Protégé 3.x** (about 100K frames in file mode with 2+ GB; database backend for larger; tested to 5M frames) and is an **outdated claim** for OWL 5.x [CLAIM-protege-07]. Heap is the binding resource; reasoner cost depends on profile (ELK scales on EL ontologies; HermiT can degrade on expressive axioms — general literature, not measured here). The hosted WebProtégé handles tens of thousands of projects [CLAIM-protege-12], which says nothing about per-ontology size. Failure modes: OOM on load, long classification, UI freezes (5.6.8 fixed "frequent freezes" on macOS) [CLAIM-protege-01]. All numbers: NOT PUBLICLY VERIFIED.

## 8. Strengths and use-case-specific advantages

| ID | Strength | Match/exceed route |
|---|---|---|
| STR-protege-01 | De facto OWL 2 authoring UX and ecosystem; BSD-2 permits embedding | integrate: customers can use Protégé against exported Turtle/OWL |
| STR-protege-02 | HermiT/ELK/explanation workflow gives justification-level feedback | integrate ELK/HermiT via an OWL API sidecar rather than extend `OWLReasoner` (BL-30) |
| STR-protege-03 | WebProtégé entity-level discussion, watches, notifications | match: entity threads in the stewardship flow (BL-32) |
| STR-protege-04 | Plugin model produced a long tail | reject copying; export ontology as files so the tail works |

## 9. Limitations with root causes

| Type | Item | Root cause | Evidence |
|---|---|---|---|
| Intentional trade-off | Desktop single-user, file-based | Editor over local files; sharing delegated to Git | [CLAIM-protege-08] |
| Operational/hardware | Ontology must fit JVM heap; manual tuning | In-memory OWL API model (hypothesis) | [CLAIM-protege-06] |
| Algorithmic | HermiT worst-case DL complexity | OWL 2 DL bounds | derived |
| User/dev friction | 6.0 breaks all 5.x plugins; alpha has only HermiT | OWL API 5 migration | [CLAIM-protege-02] |
| User/dev friction | WebProtégé release line stale (v4.0.2, 2020) while master is 5.0.0-SNAPSHOT | Microservice rewrite in progress | [CLAIM-protege-09] |
| Gap | No approval/release workflow, no semantic merge, no SHACL | Out of scope | [CLAIM-protege-11] |
| Outdated | "Scales to 5M frames" | Frames era | [CLAIM-protege-07] |
| User-reported | 2024 secondary comparison: WebProtégé hosting-bound, no text editing | Secondary, unverified | NOT VERIFIED |

**Seed hypothesis §10.5 #1 — verdict: PARTIALLY VALIDATED.** "Desktop-bound": validated for Desktop, **rejected product-wide** because WebProtégé is a self-hostable multi-user web editor [CLAIM-protege-10][CLAIM-protege-11]. "Effectively single-user": validated for Desktop, rejected for WebProtégé. "Struggles beyond client RAM": plausible and consistent with heap-tuning guidance, but **no current measurement exists** and the only scale page is outdated. "In-memory model, no storage abstraction": hypothesis, not source-proven here. Note: WebProtégé's own rewrite moves towards the headless service architecture the seed proposes — convergence risk.

## 10. Deployment, licensing, redistribution, operational viability

BSD-2-Clause: redistributable and embeddable with attribution; low legal-review need for Protégé itself. Desktop runs offline, no cloud dependency. WebProtégé: Docker Compose stack of 14 services including Keycloak, MongoDB, RabbitMQ, MinIO, nginx [CLAIM-protege-10] — heavy for one-node-first and not backend-neutral. Transitive licences (believed, UNVERIFIED this session): OWL API LGPL/Apache dual, HermiT LGPL, ELK Apache-2, Pellet/Openllet AGPL — **legal-review trigger** for any reasoner bundled into EOIP. Multi-tenancy/white-label: not supported. Air-gap: viable.

## 11. Competitive delta against EOIP baseline

| Topic | Protégé / WebProtégé | EOIP | Delta |
|---|---|---|---|
| OWL reasoning (BL-30) | HermiT/ELK complete for their profiles [CLAIM-protege-03] | subclass/disjoint/property-chain only (`ontology/rdf.py:598`) | Competitive deficit; INTEGRATE not BUILD |
| SHACL (BL-29) | Absent in core | In-house subset; pySHACL dependency absent | EOIP ahead on validation, behind on conformance |
| Governance (BL-32) | Revision log (Web) only | `OntologyGitOpsWorkflow`: branches, PRs, SemVer, rollback receipts (`ontology/gitops.py:220,635`) | EOIP ahead on workflow breadth, but works on the label manifest and keeps branches in a Python `dict` (in-process), not OWL/Turtle files |
| Collaboration (BL-53) | WebProtégé live multi-user, comments | Annotations/workspaces, no co-editing | Gap on live editing (CAP-72) |
| Authoring UX (BL-54) | Mature | React Studio | Gap on OWL-aware visual authoring |
| Interchange (BL-31) | OWL/RDF/OBO native | JSON-LD with loss accounting | No OWL/Turtle file round-trip evidenced |

## 12. Strength-adoption cards and inversion cards

STR cards: section 8 (acceptance tests in section 14).

**INV-protege-01 — "Desktop-bound, in-memory ontology editing."** Target: Protégé Desktop 5.6.9. Limitation: ontology must fit one JVM heap; manual tuning [CLAIM-protege-06]. Root cause: in-memory OWL API model (*hypothesis*). The alternative keeps the canonical ontology as sorted Turtle in Git with server-side indexes; worse when authors need full DL classification locally. Options: (a) quick — treat Protégé as an external editor over exported OWL/Turtle; (b) pragmatic — ELK-class reasoning sidecar plus EOIP stewardship workflow; (c) long-term — headless ontology service over an out-of-core axiom store plus visual editor. Selected (a)+(b). Sketch: `Turtle in Git → CI: parse + SHACL + ELK classify → diff report → release`. POC: classify a public ≥1M-axiom EL ontology (dataset to pin) in Protégé at default heap versus the sidecar; metrics time-to-classify and peak RSS; baseline Protégé 5.6.9 on a 16 GB laptop. Risks: reasoner licensing; tenant leakage if sidecar is shared; backward compatibility via file export only. Defensibility: ontology bound to permissions, evidence and multi-backend graph. Decision: **EXPERIMENT**.

**INV-protege-02 — "No branch/merge or review beyond Git text diff."** Evidence [CLAIM-protege-08][CLAIM-protege-11]. Root cause: governance (out of scope). Selected: pragmatic — extend `gitops.py` from label manifest to axiom-level semantic diff over parsed Turtle. Metric: at least 95% of curator-labelled breaking changes in a 200-commit public ontology history classified breaking (target to validate). Decision: **ADOPT** (builds on BL-32).

**INV-protege-03 — "WebProtégé stack weight and stalled release line."** Evidence [CLAIM-protege-09][CLAIM-protege-10]. Decision: **REJECT** as dependency; **DEFER** as inspiration.

## 13. Per-capability decisions

| CAP | Decision | Note |
|---|---|---|
| CAP-09 ontology modelling | INTEGRATE | Interchange files so Protégé works against EOIP; no OWL authoring UI first |
| CAP-23 OWL profile reasoning | INTEGRATE | ELK (EL) and HermiT via sidecar behind licence review; keep BL-30 for light checks |
| CAP-24 explanation traces | EXPERIMENT | OWL API justifications from sidecar |
| CAP-35 branching/diff/merge | BUILD | Extend BL-32 to axiom level |
| CAP-37 ontology evolution | BUILD | Same |
| CAP-41 governance workflow | BUILD | Add entity review threads |
| CAP-72 visual editing, co-editing | DEFER | After TopBraid/metaphactory study; CRDT unproven here |
| CAP-12 SKOS | REJECT as a Protégé feature | see PoolParty |

## 14. Tests, POC, acceptance

1. Round-trip: export EOIP ontology to Turtle/OWL, open in Protégé 5.6.9, re-import; zero axiom loss (extends BL-31 loss accounting).
2. Sidecar: ELK classification of a ≥1M-axiom EL ontology within a pinned budget on a one-node 16 GB host; record RSS.
3. Reasoner parity: differential test of `ontology/rdf.py` reasoner versus ELK on subclass/disjoint/chain cases; mismatches are failures.
4. Semantic diff: replay a public ontology's commit history; compare classification with human labels.
5. Co-editing spike (only if CAP-72 is prioritised): two-client concurrent-edit test comparing optimistic revision numbers with CRDT on conflict rate.

## 15. Risks, trade-offs, open questions

- Protégé 6 transition may fragment the plugin ecosystem; track alpha to beta.
- WebProtégé concurrency model is undocumented; read `webprotege-backend-service` source before any co-editing design.
- Reasoner and OWL API licences must be pinned by legal.
- Funding stability of the academic project: not verified.
- Open: does a maintained Protégé SHACL plugin exist? Not verified.

## Appendix A — Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | BSD-2, active maintenance, 6.0 alpha |
| D2 | 2 | Biomedical/academic OWL authoring |
| D3 | 4, 5 | Swing+OSGi; WebProtégé 14-service stack |
| D4 | 5 | In-heap OWL API; Mongo for Web (partial) |
| D5 | 3, 5 | OWL 2 DL; no SHACL |
| D6 | 5 | N/A — no query engine; DL queries via reasoner |
| D7 | 5, 9 | HermiT/ELK; on demand |
| D8 | 5 | N/A for desktop; Web undocumented |
| D9 | 3 | File import only |
| D10 | — | N/A — not an identity/evidence system |
| D11 | 3, 5 | Revision log (Web); Git (desktop) |
| D12 | — | N/A |
| D13 | — | N/A (no agent/MCP evidence) |
| D14 | — | N/A |
| D15 | 3, 8, 9 | Comments/watches; no approvals |
| D16 | 3 | Mature tree UI; no large-graph viz |
| D17 | 3, 5 | Plugin API; breaking at 6.0 |
| D18 | 5, 10 | Keycloak in new stack; tenancy undocumented |
| D19 | 10 | Absent |
| D20 | 7 | No measurements; NOT PUBLICLY VERIFIED |
| D21 | 10 | Free, BSD |
| D22 | 11 | Native OWL/OBO; strong portability |
| D23 | — | Not assessed |
| D24 | 7, App C | Official plus secondary; some outdated |

## Appendix B — Capability mapping

| CAP | Technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-09 | native | protege-01 | BL-30 partial | INTEGRATE | P2 |
| CAP-23 | native/plugin | protege-03 | BL-30 partial | INTEGRATE | P2 |
| CAP-24 | native | protege-03 | Absent | EXPERIMENT | P3 |
| CAP-10 | absent | protege-01 | BL-29 partial | n/a | — |
| CAP-35 | absent (Git) | protege-08 | BL-32 partial | BUILD | P1 |
| CAP-37 | absent | protege-08 | BL-32 partial | BUILD | P1 |
| CAP-41 | partial (Web comments) | protege-11 | BL-32 partial | BUILD | P1 |
| CAP-72 | partial (Web live edit) | protege-11 | BL-53 impl., no co-edit | DEFER | P3 |

## Appendix C — Evidence records

| CLAIM-ID | product/version/date | exact claim | class | source + URL | pub / access | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-protege-01 | Protégé 5.6.9, 2026-03-07 | Release adds label/ontology-selector options; works with Java 11–25, platform builds ship Java 11; 5.6.8 fixed frequent freezes; 5.6.6–5.6.9 dated 2025-05-23 to 2026-03-07 | Officially documented | https://api.github.com/repos/protegeproject/protege-distribution/releases | 2026-03-07 / 2026-10-26 | 0.85 (fetch summariser) | none |
| CLAIM-protege-02 | 6.0.0-alpha-1, 2026-09-28 | Pre-release; OWL API 5(.5.1); incompatible with 5.x plugins; only HermiT 1.5.0 snapshot bundled; no assets | Officially documented | https://api.github.com/repos/protegeproject/protege/releases/tags/6.0.0-alpha-1 | 2026-09-28 / 2026-10-26 | 0.85 | none |
| CLAIM-protege-03 | 5.6.0–5.6.4 | 5.6.0 migrated to Java 11, OWL API 4.5.24, bundled ELK; 5.6.3 to 4.5.26; 5.6.4 to 4.5.29, ELK plugin 0.6.0, explanation-service setting | Officially documented (via search summary of release notes) | https://github.com/protegeproject/protege-distribution/releases/tag/protege-5.6.0 | 2020–2024 / 2026-10-26 | 0.6 | none |
| CLAIM-protege-04 | both repos | BSD-2-Clause, Stanford 2014 | Observed in source | https://raw.githubusercontent.com/protegeproject/protege/master/license.txt ; …/webprotege/master/license.txt | n/a / 2026-10-26 | 0.9 | GitHub SPDX NOASSERTION |
| CLAIM-protege-05 | repos | protege pushed 2026-10-01, 446 open issues; webprotege pushed 2026-07-28, 359 issues; neither archived | Observed | https://api.github.com/repos/protegeproject/protege ; …/webprotege | / 2026-10-26 | 0.85 | none |
| CLAIM-protege-06 | Protégé 5.6+ | Max heap auto-chosen from RAM; override in `~/.Protege/conf/jvm.conf` `max_heap_size` | Officially documented (via search summary) | https://protegewiki.stanford.edu/wiki/Setting_Heap_Size | UNVERIFIED / 2026-10-26 | 0.55 | exact file name unconfirmed |
| CLAIM-protege-07 | Protégé 3.x frames | About 100K frames file-based with 2+ GB; DB backend for larger; tested 5M frames | Officially documented, outdated | https://protegewiki.stanford.edu/wiki/Scalability_and_Tuning | undated / 2026-10-26 | 0.8 that page says this; 0.2 that it applies to 5.x | predates OWL 5.x |
| CLAIM-protege-08 | Protégé 5.5 | Lightweight Git integration shows branch/status; collaboration is Git-level | Third-party report (ICBO 2018) | https://ceur-ws.org/Vol-2285/ICBO_2018_paper_23.pdf (via search summary; PDF unreadable to fetcher) | 2018 / 2026-10-26 | 0.5 | later versions may extend |
| CLAIM-protege-09 | WebProtégé repo | Java/GWT/Maven; MongoDB; README: moving to microservices in per-service repos; latest GitHub release v4.0.2 2020-07-31; master pom 5.0.0-SNAPSHOT | Observed | https://github.com/protegeproject/webprotege ; releases API | / 2026-10-26 | 0.85 | none |
| CLAIM-protege-10 | webprotege-deploy | 14 services: nginx, keycloak, mongo, rabbitmq, minio, mailpit, gwt-api-gateway, gwt-ui-server, backend, authorization, user-management, event-history, ontology-processing, initial-revision-history | Observed in source | https://github.com/protegeproject/webprotege-deploy | / 2026-10-26 | 0.8 | image tags not shown |
| CLAIM-protege-11 | WebProtégé 4 | Threaded entity comments, watches, notifications, revision download; edits visible live; no conflict mechanism or revert described | Officially documented (via search summary of paper and user guide) | https://arxiv.org/pdf/1902.08251v2.pdf ; https://protegewiki.stanford.edu/wiki/WebProtegeUsersGuide | 2019 / 2026-10-26 | 0.55 | revert may exist undocumented |
| CLAIM-protege-12 | WebProtégé paper | Hosted service supports tens of thousands of ontology projects and accounts | Officially documented | https://arxiv.org/abs/1902.08251 | 2019-02-21 / 2026-10-26 | 0.8 | 2019 figure |

## Appendix D — Assumptions

- Access date recorded as the real date 2026-10-26 rather than the brief's 2026-10-18; no claim depends on the difference.
- Where a fetch summariser could not read a PDF or page, confidence is at most 0.6 and the claim is labelled.
- Third-party licences (OWL API, HermiT, ELK, Pellet/Openllet) are background knowledge, marked UNVERIFIED.
- Registry "Protégé and WebProtégé" treated as one entry with two sub-products.
