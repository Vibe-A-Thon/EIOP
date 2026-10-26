| Field | Value |
|---|---|
| Registry ID | T-C08-openspg-kag |
| Tier | A (schema-governed, logical-form GraphRAG alternative from Ant Group; closest GraphRAG family member to EOIP's ontology-first stance) |
| Versions examined | KAG `v0.8.0` (GitHub release 2025-06-29, notes dated 2025-06-27; PyPI `openspg-kag` 0.8.0 uploaded 2025-06-30); KAG releases v0.5 (2024-11-04) … v0.7.1 (2025-04-25); OpenSPG engine repo: last release listed v0.8 line, last commit 2025-06-29; KAG-Thinker (separate repo, Qwen2.5-7B based). KAG master last commit seen: 2026-01-28 (`fdab15b`, MCP store_path fix). |
| Verified on | 2026-10-18 |
| Worker | V10 (registry seed W21) |

## 1. Identity, current status, tier, and sources

**Two repositories, one product family.** (a) `OpenSPG/openspg` — the *SPG engine*: schema management, KGDSL reasoner, builder framework, server, pluggable storage "cloudext"; Apache-2.0; ~2.3k stars. (b) `OpenSPG/KAG` — the *Knowledge Augmented Generation framework* built on OpenSPG: `kag/builder`, `kag/solver`, `kag/indexer`, `kag/mcp`, `kag/open_benchmark`; Apache-2.0; ~9.1k stars, 1,261 commits. (c) `OpenSPG/KAG-Thinker` — released 7B reasoning models (Qwen2.5-7B-Instruct base; repo licence Apache-2.0; model-weight licence beyond that label NOT PUBLICLY VERIFIED). Owner: Ant Group Knowledge Engine team with OpenKG community / Zhejiang University co-authors. [CLAIM-openspg-kag-01][02][03]

| Aspect | Verified state |
|---|---|
| Licence | Apache-2.0 (KAG README; OpenSPG README). PyPI `openspg-kag` licence metadata is empty (`None`) — rely on repo LICENSE, not PyPI [01][02][09] |
| Release history (KAG) | v0.5 2024-11-04 (first official; Oct 25 notes), v0.5.1 2024-11-22, v0.6 2025-01-08, v0.7 2025-04-17, v0.7.1 2025-04-25, **v0.8.0 2025-06-29 (latest)** [04] |
| Activity | **Slowing / possibly maintenance-only.** No release after 0.8.0 in ~16 months. KAG master commits: 2025-06-30 … 2025-08-06 (solver fixes), then one commit seen on 2026-01-28 (MCP fix). OpenSPG engine: last commit 2025-06-29. Treat as *low-cadence* — a roadmap/continuity risk [CLAIM-openspg-kag-05] |
| Governance | Corporate-led open source (Ant Group); OpenKG community; no foundation. Patents: Ant Group may hold patents on related methods — NOT PUBLICLY VERIFIED; flag for IP review (D23) |
| Name collisions | "SPG" = Semantic-enhanced Programmable Graph (this project) — unrelated to Spring/"SPG" elsewhere; "KAG" = Knowledge Augmented Generation (also "KG-augmented generation" used generically in papers). OpenSPG/KAG-Thinker is a separate artifact |
| Primary paper | arXiv:2409.13731, "KAG: Boosting LLMs in Professional Domains via Knowledge Augmented Generation", v1 2024-09-10, v3 2024-09-26; 18 authors incl. Lei Liang, Huajun Chen, Jun Zhou. KAG-Thinker: arXiv 2506.17728 [06][07] |

Cross-references: `C08-microsoft-graphrag.md`, `C08-lightrag.md`, `C08-hipporag.md` (KAG's paper benchmarks against HippoRAG), `C08-llamaindex-pgi.md` (framework-style alternative), `C08-graphiti-zep.md`, `C08-cognee.md`, `C08-neo4j-graphrag.md` (may be in progress by another batch).

## 2. Primary problem, target workloads, concrete example workflows

**Problem (vendor framing).** Vector similarity ≠ reasoning relevance; plain RAG handles numeric, temporal and rule-bound questions badly; OpenIE-built graphs are noisy. KAG proposes a schema-governed three-layer store plus a planner that decomposes questions into *logical forms* and executes them over graph, then falls back to hybrid text retrieval. [06]

| Workload | Fit |
|---|---|
| Professional-domain QA (e-government, e-health — Ant's own deployments, vendor-reported) | Designed target |
| Multi-hop QA over document sets | Designed target (benchmarks) |
| Question types needing counts/sorting/set compare | Designed target via Math/Sort/Deduce operators |
| Governed enterprise graph with source ACLs, multi-tenant, event-sourced updates | Not a design goal (see §9) |

**Workflow W1 (build).** Define `*.schema` (EntityType/EventType with typed properties and index annotations such as `TextAndVector`) → run `DefaultUnstructuredBuilderChain` (reader → splitter → extractor → vectorizer → post-processor → writer) → graph + chunks stored via OpenSPG server (v0.8 "knowledge bases" decoupled from apps).
**Workflow W2 (ask).** Question → planner (static / iterative / model-based) → logical-form steps executed by retriever / deduce / math / mcp executors → generator with reporter (shows reasoning steps in UI) → answer.
**Workflow W3 (lightweight).** v0.7 "Lightweight Construction" mode: vendor says it reduces construction token cost by 89% (workload and baseline not given on the README) [CLAIM-openspg-kag-08].

## 3. Feature inventory

| Feature | Status | Evidence |
|---|---|---|
| Web UI (project, knowledge base, task scheduling, reasoning-step display, login/permissions added v0.6) | Present | [04] |
| HTTP API, MCP integration, embeddable Q&A page | Present (v0.8) | [04] |
| Python SDK / `kag` CLI toolkit (`pip install openspg-kag`, `kag` project scaffolding) | Present | [09] (CLI command surface UNVERIFIED in detail) |
| Declarative schema (`.schema` DSL, entity/event/concept types, properties, relations, index annotations) | Present | [10] |
| SPG semantic enhancement (subject/evolutionary/predicate models; concept types; logical rules via KGDSL) | Present (OpenSPG) | [02] |
| Builder: structured mapping chain; unstructured chain with extractor/splitter/vectorizer/post-processor | Present | [11] |
| Index types (KnowledgeUnit, Outline, Summary, Chunk, AtomicQuery, Table), configurable per KB | Present (v0.8) | [04] |
| Knowledge alignment (synonym/isA/isPartOf/contains/belongTo/causes) | Present per paper; code location NOT PUBLICLY VERIFIED | [06] |
| Solver planners: static, iterative, LF-static, model (Thinker), MCP | Present (file names at v0.8.0) | [12] |
| Executors: retriever, deduce, math, mcp, finish | Present (dirs at v0.8.0) | [12] |
| Resumable tasks, DB-based build scheduling, per-stage model config | Present (v0.6) | [04] |
| Domain schema management, visual query analysis, QFS (summary) tasks | Present (notes 2025-01-07) | [04] |
| Incremental / delete-by-source updates | Project deletion API (v0.5.1); document-level incremental graph maintenance NOT PUBLICLY VERIFIED | [04] |
| Source ACLs, per-fact permissions, tenancy | Login/permissions exist at product level (v0.6); per-fact/source-ACL propagation absent from public descriptions | [04] |
| Bitemporal / versioned facts | Absent from public descriptions; "evolutionary model" in SPG is schema-evolution/ event semantics, not bitemporality (UNVERIFIED detail) | [02] |
| kag-model (own fine-tuned extraction/reasoning models) | Announced "gradually open sourced"; KAG-Thinker 7B released separately | [01][07] |

## 4. Architecture diagram

```
 Sources (docs, DB mappings) ----> KAG Builder (kag/builder: component/model/operator/prompt)
   reader -> splitter -> extractor(LLM, schema-constrained or open) -> vectorizer -> post-processor(align) -> writer
                                                                                              |
                                  +-----------------------------------------------------------+
                                  v
  OpenSPG Server (Java; project/schema/task/auth APIs; cloudext adapters)
     |-- Schema registry (SPG-Schema: EntityType/EventType/Concept, rules)
     |-- Graph store  (Neo4j confirmed in release notes; TuGraph and others per paper; "pluggable")
     |-- Vector/text index (in-graph vectors or external; ES/Milvus named in paper)
     |-- Relational metadata/scheduling DB (v0.6 "database-based scheduling"; product unnamed)
     `-- SPG-Reasoner (KGDSL rules)
                                  ^
  Query: KAG Solver (kag/solver) -- planner -> executors -> generator -> reporter
     planner(static|iterative|LF|Thinker-model|MCP)
        -> logical forms: Retrieval(s,p,o), Sort, Math, Deduce, Output   [paper]
        -> executor.retriever: graph match; if empty/low -> hybrid (text + LF constraints)
        -> global memory of step results; judge may ask follow-up (<= n rounds)
  Surfaces: Web UI, HttpAPI, MCP server, embedded page
  Layers (paper): KG_cs (curated, schema) / KG_fr (extracted) / RC (raw chunks) -- mutual index between them
```

## 5. Under-the-hood reconstruction

**Data model — "LLMFriSPG"** [CLAIM-openspg-kag-06]: three layers share one type/concept system: (1) *KG_cs* schema-constrained, expert-curated knowledge (accurate, costly), (2) *KG_fr* OpenIE/LLM-extracted graph information (coverage), (3) *RC* semantically segmented raw chunks as traceable context. Each property = pre-defined part + ad-hoc part + built-in fields (supporting chunks, description, summary, belongTo). Chunk ids are composite (article id, paragraph code, in-paragraph index) so neighbours have adjacent ids. Chunks are stored *as graph nodes of type Chunk*.

**Mutual indexing** [06]: edges between graph nodes and chunks (supporting chunks / summary / description) form a "graph-based inverted index"; retrieval can start from text (vector/BM25 → chunk → linked entities) or from graph (entity → supporting chunks). Reconstruction hypothesis: `entity -[supportedBy]-> Chunk` plus `Chunk.content` text+vector indexes declared in schema (`index: TextAndVector`) [10].

**Schema DSL** [10] (quoted fragment from the v0.8.0 CsQa example):
`Chunk(文本块): EntityType / properties: / content(内容): Text / index: TextAndVector` — types carry Chinese display names in parentheses, typed properties, relation blocks and per-property index annotations (`Text`, `TextAndVector`, `MultiValue` constraint).

**Knowledge alignment** [06]: six semantic relations (synonym, isA, isPartOf, contains, belongTo, causes). At index time: disambiguate/merge synonymous instances, link instances to concepts, complete hypernym chains. At retrieval time: exact type match first, then walk semantic relations (e.g. "political party" → "political faction"). Vendor-reported ablation: top-5 chunk recall +15.7% on average in their setting (paper's datasets/LLM only).

**Builder chains** (`kag/builder/default_chain.py`, v0.8.0) [11]: `DefaultStructuredBuilderChain` = mapping → (vectorizer) → writer; `DefaultUnstructuredBuilderChain` = reader → splitter → extractor → vectorizer → post-processor → writer (only reader mandatory). Registered names `structured` / `unstructured`. Extractors can be schema-constrained or schema-free; 2025-01-07 notes add "schema-constrained extraction". Per-stage model configuration since v0.6.

**Solver pipeline** (`kag/solver/{planner,executor,generator,pipeline,reporter,prompt}`; planners `kag_static_planner.py`, `lf_kag_static_planner.py`, `kag_iterative_planner.py`, `kag_model_planner.py`, `mcp_planner.py`; executors `retriever/`, `deduce/`, `math/`, `mcp/`, `finish_executor.py`) [12]. Paper algorithm [06]:

```
plan   = planner(question)                    # logical forms, e.g. Retrieval(s=?x:Person, p=bornIn, o=City[Paris])
memory = {}
for round in 1..n:
    for step in plan:
        r = graph_match(step)                 # schema-typed pattern match, variables reused across hops
        if empty(r) or low_score(r):
            r = hybrid_retrieve(step.nl_subquestion, step.constraints)   # text + subgraph, aligned types
        memory[step.output] = r
    if judge(question, memory).sufficient: break
    plan = planner.refine(question, memory)
answer = generator(question, memory, chunks)
```
Operators: Retrieval, Sort (top-N), Math (LaTeX-style count/sum), Deduce (entailment/greater/less/equal), Output. v0.7 added static vs iterative planning and "Simple Mode" vs "Deep Reasoning"; v0.8 adapts to KAG-Thinker (7B model that decomposes into logical forms and decides when to search; its paper claims +4.1% average vs trained deep-search models on seven benchmarks — vendor claim) [07][08].

**Reasoner** (OpenSPG `reasoner`, KGDSL): rule language for logic-based inference; commit "support necessary rule expression" 2025-03-20; expressivity bounds (Datalog-like? negation? recursion?) NOT PUBLICLY VERIFIED [02].

**Storage / concurrency / partitioning / consistency**: Neo4j named in release notes (memory-overflow and GDS conflicts under concurrency fixed v0.5.1; delete-project clears project's Neo4j database); paper names TuGraph/Neo4j for graph and Elasticsearch/Milvus for vectors. Transaction semantics, sharding and consistency are inherited from the chosen engine; no multi-writer coordination documented. Model-call concurrency default 5 (v0.5.1). **Versioning**: none public. **Caching**: none documented. **Security**: login/permissions (v0.6) at application level; no source-ACL-to-fact mapping documented; MCP surfaces added v0.7/0.8 (`McpExecutor`) widen the tool-injection surface (hypothesis).

## 6. Inferred requirements

| ID | Requirement |
|---|---|
| F1 | Schema-first modelling with typed properties, event/concept types and index declarations |
| F2 | Three-layer store with bidirectional graph↔chunk links |
| F3 | Question decomposition into executable, typed sub-queries with deterministic operators (math/sort/set compare) |
| F4 | Graceful fallback from exact graph match to hybrid retrieval |
| F5 | Concept-graph alignment at index and query time |
| N1 | Many LLM calls per question (planner, per-step, judge, generator) → latency scales with rounds |
| N2 | Requires the OpenSPG server + graph store + vector store + DB to be running (multi-service) |
| N3 | Prompts/schemas are Chinese-first (display names, prompt directories) — localisation effort for non-Chinese tenants (inference from sample schema; confidence 0.6) |

## 7. Performance and resource model

**Vendor-reported (paper, arXiv:2409.13731)** — 1,000 validation questions per dataset; EM/F1; DeepSeek-V2 as the KAG LLM in the headline row; baselines include NativeRAG (ColBERTv2, ChatGPT-3.5), HippoRAG, IRCoT+HippoRAG. Selected F1: HotpotQA 76.2 (KAG-LFSH) vs 63.7 (IRCoT+HippoRAG, DeepSeek-V2); 2Wiki 76.2 vs 57.1 (same baseline row); MuSiQue 48.7 vs 36.5. Abstract's "+19.6% F1 on HotpotQA, +33.5% on 2Wiki" reproduces from these rows (our arithmetic: 76.2/63.7 = 1.196; 76.2/57.1 = 1.334, i.e. ~33.5% allowing rounding) [CLAIM-openspg-kag-07]. Caveats: single-vendor, standard academic multi-hop sets (Wikipedia-based, prone to contamination for modern LLMs), baselines taken partly from other papers with different LLMs, no variance/seeds reported in what we read, no cost normalisation. **Not an independent benchmark; do not compare against LightRAG/GraphRAG numbers from other papers.** Ablation: 3 reflection rounds > 1 round; LF hybrid costs more compute than chunk retrieval (paper, qualitative).

**Resource facts**: v0.7/0.8 benchmarks used Qwen2.5-72B as the base model (bge-m3 embeddings in v0.7); Lightweight Construction used a 7B for construction and 72B for Q&A (release notes) [CLAIM-openspg-kag-04][08]. Hence a *published quality figure depends on a 72B-class model* — behaviour with CPU-viable local models is NOT PUBLICLY VERIFIED (KAG-Thinker 7B is the vendor's answer; its quality claims are vendor-only). Footprint: Docker + Docker Compose required (README); stack comprises openspg-server, a Neo4j image (`openspg-neo4j`), a relational DB and other services (compose file and exact component list not retrieved — UNVERIFIED; one unofficial community guide lists MySQL, Redis, Neo4j, MinIO). Memory/disk per million nodes, p50/p95 latency, ingest rate: NOT PUBLICLY VERIFIED. Failure modes: planner producing invalid logical forms → fallback to hybrid; model-concurrency throttling; Neo4j memory pressure (v0.5.1 fix).

## 8. Strengths and use-case-specific advantages

| Strength | How EOIP could match/exceed |
|---|---|
| Schema-constrained construction unified with open extraction under one type system (LLMFriSPG) | EOIP ontology gate (BL-27/28/29) already schema-first; add "curated vs extracted vs raw" labelling mapped to BL-40 epistemic classes |
| Mutual graph↔chunk indexing with traceable chunks | EOIP evidence manifests (BL-41) + chunk nodes; ensure bidirectional index and span-level citation |
| Logical-form planning with deterministic Math/Sort/Deduce operators | EOIP typed `QueryPlan` (BL-08) is the safer analogue; add arithmetic/aggregate operators executed by code, never by LLM |
| Fallback chain graph → hybrid when graph match fails | Already conceptually in BL-15/16; formalise "abstain or fall back" policy with logged reason |
| Concept-based alignment (isA/synonym chain) to bridge wording gaps | Implement as ontology-driven query expansion (SKOS/subClassOf in BL-30) — no LLM needed |
| Reasoning-step transparency in UI | Matches EOIP XAI (BL-48); expose plan + operator trace per answer |
| 7B reasoning model released for local use | Evaluate as optional local planner; licence of weights must be checked |

### Strength-adoption cards

| ID | Competitor | Strength | Evidence | Value | Verdict | Design | Acceptance |
|---|---|---|---|---|---|---|---|
| STR-openspg-kag-01 | OpenSPG/KAG | Logical-form decomposition with deterministic operators | [06][12] | Correct counts/sorts/thresholds in answers | match via EOIP QueryPlan + code operators | Planner emits plan JSON; executor computes aggregates in SQL/Cypher/Python; LLM only phrases | On 100 numeric/temporal questions, 0 LLM-computed numbers; accuracy >= hybrid RAG |
| STR-openspg-kag-02 | OpenSPG/KAG | Three-layer fact model with shared type system | [06] | Separates curated vs extracted knowledge | exceed (add epistemic status, ACL, time) | Map KG_cs→APPROVED, KG_fr→PROPOSED/CORROBORATED, RC→evidence | Retrieval can filter by epistemic class; test returns only APPROVED facts when asked |
| STR-openspg-kag-03 | OpenSPG/KAG | Type-aware alignment fallback | [06] | Recall when terms differ | match | Ontology-driven expansion with explain trace | Recall@5 gain over no-expansion on EOIP eval set; every expansion logged with ontology axiom |
| STR-openspg-kag-04 | OpenSPG/KAG | Graph→hybrid fallback with reasoning trace | [06][12] | Robustness when KG sparse | match | Retrieval policy engine | Abstain/fallback rate reported; no ungrounded answer |

## 9. Limitations with root causes

**Algorithmic dead-ends**
- Multi-round planner/judge loops multiply LLM calls and latency; quality depends on LLM planning accuracy (paper: more reflection rounds help, at higher cost) (vendor-reported, proven qualitatively).
- LLM-extracted layer (KG_fr) retains OpenIE noise; alignment mitigates but quantification is vendor-only.

**Operational / hardware overhead**
- Multi-service stack (server + graph + DB + vector) vs EOIP's one-node goal; Neo4j concurrency/memory issues fixed in 0.5.1 indicate sensitivity (proven by release notes).
- Headline results use 72B-class models; local small-model viability unverified.
- Low commit cadence since mid-2025 (proven); roadmap items (`kag-model` open-sourcing) unclear.

**User/developer friction and governance**
- Schema DSL and prompts are Chinese-first in examples; English coverage uneven (inference, conf 0.6).
- Custom components require "replacing the installation package in the openspg-server image" (release notes) — heavy extension model.
- No public per-fact source ACL propagation, bitemporal history, tenant isolation or deletion-by-source semantics (absence in documentation read, not proof of absence).
- Licensing: Apache-2.0 code is redistribution-friendly; **dependencies** (Neo4j Community GPLv3, TuGraph licence, Elasticsearch SSPL/Elastic/AGPL options, MySQL GPL) are the legal-review surface, plus KAG-Thinker weights (Qwen2.5 base licence differs by size — NOT verified here).

### Inversion cards

**INV-openspg-kag-01 — Heavyweight multi-service footprint and model dependence**
- Target: KAG 0.8.0 build + solve, benchmark workload with 72B models. Limitation: needs OpenSPG server, graph, DB, vector; quality figures from 72B (proven by notes [08]). Root cause: *deployment/coupling* (proven).
- Alternative: embed schema-governed extraction + logical-form execution inside EOIP's existing services and `GraphStore` abstraction; worse when users want KAG's UI/task scheduler out of the box.
- Options: (1) quick: run KAG as an isolated sidecar for evaluation only; (2) native: implement plan-then-execute with typed operators over EOIP stores (BL-08) and local 7–14B planner; (3) long-term: ontology-conditioned fine-tuned local planner.
- Selected: 2. Sketch: `question -> LLM -> PlanFragment(JSON) -> validate vs ontology -> execute -> evidence set -> answer w/ spans`.
- POC: 150 multi-hop + numeric questions on an EOIP corpus; success = answer F1 within 5 points of KAG-sidecar using a CPU-hosted ≤14B model, p95 < agreed latency; baseline resources: KAG sidecar RAM/CPU measured at idle and during indexing.
- Dependencies: BL-14 vector backend, BL-18 ACL; failure: plan JSON invalid → fallback to hybrid. Defensibility: governed plan execution + ACL + tenancy persists even if KAG methods are copied. Decision: **EXPERIMENT**.

**INV-openspg-kag-02 — No evidence of permission, time and tenant semantics**
- Limitation: public docs show login/permissions (v0.6) but no source-ACL or temporal propagation (absence in reading; hypothesis). Root cause: *governance/data model* (hypothesis).
- Alternative: every extracted fact stores evidence chunk ids + `acl_hash` + valid/transaction time (BL-17, BL-37, BL-41), retrieval filters at graph-match and chunk-fetch steps (both layers of mutual index!). Worse when sources have no ACL.
- Options: (1) quick: per-tenant KAG project + per-ACL-group KB (explodes KB count); (2) native: ACL filter in both index directions; (3) long-term: permission-closure precomputation with revocation propagation.
- Selected: 2. POC: 3 principals × 10k chunks; success = 0 leaked facts or chunks incl. through chunk→entity back-links; revocation visible < 1 min. Defensibility: mutual indexing creates a *second leak path* (entity↔chunk) that competitors rarely test — EOIP can own it. Decision: **ADOPT** (as design requirement), P0.

**INV-openspg-kag-03 — Benchmark claims are vendor-only and contamination-prone**
- Limitation: single-source multi-hop numbers on Wikipedia datasets, different LLMs per row (proven from table). Root cause: *maturity/UX of evidence*. Alternative: internal eval harness (CAP-78) on enterprise questions with plain-RAG baselines (§5.3). Option 2 selected; POC: pre-registered comparison against BM25/dense/hybrid/rerank. Decision: **ADOPT** (cheap).

**Seed hypotheses (§10.5)**: "Microsoft GraphRAG costly indexing / summarisation" — KAG's *Lightweight Construction* is vendor evidence that the cost concern is real (89% token reduction claimed; baseline undefined) → hypothesis partially supported, but does not target KAG itself. "Graphiti: LLM-dependent extraction cost" — KAG builder is likewise LLM-per-chunk; deterministic-first alternative applies (validated structurally).

## 10. Deployment, licensing, redistribution, operational viability

| Item | Assessment |
|---|---|
| Deployment | Docker/Compose; openspg-server + `openspg-neo4j` + DB (+ vector); Python toolkit `openspg-kag` 0.8.0 (py>=3.10 per README) |
| Air-gap | Feasible in principle (self-hosted; models configurable per stage, supports OpenAI-compatible endpoints — endpoint list UNVERIFIED). Default model/embedding endpoints in templates should be audited for external calls |
| Local models | KAG-Thinker 7B released; paper results rely on larger models; CPU-only viability unverified |
| Licence | Apache-2.0 for KAG, OpenSPG, KAG-Thinker repo; PyPI metadata empty; **legal-review trigger**: bundled/required Neo4j (GPLv3 Community vs commercial), Elasticsearch if used, model weights, possible Ant patents |
| Redistribution/OEM | Apache-2.0 permits; patent grant clause in Apache-2.0 §3 helps but does not cover third-party dependencies |
| Backend neutrality | Conflicts: KAG assumes OpenSPG as the schema+storage authority; mapping to HugeGraph/Neptune would require an OpenSPG cloudext adapter (feasibility UNVERIFIED) or use as a sidecar producing candidate facts for EOIP's gate |
| One-node first | Heavy: several containers; acceptable for evaluation, not as an embedded component |
| Maintenance | Slow since mid-2025: plan for fork/pin risk |

## 11. Competitive delta against EOIP baseline

| Area | KAG | EOIP | Delta |
|---|---|---|---|
| GraphRAG (BL-16) | Logical-form planner + hybrid fallback; LLM-heavy | Deterministic graph-first; no benchmark | KAG covers multi-hop numeric reasoning EOIP lacks; both lack independent benchmark |
| NL query (BL-11/12) | Plans → executors | Suggest-then-run, optional LLM hook | Adopt plan operators; keep suggestion step |
| Vector/hybrid (BL-14/15) | Index types per KB; external vector stores | Hashing embedder, pure-Python HNSW, RRF | EOIP lacks production vector backend; KAG has richer index types (Outline/Summary/AtomicQuery) |
| Schema/ontology (BL-27..32) | Schema DSL + concept types + KGDSL rules | Ontology gate, SHACL subset, gitops | EOIP ahead on ontology-as-code/diff (BL-32); KAG ahead on integrating schema into LLM extraction + retrieval |
| Provenance (BL-39..41) | Supporting chunk links | Claims + evidence manifests | EOIP ahead |
| ACL/tenancy (BL-17/18/20) | Not documented | Captured, not enforced | Neither; EOIP must lead |
| Temporal (BL-37) | Not documented | Bitemporal | EOIP ahead |
| Ingestion (BL-23/24/26) | Builder chains, resumable tasks | Source events, replay, DLQ, profiling | EOIP ahead on governed mutation path; KAG on LLM extraction convenience |
| Backends (BL-01..06) | Neo4j confirmed; TuGraph etc. | HugeGraph, Neo4j, Neptune… | Different; KAG not backend-neutral |

## 12. Cards

See §8 (strength cards) and §9 (inversion cards).

## 13. Per-capability decisions

| Capability | Decision | Line |
|---|---|---|
| CAP-56 GraphRAG / logical-form reasoning | EXPERIMENT | Sidecar evaluation + native plan/operator prototype |
| CAP-58 NL→query / plan decomposition | BUILD | Typed plan with deterministic operators (BL-08) |
| CAP-32 extraction | REUSE pattern | Schema-constrained extraction feeding EOIP gate as PROPOSED |
| CAP-08/09 schema | REUSE EOIP ontology; REFERENCE KAG DSL | Do not adopt a second schema authority |
| CAP-12/23 concept alignment | BUILD | Ontology-driven expansion with trace |
| CAP-55 hybrid fallback | REUSE EOIP RRF | Add explicit fallback policy |
| CAP-46/47 ACL/tenancy | BUILD | Both graph→chunk and chunk→graph paths |
| CAP-61 local models | EXPERIMENT | KAG-Thinker 7B as optional planner after weights-licence review |
| Whole-platform adoption (OpenSPG as storage authority) | REJECT | Conflicts with backend neutrality and one-node-first |
| CAP-78 evaluation harness | BUILD | Required to validate any claim |

## 14. Concrete tests and acceptance conditions

1. **Sidecar eval**: deploy KAG 0.8.0 on a scratch node with a local ≤14B model (or 72B reference if hardware allows); index a 500-document EOIP-like corpus; measure indexing tokens/time, RAM, disk, answer quality on 150 questions vs BM25/dense/hybrid+rerank/EOIP graph-first. Accept only if gains survive baselines and cost is recorded.
2. **Numeric/temporal subset**: 50 count/sort/threshold questions; require deterministic operator results equal to ground truth.
3. **Leak test**: ACL groups A/B; query as B; verify no entity, relation or chunk from A appears via graph match, chunk back-links or summaries (INV-02).
4. **Egress audit**: run with network blocked; list all outbound attempts (templates, vectorizer, telemetry).
5. **Maintenance check**: re-verify releases/commits before any adoption decision; fork-readiness assessment.
6. **Schema portability**: export an EOIP ontology slice to a KAG `.schema` and back; record semantic loss.

## 15. Risks, trade-offs, open research questions

- Continuity: no release since 2025-06 (16 months); single-company stewardship.
- Weights/dependency licensing (Qwen base, Neo4j, Elasticsearch) unresolved.
- Vendor benchmarks dated 2024 on Wikipedia multi-hop sets; no independent replication found.
- Open: KGDSL expressivity and incremental evaluation; OpenSPG storage adapters beyond Neo4j; incremental update and deletion semantics at document level; how alignment is implemented in code; whether English prompt coverage is first-class; actual compose service list and idle footprint.

---

## Appendix A. Research-dimension coverage

| Dimension | Sections | Summary |
|---|---|---|
| D1 Identity/maturity | 1 | Apache-2.0; v0.8.0 latest (2025-06); slowing activity |
| D2 Problem/workloads | 2 | Professional-domain, multi-hop QA |
| D3 Architecture | 4, 5 | Builder/solver/server/stores |
| D4 Storage/indexing | 5 | Graph + chunk nodes + vectors; engine-specific physical layout NOT PUBLICLY VERIFIED |
| D5 Schema/semantics | 5, 3 | Schema DSL, concept types, KGDSL rules |
| D6 Query pipeline | 5 | Logical forms, planners, executors |
| D7 Reasoning | 5, 9 | KGDSL rules; deduce operator; expressivity unverified |
| D8 Transactions/scale | 5, 7 | Inherited from store; none documented |
| D9 Ingestion/federation | 5, 3 | Builder chains; mapping chain; no CDC |
| D10 Identity/evidence | 5, 9 | Alignment/merge synonyms; chunk evidence; no ACL |
| D11 Time/evolution | 3, 9 | Not documented |
| D12 Algorithms/ML | N/A | Not core (GDS used by Neo4j side; unclear) |
| D13 Retrieval/agents | 5, 8 | Core strength; MCP |
| D14 NL query | 5 | Plan decomposition; not text-to-Cypher |
| D15 Governance | 3, 9 | Basic login; schema management UI |
| D16 Human experience | 3 | Web UI with reasoning steps |
| D17 Developer experience | 3, 9 | Python toolkit; heavy extension model |
| D18 Security | 9 | MCP, ACL gaps (hypothesis) |
| D19 Multi-tenancy | 9 | Project-level only |
| D20 Economics | 7 | Token claims vendor-only; 72B dependency |
| D21 Commercial | 10 | Apache-2.0; Ant ecosystem |
| D22 Interop/lock-in | 10, 14 | OpenSPG as authority; export unverified |
| D23 IP/prior art | 1, 10 | Possible Ant patents NOT PUBLICLY VERIFIED |
| D24 Research quality | 7 | Vendor paper only |

## Appendix B. Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-56 | native | [06][12] | BL-16 Implemented (deterministic) | EXPERIMENT | P1 |
| CAP-58 | partial (plan-based) | [06][12] | BL-11/12 | BUILD | P1 |
| CAP-32 | native | [11] | BL-26/27 Partial | REUSE pattern | P2 |
| CAP-08 | native (schema DSL) | [10] | BL-28 Implemented | REFERENCE | P3 |
| CAP-12 | partial (concept alignment) | [06] | BL-30 Partial | BUILD | P2 |
| CAP-24 | partial (step trace) | [04] | BL-48 xai | REUSE EOIP | P3 |
| CAP-38 | partial (chunk links) | [06] | BL-41 Implemented | REUSE EOIP | P3 |
| CAP-53 | plugin (vector stores) | [06] | BL-14 Partial | INTEGRATE | P1 |
| CAP-55 | partial (hybrid fallback) | [06] | BL-15 Implemented | REUSE | P3 |
| CAP-59 | native (MCP v0.7/0.8) | [04] | BL-47 Implemented | REFERENCE | P3 |
| CAP-61 | partial (KAG-Thinker 7B) | [07] | BL-57 Planned | EXPERIMENT | P2 |
| CAP-46 | absent/unknown | — | BL-18 Absent | BUILD | P0 |
| CAP-47 | unknown (project-level) | [04] | BL-20 Partial | BUILD | P0 |
| CAP-78 | partial (open_benchmark dir) | [04] | none | BUILD | P1 |
| CAP-77 | n/a | [01] | BL-22 | flag legal review | P2 |

## Appendix C. Evidence records

All accessed 2026-10-18. Confidence 0..1. Pages read via summarising fetch; no local clone or run.

| CLAIM-ID | product/version/date | claim | class | source | pub/access | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-openspg-kag-01 | KAG 0.8.0 | Apache-2.0; builder + solver released, kag-model to be open-sourced gradually; ~9.1k stars, 1,261 commits | Officially documented | github.com/OpenSPG/KAG (README) | 2026-10-18 | 0.85 | PyPI licence field empty |
| CLAIM-openspg-kag-02 | OpenSPG engine | Apache-2.0; modules builder, cloudext, reasoner, server; SPG-Schema/Builder/Reasoner (KGDSL); ~2.3k stars; last commit 2025-06-29 | Officially documented | github.com/OpenSPG/openspg (README, commits) | 2026-10-18 | 0.8 | — |
| CLAIM-openspg-kag-03 | KAG-Thinker | 7B models on Qwen2.5-7B-Instruct, repo Apache-2.0, papers 2506.17728 and 2511.07943; 92 stars | Officially documented | github.com/OpenSPG/KAG-Thinker | 2026-10-18 | 0.75 | weight licence not confirmed |
| CLAIM-openspg-kag-04 | KAG 0.5–0.8 | Release dates and contents; Neo4j fixes; Qwen2.5-72B/bge-m3 benchmark models; 7B construction + 72B Q&A in lightweight mode; custom components via replacing server-image package | Officially documented | github.com/OpenSPG/KAG/releases; github.com/OpenSPG/openspg/releases | 2025-06-29 / 2026-10-18 | 0.8 | page dates vs notes dates differ by 1–2 days |
| CLAIM-openspg-kag-05 | KAG master | Commits 2025-06-30..2025-08-06; single commit 2026-01-28 (`fdab15b`); no release after 0.8.0 | Observed (commit page) | github.com/OpenSPG/KAG/commits/master | 2026-10-18 | 0.7 (page may be cached) | — |
| CLAIM-openspg-kag-06 | paper v3 | LLMFriSPG layers, mutual indexing, logical-form operators and loop, hybrid fallback, six alignment relations, +15.7% top-5 recall | Peer-reviewed/preprint (vendor authors) | arXiv:2409.13731 (arxiv.org/html/2409.13731) | 2024-09-26 / 2026-10-18 | 0.75 (only first ~100k chars read) | preprint, not independent |
| CLAIM-openspg-kag-07 | paper v3 | Table: KAG-LFSH F1 76.2 / 76.2 / 48.7 (Hotpot/2Wiki/MuSiQue, DeepSeek-V2); abstract +19.6% / +33.5% | Vendor claim | same | same | 0.7 as quoted; interpretation not independently reproduced | no independent replication found |
| CLAIM-openspg-kag-08 | KAG 0.7 README | Lightweight Construction cuts construction token cost 89%; no baseline stated; KAG-Thinker adapted in 0.8 | Vendor claim | github.com/OpenSPG/KAG README | 2025-04-17 / 2026-10-18 | 0.5 | — |
| CLAIM-openspg-kag-09 | PyPI `openspg-kag` 0.8.0 | Uploaded 2025-06-30; licence metadata null | Officially documented | pypi.org/pypi/openspg-kag/json | 2026-10-18 | 0.85 | — |
| CLAIM-openspg-kag-10 | KAG 0.8.0 example | Schema DSL fragment: EntityType with `content: Text`, `index: TextAndVector`, relations, MultiValue | Observed in source | raw `kag/examples/csqa/schema/CsQa.schema` (v0.8.0) | 2026-10-18 | 0.7 | — |
| CLAIM-openspg-kag-11 | KAG 0.8.0 | `DefaultStructuredBuilderChain` and `DefaultUnstructuredBuilderChain` component order | Observed in source | `kag/builder/default_chain.py` (v0.8.0) | 2026-10-18 | 0.75 | — |
| CLAIM-openspg-kag-12 | KAG 0.8.0 | Directory structure: solver/{planner,executor,generator,pipeline,reporter,prompt}; planners and executors listed | Observed in source | github.com/OpenSPG/KAG/tree/v0.8.0/kag/solver (+ /planner, /executor) | 2026-10-18 | 0.8 (listings may be incomplete) | — |

## Appendix D. Assumptions

- KAG-level internals were read from release notes, README, paper HTML (first ~100k of ~145k chars) and directory listings; no local clone, no run, no byte-level code read of solver logic; reconstruction in §5 mixes verified directory/class names with the paper's algorithm (marked) and hypotheses (marked).
- OpenSPG server dependencies beyond Neo4j (relational DB, vector store, object store) are not verified from official files; community compose guide treated as non-evidence.
- Verification date follows the brief (2026-10-18).
- Absence of ACL/temporal semantics is "not documented in sources read", not proof of absence.
- Chinese-first usability inferred from a single example schema.
