# C18-sql-pgq — SQL/PGQ (ISO/IEC 9075-16)

| Field | Value |
|---|---|
| Registry ID | T-C18-sql-pgq |
| Tier | B (ISO SQL graph extension; BL-59) |
| Versions examined | ISO/IEC 9075-16:2023 (1st ed., June 2023); Cor 1:2026 and a CD of a next edition (listed by UNE); PostgreSQL 19 RC 1 (GA planned 2026-11-19) |
| Verified on | 2026-10-26 |
| Worker | V32 |

## 1. Identity, current status, tier, and sources
**Published ISO/IEC standard, Part 16 of SQL:2023** ("Property Graph Queries"), first edition dated June 2023 (catalogues give 2023-05-31, 2023-06-01 and 30 Jun 2023), 269 pages [CLAIM-pgq-01]. UNE lists Cor 1:2026 and a next-edition CD (ISO/IEC CD 9075-16) [CLAIM-pgq-02]. Spec is paywalled. Implementations: **PostgreSQL 19** (committed 2026-03-16 as GRAPH_TABLE plus CREATE/ALTER/DROP PROPERTY GRAPH; Beta 1 June 2026; RC 1 out; GA planned 2026-11-19, so **not yet GA** at access) [CLAIM-pgq-03]; Oracle 23ai SQL property graphs and DuckPGQ extension exist (prior knowledge, not verified in this run, conf 0.5).

## 2. Primary problem, workloads, workflows
Query relational tables as a graph without a graph database. Workflows: define a PROPERTY GRAPH view over existing tables; run `GRAPH_TABLE(... MATCH ... COLUMNS ...)` inside ordinary SQL, joined with relational data.

## 3. Feature inventory
| Feature | Status |
|---|---|
| CREATE PROPERTY GRAPH (vertex/edge tables, keys, labels, properties) | in standard |
| GRAPH_TABLE with MATCH pattern and COLUMNS clause | in standard |
| Shared pattern-matching language with GQL (GPML) | in standard (prior knowledge, conf 0.7) |
| Read-only (no graph DML) | yes: updates go through SQL on base tables |
| Variable-length paths | in standard; **PG19 initial implementation lacks them** [CLAIM-pgq-03] |
| Public conformance suite | NOT PUBLICLY VERIFIED |

## 4. Architecture (specification structure, conformance classes)
```
SQL host language
  Part 16: PROPERTY GRAPH schema objects (views over tables)
        + GRAPH_TABLE table expression (pattern -> relational result)
  Conformance = SQL feature IDs (optional features within SQL conformance model)
```

## 5. Under-the-hood (formal semantics, complexity, what an implementation must do)
A property graph is a **derived view** over base tables: vertex/edge tables, key and foreign-key joins define edges. GRAPH_TABLE result is a relational (bag) table; SQL three-valued logic and NULL apply. The simplest conformant implementation is a **query rewriter to joins** — PG19 is described as exactly this, "not a graph storage engine" [CLAIM-pgq-03]. Fixed-length patterns rewrite to a fixed join tree (polynomial in data); variable-length and path modes need recursive CTE or a graph operator; with trail/simple semantics hardness arises as in GQL. Implementer must: resolve label expressions, keys, ensure edge endpoints reference vertex keys, apply path modes, and output columns typed.

## 6. Functional and non-functional requirements inferred
FR: relational authorisation (row-level security) applies through the base tables — an advantage for EOIP tenancy if used. NFR: deterministic mapping from graph view definition to tables; migration tooling for view changes.

## 7. Performance and resource model
Engine-defined; rewriter-based engines inherit relational optimiser strength and join cost for deep traversals. No numbers.

## 8. Strengths and use-case advantages
Reuses relational ACID, indexes, security, backup; no second store; one-node-first friendly; SQL standard status. Match for tenants with relational sources; exceed with source-ACL propagation (BL-18 gap) through RLS.

## 9. Limitations with root causes
| Class | Items |
|---|---|
| Algorithmic | deep traversals = many joins; no native adjacency |
| Operational | PG19 not GA at access; first impl. lacks variable-length paths; implementations uneven |
| Friction | read-only graph; schema = relational tables, not independent graph schema; paywalled spec |

## 10. Deployment, licensing, redistribution, viability
Standard paywalled. PostgreSQL licence is permissive (PostgreSQL Licence; prior knowledge, conf 0.8; separate deep dive). Patent declarations not checked. Air-gap: yes (PG local).

## 11. Competitive delta against EOIP baseline
BL-59 Partial: `sql_adapter.py` handles ANSI SQL SELECT over an ontology projection; no `GRAPH_TABLE`, no `CREATE PROPERTY GRAPH`, no emitter. BL-01 `GraphStore` has no SQL backend. **SQL/PGQ vs RDF/OWL**: it is a *closed*, key-based, relational view; node identity = primary key not IRI; no inference. Bridging RDF to PGQ requires choosing a relational layout (triple table loses typing; per-class tables need schema), semantic loss for blank nodes, language tags, open-world typing. PGQ vs LPG engines: no edge properties beyond edge-table columns; no dynamic labels.

## 12. Strength-adoption and inversion cards
STR-pgq-01 | SQL/PGQ + PG19 | graph queries over governed relational data with RLS | CLAIM-pgq-03 | tenant-safe one-node graph queries | integrate | `PostgresGraphStore` read path using GRAPH_TABLE; writes through relational tables via the mutation gate | cross-tenant leakage test with RLS = zero rows.
INV-pgq-01 | SQL/PGQ | traversal depth cost; no variable-length in PG19 | CLAIM-pgq-03 | algorithm/maturity: proven | options: quick = recursive CTE fallback; native = hybrid with HugeGraph for deep paths | POC: 1M-edge synthetic graph, depth 1–6, compare PG19 vs HugeGraph latency (hardware stated at run) | EXPERIMENT after PG19 GA.

## 13. Per-capability decisions
CAP-16 EXPERIMENT; CAP-04 INTEGRATE (PG as single-node substrate); CAP-47 EXPERIMENT (RLS); CAP-14 DEFER.

## 14. Concrete tests and acceptance
PostgreSQL regression tests for graph_table (in its source tree; contents not read); no public ISO suite found. Acceptance: matrix of EOIP query intents compiled to GRAPH_TABLE vs Cypher with equal row sets, RLS isolation test. **PROPOSED, not run.**

## 15. Risks and open questions
PG19 GA slip (planned Nov 19; beta 4 reverted features); Cor 1:2026 content; patent declarations; relational layout for ontology-typed data.

## Appendix A — Dimension coverage
| Dim | § | Summary |
|---|---|---|
| D1 | 1 | ISO 2023 |
| D2 | 2 | relational graph view |
| D3 | 4 | SQL host |
| D4 | 5 | tables as storage |
| D5 | 3,5 | property graph schema |
| D6 | 5,7 | rewriter |
| D7 | N/A | none |
| D8 | 6 | ACID via host |
| D9-D12 | N/A | out of scope |
| D13-D14 | N/A | later |
| D15-D17 | N/A | spec |
| D18-D19 | 6,13 | RLS tenancy |
| D20-D21 | 7,10 | no numbers |
| D22 | 11 | RDF/PGQ loss |
| D23 | 10 | unchecked |
| D24 | App C | catalogues; PG sources via search |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-16 | native | pgq-01,03 | BL-59 partial | EXPERIMENT | P2 |
| CAP-47 | partial (via RLS) | pgq-03 | BL-20 partial | EXPERIMENT | P1 |
| CAP-04 | n/a | pgq-03 | BL-01 | INTEGRATE | P2 |

## Appendix C — Evidence records
| CLAIM | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| pgq-01 | ISO/IEC 9075-16:2023 | 1st ed., June 2023, 269 pages, JTC 1/SC 32 | Officially documented (catalogues) | https://www.dinmedia.de/en/standard/iso-iec-9075-16/369273602 | 2023-06 / 2026-10-26 | 0.85 | date variants 05-31 to 06-30 |
| pgq-02 | UNE listing | Cor 1:2026; superseded by ISO/IEC CD 9075-16 | Officially documented | https://www.en.une.org/encuentra-tu-norma/busca-tu-norma/iso?c=079473 | 2026-10-26 | 0.6 | single source |
| pgq-03 | PostgreSQL 19 | GRAPH_TABLE committed 2026-03-16; rewriter, no variable-length; RC1; GA planned 2026-11-19 | Third-party report + project news | https://www.postgresql.org/about/news/postgresql-19-rc-1-released-3409/ ; https://www.depesz.com/?p=4467 | 2026 / 2026-10-26 | 0.65 | secondary summaries of commit |

## Appendix D — Assumptions
Oracle/DuckPGQ and GPML-sharing from prior knowledge. PG licence from prior knowledge.
