# 15 — Validation & Benchmark Plan (KnowGridFlow / EOIP)

| Field | Value |
|---|---|
| Document | 15-VALIDATION-BENCHMARK-PLAN.md |
| Status | Proposed Reproducible Benchmark Suite (Master Prompt Section 12) |
| Reference Hardware | Reference Node: 16 vCPU AMD EPYC, 64 GB RAM, NVMe SSD (Local-First) |
| Verification Cutoff | 2026-10-18 UTC |

---

## 1. Workload Datasets & Scaled Tiers
All benchmarks shall be evaluated across 3 reproducible data tiers:
1. **Tier 1 (100k Nodes, 500k Edges):** Developer workstation validation.
2. **Tier 2 (1M Nodes, 10M Edges):** Departmental enterprise operational graph.
3. **Tier 3 (10M+ Nodes, 100M Edges):** Full global enterprise digital thread with dense code AST and logs.

**Test Corpora:**
- Synthetic LDBC Social Network Benchmark (Interactive & BI).
- Multi-Hop Question Answering: HotpotQA, 2WikiMultiHopQA, MuSiQue.
- Enterprise Digital Thread: Synthetic Jira -> Git PR -> Commit -> Python AST -> Service trace.

---

## 2. Benchmark Suites & Target Thresholds

| Benchmark ID | Test Description | Target Measure | Threshold / Pass Criteria |
|---|---|---|---|
| `BM-01` | 2-Hop Neighborhood Latency | Latency p50 / p95 | p50 < 8ms, p95 < 25ms on Tier 2 |
| `BM-02` | 4-Hop Path Traversal | Latency p95 | p95 < 150ms on Tier 2 |
| `BM-03` | Streaming Ingestion Throughput | Events / second | > 5,000 SourceEvents/sec sustained |
| `BM-04` | Derivation ACL Verification Overhead | Latency delta | < 10% overhead vs unauthenticated traversal |
| `BM-05` | HippoRAG Multi-Hop Accuracy | nDCG@10 / F1 | > 0.82 nDCG@10 on MuSiQue (beats plain RAG) |
| `BM-06` | Multi-Tenant Isolation Leakage | Security Leak Rate | 0.00% cross-tenant data/index leakage |
| `BM-07` | Sigma.js WebGL FPS on 100k Nodes | Frame Rate | >= 55 FPS sustained during pan/zoom |
| `BM-08` | Point-in-Time Restore Time | Recovery Duration | < 5 minutes for 10M node snapshot |
