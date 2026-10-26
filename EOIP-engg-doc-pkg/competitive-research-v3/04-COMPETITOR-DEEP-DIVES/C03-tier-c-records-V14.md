# C03 Tier C records, batch V14 (verified 2026-10-26; brief date 2026-10-18)

Access date for all CLAIMs below: 2026-10-26. Confidence is stated per record.

### T-C03-owl-api — OWL API
| Field | Value |
|---|---|
| Official URL | https://github.com/owlcs/owlapi |
| Owner | OWL API community (owlcs; University of Manchester lineage, UNVERIFIED) |
| Latest version | 5.5.1 (Maven Central, 2024-09-08); repo pushed 2026-10-20 |
| Status | active, slow releases |
| Licence | dual LGPL-3.0 or Apache-2.0 (user's choice); weak-copyleft / permissive |
| Deployment | Java library, embedded |
| Air-gap | yes |
| Tier reason | Java ontology API; engine under Protege and many tools |

Reference JVM API for OWL 2 parse/serialise/reason (via HermiT, ELK, etc.). EOIP is Python, so use only through a sidecar or CLI for OWL 2 profile checks. Dual licence permits an Apache-2.0 election for redistribution. Touches CAP-09, CAP-23, CAP-10 (indirectly). **Decision:** INTEGRATE (optional sidecar for OWL/profile validation).
Evidence: CLAIM-owlapi-01 | 5.5.1 | "released under both LGPL v3 and Apache v2; free to choose" | README | https://github.com/owlcs/owlapi | accessed 2026-10-26 | 0.9. CLAIM-owlapi-02 | Maven latest 5.5.1 timestamp 2024-09-08 | search.maven.org API | 0.85.

### T-C03-owlready2 — Owlready2
| Field | Value |
|---|---|
| Official URL | https://pypi.org/project/owlready2/ ; dev repo https://bitbucket.org/jibalamy/owlready2 |
| Owner | Jean-Baptiste Lamy (single maintainer) |
| Latest version | 0.51 (2026-06-22) |
| Status | active, single maintainer; GitHub `pwin/owlready2` is a stale mirror (last push 2023-01) |
| Licence | LGPL-3.0-or-later (weak copyleft) |
| Deployment | Python library with SQLite quadstore |
| Air-gap | yes |
| Tier reason | Python ontology library; licence to verify |

Loads OWL 2 (NTriples, RDF/XML, OWL/XML), treats classes and individuals as Python objects, runs HermiT/Pellet (Java required) and SPARQL over an optimised SQLite quadstore. Redistribution: LGPL-3.0 permits use as an unmodified dynamically imported library with obligations (notice, relinking ability, modifications shared); the bundled Java reasoners carry their own licences (HermiT LGPL; Pellet licence UNVERIFIED). Flag for legal review, not a legal conclusion. Touches CAP-09, CAP-23. **Decision:** EXPERIMENT (offline reasoning/classification check in CI; not in the runtime).
Evidence: CLAIM-owlready2-01 | 0.51 2026-06-22 | LGPL-3.0-or-later, features | PyPI | https://pypi.org/project/owlready2/ | 0.85. CLAIM-owlready2-02 | mirror stale | GitHub API pwin/owlready2 pushed 2023-01-30, LGPL-3.0 | 0.8.

### T-C03-oops — OOPS! (OntOlogy Pitfall Scanner)
| Field | Value |
|---|---|
| Official URL | http://oops.linkeddata.es/ ; API http://oops-ws.oeg-upm.net/ |
| Owner | Ontology Engineering Group, UPM (Madrid) |
| Latest version | OOPS! 4 (UPM technology offer); date UNVERIFIED |
| Status | maintained web service, status UNVERIFIED |
| Licence | service terms NOT PUBLICLY VERIFIED; client DrOntoAPI is Apache-2.0 |
| Deployment | hosted web service + REST |
| Air-gap | no (hosted); local copy unknown |
| Tier reason | linting reference |

Detects common modelling pitfalls (catalogue of ~40 pitfalls; count UNVERIFIED) via REST. Cannot be used on confidential ontologies because ontologies are sent to a remote service (egress policy conflict). Use as a design reference for EOIP ontology lint rules (BL-32, CAP-41). Touches CAP-41, CAP-37. **Decision:** REFERENCE-ONLY (re-implement the pitfall catalogue as local lint rules).
Evidence: CLAIM-oops-01 | 2015 SWJ report | free, online, RESTful service | https://www.semantic-web-journal.net/node/989 | 0.7. CLAIM-oops-02 | DrOntoAPI Apache-2.0 client | https://www.sourceforge.net/projects/drontoapi | 0.6 (service licence not found).

### T-C03-skos-tooling — SKOS tooling (Skosmos, Skosify, qSKOS)
| Field | Value |
|---|---|
| Official URL | https://github.com/NatLibFi/Skosmos ; https://github.com/NatLibFi/Skosify ; https://github.com/cmader/qSKOS |
| Owner | National Library of Finland (Skosmos, Skosify); C. Mader (qSKOS) |
| Latest version | Skosmos v3.5 (2026-10-22); Skosify 2.3.0 (2021-08-31, dormant); qSKOS v2.0.4 (2024-06-01) |
| Status | Skosmos active; Skosify dormant; qSKOS low activity |
| Licence | Skosmos MIT; Skosify MIT; qSKOS GPL-3.0 (strong copyleft, legal-review trigger) |
| Deployment | PHP web app over Fuseki/SPARQL; Python CLI; Java CLI |
| Air-gap | yes (self-hosted) |
| Tier reason | vocabulary publishing and QA |

Skosmos browses SKOS vocabularies from a SPARQL endpoint; Skosify converts/cleans vocabularies to valid SKOS; qSKOS lists quality issues. EOIP has no SKOS management (CAP-12). qSKOS GPL-3.0 must not be linked into EOIP; run only as a separate offline tool, if at all. **Decision:** INTEGRATE Skosmos (optional UI over Fuseki, BL-06); REUSE Skosify (CLI in CI, with dormancy risk); REFERENCE-ONLY qSKOS (GPL).
Evidence: CLAIM-skos-01 | Skosmos v3.5 | MIT, release 2026-10-22 | GitHub API/LICENSE | https://github.com/NatLibFi/Skosmos | 0.9. CLAIM-skos-02 | Skosify 2.3.0 MIT, last push 2021 | PyPI/GitHub | 0.9. CLAIM-skos-03 | qSKOS GPL-3.0 v2.0.4 | GitHub API | 0.85.

### T-C03-widoco — Widoco
| Field | Value |
|---|---|
| Official URL | https://github.com/dgarijo/Widoco |
| Owner | Daniel Garijo (OEG-UPM lineage) |
| Latest version | v1.4.26 (2026-10-23) |
| Status | active |
| Licence | Apache-2.0 (permissive) |
| Deployment | Java CLI/JAR |
| Air-gap | yes |
| Tier reason | ontology documentation generator |

Generates HTML documentation (with WebVOWL visualisation and provenance) from OWL ontologies. Fits "ontology as code" release pipelines (BL-32): generate docs per tagged release. Touches CAP-41, CAP-42. **Decision:** REUSE (CI documentation step; JVM only in build).
Evidence: CLAIM-widoco-01 | v1.4.26 2026-10-23 | Apache-2.0 | GitHub API | https://github.com/dgarijo/Widoco | 0.9.

### T-C03-grafo — Gra.fo
| Field | Value |
|---|---|
| Official URL | https://gra.fo (docs at https://docs.data.world/en/66316-introduction.html) |
| Owner | data.world (acquired Capsenta, 2019-06) |
| Latest version | n/a (SaaS) |
| Status | end of life: data.world documentation states shutdown planned 2026-03-13; actual shutdown not independently confirmed |
| Licence | proprietary SaaS |
| Deployment | SaaS only |
| Air-gap | no |
| Tier reason | visual collaborative modelling SaaS |

Launched October 2018 as a real-time collaborative visual ontology/schema editor. Discontinued, so it is a historical reference for CAP-72 only; its closure also illustrates SaaS-modelling lock-in, supporting EOIP's open exportable ontology stance. **Decision:** REJECT (EOL); keep as REFERENCE-ONLY for UX.
Evidence: CLAIM-grafo-01 | support end 2026-03-13 | data.world docs | https://docs.data.world/en/66316-introduction.html | 0.6 (via search summary). CLAIM-grafo-02 | launch 2018-10 | W3C list post by J. Sequeda | https://lists.w3.org/Archives/Public/semantic-web/2018Oct/0087.html | 0.8.

### T-C03-ontotext-refine — Ontotext Refine (Graphwise Refine)
| Field | Value |
|---|---|
| Official URL | https://graphwise.ai/ (vendor rebranded from Ontotext; exact product page UNVERIFIED) |
| Owner | Graphwise (formerly Ontotext; rebrand per vendor listings) |
| Latest version | UNVERIFIED |
| Status | active (vendor describes it as free) |
| Licence | NOT PUBLICLY VERIFIED (OpenRefine upstream is BSD; this fork has been described as commercial in a forum post) |
| Deployment | desktop/server app with GraphDB integration |
| Air-gap | probably yes (UNVERIFIED) |
| Tier reason | RDF-ising OpenRefine fork |

OpenRefine-based tool adding visual RDF mapping and a CLI for turning tabular data into RDF. Overlaps EOIP CML mapping (BL-33) for tabular sources; legal-review trigger because licence is unknown. Upstream OpenRefine is covered in C04. Touches CAP-29, CAP-28. **Decision:** REFERENCE-ONLY.
Evidence: CLAIM-refine-01 | free app on OpenRefine with RDF mapping and CLI | vendor text via search | https://graphwise.ai/?p=168034 | 0.4. CLAIM-refine-02 | "commercial application" remark | https://forum.openrefine.org/t/how-to-have-ontotext-refine-as-plugin-in-graphdb/578 | 0.3.

### T-C03-ontoportal — OntoPortal / BioPortal
| Field | Value |
|---|---|
| Official URL | https://github.com/ontoportal ; https://www.bioontology.org/ |
| Owner | OntoPortal Alliance (consortium incl. Stanford NCBO lineage) |
| Latest version | ontoportal_web_ui v3.6.0 (2026-09-16); `ontologies_api` pushed 2026-06-09 |
| Status | active |
| Licence | repository licence shown as "other/NOASSERTION"; per-component terms UNVERIFIED; appliance 3.0 introduced licensing (free for most, fees evaluated for commercial users) |
| Deployment | Ruby/Rails virtual appliance, containers |
| Air-gap | yes (self-hosted), subject to licence |
| Tier reason | ontology repository platform |

Ontology repository with REST API, mappings, annotator and versioning of submitted ontologies; a mature reference for ontology catalogue and governance UX (CAP-41, CAP-42). The commercial-use licence wording makes it a legal-review trigger. **Decision:** REFERENCE-ONLY.
Evidence: CLAIM-ontoportal-01 | v3.6.0 2026-09-16, licence NOASSERTION | GitHub API | https://github.com/ontoportal/ontoportal_web_ui | 0.8. CLAIM-ontoportal-02 | appliance 3.0 licensing note | https://www.bioontology.org/wiki/OntoPortalVA | 0.5.

### T-C03-ontouml — OntoUML ecosystem
| Field | Value |
|---|---|
| Official URL | https://github.com/OntoUML/ontouml-js ; https://ontouml.org |
| Owner | OntoUML community (NEMO, UFES / Giancarlo Guizzardi lineage; UNVERIFIED) |
| Latest version | ontouml-js v1.0.0 (2026-07-26); VP plugin pushed 2026-06-30 |
| Status | active, small |
| Licence | Apache-2.0 (ontouml-js and VP plugin) |
| Deployment | JS library, Visual Paradigm plugin (VP is proprietary) |
| Air-gap | yes (library) |
| Tier reason | conceptual modelling reference |

UFO-grounded conceptual modelling language with model verification and transformation to OWL. Value: ontology-driven stereotypes (kind, role, phase) could guide EOIP ontology quality checks. Touches CAP-09, CAP-72. **Decision:** REFERENCE-ONLY.
Evidence: CLAIM-ontouml-01 | v1.0.0 2026-07-26, Apache-2.0 | GitHub API | https://github.com/OntoUML/ontouml-js | 0.85.

### T-C03-kbpedia — KBpedia
| Field | Value |
|---|---|
| Official URL | https://kbpedia.org ; https://github.com/Cognonto/kbpedia (UNVERIFIED path) |
| Owner | Mike Bergman / Cognonto (Structured Dynamics lineage) |
| Latest version | 2.50 (release folder); date UNVERIFIED |
| Status | low activity (UNVERIFIED) |
| Licence | CC BY 4.0 (content) |
| Deployment | OWL/CSV downloads |
| Air-gap | yes |
| Tier reason | upper KG reference |

Integrates Wikipedia, Wikidata, schema.org, DBpedia, GeoNames etc. with ~58k reference concepts (count UNVERIFIED) under the KKO upper ontology. Useful as an entity-typing vocabulary for the ingest classifier; attribution required. Touches CAP-12, CAP-28. **Decision:** REFERENCE-ONLY.
Evidence: CLAIM-kbpedia-01 | CC BY 4.0, 2.50 release | Bergman post | https://lists.w3.org/Archives/Public/semantic-web/2020Jun/0053.html | 0.7.

### T-C03-upper-ontologies — Upper and domain ontologies
Owner/URL per line; deployment: static OWL/RDF files; air-gap: yes. Tier reason: design references for the enterprise ontology.
- **BFO** (https://github.com/BFO-ontology/BFO): release 2019-08-26; CC BY 4.0.
- **gist** (https://github.com/semanticarts/gist): v14.1.0, 2026-04-17, active; CC BY 4.0.
- **DOLCE** (DUL, ISTC-CNR): version and licence UNVERIFIED (site unreachable); legal-review trigger.
- **schema.org**: CC BY-SA 3.0 per site terms (ShareAlike; legal-review trigger); release UNVERIFIED.
- **FIBO** (https://github.com/edmcouncil/fibo, EDM Council): MIT; quarterly releases; finance domain.
- **W3C ORG** (https://www.w3.org/TR/vocab-org/): Recommendation 2014-01-16; W3C document-use rules, exact licence class UNVERIFIED.

Relevance: starting points and alignment targets for the EOIP core ontology (organisation, people, roles) and JSON-LD import/export (BL-31); attribution/ShareAlike obligations must be tracked in release notices (CAP-79). Touches CAP-09, CAP-12, CAP-41. **Decision:** REUSE gist and ORG as alignment references; REFERENCE-ONLY BFO/DOLCE/FIBO; EXPERIMENT schema.org mapping after ShareAlike review.
Evidence: CLAIM-upper-01 gist v14.1.0 CC-BY-4.0 (GitHub API, 0.9). CLAIM-upper-02 BFO CC-BY-4.0, 2019-08-26 (GitHub API, 0.85). CLAIM-upper-03 schema.org CC BY-SA 3.0 (https://schema.org/docs/terms.html, 0.7). CLAIM-upper-04 FIBO MIT (https://github.com/edmcouncil/fibo, 0.9). CLAIM-upper-05 ORG Rec 2014-01-16 (https://www.w3.org/TR/vocab-org/, 0.9). All accessed 2026-10-26.
