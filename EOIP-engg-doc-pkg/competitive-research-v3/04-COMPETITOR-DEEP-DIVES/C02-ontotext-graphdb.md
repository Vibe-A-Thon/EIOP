# C02 — Ontotext GraphDB (now Graphwise GraphDB)

| Field | Value |
|---|---|
| Registry ID | T-C02-ontotext-graphdb |
| Tier | A — leading commercial RDF store; EOIP ships a "certified" `GraphDBGraphStore` adapter; reference for forward-chaining materialisation, SHACL and cluster design |
| Versions examined | GraphDB 11.4.3 (2026-08-06, latest found), 11.4.2 (2026-07-20), 11.4.1 (2026-07-09), 11.4.0 (2026-06-16), 11.3.3 (2026-04-23), 11.3.2 (2026-04-07); docs set 11.4 |
| Verified on | 2026-10-26 (actual access date; brief says 2026-10-18 — see Appendix D) |
| Worker | W08 (batch V02) |

## 1. Identity, current status, tier, and sources

**Identity and naming.** GraphDB is a proprietary RDF/SPARQL database with a rule-based reasoner. Ontotext (Sofia) and Semantic Web Company (PoolParty, Vienna) announced a merger on 2024-10-23 under the name **Graphwise**; both product brands continue, the old company names are being phased out, and documentation now lives at `help.graphwise.ai` (the older `graphdb.ontotext.com` docs still serve 11.4). [CLAIM-graphdb-01] A single aggregator article reports Oakley Capital took a majority stake in Graphwise; this is a third-party report and not confirmed from a primary source. [CLAIM-graphdb-02]

**Status.** Active. 11.4.0 shipped 2026-06-16 and three patches followed within eight weeks; 11.3.2/11.3.3 patched critical XXE (federated SPARQL), an Avatica RCE vector and an OCSP issue, so the security surface is non-trivial. [CLAIM-graphdb-03] [CLAIM-graphdb-04] Whether a release newer than 11.4.3 exists was not found (UNVERIFIED). The 11.4 line deprecates the Solr connector (removal in 12) and drops the OpenAI Assistants API. [CLAIM-graphdb-03]

**Master Prompt §5 traps resolved.** (a) Ontotext to Graphwise rename. (b) "Standard Edition" is "no longer offered" but supported for legacy customers; current editions are Free and Enterprise. [CLAIM-graphdb-05] (c) The registry says "Ontotext GraphDB"; the shipped product is Graphwise GraphDB 11.x. (d) Ontotext Refine (C03) and PoolParty are separate registry rows.

**Sources used (11):** Graphwise merger announcement and FAQ; GraphDB 11.4 docs (index, release notes, reasoning, SHACL, cluster, SPARQL compliance, requirements); Graphwise Free-vs-Enterprise comparison page; HPCwire GraphDB 11 article; Ontotext GraphDB 9.5 press release; EOIP source files. Reconstruction is documentation-only because the engine is closed source.

## 2. Primary problem, target workloads, concrete example workflows

| Workload | How GraphDB addresses it | Source |
|---|---|---|
| Semantic data integration with ontologies and inference | Load RDF, pick a ruleset, query with SPARQL over explicit plus inferred triples | [CLAIM-graphdb-07] |
| Constraint checking on RDF | SHACL via RDF4J ShaclSail, validated at commit | [CLAIM-graphdb-10] |
| Hybrid text+graph search | Lucene (all editions), Solr/Elasticsearch/OpenSearch/Kafka connectors (EE) | [CLAIM-graphdb-13] |
| Relational virtualisation | Ontop-based virtual repositories over SQL sources | [CLAIM-graphdb-17] |
| LLM question answering | "Talk to Your Graph", MCP prompts, entity linking, GraphRAG assets | [CLAIM-graphdb-14] |
| HA read scaling | Raft cluster (EE) | [CLAIM-graphdb-12] |

Example workflow (KnowGridFlow-relevant): ingest a Jira/Confluence-derived ontology as RDF into repository `eoip` with `owl2-rl`; ask "which services depend on class X transitively"; GraphDB answers from materialised `rdfs:subClassOf`/transitive closure at SPARQL speed, at the cost of load-time inference and costly schema deletions.

## 3. Feature inventory

| Feature | Status | Notes / CLAIM |
|---|---|---|
| SPARQL 1.1 Query/Update/Protocol/Federation/Graph Store | present ("mostly conforms"; 2 W3C tests fail) | [CLAIM-graphdb-15] |
| RDF-star / SPARQL-star | present (vendor table) | RDF 1.2 triple terms not mentioned [CLAIM-graphdb-18] |
| Forward-chaining reasoner, RDFS/RDFS-Plus/OWL-Horst/OWL-Max/OWL2-QL/OWL2-RL | present, all editions | [CLAIM-graphdb-07] |
| Custom `.pie` rulesets, consistency rules | present, consistency checking off by default | [CLAIM-graphdb-09] |
| SHACL Core + SPARQL constraints/targets | present; enable at repo creation only | [CLAIM-graphdb-10,11] |
| Raft HA cluster, external proxy | enterprise-only | [CLAIM-graphdb-12] |
| Lucene, ChatGPT connectors | all editions | [CLAIM-graphdb-13] |
| Solr, Elasticsearch, OpenSearch, Kafka connectors | enterprise-only (Solr deprecated) | [CLAIM-graphdb-13] |
| MongoDB connector | listed in vendor table, edition split UNVERIFIED | [CLAIM-graphdb-18] |
| GeoSPARQL, geo plugins, RDF Rank, plugin API | present | [CLAIM-graphdb-18] |
| Ontop virtual repositories | present, all editions (as of 9.5) | [CLAIM-graphdb-17] |
| LLM: TTYG, MCP prompts, entity linking, Azure OpenAI embeddings | present in 11.x; local-model support per third-party report | [CLAIM-graphdb-03,14] |
| Encryption at rest, AES-256-GCM per repository | present since 11.4 | [CLAIM-graphdb-03] |
| Workbench UI, REST, RDF4J API, GraphQL | present (GraphQL listed in docs sidebar, depth UNVERIFIED) | [CLAIM-graphdb-18] |
| Vector search | present via Azure OpenAI embeddings and similarity pages; index internals NOT PUBLICLY VERIFIED | [CLAIM-graphdb-03] |
| Multi-tenancy | repository-per-tenant is possible (hypothesis); no tenant model documented | — |
| Open-source licence | absent (proprietary) | [CLAIM-graphdb-06] |

## 4. Architecture diagram

```
 Clients: Workbench UI | SPARQL/REST | RDF4J API | MCP / TTYG agents | GraphQL
                 |
        +--------v---------------------------------------------+
        | GraphDB server (JVM, Java 21 JDK)                      |
        |  protocol layer - security/roles - plugin API          |
        |  SPARQL engine (RDF4J-compatible)                      |
        |  Reasoner: forward chaining -> implicit statements     |
        |  SHACL (ShaclSail) at commit    Connectors (Lucene ...)|
        |  Ontop virtual repos (SQL sources)                     |
        |  Repository storage: explicit + inferred + indexes     |
        +--------+---------------------------------------------+
   (EE) Raft cluster: leader + followers, snapshot replication,
        internal proxy (any node) / external proxy (leader URL)
   Control plane: licence file (all editions), users/roles, repo config
   Data plane: SPARQL read -> any node; writes -> leader, majority commit
```

## 5. Under-the-hood reconstruction

Engine internals are closed source; everything below is from the 11.4 documentation unless marked *hypothesis*.

**Data model.** RDF statements in repositories, named graphs, RDF-star; the engine is "compatible with the RDF4J framework", and SHACL is RDF4J's ShaclSail. [CLAIM-graphdb-10,18] Physical index layout, dictionary encoding and join algorithms: NOT PUBLICLY VERIFIED in the sources read.

**Reasoning pipeline.** Total materialisation: rules run at load/commit over explicit statements until fixpoint; rulesets are compiled to Java (hence a JDK is required); notation is close to Horst R-entailment with generalised RDF, axiomatic triples and consistency rules; premise ordering is by fewest unbound variables; `owl:sameAs` is optimised with equivalence-class representatives to avoid N^2 statements. [CLAIM-graphdb-07,09]

**Deletion (the interesting part).** No full derivation-dependency (track) data is stored because it "can take up to 90% of storage". Deletion is:

```
delete(S):
  mark S as to-delete
  C = forwardChain(rules, S)            # candidates: everything S may have derived
  for c in C:
      if not backwardDerivable(c, rules, store minus marked):   # re-prove from remaining data
          remove c
```

Schema statements fan out to many consequences so their deletion is slow; importing ontologies as read-only schema (`imports`) speeds deletes; a "schema transaction" is the expensive escape hatch. `sys:reinfer` drops all inferred statements and recomputes. [CLAIM-graphdb-08,09] This is a DRed-like delete-and-rederive without counts; the vendor table nonetheless advertises "efficient retraction of inferred statements on update". [CLAIM-graphdb-18]

**Query.** SPARQL 1.1 with documented deviations (FILTER inside UNION sees outer variables; `DELETE` without graph clause removes from all graphs, to be corrected in "12.0 or later"; two W3C test failures). Internal federation across repositories on one instance avoids HTTP. [CLAIM-graphdb-15] Cost model and plan formats: NOT PUBLICLY VERIFIED.

**Concurrency/cluster.** Raft extended so a write commits only after a majority commit locally; out-of-sync nodes recover via snapshot replication; followers serve reads and redirect writes; read consistency modes `None` (eventual, default) and `Last Committed`; storage doubles in clusters. 11.4.3 fixes a critical `last-committed` consistency issue and adds synchronised replication for concurrent writes. [CLAIM-graphdb-12,03,16]

**Security.** Roles in Workbench, per-repository AES-256-GCM encryption with an instance master key (11.4); named-graph/fact-level ACL: NOT PUBLICLY VERIFIED. [CLAIM-graphdb-03]

**Caching/memory.** Global page cache up to 40% of heap (max 40 GB), default buffer 200,000 statements, parallel import can retain more than 800 MB heap per repository. [CLAIM-graphdb-16]

## 6. Functional and non-functional requirements inferred

| ID | Requirement an EOIP RDF backend must meet to be comparable |
|---|---|
| FR-1 | Ruleset selection per repository with a documented fixpoint semantics; custom rules with consistency checks |
| FR-2 | Deletion must retract unsupported derived facts without full recompute |
| FR-3 | Validate shapes transactionally and return a structured report on violation |
| FR-4 | Read-scale-out with explicit consistency levels |
| NFR-1 | Java 21 (docs: not supported above 21); SSD, no NFS; at least 3 GB RAM for up to 50 M triples [CLAIM-graphdb-16] |
| NFR-2 | Licence file present even for Free; air-gap viability depends on offline licence validation (UNVERIFIED) |

## 7. Performance and resource model

Only vendor sizing guidance was found; no independent benchmark. Vendor sizing (docs): 150 M statements need about 5-6 GB heap, 9 GB RAM, 17 GB repository image; 30 B statements need about 128 GB heap, 159 GB RAM, 2,900 GB image; assumes roughly 3:1 statements to unique resources; "billions of explicit statements on desktop hardware, tens of billions on commodity servers" is a vendor claim (Unverified). [CLAIM-graphdb-16] Failure modes from docs: infinite blank-node generation from free head variables in rules; slow schema deletion; SHACL parallel validation "may cause deadlock, especially with NativeStore"; NFS update times for 10 M+ statements; write stall while a node joins the cluster. [CLAIM-graphdb-08,11,12,16] Benchmark publication terms (LDBC SPB/LUBM) for GraphDB were not checked (UNVERIFIED).

## 8. Strengths and use-case-specific advantages

| ID | Strength | Match or exceed |
|---|---|---|
| S1 | Total materialisation gives uniform-latency reads for RL/QL-style reasoning | Match for tractable fragment with an explanation ledger (exceeds: proof traces) |
| S2 | Standard rulesets plus user `.pie` rules with consistency rules | Match via Datalog/Soufflé-style rule packs under gitops |
| S3 | SHACL fires at commit with a report | Match in the mutation gateway (EOIP already has the hook, BL-28) |
| S4 | Raft cluster with proxy and tunable read consistency | Do not rebuild; integrate when customer owns EE |
| S5 | Ontop virtualisation bundled | Match by integrating Ontop directly |
| S6 | MCP prompts carrying pre-validated SPARQL templates | Match: EOIP's bounded query templates are the same idea (BL-08) |
| S7 | Per-repository encryption at rest | Match at deployment layer |

## 9. Limitations with root causes

| Type | Limitation | Root cause |
|---|---|---|
| Verified trade-off | Reasoning cost paid at write/delete time; schema deletion slow | Forward chaining without stored derivations (algorithmic dead-end for non-monotonic changes) |
| Verified limit | SHACL enable-at-creation only; shapes update by clear+reload; limited path types (no `*`, `+`, `?`); shapes not visible to SPARQL | ShaclSail integration rather than engine-native shapes |
| Verified limit | Cluster = EE only; majority loss blocks writes; node join pauses writes | Raft design and licensing |
| Licensing | Proprietary, core-based, licence file even for Free; "Standard" edition withdrawn | Commercial model |
| Ops overhead | JDK 21 pin, heap sizing, avoid NFS | JVM engine |
| Friction | OWL2-QL ruleset non-conformant in places; ontology import changes deletion cost | Rule-engine approximations |
| Hypothesis | Fact-level ACL absent so per-source permission filtering must live outside | No documented triple-level security (NOT PUBLICLY VERIFIED) |
| Outdated risk | Vendor docs mirrored across several URLs; 11.3.0 notes page appeared to contain 11.3.3 text | Documentation hygiene |

## 10. Deployment, licensing, redistribution, operational viability

Self-hosted Docker/VM; Free and Enterprise editions; EE also on AWS/Azure marketplaces. [CLAIM-graphdb-06] Free: single-core licence. EE core count: sources conflict ("two or more cores" versus "12 or more cores"); treat as UNVERIFIED until the order form is read. From GraphDB 11.0.0 every edition including Free requires a licence file requested by email. [CLAIM-graphdb-06] Whether Free permits commercial or embedded redistribution is NOT PUBLICLY VERIFIED (an aggregator calls it non-commercial: Third-party report, 0.3).

**Legal-review triggers:** proprietary EULA; core-based licensing; licence file at start-up (air-gap and white-label OEM need a vendor agreement); no redistribution of the binary inside EOIP. Existing EOIP policy (access only over SPARQL, never link or vendor) is the correct posture. Air-gap: engine runs locally; offline licence validation UNVERIFIED. One-node: viable (3 GB minimum).

## 11. Competitive delta against the EOIP verified baseline

| Area | EOIP | GraphDB | Delta |
|---|---|---|---|
| BL-06 RDF adapters (baseline: "Partial, SPARQL over HTTP") | **Correction from code read:** `FusekiGraphStore`/`GraphDBGraphStore` keep vertices and edges in `self._local_cache` (`rdf_backend.py:72-83`, `126-139`); `bulk_load` loops the same upserts (`:189`); `tombstone_vertex` deletes from the dict (`:206`); `ensure_schema` returns ACK without contact (`:66`); the only HTTP call is the ASK health probe (`:49-56`). `query_url`, `update_url`, `data_url` are set (`:40-42`) but never used; `username`/`password` are never sent. `GraphDBGraphStore` only rewrites the base URL to `/repositories/{repo}` (`:216-243`). [CLAIM-graphdb-19] | Real engine | Adapter is a stub, no data reaches GraphDB |
| SPARQL front door | `SparqlProtocolHandler._execute_sparql` ignores `rdf_backend` (`pass`) and returns three synthetic bindings `urn:eoip:entity:{var}_{i}` (`query/sparql_protocol.py:124-152`). [CLAIM-graphdb-20] | Real SPARQL | Conformance claims invalid until fixed |
| BL-29 SHACL | in-house subset, pySHACL not installed | ShaclSail, commit-time | Parity needs W3C suite |
| BL-30 OWL reasoning | subclass/disjoint/property chain only (`ontology/rdf.py:598`) | RL/QL + custom rules | Large deficit; INTEGRATE |
| BL-28/37 gateway, bitemporal | Implemented | None documented | EOIP ahead |
| BL-18/20 ACL, tenancy | Absent / contract only | Roles only documented | Neither solves per-fact ACL |
| BL-47 MCP | 18 read tools | MCP prompts and TTYG | Comparable idea |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

| STR-ID | Competitor | Strength | Evidence | Value to EOIP | Decision | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-graphdb-01 | GraphDB | Materialised RL/QL inference with fast reads | 07 | Fast impact queries over class hierarchies | integrate (optional backend) | Keep backend neutral; route `inferred=true` reads to RDF backend only when configured | Same answers as pySHACL/Jena oracle on a 100 k-triple fixture |
| STR-graphdb-02 | GraphDB | Commit-time SHACL with report | 10 | Block bad mutations | match | Mutation gateway runs pySHACL/Jena SHACL, returns report object | W3C SHACL Core test suite pass rate recorded |
| STR-graphdb-03 | GraphDB | MCP prompts with validated SPARQL templates | 03,14 | Safer NL to SPARQL | match | Expose typed query templates as MCP prompts | LLM template-selection accuracy vs free-form SPARQL on 50 questions |
| STR-graphdb-04 | GraphDB | Consistency modes in cluster | 12 | Predictable reads | reject (do not rebuild) | Document backend consistency per adapter | n/a |
| STR-graphdb-05 | GraphDB | Per-repository encryption keys | 03 | Tenant data-at-rest separation | integrate | Repo-per-tenant option for RDF backend | Tenant A key rotation leaves tenant B readable |

**INV-graphdb-01 — Reasoning cost lands on delete and schema change.** Target: GraphDB 11.4, owl2-rl, deletion of schema statements [CLAIM-graphdb-08]. Root cause: no stored derivations (*proven*, documented). Alternative: derivation ledger (support counts) for the tractable fragment, maintained in EOIP's mutation gateway; worse when derivation volume dwarfs base data (the vendor's 90% storage figure, Unverified) so the ledger must be bounded to selected predicates. Options: (1) quick: mark ontology read-only via `imports`, avoid schema edits online; (2) native: counting/DRed ledger for subclass, transitive and inverse rules with explanation traces; (3) long-term: tiered hybrid (materialise hot rules, rewrite cold). Select (2). Sketch: `edge(derived) {support: [rule_id, premise_ids], count}`; delete decrements counts, tombstones at zero, epistemic label `inferred`. POC: 1 M-edge synthetic org graph, 1,000 schema deletes; metric p95 delete latency within 2x of GraphDB on the same data and zero stale derived edges; baseline = GraphDB `owl2-rl`. Dependencies: epistemic plane (BL-40), revision vertices (BL-37). Failure cases: cycles in support (use well-founded counts), cross-tenant derivation (scope ledger per tenant). Defensibility: derivations double as explanation and evidence (CAP-24, CAP-38). Decision: **EXPERIMENT**. Seed hypothesis row "Stardog: tiered hybrid materialisation" is **partially validated**: GraphDB shows materialisation works, and shows its delete cost; the ledger addition is the new part.

**INV-graphdb-02 — SHACL lifecycle is repository-bound.** Root cause: ShaclSail wired at creation, update by clear+reload (*proven*). Option: shapes as versioned gitops artifacts applied by the gateway to any backend (native option; pairs with `ontology/gitops.py`). POC: shape change with rollback in one transaction on a 1 M-triple set, zero downtime. Defensibility: portability across HugeGraph/Neo4j/Neptune. Decision: **ADOPT** (BL-32 extension).

**INV-graphdb-03 — Edition and licence gating.** Root cause: licensing (*proven*). Option: RDF backend stays optional; default RDF engine is Apache 2.0 (Jena/Fuseki) with GraphDB as customer-licensed. Decision: **ADOPT** (already EOIP policy).

**INV-SELF-RDF-01 — EOIP RDF adapters and SPARQL endpoint are stubs.** Root cause: maturity (*proven* by code read). Option: implement HTTP SPARQL 1.1 client with auth, `/update`, Graph Store protocol; remove synthetic bindings or gate them behind `test_mode`. POC: run `graph/conformance.py` against Fuseki and GraphDB containers. Decision: **ADOPT (P0 for honesty of BL-06)**.

## 13. Per-capability decisions

| Capability | Decision | Reason |
|---|---|---|
| CAP-02 RDF/quad storage | INTEGRATE (optional, over SPARQL only) | Backend neutrality, licence |
| CAP-15 SPARQL | INTEGRATE | Real client missing today |
| CAP-22 incremental rule materialisation | EXPERIMENT (BUILD ledger) | INV-graphdb-01 |
| CAP-23 OWL profiles | INTEGRATE (Jena/RDF4J first) | GraphDB optional |
| CAP-10 SHACL | REUSE pySHACL/Jena, not GraphDB-bound | INV-graphdb-02 |
| CAP-24 explanation | BUILD | GraphDB stores no derivations |
| CAP-05 cluster | REJECT (rebuild) | Use customer's backend HA |
| CAP-59 MCP | REUSE pattern (prompts) | STR-graphdb-03 |
| CAP-21 virtualisation | INTEGRATE Ontop | See C04-ontop |
| CAP-77 licensing | DEFER to legal | Triggers listed |

## 14. Concrete tests, proof-of-concept, and acceptance conditions

All PROPOSED (nothing run). T1: real round-trip — upsert 10 k vertices via adapter, restart EOIP, read back from the GraphDB repository (fails today). T2: SPARQL endpoint returns data from a live repository, not `urn:eoip:entity:*_n`. T3: W3C SPARQL 1.1 and SHACL Core suites against Fuseki and GraphDB, record deviations vs [CLAIM-graphdb-15]. T4: delete-latency POC for INV-graphdb-01. T5: air-gap start with offline licence (does 11.4 start with no network?). T6: repo-per-tenant isolation with key rotation. Acceptance: T1/T2 green before BL-06 may be reported Implemented.

## 15. Risks, trade-offs, and open research questions

Risks: licence terms for Free in a white-label product (OEM agreement needed); pace of GraphDB major changes (12.0 pending, deprecations); dependence on vendor docs mirrors. Open: exact EE core thresholds; index layout and cost model; TTYG local-model support; fact-level ACL; behaviour of `sameAs` optimisation with EOIP identity merges; benchmark publication terms.

---

## Appendix A — Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | Graphwise, versions, proprietary |
| D2 | 2 | Workloads table |
| D3 | 4 | Diagram |
| D4 | 5 | Storage layout NOT PUBLICLY VERIFIED |
| D5 | 3, 5 | RDF-star yes, SHACL, OWL profiles |
| D6 | 5 | SPARQL 1.1 with deviations; planner unverified |
| D7 | 5, 12 | Forward chaining, deletion algorithm |
| D8 | 5, 7 | Raft cluster, no sharding documented |
| D9 | 3 | Connectors, Ontop, Kafka |
| D10 | N/A | No ER; sameAs optimisation only |
| D11 | N/A | No temporal model documented |
| D12 | N/A | No graph ML found |
| D13 | 3, 5 | TTYG, MCP prompts, embeddings |
| D14 | 3 | TTYG; accuracy not measured |
| D15 | 3 | Workbench; no ontology governance workflow |
| D16 | 3 | Workbench, Geo tab |
| D17 | 3 | RDF4J API, plugin API |
| D18 | 5, 9 | Roles, encryption, CVE history |
| D19 | 3, 13 | Repo-per-tenant hypothesis |
| D20 | 7 | Vendor sizing only |
| D21 | 10 | Editions and licence |
| D22 | 3 | RDF export; LPG loss not tested |
| D23 | N/A | No patent research done |
| D24 | App C | Sources mostly vendor docs |

## Appendix B — Capability mapping

| CAP-ID | This technology | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-02 | native | 18 | BL-06 stub | INTEGRATE | P2 |
| CAP-10 | native (ShaclSail) | 10,11 | BL-29 Partial | REUSE other | P1 |
| CAP-15 | native | 15 | BL-06/09 stub | INTEGRATE | P1 |
| CAP-21 | plugin (Ontop) | 17 | BL-51 Partial | INTEGRATE | P2 |
| CAP-22 | native, non-incremental delete | 07,08 | Absent | EXPERIMENT | P1 |
| CAP-23 | native RL/QL | 07 | BL-30 Partial | INTEGRATE | P2 |
| CAP-24 | absent | 08 | Absent | BUILD | P1 |
| CAP-05 | enterprise-only | 12 | n/a | REJECT | P3 |
| CAP-59 | native (prompts) | 03 | BL-47 | REUSE | P2 |
| CAP-77 | proprietary | 06 | BL-22 | DEFER | P2 |

## Appendix C — Evidence records

| CLAIM-ID | Product/version/date | Exact claim | Class. | Source | Pub./access | Confidence | Contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-graphdb-01 | Graphwise 2024-10 | SWC and Ontotext merged into Graphwise; GraphDB and PoolParty brands continue | Third-party report | intelligentcio.com "Semantic Web Company and Ontotext merge…" and graphwise.ai FAQ | 2024-10-23 / 2026-10-26 | 0.8 press release | none |
| CLAIM-graphdb-02 | Graphwise | Oakley Capital majority stake | Third-party report | beri.net article (URL via search) | n/d / 2026-10-26 | 0.35 aggregator | no primary |
| CLAIM-graphdb-03 | 11.4.0–11.4.3 | Dates 06-16, 07-09, 07-20, 08-06; Geo tab, MCP prompts, AES-256-GCM per-repo encryption, Assistants API dropped, Azure OpenAI embeddings, Solr connector deprecated; 11.4.3 synchronised replication and last-committed fix | Officially documented | graphdb.ontotext.com/documentation/11.4/release-notes.html | 2026-08 / 2026-10-26 | 0.85 | none |
| CLAIM-graphdb-04 | 11.3.2, 11.3.3 | Critical XXE, Avatica RCE, OCSP issues fixed | Officially documented | help.graphwise.ai GraphDB 11.3.2/11.3.3 release notes | 2026-04 / 2026-10-26 | 0.75 via search digest | 11.3.0 page mirrored 11.3.3 text |
| CLAIM-graphdb-05 | 11.4 | Editions Free and Enterprise; Standard no longer offered | Officially documented | graphdb.ontotext.com/documentation/11.4/index.html | n/d / 2026-10-26 | 0.8 | older 2022 text lists Standard |
| CLAIM-graphdb-06 | 11.x | Free single-core; EE licensed per cores; all editions need licence since 11.0.0; EE on AWS/Azure | Officially documented | graphwise.ai GraphDB comparison page | n/d / 2026-10-26 | 0.7 (core count conflicts: "two or more" vs "12 or more") | see text |
| CLAIM-graphdb-07 | 11.4 | Forward chaining total materialisation; rulesets empty, rdfs, rdfsplus, owl-horst, owl-max, owl2-ql, owl2-rl; default RDFS-Plus optimised; sameAs optimisation | Officially documented | graphdb.ontotext.com/documentation/11.4/reasoning.html | n/d / 2026-10-26 | 0.85 | none |
| CLAIM-graphdb-08 | 11.4 | No full track data (up to 90% storage); delete = mark, forward chain, backward check; schema deletes slow; schema transactions | Officially documented | same reasoning page | n/d / 2026-10-26 | 0.85 | vendor table says "efficient retraction" |
| CLAIM-graphdb-09 | 11.4 | `.pie` custom rules compiled to Java (JDK needed); consistency rules, off by default; `sys:reinfer` | Officially documented | same reasoning page | n/d / 2026-10-26 | 0.85 | none |
| CLAIM-graphdb-10 | 11.4 | SHACL via RDF4J ShaclSail, enabled at repo creation, validated at commit | Officially documented | graphdb.ontotext.com/documentation/11.4/shacl-validation.html | n/d / 2026-10-26 | 0.85 | none |
| CLAIM-graphdb-11 | 11.4 | Path limits, parallel validation deadlock warning, shape update by clear+reload, SPARQL constraints supported | Officially documented | same SHACL page | n/d / 2026-10-26 | 0.85 | none |
| CLAIM-graphdb-12 | 11.4 | Cluster is EE; Raft with majority commit; proxies; consistency None/Last Committed; quorum loss stops writes | Officially documented | graphdb.ontotext.com/documentation/11.4/cluster-basics.html | n/d / 2026-10-26 | 0.85 | none |
| CLAIM-graphdb-13 | 11.4 | Lucene and ChatGPT connectors all editions; Solr, Elasticsearch, OpenSearch, Kafka EE only | Officially documented | docs index page | n/d / 2026-10-26 | 0.75 | vendor table lists MongoDB too |
| CLAIM-graphdb-14 | GraphDB 11.0 | TTYG with several LLMs incl. local models, entity linking, MCP | Third-party report | HPCwire 2025-07-08 | 2025-07-08 / 2026-10-26 | 0.5 | official TTYG page 404 |
| CLAIM-graphdb-15 | 11.4 | SPARQL 1.1 mostly conformant; two W3C test failures; DELETE-without-graph deviation fixed in 12.0 or later | Officially documented | .../sparql-compliance.html | n/d / 2026-10-26 | 0.85 | none |
| CLAIM-graphdb-16 | 11.4 | Java 21 JDK; 3 GB / 50 M triples; sizing examples; avoid NFS; cache 40% | Officially documented | .../requirements.html | n/d / 2026-10-26 | 0.85 | sizing is vendor guidance |
| CLAIM-graphdb-17 | 9.5 | Ontop-based virtual access to RDBMS in all editions | Third-party report | PR Newswire GraphDB 9.5, Dec 2020 | 2020-12 / 2026-10-26 | 0.6 | current docs page not fetched |
| CLAIM-graphdb-18 | 11.x | Vendor table: RDF-star/SPARQL-star, plugin API, GeoSPARQL, "efficient retraction", RDF4J compatibility | Officially documented | graphwise.ai/?p=166320 | n/d / 2026-10-26 | 0.65 (edition columns unreadable) | none |
| CLAIM-graphdb-19 | EOIP dev_local | Adapter stores in `_local_cache`; HTTP only for health ASK | Observed in source code | `packages/eoip/graph/rdf_backend.py:25-243` | working tree / 2026-10-26 | 0.95 | BL-06 says "SPARQL over HTTP" |
| CLAIM-graphdb-20 | EOIP dev_local | `_execute_sparql` ignores backend and returns synthetic bindings | Observed in source code | `packages/eoip/query/sparql_protocol.py:124-152` | working tree / 2026-10-26 | 0.95 | none |

## Appendix D — Assumptions

1. Access date is 2026-10-26, not the brief's 2026-10-18, because pages fetched carry later dates.
2. "Latest" = highest version seen in the 11.4 docs; no 12.0 found.
3. `.ontotext.com` and `.graphwise.ai` docs treated as the same vendor source.
4. No licence text was read; all licence statements are from vendor pages.
5. Proposed ID `INV-SELF-RDF-01` for the coordinator's self-inversion register.
6. EOIP baseline BL-06 should be restated as "Stub / local cache; live-unverified" (flag to coordinator).
7. The file was overwritten by a placeholder once during this run (another process) and rewritten; re-check before consolidation.
