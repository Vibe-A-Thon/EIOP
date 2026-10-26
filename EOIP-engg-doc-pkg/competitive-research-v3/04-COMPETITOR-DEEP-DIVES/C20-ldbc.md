# C20 LDBC benchmark family (SNB Interactive, SNB BI, FinBench, Graphalytics, SPB)

| Field | Value |
|---|---|
| Registry ID | T-C20-ldbc |
| Tier | B (the only audited, vendor-neutral graph-database benchmark family; backend-parity evidence for J14) |
| Versions examined | SNB spec 2.2.4 stable / 2.2.5-SNAPSHOT (ldbc_snb_docs); SNB Interactive v2 (work in progress); `ldbc_snb_bi` HEAD (no tagged release); FinBench v0.1 stable, v0.2 WIP; Graphalytics repo HEAD (no tagged release); SPB not re-examined beyond LDBC listing. HEAD observed 2026-10-26 |
| Verified on | 2026-10-26 |
| Worker | V33 |

## 1. Identity, current status, tier, and sources
Linked Data Benchmark Council (LDBC): non-profit; benchmarks listed at ldbcouncil.org: SNB Interactive, SNB BI, FinBench, Graphalytics, SPB [CLAIM-ldbc-01]. Code and specs are Apache-2.0 (docs, BI, Interactive v2 impls, FinBench docs, Graphalytics) [CLAIM-ldbc-02]. None of the code repos shows a tagged release; versions are branch/PDF versions. Use is "subject to the Fair Use Policy" [CLAIM-ldbc-01].

## 2. Primary problem, target workloads, example workflows
| Benchmark | Workload | EOIP use |
|---|---|---|
| SNB Interactive | OLTP-style short reads, complex reads, updates on a synthetic social network; v1.x auditable, v2 (deletes, larger scale) WIP [CLAIM-ldbc-03] | BM-01/02 latency shape, BM-03 ingest-with-reads, J7, J14 |
| SNB BI | Analytical queries over the same data; reference impls Neo4j (Cypher), Umbra (SQL), TigerGraph (GSQL) [CLAIM-ldbc-04] | J3/J9 impact-style multi-hop aggregation; J14 |
| FinBench | Transactional distributed graph (simple read, complex read, read-write, write) on financial data [CLAIM-ldbc-05] | Fraud/finance analogue for J15; weak fit otherwise |
| Graphalytics | Six graph algorithms on large graphs (BFS, connected components, PageRank named by LDBC) [CLAIM-ldbc-01, -06] | BL-43 algorithm scale test |
| SPB | RDF/SPARQL workload on a media ontology [CLAIM-ldbc-01] | CRA-024 Fuseki/GraphDB SPARQL load; low priority |

## 3. Feature inventory
| Item | Status |
|---|---|
| Synthetic data generator (Spark datagen, Parquet) | present [CLAIM-ldbc-03] |
| Workload driver (Java 17; create-validation, validate, benchmark modes) | present [CLAIM-ldbc-03] |
| Reference impls: Neo4j, PostgreSQL, SQL Server, Umbra (Interactive v2) | present; "readable, cross-validation, not performance" [CLAIM-ldbc-03] |
| HugeGraph, Neptune, JanusGraph, Fuseki implementations | absent from examined repos (UNVERIFIED elsewhere) |
| Audit | LDBC-approved auditor, commissioned [CLAIM-ldbc-04, -07] |
| Pre-generated data SF1..SF300 | present [CLAIM-ldbc-03] |
| Multi-tenancy, ACL, text, vector, temporal as-of, provenance | absent (not tested) |

## 4. Architecture diagram
```
Spark datagen -> Parquet (SF1..SF300) -> loader (system-specific)
params + update streams -> Java driver (scheduled ops, time_compression_ratio)
driver -> SUT (Cypher/SQL/GSQL impl) -> validation (cross-check vs reference) -> results/ + score script
audit: auditor + TCO statement -> "LDBC Benchmark Result" set
```

## 5. Under-the-hood (workload/generator/driver design)
- Generator is deterministic with scale factors; skewed correlated attribute distributions (design intent of SNB; spec not re-read, hypothesis).
- Interactive driver: operations scheduled against simulation time; goal is the lowest `time_compression_ratio` while 95% of queries start within 1 s of schedule [CLAIM-ldbc-03]. Updates mutate the DB, so reload/restore before every run [CLAIM-ldbc-03].
- Audited runs: warm-up 30+ min, measured phase 2+ h [CLAIM-ldbc-03].
- BI: `scripts/score-full.sh` prints summary and `.tex` tables; official results need code review and cross-validation [CLAIM-ldbc-04].

## 6. Functional and non-functional requirements inferred
FR: run SNB-style loader+driver against each EOIP backend adapter (BL-02.. adapters) with identical logical schema. NFR: reload/restore harness; scheduled-start-lag SLO metric; results labelled "not LDBC Benchmark Results".

## 7. Performance model: what it can and cannot show
Shows: throughput under latency SLO, query-plan quality on multi-hop joins, bulk-load. Cannot show: permission-aware retrieval, tenant isolation, ontology governance, GraphRAG quality, LLM paths, air-gap operation. Scores are not comparable across versions (v1 vs v2) or scale factors; audited vs unaudited are different classes. Academic comparison (arXiv:1907.07405) involved vendor tuning, see C01-tigergraph [CLAIM-tigergraph-11].

## 8. Strengths and how to match
Vendor-neutral, auditable, open. Match: adopt generator+driver unmodified for BM-01/02/03 on Tier 1/2 data.

## 9. Limitations
Verified: Interactive audits only on v1.x until v2 ships [CLAIM-ldbc-03]. Intentional: social-network schema, not enterprise. Licensing/legal: see section 10. Algorithmic dead-end: single-schema workloads reward engines tuned to it. Operational: large RAM/disk at high SF; auditor cost. Friction: no tagged releases.

## 10. Deployment, licensing, redistribution, publication restrictions
Code Apache-2.0 [CLAIM-ldbc-02]. Only audited results may be called "LDBC Benchmark Results"; other reports of non-audited results as such infringe the LDBC BENCHMARK trademark; derived work should attribute (CC BY 4.0 per policy); disclaimer "These are not LDBC Benchmark Results" suggested [CLAIM-ldbc-07]. Unaudited results allowed if stated as unofficial [CLAIM-ldbc-08]. Vendor DeWitt-style clauses are separate: TigerGraph Community licence forbids benchmark publication [CLAIM-tigergraph-04]; RDFox evaluation licence requires approval [CLAIM-rdfox-04]. Legal-review trigger: yes (trademark plus vendor terms). Air-gap: yes (Docker/Java/Spark local).

## 11. Competitive delta against baseline
BL-01..: no SNB harness found in baseline; BL-16 notes no benchmark vs plain RAG; U-06 no scale benchmarks. Delta: adopt SNB for storage/query layer only.

## 12. Strength and inversion cards
STR-ldbc-01 | LDBC | cross-validated driver+generator | CLAIM-ldbc-03 | credible backend-parity evidence for J14 | integrate | wrap driver with EOIP adapter, parity table | SF1 validation passes on 3 backends.
INV-ldbc-01 | Target SNB v1/v2 | workload ignores governance/ACL (hypothesis) | root cause semantics | EOIP adds "SNB+ACL" variant: same queries with principal filters | measure BM-04 overhead | EXPERIMENT; defensibility: tenant-aware workload is EOIP-specific. Falsifiable: overhead <10% (BM-04).
Seed hypotheses in Master Prompt 10.5: none validated for LDBC.

## 13. Per-capability decisions
CAP-78 harness: INTEGRATE (SNB driver/datagen). CAP-01/14/15 query speed: INTEGRATE SNB Interactive+BI subset. CAP-62 algorithms: INTEGRATE Graphalytics datasets. FinBench: DEFER. SPB: DEFER. Publishing audited LDBC results: REJECT (cost, not needed).

## 14. Tests and acceptance
(1) SF1 validation mode passes on Neo4j and HugeGraph adapters (J14). (2) Interactive on Tier 2 reports scheduled-start-lag p95 and BM-01/02 percentiles. (3) Label all outputs "not LDBC Benchmark Results". (4) Hash-check datagen output for reproducibility.

## 15. Risks and open questions
Trademark misuse in marketing; v2 release date unverified; whether HugeGraph/Neptune implementations exist in forks (UNVERIFIED); SPB current version unverified.

## Appendix A. Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Non-profit, Apache-2.0, no tags |
| D2 | 2 | Five workloads |
| D3 | 4,5 | Datagen, driver, SUT |
| D4,D5,D7,D9,D10,D11,D12,D15,D16,D18,D19,D21 | N/A | Benchmark, not a storage/product; no such features |
| D6 | 2,7 | Query workload shape |
| D8 | 5,7 | Updates, reload; no HA test |
| D13,D14 | N/A | not covered by LDBC (see text2cypher-bench) |
| D17 | 3 | Driver/impls |
| D20 | 7,9 | Latency SLO metric; no cost numbers verified |
| D22 | 3 | Cypher/SQL/GSQL impls |
| D23 | N/A | none found |
| D24 | 7 | Vendor-tuned comparisons flagged |

## Appendix B. Capability mapping
| CAP | Technology | Claim | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-78 | native | ldbc-03 | U-06 | INTEGRATE | P1 |
| CAP-14 | partial (impls) | ldbc-03 | BL-02.. | INTEGRATE | P1 |
| CAP-15 | partial (SPB) | ldbc-01 | BL adapters | DEFER | P3 |
| CAP-62 | native (Graphalytics) | ldbc-01 | BL-43 | INTEGRATE | P2 |
| CAP-77 | n/a (TCO statement in audit) | ldbc-07 | - | REFERENCE | P3 |

## Appendix C. Evidence records
| ID | Product/ver/date | Claim | Class | Source | Dates | Confidence | Contra |
|---|---|---|---|---|---|---|---|
| ldbc-01 | LDBC site | Lists SNB Interactive, BI, FinBench, Graphalytics (BFS, CC, PageRank), SPB; use subject to Fair Use Policy | Official | https://ldbcouncil.org/benchmarks/ | n/a / 2026-10-26 | 0.85 | none |
| ldbc-02 | repos | Apache-2.0 licences (docs, BI, Interactive v2 impls, FinBench, Graphalytics) | Official | github.com/ldbc/ldbc_snb_docs, ldbc_snb_bi, ldbc_snb_interactive_v2_impls, ldbc_finbench_docs, ldbc_graphalytics | n/a / 2026-10-26 | 0.85 | none |
| ldbc-03 | Interactive v2 impls | Driver modes, 95%/1 s rule, SF1-SF300, audited runs only v1.x, 30 min/2 h | Official | https://github.com/ldbc/ldbc_snb_interactive_v2_impls | n/a / 2026-10-26 | 0.8 | page may lag 2024 plan |
| ldbc-04 | SNB BI | Neo4j/Umbra/TigerGraph impls; audit needs code review | Official | https://github.com/ldbc/ldbc_snb_bi | n/a / 2026-10-26 | 0.8 | none |
| ldbc-05 | FinBench v0.1/0.2 | Workload files simple/complex read, read-write, write; v0.2 WIP | Official | https://github.com/ldbc/ldbc_finbench_docs | n/a / 2026-10-26 | 0.7 | none |
| ldbc-06 | Graphalytics | Six algorithms; recommends GraphBLAS/Umbra impls | Official | https://github.com/ldbc/ldbc_graphalytics | n/a / 2026-10-26 | 0.6 | algorithm names not all seen |
| ldbc-07 | Fair Use Policy | Audited by approved auditor and in results set to be "LDBC Benchmark Result"; trademark; attribution CC BY 4.0 | Official | https://ldbcouncil.org/benchmarks/fair-use-policies | n/a / 2026-10-26 | 0.8 (fetch summary) | none |
| ldbc-08 | LDBC FAQ | Unaudited results usable if stated unofficial; 2022 retrospective review of three partial publications | Official/third-party | https://ldbcouncil.org/faq | n/a / 2026-10-26 | 0.6 | review outcome not seen |

## Appendix D. Assumptions
Spec contents (query counts, metrics) not read; claims limited to repo READMEs.
