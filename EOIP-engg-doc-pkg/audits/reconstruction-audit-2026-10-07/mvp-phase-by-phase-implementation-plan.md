# MVP-Oriented Phase-By-Phase Reconstruction Implementation Plan

Generated: 2026-10-07 14:02:13Z

## Purpose

This plan reconstructs the current EOIP / KnowGridFlow project as-is from the consolidated Markdown and audit evidence. It is MVP-oriented: build a working, demonstrable, evidence-backed product first, then layer enterprise maturity without losing traceability.

## Operating Rules

- Preserve source traceability from each requirement to Markdown, implementation, and tests.
- Keep graph storage backend-neutral at the product boundary; use the client-selected graph database through adapters/configuration.
- Prefer runnable Docker/local acceptance gates over document-only claims.
- Treat generated audit JSON completion as a signal, but keep release readiness tied to tests, deployment health, and client acceptance.
- Do not remove duplicated-looking requirements until they are reconciled through a documented decision.

## Source Families Used

| Family | Files | Representative files |
| --- | --- | --- |
| EOIP-engg-doc-pkg | 118 | EOIP-engg-doc-pkg/00-specification-audit-and-enhancements.md, EOIP-engg-doc-pkg/01-project-vision.md, EOIP-engg-doc-pkg/02-scope-and-objectives.md, EOIP-engg-doc-pkg/03-functional-requirements.md, EOIP-engg-doc-pkg/04-non-functional-requirements.md, EOIP-engg-doc-pkg/05-system-requirements.md, EOIP-engg-doc-pkg/06-architecture.md, EOIP-engg-doc-pkg/07-component-architecture.md |
| README.md | 1 | README.md |
| agent_runbook.md | 1 | agent_runbook.md |
| apps | 1 | apps/vscode-extension/README.md |
| checklist.md | 1 | checklist.md |
| context.md | 1 | context.md |
| demo | 11 | demo/autodemo/README.md, demo/autodemo/runtime-validation-report.md, demo/demodata/code/README.md, demo/demodata/core/demo-repo/README.md, demo/demodata/crawler/README.md, demo/demodata/enterprise/README.md, demo/demodata/enterprise/wiki/checkout-latency-runbook.md, demo/demodata/enterprise/wiki/checkout-risk-architecture.md |
| docs | 31 | docs/61-demo-playbook.md, docs/adr-001-g2-contract-and-revision-model.md, docs/agents.md, docs/api-reference.md, docs/application-audit-2026-10-02.md, docs/audit-2026-10-06/assessed-gap-report.md, docs/audit-2026-10-06/detailed-requirements-report.md, docs/audit-2026-10-06/phase-by-phase-implementation-approach.md |
| examples | 4 | examples/demo-enterprise/README.md, examples/demo-enterprise/wiki/checkout-latency-runbook.md, examples/demo-enterprise/wiki/checkout-risk-architecture.md, examples/demo-repo/README.md |
| handoff_template.md | 1 | handoff_template.md |
| instruction.md | 1 | instruction.md |
| memory.md | 1 | memory.md |
| onboarding_checklist.md | 1 | onboarding_checklist.md |
| onboarding_prompts.md | 1 | onboarding_prompts.md |
| roles.md | 1 | roles.md |
| secrets.example | 1 | secrets.example/README.md |
| tickets | 7 | tickets/requirements-map.md, tickets/ticket-20261004-001.md, tickets/ticket-20261004-002.md, tickets/ticket-20261004-003.md, tickets/ticket-20261004-004.md, tickets/ticket-20261004-005.md, tickets/ticket-template.md |
| todo-status.md | 1 | todo-status.md |

## Phase Plan

| Phase | Name | Implementation work | Primary source docs | Exit criteria |
| --- | --- | --- | --- | --- |
| MVP-P0 | Reconstruction Baseline And Evidence Lock | Freeze the source corpus, recreate repository structure, install dependencies, validate config files, preserve generated audit JSONs, and regenerate this requirements baseline. | README.md; EOIP-engg-doc-pkg/DOCUMENTATION-INDEX.md; docs/audit-2026-10-06/*; .tmp/gap-coverage-audit.json; .tmp/g2-coverage-audit.json | All Markdown source files accounted for; dependency lock files install; Docker Desktop available; baseline tests selectable. |
| MVP-P1 | Contracts, Ontology, And Graph Core | Implement source-event contracts, ontology manifest, graph store interface, memory backend, HugeGraph backend, graph schema bootstrap, identity resolution, provenance, temporal records, and backend portability hooks. | EOIP-engg-doc-pkg/09-data-architecture.md through 18-ingestion-architecture.md; 74-data-contracts.md; 76-multi-backend.md; docs/ontology.md; docs/ingestion.md | Schema bootstrap succeeds; graph contract unit tests pass; identity/provenance records round-trip; backend config can select supported adapters. |
| MVP-P2 | Ingestion MVP | Build the core ingestion engine with demo/manual/file/git/code inputs, connector framework, retry/dead-letter behavior, cursoring, and deterministic demo data loading. | EOIP-engg-doc-pkg/19-connector-framework.md through 24-file-web-connectors.md; docs/connectors*.md; docs/file-parsing.md; demo/demodata/**/README.md | Demo ingestion loads graph facts with evidence and can be re-run idempotently; connector tests cover success and failure paths. |
| MVP-P3 | Query, Retrieval, RAG, And Explanation | Implement EOQL/query APIs, traversal controls, evidence-backed RAG, citation handling, explainability artifacts, graph algorithms, and API documentation. | EOIP-engg-doc-pkg/25-query-engine-requirements.md through 29-rag-architecture.md; docs/query-engine.md; docs/rag.md; docs/deep-agents-xai.md; docs/api-reference.md | Query endpoints return deterministic evidence-backed results; RAG answers cite graph/source records; timeout budgets and empty-result behavior are tested. |
| MVP-P4 | Agent, MCP, And Human Control | Implement MCP server, tool registry, agent runtime contracts, human-in-the-loop approval, memory governance, graph-over-loop and loop-over-graph behaviors, and audit traces. | EOIP-engg-doc-pkg/30-agent-architecture.md through 41-xai-explainability.md; docs/agents.md; EOIP-engg-doc-pkg/implementation/wp-agent-memory.md; wp-mcp.md | MCP health endpoint is live; risky actions are classified; approvals and audit trails are visible; agent operations are bounded and testable. |
| MVP-P5 | User Interfaces And Developer Experience | Build the usable web app, admin views, VS Code extension path, Hubble/local graph explorer integration, demo walkthroughs, and dashboards. | EOIP-engg-doc-pkg/42-web-user-ui-ux.md through 44-vscode-extension.md; apps/vscode-extension/README.md; docs/hubble-local.md; demo/script/walkthrough.md | Web app serves at `/app`; admin/source/graph/query workflows are reachable; VS Code extension documentation is reproducible; Hubble is available locally. |
| MVP-P6 | Security, Operations, Deployment, And Validation | Implement Docker local deployment, secrets examples, health checks, observability, backup/restore, security/privacy controls, test strategy, benchmarking, and runbooks. | EOIP-engg-doc-pkg/46-security-architecture.md through 60-operational-runbook.md; docs/docker-local.md; docs/deployment-*.md; docs/benchmarking.md | Docker Compose starts with all services healthy; API/MCP/web/Hubble checks pass; smoke, unit, coverage, recovery, and deployment validation are documented. |
| MVP-P7 | Acceptance, Traceability, And Productization | Close acceptance criteria, traceability, dependency/license/SBOM review, ADRs, risk register, demo playbook, multi-backend product positioning, and release handoff. | EOIP-engg-doc-pkg/61-demo-playbook.md through 76-multi-backend.md; tickets/*.md; docs/g2-traceability.md; docs/*audit*.md | Every requirement maps to implementation/test evidence or a declared risk; product can be rebuilt from docs; release candidate has a truthful residual-risk list. |

## Detailed Reconstruction Backlog

| Backlog ID | Item | Scope | Phase | Acceptance |
| --- | --- | --- | --- | --- |
| B-001 | Repository bootstrap | Restore source tree, dependency locks, config, demo data, and Docker assets. | MVP-P0 | Fresh clone can run validation commands. |
| B-002 | Contract layer | Implement source-event, graph, ingestion, query, evidence, audit, and API contracts. | MVP-P1 | Schema and contract tests pass. |
| B-003 | Graph adapters | Implement memory, HugeGraph, Neptune, and Neo4j-compatible graph adapters behind a stable GraphStore interface. | MVP-P1 | Backend resolver tests and adapter round-trip tests pass. |
| B-004 | Ontology governance | Load ontology packs, validate required properties, generate schema/forms, and report graph quality. | MVP-P1 | Ontology validation tests and docs pass. |
| B-005 | Ingestion framework | Build source connectors, file parsing, code graph extraction, cursoring, retries, DLQ, and provenance capture. | MVP-P2 | Demo and connector smoke tests pass. |
| B-006 | Query and RAG | Expose query API, EOQL behavior, graph traversals, retrieval ranking, evidence citations, and explanation payloads. | MVP-P3 | API tests prove cited answers and query limits. |
| B-007 | MCP and agents | Expose MCP tools, governed tool schemas, human controls, agent memory, and audit trails. | MVP-P4 | MCP health and governance tests pass. |
| B-008 | Web/admin/Hubble UX | Build the usable web app and admin flows; wire local Hubble graph exploration. | MVP-P5 | Browser/API smoke checks pass locally. |
| B-009 | Docker packaging | Build local Docker Compose deployment with health checks, one-shot schema/Hubble init, and documented ports. | MVP-P6 | Compose `up --wait` succeeds. |
| B-010 | Ops hardening | Add observability, secrets hygiene, backup/restore, security/privacy checks, benchmark path, and operational runbooks. | MVP-P6 | Recovery/deployment verification docs and tests are current. |
| B-011 | Traceability closure | Generate coverage JSON, consolidate audit reports, reconcile gaps, and prepare release handoff. | MVP-P7 | Requirement coverage gate passes with residual risks documented. |

## Workstream Ordering Rule

Source: `EOIP-engg-doc-pkg/gaps-implementation.md` §19 ("Implementation Ordering Inside Each Phase"), reinforced by `EOIP-engg-doc-pkg/67-implementation-plan.md` sequencing rules and `gaps-implementation.md` §13.

Every phase and every backlog item (B-001..B-011) must execute workstreams in this order:

1. Contract
2. Storage model
3. Domain service
4. API
5. Telemetry
6. Tests
7. CLI
8. UI
9. Docs
10. Acceptance demo

The normative constraint is explicit: "Do not build UI before the domain contract and backend path exist." The companion sequencing rules from `67-implementation-plan.md` require: schema/contracts/security foundations first; raw capture before mutation; Jira and code ingestion validated independently before cross-linking; QueryPlan/policy before NL/RAG/agent/MCP surfaces; evidence retrieval before answer generation; web/VS Code/MCP reusing the same application services; backup/restore proven before MVP release; later-phase capability only behind versioned ports or an ADR. In addition, §13 lists ten cross-phase architecture components that no phase may bypass: Canonical Contracts, HugeGraph Access Layer, Ontology Registry, Provenance Service, Validation Service, Query Planner, Audit, Telemetry, Configuration, Version Registry.

## Work-Package Cross-Reference

Source: `EOIP-engg-doc-pkg/implementation/wp-*.md` digests (reader F, all 12 files read in full). The wp files use the EOIP roadmap phase labels (P1-MVP, P2, P3, P8+); the MVP-P0..P7 mapping below is this plan's alignment, not a label found in the wp files. No wp file covers the gaps-roadmap phases P4, P6 or P7 (reader F finding).

| Work package | This plan's phase | One-line scope |
| --- | --- | --- |
| `wp-foundation.md` | MVP-P1 | HugeGraph authoritative store, logical graph domains, idempotent schema bootstrap, deterministic canonical identifiers, modular monolith boundary (5 tasks, all P1-MVP). |
| `wp-ontology-graph.md` | MVP-P1 | Meta graph, cross-domain bridge edges, index strategy, graph version journal, ontology vocabulary/relationship semantics, evidence model and provenance traversal, identity resolution, bitemporal-ready fields; RDF/OWL export is P2 (12 tasks, largest WP). |
| `wp-validation.md` | MVP-P1 | Graph validation rule packs, hard/soft validation gates, graph quality metrics with honest N/A denominators (3 tasks). |
| `wp-connectors.md` | MVP-P2 | Connector SDK, Jira JSON (fixture-based in MVP), local Git, GitLab metadata adapter, resiliency/dry-run/replay/deletion semantics; Confluence and ServiceNow are P2 of the roadmap (9 tasks). |
| `wp-ingestion.md` | MVP-P2 | Immutable raw capture, canonicalization, idempotent mutation, ingestion job lifecycle, dead-letter processing (5 tasks). |
| `wp-codegraph.md` | MVP-P2 | Deterministic Tree-sitter/AST parsing (Python + TS/JS in MVP), commit-to-symbol linking, call/import/dependency edges, source navigation ranges (5 tasks). |
| `wp-query.md` | MVP-P3 | Typed QueryPlan, path/impact/search, NL interpretation subordinate to policy, query safety policy, evidence envelope, raw-Gremlin admin boundary, parameterized Gremlin repository (9 tasks; hosts FR-GRAPH-007). |
| `wp-rag.md` | MVP-P3 | Retrieval router, evidence-backed GraphRAG, local model abstraction with model-down degradation, no mandatory vector DB, evaluation harness; adaptive RAG strategies are P3 of the roadmap (6 tasks). |
| `wp-agent-memory.md` | MVP-P4 | Agent contract, bounded runtime with budgets/circuit breaker, read-only TraceImpact agent, write/action approval boundary, controlled self-modification (P8+), scoped memory records (6 tasks). |
| `wp-mcp.md` | MVP-P4 | Read-only MCP server (search/entity/neighbors/path/query/impact/code/jira/document/lineage/evidence tools) and write-registry separation, disabled and unadvertised in MVP (2 tasks, smallest WP). |
| `wp-experience.md` | MVP-P5 | User web app over real APIs, bounded graph explorer, admin ingestion/quality UIs without hardcoded KPIs, read-only VS Code extension and trace/impact commands (6 tasks). |
| `wp-security-ops.md` | MVP-P6 | All 14 NFRs: no-egress, secret isolation, input safety, injection defenses, single-user auth without RBAC, container hardening, audit, restart safety, backup/restore, logging/health, metrics, benchmarks, modular boundary, data minimization (14 tasks, largest file). |

Caveats from the digest that this plan inherits: NFR-MAINT-001 is dual-listed (WP-FOUNDATION-05 and WP-SECURITY-OPS-13, identical text); all 86 wp tasks share identical boilerplate Dependencies/Steps, so task numbering is the only ordering signal inside a WP; Jira ingestion is JSON-fixture-based in MVP with no live Jira API task; no human-approval UI task exists despite the human-control architecture diagram.

## Testing Evolution By Phase

Source: `EOIP-engg-doc-pkg/gaps-implementation.md` §15 ("Testing Evolution by Phase"), verbatim per phase of the gaps roadmap; the right-hand column aligns each to this plan's MVP phases (alignment is this plan's, not the source's).

| Gaps-roadmap phase | Test focus (source wording) | Aligned MVP phase(s) |
| --- | --- | --- |
| Phase 1 | Unit + integration + E2E. | MVP-P0..P2 |
| Phase 2 | Semantic compatibility + migration + truth/conflict. | MVP-P1/P7 (ontology governance, traceability) |
| Phase 3 | Code-graph accuracy + architecture rules + blast radius. | MVP-P2/P3 |
| Phase 4 | Retrieval and AI evaluation. | MVP-P3 |
| Phase 5 | Federation consistency and source outage tests. | MVP-P3/P7 (backend portability, federation) |
| Phase 6 | Agent safety and prompt/tool injection. | MVP-P4 |
| Phase 7 | chaos/failure/recovery/security/performance. | MVP-P6 |
| Phase 8 | simulation correctness and predictive calibration. | Post-MVP (no MVP-P equivalent) |
| Phase 9 | SDK compatibility and extension isolation. | MVP-P7 (productization) |

The existing `55-testing-strategy.md` test-layer table (unit, contract, graph schema/integrity, integration, recovery, security, RAG/agent evaluation, UI/VS Code, E2E, performance) and its 70-row requirement-to-test obligation list remain the per-requirement test registry; this section only adds the phase-level progression.

## Release Gates A-E And KGCI Pipeline

Source: `EOIP-engg-doc-pkg/gaps-implementation.md` §16 ("Recommended Release Gates") for gates A-E; `EOIP-engg-doc-pkg/gaps-requirements.md` §30 (GAP-KGCI-001..004) for the normative KGCI chain; `packages/eoip/ci/pipeline.py` for the as-built chain. Rule from §16: "A release cannot progress if any critical gate fails."

| Gate | Name | Concrete checks |
| --- | --- | --- |
| A | Data | No critical schema violations; provenance coverage above configured threshold. |
| B | Graph | No forbidden relationship classes; graph invariant tests pass. |
| C | Security | No critical dependency vulnerability; no secret leakage; egress policy verified. |
| D | AI | Groundedness threshold met; forbidden-action rate = 0 on the safety suite. |
| E | Operations | Backup/restore tested for the release candidate; upgrade migration tested. |

KGCI (knowledge-graph CI) pipeline:

- Normative chain (gaps-requirements §30, GAP-KGCI-004): lint → schema → contract → sample ingest → SHACL → invariants → quality → compatibility → security → migration sim → publish, accompanied by GAP-KGCI-001 (CI-runnable CLI), GAP-KGCI-002 (machine-readable report), GAP-KGCI-003 (fail on semantic regression).
- As-built chain (`packages/eoip/ci/pipeline.py`, `STAGE_ORDER`, deterministic and offline): `lint` → `schema_validation` → `contract_checks` → `graph_invariants` → `quality_gates` → `compatibility` → `security` → `migration` → `publish`. Every stage returns a `StageResult` (pass/fail/skipped with findings); failure policy defaults to `FAIL_ON_ANY` with an optional `FAIL_ON_BREAKING` mode; the publish stage emits a versioned ontology artifact plus JSON report.
- Discrepancy noted, not hidden: the as-built chain has nine stages and does not implement the normative "sample ingest" and "SHACL" stages as separate steps; graph invariants are folded into `graph_invariants`, and "migration sim" is implemented as migration classification from the ontology semantic diff. Both wordings are recorded here.

## Data Migration Strategy

Source: `EOIP-engg-doc-pkg/gaps-implementation.md` §14, with alignment notes to G2-EVOL-016 (`EOIP-engg-doc-pkg/gaps2-requirements.md`, "explicit migration declaration, 5 types") and FR-GRAPH-003 (`03-functional-requirements.md`).

Every graph-schema change must declare exactly one of five migration strategies:

| Strategy | Meaning |
| --- | --- |
| `NO_MIGRATION` | Change is additive/backward-compatible; existing data needs no action. |
| `LAZY_MIGRATION` | Records are upgraded on read/write access over time. |
| `ONLINE_BACKFILL` | A background/bounded job rewrites affected data while the system stays up. |
| `OFFLINE_MIGRATION` | A maintenance-window migration; mutation path is paused or guarded. |
| `REBUILD_FROM_SOURCE` | Derived/graph data is discarded and deterministically rebuilt from immutable raw capture. |

Each change must carry a migration record with these fields (§14, verbatim list): source schema version; target schema version; affected labels; estimated mutations; reversible?; rollback; validation. This is consistent with the schema-bootstrap rule that an incompatible migration fails the application mutation path but preserves the database (FR-GRAPH-003), and with the graph-evolution model's expire-not-erase semantics (G2-EVOL family).

## Deployment Progression

Sources: `EOIP-engg-doc-pkg/gaps-requirements.md` (GAP-LITE-001 laptop/server/distributed profiles, GAP-HA-001, GAP-HG-006), `EOIP-engg-doc-pkg/gaps-implementation.md` Phase 7 §10.3-10.5, and the as-built `docs/deployment-ha.md` digest (reader G).

1. Laptop / developer Compose — `deploy/docker-compose.yml`; single-node HugeGraph 1.7.0 on RocksDB; all ports bound to 127.0.0.1 (local development model per `06-architecture.md` Implementation Reference).
2. Single-server team deployment — same Compose topology on a shared host with staged images/models, provisioned secrets, and the documented readiness/schema/backup runbook steps.
3. HA Compose profile — `deploy/docker-compose.ha.yml`: two stateless API replicas behind an nginx load balancer, and a single active worker elected through a leader lease on a shared volume (`EOIP_LEASE_PATH`); invariants from `packages/eoip/ha.py` (stateless API, single lease holder, lease TTL greater than GC pause). `docs/deployment-ha.md` carries an explicit split-brain caveat: the lease is advisory and depends on `O_CREAT|O_EXCL` atomicity on network mounts.
4. Helm chart — `deploy/helm/eoip` (Chart.yaml, values.yaml, 9 templates including HPA, Redis, PVC, ingress). The chart deliberately does not deploy the graph backend itself; worker HA requires an RWX-capable PVC.
5. HugeGraph distributed validation — the standalone→distributed migration playbook is documented as only partially covered; per `docs/deployment-ha.md`, "PD/Store images and sharding configuration are not validated in this repo… shape placeholder" and require HugeGraph enterprise/infra validation.

Discrepancy noted per policy: `docs/audit-2026-10-06/assessed-gap-report.md` marks G2-DEPLOY-HA / G2-DEPLOY-HELM / G2-SCALE-SHARD as Done under its local code/test-evidence policy, while the current operator doc `docs/deployment-ha.md` states the sharding/distributed layer is an unvalidated placeholder. Both statements stand; the reconciliation is the evidence tier (code exists vs operationally certified), not new evidence.

## Performance Engineering Plan

Source: `EOIP-engg-doc-pkg/gaps-implementation.md` §17, plus the MVP benchmark definition shared by `00-specification-audit-and-enhancements.md` / `04-non-functional-requirements.md` / `51-performance.md`, and the as-built `docs/benchmarking.md` digest.

Benchmark generator sizes (§17):

| Size | Vertices | Edges |
| --- | --- | --- |
| S | 100K | 500K |
| M | 1M | 10M |
| L | 10M | 100M |
| XL | Defined after production hardware and HugeGraph distributed validation | |

Measured query classes (§17, verbatim list): ingest throughput; upsert latency; point lookup; 2-hop; 5-hop bounded traversal; shortest path; impact query; search; hybrid retrieval; validation; concurrent reads/writes. The §17 honesty rule applies: "Never extrapolate marketing numbers from a different graph engine."

MVP-layer targets (explicitly "targets, not measured claims" in 00/04/51): dataset ≈ 2,000 Jira items, 10 repos, 15,000 commits, 25,000 files/symbols, 5,000 doc sections, 150K-300K relationships on an 8-core/32 GiB/NVMe workstation; indexed entity lookup p95 ≤ 500 ms; bounded path/impact p95 ≤ 2 s; standard API p95 ≤ 1 s excluding model generation; `docker compose up` readiness ≤ 120 s.

As-built status (both sides recorded): `docs/benchmarking.md` reports the memory-backend full profile passing and a HugeGraph smoke regression fixed (3,814 ms p95 → 917 ms via bounded identity cache), but states the full HugeGraph profile plus HTTP workload on an isolated instance "remains partially open"; `docs/audit-2026-10-06/assessed-gap-report.md` lists NFR-PERF-001 as Done. The reconciliation is again evidence tier, and the open full-profile run is carried as an MVP-P6 backlog obligation.

## Milestone Sequence M0-M10

Source: `EOIP-engg-doc-pkg/gaps-implementation.md` §21 ("Suggested Milestone Sequence"), deliverable summaries verbatim-ish per milestone; alignment column added by this plan.

| Milestone | Deliverable summary (source) | Aligned MVP phase(s) |
| --- | --- | --- |
| M0 — Foundation | Contracts + HugeGraph abstraction + Docker + CI. | MVP-P0/P1 |
| M1 — Connected Graph MVP | Jira + Git + code + graph + query. | MVP-P1/P2 |
| M2 — Evidence | Provenance + evidence + validation. | MVP-P1/P2 |
| M3 — UX | User/Admin/VS Code. | MVP-P5 |
| M4 — Semantic Governance | Ontology Studio + GitOps + quality. | MVP-P7 (post-MVP maturity) |
| M5 — Engineering Intelligence | Deep code + CI/CD + ITSM + architecture rules. | MVP-P3/P7 |
| M6 — Trusted AI | Retrieval router + GraphRAG + evidence. | MVP-P3 |
| M7 — Federation | Catalog + live sources + knowledge products. | MVP-P7 |
| M8 — Governed Agents | Agent runtime + MCP governance + firewall. | MVP-P4 (MVP scope) |
| M9 — Enterprise | SSO/RBAC/HA/DR/hardening. | MVP-P6 (MVP scope) / post-MVP |
| M10 — Analytics/Ecosystem | Simulation + SDK + domain packs. | Post-MVP |

## Ninety-Day Execution Focus

Source: `EOIP-engg-doc-pkg/gaps-implementation.md` §26 ("Recommended First 90-Day Build Focus"), which is "intentionally narrower than the complete roadmap."

| Window | Focus (source items) | Plan anchor |
| --- | --- | --- |
| Days 1-30 | canonical contracts; HugeGraph; Jira; Git/code parser; provenance; basic graph query. | MVP-P0, MVP-P1, start of MVP-P2 |
| Days 31-60 | cross-linking; impact analysis; user/admin UI; VS Code; validation; backup/restore. | MVP-P2, MVP-P3 start, MVP-P5/P6 enabling work |
| Days 61-90 | evidence service; ontology versioning; graph quality; local GraphRAG; MCP read tools; end-to-end pilot demo. | MVP-P3, MVP-P4, MVP-P7 demo closure |

Source guidance retained: "At Day 90, evaluate actual pilot feedback before accelerating advanced agents."

## Pilot And GA Readiness Checklists

Source: `EOIP-engg-doc-pkg/gaps-implementation.md` §22 (Commercial Pilot Readiness) and §23 (Enterprise GA Readiness).

Commercial pilot readiness — before the first paid pilot, complete at minimum:

- Phase 1 fully (the demonstrable MVP; in this plan: MVP-P0..P6 exit criteria).
- Critical subset of Phase 2: provenance; evidence; ontology versioning; quality dashboard.
- Critical subset of Phase 3: impact analysis; requirement-to-code traceability.
- Basic local GraphRAG from Phase 4.
- Deployment/backup/restore.
- Offline installation.
- License/SBOM/security documentation.
- Source guidance: "Do not wait for every advanced agent/RAG pattern."

Enterprise GA readiness — before broad enterprise sale, complete:

- Phase 2; Phase 3; Phase 4 core; Phase 7 security/operations.
- Validated scale benchmark; upgrade/rollback; support/diagnostics; documentation; compatibility matrix; penetration/security testing.
- Source allowance: federation, advanced agents and simulation can remain licensed/additional modules.

These are complemented, not replaced, by the MVP exit gate in `EOIP-engg-doc-pkg/MVP-requirements.md` (fresh clone → `docker compose up` → schema init → fixture ingestion → tests pass → documented demo → backup → destroy/recreate → restore → golden trace/impact queries rerun) and the release acceptance gate in `EOIP-engg-doc-pkg/70-acceptance-criteria.md` (immutable build/version metadata, SBOM/license output, test report, schema/ontology version, known-risk register, clean-deployment evidence, no-egress test, demo evidence, verified backup/restore; waivers require an ADR/risk acceptance; MVP non-negotiables are not waivable by convenience).

## Definition Of Done

Sources: `EOIP-engg-doc-pkg/gaps-implementation.md` §20 (10-point DoD), the shared "Validation / definition of done" boilerplate of the engg-doc package, `EOIP-engg-doc-pkg/70-acceptance-criteria.md`, and `EOIP-engg-doc-pkg/gaps2-requirements.md` §39.

A gap requirement (and, by adoption in this plan, any backlog item B-001..B-011) is done only if all ten hold (§20, verbatim list):

1. code exists,
2. typed interface exists,
3. tests exist,
4. error handling exists,
5. telemetry exists,
6. security impact documented,
7. migration impact documented,
8. user/admin documentation exists,
9. requirement ID appears in traceability matrix,
10. acceptance criterion demonstrated.

Acceptance-criteria conventions adopted from `70-acceptance-criteria.md` and the package-wide boilerplate:

- Every requirement carries a one-sentence acceptance criterion plus a target phase; MVP-FR-001..028 map to parent FR/NFR IDs, and the release acceptance gate (nine items listed under Pilot And GA Readiness) applies at release.
- Deferred capabilities live behind stable interfaces and are never represented as implemented; normative interfaces are documented; requirement-ID-mapped tests pass; error/security/logging/config paths are exercised; acceptance evidence is reproducible from a clean documented environment.
- From gaps2 §39: no mock or hardcoded output may be presented as a working integration.
- Tests are traceability assets (`55-testing-strategy.md`): a feature is done only when requirement, implementation task, tests, and acceptance evidence are linked.

## Requirements-To-Phase Mapping From Supplied Audit JSON

| Audit phase | Requirement count | Requirement IDs |
| --- | --- | --- |
| 10. G2-P7 — Temporal, Architecture & Process Intelligence | 41 | G2-ARCHC-001, G2-ARCHC-002, G2-ARCHC-003, G2-ARCHC-004, G2-ARCHC-005, G2-ARCHC-006, G2-ARCHC-007, G2-ARCHC-008, G2-ARCHC-009, G2-KD-001, G2-KD-002, G2-KD-003, G2-KD-004, G2-KD-005, G2-KD-006, G2-PM-001, G2-PM-002, G2-PM-003, G2-PM-004, G2-PM-005, G2-QOP-001, G2-QOP-002, G2-QOP-003, G2-QOP-004, G2-QOP-005, G2-QOP-006, G2-QOP-007, G2-QOP-008, G2-QOP-009, G2-SLO-001, G2-SLO-002, G2-SLO-003, G2-SLO-004, G2-SLO-005, G2-TIME-001, G2-TIME-002, G2-TIME-003, G2-TIME-004, G2-TIME-005, G2-TIME-006, G2-TIME-007 |
| 10. Phase 7 — Enterprise Security, HA & Operational Maturity | 3 | GAP-HA-001, GAP-LITE-001, GAP-LITE-002 |
| 11. G2-P8 — Knowledge Health & Governed AI | 25 | G2-CAP-001, G2-CAP-002, G2-CAP-003, G2-CAP-004, G2-CAP-005, G2-CAP-006, G2-IMMUNE-001, G2-IMMUNE-002, G2-IMMUNE-003, G2-IMMUNE-004, G2-IMMUNE-005, G2-IMMUNE-006, G2-IMMUNE-007, G2-IMMUNE-008, G2-IMMUNE-009, G2-IMMUNE-010, G2-IMMUNE-011, G2-IMMUNE-012, G2-IMMUNE-013, G2-OEVO-001, G2-OEVO-002, G2-OEVO-003, G2-OEVO-004, G2-OEVO-005, G2-OEVO-006 |
| 11. Phase 8 — Advanced Analytics, Simulation & Predictive Intelligence | 2 | GAP-GDS-001, GAP-GDS-002 |
| 12. G2-P9 — Counterfactual Twin & Causal Intelligence | 13 | G2-CAUSE-001, G2-CAUSE-002, G2-CAUSE-003, G2-CAUSE-004, G2-CAUSE-005, G2-CAUSE-006, G2-SIM-001, G2-SIM-002, G2-SIM-003, G2-SIM-004, G2-SIM-005, G2-SIM-006, G2-SIM-007 |
| 12. Phase 9 — Ecosystem, Extensions & Domain Packs | 12 | GAP-APP-001, GAP-APP-002, GAP-EXT-001, GAP-MKT-001, GAP-MKT-002, GAP-MKT-003, GAP-MKT-004, GAP-MKT-005, GAP-MKT-006, GAP-MKT-007, GAP-MKT-008, GAP-TEMPLATE-001 |
| 13. G2-P10 — Diamond-Standard UX & Production Hardening | 49 | G2-ADMIN-001, G2-ADMIN-002, G2-ADMIN-003, G2-ADMIN-004, G2-ADMIN-005, G2-ADMIN-006, G2-ADMIN-007, G2-ADMIN-008, G2-ADMIN-009, G2-ADMIN-010, G2-ADMIN-011, G2-ADMIN-012, G2-ADMIN-013, G2-ADMIN-014, G2-ADMIN-015, G2-ADMIN-016, G2-ADMIN-017, G2-UX-GRAPH-001, G2-UX-GRAPH-002, G2-UX-GRAPH-003, G2-UX-GRAPH-004, G2-UX-GRAPH-005, G2-UX-GRAPH-006, G2-UX-GRAPH-007, G2-UX-GRAPH-008, G2-UX-GRAPH-009, G2-UX-GRAPH-010, G2-UX-GRAPH-011, G2-UX-GRAPH-012, G2-UX-GRAPH-013, G2-UX-GRAPH-014, G2-UX-GRAPH-015, G2-UX-GRAPH-016, G2-UX-LENS-001, G2-UX-LENS-002, G2-UX-LENS-003, G2-UX-PLAY-001, G2-UX-PLAY-002, G2-UX-PLAY-003, G2-UX-PLAY-004, G2-UX-PLAY-005, G2-VSC-001, G2-VSC-002, G2-VSC-003, G2-VSC-004, G2-VSC-005, G2-VSC-006, G2-VSC-007, G2-VSC-008 |
| 3. G2-P0 — Contract & Architecture Alignment | 18 | G2-ARCH-001, G2-ARCH-002, G2-ARCH-003, G2-ARCH-004, G2-ARCH-005, G2-ARCH-006, G2-ARCH-007, G2-ARCH-008, G2-ARCH-009, G2-ARCH-010, G2-ARCH-011, G2-ARCH-012, G2-ARCH-013, G2-ARCH-014, G2-ARCH-015, G2-EKAF-003, G2-EVENT-001, G2-EVOL-009 |
| 3. Phase 0 — Architecture Foundation | 21 | GAP-AGOV-001, GAP-AGOV-002, GAP-AGOV-003, GAP-AGOV-004, GAP-CP-001, GAP-CP-002, GAP-CP-003, GAP-CP-004, GAP-CP-005, GAP-CP-006, GAP-CP-007, GAP-CP-008, GAP-CP-009, GAP-DBAGNOSTIC-001, GAP-HG-001, GAP-OBS-001, GAP-OBS-002, GAP-OBS-003, GAP-OBS-004, GAP-OBS-005, GAP-PORT-001 |
| 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core | 43 | G2-EKAF-001, G2-EKAF-002, G2-EKAF-004, G2-EKAF-005, G2-EKAF-006, G2-EKAF-007, G2-EKAF-008, G2-EKAF-009, G2-EKAF-010, G2-EKAF-011, G2-EKAF-012, G2-EKAF-013, G2-EKAF-014, G2-EKAF-015, G2-EKAF-016, G2-EKAF-017, G2-EKAF-018, G2-EKAF-019, G2-EKAF-020, G2-EKAF-021, G2-EKAF-022, G2-EKAF-023, G2-EKAF-024, G2-EKAF-025, G2-EKAF-026, G2-EKAF-027, G2-EKAF-028, G2-EKAF-029, G2-EKAF-030, G2-OBS-001, G2-OBS-002, G2-SEC-CRAWL-001, G2-SEC-CRAWL-002, G2-SEC-CRAWL-003, G2-SEC-CRAWL-004, G2-SEC-CRAWL-005, G2-SEC-CRAWL-006, G2-SEC-CRAWL-007, G2-SEC-CRAWL-008, G2-SEC-CRAWL-009, G2-SEC-CRAWL-010, G2-SEC-CRAWL-011, G2-SEC-CRAWL-012 |
| 4. Phase 1 — Fully Functional Demonstrable MVP | 17 | GAP-HG-002, GAP-HG-003, GAP-HG-004, GAP-HG-005, GAP-KRAG-001, GAP-OFFLINE-001, GAP-PROV-001, GAP-PROV-002, GAP-PROV-003, GAP-PROV-004, GAP-PROV-005, GAP-PROV-006, GAP-QI-007, GAP-SDT-001, GAP-SDT-002, GAP-SDT-003, GAP-SDT-004 |
| 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution | 49 | G2-EVENT-002, G2-EVENT-003, G2-EVENT-004, G2-EVENT-005, G2-EVENT-006, G2-EVENT-007, G2-EVOL-001, G2-EVOL-002, G2-EVOL-003, G2-EVOL-004, G2-EVOL-005, G2-EVOL-006, G2-EVOL-007, G2-EVOL-008, G2-EVOL-010, G2-EVOL-011, G2-EVOL-012, G2-EVOL-013, G2-EVOL-014, G2-EVOL-015, G2-EVOL-016, G2-JOURNAL-001, G2-JOURNAL-002, G2-JOURNAL-003, G2-JOURNAL-004, G2-JOURNAL-005, G2-JOURNAL-006, G2-REL-001, G2-REL-002, G2-REL-003, G2-REL-004, G2-REL-005, G2-REL-006, G2-REL-007, G2-REL-008, G2-SYNC-001, G2-SYNC-002, G2-SYNC-003, G2-SYNC-004, G2-SYNC-005, G2-SYNC-006, G2-SYNC-007, G2-SYNC-008, G2-SYNC-009, G2-SYNC-010, G2-SYNC-011, G2-SYNC-012, G2-SYNC-013, G2-SYNC-014 |
| 5. Phase 2 — Trustworthy Ontology & Semantic Governance | 50 | GAP-CONTRACT-001, GAP-CONTRACT-002, GAP-CONTRACT-003, GAP-CONTRACT-004, GAP-CONTRACT-005, GAP-CONTRACT-006, GAP-GITOPS-001, GAP-GITOPS-002, GAP-GITOPS-003, GAP-GITOPS-004, GAP-GITOPS-005, GAP-GITOPS-006, GAP-GITOPS-007, GAP-GITOPS-008, GAP-GOV-001, GAP-GOV-002, GAP-GOV-003, GAP-KQ-001, GAP-KQ-002, GAP-KQ-003, GAP-KQ-004, GAP-KQ-005, GAP-KQ-006, GAP-STUDIO-001, GAP-STUDIO-002, GAP-STUDIO-003, GAP-STUDIO-004, GAP-STUDIO-005, GAP-STUDIO-006, GAP-STUDIO-007, GAP-STUDIO-008, GAP-STUDIO-009, GAP-STUDIO-010, GAP-STUDIO-011, GAP-TAX-001, GAP-TRUST-001, GAP-TRUST-002, GAP-TRUST-003, GAP-TRUST-004, GAP-TRUST-005, GAP-TRUTH-001, GAP-TRUTH-002, GAP-TRUTH-003, GAP-TRUTH-004, GAP-TRUTH-005, GAP-TRUTH-006, GAP-TRUTH-007, GAP-TRUTH-008, GAP-TRUTH-009, GAP-TRUTH-010 |
| 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files | 24 | G2-SRC-CODE-001, G2-SRC-CODE-002, G2-SRC-CODE-003, G2-SRC-CODE-004, G2-SRC-CODE-005, G2-SRC-GH-001, G2-SRC-GH-002, G2-SRC-GH-003, G2-SRC-GH-004, G2-SRC-GL-001, G2-SRC-GL-002, G2-SRC-GL-003, G2-SRC-GL-004, G2-SRC-JIRA-001, G2-SRC-JIRA-002, G2-SRC-JIRA-003, G2-SRC-JIRA-004, G2-SRC-JIRA-005, G2-SRC-JIRA-006, G2-SRC-WEB-001, G2-SRC-WEB-002, G2-SRC-WEB-003, G2-SRC-WEB-004, G2-SRC-WEB-005 |
| 6. Phase 3 — Enterprise Engineering Intelligence | 21 | GAP-ARCH-001, GAP-ARCH-002, GAP-ARCH-003, GAP-ARCH-004, GAP-ARCH-005, GAP-ARCH-006, GAP-CHANGE-001, GAP-CHANGE-002, GAP-CHANGE-003, GAP-CHANGE-004, GAP-CHANGE-005, GAP-CHANGE-006, GAP-FRESH-001, GAP-FRESH-002, GAP-FRESH-003, GAP-FRESH-004, GAP-FRESH-005, GAP-SDT-005, GAP-SDT-006, GAP-SDT-007, GAP-SDT-008 |
| 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals | 23 | G2-GRAPH-API-001, G2-GRAPH-API-002, G2-GRAPH-API-003, G2-SRC-API-001, G2-SRC-API-002, G2-SRC-API-003, G2-SRC-API-004, G2-SRC-API-005, G2-SRC-API-006, G2-SRC-CONF-001, G2-SRC-CONF-002, G2-SRC-CONF-003, G2-SRC-CONF-004, G2-SRC-CONF-005, G2-SRC-SNKB-001, G2-SRC-SNKB-002, G2-SRC-SNKB-003, G2-SRC-SNOW-001, G2-SRC-SNOW-002, G2-SRC-SNOW-003, G2-SRC-SNOW-004, G2-SRC-SNOW-005, G2-SRC-SNOW-006 |
| 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG | 35 | GAP-CACHE-001, GAP-CACHE-002, GAP-CACHE-003, GAP-CACHE-004, GAP-CACHE-005, GAP-GRAG-001, GAP-GRAG-002, GAP-GRAG-003, GAP-GRAG-004, GAP-GRAG-005, GAP-GRAG-006, GAP-KRAG-002, GAP-KRAG-003, GAP-KRAG-004, GAP-KRAG-005, GAP-KRAG-006, GAP-KRAG-007, GAP-KRAG-008, GAP-KRAG-009, GAP-KRAG-010, GAP-QI-001, GAP-QI-002, GAP-QI-003, GAP-QI-004, GAP-QI-005, GAP-QI-006, GAP-QI-008, GAP-RET-001, GAP-RET-002, GAP-RET-003, GAP-RET-004, GAP-RET-005, GAP-RET-006, GAP-SEARCH-001, GAP-SEARCH-002 |
| 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM | 45 | G2-GRAPH-OBS-001, G2-GRAPH-OBS-002, G2-GRAPH-OBS-003, G2-GRAPH-RUNTIME-001, G2-GRAPH-RUNTIME-002, G2-GRAPH-RUNTIME-003, G2-GRAPH-SEC-001, G2-GRAPH-SEC-002, G2-GRAPH-SEC-003, G2-SRC-CICD-001, G2-SRC-CICD-002, G2-SRC-CICD-003, G2-SRC-CICD-004, G2-SRC-DD-001, G2-SRC-DD-002, G2-SRC-DD-003, G2-SRC-DD-004, G2-SRC-GRAF-001, G2-SRC-GRAF-002, G2-SRC-GRAF-003, G2-SRC-KIB-001, G2-SRC-KIB-002, G2-SRC-KIB-003, G2-SRC-KIB-004, G2-SRC-KIB-005, G2-SRC-OTEL-001, G2-SRC-OTEL-002, G2-SRC-OTEL-003, G2-SRC-OTEL-004, G2-SRC-OTEL-005, G2-SRC-RUNTIME-001, G2-SRC-RUNTIME-002, G2-SRC-RUNTIME-003, G2-SRC-SBOM-001, G2-SRC-SBOM-002, G2-SRC-SBOM-003, G2-SRC-SBOM-004, G2-TEL-001, G2-TEL-002, G2-TEL-003, G2-TEL-004, G2-TEL-005, G2-TEL-006, G2-TEL-007, G2-TEL-008 |
| 8. Phase 5 — Federation, Catalog & Knowledge Products | 30 | GAP-CATALOG-001, GAP-CATALOG-002, GAP-CATALOG-003, GAP-CATALOG-004, GAP-CATALOG-005, GAP-DATAOPS-001, GAP-FABRIC-001, GAP-FABRIC-002, GAP-FABRIC-003, GAP-FABRIC-004, GAP-FABRIC-005, GAP-FABRIC-006, GAP-FABRIC-007, GAP-FABRIC-008, GAP-FED-001, GAP-FED-002, GAP-FED-003, GAP-FED-004, GAP-KP-001, GAP-KP-002, GAP-KP-003, GAP-KP-004, GAP-KP-005, GAP-LAYER-001, GAP-LAYER-002, GAP-LIN-001, GAP-LIN-002, GAP-LIN-003, GAP-LIN-004, GAP-LIN-005 |
| 9. G2-P6 — Expanded Semantic Digital Twin | 10 | G2-I2R-001, G2-I2R-002, G2-I2R-003, G2-I2R-004, G2-I2R-005, G2-TWIN-001, G2-TWIN-002, G2-TWIN-003, G2-TWIN-004, G2-TWIN-005 |
| 9. Phase 6 — Governed Agentic Knowledge Operations | 26 | GAP-AGOV-005, GAP-AGOV-006, GAP-AGOV-007, GAP-AGOV-008, GAP-AGOV-009, GAP-AGOV-010, GAP-AGOV-011, GAP-AGOV-012, GAP-AKO-001, GAP-AKO-002, GAP-AKO-003, GAP-AKO-004, GAP-AKO-005, GAP-AKO-006, GAP-AKO-007, GAP-AKO-008, GAP-AKO-009, GAP-AKO-010, GAP-KFW-001, GAP-KFW-002, GAP-KFW-003, GAP-KFW-004, GAP-KFW-005, GAP-KFW-006, GAP-KFW-007, GAP-KFW-008 |
| unmapped | 103 | G2-GRAPH-BIZ-001, G2-GRAPH-BIZ-002, G2-GRAPH-BIZ-003, G2-GRAPH-DEC-001, G2-GRAPH-DEC-002, G2-GRAPH-DEC-003, G2-GRAPH-PROC-001, G2-GRAPH-PROC-002, G2-GRAPH-PROC-003, G2-GRAPH-TEST-001, G2-GRAPH-TEST-002, G2-GRAPH-TEST-003, G2-OBS-003, G2-OBS-004, G2-OBS-005, G2-OBS-006, G2-PERF-001, G2-PERF-002, G2-PERF-003, G2-PERF-004, G2-PERF-005, G2-PERF-006, G2-PERF-007, G2-PERF-008, GAP-AI-001, GAP-CDC-001, GAP-CDC-002, GAP-CDC-003, GAP-CDC-004, GAP-CDC-005, GAP-CDC-006, GAP-DRIFT-001, GAP-DRIFT-002, GAP-DRIFT-003, GAP-DRIFT-004, GAP-DRIFT-005, GAP-DRIFT-006, GAP-DRIFT-007, GAP-DUAL-001, GAP-DUAL-002, GAP-ENG-001, GAP-ER-001, GAP-ER-002, GAP-ER-003, GAP-ER-004, GAP-ER-005, GAP-ER-006, GAP-ER-007, GAP-ER-008, GAP-ER-009, GAP-ER-010, GAP-EXPORT-001, GAP-HG-006, GAP-HG-007, GAP-HG-008, GAP-HG-009, GAP-HG-010, GAP-IDE-001, GAP-KGCI-001, GAP-KGCI-002, GAP-KGCI-003, GAP-KGCI-004, GAP-LIFE-001, GAP-LIFE-002, GAP-LIFE-003, GAP-LIFE-004, GAP-LIFE-005, GAP-LIFE-006, GAP-MIGRATION-001, GAP-NLP-001, GAP-NOCODE-001, GAP-NOCODE-002, GAP-NOCODE-003, GAP-PACK-001, GAP-PROV-007, GAP-PROV-008, GAP-PROV-009, GAP-QUERY-001, GAP-REC-001, GAP-RULE-001 ... |

## Build And Deployment Gates

| Gate | Name | Evidence |
| --- | --- | --- |
| Gate 1 | Static validation | `python -m ruff check ...`; JSON/YAML validation; documentation generator has zero missing Markdown files. |
| Gate 2 | Unit validation | `python -m pytest` focused suites for graph backends, gaps, coverage, ontology, ingestion, query, API, and MCP. |
| Gate 3 | Local package build | Docker Compose `build --no-cache` completes for app, web, and Hubble images. |
| Gate 4 | Local deployment | Docker Compose `up -d --wait` reports all services healthy. |
| Gate 5 | Smoke checks | API ready, MCP live, web `/app`, and Hubble endpoints return success. |
| Gate 6 | Release truth review | Residual risks are documented; no audit row is claimed production-ready without evidence. |

## Current Honest Status Snapshot

| Area | Status |
| --- | --- |
| Markdown corpus | 818 workspace Markdown files were read and hashed; 184 project-authored Markdown files / 30,760 lines drive product reconstruction requirements. |
| Coverage JSON | 660 supplied gap/G2 requirements are marked done by the generated audit JSONs. |
| Local Docker | The stack was recently rebuilt and deployed locally with healthy API, MCP, web, worker, Hubble, and HugeGraph services. |
| Caveat | This plan does not assert that every enterprise connector/client backend has been validated against live external systems in this session. |

## Reconstruction Verification Receipts

As-built evidence captured by the independent audit pass of 2026-10-06/07 (reader digests: AUDIT-RUNTIME and AUDIT-CODE). Every receipt below is marked "verified 2026-10-06/07 by independent audit pass". Where a receipt disagrees with the assessed report `docs/audit-2026-10-06/assessed-gap-report.md`, both figures are recorded.

| Receipt | Result | Verification |
| --- | --- | --- |
| Unit test suite | `.venv/Scripts/python -m pytest tests/unit` — 1,843 collected; **1,842 passed / 0 failed / 1 skipped** (the skip is a conditional branch in `tests/unit/test_marketplace.py:150`); two full runs, both exit 0. | verified 2026-10-06/07 by independent audit pass |
| Security / performance / contract suites | `tests/security` + `tests/performance` + `tests/contract` — **56 passed**, 1 warning, exit 0 (27 security + 12 performance + 17 contract). | verified 2026-10-06/07 by independent audit pass |
| Docker stack health | **6 containers all "Up (healthy)"**: eoip-api, eoip-web, eoip-worker, eoip-mcp, hubble, hugegraph-server; `GET /health/ready` → HTTP 200 `{"status":"ready"}`; `GET /metrics` → HTTP 200 live Prometheus metrics (one historical 503 recorded for `/api/v1/admin/stats`, not current). | verified 2026-10-06/07 by independent audit pass |
| Playwright browser suite | `apps/web/test-results/.last-run.json` (mtime 2026-10-06 22:38): **`{"status":"passed","failedTests":[]}`** for the apps/web suite (8 spec files, 19 tests); one spec re-run live (`tests/hubble.spec.js`): 3 passed, 4 skipped — the 4 skips are intentional `EOIP_RUNTIME_HUBBLE=1` opt-ins. The root `test-results/.last-run.json` showing "failed" is a stale 2026-10-03 artifact from an older root-level run; disregard it. | verified 2026-10-06/07 by independent audit pass |
| Web frontend build | `npm run build` in `apps/web` completes successfully (16.31 s in the audit run; chunk-size warning only). | verified 2026-10-06/07 by independent audit pass |
| Coverage gates | `gap_coverage` gates re-run green: GAP 296/296 and G2 364/364 "done", exit 0. **Caveat (AUDIT-CODE finding):** the gate is a literal requirement-ID string matcher; 113 of the 296 GAP items trace solely to docstring ID-list comments in `packages/eoip/gaps/enterprise_completion.py` and its mirrored test file, and G2 evidence is largely an existence/import matrix (`gaps/g2_readiness.py`). The assessed report discloses this policy in its §0.2/§14.11. Treat gate counts as formal, not per-requirement behavioral proof. | verified 2026-10-06/07 by independent audit pass |
| Pass 8 focused regression | 33 passed, 0 failed — reproduced exactly. | verified 2026-10-06/07 by independent audit pass |
| Full pytest suite | Assessed report claims "1922 passed / 33 skipped / 0 failures"; the independent audit's JUnit measurement recorded **tests=1963, failures=0, errors=0, skipped=24** (≈1939 passed). Both recorded; the drift is counting methodology/timing, and 0 failures is confirmed. | verified 2026-10-06/07 by independent audit pass |
| Lint (ruff) | `.venv/Scripts/python -m ruff check .` → **exit 1, 165 errors** (97 auto-fixable, +16 with unsafe fixes; largest classes: I001 ×47 unsorted imports, F401 ×22 unused imports, BLE001 ×19 blind except, SIM115 ×17). **Open hygiene item** — carried as known debt; it does not block the green test receipts above. | verified 2026-10-06/07 by independent audit pass |

Environment-dependent (by design, not defects): `tests/e2e`, `tests/runtime_dlq`, and `tests/runtime_hubble` require the live stack or opt-in environment variables and were counted but not executed in the audit; the 4 hubble Playwright skips and the 1 unit skip are gated branches.
