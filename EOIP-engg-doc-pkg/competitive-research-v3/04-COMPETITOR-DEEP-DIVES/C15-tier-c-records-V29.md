# C15 - Tier C records (batch V29)

Verified 2026-10-26 (brief date 2026-10-18). Worker V29. Star counts and dates from the GitHub API on 2026-10-26 unless stated. EOIP baseline: BL-42 (code graph), BL-18, BL-47. Related deep dives: C15-codegraph.md, C15-graphify.md, C15-tree-sitter.md, C15-sourcegraph.md, C15-scip-lsif.md.

### T-C15-code-review-graph - code-review-graph

| Field | Value |
|---|---|
| Official URL | https://github.com/tirth8205/code-review-graph |
| Owner / version | tirth8205 (individual); v2.3.9, 2026-09-18; ~32.4k stars; pushed 2026-10-16 |
| Status / licence | active; MIT (permissive) |
| Deployment / air-gap | pip/uvx, one SQLite file; yes for core, optional cloud embeddings off by default (egress warning env) |
| Tier reason | named tool, token-efficient review graph |

**Candidate repos:** tirth8205/code-review-graph (32.4k) is the registry target; others are forks or unrelated (HaipingShi/...-plus 9 stars, demon24ru 8, harshsh-dev go port 3, mcaupybugs LangGraph agent 4). **Relevance:** Tree-sitter graph (functions, classes, calls, inheritance, tests) in SQLite, Leiden communities, blast-radius and risk-scored PR review, 30 MCP tools, custom languages via `languages.toml`; its README states blast-radius recall is an upper bound because ground truth is taken from the same graph (good evidence hygiene). Touches CAP-66, 67, 69, 59, 62. No ACLs. **Decision: REFERENCE-ONLY** - borrow test-impact and risk-score ideas for the digital thread (BL-42).

Evidence: [CLAIM-crg-01] repo metadata, https://api.github.com/repos/tirth8205/code-review-graph, 2026-10-26, Officially documented, 0.85. [CLAIM-crg-02] features, SQLite, Leiden, 30 tools, upper-bound caveat, https://github.com/tirth8205/code-review-graph (README), 0.8; benchmarks vendor-run, 0.4.

### T-C15-repomix - Repomix

| Field | Value |
|---|---|
| Official URL | https://repomix.com ; https://github.com/yamadashy/repomix |
| Owner / version | yamadashy; v1.18.1, 2026-09-21; ~29.0k stars |
| Status / licence | active; MIT |
| Deployment / air-gap | npx/npm/Docker; local packing yes; `--remote` fetches from Git hosts |
| Tier reason | repo packing for LLMs |

**Relevance:** packs a repository into one XML/Markdown/plain file with per-file token counts, Secretlint-based exclusion of credential-shaped files, and `--compress` using Tree-sitter to keep signatures. No graph, no index, no incremental model. Useful as an export format for human-approved context bundles and as a secret-filtering pattern (CAP-33). Touches CAP-33, 55, 60. **Decision: REFERENCE-ONLY** - reuse the idea of token-budgeted, secret-filtered bundles inside the egress gateway (BL-45); do not depend on it.

Evidence: [CLAIM-repomix-01] metadata, https://api.github.com/repos/yamadashy/repomix, 2026-10-26, 0.85. [CLAIM-repomix-02] Secretlint, compress, XML default, token counting, https://github.com/yamadashy/repomix README, 0.8.

### T-C15-grepai - grepai

| Field | Value |
|---|---|
| Official URL | https://github.com/yoanbernabeu/grepai ; https://yoanbernabeu.github.io/grepai/ |
| Owner / version | Yoan Bernabeu; v1.0.0, 2026-10-25; ~1.9k stars |
| Status / licence | active; MIT |
| Deployment / air-gap | single binary; default Ollama (`nomic-embed-text`), LM Studio, OpenAI optional; yes with local embedder |
| Tier reason | named tool |

**Candidate repos:** yoanbernabeu/grepai (1.9k) is the only credible one; the rest are skills, helpers or forks (grepai-skills 20, a hardened fork 1). **Relevance:** semantic code search CLI plus caller/callee tracing (`grepai trace callers`), file watcher, MCP server; storage backends gob/pgvector/Qdrant per third-party listing (UNVERIFIED in docs). It is a semantic-search layer, not a symbol graph, and has no ACLs. Touches CAP-53, 55, 66, 59. **Decision: REFERENCE-ONLY** - compare retrieval quality in the CAP-78 harness against BM25 + graph (Master Prompt 5.3).

Evidence: [CLAIM-grepai-01] metadata, https://api.github.com/repos/yoanbernabeu/grepai, 2026-10-26, 0.85. [CLAIM-grepai-02] features, Ollama default, https://github.com/yoanbernabeu/grepai README, 0.75; storage list from https://www.linuxlinks.com/grepai-cli-semantic-code-search/ 0.4.

### T-C15-gitnexus - GitNexus

| Field | Value |
|---|---|
| Official URL | https://github.com/abhigyanpatwari/GitNexus ; web UI gitnexus.vercel.app |
| Owner / version | Abhigyan Patwari; v1.6.12, 2026-09-12; ~48.0k stars; pushed 2026-10-26 |
| Status / licence | active; **PolyForm Noncommercial 1.0.0** (source-available, noncommercial) - LEGAL REVIEW TRIGGER; GitHub reports NOASSERTION |
| Deployment / air-gap | `npx gitnexus`, MCP stdio/HTTP, Docker; indexing LLM-free and local; remote embeddings/chat optional |
| Tier reason | named tool |

**Candidate repos:** abhigyanpatwari/GitNexus is canonical; pi-gitnexus (213, MIT integration), CodeWithJames-AI, m008v, nxpatterns and chengjon are mirrors/forks - ignore. **Relevance:** 19-phase ingestion DAG into an embedded graph database (LadybugDB; legacy KuzuDB files cleaned up, relationship to Kuzu UNVERIFIED), 18 language providers, Leiden communities, execution flows, embeddings (arctic-embed-xs 384D, opt-in), MCP tools `query/context/impact/trace/detect_changes/rename`. Strong design for impact and process detection. Noncommercial licence forbids white-label sale. Touches CAP-66, 67, 69, 55, 59. **Decision: REFERENCE-ONLY** - study phase DAG and impact tools; **REJECT as dependency or embedded component**.

Evidence: [CLAIM-gitnexus-01] metadata, https://api.github.com/repos/abhigyanpatwari/GitNexus, 2026-10-26, 0.85. [CLAIM-gitnexus-02] licence text, https://raw.githubusercontent.com/abhigyanpatwari/GitNexus/main/LICENSE, 0.9. [CLAIM-gitnexus-03] architecture, https://github.com/abhigyanpatwari/GitNexus/blob/main/ARCHITECTURE.md, 0.8.

### T-C15-srcml - srcML

| Field | Value |
|---|---|
| Official URL | https://www.srcml.org ; https://github.com/srcML/srcML |
| Owner / version | srcML project (academic origin, first release 2005); current version NOT VERIFIED (releases list empty on fetched page) |
| Status / licence | maintained (2026 briefing says Python, JS/TS, CMake added); **GPL-3.0** (strong copyleft) - LEGAL REVIEW TRIGGER |
| Deployment / air-gap | CLI + libsrcml C library; yes |
| Tier reason | code-as-XML |

**Relevance:** wraps source in an XML markup preserving all text, so XPath/XQuery and srcQL can query syntax and srcDiff can diff structurally; C, C++, C#, Java (page), more per briefing. Useful as an idea for lossless, round-trippable code representation (compare OpenRewrite LST). GPL forbids linking into the product; subprocess use needs legal review. Touches CAP-66, 73. **Decision: REFERENCE-ONLY** (GPL hard constraint).

Evidence: [CLAIM-srcml-01] repo page, https://github.com/srcML/srcML, 2026-10-26, licence GPL-3.0, 0.7. [CLAIM-srcml-02] ICSME 2026 briefing: new languages, srcQL, https://conf.researchr.org/track/icsme-2026/icsme-2026-technical-briefings, 0.5 (search summary).

### T-C15-scitools-understand - SciTools Understand

| Field | Value |
|---|---|
| Official URL | https://scitools.com ; https://docs.scitools.com/buildnotes/ |
| Owner / version | SciTools; 8.0 build 1258, 2026-07-27 (8.0 released ~May 2026); 7.2 Oct 2025 |
| Status / licence | active; proprietary commercial (price/terms NOT PUBLICLY VERIFIED) |
| Deployment / air-gap | desktop + CLI/Python API; yes |
| Tier reason | code analysis |

**Relevance:** static-analysis IDE with dependency graphs, metrics, CodeCheck, Python API; 8.0 adds Rust, VHDL 2008 and AI with remote or third-party models (egress to check); 7.2 safety manual cites ISO 26262/IEC 61508/EN 50128 certification. Customers in regulated embedded fields may already hold licences; a possible export source, not a dependency. Touches CAP-66, 69. **Decision: REFERENCE-ONLY**.

Evidence: [CLAIM-understand-01] build notes and release page, https://docs.scitools.com/buildnotes/index.html and https://docs.scitools.com/help/release-notes/version-releases.html, 2026-10-26, Officially documented via search summary, 0.6. [CLAIM-understand-02] safety manual, https://support.scitools.com/support/solutions/articles/70000685119-understand-safety-manual-build-7-2-1248, 0.5.

### T-C15-sonarqube - SonarQube

| Field | Value |
|---|---|
| Official URL | https://www.sonarsource.com/products/sonarqube/ ; https://docs.sonarsource.com/sonarqube-server/ |
| Owner / version | Sonar (SonarSource); Server docs 2026.x (installation docs cover 2026.5; latest NOT confirmed); Community Build monthly |
| Status / licence | active; mixed: Community Build code LGPL-3.0 but bundled analyzers under Sonar Source-Available License v1.0 since 2024-11-29; Developer/Enterprise/Data Center commercial, per instance per year by lines of code - LEGAL REVIEW TRIGGER |
| Deployment / air-gap | self-hosted Docker/Kubernetes; yes |
| Tier reason | code quality |

**Relevance:** quality gates, issues, coverage and security hotspots per project/branch. As a source system, its Web API findings and quality-gate states can feed the digital thread (Jira story -> PR -> build -> quality gate). Not a code graph. Touches CAP-26, 68, 69, 79. **Decision: INTEGRATE on demand** as a connector source (EXPERIMENT); do not bundle.

Evidence: [CLAIM-sonar-01] editions and licence split, https://www.sonarsource.com/license/ and https://docs.sonarsource.com/sonarqube-server/2026.4/discovering/sonarqube-server-editions, 2026-10-26, via search summary, 0.6. [CLAIM-sonar-02] version, https://docs.sonarsource.com/sonarqube-server/server-installation/, 0.5.

### T-C15-repo-maps - Aider repo map; Cursor and Continue codebase indexes

| Field | Value |
|---|---|
| Official URL | https://aider.chat/docs/repomap.html ; https://cursor.com/docs/context/codebase-indexing ; https://docs.continue.dev/reference/deprecated-codebase |
| Owner / version | Aider (open source; licence UNVERIFIED this run); Cursor (Anysphere, proprietary); Continue (open source, licence UNVERIFIED this run) |
| Status | Aider active (not re-checked); Cursor page now describes local "Instant Grep"; Continue `@Codebase` page marked Deprecated |
| Deployment / air-gap | Aider local with local models: yes; Cursor: client with vendor cloud, no; Continue: local LanceDB index, yes |
| Tier reason | context-packing patterns |

**Relevance:** Aider sends a ranked map of files and key symbols, ranked by a graph algorithm over a file-dependency graph, within a default 1k-token budget (`--map-tokens`). Cursor's current page says its search index is built on the machine and "does not store embeddings of your codebase for search" - older Merkle/embedding descriptions are UNVERIFIED here. Continue combines embedding retrieval with keyword search, indexes under `~/.continue/index` (LanceDB per vendor blog); docs disagree on the default embedding model. Patterns: budgeted graph-ranked context, hybrid retrieval. Touches CAP-53, 54, 55, 60. **Decision: REFERENCE-ONLY** - BUILD budgeted, ACL-filtered, graph-ranked context packing in retrieval (BL-14/15, BL-18).

Evidence: [CLAIM-repomaps-01] Aider repo map, https://aider.chat/docs/repomap.html, 2026-10-26, Officially documented, 0.8 (tree-sitter/PageRank not on page). [CLAIM-repomaps-02] Cursor, https://cursor.com/docs/context/codebase-indexing, 0.7. [CLAIM-repomaps-03] Continue, https://docs.continue.dev/features/codebase-embeddings ; https://lancedb.com/blog/ai-native-development-local-continue-lancedb, 0.6; contradictory: deprecated page names transformers.js default.
