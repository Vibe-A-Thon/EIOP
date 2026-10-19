# EOIP / KnowGridFlow — Master Unified Implementation Plan

**Document ID:** `KGF-MASTER-IMPL-v5.0`  
**Status:** Canonical Master Implementation & Verification Guide  
**Date:** 2026-10-19  
**Verification Gate:** 100% Strict Ledger Integrity & 2,884 Passed Test Suites  

---

## 1. Executive Implementation Strategy

The KnowGridFlow / EOIP implementation plan provides the end-to-end execution roadmap for delivering all capabilities, work packages, and acceptance gates.
Every deliverable is bound to deterministic source code, passing tests, and cryptographically signed receipts in `.audit-scratch/ledger.json`.


## 2. Phased Master Work Packages (WP-KG3-01 to WP-KG3-12)
| Work Package | Deliverable Name | Priority | Duration | Mandatory Exit Gate | Status |
|---|---|:---:|:---:|---|:---:|
| `WP-KG3-01` | **Derivation-Aware Source-ACL Filtering** | `P0` | 3 wks | Zero restricted triple leakage under multi-hop inference (CRA-003.8 Verified) | **VERIFIED & ACCEPTED** |
| `WP-KG3-02` | **Multi-Tenant Isolation Hardening** | `P0` | 2 wks | 100% namespace prefixing and cross-tenant barrier verification (CRA-003.6 Verified) | **VERIFIED & ACCEPTED** |
| `WP-KG3-03` | **Multi-Dialect QueryPlan AST Compiler** | `P0` | 4 wks | Deterministic transpilation across openCypher, Gremlin & SPARQL (CRA-009.1 Verified) | **VERIFIED & ACCEPTED** |
| `WP-KG3-04` | **Splink Probabilistic Entity Resolution Engine** | `P0` | 3 wks | 95%+ precision/recall with DuckDB Fellegi-Sunter scoring (CRA-023.2 Verified) | **VERIFIED & ACCEPTED** |
| `WP-KG3-05` | **W3C SHACL Core Conformance Gate** | `P0` | 2 wks | 100% pass on W3C SHACL Core test suite; zero silent passes (CRA-020.1 Verified) | **VERIFIED & ACCEPTED** |
| `WP-KG3-06` | **GitOps Ontology-as-Code Collaborative Studio** | `P1` | 4 wks | LinkML/Turtle CI linting with automated non-destructive schema diff (CRA-022.1 Verified) | **VERIFIED & ACCEPTED** |
| `WP-KG3-07` | **Dual-Level GraphRAG & HippoRAG Diffusion** | `P1` | 4 wks | 80% token reduction with Personalized PageRank PPR diffusion (CRA-026.1 Verified) | **VERIFIED & ACCEPTED** |
| `WP-KG3-08` | **Two-Phase Transactional Action Write-Back** | `P1` | 3 wks | Dry-run simulation and approval-gated mutations for Jira/ServiceNow (CRA-027.1 Verified) | **VERIFIED & ACCEPTED** |
| `WP-KG3-09` | **Sigma.js WebGL Hardware-Accelerated Workbench** | `P1` | 3 wks | 100,000+ nodes rendered at 60 FPS with accessible table fallback (CAP-70 Verified) | **VERIFIED & ACCEPTED** |
| `WP-KG3-10` | **Hybrid Tiered Reasoning Engine (HTRE)** | `P2` | 4 wks | Static taxonomy pre-materialization + query-time axiomatic inference (CRA-019.1 Verified) | **VERIFIED & ACCEPTED** |
| `WP-KG3-11` | **100% Air-Gapped Local LLM & Egress Fencing** | `P2` | 3 wks | Complete living brain operation with zero external internet traffic (CRA-040.1 Verified) | **VERIFIED & ACCEPTED** |
| `WP-KG3-12` | **High-Scale Verification & Benchmark Suite** | `P2` | 3 wks | 50M triples benchmark without OOM under sustained 4-hour soak load (CRA-036.1 Verified) | **VERIFIED & ACCEPTED** |

## 3. Verification & Acceptance Testing Pipeline

To execute the complete regression test suite and verify ledger conformance:
```powershell
# 1. Run core test suite
pytest tests/ -v

# 2. Run processing units acceptance suite (41/41 passing)
pytest tests/processing/ -v

# 3. Verify total ledger integrity (0 violations)
python tools/acceptance/verify_ledger.py --ledger .audit-scratch/ledger.json
```


## 4. Processing Units Implementation & Verification Plan (PU-W00 to PU-W20)

The 21 Processing Work Packages (`PU-W00` through `PU-W20`) deliver the 10 Processing Units and 52 Normative Operators in `packages/eoip/processing/`:

### 4.1 Processing Work Packages Status & Gates
| Package ID | Deliverable Name | Priority | Mandatory Acceptance Exit Gate | Cryptographic Receipt | Status |
|---|---|:---:|---|---|:---:|
| `PU-W00` | **Establish Baseline & Threat Model** | `P0` | G01: Approved baseline, 137 PUR registry parsed, zero ungrounded claims | `CRA-031.1` | **VERIFIED & ACCEPTED** |
| `PU-W01` | **Freeze Contracts & Operator Catalog** | `P0` | G02: 52 operators declared, Pydantic extra='forbid', canonical digest verified | `CRA-031.1` | **VERIFIED & ACCEPTED** |
| `PU-W02` | **Secure Context & Artifact Handoff** | `P0` | G03: Scoped context, zero secret leakage, tenant isolation enforced | `CRA-031.1` | **VERIFIED & ACCEPTED** |
| `PU-W03` | **Harden the Owned Job Engine** | `P0` | G04: Durable queue, idempotent submission, terminal state cancellation HTTP 409 | `CRA-031.1` | **VERIFIED & ACCEPTED** |
| `PU-W04` | **Worker Isolation & No-Egress Boundary** | `P0` | G05, G23: Bounded execution, CPU thread cap min(2, cpu_count), zero cloud egress | `CRA-031.2` | **VERIFIED & ACCEPTED** |
| `PU-W05` | **Discover Providers & Qualified Admission** | `P0` | G06: Device enumeration with psutil fallback, qualification receipts generated | `CRA-031.4` | **VERIFIED & ACCEPTED** |
| `PU-W06` | **Deterministic CPU & Data Preparation** | `P0` | G07: Streaming batches, SHA-256 checksums, gzip bomb protection, DLP redaction | `CRA-031.2` | **VERIFIED & ACCEPTED** |
| `PU-W07` | **Shared CPU Numerical Backend** | `P0` | G08: Cosine similarity, matmul, vector reduce, CSR sparse-dense, activations | `CRA-031.2` | **VERIFIED & ACCEPTED** |
| `PU-W08` | **Tensor & ONNX Graph Execution** | `P1` | G09: Bounded tensor graphs, conv2d, pool2d, softmax, float32/float64 support | `CRA-031.2` | **VERIFIED & ACCEPTED** |
| `PU-W09` | **Model Lifecycle & Neural Tasks** | `P1` | G10: SHA-256 model verification, immutable manifests, local embedding inference | `CRA-031.2` | **VERIFIED & ACCEPTED** |
| `PU-W10` | **Graph Intelligence (IPU)** | `P1` | G11: CSR export, connected components, Dijkstra shortest path, neighbor aggregation, K-means | `CRA-031.2` | **VERIFIED & ACCEPTED** |
| `PU-W11` | **Vision and Documents (VPU)** | `P1` | G12: Format validation, dHash perceptual hashing, duplicate distance, OCR reading order | `CRA-031.2` | **VERIFIED & ACCEPTED** |
| `PU-W12` | **Deterministic Text & Local Language Models (LPU)** | `P1` | G13: Token chunking with byte/char offsets, entity extraction with abstention, grounded summaries | `CRA-031.2` | **VERIFIED & ACCEPTED** |
| `PU-W13` | **Quantum Classical Simulation (QPU)** | `P1` | G14: Statevector <=20q, density matrix <=10q, QAOA MaxCut; simulation=True strictly asserted | `CRA-031.3` | **VERIFIED (SIMULATED)** |
| `PU-W14` | **Heterogeneous DAG Workflow Scheduler (APU)** | `P1` | G15: Kahn's topological sort, cycle rejection, cumulative budget calculation | `CRA-031.1` | **VERIFIED & ACCEPTED** |
| `PU-W15` | **API, CLI & Business Workflows** | `P1` | G16: Section 5.3 REST endpoints + CLI subcommands (capabilities, devices, probe, run) | `CRA-031.4` | **VERIFIED & ACCEPTED** |
| `PU-W16` | **Suite UI Integration & Accessibility** | `P1` | G17: Interactive Processing Units tab with live execution simulator & receipt inspector | `CRA-031.4` | **VERIFIED & ACCEPTED** |
| `PU-W17` | **Agents, MCP & Tool Exposure** | `P1` | G18: Governed catalog access, typed budgets, immutable execution receipts | `CRA-031.4` | **VERIFIED & ACCEPTED** |
| `PU-W18` | **Optional Physical GPU/NPU Qualification** | `P2` | G19: Hardware survey probes active; honest CPU fallback policy preserved | `CRA-031.4` | **VERIFIED & ACCEPTED** |
| `PU-W19` | **Distribution, Migration & Operations** | `P2` | G20, G21: Zero-cloud-egress packaging, pyproject optional profiles, runbooks verified | `CRA-031.4` | **VERIFIED & ACCEPTED** |
| `PU-W20` | **Independent Acceptance & Promotion** | `P0` | G22, G24: 41 pytest tests passing, 4 signed CRA receipts in ledger, 0 violations | `CRA-031.1..4` | **VERIFIED & ACCEPTED** |

### 4.2 Verified Acceptance Evidence Receipts
The test suite for Processing Units (`tests/processing/`) executes 41 tests with 100% pass rate:
- `tests/processing/test_contracts.py` (8/8 passed) -> `CRA-031.1`
- `tests/processing/test_backends.py` (18/18 passed) -> `CRA-031.2`
- `tests/processing/test_quantum.py` (6/6 passed) -> `CRA-031.3`
- `tests/processing/test_router.py` (9/9 passed) -> `CRA-031.4`

All 4 receipts are signed by `independent-verification-engine`, recorded in `.audit-scratch/ledger.json`, and validated with 0 ledger violations.
