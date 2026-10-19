# C04 — Senzing (embeddable real-time entity resolution SDK)

| Field | Value |
|---|---|
| Registry ID | T-C04-senzing |
| Tier | A — leading embeddable, real-time, principle-based ER engine; benchmark for what EOIP's identity layer must match (BL-34/35/36) |
| Versions examined | Senzing SDK **4.4.2** (2026-10-01, latest; 4.4.x line first released 2026-08-31, EOL 2028-08-31). Also 4.3.5 (2026-09-09), 4.2.4 (2026-04-09), 4.0.0 (2025-08-27). EULA "Last updated: May 2026.v1". Whitepaper "Principle-based entity resolution explained" (PBTO062226, © 2026; document type dated 2019). |
| Verified on | 2026-10-18 |
| Worker | W12 |

## 1. Identity, current status, tier, and sources

**Identity.** Senzing, Inc. sells the Senzing SDK, a proprietary entity-resolution library (C core with Python, Java and other bindings plus native CLI tools). It resolves people, organisations and other entity types in real time as records are added [CLAIM-senzing-08][CLAIM-senzing-09]. The SDK abstract base classes are published under Apache-2.0 at `github.com/senzing-garage` (for example `sz-sdk-python`, marked "work-in-progress"). The resolution engine itself is proprietary [CLAIM-senzing-13]. There are no name collisions.

**Status.** Active, with frequent releases:
- **4.4.x:** 4.4.0 (2026-08-31), 4.4.1 (2026-09-17) and 4.4.2 (2026-10-01).
- **4.3.x:** 4.3.0 to 4.3.5 (2026-05-19 to 2026-09-09).
- **4.2.x:** 4.2.0 to 4.2.4 (2026-01-28 to 2026-04-09).
- **Older lines:** 4.1.0 (2025-10-13) and 4.0.0 (2025-08-27).

Each minor line is supported for two years [CLAIM-senzing-01].

**Licence.** Proprietary EULA "May 2026.v1" [CLAIM-senzing-05]:
- non-exclusive, non-transferable, with no right to sublicense;
- a Production License covers one production instance;
- **no right to distribute**;
- installation only on hardware the licensee owns or controls;
- no third-party access;
- no reverse engineering;
- no publishing of performance information or comparisons without consent;
- quarterly-limited audits;
- Delaware law.

Pricing is per Data Source Record (DSR, "a single record that is mapped and loaded"). The pricing page shows $58,560/year for 10M DSRs with up-front payment and the standard EULA. Custom terms carry custom prices, and a partner programme is "contact us" [CLAIM-senzing-06]. Free use is 500 source records, and larger evaluations are available on request [CLAIM-senzing-07].

**Tier A reason.** Senzing is the reference design for real-time, entity-centric ER with automatic re-evaluation (merge and unmerge) and explainability. It defines the bar for EOIP's planned identity layer.

**Sources (13):** release history; v4 system requirements; EULA; pricing; v4 quickstart; "How ER works" page; principle-based whitepaper (PDF); Python SDK reference (garage docs); v4 flags and breaking-changes pages; innovation page (vendor claims); `sz-sdk-python` repository; HPCwire 2019 article; arXiv 2210.01230 (ER-evaluation caution). All accessed 2026-10-18.

## 2. Primary problem, target workloads, concrete example workflows

**Problem.** Determine "who is who" and "who is related to whom" across many sources continuously, without training data or tuning [CLAIM-senzing-08][CLAIM-senzing-09].

**Workloads.** KYC/AML, fraud, watch-list screening, customer 360, law enforcement and intelligence, supply-chain risk and data-quality hubs. Vendor positioning lists organisations, people, vessels and other types [CLAIM-senzing-08].

**Workflow (reconstructed from the SDK reference):**
1. Map each source record to Senzing JSON features. Each record has a `DATA_SOURCE` code, a `RECORD_ID`, and feature attributes such as `NAME_FIRST`, `ADDRESS_*`, `PHONE_*` and identifiers. `preprocess_record()` validates mappings [CLAIM-senzing-19].
2. Call `add_record(ds, id, json, flags=SZ_WITH_INFO)`. The engine resolves the record immediately and returns the affected entities (new, changed, no longer valid). Re-adding the same DS+ID replaces the record [CLAIM-senzing-10][CLAIM-senzing-11].
3. A downstream consumer reads `AFFECTED_ENTITIES` and pulls `get_entity_by_record_id` or `get_entity_by_entity_id` to update its own store.
4. Redo processing: `get_redo_record` / `process_redo_record` drain deferred re-evaluation work, for example after a value becomes generic [CLAIM-senzing-10].
5. Investigate:
   - `why_entities`, `why_records` and `why_record_in_entity` explain matches and non-matches;
   - `how_entity_by_entity_id` shows how an entity was assembled step by step;
   - `get_virtual_entity_by_record_id` previews a hypothetical entity built from chosen records;
   - `find_path_*` and `find_network_*` explore relationships [CLAIM-senzing-10].
6. Search with `search_by_attributes` (SEARCH or INGEST profile) for screening without loading [CLAIM-senzing-10].
7. Delete with `delete_record`, which is idempotent and re-resolves the affected entities [CLAIM-senzing-10].

**EOIP workflow.** A customer that already owns Senzing (common in financial services and public sector) wants EOIP to use Senzing entity IDs as the identity authority for people and organisations, while EOIP keeps provenance, ACLs and the graph.

## 3. Feature inventory

| Area | Feature | Status | Evidence |
|---|---|---|---|
| Resolution | Real-time, record-to-entity resolution on each add | Present | [CLAIM-senzing-09] |
| Resolution | No training or tuning; ~35 general principles; feature behaviours | Present (vendor) | [CLAIM-senzing-08] |
| Resolution | Generic-value detection and re-evaluation of prior records | Present | [CLAIM-senzing-08][CLAIM-senzing-09] |
| Resolution | Possible matches and possibly-related relationships | Present | [CLAIM-senzing-08] |
| Resolution | Automatic unmerge/re-resolve on new or deleted evidence | Present | [CLAIM-senzing-09][CLAIM-senzing-10] |
| Explainability | why / how / virtual-entity APIs | Present | [CLAIM-senzing-10] |
| Graph | Find path / network over resolved entities | Present | [CLAIM-senzing-10] |
| Search | Attribute search with profiles | Present | [CLAIM-senzing-10] |
| Change feed | `SZ_WITH_INFO` affected-entities list | Present | [CLAIM-senzing-11] |
| Survivorship | Golden-record field selection policy | Unknown (entity shows all features; configurable survivorship NOT PUBLICLY VERIFIED) | — |
| Storage | PostgreSQL ≥14/15, MS SQL ≥2019, Oracle ≥19c, MySQL ≥8.4.7 (<100M records), SQLite 3.38 (<1M records), Aurora PostgreSQL, Azure SQL | Present | [CLAIM-senzing-04] |
| Storage | In-memory `internal://` store for demos (<10k records), with vector search, path finding and export (4.3) | Present | [CLAIM-senzing-03] |
| Plugins | Credit-card standardisation with PCI DSS-compliant masking (4.2) | Present | [CLAIM-senzing-14] |
| Ops | Native CLI binaries for Linux, macOS and Windows; Python 3.10+ for the Python SDK (4.4) | Present | [CLAIM-senzing-02] |
| Ops | Optional DB-native locking for PostgreSQL and MSSQL (4.4) | Present (opt-in) | [CLAIM-senzing-02] |
| Agents | MCP server (vendor-claimed onboarding speed-up) | Present (claim) | [CLAIM-senzing-12] |
| UI | Desktop evaluation tool | Present (evaluation) | [CLAIM-senzing-07] |
| Multi-tenancy | Native tenant model | NOT PUBLICLY VERIFIED (per-database separation assumed) | — |
| Source code | Engine source | Absent (proprietary); SDK abstract classes Apache-2.0 | [CLAIM-senzing-13] |

## 4. Text-based architecture diagram

```
  Caller process (EOIP worker / app) ───────────────────────────────────────────────┐
  │  sz SDK binding (Python ≥3.10, Java, …) ─► native engine library (proprietary)   │
  │      SzAbstractFactory → SzEngine / SzConfig / SzConfigManager / SzProduct       │
  │      ┌───────────────────────── engine pipeline per add/delete ─────────────┐    │
  │      │ record JSON → feature extraction + standardisation + derived features │    │
  │      │   → candidate features (generic values suppressed)                    │    │
  │      │   → candidate entities from repository → comparators score features   │    │
  │      │   → principles: SAME / POSSIBLE MATCH / POSSIBLY RELATED             │    │
  │      │   → entity + relationship update (merge / unmerge), redo queue        │    │
  │      │   → WITH_INFO: AFFECTED_ENTITIES                                      │    │
  │      └───────────────────────────────────────────────────────────────────────┘    │
  └─────────────────────────────────────┬─────────────────────────────────────────────┘
                                        │ SQL (driver per DB; retries; optional DB locks)
               ┌────────────────────────▼────────────────────────┐
               │ Repository DB: PostgreSQL / MSSQL / Oracle /     │
               │ MySQL / SQLite / internal:// (demo)              │
               │  record library (original form), feature library,│
               │  entities, relationships, redo queue, config     │
               └──────────────────────────────────────────────────┘
  Control plane: engine configuration (features, principles, comparators) versioned in the DB.
  Scale-out: many stateless engine processes against one shared repository DB (hypothesis).
```

## 5. Under-the-hood reconstruction

Internals are proprietary. Statements below come from documentation or are marked *hypothesis*.

### 5.1 Data model (documented)
- **Record library:** each inbound record is stored in its original form, keyed by DATA_SOURCE + RECORD_ID [CLAIM-senzing-09].
- **Feature library:** standardised features with elements, variants and derived features [CLAIM-senzing-09].
- **Feature behaviours** [CLAIM-senzing-08]. Each feature type carries three properties:

| Property | Values |
|---|---|
| Frequency | F1 (one entity), FF (few), FM (many), FVM (very many), NAME, NONE |
| Exclusivity | yes / no |
| Stability | yes / no |

  Whitepaper Table 1 examples:

| Feature | Frequency | Exclusive | Stable |
|---|---|---|---|
| SSN | F1 | yes | yes |
| DATE_OF_BIRTH | FM | yes | yes |
| ADDRESS | FF | no | no |
| EMAIL | F1 | no | no |
| GENDER | FVM | yes | no |

- **Entities:** sets of records. Relationships are typed as possible match, possibly related, or disclosed. The `find_path` and `find_network` APIs show that entities and relationships form a persisted graph [CLAIM-senzing-08][CLAIM-senzing-10].

### 5.2 Resolution algorithm (documented outline; detail is hypothesis)
```
add_record(r):
  store r in record library (replace if same DS+ID)
  F = standardise(extract_features(r)) ∪ derived_features(r)
  K = [f for f in F if f.behaviour supports candidacy and not is_generic(f)]   # documented
  C = candidate_entities(K)                       # hypothesis: index on feature-value hashes
  for e in C:
     S = {feature: bucket(compare(f_r, f_e))}     # SAME/CLOSE/LIKELY/PLAUSIBLE/UNLIKELY/NO_CHANCE
     outcome[e] = first principle p in ordered rules whose qualifiers hold on S
                  and (not p.skip_on_conflicting_exclusives or no exclusive conflict)
  resolve: union r with all e where outcome = MATCH (may merge several entities)
  relate : POSSIBLE_MATCH / POSSIBLY_RELATED edges
  if a feature value's entity count crosses its generic threshold:
       mark generic; enqueue redo for entities using it           # documented behaviour
  return AFFECTED_ENTITIES
```
- **Generic suppression.** Values shared by many entities (a bank's toll-free number, or an SSN reused by many people) are dropped from candidate selection, and prior records are re-evaluated [CLAIM-senzing-08][CLAIM-senzing-09]. This is a frequency-based counterpart of Splink's TF adjustment, but applied **online** and **retroactively**.
- **Principles.** About 35 principles, including:
  - MATCH: SAME_F1+CLOSE_NAME, MULT_FF+CLOSE_NAME, MULT_STAB+LIKELY_NAME+SAME_F1;
  - POSSIBLE MATCH: CLOSE_NAME+SAME_F1, CLOSE_NAME+CLOSE_STAB;
  - POSSIBLY RELATED: SAME_F1, CFF_SURNAME.

  A "skip on conflicting exclusives" flag stops father/son merges when DOBs differ [CLAIM-senzing-08].
- **Entity-centric matching.** Records are compared with the accumulated *entity* (all its features), not with single records. This is what makes order-independent behaviour plausible, along with re-evaluation [CLAIM-senzing-09].
- **Order independence.** Requires redo processing to be drained (hypothesis, consistent with the redo API).

### 5.3 Query pipeline
Queries are API calls, not a query language: get entity, why/how, search_by_attributes, find_path/network, export. There is no user-facing SQL or graph query language (NOT PUBLICLY VERIFIED beyond the documented API) [CLAIM-senzing-10].

### 5.4 Concurrency, transactions, partitioning
- The repository is an RDBMS. 4.3.2/4.3.3 hardened transaction-retry handling, with automatic PostgreSQL retries [CLAIM-senzing-15]. 4.4.0 adds opt-in DB-native locking for PostgreSQL and MSSQL [CLAIM-senzing-02].
- 4.3.0 fixed an MSSQL table scan on record update, flagged important [CLAIM-senzing-15].
- 4.2.0 added automatic chunked mode on PostgreSQL 17+ [CLAIM-senzing-14].
- *Hypothesis:* many engine threads or processes resolve concurrently against one database, and the database's locking serialises conflicts on shared entities. Horizontal scale is therefore bounded by the database.

### 5.5 Caching, versioning, security
- **Configuration:** versioned through `SzConfigManager`. 4.0.0 required schema and configuration upgrades; 4.x upgrades need no schema change (4.4.0) [CLAIM-senzing-02].
- **Security:** delegated to the database and host. Cloud DB auth options exist: Aurora PostgreSQL IAM and Azure SQL Entra ID (4.2.0) [CLAIM-senzing-14]. PCI masking plugin [CLAIM-senzing-14].
- **Explanation:** why/how outputs are derived from the stored scoring decisions (documented API semantics) [CLAIM-senzing-10].

## 6. Functional and non-functional requirements inferred from verified behaviour

**Functional:**
- FR-1: resolve on write with an affected-entities change feed [CLAIM-senzing-10][CLAIM-senzing-11].
- FR-2: retroactive re-evaluation when statistics change (generic values) [CLAIM-senzing-08].
- FR-3: three outcomes (match, possible match, possibly related) instead of one threshold [CLAIM-senzing-08].
- FR-4: idempotent delete with re-resolution [CLAIM-senzing-10].
- FR-5: why, how and virtual-entity explanations [CLAIM-senzing-10].
- FR-6: relationship graph navigation [CLAIM-senzing-10].

**Non-functional:**
- NFR-1: RDBMS-backed durability.
- NFR-2: small footprint. Vendor claims ~560 MB library and ~0.5 s cold start [CLAIM-senzing-12].
- NFR-3: two-year support per minor release line [CLAIM-senzing-01].

## 7. Performance and resource model

| Claim | Type | Context | Confidence |
|---|---|---|---|
| Engine ~560 MB, "roughly 7× smaller"; cold start ~0.5 s | Vendor | No hardware stated | 0.3 [CLAIM-senzing-12] |
| "Proven in production to about 100 billion records" | Vendor | No hardware or dataset stated | 0.2 [CLAIM-senzing-12] |
| ~10M records in ~3 h for under $100 (2020, AWS serverless, incremental adds) | Vendor | No hardware specs | 0.25 [CLAIM-senzing-12] |
| Single commodity server up to 400M records (2019) | Third-party report citing a vendor whitepaper | Capacity, not throughput | 0.3 [CLAIM-senzing-17] |
| MySQL limited to <100M records; SQLite to <1M records | Officially documented guidance | — | 0.8 [CLAIM-senzing-04] |
| `internal://` for <10k records | Officially documented | Demo store | 0.8 [CLAIM-senzing-03] |

- **Independent benchmarks:** none found. The EULA forbids publishing performance comparisons without consent [CLAIM-senzing-05], which blocks independent public benchmarking. ER evaluation literature also warns that benchmark F1 often overstates real-world performance [CLAIM-senzing-16].
- **Resource model (hypothesis):** throughput is bound by database IOPS and lock contention on hot entities. RAM is per engine process plus database buffer cache, with no GPU.
- **Failure modes:** documented ones are the MSSQL table-scan issue, SQLite deadlock/connection fixes and non-Latin address scoring fixes [CLAIM-senzing-15]. Unbounded redo backlogs after a large generic-value flip are a hypothesis.

## 8. Strengths and use-case-specific advantages

1. **Real-time, entity-centric resolution with automatic merge and unmerge.** Order-independent results through re-evaluation and redo [CLAIM-senzing-09][CLAIM-senzing-10]. Match it with EOIP's identity ledger plus re-evaluation events.
2. **Zero-training principles from feature behaviours.** Fast time-to-value [CLAIM-senzing-08]. Match it by declaring F1/FF/FM/exclusive/stable behaviours in EOIP's ontology identity profile.
3. **Retroactive generic-value handling** [CLAIM-senzing-08]. Exceed it by keeping generic-value decisions as evidence with timestamps (bitemporal).
4. **Explainability APIs (why, how, virtual entity)** [CLAIM-senzing-10]. Match and integrate them into EOIP evidence manifests.
5. **Three-way outcome (match / possible / related).** Feeds both identity and relationship discovery [CLAIM-senzing-08]. Integrate: "possibly related" becomes a PROPOSED relationship in EOIP's epistemic plane.
6. **Change feed (`WITH_INFO`)** that suits the event-driven graph update needed for J7 [CLAIM-senzing-11].
7. **Mature and supported:** two-year release-line support and RDBMS durability [CLAIM-senzing-01].

## 9. Limitations with root causes

| # | Limitation | Class | Root cause | Category |
|---|---|---|---|---|
| L1 | No right to distribute; no third-party access; one production instance per licence | Licensing restriction (verified) | EULA §1.2–1.3 [CLAIM-senzing-05] | User/developer friction — blocks white-label bundling without an OEM agreement |
| L2 | Publishing benchmarks or comparisons requires consent | Licensing (DeWitt-style) | EULA §2 [CLAIM-senzing-05] | Friction — no independent evidence |
| L3 | Cost per DSR ($58,560/yr for 10M at list) | Commercial | Pricing [CLAIM-senzing-06] | TCO |
| L4 | Proprietary engine; reverse engineering prohibited | Licensing | EULA [CLAIM-senzing-05] | Opaque internals; explanation only through APIs |
| L5 | Principles tuned for people and organisations; other entity types need configuration | Intentional trade-off | Preconfigured behaviours [CLAIM-senzing-08] | Developer friction for IT entities (services, repositories, service accounts) |
| L6 | Database-bound scale; MySQL <100M, SQLite <1M | Verified guidance | RDBMS repository [CLAIM-senzing-04] | Operational overhead |
| L7 | Breaking 3→4 upgrade (schema and config) | Verified | v4 redesign [CLAIM-senzing-02] | Upgrade risk |
| L8 | Inconsistent PostgreSQL minimum (≥14 on the requirements page vs <15 unsupported on the breaking-changes page) | Documentation inconsistency | — [CLAIM-senzing-04] | Minor |
| L9 | Accuracy claims ("outperforms humans") without metric | Vendor claim | — [CLAIM-senzing-12] | Evidence gap |
| L10 | Native multi-tenancy | NOT PUBLICLY VERIFIED | — | Hypothesis: per-tenant DB needed |

## 10. Deployment, licensing, redistribution, and operational viability under EOIP constraints

- **Licence class:** proprietary. **Legal-review trigger: YES.**
  - EULA bars distribution, sublicensing and third-party access.
  - It requires hardware the licensee owns or controls.
  - It restricts publishing benchmarks.
  - It includes audit rights [CLAIM-senzing-05].

  EOIP therefore **cannot bundle Senzing** in its white-label distribution under the standard EULA. Options are a customer-held licence (customer installs Senzing on its own hardware, and EOIP integrates) or a negotiated OEM/partner agreement ("custom terms, custom price"; partner programme) [CLAIM-senzing-06]. We give no legal conclusion; this is recorded for legal review.
- **Air-gap:** plausible. On-prem library plus a local RDBMS, with licence-file activation (hypothesis; offline licence mechanics NOT PUBLICLY VERIFIED). The MCP server and vendor-hosted tools are optional.
- **One node:** viable with PostgreSQL on the same node. SQLite is limited to <1M records [CLAIM-senzing-04].
- **Backend neutrality:** Senzing keeps its own repository DB and entity graph. EOIP would treat Senzing entity IDs as an external identity authority and mirror decisions into HugeGraph, Neo4j or Neptune through the governed mutation path. That costs a second store of identity state.
- **Tenancy:** one Senzing repository per tenant (assumed). Licensing per instance makes per-tenant repositories costly (L1, L3).
- **Data egress:** all on-prem; no client data leaves the host by default (hypothesis — telemetry NOT PUBLICLY VERIFIED).

## 11. Competitive delta against the EOIP verified baseline

| BL | EOIP | Senzing | Delta |
|---|---|---|---|
| BL-34 deterministic identity | Person only, email key | Principle-based multi-feature resolution, any entity type [CLAIM-senzing-08] | Large deficit |
| BL-35 review queue | Partial; candidates never auto-merge | Possible-match/possibly-related outcomes; no review UI in the SDK (UNVERIFIED) | EOIP has review governance; Senzing has outcome semantics |
| BL-36 probabilistic ER | Absent | Real-time ER with re-evaluation [CLAIM-senzing-09] | Largest deficit |
| BL-37/38 revisions, diff | Implemented | `how_entity` history of entity construction [CLAIM-senzing-10]; bitemporal identity NOT PUBLICLY VERIFIED | EOIP can exceed with as-of identity queries |
| BL-39/40 claims, epistemic separation | Implemented (contract) | Not a concept in Senzing | EOIP ahead |
| BL-18 ACL enforcement | Absent | Not a Senzing concern | Both lack it; EOIP must solve it (P0) |
| BL-52 mutation streaming | Implemented in-process | `WITH_INFO` change feed [CLAIM-senzing-11] | Pattern to adopt |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

### Strength-adoption cards

| STR-ID | Competitor | Strength | Evidence | Value to EOIP customers | Decision | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-senzing-01 | Senzing | Entity-centric real-time resolution with automatic merge/unmerge | CLAIM-senzing-09, -10 | Identities stay correct as data arrives (J7) | match | EOIP identity ledger (see INV-splink-01) with per-component re-evaluation on each event; record-to-entity comparison using aggregated entity features | Order-independence test: the same 100k records in 5 random orders give identical final partitions after redo drain |
| STR-senzing-02 | Senzing | Feature-behaviour principles (F1/FF/FM/FVM/NAME × exclusive × stable) | CLAIM-senzing-08 | Zero-training start for new entity types (service accounts, repos, vendors) | match | Ontology identity profile declares feature behaviours per class; deterministic principle engine runs before the Splink scorer | New entity type onboarded by declaration only; precision ≥ 0.98 on the deterministic tier |
| STR-senzing-03 | Senzing | Retroactive generic-value detection | CLAIM-senzing-08 | Shared helpdesk phone or shared mailbox does not glue people together | exceed | Per-tenant frequency counters per feature value; threshold crossing emits a GenericValue event → re-evaluate affected components; event kept with valid time | Inject a value shared by 500 entities; all merges relying on it are proposed for unmerge within one redo cycle |
| STR-senzing-04 | Senzing | why / how / virtual-entity explanations | CLAIM-senzing-10 | Analysts trust and correct identity decisions | match | `/identity/why?a=&b=`, `/identity/how?entity=`, `/identity/what-if` (records subset) APIs over ledger and evidence | Every merge decision answerable by why/how with source spans; what-if returns without mutating |
| STR-senzing-05 | Senzing | Change feed of affected entities | CLAIM-senzing-11 | Downstream graph and indexes refresh precisely (J1 "unchanged relationships not broken") | match | Identity ledger emits `IdentityChanged{old_ids,new_ids,members}` into the BL-52 stream; the graph mutation gateway rewires edges | Replay test: edge count unchanged for entities not in the affected set |
| STR-senzing-06 | Senzing | Three-way outcome incl. "possibly related" | CLAIM-senzing-08 | Relationship discovery (household, shared address) as a by-product of ER | integrate | Map to PROPOSED `POSSIBLY_RELATED` edges in the prediction plane (BL-40) | Possibly-related edges never appear in fact queries unless approved (J8) |

### Con-to-Pro inversion cards

**INV-senzing-01 — Non-redistributable proprietary engine blocks white-label embedding**
- *Target:* Senzing SDK 4.4.2 under EULA May 2026.v1, embedded in a white-label, multi-tenant product.
- *Limitation:* no distribution right, no sublicense, no third-party access, one production instance per licence, no benchmark publication without consent [CLAIM-senzing-05].
- *Root cause:* licensing (**proven**).
- *Why an alternative helps, and when it is worse:* an EOIP-native ER stack (deterministic principle tier, Splink FS scorer, identity ledger) built only on permissive components can ship in every tenant. It is worse for customers who already own Senzing and need its tuned name, address and identifier comparators and decades of principle refinement. That is why the integration path stays open.
- *Options:*
  1. **Quick integration:** `SenzingIdentityProvider` adapter. The customer installs a licensed Senzing on its own hardware; EOIP calls the SDK in the customer's process and consumes `WITH_INFO`.
  2. **Pragmatic native enhancement:** EOIP-native principle engine (feature behaviours declared in the ontology) plus Splink scorer plus ledger, the default in all editions.
  3. **Long-term differentiated:** the identity ledger as a pluggable "identity authority" interface (native, Senzing, customer MDM) with bitemporal identity history, ACL-preserving merges and evidence. Customers can switch providers without re-keying the graph.
- *Selected:* option 2 as default, with option 3's interface designed from day one. Option 1 is an INTEGRATE connector, supported only with a customer-held licence and after legal review.
```
interface IdentityAuthority:
    resolve(record) -> list[IdentityChanged]      # synchronous or queued
    explain_why(a, b) -> Evidence
    explain_how(entity) -> Steps
    reevaluate(component) -> list[IdentityChanged]
impl NativeAuthority(principles=ontology.identity_profile, scorer=Splink, ledger=Ledger)
impl SenzingAuthority(sz_engine)                   # customer-licensed, optional
graph mutation gateway consumes IdentityChanged; canonical EOIP IDs map 1:n to provider IDs
```
- *Falsifiable POC (POC-ER-04):* on the POC-ER-01 dataset, compare NativeAuthority with SenzingAuthority (evaluation licence, results kept internal per EULA §2). Success: native pairwise F1 within 3 pp of Senzing on person entities; switching providers changes ≤ 0.5 % of canonical EOIP IDs, with every change logged. Cost baseline: one 8-core / 32 GB node, PostgreSQL local.
- *Dependencies, migration, security:* the provider-ID ↔ EOIP-ID map must be tenant-scoped, and Senzing repositories must be per tenant. Failure cases: a provider merge that crosses permission domains, so per-member ACLs must be kept; benchmark results must not be published without Senzing consent.
- *Defensibility:* provider-neutral identity with evidence and history is something neither Senzing nor Splink offers.
- *Decision:* **ADOPT** (option 2 + interface); option 1 **EXPERIMENT**, gated by legal review.

**INV-senzing-02 — Opaque, vendor-tuned principles and unverifiable accuracy**
- *Target:* Senzing accuracy claims and proprietary comparators.
- *Limitation:* accuracy is asserted without metrics, internals cannot be inspected (reverse engineering prohibited), and publishing comparisons is restricted [CLAIM-senzing-05][CLAIM-senzing-12].
- *Root cause:* licensing and maturity of public evidence (**proven** for licence; accuracy **hypothesis**).
- *Alternative:* EOIP ships an open, reproducible ER evaluation harness and per-tenant model cards. Customers measure accuracy on their own labelled samples (MoJ-style clerical labelling [CLAIM-splink-16]). This is worse in effort, because it needs labels.
- *Options:* (1) document only; (2) built-in evaluation harness with clerical sampling UI and B³/pairwise metrics; (3) continuous identity-quality monitoring (drift of merge rates, generic-value rates, review overturn rate) with alerts.
- *Selected:* options 2 + 3.
- *POC:* per-tenant monthly report generated from 300 sampled pairs; reviewer-overturn rate is tracked. Success: report reproducible from stored samples and model version.
- *Defensibility:* transparency is a buying criterion in regulated sectors (CLAIM-splink-16 pattern).
- *Decision:* **ADOPT**.

**INV-senzing-03 — Second identity store outside the graph**
- *Limitation:* Senzing keeps its own repository and entity graph [CLAIM-senzing-04][CLAIM-senzing-10]. Integrating it means dual state.
- *Root cause:* architecture/coupling (**proven**).
- *Selected mitigation:* the EOIP ledger is the authority of record for canonical IDs. Provider state is treated as a derivable cache that can be rebuilt by replaying SourceEvents (BL-24).
- *POC:* drop the Senzing repository, replay, and assert that the canonical-ID map is restored with 100 % parity.
- *Decision:* **EXPERIMENT** (with INV-senzing-01 option 1).

**Seed hypothesis (§10.5):** none targets Senzing.

## 13. Per-capability decisions

| Capability | Decision | Reason |
|---|---|---|
| CAP-31 real-time ER with merge/unmerge | **BUILD** natively (ledger + re-evaluation); patterns from Senzing | Licensing blocks bundling |
| CAP-31 Senzing as optional identity authority | **INTEGRATE** (customer-licensed, legal review) | Large installed base in regulated sectors |
| CAP-30 feature-behaviour deterministic principles | **BUILD** | Adopt the F1/FF/FM × exclusive × stable pattern in the ontology identity profile |
| CAP-24 why/how/what-if explanation | **BUILD** | Pattern match |
| CAP-43 possible/related outcomes as PROPOSED | **BUILD** | Fits BL-40 |
| CAP-52 white-label embedding of Senzing | **REJECT** under the standard EULA | No distribution right |
| CAP-78 ER evaluation harness | **BUILD** | Counter to unverifiable claims |

## 14. Concrete tests, proof-of-concept, and acceptance conditions (all PROPOSED)

- **POC-ER-04:** native vs Senzing (above). Results are internal only (EULA §2).
- **T-SZ-ORDER:** order-independence, 5 permutations, identical partitions after redo drain (native implementation must pass; Senzing used as oracle).
- **T-SZ-GENERIC:** generic-value flip → unmerge proposals within one cycle.
- **T-SZ-DELETE:** delete a bridging record → the entity splits; graph edges move to the correct survivors; the event is in the ledger (J7).
- **T-SZ-AIRGAP:** Senzing adapter installed with no network; all calls succeed (licence activation offline — verify).
- **T-SZ-TENANT:** two tenants → two repositories; no cross-tenant candidate is ever returned (J13).

## 15. Risks, trade-offs, and open research questions

- **Legal:** distribution, OEM and benchmark-publication clauses need counsel before any packaged integration.
- **Cost:** per-DSR pricing multiplied by tenants.
- **Lock-in:** Senzing entity IDs used as primary keys would couple the graph to a proprietary engine. Keep EOIP IDs canonical.
- **Open questions:**
  1. Offline licence activation mechanics?
  2. Supported multi-tenant pattern?
  3. Configurable survivorship?
  4. Exact PostgreSQL minimum (14 or 15)?
  5. Does the MCP server send data off-host?

## Appendix A — Research-dimension coverage

| Dimension | Section(s) | Summary or N/A reason |
|---|---|---|
| D1 Identity and maturity | 1 | Senzing Inc., 4.4.2 (2026-10-01), 2-year line support |
| D2 Problem and workloads | 2 | Real-time ER for KYC, fraud, 360 |
| D3 Architecture | 4 | Library + RDBMS repository |
| D4 Storage and indexing | 5.1, 5.4 | Record/feature libraries in RDBMS; index internals NOT PUBLICLY VERIFIED |
| D5 Schema and semantics | 5.1 | Feature behaviours; entity spec JSON |
| D6 Query pipeline | 5.3 | API calls; no query language |
| D7 Reasoning | 5.2 | Principle rules + comparators; re-evaluation |
| D8 Transactions and scale | 5.4, 7 | DB transactions, retries, locks; vendor scale claims |
| D9 Ingestion and federation | 2 | add/delete/redo; no connectors in SDK |
| D10 Identity and evidence | 5, 11, 12 | Core topic |
| D11 Time and evolution | 5.2, 11 | Re-evaluation; bitemporal NOT PUBLICLY VERIFIED |
| D12 Graph algorithms and ML | 3, 5 | Path/network; no ML training |
| D13 Retrieval and agents | 3 | Search API; MCP server (claim) |
| D14 NL querying | N/A | None documented |
| D15 Governance | 5.5 | Config versioning; no review workflow verified |
| D16 Human experience | 3 | Desktop evaluation tool |
| D17 Developer experience | 1, 9 | Multi-language SDK; v4 breaking changes |
| D18 Trust and security | 5.5, 10 | DB auth, PCI masking; telemetry unverified |
| D19 Multi-tenancy / white-label | 10 | Not native (assumed); EULA blocks white-label bundling |
| D20 Economics | 1, 7 | $58,560/yr per 10M DSR; vendor performance claims |
| D21 Commercial / licensing | 1, 10 | Proprietary EULA; partner programme |
| D22 Interoperability / lock-in | 10, 15 | JSON in, JSON out; ID lock-in risk |
| D23 IP and prior art | 15 | Proprietary methods; no patent search performed — legal review if native design mirrors principles closely |
| D24 Research quality | 7, App. C | Vendor docs only; no independent benchmarks (EULA restricts) |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-31 | native (real-time ER, merge/unmerge, relationships) | CLAIM-senzing-08..11 | BL-36 Absent; BL-35 Partial | BUILD native; INTEGRATE optional | P1 |
| CAP-30 | native (principles) | CLAIM-senzing-08 | BL-34 Implemented (person) | BUILD (pattern) | P1 |
| CAP-24 | native (why/how) | CLAIM-senzing-10 | BL-48 Partial | BUILD | P2 |
| CAP-43 | partial (possible/related outcomes) | CLAIM-senzing-08 | BL-40 Implemented (contract) | BUILD | P1 |
| CAP-50 | plausible on-prem (unverified offline licensing) | CLAIM-senzing-05 | — | EXPERIMENT | P2 |
| CAP-52 | blocked by EULA | CLAIM-senzing-05 | BL-21 | REJECT bundling | P1 (legal) |
| CAP-77 | proprietary, per-DSR | CLAIM-senzing-06 | BL-22 | — (TCO input) | P2 |
| CAP-59 | MCP server (claim) | CLAIM-senzing-12 | BL-47 | DEFER | P3 |

## Appendix C — Evidence records

| CLAIM-ID | Product / version / date | Exact claim | Classification | Source | Pub. / access | Confidence | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-senzing-01 | SDK 4.x | 4.4.2 2026-10-01; 4.4.0 2026-08-31 (EOL 2028-08-31); 4.3.5 2026-09-09; 4.2.4 2026-04-09; 4.1.0 2025-10-13; 4.0.0 2025-08-27; each line supported 2 years | Officially documented | Release history https://www.senzing.com/releases | / 2026-10-18 | 0.9 | None |
| CLAIM-senzing-02 | 4.4.0 | Opt-in DB-native locking (PG, MSSQL); native CLI binaries Linux/macOS/Windows; Python 3.10+ for Python SDK; MSSQL UTF-8 collation; MySQL utf8mb4; no schema change from any v4; 4.0.0 required schema+config upgrade | Officially documented | https://www.senzing.com/releases | 2026-08-31 / 2026-10-18 | 0.85 | None |
| CLAIM-senzing-03 | 4.3.0 | `internal://` in-memory store gains vector search, path finding, export, disclosed relationships; for demos <10k records | Officially documented | https://www.senzing.com/releases | 2026-05-19 / 2026-10-18 | 0.85 | None |
| CLAIM-senzing-04 | v4 | DBs: AWS RDS, Aurora PostgreSQL, Azure SQL, MSSQL ≥2019, MySQL ≥8.4.7 (<100M), Oracle ≥19c, PostgreSQL ≥14, SQLite 3.38 (<1M); Db2 and MariaDB unsupported | Officially documented | v4 System Requirements https://www.senzing.com/docs/release/4/4_0_hw_sw ; breaking changes https://www.senzing.com/docs/release/4/4_0_breaking_changes/4_0_breaking_changes_hw_sw/ | / 2026-10-18 | 0.75 | Breaking-changes page: PostgreSQL <15 unsupported |
| CLAIM-senzing-05 | EULA May 2026.v1 | Non-exclusive, non-transferable, no sublicense; one production instance; no right to distribute; hardware owned/controlled by licensee; no third-party access; no reverse engineering; no publishing performance info/comparisons without consent; audits ≤ quarterly; Delaware law | Officially documented | "End User Licensing Agreement" https://senzing.com/?p=37133 | 2026-05-14 / 2026-10-18 | 0.85 legal text read via fetch summary | None |
| CLAIM-senzing-06 | Pricing page (modified 2026-07-09) | Priced per DSR; $58,560/yr for 10M DSRs, up-front payment, standard EULA; custom terms → custom price; partner programme on request | Officially documented | https://senzing.com/pricing | 2024-05-22 (mod. 2026-07-09) / 2026-10-18 | 0.8 | Older page "as of May 2022" lists $46,800/yr (superseded) |
| CLAIM-senzing-07 | v4 quickstart / eval | Free use for 500 source records; larger evaluation on request; desktop evaluation up to 100k records | Officially documented | v4 Linux Quickstart https://senzing.com/docs/quickstart/quickstart_api ; https://senzing.com/?p=37088 | / 2026-10-18 | 0.7 | None |
| CLAIM-senzing-08 | Whitepaper PBTO062226 | Feature behaviours: frequency (F1/FF/FM/FVM/NAME/NONE), exclusivity, stability; Table 1 examples; ~35 principles; MATCH / POSSIBLE MATCH / POSSIBLY RELATED examples; skip-on-conflicting-exclusives; generic SSN learned and prior records re-evaluated; no training/tuning | Officially documented (vendor whitepaper) | "Principle-based entity resolution explained" https://senzing.com/wp-content/uploads/2026/07/Principle-Based-Entity-Resolution_062226.pdf | 2019/2026 / 2026-10-18 | 0.75 vendor description of own design | None |
| CLAIM-senzing-09 | Senzing docs | Records kept in original form; features standardised + derived; generic values excluded from candidate selection; comparator buckets same/close/likely/plausible/unlikely/not same; principles; prior assertions re-evaluated; record-to-entity matching; no pre-tuning | Officially documented | "How entity resolution works with Senzing" https://senzing.com/how-entity-resolution-works-with-senzing/ | / 2026-10-18 | 0.75 | None |
| CLAIM-senzing-10 | sz-sdk-python docs | add_record (replace same DS+ID), delete_record (idempotent, re-resolves), reevaluate_entity/record, why_entities/records/record_in_entity/search, how_entity_by_entity_id, get_virtual_entity_by_record_id, get/process_redo_record, search_by_attributes (SEARCH/INGEST profiles), find_path/network | Officially documented | https://garage.senzing.com/sz-sdk-python/senzing.html | / 2026-10-18 | 0.85 | None |
| CLAIM-senzing-11 | v4 | SZ_WITH_INFO returns AFFECTED_ENTITIES (new, updated, no longer valid) on add/delete | Officially documented | v4 beta SDK breaking changes https://senzing.com/docs/4_beta/4_0_breaking_changes/4_0_breaking_changes_sdk | / 2026-10-18 | 0.65 beta-era page via search summary | None |
| CLAIM-senzing-12 | Innovation page (2026-07) | ~560 MB engine (~7× smaller); cold start ~0.5 s; ~100B records in production; ~10M records ~3 h <$100 (2020 serverless); MCP server cuts onboarding ~300 h → <3 h; accuracy "outperforms humans" | Unverified (vendor marketing) | https://senzing.com/innovation/ | 2026-07-09 / 2026-10-18 | 0.25 no hardware/dataset | None independent |
| CLAIM-senzing-13 | sz-sdk-python | Apache-2.0 abstract base classes; "work-in-progress", not recommended yet | Observed (repository page) | https://github.com/senzing-garage/sz-sdk-python | / 2026-10-18 | 0.8 | None |
| CLAIM-senzing-14 | 4.2.0 | Faster startup, lower memory; credit-card plugin with PCI DSS-compliant masking; PG17+ chunked mode; Aurora PG IAM auth; Azure SQL Entra ID | Officially documented | https://www.senzing.com/releases | 2026-01-28 / 2026-10-18 | 0.85 | None |
| CLAIM-senzing-15 | 4.3.x | 4.3.0 flags important MSSQL table-scan fix on update; 4.3.1 EMAIL key and non-Latin address fixes; 4.3.2 automatic PG retries; 4.3.3 transaction/retry hardening, SQLite deadlock fix | Officially documented | https://www.senzing.com/releases | 2026 / 2026-10-18 | 0.8 | Minor attribution differences between summaries (4.3.2 vs 4.3.3) |
| CLAIM-senzing-16 | Literature | Benchmark ER performance often over-optimistic vs real world | Third-party report (academic) | "Estimating the Performance of Entity Resolution Algorithms: Lessons Learned Through PatentsView.org" https://arxiv.org/pdf/2210.01230 | 2022 / 2026-10-18 | 0.6 | None |
| CLAIM-senzing-17 | HPCwire 2019 | Single commodity server handles up to 400M records (citing a Senzing white paper) | Third-party report | https://www.hpcwire.com/bigdatawire/2019/06/27/inside-jeff-jonas-big-plan-to-democratize-entity-resolution/ | 2019-06-27 / 2026-10-18 | 0.3 old, secondary | None |
| CLAIM-senzing-18 | — | Offline licence activation, native multi-tenancy, configurable survivorship, telemetry | Unverified | — | / 2026-10-18 | 0.2 | — |
| CLAIM-senzing-19 | v4 | Entity specification: map attributes (e.g. NAME_FIRST/NAME_LAST) into features; DATA_SOURCE + RECORD_ID identify records; `preprocess_record()` for mapping checks | Officially documented | Entity Specification https://senzing.com/docs/entity_specification/ ; What's New in v4 https://senzing.com/docs/release/4/whatsnew/ | / 2026-10-18 | 0.7 | None |

## Appendix D — Assumptions

1. "Senzing" means the Senzing SDK from Senzing, Inc., v4 line.
2. EULA content was read through a fetch summary with quoted clauses; the full text must be read by counsel.
3. List price is indicative; OEM pricing is unknown.
4. Internals (indexes, candidate keys, thresholds) are hypotheses beyond what the whitepaper and docs state.
5. No Senzing software was installed or run; no benchmark was performed (and publishing one would need consent).
