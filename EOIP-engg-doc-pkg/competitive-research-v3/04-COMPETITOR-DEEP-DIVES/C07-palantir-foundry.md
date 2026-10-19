# C07 — Palantir Foundry Ontology and AIP

| Field | Value |
|---|---|
| Registry ID | T-C07-palantir-foundry |
| Tier | A. It is the closest operational-ontology competitor and the reference that enterprise buyers use for "ontology + actions + AI". |
| Versions examined | Palantir Foundry, AIP, Apollo and Rubix as described in the public documentation at palantir.com/docs on the access date. Palantir ships continuously and publishes **no public version numbers** for Foundry or AIP. Ontology backend: Object Storage v2. The documentation says Object Storage v1 "Phonograph" "will be unavailable after June 30, 2026". OSDK: `palantir/osdk-ts` main branch (no release tag captured). Palantir + NVIDIA sovereign AI OS reference architecture: announced 2026-03-12. |
| Verified on | 2026-10-18 |
| Worker | W16 |

---

## 1. Identity, current status, tier, and sources

**Identity.** Palantir Technologies Inc. (NYSE: PLTR) sells three linked platforms, all running on **Rubix**, Palantir's hardened Kubernetes substrate [CLAIM-palantir-foundry-08] [CLAIM-palantir-foundry-13]:

- **Foundry**, the data operations platform.
- **AIP** (Artificial Intelligence Platform), the generative-AI and agent layer built on Foundry.
- **Apollo**, the continuous-delivery and fleet-management platform.

**Gotham** is a separate government and intelligence product and is out of scope.

The **Ontology** is the part of Foundry that competes directly with EOIP. The documentation calls it a digital twin of the organisation. It maps datasets and models to object types, properties, link types and action types, plus functions, interfaces, object sets, roles and object views [CLAIM-palantir-foundry-01]. The platform summary states that "The Ontology is not a semantic layer": it combines data, logic, action and security [CLAIM-palantir-foundry-13].

**Status.** Active and continuously delivered. Documented changes in 2026:

- Object Storage v1 (Phonograph) was retired after 2026-06-30 in favour of Object Storage v2 [CLAIM-palantir-foundry-03].
- "AIP Agent Studio" was renamed **AIP Chatbot Studio** [CLAIM-palantir-foundry-11].
- "Ontology as Code" appears in a 2025–2026 community thread as a **Beta**. A later post asks whether it was removed, so it is treated as not generally available [CLAIM-palantir-foundry-20].

**Licence.** Proprietary commercial software under enterprise contract. The public `palantir/osdk-ts` repository exists, but its licence was **not visible** on the captured page and is UNVERIFIED [CLAIM-palantir-foundry-07].

**Tier reason.** Tier A. Buyers name Palantir when they say "operational ontology". Its Ontology + Actions + AIP stack sets the parity bar for EOIP's ontology, governed-mutation and agent layers.

**Name and trap resolution.** There is no name collision. Shipped vs announced is resolved per feature in §3:

- Palantir MCP is labelled **beta** in its documentation.
- Ontology as Code is a beta of uncertain status.
- The NVIDIA reference architecture is an announced, qualified configuration, not a product SKU.

**Sources used (14 primary, 3 secondary):**

- Official documentation pages: Ontology core concepts, Ontology backend, OSDK, link types, action types, markings, AIP overview, self-hosted models, the Foundry platform summary for LLMs, the Rubix architecture-centre page, Ontology MCP, Palantir MCP, DevOps/Marketplace, and code-workspace compute usage.
- The `palantir/osdk-ts` GitHub repository.
- The Palantir/NVIDIA Business Wire release.
- The Palantir blog post on deploying across security domains (403 on fetch; search snippet only).
- Secondary: Constellation Research and Palantir community threads.

Full records are in Appendix C.

## 2. Primary problem, target workloads, concrete example workflows

**Primary problem.** Large organisations hold operational data in many systems and cannot act on it coherently. Foundry handles this in three steps [CLAIM-palantir-foundry-01] [CLAIM-palantir-foundry-18] [CLAIM-palantir-foundry-22]:

1. It integrates the data into versioned datasets.
2. It maps the datasets onto an Ontology of business objects.
3. Operational applications, AI logic and agents read those objects, and they change them only through governed **actions** that write back.

**Target segments.** Defence and intelligence, government, manufacturing, supply chain, energy, healthcare and financial services. Claimed accreditations are FedRAMP High, DoD IL5/IL6 and CMMC [CLAIM-palantir-foundry-08].

**Concrete workflows.** The building blocks are documented; the scenarios themselves are illustrative.

1. **Operational decision app** [CLAIM-palantir-foundry-18] [CLAIM-palantir-foundry-02] [CLAIM-palantir-foundry-22]
   - Sources flow through a connector into a dataset (batch, incremental or streaming).
   - A Pipeline Builder transform produces the backing datasource for object type `WorkOrder`, which links to `Asset` and `Technician`.
   - A Workshop app offers the action `ReassignWorkOrder`, with parameters, submission criteria and a notification side effect.
   - Edits land in the writeback dataset, and Funnel indexes them.
2. **AI-assisted triage** [CLAIM-palantir-foundry-11]
   - An AIP Logic function reads an object set, and an LLM proposes a classification.
   - A human confirms it, and an action commits it.
   - AIP Evals evaluates the function.
3. **Custom product on Foundry** [CLAIM-palantir-foundry-06]
   - A developer generates an OSDK (TypeScript, Python or Java) scoped to a subset of the Ontology and builds an external app on it.
   - The app receives real-time updates over WebSocket subscriptions.
4. **External agent access** [CLAIM-palantir-foundry-15]
   - An Ontology MCP server exposes a Developer Console application's object types, action types and query functions as MCP tools.
   - Application scopes bound what the agent can do.
5. **Disconnected deployment** [CLAIM-palantir-foundry-08] [CLAIM-palantir-foundry-09]
   - Apollo plans install, upgrade and rollback of Foundry/AIP services.
   - Bundles are moved into air-gapped networks, where they are scanned and integrity-checked.

**Fit for on-prem, local-first operation.** On-prem and classified operation is **documented**. One-node or small-footprint operation is not documented, and the architecture points the other way (see §9 and §10).

## 3. Feature inventory

| Area | Feature | Status | Evidence |
|---|---|---|---|
| Ontology | Object types, properties, shared properties | Present | CLAIM-palantir-foundry-01 |
| Ontology | Link types (two-sided, self-links, M:N links backed by a datasource); **no cross-Ontology links** | Present / limitation | CLAIM-palantir-foundry-17 |
| Ontology | Interfaces (polymorphism over object types) | Present | CLAIM-palantir-foundry-01 |
| Ontology | Action types (parameters, rules, submission criteria, side effects including notifications and webhooks, writeback dataset, action log) | Present | CLAIM-palantir-foundry-18 |
| Ontology | Functions (code logic that reads objects and object sets; Functions on Objects) | Present | CLAIM-palantir-foundry-01, -02 |
| Ontology | Object Views and object sets (temporary sets expire within 24h) | Present | CLAIM-palantir-foundry-01, -04 |
| Ontology | Formal semantics (OWL/RDFS reasoning, SHACL) | Absent: no documentation found, and the vendor says "not a semantic layer" | CLAIM-palantir-foundry-13 |
| Ontology | Ontology-as-code | Beta / uncertain | CLAIM-palantir-foundry-20 |
| Ontology | Packaging as Marketplace "products" with release channels | Present | CLAIM-palantir-foundry-19 |
| Backend | Object Storage v2: separate indexing and query subsystems; incremental indexing by default; streaming datasources; 2,000 properties per type; Search Around default 100k; 10k objects per action | Present | CLAIM-palantir-foundry-03, -04, -05 |
| Backend | Edit migration after a breaking schema change | Present | CLAIM-palantir-foundry-05 |
| Data | Connectors to datasets, streams, CDC streams and media sets; listeners (HTTPS, WebSocket, email) | Present | CLAIM-palantir-foundry-22 |
| Data | Pipeline Builder; Code Repositories (Python, Java, SQL); batch, incremental and streaming (Flink) processing | Present | CLAIM-palantir-foundry-22 |
| Data | Datasets versioned by transactions with full history; Iceberg/Parquet storage; REST, JDBC and S3-compatible access; virtual tables over Databricks, Snowflake and BigQuery | Present | CLAIM-palantir-foundry-21 |
| Change management | Global Branching across applications, with proposals and review | Present | CLAIM-palantir-foundry-21 |
| Security | Projects (primary boundary), Organizations (mandatory silos), roles (Owner, Editor, Viewer, Discoverer) | Present | CLAIM-palantir-foundry-13 |
| Security | Markings: mandatory, conjunctive, propagated through the folder hierarchy and data lineage | Present | CLAIM-palantir-foundry-14 |
| Security | Row- and column-level (property-level) permissions via multi-datasource object types | Present (OSv2) | CLAIM-palantir-foundry-05 |
| Security | Classification-based access control (CBAC) | Present: named in the docs, not read in detail | CLAIM-palantir-foundry-06 |
| AI | AIP Logic, AIP Chatbot Studio (formerly Agent Studio), AIP Evals, AIP Assist, Threads, Automate | Present | CLAIM-palantir-foundry-11 |
| AI | LLM proxy endpoints (Anthropic and OpenAI native formats); Bring Your Own Model | Present | CLAIM-palantir-foundry-13 |
| AI | Self-hosted models in compute modules (vLLM and Ollama examples); air-gapped use case listed | Present | CLAIM-palantir-foundry-12 |
| Agents | Ontology MCP (data reads, and governed writes via actions) | Present | CLAIM-palantir-foundry-15 |
| Agents | Palantir MCP (70+ tools to edit ontology structure; cannot write data) | Beta | CLAIM-palantir-foundry-15 |
| SDK | OSDK: TypeScript (npm), Python (pip/conda), Java (Maven), plus OpenAPI for other languages; scoped tokens; WebSocket subscriptions | Present | CLAIM-palantir-foundry-06 |
| UI | Workshop (low-code), Slate (code-first), Object Views, Developer Console hosting | Present | CLAIM-palantir-foundry-13 |
| Operations | Rubix Kubernetes; Apollo install, upgrade and rollback with blue/green; nodes live at most 48h | Present | CLAIM-palantir-foundry-08 |
| Operations | Air-gapped and classified delivery via Apollo | Present (official blog, read only via search snippet) | CLAIM-palantir-foundry-09 |
| Deployment | AWS, Azure, GCP, Oracle Cloud and on-premises; NVIDIA sovereign reference architecture | Present / announced | CLAIM-palantir-foundry-08, -10 |
| Query languages | Gremlin, Cypher, SPARQL or GQL over the Ontology | Absent: no documentation found; access is through OSS APIs, the OSDK and functions | reasoned from CLAIM-palantir-foundry-02, -06 |
| Tenancy/OEM | White-label or OEM redistribution of Foundry | Unknown: no public OEM terms | — |
| Pricing | Contract pricing; compute-second metering documented for some workloads | Partial public information | CLAIM-palantir-foundry-16 |

## 4. Text-based architecture diagram

```
                     ┌──────────────────────────── CONTROL PLANE ─────────────────────────────┐
                     │ Apollo: plans install/upgrade/rollback, blue/green, constraint-based  │
                     │         delivery; bundle transfer into air-gapped hubs                 │
                     │ Rubix:  hardened K8s; every workload authenticated, authorised, logged;│
                     │         nodes recycled <=48h; AWS / Azure / GCP / OCI / on-prem        │
                     └──────────────────────────────────┬─────────────────────────────────────┘
                                                        │ manages every service below
 SOURCES               DATA LAYER (versioned)              OBJECT LAYER (Ontology)                CONSUMERS
 ┌─────────┐ connectors ┌───────────────────────┐ backing ┌────────────────────────────────┐   ┌───────────────────────┐
 │ ERP/CRM │──streams,──►│ Datasets (txn history)│─datasrc─►│ Ontology Metadata Service      │   │ Workshop / Slate /    │
 │ DBs,    │  CDC, media,│ Iceberg / Parquet     │         │ (object/link/action types,     │   │ Object Views          │
 │ files,  │  listeners  │ Pipeline Builder,     │         │  interfaces, shared props)     │   ├───────────────────────┤
 │ APIs,   │             │ Code Repos, Flink     │ Funnel  │ Object Data Funnel ──index───► │◄──┤ OSDK (TS / Py / Java) │
 │ streams │             │ Data Expectations     │────────►│ Object databases (OSv2:        │   │ REST Ontology APIs    │
 └─────────┘             └───────────┬───────────┘         │  indexing ≠ querying)          │   │ WebSocket subscribe   │
                                     │ writeback dataset ◄─│ Object Set Service (search,    │   ├───────────────────────┤
                                     │ (user edits)        │  filter, aggregate, Search     │   │ AIP Logic / Chatbot   │
                                     │                     │  Around; Spark exec at scale)  │   │ Studio / Assist /     │
                                     │                     │ Actions service (validated     │◄──┤ Evals / Automate      │
                                     │                     │  edits, side effects, webhooks)│   │ Ontology MCP (scoped) │
                                     │                     │ Functions on Objects           │   │ Palantir MCP (struct.)│
                                     │                     └────────────────────────────────┘   └───────────────────────┘
 SECURITY (cross-cutting): Organizations (mandatory) ∧ Markings (mandatory, conjunctive, lineage-propagated)
   ∧ Roles on Projects (discretionary) ∧ row/column policies on multi-datasource object types ∧ CBAC ∧ audit logs
 AI EGRESS: LLM proxy (Anthropic/OpenAI formats) | BYOM | self-hosted model in a compute module (no external connectivity)
```

State lives in two places:

- **Data layer:** versioned datasets.
- **Object layer:** indexed object databases. Funnel keeps the object layer derived from the sources plus the edit log.

The Apollo/Rubix control plane is separate from the data plane.

## 5. Under-the-hood reconstruction

The architecture is proprietary. Every statement below is either **documented** (with a CLAIM-ID) or a **hypothesis** (marked H). This is a blueprint for building equivalent behaviour. It does not describe Palantir's code, which was not inspected and must not be copied.

### 5.1 Data model

- **Object type.** The schema for an entity or event, with properties. Each object is one instance, and the documentation compares an object to a row in a dataset [CLAIM-palantir-foundry-01].
  - *H1:* every object type has a primary-key property from its backing datasource, and object identity is `(objectTypeRid, primaryKey)`. This fits the row analogy, but the fetched page does not state it explicitly.
- **Multi-datasource object types (OSv2).** One object type can be assembled from several datasources, with property-level permissions per datasource [CLAIM-palantir-foundry-05].
  - In effect this **splits an entity's properties by permission domain**, a pattern worth noting for EOIP's per-fact ACLs.
- **Shared properties and interfaces.** Shared properties are reusable property definitions with central metadata. An interface describes a shape that several object types can implement [CLAIM-palantir-foundry-01]. Together they give nominal polymorphism without an OWL class hierarchy.
- **Link types** [CLAIM-palantir-foundry-17]:
  - Two-sided, and each side can be traversed independently.
  - Several link types can connect the same pair of types, and self-links are allowed.
  - Many-to-many links are **backed by their own datasource** (a join table).
  - Other links resolve through the backing datasources of the linked types. *H2:* a foreign-key column on the "many" side.
  - **Links cannot span Ontologies.**
- **Edges carry no documented properties.** *H3:* relationship attributes are modelled as an intermediate object type. This matters because EOIP's LPG backends support edge properties natively (CAP-11).
- **Action types.** Typed, parameterised transactions over objects, properties and links, with rules, submission criteria and side effects [CLAIM-palantir-foundry-18].

```
ObjectType { rid, apiName, primaryKey (H1), properties[PropertyDef | SharedPropertyRef], interfaces[], datasources[] }
LinkType   { rid, sideA:{objectType, apiName, cardinality}, sideB:{...}, backing: FK (H2) | Datasource (M:N) }
ActionType { rid, parameters[], rules[createObject|modifyObject|deleteObject|createLink|deleteLink|function],
             submissionCriteria[], sideEffects[notification|webhook], permissions }
Interface  { rid, properties[SharedPropertyRef], implementedBy[ObjectType] }
```

### 5.2 Storage layout and indexing

- **Documented** [CLAIM-palantir-foundry-03] [CLAIM-palantir-foundry-04]:
  - OSv2 **separates indexing and querying subsystems**, so it can "scale horizontally more easily".
  - Incremental indexing is on by default.
  - Streaming datasources give low-latency indexing.
  - Vendor claim: indexing throughput "on the order of tens of billions of objects for a single object type".
- **Documented:** **Funnel** reads datasources and user edits, indexes them into object databases, and keeps them current as sources change [CLAIM-palantir-foundry-02].
- **NOT PUBLICLY VERIFIED:** the physical engine behind the "object databases".
  - *H4:* a search-engine-style inverted index with columnar values for filtering and aggregation, sharded by object type.
  - In this model, Search Around is an index lookup on link keys, and large Search Arounds and accurate aggregations go to the documented Spark-based execution layer [CLAIM-palantir-foundry-04].

Reconstruction of the derived-view pattern (hypothesis):

```
# Funnel-equivalent: object view = f(source snapshot, edit log), recomputed incrementally
on source_txn(ds, delta_rows):
    for row in delta_rows:
        pk    = row[ds.pk_column]
        base  = project(row, ds.property_map)
        edits = edit_log.latest(objtype, pk)                 # H5: user edits win over source values
        doc   = merge(base, edits, policy=objtype.conflict_policy)
        index.upsert(objtype, pk, doc,
                     acl=derive_acl(ds.markings, ds.row_policy, ds.column_policy))
on action_commit(edits):
    edit_log.append(edits)                                    # writeback dataset = durable edit log
    for e in edits:
        index.upsert(e.objtype, e.pk, merge(index.get(e.objtype, e.pk), e))
```

*H5:* user edits override source values according to a per-type policy. The documented ability to "migrate user edits after a breaking schema change" [CLAIM-palantir-foundry-05] implies that edits are stored keyed by `(objectType, pk, property)` in a form that can be re-mapped when the schema changes.

### 5.3 Query pipeline and planning

- **Documented:** reads go through the **Object Set Service**: search, filter, aggregate, load and Search Around [CLAIM-palantir-foundry-02]. Clients compose object sets declaratively via the OSDK or REST APIs [CLAIM-palantir-foundry-06].
- No public graph query language over the Ontology was found.
- Traversal is a **bounded Search Around** (default 100,000 objects), not arbitrary path queries [CLAIM-palantir-foundry-04]. This intentional bound resembles EOIP's typed, bounded `QueryPlan` (BL-08).
- *H6:* an object-set expression compiles into an operator tree (`base(type) → filter → searchAround(link) → filter → aggregate`). The tree runs against the index and moves to the Spark path above a size threshold.

```
ObjectSet := Base(objectType) | Filter(ObjectSet, predicate) | SearchAround(ObjectSet, linkApiName)
           | Union / Intersect / Subtract(ObjectSet, ObjectSet) | Static(pks) | Temporary(id, ttl <= 24h)
Aggregate(ObjectSet, groupBy[], metrics[])
```

### 5.4 Reasoning

No logical reasoning is documented. Derived knowledge comes from three sources [CLAIM-palantir-foundry-01] [CLAIM-palantir-foundry-11]:

- **Pipelines:** transforms over datasets.
- **Functions:** code over objects.
- **AIP Logic:** LLM-backed functions.

There is no open-world inference, no OWL or Datalog materialisation, and no documented proof trace. Explanations come from lineage and action logs. EOIP should not chase Palantir on reasoning, because Palantir does not compete there.

### 5.5 Concurrency and transactions

- **Documented:** an action is "a single transaction that changes the properties of one or more objects" [CLAIM-palantir-foundry-18]. In OSv2 one action can edit up to 10,000 objects by default [CLAIM-palantir-foundry-04].
- **Documented:** datasets use **transactions** with full history [CLAIM-palantir-foundry-21].
- **NOT PUBLICLY VERIFIED:** the isolation level, and how concurrent actions on the same object resolve.
  - *H7:* optimistic per-object concurrency with last-writer-wins on properties. No documentation describes locking.

### 5.6 Partitioning and consistency

OSv2 scales horizontally [CLAIM-palantir-foundry-03].

*H8:* writes reach readers with eventual consistency (source transaction → Funnel → index). The documented wording "faster observation of user edits" [CLAIM-palantir-foundry-05] implies a measurable delay before a writer sees its own edits, not synchronous visibility.

### 5.7 Caching

NOT PUBLICLY VERIFIED. The only documented server-side result cache is temporary object sets, which last at most 24h [CLAIM-palantir-foundry-04].

### 5.8 Versioning

- Datasets are versioned by transaction [CLAIM-palantir-foundry-21].
- **Global Branching** lets one branch span several applications and merge through proposals with review [CLAIM-palantir-foundry-21].
- **Marketplace products** package an Ontology or a fragment of one, with release channels [CLAIM-palantir-foundry-19].
- User edits can be migrated after breaking schema changes [CLAIM-palantir-foundry-05].
- Not documented in the sources read: bitemporal valid-time queries over objects. EOIP has an application-layer bitemporal model (BL-37).

### 5.9 Security

Effective access is the conjunction of several controls:

```
can_read(user, object, property) :=
     user ∈ allowed(Organization(resource))                                        # mandatory silo
  ∧  ∀ m ∈ markings(resource) ∪ inherited_markings(lineage(resource)): user holds m  # conjunctive, propagated
  ∧  role(user, project(resource)) ≥ Viewer                                         # discretionary
  ∧  row_policy(object, user) ∧ column_policy(property, user)                       # OSv2 multi-datasource types
```

- Markings propagate through the file hierarchy and through data dependencies "unless the marking is explicitly removed". Removing one requires a specific "Expand Access" permission [CLAIM-palantir-foundry-14].
- OSDK tokens are scoped to selected ontological entities and intersected with the user's permissions [CLAIM-palantir-foundry-06].
  - Palantir notes that row and column controls do not govern what an application does with the response, and recommends markings or CBAC for that.
- Ontology MCP carries a documented warning that external LLM clients gain access to the data [CLAIM-palantir-foundry-15].

**Lesson for EOIP:** the most valuable pattern here is the mandatory label that propagates along lineage.

- EOIP already records `PermissionMetadata` and `acl_hash` on every SourceEvent (BL-17).
- It does not yet propagate those labels to derived facts.
- It does not enforce them at retrieval (BL-18 is Absent).

## 6. Functional and non-functional requirements inferred from verified behaviour

| # | Requirement inferred | Source behaviour |
|---|---|---|
| FR-1 | Object and relationship types with shared property definitions and interfaces (polymorphism) | CLAIM-palantir-foundry-01 |
| FR-2 | Every user or agent write goes through a typed, validated, permissioned action type with side effects and an action log | CLAIM-palantir-foundry-18 |
| FR-3 | Writes are persisted to a durable edit log that is merged with source-derived state, and edits survive schema migration | CLAIM-palantir-foundry-02, -05 |
| FR-4 | Mandatory, conjunctive security labels propagate along lineage to every derived artefact | CLAIM-palantir-foundry-14 |
| FR-5 | Property-level permissions when one entity draws on sources of different sensitivity | CLAIM-palantir-foundry-05 |
| FR-6 | Generated, ontology-scoped, typed client SDKs in at least 3 languages, plus OpenAPI | CLAIM-palantir-foundry-06 |
| FR-7 | A scoped MCP server exposes types, query functions and actions to external agents, separate from an MCP server for editing structure | CLAIM-palantir-foundry-15 |
| FR-8 | Self-hosted LLM inference sits behind the same model abstraction as hosted providers and works offline | CLAIM-palantir-foundry-12 |
| FR-9 | Branches that span applications, with proposals and review | CLAIM-palantir-foundry-21 |
| NFR-1 | Bounded traversal: default caps that an operator can raise | CLAIM-palantir-foundry-04 |
| NFR-2 | Zero-downtime upgrades with planned rollback in disconnected environments | CLAIM-palantir-foundry-08, -09 |
| NFR-3 | A security posture that can be accredited (FedRAMP High, IL5/IL6) | CLAIM-palantir-foundry-08 |

## 7. Performance and resource model

- **No benchmarks or sizing.** No independent benchmark of Foundry or the Ontology backend was found, and no public hardware sizing exists for a minimum Foundry install.
- **Vendor claim (Unverified; no workload or hardware stated):** OSv2 indexing throughput "on the order of tens of billions of objects for a single object type" [CLAIM-palantir-foundry-04].
- **Documented operating limits** [CLAIM-palantir-foundry-04]:
  - 2,000 properties per object type.
  - Search Around default of 100,000 objects.
  - 10,000 objects per action.
  - Temporary object sets last at most 24h.
  - The Search Around and action limits can be raised through Palantir Support.
- **Resource model (reasoned inference, confidence 0.5).** The practical floor is a multi-node Kubernetes cluster plus a control plane, far above EOIP's one-node target (Constraint 10). Two documented facts support this:
  - Rubix requires every service to run multi-node with blue/green rollouts, and it recycles nodes within 48h [CLAIM-palantir-foundry-08].
  - The on-prem reference design is an NVIDIA Blackwell Ultra GPU datacenter [CLAIM-palantir-foundry-10].
- **Failure modes (documented or inferred):**
  - Search Around hits its cap. The cap is documented; what happens on truncation is UNVERIFIED.
  - Index lag between a source transaction and the object becoming visible (H8).
  - Actions over 10k objects are rejected.
  - Migration risk for customers who had not moved from OSv1 to OSv2 by 2026-06-30 [CLAIM-palantir-foundry-03].
- **Cost model:** contract pricing [CLAIM-palantir-foundry-16].
  - At least some compute is metered in "Foundry compute-seconds". Code workspaces have published default rates: no-GPU JupyterLab 0.1, T4 GPU 1.2, V100 3.0.
  - The documentation tells enterprise-contract customers to consult their representative.

## 8. Strengths and use-case-specific advantages, and how each could be matched or exceeded

1. **Actions are the only governed write path** [CLAIM-palantir-foundry-18]. They tie data, logic and user edits together in one transaction, with side effects.
   - *Match:* EOIP has a validation gate on ingest (BL-28) and read-only agents by design (BL-47), but no action-type model for users or agents.
   - *Exceed:* make action types produce PROPOSED claims with evidence (BL-40) that become facts on approval. This is epistemic separation, which Foundry does not document.
2. **Mandatory markings that propagate along lineage** [CLAIM-palantir-foundry-14].
   - *Match:* P0 for EOIP (BL-18).
   - *Exceed:* propagate labels into embeddings, caches and agent memory, and re-check them on revocation (J5).
3. **Property-level security via multi-datasource objects** [CLAIM-palantir-foundry-05].
   - *Match:* attribute each property to its source in EOIP revisions (BL-37, BL-41).
4. **Typed SDKs generated from the ontology** [CLAIM-palantir-foundry-06].
   - *Match:* generate TypeScript and Python clients from EOIP's ontology manifest and OpenAPI.
5. **Two MCP tiers: a data-plane MCP with scoped, governed writes, and a separate MCP for editing structure** [CLAIM-palantir-foundry-15].
   - *Match / exceed:* EOIP's MCP is read-only (BL-47). Add action-type tools that create PROPOSED changes behind review.
6. **Accredited air-gapped continuous delivery with rollback** [CLAIM-palantir-foundry-08] [CLAIM-palantir-foundry-09].
   - *Match in kind, not scale:* signed offline bundles for Compose and Helm, a reproducible upgrade and rollback plan, and verified SBOMs (CAP-79).
7. **Self-hosted models are first-class AIP models** [CLAIM-palantir-foundry-12].
   - EOIP's default is already local (Ollama in Compose; egress level S0, BL-45).
   - *Exceed:* policy-graded egress levels and a manifest for every call.
8. **Branching across ontology and apps, with edit migration after schema changes** [CLAIM-palantir-foundry-05] [CLAIM-palantir-foundry-21].
   - *Match:* extend ontology GitOps (BL-32) to migrate human assertions across breaking changes (CAP-37).
9. **Breadth of the integrated data platform**: pipelines, streaming, data-quality checks, Iceberg storage [CLAIM-palantir-foundry-21] [CLAIM-palantir-foundry-22].
   - *Integrate, do not build:* EOIP should consume lakehouse and ETL tools (C14), not rebuild a data platform.

## 9. Limitations with root causes

**Verified defects.** None found in public sources. Security advisories were not searched.

**Intentional trade-offs (documented):**

- Bounded Search Around (100k default), 10k objects per action, no cross-Ontology links, and temporary sets that last at most 24h [CLAIM-palantir-foundry-04] [CLAIM-palantir-foundry-17].
- "Not a semantic layer": no formal reasoning and no standards-based semantics [CLAIM-palantir-foundry-13].

**Licensing and commercial restrictions:**

- Proprietary, with contract-only pricing and no public price list [CLAIM-palantir-foundry-16].
- No public OEM or white-label terms (Unknown).
- The osdk-ts licence is unverified [CLAIM-palantir-foundry-07].

**User-reported complaints:**

- A community thread shows confusion about whether Ontology-as-Code still exists. An older thread says the GUI was the only supported way to manage the ontology [CLAIM-palantir-foundry-20].
- Third-party "negotiation advisory" pages describe high, opaque contract costs. These are Unverified and not used as evidence.

**Outdated claims to avoid:** "Palantir is SaaS-only and cannot run on-prem" is false. On-prem operation, IL5/IL6 accreditation and air-gapped delivery are all documented [CLAIM-palantir-foundry-08] [CLAIM-palantir-foundry-09].

**Hypotheses:**

- Edits reach readers with eventual consistency (H8).
- Edges have no properties (H3).
- The ontology's semantics lock customers in, because no standards export is documented. This rests on absence of evidence (confidence 0.4).

**Root causes:**

| Class | Root cause | Status |
|---|---|---|
| Algorithmic dead end | Traversal is bounded set expansion, not a path algebra. Deep multi-hop impact analysis (J1, J9) needs chained Search Arounds, each capped at 100k | Caps proven; depth cost is a hypothesis |
| Algorithmic dead end | No logical inference. Derived facts need pipelines or code, so there is no incremental truth maintenance and no proof trace | Proven by absence and by the vendor's statement |
| Operational and hardware overhead | Multi-node Kubernetes, blue/green for every service, 48h node cycling, a GPU datacenter as the reference design | Requirements proven (documented); size floor is inference |
| Operational and hardware overhead | Upgrades follow the vendor-operated Apollo release train. Customer control over version pinning is undocumented | Hypothesis |
| User and developer friction | Proprietary modelling primitives and APIs (OSDK, Functions, Workshop). Ontology-as-code status is unclear and authoring is GUI-centric | Proven (community) / partial |
| User and developer friction | Contract-only pricing with compute-second metering is hard to forecast | Metering documented; cost impact from third parties |

## 10. Deployment, licensing, redistribution, and operational viability under EOIP constraints

| EOIP constraint | Palantir position | Evidence |
|---|---|---|
| 1. Self-hosted, air-gap capable | **Yes**, for customers that can operate Rubix and Apollo: on-prem, IL5/IL6, air-gapped delivery | CLAIM-palantir-foundry-08, -09, -10 |
| 2. Default-local LLM, egress policy | Possible with self-hosted models; proxy endpoints to Anthropic and OpenAI are documented. The default posture per deployment is not documented | CLAIM-palantir-foundry-12, -13 |
| 3. Backend neutrality | N/A. Proprietary object store; reads external lakehouses through virtual tables | CLAIM-palantir-foundry-21 |
| 4. Connectors never mutate the graph directly | **Aligned in spirit:** sources → datasets → Funnel → index; user edits only through actions | CLAIM-palantir-foundry-02, -18 |
| 8. Permissions survive everything | **Strong:** markings propagate along lineage | CLAIM-palantir-foundry-14 |
| 9. Tenant isolation / white-label | Organizations are mandatory silos. No public white-label or OEM programme | CLAIM-palantir-foundry-13 |
| 10. One-node first | **No:** multi-node is required by design | CLAIM-palantir-foundry-08 |
| 12. Redistribution-safe licensing | Not a component EOIP would redistribute. Integration through public APIs only | — |

**Viability as a component for EOIP:** none is needed.

**Viability as an integration target:** two integrations are plausible and lawful through public APIs:

- A Foundry **source connector** that reads objects through the OSDK or REST into SourceEvents.
- A Foundry **sink** that publishes EOIP-derived evidence back as a dataset.

Any OSDK library used would need a licence review.

## 11. Competitive delta against the EOIP verified baseline

| Capability | Palantir (evidence) | EOIP baseline | Delta |
|---|---|---|---|
| Ontology primitives (types, interfaces, shared properties) | Rich and in production (CLAIM-01) | Fixed label manifest; ontology modules; GitOps partial (BL-32) | **EOIP behind** on interfaces and on the authoring UX for shared properties |
| Governed write path for humans and agents | Action types with validation and side effects (CLAIM-18) | Validation gate on ingest (BL-28); agents read-only (BL-47) | **EOIP behind** on human and agent actions |
| Source-ACL enforcement in retrieval | Markings propagated along lineage (CLAIM-14) | Captured (BL-17) but **not enforced** (BL-18 Absent) | **EOIP P0 gap** |
| Tenant isolation | Organizations (mandatory) | Contract only; adapters not tenant-aware (BL-20) | **EOIP P0 gap** |
| Evidence, claims, epistemic separation | Not documented | Claims, contradictions, PROPOSED-until-promoted (BL-39, BL-40) | **EOIP ahead** (needs verifying in deployments) |
| Bitemporal / as-of queries | Dataset transaction history; no documented valid-time object queries | Bitemporal revisions (BL-37); diff and playback (BL-38) | **EOIP ahead** at the application layer |
| Formal semantics (OWL/SHACL/JSON-LD) | Absent ("not a semantic layer") | Partial in-house subsets (BL-29, BL-30, BL-31) | **EOIP ahead in kind**; conformance unproven (U-07) |
| Backend neutrality | Proprietary store | GraphStore protocol over 6 adapters (BL-01..06) | **EOIP differentiator** |
| One-node / small footprint | Multi-node Kubernetes | Docker Compose on a single host (`deploy/`) | **EOIP differentiator** |
| Air gap | Documented and accredited | A design goal: Ollama local, offline licence (BL-22). No live air-gap test run | **Parity in claim; Palantir ahead in proof** |
| Generated SDKs | OSDK in 3 languages (CLAIM-06) | None | **EOIP behind** |
| MCP | Ontology MCP, plus Palantir MCP in beta (CLAIM-15) | 18 read-oriented tools (BL-47) | Parity on reads; **EOIP behind** on governed writes |
| Data integration platform | Extensive (CLAIM-22) | 30+ connectors, SourceEvent, replay, DLQ (BL-23, BL-24) | Palantir ahead on breadth; EOIP's event log is a sound base |
| Accreditation | FedRAMP High, IL5/IL6, CMMC (CLAIM-08) | None | **EOIP behind**: a procurement gate in the public sector |
| White-label / OEM | Unknown; not offered publicly | Branding, terminology, localisation (BL-21) | **EOIP differentiator** |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

### 12.1 Strength-adoption cards

| STR-ID | Competitor | Strength | Evidence | Value to EOIP customers | Decision | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-palantir-foundry-01 | Palantir Foundry | Action types are the only edit path: typed, parameterised, permissioned transactions with submission criteria and side effects | CLAIM-palantir-foundry-18, -04 | Humans and agents can write back to operational data safely | **Match + exceed** | An `ActionType` contract with a parameter schema, preconditions as SHACL-style shapes, a permission policy and side-effect hooks. Execution emits a governed mutation through the validation gate. Actions invoked by an agent default to PROPOSED (BL-40) | An action that violates its preconditions is rejected with a reason. An agent action lands as PROPOSED and is promoted only after approval. The audit log records actor, parameters and diff |
| STR-palantir-foundry-02 | Palantir Foundry | Mandatory, conjunctive markings that propagate through the folder hierarchy and data lineage | CLAIM-palantir-foundry-14 | Permissions stay safe across derived facts, summaries and indexes | **Match (P0)** | Security labels on SourceEvents (BL-17). Every derived vertex, edge, claim and embedding inherits the union of its inputs' labels. Retrieval filters on `labels ⊆ user.clearances` | J5 test with two users holding different clearances: zero leaked facts, chunks or citations, and revocation invalidates caches within the SLA |
| STR-palantir-foundry-03 | Palantir Foundry | Property-level permissions on entities built from several sources | CLAIM-palantir-foundry-05 | One "Customer" view that does not expose HR or finance fields | **Match** | Revisions record each property's source and label. A projection layer drops properties the caller may not see | The same entity read by two roles returns different property sets. No hidden property value appears in any answer or citation for the less-privileged role |
| STR-palantir-foundry-04 | Palantir Foundry | Generated, ontology-scoped, typed SDKs (TypeScript, Python, Java) plus OpenAPI | CLAIM-palantir-foundry-06 | Customers build apps on EOIP faster | **Match** | Generate clients from the ontology manifest and OpenAPI, with scoped tokens per app | The generated TypeScript and Python clients compile. A typed query and action round trip works against a tenant. Regenerating after an ontology change produces a semver-correct diff |
| STR-palantir-foundry-05 | Palantir Foundry | Separate MCP surfaces: one for data and actions (scoped), one for ontology structure | CLAIM-palantir-foundry-15 | Agents can act without being able to restructure the model | **Match + exceed** | EOIP MCP adds `propose_action` tools. Structure edits go only through GitOps pull requests. The egress gateway checks where the client's model runs | An external MCP client scoped to X cannot call actions outside X. Ontology edits through MCP only create pull requests. Every call carries an egress manifest |
| STR-palantir-foundry-06 | Palantir Foundry | Accredited air-gapped continuous delivery with planned rollback (Apollo) | CLAIM-palantir-foundry-08, -09 | Regulated buyers can run offline and upgrade safely | **Match (scaled down)** | A signed offline bundle (images, SBOM, migration plan), `eoipctl plan/apply/rollback`, and preflight checks | J16: install, upgrade from N to N+1 and roll back on an offline host. Signatures are verified. No outbound connections are observed |
| STR-palantir-foundry-07 | Palantir Foundry | Edit migration across breaking schema changes; branches that span apps, with proposals | CLAIM-palantir-foundry-05, -21 | Ontology changes do not lose human work | **Match** | Ontology change records (BL-32) carry migration functions for human assertions. A dry run lists the assertions affected | J4: rename or split a property. Every approved assertion is migrated or flagged, and rollback restores the prior state |
| STR-palantir-foundry-08 | Palantir Foundry | Interfaces and shared properties for polymorphic modelling | CLAIM-palantir-foundry-01 | Models reused across domains (e.g., `Asset` across IT and OT) | **Match** | Interfaces in the ontology manifest compile to SHACL shapes or labels per backend | A query by interface returns every implementing type on HugeGraph, Neo4j and Neptune (J14) |

### 12.2 Con-to-Pro inversion cards

#### INV-palantir-foundry-01: heavyweight multi-node platform vs one-node air-gapped deployment (seed hypothesis partly validated, partly rejected)

- **Target, version, workload:** Foundry/AIP on Rubix and Apollo, as documented in October 2026. The workload is a mid-size organisation (up to 5,000 users) that needs an offline knowledge graph.
- **Evidence-supported limitation:** no small or single-node footprint is documented. The documented requirements point the other way [CLAIM-palantir-foundry-08] [CLAIM-palantir-foundry-10]:
  - Every service must run multi-node with blue/green rollouts.
  - Nodes are recycled within 48h.
  - The on-prem reference design is a GPU datacenter.
- **Verdict on the seed hypothesis (Master Prompt §10.5):**
  - "Limited on-prem/air-gap" is **REJECTED** for Palantir. On-prem operation, IL5/IL6 accreditation and air-gapped delivery are documented [CLAIM-palantir-foundry-08] [CLAIM-palantir-foundry-09] [CLAIM-palantir-foundry-12].
  - "Heavyweight deployment" is **VALIDATED** by the documented architecture.
  - "SaaS" is **REJECTED** as a blanket statement. SaaS is common, but it is not the only model.
- **Root cause:** deployment and coupling. The platform is built for high availability and accreditation at large scale (*proven*, from documented requirements). The cost of a small install is a *hypothesis*, because no sizing is published.
- **Why the alternative mitigates it, and when it would be worse:**
  - A single-host Compose deployment, with HA as an option, lets small and remote sites run the full stack: factories, ships, branch offices, sovereign SMEs.
  - It would be worse for large multi-site programmes that need zero-downtime upgrades and accredited operations. Palantir's model wins there, and EOIP's one-node posture is not a selling point.
- **Options:**
  - (a) *Quick:* document a "single-node air-gap profile" of the existing Compose stack, with an offline bundle.
  - (b) *Pragmatic:* a signed bundle plus a plan/apply/rollback tool, with preflight checks and an SBOM.
  - (c) *Long-term:* the same artefacts scale from one node to a Helm/Kubernetes HA topology with no data migration ("one-node first, cluster later").
- **Selected:** (b) now, and (c) on the roadmap. The pattern is immutable, versioned bundles applied through a declarative plan.

  ```
  eoipctl bundle verify eoip-2026.11.tar --sig eoip.pub
  eoipctl plan     --from 2026.10 --to 2026.11   # shows image, schema and ontology migrations
  eoipctl apply    --plan plan.json --backup auto
  eoipctl rollback --to 2026.10
  ```

- **Falsifiable POC (proposed benchmark):**
  - Setup: one host with 16 vCPU, 64 GB RAM and 1 TB disk, and no network.
  - Steps: install; ingest a synthetic digital-thread dataset of 5M vertices and 20M edges; run the J1/J9 query set and local-LLM answers.
  - Success: install in under 60 minutes, p95 bounded query under 2 s, upgrade and rollback with no data loss, zero egress packets.
  - Cost baseline: one server.
- **Dependencies, migration, security failure cases:**
  - Depends on the offline licence (BL-22), backup and restore (BL-50), and SBOM signing (CAP-79).
  - Failure cases needing negative tests: an unsigned image is accepted; a rollback after a schema migration corrupts revisions.
- **Defensibility:** moderate. Palantir could ship a small edition, but its accreditation-driven architecture and enterprise sales model make a low-cost single-node SKU commercially unlikely (*hypothesis*). The value lasts because EOIP is also white-label and multi-backend.
- **Decision:** **ADOPT**.

#### INV-palantir-foundry-02: proprietary ontology semantics vs an open, exportable ontology and evidence

- **Target:** the Foundry Ontology (OMS, action types, functions), October 2026.
- **Evidence-supported limitation:**
  - The Ontology is proprietary and "not a semantic layer" [CLAIM-palantir-foundry-13].
  - Data can leave as Iceberg or Parquet and through JDBC or REST [CLAIM-palantir-foundry-21], but the sources read show no OWL, RDFS, SHACL or JSON-LD export of the *model*.
  - Ontology-as-code is a beta of uncertain status [CLAIM-palantir-foundry-20].
  - Marketplace product packaging stays inside Foundry [CLAIM-palantir-foundry-19].
- **Root cause:** semantics plus licensing and commercial model. The model, actions and functions execute only inside the platform (*proven* for execution). The lack of a standards export is a *hypothesis* resting on absence of evidence (confidence 0.4).
- **Why the alternative mitigates it, and when it would be worse:**
  - Keeping the ontology as code (Turtle, LinkML or YAML) with SHACL, exporting to JSON-LD with loss accounting (BL-31), and exporting evidence as PROV-O gives customers an exit path and portable audit records.
  - It would be worse where standards add modelling friction for business users. Palantir's GUI-first, action-centric model is faster for app builders who never need to leave.
- **Options:**
  - (a) *Quick:* publish EOIP's ontology export to OWL, SHACL and JSON-LD, with a loss report.
  - (b) *Pragmatic:* round-trip tests between ontology-as-code, SHACL and each backend's schema, running the W3C test suites first (U-07).
  - (c) *Long-term:* a Foundry import bridge that reads a Foundry Ontology through public APIs into EOIP's ontology-as-code, so a customer can migrate with its model.
- **Selected:** (a) and (b) now; (c) as an EXPERIMENT. The pattern is a canonical ontology IR with emitters for OWL, SHACL, LinkML, Cypher constraints and the HugeGraph schema.
- **Falsifiable POC:**
  - Steps: export a 60-type ontology to OWL and SHACL, re-import it, and diff.
  - Success: zero semantic loss for the supported fragment and an explicit loss list for anything else. pySHACL agrees with the in-house validator on the W3C SHACL Core tests that the fragment covers.
- **Security and privacy:** exports must respect labels, because ontology metadata can itself be sensitive.
- **Defensibility:** high. It aligns with the GitOps-ontology moat (project memory: `gitops.py` is the moat). Copying it would mean Palantir giving up its own lock-in.
- **Decision:** **ADOPT** (a) and (b); **EXPERIMENT** (c).

#### INV-palantir-foundry-03: opaque contract pricing and compute-second metering vs predictable, offline-licensed pricing

- **Limitation:** there is no public price list. Compute-second metering is documented, and enterprise customers are told to consult their representative [CLAIM-palantir-foundry-16].
- **Root cause:** licensing and commercial model. The opacity is *proven*. The impact on TCO is a *hypothesis* (third-party reports only).
- **Alternative:** offline signed licence files per node or tenant with published tiers (BL-22), and metering the customer can see (`licensing/meter.py`). It would be worse for very large buyers who prefer enterprise agreements that bundle services.
- **Options:** (a) publish tiered price bands; (b) a usage dashboard visible to the customer; (c) white-label OEM pricing for partners.
- **Selected:** (a) and (b).
- **POC:** a pricing calculator that matches metered usage within ±5% over a 30-day pilot.
- **Defensibility:** low on its own, because it is easy to copy. It does reinforce the white-label channel.
- **Decision:** **ADOPT** (commercial, not engineering).

#### INV-palantir-foundry-04: bounded set expansion with no cross-Ontology links vs backend-pushed multi-hop queries over a graph of graphs

- **Limitation:** Search Around defaults to 100,000 objects, links cannot span Ontologies, and there is no public path-query language [CLAIM-palantir-foundry-04] [CLAIM-palantir-foundry-17].
- **Root cause:** data model and algorithm. Set expansion over an index is a deliberate trade-off for predictable latency. The caps are *proven*; the reasoning behind them is a *hypothesis*.
- **Alternative:**
  - Typed, bounded QueryPlans (BL-08) push variable-length path queries down to each backend's native engine (Gremlin `repeat`, Cypher `*1..k`) where available.
  - Meta-graph links connect ontologies within a tenant (`graph/meta.py`).
  - This would be worse in two ways: pushdown makes latency less predictable and multiplies backend-specific test cost, and bounded caps are also a security feature.
- **Options:** (a) keep Python traversal with caps; (b) per-backend pushdown for k-hop impact queries under an identical result contract; (c) a portable path IR compiled per backend (CAP-20).
- **Selected:** (b), as an **EXPERIMENT**.
- **POC:** a 6-hop J1/J9 impact query over 20M edges, comparing pushdown with Python traversal on HugeGraph and Neo4j. Success: identical result sets, p95 at least 5× better with pushdown, and caps still enforced.
- **Defensibility:** medium. It depends on the multi-backend design, which Palantir does not need.
- **Decision:** **EXPERIMENT**.

#### INV-palantir-foundry-05: facts as mutable object properties vs evidence-backed claims with epistemic separation

- **Limitation:** user edits overwrite object property values. This is documented: actions change properties, and edits are kept in a writeback dataset [CLAIM-palantir-foundry-18]. The sources read document no first-class model for claims, evidence or confidence, and no contradiction handling (absence of evidence; *hypothesis*, confidence 0.4).
- **Root cause:** data model, where a property holds only the current value. Provenance relies on lineage and action logs.
- **Alternative:**
  - EOIP claims carry evidence spans, confidence, author or agent, and validity time.
  - Contradictions are preserved (BL-39), and AI outputs stay PROPOSED until promoted (BL-40). J2 and J8 depend on this.
  - It would be worse for simple operational CRUD apps that do not want claim-level overhead. EOIP needs a "current value" projection that is as simple as Foundry's.
- **Options:** (a) a claim layer over the current graph; (b) store-wide prediction and assertion planes on every backend; (c) calibrated truth maintenance with as-of queries.
- **Selected:** (b).
- **POC:** run J2 and J8 on HugeGraph and Neo4j. Success: conflicting owners are preserved, as-of answers are correct, and no predicted fact appears in fact-only queries.
- **Defensibility:** high. It is hard to retrofit onto a property-overwrite model that customers have built apps on for years.
- **Decision:** **ADOPT**.

#### INV-palantir-foundry-06: external MCP clients can export Ontology data to non-Palantir LLMs vs egress-gated MCP

- **Limitation:** Palantir documents that enabling Ontology MCP locally with LLMs hosted outside AIP "makes data in your Palantir environment available to an external MCP client". It recommends a governance review and scopes [CLAIM-palantir-foundry-15].
- **Root cause:** governance (*proven*). MCP has no standard way for a server to learn where the client's model runs.
- **Alternative:**
  - EOIP's MCP server routes responses through the egress gateway (BL-45), with sharing level S0 by default, tokenisation, a per-call manifest, and a client attestation of where its model runs.
  - It would be worse wherever that attestation is trusted too far. It is self-reported and can be forged, so it reduces risk but does not remove it.
- **Selected:** pragmatic native enhancement, with an MCP response policy per sharing level.
- **POC:** an external client under an S0 policy receives only IDs and counts, never PII strings. A DLP scan of the transcripts verifies this.
- **Decision:** **ADOPT**.

## 13. Per-capability decisions

| CAP-ID | Capability | Decision for EOIP | Rationale |
|---|---|---|---|
| CAP-08 | Schema and typing with interfaces and shared properties | BUILD (extend the manifest) | STR-08 |
| CAP-41 | Governed ontology change (branches, proposals, migration of edits) | BUILD | STR-07; extends BL-32 |
| CAP-37 | Ontology evolution with migration of human assertions | BUILD | STR-07 |
| CAP-45 / CAP-46 | Mandatory labels propagated along lineage; ACL enforcement in retrieval | BUILD (P0) | STR-02, STR-03; BL-18 |
| CAP-47 | Tenant isolation as a mandatory silo, like Organizations | BUILD (P0) | BL-20 |
| CAP-59 | MCP with scoped, governed actions | BUILD | STR-05 |
| CAP-51 | Egress gating for MCP and LLM traffic | BUILD (extend BL-45) | INV-06 |
| CAP-50 | Air-gapped install, upgrade and rollback | BUILD | STR-06, INV-01 |
| CAP-17 | Generated typed client SDKs (with the GraphQL/API surface) | BUILD | STR-04 |
| CAP-43 | Store-wide epistemic separation | BUILD | INV-05 |
| CAP-19 / CAP-20 | Multi-hop queries pushed down to the backend | EXPERIMENT | INV-04 |
| CAP-09 / CAP-10 | Open ontology export (OWL, SHACL, JSON-LD) | BUILD (bridge at the boundary, per the ontology strategy) | INV-02 |
| CAP-26 | Foundry source connector (public APIs) | DEFER (build on demand) | An integration, not a parity item |
| CAP-61 | Local model serving | REUSE (Ollama, vLLM) | Parity is already in the design |
| CAP-22 / CAP-23 | Reasoning | REJECT as a driver of Palantir parity | Palantir does not compete here |
| CAP-77 | Transparent pricing and licensing | ADOPT (commercial) | INV-03 |

## 14. Concrete tests, proof-of-concept, and acceptance conditions

All tests are **PROPOSED**. None has been run.

| Test | Setup | Pass condition | Journeys |
|---|---|---|---|
| T-PAL-01 Action-type parity | Define `ReassignOwner` with parameters, a precondition shape, a permission and a notification side effect | Invalid inputs are rejected with reasons. A valid action produces exactly one atomic mutation, one audit record and one webhook. An agent call produces PROPOSED | J2, J4 |
| T-PAL-02 Label propagation | Source A labelled `HR`, source B unlabelled; a derived entity, a summary and an embedding | Users without `HR` never see values, chunks, citations or counts derived from A. Revocation purges caches within 60 s | J5, J13 |
| T-PAL-03 Property-level projection | One entity with properties from three sources of different sensitivity | Property sets are correct for each role on all three backends | J5, J14 |
| T-PAL-04 SDK generation | Generate TypeScript and Python clients from the ontology manifest | They compile. A typed query and action round trip works. A breaking ontology change triggers a major version bump | — |
| T-PAL-05 Air-gap lifecycle | Offline host and signed bundle | Install, upgrade and rollback succeed with zero egress. A signature failure blocks install | J16 |
| T-PAL-06 Ontology export round trip | A 60-type ontology | The diff after exporting to OWL/SHACL/JSON-LD and re-importing is empty for the supported fragment; otherwise a loss report is produced | J4, J14 |
| T-PAL-07 MCP scope | An external client scoped to read `Incident` and propose `AssignIncident` | Other tools are denied. S0 egress returns no PII. Proposals require approval | J5, J6 |
| T-PAL-08 Multi-hop pushdown | A digital thread with 20M edges | Pushdown returns the same results as Python traversal. The p95 improvement is measured. Caps are enforced | J1, J9 |

## 15. Risks, trade-offs, and open research questions

- **Risk: buyers compare EOIP to Palantir's integrated breadth** (pipelines, apps, AIP). Mitigation: position EOIP as the evidence-grade, white-label knowledge graph that *integrates* with lakehouses and ETL, not as a Foundry replacement.
- **Risk: the accreditation gap** (FedRAMP, IL) in defence and public-sector deals. There is no near-term mitigation beyond supply-chain evidence (SBOM, signing) and accreditation run by the customer.
- **Trade-off:** an action-type model adds a second write path alongside ingestion. Both must converge on the same validation gate and revision model, or truth maintenance breaks.
- **IP flag (recorded only, no legal conclusion):** Palantir holds a large patent portfolio. No patent search was performed in this run (NOT PUBLICLY VERIFIED). Counsel should check the ontology-action-writeback, marking-propagation and air-gapped delivery patterns before EOIP files or ships closely similar inventions.
- **Open questions:**
  1. Is there a documented standards export of the Ontology model?
  2. What consistency guarantee does a reader get immediately after an action?
  3. What is the current status of Ontology as Code?
  4. What is the minimum supported on-prem footprint?
  5. What is the osdk-ts licence?
  6. Do markings propagate into AIP embeddings and agent memories? The sources read do not say.

---

## Appendix A — Research-dimension coverage

| Dimension | Covered in section(s) | Summary or N/A reason |
|---|---|---|
| D1 Identity and maturity | 1 | Palantir; continuously delivered with no public versions; OSv1 retired 2026-06-30; proprietary |
| D2 Problem and workloads | 2 | Operational decision-making on an ontology for defence, government and industry |
| D3 Architecture decomposition | 4, 5 | Apollo/Rubix control plane; datasets → Funnel → object databases; OSS; Actions; AIP |
| D4 Storage primitives and indexing | 5.2 | OSv2 separates indexing and querying; physical engine NOT PUBLICLY VERIFIED (H4) |
| D5 Schema and semantic expressivity | 5.1 | Object, link and action types, interfaces, shared properties; no OWL or SHACL; edge properties not documented |
| D6 Query pipeline and optimisation | 5.3 | Object sets, Search Around (100k cap), Spark execution at scale; no graph query language |
| D7 Reasoning and inference | 5.4 | None documented; pipelines, functions and AIP Logic instead |
| D8 Transactions, concurrency, scale | 5.5, 5.6, 7 | Actions are transactions (up to 10k objects); isolation undocumented; horizontal scale |
| D9 Ingestion and federation | 3, 4 | Connectors, CDC, streams, listeners; virtual tables over lakehouses |
| D10 Identity and evidence | 5.1, 11, INV-05 | Primary-key identity (H1); no documented claim or evidence model; provenance via lineage |
| D11 Time and evolution | 5.8 | Dataset transactions, Global Branching, edit migration; no documented bitemporal object queries |
| D12 Graph algorithms and ML | 3, 5.4 | Not centred on graph algorithms; ML via Foundry model tooling and AIP (not researched in depth) |
| D13 Retrieval and agent integration | 3, 12 (STR-05, INV-06) | AIP agents, Ontology MCP, Palantir MCP (beta) |
| D14 Natural-language querying | 3 | AIP Assist and Chatbot Studio over objects; text-to-query accuracy NOT PUBLICLY VERIFIED |
| D15 Governance and authoring | 5.8, 9 | GUI-first authoring, branches and proposals, Marketplace releases; ontology-as-code in beta |
| D16 Human experience | 3 | Workshop, Slate, Object Views |
| D17 Developer experience | 3, STR-04 | OSDK (3 languages plus OpenAPI), Code Repositories, VS Code integration |
| D18 Trust and security | 5.9 | Organizations, markings, roles, row/column policies, CBAC; Rubix hardening; accreditations |
| D19 Multi-tenancy and white-label | 10, 11 | Organizations as silos; no public white-label or OEM offering |
| D20 Empirical economics | 7 | No benchmarks; documented limits; compute-second metering |
| D21 Commercial and licensing | 1, 9, INV-03 | Proprietary; contract pricing |
| D22 Interoperability and lock-in | 9, INV-02 | Data is open (Iceberg, Parquet, JDBC); model and actions are proprietary |
| D23 IP and prior art | 15 | Patent portfolio not searched; legal-review flag recorded |
| D24 Research quality | 1, Appendix C | Official docs as the primary source; no product trial; internals marked as hypotheses |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline (BL-ID + status) | Decision for EOIP | Priority |
|---|---|---|---|---|---|
| CAP-01 | native (proprietary object store) | CLAIM-palantir-foundry-02, -03 | BL-01..05 Implemented (adapters) | REUSE backends (no change) | P3 |
| CAP-08 | native | CLAIM-palantir-foundry-01 | BL-28 Implemented (gate); manifest fixed | BUILD interfaces and shared properties | P1 |
| CAP-09 | absent | CLAIM-palantir-foundry-13 | BL-30 Partial | BUILD bridge (export) | P2 |
| CAP-10 | absent | CLAIM-palantir-foundry-13 | BL-29 Partial | REUSE pySHACL in CI | P2 |
| CAP-11 | partial (no documented edge properties) | CLAIM-palantir-foundry-17 | LPG edge properties via backends | REUSE (backend-native) | P3 |
| CAP-17 | native (OSDK + OpenAPI; not GraphQL) | CLAIM-palantir-foundry-06 | BL-58 Absent | BUILD generated SDKs | P2 |
| CAP-19 | partial (bounded Search Around) | CLAIM-palantir-foundry-04 | BL-08 Implemented (bounded) | EXPERIMENT pushdown | P2 |
| CAP-21 | native (virtual tables) | CLAIM-palantir-foundry-21 | BL-51 Partial | DEFER | P3 |
| CAP-26 | native | CLAIM-palantir-foundry-22 | BL-23 Implemented | INTEGRATE (Foundry connector, on demand) | P3 |
| CAP-35 | native (Global Branching) | CLAIM-palantir-foundry-21 | BL-32 Partial; BL-38 Implemented | BUILD | P1 |
| CAP-36 | native (dataset transactions, edit log) | CLAIM-palantir-foundry-21, -18 | BL-37 Implemented | REUSE own | P2 |
| CAP-37 | native (edit migration) | CLAIM-palantir-foundry-05 | BL-32 Partial | BUILD | P1 |
| CAP-38 | partial (lineage) | CLAIM-palantir-foundry-14, -21 | BL-41 Implemented | REUSE own | P2 |
| CAP-43 | unknown / absent | — (absence of evidence) | BL-40 Implemented (contract) / Partial | BUILD store-wide | P1 |
| CAP-45 | native | CLAIM-palantir-foundry-13 | BL-19 Implemented | REUSE own | P2 |
| CAP-46 | native (markings, row/column policies) | CLAIM-palantir-foundry-14, -05 | BL-17 Implemented; **BL-18 Absent** | BUILD | **P0** |
| CAP-47 | native (Organizations) | CLAIM-palantir-foundry-13 | BL-20 Partial | BUILD | **P0** |
| CAP-48 | native (audit, action log) | CLAIM-palantir-foundry-13, -18 | Partial (audit modules) | BUILD action audit | P1 |
| CAP-50 | native (accredited) | CLAIM-palantir-foundry-08, -09 | Design goal; no live air-gap test run | BUILD | P1 |
| CAP-51 | partial (BYOM and self-hosting; MCP warning) | CLAIM-palantir-foundry-12, -15 | BL-45 Implemented | BUILD MCP egress policy | P1 |
| CAP-52 | absent (no public OEM) | — | BL-21 Implemented | REUSE own (differentiator) | P2 |
| CAP-59 | native (Ontology MCP; Palantir MCP in beta) | CLAIM-palantir-foundry-15 | BL-47 Implemented (read-only) | BUILD governed action tools | P1 |
| CAP-61 | native (self-hosting in compute modules) | CLAIM-palantir-foundry-12 | Ollama in Compose | REUSE | P2 |
| CAP-76 | native (blue/green, multi-node) | CLAIM-palantir-foundry-08 | HA Compose files, live-unverified | DEFER beyond one node | P3 |
| CAP-77 | contract only | CLAIM-palantir-foundry-16 | BL-22 Implemented | ADOPT transparent tiers | P2 |
| CAP-79 | native (Apollo integrity checks) | CLAIM-palantir-foundry-09 | Not verified | BUILD signed bundles | P1 |

## Appendix C — Evidence records

| CLAIM-ID | Product / version / date | Exact claim | Classification | Source title + URL | Publication / access date | Confidence + rationale | Contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-palantir-foundry-01 | Foundry Ontology, docs 2026 | Ontology concepts: object type, property, shared property, link type, action type ("the schema definition of a set of changes or edits to objects, property values, and links"), functions, interfaces ("an Ontology type that describes the shape of an object type and its capabilities"), object sets, roles, object views | Officially documented | Palantir docs, Ontology core concepts: https://www.palantir.com/docs/foundry/ontology/core-concepts/ | undated / 2026-10-18 | 0.9: current official docs | none |
| CLAIM-palantir-foundry-02 | Ontology backend, 2026 | Backend components: Ontology Metadata Service, object databases, Object Set Service, Actions service, Object Data Funnel ("responsible for orchestrating data writes into the Ontology"), Functions on Objects | Officially documented | Palantir docs, Ontology backend overview: https://www.palantir.com/docs/foundry/object-backend/overview/ | undated / 2026-10-18 | 0.9 | none |
| CLAIM-palantir-foundry-03 | Object Storage v1/v2, 2026 | OSv1 (Phonograph) "will be unavailable after June 30, 2026". OSv2 separates indexing and querying subsystems so it can "scale horizontally more easily" | Officially documented | same as -02 | undated / 2026-10-18 | 0.9 | none |
| CLAIM-palantir-foundry-04 | OSv2, 2026 | Up to 10,000 objects per action; at most 2,000 properties per object type; Search Around default 100,000; temporary object sets expire within 24h; vendor claim of "tens of billions of objects for a single object type"; Spark-based execution for high-scale Search Around | Officially documented (limits) / Unverified (throughput claim) | same as -02 | undated / 2026-10-18 | 0.85 for limits; 0.3 for throughput (vendor claim, no workload stated) | none |
| CLAIM-palantir-foundry-05 | OSv2, 2026 | Streaming datasources; multi-datasource object types with column/property-level permissions; migration of user edits after a breaking schema change; "faster observation of user edits" | Officially documented | same as -02 | undated / 2026-10-18 | 0.85 | none |
| CLAIM-palantir-foundry-06 | OSDK, 2026 | OSDK for TypeScript (npm), Python (pip/Conda) and Java (Maven), with OpenAPI for other languages; generated for the relevant Ontology subset; token scoped to selected ontological entities and intersected with user permissions; WebSocket subscriptions; row and column controls do not cover how an application handles responses, so pair them with markings or CBAC; Ontology can be defined as code in a SuperRepo | Officially documented | Palantir docs, Ontology SDK overview: https://www.palantir.com/docs/foundry/ontology-sdk/overview/ | undated / 2026-10-18 | 0.85 | none |
| CLAIM-palantir-foundry-07 | palantir/osdk-ts, main | Public repo "Typescript related OSDK libraries" (@osdk/client, @osdk/api, @osdk/foundry-sdk-generator, @osdk/oauth). Licence not shown on the captured page; no release captured | Observed in source repository page | GitHub, palantir/osdk-ts: https://github.com/palantir/osdk-ts | n/a / 2026-10-18 | 0.5; licence = UNVERIFIED (incomplete page capture) | none |
| CLAIM-palantir-foundry-08 | Rubix / Apollo, 2026 | AIP, Foundry and Apollo run on Rubix (hardened Kubernetes) and can be deployed "across AWS, Azure, Google Cloud, Oracle Cloud, or on-premises environments"; accreditations FedRAMP High, DoD DISA IL-5/IL-6, CMMC; "nodes in Rubix environments cannot live longer than 48 hours"; Apollo plans install, upgrade and rollback and requires multi-node blue/green for every service | Officially documented | Palantir Architecture Center, The Rubix substrate: https://palantir.com/docs/foundry/architecture-center/rubix/ | undated (© 2026) / 2026-10-18 | 0.85 | none |
| CLAIM-palantir-foundry-09 | Apollo | Apollo delivers software into air-gapped classified and unclassified networks. Bundles are transferred manually or through the Bundle Transfer System, and payloads are scanned and integrity-verified at multiple checkpoints | Officially documented (read via search snippet; page returned 403) | Palantir Blog, Deploying Across Security Domains: https://blog.palantir.com/deploying-across-security-domains-449c786d92c0 | date not captured / 2026-10-18 | 0.6: official source, but the full text was not read | none |
| CLAIM-palantir-foundry-10 | Palantir + NVIDIA, 2026-03-12 | Sovereign AI OS reference architecture: AIP, Foundry, Apollo, Rubix and AIP Hub qualified on NVIDIA enterprise reference architectures (Blackwell Ultra); on-premises, edge and sovereign cloud | Officially documented (press release) | Business Wire, Palantir and NVIDIA Team to Deliver Sovereign AI Operating System Reference Architecture: https://www.businesswire.com/news/home/20260312795208/en/Palantir-and-NVIDIA-Team-to-Deliver-Sovereign-AI-Operating-System-Reference-Architecture | 2026-03-12 / 2026-10-18 | 0.75: press release describing an announced configuration | Constellation Research frames it as an on-prem bet (consistent) |
| CLAIM-palantir-foundry-11 | AIP, 2026 | AIP builder tools: AIP Logic, AIP Chatbot Studio ("formerly known as AIP Agent Studio"), AIP Evals; also AIP Assist, Threads, Automate, BYOM and self-hosted models | Officially documented | Palantir docs, AIP overview: https://www.palantir.com/docs/foundry/aip/overview/ | undated / 2026-10-18 | 0.85 | none |
| CLAIM-palantir-foundry-12 | AIP self-hosted models, 2026 | Self-hosted LLMs are backed by compute modules (vLLM or Ollama given as examples); this keeps "all inference traffic within your own network boundary"; "on-premise or air-gapped deployments" listed as a use case; "run models without any external connectivity" | Officially documented | Palantir docs, Self-host models with AIP: https://www.palantir.com/docs/foundry/aip/self-host-models/ | undated / 2026-10-18 | 0.85 | none |
| CLAIM-palantir-foundry-13 | Foundry platform summary, 2026 | "The Ontology is not a semantic layer"; data layer plus object layer; Projects are the primary security boundary; Organizations are "Mandatory controls for user silos"; roles Owner, Editor, Viewer, Discoverer; markings; LLM proxy endpoints for Anthropic and OpenAI; BYOM; Workshop, Slate, Developer Console | Officially documented | Palantir docs, Foundry platform summary for LLMs: https://www.palantir.com/docs/foundry/getting-started/foundry-platform-summary-llm/ | undated / 2026-10-18 | 0.85 | none |
| CLAIM-palantir-foundry-14 | Markings, 2026 | "Markings are a mandatory control, while roles are a discretionary control"; markings are conjunctive; they are inherited through the file hierarchy and data dependencies unless explicitly removed; removing one requires the Expand Access permission | Officially documented | Palantir docs, Markings: https://www.palantir.com/docs/foundry/security/markings/ | undated / 2026-10-18 | 0.9 | none |
| CLAIM-palantir-foundry-15 | Ontology MCP / Palantir MCP, 2026 | Ontology MCP exposes a Developer Console application's object types, action types and query functions as MCP tools, bounded by application scopes. Palantir MCP [Beta] provides 70+ tools to build and modify ontology types but cannot write ontology data. Warning: using external LLM clients makes Palantir data available outside AIP | Officially documented | Palantir docs, Ontology MCP overview: https://palantir.com/docs/foundry/ontology-mcp/overview/ ; Palantir MCP: https://www.palantir.com/docs/foundry/palantir-mcp/ | undated / 2026-10-18 | 0.8 (read via search-result extracts of official pages) | none |
| CLAIM-palantir-foundry-16 | Pricing, 2026 | Code workspace usage is tracked in Foundry compute-seconds with default rates (e.g., no-GPU JupyterLab 0.1, T4 1.2, V100 3.0); enterprise-contract customers are told to contact their representative; the AWS Marketplace FedRAMP listing is "Private Offer Only"; no public list price found | Officially documented (metering) / Third-party report (no list price) | Palantir docs, Compute usage with Code Workspaces: https://palantir.com/docs/foundry/code-workspaces/compute-usage/ ; AWS Marketplace listing: https://aws.amazon.com/marketplace/pp/prodview-mxjuquuockgku | undated / 2026-10-18 | 0.75 for metering; 0.5 for the absence of a list price | none |
| CLAIM-palantir-foundry-17 | Link types, 2026 | A link type is the schema of a relationship between two object types; its two sides are traversed independently; self-links are allowed; links cannot span Ontologies; M:N link types are backed by datasources; a link type is analogous to a join | Officially documented | Palantir docs, Link types overview: https://www.palantir.com/docs/foundry/object-link-types/link-types-overview/ | undated / 2026-10-18 | 0.85 | none |
| CLAIM-palantir-foundry-18 | Action types, 2026 | An action is "a single transaction that changes the properties of one or more objects"; action types have rules, parameters, submission criteria and side effects (notifications, webhooks); edits are captured in the object type's writeback dataset; there is an action log | Officially documented | Palantir docs, Action types overview: https://www.palantir.com/docs/foundry/action-types/overview/ | undated / 2026-10-18 | 0.85 | none |
| CLAIM-palantir-foundry-19 | DevOps / Marketplace, 2026 | Products bundle Foundry resources, including an Ontology or an ontology fragment; they are shared through the Foundry Marketplace and tagged with release channels | Officially documented | Palantir docs, Product delivery: https://palantir.com/docs/foundry/devops/overview/ | undated / 2026-10-18 | 0.75 (read via search extract) | none |
| CLAIM-palantir-foundry-20 | Ontology as Code (Beta) | A community thread describes an "Ontology as Code" repo built with the osdk-ts maker package; another user asks whether it was removed; an older thread says the GUI was the only supported option | Third-party report (vendor community forum) | Palantir Community, Ontology as Code (Beta): https://community.palantir.com/t/ontology-as-code-beta/5257 ; Programmatic Ontology Management thread: https://community.palantir.com/t/programmatic-ontology-management-in-palantir-foundry-alternatives-to-gui-based-approach/979 | n/a / 2026-10-18 | 0.4: forum source; status unclear | The OSDK page mentions an Ontology defined as code in a "SuperRepo" (CLAIM-06), which suggests some as-code path exists |
| CLAIM-palantir-foundry-21 | Foundry platform summary, 2026 | Datasets are versioned through transactions with full history; Global Branching spans applications, with proposals; data is stored in Iceberg/Parquet with REST, JDBC and S3-compatible access; virtual tables over Databricks, Snowflake and BigQuery | Officially documented | same as -13 | undated / 2026-10-18 | 0.85 | none |
| CLAIM-palantir-foundry-22 | Foundry data integration, 2026 | Connectors sync into datasets, streams, CDC streams and media sets; Pipeline Builder; Code Repositories (Python, Java, SQL); batch, incremental and streaming (Flink) processing; listeners (HTTPS, WebSocket, email) | Officially documented | same as -13 | undated / 2026-10-18 | 0.85 | none |
| CLAIM-palantir-foundry-23 | Constellation Research, 2026 | The Palantir/NVIDIA design runs Foundry services on hardened Kubernetes managed by Rubix and Apollo; framed as a bet on on-prem enterprise AI | Third-party report | Constellation Research, Palantir and Nvidia build sovereign, on-premises AI reference architecture: https://www.constellationr.com/insights/news/palantir-and-nvidia-build-sovereign-premises-ai-reference-architecture | 2026-03 / 2026-10-18 | 0.55 | none |

## Appendix D — Assumptions

1. Palantir publishes no version numbers. "Versions examined" means the public documentation as of 2026-10-18.
2. Ontology MCP is treated as generally available because its pages do not carry the beta label that Palantir MCP carries. This was not confirmed explicitly.
3. Object identity by primary key (H1) and FK-backed 1:N links (H2) are assumed from the row and join analogies in the documentation.
4. The Apollo air-gapped claims come from an official blog post read only through a search snippet (403 on fetch). They are consistent with the accreditation list on the Rubix page.
5. Third-party pricing estimates were seen but not used as evidence.
6. No Palantir product trial was performed (methodology §8). All internals are either documented or marked as hypotheses.
7. Gotham is out of scope. Only Foundry, AIP, Apollo and Rubix are assessed.
