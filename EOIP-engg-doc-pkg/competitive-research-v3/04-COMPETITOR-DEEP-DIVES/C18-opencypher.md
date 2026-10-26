# C18-opencypher — Cypher / openCypher

| Field | Value |
|---|---|
| Registry ID | T-C18-opencypher |
| Tier | B (de-facto LPG query language; BL-03, BL-04, BL-09) |
| Versions examined | openCypher repository (github.com/opencypher/openCypher, Apache-2.0); openCypher TCK Maven artifact `org.opencypher:tck` 2024.2 (listed July 2025); Neo4j Cypher 5 / Cypher 25 (2025.06 and 2026.02 release notes); Amazon Neptune openCypher |
| Verified on | 2026-10-26 |
| Worker | V32 |

## 1. Identity, current status, tier, and sources
Three things share the name: **(a)** openCypher: an open specification/grammar/TCK project originating at Neo4j (repo copyright Neo4j, Inc.; repo states it is not an official Neo4j product, maintained by Neo4j employees/contributors, "unsupported") [CLAIM-ocy-01]; **(b)** the vendor language **Cypher 5 / Cypher 25** inside Neo4j (vendor dialect); **(c)** the Neptune/Memgraph/FalkorDB/others' openCypher subsets (vendor dialects). Status: **de facto standard, not an ISO/W3C standard**; the project's mission is now to move implementers toward ISO GQL by adding GQL features incrementally [CLAIM-ocy-02]. Repo not archived at fetch (no archive banner); release/tag history not shown (UNVERIFIED cadence). Neo4j 2025.06 kept CYPHER 5 default with CYPHER 25 opt-in; 2026.02 notes Cypher 25 default for newly created organisations [CLAIM-ocy-03].

## 2. Primary problem, workloads, workflows
Declarative pattern matching over property graphs with ASCII-art patterns. Workflows: traverse 3-hop dependencies; MERGE-based upsert (BL-03 HTTP transactional Cypher); Neptune openCypher path (BL-04).

## 3. Feature inventory
| Feature | Status |
|---|---|
| MATCH/WHERE/RETURN/WITH, OPTIONAL MATCH, UNWIND, MERGE, CREATE, DELETE | openCypher 9 |
| Variable-length paths, shortestPath | openCypher 9 |
| Quantified path patterns, WHEN/ELSE, FILTER, REPEATABLE ELEMENTS | Neo4j Cypher 25 (vendor) |
| Constraints/indexes DDL | vendor-specific, not in openCypher spec |
| TCK (Cucumber features) | present, repo `/tck` |
| CIP (Cypher Improvement Proposals) process | present, repo `/cip` |

## 4. Architecture (specification structure, conformance classes)
```
Grammar (ISO WG3 BNF artefact) + reference semantics docs + CIPs
        |-> TCK (Gherkin) -> implementation conformance claims
Vendor dialects (Cypher 5/25, Neptune, Memgraph...) extend / diverge
```
There is no formal conformance class ladder; "openCypher compatible" is a TCK pass-rate claim, unverified per vendor.

## 5. Under-the-hood (formal semantics, complexity, what an implementation must do)
Data model: nodes with labels and property maps, directed typed relationships with property maps, parallel edges allowed, nulls with three-valued logic. Pattern matching uses **relationship isomorphism (no repeated relationships in a MATCH)** by default; GQL calls this a match mode, and Cypher 25's REPEATABLE ELEMENTS opts out. Semantics are specified informally plus a TCK; a formal semantics exists in research (Francis et al., SIGMOD 2018 — prior knowledge, conf 0.7). Expressive complexity of pattern matching with these path semantics can reach NP-hardness for trail/simple-path semantics. An implementation must: parse, plan (cost-based), enforce null and ordering semantics, handle MERGE atomicity, and expose the transaction model. **No entailment/ontology.**

## 6. Functional and non-functional requirements inferred
FR: parameterised queries; read-only role enforcement; query timeouts; tenant label/property scoping. NFR: never string-splice user input (Cypher injection); translation tests across dialects.

## 7. Performance and resource model
Engine-defined; no numbers. Failure modes: unbounded variable-length paths, Cartesian products, supernode expansion, MERGE contention.

## 8. Strengths and use-case advantages
Widest developer familiarity and tooling among graph languages; direct bridge to GQL. Match: accept openCypher-subset plans via typed IR rather than text pass-through.

## 9. Limitations with root causes
| Class | Items |
|---|---|
| Algorithmic | trail semantics hardness; planner-dependent path blowup |
| Operational | vendor drift; unsupported repo; TCK 2024.2 last listing; dialect-specific DDL |
| Friction | no ontology/entailment; "openCypher compatible" claims vary; Neo4j-owned copyright |

## 10. Deployment, licensing, redistribution, viability
Spec/TCK Apache-2.0 [CLAIM-ocy-01]. Neo4j Community GPLv3 / Enterprise commercial (prior knowledge; belongs to the Neo4j deep dive) — legal-review trigger for embedding, not for the spec. Air-gap: yes.

## 11. Competitive delta against EOIP baseline
BL-03/BL-04: HTTP Cypher adapters; BL-09 `ast_compiler.compile_cypher` emits query text, nothing executes it on Neo4j (01a); no GQL form. Semantics gap to RDF: Cypher relationship = object with identity and properties; SPARQL triple = fact. Mapping an RDF graph to Cypher mints edge identity (blank/IRI reifier) and cannot express open-world absence; mapping Cypher to RDF loses parallel-edge identity unless reified, relationship isomorphism has no RDF counterpart, labels are multi-valued types not classes with inference. Syntax similarity of `(a)-[:R]->(b)` and a triple is **not** equivalence.

## 12. Strength-adoption and inversion cards
STR-ocy-01 | openCypher | familiar pattern syntax + TCK | CLAIM-ocy-01 | developer onboarding | integrate (via IR) | compile typed plan to Cypher; run TCK subset as differential | pass rate by feature reported.
INV-ocy-01 | openCypher | project stewardship unclear ("unsupported"), dialect drift | CLAIM-ocy-01,03 | governance: proven | option: target GQL core + minimal Cypher subset by feature-flag per backend | POC: 100 plans, one per feature, across Neo4j, Neptune, HugeGraph | EXPERIMENT. Seed hypothesis on IR lock-in: not targeted.

## 13. Per-capability decisions
CAP-14 INTEGRATE (backend dialect emitted from IR); CAP-20 BUILD; CAP-18 REJECT (own planner); CAP-19 REUSE (variable-length via backend).

## 14. Concrete tests and acceptance
openCypher TCK (`org.opencypher:tck`; `/tck` features) run against each backend adapter with an allow-list of known-failing scenarios; injection tests on parameter binding. **PROPOSED, not run.**

## 15. Risks and open questions
TCK release cadence; whether Cypher 25 diverges from GQL; Neptune subset documentation not read.

## Appendix A — Dimension coverage
| Dim | § | Summary |
|---|---|---|
| D1 | 1 | status, owners |
| D2 | 2 | workflows |
| D3 | 4 | spec structure |
| D4 | N/A | storage engine-defined |
| D5 | 3,5 | no schema in spec |
| D6 | 5,7 | semantics |
| D7 | N/A | none |
| D8-D9 | N/A | engine-defined |
| D10-D12 | N/A | out of scope |
| D13-D14 | 6 | injection; NL-to-Cypher via IR |
| D15-D17 | 8 | TCK, CIPs |
| D18 | 6 | injection |
| D19 | N/A | none |
| D20-D21 | 7,10 | no numbers; GPL/commercial split |
| D22 | 11 | RDF/LPG |
| D23 | N/A | not assessed |
| D24 | App C | maintainer-statement sources |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-14 | native | ocy-01,02 | BL-03/04 | INTEGRATE | P1 |
| CAP-20 | absent | ocy-02 | BL-09 partial | BUILD | P1 |

## Appendix C — Evidence records
| CLAIM | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| ocy-01 | openCypher repo | Apache-2.0; TCK in /tck; CIPs in /cip; copyright Neo4j; unsupported; not archived | Officially documented | https://github.com/opencypher/openCypher | 2026-10-26 | 0.8 (page capture) | release history not shown |
| ocy-02 | openCypher site | With GQL published (April 11, 2024), mission is to help implementers evolve toward GQL, integrating GQL features incrementally | Officially documented | https://opencypher.org/ | undated / 2026-10-26 | 0.7 | date unclear |
| ocy-03 | Neo4j 2025.06, 2026.02 | CYPHER 5 default in 2025.06; Cypher 25 default for new organisations in 2026.02 | Third-party/vendor notes (search snippet) | https://neo4j.com/release-notes/database/neo4j-2025-06/ | 2025-07 / 2026-10-26 | 0.6 | 2026.02 page not fetched |
| ocy-04 | TCK 2024.2 | Maven Central latest listed July 2025 | Third-party report | https://central.sonatype.com/artifact/org.opencypher/tck | 2026-10-26 | 0.5 | snippet only |

## Appendix D — Assumptions
Formal-semantics paper, Neo4j licence from prior knowledge. "Active" judged by absence of archive banner, not commit dates.
