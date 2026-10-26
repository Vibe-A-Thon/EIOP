| Field | Value |
|---|---|
| Registry ID | T-C08-llamaindex-pgi |
| Tier | A (widely used GraphRAG framework; the de-facto Python "glue" layer between LLMs and many graph stores) |
| Versions examined | `llama-index-core` 0.14.25 (PyPI upload 2026-09-21, MIT); `llama-index-graph-stores-neo4j` 0.8.0, `-memgraph` 0.6.0, `-falkordb` 0.7.0, `-neptune` 0.6.0, `-nebula` 0.7.0 (Apache-2.0), `-tidb` 0.6.0 (all 2026-08-31); `-kuzu` 0.9.1 (2025-09-08). Source read at tag `v0.14.25` (core) and `main` (Neo4j store). |
| Verified on | 2026-10-18 |
| Worker | V10 (registry seed W21) |

## 1. Identity, current status, tier, and sources

**What it is.** `PropertyGraphIndex` is an *index class inside the LlamaIndex Python framework* (owner: LlamaIndex Inc., repo `run-llama/llama_index`). It is not a database or a service. It (a) runs *KG extractors* (LLM or rule transforms) over chunks to produce `EntityNode` / `Relation` objects, (b) upserts them into a pluggable `PropertyGraphStore` (+ optional separate vector store), and (c) exposes composable *sub-retrievers* that are merged by `PGRetriever`. [CLAIM-llamaindex-pgi-01]

| Aspect | Verified state |
|---|---|
| Licence | MIT for core and for the Neo4j/Memgraph/FalkorDB/Neptune/TiDB/Kuzu stores; Apache-2.0 for the Nebula store (PyPI metadata) [CLAIM-llamaindex-pgi-02] |
| Status | Active: core 0.14.25 on 2026-09-21; integration packages bumped 2026-08-31. Release cadence is roughly weekly for core (inferred from version number density; exact cadence NOT VERIFIED) |
| Python | `>=3.10,<4.0` for core |
| Stores listed in the official guide | `SimplePropertyGraphStore`, Neo4j, Nebula, TiDB, FalkorDB [CLAIM-llamaindex-pgi-03]; further PyPI packages exist for Memgraph, Neptune (Database/Analytics) and Kuzu |
| Kuzu trap (Master Prompt §5.1) | The `-kuzu` integration last released 2025-09-08, i.e. before the upstream Kuzu repository was reported archived (10 Oct 2025, not re-verified by this worker). Treat the Kuzu store as frozen/orphaned-risk; do not describe it as advancing [CLAIM-llamaindex-pgi-04] |
| Governance | Single-vendor open-source project; commercial products (LlamaCloud, LlamaParse) are separate and not required for PGI. Patents/trademark: NOT PUBLICLY VERIFIED |
| Name collisions | "LlamaIndex PropertyGraphIndex" replaces the older `KnowledgeGraphIndex` (triplet-only, no labels/properties) and `KnowledgeGraphRAGRetriever`; do not conflate |

Related deep dives (cross-reference, not duplicated here): `C08-microsoft-graphrag.md` (community summarisation), `C08-lightrag.md` and `C08-hipporag.md` (dual-level / PPR retrieval), `C08-graphiti-zep.md` (temporal agent memory), `C08-cognee.md` (pipeline + memory), `C08-openspg-kag.md` (schema-constrained KAG), `C08-neo4j-graphrag.md` (Neo4j's own package, may be in progress by another batch — LlamaIndex's Neo4j store and Neo4j's package overlap in function).

## 2. Primary problem, target workloads, concrete example workflows

**Problem.** Give a developer a few lines of Python that turn documents into a labelled property graph and retrieve from it with LLM-driven strategies, independent of which graph store is used.

| Workload | Fit | Notes |
|---|---|---|
| Prototype GraphRAG over a document set | Strong | `PropertyGraphIndex.from_documents(docs, property_graph_store=...)` |
| Schema-constrained extraction from domain documents | Good | `SchemaLLMPathExtractor` with allowed entities/relations/validation triples |
| NL-to-Cypher over an existing graph | Possible | `TextToCypherRetriever` — unsafe by default (see §9) |
| Governed enterprise KG with ACLs, versions, ER | Weak | None of these concepts exists in the model (see §9/§11) |

**Workflow W1 (default).** `docs -> SentenceSplitter -> [SimpleLLMPathExtractor, ImplicitPathExtractor] -> embed KG nodes -> upsert -> as_retriever() (LLMSynonym + VectorContext) -> LLM synthesis`.
**Workflow W2 (schema-strict).** `SchemaLLMPathExtractor(possible_entities=[...], possible_relations=[...], kg_validation_schema=[(S,R,O),...], strict=True)` -> store in Neo4j -> `CypherTemplateRetriever` for fixed analytical questions (e.g. "what depends on service X").
**Workflow W3 (attach to existing graph).** `PropertyGraphIndex.from_existing(property_graph_store=store, vector_store=qdrant)` and retrieve only (no extraction).

## 3. Feature inventory

| Feature | Status | Evidence |
|---|---|---|
| Python SDK / index class | Present | [01] |
| UI | Absent (library) | — |
| CLI | Absent for PGI (framework has `llama-index-cli` for RAG, unrelated) | UNVERIFIED for PGI |
| REST API / server | Absent in core (LlamaDeploy/workflows are separate) | UNVERIFIED depth |
| `SimpleLLMPathExtractor` (single-hop triples, free text labels) | Present, default | [05] |
| `ImplicitPathExtractor` (uses existing node relationships, no LLM) | Present, default | [05] |
| `DynamicLLMPathExtractor` (open ontology, optional seed type lists, optional properties) | Present | [06] |
| `SchemaLLMPathExtractor` (Pydantic/`Literal` schema, validation triples, strict/non-strict, properties) | Present | [07] |
| Retrievers: `LLMSynonymRetriever`, `VectorContextRetriever`, `TextToCypherRetriever`, `CypherTemplateRetriever`, `CustomPGRetriever` | Present | [08] |
| Native vector queries inside graph store | Per store (Neo4j, FalkorDB, TiDB yes per guide; Nebula no) | [03] |
| External vector store pairing | Present | [03] |
| Incremental insert (`insert`, `insert_nodes`) | Present (upsert); doc-hash dedupe | [09] |
| Per-document deletion / `ref_doc_info` | Absent: `ref_doc_info` raises `NotImplementedError`; delete is by node id | [09] |
| Schema introspection for text-to-Cypher | Present where store supports structured queries | [08] |
| Async | Present (`use_async=True` default); store async methods in the ABC are wrappers over sync | [10] |
| ACL / tenant / permission fields | **Absent** (only free-form `properties`) | [10] |
| Temporal validity, bitemporality, provenance beyond `MENTIONS`/source-id | Absent | [09][10] |
| Entity resolution / merging | Absent (entity id = name string) | [10] |
| Community detection / global summaries | Absent in core (separate `GraphRAGExtractor` cookbooks, UNVERIFIED) | — |

## 4. Architecture diagram

```
 Documents/Nodes (LlamaIndex node parser)
        |
        v
 +--------------------------- PropertyGraphIndex (in-process library) --------------------------+
 |  kg_extractors (TransformComponents, async, num_workers)                                      |
 |   [SimpleLLMPath | DynamicLLMPath | SchemaLLMPath | ImplicitPath | custom]                    |
 |      -> metadata[KG_NODES_KEY], metadata[KG_RELATIONS_KEY]                                    |
 |  _insert_nodes: pop KG meta -> dedupe by id/hash -> embed text + KG nodes ->                  |
 |      upsert ChunkNodes -> upsert EntityNodes -> upsert Relations (+ KG_SOURCE_REL chunk links)|
 +---------------------------+---------------------------------------+---------------------------+
                             |                                       |
                   PropertyGraphStore (ABC)                   VectorStore (optional)
         Simple(disk) | Neo4j | Memgraph | FalkorDB |          Qdrant/Chroma/PG etc.
         Neptune | Nebula | TiDB | Kuzu(frozen)
                             ^
 Query: PGRetriever = union of sub_retrievers (each -> TextNode w/ score)
   LLMSynonym  -> LLM keywords -> store.get(ids=...) -> get_rel_map(depth)
   VectorContext -> embed query -> vector_query -> get_rel_map(depth)
   Text2Cypher -> LLM(schema,q) -> optional validator -> structured_query
   CypherTemplate -> LLM structured_predict(pydantic) -> param_map -> fixed Cypher
   Custom -> user code
 Then: response synthesiser LLM (any LlamaIndex LLM, incl. local)
 Control plane: none (library). State: only in the chosen stores. No tenancy/ACL plane.
```

## 5. Under-the-hood reconstruction

**Data model** (`graph_stores/types.py`, tag v0.14.25) [CLAIM-llamaindex-pgi-10]:
- `LabelledNode{label, embedding?, properties:dict}`; `EntityNode{name; id = name with " replaced}`, label default `"entity"`; `ChunkNode{text, id_?; id = id_ or hash(text)}`, label `"text_chunk"`; `Relation{label, source_id, target_id, properties}`.
- Consequence: **identity of an entity is its surface string** (type is a label, not part of the key). Two different "Mercury" entities collapse; case/alias variants fork. A `ChunkNode` default id derived from `hash(text)` is described in the source reading as not stable across Python processes (Python string hash randomisation, *inferred, confidence 0.6*; supply `id_` explicitly).
- In-memory `LabelledPropertyGraph.delete_triplet` also deletes both endpoint nodes even when still referenced — a data-loss footgun in the Simple store [CLAIM-llamaindex-pgi-10].

**Extraction** (`indices/property_graph/transformations/`):
- *Simple*: prompt asks for `(subject, predicate, object)` triples, parsed with a regex-style parser; no types (labels default).
- *Dynamic*: prompt returns JSON list `{head, head_type, relation, tail, tail_type[, *_props]}`; parse falls back to a regex when JSON fails; allowed type lists are *prompt hints only*, not enforced. Known inconsistency: with empty property lists the props prompt is still chosen while the non-props parser is used [CLAIM-llamaindex-pgi-06].
- *Schema*: builds a Pydantic model whose entity/relation types are `Literal`s; a `before` validator uppercases and underscore-normalises labels and **drops** triplets that fail construction; with `strict=True` it additionally requires `(subjType, rel, objType)` to appear in `kg_validation_schema`, prunes non-allowed properties; self-loops with identical names dropped in both modes; errors are logged and the chunk yields no triplets unless `raise_on_error=True`. Uses structured output where the LLM supports it (`allow_additional_properties=False` for OpenAI/Gemini) [CLAIM-llamaindex-pgi-07].
- All extractors copy the *chunk's metadata* onto each produced entity/relation properties. This is the only provenance/permission propagation hook: if the loader puts `acl` in node metadata it would be copied onto the graph objects *(inferred from code behaviour; confidence 0.6)*. No enforcement.

**Insert path** (`base.py::_insert_nodes`) [CLAIM-llamaindex-pgi-09]: run extractors -> assert metadata keys -> tag KG items with `source_id` -> skip already-stored nodes (hash) -> embed chunk text and KG node strings (`embed_kg_nodes=True` default) -> write KG-node vectors to the vector index -> upsert chunks, entities, then relations ("upsert relations after nodes") -> refresh schema. Re-ingest of a changed document therefore **adds** new triplets but does not remove triplets from the old version (no reverse mapping from document to derived facts; `ref_doc_info` unimplemented).

**Storage layout (Neo4j store, `main`)** [CLAIM-llamaindex-pgi-11]: labels `__Node__` (all), `__Entity__` (+ APOC-added type label), `Chunk`; `MENTIONS` edges chunk->entity; uniqueness constraints on `id`; vector index `entity` on `__Entity__.embedding` (Neo4j >= 5.23); writes batched 1,000 via `UNWIND ... MERGE`; **requires APOC** (`apoc.merge.relationship`, `apoc.create.addLabels`, schema procedures). `structured_query` uses `driver.execute_query` (default write routing; no `execute_read`), so a generated `DELETE` would execute. `database` argument selects a Neo4j database (a *possible* tenant-isolation hook, not provided as a feature).

**Query pipeline**:
- *LLMSynonym*: LLM emits `^`-separated keywords (prompt: synonyms, case/plural variants) -> each `.capitalize()`d (lowercases the rest, so "NASA" becomes "Nasa" — a documented-in-code mismatch with ingestion normalisation) -> `store.get(ids=keywords)` (exact id match, not fuzzy) -> `get_rel_map(depth=path_depth, limit=30, ignore_rels=[KG_SOURCE_REL])` [CLAIM-llamaindex-pgi-08].
- *VectorContext*: embed question -> `vector_query` on graph store if supported, else external vector store then map ids back -> `get_rel_map` -> score each triplet by max(endpoint score) -> sort -> optional `similarity_score` cut-off (0.0 disables because of a truthiness check). Default `similarity_top_k=4`, `path_depth=1`.
- *Text2Cypher*: `schema` string + question -> `llm.predict` -> optional `cypher_validator` -> `structured_query`; optional output-field allow-list; optional LLM summarisation. **No built-in write guard**; docs/docstring tell integrators to use read-only roles [CLAIM-llamaindex-pgi-08].
- *CypherTemplate*: LLM only fills a Pydantic model; values bound as parameters to a fixed Cypher string — the safest option and the closest analogue of EOIP's typed plan (BL-08) [CLAIM-llamaindex-pgi-08].
- Pseudocode of the fusion: `nodes = ⋃ r.retrieve(q) for r in sub_retrievers; text-chunk attach if include_text (via MENTIONS/source rel); return nodes` (no rank fusion across sub-retrievers in the code read; fusion semantics for `PGRetriever` NOT VERIFIED beyond concatenation).

**Reasoning / concurrency / partitioning / caching / versioning / security**: none native. Transactions, isolation, sharding and consistency are inherited entirely from the chosen store; core does not coordinate multi-step ingestion atomically (nodes then relations are separate upserts; partial failure leaves orphan nodes). No caching beyond LLM-level caches users configure. No versioning. Security = whatever the store enforces; the library has no principal concept [CLAIM-llamaindex-pgi-10].

## 6. Inferred requirements

| ID | Requirement visible from behaviour |
|---|---|
| F1 | Pluggable extractor chain with schema-constrained mode and validation triples |
| F2 | Store abstraction with `get / get_triplets / get_rel_map / upsert / delete / structured_query / vector_query` |
| F3 | Retrieval sub-strategies composable per query, including a parameterised-Cypher retriever |
| F4 | Embedding of KG nodes (not only chunks) |
| N1 | Works with any LlamaIndex-compatible LLM/embedding (local or hosted) |
| N2 | Extraction throughput bound by LLM concurrency (`num_workers`) |
| N3 | No consistency guarantees across multi-step writes |

## 7. Performance and resource model

No vendor benchmark of PGI itself was found; none is claimed here. Cost model derived from code: ingestion makes **one LLM call per chunk** per LLM extractor (plus an embedding call per KG node when `embed_kg_nodes=True`); query makes **one LLM call for synonyms** (LLMSynonym) and/or one for Text2Cypher / template parameterisation, plus embedding of the query, plus final synthesis [CLAIM-llamaindex-pgi-09]. Latency at query = LLM(synonym) + store round trips + LLM(answer). Write throughput = 1,000-row UNWIND batches on Neo4j. Failure modes: LLM JSON/format errors silently produce zero triplets (`raise_on_error=False` default) so recall loss is invisible without telemetry; exact-id synonym lookup misses non-canonical spellings; Simple store keeps the whole graph in RAM. Scaling behaviour on large corpora, memory per million nodes, p95 latency: NOT PUBLICLY VERIFIED. Independent evaluations comparing PGI with other GraphRAG systems were not located (confidence in any ranking claim = 0). Master Prompt §5.3 applies: benchmark against BM25/dense/hybrid/rerank baselines before adopting graph retrieval.

## 8. Strengths and use-case-specific advantages

| Strength | How to match/exceed |
|---|---|
| Broad store/LLM/embedding coverage in one abstraction | EOIP already has `GraphStore` (BL-01..06); add an *adapter-level* extractor/retriever interface instead of copying the ABC |
| Four extractor modes spanning open → strict schema | Reuse the *pattern*: open extraction proposes, strict mode validates against EOIP ontology (BL-27/28) |
| `CypherTemplateRetriever`: LLM fills typed parameters, query text is fixed | EOIP's `QueryPlan` (BL-08) is stronger (typed, bounded, policy-checked); extend with LLM-filled plan parameters |
| Embeddings on KG nodes allow entity linking by vector | Implement against EOIP vector layer (BL-14) with tenant filter |
| `ImplicitPathExtractor` (no LLM) | Matches EOIP's deterministic-first stance; EOIP's JSON relationship discovery (BL-26) already exceeds it |
| Large community, many examples | Compatibility goal: expose an EOIP `PropertyGraphStore` shim so LlamaIndex apps can read through EOIP's permissioned API |

### Strength-adoption cards

| ID | Competitor | Strength | Evidence | Value to EOIP customers | Verdict | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-llamaindex-pgi-01 | LlamaIndex PGI | LLM-fills-parameters-of-fixed-query (CypherTemplate) | [08] | NL questions without LLM-authored query text | match (EOIP QueryPlan is already stronger) | Let local LLM emit a Pydantic `QueryPlan` fragment; the existing executor validates | 200 NL questions: 0 plans bypass policy; >= X% correct plan vs gold |
| STR-llamaindex-pgi-02 | LlamaIndex PGI | Schema-strict extraction with validation triples and property pruning | [07] | Fewer junk edges | exceed | Feed EOIP ontology (allowed types/edges) into extraction prompt; reject outside schema into review queue not drop silently | Precision of accepted edges >= baseline; 100% rejected edges logged with reason |
| STR-llamaindex-pgi-03 | LlamaIndex PGI | Pluggable retriever composition (synonym + vector + structured) | [08] | Recall across query styles | match | Express as EOIP retrieval strategy registry feeding RRF (BL-15) | Ablation: each strategy's marginal recall on eval set |
| STR-llamaindex-pgi-04 | LlamaIndex PGI | Store-agnostic framework adoption | [03] | Ecosystem reach | integrate (read-only shim) | Optional shim package, tenant-scoped, ACL-filtered | LlamaIndex app reads EOIP graph only through shim; cross-tenant read test fails closed |

## 9. Limitations with root causes

**Algorithmic dead-ends**
- Entity identity = name string (no ER, no type in key) -> collisions/forks; no merge/split [CLAIM-llamaindex-pgi-10]. (proven from source)
- Retrieval = one-hop-ish neighbourhood expansion from LLM-guessed/embedded seeds; no ranking over multi-hop evidence (contrast HippoRAG PPR in `C08-hipporag.md`) (proven for default retrievers).

**Operational / hardware overhead**
- One LLM call per chunk at ingest; failures silent by default; Neo4j store needs APOC and Neo4j >= 5.23 for the vector index [CLAIM-llamaindex-pgi-11].
- Re-ingest/update leaves stale triplets (no document-to-fact mapping) [CLAIM-llamaindex-pgi-09].
- Non-atomic nodes-then-relations upsert.

**User/developer friction and security**
- `TextToCypherRetriever`: no write guard, Neo4j store executes through write-routed `execute_query` -> a prompt-injected question can mutate or delete (docs recommend read-only roles) [CLAIM-llamaindex-pgi-08][11]. (proven)
- No ACL/tenant model at all [CLAIM-llamaindex-pgi-10]. (proven) Vector search `filters` can be passed, but nothing populates or enforces them.
- Docstring/code mismatches (default extractor name; `capitalize()` lowering acronyms; props prompt/parser mismatch) — maturity signal (proven).
- Kuzu store orphaned if upstream archived (to be re-verified) [04].
- Licensing: MIT everywhere checked; the stores talk to Neo4j (GPLv3 Community / commercial) and others whose server licences differ — outside the library, flag for legal review per store, not for PGI.

### Inversion cards

**INV-llamaindex-pgi-01 — Unguarded NL→Cypher**
- Target: PGI 0.14.25, `TextToCypherRetriever` + Neo4j store, any workload with untrusted question text. Limitation: no read-only enforcement (proven, [08][11]). Root cause: *semantics/governance* (proven).
- Alternative: LLM proposes a typed `QueryPlan` ⇒ compiled by trusted templates (EOIP BL-08); worse when questions need arbitrary analytics beyond template coverage.
- Options: (1) quick: wrap retriever with `cypher_validator` + read-only DB role; (2) native: LLM-emitted plan JSON validated by `query/policy.py` and tenant-scoped; (3) long-term: verified plan synthesis with explain/preview and candidate-query suggestion (BL-11) before execution.
- Selected: option 2. Sketch: `LLM -> QueryPlan(intent, anchors, hops<=k, limit) -> policy.check(principal) -> template -> backend`.
- POC: 300-question set incl. 50 injection attempts; success = 0 writes, >= parity answer accuracy vs raw text-to-Cypher; baseline cost = one local LLM call.
- Dependencies: BL-18 ACL enforcement. Failure cases: LLM emits plan with widened anchors -> policy truncates; fallback deterministic suggestion.
- Defensibility: policy + tenant + audit integration, not the prompt. Decision: **ADOPT** (already direction of BL-08/BL-12).

**INV-llamaindex-pgi-02 — No fact-level provenance/ACL/update semantics**
- Limitation: facts carry only `source_id`/metadata copy; stale facts persist; no ACL enforcement (proven, [09][10]). Root cause: *data model* (proven).
- Alternative: derived facts as `PROPOSED` claims with evidence span + `acl_hash` inherited from source (BL-17, BL-40, BL-41); re-ingest retracts facts whose sole evidence was the superseded revision (tombstone BL-25); retrieval filters by principal. Worse when there is no source ACL to inherit.
- Options: (1) quick: carry `acl_hash` in chunk metadata and filter vector store; (2) native: fact-evidence table + reference counting; (3) long-term: bitemporal evidence graph with per-fact permission closure.
- Selected: 2. POC: update 1,000 docs, assert stale-fact count 0 and cross-principal leak count 0 across 10 principals; baseline: PGI re-ingest leaves N stale facts (measure). Defensibility: governance data model is the moat, not extraction. Decision: **ADOPT**.

**INV-llamaindex-pgi-03 — Silent extraction loss**
- Limitation: `raise_on_error=False` default, invalid triplets dropped, no counters (proven, [07]). Root cause: *UX/governance*. Alternative: extraction telemetry (accepted/rejected/error per chunk) and a rejected-edge review queue (BL-35). Option 1: set `raise_on_error=True`; 2: wrap extractors with counters; 3: calibrated extraction QA. Selected 2. POC: inject 5% malformed LLM outputs; success = 100% surfaced. Decision: **ADOPT** (small).

**Seed hypothesis check (Master Prompt §10.5):** "Graphiti/agent-memory: LLM-dependent extraction cost" — partly applies to PGI (one call per chunk, proven) → *validated in structure*; "Microsoft GraphRAG costly indexing" — PGI default avoids community summaries, so the hypothesis does **not** target PGI (rejected for this target).

## 10. Deployment, licensing, redistribution, operational viability

| Item | Assessment |
|---|---|
| Deployment | Library inside EOIP's Python/FastAPI process; no extra service. Optional store servers (Neo4j etc.) as separate containers |
| Air-gap | Viable: no mandatory network call in the code read; LLM/embedding are injected objects. Default `Settings.llm` historically resolves to OpenAI if unset — must be explicitly overridden (egress risk; UNVERIFIED for 0.14.25 default, confidence 0.5) |
| Local models | Supported via LlamaIndex LLM integrations (Ollama, llama.cpp, vLLM); structured-output-dependent extractors (`SchemaLLMPathExtractor`) degrade on small models that cannot emit valid JSON/Pydantic — error → zero triplets. Quality on 7–8B models: NOT PUBLICLY VERIFIED |
| Licence | MIT (core + stores except Nebula Apache-2.0): redistribution/OEM permissive; no copyleft in the library. Transitive deps (e.g. `neo4j` driver Apache-2.0, `falkordb`, `nebula3-python`, `pymemgraph`) need an SBOM scan: not done here [CLAIM-llamaindex-pgi-02] |
| Legal review trigger | Not for the library; yes for server-side stores (Neo4j GPLv3/commercial, Memgraph BSL/Enterprise, FalkorDB SSPL — see their C01 deep dives) |
| One-node first | Yes with `SimplePropertyGraphStore` (RAM-bound, no Cypher) or a single Neo4j/FalkorDB container |
| Dependency weight | Core pulls a large transitive tree (NLTK, tiktoken, SQLAlchemy, etc.; details UNVERIFIED) — a supply-chain surface to pin and mirror |

## 11. Competitive delta against EOIP baseline

| Area | PGI | EOIP | Delta |
|---|---|---|---|
| GraphRAG/retrieval (BL-16) | LLM-driven seeds + neighbourhood | Deterministic graph-first evidence retrieval; no benchmark vs plain RAG | EOIP has no LLM-synonym/entity-vector seeding; PGI has no benchmark either — run both against hybrid baseline |
| NL→query (BL-11/12) | Text2Cypher (unsafe), CypherTemplate (safe) | Deterministic suggestions + optional `LLMAssistHook` | EOIP safer; PGI more automated. Adopt parameter-filling pattern |
| Vector/hybrid (BL-14/15) | Delegates to store/vector DB; no fusion | Hashing embedder default, pure-Python HNSW, RRF implemented | EOIP has fusion; lacks production vector backend (BL-14 Partial) — INTEGRATE external vector store |
| Extraction (BL-26/27/28) | LLM extractors with schema | Rule-based JSON profiling + validation gate; LLM extraction partial | PGI offers LLM text extraction EOIP lacks as a first-class path (CAP-32) |
| ACL (BL-17/18) | None | Captured, not enforced (P0 gap) | PGI offers no help; parity not a differentiator |
| Provenance/epistemic (BL-39..41) | Chunk link only | Claims, evidence manifests | EOIP ahead |
| Backends (BL-01..06) | Neo4j, Memgraph, FalkorDB, Neptune, Nebula, TiDB, Kuzu; **not HugeGraph/JanusGraph** | HugeGraph, Neo4j, Neptune, Janus, RDF | EOIP backend coverage differs; PGI cannot be a HugeGraph path without writing a store |

## 12. Cards

Strength cards: see §8. Inversion cards: see §9.

## 13. Per-capability decisions

| Capability | Decision | Line |
|---|---|---|
| CAP-32 unstructured extraction | EXPERIMENT | Prototype `SchemaLLMPathExtractor` behaviour behind EOIP ontology (reimplement pattern; LlamaIndex as optional dev dependency only) |
| CAP-58 NL→query | BUILD (typed-plan pattern) / REJECT raw Text2Cypher in production |
| CAP-56 GraphRAG | EXPERIMENT: PGI-style synonym+vector seeding as an *additional* strategy; require beating hybrid baseline |
| CAP-53/55 vector + fusion | REUSE EOIP RRF; INTEGRATE external vector store |
| CAP-46 source-ACL | BUILD (PGI offers nothing) |
| CAP-59 MCP/agent interface | REFERENCE: EOIP MCP is more governed |
| CAP-61 local model serving | INTEGRATE via EOIP model-abstraction, not via LlamaIndex Settings |
| Store ABC adoption | REJECT copying; optional read-only shim DEFER |

## 14. Concrete tests and acceptance conditions

1. **Baseline shootout** (CAP-56): same 500-question eval over EOIP corpus: BM25, dense, hybrid+rerank, EOIP graph-first, PGI default, PGI+EOIP ontology. Metric: answer support rate with cited spans, recall@k; report cost (LLM calls) — accept PGI-style seeding only if it beats hybrid by a pre-registered margin.
2. **Extraction QA**: 200 chunks gold-labelled; compare Simple/Dynamic/Schema(strict) with a local 8B model vs hosted reference (hosted only on synthetic data); metrics: edge precision/recall, invalid-output rate.
3. **Safety**: replay 50 prompt-injection questions into Text2Cypher with a Neo4j database that has write permission; expect writes without guard (confirms INV-01); then through EOIP plan route: 0 writes.
4. **Update semantics**: ingest doc v1, v2 (changed facts); count stale triplets in PGI vs EOIP design.
5. **Tenant/ACL**: two tenants, same entity name — verify collision in PGI default store; EOIP design must isolate.

## 15. Risks, trade-offs, open questions

- Default LLM/embedding resolution may reach external endpoints if unset: enforce EOIP egress gateway (BL-45) by constructing explicit local objects.
- Framework churn (0.x semantic versioning, frequent breaking changes in integrations) — pin versions.
- Graph benefit unproven vs plain RAG for our corpora (§5.3).
- Open: does `PGRetriever` apply any rank fusion? Does `include_text` attach chunks via `MENTIONS`/source rel for all stores? Quality of Schema extractor on local 7–14B models? Kuzu upstream status re-check.

---

## Appendix A. Research-dimension coverage

| Dimension | Sections | Summary / N/A |
|---|---|---|
| D1 Identity/maturity | 1 | MIT, active, single vendor |
| D2 Problem/workloads | 2 | Doc-to-graph RAG glue |
| D3 Architecture | 4, 5 | Library; no services |
| D4 Storage/indexing | 5 | Delegated to store; Neo4j layout read |
| D5 Schema/semantics | 5, 9 | Schema only in extraction; no constraints in model |
| D6 Query pipeline | 5 | Retriever strategies; no planner |
| D7 Reasoning | N/A | None native |
| D8 Transactions/scale | 5, 7 | Delegated; non-atomic multi-step |
| D9 Ingestion/federation | 5 | Extractor chain; no CDC/replay |
| D10 Identity/evidence | 5, 9 | Name-string identity; chunk link only |
| D11 Time/evolution | 5, 9 | None; stale facts |
| D12 Algorithms/ML | N/A | None (embeddings only) |
| D13 Retrieval/agents | 5, 8 | Core strength |
| D14 NL query | 5, 9 | Text2Cypher/Template |
| D15 Governance | N/A | None |
| D16 Human experience | N/A | Library; no UI |
| D17 Developer experience | 3, 9 | Strong docs/community; docstring mismatches |
| D18 Security | 9 | Injection exposure; no ACL |
| D19 Multi-tenancy | 9 | None; `database` arg only |
| D20 Economics | 7 | LLM-call-per-chunk model; no measured numbers |
| D21 Commercial | 10 | MIT; vendor products separate |
| D22 Interop/lock-in | 3, 11 | Store ABC; no import/export semantics |
| D23 IP/prior art | 10 | NOT PUBLICLY VERIFIED |
| D24 Research quality | 7, 15 | No independent benchmark found |

## Appendix B. Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-32 | native (LLM extractors) | [05][06][07] | BL-26/27 Partial | EXPERIMENT | P1 |
| CAP-28 | partial (LLM-induced types) | [06] | BL-26 Implemented | REUSE EOIP | P3 |
| CAP-14 | partial (Cypher via stores) | [08] | BL-03 Implemented | REUSE | P3 |
| CAP-53 | partial (delegated) | [03][11] | BL-14 Partial | INTEGRATE external | P1 |
| CAP-55 | absent (no fusion read) | [08] | BL-15 Implemented | REUSE EOIP | P3 |
| CAP-56 | partial (local retrieval only) | [08] | BL-16 Implemented | EXPERIMENT | P2 |
| CAP-58 | native (unsafe/safe variants) | [08] | BL-11/12 | BUILD typed-plan | P1 |
| CAP-46 | absent | [10] | BL-18 Absent | BUILD | P0 |
| CAP-47 | absent | [10] | BL-20 Partial | BUILD | P0 |
| CAP-38 | partial (source id) | [09] | BL-41 Implemented | REUSE EOIP | P3 |
| CAP-31 | absent | [10] | BL-36 Absent | INTEGRATE Splink/Zingg | P1 |
| CAP-49 | absent | [08] | BL-08 Implemented | BUILD | P1 |
| CAP-61 | plugin (LLM integrations) | [01] | BL-45 | INTEGRATE | P2 |
| CAP-78 | absent | — | none | BUILD | P1 |

## Appendix C. Evidence records

All sources accessed 2026-10-18; code at tag `v0.14.25` unless noted. Confidence 0..1.

| CLAIM-ID | product/version/date | claim | class | source | pub/access | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-llamaindex-pgi-01 | llama-index-core 0.14.25 | PGI = extractors + PropertyGraphStore + sub-retrievers | Observed in source | `llama-index-core/llama_index/core/indices/property_graph/base.py` (github.com/run-llama/llama_index) | tag 0.14.25 / 2026-10-18 | 0.85 (read via summarising fetch) | none |
| CLAIM-llamaindex-pgi-02 | PyPI metadata | Core MIT, py>=3.10; stores MIT (Nebula Apache-2.0) | Officially documented | pypi.org/pypi/llama-index-core/json and per-package JSON | 2026-09-21 / 2026-10-18 | 0.9 | none |
| CLAIM-llamaindex-pgi-03 | guide | Store table: Simple, Neo4j, Nebula, TiDB, FalkorDB; native embeddings on Neo4j/TiDB/FalkorDB | Officially documented | developers.llamaindex.ai/python/framework/module_guides/indexing/lpg_index_guide/ | n.d. / 2026-10-18 | 0.8 | Memgraph/Neptune/Kuzu packages exist but absent from table |
| CLAIM-llamaindex-pgi-04 | kuzu store 0.9.1 | Last release 2025-09-08 | Officially documented | PyPI `llama-index-graph-stores-kuzu` | 2025-09-08 / 2026-10-18 | 0.8; upstream archival NOT re-verified here | — |
| CLAIM-llamaindex-pgi-05 | 0.14.25 | Default extractors Simple + Implicit; docstring says ImplicitEdge | Observed in source | `base.py`; guide above | 2026-10-18 | 0.8 | docstring vs code |
| CLAIM-llamaindex-pgi-06 | 0.14.25 | Dynamic extractor behaviours, JSON+regex parse, props prompt/parser mismatch | Observed in source | `transformations/dynamic_llm.py` | 2026-10-18 | 0.75 | — |
| CLAIM-llamaindex-pgi-07 | 0.14.25 | Schema extractor strict/non-strict, drops invalid, `raise_on_error=False` default | Observed in source | `transformations/schema_llm.py` | 2026-10-18 | 0.8 | — |
| CLAIM-llamaindex-pgi-08 | 0.14.25 | Retriever behaviours; Text2Cypher no write guard; CypherTemplate parameter binding | Observed in source | `sub_retrievers/{text_to_cypher,cypher_template,vector,llm_synonym}.py` | 2026-10-18 | 0.8 | — |
| CLAIM-llamaindex-pgi-09 | 0.14.25 | `_insert_nodes` flow; `ref_doc_info` NotImplemented; no per-doc fact removal | Observed in source | `base.py` | 2026-10-18 | 0.8 | Stale-fact consequence is a reasoned inference |
| CLAIM-llamaindex-pgi-10 | 0.14.25 | Node/relation model, id semantics, no ACL/tenant fields, in-memory delete_triplet removes endpoints | Observed in source | `graph_stores/types.py` | 2026-10-18 | 0.8 | hash-instability statement is inference (0.6) |
| CLAIM-llamaindex-pgi-11 | neo4j store main/0.8.0 | Labels, APOC dependency, vector index >=5.23, UNWIND batches 1000, `execute_query` default routing | Observed in source | `llama-index-integrations/graph_stores/llama-index-graph-stores-neo4j/.../neo4j_property_graph.py` | main / 2026-10-18 | 0.75 | — |

## Appendix D. Assumptions

- Code facts were read through a summarising fetch tool, not a local clone; line-level pinning and behavioural reproduction were not performed (hence confidence <= 0.85).
- "Verified on 2026-10-18" follows the brief although the environment date is later.
- `PGRetriever` fusion semantics and default LLM resolution in 0.14.25 were not read; marked UNVERIFIED.
- Kuzu upstream archival taken from Master Prompt §5.1, not re-verified.
- Performance statements are cost-model derivations from code, not measurements.
