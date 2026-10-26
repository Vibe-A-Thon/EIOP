# C08 WhyHow.AI

| Field | Value |
|---|---|
| Registry ID | T-C08-whyhow |
| Tier | B (schema-guided KG for RAG; current status unclear) |
| Versions examined | `whyhow-ai/knowledge-graph-studio` `main` as indexed 2026-08-03 by a third-party docs index; PyPI `whyhow` (old SDK) |
| Verified on | 2026-10-26 |
| Worker | V20 |

## 1. Identity, current status, tier, sources
WhyHow.AI is a startup offering "RAG-native" knowledge graph tooling: an open-source **Knowledge Graph Studio** backend (MongoDB-based, FastAPI), a Python SDK (`whyhow`), and an enterprise cloud-hosted product [CLAIM-why-01, -02]. **Status: NOT PUBLICLY VERIFIED; evidence points to the open-source repos having been removed or made private.** On 2026-10-26: `github.com/whyhow-ai` (organisation page) returned HTTP 404; `git ls-remote` on `knowledge-graph-studio`, `whyhow-ai-sdk`, `rule-based-retrieval` returned "Repository not found"; PyPI JSON for `whyhow` returned Not Found from this host (a web-search snippet earlier showed the PyPI page carrying an "old SDK" warning); the `whyhow.ai` hostname did not resolve from this host [CLAIM-why-03]. Counter-evidence: a third-party index recorded the studio repo's `main` on 2026-08-03 [CLAIM-why-02]. No announcement of acquisition, shutdown or pivot was found in searches. Conclusion: **wound down / withdrawn OSS is likely but unproven (confidence 0.4)**. Do not build on it.

## 2. Problem and workloads
Schema-guided (workspace-level schema, rule-based entity resolution) graph construction from documents, stored as triples with chunk links, queried in natural language, for RAG accuracy [CLAIM-why-02].

## 3. Feature inventory
| Feature | Status |
|---|---|
| Workspace/schema/graph/triple/node/chunk/document/query/rule/task/user collections (11 MongoDB collections) | present (historic, per index) [CLAIM-why-02] |
| Rule-based entity resolution | present (per index) |
| Triples with source-chunk links | present (per index) |
| Chunk embeddings (default dim 1536) | present (per index) |
| Python SDK, admin CLI, Docker | present (historic) |
| NL graph query | present (per index; mechanism UNVERIFIED) |
| Hosted enterprise cloud | proprietary; UNVERIFIED current |
| Source ACL, tenancy | workspace/user model only; ACL propagation absent (UNVERIFIED) |

## 4. Architecture
```
SDK/CLI -> FastAPI routers (workspaces, schemas, graphs, triples, nodes, documents, chunks, queries, rules, tasks)
        -> MongoDB Atlas (11 collections; chunk vectors in Atlas vector search)
LLM calls: extraction against workspace schema; NL query
```

## 5. Under-the-hood reconstruction
Data model: triples (head node, relation, tail node) with graph id, creating user and source chunk ids; schema constrains allowed entities/relations (extraction prompt uses schema; hypothesis for the enforcement mode). Storage: documents in MongoDB; graph traversal is application-side or via aggregation (hypothesis). Pattern worth reusing: **triple-to-chunk provenance with schema-guided extraction and rule-based merge**, which maps to EOIP evidence manifests (BL-41) and the validation gate (BL-28). Concurrency and transactions: those of MongoDB; no graph-native semantics (hypothesis).

## 6. Requirements inferred
Per-workspace schema; deterministic merge rules before any LLM dedupe; every triple carries chunk provenance.

## 7. Performance and resource model
No published benchmarks found; none quoted. MongoDB Atlas dependency implies a cloud service for vectors in the documented setup (Atlas) [CLAIM-why-02]; self-host with community MongoDB loses Atlas vector search (hypothesis).

## 8. Strengths
Rule-based, schema-first construction with chunk-level provenance. Match through the existing ontology manifest and validation gate. STR below.

## 9. Limitations
Verified: repositories not retrievable on check date (maturity/continuity). Hypotheses: Atlas dependency conflicts with air-gap; MongoDB licensing (SSPL for server) is itself a legal-review trigger if bundled. Users' complaints: none found.

## 10. Deployment and licensing
Repository licence not stated by the sources reached: **UNVERIFIED**. Atlas-based setup is cloud-first (CLAIM-why-02); air-gap viability: partial/unknown. Hosted product proprietary.

## 11. Delta vs EOIP baseline
EOIP already has schema-guided ontology promotion (BL-27), validation gate (BL-28), evidence manifests (BL-41) and CML mapping (BL-33); it lacks LLM unstructured extraction (BL-26 covers JSON, not text). WhyHow adds nothing EOIP cannot build; its value is as a design reference.

## 12. Cards
| ID | Card |
|---|---|
| STR-whyhow-01 | Schema-first extraction with rule-based merge and triple-to-chunk links; evidence CLAIM-why-02; value: governed text ingestion (CAP-32/CAP-31/CAP-38); **match**; design: extractor emits PROPOSED claims against the ontology manifest, deterministic merge keys before LLM merge, chunk/span evidence on every edge; acceptance: 100% of extracted edges have span evidence and validation-gate verdict |
| INV-whyhow-01 | Vendor/OSS continuity risk (proven for repo availability, hypothesis for cause). Alternative: build on EOIP governed pipeline and generic OSS libs. Options: (1) none, (2) native extractor (selected), (3) differentiated: ACL-inherited extraction. POC: extract 200 docs with local 14B model; success: >=95% edges with valid span provenance. Decision **DEFER** the vendor, **ADOPT** the pattern. No seed hypothesis targets it. |

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-32 unstructured extraction | BUILD (schema-guided), pattern only |
| CAP-31 merge rules | REUSE existing identity rules (BL-34) extended |
| Product itself | REJECT as dependency (status, Atlas) |

## 14. Tests
Re-check repo/org availability monthly; if a fork is later found, verify licence before any code review.

## 15. Risks and open questions
Is the OSS gone intentionally (pivot)? Is there a successor product or fork? Licence of last public release?

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | status unverified |
| D2 | 2 | schema-guided KG for RAG |
| D3 | 4 | FastAPI + MongoDB |
| D4-D5 | 5 | triples, schema (partly hypothesis) |
| D6-D8 | N/A | not publicly evidenced |
| D9 | 5 | extraction only |
| D10 | 5,12 | chunk provenance |
| D11-D12 | N/A | not evidenced |
| D13 | 3 | NL query |
| D14 | 3 | mechanism unverified |
| D15-D17 | 3 | SDK/CLI |
| D18-D19 | 3,9 | unverified |
| D20 | 7 | no data |
| D21 | 10 | OSS + cloud |
| D22 | 9 | MongoDB-coupled |
| D23 | N/A | none found |
| D24 | 1 | low-confidence sources |

## Appendix B. Capability mapping
| CAP | This tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-32 | partial (historic) | why-02 | Absent for text | BUILD | P1 |
| CAP-38 | native | why-02 | BL-41 Implemented | REUSE | P2 |
| CAP-58 | partial | why-02 | BL-12 Partial | DEFER | P3 |

## Appendix C. Evidence records
| CLAIM | Product/version/date | Claim | Class | Source | Dates/conf | Contradiction |
|---|---|---|---|---|---|---|
| why-01 | whyhow SDK | Old SDK; points to upgraded Studio and SDK | Third-party report | pypi.org/project/whyhow (via web search snippet) | acc 2026-10-26; 0.4 | PyPI JSON not found from this host |
| why-02 | studio `main`, 2026-08-03 | MongoDB-based, 11 collections, rule-based ER, triples with chunk links, SDK/CLI/Docker; open-source backend plus enterprise cloud | Third-party report | docsearch.algolia.com/mcp/docs/repo/whyhow-ai/knowledge-graph-studio; dealroom.co listing | indexed 2026-08-03, acc 2026-10-26; 0.6 | repo now 404 |
| why-03 | github org | `github.com/whyhow-ai` and three repos return 404/not found; `whyhow.ai` did not resolve from this host | Reproduced by our check | github.com, git ls-remote | 2026-10-26; 0.6 (DNS may be local) | index shows repo existed Aug 2026 |

## Appendix D. Assumptions
Status conclusion drawn from absence of retrievable artefacts only; no company statement found. Registry action: KEEP as REFERENCE-ONLY with status UNKNOWN.
