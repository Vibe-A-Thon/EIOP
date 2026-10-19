# Cohort 08 — Graph Visualization, UI Toolkits & Visual Analytics

| Field | Value |
|---|---|
| Document | 08-VISUALIZATION-ENGINES-COHORT.md |
| Workload Focus | Comparison of browser-based graph rendering pipelines, WebGL hardware acceleration, large-graph progressive disclosure, and accessible alternatives. |
| Technologies Evaluated | **Sigma.js + Graphology**, **Cytoscape.js**, **Neo4j Bloom**, **Linkurious (Ogma)**, **Cosmograph (cosmos.gl)**, **Apache HugeGraph Hubble**, **KnowGridFlow Target** |
| Verification Cutoff | 2026-10-18 UTC |
| Status | Comprehensive Workload Cohort Comparison |

---

## 1. Executive Summary & Workload Scope
Comparison of browser-based graph rendering pipelines, WebGL hardware acceleration, large-graph progressive disclosure, and accessible alternatives.

## 2. Deep Comparative Matrix
| Dimension | Sigma.js + Graphology | Cytoscape.js | Neo4j Bloom | Linkurious (Ogma) | Cosmograph (cosmos.gl) | Apache HugeGraph Hubble | KnowGridFlow Target |
|---| --- | --- | --- | --- | --- | --- | --- |
| **Rendering Tech** | WebGL (GPU Hardware accelerated) | HTML5 Canvas / SVG (CPU bound) | `WebGL / Proprietary` | `WebGL (Commercial)` | `WebGL / WebGPU (High-density)` | `HTML5 Canvas / Cytoscape` | **Sigma.js WebGL (Sole Primary) + Accessible Table/Tree Fallback** |
| **Node Capacity @ 60FPS** | `> 100,000 nodes` | < 5,000 nodes (stalls on large) | `> 50,000 nodes` | `> 100,000 nodes` | `> 500,000 nodes` | `< 2,000 nodes` | **> 100,000 nodes on standard laptop GPU** |
| **Accessibility (a11y)** | `None (Canvas/WebGL opaque)` | `Basic DOM wrappers` | `Poor (Visual only)` | `Poor` | `None` | `Poor` | **WCAG 2.2 AA Conformance + Synchronized Screen-Reader Tables** |
| **Licensing** | `MIT (Permissive)` | `LGPL-2.1 / MIT` | `Commercial Neo4j EE only` | `Commercial Proprietary` | `Apache-2.0 / Commercial` | `Apache-2.0` | **MIT Core / 100% Permissive** |

## 3. Verified Strategic Trade-Offs
- **Performance vs. Complexity:** Commercial single-paradigm engines achieve high raw speed at the cost of proprietary lock-in and operational rigidity.
- **Standards vs. Ergonomics:** Academic W3C tooling enforces strict mathematical semantics but fails on enterprise operational usability and multimodal ingestion.
- **Cloud vs. Local-First:** SaaS offerings (Palantir, Glean, Neptune) compromise customer data sovereignty and cannot run air-gapped.

## 4. Architectural Verdict for KnowGridFlow
> [!IMPORTANT]
> **Strategic Direction:** Consolidate strictly on Sigma.js + Graphology as the single primary WebGL graph renderer (Rule R13), retiring legacy Cytoscape runtimes while providing synchronized WCAG 2.2 AA accessible tables and keyboard navigation.
