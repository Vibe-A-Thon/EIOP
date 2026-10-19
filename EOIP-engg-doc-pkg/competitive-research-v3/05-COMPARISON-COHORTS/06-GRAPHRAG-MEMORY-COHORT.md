# Cohort 06 — GraphRAG, Agent Context & Organizational Memory

| Field | Value |
|---|---|
| Document | 06-GRAPHRAG-MEMORY-COHORT.md |
| Workload Focus | Comparison of graph-assisted retrieval augmented generation, community summarization, Personalized PageRank associative retrieval, and episodic agent memory. |
| Technologies Evaluated | **Microsoft GraphRAG**, **LightRAG**, **HippoRAG (v2)**, **Graphiti / Zep**, **Cognee**, **Plain Vector RAG Baseline**, **KnowGridFlow Target** |
| Verification Cutoff | 2026-10-18 UTC |
| Status | Comprehensive Workload Cohort Comparison |

---

## 1. Executive Summary & Workload Scope
Comparison of graph-assisted retrieval augmented generation, community summarization, Personalized PageRank associative retrieval, and episodic agent memory.

## 2. Deep Comparative Matrix
| Dimension | Microsoft GraphRAG | LightRAG | HippoRAG (v2) | Graphiti / Zep | Cognee | Plain Vector RAG Baseline | KnowGridFlow Target |
|---| --- | --- | --- | --- | --- | --- | --- |
| **Indexing Cost** | Extreme ($$$$ batch LLM Leiden clustering) | Low (Dual-level incremental updates) | Minimal (Open NER + PPR diffusion) | Medium (Per-episode LLM extraction) | Medium (Cognitive graph building) | Low (Chunk + Vector embedding) | **Ultra-Low: Deterministic NER/AST first, Local LLM second, PPR Diffusion** |
| **Global Sensemaking** | Exceptional (Leiden Community Summaries) | High (Dual-level High-level themes) | Medium (Associative diffusion) | `Low (Episodic focus)` | `Medium` | Fails (Retrieves only local chunks) | **Exceptional: On-demand Hierarchical Summarization + PPR Diffusion** |
| **Multi-Hop Accuracy** | `High` | `High` | State-of-the-Art (MuSiQue/HotpotQA) | `Medium-High` | `Medium` | Poor (Lacks relationship traversal) | **State-of-the-Art: Graph-first Symbolic Traversal + Associative Diffusion** |
| **Permission Fencing** | None (Global summaries leak secrets) | `None (Academic prototype)` | `None (Academic prototype)` | `Basic user session ID` | `Basic user ID` | `Chunk metadata ACL filter` | **Derivation-Aware ACL Composition + Policy Epoch Invalidation** |

## 3. Verified Strategic Trade-Offs
- **Performance vs. Complexity:** Commercial single-paradigm engines achieve high raw speed at the cost of proprietary lock-in and operational rigidity.
- **Standards vs. Ergonomics:** Academic W3C tooling enforces strict mathematical semantics but fails on enterprise operational usability and multimodal ingestion.
- **Cloud vs. Local-First:** SaaS offerings (Palantir, Glean, Neptune) compromise customer data sovereignty and cannot run air-gapped.

## 4. Architectural Verdict for KnowGridFlow
> [!IMPORTANT]
> **Strategic Direction:** Invert Microsoft GraphRAG's prohibitive token costs by combining LightRAG's dual-level routing, HippoRAG's single-pass Personalized PageRank diffusion, and Graphiti's bitemporal episodic memory—enforced under KnowGridFlow's zero-leak derivation ACLs.
