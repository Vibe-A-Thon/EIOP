# C07 — ServiceNow Knowledge Graph, CMDB/CSDM, Workflow Data Fabric, RaptorDB, Now Assist / Otto

| Field | Value |
|---|---|
| Registry ID | T-C07-servicenow-kg |
| Tier | A. ITSM knowledge-graph competitor. ServiceNow is also an EOIP *source system* (incidents, problems, changes, KB, CMDB) on the reference digital thread, so it is both a competitor and a dependency. |
| Versions examined | ServiceNow AI Platform family releases **Zurich** (Knowledge Graph docs updated 2026-03-12; IRE docs 2025-07-31), **Australia** (Knowledge Graph and Zero Copy Connectors release notes, docs dated 2026-03-12), **Brazil** (Knowledge Graph release notes, updated 2026-09-10). Knowledge Graph app `sn_kg` 7.1.2 seen in a community tutorial (exact current version UNVERIFIED). Knowledge 2026 announcements, 2026-05-06. |
| Verified on | 2026-10-18 |
| Worker | W17 |

In this file `CLAIM-…-NN` is short for `CLAIM-servicenow-kg-NN`.

---

## 1. Identity, current status, tier, and sources

**Owner.** ServiceNow, Inc. (NYSE: NOW). Proprietary platform, normally delivered as a per-customer instance on ServiceNow's cloud. Self-hosted (customer-operated) instances exist for restricted customers [CLAIM-…-17].

**Trap resolution (Master Prompt §5.7, "ServiceNow knowledge graph — shipped vs announced").** "ServiceNow knowledge graph" refers to five different things:

| Thing | What it is | Shipped? | Evidence |
|---|---|---|---|
| **Knowledge Graph (app, `sn_kg`)** | A semantic layer over platform tables. Schemas of nodes (= tables), properties (= columns) and edges (= relationships), built in the no-code **Knowledge Graph Designer**, queried in natural language (NLQ) and through a **Graph Query Builder**. Consumed by Otto (formerly Now Assist) Virtual Agent, the Otto panel and AI agents | **Shipped** (Zurich, Australia, Brazil). Available "with activation of any Now Assist plugin" | [CLAIM-…-01], [CLAIM-…-02], [CLAIM-…-03] |
| **CMDB + CSDM + IRE + Service Graph Connectors** | The long-standing CI/relationship store (`cmdb_ci*`, `cmdb_rel_ci`), the Common Service Data Model (prescriptive service model), the Identification and Reconciliation Engine, and connectors that load third-party inventory through IRE | **Shipped**, mature | [CLAIM-…-13], [CLAIM-…-14], [CLAIM-…-15], [CLAIM-…-22] |
| **Workflow Data Fabric / Zero Copy Connectors** | Federated (zero-copy) access to Snowflake, Databricks, BigQuery, Redshift, SQL Server, Oracle, Teradata, Cloudera, OneLake, Prometheus and other ServiceNow instances | **Shipped** ("available now" per Knowledge 2026; connectors app in the Store) | [CLAIM-…-08], [CLAIM-…-16] |
| **RaptorDB / RaptorDB Pro** | The platform database: PostgreSQL-based, derived from the 2021 Swarm64 acquisition, replacing MariaDB. RaptorDB Pro is marketed as handling operational and analytical workloads together and "natively" processing graph and time-series data | RaptorDB: shipped (migration under way). Pro features Live Connect, Live Perform and Live Archive "available now". Graph-native processing: **announced, details NOT PUBLICLY VERIFIED** | [CLAIM-…-08], [CLAIM-…-11] |
| **Context Engine** | Announced at Knowledge 2026 as a real-time map of people, roles, assets, services and policies, described by analysts as a "graph of graphs" (knowledge, action, access, asset, decision graphs) | **Announced; no availability date found** | [CLAIM-…-08], [CLAIM-…-09] |

Related: **data.world** (knowledge-graph-based data catalog) was acquired in July 2025 and is being folded into Workflow Data Fabric [CLAIM-…-12]. The **ServiceNow Data Catalog** is "available now" [CLAIM-…-08]. **Now Assist has been rebranded "ServiceNow Otto"**, and ServiceNow says Otto is more than a rename [CLAIM-…-07]. Contracts may still say Now Assist.

**Status.** Active, with fast release cadence (two family releases a year plus Store app updates). No archival or EOL concerns.

**Sources.** 18 sources (Appendix C): ServiceNow docs (release-pinned), the ServiceNow newsroom, the SEC 10-K, the Futurum analyst note, Techzine, DBDB, and ServiceNow Community posts (lower trust).

## 2. Primary problem, target workloads, concrete example workflows

ServiceNow's graph assets serve **workflow execution inside ServiceNow**: IT service management, operations, HR, customer service. The graph is a means to route, resolve and personalise. It is not an organisation-wide evidence store.

- **CMDB/CSDM.** Service mapping, impact analysis, change risk, incident routing. Discovery, Service Graph Connectors and integrations write CIs through IRE, which identifies duplicates and enforces authoritative-source rules [CLAIM-…-13], [CLAIM-…-15].
- **Knowledge Graph.** Gives agents structured context. Documented examples: "Who is my manager?", "What assets are assigned to me?"; slot-filling Virtual Agent topics; people citation cards; and (Australia) **natural-language questions about CI dependencies and infrastructure topology over the CMDB** [CLAIM-…-01], [CLAIM-…-03].
- **Workflow Data Fabric.** Lets workflows and agents read external warehouse data without copying it. Databricks is documented as read-only [CLAIM-…-16].

**Example workflow (documented pieces):** an employee asks the Otto Virtual Agent "my laptop is broken". The Knowledge Graph user schema resolves the user's assigned assets (NLQ), the topic slot is pre-filled, the AI agent tool queries the KG for follow-up context, and a ticket is created in workflow [CLAIM-…-01].

**Relation to EOIP reference questions.** "What is impacted if service account abc changes?" ServiceNow can answer this *only for what the CMDB models* (CIs and `cmdb_rel_ci` relationships, CSDM services). Code, commits, pipelines and observability signals are outside the CMDB unless customers build integrations. "Which class caused an incident?" sits below CMDB granularity, and nothing found indicates a code-symbol graph. **ServiceNow and EOIP are complementary on J1/J3/J9:** EOIP ingests ServiceNow incidents, changes and CMDB as evidence.

**On-prem suitability.** Self-hosted exists for restricted customers, but "some Now Assist products/features are currently unavailable" for self-hosted customers and in FedRAMP / DoD IL5 / IRAP-Protected environments [CLAIM-…-18]. The AI layer that consumes the Knowledge Graph therefore cannot be assumed available on-prem.

## 3. Feature inventory

| Capability | Status | Surface | Evidence |
|---|---|---|---|
| Knowledge Graph schemas (nodes = tables, properties = columns, edges) | Present | Designer UI (kg_admin) | [CLAIM-…-01] |
| Copy/customise schemas; default user NLQ graph | Present | Designer | [CLAIM-…-01], [CLAIM-…-04] |
| NLQ over structured platform data | Present (requires a Now Assist / Otto plugin) | Otto VA, Otto panel, AI agents | [CLAIM-…-01], [CLAIM-…-02] |
| Visual Graph Query Builder (also NL → query) | Present | UI | [CLAIM-…-01] |
| CI relationship / topology NLQ over CMDB | Present (Australia) | Otto / KG | [CLAIM-…-03] |
| Tags with AI instructions at node/property/edge level; table/column synonyms; data and column filters | Present (Australia) | Designer | [CLAIM-…-03] |
| NLQ failure reasoning (tables, filters, paths) shown | Present (Australia notes, localised) | Designer | [CLAIM-…-03] |
| KG as a tool in the MCP server console (subset of skills) | Present (Australia Patch 4) | MCP | [CLAIM-…-03] |
| External users (snc_external) access to KG | Optional, property-gated (Brazil) | — | [CLAIM-…-02] |
| Public graph query language (Cypher/GQL/SPARQL/Gremlin) | **Absent** (none documented) | — | Reasoned from docs [CLAIM-…-01] |
| Ontology standards (RDF/OWL/SHACL) import/export | **Absent** (none documented for KG; data.world historically RDF-based, integration status UNVERIFIED) | — | [CLAIM-…-12] |
| CMDB CI classes, relationships, CSDM | Present, mature | UI, Table API, IRE API | [CLAIM-…-13], [CLAIM-…-22] |
| Identification and reconciliation (dedupe, authoritative sources, reclassification) | Present | IRE REST / scriptable API | [CLAIM-…-13], [CLAIM-…-14] |
| Third-party inventory ingestion (Service Graph Connectors, RTE → IRE) | Present | Store apps, SGC Central | [CLAIM-…-15] |
| Zero-copy federation to warehouses and lakes | Present | Zero Copy Connector Hub | [CLAIM-…-16] |
| Data catalog | Present ("available now") | — | [CLAIM-…-08] |
| Graph-native and time-series processing in RaptorDB Pro | Announced; mechanism NOT PUBLICLY VERIFIED | — | [CLAIM-…-08] |
| Context Engine ("graph of graphs") | Announced; availability UNVERIFIED | — | [CLAIM-…-08], [CLAIM-…-09] |
| Action Fabric MCP server for external agents | Reported GA (third-party) | MCP | [CLAIM-…-10] |
| Self-hosted / air-gapped instances | Present for restricted customers (internal Application Repository) | — | [CLAIM-…-17] |
| Now Assist / Otto on self-hosted | **Partial / restricted** ("some … unavailable") | — | [CLAIM-…-18] |
| Bitemporal/as-of graph queries | Absent (not documented; CMDB has audit history, not as-of graph queries) | — | Reasoned |
| White-label/OEM of the platform | Absent for KG (ServiceNow branding; partners build on-platform apps) | — | Reasoned |

## 4. Text-based architecture diagram

```
             ┌──────────────────────── ServiceNow instance (per-customer; SN cloud or self-hosted) ────────────────────────┐
 Discovery ─►│ Import Sets / Service Graph Connectors (RTE transform) ─► IRE API (identify ▸ reconcile ▸ dedupe) ─►          │
 3rd-party   │                                                           CMDB tables cmdb_ci_* + cmdb_rel_ci (CSDM model)  │
 inventory   │ Task tables (incident, problem, change), KB, HR, CSM, sys_user, assets ...                                    │
             │      │ all stored in RaptorDB (PostgreSQL-derived; MariaDB being migrated)                                    │
             │      ▼                                                                                                        │
             │ Knowledge Graph (sn_kg): schema = {nodes=tables, properties=columns, edges=reference/relationship fields},     │
             │   tags + AI instructions + synonyms + filters ─► NLQ engine (LLM-assisted) ─► platform queries (ACL-checked?) │
             │   consumers: Otto VA, Otto panel, AI Agents (KG tool), MCP server console                                     │
             │ Workflow Data Fabric: Zero Copy Connectors ─► Snowflake / Databricks / BigQuery / OneLake / SQL ... (live)    │
             │ Data Catalog (data.world lineage) ─ Context Engine (announced) ─ Action Fabric MCP (external agents)          │
             │ AI layer: Now LLM / platform LLM + AI Controller + Agent Orchestrator (availability restricted when self-hosted)│
             │ Control plane: roles (kg_admin, itil ...), ACLs, Application Repository (air-gapped), upgrades per family      │
             └──────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Data plane.** Writes go through IRE into relational tables. The KG reads tables through schema mappings, and NLQ turns questions into platform queries. **State** lives in RaptorDB tables. The KG holds schemas and configuration and "does not store new data" per a community description [CLAIM-…-05] (official doc: graph representation "stored in a database" [CLAIM-…-01]; ambiguity recorded).

## 5. Under-the-hood reconstruction

### 5.1 Data model
- **CMDB.** A class hierarchy of CI tables (table-per-class inheritance under `cmdb_ci`) plus a relationship table (`cmdb_rel_ci`: parent, child, type) [CLAIM-…-05] (commenter note on `cmdb_rel_ci`), [CLAIM-…-13]. CSDM prescribes domains (business service, application service, technical service, and so on). CSDM's current version is **UNVERIFIED** in this run [CLAIM-…-22].
- **Knowledge Graph.** A *schema graph* over tables. Node = table, property = column, edge = a reference field or relationship table between tables [CLAIM-…-01]. A community report says the graph "expects exact table names" and did not pick up `cmdb_rel_ci` relationships to `cmdb_ci` subclasses in one case [CLAIM-…-05]. Australia then added CI-relationship query support [CLAIM-…-03], which suggests relationship-table traversal was added later. *Hypothesis:* KG instance data is **virtual**, resolved at query time from tables. The graph is not a separately materialised store. Evidence: the community statement plus the "nodes (tables)" framing. Confidence 0.5.

### 5.2 Storage and indexing
RaptorDB is PostgreSQL-derived (Swarm64 lineage) [CLAIM-…-11], so B-tree/heap storage with platform indexes and (Swarm64 heritage) columnar/parallel acceleration. Physical details are NOT PUBLICLY VERIFIED. "Natively processes graph and time-series data" (RaptorDB Pro) has no public mechanism [CLAIM-…-08]. *Hypotheses:* recursive CTE / adjacency-table traversal, or a graph extension on PostgreSQL. Neither is verified.

### 5.3 Query pipeline (KG NLQ, reconstructed)

```
question ─► entity/intent detection using schema tags, synonyms, AI instructions (Australia) [CLAIM-03]
        ─► choose schema (default user NLQ graph or Enterprise Graph) [CLAIM-04]
        ─► LLM plans path: start node(table) → edges → filters → target properties
        ─► compile to platform query (GlideRecord / encoded query; joins along reference fields) — hypothesis
        ─► execute under platform ACLs — documented claim of "permission controls"; leak report exists [CLAIM-05]
        ─► answer + citations / people cards; on failure show reasoning on tables, filters, paths [CLAIM-03]
```

No query language is exposed to users; the Graph Query Builder is visual [CLAIM-…-01]. Cost-based optimisation is the database's own (PostgreSQL planner, presumably).

### 5.4 Reasoning
No formal reasoning is documented. Semantics come from schema plus LLM instructions. CSDM gives modelling conventions, not inference.

### 5.5 Identity and reconciliation (the strongest published mechanism)
IRE: **identification rules** (ordered criterion attribute sets per class) decide new vs existing CI. **Reconciliation rules** allow only authoritative data sources to write given attributes. There are **de-duplication tasks** and **reclassification tasks**, plus **Dynamic IRE** for hardware classes (self-maintained rules, algorithms not alterable). APIs: `identifyCI`, `createOrUpdateCI`, and `createOrUpdateCIEnhanced` (partial payloads/commits). Updates are applied **in real time without a staging area** [CLAIM-…-13], [CLAIM-…-14].

```
def createOrUpdateCI(payload, source):
    for item in payload.items:
        match = apply_identification_rules(item.class, item.values)      # independent / dependent (relationship-qualified) rules
        if match.duplicates: open_dedup_task(match)                       # human review
        allowed = reconciliation_rules.attributes_writable_by(source, item.class)
        write(match.ci or insert(item), {k:v for k,v in item.values if k in allowed})   # committed immediately
    for rel in payload.relations: upsert cmdb_rel_ci(parent, child, type)
```

**EOIP comparison.** EOIP already separates SourceEvent capture from governed mutation (BL-23, BL-28). IRE's *authoritative-source attribute precedence* is the pattern EOIP lacks as a declarative rule set (BL-34 is person-only).

### 5.6 Concurrency, partitioning, consistency
Single-instance relational ACID (PostgreSQL semantics, inferred). Each customer has a dedicated instance, so tenant isolation is physical at the instance level. This is a strength (CAP-47). Context Engine "real time" claims are not substantiated publicly.

### 5.7 Versioning
Platform audit history and update sets for configuration. KG schema copies exist [CLAIM-…-01]. No semantic diff, branch/merge or as-of query over the graph is documented.

### 5.8 Security
Roles (`kg_admin`; requester/fulfiller personas) [CLAIM-…-01]. External-user access to KG is property-gated (Brazil) [CLAIM-…-02]. ACL enforcement for NLQ answers is *claimed* ("data is accessed securely") but **contested**: a community user reported that a minimal-role user got the "manager of my manager" answer despite lacking read access to the manager field [CLAIM-…-05]. Classification: user report, unverified, confidence 0.35. It is significant because it is exactly the J5 failure mode.

## 6. Functional and non-functional requirements inferred

| ID | Requirement inferred from ServiceNow behaviour | Evidence | EOIP implication |
|---|---|---|---|
| FR-1 | Every external writer goes through an identification/reconciliation API, never directly to tables | [CLAIM-…-13], [CLAIM-…-15] | Same doctrine as EOIP (connectors never mutate) |
| FR-2 | Attribute-level authoritative-source precedence | [CLAIM-…-13] | EOIP gap: declarative source-authority rules (CAP-31/CAP-39) |
| FR-3 | Duplicate candidates go to human tasks, not silent merges | [CLAIM-…-13] | Matches BL-35 review queue |
| FR-4 | Admin-curated semantic layer (tags, synonyms, AI instructions per node/edge) to ground NLQ | [CLAIM-…-03] | Adopt for EOIP NL suggestion grounding (BL-11) |
| FR-5 | NLQ failures are explained (tables, filters, paths) | [CLAIM-…-03] | Match in J11 |
| FR-6 | Federated read of warehouse data without copying | [CLAIM-…-16] | EOIP federation planner (BL-51) |
| NFR-1 | Per-customer instance isolation | Reasoned from the deployment model | EOIP SILO mode should be equally physical (BL-20 gap) |
| NFR-2 | Real-time commit without staging (IRE) | [CLAIM-…-14] | EOIP favours staged, replayable events (BL-24). A conscious divergence |

## 7. Performance and resource model

- No independent benchmark of Knowledge Graph NLQ, IRE throughput or RaptorDB was found.
- **Vendor claims:** RaptorDB at Knowledge 2024: 93,257 vs 35,121 transactions per minute against MariaDB, workload and hardware unstated [CLAIM-…-11] (Unverified, 0.25). PayPal customer quote: "database tasks are twice as fast, longest-running operations five times faster" [CLAIM-…-08] (Unverified). A reseller's "27x query speedup" for WDF (search snippet) is excluded as non-attributable.
- **Scaling (reasoned).** KG NLQ cost is dominated by LLM calls plus relational joins. Deep multi-hop paths over `cmdb_rel_ci` on PostgreSQL degrade with path length unless recursive queries are bounded. Whether RaptorDB Pro adds graph-native execution is unverified.
- **Failure modes.** NLQ misinterpretation (admins mitigate with tags and synonyms, which implies accuracy issues [CLAIM-…-03]). The ACL leak report [CLAIM-…-05]. IRE commits without staging, so bad payloads land immediately [CLAIM-…-14].

## 8. Strengths and how to match or exceed

1. **IRE: mature identity and reconciliation for CIs** with authoritative-source precedence, dedupe tasks and reclassification [CLAIM-…-13]. *Match/exceed:* EOIP declarative source-authority rules per attribute, applied to *all* entity types, with staged dry-run (EOIP's replay log) that IRE lacks.
2. **Installed base and system of record for ITSM.** Incidents, changes and CMDB already live there. *Integrate:* first-class EOIP ServiceNow connector (exists in the EOIP connector set per BL-23) covering CMDB relationships, CSDM services and IRE source metadata as evidence.
3. **Curated semantic grounding for NLQ** (tags with AI instructions, synonyms, filters, failure explanations) [CLAIM-…-03]. *Match:* add the same metadata to the EOIP ontology manifest to feed the suggestion engine.
4. **Physical per-customer instance isolation** (reasoned). *Match:* EOIP SILO tenancy must be enforced physically (BL-20).
5. **Zero-copy warehouse federation** at enterprise breadth [CLAIM-…-16]. *Match* selectively through BL-51 adapters (Trino/DuckDB-style federation is a candidate; out of scope here).
6. **MCP exposure** of the KG tool and the workflow engine [CLAIM-…-03], [CLAIM-…-10]. *Integrate:* EOIP agents can call ServiceNow MCP tools (read-only by default, ADR-007) for live ticket context.

## 9. Limitations with root causes

**Verified / documented**
- KG requires a Now Assist (Otto) plugin [CLAIM-…-02].
- No public graph query language or standards interchange documented [CLAIM-…-01].
- Graph scope is the platform's own tables plus zero-copy sources. Databricks connector is read-only [CLAIM-…-16].
- Now Assist features restricted for self-hosted and high-compliance clouds [CLAIM-…-18].

**Intentional trade-offs**
- Schema graph over relational tables rather than a native graph store, which keeps one system of record.
- IRE commits in real time without staging [CLAIM-…-14].

**Licensing**
- Proprietary subscription. AI features gated by Now Assist / Otto SKUs and (from 2026) Data Fabric credits [CLAIM-…-08].

**User-reported**
- Possible ACL bypass in NLQ answers [CLAIM-…-05].
- KG "not a replacement for learning the table schema" [CLAIM-…-06].
- Exact-table-name sensitivity [CLAIM-…-05].

**Outdated claims to avoid**
- "Now Assist" as the current brand (now Otto) [CLAIM-…-07].
- "ServiceNow runs on MariaDB" (migrating to RaptorDB) [CLAIM-…-11].
- Context Engine as shipped (only announced) [CLAIM-…-08].

**Root causes**
- *Algorithmic:* multi-hop traversal compiled to relational joins (hypothesis); LLM-mediated NLQ without a typed, inspectable plan.
- *Operational:* everything must live in or federate into the instance; restricted AI on self-hosted; heavyweight platform administration (third-party competitor blogs say so; low weight).
- *Developer friction:* no portable query language; proprietary scripting (Glide); KG configuration needs deep table-schema knowledge [CLAIM-…-06].

## 10. Deployment, licensing, redistribution, operational viability under EOIP constraints

| EOIP constraint | ServiceNow | Verdict |
|---|---|---|
| Air-gap | Self-hosted, air-gapped instances are supported, with an internal Application Repository paired with ServiceNow Support [CLAIM-…-17]. **But** Now Assist / Otto features are partly unavailable there [CLAIM-…-18], and the KG depends on a Now Assist plugin [CLAIM-…-02]. Whether KG NLQ works air-gapped is **UNVERIFIED** (KB0743854 not accessible). | **Partial** (platform yes, KG+AI unverified/likely limited) |
| Local LLM / egress | Platform LLMs are ServiceNow-hosted. BYO-LLM options exist in the AI platform generally, but were not verified for self-hosted | Not compatible by default |
| Backend neutrality | Single proprietary database | Lock-in |
| White-label | No (ServiceNow-branded platform; partners build scoped apps) | Not embeddable |
| Redistribution | Proprietary; EOIP integrates via REST/Table/IRE APIs and MCP under customer licences | **Legal-review trigger:** API use terms and data-extraction clauses in customer subscriptions when EOIP bulk-ingests CMDB |

**Seed inversion ("SaaS or heavyweight deployment, vendor lock-in, limited on-prem/air-gap").** **Partially validated.**
- *On-prem/air-gap:* **rejected for the base platform** (self-hosted air-gapped is a documented mode) and **validated for the AI/KG layer** (restricted Now Assist availability).
- *Lock-in:* **validated** (proprietary DB, no standard graph query or ontology interchange; *proven* from docs absence, confidence 0.7).
- *Heavyweight:* **validated as hypothesis only** (competitor blogs; not evidenced by primary sources).

## 11. Competitive delta against the EOIP verified baseline

| Area | ServiceNow | EOIP | Delta |
|---|---|---|---|
| Identity / reconciliation | IRE: identification, authoritative-source reconciliation, dedupe and reclassify tasks [CLAIM-…-13] | Deterministic person identity only (BL-34); review queue Partial (BL-35); probabilistic ER Absent (BL-36) | **Deficit**: adopt IRE-style source authority (STR-01) |
| Source-ACL in answers | Claimed, contested [CLAIM-…-05] | **BL-18 Absent** | Both weak; EOIP must lead (INV-01) |
| Cross-domain digital thread | CMDB + ITSM; no code-level graph found | Code graph (BL-42), SourceEvents from Jira/GitLab/GitHub/CI/observability (BL-23) | **EOIP differentiator** (J1, J9, J10) |
| Contradictions (J2: Confluence vs ServiceNow owner) | Reconciliation picks an authoritative source and overwrites the attribute [CLAIM-…-13], [CLAIM-…-14] | Claims and contradictions preserved (BL-39), bitemporal (BL-37) | **EOIP differentiator**: keep both claims plus the decision |
| NL query | LLM NLQ with failure reasoning [CLAIM-…-03] | Deterministic suggestions, candidate query shown (BL-11), LLM hook Partial (BL-12) | EOIP ahead on explainability; ServiceNow ahead on grounding metadata UX |
| Federation | Zero Copy Connectors, broad [CLAIM-…-16] | Federation planner Partial (BL-51) | Deficit in breadth |
| Tenancy | Per-customer instance (physical) | Contract only (BL-20) | **Deficit**, P0 |
| Air-gap AI | Restricted [CLAIM-…-18] | Local Ollama + egress gateway (BL-45) | **EOIP differentiator** |
| Standards / portability | None documented | JSON-LD, SHACL subset, multi-backend (BL-01, BL-31) | **EOIP differentiator** |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

### Strength-adoption cards

| STR-ID | Competitor | Strength | Evidence | Value to EOIP customers | Match / exceed / integrate / reject | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-servicenow-kg-01 | ServiceNow | IRE: attribute-level authoritative-source reconciliation, identification rules, dedupe tasks | [CLAIM-…-13], [CLAIM-…-14] | Trustworthy merged entities from many sources | **Exceed** | Declarative `source_authority.yaml` per entity type and attribute. The resolver proposes; conflicts become claims (BL-39) rather than overwrites. Staged dry-run over replay (BL-24) before commit | J2 plus a synthetic 5-source CI feed: 0 duplicate identities; authority honoured on 100% of attributes; losing values preserved as claims (PROPOSED) |
| STR-servicenow-kg-02 | ServiceNow | NLQ grounding metadata: tags, AI instructions per node/property/edge, synonyms, filters, failure reasoning | [CLAIM-…-03] | Better NL accuracy for non-technical users (J11) | **Match** | Add `synonyms`, `ai_instructions` and `default_filters` to the ontology manifest; the suggestion engine uses them; on failure, return the unmatched tokens and the path attempted | J11 accuracy on 200 NL questions, with vs without metadata (PROPOSED) |
| STR-servicenow-kg-03 | ServiceNow | Installed ITSM/CMDB system of record | [CLAIM-…-15], [CLAIM-…-13] | EOIP needs ServiceNow data for J1/J2/J3/J9 | **Integrate** | ServiceNow connector reads CMDB (`cmdb_ci*`, `cmdb_rel_ci`), CSDM services, task tables and IRE data-source attribution into SourceEvents with ACL metadata | Ingest a PDI export; CI relationships round-trip with 100% edge fidelity (PROPOSED) |
| STR-servicenow-kg-04 | ServiceNow | Physical per-customer instance isolation | Reasoned | P0 tenant isolation | **Match** | SILO tenancy = separate backend graph or namespace, plus separate index and vector store per tenant | J13 leakage suite (PROPOSED) |

### Con-to-Pro inversion cards

**INV-servicenow-kg-01 — NLQ answers through an LLM over tables, with ACL enforcement contested and no inspectable plan**
- *Target:* Knowledge Graph NLQ (Zurich–Brazil), people/asset/CI questions.
- *Limitation:* ACL bypass reported for a manager-chain question [CLAIM-…-05]. NLQ is LLM-planned with no exposed query language [CLAIM-…-01].
- *Root cause:* **governance / coupling**. *Hypothesis*: permission checks may apply to the final record set but not to intermediate hops.
- *Alternative / when worse:* a typed QueryPlan (BL-08) with per-hop ACL checks and the plan shown to the user. Worse when users want free-form questions that templates cannot cover. Mitigate by keeping LLM suggestion → plan → user selection (J11).
- *Three options:* (1) Final-result ACL filter. (2) Per-hop ACL filter in the executor (each edge expansion checks principal access to source and target records and to the edge evidence). (3) ReBAC policy engine with traversal-aware checks.
- *Selected:* (2).
  ```
  for hop in plan.hops:
      frontier = [n for n in expand(frontier, hop.edge) if can_read(principal, n) and can_read_edge(principal, hop.edge, n)]
  ```
- *Benchmark:* J5 with a manager-chain probe set (100 two- and three-hop questions; low-privilege role). Success: 0 answers that depend on an unreadable intermediate node. Cost: p95 latency overhead ≤20% vs no checks on 1 M nodes.
- *Failure cases:* cached group membership goes stale after revocation (invalidate on identity events).
- *Defensibility:* combining a deterministic plan, per-hop checks and an evidence display is an architectural property, not a feature toggle.
- *Decision:* **ADOPT** (P0).

**INV-servicenow-kg-02 — Reconciliation overwrites: one authoritative value wins, no preserved disagreement or as-of truth**
- *Target:* IRE reconciliation; J2 (Confluence vs ServiceNow ownership).
- *Limitation:* only authoritative sources write attributes, applied in real time with no staging [CLAIM-…-13], [CLAIM-…-14].
- *Root cause:* **data model** (single current-state CI row), *proven*.
- *Alternative / when worse:* claim-based truth maintenance (BL-39) with bitemporal revisions (BL-37). Worse on storage and query complexity for simple "current value" lookups, so serve a materialised current view.
- *Three options:* (1) Store the losing values as annotations. (2) Claims plus a current-view projection. (3) Full bitemporal truth maintenance with resolution decisions and as-of queries.
- *Selected:* (3), already Implemented in-memory (BL-37, BL-39); it needs backend persistence.
- *Benchmark:* J2 scenario at 100 k entities × 3 sources. Success: as-of query returns the historically correct owner for 100% of sampled timestamps; current-view latency within 1.2× a single-value store.
- *Defensibility:* buyers in regulated domains need "who said what, when". Current-state CMDB designs cannot add this without a data-model change.
- *Decision:* **ADOPT**.

**INV-servicenow-kg-03 — Platform-bound graph: proprietary DB, no standard query or ontology interchange, AI restricted when self-hosted**
- *Limitation:* [CLAIM-…-01], [CLAIM-…-11], [CLAIM-…-18].
- *Root cause:* **deployment / licensing**. Proven for self-hosted AI restrictions; absence of interchange is reasoned from docs.
- *Alternative / when worse:* an open, exportable ontology and evidence (JSON-LD/Turtle, BL-31), multi-backend (BL-01), local models. Worse when the customer's whole workflow lives inside ServiceNow and wants no second system.
- *Three options:* (1) Export EOIP insights back into ServiceNow (KB articles, CI attributes) through its APIs under review gates. (2) An EOIP MCP server callable from ServiceNow's MCP client (if supported). (3) Position EOIP as the cross-system evidence graph that ServiceNow agents consult.
- *Selected:* (1) with review gates, plus (3) for positioning. No direct writes without approval (§4.3.8).
- *Benchmark:* J16 run with the ServiceNow connector reading an offline export.
- *Decision:* **EXPERIMENT**.

## 13. Per-capability decisions

| Capability | Decision | Rationale |
|---|---|---|
| CAP-31 source authority, merge/split, survivorship | **BUILD** (IRE-inspired, claim-preserving) | STR-01, INV-02 |
| CAP-30 deterministic identity keys beyond persons | **BUILD** | IRE identification rules per class |
| CAP-46 per-hop ACL in traversal and answers | **BUILD** (P0) | INV-01 |
| CAP-58 NL grounding metadata and failure explanations | **BUILD** | STR-02 |
| CAP-26 ServiceNow connector (CMDB, CSDM, tasks, IRE attribution) | **BUILD/extend** | STR-03 |
| CAP-21 zero-copy federation breadth | **DEFER** (beyond BL-51 core adapters) | Breadth race not core |
| CAP-59 consume ServiceNow MCP tools (read-only) | **EXPERIMENT** | Live ticket context for agents |
| CAP-47 physical tenant isolation | **BUILD** (P0) | STR-04 |
| ServiceNow KG as an EOIP backend | **REJECT** | Platform-bound, proprietary |

## 14. Concrete tests, POCs, acceptance (all PROPOSED)

1. **T-SN-01 IRE parity plus.** 5 synthetic sources feed 50 k CIs with conflicting attributes. EOIP must produce 0 duplicate identities, apply authority rules, preserve losing claims, and answer as-of correctly.
2. **T-SN-02 manager-chain leakage (J5).** 100 multi-hop people questions as a minimal-role user. 0 leaks.
3. **T-SN-03 ServiceNow ingest fidelity.** PDI or export of CMDB plus `cmdb_rel_ci` plus incidents/changes. Edge count and type fidelity 100%; ACL metadata captured per record.
4. **T-SN-04 NLQ grounding A/B (J11).** 200 questions; top-3 candidate accuracy with vs without synonyms and AI instructions.
5. **T-SN-05 J2 owner disagreement.** Confluence page says team A, ServiceNow CI says team B. Both claims kept; resolution recorded; as-of queries correct.

## 15. Risks, trade-offs, open questions

- **Risk:** Context Engine plus RaptorDB Pro graph processing may ship as a native graph with access-graph (Veza-style) semantics, which would narrow EOIP's permission-aware graph lead *inside* ServiceNow estates. Re-verify after the next family release.
- **Risk:** customers may expect EOIP to write back into the CMDB. Writes must go through IRE APIs and review gates.
- **Open questions:** (a) Is KG NLQ available on self-hosted or air-gapped instances (KB0743854)? (b) How are ACLs enforced per hop in KG NLQ? (c) Does RaptorDB Pro expose any graph query surface? (d) Current CSDM version and its relationship to the KG schemas. (e) Status of data.world's RDF/knowledge-graph tech inside WDF (the "Declan" rename is single-source).

---

## Appendix A — Research-dimension coverage

| Dimension | Covered in | Summary or N/A reason |
|---|---|---|
| D1 Identity and maturity | 1 | Five-way disambiguation; KG shipped; Context Engine announced; Otto rename |
| D2 Problem and workloads | 2 | ITSM workflow context; complementary to EOIP's digital thread |
| D3 Architecture | 4 | Instance-centric; IRE write path; KG schema layer |
| D4 Storage and indexing | 5.2 | PostgreSQL-derived RaptorDB; graph-native claims unverified |
| D5 Schema and semantics | 5.1 | CMDB class hierarchy plus relationship table; KG schema graph; CSDM conventions |
| D6 Query pipeline | 5.3 | LLM NLQ and visual builder; no public graph QL |
| D7 Reasoning | 5.4 | None formal |
| D8 Transactions and scale | 5.6, 7 | Single-instance ACID (inferred); vendor TPM claims only |
| D9 Ingestion and federation | 3, 5.5 | Service Graph Connectors, IRE, Zero Copy Connectors |
| D10 Identity and evidence | 5.5 | IRE identification/reconciliation; no evidence spans |
| D11 Time and evolution | 5.7 | Audit history; no as-of graph queries |
| D12 Graph algorithms and ML | — | N/A: no graph algorithm library documented for KG/CMDB beyond impact/service maps (not examined) |
| D13 Retrieval and agents | 3, 8 | Otto VA, AI agents KG tool, MCP server console, Action Fabric |
| D14 NL querying | 3, 5.3 | NLQ with tags, synonyms, failure reasoning |
| D15 Governance and authoring | 3, 5.7 | Designer (kg_admin); no ontology review workflow documented |
| D16 Human experience | 3 | Designer, Graph Query Builder, guided tour |
| D17 Developer experience | 9 | Glide/scoped apps; no portable QL |
| D18 Trust and security | 5.8 | Roles; contested ACL behaviour in NLQ |
| D19 Multi-tenancy / white-label | 5.6, 10 | Per-customer instance; no white-label |
| D20 Empirical economics | 7 | Vendor claims only |
| D21 Commercial and licensing | 9, 10 | Subscription; Now Assist plugin required for KG; Data Fabric credits |
| D22 Interoperability and lock-in | 10 | No standard interchange found |
| D23 IP and prior art | 15 | Not examined; IRE-style source authority is long-established practice (low novelty risk for EOIP) |
| D24 Research quality | App. C | Official docs plus press release; several community sources flagged low trust |

## Appendix B — Capability mapping

| CAP-ID | ServiceNow | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-08 | partial (CI classes, mandatory fields) | CLAIM-…-13 | BL-28 Implemented | — | P2 |
| CAP-21 | native (Zero Copy Connectors) | CLAIM-…-16 | BL-51 Partial | DEFER breadth | P2 |
| CAP-26 | native (Service Graph Connectors) | CLAIM-…-15 | BL-23 Implemented | BUILD ServiceNow connector depth | P1 |
| CAP-30 | native (IRE identification rules) | CLAIM-…-13 | BL-34 person-only | BUILD | P1 |
| CAP-31 | partial (reconciliation, dedupe tasks; no probabilistic ER documented) | CLAIM-…-13 | BL-35 Partial, BL-36 Absent | BUILD | P1 |
| CAP-39 | absent (overwrite by authority) | CLAIM-…-13, -14 | BL-39 Implemented | — (EOIP ahead) | — |
| CAP-34 | absent | Reasoned | BL-37 Implemented | — (EOIP ahead) | — |
| CAP-42 | native (Data Catalog, data.world) | CLAIM-…-08, -12 | Absent (catalog not a BL item) | DEFER | P3 |
| CAP-46 | claimed, contested | CLAIM-…-05 | BL-18 Absent | BUILD | **P0** |
| CAP-47 | native (instance per customer) | Reasoned | BL-20 Partial | BUILD | **P0** |
| CAP-50 | partial (self-hosted; AI restricted) | CLAIM-…-17, -18 | compose + Ollama | — (EOIP ahead on AI) | P0 |
| CAP-58 | native (NLQ, tags, synonyms) | CLAIM-…-01, -03 | BL-11/BL-12 | BUILD grounding metadata | P1 |
| CAP-59 | native (MCP console, Action Fabric) | CLAIM-…-03, -10 | BL-47 Implemented | EXPERIMENT consume | P2 |
| CAP-69 | partial (CI impact; no code level) | CLAIM-…-03 | BL-42 Implemented/Partial | — (EOIP ahead) | — |

## Appendix C — Evidence records

All access dates are 2026-10-18.

| CLAIM-ID | Product / version / date | Exact claim | Classification | Source + URL | Pub / access | Confidence | Contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-servicenow-kg-01 | Knowledge Graph, Zurich docs (updated 2026-03-12) | Semantic layer; "graphical representation of real-world entities (tables) and their relationships, stored in a database"; schema = nodes (tables), properties (columns), edges; Designer for kg_admin; Graph Query Builder (also NL-generated); NLQ ("Who is my manager?"); prebuilt integrations with Otto VA, Otto panel, AI agents (tool) | Officially documented | Exploring Knowledge Graph — https://www.servicenow.com/docs/r/SRy58xeijUUqttfwLgfrHQ/ADBXI0oa_suBlOXW7fzomg | 2026-03-12 / 2026-10-18 | 0.85 | Community: KG "does not store new data" (CLAIM-05) |
| CLAIM-servicenow-kg-02 | Knowledge Graph, Brazil release notes (2026-09-10) | "Knowledge Graph is available with activation of any Now Assist plugin from the ServiceNow Store"; snc_external users allowed when `sn_kg.enable_external_user_check` = true; improved accuracy for Otto VA, panel and AI Agent | Officially documented | Knowledge Graph release notes — https://www.servicenow.com/docs/r/release-notes/knowledge-graph-rn.html | 2026-09-10 / 2026-10-18 | 0.85 | None |
| CLAIM-servicenow-kg-03 | Knowledge Graph, Australia release notes (2026-03-12) | CI relationship queries over CMDB dependencies/topology; tags with AI instructions at node/property/edge level; table/column synonyms, data/column filters; guided tour; Patch 4: KG as a tool in MCP server console; Glidelist references; NLQ failure reasoning (localised notes) | Officially documented (via search snippets of docs) | Knowledge Graph release notes / Combined Yokohama→Australia notes — https://www.servicenow.com/docs/r/IDeOjpA1hzonPLWG~inEpg/jRelaxUyc2pARPjaZbLxzg ; https://www.servicenow.com/docs/r/AWjfoG0XNF6COBtQI5zL~A/EFtKRYAXIk7mvSoxqM2mkQ | 2026-03-12 / 2026-10-18 | 0.7; pages not fetched in full | None |
| CLAIM-servicenow-kg-04 | Community, Dec '25 release | Default schema `sn_kg.now_user_graph_nlq` (property `sn_ais_assist.kgnlq_schema_name`); Enterprise Graph hidden by default for Now Assist VA/panel; re-enable via `sn_kg.va.enable_global_graph_all_modes` | Third-party report | Customizing Knowledge Graph Configurations — https://www.servicenow.com/community/now-assist-blog/customizing-knowledge-graph-configurations/ba-p/3476626 | 2025-12 / 2026-10-18 | 0.45 | None |
| CLAIM-servicenow-kg-05 | Community article 2025-11-17 | KG "references existing systems of record" and does not duplicate data; AI "sees exactly what the user is authorized to see"; commenter (2025-11-27): minimal-role user still got "manager of my manager"; commenter: graph expects exact table names; `cmdb_rel_ci` → `cmdb_ci` not picked up | Third-party report (user report for the leak) | ServiceNow Knowledge Graph: The Semantic Foundation… — https://www.servicenow.com/community/now-assist-articles/servicenow-knowledge-graph-the-semantic-foundation-for/ta-p/3429209 | 2025-11-17 / 2026-10-18 | 0.35; unverified user report | Official docs claim "robust data governance and permission controls" |
| CLAIM-servicenow-kg-06 | Community tutorial | Knowledge Graph [sn_kg] 7.1.2 with Now Assist AI Agents; KG "is not a replacement for learning and understanding the ServiceNow table schema" | Third-party report | Quick Tutorial: AI Agent Knowledge Graph Tool — https://www.servicenow.com/community/now-assist-articles/quick-tutorial-ai-agent-knowledge-graph-tool/ta-p/3533655 | 2026 / 2026-10-18 | 0.4 | None |
| CLAIM-servicenow-kg-07 | Otto brand 2026 | "ServiceNow Otto isn't Now Assist with a new name"; app listing: "Now Assist has been renamed to ServiceNow Otto"; entitlements unchanged | Officially documented (product page, via search) / Third-party | ServiceNow Otto — https://www.servicenow.com/de/platform/otto.html ; store release notes — https://www.servicenow.com/docs/r/store-release-notes/store-rn-itsm-now-assist.html | 2026 / 2026-10-18 | 0.6 | None |
| CLAIM-servicenow-kg-08 | Knowledge 2026 press release | Context Engine "maps every person, role, asset, service, and policy across a business in real time" (no availability given); RaptorDB Pro handles operational and analytical workloads and natively processes graph and time-series data; Workflow Data Fabric "available now"; Live Connect (SQL API), Live Perform, Live Archive, Data Catalog available now; Autonomous Data Governance H2 2026; MCP Registry via Innovation Lab; PayPal quote 2×/5× faster | Officially documented (vendor PR); performance = Unverified | ServiceNow launches the real-time data foundation… — https://newsroom.servicenow.com/press-releases/details/2026/ServiceNow-launches-the-real-time-data-foundation-that-puts-autonomous-AI-to-work-across-the-enterprise/default.aspx | 2026-05-06 / 2026-10-18 | 0.8 capability statements; 0.2 performance | None |
| CLAIM-servicenow-kg-09 | Context Engine | Integrates "knowledge, action, access, asset, and decision graphs"; no availability stated; governance and write-back called open questions | Third-party report (analyst) | Futurum, Keith Kirkpatrick — https://futurumgroup.com/insights/can-servicenows-real-time-data-foundation-make-autonomous-ai-a-reality/ | 2026-05-08 / 2026-10-18 | 0.5 | Other blogs list "User Graph" and Veza-powered Access Graph (shashi.co, not fetched) |
| CLAIM-servicenow-kg-10 | Action Fabric | Exposes the workflow engine to external agents via a GA MCP server; Anthropic Claude launch partner | Third-party report | Constellation Research — https://www.constellationr.com/insights/news/servicenow-knowledge-2026-ai-control-tower-action-fabric-autonomous-workforce-and (search snippet) | 2026-05 / 2026-10-18 | 0.45 | None |
| CLAIM-servicenow-kg-11 | RaptorDB | PostgreSQL-based proprietary RDBMS derived from Swarm64 (acquired 2021) replacing MariaDB for all customers; Knowledge 2024 vendor figure 93,257 vs 35,121 TPM (no workload/hardware) | Third-party report / Unverified (figure) | Techzine — https://techzine.eu/news/data-management/119846/servicenow-trades-mariadb-for-raptordb-postgresql ; DBDB — https://dbdb.io/db/raptordb-servicenow | 2024 / 2026-10-18 | 0.7 identity; 0.25 figure | Migration completion date not found |
| CLAIM-servicenow-kg-12 | data.world | Acquisition of data.world completed July 2025; not material; strengthens AI platform with data meaning/context; being integrated into WDF | Officially documented (SEC) / Third-party (integration) | ServiceNow Form 10-K FY2025 — https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm ; SC World — https://www.scworld.com/brief/servicenow-expands-ai-platform-with-data-world-deal | 2026-01 / 2026-10-18 | 0.85 (10-K, via search snippet) | "Declan" rename single-source, UNVERIFIED |
| CLAIM-servicenow-kg-13 | CMDB IRE, Zurich (2025-07-31) | IRE prevents duplicate CIs with identification rules; reconciliation lets only authoritative sources write attributes; dedupe and reclassification tasks; Dynamic IRE for cmdb_ci_hardware descendants (algorithms not alterable); Discovery, Event Mgmt, Import Sets, Cloud Insights use IRE APIs; REST and scriptable APIs for third parties; some non-CMDB tables supported | Officially documented | Exploring CMDB Identification and Reconciliation (IRE) — https://www.servicenow.com/docs/r/zS6yb8e~gR8BPjeviYdV9g/~mjd2YB~xROkz9c39aS_sQ | 2025-07-31 / 2026-10-18 | 0.85 | None |
| CLAIM-servicenow-kg-14 | CMDB IRE | "The CMDB is updated in real time … There is no staging area"; APIs createOrUpdateCI(), identifyCI(), createOrUpdateCIEnhanced() (partial payloads/commits) | Officially documented (search snippet) | Components and process of Identification and Reconciliation — https://www.servicenow.com/docs/r/GCPjp~ldPTNRN99oH1DYFg/eUXumCBbcZFJ~GfPH0xxsA | 2026-03-12 / 2026-10-18 | 0.7 | None |
| CLAIM-servicenow-kg-15 | Service Graph Connector for Microsoft Intune, Australia | Data transformed by Robust Transform Engine into CMDB classes, then written by IRE; SGC Central; supports Yokohama, Zurich, Australia; Integration Commons dashboard | Officially documented (search snippet) | Service Graph Connector for Microsoft Intune — https://www.servicenow.com/docs/r/servicenow-platform/service-graph-connectors/cmdb-integration-intune.html | 2026-03 / 2026-10-18 | 0.75 | None |
| CLAIM-servicenow-kg-16 | Zero Copy Connectors | Databricks and Snowflake primary connectors (from Yokohama Patch 5); Databricks read-only; Australia added Cloudera Hive/Impala, Microsoft OneLake, Prometheus, ServiceNow instance; WDF Hub renamed Zero Copy Connector Hub; May 2025: Redshift, Databricks, BigQuery, SQL Server, Oracle, Snowflake, Cloudera, Teradata | Officially documented | Zero Copy Connectors release notes — https://www.servicenow.com/docs/r/7GoNY9eeDRD0FzxldbEmXw/Mh8gnbIq2sJO3GFr04JInA ; primary connectors — https://www.servicenow.com/docs/r/integrate-applications/primary-connectors-zcc.html ; BusinessWire 2025-05-07 | 2026-03 / 2026-10-18 | 0.75 | None |
| CLAIM-servicenow-kg-17 | Self-hosted | "self-hosted, air-gapped customers don't allow their instances to communicate with external networks"; internal Application Repository with pairing; contact account rep | Officially documented | Application Repository for self-hosted, air-gapped customers — https://www.servicenow.com/docs/r/application-development/application-repository-self-hosted/manage-store-app-air-gapped.html | 2026 / 2026-10-18 | 0.8 | None |
| CLAIM-servicenow-kg-18 | Now Assist availability | "Some Now Assist products/features are currently unavailable for customers in the FedRAMP, NSC DOD IL5, or Australia IRAP-Protected data centers, self-hosted customers, or in other restricted environments" (KB0743854) | Officially documented (via search snippet; older release page) | Integration Hub — https://docs.servicenow.com/bundle/rome-servicenow-platform/page/administer/integrationhub/concept/integrationhub.html | 2025-03 / 2026-10-18 | 0.6; may have changed | None |
| CLAIM-servicenow-kg-19 | Self-hosted naming | Self-hosted offering now referred to as "Private Stack" | Third-party report | UnoGeeks — https://unogeeks.com/servicenow-on-premise/ | n/a / 2026-10-18 | 0.25 | None |
| CLAIM-servicenow-kg-20 | Zurich release notes | Lists "Service summary using Knowledge Graph" | Officially documented (search snippet) | Zurich Release Notes PDF — https://downloads.docs.servicenow.com/pdf/enus/servicenow-zurich-release-notes-enus.pdf | 2026-10-08 / 2026-10-18 | 0.6 | None |
| CLAIM-servicenow-kg-21 | Microsoft Copilot connectors | A prebuilt Microsoft Copilot connector for ServiceNow exists, so ServiceNow content also flows into Microsoft 365 Copilot | Officially documented | see CLAIM-microsoft-graph-copilot-fabric-17 | 2026-10-12 / 2026-10-18 | 0.85 | None |
| CLAIM-servicenow-kg-22 | CSDM | CSDM is ServiceNow's prescriptive service data model for CMDB; current version number UNVERIFIED in this run | Reasoned inference / Unverified | (no primary page fetched) | — / 2026-10-18 | 0.3 | None |

## Appendix D — Assumptions

1. "ServiceNow knowledge graph and CMDB" covers the Knowledge Graph app, CMDB/CSDM/IRE, Workflow Data Fabric, RaptorDB and the Context Engine together. They are not split into separate entries.
2. Family release order Zurich → Australia → Brazil is taken from the docs as published. The Brazil GA date was not verified.
3. No ServiceNow instance (PDI) was used; all tests are PROPOSED.
4. Community posts are used only as user reports with confidence ≤0.45.
5. The KB0743854 restriction on Now Assist for self-hosted customers is assumed to still apply, because no newer contradicting source was found.
