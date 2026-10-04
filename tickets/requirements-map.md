# EOIP Requirements and Coordination Map

Canonical product IDs come from [MVP requirements](../EOIP-engg-doc-pkg/MVP-requirements.md),
the [MVP matrix](../EOIP-engg-doc-pkg/traceability/mvp-traceability.csv) and applicable
engineering specifications. This map tracks packet tickets; it is not a
replacement requirement inventory or a claim of whole-product coverage.

| Requirement / scope | Source | Implementation / evidence surface | Acceptance / verification | Ticket | Status | Accountable role |
|---|---|---|---|---|---|---|
| Coordination synchronization (user request; no invented product ID) | [instruction](../instruction.md), [role catalog](../roles.md) | Supplied root packet, existing tickets and [ticket template](ticket-template.md) | All files read; local links, persona, real ticket states/owners/dependencies and snapshot/handoff consistent; author-executed checks, not product QA | [ticket-20261004-002](ticket-20261004-002.md) | Done | Senior Engineer |
| MVP-FR-001 through MVP-FR-028 (assessment umbrella; not 28 implemented features) | [MVP matrix](../EOIP-engg-doc-pkg/traceability/mvp-traceability.csv), [MVP acceptance](../EOIP-engg-doc-pkg/MVP-requirements.md) | [Tests](../tests), [receipt directory](../test-results), [evidence checker](../scripts/verify_requirement_evidence.py) | Reconcile actual per-row behavior, parent IDs, latest receipts and source binding; old mapping 3/28 is historical annotation coverage only | [ticket-20261004-003](ticket-20261004-003.md) | Open | QA Lead |
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
