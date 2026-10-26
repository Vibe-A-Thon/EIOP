# C02 AllegroGraph (Franz Inc.)

| Field | Value |
|---|---|
| Registry ID | T-C02-allegrograph |
| Tier | B (commercial RDF + neuro-symbolic positioning) |
| Versions examined | 9.0 (announced 2026-05-05); 8.4 (2025-05-06); 8.3 (Nov 2024); 8.0 (RDF-star, WebView, LLM/vector) |
| Verified on | 2026-10-26 (brief says 2026-10-18; several sources post-date that, so the real access date is recorded) |
| Worker | V16 (registry worker W09) |

## 1. Identity, current status, tier, sources
Franz Inc.'s commercial RDF/graph database, with a free capped edition. Current line is 9.0 (GraphTalker agent) [CLAIM-allegrograph-01]; 8.4 added NL-to-SPARQL over a vector store, FedShard improvements, Gruff v9 [CLAIM-allegrograph-02]. Licence: proprietary; free edition capped at 5M triples in v5-v7 docs (current cap not re-verified) [CLAIM-allegrograph-05]. Status: active, commercial. Peer deep dives: `C02-stardog.md`, `C02-ontotext-graphdb.md`, `C02-apache-jena.md`. Sources: Franz press room, product page, DBTA, edition pages (Appendix C).

## 2. Problem, workloads, workflows
Enterprise knowledge graphs needing RDF/SPARQL plus symbolic rules, geospatial/temporal queries, triple-level security and sharded federation. Workflows: load RDF, apply RDFS++ or OWL 2 RL, validate with SHACL, query with SPARQL or Prolog, ask in natural language (GraphTalker), explore in Gruff. EOIP link: J-journeys on reasoning and NL query (Master Prompt §14).

## 3. Feature inventory
| Feature | Status | Evidence |
|---|---|---|
| RDF/quad store, SPARQL | present | [CLAIM-allegrograph-03] |
| RDF-star | present (8.0+) | [CLAIM-allegrograph-03] |
| RDFS++ dynamic materialisation | present | [CLAIM-allegrograph-03] |
| OWL 2 RL precomputing materializer | present | [CLAIM-allegrograph-03] |
| SHACL validation | present | [CLAIM-allegrograph-03] |
| RDF-oriented Prolog rules | present | [CLAIM-allegrograph-03] |
| Geospatial / temporal types and range queries | present | [CLAIM-allegrograph-03] |
| FedShard sharding + federation | present | [CLAIM-allegrograph-03] |
| Multi-master replication, Helm/K8s | present (edition gating UNKNOWN) | [CLAIM-allegrograph-03] |
| Triple-level security filters, triple attributes | present | [CLAIM-allegrograph-03] |
| Vector store tied to KG; same security as graphs | present (8.4) | [CLAIM-allegrograph-02] |
| NL to SPARQL (8.4), GraphTalker agent (9.0) | present; accuracy NOT PUBLICLY VERIFIED | [CLAIM-allegrograph-01,02] |
| Gruff explorer incl. time machine | present | [CLAIM-allegrograph-03] |
| Ollama / external model support | present (8.3) | [CLAIM-allegrograph-04] |
| OWL DL / full reasoner, GQL/Cypher | absent / not found | no source |

## 4. Architecture diagram
```
 clients (SPARQL/HTTP, Prolog, Gruff, GraphTalker HTTP API)
        |
 +------ AllegroGraph server (single node | MMR cluster | FedShard shards) ------+
 | parser/planner (SPARQL, Prolog) -- reasoners (RDFS++ dynamic | OWL2RL mat.)   |
 | security filters (triple-level) -- SHACL -- vector store (LLM query examples) |
 | triple indices + attributes (proprietary layout, NOT PUBLICLY VERIFIED)       |
 +------------------------------------------------------------------------------+
        |  optional external LLM / Ollama for NL query
```

## 5. Under-the-hood reconstruction
Public evidence covers behaviour, not internals. Data model: quads plus per-triple attributes (used by security filters) [CLAIM-allegrograph-03]. Reasoning split is documented: RDFS++ is computed at query time ("no separate precomputation"), OWL 2 RL is a materialiser recommended when data changes infrequently [CLAIM-allegrograph-03]. Hypothesis (not verified): hexastore-style multi-index storage and a Lisp-hosted query engine. Storage layout, transaction isolation and planner statistics are NOT PUBLICLY VERIFIED. The NL pipeline stores query examples in the vector store and iterates schema inspection/test-run/refine (GraphTalker) [CLAIM-allegrograph-01,02]; hypothesis: few-shot retrieval of past queries, then execution feedback loop.

## 6. Inferred requirements
FR: SPARQL 1.1 endpoint, RDF-star, per-triple access filters, rule engine selectable per repository, SHACL gate. NFR: vector/KG security parity, offline model option (Ollama) for air gap, K8s deployability. EOIP should require the same security-model parity between graph and vector indexes (CAP-46).

## 7. Performance and resource model
No independent benchmark found in this run. Vendor claims are not restated. Reasoning cost model implied by docs: RDFS++ shifts cost to query time; OWL 2 RL shifts to write/load and storage growth. Failure modes: materialiser blow-up on frequently changing data (per Franz's own guidance), free-edition cap error on overage [CLAIM-allegrograph-05]. Uncertainty high.

## 8. Strengths
Mixed reasoning modes per repository; triple-level security plus vector governance; time-machine UI; integrated agentic NL query. Match: EOIP's tiered reasoning and ACL-aware retrieval (BL-18 gap) can exceed by enforcing ACL in retrieval first.

## 9. Limitations
Algorithmic: materialised OWL 2 RL cost on volatile data (documented trade-off). Operational: proprietary, edition gating of clustering UNVERIFIED. Friction: Prolog/Franz-specific rule dialect lock-in; conflicting edition pages (Free/Developer 50M/Enterprise) [CLAIM-allegrograph-05]. No SPARQL 1.2/RDF 1.2 claim found.

## 10. Deployment, licensing, viability
Self-hosted, Docker, Kubernetes/Helm, AWS/Azure marketplace, managed cloud. Air-gap: likely (on-prem, Ollama option) but licence server needs not verified. Licence proprietary; free edition capped; OEM/white-label terms NOT PUBLICLY VERIFIED -> legal review trigger.

## 11. Competitive delta vs EOIP baseline
BL-06 (Fuseki/GraphDB adapters only) lacks an AllegroGraph adapter; BL-30 in-house reasoner is subclass/disjoint/property-chain only vs RDFS++/OWL 2 RL; BL-29 partial SHACL vs native SHACL; BL-18 absent vs triple-level filters; BL-12 optional LLM hook vs GraphTalker.

## 12. Strength and inversion cards
STR-allegrograph-01 | AllegroGraph | security filters shared by graph and vector data | CLAIM-allegrograph-02,03 | closes EOIP BL-18 pattern | match | enforce principal filter in one policy layer used by search, vector, graph | test: user without ACL gets 0 snippets from either index (J5).
STR-allegrograph-02 | AllegroGraph | per-repository choice of dynamic vs materialised reasoning | CLAIM-allegrograph-03 | supports tiered reasoning | match | per-tenant reasoning profile | test: same query, both modes, result parity on LUBM-style fixture.
INV-allegrograph-01 | target AllegroGraph 9.0; materialised OWL 2 RL on changing data | limitation per vendor guidance | root cause: algorithm (full re-materialisation; *hypothesis* for internals) | alternative: incremental maintenance (see `C02-rdfox.md`); worse when rules non-Datalog | options: (a) integrate RDFox/other (b) native Datalog subset incremental (c) tiered reasoning with explanation | select (b)/(c) EXPERIMENT | POC: update 1% of triples, measure re-materialisation time vs full | dependencies: reasoner choice, tenancy | defensibility: explanation traces + ACL | decision EXPERIMENT. Seed hypothesis §10.5 (Stardog) not targeted here.

## 13. Per-capability decisions
CAP-23 OWL profile reasoning: REFERENCE/EXPERIMENT. CAP-10 SHACL: REUSE engine (pySHACL/RDF4J) not AllegroGraph. CAP-46 security parity: BUILD. CAP-58 NL-to-SPARQL loop: EXPERIMENT. CAP-15/02 as backend: DEFER (no adapter demand evidence).

## 14. Tests and acceptance
PROPOSED: (1) adapter conformance via BL-07 if ever built; (2) NL-to-SPARQL iterative-refinement harness vs one-shot on a fixed question set with a local model; (3) ACL leakage test on any retrieval stack; (4) obtain free-edition licence text for OEM review.

## 15. Risks and open questions
Edition limits current? Is a licence key needed offline? Is GraphTalker usable with local-only models? RDF 1.2 roadmap?

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Franz Inc., 9.0, proprietary |
| D2 | 2 | enterprise KG + agentic NLQ |
| D3 | 4 | server/MMR/FedShard |
| D4 | 5 | layout NOT PUBLICLY VERIFIED |
| D5 | 3 | RDF-star, SHACL |
| D6 | 5 | SPARQL/Prolog; planner unknown |
| D7 | 3,5 | RDFS++, OWL 2 RL, Prolog |
| D8 | 3,7 | MMR, FedShard; isolation unknown |
| D9 | 3 | federation; connectors unknown |
| D10 | N/A | not a focus; no ER found |
| D11 | N/A | temporal types only |
| D12 | N/A | not found |
| D13 | 3 | vector store, GraphRAG claim |
| D14 | 3,5 | NL to SPARQL |
| D15 | N/A | no governance workflow found |
| D16 | 3 | Gruff |
| D17 | 3 | HTTP API, Prolog |
| D18 | 3 | triple-level security |
| D19 | N/A | not documented |
| D20 | 7 | no verified numbers |
| D21 | 10 | free capped + paid |
| D22 | 9 | standard RDF I/O |
| D23 | N/A | no patents reviewed |
| D24 | App C | mostly vendor sources |

## Appendix B. Capability mapping
| CAP | AllegroGraph | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-02 | native | 03 | BL-06 partial | DEFER | P3 |
| CAP-10 | native | 03 | BL-29 partial | REUSE other lib | P2 |
| CAP-11 | native RDF-star | 03 | absent | EXPERIMENT | P2 |
| CAP-15 | native | 03 | BL-06 | REUSE | P2 |
| CAP-22/23 | native | 03 | BL-30 partial | EXPERIMENT | P1 |
| CAP-46 | partial (triple filters) | 03 | BL-18 absent | BUILD | P0 |
| CAP-53/55 | native vector | 02 | BL-14 partial | REFERENCE | P2 |
| CAP-58 | native | 01 | BL-12 partial | EXPERIMENT | P2 |

## Appendix C. Evidence records
| CLAIM | product/version/date | claim | class | source | pub/access | conf | contra |
|---|---|---|---|---|---|---|---|
| allegrograph-01 | 9.0, 2026-05-05 | 9.0 launched with GraphTalker iterative NL agent, HTTP API embeddable | Third-party report (press release) | Franz press room, https://allegrograph.com/press_room/franz-inc-launches-allegrograph-9-0-with-graphtalker-the-ai-agent-for-enterprise-knowledge-graphs/ | 2026-05 / 2026-10-26 | 0.6 vendor PR | none |
| allegrograph-02 | 8.4, 2025-05-06 | NL-to-SPARQL via vector store, vector governed by graph security, FedShard, Gruff v9 | Third-party report | DBTA, https://www.dbta.com/Editorial/News-Flashes/Franz-Inc-Launches-AllegroGraph-84-Supporting-Agentic-AI-Solutions-169344.aspx | 2025-05-06 / 2026-10-26 | 0.6 | none |
| allegrograph-03 | current product page | RDF-star, RDFS++, OWL 2 RL, SHACL, Prolog, geo/temporal, FedShard, MMR, security filters, Gruff | Officially documented | https://allegrograph.com/products/allegrograph/ | undated / 2026-10-26 | 0.75 | none |
| allegrograph-04 | 8.3, Nov 2024 | Ollama model support | Third-party report | https://allegrograph.com/press_room/franz-inc-enhances-allegrographs-neuro-symbolic-ai-features-with-support-for-additional-ai-models/ | 2024-11 / 2026-10-26 | 0.6 | none |
| allegrograph-05 | v5-v7 docs | free edition 5M triples; Developer tier conflicting | Officially documented (old docs) | https://allegrograph.com/allegrograph-editions/ ; Franz quick-start docs | undated / 2026-10-26 | 0.4 | pages disagree on Developer tier |

## Appendix D. Assumptions
Version 9.0 treated as current (no later release found). Implementation language and storage layout not asserted. Edition terms treated as unverified.
