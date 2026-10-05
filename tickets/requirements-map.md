# EOIP Requirements and Coordination Map

Canonical product IDs come from [MVP requirements](../EOIP-engg-doc-pkg/MVP-requirements.md),
the [MVP matrix](../EOIP-engg-doc-pkg/traceability/mvp-traceability.csv) and applicable
engineering specifications. This map tracks packet tickets; it is not a
replacement requirement inventory or a claim of whole-product coverage.

| Requirement / scope | Source | Implementation / evidence surface | Acceptance / verification | Ticket | Status | Accountable role |
|---|---|---|---|---|---|---|
| User-requested VS Code NLQ/MCP auto-demo (no invented product ID) | [Extension demo instructions](../demo/autodemo/README.md) | [Extension commands](../apps/vscode-extension/extension.js), [MCP client](../apps/vscode-extension/mcp-client.js), [desktop driver](../demo/autodemo/vscode-demo.js) | 3 live isolated-host steps passed historically; current `npm --prefix apps\vscode-extension test` exits 0 with 7 native protocol/driver tests and 5 real-host fixture journeys. Source extension only; installed VSIX and independent QA unverified. | [ticket-20261004-005](ticket-20261004-005.md) | In Progress | Senior Engineer |
| User-requested guided end-to-end demo of the eight enterprise journeys (no invented product ID) | [Northstar scenario pack](../demo/demodata/enterprise/scenario-pack.json), [demo README](../demo/autodemo/README.md) | [Guided UI](../apps/web/src/App.jsx), [console runner](../demo/autodemo/runner.py), [runner and graph-query tests](../tests/unit/test_autodemo_runner.py) | Current focused Python regressions exit 0, web production build exits 0, autodemo Node checks pass 11/11 and full console exits 0 (134/138 passed, 4 unsupported query examples explicitly skipped). Prior five guided-demo browser tests passed. Independent QA and live-stack verification remain pending. | [ticket-20261004-005](ticket-20261004-005.md) | In Progress | Senior Engineer |
| Coordination synchronization (user request; no invented product ID) | [instruction](../instruction.md), [role catalog](../roles.md) | Supplied root packet, existing tickets and [ticket template](ticket-template.md) | All files read; local links, persona, real ticket states/owners/dependencies and snapshot/handoff consistent; author-executed checks, not product QA | [ticket-20261004-002](ticket-20261004-002.md) | Done | Senior Engineer |
| MVP-FR-001 through MVP-FR-028 and broader allowed documentation IDs (assessment umbrella; not implemented features) | [MVP matrix](../EOIP-engg-doc-pkg/traceability/mvp-traceability.csv), [MVP acceptance](../EOIP-engg-doc-pkg/MVP-requirements.md), [MVP gap report](../docs/audit-2026-10-04/mvp-gap-report.md), [full-document gap report](../docs/audit-2026-10-04/full-doc-gap-report.md) | [Tests](../tests), [receipt directory](../test-results), [evidence checker](../scripts/verify_requirement_evidence.py), [structured MVP JSON](../docs/audit-2026-10-04/mvp-gap-report.json) | MVP gap-report active implementation gaps are locally closed: 28/28 MVP-FR, 62/62 Core FR P1-MVP, 14/14 P1 NFR and 4/4 demo artifact groups Done with receipt links. The broader full-doc scan remains conservative triage and not independent product acceptance. | [ticket-20261004-003](ticket-20261004-003.md) | In Progress | QA Lead |
| MVP-FR-027 (source-bound validation support only) | [MVP automated tests](../EOIP-engg-doc-pkg/MVP-requirements.md#mvp-fr-027--automated-tests) | [Validation wrapper](../scripts/validate_with_evidence.py), [phase report](../docs/validation-evidence-phase1.md), [source-bound receipt](../test-results/audit-source-bound-validation.json) | 45 focused outcomes pass; final local source-bound full regression PASS with 1,207 outcomes / 1,192 passed / 15 skipped / zero failures/errors; remote CI, publication and independent review pending; not full release certification | [ticket-20261004-004](ticket-20261004-004.md) | Blocked | Senior Engineer |
| User-import proposal (former REQ-USER-IMPORT-001 is unverified) | Original proposal retained in [ticket](ticket-20261004-001.md); no approved source exists | No verified EOIP endpoint/stub/test for this proposed work | Obtain scope decision; map real ID/design if accepted or cancel explicitly if rejected | [ticket-20261004-001](ticket-20261004-001.md) | Blocked | Product Manager |

## Mapping rules

- Link existing files and stable sections; use line numbers only when checked.
- Identify exact verified behavior, requirement IDs and test/receipt provenance.
- Record missing/failed/skipped/fixture-only evidence explicitly.
- Keep ticket status and accountable role identical to [queue](../todo-status.md)
  and [checklist](../checklist.md).
- Coordination tasks need no invented functional requirement ID.
- Referenced historical receipts may be absent in a fresh clone; rerun scoped
  validation rather than asserting green results from unavailable files.
- Prioritize demo-preserving vertical slices; full-product certification remains
  limited by scope exclusions, live evidence and independent release gates.
