# C07 — Onyx (formerly Danswer)

| Field | Value |
|---|---|
| Registry ID | T-C07-onyx |
| Tier | A — closest open-source, self-hosted enterprise-search/permissioned-RAG competitor |
| Versions examined | v5.0.0 (changelog 2026-10-23; GitHub release list shows "24 Oct"), v5.0.0-beta.3, v4.9.x; Helm chart onyx-0.9.24; docker-compose on `main` (OpenSearch 3.6.0, Postgres 15.2, Redis 7.4) |
| Verified on | 2026-10-26 (brief states 2026-10-18; actual session date used) |
| Worker | V04 |

## 1. Identity, current status, tier, and sources

Onyx (GitHub `onyx-dot-app/onyx`, formerly `danswer-ai/danswer`; rename visible in search results to `danswer-ai/danswerai`) is an open-source "AI platform / enterprise search" with chat, agents, deep research, connectors, MCP and code-interpreter features. Active: v4.x to v5.0.0 inside about a month; roughly 33k stars [CLAIM-onyx-01]. **Two licences in one repo**: everything outside `ee` directories is MIT (Expat); content under `backend/ee`, `web/src/app/ee`, `web/src/ee` is under the "Onyx Enterprise License" [CLAIM-onyx-02]. Commercial plans: Business $20/user/month; Enterprise custom, listing SSO (OIDC/SAML), on-prem deployments, white-labelling, hook extensions [CLAIM-onyx-04]. The Enterprise Edition licence text was **not read in full** — legal review required. Cross-category: Glean (SaaS) `C07-glean-enterprise.md` is the commercial analogue.

## 2. Primary problem, target workloads, concrete example workflows

Problem: permission-respecting RAG/chat across company tools, deployable in the customer's environment, with any LLM.

| Workflow | Onyx mechanism |
|---|---|
| Ask across Confluence + Jira + Slack + Drive with answers limited to what the asker can see | Connectors with Auto Sync Permissions (EE) feeding per-document ACL sets in the index [CLAIM-onyx-03, -07] |
| Run on a laptop or small VM | "Lite" mode under 1 GB memory, no indexing; "Standard" with indexing, workers, model servers [CLAIM-onyx-01] |
| Deep research / custom agents / MCP actions | Features listed in README; MCP server service in compose [CLAIM-onyx-01, -06] |
| Local model | Ollama, GPT4All or any OpenAI-compatible endpoint [CLAIM-onyx-10] |

## 3. Feature inventory

| Feature | Status | Evidence |
|---|---|---|
| Hybrid (keyword + vector) search, OpenSearch as sole document index since v4.0.0; Vespa removed in 5.0 | Present | CLAIM-05 |
| 56 official connectors (wikis 18, storage 8, ticketing 10, messaging 8, meetings 2, sales 4, code 3, other 3) | Present | CLAIM-03 |
| Auto Sync Permissions, 14 connectors: Confluence, Jira, Google Drive, Gmail, Slack, Salesforce, GitHub, Box, Canvas, SharePoint, Teams, Outlook, Zoom, YouTrack | **Enterprise Edition** | CLAIM-03 |
| Connector visibility: private / public / synced | Present (private and public in CE) | CLAIM-03 |
| Query-time cc-pair access filter (shadow/enforce flag), Editor/Operator roles on cc-pairs | Present in v5.0.0 | CLAIM-08 |
| SSO OIDC/SAML, on-prem packaging, white-labelling, data exports | Enterprise plan | CLAIM-04 |
| RBAC and permission inheritance | Business plan per pricing page | CLAIM-04 (see contradiction) |
| Agents, deep research, web search, code interpreter, voice, MCP, image generation | Present | CLAIM-01 |
| Knowledge graph | **Partial / de-emphasised**: `backend/onyx/kg` (models, setup, resets); v5.0.0 notes say KG-pipeline variables are now ignored; no KG docs page found (404) | CLAIM-09 |
| Graph query language, ontology, reasoning, temporal model | Absent | CLAIM-09 |
| Air-gap guide | NOT PUBLICLY VERIFIED | CLAIM-10 |
| CLI/SDK | API plus Slack bot (`onyxbot`); no graph SDK | CLAIM-01 |

## 4. Architecture diagram

```
 Sources (56 connectors; federated connectors for live Slack)
     | pull on schedule: refresh 30 min default, prune 30 days default
     v
 [background workers (celery-style)] --> permission-sync workers (EE) --> ExternalAccess(emails, group ids, is_public)
     |  chunk + embed (indexing_model_server)                                      |
     v                                                                             v
 [OpenSearch 3.6 : chunks, vectors (quantisation in 5.0), ACL strings] <--- DocumentAccess.to_acl() prefixed strings
 [Postgres 15 : users, connectors, cc-pairs, chats, KG tables]  [Redis cache/queue]  [object store: SeaweedFS (MinIO retired)]
     ^
 [api_server] <-> [inference_model_server (query embeddings)] ; [mcp_server] ; [web_server + nginx] ; [code-interpreter]
     |
 LLM provider: cloud API or Ollama / GPT4All / OpenAI-compatible (customer-chosen)
```

## 5. Under-the-hood reconstruction

Pinned to `main` as of 2026-10-26 (v5.0.0 tag not individually diffed); paths from `backend/onyx`.

| Layer | Verified from public files | Hypothesis |
|---|---|---|
| Services | Compose: api_server, background, mcp_server, web_server, inference_model_server, indexing_model_server (`INDEXING_ONLY=True`), relational_db Postgres 15.2, opensearch 3.6.0, Redis 7.4 (tmpfs), nginx, object store SeaweedFS plus legacy MinIO copy job, code-interpreter 0.4.9 [CLAIM-06] | Worker queues partitioned by connector/permission/pruning (not read) |
| Index | OpenSearch is "the search backend and is enabled by default"; vector quantisation added in 5.0; Vespa removed [CLAIM-05, -06] | Hybrid scoring weights and schema (not read) |
| ACL model | `access/models.py`: frozen `ExternalAccess{external_user_emails, external_user_group_ids, is_public}`; soft limit `MAX_NUM_ENTRIES = 5000` "not enforced, so callers must check"; `empty()` makes a doc private as fallback; `DocumentAccess` adds internal `user_emails`, `user_groups`; `to_acl()` emits prefixed strings (`prefix_user_email`, `prefix_user_group`, `prefix_external_group`, `PUBLIC_DOC_PAT`); query filters must be formatted identically [CLAIM-07] | Filter executes as a term filter inside the OpenSearch query so unauthorised chunks never reach the LLM; consistent with "ACL strings" design but the filter code was not read |
| Permission freshness | Documents' ACL set in the index; sync loops update ACLs; v5.0.0 adds query-time cc-pair access filter with shadow/enforce flag [CLAIM-08] | Dual check = index ACL AND connector-level check; shadow mode logs would-be denials before enforcing |
| Group sync | Entra nested-group listing optimisation in v4.9.4; Google Drive permission sync resumes from checkpoint (beta.3) [CLAIM-08] | — |
| KG | `kg/models.py` classes: `KGConfigSettings` (enabled/exposed, vendor domains, ignored email domains, coverage date range, max recursion depth), `KGEntityTypeDefinition` (grounded vs ungrounded types, attributes, classifications), `KGAttributeImplicationProperty` (implied entities from metadata, e.g. account/employee from email), `KGStage` states (not started, extracting, extracted, normalized, failed, skipped) [CLAIM-09] | Entity/relationship tables in Postgres, LLM extraction at index time; relationship to retrieval unverified. 5.0 treats pipeline vars as ignored: likely deprecated/removed |
| Pipeline | Connector -> doc -> chunk -> embed -> index; "Contextual Retrieval" toggle without re-index (beta.3) [CLAIM-08] | — |
| Tenancy | Not examined; EE features toggle inside one codebase (PRs: drop two EE env vars; downgrade to Community) [CLAIM-11] | Multi-tenant mode exists historically; not verified for 2026 |
| Transactions/versioning | Postgres + OpenSearch eventually consistent | No temporal or bitemporal model found |

## 6. Functional and non-functional requirements inferred

FR: per-connector private/public/synced visibility; ACL sets stored with each chunk; deleted-source pruning (default 30 days); incremental checkpointing for permission sync; pluggable LLM and embedding providers; admin-visible connector state. NFR: runs as ~10 containers; Lite under 1 GB RAM; GPU optional (commented out in compose); embedding model weights cached in volumes (`model_cache_huggingface`), so first start needs model download unless pre-seeded (air-gap hypothesis).

## 7. Performance and resource model

No independent benchmark retrieved; no vendor throughput figures cited here. Resource facts from compose: separate indexing and inference model servers, OpenSearch heap and disk, object store. Scaling: Kubernetes/Helm charts (onyx-0.9.24); scaling behaviour NOT PUBLICLY VERIFIED. Failure modes noted in release notes: per-connector deletion cleanup bounded into batches, embedding rate limit added globally (indexing), Jira permission checks sampled across projects (beta.3) — suggests permission sync at scale needed tuning [CLAIM-08]. Smaller local LLMs require longer timeouts and disabling LLM-driven steps (query rephrasing, chunk filtering) per Onyx docs [CLAIM-10].

## 8. Strengths and use-case-specific advantages

| Strength | Why it matters | Match / exceed |
|---|---|---|
| Per-chunk ACL strings in the index plus 14 permission-syncing connectors | Real source-ACL retrieval, the exact EOIP P0 gap (BL-18) | Match design; exceed with fact-level ACL and tenant partition |
| 56 connectors, 30-minute default refresh | Breadth | Integrate selectively; EOIP connectors emit SourceEvents, not index writes |
| MIT core, self-hostable in Docker/K8s, local LLM | Closest to EOIP constraints | Reuse patterns; consider as optional unstructured-search sidecar |
| Shadow/enforce rollout of a new access filter | Safe security migrations | Adopt for BL-18 rollout |
| Credential-family framework (Atlassian/Google/Microsoft) | Fewer re-auths | Match |

## 9. Limitations with root causes

| Limitation | Class | Root cause | Evidence |
|---|---|---|---|
| Permission sync gated to Enterprise licence | Licensing | Open-core split | CLAIM-03 |
| White-label, SSO, "on-premise deployments" listed under Enterprise plan though CE is MIT-self-hostable | Licensing/commercial ambiguity | Plan-page wording | CLAIM-04 |
| Docs and pricing page disagree on where permission features sit (Business lists "permission inheritance"; docs call Auto Sync Permissions EE) | Doc inconsistency | — | CLAIM-03, -04 |
| Soft ACL entry cap (5,000) not enforced centrally | Verified design limit | Per-chunk ACL list stored in index | CLAIM-07 |
| KG feature appears abandoned/de-emphasised | Maturity | Not core to retrieval | CLAIM-09 |
| No graph store, no typed entities beyond (former) KG tables, no temporal/claim model | Verified absent | Chunk-centric search architecture | CLAIM-09 |
| Infrastructure churn: Vespa -> OpenSearch, MinIO -> SeaweedFS in a year | Operational | Fast release cadence | CLAIM-05, -06 |
| Air-gap not documented; model downloads at first start | Hypothesis | Hugging Face cache volumes | CLAIM-10 |
| Approx. 10 containers for Standard mode | Operational | Separate workers, model servers, store | CLAIM-06 |

Algorithmic dead-ends: chunk-only retrieval cannot answer multi-hop impact questions (J1/J2) — reasoned inference. User friction: local-LLM tuning.

## 10. Deployment, licensing, redistribution, and operational viability

Self-hosted via Docker Compose, Kubernetes, Helm/Terraform [CLAIM-01]. Licence class: **mixed (MIT + proprietary EE directories)**. **Legal-review trigger**: Enterprise License text in `ee` directories, EE-gated permission sync, white-label listed as an Enterprise-plan feature, PR indication that EE can be toggled on/off in self-hosted deployments [CLAIM-11]. Redistribution of the MIT part inside a white-labelled commercial product looks permitted by the MIT text, but trademark ("Onyx") and EE code exclusion require review — **no legal conclusion given**. Air-gap: partial (images and models must be pre-seeded; nothing documented). Egress policy: customer chooses LLM provider; no DLP gate comparable to EOIP `egress/gateway.py` (BL-45) found.

## 11. Competitive delta against the EOIP verified baseline

| Area | Onyx | EOIP | Delta |
|---|---|---|---|
| ACL in retrieval | Implemented (14 connectors, EE) | BL-18 Absent | Onyx ahead — closes via STR-01 |
| Connectors | 56 pull-to-index | 30+ emit SourceEvents (BL-23), graph-governed | Onyx ahead on breadth, behind on governance (connectors write index directly) |
| Vector/keyword | OpenSearch hybrid, persistent | BL-13..15: in-process, not persistent | Onyx ahead |
| Graph/ontology/temporal | Absent | BL-37 Implemented, BL-28 Implemented | EOIP ahead |
| Egress control | Provider choice only | BL-45 Implemented | EOIP ahead |
| Tenancy | Not verified | BL-20 Partial | Unknown |
| Deployment weight | ~10 containers | ~8 services plus backends | Parity |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

**STR-onyx-01** | Onyx | Per-chunk ACL principal strings in the index and filter at query time | CLAIM-07, -08 | Source-ACL enforcement (J5) | **match** | Store `acl_principals` (tenant-prefixed) on every index document and fact; retrieval always injects caller principals; unknown ACL => private (`empty()` semantics) | 1,000 docs with mixed ACLs: 0 forbidden results across search, GraphRAG, summaries, cache.

**STR-onyx-02** | Onyx | Shadow/enforce rollout for access filters | CLAIM-08 | Safe migration of BL-18 | **match** | Feature flag logs would-be denials for N days before enforce | Shadow log shows denial set equal to oracle ACL.

**STR-onyx-03** | Onyx | Group-based sync with nested group expansion and checkpointed resumption | CLAIM-08 | Large directory sources | **match** | Resolver for nested groups with checkpoints in `source_checkpoint` | Resume after kill with no duplicate grants.

**INV-onyx-01 — Permission sync gated behind an enterprise licence (open-core).** Target Onyx v5.0.0, enterprise search. Root cause: licensing (proven). Alternative: ship ACL enforcement in the base product, differentiate on governance; worse if EOIP lacks maintenance capacity for 14-connector sync. Options: (1) quick: embed Onyx CE as unstructured-search sidecar, no ACL sync — rejected, violates "permissions survive everything"; (2) native: ACL strings on EOIP index/graph facts, connector ACL resolvers for Jira/Confluence/GitLab first; (3) long-term: ReBAC with provenance of grants. Selected (2). Sketch: `SourceEvent.permission -> principal_set -> index.acl_principals; query(caller) => filter(principal_set ∩ caller.principals)`. POC: Jira DC + Confluence DC ACL parity vs source for 200 pairs; cost: CPU only. Failure cases: stale ACL window (default refresh 30 min in Onyx; EOIP must bound), cap on entries, group explosion. Defensibility: graph-level fact ACL + evidence. **Decision: ADOPT.**

**INV-onyx-02 — Chunk-only index without graph, claims or temporal state.** Root cause: data model (proven by absence). Alternative: graph-first with evidence spans; worse for pure FAQ search where graph adds cost. Options: (1) integrate Onyx for plain document Q&A and EOIP for relational questions; (2) hybrid retrieval with graph expansion; (3) bitemporal evidence graph. Selected (2). POC: 50 impact questions (reference customer questions 1-5); success = graph-first beats BM25+dense+rerank baseline by a pre-registered margin (Master Prompt §5 trap 3). **Decision: EXPERIMENT.**

**INV-onyx-03 — Onyx KG deprecated/de-emphasised.** Evidence thin (variables ignored in 5.0; no docs). Treat as signal that LLM-extracted KG at index time did not justify its cost for this vendor (hypothesis). **Decision: DEFER** any copying; record as counter-evidence to "GraphRAG automatically superior".

## 13. Per-capability decisions

| Capability | Decision |
|---|---|
| CAP-46 ACL in retrieval | BUILD (pattern from Onyx) |
| CAP-26 connector breadth | INTEGRATE selectively / BUILD per EOIP SourceEvent contract |
| CAP-53/54/55 persistent hybrid index | EXPERIMENT: OpenSearch as optional module (check Apache-2.0 for OpenSearch: not verified here) |
| CAP-61 local model serving | REUSE Ollama (already in compose) |
| Onyx as a sidecar | EXPERIMENT only as comparison harness, never as a mandatory dependency |
| Onyx EE code | REJECT (proprietary, gated) |
| CAP-56 KG from LLM extraction | DEFER |

## 14. Concrete tests, proof-of-concept, and acceptance conditions

1. Deploy Onyx CE v5.0.0 with Ollama on one node; record RAM/disk/containers; run egress-blocked start to test model pre-seeding. 2. ACL parity harness: same 200 user/doc pairs against Onyx EE trial (if licensed) and EOIP prototype. 3. Retrieval baseline: use Onyx hybrid as the strong non-graph baseline for the EOIP GraphRAG benchmark. 4. Shadow-mode rollout drill on EOIP retrieval.

## 15. Risks, trade-offs, and open research questions

Risks: EE licence text unread; pricing-page/doc contradictions; cadence implies breaking upgrades; unverified tenancy; trademark. Open: exact filter implementation; behaviour at the 5,000-entry cap; whether CE disables permission sync entirely or lets private-per-connector only; KG fate; air-gapped model bundle.

---

## Appendix A — Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | MIT + EE licence; active; rename from Danswer |
| D2 | 2 | Permissioned RAG |
| D3 | 4, 5 | Services and flows |
| D4 | 5 | OpenSearch, Postgres, object store |
| D5 | 5 | KG type definitions only |
| D6 | 5 | Hybrid search; no graph query language; detail unread |
| D7 | — | N/A: no reasoning |
| D8 | 5, 7 | Eventually consistent; scale unverified |
| D9 | 3, 5 | Pull connectors, refresh/prune, checkpoint |
| D10 | 5 | ACL principals; no ER |
| D11 | 5 | No temporal model |
| D12 | — | N/A |
| D13 | 2, 3, 5 | RAG, MCP, agents; citations not verified |
| D14 | — | N/A: no graph NL query |
| D15 | 3 | Roles on cc-pairs |
| D16 | 3 | Chat UI, Slack bot, voice |
| D17 | 3 | API, MCP, hooks (EE) |
| D18 | 5, 9 | ACL, EE gating |
| D19 | 10 | Not verified |
| D20 | 7 | No benchmarks |
| D21 | 1, 9, 10 | Open-core |
| D22 | 9 | Export on Enterprise plan |
| D23 | — | N/A |
| D24 | App. C | Official docs and source files; one GitHub page truncated |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-46 | enterprise-only (sync); native (index ACL) | 03, 07, 08 | BL-18 Absent | BUILD | P0 |
| CAP-26 | native (56) | 03 | BL-23 Implemented | BUILD/INTEGRATE | P1 |
| CAP-53/54/55 | native | 05, 06 | BL-13/14/15 | EXPERIMENT | P2 |
| CAP-61 | native (Ollama etc.) | 10 | Implemented | REUSE | P2 |
| CAP-59 | native (MCP server) | 01, 06 | BL-47 | REFERENCE | P3 |
| CAP-56 | partial/abandoned | 09 | BL-16 | DEFER | P3 |
| CAP-52 | enterprise-only (white-label) | 04 | BL-21 | REJECT dependence | P3 |
| CAP-50 | partial | 10 | — | BUILD | P1 |
| CAP-77 | open-core | 02, 04 | BL-22 | REFERENCE | P3 |

## Appendix C — Evidence records (access date 2026-10-26)

| CLAIM-ID | Product / version / date | Exact claim | Classification | Source + URL | Pub / access | Confidence | Contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-onyx-01 | Onyx main | Community Edition MIT; Enterprise Edition adds features; ~33.0k stars; Docker, Kubernetes, Helm/Terraform; Standard vs Lite (<1 GB, no indexing); "50+ applications"; agents, deep research, web search, code sandbox, voice, MCP | Officially documented | GitHub README, https://github.com/onyx-dot-app/onyx | undated / 2026-10-26 | 0.85 | Connector count: 56 in docs |
| CLAIM-onyx-02 | Onyx LICENSE | Content under `ee` directories licensed under the Onyx Enterprise License (copies at backend/ee, web/src/app/ee, web/src/ee); other content MIT Expat; bundled third-party code keeps original licence | Observed in source code | https://raw.githubusercontent.com/onyx-dot-app/onyx/main/LICENSE | undated / 2026-10-26 | 0.85 | EE licence terms not read |
| CLAIM-onyx-03 | Onyx docs connectors | 56 official connectors in 8 groups; Auto Sync Permissions "an Enterprise Edition feature" for 14 named connectors; refresh default 30 min, prune default 30 days; private/public/synced visibility | Officially documented | https://docs.onyx.app/admins/connectors/overview | undated / 2026-10-26 | 0.8 | Pricing page says "40+ app connectors" |
| CLAIM-onyx-04 | Onyx pricing | Business $20/user/month annual (RBAC, permission inheritance, 40+ connectors, MCP/OpenAPI actions); Enterprise custom: OIDC/SAML SSO, on-premise, white-labelling, hook extensions, data exports | Vendor claim | https://onyx.app/pricing | undated / 2026-10-26 | 0.7 | CE is MIT and self-hostable; docs place permission sync in EE |
| CLAIM-onyx-05 | Onyx v5.0.0 changelog | v5.0.0 dated 2026-10-23; OpenSearch only document index since v4.0.0; Vespa settings now ignored; KG pipeline variables now ignored; release cadence v4.4.0 2026-07-21 to v4.9.0 2026-10-07 | Officially documented | https://docs.onyx.app/changelog | 2026-10-23 / 2026-10-26 | 0.8 | GitHub shows "24 Oct" (time zone) |
| CLAIM-onyx-06 | docker-compose main | Services and images as listed (OpenSearch 3.6.0, Postgres 15.2-alpine, Redis 7.4-alpine, SeaweedFS 4.47, MinIO legacy, code-interpreter 0.4.9, two model servers) | Observed in source code | https://raw.githubusercontent.com/onyx-dot-app/onyx/main/deployment/docker_compose/docker-compose.yml | undated / 2026-10-26 | 0.85 | — |
| CLAIM-onyx-07 | `access/models.py` main | `ExternalAccess`, `DocumentAccess`, `MAX_NUM_ENTRIES = 5000` unenforced, `to_acl()` prefixed strings, `empty()` private fallback | Observed in source code | https://raw.githubusercontent.com/onyx-dot-app/onyx/main/backend/onyx/access/models.py | undated / 2026-10-26 | 0.8 (summarised by fetch tool) | Not pinned to tag |
| CLAIM-onyx-08 | Onyx releases | v5.0.0: query-time cc-pair access filter behind shadow/enforce flag, Editor/Operator roles, credential families; beta.3: Google Drive permission sync checkpoint resume, Jira permission sampling; v4.9.4: Entra nested group listing | Officially documented | https://github.com/onyx-dot-app/onyx/releases | 2026-10 / 2026-10-26 | 0.7 | Release notes truncated |
| CLAIM-onyx-09 | Onyx KG | `backend/onyx/kg` contains models.py, setup/, resets/; model classes as in §5; product page markets "LLM-based knowledge graph approaches"; docs KG page 404; 5.0 ignores KG variables | Observed in source code | https://raw.githubusercontent.com/onyx-dot-app/onyx/main/backend/onyx/kg/models.py ; https://onyx.app/product/search ; CLAIM-05 | undated / 2026-10-26 | 0.6 | Marketing implies active KG |
| CLAIM-onyx-10 | Onyx LLM docs | Self-hosted models via Ollama, GPT4All or OpenAI-compatible API; weaker local models need longer timeouts and disabling rephrasing/chunk filtering; no air-gap guide found | Officially documented (search summary) | https://docs.onyx.app/gen_ai_configs/overview ; https://docs.onyx.app/admins/ai_models/ollama | undated / 2026-10-26 | 0.6 | — |
| CLAIM-onyx-11 | Onyx v5.0.0 PR titles | "feat(ee): downgrade a self-hosted deployment to Community" (#15625); "drop the two EE env vars" (#15645) | Observed in source code (release notes) | https://github.com/onyx-dot-app/onyx/releases/tag/v5.0.0 | 2026-10-24 / 2026-10-26 | 0.6 | Semantics of EE toggle unverified |

## Appendix D — Assumptions

A1 Access date 2026-10-26. A2 Source files read from `main`, not the v5.0.0 tag. A3 Fetch tool summarised files; line numbers not available. A4 Danswer rename taken from repository redirect evidence in search results. A5 Tenancy, SSO and EE licence text left unverified.
