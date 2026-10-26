# Batch queue (coordinator working file)

Revised execution plan from 2026-10-26: Sonnet workers, HARD CAPS in WORKER-BRIEF.md, at most 6 running at once. Placeholder files committed on 2026-10-19 (no CLAIM records) are overwritten by real deep dives where slugs match and are excluded from aggregation otherwise.

Already complete (17 real deep dives, Opus workers W01–W20, before the weekly limit): amazon-neptune, apache-hugegraph, arangodb, azure-cosmos-db-gremlin, kuzu, memgraph, neo4j, stardog, senzing, splink, apache-tika, datahub, glean-enterprise, microsoft-graph-copilot-fabric, palantir-foundry, servicenow-kg, graphiti-zep. Registry fragments for these (except W03) are built by the coordinator from the files.

| Batch | Scope | Status |
|---|---|---|
| V01 | falkordb, tigergraph, janusgraph (A); redisgraph (C) | running |
| V02 | ontotext-graphdb, apache-jena, zingg, ontop (A) | running |
| V03 | protege, topbraid-edg, poolparty, metaphactory (A) | running |
| V04 | atlassian-rovo, onyx, cognee (A) | running |
| V05 | microsoft-graphrag, lightrag, hipporag (A) | running |
| V06 | mcp, ollama, qdrant, pgvector, opensearch (A) | running |
| V07 | mem0, letta, neo4j-graphrag (A) | queued |
| V08 | pyg, tinkerpop (A) | queued |
| V09 | sourcegraph, tree-sitter, scip-lsif (A) | queued |
| V10 | llamaindex-pgi, openspg-kag (A) | queued |
| V11 | C19 security (8 B + 1 C) | queued |
| V12 | C04 ER/mapping (8 B + 4 C) | queued |
| V13 | C03 ontology tooling B (7 B) | queued |
| V14 | C03 Tier C (11 C) + C01 B rest: nebulagraph, arcadedb, apache-age, typedb, terminusdb | queued |
| V15 | C01 W07 set (5 B + 10 C) | queued |
| V16 | C02 W09 set (7 B + 8 C) | queued |
| V17 | C05 extraction (7 B + 3 C) | queued |
| V18 | C06 catalogs (6 B + 9 C) | queued |
| V19 | C07 W18 set (6 B + 2 C) | queued |
| V20 | C08 B set (8 B) | queued |
| V21 | C08 Tier C (16 C) | queued |
| V22 | C09 B set (9 B) | queued |
| V23 | C10 B/C set (5 B + 3 C) | queued |
| V24 | C11 (4 B + 9 C) | queued |
| V25 | C12 W33 set (5 B + 4 C) | queued |
| V26 | C13 (6 B + 5 C) | queued |
| V27 | C14 (5 B + 6 C) | queued |
| V28 | C15 W27 B/C (7 B + 2 C) | queued |
| V29 | C15 W28 set (6 B + 8 C) | queued |
| V30 | C16 (8 B + 12 C) | queued |
| V31 | C17 (4 B + 7 C) | queued |
| V32 | C18 (9 B + 10 C) | queued |
| V33 | C20 (5 B + 9 C) | queued |
