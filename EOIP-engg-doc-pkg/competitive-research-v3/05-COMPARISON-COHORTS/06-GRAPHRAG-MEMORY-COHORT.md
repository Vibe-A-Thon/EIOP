# Cohort 06 - GraphRAG versus strong plain RAG, and agent memory

| Field | Value |
|---|---|
| Cohort ID | COH-06 |
| Workload class | Graph-assisted retrieval and answer generation (GraphRAG, hierarchical/associative retrieval) judged against non-graph baselines; agent and organisational memory (write, expire, invalidate) |
| Members, GraphRAG engines | [microsoft-graphrag](../04-COMPETITOR-DEEP-DIVES/C08-microsoft-graphrag.md), [lightrag](../04-COMPETITOR-DEEP-DIVES/C08-lightrag.md), [hipporag](../04-COMPETITOR-DEEP-DIVES/C08-hipporag.md), [neo4j-graphrag](../04-COMPETITOR-DEEP-DIVES/C08-neo4j-graphrag.md), [llamaindex-pgi](../04-COMPETITOR-DEEP-DIVES/C08-llamaindex-pgi.md), [openspg-kag](../04-COMPETITOR-DEEP-DIVES/C08-openspg-kag.md), [fast-graphrag](../04-COMPETITOR-DEEP-DIVES/C08-fast-graphrag.md) |
| Members, pipelines and methods | [whyhow](../04-COMPETITOR-DEEP-DIVES/C08-whyhow.md), [raptor](../04-COMPETITOR-DEEP-DIVES/C08-raptor.md), [think-on-graph](../04-COMPETITOR-DEEP-DIVES/C08-think-on-graph.md), [ragflow](../04-COMPETITOR-DEEP-DIVES/C08-ragflow.md), [haystack](../04-COMPETITOR-DEEP-DIVES/C08-haystack.md), [langchain-langgraph](../04-COMPETITOR-DEEP-DIVES/C08-langchain-langgraph.md) |
| Members, agent memory | [graphiti-zep](../04-COMPETITOR-DEEP-DIVES/C08-graphiti-zep.md), [cognee](../04-COMPETITOR-DEEP-DIVES/C08-cognee.md), [mem0](../04-COMPETITOR-DEEP-DIVES/C08-mem0.md), [letta](../04-COMPETITOR-DEEP-DIVES/C08-letta.md) |
| Tier C records | [C08-tier-c-records-V21](../04-COMPETITOR-DEEP-DIVES/C08-tier-c-records-V21.md): nano-graphrag, InfraNodus, ContextClue, Harmony MCP, MemPalace, MythOS, claude-mem, G-Retriever, PathRAG, MiniRAG, StructRAG, R2R, Kotaemon, txtai, LangMem, A-MEM (all REFERENCE-ONLY or EXPERIMENT; one claim each, repo metadata only) |
| Reference columns | HugeGraph, Neo4j, Neptune, EOIP @HEAD 896e06d (BL-IDs from `01-SYSTEM-BASELINE.md` at ad9937b, status from `01a-BASELINE-DELTA-HEAD.md`) |
| Date | 2026-10-26 (evidence accessed 2026-10-18 to 2026-10-26) |

## 1. Workload class and comparison basis

**Customer workloads served.** (a) Cited question answering over enterprise corpora and the knowledge graph; (b) global "sensemaking" questions over large corpora; (c) multi-hop questions that need several linked facts; (d) long-lived assistant or agent context that accumulates, supersedes and forgets facts.

**Why comparable.** Every member turns text into retrievable context for an LLM and differs in what it indexes (chunks, entity/relation graph, community summaries, summary tree, episodic edges). The Master Prompt (section 5.3) requires that graph retrieval be judged against a strong non-graph baseline, so the baseline is part of the cohort: dense plus BM25 plus rerank, which EOIP already ships (BL-13/14/15; weighted fusion in `retrieval/service.py` per 01a).

**Excluded or marked reference-only.** Cloud-only managed products (Zep Cloud, Mem0 Platform, Letta Cloud) are described only where they show what the OSS part lacks (CLAIM-graphiti-zep-17/18, CLAIM-mem0-02). WhyHow is not publicly verifiable (CLAIM-why-02); ToG and StructRAG have no licence file, so only ideas can be used. Tier C items have repo-metadata evidence only and do not enter the findings except where stated.

**Evidence rule.** Independent academic benchmarks are used for quality and cost comparison: Han et al. (arXiv 2502.11371), GraphRAG-Bench (2506.05690), Zeng et al. (2506.06331). Author and vendor figures are labelled as such. Every member dive records **no source-ACL or tenant model** (see section 2); that is a cohort-wide fact, not a differentiator.

## 2. Capability comparison

Cell values: native / partial / plugin / absent / unknown, with CLAIM-ID (competitor) or BL/NB-ID (EOIP). Where a dive gives an inline evidence ID rather than a claim row, that ID is used; "dive" means the statement is in the dive text without a claim ID.

### 2.1 GraphRAG engines

| CAP | MS GraphRAG | LightRAG | HippoRAG 2 | neo4j-graphrag | LlamaIndex PGI | OpenSPG KAG | fast-graphrag | Neo4j | HugeGraph | Neptune | EOIP @HEAD |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CAP-56 GraphRAG | native: local, global, DRIFT (msgraphrag-08..10) | native: ll/hl keyword modes (lightrag-04) | native: PPR passage retrieval (hipporag-04/06) | partial: vector+Cypher expansion; no community or global (n4gr-05, -06) | partial: neighbourhood expansion (pgi-08) | native: logical-form planner (kag-06, -12) | native: PPR (fgr-03) | via neo4j-graphrag (n4gr-02) | HugeGraph-LLM, separate service (hugegraph-28) | managed GraphRAG only mentioned in an announcement (neptune-35) | Implemented deterministic plus local-LLM synthesis with claim check (BL-16); community/PPR diffusion `rag/dual_level_diffusion.py` library-only, no caller |
| CAP-55 hybrid fusion | absent (msgraphrag Appx B) | partial: mix mode (lightrag-04) | dense fallback (hipporag-04) | native: max or linear, no RRF (n4gr-06) | absent (pgi dive) | partial: hybrid fallback (kag-06) | unknown | native FTS+vector in Cypher 25 (neo4j-09/10) | vector index absent in server (hugegraph-09) | FTS via OpenSearch (neptune-16) | Implemented: weighted 0.45/0.35/0.20 on the API path; RRF library-only (BL-15) |
| CAP-31 entity identity | LLM merge, no ER | string key (lightrag dive) | soft synonym edges, thr 0.8 (hipporag-05) | exact name; fuzzy replaces nodes (n4gr-09) | name string, no ER (pgi-10) | alignment relations (kag-06) | unknown | n/a | n/a | n/a | Partial, own FS engine, library-only (BL-36) |
| CAP-34/39 temporal and contradiction | absent | absent | absent | absent | absent | absent | absent | n/a | n/a | n/a | Implemented bitemporal and claims, in-memory TruthStore (BL-37, BL-39) |
| CAP-67 incremental update | partial: title diff, deleted_inputs unused (msgraphrag-11) | native delete rebuild (lightrag-05) | native add and delete (hipporag-07) | writer upsert, no delete lineage (n4gr-08) | stale triplets on re-ingest (pgi-09) | unknown | unknown | n/a | n/a | n/a | Implemented replay and tombstones (BL-24, BL-25) |
| CAP-46 source-ACL | absent (msgraphrag-12) | absent (lightrag-06) | absent (hipporag-09) | absent (n4gr-11) | absent (pgi-10) | absent/unknown (dive) | absent (fgr dive) | EE privileges, not source ACL (neo4j-14) | auth optional (hugegraph-14) | IAM actions, app does finer (neptune-09/12) | **Partial**: evaluator exists, applied only in the graph branch when `scope` is passed; no deployed caller passes it (BL-18, U-04) |
| CAP-47 tenancy | absent (msgraphrag-12) | workspace only (lightrag-06) | absent (hipporag-09) | absent (n4gr-11) | absent (pgi-10) | unknown (project level) | not multi-tenant (dive) | EE database per tenant (neo4j-13) | graphspaces (hugegraph dive) | silo/pool guidance (neptune-32) | Partial improved: embedded layers and retrieval index tenant-scoped (BL-20, NB-11); adapters tenant-blind |
| CAP-60 citations and abstention | LLM-emitted ids, unvalidated (msgraphrag-13) | partial (lightrag dive) | passages only (dive) | unknown | source id only (pgi-09) | chunk links (kag-06) | unknown | n/a | n/a | n/a | Implemented: cited-span claim-support check removes unsupported claims, extractive fallback (BL-16) |
| CAP-61/50 local, air-gap | partial (msgraphrag-14) | yes in principle, offline files (lightrag-07) | partial, 70B on 2 GPUs example (hipporag-14) | yes (n4gr dive) | plugin | partial, 72B benchmarks (kag-04) | partial (dive) | CE GPLv3 | Apache-2.0 | cloud only | Implemented ModelPort, Ollama default, egress S0 (NB-10, BL-45) |
| CAP-78 evaluation harness | absent in project | absent | absent | absent | absent | partial `open_benchmark` (kag dive) | absent | n/a | n/a | n/a | **Absent**; no benchmark against plain RAG (BL-16 note) |

### 2.2 Pipelines and methods

| CAP | WhyHow | RAPTOR | Think-on-Graph | RAGFlow | Haystack | LangChain/LangGraph | EOIP @HEAD |
|---|---|---|---|---|---|---|---|
| CAP-56 | partial, schema-guided triples (why-02) | partial: summary tree, not graph (rap-01) | native: LLM-guided beam search on KG (tog-01, -02) | native: General or Light KG, optional ER and reports (rf-03) | none; storage-adjacent only (dive) | Cypher QA chain, no read-only check (lc-03) | BL-16 / diffusion library-only |
| CAP-32 extraction | partial (why-02) | n/a | n/a | native DeepDoc layout parsing (rf-01) | via components | via integrations | Absent for unstructured text (CAP-32, BL-26 JSON only) |
| CAP-46 / CAP-47 | unknown | absent: summaries mix ACL groups (rap dive) | absent: neighbour API must filter (tog dive) | workspace/team level only (dive) | metadata filters only (dive) | absent (lc dive) | see 2.1 |
| Licence | unverified | MIT, dormant since 2024-09 (rap-02) | none found (tog dive) | Apache-2.0 (rf-01) | Apache-2.0 (hay-01) | MIT, community pkg stale (lc dive) | n/a |
| Air-gap | partial/unknown, Atlas (why-02) | yes (dive) | yes with local KG (dive) | partial (dive) | yes | tracing must be off | Implemented |

### 2.3 Agent memory

| CAP | Graphiti / Zep | Cognee | Mem0 | Letta | EOIP @HEAD |
|---|---|---|---|---|---|
| CAP-57 write | native: LLM extract, dedupe, date per episode (graphiti-zep-28); `add_triplet` bypass (-30) | native remember/improve; two LLM calls per chunk (cognee-04) | native: ADD-only, md5 dedup (mem0-04, -06) | native: self-edit blocks, git-versioned (letta-06, -09) | **No BL/NB row**; dives cite `agents/memory.py` stubs only; PROPOSED-until-validated contract (BL-40) |
| Expire / invalidate | native: valid_at, invalid_at, expired_at; LLM-detected contradiction (graphiti-zep-05, -06); deletion does not reopen edges (-16) | forget item/dataset; best effort, bytes may remain (cognee-07); temporal removed (dive) | read-time `expiration_date` filter, data persists (mem0-09); no supersession (mem0-06) | absent: unstructured text (letta-08); dreaming rewrites without approval (letta-07) | Bitemporal revisions exist for graph facts (BL-37); not applied to memory |
| CAP-46 / CAP-47 | `group_id` partition; empty list means global search (graphiti-zep-08, -09); MCP has no authn (-10) | dataset-level ACL, principals user/tenant/role (cognee-06) | scope keys by caller, no ACL (mem0-08) | org-level scope, `access` ignored, shared token (letta-04, -08) | Partial (BL-18, BL-20) |
| Provenance | episode links (graphiti-zep-05) | off unless `PROVENANCE_TRACKING=true` (cognee-04) | none | git history of memory (letta-06) | Evidence manifests (BL-41) |
| Licence | Apache-2.0 (-02); Zep engine proprietary (-18); FalkorDB backend SSPL (dive) | Apache-2.0; default graph engine is renamed Kuzu, upstream archived (cognee-10) | Apache-2.0; typed graph removed from OSS (mem0-03, -04) | Apache-2.0; V1 server archived (letta-02) | n/a |
| Backend fit | Neo4j, FalkorDB, Neptune+OpenSearch Serverless; no HugeGraph (graphiti-zep-03) | Neo4j, Neptune optional (cognee-09) | vector stores only; no Neo4j/HugeGraph in OSS (mem0-12) | Postgres/SQLite (letta-11) | Backend-neutral GraphStore (BL-01) |

## 3. Operational and licensing comparison

| Member | Licence class | Redistribution / OEM trigger | One-node footprint | Air-gap | Maintenance |
|---|---|---|---|---|---|
| MS GraphRAG | MIT | Transitive deps need review; one index per tenant and scope | Pure Python; indexing hours-to-days on local GPUs (hypothesis, msgraphrag dive) | Partial; spaCy model must be pre-seeded | Active, v3.3.0; internals not semver-bound (msgraphrag-02) |
| LightRAG | MIT | None known | Library plus PG/Neo4j/Qdrant; default stores dev-only (lightrag-14) | Yes in principle (offline docs) | Active, v1.5.7; upgrade needs all writers stopped |
| HippoRAG 2 | MIT | Model weights carry separate licences | In-memory igraph pickle; whole-graph PPR; 9.9 GB reported (hipporag-10) | Partial-to-yes | Alpha `2.0.0a5` (hipporag-15) |
| neo4j-graphrag | Apache-2.0 plus PSF | Useful only against Neo4j; bundling CE (GPLv3) brings GPL duties | Library plus Neo4j with APOC | Yes | Active, v1.22.0; first-party (n4gr-02) |
| LlamaIndex PGI | MIT | Per-store server licences | Library | Plugin | Stores lag; Kuzu store orphaned (pgi-04) |
| OpenSPG KAG | Apache-2.0; PyPI licence metadata null (kag-09) | Neo4j CE GPLv3, ES SSPL/Elastic, MySQL GPL are the review surface | Multi-service stack; 72B-class models in headline results (kag-04) | Unverified at small models | Low cadence; one commit since 2025-08 (kag-05) |
| fast-graphrag | MIT | Managed service separate | In-memory | Viable (0.5 confidence) | Last commit 2025-11; PyPI 0.0.5 (fgr-02) |
| RAGFlow | Apache-2.0 | Bundled infra licences need review | 4 CPU, 16 GB, 50 GB recommended (rf-01) | Partial | Very active, 1.0 RC (rf-01) |
| Graphiti | Apache-2.0 | `posthog` hard dependency; FalkorDB SSPL if bundled | Light process; LLM dominates (dive) | Viable with local stack, telemetry off (graphiti-zep-11, -12) | Active, 0.31.1 (-01) |
| Cognee | Apache-2.0 | Ladybug/Kuzu licence not verified | File-based embedded stores | Partial | 1.x with breaking changes in most releases (cognee-02) |
| Mem0 | Apache-2.0 | OSS vs Platform split | Library plus local Qdrant/SQLite | Partial; telemetry on by default (mem0-10) | Active, 2.2.1 |
| Letta | Apache-2.0 | Trademark not for white-label (unverified) | Poor fit as embedded component (dive) | Partial-to-yes | Re-architected 2026 (letta-01, -02) |
| Reference: Neo4j | CE GPLv3; EE privileges, multi-DB, GDS EE commercial (neo4j-13, -14, -24) | GPL and EE gating | n/a | n/a | n/a |
| Reference: HugeGraph | Apache-2.0 (hugegraph-04) | None | Vector index absent (hugegraph-09) | n/a | 1.7.0 |
| Reference: Neptune | Managed AWS | Cloud only | n/a | No | n/a |

## 4. Performance evidence

No comparable end-to-end benchmark exists across the cohort on EOIP-like hardware (one CPU node, local LLM). The independent figures below use different corpora and models; read them as direction, not ranking.

| Evidence | Workload and setup | Result | Class |
|---|---|---|---|
| Han et al. 2502.11371 (msgraphrag-18) | MultiHop-RAG and others, Llama-3.1-8B | Build 135 s plain RAG vs 5,560 s community GraphRAG; NQ F1 64.78 RAG vs 54.48 community-global; HotpotQA 60.04 RAG vs 61.66 community-local vs 63.01 HippoRAG 2 | Independent |
| GraphRAG-Bench 2506.05690 (msgraphrag-17, lightrag-10, hipporag-11) | Novel and medical corpora, GPT-4o-mini | Tokens per query: vanilla 879; HippoRAG 2 1,008; MS local 38,707; MS global 331,375; LightRAG about 100,000. Fact retrieval: vanilla 60.92 vs best graph 60.14 (novel). Summarisation: MS 64.40 vs 51.30 vanilla (novel) but 41.87 vs 65.75 (medical). Complex reasoning: HippoRAG 2 53.38 vs 42.93 | Independent |
| Zeng et al. 2506.06331 (lightrag-11, msgraphrag-19) | Re-evaluation without LLM-judge bias | The same LightRAG system scores 90% vs 10% win rate under the original judge protocol; true gains "much more moderate" | Independent (abstract level, confidence 0.7) |
| HippoRAG 2 paper (hipporag-10, msgraphrag-20) | MuSiQue 11.7k passages | Indexing input tokens: GraphRAG about 115.5M, LightRAG 68.5M, HippoRAG 2 about 9.2M. Average F1: HippoRAG 2 59.8, dense 57.0, GraphRAG 49.6 | Competitor-authored; the LightRAG F1 of 6.6 is flagged implausible in two dives |
| KAG paper (kag-07) | HotpotQA, 2Wiki, MuSiQue, 72B-class models | F1 76.2 / 76.2 / 48.7 | Vendor; no local small-model figure |
| LoCoMo memory (graphiti-zep-21, mem0-15..17, letta-14) | Zep 75.14 (Zep), Mem0 92.5 (Mem0), Letta 74.0 (Letta) | Three vendors report different numbers under different configurations; an audit found 99 score-corrupting errors in 1,540 questions and a judge that accepted 62.81% of deliberately wrong answers (graphiti-zep-22) | Contested; no usable winner |

Not found for any member: p95 latency on one CPU node, memory per million entities, retrieval quality under ACL-filtered corpora, and any cost-per-correct-answer. LazyGraphRAG's claims (about 0.1% of GraphRAG index cost) are a vendor claim with no code in v3.3.0 (msgraphrag-15). EOIP has no benchmark of its own (CAP-78 Absent).

## 5. Findings

1. **Graph retrieval is not a general win over strong plain RAG.** On independent benchmarks plain RAG leads on single-hop fact retrieval (60.92 vs 60.14, GraphRAG-Bench; NQ 64.78 vs 54.48 and 61.03 for HippoRAG 2, Han et al.), while graph methods lead on multi-hop and some summarisation tasks (HotpotQA 63.01 vs 60.04; reasoning 53.38 vs 42.93) [msgraphrag-17, -18; hipporag-11, -12]. Falsifier: an EOIP corpus where plain hybrid retrieval matches HippoRAG-style PPR on multi-hop questions.
2. **Community-summary GraphRAG costs one to three orders of magnitude more than plain RAG and its gains are corpus-dependent.** 41x build time, about 44x tokens per query for local search and about 377x for global search, with a medical summarisation score below vanilla [msgraphrag-17, -18]. Associative PPR (HippoRAG 2) is the only graph method in the cohort with query cost near vanilla (1,008 vs 879 tokens) [hipporag-11].
3. **Reported graph-method gains shrink under unbiased evaluation.** LLM-judge win rates inflate (90% vs 10% for the same system) [lightrag-11]; the 100-token LightRAG figure and the 100k-token benchmark figure are unreconciled [lightrag dive section 7]. Treat any author-only figure as a hypothesis.
4. **No GraphRAG engine or memory system in the cohort enforces source ACLs; tenant handling is at most a partition key.** Seven engine dives and four memory dives record absence or a coarse scope (section 2). Graphiti's empty `group_ids` meaning global search [graphiti-zep-09] and Letta's ignored `access` argument [letta-08] show the failure mode. This is the single largest differentiator EOIP can claim, but only once BL-18 is wired in deployed paths.
5. **EOIP's BL-18 is "Partial", not "Absent": the enforcement code exists but is not on the deployed retrieval paths.** `authz/pdp.py` and `retrieval/service.py:575` filter only in the graph branch and only when a `scope` is passed; `apps/api/extended.py:906-913`, `/api/v1/rag` and `agents/governed.py:250` do not pass it, and keyword/vector/hybrid candidates are filtered by tenant only (01a, BL-18, U-04). Any claim of ACL-safe retrieval is currently false for those paths.
6. **Derived layers leak by construction unless built per ACL group.** RAPTOR summaries mix content from sources with different ACLs [rap dive]; MS GraphRAG community reports are global artefacts [msgraphrag-12]. EOIP's derived-fact check (`authz/pdp.py:200-215`, NB-17) is the right primitive but is applied in one branch only.
7. **Memory systems diverge on invalidation, and none provides approved, auditable supersession.** Graphiti invalidates by LLM judgement over top-k candidates, so facts outside the candidate set are never invalidated, and episode deletion does not reopen invalidated edges [graphiti-zep-06, -16]; Mem0 keeps contradictions side by side [mem0-04]; Letta rewrites memory without approval [letta-07]; Cognee's forget is best effort [cognee-07]. EOIP's claims/contradiction primitives (BL-39, BL-40) are a better base but are in-memory and not connected to a memory plane.
8. **Local-model viability is the weak point of every LLM-in-the-write-path design.** Graphiti and LightRAG warn that small models emit invalid JSON or loop [graphiti-zep-12, lightrag-07]; KAG's headline numbers use 72B models [kag-04]; HippoRAG's example needs 2 GPUs [hipporag-14]. No dive reports CPU-only quality. EOIP's CPU-only constraint (ADR-H15/H16) makes cheap extraction (GLiNER-class NER is used by Graphiti, graphiti-zep-14) and a deterministic fallback a requirement.
9. **Several apparently mature options are not usable as dependencies.** WhyHow is unverifiable [why-02]; Think-on-Graph and StructRAG have no licence; Mem0 removed typed graph memory from the OSS release [mem0-03, -04]; Cognee's default store is a renamed archived engine [cognee-10]; OpenSPG's engine has had almost no commits since 2025-08 [kag-05]; Zep CE is abandoned [graphiti-zep-17].
10. **Dives disagree on the shape of the evidence in two places.** Mem0's own pages report 92.5 and 91.6 for LoCoMo [mem0-15, -16]; Cognee's docs say forget only warns when history purge fails while the 1.6.6rc1 release notes say it fails [cognee dive, cognee-02]. Neither is resolved by independent runs.

## 6. Implications for EOIP

Respecting backend neutrality: neo4j-graphrag is Neo4j-specific and HugeGraph-LLM is a separate Python tier, so graph retrieval must stay in EOIP's layer over the `GraphStore` protocol; upstream features are "available upstream / not integrated", not "missing".

| CAP | Parity needed (STR-IDs) | Exploitable weakness (INV-IDs) | Decision | Candidate gap statement |
|---|---|---|---|---|
| CAP-78 evaluation harness | STR-msgraphrag-02 (in-tool plain-RAG control, `basic` mode) | INV-lightrag-01, INV-hipporag-01 (author-only cost and quality claims) | **BUILD, P0** | EOIP has no harness comparing graph retrieval with hybrid BM25+dense+rerank on its own corpora; BL-16 has no benchmark. Must precede any further GraphRAG investment. |
| CAP-46 source-ACL | STR-haystack-01 (mandatory ACL stage in the pipeline); STR-tog-01 (ACL-filtered `neighbourhood()`); STR-mem0-04 (scope never from payload) | INV-n4gr-02, INV-lightrag-02, INV-msgraphrag-02, INV-hipporag-02, INV-llamaindex-pgi-02, INV-mem0-02, INV-graphiti-zep-02 | **BUILD, P0** | Pass `scope` through `/api/v1/rag`, `/api/v1/retrieval`, `agents/governed.py`, MCP; add ACL filtering to keyword, vector and hybrid candidate stages; test with permission-leakage test J5 (target zero). |
| CAP-47 tenancy | Group-per-graph isolation of Graphiti on FalkorDB (graphiti-zep-08) as a reference | INV-graphiti-zep-02, INV-letta-02 (coarse or optional tenancy) | **BUILD, P0** | Adapter-level tenant enforcement; deny when scope is empty. |
| CAP-56 GraphRAG | STR-hipporag-01 (PPR at near-vanilla token cost), STR-hipporag-03 (hub down-weighting), STR-lightrag-01 (dual-level keys), STR-fast-graphrag-01, STR-raptor-01 (summary per ACL group with lineage) | INV-msgraphrag-01 (cost of community summaries), INV-msgraphrag-02 (summaries mix ACL groups), INV-hipporag-01 | **EXPERIMENT, P1**: wire `rag/dual_level_diffusion.py` behind a flag, compare with hybrid baseline | HippoRAG-style PPR is the only candidate with near-baseline query cost; community summaries need per-ACL-group build before use. REJECT MS-style global search as default. |
| CAP-55/53 hybrid and vector | STR-haystack-01 typed stages; STR-graphiti-zep-03 (graph-distance and mention rerankers); STR-mem0-02 (entity-link boost) | Two fusion implementations exist in EOIP (01a BL-15) | **BUILD, P1** | Consolidate weighted and RRF paths; see cohort 10 for the vector engine. |
| CAP-60 grounded answers | Cited-span check already present; STR-mem0-03 (per-signal score explanation) | LLM-emitted unvalidated citations (msgraphrag-13); INV-n4gr-01 | **REUSE EOIP, P2** | Extend claim-support to abstention-rate measurement. |
| CAP-57 agent memory | STR-graphiti-zep-01 (four-timestamp edges), STR-graphiti-zep-02 (model proposes, code closes interval), STR-letta-02 (git-versioned memory), STR-letta-03 (sleep-time consolidation as PROPOSED), STR-letta-04 (optimistic locking), STR-mem0-01 (single-call id-aliased extraction) | INV-graphiti-zep-03/-04, INV-letta-01, INV-cognee-02 (no governed supersession) | **BUILD, P1** | No memory plane exists. Specify write (PROPOSED), expire, invalidate, approve and erase, scoped by principal and tenant, reusing BL-37/39/40. |
| CAP-31 identity | STR-graphiti-zep-04 (deterministic-first resolution), STR-hipporag-02 (soft synonym edges as PROPOSED) | INV-lightrag-03, INV-n4gr-01 (string-key identity, destructive merge) | **INTEGRATE** via cohort 04 | EOIP ER is a library-only own implementation (BL-36). |
| CAP-32 extraction | STR-ragflow-01 (parser worker emitting SourceEvents) | INV-n4gr-01 (writers mutate the graph directly), INV-llamaindex-pgi-03 | **EXPERIMENT, P2** | Unstructured extraction must emit PROPOSED claims with spans, never write to the graph. |
| CAP-61 local models | STR-lightrag-03 (per-role model routing); KAG-Thinker and MiniRAG as small-model options | INV-openspg-kag-01 (72B-class dependence) | **EXPERIMENT, P2** | Evaluate small-model paths on CPU nodes; see cohort 14. |

## 7. Open questions

1. Does PPR diffusion (`rag/dual_level_diffusion.py`) beat the current hybrid path on an EOIP-shaped multi-hop corpus, and at what graph size does whole-graph PPR exceed a latency budget on one CPU node? (No evidence: hipporag dive.)
2. What is the abstention rate of the claim-support check, and how often does the extractive fallback fire with a CPU-class local model? (BL-16 note: requires a running local model.)
3. Should memory be a plane inside the governed graph (claims with validity) or a separate store keyed by principal? Tenant-erasure semantics decide (DSAR coverage in `privacy/dsr.py`).
4. Can the Zeng et al. unbiased protocol be reproduced locally, and which judge model is licensable for air-gapped evaluation?
5. Which of the library-only modules (U-14) is intended to be mounted: diffusion, hybrid vector service, memory?
6. Licence status of Think-on-Graph, StructRAG and WhyHow remains unverified; legal review before any reuse.
