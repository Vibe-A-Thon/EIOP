# EOIP Full Documentation Gap Report

Generated: `2026-10-04T07:00:33.948606+00:00`  
Branch/HEAD: `feature/audit-evidence-foundation` / `cb36bb667d02323617010361e277b0d2f9880fd0`

## Scope

- Source Markdown/text files opened: 156
- Excluded by user/instruction: `EOIP-engg-doc-pkg/KGR-requirements.md`, `EOIP-engg-doc-pkg/KGR-implementation-plan.md`
- Generated report files were excluded from the source-document input to avoid self-referential reads.
- Secret-like file content withheld: `secrets.example/api-token.txt`
- Statuses are conservative: no requirement is marked Done without full current acceptance and independent verification.

## Summary

- Requirements/IDs extracted: 761
- Missing: 653
- Partial: 108

## Post-Audit Reconciliation

This generated scan remains a conservative documentation triage artifact from
HEAD `cb36bb667d02323617010361e277b0d2f9880fd0`. A later MVP implementation
evidence pass at HEAD `47bc8516d76031481c637780ddf8952ca865f2e1` is recorded in
[mvp-gap-report.md](./mvp-gap-report.md): 28/28 MVP-FR, 62/62 Core FR P1-MVP,
14/14 P1 NFR and 4/4 demo artifact groups are Done under code/test evidence.

The rows below intentionally remain Partial/Missing under the stricter policy
used by this full-document scan: no requirement is marked Done without full
current acceptance and independent verification. Remote CI observation,
independent review, live environment checks and broader GAP/G2 roadmap decisions
remain outside this report.

## Ambiguities and Resolutions

- **No RBAC versus authentication**: Preserve local authentication, secret hygiene, network isolation and audit; URL namespaces are not authorization.
- **MVP read-only AI/MCP versus admin operations**: MVP agent/MCP graph tools stay read-only; admin ingestion/validation/backup operations remain explicit app functions, not unrestricted graph writes.
- **Temporal fields versus point-in-time truth**: P1 temporal/version fields are current-state metadata; snapshots/diffs/as-of intelligence remain later phase until implemented and verified.
- **Synthetic demo data versus enterprise tenancy**: Use multi-tenant demo data for scenario coverage only; do not claim product RBAC/tenant isolation from fixtures.
- **Conflicting completion claims in historic audits**: Resolve against current HEAD, current tests, and independent acceptance receipts; historical green receipts remain dated evidence.
- **Case-only demo paths on Windows**: Use canonical `demo/demodata/manual`, `demo/demodata/pipelines`, `demo/script`, and `demo/autodemo` paths.

## Highest Priority MVP Rows

| ID | Status | Priority | Evidence | Recommendation |
|---|---|---|---|---|
| MVP-FR-001 | Partial | P0 | scripts/verify_requirement_evidence.py:159; tests/unit/test_requirement_evidence.py:73 | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-002 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-003 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-004 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-005 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-006 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-007 | Partial | P1 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-008 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-009 | Partial | P1 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-010 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-011 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-012 | Partial | P0 | packages/eoip/validation/gate.py:8 | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-013 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-014 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-015 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-016 | Partial | P1 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-017 | Partial | P1 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-018 | Partial | P1 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-019 | Partial | P1 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-020 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-021 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-022 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-023 | Partial | P1 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-024 | Partial | P1 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-025 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-026 | Partial | P0 | No identifier-bound source/test evidence found by scan | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-027 | Partial | P0 | tests/unit/test_validation_source_binding.py:32 | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |
| MVP-FR-028 | Partial | P0 | scripts/verify_requirement_evidence.py:159; tests/e2e/test_demo_flow.py:1 | Promote to Done only after current-source automated/manual acceptance and independent review cover the full criterion; otherwise keep as Partial. |

## Requirement Inventory

Detailed JSON includes source line references, acceptance snippets, implementation evidence, severity, priority, and recommended changes for every extracted ID: `full-doc-gap-report.json`.

## Files Read

- `agent_runbook.md`: complete, 83 lines
- `apps/vscode-extension/README.md`: complete, 51 lines
- `checklist.md`: complete, 64 lines
- `context.md`: complete, 92 lines
- `docs/61-demo-playbook.md`: complete, 233 lines
- `docs/adr-001-g2-contract-and-revision-model.md`: complete, 48 lines
- `docs/application-audit-2026-10-02.md`: complete, 76 lines
- `docs/audit-2026-10-04/gap-report.md`: complete, 116 lines
- `docs/benchmarking.md`: complete, 105 lines
- `docs/connectors-github.md`: complete, 85 lines
- `docs/connectors-gitlab.md`: complete, 109 lines
- `docs/deep-agents-xai.md`: complete, 55 lines
- `docs/demo-readiness-audit-2026-10-03.md`: complete, 107 lines
- `docs/deployment-verification.md`: complete, 35 lines
- `docs/docker-local.md`: complete, 732 lines
- `docs/eoip-development-audit-2026-10-03.md`: complete, 563 lines
- `docs/g2-traceability.md`: complete, 45 lines
- `docs/gap-audit-2026-10-02.md`: complete, 637 lines
- `docs/phase-completion-audit-2026-10-03.md`: complete, 400 lines
- `docs/validation-evidence-phase1.md`: complete, 85 lines
- `EOIP-engg-doc-pkg/00-specification-audit-and-enhancements.md`: complete, 108 lines
- `EOIP-engg-doc-pkg/01-project-vision.md`: complete, 42 lines
- `EOIP-engg-doc-pkg/02-scope-and-objectives.md`: complete, 42 lines
- `EOIP-engg-doc-pkg/03-functional-requirements.md`: complete, 683 lines
- `EOIP-engg-doc-pkg/04-non-functional-requirements.md`: complete, 171 lines
- `EOIP-engg-doc-pkg/05-system-requirements.md`: complete, 42 lines
- `EOIP-engg-doc-pkg/06-architecture.md`: complete, 105 lines
- `EOIP-engg-doc-pkg/07-component-architecture.md`: complete, 72 lines
- `EOIP-engg-doc-pkg/08-deployment-architecture.md`: complete, 79 lines
- `EOIP-engg-doc-pkg/09-data-architecture.md`: complete, 44 lines
- `EOIP-engg-doc-pkg/10-enterprise-ontology.md`: complete, 40 lines
- `EOIP-engg-doc-pkg/11-graph-schema.md`: complete, 62 lines
- `EOIP-engg-doc-pkg/12-meta-graph-design.md`: complete, 40 lines
- `EOIP-engg-doc-pkg/13-relationship-model.md`: complete, 40 lines
- `EOIP-engg-doc-pkg/14-temporal-graph.md`: complete, 39 lines
- `EOIP-engg-doc-pkg/15-provenance-lineage.md`: complete, 40 lines
- `EOIP-engg-doc-pkg/16-identity-resolution.md`: complete, 39 lines
- `EOIP-engg-doc-pkg/17-code-graph.md`: complete, 42 lines
- `EOIP-engg-doc-pkg/18-ingestion-architecture.md`: complete, 53 lines
- `EOIP-engg-doc-pkg/19-connector-framework.md`: complete, 41 lines
- `EOIP-engg-doc-pkg/20-jira-connector-requirements.md`: complete, 39 lines
- `EOIP-engg-doc-pkg/21-confluence-connector-requirements.md`: complete, 38 lines
- `EOIP-engg-doc-pkg/22-gitlab-connector-requirements.md`: complete, 40 lines
- `EOIP-engg-doc-pkg/23-servicenow-connector-requirements.md`: complete, 38 lines
- `EOIP-engg-doc-pkg/24-file-web-connectors.md`: complete, 42 lines
- `EOIP-engg-doc-pkg/25-query-engine-requirements.md`: complete, 57 lines
- `EOIP-engg-doc-pkg/26-query-engine-implementation.md`: complete, 66 lines
- `EOIP-engg-doc-pkg/27-ontology-validation.md`: complete, 39 lines
- `EOIP-engg-doc-pkg/28-graph-quality.md`: complete, 39 lines
- `EOIP-engg-doc-pkg/29-rag-architecture.md`: complete, 58 lines
- `EOIP-engg-doc-pkg/30-agent-architecture.md`: complete, 61 lines
- `EOIP-engg-doc-pkg/31-multi-agent-architecture.md`: complete, 40 lines
- `EOIP-engg-doc-pkg/32-memory-engineering.md`: complete, 39 lines
- `EOIP-engg-doc-pkg/33-context-engineering.md`: complete, 42 lines
- `EOIP-engg-doc-pkg/34-loop-engineering.md`: complete, 38 lines
- `EOIP-engg-doc-pkg/35-graph-engineering.md`: complete, 42 lines
- `EOIP-engg-doc-pkg/36-harness-engineering.md`: complete, 42 lines
- `EOIP-engg-doc-pkg/37-graph-over-loop.md`: complete, 41 lines
- `EOIP-engg-doc-pkg/38-loop-over-graph.md`: complete, 40 lines
- `EOIP-engg-doc-pkg/39-mcp-architecture.md`: complete, 40 lines
- `EOIP-engg-doc-pkg/40-human-control-model.md`: complete, 39 lines
- `EOIP-engg-doc-pkg/41-xai-explainability.md`: complete, 40 lines
- `EOIP-engg-doc-pkg/42-web-user-ui-ux.md`: complete, 40 lines
- `EOIP-engg-doc-pkg/43-admin-ui-ux.md`: complete, 43 lines
- `EOIP-engg-doc-pkg/44-vscode-extension.md`: complete, 42 lines
- `EOIP-engg-doc-pkg/45-api-specification.md`: complete, 43 lines
- `EOIP-engg-doc-pkg/46-security-architecture.md`: complete, 56 lines
- `EOIP-engg-doc-pkg/47-threat-model.md`: complete, 49 lines
- `EOIP-engg-doc-pkg/48-data-privacy.md`: complete, 40 lines
- `EOIP-engg-doc-pkg/49-local-ai-model-strategy.md`: complete, 40 lines
- `EOIP-engg-doc-pkg/50-observability.md`: complete, 38 lines
- `EOIP-engg-doc-pkg/51-performance.md`: complete, 45 lines
- `EOIP-engg-doc-pkg/52-scalability.md`: complete, 40 lines
- `EOIP-engg-doc-pkg/53-backup-restore.md`: complete, 38 lines
- `EOIP-engg-doc-pkg/54-devsecops.md`: complete, 40 lines
- `EOIP-engg-doc-pkg/55-testing-strategy.md`: complete, 110 lines
- `EOIP-engg-doc-pkg/56-rag-agent-evaluation.md`: complete, 42 lines
- `EOIP-engg-doc-pkg/57-graph-validation-test-plan.md`: complete, 43 lines
- `EOIP-engg-doc-pkg/58-end-to-end-test-plan.md`: complete, 42 lines
- `EOIP-engg-doc-pkg/59-docker-deployment.md`: complete, 64 lines
- `EOIP-engg-doc-pkg/60-operational-runbook.md`: complete, 41 lines
- `EOIP-engg-doc-pkg/61-demo-playbook.md`: complete, 61 lines
- `EOIP-engg-doc-pkg/62-risk-register.md`: complete, 27 lines
- `EOIP-engg-doc-pkg/63-assumptions.md`: complete, 31 lines
- `EOIP-engg-doc-pkg/64-decisions-and-adrs.md`: complete, 39 lines
- `EOIP-engg-doc-pkg/65-glossary.md`: complete, 50 lines
- `EOIP-engg-doc-pkg/66-phase-roadmap.md`: complete, 64 lines
- `EOIP-engg-doc-pkg/67-implementation-plan.md`: complete, 265 lines
- `EOIP-engg-doc-pkg/68-project-structure.md`: complete, 87 lines
- `EOIP-engg-doc-pkg/69-dependency-license-sbom.md`: complete, 37 lines
- `EOIP-engg-doc-pkg/70-acceptance-criteria.md`: complete, 131 lines
- `EOIP-engg-doc-pkg/71-research-and-verification-basis.md`: complete, 31 lines
- `EOIP-engg-doc-pkg/72-requirement-traceability.md`: complete, 128 lines
- `EOIP-engg-doc-pkg/73-architecture-diagrams.md`: complete, 293 lines
- `EOIP-engg-doc-pkg/74-data-contracts.md`: complete, 209 lines
- `EOIP-engg-doc-pkg/75-self-review-and-gap-closure.md`: complete, 40 lines
- `EOIP-engg-doc-pkg/diagrams/01-system-context.md`: complete, 18 lines
- `EOIP-engg-doc-pkg/diagrams/02-container-architecture.md`: complete, 24 lines
- `EOIP-engg-doc-pkg/diagrams/03-ingestion-pipeline.md`: complete, 10 lines
- `EOIP-engg-doc-pkg/diagrams/04-enterprise-graph-architecture.md`: complete, 17 lines
- `EOIP-engg-doc-pkg/diagrams/05-meta-graph.md`: complete, 14 lines
- `EOIP-engg-doc-pkg/diagrams/06-code-graph.md`: complete, 12 lines
- `EOIP-engg-doc-pkg/diagrams/07-cross-domain-relationship-graph.md`: complete, 15 lines
- `EOIP-engg-doc-pkg/diagrams/08-query-execution.md`: complete, 14 lines
- `EOIP-engg-doc-pkg/diagrams/09-graphrag.md`: complete, 14 lines
- `EOIP-engg-doc-pkg/diagrams/10-agent-runtime.md`: complete, 18 lines
- `EOIP-engg-doc-pkg/diagrams/11-multi-agent-orchestration.md`: complete, 17 lines
- `EOIP-engg-doc-pkg/diagrams/12-mcp-architecture.md`: complete, 12 lines
- `EOIP-engg-doc-pkg/diagrams/13-human-control-architecture.md`: complete, 13 lines
- `EOIP-engg-doc-pkg/diagrams/14-web-ui-architecture.md`: complete, 14 lines
- `EOIP-engg-doc-pkg/diagrams/15-vscode-architecture.md`: complete, 12 lines
- `EOIP-engg-doc-pkg/diagrams/16-deployment.md`: complete, 21 lines
- `EOIP-engg-doc-pkg/diagrams/17-mvp-e2e-flow.md`: complete, 22 lines
- `EOIP-engg-doc-pkg/DOCUMENTATION-INDEX.md`: complete, 99 lines
- `EOIP-engg-doc-pkg/examples/demo_documentation.md`: complete, 3 lines
- `EOIP-engg-doc-pkg/gaps-implementation.md`: complete, 1216 lines
- `EOIP-engg-doc-pkg/gaps-requirements.md`: complete, 1401 lines
- `EOIP-engg-doc-pkg/gaps2-implementation.md`: complete, 1625 lines
- `EOIP-engg-doc-pkg/gaps2-requirements.md`: complete, 2059 lines
- `EOIP-engg-doc-pkg/implementation/wp-agent-memory.md`: complete, 77 lines
- `EOIP-engg-doc-pkg/implementation/wp-codegraph.md`: complete, 67 lines
- `EOIP-engg-doc-pkg/implementation/wp-connectors.md`: complete, 107 lines
- `EOIP-engg-doc-pkg/implementation/wp-experience.md`: complete, 77 lines
- `EOIP-engg-doc-pkg/implementation/wp-foundation.md`: complete, 67 lines
- `EOIP-engg-doc-pkg/implementation/wp-ingestion.md`: complete, 67 lines
- `EOIP-engg-doc-pkg/implementation/wp-mcp.md`: complete, 37 lines
- `EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md`: complete, 137 lines
- `EOIP-engg-doc-pkg/implementation/wp-query.md`: complete, 107 lines
- `EOIP-engg-doc-pkg/implementation/wp-rag.md`: complete, 77 lines
- `EOIP-engg-doc-pkg/implementation/wp-security-ops.md`: complete, 157 lines
- `EOIP-engg-doc-pkg/implementation/wp-validation.md`: complete, 47 lines
- `EOIP-engg-doc-pkg/knowgridflow-product-architecture.md`: complete, 2010 lines
- `EOIP-engg-doc-pkg/MVP-implementation-plan.md`: complete, 590 lines
- `EOIP-engg-doc-pkg/MVP-requirements.md`: complete, 275 lines
- `EOIP-engg-doc-pkg/README.md`: complete, 49 lines
- `EOIP-engg-doc-pkg/source-master-prompt.txt`: complete, 2374 lines
- `examples/demo-enterprise/README.md`: complete, 28 lines
- `examples/demo-enterprise/wiki/checkout-latency-runbook.md`: complete, 12 lines
- `examples/demo-enterprise/wiki/checkout-risk-architecture.md`: complete, 34 lines
- `examples/demo-repo/README.md`: complete, 4 lines
- `handoff_template.md`: complete, 39 lines
- `instruction.md`: complete, 140 lines
- `memory.md`: complete, 151 lines
- `onboarding_checklist.md`: complete, 27 lines
- `onboarding_prompts.md`: complete, 71 lines
- `README.md`: complete, 78 lines
- `roles.md`: complete, 526 lines
- `secrets.example/api-token.txt`: content_withheld_secret_like,  lines
- `secrets.example/README.md`: complete, 24 lines
- `tickets/requirements-map.md`: complete, 26 lines
- `tickets/ticket-20261004-001.md`: complete, 83 lines
- `tickets/ticket-20261004-002.md`: complete, 61 lines
- `tickets/ticket-20261004-003.md`: complete, 69 lines
- `tickets/ticket-20261004-004.md`: complete, 62 lines
- `tickets/ticket-template.md`: complete, 38 lines
- `todo-status.md`: complete, 29 lines
