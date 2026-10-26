# Cohort 05 — Enterprise Work Graphs and Operational-Ontology Platforms

| Field | Value |
|---|---|
| Cohort ID | COH-05 |
| Workload class | Closest commercial competitors: platforms that connect enterprise sources into a graph or ontology and put search, assistants, agents and actions on top |
| Core members (Tier A, deep) | [Palantir Foundry/AIP](../04-COMPETITOR-DEEP-DIVES/C07-palantir-foundry.md), [Glean](../04-COMPETITOR-DEEP-DIVES/C07-glean-enterprise.md), [Atlassian Rovo](../04-COMPETITOR-DEEP-DIVES/C07-atlassian-rovo.md), [Microsoft Graph / Copilot / Fabric IQ](../04-COMPETITOR-DEEP-DIVES/C07-microsoft-graph-copilot-fabric.md), [ServiceNow Knowledge Graph](../04-COMPETITOR-DEEP-DIVES/C07-servicenow-kg.md), [Onyx](../04-COMPETITOR-DEEP-DIVES/C07-onyx.md) |
| Adjacent members (lighter evidence) | [SAP knowledge graph](../04-COMPETITOR-DEEP-DIVES/C07-sap-knowledge-graph.md), [Salesforce Data 360](../04-COMPETITOR-DEEP-DIVES/C07-salesforce-data-cloud.md), [Diffbot](../04-COMPETITOR-DEEP-DIVES/C07-diffbot.md), [Writer KG](../04-COMPETITOR-DEEP-DIVES/C07-writer-kg.md), [Azure Digital Twins](../04-COMPETITOR-DEEP-DIVES/C07-azure-digital-twins.md), [Process mining (OCEL, PM4Py, Celonis)](../04-COMPETITOR-DEEP-DIVES/C07-process-mining.md) |
| Tier C records | [C07-tier-c-records-V19](../04-COMPETITOR-DEEP-DIVES/C07-tier-c-records-V19.md): Eclipse Ditto, organisational network analysis (both REFERENCE/EXPERIMENT, not scored) |
| Reference columns | HugeGraph, Neo4j, Neptune (security/tenancy/air-gap rows only) |
| EOIP status basis | `01-SYSTEM-BASELINE.md` (BL, ad9937b) superseded by `01a-BASELINE-DELTA-HEAD.md` (HEAD 896e06d, BL/NB rows) |
| Journeys | J1 evidence-rich change impact; J2 evolving organisational truth; J5 permission-aware GraphRAG; J9 service-account blast radius; J15 non-IT organisation; J16 air-gapped operation |
| Date | 2026-10-26 |

Count: 12 deep dives (6 core, 6 adjacent) plus 2 Tier C records.

## 1. Workload class and comparison basis

**Customer workloads.** An enterprise wants one place to ask "what is affected, who owns it, what changed, and may I see it?" across ticketing, wiki, code, CMDB, HR and finance systems, with agents that can act. These products are what an EOIP buyer will put on the same evaluation spreadsheet.

**Why comparable.** All six core members ingest from many sources, keep a model of objects/relations/people, enforce (or claim to enforce) source permissions at retrieval, and expose agents or MCP. Their evidence base is documentation plus vendor statements; no product trials were run (method limit, `03-RESEARCH-METHODOLOGY.md` §8), so internals are documented-or-hypothesis.

**Core versus adjacent.** Palantir, Glean, Rovo, Microsoft, ServiceNow and Onyx have full deep dives (50 to 182 evidence records each). SAP, Salesforce, Diffbot, Writer, Azure Digital Twins and process mining have only 1 to 9 CLAIM records and several are search-summary grade, so they are compared in a separate, thinner table and no ranking is drawn from them.

**Excluded.** Graph engines (cohort 01/02), ontology tools (cohort 03) and GraphRAG libraries (cohort 06) are different workloads. Meta's Glean code indexer is not this Glean (name trap resolved in C07-glean-enterprise §1).

**Seed hypothesis under test (Master Prompt §10.5).** "Palantir / Glean / Rovo: SaaS or heavyweight deployment, vendor lock-in, limited on-prem/air-gap." Validated per product in §3. Result: the SaaS and limited-air-gap parts hold for Glean, Rovo and Microsoft; "heavyweight" is rejected for all three (customers run nothing); the seed is partially validated for ServiceNow, **partly rejected for Palantir** (on-prem and air-gap documented, heavyweight validated) and fully rejected for Onyx.

## 2. Capability comparison

Notation: claim IDs shortened: `pal-` palantir-foundry, `gl-` glean-enterprise, `rv-` atlassian-rovo, `ms-` microsoft-graph-copilot-fabric, `sn-` servicenow-kg, `ox-` onyx, `sap-`, `sf-`, `dif-`, `wri-`, `adt-`, `pm-` as in the deep dives; `n4-` neo4j, `hg-` apache-hugegraph, `nep-` amazon-neptune. `§n` is a deep-dive section without a CLAIM row. `unknown` = not publicly verified.

### 2.1 Core members

| Capability | Palantir | Glean | Rovo | Microsoft | ServiceNow | Onyx | EOIP @HEAD |
|---|---|---|---|---|---|---|---|
| Data / ontology model (CAP-08, CAP-09) | native Ontology: object, link, action types, interfaces; "not a semantic layer", no OWL/SHACL (pal-01, pal-13) | native Knowledge Graph over content, people, activity; entities from NLP, triples kept on repeatable evidence (gl-04, gl-05) | native Teamwork Graph of work objects plus connector objects (rv §1) | partial: Fabric IQ ontology item still preview; RDF/Turtle export (ms §1, ms-05) | native: tables-as-nodes Knowledge Graph app plus CMDB/CSDM (sn-02, sn-13) | absent (index + chunks; graph retrieval partial/abandoned, ox §B) | Partial: fixed label manifest, in-house SHACL/OWL subset (BL-28/29/30) |
| Connectors (CAP-26) | native: sources, CDC, streams, batch and Flink (pal-22) | native: 100+ (gl-04), push API, MCP tools (gl-11) | native cloud; Forge `graph:connector` (rv-08); DC connectors index into Cloud (rv-04) | native: 100+ prebuilt, synced or federated (ms-16, ms-17) | native Service Graph Connectors and Zero Copy (sn-15, sn-16) | native: 56 (ox-03) | Implemented, IT-focused; new Snowflake, Artifactory, Slack etc., live-unverified (BL-23, NB-06) |
| Permission sync / enforcement (CAP-46) | native: markings propagate along lineage (pal-14) | native: query-time, `allowed_users/groups`, identity graph (gl-10, gl-11); derived-edge and agent-memory enforcement undocumented | claimed; `replicatesPermissions=false` exposes data to every workspace user (rv-08); mechanism undocumented (rv-09) | native at document level (ms-17, ms-22) | claimed but contested by a user leak report (sn-05) | enterprise-only for 14 connectors (ox-03); query-time filter in v5.0.0 (ox-08) | Partial: PDP with deny-by-default and derived-fact check, applied only in one retrieval branch when `scope` passed (BL-18 HEAD, NB-17) |
| Tenant isolation (CAP-47) | Organizations as mandatory silos (pal-13) | isolated single tenant (gl-16) | SaaS tenancy, mechanism unknown | one Microsoft tenant per customer (reasoned, ms App. B) | instance per customer (reasoned) | not stated | Partial (improved): runtime isolation for vector, index, SQLite, objects, keys; adapters not tenant-aware (BL-20 HEAD) |
| Versioning / history (CAP-34/35/36) | native: dataset transactions, global branching, action edit log (pal-18, pal-21) | unknown | unknown | absent in Graph in Fabric; full reload on structural change (ms-13, ms-14) | absent: IRE overwrites by authority, no staging (sn-13, sn-14) | absent | Implemented: bitemporal reads, diff, snapshots (BL-37/38) |
| Governed actions / write-back | native: action types with rules, side effects, writeback dataset (pal-18) | partial: agents; write path undocumented | partial: Jira agents GA (rv-05) | write actions on federated connectors "from early October 2026" (ms-16) | native workflows; Action Fabric (sn-10, per Appendix B) | MCP/OpenAPI actions in Business plan (ox-04) | Implemented as library, in-memory, not mounted (NB-03) |
| MCP / agent tools (CAP-59) | Ontology MCP; Palantir MCP beta, no data writes (pal-15) | server + host + gateway, OAuth 2.1 (gl-08, gl-09) | MCP v2, OAuth 2.1; Teamwork Graph tools in open beta (rv-05, rv-07) | federated connectors via MCP; Work IQ API GA (ms-16, ms-25) | MCP console (sn §B) | MCP server (ox-01) | Implemented, 18 read-oriented tools, one shared static token for all callers (BL-47 HEAD) |
| LLM egress control / local models (CAP-51, CAP-61) | self-hosted models in compute modules, vLLM/Ollama, no external connectivity needed (pal-12) | hyperscaler LLMs, zero retention, no local option (gl-12, gl-13) | external LLM egress not customer-controllable (rv-10, rv §10) | Microsoft-hosted LLM; no local model (ms-22) | platform LLMs hosted by ServiceNow (sn §10) | Ollama and OpenAI-compatible endpoints; no air-gap guide (ox-10) | Implemented: egress gateway default S0, kill switch, DLP; Model Provider Port (BL-45 HEAD, NB-10) |
| Grounded answers with citations (CAP-60) | AIP; citations not detailed | native citations (gl-05) | partial | partial, abstention undocumented (ms-17) | NLQ answers, accuracy needs tags/synonyms (sn-03) | native chat with sources | Implemented: fenced context, cited-span claim check, removal of unsupported claims (BL-16 HEAD) |
| White-label / OEM (CAP-52) | none public (pal-13) | none | none (rv §10) | none (first-party SaaS, ms §10) | none (sn §10) | enterprise plan lists white-labelling (ox-04) | Implemented branding/terminology (BL-21) |

### 2.2 Adjacent members (thin evidence)

| Capability | SAP | Salesforce Data 360 | Diffbot | Writer KG | Azure Digital Twins | Process mining | EOIP @HEAD |
|---|---|---|---|---|---|---|---|
| Core model | RDF/OWL/SPARQL engine in HANA Cloud (sap-02) | lakehouse with identity resolution; data graphs unverified (sf-03) | public-web KG, >10B entities (vendor claim, dif-01) | managed graph-RAG, opaque (wri-01) | DTDL twin graphs (adt-01, adt-02) | OCEL 2.0 object-centric logs; PM4Py AGPL-3.0 (pm-01, pm-03) | LPG over supported backends |
| Deployment | managed cloud only (sap-02) | SaaS (sf-01) | SaaS API; self-host unverified (dif §10) | SaaS; self-host not verified (wri §10) | Azure PaaS (adt-01) | OCEL open format; PM4Py self-hostable (pm-03) | self-hosted, local-first (BL-45, compose) |
| Probabilistic ER | n/a | native (sf-03, unverified detail) | native, external IDs (dif-01) | n/a | n/a | n/a | Partial, own engine, library-only (BL-36 HEAD) |
| Evidence strength | 0.4 to 0.7 per record | 0.25 to 0.8 | 0.3 to 0.6 | 0.35 to 0.8 | 0.5 to 0.85 | 0.5 to 0.8 | n/a |

### 2.3 Reference columns

| Capability | HugeGraph | Neo4j | Neptune | EOIP @HEAD |
|---|---|---|---|---|
| CAP-45 RBAC | native RBAC + targets, off unless configured (hg-14, hg-32) | enterprise-only (n4-14) | partial, per-action IAM (nep-09) | Implemented, deny-by-default routes (BL-19, NB-05) |
| CAP-46 ACL in retrieval | partial, post-filter (hg-15) | enterprise-only, partial (n4-15) | absent (nep-12) | Partial (BL-18 HEAD) |
| CAP-47 tenancy | partial, graphs and spaces (hg-16) | enterprise-only multi-database (n4-13) | one graph per cluster (nep-12) | Partial (BL-20 HEAD) |
| CAP-50 air-gap | native (hg §10) | native with usage report off (n4-30) | absent, VPC-only (nep-08) | design goal, no live air-gap test (BL-45; J16) |
| CAP-59 MCP | unreleased, master only (hg-30) | not scored here | not scored here | Implemented (BL-47) |

## 3. Operational and licensing comparison

Seed validation is in the last column.

| Product | Deployment models | One-node footprint | Air-gap | Licence / OEM | Pricing (public?) | Maintenance | §10.5 seed verdict |
|---|---|---|---|---|---|---|---|
| Palantir | Rubix Kubernetes on AWS/Azure/GCP/OCI or on-prem; IL5/IL6; Apollo delivers into air-gapped networks (pal-08, pal-09); NVIDIA sovereign reference architecture (pal-10) | none: multi-node blue/green required, nodes recycled within 48 h (pal-08) | **yes, documented** | proprietary; no public OEM/white-label; osdk-ts licence unverified (pal-07) | contract only; compute-second metering rates published (pal-16) | active | **SaaS-only: rejected. Heavyweight: validated** (inference, 0.5). Lock-in: weakly supported (no standards export documented, 0.4) |
| Glean | Glean Hosted (GCP) or Customer Hosted in customer GCP/AWS, still operated by Glean, no manual deploy or patch (gl-01); Dell on-prem announced only (gl-14) | n/a (managed) | **no** documented | proprietary SaaS; none | no list price; third-party estimates unverified (gl-15) | active | **SaaS and air-gap limits: validated. Heavyweight: not validated** (customers do not run the footprint). Lock-in: partially (no documented export, hypothesis) |
| Rovo | Cloud for full feature set; DC connectors index into Cloud (rv-01, rv-04); DC end of life 2029-03-28 (rv-03) | n/a | **no** | proprietary; none | credits included in plans; $0.01 per extra credit (rv-01) | active | **Partially validated.** SaaS-only for full function and DC end of life validated; "heavyweight" rejected (bundled, auto-activated, rv-01); lock-in mechanism unproven (INV-atlassian-rovo-01) |
| Microsoft | all layers Microsoft cloud; connector agent needs outbound 443 (ms-21); disconnected offerings exclude Copilot/Graph (ms-26) | connector agent 8 cores/16 GB (ms-21) | **no** | proprietary, Microsoft API terms (ms §10) | per user, Fabric CU, Copilot credits (ms-12, ms-25) | active, ontology item preview | **Validated**; "heavyweight" partly rejected (nothing to install for M365 shops) |
| ServiceNow | per-customer instance; self-hosted air-gapped supported (sn-17); Now Assist/KG partly unavailable there (sn-18) | n/a | platform yes, KG+AI unverified | proprietary | not found in deep dive | active | **Partially validated** |
| Onyx | Compose, Kubernetes, Helm, Terraform; Lite <1 GB (ox-01) | yes, Lite | partial, no guide (ox-10) | MIT core + Enterprise License in `ee` dirs: **legal review** (ox-01, ox-11) | Business $20/user/month annual, vendor page (ox-04) | active, v5.0.0 | **Rejected** |
| SAP, Salesforce, Diffbot, Writer, Azure DT | managed or PaaS only (sap-02, sf-01, dif §10, wri §10, adt-01) | n/a | no | proprietary; DTDL open (CC-BY-4.0/MIT, adt-02) | Diffbot tiers via aggregator only (dif-04, 0.3) | active | consistent with seed |

## 4. Performance evidence

No independent or reproducible benchmark exists for any member. All figures below are vendor or secondary claims and are **not comparable** with each other or with EOIP.

| Source | Figure | Context | Class |
|---|---|---|---|
| Palantir | object indexing "tens of billions of objects for a single object type" (pal-04) | no workload or hardware | vendor, unverified |
| Palantir limits | 2,000 properties per object type; Search Around default 100,000; 10,000 objects per action (pal-04) | documented limits | official |
| Microsoft | Graph in Fabric: 10 CU-seconds per uptime second, 100 GB minimum, about 2B element ceiling; loads "several hours", >24 h goes to support (ms-12, ms-14) | documented limits | official |
| Microsoft | "billions of relationships without slowdowns" (ms-11) | none | vendor, unverified |
| Rovo | ">150 billion connections", "44% more accurate", "48% fewer tokens" (rv-06) | internal benchmark, no dataset | vendor, not comparable |
| ServiceNow | RaptorDB 93,257 vs 35,121 transactions per minute (sn-11) | hardware unstated | vendor, 0.25 |
| Writer | RobustQA 86.31% (wri-03) | vendor run; independent study finds graph benefit task-dependent (wri-06) | vendor vs independent |
| EOIP | none for retrieval quality or permission-leakage rate | PROPOSED in `15-VALIDATION-BENCHMARK-PLAN.md` | not run |

Consequence: no winner can be declared. The comparable ground is functional (documented behaviours and limits), plus the permission-leakage and cross-tenant-leakage rates in Master Prompt §12, which no competitor publishes.

## 5. Findings

1. **Air-gapped operation is not unique to EOIP.** Palantir documents on-prem, IL5/IL6 and air-gapped delivery (pal-08, pal-09) and ServiceNow supports self-hosted air-gapped instances (sn-17). EOIP's differentiator against these two is one-node footprint and local-model default, not mere air-gap. Falsified if EOIP cannot demonstrate J16 on one node (no live test yet).
2. **Glean, Rovo and Microsoft cannot run air-gapped on current evidence.** Glean Customer Hosted is still Glean-operated (gl-01), Rovo needs Cloud (rv-01), Microsoft agents need outbound 443 (ms-21). Air-gap plus local LLM is a defensible wedge against these three.
3. **Source-ACL enforcement is table stakes and EOIP is behind.** Glean enforces at query time (gl-10), Palantir propagates markings along lineage (pal-14), Microsoft shows only user-accessible items (ms-17). EOIP has a PDP but applies it in one retrieval branch only when `scope` is passed; `agents/governed.py` and `/api/v1/rag` pass none (BL-18/48 HEAD). Per Master Prompt §4.3 item 8 this is P0 regardless of competitors.
4. **Competitor permission claims are not uniformly reliable.** ServiceNow has a user report of a leak (sn-05, third-party), Rovo connectors can leave data visible to everyone if `replicatesPermissions` is false (rv-08), Onyx puts permission sync behind Enterprise (ox-03). A published, reproducible leakage test would be a credible differentiator.
5. **None documents epistemic separation, bitemporal as-of queries or contradiction preservation.** ServiceNow overwrites by authority (sn-13); Palantir keeps an action edit log and branches (pal-18, pal-21) but no claim/contradiction model; Glean, Rovo, Onyx are `unknown`. J2 is a genuine EOIP lead (BL-37/39/40), conditional on the claims engine moving off the in-memory store.
6. **Palantir's Ontology is the capability parity bar, and it is proprietary in both directions.** Governed actions with approval rules, writeback and branching (pal-18, pal-21) have no mounted EOIP equivalent (NB-03 is library-only, in-memory, no built-in connector write path). Palantir itself says its Ontology is not a semantic layer (pal-13), so open ontology export is where EOIP can differ.
7. **Open-core is the only self-hostable peer in the cohort and it gates permissions.** Onyx's core is MIT, but Auto Sync Permissions, SSO, on-prem terms and white-labelling sit in Enterprise (ox-03, ox-04). It is the nearest "self-host first" comparator buyers will test; it carries a legal-review trigger for any EOIP reuse (ox-11).
8. **MCP is converging as the integration seam, with OAuth 2.1.** Glean, Rovo and Palantir expose MCP with scoped authentication (gl-08, rv-07, pal-15). EOIP's MCP server authenticates every caller with one shared static token, so no user or tenant identity propagates (BL-47 HEAD). This blocks J5 over MCP.
9. **Every core product lists many more connectors than EOIP's IT-centric set.** 56 to 100+ (ox-03, gl-04, ms-17) against EOIP's 30+ IT connectors (BL-23, NB-06, mostly live-unverified). J15 (non-IT organisation) has no competitor-demonstrated advantage over EOIP's generic ontology, but connector breadth favours competitors.
10. **Pricing is opaque for four of six core members.** Only Rovo (credits, rv-01), Onyx (list price, ox-04) and Palantir's metering rates (pal-16) are public. Buyers will compare TCO using estimates, so EOIP's offline licence file and metering (BL-22) should be priced transparently.

## 6. Implications for EOIP

| CAP | Parity needed (STR) | Exploitable weakness (INV) | Decision | Candidate gap statement |
|---|---|---|---|---|
| CAP-46 ACL enforcement | STR-glean-enterprise-01/03, STR-palantir-foundry-02/03, STR-microsoft-graph-copilot-fabric-01 | INV-servicenow-kg-01, INV-atlassian-rovo-02, INV-onyx-01 | **BUILD (P0)**: apply `can_read` on every retrieval, agent and MCP path; publish a leakage test | "Enforcement exists but is not applied on deployed paths (BL-18 HEAD)." |
| CAP-47 tenancy | STR-servicenow-kg-04 (instance isolation); Palantir Organizations (pal-13) | n/a | **BUILD (P0)**: make adapters tenant-aware | "Runtime isolation covers retrieval/DSAR; graph adapters carry no tenant handling." |
| CAP-59 MCP | STR-palantir-foundry-05, STR-glean-enterprise-04 | Palantir MCP cannot write data (pal-15) | **BUILD**: per-user OAuth 2.1/PKCE, tenant propagation, governed action tools; **EXPERIMENT**: EOIP as a tool inside Glean/Copilot | "MCP callers share one token." |
| Governed actions | STR-palantir-foundry-01/07 (action types, branches) | pal-04 (10k object cap) | **BUILD**: mount `ActionEngine`, persist state | "Governed write-back is library-only and in-memory (NB-03)." |
| CAP-50 air-gap / J16 | STR-palantir-foundry-06 (Apollo-style bundle transfer, integrity checks) | INV-palantir-foundry-01 (multi-node floor), INV-glean-enterprise-01, INV-microsoft-graph-copilot-fabric-01 | **BUILD** acceptance kit; run offline install test | "No executed air-gap test; signed offline bundles unproven." |
| CAP-51 / CAP-61 local models | Palantir self-hosted models (pal-12) | gl-12, ms-22, rv §10 | **REUSE** Ollama/vLLM; **BUILD** MCP egress policy | "Egress covers LLM calls; MCP traffic policy not specified (pal-15 warning)." |
| CAP-26 connectors | STR-glean-enterprise-02/07, STR-microsoft-graph-copilot-fabric-02, STR-onyx-01..03 | breadth gap | **BUILD** prioritised non-IT connectors on demand (J15); **INTEGRATE** Microsoft Graph connector | "Connector breadth is IT-centric; most live-unverified." |
| CAP-34/35 history, CAP-39 contradictions | STR-palantir-foundry-07 | INV-servicenow-kg-02 (sn-13/14 overwrite); INV-microsoft-graph-copilot-fabric-02 (ms-13 full reload) | **REUSE** own (BL-37/38/39); **BUILD** persistence for `TruthStore` | "Claims engine is in-memory." |
| CAP-09 ontology | STR-microsoft-graph-copilot-fabric-05 (RDF import/export report), STR-palantir-foundry-08 | pal-13 no semantic layer; INV-servicenow-kg-03 | **BUILD** open export/bridge at the boundary; **REUSE** pySHACL in CI | "Semantic layer is in-house subset." |
| CAP-52 white-label | n/a | none of 5 offers OEM; Onyx gates it (ox-04) | **REUSE** own (BL-21) as differentiator; verify de-vendoring checklist | |
| CAP-77 pricing | Rovo credit model (rv-01) | INV-atlassian-rovo-03 (default-on overage), gl-15 opacity | **ADOPT** transparent tiers on offline licensing | |
| CAP-80 process/org intelligence | OCEL 2.0, ONA | PM4Py AGPL (pm-03) | **EXPERIMENT**: OCEL importer, event-graph projection; **REJECT** bundling PM4Py | "No process-intelligence capability." |
| Adjacent products | n/a | n/a | **REJECT** SAP, Salesforce, Writer, Diffbot, ADT as dependencies; **REUSE** DTDL as import schema; optional Diffbot connector behind egress policy | |

Backend neutrality: nothing here requires a particular graph backend. Per-engine security features (HugeGraph RBAC, Neo4j EE multi-database, Neptune IAM) are "available upstream / not integrated" and should sit under, not replace, EOIP's PDP (hg-15, n4-15, nep-12). Neptune IAM SigV4 is absent from the adapter (BL-04 HEAD).

## 7. Open questions

1. Does any competitor enforce permissions on derived edges and agent memory? Glean states retrieval enforcement only (gl-10); the rest are undocumented. Needs a leakage test design (J5).
2. Is Palantir's osdk-ts licence permissive (pal-07), and do Palantir/ServiceNow API terms allow EOIP bulk-ingest connectors (legal review triggers, ms §10, sn §10)?
3. Does Glean's Dell on-prem architecture ship, and is it air-gappable (gl-14, no date or details)?
4. Do Fabric IQ ontology and Context Engine (ServiceNow) reach GA, and with what query surface (ms §1, sn §1)? Both are announced or preview.
5. What does the HEAD route set expose for J1 and J9? Impact simulator is library-only (NB-07), and no competitor documents a service-account blast-radius feature (`unknown`).
6. Evidence conflicts: Onyx connector count is 56 in docs versus "40+" and "50+" elsewhere (ox-01, ox-03, ox-04); Rovo AI-provider pages disagree (rv-10); Glean zero-retention scope differs by key type (gl-13); Writer and Salesforce records rest on search summaries or unrendered pages (wri-05, sf-03). The Glean, Palantir and Rovo deep dives each return a different seed verdict (heavyweight rejected for Glean and Rovo, validated for Palantir), so the seed cannot be applied to the trio as one statement. No decision rests solely on these.
7. Which journeys should buyers see first: J5 and J16, where EOIP can win after closing BL-18, or J2, where it already leads?
