# 19 — Traceability Matrix

| Field | Value |
|---|---|
| Document | 19-TRACEABILITY-MATRIX.md |
| Traceability Chain | Source -> Competitor -> GAP/STR/INV -> REQ-ID -> ADR -> Roadmap WP -> Test -> Metric |
| Quality Gate | 100% End-to-End Traceability with Zero Orphaned Requirements |
| Verification Cutoff | 2026-10-18 UTC |

---

## Complete Traceability Matrix

| Source Baseline | Competitor Technology | GAP / STR / INV | REQ-ID | Architecture ADR | Roadmap WP | Test Reference | Success Metric |
|---|---|---|---|---|---|---|---|
| `BL-18` | **GraphDB / Stardog** | `GAP-01 / INV-01` | `REQ-SEC-01` | `ADR-KG3-03` | `WP-KG3-01` | `tests/security/test_derivation_acl_filtering.py` | **0.00% permission leak on J5** |
| `BL-20` | **AWS Neptune** | `GAP-07 / INV-SELF-02` | `REQ-SEC-03` | `ADR-KG3-04` | `WP-KG3-02` | `tests/tenancy/test_multi_tenant_isolation.py` | **0.00% cross-tenant leak on J13** |
| `BL-09` | **Universal Transpiler** | `GAP-04 / INV-SELF-03` | `REQ-QRY-01` | `ADR-KG3-01` | `WP-KG3-03` | `tests/query/test_query_ast_compilers.py` | **100% pass on J14 multi-backend** |
| `BL-36` | **Senzing** | `GAP-03 / STR-07` | `REQ-ING-02` | `ADR-KG3-08` | `WP-KG3-04` | `tests/identity/test_splink_probabilistic_er.py` | **F1 >= 0.95 on deduplication** |
| `BL-29` | **TopBraid EDG** | `GAP-02 / INV-05` | `REQ-ONT-02` | `ADR-KG3-05` | `WP-KG3-05` | `tests/semantic/test_shacl_w3c_conformance.py` | **100% W3C SHACL Core pass** |
| `BL-32` | **Protégé** | `STR-05 / INV-02` | `REQ-ONT-01` | `ADR-KG3-05` | `WP-KG3-06` | `tests/ontology/test_gitops_lifecycle.py` | **Zero data loss on J4 rollback** |
| `BL-16` | **Microsoft GraphRAG** | `GAP-05 / STR-11` | `REQ-RAG-01` | `ADR-KG3-07` | `WP-KG3-07` | `tests/retrieval/test_hipporag_diffusion.py` | **nDCG@10 >= 0.82 on MuSiQue** |
| `BL-23` | **Palantir Foundry** | `STR-08 / INV-06` | `REQ-ING-01` | `ADR-KG3-09` | `WP-KG3-08` | `tests/connectors/test_source_event_queue.py` | **Idempotent writeback verified** |
| `BL-51` | **Ontop** | `GAP-09 / STR-06` | `REQ-QRY-01` | `ADR-KG3-01` | `WP-KG3-09` | `tests/federation/test_ontop_sql_rewriting.py` | **Self-join elimination active** |
| `BL-54` | **Cytoscape / Sigma** | `GAP-10 / STR-15` | `REQ-UIX-01` | `ADR-KG3-10` | `WP-KG3-10` | `apps/web/tests/gui-foundations.spec.js` | **>= 55 FPS on 100k nodes** |
| `BL-44` | **PyTorch Geometric** | `GAP-08 / STR-02` | `REQ-WIS-01` | `ADR-KG3-11` | `WP-KG3-11` | `tests/neural/test_antistub.py` | **All 4 anti-stub probes PASS** |
| `BL-56` | **Wisdom Graph** | `CAP-80` | `REQ-WIS-01` | `ADR-KG3-12` | `WP-KG3-12` | `tests/wisdom/test_wisdom_lifecycle.py` | **ADR & risk hotspot mining verified** |