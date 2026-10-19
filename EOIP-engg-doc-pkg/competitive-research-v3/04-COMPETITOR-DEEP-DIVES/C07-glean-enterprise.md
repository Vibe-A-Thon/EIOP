# C07 — Glean (enterprise search, Knowledge Graph and Enterprise Graph)

| Field | Value |
|---|---|
| Registry ID | T-C07-glean-enterprise |
| Tier | A. Glean is the closest enterprise-knowledge competitor and the reference buyers use for permission-aware enterprise search and assistants. |
| Versions examined | Glean SaaS as documented at docs.glean.com and developers.glean.com on the access date. Glean publishes no public version numbers. Milestones: Personal Graph (Glean:GO, May 2025); Enterprise Graph, third-generation Assistant and Agentic Engine 2 (Glean:LIVE, 2025-09-25); on-premises architecture with Dell announced 2025-05-20; knowledge-graph engineering blog last updated 2025-06-27. |
| Verified on | 2026-10-18 |
| Worker | W16 |

---

## 1. Identity, current status, tier, and sources

**Identity.** Glean Technologies, Inc. (glean.com) sells "Work AI". The product is a SaaS platform with five parts:

- Enterprise search across 100+ connectors [CLAIM-glean-enterprise-04].
- A **Knowledge Graph** built on three pillars: content, people and activity [CLAIM-glean-enterprise-04].
- A per-user **Personal Graph** [CLAIM-glean-enterprise-06].
- The **Enterprise Graph**, which extends the Knowledge Graph to projects, processes and data [CLAIM-glean-enterprise-06].
- The Glean Assistant, Glean Agents, an MCP server and an MCP gateway [CLAIM-glean-enterprise-08].

**Name collision (Master Prompt §5.7) resolved.** This entry covers the **enterprise SaaS product from Glean Technologies**. It is not *Glean*, Meta's open-source code-indexing system, which is researched separately in C15 by W27. Glean the company does offer a "Code Search" tool through its MCP server [CLAIM-glean-enterprise-08], but that is a feature of the SaaS product, not Meta's indexer.

**Status.** Active and continuously delivered.

- The Enterprise Graph, Personal Graph, third-generation Assistant and Agentic Engine 2 (Assistant only) were reported **generally available** at Glean:LIVE on 2025-09-25.
- At that point, remote MCP servers, the conversational agent builder and the agent toolkit were **beta**, and model choice, the MCP directory and Canvas were "coming soon" [CLAIM-glean-enterprise-06].
- In 2026 Glean was named a "Market Shaper" in Gartner's 2026 Emerging Market Quadrant for no-code agent builders [CLAIM-glean-enterprise-17].

**Licence.** Proprietary SaaS with per-seat contracts. No price list is published [CLAIM-glean-enterprise-15]. The licence of the Indexing SDK was not verified.

**Tier reason.** Tier A. Buyers compare EOIP's retrieval, permissions and assistant layers with Glean before anything else.

**Sources:** 12 official Glean pages (docs, developer docs, engineering blog, press releases), plus 4 third-party sources (Reworked twice, Business Wire, pricing aggregators). Records are in Appendix C.

## 2. Primary problem, target workloads, concrete example workflows

**Problem.** Employees cannot find or act on knowledge scattered across SaaS applications. Glean solves this in three steps [CLAIM-glean-enterprise-04] [CLAIM-glean-enterprise-05] [CLAIM-glean-enterprise-10]:

1. It crawls every app and keeps each source's permissions.
2. It builds a graph of content, people and activity.
3. It answers through search, an assistant and agents, filtering results by the user's permissions at query time.

**Segments.** Mid-size to large enterprises across industries. The Dell on-prem announcement names regulated sectors such as healthcare and financial services [CLAIM-glean-enterprise-14].

**Workflows (illustrative; the capabilities are documented):**

1. *Permission-aware search.* An engineer searches "payments outage runbook". Results come from Confluence, Slack and Google Drive, trimmed to documents the engineer can open in each source [CLAIM-glean-enterprise-10] [CLAIM-glean-enterprise-11].
2. *Assistant answer with people context.* "Who owns the billing service?" The answer draws on the people pillar (identities, roles, reporting lines) and on activity signals [CLAIM-glean-enterprise-04].
3. *Agent across tools.* A scheduled agent summarises new Jira tickets and drafts a reply using connector "tools/actions" and remote MCP servers [CLAIM-glean-enterprise-06] [CLAIM-glean-enterprise-09] [CLAIM-glean-enterprise-11].
4. *External agent host.* Claude Code or Cursor calls Glean's MCP server tools (Search, Chat, Read Document, People, Code Search) with user-scoped OAuth [CLAIM-glean-enterprise-08].
5. *Custom source.* A firewalled in-house system pushes documents and per-document ACLs through the Indexing API/SDK [CLAIM-glean-enterprise-10] [CLAIM-glean-enterprise-11].

**Fit for on-prem, local-first.** The deployment models currently documented are both managed by Glean: Glean Hosted on GCP, and Customer Hosted (formerly "Cloud-Prem") on GCP or AWS [CLAIM-glean-enterprise-01]. An on-prem architecture with Dell was **announced** in May 2025. It is not listed in the current deployment documentation, so GA is **unverified** [CLAIM-glean-enterprise-14].

## 3. Feature inventory

| Area | Feature | Status | Evidence |
|---|---|---|---|
| Search | Hybrid semantic + lexical search fed by a real-time crawler | Present | CLAIM-glean-enterprise-05 |
| Graph | Knowledge Graph (content, people, activity pillars) | Present | CLAIM-glean-enterprise-04 |
| Graph | Enterprise Graph (projects, processes, data) | Present (GA per Reworked) | CLAIM-glean-enterprise-06 |
| Graph | Personal Graph (private per user; tasks and projects inferred from actions) | Present (GA per Reworked) | CLAIM-glean-enterprise-05, -06 |
| Graph | Customer-facing graph query API, schema or ontology editing, graph export | Absent / unknown: not found in public docs | — |
| Connectors | Native connectors (100+), web history, push via the Indexing API, partner connectors, tools/MCP for live access | Present | CLAIM-glean-enterprise-04, -11 |
| Connectors | Incremental crawl and webhooks; permission-change notifications (e.g., OneDrive Graph delta queries plus webhooks) | Present | CLAIM-glean-enterprise-11, -19 |
| Connectors | Indexed, live and hybrid access modes | Present | CLAIM-glean-enterprise-11 |
| Permissions | Query-time enforcement; per-document ACLs (users, groups, group intersections); identity graph of users, groups and memberships | Present | CLAIM-glean-enterprise-10 |
| Permissions | Admin item-level inclusion and exclusion; SharePoint site allow/block lists, Entra-group restriction | Present | CLAIM-glean-enterprise-04, -11 |
| AI | Assistant (third generation), Agentic Engine 2 | Present | CLAIM-glean-enterprise-06, -07 |
| AI | Agents: scheduled agents GA; conversational builder beta (2025-09) | Present / beta | CLAIM-glean-enterprise-06 |
| AI | LLM keys: Universal Model Key (managed by Glean) or Customer Key (BYOK); OpenAI, Azure OpenAI, Vertex AI, Bedrock; Claude via Vertex or Bedrock | Present | CLAIM-glean-enterprise-12 |
| AI | Local or self-hosted LLM | Not documented in the deployment or LLM pages read | CLAIM-glean-enterprise-01, -12 |
| AI governance | Glean Protect: zero LLM data retention, no training on enterprise data | Present | CLAIM-glean-enterprise-13 |
| MCP | Glean MCP server (Search, Chat, Read Document, Code Search, People, Artifacts, agents as tools); OAuth 2.1 + PKCE; 22 listed hosts | Present | CLAIM-glean-enterprise-08 |
| MCP | Glean as MCP host (remote MCP servers): fully supported in Glean, beta in agents; MCP gateway | Present / beta | CLAIM-glean-enterprise-08, -09 |
| Deployment | Glean Hosted (GCP); Customer Hosted (GCP or AWS), operated by Glean | Present | CLAIM-glean-enterprise-01 |
| Deployment | On-prem (Dell AI Factory) | Announced 2025-05-20; GA unverified | CLAIM-glean-enterprise-14 |
| Deployment | Air-gapped | Absent: not documented | CLAIM-glean-enterprise-01 |
| Tenancy | Isolated single tenant per customer | Present | CLAIM-glean-enterprise-16 |
| Residency | Multiple GCP and AWS regions; Customer Hosted gives "full data residency guarantees" | Present | CLAIM-glean-enterprise-03 |
| White-label/OEM | — | Absent (not found) | — |
| Query languages | Cypher, Gremlin, SPARQL or GQL | Absent (not found) | — |

## 4. Text-based architecture diagram

```
  SaaS SOURCES (100+)                       GLEAN SINGLE-TENANT DEPLOYMENT
  (Drive, SharePoint, Slack,                (Glean Hosted on GCP, or Customer Hosted in customer GCP/AWS;
   Confluence, Jira, Salesforce ...)         operated, upgraded and monitored by Glean; Glean support access)
        │  native connectors: crawl +       ┌──────────────────────────────────────────────────────────────┐
        │  webhooks/incremental             │ Crawler: content analysis, metadata, PERMISSIONS, facets     │
        │  (permission map fetched)         │   │                                                          │
  Custom/firewalled systems ──Indexing API──►   ├─► Lexical index ┐                                        │
  Browser extension (web history) ─────────►   ├─► Semantic index├─► Hybrid retrieval ─► ranking (people +  │
  Activity (Slack/Teams/email/plugins) ────►   │                 ┘     (query-time ACL     activity signals)│
                                            │   ├─► Identity graph (users, groups, memberships)            │
                                            │   └─► Knowledge Graph → Enterprise Graph (entities, triples   │
                                            │        with timestamps/ACL/confidence/provenance; LLM-        │
                                            │        expanded edges) + Personal Graph (per user)            │
                                            │                         │                                     │
                                            │   Assistant / Agentic Engine 2 / Agents (planner, memory)     │
                                            │        │ tools: connector actions, remote MCP (via gateway)   │
                                            └────────┼──────────────────────────────┬──────────────────────┘
                                                     ▼                              ▼
                                   LLM providers via Universal Model Key   Glean MCP server (OAuth 2.1/PKCE)
                                   or Customer Key: OpenAI / Azure OpenAI  → Claude Code, Cursor, VS Code,
                                   / Vertex / Bedrock (zero retention)       ChatGPT ... (22 hosts)
  CONTROL PLANE: Glean-operated (upgrades, patching, monitoring); customer has no manual deploy or patch rights.
```

## 5. Under-the-hood reconstruction

The platform is proprietary. Statements are **documented** (with a CLAIM-ID) or a **hypothesis** (marked H). This is a blueprint for equivalent behaviour, not a description of Glean's code.

### 5.1 Data model

- **Documents** carry content, metadata and a `DocumentPermissionsDefinition` with three fields: `allowed_users`, `allowed_groups` and `allowed_group_intersections` [CLAIM-glean-enterprise-10].
  - Inside one intersection entry, the user must belong to *every* listed group. Separate entries are alternatives.
  - An ACL is therefore a disjunction of conjunctions of group memberships, OR'd with direct user grants. This is more expressive than the flat "user or group" lists most RAG stacks use.
- **Identity graph:** users, groups and memberships are pushed separately from content. If a connector returns groups it must also return memberships, or the SDK raises `InconsistentDataError`.
  - Glean advises against flattening groups into user lists, because flattened ACLs go stale [CLAIM-glean-enterprise-10].
- **Knowledge Graph:** entities and edges stored as (subject, predicate, object) triples [CLAIM-glean-enterprise-05].
  - Edge properties may include "timestamps, access control, confidence scores, or provenance".
  - Entities come from NLP noun-phrase extraction, with common terms filtered out statistically. An entity is promoted using signals such as appearing in document titles, being linked often, and being popular in shared or accessed files.
  - A predicate is kept only when the evidence for it is "strong, repeatable" (e.g., "project led by").
  - LLMs extended the graph to "thousands of edges".
- **Personal Graph:** LLMs group a user's atomic actions into subtasks, tasks and themes, and map them to objectives such as OKRs [CLAIM-glean-enterprise-05].
- **NOT PUBLICLY VERIFIED:** the physical graph store, the schema, and whether the graph is exposed to customers.
  - *H1:* the graph is an internal ranking and planning substrate. There is no customer-facing graph query language and no ontology editing.

```
Document  { id, datasource, title, body, url, metadata, permissions: { allowed_users[], allowed_groups[],
            allowed_group_intersections[[group]] }, updated_at }
Identity  { users[], groups[], memberships[(group, member)] }
Edge      { subject_entity, predicate, object_entity, timestamp?, acl?, confidence?, provenance? }   # per blog
PersonalTask { user, actions[], task, theme, objective? }                                           # per blog
```

### 5.2 Storage layout and indexing

- **Documented:** the crawler feeds both semantic and lexical search and the knowledge graph. Glean argues that indexing, not federation, is needed to connect data across sources [CLAIM-glean-enterprise-05].
- **Documented:** activity data "never leaves your exclusive GCP project" [CLAIM-glean-enterprise-04]. Each tenant is isolated as a single tenant [CLAIM-glean-enterprise-16].
- **NOT PUBLICLY VERIFIED:** the index engines (inverted index technology, vector index type) and the storage layout.
  - *H2:* per-tenant lexical and vector indexes, with ACL fields indexed as tokens so permission filtering happens inside the retrieval query and not after it. This is the standard way to make query-time enforcement scale.

### 5.3 Query pipeline

The pipeline below is a hypothesis (H3), consistent with [CLAIM-glean-enterprise-05] and [CLAIM-glean-enterprise-10]:

```
principals = expand(user) ∪ groups_transitive(user)             # from identity graph
q_struct   = parse_intent(query, personal_graph(user))           # blog: intent -> structured form
cands      = lexical(q, filter=acl_match(principals)) ⊕ semantic(q, filter=acl_match(principals))
cands     += graph_expand(q_struct, enterprise_graph, filter=acl_match(principals))
ranked     = rerank(cands, signals={popularity, people proximity, recency, activity})
acl_match(doc) := user ∈ doc.allowed_users ∨ ∃g ∈ doc.allowed_groups: g ∈ principals
                  ∨ ∃S ∈ doc.allowed_group_intersections: S ⊆ principals
answer     = LLM(ranked[:k], citations=True)                     # via Universal or Customer key
```

The blog says query intent is converted into a structured form and executed against the graph, and that "this fulfilment step is where the graph structure proves essential" [CLAIM-glean-enterprise-05]. How ranking weighs graph signals is **not documented**.

### 5.4 Reasoning

The blog says triples "can be traversed to infer additional knowledge" [CLAIM-glean-enterprise-05]. There is no documented rule engine, ontology or formal semantics. Inference is statistical (NLP and LLM) and graph traversal.

### 5.5 Concurrency, freshness, consistency

- **Documented:** changes are captured "often through webhooks or incremental crawling", as fast as the source and connector allow. Admins can tune crawl frequency and blackout periods [CLAIM-glean-enterprise-04] [CLAIM-glean-enterprise-11].
- **Consistency model** *(H4)*: eventually consistent with each source. Permission-change propagation latency depends on the connector (OneDrive uses delta queries plus webhooks) [CLAIM-glean-enterprise-19].
- No transactional semantics apply, since this is a search index.

### 5.6 Partitioning, caching, versioning

- **Partitioning:** one isolated tenant per customer [CLAIM-glean-enterprise-16].
- **Caching and versioning:** not documented. There is no documented document-version history or as-of query.

### 5.7 Security

- **Query-time ACL enforcement** [CLAIM-glean-enterprise-10].
- **Single-tenant isolation**, with support access that requires approval, uses a 1-hour time-bound token, and is audited [CLAIM-glean-enterprise-16].
  - Glean also retains support access in Customer Hosted deployments [CLAIM-glean-enterprise-02].
- **Zero LLM data retention** and no training on enterprise data (Glean Protect) [CLAIM-glean-enterprise-13].
- **MCP:** OAuth 2.1 with PKCE, user-level access control [CLAIM-glean-enterprise-08].
- **SDK test harness:** can assert that listed identities never appear in any transformed ACL [CLAIM-glean-enterprise-10]. This is a testable leakage guard EOIP should copy as a pattern.

## 6. Functional and non-functional requirements inferred

| # | Requirement | Source |
|---|---|---|
| FR-1 | Per-document ACLs as a disjunction of users, groups and group-intersections, with an unflattened identity graph | CLAIM-glean-enterprise-10 |
| FR-2 | Filtering by permission at query time on every retrieval path (search, assistant, MCP) | CLAIM-glean-enterprise-08, -10 |
| FR-3 | Incremental, webhook-driven sync of content **and** permission changes | CLAIM-glean-enterprise-11, -19 |
| FR-4 | A push API so custom or firewalled sources can join with the same ACL semantics | CLAIM-glean-enterprise-11 |
| FR-5 | Indexed, live and hybrid source access modes | CLAIM-glean-enterprise-11 |
| FR-6 | People and activity signals in ranking; a private per-user context graph | CLAIM-glean-enterprise-04, -05 |
| FR-7 | An MCP server exposing search, read and people tools with OAuth, plus a governed gateway to third-party MCP servers | CLAIM-glean-enterprise-08, -09 |
| NFR-1 | Isolated single tenant per customer; time-bound, audited support access | CLAIM-glean-enterprise-16 |
| NFR-2 | Zero LLM data retention; no training on customer data | CLAIM-glean-enterprise-13 |
| NFR-3 | Regional data residency | CLAIM-glean-enterprise-03 |

## 7. Performance and resource model

- **No public latency, throughput or recall benchmarks** and no independent evaluation were found. Retrieval quality claims are vendor marketing (Unverified).
- **Freshness:** depends on the source and connector (webhooks vs incremental crawl). No SLA was found in the sources read [CLAIM-glean-enterprise-11].
- **Resource footprint:** not applicable to customers in the managed models; Glean operates the infrastructure [CLAIM-glean-enterprise-01]. The footprint of the Dell on-prem architecture is not published [CLAIM-glean-enterprise-14].
- **Cost:** per seat, not published. Third-party estimates range from about $30 to $75 per user per month with roughly 100-seat minimums, plus usage-based pricing for agents and Deep Research. All of this is **Unverified** (buyer-reported or from competitors) [CLAIM-glean-enterprise-06] [CLAIM-glean-enterprise-15].
- **Failure modes (inferred):**
  - ACLs go stale if connectors flatten groups, which is why Glean warns against it.
  - Permission-change lag between the source and the index.
  - Gaps where no connector exists (a Reworked commentator notes mid-size companies run 200–300 apps) [CLAIM-glean-enterprise-06].
  - Source-vendor API restrictions, e.g., the 2025 Slack API restriction mentioned by Reworked [CLAIM-glean-enterprise-06].

## 8. Strengths and how to match or exceed them

1. **Rigorous ACL model with an identity graph and query-time enforcement** [CLAIM-glean-enterprise-10]. EOIP captures permission metadata (BL-17) but does not enforce it (BL-18 Absent). **Match (P0).** EOIP can *exceed* by carrying the ACL onto derived graph facts and claims, which Glean's blog says edges can hold but does not document as enforced on inferred edges.
2. **Connector breadth and permission-change sync** [CLAIM-glean-enterprise-04] [CLAIM-glean-enterprise-11] [CLAIM-glean-enterprise-19]. EOIP has 30+ connectors emitting SourceEvents (BL-23) with replay and DLQ (BL-24). **Match selectively** on the general-enterprise sources (SharePoint, Drive, Slack, Teams).
3. **People and activity graph in ranking** [CLAIM-glean-enterprise-04] [CLAIM-glean-enterprise-05]. **Experiment.** EOIP has an identity resolver (BL-34) but no activity signals.
4. **MCP server and gateway** [CLAIM-glean-enterprise-08] [CLAIM-glean-enterprise-09]. **Match.** EOIP's MCP is read-only (BL-47) with no OAuth 2.1 flow verified, and it has no gateway for third-party MCP servers.
5. **Zero-retention LLM terms and BYOK** [CLAIM-glean-enterprise-12] [CLAIM-glean-enterprise-13]. **Exceed.** EOIP's default is local models with egress level S0 (BL-45).
6. **Indexed, live and hybrid access** [CLAIM-glean-enterprise-11]. **Match** via the federation planner (BL-51 Partial).
7. **Identity-leak test harness** [CLAIM-glean-enterprise-10]. **Adopt** the pattern in the EOIP connector conformance tests.

## 9. Limitations with root causes

**Verified defects.** None found.

**Intentional trade-offs (documented):**

- Both documented deployment models are operated by Glean. Customers cannot deploy or patch manually, and Glean keeps support access [CLAIM-glean-enterprise-01] [CLAIM-glean-enterprise-02].
- Index-centric design: Glean argues federation is insufficient [CLAIM-glean-enterprise-05].

**Licensing and commercial:** proprietary per-seat SaaS with no public price list [CLAIM-glean-enterprise-15]. No OEM or white-label offering was found.

**User-reported complaints and third-party commentary:** integration depth is the main risk, as are mostly read-only integrations that need new actions [CLAIM-glean-enterprise-06]. Third-party pricing pages complain about seat minimums (Unverified).

**Outdated claims to avoid:**

- "Glean is cloud-only." Partly outdated: Customer Hosted runs in the customer's cloud, and on-prem with Dell has been announced.
- "Glean is fully on-prem." Unverified: the current documentation does not list on-prem.

**Hypotheses:** no customer-facing graph query or ontology layer (H1). Permission enforcement on LLM-inferred edges is not documented.

| Root-cause class | Root cause | Status |
|---|---|---|
| Algorithmic dead end | A statistically inferred, schema-less graph (noun phrases, LLM edges) is opaque to users. There is no governed ontology, evidence UI or epistemic separation for multi-hop "why" questions (J1, J2) | Construction documented; customer-facing absence is a hypothesis |
| Algorithmic dead end | A search-first architecture answers "find" questions well. Typed digital-thread traversal (story → PR → commit → function → deployment) is not documented | Hypothesis |
| Operational overhead | Vendor-operated SaaS or managed deployment in the customer's cloud. No air-gap; on-prem not in the docs | Proven (docs) |
| Operational overhead | The LLM path depends on hyperscaler providers (OpenAI, Azure, Vertex, Bedrock). No documented local-model path in the pages read | Proven for providers listed; absence of a local option is a hypothesis |
| User/developer friction | Graph not exportable or queryable by customers; proprietary ranking. Lock-in through the index and the graph | Hypothesis (absence) |
| User/developer friction | Seat minimums and opaque pricing | Third-party |

## 10. Deployment, licensing, redistribution, and operational viability under EOIP constraints

| EOIP constraint | Glean position | Evidence |
|---|---|---|
| 1. Self-hosted, air-gap capable | **No** air-gap documented. Customer Hosted is "not a traditional self-hosted model" and is operated by Glean. On-prem with Dell is announced only | CLAIM-glean-enterprise-01, -02, -14 |
| 2. Default-local LLM | **No**. Hyperscaler LLMs via a Glean-managed key or BYOK; zero retention | CLAIM-glean-enterprise-12, -13 |
| 3. Backend neutrality | N/A (proprietary indexes) | — |
| 4. Connectors never mutate graph directly | Connectors feed a crawler and index (aligned in spirit) | CLAIM-glean-enterprise-04 |
| 8. Permissions survive everything | **Strong** for retrieval. Enforcement on derived graph edges and agent memory is not documented | CLAIM-glean-enterprise-10, -05 |
| 9. Tenant isolation / white-label | Single-tenant isolation **yes**; white-label **no** | CLAIM-glean-enterprise-16 |
| 10. One-node first | N/A (managed) | — |
| 12. Redistribution | Not a redistributable component | — |

**Integration options for EOIP (lawful, public APIs):**

- An EOIP MCP client consumes Glean's MCP server as a *read-only external source*. This is subject to the egress policy, because Glean results leave Glean.
- Glean consumes EOIP through Glean's remote-MCP host feature, so EOIP becomes a "tool" inside Glean [CLAIM-glean-enterprise-09]. This is a plausible go-to-market path ("EOIP as the evidence graph behind Glean").

## 11. Competitive delta against the EOIP verified baseline

| Capability | Glean | EOIP baseline | Delta |
|---|---|---|---|
| Source-ACL enforcement in retrieval | Query-time, identity graph (CLAIM-10) | BL-17 captured; **BL-18 Absent** | **EOIP P0 gap** |
| Connector breadth (general enterprise) | 100+ (CLAIM-04) | 30+ mostly IT/engineering (BL-23) | **EOIP behind** on SharePoint, Drive, Slack, Teams, CRM |
| Permission-change sync | Webhooks and delta (CLAIM-19) | Webhook dedupe, replay (BL-24); ACL-change propagation untested | **EOIP behind** |
| Hybrid search | Lexical + semantic (CLAIM-05) | BM25 + hashing vectors + RRF in-process (BL-13..15) | **EOIP behind** in quality and scale (no persistent vector DB) |
| People/activity ranking | Yes (CLAIM-04) | Identity resolver only (BL-34) | **EOIP behind** |
| Typed knowledge graph, digital thread, evidence, claims | Inferred graph, internal (CLAIM-05) | LPG with revisions, claims, contradictions, evidence (BL-37..41) | **EOIP ahead** |
| Ontology governance | Not documented | GitOps partial (BL-32) | **EOIP ahead** |
| Code graph | "Code Search" tool (CLAIM-08) | Python/TS symbol graph, diff hunks (BL-42) | EOIP ahead on precision (to be proven by C15 benchmarks) |
| MCP | Server + gateway + 22 hosts (CLAIM-08) | 18 read tools (BL-47) | **EOIP behind** on auth and gateway |
| LLM locality | Hyperscaler LLMs, zero retention | Local default, egress gateway S0 (BL-45) | **EOIP differentiator** |
| Deployment | Managed SaaS / customer cloud; no air-gap | Compose single host, air-gap design (live test not run) | **EOIP differentiator** |
| White-label, multi-tenant for resellers | None | BL-21 Implemented, BL-20 Partial | **EOIP differentiator** (tenant isolation must reach P0 first) |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

### 12.1 Strength-adoption cards

| STR-ID | Competitor | Strength | Evidence | Value | Decision | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-glean-enterprise-01 | Glean | Query-time ACL enforcement over an unflattened identity graph, with group-intersection ACLs | CLAIM-glean-enterprise-10 | Users never see what they could not open in the source | **Match (P0)** | `PermissionMetadata` (BL-17) extended to `{users, groups, group_intersections}`. A principal-expansion service runs over directory connectors. ACL tokens are indexed in BM25 and vector stores and in graph filters; retrieval passes `principals` | J5: two users, same question, disjoint ACLs. Zero leaked documents, chunks, entities or citations across 1,000 randomised queries. A group-intersection case passes |
| STR-glean-enterprise-02 | Glean | Incremental and webhook sync of permission changes, not only content | CLAIM-glean-enterprise-11, -19 | Revocation takes effect quickly | **Match** | ACL-change SourceEvents (new event type) trigger index and cache invalidation and a re-check of agent memory | Revoke access in the source; within N minutes the document disappears from search, answers and MCP results. Measure p95 propagation latency |
| STR-glean-enterprise-03 | Glean | Identity-leak test harness in the indexing SDK | CLAIM-glean-enterprise-10 | Leakage is caught in CI, before production | **Adopt pattern** | Connector conformance test with a forbidden-identities list, asserted over every emitted SourceEvent ACL | CI fails if a forbidden identity appears. Seeded mutation tests prove the check detects it |
| STR-glean-enterprise-04 | Glean | MCP server with OAuth 2.1/PKCE, many validated hosts, agents as tools, and a governed MCP gateway | CLAIM-glean-enterprise-08, -09 | Customers use EOIP from any agent host safely | **Match** | OAuth 2.1 for EOIP MCP; per-tool scopes; gateway mode that proxies approved third-party MCP servers through the egress policy | MCP Inspector plus 3 hosts connect via OAuth. Scope-denied calls fail. Proxied tool calls are logged with egress manifests |
| STR-glean-enterprise-05 | Glean | People and activity signals personalise ranking; Personal Graph infers tasks | CLAIM-glean-enterprise-04, -05 | Better relevance and ownership answers | **Experiment** | Opt-in activity events (views, edits, commits) as ranking features, tenant-scoped and privacy-classified (BL-46). No per-user profiling without consent | nDCG@10 lift ≥ 5% over BM25 + dense + RRF on an internal relevance set. DSAR deletion removes the features |
| STR-glean-enterprise-06 | Glean | Indexed, live and hybrid source access | CLAIM-glean-enterprise-11 | Freshness for volatile sources without full indexing | **Match** | Federation planner (BL-51) marks sources `indexed`, `live` or `hybrid`; live calls go through ACL and egress checks | Live-mode answer reflects a source change within 5 s. Results respect ACLs |
| STR-glean-enterprise-07 | Glean | Broad general-enterprise connector catalogue | CLAIM-glean-enterprise-04 | Non-IT journeys (J15) | **Match selectively / integrate** | Prioritise SharePoint/OneDrive, Google Drive, Slack, Teams, Salesforce; reuse OSS connector frameworks (C14) behind the SourceEvent contract | Each connector passes the conformance, ACL and replay suites |

### 12.2 Con-to-Pro inversion cards

#### INV-glean-enterprise-01: managed SaaS / customer-cloud only, no air gap, vs customer-operated air-gapped deployment (seed hypothesis **validated with nuance**)

- **Target and workload:** Glean deployment models as documented 2026-10, for a regulated or sovereign buyer that needs offline operation.
- **Limitation (evidence):**
  - Two documented models: Glean Hosted (GCP), and Customer Hosted in the customer's GCP or AWS.
  - Glean operates both. Customers cannot deploy or patch manually, and Glean keeps support access [CLAIM-glean-enterprise-01] [CLAIM-glean-enterprise-02].
  - Air-gap is not documented. An on-prem architecture with Dell was **announced** on 2025-05-20, but it does not appear in current deployment docs [CLAIM-glean-enterprise-14].
- **Seed verdict (§10.5):**
  - "SaaS": **VALIDATED**. Even Customer Hosted is a managed service.
  - "Limited on-prem/air-gap": **VALIDATED**. On-prem is announced, not documented as available. Air-gap is undocumented.
  - "Heavyweight": **NOT VALIDATED**. Customers do not run the footprint, and no sizing is published.
  - "Lock-in": **PARTIALLY VALIDATED**. No documented graph or index export (hypothesis).
- **Root cause:** deployment (*proven*). The SaaS operating model relies on central operations and hyperscaler LLMs.
- **Why the alternative mitigates it:** customer-operated, single-node-capable, air-gapped EOIP with local models serves defence, critical infrastructure, sovereign and highly regulated buyers.
  - It is worse for buyers who want zero operational burden. Glean's managed model is better there.
- **Options:**
  - (a) Document an air-gap profile.
  - (b) Signed offline bundles with plan, apply and rollback (shared with INV-palantir-foundry-01).
  - (c) Partner-operated "managed sovereign" EOIP, giving Glean-like operations without vendor access.
- **Selected:** (b) now, and (c) as a channel option.
- **POC:** J16 on an offline host. Full ingest, permission-aware search and local-LLM answers with zero egress. The answer-quality gap against a hosted-LLM baseline is measured, not assumed.
- **Defensibility:** high. Moving a SaaS operating model with hyperscaler LLM dependencies to true air-gap is costly.
- **Decision:** **ADOPT**.

#### INV-glean-enterprise-02: standing vendor support access vs customer-held keys with break-glass access

- **Limitation:** "Glean maintains support access to your environment" in all models [CLAIM-glean-enterprise-02]. Access is time-bound to 1 hour, approved and audited [CLAIM-glean-enterprise-16].
- **Root cause:** governance and operating model (*proven*).
- **Alternative:** no vendor access by default in EOIP. Support works through customer-initiated break-glass sessions, signed diagnostic bundles with PII redaction (BL-46), and customer-held encryption keys.
  - It is worse when diagnosing incidents takes longer.
- **Options:** (a) redacted diagnostic bundle; (b) a break-glass workflow with dual approval and an audit chain; (c) remote support relays the customer controls.
- **Selected:** (a) and (b).
- **POC:** resolve 5 seeded faults using only redacted bundles. A DLP scan shows no PII in the bundles.
- **Defensibility:** medium. A procurement differentiator in regulated sectors.
- **Decision:** **ADOPT**.

#### INV-glean-enterprise-03: hyperscaler LLM dependency vs local-first models with policy-graded egress

- **Limitation:** documented LLM paths are OpenAI, Azure OpenAI, Vertex AI and Bedrock, through the Universal Model Key or a Customer Key. The deployment's cloud constrains which providers are allowed [CLAIM-glean-enterprise-12]. No self-hosted model path was found in the pages read (hypothesis; a secondary source mentions NVIDIA Nemotron support in 2026, which was not verified).
- **Root cause:** coupling to providers (*proven* for the listed providers).
- **Alternative:** a local model abstraction (Ollama/vLLM) with egress levels S0–Sn (BL-45). Hosted LLMs are used only after explicit client confirmation.
  - It is worse where local models answer less well. This must be measured (J6).
- **POC:** grounded-answer quality of local vs hosted models on 300 enterprise questions with citations. Report faithfulness and abstention, and accept local if within an agreed margin.
- **Defensibility:** medium-high when combined with air-gap.
- **Decision:** **ADOPT** (already in the design; prove it with benchmarks).

#### INV-glean-enterprise-04: opaque, statistically inferred internal graph vs a governed, typed, evidence-backed graph that customers can query

- **Limitation:**
  - The graph is built with NLP noun phrases plus LLM expansion [CLAIM-glean-enterprise-05].
  - No customer-facing schema, graph query API, ontology editing or export was found (hypothesis H1).
  - Edges *may* carry confidence and provenance, per the blog, but customers cannot inspect, approve or correct them through any documented UI.
- **Root cause:** semantics and UX. The graph is optimised for ranking, not as an asset the customer governs (*hypothesis*).
- **Alternative:** EOIP's typed ontology, evidence spans, claims with contradictions, PROPOSED-until-approved for AI-inferred edges (BL-39, BL-40), and as-of queries (BL-37). Answers to J1, J2 and J9 come with an explicit chain of evidence.
  - It is worse because curation costs effort. Glean needs no modelling; EOIP must make automatic proposal (BL-27) good enough.
- **Options:** (a) evidence panel for every answer; (b) a reviewable queue of inferred edges; (c) a calibrated confidence plane with feedback learning.
- **Selected:** (a) and (b).
- **POC:** on a 5k-document plus Jira/Git corpus, compare EOIP evidence-chain answers with a hybrid-RAG baseline on 100 multi-hop "why/impact" questions. Measure answer correctness, citation precision and reviewer time.
- **Defensibility:** high. It requires a data model and governance workflow, not a feature.
- **Decision:** **ADOPT**.

#### INV-glean-enterprise-05: per-seat SaaS with no white-label vs a white-label, multi-tenant OEM platform

- **Limitation:** proprietary per-seat SaaS, with no OEM or white-label offering found [CLAIM-glean-enterprise-15].
- **Root cause:** commercial model (*proven* absence in public material).
- **Alternative:** EOIP white-label branding (BL-21), offline licensing (BL-22) and tenant metering.
  - It is worse until tenant isolation is physically enforced (BL-20 Partial). Reselling before J13 passes is a P0 risk.
- **POC:** J13 isolation proof, then a two-tenant branded deployment.
- **Decision:** **ADOPT**, gated on J13.

## 13. Per-capability decisions

| CAP-ID | Capability | Decision | Note |
|---|---|---|---|
| CAP-46 | Source-ACL enforcement in retrieval and answers | BUILD (P0) | STR-01, STR-02, STR-03 |
| CAP-26 | General-enterprise connectors with ACL sync | BUILD + REUSE OSS frameworks | STR-07 |
| CAP-55 | Hybrid retrieval with people/activity features | BUILD baseline; EXPERIMENT personalisation | STR-05 |
| CAP-53 | Persistent vector index | REUSE (C10 decision) | Needed for parity |
| CAP-59 | MCP server with OAuth 2.1 and gateway | BUILD | STR-04 |
| CAP-21 | Indexed/live/hybrid source access | BUILD (extend BL-51) | STR-06 |
| CAP-50 | Air-gapped operation | BUILD | INV-01 |
| CAP-51/61 | Local-first LLM with egress | REUSE Ollama/vLLM + own gateway | INV-03 |
| CAP-38/43 | Evidence chains, reviewable inferred edges | BUILD | INV-04 |
| CAP-52 | White-label OEM | REUSE own (after J13) | INV-05 |
| CAP-48 | Support-access audit, break-glass | BUILD | INV-02 |
| — | Glean integration (EOIP as MCP tool inside Glean) | EXPERIMENT (go-to-market) | §10 |

## 14. Concrete tests and acceptance conditions (all PROPOSED)

| Test | Pass condition | Journeys |
|---|---|---|
| T-GLN-01 ACL parity | Group-intersection ACLs honoured; 0 leaks in 1,000 randomised two-user queries across search, answers, MCP and graph traversal | J5 |
| T-GLN-02 Revocation latency | Source revocation is reflected everywhere (index, cache, agent memory) within the agreed p95 | J5 |
| T-GLN-03 Connector identity-leak harness | Forbidden identities never present; mutation test detects seeded leaks | J7 |
| T-GLN-04 Retrieval quality vs strong baseline | EOIP hybrid ≥ BM25 + dense + RRF baseline on nDCG@10; graph-augmented beats it on multi-hop questions, or is not claimed | J6 |
| T-GLN-05 MCP OAuth | 3 hosts connect via OAuth 2.1/PKCE; scopes enforced; egress manifests logged | J5, J16 |
| T-GLN-06 Offline parity | J16 full run with local models; quality gap vs hosted LLM reported | J16 |
| T-GLN-07 EOIP-in-Glean | EOIP registered as a remote MCP server inside a Glean trial tenant (if one becomes available); ACLs still enforced on EOIP's side | J5 |

## 15. Risks, trade-offs, open questions

- **Risk:** buyers judge EOIP on Glean-grade search relevance and connector breadth. EOIP's in-process BM25 and hashing vectors (BL-13, BL-14) will lose a head-to-head comparison. Mitigation: a persistent vector/hybrid engine (C10) and a relevance evaluation set before any demo.
- **Risk:** Glean ships on-prem (Dell) broadly, which would weaken the "air-gap" differentiation. Track GA status quarterly.
- **Trade-off:** personalisation from activity signals collides with privacy and works-council constraints in the EU. Keep it opt-in.
- **IP flag (record only):** enterprise-search permission and knowledge-graph ranking patents by Glean were not searched (NOT PUBLICLY VERIFIED). Legal review is needed before patenting similar ranking methods.
- **Open questions:**
  1. Is the Dell on-prem offering GA, and who operates it?
  2. Is permission enforcement applied to LLM-inferred graph edges and agent memory?
  3. Is there any graph export or graph query API?
  4. Is there a self-hosted LLM option?
  5. What is the Indexing SDK licence?

---

## Appendix A — Research-dimension coverage

| Dimension | Section(s) | Summary or N/A reason |
|---|---|---|
| D1 Identity and maturity | 1 | Glean Technologies; continuous SaaS; name collision with Meta Glean resolved |
| D2 Problem and workloads | 2 | Permission-aware enterprise search, assistant, agents |
| D3 Architecture | 4, 5 | Crawler → lexical/semantic indexes + graphs → assistant/agents; Glean-operated control plane |
| D4 Storage and indexing | 5.2 | Engines NOT PUBLICLY VERIFIED; ACL-in-index hypothesis |
| D5 Schema and semantics | 5.1 | Documents + ACLs; triples with optional edge properties; no ontology |
| D6 Query pipeline | 5.3 | Hybrid retrieval, intent structuring, graph fulfilment (blog); ranking undocumented |
| D7 Reasoning | 5.4 | Statistical/LLM inference and traversal only |
| D8 Transactions and scale | 5.5, 7 | Search index, eventual consistency; no public scale figures |
| D9 Ingestion and federation | 3, 5.5 | 100+ connectors, push API, webhooks, indexed/live/hybrid |
| D10 Identity and evidence | 5.1 | Identity graph for ACLs; people pillar; evidence not exposed to customers |
| D11 Time and evolution | 5.6 | Activity history; no documented versioning or as-of |
| D12 Graph algorithms and ML | 5.1 | Entity promotion signals, LLM edge expansion; no algorithm library exposed |
| D13 Retrieval and agents | 3, 5.3 | Assistant, Agentic Engine 2, agents, MCP server and host |
| D14 NL querying | 5.3 | NL is the primary interface; no text-to-query to a customer graph |
| D15 Governance and authoring | 9 | No ontology governance; admin crawl controls |
| D16 Human experience | 2, 3 | Search UI, Assistant, browser extension |
| D17 Developer experience | 3 | Indexing SDK/API, Chat API, MCP, agent SDKs |
| D18 Trust and security | 5.7 | Query-time ACLs, single tenant, audited support access, zero retention |
| D19 Multi-tenancy and white-label | 10 | Single tenant per customer; no white-label |
| D20 Empirical economics | 7 | No benchmarks; pricing from third parties only |
| D21 Commercial and licensing | 1, 9 | Proprietary per seat plus usage-based agents |
| D22 Interoperability and lock-in | 9, INV-04 | MCP is the main open interface; no graph export found |
| D23 IP and prior art | 15 | Not searched; legal flag |
| D24 Research quality | App. C | Official docs plus engineering blog; no trial; hypotheses marked |

## Appendix B — Capability mapping

| CAP-ID | Glean | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-26 | native (100+) | CLAIM-glean-enterprise-04, -11 | BL-23 Implemented (IT-focused) | BUILD + REUSE | P1 |
| CAP-27 | partial (incremental/webhooks; replay undocumented) | CLAIM-glean-enterprise-11 | BL-24 Implemented | REUSE own | P2 |
| CAP-28 | partial (entity inference via NLP) | CLAIM-glean-enterprise-05 | BL-26 Implemented, BL-27 Partial | REUSE own | P2 |
| CAP-31 | partial (people consolidation) | CLAIM-glean-enterprise-04 | BL-34 Implemented (person), BL-36 Absent | BUILD/REUSE (C04) | P1 |
| CAP-38 | partial (edge provenance per blog, not exposed) | CLAIM-glean-enterprise-05 | BL-41 Implemented | REUSE own | P2 |
| CAP-43 | absent (not documented) | — | BL-40 Partial | BUILD | P1 |
| CAP-44 | native (SSO, OAuth 2.1 for MCP) | CLAIM-glean-enterprise-08 | BL-19 Partial | BUILD OAuth for MCP | P1 |
| CAP-46 | native | CLAIM-glean-enterprise-10 | BL-17 Implemented, **BL-18 Absent** | BUILD | **P0** |
| CAP-47 | native (single tenant per customer) | CLAIM-glean-enterprise-16 | BL-20 Partial | BUILD | **P0** |
| CAP-48 | partial (audited support access) | CLAIM-glean-enterprise-16 | Partial | BUILD | P2 |
| CAP-50 | absent (announced on-prem only) | CLAIM-glean-enterprise-01, -14 | design goal | BUILD | P1 |
| CAP-51 | partial (zero retention, BYOK; no local) | CLAIM-glean-enterprise-12, -13 | BL-45 Implemented | REUSE own | P1 |
| CAP-52 | absent | — | BL-21 Implemented | REUSE own | P2 |
| CAP-53/54/55 | native | CLAIM-glean-enterprise-05 | BL-13/14/15 Implemented/Partial | REUSE engine (C10) + BUILD fusion | P1 |
| CAP-56 | partial (graph-assisted retrieval) | CLAIM-glean-enterprise-05 | BL-16 Implemented | EXPERIMENT vs baseline | P2 |
| CAP-57 | partial (personal graph, agent memory) | CLAIM-glean-enterprise-05, -06 | BL-48 Partial | BUILD with ACL re-check | P1 |
| CAP-59 | native (server + host + gateway) | CLAIM-glean-enterprise-08, -09 | BL-47 Implemented | BUILD | P1 |
| CAP-60 | native (citations) | CLAIM-glean-enterprise-05 | BL-16 Implemented | REUSE own + abstention | P1 |
| CAP-61 | absent (not documented) | CLAIM-glean-enterprise-12 | Ollama in compose | REUSE | P1 |
| CAP-80 | partial (activity/people/process graph) | CLAIM-glean-enterprise-04, -06 | BL-56 Planned | EXPERIMENT | P3 |

## Appendix C — Evidence records

| CLAIM-ID | Product / version / date | Exact claim | Classification | Source + URL | Pub / access | Confidence | Contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-glean-enterprise-01 | Glean deployment, 2026 | Two models: Glean Hosted ("Glean uses GCP as its cloud provider") and Customer Hosted ("previously known as Cloud-Prem") in the customer's GCP or AWS; "Glean is responsible for infrastructure and application management, including upgrades, patching, and monitoring"; "Glean doesn't support manually deploying or patching the Glean services"; Customer Hosted is "Not a traditional self-hosted model"; no on-prem or air-gap mentioned | Officially documented | Glean docs, Glean deployment models: https://docs.glean.com/get-started/prepare/about-deployment | undated / 2026-10-18 | 0.85 | The page's own "next steps" section calls it "self-hosted in your own cloud" (inconsistent wording); Dell on-prem announcement (CLAIM-14) |
| CLAIM-glean-enterprise-02 | same | "Glean maintains support access to your environment for debugging and support purposes" (all models) | Officially documented | same | undated / 2026-10-18 | 0.85 | — |
| CLAIM-glean-enterprise-03 | same | Glean Hosted "available in multiple GCP and AWS regions"; Customer Hosted gives "Full data residency guarantees" | Officially documented | same | undated / 2026-10-18 | 0.8 | — |
| CLAIM-glean-enterprise-04 | Knowledge Graph, 2026 | Knowledge Graph "organizes your enterprise's indexed information in real time"; pillars are content, people, activity; 100+ connectors; crawler does content analysis, metadata extraction, permissions management, facets; admins configure item-level access; activity data "never leaves your exclusive GCP project" | Officially documented | Glean docs, Knowledge Graph: https://docs.glean.com/security/knowledge-graph | undated / 2026-10-18 | 0.85 | — |
| CLAIM-glean-enterprise-05 | Glean engineering blog, 2025-06-27 | Entities from NLP noun-phrase extraction with statistical filtering; promotion signals; edges as (subject, predicate, object) triples kept on "strong, repeatable" evidence; edge properties may include "timestamps, access control, confidence scores, or provenance"; LLMs expanded the graph; personal graph groups actions into tasks/themes; crawler "powers both semantic and lexical search"; intent is converted to a structured form and executed against the graph | Officially documented (vendor engineering blog) | Glean blog, How knowledge graphs work and why they are the key to context for enterprise AI: https://www.glean.com/blog/knowledge-graph-agentic-engine | 2025-06-27 / 2026-10-18 | 0.7 (blog, not reference docs) | — |
| CLAIM-glean-enterprise-06 | Glean:LIVE, 2025-09-25 | Enterprise Graph extends the Knowledge Graph to projects, processes, data (GA); Personal Graph introduced May 2025 (GA); Agentic Engine 2 GA for Assistant only; beta: remote MCP servers, conversational agent builder, agent toolkit; coming soon: Canvas, model choice, MCP directory; scheduled agents and Deep Research usage-priced; author notes 200–300 apps in mid-size firms, mostly read-only integrations, Slack API restriction | Third-party report | Reworked, Glean thinks its AI understands your company better than you do: https://www.reworked.co/knowledge-findability/glean-thinks-its-ai-understands-your-company-better-than-you-do/ | 2025-09-29 / 2026-10-18 | 0.6 (trade press summarising vendor announcements) | Glean press page states no availability status |
| CLAIM-glean-enterprise-07 | Glean press, 2025-09-25 | Third-generation Glean Assistant and new Enterprise Graph, new SDKs and MCP support for agent building | Officially documented (press) | Business Wire: https://www.businesswire.com/news/home/20250925784461/en ; Glean press: https://www.glean.com/press/glean-introduces-third-generation-ai-assistant-new-enterprise-graph-to-enable-the-superintelligent-enterprise | 2025-09-25 / 2026-10-18 | 0.65 | — |
| CLAIM-glean-enterprise-08 | Glean MCP server, 2026 | Remote MCP server exposing Search, Chat, Read Document, Code Search, People, Artifacts, image generation, Glean agents as tools, plus external tools via MCP Gateway; permissions enforced via the Knowledge Graph ("strict user-level access control"); OAuth 2.1 + PKCE recommended; 22 hosts listed incl. Claude Code, Cursor, VS Code, ChatGPT | Officially documented | Glean docs, About Glean MCP server: https://docs.glean.com/administration/platform/mcp/about | undated / 2026-10-18 | 0.85 | — |
| CLAIM-glean-enterprise-09 | Remote MCP in Glean | "Glean fully supports remote MCP servers in Glean and currently offers beta support for servers in agents" | Officially documented | Glean docs, Connect remote MCP servers to Glean: https://docs.glean.com/administration/tools/connect-remote-mcp-servers-to-glean | undated / 2026-10-18 | 0.75 (search extract) | — |
| CLAIM-glean-enterprise-10 | Glean Indexing SDK | "Glean enforces permissions at query time"; `DocumentPermissionsDefinition` with `allowed_users`, `allowed_groups`, `allowed_group_intersections`; identity graph via `get_identities()`; groups require memberships, else `InconsistentDataError`; do not flatten groups; test harness asserts forbidden identities are absent from ACLs | Officially documented | Glean developers, Indexing SDK permissions: https://developers.glean.com/libraries/indexing-sdk/permissions | undated / 2026-10-18 | 0.85 | — |
| CLAIM-glean-enterprise-11 | Connectors, 2026 | Connector types: native, web history, push API (Indexing API), partner, tools/MCP (live access, not searchable); changes captured "often through webhooks or incremental crawling"; connectors "fetch the permissions map from each source"; indexed, live or hybrid access | Officially documented | Glean docs, About Connectors: https://docs.glean.com/connectors/about | undated / 2026-10-18 | 0.85 | — |
| CLAIM-glean-enterprise-12 | LLM availability, 2026 | Universal Model Key (formerly Glean Key) vs Customer Key; OpenAI and Azure OpenAI on GCP and AWS deployments; Vertex AI with Universal Key or GCP Customer Key; Bedrock with Universal Key or AWS Customer Key; Claude via Vertex or Bedrock; Customer Key defaults must come from one provider | Officially documented | Glean docs, Feature availability by LLM key, provider, and cloud: https://docs.glean.com/administration/llm-key-feature-availability | undated / 2026-10-18 | 0.75 (search extract) | Older "Supported LLMs" page differs on Glean-key options |
| CLAIM-glean-enterprise-13 | Glean Protect | Zero LLM data retention; no training of LLMs on enterprise data | Officially documented | Glean docs, About Glean Protect and Protect+: https://docs.glean.com/administration/protect/overview | undated / 2026-10-18 | 0.7 (search extract) | Slack marketplace listing ties 0-day retention to the default Glean Key path |
| CLAIM-glean-enterprise-14 | Glean + Dell, 2025-05-20 | Collaboration "to deliver the first on-premises deployment architecture for Glean's Work AI platform" on Dell AI Factory infrastructure; enterprises can "deploy Glean's enterprise search and AI agents within their own data centers"; no availability date, LLM, operator or air-gap details stated | Officially documented (press release; GA unverified) | Business Wire: https://www.businesswire.com/news/home/20250520211371/en ; Reworked wire copy: https://www.reworked.co/the-wire/glean-delivers-ai-agents-and-enterprise-search-to-on-premises-environments-in-collaboration-with-dell-technologies/ | 2025-05-20 / 2026-10-18 | 0.6 for the announcement; 0.3 that it is generally available | Current deployment docs (CLAIM-01) list no on-prem model |
| CLAIM-glean-enterprise-15 | Pricing | No public price list; third-party estimates of ~$30–75/user/month, ~100-seat minimum, Vendr-cited median ~$98.9k/yr | Unverified (third-party, partly competitor sources) | Workativ: https://workativ.com/blog/glean-pricing ; GoSearch: https://www.gosearch.ai/blog/glean-pricing-explained ; Macha: https://www.getmacha.com/blog/glean-ai-pricing-explained | 2026 / 2026-10-18 | 0.25 | Figures vary widely |
| CLAIM-glean-enterprise-16 | Glean help center | Tenant is hosted in an isolated single tenant; support engineers need approval and receive a 1-hour time-bound token; access audited | Officially documented | Glean Help Center, Glean deployment options: https://help.glean.com/en/articles/10093412-glean-deployment-options | undated / 2026-10-18 | 0.7 (search extract) | — |
| CLAIM-glean-enterprise-17 | Gartner recognition, 2026 | Glean named a Market Shaper in Gartner's 2026 Emerging Market Quadrant for No-Code Agent Builders | Officially documented (vendor press) | Glean press: https://www.glean.com/press/gartner-emerging-market-quadrant-for-no-code-agent-builders-startup-vendors | 2026-06 / 2026-10-18 | 0.6 | — |
| CLAIM-glean-enterprise-18 | Name collision | "Glean" also names Meta's open-source code-indexing system; researched in C15 by W27 | Reasoned inference (Master Prompt §5.7) | Master Prompt §5.7 (internal) | — / 2026-10-18 | 0.9 | — |
| CLAIM-glean-enterprise-19 | OneDrive connector | Uses Graph delta queries and webhooks for permission-change notifications | Officially documented | Glean docs, OneDrive connector: https://docs.glean.com/connectors/native/onedrive | undated / 2026-10-18 | 0.6 (search extract) | — |

## Appendix D — Assumptions

1. "Glean" in the registry means Glean Technologies' enterprise SaaS. Meta's Glean belongs to W27.
2. GA statuses from Glean:LIVE 2025 are taken from Reworked's table, because the Glean press page does not state availability.
3. The Dell on-prem architecture is treated as announced, not GA, because the current deployment docs omit it.
4. No Glean trial was performed. Internals are hypotheses where marked.
5. Pricing figures are recorded only as Unverified context.
