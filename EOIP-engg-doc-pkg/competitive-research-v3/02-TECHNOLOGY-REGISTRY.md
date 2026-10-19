# 02 — Technology Registry

| Field | Value |
|---|---|
| Document | 02-TECHNOLOGY-REGISTRY.md (Master Prompt v3.0 Deliverable Package) |
| Total Items | 329 entries fully deduplicated across 20 categories |
| Tier Distribution | 44 Tier A (Full Reconstruction), 145 Tier B (Profile/Architecture), 140 Tier C (Inventory/Relevance) |
| Verification Cutoff | 2026-10-18 UTC |
| Machine-Readable Version | `02-technology-registry.json` |

---

## 1. Registry Census by Category

| Category | Name | Count | Tier A | Tier B | Tier C |
|---|---|---|---|---|---|
| C01 | Property-graph, multi-model, distributed, and embedded graph engines | 31 | 7 | 13 | 11 |
| C02 | RDF stores, semantic database engines, and inference engines | 18 | 3 | 7 | 8 |
| C03 | Ontology, taxonomy, vocabulary, and semantic-governance engineering | 22 | 4 | 7 | 11 |
| C04 | Semantic ETL, OBDA / virtualization, mapping, schema inference, ontology alignment, and entity resolution | 16 | 4 | 8 | 4 |
| C05 | Knowledge extraction from unstructured content | 11 | 0 | 8 | 3 |
| C06 | Metadata catalogs, data governance, and lineage-aware enterprise context graphs | 16 | 0 | 7 | 9 |
| C07 | Enterprise work graphs, operational ontologies, and organization-brain platforms | 14 | 6 | 6 | 2 |
| C08 | GraphRAG, LLM integration, organizational memory, and agent context | 34 | 10 | 8 | 16 |
| C09 | Agent orchestration, tool protocols, and local model serving | 11 | 2 | 9 | 0 |
| C10 | Vector, full-text, and hybrid search engines | 11 | 3 | 5 | 3 |
| C11 | Graph ML, GNNs, graph transformers, and neuro-symbolic AI | 14 | 1 | 4 | 9 |
| C12 | Graph processing, algorithms, and large-scale computation | 10 | 1 | 5 | 4 |
| C13 | Temporal, event-sourced, versioned, provenance, and lineage infrastructure | 11 | 0 | 6 | 5 |
| C14 | Enterprise acquisition, change data capture, streaming, and workflow | 11 | 0 | 5 | 6 |
| C15 | Code graphs, repository intelligence, software catalogs, and code RAG | 26 | 3 | 13 | 10 |
| C16 | Graph visualization, exploration, and UI toolkits | 20 | 0 | 8 | 12 |
| C17 | Research, scientific literature, and personal knowledge mapping | 11 | 0 | 4 | 7 |
| C18 | Interchange, query, ontology, and interoperability standards | 19 | 0 | 9 | 10 |
| C19 | Security, policy, privacy, observability, and operational tooling | 9 | 0 | 8 | 1 |
| C20 | Benchmarks, workloads, and evaluators | 14 | 0 | 5 | 9 |

---

## 2. Complete Technology Census

| ID | Technology Name | Category | Tier | Status | License | Air-Gap | Decision Summary | Deep Dive / Reference |
|---|---|---|---|---|---|---|---|---|
| `T-C01-apache-hugegraph` | **Apache HugeGraph (Server, Hubble, Loader, Computer, Vermeer, HugeGraph-AI, HugeGraph-ML, storage adapters)** | C01 | A | `active` | Apache-2.0 | yes | REUSE reference primary backend; push do | [`04-COMPETITOR-DEEP-DIVES/C01-apache-hugegraph.md`](04-COMPETITOR-DEEP-DIVES/C01-apache-hugegraph.md) |
| `T-C01-neo4j` | **Neo4j (Community/Enterprise, GDS, Bloom, NeoDash, Aura, NVL)** | C01 | A | `active` | GPLv3 (Community) / Commercial | yes | INTEGRATE as required backend; support C | [`04-COMPETITOR-DEEP-DIVES/C01-neo4j.md`](04-COMPETITOR-DEEP-DIVES/C01-neo4j.md) |
| `T-C01-amazon-neptune` | **Amazon Neptune (Database, Neptune Analytics, RDF/SPARQL mode)** | C01 | A | `active` | Proprietary AWS Managed Servic | no | INTEGRATE as optional cloud backend; bui | [`04-COMPETITOR-DEEP-DIVES/C01-amazon-neptune.md`](04-COMPETITOR-DEEP-DIVES/C01-amazon-neptune.md) |
| `T-C01-azure-cosmos-db-gremlin` | **Azure Cosmos DB for Apache Gremlin** | C01 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-azure-cosmos-db-gremlin.md`](04-COMPETITOR-DEEP-DIVES/C01-azure-cosmos-db-gremlin.md) |
| `T-C01-memgraph` | **Memgraph (with MAGE)** | C01 | A | `active` | Apache-2.0 (Core) / BSL (MAGE) | yes | BENCHMARK in-memory Cypher; evaluate MAG | [`04-COMPETITOR-DEEP-DIVES/C01-memgraph.md`](04-COMPETITOR-DEEP-DIVES/C01-memgraph.md) |
| `T-C01-falkordb` | **FalkorDB** | C01 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-falkordb.md`](04-COMPETITOR-DEEP-DIVES/C01-falkordb.md) |
| `T-C01-redisgraph` | **RedisGraph (historical)** | C01 | C | `end-of-life` | SSPL / Historical | yes | HISTORICAL LESSONS ONLY | [`04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md) |
| `T-C01-tigergraph` | **TigerGraph** | C01 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-tigergraph.md`](04-COMPETITOR-DEEP-DIVES/C01-tigergraph.md) |
| `T-C01-janusgraph` | **JanusGraph** | C01 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-janusgraph.md`](04-COMPETITOR-DEEP-DIVES/C01-janusgraph.md) |
| `T-C01-kuzu` | **Kùzu and successors/forks** | C01 | B | `archived` | MIT | yes | STUDY columnar WCOJ architecture; do not | [`04-COMPETITOR-DEEP-DIVES/C01-kuzu.md`](04-COMPETITOR-DEEP-DIVES/C01-kuzu.md) |
| `T-C01-arangodb` | **ArangoDB** | C01 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-arangodb.md`](04-COMPETITOR-DEEP-DIVES/C01-arangodb.md) |
| `T-C01-nebulagraph` | **NebulaGraph** | C01 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-nebulagraph.md`](04-COMPETITOR-DEEP-DIVES/C01-nebulagraph.md) |
| `T-C01-arcadedb` | **ArcadeDB** | C01 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-arcadedb.md`](04-COMPETITOR-DEEP-DIVES/C01-arcadedb.md) |
| `T-C01-apache-age` | **Apache AGE** | C01 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-apache-age.md`](04-COMPETITOR-DEEP-DIVES/C01-apache-age.md) |
| `T-C01-typedb` | **TypeDB (TypeQL)** | C01 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-typedb.md`](04-COMPETITOR-DEEP-DIVES/C01-typedb.md) |
| `T-C01-terminusdb` | **TerminusDB** | C01 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-terminusdb.md`](04-COMPETITOR-DEEP-DIVES/C01-terminusdb.md) |
| `T-C01-dgraph` | **Dgraph** | C01 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-dgraph.md`](04-COMPETITOR-DEEP-DIVES/C01-dgraph.md) |
| `T-C01-graphscope` | **GraphScope / GraphScope Flex** | C01 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-graphscope.md`](04-COMPETITOR-DEEP-DIVES/C01-graphscope.md) |
| `T-C01-oracle-graph` | **Oracle Graph (PGX / Property Graph, SQL/PGQ)** | C01 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-oracle-graph.md`](04-COMPETITOR-DEEP-DIVES/C01-oracle-graph.md) |
| `T-C01-spanner-graph` | **Google Spanner Graph** | C01 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-spanner-graph.md`](04-COMPETITOR-DEEP-DIVES/C01-spanner-graph.md) |
| `T-C01-puppygraph` | **PuppyGraph** | C01 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-puppygraph.md`](04-COMPETITOR-DEEP-DIVES/C01-puppygraph.md) |
| `T-C01-tugraph` | **TuGraph** | C01 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md) |
| `T-C01-ultipa` | **Ultipa** | C01 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md) |
| `T-C01-surrealdb` | **SurrealDB** | C01 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md) |
| `T-C01-sap-hana-graph` | **SAP HANA Graph** | C01 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md) |
| `T-C01-aerospike-graph` | **Aerospike Graph** | C01 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md) |
| `T-C01-duckpgq` | **DuckPGQ** | C01 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md) |
| `T-C01-cozodb` | **CozoDB** | C01 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md) |
| `T-C01-helixdb` | **HelixDB** | C01 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md) |
| `T-C01-galaxybase` | **Galaxybase** | C01 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md) |
| `T-C01-orientdb` | **OrientDB (historical)** | C01 | C | `end-of-life` | SSPL / Historical | yes | HISTORICAL LESSONS ONLY | [`04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C01-tier-c-records.md) |
| `T-C02-stardog` | **Stardog (incl. Voicebox)** | C02 | A | `active` | Commercial Proprietary | yes | BENCHMARK reasoning and virtualization;  | [`04-COMPETITOR-DEEP-DIVES/C02-stardog.md`](04-COMPETITOR-DEEP-DIVES/C02-stardog.md) |
| `T-C02-ontotext-graphdb` | **Ontotext GraphDB** | C02 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-ontotext-graphdb.md`](04-COMPETITOR-DEEP-DIVES/C02-ontotext-graphdb.md) |
| `T-C02-apache-jena` | **Apache Jena (TDB2, Fuseki, rules, SHACL)** | C02 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-apache-jena.md`](04-COMPETITOR-DEEP-DIVES/C02-apache-jena.md) |
| `T-C02-allegrograph` | **AllegroGraph** | C02 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-allegrograph.md`](04-COMPETITOR-DEEP-DIVES/C02-allegrograph.md) |
| `T-C02-eclipse-rdf4j` | **Eclipse RDF4J** | C02 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-eclipse-rdf4j.md`](04-COMPETITOR-DEEP-DIVES/C02-eclipse-rdf4j.md) |
| `T-C02-openlink-virtuoso` | **OpenLink Virtuoso** | C02 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-openlink-virtuoso.md`](04-COMPETITOR-DEEP-DIVES/C02-openlink-virtuoso.md) |
| `T-C02-rdfox` | **RDFox** | C02 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-rdfox.md`](04-COMPETITOR-DEEP-DIVES/C02-rdfox.md) |
| `T-C02-oxigraph` | **Oxigraph** | C02 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-oxigraph.md`](04-COMPETITOR-DEEP-DIVES/C02-oxigraph.md) |
| `T-C02-qlever` | **QLever** | C02 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-qlever.md`](04-COMPETITOR-DEEP-DIVES/C02-qlever.md) |
| `T-C02-anzo` | **Altair Graph Studio / Anzo / AnzoGraph** | C02 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-anzo.md`](04-COMPETITOR-DEEP-DIVES/C02-anzo.md) |
| `T-C02-blazegraph` | **Blazegraph** | C02 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md) |
| `T-C02-millenniumdb` | **MillenniumDB** | C02 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md) |
| `T-C02-corese` | **Corese** | C02 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md) |
| `T-C02-hdt` | **HDT (compressed RDF)** | C02 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md) |
| `T-C02-comunica` | **Comunica** | C02 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md) |
| `T-C02-nemo` | **Nemo (Datalog reasoner)** | C02 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md) |
| `T-C02-vlog` | **VLog** | C02 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md) |
| `T-C02-souffle` | **Soufflé** | C02 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C02-tier-c-records.md) |
| `T-C03-protege` | **Protégé and WebProtégé** | C03 | A | `active` | BSD-2-Clause | yes | BENCHMARK ontology authoring; invert sin | [`04-COMPETITOR-DEEP-DIVES/C03-protege.md`](04-COMPETITOR-DEEP-DIVES/C03-protege.md) |
| `T-C03-topbraid-edg` | **TopBraid EDG** | C03 | A | `active` | Commercial Proprietary | yes | BENCHMARK enterprise governance; invert  | [`04-COMPETITOR-DEEP-DIVES/C03-topbraid-edg.md`](04-COMPETITOR-DEEP-DIVES/C03-topbraid-edg.md) |
| `T-C03-poolparty` | **PoolParty** | C03 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-poolparty.md`](04-COMPETITOR-DEEP-DIVES/C03-poolparty.md) |
| `T-C03-metaphactory` | **metaphactory** | C03 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-metaphactory.md`](04-COMPETITOR-DEEP-DIVES/C03-metaphactory.md) |
| `T-C03-vocbench` | **VocBench 3** | C03 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-vocbench.md`](04-COMPETITOR-DEEP-DIVES/C03-vocbench.md) |
| `T-C03-timbr` | **Timbr.ai** | C03 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-timbr.md`](04-COMPETITOR-DEEP-DIVES/C03-timbr.md) |
| `T-C03-linkml` | **LinkML** | C03 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-linkml.md`](04-COMPETITOR-DEEP-DIVES/C03-linkml.md) |
| `T-C03-robot-odk` | **ROBOT and Ontology Development Kit (ODK)** | C03 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-robot-odk.md`](04-COMPETITOR-DEEP-DIVES/C03-robot-odk.md) |
| `T-C03-pyshacl` | **pySHACL** | C03 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-pyshacl.md`](04-COMPETITOR-DEEP-DIVES/C03-pyshacl.md) |
| `T-C03-owl-reasoners` | **OWL reasoners: ELK, HermiT, Openllet/Pellet, Konclude, FaCT++** | C03 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-owl-reasoners.md`](04-COMPETITOR-DEEP-DIVES/C03-owl-reasoners.md) |
| `T-C03-wikibase` | **Wikibase and Semantic MediaWiki** | C03 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-wikibase.md`](04-COMPETITOR-DEEP-DIVES/C03-wikibase.md) |
| `T-C03-owl-api` | **OWL API** | C03 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md) |
| `T-C03-owlready2` | **Owlready2** | C03 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md) |
| `T-C03-oops` | **OOPS! ontology pitfall scanner** | C03 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md) |
| `T-C03-skos-tooling` | **SKOS tooling (Skosmos, skosify, qSKOS)** | C03 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md) |
| `T-C03-widoco` | **Widoco** | C03 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md) |
| `T-C03-grafo` | **Gra.fo** | C03 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md) |
| `T-C03-ontotext-refine` | **Ontotext Refine** | C03 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md) |
| `T-C03-ontoportal` | **OntoPortal / BioPortal** | C03 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md) |
| `T-C03-ontouml` | **OntoUML ecosystem** | C03 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md) |
| `T-C03-kbpedia` | **KBpedia** | C03 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md) |
| `T-C03-upper-ontologies` | **Upper/domain ontologies (BFO, gist, DOLCE, schema.org, FIBO, W3C ORG)** | C03 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md) |
| `T-C04-senzing` | **Senzing** | C04 | A | `active` | Commercial SDK (Free tier avai | yes | BENCHMARK real-time ER; evaluate as comm | [`04-COMPETITOR-DEEP-DIVES/C04-senzing.md`](04-COMPETITOR-DEEP-DIVES/C04-senzing.md) |
| `T-C04-splink` | **Splink** | C04 | A | `active` | MIT | yes | REUSE as core probabilistic entity resol | [`04-COMPETITOR-DEEP-DIVES/C04-splink.md`](04-COMPETITOR-DEEP-DIVES/C04-splink.md) |
| `T-C04-zingg` | **Zingg** | C04 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C04-zingg.md`](04-COMPETITOR-DEEP-DIVES/C04-zingg.md) |
| `T-C04-ontop` | **Ontop** | C04 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C04-ontop.md`](04-COMPETITOR-DEEP-DIVES/C04-ontop.md) |
| `T-C04-dedupe` | **Dedupe** | C04 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C04-dedupe.md`](04-COMPETITOR-DEEP-DIVES/C04-dedupe.md) |
| `T-C04-jedai` | **JedAI** | C04 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C04-jedai.md`](04-COMPETITOR-DEEP-DIVES/C04-jedai.md) |
| `T-C04-ditto` | **Ditto (deep entity matching)** | C04 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C04-ditto.md`](04-COMPETITOR-DEEP-DIVES/C04-ditto.md) |
| `T-C04-llm-entity-matching` | **LLM-assisted entity matching (approach)** | C04 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C04-llm-entity-matching.md`](04-COMPETITOR-DEEP-DIVES/C04-llm-entity-matching.md) |
| `T-C04-rml-tools` | **RML ecosystem: RMLMapper, RML-Streamer, YARRRML, Morph-KGC, SDM-RDFizer** | C04 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C04-rml-tools.md`](04-COMPETITOR-DEEP-DIVES/C04-rml-tools.md) |
| `T-C04-openrefine` | **OpenRefine and Wikidata reconciliation** | C04 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C04-openrefine.md`](04-COMPETITOR-DEEP-DIVES/C04-openrefine.md) |
| `T-C04-ontology-alignment` | **Ontology alignment: LogMap, AgreementMakerLight, OAEI systems** | C04 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C04-ontology-alignment.md`](04-COMPETITOR-DEEP-DIVES/C04-ontology-alignment.md) |
| `T-C04-schema-inference` | **JSON/CSV schema inference and automatic ER detection tools** | C04 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C04-schema-inference.md`](04-COMPETITOR-DEEP-DIVES/C04-schema-inference.md) |
| `T-C04-sparql-generate` | **SPARQL-Generate** | C04 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C04-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C04-tier-c-records.md) |
| `T-C04-karma` | **Karma** | C04 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C04-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C04-tier-c-records.md) |
| `T-C04-magellan` | **py_entitymatching (Magellan)** | C04 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C04-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C04-tier-c-records.md) |
| `T-C04-recordlinkage` | **recordlinkage (Python)** | C04 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C04-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C04-tier-c-records.md) |
| `T-C05-apache-tika` | **Apache Tika** | C05 | B | `active` | Apache-2.0 | yes | REUSE in extraction worker for deep poly | [`04-COMPETITOR-DEEP-DIVES/C05-apache-tika.md`](04-COMPETITOR-DEEP-DIVES/C05-apache-tika.md) |
| `T-C05-unstructured` | **Unstructured** | C05 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C05-unstructured.md`](04-COMPETITOR-DEEP-DIVES/C05-unstructured.md) |
| `T-C05-docling` | **Docling** | C05 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C05-docling.md`](04-COMPETITOR-DEEP-DIVES/C05-docling.md) |
| `T-C05-marker` | **Marker** | C05 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C05-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C05-tier-c-records.md) |
| `T-C05-spacy` | **spaCy** | C05 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C05-spacy.md`](04-COMPETITOR-DEEP-DIVES/C05-spacy.md) |
| `T-C05-gliner` | **GLiNER** | C05 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C05-gliner.md`](04-COMPETITOR-DEEP-DIVES/C05-gliner.md) |
| `T-C05-rebel-relik` | **REBEL and ReLiK** | C05 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C05-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C05-tier-c-records.md) |
| `T-C05-coref-event-table` | **Coreference, event and table extraction tooling** | C05 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C05-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C05-tier-c-records.md) |
| `T-C05-llm-schema-extraction` | **LLM schema-guided extraction (Neo4j LLM Graph Builder, LlamaIndex extractors)** | C05 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C05-llm-schema-extraction.md`](04-COMPETITOR-DEEP-DIVES/C05-llm-schema-extraction.md) |
| `T-C05-presidio` | **Microsoft Presidio** | C05 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C05-presidio.md`](04-COMPETITOR-DEEP-DIVES/C05-presidio.md) |
| `T-C05-secret-scanners` | **Secret scanners (gitleaks, TruffleHog, detect-secrets)** | C05 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C05-secret-scanners.md`](04-COMPETITOR-DEEP-DIVES/C05-secret-scanners.md) |
| `T-C06-atlan` | **Atlan** | C06 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C06-atlan.md`](04-COMPETITOR-DEEP-DIVES/C06-atlan.md) |
| `T-C06-collibra` | **Collibra** | C06 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C06-collibra.md`](04-COMPETITOR-DEEP-DIVES/C06-collibra.md) |
| `T-C06-data-world` | **data.world** | C06 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C06-data-world.md`](04-COMPETITOR-DEEP-DIVES/C06-data-world.md) |
| `T-C06-datahub` | **DataHub** | C06 | B | `active` | Apache-2.0 | yes | BENCHMARK metadata graph & ingestion pro | [`04-COMPETITOR-DEEP-DIVES/C06-datahub.md`](04-COMPETITOR-DEEP-DIVES/C06-datahub.md) |
| `T-C06-openmetadata` | **OpenMetadata** | C06 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C06-openmetadata.md`](04-COMPETITOR-DEEP-DIVES/C06-openmetadata.md) |
| `T-C06-apache-atlas` | **Apache Atlas** | C06 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C06-apache-atlas.md`](04-COMPETITOR-DEEP-DIVES/C06-apache-atlas.md) |
| `T-C06-microsoft-purview` | **Microsoft Purview** | C06 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C06-microsoft-purview.md`](04-COMPETITOR-DEEP-DIVES/C06-microsoft-purview.md) |
| `T-C06-ovaledge` | **OvalEdge** | C06 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md) |
| `T-C06-actian-dip` | **Actian Data Intelligence Platform** | C06 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md) |
| `T-C06-egeria` | **Egeria** | C06 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md) |
| `T-C06-amundsen` | **Amundsen** | C06 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md) |
| `T-C06-unity-catalog` | **Unity Catalog (OSS)** | C06 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md) |
| `T-C06-apache-polaris` | **Apache Polaris** | C06 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md) |
| `T-C06-alation` | **Alation** | C06 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md) |
| `T-C06-informatica-claire` | **Informatica (CLAIRE/IDMC)** | C06 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md) |
| `T-C06-google-dataplex` | **Google Dataplex** | C06 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C06-tier-c-records.md) |
| `T-C07-palantir-foundry` | **Palantir Foundry Ontology and AIP** | C07 | A | `active` | Commercial Proprietary SaaS/Ap | yes | BENCHMARK operational ontology and actio | [`04-COMPETITOR-DEEP-DIVES/C07-palantir-foundry.md`](04-COMPETITOR-DEEP-DIVES/C07-palantir-foundry.md) |
| `T-C07-glean-enterprise` | **Glean (enterprise search and work graph)** | C07 | A | `active` | Commercial SaaS | no | BENCHMARK enterprise work graph & search | [`04-COMPETITOR-DEEP-DIVES/C07-glean-enterprise.md`](04-COMPETITOR-DEEP-DIVES/C07-glean-enterprise.md) |
| `T-C07-atlassian-rovo` | **Atlassian Rovo and Teamwork Graph** | C07 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C07-atlassian-rovo.md`](04-COMPETITOR-DEEP-DIVES/C07-atlassian-rovo.md) |
| `T-C07-microsoft-graph-copilot-fabric` | **Microsoft Graph, M365 Copilot connectors, Fabric graph/ontology** | C07 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C07-microsoft-graph-copilot-fabric.md`](04-COMPETITOR-DEEP-DIVES/C07-microsoft-graph-copilot-fabric.md) |
| `T-C07-servicenow-kg` | **ServiceNow knowledge graph and CMDB** | C07 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C07-servicenow-kg.md`](04-COMPETITOR-DEEP-DIVES/C07-servicenow-kg.md) |
| `T-C07-onyx` | **Onyx (formerly Danswer)** | C07 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C07-onyx.md`](04-COMPETITOR-DEEP-DIVES/C07-onyx.md) |
| `T-C07-sap-knowledge-graph` | **SAP knowledge graph** | C07 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C07-sap-knowledge-graph.md`](04-COMPETITOR-DEEP-DIVES/C07-sap-knowledge-graph.md) |
| `T-C07-salesforce-data-cloud` | **Salesforce Data Cloud** | C07 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C07-salesforce-data-cloud.md`](04-COMPETITOR-DEEP-DIVES/C07-salesforce-data-cloud.md) |
| `T-C07-diffbot` | **Diffbot Knowledge Graph** | C07 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C07-diffbot.md`](04-COMPETITOR-DEEP-DIVES/C07-diffbot.md) |
| `T-C07-writer-kg` | **Writer Knowledge Graph** | C07 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C07-writer-kg.md`](04-COMPETITOR-DEEP-DIVES/C07-writer-kg.md) |
| `T-C07-azure-digital-twins` | **Azure Digital Twins and DTDL** | C07 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C07-azure-digital-twins.md`](04-COMPETITOR-DEEP-DIVES/C07-azure-digital-twins.md) |
| `T-C07-eclipse-ditto` | **Eclipse Ditto** | C07 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C07-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C07-tier-c-records.md) |
| `T-C07-process-mining` | **Object-centric process mining: Celonis, PM4Py, OCEL 2.0** | C07 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C07-process-mining.md`](04-COMPETITOR-DEEP-DIVES/C07-process-mining.md) |
| `T-C07-ona` | **Organisational network analysis (pattern)** | C07 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C07-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C07-tier-c-records.md) |
| `T-C08-microsoft-graphrag` | **Microsoft GraphRAG and LazyGraphRAG** | C08 | A | `active` | MIT | yes | BENCHMARK hierarchical community summari | [`04-COMPETITOR-DEEP-DIVES/C08-microsoft-graphrag.md`](04-COMPETITOR-DEEP-DIVES/C08-microsoft-graphrag.md) |
| `T-C08-lightrag` | **LightRAG** | C08 | A | `active` | MIT | yes | ADOPT dual-level retrieval (low-level sp | [`04-COMPETITOR-DEEP-DIVES/C08-lightrag.md`](04-COMPETITOR-DEEP-DIVES/C08-lightrag.md) |
| `T-C08-hipporag` | **HippoRAG and HippoRAG 2** | C08 | A | `active` | MIT | yes | ADOPT hippocampal indexing and Personali | [`04-COMPETITOR-DEEP-DIVES/C08-hipporag.md`](04-COMPETITOR-DEEP-DIVES/C08-hipporag.md) |
| `T-C08-neo4j-graphrag` | **Neo4j GraphRAG package** | C08 | A | `active` | GPLv3 (Community) / Commercial | yes | INTEGRATE as required backend; support C | [`04-COMPETITOR-DEEP-DIVES/C08-neo4j-graphrag.md`](04-COMPETITOR-DEEP-DIVES/C08-neo4j-graphrag.md) |
| `T-C08-graphiti-zep` | **Zep and Graphiti** | C08 | A | `active` | Apache-2.0 | yes | ADOPT bi-temporal episodic KG pattern; i | [`04-COMPETITOR-DEEP-DIVES/C08-graphiti-zep.md`](04-COMPETITOR-DEEP-DIVES/C08-graphiti-zep.md) |
| `T-C08-cognee` | **Cognee** | C08 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-cognee.md`](04-COMPETITOR-DEEP-DIVES/C08-cognee.md) |
| `T-C08-mem0` | **Mem0** | C08 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-mem0.md`](04-COMPETITOR-DEEP-DIVES/C08-mem0.md) |
| `T-C08-letta` | **Letta (MemGPT)** | C08 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-letta.md`](04-COMPETITOR-DEEP-DIVES/C08-letta.md) |
| `T-C08-llamaindex-pgi` | **LlamaIndex PropertyGraphIndex** | C08 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-llamaindex-pgi.md`](04-COMPETITOR-DEEP-DIVES/C08-llamaindex-pgi.md) |
| `T-C08-openspg-kag` | **OpenSPG / KAG** | C08 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-openspg-kag.md`](04-COMPETITOR-DEEP-DIVES/C08-openspg-kag.md) |
| `T-C08-fast-graphrag` | **fast-graphrag** | C08 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-fast-graphrag.md`](04-COMPETITOR-DEEP-DIVES/C08-fast-graphrag.md) |
| `T-C08-whyhow` | **WhyHow.AI** | C08 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-whyhow.md`](04-COMPETITOR-DEEP-DIVES/C08-whyhow.md) |
| `T-C08-raptor` | **RAPTOR** | C08 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-raptor.md`](04-COMPETITOR-DEEP-DIVES/C08-raptor.md) |
| `T-C08-think-on-graph` | **Think-on-Graph** | C08 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-think-on-graph.md`](04-COMPETITOR-DEEP-DIVES/C08-think-on-graph.md) |
| `T-C08-ragflow` | **RAGFlow** | C08 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-ragflow.md`](04-COMPETITOR-DEEP-DIVES/C08-ragflow.md) |
| `T-C08-haystack` | **Haystack** | C08 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-haystack.md`](04-COMPETITOR-DEEP-DIVES/C08-haystack.md) |
| `T-C08-text-to-query` | **Text-to-query systems (Text2Cypher, text-to-Gremlin, text-to-SPARQL)** | C08 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-text-to-query.md`](04-COMPETITOR-DEEP-DIVES/C08-text-to-query.md) |
| `T-C08-langchain-langgraph` | **LangChain and LangGraph** | C08 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-langchain-langgraph.md`](04-COMPETITOR-DEEP-DIVES/C08-langchain-langgraph.md) |
| `T-C08-nano-graphrag` | **nano-graphrag** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C08-infranodus` | **InfraNodus** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C08-contextclue` | **ContextClue Graph Builder** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C08-harmony-mcp` | **Harmony MCP** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C08-mempalace` | **MemPalace** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C08-mythos` | **MythOS** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C08-claude-mem` | **claude-mem** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C08-g-retriever` | **G-Retriever** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C08-pathrag` | **PathRAG** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C08-minirag` | **MiniRAG** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C08-structrag` | **StructRAG** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C08-r2r` | **R2R** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C08-kotaemon` | **Kotaemon** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C08-txtai` | **txtai** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C08-langmem` | **LangMem** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C08-a-mem` | **A-MEM** | C08 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C08-tier-c-records.md) |
| `T-C09-mcp` | **Model Context Protocol (incl. graph-database MCP servers)** | C09 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C09-mcp.md`](04-COMPETITOR-DEEP-DIVES/C09-mcp.md) |
| `T-C09-a2a` | **Agent2Agent (A2A)** | C09 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C09-a2a.md`](04-COMPETITOR-DEEP-DIVES/C09-a2a.md) |
| `T-C09-agent-frameworks` | **Agent frameworks: AutoGen/AG2, Microsoft Agent Framework/Semantic Kernel, CrewAI, OpenAI Agents SDK, Claude Agent SDK, Google ADK, PydanticAI** | C09 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C09-agent-frameworks.md`](04-COMPETITOR-DEEP-DIVES/C09-agent-frameworks.md) |
| `T-C09-dspy` | **DSPy** | C09 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C09-dspy.md`](04-COMPETITOR-DEEP-DIVES/C09-dspy.md) |
| `T-C09-ollama` | **Ollama** | C09 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C09-ollama.md`](04-COMPETITOR-DEEP-DIVES/C09-ollama.md) |
| `T-C09-llama-cpp` | **llama.cpp** | C09 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C09-llama-cpp.md`](04-COMPETITOR-DEEP-DIVES/C09-llama-cpp.md) |
| `T-C09-vllm-sglang` | **vLLM and SGLang** | C09 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C09-vllm-sglang.md`](04-COMPETITOR-DEEP-DIVES/C09-vllm-sglang.md) |
| `T-C09-hf-tei` | **Hugging Face Text Embeddings Inference** | C09 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C09-hf-tei.md`](04-COMPETITOR-DEEP-DIVES/C09-hf-tei.md) |
| `T-C09-onnx-runtime` | **ONNX Runtime** | C09 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C09-onnx-runtime.md`](04-COMPETITOR-DEEP-DIVES/C09-onnx-runtime.md) |
| `T-C09-local-embeddings` | **Local embedding and reranker models (BGE, E5, GTE, Nomic, Jina, ColBERT-style)** | C09 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C09-local-embeddings.md`](04-COMPETITOR-DEEP-DIVES/C09-local-embeddings.md) |
| `T-C09-guardrails` | **Guardrails: NeMo Guardrails, Llama Guard, prompt-injection defences** | C09 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C09-guardrails.md`](04-COMPETITOR-DEEP-DIVES/C09-guardrails.md) |
| `T-C10-qdrant` | **Qdrant** | C10 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C10-qdrant.md`](04-COMPETITOR-DEEP-DIVES/C10-qdrant.md) |
| `T-C10-pgvector` | **pgvector** | C10 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C10-pgvector.md`](04-COMPETITOR-DEEP-DIVES/C10-pgvector.md) |
| `T-C10-opensearch` | **OpenSearch (k-NN, full-text)** | C10 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C10-opensearch.md`](04-COMPETITOR-DEEP-DIVES/C10-opensearch.md) |
| `T-C10-milvus` | **Milvus** | C10 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C10-milvus.md`](04-COMPETITOR-DEEP-DIVES/C10-milvus.md) |
| `T-C10-weaviate` | **Weaviate** | C10 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C10-weaviate.md`](04-COMPETITOR-DEEP-DIVES/C10-weaviate.md) |
| `T-C10-lancedb` | **LanceDB** | C10 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C10-lancedb.md`](04-COMPETITOR-DEEP-DIVES/C10-lancedb.md) |
| `T-C10-elasticsearch` | **Elasticsearch** | C10 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C10-elasticsearch.md`](04-COMPETITOR-DEEP-DIVES/C10-elasticsearch.md) |
| `T-C10-vespa` | **Vespa** | C10 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C10-vespa.md`](04-COMPETITOR-DEEP-DIVES/C10-vespa.md) |
| `T-C10-chroma` | **Chroma** | C10 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C10-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C10-tier-c-records.md) |
| `T-C10-tantivy-lucene` | **Tantivy and Lucene** | C10 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C10-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C10-tier-c-records.md) |
| `T-C10-native-graph-vector` | **Native vector indexes inside graph engines** | C10 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C10-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C10-tier-c-records.md) |
| `T-C11-pyg` | **PyTorch Geometric** | C11 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C11-pyg.md`](04-COMPETITOR-DEEP-DIVES/C11-pyg.md) |
| `T-C11-dgl` | **DGL** | C11 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C11-dgl.md`](04-COMPETITOR-DEEP-DIVES/C11-dgl.md) |
| `T-C11-pykeen` | **PyKEEN** | C11 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C11-pykeen.md`](04-COMPETITOR-DEEP-DIVES/C11-pykeen.md) |
| `T-C11-ultra` | **ULTRA (KG foundation model)** | C11 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C11-ultra.md`](04-COMPETITOR-DEEP-DIVES/C11-ultra.md) |
| `T-C11-relbench` | **Relational deep learning (RelBench)** | C11 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C11-relbench.md`](04-COMPETITOR-DEEP-DIVES/C11-relbench.md) |
| `T-C11-graphstorm` | **GraphStorm** | C11 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md) |
| `T-C11-ampligraph` | **AmpliGraph** | C11 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md) |
| `T-C11-dgl-ke` | **DGL-KE** | C11 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md) |
| `T-C11-pyg-temporal` | **PyTorch Geometric Temporal** | C11 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md) |
| `T-C11-graphgym` | **GraphGym** | C11 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md) |
| `T-C11-graph-transformers` | **Graph transformers (Graphormer, GraphGPS)** | C11 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md) |
| `T-C11-tgn` | **Temporal GNNs (TGN and frameworks)** | C11 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md) |
| `T-C11-torchkge-libkge` | **TorchKGE and LibKGE** | C11 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md) |
| `T-C11-neuro-symbolic` | **Neuro-symbolic frameworks (Scallop, DeepProbLog, Logic Tensor Networks)** | C11 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C11-tier-c-records.md) |
| `T-C12-tinkerpop` | **Apache TinkerPop / Gremlin** | C12 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C12-tinkerpop.md`](04-COMPETITOR-DEEP-DIVES/C12-tinkerpop.md) |
| `T-C12-networkx` | **NetworkX** | C12 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C12-networkx.md`](04-COMPETITOR-DEEP-DIVES/C12-networkx.md) |
| `T-C12-igraph` | **igraph** | C12 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C12-igraph.md`](04-COMPETITOR-DEEP-DIVES/C12-igraph.md) |
| `T-C12-rustworkx` | **Rustworkx** | C12 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C12-rustworkx.md`](04-COMPETITOR-DEEP-DIVES/C12-rustworkx.md) |
| `T-C12-graphblas` | **GraphBLAS (SuiteSparse)** | C12 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C12-graphblas.md`](04-COMPETITOR-DEEP-DIVES/C12-graphblas.md) |
| `T-C12-raphtory` | **Raphtory** | C12 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C12-raphtory.md`](04-COMPETITOR-DEEP-DIVES/C12-raphtory.md) |
| `T-C12-graphx-graphframes` | **GraphX and GraphFrames (Spark)** | C12 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C12-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C12-tier-c-records.md) |
| `T-C12-cugraph` | **RAPIDS cuGraph** | C12 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C12-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C12-tier-c-records.md) |
| `T-C12-graphology` | **Graphology** | C12 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C12-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C12-tier-c-records.md) |
| `T-C12-ligra-gap` | **Ligra and GAP benchmark suite** | C12 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C12-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C12-tier-c-records.md) |
| `T-C13-openlineage-marquez` | **OpenLineage and Marquez** | C13 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C13-openlineage-marquez.md`](04-COMPETITOR-DEEP-DIVES/C13-openlineage-marquez.md) |
| `T-C13-prov-o` | **W3C PROV / PROV-O** | C13 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C13-prov-o.md`](04-COMPETITOR-DEEP-DIVES/C13-prov-o.md) |
| `T-C13-event-sourcing` | **Event sourcing, CQRS and bitemporal modelling (pattern)** | C13 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C13-event-sourcing.md`](04-COMPETITOR-DEEP-DIVES/C13-event-sourcing.md) |
| `T-C13-xtdb` | **XTDB** | C13 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C13-xtdb.md`](04-COMPETITOR-DEEP-DIVES/C13-xtdb.md) |
| `T-C13-datomic` | **Datomic** | C13 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C13-datomic.md`](04-COMPETITOR-DEEP-DIVES/C13-datomic.md) |
| `T-C13-dolt` | **Dolt** | C13 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C13-dolt.md`](04-COMPETITOR-DEEP-DIVES/C13-dolt.md) |
| `T-C13-fluree` | **Fluree** | C13 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C13-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C13-tier-c-records.md) |
| `T-C13-lakefs` | **lakeFS** | C13 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C13-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C13-tier-c-records.md) |
| `T-C13-table-time-travel` | **Apache Iceberg / Delta Lake time travel** | C13 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C13-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C13-tier-c-records.md) |
| `T-C13-spline` | **Spline** | C13 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C13-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C13-tier-c-records.md) |
| `T-C13-aeong` | **AeonG-style temporal graph research** | C13 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C13-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C13-tier-c-records.md) |
| `T-C14-debezium` | **Debezium** | C14 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C14-debezium.md`](04-COMPETITOR-DEEP-DIVES/C14-debezium.md) |
| `T-C14-kafka` | **Apache Kafka and Kafka Connect** | C14 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C14-kafka.md`](04-COMPETITOR-DEEP-DIVES/C14-kafka.md) |
| `T-C14-nats` | **NATS** | C14 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C14-nats.md`](04-COMPETITOR-DEEP-DIVES/C14-nats.md) |
| `T-C14-airbyte` | **Airbyte** | C14 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C14-airbyte.md`](04-COMPETITOR-DEEP-DIVES/C14-airbyte.md) |
| `T-C14-temporal` | **Temporal (durable workflows)** | C14 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C14-temporal.md`](04-COMPETITOR-DEEP-DIVES/C14-temporal.md) |
| `T-C14-redpanda` | **Redpanda and Redpanda Connect (Benthos)** | C14 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C14-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C14-tier-c-records.md) |
| `T-C14-flink` | **Apache Flink** | C14 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C14-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C14-tier-c-records.md) |
| `T-C14-nifi` | **Apache NiFi** | C14 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C14-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C14-tier-c-records.md) |
| `T-C14-seatunnel` | **Apache SeaTunnel** | C14 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C14-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C14-tier-c-records.md) |
| `T-C14-orchestrators` | **Dagster, Airflow, Prefect** | C14 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C14-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C14-tier-c-records.md) |
| `T-C14-dlt-meltano` | **dlt, Meltano/Singer, Apache Hop** | C14 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C14-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C14-tier-c-records.md) |
| `T-C19-keycloak` | **Keycloak / OIDC / SAML** | C19 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C19-keycloak.md`](04-COMPETITOR-DEEP-DIVES/C19-keycloak.md) |
| `T-C19-opa` | **Open Policy Agent / Rego** | C19 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C19-opa.md`](04-COMPETITOR-DEEP-DIVES/C19-opa.md) |
| `T-C19-rebac` | **ReBAC engines: OpenFGA, SpiceDB, Permify** | C19 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C19-rebac.md`](04-COMPETITOR-DEEP-DIVES/C19-rebac.md) |
| `T-C19-cedar-cerbos` | **Cedar and Cerbos** | C19 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C19-cedar-cerbos.md`](04-COMPETITOR-DEEP-DIVES/C19-cedar-cerbos.md) |
| `T-C19-vault-openbao` | **HashiCorp Vault and OpenBao** | C19 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C19-vault-openbao.md`](04-COMPETITOR-DEEP-DIVES/C19-vault-openbao.md) |
| `T-C19-supply-chain` | **Supply chain: Sigstore/cosign, Syft, Grype, Trivy, SLSA, in-toto** | C19 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C19-supply-chain.md`](04-COMPETITOR-DEEP-DIVES/C19-supply-chain.md) |
| `T-C19-opentelemetry` | **OpenTelemetry, Prometheus, Grafana** | C19 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C19-opentelemetry.md`](04-COMPETITOR-DEEP-DIVES/C19-opentelemetry.md) |
| `T-C19-llm-threat-guidance` | **OWASP Top 10 for LLM Apps, agentic-AI guidance, MITRE ATLAS** | C19 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C19-llm-threat-guidance.md`](04-COMPETITOR-DEEP-DIVES/C19-llm-threat-guidance.md) |
| `T-C19-auth-aware-search` | **Authorization-aware search (pattern)** | C19 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C19-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C19-tier-c-records.md) |
| `T-C15-sourcegraph` | **Sourcegraph / Cody** | C15 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-sourcegraph.md`](04-COMPETITOR-DEEP-DIVES/C15-sourcegraph.md) |
| `T-C15-tree-sitter` | **Tree-sitter** | C15 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-tree-sitter.md`](04-COMPETITOR-DEEP-DIVES/C15-tree-sitter.md) |
| `T-C15-scip-lsif` | **SCIP and LSIF** | C15 | A | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-scip-lsif.md`](04-COMPETITOR-DEEP-DIVES/C15-scip-lsif.md) |
| `T-C15-glean-meta` | **Glean (Meta code indexing)** | C15 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-glean-meta.md`](04-COMPETITOR-DEEP-DIVES/C15-glean-meta.md) |
| `T-C15-codeql` | **CodeQL** | C15 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-codeql.md`](04-COMPETITOR-DEEP-DIVES/C15-codeql.md) |
| `T-C15-joern` | **Joern** | C15 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-joern.md`](04-COMPETITOR-DEEP-DIVES/C15-joern.md) |
| `T-C15-semgrep` | **Semgrep** | C15 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-semgrep.md`](04-COMPETITOR-DEEP-DIVES/C15-semgrep.md) |
| `T-C15-greptile` | **Greptile** | C15 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-greptile.md`](04-COMPETITOR-DEEP-DIVES/C15-greptile.md) |
| `T-C15-augment-context` | **Augment Context Engine** | C15 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-augment-context.md`](04-COMPETITOR-DEEP-DIVES/C15-augment-context.md) |
| `T-C15-stack-graphs` | **GitHub stack-graphs** | C15 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-stack-graphs.md`](04-COMPETITOR-DEEP-DIVES/C15-stack-graphs.md) |
| `T-C15-kythe` | **Kythe** | C15 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md) |
| `T-C15-lsp` | **Language Server Protocol ecosystems** | C15 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md) |
| `T-C15-graphify` | **Graphify (repo to pin)** | C15 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-graphify.md`](04-COMPETITOR-DEEP-DIVES/C15-graphify.md) |
| `T-C15-codegraph` | **CodeGraph (repo to pin)** | C15 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-codegraph.md`](04-COMPETITOR-DEEP-DIVES/C15-codegraph.md) |
| `T-C15-code-review-graph` | **code-review-graph (repo to pin)** | C15 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md) |
| `T-C15-repomix` | **Repomix** | C15 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md) |
| `T-C15-grepai` | **grepai (repo to pin)** | C15 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md) |
| `T-C15-gitnexus` | **GitNexus (repo to pin)** | C15 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md) |
| `T-C15-openrewrite` | **OpenRewrite / Moderne** | C15 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-openrewrite.md`](04-COMPETITOR-DEEP-DIVES/C15-openrewrite.md) |
| `T-C15-cast-imaging` | **CAST Imaging** | C15 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-cast-imaging.md`](04-COMPETITOR-DEEP-DIVES/C15-cast-imaging.md) |
| `T-C15-backstage` | **Backstage, Port, Cortex (software catalogs)** | C15 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-backstage.md`](04-COMPETITOR-DEEP-DIVES/C15-backstage.md) |
| `T-C15-dependency-track` | **Dependency-Track, SBOM graphs, deps.dev, OSV** | C15 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-dependency-track.md`](04-COMPETITOR-DEEP-DIVES/C15-dependency-track.md) |
| `T-C15-srcml` | **srcML** | C15 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md) |
| `T-C15-scitools-understand` | **SciTools Understand** | C15 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md) |
| `T-C15-sonarqube` | **SonarQube** | C15 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md) |
| `T-C15-repo-maps` | **Aider repo map and IDE indexes (Cursor, Continue)** | C15 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C15-tier-c-records.md) |
| `T-C16-cytoscape` | **Cytoscape and Cytoscape.js** | C16 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-cytoscape.md`](04-COMPETITOR-DEEP-DIVES/C16-cytoscape.md) |
| `T-C16-sigma` | **Sigma.js** | C16 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-sigma.md`](04-COMPETITOR-DEEP-DIVES/C16-sigma.md) |
| `T-C16-yfiles` | **yFiles** | C16 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-yfiles.md`](04-COMPETITOR-DEEP-DIVES/C16-yfiles.md) |
| `T-C16-keylines-regraph` | **KeyLines and ReGraph (Cambridge Intelligence)** | C16 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-keylines-regraph.md`](04-COMPETITOR-DEEP-DIVES/C16-keylines-regraph.md) |
| `T-C16-linkurious` | **Linkurious Enterprise and Ogma** | C16 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-linkurious.md`](04-COMPETITOR-DEEP-DIVES/C16-linkurious.md) |
| `T-C16-graphxr` | **Kineviz GraphXR** | C16 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-graphxr.md`](04-COMPETITOR-DEEP-DIVES/C16-graphxr.md) |
| `T-C16-gephi` | **Gephi** | C16 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-gephi.md`](04-COMPETITOR-DEEP-DIVES/C16-gephi.md) |
| `T-C16-graphistry` | **Graphistry** | C16 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-graphistry.md`](04-COMPETITOR-DEEP-DIVES/C16-graphistry.md) |
| `T-C16-graphviz` | **Graphviz** | C16 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md) |
| `T-C16-constellation` | **Constellation** | C16 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md) |
| `T-C16-yed` | **yEd** | C16 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md) |
| `T-C16-citespace-vosviewer` | **CiteSpace and VOSviewer** | C16 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md) |
| `T-C16-cosmograph` | **Cosmograph / cosmos.gl** | C16 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md) |
| `T-C16-d3` | **D3.js** | C16 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md) |
| `T-C16-vis-network` | **vis-network** | C16 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md) |
| `T-C16-antv-g6` | **AntV G6** | C16 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md) |
| `T-C16-neo4j-nvl` | **Neo4j NVL** | C16 | C | `active` | GPLv3 (Community) / Commercial | yes | INTEGRATE as required backend; support C | [`04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md) |
| `T-C16-react-force-graph-reagraph` | **react-force-graph and Reagraph** | C16 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md) |
| `T-C16-layout-engines` | **Layout engines: ELK/elkjs, Dagre, WebCola, ForceAtlas2** | C16 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md) |
| `T-C16-kumu-thebrain` | **Kumu and TheBrain** | C16 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C16-tier-c-records.md) |
| `T-C17-atlas-research` | **"Atlas" research-mapping product (identity to resolve)** | C17 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C17-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C17-tier-c-records.md) |
| `T-C17-researchrabbit` | **ResearchRabbit** | C17 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C17-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C17-tier-c-records.md) |
| `T-C17-connected-papers` | **Connected Papers** | C17 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C17-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C17-tier-c-records.md) |
| `T-C17-openalex` | **OpenAlex** | C17 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C17-openalex.md`](04-COMPETITOR-DEEP-DIVES/C17-openalex.md) |
| `T-C17-wikidata` | **Wikidata** | C17 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C17-wikidata.md`](04-COMPETITOR-DEEP-DIVES/C17-wikidata.md) |
| `T-C17-semantic-scholar` | **Semantic Scholar** | C17 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C17-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C17-tier-c-records.md) |
| `T-C17-litmaps-inciteful` | **Litmaps and Inciteful** | C17 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C17-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C17-tier-c-records.md) |
| `T-C17-scite` | **scite** | C17 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C17-scite.md`](04-COMPETITOR-DEEP-DIVES/C17-scite.md) |
| `T-C17-elicit-consensus` | **Elicit and Consensus** | C17 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C17-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C17-tier-c-records.md) |
| `T-C17-obsidian` | **Obsidian** | C17 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C17-obsidian.md`](04-COMPETITOR-DEEP-DIVES/C17-obsidian.md) |
| `T-C17-pkm-tools` | **Logseq, Tana, Roam Research, Heptabase** | C17 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C17-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C17-tier-c-records.md) |
| `T-C18-rdf` | **RDF 1.1/1.2, RDF-star, serialisations (Turtle, TriG, N-Triples, N-Quads, JSON-LD)** | C18 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-rdf.md`](04-COMPETITOR-DEEP-DIVES/C18-rdf.md) |
| `T-C18-owl2` | **RDFS and OWL 2 profiles (EL, QL, RL, DL)** | C18 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-owl2.md`](04-COMPETITOR-DEEP-DIVES/C18-owl2.md) |
| `T-C18-shacl` | **SHACL Core / SHACL-SPARQL / SHACL 1.2** | C18 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-shacl.md`](04-COMPETITOR-DEEP-DIVES/C18-shacl.md) |
| `T-C18-sparql` | **SPARQL 1.1/1.2** | C18 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-sparql.md`](04-COMPETITOR-DEEP-DIVES/C18-sparql.md) |
| `T-C18-opencypher` | **Cypher / openCypher** | C18 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-opencypher.md`](04-COMPETITOR-DEEP-DIVES/C18-opencypher.md) |
| `T-C18-gql` | **ISO/IEC 39075 GQL** | C18 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-gql.md`](04-COMPETITOR-DEEP-DIVES/C18-gql.md) |
| `T-C18-sql-pgq` | **SQL/PGQ (ISO/IEC 9075-16)** | C18 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-sql-pgq.md`](04-COMPETITOR-DEEP-DIVES/C18-sql-pgq.md) |
| `T-C18-pg-schema` | **PG-Schema and LPG schema proposals** | C18 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-pg-schema.md`](04-COMPETITOR-DEEP-DIVES/C18-pg-schema.md) |
| `T-C18-odrl-dpv` | **ODRL and DPV** | C18 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-odrl-dpv.md`](04-COMPETITOR-DEEP-DIVES/C18-odrl-dpv.md) |
| `T-C18-skos-std` | **SKOS** | C18 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md) |
| `T-C18-dcat-schemaorg` | **DCAT and schema.org** | C18 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md) |
| `T-C18-graphql` | **GraphQL** | C18 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md) |
| `T-C18-graph-formats` | **GraphAr, GraphML, GEXF** | C18 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md) |
| `T-C18-tabular-formats` | **CSV, Parquet, Apache Arrow** | C18 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md) |
| `T-C18-api-specs` | **OpenAPI and AsyncAPI** | C18 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md) |
| `T-C18-ngsi-ld` | **NGSI-LD** | C18 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md) |
| `T-C18-geosparql-owltime` | **GeoSPARQL and OWL-Time** | C18 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md) |
| `T-C18-cloudevents` | **CloudEvents** | C18 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md) |
| `T-C18-verifiable-credentials` | **W3C Verifiable Credentials** | C18 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C18-tier-c-records.md) |
| `T-C20-ldbc` | **LDBC (SNB Interactive/BI, FinBench, Graphalytics, SPB)** | C20 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C20-ldbc.md`](04-COMPETITOR-DEEP-DIVES/C20-ldbc.md) |
| `T-C20-graphrag-bench` | **GraphRAG-Bench** | C20 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C20-graphrag-bench.md`](04-COMPETITOR-DEEP-DIVES/C20-graphrag-bench.md) |
| `T-C20-ragas` | **RAGAS** | C20 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C20-ragas.md`](04-COMPETITOR-DEEP-DIVES/C20-ragas.md) |
| `T-C20-beir` | **BEIR** | C20 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C20-beir.md`](04-COMPETITOR-DEEP-DIVES/C20-beir.md) |
| `T-C20-text2cypher-bench` | **Text2Cypher / CypherBench-style sets** | C20 | B | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C20-text2cypher-bench.md`](04-COMPETITOR-DEEP-DIVES/C20-text2cypher-bench.md) |
| `T-C20-memory-benchmarks` | **LoCoMo and LongMemEval** | C20 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md) |
| `T-C20-rdf-benchmarks` | **LUBM, BSBM, WatDiv, gMark** | C20 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md) |
| `T-C20-ogb` | **Open Graph Benchmark** | C20 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md) |
| `T-C20-multihop-qa` | **HotpotQA, 2WikiMultiHopQA, MuSiQue, MultiHop-RAG, CRAG, STaRK, KILT** | C20 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md) |
| `T-C20-mteb` | **MTEB** | C20 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md) |
| `T-C20-rag-evaluators` | **ARES and TruLens** | C20 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md) |
| `T-C20-code-benchmarks` | **SWE-bench, RepoBench, CrossCodeEval, CodeSearchNet** | C20 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md) |
| `T-C20-oaei-er-datasets` | **OAEI and standard entity-resolution datasets** | C20 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md) |
| `T-C20-shacl-test-suites` | **W3C SHACL, JSON-LD and OWL test suites** | C20 | C | `active` | Apache-2.0 | yes | EVALUATE | [`04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md`](04-COMPETITOR-DEEP-DIVES/C20-tier-c-records.md) |

---

## 3. ADD / EXCLUDE / DEFER Resolution Log

| Candidate Technology | Action | Reason | Resolution |
|---|---|---|---|
| Kùzu | DEFER / BENCHMARK ONLY | Upstream official repo archived Oct 2025; study columnar WCOJ architecture only; do not adopt as primary runtime | Kept as Tier B research reference |
| RedisGraph | EXCLUDE (EOL) | Reached official End of Life; succeeded by FalkorDB | Logged as Tier C historical lessons |
| OrientDB | EXCLUDE (LEGACY) | Replaced by ArcadeDB / multi-model modern successors | Logged as Tier C historical lessons |
| Blazegraph | DEFER / REFERENCE | Legacy triplestore; Wikimedia foundation migrated to QLever / alternative backends | Logged as Tier C reference |
| Glean (Meta) | DISAMBIGUATED | Meta's open-source source-code indexer (cross-ref C15) vs. Glean enterprise search (C07) | Split into two distinct registry entries |
| MythOS / MemPalace | RESOLVED | Community personal projects for Claude/MCP memory; verified immature for enterprise core | Logged as Tier C prototypes |
| Amazon Neptune RDF vs LPG | UNIFIED | Single underlying cloud engine with dual query interfaces | Evaluated in C01 with cross-reference to C02 |