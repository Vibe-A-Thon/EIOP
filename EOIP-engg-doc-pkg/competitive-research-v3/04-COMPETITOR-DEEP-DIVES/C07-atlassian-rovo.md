# C07 — Atlassian Rovo and the Teamwork Graph

| Field | Value |
|---|---|
| Registry ID | T-C07-atlassian-rovo |
| Tier | A — work-graph competitor over Jira/Confluence, the buyer's default IT-engineering source pair |
| Versions examined | Rovo (SaaS, rolling; no version numbers). Rovo MCP Server v2 (`/v2/mcp`; v1 retiring 2027-03-01). Team '26 announcements (2026-05-06). Forge `graph:connector` module / Teamwork Graph connector SDK (docs page updated 2025-11-24). Data Center EOL schedule (official page) |
| Verified on | 2026-10-26 (brief states 2026-10-18; the actual session date is used as access date) |
| Worker | V04 (replaces placeholder file) |

Cross-references (not repeated here): `C07-glean-enterprise.md` (same SaaS/work-graph class; Customer Hosted model), `C07-microsoft-graph-copilot-fabric.md`, `C07-palantir-foundry.md`, `C07-servicenow-kg.md`.

## 1. Identity, current status, tier, and sources

Rovo is Atlassian Corporation's proprietary AI layer (search, chat, agents, Studio) over the **Teamwork Graph**, Atlassian's cross-product graph of work objects (people, teams, goals, work items, pages, files, signals) plus third-party objects ingested through connectors. Status: active, shipping; owned by Atlassian; closed source; Cloud-only for full functionality. Rovo is bundled and auto-activated on Standard/Premium/Enterprise Cloud plans, with a monthly per-user credit pool (25/70/150 for Jira or Confluence; 250/700/1,500 for Teamwork or Service Collection) and extra usage at $0.01 per credit [CLAIM-atlassian-rovo-01]. Data Center customers get only *connectors that push DC content to Rovo on Cloud*; the full AI feature set needs a Cloud plan [CLAIM-atlassian-rovo-01, -04]. Atlassian Data Center reaches end of life on 2029-03-28 (read-only), new DC sales to new customers ended 2026-03-30 [CLAIM-atlassian-rovo-03].

Shipped vs announced (Master Prompt §5 trap): see table in §3 and CLAIM-05. Key sources: Atlassian licensing page, Rovo MCP support docs, Forge module reference, Team '26 coverage (SiliconANGLE) and Atlassian's own Team '26 post, Atlassian DC EOL page. Most internals are **NOT PUBLICLY VERIFIED**; the permission-check mechanism at query time is not documented in anything retrieved.

## 2. Primary problem, target workloads, concrete example workflows

Problem: give every employee and every AI agent context drawn from Atlassian work data (and connected SaaS) with source permissions respected. Workloads: enterprise search and chat over Jira/Confluence/JSM/Bitbucket/Loom plus connected SaaS; no-code and Forge agents (assignable to Jira work items); automations; external agents reading/writing the graph through MCP and a CLI.

| Workflow | How Rovo does it | Evidence |
|---|---|---|
| "What changed on service X and who owns it?" | Rovo Chat over Teamwork Graph objects (issues, pages, teams) | CLAIM-05, -09 |
| Coding agent (Claude Code/Cursor) queries work context | Teamwork Graph CLI (300+ commands) or Rovo MCP tools, both **open beta** | CLAIM-05, -07 |
| Pull Salesforce/Notion/Slack content into search | Synced / Synced Lite / Direct / Smart Link connector types | CLAIM-09 |
| Ingest a proprietary system | Forge Teamwork Graph connector with declared capabilities | CLAIM-08 |
| Include on-prem Jira/Confluence | DC connectors index DC content into the **Cloud** Rovo | CLAIM-04 |

## 3. Feature inventory

| Feature | Status | Evidence |
|---|---|---|
| Rovo Search / Chat / Agents (UI, Jira, Slack) | Present (Cloud only) | CLAIM-01, -05 |
| Rovo Studio no-code agent builder with roles, approvals, versioning, audit | Present (GA per press) | CLAIM-05 |
| Agents assignable to Jira work items | Present (GA per press) | CLAIM-05 |
| Teamwork Graph connectors (Forge) | GA per press; Atlassian docs page does not state stage (sidebar marks only Global module EAP) | CLAIM-05, -08 |
| Teamwork Graph tools via Rovo MCP, Teamwork Graph CLI | **Open beta** (press) / stage not stated (Atlassian post) | CLAIM-05 |
| Rovo MCP Server v2 (Jira, JSM, Confluence, Bitbucket, Projects, Goals, Loom), OAuth 2.1, optional API tokens | Present, cloud-hosted; GA/beta not stated | CLAIM-07 |
| Max reasoning mode in Rovo Chat | Early access ("coming soon") | CLAIM-05 |
| Incident Command Center, org-wide agent inventory, build-vs-run permission split, AI usage dashboards and audit logs | Announced; availability not stated | CLAIM-05 |
| Data residency for Rovo | Limited availability (2025, third-party) | CLAIM-09 |
| Data Center connectors (Confluence DC, Jira DC) | Present; push-to-cloud only | CLAIM-04 |
| Rovo on Data Center / air-gap / self-hosted LLM | **Absent** (no evidence of any) | CLAIM-01, -03, -07 |
| Graph query language, bulk export of graph, ontology editing | NOT PUBLICLY VERIFIED | — |
| Source-ACL honouring | Claimed ("honored throughout"); mechanism unknown | CLAIM-09 |

## 4. Architecture diagram (reconstructed from public statements; hypothesis where marked)

```
 Atlassian Cloud products (Jira, Confluence, JSM, Bitbucket, Loom, Goals, Teams)
        |  first-party signals                       3rd-party SaaS / Data Center
        v                                            |  connectors: Synced | Synced Lite | Direct | Smart Link
 +-----------------------------------------------+   |  Forge graph:connector (objectTypes, replicatesPermissions,
 |  Teamwork Graph (storage tech: NOT VERIFIED)  |<--+  syncFidelity append/upsert/mirror, incremental sync)
 |  objects + relationships ( >150e9 connections |
 |  claimed by vendor)                           |   DC: Jira DC / Confluence DC -> pushed to Cloud index
 +-----------------------+-----------------------+
                         | hybrid retrieval: BM25 + kNN on AWS OpenSearch (third-party report)
                         v
   Rovo orchestration -> multi-vendor LLMs (OpenAI, Google, Anthropic, Llama; page-dependent) [Atlassian-hosted]
        |                    |                         |
   Rovo Search/Chat    Rovo Studio / Forge agents   Rovo MCP Server v2 + Teamwork Graph CLI (external agents)
   Control plane: Atlassian admin (credits pool, agent policies, residency); no customer-hosted plane
```

## 5. Under-the-hood reconstruction

Only what public evidence supports; everything else is labelled.

| Layer | What is verified | Hypothesis / unknown |
|---|---|---|
| Data model | Typed *objects* with *relationships*; connector SDK exposes object CRUD, relationship create/delete, user and group operations, recurring root task fanning into child tasks with `taskRunner` callback [CLAIM-08]. Connector manifest declares `objectTypes` | Object type catalogue ("Connector object types") not read; internal graph store NOT PUBLICLY VERIFIED |
| Ingestion | Connector classes: Synced (index content+metadata), Synced Lite, Direct (live external search API, no index), Smart Link (URL preview, signals) [CLAIM-09]. Forge `syncFidelity`: append / upsert / mirror (mirror implies delete propagation); `supportsIncrementalSync` flag [CLAIM-08] | Delete/tombstone semantics beyond "mirror" unknown |
| Index | Hybrid BM25 + embedding kNN on OpenSearch; reranker retrained Sept 2025 with pairwise loss [CLAIM-09, third-party] | Chunking, embedding model, graph-expansion step unknown |
| Permissions | Connector declares `replicatesPermissions`; if false, "all ingested data is visible to every user in the Atlassian workspace"; without per-user OAuth (`auth.provider`) Atlassian "can't reliably link external accounts to Atlassian users" so scope falls back to workspace [CLAIM-08]. Vendor says source permissions are "honored throughout" [CLAIM-09] | Query-time vs index-time ACL filtering NOT PUBLICLY VERIFIED. A plausible design is per-document principal sets filtered at retrieval (as in Onyx, see C07-onyx §5) — hypothesis |
| Agents | Studio agents with roles/approvals/versioning; Jira agents audited; Forge agents with custom actions [CLAIM-05, -10] | Tool-call authorisation model unknown |
| External access | MCP v2 exposes tools incl. Teamwork Graph tools; Teamwork Graph tools reportedly need a separate `read_teamwork_graph` scope that admins must grant; a developer-community report says calls still failed after the grant [CLAIM-07, -11] | Rate limits not documented; credits consumed per call by data volume and reasoning depth |
| Versioning/temporal | NOT PUBLICLY VERIFIED | — |
| Tenancy | Org/site-scoped; "Units" (announced Team '25 Europe) described as separate policy/data-residency scopes with separate graph (search snippet only; UNVERIFIED) | — |

## 6. Functional and non-functional requirements inferred

| ID | Requirement inferred | Basis |
|---|---|---|
| FR-1 | Connectors must *declare* capability flags (permission replication, sync fidelity, incremental) and admins see "not declared" | CLAIM-08 |
| FR-2 | Three ingestion modes per source: materialise, federate live, link-unfurl | CLAIM-09 |
| FR-3 | Graph exposed to external agents via MCP and CLI with a distinct read scope | CLAIM-07, -11 |
| FR-4 | Agents have build/run permission separation, inventory and audit (announced) | CLAIM-05 |
| FR-5 | Content classes excluded from connectors: email, calendar, meeting recordings, HRIS, regulated finance/health, GDPR special categories | CLAIM-08 |
| NFR-1 | Metered consumption (credit pool, overage) | CLAIM-01 |
| NFR-2 | Cloud-region residency pinning | CLAIM-09 |

## 7. Performance and resource model

No independent benchmark found. Vendor claims, quoted only: ">150 billion connections", "44% more accurate" and "48% fewer tokens" from Atlassian internal benchmarks with no workload, dataset or hardware disclosed [CLAIM-06] — **not comparable** with any EOIP figure. Customer-side resource model: none (SaaS); cost is credits: Chat/Agents 10 credits per request and Deep Research 100 credits per request per third-party blogs (not confirmed on the Atlassian page) with search free [CLAIM-01 note]. Failure modes: credit exhaustion pauses credit-consuming features when extra usage is off [CLAIM-01]; scope errors on Teamwork Graph MCP tools [CLAIM-11]. Latency and freshness: NOT PUBLICLY VERIFIED.

## 8. Strengths and use-case-specific advantages

| Strength | Use case | How to match or exceed |
|---|---|---|
| First-party Jira/Confluence/Bitbucket graph with no connector latency or auth plumbing | Digital-thread J1/J2 for Atlassian shops | EOIP ingests Jira/Confluence via connectors (BL-23); exceed by being able to join them with GitLab, ServiceNow, Datadog |
| Declarative connector capability contract | Honest permission-fidelity labelling per source | Add capability flags to EOIP connector manifests (STR-01) |
| Three-mode ingestion (synced / direct / smart link) | Fresh data without full replication | EOIP `federation/planner.py` (BL-51) partial; adopt mode taxonomy (STR-02) |
| Graph exposed through MCP + CLI | Coding-agent context | EOIP MCP has 18 read tools (BL-47); exceed with ACL-filtered, evidence-cited results (STR-03) |
| Agent governance (inventory, build/run split, audit) | Enterprise agent rollout | BL-48 partial; adopt inventory and role split (STR-04) |
| Bundled pricing, 90% of enterprise cloud customers reported using it (vendor) | Zero-friction adoption | Not matchable; counter with air-gap and ownership |

## 9. Limitations with root causes

| Limitation | Class | Root cause | Evidence |
|---|---|---|---|
| No on-prem or air-gap path; DC gets only push-to-cloud connectors; DC ends 2029-03-28 | Verified trade-off | Cloud-centric architecture; Atlassian "cloud-first" strategy | CLAIM-01, -03 |
| Third-party LLM providers process prompts (providers vary by transparency page: OpenAI/Google/Llama on one, Anthropic on others) | Verified (page-dependent) | Multi-vendor hosted orchestration; no customer model control found | CLAIM-10 |
| Connector may expose data to the whole workspace when `replicatesPermissions=false` | Verified | Permission replication is the connector author's job | CLAIM-08 |
| Excluded data classes (email, HRIS, regulated data) cannot go through Forge connectors | Verified policy | Terms-of-use restriction | CLAIM-08 |
| Metered credits and default-on overage | Commercial | Consumption pricing | CLAIM-01 |
| MCP Teamwork Graph scope errors after admin grant | User-reported | Unknown (scope propagation) | CLAIM-11 |
| Graph not user-queryable by standard language; export unknown | Hypothesis | Proprietary store | — |
| Many headline features announced, not dated | Maturity | Team '26 announcements | CLAIM-05 |

Algorithmic dead-ends: none evidenced. Operational overhead: none for customer (SaaS), moved to cost and dependence. User/developer friction: Forge-only connector authoring, EAP/GA ambiguity, scope configuration.

## 10. Deployment, licensing, redistribution, and operational viability

Proprietary SaaS; no redistribution, OEM, white-label or embedding right found. Not a candidate dependency. Air-gap: **no**. External LLM egress cannot be disabled by the customer on the evidence found. Legal-review trigger: proprietary terms; Forge/Marketplace data restrictions; consumption pricing. Viability under EOIP constraints: **REJECT as component; use only as a source system (Jira/Confluence) and as an MCP peer**.

## 11. Competitive delta against the EOIP verified baseline

| Area | Rovo | EOIP baseline | Delta |
|---|---|---|---|
| Source-ACL in retrieval | Claimed, mechanism unknown, connector-declared fidelity | BL-17 captured; **BL-18 Absent** | Rovo ahead on claim; EOIP's gap is P0 regardless |
| Tenancy | Org-scoped SaaS, Units (unverified) | BL-20 Partial, adapters not tenant-aware | Parity unknown |
| Deployment | Cloud only | Self-hosted, Compose, Helm (01-SYSTEM-BASELINE §4 Deployment row) | EOIP ahead on air-gap |
| Connector capability declaration | Explicit flags | `PermissionMetadata` + `acl_hash` (BL-17), no fidelity flags | Adopt |
| MCP | Read+write on cloud graph | BL-47 read-only by design (ADR-007) | EOIP safer, less capable |
| Agents governance | Studio + audit (GA per press) | BL-48 Partial | Rovo ahead |
| Temporal/bitemporal | Unknown | BL-37 Implemented | EOIP ahead on evidence |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

**STR-atlassian-rovo-01** | Rovo | Connector capability declaration (`replicatesPermissions`, `syncFidelity`, `supportsIncrementalSync`) | CLAIM-08 | Honest, admin-visible fidelity per source | **match** | Add `capabilities` block to each connector manifest and a deny-by-default rule when `replicates_permissions=false` | A connector without declared ACL replication cannot publish to a tenant-wide index; test asserts denial.

**STR-atlassian-rovo-02** | Rovo | Per-source ingestion mode: synced / direct / link | CLAIM-09 | Freshness without replicating sensitive stores | **match** | Map to `federation/planner.py` modes (materialise, federate, link) with mapping versioning | One source per mode in a POC; stale-read bound measured.

**STR-atlassian-rovo-03** | Rovo | Graph served to external agents over MCP + CLI with a dedicated scope | CLAIM-07, -11 | Coding-agent context (J1) | **exceed** | Keep read-only; add `graph.read` scope bound to caller principal; return evidence refs and abstain on ACL denial | Agent as user U never sees an entity U cannot read (J5).

**STR-atlassian-rovo-04** | Rovo | Agent inventory plus build/run permission split | CLAIM-05 (announced only) | Agent sprawl control | **match** (design only until shipped) | Registry of agents with owner, tools, last-run; separate `agent.author` and `agent.run` roles | Inventory lists 100% of registered agents; run without run role denied.

**INV-atlassian-rovo-01 — Seed hypothesis §10.5 (Palantir/Glean/Rovo: SaaS, lock-in, limited on-prem/air-gap): PARTIALLY VALIDATED.** Validated: SaaS-only for full function, DC only pushes to cloud, DC EOL 2029 [CLAIM-01, -03]; lock-in *mechanism* unproven (graph export not found: hypothesis). **Rejected: "heavyweight"** — Rovo is bundled and auto-activated, which is the opposite of heavyweight for the buyer. Target: Rovo, 2026-10, enterprise search/agents. Root cause (proven for deployment; hypothesis for lock-in): deployment/licensing. Mitigation: air-gapped, local-model deployment with open exportable evidence formats; worse when customer already accepts SaaS and lacks ops capacity. Options: (1) *quick* — Jira/Confluence connectors into EOIP (BL-23) with MCP bridge to Rovo MCP read tools where policy allows; (2) *native* — DC-first Atlassian importer with ACL replication plus offline mode; (3) *long-term* — positioning as the post-DC-EOL home for Atlassian on-prem knowledge. Selected: (2). Sketch: `DC REST -> SourceEvent v2 (acl_hash) -> gate -> graph`. POC: ingest a 10k-issue Jira DC project and 2k Confluence pages offline; success = 100% ACL parity with source on 200 sampled user/doc pairs; cost baseline CPU-only one node. Failure cases: DC group nesting, anonymous access, permission scheme drift. Defensibility: ownership and air-gap persist even if Atlassian adds features. **Decision: ADOPT (as DC-ingest priority).**

**INV-atlassian-rovo-02 — Optional permission replication on connectors (`replicatesPermissions=false` makes data workspace-visible).** Root cause: governance/semantics (proven). Alternative: EOIP refuses unlabelled ingestion; worse when sources are truly public. Options: quick — default-deny gate; native — per-fact principal sets; long-term — ACL-aware retrieval proofs. Selected: native. POC: seed 100 docs with mixed ACLs, 3 principals; zero leakage in retrieval, summaries and caches (J5). Decision: **ADOPT** (also closes BL-18).

**INV-atlassian-rovo-03 — Consumption metering with default-on overage.** Root cause: licensing. EOIP counterpart: flat per-node licence plus local model cost; worse if the customer has no GPU/CPU capacity. Decision: **DEFER** (commercial, not engineering).

## 13. Per-capability decisions

| Capability | Decision | Note |
|---|---|---|
| CAP-26 Jira/Confluence DC and Cloud connectors | BUILD | Ingest, never mutate graph directly |
| CAP-46 source-ACL in retrieval | BUILD | P0 |
| CAP-59 MCP interface to graph | EXPERIMENT | Add principal-bound read scope; stay read-only |
| CAP-21 federation vs materialise per source | EXPERIMENT | Rovo's 3 modes as taxonomy |
| CAP-52 / CAP-50 air-gap packaging | BUILD | Differentiator |
| Rovo/Teamwork Graph as a dependency | REJECT | SaaS, proprietary |
| Consume Rovo MCP as an optional external source | DEFER | Egress policy must be explicit per tenant |

## 14. Concrete tests, proof-of-concept, and acceptance conditions

1. DC-ACL parity (INV-01 POC) — 200 sampled principal/doc pairs, 100% match. 2. Connector without declared ACL fidelity is denied tenant-wide publication. 3. Agent via MCP as low-privilege principal: zero forbidden entities in results, summaries or caches. 4. Offline run: block egress at firewall, full ingest + query succeeds. 5. Re-run when Rovo MCP/CLI leave beta: re-verify scopes, rate limits and write semantics (tracked as open item).

## 15. Risks, trade-offs, and open research questions

Risks: most Rovo internals unverified; GA/beta status inconsistent between press and Atlassian; Atlassian could ship DC AI features later (no evidence). Open questions: query-time ACL mechanism; whether graph export or API enumeration exists; Teamwork Graph storage engine; how Units isolate; whether Atlassian offers any self-hosted LLM path. Legal items for review: Forge/Marketplace terms if EOIP ever publishes an Atlassian app.

---

## Appendix A — Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | Proprietary SaaS; DC EOL 2029-03-28; no patents examined |
| D2 | 2 | Work-graph search/agents |
| D3 | 4, 5 | Cloud only; connectors, OpenSearch hybrid retrieval |
| D4 | 5 | Storage NOT PUBLICLY VERIFIED |
| D5 | 5 | Object types + relationships; no ontology language found |
| D6 | 5 | No query language exposed; N/A beyond MCP/CLI |
| D7 | — | N/A: no reasoning engine documented |
| D8 | 7 | N/A (SaaS); no benchmarks |
| D9 | 5, 3 | Connector modes, sync fidelity, incremental flag |
| D10 | 5 | No ER detail; permission mapping via OAuth |
| D11 | 5 | Not verified |
| D12 | — | N/A: no graph ML documented |
| D13 | 2, 3, 5 | Hybrid retrieval, MCP, agents; citations not verified |
| D14 | — | N/A |
| D15 | 3, 8 | Agent governance announced |
| D16 | 3 | Chat, Slack, Jira embedded |
| D17 | 3, 5 | Forge, MCP, CLI |
| D18 | 5, 9 | Connector ACL declaration; scope errors |
| D19 | 5 | Org scoped; Units UNVERIFIED |
| D20 | 7, 9 | Credits; no latency data |
| D21 | 1, 10, 12 | Bundled, credits, overage |
| D22 | 9 | Export NOT VERIFIED |
| D23 | — | N/A: no patent review done |
| D24 | App. C | Many third-party sources; confidence stated |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-26 | native (cloud) / plugin (Forge) | 04, 08 | BL-23 Implemented | BUILD | P1 |
| CAP-46 | native (claimed) | 09, 08 | BL-18 Absent | BUILD | P0 |
| CAP-47 | native (SaaS) | 09 | BL-20 Partial | BUILD | P0 |
| CAP-50 | absent | 01, 03 | Implemented (files) | BUILD | P1 |
| CAP-51 | absent (no customer control found) | 10 | BL-45 Implemented | BUILD | P1 |
| CAP-53/54/55 | native (OpenSearch hybrid) | 09 | BL-13/14/15 | REUSE patterns | P2 |
| CAP-59 | native, beta | 05, 07 | BL-47 Implemented | EXPERIMENT | P2 |
| CAP-21 | native (Direct connectors) | 09 | BL-51 Partial | EXPERIMENT | P2 |
| CAP-48 | native (agent audit, announced) | 05 | unknown | DEFER | P3 |
| CAP-77 | native (credits) | 01 | BL-22 Implemented | REFERENCE | P3 |

## Appendix C — Evidence records (access date 2026-10-26)

| CLAIM-ID | Product / version / date | Exact claim | Classification | Source + URL | Pub / access | Confidence | Contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-atlassian-rovo-01 | Rovo licensing, 2026 | Included with Standard/Premium/Enterprise Cloud plans; credits 25/70/150 (Jira or Confluence) and 250/700/1,500 (Teamwork/Service Collection); extra usage $0.01/credit, on by default up to a cap; full Rovo features (search, chat, agents, studio) require a Cloud plan; DC connectors "don't provide the full AI feature set" | Officially documented | Atlassian, Rovo licensing, https://www.atlassian.com/licensing/rovo | undated / 2026-10-26 | 0.85 (fetched page) | Per-request credit costs (10/100) only in third-party blogs |
| CLAIM-atlassian-rovo-03 | DC EOL | DC subscriptions and Marketplace apps expire 2029-03-28 23:59 PST (read-only); new DC sales to new customers ended 2026-03-30; existing customers may buy until 2028-03-30; Bitbucket/Bamboo/Jira Align DC excluded | Officially documented (via search summary of the page) | Atlassian, https://www.atlassian.com/licensing/data-center-end-of-life | undated / 2026-10-26 | 0.8 (page not fetched directly) | A community post says 2029-03-30 |
| CLAIM-atlassian-rovo-04 | Rovo DC connectors | Connectors exist for Confluence DC (pages, blogs, attachments) and Jira/JSM DC (issues, projects, work items); Confluence space allowlist; data indexed into Rovo on Cloud | Officially documented (search summary) | Atlassian, https://www.atlassian.com/migration/rovo-connectors-data-center | undated / 2026-10-26 | 0.6 (page body would not render in fetch) | Supported DC versions and data flow not verified |
| CLAIM-atlassian-rovo-05 | Team '26, 2026-05-06 | Connectors (Forge) GA; Rovo Studio GA; Jira agents GA; Teamwork Graph CLI (300+ commands) and Teamwork Graph tools in Rovo MCP open beta; Max mode early access; several governance items announced without status | Third-party report | SiliconANGLE, https://siliconangle.com/2026/05/06/atlassian-opens-teamwork-graph-pushes-rovo-agentic-execution-team-26 ; Atlassian, https://www.atlassian.com/blog/company-news/rovo-team-26 | 2026-05-06 / 2026-10-26 | 0.7 | Atlassian's own post gives no availability stage for MCP/CLI |
| CLAIM-atlassian-rovo-06 | Team '26 | ">150 billion connections"; "44% more accurate" and "48% fewer tokens" (Atlassian benchmarks; workload undisclosed); >90% of enterprise cloud customers use Rovo | Vendor claim | same as 05 | 2026-05-06 / 2026-10-26 | 0.4 (as truth) / 0.8 (as quoted) | None independent |
| CLAIM-atlassian-rovo-07 | Rovo MCP Server v2 | Endpoint `https://mcp.atlassian.com/v2/mcp`; OAuth 2.1 primary, API token optional; Jira, JSM, Confluence, Bitbucket, Projects, Goals, Loom; "powered by your Teamwork Graph"; v1 retires 2027-03-01; docs say nothing on Data Center | Officially documented | Atlassian Support, https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/ | undated / 2026-10-26 | 0.8 | Beta/GA stage unstated |
| CLAIM-atlassian-rovo-08 | Forge `graph:connector` | Manifest `objectTypes`; capabilities `replicatesPermissions`, `syncFidelity` (append/upsert/mirror), `supportsIncrementalSync`; if `replicatesPermissions` false, all ingested data visible to every workspace user; storing email, calendar, recordings, HRIS, regulated financial/health, GDPR special-category data prohibited; SDK offers object, relationship, user, group and task operations | Officially documented | Atlassian Developer, https://developer.atlassian.com/platform/forge/manifest-reference/modules/teamwork-graph-connector and https://developer.atlassian.com/platform/teamwork-graph/connector-reference/overview | 2025-11-24 (SDK page) / 2026-10-26 | 0.8 | Stage (EAP vs GA) unstated; search summary earlier called the SDK EAP |
| CLAIM-atlassian-rovo-09 | Rovo architecture, 2025-12 | Hybrid retrieval BM25 + kNN on AWS OpenSearch; connector types Synced, Synced Lite, Direct, Smart Link; permissions "honored throughout" without mechanism; Rovo residency limited availability | Third-party report | NetEye blog, https://www.neteye-blog.com/blog/2025/12/30/atlassian-rovo-today-architecture-technologies-and-enterprise-trust/ | 2025-12-30 / 2026-10-26 | 0.5 | Not confirmed by Atlassian primary doc |
| CLAIM-atlassian-rovo-10 | Rovo AI transparency | Atlassian's transparency pages name OpenAI and Google plus open-source models for Rovo Agents; other-language pages name Anthropic for Rovo Chat | Officially documented (search summary) | https://www.atlassian.com/trust/ai/transparency | undated / 2026-10-26 | 0.5 | Pages disagree with each other |
| CLAIM-atlassian-rovo-11 | Rovo MCP | Developer-community report that Teamwork Graph MCP tools returned "read teamwork graph not authorized" after admin grant | User-reported | https://community.developer.atlassian.com/t/rovo-mcp-bitbucket-teamwork-graph-tools-return-read-teamwork-graph-not-authorized-after-admin-grants-the-permission-api-token-auth/100501 | n/d / 2026-10-26 | 0.4 | No Atlassian response retrieved |

## Appendix D — Assumptions

A1 Access date 2026-10-26 used. A2 Several Atlassian pages rendered only navigation in WebFetch; those claims rely on search-result summaries and carry lower confidence. A3 Rovo Dev, Rovo pricing for individual features and "Units" were not investigated beyond snippets. A4 No query-time ACL mechanism claimed for Rovo. A5 "Heavyweight" interpreted as customer-side deployment weight.
