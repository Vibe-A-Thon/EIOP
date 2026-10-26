# C04 — RML ecosystem (RMLMapper, RML-Streamer, YARRRML, Morph-KGC, SDM-RDFizer)

| Field | Value |
|---|---|
| Registry ID | T-C04-rml-tools |
| Tier | B — declarative mapping reference for BL-33 (CML/IR) |
| Versions examined | RMLMapper **8.1.0** (2025-12-23); RML-Streamer **2.5.0** (2023-06-02); YARRRML parser **1.12.2** (2025-10-22); Morph-KGC **2.10.0** (2026-01-20); SDM-RDFizer **4.7.5.15.4.1** (2026-09-25); kg-construct `rml-core` spec repo v0.2.0 (2026-03-16) |
| Verified on | 2026-10-18 |
| Worker | V12 |

## 1. Identity, current status, tier, and sources
| Member | Owner | Licence | Latest / last commit | Status |
|---|---|---|---|---|
| RMLMapper (`RMLio/rmlmapper-java`) | RML.io (Ghent IDLab) | MIT | 8.1.0, 2025-12-23; commit 2026-02-17 | active |
| RML-Streamer (`RMLio/RMLStreamer`) | RML.io | MIT | 2.5.0, 2023-06-02; commit 2023-06-08 | **stale** (no 2024-26 activity seen) |
| YARRRML parser (`RMLio/yarrrml-parser`) | RML.io | MIT | 1.12.2, 2025-10-22; commit 2026-06-11 | active |
| Morph-KGC (`morph-kgc/morph-kgc`) | Julián Arenas-Guerrero / UPM | Apache-2.0 | 2.10.0, 2026-01-20; commit 2026-10-15 | active |
| SDM-RDFizer (`SDM-TIB/SDM-RDFizer`) | SDM group, TIB Hannover | Apache-2.0 | 4.7.5.15.4.1, 2026-09-25 | active |
Evidence: [CLAIM-rml-01..06]. The RML spec itself is now developed by the W3C KG-Construction Community Group (repo `kg-construct/rml-core`) [CLAIM-rml-06]; it is a Community Group deliverable, not a W3C Recommendation (status per CG model; conf 0.7). R2RML is the W3C Recommendation (2012) that RML extends (from memory, conf 0.8). Ontop (OBDA) is a separate Tier A dive: `C04-ontop.md`. Sources (7): five repos/feeds, PyPI, LICENSE files.

## 2. Problem, workloads, workflows
Generate RDF from heterogeneous sources (CSV, JSON, XML, SQL, APIs) declaratively. Typical workflow: author YARRRML (YAML) -> convert to RML (Turtle) -> run RMLMapper/Morph-KGC/SDM-RDFizer -> load N-Quads into a triplestore; streaming variant via RML-Streamer on Flink/Kafka.

## 3. Feature inventory
| Feature | RMLMapper | RML-Streamer | YARRRML | Morph-KGC | SDM-RDFizer |
|---|---|---|---|---|---|
| Language | RML (some CG-RML) | RML | YAML to RML | R2RML, RML, RML 1.2 | RML |
| Inputs | xlsx, ods, CSV, JSON, XML, 4 RDBs, SPARQL, Web APIs | files, Kafka, TCP, JDBC | n/a | RDBs, tabular, JSON/XML, DataFrames, Neo4j, Snowflake, Databricks, HTTP | CSV, JSON, RDB, XML |
| Functions | FnO (most) | partial | n/a | FNML, Python UDFs | unknown |
| Processing | in-memory | Flink | n/a | pandas, partitioned | planned, optimised |
| Outputs | N-Quads, Turtle, TriG, JSON-LD, HDT; SPARQL UPDATE | N-Quads, JSON-LD, Kafka, MQTT | RML | RDF, RDFLib/Oxigraph | RDF |
| LPG output, PROV per row | absent | absent | absent | absent | absent |
RMLMapper lacks conditions, logical views, NoSQL, TPF [CLAIM-rml-01].

## 4. Architecture
```
YARRRML --(yarrrml-parser)--> RML mapping (RDF/Turtle)
RML + sources --> engine: [logical source iterators] -> [term maps/ function maps] -> [join / dedupe of triples] -> RDF sink
  RMLMapper: in-memory | Morph-KGC: pandas partitions | SDM-RDFizer: plan triples maps, hashed dup removal | RML-Streamer: Flink dataflow
```

## 5. Under-the-hood reconstruction
Common model: TriplesMap = logical source (+iterator, reference formulation) + subject map + predicate-object maps (referencing maps use joins). Execution: iterate rows, evaluate term maps, emit quads, deduplicate with a set. Morph-KGC partitions mappings to bound memory [CLAIM-rml-03]; SDM-RDFizer plans triples-map order and compresses structures in v4 [CLAIM-rml-05]; RMLMapper loads all data in memory, XML up to 10x [CLAIM-rml-01]; RML-Streamer output order is not preserved unless `--disable-local-parallel` and Kafka partitions can duplicate output [CLAIM-rml-02]. Internals beyond these documented behaviours are hypotheses.

## 6. Requirements inferred
Declarative, versioned mappings; engine independence via a spec; join and function support; large-source memory bounds; pushdown to RDBs (OBDA is the virtual counterpart); test-case conformance suites (RML test cases referenced by RMLMapper v7.0.0 and SDM-RDFizer 4.0) [CLAIM-rml-01][CLAIM-rml-05].

## 7. Performance and resource model
Only vendor/author claims: SDM-RDFizer authors state v4.0 was best in all their testbeds and used less peak memory than 3.6; benchmarks use 25% and 75% duplicate-rate data, hardware not given on the page [CLAIM-rml-05]. No independent benchmark was retrieved (UNVERIFIED). Failure modes: memory blow-up (RMLMapper), join cost for referencing maps, unordered/duplicated streams (RML-Streamer), Flink 1.14.5 pin [CLAIM-rml-02].

## 8. Strengths
| ID | Strength | Match/exceed |
|---|---|---|
| STR-rml-01 | Standards-track declarative mapping with conformance test cases and multiple interchangeable engines | INTEGRATE: accept RML/YARRRML import into CML IR (extend `mapping/r2rml.py`); run RML test cases in CI |
| STR-rml-02 | YARRRML human-friendly YAML authoring | EXPERIMENT: CML already similar; provide YARRRML-to-IR transpile |
| STR-rml-03 | Morph-KGC breadth of sources, stateful functions (e.g. reconciliation), permissive licence | INTEGRATE as optional RDF materialisation backend |
| STR-rml-04 | SDM-RDFizer triples-map planning | EXPERIMENT: reuse idea for executor ordering |

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | RDF-only output; PG semantics not expressible; in-memory joins |
| Operational | RML-Streamer stale since 2023; RMLMapper in-memory [CLAIM-rml-01] |
| Standards | RML spec still evolving (CG v0.2.0), conformance varies |
| Friction | verbose Turtle mappings; no mapping review/versioning |
INV-rml-01: *Target* RML engines. *Limitation:* RDF-only, no per-row PROV (proven by output lists; data model). *Options:* (a) Morph-KGC then import RDF; (b) RML import/export on the EOIP IR with loss report; (c) full RML engine. *Selected:* (b) plus (a) as bridge. *POC:* RML test-case pass list on the importer, loss report per unsupported construct. *Decision:* ADOPT (b). No Ontop seed hypothesis tested here.

## 10. Deployment, licensing, viability
All permissive (MIT/Apache-2.0), self-hosted, air-gap viable (file inputs); JVM (RMLMapper, Streamer), Node (yarrrml-parser), Python (Morph-KGC, SDM-RDFizer). Connectors in these tools read sources directly and write RDF, so EOIP must put them behind the mutation gateway (connectors never mutate the graph directly).

## 11. Competitive delta vs EOIP baseline (BL-33)
EOIP has CML, an engine-neutral IR and an executor (`mapping/cml.py`, `ir.py`, `executor.py`). `mapping/r2rml.py::R2RMLAdapter.import_r2rml_dict` consumes a parsed Python **dict**, not Turtle mapping graphs, and returns a `LossReport` that blocks lossless claims: an import stub, confirming "not R2RML/RML-conformant". **SQL check (cross-batch report):** `mapping/virtualization.py::OBDAPushdownEngine.rewrite_point_query` builds `f"SELECT {col_clause} FROM {table_name} WHERE {pk_col} = '{entity_id}' LIMIT 1;"` with no quoting or parameters: confirmed string interpolation, injectable through `entity_id`, table and column names. Mitigation: only `execute_point_query_mock` calls it; outside the file there are only exports in `mapping/__init__.py` and a test (grep, build copies excluded), so no production caller found. `pk_col` is hardcoded `"id"`. Verdict: real latent defect; parameterise before live use. Also missing: streaming mapping, function library, PG-aware conformance tests.

## 12. Cards
STR-rml-01..04; INV-rml-01.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| RML/R2RML import into IR (CAP-29) | BUILD (Turtle parsing, conformance suite) |
| YARRRML front-end (CAP-29) | INTEGRATE yarrrml-parser as optional tool |
| RDF materialisation backend (CAP-29, CAP-02) | INTEGRATE Morph-KGC optional |
| Streaming RML (CAP-26) | REJECT RML-Streamer (stale); DEFER |
| SQL pushdown (CAP-21) | BUILD with parameterised queries / Ontop for OBDA |
| Functions (FnO) | EXPERIMENT |

## 14. Tests and acceptance
Run official RML test cases against EOIP importer; differential output vs Morph-KGC on 3 mappings; SQL-injection test for `rewrite_point_query` (ids containing `'`); acceptance: zero injection, documented pass list.

## 15. Risks and open questions
RML spec churn; RDF-only semantics; stale Streamer; whether CML should become RML-compatible superset.

## Appendix A — Research-dimension coverage
| Dimension | Covered in | Summary or N/A reason |
|---|---|---|
| D1, D21 | 1,10 | licences, cadence, permissive |
| D2-D3 | 2,4 | RDF generation engines |
| D4,D5,D7,D11,D12,D13,D14,D16,D19,D23 | N/A | mapping engines: no storage, reasoning, time model, ML, retrieval or UI; patents not searched |
| D6,D8,D9 | 3,5,7 | mapping execution, memory and streaming limits, core ingestion |
| D10 | N/A | no ER |
| D15,D17 | 9 | no mapping review or versioning; CLI/libs |
| D18 | 10 | connectors bypass the mutation gateway |
| D20,D24 | 7 | author claims only; specs not read |
| D22 | 9 | RDF vs LPG loss |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-29 | native | rml-01,03 | BL-33 implemented, not conformant | BUILD/INTEGRATE | P1 |
| CAP-21 | absent | rml-01 | BL-33 stub | BUILD | P2 |
| CAP-26 | partial | rml-02 | n/a | DEFER | P3 |

## Appendix C — Evidence records
| CLAIM | product/version/date | claim | class | source | dates | conf | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-rml-01 | RMLMapper 8.1.0 | I/O, in-memory, XML 10x, unsupported list; MIT | Officially documented | https://github.com/RMLio/rmlmapper-java | 2025-12-23 | 0.9 | none |
| CLAIM-rml-02 | RML-Streamer 2.5.0 | Flink 1.14.5, Kafka caveats; MIT; 2023-06-02 | Officially documented | https://github.com/RMLio/RMLStreamer | 2026-10-18 | 0.9 | none |
| CLAIM-rml-03 | Morph-KGC 2.10.0 | Apache-2.0; sources; pandas partitions; commit 2026-10-15 | Officially documented | https://github.com/morph-kgc/morph-kgc | 2026-01-20 | 0.9 | none |
| CLAIM-rml-04 | YARRRML 1.12.2 | MIT; 2025-10-22 | Officially documented | https://github.com/RMLio/yarrrml-parser | 2026-10-18 | 0.85 | none |
| CLAIM-rml-05 | SDM-RDFizer 4.7.5.15.4.1 | Apache-2.0; TMP/TME; self-reported best performance | Vendor claim | https://github.com/SDM-TIB/SDM-RDFizer | 2026-09-25 | 0.8 | no independent benchmark |
| CLAIM-rml-06 | rml-core v0.2.0 | CG spec release 2026-03-16 | Officially documented | https://github.com/kg-construct/rml-core | 2026-10-18 | 0.7 | W3C status unconfirmed |
| CLAIM-rml-07 | EOIP HEAD | f-string SQL; dict-based R2RML adapter | Observed in source code | packages/eoip/mapping/virtualization.py:73; r2rml.py | 2026-10-18 | 0.95 | none |

## Appendix D — Assumptions
YARRRML parser capabilities and RML spec status taken from repo metadata and memory, not the spec text.
