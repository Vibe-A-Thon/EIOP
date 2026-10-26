# C08 — Neo4j GraphRAG package (`neo4j-graphrag`, Python)

| Field | Value |
|---|---|
| Registry ID | T-C08-neo4j-graphrag |
| Tier | A — first-party GraphRAG/KG-builder library of a required EOIP backend (Neo4j); reuse/pattern candidate for CAP-55, CAP-56, CAP-58, CAP-32 |
| Versions examined | `neo4j-graphrag` 1.22.0 (PyPI 2026-10-01; wheel unpacked and read); 1.21.0 (2026-09-23), 1.19.0 (2026-08-26; 1.20.0 not on PyPI), 1.18.0 (2026-06-24), 1.17.0 (2026-05-27); CHANGELOG at `main` |
| Verified on | 2026-10-26 |
| Worker | V07 (batch for W19 scope) |

## 1. Identity, current status, tier, and sources

- **What it is.** The official Neo4j (Neo4j Sweden AB) Python package "neo4j-graphrag": retrievers, a `GraphRAG` answer class, and a knowledge-graph builder pipeline, all targeting Neo4j [CLAIM-n4gr-01][CLAIM-n4gr-02]. Repository `neo4j/neo4j-graphrag-python`. It supersedes the deprecated **`neo4j-genai`** package (docs: "no longer maintained") [CLAIM-n4gr-03].
- **Name traps.** (a) Not the Neo4j *LLM Graph Builder* web app (a separate Neo4j Labs product, covered by C05) though they share ideas; (b) not Microsoft GraphRAG (`C08-microsoft-graphrag.md`); (c) not `neo4j-graphrag` forks in LlamaIndex/LangChain (`Neo4jPropertyGraphStore`, `Neo4jVector`) which are separate codebases.
- **Licence.** Apache-2.0, with parts under the Python Software Foundation License v2 (marked in code); `NOTICE.txt` copyright Neo4j Sweden AB [CLAIM-n4gr-01]. Permissive. The **Neo4j server it needs** is not: Community Edition is GPLv3 and several features it assumes (multi-database, RBAC) are Enterprise [`C01-neo4j.md` CLAIM-neo4j-04, -05].
- **Status.** Active: 11 PyPI releases between 2026-02-25 and 2026-10-01, roughly every 2-8 weeks; "long-term support and maintenance directly from Neo4j" is a README statement, not a formal support policy; docs name GitHub issues and Enterprise customer support as channels [CLAIM-n4gr-02][CLAIM-n4gr-03]. Maturity: production for retrievers; the KG builder is still documented as "experimental. API changes and bug fixes are expected" although components left the `experimental` namespace in 1.19.0 (old imports removed in 2.0) [CLAIM-n4gr-04][CLAIM-n4gr-09].
- Sources used (11): PyPI JSON and project page; GitHub README; docs landing and KG-builder user guide; CHANGELOG; wheel source (retrievers, `neo4j_queries.py`, `components/*`, `llm/*`, `embeddings/*`); `C01-neo4j.md`. Cross-references: `C01-neo4j.md`, `C08-microsoft-graphrag.md`, `C08-graphiti-zep.md`, `C08-cognee.md`.

## 2. Primary problem, target workloads, concrete example workflows

Problem: give an LLM grounded context from a Neo4j graph (and optional external vector stores), and build that graph from documents with a schema-guided LLM pipeline. Workloads: document Q&A with graph expansion, NL-to-Cypher analytics, PDF/text -> graph ingestion, agentic tool selection over several retrievers.

Workflows (verified in source): (1) **VectorCypher**: embed question -> `db.index.vector.queryNodes` (or Cypher-25 `SEARCH` clause on Neo4j 2026+) -> user-supplied `retrieval_query` traverses from each hit (e.g. chunk -> entities -> related entities) -> records formatted into the prompt [CLAIM-n4gr-05][CLAIM-n4gr-06]. (2) **Text2Cypher**: schema + examples -> LLM -> Cypher -> `EXPLAIN` -> reject unless read-only -> run on a READ route [CLAIM-n4gr-07]. (3) **SimpleKGPipeline**: load PDF/text -> split -> (optional) LLM schema extraction -> per-chunk LLM entity/relation extraction -> prune against schema -> write with APOC -> resolve duplicates [CLAIM-n4gr-08][CLAIM-n4gr-09][CLAIM-n4gr-10].

## 3. Feature inventory

| Feature | Status | Surface | Evidence |
|---|---|---|---|
| `VectorRetriever` / `VectorCypherRetriever` (vector + custom traversal) | Present | Python | CLAIM-05, -06 |
| `HybridRetriever` / `HybridCypherRetriever` (vector index + full-text; rankers NAIVE=max, LINEAR with alpha) | Present | Python | CLAIM-06 |
| `Text2CypherRetriever` with EXPLAIN read-only guard, few-shot examples, custom prompt | Present | Python | CLAIM-07 |
| `ToolsRetriever` (LLM picks among retrievers via tool calling) | Present | Python | CLAIM-05 |
| External-store retrievers: Pinecone, Qdrant, Weaviate (hit ids joined to Neo4j nodes via an id property) | Present (extras) | Python | CLAIM-05 |
| Metadata pre-filters (eq, neq, lt, gt, in, nin, like...) compiled to Cypher | Present | Python | CLAIM-05 |
| `GraphRAG` class (retriever + LLM + prompt, message history, `return_context`) | Present | Python | CLAIM-05 |
| KG builder: loaders (PDF/text), splitters (fixed size, LangChain, LlamaIndex), LLM extractor, pruner, writer, resolvers | Present | Python | CLAIM-08..10 |
| Schema modes: explicit, `EXTRACTED` (LLM derives schema once), `FREE` | Present | Python | CLAIM-09 |
| Lexical graph (Document -> Chunk -> NEXT_CHUNK; entity -FROM_CHUNK-> chunk) | Present (default on) | Python | CLAIM-08 |
| Entity resolution: exact (label+name), spaCy semantic, RapidFuzz fuzzy | Present (exact on by default) | Python | CLAIM-09 |
| Parquet writer (export instead of writing to Neo4j) | Present | Python | CLAIM-08 |
| LLMs: OpenAI/Azure, Anthropic, Bedrock, Cohere, Google (Vertex, GenAI), Mistral, **Ollama**, LiteLLM; embedders incl. **Ollama**, sentence-transformers | Present | Python | CLAIM-12 |
| Structured-output extraction | Partial (OpenAI, Vertex, Anthropic; error otherwise) | Python | CLAIM-09 |
| Non-Neo4j graph backends | **Absent** | – | CLAIM-05 |
| ACL / tenant / principal filtering | **Absent** | – | CLAIM-11 |
| Temporal validity, bitemporal, memory expiry | Absent | – | source |
| Review gate / proposed-vs-approved writes | Absent (writer upserts) | – | CLAIM-08 |
| UI / CLI | Absent (library only) | – | CLAIM-02 |

## 4. Architecture diagram

```
 documents ─► DataLoader (PDF/text) ─► TextSplitter ─► [SchemaFromText (LLM, once)] ─► LLMEntityRelationExtractor (1 LLM call / chunk, concurrency 5)
                                                                                         │ JSON repair / structured output
                                                                                         ▼
                                              GraphPruning (types, patterns, required props, constraints)  ──► pruned items + stats
                                                                                         ▼
                              Neo4jWriter (batched APOC MERGE; __KGBuilder__ tmp ids) ──► Neo4j  (labels, vector index, full-text index)
                                                                                         ▼
                              EntityResolver (exact | spaCy | fuzzy)  — merges nodes in the DB
 question ─► Retriever (Vector | VectorCypher | Hybrid | HybridCypher | Text2Cypher | Tools | Pinecone/Qdrant/Weaviate→Neo4j join)
          ─► records ─► result_formatter ─► prompt template ─► LLM (any provider incl. Ollama) ─► answer (+ optional retriever context)
 Control plane: Python Pipeline DAG (orchestrator, notification events, config-driven runner); no server, no UI, no auth layer of its own
```

## 5. Under-the-hood reconstruction (wheel 1.22.0; paths under `neo4j_graphrag/`)

**Data model written.** Nodes get labels from the schema plus `__Entity__` (and transient `__KGBuilder__` + `__tmp_internal_id`), `Chunk`/`Document` nodes for the lexical graph, relationships `FROM_CHUNK`, `NEXT_CHUNK`, `FROM_DOCUMENT` (names configurable via `LexicalGraphConfig`); optional embeddings on chunks and entities. Entity properties come from the LLM within the schema; `document_metadata` is stored on the Document node [CLAIM-n4gr-08][CLAIM-n4gr-09]. Provenance granularity = **chunk** (no character spans, no model/version, no confidence).

**Indexes and query pipeline.** Retrievers do not own storage; they require a pre-created Neo4j vector index (and full-text index for hybrid). Query templates in `neo4j_queries.py`:
- Vector: `CALL db.index.vector.queryNodes($index,$k*ratio,$vec) YIELD node,score`; on Neo4j 2026+ a `CYPHER 25 ... SEARCH node IN (VECTOR INDEX ... FOR $vec WHERE <filters> LIMIT k)` form is used and falls back to the procedure on failure (1.19.0), which enables in-index filtering [CLAIM-n4gr-03][CLAIM-n4gr-04].
- Hybrid: vector and `db.index.fulltext.queryNodes` run in a `CALL { ... UNION ... }`; scores normalised per branch; ranker NAIVE = max score per node, LINEAR = `alpha*vec + (1-alpha)*fulltext` [CLAIM-n4gr-06]. No reciprocal-rank fusion.
- Cypher variants append the user `retrieval_query` after the index hit (`node`, `score` in scope) — the graph expansion is entirely author-written Cypher; the library does no automatic multi-hop planning.
- `effective_search_ratio` over-fetches candidates before post-filtering to offset ANN recall loss when filters are applied outside the index (pre-2026 path).

**Text2Cypher.** Schema text is obtained via `apoc.meta.data` (optionally enhanced), injected with examples into a prompt; the answer is parsed by `extract_cypher`; then `EXPLAIN <query>` is executed and the summary's `query_type` must equal read-only or `Text2CypherRetrievalError` is raised; execution uses `RoutingControl.READ` [CLAIM-n4gr-07]. Observed: this is an engine-side guard, stronger than regex deny-lists; it does not constrain *what* is read (no label/property allow-list, no row/hop limits, no tenant predicate), so data exfiltration across tenants is possible if the DB user can read it (hypothesis, follows from absence of ACL code [CLAIM-n4gr-11]).

**KG builder internals.**
```
for chunk in chunks (asyncio, max_concurrency=5):
    prompt = ERExtractionTemplate(text=chunk.text, schema=schema.model_dump(), examples)
    out = llm.ainvoke(prompt)                       # V1: prompt-based JSON; V2: response_format=Neo4jGraph (OpenAI, Vertex, Anthropic only)
    json = json_repair.repair_json(out)             # tolerate malformed JSON from small models
    graph = Neo4jGraph.model_validate(json)         # on error: skip chunk (or raise, per on_error)
graph = combine(chunk_graphs); prune(graph, schema) # drop unknown labels/rel patterns/missing required props; typed property coercion
Neo4jWriter: UNWIND batch(1000) -> apoc.merge/ create labels + apoc.merge.relationship ; index on __KGBuilder__.__tmp_internal_id ; cleanup tmp ids
resolver (default exact label+name over all __Entity__): merge duplicates IN the database
```
[CLAIM-n4gr-08][CLAIM-n4gr-10]. Schema = `GraphSchema{node_types[label, properties(type, required), additional_*], relationship_types, patterns, constraints(KEY/UNIQUENESS/EXISTENCE)}`; 1.18.0 tightened validation (duplicate relationship labels rejected; `KEY`+`EXISTENCE` on one property rejected). Schema extraction is itself an LLM call (`graph_schema_extraction.py`) [CLAIM-n4gr-04][CLAIM-n4gr-10]. Resolvers "replace the nodes created by the KG writer" i.e. merges are destructive with only `ResolutionStats` counts returned, no merge ledger [CLAIM-n4gr-09].

**Concurrency/transactions.** Driver-level transactions per batch; idempotence via MERGE on `name`-like properties only if the schema defines them; no cross-chunk transaction, so partial runs leave partial graphs (default `on_error` skips failing chunks and still writes the rest). Caching: none. Versioning: none (no revision nodes). Security: whatever the Neo4j user can do; the library sets only the driver user-agent. Partitioning/consistency: delegated to Neo4j (CE single instance; vector index not visible within the writing transaction per `C01-neo4j.md` CLAIM-neo4j-09, which also affects write-then-read pipelines).

## 6. Functional and non-functional requirements inferred

| ID | Requirement | Basis |
|---|---|---|
| FR-G1 | Vector retrieval followed by author-defined parametrised graph expansion (VectorCypher pattern) | CLAIM-05, -06 |
| FR-G2 | Hybrid fusion with a tunable weight | CLAIM-06 |
| FR-G3 | Generated queries pass an engine-level read-only check before execution | CLAIM-07 |
| FR-G4 | Extraction guided by an explicit, validated schema; out-of-schema items are pruned and counted | CLAIM-10 |
| FR-G5 | Lexical graph linking every extracted entity to its source chunk | CLAIM-08 |
| FR-G6 | Pluggable LLM/embedder including local servers | CLAIM-12 |
| NFR-G1 | Tolerate malformed JSON from weak models (repair) and isolate chunk failures | CLAIM-08 |
| NFR-G2 | Adaptation to engine version (5.18+, 5.23+, 2026+ SEARCH) | CLAIM-03, -04 |

## 7. Performance and resource model

No benchmark published by Neo4j in the sources examined; none quoted. Derived model (hypothesis, assumptions stated): KG builder cost = 1 schema call (if `EXTRACTED`) + C chunk-extraction calls where C = ceil(chars/chunk_size); throughput bounded by LLM concurrency (default 5) and LLM latency; writer throughput bounded by APOC MERGE batches of 1000 and by index maintenance; resolvers are O(n^2) pairwise for the similarity resolvers within each label (code uses pair comparison and set consolidation) -> restrict with `filter_query`. Retrieval latency = 1 embedding + 1 index query + expansion Cypher + 1 LLM call (answer); Text2Cypher adds 1 LLM call + 1 `EXPLAIN`. Dependencies are heavy: core pulls numpy, scipy, pypdf, fsspec; `nlp` extra pins spaCy 3.8.16 (not on Python 3.14) [CLAIM-n4gr-01]. Failure modes: LLM returns invalid JSON (skipped chunk -> silently incomplete graph), structured output unsupported for other providers (ValueError), Qdrant/Pinecone id join mismatches, SEARCH clause fallback on older servers, resolver merges the wrong entities (name collision).

## 8. Strengths and use-case-specific advantages

- Compact, readable implementation of the three patterns most teams need (vector, hybrid, vector+traversal) with engine-version adaptation.
- **Read-only guard via `EXPLAIN`** for LLM-generated Cypher — the right primitive (uses the planner, not string matching).
- Schema-guided extraction with pruning, constraint types, typed properties, and `EXTRACTED`/`FREE` modes; pruning stats are surfaced.
- Lexical graph default gives chunk-level provenance for free.
- Runs with local models (Ollama LLM and embedder; sentence-transformers) and with JSON repair for small models.
- First-party, Apache-2.0, driver-level `user-agent` identification, Parquet export for offline loading.

## 9. Limitations with root causes

| Class | Limitation | Type | Evidence |
|---|---|---|---|
| Coupling | Neo4j-only (vector index procedures, APOC, Cypher); external vector stores still join into Neo4j | Design | CLAIM-05 |
| Algorithmic | Graph expansion is hand-written Cypher; no entity-linking from question to graph; no community summaries or global search | Design | CLAIM-05, -06 |
| Algorithmic | Hybrid ranking = max or linear of per-branch normalised scores, no RRF; tuning alpha is per-corpus | Design | CLAIM-06 |
| Quality | Per-chunk extraction without cross-chunk context; coreference and relation direction errors propagate; resolution by exact `name` by default | Design/hypothesis | CLAIM-08, -09 |
| Governance | Writer upserts straight into the graph; resolvers merge destructively; no proposal/approval stage | Verified | CLAIM-08, -09 |
| Security | No tenant/principal/ACL handling anywhere in the package | Verified (grep) | CLAIM-11 |
| Security | Text2Cypher read-only but unconstrained in scope; prompt-injection in documents can steer extraction/answers (hypothesis) | Verified + hypothesis | CLAIM-07 |
| Operational | Requires APOC core plugin and Neo4j >=5.18.1; CE is GPLv3 and single-database | Licensing/operational | CLAIM-03, `C01-neo4j.md` |
| Friction | KG builder documented as experimental; API moved (1.19.0), breaking changes in minor releases; docs vs code mismatch on structured-output provider list (docs: OpenAI, Vertex, Anthropic; extractor docstring: OpenAI, Vertex) | Verified | CLAIM-04, -09 |
| Friction | `on_error` defaults differ between docs (skip chunk) and extractor docstring (raise) | Verified inconsistency | CLAIM-09, source |

## 10. Deployment, licensing, redistribution, operational viability

- **Licence class: permissive (Apache-2.0 + PSF-2.0 snippets).** Redistributable in a white-label product. **Legal-review trigger:** the dependency is only useful against Neo4j; bundling Neo4j CE (GPLv3) in an appliance has GPL distribution duties, whereas customer-supplied Neo4j accessed over the network is the lower-risk pattern (see `C01-neo4j.md` section 10). The PSF-licensed portions need attribution handling.
- **Air-gap: yes** (pure library; Ollama + sentence-transformers + local Neo4j). `spacy` resolver may try to download models (`_load_or_download_spacy_model`) — must be pre-staged offline. No telemetry code found except the driver user-agent string.
- **One-node:** yes (library in the API/worker process plus a Neo4j instance).
- **Backend neutrality:** fails as a runtime layer (Neo4j-only). Fine as an **optional Neo4j-specific retrieval module** in the backend adapter.

## 11. Competitive delta against EOIP verified baseline

| Area | neo4j-graphrag | EOIP baseline | Delta |
|---|---|---|---|
| Retrieval | vector, hybrid (max/linear), VectorCypher | graph-first evidence retrieval (BL-16), BM25+hash vectors (BL-14), RRF (BL-15) | EOIP has RRF and backend-neutral retrieval but no real embedding index; library offers server-side ANN + filters on Neo4j |
| NL->query | Text2Cypher, EXPLAIN guard | `QueryPlan` + named bounded templates (BL-08), suggestion engine (BL-11/12), optional LLM hook | EOIP safer by construction (no generated query), less expressive; adopt EXPLAIN guard for any future Cypher generation |
| KG builder | schema-guided LLM extraction, pruning, resolvers | JSON profiler (BL-26), CML mapping (BL-33), validation gate (BL-28), ontology proposal (BL-27); no unstructured extraction pipeline (see C05) | Complementary: unstructured -> graph is where EOIP is thinnest (CAP-32) |
| Provenance | chunk-level lexical graph | evidence manifests/lineage (BL-41), SourceEvent (BL-23) | EOIP ahead on governance; lacks chunk-level text provenance |
| Permissions | none | BL-17 captured, BL-18 Absent | Neither enforces; library offers no hook |
| Writes | direct MERGE | governed mutation path, connectors never write (BL-23, BL-28) | Library writer must not be used as-is |
| Entity resolution | exact/spaCy/fuzzy, destructive | deterministic person identity + candidate queue (BL-34/35) | EOIP has reversible review queue; library has similarity matchers worth reusing as candidate generators |

## 12. Strength-adoption cards and inversion cards

| ID | Competitor | Strength | Evidence | Value to EOIP | Verdict | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-n4gr-01 | neo4j-graphrag | VectorCypher: vector hit then parametrised traversal | CLAIM-05, -06 | Vector-first GraphRAG that preserves graph context | match | `GraphStore` capability `neighbourhood(ids, template)`; Neo4j adapter may push down to Cypher, others emulate in Python; ACL filter applied to both hit set and expansion | Same QueryPlan returns equal result sets on Neo4j and HugeGraph (BL-07 conformance) |
| STR-n4gr-02 | neo4j-graphrag | Planner-based read-only guard for generated queries | CLAIM-07 | Safe NL->query | integrate (pattern) | For any generated Cypher/Gremlin/SPARQL: validate with engine `EXPLAIN`/profile equivalent plus label/property allow-list, hop and row limits, tenant predicate injection | 500 adversarial prompts incl. `CALL`/`MERGE`/`LOAD CSV`/APOC: 0 mutations, 0 cross-tenant reads |
| STR-n4gr-03 | neo4j-graphrag | Schema-guided extraction + pruning with counted rejections | CLAIM-09, -10 | Controlled unstructured ingestion (CAP-32/CAP-08) | match | Prompt from EOIP ontology manifest; prune/validate in validation gate (BL-28); rejects counted as DLQ-like events | Out-of-ontology items: 100% rejected and logged; precision/recall on gold set reported |
| STR-n4gr-04 | neo4j-graphrag | Lexical graph for chunk provenance | CLAIM-08 | Every extracted fact traceable to a chunk | exceed | Evidence record with `source_event_id`, chunk id, char span, extractor/model version, confidence; ACL inherited from source | Every extracted edge has span-level evidence; answer citations resolve to spans |
| STR-n4gr-05 | neo4j-graphrag | JSON repair + chunk-level failure isolation | CLAIM-08 | Local small models usable | match | Retry ladder: repair -> reprompt -> larger local model -> DLQ | JSON-parse failure rate on 7-14B models measured; failures land in DLQ, not silently dropped |

**INV-n4gr-01 — Writer and resolvers mutate the graph directly and destructively (proven, governance).** Violates EOIP constraint "connectors never mutate the authoritative graph". Options: (a) run the library with `Parquet` writer and import through the governed pipeline; (b) reuse extractor + pruner components, replace writer with a SourceEvent/assertion emitter, resolvers as candidate generators into `identity/candidates.py`; (c) long-term: extraction as a PROPOSED-assertion producer with evidence and calibrated confidence (BL-40). Selected (b). POC: 50 documents, 3 local models; metric = % extractions admitted without review that are wrong (target < 2%) and 100% reversibility of merges. Worse when: throw-away demo graphs. **ADOPT (pattern + selective reuse).**

**INV-n4gr-02 — No tenant/ACL anywhere (proven, governance).** The vector hit set, full-text hits, Text2Cypher and the expansion Cypher all ignore permissions. Alternative: ACL as an index-time property (e.g. `acl_hash`) plus query-time principal filter inside the index (`SEARCH ... WHERE` on 2026+; post-filter with over-fetch on older), and tenant predicate injection into generated queries. Cost baseline: filter selectivity vs recall loss at `effective_search_ratio`. POC: 10 tenants, 1M chunks, recall@10 vs unfiltered and 0 leaks. Defensibility: ACL-aware GraphRAG across backends is EOIP's core differentiator (BL-18, J5). **ADOPT.**

**INV-n4gr-03 — Neo4j lock-in (proven, coupling).** Alternative: capability-based retrieval interface with Neo4j push-down as an optimisation (STR-01). Worse when: Neo4j is the only backend and performance dominates. **ADOPT** (design constraint).

**INV-n4gr-04 — Extraction quality is unmeasured and contexts are per-chunk (hypothesis).** Mirrors the "GraphRAG is not automatically superior" trap (Master Prompt §5.3). Alternative: benchmark against BM25/dense/hybrid/reranked baselines before enabling graph expansion. **EXPERIMENT.**

**Seed §10.5 "Neo4j: weak formal semantics; schema-optional models decay" — PARTIALLY VALIDATED.** The package adds client-side schema enforcement (pruning, constraint types) but only inside its own pipeline; the database itself is unchanged and other writers bypass it. EOIP's mutation-gateway enforcement is backend-portable and covers all writers. Decision: **EXPERIMENT** (reuse the `GraphSchema` shape as an interchange format candidate).

**INV-SELF-n4gr-01 (EOIP weakness).** EOIP lacks an unstructured -> graph extraction pipeline with schema-guided prompts and chunk-level evidence; BL-14 has no true embedding index. Fix: STR-03/-04 plus C10 vector decision. **ADOPT.**

## 13. Per-capability decisions

| Capability | Decision | Reason |
|---|---|---|
| CAP-53/55 vector + hybrid retrieval on Neo4j | INTEGRATE as optional Neo4j retriever module (Apache-2.0), behind `GraphStore` capability flags; emulated elsewhere | STR-01 |
| CAP-56 VectorCypher traversal pattern | REUSE pattern (BUILD backend-neutral) | STR-01 |
| CAP-58 NL->Cypher | REUSE EXPLAIN-guard pattern; DEFER generated Cypher in prod (keep QueryPlan templates) | STR-02 |
| CAP-32 unstructured extraction | EXPERIMENT with extractor + pruner components (library reuse) feeding governed pipeline | STR-03, INV-01 |
| CAP-31 entity resolution | REUSE similarity matchers as candidate generators only; REJECT destructive resolvers | INV-01 |
| CAP-38 chunk provenance | BUILD richer span-level evidence | STR-04 |
| CAP-46/47 ACL/tenant in retrieval | BUILD | INV-02 |
| Whole package as mandatory dependency | REJECT (Neo4j-only) | INV-03 |

## 14. Concrete tests, POC, acceptance conditions (all PROPOSED; none run)

1. **Equivalence:** same 100 questions through VectorCypher on Neo4j 5.x and 2026.x (SEARCH path) and EOIP emulation on HugeGraph; compare answers and recall@k; record SEARCH-fallback frequency.
2. **Read-only guard red team:** 500 adversarial prompts against Text2Cypher with a read-write DB user; pass = 0 writes; separately measure unauthorised reads without tenant predicate (expected failures, to size INV-02).
3. **Extraction on local models:** SimpleKGPipeline with Ollama 7B/14B/32B on 200 IT-domain documents (tickets, runbooks): JSON failure rate, schema-conformance rate, entity/relation P/R vs gold, tokens and wall-clock per 1k chunks; compare `EXTRACTED` vs explicit schema.
4. **Resolver safety:** inject 200 known homonyms; count wrong merges for exact/spaCy/fuzzy; require reversible audit in the EOIP wrapper.
5. **GraphRAG vs baselines:** BM25, dense, hybrid, reranked vs VectorCypher on multi-hop questions from the IT corpus (Master Prompt §5.3); report where graph expansion helps.
6. **Air-gap:** run builder + retriever with no network (spaCy model pre-staged); pass = no outbound connections.

## 15. Risks, trade-offs, open research questions

Risks: API churn (experimental namespace removal in 2.0; minor-release breakage); silent incompleteness from skipped chunks; destructive resolution; ACL absence; Neo4j server licensing. Open: Does the SEARCH-clause in-index filtering behave correctly for ACL-style multi-valued filters (arrays)? Throughput of APOC MERGE writer on CE single instance at 10M entities (not measured, no source). Does the 1.22 "connected graph" prompt change improve or distort extraction (unmeasured)? Is there an official support SLA beyond Enterprise customer support (NOT PUBLICLY VERIFIED)?

---

## Appendix A — Research-dimension coverage

| Dimension | Sections | Summary / N/A reason |
|---|---|---|
| D1 Identity and maturity | 1 | official, Apache-2.0, active, KG builder experimental |
| D2 Problem/workloads | 2 | doc Q&A, NL2Cypher, KG build |
| D3 Architecture | 4 | library DAG, no services |
| D4 Storage/indexing | 5 | delegated to Neo4j vector/fulltext indexes |
| D5 Schema/semantics | 5, 12 | GraphSchema with constraints; client-side |
| D6 Query pipeline | 5 | procedure vs SEARCH clause; hybrid union |
| D7 Reasoning | N/A | none |
| D8 Transactions/scale | 5, 7 | batch MERGE; delegated |
| D9 Ingestion/federation | 5 | loaders, Parquet; no CDC |
| D10 Identity/evidence | 5, 9 | resolvers; chunk provenance |
| D11 Time/evolution | 9 | absent |
| D12 Graph algorithms/ML | N/A | none (GDS separate; see C01-neo4j) |
| D13 Retrieval/agent integration | 2, 5 | retrievers, ToolsRetriever, GraphRAG |
| D14 NL query | 5, 8 | Text2Cypher EXPLAIN guard |
| D15 Governance/authoring | 9, 12 | none |
| D16 Human experience | 3 | none (library) |
| D17 Developer experience | 3, 9 | typed pydantic models, extras; churn |
| D18 Trust/security | 5, 9 | read-only guard, no ACL, injection |
| D19 Multi-tenancy/white-label | 9, 12 | absent |
| D20 Empirical economics | 7 | model only; no vendor numbers |
| D21 Commercial/licensing | 1, 10 | Apache-2.0 library, server licence split |
| D22 Interop/lock-in | 9, 10 | Neo4j-only; Parquet export |
| D23 IP/prior art | 10 | none found; no patent search |
| D24 Research quality | 7 | source-level; no benchmarks |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-53 vector search | native on Neo4j + 3 external stores | CLAIM-05 | BL-14 Partial | INTEGRATE (optional) | P2 |
| CAP-55 hybrid fusion | native (max/linear) | CLAIM-06 | BL-15 Implemented (RRF) | REUSE pattern | P3 |
| CAP-56 GraphRAG | partial (VectorCypher; no global/community) | CLAIM-05 | BL-16 Implemented | REUSE pattern | P2 |
| CAP-58 NL->query | native (Text2Cypher) | CLAIM-07 | BL-12 Partial | DEFER; adopt guard | P2 |
| CAP-32 unstructured extraction | native (LLM, schema-guided) | CLAIM-08, -10 | Absent (see C05) | EXPERIMENT | P1 |
| CAP-08 schema enforcement | partial (client-side pruning) | CLAIM-10 | BL-28 Implemented | REUSE shape | P2 |
| CAP-31 entity resolution | partial (exact/fuzzy/spaCy, destructive) | CLAIM-09 | BL-34/35 | REUSE as candidates | P2 |
| CAP-38 provenance | partial (chunk-level) | CLAIM-08 | BL-41 | BUILD span-level | P1 |
| CAP-46 ACL in retrieval | absent | CLAIM-11 | BL-18 Absent | BUILD | P0 |
| CAP-47 tenant isolation | absent | CLAIM-11 | BL-20 Partial | BUILD | P0 |
| CAP-49 query-injection defence | partial (read-only EXPLAIN guard) | CLAIM-07 | BL-08 | REUSE pattern | P1 |
| CAP-61 local models | native (Ollama, ST) | CLAIM-12 | BL-45 | INTEGRATE | P2 |
| CAP-14 Cypher | native | CLAIM-05 | BL-03 | REUSE (Neo4j adapter) | P3 |

## Appendix C — Evidence records

| CLAIM-ID | Product/version/date | Exact claim | Class | Source + URL | Pub/access | Confidence + rationale | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-n4gr-01 | 1.22.0, 2026-10-01 | Apache-2.0 (LICENSE.txt: parts under PSF-2.0); NOTICE copyright Neo4j Sweden AB; Python >=3.10,<3.15; core deps neo4j>=6.3.1, numpy, scipy, pypdf, json-repair, pydantic; extras anthropic, bedrock, cohere, google, google-genai, litellm, mistralai, ollama, openai, pinecone, qdrant, weaviate, sentence-transformers, nlp (spacy==3.8.16, <3.14), fuzzy-matching, experimental; releases 1.22.0 (10-01), 1.21.0 (09-23), 1.19.0 (08-26), 1.18.0 (06-24), 1.17.0 (05-27), 1.16.1 (05-20), 1.16.0 (05-07) | Officially documented + source | https://pypi.org/pypi/neo4j-graphrag/json ; wheel https://files.pythonhosted.org/packages/07/4b/4ab5a48baa315b11867621a04a0b925d5622ba47fe35827f7cca2ca9bbc5/neo4j_graphrag-1.22.0-py3-none-any.whl | 2026-10-01 / 2026-10-26 | 0.9 | none |
| CLAIM-n4gr-02 | README main | "The official Neo4j GraphRAG package for Python", first-party with "long-term support and maintenance"; features: KG builder (`Pipeline`, `SimpleKGPipeline`, text and PDFs, APOC required), vector index creation/upsert/search, `GraphRAG`; external stores Weaviate, Pinecone, Qdrant; experimental namespace "not recommended for production use"; LLMs via extras (Ollama, OpenAI/Azure, Vertex, Gemini, Cohere, Anthropic, Mistral, Bedrock) | Officially documented | https://github.com/neo4j/neo4j-graphrag-python | n/a / 2026-10-26 | 0.8 | components left experimental in 1.19.0 (CLAIM-04) |
| CLAIM-n4gr-03 | docs landing | Neo4j >=5.18.1, Aura >=5.18.0, 2026.01+ enables SEARCH with in-index filtering; predecessor neo4j-genai deprecated; support via GitHub issues, Enterprise customer support, community | Officially documented | https://neo4j.com/docs/neo4j-graphrag-python/current/index.html | n/a / 2026-10-26 | 0.8 | 2025.x compatibility unstated |
| CLAIM-n4gr-04 | CHANGELOG | 1.19.0: components moved out of `experimental` (old imports removed in 2.0), SEARCH queries prefixed `CYPHER 25` with procedure fallback, Anthropic structured output default True; 1.18.0: GraphSchema rejects duplicate relationship labels, KEY+EXISTENCE conflict rejected; 1.22.0: schema prompt steers toward connected graphs, lazy provider imports; releases lack dates in changelog | Officially documented | https://github.com/neo4j/neo4j-graphrag-python/blob/main/CHANGELOG.md | n/a / 2026-10-26 | 0.8 | none |
| CLAIM-n4gr-05 | 1.22.0 wheel | Retrievers: VectorRetriever, VectorCypherRetriever, HybridRetriever, HybridCypherRetriever, Text2CypherRetriever, ToolsRetriever; external Pinecone/Qdrant/Weaviate retrievers join hit ids to Neo4j nodes by `id_property_neo4j`; filters (eq, neq, lt, gt, in, nin...) compiled to Cypher; `GraphRAG.search(query_text, message_history, examples, retriever_config, return_context, response_fallback)` | Observed in source code | `retrievers/*.py`, `filters.py`, `generation/graphrag.py` in 1.22.0 wheel | 2026-10-01 / 2026-10-26 | 0.9 | none |
| CLAIM-n4gr-06 | 1.22.0 wheel | `neo4j_queries.py`: `db.index.vector.queryNodes`; Cypher-25 `SEARCH node IN (VECTOR INDEX ...)` with filters; hybrid = vector + `db.index.fulltext.queryNodes` in `CALL { UNION }`; rankers NAIVE (max) and LINEAR (`alpha`, required for linear); `effective_search_ratio` | Observed in source code | `neo4j_queries.py:39-66,197-400`, `retrievers/hybrid.py:148-195` | 2026-10-01 / 2026-10-26 | 0.9 | none |
| CLAIM-n4gr-07 | 1.22.0 wheel | Text2Cypher: prompt with schema (`apoc.meta.data`) + examples; `EXPLAIN` then refuse unless `query_type` read-only; executes with `RoutingControl.READ`; `Text2CypherRetrievalError` | Observed in source code | `retrievers/text2cypher.py:173-240`, `schema.py:32-50` | 2026-10-01 / 2026-10-26 | 0.9 | none |
| CLAIM-n4gr-08 | 1.22.0 wheel | `LLMEntityRelationExtractor`: per-chunk LLM call, `max_concurrency=5`, `json_repair`, `on_error`, `create_lexical_graph=True`; `Neo4jWriter` batch_size 1000, APOC merge, `__KGBuilder__` tmp-id index; `ParquetWriter`; lexical graph NEXT_CHUNK / chunk-entity links | Observed in source code | `components/entity_relation_extractor.py`, `kg_writer.py:185-330`, `lexical_graph.py` | 2026-10-01 / 2026-10-26 | 0.9 | none |
| CLAIM-n4gr-09 | docs KG builder | SimpleKGPipeline params; schema `EXTRACTED` (default) / `FREE`; exact-match resolution on by default (label + `name`), spaCy/fuzzy resolvers "replace the nodes"; default skip failing chunk, `RAISE` fails all; structured output auto for OpenAI/Vertex/Anthropic else ValueError; "still experimental"; extractor docstring says structured output only OpenAI/Vertex and `on_error` default raise | Officially documented | https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_kg_builder.html ; wheel docstrings | n/a / 2026-10-26 | 0.8 | docstring vs docs mismatch noted |
| CLAIM-n4gr-10 | 1.22.0 wheel | `GraphPruning` enforces node/relationship types, patterns, required properties, property types and reports `PruningStats`; `GraphSchema` (node_types, relationship_types, patterns, constraints KEY/UNIQUENESS/EXISTENCE); LLM schema extraction component | Observed in source code | `components/graph_pruning.py`, `schema.py`, `graph_schema_extraction.py` | 2026-10-01 / 2026-10-26 | 0.85 | none |
| CLAIM-n4gr-11 | 1.22.0 wheel | Case-insensitive search for tenant, acl, permission, principal, access_control returns no functional code (only licence boilerplate "permissions" text) | Observed in source code (absence) | grep over all `.py` files in wheel | 2026-10-01 / 2026-10-26 | 0.85 | none |
| CLAIM-n4gr-12 | 1.22.0 wheel | `llm/`: openai, anthropic, bedrock, cohere, google_genai, mistralai, ollama, vertexai (+ litellm extra); `embeddings/`: bedrock, cohere, google_genai, mistral, ollama, openai, sentence_transformers, vertexai | Observed in source code | `llm/*.py`, `embeddings/*.py` | 2026-10-01 / 2026-10-26 | 0.9 | none |

## Appendix D — Assumptions

1. "Neo4j GraphRAG package" = PyPI `neo4j-graphrag` (`neo4j/neo4j-graphrag-python`); LLM Graph Builder app and Neo4j GDS are other entries.
2. Release dates come from PyPI; the GitHub releases page was empty in capture and the CHANGELOG has no dates.
3. Absence of ACL handling is based on a keyword search of all package files, not runtime testing.
4. Cost/throughput statements are derived models, not measurements; nothing was executed.
5. Neo4j server behaviours (vector index freshness, edition split) are taken from `C01-neo4j.md`, not re-verified.
