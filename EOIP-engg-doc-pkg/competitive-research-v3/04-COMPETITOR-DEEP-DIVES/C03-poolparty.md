# C03 — PoolParty (Semantic Suite; now Graphwise "Graph Modeling")

| Field | Value |
|---|---|
| Registry ID | T-C03-poolparty |
| Tier | A — leading taxonomy/thesaurus platform; corporate-status trap (Graphwise merger) |
| Versions examined | PoolParty 10.1 (released about 2026-01-19; vendor page dates inconsistent), 10.1.2 patch, 10.2 / "Graph Modeling and Semantic Analytics 10.2" (blog 2026-03-19; notes dated 2026-04-22); older docs 2022 R2–2025 R2 (9.6/9.7) for architecture |
| Verified on | 2026-10-26 (actual access date; brief said 2026-10-18 — see Appendix D) |
| Worker | V03 |

## 1. Identity, current status, tier, and sources

PoolParty was the flagship product of **Semantic Web Company (SWC)**, Vienna. On 2024-10-23 SWC and **Ontotext** (GraphDB) announced a merger forming **Graphwise**; the product brands PoolParty and GraphDB were to continue initially and eventually merge into the Graphwise name [CLAIM-pp-01]. A Graphwise transition guide (dated 2026-02-27) says PoolParty Semantic Suite and GraphDB are being rebranded into a unified **Graphwise Platform**; in the first phase the core PoolParty components are renamed **Graph Modeling**, while the "PoolParty" name persists in 10.x releases [CLAIM-pp-02][CLAIM-pp-04]. Registry resolution: "PoolParty" = Graphwise Graph Modeling (ex-PoolParty Thesaurus Server and Extraction Server, PPT/PPX). Cross-reference C02 `ontotext-graphdb` (same company).

| Item | Verified state |
|---|---|
| Latest | 10.2 (Graph Modeling 10.2); documentation selector lists "GWP 26/1", 10.2, 10.1 [CLAIM-pp-02] |
| Cadence | 2025 R1/R2 (9.6/9.7) → 10.0 → 10.1 (2026-01) → 10.2 (2026-03/04): faster than historic two-per-year [CLAIM-pp-03][CLAIM-pp-04] |
| Owner | Graphwise (SWC + Ontotext) [CLAIM-pp-01] |
| Licence | Proprietary commercial; terms and pricing NOT PUBLICLY VERIFIED |
| Customers | Vendor claim: GraphDB + PoolParty "used by over 100 organizations" (another report says ~200) — marketing figures [CLAIM-pp-01] |
| Date inconsistencies | Several release-note pages carry a 2025 date for 2026 content; treated as typos, confidence reduced |

## 2. Primary problem, target workloads, concrete example workflows

Enterprise taxonomy/thesaurus/ontology management on SKOS and SKOS-XL, plus semantic tagging ("concept extraction") of documents and graph-powered search (GraphSearch). Example workflows:

1. **Build a taxonomy**: 10.1's LLM-driven *Taxonomy Builder* generates a top-down skeleton from a domain description, with labels and definitions; humans review and accept [CLAIM-pp-03].
2. **Govern concepts**: concepts move draft → suggested → approved, with deprecated-concept handling via the Workflow Dashboard [CLAIM-pp-07].
3. **Tag content**: extractor API tags documents against the taxonomy; 10.2 adds a Lucene-based engine for 40+ languages via `extractorType=LUCENE` and a unified `/api/tag` endpoint [CLAIM-pp-04].
4. **Publish to search/RAG**: GraphSearch indices and GraphRAG components in the wider Graphwise platform [CLAIM-pp-05].

## 3. Feature inventory

| Capability | State | Notes |
|---|---|---|
| SKOS thesaurus editing, SKOS-XL labels | present | docs sections "SKOS-XL with Graph Modeling", "Graph Modeling, SKOS, RDF and URIs" [CLAIM-pp-02] |
| Custom OWL ontologies | partial/UNKNOWN | ontology modelling exists in Graph Modeler overview; depth NOT VERIFIED |
| SHACL | UNKNOWN | not evidenced in material read |
| Approval workflow, suggested/deprecated concepts | present | [CLAIM-pp-07] |
| Custom roles (10.1) | present | granular governance [CLAIM-pp-03] |
| Project history in named graph, filter, export RDF/XLSX | present | [CLAIM-pp-07] |
| Version snapshots / branch / rollback | NOT FOUND | deletion not covered by approval; no restore found [CLAIM-pp-07] |
| Semantic diff | NOT FOUND (history view only) | — |
| Concurrent editing | UNKNOWN | no co-editing doc found |
| Extraction/tagging, categorization | present | [CLAIM-pp-04] |
| LLM taxonomy generation | present | provider/local-model options NOT VERIFIED [CLAIM-pp-03] |
| Linked-data frontend, SPARQL endpoint | present (LDF config with Docker page) | nav evidence only |
| SSO: SAML, LDAP, 2FA | present via Keycloak | nav evidence [CLAIM-pp-05] |
| HA | present: documented HA workflow with load balancer | nav evidence only [CLAIM-pp-05] |
| API | REST (project, extractor); API user setup | [CLAIM-pp-04] |
| CLI/SDK | UNKNOWN | — |

## 4. Architecture diagram

```
 browser (JS frontend) ───────────────►  PoolParty application (Java; Tomcat; 64-bit Linux only since 2024 R2)
                                           │  Thesaurus/Graph Modeler · Workflow · History · Extractor · GraphSearch
   Keycloak (SAML/LDAP/2FA) ◄──────────────┤
        └─ external PostgreSQL (recommended; H2 embedded by default)
                                           │ SPARQL/RDF4J-style API
                                           ▼
                            GraphDB (externalised from 10.0; project + system repositories)
                                           │
              Elasticsearch (entity-extraction models, GraphSearch indices; older releases: embedded Solr)
              Apache Spark (ML for document classification)
```
[CLAIM-pp-05][CLAIM-pp-06]. State: all taxonomy data and history in GraphDB repositories (history in a named graph per project [CLAIM-pp-07]); search state in Elasticsearch; identity in Keycloak/PostgreSQL.

## 5. Under-the-hood reconstruction

**Data model.** SKOS concept schemes (`skos:Concept`, `broader/narrower/related`, `prefLabel/altLabel`) with optional SKOS-XL labels as first-class resources; custom schemes/classes extend SKOS. Concept states (draft, suggested, approved, deprecated) are represented as additional triples/graphs; deprecated concepts are moved to a "deprecated resources" graph so URIs are never reused [CLAIM-pp-07]. Exact predicates are NOT PUBLICLY VERIFIED.

**Storage and indexing.** GraphDB repositories (RDF4J-compatible) per project; from 10.0 GraphDB is a separate externally scaled instance, enabling independent scaling and HA [CLAIM-pp-05]. Older releases embedded GraphDB or RDF4J and Solr. Extraction models are built into Elasticsearch indices (label-driven, so extraction is a *dictionary/label match with linguistic normalisation*, not a trained NER: hypothesis supported by 10.2 notes describing Lucene analyzers and finite-state transducers for tokenisation and inflection [CLAIM-pp-04]). Machine-learned classification uses Spark [CLAIM-pp-05].

**Query pipeline.** SPARQL against GraphDB; GraphSearch is Elasticsearch-backed faceted search over annotated documents plus concept graph expansion (hypothesis; internals NOT PUBLICLY VERIFIED).

**Reasoning.** Whatever the GraphDB repository ruleset provides (RDFS/OWL-Horst/OWL2-RL family — that is GraphDB's capability, see C02) plus SKOS-aware inference such as transitive broader closure (hypothesis). PoolParty itself is not a reasoner.

**Concurrency/transactions.** Multi-user on a shared project; GraphDB provides transactional isolation. Whether PoolParty uses optimistic or pessimistic concept-level locking is NOT PUBLICLY VERIFIED; the approval workflow, not locking, is the documented conflict-avoidance mechanism (draft/suggested stage) [CLAIM-pp-07].

**Versioning.** Event history only: project history captures all edits and approval state changes in a named graph; filterable; exportable as RDF/XLSX; per-concept history from the workflow overview. Deletion bypasses approval and cannot be rejected back [CLAIM-pp-07]. No tagged release / snapshot / rollback mechanism was found, which is a gap relative to Git-style ontology releases.

**Caching.** NOT PUBLICLY VERIFIED.

**Security.** Keycloak realms (SAML, LDAP, 2FA, password policy); custom roles from 10.1 [CLAIM-pp-03][CLAIM-pp-05]. Per-project permissions exist; tenant isolation model NOT PUBLICLY VERIFIED.

**Pseudocode (hypothesis) for label-driven tagging.**
```
index_build(taxonomy): for each concept, for each label in lang: analyze(label) -> token FST -> add to ES model
tag(doc, lang): tokens = lucene_analyze(doc, lang); matches = longest_match(tokens, model); return concepts(matches) with offsets
```

## 6. Functional and non-functional requirements inferred

| ID | Requirement | Basis |
|---|---|---|
| FR-1 | SKOS/SKOS-XL concept lifecycle with approval and deprecation | [CLAIM-pp-07] |
| FR-2 | Label-driven multilingual tagging with offsets | [CLAIM-pp-04] |
| FR-3 | Immutable URIs for deprecated concepts | [CLAIM-pp-07] |
| FR-4 | LLM-assisted generation under human acceptance | [CLAIM-pp-03] |
| NFR-1 | 64-bit Linux, OpenJDK 21 (2025 R1 docs), Elasticsearch, Keycloak, external DB | [CLAIM-pp-06] |
| NFR-2 | Advanced Server ≥ 8 GB RAM (16 recommended); Enterprise/Search ≥ 16 GB (32 recommended); disk ≥ 2.5× RAM | [CLAIM-pp-06] |
| NFR-3 | Externalised GraphDB for scaling/HA | [CLAIM-pp-05] |

## 7. Performance and resource model

Vendor sizing only: 8–16 GB (Advanced) and 16–32 GB (Enterprise/Search/Integrator) RAM plus disk of 2.5× RAM, stated in documentation that spans 2022–2025 releases [CLAIM-pp-06]. This is a multi-component stack (application JVM, GraphDB, Elasticsearch, Keycloak/PostgreSQL, optionally Spark), so a realistic one-node footprint exceeds the web-application figure; total NOT PUBLICLY VERIFIED. No independent benchmark of tagging throughput, taxonomy size limits, or GraphSearch latency was found. The 10.2 Lucene engine is vendor-described without numbers. Failure modes: Keycloak embedded H2 not recommended for production; legacy Solr-to-Elasticsearch migration; version drift across the externalised GraphDB.

## 8. Strengths and use-case-specific advantages

| ID | Strength | Route |
|---|---|---|
| STR-pp-01 | SKOS-first UX with approval/suggest/deprecate lifecycle; URIs never reused | match: add SKOS lifecycle states + URI-tombstone rule to EOIP ontology stewardship |
| STR-pp-02 | Label-driven multilingual tagging (40+ languages) producing concept links with offsets | integrate or match: deterministic first-tier extractor (aligns with seed "deterministic extraction first") |
| STR-pp-03 | History as queryable named graph, exportable | match: BL-37/38 already exceed on bitemporal; expose as RDF/XLSX export |
| STR-pp-04 | Taxonomy Builder with human acceptance | match with local model under egress policy (BL-45) |
| STR-pp-05 | Externalised graph store enables HA | already EOIP-consistent (backend neutrality) |

## 9. Limitations with root causes

| Class | Item | Root cause | Evidence |
|---|---|---|---|
| Op/hardware | Multi-service stack, 16–32 GB for enterprise | GraphDB + ES + Keycloak + Spark | [CLAIM-pp-05][CLAIM-pp-06] |
| Op | Windows server dropped; Linux only from 2024 R2 | Packaging decision | [CLAIM-pp-06] |
| Governance | Deletion outside approval; no restore | Workflow design | [CLAIM-pp-07] |
| Governance | No snapshot/branch/rollback evidence | History-only versioning | [CLAIM-pp-07] |
| Licensing | Proprietary; OEM/white-label terms unknown | Commercial | — |
| User friction | Corporate rebrand (PoolParty → Graph Modeling → Graphwise Platform) and doc dates inconsistent | Merger integration | [CLAIM-pp-02] |
| Maturity | LLM features: model hosting options undisclosed | — | [CLAIM-pp-03] |

No seed inversion in Master Prompt §10.5 targets PoolParty; none validated or rejected.

## 10. Deployment, licensing, redistribution, operational viability

Self-hosted on Linux; 10.1 adds containerised ("Dockerization of PoolParty apps") components [CLAIM-pp-03]; SaaS also offered by the vendor (details NOT VERIFIED). Air-gap viable for the classic stack (all components self-hosted); LLM Taxonomy Builder requires an LLM endpoint — egress posture NOT VERIFIED. Proprietary: no redistribution or white-label right without OEM agreement — **legal-review trigger**. Component licences: Elasticsearch (Elastic License/SSPL/AGPL family per version), Keycloak (Apache-2.0), GraphDB (Free vs Standard/Enterprise editions) — all from background knowledge, UNVERIFIED this session; flag for legal. Merger raises vendor-roadmap uncertainty (naming, support lifecycle).

## 11. Competitive delta against EOIP baseline

| Topic | PoolParty | EOIP | Delta |
|---|---|---|---|
| Taxonomy/SKOS (CAP-12) | Native, SKOS-XL | Absent: no SKOS module in baseline (label manifest, JSON-LD BL-31) | Missing; INTEGRATE or BUILD thin SKOS layer |
| Governance workflow (BL-32) | Approval states, roles, history | `OntologyGitOpsWorkflow` + stewardship | Different shape: EOIP is change-set PRs on manifests; PoolParty is per-concept states |
| Versioning | History graph only | SemVer releases, rollback receipts (`gitops.py:635-735`) | EOIP ahead on release/rollback |
| Extraction | Label-driven tagger, 40+ langs | Connectors + profile; no document concept tagger in baseline | Gap vs CAP-32 (cross-ref C05) |
| Backend neutrality | GraphDB centred | HugeGraph/Neo4j/Neptune/Fuseki/GraphDB | EOIP broader |
| SHACL (BL-29) | UNKNOWN | in-house subset | n/a |
| Tenancy | NOT VERIFIED | contract only (BL-20) | n/a |

## 12. Strength-adoption cards and inversion cards

STR cards: section 8.

**INV-pp-01 — "Event history without release/rollback; deletion bypasses approval."** Target: PoolParty 10.x Graph Modeling. Evidence [CLAIM-pp-07]. Root cause: governance (workflow design; *proven* in docs). Alternative: concept-level states plus SemVer vocabulary releases and reversible deletions via tombstones (EOIP already uses tombstones, BL-25). Worse when stewards want instant edits without release ceremony. Options: (a) quick — export SKOS to Turtle in Git and tag releases; (b) pragmatic — add SKOS lifecycle (draft/suggested/approved/deprecated) to stewardship with deprecated-URI graph and approval-covered deletion; (c) long-term — per-concept bitemporal revision with release bundles. Selected (b). Sketch: `concept{id, state, valid_from/to, replaced_by}`; delete = transition to deprecated + tombstone; release = frozen snapshot of approved set. POC: take a 10k-concept public thesaurus, run 500 scripted edits including deletes, restore to any release with 0 URI loss; metric: restore exactness and time; baseline PoolParty not measured (licence). Risks: URI collisions with external linked data; tenant per-scheme permissions. Defensibility: tied to evidence, tenancy and multi-backend. Decision: **EXPERIMENT**.

**INV-pp-02 — "Heavy multi-service stack."** Evidence [CLAIM-pp-05][CLAIM-pp-06]. Root cause: deployment coupling (*proven*). Alternative: single-process SKOS module over the existing GraphStore. Worse at vendor scale for search. Decision: **ADOPT** as a design principle (one-node-first), no new feature.

**INV-pp-03 — "Label-driven tagging misses context."** Hypothesis only (no evidence read). Decision: **DEFER**.

## 13. Per-capability decisions

| CAP | Decision | Note |
|---|---|---|
| CAP-12 taxonomy/SKOS | BUILD (thin) + INTEGRATE import/export | SKOS as a profile on the label manifest; round-trip with VocBench/PoolParty exports |
| CAP-41 governance workflow | BUILD | add per-concept states |
| CAP-32 unstructured extraction | EXPERIMENT | deterministic dictionary tagger from taxonomy, then local model (C05) |
| CAP-37 evolution | BUILD | releases of SKOS sets |
| CAP-55/56 retrieval | DEFER | GraphSearch pattern only for reference |
| CAP-77 licensing/TCO | REFERENCE | PoolParty not embeddable |
| CAP-58 NL/LLM generation | EXPERIMENT | Taxonomy Builder analogue under egress policy |

## 14. Tests, POC, acceptance

1. SKOS round-trip: import a public SKOS file (e.g. a thesaurus of ≥10k concepts), export, compare with Turtle isomorphism; zero loss, SKOS-XL labels preserved.
2. Lifecycle test: deleted concept yields tombstone, URI never reissued, restore reverses.
3. Tagger: dictionary tagger on a 1k-document multilingual sample; measure precision/recall against hand labels; compare with PoolParty only if a trial is licensed.
4. Taxonomy generation: local-model generation with egress policy S0; no data egress.
5. Permissions: stewards restricted to schemes; cross-tenant read denied.

## 15. Risks, trade-offs, open questions

- Rebrand turbulence: product names, doc URLs and dates are unstable; re-verify before any customer-facing comparison.
- No evidence on SHACL, co-editing, OEM, or on-prem LLM options.
- Elasticsearch licence class must be checked if EOIP ever bundles it.
- Open: does Graphwise Platform keep a stand-alone on-prem Graph Modeling SKU?
- Open: GraphDB edition limits on repository count/size for white-label use (C02).

## Appendix A — Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Merger, rebrand, proprietary |
| D2 | 2 | Taxonomy governance + tagging |
| D3 | 4, 5 | App + GraphDB + ES + Keycloak + Spark |
| D4 | 5 | GraphDB repos; ES indices |
| D5 | 5, 3 | SKOS/SKOS-XL; SHACL unknown |
| D6 | 5 | SPARQL via GraphDB; internals N/A |
| D7 | 5 | Delegated to GraphDB |
| D8 | 5, 7 | HA via external GraphDB; limited detail |
| D9 | 2, 3 | Extractor API, UnifiedViews (nav only) |
| D10 | 5 | URI permanence; no ER |
| D11 | 5, 12 | History graph, no rollback |
| D12 | — | N/A (Spark classification only) |
| D13 | 2, 3 | GraphSearch/GraphRAG (shallow) |
| D14 | — | NOT ASSESSED |
| D15 | 3, 5, 9 | Core strength |
| D16 | 3 | Web UI; no detail |
| D17 | 3 | API; SDK unknown |
| D18 | 5, 10 | Keycloak; tenancy unknown |
| D19 | 10 | Unknown |
| D20 | 7 | Vendor sizing only |
| D21 | 10 | Proprietary |
| D22 | 10, 11 | SKOS/RDF exports; XLSX |
| D23 | — | Not assessed |
| D24 | App C | Mostly vendor docs; navigation-heavy fetches reduced confidence |

## Appendix B — Capability mapping

| CAP | Technology | Evidence | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-12 | native | pp-02 | Absent | BUILD thin + INTEGRATE | P1 |
| CAP-41 | native | pp-07 | BL-32 partial | BUILD | P1 |
| CAP-37 | partial | pp-07 | BL-32 partial | BUILD | P2 |
| CAP-32 | native (tagging) | pp-04 | Absent | EXPERIMENT | P2 |
| CAP-58 | native (LLM taxonomy) | pp-03 | BL-12 partial | EXPERIMENT | P3 |
| CAP-45 | native (custom roles) | pp-03 | BL-19 impl. | REFERENCE | P3 |
| CAP-50 | partial | pp-06 | impl. | n/a | — |
| CAP-77 | n/a | pp-01 | — | REFERENCE | P3 |

## Appendix C — Evidence records

| CLAIM-ID | product/version/date | exact claim | class | source + URL | pub / access | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-pp-01 | SWC / Ontotext | Merger announced 2024-10-23 creating Graphwise; GraphDB and PoolParty brands continue then merge into Graphwise; >100 organisations use both (vendor), later report ~200 | Third-party report of vendor announcement | https://www.intelligentcio.com/north-america/2024/10/23/semantic-web-company-and-ontotext-merge-to-create-knowledge-graph-and-ai-powerhouse-graphwise/ ; https://graphwise.ai/blog/graphwise-merger-swc-ontotext | 2024-10-23 / 2026-10-26 | 0.85 | customer figures differ |
| CLAIM-pp-02 | Graphwise docs | Transition guide (27/02/2026): PoolParty Semantic Suite and GraphDB rebranded to Graphwise Platform; core PoolParty components renamed Graph Modeling; doc versions GWP 26/1, 10.2, 10.1; SKOS-XL and History sections exist | Officially documented (nav and search summary) | https://help.graphwise.ai/en/graphwise-documentation/graphwise-sub-components-at-a-glance/poolparty-semantic-suite-to-graphwise-platform-transition-guide.html ; https://help.graphwise.ai/pp10.2/en/graph-modeling/graph-modeling-release-notes/graph-modeling-10-2-release-notes.html | 2026-02-27 / 2026-10-26 | 0.65 | transition-guide body not readable (404/nav-only on fetch) |
| CLAIM-pp-03 | PoolParty 10.1 | AI Taxonomy Builder (LLM, top-down, human review), custom roles, improved GraphSearch ranking, Extractor API cleanup, Dockerization of apps; release about 2026-01 | Officially documented | https://help.graphwise.ai/en/graphwise-documentation/poolparty-10-1---ai-powered-taxonomy-creation.html ; https://graphwise.ai/blog/poolparty-10-1-ai-assisted-taxonomy-building-for-the-graphwise-era/ | 2026-01-19 (help pages) / 2026-10-26 | 0.7 | some pages dated 2025 |
| CLAIM-pp-04 | PoolParty 10.2 | Lucene-based concept tagging, 40+ languages, `extractorType=LUCENE`, unified `/api/tag`, NIF support discontinued, will become default | Officially documented | https://graphwise.ai/news/poolparty-10-2-advances-global-semantic-reach-with-a-unified-identity/ ; help.graphwise.ai 10.2 release notes | blog 2026-03-19; notes 2026-04-22 / 2026-10-26 | 0.75 | duplicate notes dated 2025 |
| CLAIM-pp-05 | PoolParty 10.x architecture | Java suite + JS frontend; GraphDB externalised from 10.0 for scaling/HA; Elasticsearch for extraction models and GraphSearch; Spark for ML; Keycloak with external PostgreSQL; older releases: built-in GraphDB/RDF4J and Solr, Tomcat 9; HA workflow page and SAML/LDAP/2FA exist | Officially documented | https://help.graphwise.ai/en/poolparty-overview/poolparty-system-architecture.html ; https://help.graphwise.ai/pp10.1/en/graphwise-documentation/system-architecture.html | / 2026-10-26 | 0.7 | version-dependent |
| CLAIM-pp-06 | PoolParty 2022–2025 docs | 64-bit Linux only from 2024 R2; OpenJDK 21 in 2025 R1 docs; Advanced ≥8 GB (16 rec.), Enterprise/Search/Integrator ≥16 GB (32 rec.); disk ≥2.5× RAM; Keycloak H2 embedded not recommended | Officially documented (via search summary) | https://help.poolparty.biz/en/administrator-guide/poolparty-installation/poolparty-system-requirements.html | / 2026-10-26 | 0.6 | numbers described as consistent across versions by summariser; may differ in 10.x |
| CLAIM-pp-07 | PoolParty workflow docs | States draft/suggested/approved/deprecated; deprecated concepts kept in a deprecated graph (URIs not reused); deletion not covered by approval; history in named graph, filterable, exportable RDF/XLSX; no restore/snapshot found | Officially documented | https://help.graphwise.ai/en/graph-modeling/thesaurus/the-workflow-dashboard/approval-workflow.html ; https://help.graphwise.ai/en/graph-modeling/thesaurus/poolparty-history/poolparty-history-on-project-level.html | / 2026-10-26 | 0.7 | absence of rollback is "not found", not proof |

## Appendix D — Assumptions

- Access date is the actual 2026-10-26, not the brief's 2026-10-18.
- Graphwise help pages fetched mostly as navigation (300 KB); claims rest on search-result summaries of the specific pages, so confidences are ≤0.75.
- "PoolParty" resolved to Graphwise Graph Modeling (ex PPT/PPX); the Graphwise Platform's other components (GraphDB, ADF, UnifiedViews) are out of scope here.
- Third-party licences (Elasticsearch, Keycloak, GraphDB) are background knowledge, UNVERIFIED.
