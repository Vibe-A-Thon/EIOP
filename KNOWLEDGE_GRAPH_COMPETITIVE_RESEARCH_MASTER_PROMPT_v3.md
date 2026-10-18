# MASTER PROMPT v3.0 — Enterprise Knowledge Graph, Ontology & Organizational Intelligence: Single-Pass Competitive Research → Architecture → Engineering Program

| Field | Value |
|---|---|
| Version | 3.0 (consolidates and supersedes all earlier drafts: the original research request, the category additions, Master Prompt v2.0, the launcher prompt, and the Con-to-Pro blueprint) |
| System under design | **KnowGridFlow / EOIP** (working name; candidate rebrand "Semaplexvell" — confirm spelling before use in any artifact) |
| Research cutoff | Determine at execution time. Record the UTC date and the exact version of every product, standard, and library examined. |
| Execution mode | **Single pass, all at once.** Every category, every technology, every dimension, and every deliverable is produced in one continuous, uninterrupted run. No phase-by-phase, category-by-category, or tool-by-tool stopping for approval. |
| Primary outcome | Evidence-backed competitor research converted into verified gaps, Con-to-Pro inversions, architecture decisions, implementation-ready requirements, tests, and a roadmap that makes our platform the strongest available option on its chosen workloads. |
| Legend | Items marked **(+)** were added during consolidation because the earlier drafts missed them. Treat them exactly like every other item. |

---

## 0. Invocation

Act on this entire document as a standing research-and-engineering protocol. Do not summarize it, and do not summarize the market in place of doing the work. Produce every artifact defined in Section 16 and enforce every gate in Section 17.

If browsing, repository access, file access, or code execution is unavailable, state that limitation once at the top of `00-EXECUTIVE-SUMMARY.md`, mark the affected claims UNVERIFIED, and continue with the strongest supportable analysis. Never claim to have tested software you did not run, read code you did not open, or verified a fact you did not check.

Do not modify production source code. This is a research, architecture, and specification mission. Implementation requires a separate, explicit request.

---

## 1. Operating persona

Act as an independent architecture review board that combines these roles:

- Principal enterprise knowledge graph architect and ontology scientist (RDF, RDFS, OWL 2 profiles, SHACL, SKOS, PROV-O)
- Property-graph and multi-model database engineer; graph query compiler and optimizer engineer
- Distributed systems, storage, and transaction engineer
- Graph algorithms, GNN, graph transformer, and neuro-symbolic AI scientist
- GraphRAG, LLM integration, agent-memory, and agent-orchestration architect
- Enterprise integration, CDC, streaming, and connector engineer
- Entity resolution, data quality, and information extraction scientist
- Knowledge governance, security, privacy, and multi-tenancy architect
- SRE, DevSecOps, and supply-chain security engineer
- Performance and benchmark engineer
- UX and visual analytics designer
- Product strategist, pricing and white-label/OEM analyst
- OSS licensing, patent/prior-art, and IP analyst **(+)**
- Skeptical technical auditor

Your job is to discover, verify, lawfully reconstruct, compare, design, test, and specify. Challenge competitor marketing and challenge assumptions about our own platform with equal rigor. Prefer clear, falsifiable conclusions over promotional language. Distinguish market differentiation from engineering superiority.

---

## 2. Mission and the meaning of "best of the best"

### 2.1 Mission

Research every named technology, plus the adjacent technologies required, to build an enterprise-wide, explainable, continuously evolving **living organizational knowledge fabric** — a sellable, white-label, multi-tenant, local-first "organization brain" usable by almost any organization, not only IT organizations.

For each technology:

1. Investigate its complete functional and technical surface — features, functionality, requirements, enhancements, architecture, internals, limitations, pros, and cons — in enough depth that a competent team could reconstruct equivalent behavior from public evidence.
2. Compare it against competing tools in the same workload class and against our verified baseline.
3. Identify what we are missing, what we have only partially, what we do weakly, and what we do unnecessarily.
4. **Adopt strengths:** decide how each verified strength should be matched, reused, integrated, or exceeded.
5. **Invert weaknesses:** turn each verified competitor weakness into a measurable advantage of our system (Con-to-Pro, Section 10).
6. Issue implementation-ready specifications for everything approved.

Deliver one cohesive system, not a collection of bolted-on products.

### 2.2 Honest definition of "best"

"Best of the best" means: on the workloads our customers actually run, our platform is demonstrably better in correctness, evidence, governance, explainability, operability, cost, and user value than the available alternatives — proven by reproducible benchmarks and acceptance journeys. It does **not** mean cloning every product, winning every benchmark against every specialized engine, or absorbing every feature. Reject features whose complexity outweighs their value. Never promise universal superiority.

---

## 3. Single-pass, all-at-once execution mandate

The user has explicitly required that everything be done at once rather than in phases, cohorts, categories, or tools with pauses between them. Honor that as follows.

### 3.1 What "all at once" means

- Execute the entire program — baseline, registry, every deep dive, every comparison, synthesis, inversions, architecture, requirements, contracts, tests, roadmap, and all deliverables — in **one continuous run**.
- Do not stop between categories or technologies to ask for confirmation, approval, or permission to continue.
- Do not ask clarifying questions. Where input is missing, record an assumption in `BASELINE_UNCERTAINTIES` and proceed.
- Do not output "Phase 1 complete — shall I continue?" or any equivalent. The only legitimate stop is the final completion report, or a hard environmental limit (Section 3.4).

### 3.2 How to achieve depth without phasing

Single-pass does not license shallowness. Coverage must not be bought by compressing each technology into three generic bullets.

- **Parallel fan-out.** If the execution environment supports subagents, workers, or parallel tasks, dispatch every technology deep dive simultaneously, each worker receiving Sections 4, 5, 7, 8, and 9 of this prompt plus the verified baseline. One worker per technology (at most two tightly coupled technologies per worker). Workers write their reports directly to files.
- **Write to files continuously.** Every deep dive, cohort comparison, and register is persisted the moment it is complete. Never hold the whole program in conversational output.
- **Dependency order inside the single run.** Some artifacts logically depend on others. Produce them in this order within the same uninterrupted run, without pausing:
  1. System baseline and uncertainties
  2. Deduplicated technology registry
  3. All deep dives (in parallel where possible)
  4. All workload-cohort comparisons (in parallel where possible)
  5. Capability matrix, gap register, strength-adoption register, inversion register
  6. Reference architecture, ADRs, requirements, data/ontology/event contracts, API/agent/security contracts
  7. Benchmark and validation plan, POC specs, threat model, operations and cost model
  8. Roadmap, traceability matrix, IP/prior-art register, progress tracker, executive summary (written last, because it summarizes everything)
- **Depth floor per technology.** Every deep dive must address every applicable dimension of Section 7 and every heading of Section 9, or mark it N/A with a reason. Breadth does not override the depth floor.

### 3.3 Proportionate depth

Depth is proportional to strategic relevance, not uniform. Tag every registry entry with a research tier:

- **Tier A — full reconstruction:** direct competitors, candidate components we may reuse or integrate, and any technology defining a capability we must match (all of the graph backends we support, the leading ontology platforms, GraphRAG and agent-memory systems, enterprise work-graph platforms, entity resolution, code intelligence).
- **Tier B — capability and architecture profile:** important references and adjacent tools.
- **Tier C — inventory record with verified status and a one-paragraph relevance note:** libraries, visualization SDKs, and tools with narrow relevance.

Tier C entries are still researched and recorded; they simply require fewer pages. Every tier assignment must state a reason.

### 3.4 Hard-limit fallback only

If, and only if, the environment physically ends the run (context, output, time, or tool quota), write `20-RESEARCH-STATE.md` with: completed items, partially completed items, pending items, evidence references, decisions taken, blockers, and the exact next action — so a fresh run can resume without repeating work. Never declare full coverage when only part was completed. This fallback is not a license to plan for phases.

---

## 4. System under design: baseline, constraints, and verification

### 4.1 First action — verify the baseline (same run, no pause)

Read every supplied requirement document, source tree, architecture doc, schema, connector contract, API, test, build file, ADR, and historical gap report. Produce `01-SYSTEM-BASELINE.md` and a `BASELINE_UNCERTAINTIES` section. If nothing is accessible, use the provisional baseline below, tag every item **USER-STATED / NOT CODE-VERIFIED**, and continue.

Every capability carries one status — **Implemented / Partial / Planned / Absent / Unknown** — plus an evidence pointer (file path and line, test name, or document section). Never infer code completion from requirements Markdown.

### 4.2 Baseline fields to fill (verify each against code)

| Field | Provisional value (verify) |
|---|---|
| Graph backend(s) | **Multi-backend by design.** Apache HugeGraph (RocksDB, standalone) is the current reference operational property graph; Neo4j and Amazon Neptune are required supported backends; others may be added. Verify which backend is authoritative in code today and whether a backend-abstraction layer exists. |
| Vector store(s) | Multiple vector databases are a stated requirement. Verify which exist. |
| Data model | Labeled property graph, plus planned ontology, meta-graph, and higher layers. Verify. |
| Knowledge layers | Instance graph → meta-graph / graph-of-graphs → ontology → "living brain" → **wisdom graph** and context-graph layer (planned). Verify which exist. |
| Reasoning | Unknown. Verify (none / rules / Datalog / OWL profile / SHACL validation). |
| Query languages | Gremlin (REST). Multiple graph and data query languages are a stated requirement (Cypher/openCypher, GQL, SPARQL, SQL, GraphQL — verify). |
| Natural-language query | Deterministic and non-deterministic NL querying with deep answers and reports; the system **suggests candidate queries** for the user to pick before execution. Verify status. |
| Backend stack | Python / FastAPI services and workers. Verify. |
| Frontend | React web and admin UI (a complete GUI redesign is planned — treat the current GUI as non-binding). Optional VS Code extension. |
| Deployment | Docker / Docker Compose; local-first; distributed scale-out later. |
| AI | Model-abstraction layer defaulting to local/self-hosted models and embeddings. Optional MCP / agent access, GraphRAG, agent orchestration, neuro-symbolic layer with GNNs over the multi-level hierarchy. |
| Ingestion | Generic JSON from arbitrary systems with **automatic entity and relationship detection**, building graphs, meta-graphs, and relationship graphs. Plus source-specific connectors. |
| Tenancy and packaging | **White-label, multi-tenant, fully customizable**, sold to organizations in any industry. |

### 4.3 Non-negotiable platform constraints

1. **Self-hosted, on-premises, local-first, air-gap capable.** No mandatory SaaS, cloud service, external LLM API, or internet dependency at runtime. Cloud deployment and cloud services are enabled only when a client explicitly requests them. Cloud-only products may be researched as competitors, never made mandatory dependencies.
2. **Data-egress policy for AI.** External LLM endpoints may be used only with explicit client confirmation under secured norms. Real client data never goes to external LLMs by default. The levels and types of shareable data are configurable policy parameters. The default is local models only.
3. **Graph-backend neutrality.** Do not silently replace, drop, or lock in any graph backend. Recommendations must respect the multi-backend requirement (HugeGraph, Neo4j, Neptune, and others) and must state, for every capability, whether it is backend-native, emulated in our layer, or unavailable on a given backend. Do not reimplement what a supported backend or a suitable OSS component already provides — mark it "available upstream / not integrated" instead.
4. **Canonical ingest-to-graph pipeline.** Source adapters → versioned source events → parsing / normalization / schema inference → entity identity and linking → evidence and provenance → ontology mapping and validation → governed graph mutation → indexing and intelligence → query / API / UI / agents. Connectors never mutate the authoritative graph directly.
5. **Living-graph mechanics.** Baseline plus incremental sync, replay, idempotency, deletions and tombstones, conflict reconciliation, graph-version history, source lineage, temporal validity, and relationship-preserving updates. Distinguish proposed mechanisms from verified code.
6. **Epistemic separation.** Observed facts, inferred facts, predictions, hypotheses, and human-approved assertions remain explicitly distinct, each with evidence, confidence and calibration, author or agent, source, model or rule version, and timestamps.
7. **Optional modules.** RDF/OWL/SPARQL/SHACL services, vector indexes, event buses, graph OLAP, and GNN stacks are optional modules, adopted only on demonstrated value.
8. **Permissions survive everything.** Source permissions are preserved through ingestion, indexing, retrieval, summarization, traversal, caching, memory, and agent actions. Least privilege, audit trails, read-only-by-default agents, typed and bounded query plans, and review gates for destructive operations.
9. **Tenant isolation (+).** Tenant data, models, embeddings, caches, indexes, logs, and agent memories are isolated; cross-tenant leakage is a P0 defect. White-label branding, configuration, ontology, and workflows are per-tenant and customizable.
10. **One-node first.** The platform must be practical on a single node before distributed scale-out. Cost every optional capability in CPU, RAM, disk, GPU, development time, maintenance, and operating complexity.
11. **Lawful research only.** Use public documentation, OSS code within license terms, published interfaces, papers, benchmarks, and independent experiments. No proprietary source, leaked material, bypassed access controls, or copied protected implementation assets.
12. **Redistribution-safe licensing (+).** Because the product is sold and white-labeled, every reused or integrated component must be checked for redistribution, OEM, SaaS, and embedding terms (e.g., GPL/AGPL/SSPL/BSL/Elastic/Commons Clause, community-vs-enterprise splits, patent clauses). Flag legal-review triggers.
13. **Preserve working functionality.** Recommend migrations only with backward compatibility, rollback, test coverage, and an approved ADR.

### 4.4 Reference source systems and traceability path

- **IT and engineering sources:** Jira, Confluence, ServiceNow (incidents, problems, changes, KB, CMDB), GitHub / GitLab / Bitbucket / Azure DevOps, repositories with code AST and symbols, CI/CD builds, API catalogs and documentation, Kibana, Datadog, Grafana, logs and observability, identity directories and service accounts.
- **General-enterprise sources (+)** (the product is for any organization): SharePoint, OneDrive, Google Drive, Teams, Slack, email, file shares, Salesforce and other CRMs, SAP and other ERPs, Workday and other HRIS, finance and procurement systems, policy and contract repositories, relational databases, data warehouses and lakes, spreadsheets, and arbitrary JSON/CSV/XML exports.
- **Reference digital-thread path:** Jira Story → Merge/Pull Request → Commit → Source File → Function/Class → Dependency → Pipeline/Build → Deployment → Incident → Documentation/Evidence.
- **Reference customer questions** (the system must answer these with evidence):
  - What is impacted if service account "abc" is changed or deleted?
  - Who changed this class in this API, when, and why?
  - Which systems change for a new feature?
  - What must be tested when a rule is added, updated, or deleted?
  - Which system or class caused an incident, and where should troubleshooting start?

---

## 5. Known corrections, ambiguities, and traps to resolve first

Resolve each of these during registry construction, with sources:

1. **Kùzu** — the official repository was reported archived on 10 October 2025. Verify status, licensing, and any community forks or successors (verify their names and activity). Study it for embedded graph architecture, columnar storage, and worst-case-optimal joins, but do not describe it as actively advancing without evidence. The earlier phrase "rapidly becoming the standard local engine for GraphRAG" is unverified — do not repeat it.
2. **Standards status** — ISO/IEC 39075 (GQL) was published in 2024 and SQL/PGQ (ISO/IEC 9075-16) in 2023. RDF 1.2, SPARQL 1.2, and SHACL 1.2 must be checked for their current W3C status at execution time. Always label: published standard / candidate or draft / de facto interface / vendor dialect.
3. **GraphRAG is not automatically superior to RAG.** Benchmark graph retrieval against strong non-graph baselines (BM25, dense, hybrid, reranked) before claiming benefit.
4. **Apache HugeGraph** already includes OLTP, separate computing engines (HugeGraph-Computer, Vermeer), HugeGraph-AI and HugeGraph-ML components, Gremlin and Cypher support, Hubble, Loader, and multiple storage backends. Distinguish what upstream provides from what our application must build.
5. **Blazegraph** — verify maintenance status and the Wikidata Query Service backend migration history; do not present Blazegraph as Wikidata's current long-term engine without checking.
6. **RedisGraph** reached end of life; FalkorDB is its successor lineage. Verify.
7. **Ambiguous or colliding names — identify the exact project before research:**
   - "Glean" = Glean (enterprise search and work graph, SaaS) **and** Glean (Meta's open-source code-indexing system). Research both, in different categories.
   - "Atlas" = several unrelated research-mapping products; Apache Atlas is a separate metadata catalog.
   - "CodeGraph", "Graphify", "code-review-graph", "grepai", "GitNexus" — multiple similarly named repositories exist; pin exact repos and owners.
   - "MythOS", "MemPalace", "Harmony MCP", "claude-mem" — verify existence, owner, maturity, and whether they are libraries, products, or personal projects. "MythOS" must not be confused with Anthropic's Claude Mythos model family.
   - "ContextClue Graph Builder", "InfraNodus" — verify vendor and scope.
   - "Actian Data Intelligence Platform" — verify current naming after acquisitions.
   - "Anzo / AnzoGraph" — verify current ownership and product status after acquisition.
   - "Microsoft Fabric graph / ontology features", "SAP knowledge graph", "ServiceNow knowledge graph" — verify what has actually shipped versus announced.
8. **Marketing claims** ("fastest", "petabyte-scale", "orders of magnitude") are recorded as vendor claims with their stated workload and hardware, never restated as facts.

---

## 6. Mandatory technology registry (deduplicated; expand where justified)

For each entry, verify: exact identity and official URL, owner, latest maintained version, release history, activity or archival status, license and usage terms (including redistribution/OEM terms), community-versus-enterprise feature boundaries, deployment modes, maturity, provenance of technical claims, research tier (A/B/C), and relevance to our platform. Correct renamed, discontinued, mis-described, or ambiguous entries before comparing. A technology that spans categories is researched once and cross-referenced.

### C01. Property-graph, multi-model, distributed, and embedded graph engines
Neo4j (Community and Enterprise, including Graph Data Science, Bloom, NeoDash, Aura for reference); Amazon Neptune (Database and **Neptune Analytics (+)**); TigerGraph; Memgraph (with MAGE); ArangoDB; JanusGraph; NebulaGraph; Dgraph; ArcadeDB; Azure Cosmos DB (Gremlin API); FalkorDB; Apache AGE; **Apache HugeGraph (deep baseline study — Server, Hubble, Loader, Computer, Vermeer, HugeGraph-AI, HugeGraph-ML, storage adapters)**; Kùzu and successors/forks; TypeDB (TypeQL); TerminusDB; SurrealDB; TuGraph; GraphScope / GraphScope Flex; **(+)** Ultipa; Oracle Graph (PGX / Property Graph); SAP HANA Graph; Google Spanner Graph; Aerospike Graph; PuppyGraph (graph query engine over existing SQL/lake data without ETL); DuckPGQ (SQL/PGQ on DuckDB); CozoDB (embedded Datalog + graph + vector); HelixDB (graph-vector database); Galaxybase; OrientDB and RedisGraph (historical lessons only).

### C02. RDF stores, semantic database engines, and inference engines
Stardog; Ontotext GraphDB; AllegroGraph; Apache Jena (TDB2, Fuseki, rule engines, SHACL); Blazegraph; Eclipse RDF4J; OpenLink Virtuoso; Cambridge Semantics Anzo / AnzoGraph; RDFox; Oxigraph; VLog; Soufflé (Datalog); **(+)** QLever; MillenniumDB; Corese; Amazon Neptune (RDF mode); HDT (compressed RDF); Comunica (federated SPARQL querying); Nemo (Datalog reasoner). Separate storage engines from editing and governance products.

### C03. Ontology, taxonomy, vocabulary, and semantic-governance engineering
Protégé; WebProtégé; TopBraid EDG; VocBench 3; PoolParty; metaphactory; Timbr.ai; KBpedia; ROBOT; OntoUML ecosystem; OOPS! (ontology pitfall scanner); pySHACL; SKOS tooling; ontology documentation and linting tools; OWL reasoners (HermiT, ELK, Pellet/Openllet); **(+)** Konclude; FaCT++; OWL API; Owlready2; LinkML (schema-as-code modeling language); Ontology Development Kit (ODK); Widoco (ontology documentation); Gra.fo (visual collaborative modeling); Ontotext Refine; OntoPortal / BioPortal; Wikibase and Semantic MediaWiki; reusable upper and domain ontologies as design references (BFO, gist, DOLCE, schema.org, FIBO, W3C ORG ontology). Distinguish design-time editors, reasoners, validators, and knowledge databases.

### C04. Semantic ETL, OBDA / virtualization, mapping, schema inference, ontology alignment, and entity resolution
Ontop; Morph-KGC; RML-Streamer; RMLMapper; SDM-RDFizer; OpenRefine and Wikidata reconciliation; Senzing; Zingg; Splink; Dedupe; **(+)** YARRRML; SPARQL-Generate; Karma; JedAI; py_entitymatching (Magellan); Ditto (deep entity matching); recordlinkage; LLM-assisted entity matching; ontology alignment (AgreementMakerLight, LogMap, OAEI systems); JSON/CSV schema inference and automatic entity-relationship detection tools. Cover R2RML/RML, mapping versioning, blocking strategies, merge/split, and survivorship.

### C05. Knowledge extraction from unstructured content **(+ new category)**
Document parsing: Apache Tika, Unstructured, Docling, Marker. Information extraction: spaCy, GLiNER, REBEL, ReLiK, coreference resolution, relation extraction, event extraction, table extraction, LLM-based schema-guided extraction (e.g., Neo4j LLM Graph Builder, LlamaIndex property-graph extractors). PII and secret detection: Microsoft Presidio, secret scanners. Evaluate precision/recall, evidence-span capture, and local-model viability.

### C06. Metadata catalogs, data governance, and lineage-aware enterprise context graphs
Atlan; Collibra; data.world; OvalEdge; Actian Data Intelligence Platform; DataHub; **(+)** OpenMetadata; Apache Atlas; Egeria; Amundsen; Unity Catalog (OSS); Apache Polaris; Alation; Informatica (CLAIRE / IDMC); Microsoft Purview; Google Dataplex; Marquez / OpenLineage (cross-reference C13). Separate catalog search from semantic inference, operational lineage, and knowledge intelligence.

### C07. Enterprise work graphs, operational ontologies, and organization-brain platforms **(+ new category — closest commercial competitors)**
Palantir Foundry Ontology and AIP; Glean (enterprise knowledge/work graph and search); Atlassian Rovo and the Teamwork Graph; Microsoft Graph, Microsoft 365 Copilot connectors, and Microsoft Fabric graph/ontology capabilities (verify what has shipped); ServiceNow knowledge graph and CMDB; SAP knowledge graph (verify); Salesforce Data Cloud; Onyx (formerly Danswer — open-source self-hosted enterprise search); Diffbot Knowledge Graph; Stardog Voicebox; Writer Knowledge Graph; Azure Digital Twins and DTDL; Eclipse Ditto; object-centric process mining (Celonis, PM4Py, OCEL 2.0) and organizational network analysis as graph patterns. These define what buyers already compare us against — research them at Tier A where evidence allows.

### C08. GraphRAG, LLM integration, organizational memory, and agent context
Microsoft GraphRAG and **LazyGraphRAG (+)**; LightRAG; HippoRAG (and **HippoRAG 2 (+)**); fast-graphrag; nano-graphrag **(+)**; Cognee; WhyHow.AI; Zep / Graphiti; LlamaIndex (PropertyGraphIndex); LangChain / LangGraph; InfraNodus; ContextClue Graph Builder; Harmony MCP; MemPalace; MythOS; claude-mem; Mem0; Letta (MemGPT); **(+)** Neo4j GraphRAG package; OpenSPG / KAG (Ant Group); RAPTOR; Think-on-Graph; G-Retriever; PathRAG; MiniRAG; StructRAG; RAGFlow; R2R; Kotaemon; Haystack; txtai; LangMem; A-MEM; text-to-query systems (Text2Cypher, text-to-Gremlin, text-to-SPARQL) and query-suggestion approaches. Verify every ambiguous name; never repeat unproven performance marketing.

### C09. Agent orchestration, tool protocols, and local model serving **(+ new category)**
Agent frameworks: LangGraph, AutoGen/AG2, Microsoft Agent Framework / Semantic Kernel, CrewAI, OpenAI Agents SDK, Claude Agent SDK, Google ADK, PydanticAI, DSPy. Protocols: MCP (and existing graph-database MCP servers), Agent2Agent (A2A). Local inference: Ollama, llama.cpp, vLLM, SGLang, Hugging Face TEI, ONNX Runtime. Embeddings and rerankers suitable for local use (BGE, E5, GTE, Nomic, Jina, ColBERT-style late interaction). Guardrails: NeMo Guardrails, Llama Guard, prompt-injection defenses.

### C10. Vector, full-text, and hybrid search engines **(+ new category)**
Qdrant; Milvus; Weaviate; pgvector; LanceDB; Chroma; OpenSearch (k-NN); Elasticsearch; Vespa; Tantivy / Lucene; native vector indexes inside graph engines (Neo4j, Memgraph, FalkorDB, Neptune Analytics, HugeGraph-AI). Evaluate multi-backend support, ACL-filtered search, hybrid rank fusion, incremental indexing, and tenant isolation.

### C11. Graph ML, GNNs, graph transformers, and neuro-symbolic AI
PyTorch Geometric (PyG); DGL; HugeGraph-ML; AmpliGraph; PyKEEN; DGL-KE; PyTorch Geometric Temporal; GraphGym; graph transformers (Graphormer, GraphGPS, maintained alternatives); temporal GNNs (TGN and frameworks); graph embeddings; link prediction; heterogeneous graph learning; graph foundation models where empirically useful; **(+)** GraphStorm; Neo4j GDS ML pipelines; TorchKGE / LibKGE; ULTRA (KG foundation model for link prediction); relational deep learning (RelBench); neuro-symbolic frameworks (Scallop, DeepProbLog, Logic Tensor Networks). Evaluate CNN/RNN/Transformer/GAN/SNN components only where they genuinely add graph intelligence, never as checkbox features.

### C12. Graph processing, algorithms, and large-scale computation
Apache TinkerPop / Gremlin; NetworkX; igraph; GraphX; GraphFrames; GraphScope; HugeGraph-Computer; Vermeer; Apache Spark graph workflows; GraphBLAS (SuiteSparse); RAPIDS cuGraph; **(+)** Raphtory (temporal graph analytics); Graphology; Rustworkx; Memgraph MAGE; Neo4j GDS; TigerGraph algorithm library; Ligra / GAP benchmark suite as algorithmic references. Cover centrality, community detection, subgraph matching, k-hop, shortest paths, anomaly detection, sampling, and distributed computation.

### C13. Temporal, event-sourced, versioned, provenance, and lineage infrastructure
TerminusDB (cross-ref C01); Graphiti (cross-ref C08); OpenLineage; Marquez; W3C PROV / PROV-O; event sourcing and CQRS; bitemporal modeling; audit/event logs; branching, diff, merge, rollback, snapshots, schema evolution, lineage propagation; **(+)** XTDB (bitemporal); Datomic; Fluree; Dolt; lakeFS; Apache Iceberg / Delta Lake time travel; Spline; AeonG-style temporal graph research. Compare application-layer temporal models with database-native history.

### C14. Enterprise acquisition, change data capture, streaming, and workflow
Apache NiFi; Airbyte; Apache SeaTunnel; Debezium; Kafka / Redpanda; Flink; NATS; Dagster; Airflow; Prefect; **(+)** Kafka Connect; Redpanda Connect (Benthos); dlt; Meltano / Singer; Apache Hop; Temporal (durable workflows); source webhooks and APIs. Cover rate limits, backfills, incremental crawls, checkpointing, replay, dead-letter queues, ordering, consistency, and source-ACL propagation. These are enabling technologies, not graph databases.

### C15. Code graphs, repository intelligence, software catalogs, and code RAG
Graphify; CodeGraph; code-review-graph; Repomix; grepai; GitNexus; Greptile; Sourcegraph / Cody; Augment Context Engine; Tree-sitter; SCIP / LSIF; Language Server Protocol ecosystems; CodeQL; Joern; Semgrep; **(+)** Glean (Meta, code indexing); Kythe; GitHub stack-graphs; srcML; OpenRewrite / Moderne (lossless semantic trees, multi-repo refactoring); CAST Imaging; SciTools Understand; SonarQube; Backstage software catalog, Port, and Cortex (service/ownership graphs); Dependency-Track and SBOM graphs; deps.dev and OSV; Aider repo map and IDE codebase indexes (Cursor, Continue). Require exact file/line/symbol/revision traceability, incremental reindexing, dependency impact, permissions, and CI integration.

### C16. Graph visualization, exploration, and UI toolkits
Gephi; Graphviz; Cytoscape / Cytoscape.js; Linkurious (Ogma); Kineviz / GraphXR; Constellation; Neo4j Bloom; yEd; CiteSpace; VOSviewer; KeyLines and ReGraph; yFiles; Graphistry; Cosmograph / cosmos.gl; Sigma.js; D3.js; vis-network / vis.js; Apache HugeGraph Hubble; **(+)** AntV G6; Neo4j NVL; react-force-graph; Reagraph; layout engines (ELK / elkjs, Dagre, WebCola, ForceAtlas2); Kumu and TheBrain (systems mapping). Compare rendering libraries separately from complete visual-intelligence products; cover WebGL/Canvas/GPU rendering and large-graph progressive disclosure.

### C17. Research, scientific literature, and personal knowledge mapping
Atlas (identify the correct vendor/product); ResearchRabbit; Connected Papers; OpenAlex; Wikidata; Protégé (cross-ref C03); **(+)** Semantic Scholar; Litmaps; Inciteful; scite (supporting vs contrasting citations — relevant to contradiction tracking); Elicit; Consensus; Obsidian; Logseq; Tana (typed "supertags"); Roam Research; Heptabase. Cover literature-graph import, citation provenance, semantic search, and contradiction tracking.

### C18. Interchange, query, ontology, and interoperability standards
RDF 1.1 and 1.2 (including the RDF-star lineage); Turtle, TriG, N-Triples, N-Quads, JSON-LD; RDFS; OWL 2 profiles (EL, QL, RL, DL); SHACL Core / SHACL-SPARQL and 1.2 drafts; SKOS; PROV-O; DCAT; schema.org; SPARQL 1.1 and 1.2 drafts; Cypher / openCypher; Gremlin; ISO/IEC GQL; SQL/PGQ; GraphQL; R2RML / RML; GraphAr; GraphML; GEXF; CSV; Parquet; Apache Arrow; OpenAPI / AsyncAPI; MCP; **(+)** PG-Schema and LPG schema proposals; NGSI-LD; DTDL; GeoSPARQL; OWL-Time; ODRL (usage policies); DPV (Data Privacy Vocabulary); CloudEvents; OpenLineage spec; W3C Verifiable Credentials (signed provenance); A2A. Label status precisely and test exact interoperability rather than inferring it from syntax.

### C19. Security, policy, privacy, observability, and operational tooling
Keycloak / OIDC / SAML; OPA / Rego; OpenFGA and relationship-based access control; authorization-aware search; ABAC; secrets management; provenance signing; SBOM and signature tooling; OpenTelemetry; Prometheus / Grafana; audit logging; OpenSearch where locally viable; backup/restore; release and container-hardening scanners; **(+)** SpiceDB (Zanzibar model); Cedar; Cerbos; Permify; Vault / OpenBao; Sigstore / cosign; Syft / Grype / Trivy; SLSA and in-toto; Presidio; OWASP Top 10 for LLM Applications and agentic-AI threat guidance; MITRE ATLAS. Treat as architecture references, not compulsory dependencies.

### C20. Benchmarks, workloads, and evaluators
LDBC (Social Network Benchmark Interactive and BI, FinBench, Graphalytics, Semantic Publishing Benchmark); GraphRAG-Bench; RAGAS; BEIR; LoCoMo; LongMemEval; code-retrieval and impact-analysis benchmarks; ontology reasoning and SHACL conformance suites; synthetic enterprise traceability datasets; **(+)** LUBM, BSBM, WatDiv, gMark (RDF/SPARQL); Open Graph Benchmark (OGB); multi-hop QA sets (HotpotQA, 2WikiMultiHopQA, MuSiQue, MultiHop-RAG); CRAG; STaRK (semi-structured KB retrieval); KILT; MTEB; ARES and TruLens (RAG evaluation); Text2Cypher / CypherBench-style text-to-query sets; SWE-bench, RepoBench, CrossCodeEval, CodeSearchNet (code); OAEI (ontology alignment); standard entity-resolution datasets. Record workload comparability and any license restrictions on publishing benchmark results (e.g., vendor "DeWitt clauses").

### Registry growth rule
Add a further technology only if it fills a demonstrable architectural or product gap, is a credible counterexample, or has meaningful ecosystem adoption. Record every addition or exclusion as **ADD / EXCLUDE / DEFER** with a one-line reason. Do not inflate counts for completeness theater, and do not drop any user-named technology without an explicit duplicate / rename / ambiguous / excluded resolution.

---

## 7. Mandatory research dimensions (per technology)

Cover every applicable dimension. Mark N/A with a justification rather than inventing internals. Link every substantive claim to an evidence record (Section 8).

1. **Identity and maturity** — identity, developer, versions, release cadence, governance, activity, archival/EOL, roadmap, license, patents, trademarks, enterprise restrictions.
2. **Problem and workloads** — customer segments, use cases, differentiators, core vs adjacent scope, suitability for on-prem local-first operation.
3. **Architecture decomposition** — components and services, data and control planes, tenancy, process boundaries, protocols, extension points, dependencies, network calls, deployment topology.
4. **Storage primitives and indexing** — RDF triples/quads vs property graph vs hypergraph; physical layout (hexastore SPO/POS/OSP permutations, adjacency lists, CSR/CSC, key-value layouts, columnar, B-tree, LSM, bitmap/roaring indexes, secondary and vector indexes); dictionaries and compression; read, write, and storage amplification.
5. **Schema and semantic expressivity** — strict vs optional schema, labels and typing, ontology profiles and their formal bounds, axioms, constraints, SHACL, cardinality, uncertainty, hyperedges, reification and quoted triples, properties on edges, cross-graph and graph-of-graphs relationships.
6. **Query pipeline and optimization** — dialects and conformance, parser → AST → IR → logical and physical plans, statistics and cost-based optimization, join algorithms (hash, merge, index nested loop, leapfrog trie join, worst-case-optimal joins), index seek vs scan, multi-hop, recursion, path algebra, full-text, geospatial, temporal, vector queries, EXPLAIN/PROFILE.
7. **Reasoning and inference** — RDFS/OWL rules, open vs closed world, monotonic vs non-monotonic, forward chaining (RETE, semi-naïve Datalog), backward chaining and query rewriting, tableaux, hybrid materialization, incremental maintenance and invalidation, inconsistency policy, proof and explanation paths, complexity on transitive closure and recursion.
8. **Transactions, concurrency, and scale** — ACID, isolation levels, MVCC, locking, consistency model, partitioning and sharding, consensus (Raft/Paxos), replication, fault tolerance, backup and restore, disaster recovery, bulk load, memory/disk/GPU footprint, ingestion-vs-query interference, supernode handling.
9. **Ingestion and federation** — connectors, streaming/batch/CDC, pushdown, OBDA, mapping, schema inference, deduplication, canonicalization, idempotency, deletes, rate limits, retries, replay, index freshness, conflict reconciliation.
10. **Identity and evidence** — entity resolution, alias/merge/split, match confidence, source authority, conflicting claims, claim-to-source spans, data contracts, PII and secret handling, source-ACL inheritance, temporal provenance.
11. **Time and evolution** — valid time vs transaction time, bitemporality, change capture, event sourcing, revisions, replay, branch/merge, "what changed and why", schema and ontology evolution, backward compatibility, rollback.
12. **Graph algorithms and ML** — analytics, anomaly detection, embeddings, GNNs, link prediction, feature lifecycle, drift, training-serving skew, explanation and uncertainty, separation of predictions from facts.
13. **Retrieval and agent integration** — text/vector/graph/hybrid retrieval, rank fusion, traversal guardrails, context construction, freshness, memory write/expire/delete rules, MCP tools, authorization, grounded answers with citations, LLM cost, latency, hallucination rate.
14. **Natural-language querying (+)** — text-to-query accuracy per language (Gremlin, Cypher, GQL, SPARQL, SQL), schema grounding, query suggestion and disambiguation, deterministic fallback, explanation of the executed query, safety of generated queries.
15. **Governance and authoring** — ontology workflows, semantic review, collaboration (including real-time co-editing and CRDTs), taxonomy lifecycle, semantic diff, schema migration, stewardship, approvals, audit, access control.
16. **Human experience** — web/desktop/API/CLI/IDE interfaces, onboarding, navigation, large-graph visualization, investigation workflows, data-quality UX, explanation UX, accessibility, internationalization and localization.
17. **Developer experience and extensibility** — SDKs, APIs, plugin architecture, documentation, testability, CI/CD and GitOps, migrations, debugging and explainability of inference chains.
18. **Trust and security** — authentication, RBAC/ABAC/ReBAC, tenant isolation, query injection, prompt injection, data and model poisoning, exfiltration, audit integrity, supply chain, resource limits, deployment isolation.
19. **Multi-tenancy and white-label (+)** — isolation model (database, schema, label, row/property), per-tenant ontology and configuration, branding, noisy-neighbor controls, per-tenant backup/restore and deletion, tenant-aware licensing and metering.
20. **Empirical economics** — p50/p95/p99 latency, ingest rate, storage per node and edge, memory per million nodes/edges, reindexing cost, build effort, ops burden, license and TCO, offline performance, upgrade risk, energy and hardware footprint.
21. **Commercial and licensing position (+)** — pricing model, packaging, community-vs-enterprise gating, redistribution/OEM/embedding terms, vendor lock-in levers, market positioning.
22. **Interoperability and lock-in** — import/export semantics, semantic loss when bridging RDF and LPG, query translation limits, migration paths, artifact portability, exit strategy.
23. **IP and prior art (+)** — notable patents or published methods that bear on our planned inventions, novelty risks, and freedom-to-operate flags for legal review (record, do not give legal conclusions).
24. **Research quality** — source quality, reproducibility, version, hardware, dataset, counterclaims, uncertainty, applicability to our platform.

---

## 8. Evidence and lawful reverse-engineering protocol

For every substantive claim, create an evidence record:

`CLAIM-ID | product / version / date | exact claim | classification | source title + URL or permalink | publication and access date | confidence 0–1 with rationale | contradictory evidence`

Classifications: **Observed in source code / Officially documented / Reproduced by our experiment / Independent benchmark / Third-party report / Reasoned inference / Unverified.**

- Prefer official specifications, current documentation, source code and release tags, test suites, and peer-reviewed papers. Vendor figures require explicit workload and hardware context; never compare unlike tests.
- Use lawful black-box testing, open-source inspection, public architecture disclosures, and independent reference implementations. Where internals are proprietary or undocumented, write **NOT PUBLICLY VERIFIED** and present plausible designs as hypotheses.
- Distinguish five actions: reproduce a capability, adopt a design pattern, reuse an OSS library, integrate an engine, copy an implementation. Never recommend unauthorized copying.
- Check recent releases, archived repositories, security advisories, and standards status at execution time. Flag renames, roadmap-vs-shipped mismatches, and cross-category tools. Never infer license permissiveness from source availability.

---

## 9. Per-technology deep-dive template

Write `04-COMPETITOR-DEEP-DIVES/<category>-<slug>.md` for every Tier A and Tier B technology, and a compact record for Tier C, using these numbered headings:

1. Identity, current status, tier, and sources.
2. Primary problem, target workloads, concrete example workflows.
3. Feature inventory — present / partial / optional / enterprise-only / absent / unknown — across UI, API, CLI, SDK, and integrations.
4. Text-based architecture diagram — boundaries, flows, state, control and data planes.
5. **Under-the-hood reconstruction** (as a blueprint to re-implement equivalent behavior from scratch): data model; storage layout and indexing; query pipeline and planning; reasoning; concurrency and transactions; partitioning and consistency; caching; versioning; security. Include pseudocode and public code entry points only where supportable.
6. Functional and non-functional requirements inferred from verified behavior.
7. Performance and resource model — methodology, hardware, dataset, scaling behavior, uncertainty, failure modes.
8. Strengths and use-case-specific advantages — and how each could be matched or exceeded.
9. Limitations with root causes — separating verified defects, intentional trade-offs, licensing restrictions, user-reported complaints, outdated claims, and hypotheses. Organize root causes as: algorithmic dead-ends (e.g., OWL DL complexity, supernode traversal degradation), operational and hardware overhead (RAM, GC pauses, indexing lockups, cold starts), and user/developer friction (learning curve, SDK gaps, opaque inference, restrictive licensing).
10. Deployment, licensing, redistribution, and operational viability under our constraints.
11. Competitive delta against our verified baseline, with evidence links.
12. Strength-adoption cards and Con-to-Pro inversion cards (Section 10), each with a validation experiment, feasibility, and side effects.
13. Per-capability decisions — **BUILD / REUSE / INTEGRATE / EXPERIMENT / DEFER / REJECT** — not per vendor.
14. Concrete tests, proof-of-concept, and acceptance conditions.
15. Risks, trade-offs, and open research questions.

Never assert a competitor's exact physical index, optimizer, or transaction mechanism without published or source-level proof. Derive complexity claims only from stated assumptions.

---

## 10. Comparison, gap discovery, strength adoption, and Con-to-Pro inversion

### 10.1 Two comparison types

- **Cross-competitor, within a coherent workload class:** ontology authoring vs ontology authoring; LPG engines vs LPG engines; triplestores vs triplestores; GraphRAG vs strong plain RAG; work-graph platforms vs work-graph platforms; and so on. Include HugeGraph, Neo4j, Neptune, and our platform as reference columns wherever applicable. Write one file per cohort in `05-COMPARISON-COHORTS/`.
- **Competitor vs our system,** remembering that ours is a composed enterprise knowledge platform, not a replacement for every database or visualization SDK.

### 10.2 Master capability matrix

Columns:

`CAP-ID | capability / sub-capability | user problem | competitors + verified evidence | common vs differentiator | our status (Implemented/Partial/Planned/Absent/Unknown) + code/doc evidence | backend support (HugeGraph / Neo4j / Neptune / other: native, emulated, unavailable) | gap class | gap severity | technical options | BUILD/REUSE/INTEGRATE/EXPERIMENT/DEFER/REJECT | priority P0–P3 | dependencies | tests | effort range | risks`

Include at least these summary dimensions: storage substrate, expressivity and semantics, query expressivity and speed, reasoning, ingestion and identity, temporal and versioning, governance and lineage, security and tenancy, agentic / GraphRAG / NL-query stack, visualization and UX, operations and cost.

**Gap classes:** Missing; Partial; Performance; Quality; Security; Interoperability; Operability; UX; Research gap; Competitive deficit; Unnecessary complexity. Never mark a capability "missing" if a supported backend or the project already provides it — mark "available upstream / not integrated".

### 10.3 Strength-adoption register **(+)**

For every verified competitor strength relevant to our customers: `STR-ID | competitor | strength | evidence | value to our customers | match / exceed / integrate / reject | design approach | acceptance test`. Gaps are not only weaknesses to exploit — they are also strengths we must reach parity on.

### 10.4 Con-to-Pro inversion engine (verifiable, not rhetorical)

For every material competitor drawback, create an inversion card:

- **INVERSION-ID**; target, version, workload; evidence-supported limitation.
- **Root cause** (data model, algorithm, coupling, storage, deployment, semantics, governance, UX, licensing, or maturity), marked proven or hypothesis.
- Why an alternative design mitigates it — and when that alternative would be worse.
- **Three options:** quick integration; pragmatic native enhancement; long-term differentiated architecture.
- Selected option, trade-offs, design pattern, diagram/pseudocode/API sketch.
- Falsifiable benchmark or POC with dataset, success metric, and cost/resource baseline.
- Dependencies, migration, backward compatibility, security and privacy failure cases.
- **Defensibility:** why the customer value persists if competitors copy the idea.
- **Decision:** ADOPT / EXPERIMENT / DEFER / REJECT.

**Apply the same engine to our own platform's weaknesses (+).** Every verified weakness of ours gets a card too.

### 10.5 Seed inversion hypotheses (validate or reject each — none is pre-approved)

| Target limitation (verify) | Hypothesized root cause | Candidate inverted design for our system |
|---|---|---|
| Protégé: desktop-bound, effectively single-user, struggles beyond client RAM | Desktop client with in-memory model, no storage abstraction | Headless web-native ontology engine over out-of-core storage, with multi-user collaboration (evaluate CRDT/OT vs locking), semantic diff, and review workflows |
| TopBraid EDG: heavy enterprise footprint, slow time-to-value | Monolithic server stack and complex configuration | GitOps-native ontology-as-code (Turtle/LinkML/YAML) with CI SHACL tests, semantic diff, release, and rollback — plus a visual editor writing to the same source |
| Stardog: query-time reasoning can cause latency variance; high license cost | Backward-chaining query rewriting over complex axioms | Tiered hybrid materialization: incremental forward-chaining of tractable profiles (RL/EL fragments, Datalog) at ingest, lightweight path rewriting at query time, with explanation traces |
| Neo4j: weak formal semantics and no native reasoning; schema-optional models can decay | LPG optimized for traversal without an axiom/validation layer | Typed property graph with SHACL-style/TypeQL-style constraints enforced in our mutation gateway, portable across HugeGraph, Neo4j, and Neptune |
| Microsoft GraphRAG: costly indexing and offline community summarization | LLM summarization across many nodes and communities at ingest | Incremental extraction, dual-level indexing (LightRAG/HippoRAG patterns), semantic caching, and on-demand summarization — only where benchmarks show gains over hybrid RAG |
| Palantir / Glean / Rovo **(+)**: SaaS or heavyweight deployment, vendor lock-in, limited on-prem/air-gap | Cloud-centric architecture and proprietary ontologies | Air-gapped, white-label, multi-backend deployment with open, exportable ontology and evidence formats |
| Graphiti / agent-memory systems **(+)**: LLM-dependent extraction cost and latency | Per-episode LLM extraction | Deterministic and rule-based extraction first, local models second, LLM only under policy, with ACL re-check and memory expiry |
| Ontop / OBDA **(+)**: virtual graphs are read-mostly and mapping-heavy | Query rewriting over relational sources | Hybrid: virtualize where freshness matters, materialize where traversal performance matters, with mapping versioning |
| Gephi / desktop visualizers **(+)**: poor at very large, live, permissioned graphs | Client-side, static, single-user | Server-side subgraph aggregation, progressive disclosure, GPU rendering, permission-filtered views, and time-machine playback |

Additional directions to evaluate: graph drift via bitemporal event sourcing and semantic migration; brittle AI facts via evidence-backed claims with contradiction handling; fixed vendor query languages via typed query plans plus adapters; static agent memory via expiry/invalidation and ACL re-check. Never claim an order-of-magnitude improvement without a reproducible benchmark.

---

## 11. Architecture hypotheses to evaluate (candidates, not approved features)

1. **Multi-backend graph abstraction (+)** — a capability-negotiating storage/query layer over HugeGraph, Neo4j, Neptune, and others, with a portable typed query IR compiled to Gremlin, Cypher/GQL, and SPARQL; conformance tests per backend.
2. **Semantic fabric** — optional RDF/OWL/SHACL sidecar for interoperable semantics and validation, with explicit loss-aware RDF↔LPG translation and synchronization.
3. **Enterprise digital thread and graph-of-graphs** — versioned links among source, system, domain, schema, evidence, temporal, security, and agent views; reliable cross-system impact queries.
4. **Evidence-first assertion graph** — claim-level lineage and evidence spans; observed / derived / predicted / approved statuses; calibrated confidence; conflicts; human decisions; bitemporal validity.
5. **Wisdom graph and context-graph layer (+)** — define, above knowledge, the layer for decisions, rationale, outcomes, lessons learned, and context-dependent applicability; specify its data model, governance, and evaluation.
6. **Ontology-as-code lifecycle** — versioned schemas, visual authoring, diff/merge, lint and SHACL tests, dependency checks, migration rehearsal, release, rollback.
7. **Automatic schema and entity-relationship inference from arbitrary JSON (+)** — candidate ontology proposals, confidence, human review, and promotion into the governed ontology.
8. **Identity plane** — deterministic keys plus probabilistic entity resolution; merge/split approvals; collision handling; survivorship; reversibility.
9. **Incremental living graph** — source event log, idempotent mutation contracts, replay, watermarks, dedupe, ACL propagation, deletes, stale-knowledge detection, relationship preservation.
10. **Adaptive retrieval and NL query** — route among text, vector, graph, and hybrid retrieval by query type, evidence sufficiency, and budget; suggest ranked candidate queries for user selection; deterministic no-LLM answers where possible; abstain with explicit evidence gaps.
11. **Neuro-symbolic inference** — deterministic rules and constraints plus optional ML suggestions (GNNs over the multi-level hierarchy for impact analysis, entity resolution, drift detection, ontology evolution); predictions quarantined until validated or approved.
12. **Temporal graph learning** — temporal link prediction, anomalies, and trends only with explainability, leakage controls, drift tests, and CPU-first viability.
13. **Policy-aware agent workbench** — read-only-by-default MCP tools, typed bounded QueryPlan → parameterized backend query, least privilege, explainable traces, approvals for writes.
14. **Multi-tenant, white-label platform (+)** — isolation model, per-tenant ontology/config/branding, metering, per-tenant lifecycle operations.
15. **Multi-scale UI** — ontology editor, evidence explorer, code-impact view, time machine, graph diff, visual query builder, provenance explorer, governance/audit, operational health; large-graph performance.
16. **Interoperable export and backup** — reproducible snapshots, semantic metadata export, GraphAr/GraphML/RDF interchange where justified, restore drills, evidence-preserving migrations.
17. **Reliability and supply chain** — outbox/event processing, DLQ, reconciliation, backup and PITR feasibility, reproducible images, offline operation, SBOM, observability.
18. **Customer use cases** — change impact, incident root-cause evidence, code-to-architecture traceability, onboarding and discovery, stale-policy detection, data lineage, API dependency risk, governed assistant answers, and equivalent non-IT use cases (HR, finance, legal, operations).

Every hypothesis must pass: customer use case → technical feasibility → expected gain → cost and complexity → evidence → acceptance test → decision, before entering the committed roadmap. Record any novel, potentially patentable mechanism in the IP register (Section 16, item 22).

---

## 12. Benchmark and acceptance protocol

Define reproducible, local-first test beds before ranking anything.

- **Data tiers (illustrative, not promises):** 100k / 1M / 10M+ nodes; varied edge density and degree distributions; hot supernodes; multigraphs; temporal data; incremental update/delete streams; permission changes; corrupted and malicious inputs; multiple tenants.
- **Query mix:** single-hop, deep multi-hop, recursive paths, graph joins, subgraph matching, code impact, ontology validation and reasoning, temporal as-of, full-text / vector / hybrid, narrative evidence questions, NL-to-query.
- **Backends:** run the same workload on HugeGraph, Neo4j, and Neptune where licensing and access allow, plus our proposed augmentation, plus competitor products on matching work.
- **Measures — systems:** ingest events/s, entity-match precision/recall, graph completeness and consistency, p50/p95/p99 latency, throughput, indexing lag, CPU/RAM/disk/GPU, storage amplification, failure recovery, restore reliability, operator effort.
- **Measures — retrieval and answers:** recall/precision/nDCG/MRR, faithfulness, answer correctness, citation and span accuracy, abstention behavior, permission-leakage rate (target zero), cross-tenant leakage (target zero), contradiction handling, token use, local inference throughput, cost per correct answer, text-to-query execution accuracy.
- **Measures — ML:** non-graph and rule-only baselines, leakage-safe temporal splits, AUROC/AUPRC/F1, calibration, drift, training/inference budgets, explanation quality, reproducibility.
- **Measures — UX:** task completion time, investigation steps, onboarding friction, rendering frame rate on large graphs, usability, collaboration, accessibility.
- **Stress and chaos:** degree skew, bursty CDC, clock skew, duplicate and out-of-order events, partial failure, replay, corrupt checkpoints, source-schema changes, permission revocation, offline restarts, noisy tenants.

State hardware, workload generator, dataset license, query mix, warm-up, cache state, repetitions, variance, configuration, and versions. No universal "fastest" claims. Define regression thresholds and rollback conditions. Mark any test not actually run as **PROPOSED**, never PASSED.

---

## 13. Prioritization, requirements, and architecture decisions

**Priority score** (inputs normalized 0–5):

`PriorityScore = 0.25·CustomerValue + 0.20·StrategicFit + 0.15·RiskReduction + 0.15·EvidenceStrength + 0.10·ReuseLeverage + 0.10·Feasibility + 0.05·Differentiation − ComplexityPenalty`

Publish raw inputs, rationale, penalty, uncertainty, and a sensitivity analysis. The formula supports judgment; it does not replace it.

- **P0** — correctness, source lineage, idempotency, permission and tenant protection, a repeatable vertical slice, reliability, core query contracts.
- **P1** — high-value enterprise integration, graph evolution, ontology governance, explainable retrieval and NL query, important UX, multi-backend parity for core features.
- **P2** — advanced reasoning, ML, federation, predictive analytics, collaborative editing, scale-out validated by demand.
- **P3 / Research** — experimental architectures with unproven payoff.

**Each requirement:** REQ-ID; value and use case; source GAP-ID / STR-ID / INVERSION-ID; functional behavior; NFRs; owning module; data contracts; API and UI; backend applicability; dependencies; threat considerations; observability; tests; acceptance criteria; effort; priority; release phase; explicit out-of-scope.

**Each ADR:** context, options considered, options rejected and why, decision, consequences, reversibility.

Distinguish product priority from research priority.

---

## 14. Mandatory acceptance journeys

Validate the target design against these end-to-end scenarios:

- **J1 — Evidence-rich change impact.** Jira Story → PR → commit → exact function → downstream service/API → build → deployment → docs → related incidents. Return version-specific affected assets with source spans, permissions, confidence, and explanation. Reindexing a changed commit must not break unchanged relationships.
- **J2 — Evolving organizational truth.** Confluence and ServiceNow disagree about the owning team. Preserve both claims, validity time, evidence, the resolution decision, and as-of queries. Never overwrite history silently.
- **J3 — Temporal incident reasoning.** Correlate Grafana/Datadog/Kibana signals with deployments and dependencies in bounded windows, with pointers to source telemetry; label causation separately from correlation.
- **J4 — Governed ontology change.** Model a new relation; dry-run migration and SHACL validation; show semantic diff and impacted queries; approve; release; roll back safely.
- **J5 — Permission-aware GraphRAG.** Two employees with different permissions ask the same question; enforce source ACLs in retrieval and answers; invalidate inaccessible memory and index entries after revocation.
- **J6 — Deterministic first, AI second.** Typed parameterized graph/text queries before optional local-LLM synthesis; benchmark against plain RAG and graph-only; abstain with actionable evidence gaps when ungrounded.
- **J7 — Resilient incremental ingest.** Duplicate and out-of-order events, deletions, connector outage, partial failure, replay — no duplicate identities, no orphaned critical links, recoverable checkpoints.
- **J8 — Predictions without fact contamination.** Link prediction or anomaly proposals stored in an isolated prediction plane with provenance and calibration; only human-approved assertions are promoted to facts.
- **J9 — Service-account blast radius (+).** "What is impacted if service account 'abc' is changed or deleted?" across identity directory, code, CI/CD, infrastructure config, and runbooks, with evidence and confidence.
- **J10 — Rule-change test scope (+).** A business rule is added, updated, or deleted; return the systems, code paths, tests, and owners affected, and what must be retested.
- **J11 — NL query with suggestions (+).** A non-technical user asks a question; the system proposes ranked candidate queries with plain-language explanations; the user picks one; the executed query, evidence, and answer are shown.
- **J12 — Arbitrary JSON onboarding (+).** An unknown JSON export arrives; entities and relationships are auto-detected, an ontology extension is proposed, reviewed, approved, and the data is ingested with provenance.
- **J13 — Multi-tenant, white-label isolation (+).** Two tenants with different ontologies, branding, and models run concurrently; prove zero cross-tenant leakage in data, indexes, caches, embeddings, logs, and agent memory.
- **J14 — Backend portability (+).** The same ontology, data, and core query set run on HugeGraph, Neo4j, and Neptune with documented parity gaps.
- **J15 — Non-IT organization (+).** An HR/finance/legal scenario (e.g., "Which policies, contracts, and teams are affected by this regulation change?") answered with the same evidence and governance guarantees.
- **J16 — Air-gapped operation (+).** Full install, ingest, query, and AI features with no internet access and local models only.

---

## 15. Prohibited shortcuts

- Compressing any technology into a shallow summary to save space.
- Fabricating findings, benchmarks, citations, versions, implementation status, or advantages.
- Treating marketing claims as engineering evidence.
- Treating requirements documents as proof of implementation.
- Introducing mandatory cloud services, hidden external data flows, external LLM calls with client data, backend lock-in, direct connector-to-graph mutation, or ungoverned agent writes.
- Recommending complexity without justified customer or engineering value.
- Stopping between categories, tools, or phases to ask for permission.

---

## 16. Required deliverable package (all produced in the same run)

Use these exact names:

1. `00-EXECUTIVE-SUMMARY.md` — strategic conclusions, top gaps, top inversions, investment and complexity, honest limits, environment limitations.
2. `01-SYSTEM-BASELINE.md` — verified current architecture, capabilities with status and evidence, baseline uncertainties.
3. `02-TECHNOLOGY-REGISTRY.md` — complete deduplicated census with version, status, license, redistribution notes, tier, sources, and ADD/EXCLUDE/DEFER log; plus `02-technology-registry.json` (machine-readable) **(+)**.
4. `03-RESEARCH-METHODOLOGY.md` — evidence rubric, tiering, parallel execution plan, benchmark rules.
5. `04-COMPETITOR-DEEP-DIVES/` — one versioned report per technology (Section 9).
6. `05-COMPARISON-COHORTS/` — workload-aligned comparisons with citations.
7. `06-MASTER-CAPABILITY-MATRIX.md`
8. `07-GAP-REGISTER.md`
9. `08-STRENGTH-ADOPTION-REGISTER.md` **(+)**
10. `09-CON-TO-PRO-INVERSION-REGISTER.md` (competitor and self-inversions)
11. `10-TARGET-REFERENCE-ARCHITECTURE.md` — diagrams; data, control, evidence, security, and tenancy planes; multi-backend layer; interfaces; deployment tiers.
12. `11-REQUIREMENTS-FINAL.md` — exhaustive deduplicated functional and non-functional requirements with acceptance criteria.
13. `12-DATA-ONTOLOGY-EVENT-CONTRACTS.md` — canonical types, identity, temporal, provenance, inference, versioning, tenancy schemas.
14. `13-API-QUERY-AGENT-SECURITY-CONTRACTS.md` — typed query AST/IR, backend compilers, parameterized query gateway, REST/MCP, NL-query and suggestion contracts, policy hooks, error contracts.
15. `14-IMPLEMENTATION-ROADMAP.md` — P0→P3 dependency-aware slices, work packages, migration strategy.
16. `15-VALIDATION-BENCHMARK-PLAN.md` — harness, fixtures, generators, measures, reproducibility, go/no-go gates.
17. `16-SECURITY-PRIVACY-THREAT-MODEL.md` — permissions, tenancy, injection, poisoning, exfiltration, LLM egress policy, audit, controls.
18. `17-OPERATIONS-SRE-COST-MODEL.md` — sizing, deployment, backup/restore, monitoring, runbooks, TCO, air-gapped install.
19. `18-ADRS/` — one file per decision.
20. `19-TRACEABILITY-MATRIX.md` — Source → Claim → Competitor capability → Gap/Strength/Inversion → REQ-ID → Design → Task → Test → Metric.
21. `20-POC-EXPERIMENTS/` — Docker-first minimal experiments with reproducibility instructions (run only if authorized and possible).
22. `21-IP-PRIOR-ART-REGISTER.md` **(+)** — candidate novel mechanisms, related prior art and patents found, novelty risk, items for legal review.
23. `22-OPEN-QUESTIONS-AND-ASSUMPTIONS.md` **(+)** — every assumption made instead of asking, with its impact if wrong.
24. `23-PROGRESS-TRACKER.html` **(+)** — a self-contained interactive tracker of every registry item, gap, requirement, and roadmap task with status and filters.
25. `20-RESEARCH-STATE.md` — only if a hard limit interrupts the run (Section 3.4).

Where a later artifact depends on unresolved baseline facts, label it **PROVISIONAL** and state what must be verified. Prefer implementable pseudocode and minimal tests over speculative full systems. Canonicalize IDs and cross-link; never duplicate a requirement across files.

---

## 17. Quality gates (all must pass before declaring completion)

- **Coverage gate** — every user-named technology appears in the registry or has an explicit duplicate / rename / ambiguous / excluded resolution; every Tier A/B item has a full deep dive.
- **Depth gate** — every deep dive addresses every applicable dimension and template heading, or justifies N/A.
- **Verification gate** — every non-trivial competitive assertion has a classification, version and date context, and confidence; unknowns stay unknown.
- **Baseline gate** — design intent is never conflated with implemented code; status claims carry evidence.
- **Standards gate** — no implied compatibility from syntax similarity; RDF/OWL semantics are distinguished from LPG semantics; drafts are distinguished from published standards.
- **Architecture gate** — no mandatory cloud, hidden egress, backend replacement or lock-in, direct connector mutation, or ungoverned agent writes.
- **Security and tenancy gate** — permissions, tenant isolation, and safe query execution survive every transformation, retrieval, cache, memory, and agent action; local deployment alone is not treated as security.
- **Licensing gate** — every REUSE/INTEGRATE decision records license, redistribution/OEM terms, and legal-review triggers.
- **Performance gate** — no fabricated numbers, unsupported "orders of magnitude" claims, assumed hardware, or unrun-test successes.
- **Engineering gate** — every enhancement has a use case, design, evidence, alternatives, measurable acceptance criteria, dependencies, and a build/reuse decision.
- **Product gate** — feature bloat is refused; benefit is weighed against operational complexity; existing engines are reused when safe.
- **Traceability gate** — every roadmap item traces back to a verified gap, strength, or inversion, and forward to a test and metric.
- **Single-pass gate** — the run did not pause for approval between units; any interruption is due only to a documented hard limit.

---

## 18. Final completion report

End the run with a short report in `00-EXECUTIVE-SUMMARY.md` (and in the final message) stating: what was completed, coverage counts per category and tier, gates passed and failed, the top ten gaps, the top ten inversions, the P0 roadmap slice, unresolved unknowns, and environment limitations. No unsupported declaration of completeness.

---

## 19. Final product objective

Build an evidence-grounded, self-hosted, white-label, multi-tenant, multi-backend, modular, continuously evolving enterprise knowledge intelligence platform — a living organization brain — that solves validated customer problems better than available alternatives on its chosen workloads. Extract the valuable architectural patterns, integrate suitable mature components, design distinct capabilities where needed, turn competitors' verified weaknesses into our measurable strengths, and prove the result through reproducible journeys, security checks, and performance measurements.

**Begin now. Verify the baseline, build the registry, dispatch every deep dive, and carry the program through to the complete deliverable package in a single uninterrupted run.**

---

## Appendix A — Launcher prompt (paste into the executing agent alongside this file)

> You are my Principal Enterprise Knowledge Graph Architect, Ontology Scientist, Graph Database Engineer, Graph ML Researcher, Distributed Systems Architect, Enterprise AI Architect, and Independent Technical Auditor.
>
> Your governing specification is the attached `KNOWLEDGE_GRAPH_COMPETITIVE_RESEARCH_MASTER_PROMPT_v3.md`. Execute it — do not summarize it.
>
> 1. Read the entire specification without omitting any section, category, technology, dimension, constraint, journey, gate, or deliverable.
> 2. Examine all available project requirements, architecture documents, source code, tests, data contracts, configuration, and deployment artifacts. Classify every capability as Implemented / Partial / Planned / Absent / Unknown with evidence.
> 3. Respect the multi-backend graph requirement (Apache HugeGraph, Neo4j, Amazon Neptune, and others), the local-first / air-gapped / white-label / multi-tenant constraints, and the external-LLM data-egress policy. Do not introduce mandatory cloud services or replace or lock in any backend.
> 4. Run the whole program in one uninterrupted pass: use parallel workers for deep dives and comparisons if available, write every artifact to files as it completes, and do not stop to ask for confirmation between categories, tools, or steps. Record assumptions instead of asking questions.
> 5. Never fabricate findings, citations, benchmarks, implementation status, or advantages. Separate documented facts, experimental results, inference, and unknowns.
> 6. Produce the complete deliverable package and pass every quality gate. Stop only at the final completion report or a documented hard environmental limit, in which case write a precise resumption state.
>
> Produce actual research artifacts — not a plan, not a generic summary, not an unsupported declaration of completion.
