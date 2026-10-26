# C08 — Cognee

| Field | Value |
|---|---|
| Registry ID | T-C08-cognee |
| Tier | A — memory/knowledge-graph pipeline competitor; open-source with dataset ACLs |
| Versions examined | v1.6.5 (stable; `pyproject.toml`, released 2026-10-16); v1.6.6rc1 (pre-release, flagged "Latest", 2026-10-23); v1.6.3-1.6.4 (2026-10-07..13) |
| Verified on | 2026-10-26 (brief states 2026-10-18; actual session date used) |
| Worker | V04 |

Cross-reference: `C08-graphiti-zep.md` (INV-graphiti-zep-02 "no permission model": Cognee differs, see §9/12). EOIP baseline for memory: `packages/eoip/memory_eng/engine.py`, `config/memory-policy.yaml`.

## 1. Identity, current status, tier, and sources

Cognee (GitHub `topoteretes/cognee`, company Topoteretes) is an "AI memory platform": ingest documents, code and conversations, build a knowledge graph plus vector index, and expose it to agents via Python/TypeScript/Rust SDKs, REST API, CLI and MCP [CLAIM-cognee-01]. Licence **Apache-2.0** (pyproject) [CLAIM-cognee-01]. Python 3.10-3.14. Very active: six releases in about three weeks, several with breaking changes [CLAIM-cognee-02]. A hosted Cognee Cloud exists with dataset-level team permissions [CLAIM-cognee-13]. Core operations in the 1.x vocabulary: `remember`, `recall`, `improve`, `forget` (older: `add`, `cognify`, `memify`, `search`) [CLAIM-cognee-03].

## 2. Primary problem, target workloads, concrete example workflows

Problem: persistent, queryable agent memory beyond vector-only RAG. Workloads: agent memory across sessions, document-to-graph, code graph (docstrings stored in the code graph in 1.6.5), session distillation into permanent memory.

| Workflow | Cognee path |
|---|---|
| Keyless local mode | Text ingest, retrieval and session storage with GLiNER extractor and local embeddings, no LLM key [CLAIM-cognee-03] |
| Build memory from documents | `add` -> `cognify` (classify, permission check, chunk, LLM graph extraction, summarise, embed) [CLAIM-cognee-04] |
| Enrich later | `memify` pipelines or `improve` (session persistence, entity consolidation, cross-connect, coding rules) [CLAIM-cognee-05] |
| Delete a customer's data | `forget(dataset=…, data_id=…)` [CLAIM-cognee-07] |
| Multi-user | Dataset ACL + `ENABLE_BACKEND_ACCESS_CONTROL` per-user/per-dataset databases [CLAIM-cognee-06] |

## 3. Feature inventory

| Feature | Status | Evidence |
|---|---|---|
| Python SDK, REST, CLI (`cognee-cli`), local UI, MCP server, TS SDK, Rust SDK (experimental), Claude Code/Codex plugins | Present | CLAIM-01, -13 |
| cognify pipeline with incremental loading (hash dedupe) | Present | CLAIM-04 |
| memify / improve enrichment pipelines | Present; `memify()` deprecated; no default tasks | CLAIM-05 |
| Custom graph models and OWL ontology guidance for entity naming | Present (details unread) | CLAIM-04 |
| Dataset-level ACL (read/write/delete/share), tenants, roles | Present | CLAIM-06 |
| Backend per-user/dataset isolation (Ladybug/Kuzu graph file + LanceDB per dataset) | Present when `ENABLE_BACKEND_ACCESS_CONTROL` | CLAIM-06 |
| Provenance recording | Optional, **off by default** (`PROVENANCE_TRACKING=true`) | CLAIM-04 |
| Contradiction checking | Separate `review_conflicts` stage of `improve`; removed from cognify | CLAIM-04 |
| Item/dataset/memory-only forget, history purge | Present | CLAIM-07 |
| Temporal graph (`temporal_cognify`) | **Removed** in v1.6.3 | CLAIM-02 |
| Graph backends: Ladybug (default), Kuzu, Neo4j, Neptune, Neptune Analytics, Memgraph (listed, unclear) | Present | CLAIM-09 |
| Vector: LanceDB (default), PGVector, ChromaDB, Neptune Analytics; Qdrant/Redis/FalkorDB community | Present | CLAIM-09 |
| Local LLM/embeddings: Ollama, llama.cpp, vLLM-style OpenAI-compatible, Fastembed | Present | CLAIM-09 |
| Graph query language exposure, SHACL, bitemporal, RBAC beyond datasets | Absent / unknown | — |
| Visualization endpoint/UI | Present | CLAIM-01 |

## 4. Architecture diagram

```
 add(data) --> relational metadata (SQLite default | Postgres) + raw files (.data_storage/<tenant|user>)
    |
    v  cognify pipeline (fixed): classify -> permission check (write on dataset) -> chunk
    |       -> LLM/GLiNER graph extraction -> chunk summary -> embed + add data points
    v
 +---------------------+      +--------------------------+
 | Graph store         |      | Vector store             |
 | Ladybug (Kuzu fork) |      | LanceDB | PGVector | ... |
 | | Neo4j | Neptune   |      +--------------------------+
 +---------------------+  per user/dataset files when ENABLE_BACKEND_ACCESS_CONTROL
    ^        ^
    | memify/improve: extraction tasks -> enrichment tasks (entity consolidation, cross-connect, rules, session persistence)
 recall(search) --> retrievers (e.g. GRAPH_COMPLETION, CoT variants) --> LLM answer
 forget(): item | dataset | everything | memory_only -> graph+vector+relational (+ best-effort session cache purge)
 Interfaces: Python/TS/Rust SDK, FastAPI, MCP, CLI, UI.   Control: users/tenants/roles + dataset ACL table.
```

## 5. Under-the-hood reconstruction

Source entry points (directory level, `main`): `cognee/modules`, `cognee/tasks`, `cognee/pipelines`, `cognee/memify_pipelines`, `cognee/memory`, `cognee/infrastructure`, `cognee/eval_framework`. Per-function pinned lines were not read.

| Layer | Verified | Hypothesis |
|---|---|---|
| Data model | `DataPoint` objects embedded + stored as graph nodes/edges; node and relationship ownership tracked per source document so shared entities survive until the last referencing item is deleted; relationships between surviving shared nodes are not removed by item deletion [CLAIM-08] | Pydantic-based models; custom graph models need `datamodel-code-generator >= 0.56.0` (1.6.5 breaking note) |
| Pipelines | cognify steps 1-6 fixed; two LLM calls per chunk (extraction + summary), `ceil(tokens/chunk) x 2`; `summary_method="from_extraction"` cuts to one; incremental loading/data cache default True; status `COMPLETED` skips items [CLAIM-04] | Task graph executed by an async runner with dlt for ingestion (dlt is a core dependency) |
| memify | Extraction tasks select/prepare graph data; enrichment tasks write nodes/edges; pipeline cache off; cross-connect proposes edges and `dry_run` defaults **False**; `memify()` deprecated -> `improve()`/`run_custom_pipeline()` [CLAIM-05] | — |
| Storage | Default Ladybug (Kuzu-compatible), LanceDB, SQLite; file name `cognee_graph_<provider>`; existing kuzu file reused by ladybug [CLAIM-09, -10] | Embedded engines make one-node-first trivial; concurrency across processes limited by file-lock semantics (hypothesis) |
| Retrieval | Search types incl. graph completion and chain-of-thought variants (vendor benchmark config GRAPH_COMPLETION_COT) [CLAIM-11] | Triplet embedding retrieval was removed in 1.6.5 breaking change [CLAIM-02] |
| ACL | `User`, `Tenant`, `Role`, ACL rows (principal, dataset, permission); effective permissions computed on demand (direct + role + tenant); capabilities `manage_users`, `grant_capabilities`, `revoke_capabilities` at tenant level; tenant owner holds all [CLAIM-06] | Enforcement at API/dataset boundary; no per-fact or per-chunk ACL |
| Isolation | `ENABLE_BACKEND_ACCESS_CONTROL=true`: auth mandatory; graph and vector isolated per user and dataset via `.cognee_system/databases/<user_uuid>/` files [CLAIM-06] | Physical (file-level) isolation, stronger than label filtering but multiplies stores |
| Forget | Item / dataset / everything / memory-only modes; no LLM or embedding calls; session cleanup "surgical" for item deletes; best-effort; deleted bytes may stay (LanceDB fragments until compaction; Ladybug file has no user-facing compaction) [CLAIM-07] | — |
| Versioning/time | `temporal_cognify` removed (1.6.3); no bitemporal model found; history = search/session history only | Graphiti (C08-graphiti-zep) is stronger here |
| Concurrency/transactions | NOT PUBLICLY VERIFIED | — |

## 6. Functional and non-functional requirements inferred

FR: dataset as unit of permission and deletion; idempotent re-ingest by content hash; pluggable extractor (LLM vs GLiNER); post-hoc enrichment that never merges entities (cross-connect proposes edges); deletion without LLM calls; purge of derived history on delete (1.6.6rc1). NFR: embedded defaults for single node; per-chunk LLM cost; Postgres/pgvector for production; weekly breaking changes imply pinned versions.

## 7. Performance and resource model

Cost model (documented): about `2 x ceil(tokens / chunk_size)` LLM calls per ingested document (10,000 tokens at 1,024 chunk size -> about 20 calls) [CLAIM-04]; keyless mode removes LLM calls for extraction. Local model notes: `OLLAMA_NUM_CTX` defaults to 2048, embeddings via Fastembed (`BAAI/bge-small-en-v1.5`, 384-d) or Ollama; extraction quality with small local models **UNVERIFIED**. Vendor benchmarks (labelled): Cognee blog, 2026-01-07, 24 HotPotQA questions, 45 runs per system on Modal, Cognee tuned config reported 0.93 human-like correctness, 0.85 DeepEval correctness, 0.84 F1 vs Mem0, Graphiti, LightRAG (competitor rows not recovered) [CLAIM-11]; README BEAM scores 0.79 at 100K tokens and 0.67 at 10M tokens, explicitly not comparable with each other [CLAIM-12]. No independent benchmark found; sample size 24 is small; vendor-run. Failure modes: LanceDB space not reclaimed (auto-pruning removed in 1.6.4, manual compaction) [CLAIM-02]; best-effort session purge; payment-error loop fixed 1.6.5.

## 8. Strengths and use-case-specific advantages

| Strength | Value | Match / exceed |
|---|---|---|
| Dataset-level ACL with tenants/roles/share plus per-dataset physical stores | Isolation story absent in many memory tools | Match concept; EOIP needs fact-level ACL (finer) |
| `forget` with item/dataset/memory-only modes and shared-node ownership | GDPR-style erasure and re-cognify | Exceed with tombstone + audit and non-destructive retire (BL-25, BL-37) |
| Keyless/GLiNER extraction path | Deterministic-ish, cheap, local | Match; supports EOIP "rules first, local model second" |
| Embedded defaults | One-node first | Match |
| Hash-based incremental ingest | Idempotency | EOIP has (BL-24) |
| Agent integrations (MCP, plugins) | Adoption | BL-47 |

## 9. Limitations with root causes

| Limitation | Class | Root cause | Evidence |
|---|---|---|---|
| Churn: breaking changes in nearly every release (temporal_cognify, triplet embeddings, nested agents, LanceDB pruning removed, dataset delete semantics) | Verified | Fast-moving 1.x | CLAIM-02 |
| Provenance off by default; no claim/evidence model; contradiction checking moved out of cognify | Verified design | Memory-first, not evidence-first | CLAIM-04 |
| ACL only at dataset granularity | Verified | Dataset is the unit of storage | CLAIM-06 |
| `forget` cleanup best-effort; deleted data may persist in files; docs say history-purge failure only warns while 1.6.6rc1 notes say forget now fails if purge fails | Verified + contradiction | Log-structured stores; docs lag | CLAIM-07, -02 |
| Per-user/dataset physical files multiply stores | Operational | Isolation by file | CLAIM-06 |
| Cross-connect `dry_run=False` by default writes edges | Verified | Default choice | CLAIM-05 |
| Default graph engine lineage Kuzu (archived upstream; Ladybug is the renamed engine) | Maturity risk | Dependency archival | CLAIM-10 |
| LLM cost per chunk (two calls) | Verified trade-off | LLM extraction | CLAIM-04 |
| Benchmarks vendor-run, tiny | Evidence quality | — | CLAIM-11 |
| Docs inconsistent (graph-stores page still says Kuzu default) | Doc | — | CLAIM-10 |

Algorithmic dead-ends: no graph-reasoning or formal ontology semantics; LLM extraction quality drives graph quality. Operational: file-based embedded stores; compaction. User friction: API renames (cognify/memify -> remember/improve).

## 10. Deployment, licensing, redistribution, and operational viability

Apache-2.0 core (permissive; includes patent grant — **legal review** still required for transitive dependencies and the Ladybug/Kuzu licence, not verified here). Docker image and Compose profiles, pip install, embedded defaults; Postgres/Neo4j/Neptune optional. Cognee Cloud is separate commercial. Air-gap: **partial** — local LLM via Ollama/llama.cpp and Fastembed possible, but Fastembed/GLiNER weights download on first use (default `~/.cognee/models`); telemetry/posthog extra exists (default on/off not verified: **UNVERIFIED**). Embedding as a library in a white-label product is licence-compatible on the evidence; community-vs-enterprise split: open-source engine vs hosted Cloud (features beyond dataset permissions not enumerated).

## 11. Competitive delta against the EOIP verified baseline

| Area | Cognee | EOIP baseline | Delta |
|---|---|---|---|
| Memory record | Graph+vector DataPoints, sessions, datasets | `MemoryEntry{entry_id, content, tier, relevance, ttl_seconds, tags, metadata, source}` in `memory_eng/engine.py:33`; **no ACL, tenant, evidence or validity fields** | Cognee ahead on structure and ACL |
| Retention | Explicit forget modes | `ttl_seconds` 2,592,000, `max_records` 1000, `max_bytes` 8 MiB (`config/memory-policy.yaml`); expiry eviction | EOIP has TTL; Cognee has data-subject delete |
| Tenant/ACL | Dataset ACL + file isolation | BL-17 metadata only, BL-18 Absent, BL-20 Partial | Cognee ahead |
| Temporal | Removed | BL-37 bitemporal Implemented | EOIP ahead (MemoryEntry itself is not bitemporal) |
| Evidence/contradiction | Optional provenance; `review_conflicts` | BL-39/41 Implemented | EOIP ahead |
| Extraction | LLM or GLiNER | Deterministic ingest (BL-26), person identity (BL-34) | Different; no memory-side extractor in EOIP |
| Egress | Provider selection | BL-45 | EOIP ahead |
| Backends | Ladybug/Kuzu, Neo4j, Neptune | HugeGraph, Neo4j, Neptune, Janus (BL-01..05) | Neo4j/Neptune overlap; HugeGraph unsupported in Cognee |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

**STR-cognee-01** | Cognee | Dataset ACL (read/write/delete/share) with tenant/role resolution computed on demand | CLAIM-06 | Memory access control | **match** | Add `tenant_id`, `principal_set`, `acl_hash` to memory records; resolve effective permission on read | Agent A cannot recall B's memory; 0 leaks over 1,000 randomized probes (J13).

**STR-cognee-02** | Cognee | Multi-mode forget (item/dataset/memory-only) without LLM calls, with shared-node ownership counting | CLAIM-07, -08 | Erasure and re-derivation | **exceed** | Implement as retire-with-tombstone + physical purge job; reference-count evidence per fact | Delete source S: facts only supported by S retired; shared facts keep other evidence; audit record written.

**STR-cognee-03** | Cognee | Keyless extractor (GLiNER) alternative to LLM | CLAIM-03, -04 | Cost/egress control | **integrate** (experiment) | Rule/dictionary extractor first, GLiNER second, LLM under egress policy | On IT corpus: >= X% of entities extracted without LLM (target set by POC; no number claimed).

**STR-cognee-04** | Cognee | Hash-based incremental ingest and skip of completed items | CLAIM-04 | Idempotency | **match** | Already BL-24; reuse for memory ingest | Re-ingest unchanged corpus -> 0 new writes.

**INV-cognee-01 — Seed hypothesis §10.5 "agent-memory systems: LLM-dependent extraction cost and latency": PARTIALLY VALIDATED.** Validated: default cognify makes two LLM calls per chunk [CLAIM-04]. Rejected in part: a documented keyless GLiNER path exists [CLAIM-03]; its quality is unmeasured. Target: Cognee 1.6.5, document-to-graph. Root cause: algorithm (proven). Alternative: rules first, local model second, LLM under policy; worse for unstructured prose with no schema where only an LLM yields relations. Options: (1) quick: Cognee as optional memory sidecar with Ollama; (2) native: `MemoryFact` through governed mutation path using deterministic extractors; (3) long-term: learned extractor distilled from approved assertions. Selected (2) then (3). POC: 200 documents; compare entity/relation F1 and tokens for rules, GLiNER, local LLM, remote LLM; success = rules+GLiNER within pre-agreed margin at zero egress. Failure cases: extractor hallucinated edges bypassing the gate; ACL lost on summaries. Defensibility: ACL + evidence + epistemic labels persist regardless of extractor. **Decision: EXPERIMENT.**

**INV-cognee-02 — Memory with no evidence, validity, or epistemic status by default (provenance off; contradictions separate).** Root cause: data model (proven). EOIP alternative: every memory is a PROPOSED claim with evidence_refs, validity interval and ACL (`ai/boundary.py`, BL-40); worse for ephemeral scratch memory where overhead outweighs value. Options: (1) wrap Cognee outputs as PROPOSED; (2) extend `MemoryEntry` into `MemoryFact`; (3) bitemporal memory graph. Selected (2). POC: contradiction ingest A then B — as-of reads correct, 0 physical deletes (shared with STR-graphiti-zep-01). **Decision: ADOPT.**

**INV-cognee-03 — Isolation by many embedded files; delete is best-effort and space not reclaimed.** Root cause: storage (proven). Alternative: backend-native tenant partition + verified purge/compaction job; worse for many tiny tenants on one node. POC: delete 10% of a 1M-fact tenant and verify bytes recoverable and no ghost recall (embedding probes). **Decision: EXPERIMENT.**

**INV-cognee-04 — Release volatility with breaking changes.** Root cause: maturity (proven by release list). Option: pin versions, wrap behind an adapter; do not take as hard dependency. **Decision: ADOPT (pinning rule).**

## 13. Per-capability decisions

| Capability | Decision |
|---|---|
| CAP-57 agent memory write/expire/invalidate | BUILD native in EOIP (extend `memory_eng`) |
| CAP-46/47 ACL + tenancy on memory | BUILD (pattern from Cognee dataset ACL, fact-level) |
| CAP-32 extraction with GLiNER | EXPERIMENT (INTEGRATE if POC passes) |
| CAP-53 LanceDB/PGVector as optional vector module | EXPERIMENT |
| Cognee as a runtime dependency | DEFER (churn, embedded stores, backend mismatch) |
| CAP-56 graph retrieval variants | EXPERIMENT against strong non-graph baseline |
| CAP-74 deletion/erasure workflow | BUILD |
| Kuzu/Ladybug as embedded engine | DEFER (archival lineage; see C03 deep dive owners) |

## 14. Concrete tests, proof-of-concept, and acceptance conditions

1. Install v1.6.5 in a venv with Ollama + Fastembed, egress blocked after model seeding; ingest 50 docs; record RAM/disk/time. 2. ACL probe: two users, two datasets, `ENABLE_BACKEND_ACCESS_CONTROL=true`, search each other's content, expect zero hits. 3. Forget probe: forget item, search for its facts and verbatim text, inspect LanceDB/graph files for residue. 4. Extractor comparison (INV-01). 5. Reproduce the HotPotQA comparison from `cognee/evals` with identical judge and report variance; acceptance: documented results within CI before any claim. 6. EOIP side: add `tenant_id` and ACL to `MemoryEntry`, and a test that `recall` filters by principal.

## 15. Risks, trade-offs, and open research questions

Risks: licence of Ladybug/Kuzu and transitive deps unreviewed; telemetry defaults; pre-release channel labelled "Latest" on GitHub (v1.6.6rc1) — pin to stable; vendor benchmark bias. Open: how ACL behaves for shared nodes across datasets (shared-node deletion implies cross-document sharing inside a dataset only); concurrency semantics of embedded stores; extraction quality on small local models; whether GLiNER weights have redistribution constraints.

---

## Appendix A — Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | Apache-2.0, v1.6.5/1.6.6rc1, Topoteretes |
| D2 | 2 | Agent memory, doc-to-graph |
| D3 | 4, 5 | Pipelines, stores, ACL |
| D4 | 5 | LanceDB, Ladybug; layout detail unread |
| D5 | 3, 5 | Custom graph models, OWL guidance; no SHACL |
| D6 | 5 | Retrievers; no query language |
| D7 | — | N/A: no reasoning engine |
| D8 | 5, 7 | Concurrency NOT VERIFIED |
| D9 | 3, 4, 5 | dlt ingestion, incremental, connectors via extras |
| D10 | 5, 9 | Entity consolidation, no merge in cross-connect; ER unverified |
| D11 | 5, 9 | Temporal removed |
| D12 | — | N/A |
| D13 | 2, 5, 7 | recall/improve, MCP, forget rules |
| D14 | — | N/A |
| D15 | 3 | Capabilities model |
| D16 | 3 | Local UI, visualization |
| D17 | 3 | SDKs, plugins, custom pipelines |
| D18 | 5, 9 | ACL, isolation; injection defence not examined |
| D19 | 5, 8 | Tenant/role/dataset; per-user files |
| D20 | 7 | LLM-call model; no independent numbers |
| D21 | 1, 10 | OSS + Cloud |
| D22 | 9 | Graph file formats; Kuzu->Ladybug |
| D23 | — | N/A not reviewed |
| D24 | App. C | Vendor evals labelled |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-57 | native | 03, 05, 07 | MemoryEntry (no BL-ID; engine.py:33) Partial | BUILD | P1 |
| CAP-46 | partial (dataset-level) | 06 | BL-18 Absent | BUILD | P0 |
| CAP-47 | native (file-level) | 06 | BL-20 Partial | BUILD | P0 |
| CAP-32 | native (LLM/GLiNER) | 03, 04 | BL-26 | EXPERIMENT | P2 |
| CAP-38 | partial (optional) | 04 | BL-41 Implemented | REFERENCE | P3 |
| CAP-39 | partial (`review_conflicts`) | 04 | BL-39 Implemented | REFERENCE | P3 |
| CAP-34 | absent (removed) | 02 | BL-37 Implemented | REFERENCE | P3 |
| CAP-53 | native | 09 | BL-14 Partial | EXPERIMENT | P2 |
| CAP-61 | native | 09 | Implemented | REUSE | P2 |
| CAP-59 | native | 01 | BL-47 | REFERENCE | P3 |
| CAP-74 | native (forget) | 07 | BL-50 | BUILD | P1 |
| CAP-78 | partial (eval_framework) | 11, 12 | — | EXPERIMENT | P2 |

## Appendix C — Evidence records (access date 2026-10-26)

| CLAIM-ID | Product / version / date | Exact claim | Classification | Source + URL | Pub / access | Confidence | Contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-cognee-01 | Cognee 1.6.5 | Apache-2.0; Python >=3.10,<3.15; core deps include lancedb, ladybug, networkx, rdflib, fastembed, litellm, dlt, fastapi; extras neo4j, neptune, postgres, ollama, llama-cpp, gliner, evals; README: "free open-source AI memory platform" with MCP, Python/TS SDKs, Rust, REST, Docker | Observed in source code | https://raw.githubusercontent.com/topoteretes/cognee/main/pyproject.toml ; https://github.com/topoteretes/cognee | undated / 2026-10-26 | 0.85 | pyproject on main said 1.6.5 while release list showed 1.6.6rc1 |
| CLAIM-cognee-02 | Cognee releases | v1.6.6rc1 (2026-10-23, pre-release, marked Latest): dataset delete purges search/conversation history (breaking), `forget(clean_history=True)`, forget fails if purge fails; v1.6.5 (2026-10-16); triplet embedding removed; v1.6.4 LanceDB auto-pruning removed; v1.6.3 `temporal_cognify` removed, nested agents disallowed | Officially documented | https://github.com/topoteretes/cognee/releases | 2026-10 / 2026-10-26 | 0.8 | forget docs say cleanup is best-effort |
| CLAIM-cognee-03 | README | Operations remember/recall/improve/forget; keyless local mode with GLiNER extractor and local embedding; session distillation | Vendor claim | https://github.com/topoteretes/cognee | undated / 2026-10-26 | 0.7 | Local-mode quality unmeasured |
| CLAIM-cognee-04 | cognify docs | Steps: classify, check write permission, chunk, LLM graph extraction, summarise, embed/add data points; provenance off unless `PROVENANCE_TRACKING=true`; contradiction check separate `review_conflicts` in `improve`; two LLM calls per chunk; incremental loading/data_cache default True; GLiNER via `GRAPH_EXTRACTOR=gliner_demo` | Officially documented | https://docs.cognee.ai/core-concepts/main-operations/cognify | undated / 2026-10-26 | 0.8 | — |
| CLAIM-cognee-05 | memify docs | No default tasks; `cognee.memify()` deprecated; built-ins: session persistence, entity consolidation, cross-connect (proposes edges, never merges; `dry_run` default False), coding rules; pipeline cache off | Officially documented | https://docs.cognee.ai/core-concepts/main-operations/memify | undated / 2026-10-26 | 0.8 | — |
| CLAIM-cognee-06 | permissions docs | Permissions at dataset level (read/write/delete/share); principals user/tenant/role; ACL rows; effective permissions computed on demand; capabilities manage_users, grant/revoke_capabilities; `ENABLE_BACKEND_ACCESS_CONTROL` => mandatory auth, per-user per-dataset graph and vector isolation under `.cognee_system/databases/<user_uuid>/` | Officially documented | https://docs.cognee.ai/core-concepts/multi-user-mode/permissions-system/overview | undated / 2026-10-26 | 0.8 | Cloud docs describe dataset permissions only |
| CLAIM-cognee-07 | forget docs | Modes item/dataset/everything/memory-only; no LLM or embedding calls; session history cleanup best-effort; deleted bytes may remain (LanceDB fragments; Ladybug no user-facing compaction); delete permission required | Officially documented | https://docs.cognee.ai/core-concepts/main-operations/forget | undated / 2026-10-26 | 0.8 | CLAIM-02 says forget fails if purge fails |
| CLAIM-cognee-08 | delete docs | Ownership of nodes/relationships tracked per source document; shared entity removed only with last referencing item; `prune` bypasses permissions, dev only | Officially documented | https://docs.cognee.ai/core-concepts/main-operations/delete | undated / 2026-10-26 | 0.75 | Container-deletion behaviour unclear |
| CLAIM-cognee-09 | setup docs | Defaults SQLite, LanceDB, Ladybug; alternatives Postgres, PGVector, Chroma, Neptune Analytics, Kuzu, Neo4j, Neptune, Memgraph (unclear); Ollama, llama.cpp, OpenAI-compatible; Fastembed `BAAI/bge-small-en-v1.5` 384-d; `OLLAMA_NUM_CTX` default 2048 | Officially documented | https://docs.cognee.ai/setup-configuration/overview | undated / 2026-10-26 | 0.8 | Graph-stores page lists Kuzu as default |
| CLAIM-cognee-10 | Ladybug guide / Kuzu | Ladybug is Cognee's default embedded graph DB, a renamed Kuzu engine; file name `cognee_graph_<provider>`; Kuzu archived (third-party post Aug 2026) | Officially documented + third-party | https://docs.cognee.ai/guides/ladybug ; https://oneuptime.com/blog/post/2026-08-12-kuzu-to-ladybugdb-packages-apis-extensions-database-files/markdown | 2026-08-12 / 2026-10-26 | 0.6 | Master Prompt reports Kuzu archived 2025-10-10 (not re-verified here) |
| CLAIM-cognee-11 | Cognee benchmark blog | 24 HotPotQA questions, 45 runs per system; tuned Cognee 0.93 human-like, 0.85 DeepEval correctness, 0.84 F1; competitor rows not recovered | Vendor claim | https://www.cognee.ai/blog/deep-dives/knowledge-graph-memory-benchmarks | 2026-01-07 / 2026-10-26 | 0.4 | Third-party repeat is not independent |
| CLAIM-cognee-12 | README BEAM | 0.79 at 100K tokens (fixed hybrid retrieval); 0.67 at 10M tokens (exploratory with question-type routing); different conversations/procedures | Vendor claim | https://github.com/topoteretes/cognee | undated / 2026-10-26 | 0.4 | — |
| CLAIM-cognee-13 | Cognee docs | Cloud offers dataset-level permissions; self-hosted engine runs with embedded databases or own infrastructure | Officially documented | https://docs.cognee.ai/ | undated / 2026-10-26 | 0.7 | — |

## Appendix D — Assumptions

A1 Access date 2026-10-26. A2 "Stable" taken as v1.6.5 since v1.6.6rc1 is a release candidate. A3 Cognee evaluation repo not run. A4 Ladybug/Kuzu licence and telemetry defaults not checked. A5 EOIP memory comparison limited to the dataclass fields and policy file read in this session.
