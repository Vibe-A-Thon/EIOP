# C17 — Wikidata

| Field | Value |
|---|---|
| Registry ID | T-C17-wikidata |
| Tier | B (open KG; model reference for claim provenance and contradictions) |
| Versions examined | Rolling Wikibase service; WDQS backend update page last edited 2026-10-17 |
| Verified on | 2026-10-26 (brief said 2026-10-18; actual access date used) |
| Worker | V31 |

## 1. Identity, status, sources
Wikidata is the Wikimedia Foundation's collaborative multilingual knowledge base, built on the Wikibase software. Active. Structured data (main, Property, Lexeme, EntitySchema namespaces) is CC0; other namespaces CC BY-SA 4.0 [CLAIM-wikidata-01]. Tier B: a reference model, plus an optional import/linking target (entity IDs as external identifiers).

## 2. Problem and workflows
General-purpose open entity graph with sourced statements. Workflows: entity linking (QID as canonical identifier), SPARQL lookups via WDQS, dumps for bulk load, community editing with constraints.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Items, properties, lexemes, entity schemas (ShEx-style) | present [CLAIM-wikidata-02] |
| Statement = property + value, qualifiers, references, rank | present [CLAIM-wikidata-02] |
| Ranks normal/preferred/deprecated | present [CLAIM-wikidata-02] |
| "no value" / "unknown value" special values | present [CLAIM-wikidata-02] |
| Property constraints (flag, not block) | present [CLAIM-wikidata-02] |
| WDQS SPARQL endpoint | present, backend changing [CLAIM-wikidata-03] |
| Per-user ACL / tenant isolation | absent (public wiki) |
| Truth maintenance / automatic contradiction resolution | absent (human editorial) |

## 4. Architecture
```
 editors/bots -> MediaWiki+Wikibase (entity JSON revisions, MariaDB) -> dumps (RDF/JSON)
                                                  \-> updater -> WDQS triplestore (Blazegraph -> QLever) -> SPARQL
 statement node: Item --p:Pxx--> [stmt] --ps:--> value ; --pq:--> qualifiers ; --prov:wasDerivedFrom--> reference ; wikibase:rank
```
(RDF mapping details from secondary sources, confidence medium.)

## 5. Under the hood
Reification by design: every statement is a first-class node carrying qualifiers, references and rank, so conflicting statements for the same property coexist. Consumers select by rank (queries default to preferred, else normal; deprecated excluded) [CLAIM-wikidata-02]. Restrictive qualifiers change a statement's scope and must be honoured by consumers; non-restrictive ones can be ignored [CLAIM-wikidata-02]. Storage internals of Wikibase NOT verified here.

## 6. Requirements inferred
Claim records need: subject, predicate, value-or-special-value, qualifiers (scope), references (source, retrieval date), rank/status, and revision history; consumers must declare which rank policy they use.

## 7. Performance and resource model
No benchmark verified. WDQS operational facts (vendor-side): about 48 h replication lag from September 21, 2026 caused by a few expensive queries; global rate limiting targeted January 2027 [CLAIM-wikidata-03]. Scale figures UNVERIFIED.

## 8. Strengths
Mature, widely understood claim model: multi-value, sourced, scoped, ranked; "unknown" vs "no value" distinction; constraint reports as soft governance.

## 9. Limitations
| Class | Item |
|---|---|
| Intentional | Constraints are advisory; quality relies on editors; CC0 rule excludes many licensed datasets [CLAIM-wikidata-01] |
| Operational | WDQS on Blazegraph (unmaintained, GPL-2.0, archived) being replaced by QLever; Blazegraph-specific features (named subqueries, geospatial) are not carried over (job posting, secondary) [CLAIM-wikidata-03]; new endpoints expected for the community by 2026-11-01, Blazegraph may degrade from 2027-02 |
| Semantics | Ranks encode editorial preference, not confidence or stance; no agent-level belief or ACL |

Cross-reference: C02-tier-c-records-V16.md covers Blazegraph and QLever.

## 10. Deployment, licensing
Data CC0 (safe to redistribute); Wikibase software is open source (licence GPL-2.0-or-later per MediaWiki family, UNVERIFIED this run, legal-review trigger if embedded). Self-hosting Wikibase is possible but heavy; the model can be re-implemented without it. Air-gap: dumps yes.

## 11. Delta vs baseline
EOIP `TruthStore` (BL-39) keeps conflicting claims side by side with status accepted/rejected/obsolete and resolution decisions; evidence manifests (BL-41). Gaps vs Wikidata: no qualifier-scoped statements, no preferred/deprecated rank semantics or "unknown/no value" distinction (not seen in `truth/engine.py`); the store is in-memory.

## 12. Cards
STR-wikidata-01 | Wikidata | statement model: qualifiers+references+rank | CLAIM-02 | principled multi-source facts | match | add `qualifiers`, `rank`, `special_value` to Claim; map to PROV-O and RDF-star | round-trip 1,000 sampled statements with zero loss.
INV-wikidata-01 | target Wikidata WDQS 2026 | single-engine dependency, engine-specific SPARQL extensions; root cause: coupling (proven by migration) | EOIP backend-neutral GraphStore avoids it; worse when a backend feature is needed for speed. Options: quick = standard SPARQL only; native = capability flags per backend; long = IR transpiler. Select native. POC: run one query corpus on two engines and diff results. Defensibility: conformance suite. Decision ADOPT (principle). No seed hypothesis targets it.

## 13. Decisions
| Capability | Decision |
|---|---|
| Claim data model with qualifiers/references/rank (CAP-38, CAP-11) | BUILD (REFERENCE design) |
| Contradiction representation (CAP-39) | BUILD: coexisting claims plus rank policy |
| Entity linking to QIDs (CAP-30) | INTEGRATE as external-ID property |
| Running Wikibase/WDQS | REJECT |
| Dump import | DEFER |

## 14. Tests
Model 50 contradictory statements (two values, scoped by time qualifiers, one deprecated) in TruthStore; assert `explain()` returns all with reasons; assert rank-policy switch changes the canonical value without deletion.

## 15. Risks and open questions
Qualifier explosion; mapping to RDF-star vs reification across LPG backends (loss accounting, BL-31); whether to expose ranks to NL answers.

## Appendix A — Dimension coverage
| Dim | Sec | Summary |
|---|---|---|
| D1 | 1,10 | owner, licence |
| D2 | 2 | open KG |
| D3 | 4 | Wikibase+WDQS |
| D4,D6 | 4,5 | statement nodes; Blazegraph→QLever |
| D5 | 3,5 | constraints, entity schemas |
| D7 | N/A | no reasoning in core |
| D8 | 7 | partial, vendor incidents |
| D9 | 2 | dumps/bots |
| D10 | 5,6 | references, ranks |
| D11 | 6 | revision history (not detailed) |
| D12–D14 | N/A | out of scope |
| D15 | 3,8 | community governance |
| D16,D17 | N/A | not examined |
| D18–D19 | 3 | public, no tenancy |
| D20 | 7 | UNVERIFIED |
| D21 | 10 | CC0 |
| D22 | 10 | RDF/JSON dumps |
| D23 | N/A | none found |
| D24 | 9 | pages inconsistent on dates |

## Appendix B — Capability mapping
| CAP | Wikidata | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-38 | native | 02 | BL-39,BL-41 Implemented | BUILD | P1 |
| CAP-39 | partial (ranks, human) | 02 | BL-39 Implemented | BUILD | P1 |
| CAP-11 | native (reified statements) | 02 | BL-31 Implemented | EXPERIMENT | P2 |
| CAP-15 | native (WDQS) | 03 | BL-06 Partial | REFERENCE | P3 |

## Appendix C — Evidence
| ID | Product/date | Claim | Class | Source | Access | Conf | Contra |
|---|---|---|---|---|---|---|---|
| wikidata-01 | 2026 | CC0 for main/Property/Lexeme/EntitySchema; CC BY-SA 4.0 elsewhere | Official | https://www.wikidata.org/wiki/Wikidata:Licensing | 2026-10-26 | 0.9 | none |
| wikidata-02 | 2026 | statements, qualifiers, references, three ranks, special values, constraints | Official | https://www.wikidata.org/wiki/Wikidata:Data_model | 2026-10-26 | 0.85 | none |
| wikidata-03 | 2026-10-17 | WDQS moving Blazegraph→QLever; community endpoints by 2026-11-01; Blazegraph may degrade from 2027-02; Sept 2026 lag incident | Official wiki | https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/WDQS_backend_update | 2026-10-26 | 0.8 | V16 notes dates differ across Wikimedia pages |

## Appendix D — Assumptions
RDF namespace mapping from secondary sources. Wikibase licence unverified. Access date 2026-10-26.
