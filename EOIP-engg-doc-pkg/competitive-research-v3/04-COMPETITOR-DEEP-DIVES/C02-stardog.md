# C02 — Stardog (Enterprise Knowledge Graph platform, incl. Voicebox)

| Field | Value |
|---|---|
| Registry ID | T-C02-stardog |
| Tier | A — leading commercial knowledge-graph platform; direct competitor on reasoning, virtualisation and LLM question answering (Voicebox is also listed under C07) |
| Versions examined | Stardog Platform 12.2.0 (2026-10-14), 12.1.5 (2026-10-14), 12.1.0 (2026-06-10), 12.0.0 (2026-02-12), 11.2.5 (2026-08-01, maintenance line), 11.0.0 (2025-01-22); Voicebox Service container `v1.1.1` (docs, date not stated); Stardog Free EULA "revised December 13, 2022" |
| Verified on | 2026-10-18 |
| Worker | W08 |

---

## 1. Identity, current status, tier, and sources

**Identity.** Stardog is a proprietary, closed-source knowledge-graph platform from Stardog Union, Inc. (trading as Stardog), a private US company. The product family is:

- the **Stardog Platform** — the server: RDF quad store, SPARQL engine, query-time reasoner, virtual-graph/federation engine, SHACL validation and GraphQL;
- the **Stardog applications** — Studio (IDE), Designer (visual modelling and mapping), Explorer (end-user browsing), **Voicebox** (LLM question answering) and Launchpad (a single sign-on portal that also hosts the on-prem Voicebox integration). [CLAIM-stardog-01] [CLAIM-stardog-18] [CLAIM-stardog-19]

**Current status — active, with two maintained lines.** The platform release notes list 12.2.0 and 12.1.5 on 2026-10-14, 12.1.4 on 2026-09-03, and so on back to 12.0.0 on 2026-02-12. The 11.2.x line is still patched (11.2.5 on 2026-08-01). A minor release comes out about every four months, with patch releases roughly monthly. [CLAIM-stardog-01] [CLAIM-stardog-02]

**Ownership and corporate status.** No acquisition was found. The official news page records these changes:

- 2025-09-30: new CEO Craig Harper (formerly of ServiceNow). He replaced the co-founder CEO, Kendall Clark.
- 2026-05-11: new Chief Product Officer.
- 2026-06-11: new brand identity, positioned on "Trusted Enterprise AI".
- 2026-08-11: new CRO.

This reads as a go-to-market reset around Voicebox, not a change of ownership. Funding is private. Third-party trackers disagree on the total (roughly USD 23–33 M over several rounds). The last priced round was a 2020 Series B extension, and Accenture made a strategic investment in 2023. [CLAIM-stardog-23] [CLAIM-stardog-24]

**Master Prompt §5 traps.**

- The registry row "Stardog (incl. Voicebox)" is one vendor. Voicebox is not a separate company or an open-source project.
- Voicebox is also listed in C07 ("Stardog Voicebox"). This file is the single record; C07 should cross-reference it.
- The 2023–2024 "Karaoke" on-prem appliance (Nvidia and Supermicro hardware running a fine-tuned Llama 2 variant) is **historical**. The current documentation does not mention it, and whether it is still sold is UNVERIFIED. [CLAIM-stardog-22]

**Tier reason.** Tier A. Stardog is the reference commercial product for three things EOIP plans to offer:

- reasoning over a knowledge graph without ETL;
- virtual graphs over relational sources;
- LLM question answering grounded in a semantic layer.

**Sources used (15).** Platform release notes; inference-engine documentation and its troubleshooting page; virtual-graph documentation; data-quality-constraint (SHACL) documentation; HA-cluster documentation; Voicebox documentation; Voicebox Service configuration; the Stardog 11 "What's new" community post; the Mastiff storage-engine blog; the pricing page; the Stardog Free licence; the news page; the Knowledge Kits blog; the Karaoke press release; the Designer documentation. All are listed in Appendix C.

## 2. Primary problem, target workloads, concrete example workflows

**Problem.** Large enterprises have data spread across relational warehouses, lakes and document stores. The main buyers are in pharma and life sciences, financial services, manufacturing, and government and defence. They want one semantic layer over all of it: a shared ontology, queried in place, with inference, and now with natural-language question answering on top.

Stardog's pitch is "connect, don't collect". Virtual graphs rewrite SPARQL into source-native SQL, and reasoning happens at query time, so nothing has to be materialised. [CLAIM-stardog-06] [CLAIM-stardog-12]

**Target workloads.**
- **Data-fabric and semantic-layer queries** over Databricks, Snowflake, BigQuery, Teradata, SingleStore, Oracle and similar sources, through virtual graphs. Teradata was added in 12.1.0; SingleStore and STRUCT support in 12.2.0. [CLAIM-stardog-05] [CLAIM-stardog-30]
- **Ontology-driven integration with inference**: subclass and subproperty hierarchies, transitive and inverse properties, and user rules written as `IF {…} THEN {…}`. [CLAIM-stardog-07] [CLAIM-stardog-09]
- **Data quality with SHACL**, as validation reports or through transactional "guard mode". [CLAIM-stardog-13]
- **"Answer engine"**: Voicebox turns a question into SPARQL, Stardog pushes that down as SQL, and Voicebox summarises the result. When it cannot answer from data, it says "cannot find an answer". [CLAIM-stardog-18]

**Example workflows.**
1. *Pharma R&D.* An analyst asks Voicebox: "which compounds in phase II target kinase X and failed toxicity screening?"
   - Voicebox matches "compound", "target" and "screening" to ontology concepts through an embedded vector store.
   - The LLM writes SPARQL, and Stardog rewrites it into SQL against two warehouses.
   - The result is summarised. The generated SPARQL stays available for audit. [CLAIM-stardog-18] [CLAIM-stardog-31]
2. *Supply chain.* A modeller builds an ontology in Designer, with Voicebox suggesting concepts from a use-case description. Designer maps tables to classes and publishes the model to a Stardog endpoint as virtual graphs. Later, a data engineer runs `virtual import` on the slow-changing, high-traffic tables to materialise them. [CLAIM-stardog-12] [CLAIM-stardog-26]
3. *Regulatory data quality.* SHACL shapes run in guard mode, so any transaction that violates them fails. Running the same shapes with reasoning on also catches violations on inferred types. [CLAIM-stardog-13]

**Suitability for on-prem, local-first operation.**
- The server is self-managed: tarball, Docker (including ARM since 12.2.0), Kubernetes, and AWS/Azure marketplace images. [CLAIM-stardog-05]
- Voicebox can be self-managed through Launchpad and the `voicebox-service` container. However, its documented LLM providers are all cloud APIs (see §10). [CLAIM-stardog-20]

## 3. Feature inventory

| Area | Feature | Status | Evidence |
|---|---|---|---|
| Storage | RDF quads on a RocksDB-based LSM engine (Mastiff) with MVCC and snapshot isolation | present (internals documented since 7.0; current detail NOT PUBLICLY VERIFIED) | [CLAIM-stardog-15] |
| Storage | Encryption at rest | **absent — removed in 11.0.0** | [CLAIM-stardog-04] |
| Storage | Point-in-time restore | present (12.0.0) | [CLAIM-stardog-03] |
| Query | SPARQL 1.1 query and update | present | [CLAIM-stardog-12] |
| Query | GraphQL endpoint | present (12.1.0 fixed `@type`; 11.2.0 added predicate IRIs and language literals) | [CLAIM-stardog-28] [CLAIM-stardog-30] |
| Query | Path queries (block-based path operator) | present (12.0.0) | [CLAIM-stardog-03] |
| Query | BARQ (block-based execution engine) | beta at 10.1.0; extended in 11.x; GA status UNVERIFIED | [CLAIM-stardog-29] [CLAIM-stardog-28] |
| Query | Query triggers (change detection) | present (11.1.0) | [CLAIM-stardog-28] |
| Reasoning | Query-time rewriting reasoner "Blackout": RDFS, QL, RL, EL, SL (default) | present | [CLAIM-stardog-06] [CLAIM-stardog-07] |
| Reasoning | OWL 2 DL | partial — only for data that fits in main memory | [CLAIM-stardog-11] |
| Reasoning | User rules (Stardog Rules syntax; SWRL inside SL) | present, with restrictions | [CLAIM-stardog-09] |
| Reasoning | Stride reasoner (negation, aggregation) | beta, "not recommended for production" | [CLAIM-stardog-08] |
| Reasoning | Explanations and consistency check | present as CLI commands (`reasoning explain`, `reasoning consistency`); depth UNVERIFIED | [CLAIM-stardog-11] |
| Reasoning | Materialised inferences | **absent by design** (query-time only); `virtual import` materialises data, not inferences | [CLAIM-stardog-06] |
| Validation | SHACL Core plus SPARQL constraints (with listed exceptions) | present | [CLAIM-stardog-13] |
| Validation | Transactional guard mode | present (`icv.enabled`) | [CLAIM-stardog-13] |
| Virtualisation | Virtual graphs over RDBMS, CSV, MongoDB, Elasticsearch, Cassandra and JSON, using SMS, R2RML or SMS2 mappings | present | [CLAIM-stardog-12] |
| Virtualisation | Materialise with `virtual import` | present | [CLAIM-stardog-12] |
| Virtualisation | Caching | enterprise-only (not in Free) | [CLAIM-stardog-16] |
| Ops | HA cluster (ZooKeeper, full replicas), standby, read and geo replicas | enterprise-only (HA not in Free) | [CLAIM-stardog-14] [CLAIM-stardog-05] [CLAIM-stardog-16] |
| Ops | Rolling minor-version upgrade | present (11.2.0) | [CLAIM-stardog-28] |
| Security | RBAC, including stored queries as securable objects (12.0.0); LDAP; Okta and Entra passthrough | present; LDAP is enterprise-only (not in Free) | [CLAIM-stardog-03] [CLAIM-stardog-30] [CLAIM-stardog-16] |
| Lineage | Provenance capture for CSV/JSON imports | present (11.0.0) | [CLAIM-stardog-04] |
| ML | Machine-learning support | **deprecated in 12.2.0** | [CLAIM-stardog-05] |
| AI | Voicebox: NL → SPARQL → SQL, summarised answers, abstention | present (Cloud; on-prem/VPC through Launchpad) | [CLAIM-stardog-18] [CLAIM-stardog-19] |
| AI | Voicebox multi-agent | private preview | [CLAIM-stardog-18] |
| AI | Voicebox over unstructured PDF/DOCX (Spark-based RAG pipeline) | present | [CLAIM-stardog-18] |
| AI | Local / self-hosted LLM for Voicebox | partial — only through an OpenAI-compatible proxy (`server_url`); no local provider documented | [CLAIM-stardog-20] |
| AI | Voicebox audit report (questions, generated SPARQL, responses, feedback) | present | [CLAIM-stardog-31] |
| UI | Studio, Designer, Explorer, Launchpad | present (proprietary apps) | [CLAIM-stardog-26] |
| Content | Knowledge Kits (pre-built domain models and demo data) | present (free) | [CLAIM-stardog-25] |
| Integrations | Power BI (BI Server), Microsoft Purview v2, Spark on Kubernetes as external compute | present | [CLAIM-stardog-05] [CLAIM-stardog-30] |
| Integrations | NiFi connector | removed (11.0.0) | [CLAIM-stardog-04] |
| API/SDK | HTTP API, CLI, Python client (pystardog) | present | [CLAIM-stardog-03] |
| Platform | Windows server | removed (10.1.0) | [CLAIM-stardog-29] |

## 4. Text-based architecture diagram

```
                          CONTROL PLANE                                    DATA / AI PLANE
 +-----------------------------------------------+      +-----------------------------------------+
 | Launchpad (SSO portal) -- Studio / Designer / |      | Voicebox Service (container v1.1.1)     |
 | Explorer (browser apps)                       |----->|  concept extraction                     |
 |   | HTTP/JSON                                 |      |  ontology match (embedded vector store) |
 |   v                                           |<-----|  LLM call  -----------------------------+--> anthropic | azure | bedrock |
 | Stardog Server (JVM, Java 21 since 12.0)      |SPARQL|  SPARQL gen -> submit -> summarise      |    vertex | openai (+ OpenAI-
 |  +- RBAC / LDAP / Okta / Entra passthrough    |      +-----------------------------------------+    compatible proxy)   [EGRESS]
 |  +- Admin: DB config, schema graphs, rules    |
 |  +- ZooKeeper ensemble (cluster only)         |
 +-----------------------------------------------+
                     |
                     v
 +-------------------------------------------------------------------------------------------+
 | Query pipeline: parse SPARQL/GraphQL -> algebra -> [reasoning rewrite: schema -> EQ       |
 | (unions of patterns / rule bodies)] -> optimiser (stats; BARQ block exec; joins)          |
 |   +- local quads  --> Mastiff (RocksDB LSM, MVCC, snapshot isolation)                      |
 |   +- virtual://g  --> VG translator -> SQL / Mongo / ES query --> external source (JDBC)   |
 |   |                     +- optional caches (Enterprise)                                    |
 |   +- SERVICE icv:validate --> SHACL engine (optionally with reasoning)                     |
 +-------------------------------------------------------------------------------------------+
                     | commit (cluster): coordinator -> all participants ack -> client ack
                     v
           Participants (full replicas) . standby . read replicas . geo replica (12.2)
```

**State held by the system:**
- quads and indexes in Mastiff;
- named schema graphs, plus their processed in-memory form;
- the transaction log, which carries timestamps since 12.0.0 (this is what enables point-in-time restore);
- virtual-graph mappings and properties;
- Voicebox configuration (`vbx-config.json`). [CLAIM-stardog-03] [CLAIM-stardog-11] [CLAIM-stardog-20]

## 5. Under-the-hood reconstruction

Stardog is closed source. Everything below is either **documented** (and carries a CLAIM) or is labelled *hypothesis*. No proprietary material was used.

### 5.1 Data model
- Data is stored as RDF 1.1 quads: a default graph plus named graphs.
- Virtual graphs appear as named graphs with a `virtual://` IRI.
- Schemas are named graphs of RDFS/OWL axioms and rules. Several named schemas can exist side by side and be chosen per query; Stardog presents this as a multi-tenancy feature.
- Reasoning sees only the schema that was explicitly loaded, because `owl:imports` is not followed. [CLAIM-stardog-10] [CLAIM-stardog-12]

### 5.2 Storage layout and indexing
**Documented.** Since version 7.0, storage is RocksDB (an LSM tree) with MVCC and snapshot isolation. Moving from a B-tree to an LSM tree brought a vendor-claimed "10x–20x" write improvement and 20–30 % more disk use. RocksDB memory is off-heap. [CLAIM-stardog-15]

**Hypothesis** (standard for RDF stores, not confirmed for Stardog). Terms are dictionary-encoded (each IRI or literal mapped to an integer ID). Quad keys are stored in several sorted permutations (for example SPOC, POSC and OSPC, plus context-first orders) as RocksDB key ranges, so any triple pattern with a bound prefix becomes a range scan.

Aggregate indexes were deprecated in 11.0 and removed in 12.0, which suggests a slim index set. [CLAIM-stardog-03] [CLAIM-stardog-04]

### 5.3 Query pipeline and planning
**Documented elements:**
- SPARQL rewriting for virtual graphs;
- an "equivalent query" (EQ) built by the reasoner;
- BARQ, a block-based execution engine: beta in 10.1, extended in 11.x to the WHERE clauses of updates, to bind joins and to index scans;
- block-based property paths;
- query hints. [CLAIM-stardog-11] [CLAIM-stardog-28] [CLAIM-stardog-29]

**Reconstructed blueprint (hypothesis):**
```
plan(q, reasoning_on, schema_name):
  A = parse_to_algebra(q)
  if reasoning_on:
     S = schema_cache.get_or_build(schema_name)   # whole TBox in memory; the first query pays the build
     A = rewrite(A, S)        # each basic graph pattern -> UNION of expansions (sub-classes,
                              # sub-properties, inverse/symmetric, rule heads -> rule bodies);
                              # transitive properties -> property paths
     A = prune(A, S.domain_range, S.functional)   # 12.x optimisations (documented options)
  for each GRAPH <virtual://g> block: A = push_down(A, mapping[g], dialect[g])   # SQL / NoSQL
  P = cost_based_join_order(A, stats)             # BARQ where supported
  return execute(P, snapshot = mvcc.snapshot())
```

**Why this matters for latency (documented):**
- the EQ grows with hierarchy depth and with the number of matching rules;
- variable predicates and variable `rdf:type` objects make it much larger;
- the first reasoning query after a database change rebuilds the schema. [CLAIM-stardog-11]

### 5.4 Reasoning
**Documented behaviour:**
- Reasoning happens at query time, by rewriting the query. Inferences are never materialised. Axioms and rules are treated as "(basically) Datalog rules over a graph".
- The supported profiles are RDFS, QL, RL, EL and SL. SL is the default and combines RDFS, QL, RL, EL and SWRL.
- Axioms outside the chosen profile are **ignored silently**; they are only logged.
- Rules cannot use variables in predicate position (except `rdf:type`). Recursion is limited to what maps onto property paths.
- Full OWL 2 DL works only for data that fits in memory.
- The Stride reasoner (beta) adds negation and aggregation and fails fast on invalid rules. [CLAIM-stardog-06] [CLAIM-stardog-07] [CLAIM-stardog-08] [CLAIM-stardog-09] [CLAIM-stardog-11]

**Blueprint for equivalent behaviour.** Backward chaining by rewriting: unfold rule heads into rule bodies until a fixpoint, bounded because the schema is acyclic, and turn linear transitive recursion into SPARQL property paths. That is Datalog query rewriting restricted to non-recursive programs plus linear recursion. In the worst case, rewriting over EL/RL axioms produces an exponential number of unions.

*Hypothesis:* Stardog limits this blow-up with a hierarchy cache and pruning.

### 5.5 Concurrency and transactions
- Transactions use snapshot isolation through MVCC on RocksDB. [CLAIM-stardog-15]
- In a cluster, writes take a cluster-wide lock managed by ZooKeeper. A commit is acknowledged only after every non-failing participant has committed. A peer that fails during commit is expelled, and if the coordinator fails mid-commit the transaction aborts. [CLAIM-stardog-14]
- *Reasoned inference:* this amounts to one writer at a time across the whole cluster. That would explain the documented "larger clusters … perform worse for writes". [CLAIM-stardog-14]

### 5.6 Partitioning and consistency
There is no sharding. Every node is a full replica, with strong consistency. Read replicas and standby nodes, and geo replicas since 12.2, add read capacity and disaster recovery only. [CLAIM-stardog-14] [CLAIM-stardog-05]

### 5.7 Caching
- The processed schema is cached in memory and rebuilt after database changes. [CLAIM-stardog-11]
- Caching is an Enterprise feature and is not in Free. [CLAIM-stardog-16]
- Cached datasets built from a virtual graph do not move when that graph is reassigned to another database. [CLAIM-stardog-12]

### 5.8 Versioning
There is no graph branching and no time-travel query. 12.0.0 added point-in-time restore through a timestamped transaction log. Since 10.0, schema versions are tracked by a content hash. [CLAIM-stardog-03] [CLAIM-stardog-10]

### 5.9 Security
**Documented:**
- RBAC, with stored queries as securable objects (12.0);
- LDAP (Enterprise only);
- Okta passthrough (12.1);
- Microsoft Entra ID passthrough for BigQuery and Power BI (12.2).

Encryption at rest was **removed in 11.0.0**, so customers must rely on disk or volume encryption. [CLAIM-stardog-03] [CLAIM-stardog-04] [CLAIM-stardog-05] [CLAIM-stardog-30]

*Reasoned inference:* no documented per-triple or per-source ACL filtering was found that compares with EOIP's planned source-ACL enforcement. Named-graph security appears in the documentation navigation but was not examined in depth (UNVERIFIED).

Voicebox can pass `$VOICEBOX_USER` to the LLM provider for auditing at the provider. [CLAIM-stardog-20]

### 5.10 Voicebox pipeline (documented flow, reconstructed as a contract)
```
answer(question, user):
  concepts = extract_concepts(question)
  matches  = vector_store.match(concepts, ontology_terms)     # embedded vector store over the model
  sparql   = LLM.generate(question, matches, few_shot_examples)
  plan     = stardog.plan(sparql)                             # SPARQL -> SQL pushdown via mappings
  rows     = execute(plan)
  if rows empty or ungrounded: return "Cannot find an answer for this question."
  return LLM.summarise(question, rows) + {sparql, source_type in {KG, RAG, code, external LLM}}
```
[CLAIM-stardog-18]

The design keeps two jobs apart: the LLM writes a query, and the database supplies the facts. The "hallucination-free" label is a vendor claim. [CLAIM-stardog-32]

## 6. Functional and non-functional requirements inferred from verified behaviour

| ID | Requirement inferred | Source behaviour |
|---|---|---|
| FR-SD-1 | Reasoning results must reflect a schema change without re-ingesting data | query-time reasoning [CLAIM-stardog-06] |
| FR-SD-2 | A selectable reasoning profile per query, with explicit reporting of ignored axioms | the SL default ignores out-of-profile axioms [CLAIM-stardog-07] |
| FR-SD-3 | Several schemas (ontologies) per database, selected per query or tenant | named schemas [CLAIM-stardog-10] |
| FR-SD-4 | Query relational and NoSQL sources in place through a standard mapping (R2RML), with an option to materialise | virtual graphs and `virtual import` [CLAIM-stardog-12] |
| FR-SD-5 | Enforce constraints inside transactions as well as report on them | SHACL guard mode [CLAIM-stardog-13] |
| FR-SD-6 | Answer NL questions only from executed queries, with abstention and an auditable query log | Voicebox [CLAIM-stardog-18] [CLAIM-stardog-31] |
| FR-SD-7 | The LLM provider is configurable per deployment | vbx-config [CLAIM-stardog-20] |
| NFR-SD-1 | Strongly consistent replicated HA with at least 2 data nodes and a 3-node coordination ensemble | [CLAIM-stardog-14] |
| NFR-SD-2 | Point-in-time restore | [CLAIM-stardog-03] |
| NFR-SD-3 | Rolling upgrades for minor versions | [CLAIM-stardog-28] |
| NFR-SD-4 | Memory budget grows with schema size (the whole TBox is held in memory) | [CLAIM-stardog-11] |

## 7. Performance and resource model

**Published evidence.** No independent, reproducible benchmark of Stardog 11 or 12 was found in this run. Stardog's own figures, such as the 7.0 write-throughput claim of "10x–20x", are vendor claims on unspecified hardware. They are recorded here, not restated as fact. [CLAIM-stardog-15]

**Documented scaling behaviour (qualitative).**
- **Reasoning latency** depends on EQ size, which grows with class and property hierarchy depth, the number of rules, and variable predicates. The first query after a change pays the schema-processing cost. [CLAIM-stardog-11]
- **Reasoning memory** depends on schema size. OWL 2 DL is limited by the RAM available for the data. [CLAIM-stardog-11]
- **Cluster writes** slow down as nodes are added, while reads scale with replicas. [CLAIM-stardog-14]
- **Virtual-graph latency** is dominated by the remote source. Stardog recommends selective `GRAPH` clauses, and materialising sources that are slow to query. [CLAIM-stardog-12]
- **Voicebox** is disabled on databases with "extremely large schemas" (11.1.0). This implies a size or latency ceiling in the step that brings the ontology into the prompt. [CLAIM-stardog-27]

**Failure modes.**
- Out-of-profile axioms are ignored, which gives wrong answers with no error. [CLAIM-stardog-07]
- Blackout skips invalid rules and only logs them. [CLAIM-stardog-08]
- When a variable's type is ambiguous, the reasoner guesses, and its assumption can differ from the author's intent. [CLAIM-stardog-11]
- A cluster node that loses its ZooKeeper connection must re-sync before it is consistent. [CLAIM-stardog-14]
- Virtual graphs can return duplicate solutions, and `MINUS` is not translated to SQL. [CLAIM-stardog-12]

**Uncertainty.** Latency percentiles (p50/p95/p99), ingest rates and per-edge storage cost are NOT PUBLICLY VERIFIED for current versions. Any comparison with EOIP must come from the benchmarks in §14.

## 8. Strengths and use-case-specific advantages

| # | Strength | Why it matters | How EOIP could match or exceed |
|---|---|---|---|
| S1 | Query-time reasoning: a schema change is visible at once, with no re-materialisation | Fast ontology iteration, and no inference bloat in storage [CLAIM-stardog-06] | Hybrid: materialise tractable rules incrementally (DRed or counting) **and** rewrite at query time for the parts that change often; keep both explainable |
| S2 | Mature virtual graphs with R2RML, plus a simple switch to materialise | Freshness without ETL; one mapping serves both modes [CLAIM-stardog-12] | EOIP has CML→IR (BL-33); its working tree also has R2RML import and a VIRTUAL/MATERIALIZED split (`mapping/virtualization.py`). Finish these, and label every answer's freshness honestly |
| S3 | SHACL guard mode inside the transaction | Violations cannot land in the graph [CLAIM-stardog-13] | EOIP already has a validation gate on the mutation path (BL-28). Upgrade it to W3C SHACL Core semantics |
| S4 | Voicebox: "the LLM writes queries, the database supplies facts", with abstention and an audit report | Trust story for regulated buyers [CLAIM-stardog-18] [CLAIM-stardog-31] | EOIP's suggestion engine (BL-11) plus QueryPlan (BL-08) is structurally stronger: typed, bounded plans that the user picks before execution. Add an abstention contract and an exchange report |
| S5 | Ontology concepts matched through a vector store before the query is generated | Grounding in the schema improves NL→query [CLAIM-stardog-18] | Retrieve schema terms from the tenant ontology using local embeddings |
| S6 | Knowledge Kits: domain starter models and data | Time to value in demos and proofs of concept [CLAIM-stardog-25] | Per-industry ontology packs shipped as GitOps bundles (`ontology/gitops.py`) |
| S7 | Strongly consistent HA, point-in-time restore, rolling upgrades, geo replica | Enterprise operability [CLAIM-stardog-03] [CLAIM-stardog-14] | Inherit these from the chosen backend. EOIP should not build a replicated store |

## 9. Limitations with root causes

**Verified, documented limitations.**
- **L1 — Silent skipping.** Axioms outside the selected profile are ignored (SL is the default), and invalid rules are skipped with only a log entry. Root cause: *user and developer friction* (inference you cannot see). [CLAIM-stardog-07] [CLAIM-stardog-08]
- **L2 — Rule-language restrictions.** No variable predicates, and limited recursion. Stride lifts some of this but is beta. Root cause: an *algorithmic dead-end*: pure query rewriting cannot express general recursion efficiently without materialisation. [CLAIM-stardog-08] [CLAIM-stardog-09]
- **L3 — Reasoning cost.** Cost grows with hierarchy depth, variable types and schema expressivity, and OWL 2 DL is limited to data in memory. Root cause: *algorithmic* (the EQ grows) plus *operational and hardware overhead* (the whole TBox sits in RAM). [CLAIM-stardog-11]
- **L4 — Write scaling.** Cluster write throughput falls as nodes are added, and there is no sharding. Root cause: *operational and hardware overhead* (every node is a full replica, and every commit needs every node's acknowledgement under a cluster lock). [CLAIM-stardog-14]
- **L5 — No encryption at rest.** Removed in 11.0.0. Root cause: an intentional product trade-off. [CLAIM-stardog-04]
- **L6 — Virtual-graph translation gaps.** Duplicate solutions, `MINUS` not translated, R2RML named graphs not supported. Root cause: a *semantics* mismatch between SPARQL and SQL. [CLAIM-stardog-12]

**Intentional trade-offs.** Inferences are never materialised. ML support was deprecated in 12.2.0 as the product moved to LLM features. [CLAIM-stardog-05] [CLAIM-stardog-06]

**Licensing restrictions.**
- The licence is proprietary. Enterprise pricing is not published.
- The Free edition's EULA says it is **evaluation-only**, while the pricing page calls it "available for commercial use". This contradiction is a legal-review item.
- Free lacks HA, caching, backups, LDAP and the full set of connectors. [CLAIM-stardog-16] [CLAIM-stardog-17]

**Voicebox constraints.**
- The documented LLM providers are all cloud APIs: Anthropic, Azure AI Foundry, Bedrock, Vertex and OpenAI.
- A local model is possible only behind an OpenAI-compatible proxy, which is not documented as a supported setup.
- Voicebox is disabled on very large schemas, and multi-agent support is in private preview. [CLAIM-stardog-18] [CLAIM-stardog-20] [CLAIM-stardog-27]

**Outdated claims to avoid.** The "Karaoke" appliance and the "fine-tuned Llama 2" are 2023–2024 messaging and are absent from the current documentation. [CLAIM-stardog-22] "Hallucination-free" is vendor marketing. [CLAIM-stardog-32]

**User-reported complaints.** No systematic sample was collected in this run (NOT PUBLICLY VERIFIED).

**Seed hypothesis §10.5 (Stardog) — verdict: PARTIALLY VALIDATED.**
- *"Query-time reasoning can cause latency variance."* **Validated as a documented mechanism**: the EQ grows with schema depth, the schema is rebuilt on the first query after a change, variable predicates blow up the query, and expressive schemas are costly. [CLAIM-stardog-11] The *size* of the variance has **not been measured** by any independent source; it stays a hypothesis to test (BM-SD-01).
- *"Root cause: backward-chaining query rewriting over complex axioms."* **Validated.** Stardog documents query rewriting and no materialisation. [CLAIM-stardog-06]
- *"High licence cost."* **Unverified.** No price is published. What is verified is narrower: there is no free tier licensed for production (per the EULA), and Enterprise pricing is only given on request. [CLAIM-stardog-16] [CLAIM-stardog-17]

## 10. Deployment, licensing, redistribution, and operational viability under EOIP constraints

| Constraint | Assessment |
|---|---|
| Self-hosted / air-gap (server) | **Viable.** Tarball, Docker (x86 and ARM) and Kubernetes, with a licence key. Whether licence activation works offline is UNVERIFIED. [CLAIM-stardog-05] |
| Air-gap (Voicebox) | **Partial at best.** The service container is pulled from a vendor JFrog registry, and the documented LLM providers are cloud APIs. A local model would need an OpenAI-compatible proxy (for example vLLM), which is not a documented path. [CLAIM-stardog-20] |
| LLM egress policy | Voicebox sends the question, the matched ontology terms, few-shot examples and **query results (for summarising)** to the configured LLM. The exact payload is NOT PUBLICLY VERIFIED. This conflicts with EOIP's S0 default unless a local endpoint is used. [CLAIM-stardog-18] [CLAIM-stardog-19] |
| Backend neutrality | Stardog would be one more SPARQL backend. Adopting its reasoning or Voicebox would lock reasoning semantics to one vendor. |
| Licence class | Proprietary. Free is an evaluation-only EULA with no sublicensing, no derivative works and no evaluation for competitive purposes. Enterprise terms were not examined in this run (sales contract). [CLAIM-stardog-17] |
| Redistribution / OEM | **Not permitted** under the published terms. White-label embedding would need a negotiated OEM agreement. **Legal-review trigger.** |
| Benchmark publication | No DeWitt clause was seen in the Free EULA, but evaluating the software "to compete with Stardog" is prohibited. That bears on publishing EOIP-vs-Stardog benchmarks: **legal-review trigger**. [CLAIM-stardog-17] |
| One-node first | The server runs on a single node. Free has no backups, so a production single node needs Enterprise. [CLAIM-stardog-16] |
| Tenant isolation | One database per tenant, or one named schema per tenant. EOIP must enforce tenancy above Stardog. [CLAIM-stardog-10] |

**Conclusion.** Stardog is viable as a *customer-supplied* SPARQL backend that EOIP talks to over HTTP. It is not a component EOIP can bundle or white-label. Voicebox should be treated as a competitor, not an integration.

## 11. Competitive delta against the EOIP verified baseline

| Area | Stardog | EOIP baseline | Delta |
|---|---|---|---|
| Stardog adapter | — | Only a **manifest entry** (`adapters/manifests.py:336`, `adapter_status="manifest-only"`). `graph/database_adapters.py` maps Cypher to SPARQL by regex for `STARDOG`. | Not a working backend in EOIP. The nearest are the Fuseki and GraphDB adapters (BL-06), which are themselves cache-only (see C02-apache-jena §11). |
| Reasoning | Query-time OWL 2 profiles plus rules [CLAIM-stardog-07] | In-house `OWLReasoner` covering subclass, disjointness and property chains only (BL-30, Partial) | **Large competitive deficit** |
| SHACL | SHACL Core plus SPARQL constraints, guard mode [CLAIM-stardog-13] | In-house subset over the in-memory store (BL-29, Partial); a validation gate on the mutation path (BL-28) | Deficit in conformance. EOIP's structure is comparable: its gate sits on the mutation path too |
| Virtualisation | Production virtual graphs over many sources [CLAIM-stardog-12] | Federation planner (BL-51, Partial); CML→IR (BL-33). An R2RML adapter and a virtual/materialised split exist in the working tree but not in the baseline | Deficit, partly addressed by work in progress |
| NL query | Voicebox: LLM→SPARQL with abstention [CLAIM-stardog-18] | Deterministic suggestion tier (BL-11, Implemented); LLM hook (BL-12, Partial) | **EOIP is ahead on determinism** (the user picks a typed plan before execution) and **behind on LLM breadth** |
| Egress | Cloud LLM providers [CLAIM-stardog-20] | Egress gateway with S0 default (BL-45) | **EOIP advantage** |
| Source-ACL enforcement in answers | Not documented (UNVERIFIED) | Absent (BL-18, P0) | Both weak. EOIP must close BL-18 whatever competitors do |
| Tenancy | Named schemas and databases [CLAIM-stardog-10] | Contract only; adapters are not tenant-aware (BL-20) | Parity gap for EOIP |
| Temporal | Point-in-time restore only [CLAIM-stardog-03] | Bitemporal revisions, diff and playback (BL-37, BL-38) | **EOIP advantage** |
| Claims and epistemic separation | Not documented in the sources examined | Truth engine and epistemic boundary (BL-39, BL-40) | **EOIP advantage** |
| HA | Strong-consistency cluster [CLAIM-stardog-14] | Inherited from the backend | Not EOIP's layer |
| White-label / OEM | Not available [CLAIM-stardog-17] | Branding and offline licensing (BL-21, BL-22) | **EOIP advantage** |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

### Strength-adoption cards

| STR-ID | Competitor | Strength | Evidence | Value to EOIP customers | Match / exceed / integrate / reject | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-stardog-01 | Stardog | A schema change takes effect without reloading data (query-time reasoning) | CLAIM-stardog-06, -11 | Ontology iteration in J4 without re-ingest | **exceed** | Hybrid tiered reasoning (INV-stardog-01): incremental materialisation of RL/Datalog rules into an *inferred plane*, plus query-time expansion for hierarchy-only axioms | Change a subclass axiom on 1 M triples: inferred answers are correct within 5 s with no full re-ingest, and the explanation names the axiom |
| STR-stardog-02 | Stardog | One mapping serves both virtual and materialised modes | CLAIM-stardog-12 | Choose freshness or speed per source (J7, J15) | **match** | `MappingIR` carries an execution mode; the planner labels freshness on every answer row | The same R2RML mapping returns identical results in both modes on a 10-table Postgres fixture, and every answer shows its freshness label |
| STR-stardog-03 | Stardog | SHACL enforced inside the transaction | CLAIM-stardog-13 | Violations never reach the authoritative graph (J4, J12) | **match** | Run W3C-conformant SHACL Core inside `validation/gate.py` in a guard mode, either by reusing pySHACL or with a backend-native engine | ≥95 % of the W3C SHACL Core test suite passes; a violating mutation is rejected with a SHACL report |
| STR-stardog-04 | Stardog | NL→query grounded in the ontology, with abstention and an audit log | CLAIM-stardog-18, -31 | Trustworthy NL query (J6, J11) | **exceed** | Keep EOIP's suggest-then-pick plans; add schema-term vector retrieval with local embeddings, an "insufficient evidence" contract, and an exchange report (question, plan, evidence, model, egress level) | On a 200-question gold set: top-3 suggestion accuracy ≥ a threshold set from the baseline run; 100 % of answers carry a plan and evidence; abstention on 100 % of the unanswerable controls |
| STR-stardog-05 | Stardog | Domain starter kits | CLAIM-stardog-25 | Time to value for non-IT tenants (J15) | **match** | Signed ontology packs (SKOS/OWL, SHACL and sample data) installed through GitOps | A new tenant installs the HR pack offline and answers 5 canned questions within 15 minutes |

### Inversion cards

**INV-stardog-01 — Query-time-only reasoning causes latency variance and a recursion ceiling**
- **Target / version / workload:** Stardog 12.2.0, Blackout reasoner, SL profile; deep class and property hierarchies, rule-heavy schemas, queries with variable predicates.
- **Evidence-supported limitation:**
  - the EQ grows with hierarchy depth;
  - variable predicates and types cause problems;
  - the first query after a change rebuilds the schema;
  - recursion is limited to property-path shapes;
  - OWL 2 DL works only in memory. [CLAIM-stardog-06] [CLAIM-stardog-09] [CLAIM-stardog-11]
- **Root cause:** **algorithm** — backward rewriting enumerates expansions on every query. The mechanism is *proven* (documented); the size of the latency variance is a *hypothesis*.
- **Why the alternative helps, and when it is worse:** forward materialisation moves the cost to write time and keeps read latency flat. It is worse when:
  - the schema changes very often;
  - the inferences are huge (for example `owl:sameAs` cliques, or transitive closure over supernodes);
  - storage is tight.
- **Options:**
  1. **Quick integration:** delegate reasoning to a customer-supplied engine (GraphDB rulesets, or Jena rules behind Fuseki) through a repaired RDF adapter.
  2. **Pragmatic native enhancement:** an EOIP-side semi-naïve Datalog evaluator for an OWL 2 RL subset and custom rules.
     - Inferred facts go into a separate epistemic plane (BL-40), with the rule version as provenance.
     - The plane is maintained incrementally with delete-and-rederive (DRed).
     - Hierarchy-only axioms are expanded at query time inside the `QueryPlan` templates.
  3. **Long-term differentiated architecture:** a tiered reasoner whose cost model chooses, per rule, between materialising and rewriting, based on the observed query mix and write rate; proof traces are stored.
- **Selected:** option 2 now, designed so that option 3 can follow.
  - Trade-off: storage growth and write amplification in exchange for flat reads.
  - Pattern: the governed mutation gateway also maintains derived facts.
  - The new code is limited to a bounded rule subset.
```
on_mutation(delta):                                   # inside the governed mutation gateway
  base_plane.apply(delta)
  inferred_delta = dred(delta, rules_RL_subset, inferred_plane)        # delete-rederive
  inferred_plane.apply(inferred_delta, provenance={rule_id, rule_version, premises},
                       acl = most_restrictive(premises.acl))
query(plan):
  if plan.reasoning == "hierarchy": expand(plan, class_closure_cache)  # cheap rewrite
  read(base_plane UNION inferred_plane)    # epistemic flag carried on every result row
```
- **Falsifiable benchmark (BM-SD-01):**
  - *Dataset:* LUBM(50) plus a synthetic EOIP IT ontology (depth 8, 300 classes).
  - *Measurement:* p50/p95/p99 for the 14 LUBM queries on (a) Stardog with reasoning, only if the legal review clears it, otherwise GraphDB or Jena as a proxy, and (b) the EOIP hybrid.
  - *Success:* EOIP's p99/p50 ratio ≤ 3, and its p95 within 2× of the best engine, on one node (16 vCPU, 64 GB).
  - *Cost baseline:* storage ≤ 1.6× the base triples; incremental update of a 1 % delta in ≤ 10 % of the full materialisation time.
- **Dependencies, migration and compatibility:** HugeGraph, Neo4j and Neptune would hold inferred facts as labelled edges or properties marked `epistemic=inferred`. Backward compatible, because the inferred plane is additive.
- **Security and privacy failure cases:**
  - An inferred fact derived from an ACL-restricted premise must inherit the most restrictive ACL of its premises, or it leaks (ties to BL-18).
  - Retraction must cascade when a source fact is deleted (J7).
- **Defensibility:** single-engine vendors do not ship this combination: epistemic separation, inferences that inherit ACLs, and per-rule provenance across several LPG backends. Copying it would require a governed mutation gateway.
- **Decision:** **ADOPT** option 2; **EXPERIMENT** with option 3.

**INV-stardog-02 — Voicebox depends on cloud LLM providers and sends results for summarising**
- **Target / version / workload:** Voicebox Service v1.1.1, on-prem through Launchpad, NL question answering.
- **Evidence-supported limitation:** the providers are anthropic, azure, bedrock, vertex and openai. A local model works only through an undocumented OpenAI-compatible proxy. The summarising step needs query results in the prompt. [CLAIM-stardog-18] [CLAIM-stardog-20]
- **Root cause:** **deployment and coupling**. *Proven* for the provider list; the exact payload is a *hypothesis*.
- **Why the alternative helps, and when it is worse:** deterministic plan suggestion plus templated answers needs no LLM, and a local model keeps data on site. This is worse when free-form summaries of large result sets are the main value, because local models are weaker.
- **Options:**
  1. **Quick:** route EOIP's LLM hook only through the egress gateway, with Ollama as the default.
  2. **Pragmatic:** an "answer without an LLM" path that renders plan results and evidence through templates. An LLM summary is allowed only at sharing level S1 or above, with DLP redaction.
  3. **Long-term:** a per-tenant policy compiler that decides, for each field and sensitivity class, what may enter any prompt, with signed exchange manifests.
- **Selected:** option 2. Most of it already exists (BL-45 gateway, BL-11 suggestions). Pattern: "LLM optional, evidence mandatory".
- **Falsifiable benchmark (BM-SD-02):**
  - *Setup:* an air-gapped VM with no egress, running 100 J11 questions.
  - *Success:* every question answered or abstained, zero network packets leaving the host (checked by packet capture), and median latency ≤ 3 s on CPU only.
- **Security failure cases:**
  - prompt injection hidden in source text reaching the summariser (CAP-49);
  - restricted rows leaking into summaries while ACL filtering (BL-18) is missing.
- **Defensibility:** buyers in defence, health and finance with air-gap mandates can verify this by audit. A SaaS-first vendor would have to re-architect its provider layer to match.
- **Decision:** **ADOPT.**

**INV-stardog-03 — Silent profile-dropping and rule skipping make inference opaque**
- **Target / version / workload:** Stardog 12.x Blackout reasoner, SL default.
- **Evidence-supported limitation:** out-of-profile axioms are ignored and invalid rules are skipped, with log lines only. [CLAIM-stardog-07] [CLAIM-stardog-08]
- **Root cause:** **UX and governance** — *proven*.
- **Why the alternative helps, and when it is worse:** fail-closed ontology CI. Each ontology release is checked against the OWL profiles (EL, QL, RL, DL), and any construct the active reasoner does not support blocks the release with a report. This is worse when users want permissive, best-effort exploration, so offer an explicit permissive mode with a visible banner.
- **Options:**
  1. Run ROBOT or OWL API profile validation in CI.
  2. Build the profile check into the release gates of `ontology/gitops.py` (BL-32).
  3. A semantic diff that shows *which answers change* when an axiom would be dropped.
- **Selected:** option 2, plus a step toward option 3.
- **Falsifiable benchmark:** inject 20 out-of-profile axioms into a test ontology. Success: all 20 reported before release, none dropped silently.
- **Defensibility:** governance-as-code (`gitops.py`) is EOIP's stated moat.
- **Decision:** **ADOPT.**

**INV-stardog-04 — Full-replica, all-acknowledge cluster limits write scaling**
- **Target / version / workload:** Stardog 12.x HA cluster, write-heavy ingest.
- **Evidence-supported limitation:** larger clusters are worse for writes, and there is no sharding. [CLAIM-stardog-14]
- **Root cause:** **storage and deployment** — *proven* (documented).
- **What it means for EOIP:** EOIP does not build storage. The inversion is to keep the **ingest log** (SourceEvent, BL-23/BL-24) as the scale-out boundary, and let backends that do shard absorb the writes (Neptune, distributed HugeGraph, Neo4j composite databases). This is worse against a single strongly consistent store, where fan-out across backends adds lag.
- **Options:**
  1. Document per-backend write ceilings.
  2. Batch writes per partition in the mutation gateway.
  3. Partition the ingest log per tenant.
- **Selected:** none now.
- **Decision:** **DEFER**. Revisit when the scale-out work package starts.

## 13. Per-capability decisions

| Capability | Decision | Rationale |
|---|---|---|
| CAP-22 incremental rule materialisation | **BUILD** a bounded RL/Datalog subset; **EXPERIMENT** with the tiered planner | INV-stardog-01 |
| CAP-23 OWL profile reasoning | **INTEGRATE** customer-supplied engines (GraphDB, Jena, Stardog) over SPARQL; **REUSE** profile checkers (OWL API, ROBOT) in CI | Do not rebuild a description-logic reasoner (project ontology strategy) |
| CAP-24 explanation and proof traces | **BUILD** inside the inferred plane | Stardog offers a CLI `explain` only (depth UNVERIFIED) |
| CAP-10 SHACL | **REUSE** pySHACL (Apache-2.0) behind the gate; **INTEGRATE** backend SHACL where available | STR-stardog-03 |
| CAP-21 virtualisation | **BUILD** (finish the virtual/materialised split already in the working tree); **INTEGRATE** Ontop for SQL sources (see W12) | STR-stardog-02 |
| CAP-29 R2RML/RML | **BUILD** R2RML import into the mapping IR (in progress) | Parity |
| CAP-58 NL→query and suggestions | **BUILD** (extend BL-11 and BL-12) | STR-stardog-04 |
| CAP-60 grounded answers and abstention | **BUILD** | STR-stardog-04 |
| CAP-51 egress control | **BUILD** (already BL-45; extend) | INV-stardog-02 |
| CAP-15 SPARQL backend (Stardog) | **DEFER** a native Stardog adapter. Stardog speaks the SPARQL 1.1 Protocol, so a repaired generic SPARQL adapter (C02-apache-jena INV-apache-jena-01) covers it | No demand evidence yet |
| CAP-76 HA and DR | **REJECT** building it; inherit from the backend | Not EOIP's layer |
| CAP-77 licensing and TCO | **REJECT** bundling Stardog | Proprietary, no OEM terms |

## 14. Concrete tests, proof-of-concept, and acceptance conditions

All tests below are **PROPOSED**. None was run.

| Test | Setup | Acceptance |
|---|---|---|
| BM-SD-01 Reasoning latency variance | LUBM(50) plus the synthetic IT ontology. Engines: GraphDB Free (`owl2-rl-optimized`), Jena rules, EOIP hybrid; Stardog only if the licence review clears it | EOIP p99/p50 ≤ 3; correctness matches the LUBM gold answers |
| BM-SD-02 Air-gapped NL | J16 VM, a local Ollama model, 100 J11 questions | Zero egress packets; 100 % answered or abstained; every answer carries a plan and evidence |
| POC-SD-03 SHACL guard | W3C SHACL Core test suite run through pySHACL in `validation/gate.py` | ≥95 % pass; a violating mutation is rejected; the report is stored with the mutation ID |
| POC-SD-04 Virtual vs materialised | Postgres fixture, an R2RML mapping, the same 20 queries in both modes | Identical result multisets (apart from documented bag-semantics differences); a freshness label on every row |
| POC-SD-05 Profile gate | An ontology with 20 injected out-of-profile axioms | All 20 flagged before release |
| POC-SD-06 ACL inheritance of inferred facts | Two principals; the premise is restricted to principal A | B never sees the inferred fact; after revocation it disappears within one sync cycle (J5) |

## 15. Risks, trade-offs, and open research questions

**Risks.**
- **R1 (legal).** The Free EULA prohibits evaluation "to compete with Stardog". Any Stardog benchmark that EOIP publishes needs legal review first. [CLAIM-stardog-17]
- **R2 (maintenance).** Even a bounded reasoner adds maintenance. Keep it to an RL/Datalog subset with W3C test cases, and integrate external engines for anything more expressive.
- **R3 (sales).** Voicebox's answer quality has not been measured publicly, so EOIP may underestimate it. Evaluate it through a Stardog Cloud Knowledge Kit; this needs an account and was not done in this run.

**Open questions.**
- **Q1.** Can an air-gapped Stardog server activate its licence offline? (UNVERIFIED)
- **Q2.** Is BARQ generally available in 12.x, and does it apply to reasoning queries?
- **Q3.** What exactly does Voicebox send to the LLM: a schema subset, rows, row counts? Is there a redaction hook?
- **Q4.** How deep does `reasoning explain` go: full proof trees, or one step?
- **Q5.** How does Stardog's named-graph security interact with reasoning? Can an inference cross a security boundary?

---

## Appendix A — Research-dimension coverage

| Dimension | Covered in section(s) | Summary or N/A reason |
|---|---|---|
| D1 Identity and maturity | 1 | Proprietary; 12.2.0 released 2026-10-14; two maintained lines; new CEO 2025-09-30; no acquisition |
| D2 Problem and workloads | 2 | Semantic layer / data fabric, reasoning, NL answer engine; on-prem server viable |
| D3 Architecture decomposition | 4, 5 | JVM server, browser apps, Voicebox service, ZooKeeper (cluster only) |
| D4 Storage primitives and indexing | 5.2 | RocksDB LSM with MVCC (documented); the permutation layout is a hypothesis |
| D5 Schema and semantic expressivity | 3, 5.1, 5.4 | RDFS and OWL 2 profiles, rules, SHACL; OWL 2 DL limited to data in memory |
| D6 Query pipeline and optimisation | 5.3 | SPARQL and GraphQL; EQ rewriting; BARQ; virtual-graph pushdown |
| D7 Reasoning and inference | 5.4, 9, 12 | Query-time rewriting; Blackout vs Stride; seed hypothesis partially validated |
| D8 Transactions, concurrency, scale | 5.5, 5.6 | Snapshot isolation / MVCC; full-replica strong consistency; no sharding |
| D9 Ingestion and federation | 2, 3, 5.3 | Virtual graphs, `virtual import`, CSV/JSON import with provenance |
| D10 Identity and evidence | 3, 11 | Import provenance only; no entity-resolution feature found in the sources examined (UNVERIFIED) |
| D11 Time and evolution | 5.8 | Point-in-time restore, schema hash versioning; no branching or as-of queries |
| D12 Graph algorithms and ML | 3 | ML support deprecated in 12.2.0; no graph algorithm library found in the sources examined |
| D13 Retrieval and agent integration | 5.10 | Voicebox RAG over unstructured documents; multi-agent in private preview; MCP support not found (UNVERIFIED) |
| D14 Natural-language querying | 5.10, 12 | LLM→SPARQL with ontology vector matching and abstention |
| D15 Governance and authoring | 2, 3 | Designer; no Git-native ontology workflow documented |
| D16 Human experience | 3 | Studio, Designer, Explorer, Launchpad |
| D17 Developer experience | 3, 9 | HTTP API, CLI, pystardog; opaque rule errors (L1) |
| D18 Trust and security | 5.9 | RBAC, LDAP, SSO passthrough; encryption at rest removed |
| D19 Multi-tenancy and white-label | 5.1, 10 | Named schemas and databases; no white-label or OEM terms |
| D20 Empirical economics | 7 | No independent numbers; qualitative scaling documented |
| D21 Commercial and licensing | 9, 10 | Proprietary; the Free EULA says evaluation-only while the pricing page says commercial use is allowed; Enterprise priced on request |
| D22 Interoperability and lock-in | 10, 11 | Data exits through standards (SPARQL, SHACL, R2RML); SMS/SMS2 mappings, rule syntax and Voicebox configuration are proprietary |
| D23 IP and prior art | 15 | Stardog patents not searched (NOT PUBLICLY VERIFIED). Query rewriting is well-established prior art in the OBDA literature. Legal review, no conclusion |
| D24 Research quality | 1, 7, App. C | Mostly official documentation (high); corporate facts from the official news page; no independent benchmarks |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence CLAIM-ID | EOIP baseline (BL-ID + status) | Decision for EOIP | Priority hint |
|---|---|---|---|---|---|
| CAP-02 RDF/quad storage | native | CLAIM-stardog-15 | BL-06 Partial | INTEGRATE (only as an external SPARQL store) | P3 |
| CAP-09 ontology modelling | native | CLAIM-stardog-07 | BL-30 Partial | INTEGRATE external reasoners; REUSE profile checkers | P2 |
| CAP-10 SHACL | native (Core plus SPARQL, with exceptions) | CLAIM-stardog-13 | BL-29 Partial; BL-28 Implemented | REUSE pySHACL in the gate | P1 |
| CAP-15 SPARQL | native | CLAIM-stardog-12 | BL-06 Partial | BUILD a real SPARQL adapter (shared with Fuseki and GraphDB) | P2 |
| CAP-17 GraphQL | native | CLAIM-stardog-28 | BL-58 Absent | DEFER | P3 |
| CAP-21 federation / virtualisation | native | CLAIM-stardog-12 | BL-51 Partial | BUILD (finish) + INTEGRATE Ontop | P2 |
| CAP-22 rule materialisation | absent (query-time only) | CLAIM-stardog-06 | BL-30 Partial | BUILD (bounded) | P1 |
| CAP-23 OWL profile reasoning | native (RDFS/QL/RL/EL/SL; DL in memory only) | CLAIM-stardog-07, -11 | BL-30 Partial | INTEGRATE | P2 |
| CAP-24 explanation | partial (CLI explain) | CLAIM-stardog-11 | Absent for rules | BUILD | P1 |
| CAP-29 R2RML | native (plus SMS/SMS2) | CLAIM-stardog-12 | BL-33 Implemented (CML, not R2RML) | BUILD R2RML import | P2 |
| CAP-35 branching / rollback | partial (point-in-time restore only) | CLAIM-stardog-03 | BL-38 Implemented | — (EOIP ahead) | — |
| CAP-45 RBAC/ABAC | native (LDAP enterprise-only) | CLAIM-stardog-03, -16 | BL-19 Implemented | — | — |
| CAP-47 multi-tenant isolation | partial (named schemas, databases) | CLAIM-stardog-10 | BL-20 Partial | BUILD (P0 per Master Prompt §4.3) | P0 |
| CAP-50 air-gapped operation | partial (server yes; Voicebox no) | CLAIM-stardog-20 | BL-45 Implemented | BUILD / verify J16 | P0 |
| CAP-51 LLM egress control | absent (provider-level identity only) | CLAIM-stardog-20 | BL-45 Implemented | — (EOIP advantage) | — |
| CAP-52 white-label / OEM | absent | CLAIM-stardog-17 | BL-21 Implemented | — (EOIP advantage) | — |
| CAP-56 GraphRAG | partial (Voicebox RAG over PDF/DOCX) | CLAIM-stardog-18 | BL-16 Implemented | — | — |
| CAP-58 NL→query and suggestions | native (LLM) | CLAIM-stardog-18 | BL-11 Implemented; BL-12 Partial | BUILD | P1 |
| CAP-60 grounded answers and abstention | native | CLAIM-stardog-18 | BL-16 (no abstention contract) | BUILD | P1 |
| CAP-74 backup / restore / PITR | native (enterprise) | CLAIM-stardog-03 | BL-50 Implemented | — | — |
| CAP-76 HA and DR | native (enterprise) | CLAIM-stardog-14 | inherited from backend | REJECT building | — |
| CAP-77 licensing and TCO | proprietary | CLAIM-stardog-16, -17 | BL-22 | REJECT bundling | — |

## Appendix C — Evidence records

| CLAIM-ID | product / version / date | exact claim | classification | source title + URL | publication date / access date | confidence + rationale | contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-stardog-01 | Stardog Platform 12.2.0 / 2026-10-14 | Latest releases: 12.2.0 and 12.1.5 (2026-10-14), 12.1.4 (2026-09-03), 12.1.3 (2026-08-26), 12.1.2 (2026-08-04), 12.1.1 (2026-07-01), 12.1.0 (2026-06-10), 12.0.0 (2026-02-12) | Officially documented | Stardog Platform Release Notes — https://docs.stardog.com/release-notes/stardog-platform | continuous / 2026-10-18 | 0.9 — official release notes | none |
| CLAIM-stardog-02 | 11.2.5 / 2026-08-01 | The 11.2.x line is still patched: 11.2.5 (2026-08-01), 11.2.4 (2026-06-10), 11.2.3 (2026-02-11) | Officially documented | same | 2026-10-18 | 0.9 | none |
| CLAIM-stardog-03 | 12.0.0 / 2026-02-12 | "Upgrade to Java 21"; point-in-time restore; stored queries as RBAC objects; "Drop BITES v1"; aggregate indexes removed; on-disk transaction log protocol with timestamps; block-based path operator; CLI-only client distribution | Officially documented | same | 2026-10-18 | 0.85 | none |
| CLAIM-stardog-04 | 11.0.0 / 2025-01-22 | NiFi connector removed; aggregate indexes deprecated; encryption at rest support removed; legacy SMS1 syntax removed; provenance capture for CSV/JSON imports; token authorization from the CLI | Officially documented | same | 2026-10-18 | 0.85 | none |
| CLAIM-stardog-05 | 12.2.0 / 2026-10-14 | Change a virtual graph's database; dialect-specific SQL functions; STRUCT in SQL virtual graphs; SingleStore connector; SPARQL date/time→SQL; functional-property semantics used to optimise reasoning; cluster as geo-replica; ARM Docker image; Purview v2; Entra ID for Power BI and BigQuery; machine-learning support, Purview v1 and ZooKeeper 3.8 deprecated | Officially documented | same | 2026-10-18 | 0.85 | none |
| CLAIM-stardog-06 | current docs | "it does not materialize inferences"; "computes inferences as needed, on-the-fly, using a query rewriting approach"; axioms and rules are "(basically) Datalog rules over a graph" | Officially documented | Inference Engine — https://docs.stardog.com/inference-engine/ | 2026-10-18 | 0.9 | none |
| CLAIM-stardog-07 | current docs | `reasoning.type` ∈ RDFS, QL, RL, EL, SL; the SL default combines RDFS, QL, RL, EL and SWRL; "Any axiom outside the selected type will be ignored by the reasoner" | Officially documented | same | 2026-10-18 | 0.9 | CLAIM-stardog-11 says full OWL 2 DL is supported for data in memory |
| CLAIM-stardog-08 | current docs | Stride reasoner (beta) supports negation and aggregation over a smaller axiom set and is "currently not recommended for production usage"; it halts on an invalid rule, while Blackout skips the rule and logs it | Officially documented | same | 2026-10-18 | 0.85 | none |
| CLAIM-stardog-09 | current docs | Rule restrictions: no variables in predicate position except with rdf:type; limited recursion that maps to property paths | Officially documented | same | 2026-10-18 | 0.8 | none |
| CLAIM-stardog-10 | current docs | Schemas are named graphs (default `tag:stardog:api:context:schema`); named schemas support multi-tenancy; `owl:imports` is not followed; schema versioning by content hash (10+), with overhead for large schemas | Officially documented | same | 2026-10-18 | 0.85 | none |
| CLAIM-stardog-11 | current docs | "the larger the EQ, the longer it takes to evaluate"; variable predicate or type patterns "often cause performance problems"; reasoning "pulls the complete schema into memory"; the first reasoning query triggers slow schema processing, repeated after the database is modified; expressive schemas cost time and memory; full OWL 2 DL only for data in main memory; the domain/range optimisation is on by default since 12; CLI commands `reasoning explain` and `reasoning consistency` exist | Officially documented | Inference troubleshooting — https://docs.stardog.com/inference-engine/troubleshooting | 2026-10-18 | 0.85 | none |
| CLAIM-stardog-12 | current docs | Virtual graphs rewrite SPARQL "into native query syntaxes like SQL"; sources: RDBMS, CSV, MongoDB, Elasticsearch, Cassandra, JSON; mappings: SMS (default), R2RML, SMS2; the user supplies JDBC drivers; `virtual import` materialises; limitations: duplicate solutions, MINUS not translated to SQL, R2RML named graphs unsupported; cached datasets must be recreated when a virtual graph changes database | Officially documented | Virtual Graphs — https://docs.stardog.com/virtual-graphs/ | 2026-10-18 | 0.85 | none |
| CLAIM-stardog-13 | current docs | Supports SHACL Core except prebinding $shapesGraph/$currentShape, property validators, and SHACL-AF/JavaScript; guard mode (`icv.enabled`) fails violating transactions; "the validation results will change if reasoning is enabled or disabled" | Officially documented | Data Quality Constraints — https://docs.stardog.com/data-quality-constraints | 2026-10-18 | 0.85 | none |
| CLAIM-stardog-14 | current docs | ZooKeeper (odd ensemble, at least 3) holds membership and locks; at least 2 Stardog nodes; "all nodes in the cluster have all of the data"; a commit is acknowledged after all non-failing peers commit; "larger Stardog clusters perform better than smaller ones for reads but worse for writes" | Officially documented | High Availability Cluster — https://docs.stardog.com/high-availability-cluster/ | 2026-10-18 | 0.85 | none |
| CLAIM-stardog-15 | 7.0 / 2019 | Mastiff storage engine built on RocksDB (LSM tree), adding MVCC and snapshot isolation; vendor claim of "10x and 20x" write improvement; 20–30 % more disk use | Officially documented (vendor blog; old) | Mastiff Storage Engine — https://www.stardog.com/blog/mastiff-storage-engine ; Announcing Stardog 7 — https://www.stardog.com/blog/announcing-stardog-7 | 2019 / 2026-10-18 | 0.6 — old source; current internals not re-verified; the performance figure is Unverified | none |
| CLAIM-stardog-16 | pricing page | Stardog Free costs nothing, has a renewable 1-year licence, is "available for commercial use", and lacks HA, caching, backups, LDAP and the full set of connectors; Enterprise runs on-prem or in the cloud, priced on request | Officially documented | Pricing & Licensing — https://www.stardog.com/pricing/ | 2026-10-18 | 0.7 | **Contradicted by CLAIM-stardog-17** |
| CLAIM-stardog-17 | Free EULA, revised 2022-12-13 | "non-exclusive, non-transferable revocable license … for the sole purpose of evaluating Stardog"; "Using Stardog for any business purpose other than evaluating Stardog is expressly prohibited"; no sublicensing or derivative works; no evaluation to compete | Officially documented (legal text) | Stardog Free licence — https://www.stardog.com/legal/stardog-free/ | 2022-12-13 / 2026-10-18 | 0.8 — binding text; the footer date (1/9/23) does not match | CLAIM-stardog-16 |
| CLAIM-stardog-18 | Voicebox docs | Flow: identify concepts → match the ontology through an embedded vector store → the LLM generates SPARQL → query plan with SQL via mappings → the LLM summarises; returns "Cannot find an answer for this question."; tracks whether information came from RAG, code, an external LLM or the knowledge graph; multi-agent "only available as part of a private preview"; PDF/DOCX through a Spark-based RAG pipeline; the Studio integration ignores conversational context; the External LLM Agent "may contain Hallucinations" | Officially documented | Stardog Voicebox — https://docs.stardog.com/voicebox/ | 2026-10-18 | 0.85 | none |
| CLAIM-stardog-19 | Voicebox docs | Available to Cloud and on-prem/VPC customers; on-prem through Launchpad; "We don't use actual customer data to train or finetune our models" | Officially documented | same | 2026-10-18 | 0.8 | none |
| CLAIM-stardog-20 | Voicebox Service v1.1.1 | `llm_provider` ∈ anthropic, azure, bedrock, vertex, openai; openai `server_url` "can be set if OpenAI endpoint is access via proxy"; basic auth and OAuth for OpenAI-compatible proxies; image `stardog-stardog-apps.jfrog.io/voicebox-service:v1.1.1`; no air-gap statement; `$VOICEBOX_USER` lets "LLM requests carry user identity" | Officially documented | Voicebox Service configuration — https://docs.stardog.com/launchpad/voicebox-service/configuration | 2026-10-18 | 0.85 | CLAIM-stardog-21 lists other hosting options |
| CLAIM-stardog-21 | Stardog 11 / 2025 | Voicebox can be deployed in a customer VPC, connecting to Bedrock or SageMaker, Azure AI Foundry, or Databricks Mosaic AI | Third-party report (vendor community post, seen only as a search snippet) | What's New in Stardog 11 (2025.1) — https://community.stardog.com/t/what-s-new-in-stardog-11-2025-1/5259 | 2025 / 2026-10-18 | 0.55 — snippet only, page not opened | CLAIM-stardog-20 (the current provider list differs) |
| CLAIM-stardog-22 | Karaoke / 2023–2024 | On-prem "Karaoke" server, built with Nvidia and Supermicro, hosting a fine-tuned Llama 2 variant for Voicebox | Third-party report / vendor press | Stardog news — https://www.stardog.com/news/stardogs-karaoke-offers-on-premises-zero-hallucination-llm-solution-for-enterprises | 2024 / 2026-10-18 | 0.4 — historical; absent from current docs | absent from CLAIM-stardog-20 |
| CLAIM-stardog-23 | corporate / 2025–2026 | CEO Craig Harper appointed 2025-09-30; CPO Navin Sharma 2026-05-11; new brand identity 2026-06-11; CRO Alan Gibson 2026-08-11; no acquisition news | Officially documented | Stardog News — https://www.stardog.com/news/ | 2026-10-18 | 0.85 | Owler still lists Kendall Clark as CEO (out of date) |
| CLAIM-stardog-24 | funding | Series B extended to USD 11.4 M (2020); Accenture investment (2023); totals of USD 23–33 M depending on the tracker | Third-party report | Stardog news (Series B) — https://www.stardog.com/news/stardog-the-leading-enterprise-knowledge-graph-platform-expands-series-b-to-11.4-million-to-mature-go-to-market-initiatives/ ; CB Insights — https://www.cbinsights.com/company/stardog | 2020 / 2026-10-18 | 0.5 — trackers disagree | Tracxn contradicts itself |
| CLAIM-stardog-25 | Knowledge Kits | Pre-built databases with domain models and dummy data (for example healthcare, insurance, C360), free | Officially documented (vendor blog) | Stardog Knowledge Kits — https://www.stardog.com/blog/stardog-knowledge-kits-your-path-to-mastery-in-knowledge-graphs/ | 2026-10-18 | 0.6 — via search snippet | none |
| CLAIM-stardog-26 | Designer | Visual environment for the data model and mappings, publishing to an endpoint; Voicebox helps create concepts and make bulk edits | Officially documented | Designer — https://docs.stardog.com/stardog-applications/designer/ ; Voicebox — https://docs.stardog.com/voicebox/ | 2026-10-18 | 0.7 | none |
| CLAIM-stardog-27 | 11.1.0 / 2025-06-11 | Voicebox is disabled on databases with extremely large schemas | Officially documented | Release notes (as CLAIM-01) | 2026-10-18 | 0.8 | none |
| CLAIM-stardog-28 | 11.1.0 / 11.2.0 | 11.1.0: rename database, query triggers, Semantalytics functions, Ubuntu 20 dropped, BARQ binary/unary index scans. 11.2.0 (2025-10-01): rolling minor-version upgrade, GraphQL predicate IRIs, Stride variable predicates, BARQ join fixes | Officially documented | Release notes | 2026-10-18 | 0.85 | none |
| CLAIM-stardog-29 | 10.1.0 / 2024-06-05 | BARQ introduced as a beta feature; Windows server support dropped | Officially documented | Release notes | 2026-10-18 | 0.8 | GA status of BARQ unverified |
| CLAIM-stardog-30 | 12.1.0 / 2026-06-10 | Okta passthrough authentication; Teradata virtual graphs; Spark on Kubernetes as external compute; GraphQL `@type` fix; reasoning-timeout fix | Officially documented | Release notes | 2026-10-18 | 0.85 | none |
| CLAIM-stardog-31 | Voicebox reporting | CSV reports of exchanges (questions, generated SPARQL, responses, feedback) for users with READ on `dbms-admin:logs` | Officially documented | Voicebox docs | 2026-10-18 | 0.8 | none |
| CLAIM-stardog-32 | 2025-09 | "Hallucination-free" answer engine | Unverified (vendor marketing) | Stardog News — https://www.stardog.com/news/ | 2025-09-03 / 2026-10-18 | 0.2 — marketing | The Voicebox docs say the External LLM Agent "may contain Hallucinations" |

## Appendix D — Assumptions

1. "Stardog (incl. Voicebox)" means Stardog Union's platform and Voicebox. C07's "Stardog Voicebox" is covered by this file.
2. Stardog is closed source, so its code could not be inspected. Internals in §5 beyond the documentation are hypotheses.
3. The release-notes page describes the self-managed platform. Stardog Cloud may run different builds.
4. The Free EULA (the legal text) is taken as binding over the wording on the pricing page. This is a legal-review item, not a conclusion.
5. A local LLM behind an OpenAI-compatible proxy *might* work with Voicebox, but the documentation does not support it, so it is not treated as supported.
6. No account was created and no trial was run (Methodology §8).
7. EOIP's working tree contains uncommitted `mapping/r2rml.py` and `mapping/virtualization.py`. They are cited as work in progress, not as baseline capabilities.
