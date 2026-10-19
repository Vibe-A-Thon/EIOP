# C07 — Microsoft Graph, Microsoft 365 Copilot connectors, and Microsoft Fabric graph / ontology (Fabric IQ)

| Field | Value |
|---|---|
| Registry ID | T-C07-microsoft-graph-copilot-fabric |
| Tier | A. This is the comparison buyers make by default: most EOIP prospects already pay for Microsoft 365, and many also run Fabric. |
| Versions examined | Microsoft Graph v1.0 REST (Learn overview, updated 2026-04-16). Microsoft 365 Copilot connectors: overview updated 2026-10-12, prerequisites/licensing 2026-09-25, Graph connector agent page 2026-09-22. Semantic indexing for Copilot (updated 2026-08-18). Graph in Microsoft Fabric: overview 2026-06-26, how-it-works and limitations 2026-09-29; GA announced 2026-06-02. Fabric IQ ontology (preview): overview ms.date 2026-10-16. Work IQ API: GA 2026-06-16. All SaaS, so there are no customer-visible version numbers; docs are pinned by git commit in Appendix C. |
| Verified on | 2026-10-18 |
| Worker | W17 |

---

## 1. Identity, current status, tier, and sources

**What the entry covers.** "Microsoft graph / ontology" is not one product. It is several layers, each with a different shipping status:

| Layer | Exact current name | Status on 2026-10-18 | Evidence |
|---|---|---|---|
| M365 data API | **Microsoft Graph** (REST, `graph.microsoft.com`), plus **Microsoft Graph Data Connect** for bulk export to Azure | GA, mature | [CLAIM-microsoft-graph-copilot-fabric-23] |
| External-content ingestion | **Microsoft 365 Copilot connectors**, formerly "Microsoft Graph connectors". Two kinds: *synced* (indexed) and *federated* (live, MCP-based) | Synced: GA. Federated: available, read-only, with write actions "starting early October 2026" | [CLAIM-…-16], [CLAIM-…-17] |
| Retrieval index | **Semantic indexing for Microsoft Copilot** (lexical plus vector index over Graph content) | GA, enabled automatically, cannot be disabled | [CLAIM-…-22] |
| Agent API onto M365 context | **Work IQ API** (Chat, Context and Tool APIs) | GA 2026-06-16, billed in Copilot Credits | [CLAIM-…-25] |
| Analytical graph engine | **Graph in Microsoft Fabric** (LPG, GQL ISO/IEC 39075, scale-out) | **GA**, announced at Build on 2026-06-02. NL2GQL through Fabric Data Agent is still **preview** | [CLAIM-…-01], [CLAIM-…-11], [CLAIM-…-29] |
| Semantic / ontology layer | **Fabric IQ**, with its **ontology (preview)** item | Fabric IQ umbrella: **GA** (Build 2026). Ontology item: **still preview** on 2026-10-16, with Microsoft saying GA is "expected … in the coming months". The old ontology experience retires 2027-01-31 | [CLAIM-…-02], [CLAIM-…-03] |

In this file `CLAIM-…-NN` is short for `CLAIM-microsoft-graph-copilot-fabric-NN`.

**Trap resolution (Master Prompt §5.7, "verify what has shipped vs announced").** Graph in Fabric has shipped (GA). Fabric IQ as a brand is GA. The **ontology item has not reached GA**; it is preview with a new experience, and the earlier preview experience is being deprecated. Fabric IQ's surfaces inside Microsoft 365 Copilot (Cowork, Copilot Chat) were limited to "Frontier" programme customers when Build 2026 announced them [CLAIM-…-02]. One third-party claim that the Copilot integration reached GA on 2026-09-28 could not be confirmed from a Microsoft source and is recorded as UNVERIFIED [CLAIM-…-33].

**Owner.** Microsoft Corporation. Every layer is proprietary SaaS, billed per user (M365 / Copilot add-on / E7), per Fabric capacity unit (CU), or per Copilot Credit.

**Sources used.** 19 primary and secondary sources, listed in Appendix C: Microsoft Learn pages pinned by git commit, the Azure blog, the Microsoft licensing site, Techzine, Computer Weekly, The Next Web, and community material.

## 2. Primary problem, target workloads, concrete example workflows

Microsoft's stack answers one question: "ground AI assistants and analysts in the organisation's data without leaving the Microsoft cloud." It comes from two directions:

1. **Work-graph direction (M365).** People, mail, meetings, files, Teams chats and org chart live in Microsoft Graph. Copilot connectors pull in external systems (Jira, Confluence, ServiceNow, Salesforce, SAP, file shares, SQL/Oracle) as *external items*, each with an ACL [CLAIM-…-17], [CLAIM-…-18]. The semantic index vectorises that content, and Copilot grounds prompts on it under the user's identity [CLAIM-…-22].
2. **Data-estate direction (Fabric).** Structured data sits in OneLake. The Fabric IQ ontology names business concepts and binds them to tables, semantic models, eventhouses and so on [CLAIM-…-04]. Graph in Fabric materialises an LPG from lakehouse tables for multi-hop GQL [CLAIM-…-11], [CLAIM-…-13]. Data agents and operations agents consume the result.

**Example workflows (documented behaviour):**
- *"Summarise the Contoso deal."* Copilot Chat retrieves a Salesforce record ingested by a synced connector and cites it [CLAIM-…-17].
- *Help-desk ticket index.* A custom connector `PUT`s `/external/connections/contosohelpdesk/items/SR00145` with properties, content and an ACL. Deny overrides grant, and non-Entra groups are mirrored as *external groups* [CLAIM-…-18].
- *Supply-chain reachability.* Model node and edge types over lakehouse tables, press **Save** (a full load), then run bounded variable-length or `ANY SHORTEST` GQL in the code editor or through REST [CLAIM-…-13], [CLAIM-…-14].
- *Semantic-model reuse.* Generate an ontology from a Power BI semantic model so that DAX measures appear as ontology *metrics*, then let a data agent answer with those metrics instead of improvising formulas [CLAIM-…-06].

**How this maps to the EOIP reference questions (§4.4).** Microsoft can find documents *about* service account "abc" (semantic index plus connectors). Entra ID through Graph knows the account's group memberships and app-role assignments [CLAIM-…-24]. No layer documents a **cross-source dependency graph** linking that account to code, pipelines, deployments and incidents with evidence spans. To get that, a customer would have to model and load it into Graph in Fabric themselves (§11).

**Suitability for on-prem / local-first.** Poor (§10). Every layer runs in Microsoft's cloud. Even the on-prem connector agent needs outbound internet to Microsoft endpoints [CLAIM-…-21].

## 3. Feature inventory

| Capability | M365 Graph + connectors + semantic index | Fabric graph | Fabric IQ ontology | Notes |
|---|---|---|---|---|
| Unified REST API over M365 entities and relationships | Present (OData resources, navigation `manager`, `memberOf`) | — | — | [CLAIM-…-23] |
| Bulk export of M365 data | Present (Graph Data Connect → Azure Data Factory) | — | — | [CLAIM-…-23] |
| Prebuilt external connectors | Present: "over 100" | Sources limited to OneLake + mirrored DBs | Bindings to Fabric sources only | [CLAIM-…-17], [CLAIM-…-14], [CLAIM-…-04] |
| Custom connector SDK/API | Present (Graph connectors API, M365 Agents Toolkit) | — | Ontology APIs and CI/CD | [CLAIM-…-17], [CLAIM-…-08] |
| Live / federated retrieval (no index) | Present (federated connectors via MCP; Copilot add-on required) | — | Virtual bindings query the live source | [CLAIM-…-16], [CLAIM-…-19], [CLAIM-…-04] |
| Per-item ACL with deny and external groups | Present | NOT PUBLICLY VERIFIED at graph-element level | Inherits source RLS/OLS/CLS | [CLAIM-…-18], [CLAIM-…-31], [CLAIM-…-08] |
| Full-text and vector (semantic) index | Present, automatic, cannot be disabled | No `VECTOR` value type | — | [CLAIM-…-22], [CLAIM-…-14] |
| LPG storage and query | — | Present (GQL, ISO/IEC 39075 subset) | Schema graph; optional materialisation | [CLAIM-…-11], [CLAIM-…-10] |
| GQL DML / DDL | — | **Absent** | — | [CLAIM-…-14] |
| Incremental structural refresh | — | **Absent** (Save reloads everything) | — | [CLAIM-…-13] |
| Graph algorithms | — | Present (claimed "built-in graph analytics algorithms"; catalogue not examined) | — | [CLAIM-…-11] |
| NL → query | Copilot (no inspectable query) | NL2GQL, **preview**, via Data Agent | Ontology agent (preview, proposal-first) | [CLAIM-…-29], [CLAIM-…-09] |
| Ontology modelling (entity types, inheritance, namespaces, shared properties) | — | — | Present (preview) | [CLAIM-…-04] |
| RDF/Turtle/OWL import/export | — | — | Present (preview), with a preserved/adjusted/unsupported report | [CLAIM-…-05] |
| Formal reasoning (OWL/RDFS/SHACL) | Absent | Absent | **Absent**: "rules" are natural-language statements | [CLAIM-…-06] |
| Versioning | — | — | Manual named versions; restore replaces the whole definition | [CLAIM-…-07] |
| Bitemporal / as-of queries | Absent | Absent | Absent | Reasoned from docs [CLAIM-…-14] |
| Result / graph export | — | **Absent** | RDF/Turtle export of definitions only | [CLAIM-…-14], [CLAIM-…-05] |
| MCP / agent interface | Federated connectors use MCP; Work IQ API (MCP/A2A per third-party report) | — | Fabric IQ as MCP tool in Agent 365 (preview) | [CLAIM-…-16], [CLAIM-…-25], [CLAIM-…-32] |
| On-prem / air-gap | Absent (connector agent needs the internet) | Absent | Absent | [CLAIM-…-21], [CLAIM-…-26] |
| White-label / OEM | Absent | Absent | Absent | Reasoned (first-party SaaS) |

## 4. Text-based architecture diagram

```
 ┌──────────────────────────── Microsoft cloud (customer tenant, Microsoft-operated) ───────────────────────────────┐
 │ Copilot connectors service (gcs.office.com)                                                                      │
 │  synced:    crawl → externalItem{id, properties(schema), content(text|html), acl[grant|deny], activities}        │
 │             → Microsoft Graph index → semantic index (lexical + vectors; tenant & user level)                    │
 │  federated: MCP fetch at query time (OAuth on behalf of user; nothing indexed)                                   │
 │        ▲ External SaaS (Jira, ServiceNow, Salesforce, SAP …)                                                     │
 │        ▲ Graph connector agent (Windows service on-prem; outbound 443 to *.office.com, graph, Service Bus)       │
 │                                                                                                                  │
 │ M365 workloads (Exchange, SharePoint, Teams, Entra) ── Microsoft Graph REST (graph.microsoft.com)               │
 │        delegated perms = app scopes ∩ user rights; application perms = tenant-wide                               │
 │ Copilot orchestrator: prompt → Graph + semantic index grounding → Microsoft-hosted LLM → post-process → app      │
 │ Work IQ API (Chat / Context / Tool) → custom and 3rd-party agents (Copilot Credits)                              │
 │                                                                                                                  │
 │ ── Fabric capacity (CU) ──────────────────────────────────────────────────────────────────────────────────────── │
 │ OneLake (Delta tables, mirrored DBs, shortcuts) ◄── pipelines / mirroring                                        │
 │    │ Save = full load                 ▲ live bound queries                                                       │
 │    ▼                                  │                                                                          │
 │ Graph in Fabric: node/edge types → table mappings → read-optimised sharded graph (graph cache ≥100 GB)           │
 │    → GQL engine ◄ Query Builder / code editor / REST GQL API / NL2GQL (Data Agent, preview)                      │
 │    ▲ optional materialisation                                                                                    │
 │ Fabric IQ ontology (preview): entity types, relationships, metrics (DAX-owned), NL rules, namespaces, bindings   │
 │    → data agents, operations agents, Real-Time Dashboards, Foundry (preview), Agent 365 (preview)                │
 │ Control plane: Entra ID, workspace/item roles, OneLake security (RLS/CLS/OLS), Purview, capacity metrics app     │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**State.** Connector items and vectors live in the M365 substrate in the tenant's region [CLAIM-…-22]. The Fabric graph is a *copy* of OneLake tables, read-optimised and rebuilt on Save [CLAIM-…-13]. The ontology stores only definitions and bindings [CLAIM-…-04]. **Control plane:** Entra ID, workspace and item permissions, admin centre. **Data plane:** crawl → index → retrieve, and OneLake → graph cache → GQL.

## 5. Under-the-hood reconstruction

Every internal below is either *documented* (cited) or a *hypothesis*. Microsoft publishes no storage or engine internals for the semantic index or for Graph in Fabric.

### 5.1 Data model
- **Microsoft Graph**: an OData entity model. Typed resources (`user`, `group`, `driveItem`, `event`, `message` …) with navigation properties (`manager`, `memberOf`, `members`, `lastModifiedByUser`) [CLAIM-…-23]. This is a *virtual* graph over service-owned stores, not a graph database. Traversal is client-driven, one REST hop at a time.
- **External items**: `externalItem{ id (source PK), properties (typed by a registered schema), content {type: text|html}, acl [{type: user|group|everyone|externalGroup, value, accessType: grant|deny}], activities[] (write-only) }` [CLAIM-…-18]. No relationship type between external items is documented, so connector content is a **flat document set with ACLs**, not a graph.
- **Fabric graph**: an LPG with node and edge types mapped to tables. Property types are BOOLEAN, INT64, DOUBLE, FLOAT, STRING (≤65,535 B) and ZONED DATETIME. No nested types, no VECTOR. One graph type per catalog. Auto-generated graph and constraint names [CLAIM-…-14].
- **Ontology**: entity type → properties, identifiers (keyless types allowed), relationships (join tables optional), inheritance, shared properties, namespaces, metrics (references to DAX measures), rules (natural-language text), bindings (source structure ↔ concept) [CLAIM-…-04], [CLAIM-…-06].

### 5.2 Storage layout and indexing
- *Semantic index*: "vectorized indices … billions of vectors". Tenant-level content comes from SharePoint text files reachable by ≥2 users and from connector data; user-level content from the mailbox. New tenant documents are indexed daily, and edits "immediately" [CLAIM-…-22]. ANN algorithm, embedding model and dimensionality: **NOT PUBLICLY VERIFIED**.
- *Fabric graph*: "scale-out sharding across multiple machines"; "read-optimized, queryable graph"; storage billed as OneLake Cache with a 100 GB minimum; ~2 billion element ceiling; `uint64` raw node and edge IDs; `uint16` length caps on strings, lists and paths [CLAIM-…-11], [CLAIM-…-12], [CLAIM-…-14]. *Hypothesis*: a CSR-like per-shard adjacency built offline from Delta files. The full rebuild on schema change and the read-only GQL surface fit an immutable, bulk-built structure, but the layout is not documented.

### 5.3 Query pipeline
- GQL subset: MATCH / OPTIONAL MATCH, WHERE, LET, FOR, NEXT, GROUP BY, ORDER BY, LIMIT/OFFSET, UNION, CALL subqueries. Path prefixes are `ALL` and `ANY SHORTEST` only. Unbounded `ANY SHORTEST WALK` returns reachability or length without materialising the path. Results are truncated at 64 MB, intermediates capped at 128 MB, and the API times out at 20 minutes. **No `$param` dynamic parameters** [CLAIM-…-14]. EXPLAIN/PROFILE: NOT PUBLICLY VERIFIED.
- Without parameters, programmatic callers have to build GQL strings. That is a query-injection surface for agent-generated queries; EOIP's typed QueryPlan (BL-08) does not have it.

### 5.4 Reasoning
None in the formal sense. Ontology "rules" are natural-language context for LLM consumers [CLAIM-…-06]. Inheritance is a modelling convenience; no subsumption reasoning or validation is documented. OWL import reports elements as "unsupported" or "automatically adjusted", which implies a lossy mapping [CLAIM-…-05].

### 5.5 Concurrency, transactions, partitioning, consistency
Fabric graph is read-only through GQL. Writes happen only through reload or refresh from OneLake, so a transactional model does not apply. Consistency is snapshot-at-load: the graph is only as fresh as its last load, which can take hours for large graphs [CLAIM-…-13], [CLAIM-…-14]. The connector index is eventually consistent (incremental or full crawls; scheduled or event-based push) [CLAIM-…-18].

### 5.6 Caching and versioning
Graph "automatically shut[s] down when not in use"; billing is per CPU-uptime second, rounded to minutes [CLAIM-…-12]. Ontology versions are manual checkpoints whose restore overwrites the current definition [CLAIM-…-07]. Neither has semantic diff, branch/merge, or instance-level as-of queries.

### 5.7 Security
- Graph API: delegated permissions = app scopes ∩ the signed-in user's rights. Application permissions grant tenant-wide access ("can read any file"). Resource-specific consent covers a subset (Teams, chats) [CLAIM-…-24].
- Connector ACL: evaluated against Entra identities; deny wins; non-Entra principals must be translated to Entra users [CLAIM-…-18]. Search and Copilot "only show items to users who have access in the source system" [CLAIM-…-17].
- Ontology: honours OneLake security and source RLS/OLS/CLS [CLAIM-…-08]. **Graph in Fabric**: the docs only say it is "governed by Fabric OneLake security, compliance, and permission model". Whether source row-level security carries through to graph elements after materialisation is **NOT PUBLICLY VERIFIED** [CLAIM-…-31].

### 5.8 Re-implementation blueprint (equivalent behaviour, EOIP-native)

```
# connector item → governed event (EOIP already has SourceEvent v2 + PermissionMetadata, BL-17/BL-23)
on_crawl(item):
    emit(SourceEvent(source, native_id=item.pk, payload=item.body,
         permissions=PermissionMetadata(grants=map(item.allow), denies=map(item.deny),
                                        external_groups=item.groups)))   # never write the graph directly

# retrieval with Microsoft-equivalent trimming (closes BL-18), then exceed it at graph hops
def retrieve(query, principal):
    groups = expand_groups(principal)            # cached; invalidated by group-change events
    cands  = hybrid_search(query, k=200)         # BM25 + dense + RRF (BL-13..15)
    return [c for c in cands if acl_allows(c.acl, principal, groups)][:k]   # deny > grant

# ontology binding without copying (Fabric IQ-like) → EOIP mapping IR (BL-33) + federation planner (BL-51)
Concept("Customer").bind(source="warehouse.dim_customer", key="cust_id", props={...}, mode="virtual")
```

## 6. Functional and non-functional requirements inferred from verified behaviour

| ID | Inferred requirement (Microsoft's design) | Evidence | EOIP implication |
|---|---|---|---|
| FR-1 | Every indexed item carries an ACL with grant/deny and group indirection; deny has precedence | [CLAIM-…-18] | Floor for EOIP (BL-17 captured, BL-18 absent) |
| FR-2 | Non-IdP groups replicated as first-class external groups instead of being expanded per item | [CLAIM-…-18] | Adopt: avoids ACL write amplification |
| FR-3 | Two retrieval modes: indexed, and federated live fetch for sensitive or volatile sources | [CLAIM-…-16] | EOIP federation planner (BL-51, Partial) |
| FR-4 | Ontology is a virtual binding layer; graph materialised only when traversal needs it | [CLAIM-…-10] | Supports EOIP's hybrid virtualise/materialise direction (OBDA seed hypothesis) |
| FR-5 | Business metrics stay owned by their source (DAX), referenced by the ontology | [CLAIM-…-06] | Reference, don't duplicate, metric logic |
| FR-6 | AI ontology edits are proposal-first and human-reviewed | [CLAIM-…-09] | Already EOIP doctrine (BL-40) |
| NFR-1 | Graph up to ~2 B elements; loads of several hours | [CLAIM-…-14] | Sets the scale buyers will quote |
| NFR-2 | Query timeout 20 min; result cap 64 MB | [CLAIM-…-14] | EOIP should publish comparable bounded-plan limits |
| NFR-3 | Index data stays in tenant region; EUDB honoured | [CLAIM-…-22] | EOIP meets this trivially on-prem |

## 7. Performance and resource model

- **No independent benchmark** of Graph in Fabric, the semantic index, or connector throughput was found. Microsoft states no latency figures. "Analyze billions of relationships without slowdowns" is a **vendor claim** with no workload or hardware stated [CLAIM-…-11] and is classified Unverified.
- **Documented resource facts.** Graph billing is 10 CU-seconds per uptime second, with a 100 GB storage minimum and a ~2 B element ceiling. Large loads can take "several hours", and loads unfinished after 24 h go to support [CLAIM-…-12], [CLAIM-…-14]. The connector agent needs 8 cores, 16 GB RAM, and 40 GB disk for 5 M items plus 9 GB per extra million; it handles ≤3 connections per agent [CLAIM-…-21]. Index quota is 50 M items per tenant (confidence 0.6) [CLAIM-…-20].
- **Scaling behaviour (reasoned).** Freshness gets worse as the graph grows, because any structural change forces a full reload [CLAIM-…-13]. Cost scales with CU uptime, not query count, so sporadic interactive use pays for minute-rounded sessions [CLAIM-…-12].
- **Failure modes.** Silent truncation (warning only, no continuation token). 20-minute timeout. Load failure past 24 h. The connector agent goes "offline" when outbound 443 is blocked, which happens by design in an air gap [CLAIM-…-14], [CLAIM-…-21].
- **Uncertainty.** High. Internals are proprietary and no trial was run.

## 8. Strengths and use-case-specific advantages, and how to match or exceed

1. **Zero-setup distribution.** Copilot, the semantic index and M365 content ACLs already sit in tenants EOIP prospects own; the index is "automatically enabled" [CLAIM-…-22]. *Match?* Distribution cannot be matched. *Integrate:* ingest M365 through Graph as an EOIP source, and optionally expose EOIP evidence to Copilot through a federated (MCP) connector, so EOIP becomes a provider into Copilot rather than a competitor to it.
2. **A mature ACL model on external items** (grant/deny, external groups, Entra mapping) [CLAIM-…-18]. *Exceed:* EOIP enforces ACLs on **graph traversals and derived facts**, not only on documents (INV-03).
3. **Federated or synced, chosen per source** [CLAIM-…-16]. *Match:* EOIP federation planner (BL-51) with a per-source "never index" policy.
4. **Standards-based graph query (GQL) at large scale** [CLAIM-…-11]. *Match:* QueryPlan → GQL/Cypher compilation (BL-09 Partial today).
5. **Ontology bound to existing BI semantics** (DAX metrics) [CLAIM-…-06]. *Integrate:* an EOIP binding type that references external metric definitions (Power BI / dbt semantic layer).
6. **RDF/OWL import with a loss report** [CLAIM-…-05]. *Match/exceed:* extend EOIP's JSON-LD loss accounting (BL-31) to Turtle/OWL, with W3C test evidence.

## 9. Limitations with root causes

**Verified defects / documented limits**
- GQL is read-only: no DML or DDL [CLAIM-…-14].
- No incremental structural change: Save reloads the whole graph [CLAIM-…-13].
- No result export, no direct Power BI connection, no `$param` parameters, no VECTOR type, no `ALL SHORTEST` [CLAIM-…-14].
- Graph sources limited to OneLake and mirrored databases [CLAIM-…-14].
- Ontology still preview, the old experience is being retired, and migration requires re-creating rules and reconnecting consumers [CLAIM-…-03].
- Federated connectors were read-only until write actions began in October 2026 [CLAIM-…-16].

**Intentional trade-offs**
- Natural-language ontology "rules" are cheap to author and impossible to verify [CLAIM-…-06].
- Snapshot graph instead of a transactional store [CLAIM-…-13].

**Licensing restrictions**
- Copilot grounding on connector data needs the Copilot add-on or E7. Federated connectors need a Copilot add-on for every querying user [CLAIM-…-19].
- Work IQ is metered in Copilot Credits [CLAIM-…-25].

**User-reported / third-party complaints**
- Azure Local disconnected was criticised for shipping preview-grade AKS under a GA label (Computer Weekly opinion) [CLAIM-…-30].
- Fabric in GCC High lacks parity and does not cover DoD [CLAIM-…-28].

**Outdated claims to avoid**
- "Graph connectors" is an old name.
- Per-licence connector quotas were replaced by a tenant-wide 50 M quota in 2024 [CLAIM-…-20].
- "Every ontology automatically materialises an instance graph" is the earlier framing, which Microsoft now explicitly replaces [CLAIM-…-10].

**Root causes**
- *Algorithmic dead-ends:* none proven. Read-only GQL plus full reload *suggest* a bulk-built immutable layout (hypothesis), which is a dead end for living-graph mechanics (Master Prompt §4.3.5).
- *Operational / hardware overhead:* multi-hour reloads; 100 GB storage minimum; CU billing by uptime; a Windows-only connector agent with ≤3 connections and mandatory outbound internet [CLAIM-…-21].
- *User / developer friction:* overlapping brands (Graph, Copilot connectors, Fabric IQ, Work IQ); preview churn on the ontology; graph and ontology are separate items with separate refresh behaviour; natural-language rules cannot be tested.

## 10. Deployment, licensing, redistribution, and operational viability under EOIP constraints

| EOIP constraint | Microsoft position | Verdict |
|---|---|---|
| Self-hosted / air-gap | All layers are Microsoft-cloud SaaS. The connector agent needs outbound 443 to `*.office.com`, `graph.microsoft.com` and Service Bus [CLAIM-…-21]. **Sovereign/disconnected offerings exist but exclude these layers.** Azure Local disconnected operations and Microsoft 365 Local Disconnected were reported GA in February 2026; M365 Local covers **Exchange Server, SharePoint Server and Skype for Business Server** [CLAIM-…-26], [CLAIM-…-27]. No Microsoft source found states that Copilot, Microsoft Graph, the semantic index, Fabric graph or Fabric IQ run disconnected. Foundry Local runs models offline [CLAIM-…-26]. | **Not air-gap viable** |
| Government clouds | The connector agent documents GCC, GCC High and DoD endpoint configurations [CLAIM-…-21]. Fabric in GCC High: preview 2026-09-02, GA 2026-10-01, no DoD, partial features (third-party) [CLAIM-…-28]. Graph-in-Fabric in GCC High: UNVERIFIED. | Partial (still cloud) |
| Data egress / LLM policy | Microsoft-hosted LLM. Prompts are not used to train foundation models; EUDB applies [CLAIM-…-22]. A customer cannot pick a local model for Copilot grounding. | Incompatible with the default-local policy |
| Backend neutrality | Fabric graph engine only; OneLake only | Lock-in |
| White-label / OEM | Not offered (first-party SaaS) | Not embeddable |
| Redistribution | Proprietary; usage under Microsoft product terms and the Microsoft APIs Terms of Use [CLAIM-…-23]. Nothing to redistribute. Integrating *with* the Graph and connectors APIs is the lawful route. | **Legal-review trigger:** API terms of use for any EOIP connector that reads M365 or writes external items |

**Seed inversion (Master Prompt §10.5, "SaaS or heavyweight deployment, vendor lock-in, limited on-prem/air-gap").** **VALIDATED** for this entry, with one qualification.
- *SaaS / limited air-gap:* **proven** (documented cloud endpoints; no disconnected Copilot or Fabric).
- *Lock-in:* **proven** for storage and engine (OneLake-only graph sources, no graph result export). **Partly mitigated** by RDF/Turtle ontology export [CLAIM-…-05].
- *"Heavyweight": partially rejected.* For a customer already on M365 and Fabric there is nothing to install. EOIP has to win on air-gap, evidence and permission depth, not on setup effort.

## 11. Competitive delta against the EOIP verified baseline

| Area | Microsoft | EOIP baseline | Delta |
|---|---|---|---|
| Source-ACL enforcement in retrieval and answers | Documented and enforced for connector items and M365 content [CLAIM-…-17], [CLAIM-…-18], [CLAIM-…-22] | **BL-18 Absent** (BL-17 captures metadata only) | **Competitive deficit, P0.** Microsoft is ahead on the most basic trust property |
| Connector breadth | 100+ prebuilt plus partners [CLAIM-…-17] | 30+ connectors emitting SourceEvent v2 (BL-23) | Deficit in breadth. EOIP leads on replay, DLQ and idempotency (BL-24), which Microsoft does not document beyond crawl modes |
| Relationship graph across sources | Flat external items; a separate Fabric graph hand-modelled from OneLake | Profiler with relationship discovery (BL-26), deterministic identity (BL-34), code graph (BL-42) | **EOIP differentiator** for J1, J9, J10 |
| Living graph / incremental | Full reload on structural change [CLAIM-…-13] | Revisions, tombstones, replay, bitemporal (BL-24, BL-25, BL-37) | **EOIP differentiator** (J7, J2) |
| Evidence and epistemic separation | Copilot cites sources; no claim/contradiction model documented | Claims and contradictions (BL-39), epistemic boundary (BL-40), evidence manifests (BL-41) | **EOIP differentiator** |
| Ontology | Preview; NL rules; manual versions; RDF/OWL import [CLAIM-…-03], [CLAIM-…-05], [CLAIM-…-06], [CLAIM-…-07] | LPG manifest, SHACL subset (BL-29), OWL subset (BL-30), GitOps change records (BL-32 Partial) | Roughly level on maturity. EOIP has executable validation; Microsoft has better BI-semantic alignment and UX |
| Standard query | GQL subset, GA [CLAIM-…-14] | QueryPlan templates (BL-08); GQL transpiler subset off the production path (BL-09, BL-59) | Deficit for analyst-facing querying |
| NL query | NL2GQL preview; Copilot is opaque | Deterministic suggestion engine shows candidate queries first (BL-11) | **EOIP differentiator** for J11 |
| Air-gap / local LLM | Not available [CLAIM-…-26] | Ollama in compose; egress gateway S0 default (BL-45) | **EOIP differentiator** (J16) |
| Multi-tenant white-label | N/A (each customer is its own Microsoft tenant) | BL-20 Partial, BL-21 Implemented | EOIP differentiator only *once* BL-20 physical isolation exists |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

### Strength-adoption cards

| STR-ID | Competitor | Strength | Evidence | Value to EOIP customers | Match / exceed / integrate / reject | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-microsoft-graph-copilot-fabric-01 | Microsoft | Per-item ACL with grant/deny precedence and external (non-IdP) groups, enforced at retrieval | [CLAIM-…-18], [CLAIM-…-17] | No customer answer is trustworthy unless permissions survive (J5) | **Exceed** | Make `PermissionMetadata` (BL-17) authoritative; add deny entries and an external-group table fed by connector group-sync events; filter at candidate generation, at each graph hop, and at answer synthesis | J5: 2 principals × 200 queries, 0 leaked evidence items; revocation reaches index and caches ≤60 s (PROPOSED) |
| STR-microsoft-graph-copilot-fabric-02 | Microsoft | Synced vs federated connector mode per source | [CLAIM-…-16] | Sensitive sources (HR, payroll) never get indexed | **Match** | Source-level `mode: index or federate or hybrid`. The federation planner (BL-51) issues live, permission-scoped calls; results are tagged ephemeral and never persisted | Federated source leaves 0 bytes in index, vector store and logs after 100 queries (PROPOSED) |
| STR-microsoft-graph-copilot-fabric-03 | Microsoft | Ontology as a virtual binding layer; graph materialised only on demand | [CLAIM-…-04], [CLAIM-…-10] | Less storage and fresher answers for lookup and metric questions | **Match** | Ontology concept → binding (CML/IR, BL-33) → planner picks virtual or materialised per query class | Benchmark virtual vs materialised latency and freshness on 3 query classes (PROPOSED) |
| STR-microsoft-graph-copilot-fabric-04 | Microsoft | Distribution inside Copilot / M365 | [CLAIM-…-17], [CLAIM-…-25] | Users stay in Teams/Copilot | **Integrate** (optional; customer-requested, connected deployments only) | EOIP publishes an MCP server that a custom federated connector can call. Only answers already permission-trimmed by EOIP leave; the egress gateway logs every call | Copilot query through EOIP MCP returns cited EOIP evidence; egress manifest records every call (PROPOSED) |
| STR-microsoft-graph-copilot-fabric-05 | Microsoft | RDF/OWL import with a preserved/adjusted/unsupported report | [CLAIM-…-05] | Safe onboarding of existing ontologies | **Match** | Extend BL-31 loss accounting to Turtle/OWL import | Import 3 public ontologies; report counts match a manual audit (PROPOSED) |

### Con-to-Pro inversion cards

**INV-microsoft-graph-copilot-fabric-01 — Cloud-only stack: no disconnected Copilot, Graph, semantic index or Fabric**
- *Target / version / workload:* Copilot connectors, semantic index, Graph in Fabric and Fabric IQ as of 2026-10; regulated, defence and critical-infrastructure buyers.
- *Limitation:* the connector agent requires outbound internet [CLAIM-…-21]. The disconnected sovereign offering covers Exchange, SharePoint and Skype servers only [CLAIM-…-26]. Fabric in GCC High excludes DoD [CLAIM-…-28].
- *Root cause:* **deployment / coupling**, *proven*. Indexing, vectorisation and the LLM are hosted multi-tenant services.
- *Why the alternative helps / when it is worse:* a single-node offline install with local models keeps full function under an air gap. It is worse for customers who want zero operations and already accept the Microsoft cloud; for them EOIP costs more to run than something "already included".
- *Three options:* (1) Quick: an EOIP offline bundle (compose plus model weights plus signed licence, BL-22). (2) Pragmatic: an air-gap acceptance kit, with J16 automated in CI and networking disabled. (3) Long-term: dual-mode connectors that run offline and, when the customer opts in, also publish to Copilot through MCP.
- *Selected:* (2) + (1). Pattern: a network-denied CI lane.
  ```
  docker network create --internal eoip-airgap
  docker compose --profile airgap up      # ollama + hugegraph + api + worker + web; no egress route
  pytest tests/acceptance/j16_airgap.py   # install → ingest SharePoint Server export → query → local-LLM answer
  ```
- *Falsifiable benchmark:* J16 on 1 node (16 vCPU / 64 GB / no GPU), 1 M-document mixed corpus. Success: J1–J6 pass with 0 outbound packets (pcap). Cost baseline: hardware plus operator hours vs the Copilot add-on per user (price not verified in this run).
- *Dependencies and failure cases:* local model quality is below hosted frontier models (mitigate with deterministic-first, J6). Signed model and update supply chain needed (CAP-79). Offline vulnerability feeds go stale.
- *Defensibility:* Microsoft couples Copilot to its multi-tenant cloud. Disconnected Copilot would be a different product, and the February 2026 disconnected launch left it out.
- *Decision:* **ADOPT**.

**INV-microsoft-graph-copilot-fabric-02 — Snapshot graph: full reload on structural change, read-only GQL, no history**
- *Target:* Graph in Fabric GA; living digital-thread workloads (J1, J2, J7).
- *Limitation:* Save reloads all data; loads can take hours; no DML; no as-of queries [CLAIM-…-13], [CLAIM-…-14].
- *Root cause:* **storage / data model**. Reload behaviour is *proven*; the bulk-built layout is a *hypothesis*.
- *Alternative / when worse:* event-sourced revisions with incremental apply (BL-24, BL-37) keep the graph live and auditable. Worse for very large one-off analytic scans, where a bulk-built CSR wins.
- *Three options:* (1) Export EOIP snapshots to Delta/Parquet so Fabric users can also query them. (2) Measure and publish EOIP incremental-apply latency and correctness on the supported backends. (3) Dual-plane architecture: an operational revisioned graph, plus an optional read-optimised analytic snapshot (Neo4j GDS, HugeGraph-Computer, or Fabric graph) built from the same event log.
- *Selected:* (2), with (3) as the architecture direction. API sketch: `POST /graph/snapshots {as_of, target: "parquet"|"gds"|"hugegraph-computer"}`.
- *Benchmark:* replay 10 M SourceEvents, then apply 10 k changes. Success: p95 change-to-queryable ≤5 s on 1 node, and unchanged relationships byte-identical (J1 clause). Baseline: Fabric full-reload time on the same dataset (needs a trial; PROPOSED).
- *Failure cases:* out-of-order events and tombstone races (J7 suite).
- *Defensibility:* incremental, bitemporal provenance is a data-model commitment that a snapshot engine cannot add cheaply.
- *Decision:* **ADOPT** (option 2), **EXPERIMENT** (option 3).

**INV-microsoft-graph-copilot-fabric-03 — Permission trimming stops at documents; graph-level ACL after materialisation unverified**
- *Target:* connector items (flat) and Graph in Fabric (a copy of OneLake).
- *Limitation:* ACLs are per item, with no inter-item relationships [CLAIM-…-18]. The docs do not say whether source RLS survives graph materialisation [CLAIM-…-31].
- *Root cause:* **governance / data model**; *hypothesis* for the graph part.
- *Alternative / when worse:* edge- and fact-level ACL lineage, where a derived edge inherits the intersection of its evidence ACLs. Worse when intersection hides most derived facts and the graph looks empty to low-privilege users.
- *Three options:* (1) Document-level trimming (Microsoft parity). (2) Edge ACL = ∩ of evidence ACLs, computed in the mutation gateway. (3) Query-time ReBAC (OpenFGA/SpiceDB-style) with policy-checked traversal.
- *Selected:* (2), with (3) evaluated later.
  ```
  edge.acl = intersect(acl(e) for e in edge.evidence)       # mutation gateway
  traverse(start, principal): expand only edges where allows(edge.acl, principal)
  ```
- *Benchmark:* J5 plus a derived-fact leakage test. Success: 0 derived edges exposed whose evidence is hidden from the principal. Also report the share of the graph visible per role.
- *Defensibility:* it depends on an evidence model (BL-41) that connector items do not carry.
- *Decision:* **ADOPT** (P0, together with BL-18).

**INV-microsoft-graph-copilot-fabric-04 — Ontology "rules" are untestable natural language; versions are manual checkpoints**
- *Limitation:* [CLAIM-…-06], [CLAIM-…-07]. *Root cause:* **semantics / governance**, *proven*.
- *Alternative / when worse:* executable constraints (SHACL subset, BL-29) shown with a generated NL description, and GitOps versions with semantic diff (BL-32). Worse for business authors who cannot write shapes, so keep an NL-first editor that compiles to shapes under review.
- *Three options:* (1) Store NL rules beside shapes. (2) NL → SHACL proposal by a local LLM, PROPOSED until approved. (3) The full governed lifecycle of J4.
- *Selected:* (2) + (3). *Benchmark:* compile 50 NL business rules to shapes; measure reviewer acceptance rate and false-violation rate on a test graph.
- *Defensibility:* testable rules underpin J10 (rule-change test scope); NL-only rules cannot answer J10.
- *Decision:* **EXPERIMENT**.

## 13. Per-capability decisions

| Capability | Decision | Rationale |
|---|---|---|
| CAP-46 source-ACL enforcement in retrieval and answers | **BUILD** (P0) | Microsoft sets the floor; exceed it with edge-level ACL (INV-03) |
| CAP-26 M365 sources through the Microsoft Graph API | **BUILD** an EOIP connector (least-privilege delegated or application permissions) emitting SourceEvents | Lawful integration route; never mutates the graph directly |
| CAP-59 MCP endpoint usable by Copilot federated connectors | **EXPERIMENT** | Opt-in, connected customers only, through the egress gateway |
| CAP-21 per-source synced vs federated mode | **BUILD** (extend BL-51) | STR-02 |
| CAP-14 GQL | **DEFER** native GQL execution; **EXPERIMENT** with a QueryPlan → GQL compiler | GQL is becoming the buyer's vocabulary |
| CAP-50 air-gapped operation | **BUILD** (acceptance kit) | INV-01 |
| CAP-34 / CAP-36 event-sourced, as-of graph | **BUILD** (BL-37 Implemented; prove it by benchmark) | INV-02 |
| CAP-41 ontology governance + CAP-10 SHACL | **BUILD** | INV-04 |
| CAP-09 RDF/OWL import with loss report | **BUILD** (extend BL-31) | STR-05 |
| Fabric graph as an EOIP backend | **DEFER** | Read-only GQL and OneLake-only sources rule it out as an authoritative backend; possibly an export target later |
| Semantic index / Copilot as a mandatory dependency | **REJECT** | Violates constraints 1 and 2 |

## 14. Concrete tests, proof-of-concept, and acceptance conditions (all PROPOSED)

1. **T-MS-01 permission parity (J5).** Ingest the same SharePoint/Confluence corpus into EOIP. Run 200 queries as 2 principals. Pass: 0 leaks, and revocation honoured within 60 s across index, vectors, caches and agent memory.
2. **T-MS-02 air-gap (J16).** Network-denied CI lane from INV-01. Pass: J1–J6 with 0 outbound packets.
3. **T-MS-03 incremental vs reload.** The same dataset in EOIP and (with a trial) Graph in Fabric. Measure change-to-queryable latency for one property added to a node type. Pass: EOIP p95 ≤5 s. The Fabric figure is recorded, not assumed.
4. **T-MS-04 Microsoft Graph connector (J9).** Ingest Entra users, groups, service principals and app-role assignments with least-privilege application permissions (`User.ReadBasic.All`, `GroupMember.Read.All`, `Application.Read.All`). Answer "impact if service account abc is deleted" joined with CI/CD configuration. Pass: evidence-linked answer with confidence.
5. **T-MS-05 Copilot federation (optional).** Register EOIP's MCP endpoint as a custom federated connector in a test tenant. Pass: Copilot shows EOIP citations; the egress manifest lists every call; no raw source text leaves without policy.
6. **T-MS-06 ontology round-trip.** Export an EOIP ontology to Turtle and import it into a Fabric ontology (preview). Record Microsoft's preserved/adjusted/unsupported report as an interoperability matrix.

## 15. Risks, trade-offs, and open research questions

- **Risk: "already in our licence".** Buyers on M365 E5/E7 may treat Copilot connectors plus Fabric as free. EOIP has to show the specific gaps: cross-source relationships, evidence, as-of queries, air-gap, explainable queries.
- **Risk: a fast-moving preview.** The ontology could reach GA within months with incremental refresh, executable rules or graph-level RLS. Re-verify every quarter.
- **Trade-off:** Copilot integration (STR-04) helps adoption but introduces egress. Keep it opt-in under the egress gateway.
- **Open questions:** (a) Does source RLS/OLS carry into Graph in Fabric after materialisation? (b) Which refresh modes exist for data-only changes (the "Manage and refresh data" page was not examined)? (c) Is Graph in Fabric available in GCC High or sovereign regions? (d) Which ANN index and embedding model does the semantic index use? (e) Do federated connectors re-check source ACLs on every call, or can Copilot cache results? (f) Work IQ MCP/A2A specifics (third-party report only).

---

## Appendix A — Research-dimension coverage

| Dimension | Covered in section(s) | Summary or N/A reason |
|---|---|---|
| D1 Identity and maturity | 1 | Multiple layers. Graph, connectors and Fabric graph GA; ontology preview; Work IQ GA June 2026 |
| D2 Problem and workloads | 2 | Copilot grounding and Fabric analytics; unsuitable for on-prem |
| D3 Architecture decomposition | 4, 5 | Cloud control and data planes; connector agent; OneLake → graph cache |
| D4 Storage primitives and indexing | 5.2 | Vector index and sharded read-optimised graph; layout NOT PUBLICLY VERIFIED |
| D5 Schema and semantic expressivity | 5.1, 5.4 | LPG with limited types; ontology with inheritance and namespaces; NL rules; no formal semantics |
| D6 Query pipeline and optimisation | 5.3 | GQL subset with documented limits; optimiser undocumented |
| D7 Reasoning and inference | 5.4 | No formal reasoning |
| D8 Transactions, concurrency, scale | 5.5, 7 | Read-only snapshot; ~2 B elements; multi-hour loads |
| D9 Ingestion and federation | 3, 5.1, 6 | 100+ connectors; synced vs federated; full/incremental crawl |
| D10 Identity and evidence | 5.7, 11 | Entra identity mapping for ACLs; no entity resolution or claim model documented |
| D11 Time and evolution | 5.6, 9 | Manual ontology versions; no bitemporality |
| D12 Graph algorithms and ML | 3 | Built-in algorithms claimed; catalogue not examined |
| D13 Retrieval and agent integration | 2, 3, 5.7 | Semantic index, Copilot, Work IQ, MCP federated connectors |
| D14 NL querying | 3, 11 | NL2GQL preview; Copilot answers without exposing the query |
| D15 Governance and authoring | 3, 5.6 | Ontology agent is proposal-first; Purview; no semantic diff |
| D16 Human experience | 3 | Query builder (≤8 hops in UI), code editor, Copilot surfaces |
| D17 Developer experience | 3, 5.3 | REST GQL API, Graph SDKs, Agents Toolkit; no GQL parameters |
| D18 Trust and security | 5.7, 12 | Delegated vs application permissions; deny precedence; graph RLS unverified |
| D19 Multi-tenancy and white-label | 10, 11 | Tenant = Microsoft tenant; no white-label |
| D20 Empirical economics | 7 | CU billing, quotas, connector agent sizing; no latency data |
| D21 Commercial and licensing | 9, 10 | Copilot add-on / E7, CU, Copilot Credits |
| D22 Interoperability and lock-in | 3, 10 | RDF/Turtle ontology export; no graph result export; OneLake-only |
| D23 IP and prior art | 15 | No patents examined. Freedom-to-operate review advised before EOIP claims novelty for "virtual ontology bindings with optional graph materialisation", which Microsoft ships publicly |
| D24 Research quality | Appendix C | Mostly official Learn docs pinned by commit; internals unknown; no trial performed |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence CLAIM-ID | EOIP baseline (BL-ID + status) | Decision for EOIP | Priority |
|---|---|---|---|---|---|
| CAP-01 | partial (Fabric graph, read-only) | CLAIM-…-11, -14 | BL-01..05 Implemented | DEFER as backend | P3 |
| CAP-05 | native (scale-out sharding) | CLAIM-…-11 | adapters only | REUSE backend-native scale-out (Neptune, HugeGraph distributed) | P2 |
| CAP-09 | partial (ontology preview) | CLAIM-…-04, -05 | BL-30 Partial | BUILD | P1 |
| CAP-10 | absent | CLAIM-…-06 | BL-29 Partial | BUILD | P1 |
| CAP-14 | native (GQL subset) | CLAIM-…-11, -14 | BL-59 Absent | EXPERIMENT (compiler) | P2 |
| CAP-21 | native (federated connectors, virtual bindings) | CLAIM-…-16, -04 | BL-51 Partial | BUILD | P1 |
| CAP-26 | native (100+ connectors) | CLAIM-…-17 | BL-23 Implemented | BUILD (M365 Graph connector) | P1 |
| CAP-27 | partial (crawl modes) | CLAIM-…-18 | BL-24 Implemented | — (EOIP ahead) | — |
| CAP-34 | absent | CLAIM-…-14 | BL-37 Implemented | BUILD (benchmark proof) | P1 |
| CAP-35 | partial (manual versions) | CLAIM-…-07 | BL-38 Implemented | — | P2 |
| CAP-41 | partial (proposal-first agent) | CLAIM-…-09 | BL-32 Partial | BUILD | P1 |
| CAP-44 | native (Entra ID) | CLAIM-…-24 | BL-19 Implemented / Partial | INTEGRATE (Entra OIDC) | P1 |
| CAP-46 | native at document level | CLAIM-…-17, -18 | **BL-18 Absent** | BUILD | **P0** |
| CAP-47 | native (one Microsoft tenant per customer) | Reasoned | BL-20 Partial | BUILD | **P0** |
| CAP-50 | absent | CLAIM-…-21, -26 | compose + Ollama (deploy/) | BUILD (acceptance kit) | P0 |
| CAP-51 | absent (Microsoft-hosted LLM) | CLAIM-…-22 | BL-45 Implemented | — (EOIP ahead) | — |
| CAP-52 | absent | Reasoned | BL-21 Implemented | — | — |
| CAP-53 | native (semantic index) | CLAIM-…-22 | BL-14 Partial | BUILD (persistent vector option) | P1 |
| CAP-55 | native | CLAIM-…-22 | BL-15 Implemented | — | P2 |
| CAP-58 | preview (NL2GQL) | CLAIM-…-29 | BL-11 Implemented / BL-12 Partial | — (EOIP ahead on explainability) | P2 |
| CAP-59 | native (MCP federated, Work IQ) | CLAIM-…-16, -25 | BL-47 Implemented | EXPERIMENT (EOIP as Copilot MCP source) | P2 |
| CAP-60 | partial (citations; abstention not documented) | CLAIM-…-17 | BL-16 Implemented | BUILD (abstention) | P1 |
| CAP-77 | proprietary per user / CU / credits | CLAIM-…-12, -19, -25 | BL-22 Implemented | — | — |

## Appendix C — Evidence records

All access dates are 2026-10-18.

| CLAIM-ID | Product / version / date | Exact claim | Classification | Source title + URL | Publication / access | Confidence + rationale | Contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-microsoft-graph-copilot-fabric-01 | Graph in Fabric, 2026-06 | "We're announcing the general availability of graph in Fabric." | Officially documented | Microsoft Build 2026: Building agentic apps with Microsoft Fabric and Microsoft Databases — https://azure.microsoft.com/en-us/blog/microsoft-build-2026-building-agentic-apps-with-microsoft-fabric-and-microsoft-databases/ | 2026-06-02 / 2026-10-18 | 0.9, official EVP blog | None |
| CLAIM-microsoft-graph-copilot-fabric-02 | Fabric IQ, 2026-06 | Fabric IQ "now generally available"; "Ontologies in Fabric IQ, expected to be generally available in the coming months"; ontologies preview in Foundry; Fabric IQ in M365 Copilot for "customers in Frontier"; operations agents GA; planning GA later in June | Officially documented | same as -01 | 2026-06-02 / 2026-10-18 | 0.9 | None |
| CLAIM-microsoft-graph-copilot-fabric-03 | Fabric IQ ontology, docs 2026-10-16 | "This feature is in preview." "The old experience of ontology retires on Jan 31, 2027." Migration needs reconnecting consumers and re-creating rules | Officially documented | What Is Ontology (Preview)? — https://learn.microsoft.com/en-us/fabric/iq/ontology/overview (commit 0835e1657760) | 2026-10-16 / 2026-10-18 | 0.9 | Agrees with community post "Fabric IQ Is GA. Your Ontology Isn't." (community.fabric.microsoft.com, HTTP 403, title only) |
| CLAIM-microsoft-graph-copilot-fabric-04 | ontology preview | Ontology "stores and serves ontology definitions and bindings (it isn't itself a general-purpose data-query engine)"; bindings to semantic models, lakehouses, eventhouses, warehouses, SQL DBs, mirrored DBs, shortcuts/views; entity types, inheritance, namespaces, shared properties, keyless types | Officially documented | same as -03 | 2026-10-16 / 2026-10-18 | 0.85 | None |
| CLAIM-microsoft-graph-copilot-fabric-05 | ontology preview | Imports RDF, Turtle and OWL into an empty ontology; exports RDF or Turtle; import identifies preserved, automatically adjusted and unsupported elements | Officially documented | same as -03 | 2026-10-16 / 2026-10-18 | 0.85; fidelity not tested | None |
| CLAIM-microsoft-graph-copilot-fabric-06 | ontology preview | Metrics originate from DAX measures in a source semantic model, which keeps ownership; "A rule is a natural-language statement of business logic" | Officially documented | same as -03 | 2026-10-16 / 2026-10-18 | 0.85 | None |
| CLAIM-microsoft-graph-copilot-fabric-07 | ontology preview | Versions created manually; restoring replaces the current definition | Officially documented | same as -03 | 2026-10-16 / 2026-10-18 | 0.85 | None |
| CLAIM-microsoft-graph-copilot-fabric-08 | ontology preview | Authoring and querying respect OneLake security and source-enforced RLS, OLS and CLS; Fabric permissions; programmatic access and CI/CD | Officially documented | same as -03 | 2026-10-16 / 2026-10-18 | 0.8; not tested | None |
| CLAIM-microsoft-graph-copilot-fabric-09 | ontology agent preview | Agent can "propose changes for review … proposal-first model" | Officially documented | same as -03 | 2026-10-16 / 2026-10-18 | 0.8 | None |
| CLAIM-microsoft-graph-copilot-fabric-10 | ontology preview | "Graph in Microsoft Fabric is an optional execution layer"; ontology-derived schema graph "doesn't load instance data by default"; this replaces the earlier automatic-materialisation framing | Officially documented | same as -03 | 2026-10-16 / 2026-10-18 | 0.85 | 2025 preview material described auto-materialised graphs |
| CLAIM-microsoft-graph-copilot-fabric-11 | Graph in Fabric GA | LPG; GQL ISO/IEC 39075; "scale-out sharding across multiple machines"; "analyze billions of relationships without slowdowns" (vendor claim, no workload); built-in algorithms; NL2GQL | Officially documented (capability) / Unverified (performance) | What is graph in Microsoft Fabric? — https://learn.microsoft.com/en-us/fabric/graph/overview (commit e34caf4d02c2) | 2026-06-26 / 2026-10-18 | 0.85 capability; 0.2 performance | None |
| CLAIM-microsoft-graph-copilot-fabric-12 | Graph in Fabric GA | "Each second of uptime incurs 10 CU-seconds"; rounded up to minutes; 100 GB minimum storage billed as OneLake Cache; automatic shutdown when unused; no separate SKU | Officially documented | same as -11 | 2026-06-26 / 2026-10-18 | 0.9 | None |
| CLAIM-microsoft-graph-copilot-fabric-13 | Graph in Fabric GA | "Graph doesn't apply structural changes incrementally … select Save … to reload all data and rebuild the queryable graph"; ingests lakehouse tables on save; read-optimised graph; GQL, NL2GQL (preview), REST | Officially documented | How graph in Microsoft Fabric works — https://learn.microsoft.com/en-us/fabric/graph/how-graph-works (commit 80a24c9bbee5) | 2026-09-29 / 2026-10-18 | 0.9 | Data-only refresh behaviour not examined |
| CLAIM-microsoft-graph-copilot-fabric-14 | Graph in Fabric GA | Sources: OneLake and mirrored DBs; ~2 billion elements; loads "may take several hours"; >24 h → support; no DML/DDL via GQL; export of results/structures unsupported; no direct Power BI; 64 MB truncation, 128 MB intermediates; 20 min timeout; `ALL SHORTEST`/`ANY` unsupported; no `$param`; no VECTOR type; Explore UI ≤8 hops | Officially documented | Current limitations of graph in Microsoft Fabric — https://learn.microsoft.com/en-us/fabric/graph/limitations (commit 80a24c9bbee5) | 2026-09-19 / 2026-10-18 | 0.9 | None |
| CLAIM-microsoft-graph-copilot-fabric-15 | Graph in Fabric GA | Available in 36 listed commercial regions; no government or sovereign region listed | Officially documented / Reasoned inference (absence) | same as -11 | 2026-06-26 / 2026-10-18 | 0.7 | Fabric GCC High (CLAIM-28) |
| CLAIM-microsoft-graph-copilot-fabric-16 | Copilot connectors 2026-10 | Synced (indexed into Microsoft Graph) vs federated (MCP, fetched live, no indexing); federated read-only; "Write actions will be available starting early October 2026" | Officially documented | Copilot connectors overview — https://learn.microsoft.com/en-us/microsoft-365/copilot/connectors/overview (commit a8bd55dfab63) | 2026-10-12 / 2026-10-18 | 0.9 | None |
| CLAIM-microsoft-graph-copilot-fabric-17 | Copilot connectors 2026-10 | "over 100 prebuilt connectors" incl. Box, Dropbox, Google Drive, Confluence, MediaWiki, file shares, Salesforce, ServiceNow, Dynamics 365, SQL/Oracle, SAP, Workday, Zendesk, Jira; custom via Graph connectors API / Agents Toolkit; Search and Copilot show only items the user can access in source; Copilot cites source | Officially documented | same as -16 | 2026-10-12 / 2026-10-18 | 0.85 | None |
| CLAIM-microsoft-graph-copilot-fabric-18 | Graph connectors API | externalItem = ACL + properties + content (+ write-only activities); ACL entries user / group / Everyone; "deny takes precedence over grant"; external groups for non-Entra groups; non-Entra users must be translated; content text/html; incremental vs full crawl; event vs scheduled sync | Officially documented | Create, update, and delete items in a Microsoft Graph connection — https://learn.microsoft.com/en-us/graph/connecting-external-content-manage-items (commit 70f4b4eecebc) | 2025-08-06 / 2026-10-18 | 0.9 | None |
| CLAIM-microsoft-graph-copilot-fabric-19 | Copilot connectors licensing | Synced indexing incurs no extra cost; Copilot grounding needs M365 Copilot add-on or M365 E7; federated connectors require a Copilot add-on for every querying user; not with Copilot Studio or PAYG | Officially documented | Prerequisites for deploying connectors — https://learn.microsoft.com/en-us/microsoft-365/copilot/connectors/prerequisites (commit 247d476fbab8) | 2026-09-25 / 2026-10-18 | 0.9 | None |
| CLAIM-microsoft-graph-copilot-fabric-20 | Microsoft Search licensing | Index quota of 50 million items per tenant at no extra cost; an item = one record; per-connection default 5 M items (secondary) | Officially documented (search snippet of the Learn page) / Third-party (5 M figure) | License requirements and pricing — https://learn.microsoft.com/en-gb/MicrosoftSearch/licensing ; MC865187 — https://mc.merill.net/message/MC865187 | 2024-09 / 2026-10-18 | 0.6; the en-us page redirected to Prerequisites (no figure) when fetched | Older cached pages: 500 items per licence and $1,000 per million beyond quota |
| CLAIM-microsoft-graph-copilot-fabric-21 | Graph connector agent 2.x | Windows service (GcaHostService); 8 cores, 16 GB RAM, 40 GB per 5 M items + 9 GB per extra million; ≤3 connections per agent; needs internet on 443 to *.office.com, login.microsoftonline.com, gcs.office.com, graph.microsoft.com, Service Bus; Graph application permissions only; GCC, GCC High and DoD configs | Officially documented | Microsoft Graph connector agent overview — https://learn.microsoft.com/en-us/microsoft-365/copilot/connectors/connector-agent (commit f000594eb1b4) | 2026-09-22 / 2026-10-18 | 0.9 | None |
| CLAIM-microsoft-graph-copilot-fabric-22 | Semantic indexing 2026 | "vectorized indices"; tenant-level index from text-based SharePoint files plus Copilot connector data; user mailbox at user level; automatically enabled and "can't be disabled"; site-level exclusion only; respects RBAC; stored in tenant region / EUDB; prompts not used to train foundation LLMs; files ≤512 MB | Officially documented | Semantic indexing for Microsoft Copilot — https://learn.microsoft.com/en-us/microsoftsearch/semantic-index-for-copilot (commit 147ce69f4334) | 2026-08-18 / 2026-10-18 | 0.85 | Localised versions differ on tenant vs user scope |
| CLAIM-microsoft-graph-copilot-fabric-23 | Microsoft Graph v1.0 | Single endpoint graph.microsoft.com; resources and relationships (manager, memberOf, members); Graph Data Connect delivers cached data to Azure; Microsoft APIs Terms of Use apply | Officially documented | Microsoft Graph overview — https://learn.microsoft.com/en-us/graph/overview (commit b30643bc4119) | 2026-04-16 / 2026-10-18 | 0.9 | None |
| CLAIM-microsoft-graph-copilot-fabric-24 | Microsoft Graph permissions | Delegated = granted permission ∩ user's own rights; application permissions access "any data that the permission is associated with"; RSC for a subset (Teams, chats); connector agents require application permissions | Officially documented | Overview of Microsoft Graph permissions — https://learn.microsoft.com/en-us/graph/permissions-overview (commit 6d5d5440d8c6) | 2026-09-04 / 2026-10-18 | 0.9 | None |
| CLAIM-microsoft-graph-copilot-fabric-25 | Work IQ API | "On June 16, Work IQ API reaches general availability"; Chat, Context and Tool APIs; billed in Copilot Credits; Tool API 0.1 credits per call; no separate SKU. MCP / A2A support per third-party review only | Officially documented (GA, billing) / Third-party (protocols) | Work IQ GA — https://microsoft.com/en-us/licensing/news/work-iq-general-availability ; Licensing School — https://www.licensingschool.co.uk/licensing-blog/2026/06/19/work-iq-api-is-generally-available/ | 2026-06-02 / 2026-10-18 | 0.85 GA; 0.45 protocols | None |
| CLAIM-microsoft-graph-copilot-fabric-26 | Sovereign cloud 2026-02 | Azure Local disconnected operations and Microsoft 365 Local Disconnected generally available; M365 Local = Exchange Server, SharePoint Server, Skype for Business Server, supported to at least 2035; Foundry Local runs models fully offline; Copilot and Microsoft Graph not mentioned | Third-party report | Techzine — https://www.techzine.eu/news/privacy-compliance/139052/microsoft-azure-local-365-local-generally-available-the-cloud-offline/ | 2026-02-24 / 2026-10-18 | 0.6; absence of Copilot is inferred from silence | None found |
| CLAIM-microsoft-graph-copilot-fabric-27 | Sovereign cloud 2025-11 | M365 Local GA, connected from Dec 2025, "with a disconnected option for complete isolation coming early 2026"; Azure Local disconnected "available in early 2026"; Copilot only mentioned for in-country processing | Officially documented | Microsoft strengthens sovereign cloud capabilities with new services — https://azure.microsoft.com/en-us/blog/microsoft-strengthens-sovereign-cloud-capabilities-with-new-services/ | 2025-11-04 / 2026-10-18 | 0.85 | None |
| CLAIM-microsoft-graph-copilot-fabric-28 | Fabric GCC High | Public preview 2026-09-02, GA 2026-10-01; not available for DoD; availability varies by workload | Third-party report | The Next Web — https://thenextweb.com/news/microsoft-fabric-gcc-high-government-cloud-eucs-certification-stalled-europe-sovereignty | 2026-09 / 2026-10-18 | 0.5; not confirmed on Learn in this run | None |
| CLAIM-microsoft-graph-copilot-fabric-29 | Fabric Data Agent | Graph as a Data Agent source and NL2GQL "currently in preview" | Officially documented | same as -11 and -13 | 2026-09-29 / 2026-10-18 | 0.9 | None |
| CLAIM-microsoft-graph-copilot-fabric-30 | Azure Local disconnected | Opinion: AKS still "Preview" in disconnected mode, so the GA label is premature | Third-party report | Computer Weekly — https://www.computerweekly.com/opinion/Azure-Local-Disconnected-looks-the-part-for-sovereignty-It-isnt | 2026-03 / 2026-10-18 | 0.4; opinion | Learn "What's new in disconnected operations" lists AKS GA in release 2609 (search snippet) |
| CLAIM-microsoft-graph-copilot-fabric-31 | Graph in Fabric security | Docs say graph is "governed by Fabric OneLake security, compliance, and permission model"; no page found stating whether source RLS/CLS applies to graph elements after materialisation | Officially documented (statement) / Unverified (RLS propagation) | same as -11 | 2026-06-26 / 2026-10-18 | 0.3 for the RLS question | None |
| CLAIM-microsoft-graph-copilot-fabric-32 | Fabric IQ integrations | Fabric IQ tools reachable from GitHub Copilot CLI via Agent Skills for Fabric; Fabric IQ preview as a first-party MCP tool in Agent 365 | Officially documented | same as -01 | 2026-06-02 / 2026-10-18 | 0.8 | None |
| CLAIM-microsoft-graph-copilot-fabric-33 | Fabric IQ ↔ M365 Copilot | Third-party claim that the Copilot Chat / Cowork integration went GA on 2026-09-28 | Unverified | Search-result summary of atlan.com/know/microsoft-fabric/what-is-fabric-iq/ | 2026 / 2026-10-18 | 0.2; single unconfirmed source | Build blog: Frontier-only at announcement |

## Appendix D — Assumptions

1. The registry entry covers Graph API, Copilot connectors, semantic index, Work IQ, Fabric graph and the Fabric IQ ontology as one competitive bundle, because buyers compare them as one bundle. They were not split into separate entries.
2. "Shipped" means GA per a Microsoft source. Preview counts as not shipped, even when broadly usable.
3. No Fabric or M365 trial tenant was used. Every behaviour is documented-or-hypothesis, and all tests are PROPOSED.
4. The 50 M-item quota comes from a search snippet of the official page, because the fetch redirected (confidence 0.6).
5. Silence about Copilot, Graph or Fabric in the sovereign/disconnected announcements is read as "not included". This is a reasoned inference, flagged as such.
6. "Microsoft 365 E7" is accepted as an existing SKU because Microsoft's own licensing table lists it; its price was not examined.
