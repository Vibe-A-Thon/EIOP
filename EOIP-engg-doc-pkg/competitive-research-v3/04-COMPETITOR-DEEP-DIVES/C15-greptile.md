# C15 — Greptile

| Field | Value |
|---|---|
| Registry ID | T-C15-greptile |
| Tier | B — commercial AI pull-request review over a codebase index |
| Versions examined | Hosted SaaS (unversioned); self-hosted docs as of 2026-10-26; no public version number found |
| Verified on | 2026-10-26 (brief date 2026-10-18) |
| Worker | V28 (W27 scope) |

## 1. Identity, current status, tier, and sources

| Item | Finding | Claim |
|---|---|---|
| Identity | Greptile: AI agents that review (and, via "TREX", test) pull requests "with full context of the codebase"; GitHub and GitLab | [CLAIM-greptile-01] |
| Status | Commercial, active (pricing and docs current); version and release cadence: NOT PUBLICLY VERIFIED | [CLAIM-greptile-01] |
| Licence | Proprietary (no OSS licence found for the product; docs mention a related `akupara` repo, not examined) | [CLAIM-greptile-02] |
| Graph claim | Marketing says it "constructs a graph index of your codebase" (files, functions, dependencies); docs describe the data stores as PostgreSQL+pgvector with chunker and summarizer workers, no graph database named | [CLAIM-greptile-01][CLAIM-greptile-03] |

## 2. Primary problem, workloads, workflows

Reduce review load: on each PR, parallel agents assess impact beyond the diff, learn from past comments, apply plain-English team rules. EOIP relevance (J1): impact-aware review comments tied to a Jira story and commit.

## 3. Feature inventory

| Feature | Status | Claim |
|---|---|---|
| PR review GitHub/GitLab | present | [CLAIM-greptile-01] |
| Plain-English custom rules; learning from comments | present (vendor) | [CLAIM-greptile-01] |
| Test-writing agent (TREX) | present (vendor) | [CLAIM-greptile-01] |
| MCP, Claude Code plugin, API (via support) | present | [CLAIM-greptile-01] |
| Self-host (Docker Compose to 100 devs; Kubernetes 100+); own LLM providers | present | [CLAIM-greptile-01][CLAIM-greptile-03] |
| Air-gapped deployment | claimed by vendor; CLI update and diagram renderer need registry mirrors | [CLAIM-greptile-01][CLAIM-greptile-04] |
| SSO (SAML via saml-jackson), audit logs | present (vendor) | [CLAIM-greptile-01][CLAIM-greptile-03] |
| Public graph/query API | absent in evidence | |

## 4. Architecture diagram

```
 GitHub/GitLab webhook -> greptile-webhook -> Hatchet (+RabbitMQ) -> workers: chunker, summarizer, reviews, jobs
                                   workers -> greptile-llmproxy -> OpenAI/Anthropic/Bedrock/Azure/Vertex
 state: greptile-postgres (+pgvector: metadata, summaries, embeddings, review history, accounts)
 api/web/auth/saml-jackson front the same DB
```
(from system-architecture docs) [CLAIM-greptile-03]

## 5. Under-the-hood reconstruction

- Data model: repositories chunked, summarised by an LLM, embedded; stored in Postgres/pgvector; embeddings are "the largest component" [CLAIM-greptile-03].
- Query/review pipeline: webhook enqueue, workflow dispatch, retrieval over chunks/summaries (graph traversal over "files, functions, dependencies" is a marketing statement; mechanism NOT PUBLICLY VERIFIED), LLM review, comment posted [CLAIM-greptile-03].
- Concurrency: Hatchet workflow engine; summarizer and reviews are LLM-bound so scale with LLM throughput [CLAIM-greptile-03].
- Reasoning, versioning, caching, source ACL handling: NOT PUBLICLY VERIFIED. Security: egress to LLM, SCM and registry listed; payload contents sent to LLMs not specified [CLAIM-greptile-03].

## 6. Requirements inferred

An LLM gateway, embedding model, Postgres+pgvector, workflow engine, SCM webhooks.

## 7. Performance and resource model

Sizing guidance only (Compose for up to 100 developers) [CLAIM-greptile-03]. No review-quality or latency benchmark independent of vendor retrieved; vendor claims unverified. LLM cost is credit-priced: starter 50 credits/month free; $1 per credit; review base 1 / plus 3 / apex 10 credits (pricing page, vendor) [CLAIM-greptile-01].

## 8. Strengths

| Strength | Match or exceed |
|---|---|
| Self-hostable with customer LLM providers | EOIP default-local LLM (BL-45 gateway) already stricter |
| Review workflow integrated with agents via MCP | exceed with governed evidence spans (BL-41) |
| Learning team conventions from comment history | EXPERIMENT: store as ontology rules, approved by human |

## 9. Limitations

| Class | Finding | Claim |
|---|---|---|
| Licensing | Proprietary, per-credit; no OEM terms found | [CLAIM-greptile-01] |
| Operational | Needs external LLM provider list; local model support not stated | [CLAIM-greptile-03] |
| Verification | "Graph index" not described; accuracy and SOC 2 claims not independently verifiable | [CLAIM-greptile-01] |
| Scope | PR-review only; no general graph, ACLs or tenancy semantics described | [CLAIM-greptile-03] |

## 10. Deployment, licensing, redistribution

Self-hosted Compose/Kubernetes; air-gap claimed (vendor). Proprietary; cannot be white-labelled or embedded without a commercial agreement (none published). Legal-review trigger: yes (proprietary, per-credit, OEM unknown).

## 11. Competitive delta against EOIP baseline

BL-42 is a graph builder, not a reviewer. Greptile shows a product shape: PR diff to impact set to comment. EOIP has diff hunks (BL-42), lineage (BL-41), MCP (BL-47) to produce the same with evidence; BL-18 ACL gap applies to any such feature. Related: C15-sourcegraph.md for code search platform; C15-augment-context.md for hosted context retrieval.

## 12. Cards

`STR-greptile-01 | Greptile | PR review with codebase-wide impact | CLAIM-01 | J1 change impact surfaced where developers work | match | EOIP impact query on diff hunks, results as PROPOSED comments with spans | 20 historical PRs: impact set precision/recall vs human labels`

INV-greptile-01: target hosted/self-hosted current; workload regulated enterprise. Limitation: LLM provider dependency and unspecified payloads (documented gap, CLAIM-03). Root cause: coupling (hypothesis). Alternative: local-model review through EOIP egress gateway; worse when frontier quality needed. Options: (a) integrate Greptile self-hosted behind egress policy, (b) native reviewer over graph impact queries, (c) differentiated: evidence-bound review with ACL re-check. Selected (b) experiment. POC: as above with a local model; metric: comment acceptance vs baseline, zero off-prem bytes. Decision: EXPERIMENT. Seed hypotheses in §10.5 do not target Greptile.

## 13. Decisions

| Capability | Decision |
|---|---|
| CAP-69 change-impact digital thread | BUILD |
| AI PR review | EXPERIMENT |
| Greptile as component | REJECT (proprietary, OEM unknown) |

## 14. Tests and acceptance

Network-capture of a fully local review path; ACL test: reviewer never cites files the PR author cannot read.

## 15. Risks and open questions

What content reaches LLM providers; real mechanism of the graph; SOC 2 scope; pricing changes.

## Appendix A — Dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Commercial, proprietary |
| D2 | 2 | PR review |
| D3 | 4 | Compose/K8s services |
| D4 | 5 | pgvector |
| D5 | N/A | Not described |
| D6 | 5 | Not public |
| D7 | N/A | None |
| D8 | 5,7 | Hatchet workers |
| D9 | 5 | Webhooks |
| D10 | N/A | None |
| D11 | N/A | Review history only |
| D12 | N/A | None |
| D13 | 3 | MCP, API |
| D14 | N/A | Absent |
| D15 | 3 | Rules |
| D16 | 3 | PR comments |
| D17 | 3 | API on request |
| D18 | 3,5 | SSO; egress |
| D19 | N/A | Not described |
| D20 | 7 | Pricing only |
| D21 | 7,10 | Credits |
| D22 | N/A | None |
| D23 | N/A | Not checked |
| D24 | 15 | Vendor sources only |

## Appendix B — Capability mapping

| CAP | Technology | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-69 | partial | 01 | BL-42 Partial | BUILD | P1 |
| CAP-55 | partial | 03 | BL-15 | DEFER | P3 |
| CAP-50 | partial | 04 | BL-45 | DEFER | P3 |
| CAP-60 | unknown | 01 | BL-16 | EXPERIMENT | P2 |

## Appendix C — Evidence records

| CLAIM | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| 01 | Greptile site 2026-10 | product, graph index claim, self-host/air-gap claim, platforms, pricing | Third-party report (vendor marketing) | https://www.greptile.com | n/a / 2026-10-26 | 0.6 (promotional) | none |
| 02 | n/a | no OSS licence located | Unverified | not found | 2026-10-26 | 0.4 | docs reference akupara repo |
| 03 | docs | services, stores, indexing flow, egress, sizing | Officially documented | https://www.greptile.com/docs/system-architecture.md | 2026-10-26 | 0.8 | older page says Helm only |
| 04 | docs | air-gap caveats npm update check, renderer | Officially documented | https://www.greptile.com/docs/self-hosting/cli-reviews.md (via search summary) | 2026-10-26 | 0.6 | none |

## Appendix D — Assumptions

Claim 04 taken from a search summary, page not opened; treated as 0.6.
