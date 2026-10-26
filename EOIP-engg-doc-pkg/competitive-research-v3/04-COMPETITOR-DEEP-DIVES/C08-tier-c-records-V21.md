# C08 Tier C records — batch V21

Verified on 2026-10-18 (access date for all claims). Worker: V21. Method: GitHub repo pages and vendor pages via web fetch (GitHub API was rate-limited; **last-commit dates and release dates were not retrievable for any repo and are UNVERIFIED**). Star counts are the page-header values at access date. Per Master Prompt §5.3, no performance claims are repeated except where flagged as vendor claims.

---

### T-C08-nano-graphrag — nano-graphrag

| Field | Value |
|---|---|
| Official URL | https://github.com/gusye1234/nano-graphrag |
| Owner | gusye1234 (individual) |
| Latest version / date | No GitHub releases listed; version UNVERIFIED |
| Status | Appears active-or-dormant, UNVERIFIED (155 commits, ~4.0k stars) |
| Licence / class | MIT / permissive |
| Deployment | Embedded Python library |
| Air-gap viable | Yes if local LLM/embedding supplied (UNVERIFIED by test) |
| Tier reason | Minimal, hackable GraphRAG reference |

Relevance: a compact reimplementation of Microsoft-style GraphRAG (entity extraction, communities, local/global query), repository tagline "A simple, easy-to-hack GraphRAG implementation". Useful as a readable reference and as an embedded engine (Kotaemon wraps it). Not a governed graph: no tenancy, ACLs, provenance beyond chunks. Touches CAP-56, CAP-32, CAP-28.

**Decision:** REFERENCE-ONLY — study for minimal community-summary pipeline; do not depend on it.

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-nano-graphrag-01 | MIT, ~4.0k stars, "simple, easy-to-hack GraphRAG implementation", no releases listed | repo metadata | github.com/gusye1234/nano-graphrag, accessed 2026-10-18 | 0.8 |

---

### T-C08-infranodus — InfraNodus

| Field | Value |
|---|---|
| Official URL | https://infranodus.com ; MCP repo https://github.com/infranodus/mcp-server-infranodus |
| Owner | InfraNodus (Nodus Labs) — owner name per vendor; UNVERIFIED legal entity |
| Latest version / date | UNVERIFIED (no releases listed on MCP repo) |
| Status | Active commercial SaaS; MCP repo 104 stars, 88 commits |
| Licence / class | MCP server MIT (package manifest + repo); vendor says underlying open-source tools are AGPL — mixed |
| Deployment | SaaS; MCP server self-hostable but calls InfraNodus API (key; ~70 free requests then quota per README) |
| Air-gap viable | No (cloud API dependency) |
| Tier reason | Text network analysis SaaS |

Relevance: product (not a library) doing text-network / gap analysis over text, exposed to agents via MCP. Relevant as an interaction idea (structural gaps, topical clusters) not as infrastructure. AGPL statement for components is a legal-review trigger if anything beyond the MCP client is considered. Touches CAP-59, CAP-71, CAP-62.

**Decision:** REFERENCE-ONLY — UX idea of structural-gap discovery; EXPERIMENT later on an in-house equivalent.

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-infranodus-01 | MCP server repo is MIT, owner infranodus, requires API key beyond a free quota | repo | github.com/infranodus/mcp-server-infranodus | 0.7 |
| CLAIM-infranodus-02 | Vendor states underlying open-source tools are AGPL | vendor statement | infranodus.com/mcp/deployment (via search snippet) | 0.5 |

---

### T-C08-contextclue — ContextClue Graph Builder

| Field | Value |
|---|---|
| Official URL | https://github.com/addepto/graph_builder ; https://context-clue.com/contextclue-graph-builder-open-source/ |
| Owner | Addepto (company; ContextClue is its product line) |
| Latest version / date | No releases/tags listed; UNVERIFIED |
| Status | Early open-source toolkit; 113 stars, 26 commits |
| Licence / class | MIT / permissive (open-source toolkit); the commercial ContextClue platform is proprietary (UNVERIFIED terms) |
| Deployment | Python package (Poetry, Python 3.12+), Docker Compose FastAPI service |
| Air-gap viable | Partial / UNVERIFIED (LLM provider not stated; graphs persist only while the API runs) |
| Tier reason | Vendor scope to verify |

Relevance: resolution — the registry means the Addepto open-source toolkit, not Neo4j's "LLM Knowledge Graph Builder" (name-alike). It extracts graphs from PDFs/tables; roadmap (per vendor) lists persistence and graph-DB integration, so today it is in-memory. A small ingest-side reference only. Touches CAP-32, CAP-28.

**Decision:** REFERENCE-ONLY.

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-contextclue-01 | MIT; toolkit for KG extraction from documents/tables; FastAPI+Docker; graphs not persisted across service restarts | repo/vendor | github.com/addepto/graph_builder | 0.7 |

---

### T-C08-harmony-mcp — Harmony MCP

| Field | Value |
|---|---|
| Official URL | https://codeconductor.ai/harmony/ (vendor page; no GitHub repo found) |
| Owner | CodeConductor (founder Paul Dhaliwal per its blog) |
| Latest version / date | NOT PUBLICLY VERIFIED |
| Status | Vendor-marketed product; maturity unknown |
| Licence / class | NOT PUBLICLY VERIFIED (not stated as open source) / proprietary assumed |
| Deployment | MCP server for coding agents (Claude Code, Cursor, Windsurf, Gemini per vendor) |
| Air-gap viable | Unknown |
| Tier reason | Existence/owner to verify |

Relevance: candidates found — (1) CodeConductor "Harmony MCP" repository-memory server (the registry's likely meaning); (2) Amdocs-Studio/harmony2-gemini-mcp (Gemini guide for Harmony 2.0 dev); (3) JorgeHI/mcp-harmony-context (Toon Boom Harmony docs, MIT); (4) mcp-harmonyos (HarmonyOS). No star/last-commit data obtainable. Claims are vendor-only (token budgeting, symbol/call-graph indexing). Touches CAP-66, CAP-57, CAP-59. Recommend DEFER pending a verifiable repo; no independent evidence.

**Decision:** REFERENCE-ONLY (registry action DEFER).

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-harmony-mcp-01 | CodeConductor describes Harmony as a token-budgeted repository-memory MCP; licence not stated | vendor claim | codeconductor.ai/blog/codebase-memory-alternative/ | 0.4 |

---

### T-C08-mempalace — MemPalace

| Field | Value |
|---|---|
| Official URL | https://github.com/MemPalace/mempalace |
| Owner | MemPalace org; press attributes concept to actress Milla Jovovich and engineering to Ben Sigman (Decrypt) |
| Latest version / date | README badge 3.12.0; date UNVERIFIED |
| Status | Active, very popular (~59.7k stars, 2,498 commits) |
| Licence / class | MIT / permissive |
| Deployment | Local Python; ChromaDB default, also sqlite_exact, rust_exact, Milvus, Qdrant, pgvector |
| Air-gap viable | Yes (local-first, no API calls per README) |
| Tier reason | Agent-memory project, existence/owner to verify |

Relevance: personal-origin open-source verbatim memory for coding agents ("wings/rooms" hierarchy). Verbatim retrieval plus pluggable backend mirrors EOIP's backend neutrality. Benchmark claims are contested: README itself reports 96.6% raw R@5 and 98.4% held-out on LongMemEval and disclaims a "100%" figure as tuned on missed questions; third-party analysis reports palace features did not help in a reproduction. Treat all as unproven (§5.3). Touches CAP-57, CAP-53, CAP-59.

**Decision:** REFERENCE-ONLY; EXPERIMENT with its verbatim-first design as a baseline in memory evals (CAP-78).

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-mempalace-01 | MIT, ~59.7k stars, v3.12.0 badge, pluggable vector backends | repo | github.com/MemPalace/mempalace | 0.8 |
| CLAIM-mempalace-02 | Benchmark claims disputed; README concedes tuning on missed questions for 100% | vendor + third party | same; vectorize.io/articles/what-is-mempalace | 0.5 |

---

### T-C08-mythos — MythOS

| Field | Value |
|---|---|
| Official URL | https://mythos.one |
| Owner | Brian Swichkow (builder per site); footer credits "One Inc" — legal owner UNVERIFIED |
| Latest version / date | NOT PUBLICLY VERIFIED (tiered loading change April 2026) |
| Status | Hosted product, early; maturity unknown |
| Licence / class | Platform proprietary; npm `mythos-mcp` licence not stated |
| Deployment | SaaS (web, mobile, MCP, Claude Code skill); self-hosting not mentioned |
| Air-gap viable | No |
| Tier reason | Existence/owner to verify; not Claude Mythos |

Relevance: resolution — MythOS (mythos.one) is an AI-native personal knowledge platform with @mention-linked memos, 3-hop traversal tool and identity/memory layers. It is unrelated to Anthropic's Claude Mythos model family; do not conflate. It is a hosted personal product, so low relevance beyond UX ideas (tiered context loading, visibility tiers). Touches CAP-57, CAP-59.

**Decision:** REFERENCE-ONLY.

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-mythos-01 | mythos.one is a hosted knowledge-graph memo platform built by Brian Swichkow with an MCP package; no pricing/licence/self-host info | vendor | mythos.one/me/mythos/ce6e4c | 0.5 |

---

### T-C08-claude-mem — claude-mem

| Field | Value |
|---|---|
| Official URL | https://github.com/thedotmack/claude-mem |
| Owner | thedotmack (Alex Newman), individual |
| Latest version / date | 15.2.1 (README badge); date UNVERIFIED |
| Status | Very active, reported ~103k stars, 3,678 commits |
| Licence / class | Apache-2.0 / permissive (README links an "open/commercial boundary" doc, contents unread — check before reuse) |
| Deployment | Local plugin/hooks for coding agents; SQLite (FTS5) + Chroma |
| Air-gap viable | Partial — compression step uses an AI model; local feasibility UNVERIFIED |
| Tier reason | Personal/community project to verify |

Relevance: community project (not Anthropic's), captures agent actions, compresses via an LLM, injects context next session. Pattern of hook-based capture + progressive disclosure is a reference for CAP-57 agent memory; no tenancy or ACLs. Touches CAP-57, CAP-54, CAP-53.

**Decision:** REFERENCE-ONLY; ingest/consolidation pattern for EXPERIMENT.

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-claude-mem-01 | Apache-2.0, v15.2.1 badge, SQLite+Chroma, owner thedotmack, ~103k stars | repo | github.com/thedotmack/claude-mem | 0.7 |

---

### T-C08-g-retriever — G-Retriever

| Field | Value |
|---|---|
| Official URL | https://github.com/XiaoxinHe/G-Retriever |
| Owner | Xiaoxin He et al. (academic) |
| Latest version / date | No releases; paper arXiv 2402.07630 |
| Status | Research code (558 stars, 37 commits) |
| Licence / class | MIT / permissive |
| Deployment | Research scripts (PyTorch/GNN + LLM) |
| Air-gap viable | Yes after model download |
| Tier reason | Research |

Relevance: "G-Retriever: Retrieval-Augmented Generation for Textual Graph Understanding and Question Answering", NeurIPS 2024 (arXiv 2402.07630). Combines retrieval of a subgraph via Prize-Collecting Steiner Tree with a GNN soft prompt for the LLM. Independent replication: NOT PUBLICLY VERIFIED by this batch; reported gains are the authors' own. Touches CAP-56, CAP-64, CAP-19.

**Decision:** EXPERIMENT — PCST subgraph selection as a retrieval-budget technique.

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-g-retriever-01 | NeurIPS 2024 paper, code MIT, 558 stars | paper/repo | github.com/XiaoxinHe/G-Retriever | 0.8 |

---

### T-C08-pathrag — PathRAG

| Field | Value |
|---|---|
| Official URL | https://github.com/BUPT-GAMMA/PathRAG |
| Owner | BUPT-GAMMA (Beijing University of Posts and Telecommunications) |
| Latest version / date | No releases; paper arXiv 2502.14902 (v1 18 Feb 2025, v2 later) |
| Status | Research code (378 stars, 27 commits) |
| Licence / class | MIT / permissive |
| Deployment | Python research library |
| Air-gap viable | Yes with local LLM (UNVERIFIED) |
| Tier reason | Research |

Relevance: "PathRAG: Pruning Graph-based Retrieval Augmented Generation with Relational Paths" (Chen, Guo et al.); flow-based pruning to pick key relational paths, ordered by reliability in the prompt. Venue: arXiv preprint only found (no peer-reviewed venue verified). Evaluation is LLM-judged by the authors; independent replication NOT PUBLICLY VERIFIED. Touches CAP-56, CAP-19, CAP-60.

**Decision:** EXPERIMENT — path pruning as redundancy control for graph context.

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-pathrag-01 | arXiv 2502.14902; MIT; 378 stars | paper/repo | arxiv.org/abs/2502.14902; github.com/BUPT-GAMMA/PathRAG | 0.8 |

---

### T-C08-minirag — MiniRAG

| Field | Value |
|---|---|
| Official URL | https://github.com/HKUDS/MiniRAG |
| Owner | HKUDS (University of Hong Kong Data Intelligence Lab) |
| Latest version / date | PyPI `minirag-hku` announced 2025-02-27; current version UNVERIFIED |
| Status | Research with package (~2.0k stars, 106 commits) |
| Licence / class | MIT / permissive |
| Deployment | Python library; aimed at small language models |
| Air-gap viable | Yes (small local models is the premise) |
| Tier reason | Research |

Relevance: "MiniRAG: Towards Extremely Simple Retrieval-Augmented Generation", arXiv 2501.06713; repo labels it ACL 2026 (venue as stated by repo, not independently confirmed). Heterogeneous graph of chunks and entities with topology-enhanced retrieval for small models. Independent replication NOT PUBLICLY VERIFIED. Fits EOIP default-local LLM constraint. Touches CAP-56, CAP-61, CAP-55.

**Decision:** EXPERIMENT — small-model retrieval path for CPU-only nodes.

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-minirag-01 | arXiv 2501.06713, repo MIT, ~2.0k stars, venue label ACL 2026 per repo | repo | github.com/HKUDS/MiniRAG | 0.6 |

---

### T-C08-structrag — StructRAG

| Field | Value |
|---|---|
| Official URL | https://github.com/Li-Z-Q/StructRAG |
| Owner | Li-Z-Q et al. (academic; Chinese Academy of Sciences affiliation UNVERIFIED) |
| Latest version / date | No releases; paper on OpenReview GhexuBLxbO |
| Status | Research code (171 stars, 10 commits) |
| Licence / class | **No LICENSE file seen — all rights reserved by default** / unlicensed (legal-review trigger) |
| Deployment | Research scripts |
| Air-gap viable | Unknown |
| Tier reason | Research |

Relevance: "StructRAG: Boosting Knowledge Intensive Reasoning of LLMs via Inference-time Hybrid Information Structurization", ICLR 2025 (per repo README). A router chooses a structure (table, graph, algorithm, catalogue, chunk) for the task before reasoning. Idea is relevant to CAP-56/CAP-58; code cannot be reused without a licence. Independent replication NOT PUBLICLY VERIFIED.

**Decision:** REFERENCE-ONLY — idea only; do not copy code.

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-structrag-01 | ICLR 2025 per README; no LICENSE file in listing; 171 stars | repo | github.com/Li-Z-Q/StructRAG | 0.6 |

---

### T-C08-r2r — R2R

| Field | Value |
|---|---|
| Official URL | https://github.com/SciPhi-AI/R2R |
| Owner | SciPhi-AI (company) |
| Latest version / date | No releases listed; UNVERIFIED |
| Status | Active-looking (~8.0k stars, 2,096 commits); no deprecation notice seen |
| Licence / class | MIT / permissive |
| Deployment | Docker, self-hosted REST API; managed cloud existence UNVERIFIED |
| Air-gap viable | Partial (local LLM support UNVERIFIED) |
| Tier reason | RAG system |

Relevance: "Agentic RAG with a RESTful API" — ingestion, hybrid search, knowledge-graph extraction, user/collection scoping. Closest to a full RAG service in this batch; comparison point for EOIP's API surface and permissions in retrieval. Touches CAP-55, CAP-56, CAP-46, CAP-32.

**Decision:** REFERENCE-ONLY; benchmark in CAP-78 harness (INTEGRATE not justified: EOIP owns tenancy/ACL).

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-r2r-01 | MIT, ~8.0k stars, tagline "production-ready ... Agentic RAG with a RESTful API" (vendor claim) | repo | github.com/SciPhi-AI/R2R | 0.7 |

---

### T-C08-kotaemon — Kotaemon

| Field | Value |
|---|---|
| Official URL | https://github.com/Cinnamon/kotaemon |
| Owner | Cinnamon (company) |
| Latest version / date | No releases listed; UNVERIFIED |
| Status | Active-looking (~25.8k stars) |
| Licence / class | Apache-2.0 / permissive |
| Deployment | Docker (lite/full image bundling Ollama), local via uv/conda, port 7860 |
| Air-gap viable | Yes with Ollama/llama.cpp |
| Tier reason | RAG UI |

Relevance: open-source document-chat UI with optional NanoGraphRAG, LightRAG and Microsoft GraphRAG (≤0.3.6) pipelines. Useful as a UX reference for cited document QA and as evidence of nano-graphrag adoption. Touches CAP-60, CAP-56, CAP-61, CAP-71.

**Decision:** REFERENCE-ONLY.

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-kotaemon-01 | Apache-2.0, ~25.8k stars, optional Nano/Light/MS GraphRAG, Ollama images | repo | github.com/Cinnamon/kotaemon | 0.8 |

---

### T-C08-txtai — txtai

| Field | Value |
|---|---|
| Official URL | https://github.com/neuml/txtai |
| Owner | NeuML (company) |
| Latest version / date | 9.0 referenced in blog; exact release/date UNVERIFIED |
| Status | Active (~13.0k stars) |
| Licence / class | Apache-2.0 / permissive |
| Deployment | Embedded Python, API server, Docker |
| Air-gap viable | Yes (local-first) |
| Tier reason | Embeddings DB / RAG |

Relevance: embeddings database combining sparse+dense indexes, a graph network and relational (SQL) storage, with semantic-graph and GraphRAG examples. Candidate embedded single-node search/vector component (REUSE-class) for CAP-04/53/54/55; graph is auxiliary, not a governed KG.

**Decision:** EXPERIMENT — as optional embedded hybrid-search backend behind EOIP's retrieval interface.

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-txtai-01 | Apache-2.0, ~13.0k stars, embeddings DB with vector+graph+SQL | repo | github.com/neuml/txtai | 0.8 |

---

### T-C08-langmem — LangMem

| Field | Value |
|---|---|
| Official URL | https://github.com/langchain-ai/langmem |
| Owner | LangChain (langchain-ai) |
| Latest version / date | No releases listed; UNVERIFIED |
| Status | Maintenance level UNVERIFIED (154 commits, 56 open issues; ~1.7k stars) |
| Licence / class | MIT / permissive |
| Deployment | Python library on LangGraph BaseStore |
| Air-gap viable | Yes if store and LLM local |
| Tier reason | Memory library |

Relevance: primitives for semantic/episodic/procedural memory extraction, memory tools and background consolidation. Couples to LangGraph store; useful design reference for CAP-57 (write, expire, invalidate), not a dependency.

**Decision:** REFERENCE-ONLY.

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-langmem-01 | MIT, ~1.7k stars, integrates with LangGraph long-term store | repo | github.com/langchain-ai/langmem | 0.7 |

---

### T-C08-a-mem — A-MEM

| Field | Value |
|---|---|
| Official URL | https://github.com/WujiangXu/A-mem (paper reproduction); implementation: A-mem-sys (name per README, not opened) |
| Owner | Wujiang Xu et al. (Rutgers-affiliated, UNVERIFIED) |
| Latest version / date | No releases; paper arXiv 2502.12110 |
| Status | Research (~1.0k stars, 33 commits) |
| Licence / class | MIT / permissive |
| Deployment | Python research code |
| Air-gap viable | Yes with local models (UNVERIFIED) |
| Tier reason | Agentic memory research |

Relevance: "A-Mem: Agentic Memory for LLM Agents", NeurIPS 2025 (per repo). Zettelkasten-style notes that are linked and evolve on write; repo is for reproducing paper results, with separate system repo for building agents. Independent replication NOT PUBLICLY VERIFIED. Touches CAP-57, CAP-39.

**Decision:** EXPERIMENT — note linking/evolution as consolidation strategy; guard against uncontrolled memory mutation (provenance, CAP-38).

| CLAIM | Claim | Class | Source | Conf. |
|---|---|---|---|---|
| CLAIM-a-mem-01 | arXiv 2502.12110, NeurIPS 2025 per repo, MIT | paper/repo | github.com/WujiangXu/A-mem | 0.7 |
