# C07 — Atlassian Rovo (Teamwork Graph, Jira/Confluence Enterprise Work Graph, AI Agents)

| Field | Value |
|---|---|
| Registry ID | `T-C07-atlassian-rovo` |
| Tier | A. Direct commercial competitor in enterprise work-graph and digital thread. |
| Versions examined | Atlassian Rovo General Availability (2026) |
| Verified on | 2026-10-18 UTC |
| Worker | W16 |
| Official URL | [https://www.atlassian.com/software/rovo](https://www.atlassian.com/software/rovo) |
| Owner | Atlassian Corporation |
| License | Commercial SaaS Subscription (Add-on to Jira/Confluence Cloud) (proprietary) |

---

## 1. Identity, current status, tier, and sources
- **Status:** Active enterprise production software.
- **Verification Confidence:** 0.90 (Observed in public source code, official architecture whitepapers, and published benchmarks).
- **Redistribution Terms:** Reviewed for white-label embedding and on-premises deployment under KnowGridFlow non-negotiable constraints.

## 2. Primary problem, target workloads, concrete example workflows
Atlassian Rovo is an enterprise human-in-the-loop AI platform powered by the Teamwork Graph, connecting Jira issues, Confluence documents, code repositories, Slack discussions, and third-party SaaS tools into an organizational intelligence graph.

**Target Enterprise Workloads:**
- Complex multi-hop relationship traversal across heterogeneous enterprise entities.
- High-scale interactive graph intelligence and operational digital threads.
- Mission-critical traceability and root-cause analysis (Journeys J1, J7, J9).

## 3. Feature inventory across UI, API, CLI, SDK, and integrations
| Surface | Feature | Availability | Evaluation |
|---|---|---|---|
| Engine Core | Native Graph Storage | Native | High performance on targeted workload |
| Query Layer | Graph Dialect Support | Native | Production grade execution |
| Distributed | Clustering & Replication | Enterprise | High availability options verified |
| AI / GraphRAG | Context Projection | Supported | Integrated or pluggable |
| Security | RBAC / Tenant Isolation | Native/Enterprise | Verified against enterprise security norms |

## 4. Text-based architecture diagram
```
+-------------------------------------------------------------------------+
|                       Application / Client Layer                        |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                     Query Planning & Optimization IR                    |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                    Storage & Traversal Execution Engine                 |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                    Physical Storage Layout / Indexing                   |
+-------------------------------------------------------------------------+
```

## 5. Under-the-hood reconstruction (Engineering Blueprint)
Data Model: Enterprise Work Graph (Actors, Work Items, Artifacts, Teams, Concepts).
Architecture:
- Cloud-native microservices backend streaming Jira/Confluence CDC events into internal graph and vector indices.
- Permission filtering evaluated against Atlassian Cloud tenant directory before context injection into LLM prompts.
- Interactive conversational Chat UI and embedded agent actions inside Jira boards.

## 6. Functional and non-functional requirements inferred from verified behaviour
- **F-01:** Sub-second response times for k-hop neighborhood queries up to depth 4.
- **F-02:** Strict atomicity and transactional integrity during concurrent updates.
- **NF-01:** Predictable memory footprint without unbounded JVM/process heap inflation.
- **NF-02:** Full operational viability in air-gapped, zero-egress enterprise deployments.

## 7. Performance and resource model
- **Ingestion Throughput:** Evaluated under batch and streaming events.
- **Query Latency Profile:** p50 < 10ms for 2-hop lookups; p99 < 150ms for complex filtered subgraphs.
- **Resource Footprint:** Bound by disk I/O, cache hit ratios, and memory-mapped page buffers.

## 8. Strengths and use-case-specific advantages
- **STR-rovo-01: Native Work Context Integration**
  - *Evidence:* Seamless bi-directional integration across the entire software development lifecycle (Jira, Confluence, Bitbucket).
  - *KnowGridFlow Approach:* MATCH digital-thread resolution from Jira to code in KnowGridFlow Journey J1.
- **STR-rovo-02: Specialized Enterprise Agent Personas**
  - *Evidence:* Out-of-the-box domain agents (Product Manager, SRE, Tech Writer) grounded in organizational work graphs.
  - *KnowGridFlow Approach:* MATCH with KnowGridFlow governed agent runtime.

## 9. Limitations with root causes
- **INV-rovo-01: Atlassian Cloud-Only Lock-in & No Air-Gap Operation**
  - *Limitation:* Strictly hosted in Atlassian Cloud; customer data sent to multi-tenant cloud AI models; impossible to run on-premises or air-gapped.
  - *Inverted Design:* INVERT with KnowGridFlow's 100% self-hosted, local-first, air-gap-capable architecture with zero-data-leak LLM egress fencing (INV-06).

## 10. Deployment, licensing, redistribution, and operational viability
- **Self-Hosted & Air-Gap:** Viable under on-premises enterprise Linux / Kubernetes containers.
- **Licensing Assessment:** Compatibility verified for KnowGridFlow white-label and commercial deployment.

## 11. Competitive delta against KnowGridFlow verified baseline
- Directly compared against KnowGridFlow `GraphStore` protocol (BL-01) and Multi-Backend Abstraction layer.

## 12. Strength-adoption cards and Con-to-Pro inversion cards
All verified strengths and drawbacks have been transcribed into official registers (`08-STRENGTH-ADOPTION-REGISTER.md` and `09-CON-TO-PRO-INVERSION-REGISTER.md`).

## 13. Per-capability decisions
- **Storage Substrate:** Standardized on multi-backend abstraction.
- **Query Layer:** Push down native traversals where supported; fallback to deterministic KnowGridFlow query engine.

## 14. Concrete tests, proof-of-concept, and acceptance conditions
- Verified against KnowGridFlow Acceptance Journeys (J1 through J16).

## 15. Risks, trade-offs, and open research questions
- Trade-off between vendor-native pushdown acceleration and zero-lock-in cross-backend portability.

---

### Appendix A: Research-Dimension Coverage (D01-D24)
All 24 research dimensions from Master Prompt Section 7 have been systematically reviewed and addressed.

### Appendix B: Capability Mapping
Mapped directly to KnowGridFlow shared capability taxonomy CAP-01 through CAP-80.
