# Cohort 02: RDF stores, SPARQL engines and inference engines

| Field | Value |
|---|---|
| Cohort ID | COH-02-RDF |
| Workload class | Optional RDF/OWL/SPARQL/SHACL tier: standards interchange, ontology validation and reasoning, SPARQL access to the EOIP graph (CAP-02, 09, 10, 11, 15, 21..25, 45..47) |
| Date | 2026-10-26 |
| EOIP reference | BL-IDs at `ad9937b` ([01-SYSTEM-BASELINE.md](../01-SYSTEM-BASELINE.md)); status at HEAD `896e06d` ([01a-BASELINE-DELTA-HEAD.md](../01a-BASELINE-DELTA-HEAD.md)) wins where they differ |
| Reference columns | HugeGraph, Neo4j, Neptune (RDF mode), EOIP @HEAD |
| Stores (10) | [Stardog](../04-COMPETITOR-DEEP-DIVES/C02-stardog.md), [Ontotext/Graphwise GraphDB](../04-COMPETITOR-DEEP-DIVES/C02-ontotext-graphdb.md), [Apache Jena](../04-COMPETITOR-DEEP-DIVES/C02-apache-jena.md), [AllegroGraph](../04-COMPETITOR-DEEP-DIVES/C02-allegrograph.md), [Eclipse RDF4J](../04-COMPETITOR-DEEP-DIVES/C02-eclipse-rdf4j.md), [OpenLink Virtuoso](../04-COMPETITOR-DEEP-DIVES/C02-openlink-virtuoso.md), [RDFox](../04-COMPETITOR-DEEP-DIVES/C02-rdfox.md), [Oxigraph](../04-COMPETITOR-DEEP-DIVES/C02-oxigraph.md), [QLever](../04-COMPETITOR-DEEP-DIVES/C02-qlever.md), [Anzo / Graph Studio](../04-COMPETITOR-DEEP-DIVES/C02-anzo.md) |
| Inference and validation (2) | [OWL reasoners](../04-COMPETITOR-DEEP-DIVES/C03-owl-reasoners.md) (ELK, HermiT, Openllet, Konclude, FaCT++), [pySHACL](../04-COMPETITOR-DEEP-DIVES/C03-pyshacl.md) |
| Tier C (context) | [C02-tier-c-records-V16](../04-COMPETITOR-DEEP-DIVES/C02-tier-c-records-V16.md): Blazegraph, MillenniumDB, Corese, HDT, Comunica, Nemo, VLog, Soufflé. [C02-tier-c-records](../04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md) has no CLAIM records and is not used |

CLAIM shorthand: cell suffixes take the prefix of the column. SD `CLAIM-stardog-`, GD `CLAIM-graphdb-`, AG `CLAIM-allegrograph-`, RX `CLAIM-rdfox-`, AZ `CLAIM-anzo-`, JN `CLAIM-jena-`, R4 `CLAIM-eclipse-rdf4j-`, OX `CLAIM-oxigraph-`, QL `CLAIM-qlever-`, VT `CLAIM-openlink-virtuoso-`, OWLR `CLAIM-owlr-`, PS `CLAIM-pyshacl-`, N4 `CLAIM-neo4j-`, NP `CLAIM-amazon-neptune-`. "§n" is a deep-dive section without a CLAIM row.

## 1. Workload class and comparison basis

**Workload.** Per constraint 7 of §4.3, RDF/OWL/SPARQL/SHACL services are optional modules adopted on demonstrated value. This cohort asks which RDF stores can serve as (a) an optional SPARQL backend behind `GraphStore`, (b) an embedded sidecar for validation and reasoning, and (c) a reference for reasoning and governance behaviour.

**Why comparable.** Every member speaks RDF or consumes RDF/OWL/SHACL artefacts, and EOIP reaches them over SPARQL 1.1 (BL-06) or as a library or CLI.

**Excluded.** Property-graph engines (cohort 01, except that Neptune's RDF mode is the same engine as the cohort 01 column [NP-26]). Ontology authoring and governance tools (cohort 03). Ontop is researched under C04 and is only referenced for virtualisation.

## 2. Capability comparison

### 2.1 Commercial platforms

| CAP | Stardog (SD) | GraphDB (GD) | AllegroGraph (AG) | RDFox (RX) | Anzo (AZ) |
|---|---|---|---|---|---|
| CAP-02/15 RDF + SPARQL | native, SPARQL 1.1, Mastiff LSM store -12, -15 | native, "mostly conforms", 2 W3C tests fail -15 | native -03 | native, plus federated SPARQL -02, -05 | native in-memory MPP, SPARQL 1.1 -05, -08 |
| CAP-11 RDF-star / 1.2 | unknown | RDF-star present; 1.2 triple terms not mentioned -18 | RDF-star 8.0+ -03; 1.2 none found | 1.2 not found (unknown) | legacy RDF-star LPG -08; 1.2 not found |
| CAP-10 SHACL | Core + SPARQL, transactional guard -13 | Core + SPARQL; enable at repo creation only -10, -11 | present -03 | present -02 | listed, depth unverified -05 |
| CAP-22 materialisation | absent by design, query-time only -06 | native forward chaining; deletes costly -07, -08 | native RDFS++ dynamic, OWL 2 RL precompute -03 | native, incremental add and delete -03 | RDFS+ in legacy docs -08 |
| CAP-23 OWL profiles | RDFS, QL, RL, EL, SL; DL only in memory -07, -11 | RDFS to OWL2-QL/RL -07 | OWL 2 RL -03 | OWL 2 RL by best-effort translation -03 | unknown |
| CAP-24 explanation | partial, CLI `reasoning explain` -11 | absent -08 | unknown | native shortest proof -03 | unknown |
| CAP-21 virtualisation | native virtual graphs -12 | plugin, Ontop repositories -17 | partial, FedShard -03 | federated SPARQL -05 | native -05 |
| CAP-45/46 access control | RBAC; LDAP enterprise-only -03, -16; no source-ACL stated | no fact-level ACL documented (§9) | triple-level security filters, shared with vectors -02, -03 | per-graph roles, details unread -06 | RBAC; ABAC experimental -06 |
| CAP-47 tenancy | database or named schema per tenant -10 | repository per tenant (hypothesis, §3) | unknown | unknown | unknown |
| CAP-05 scale-out | full-replica HA; writes slow as nodes grow -14 | Raft cluster, enterprise-only -12 | FedShard sharding, multi-master -03 | HA replication, edition unknown -02 | native MPP -07 |
| CAP-50 air-gap | server viable; Voicebox needs cloud LLM or untested proxy -20 | engine local; offline licence unverified (§10) | likely; licence server unverified | plausible; offline renewal unverified | unknown |

### 2.2 Open and embeddable stores

| CAP | Jena/Fuseki (JN) | RDF4J (R4) | Oxigraph (OX) | QLever (QL) | Virtuoso OSS (VT) |
|---|---|---|---|---|---|
| CAP-02/15 | native TDB2, SPARQL 1.1 -04, -05 | native SPARQL 1.1 and 1.2 -02 | "nearly fully conformant" 1.1 -01 | full SPARQL 1.1 incl. Update -01, -02 | native -02 |
| CAP-11 RDF 1.2 | partial: preview since 5.4; 6.x unverified -08 | present in 6.0.0 -02 | preliminary, `rdf-12` Cargo flag -01, -03 | not found | not found |
| CAP-10 SHACL | Core + SPARQL -07 | extension -01 | absent | absent | not found |
| CAP-22/23 reasoning | partial: RETE forward, tabled backward, incomplete OWL -06 | partial: RDFS inferencer -01 | absent | absent | enterprise-only custom rules -02 |
| CAP-21 federation | not listed | FedX -02 | partial, `SERVICE` -01 | not listed | RDF Views; external sources commercial-only -02 |
| CAP-45/46/47 | Shiro, graph-level access module, no tenant model -04 | not found | absent | update token only -05 | ABAC commercial-only -02 |
| CAP-04/05 footprint and scale | single node, no HA; embedded -03, -05 | embedded JVM; Native store about 100M triples guidance -01 | single static binary; one read-write process -06 | single node scale-up; vendor "hundreds of billions" -01 | commercial cluster; 20B-triple load reported -04 |

### 2.3 Reference columns and EOIP

| CAP | HugeGraph | Neo4j (N4) | Neptune (NP) | EOIP @HEAD |
|---|---|---|---|---|
| CAP-02/15 | absent: no SPARQL or RDF module (CLAIM-apache-hugegraph-09 §3, reasoned) | n10s Labs import/export only -31 | native SPARQL 1.1; RDF data not queryable from Gremlin or openCypher -06, -26 | Fuseki and GraphDB adapters Implemented, live-unverified (BL-06). SPARQL backends exist, not mounted in `apps/api` (BL-06a) |
| CAP-10 SHACL | absent | Labs n10s, partial -31 | absent | Partial: in-house engine rejects unsupported components; pySHACL adapter; differential test passes; W3C suite not run (BL-29, U-07) |
| CAP-22/23 | absent | no native reasoner; n10s query-time hierarchy -32 | no reasoner documented -06 | Partial: native RDFS-subset reasoner; Openllet/HermiT/Jena adapters return canned OK; no caller (BL-30) |
| CAP-24 | absent | absent | absent | Absent for rules (BL-30; `HybridReasoningEngine` has justification sets, no caller) |
| CAP-29 R2RML | n/a | n/a | n/a | CML implemented; R2RML importer is 76 lines, not conformance-tested (BL-33, NB-09) |
| CAP-47 tenancy | graph or space (cohort 01) | EE database per tenant | one graph per cluster | Partial; RDF adapter does not use the tenant graph IRI (BL-20) |

### 2.4 Reasoners and validators

| Member | Scope | Licence | Evidence |
|---|---|---|---|
| ELK 0.6.0 | OWL 2 EL, polynomial, incremental, explanations | Apache-2.0 | OWLR-01 |
| HermiT 1.3.8 / 1.4.5.519 | OWL 2 DL, DL-safe rules | LGPL (older text says GPL) | OWLR-02, -03 |
| Openllet 2.6.5 | OWL 2 DL, explanations; Maven latest 2019-09-27 | AGPL-3.0 dual | OWLR-04, -05 |
| Konclude v0.7.0-1138 | OWL 2 DL, parallel tableau | LGPLv3 | OWLR-06 |
| FaCT++ | OWL 2 DL | LGPL unconfirmed | OWLR-07 (confidence 0.35) |
| pySHACL 0.40.1 | SHACL Core, SPARQL, AF rules, optional JS; RDF only; no incremental validation | Apache-2.0 | PS-03, -05, -08 |

## 3. Reasoning strategies and incremental maintenance

| Strategy | Members | Behaviour on change | Evidence |
|---|---|---|---|
| Query-time rewriting | Stardog | Schema change needs no reload; cost lands on each query; latency grows with hierarchy depth; out-of-profile axioms silently ignored | SD-06, -07, -11 |
| Forward-chaining materialisation | GraphDB, AllegroGraph (OWL 2 RL), Jena (RETE) | Cost at write and delete time; GraphDB schema deletion slow because derivations are not stored | GD-07, -08; AG-03; JN-06 |
| Incremental materialisation (add and delete) | RDFox | Maintains data and rule changes; documented phases and proofs | RX-03 |
| Per-repository choice | AllegroGraph (RDFS++ dynamic vs OWL 2 RL materialised) | Operator picks; materialiser blow-up on volatile data per vendor guidance | AG-03, §7 |
| Tabled backward / hybrid | Jena | Tables flushed on update | JN-06, §9 |
| Profile classifier | ELK | Incremental EL classification | OWLR-01 |
| Open Datalog engines | Nemo (v0.10.1), Soufflé, VLog | Nemo documents no incremental deletion in sources read; Soufflé is batch | CLAIM-nemo-01, -02; CLAIM-souffle-01 |
| EOIP | in-house subset reasoner | no incremental maintenance; adapters scaffolding | BL-30 |

## 4. Operational and licensing comparison

| Member | Licence class | OEM / redistribution | Air-gap and sidecar fit | Maintenance |
|---|---|---|---|---|
| Stardog | proprietary; Free is evaluation-only EULA although pricing page says commercial use (SD-16, -17) | not permitted; evaluating "to compete" prohibited, bears on benchmark publication | server viable; Voicebox sends results to cloud LLM providers (SD-18..20) | 12.2.0 (2026-10-14) (SD-01) |
| GraphDB | proprietary; licence file for every edition since 11.0.0 (GD-06) | needs vendor agreement; EE core count sources conflict | engine local; offline licence unverified | 11.4.3 (2026-08-06); Graphwise merger (GD-03) |
| AllegroGraph | proprietary; edition pages disagree (AG-05) | OEM terms not public | likely; Ollama supported (AG-04) | 9.0 (2026-05-05) (AG-01) |
| RDFox | proprietary; evaluation licence forbids commercial use and benchmark publication without approval (RX-04) | not public | plausible | 7.7 (2026-09-29); Samsung acquisition (RX-01, RX-05) |
| Anzo | proprietary; Siemens-owned (AZ-01, AZ-02) | not public | unknown | Graph Studio 2026.0 (AZ-06) |
| Jena / Fuseki | Apache-2.0 (JN-02) | permissive | Java 21 floor in 6.x; compose service | 6.2.0 (2026-08-01) |
| RDF4J | EDL 1.0 = BSD-3 (R4-03) | permissive | embedded JVM, Java 25 floor | 6.0.0 (2026-07-02) |
| Oxigraph | Apache-2.0 OR MIT (OX-01) | permissive | single binary, Python and WASM bindings; pre-1.0 | 0.5.13 (2026-10-22) |
| QLever | Apache-2.0; one catalogue says MIT (QL-01, -02) | permissive | binary or container; offline index builds | v0.6.0 |
| Virtuoso | GPLv2 open source; HA, inference, ABAC, encryption commercial-only (VT-02, -03) | GPL: customer-installed only | self-hosted | 7.2.17 (2026-05-07) |
| ELK / pySHACL | Apache-2.0 | permissive | JVM sidecar / in-process Python extra | ELK 0.6.0 (2024-05); pySHACL 0.40.1 (2026-07-28) |
| HermiT, Konclude, FaCT++, Openllet | LGPL, LGPLv3, LGPL?, AGPL-3.0 | linking is a legal-review trigger | external process only | HermiT Maven 2020; Openllet Maven 2019 |
| Blazegraph (Tier C) | GPL-2.0; archived 2026-03-23 (CLAIM-blazegraph-01) | blocked | n/a | being replaced at Wikimedia (CLAIM-blazegraph-02) |

## 5. Performance and scale evidence

No two figures share workload and hardware; no ranking follows.

| Source | Figure | Class |
|---|---|---|
| RDFox, ISWC 2015 (RX-08) | 128 cores, 4 TB RAM: up to 87x speed-up, 9.2B triples, 6.1M triples/s | peer-reviewed, atypical hardware, 2015 |
| RDFox product page (RX-02) | 2-3M inferred facts/s, no workload | vendor, unverified |
| QLever (QL-01, -04) | "hundreds of billions", ">1 trillion" demo; Wikidata 17B and UniProt 94B triples cited | vendor / documentation, unreproduced |
| Virtuoso via Wikimedia (VT-04) | able to load 20B triples; heavier tuning | third-party report, confidence 0.6 |
| Oxigraph via Wikimedia (OX-05) | could not load Wikidata (version unstated) | third-party report |
| GraphDB sizing (GD §7) | 150M statements about 9 GB RAM; 30B about 159 GB RAM | vendor sizing guidance |
| Jena (JN-05), RDF4J (R4-01) | "hundreds of millions"; Native store about 100M triples | project guidance, no hardware |
| Stardog (SD-15) | 7.0 write throughput "10x-20x" | vendor, unspecified |
| Anzo (AZ-05) | "tens of billions", trillion-triple benchmark | vendor, confidence 0.2 |
| pySHACL (PS-06) | benchmark script, no published numbers | none |

EOIP has no RDF performance measurement; the LPG-over-RDF mapping's semantic loss is unmeasured (BL-06). BM-01..06 remain PROPOSED.

## 6. Findings

1. **Only RDFox documents incremental maintenance for both inserts and deletes.** GraphDB pays at delete time (GD-08), Stardog does not materialise (SD-06), Jena discards tabling on update (JN §9). Falsified by another member documenting incremental delete maintenance.
2. **Only AllegroGraph documents triple-level security filters (AG-03); tenancy is only database- or named-schema-per-tenant (Stardog, SD-10).** Jena has graph-level access only (JN-04), QLever an update token (QL-05), Oxigraph nothing (OX-01), GraphDB no documented fact-level ACL (GD §9). EOIP must keep ACL and tenant enforcement above the store (BL-18, BL-20).
3. **Every commercial store blocks bundling.** Stardog, GraphDB, AllegroGraph, RDFox and Anzo are proprietary, Virtuoso OSS is GPLv2. Only Jena, RDF4J, Oxigraph and QLever are permissive.
4. **Of the DL reasoners only ELK is permissive, and it covers EL only.** Openllet is AGPL-3.0 with a 2019 Maven release, HermiT and Konclude are LGPL (OWLR-02..06). EOIP's Openllet, HermiT and Jena adapters at HEAD return canned OK results and must not be cited as capability (BL-30).
5. **SHACL integration differs more than SHACL coverage.** GraphDB binds shapes at repository creation and updates by clear and reload (GD-10, -11); Stardog guards transactions (SD-13); pySHACL has two known W3C-suite failures and no incremental validation (PS-08). EOIP's pySHACL differential test passes at HEAD but the W3C suite is unrun (BL-29, U-07). Falsified by an EOIP W3C run.
6. **RDF 1.2 and SPARQL 1.2 are still moving.** RDF4J 6.0.0 ships them (R4-02), Oxigraph behind a flag (OX-03), Jena as preview (JN-08). Concepts is a Candidate Recommendation Snapshot dated 2026-04-07 and SPARQL 1.2 Query a Working Draft (JN-08, OX-07). The two deep dives give different latest-draft dates (2026-10-25 vs 2026-03-23). Stardog, GraphDB, RDFox and QLever claim none in sources read.
7. **Stardog's NL layer conflicts with the egress default.** Voicebox's documented providers are cloud APIs and results go to the model for summarising (SD-18..20). EOIP's gateway default S0 and local-model path (BL-45, BL-16) are an advantage, not parity.
8. **Exit cost of store-specific services is real.** Wikimedia is replacing Blazegraph with QLever, endpoints 2026-11-01, shutdown targeted 2027-06-30, and Blazegraph-only SPARQL services will not migrate (QL-03, CLAIM-blazegraph-02). This supports a SPARQL-1.1-only adapter contract.
9. **Deep-dive statements about EOIP's RDF adapters are stale.** C02 files say the adapters are stubs or a cache (INV-SELF-RDF-01, "BL-06 stub"). At HEAD every `GraphStore` operation runs as SPARQL 1.1 over HTTP with no local cache (BL-06). The remaining gap is unmounted SPARQL protocol handling (BL-06a) and unmeasured semantic loss.
10. **Independent evidence is thin.** No independent reproducible benchmark exists for Stardog, GraphDB, AllegroGraph, Anzo or QLever in the deep dives (SD-15, GD §7, AG §7, AZ-05, QL-01).

## 7. Implications for EOIP

| CAP | Parity needed (STR) | Exploitable weakness (INV) | Decision | Candidate gap statement |
|---|---|---|---|---|
| CAP-02/15 RDF sidecar | STR-jena-01, STR-oxigraph-01, STR-qlever-01 | INV-jena-02, INV-oxigraph-01, INV-qlever-01 | INTEGRATE Fuseki/TDB2 as default optional store; EXPERIMENT Oxigraph (embedded) and QLever (read tier); Stardog, GraphDB customer-supplied only | Interoperability: SPARQL handler built, not mounted (BL-06a); mapping loss unmeasured |
| CAP-10 SHACL | STR-graphdb-02, STR-stardog-03, STR-jena-02, STR-pyshacl-01 | INV-graphdb-02, INV-pyshacl-01 | REUSE pySHACL as oracle and optional engine; BUILD LPG-native subset kept | Quality: W3C SHACL suite not run; pySHACL not in runtime lock |
| CAP-22 materialisation | STR-rdfox-01, STR-graphdb-01, STR-stardog-01 | INV-stardog-01, INV-graphdb-01, INV-jena-01, INV-rdfox-01 | EXPERIMENT Nemo as batch worker; BUILD bounded incremental subset | Missing: no Datalog engine (BL-30) |
| CAP-23 OWL | STR-owlr-01 | INV-owlr-01 | INTEGRATE ELK as optional JVM sidecar; REJECT embedding copyleft DL reasoners | Partial: adapter layer is scaffolding; ELK available upstream / not integrated |
| CAP-24 explanation | STR-rdfox-02, STR-owlr-02 | INV-stardog-03 | BUILD (rule id plus premise ids, ACL-checked) | Missing for rules |
| CAP-21 virtualisation | STR-stardog-02, STR-openlink-virtuoso-01 | INV-openlink-virtuoso-01 | INTEGRATE Ontop (C04); finish BL-51 | Partial (BL-51) |
| CAP-46/47 | STR-allegrograph-01, STR-graphdb-05, STR-anzo-02 | INV-jena-02, INV-qlever-01 | BUILD above the store; tenant graph IRI available upstream / not integrated in `rdf_backend` | Security (P0): BL-18, BL-20 |
| CAP-58/60 | STR-stardog-04, STR-graphdb-03 | INV-stardog-02 | EXPERIMENT typed query templates and abstention | Competitive deficit: no audit log of generated queries |
| CAP-11 RDF 1.2 | STR-eclipse-rdf4j-02 | INV-jena-03, INV-eclipse-rdf4j-01 | DEFER; EXPERIMENT behind a flag | Research gap while standards move |
| CAP-77 licence gate | n/a | INV-graphdb-03, INV-openlink-virtuoso-01 | BUILD SBOM licence gate | Operability: `compliance/sbom.py` library-only (NB-14) |

## 8. Open questions

1. Does the EOIP Fuseki adapter pass round-trip fidelity and the live corpus against Fuseki 6.2 and GraphDB 11.4 (BL-06; live cases skipped)?
2. What are the W3C SHACL Core pass rates for the in-house validator and pySHACL (U-07)?
3. Is RDFox available to third parties after the Samsung acquisition, and on what OEM terms (RX-01)?
4. Does Nemo support incremental deletion, and can it run per tenant (CLAIM-nemo-02)?
5. Is QLever licensed Apache-2.0 or MIT (QL-02)?
6. What does Voicebox send to the LLM, and can a local OpenAI-compatible endpoint be supported (SD-20)?
7. Will the SPARQL protocol handler be mounted, and with what ACL (U-14)?
