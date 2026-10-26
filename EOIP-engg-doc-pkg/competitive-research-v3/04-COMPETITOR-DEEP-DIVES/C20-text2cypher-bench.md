# C20 Text2Cypher / CypherBench-style evaluation sets

| Field | Value |
|---|---|
| Registry ID | T-C20-text2cypher-bench |
| Tier | B (J11 / CAP-58 evaluation; complements C08-text-to-query.md which holds system-level evidence) |
| Versions examined | Neo4j Text2Cypher dataset arXiv:2412.10064 (2024-12-13) via `neo4j-labs/text2cypher` HEAD; CypherBench arXiv:2412.18702 (ACL 2025 main), `megagonlabs/cypherbench` HEAD |
| Verified on | 2026-10-26 |
| Worker | V33 |

Cross-reference: C08-text-to-query.md [CLAIM-t2q-01..03, -06, -07] covers systems, TEXT2SPARQL challenge and safety patterns; this file covers the evaluation sets and metrics only.

## 1. Identity, current status, tier, and sources
(a) **Text2Cypher dataset** (Neo4j Labs): 44,387 instances per C08 [CLAIM-t2q-01]; repo CC0-1.0; experimental, "not part of Neo4j's supported product lineup"; 245 stars [CLAIM-t2c-01]. (b) **CypherBench** (Megagon Labs): 11 property graphs (7 in test split), published Dec 2024 to Jun 2025, ACL 2025; Apache-2.0 repo; Wikidata-to-property-graph engine and task generator released June 2025 [CLAIM-t2c-02]. "-style sets": TEXT2SPARQL challenge for SPARQL (200 DBpedia + 50 corporate questions in 2025, via C08) [CLAIM-t2q-07]; no public Gremlin benchmark found [CLAIM-t2q-06].

## 2. Primary problem, target workloads, example workflows
Measure whether generated Cypher is executable and correct. CypherBench targets full-scale graphs (C08: >10k questions, 7.8M entities) [CLAIM-t2q-02]. Workflow: load graph, give schema+question to model, execute, compare result sets.

## 3. Feature inventory
| Item | Text2Cypher dataset | CypherBench |
|---|---|---|
| Size | 44,387 (C08) | question count not on repo page (C08: >10k) |
| Graphs | many small/derived (UNVERIFIED) | 11 Wikidata-derived property graphs, 7 test |
| Metrics | page names none; paper metrics UNVERIFIED here | Execution Accuracy (EX), Provenance Subgraph Jaccard Similarity (PSJS), Executable % [CLAIM-t2c-02] |
| Reference score | none verified | gpt-4o-mini test: EX 0.3143, PSJS 0.4591, Executable 0.8739 (repo, vendor-of-benchmark number) |
| Fine-tuning split | yes | train+test on Hugging Face |
| Safety/mutation tests, ACL, tenancy | absent | absent |

## 4. Architecture diagram
```
Wikidata/KG -> property-graph engine -> graphs (Neo4j-loadable) + task generator -> (question, gold Cypher)
model(schema, question) -> Cypher -> run on DB -> EX / PSJS / executable% 
```

## 5. Under-the-hood (metrics)
EX: result sets of predicted vs gold query compared on execution (set equality; exact tie rules not read). PSJS: Jaccard similarity between the subgraphs (provenance) touched by predicted vs gold queries, crediting partially right traversals (design from paper abstract-level; implementation at `cypherbench/metrics/provenance_subgraph_jaccard_similarity.py`, not read) [CLAIM-t2c-02]. Executable % counts queries that run without error. Text2Cypher's original paper reports text-similarity style metrics (Google-BLEU, exact match: UNVERIFIED from page).

## 6. Requirements inferred
EOIP evaluation needs: execution-based scoring on EOIP's own schema (BL-08), dialect-neutral gold (typed QueryPlan), safety corpus (mutation, cross-tenant), top-3 candidate scoring for J11, and a reproducible local-model run.

## 7. Performance model: what it can and cannot show
Shows single-turn NL-to-Cypher accuracy on Wikidata-style graphs and on Neo4j-curated examples. Cannot show: ranked suggestions UX (J11), disambiguation dialogue, EOIP ontology specifics, read-only safety, tenant predicates, Gremlin/SPARQL parity. Hardware: CypherBench needs at least 64 GB RAM for the 7 test graphs and 128 GB for all 11 [CLAIM-t2c-02], which exceeds the 64 GB reference node for the full set.

## 8. Strengths and matching
Execution-based, graded (PSJS) scoring that exposes "executable but wrong" (C08 INV-t2q-01). Match by running CypherBench subset on Neo4j adapter and writing an EOIP-ontology set of about 200 questions with gold QueryPlans.

## 9. Limitations
Verified: Text2Cypher repo carries no separate dataset licence statement (repo-wide CC0) [CLAIM-t2c-01]; CypherBench hardware demand. Hypotheses: Wikidata-derived questions overlap pretraining data; gold queries may have multiple valid forms; single-turn only. Friction: graph deployment effort.

## 10. Deployment, licensing, redistribution, publication
Text2Cypher repo CC0-1.0; CypherBench repo Apache-2.0; underlying Wikidata licence and Hugging Face dataset card licences not verified (legal-review trigger: yes for redistributing graphs; keep as download-only). Neo4j Community/Enterprise licence terms for running the harness (GPLv3 Community; commercial Enterprise) belong to C01-neo4j; benchmark-publication clauses in vendor EULAs (e.g. TigerGraph CE, RDFox evaluation) apply if those engines are targets [CLAIM-tigergraph-04, CLAIM-rdfox-04]. Air-gap: yes after staging, with a local model.

## 11. Competitive delta against baseline
No NL-to-query evaluation found in baseline; no read-only validator evidence for BL adapters beyond C08 notes. Delta: EOIP must build its own ontology-specific set; external sets calibrate the harness only.

## 12. Cards
STR-t2c-01 | CypherBench PSJS partial-credit metric | t2c-02 | detects near-miss traversals | integrate | implement PSJS analogue over EOIP QueryPlan graph patterns | rank correlation with human judgement >= 0.7 on 100 items.
INV-t2c-01 | single-turn accuracy ignores safety and suggestion ranking (semantics, proven by metric list) | add mutation corpus (CREATE/DELETE/SET/CALL) and cross-tenant canary to the set, score top-3 | worse where gold plan has several valid forms. Falsifiable: 100% mutation rejection, 0 canary leaks, top-3 contains valid plan >= deterministic baseline +15 points (aligns with C08). Decision ADOPT.

## 13. Per-capability decisions
CAP-58 NL-to-query evaluation: INTEGRATE CypherBench metrics; BUILD EOIP-ontology set. CAP-14 Cypher: REFERENCE. SPARQL: INTEGRATE TEXT2SPARQL sets (via C08). Gremlin: DEFER (no set). Training on Text2Cypher data: DEFER.

## 14. Tests and acceptance
Local 7-14B model on reference node; CypherBench subset of graphs fitting 64 GB; report EX, PSJS, Executable% and refusal rate; plus EOIP set top-3 accuracy; log model, prompt, seed; no network.

## 15. Risks and open questions
Dataset licences; contamination; hardware; metric exact definitions unread; whether Text2Cypher paper metrics still standard.

## Appendix A. Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | CC0 / Apache-2.0 repos |
| D6 | 3,5 | Cypher execution scoring |
| D14 | all | primary dimension |
| D18 | 6,12 | query safety gap |
| D24 | 5,7,9 | contamination, definitions unread |
| D3-D5,D7-D13,D15-D17,D19-D23 | N/A | evaluation sets |

## Appendix B. Capability mapping
| CAP | Tech | Claim | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-58 | native (eval) | t2c-02 | none | INTEGRATE + BUILD | P1 |
| CAP-14 | partial | t2c-02 | adapters | REFERENCE | P2 |
| CAP-15 | partial (via C08) | t2q-07 | - | INTEGRATE | P2 |
| CAP-78 | native | t2c-02 | U-06 | INTEGRATE | P1 |

## Appendix C. Evidence records
| ID | Product/ver/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| t2c-01 | neo4j-labs/text2cypher | CC0-1.0, experimental, 245 stars, no separate dataset licence shown | Official | https://github.com/neo4j-labs/text2cypher | n/a / 2026-10-26 | 0.8 | dataset card may differ |
| t2c-02 | CypherBench | Apache-2.0; EX, PSJS, Executable; 11 graphs/7 test; 64/128 GB RAM; gpt-4o-mini reference scores; ACL 2025 | Official | https://github.com/megagonlabs/cypherbench ; arXiv:2412.18702 | 2024-12 / 2026-10-26 | 0.85 | none |
Also see C08 CLAIM-t2q-01, -02, -06, -07.

## Appendix D. Assumptions
Metric internals not read; dataset sizes taken from C08.
