# EOIP Requirements and Coordination Map

Canonical product IDs come from [MVP requirements](../EOIP-engg-doc-pkg/MVP-requirements.md),
the [MVP matrix](../EOIP-engg-doc-pkg/traceability/mvp-traceability.csv) and applicable
engineering specifications. This map tracks packet tickets; it is not a
replacement requirement inventory or a claim of whole-product coverage.

| Requirement / scope | Source | Implementation / evidence surface | Acceptance / verification | Ticket | Status | Accountable role |
|---|---|---|---|---|---|---|
| Coordination synchronization (user request; no invented product ID) | [instruction](../instruction.md), [role catalog](../roles.md) | Supplied root packet, existing tickets and [ticket template](ticket-template.md) | All files read; local links, persona, real ticket states/owners/dependencies and snapshot/handoff consistent; author-executed checks, not product QA | [ticket-20261004-002](ticket-20261004-002.md) | Done | Senior Engineer |
| MVP-FR-001 through MVP-FR-028 and broader allowed documentation IDs (assessment umbrella; not implemented features) | [MVP matrix](../EOIP-engg-doc-pkg/traceability/mvp-traceability.csv), [MVP acceptance](../EOIP-engg-doc-pkg/MVP-requirements.md), [full-document gap report](../docs/audit-2026-10-04/full-doc-gap-report.md) | [Tests](../tests), [receipt directory](../test-results), [evidence checker](../scripts/verify_requirement_evidence.py), [structured audit JSON](../docs/audit-2026-10-04/full-doc-gap-report.json) | Full allowed Markdown/text scan extracted 761 IDs/requirement-like IDs: 108 Partial, 653 Missing, zero Done under conservative current-acceptance policy; review and convert only verified active gaps into scoped tickets | [ticket-20261004-003](ticket-20261004-003.md) | In Progress | QA Lead |
| MVP-FR-027 (source-bound validation support only) | [MVP automated tests](../EOIP-engg-doc-pkg/MVP-requirements.md#mvp-fr-027--automated-tests) | [Validation wrapper](../scripts/validate_with_evidence.py), [phase report](../docs/validation-evidence-phase1.md) | 45 focused outcomes pass; full source binding blocked by concurrent edits, CI/review pending; not full requirement certification | [ticket-20261004-004](ticket-20261004-004.md) | Blocked | Senior Engineer |
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
