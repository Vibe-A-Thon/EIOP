# 07 — Gap Register

| Field | Value |
|---|---|
| Document | 07-GAP-REGISTER.md |
| Generated | 2026-10-26 by the coordinator from `06-MASTER-CAPABILITY-MATRIX.md`, `01-SYSTEM-BASELINE.md`, `01a-BASELINE-DELTA-HEAD.md` and the deep dives |
| Gaps | 46 (P0 11, P1 18, P2 11, P3 6) |
| Priority method | PriorityScore = 0.25·CV + 0.20·SF + 0.15·RR + 0.15·ES + 0.10·RL + 0.10·FE + 0.05·DI − ComplexityPenalty (Master Prompt §13). Inputs 0–5 are coordinator judgements with the rationale shown; P0 is **forced** for correctness, permission, tenant, egress and supply-chain protection regardless of score; otherwise P1 ≥ 3.15, P2 ≥ 2.5, else P3; three judgement overrides are listed with reasons below the table. |
| Gap classes | Missing; Partial; Performance; Quality; Security; Interoperability; Operability; UX; Research gap; Competitive deficit; Unnecessary complexity (Master Prompt §10.2) |

## 1. Register (sorted by priority, then score)

| GAP-ID | Gap | CAP-IDs | Class | Severity | Root cause (proven / hypothesis) | EOIP evidence | Competitor references (deep dive + card) | CV SF RR ES RL FE DI −Pen | Score | Priority | Sensitivity (±1 on CV/ES) | Uncertainty |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GAP-19 | No licence allow-list in CI; several attractive components block OEM | CAP-52, CAP-77 | Differentiator; Operability | High | Proven: no CI licence gate found; research flags AGPL/SSPL/BSL/ELv2 components (Zingg, FalkorDB, Vault, Grafana, Elasticsearch, Airbyte, Redpanda, TruffleHog, PM4Py, igraph, Raphtory) | BL-21, BL-22 | 02-TECHNOLOGY-REGISTRY §3 | 4 5 5 5 4 5 2 −0.0 | 4.5 | **P0** (forced) | stable | Legal review decides; registry only records triggers |
| GAP-08 | Egress vault uses an unauthenticated XOR keystream cipher | CAP-51 | Security | High | Proven: egress/vault.py (C19-vault-openbao STR-vo-01; 01a BL-45) | BL-45 | C19-vault-openbao STR-vo-01 | 4 4 5 5 4 5 1 −0.0 | 4.25 | **P0** (forced) | stable | — |
| GAP-36 | Local model runtime pinned to an old, root, unauthenticated Ollama | CAP-61 | Security + Operability | High | Proven: compose pins ollama:0.12.3 running as root without auth (C09-ollama INV-ollama-01) | — | C09-llama-cpp STR-llcpp-01 | 4 4 5 5 4 5 1 −0.0 | 4.25 | **P0** (forced) | stable | — |
| GAP-09 | MCP surface authenticates one shared bearer token; tools unannotated | CAP-59 | Security | Critical | Proven: apps/mcp/main.py:220-223 (C09-mcp INV-mcp-02); in-process EOIPMCPServer not mounted (01a BL-47) | BL-47 | C09-mcp INV-mcp-01, INV-mcp-02; C08-neo4j-graphrag STR-n4gr-02 | 5 5 5 5 3 4 3 −0.5 | 4.1 | **P0** (forced) | stable | — |
| GAP-01 | Backend adapters unproven live; known adapter defects | CAP-01 | Quality (live parity unproven) | High | Proven by code reading: JanusGraph writes `p_`-prefixed keys but reads unprefixed (C01-janusgraph INV-janusgraph-01); Neptune adapter has no SigV4 and filters labels after LIMIT (C01-amazon-neptune); HugeGraph template forces Groovy closures (C12-tinkerpop INV-tinkerpop-02); no live runs (U-01) | BL-01..05, U-01, U-03 | C01-janusgraph, C01-amazon-neptune, C12-tinkerpop | 5 5 5 4 3 4 1 −0.5 | 3.85 | **P0** (forced) | stable | Defect severity depends on live behaviour |
| GAP-07 | Epistemic planes not enforced store-wide | CAP-43 | Differentiator | High | Proven: PROPOSED-until-promoted contract exists (ai/boundary.py) but is not a storage-level plane on every backend | BL-40 | C08-letta INV-letta-01, C08-openspg-kag STR-openspg-kag-02, C11-pyg INV-pyg-01 | 5 5 4 4 3 3 5 −0.5 | 3.8 | **P0** (forced) | stable | — |
| GAP-43 | No unified evaluation harness with regression gates | CAP-78 | Quality | High | Proven: deterministic RAG eval only | — | C20-ldbc, C20-beir, C20-ragas INV-ragas-01, C20-graphrag-bench | 4 5 4 4 4 4 2 −0.5 | 3.6 | **P0** (forced) | stable | Needed to prove every claim |
| GAP-02 | Source-ACL enforcement not applied on deployed retrieval, answer, memory, export and MCP paths | CAP-46 | Security | Critical | Proven: filter called in one branch of retrieve() only when scope passed; no deployed caller passes it; keyword/vector/hybrid stages filter by tenant only (01a BL-18); Obsidian exporter has no ACL (C17-obsidian INV-obsidian-01); MCP single token (C09-mcp INV-mcp-02) | BL-17, BL-18, NB-17 | C07-onyx STR-onyx-01, C10-opensearch STR-opensearch-01, C10-pgvector STR-pgvector-01, C19-rebac STR-rebac-01, C15-sourcegraph STR-sourcegraph-02 | 5 5 5 5 3 3 4 −1.0 | 3.55 | **P0** (forced) | stable | Leak paths beyond those found may exist (U-04) |
| GAP-03 | Tenant isolation not enforced in graph adapters, caches, logs or memory | CAP-47 | Security | Critical | Proven: 0 tenant handling in graph adapters at HEAD (01a BL-20); isolation placement is a contract ('external gate') | BL-20 | C01-falkordb STR-falkordb-02, C10-weaviate STR-weaviate-01, C01-apache-age STR-age-01, C01-amazon-neptune INV-amazon-neptune-02 | 5 5 5 5 3 3 3 −1.0 | 3.5 | **P0** (forced) | stable | Per-backend isolation primitive differs (graph space / multi-db / cluster) |
| GAP-34 | Agent memory lacks ACL, tenant, evidence and validity fields | CAP-57 | Security + Partial | High | Proven: MemoryEntry fields (C08-cognee; C08-mem0) | BL-40 | C08-cognee STR-cognee-02, C08-graphiti-zep, C08-letta STR-letta-02 | 4 4 5 4 3 3 4 −0.5 | 3.45 | **P0** (forced) | stable | — |
| GAP-05 | String-built Gremlin and regex-only injection defences | CAP-13, CAP-49 | Security; Security + Interoperability | High | Proven by code reading: labels/keys spliced into scripts (adapters/janusgraph.py:192,276; hugegraph.py:525-551); regex firewall (C09-guardrails INV-grd-01) | BL-02, BL-05, BL-48 | C12-tinkerpop INV-tinkerpop-01, C09-guardrails STR-grd-01 | 4 4 5 4 3 4 1 −0.5 | 3.4 | **P0** (forced) | stable | Exploitability depends on key provenance (not traced) |
| GAP-42 | Restore drills not run | CAP-74 | Operability | High | Proven: scripts only (BL-50) | BL-50 | C01-neo4j, C01-apache-hugegraph | 4 4 5 4 4 4 1 −0.0 | 4.0 | **P1** | stable | — |
| GAP-44 | No SBOM/signing pipeline; scanners unpinned | CAP-79 | Security | High | Proven: sbom.py library-only (01a NB-14); Trivy 2026 compromise (C19-supply-chain INV-sc-01) | NB-14 | C19-supply-chain | 4 4 5 4 4 4 1 −0.0 | 4.0 | **P1** | stable | — |
| GAP-11 | SHACL conformance unproven | CAP-10 | Quality | High | Proven: W3C test suite not run (01a BL-29, U-07) | BL-29 | C03-pyshacl STR-pyshacl-01, C20-tier-c shacl-test-suites | 3 4 3 5 5 5 1 −0.0 | 3.8 | **P1** | stable | — |
| GAP-21 | Air-gapped install unverified; Neptune cannot be air-gapped | CAP-50 | Operability | High | Proven: no air-gap install run; Neptune cloud-only (C01-amazon-neptune) | BL-22, BL-50 | C01-amazon-neptune, C09-ollama | 5 5 4 4 3 3 4 −0.5 | 3.75 | **P1** | stable | — |
| GAP-46 | No persistent vector/full-text engine; hashing embedder default | CAP-53, CAP-54 | Partial; Performance | High | Proven: in-memory indexes only, incl. hybrid_vector_service (C10 cohort; 01a BL-14) | BL-13, BL-14 | C10-lancedb STR-lancedb-01, C10-qdrant STR-qdrant-01, C09-local-embeddings STR-emb-01 | 5 4 3 5 4 4 2 −0.5 | 3.65 | **P1** | stable | — |
| GAP-10 | PII detection narrow; no secret scanning at ingest; raw values retained | CAP-33 | Security | High | Proven: privacy/scanner.py 5 regex types, keeps raw_value; dlp only on egress (C05-presidio STR-pres-01, C05-secret-scanners STR-sec-01) | BL-46 | C05-presidio, C05-secret-scanners | 4 4 5 4 4 4 1 −0.5 | 3.5 | **P1** | stable | — |
| GAP-30 | One-node sizing profiles unmeasured | CAP-04 | Operability | Medium | Proven: no sizing evidence | BL-01 | C01-arcadedb, C01-kuzu | 4 4 3 3 3 4 2 −0.0 | 3.5 | **P1** | stable | — |
| GAP-40 | Digital-thread journeys J1/J9/J10 untested end to end | CAP-69 | Differentiator | High | Proven: no journey test | BL-42 | C15-sourcegraph, C07-servicenow-kg | 5 5 3 3 3 3 5 −0.5 | 3.5 | **P1** | stable | — |
| GAP-15 | Claims and contradictions held in memory only | CAP-25, CAP-39 | Partial | High | Proven: in-memory TruthStore (01a BL-39) | BL-39 | C17-wikidata STR-wikidata-01, C17-scite STR-scite-01, C08-graphiti-zep | 4 4 4 4 3 3 4 −0.5 | 3.3 | **P1** | CV-1→P2 | — |
| GAP-14 | Ontology proposal from arbitrary JSON not wired into governance | CAP-28 | Partial → differentiator | High | Proven: induce_schema and inclusion-dependency discovery exist but are not connected to gitops review (C04-schema-inference INV-si-01) | BL-26, BL-27 | C04-schema-inference STR-si-01, INV-si-01 | 4 4 3 4 4 3 4 −0.5 | 3.25 | **P1** | CV-1→P2, ES-1→P2 | — |
| GAP-17 | Ontology/data branches not persisted on Git; governance mostly unmounted | CAP-35, CAP-41 | Partial; Partial → differentiator | High | Proven: OntologyGitOpsWorkflow keeps branches in a dict (C03-topbraid-edg INV-edg-01); governance.py unmounted (01a BL-32) | BL-32, BL-38 | C03-topbraid-edg STR-edg-01, INV-edg-01; C03-linkml; C03-robot-odk STR-robot-01 | 4 4 3 4 4 3 4 −0.5 | 3.25 | **P1** | CV-1→P2, ES-1→P2 | — |
| GAP-20 | Audit trail not tamper-evident | CAP-48 | Security | Medium | Hypothesis: audit events not hash-chained (not verified) | — | C07-palantir-foundry, C07-atlassian-rovo | 3 4 4 2 3 4 2 −0.0 | 3.25 | **P1** | CV-1→P2, ES-1→P2 | U-unknown |
| GAP-28 | No parser-neutral evidence-span anchors for documents | CAP-32 | Partial | Medium | Proven: extraction tools lack char offsets (C05-unstructured INV-unstr-01, C05-gliner INV-gli-01) | BL-41 | C05-docling STR-docl-01 | 4 4 3 4 4 3 4 −0.5 | 3.25 | **P1** | CV-1→P2, ES-1→P2 | — |
| GAP-39 | Code graph is syntactic (2 languages); no compiler-grade symbols | CAP-66 | Partial | High | Proven (BL-42) | BL-42 | C15-scip-lsif STR-scip-lsif-01, C15-tree-sitter STR-tree-sitter-02, C15-sourcegraph INV-sourcegraph-01 | 4 4 3 4 4 3 3 −0.5 | 3.2 | **P1** | CV-1→P2, ES-1→P2 | — |
| GAP-35 | LLM NL-query tier emits raw queries rather than typed plan candidates | CAP-58 | Partial → differentiator | Medium | Proven: optional LLM hook (BL-12); research shows executable-but-wrong queries common (C08-text-to-query INV-t2q-01) | BL-11, BL-12 | C08-text-to-query STR-t2q-01, C20-text2cypher-bench | 4 4 3 4 3 3 4 −0.5 | 3.15 | **P1** | CV-1→P2, ES-1→P2 | — |
| GAP-13 | Identity limited to persons; probabilistic ER is an unintegrated reimplementation | CAP-30, CAP-31 | Partial | High | Proven: identity resolver handles persons only; 'Splink' engine is stdlib reimplementation, not integrated (01a BL-34/36) | BL-34, BL-35, BL-36 | C04-splink, C04-senzing, C04-zingg STR-zingg-01, C04-llm-entity-matching STR-llmem-01, C07-salesforce-data-cloud STR-sf-01 | 5 4 4 4 4 3 2 −1.0 | 3.05 | **P1** (override) | stable | Merge errors are costly — review workflow needed |
| GAP-04 | Portable query IR not on the production path | CAP-20 | Competitive deficit → differentiator | High | Proven: typed AST compiler exists but is not used by deployed routes (01a BL-09); production traversal runs in Python templates | BL-08, BL-09, BL-09a | C12-tinkerpop STR-tinkerpop-01, C08-llamaindex-pgi STR-llamaindex-pgi-01, C08-text-to-query INV-t2q-01 | 4 5 3 4 3 3 5 −1.0 | 2.9 | **P1** (override) | stable | Semantics vary by backend; push-down may fragment |
| GAP-26 | General-enterprise connector breadth and permission sync | CAP-26 | Partial (breadth) | Medium | Proven: connectors are IT-centric (BL-23); permission sync per connector not verified | BL-23 | C07-onyx INV-onyx-01, C07-atlassian-rovo STR-atlassian-rovo-01, C14-debezium INV-debezium-01 | 5 4 3 4 3 2 2 −1.0 | 2.7 | **P1** (override) | stable | — |
| GAP-18 | No dry-run migration with impacted-query analysis and rollback (J4) | CAP-37 | Partial | High | Proven: migration/protocol.py library-only (01a NB-09) | BL-32 | C07-palantir-foundry, C03-robot-odk | 4 4 4 3 3 3 3 −0.5 | 3.1 | **P2** | CV+1→P1, ES+1→P1 | — |
| GAP-25 | Virtualisation builds SQL by string interpolation (latent) | CAP-21 | Security + Partial | Medium | Proven: mapping/virtualization.py rewrite_point_query f-string; no production caller (C04-rml-tools; V12 finding) | BL-51 | C04-ontop STR-ontop-01, C01-puppygraph STR-puppygraph-02 | 3 3 4 5 4 4 2 −0.5 | 3.1 | **P2** | CV+1→P1 | — |
| GAP-41 | Large-graph rendering unmeasured | CAP-70 | UX | Medium | Proven: no FPS evidence (U-09) | BL-54 | C16 cohort | 3 3 2 3 4 4 2 −0.0 | 3.0 | **P2** | CV+1→P1, ES+1→P1 | Do not churn libraries before measurement |
| GAP-23 | OWL reasoning adapters return canned results | CAP-09, CAP-23 | Partial; Quality | Medium | Proven: Openllet/HermiT/Jena adapters canned (01a BL-30) | BL-30 | C03-owl-reasoners INV-owlr-01, C03-protege INV-protege-01 | 3 3 3 5 4 4 1 −0.5 | 2.9 | **P2** | CV+1→P1 | — |
| GAP-06 | Multi-hop queries lack path modes and push-down | CAP-19 | Performance | High | Hypothesis (unmeasured): Python traversal will not meet latency at 1M+ nodes; path semantics not explicit | BL-08, BL-19 | C01-spanner-graph STR-spanner-graph-01, C01-tigergraph STR-tigergraph-01 | 4 4 2 3 3 3 2 −0.5 | 2.75 | **P2** | stable | Needs BM-02 measurement |
| GAP-12 | No typed constraint layer (cardinality/roles/value ranges) at the mutation gateway | CAP-08 | Partial | High | Proven: gate checks labels and required properties only (BL-28) | BL-28 | C01-typedb STR-typedb-01, INV-typedb-01 | 4 4 4 4 3 3 3 −1.0 | 2.75 | **P2** | stable | — |
| GAP-16 | Bitemporal reads unindexed and untested against an oracle | CAP-34 | Differentiator (verify) | Medium | Hypothesis: reconstruction from revision vertices will be slow and edge cases untested | BL-37 | C13-xtdb STR-xtdb-01, C13-event-sourcing INV-event-sourcing-01 | 3 4 3 3 3 3 3 −0.5 | 2.7 | **P2** | CV-1→P3 | Needs BM-11 |
| GAP-29 | No OpenLineage interoperability | CAP-40 | Interoperability | Low | Proven: mapper scaffolding only (future_scope.py:622) | — | C13-openlineage-marquez STR-openlineage-01 | 2 3 1 4 4 4 1 −0.0 | 2.7 | **P2** | CV-1→P3 | — |
| GAP-33 | GraphRAG layers not benchmarked against strong RAG; summaries not ACL-scoped | CAP-56 | Research gap | Medium | Proven: no comparative benchmark; community layer library-only (01a BL-16); competitors lack ACL (C08-microsoft-graphrag INV-msgraphrag-02) | BL-16 | C08-hipporag STR-hipporag-01, C08-raptor INV-raptor-01, C20-graphrag-bench | 4 4 3 4 3 3 3 −1.0 | 2.6 | **P2** | CV-1→P3, ES-1→P3 | Graph gains are workload-specific |
| GAP-37 | Algorithms pure Python; no fast engine port | CAP-62 | Performance | Medium | Proven for code; performance hypothesis | BL-43, NB-01 | C12-rustworkx STR-rustworkx-01, C12-graphblas STR-graphblas-01, C12-networkx STR-networkx-01 | 3 3 2 4 4 4 1 −0.5 | 2.6 | **P2** | CV-1→P3, ES-1→P3 | — |
| GAP-31 | Bulk-load path bypass risk and unmeasured throughput | CAP-06 | Performance | Medium | Hypothesis | BL-01 | C01-apache-hugegraph, C01-neo4j | 3 3 3 3 4 3 1 −0.5 | 2.5 | **P2** | CV-1→P3, ES-1→P3 | — |
| GAP-32 | No supernode controls | CAP-07 | Performance | Medium | Hypothesis | — | C01-janusgraph STR-janusgraph-04 | 3 3 3 3 3 3 2 −0.5 | 2.45 | **P3** | CV+1→P2, ES+1→P2 | — |
| GAP-24 | SPARQL endpoint not mounted; LPG↔RDF loss unmeasured | CAP-02, CAP-15 | Interoperability; Partial | Medium | Proven: SparqlProtocolHandler has no route (01a BL-06a) | BL-06, BL-06a, BL-31 | C02-apache-jena STR-jena-01, C02-oxigraph STR-oxigraph-01, C18-rdf | 2 3 2 4 4 4 2 −0.5 | 2.4 | **P3** | CV+1→P2, ES+1→P2 | — |
| GAP-27 | Mapping not RML-conformant | CAP-29 | Interoperability | Low | Proven: CML IR; RML test cases not run (BL-33) | BL-33 | C04-rml-tools STR-rml-01, INV-rml-01 | 2 3 1 4 4 4 1 −0.5 | 2.2 | **P3** | stable | — |
| GAP-45 | Wisdom/decision layer library-only; no process-event import | CAP-80 | Research gap → differentiator | Medium | Proven (01a BL-56) | BL-56 | C07-process-mining STR-pm-01, INV-pm-01 | 3 4 2 3 3 3 4 −1.0 | 2.1 | **P3** | stable | Scope must be defined |
| GAP-38 | Neural tier not executable (torch absent); no calibration | CAP-64 | Research gap | Medium | Proven (01a BL-44/57) | BL-44, BL-57 | C11-pyg STR-pyg-01, INV-pyg-01; C11-relbench INV-relbench-01 | 2 3 2 4 4 3 2 −1.0 | 1.8 | **P3** | stable | Must beat tabular baseline |
| GAP-22 | No incremental rule materialisation | CAP-22 | Missing | Medium | Proven: no Datalog engine (BL-30) | BL-30 | C02-rdfox STR-rdfox-01, INV-rdfox-01; C02-ontotext-graphdb INV-graphdb-01 | 3 3 2 4 3 2 3 −1.5 | 1.4 | **P3** | stable | Research |

## 2. Linked strength and inversion cards

Cards are defined in the deep dives and collected in `08-STRENGTH-ADOPTION-REGISTER.md` and `09-CON-TO-PRO-INVERSION-REGISTER.md`. Card IDs cited per gap:

- **GAP-08** → STR-vo-01
- **GAP-36** → STR-llcpp-01
- **GAP-09** → INV-mcp-01, INV-mcp-02, STR-n4gr-02
- **GAP-07** → INV-letta-01, INV-pyg-01, STR-openspg-kag-02
- **GAP-43** → INV-ragas-01
- **GAP-02** → STR-onyx-01, STR-opensearch-01, STR-pgvector-01, STR-rebac-01, STR-sourcegraph-02
- **GAP-03** → INV-amazon-neptune-02, STR-age-01, STR-falkordb-02, STR-weaviate-01
- **GAP-34** → STR-cognee-02, STR-letta-02
- **GAP-05** → INV-tinkerpop-01, STR-grd-01
- **GAP-11** → STR-pyshacl-01
- **GAP-46** → STR-emb-01, STR-lancedb-01, STR-qdrant-01
- **GAP-15** → STR-scite-01, STR-wikidata-01
- **GAP-14** → INV-si-01, STR-si-01
- **GAP-17** → INV-edg-01, STR-edg-01, STR-robot-01
- **GAP-28** → STR-docl-01
- **GAP-39** → INV-sourcegraph-01, STR-scip-lsif-01, STR-tree-sitter-02
- **GAP-35** → STR-t2q-01
- **GAP-13** → STR-llmem-01, STR-sf-01, STR-zingg-01
- **GAP-04** → INV-t2q-01, STR-llamaindex-pgi-01, STR-tinkerpop-01
- **GAP-26** → INV-debezium-01, INV-onyx-01, STR-atlassian-rovo-01
- **GAP-25** → STR-ontop-01, STR-puppygraph-02
- **GAP-23** → INV-owlr-01, INV-protege-01
- **GAP-06** → STR-spanner-graph-01, STR-tigergraph-01
- **GAP-12** → INV-typedb-01, STR-typedb-01
- **GAP-16** → INV-event-sourcing-01, STR-xtdb-01
- **GAP-29** → STR-openlineage-01
- **GAP-33** → INV-raptor-01, STR-hipporag-01
- **GAP-37** → STR-graphblas-01, STR-networkx-01, STR-rustworkx-01
- **GAP-32** → STR-janusgraph-04
- **GAP-24** → STR-jena-01, STR-oxigraph-01
- **GAP-27** → INV-rml-01, STR-rml-01
- **GAP-45** → INV-pm-01, STR-pm-01
- **GAP-38** → INV-pyg-01, INV-relbench-01, STR-pyg-01
- **GAP-22** → INV-graphdb-01, INV-rdfox-01, STR-rdfox-01

## 3. Self-inversion summary (our own weaknesses)

Every P0 gap above is a verified weakness of EOIP and receives a self-inversion card (INV-SELF-NN) in `09-CON-TO-PRO-INVERSION-REGISTER.md` §3.

## 4. Notes

- 'Available upstream / not integrated' applies to: HugeGraph graph spaces and auth (GAP-03), HugeGraph Computer/Vermeer and Neo4j GDS (GAP-37), backend-native vector indexes (GAP-46), Neptune Streams (GAP-26). These are integration gaps, not missing engines.
- Gap scores are judgements; the sensitivity column shows which priorities would change if the customer-value or evidence-strength judgement moved by one point.
- PROVISIONAL rows depend on unresolved baseline uncertainties (U-IDs in `01a-BASELINE-DELTA-HEAD.md`).
