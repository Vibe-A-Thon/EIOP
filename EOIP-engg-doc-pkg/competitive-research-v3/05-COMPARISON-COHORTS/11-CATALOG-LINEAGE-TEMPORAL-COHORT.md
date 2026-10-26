# Cohort 11 — Metadata Catalogs, Lineage, Provenance and Temporal/Versioned Stores

| Field | Value |
|---|---|
| Cohort ID | COH-11 |
| Workload class | Knowing what data exists and where it came from (catalog, lineage, provenance), and being able to ask "what did the graph look like then, and how did it change" (bitemporal, versioned, event-sourced storage) |
| Catalog/lineage members | [DataHub](../04-COMPETITOR-DEEP-DIVES/C06-datahub.md), [Atlan](../04-COMPETITOR-DEEP-DIVES/C06-atlan.md), [Collibra](../04-COMPETITOR-DEEP-DIVES/C06-collibra.md), [data.world](../04-COMPETITOR-DEEP-DIVES/C06-data-world.md), [OpenMetadata](../04-COMPETITOR-DEEP-DIVES/C06-openmetadata.md), [Apache Atlas](../04-COMPETITOR-DEEP-DIVES/C06-apache-atlas.md), [Microsoft Purview](../04-COMPETITOR-DEEP-DIVES/C06-microsoft-purview.md) |
| Temporal/versioned/provenance members | [OpenLineage/Marquez](../04-COMPETITOR-DEEP-DIVES/C13-openlineage-marquez.md), [PROV-O](../04-COMPETITOR-DEEP-DIVES/C13-prov-o.md), [Event sourcing / CQRS / bitemporal patterns](../04-COMPETITOR-DEEP-DIVES/C13-event-sourcing.md), [XTDB](../04-COMPETITOR-DEEP-DIVES/C13-xtdb.md), [Datomic](../04-COMPETITOR-DEEP-DIVES/C13-datomic.md), [Dolt](../04-COMPETITOR-DEEP-DIVES/C13-dolt.md) |
| Cross-references | [TerminusDB](../04-COMPETITOR-DEEP-DIVES/C01-terminusdb.md) (versioned graph/document store), [Graphiti/Zep](../04-COMPETITOR-DEEP-DIVES/C08-graphiti-zep.md) (bitemporal agent-memory angle) |
| Tier C records | [C06-tier-c-records-V18](../04-COMPETITOR-DEEP-DIVES/C06-tier-c-records-V18.md): OvalEdge, Actian DIP (ex-Zeenea), Egeria, Amundsen (archived), Unity Catalog OSS, Apache Polaris, Alation, Informatica CLAIRE/IDMC, Google Dataplex; [C13-tier-c-records-V26](../04-COMPETITOR-DEEP-DIVES/C13-tier-c-records-V26.md): Fluree, lakeFS, Iceberg/Delta Lake time travel, Spline, AeonG research |
| Reference columns | HugeGraph, Neo4j, Neptune (temporal/versioning rows only; none offers a catalog) |
| EOIP status basis | `01-SYSTEM-BASELINE.md` (BL, ad9937b) superseded by `01a-BASELINE-DELTA-HEAD.md` (HEAD 896e06d, BL/NB rows) |
| Related BL | BL-32 ontology-as-code/stewardship, BL-37 bitemporal reads, BL-38 diff/snapshots/playback, BL-39 claims/contradictions, BL-40 epistemic separation, BL-41 evidence/lineage |
| Date | 2026-10-26 |

Count: 7 core C06 deep dives + 6 core C13 deep dives + 2 cross-reference deep dives (C01, C08) = 15 Tier A/B deep dives, plus 2 Tier C batches (9 + 5 records).

## 1. Workload class and comparison basis

**Customer workloads.** (a) "What datasets, tables and columns exist, who owns them, and are they governed?" (catalog). (b) "Where did this fact come from, and what transformed it?" (lineage, provenance). (c) "What did this record/graph look like as of a past date, and can I branch, diff or roll back?" (bitemporal/versioned storage).

**Why comparable.** All fifteen deep dives describe systems whose job is to make the graph's history and metadata trustworthy and queryable, rather than to store the graph's current state (that is cohort 01/02). They are compared on: granularity of lineage (table vs column vs fact-level), whether time is one axis (transaction-time only) or two (bitemporal), whether branch/diff/merge exists, and self-host/air-gap viability.

**Sub-groups.** Catalogs (DataHub, Atlan, Collibra, data.world, OpenMetadata, Apache Atlas, Microsoft Purview) answer "what exists". Lineage/provenance (OpenLineage/Marquez, PROV-O) answer "where did it come from". Temporal/versioned stores (event-sourcing patterns, XTDB, Datomic, Dolt, TerminusDB) answer "what did it look like, and can I go back". Graphiti/Zep is cross-referenced only for its bitemporal edge model, not as a catalog or store.

**Excluded.** Lakehouse table catalogs (Unity Catalog OSS, Apache Polaris) are Tier C, REFERENCE-ONLY or INTEGRATE-as-source only; they are metadata about files, not an enterprise semantic catalog. Fluree and lakeFS are Tier C under source-available licences and are not scored against DataHub/OpenMetadata. Spline and AeonG are research/adjacent and REFERENCE-ONLY in their own records.

## 2. Capability comparison

Notation: `dh-` datahub, `atl-` atlan, `col-` collibra, `dw-` data-world, `om-` openmetadata, `atlas-` apache-atlas, `pv-` microsoft-purview, `ol-` openlineage-marquez, `prov-` prov-o, `es-` event-sourcing, `xtdb-`, `datomic-`, `dolt-`, `term-` terminusdb, `gz-` graphiti-zep, `n4-` neo4j, `hg-` apache-hugegraph, `nep-` amazon-neptune. `unknown` = not publicly verified.

### 2.1 Catalog members

| Capability | DataHub | Atlan | Collibra | data.world | OpenMetadata | Apache Atlas | Microsoft Purview | EOIP @HEAD |
|---|---|---|---|---|---|---|---|---|
| CAP-42 catalog / metadata model | native: entity-aspect model, URN-identified, versioned aspects (dh-05) | native, "Context Lakehouse" (atl-01) | native, governance-workflow centric (col §1) | native (dw §Appendix B) | native: per-entity JSON tables, `entity_relationship`, `change_event` (om-03) | native, Hadoop-centric type system (atlas-04) | native, Data Map plus Unified Catalog (pv-01, pv-02) | absent as a dedicated module; evidence manifests exist but no catalog entity model (BL-41; no BL-ID for `catalog/*`) |
| CAP-40 lineage | native: MCP/MCL async log, OpenLineage ingestion, Spark listener, column-level (dh-06, dh-09) | native, vendor claim only (atl-02) | native (col-01) | unknown (dw §7) | native: auto-extract, OpenLineage ingest, column-level, cross-DB (om-04) | native, lineage and classification propagation (atlas-04) | native but source-dependent (pv-02); Unity Catalog lineage limited to notebooks per a third party (pv-03) | Partial: evidence lineage exists (BL-41); SQL/table-level lineage not baselined |
| CAP-26 connectors into the catalog | native (dh-09) | native (atl-01) | native via Edge (col-04) | unknown | native, 130+ connectors (om-01) | native (Hadoop ecosystem) | native, Azure-only sources | Implemented, IT-focused connectors feed SourceEvents, not a catalog (BL-23) |
| CAP-46 ACL on catalog/lineage reads | enterprise-only / absent in core (dh §Appendix B) | unknown | unknown | unknown | unknown | unknown | unknown | Partial, same PDP gap as elsewhere (BL-18 HEAD) |
| CAP-47 tenant isolation | absent, hypothesis (dh-14) | n/a (SaaS single tenant) | n/a (SaaS) | n/a (SaaS) | unknown | unknown | n/a (SaaS) | Partial (BL-20 HEAD) |
| CAP-59 MCP tools | native, `get_lineage` etc. (dh-10) | vendor claim (atl-01) | unknown | unknown | native MCP at `/mcp` (om-01) | unknown | third-party only, no first-party MCP for Unified Catalog (pv-03) | Implemented, 18 read-oriented tools, one shared token (BL-47 HEAD) |
| Open interchange / standards | none native beyond its own model | none | none | SPARQL templates (dw-04) | JSON Schema, RDF/OWL, SHACL, JSON-LD claimed (om-01) | Atlas type system, used by Purview's Atlas-compatible API (pv-01) | Atlas-compatible APIs (pv-01) | JSON-LD export/import with loss accounting (BL-31) |

### 2.2 Lineage, provenance, temporal/versioned stores

| Capability | OpenLineage/Marquez | PROV-O | Event sourcing/CQRS/bitemporal (pattern) | XTDB | Datomic | Dolt | TerminusDB | Graphiti/Zep (cross-ref) | EOIP @HEAD |
|---|---|---|---|---|---|---|---|---|---|
| CAP-38 provenance model | native run/job/dataset events, open JSON-Schema spec (ol-01) | native: standard OWL 2 vocabulary for derivation (prov-01) | pattern only | n/a | n/a | n/a | n/a | native episode provenance (gz CLAIM-05, -10) | Implemented: evidence manifests, warrant composition/order added at HEAD (BL-41, NB row) |
| CAP-40 lineage granularity | native, job/run/dataset/column-level via facets (ol-01, ol-04) | n/a (vocabulary, not a system) | n/a | n/a | n/a | n/a | n/a | n/a | Partial, evidence-level lineage, not dataset/job-level |
| CAP-34 bitemporal / as-of queries | n/a | n/a | pattern: two time axes, valid vs transaction time (es-01) | native, automatic bitemporality (xtdb-03) | partial: transaction-time only (datomic-04) | n/a (versioned tables, not bitemporal) | partial, unverified (term-02) | native on edges, valid-time only for memory (gz CLAIM-05) | Implemented: `temporal/authorized_as_of.py`, `deterministic_graph.py` added at HEAD (BL-37 HEAD) |
| CAP-35 branch/diff/merge | n/a | n/a | n/a | n/a (no branching found) | n/a | native: git-style branch, merge, push/pull, diff (dolt-02) | native: commits, branches, diff, patch, push/pull/clone (term-02) | n/a | Implemented: `graph/diff_engine.py`, snapshots, playback (BL-38) |
| CAP-36 event sourcing / history | n/a | n/a | pattern: append-only log, CQRS projections (es-01) | native (xtdb-03) | native (datomic-04) | partial (dolt-02) | partial | n/a | Implemented: revisions, `execution/eventstore.py`, WAL/backup (BL-37, BL-50) |
| CAP-37 schema/ontology evolution | n/a | n/a | pattern (es-01) | n/a | n/a | partial, table schema versioning (dolt-02) | n/a | n/a | Partial: lint rules, SKOS governance, `gitops.py` unchanged at HEAD (BL-32 HEAD) |
| CAP-16 SQL / query surface | n/a | n/a | n/a | native SQL over bitemporal data (xtdb-02) | native Datalog, not SQL | native, MySQL-compatible server (dolt-01) | native GraphQL/WOQL, not SQL | n/a | Absent (BL-59) |
| CAP-74 backup/restore/PITR | n/a | n/a | n/a | partial, history retained forever on object storage (xtdb-02) | n/a | n/a | n/a | n/a | Implemented (scripts), live-unverified (BL-50) |
| Licence class | Apache-2.0 (ol-02) | W3C document licence (prov-01) | n/a (ideas) | MPL-2.0-or-later, weak copyleft (xtdb-02) | binaries Apache-2.0, source closed (datomic-02, datomic-03) | Apache-2.0 (dolt-01) | Apache-2.0 (term-01) | Apache-2.0 core; FalkorDB backend is SSPL (gz CLAIM licence row) | n/a |

### 2.3 Reference columns

| Capability | HugeGraph | Neo4j | Neptune | EOIP @HEAD |
|---|---|---|---|---|
| CAP-34 bitemporal | absent, TTL only (hg §5.9, per C01 dive) | absent; history only via WAL-based PITR and CDC, both Enterprise-only (n4-17, per C01 dive) | absent (nep-14, per C01 dive) | Implemented at the application layer (BL-37) |
| CAP-35 branch/diff | absent | absent | absent | Implemented (BL-38) |
| CAP-36 change capture | native RocksDB snapshots (hg §5.9) | enterprise-only CDC (n4-17) | native Streams, 7-day default retention, 1 to 90 configurable (nep-14) | Implemented in-process (BL-52), own log authoritative |
| CAP-42 catalog | absent | absent | absent | absent |

## 3. Operational and licensing comparison

| Member | Licence class | Redistribution / OEM trigger | Deployment and footprint | Air-gap | Maintenance (as verified 2026-10) |
|---|---|---|---|---|---|
| DataHub | Apache-2.0 core (dh-02) | none for OSS core; **check**: optional Neo4j backend is GPLv3, Elasticsearch terms differ from OpenSearch (dh §10) | 3+ stateful services (DB, Elasticsearch/OpenSearch, Kafka) plus optional Neo4j; quickstart needs about 8 GB RAM, OOM kills documented (dh-13) | plausible, self-hosted | active, v1.7.0 on 2026-08-04, v1.7.0.1 patch, v1.6.0.x still patched (dh-04) |
| Atlan | proprietary core; SDKs Apache-2.0 (atl-03) | **legal review**: any reuse of docs/typedef layouts | SaaS only | not publicly verified, assume no | active |
| Collibra | proprietary | none beyond proprietary terms | Edge on customer K8s, control plane in vendor cloud; outage stops ingestion while SaaS stays up (col §7, hypothesis) | no for core (inferred, 0.6) | active; Raito and Deasy Labs acquisitions in 2025 (col-02, col-03) |
| data.world | proprietary, ServiceNow-owned since July 2025 (dw-01, dw-02) | none identified | SaaS only | no evidence | acquired; packaging inside ServiceNow not publicly verified |
| OpenMetadata | Apache-2.0 (om-01) | community-vs-enterprise split (Collate) is a **legal-review trigger** | Docker/Helm/bare metal; one-replica sizing 4 vCPU/16 GiB server plus DB plus Elasticsearch (om-05) | viable, 0.7 | very active, four patch releases in 3 weeks (om-02) |
| Apache Atlas | Apache-2.0, ASF (atlas-01) | none at ASF; vendor distributions (Cloudera) add features | JanusGraph + HBase + Solr + Kafka, heavy; one-node-first is hard (atlas §10) | viable | maintenance-to-active, about 15 months between minors (atlas-02) |
| Microsoft Purview | proprietary, pay-as-you-go (pv-01) | none; integrate only as upstream source | managed Azure only | no, core is Azure | active |
| OpenLineage/Marquez | Apache-2.0 (ol-02) | none identified | Docker/K8s, Postgres required | viable | spec active; Marquez reference server effectively maintenance (ol §1) |
| PROV-O | W3C document licence | none (vocabulary) | zero runtime dependency | trivial | stable since 2013, no verified successor (prov §1) |
| Event sourcing (pattern) | none | none | any store can host the log | trivial | n/a, a pattern |
| XTDB | MPL-2.0-or-later (xtdb-02) | low legal-review flag (weak, file-level copyleft) | JVM plus object store plus log; embeddable in-process | viable with local object store (hypothesis) | active, 2.x GA, rolling-upgrade requirement between 2.1.1 and 2.2.0 (xtdb-01) |
| Datomic | binaries Apache-2.0, source closed (datomic-02, datomic-03) | **legal review**: closed-source binary dependency, confirm EULA scope for OEM | transactor-bound writes; working set must fit peer caches | viable, hypothesis | active, release 2026-10-16 (datomic-01) |
| Dolt | Apache-2.0 (dolt-01) | none | single Go binary or Docker | viable | active, releases within days |
| TerminusDB | Apache-2.0 (term-01) | none verified | Docker/self-hosted | viable | active, v12.0.8 on 2026-10-12; maintainer now Gettier/DFRNT, no acquisition announcement found (term-02) |
| Graphiti (cross-ref) | Apache-2.0; `posthog` hard dependency MIT (gz CLAIM licence row) | FalkorDB backend SSPL if bundled | air-gap viable with Neo4j/FalkorDB plus local LLM | viable | active, monthly cadence |

## 4. Performance evidence

No comparable, reproducible benchmark exists across any pair of members. Everything below is a vendor or author claim.

| Source | Figure | Context | Class |
|---|---|---|---|
| DataHub (dh-12) | "Proven to 10M+ assets and O(1B) relationships" | no hardware or workload | vendor, 0.3 |
| Atlan (atl-04) | "5x agent accuracy" | no workload or hardware | internal vendor claim, not usable |
| Microsoft Purview (pv-01) | capacity unit: 25 ops/s and 10 GB per unit | billing unit, not a benchmark | official but not comparative |
| AeonG research (C13 Tier C) | up to 5.73x lower storage, 2.57x lower temporal latency vs unspecified baseline | research prototype on Memgraph fork; workload/hardware not extracted | author claim, 0.7 confidence on the citation only |
| Zep paper (gz CLAIM-20, cross-ref) | DMR 94.8% vs MemGPT 93.4%; "up to 18.5%" LongMemEval gain | vendor-authored paper, small saturated benchmark | vendor, not independently reproduced |
| EOIP | none measured for lineage granularity, catalog scale, or bitemporal query latency | `graph/diff_engine.py`, `temporal/*` untested at scale | not run |

No winner can be declared on performance. The comparable ground is functional: lineage granularity (column vs job vs fact), whether bitemporality is native to the store or layered at the application, and whether branch/merge exists at all.

## 5. Findings

1. **EOIP has no catalog entity model, and every catalog member does.** DataHub's URN-identified entity/aspect model (dh-05), OpenMetadata's per-entity JSON tables (om-03) and Apache Atlas's type system (atlas-04) all give a first-class "what exists" layer; EOIP's evidence manifests (BL-41) record provenance for facts already in the graph but nothing enumerates datasets, tables or columns as catalog objects. This is a genuine gap, not a BL/NB row that can be marked Partial.
2. **Dataset/column/job-level lineage is a capability EOIP does not have, and OpenLineage is the standards-track way to get it.** OpenLineage is an open JSON-Schema spec with Spark/Airflow/dbt/Flink integrations (ol-01); DataHub and OpenMetadata both ingest OpenLineage events directly (dh-09, om-04). EOIP's lineage is evidence-to-fact (BL-41), not job/dataset-to-dataset. These are complementary, not substitutes: combining both is the opportunity, not a replacement.
3. **EOIP's bitemporal model is ahead of every graph-engine reference column and most catalogs, but behind the dedicated temporal databases in standards maturity.** HugeGraph has TTL only, Neo4j's history needs Enterprise CDC/PITR, Neptune has none (all per their C01 dives). XTDB gives automatic bitemporality natively in the database (xtdb-03) and event-sourcing theory names SQL:2011 system/application time as the standards anchor (es-02) that EOIP's `temporal/*` modules do not cite. EOIP's bitemporal reads are Implemented at HEAD (`temporal/authorized_as_of.py`, `deterministic_graph.py`) but are application-layer, not store-native.
4. **Branch/diff/merge exists in EOIP (BL-38) and in exactly two members of this cohort, both for different data shapes.** Dolt gives Git semantics over SQL tables (dolt-02) and TerminusDB gives Git semantics over a document/graph store (term-02); neither is a catalog or lineage tool. No catalog product in this cohort documents branching. EOIP's `graph/diff_engine.py` and snapshots/playback are a distinctive combination once proven at scale (no benchmark exists for any member, including EOIP).
5. **Every commercial catalog's lineage-level access control is unknown or absent.** DataHub gates search-access controls to its enterprise Cloud tier (dh §Appendix B); no other catalog's deep dive found a documented lineage-level ACL. This mirrors EOIP's own BL-18 gap (Partial at HEAD) rather than giving competitors an edge — nobody in this cohort has solved permission-filtered lineage.
6. **Closed-source-with-free-binaries is a real middle category, and it carries legal review regardless of price.** Datomic's binaries are Apache-2.0 at no cost but the source is closed (datomic-02, datomic-03); the deep dive flags EULA scope for OEM white-label as unresolved. This is a distinct risk from AGPL or proprietary SaaS and needs its own legal checklist entry.
7. **Source-available (BSL) licences recur in this space and are explicitly excluded from bundling.** Fluree (BSL 1.1, hosted-offering restriction) and lakeFS (BUSL-1.1, four-year Apache conversion) are both Tier C REFERENCE-ONLY for exactly this reason; both are still useful as design references for branch/merge and hook-gated publish patterns.
8. **PROV-O is the only standards-track vocabulary in this cohort, and EOIP already emits a PROV-shaped structure without importing the vocabulary.** EOIP's mapping executor adds roughly 3 triples per derived entity for unqualified PROV (prov §7, reasoned from code); formally adopting the `http://www.w3.org/ns/prov#` namespace (prov-01) would make evidence manifests directly interoperable with any PROV-O consumer, at the cost the deep dive estimates as near zero for unqualified form.
9. **Lineage-over-MCP is an emerging pattern among catalogs, not yet matched by EOIP's MCP server.** DataHub exposes `get_lineage` as an MCP tool (dh-10), OpenMetadata exposes MCP at `/mcp` (om-01), and Google Dataplex (Tier C) previews a lineage MCP server (C06 Tier C, gcp-01). EOIP's MCP server has no lineage-specific tool and authenticates every caller with one shared static token (BL-47 HEAD, noted in cohort 05 as well), which blocks exposing lineage safely over MCP today.
10. **Acquisitions have consolidated three of seven catalog vendors into larger platforms within the last 18 months.** data.world into ServiceNow (dw-01, dw-02, July 2025), Zeenea into Actian/HCLSoftware (C06 Tier C, actian-01, September 2024), and Informatica's pending acquisition by Salesforce (C06 Tier C, infa-01, unclosed per primary sources). Buyers evaluating a catalog in this space face vendor-roadmap uncertainty that a self-hosted, backend-neutral EOIP catalog module would not carry.

## 6. Implications for EOIP

| CAP | Parity needed (STR/pattern) | Exploitable weakness (INV) | Decision | Candidate gap statement |
|---|---|---|---|---|
| CAP-42 catalog entity model | DataHub entity/aspect/URN pattern (dh-05), OpenMetadata per-entity tables (om-03) | dh-13 (multi-service footprint), om §7 (sizing, not benchmark) | **BUILD** a thin catalog layer over existing graph entities, reusing BL-41 evidence identifiers as URNs; **INTEGRATE** Egeria's open type system only as an import vocabulary (Tier C, EXPERIMENT decision already recorded) | "No catalog entity model exists; evidence manifests cover facts, not datasets." |
| CAP-40 lineage (dataset/job/column) | OpenLineage spec and Marquez reference model (ol-01, ol-04) | ol §1 (Marquez maintenance-only) | **INTEGRATE** OpenLineage as the ingest-side lineage event format; **BUILD** a lightweight EOIP-hosted consumer rather than adopting Marquez | "Lineage is evidence-to-fact; no job/dataset/column-level lineage graph." |
| CAP-38 provenance vocabulary | PROV-O namespace (prov-01) | none; it is a vocabulary | **BUILD** PROV-O export mapping from `provenance/evidence.py` and `warrant_composition.py`; **REUSE** the vocabulary, do not reimplement a reasoner | "Evidence manifests are not PROV-O interoperable." |
| CAP-34 bitemporal at the store level | XTDB automatic bitemporality (xtdb-03), SQL:2011 anchor (es-02) | xtdb §7 (unverified scale), xtdb-01 (rolling-upgrade coupling) | **EXPERIMENT**: evaluate XTDB only as an optional history/audit side-store, not a `GraphStore` backend (xtdb dive's own recommendation, §10); **BUILD** citation of the SQL:2011 standard in `temporal/models.py` design docs | "Bitemporal reads are application-layer only; not benchmarked at scale." |
| CAP-35 branch/diff/merge | Dolt (dolt-02), TerminusDB (term-02) git-style semantics | dolt §9/term §9 (both unclear on conflict resolution at enterprise scale) | **REUSE** own (BL-38); **REFERENCE** Dolt/TerminusDB merge-conflict UX for the review workflow design | "Diff/snapshot/playback exists; merge-conflict handling under concurrent edits is unverified." |
| CAP-37 ontology/schema evolution | Dolt table-schema versioning (dolt-02) pattern | BL-32 `gitops.py` unchanged at HEAD | **BUILD**: extend `ontology/gitops.py` with the same branch/diff primitives already proven in BL-38, rather than treating ontology versioning as a separate problem | "Ontology stewardship is partial and mostly unmounted; gitops.py has not absorbed the graph-diff engine's primitives." |
| CAP-59 lineage-over-MCP | DataHub `get_lineage` tool (dh-10), Dataplex lineage MCP preview (C06 Tier C) | BL-47 shared static token (HEAD) | **BUILD** per-tenant MCP authentication before exposing any lineage tool; **DEFER** a lineage-specific MCP tool until then | "No lineage MCP tool; and MCP auth is a single shared token, so one could not be exposed safely today." |
| CAP-46 permissioned lineage/catalog | none demonstrated by any competitor | n/a (shared weakness) | **BUILD** ahead of the field; this is a differentiator opportunity, not a parity gap | "No competitor in this cohort documents permission-filtered lineage; neither does EOIP (BL-18 HEAD)." |
| Datomic, XTDB, Fluree, lakeFS as dependencies | n/a | legal triggers (closed-source binary, MPL, BSL, BUSL) | **REJECT** as bundled dependencies; **REFERENCE-ONLY** for design patterns | |
| Catalog vendors (Atlan, Collibra, data.world, Purview) as dependencies | n/a | all proprietary SaaS | **REJECT** as dependencies; **INTEGRATE** only as upstream sources for buyers who already run them (Purview, data.world via ServiceNow) | |

Backend neutrality: a catalog or lineage layer sits beside the `GraphStore` protocol, not inside it, so none of this cohort's recommendations touch HugeGraph, Neo4j or Neptune choice. HugeGraph's RocksDB snapshots and Neptune Streams are "available upstream / not integrated" change-capture mechanisms that a future lineage consumer could read from, rather than reimplement (both per their C01 dives).

## 7. Open questions

1. Can EOIP's evidence manifests (BL-41) be extended into catalog entities without duplicating the URN concept, or does this need a new BL-ID and module?
2. Does `ontology/gitops.py` (unchanged at HEAD per BL-32) already share code with `graph/diff_engine.py` (BL-38), or would merging them require new engineering?
3. Is XTDB's "history retained forever on object storage" model (xtdb-02) compatible with EOIP's tombstone and retention policies (BL-25), or does it conflict with DSAR erasure (privacy/dsr.py, BL-46)?
4. What does OpenLineage ingestion cost in EOIP's pipeline if adopted as the connector-to-catalog event format — is a new SourceEvent subtype needed?
5. Does the Zep/Graphiti bitemporal edge model (valid-time only, per gz CLAIM-05) suggest anything for EOIP's agent-memory design that `temporal/*` does not already cover?
6. Evidence conflicts: DataHub's component docs disagree on whether MySQL or Postgres, and Elasticsearch or OpenSearch, is the supported combination (dh-08, noted contradictory in the deep dive itself); OpenMetadata's production-sizing doc has conflicting database-storage numbers (om-05); Microsoft Purview's capacity-unit page shows an older "2 GB" figure superseded by "10 GB" (pv-01); TerminusDB's current maintainer (Gettier vs DFRNT vs the original company) is stated three ways across sources (term-02). None of these changes a decision above, but all should be re-verified before citing externally.
7. Which journey should drive the catalog build first: J2 (evolving organisational truth, which needs lineage across disagreeing sources) or J12 (arbitrary JSON onboarding, which needs a catalog entity for every newly inferred type)?
