# C15 — Augment Context Engine

| Field | Value |
|---|---|
| Registry ID | T-C15-augment-context |
| Tier | B — commercial code-context retrieval service exposed via MCP |
| Versions examined | Context Engine MCP, GA 2026-02-06 (per changelog via search summary); no version numbers published |
| Verified on | 2026-10-26 (brief date 2026-10-18) |
| Worker | V28 (W27 scope) |

## 1. Identity, current status, tier, and sources

| Item | Finding | Claim |
|---|---|---|
| Identity | Augment Code's semantic codebase retrieval ("Context Engine"), offered to any MCP-compatible agent; part of the closed-source Augment Code product | [CLAIM-augment-context-01][CLAIM-augment-context-04] |
| Status | Active; MCP server GA 2026-02-06 (changelog page via search summary, not opened) | [CLAIM-augment-context-02] |
| Licence | Proprietary SaaS; third-party review says you cannot self-host (contradicted by vendor comparison pages claiming VPC, on-prem, air-gapped options) | [CLAIM-augment-context-04] |
| Tool surface | Docs name one tool, `codebase-retrieval` | [CLAIM-augment-context-03] |

## 2. Primary problem, workloads, workflows

Give coding agents accurate repository context (patterns, architecture, history, docs, tickets) rather than file-by-file grep. Workflow: agent calls `codebase-retrieval` over MCP; local mode indexes the working directory in real time; remote mode indexes default branches of repos installed through the GitHub App and updates on push [CLAIM-augment-context-03].

## 3. Feature inventory

| Feature | Status | Claim |
|---|---|---|
| MCP server (stdio local via Auggie CLI; HTTP remote api.augmentcode.com/mcp) | present | [CLAIM-augment-context-01][CLAIM-augment-context-03] |
| Real-time local index | present | [CLAIM-augment-context-03] |
| Remote multi-repo index, default branches only | present | [CLAIM-augment-context-03] |
| Commit history, patterns, external docs/tickets | stated present | [CLAIM-augment-context-03] |
| OAuth / API key | present | [CLAIM-augment-context-03] |
| Self-hosted / air-gapped | conflicting (vendor says yes; third party says no) | [CLAIM-augment-context-04] |
| Retention and privacy policy for MCP | not on pages read | [CLAIM-augment-context-03] |
| Graph query API | absent | [CLAIM-augment-context-03] |

## 4. Architecture diagram

```
 agent (Claude Code/Cursor/...) --MCP--> [local: Auggie CLI stdio, index of working dir]
                                  \--MCP/HTTP--> [remote: Augment-hosted engine, index of GitHub default branches]
 retrieval -> ranked code context -> agent LLM (customer's choice)
```

## 5. Under-the-hood reconstruction

Index build, embedding model, ranking, freshness and branch handling: NOT PUBLICLY VERIFIED (blog says nothing on indexing) [CLAIM-augment-context-01]. Hypothesis (reasoned, 0.4): chunking plus embeddings plus lexical signals plus recency/commit features, rank-fused. Concurrency, security (ACLs, per-user isolation of the remote index): NOT PUBLICLY VERIFIED. Billing: LLM tokens at provider list price plus 40% service fee, about $0.03-0.06 per query estimated by Augment [CLAIM-augment-context-03].

## 6. Requirements inferred

Real-time local indexing; push-triggered remote index; authenticated MCP endpoint; token-metered billing.

## 7. Performance and resource model

Vendor evaluation: 300 Elasticsearch PRs x 3 prompts (900 attempts); agents turned a prompt into a PR, scored on correctness, completeness, best practices, code reuse, unsolicited docs; reported gains with MCP of 71% (Cursor+Claude Opus 4.5), 80% (Claude Code+Opus 4.5), 30% (Cursor+Composer-1). Vendor-run, single repository, no independent reproduction; a third-party analysis calls them self-reported [CLAIM-augment-context-01][CLAIM-augment-context-02]. Latency/resource figures: NOT PUBLICLY VERIFIED.

## 8. Strengths

| Strength | Match or exceed |
|---|---|
| Agent-neutral MCP delivery of codebase context | EOIP MCP (BL-47) already exposes graph tools; add a code-context tool |
| Real-time working-tree index | match with incremental indexer (BL-42) |
| Cross-source context (commits, docs, tickets) | EOIP graph joins this natively (J1) |

## 9. Limitations

| Class | Finding | Claim |
|---|---|---|
| Licensing/commercial | Proprietary, metered with 40% fee | [CLAIM-augment-context-03] |
| Deployment | Remote index requires cloud and GitHub App; air-gap conflict | [CLAIM-augment-context-04] |
| Evidence | Benchmark vendor-run, one repo | [CLAIM-augment-context-01] |
| Governance | Retention, ACL behaviour unpublished | [CLAIM-augment-context-03] |

## 10. Deployment, licensing, redistribution

SaaS or local CLI plus hosted retrieval; no redistribution rights found; proprietary; breaches EOIP no-mandatory-cloud rule if remote mode is required. Legal-review trigger: yes (proprietary; usage-metered; data handling).

## 11. Competitive delta against EOIP baseline

BL-47: EOIP MCP has 18 read tools incl. `query(plan)`, but no codebase-retrieval; BL-14 vectors are hashing+pure-Python HNSW (weak); BL-42 incremental indexer exists for 2 languages. Delta: retrieval quality and polyglot breadth. Related: C15-sourcegraph.md (self-hostable code search + SCIP), C15-greptile.md.

## 12. Cards

`STR-augment-context-01 | Augment | agent-neutral codebase retrieval via MCP | CLAIM-01,03 | J1 agent context | match | EOIP tool `code_context(query, scope)` fusing BM25 + embeddings + graph neighbours with ACL filter | bench vs BM25 and dense baselines on 50 questions, no leakage of ACL-denied files`

INV-augment-context-01: target remote mode; workload air-gapped enterprise. Limitation: hosted index (documented, CLAIM-03). Root cause: deployment (proven for remote mode). Alternative: local engine over EOIP indexes; worse where cross-repo scale is huge and no local GPU. Options: (a) customer chooses Augment local CLI under egress policy, (b) native tool, (c) differentiated: graph-aware, permission-aware retrieval. Selected (b). POC: 3 repos; metric: answer recall vs BM25/dense/hybrid baseline (per Master Prompt trap 3). Decision: EXPERIMENT. Seed hypotheses in §10.5 do not target Augment.

## 13. Decisions

| Capability | Decision |
|---|---|
| CAP-55 hybrid code retrieval | BUILD (extend BL-15) |
| CAP-59 code-context MCP tool | BUILD |
| Augment as dependency | REJECT (proprietary, cloud path) |

## 14. Tests and acceptance

Offline run with no external calls; retrieval benchmark vs BM25, dense, hybrid, reranked; ACL-denied files absent from results.

## 15. Risks and open questions

Self-host reality; data retention; pricing churn; vendor benchmark validity.

## Appendix A — Dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Proprietary, GA 2026-02 |
| D2 | 2 | Agent context |
| D3 | 4 | Local/remote MCP |
| D4 | 5 | Not public |
| D5 | N/A | None |
| D6 | 5 | Not public |
| D7 | N/A | None |
| D8 | N/A | Not public |
| D9 | 3 | GitHub App, working dir |
| D10 | N/A | None |
| D11 | 3 | Commit history stated |
| D12 | N/A | None |
| D13 | 3,5 | MCP tool |
| D14 | N/A | Absent |
| D15 | N/A | None |
| D16 | N/A | Agent hosts |
| D17 | 3 | Auggie CLI |
| D18 | 3,9 | OAuth/API key; ACL unknown |
| D19 | N/A | Not described |
| D20 | 7 | Vendor claim only |
| D21 | 5,10 | Token plus 40% |
| D22 | N/A | None |
| D23 | N/A | Not checked |
| D24 | 7,15 | Vendor-run |

## Appendix B — Capability mapping

| CAP | Technology | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-55 | native (closed) | 01 | BL-15 Implemented | BUILD | P1 |
| CAP-59 | native | 03 | BL-47 Implemented | BUILD | P1 |
| CAP-53 | unknown | 01 | BL-14 Partial | DEFER | P2 |
| CAP-50 | unknown | 04 | BL-45 | REJECT dependency | P2 |

## Appendix C — Evidence records

| CLAIM | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| 01 | MCP launch post | semantic search for MCP agents; local/remote; benchmark 300 PRs | Officially documented (vendor) | https://www.augmentcode.com/blog/context-engine-mcp-now-live | 2026-02 (month per search result) / 2026-10-26 | 0.7 | third party says single-repo self-reported |
| 02 | changelog | GA 2026-02-06, 1,000 free requests through Feb 2026 | Third-party report (search summary) | https://www.augmentcode.com/changelog/context-engine-mcp-in-ga | 2026-02-06 / 2026-10-26 | 0.6 | none |
| 03 | docs | `codebase-retrieval`, auth, modes, indexing, pricing 40% fee | Officially documented | https://docs.augmentcode.com/context-services/mcp/overview.md | 2026-10-26 | 0.8 | none |
| 04 | third-party review vs vendor comparison pages | closed-source/no self-host vs VPC/on-prem/air-gap claims | Third-party report | https://www.fast.io/resources/augment-ai-review-2026.md ; https://www.augmentcode.com/tools/augment-code-vs-tabnine-model-choice-privacy-and-features | 2026 / 2026-10-26 | 0.4 | the two sources conflict |

## Appendix D — Assumptions

Changelog and comparison pages taken from search summaries, not opened. "Closed-source" from the third-party review.
