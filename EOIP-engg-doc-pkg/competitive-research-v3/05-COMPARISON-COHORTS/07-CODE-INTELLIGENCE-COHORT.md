# Cohort 07 — Code Graphs, Software Catalogs & Repository Intelligence

| Field | Value |
|---|---|
| Document | 07-CODE-INTELLIGENCE-COHORT.md |
| Workload Focus | Analysis of compiler-accurate code graphs, symbol resolution, cross-references, AST extraction, and digital thread tracking. |
| Technologies Evaluated | **Meta Glean (Code)**, **Sourcegraph / Cody**, **Tree-sitter**, **CodeQL (GitHub)**, **Semgrep**, **Backstage Catalog**, **KnowGridFlow Target** |
| Verification Cutoff | 2026-10-18 UTC |
| Status | Comprehensive Workload Cohort Comparison |

---

## 1. Executive Summary & Workload Scope
Analysis of compiler-accurate code graphs, symbol resolution, cross-references, AST extraction, and digital thread tracking.

## 2. Deep Comparative Matrix
| Dimension | Meta Glean (Code) | Sourcegraph / Cody | Tree-sitter | CodeQL (GitHub) | Semgrep | Backstage Catalog | KnowGridFlow Target |
|---| --- | --- | --- | --- | --- | --- | --- |
| **Granularity** | Symbol / Type / Call Graph (Exact) | `Symbol / SCIP LSIF index` | Abstract Syntax Tree (Concrete) | Datalog Predicate Relational AST | `Pattern-based AST matching` | `Service / Component ownership` | **Byte-exact Symbol, Function, Class, AST, Dependency & Digital Thread** |
| **Cross-System Thread** | `Code Only` | `Code + Documentation` | `Syntax Only` | `Code Security Only` | `Code Patterns Only` | `Catalog metadata only` | **Full Thread: Jira Story -> PR -> Commit -> Symbol -> Service -> Incident** |
| **Deployment** | Self-hosted / C++ infrastructure | `Self-hosted / Cloud SaaS` | `Embedded Library` | `Local CLI / GitHub Cloud` | `Local CLI / Cloud` | `Node.js / React Web` | **Pure-Python First + Web-native Sigma WebGL Workbench** |
| **Licensing** | `BSD-3-Clause` | Source-Available / Proprietary | `MIT` | Proprietary (Free for Public Repos) | `LGPL-2.1 / Commercial` | `Apache-2.0` | **Permissive / In-house cleanroom** |

## 3. Verified Strategic Trade-Offs
- **Performance vs. Complexity:** Commercial single-paradigm engines achieve high raw speed at the cost of proprietary lock-in and operational rigidity.
- **Standards vs. Ergonomics:** Academic W3C tooling enforces strict mathematical semantics but fails on enterprise operational usability and multimodal ingestion.
- **Cloud vs. Local-First:** SaaS offerings (Palantir, Glean, Neptune) compromise customer data sovereignty and cannot run air-gapped.

## 4. Architectural Verdict for KnowGridFlow
> [!IMPORTANT]
> **Strategic Direction:** Surpass code-only tools by embedding lossless Python/TypeScript AST extraction into KnowGridFlow's digital thread, enabling root-cause blast radius queries that trace from a Jira user story down to a specific class method and outward to deployed Kubernetes services.
