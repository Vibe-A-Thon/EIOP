# C08 — Zep and Graphiti (temporal context graph for agent memory)

| Field | Value |
|---|---|
| Registry ID | T-C08-graphiti-zep |
| Tier | A — temporal agent-memory graph; direct competitor for CAP-57/CAP-34 and target of Master Prompt §10.5 seed hypothesis "Graphiti / agent-memory systems" |
| Versions examined | `graphiti-core` 0.31.1 (PyPI upload 2026-10-15, wheel inspected); Graphiti MCP server README at `main` (2026-10-18); Zep Cloud (managed, SDK `zep-cloud` 4.0.0, PyPI 2026-10-14); Zep Community Edition (deprecated 2025-04-02); Zep paper arXiv:2501.13956 v1 (2025-01-20) |
| Verified on | 2026-10-18 (sources accessed 2026-10-18/19) |
| Worker | W20 |

## 1. Identity, current status, tier, and sources

- **Graphiti** — open-source Python framework (`getzep/graphiti`, PyPI `graphiti-core`) that builds and queries *temporal context graphs* from "episodes" using LLM extraction, storing them in a third-party graph database [CLAIM-graphiti-zep-01]. Licence **Apache-2.0** (licence file and PyPI licence expression) [CLAIM-graphiti-zep-02]. Latest release 0.31.1 (2026-10-15); release cadence roughly monthly with patch releases (0.29.1 2026-05-21 → 0.29.2 06-08 → 0.29.3 07-27 → 0.30.1 09-01 → 0.30.2 09-08 → 0.31.1 10-15) [CLAIM-graphiti-zep-01]. Status: **active**, pre-1.0 (API churn expected).
- **Zep** — Zep Software Inc.'s commercial "context infrastructure": managed users/threads/graphs, a context-block assembler and a **proprietary graph database ("Context Graph Engine")** underneath; Graphiti is described as the open-source core [CLAIM-graphiti-zep-18]. Deployment: Zep Cloud, Cloud + customer-managed keys (BYOK), and **Bring Your Own Cloud (in the customer's VPC)** for Enterprise; credit-metered per ingested episode [CLAIM-graphiti-zep-19].
- **Zep Community Edition** — **deprecated** on 2025-04-02; repository remains under Apache-2.0 but receives no updates or support; Zep recommends Zep Cloud or Graphiti instead [CLAIM-graphiti-zep-17]. Trap resolved: "Zep open source" today means **Graphiti**, not a self-hostable Zep server.
- Name collisions: unrelated GitHub projects named "zep" (e.g. a text editor `khiner/zep`) are out of scope.
- Sources used (14): PyPI JSON for `graphiti-core`, `zep-cloud`, `zep-python`; Graphiti README and LICENSE; Graphiti MCP README; Graphiti 0.31.1 wheel source (`edges.py`, `nodes.py`, `graphiti.py`, `utils/maintenance/edge_operations.py`, `search/*`, `driver/*`, `llm_client/*`); Zep CE deprecation blog and help page; Zep pricing page; Zep concepts page; arXiv:2501.13956; Zep LoCoMo rebuttal blog; Mem0 comparison page; third-party LoCoMo audit report (low trust). See Appendix C.

## 2. Primary problem, target workloads, concrete example workflows

Problem: agents need memory that (a) updates incrementally as conversations and business data arrive, (b) knows *when* a fact was true and when it was superseded, and (c) retrieves relevant facts in sub-second time without an LLM in the read path. Graphiti positions itself against batch GraphRAG (community summarisation at index time) [CLAIM-graphiti-zep-31].

Workloads: per-user conversational memory (Zep "user graphs"), shared domain graphs (`graph_uuid`) [CLAIM-graphiti-zep-23], ingestion of JSON business records as episodes, MCP memory for coding assistants (Claude Desktop / Cursor via the MCP server) [CLAIM-graphiti-zep-10].

Example workflows:
1. *Preference drift*: episode 1 "Kendra loves Adidas" → edge `LOVES(Kendra, Adidas)` valid_at = episode reference time; episode 2 "Kendra switched to Nike" → LLM flags edge 1 as contradicted → edge 1 gets `invalid_at = valid_at(edge 2)` and `expired_at = now`; both remain queryable [CLAIM-graphiti-zep-05][CLAIM-graphiti-zep-06].
2. *Structured JSON*: CRM export ingested with `source=json`; entity/edge types constrained by Pydantic models and an `edge_type_map` [CLAIM-graphiti-zep-24].
3. *Agent context*: before each turn, hybrid search (BM25 + cosine + BFS around a centre node, reranked by RRF / node distance / cross-encoder) returns facts with validity dates; Zep packs them into a "context block" [CLAIM-graphiti-zep-07][CLAIM-graphiti-zep-23].
4. *Provenance*: `get_episode_entities` returns nodes/edges created by a given episode [CLAIM-graphiti-zep-10].

EOIP relevance: EOIP's J2 (evolving organisational truth), J5 (permission-aware memory) and J6 (deterministic first) are exactly the axes on which Graphiti is strong (bitemporal invalidation) and weak (LLM-first, no ACL).

## 3. Feature inventory

| Feature | Graphiti OSS 0.31.1 | Zep Cloud | Evidence |
|---|---|---|---|
| Episode ingestion (text, message, JSON) | present | present | CLAIM-01, -10 |
| Bulk ingestion (`add_episode_bulk`) | present (skips some invalidation semantics — hypothesis) | present | CLAIM-28 |
| Direct triplet insert bypassing LLM (`add_triplet`) | present | unknown | CLAIM-30 |
| Bitemporal edges (`valid_at`/`invalid_at` + `created_at`/`expired_at`) | present | present | CLAIM-05 |
| LLM contradiction detection + deterministic temporal invalidation | present | present | CLAIM-06 |
| Entity resolution (exact-name/identity-property fast paths, embedding candidates, LLM judge) | present | present | CLAIM-28 |
| Custom entity/edge types (Pydantic), edge-type signatures | present | present | CLAIM-24 |
| Hybrid search: BM25, cosine, BFS; RRF/MMR/node-distance/episode-mentions/cross-encoder rerank | present | present (pre-configured) | CLAIM-07 |
| Temporal filters on search (valid/invalid/created/expired) | present (opt-in) | partial (documented as facts with dates) | CLAIM-27 |
| Communities (label propagation + LLM summaries) | optional | unknown | §5 |
| Sagas (episode chains with running summary) | present | unknown | CLAIM-28 |
| Graph backends | Neo4j 5.26, FalkorDB 1.1.2 (+ embedded FalkorDB Lite), Neptune DB/Analytics + OpenSearch Serverless, Kùzu (deprecated) | proprietary engine | CLAIM-03, -04, -18 |
| LLM providers | OpenAI default; Anthropic, Gemini, Groq, Azure; any OpenAI-compatible (Ollama, vLLM, llama.cpp) | managed | CLAIM-12 |
| Local NER (GLiNER2, CPU) | optional | n/a | CLAIM-14 |
| Per-prompt model routing, prompt overrides | present | n/a | CLAIM-29 |
| MCP server | present, **experimental, no authn/authz** | Zep MCP: unknown | CLAIM-10 |
| REST server (FastAPI) | present (sample) | managed API | CLAIM-01 |
| Users, threads, context block, dashboards | absent (build your own) | present | CLAIM-18, -23 |
| Multi-tenancy | `group_id` partition (separate graph on FalkorDB only) | projects/users; isolation model NOT PUBLICLY VERIFIED | CLAIM-08, -23 |
| Source-ACL / per-fact permissions | **absent** | not described | CLAIM-23 |
| Delete episode (cascade) / delete edge / clear group | present | present (not on concepts page) | CLAIM-16, -10 |
| Telemetry | PostHog, **opt-out** | n/a | CLAIM-11 |
| SOC 2 Type II, HIPAA BAA | n/a | present (Enterprise) | CLAIM-19 |
| Air-gapped deployment | possible with Neo4j/FalkorDB + local LLM + telemetry off | **absent** (BYOC still a Zep-operated VPC deployment) | CLAIM-19 |

## 4. Text-based architecture diagram

```
                ┌──────────────────────── Graphiti process (Python, asyncio) ─────────────────────────┐
 episode ──────►│ add_episode(name, body, source, reference_time, group_id, entity_types, edge_types)  │
 (text/json/msg)│   1 retrieve previous N episodes (context)                ── graph read             │
                │   2 extract_nodes (LLM | GLiNER2)  ── LLM ──► provider (OpenAI / Ollama / …)        │
                │   3 resolve nodes: exact name / identity props → embeddings → dedupe_nodes (LLM)    │
                │   4 extract_edges (LLM, typed by edge_type_map)                                    │
                │   5 per edge: fast path exact-fact match → else resolve_edge (LLM: duplicate idx,   │
                │     contradiction idx) → extract_timestamps (LLM) → attributes (LLM)               │
                │   6 _apply_temporal_invalidation (deterministic date compare) → expire old edges   │
                │   7 summaries/attributes for nodes (LLM); optional communities; saga links         │
                │   8 embed (embedder) → add_nodes_and_edges_bulk  ── graph write                    │
                │ search(query, group_ids, center_node, filters) → BM25 ∥ cosine ∥ BFS → rerank      │
                └────────────┬─────────────────────────────────────────────┬──────────────────────────┘
                 data plane  │ Cypher / openCypher                          │ control: env vars, SEMAPHORE_LIMIT,
                             ▼                                              │ LLMRuntime routes, telemetry (PostHog)
   ┌──────────── GraphDriver ────────────┐                                   ▼
   │ Neo4j │ FalkorDB(+Lite) │ Neptune + │                          MCP server (HTTP /mcp/ or stdio,
   │       │ graph per group │ OpenSearch│                          queue per group, NO authn/authz)
   │       │                 │ Serverless│ Kùzu (deprecated)
   └───────┴─────────────────┴───────────┘
 Zep Cloud = users/threads/context-block service + proprietary Context Graph Engine (managed or BYOC VPC)
```

State: all durable state is in the graph DB (Episodic, Entity, Community, Saga nodes; MENTIONS, RELATES_TO, HAS_MEMBER, HAS_EPISODE, NEXT_EPISODE edges); optional on-disk LLM response cache (`./llm_cache`) [CLAIM-graphiti-zep-26]. No separate vector store: embeddings are node/edge properties indexed by the backend (or OpenSearch for Neptune) [CLAIM-graphiti-zep-03].

## 5. Under-the-hood reconstruction

**Data model** (observed, `edges.py`, `nodes.py` at 0.31.1) [CLAIM-graphiti-zep-05]:
- `Node{uuid, name, group_id, labels, created_at}`; `EpisodicNode{content, source, source_description, valid_at (= reference time), entity_edges[]}`; `EntityNode{summary, name_embedding, attributes}`; `CommunityNode`, `SagaNode`.
- `Edge{uuid, group_id, source_node_uuid, target_node_uuid, created_at}`; `EntityEdge{name, fact, fact_embedding, episodes[], valid_at, invalid_at, expired_at, reference_time, attributes}`.
- Bitemporality: **valid time** = `valid_at`/`invalid_at` (when the fact was true in the world, LLM-extracted relative to the episode reference time); **transaction time** = `created_at`/`expired_at` (when the system learned / retired it). Facts are never overwritten by invalidation, only closed [CLAIM-graphiti-zep-05][CLAIM-graphiti-zep-06].
- Provenance: `EntityEdge.episodes` lists episode UUIDs; `MENTIONS` edges link episodes to entities. The raw episode text can be blanked with `store_raw_episode_content=False` [CLAIM-graphiti-zep-25].

**Write pipeline** (observed; LLM prompt call sites enumerated in `utils/maintenance/*`: `extract_nodes_and_edges.extract_message`, `extract_edges.edge`, `dedupe_nodes.nodes`, `dedupe_edges.resolve_edge`, `extract_edges.extract_timestamps(_batch)`, `extract_*.extract_attributes`, `summarize_nodes.*`, `summarize_sagas.*`) [CLAIM-graphiti-zep-28]:

```
add_episode(ep):
  ctx   = last_n_episodes(ep.group_id)                      # graph read
  nodes = LLM.extract_nodes(ep, ctx, entity_types)           # or GLiNER2 locally (NER only)
  for n in nodes:                                            # entity resolution
      cand = exact_name(n) ∪ identity_props(n) ∪ ann(n.name_embedding)
      n'   = deterministic_match(n,cand) or LLM.dedupe_nodes(n,cand)
  edges = LLM.extract_edges(ep, nodes', edge_type_map)
  for e in edges:
      same_pair = edges_between(e.src,e.dst); related = ann(e.fact_embedding, group)
      if exact_fact_match(e, same_pair): e = existing; append episode; continue
      dup_idx, contra_idx = LLM.resolve_edge(e, same_pair, related)   # one structured call
      LLM.extract_timestamps(e, ep.reference_time)                    # valid_at / invalid_at
      invalidated += temporal_invalidation(e, related[contra_idx])    # deterministic
  LLM.summaries(nodes'); embed(all); bulk_write(ep, nodes', edges, invalidated)
```

`temporal_invalidation` (observed, `edge_operations.py:715-783`): if the new edge already has `invalid_at` it is born expired; if a contradicting candidate starts *later*, the new edge is closed at the candidate's `valid_at`; otherwise each contradicting candidate that started *earlier* gets `invalid_at = new.valid_at`, `expired_at = now`; non-overlapping intervals are left alone [CLAIM-graphiti-zep-06]. Key design point: **the LLM decides "is this a contradiction"; code decides "which interval closes"**. EOIP can reuse this split with a deterministic contradiction detector for typed functional properties (e.g. `OWNED_BY` cardinality 1) and reserve the LLM for free-text facts.

**Storage layout and indexing**: delegated to the backend. Graphiti creates range indexes on uuid/group_id and full-text plus vector indexes per provider (`build_indices_and_constraints`); Neptune needs Amazon OpenSearch Serverless for full-text [CLAIM-graphiti-zep-03]. Physical layout is the backend's (Neo4j native store, FalkorDB sparse matrices) — not Graphiti's.

**Query pipeline**: `search()` → validate `group_ids` → embed query → run configured methods in parallel (edge/node BM25, cosine, BFS to `bfs_max_depth`; episode BM25; community BM25/cosine) → rerank (RRF default; MMR λ; node distance from `center_node_uuid`; episode-mention frequency; cross-encoder via OpenAI/Gemini log-probs or local BGE reranker) → top-k [CLAIM-graphiti-zep-07]. No LLM on the read path unless a cross-encoder reranker that is an LLM is configured. **No default filter excludes expired facts**; callers pass `SearchFilters(invalid_at/expired_at …)` or rely on dates in the returned fact [CLAIM-graphiti-zep-27]. Empty `group_ids` becomes "no group filter" (`search.py:155-156`) [CLAIM-graphiti-zep-09].

**Reasoning**: none symbolic. Communities via label propagation over the entity projection with LLM summaries (`community_operations.py:82,96`). Edge-type signatures are enforced against `edge_type_map` (`enforce_edge_type_signatures`) — a light schema check, not SHACL.

**Concurrency and transactions**: async with a global semaphore (`SEMAPHORE_LIMIT`, default 10) to avoid LLM 429s; the docs say episodes for one graph should be added **sequentially** and processed in a background queue [CLAIM-graphiti-zep-13]. Bug #1676 (concurrent `group_id`s mutating a shared driver and writing to the wrong database) was fixed by request-scoped driver clones — evidence that partitioning is application-level and fragile [CLAIM-graphiti-zep-33]. No multi-statement transaction wraps an episode; a crash between LLM steps and `bulk_write` loses the episode (hypothesis; no outbox/replay found).

**Partitioning / tenancy**: `group_id` (regex `^[a-zA-Z0-9_-]+$`) is a property on every node/edge; on FalkorDB `driver.clone(database=group_id)` puts each group in its own graph; the base `GraphDriver.clone` returns `self`, so on Neo4j/Neptune/Kùzu groups are **property filters in one database** [CLAIM-graphiti-zep-08].

**Caching**: optional disk cache of LLM responses keyed by prompt (`llm_client/cache.py`) [CLAIM-graphiti-zep-26]; no retrieval cache.

**Versioning**: valid/transaction time on edges only; nodes have `created_at` and evolving summaries (summary history is overwritten — observed by absence of summary versioning; hypothesis-level 0.6). No branch/merge, no graph snapshots.

**Deletion**: `remove_episode` deletes edges whose *first* episode is the removed one and entities mentioned only by it (`graphiti.py:2164-2192`); it does **not** re-open edges that the removed episode had invalidated (no such logic present) [CLAIM-graphiti-zep-16]. For GDPR-style erasure, `clear_graph`/`delete_by_group_id` remove a whole partition.

**Security**: no authentication, authorisation or ACL model in the library; the MCP server explicitly "has no authentication or authorization, and any caller can read, change, or delete all graph data" [CLAIM-graphiti-zep-10]. Zep Cloud: SOC 2 Type II, BYOK, BAA; internal isolation NOT PUBLICLY VERIFIED [CLAIM-graphiti-zep-19].

## 6. Functional and non-functional requirements inferred

- FR: every derived fact must carry episode provenance and four timestamps; invalidation closes intervals, never deletes [CLAIM-05/06].
- FR: entity resolution must try deterministic keys before semantic/LLM matching (Graphiti's exact-name and identity-property fast paths) [CLAIM-28].
- FR: typed ontology optional but enforceable at write (edge-type signatures) [CLAIM-24].
- FR: read path must be LLM-free and hybrid (lexical + vector + graph proximity) [CLAIM-07].
- NFR: ingestion is throughput-bound by LLM rate limits; must run asynchronously off the request path [CLAIM-13].
- NFR: extraction quality depends on reliable structured output; small local models degrade it [CLAIM-12].
- NFR (gap for EOIP): partition key must be mandatory on every read; Graphiti treats missing `group_ids` as "all" [CLAIM-09].

## 7. Performance and resource model

- **Vendor-reported (Zep paper, 2025-01)**: DMR 94.8% vs MemGPT 93.4%; LongMemEval accuracy improvement "up to 18.5%" and "90%" response-latency reduction versus full-context baselines [CLAIM-graphiti-zep-20]. Classification: vendor-authored paper, not independently reproduced; DMR is a small, saturated benchmark.
- **LoCoMo (contested)**: Mem0's paper reported Zep 65.99% (J), Mem0-graph 68.44%, full-context 72.90%; Zep's rebuttal (2025-05-06, later corrected) claims 75.14% ± 0.17 with a "correct" integration and p95 search 0.632 s from AWS us-west-2 [CLAIM-graphiti-zep-21]. Mem0's later pages claim much higher numbers for its 2026 algorithm and cite Zep at 62–83% "depending on settings" [CLAIM-graphiti-zep-21]. A vendor-run audit (Penfield Labs, via a third-party article) reported 99 score-corrupting errors in 1,540 LoCoMo questions and a judge accepting 62.81% of deliberately wrong answers [CLAIM-graphiti-zep-22]. **Treat all LoCoMo numbers as contested vendor claims.**
- **Latency claims**: Graphiti "typically sub-second" retrieval; Zep "sub-200ms performance at scale" — vendor claims without published hardware/dataset [CLAIM-31/32].
- **Cost model (reasoned from code)**: per episode ≈ 1 node-extraction call + 0–N node-dedupe calls + 1 edge-extraction call + per new edge up to {resolve_edge, timestamps, attributes} calls + per touched node a summary call. For an episode yielding *E* new edges and *N* entities with ambiguous matches, LLM calls ≈ 2 + N_amb + 2–3·E + N_sum. Zep's own pricing meters ingestion (1 credit per 350 bytes) and leaves retrieval unmetered, consistent with ingestion being the dominant cost [CLAIM-graphiti-zep-19].
- **Footprint**: Graphiti process is light; resource load sits in the graph DB, embedding model and LLM. On one node with Ollama, the LLM dominates (GPU strongly preferred; CPU-only 7–8B models give minutes-per-episode latencies — hypothesis, untested).
- **Failure modes**: 429 rate limiting; schema-invalid JSON from small models → extraction failure [CLAIM-12]; wrong-database writes under concurrency (fixed, #1676) [CLAIM-33]; silent cross-group reads when `group_ids` omitted [CLAIM-09]; deleted episodes leave stale invalidations [CLAIM-16].

## 8. Strengths and how to match or exceed them

1. **Bitemporal fact edges with non-destructive invalidation** — the cleanest public implementation of valid-time + transaction-time on LLM-derived facts. EOIP already has application-level bitemporal revisions (BL-37) and claims/contradictions (BL-39); *match* by attaching the same four timestamps to memory facts and agent claims, *exceed* by doing invalidation through the governed mutation path with evidence and approval states (BL-40).
2. **LLM-decides-contradiction / code-decides-interval split** — reusable pattern; exceed with deterministic contradiction for functional properties from the ontology.
3. **Deterministic-first entity resolution fast paths** — adopt into EOIP identity (BL-34) for memory entities.
4. **LLM-free hybrid retrieval with graph-distance reranking** — EOIP has RRF (BL-15) and graph-first retrieval (BL-16); add node-distance and episode-mention rerankers.
5. **Backend pluggability (Neo4j, FalkorDB, Neptune)** — overlaps EOIP's Neo4j/Neptune adapters; Graphiti does *not* support HugeGraph or Gremlin.
6. **Developer ergonomics**: Pydantic ontology, prompt overrides, per-prompt model routing, MCP server.

## 9. Limitations with root causes

Verified defects / risks (source-observed): no authn/authz on MCP server [CLAIM-10]; empty `group_ids` = global search [CLAIM-09]; no restore of invalidated edges on episode deletion [CLAIM-16]; concurrency bug #1676 (fixed) [CLAIM-33].
Intentional trade-offs: LLM in the write path for extraction, dedupe, contradiction and dating [CLAIM-28]; sequential per-graph ingestion [CLAIM-13]; OpenAI default; PostHog telemetry opt-out [CLAIM-11].
Licensing: Graphiti Apache-2.0 (clean). Zep engine proprietary; Zep CE abandoned [CLAIM-17/18].
User-reported / contested: LoCoMo comparisons disputed among Zep, Mem0, Letta [CLAIM-21/22].
Outdated claims: "Zep open source" (CE) — outdated since 2025-04; Kùzu backend — deprecated [CLAIM-04].

Root causes:
- *Algorithmic dead-ends*: contradiction detection by LLM over embedding-retrieved candidates is recall-bounded by the candidate search (facts outside top-k are never invalidated) and non-deterministic across model versions (hypothesis, 0.6). Valid-time extraction from text is inherently ambiguous (the code has special rules for future tense and soft deadlines, `edges.py` field descriptions).
- *Operational overhead*: per-episode multi-call LLM pipeline → cost, latency, rate limits; Neptune path needs OpenSearch Serverless (cloud-only).
- *Developer friction*: tenancy and permissions left to the integrator; pre-1.0 API churn; small local models fail structured output.

## 10. Deployment, licensing, redistribution, and operational viability under EOIP constraints

| Constraint | Graphiti | Zep Cloud |
|---|---|---|
| Air-gap | **Viable**: Neo4j or FalkorDB (or FalkorDB Lite embedded) + Ollama/vLLM via `OpenAIGenericClient` + local embedder + `GRAPHITI_TELEMETRY_ENABLED=false`; do not use Jev (hosted by TypeSafe; sends dedupe prompt content) [CLAIM-11][CLAIM-12][CLAIM-15] | Not viable (managed / BYOC VPC) |
| Egress policy | Must route all LLM calls through EOIP egress gateway (BL-45); default config calls OpenAI | Data leaves to Zep |
| Backend neutrality | Neo4j and Neptune overlap EOIP; HugeGraph/JanusGraph unsupported (Cypher-only driver set) | n/a |
| Permissions | absent | not described |
| Licence | Apache-2.0 — redistribution/OEM permitted with notices; `posthog` is a hard dependency (MIT) | proprietary SaaS terms |
| Legal-review trigger | Low (Apache-2.0 patent grant); FalkorDB backend is **SSPL-licensed** — trigger if bundled (cross-ref W04) | Yes, if ever embedded (proprietary) |

## 11. Competitive delta against the EOIP verified baseline

EOIP has **no BL-ID dedicated to agent memory** in `01-SYSTEM-BASELINE.md`; the closest are BL-37 (bitemporal revisions), BL-39 (claims/contradictions, in-memory `TruthStore`), BL-40 (epistemic separation contract), BL-47 (read-only MCP), BL-52 (in-process mutation streaming), BL-18 (source-ACL enforcement **absent**), BL-20 (tenancy contract only). Code inspected for this comparison:

- `packages/eoip/agents/memory.py` `FileMemoryStore` + `config/memory-policy.yaml` (`ttl_seconds: 2592000`, `max_records: 1000`, `max_bytes: 8388608`): records keyed by `(memory_id, scope, owner)`; only `kind=TASK`, classification PUBLIC/INTERNAL, `deletion_policy=DELETE_AT_EXPIRY`, mandatory provenance refs, immutable until delete/expiry, TTL ≤ 30 days, atomic file writes under OS lock; content restricted to `{status, evidence_count}`; written only for agents with `memory_policy="APPROVED"` (`agents/runtime.py:460-477`). **Stronger than Graphiti on governance** (minimisation, mandatory expiry, owner scoping) but stores no facts at all.
- `packages/eoip/memory_eng/engine.py`: in-process tiers (working…procedural), decay functions, consolidation by access count; no tenant, owner, ACL or persistence.
- `packages/eoip/reasoning/memory.py`: `TemporalMemory` (valid-time only, no transaction time, no invalidation), `SemanticMemory` (confidence-wins upsert on (subject,predicate) — destructive overwrite).
- `packages/eoip/moonshot/streaming_agent_memory.py`: dual timeline (event/ingestion time) with a `ConflictResolver` that is last-writer/salience-wins on the same `event_id` — no semantic contradiction detection.
- `packages/eoip/graph/memory.py` is `MemoryGraphStore`, the in-process *graph store*, not agent memory (the registry note pairing it with memory is a naming coincidence).

| Axis | Graphiti/Zep | EOIP | Delta |
|---|---|---|---|
| Fact memory with valid+transaction time | native [CLAIM-05] | BL-37 for graph revisions; memory stores valid-time only | Competitive deficit for agent memory |
| Contradiction → invalidation | LLM + deterministic intervals [CLAIM-06] | BL-39 claims/contradictions (manual/rule), not wired to memory | Partial |
| Memory expiry/TTL, minimisation | none built in | `FileMemoryStore` mandatory TTL, classification gate | **EOIP ahead** |
| Owner/tenant scoping on read | `group_id`, optional, global if omitted [CLAIM-09] | `(scope, owner)` mandatory on get/delete; tenant not in key; BL-20 partial | EOIP ahead on owner; both weak on tenant |
| Source-ACL re-check on read | absent | absent (BL-18) | Shared P0 gap |
| Deterministic extraction | partial (GLiNER2 NER, exact fast paths) | profiling + connectors deterministic (BL-26, BL-23) | EOIP ahead for structured sources |
| MCP memory tools | read/write/delete, no auth [CLAIM-10] | read-only by design (BL-47) | EOIP safer; lacks governed write |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

**STR-graphiti-zep-01** | Graphiti | Four-timestamp fact edges with non-destructive invalidation | CLAIM-05, -06 | J2 as-of answers for agent memory and org truth | **match/exceed** | Extend `MemoryRecord` → `MemoryFact{subject, predicate, object, valid_from, valid_to, recorded_at, retired_at, evidence_refs, acl_hash, tenant_id, epistemic_status}` persisted through the governed mutation path; reuse `graph/bitemporal.py` | Ingest A then contradicting B: as-of(t<B) returns A, as-of(now) returns B, A has `retired_at`; zero physical deletes.

**STR-graphiti-zep-02** | Graphiti | Split "is it contradictory" (model) from "which interval closes" (code) | CLAIM-06 | Deterministic, auditable invalidation | **match/exceed** | Contradiction detectors in priority: ontology functional-property cardinality → rule catalog → local model → external LLM only under egress policy; interval closure always deterministic and logged as a `ResolutionDecision` (BL-39) | 100 synthetic owner changes: 100% closed deterministically without a model call; free-text contradictions measured for precision/recall.

**STR-graphiti-zep-03** | Graphiti | LLM-free hybrid retrieval with graph-distance and mention-frequency rerankers | CLAIM-07 | Low-latency agent context | **match** | Add `node_distance` and `evidence_mentions` rerankers to `search/hybrid_engine.py` alongside RRF | BM-style test: nDCG@10 not worse than RRF alone on EOIP eval set; p95 < 300 ms at 1M edges (PROPOSED).

**STR-graphiti-zep-04** | Graphiti | Deterministic-first entity resolution (exact name, identity properties) before embeddings/LLM | CLAIM-28 | Fewer model calls, stable identities | **match** | Memory entity linking calls `identity/resolver.py` keys first | ≥ 80% of memory mentions on IT corpus resolved without a model call.

**STR-graphiti-zep-05** | Graphiti | Pydantic-typed ontology for extraction with edge-type signature enforcement | CLAIM-24 | Customer-specific memory schemas | **integrate** | Generate extraction schemas from EOIP ontology manifest | Out-of-signature edges rejected at the validation gate (BL-28).

**INV-graphiti-zep-01 — Seed hypothesis §10.5 "Graphiti / agent-memory: LLM-dependent extraction cost and latency"** → **VALIDATED, with upstream mitigation noted**.
- Target/version/workload: Graphiti 0.31.1, conversational and document episodes.
- Evidence: write path issues multiple structured LLM calls per episode and per new edge [CLAIM-28]; README requires background queues, sequential episodes and a semaphore against 429s [CLAIM-13]; small local models fail schema output [CLAIM-12]; Zep meters ingestion, not retrieval [CLAIM-19]. Upstream mitigations exist but are partial: GLiNER2 local NER (entities only), exact-match fast paths, LLM disk cache, per-prompt routing to small models, `add_triplet` bypass [CLAIM-14][CLAIM-26][CLAIM-29][CLAIM-30].
- Root cause: *algorithm/coupling* (proven) — extraction, resolution, contradiction and temporal dating are all prompt tasks; there is no deterministic path for structured sources other than manual triplets.
- Why an alternative mitigates: most EOIP inputs (Jira, ServiceNow, Git, CMDB) are structured; schema-driven mapping (BL-26, BL-33) yields facts and validity times (field timestamps) without a model. Worse when: input is free-form conversation where rules miss implicit facts.
- Options: (1) quick — run Graphiti with Ollama behind EOIP egress for conversational memory only; (2) pragmatic — EOIP-native memory facts from SourceEvents deterministically, local model only for free-text spans, LLM under policy; (3) long-term — tiered extraction cascade with confidence-calibrated escalation and per-tenant cost budgets, model outputs stored as PROPOSED (BL-40).
- Selected: (2) now, (3) as roadmap. Pattern: *extraction cascade*.
```
extract(event):
  facts = mapping_rules(event)                  # deterministic, evidence span = field path
  if event.has_free_text:
     facts += local_ner_re(event.text)  -> status=PROPOSED
     if policy.allows_llm(tenant, classification) and confidence < τ:
        facts += llm_extract(event.text) via egress_gateway -> status=PROPOSED
  return facts
```
- Benchmark/POC (PROPOSED, BM-mem-01): 10k Jira+Confluence events; metrics: model calls per event, CPU-seconds per event, fact F1 vs a 500-event gold set, as-of accuracy; baseline = Graphiti 0.31.1 + Ollama 8B on the same hardware. Success: ≥ 10× fewer model calls with F1 within 5 points on structured events.
- Dependencies: mapping IR, identity, egress gateway. Backward compatibility: additive store. Security failure cases: prompt injection in free text → only PROPOSED facts; ACL loss if spans are merged across sources (keep per-fact `acl_hash`).
- Defensibility: requires EOIP's connectors, mapping and governance — not a prompt trick a competitor copies quickly.
- **Decision: ADOPT.**

**INV-graphiti-zep-02 — No permission model; tenancy is an optional partition key**.
- Evidence: MCP server without authn/authz [CLAIM-10]; empty `group_ids` → global search [CLAIM-09]; partition is a property except on FalkorDB [CLAIM-08]; Zep concepts page describes no ACL [CLAIM-23].
- Root cause: *governance/data model* (proven) — memory is modelled per user/agent, not per source permission.
- Alternative: every memory fact carries `tenant_id` + `acl_hash` + `principal_set`, and retrieval re-checks the caller's current entitlements on read; revocation invalidates. Worse when: ACL re-check latency on large candidate sets (mitigate with pre-filter by tenant + cached principal bitmaps).
- Options: (1) wrap Graphiti with one group per tenant and post-filter by ACL; (2) EOIP memory store with mandatory tenant key and read-time ACL check; (3) ReBAC engine (cross-ref C19 OpenFGA/SpiceDB) with memory facts as objects.
- Selected: (2) now, (3) later. API sketch: `recall(principal, tenant, query, as_of) -> [Fact]` where `filter(f: f.tenant==tenant and authz.check(principal, f.acl_ref, "read", now))`.
- POC (PROPOSED, J5): two principals, 1,000 facts, revoke 100 source permissions; success = 0 revoked facts returned after revocation, p95 overhead < 20 ms.
- Failure cases: summaries/consolidations that mix facts from different ACLs must inherit the intersection of permissions or be dropped.
- Defensibility: EOIP's permission metadata already exists at ingest (BL-17); competitors would need source connectors that capture ACLs.
- **Decision: ADOPT (P0).**

**INV-graphiti-zep-03 — Deletion and invalidation are not reversible**.
- Evidence: `remove_episode` deletes first-episode edges and does not reopen edges it invalidated [CLAIM-16].
- Root cause: *data model* (proven for 0.31.1) — invalidation is stored as mutable fields on the old edge, not as a separate decision record.
- Alternative: invalidation as an event (`ResolutionDecision{superseded, superseding, evidence}`) so removing evidence replays decisions. Worse when: replay cost on large histories.
- Options: (1) document; (2) store invalidations as decision records in BL-39 and recompute on evidence removal; (3) full event-sourced memory with incremental truth maintenance.
- Selected: (2). POC: delete the episode that caused invalidation; success = previously valid fact reopens, audit shows both decisions.
- **Decision: ADOPT.**

**INV-graphiti-zep-04 — Expired facts returned unless filtered**: search applies no default validity filter [CLAIM-27]. Selected design: EOIP `recall` defaults to `as_of=now` and exposes history explicitly. **Decision: ADOPT** (cheap).

**INV-SELF-graphiti-01 (EOIP weakness)** — EOIP memory stores either keep only task outcome stubs (`FileMemoryStore`) or overwrite facts destructively (`SemanticMemory.upsert`); `memory_eng` has no tenant/owner. Fix: unify into one governed memory-fact store (STR-01) and retire duplicate in-process stores behind it. **Decision: ADOPT.**

## 13. Per-capability decisions

| Capability | Decision | Rationale |
|---|---|---|
| CAP-57 agent memory (write/expire/invalidate) | **BUILD** (EOIP-native, Graphiti patterns) | needs tenant + ACL + egress which Graphiti lacks |
| CAP-34 bitemporal on memory facts | **BUILD** on BL-37 | reuse existing temporal model |
| CAP-39 contradiction handling | **BUILD** deterministic-first; **EXPERIMENT** local-model detector | STR-02 |
| CAP-32 free-text fact extraction for memory | **EXPERIMENT** with Graphiti-as-library behind egress (Apache-2.0) | compare with cascade (INV-01) |
| CAP-55 hybrid retrieval rerankers | **BUILD** (node distance, mention frequency) | small, high value |
| CAP-59 MCP memory tools | **BUILD** governed write tools (proposal-only) | Graphiti MCP rejected (no auth) |
| CAP-46/CAP-47 ACL + tenancy for memory | **BUILD (P0)** | absent upstream |
| Zep Cloud as dependency | **REJECT** | managed/proprietary, no air-gap |
| Graphiti as a bundled runtime component | **DEFER** | only if EXPERIMENT shows quality gain; no HugeGraph support |

## 14. Concrete tests, proof-of-concept, and acceptance conditions (all PROPOSED)

1. **T-mem-01 As-of correctness**: 200 scripted ownership changes (Confluence vs ServiceNow, J2); acceptance: 100% correct as-of answers, both claims preserved, decisions auditable.
2. **T-mem-02 Revocation (J5)**: revoke source permission → next `recall` excludes the fact and any consolidation derived from it; acceptance 0 leaks.
3. **T-mem-03 Tenant isolation (J13)**: two tenants with identical entity names; acceptance 0 cross-tenant results including when the tenant parameter is omitted (must error, unlike Graphiti [CLAIM-09]).
4. **BM-mem-01 Extraction cost** (INV-01): model calls/event, CPU-s/event, F1; Graphiti 0.31.1 + Ollama as baseline.
5. **BM-mem-02 Memory QA**: LongMemEval-S and LoCoMo run locally with a fixed open judge and published prompts, comparing EOIP memory, Graphiti (local models), plain BM25+dense RAG over raw history (Master Prompt §5.3); report variance across 3 seeds; LoCoMo results flagged with the known label-error caveat [CLAIM-22].
6. **T-mem-04 Evidence deletion**: delete the source episode of a superseding fact → superseded fact reopens (INV-03).
7. **T-mem-05 Air-gap (J16)**: Graphiti experiment runs with network disabled and telemetry off; acceptance: no outbound connection attempts (packet capture).

## 15. Risks, trade-offs, and open research questions

- Risk: copying Graphiti's LLM-centric pipeline would import its cost profile; mitigated by the cascade.
- Risk: valid-time extraction from free text is error-prone; label model-dated intervals PROPOSED.
- Trade-off: deterministic contradiction only covers properties with declared cardinality; free-text facts still need a model.
- Open: does Graphiti's candidate-retrieval-bounded contradiction detection miss long-range contradictions at scale (recall vs graph size)? Measure.
- Open: Zep's proprietary engine and isolation model — NOT PUBLICLY VERIFIED.
- Open: independent LongMemEval results for Graphiti with local models — none found.
- Open: FalkorDB (SSPL) is Graphiti's default MCP backend — licence trigger if EOIP ever ships it.

## Appendix A — Research-dimension coverage

| Dimension | Section(s) | Summary or N/A reason |
|---|---|---|
| D1 Identity and maturity | 1 | Graphiti 0.31.1 Apache-2.0 active pre-1.0; Zep proprietary; CE deprecated 2025-04-02 |
| D2 Problem and workloads | 2 | temporal agent memory, per-user and shared graphs |
| D3 Architecture | 4, 5 | Python library over Cypher backends; MCP and REST samples |
| D4 Storage and indexing | 5 | delegated to backend; fulltext + vector indexes; OpenSearch for Neptune |
| D5 Schema/semantics | 5, 8 | Pydantic types, edge-type map; no OWL/SHACL |
| D6 Query pipeline | 5 | BM25 ∥ cosine ∥ BFS + rerankers; no planner of its own |
| D7 Reasoning | 5 | none symbolic; label-propagation communities |
| D8 Transactions/scale | 5, 7 | async semaphore, sequential per graph, no episode transaction |
| D9 Ingestion/federation | 2, 5 | episodes; bulk; triplets; no connectors |
| D10 Identity and evidence | 5 | deterministic fast paths + LLM dedupe; episode provenance |
| D11 Time and evolution | 5, 12 | valid/transaction time on edges; non-destructive invalidation |
| D12 Graph ML | 5 | embeddings; communities; no GNN |
| D13 Retrieval/agents | 3, 5, 12 | hybrid retrieval, MCP tools, memory write/expire/delete rules analysed |
| D14 NL querying | — | N/A: no NL→query; retrieval is semantic search |
| D15 Governance | 9, 11 | no approvals or stewardship |
| D16 Human experience | 3 | Zep dashboard; Graphiti none |
| D17 Developer experience | 8 | Pydantic API, prompt overrides, routing, MCP |
| D18 Trust and security | 5, 10 | no authn/authz in OSS; telemetry opt-out; SOC2 for Zep |
| D19 Multi-tenancy | 5, 12 | group_id partition; global read if omitted |
| D20 Economics | 7 | LLM-call cost model; Zep credit pricing |
| D21 Commercial | 1, 10 | open core: Apache library + proprietary cloud engine |
| D22 Interop/lock-in | 10 | Cypher backends; no HugeGraph/Gremlin |
| D23 IP and prior art | 15 | published method (arXiv 2501.13956) is prior art for bitemporal LLM memory graphs — record for EOIP novelty claims; no patent search done |
| D24 Research quality | 7 | vendor papers and contested LoCoMo; no independent reproduction |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-57 | native | CLAIM-05, -06, -28 | Partial (agents/memory.py task stubs; no BL-ID) | BUILD | P1 |
| CAP-34 | native (edges) | CLAIM-05 | BL-37 Implemented (graph), memory valid-time only | BUILD | P1 |
| CAP-39 | native (LLM) | CLAIM-06 | BL-39 Implemented (in-memory) | BUILD | P1 |
| CAP-38 | native (episode provenance) | CLAIM-05, -10 | BL-41 Implemented | REUSE (EOIP) | P2 |
| CAP-31 | partial (LLM dedupe) | CLAIM-28 | BL-36 Absent | EXPERIMENT | P2 |
| CAP-32 | native (LLM) | CLAIM-28 | Partial | EXPERIMENT | P2 |
| CAP-55 | native | CLAIM-07 | BL-15 Implemented | BUILD (rerankers) | P2 |
| CAP-53 | native (backend vectors) | CLAIM-03 | BL-14 Partial | DEFER | P3 |
| CAP-59 | native, unauthenticated | CLAIM-10 | BL-47 Implemented (read-only) | BUILD (governed write) | P2 |
| CAP-46 | absent | CLAIM-10, -23 | BL-18 Absent | BUILD | P0 |
| CAP-47 | partial (group_id) | CLAIM-08, -09 | BL-20 Partial | BUILD | P0 |
| CAP-51 | partial (configurable endpoint; Jev egress) | CLAIM-12, -15 | BL-45 Implemented | REUSE (EOIP) | P1 |
| CAP-50 | partial (possible with local stack) | CLAIM-11, -12 | Implemented (compose) | REUSE | P1 |
| CAP-61 | via OpenAI-compatible endpoints | CLAIM-12 | Partial (Ollama in compose) | REUSE | P2 |
| CAP-78 | vendor benchmarks only | CLAIM-20, -21 | Absent | BUILD (BM-mem-02) | P2 |

## Appendix C — Evidence records

| CLAIM-ID | Product / version / date | Exact claim | Classification | Source | Pub / access | Confidence | Contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-graphiti-zep-01 | graphiti-core 0.31.1, 2026-10-15 | Latest PyPI release 0.31.1; prior 0.29.1 (2026-05-21) … 0.30.2 (2026-09-08); Python ≥3.10 | Officially documented | PyPI JSON https://pypi.org/pypi/graphiti-core/json | 2026-10-15 / 2026-10-18 | 0.9 registry metadata | none |
| CLAIM-graphiti-zep-02 | Graphiti main | Licence Apache License 2.0 (LICENSE; PyPI `license_expression: Apache-2.0`) | Officially documented | https://raw.githubusercontent.com/getzep/graphiti/main/LICENSE | n/a / 2026-10-18 | 0.95 | none |
| CLAIM-graphiti-zep-03 | README main | Requires Neo4j 5.26 / FalkorDB 1.1.2 / Neptune DB or Analytics + Amazon OpenSearch Serverless (full-text) / Kùzu 0.11.2 (deprecated); FalkorDB Lite embedded needs Py 3.12 | Officially documented | Graphiti README https://github.com/getzep/graphiti | n/a / 2026-10-18 | 0.85 | none |
| CLAIM-graphiti-zep-04 | README main | "Kuzu is deprecated … upstream Kuzu project is no longer maintained"; driver emits DeprecationWarning | Officially documented | Graphiti README | n/a / 2026-10-18 | 0.85 | consistent with Kùzu archival (Master Prompt §5.1) |
| CLAIM-graphiti-zep-05 | 0.31.1 `edges.py`, `nodes.py` | `EntityEdge` has fact, fact_embedding, episodes, valid_at, invalid_at, expired_at, reference_time, attributes; `Edge`/`Node` carry group_id ("partition of the graph") and created_at | Observed in source code | graphiti_core-0.31.1 wheel `edges.py:49-55,263-290` | 2026-10-15 / 2026-10-18 | 0.9 | none |
| CLAIM-graphiti-zep-06 | 0.31.1 `utils/maintenance/edge_operations.py` | LLM `dedupe_edges.resolve_edge` returns duplicate and invalidation candidate indexes; `_apply_temporal_invalidation`/`resolve_edge_contradictions` deterministically set invalid_at = new.valid_at and expired_at = now for earlier contradicted edges, or close the new edge if a later one exists | Observed in source code | wheel `edge_operations.py:715-783, 864-960` | 2026-10-15 / 2026-10-18 | 0.9 | none |
| CLAIM-graphiti-zep-07 | 0.31.1 `search/search_config.py` | Search methods cosine, bm25, breadth_first_search; rerankers RRF (default), node_distance, episode_mentions, MMR, cross_encoder | Observed in source code | wheel `search_config.py:32-92` | 2026-10-15 / 2026-10-18 | 0.9 | none |
| CLAIM-graphiti-zep-08 | 0.31.1 drivers; MCP README | Base `GraphDriver.clone` returns self; FalkorDriver clones to a different graph per group; "On FalkorDB, each group_id is stored in its own graph" | Observed in source code + Officially documented | wheel `driver/driver.py:131-133`, `falkordb_driver.py:334-342`; MCP README | 2026-10-18 | 0.85 | none |
| CLAIM-graphiti-zep-09 | 0.31.1 `search/search.py` | "if group_ids is empty, set it to None" → no group filter | Observed in source code | wheel `search.py:155-156` | 2026-10-18 | 0.8 (effect on each driver's query inferred) | none |
| CLAIM-graphiti-zep-10 | MCP server README main | "reference implementation… no authentication or authorization, and any caller can read, change, or delete all graph data"; experimental; HTTP `/mcp/` default, stdio optional; FalkorDB default; tools add_memory, add_triplet, search_nodes, search_memory_facts, summarize_saga, build_communities, get_episode_entities, delete_entity_edge, delete_episode, get_entity_edge, get_episodes, clear_graph, get_status | Officially documented | https://github.com/getzep/graphiti/blob/main/mcp_server/README.md | n/a / 2026-10-18 | 0.9 | none |
| CLAIM-graphiti-zep-11 | README; METADATA | Anonymous telemetry via PostHog, opt-out `GRAPHITI_TELEMETRY_ENABLED=false`; `posthog` is a required dependency | Officially documented + Observed | README "Telemetry"; wheel METADATA | 2026-10-18 | 0.9 | none |
| CLAIM-graphiti-zep-12 | README | Local servers (Ollama, vLLM, llama.cpp, LM Studio) via `OpenAIGenericClient`; "Very small models frequently emit JSON that doesn't match the requested schema"; works best with structured-output providers | Officially documented | Graphiti README | 2026-10-18 | 0.85 | none |
| CLAIM-graphiti-zep-13 | README; graphiti.py docstring | `SEMAPHORE_LIMIT` default 10 to avoid 429s; "each episode is added sequentially"; run in a background queue | Officially documented | README; wheel `graphiti.py` add_episode docstring | 2026-10-18 | 0.85 | none |
| CLAIM-graphiti-zep-14 | 0.31.1 `llm_client/gliner2_client.py` | GLiNER2 (205M–340M params) does NER locally on CPU; all other operations delegated to the LLM | Observed in source code | wheel `gliner2_client.py:54-64` | 2026-10-18 | 0.85 | none |
| CLAIM-graphiti-zep-15 | README | Jev dedupe hosted by TypeSafe; "Graphiti sends dedupe prompt content to TypeSafe" | Officially documented | README "Jev dedupe" | 2026-10-18 | 0.8 | none |
| CLAIM-graphiti-zep-16 | 0.31.1 `graphiti.py` | `remove_episode` deletes edges whose first episode is the removed one and nodes mentioned only by it; no code re-opens edges it invalidated | Observed in source code (absence = reasoned inference) | wheel `graphiti.py:2164-2192` | 2026-10-18 | 0.75 | none found |
| CLAIM-graphiti-zep-17 | Zep CE, 2025-04-02 | Zep stops maintaining/releasing Community Edition; repo stays Apache-2.0 without updates; focus on Graphiti; help page: CE deprecated, use Zep Cloud or Graphiti | Officially documented | https://www.getzep.com/blog/announcing-a-new-direction-for-zeps-open-source-strategy/ ; https://help.getzep.com/ce-deprecation-notice | 2025-04-02 / 2026-10-18 | 0.9 | none |
| CLAIM-graphiti-zep-18 | README main | Zep powered by proprietary "Context Graph Engine"; Zep deployment "Fully managed or in your cloud"; Graphiti "Self-hosted only" | Officially documented (vendor) | Graphiti README "Zep vs Graphiti" | 2026-10-18 | 0.8 | none |
| CLAIM-graphiti-zep-19 | Zep pricing | Credits: 1 per episode up to 350 bytes; retrieval/storage unmetered; Free 10k credits; Flex $125/mo; Flex Plus $375/mo; Enterprise; Cloud, BYOK, BYOC (in customer VPC); SOC 2 Type II; HIPAA BAA on Enterprise | Officially documented | https://www.getzep.com/pricing | n/a / 2026-10-18 | 0.75 (pricing changes often) | none |
| CLAIM-graphiti-zep-20 | Zep paper v1 | DMR 94.8% vs MemGPT 93.4%; LongMemEval accuracy improvements up to 18.5%; response latency reduced 90% vs baselines | Unverified (vendor-authored paper) | arXiv:2501.13956 https://arxiv.org/abs/2501.13956 | 2025-01-20 / 2026-10-18 | 0.4 vendor-authored, not reproduced | Contested LoCoMo results (CLAIM-21) |
| CLAIM-graphiti-zep-21 | LoCoMo, 2025-05-06 (modified 2026-06-03) | Zep: corrected LoCoMo J 75.14% ± 0.17; Mem0 had reported Zep 65.99%, Mem0-graph 68.44%, full-context 72.90%; Mem0 misconfigured roles/timestamps; p95 search 0.632 s (us-west-2). Mem0 later cites Zep at 62–83% depending on settings | Unverified (contested vendor claims) | https://www.getzep.com/blog/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/ ; https://mem0.ai/blog/zep-vs-mem0-which-ai-memory-layer-should-you-choose | 2025-05-06 / 2026-10-18 | 0.3 | each vendor disputes the other |
| CLAIM-graphiti-zep-22 | LoCoMo audit | Penfield Labs audit: 99 score-corrupting errors in 1,540 questions; LLM judge accepted 62.81% of deliberately wrong answers | Third-party report (secondary, vendor-originated) | https://www.beri.net/article/zep-vs-mem0-vs-postgres-agent-memory-store-buy-last-2026 | 2026 / 2026-10-18 | 0.3 secondary source | none |
| CLAIM-graphiti-zep-23 | Zep docs | Users with user graphs and threads; standalone graphs by `graph_uuid`; context block; custom types; page describes no ACL/RBAC/multi-tenancy model | Officially documented | https://help.getzep.com/concepts | 2026-10-18 | 0.7 | none |
| CLAIM-graphiti-zep-24 | README | Custom entity and edge types via Pydantic; prescribed and learned ontology; `edge_type_map` | Officially documented | README; MCP README | 2026-10-18 | 0.85 | none |
| CLAIM-graphiti-zep-25 | 0.31.1 graphiti.py | `store_raw_episode_content` flag blanks episode content | Observed in source code | wheel `graphiti.py:216,335,1032` | 2026-10-18 | 0.85 | none |
| CLAIM-graphiti-zep-26 | 0.31.1 llm_client | Optional disk LLM cache `./llm_cache`, off by default | Observed in source code | wheel `llm_client/client.py:29-92` | 2026-10-18 | 0.85 | none |
| CLAIM-graphiti-zep-27 | 0.31.1 search | `SearchFilters` supports valid_at/invalid_at/created_at/expired_at; no default exclusion of expired edges found in `search/` | Observed (absence = reasoned inference) | wheel `search_filters.py:55-73` | 2026-10-18 | 0.65 | Zep Cloud may filter server-side (unknown) |
| CLAIM-graphiti-zep-28 | 0.31.1 maintenance | LLM prompt call sites: extract_nodes_and_edges.extract_message, extract_edges.edge, dedupe_nodes.nodes, dedupe_edges.resolve_edge, extract_edges.extract_timestamps(_batch), extract_*.extract_attributes, summarize_nodes.*, summarize_sagas.*; exact-name and identity-property candidate fast paths | Observed in source code | wheel `utils/maintenance/*.py`, `node_operations.py:487-585` | 2026-10-18 | 0.85 | none |
| CLAIM-graphiti-zep-29 | README | Prompt overrides (`ChatPromptLibrary`) and per-prompt model routing (`LLMRuntime`, `PromptRoutes`) | Officially documented | README "Configurable Prompts" | 2026-10-18 | 0.85 | none |
| CLAIM-graphiti-zep-30 | MCP README; graphiti.py | `add_triplet` adds a fact directly, bypassing extraction | Officially documented + Observed | MCP README; wheel `graphiti.py:2023` | 2026-10-18 | 0.85 | none |
| CLAIM-graphiti-zep-31 | README | Graphiti vs GraphRAG: "Typically sub-second latency" vs "Seconds to tens of seconds" | Unverified (vendor claim, no workload stated) | README | 2026-10-18 | 0.3 | none |
| CLAIM-graphiti-zep-32 | README | Zep "sub-200ms performance at scale" | Unverified (vendor claim) | README "Zep vs Graphiti" | 2026-10-18 | 0.3 | Zep rebuttal reports p95 0.632 s for its LoCoMo setup (CLAIM-21) |
| CLAIM-graphiti-zep-33 | 0.31.1 graphiti.py | Issue #1676: concurrent calls for different group_ids could reassign shared driver and persist episodes under the wrong graph; fixed via request-scoped driver | Observed in source code (docstring) | wheel `graphiti.py:1302-1330` | 2026-10-18 | 0.8 | none |

## Appendix D — Assumptions

- A1: The registry entry covers Graphiti (OSS) and Zep (commercial) together; Zep CE is treated as historical.
- A2: Wheel contents of 0.31.1 equal the GitHub tag (no tag checkout possible under GitHub API rate limits); line numbers refer to the wheel.
- A3: The Graphiti MCP server and REST server are not in the wheel; their behaviour is taken from the `main` README on 2026-10-18.
- A4: LLM-call counts are derived from code paths, not measured.
- A5: FalkorDB licence (SSPL) is taken from the C01 worker scope (W04); not re-verified here.
- A6: Zep Cloud internals, isolation and benchmark harnesses are NOT PUBLICLY VERIFIED.
- A7: EOIP comparison uses `agents/memory.py`, `memory_eng/engine.py`, `reasoning/memory.py`, `moonshot/streaming_agent_memory.py`; the coordinator's mention of `graph/memory.py` was checked and it is the in-memory graph store.
