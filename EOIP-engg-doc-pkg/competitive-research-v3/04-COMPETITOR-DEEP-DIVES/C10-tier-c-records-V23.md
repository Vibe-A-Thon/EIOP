# C10 Tier C records, batch V23 (verified 2026-10-26)

### T-C10-chroma — Chroma
| Field | Value |
|---|---|
| URL / owner | github.com/chroma-core/chroma; Chroma |
| Latest | 1.5.9 (GitHub "Latest", 05 May 2026; PyPI 1.5.9) |
| Status / licence | active; Apache-2.0 (README and PyPI classifier; PyPI licence field null) - permissive |
| Modes / air-gap | in-memory, persistent, client-server, Chroma Cloud; air-gap yes (local) |

Embedded-first vector store with automatic embedding functions. Touches CAP-53, CAP-04. Tenancy and OSS auth were not covered by the page read, so CAP-46/47 are UNVERIFIED. Adds nothing over LanceDB or Qdrant for EOIP's ACL needs.
**Decision:** REFERENCE-ONLY; prototype-grade comparator.
| CLAIM | Claim | Source | Conf. |
|---|---|---|---|
| CLAIM-chroma-01 | 1.5.9 latest, modes as above, Cloud exists | github.com/chroma-core/chroma/releases; docs.trychroma.com getting-started (2026-10-26) | 0.7 |
| CLAIM-chroma-02 | Apache-2.0 per PyPI classifier and README | pypi.org/project/chromadb (2026-10-26) | 0.8 |

### T-C10-tantivy-lucene — Tantivy and Lucene
| Field | Value |
|---|---|
| URL / owner | github.com/quickwit-oss/tantivy (Quickwit/community); lucene.apache.org (ASF) |
| Latest | Tantivy 0.26.1 (GitHub "Latest", 10 May, year inferred 2026); Lucene 10.5.2 (date UNVERIFIED) |
| Status / licence | both active; Tantivy MIT, Lucene Apache-2.0 - permissive |
| Modes / air-gap | embedded libraries (Rust; Java); air-gap yes |

Full-text libraries beneath most search engines: Lucene powers Elasticsearch, OpenSearch (see C10-opensearch.md) and Neo4j full-text/vector indexes; Tantivy powers Memgraph text search (C01-memgraph). EOIP's BM25 is in-process and non-persistent (BL-13); Tantivy (via a Rust binding, extra native dependency) or Lucene (JVM) would give persistent BM25, but EOIP's lock has no native-extension policy yet. Touches CAP-54, CAP-55.
**Decision:** EXPERIMENT Tantivy as optional persistent BM25 behind the index port; REFERENCE Lucene.
| CLAIM | Claim | Source | Conf. |
|---|---|---|---|
| CLAIM-tantivy-lucene-01 | Tantivy 0.26.1, MIT; project keeps skipping versions (0.23) | github.com/quickwit-oss/tantivy/releases, LICENSE (2026-10-26) | 0.75 |
| CLAIM-tantivy-lucene-02 | Lucene 10.5.2 latest, Apache-2.0, pure Java | lucene.apache.org/core (2026-10-26) | 0.8 |

### T-C10-native-graph-vector — Native vector indexes inside graph engines
| Field | Value |
|---|---|
| Engines | Neo4j, Memgraph, FalkorDB, Neptune Analytics, HugeGraph |
| Status / licence | per C01 deep dives (licences differ; see each) |
| Modes / air-gap | per engine; Neptune Analytics is AWS-managed only |

Per C01 evidence: Neo4j HNSW on Lucene (to 4096 dims, filter properties, same-transaction writes not visible) [CLAIM-neo4j-09]; Memgraph USearch on nodes and edges, ACL-failing results silently dropped, planner ignores vector indexes [CLAIM-memgraph-21]; FalkorDB HNSW with weak filter combination, about 3 GB per 1M x 768 [CLAIM-falkordb-09]; Neptune Analytics one HNSW index per graph (C01-amazon-neptune.md); HugeGraph has no server vector index (HugeGraph-LLM uses external stores) [CLAIM-apache-hugegraph-09]. Relevance: co-locating vectors with graph removes a sync hop but ties ACL to each engine's semantics. Touches CAP-53, CAP-46, CAP-47.
**Decision:** INTEGRATE per-adapter capability flags (`in_tx_visibility`, `filter_props`) behind the vector port; do not rely on them for ACL.
| CLAIM | Claim | Source | Conf. |
|---|---|---|---|
| CLAIM-native-graph-vector-01 | Summary of the five cited C01 claims above | C01-neo4j, C01-memgraph, C01-falkordb, C01-amazon-neptune, C01-apache-hugegraph (2026-10-18/26) | 0.75 |
