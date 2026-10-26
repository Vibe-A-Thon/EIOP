# C08 — Mem0 (agent memory layer)

| Field | Value |
|---|---|
| Registry ID | T-C08-mem0 |
| Tier | A — most-adopted agent-memory library (67.8k GitHub stars); reuse/pattern candidate for CAP-57; target of Master Prompt §10.5 seed "Graphiti / agent-memory systems" |
| Versions examined | `mem0ai` 2.2.1 (PyPI 2026-09-25; wheel unpacked and read); 2.2.0 (09-23), 2.1.0 (09-18), 2.0.20 (09-02), 2.0.19 (08-24); algorithm change shipped as Python 2.0.0 / TypeScript 3.0.0 on 2026-04-14; paper arXiv:2504.19413 v1 (2025-04-28) |
| Verified on | 2026-10-26 |
| Worker | V07 (batch for W20 scope) |

## 1. Identity, current status, tier, and sources

- **What it is.** Mem0 ("The Memory Layer for AI Agents") is a Python/TypeScript library plus a self-hosted REST server and a managed **Mem0 Platform**. Owner: Mem0 (GitHub `mem0ai/mem0`, authors of the paper include Taranjeet Singh and Deshraj Yadav) [CLAIM-mem0-01][CLAIM-mem0-02].
- **Licence.** Apache-2.0 for the repository and the `mem0ai` wheel [CLAIM-mem0-01]. The licence text's copyright line is the unfilled appendix template; the holder is **not verifiable from the licence text**. Open-source vs platform split is real: the README says published benchmark scores reflect the managed platform's "proprietary optimizations not available in the open-source SDK", and "Advanced Features" are "Teasers" in the self-hosted server and "All included" on Cloud [CLAIM-mem0-02]. This is a community-vs-commercial split to record for legal review.
- **Status.** Active, ~weekly releases; major algorithm break on 2026-04-14 ("v3 algorithm": ADD-only extraction, **external graph stores removed from OSS**) [CLAIM-mem0-03][CLAIM-mem0-04]. Version numbers diverge by language (Python 2.x, TypeScript 3.x). Traps resolved: (a) older blog posts and the paper describe a LLM-driven ADD/UPDATE/DELETE/NOOP pipeline and a Neo4j/Memgraph "Mem0g" graph variant; **both are gone from the current OSS code** (§5). (b) "OpenMemory MCP" is a separate Mem0 product line, not examined here (NOT PUBLICLY VERIFIED in this run).
- Sources used (13): PyPI project page and JSON for `mem0ai`; GitHub README and LICENSE; Mem0 changelog; OSS v2-to-v3 migration guide; graph-memory, add-operation, vector-store, Ollama, OSS-overview, REST-API and platform-overview docs; the 2.2.1 wheel source; arXiv:2504.19413; Zep rebuttal blog (2025-05-06); Letta benchmark blog (2025-08-12); a search-aggregated Mem0 comparison summary. Cross-references: `C08-graphiti-zep.md` (temporal facts, ACL gap), `C08-cognee.md` (dataset ACL, forget), `C08-tier-c-records.md`.

## 2. Primary problem, target workloads, concrete example workflows

Problem: LLM apps forget between sessions; stuffing full history is expensive. Mem0 extracts durable "memories" from conversations, stores them with embeddings, and retrieves a small relevant set (vendor: ~7K tokens/query) [CLAIM-mem0-15]. Workloads: per-user personalisation (support, coaching), per-agent knowledge, per-run scratch memory; coding assistants via MCP.

Workflows (verified against source): (1) `m.add(messages, user_id="u1")` -> top-10 similar existing memories fetched -> one LLM call returns new facts -> hash-dedup -> embed -> insert [CLAIM-mem0-06]. (2) `m.search("diet?", filters={"user_id":"u1"})` -> semantic + BM25 + entity boost -> top-20 [CLAIM-mem0-07]. (3) `m.add(..., infer=False)` stores raw messages verbatim [CLAIM-mem0-09]. (4) `m.update/delete/history(memory_id)` explicit CRUD with an audit-style history table [CLAIM-mem0-06].

## 3. Feature inventory

| Feature | Status | Surface | Evidence |
|---|---|---|---|
| LLM fact extraction, single call, ADD-only | Present (since 2026-04-14) | SDK, REST | CLAIM-03, -06 |
| LLM-driven UPDATE/DELETE/NOOP on add | **Absent in OSS now** (present before 2.0; custom_update_memory_prompt deprecated) | – | CLAIM-04 |
| Explicit update / delete / delete_all / history | Present | SDK, REST | CLAIM-06, -08 |
| Typed graph memory in OSS (Neo4j, Memgraph, Kuzu, AGE, Neptune) | **Removed**; `relations` always `[]` | – | CLAIM-04, -05 |
| Graph memory on Platform | Platform-only, "native"; described as entity linking, **no typed relationships** | Cloud | CLAIM-05 |
| Hybrid retrieval (semantic + BM25 + entity linking) | Present; BM25/entity need `mem0ai[nlp]` + fastembed | SDK | CLAIM-04, -07 |
| Scoping ids `user_id`, `agent_id`, `run_id`, `app_id`, `actor_id` | Present (caller-supplied filters) | SDK, REST | CLAIM-08 |
| Expiry `expiration_date` (date granularity) | Present | SDK | CLAIM-09 |
| Reranker | Optional, default off | SDK | CLAIM-04 |
| Vector stores | 22 (Python): Qdrant default, FAISS, Chroma, pgvector, Milvus, Weaviate, OpenSearch, Elasticsearch, Neptune Analytics… | SDK | CLAIM-12 |
| LLM providers incl. local | Ollama, vLLM, LM Studio, LiteLLM, plus cloud providers | SDK | CLAIM-13 |
| Self-hosted server (FastAPI + Postgres/pgvector, dashboard, per-user API keys, request log) | Present; auth on by default | Docker Compose | CLAIM-11 |
| Multi-tenant model, ACL, ReBAC | **Absent** in library; not documented for server | – | CLAIM-08, -11 |
| Procedural memory (`_create_procedural_memory`) | Present | SDK | source |
| Evidence spans / source provenance on a memory | Absent (only `attributed_to`, `role`, timestamps) | – | CLAIM-06 |
| Temporal validity (valid_from/valid_to) | Absent (only created_at/updated_at/expiration_date) | – | CLAIM-06, -09 |
| Telemetry | Present, **on by default** (PostHog) | – | CLAIM-10 |

## 4. Architecture diagram

```
 app/agent ──add(messages, user_id|agent_id|run_id, infer)──►  Memory (in-process library)  or  FastAPI server (JWT / X-API-Key, Postgres+pgvector)
                                                              │
        ┌─────────────────────────┬──────────────────────────┼───────────────────────────┬──────────────────────┐
        ▼                         ▼                          ▼                           ▼                      ▼
  LLM client (1 call/add)   Embedder (per fact)   Vector store (payload = memory row)  Entity store          History DB (SQLite)
  OpenAI default; Ollama,   OpenAI default;       Qdrant default; 22 backends;          collection             `history` (event log)
  vLLM, LM Studio …         Ollama/HF/fastembed   dense + sparse BM25 (Qdrant)          `{coll}_entities`      `messages` (last-10 context)
                                                                                         (spaCy entities)      ~/.mem0/history.db
 search(query, filters) ──► embed ─► vector top-N ─► keyword top-N ─► entity boost ─► additive score ─► top_k (default 20, threshold 0.1)
 Telemetry (PostHog, default on, 10% sampling of hot-path events) ──► external
```

## 5. Under-the-hood reconstruction (from `mem0ai` 2.2.1 wheel, `mem0/memory/main.py`, `utils/scoring.py`, `memory/storage.py`)

**Data model.** A memory is **one row in the vector store**: id (uuid4), vector, payload `{data, hash(md5 of text), text_lemmatized, user_id, agent_id, run_id, actor_id?, role?, attributed_to?, created_at, updated_at, expiration_date?, <free metadata>}` [CLAIM-mem0-06]. There is no edge, no entity-typed node, no evidence pointer, no validity interval. The "graph" is a second vector collection `{collection}_entities` whose rows hold `entity_text`, type and linked memory ids; `_upsert_entity`/`_link_entities_for_memory` create it, `_remove_memory_from_entity_store` cleans it on delete. Relationships are co-occurrence of an entity across memories only [CLAIM-mem0-05].

**History/audit.** SQLite (`history_db_path`, default under `~/.mem0`) with `history` (per-memory event log) and `messages` (last messages per session scope, used as 10-message context) [CLAIM-mem0-06]. History is a local file, not in the vector store, so backup/restore consistency across the two is the operator's problem (hypothesis; no cross-store transaction visible).

**Write path (`_add_to_vector_store`, phased batch).**
```
if not infer: for each non-system message: embed; _create_memory(...); event=ADD          # verbatim
ctx   = db.get_last_messages(scope, 10)
exist = vector_store.search(parsed_messages, top_k=10, filters={user_id,agent_id,run_id})
map   = {"0":uuid0, "1":uuid1 ...}      # integer aliases shown to the LLM (anti-hallucination of ids)
out   = llm(ADDITIVE_EXTRACTION_PROMPT [+AGENT_CONTEXT_SUFFIX if agent-only scope], json_object)  # ONE call
facts = out["memory"]                    # LLM failure -> raise LLMError (no silent empty list)
embeddings = embed_batch(texts)          # fallback to one-by-one
for f in facts: h = md5(text); skip if h in existing hashes or batch; payload+=lemmatized,hash,timestamps
vector_store.insert(batch); history.add(ADD); link entities; return only persisted rows
```
Evidence: [CLAIM-mem0-06]. Deduplication is **exact-hash only** within the top-10 neighbours; near-duplicates and contradictions are not reconciled in the write path (the LLM sees the 10 neighbours and is prompted to extract new information, but cannot emit UPDATE/DELETE) [CLAIM-mem0-04][CLAIM-mem0-06].

**Read path (`_search_vector_store`).**
```
q_lem = lemmatize(query); q_ent = spaCy entities(query)     # extras: mem0ai[nlp]
sem   = vector_store.search(q_vec, top_k=max(4*limit,60), filters)
kw    = vector_store.keyword_search(q_lem, ...)             # BM25; all 15 stores gained keyword_search in v3
bm25  = sigmoid(raw; midpoint,steepness by query length)    # per-query normalisation
ent   = entity-store similarity boost (weight ENTITY_BOOST_WEIGHT)
drop expired (payload.expiration_date < today UTC) unless show_expired
score = (sem + bm25 + ent) / (1 + [bm25 present] + [ent present]*W)   # threshold gates *semantic* score first
```
[CLAIM-mem0-07]. Hypothesis: the score is not calibrated across queries (divisor depends on which signals fired), so thresholds are not comparable between queries.

**Scoping and security.** Scope is **payload equality filters** built by `_build_filters_and_metadata`; identity keys inside user metadata are dropped so free metadata cannot move a memory into another scope; empty/whitespace ids are rejected; `delete_all` requires at least one filter; top-level entity kwargs on `search`/`get_all` raise (v3) [CLAIM-mem0-04][CLAIM-mem0-08]. There is **no principal, no ACL, no policy hook** in the library: whoever calls with a `user_id` reads that user's memories. The server adds authentication (JWT / `X-API-Key`, `AUTH_DISABLED` escape hatch) but documents no tenant model [CLAIM-mem0-11].

**Expiry/deletion.** Expiry is a **read-time filter** on a date (no time-of-day), not physical deletion; fetch-by-id still returns expired rows [CLAIM-mem0-09]. Physical delete is explicit (`delete`, `delete_all`), with entity-store cleanup.

**Concurrency/transactions.** None across stores: vector insert, history write and entity link are sequential; code comments confirm partial-failure handling ("a record the store rejected must never be reported as ADD") [CLAIM-mem0-06]. Partitioning/consistency are delegated to the chosen vector store. Caching: none beyond the vector store. Versioning: `history` events only.

## 6. Functional and non-functional requirements inferred

| ID | Requirement (what a competitive EOIP memory service must do) | Basis |
|---|---|---|
| FR-M1 | One LLM call (or zero, `infer=False`) per write; failure is surfaced, never swallowed | CLAIM-06 |
| FR-M2 | Scope keys (user/agent/run/actor/app) as first-class filters; metadata cannot override scope | CLAIM-08 |
| FR-M3 | Hybrid retrieval (dense + lexical + entity) with explainable score details (`explain=True`) | CLAIM-07 |
| FR-M4 | Per-memory expiry plus explicit delete with cascade to entity index | CLAIM-06, -09 |
| FR-M5 | Backend-pluggable vector store (22) and LLM/embedder (local included) | CLAIM-12, -13 |
| NFR-M1 | Telemetry off by default and removable for air-gap (Mem0 fails this) | CLAIM-10 |
| NFR-M2 | Local default models; Mem0 defaults to OpenAI (gpt-5-mini, text-embedding-3-small) | CLAIM-11 |

## 7. Performance and resource model

All figures below are **vendor claims**: LoCoMo 92.5, LongMemEval 94.4, BEAM-1M 64.1, BEAM-10M 48.6; ~6.7-7.0K tokens per query; p50 latency 0.88-1.09 s; "single-pass retrieval at top_200", on the **managed platform** with proprietary optimisations; hardware and judge model not stated on the README page [CLAIM-mem0-15]. A second vendor page reports 91.6 on LoCoMo (April 2026) vs 92.5 in the README: internal inconsistency, treated as Unverified [CLAIM-mem0-16]. Paper claims (2025): +26% relative LLM-judge over OpenAI memory, 91% lower p95 latency vs full-context, >90% token saving on LoCoMo [CLAIM-mem0-14]. **LoCoMo is contested**: Zep's rebuttal disputes how Mem0 configured Zep (both speakers as "user", timestamps in message text, sequential search) and reports corrected Zep 75.14% +/-0.17 against Mem0-graph 68.44% under the 2025 setup; Letta disputes Mem0's MemGPT numbers and reports a plain filesystem agent at 74.0% with gpt-4o-mini [CLAIM-mem0-17][CLAIM-mem0-18]. Each side is a vendor with a stake; no independent run with a shared judge exists in the sources found. Resource model (derived): write = 1 LLM call + (1+k) embeddings + 1 top-10 query; read = 1 embedding + 2 index queries + entity lookups. Failure modes: LLM unavailable -> `LLMError`; Qdrant without `fastembed` silently drops BM25 and falls back to semantic-only; missing spaCy silently disables entity boost [CLAIM-mem0-04].

## 8. Strengths and use-case-specific advantages

- Lowest-friction memory API (`add/search/update/delete/history`), 22 vector stores, local-LLM wiring, large adoption.
- v3 write path is cheap and auditable: one call, integer-aliased ids, hash dedup, explicit failure; cheaper than Graphiti's multi-call episodes but gives up temporal reconciliation.
- Entity-linked hybrid retrieval gives a graph-like recall boost without a graph database; `explain=True` score decomposition.

## 9. Limitations with root causes

| Class | Limitation | Type | Evidence |
|---|---|---|---|
| Algorithmic dead-end | ADD-only accumulation: contradictory and stale facts coexist; correctness delegated to ranking | Intentional trade-off (vendor says changed facts "stored alongside older ones, and retrieval ranks them") | CLAIM-04 |
| Algorithmic | Exact-md5 dedup only; no semantic merge, no supersession, no confidence | Verified in code | CLAIM-06 |
| Algorithmic | "Graph memory" is entity co-occurrence; no typed relations, no multi-hop | Verified (docs) | CLAIM-05 |
| Operational | No cross-store atomicity (vector + SQLite history + entity collection) | Hypothesis from code | CLAIM-06 |
| Operational | Expiry is read-time date filter; data persists (GDPR erasure needs explicit delete) | Verified | CLAIM-09 |
| Friction | Typed graph removed from OSS, kept for paying Platform users; headline benchmarks not reproducible with OSS | Licensing/packaging, verified | CLAIM-02, -04 |
| Friction | Telemetry on by default with PostHog as a hard dependency; OpenAI defaults | Verified | CLAIM-10, -11 |
| Friction | Breaking API churn (v2->v3 renames, `version` args ignored); Python/TS version skew | Verified | CLAIM-04 |
| Security | No ACL/tenant/principal model; trust-the-caller scoping | Verified | CLAIM-08 |
| Quality | Benchmark claims contested by two competitors; numbers differ between Mem0's own pages | Contested | CLAIM-16..18 |

## 10. Deployment, licensing, redistribution, operational viability

- **Licence class: permissive (Apache-2.0)**, redistribution-safe for the library; legal review trigger = the **OSS-vs-Platform split** (features gated to Cloud, "proprietary optimizations") and the unfilled copyright line. No patent clause beyond Apache-2.0 s3.
- **Air-gap: partial.** Possible with `MEM0_TELEMETRY=false`, Ollama/vLLM LLM, Ollama/HF/fastembed embedder, local Qdrant/FAISS/pgvector; defaults reach OpenAI and PostHog. Local-model quality for the JSON extraction prompt is untested here (docs only say pick an Ollama model that supports tool calling) [CLAIM-mem0-13].
- **One-node:** yes (library + local Qdrant + SQLite). Server mode needs Postgres/pgvector.
- **Backend neutrality:** Mem0's vector-store set includes Neptune Analytics, pgvector, OpenSearch, but **no HugeGraph/Neo4j graph store in OSS any more**.

## 11. Competitive delta against EOIP verified baseline

| Area | Mem0 | EOIP baseline | Delta |
|---|---|---|---|
| Memory record | vector row with scope + timestamps | `MemoryEntry` (tier, relevance, ttl, tags, metadata, source) in `memory_eng/engine.py`; `Fact` upsert in `reasoning/memory.py` (overwrites); `FileMemoryStore` with `config/memory-policy.yaml` (ttl 30 d, 1000 records, 8 MiB) | EOIP has tiers/decay Mem0 lacks; **both lack ACL/tenant/evidence on memory** (BL-18 Absent, BL-20 Partial) |
| Retrieval | semantic+BM25+entity | RRF hybrid (BL-15), hashing vectors (BL-14) | Add entity-link signal; EOIP RRF is rank-based, Mem0 additive-score |
| Epistemic status | none | PROPOSED-until-validated (BL-40) | EOIP ahead; memory must be routed through it |
| Deletion | explicit + read-time expiry | tombstones (BL-25), revisions (BL-37) | EOIP ahead on non-destructive history |
| Graph memory | removed from OSS | GraphStore protocol (BL-01), GraphRAG retrieval (BL-16) | EOIP can own a typed memory graph on any backend |

## 12. Strength-adoption cards and inversion cards

| ID | Competitor | Strength | Evidence | Value to EOIP | Verdict | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-mem0-01 | Mem0 | Single-call, id-aliased, fail-loud extraction | CLAIM-06 | Cheap, auditable memory writes | match | Extraction adapter: neighbours (top-10, ACL-filtered) shown with integer aliases; one local-model call; hash dedup; failure -> DLQ | 200 synthetic chats: 0 hallucinated ids; LLM outage yields DLQ entries, not empty results |
| STR-mem0-02 | Mem0 | Entity-link boost as a third retrieval signal | CLAIM-07 | Graph-like recall without traversal | match | Add `entity_overlap` to `search/hybrid_engine.py` using identity keys (`identity/resolver.py`) instead of spaCy | nDCG@10 >= RRF alone on EOIP memory eval set (PROPOSED) |
| STR-mem0-03 | Mem0 | `explain=True` per-signal score decomposition | CLAIM-07 | Debuggable recall | exceed | Return per-signal contributions plus ACL decision trace | Every result carries score parts and `acl_decision` |
| STR-mem0-04 | Mem0 | Metadata cannot override scope keys | CLAIM-08 | Anti-spoofing | match | Scope set by gateway from principal, never from payload | Fuzz: payload `tenant_id` ignored in 10k cases |

**INV-mem0-01 — Seed §10.5 "agent-memory systems: LLM-dependent extraction cost/latency" -> PARTIALLY VALIDATED.** Mem0 v3 reduced to one call per add, so the hypothesis holds weakly; the remaining cost is quality (accumulating contradictions). Proven root cause: write-path design (ADD-only). Options: (a) wrap Mem0 as-is; (b) native cascade: rules -> ontology functional-property check -> local model -> external model under egress policy, with non-destructive supersession (see `STR-graphiti-zep-01/-02`); (c) long-term: memory facts as governed graph assertions with evidence and ACL. **Selected (b)->(c).** Benchmark: 100 owner-change facts, success = 100% correct current-value recall without model call; cost baseline = Mem0 1 call/add. Defensibility: ACL+evidence+bitemporal semantics are enterprise-specific. **Decision: ADOPT (pattern), REJECT (runtime dependency).**

**INV-mem0-02 — No principal/ACL/tenant model (proven, governance).** Memory leaks across users if the caller mislabels scope; no per-fact source ACL. Alternative: ACL fields (`acl_hash`, `tenant_id`, `owner`) stored with each memory fact and enforced in the mutation gateway and retrieval filter (extends BL-17 `PermissionMetadata`; closes the memory part of BL-18/BL-20). Worse when: only single-user, single-tenant local use. POC: cross-tenant red-team (J5/J13) 0 leaks in 10k queries incl. entity-index path (the entity collection is a second leak surface). **ADOPT.**

**INV-mem0-03 — Typed graph removed from OSS; graph is platform-only (proven, licensing/packaging).** Alternative: typed memory graph on any `GraphStore` backend (HugeGraph/Neo4j/Neptune), edges carrying evidence, validity, ACL. Quick option: none (nothing to integrate); native: entity-link signal (STR-02); long-term: memory subgraph in meta-graph. Cost baseline: Mem0 entity collection = 1 extra vector collection. **EXPERIMENT.**

**INV-mem0-04 — Default telemetry, OpenAI defaults, benchmark not reproducible in OSS (proven, deployment).** Alternative: egress gateway (BL-45) as the only outbound path; benchmark harness (CAP-78) with fixed judge. **ADOPT** as policy: any adopted third-party memory library must pass an egress-silence test (no DNS/HTTP outside allowlist for 24 h).

**INV-SELF-mem0-01 (EOIP weakness).** Three unconnected memory stores (`memory_eng`, `reasoning/memory.py`, `agents/memory.py`) none with tenant/ACL/evidence fields; `SemanticMemory.upsert` overwrites. Fix: single governed memory-fact store (see C08-graphiti-zep `INV-SELF-graphiti-01`). **ADOPT.**

## 13. Per-capability decisions

| Capability | Decision | Reason |
|---|---|---|
| CAP-57 agent memory write/expire/invalidate | BUILD (EOIP governed store); EXPERIMENT Mem0 as library behind egress for comparison only | no ACL, no supersession |
| CAP-55 hybrid retrieval | REUSE pattern (entity signal, explain) | STR-02/-03 |
| CAP-56 graph memory | BUILD on GraphStore | INV-03 |
| CAP-46 ACL in retrieval/memory | BUILD | INV-02 |
| CAP-61 local model serving | INTEGRATE (Ollama/vLLM through existing abstraction) | – |
| CAP-78 eval harness | BUILD LoCoMo/LongMemEval adapters with fixed judge; never quote vendor numbers | CLAIM-16..18 |
| Mem0 as runtime dependency | DEFER | telemetry, OpenAI defaults, OSS/Platform split, no ACL |

## 14. Concrete tests, POC, acceptance conditions (all PROPOSED; none run)

1. **Egress-silence:** `mem0ai==2.2.1` + Ollama + local Qdrant, `MEM0_TELEMETRY=false`, 24 h packet capture; pass = zero outbound except allowlist; repeat with defaults to confirm PostHog traffic.
2. **Local-model extraction:** 500 LoCoMo-style dialogues, 3 local models (7-14B); fact precision/recall, JSON-parse failure rate vs gpt-5-mini default.
3. **Contradiction handling:** 100 preference changes; share of stale facts in top-5, ADD-only vs EOIP supersession.
4. **Leak test:** two tenants, shared store; crafted filters and entity-store probes; pass = 0 cross-tenant hits.
5. **LoCoMo reproduction** with one fixed judge for Mem0 OSS, Graphiti, EOIP memory, per category (resolves CLAIM-16..18).

## 15. Risks, trade-offs, open research questions

Risks: upstream API churn; platform-only features; benchmark-driven design on a contested benchmark. Open: does ADD-only + hybrid ranking beat supersession on temporal questions at 100k+ memories? What does Platform "native graph memory" store (NOT PUBLICLY VERIFIED)? Self-hosted server tenant model (undocumented)? OpenMemory MCP data locality (not examined)?

---

## Appendix A — Research-dimension coverage

| Dimension | Sections | Summary / N/A reason |
|---|---|---|
| D1 Identity and maturity | 1, 10 | Apache-2.0, active, v2 break 2026-04-14 |
| D2 Problem and workloads | 2 | personalisation memory |
| D3 Architecture | 4, 5 | library/server, 5 stores |
| D4 Storage and indexing | 5 | vector row + entity collection + SQLite |
| D5 Schema/semantics | 5, 9 | schemaless text facts; no typing |
| D6 Query pipeline | 5 | hybrid additive scoring; no query language |
| D7 Reasoning | N/A | none; ranking only |
| D8 Transactions/scale | 5, 7 | no cross-store atomicity; scale via vector store |
| D9 Ingestion/federation | 5 | messages in; no connectors |
| D10 Identity/evidence | 5, 9 | no ER, no evidence spans |
| D11 Time/evolution | 5, 9 | created/updated only; ADD-only |
| D12 Graph algorithms/ML | N/A | none |
| D13 Retrieval/agent integration | 5, 8 | hybrid; memory write/expire/delete rules |
| D14 NL query | N/A | not a query system |
| D15 Governance/authoring | 9 | none; custom_instructions prompt only |
| D16 Human experience | 3 | dashboard in server (details NOT PUBLICLY VERIFIED) |
| D17 Developer experience | 8, 9 | strong SDK; churn |
| D18 Trust/security | 5, 9, 12 | no ACL; telemetry; prompt-injection into memory not addressed (hypothesis) |
| D19 Multi-tenancy/white-label | 5, 12 | caller-filter scoping only |
| D20 Empirical economics | 7 | vendor claims only |
| D21 Commercial/licensing | 1, 10 | OSS vs Platform; pricing not examined |
| D22 Interop/lock-in | 10 | 22 stores; export via `get_all` (hypothesis) |
| D23 IP/prior art | 10 | Apache-2.0 only; no patent search performed |
| D24 Research quality | 7 | contested benchmarks |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-57 agent memory | native (no supersession) | CLAIM-06 | Partial (three unconnected stores) | BUILD | P1 |
| CAP-55 hybrid retrieval | native | CLAIM-07 | BL-15 Implemented | REUSE pattern | P2 |
| CAP-56 GraphRAG/graph memory | absent in OSS (platform-only, untyped) | CLAIM-05 | BL-16 Implemented | BUILD | P2 |
| CAP-53 vector search | native via 22 stores | CLAIM-12 | BL-14 Partial | DEFER (see C10) | P2 |
| CAP-46 ACL in retrieval | absent | CLAIM-08 | BL-18 Absent | BUILD | P0 |
| CAP-47 tenant isolation | absent | CLAIM-08, -11 | BL-20 Partial | BUILD | P0 |
| CAP-43 epistemic separation | absent | CLAIM-06 | BL-40 | BUILD | P1 |
| CAP-38 provenance/evidence | absent | CLAIM-06 | BL-41 | BUILD | P1 |
| CAP-51 egress control | absent (telemetry on) | CLAIM-10 | BL-45 | BUILD | P0 |
| CAP-61 local models | partial | CLAIM-13 | BL-45 | INTEGRATE | P2 |
| CAP-78 eval harness | external (memory-benchmarks repo, vendor) | CLAIM-15 | Absent | BUILD | P2 |

## Appendix C — Evidence records

| CLAIM-ID | Product/version/date | Exact claim | Class | Source + URL | Pub/access | Confidence + rationale | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-mem0-01 | mem0ai 2.2.1, 2026-09-25 | Latest PyPI release 2.2.1 on 2026-09-25; Apache-2.0; prior 2.2.0 09-23, 2.1.0 09-18, 2.0.20 09-02, 2.0.19 08-24; extras dev/extras/llms/nlp/test/vector-stores | Officially documented | PyPI mem0ai https://pypi.org/project/mem0ai/ | 2026-09-25 / 2026-10-26 | 0.9 registry | none |
| CLAIM-mem0-02 | repo main | Apache 2.0; 67.8k stars; Library / Self-Hosted Server / Cloud table; benchmark scores reflect platform with proprietary optimisations not in OSS SDK; LICENSE appendix copyright line is template text | Officially documented | https://github.com/mem0ai/mem0 and /blob/main/LICENSE | n/a / 2026-10-26 | 0.85 | none |
| CLAIM-mem0-03 | Py 2.0.0 / TS 3.0.0 | 2026-04-14 "New Memory Algorithm": ADD-only extraction; external graph stores removed from OSS | Officially documented | Mem0 changelog https://docs.mem0.ai/changelog | 2026-04-14 / 2026-10-26 | 0.85 | none |
| CLAIM-mem0-04 | OSS v3 | Graph store config (`enable_graph`, `graph_store`) removed, not replaced; `relations` not returned; add() returns ADD only; top_k 100->20, threshold ->0.1, rerank default False; BM25 needs fastembed on Qdrant, entity matching needs `mem0ai[nlp]`, else silent semantic-only fallback; changed facts stored alongside old ones | Officially documented | https://docs.mem0.ai/migration/oss-v2-to-v3 | n/a / 2026-10-26 | 0.85 | none |
| CLAIM-mem0-05 | graph memory docs | Graph memory now native/built-in; "does not assign typed, labeled relationships"; links memories sharing an entity; older store list Neo4j, Memgraph, Kuzu, AGE, Neptune | Officially documented | https://docs.mem0.ai/open-source/features/graph-memory | n/a / 2026-10-26 | 0.8 (fetched through summariser) | Platform behaviour NOT PUBLICLY VERIFIED |
| CLAIM-mem0-06 | 2.2.1 wheel | `_add_to_vector_store`: infer=False stores verbatim; else last-10 messages, top-10 neighbours, integer id aliasing, single LLM call (json_object), LLMError on failure, md5 hash dedup, batch embed/insert, history; SQLite `history` and `messages` tables; payload fields data/hash/text_lemmatized/scope ids/timestamps | Observed in source code | mem0/memory/main.py:881-1060, storage.py in wheel https://files.pythonhosted.org/packages/aa/48/7051dd9009232802c11a4c4d9e58ea32968c8e076ea79e2e8a6d243e49b3/mem0ai-2.2.1-py3-none-any.whl | 2026-09-25 / 2026-10-26 | 0.9 | none |
| CLAIM-mem0-07 | 2.2.1 wheel | Search = semantic top max(4*limit,60) + keyword BM25 (sigmoid-normalised) + entity boost; additive score divided by max_possible (1.0/2.0/2.5/1.5); threshold gates semantic score | Observed in source code | main.py:1642-1700, utils/scoring.py | 2026-09-25 / 2026-10-26 | 0.9 | none |
| CLAIM-mem0-08 | 2.2.1 wheel | Scope via user_id/agent_id/run_id/actor_id filters; identity keys in metadata dropped; ids validated and trimmed; delete_all needs >=1 filter; no principal/ACL code in package (grep of main.py structure) | Observed in source code | main.py:314-420, 1904-1960 | 2026-09-25 / 2026-10-26 | 0.8 (absence of ACL inferred from structure and function list, not a full grep of all files) | none |
| CLAIM-mem0-09 | 2.2.1 / docs | `expiration_date` YYYY-MM-DD; expired hidden from search/get_all unless show_expired; get by id still returns; `infer=False` can duplicate | Officially documented + source | https://docs.mem0.ai/core-concepts/memory-operations/add ; main.py:427-460 | n/a / 2026-10-26 | 0.9 | none |
| CLAIM-mem0-10 | 2.2.1 wheel | `MEM0_TELEMETRY` default "True"; posthog is a core dependency; hot-path sampling 0.1 | Observed in source code | memory/telemetry.py:14-45; wheel METADATA | 2026-09-25 / 2026-10-26 | 0.9 | none |
| CLAIM-mem0-11 | OSS docs | Defaults gpt-5-mini + text-embedding-3-small; server = Docker Compose, Postgres/pgvector, dashboard; auth on by default (JWT or X-API-Key; AUTH_DISABLED for dev); no multi-tenant model described | Officially documented | https://docs.mem0.ai/open-source/overview ; /open-source/features/rest-api | n/a / 2026-10-26 | 0.8 | none |
| CLAIM-mem0-12 | docs | 22 Python vector stores; Qdrant default | Officially documented | https://docs.mem0.ai/components/vectordbs/overview | n/a / 2026-10-26 | 0.85 | wheel lists additional stores (baidu, azure_mysql, cassandra) |
| CLAIM-mem0-13 | 2.2.1 wheel / docs | LLM modules: ollama, vllm, lmstudio, litellm, etc.; embedders: ollama, huggingface, lmstudio, fastembed; Ollama doc: models must support tool calling | Observed in source + docs | wheel `llms/`, `embeddings/`; https://docs.mem0.ai/components/llms/models/ollama | 2026-10-26 | 0.85 | local extraction quality unmeasured |
| CLAIM-mem0-14 | arXiv:2504.19413 v1 | Abstract: +26% relative LLM-judge vs OpenAI, graph variant ~2% over base, 91% lower p95 latency vs full-context, >90% token saving, evaluated on LOCOMO | Unverified (author preprint, vendor claim) | https://arxiv.org/abs/2504.19413 | 2025-04-28 / 2026-10-26 | 0.4 as performance evidence (vendor, contested) | CLAIM-17, -18 |
| CLAIM-mem0-15 | README 2026 | LoCoMo 92.5, LongMemEval 94.4, BEAM 1M 64.1 / 10M 48.6; ~7K tokens; p50 0.88-1.09 s; single-pass top_200; platform | Unverified (vendor claim) | https://github.com/mem0ai/mem0 | n/a / 2026-10-26 | 0.25 | CLAIM-16 gives 91.6 |
| CLAIM-mem0-16 | Mem0 comparison page | LoCoMo 91.6 (April 2026) vs Zep 80.32; Mem0 notes active methodology dispute | Unverified (vendor, via search summary; page not fetched directly) | https://mem0.ai/blog/zep-vs-mem0-which-ai-memory-layer-should-you-choose | n/a / 2026-10-26 | 0.2 | CLAIM-15, -17 |
| CLAIM-mem0-17 | Zep blog | Zep says Mem0 mis-configured Zep (both roles "user", timestamps in text, sequential search); corrected Zep 75.14%+/-0.17 vs Mem0 graph 68.44%, base 66.88%; admits earlier miscalculation; p95 0.632 s | Third-party report (competitor) | https://www.getzep.com/blog/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/ | 2025-05-06 / 2026-10-26 | 0.45 | page meta says 24%, body 10% |
| CLAIM-mem0-18 | Letta blog | Letta filesystem agent 74.0% on LoCoMo (gpt-4o-mini); Mem0 graph 68.5% cited; says Mem0's MemGPT numbers not reproducible | Third-party report (competitor) | https://www.letta.com/blog/benchmarking-ai-agent-memory | 2025-08-12 / 2026-10-26 | 0.4 | Mem0 numbers not independently checked |

## Appendix D — Assumptions

1. "Mem0" = `mem0ai/mem0` and its Platform; OpenMemory MCP excluded.
2. ACL absence is judged from the scoping code and function inventory, not a full-text audit.
3. Versions come from PyPI and the changelog (GitHub API rate-limited). The wheel was read, never executed.
