# C03 — metaphactory (metaphacts GmbH, a Digital Science company)

| Field | Value |
|---|---|
| Registry ID | T-C03-metaphactory |
| Tier | A — knowledge-graph application, modelling and governance platform; closest commercial analogue to an "ontology + app + AI" layer |
| Versions examined | 5.4 (2024-07-10), 5.7 (2025-03-31), 5.9 (2025-10-13), 5.10 (2026-01-12), 5.11 (2026-03-31), 6.0 (2026-07-14), 6.1 (general availability 2026-09-30) |
| Verified on | 2026-10-26 (actual access date; brief said 2026-10-18 — see Appendix D) |
| Worker | V03 |

## 1. Identity, current status, tier, and sources

metaphactory is the product of **metaphacts GmbH** (Walldorf, Germany), acquired by **Digital Science** (announced 2023-01-23; metaphacts continues as an independent entity) [CLAIM-mph-01]. On 2026-09-23 the company announced "metaphacts is now metaphactory" with a new site; on 2026-03-25 Digital Science acquired **Ontopic** (headline only; whether Ontopic is the commercial vehicle of the Ontop OBDA engine, cross-ref C04 `ontop`, is NOT VERIFIED here) [CLAIM-mph-01]. Product positioning in 2026: "the semantic intelligence layer for enterprise AI" — modelling, mapping and virtualised access plus an AI assistant (**metis**) [CLAIM-mph-02].

| Item | Verified state |
|---|---|
| Latest | 6.1 (2026-09-30) [CLAIM-mph-04] |
| Cadence | 5.4 (2024-07), 5.5, 5.7 (2025-03), 5.9 (2025-10), 5.10 (2026-01), 5.11 (2026-03), 6.0 (2026-07), 6.1 (2026-09): roughly quarterly, accelerating [CLAIM-mph-03][CLAIM-mph-04] |
| Licence | Current: proprietary subscription; terms NOT PUBLICLY VERIFIED. Historical: a third-party Docker Hub page describes the 4.1.0 community platform as LGPL 2.1 + Commons Clause (about five years old) [CLAIM-mph-09]. No current public source repository for the platform is in the vendor's GitHub org listing (only deployment, samples and helper repos) [CLAIM-mph-08] |
| Customers | Vendor-named: Boehringer Ingelheim, Bosch, Siemens, IKEA, Schaeffler — marketing [CLAIM-mph-02] |
| Partnership | SAP HANA Cloud Knowledge Graph Engine integration announced 2026-05-12; "now available on SAP Store" 2026-10-07 [CLAIM-mph-07] |

## 2. Primary problem, target workloads, concrete example workflows

Model enterprise meaning once (ontologies, vocabularies, business objects), map it to data, serve it to people and AI. Example workflows:

1. **Visual ontology modelling with AI**: real-time collaborative Visual Ontology Editor with metis suggestions; changes are previewed and confirmed on the canvas [CLAIM-mph-03][CLAIM-mph-04].
2. **Vocabulary governance**: term-level provenance (PROV-O), editorial states (development, ready for review, in review, accepted for publication), review comments [CLAIM-mph-05].
3. **Model–Map–Access**: map relational/JSON schemas to ontology; virtualised queries over Snowflake, Databricks, BigQuery, Redshift without copying [CLAIM-mph-02][CLAIM-mph-03].
4. **Schema change governance (6.1)**: schema snapshots, re-import flags renamed columns/dropped tables, governance agent recommends mapping updates [CLAIM-mph-04].
5. **Question answering**: NL-to-SPARQL and Search & Discovery agent grounded in the ontology [CLAIM-mph-06].

## 3. Feature inventory

| Capability | State | Notes |
|---|---|---|
| Visual ontology editor (OWL, SHACL-based modelling per vendor) | present | real-time concurrent editing in beta from 5.11 [CLAIM-mph-03] |
| Vocabulary editor, SKOS-XL labels | present | [CLAIM-mph-06] |
| SHACL | present (positioned as supported standard) | enforcement depth NOT VERIFIED [CLAIM-mph-02][CLAIM-mph-07] |
| Editorial states, review comments, threaded comments | present | [CLAIM-mph-05] |
| Ontology element version pages | present (5.4) | [CLAIM-mph-05] |
| Schema/mapping version history, snapshots | present (6.1) | [CLAIM-mph-04] |
| Release management, branch, rollback | NOT FOUND | 6.1 article does not cover [CLAIM-mph-04] |
| Concurrent editing | beta, mechanism undisclosed | [CLAIM-mph-03] |
| Data mapping and virtualisation (JDBC) | present (6.0/6.1) | [CLAIM-mph-03][CLAIM-mph-04] |
| Federation engine (transparent federation) | present | model-driven source selection [CLAIM-mph-05] |
| Excel vocabulary import | present (5.11) | [CLAIM-mph-03] |
| Knowledge extraction/annotation from documents | beta/present (6.0 beta, 6.1) | [CLAIM-mph-03][CLAIM-mph-04] |
| LLM: NL2SPARQL, metis assistant and agents, embedding search (beta) | present; providers named GPT-5.1/5.2, Gemini 3 Pro; local model support NOT confirmed | [CLAIM-mph-06] |
| RDF 1.2 / SPARQL 1.2 annotated statements | present (6.0) | [CLAIM-mph-03] |
| Database-level ACL | experimental (5.9) | enforced natively "if the graph database supports it" [CLAIM-mph-06] |
| Low-code app building, templates, diagrams, query catalog | present | [CLAIM-mph-05][CLAIM-mph-03] |
| API / SDK | SDK for apps (sample-apps repo); REST NOT VERIFIED | [CLAIM-mph-08] |
| Kubernetes/Docker | Helm charts and compose repos, actively pushed | [CLAIM-mph-08] |

## 4. Architecture diagram

```
 browser  ─ app framework (templates, components, visual ontology editor, query catalog, diagrams)
     │
 metaphactory server (Java web platform; app/config store)  ── metis: LLM assistants/agents ──► external LLM APIs (GPT/Gemini; local: unconfirmed)
     │  ├─ ontology/vocabulary governance (editorial states, PROV-O, versions)
     │  ├─ mapping + virtualisation engine (schema→ontology) ── JDBC ──► Snowflake/Databricks/BigQuery/Redshift/RDBMS
     │  └─ federation (declarative source selection)
     │ SPARQL
     ▼
 RDF repository: RDF4J-class / external triple store; named partner: SAP HANA Cloud KG Engine; other stores NOT VERIFIED here
```
[CLAIM-mph-02][CLAIM-mph-07]. State: ontology/vocabulary graphs, provenance and app content live in the underlying RDF repository; platform configuration and app files in platform storage (layout NOT PUBLICLY VERIFIED). Deployment: self-managed via Docker or AWS Marketplace, or hosted trial [CLAIM-mph-07].

## 5. Under-the-hood reconstruction

Public evidence for internals is marketing and release articles; code is closed. Everything below is labelled accordingly.

**Data model.** RDF/OWL with SHACL shapes; vocabulary terms with SKOS-XL labels; editorial state and review decisions stored as triples with PROV-O provenance at term level [CLAIM-mph-05][CLAIM-mph-06]. 6.0 adds RDF 1.2 triple annotations ("statements about statements") [CLAIM-mph-03]. Hypothesis: state machine per term as a property with a transitions log in a provenance named graph.

**Storage and indexing.** Delegated to the connected triple store; the platform itself is store-agnostic in positioning (historic RDF4J/Blazegraph-class lineage not verified now). The 5.9 database-level ACL feature depends on the store [CLAIM-mph-06]. Embedding-based retrieval (5.10 beta) implies a vector index; its location is NOT PUBLICLY VERIFIED [CLAIM-mph-06].

**Query pipeline.** SPARQL against repositories; federation engine selects sources using declarative model-driven knowledge (source descriptions in the ontology), improved in 5.4 [CLAIM-mph-05]. For virtual KG: mapping → query rewriting to SQL over JDBC (OBDA pattern, cross-ref Ontop); engine specifics NOT PUBLICLY VERIFIED. NL2SPARQL: generated SPARQL is validated against the ontology before execution (5.9) [CLAIM-mph-06] — a design pattern directly relevant to EOIP's "typed bounded query plan" principle.

**Reasoning.** Not a reasoner; relies on store (UNKNOWN).

**Concurrency.** Real-time concurrent editing in a "Google Docs-like environment", beta, first phase of several [CLAIM-mph-03]. Mechanism (OT, CRDT, locking) is not disclosed; honest classification: NOT PUBLICLY VERIFIED. Editorial states provide coarse coordination at term level [CLAIM-mph-05].

**Versioning.** (a) ontology element pages versioned (5.4); (b) term-level provenance with comparison from whole vocabulary down to a term (5.7); (c) schema snapshots and version history with mapping impact flags (6.1) [CLAIM-mph-05][CLAIM-mph-04]. No branch/merge/release/rollback is claimed. The governance agent assesses schema-change impact and recommends; in 6.1 humans apply changes, with auto-apply a stated future vision [CLAIM-mph-04].

**Caching.** NOT PUBLICLY VERIFIED.

**Security.** Platform roles plus experimental native DB ACL pass-through [CLAIM-mph-06]; tenant isolation NOT PUBLICLY VERIFIED.

**AI integration shape.** metis modelling assistant makes proposals that are previewed and confirmed (optional auto-mode in 6.1) — i.e. proposal-before-mutation, which matches EOIP's PROPOSED-until-promoted boundary (BL-40) [CLAIM-mph-04][CLAIM-mph-06].

## 6. Functional and non-functional requirements inferred

| ID | Requirement | Basis |
|---|---|---|
| FR-1 | Term-level editorial state machine with PROV-O provenance and review comments | [CLAIM-mph-05] |
| FR-2 | AI proposals shown as diffs on canvas; confirm before applying | [CLAIM-mph-04][CLAIM-mph-06] |
| FR-3 | Schema snapshot comparison with mapping-impact detection | [CLAIM-mph-04] |
| FR-4 | Generated queries validated against the ontology | [CLAIM-mph-06] |
| FR-5 | Virtualised access without data copy | [CLAIM-mph-03] |
| NFR-1 | Containerised deployment; Helm charts | [CLAIM-mph-08] |
| NFR-2 | Store-native ACL enforcement where available | [CLAIM-mph-06] |

## 7. Performance and resource model

No benchmark, hardware sizing, or latency figures were found in public material. Vendor-reported outcomes are business claims (e.g., break-even under two years at a utility; 1,500 processing hours saved at an energy company) with no workload context — marketing, not performance evidence [CLAIM-mph-02]. Resource model: platform server plus triple store plus optional LLM endpoints; virtualised queries inherit source warehouse latency/cost. Failure modes (hypotheses): LLM latency and cost on agents; federated query slowness; beta concurrency features. All numeric performance: NOT PUBLICLY VERIFIED.

## 8. Strengths and use-case-specific advantages

| ID | Strength | Route |
|---|---|---|
| STR-mph-01 | Proposal-preview-confirm AI modelling on a visual canvas | match: render EOIP ontology proposals (BL-27) as semantic diffs for approval |
| STR-mph-02 | Ontology-validated generated queries (NL2SPARQL) | match/exceed: validate NL queries against typed QueryPlan templates (BL-08, BL-12) |
| STR-mph-03 | Term-level PROV-O provenance and editorial states | match: ontology term provenance in stewardship; link to evidence (BL-41) |
| STR-mph-04 | Schema-change governance: snapshot diff with mapping impact | exceed: connect to `run_ontology_impact_analysis` (`gitops.py:412`) and CML mappings (BL-33) |
| STR-mph-05 | Unified Model–Map–Access flow and Excel onboarding | match: low-effort onboarding path |
| STR-mph-06 | Native DB ACL pass-through | cross-check with BL-18 source-ACL gap |
| STR-mph-07 | Real-time collaborative ontology editor | DEFER; mechanism undisclosed |

## 9. Limitations with root causes

| Class | Item | Root cause | Evidence |
|---|---|---|---|
| Licensing | Proprietary; community edition history unclear | Commercial/open-core shift | [CLAIM-mph-09][CLAIM-mph-08] |
| Op | LLM features named for external hosted models; local-model support not stated | Cloud-AI-first | [CLAIM-mph-06] |
| Maturity | Concurrent editing (beta), semantic annotation (beta), embedding search (beta), DB ACL (experimental) | Fast release cycle | [CLAIM-mph-03][CLAIM-mph-06] |
| Governance | No branch/merge/release/rollback claimed | Versioning scoped to terms, elements and schemas | [CLAIM-mph-04] |
| Coupling | Increasing coupling to SAP HANA Cloud and Digital Science datasets | Partnership strategy | [CLAIM-mph-07] |
| User friction | Brand and URL churn (metaphacts → metaphactory; docs moved) | Rebrand | [CLAIM-mph-01] |

No §10.5 seed targets metaphactory; none validated or rejected.

## 10. Deployment, licensing, redistribution, operational viability

Self-managed via Docker/Helm (vendor-published repos without detected licence files) or AWS Marketplace; hosted trial; SAP Store route [CLAIM-mph-07][CLAIM-mph-08]. Air-gap: containers are self-hostable, but the documented LLM providers are external APIs, so air-gap with AI features is NOT VERIFIED; core modelling without AI plausibly viable. Egress policy: metis agents need an explicit local-model path to satisfy EOIP's default. Proprietary licence: no OEM/white-label rights evidenced — **legal-review trigger**, plus the historical LGPL + Commons Clause note (a Commons Clause is a source-available restriction on selling; legal to confirm whether any such code is still in circulation) [CLAIM-mph-09]. Backend neutrality: RDF stores; LPG backends unsupported.

## 11. Competitive delta against EOIP baseline

| Topic | metaphactory | EOIP | Delta |
|---|---|---|---|
| Ontology proposal + approval (BL-27, BL-32, BL-40) | AI proposals, preview/confirm, editorial states | Ontology induction schema + module, PROPOSED-until-promoted, PR-style workflow | Conceptually aligned; EOIP governance not end-to-end and lacks a UI |
| SHACL (BL-29) | positioned support | in-house subset | UNKNOWN depth on their side |
| Collaboration (BL-53) | real-time beta + comments | annotations/workspaces, no co-editing | Gap on live editing |
| Provenance (BL-41) | term-level PROV-O | evidence manifests, lineage | Comparable; EOIP has evidence spans and claims (BL-39) beyond |
| Mapping/virtualisation (BL-33, BL-51) | JDBC virtual KG + schema snapshots | CML→IR, federation planner (partial) | EOIP behind on schema-drift governance |
| NL query safety (BL-08, BL-12) | validate vs ontology | typed templates | EOIP safer by construction, less flexible |
| ACL (BL-18) | experimental native pass-through | Absent in retrieval | EOIP P0 gap independent of competitor |
| Packaging | product + SDK apps | white-label platform | EOIP ahead on OEM/white-label if achieved |

## 12. Strength-adoption cards and inversion cards

STR cards: section 8 (acceptance tests in section 14).

**INV-mph-01 — "No release/branch/rollback for the semantic layer; AI auto-apply is only a vision."** Target: metaphactory 6.1. Evidence [CLAIM-mph-04]. Root cause: governance/versioning scope (*proven* from article's omissions, mechanism hypothesis). Alternative: treat the semantic layer (ontology + mappings + shapes) as one versioned bundle with SemVer, impact report and rollback. Worse when business users want instant ad-hoc edits. Options: (a) quick — export ontology + CML mappings to a repo with `diff_manifests`; (b) pragmatic — bundle manifest + mapping IR + SHACL shapes into a release unit in `OntologyVersionStore`; (c) long-term — schema-drift agent proposing mapping fixes that go through the same PR gate. Selected (b), later (c). Sketch: `schema snapshot Δ → impacted mappings (CML) → proposed fix → PR → CI → release`. POC: 20 scripted schema changes (rename, drop, type change) on a sample relational source; metric: 100% of impacted mappings flagged, false-positive rate < 10%, rollback restores byte-identical bundle; baseline: manual review time. Risks: mapping semantics drift; tenant-scoped mappings; permission to read schemas. Defensibility: ties to evidence, tenancy, offline operation. Decision: **EXPERIMENT**.

**INV-mph-02 — "AI assistants assume hosted LLM APIs."** Evidence [CLAIM-mph-06]. Root cause: deployment/coupling (*proven for named providers; local support unconfirmed*). Alternative: local-first model abstraction with egress gateway (BL-45) and ontology-validated outputs. Worse when hosted models materially outperform local ones on modelling suggestions. Options: (a) quick — expose proposals through MCP to any client under policy; (b) pragmatic — local-model modelling assistant with PROPOSED status; (c) long-term — evaluated assistant with LLM-as-judge regression suite. Metric: accepted-proposal rate and edit distance versus human gold on a 50-class domain. Decision: **ADOPT** (pattern), measurement via **EXPERIMENT**.

**INV-mph-03 — "Beta co-editing with undisclosed semantics."** Decision: **DEFER**; revisit after sources disclose mechanism.

## 13. Per-capability decisions

| CAP | Decision | Note |
|---|---|---|
| CAP-41 governance workflow | BUILD | editorial states per term/element |
| CAP-37 evolution/migration | BUILD | include mapping + schema snapshots |
| CAP-29 declarative mapping | REUSE (Ontop/RML tooling per C04) | do not copy platform |
| CAP-21 federation/virtualisation | EXPERIMENT | hybrid virtualise vs materialise (seed #8) |
| CAP-58 NL→query | BUILD | validate against ontology + typed plans |
| CAP-72 visual/co-editing | DEFER | |
| CAP-38 provenance | BUILD | PROV-O term-level export |
| CAP-12 SKOS | INTEGRATE | SKOS-XL import/export |
| CAP-46 source-ACL | BUILD (P0) | independent of competitor |
| CAP-77 licensing/TCO | REFERENCE | not embeddable |

## 14. Tests, POC, acceptance

1. Proposal workflow: LLM-proposed ontology change appears as a semantic diff, unapplied until approver confirms; audit entry created.
2. NL query validation: 100 generated queries; 0 execute outside allowed labels/relations (typed plan).
3. Schema drift: 20 scripted changes; impacted mappings flagged; release bundle rollback exact.
4. Term provenance: every accepted term carries author, time, source, decision; export valid PROV-O (round-trip with an RDF validator).
5. Air-gap: all above pass with network disabled using a local model.

## 15. Risks, trade-offs, open questions

- Vendor trajectory toward SAP and Digital Science ecosystems may reduce neutrality.
- Ontopic acquisition may affect the open-source Ontop project's direction (verify, cross-ref C04).
- Release notes are marketing-grade; the real changelog at help.metaphacts.com could not be fetched (page returned only a title) — re-check.
- Concurrency semantics, store compatibility list, HA, multi-tenancy: unverified.
- Licence of any current community distribution: unverified.

## Appendix A — Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Digital Science, quarterly releases, proprietary |
| D2 | 2 | Modelling, governance, virtual KG, AI |
| D3 | 4 | Platform + triple store + JDBC + LLM |
| D4 | 5 | Delegated to store; vector index unknown |
| D5 | 3, 5 | OWL/SHACL/SKOS-XL/RDF 1.2 |
| D6 | 5 | SPARQL, federation, NL2SPARQL; internals unknown |
| D7 | 5 | Not a reasoner |
| D8 | 5, 7 | Not documented |
| D9 | 2, 3 | JDBC virtual KG, Excel, annotation |
| D10 | 5 | Provenance yes; ER N/A |
| D11 | 5, 12 | Term/element/schema versions; no rollback |
| D12 | — | N/A |
| D13 | 3, 5 | Agents, embedding search, tools |
| D14 | 5, 8 | NL2SPARQL with ontology validation |
| D15 | 2, 3, 5 | Core strength |
| D16 | 3 | Visual editor, diagrams |
| D17 | 3 | SDK, templates; limited evidence |
| D18 | 5, 10 | DB ACL experimental |
| D19 | 10 | Unknown |
| D20 | 7 | Not verifiable |
| D21 | 1, 10 | Proprietary; historical commons clause |
| D22 | 10, 11 | RDF-only |
| D23 | — | Not assessed |
| D24 | App C | Vendor news only |

## Appendix B — Capability mapping

| CAP | Technology | Evidence | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-41 | native | mph-05 | BL-32 partial | BUILD | P1 |
| CAP-37 | partial | mph-04 | BL-32 partial | BUILD | P1 |
| CAP-21 | native | mph-03,05 | BL-51 partial | EXPERIMENT | P2 |
| CAP-29 | native | mph-03 | BL-33 impl. | REUSE | P2 |
| CAP-58 | native | mph-06 | BL-12 partial | BUILD | P1 |
| CAP-38 | native | mph-05 | BL-41 impl. | BUILD | P2 |
| CAP-12 | native | mph-06 | Absent | INTEGRATE | P2 |
| CAP-72 | partial (beta) | mph-03 | BL-53 impl. | DEFER | P3 |
| CAP-46 | experimental | mph-06 | BL-18 Absent | BUILD | P0 |
| CAP-10 | UNKNOWN | mph-02 | BL-29 partial | n/a | — |
| CAP-56/57 | partial | mph-06 | BL-16 impl. | DEFER | P3 |

## Appendix C — Evidence records

| CLAIM-ID | product/version/date | exact claim | class | source + URL | pub / access | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-mph-01 | metaphacts | Digital Science acquired metaphacts (announced 2023-01-23; independent entity); 2026-09-23 rebrand "metaphacts is now metaphactory"; 2026-03-25 Digital Science acquires Ontopic | Officially documented (vendor/acquirer news) | https://www.digital-science.com/news/digital-science-acquires-metaphacts/ ; https://metaphactory.com/news | 2023-01-23; 2026 / 2026-10-26 | 0.85 | none |
| CLAIM-mph-02 | metaphactory home | Positioned as semantic intelligence layer for enterprise AI; components: modelling and governance, virtual KG over Snowflake/Databricks/BigQuery/Redshift, metis, EIA; standards RDF/OWL/SHACL/SPARQL; named customers; deployment not stated | Officially documented (marketing) | https://metaphactory.com | 2026 / 2026-10-26 | 0.75 | marketing |
| CLAIM-mph-03 | 6.0 / 5.11 | 6.0 (2026-07-14): Model–Map–Access, publish ontologies for virtualised access, metis in real-time collaborative Visual Ontology Editor, semantic annotation beta, RDF/SPARQL 1.2 annotated facts. 5.11 (2026-03-31): concurrent modeling beta, "Google Docs-like", mechanism unspecified; Excel import | Officially documented | https://metaphactory.com/metaphactory-6-0-helps-organizations-connect-trusted-enterprise-knowledge-to-ai-applications ; https://metaphactory.com/metaphactory-5-11-introduces-concurrent-modeling-and-simplified-excel-onboarding | 2026-07-14; 2026-03-31 / 2026-10-26 | 0.8 | none |
| CLAIM-mph-04 | 6.1 | GA 2026-09-30: schema snapshots/version history, re-import flags renamed/dropped/type-changed; governance agent recommends, humans apply; metis preview-and-confirm with optional auto-mode; extraction with source traceability; branching/release/rollback/SHACL not covered | Officially documented | https://metaphactory.com/metaphactory-6-1 | 2026-09-30 / 2026-10-26 | 0.8 | omissions are not proof of absence |
| CLAIM-mph-05 | 5.4 / 5.7 | 5.4 (2024-07-10): federation tuned declaratively, threaded review comments, versioned ontology element pages; 5.7 (2025-03-31): term-level provenance (PROV-O), editorial states (development, ready for review, in review, accepted for publication), review comments | Officially documented | https://metaphactory.com/metaphactory-5-4 ; https://metaphactory.com/metaphactory-5-7 | 2024-07-10; 2025-03-31 / 2026-10-26 | 0.8 | none |
| CLAIM-mph-06 | 5.9 / 5.10 | 5.9 (2025-10-13): SKOS-XL in vocabulary editor, SPARQL validated against ontology, experimental DB-level ACL enforced natively if store supports; 5.10 (2026-01-12): embedding retrieval beta, model list GPT-5.1/5.2/Gemini 3 Pro, local models not stated, deprecation of ontology elements | Officially documented | https://metaphactory.com/metaphactory-5-9-delivers-powerful-enhancements-to-power-trustworthy-ai-driven-knowledge-modeling-decision-making ; https://metaphactory.com/metaphactory-5-10-delivers-advanced-ai-search-capabilities-and-enhanced-modular-ontology-management | 2025-10-13; 2026-01-12 / 2026-10-26 | 0.8 | none |
| CLAIM-mph-07 | SAP partnership | 2026-05-12 partnership; requires SAP HANA Cloud with KG Engine; metaphactory self-managed via Docker or AWS Marketplace or hosted trial; SAP Store availability announced 2026-10-07 | Officially documented | https://metaphactory.com/metaphactory-now-available-with-sap-hana-cloud-knowledge-graph-engine ; https://metaphactory.com/news | 2026-05-12 / 2026-10-26 | 0.8 | SAP announcement said "planned" then "available" |
| CLAIM-mph-08 | metaphacts GitHub org | Repos: Helm charts (pushed 2026-10-07), docker-compose (2026-09-30), sample-apps; MIT carml, etc.; platform source repo not listed; no licence detected on deployment repos | Observed | https://api.github.com/orgs/metaphacts/repos | 2026-10-07 / 2026-10-26 | 0.7 | listing truncated after 18 repos |
| CLAIM-mph-09 | metaphactory community platform 4.1.0 | Third-party Docker Hub page: LGPL 2.1 + Commons Clause | Third-party report | https://hub.docker.com/r/robcast/metaphacts-community-platform | ~2021 / 2026-10-26 | 0.4 | outdated; current terms UNVERIFIED |

## Appendix D — Assumptions

- Access date is the actual 2026-10-26, not the brief's 2026-10-18.
- Claims rest on vendor release articles; the help-site changelog and documentation were not retrievable, hence several UNKNOWN entries.
- "metaphactory" and former "metaphacts" brand treated as the same product line; Ontopic relation to Ontop assumed unverified.
- Supported triple stores other than SAP HANA Cloud KG Engine are not asserted.
