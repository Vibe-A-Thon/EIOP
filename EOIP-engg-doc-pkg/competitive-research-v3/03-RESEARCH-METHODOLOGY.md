# 03 — Research Methodology

| Field | Value |
|---|---|
| Governing specification | `KNOWLEDGE_GRAPH_COMPETITIVE_RESEARCH_MASTER_PROMPT_v3.md` (v3.0, 564 lines; read in full on 2026-10-18) |
| Research cutoff (UTC) | 2026-10-18. Every version, licence and status in this package is "as verified on the access date recorded in its evidence record". |
| System under design | KnowGridFlow / EOIP, baseline in `01-SYSTEM-BASELINE.md` |
| Scope rule | Research, architecture and specification only. No production source code was modified (Master Prompt §0). |

## 1. Evidence rubric

Every substantive claim becomes an evidence record:

`CLAIM-ID | product / version / date | exact claim | classification | source title + URL | publication date + access date | confidence 0–1 + rationale | contradictory evidence`

### 1.1 Classifications (Master Prompt §8)

| Classification | Use when | Default confidence band |
|---|---|---|
| Observed in source code | We opened the code at a pinned tag/commit | 0.85–0.95 |
| Officially documented | Current official documentation, specification or release notes | 0.75–0.90 |
| Reproduced by our experiment | We ran it ourselves in this programme | 0.85–0.95 (none in this run except the EOIP baseline test run) |
| Independent benchmark | Third-party, reproducible, workload and hardware stated | 0.60–0.80 |
| Third-party report | Analyst, journalist, blog, conference talk not by the vendor | 0.40–0.65 |
| Reasoned inference | Derived by us from stated assumptions; assumptions written down | 0.30–0.60 |
| Unverified | Claim found but not checked, or a vendor marketing figure | ≤ 0.30 |

### 1.2 Rules applied by every worker

1. Vendor performance figures are recorded as **vendor claims** with their workload and hardware, never restated as fact. "Fastest", "petabyte-scale" and "orders of magnitude" are quoted, attributed and given `Unverified` unless independently reproduced.
2. Internals that are proprietary or undocumented are written **NOT PUBLICLY VERIFIED**; plausible designs are labelled *hypothesis*.
3. Source-available is never treated as permissive. Licence class comes from the licence text or the official licensing page.
4. Five actions are kept apart: reproduce a capability, adopt a design pattern, reuse an OSS library, integrate an engine, copy an implementation. Copying protected implementation assets is never recommended.
5. Renames, archival, end-of-life, roadmap-vs-shipped gaps and name collisions are resolved before comparison (Master Prompt §5).
6. No test is reported as passed unless it was run. Unrun tests are **PROPOSED**.

## 2. Research tiers (Master Prompt §3.3)

| Tier | Depth | Assigned when |
|---|---|---|
| A — full reconstruction | All 15 deep-dive headings (Master Prompt §9), all 24 research dimensions (§7) addressed or justified N/A, under-the-hood reconstruction blueprint, strength and inversion cards with validation experiments | supported/adapter backends, direct and closest commercial competitors, reuse/integration candidates for P0/P1, leading ontology platforms, GraphRAG and agent-memory systems, entity resolution, code intelligence |
| B — capability and architecture profile | All 15 headings in compact form, dimension coverage table, at least one strength or inversion card where material | important references and adjacent tools |
| C — inventory record | Verified identity, status, version, licence, owner, official URL, one-paragraph relevance note, decision | libraries, SDKs, narrow-relevance tools, research prototypes |

Each registry entry carries its tier reason. A grouped record (for example "OWL reasoners: ELK, HermiT, Openllet, Konclude, FaCT++") covers several named technologies that share one decision; every named member still gets its own identity line inside the record.

## 3. Parallel execution plan (single pass)

The programme ran as one continuous pass in the dependency order of Master Prompt §3.2:

1. Baseline (`01-SYSTEM-BASELINE.md`) — done first, by the coordinator, from code and a local test run.
2. Registry seed (`_work/registry-seed.txt`) — 329 entries, tiered, each assigned to one of 35 research workers.
3. **Deep dives — 35 parallel workers (W01–W35).** Each worker received this methodology, the baseline, Master Prompt §§4, 5, 7, 8, 9 and 10.3–10.4, and its assignment. The prompt's ideal of one worker per technology was adapted to one worker per coherent batch (1–26 entries, Tier A entries concentrated in small batches) because of concurrency limits; the depth floor per technology was kept. Each worker wrote its deep dives, a Tier C records file, a machine-readable registry fragment (`_work/registry-fragments/Wxx.json`) and proposed ADD/EXCLUDE/DEFER entries.
4. Cohort comparisons (`05-COMPARISON-COHORTS/`) — written after the deep dives, from their evidence.
5. Matrix and registers (`06`–`09`) — aggregated from the cards and capability decisions in the deep dives.
6. Architecture, ADRs, requirements, contracts (`10`–`13`, `18-ADRS/`).
7. Benchmark plan, POC specs, threat model, operations and cost (`15`–`17`, `20-POC-EXPERIMENTS/`).
8. Roadmap, traceability, IP register, open questions, progress tracker, executive summary (`14`, `19`, `21`, `22`, `23`, `00`).

| Worker | Scope |
|---|---|
| W01 | Apache HugeGraph deep baseline |
| W02 | Neo4j |
| W03 | Amazon Neptune; Azure Cosmos DB Gremlin |
| W04 | Memgraph; FalkorDB; RedisGraph (historical) |
| W05 | TigerGraph; JanusGraph |
| W06 | Kùzu, ArangoDB, NebulaGraph, ArcadeDB, Apache AGE, TypeDB, TerminusDB |
| W07 | Remaining C01 engines (Dgraph, GraphScope, Oracle, Spanner Graph, PuppyGraph + Tier C) |
| W08 | Stardog, Ontotext GraphDB, Apache Jena |
| W09 | Remaining C02 RDF/reasoning engines |
| W10 | Protégé/WebProtégé, TopBraid EDG, PoolParty, metaphactory |
| W11 | Remaining C03 ontology tooling |
| W12 | Senzing, Splink, Zingg, Ontop |
| W13 | Remaining C04 mapping/ER/alignment |
| W14 | C05 extraction |
| W15 | C06 catalogs |
| W16 | Palantir Foundry/AIP, Glean (enterprise), Atlassian Rovo/Teamwork Graph |
| W17 | Microsoft Graph/Copilot/Fabric, ServiceNow, Onyx |
| W18 | Remaining C07 work-graph and twin platforms |
| W19 | Microsoft GraphRAG/LazyGraphRAG, LightRAG, HippoRAG, Neo4j GraphRAG |
| W20 | Zep/Graphiti, Cognee, Mem0, Letta |
| W21 | Remaining C08 GraphRAG/memory |
| W22 | C09 agents, protocols, local serving |
| W23 | C10 vector/full-text/hybrid search |
| W24 | C11 graph ML |
| W25 | TinkerPop/Gremlin; C13 temporal/provenance/lineage |
| W26 | C14 acquisition/CDC/workflow |
| W27 | C15 code intelligence (part 1) |
| W28 | C15 code intelligence (part 2) |
| W29 | C16 visualisation |
| W30 | C18 standards |
| W31 | C17 research and personal knowledge mapping |
| W32 | C20 benchmarks and evaluators |
| W33 | C12 graph processing (except TinkerPop) |
| W34 | C19 security, policy, observability, supply chain |
| W35 | C08 Tier C records (name verification and inventory) |

## 4. Identifier conventions

| Object | Pattern | Example |
|---|---|---|
| Registry entry | `T-<cat>-<slug>` | `T-C01-neo4j` |
| Evidence record | `CLAIM-<slug>-NN` | `CLAIM-neo4j-07` |
| Strength-adoption card | `STR-<slug>-NN` | `STR-graphiti-zep-02` |
| Inversion card | `INV-<slug>-NN`; self-inversions `INV-SELF-NN` | `INV-protege-01` |
| Capability (shared taxonomy, §6) | `CAP-NN` | `CAP-46` |
| Baseline capability | `BL-NN` | `BL-18` |
| Gap | `GAP-NN` | `GAP-01` |
| Requirement | `REQ-<area>-NN` | `REQ-SEC-03` |
| ADR (this package) | `ADR-KG3-NN` (distinct from the existing ADR-001..010 and ADR-H15..H17) | `ADR-KG3-04` |
| Benchmark | `BM-NN` | `BM-05` |
| Journey | `J1`–`J16` (Master Prompt §14) | `J5` |
| Roadmap work package | `WP-KG3-NN` | `WP-KG3-02` |

## 5. Benchmark rules (Master Prompt §12)

- Test beds are local-first and reproducible: hardware, workload generator, dataset licence, query mix, warm-up, cache state, repetitions, variance, configuration and versions are stated before results.
- Graph retrieval is always compared with strong non-graph baselines (BM25, dense, hybrid, reranked) before any benefit is claimed (Master Prompt §5.3).
- No universal "fastest" claims. Regression thresholds and rollback conditions are defined per benchmark.
- Benchmark licences are checked for result-publication restrictions ("DeWitt clauses").
- In this run **no benchmark was executed**. Every benchmark in `15-VALIDATION-BENCHMARK-PLAN.md` is **PROPOSED**.

## 6. Shared capability taxonomy (used by every deep dive and by the master matrix)

| Summary dimension | CAP-IDs |
|---|---|
| Storage substrate | CAP-01 property-graph storage and indexing · CAP-02 RDF/quad storage · CAP-03 multi-model/document storage · CAP-04 embedded/single-node footprint · CAP-05 distributed scale-out, sharding, replication · CAP-06 bulk load and ingest throughput · CAP-07 supernode handling |
| Expressivity and semantics | CAP-08 schema, typing and constraint enforcement · CAP-09 ontology modelling (RDFS/OWL) · CAP-10 SHACL/shape validation · CAP-11 edge properties, reification, RDF-star, hyperedges · CAP-12 taxonomy/SKOS management |
| Query expressivity and speed | CAP-13 Gremlin · CAP-14 Cypher/openCypher/GQL · CAP-15 SPARQL · CAP-16 SQL/PGQ and SQL bridges · CAP-17 GraphQL API · CAP-18 cost-based optimisation, WCOJ, EXPLAIN/PROFILE · CAP-19 multi-hop, path and recursive queries · CAP-20 portable query IR and translation · CAP-21 federation and virtualisation (OBDA) |
| Reasoning | CAP-22 rule/Datalog materialisation (incremental) · CAP-23 OWL profile reasoning · CAP-24 explanation and proof traces · CAP-25 inconsistency handling |
| Ingestion and identity | CAP-26 connectors and CDC · CAP-27 idempotent event log, replay, DLQ · CAP-28 schema inference and automatic entity/relationship detection · CAP-29 declarative mapping (R2RML/RML) · CAP-30 deterministic identity keys · CAP-31 probabilistic entity resolution, merge/split, survivorship · CAP-32 unstructured extraction (parsing, NER, RE) · CAP-33 PII and secret detection at ingest |
| Temporal and versioning | CAP-34 bitemporal and as-of queries · CAP-35 branching, diff, merge, rollback · CAP-36 event sourcing and history · CAP-37 schema/ontology evolution and migration |
| Governance and lineage | CAP-38 provenance, evidence spans, claims · CAP-39 contradiction handling and truth maintenance · CAP-40 data lineage (OpenLineage-style) · CAP-41 ontology governance workflow (review, approve, release, rollback) · CAP-42 catalog and metadata management · CAP-43 epistemic separation (observed/inferred/predicted/approved) |
| Security and tenancy | CAP-44 authentication and SSO · CAP-45 RBAC/ABAC · CAP-46 ReBAC and source-ACL enforcement in retrieval and answers · CAP-47 multi-tenant isolation · CAP-48 audit integrity · CAP-49 query and prompt-injection defence · CAP-50 air-gapped/offline operation · CAP-51 LLM egress control · CAP-52 white-label/OEM packaging |
| Agentic / GraphRAG / NL-query stack | CAP-53 vector search · CAP-54 full-text search · CAP-55 hybrid retrieval and rank fusion · CAP-56 GraphRAG (local/global/community) · CAP-57 agent memory (write, expire, invalidate) · CAP-58 NL→query and query suggestions · CAP-59 MCP/agent tool interface · CAP-60 grounded answers with citations and abstention · CAP-61 local model serving |
| Graph analytics and ML | CAP-62 graph algorithm library · CAP-63 graph embeddings and KGE · CAP-64 GNN/link prediction with a prediction plane · CAP-65 temporal graph analytics |
| Code intelligence | CAP-66 precise code graph (symbols, cross-references) · CAP-67 incremental re-indexing · CAP-68 dependency and SBOM risk · CAP-69 change-impact digital thread |
| Visualisation and UX | CAP-70 large-graph rendering · CAP-71 investigation UX and visual query building · CAP-72 ontology visual editing and real-time co-editing · CAP-73 time-machine and graph-diff UX |
| Operations and cost | CAP-74 backup, restore, PITR · CAP-75 observability · CAP-76 HA and DR · CAP-77 licensing and TCO · CAP-78 evaluation and benchmark harness · CAP-79 supply chain (SBOM, signing) · CAP-80 organisational and process intelligence (process mining, ONA, decisions/wisdom) |

## 7. Priority formula (Master Prompt §13)

`PriorityScore = 0.25·CustomerValue + 0.20·StrategicFit + 0.15·RiskReduction + 0.15·EvidenceStrength + 0.10·ReuseLeverage + 0.10·Feasibility + 0.05·Differentiation − ComplexityPenalty` (inputs 0–5; penalty 0–2). Raw inputs, rationale and a sensitivity check are published with the gap register. The score supports judgement; P0 is forced for correctness, lineage, idempotency, permission and tenant protection regardless of score.

## 8. Limits of this method

- Web research covers public documentation, repositories, papers and release notes reachable on the access date. Paywalled analyst reports and private vendor documentation were not used.
- Product trials of commercial SaaS products were not performed (no accounts, no authorisation). Their internals are documented-or-hypothesis only.
- Benchmarks and proofs of concept were specified, not executed.
