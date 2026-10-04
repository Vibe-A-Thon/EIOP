# Feature specification: reproducible audit evidence foundation

Status: implementation awaiting verification and PR review.
Scope: documentation audit tooling and native-parser CI coverage only.

## Scope baseline

Discover all Git-listed tracked/untracked nonignored `.md`/`.txt` files recursively.
The user's latest decision includes both KGR catalogs. Exclude secret content,
Git internals, dependencies and generated runtime files. Generated audit reports
are historical evidence, not recursively generated product requirements.
The attached commit-message file was inspected as historical context, not modified.
No uncommitted user-owned API/readiness changes belong to this phase PR.

## User scenarios and testing

### Reviewer reproduces the document inventory (P1)

Given a checkout with nested first-party documentation, when the audit runs,
then every included file has its SHA-256, byte/line count and mechanical-read
receipt. Semantic review remains pending until actual review occurs.

### Engineer follows evidence leads without false closure (P1)

Given a requirement ID in documentation, code and tests, when the audit runs,
then exact occurrence locations appear but the requirement is not declared Done.
Unnumbered normative statements enter an explicit candidate queue.

### Maintainer verifies native file parsing in CI (P1)

Given a clean Windows CI environment, when regression runs, then native parser
dependencies are installed so real binary fixtures are not skipped for missing extras.
External executable prerequisites remain separately qualified.

## Requirements

- **REQ-001**: Inventory all in-scope nested documentation without reading excluded
  secret/runtime/dependency content; fail explicitly on unreadable inputs.
- **REQ-002**: Index explicit requirement IDs and unnumbered normative candidates
  with exact document path/line references and pending semantic-review status.
- **REQ-003**: Separate implementation/test identifier leads from verified
  acceptance; no automatic Done based on text occurrence.
- **REQ-004**: Persist consistent JSON/Markdown reports and a read ledger in the
  attached audit directory; prevent source-document overwrite.
- **REQ-005**: Run native parser regression fixtures in CI with the fileparse extra.

Nonfunctional criteria: local-only processing, bounded inputs, no symlink escape,
deterministic record identities/order, explicit error propagation, unchanged
existing application behavior and isolated scoped publication.

## Key entities

Document receipt; requirement candidate; evidence lead; acceptance receipt;
ambiguity decision; implementation phase; review gate.

## Measurable outcomes

All included documentation is mechanically read with hashes and exact counts.
All indexed candidates retain source citations. Zero completion claims arise
solely from identifier occurrences. All phase acceptance tests pass before PR.

## Decisions and conflicts

1. **KGR exclusion:** latest explicit user approval supersedes older exclusions
   for this audit; historical reports remain qualified to their original scope.
2. **Conflicting Done policies:** code/test mentions are only leads. Completion
   requires acceptance-specific evidence, not a module's existence.
3. **Roadmap versus MVP:** preserve phased delivery and local-first/HugeGraph
   authority; later-phase scope does not silently replace MVP constraints.
4. **Historical assertions:** retain original receipts and append a current
   supersession pointer. Never redate old passing tests as fresh results.
5. **Examples/proposals versus normative obligations:** retain candidates and
   source context, then reconcile before implementing a speculative feature.
6. **Every requirement Completed:** this is a final-product goal, not a permitted
   interim assertion. Pending work stays explicit until verified.
7. **Competitor comparisons:** product targets may be requirements; competitor
   superiority/pricing claims are unverified context, not implementation evidence.

## Iterative delivery plan

1. This phase: reproducible inventory/evidence triage, report reconciliation and CI
   parser coverage. Publish a scoped PR and stop for review.
2. After approval: finish semantic line-by-line review and atomic acceptance
   decomposition of all catalogs, including KGR and unnumbered obligations;
   reconcile duplicates/ranges/conflicts and establish approved dependency order.
3. Implement highest-priority validated gaps as independently testable vertical
   slices. Each phase includes unit/integration tests, full regression receipts,
   manual environment evidence where necessary, and a reviewed PR.
4. Final sign-off only after all acceptance criteria, live integration/UI gates
   and remote CI evidence are actually verified. No promised completion count.
