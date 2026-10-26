# C08 — Letta (formerly MemGPT)

| Field | Value |
|---|---|
| Registry ID | T-C08-letta |
| Tier | A — stateful-agent runtime with the most explicit memory-tier design (blocks, archival, recall, sleep-time); reference for CAP-57 and the "memory is files in git" counter-pattern |
| Versions examined | Server line `letta` PyPI 0.16.8 (2026-05-14, last server release; wheel unpacked and read); product line **Letta Code** `@letta-ai/letta-code` npm 0.34.24 (2026-10-25) and PyPI `letta` 0.34.12 (2026-10-12); MemGPT paper arXiv:2310.08560 (2023-10-12); sleep-time compute paper arXiv:2504.13171 (2025-04-17) |
| Verified on | 2026-10-26 |
| Worker | V07 (batch for W20 scope) |

## 1. Identity, current status, tier, and sources

- **Owner/identity.** Letta (company) — `letta-ai/letta` (25.3k stars), `letta-ai/letta-code` (3.7k stars). Letta is the rename of MemGPT; the MemGPT paper authors (Packer, Wooders, Lin, Fang, Patil, Stoica, Gonzalez) are the founders [CLAIM-letta-12].
- **Major trap — the product changed shape in 2026.** (a) The PyPI name `letta` was the Python **server** up to 0.16.8 (2026-05-14); from then on the same name ships **Letta Code**, a terminal agent CLI with a bundled Node runtime ("a CLI rather than a Python SDK") [CLAIM-letta-01]. (b) The `letta-ai/letta` README now says the repo is no longer the main source: active development moved to `letta-code`; the **retired "Letta V1 API server" lives on the `archive` branch** [CLAIM-letta-02]. (c) Docs describe MemFS (git-tracked markdown memory) as the current memory model, with "memory blocks" described as the older/legacy system for servers that lack MemFS [CLAIM-letta-06]. Any blog or tutorial describing `pip install letta` + `letta server` with Postgres is describing the archived V1 line.
- **Licence.** Apache-2.0 for the server wheel (METADATA "License: Apache License"), `letta` repo, `letta-code` repo and npm package [CLAIM-letta-01][CLAIM-letta-03]. Cloud (Letta Cloud) is a separate commercial service with plan limits (Free 5 MiB / Pro 50 MiB per memory repository) [CLAIM-letta-07]. Redistribution: permissive code; legal-review note only for the cloud/commercial boundary.
- **Status.** Very active (letta-code ships several releases per week); pre-1.0 (0.x) and re-architected twice in 12 months -> high API churn.
- Sources used (13): PyPI JSON for `letta`; npm registry for `@letta-ai/letta-code`; GitHub READMEs (`letta`, `letta-code`, archive branch); docs.letta.com install, self-hosting, MemFS concept, memory-configuration pages; search-surfaced docs for Docker, sleep-time, dreaming; 0.16.8 wheel source; arXiv papers 2310.08560 and 2504.13171; Letta benchmark blog (2025-08-12). Cross-references: `C08-mem0.md` (LoCoMo dispute), `C08-graphiti-zep.md`, `C08-cognee.md`.

## 2. Primary problem, target workloads, concrete example workflows

Problem: LLM context windows are finite; agents need persistent identity and self-managed memory. MemGPT's "virtual context management" lets the model page information between in-context memory and external storage using tool calls, like OS paging [CLAIM-letta-12]. Workloads: long-lived personal/assistant agents, coding agents (Letta Code), multi-agent systems sharing memory blocks, always-on agents behind messaging channels (Slack, Telegram, Discord, WhatsApp, Signal).

Workflows (verified): (1) agent edits its own always-in-context memory via `memory_*` tools (replace/insert/rethink/patch/rename/delete) [CLAIM-letta-09]; (2) agent recalls with `conversation_search` (past messages) and `archival_memory_search` (vector store) [CLAIM-letta-09]; (3) every N user turns or at context compaction, a background "dreaming"/sleep-time agent reviews recent conversation and rewrites memory without blocking the main agent [CLAIM-letta-07][CLAIM-letta-10].

## 3. Feature inventory

| Feature | Status | Surface | Evidence |
|---|---|---|---|
| Core memory blocks (label, value, char limit, read_only, description) always in prompt | Present in V1 server; "legacy" in current docs | API/SDK/ADE | CLAIM-08 |
| MemFS: per-agent git repo of markdown; root files in system prompt; `MEMORY.md` indexed dirs on demand | Present (current) | CLI, App Server | CLAIM-06 |
| Archival memory (vector passages with tags) | Present (V1 server) | tools/API | CLAIM-08, -09 |
| Recall memory (`conversation_search` over message history) | Present | tool | CLAIM-09 |
| Sleep-time agents / "dreaming" / "memory doctor" | Present (docs label V1 sleep-time architecture experimental — low confidence) | config | CLAIM-07, -10, -15 |
| Shared memory blocks across agents (groups: supervisor, round-robin, dynamic, sleeptime) | Present | API | CLAIM-10 |
| Identities (per-end-user object linked to agents and blocks) | Present (V1 server) | API | CLAIM-08 |
| Organization scoping (`organization_id` on every ORM row) | Present; **single-level, "all permissions"** | server | CLAIM-08 |
| Per-block/per-fact ACL, source-ACL, ReBAC | **Absent** | – | CLAIM-08 |
| Block version history + optimistic locking | Present (BlockHistory, version col) | server | CLAIM-08 |
| Git commit history of memory (MemFS) | Present | CLI | CLAIM-06 |
| Knowledge graph / typed relations | **Absent** (memory is text blocks/files/passages) | – | CLAIM-08 |
| Temporal validity/bitemporal facts | Absent (git history + created_at only) | – | CLAIM-06, -08 |
| Local models: Ollama, LM Studio, llama.cpp (App Server); vLLM, SGLang, Ollama, LM Studio providers in V1 server | Present | CLI/server | CLAIM-04, -11 |
| MCP tools, custom tools, tool sandboxes | Present | server | wheel `services/mcp`, `tool_sandbox` |
| Channels (Slack, Telegram, Discord, WhatsApp, Signal) | Present (current) | App Server | CLAIM-04 |
| Self-hosted App Server with bearer token | Present | `letta server --backend local` | CLAIM-04 |
| Telemetry/observability (OTel, ClickHouse traces in V1 server) | Present, optional | server | CLAIM-11 |

## 4. Architecture diagram

```
CURRENT (2026)                                          ARCHIVED V1 SERVER (pip letta <= 0.16.8)
 Letta Code CLI / desktop / web (chat.letta.com)         Client SDK / ADE ──REST──► FastAPI server
        │ (agent harness runs on user's computer)                │ organization_id on every row
        ▼                                                         ▼
 App Server (`letta server --backend local`,             Agent loop (LettaAgentV3) ──► LLM providers (OpenAI, Anthropic, Ollama, vLLM, LM Studio, SGLang …)
   ws://…:4500, LETTA_APP_SERVER_TOKEN;                   │ tools: memory_*/core_memory_*, archival_memory_*, conversation_search, MCP, sandbox
   shell+filesystem access on host)                       ▼
        │                                                 Postgres (letta_pg_uri) or SQLite ── blocks(+history), passages(CommonVector, tags), messages, identities, groups
        ▼                                                 optional: Turbopuffer/Pinecone vectors, ClickHouse traces, Redis
 MemFS: per-agent git repo (~/.letta/lc-local-backend/memfs/<agent>/memory)   Sleep-time group: primary agent + sleeping agent share blocks (frequency counter)
   dreaming / memory-doctor subagents via git worktrees                     MemFS service: git CLI over object storage (local/GCS/S3)
 Letta Cloud (optional): hosted repo, backup, cross-device sync
```

## 5. Under-the-hood reconstruction (V1 server wheel 0.16.8 read; current App Server NOT PUBLICLY VERIFIED beyond docs)

**Data model (V1).** `Block`: `label`, `value` (text), `limit` (char cap, default `CORE_MEMORY_BLOCK_CHAR_LIMIT`), `read_only`, `hidden`, `description`, `metadata_`, template flags, `version` (SQLAlchemy `version_id_col` optimistic lock) and `current_history_entry_id` -> `BlockHistory`; many-to-many to agents, identities, groups, conversations; `organization_id` mandatory via `OrganizationMixin` [CLAIM-letta-08]. `Passage`: id, text, `embedding` (`CommonVector` column: pgvector on Postgres, emulated on SQLite via `sqlite_functions`), `embedding_config`, `metadata_`, `tags` (+ `PassageTag` table), per-archive scoping [CLAIM-letta-08]. `Identity` ties an external user id to agents/blocks with a unique (identifier_key, project, organization) constraint. Entities are rows of opaque text; there are **no edges between memories**.

**Memory API as tools.** The agent, not the platform, decides what to remember: `core_memory_append/replace`, `memory_insert/replace/rethink/apply_patch/str_replace/str_insert/create/rename/delete/update_description`, `memory_finish_edits`, `archival_memory_insert/search`, `conversation_search` [CLAIM-letta-09]. Eviction of context to recall memory is automatic (summariser service) — mechanism not read in detail (hypothesis from `services/summarizer` directory name).

**Context assembly (hypothesis from structure + paper).** `compile(memory) -> system prompt` embeds every block with its label, description, size/limit; messages are windowed; when over budget the summariser compacts and old messages remain searchable via `conversation_search`. Limits are character counts, not tokens.

**Sleep-time.** `ManagerType.sleeptime` groups: the primary agent's request increments `turns_counter`; when `counter % sleeptime_agent_frequency == 0` the group spawns a background run of the sleep-time agent, which has tools to edit the primary's **shared blocks**; four generations of implementation exist (v1-v4) [CLAIM-letta-10]. The paper's claim is test-time compute is shifted offline; reported 5x lower test-time compute at equal accuracy on stateful math tasks, up to +13%/+18% accuracy, 2.5x lower amortised cost — on synthetic *stateful GSM-Symbolic/AIME*, not memory-QA [CLAIM-letta-13].

**MemFS (current).** Memory = markdown files in a per-agent git repo; root files go into the system prompt every turn; directories with `MEMORY.md` are lazily loaded; the agent edits with ordinary file tools; commits give history; dreaming/memory-doctor subagents use git worktrees to avoid blocking; local-only agents are backed up by the user; cloud repos have plan size limits [CLAIM-letta-06][CLAIM-letta-07]. V1 server MemFS code (`services/memory_repo/git_operations.py`) shells out to the `git` CLI over a pluggable storage backend (local, S3/GCS) [wheel].

**Security/tenancy.** Row filter `apply_access_predicate(actor, access)` adds `organization_id = actor.organization_id`; the `access` argument is explicitly discarded ("entrypoint for row-level permissions. Defaults to same org as the actor, all permissions at the moment") [CLAIM-letta-08]. An alternate `AccessType.USER` filters by `user_id`. App Server: single bearer token; docs warn it "has shell and filesystem access on its host" and that self-hosted tenant isolation/per-user access control is not described [CLAIM-letta-04].

**Concurrency/transactions.** Optimistic locking on blocks; deadlock/lock-timeout handling in the ORM base; git worktrees for concurrent memory edits. Partitioning: none (single DB/repo). Caching: Redis optional (hypothesis from imports). Versioning: BlockHistory rows (V1), git commits (current).

## 6. Functional and non-functional requirements inferred

| ID | Requirement | Basis |
|---|---|---|
| FR-L1 | Always-in-context "core" tier with hard size limit and read-only option | CLAIM-08 |
| FR-L2 | Searchable cold tiers: archival (vector+tags) and recall (message search) | CLAIM-09 |
| FR-L3 | Background consolidation that edits memory without blocking the user turn | CLAIM-06, -10 |
| FR-L4 | Versioned memory with history and optimistic concurrency | CLAIM-06, -08 |
| FR-L5 | Shared memory between cooperating agents | CLAIM-10 |
| NFR-L1 | Local-model support without cloud account | CLAIM-04 |
| NFR-L2 | Agent-driven memory writes require governance (here absent): review gate, ACL, audit | gap |

## 7. Performance and resource model

No independent benchmark found. Vendor claims: filesystem agent 74.0% on LoCoMo with gpt-4o-mini, compared with Mem0's self-reported 68.5% graph variant [CLAIM-letta-14] — **contested** (Mem0 and Zep publish different numbers under different configurations; see `C08-mem0.md` CLAIM-mem0-16..18; Letta also disputes Mem0's MemGPT run). Sleep-time paper numbers are on synthetic math tasks (above) and not transferable to memory QA [CLAIM-letta-13]. Resource model (derived, hypothesis): every memory edit is an LLM tool call (cost grows with agent self-management); dreaming "uses more model tokens and does not ask you for approval" [CLAIM-letta-07]; core blocks consume prompt tokens on every turn (size-limited by design); V1 server needs Postgres+pgvector for production; MemFS repos are small (cloud caps 5/50 MiB). Failure modes: model forgets to save or overwrites a block (rethink/replace are destructive in-context, recoverable only via history); background dreaming can silently rewrite memory; local models with weak tool-calling degrade memory discipline (hypothesis).

## 8. Strengths and use-case-specific advantages

- Clean tier vocabulary (core/recall/archival) with an explicit per-block size budget — easy to reason about prompt cost.
- Memory-as-git-files: free history, diff, review, rollback, offline editing; human-auditable; the strongest governance-friendly idea in the agent-memory field.
- Sleep-time/dreaming: consolidation off the critical path with a cheaper model.
- Shared blocks for multi-agent teams; read-only blocks for policy text.
- Apache-2.0, runs against local model servers, no vendor account needed for local mode.

## 9. Limitations with root causes

| Class | Limitation | Type | Evidence |
|---|---|---|---|
| Algorithmic | Memory is unstructured text; no entity identity, relations, contradiction logic, or temporal validity | Design | CLAIM-08 |
| Algorithmic | Quality depends on the agent LLM correctly calling memory tools (self-editing) | Inherent | CLAIM-09 |
| Operational | Dreaming rewrites memory automatically without approval; extra token cost | Verified | CLAIM-07 |
| Operational | Self-hosted agents: no automatic backup; built-in tools run with host shell/filesystem access | Verified | CLAIM-04 |
| Friction | Re-architected in 2026: V1 server archived; PyPI name reused for a CLI; docs describe Docker as deprecated on one page and as the self-hosting path on another | Verified, contradictory | CLAIM-01, -02, -05 |
| Security | Org-level scoping only; `access` argument ignored; no per-fact ACL; App Server has a single shared token | Verified | CLAIM-04, -08 |
| Friction | Self-hosted multi-tenant story not documented | Verified (absence) | CLAIM-04 |
| Quality | Public memory benchmark number is vendor-run, filesystem baseline, contested | Contested | CLAIM-14 |

## 10. Deployment, licensing, redistribution, operational viability

- **Licence class: permissive (Apache-2.0).** No copyleft; commercial cloud separate. Trademark ("Letta") not for white-label reuse (standard; no text found, not verified).
- **Air-gap: partial-to-yes** for local mode: `letta --backend local connect ollama`, `letta server --backend local --listen ws://127.0.0.1:4500`; state under `~/.letta/lc-local-backend` [CLAIM-letta-04]. Default experience nudges `/login` (cloud backup) and chat.letta.com; V1 server telemetry optional (OTel/ClickHouse). Node.js >= 22.19 runtime for the CLI.
- **One-node:** yes. V1 server: Postgres or SQLite.
- **Fit as embedded component:** poor; Letta is an agent runtime/harness, not a memory service you call from your own agents. Pattern reuse (blocks + git-versioned memory) is the realistic path.

## 11. Competitive delta against EOIP verified baseline

| Area | Letta | EOIP | Delta |
|---|---|---|---|
| Tiering | core/recall/archival, char budgets | `MemoryTier` WORKING/…, decay functions, promote/consolidate in `memory_eng/engine.py` | EOIP has tiers + decay + consolidation graph; lacks explicit prompt-budgeted always-on tier and background consolidation worker |
| Versioning | git commits / BlockHistory | revisions + bitemporal (BL-37), diff/snapshots (BL-38) — graph-level | EOIP ahead structurally; memory stores themselves unversioned |
| Governance | none | BL-40 PROPOSED-until-validated, egress gateway BL-45 | EOIP can gate agent memory writes; Letta's agent writes directly |
| ACL/tenant | org id only | BL-18 Absent, BL-20 Partial; memory entries have no tenant/ACL/evidence fields | Neither solves; EOIP target is finer |
| Agent memory policy | tool-driven | `config/memory-policy.yaml` (ttl 30 d, 1000 records, 8 MiB), `agents/memory.py` task-outcome stubs | EOIP policy is a retention cap only |
| Graph structure | none | GraphStore, GraphRAG BL-16 | EOIP ahead |

## 12. Strength-adoption cards and inversion cards

| ID | Competitor | Strength | Evidence | Value to EOIP | Verdict | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-letta-01 | Letta | Prompt-budgeted always-on memory tier with read-only blocks | CLAIM-08 | Predictable context cost; policy text pinned | match | `CoreMemoryBlock{label,value,char_limit,read_only,acl_hash,tenant_id}` per agent, loaded only after ACL check | Prompt never exceeds budget; read-only block edit attempt rejected and audited |
| STR-letta-02 | Letta | Memory as versioned, human-reviewable files in git | CLAIM-06 | Review/rollback for agent memory; fits EOIP GitOps moat | integrate (pattern) | Render core/archival memory to markdown in `ontology/gitops.py`-style repo; PR review for promoted memory | Any agent memory change reproducible from a commit; revert restores answers |
| STR-letta-03 | Letta | Sleep-time consolidation off the critical path | CLAIM-07, -10 | Cheaper, better memory hygiene | match | Worker job (existing worker app) that proposes memory edits as PROPOSED assertions, not writes | Dreaming produces 0 direct writes; reviewer accepts/rejects; token cost per 100 turns logged |
| STR-letta-04 | Letta | Optimistic locking + history on shared blocks | CLAIM-08 | Safe multi-agent shared memory | match | Version column on memory facts; compare-and-swap in mutation gateway | Concurrent writers: 0 lost updates in 1k races |

**INV-letta-01 — Agent self-edits memory with no governance (proven, governance).** Evidence: memory tools write directly; dreaming runs without approval [CLAIM-07][CLAIM-09]. Alternative: agent *proposes* memory changes (PROPOSED, BL-40), validation gate checks schema/ACL/contradiction, human or policy promotes. Worse when: low-stakes single-user chat where latency matters. Options: (a) wrap Letta tools with a review proxy; (b) native proposal queue + auto-promote rules; (c) long-term: memory as graph assertions with evidence and calibration. Selected (b). POC: 1k agent turns, measure poisoned/incorrect memory writes admitted (target < 1% vs ungoverned baseline) and added latency (< 200 ms p95). Defensibility: epistemic separation + audit is enterprise-grade. **ADOPT.**

**INV-letta-02 — Coarse org-level tenancy; discarded `access` argument (proven, governance).** Alternative: tenant + principal + source-ACL on each memory row, enforced in retrieval (closes memory slice of BL-18/BL-20). POC as in `C08-mem0.md` INV-mem0-02. **ADOPT.**

**INV-letta-03 — Unstructured text memory without entities/relations/time (proven, data model).** Alternative: typed memory facts linked to EOIP entities and valid-time (see `C08-graphiti-zep.md` STR-01). Worse when: tiny personal agents. **ADOPT** (pattern gap, EOIP differentiator).

**INV-letta-04 — Product/packaging instability (proven, maturity/licensing-adjacent).** V1 server retired, name reused, contradictory docs. Mitigation: never depend on Letta runtime; consume ideas only. Decision: **REJECT as runtime dependency.**

**Seed §10.5 "Graphiti / agent-memory: LLM-dependent extraction cost"** — for Letta: **VALIDATED, worse**: every memory operation is a model-driven tool call plus background dreaming tokens [CLAIM-07]. EOIP rule-first cascade (see C08-graphiti-zep INV-01) applies.

**INV-SELF-letta-01 (EOIP weakness).** No always-on prompt-budgeted memory tier and no background consolidation worker; `MemoryEngine.consolidate` is a counter-based in-process routine without review. Fix: STR-01/-03. **ADOPT.**

## 13. Per-capability decisions

| Capability | Decision | Reason |
|---|---|---|
| CAP-57 memory tiers (core/archival/recall) | BUILD in `memory_eng` over governed store | STR-01 |
| CAP-35/CAP-36 versioned memory history | REUSE EOIP revisions + EXPERIMENT git-rendered memory | STR-02 |
| Sleep-time consolidation | BUILD as proposal-only worker | STR-03, INV-01 |
| Shared multi-agent memory with locking | BUILD | STR-04 |
| CAP-46/47 memory ACL/tenant | BUILD | INV-02 |
| Letta runtime / App Server | REJECT as dependency; REFERENCE-ONLY | INV-04, App Server shell access |
| CAP-61 local models | INTEGRATE through EOIP provider abstraction (Ollama/vLLM) | – |

## 14. Concrete tests, POC, acceptance conditions (all PROPOSED; none run)

1. **Local-only run:** install Letta Code, `letta --backend local connect ollama`, 24 h packet capture with an agent conversation; pass = zero traffic except localhost and the model server (check `/login` nudges, update checks).
2. **Memory discipline with local models:** 100 scripted sessions with 3 local models; measure facts the agent should have saved vs saved, and wrongful overwrites.
3. **Dreaming governance POC:** run dreaming-equivalent on EOIP worker, count proposals promoted vs rejected, regression on recall questions.
4. **MemFS vs graph store:** same 200 facts stored as markdown files vs governed graph facts; compare retrieval accuracy and edit auditability.
5. **Concurrency:** 1k concurrent shared-block edits; lost updates = 0.
6. **LoCoMo/LongMemEval** under the shared harness in `C08-mem0.md` test 5; report filesystem-baseline strength honestly (grep-style retrieval is a strong baseline per Letta; verify).

## 15. Risks, trade-offs, open research questions

Risks: chasing a moving target (two rewrites); agent-written memory as prompt-injection persistence channel (a poisoned document can instruct the agent to store malicious "memory", hypothesis); git-file memory scales poorly beyond thousands of files without an index. Open: Does the current App Server (not archived V1) have a DB/tenant model? (NOT PUBLICLY VERIFIED.) Does MemFS plus a lightweight index match graph memory on multi-hop questions? What are the actual dreaming defaults and models? How does Letta's "memory doctor" subagent decide edits (undocumented in sources read)?

---

## Appendix A — Research-dimension coverage

| Dimension | Sections | Summary / N/A reason |
|---|---|---|
| D1 Identity and maturity | 1, 10 | MemGPT->Letta; Apache-2.0; 2026 re-architecture |
| D2 Problem/workloads | 2 | stateful agents |
| D3 Architecture | 4, 5 | V1 server vs App Server/MemFS |
| D4 Storage/indexing | 5 | Postgres/SQLite rows, pgvector; git repo |
| D5 Schema/semantics | 5, 9 | text blocks; none |
| D6 Query pipeline | 5 | vector + message search tools |
| D7 Reasoning | N/A | LLM only |
| D8 Transactions/scale | 5 | optimistic locks, worktrees; no sharding |
| D9 Ingestion/federation | 3 | file sources, MCP tools; no CDC |
| D10 Identity/evidence | 3, 9 | Identity object only; no evidence |
| D11 Time/evolution | 5 | history/git; no valid time |
| D12 Graph algorithms/ML | N/A | none |
| D13 Retrieval/agent integration | 2, 5 | tool-driven memory |
| D14 NL query | N/A | not a query system |
| D15 Governance/authoring | 8, 9, 12 | git review possible; no gate |
| D16 Human experience | 3 | CLI, desktop, web, ADE (V1) |
| D17 Developer experience | 3 | SDKs, tools, MCP; churn |
| D18 Trust/security | 5, 9 | shared token; host shell access; injection |
| D19 Multi-tenancy/white-label | 5, 9 | org id only |
| D20 Empirical economics | 7 | no independent data |
| D21 Commercial/licensing | 1, 10 | Cloud plans; OSS Apache-2.0 |
| D22 Interop/lock-in | 8 | markdown/git export is strong |
| D23 IP/prior art | 12 | sleep-time compute and MemGPT papers are published prior art; no patent search |
| D24 Research quality | 7 | vendor benchmarks, contested |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-57 agent memory | native (text tiers) | CLAIM-08, -09 | Partial | BUILD | P1 |
| CAP-36 history | native (git/BlockHistory) | CLAIM-06, -08 | BL-37 Implemented | REUSE EOIP | P2 |
| CAP-43 epistemic separation | absent | CLAIM-09 | BL-40 | BUILD | P1 |
| CAP-46 ACL in retrieval | absent | CLAIM-08 | BL-18 Absent | BUILD | P0 |
| CAP-47 tenant isolation | partial (org id) | CLAIM-08 | BL-20 Partial | BUILD | P0 |
| CAP-53 vector search | native (pgvector/Turbopuffer/Pinecone) | CLAIM-08, -11 | BL-14 Partial | DEFER | P3 |
| CAP-59 tool interface | native (tools, MCP) | wheel | BL-47 | REFERENCE | P3 |
| CAP-61 local models | native | CLAIM-04, -11 | BL-45 | INTEGRATE | P2 |
| CAP-50 air-gap | partial | CLAIM-04 | BL-01 | EXPERIMENT | P2 |
| CAP-48 audit integrity | partial (git) | CLAIM-06 | BL-41 | REUSE EOIP | P2 |

## Appendix C — Evidence records

| CLAIM-ID | Product/version/date | Exact claim | Class | Source + URL | Pub/access | Confidence + rationale | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-letta-01 | PyPI `letta` | `letta` 0.34.12 uploaded 2026-10-12 = Letta Code CLI ("stateful agents in your terminal", not a Python SDK); previous server line ended at 0.16.8 on 2026-05-14 (Apache License, Python >=3.11) | Officially documented | https://pypi.org/project/letta/ ; https://pypi.org/pypi/letta/json | 2026-10-12 / 2026-10-26 | 0.9 | none |
| CLAIM-letta-02 | `letta-ai/letta` main | README: active dev in `letta-code`; `archive` branch holds retired Letta V1 API server; 25.3k stars; Apache-2.0 | Officially documented | https://github.com/letta-ai/letta ; /tree/archive | n/a / 2026-10-26 | 0.85 | none |
| CLAIM-letta-03 | letta-code / npm | 3.7k stars, Apache-2.0; npm latest 0.34.24 (2026-10-25), license Apache-2.0; "All context (including memory blocks) is tracked via git"; `/connect` for provider keys | Officially documented | https://github.com/letta-ai/letta-code ; https://registry.npmjs.org/@letta-ai/letta-code | 2026-10-25 / 2026-10-26 | 0.85 | none |
| CLAIM-letta-04 | docs self-hosting | Two modes (local runtime; self-hosted App Server); `LETTA_APP_SERVER_TOKEN`; "App Server has shell and filesystem access on its host"; local providers Ollama, LM Studio, llama.cpp via `letta --backend local connect`; state `~/.letta/lc-local-backend`; not auto-backed-up; tenant isolation not described; remote provider prompts still go to provider | Officially documented | https://docs.letta.com/self-hosting | n/a / 2026-10-26 | 0.8 | CLAIM-05 |
| CLAIM-letta-05 | docs install / Letta Code self-hosting | Install page lists Docker under "Deprecated"; a Letta Code self-hosting page (search-surfaced, not fetched directly) describes Docker `letta/letta` on port 8283 | Third-party report (search summary of docs) | https://docs.letta.com/install ; https://docs.letta.com/letta-code/selfhosting | n/a / 2026-10-26 | 0.4 | CLAIM-04 |
| CLAIM-letta-06 | docs MemFS | Memory in per-agent git repo; edits committed; root files loaded into system prompt every turn (older agents `system/` dir); dirs with `MEMORY.md` lazily loaded; dreaming and memory doctor use git worktrees; local-only agents: user backs up; search-surfaced note that MemFS is unavailable on Docker server (legacy blocks) | Officially documented | https://docs.letta.com/letta-agent/concepts/memfs | n/a / 2026-10-26 | 0.8 | Docker caveat from search snippet only |
| CLAIM-letta-07 | docs memory config | Dreaming configured via `/sleeptime`; triggers: step count or context compaction; "uses more model tokens and does not ask you for approval"; Free 5 MiB / Pro 50 MiB per memory repo | Officially documented | https://docs.letta.com/configuration/memory/index.md | n/a / 2026-10-26 | 0.8 | none |
| CLAIM-letta-08 | letta 0.16.8 wheel | ORM `Block` (label, value, limit, read_only, hidden, version optimistic lock, BlockHistory, OrganizationMixin); `Passage` with `CommonVector` embedding, tags; `apply_access_predicate` discards `access`, filters on organization_id ("all permissions at the moment"); Identity unique per organization | Observed in source code | `letta/orm/block.py`, `passage.py`, `sqlalchemy_base.py:872-905`, `identity.py` in https://files.pythonhosted.org/packages/10/20/eedf6bd8b55e97edf9cbcaea8f575b83157737d6483ddba6b304babc0a4a/letta-0.16.8-py3-none-any.whl | 2026-05-14 / 2026-10-26 | 0.9 | archived line |
| CLAIM-letta-09 | letta 0.16.8 wheel | Memory tools: core_memory_append/replace; memory_replace/insert/rethink/apply_patch/delete/rename/create/str_replace/str_insert/update_description/finish_edits; archival_memory_insert/search; conversation_search | Observed in source code | `letta/services/tool_executor/core_tool_executor.py` | 2026-05-14 / 2026-10-26 | 0.9 | archived line |
| CLAIM-letta-10 | letta 0.16.8 wheel | `SleeptimeMultiAgentV4` (v1-v4 exist): group `ManagerType.sleeptime`, turns counter vs `sleeptime_agent_frequency` triggers background run; groups also supervisor, round-robin, dynamic | Observed in source code | `letta/groups/sleeptime_multi_agent_v4.py:139-145` | 2026-05-14 / 2026-10-26 | 0.85 | archived line |
| CLAIM-letta-11 | letta 0.16.8 wheel | Provider schemas incl. ollama, vllm, lmstudio, sglang, openai, anthropic, bedrock-like, together, etc.; Postgres via `letta_pg_uri` else SQLite; optional Turbopuffer, Pinecone, ClickHouse | Observed in source code | `letta/schemas/providers/`, `settings.py:275,472-493,435`, `helpers/tpuf_client.py` | 2026-05-14 / 2026-10-26 | 0.85 | archived line |
| CLAIM-letta-12 | arXiv:2310.08560 | MemGPT: "virtual context management" inspired by OS memory tiers, interrupts for control flow; evaluated on document analysis and multi-session chat | Officially documented (preprint) | https://arxiv.org/abs/2310.08560 | 2023-10-12 / 2026-10-26 | 0.8 | none |
| CLAIM-letta-13 | arXiv:2504.13171 | Sleep-time compute: ~5x less test-time compute at same accuracy, up to +13% (GSM-Symbolic) / +18% (AIME) accuracy, 2.5x lower per-query cost on multi-query; on Stateful GSM-Symbolic/AIME | Officially documented (preprint) | https://arxiv.org/abs/2504.13171 | 2025-04-17 / 2026-10-26 | 0.5 for memory relevance (math tasks) | none |
| CLAIM-letta-14 | Letta blog | Letta filesystem agent 74.0% on LoCoMo with gpt-4o-mini; Mem0 graph 68.5%; Mem0 did not explain MemGPT numbers | Unverified (vendor claim, competitor-disputed) | https://www.letta.com/blog/benchmarking-ai-agent-memory | 2025-08-12 / 2026-10-26 | 0.3 | CLAIM-mem0-15..17 |
| CLAIM-letta-15 | docs sleep-time (V1) | V1 sleep-time architecture page labelled experimental; enabling `enable_sleeptime` creates primary + sleep-time agents sharing blocks | Third-party report (search summary of docs page that returned 404 on direct fetch) | https://docs.letta.com/guides/agents/architectures/sleeptime/index.md | n/a / 2026-10-26 | 0.35 | none |

## Appendix D — Assumptions

1. "Letta" = the registry name Letta (MemGPT): both the archived V1 server and current Letta Code; reconstruction uses the V1 wheel because the current App Server source was not read (it ships in the npm package; not inspected).
2. Docs statements about Docker conflict; both are recorded, neither resolved.
3. Core-block char-limit constant and summariser internals were not read (grep returned nothing for the constant name).
4. Access dates are the session date 2026-10-26; nothing executed.
