# Risk Register

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Track delivery, architecture, data, AI, security and operations risks

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

| ID | Risk | Likelihood | Impact | Mitigation / trigger | Phase owner |
|---|---|---:|---:|---|---|
| R-001 | Jira/GitLab real schemas differ from synthetic fixtures | M | H | Configurable mappings + contract tests; remap when actual samples arrive | P1/P2 |
| R-002 | HugeGraph schema/index assumptions do not match pinned release | M | H | Verify against official docs/test container; schema bootstrap integration tests | P0/P1 |
| R-003 | Cross-domain deterministic identifiers are sparse | M | H | Evidence-scored linker; do not fabricate; add approved mapping rules/human confirmation later | P1/P2 |
| R-004 | Tree-sitter static analysis misses dynamic behavior | H | M | Mark unresolved; supplement with language-specific analyzers/runtime evidence only when available | P1+ |
| R-005 | Graph queries become expensive on dense graph | M | H | QueryPlan limits, index benchmarks, edge allowlists, timeout/cancellation | P1+ |
| R-006 | Local model quality/latency varies by workstation | H | M | Core graph functions model-independent; provider abstraction; benchmark profile | P1/P3 |
| R-007 | Prompt injection from code/docs | M | H | untrusted-context handling, read-only tools, plan validation, adversarial tests | P1+ |
| R-008 | Single-node RocksDB lacks HA | H | M in MVP / H production | accepted demo constraint; backup/rebuild; P7 distributed topology if required | P1/P7 |
| R-009 | Backup covers graph but not full app reproducibility | M | H | manifest raw/config/state/model references + restore verification | P1 |
| R-010 | Too many requested AI patterns inflate MVP | H | H | strategy interfaces + phased roadmap; TraceImpactAgent only in P1 | P1 |
| R-011 | Lack of RBAC is mistaken for production-ready multi-user security | M | H | explicit deployment assumption/auth/network warning; P7 RBAC/SSO | P1/P7 |
| R-012 | License incompatibility in parser/UI/model dependencies | M | H | SBOM/license allowlist/review before merge/release | P0+ |
| R-013 | Raw capture contains sensitive fields unnecessarily | M | H | connector field mapping/data minimization/classification/retention | P1+ |
| R-014 | Physical graph partitioning later is costly | L/M | M | canonical IDs/domain tags/versioned APIs; trigger partition only on measured need | P7 |
| R-015 | Self-improving capability bypasses governance | L before P8 | Critical | no implementation path before governance/sandbox/approval/regression/rollback | P8+ |
