| Field | Value |
|---|---|
| Registry ID | T-C03-wikibase |
| Tier | B (collaborative KG authoring at scale; grouped record: Wikibase + Semantic MediaWiki) |
| Versions examined | Wikibase Suite 8.0 (Phabricator "WBS 8.0 Release" resolved 18 Aug, year inferred 2026); Wikibase Repository extension (master, continuous); Semantic MediaWiki 6.0.0 (2025-08-12), 7.0.0 (2026-06-04), 7.2.0 (2026-07-18, via Professional.wiki) |
| Verified on | 2026-10-26 (actual access date) |
| Worker | V13 |

## 1. Identity, current status, tier, and sources
Member 1, Wikibase: MediaWiki extensions (Repository, Client) from Wikimedia Deutschland (WMDE) providing a structured-data repository; extension licence GPL-2.0-or-later, status "stable", master "not backward compatible", snapshot releases accompany MediaWiki [CLAIM-wiki-01]. Packaged for self-hosting as Wikibase Suite (WBS; Docker images, release pipeline `wmde/wikibase-release-pipeline`) and hosted as Wikibase.cloud [CLAIM-wiki-02]. Member 2, Semantic MediaWiki (SMW): MediaWiki extension adding typed semantic annotations and queries; 6.0.0 12 Aug 2025 (maintenance for newer MediaWiki), 7.0.0 4 Jun 2026 (performance, admin simplification), 7.2.0 18 Jul 2026 (parser features, six security fixes, PostgreSQL restored) [CLAIM-wiki-03]. SMW licence: GPL-2.0-or-later per project documentation (NOT re-fetched this run; confidence 0.5). Both active. Tier B: two different models for wiki-based KG authoring.
Sources: `https://www.mediawiki.org/wiki/Extension:Wikibase_Repository`, `https://www.semantic-mediawiki.org/wiki/SMW_6.0`, Professional.wiki news, Wikibase.cloud Meta page.

## 2. Problem, workloads, workflows
Crowd or team curation of entities and statements with edit history, discussion and bots. Wikibase: items/properties with statements, qualifiers, references; query via SPARQL query service; bulk edits via API and tools such as QuickStatements. SMW: authors annotate wiki pages with typed properties and query them inline (`#ask`). Example: a consortium maintains a domain KG with provenance per statement.

## 3. Feature inventory
| Feature | Wikibase | SMW |
|---|---|---|
| Entity/statement model with qualifiers and references | present (MediaWiki-documented model; not opened in this run) | partial (properties on pages; no first-class references) |
| Revision history, talk pages, user rights | present (MediaWiki core) | present |
| Query | SPARQL via separate query service component (WBS exposes SPARQL UI) [CLAIM-wiki-02] | inline `#ask`, SPARQL store optional (UNVERIFIED) |
| Full-text search | OpenSearch image bundled in WBS [CLAIM-wiki-02] | MediaWiki search; Elasticsearch optional (UNVERIFIED) |
| Bulk import tools, OAuth | QuickStatements; needs public hostnames [CLAIM-wiki-02] | import via templates/CSV extensions (UNVERIFIED) |
| Federated query | Wikibase.cloud federation with Wikidata allowlist (quality issues reported) [CLAIM-wiki-04] | absent |
| Schema/constraints | property constraints (UNVERIFIED); ShEx schemas (UNVERIFIED) | semantic property types |
| OWL reasoning | absent | absent |
| Fine-grained per-statement ACL | absent (wiki-level rights only; inference) | absent |
| Multi-tenant isolation | per-instance (Wikibase.cloud hosts many wikis) | per-wiki |

## 4. Architecture diagram
```
 Browser / API / bots --> Apache + PHP: MediaWiki core + Wikibase Repository/Client (or SMW)
      |-- SQL DB (MariaDB/MySQL; term store tables wbt_*, wb_id_counters ...) [CLAIM-wiki-01]
      |-- OpenSearch (WBS image with Wikibase plugins)  [CLAIM-wiki-02]
      |-- Wikibase Query Service (RDF store + updater) --> SPARQL UI (WBS)  [CLAIM-wiki-02]
      `-- QuickStatements, OAuth, job queue (UNVERIFIED)
```

## 5. Under-the-hood reconstruction
Wikibase stores entities as MediaWiki revisions (JSON blobs) plus relational term-store and id-counter tables [CLAIM-wiki-01]; the RDF projection and updater feed a separate SPARQL service (documented as a deployed component; the backing triplestore product NOT verified in this run, historically Blazegraph: UNVERIFIED for current WBS). Concurrency and history come from MediaWiki's revision model (hypothesis grounded in core design). SMW stores annotations in relational tables with optional external store (UNVERIFIED). Reasoning: none. Security: MediaWiki user groups and page protection. Internals not opened at tags.

## 6. Inferred requirements
Revisioned entities, per-statement references, bot/API bulk edit, search, SPARQL projection, language labels, OAuth.

## 7. Performance and resource model
No verified numbers. Cost: PHP/MariaDB plus search and query-service containers; updater lag between edits and SPARQL is the known operational concern (hypothesis; Wikidata-scale scaling history is public but not read here). Federated queries on Wikibase.cloud time out when allowlisted endpoints fail [CLAIM-wiki-04].

## 8. Strengths
Mature collaborative authoring with history, discussion, vandalism patrol tooling; per-statement qualifiers and references (provenance as a first-class concept); GPL stack with strong community; WBS makes self-hosting turnkey. Match: statement-with-reference model corresponds to EOIP claims plus evidence (BL-39/41); exceed with ACL-aware retrieval.

## 9. Limitations
Documented: Wikibase master not backward compatible; installation needs public hostnames for QuickStatements OAuth [CLAIM-wiki-01][CLAIM-wiki-02]; federation allowlist endpoints often failing [CLAIM-wiki-04]. Hypotheses: not a reasoner; weak schema enforcement versus SHACL; eventual consistency to SPARQL; wiki-level (not statement-level) permissions; heavy multi-container stack; SMW tied to MediaWiki upgrade cadence. Licensing: GPL-2.0-or-later is copyleft: legal-review trigger for embedding/redistribution; running unmodified as a separate service is a different question for counsel.

## 10. Deployment, licensing, viability
Self-host via WBS Docker images (air-gap feasible with mirrored images; OAuth tools need hostnames); GPL copyleft trigger (record, no conclusion). Not embeddable in a Python product; at most an adjacent authoring front end. White-label: MediaWiki skinning possible (UNVERIFIED).

## 11. Competitive delta vs baseline
BL-53 collaboration (annotations, workspaces; no co-editing) versus MediaWiki's mature revision/talk model; BL-37/39/41 give revisions, claims and evidence manifests that map to Wikibase statements+references. BL-18 source-ACL absent in retrieval: Wikibase offers none either, so no delta. BL-32 governance partial.

## 12. Cards
**STR-wiki-01** | Wikibase | first-class statement ranks, qualifiers and references | [CLAIM-wiki-01] | evidence-backed facts at the statement level | match | confirm EOIP claim contract carries qualifier/reference slots and rank (preferred/normal/deprecated) | acceptance: round-trip of 1,000 Wikidata-style statements with references lossless in JSON-LD.
**STR-wiki-02** | Wikibase Suite | turnkey self-hosting bundle | [CLAIM-wiki-02] | quick start for self-hosted KG | match | one-command single-node compose profile already planned in deploy/ | acceptance: cold start to first entity < target defined in POC.
**INV-wiki-01** | Wikibase / SMW | wiki permission granularity and SQL-to-SPARQL lag | [CLAIM-wiki-02][CLAIM-wiki-04] | root cause architecture/coupling (*hypothesis*) | alternative: write path through a validation gate with synchronous projection and per-fact ACL | options (a) import Wikibase JSON dumps; (b) native claim UI on EOIP gate; (c) differentiated ACL-aware co-editing | selected (b) | POC: measure edit-to-query lag in WBS (baseline) vs EOIP gate | decision EXPERIMENT.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-38 statement-level provenance model | BUILD (adopt rank/qualifier/reference shape) |
| CAP-72 collaborative editing UI | DEFER |
| CAP-26 import of Wikibase/Wikidata dumps | EXPERIMENT |
| Wikibase/SMW as embedded component | REJECT (GPL, PHP stack) |
| CAP-12 taxonomy | REFERENCE-ONLY |

## 14. Tests
(PROPOSED.) Deploy WBS offline from mirrored images; time edit-to-SPARQL visibility; export a statement set with references to JSON-LD and validate round-trip; verify GPL notices in image SBOM; test federated query failure handling.

## 15. Risks and open questions
Current WBS 8.0 release notes not read; Wikibase storage/RDF backend of current WBS unverified; SMW licence and store options not re-verified; GPL distribution obligations; security advisories (SMW 7.2.0 fixed six issues) imply patch cadence cost.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | GPL, WMDE/community |
| D2 | 2 | Collaborative KG |
| D3 | 4 | PHP + SQL + search + SPARQL |
| D4 | 5 | Revision blobs + SQL tables |
| D5 | 3 | Statement model; no OWL |
| D6 | 3 | SPARQL service; #ask |
| D7 | 3 | None |
| D8 | 7 | Not verified |
| D9 | 3 | QuickStatements, bots |
| D10 | 8 | References per statement |
| D11 | 3,5 | MediaWiki revisions |
| D12 | N/A | None |
| D13 | N/A | None |
| D14 | N/A | None |
| D15 | 2,8 | Wiki workflows |
| D16 | 3 | Wiki UI |
| D17 | 3 | API, bots |
| D18 | 9 | Wiki-level rights |
| D19 | 3 | Per-instance |
| D20 | 7 | No data |
| D21 | 10 | Free, hosted option |
| D22 | 5 | RDF projection |
| D23 | N/A | None identified |
| D24 | App. C | Partly secondary sources |

## Appendix B. Capability mapping
| CAP-ID | Technology | CLAIM | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-38 | native | 01 | BL-39/41 Implemented | BUILD | P1 |
| CAP-36 | native (MediaWiki) | 01 | BL-37 Implemented | REFERENCE | P3 |
| CAP-72 | partial | 02 | BL-53 | DEFER | P3 |
| CAP-26 | partial (bots) | 02 | BL-23 | EXPERIMENT | P3 |
| CAP-15 | plugin (query service) | 02 | BL-06 Partial | REFERENCE | P3 |

## Appendix C. Evidence records
| CLAIM-ID | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-wiki-01 | Wikibase Repository master | GPL-2.0-or-later; stable; master not backward compatible; SQL term-store tables | Officially documented | https://www.mediawiki.org/wiki/Extension:Wikibase_Repository | continuous / 2026-10-26 | 0.8 | none |
| CLAIM-wiki-02 | Wikibase Suite | Self-hosting bundle; Docker images; OpenSearch image with Wikibase plugins; SPARQL UI; QuickStatements OAuth needs public hosts | Third-party report | https://www.mediawiki.org/wiki/Wikibase/Docker ; https://hub.docker.com/r/wikibase/opensearch (via search) | undated / 2026-10-26 | 0.55 | older docs |
| CLAIM-wiki-03 | SMW 6.0.0/7.0.0/7.2.0 | 6.0.0 2025-08-12; 7.0.0 2026-06-04; 7.2.0 2026-07-18 with six security fixes | Third-party report | https://www.semantic-mediawiki.org/wiki/Semantic_MediaWiki_7.0.0_released ; https://www.professional.wiki (via search) | 2026-06-04 / 2026-10-26 | 0.55 | SMW page itself blocked by bot protection |
| CLAIM-wiki-04 | Wikibase.cloud | Q1 2026 work on query federation; many allowlist endpoints non-operational causing timeouts | Officially documented | https://meta.wikimedia.org/wiki/Wikibase/Wikibase.cloud (via search) | 2026 / 2026-10-26 | 0.5 | none |
| CLAIM-wiki-05 | WBS 8.0 | Phabricator task "WBS 8.0 Release" resolved 18 Aug (year inferred) | Third-party report | Phabricator via search | 2026-08-18 (inferred) / 2026-10-26 | 0.3 | no changelog |

## Appendix D. Assumptions
Wikibase data model details are from general knowledge of the public model and were not re-fetched; marked accordingly. SMW licence assumed GPL-2.0-or-later (UNVERIFIED). Year of WBS 8.0 inferred.
