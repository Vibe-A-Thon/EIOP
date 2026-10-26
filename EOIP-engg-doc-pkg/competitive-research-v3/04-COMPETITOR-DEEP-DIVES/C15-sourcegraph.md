# C15 — Sourcegraph (Code Search, Deep Search, Cody Enterprise, Amp lineage)

| Field | Value |
|---|---|
| Registry ID | T-C15-sourcegraph |
| Tier | A — code-intelligence leader; the only vendor shipping precise cross-repo code navigation, trigram search, permission-aware access and agentic code Q&A as one self-hostable product |
| Versions examined | No single product version is published on the pages read. Docs for the current line (2026), `sourcegraph/sourcegraph-public-snapshot` (archived 2024-09-30), `sourcegraph/zoekt` (Apache-2.0, active), `sourcegraph/scip*` indexers. Release numbers of the closed core: **UNVERIFIED** |
| Verified on | 2026-10-18 (brief date; the fetches ran 2026-10-26) |
| Worker | V09 (W27 scope) |

## 1. Identity, current status, tier, and sources

| Item | Finding | Claim |
|---|---|---|
| Owner | Sourcegraph Inc. (commercial vendor) | [CLAIM-sourcegraph-04] |
| Product line today | Code Search, Deep Search (agentic search), Batch Changes ("Agentic Batch Changes"), Code Insights, MCP server, Cody Enterprise (Cody not mentioned on the pricing page). One published plan: Enterprise, from $16K/yr (vendor page) | [CLAIM-sourcegraph-05] |
| Cody | Cody Free, Cody Pro and Cody in Enterprise Starter: sign-ups closed 2025-06-25, discontinued 2025-07-23. "Cody Enterprise remains fully supported" per the vendor. Enterprise Starter kept Code Search | [CLAIM-sourcegraph-01] |
| Amp | Vendor pointed Cody Free/Pro users to Amp (ampcode.com, agentic coding tool). A December 2025 spin-off into a separate company is reported only by third-party review sites; no official announcement found | [CLAIM-sourcegraph-02] |
| Licence | Fair Source 2016 -> Apache-2.0 2018 -> relicensed to the non-OSS "Sourcegraph Enterprise" licence 2023-06-13 (press/Wikipedia) -> core moved to a private monorepo Aug 2024. The public snapshot repo (archived 2024-09-30) "contains primarily non-OSS-licensed files" (`LICENSE`, `LICENSE.enterprise`) and points to the last Apache-licensed commit | [CLAIM-sourcegraph-03], [CLAIM-sourcegraph-04] |
| Still open | `sourcegraph/zoekt` (Apache-2.0, "maintained source since 2017"), SCIP protocol and indexers (Apache-2.0 for `scip`, `scip-typescript`, `scip-java`; see C15-scip-lsif) | [CLAIM-sourcegraph-12] |
| Trap resolved | "Sourcegraph core closed-sourced in 2024?" Confirmed: Aug 2024 private-repo move (press-reported date 21 or 22 Aug; snapshot archive 2024-09-30 is vendor-repo evidence). The handbook still says "core is Apache 2.0": stale, contradicted by the snapshot README | [CLAIM-sourcegraph-04] |
| Tier reason | Defines the capability target for CAP-66..69; closed core means it is a pattern source and optional external integration, not a component | |

Sources: see Appendix C. Confidence on the commercial line 0.75; on the Amp spin-off 0.4.

## 2. Primary problem, target workloads, concrete example workflows

Problem: engineers and agents cannot find, understand or safely change code spread over thousands of repositories and several code hosts. Target: large enterprises (tens of thousands of repos), platform and security teams, and AI agents needing grounded code context.

| Workflow | How Sourcegraph does it | EOIP journey |
|---|---|---|
| Find every caller of a deprecated API across all repos | Regex/literal search (Zoekt trigram index of default branches; non-indexed search via `searcher` for other branches) then precise "find references" from uploaded SCIP indexes | J1 impact |
| Go-to-definition across repo boundaries | Precise navigation if a SCIP index exists, else search-based heuristics | J9 |
| Roll out a fix across 400 repos | Batch Changes: server-side specs run on executors, opens PRs | J10 |
| Ask "how does auth work here?" | Deep Search: agent runs searches, reads files, returns a Markdown answer with the searches and files as sources | J1/J9 |
| Hide repos a user may not see | Permission sync from code host, repo-level | P0 permission requirement |

## 3. Feature inventory

| Feature | Status | UI | API | CLI/SDK | Notes / claim |
|---|---|---|---|---|---|
| Indexed regex/literal code search | present | yes | GraphQL, stream API | `src` CLI (name from vendor docs; not re-verified) | trigram index [CLAIM-sourcegraph-11] |
| Search-based code navigation | present | yes | yes | | fallback when no precise index [CLAIM-sourcegraph-10] |
| Precise code navigation (SCIP) | enterprise-only, opt-in | yes + code host/review extensions | yes | `scip` CLI | [CLAIM-sourcegraph-10] |
| Auto-indexing via executors | enterprise (part of precise nav) | admin UI | | | [CLAIM-sourcegraph-10] |
| Cross-repo navigation | present when indexes exist | yes | | | via package/moniker-like symbols (see C15-scip-lsif) |
| Permissions sync | present, repo-level; file-level only mentioned for Perforce | admin | explicit permissions API | | [CLAIM-sourcegraph-09] |
| Deep Search | enterprise / enterprise starter | web only | | | Sourcegraph Model Provider only; BYOK unsupported; SSE up to 5 min [CLAIM-sourcegraph-06] |
| Cody (chat/autocomplete) | enterprise-only; sold with Enterprise | IDE + web | | | needs Cody Gateway or third-party LLM; local-model route unconfirmed [CLAIM-sourcegraph-13] |
| Batch Changes | enterprise | yes | | `src batch` | not examined in depth |
| Code Insights | enterprise | yes | | | separate `codeinsights-db` [CLAIM-sourcegraph-11] |
| MCP server | present (pricing page lists) | | MCP | | tool list NOT PUBLICLY VERIFIED here |
| Graph query / knowledge-graph API | absent (code graph is internal, not user-queryable as a graph) | | | | reasoned inference, 0.6 |
| Dependency/SBOM risk | partial/unknown | | | | not verified; treat as absent |

## 4. Architecture diagram

```
 Code hosts (GitHub/GitLab/Bitbucket/Perforce/...)         CI pipelines
        |  clone/fetch, webhooks, permission sync                |  scip-<lang> index  ->  `src code-intel upload`
        v                                                        v
  [worker]  repo sync, perms syncer, code monitors      [frontend (GraphQL/HTTP)] <--- browser, IDE, MCP, Amp/agents
        |                                                   |        |         |
        v                                                   |        |         +--> LLM (Sourcegraph Model Provider /
  [gitserver] sharded repo storage (code host = truth)      |        |              Cody Gateway / customer provider)
        |                                                   |        |
   +----+-----------+----------------+                      |        +--> [precise code-intel worker] --> codeintel DB
   v                v                v                      v                (SCIP uploads, symbol tables; internals
 [zoekt] trigram   [searcher]    [symbols]            [Postgres: repo table,                 NOT PUBLICLY VERIFIED)
 default-branch    unindexed     (ctags-like)          perms, "frontend" DB]
 index             search                              [codeinsights-db]   [executors: auto-index, batch changes]
 CONTROL PLANE: frontend + worker + Postgres.  DATA PLANE: gitserver, zoekt, searcher, code-intel store.
```

Services in the diagram that the architecture page did not describe (symbols, precise-code-intel worker, codeintel DB, blobstore) are from general vendor knowledge and are marked unverified [CLAIM-sourcegraph-11].

## 5. Under-the-hood reconstruction

Evidence is thin because the core is closed; anything not in Zoekt or SCIP source is a hypothesis.

**5.1 Data model (reconstructed).** Three separate stores, no unified graph.
1. Git objects in gitserver (shards of bare clones). Code host is source of truth [CLAIM-sourcegraph-11].
2. Search index: Zoekt trigram shards of the default branch (shard per repo) [CLAIM-sourcegraph-11][CLAIM-sourcegraph-12].
3. Precise index: per (repo, commit, indexer) SCIP uploads, each a protobuf `Index` of documents/occurrences/symbols (schema reconstructed in C15-scip-lsif section 5). Server side tables are hypothesis: upload row(repo, commit, root, indexer) + per-document blobs + symbol-name -> occurrence lookup tables in Postgres ("codeintel" DB) *(hypothesis; NOT PUBLICLY VERIFIED)*.

**5.2 Search path (Zoekt, source-available, Apache-2.0).** Trigram inverted index: for each 3-byte rune sequence, a posting list of file offsets. Query "foo.*bar" -> extract required literal substrings -> intersect posting lists -> verify candidate documents with the regexp engine -> rank with signals including symbol matches [CLAIM-sourcegraph-12]. Non-default branches or unindexed repos go to `searcher`, which scans the git tree [CLAIM-sourcegraph-11]. Exact posting-list encoding: verify in Zoekt `index/` package at a pinned tag (not read here).

**5.3 Precise navigation path (hypothesis consistent with docs).**
```
hover/definition(repo, commit, path, line, col):
  nearest commit with an uploaded index for (repo, path)   # "closest index" lookup via git ancestry
  doc = index.document(path); occ = occurrence containing (line,col)
  if occ.symbol is local -> resolve within doc
  elif occ has Definition role in same index -> return that range
  else -> symbol string lookup across indexes (package manager+name+version resolves the owning repo/index)
  adjust ranges from index commit to requested commit via git diff hunks   # needs verification
  fallback if no index: search-based navigation (ctags symbols + text search) [CLAIM-sourcegraph-10]
```
Diff-adjustment and closest-commit logic are widely described by Sourcegraph but not read in primary source here: hypothesis 0.5.

**5.4 Reasoning.** None in the knowledge-graph sense. "Reasoning" is the LLM agent in Deep Search driving search/read tools [CLAIM-sourcegraph-06]. No inference of transitive dependencies beyond references in SCIP relationships.

**5.5 Concurrency / transactions / partitioning.** Gitserver is sharded; zoekt shards per repo; Kubernetes (Helm) is the vendor-recommended scalable topology, Docker Compose is single-node; switching requires redeploy + DB migration [CLAIM-sourcegraph-07]. Postgres is the only transactional store described.

**5.6 Caching.** Not publicly documented beyond the default-branch trigram index. Deep Search keeps conversation state per user; sharing is off by default [CLAIM-sourcegraph-06].

**5.7 Versioning.** Index freshness equals "commit of the last upload". Default-branch-only trigram index means history search needs `searcher`. Auto-indexing keeps indexes "up to date" via executors [CLAIM-sourcegraph-10]. No bitemporal model.

**5.8 Security.** Repo-level authz from code host, explicit permissions API union with synced set, enforced across all features reading repository data; invisible repos are hidden including existence; admins bypass by default; without a valid licence every repo is treated as public [CLAIM-sourcegraph-09]. No file-level or symbol-level ACLs (except Perforce).

## 6. Functional and non-functional requirements inferred

| ID | Requirement derived | Basis |
|---|---|---|
| FR-1 | Every code fact answers (repo, commit, path, range, symbol) | SCIP/precise nav |
| FR-2 | Index must be producible in CI and uploadable, with auto-indexing as option | [CLAIM-sourcegraph-10] |
| FR-3 | Fallback tier (text/symbol heuristics) when no precise index exists | [CLAIM-sourcegraph-10] |
| FR-4 | Permission filter before any result, snippet or LLM context | [CLAIM-sourcegraph-09] |
| FR-5 | Agentic Q&A must show searches run and files read as sources | [CLAIM-sourcegraph-06] |
| NFR-1 | Reverse proxies must tolerate 5 min streams | [CLAIM-sourcegraph-06] |
| NFR-2 | Offline operation needs an offline licence | [CLAIM-sourcegraph-08] |
| NFR-3 | ARM64 not supported in production (vendor) | [CLAIM-sourcegraph-07] |

## 7. Performance and resource model

No vendor benchmark was retrieved; **NOT PUBLICLY VERIFIED**. Qualitative model: Zoekt memory-maps index shards, so RAM and disk scale with indexed default-branch bytes (trigram index typically a multiple of source size: hypothesis, not measured here). Precise-index cost = indexer build time (compiler-grade for scip-java/clang/typescript) + upload size. Deep Search latency is minutes with SSE (up to 5 min) [CLAIM-sourcegraph-06] and credit-metered. Failure modes: stale index vs HEAD; missing indexer for language -> silent fallback to heuristic navigation; license check failure disables Enterprise features [CLAIM-sourcegraph-08].

## 8. Strengths and use-case-specific advantages

| ID | Strength | Match / exceed approach |
|---|---|---|
| STR-sourcegraph-01 | Two-tier navigation: precise SCIP index when present, heuristic fallback otherwise | Match: EOIP keeps Tree-sitter heuristic tier (BL-42) and adds SCIP ingestion as precise tier; exceed by recording tier and confidence on every edge |
| STR-sourcegraph-02 | Repo-level permission enforcement across every feature | Match then exceed: apply to graph traversal, answers and agent context (closes BL-18), down to file/path level |
| STR-sourcegraph-03 | Trigram regex search with symbol-aware ranking (Zoekt, Apache-2.0) | Integrate/reuse Zoekt as optional search sidecar; EOIP BL-15 hybrid search lacks exact-regex code search |
| STR-sourcegraph-04 | Deep Search shows its searches and files read | Match with EOIP evidence manifests (BL-41), citing file/line/revision |
| STR-sourcegraph-05 | Batch Changes: server-side fleet-wide change with PRs | Defer; EOIP is read-oriented (BL-47, ADR-007) |

## 9. Limitations with root causes

| Class | Limitation | Type | Claim |
|---|---|---|---|
| Licensing | Core closed since 2023/2024; public snapshot archived; Enterprise licence required for precise nav, Deep Search | licensing restriction (verified) | [CLAIM-sourcegraph-03/04] |
| Licensing/ops | Periodic licence check; air-gap needs special key from support | intentional trade-off | [CLAIM-sourcegraph-08] |
| AI egress | Deep Search works only with Sourcegraph Model Provider, no BYOK; Cody needs Cody Gateway or third-party provider | architecture/vendor coupling (verified) | [CLAIM-sourcegraph-06/13] |
| Product churn | Cody Free/Pro/Starter ended within about 4 weeks of notice (2025-06-25 to 2025-07-23); Amp separated | verified | [CLAIM-sourcegraph-01] |
| Granularity | Permissions are repo-level | verified | [CLAIM-sourcegraph-09] |
| Data model | No queryable code knowledge graph; three disjoint stores; no temporal/bitemporal facts | reasoned inference | |
| Algorithmic dead-ends | Trigram index covers default branch only; other branches need slower scan | verified | [CLAIM-sourcegraph-11] |
| Operational/hardware | Multi-service topology (gitserver, zoekt, Postgres x3, executors); ARM64 unsupported for production | verified | [CLAIM-sourcegraph-07] |
| User/developer friction | Precise nav needs one indexer per language wired into CI or executors; otherwise silent fallback | verified (docs) / inference | [CLAIM-sourcegraph-10] |

## 10. Deployment, licensing, redistribution, operational viability under EOIP constraints

| Constraint | Assessment |
|---|---|
| Self-hosted / one-node | Docker Compose single node and Helm available [CLAIM-sourcegraph-07]; heavy for a sidecar |
| Air-gap | Possible only with a vendor-issued offline licence; LLM features additionally need a reachable provider; Deep Search impossible without Sourcegraph Model Provider -> **not viable for default-local AI** [CLAIM-sourcegraph-06/08] |
| Redistribution / white-label | Proprietary Enterprise licence; **legal-review trigger**: no OEM/embedding right visible in public pages; cannot bundle |
| Backend neutrality | n/a: it is a separate product, not a graph backend |
| Tenant isolation | Single-instance repo-level authz; not a multi-tenant SaaS substrate (reasoned) |
| Verdict | Do not embed. Reuse only: Zoekt (Apache-2.0), SCIP protocol and indexers (Apache-2.0 per repo pages; scip-python licence file type not confirmed). Optionally integrate a customer's existing Sourcegraph as an external read-only source via SourceEvent adapter, never as a dependency |

## 11. Competitive delta against the EOIP verified baseline

| Area | Sourcegraph | EOIP baseline | Delta |
|---|---|---|---|
| Symbol extraction | compiler-grade SCIP for 10+ languages | BL-42: Python/TS via `codegraph/parser.py`; Tree-sitter referenced in 2 files; SCIP/LSIF absent | EOIP is heuristic and 2-language; gap on precision and breadth |
| Incremental re-index | per-commit uploads, auto-indexing | BL-42 `ingestion/incremental_indexer.py:30` | different mechanism; EOIP has replay/idempotency (BL-24) that Sourcegraph does not expose |
| Permissions | repo-level authz across all features | BL-17 captured, **BL-18 Absent** in retrieval | Sourcegraph ahead; EOIP must close as P0 |
| Digital thread (Jira->PR->commit->function->incident) | not a product feature; code-only | BL-41 lineage + BL-42 diff hunks, link to Jira/incident connectors | EOIP differentiates on cross-source graph |
| Agentic answers | Deep Search with sources | BL-16 deterministic GraphRAG, BL-47 MCP | Sourcegraph LLM-driven; EOIP local-first |
| Regex code search | trigram | BL-15 hybrid RRF (not trigram) | gap |

## 12. Strength-adoption cards and inversion cards

| Card | Detail |
|---|---|
| STR-sourcegraph-01 | evidence [CLAIM-sourcegraph-10]; value: precision where indexers exist without losing coverage; **match**; design: `CodeFact.provenance_tier = scip|treesitter|textual`, query prefers highest tier per symbol; acceptance: for a 3-language fixture repo, 100% of SCIP-resolvable references return tier=scip and heuristic results never override them |
| STR-sourcegraph-02 | [CLAIM-sourcegraph-09]; **exceed**; design: path-level ACL attached to Document/Symbol nodes, filter in traversal and in LLM context builder; acceptance: user without access to repo X gets zero nodes, snippets, counts or citations from X in 200 adversarial queries |
| STR-sourcegraph-03 | [CLAIM-sourcegraph-11/12]; **integrate** Zoekt as optional sidecar, with ACL post-filter; acceptance: regex query p95 on 1M-line corpus on one node under agreed budget (budget to set in POC) |

**INV-sourcegraph-01 — closed core and licence-gated precision (licensing, proven).** Target: Sourcegraph Enterprise 2026, any workload needing OEM. Limitation: precise nav and Deep Search are proprietary [CLAIM-sourcegraph-03/04/10]. Alternative: build on open SCIP + Tree-sitter, store facts in EOIP graph. Worse when: customer already owns Sourcegraph and wants its UI. Options: (1) integrate customer's Sourcegraph via adapter; (2) native SCIP ingestor (`.scip` protobuf -> SourceEvents -> mutation gateway); (3) long-term: polyglot code graph merged with Jira/CI/incident nodes. Selected: 2 then 3. Sketch: `scip-<lang> -> index.scip -> scip_to_events.py -> validation gate (BL-28) -> GraphStore`. POC: 3 repos (Python, TS, Java), success = definition/reference parity >= 95% vs `scip print` ground truth, ingestion time and RAM baseline recorded. Dependencies: protobuf runtime, indexer toolchains in CI. Failure cases: index for a commit the user cannot see (permission leak) -> store ACL with the index. Defensibility: the cross-source digital thread is not reproducible by a code-only tool. Decision: **ADOPT** (option 2).

**INV-sourcegraph-02 — AI features require vendor model provider (deployment/coupling, proven).** Deep Search works only with Sourcegraph Model Provider; BYOK unsupported [CLAIM-sourcegraph-06]. Alternative: local-model agent over typed, bounded tools (search, read_file, find_refs) with egress policy (BL-45). Worse when: frontier-model quality is mandatory and egress is approved. Options: (1) none; (2) EOIP agent runtime with code tools; (3) tool-use evals. POC: 50 code questions with gold file/line answers, metric citation precision and recall vs a baseline of BM25 + reranker (GraphRAG not assumed superior). Decision: **EXPERIMENT**.

**INV-sourcegraph-03 — repo-level permissions (governance, proven).** [CLAIM-sourcegraph-09]. Alternative: path/symbol-level ACL inherited from source. Worse when: code host exposes only repo-level ACLs anyway. Decision: **ADOPT** as part of closing BL-18. POC: seeded leak tests.

Seed hypothesis check: the Master Prompt seed "Palantir/Glean/Rovo: SaaS or heavyweight, limited air-gap" is not Sourcegraph-specific; for Sourcegraph it is **partly validated** (air-gap possible via offline licence, AI path not).

## 13. Per-capability decisions

| CAP | Decision | Note |
|---|---|---|
| CAP-66 precise code graph | INTEGRATE SCIP (open format) / BUILD ingestor; REJECT embedding Sourcegraph | |
| CAP-67 incremental re-indexing | BUILD on `incremental_indexer.py`, key by (repo, path, blob SHA) | |
| CAP-69 change-impact thread | BUILD (differentiator) | |
| CAP-46 source-ACL in retrieval | BUILD (P0) | |
| CAP-54 full-text/regex | EXPERIMENT: Zoekt sidecar | |
| CAP-56 GraphRAG/agent code Q&A | EXPERIMENT local-model agent | |
| CAP-68 dependency risk | DEFER (not shown by Sourcegraph) | |
| CAP-77 licensing/TCO | REJECT dependency on Enterprise licence | |

## 14. Concrete tests, POC, and acceptance conditions

1. SCIP ingest POC (INV-01) as above.
2. Permission leak suite: users A/B, repo X private; assert no node, snippet, count, citation or cached answer from X reaches B.
3. Zoekt sidecar: index fixture, compare regex hit set with `git grep` (must be equal on default branch).
4. Fallback tier test: delete SCIP index; confirm Tree-sitter tier answers with lower confidence flag.
5. Air-gap test: run ingestion and query with network namespace denied; zero outbound connections.
6. Competitor reproduction test (optional): customer Sourcegraph as external source over GraphQL, read-only.

## 15. Risks, trade-offs, and open research questions

| Risk / question | Note |
|---|---|
| Amp spin-off and exact corporate structure unverified | confidence 0.4 |
| Server-side SCIP storage schema unknown | hypothesis only |
| Whether Cody Enterprise can use a fully local model | no source found |
| Pricing ($16K+) vendor page vs $59/user third-party | unreconciled |
| Zoekt maintenance continuity if vendor priorities shift | Apache-2.0 allows fork |
| Legal review: any reuse of snapshot-era Apache code (pre-2023) needs provenance check | trigger |

## Appendix A. Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | status, licence history, Cody/Amp |
| D2 | 2 | workflows |
| D3 | 4 | services, planes |
| D4 | 5.1-5.2 | trigram shards, SCIP uploads (hypothesis) |
| D5 | N/A | no ontology/schema layer; SCIP kinds only |
| D6 | 5.2-5.3 | regex-to-trigram, nav resolution |
| D7 | 5.4 | none; LLM agent only |
| D8 | 5.5 | sharded gitserver/zoekt, Postgres; no HA detail |
| D9 | 2, 5.7 | code host sync, CI upload |
| D10 | N/A | no entity resolution; symbol strings |
| D11 | 5.7 | commit-based indexes; no bitemporal |
| D12 | N/A | none |
| D13 | 3, 5.4 | Deep Search, MCP, Cody |
| D14 | N/A | NL query of code via Deep Search, not graph query languages |
| D15 | N/A | no ontology governance |
| D16 | 3 | web, IDE, code-host overlays |
| D17 | 3 | GraphQL, `src`, SCIP indexers |
| D18 | 5.8, 9 | repo-level authz, licence check |
| D19 | 10 | single-instance; not multi-tenant substrate |
| D20 | 7 | no benchmarks verified |
| D21 | 1, 10 | Enterprise from $16K, closed core |
| D22 | 10 | SCIP open export; rest proprietary |
| D23 | 10 | no patents examined: NOT PUBLICLY VERIFIED |
| D24 | App. C | mostly vendor docs; third-party for Amp |

## Appendix B. Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-66 | native (enterprise-only precise) | sourcegraph-10 | BL-42 Partial | INTEGRATE SCIP / BUILD | P1 |
| CAP-67 | native (auto-indexing, enterprise) | sourcegraph-10 | BL-42 Implemented (2 langs) | BUILD | P1 |
| CAP-69 | absent | sourcegraph-05 | BL-41/42 Partial | BUILD | P1 |
| CAP-46 | native (repo-level) | sourcegraph-09 | BL-18 Absent | BUILD | P0 |
| CAP-54 | native (Zoekt) | sourcegraph-12 | BL-15 Implemented (no trigram) | EXPERIMENT | P2 |
| CAP-56 | partial (Deep Search, vendor models) | sourcegraph-06 | BL-16 Implemented | EXPERIMENT | P2 |
| CAP-68 | unknown | n/a | none cited | DEFER | P3 |
| CAP-77 | proprietary | sourcegraph-03/05 | BL-22 | REJECT dependency | P2 |

## Appendix C. Evidence records

| CLAIM-ID | Product/version/date | Claim | Class | Source | Dates | Confidence | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-sourcegraph-01 | Cody plans, 2025 | Free/Pro sign-ups stopped 2025-06-25; discontinued 2025-07-23 incl. Starter; Cody Enterprise remains; Starter keeps Code Search | Officially documented | "Changes to Cody Free, Pro and Enterprise Starter plans", https://sourcegraph.com/blog/changes-to-cody-free-pro-and-enterprise-starter-plans | 2025 / 2026-10-26 | 0.9 | Wikipedia wording looser |
| CLAIM-sourcegraph-02 | Amp, 2025 | Vendor recommended Amp (ampcode.com); spin-off Dec 2025 reported by review sites | Official (recommendation) / Third-party (spin-off) | same blog; https://www.promptquorum.com/power-local-llm/sourcegraph-cody-review | 2026-10-26 | 0.4 for spin-off | no official confirmation found |
| CLAIM-sourcegraph-03 | licence history | Apache-2.0 2018; relicensed to Sourcegraph Enterprise licence 2023-06-13 | Third-party report | https://en.wikipedia.org/wiki/Sourcegraph | 2026-10-26 | 0.6 | handbook https://handbook.sourcegraph.com/product/licensing still says Apache |
| CLAIM-sourcegraph-04 | core repo, Aug 2024 | Core moved to private monorepo; public snapshot archived 2024-09-30, "primarily non-OSS-licensed files" | Observed (repo README) + press | https://github.com/sourcegraph/sourcegraph-public-snapshot ; https://devclass.com/2024/08/21/sourcegraph-makes-core-repository-private-co-founder-complains-open-source-means-extra-work-and-risk | 2024 / 2026-10-26 | 0.85 | press date 21 vs 22 Aug |
| CLAIM-sourcegraph-05 | pricing page | Single Enterprise plan from $16K/yr; Code Search, Deep Search, Batch Changes, Code Insights, MCP; Cody not listed | Officially documented | https://sourcegraph.com/pricing | 2026-10-26 | 0.8 | third-party $59/user Cody price |
| CLAIM-sourcegraph-06 | Deep Search | Enterprise/Starter; Sourcegraph Model Provider only, no BYOK; SSE up to 5 min; credits | Officially documented | https://sourcegraph.com/docs/deep-search | 2026-10-26 | 0.85 | |
| CLAIM-sourcegraph-07 | deployment | Cloud, Helm, Docker Compose; ARM64 not for production; switching needs migration | Officially documented | https://sourcegraph.com/docs/admin/deploy | 2026-10-26 | 0.85 | |
| CLAIM-sourcegraph-08 | licensing/air-gap | Periodic licence check; "Allow air gapped" offline keys via support (5.1+) | Third-party search digest of vendor docs | https://docs-legacy.sourcegraph.com/admin/licensing ; https://about.sourcegraph.com/handbook/ce/license_keys | 2026-10-26 | 0.6 | `/docs/admin/air-gapped` returned 404 |
| CLAIM-sourcegraph-09 | permissions | Repo-level sync/webhook/explicit API; hidden repos; admins bypass; no licence = public | Officially documented | https://sourcegraph.com/docs/admin/permissions | 2026-10-26 | 0.85 | |
| CLAIM-sourcegraph-10 | precise nav | Opt-in Enterprise; SCIP; fallback search-based; manual/CI/auto-indexing; language list | Officially documented | https://sourcegraph.com/docs/code-search/code-navigation/precise_code_navigation | 2026-10-26 | 0.9 | |
| CLAIM-sourcegraph-11 | architecture | gitserver, searcher, zoekt (default-branch trigram), worker, executors, Postgres, codeinsights-db | Officially documented | https://sourcegraph.com/docs/admin/architecture | 2026-10-26 | 0.8 | other services undocumented there |
| CLAIM-sourcegraph-12 | Zoekt | Apache-2.0; maintained by Sourcegraph since 2017 fork of google/zoekt; trigram + syntactic parsing | Observed (repo page) | https://github.com/sourcegraph/zoekt | 2026-10-26 | 0.85 | |
| CLAIM-sourcegraph-13 | Cody Enterprise | Needs Cody Gateway or third-party LLM; local-model path unconfirmed | Third-party digest of vendor docs | https://sourcegraph.com/docs/cody/clients/enable-cody-enterprise | 2026-10-26 | 0.5 | |

## Appendix D. Assumptions

1. "Sourcegraph / Cody and successors" = Sourcegraph Code Search, Deep Search, Cody Enterprise; Amp treated as a separate lineage.
2. Server-side code-intel internals are hypotheses because the core is closed.
3. Dates not shown on pages (releases) are left UNVERIFIED rather than inferred.
4. Pricing quoted as vendor page values, not validated against contracts.
