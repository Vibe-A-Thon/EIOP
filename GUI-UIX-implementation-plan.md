# EOIP GUI / UI-UX Implementation and Evidence Plan

Version: 1.0.0. Prepared: 2026-10-16. Status: implementation specification, NOT a completion certificate.

Primary source: [GUI-UIX-requirements.md](GUI-UIX-requirements.md), version 1.0.0, dated 2026-10-13. Repository planning baseline: `edfa7aed607b8509da5801acc16490c97f5fe375`.

Related execution programme: [gaps-audit-cp-implementation-plan.md](gaps-audit-cp-implementation-plan.md). Historical findings: [gaps-audit-cp.md](gaps-audit-cp.md) and [Audit-GAPS-G-dev.md](Audit-GAPS-G-dev.md). Preserve their historical evidence and source bindings.

Implementation follow-up, 2026-10-16: [GUI audit and first implementation batch](GUI-UIX-audit-2026-10-16.md). Structural intake now preserves all source IDs and nonblank lines; new shared GUI foundations, truthful administrative states, policy round-trip/replacement, selected keyboard behavior, event polling and export repairs have executable checks. GUI-00/01 and all feature packages remain partial until their full semantic, runtime and release acceptance passes. The follow-up records actual outcomes and open gaps; the package list below remains the complete target scope.

### Agent Start Here

1. Read the [completion contract](#1-outcome-and-non-negotiable-completion-contract) and [known mapping problems](#23-correct-known-mapping-problems-before-wiring-screens).
2. Resolve the relevant [decisions](#3-decision-register-and-no-assumption-protocol), then follow the [ordered engineering packages](#12-ordered-engineering-packages).
3. Use the [screen work packages](#11-screen-by-screen-implementation-work-packages), [backend contracts](#10-missing-backend-contracts-concrete-closure-instructions) and [complete integration index](#appendix-c-all-735-historical-integration-records) for the selected slice.
4. Execute the [test/evidence strategy](#16-test-strategy-and-anti-false-completion-controls), then apply the [release gates and handoff](#18-release-acceptance-rollback-and-handoff).

Do not begin by replacing every page or installing the whole proposed stack. Start with GUI-00 and one scoped, real end-to-end workflow.

## 1. Outcome and Non-Negotiable Completion Contract

Enhance the existing EOIP application into an integrated, domain-neutral enterprise workbench implementing every mandatory GUI requirement. Deliver polished graphics, useful motion, consistent icons, modular screens, accessible equivalents, secure real integrations, and low-complexity task flows. This is an application, not a marketing landing page or a collection of disconnected demonstration screens.

This plan defines how to reach and prove completion. It cannot promise that writing code alone will achieve 100%: unresolved product decisions, missing services, hardware qualification, manual accessibility evaluation, legal review, and independent acceptance must also finish. Do not silently make assumptions to hide these dependencies.

### 1.1 Meaning of 100%

1. Every source clause is registered, decomposed into independently testable acceptance clauses, assigned an owner, and given an explicit applicability decision.
2. Every mandatory clause passes on the exact release candidate, using the real deployment profile it claims to support.
3. All 27 screens, shared surfaces, 20 missing-contract families, and 735 historical integration records have a recorded disposition. A disposition is not an implementation pass.
4. Required functionality has no remaining mock, simulator masquerading as a runtime, stub, placeholder, unimplemented button, unreachable route, skipped acceptance test, or unexplained failure.
5. Persistence, permission checks, tenant/workspace boundaries, restart recovery, negative paths, cancellation and concurrency are demonstrated, not inferred from HTTP 200.
6. Visual, performance, security, accessibility, usability, release, and documentation gates all pass. A failed gate blocks its dependent scope.
7. Report three separate totals: implementation clauses passed; end-to-end acceptance clauses passed; external/manual approvals passed. Never blend them into a flattering single percentage.
8. Optional 3D, Tauri, and optional CRDT work require a recorded scope decision. Exclusions require owner approval and remain visible. Removing a mandatory requirement changes scope; it does not complete the original scope.

### 1.2 What Does Not Prove Completion

The following are navigation aids or partial evidence only: a source filename, a test filename, a requirement marker, route registration, an OpenAPI operation, generated code, a screenshot of a static mock, a successful build, a green test that intercepted all APIs, line/branch coverage, a manually edited status, a simulator response, and a test receipt from a different source revision.

A passing automated test must name its acceptance clause, assert the actual business outcome, and retain an executable run receipt. Integration tests must additionally prove which backend and storage were used. Visual evidence must show the intended state with representative data. Manual evaluation must identify the reviewer, environment, procedure, observations, and result. No agent may self-certify a human review it did not receive.

### 1.3 Scope of This Planning Pass

The full 1,395-line source was loaded and structurally inspected. Its repeated screen rules were deduplicated for analysis without removing obligations. All catalogue rows were parsed, including their request/response, status, source locator, and screen fields. The appendices preserve complete identifier coverage. Selected current frontend, API, licensing, test, and CI files were inspected for migration planning; this is not a fresh full-repository runtime audit or a claim that every backend operation was exercised.

Source size: 344,160 bytes. SHA-256 of UTF-8 source bytes, also its LF-normalized hash at this baseline:

```text
fc4cfc1692239a157aa09467be25087a6a8def2a254c445fbb7696d4561e3bff
```

The interrupted report-storage work is outside this document-only task. Leave `tests/unit/test_report_storage_contract.py` and any other existing working-tree changes untouched; do not interpret those two currently failing regression tests as delivered fixes.

## 2. Baseline and Source Corrections

### 2.1 Inventory Reconciliation

| Inventory | Source baseline | Meaning |
|---|---:|---|
| Numbered source sections | 23 | All require clause extraction, not just screen headings. |
| Screen specifications | 27 | `SCR-001` through `SCR-027`, contiguous. |
| Integration records | 735 | 734 REST operations plus one WebSocket entry. |
| Historical integration states | 697 IMPLEMENTED-UNVERIFIED; 38 PARTIAL | Historical labels, not present-day verification. |
| Integrations assigned a primary screen | 151 | Source assignment still needs semantic review. |
| Integrations with no primary screen | 584 | Must be classified, not dropped or turned into 584 new menu items. |
| Missing backend families | 20 | Proposed contracts, not verified services. |
| Source screen-to-integration matrix rows | 27 | Omits INT-735 even though its catalogue row names SCR-017 and SCR-024. |
| Source API summary | 689 paths, 734 REST operations, 303 schemas | Historical statement; recapture the composed API before generating clients. |

The catalogue's generic `object`, `none`, `inline`, and `HTTPValidationError` values do not establish successful response contracts. The two delete rows describing `HTTPValidationError` are especially unsuitable as success types. Similarly, generic error lists omit runtime authorization and service failures. Inspect real schemas and behavior before exposing an operation.

### 2.2 Current Frontend Starting Points

| Existing location | Observed starting point | Required treatment |
|---|---|---|
| `apps/web/package.json`, `package-lock.json` | React/React DOM 19.1.1, Vite 7.3.6, Sigma 2.4.0, Graphology 0.25.4, locked Cytoscape 3.34.3, Playwright 1.55.1 | Preserve lockfile reproducibility; introduce strict TypeScript and tools through verified migration steps. |
| `apps/web/src/App.jsx` | Monolithic shell, local mode navigation, direct fetch wrapper, API token in sessionStorage | Extract composition; typed deep links; central transport; real session lifecycle. |
| `apps/web/src/components/ui/` | Existing primitives and tokens, but dark indigo/glass/glow styling and large radii | Migrate consumers to source Evidence Atlas tokens; do not add another permanently competing system. |
| `apps/web/src/icons.jsx` | Hand-authored icon paths | Introduce a Lucide-backed registry with named compatibility adapters, then remove redundant definitions. |
| `apps/web/src/kgr/` | Useful graph views, exporters, selection tools, workers and analytical helpers | Inventory behavior before changing rendering; preserve verified semantics behind typed boundaries. |
| `kgr/renderers/SigmaRenderer.jsx` | Random initial positions, synchronous pairwise force layout, errors swallowed during edge insertion | Replace layout core with worker library; deterministic fixtures; preserve parallel-edge identity; surface invalid input. |
| `kgr/hooks/useGraphEvents.js` | Direct socket and recovery fetch without shared authenticated transport; reconnect timer lacks lifecycle cancellation | Replace with one scoped subscription manager; test unmount, tenant switch, gaps and expiry. |
| `kgr/KGRExplorer.jsx` | Local notes keyed only by entity ID | Explicitly migrate or quarantine legacy notes; never assign ambiguous notes to an arbitrary tenant. |
| `studio/`, `admin/`, `cognitive/`, `dashboards/` | Existing useful experiences outside the proposed 27-screen taxonomy | Map each workflow to a destination before replacing its entry point. |
| `apps/web/tests/application.spec.js` | Browser API interception supplies many fixture responses | Retain for controlled UI tests; do not count it as real backend integration evidence. |
| `apps/web/playwright.config.js` | Single default viewport and screenshot-on-failure | Add explicit browser/theme/viewport/evidence projects, real and mocked suites separately. |
| `.github/workflows/ci.yml` | Web build plus selected export-security browser tests | Add type, lint, component, contract, visual, accessibility, real API and performance gates. |
| `packages/eoip/verification/`, `scripts/validate_with_evidence.py` | Source-bound Python evidence machinery exists | Reuse concepts and compatible receipts; add browser/build/runtime bindings rather than bypassing checks. |

These observations are code-inspection findings. No fresh visual baseline, bundle measurement, browser pass or production readiness is claimed by this document.

### 2.3 Correct Known Mapping Problems Before Wiring Screens

| Problem | Explicit resolution instruction |
|---|---|
| SCR-019 lists authz/config/product exports, but INT-595..603 report operations have no primary screen | Assign the real reports family to SCR-019. Keep administrative exports under their owning administrative surfaces. Validate any approved report data source separately. |
| SCR-025 lists user creation, schema profiling, tokenizer and architecture-policy operations | Settings must use the current principal and preferences contracts. Move user administration to SCR-021/022 and profiling to SCR-015/016; never grant those actions merely to render Settings. |
| SCR-016 points at context-build and model-evaluation operations | Use identity candidate review, validation, conformance and the resolution contract for quality. Do not relabel model evaluation as entity resolution. |
| SCR-005 lacks core neighbourhood/search/path/view operations | Review INT-263..286, 344, 373, 570, 604..606 and BACKEND-MISSING-004; expose only semantically appropriate, authorized actions. |
| SCR-012/013 interchange read-only meta-graph and schema mutation actions | Meta-graph remains exploratory. Editing redirects to a governed ontology draft with permission checks. |
| SCR-027 includes health-check mutations | Error rendering must not trigger infrastructure checks or mutate state automatically. Use safe minimal health probes and explicit authorized recovery commands. |
| SCR-022 lists quota consume/refund | Usage accounting is a server responsibility, not a client permission to alter quota balances. Tenant administrators view usage and approved configuration operations. |
| INT-708..731 duplicate unversioned brain routes | Verify alias equivalence, select one canonical versioned client route, retain compatibility tests; do not count aliases as separate feature completion. |
| INT-735 names a jobs socket not matched by the inspected current graph socket route | Re-enumerate mounted WebSocket routes; do not guess that graph events equal job events. Add actual `/ws/graph/events` to the current transport inventory. |
| Source says global bearer is the only auth | Current backend contains signed-principal validation changes. Revalidate those improvements, but do not confuse them with complete cookie/PKCE/session/revocation support. |
| Source leaves licence choice open | Product owner chose commercial first-party terms plus original third-party terms. Preserve `LICENSE`, `NOTICE`, `LICENSING.md` and `licenses/`; legal clearance and full notices remain separate work. |

### 2.4 Dependency Verification, Not Blind Upgrades

The source's version list is a planning input, not an instruction to install every package immediately. During preparation, direct npm registry lookups confirmed that React 19.3.0, Vite 8.3.4, TypeScript 7.0.2 and `@playwright/test` 1.64.0 exist. This does not establish compatibility, latest-version status, licence approval, or validation of the other listed versions.

For every selected package record exact npm name, version, tarball integrity, engines, peer dependencies, transitive licences, bundle impact, offline-build implications and the functionality requiring it. Resolve marketing names to actual packages, notably React Flow and scoped TanStack/Radix packages. Validate in a disposable branch and pin exact compatible versions. Do not use `--force`, `--legacy-peer-deps`, a suppressed type check, or dependency replacement merely to make installation green.

Add libraries when their owning feature starts. Keep a single primary graph model/renderer and a single owner per state category. This avoids paying the complexity and startup cost of every proposed library before its feature exists.

## 3. Decision Register and No-Assumption Protocol

Each decision record must contain: ID, question, alternatives, selected answer, accountable owner, rationale, affected clauses/screens/contracts, evidence, approval date, and superseded decision. The execution agent may propose an answer but may not mark owner-dependent policy approved.

| Decision | Known direction / required answer | Owner and blocking scope |
|---|---|---|
| D-01 | Incrementally enhance `apps/web`; source target architecture wins after migration. Preserve behavior, not outdated visuals. | Technical lead; approve route-by-route cutover before removing old surfaces. |
| D-02 | Evidence Atlas, light-first; optional dark and two high-contrast themes. This plan selects the source's recommended direction. | UX lead validates representative screens before broad rollout. |
| D-03 | Exact dependency matrix and supported Node/package-manager versions require tested resolution. | Frontend lead; blocks foundation lockfile change. |
| D-04 | Confirm production IdPs, SAML requirement, local-password mode, MFA, recovery and session policy. | Product/security; blocks complete SCR-001. |
| D-05 | Confirm workspace membership model and production tenant isolation tier/backend topology. | Architecture/security; blocks scope-sensitive integrations. |
| D-06 | Confirm supported SaaS, installed, air-gap, distributed and optional desktop profiles, with a test matrix. | Product/platform; no profile is supported solely because an environment enum exists. |
| D-07 | Define role/action/resource/attribute policies and separation of duties. | Security/domain owners; blocks sensitive mutations and sharing. |
| D-08 | Choose real model runtime, model artefacts, capability names, calibrated confidence and egress policies. | AI/security; blocks live inference and model-quality claims. |
| D-09 | Specify CPU/GPU/OS/browser reference hardware, dataset shapes, edge density and percentile measurement policy. | Performance/product; blocks commercial scale acceptance. |
| D-10 | Source mandatory formats remain required. Approve renderer/dependency licences, template list and visual fidelity samples. | Reporting/product/legal; blocks export acceptance. |
| D-11 | Define offline-safe data classes, retention, cache encryption/key handling and whether queued writes are mandatory. | Security/product; default until approved is read-only permitted cache, no queued mutations. |
| D-12 | Decide collaborative rich-text CRDT editing vs comments/presence only; conflict and retention policies. | Collaboration/product; comments/presence are not silently dropped. |
| D-13 | Resolve mobile read-only requirement versus screen boilerplate mentioning approvals. Until decided, mobile approvals are read-only. | Product/security; narrow mobile mutation decision remains blocked. |
| D-14 | Confirm supported production locales, translation ownership, tenant/user locale precedence and time-zone policy. | Product/localization; pseudo-locales do not prove translations. |
| D-15 | Specify entity deletion/restore windows, legal hold, report expiry, audit retention and approval timeouts. | Domain/security/legal; no invented duration defaults. |
| D-16 | Confirm telemetry consent, destination, retention and support-bundle permissions for each profile. | Security/platform; no unsolicited external export. |
| D-17 | Commercial first-party licensing is chosen; contracting identity, third-party notices and distribution blockers still require clearance. | Product/legal; preserve Avyukthi AI and Murthy Ravinder kumar naming supplied by owner. |
| D-18 | Classify every unmapped integration as a user workflow, contextual tool, internal/service-only API, verified alias, optional capability, or approved obsolete route. | Domain owners; blocks catalogue closeout. |
| D-19 | Decide capability discovery/version negotiation, canonical session routes, event retention and durable job contract. | Backend/frontend leads; blocks truthful availability and resumption. |
| D-20 | Optional 3D/Tauri/multi-monitor support requires explicit inclusion, budget and qualification. | Product/platform; excluded from mandatory baseline only with documented source-based applicability. |

When a decision is unresolved, record `BLOCKED_DECISION` against affected clauses and continue independent work. Never replace the question with a default silently. This is how the plan avoids hidden assumptions; a document cannot legitimately manufacture missing business decisions.

## 4. Requirement Ledger and Evidence State Machine

### 4.1 Build the Ledger Before Features

Create a proposed `config/verification/gui-requirements.json` with a schema and parser/checker. Do not overwrite the existing CP registry or change original source IDs. Use stable clause IDs, for example `GUI-SCR-005-A01`, `GUI-MOTION-001`, and `GUI-INT-595-C01`, with backlinks to the parent source and related CP package.

Each record must include source file/hash/line span/exact text, source section, parent ID, normative vs informative classification, applicability, priority, persona, screen, domain owner, dependency IDs, decision IDs, observable behavior, security/data constraints, test scenarios, evidence requirements, current status and unresolved gaps. Record implementation paths separately from proof.

Compound requirements must be split. For example, graph export PNG 2x/4x, SVG, PDF, GraphML, GEXF, JSON and node/edge CSV are separate clauses; export authorization, redaction, large-graph execution and offline notices are additional clauses. One passing PNG test cannot close all exports.

### 4.2 States

`UNTRIAGED -> SPECIFIED -> IMPLEMENTING -> IMPLEMENTED_UNVERIFIED -> BEHAVIOR_VERIFIED -> INTEGRATION_VERIFIED -> RELEASE_ACCEPTED`.

`BLOCKED_DECISION`, `BLOCKED_BACKEND`, `FAILED`, and `STALE_EVIDENCE` remain incomplete. `APPROVED_NOT_APPLICABLE` needs source justification and owner approval; it is never a passing implementation. Mocked component verification may reach `BEHAVIOR_VERIFIED` for purely client-local behavior, but cannot prove a server operation.

Changing a dependency, contract, build, dataset, policy, migration or model invalidates affected evidence. Propagate invalidation through the dependency graph. Keep prior receipts as historical records, not current passes.

### 4.3 Required Evidence Bundle

Store under a proposed `test-results/gui/<run-id>/`, with restricted access and retention because traces can contain data:

1. Manifest binding requirement clauses, source commit plus dirty-tree digest, frontend build hash, lockfile hashes, backend revision/image digest, contract hashes, environment/profile, dataset hashes, model identity and runtime versions.
2. Exact commands, start/end UTC timestamps, exit codes, selected/discovered/executed test IDs, passed/failed/skipped/xfail counts and retry history.
3. JUnit and browser reports, redacted trace/HAR, console/page errors, network failures, server request IDs, and storage/audit assertions.
4. Desktop/tablet/mobile/theme screenshots, interaction video where motion matters, automated layout/contrast checks, and reviewer disposition of visual diffs.
5. Accessibility output plus manual keyboard and AT transcripts; performance frame/heap/bundle traces with measured budgets.
6. Restart, cross-instance, negative authorization, conflict, cancellation, download-integrity and recovery evidence as applicable.
7. Approvals and defect links; cryptographic artifact hashes; manifest validation result. Hashing detects change, not independent execution authenticity. CI provenance and reviewers are separate controls.

Acceptance automation fails closed on a missing artifact, mismatched hash, absent required test, empty selection, unexpected skip, xfail, flaky retry, stale receipt, unknown runtime identity, API interception in a real-integration project, or unapproved manual gate.

## 5. Architecture and Migration Boundaries

### 5.1 Target Layout

Paths below are proposed deliverables, not assertions that files already exist.

```text
apps/web/src/
  app/
    router/                 typed routes, permission guards, route metadata
    providers/              query, identity, tokens, i18n, telemetry
    shell/                  navigation, context bar, inspector, dock, palette
  design-system/
    tokens/                 versioned token source and generated CSS/types
    primitives/             accessible headless wrappers
    components/             application-wide compositions and stories
  entities/
    tenant/ workspace/ source/ ontology/ graph/ job/ report/ agent/
  features/
    auth/ onboarding/ overview/ ask/ graph/ entity/ impact/ changes/
    incidents/ time/ query/ ontology/ meta-graph/ sources/ ingestion/
    quality/ jobs/ agents/ reports/ collaboration/ governance/
    tenant-admin/ branding/ health/ settings/ notifications/ help/ errors/
  shared/
    api/ events/ auth/ telemetry/ i18n/ workers/ security/ test/
  legacy/                   temporary adapters only, with removal criteria
```

Move files only when their imports and behavior are covered. A folder rename is not modularization. Features expose narrow public interfaces; no feature imports another feature's private stores/components. Application composition may connect public feature actions. Reusable domain data belongs in `entities`, and cross-screen infrastructure belongs in `shared`. Use import-boundary lint rules and circular-dependency checks.

### 5.2 State Ownership

| State | Owner | Rules |
|---|---|---|
| Server resources | TanStack Query | Typed keys include tenant, workspace, resource, parameters and relevant permission/version identity. No duplicated authoritative lists in Zustand. |
| Shareable view | Typed URL | Filter, focus, lens and time coordinates; validate on entry. Sensitive query text/PII must not enter URLs. |
| Transient shell | Zustand | Inspector/dock open state, ephemeral selection and drag state; clear on scope changes. |
| Complex workflows | XState, only where justified | Ingestion, publish and long-running query transitions; guard against duplicate side effects. |
| Approved local drafts | Dexie | Principal/tenant/workspace/schema-version namespace; expiry and policy; no credentials. |
| Graph model | Graphology domain adapter | Stable node/edge IDs and separate renderer attributes. Do not copy graph truth into several engines. |
| Layout computation | Worker | Versioned requests, cancellation, bounded memory and stale-result rejection. |

### 5.3 Incremental Migration

1. Inventory current route/mode, controls, APIs, data persistence, hotkeys, exports and tests, including cognitive/dashboards/legacy administration. Assign a destination or approved retention decision.
2. Add the new providers/router around a compatibility route. Do not combine a backend rewrite, framework upgrade and all-screen redesign in one change.
3. Implement shared infrastructure and one production-quality reference workflow first: authenticated scope -> graph -> entity -> evidence -> authorized export.
4. Move one screen family at a time. Compare old/new task outcomes against the same real dataset; retain reversible route flags until accepted.
5. Keep obsolete routes redirectable with validated scope. Do not use an old route to bypass new policy checks.
6. Migrate persisted browser state with versioned, idempotent transforms and export/recovery options. Ambiguous unscoped notes/bookmarks must be quarantined until ownership is established.
7. Retire legacy dependencies/styles/components only when no required workflow imports them and parity evidence passes. Remove Cytoscape as a second primary runtime at that point, not before an equivalent required behavior exists.

## 6. Information Architecture and Low-Complexity UX

Keep the source's 27 screens and routes. Organize navigation by work, not backend package count:

| Navigation group | Screens / contextual destinations |
|---|---|
| Explore | Overview, Ask, Graph; Entity 360 and Meta-graph as context destinations |
| Investigate | Impact, Changes, Incidents, Time, Query |
| Build Data | Sources, Ingestion, Quality, Ontology, Jobs |
| Work Together | Agents, Reports, Collaboration |
| Govern | Governance, Tenant administration, Brand; role-dependent |
| Personal / platform | Settings, Notifications, Help/About; Health for authorized operators |

Do not display all 27 destinations as equal-weight buttons. Use a small persistent primary rail, an accessible labelled navigation drawer, recents and search. One primary action per surface; contextual actions appear near the selected object; advanced controls stay available through progressive disclosure, not hidden behind unexplained gestures.

Shell specifications: 56 px rail, 48 px context bar, 320-480 px inspector, 240-480 px bottom dock, matching source constraints. At 1280 px prioritize the work area, at 1920 permit inspector and dock, at 2560 allow a second inspector only if minimum central width remains usable. Persist panel sizes by principal/workspace; clamp restored sizes after viewport changes. Route changes restore logical focus and announce the page title once.

Mobile is a real companion layout, not a scaled desktop canvas. Read-only entity/report/job/notification views and accessible graph table are first-class. Disable unsupported edits with a concise capability reason. Do not show a tiny editable ontology canvas. Tablet allows one overlay inspector with reversible focus and scroll handling.

### 6.1 Proposed Usability Acceptance Targets

These are additional plan targets requiring UX/product approval, not claimed measurements:

1. Reach an authorized primary destination in at most two navigation selections from the shell; direct command-palette access is an alternative, not the only route.
2. Open entity details from a graph/table selection with one inspect action; return to previous camera/filter/scroll state without reconstructing the investigation.
3. No mandatory action relies on hover, color, a drag gesture, or memorizing a shortcut.
4. Every task has a visible current state, next valid action, cancellation/recovery path and retained context. Show progressive details instead of multiple competing modal stacks.
5. Evaluate the connect-to-first-question, question-to-evidence, incident-to-finding and export journeys with representative users from at least analyst, steward and operator roles. Target at least 90% unassisted task completion, no critical task failure, and document sample size and limitations. Do not invent participants or statistical confidence.
6. Compare time-on-task, navigation errors and unnecessary interactions against the captured current baseline. An attractive screenshot does not establish ease of use.

## 7. Visual System, Assets and Motion

### 7.1 Design Quality Contract

Use the source's exact semantic palette and scale as the initial token baseline. Light-first neutral surfaces with graphite text, teal interaction, amber evidence and red risk must not become a one-hue theme. Dark mode is an alternate mode, not a licence to restore the current indigo/glow aesthetic. Use full-width bands and unframed work areas; cards are for repeated items and genuinely framed tools, never nested page sections. No decorative orbs, glass blur, marketing heroes, excessive gradients or giant dashboard headings.

Visual assets must carry information: the actual authorized graph, real charts, tenant-approved logos, safe source thumbnails and document previews. Do not use generic imagery to disguise missing product state. Fonts, logos, icons, illustrations and sample screenshots require provenance/licence records and local/offline availability. Never fetch a customer-provided asset URL without the approved asset/egress pipeline.

### 7.2 Tokens and Typography

1. Create versioned primitive -> semantic -> component tokens for all source light/dark/high-contrast colors, graph encodings, typography, spacing, radii, z-index, density, focus and motion. Generate CSS variables and TypeScript types from one source.
2. Use Inter/system UI, Noto fallbacks and JetBrains Mono/system mono where licensed/packaged. Body 12/14/16, headings 20/24/32 with specified line heights. Do not scale font size with viewport width or use negative letter spacing.
3. Keep radii within 2/4/6/8 px; shadows only for overlay hierarchy. Use tabular numerals and stable column widths for changing metrics.
4. Source density rows are 44/36/28 px. Preserve minimum actionable target area even in dense rows; compact density must not shrink touch/keyboard usability below acceptance requirements.
5. Test every foreground/background/hover/selected/disabled/focus combination, not isolated hex values. Categorical and severity colors require redundant icon/shape/text meaning. Dimmed graph opacity must not erase the focus/selection or accessible equivalent.
6. White-label overrides may affect approved brand tokens and assets, never semantic risk colors, permission states, focus visibility or source attribution. Validate actual rendered themes before publish.
7. Validate token format against the chosen DTCG revision. The source's JSON seed is illustrative and must not be assumed schema-valid: modern color and duration values need the chosen specification's structures. DTCG is a Community Group specification, not a W3C Recommendation. See [DTCG 2025.10](https://www.designtokens.org/tr/2025.10/format/).

### 7.3 Icon and Control Grammar

Use Lucide for familiar actions, via a typed registry: search, filter, expand/collapse, undo/redo, zoom/fit, save, download, share, copy, play/pause/stop, settings, warning, evidence and permission. Use 12/16/20/24/32 px icons with 1.75 px stroke and optical alignment. Domain/ontology glyphs may extend the registry with vetted assets; never execute arbitrary tenant SVG/HTML.

Tool commands use icon buttons with accessible names and hover/focus tooltips. Modes use segmented controls; colors use labelled swatches; numeric values use inputs/sliders/steppers; binary values use checkboxes/toggles; view changes use tabs; option sets use menus. Unfamiliar or destructive commands retain concise text. Loading controls preserve dimensions, focus and accessible name. Badge color alone must never imply success.

### 7.4 Motion Choreography

| Interaction | Prescribed behavior | Reduced motion / verification |
|---|---|---|
| Hover/focus | 100 ms color/opacity; clear focus ring | Immediate focus; no motion required to find a control. |
| Route transition | 160 ms crossfade after data boundary; no full-screen slide | Immediate replacement; focus/scroll restoration remains correct. |
| Inspector/dock | 160-240 ms, translate at most 12 px, dimensions constrained | Immediate final state; no focus loss or scroll jump. |
| Loading to content | 120 ms dissolve; reserve geometry | No shimmer required; aria-busy ends only on actual settlement. |
| Drag/drop | Border/fill target feedback; ghost tied to pointer | Keyboard move controls and result announcement. |
| Graph layout | 600-1200 ms interpolation, identity/selection preserved | Instant final layout plus persistent selection and summary. |
| Expand/collapse | Expand from parent; preserve centroid on collapse | Direct update, announce added/removed counts. |
| Direction/impact | Directed path pulse; impact hop step 180 ms | Static directed/highlighted path and ordered list. |
| Camera fly-to | 400-700 ms, user-requested only | Instant camera target; preserve orientation. |
| Temporal play | Distinct added/removed/changed marks, explicit playback controls | No autoplay; discrete labelled time steps. |

Use source easing values and spring stiffness 320/damping 30 only for appropriate bounded interactions. Stagger at most six items, at most 30 ms apart. Cap animated elements at 200, edge drawing below 2k edges, and disable graph animation above 10k elements. Cancel superseded animations; never delay a completed task just to finish an animation.

Test `prefers-reduced-motion` at startup and after preference changes, plus a persistent user setting. Do not count CSS rules alone as proof; record interaction behavior in both modes. [MDN reduced-motion reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion).

### 7.5 Layout and Visual Verification Matrix

Use fixed test viewports: 390x844 and 320x568 mobile; 768x1024 and 1024x768 tablet; 1280x800, 1440x900, 1920x1080 desktop; 2560x1440; 3440x1440 ultrawide. Add 400% zoom/reflow and DPR 1/2. Use container queries for independent panels and actual minimum widths, not font-size scaling.

Required modes: light, dark, high-contrast light, high-contrast dark; compact/default/comfortable density; normal/reduced motion; default and deliberately extreme valid tenant branding; English, RTL Arabic, Indic/CJK samples and 30% expanded pseudo-locale. Pairwise sampling is acceptable for routine CI; all high-risk boundary combinations and supported release profiles require explicit coverage. Do not claim a full Cartesian run when only pairwise cases ran.

Check bounding boxes for clipping/overlap, horizontal page overflow, visible focus, scroll ownership, modal stacking, popover collision and long-word wrapping. Test long tenant names, translated buttons, unknown values, large counts, validation messages and disconnected state. Screenshot real populated, empty, busy, failed, denied and stale states. Review all changed visual baselines; never bulk-accept diffs to clear CI.

### 7.6 Analytical Graphics and Chart Grammar

Use lazy ECharts modules for the source-required timeline, Sankey, treemap, sunburst, heatmap and chord views, with a verified implementation choice for any chart not natively supported by the selected version. Do not silently replace an unsupported chart with a decorative approximation. Register a bounded feature gap and use a truthful table until the required implementation passes. Reuse the token/formatting/evidence system, not an independent chart theme.

| Graphic | Appropriate use | Required safeguards |
|---|---|---|
| Timeline | Jobs, events, incidents, changes, temporal graph | Explicit timezone/interval; missing samples; accessible ordered list; zoom does not change meaning. |
| Sankey | Measured flow between stages/types/owners | Consistent units, conserved totals where the domain requires them, labelled partial coverage; no inferred flow disguised as measured volume. |
| Treemap / sunburst | Hierarchical counts/size and ontology/category structure | Stable category IDs, accessible tree/table, breadcrumb drill-up, distinguish zero from unknown. |
| Heatmap | Time/category intensity or adjacency | Labelled axes and legend, accessible cell values, color-blind-safe sequential/diverging palette. |
| Chord | Aggregate relationships between groups | State direction/aggregation and filtering, avoid double counting, provide equivalent matrix/table. |
| Standard trend/bar | Health, throughput, usage and comparisons | Baseline/unit/time-window labels, truthful axes, no unsupported interpolation of missing values. |

All graphics require a data contract, declared aggregation, sample/partial indicators, safe tooltip content, legend filtering, keyboard/table equivalent, responsive resizing and deterministic export. Do not use animation, pseudo-3D or saturation to exaggerate a metric. Test real data changes, no data, one category, outliers, negative values where valid, long labels, high cardinality, dark/high-contrast mode and reduced motion.

## 8. Shared Components and Universal Screen Contract

### 8.1 Component Work Breakdown

| Family | Deliverable and behaviors to demonstrate |
|---|---|
| Commands | Button/IconButton/SplitButton variants, fixed loading width, disabled semantics, focus tooltip, command registry binding. |
| Fields | Text/number/secret/textarea, select/async combobox, multi-select, date/range/time, slider, toggle, checkbox; label/error/help association and server-error mapping. |
| Navigation | Tabs, accordion, breadcrumbs, lazy tree, cursor pagination, palette, recents/favourites; back/forward and keyboard semantics. |
| Data | Virtual grid sort/filter/group/edit/pin/columns/saved-view/export; stable row IDs, accessible counts, selection retained only within scope. |
| Objects | Entity summary, relationship chip, property/evidence inspector, JSON/diff viewer; masking, copy permission and absent-vs-null distinction. |
| Feedback | Status badge, skeleton, progress/ETA, toast, inline error, stale/offline/denied states; unknown never represented as zero or success. |
| Overlays | Tooltip/popover/hovercard/dialog/drawer/sheet; focus restoration, Escape stack, outside click policy, inert background where modal. |
| Creation | Wizard, resumable upload, AND/OR filter builder, code/rich-text/diagram editors; drafts, validation, preview, undo and cancellation. |
| AI | True incremental answer, stop/regenerate, citations, uncertainty, local/external boundary, query/cost preview and approval interaction. |
| Graph | Canvas/legend/toolbar/minimap/layout/lens/timeline/path breadcrumb and equivalent table/tree. |
| Work | Notification, presence, comments, approvals, remediation board, job log/activity tray; permissions and real delivery status. |

Every component has typed props, documented controlled/uncontrolled behavior, applicable default/hover/focus/active/selected/disabled/loading/error/read-only/empty stories, unit behavior tests and accessibility checks. Build stories with realistic content extremes. Avoid a universal mega-component with dozens of unrelated flags.

### 8.2 Contract Applied to Every SCR Work Package

For each screen implement all of these acceptance scenarios, marking truly inapplicable states with a reviewed reason:

1. Authorized deep link, refresh, back/forward, command-palette entry and related-object navigation retain tenant/workspace and intended focus.
2. First-run, loading, empty, partial, populated, validation error, transport/server failure, offline cached, permission denied, stale and development missing-backend states are distinct.
3. Runtime-validated data is sanitized; errors do not reveal inaccessible object existence; authorization changes remove data and cancel work immediately.
4. Inputs validate on blur/submit; async checks debounce 400 ms and ignore obsolete responses. Error summary links to fields. Drafts autosave after 1 s only under approved local-data policy.
5. Successful mutations are confirmed by authoritative state; failure rolls back only permitted optimistic metadata. Retry and repeated clicks do not duplicate business effects.
6. Keyboard and AT users can complete the same task; mobile/tablet behavior is deliberate; all localizable text fits.
7. Authenticated events reconcile by scope and version; gaps become stale state with refetch, not silent loss. Background jobs remain discoverable after leaving the screen.
8. Telemetry uses approved event schemas, never prompts/query text/credentials/raw IDs or graph values. Analytics denial does not break the task.
9. Required backend absence is an explicit blocker. MSW may demonstrate component states only in development/test; it may not provide production success responses.
10. Retain evidence from real actions, server outcome, restart where durable, network trace, screenshots and required manual review. A story or test file is not the receipt.

## 9. Integration and Security Engineering

### 9.1 Capture Contracts Before Client Generation

Enumerate `apps.api.main:create_app` and the composed router factories, middleware, exception handlers, WebSockets, SSE and download responses. Use an isolated data directory and explicit test profile; never seed demo data or mutate a customer database while discovering routes. Capture mounted method/path/operation IDs and normalized OpenAPI. Fail on duplicate/ambiguous operation IDs, unknown success bodies, overlapping handlers and schema drift.

Maintain a separate versioned event/channel contract because OpenAPI alone does not describe replay/cancellation/authentication. Compare current captures with all 735 historical entries, preserving renames/removals/aliases and adding new IDs without renumbering old ones. Catalogue presence does not authorize UI exposure.

Generate TypeScript client types from the reviewed snapshot. Runtime schemas are a separate deliverable: `openapi-typescript` does not itself create Zod validators. Select and test a converter or write small explicit validators with contract coverage; do not cast unchecked JSON as a valid domain object.

### 9.2 Central HTTP Contract

Implement one transport with base URL validation, explicit credentials policy, AbortSignal, trace context, correlation ID, principal-derived scope selection, runtime response validation, error normalization, rate-limit handling and redaction. Application components must not handcraft fetch/auth logic.

Keep successful empty responses distinct from JSON objects and download bytes. For legacy errors normalize 400/401/403/404/409/412/413/415/422/429/500/503, network timeout and cancellation without inventing server guarantees. The source requests RFC 7807-style problems; adopt compatible current [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html), recording the contract update because it obsoletes RFC 7807. Unknown errors remain safe and correlated, not fabricated successes.

Proposed mutation contract: server-verified idempotency key scoped to principal/tenant/operation, request-body hash, documented retention, replayed result, conflict on different payload; ETag/If-Match or equivalent revision checks for concurrent edits. A header the backend ignores provides no safety. Retry only approved idempotent operations; respect Retry-After and the source jittered backoff capped at 15 s. Explicitly bound attempt count and total deadline in the reviewed transport policy.

### 9.3 Identity and Scope

Implement real authorization-code + PKCE browser login with approved IdP integration, state/nonce checks, secure HttpOnly/SameSite cookies where specified, CSRF protection, session renewal/revocation/logout and expiry warnings. Cookie and in-memory token behavior must be decided per deployment; do not persist bearer tokens in localStorage, sessionStorage, IndexedDB, URLs or logs. Development bootstrap access must remain explicit and excluded from production profiles.

Tenant/workspace selections come from authenticated allowed grants. Every server operation validates membership and resource policy again. On scope change, increment a request generation, abort requests/layout jobs, close subscriptions, clear selection/inspectors/caches/drafts according to policy, then hydrate the new scope. Reject late responses tagged with the old generation. Test identical entity IDs in two tenants and two workspaces, including downloads, search, presence, browser history and offline caches.

### 9.4 Events and Jobs

One subscription manager owns authentication, channel scope, heartbeat, jittered reconnect, resume cursor, deduplication, schema/version validation, maximum buffer, visibility behavior and cleanup. Do not use a long-lived bearer in a WebSocket URL. Use approved same-origin cookie or short-lived one-use connection tickets; origin checks and server policy still apply.

Each event envelope must define version, event ID, sequence, tenant/workspace, resource/version, timestamp, request/trace linkage and safe payload. Sequence gaps or retention expiry trigger snapshot/refetch; they must not silently continue as current. Permission revocation closes subscriptions and removes unauthorized cached data. Cancellation must stop server/provider work or report its actual terminal race outcome.

Long jobs need durable submit -> accepted/location -> progress -> terminal result semantics, queued/running/cancelling/cancelled/failed/succeeded states, resume after refresh and worker restart, bounded logs, idempotent retry and authorized result access. UI percentages and ETA derive from measurable progress; unknown stays indeterminate.

### 9.5 Rendering, Assets, Offline and Privacy

Sanitize rich text with a maintained allowlist sanitizer and enforce CSP/Trusted Types with supported-browser fallbacks. Render ordinary graph/source/AI values as text. Do not execute source-provided HTML, script, URLs or tool instructions. Validate link schemes, attachment content type/size and asset MIME; isolate previews where needed.

Caches and persisted views must be scoped, expiring and purgeable. Offline snapshots show capture age and cannot assert live permission. No credentials or unapproved sensitive report exports in Dexie/service-worker caches. Plain browser encryption without a sound key policy is not a security claim. Draft synchronization requires conflict handling, idempotency and revocation revalidation before any queued write is enabled.

Audit sensitive reveal/copy/download/server actions under the authenticated principal. This requires server support; a browser analytics event alone is not an audit trail. Do not log the secret being revealed.

## 10. Missing Backend Contracts: Concrete Closure Instructions

These are contract-design work packages, not claims that the proposed endpoint is already authoritative. Preserve source IDs. Agree schemas, access policy, limits, persistence, migrations and errors in reviewed OpenAPI/event contracts before implementing clients. Suggested fields below are minimum design requirements, not fabricated descriptions of current responses.

### BACKEND-MISSING-001: Session Exchange

Source proposal: `POST /api/v1/session/exchange`. Owner: identity/security. Consumers: SCR-001 and all protected routes. Define protocol-specific exchange and callback validation, issuer/audience, principal, allowed scopes, CSRF material and session expiry without exposing refresh secrets. Add logout/revoke/renew and expiry notification contracts; an exchange endpoint alone is incomplete. Persist/revoke sessions across instances. Prove valid login, replay/state/nonce rejection, expired session, logout, IdP outage, refresh race and tenant-grant removal. Block production bootstrap-token fallback.

### BACKEND-MISSING-002: Current Principal

Source proposal: `GET /api/v1/me`. Return authoritative principal identity, allowed tenant/workspace memberships, effective capability/version references and safe preferences. Do not return other users' profiles or administrative policy internals. ETag/cache policy must account for revoked grants. Prove two distinct principals, forbidden tenant selection, logout cache purge and grant revocation during an open screen. Connect this contract to the workspace lifecycle gap in section 10.21.

### BACKEND-MISSING-003: Onboarding

Source proposal: `GET/PUT /api/v1/onboarding`. Persist versioned step state, workspace/source/job references and draft inputs permitted by policy. Completion derives from actual successful resources, not client checkboxes. Support restart/resume, skipped optional steps with reason, and conflicts between two admins. Never persist raw source credentials in the wizard draft. Prove source failure and cancelled ingestion cannot mark onboarding complete.

### BACKEND-MISSING-004: Saved Graph Views

Source proposal: `POST /api/v1/workspaces/{w}/graph/views`. Complete authorized list/get/update/delete/share contracts, not only creation. Persist schema version, viewport/layout/lens/filter/time/pins, underlying source revision, owner, ACL and revision. Stable IDs must survive graph pagination and restart. Validate stale/missing entities on restore; enforce If-Match conflicts. Prove same view ID in distinct scopes cannot leak, and revoked shared links fail after refresh and from an existing tab.

### BACKEND-MISSING-005: Answers and True Streaming

Source proposal: `GET /api/v1/brain/answers/{id}/events`. Define answer creation, durable status/result, typed delta/evidence/status/error/done events, sequence/replay retention and cancel. Evidence references bind real authorized source revisions; inference mode and unknown confidence remain explicit. Prove first delta arrives before generation ends, disconnect cleanup, stop reaches the provider, resumption without duplication, model outage, expired access and cross-tenant denial. Splitting a completed string into words does not pass.

### BACKEND-MISSING-006: Entity 360

Source proposal: `GET /api/v1/entities/{id}/360`. Return authorized properties, relation-group pagination, provenance, history/issue summaries, source revision and section-level partial/error status. Enforce field masking before aggregation and counts. Define missing/deleted/forbidden semantics without existence leaks. Prove large relation groups, null vs missing, conflicting facts, stale sources and two-tenant identical IDs with real graph data.

### BACKEND-MISSING-007: Impact Plans

Source proposal: `POST /api/v1/impact/plans`. Persist proposed change, baseline graph revision, algorithm/version, scope/cost limits, observed vs inferred impact, severity rationale, test/owner checklist and export-job reference. Add read/update/status lifecycle and approval rules. Recompute or flag stale plans after graph changes. Prove what-if does not mutate production graph, bounded traversal/cancel, no-path results, restart persistence and policy-filtered exports.

### BACKEND-MISSING-008: Incident Workspaces

Source proposal: `POST /api/v1/incidents/{id}/workspaces`. Persist ranked hypotheses, evidence references, investigation steps, owners, findings, comments and decisions, with revisions and audit. Confidence/ranking provenance must be explicit. Support save/resume and concurrent edit conflicts. Prove a hypothesis cannot become a confirmed cause without the specified evidence/decision, and a revoked participant cannot read the saved investigation.

### BACKEND-MISSING-009: Query Lifecycle

Source shorthand `POST /api/v1/query/validate|explain|profile|cancel` means separate reviewed operations, never a literal pipe-containing route. Define dialect capability discovery, validation locations, cost/limits, execution ID, result-frame schemas, pagination, status and cancellation. Separate read-only query permissions from writes and raw administrative Gremlin. Prove unsupported dialect, oversized plan, timeout, cancellation race, policy denial and result download. Saved templates need real durable CRUD.

### BACKEND-MISSING-010: Ontology Publish

Source proposal: `POST /api/v1/ontology/drafts/{id}/publish`. Complete draft create/read/edit, diff, validation, impact preview, approval, migration, atomic publish, rollback and event contracts. Bind approval to the exact draft revision; prevent self-approval where policy requires separation. Persist versions and idempotency. Prove validation failure leaves active ontology unchanged, simultaneous publication conflicts safely, and rollback restores a consistent graph/schema state.

### BACKEND-MISSING-011: Resumable Uploads

Source proposal: `POST/PATCH /api/v1/uploads`. Define initiate/chunk/status/complete/abort operations, permitted MIME/size, offset and checksum rules, expiry, scanner result and quarantine storage. Enforce ownership on every chunk and resume. Reject out-of-order or mismatching chunks without publishing corrupt files. Prove lost network, duplicate chunk, server restart, expired upload, malicious filename, oversize input and unauthorized resume; original unsafe content never reaches a preview.

### BACKEND-MISSING-012: Mapping Review

Source proposal: `POST /api/v1/mappings/{id}/review`. Version inferred entities/relations, proposed matches, acceptance/rejection/edits, reviewer and rationale. Add sample preview, dry-run graph diff, row-level errors and approved publish linkage. Bind review to source/mapping revisions. Prove edit/reject actually changes published output, retry is idempotent, stale review conflicts, and PII stays masked in preview/download errors.

### BACKEND-MISSING-013: Entity Resolution

Source proposal: `POST /api/v1/resolution/actions`. Define candidate retrieval and merge/split/undo commands with impact preview, canonical identity, fact/provenance retention, actor/revision/idempotency and irreversible-case policy. Prove incoming/outgoing links and evidence survive approved merge, undo restores expected identity, concurrent actions conflict, and no cross-tenant candidate is returned. Quality scores without real resolution actions do not close this contract.

### BACKEND-MISSING-014: Agent Run Events

Source proposal: `GET /api/v1/agents/runs/{id}/events`. Define real step/tool/status/error/approval events, redacted payloads, sequence and cancel/resume. Approval binds principal, tenant, exact proposed tool arguments, target revision and expiry; a changed proposal needs a new approval. Prove denied/revoked approval cannot execute, duplicate events do not repeat tools, restart preserves approval state and untrusted content cannot authorize a tool.

### BACKEND-MISSING-015: Report Export Jobs

Source proposal: `POST /api/v1/reports/{id}/exports`. Persist template/input/source/generator/brand revisions, actor/scope, content type, byte size, checksum, expiry and execution state. Complete durable report CRUD, schedule timezone/missed-run policy, approval and download contracts. PDF/DOCX/PPTX/CSV/PNG/SVG must be real formats, not renamed text. Validate files with independent parsers/renderers, inspect representative pages/slides, restart services, try another tenant and expired/revoked download references. Current basic render/download endpoints are reusable but not proof of this complete lifecycle.

### BACKEND-MISSING-016: Collaboration

Source proposal: `WS /api/v1/collaboration/{workspace}`. Define authenticated membership, presence TTL, comment/mention CRUD, ACL-aware sharing, persistence, replay and moderation/deletion policy. Presence is ephemeral; comments/decisions are durable. If Yjs is approved, specify document schema/update validation, persistence/compaction, revocation and offline merge. Prove two real clients, concurrent edits, disconnect/rejoin, role removal and cross-workspace isolation. A local avatar list is not presence integration.

### BACKEND-MISSING-017: Model Data Policy

Source proposal: `PUT /api/v1/tenants/{id}/model-data-policy`. Version classification -> endpoint/model rules, redaction preview, approvals and kill switches. Enforce server-side at every model/tool egress call; the badge only reflects the decision. Prove a prohibited request makes no external call, approved calls produce a redacted manifest, policy change invalidates pending work, and a client flag cannot enable sharing.

### BACKEND-MISSING-018: Brand Publish

Source proposal: `POST /api/v1/tenants/{id}/brand/publish`. Define safe asset upload, draft/version, preview token, contrast/layout validation, publish/rollback and cache invalidation. Prevent semantic-token override, unsafe fonts/SVG, asset URL abuse and cross-tenant preview access. Prove all four themes, long labels, missing font/logo fallback, atomic publication across two clients and rollback after reload.

### BACKEND-MISSING-019: Preferences

Source proposal: `GET/PUT /api/v1/me/preferences`. Persist theme, density, locale, time zone, shortcuts and notification choices with a revision and validation. Separate personal choices from tenant policy; an override cannot enable prohibited telemetry, egress or permissions. Prove two-device conflict handling, reduced-motion preference, invalid shortcut recovery, logout isolation and locale propagation without losing work.

### BACKEND-MISSING-020: About and Licences

Source proposal: `GET /api/v1/about/licenses`. Return build/version, first-party commercial notice, exact shipped component/asset licence references, required texts/notices and downloadable SBOM, with offline delivery parity. Do not present a preliminary index as a cleared inventory. Prove web/static/container artefacts contain matching approved notices. This closes delivery behavior only; legal approval remains a separate gate.

### 10.21 Additional Gaps Revealed by the Journeys

Register these as new linked clauses; the original list of 20 is not a ceiling on backend work:

| Gap | Required contract/design completion | Related screens |
|---|---|---|
| GUI-BE-021 | Workspace list/create/update/archive, memberships, roles, selected context and resource grants | All scoped routes, onboarding, collaboration |
| GUI-BE-022 | Scoped capability manifest with unavailable/disabled/forbidden reasons and schema/build compatibility | Shell, every screen |
| GUI-BE-023 | Graph paging/aggregation/LOD, stable cursors and count estimates with authorization before counts | Graph, meta-graph, entity, overview |
| GUI-BE-024 | Server-supported large graph render/export jobs and format-preserving conversion | Graph, reports, impact |
| GUI-BE-025 | Durable notifications/read state/preferences and permitted send semantics | Notifications, jobs, collaboration |
| GUI-BE-026 | Shared event replay/outbox, job cancellation and resource revision contract across all domains | Jobs, query, agents, ingestion, reports |
| GUI-BE-027 | Verified soft-delete/restore/legal-hold and conflict contracts for destructive screens | Entity, sources, ontology, tenant admin |
| GUI-BE-028 | Versioned local-first/offline synchronisation with reauthorization, only if approved | Settings, drafts, collaboration |

Each receives the same schema/security/storage/negative-test/evidence treatment as BACKEND-MISSING-001..020. Route names for these additions are deliberately not invented here; settle them in the reviewed contract package.

## 11. Screen-by-Screen Implementation Work Packages

All packages inherit section 8.2 in full. The route, persona and integration identifiers in Appendix B preserve the source. Correct semantic mappings through section 2.3 and the contract ledger; do not mechanically call every source-listed operation on screen load. Each numbered task below becomes one or more acceptance clauses, not a single broad checkbox.

### SCR-001: Authentication and Tenant Entry

Route `/auth/*`. Dependencies: GUI-01..06; BACKEND-MISSING-001/002; D-04/05/07.

1. Build focused sign-in, callback, tenant/workspace selection, session-expiring, locked/denied and recovery views. Authentication precedes the tenant workbench; do not render inaccessible workbench data behind the sign-in form.
2. Support approved IdP/local modes, MFA and account recovery without inventing a password flow when the backend lacks one. Permit password-manager paste and accessible authentication. Validate return routes against the same-origin route allowlist.
3. Populate tenant/workspace choices from real grants. Single-choice navigation may streamline entry but must retain visible scope. Logout cancels requests/events, clears sensitive state, and invalidates the server session.
4. Demonstrate valid/invalid login, wrong issuer, expired callback, replay, session renewal race, user cancellation, external IdP outage and revoked tenant access.

Proof: real session exchange and cookie/CSRF behavior, keyboard/AT transcript, redacted network trace, no token in browser persistent stores/URLs, refresh/logout/revocation checks. A token-length badge is not authentication verification.

### SCR-002: First-Run Onboarding

Route `/t/:tenant/onboarding`. Dependencies: SCR-001, SCR-014/015/017; BACKEND-MISSING-003 and GUI-BE-021.

1. Create a resumable sequence: workspace -> source -> connection test -> ingestion -> inferred graph review -> dry-run diff -> publish -> first question. Show only the current step and a compact progress trail; allow safe backtracking.
2. Reuse Sources and Ingestion public components/contracts, not duplicate mini-implementations. Distinguish configured, validated, running, review-required and completed states.
3. Persist progress against real resource/job revisions; retain approved drafts after refresh, interruption and session renewal. Never save credentials as draft state.
4. Run a real connector fixture through publication and the first evidence-backed query. Inject connection failure, upload interruption, rejected mapping and stale draft; none may falsely finish the journey.

Proof: durable wizard reload, source/job IDs and audit linkage, before/after graph assertions, first-answer evidence and a task-flow usability recording. Include this screen in M3/M0 sequencing; the source milestone table otherwise omits it.

### SCR-003: Brain Overview

Route `/t/:tenant/w/:workspace`. Dependencies: identity, scoped aggregates, jobs, saved views.

1. Present a compact operational overview: graph health, recent changes, active jobs, alerts, saved work and direct Ask/Graph entry. Prefer aligned metrics and scannable lists over decorative metric cards.
2. Every count includes scope, observation time and known/partial/unknown semantics. Do not fetch global admin counts for ordinary users or represent unknown denominator as 0%.
3. Add actionable drill-down preserving filters/time; loading or failure of one section must not erase valid independent sections. Refresh invalidates the right keys without losing focus.
4. Test an empty tenant, healthy dataset, partial source outage, stale cache, active job and denied aggregate. Verify every drill-down resolves to the correct scoped screen.

Proof: aggregate-to-detail consistency on real data, permission-filtered counts, stale-state screenshot and two-tenant overview comparison.

### SCR-004: Ask the Brain

Route `/t/:tenant/w/:workspace/ask`. Dependencies: BACKEND-MISSING-005/017, query lifecycle, real model/retrieval prerequisites in CP-19..21.

1. Build accessible composer, scoped suggestions, query/explanation/cost preview, streamed answer, evidence inspector and save/share/export actions. Label deterministic, inferred, simulated-development and unavailable modes accurately.
2. Render true stream chunks and terminal status; Stop cancels computation, Regenerate creates a new answer identity and preserves prior evidence/history. Do not reveal hidden model chain-of-thought; show observable computation/evidence summaries.
3. Bind factual clauses to retrievable authorized evidence; citation focus highlights graph/source and works by keyboard. Missing/revoked evidence becomes an explicit uncertainty state.
4. Test injection-like source content, model absence, egress denial, malformed/duplicate/out-of-order chunks, reconnect, cancel and partial answer. Feedback must not silently train a model.

Proof: timed first/last chunk and provider cancellation trace, source-resolving citations, no-egress denial evidence, accessible incremental announcements and persistent answer reload.

### SCR-005: Graph Explorer

Route `/t/:tenant/w/:workspace/graph?view=&focus=&t=`. Dependencies: GUI-07, BACKEND-MISSING-004, GUI-BE-023/024.

1. Implement primary full-bleed Sigma surface, ontology-driven legend, bounded toolbar, search/filter/lens/layout controls, minimap, inspector and synchronized table/tree. Load actual graph state, not an illustrative bitmap.
2. Support pan/zoom, box/lasso/multi-select, hover/inspect/expand, context actions, pins, clustering, hide/isolate, undo/redo and breadcrumbs. Preserve edge IDs, direction, parallel edges, self-loops, scope and evidence.
3. Make URL and saved views restore camera/filter/lens/time/selection safely. Keep context stable during pagination, worker completion and live updates. Show sampling/aggregation explicitly above supported raw limits.
4. Implement all source layouts and exports through the shared graph package. No automatic re-fit while the user inspects a node; explicit Fit and Fit Selection remain available.

Proof: real-backend exploration/saved-view/restart, graph/table action parity, WebGL pixel checks, 1k/10k/100k traces, invalid/large payload behavior and cross-tenant saved-view/export denial.

### SCR-006: Entity 360

Route `/t/:tenant/w/:workspace/entity/:id`. Dependencies: BACKEND-MISSING-006 and scoped provenance/history.

1. Show stable identity/title/type/status header; tabs for properties, grouped relationships, provenance, history and work/issues. Use a contextual graph preview only when it helps inspect actual relationships.
2. Represent conflicting assertions and source freshness explicitly. Provide permitted reveal/copy/edit, relation expansion, impact and incident actions; unauthorized fields never enter the payload/DOM.
3. Keep relationship groups paginated, maintain selection on return to Graph, and distinguish absent/deleted/forbidden entities without existence leakage.
4. Test large groups, long Unicode values, null/missing properties, stale sources, conflicting facts, denied fields and a deletion race. Destructive actions require server impact preview and policy-driven restore behavior.

Proof: aggregated values match the authorized source graph, deep-link/return continuity, masked-field network assertions and audit-backed reveal/download checks.

### SCR-007: Impact Analysis Studio

Route `/t/:tenant/w/:workspace/impact`. Dependencies: BACKEND-MISSING-007, graph traversal and query cost limits.

1. Compose proposed change inputs, baseline/time/scope controls, concentric hop graph, severity/owner/test checklist and evidence inspector. Show direct vs inferred impacts distinctly.
2. Preview cost and bounds before running; show progress and allow cancellation. Save a versioned plan and expose governed export/approval actions.
3. Let users filter by hop/severity/type and inspect the path supporting each affected item. Preserve the original graph; scenarios must not mutate production state.
4. Test no-path, cycles, truncated traversal, unsupported change type, stale baseline, denied affected entities, concurrent plan edits and cancellation.

Proof: known graph fixture produces expected paths/severity rationale, immutable baseline checks, plan restart/reload and real checklist/report artefacts.

### SCR-008: Change History

Route `/t/:tenant/w/:workspace/changes`. Dependencies: journal/version/diff contracts, governed change transitions.

1. Build filterable time/actor/type/source timeline with side-by-side and inline diff. Color is reinforced by added/removed/changed symbols and accessible labels.
2. Correlate each change to entity, source, evidence, actor and revision; distinguish event time from recorded/observed time. Support safe deep links to exact comparison coordinates.
3. Separate audit viewing from proposing/approving/rolling back changes. An event list is not a restoration capability.
4. Test pagination gaps, identical timestamps, deleted entities, partial history, permission filtering and concurrent transitions. Preserve scroll position on refresh/new events.

Proof: known before/after fixtures and durable journal records match rendered diffs; unauthorized actors/resources are not leaked; time-zone and keyboard comparison checks.

### SCR-009: Incident Root-Cause Workspace

Route `/t/:tenant/w/:workspace/incidents/:id`. Dependencies: BACKEND-MISSING-008 and correlation/evidence services.

1. Present incident summary, ranked hypotheses, causal/evidence graph, investigation steps and a decision log. Keep the current investigative question prominent, not a wall of unrelated metrics.
2. Link each hypothesis to evidence and method; distinguish correlation, inference and confirmed finding. Support ownership, comments, status transitions and export through governed services.
3. Persist the investigation and support explicit base/local/remote conflict resolution for concurrent responders. Never resolve silently by latest UI response.
4. Exercise an incident with ambiguous causes, missing evidence, newly arriving evidence, cancellation and permission revocation.

Proof: saved investigation survives restart; two clients see consistent decisions; confirmed findings have source-backed evidence; unsupported confidence is not fabricated.

### SCR-010: Temporal and Time Travel

Route `/t/:tenant/w/:workspace/time`. Dependencies: scoped snapshot and bitemporal contracts.

1. Provide explicit valid-time/known-time controls where supported, timeline scrubber, compare endpoints, playback controls and synchronized changed-entity list. Do not confuse service uptime with graph history.
2. Preserve graph identities/camera across steps; communicate additions/removals/changes with text and shape as well as color. Respect reduced motion and no autoplay.
3. Separate read-only historical exploration from privileged restore. Restore requires impact preview, durable job, confirmation and rollback procedure.
4. Test unavailable timestamp, time-zone/DST edges, snapshot retention expiry, inconsistent comparison revisions, playback interruption and denied restore.

Proof: fixture changes appear at correct coordinates, snapshot restore changes only authorized scope, reduced-motion step behavior and restart-backed snapshot access.

### SCR-011: Query Workbench

Route `/t/:tenant/w/:workspace/query`. Dependencies: BACKEND-MISSING-009, reviewed dialect capability matrix.

1. Use lazy Monaco with query/template navigation, parameter form, validate/explain/cost/profile actions, results table/graph and console dock. Always show active scope and dialect.
2. Support saved templates/history, result paging/export, bounded execution and cancel. Require explicit authorization and confirmation for mutating queries; ordinary analysts cannot call administrative Gremlin by implication.
3. Keep drafts local only under policy and exclude sensitive query text from URLs/telemetry. Schema validation and result frames must be runtime checked.
4. Test syntax errors with positions, unsupported dialect, timeout/cancel race, excessive cost, partial result, rate limit and a server permission denial after editing.

Proof: each supported dialect executes on its qualified backend; explain/cost correspond to actual plan; cancel reaches execution; restart-persistent templates and download contents match results.

### SCR-012: Ontology Designer

Route `/t/:tenant/w/:workspace/ontology`. Dependencies: BACKEND-MISSING-010, GUI-09, ontology migration/approval services.

1. Build type/relation/property/constraint editing with React Flow and equivalent structured forms/tree. Support multilingual labels, cardinality, validation findings and source/domain packs.
2. Separate draft from active ontology with clear version indicators. Implement diff, impact preview, validation, review, publish and rollback as explicit lifecycle states.
3. Use keyboard alternatives for every drag/reconnect action. Keep transaction boundaries in the backend; optimistic local edits do not publish schema.
4. Test invalid cycles/constraints, stale draft revision, rejected approval, partial migration failure, simultaneous publish and rollback.

Proof: published schema and real graph validation change together, failed publish leaves active state unchanged, approval binds draft hash, and editor/table parity is manually checked.

### SCR-013: Meta-Graph

Route `/t/:tenant/w/:workspace/meta-graph`. Dependencies: typed ontology/count aggregates and shared graph rendering.

1. Visualize types, allowed relationships and authorized instance counts. Distinguish schema edges from data edges; add scope/version legend and drill-down to filtered instances.
2. Provide type search, hierarchy/table equivalent, relationship inspection and read-only comparison of ontology versions. Editing opens SCR-012 with a governed draft.
3. Treat counts as unknown/partial when unsupported; never infer instance totals from a sampled graph.
4. Test zero-instance types, multilingual labels, high fan-out schema, hidden types and changing schema revision during exploration.

Proof: counts and drill-down agree on the same scope/revision; no mutation occurs during exploration; keyboard access and selection survive layout changes.

### SCR-014: Sources and Connectors

Route `/t/:tenant/w/:workspace/sources`. Dependencies: source registry/catalogue and connector capability contracts.

1. Present source list with health/freshness/owner/status, searchable connector catalogue and a schema-driven setup drawer. Reuse `ConnectorSetupWizard` behavior only after validating security and contracts.
2. Implement create/edit/test/discover/dry-run/baseline/sync/pause/resume/schedule/delete where the connector actually supports them. Hide unsupported modes with truthful capability state; no successful empty test response.
3. Use secret references and write-only credential fields; masked placeholders cannot accidentally overwrite secrets. Test connection is a real authorized backend operation.
4. Exercise valid/invalid credentials, unreachable source, rate limit, schema drift, pause during sync, retry and deletion with dependent jobs.

Proof: a real test fixture connector produces expected ingested objects; credentials absent from DOM/logs/receipts; acquisition state survives restart and other tenants cannot inspect the source.

### SCR-015: Ingestion and Mapping Studio

Route `/t/:tenant/w/:workspace/ingestion`. Dependencies: BACKEND-MISSING-011/012, job lifecycle, source/profile contracts.

1. Build upload/source selection -> profiling -> mapping -> inferred entities/relations review -> dry-run diff -> publish pipeline. Use source preview, mapping canvas and accessible mapping grid with shared state.
2. Show field types, key candidates, relationship confidence/method, validation and per-row errors. Reviewer accept/reject/edit actions must affect the publish plan.
3. Support resumable uploads, cancellation, drafts, restart recovery and explicit migration conflicts. No automatic publish after a merely successful parse.
4. Test duplicate chunks, corrupt checksums, scanner rejection, encoding errors, changed source revision, invalid mappings and partial job failure.

Proof: actual file/API records produce the reviewed graph and provenance; rejected items are absent; resume/cancel/restart and error-file contents are verified without PII leakage.

### SCR-016: Entity Resolution and Quality

Route `/t/:tenant/w/:workspace/quality`. Dependencies: BACKEND-MISSING-013, identity candidates, conformance and validation findings.

1. Provide candidate-pair comparison, property/evidence conflicts, rule findings, merge/split preview, steward decisions and remediation queue. Distinguish quality dimensions; never merge them into unsupported certainty.
2. Support accept/reject/edit/merge/split/undo only with backend semantics and impact preview. Keep source references and canonical IDs visible and accessible.
3. Persist decision rationale and owner, allow filters/bulk review only with per-item results, and require separate confirmation for destructive batches.
4. Test false positive candidate, conflicting provenance, incoming links, concurrent merge, rejected undo and cross-tenant matching attempt.

Proof: canonical graph and evidence are correct after merge/split/undo; counts reflect real checks; failed/skipped bulk items remain visible and recoverable.

### SCR-017: Pipelines and Jobs

Route `/t/:tenant/w/:workspace/jobs`. Dependencies: GUI-06, GUI-BE-026; verify actual replacement for historical INT-735.

1. Build filterable durable jobs table, DAG/step view, bounded logs, progress, retries/cancel/rerun and checkpoint/recovery actions. Render unknown ETA as unknown.
2. Define a single job-state interpretation across activity tray, screen and notifications. Leaving the screen must not cancel a job unless the user explicitly chooses that operation.
3. Support events plus verified polling fallback, reconnect/resume, retention expiry and worker restart. Retry/cancel outcomes must match server state.
4. Test queued/running/cancelling/terminal races, duplicate updates, gaps, partial batch completion and denied job IDs.

Proof: two clients and restarted API see the same durable job; cancellation stops work or reports already-finished outcome; tenant-filtered logs and event resumption have trace evidence.

### SCR-018: Agents

Route `/t/:tenant/w/:workspace/agents`. Dependencies: BACKEND-MISSING-014/017, run/tool/approval services.

1. Present agent catalogue/configuration, permitted tool scopes, run history, live trace, evidence and approval queue. A workflow editor uses React Flow only for real editable definitions.
2. Label each execution mode and tool effect; approvals display exact target, changed fields, classification and expiry. Never reduce approval to a generic Allow button with hidden arguments.
3. Implement stop/retry/resume only when the backend contract supports safe semantics; preserve traces and approval decisions after restart.
4. Test injection-like tool output, disallowed tool, invalid/expired approval, changed arguments, repeated approval message, model outage and kill switch.

Proof: denied operations cause no side effect; approved operations happen once with the expected revision; live traces are real, redacted and scoped.

### SCR-019: Reports and Dashboards

Route `/t/:tenant/w/:workspace/reports`. Dependencies: BACKEND-MISSING-015, real reports INT-595..603, source/provenance and branding.

1. Provide report list, template chooser, parameter form, evidence appendix, preview/editor, approval/status and version history. Separate report content from operational dashboards and admin exports.
2. Add schedule timezone, recurrence, next/last run and missed-run/failure visibility. Wire durable scheduler execution; persisting a schedule definition alone does not satisfy recurrence.
3. Support required document and graph formats, authorized downloads, share/revoke/expiry and tenant branding without fabricating chart data.
4. Test renderer absence, malformed/stale evidence, revoked permission, corrupt artefact, schedule overlap, interrupted render and two-client edits.

Proof: independently parsed and visually inspected PDF/DOCX/PPTX/HTML/Markdown/JSON and other required export artefacts; content/checksum match; real schedule execution, restart and cross-tenant denial.

### SCR-020: Collaboration

Route `/t/:tenant/w/:workspace/collaboration`. Dependencies: BACKEND-MISSING-016, workspace membership and notification contracts.

1. Implement discussion threads, contextual comments, mentions, shared investigations/views and presence in context, with a consolidated activity view rather than a second disconnected application.
2. Show delivery/pending/failed states truthfully; presence expires on disconnect. Mention search is permission-filtered and sharing exposes exact scope/expiry.
3. Add CRDT rich-text collaboration only after D-12 and backend persistence/security pass. Local optimistic comments require server confirmation and conflict/retry handling.
4. Test two clients editing/commenting, disconnect/reconnect, duplicate delivery, deleted object, removed member and revoked shared link.

Proof: durable comments remain after restart, transient presence expires, no cross-workspace updates leak, and concurrent edits follow the approved conflict policy.

### SCR-021: Governance and Security

Route `/t/:tenant/admin/governance`. Dependencies: policy enforcement, BACKEND-MISSING-017, audit/privacy contracts.

1. Organize users/roles/permissions, classifications, model/egress policy, approvals and audit into clearly labelled tabs. Display effective permissions and inheritance with an explain view.
2. Provide policy draft/diff/preview, impact on affected principals/resources, review and publish. Prevent self-escalation through backend policy, not hidden buttons.
3. Add redaction preview, kill switch, audit search/export and sensitive reveal controls only with appropriate permissions; do not fetch global user lists for ordinary settings.
4. Test deny-by-default, revocation across clients, cross-tenant admin access, separation of duties, stale policy version and a client tampering attempt.

Proof: table-driven role/action/resource checks through real services, forbidden mutation has no side effect, egress denial has no external traffic, and sensitive operations have safe actor-bound audit records.

### SCR-022: Tenant Administration

Route `/platform/tenants/:tenant`. Dependencies: tenant lifecycle/isolation/quota/licensing/backup services, D-05/06/15.

1. Separate platform-wide tenant operations from tenant-admin self-scope. Show lifecycle state, isolation placement, workspace/membership, quotas/usage, storage, entitlement and backup freshness.
2. Implement provision/configure/suspend/resume/export/delete/restore only as approved server jobs with impact preview and confirmation. Clients must not directly consume/refund usage counters.
3. Make destructive/restore transitions explicit and resumable, with legal-hold and retention behavior. Never show a licence badge as legal clearance.
4. Test partial provisioning, suspend during work, quota exhaustion, failed backup/restore, tenant-bound admin path tampering and deletion under hold.

Proof: real isolation profile changes and lifecycle records survive restart; another tenant is unaffected; backup/restore verifies data and authorized access, not just a success message.

### SCR-023: White-Label Studio

Route `/t/:tenant/admin/brand`. Dependencies: BACKEND-MISSING-018, tokens, asset policy and localization.

1. Provide brand-token controls, asset manager, terminology/localization inputs and live previews of authentication, graph, tables, forms and report pages in all four themes.
2. Use swatches, font selectors and actual upload previews; show validation near the failing override. Keep semantic colors and security states locked.
3. Implement draft/save/preview/publish/rollback with version and reviewer information. Publication updates all clients atomically without flashing unstyled or another tenant's theme.
4. Test low contrast, long brand name, missing font, oversized/malicious asset, invalid semantic override, concurrent edit and rollback.

Proof: rendered contrast/layout and asset loading checks, cross-client/version consistency, offline font/logo fallback, and brand-isolation negative tests.

### SCR-024: Platform Health

Route `/platform/health`. Dependencies: authorized health/metrics/jobs/store/model/node contracts and qualified deployment profile.

1. Display service topology/status, queues, graph/storage health, model availability, replication/recovery, capacity and recent incidents using real observations and timestamps.
2. Prioritize actionable fault lists and drill-down. Charts include units, aggregation windows, missing samples and accessible tables; never seed random telemetry to fill empty space.
3. Privileged operations such as drain/reset/restart/restore remain explicit commands with policy checks and audit. Polling must not trigger mutating checks automatically.
4. Test unavailable subsystem, partial response, stale telemetry, high load, role denial and recovery. Mask sensitive operational configuration.

Proof: induced service fault appears correctly, recovery updates after actual health restoration, no unauthorized metrics leak and chart values match raw fixture observations.

### SCR-025: User Settings

Route `/settings`. Dependencies: BACKEND-MISSING-002/019 and approved account/token services.

1. Provide personal profile, appearance/density, reduced motion, locale/time zone, keyboard shortcuts and notification settings. Do not mix tenant-wide feature flags or source profiling into this screen.
2. Preview appearance changes immediately but show persistence status. Reset restores approved defaults; policy-enforced settings explain their constraint.
3. Token creation/revocation is available only if approved for the user; show new secrets once, never persist them in browser storage or analytics.
4. Test two-device conflict, offline preference edit policy, invalid shortcut collisions, locale overflow, failed save and logout followed by a different principal.

Proof: real preference persistence after reload/relogin, scope isolation, reduced-motion change applied to running interactions and safe secret handling where supported.

### SCR-026: Notifications, Help and Licences

Routes `/notifications`, `/help`, `/about`. Dependencies: GUI-BE-025, BACKEND-MISSING-020 and scoped job/activity links.

1. Build notification inbox with read/unread/filter/group controls and authorized deep links. Opening another recipient's path must not expose their inbox.
2. Help includes searchable task documentation and the actual rebindable shortcut map. Use a dedicated help surface, not permanent instructional prose throughout application chrome.
3. About shows exact build/profile, commercial first-party notice, original third-party notices and SBOM/download availability, including offline access. Entitlements and copyright notices are distinct concepts.
4. Test deleted/forbidden notification targets, duplicate delivery, read-state sync, offline help, missing notice artefact and long translated content.

Proof: read state persists, server recipient authorization holds, deep links preserve scope and shipped notices match the approved build inventory byte-for-byte where applicable.

### SCR-027: Global Errors and Recovery

Route `/errors/:code` plus route-level boundaries. Dependencies: transport normalization, shell and minimal safe health contract.

1. Provide distinct unauthenticated/forbidden/not-found/offline/incompatible-version/server-failure routes and local error boundaries. Keep valid neighbouring work available when only one panel fails.
2. Show safe correlation/support reference, retry/back/re-authenticate actions and draft recovery where permitted. Do not expose stack traces, credentials or protected object identity.
3. Recover from lazy-chunk failure, service-worker/build mismatch and WebGL context loss. Retry never repeats unsafe mutations or loops indefinitely.
4. Inject each failure during navigation, mutation and background work. Focus the recovery heading/action, preserve safe context and verify keyboard exit.

Proof: reproducible fault injections against the release build, correct normalized states, no mutation on error rendering and restored task after the underlying fault clears.

## 12. Ordered Engineering Packages

Package owners below are roles, not invented assignments to named people. Before execution, record the responsible person/agent and reviewer. Parallel work is possible only after shared contracts are agreed and write ownership is explicit; do not spawn agents without user authorization. A later package may prototype against development contracts but cannot claim integration completion before its dependencies pass.

### GUI-00: Source Ledger and Current-State Baseline

Priority P0. Owner: verification lead. Dependencies: none. CP linkage: CP-00/01/02/35.

1. Verify the source hash and parse all 23 sections, 27 screens, 735 integrations and 20 missing-contract IDs. Detect duplicate/missing IDs and table parse failures; compare the two screen mappings, including INT-735.
2. Create the clause ledger/schema/checker described in section 4. Preserve original text and separate historical status, present observation and acceptance status.
3. Inventory existing GUI workflows and browser data; capture baseline screenshots/task paths and inspect current backend capabilities without mutating production data.
4. Resolve or register decisions in section 3. Classify all 584 unassigned integrations and correct suspect screen assignments with domain owners.
5. Produce a dependency graph, approved mandatory/optional scope and initial defects. Every later change links back to clause IDs.

Deliverables: proposed `config/verification/gui-requirements.json`, `docs/gui/decisions/`, current-state inventory and baseline evidence. Exit: exact inventory reconciliation; no orphan mandatory clause; unresolved policy is visibly blocked. Rollback: retain immutable inputs and prior ledger versions; never regenerate away adverse evidence.

### GUI-01: API, Event and Capability Contracts

Priority P0. Owner: backend/frontend contract leads. Dependencies: GUI-00. CP linkage: CP-03..11/24.

1. Capture the actual composed OpenAPI and transport routes, review status/body/auth behavior, normalize and commit a versioned snapshot.
2. Design all BACKEND-MISSING and GUI-BE families with schema/error/authorization/storage/version/cancel/replay semantics. Reuse genuine existing services rather than duplicate them under new names.
3. Add contract tests using real API factories and the selected persistent backend. Separate fake transport fixtures from runtime tests.
4. Implement capability discovery and compatibility negotiation; permissions are evaluated independently from installed features/licence availability.
5. Generate clients/runtime validators and add CI schema-diff review. A removed operation must identify affected screens, migration and rollback.

Deliverables: proposed `contracts/gui/openapi.json`, event schema files, client generation tooling and contract receipts. Exit: each exposed operation has a complete reviewed contract and a real positive/negative test. Rollback: versioned clients/contracts and compatibility window, not silent response-shape coercion.

### GUI-02: Strict Frontend Toolchain

Priority P0. Owner: frontend platform. Dependencies: GUI-00, D-03. CP linkage: CP-24/36.

1. Introduce strict TypeScript, exact dependency resolution, ESLint/import-boundaries, formatter, unit/component runner and build analysis. Keep old JavaScript isolated behind typed adapters during migration.
2. Add proposed scripts `typecheck`, `lint`, `test:unit`, `test:component`, `test:contract`, `test:e2e:real`, `test:visual`, `test:a11y`, `test:perf`, `check:bundle`, `check:gui-evidence`. Document exact commands after implementation; they do not exist merely because this plan names them.
3. Add Storybook, Testing Library, MSW and axe incrementally. Use separate mocked and real-integration project configurations and artifacts.
4. Define exact Node/browser/package-manager profiles, offline dependency packaging and reproducible clean install/build checks.
5. Eliminate broad `any`, unchecked JSON casts and disabled lint/type rules from new modules; exceptions need a documented bounded migration issue.

Deliverables: updated package/lock/config and runnable scripts. Exit: clean install, type/lint/unit/build and fixture boundaries pass. Rollback: prior lockfile/build remains reproducible; no forced peer-resolution workaround.

### GUI-03: Tokens, Assets, Icons and Motion System

Priority P0. Owner: design-system lead. Dependencies: GUI-02, D-02. CP linkage: CP-24/28.

1. Implement section 7 tokens, four themes, three densities, typography/local fonts and licence-aware asset pipeline.
2. Add Lucide registry and compatibility adapter; map every current icon name and meaningful semantic state.
3. Create Motion wrappers using shared duration/easing tokens, reduced-motion hook and animation-budget controller. Avoid two competing animation systems.
4. Replace hardcoded decorative styles in migrated components only; leave unrelated legacy styles until their consumers migrate.
5. Build representative graph/table/form/report/theme stories and secure branding validation. Obtain visual review before scaling.

Deliverables: `src/design-system/tokens/`, icons/motion primitives, theme/asset manifest and reviewed reference screenshots. Exit: contrast, layout, typography, motion and forced-colors checks pass. Rollback: versioned token package; restore previous valid tenant theme if publish validation fails.

### GUI-04: Shell, Routing, Identity and Scope

Priority P0. Owner: frontend/security. Dependencies: GUI-01..03, identity backend. CP linkage: CP-04..08/24.

1. Build typed routes, lazy feature loading, public/authenticated/admin boundaries, route titles, safe return URLs and deep-link restoration.
2. Implement shell/navigation/context bar/inspector/dock/palette and responsive layouts without removing current workflow entry points prematurely.
3. Integrate real identity/current-principal/tenant/workspace grants, session expiry and logout. Add scope-generation cancellation and cache/subscription purge.
4. Add capability-aware navigation and discoverable action reasons; never rely on UI hiding as authorization.
5. Complete SCR-001/027 and the shared settings/context hooks needed by every screen.

Exit: real login -> authorized route -> scope switch -> logout, keyboard shell, denied deep links and no late-response contamination. Rollback: route flag may restore old UI only if it still enforces current authentication and scope policy.

### GUI-05: Shared Components, Forms and Editors

Priority P0/P1. Owner: component maintainers. Dependencies: GUI-02/03. CP linkage: CP-24.

1. Implement section 8 families using native HTML/Radix behavior, typed contracts and controlled state ownership.
2. Add form schema/error mapping, dirty-navigation protection, policy-approved drafts, stepper lifecycle and undo/redo commands.
3. Build virtual grid/tree with stable identity and accessible row position/count, filter builder, inspector and bounded overlays.
4. Lazy-load Monaco/Tiptap/React Flow only for consumers requiring them; define safe plugins, paste/sanitization and keyboard alternatives.
5. Exercise all applicable component states, localization extremes, focus transitions, data-volume boundaries and responsive layout stories.

Exit: story inventory matches component-state ledger and executed tests; no primitive silently drops ARIA attributes/ref/keyboard support. Rollback: per-component adapters allow migration without breaking unchanged consumers.

### GUI-06: Transport, Queries, Events and Job Lifecycles

Priority P0. Owner: frontend/backend platform. Dependencies: GUI-01/02/04. CP linkage: CP-07/09/10/11.

1. Implement central HTTP/error/security layer, typed query-key factories and exact mutation invalidation.
2. Implement one authenticated subscription manager and job lifecycle adapter; add abort/reconnect/sequence/revision handling and polling fallback.
3. Use explicit state machines only where multi-step lifecycle benefits; model partial success, cancellation races, rollback and recovery.
4. Remove direct ad hoc fetch/socket usage from migrated features; prevent duplicate subscriptions after remount/StrictMode/HMR.
5. Test malformed payload, stale event, expired session, revoked grant, 429/Retry-After, server restart and duplicate mutation delivery.

Exit: real server lifecycle proofs with scoped events; no fire-and-forget success, unsafe automatic retry or unbounded log/event buffer. Rollback: protocol-version compatibility and fallback to bounded truthful polling, not a mock stream.

### GUI-07: Graph Engine and Exploration

Priority P0. Owner: graph frontend/performance. Dependencies: GUI-03..06, GUI-BE-023/024. CP linkage: CP-13/23/24/25/32.

1. Normalize graph IDs/types/properties/evidence into one Graphology model supporting directed parallel edges and self-loops. Validate dangling endpoints and duplicate IDs instead of swallowing exceptions.
2. Run ForceAtlas2/ELK and approved layout algorithms in workers using maintained libraries. Implement cancellation, deterministic test seeds, progress, bounded iterations and stale-version rejection.
3. Implement LOD, label collision rules, categorical/metric/severity encodings, clusters/meta-edges, centrality/community/path overlays and semantic zoom.
4. Implement source interactions, accessible equivalents, saved view lifecycle and all export formats. Maintain camera/selection through data and renderer changes.
5. Add genuine WebGL context/pixel/interaction tests and declared dataset/hardware traces before advertising 10k/100k support.

Exit: SCR-005/006/013 and overview graph integration pass; required graph semantics match real datasets; performance and AT alternatives qualify. Rollback: preserve saved-view schema/version and safe read-only table fallback; do not silently switch to an incompatible renderer.

### GUI-08: Intelligence and Investigation Screens

Priority P0/P1. Owner: intelligence frontend + domain services. Dependencies: GUI-04..07, missing contracts 005..009. CP linkage: CP-14/17..22/24.

1. Implement SCR-004/007/008/009/010/011 through real query/retrieval/causal/temporal services.
2. Bind evidence, model/runtime identity, source revisions, uncertainty and privacy boundary to each result.
3. Add real streaming/cancellation, cost guards, saved plans/templates/investigations, history and governed exports.
4. Cover negative and ambiguous cases without synthetic certainty or invented citations. Keep simulation explicitly development-only where required.
5. Run end-to-end question-to-evidence, change-to-impact, incident-to-finding and temporal-comparison journeys.

Exit: domain outcomes verified, not only page rendering; model downtime and missing services remain visible blockers. Rollback: retain durable records and disable unavailable capabilities truthfully; never replace failed runtime output with success-shaped demo content.

### GUI-09: Data and Stewardship Screens

Priority P0/P1. Owner: data/stewardship frontend + ingestion/ontology services. Dependencies: GUI-04..07, contracts 003/010..013. CP linkage: CP-12/15..18/24.

1. Implement SCR-002/012/014/015/016/017 using shared connectors, editors, workflow and job infrastructure.
2. Complete actual source test/upload/profile/inference/review/dry-run/publish, not disconnected wizard forms.
3. Enforce revision-bound approval, source provenance, secret handling and idempotent publish/merge actions.
4. Test long-running job continuation, worker/API restart, conflicting reviewers, bad rows/files and rejected publish.
5. Complete the first-source-to-first-question journey against a real persistent backend.

Exit: graph contents and provenance match the reviewed plan after restart; failed actions leave recoverable state. Rollback: versioned mapping/ontology and durable checkpoints; never clear original data automatically to repair a failed migration.

### GUI-10: Agents, Content and Collaboration

Priority P1 with P0 safety. Owner: workflow/content teams. Dependencies: GUI-06/08/09, contracts 014..016. CP linkage: CP-10/22/25/26.

1. Implement SCR-018/019/020 with real run approvals, report records/renderers/scheduler and authenticated multi-client collaboration.
2. Share approval/evidence/activity primitives, but retain distinct domain state transitions and policies.
3. Complete export checksums/expiry/revocation, schedule concurrency and failure alerts, comments/mentions/presence lifecycle.
4. Run tool denial/replay, independent document parsing/render review and two-browser collaboration scenarios.
5. Gate optional CRDT work separately and prove convergence/persistence if included.

Exit: durable and authorized outcomes survive service restart; no fake presence, mock report bytes or approval without enforced policy. Rollback: backwards-compatible document/report/run schemas and explicit draining of incompatible live sessions.

### GUI-11: Enterprise and Personal Surfaces

Priority P0/P1. Owner: administration/security/frontend. Dependencies: GUI-04..06, contracts 017..020 and tenant services. CP linkage: CP-05/06/09/24/28/30/31/33.

1. Implement SCR-021..026 and approved administrative destinations for existing workflows.
2. Separate platform authority, tenant authority and personal settings; ensure deep links and direct API calls enforce the same policy.
3. Implement real brand preview/publish/rollback, model egress enforcement, tenant lifecycle/backup/quota views and actual health metrics.
4. Complete local/offline notices, build metadata, SBOM linkage, notification persistence and help/shortcut search.
5. Test policy revocation across clients, tenant suspension, asset abuse, extreme branding and each supported deployment profile.

Exit: no admin capability exposed by ordinary screen load; notices/build/profile data match shipped artefacts. Rollback: valid prior policy/theme and reversible lifecycle operations under documented operational procedures.

### GUI-12: Accessibility, Localization and Usability

Priority P0, continuous rather than end-only. Owner: accessibility/UX/localization. Dependencies: begins GUI-03 and follows every screen. CP linkage: CP-24.

1. Apply keyboard, landmarks, focus, accessible names, error summaries, status announcements, non-color encodings and drag alternatives to every component/task.
2. Externalize ICU messages; implement number/date/unit/currency formatting, approved locale fallback, RTL layout rules and local font packaging.
3. Execute zoom/reflow, forced colors, reduced motion, pseudo-expansion and input-modality tests throughout feature delivery.
4. Manually qualify NVDA/Chrome, JAWS/Edge and VoiceOver/Safari with recorded versions and task transcripts. Unavailable AT is a blocked manual gate, not an automated pass.
5. Run section 6.1 usability tasks, retain findings and fix critical friction before release.

Exit: section 14 gates pass for supported routes/profiles; no serious/critical automated findings and no unresolved mandatory manual failure. Rollback: simplify the interaction while preserving capability, not remove accessible alternatives to improve visual scores.

### GUI-13: Offline, Privacy and Browser Security

Priority P0. Owner: security/frontend. Dependencies: GUI-04..06, D-11/15/16. CP linkage: CP-08/09/27.

1. Implement policy-scoped caches/drafts, retention, purge, schema migration and truthful capture-age/offline states.
2. Enforce CSP/sanitization/Trusted Types where supported, safe links/assets, secret storage restrictions and telemetry redaction.
3. Add approved sync-safe actions only after durable queue/idempotency/conflict/revocation contracts pass. Otherwise remain explicitly read-only offline.
4. Test tenant switch with pending requests, logout/offline reopening, revoked access, XSS/prompt injection, poisoned cache and incompatible schema migration.
5. Verify no unintended external network requests in local/air-gap profiles, including fonts, error reporters and worker bundles.

Exit: concrete threat scenarios and network/storage assertions pass. Rollback: disable sync/cache feature and preserve quarantined drafts safely; never expose old scope as a fallback.

### GUI-14: Performance and Rendering Qualification

Priority P0 for advertised scale. Owner: performance/frontend/backend. Dependencies: GUI-02/07 and D-09. CP linkage: CP-32.

1. Establish reproducible small/medium/large/adversarial datasets and fixed hardware/browser/GPU profiles.
2. Measure shell/route bundle costs, LCP/INP/CLS, graph first paint/frame times, memory, worker tasks, network payload and interaction latency.
3. Lazy-load graph/editor/chart engines, virtualize bounded lists, cache safe immutable ontology by ETag and release workers/GPU buffers on scope/unmount.
4. Run node/edge-density variations, labels, selected/highlighted subsets, streaming updates, repeated screen transitions and WebGL context loss.
5. Store raw traces and analysis; prevent budget relaxation without an approved requirement change.

Exit: section 15 budgets hold on declared profiles, not only a developer desktop. Rollback: reduce exposed scale with explicit refinement/aggregation limits; do not advertise unmeasured performance.

### GUI-15: Evidence, CI and Release Gates

Priority P0. Owner: verification/release. Dependencies: GUI-00/02; grows with every package. CP linkage: CP-02/35/36.

1. Implement source/build/runtime-bound receipts and the fail-closed verifier; reuse existing CP evidence machinery where it genuinely matches browser requirements.
2. Add pipeline stages for static checks, unit/component, schema/contracts, real integration, visual/a11y, performance/security and artifact integrity.
3. Separate intercepted/mock tests from real-backend projects. Record fixture/server/DB identities and prohibit route fulfilment in real journeys except explicitly labelled failure-injection cases.
4. Add verifier negative tests: remove a required test/artifact, alter a source hash, inject a mock, skip a clause, change the backend or introduce a flaky retry; each must block acceptance.
5. Collect manual approvals and unresolved external gates without pretending they were executed by CI.

Exit: gate can reject false positives as well as accept valid evidence; exact release candidate has complete required receipts. Rollback: retain previous signed/approved release evidence; never rewrite failed evidence as passed.

### GUI-16: Packaging, Migration and Cutover

Priority P0. Owner: release/platform. Dependencies: all mandatory earlier packages. CP linkage: CP-31/33/35/36.

1. Build immutable browser/container/installed artefacts for the approved profiles with contracts, fonts/assets, workers and notices included.
2. Test deep-link refresh at the actual reverse proxy, API/WS/SSE routing, compression/cache policy, cookie/CSP headers and mixed-version compatibility.
3. Migrate browser/server state through backed-up idempotent steps; run upgrade and rollback rehearsals on representative data.
4. Roll out by approved capability/cohort flags with telemetry/health checks. Flags cannot bypass permission or required completion gates.
5. Remove legacy code/dependencies only after parity and rollback windows; update help/runbooks/source catalogue and archive final receipts.

Exit: release acceptance in section 18; no unresolved mandatory feature or manual approval. Rollback: documented versioned artefact restoration, compatibility/read-only mode and safe data recovery; never destructive reset.

### GUI-17: Optional Desktop, 3D and Advanced Collaboration

Priority explicitly optional until D-12/20. Owner: product/platform/graph. Dependencies: accepted 2D/browser baseline.

1. If approved, qualify Tauri capabilities, signing/update/offline packaging, permission scopes, inspector pop-outs and multi-monitor state.
2. If approved, implement Three.js 3D as a separate exploratory lens with full-bleed scene, real data, camera controls, accessible 2D/table equivalent and explicit performance budgets.
3. If approved, qualify Yjs update authorization, persistence/compaction, convergence and offline/revocation behavior beyond simple comments.
4. Each optional capability has its own requirement ledger, security review, actual device/runtime test and retained evidence.

Exit: only the specifically approved optional profile is claimed. Missing optional work must never inflate mandatory completion, and enabling the flag does not qualify the feature.

## 13. Graph-Specific Acceptance Specification

### 13.1 Rendering and Layout

Use Sigma WebGL as primary renderer and Graphology as the single graph model. At <=1k elements, rich overlays may be used without replacing the authoritative model. At 1k-100k use workers and LOD; above 100k require backend aggregation/sampling and display the reduction. Define whether a measured threshold counts vertices, edges or total elements in each benchmark; preserve the source's node-specific performance targets separately.

Implement ForceAtlas2, ELK layered, radial ego, concentric hop, circular, grid, timeline, geographic layout only when valid coordinates exist, and adjacency matrix for dense topology. Prefer established layout libraries; do not carry forward the current synchronous pairwise force implementation as evidence of scale. Map impact -> concentric, lineage -> layered, entity -> radial, time -> timeline unless a saved user choice applies.

Graph-fit rules: 48 px padding, explicit fit selection/path, zoom .05-16, zoom-to-cursor, labels hidden below .35 and abbreviated .35-.7, full above .7, label size clamped 10-16 px, ResizeObserver debounce 100 ms and DPR capped at 2 except explicit export. Do not apply camera animation or auto-fit after every live update.

### 13.2 Data and Interaction Cases

Test an empty graph, singleton, disconnected components, cycle, self-loop, parallel directed edges, reverse edges, long/multilingual labels, missing endpoint, duplicate ID, hidden classified node, high-degree hub, dense subgraph and rapidly changing topology. Ensure server filtering happens before counts, paths, aggregates or export; frontend hiding is not isolation.

Selection, expansion, pinning, filter dimming, clustering, undo/redo and keyboard traversal must yield the same domain action in canvas/table/tree. Arrow traversal order must be stable and documented. Enter inspect/expand is context-specific and consistent with the shortcut registry; Space selects without scrolling the page. Escape exits the current mode without unexpectedly leaving the investigation.

### 13.3 Visual Truth and Export

Preserve typed direction, evidence, IDs and Unicode in GraphML/GEXF/JSON/CSV; use format-specific parser/round-trip checks. Verify PNG 2x/4x dimensions and nonblank content. Verify SVG/PDF safe embedded assets, large graph server rendering, legend/filter/time metadata and classification masking. Export only what the user is authorized to export, not a hidden full graph buffer.

Canvas tests inspect real rendered pixels plus graph instance node/edge counts, camera bounds, selection changes and screenshot content. A nonzero pixel alone is insufficient; a background rectangle could pass that check. Capture representative frames before/after actual interactions and verify reference assets are visible. In headless environments record GPU/WebGL/software-renderer details; do not claim laptop performance from a software-rendered CI run.

## 14. Accessibility and Localization Gates

Target full applicable WCAG 2.2 AA conformance, not just an axe score. Use native semantics first and the relevant APG keyboard/focus patterns for composite widgets. Include accessible authentication, non-drag alternatives, visible/unobscured focus, reflow and status announcements. Automated tools cannot certify all criteria. [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/).

| Gate | Concrete proof |
|---|---|
| Contrast | Source text ratios >=4.5:1, large text/icons and meaningful UI/focus >=3:1 in tested combinations; branded overrides included. |
| Keyboard | Every primary journey without pointer; no trap; predictable tab/arrow order; focus returned after overlays and errors. |
| Targets | Minimum 24x24 CSS px target with reviewed applicable exceptions; prefer 44 px; dense mode still operable. |
| Zoom/reflow | 400% zoom and narrow viewport without lost controls/text; intrinsically 2D graph/table areas have usable alternatives and scoped scrolling. |
| Assistive tech | Recorded NVDA/Chrome, JAWS/Edge, VoiceOver/Safari versions, tasks, utterances/observations and reviewer approval. |
| Virtualization | Correct logical counts/positions, stable focus, reachable offscreen items and accessible loading announcements. |
| Motion | Reduced-motion and user preference honored in CSS, JS, canvas and worker-driven layout; no autoplay-dependent task. |
| Color/graphics | Shape/text/line-pattern meaning, color-vision simulation, forced-colors selection/focus, table/tree parity. |
| Errors/forms | Visible labels, described field errors, error summary links, preserved valid input and consistent recovery. |
| Media | Caption/transcript alternatives for any instructional or recorded media actually delivered. |
| Localization | No concatenated grammar, ICU plural/select support, numbers/units/currency/dates/time zones formatted correctly. |
| RTL/font/layout | Directional layout mirrors; graph/timeline/code do not reverse meaning; Noto fallback, 30% expansion and long labels fit. |

Externalize all strings, including validation, tooltips, empty/error states and server-code mappings. Tenant ontology labels follow the source's tenant locale -> user locale -> canonical fallback unless D-14 approves a change. Do not leak raw server exceptions to avoid translating them. Manual reviewers must not approve only the light populated happy path.

## 15. Performance and Operational Budgets

The values below preserve source requirements. D-09 must make hardware, workload and measurement window precise before acceptance. The proposed reporting method is median and p95 across repeated scripted interactions, plus raw worst-case traces; do not change an explicitly required source target by averaging away stalls.

| Surface | Required budget / instruction |
|---|---|
| Web responsiveness | LCP <2.0 s, INP <200 ms, CLS <0.1 on declared reference profile; distinguish synthetic lab approximation from field INP. |
| Bundles | Shell <=250 kB gzip; each initial route <=150 kB gzip excluding explicitly lazy engines. Count shared/eager chunks once by a documented loading model. |
| Graph first render | 1k nodes visible <1 s after data arrival; separately report network and layout time. |
| Graph interaction | Target 60 fps at 10k nodes; >=30 fps at 100k WebGL on qualified hardware and declared edge counts. |
| Main thread | Worker layout/parsing/algorithms when work exceeds 16 ms; measure actual blocking tasks. |
| Tables/trees | Virtualize >100 rows / >300 nodes; server pagination remains bounded. |
| Graph heap | <=800 MB active graph heap; warning at 70% (560 MB). Define measurement method and limits where browser memory APIs are unavailable. |
| Animation | <=200 animated elements, graph animations off above 10k, edges draw only below 2k, no continuous decorative work. |
| Resource lifecycle | No unbounded worker/socket/event/GPU/cache growth on repeated navigate/scope-switch cycles; establish a bounded post-GC plateau. |
| Offline/local | No unintended external font/asset/analytics/model calls; explicit supported failures for unavailable local services. |

Benchmark datasets must include chains, hubs, communities, disconnected components, dense multigraphs and long labels at 1k/10k/100k, with recorded edge counts/distribution and source seed/hash. A sparse 100k-node graph cannot qualify all dense 100k workloads. Include filtered and unfiltered, normal and selected, active event stream and export scenarios. Large graph rejection/refinement is valid behavior but does not prove the rejected scale target.

The historical source bundle size is not a current measurement. Measure the new release build; retain compressed chunk manifest and route network traces. Do not simply raise Vite's warning limit to meet a budget.

## 16. Test Strategy and Anti-False-Completion Controls

### 16.1 Test Layers

| Layer | What it proves | What it cannot prove alone |
|---|---|---|
| Static/type/lint | Types, boundaries, generated-client consistency and unsafe patterns | Runtime service behavior or usable UI |
| Unit/reducer | Parsing, validation, cache keys, state transitions, cancellation/retry logic | Database persistence or browser accessibility |
| Component/story | Interactive states, focus, validation and layout with controlled fixtures | Real authentication, transport or durable integration |
| Contract | Schema/status/error compatibility for every exposed client operation | Whole user journey or visual quality |
| Real API/storage | Authorization, tenancy, transactions, migration, restart and concurrent instances | Actual rendered screen behavior |
| Real browser journey | User action -> actual service -> persistence -> UI reconciliation | Every screen-reader behavior or production-scale performance |
| Visual/render | Geometry, themes, assets, nonblank canvas and approved presentation | Correct backend outcomes or meaningful accessible semantics |
| A11y/manual | Keyboard/AT task completion and applicable criteria | Model quality, security or persistence |
| Performance/security | Declared workload budgets and adversarial boundary outcomes | Untested hardware/profile or every threat |
| Packaging/upgrade | Delivered assets/contracts/notices, migration and rollback | External legal clearance or unexecuted customer profile |

Security/state reducer branch coverage target is >=90%; feature logic >=80%, as requested by the source. Coverage is a diagnostic floor, not proof that assertions check the right outcome. Add negative controls and targeted mutation checks for tenant filtering, stale-response rejection, unsafe retry and evidence verification.

### 16.2 Required Real Journeys

Assign stable `GUI-JRN-*` IDs and link every step to screen/contract/acceptance clauses:

1. JRN-01: login -> choose authorized tenant/workspace -> refresh deep link -> switch scope -> logout/revocation.
2. JRN-02: source configure/test -> ingest -> review -> dry-run -> publish -> first evidence-backed question.
3. JRN-03: graph search/expand/filter -> entity/provenance -> save view -> restart -> restore -> authorized export.
4. JRN-04: question -> query/cost preview -> real streamed answer -> citation/source -> cancel/regenerate -> report.
5. JRN-05: proposed change -> bounded impact -> evidence/test checklist -> saved plan -> export/approval.
6. JRN-06: incident -> hypotheses -> evidence traversal -> collaborative finding -> durable decision.
7. JRN-07: ontology draft -> invalid/valid validation -> review -> publish -> graph/schema check -> rollback.
8. JRN-08: interrupted resumable upload -> review/mapping conflict -> job resume/retry -> verified graph result.
9. JRN-09: entity duplicate -> preview -> merge -> affected relations/provenance -> split/undo.
10. JRN-10: query validate/explain/run/profile -> cancel/timeout -> saved template -> paged/exported result.
11. JRN-11: agent run -> scoped approval -> tool side effect -> denial/replay/kill switch -> audited terminal result.
12. JRN-12: report template/parameters -> render -> approve -> real scheduled execution -> secure download/revoke.
13. JRN-13: two-browser collaboration -> presence/comments -> disconnect/rejoin -> membership revocation.
14. JRN-14: governance policy -> denied egress -> approved redacted call -> revocation across active clients.
15. JRN-15: tenant lifecycle/quota -> suspend/resume -> backup -> isolated restore -> denied cross-tenant admin.
16. JRN-16: brand draft -> failed contrast -> corrected preview -> atomic publish -> all themes -> rollback.
17. JRN-17: settings/locale/motion -> second device -> notification/read state -> help/about/offline notices.
18. JRN-18: failure/offline/version mismatch -> safe recovery -> retained authorized draft/context.

For each applicable journey, run happy path, invalid input, unauthorized principal, tenant/workspace substitution, revoked permission mid-flow, empty/partial result, network fault, server restart and cancellation/concurrent edit. Use one real shared backend for isolation tests, not separate tenant-specific fake objects.

### 16.3 Evidence Receipt Schema

This illustrative structure is a proposed artifact, NOT a recorded passing run:

```json
{
  "schema_version": "gui-evidence-v1",
  "run_id": "TO_BE_ASSIGNED_BY_RUNNER",
  "status": "NOT_RUN",
  "source": {
    "commit": "REQUIRED",
    "dirty_manifest_sha256": "REQUIRED_IF_DIRTY",
    "requirements_sha256": "REQUIRED",
    "frontend_build_sha256": "REQUIRED",
    "lockfiles_sha256": {},
    "backend_revision_or_image_digest": "REQUIRED",
    "openapi_sha256": "REQUIRED",
    "event_contract_sha256": "REQUIRED"
  },
  "environment": {
    "deployment_profile": "REQUIRED",
    "real_backend": true,
    "storage_adapter": "REQUIRED",
    "database_fixture_sha256": "REQUIRED",
    "model_runtime": "REQUIRED_OR_REVIEWED_NOT_APPLICABLE",
    "os_browser_gpu_hardware": "REQUIRED",
    "viewport_theme_density_locale_motion": "REQUIRED"
  },
  "execution": {
    "command": "REQUIRED",
    "started_at": null,
    "finished_at": null,
    "exit_code": null,
    "expected_test_ids": [],
    "executed_test_ids": [],
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "xfail": 0,
    "retried": 0
  },
  "clauses": [],
  "artifacts": [],
  "manual_reviews": [],
  "unresolved_gates": []
}
```

The verifier rejects literal placeholders, empty required lists, `NOT_RUN`, missing environment identity, mock fulfilment in real projects, stale source/build hashes and incomplete manual gates. Each artifact entry supplies path, MIME, bytes and SHA-256; each clause entry identifies expected outcome, test IDs, actual result and supporting artifacts. Redact sensitive data before retention without deleting the information needed to verify the outcome.

### 16.4 Commands and Execution Instructions

Current commands that exist in the inspected repository:

```powershell
git status --short
git rev-parse HEAD
Get-FileHash GUI-UIX-requirements.md -Algorithm SHA256
npm --prefix apps/web ci
npm --prefix apps/web run build
```

After GUI-02 implements the proposed scripts, run the following from repository root. Until then, a missing script is incomplete tooling, not a skipped gate:

```powershell
npm --prefix apps/web run typecheck
npm --prefix apps/web run lint
npm --prefix apps/web run test:unit
npm --prefix apps/web run test:component
npm --prefix apps/web run test:contract
npm --prefix apps/web run test:e2e:real
npm --prefix apps/web run test:visual
npm --prefix apps/web run test:a11y
npm --prefix apps/web run test:perf
npm --prefix apps/web run check:bundle
npm --prefix apps/web run check:gui-evidence
```

GUI-01/15 must also provide a reproducible fixture launcher with temporary scoped data, real API/storage, optional qualified local model, health wait, seed manifest and teardown. Browser tests target the actual built artifact and configured API origin, not a development proxy accidentally connected to a different revision. Allocate unused ports; retain logs; redact credentials. Do not run customer-mutating fixtures in a user's existing deployment.

### 16.5 CI Sequence

1. Inventory/hash/decision/schema drift gate; fail on lost clauses, unknown IDs or unreviewed contracts.
2. Reproducible install, dependency/license inventory, type/lint/import-boundaries and generated-client consistency.
3. Unit/component/stories/runtime schemas and verifier negative controls.
4. Real API/storage security, transaction, migration, restart and event tests.
5. Production web build, no-mock/no-dev-bypass scan, chunk and asset manifest.
6. Real-browser journeys across approved engines; retain traces, console/network failures and screenshots.
7. Visual/accessibility/localization/reduced-motion matrix, with reviewed baselines and manual gate records.
8. Qualified performance and operational failure/recovery scenarios.
9. Package/upgrade/offline/notices verification and final receipt binding.
10. Independent review of mandatory clause coverage; publish only the exact artifact that passed.

Routine PR pipelines may run impacted subsets, but the release candidate must run the complete required matrix. Record selection logic; never present a subset as a complete run. Avoid treating retried flaky tests as clean acceptance. Diagnose and rerun with a new honest receipt after fixing the cause.

## 17. Milestones and Dependency Order

| Milestone | Ordered scope | Entry dependencies | Exit evidence |
|---|---|---|---|
| M0A Baseline | GUI-00/01, decisions and full inventory | Source available | Clause ledger, current contract capture, owner-assigned blockers |
| M0B Foundations | GUI-02..06, SCR-001/027, shared a11y/security | Identity/workspace contracts agreed | Real scoped session, keyboard shell, four themes, generated client, no production mocks |
| M1 Graph core | GUI-07; SCR-003/005/006/013 | Scoped graph/aggregate/view services | Real saved view/entity evidence, table/tree parity, 10k performance receipt |
| M2 Intelligence | GUI-08; SCR-004/007..011 | Real query/model/evidence/temporal services | True stream/cancel, saved investigation/plan, correct evidence and temporal comparisons |
| M3 Data foundation | GUI-09; SCR-002/012/014..017 | Source/upload/review/publish/job contracts | Resumable ingest/review/publish, real first question, restart and rollback |
| M4 Work/content | GUI-10; SCR-018..020 | Tool approvals, reports/scheduler, collaboration backend | Exactly-once approved effects, valid documents/schedules, two-client durable collaboration |
| M5 Enterprise | GUI-11; SCR-021..026 | Policy/tenant/brand/preferences/notice contracts | Real policy denial, tenant ops, atomic brand, local notices and preferences |
| M6 Qualification | GUI-12..16 across all mandatory work | Feature integration complete | Complete visual/AT/security/performance/profile/upgrade receipts and approvals |
| M7 Optional | GUI-17 only where approved | Accepted required 2D/browser product | Separate optional capability qualification |

Accessibility, security, test automation and performance instrumentation start in M0, not after the screens are finished. M3 onboarding may begin as a shell in M0, but cannot be accepted before its data journey works. Do not create a circular gate by requiring M2's full feature set merely to test a minimal evidence-backed first question; define the minimal real query dependency explicitly in GUI-01.

Suggested first implementation slice: GUI-00 inventory -> identity/workspace decisions and contracts -> GUI-02/03 -> SCR-001/027 shell -> central transport -> Graph/Entity saved-view workflow -> one real persisted export. Obtain evidence and review before multiplying the pattern across all screens.

## 18. Release Acceptance, Rollback and Handoff

### 18.1 Named Gates

| Gate | Reject release when |
|---|---|
| G0 Scope | Mandatory source clause unregistered, unassigned, ambiguously interpreted or silently removed |
| G1 Contracts | Missing/incorrect API/event schemas, unreviewed capability or unresolved required backend |
| G2 Identity/isolation | Bootstrap-only production login, cross-scope data/cache/event/download exposure, absent server authorization |
| G3 Behavior | Required action/state/journey fails, is unreachable, mocked, simulated as real, skipped or stale |
| G4 Durability | Claimed saved resources/jobs/preferences disappear or conflict incorrectly after restart/concurrent access |
| G5 Visual/usability | Clipped/overlapping controls, blank graph, inaccessible workflow, unreviewed visual regression or critical user-task failure |
| G6 Accessibility/localization | Applicable AA/manual AT failure, serious/critical axe issue, untranslated required copy or broken RTL/reflow |
| G7 Performance | Declared budget or qualified scale fails, or hardware/dataset evidence is absent |
| G8 Security/privacy/legal delivery | Unsafe browser behavior, secret/PII leakage, unauthorized egress, missing required shipped notices or unresolved release approval |
| G9 Operational/evidence | Mismatched artifacts/receipts, untested mandatory profile, failed migration/rollback, missing reviewer approval |

### 18.2 Cutover Procedure

1. Freeze mandatory scope and exact contract/build/dependency/model/data versions for a release candidate. Changes after qualification invalidate affected receipts.
2. Back up required browser/server data under the approved retention/access policy. Rehearse migrations against copies, including ambiguous legacy ownership handling.
3. Deploy a limited approved cohort/profile and inspect real error, job, latency, permission-denial and event-gap signals. Do not enable external telemetry without consent.
4. Verify real tasks and approved manual reviews; publish the immutable artifact and its evidence manifest.
5. On rollback, stop incompatible writes, restore the compatible previous artifact/configuration and execute the tested data recovery procedure. Do not run destructive schema downgrade blindly.
6. Keep old workflow redirects and compatibility windows until their removal criteria are met. Archive prior status/receipts instead of overwriting history.

### 18.3 Agent Handoff Template

```text
Package and clause IDs:
Source hash and repository/build revisions:
Approved decisions used; unresolved decisions:
Existing files inspected; new/modified files:
Actual behavior delivered (not just files added):
Real backend/storage/model/profile exercised:
Commands, timestamps and exact test counts:
Evidence manifest path and artifact hashes:
Mocked/component-only checks, clearly separated:
Negative authorization/failure/restart/conflict results:
Visual review and manual AT/usability status:
Remaining blockers, defects and external approvals:
Migration/rollback instructions:
Next bounded task and prerequisites:
```

Never conclude "100% complete" from this document's existence, code references, test references, a green build or a subset of tests. State exactly which clauses and gates passed and which remain open. Keep an approved-not-applicable record separate from implemented work. Update the GUI plan and integration catalogue through versioned follow-ups; do not rewrite historical CP receipts to pretend they prove the new GUI.

## Appendix A. Complete Source-Section Coverage

This index accounts for all source lines by section, including non-screen requirements. Line 1 is the document title; line 2 is spacing. Section ranges are source locators, not evidence of implementation. GUI-00 must split each normative paragraph/table cell into acceptance clauses without losing qualifications or exceptions.

| Source section | Source lines | Execution owners/packages |
|---|---|---|
| 1. Document Control | 3-9 | GUI-00, GUI-15 |
| 2. Product And Design Vision | 10-21 | GUI-00, GUI-03, GUI-04, GUI-12 |
| 3. Technology Stack | 22-70 | GUI-02, GUI-07, GUI-17 |
| 4. Information Architecture | 71-84 | GUI-04 |
| 5. Design System | 85-94 | GUI-03, GUI-11 |
| 6. Motion And Animation | 95-100 | GUI-03, GUI-07, GUI-12 |
| 7. Layout, Responsiveness And Fit | 101-106 | GUI-04, GUI-07, GUI-12 |
| 8. Component Library Specification | 107-123 | GUI-05 |
| 9. Screen-By-Screen Specification | 124-477 | GUI-04..11; SCR-001..027 |
| 10. Graph Visualisation Specification | 478-485 | GUI-07, GUI-14 |
| 11. Forms, Validation And Data Entry | 486-489 | GUI-05, GUI-09, GUI-13 |
| 12. AI And LLM UX Patterns | 490-493 | GUI-08, GUI-10 |
| 13. States, Feedback And Resilience | 494-497 | GUI-05, GUI-06, GUI-13 |
| 14. Accessibility | 498-501 | GUI-12 |
| 15. Internationalisation And Localisation | 502-505 | GUI-12 |
| 16. Security, Privacy And Multi-Tenancy In The UI | 506-509 | GUI-04, GUI-06, GUI-13 |
| 17. Backend Integration Map | 510-1314 | GUI-00, GUI-01, GUI-06 |
| 18. Performance Budgets | 1315-1318 | GUI-14 |
| 19. Observability And Product Analytics | 1319-1322 | GUI-06, GUI-13, GUI-15 |
| 20. Front-End Project Structure And Standards | 1323-1334 | GUI-02, GUI-05 |
| 21. Delivery Plan | 1335-1346 | GUI-00..17 |
| 22. Global Definition Of Done | 1347-1350 | GUI-15, GUI-16 |
| 23. Appendices | 1351-1395 | GUI-00, GUI-01, GUI-03, GUI-04, GUI-06 |

## Appendix B. Complete Screen and Historical Integration Index

The links below are the source assignments, preserved for reconciliation, not approved frontend request lists. Section 2.3 lists known corrections. A screen package must add its actual accepted operations and remove inappropriate calls through a reviewed mapping change. INT-735 is additionally linked to SCR-017/024 in the source catalogue but missing from its source matrix; resolve this discrepancy in GUI-01.

| Screen | Source specification line | Required route | Source integration IDs |
|---|---|---|---|
| SCR-001 - Authentication and tenant entry | 126 | `/auth/*` | `INT-049`, `INT-050`, `INT-051`, `INT-052`, `INT-053`, `INT-054`, `INT-055`, `INT-056`, `BACKEND-MISSING-001`, `BACKEND-MISSING-002` |
| SCR-002 - First-run onboarding | 139 | `/t/:tenant/onboarding` | `INT-009`, `INT-010`, `INT-011`, `INT-012`, `INT-013`, `INT-014`, `INT-015`, `INT-016`, `BACKEND-MISSING-003` |
| SCR-003 - Brain overview | 152 | `/t/:tenant/w/:workspace` | `INT-020`, `INT-021`, `INT-022`, `INT-023`, `INT-049`, `INT-161`, `INT-162`, `INT-163` |
| SCR-004 - Ask the Brain | 165 | `/t/:tenant/w/:workspace/ask` | `INT-039`, `INT-061`, `INT-062`, `INT-063`, `INT-064`, `INT-065`, `INT-066`, `INT-067`, `BACKEND-MISSING-005` |
| SCR-005 - Graph Explorer | 178 | `/t/:tenant/w/:workspace/graph` | `INT-178`, `INT-216`, `INT-232`, `INT-252`, `INT-253`, `INT-254`, `INT-255`, `INT-256`, `BACKEND-MISSING-004` |
| SCR-006 - Entity 360 | 191 | `/t/:tenant/w/:workspace/entity/:id` | `INT-005`, `INT-100`, `INT-102`, `INT-180`, `INT-226`, `INT-289`, `INT-290`, `INT-291`, `BACKEND-MISSING-006` |
| SCR-007 - Impact Analysis studio | 204 | `/t/:tenant/w/:workspace/impact` | `INT-044`, `INT-105`, `INT-252`, `INT-262`, `INT-277`, `INT-278`, `INT-280`, `INT-292`, `BACKEND-MISSING-007` |
| SCR-008 - Change history | 217 | `/t/:tenant/w/:workspace/changes` | `INT-107`, `INT-114`, `INT-115`, `INT-116`, `INT-129`, `INT-178`, `INT-179`, `INT-180` |
| SCR-009 - Incident root-cause workspace | 230 | `/t/:tenant/w/:workspace/incidents/:id` | `INT-104`, `INT-175`, `INT-242`, `INT-439`, `INT-440`, `INT-441`, `INT-442`, `INT-443`, `BACKEND-MISSING-008` |
| SCR-010 - Temporal and time travel | 243 | `/t/:tenant/w/:workspace/time` | `INT-029`, `INT-083`, `INT-180`, `INT-196`, `INT-215`, `INT-216`, `INT-217`, `INT-218` |
| SCR-011 - Query Workbench | 256 | `/t/:tenant/w/:workspace/query` | `INT-008`, `INT-039`, `INT-062`, `INT-067`, `INT-081`, `INT-167`, `INT-230`, `INT-326`, `BACKEND-MISSING-009` |
| SCR-012 - Ontology Designer | 269 | `/t/:tenant/w/:workspace/ontology` | `INT-024`, `INT-066`, `INT-204`, `INT-279`, `INT-345`, `INT-346`, `INT-347`, `INT-348`, `BACKEND-MISSING-010` |
| SCR-013 - Meta-graph | 282 | `/t/:tenant/w/:workspace/meta-graph` | `INT-066`, `INT-345`, `INT-346`, `INT-347`, `INT-348`, `INT-349`, `INT-350`, `INT-351` |
| SCR-014 - Sources and connectors | 295 | `/t/:tenant/w/:workspace/sources` | `INT-142`, `INT-143`, `INT-231`, `INT-444`, `INT-446`, `INT-447`, `INT-448`, `INT-620` |
| SCR-015 - Ingestion and Mapping studio | 308 | `/t/:tenant/w/:workspace/ingestion` | `INT-009`, `INT-010`, `INT-011`, `INT-012`, `INT-013`, `INT-014`, `INT-015`, `INT-016`, `BACKEND-MISSING-011`, `BACKEND-MISSING-012` |
| SCR-016 - Entity resolution and quality | 321 | `/t/:tenant/w/:workspace/quality` | `INT-388`, `INT-414`, `BACKEND-MISSING-013` |
| SCR-017 - Pipelines and Jobs | 334 | `/t/:tenant/w/:workspace/jobs` | `INT-020`, `INT-021`, `INT-022`, `INT-023`, `INT-025`, `INT-026`, `INT-374`, `INT-433` |
| SCR-018 - Agents | 347 | `/t/:tenant/w/:workspace/agents` | `INT-032`, `INT-033`, `INT-034`, `INT-035`, `INT-036`, `INT-037`, `INT-038`, `INT-039`, `BACKEND-MISSING-014` |
| SCR-019 - Reports and dashboards | 360 | `/t/:tenant/w/:workspace/reports` | `INT-057`, `INT-060`, `INT-081`, `INT-099`, `INT-132`, `INT-159`, `INT-163`, `INT-194`, `BACKEND-MISSING-015` |
| SCR-020 - Collaboration | 373 | `/t/:tenant/w/:workspace/collaboration` | `BACKEND-MISSING-016` |
| SCR-021 - Governance and security | 386 | `/t/:tenant/admin/governance` | `INT-001`, `INT-051`, `INT-052`, `INT-053`, `INT-054`, `INT-055`, `INT-056`, `INT-057`, `BACKEND-MISSING-017` |
| SCR-022 - Tenant administration | 399 | `/platform/tenants/:tenant` | `INT-188`, `INT-678`, `INT-679`, `INT-680`, `INT-681` |
| SCR-023 - White-label studio | 412 | `/t/:tenant/admin/brand` | `INT-085`, `INT-086`, `INT-087`, `INT-088`, `INT-089`, `BACKEND-MISSING-018` |
| SCR-024 - Platform health | 425 | `/platform/health` | `INT-049`, `INT-161`, `INT-162`, `INT-163`, `INT-164`, `INT-165`, `INT-166`, `INT-190` |
| SCR-025 - User settings | 438 | `/settings` | `INT-058`, `INT-059`, `INT-060`, `INT-078`, `INT-236`, `INT-293`, `INT-294`, `INT-295`, `BACKEND-MISSING-019` |
| SCR-026 - Notifications, help and licences | 451 | `/notifications` | `INT-312`, `INT-313`, `INT-314`, `INT-315`, `INT-316`, `INT-317`, `INT-468`, `INT-469`, `BACKEND-MISSING-020` |
| SCR-027 - Global errors | 464 | `/errors/:code` | `INT-049`, `INT-190`, `INT-191`, `INT-192`, `INT-193`, `INT-194`, `INT-195`, `INT-196` |

## Appendix C. All 735 Historical Integration Records

No operation is accepted by this table. Every row is initially **OPEN CONTRACT REVIEW**. `ASSIGN` means the source has no primary screen; GUI-00/01 and the owning backend domain must decide its UI/internal/alias/optional/obsolete disposition. `REVIEW` means a historical screen assignment exists but still needs semantic and security validation. Do not turn internal service operations into GUI controls just to eliminate ASSIGN rows.

Source request/response labels are preserved verbatim and may be incomplete or wrong. Source code locators and generic error/paging/event descriptions remain in the original full catalogue; consult the complete source row during contract definition. This compact execution index deliberately does not mistake those locators for evidence.

Every **exposed** operation requires contract and real positive/negative integration tests, scope enforcement, cancellation/timeouts where applicable, and screen reconciliation. Read operations additionally prove empty/partial/pagination/masking semantics. Mutations additionally prove durable effects, idempotency/conflicts, authorization and audit; job/stream/download operations also need their specialized lifecycle/integrity evidence. Internal-only/alias decisions require owner approval and documented rationale, not an untested blanket exclusion.

| ID | Source line | Method and path | Historical request / parameters | Historical response | Historical status | Historical screens | Required disposition task |
|---|---|---|---|---|---|---|---|
| `INT-001` | 520 | `GET /api/v1/admin/audit` | `none`; params: limit | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-021 | GUI-01: REVIEW |
| `INT-002` | 521 | `POST /api/v1/admin/demo` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-003` | 522 | `GET /api/v1/admin/dlq` | `none`; params: limit | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-004` | 523 | `POST /api/v1/admin/dlq/{event_id}/replay` | `none`; params: event_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-005` | 524 | `POST /api/v1/admin/entities/{canonical_id}/delete` | `none`; params: canonical_id | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-006 | GUI-01: REVIEW |
| `INT-006` | 525 | `GET /api/v1/admin/event-consumers` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-007` | 526 | `POST /api/v1/admin/event-consumers/run` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-008` | 527 | `POST /api/v1/admin/gremlin` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-011 | GUI-01: REVIEW |
| `INT-009` | 528 | `POST /api/v1/admin/ingestion/confluence` | `IncrementalSyncRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-002, SCR-015 | GUI-01: REVIEW |
| `INT-010` | 529 | `POST /api/v1/admin/ingestion/files` | `none`; params: filename, source_id, ocr, dry_run | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-002, SCR-015 | GUI-01: REVIEW |
| `INT-011` | 530 | `GET /api/v1/admin/ingestion/files/bundles/{bundle_id}/{artifact}` | `none`; params: bundle_id, artifact | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-002, SCR-015 | GUI-01: REVIEW |
| `INT-012` | 531 | `POST /api/v1/admin/ingestion/files/parse` | `none`; params: filename, source_id, ocr | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-002, SCR-015 | GUI-01: REVIEW |
| `INT-013` | 532 | `POST /api/v1/admin/ingestion/gitlab` | `GitLabIngestionRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-002, SCR-015 | GUI-01: REVIEW |
| `INT-014` | 533 | `POST /api/v1/admin/ingestion/jira` | `IngestionRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-002, SCR-015 | GUI-01: REVIEW |
| `INT-015` | 534 | `POST /api/v1/admin/ingestion/json` | `JsonIngestionRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-002, SCR-015 | GUI-01: REVIEW |
| `INT-016` | 535 | `POST /api/v1/admin/ingestion/json/batch` | `BatchIngestionRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-002, SCR-015 | GUI-01: REVIEW |
| `INT-017` | 536 | `POST /api/v1/admin/ingestion/process-and-convert` | `JsonIngestionRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-018` | 537 | `POST /api/v1/admin/ingestion/replay` | `ReplayRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-019` | 538 | `POST /api/v1/admin/ingestion/servicenow` | `IncrementalSyncRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-020` | 539 | `GET /api/v1/admin/jobs` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-003, SCR-017 | GUI-01: REVIEW |
| `INT-021` | 540 | `GET /api/v1/admin/jobs/{job_id}` | `none`; params: job_id | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-003, SCR-017 | GUI-01: REVIEW |
| `INT-022` | 541 | `POST /api/v1/admin/jobs/{job_id}/cancel` | `none`; params: job_id | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-003, SCR-017 | GUI-01: REVIEW |
| `INT-023` | 542 | `POST /api/v1/admin/jobs/{job_id}/readmit` | `none`; params: job_id | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-003, SCR-017 | GUI-01: REVIEW |
| `INT-024` | 543 | `GET /api/v1/admin/schema` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-012 | GUI-01: REVIEW |
| `INT-025` | 544 | `POST /api/v1/admin/semantic-pipeline` | `SemanticPipelineRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-017 | GUI-01: REVIEW |
| `INT-026` | 545 | `GET /api/v1/admin/semantic-pipeline/stages` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-017 | GUI-01: REVIEW |
| `INT-027` | 546 | `GET /api/v1/admin/stats` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-028` | 547 | `GET /api/v1/admin/system` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-029` | 548 | `GET /api/v1/admin/timeline` | `none`; params: limit | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-010 | GUI-01: REVIEW |
| `INT-030` | 549 | `POST /api/v1/admin/validation` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-031` | 550 | `GET /api/v1/admin/worker` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-032` | 551 | `GET /api/v1/agents` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-018 | GUI-01: REVIEW |
| `INT-033` | 552 | `POST /api/v1/agents/analytics` | `AgentAnalyticsRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-018 | GUI-01: REVIEW |
| `INT-034` | 553 | `POST /api/v1/agents/mesh/recover/{recovery_id}` | `none`; params: recovery_id | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-018 | GUI-01: REVIEW |
| `INT-035` | 554 | `GET /api/v1/agents/mesh/recoveries` | `none`; params: status | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-018 | GUI-01: REVIEW |
| `INT-036` | 555 | `GET /api/v1/agents/proposals` | `none`; params: status | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-018 | GUI-01: REVIEW |
| `INT-037` | 556 | `POST /api/v1/agents/proposals/{proposal_id}/approve` | `ProposalDecisionRequest`; params: proposal_id | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-018 | GUI-01: REVIEW |
| `INT-038` | 557 | `POST /api/v1/agents/proposals/{proposal_id}/reject` | `ProposalDecisionRequest`; params: proposal_id | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-018 | GUI-01: REVIEW |
| `INT-039` | 558 | `POST /api/v1/agents/query` | `AgentQueryRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-004, SCR-011, SCR-018 | GUI-01: REVIEW |
| `INT-040` | 559 | `GET /api/v1/agents/runs/{run_id}` | `none`; params: run_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-041` | 560 | `GET /api/v1/agents/runs/{run_id}/explanation` | `none`; params: run_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-042` | 561 | `GET /api/v1/agents/runs/{run_id}/memory` | `none`; params: run_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-043` | 562 | `POST /api/v1/agents/semantic-index` | `AgentAnalyticsRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-044` | 563 | `POST /api/v1/agents/trace-impact` | `TraceRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-007 | GUI-01: REVIEW |
| `INT-045` | 564 | `GET /api/v1/agents/types` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-046` | 565 | `POST /api/v1/agents/{agent_id}/runs` | `AgentRunRequest`; params: agent_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-047` | 566 | `GET /api/v1/algorithms` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-048` | 567 | `POST /api/v1/algorithms/run` | `AlgorithmRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-049` | 568 | `GET /api/v1/auth/health` | `none`; params: none | `object` | `PARTIAL` | SCR-001, SCR-003, SCR-024, SCR-027 | GUI-01: REVIEW |
| `INT-050` | 569 | `POST /api/v1/auth/login` | `LoginRequest`; params: none | `object` | `PARTIAL` | SCR-001 | GUI-01: REVIEW |
| `INT-051` | 570 | `GET /api/v1/authz/decisions` | `none`; params: none | `object` | `PARTIAL` | SCR-001, SCR-021 | GUI-01: REVIEW |
| `INT-052` | 571 | `POST /api/v1/authz/evaluate` | `AuthzEvaluateRequest`; params: none | `object` | `PARTIAL` | SCR-001, SCR-021 | GUI-01: REVIEW |
| `INT-053` | 572 | `GET /api/v1/authz/policies` | `none`; params: none | `object` | `PARTIAL` | SCR-001, SCR-021 | GUI-01: REVIEW |
| `INT-054` | 573 | `POST /api/v1/authz/policies/reload` | `none`; params: none | `object` | `PARTIAL` | SCR-001, SCR-021 | GUI-01: REVIEW |
| `INT-055` | 574 | `GET /api/v1/authz/roles` | `none`; params: none | `object` | `PARTIAL` | SCR-001, SCR-021 | GUI-01: REVIEW |
| `INT-056` | 575 | `POST /api/v1/authz/roles` | `AuthzRoleRequest`; params: none | `object` | `PARTIAL` | SCR-001, SCR-021 | GUI-01: REVIEW |
| `INT-057` | 576 | `GET /api/v1/authz/roles/export` | `none`; params: none | `none` | `PARTIAL` | SCR-019, SCR-021 | GUI-01: REVIEW |
| `INT-058` | 577 | `GET /api/v1/authz/users` | `none`; params: none | `object` | `PARTIAL` | SCR-025 | GUI-01: REVIEW |
| `INT-059` | 578 | `POST /api/v1/authz/users` | `AuthzUserRequest`; params: none | `object` | `PARTIAL` | SCR-025 | GUI-01: REVIEW |
| `INT-060` | 579 | `GET /api/v1/authz/users/export` | `none`; params: none | `none` | `PARTIAL` | SCR-019, SCR-025 | GUI-01: REVIEW |
| `INT-061` | 580 | `GET /api/v1/brain/agents` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | SCR-004 | GUI-01: REVIEW |
| `INT-062` | 581 | `GET /api/v1/brain/approaches` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | SCR-004, SCR-011 | GUI-01: REVIEW |
| `INT-063` | 582 | `POST /api/v1/brain/ask` | `BrainAskRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-004 | GUI-01: REVIEW |
| `INT-064` | 583 | `GET /api/v1/brain/databases` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | SCR-004 | GUI-01: REVIEW |
| `INT-065` | 584 | `GET /api/v1/brain/dialects` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | SCR-004 | GUI-01: REVIEW |
| `INT-066` | 585 | `POST /api/v1/brain/induce` | `InduceRequest`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | SCR-004, SCR-012, SCR-013 | GUI-01: REVIEW |
| `INT-067` | 586 | `POST /api/v1/brain/intelligent-query` | `IntelligentQueryRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-004, SCR-011 | GUI-01: REVIEW |
| `INT-068` | 587 | `POST /api/v1/brain/learning/load` | `none`; params: directory | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-069` | 588 | `GET /api/v1/brain/learning/policy` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-070` | 589 | `POST /api/v1/brain/learning/save` | `none`; params: directory | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-071` | 590 | `GET /api/v1/brain/learning/status` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-072` | 591 | `POST /api/v1/brain/learning/train` | `LearningTrainRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-073` | 592 | `POST /api/v1/brain/llm/embed` | `LLMEmbedRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-074` | 593 | `POST /api/v1/brain/llm/explain` | `LLMGenerateRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-075` | 594 | `POST /api/v1/brain/llm/generate` | `LLMGenerateRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-076` | 595 | `GET /api/v1/brain/llm/models` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-077` | 596 | `POST /api/v1/brain/llm/stream` | `LLMGenerateRequest`; params: none | `array` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-078` | 597 | `POST /api/v1/brain/llm/tokenize` | `LLMTokenizeRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-025 | GUI-01: REVIEW |
| `INT-079` | 598 | `GET /api/v1/brain/loops` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-080` | 599 | `POST /api/v1/brain/narrate` | `CognitiveNarrateRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-081` | 600 | `POST /api/v1/brain/query` | `BrainQueryReportRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-011, SCR-019 | GUI-01: REVIEW |
| `INT-082` | 601 | `GET /api/v1/brain/rag-modes` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-083` | 602 | `GET /api/v1/brain/snapshot` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-010 | GUI-01: REVIEW |
| `INT-084` | 603 | `GET /api/v1/brain/telemetry` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-085` | 604 | `GET /api/v1/branding/legal` | `none`; params: tenant_id, kind | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-023 | GUI-01: REVIEW |
| `INT-086` | 605 | `GET /api/v1/branding/locales/{locale}/message` | `none`; params: locale, key, tenant_id, default | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-023 | GUI-01: REVIEW |
| `INT-087` | 606 | `POST /api/v1/branding/terminology/canonicalize` | `CanonicalizeRequest`; params: tenant_id | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-023 | GUI-01: REVIEW |
| `INT-088` | 607 | `POST /api/v1/branding/terminology/rename` | `RenameRequest`; params: tenant_id | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-023 | GUI-01: REVIEW |
| `INT-089` | 608 | `GET /api/v1/branding/theme` | `none`; params: tenant_id, mode | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-023 | GUI-01: REVIEW |
| `INT-090` | 609 | `GET /api/v1/capsules` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-091` | 610 | `POST /api/v1/capsules` | `CapsuleRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-092` | 611 | `GET /api/v1/capsules/{name}` | `none`; params: name | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-093` | 612 | `GET /api/v1/catalog/products` | `none`; params: owner, domain, state, access_policy, consumer | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-094` | 613 | `POST /api/v1/catalog/products` | `KnowledgeProduct`; params: none | `KnowledgeProduct` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-095` | 614 | `POST /api/v1/catalog/products/import` | `KnowledgeProduct`; params: none | `KnowledgeProduct` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-096` | 615 | `GET /api/v1/catalog/products/{product_id}` | `none`; params: product_id | `KnowledgeProduct` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-097` | 616 | `PUT /api/v1/catalog/products/{product_id}` | `KnowledgeProduct`; params: product_id | `KnowledgeProduct` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-098` | 617 | `DELETE /api/v1/catalog/products/{product_id}` | `none`; params: product_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-099` | 618 | `GET /api/v1/catalog/products/{product_id}/export` | `none`; params: product_id | `none` | `PARTIAL` | SCR-019 | GUI-01: REVIEW |
| `INT-100` | 619 | `GET /api/v1/catalog/products/{product_id}/lineage` | `none`; params: product_id | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-006 | GUI-01: REVIEW |
| `INT-101` | 620 | `POST /api/v1/catalog/products/{product_id}/transition` | `CatalogTransitionRequest`; params: product_id | `KnowledgeProduct` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-102` | 621 | `POST /api/v1/causal/correlations/{entity_cid}` | `inline`; params: entity_cid | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-006 | GUI-01: REVIEW |
| `INT-103` | 622 | `POST /api/v1/causal/counterfactual-intervention` | `CounterfactualInterventionRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-104` | 623 | `POST /api/v1/causal/hypotheses/{incident_cid}` | `inline`; params: incident_cid | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-009 | GUI-01: REVIEW |
| `INT-105` | 624 | `POST /api/v1/causal/live-blast-radius` | `LiveBlastRadiusRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-007 | GUI-01: REVIEW |
| `INT-106` | 625 | `POST /api/v1/causal/prerequisites` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-107` | 626 | `GET /api/v1/change-journal` | `none`; params: after, limit | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-008 | GUI-01: REVIEW |
| `INT-108` | 627 | `GET /api/v1/compliance/ai/evaluations` | `none`; params: model_card_id | `array<EvaluationRecord>` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-109` | 628 | `POST /api/v1/compliance/ai/evaluations` | `EvaluationRecord`; params: none | `EvaluationRecord` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-110` | 629 | `GET /api/v1/compliance/ai/model-cards` | `none`; params: none | `array<ModelCard>` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-111` | 630 | `POST /api/v1/compliance/ai/model-cards` | `ModelCard`; params: none | `ModelCard` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-112` | 631 | `GET /api/v1/compliance/ai/model-cards/{model_card_id}/label` | `none`; params: model_card_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-113` | 632 | `POST /api/v1/compliance/ai/oversight` | `HumanOversightConfig`; params: none | `HumanOversightConfig` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-114` | 633 | `GET /api/v1/compliance/changes` | `none`; params: state, kind | `array` | `IMPLEMENTED-UNVERIFIED` | SCR-008 | GUI-01: REVIEW |
| `INT-115` | 634 | `POST /api/v1/compliance/changes` | `none`; params: kind, title, description, requested_by, created_at | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-008 | GUI-01: REVIEW |
| `INT-116` | 635 | `POST /api/v1/compliance/changes/{proposal_id}/transition` | `none`; params: proposal_id, to_state, actor, at, reason | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-008 | GUI-01: REVIEW |
| `INT-117` | 636 | `GET /api/v1/compliance/exceptions` | `none`; params: active_only | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-118` | 637 | `POST /api/v1/compliance/exceptions` | `none`; params: policy_ref, subject, justification, approved_by, expires_at | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-119` | 638 | `POST /api/v1/compliance/exceptions/{exception_id}/revoke` | `none`; params: exception_id, actor | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-120` | 639 | `GET /api/v1/compliance/packs` | `none`; params: none | `array<CompliancePack>` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-121` | 640 | `GET /api/v1/compliance/packs/{framework}` | `none`; params: framework | `CompliancePack` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-122` | 641 | `POST /api/v1/compliance/packs/{framework}/gap-analysis` | `none`; params: framework | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-123` | 642 | `GET /api/v1/compliance/roles` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-124` | 643 | `GET /api/v1/compliance/roles/auditor-view` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-125` | 644 | `GET /api/v1/compliance/roles/{role}` | `none`; params: role | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-126` | 645 | `GET /api/v1/config/audit` | `none`; params: key | `array<ConfigChangeRecord>` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-127` | 646 | `POST /api/v1/config/bounds` | `object`; params: none | `ConfigChangeRecord` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-128` | 647 | `GET /api/v1/config/definitions` | `none`; params: none | `array<SettingDef>` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-129` | 648 | `POST /api/v1/config/diff` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-008 | GUI-01: REVIEW |
| `INT-130` | 649 | `GET /api/v1/config/effective` | `none`; params: key, tenant, business_unit, workspace, user_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-131` | 650 | `GET /api/v1/config/explain` | `none`; params: key, tenant, business_unit, workspace, user_id | `ExplainResult` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-132` | 651 | `POST /api/v1/config/export` | `object`; params: none | `ConfigArchive` | `PARTIAL` | SCR-019 | GUI-01: REVIEW |
| `INT-133` | 652 | `GET /api/v1/config/flags` | `none`; params: none | `array<FeatureFlag>` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-134` | 653 | `POST /api/v1/config/flags` | `object`; params: none | `FeatureFlag` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-135` | 654 | `POST /api/v1/config/import` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-136` | 655 | `POST /api/v1/config/reload-subscribe` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-137` | 656 | `POST /api/v1/config/rollback` | `object`; params: none | `ConfigChangeRecord` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-138` | 657 | `POST /api/v1/config/set` | `object`; params: none | `ConfigChangeRecord` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-139` | 658 | `POST /api/v1/conformance/check` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-140` | 659 | `GET /api/v1/conformance/rules` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-141` | 660 | `PUT /api/v1/conformance/rules/{name}` | `object`; params: name | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-142` | 661 | `GET /api/v1/connectors/catalog` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-014 | GUI-01: REVIEW |
| `INT-143` | 662 | `GET /api/v1/connectors/files/formats` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-014 | GUI-01: REVIEW |
| `INT-144` | 663 | `GET /api/v1/demo/scenarios` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-145` | 664 | `GET /api/v1/domain-packs` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-146` | 665 | `GET /api/v1/domain-packs/{pack_name}` | `none`; params: pack_name | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-147` | 666 | `POST /api/v1/domain-packs/{pack_name}/activate` | `ActivateDomainPackRequest`; params: pack_name | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-148` | 667 | `POST /api/v1/egress/call` | `CallRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-149` | 668 | `GET /api/v1/egress/endpoints` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-150` | 669 | `POST /api/v1/egress/endpoints/{endpoint_id}/disable` | `KillRequest`; params: endpoint_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-151` | 670 | `POST /api/v1/egress/endpoints/{endpoint_id}/enable` | `EnableEndpointRequest`; params: endpoint_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-152` | 671 | `POST /api/v1/egress/kill` | `KillRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-153` | 672 | `GET /api/v1/egress/manifests` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-154` | 673 | `GET /api/v1/egress/plugins` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-155` | 674 | `POST /api/v1/egress/plugins/install` | `InstallPluginRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-156` | 675 | `POST /api/v1/egress/plugins/submit` | `SubmitPluginRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-157` | 676 | `GET /api/v1/egress/policy/rules` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-158` | 677 | `POST /api/v1/egress/policy/rules` | `AddRuleRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-159` | 678 | `GET /api/v1/egress/report` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-019 | GUI-01: REVIEW |
| `INT-160` | 679 | `POST /api/v1/engineering/{discipline}` | `EngineeringRequest`; params: discipline | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-161` | 680 | `GET /api/v1/enterprise/analytics/anomalies/{metric}` | `none`; params: metric, threshold | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-003, SCR-024 | GUI-01: REVIEW |
| `INT-162` | 681 | `GET /api/v1/enterprise/analytics/forecast/{metric}` | `none`; params: metric, horizon, method | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-003, SCR-024 | GUI-01: REVIEW |
| `INT-163` | 682 | `GET /api/v1/enterprise/analytics/growth/{metric}` | `none`; params: metric, threshold | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-003, SCR-019, SCR-024 | GUI-01: REVIEW |
| `INT-164` | 683 | `GET /api/v1/enterprise/analytics/metrics` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-024 | GUI-01: REVIEW |
| `INT-165` | 684 | `POST /api/v1/enterprise/analytics/record` | `RecordMetricRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-024 | GUI-01: REVIEW |
| `INT-166` | 685 | `GET /api/v1/enterprise/analytics/trend/{metric}` | `none`; params: metric, window | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-024 | GUI-01: REVIEW |
| `INT-167` | 686 | `GET /api/v1/enterprise/audit/events` | `none`; params: category, actor, resource, limit | `array` | `IMPLEMENTED-UNVERIFIED` | SCR-011 | GUI-01: REVIEW |
| `INT-168` | 687 | `GET /api/v1/enterprise/audit/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-169` | 688 | `GET /api/v1/enterprise/audit/verify` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-170` | 689 | `POST /api/v1/enterprise/cache/clear` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-171` | 690 | `GET /api/v1/enterprise/cache/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-172` | 691 | `GET /api/v1/enterprise/chaos/experiments` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-173` | 692 | `POST /api/v1/enterprise/chaos/experiments` | `ChaosExperimentRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-174` | 693 | `POST /api/v1/enterprise/chaos/experiments/{experiment_id}/run` | `none`; params: experiment_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-175` | 694 | `POST /api/v1/enterprise/correlation/analyze/{event_id}` | `none`; params: event_id | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-009 | GUI-01: REVIEW |
| `INT-176` | 695 | `GET /api/v1/enterprise/correlation/events` | `none`; params: system_id, limit | `object` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-177` | 696 | `GET /api/v1/enterprise/correlation/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-178` | 697 | `GET /api/v1/enterprise/diff/changes` | `none`; params: limit | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-005, SCR-008 | GUI-01: REVIEW |
| `INT-179` | 698 | `GET /api/v1/enterprise/diff/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-008 | GUI-01: REVIEW |
| `INT-180` | 699 | `GET /api/v1/enterprise/diff/timeline/{entity_id}` | `none`; params: entity_id | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-006, SCR-008, SCR-010 | GUI-01: REVIEW |
| `INT-181` | 700 | `GET /api/v1/enterprise/dlq/entries` | `none`; params: source, limit | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-182` | 701 | `POST /api/v1/enterprise/dlq/replay` | `DLQReplayRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-183` | 702 | `GET /api/v1/enterprise/dlq/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-184` | 703 | `DELETE /api/v1/enterprise/dlq/{entry_id}` | `none`; params: entry_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-185` | 704 | `GET /api/v1/enterprise/feature-flags` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-186` | 705 | `POST /api/v1/enterprise/feature-flags` | `FeatureFlagRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-187` | 706 | `POST /api/v1/enterprise/feature-flags/evaluate` | `FlagEvalRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-188` | 707 | `POST /api/v1/enterprise/feature-flags/override` | `FlagOverrideRequest`; params: none | `object` | `PARTIAL` | SCR-022 | GUI-01: REVIEW |
| `INT-189` | 708 | `GET /api/v1/enterprise/feature-flags/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-190` | 709 | `GET /api/v1/enterprise/health/aggregate` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-024, SCR-027 | GUI-01: REVIEW |
| `INT-191` | 710 | `POST /api/v1/enterprise/health/check-all` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-027 | GUI-01: REVIEW |
| `INT-192` | 711 | `GET /api/v1/enterprise/health/live` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-027 | GUI-01: REVIEW |
| `INT-193` | 712 | `GET /api/v1/enterprise/health/ready` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-027 | GUI-01: REVIEW |
| `INT-194` | 713 | `GET /api/v1/enterprise/health/sla` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-019, SCR-027 | GUI-01: REVIEW |
| `INT-195` | 714 | `GET /api/v1/enterprise/health/startup` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-027 | GUI-01: REVIEW |
| `INT-196` | 715 | `GET /api/v1/enterprise/health/uptime` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-010, SCR-027 | GUI-01: REVIEW |
| `INT-197` | 716 | `POST /api/v1/enterprise/learning/feedback` | `FeedbackRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-198` | 717 | `POST /api/v1/enterprise/learning/prune` | `none`; params: threshold | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-199` | 718 | `GET /api/v1/enterprise/learning/rules` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-200` | 719 | `GET /api/v1/enterprise/learning/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-201` | 720 | `POST /api/v1/enterprise/lifecycle/drain` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-202` | 721 | `GET /api/v1/enterprise/lifecycle/status` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-203` | 722 | `GET /api/v1/enterprise/migrations` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-204` | 723 | `POST /api/v1/enterprise/migrations` | `MigrationRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-012 | GUI-01: REVIEW |
| `INT-205` | 724 | `POST /api/v1/enterprise/migrations/apply-all` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-206` | 725 | `POST /api/v1/enterprise/migrations/{migration_id}/apply` | `none`; params: migration_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-207` | 726 | `POST /api/v1/enterprise/migrations/{migration_id}/rollback` | `none`; params: migration_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-208` | 727 | `POST /api/v1/enterprise/nlconfig/execute` | `NLConfigRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-209` | 728 | `POST /api/v1/enterprise/nlconfig/suggest` | `NLConfigRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-210` | 729 | `GET /api/v1/enterprise/observability/metrics` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-211` | 730 | `GET /api/v1/enterprise/plugins` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-212` | 731 | `GET /api/v1/enterprise/plugins/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-213` | 732 | `GET /api/v1/enterprise/resilience/circuit-breakers` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-214` | 733 | `POST /api/v1/enterprise/resilience/circuit-breakers/reset` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-215` | 734 | `GET /api/v1/enterprise/snapshots` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-010 | GUI-01: REVIEW |
| `INT-216` | 735 | `POST /api/v1/enterprise/snapshots` | `SnapshotRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-005, SCR-010 | GUI-01: REVIEW |
| `INT-217` | 736 | `POST /api/v1/enterprise/snapshots/compare` | `none`; params: id_a, id_b | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-010 | GUI-01: REVIEW |
| `INT-218` | 737 | `POST /api/v1/enterprise/snapshots/restore` | `RestoreRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-010 | GUI-01: REVIEW |
| `INT-219` | 738 | `GET /api/v1/enterprise/snapshots/{snapshot_id}` | `none`; params: snapshot_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-220` | 739 | `DELETE /api/v1/enterprise/snapshots/{snapshot_id}` | `none`; params: snapshot_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-221` | 740 | `GET /api/v1/enterprise/webhooks` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-222` | 741 | `GET /api/v1/enterprise/webhooks/dead-letters` | `none`; params: limit | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-223` | 742 | `GET /api/v1/enterprise/webhooks/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-224` | 743 | `POST /api/v1/enterprise/webhooks/subscribe` | `WebhookSubscribeRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-225` | 744 | `DELETE /api/v1/enterprise/webhooks/{subscription_id}` | `none`; params: subscription_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-226` | 745 | `GET /api/v1/entities/{canonical_id}` | `none`; params: canonical_id, include_deleted | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-006 | GUI-01: REVIEW |
| `INT-227` | 746 | `POST /api/v1/evidence/manifest` | `EvidenceManifestRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-228` | 747 | `GET /api/v1/experts/{canonical_id}` | `none`; params: canonical_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-229` | 748 | `GET /api/v1/export/formats` | `none`; params: none | `none` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-230` | 749 | `POST /api/v1/federation/query` | `FederationQueryRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-011 | GUI-01: REVIEW |
| `INT-231` | 750 | `GET /api/v1/federation/sources` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-014 | GUI-01: REVIEW |
| `INT-232` | 751 | `GET /api/v1/files/{path}` | `none`; params: path | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-005 | GUI-01: REVIEW |
| `INT-233` | 752 | `GET /api/v1/gaps/completion-gate` | `none`; params: doc_set, max_priority, include_requirements | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-234` | 753 | `GET /api/v1/gaps/coverage` | `none`; params: status, priority, include_requirements, doc_set | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-235` | 754 | `GET /api/v1/gaps/g2/architecture-guardrails` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-236` | 755 | `POST /api/v1/gaps/g2/architecture-guardrails` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-025 | GUI-01: REVIEW |
| `INT-237` | 756 | `GET /api/v1/gaps/g2/observability-contract` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-238` | 757 | `POST /api/v1/gaps/g2/observability-contract` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-239` | 758 | `GET /api/v1/gaps/g2/readiness` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-240` | 759 | `GET /api/v1/gaps/requirements/{requirement_id}` | `none`; params: requirement_id, doc_set | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-241` | 760 | `POST /api/v1/governance/evaluate` | `ModelOutput`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-242` | 761 | `GET /api/v1/governance/incidents` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-009 | GUI-01: REVIEW |
| `INT-243` | 762 | `GET /api/v1/governance/kill-switch` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-244` | 763 | `POST /api/v1/governance/kill-switch` | `KillSwitchRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-245` | 764 | `POST /api/v1/governance/kill-switch/features/{feature}` | `KillSwitchFeatureRequest`; params: feature | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-246` | 765 | `GET /api/v1/governance/models` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-247` | 766 | `POST /api/v1/governance/models` | `ModelEntry`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-248` | 767 | `POST /api/v1/governance/models/{model_id}/approval` | `none`; params: model_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-249` | 768 | `DELETE /api/v1/governance/models/{model_id}/approval` | `none`; params: model_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-250` | 769 | `GET /api/v1/governance/templates` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-251` | 770 | `POST /api/v1/governance/templates` | `PromptTemplate`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-252` | 771 | `POST /api/v1/graph-tests/run` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-005, SCR-007 | GUI-01: REVIEW |
| `INT-253` | 772 | `POST /api/v1/graph/anomalies` | `AnomalyRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-005 | GUI-01: REVIEW |
| `INT-254` | 773 | `GET /api/v1/graph/as-of` | `none`; params: at, limit | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-005 | GUI-01: REVIEW |
| `INT-255` | 774 | `GET /api/v1/graph/backend` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-005 | GUI-01: REVIEW |
| `INT-256` | 775 | `GET /api/v1/graph/backends` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-005 | GUI-01: REVIEW |
| `INT-257` | 776 | `POST /api/v1/graph/bitemporal/diff` | `BitemporalDiffRequest`; params: none | `BitemporalDiff` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-258` | 777 | `POST /api/v1/graph/bitemporal/known-at` | `BitemporalCoordinate`; params: none | `BitemporalSlice` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-259` | 778 | `POST /api/v1/graph/bitemporal/slice` | `BitemporalCoordinate`; params: none | `BitemporalSlice` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-260` | 779 | `POST /api/v1/graph/bitemporal/topology` | `BitemporalCoordinate`; params: none | `BitemporalTopology` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-261` | 780 | `POST /api/v1/graph/bitemporal/valid-at` | `BitemporalCoordinate`; params: none | `BitemporalSlice` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-262` | 781 | `POST /api/v1/graph/blast-radius` | `BlastRadiusRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-007 | GUI-01: REVIEW |
| `INT-263` | 782 | `POST /api/v1/graph/centrality/full` | `FullCentralityRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-264` | 783 | `POST /api/v1/graph/cluster` | `ClusterRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-265` | 784 | `POST /api/v1/graph/components` | `ComponentsRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-266` | 785 | `POST /api/v1/graph/convert` | `FormatConvertRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-267` | 786 | `POST /api/v1/graph/degree-distribution` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-268` | 787 | `POST /api/v1/graph/diff` | `apps__api__app__DiffRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-269` | 788 | `GET /api/v1/graph/diff` | `none`; params: from, to, limit | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-270` | 789 | `GET /api/v1/graph/events` | `none`; params: since, since_id, limit | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-271` | 790 | `GET /api/v1/graph/formats` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-272` | 791 | `POST /api/v1/graph/k-core` | `KCoreRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-273` | 792 | `POST /api/v1/graph/link-prediction` | `LinkPredictionRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-274` | 793 | `POST /api/v1/graph/merge` | `GraphMergePayload`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-275` | 794 | `POST /api/v1/graph/metrics` | `MetricsRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-276` | 795 | `GET /api/v1/graph/orphaned` | `none`; params: entity_types | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-277` | 796 | `GET /api/v1/graph/pr-impact` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-007 | GUI-01: REVIEW |
| `INT-278` | 797 | `POST /api/v1/graph/reverse-impact` | `BlastRadiusRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-007 | GUI-01: REVIEW |
| `INT-279` | 798 | `GET /api/v1/graph/schema` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-012 | GUI-01: REVIEW |
| `INT-280` | 799 | `POST /api/v1/graph/shortest-paths` | `ShortestPathsRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-007 | GUI-01: REVIEW |
| `INT-281` | 800 | `POST /api/v1/graph/similarity` | `SimilarityRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-282` | 801 | `GET /api/v1/graph/stale` | `none`; params: threshold_hours | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-283` | 802 | `GET /api/v1/graph/statistics` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-284` | 803 | `POST /api/v1/graph/surprises` | `SurpriseRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-285` | 804 | `GET /api/v1/graph/versions` | `none`; params: limit | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-286` | 805 | `POST /api/v1/graph/what-if` | `WhatIfRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-287` | 806 | `GET /api/v1/health/embeddings` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-288` | 807 | `GET /api/v1/health/graph` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-289` | 808 | `GET /api/v1/identity/candidates` | `none`; params: status | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-006 | GUI-01: REVIEW |
| `INT-290` | 809 | `POST /api/v1/identity/candidates/{candidate_id}/decide` | `ProposalDecisionRequest`; params: candidate_id | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-006 | GUI-01: REVIEW |
| `INT-291` | 810 | `POST /api/v1/identity/candidates/{candidate_id}/reject` | `ProposalDecisionRequest`; params: candidate_id | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-006 | GUI-01: REVIEW |
| `INT-292` | 811 | `POST /api/v1/impact` | `apps__api__app__ImpactRequest`; params: none | `TraversalGraphResult` | `IMPLEMENTED-UNVERIFIED` | SCR-007 | GUI-01: REVIEW |
| `INT-293` | 812 | `POST /api/v1/ingest/profile` | `ProfileRequest`; params: none | `ProfileReport` | `IMPLEMENTED-UNVERIFIED` | SCR-025 | GUI-01: REVIEW |
| `INT-294` | 813 | `POST /api/v1/ingest/profile/drift` | `DriftRequest`; params: none | `ProfileDrift` | `IMPLEMENTED-UNVERIFIED` | SCR-025 | GUI-01: REVIEW |
| `INT-295` | 814 | `POST /api/v1/ingest/profile/keys` | `ProfileRequest`; params: none | `array<KeyCandidate>` | `IMPLEMENTED-UNVERIFIED` | SCR-025 | GUI-01: REVIEW |
| `INT-296` | 815 | `POST /api/v1/ingest/profile/relationships` | `RelationshipsRequest`; params: none | `array<RelationshipCandidate>` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-297` | 816 | `GET /api/v1/ingestion/dlq` | `none`; params: limit | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-298` | 817 | `POST /api/v1/ingestion/jira-json` | `IngestionRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-299` | 818 | `POST /api/v1/ingestion/replay` | `ReplayRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-300` | 819 | `GET /api/v1/ingestion/runs` | `none`; params: limit | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-301` | 820 | `GET /api/v1/kgci/report` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-302` | 821 | `POST /api/v1/kgci/run` | `inline`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-303` | 822 | `GET /api/v1/knowledge-debt` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-304` | 823 | `GET /api/v1/knowledge-slos` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-305` | 824 | `GET /api/v1/knowledge/debt` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-306` | 825 | `POST /api/v1/knowledge/firewall/inspect` | `FirewallInspectRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-307` | 826 | `GET /api/v1/knowledge/freshness` | `none`; params: stale_days | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-308` | 827 | `POST /api/v1/knowledge/slo` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-309` | 828 | `GET /api/v1/knowledge/trust/states` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-310` | 829 | `GET /api/v1/lens/catalog` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-311` | 830 | `POST /api/v1/lens/{lens_id}` | `inline`; params: lens_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-312` | 831 | `POST /api/v1/licensing/check-module` | `ModuleCheckRequest`; params: none | `CheckOutcome` | `IMPLEMENTED-UNVERIFIED` | SCR-026 | GUI-01: REVIEW |
| `INT-313` | 832 | `GET /api/v1/licensing/meter/export` | `none`; params: none | `object` | `PARTIAL` | SCR-026 | GUI-01: REVIEW |
| `INT-314` | 833 | `POST /api/v1/licensing/meter/record` | `MeterRecordRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-026 | GUI-01: REVIEW |
| `INT-315` | 834 | `GET /api/v1/licensing/meter/verify` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-026 | GUI-01: REVIEW |
| `INT-316` | 835 | `GET /api/v1/licensing/status` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-026 | GUI-01: REVIEW |
| `INT-317` | 836 | `POST /api/v1/licensing/verify` | `LicenseVerifyRequest`; params: none | `LicenseVerification` | `IMPLEMENTED-UNVERIFIED` | SCR-026 | GUI-01: REVIEW |
| `INT-318` | 837 | `POST /api/v1/lineage` | `LineageRequest`; params: none | `GraphResult` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-319` | 838 | `POST /api/v1/loops/approvals/decide` | `DecideRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-320` | 839 | `GET /api/v1/loops/approvals/pending` | `none`; params: none | `array<ApprovalRequest>` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-321` | 840 | `GET /api/v1/loops/catalog` | `none`; params: none | `LoopCatalog` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-322` | 841 | `POST /api/v1/loops/run/{loop_name}` | `RunLoopRequest`; params: loop_name | `LoopResult` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-323` | 842 | `POST /api/v1/marketplace/build/agent-workflow` | `BuildAgentWorkflowPackageRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-324` | 843 | `POST /api/v1/marketplace/build/dashboard` | `BuildDashboardPackageRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-325` | 844 | `POST /api/v1/marketplace/build/mapping` | `BuildMappingPackageRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-326` | 845 | `POST /api/v1/marketplace/build/query-template` | `BuildQueryTemplatePackageRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-011 | GUI-01: REVIEW |
| `INT-327` | 846 | `POST /api/v1/marketplace/build/validator` | `BuildValidatorPackageRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-328` | 847 | `POST /api/v1/marketplace/install` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-329` | 848 | `GET /api/v1/marketplace/installed` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-330` | 849 | `GET /api/v1/marketplace/installed/search` | `none`; params: q | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-331` | 850 | `GET /api/v1/marketplace/packages` | `none`; params: q | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-332` | 851 | `POST /api/v1/marketplace/packages/install` | `InstallPackageRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-333` | 852 | `DELETE /api/v1/marketplace/packages/{name}` | `none`; params: name | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-334` | 853 | `POST /api/v1/marketplace/uninstall/{name}` | `none`; params: name | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-335` | 854 | `POST /api/v1/moonshot/bitemporal/branch` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-336` | 855 | `POST /api/v1/moonshot/bitemporal/time-warp` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-337` | 856 | `POST /api/v1/moonshot/causal/simulate` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-338` | 857 | `POST /api/v1/moonshot/compliance/audit` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-339` | 858 | `POST /api/v1/moonshot/confidential/zk-proof` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-340` | 859 | `POST /api/v1/moonshot/memory/consolidate` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-341` | 860 | `POST /api/v1/moonshot/self-healing/scan` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-342` | 861 | `POST /api/v1/moonshot/studio/induce` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-343` | 862 | `POST /api/v1/moonshot/transpile` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-344` | 863 | `POST /api/v1/neighborhood` | `NeighborhoodRequest`; params: none | `GraphResult` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-345` | 864 | `POST /api/v1/ontology/diff` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-012, SCR-013 | GUI-01: REVIEW |
| `INT-346` | 865 | `GET /api/v1/ontology/drift` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-012, SCR-013 | GUI-01: REVIEW |
| `INT-347` | 866 | `GET /api/v1/ontology/export` | `none`; params: limit | `none` | `PARTIAL` | SCR-012, SCR-013 | GUI-01: REVIEW |
| `INT-348` | 867 | `GET /api/v1/ontology/gitops/branches` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-012, SCR-013 | GUI-01: REVIEW |
| `INT-349` | 868 | `POST /api/v1/ontology/gitops/branches` | `CreateBranchRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-013 | GUI-01: REVIEW |
| `INT-350` | 869 | `POST /api/v1/ontology/gitops/branches/commit` | `CommitManifestRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-013 | GUI-01: REVIEW |
| `INT-351` | 870 | `POST /api/v1/ontology/gitops/diff` | `eoip__ontology__gitops_router__DiffRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-013 | GUI-01: REVIEW |
| `INT-352` | 871 | `POST /api/v1/ontology/gitops/impact` | `eoip__ontology__gitops_router__ImpactRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-353` | 872 | `POST /api/v1/ontology/gitops/migration` | `MigrationGenRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-354` | 873 | `POST /api/v1/ontology/gitops/package-release` | `PackageReleaseRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-355` | 874 | `POST /api/v1/ontology/gitops/prs` | `CreatePRRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-356` | 875 | `GET /api/v1/ontology/gitops/prs` | `none`; params: status | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-357` | 876 | `POST /api/v1/ontology/gitops/prs/{pr_id}/merge` | `MergePRRequest`; params: pr_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-358` | 877 | `POST /api/v1/ontology/gitops/prs/{pr_id}/review` | `ReviewPRRequest`; params: pr_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-359` | 878 | `POST /api/v1/ontology/gitops/rollback` | `RollbackRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-360` | 879 | `POST /api/v1/ontology/gitops/validate` | `eoip__ontology__gitops_router__DiffRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-361` | 880 | `POST /api/v1/ontology/import` | `object`; params: clear | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-362` | 881 | `GET /api/v1/ontology/packs` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-363` | 882 | `GET /api/v1/ontology/packs/{name}` | `none`; params: name | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-364` | 883 | `POST /api/v1/ontology/proposals` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-365` | 884 | `GET /api/v1/ontology/shacl` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-366` | 885 | `GET /api/v1/ontology/validate` | `none`; params: limit | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-367` | 886 | `GET /api/v1/ops/ha-topology` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-368` | 887 | `POST /api/v1/ops/helm-summary` | `inline`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-369` | 888 | `GET /api/v1/ops/preflight` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-370` | 889 | `POST /api/v1/ops/shard-plan` | `ShardPlanRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-371` | 890 | `GET /api/v1/ops/support-bundle` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-372` | 891 | `POST /api/v1/ops/upgrade-plan` | `UpgradePlanRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-373` | 892 | `POST /api/v1/path` | `PathRequest`; params: none | `GraphResult` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-374` | 893 | `GET /api/v1/pipeline/status` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | SCR-017 | GUI-01: REVIEW |
| `INT-375` | 894 | `POST /api/v1/platform/aiml/hallucination/check` | `HallucinationCheckRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-376` | 895 | `GET /api/v1/platform/aiml/hallucination/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-377` | 896 | `POST /api/v1/platform/aiml/rlhf/preference` | `RLHFPreferenceRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-378` | 897 | `POST /api/v1/platform/aiml/rlhf/reward` | `RewardScoreRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-379` | 898 | `GET /api/v1/platform/aiml/rlhf/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-380` | 899 | `GET /api/v1/platform/aiml/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-381` | 900 | `GET /api/v1/platform/aiml/temperature/best` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-382` | 901 | `POST /api/v1/platform/aiml/temperature/experiment` | `SamplingExperimentRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-383` | 902 | `POST /api/v1/platform/aiml/temperature/trial` | `TrialRecordRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-384` | 903 | `POST /api/v1/platform/aiml/tokens/budget` | `TokenBudgetRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-385` | 904 | `POST /api/v1/platform/aiml/tokens/consume` | `TokenConsumeRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-386` | 905 | `GET /api/v1/platform/compliance/frameworks` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-387` | 906 | `POST /api/v1/platform/context/bitemporal-slate` | `BitemporalSlateRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-388` | 907 | `POST /api/v1/platform/context/build` | `ContextBuildRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-016 | GUI-01: REVIEW |
| `INT-389` | 908 | `POST /api/v1/platform/context/item` | `ContextItemAddRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-390` | 909 | `GET /api/v1/platform/context/items` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-391` | 910 | `POST /api/v1/platform/context/slice-graph` | `GraphSliceRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-392` | 911 | `GET /api/v1/platform/context/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-393` | 912 | `POST /api/v1/platform/copilot/insights` | `CopilotInsightRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-394` | 913 | `GET /api/v1/platform/copilot/insights` | `none`; params: limit | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-395` | 914 | `POST /api/v1/platform/copilot/message` | `CopilotMessageRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-396` | 915 | `GET /api/v1/platform/copilot/rules` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-397` | 916 | `POST /api/v1/platform/copilot/rules` | `CopilotRuleRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-398` | 917 | `GET /api/v1/platform/copilot/sessions` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-399` | 918 | `GET /api/v1/platform/copilot/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-400` | 919 | `GET /api/v1/platform/copilot/suggest/{session_id}` | `none`; params: session_id, limit | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-401` | 920 | `GET /api/v1/platform/cost/recommendations` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-402` | 921 | `POST /api/v1/platform/cost/record` | `CostRecordRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-403` | 922 | `GET /api/v1/platform/cost/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-404` | 923 | `POST /api/v1/platform/edge/nodes` | `EdgeNodeRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-405` | 924 | `GET /api/v1/platform/edge/nodes` | `none`; params: region, status | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-406` | 925 | `GET /api/v1/platform/edge/nodes/{node_id}/query` | `none`; params: node_id, entity_type, limit | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-407` | 926 | `POST /api/v1/platform/edge/promote` | `EdgePromoteRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-408` | 927 | `GET /api/v1/platform/edge/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-409` | 928 | `POST /api/v1/platform/edge/sync` | `EdgeSyncRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-410` | 929 | `POST /api/v1/platform/embeddings/drift` | `EmbeddingDriftRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-411` | 930 | `POST /api/v1/platform/embeddings/versions` | `EmbeddingRegisterRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-412` | 931 | `POST /api/v1/platform/eval/distill-prompts` | `PromptDistillRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-413` | 932 | `POST /api/v1/platform/eval/graph-repair-sentinel` | `GraphRepairSentinelRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-414` | 933 | `POST /api/v1/platform/eval/run` | `EvalRunRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-016 | GUI-01: REVIEW |
| `INT-415` | 934 | `GET /api/v1/platform/eval/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-416` | 935 | `POST /api/v1/platform/eval/suite/run` | `BenchmarkRunRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-417` | 936 | `POST /api/v1/platform/features/extract` | `FeatureExtractRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-418` | 937 | `GET /api/v1/platform/features/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-419` | 938 | `GET /api/v1/platform/gateway/introspect` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-420` | 939 | `GET /api/v1/platform/gateway/openapi` | `none`; params: none | `object` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-421` | 940 | `GET /api/v1/platform/gateway/playground` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-422` | 941 | `POST /api/v1/platform/gateway/query` | `GatewayQueryRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-423` | 942 | `GET /api/v1/platform/gateway/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-424` | 943 | `POST /api/v1/platform/gateway/types` | `GatewayTypeRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-425` | 944 | `POST /api/v1/platform/graph-graph/cross-layer-query` | `CrossLayerQueryRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-426` | 945 | `POST /api/v1/platform/graph-graph/diff` | `none`; params: layer_a, layer_b | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-427` | 946 | `POST /api/v1/platform/graph-graph/layers` | `GraphLayerCreateRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-428` | 947 | `POST /api/v1/platform/graph-loop/execute` | `GraphLoopExecuteRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-429` | 948 | `POST /api/v1/platform/graph-loop/plan` | `GraphLoopPlanRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-430` | 949 | `GET /api/v1/platform/graph-loop/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-431` | 950 | `POST /api/v1/platform/guardrails/inoculate` | `JailbreakInoculateRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-432` | 951 | `POST /api/v1/platform/guardrails/reflection-sandbox` | `ReflectionSandboxRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-433` | 952 | `GET /api/v1/platform/harness/pipelines` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-017 | GUI-01: REVIEW |
| `INT-434` | 953 | `POST /api/v1/platform/harness/run` | `HarnessRunRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-435` | 954 | `GET /api/v1/platform/harness/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-436` | 955 | `POST /api/v1/platform/imports/csv` | `ImportCSVRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-437` | 956 | `GET /api/v1/platform/imports/jobs` | `none`; params: limit | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-438` | 957 | `GET /api/v1/platform/imports/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-439` | 958 | `POST /api/v1/platform/incidents` | `IncidentCreateRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-009 | GUI-01: REVIEW |
| `INT-440` | 959 | `GET /api/v1/platform/incidents` | `none`; params: state, severity, limit | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-009 | GUI-01: REVIEW |
| `INT-441` | 960 | `GET /api/v1/platform/incidents/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-009 | GUI-01: REVIEW |
| `INT-442` | 961 | `GET /api/v1/platform/incidents/{incident_id}` | `none`; params: incident_id | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-009 | GUI-01: REVIEW |
| `INT-443` | 962 | `POST /api/v1/platform/incidents/{incident_id}/transition` | `IncidentTransitionRequest`; params: incident_id | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-009 | GUI-01: REVIEW |
| `INT-444` | 963 | `GET /api/v1/platform/integrations` | `none`; params: connector_type | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-014 | GUI-01: REVIEW |
| `INT-445` | 964 | `GET /api/v1/platform/integrations/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-446` | 965 | `POST /api/v1/platform/integrations/{connector_id}/health` | `none`; params: connector_id | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-014 | GUI-01: REVIEW |
| `INT-447` | 966 | `GET /api/v1/platform/integrations/{connector_id}/history` | `none`; params: connector_id, limit | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-014 | GUI-01: REVIEW |
| `INT-448` | 967 | `POST /api/v1/platform/integrations/{connector_id}/sync` | `none`; params: connector_id | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-014 | GUI-01: REVIEW |
| `INT-449` | 968 | `POST /api/v1/platform/intelligence/analyze` | `IntelligenceAnalyzeRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-450` | 969 | `GET /api/v1/platform/intelligence/autonomy/{query}` | `none`; params: query | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-451` | 970 | `GET /api/v1/platform/intelligence/capabilities` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-452` | 971 | `POST /api/v1/platform/intelligence/pipeline` | `IntelligencePipelineRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-453` | 972 | `POST /api/v1/platform/intelligence/plan` | `IntelligencePlanRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-454` | 973 | `GET /api/v1/platform/intelligence/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-455` | 974 | `POST /api/v1/platform/intelligence/supervisory-loop` | `SupervisoryLoopExecuteRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-456` | 975 | `GET /api/v1/platform/maintenance/enrichments` | `none`; params: status, limit | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-457` | 976 | `GET /api/v1/platform/maintenance/entity/{entity_id}` | `none`; params: entity_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-458` | 977 | `POST /api/v1/platform/maintenance/scan` | `none`; params: threshold_days | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-459` | 978 | `GET /api/v1/platform/maintenance/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-460` | 979 | `POST /api/v1/platform/memory/recall` | `MemoryRecallRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-461` | 980 | `GET /api/v1/platform/memory/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-462` | 981 | `POST /api/v1/platform/memory/store` | `MemoryStoreRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-463` | 982 | `POST /api/v1/platform/mlops/experiments` | `ExperimentCreateRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-464` | 983 | `POST /api/v1/platform/mlops/runs/start` | `RunStartRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-465` | 984 | `POST /api/v1/platform/mlops/runs/{run_id}/metrics` | `RunLogMetricRequest`; params: run_id, exp_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-466` | 985 | `GET /api/v1/platform/models` | `none`; params: status, model_type | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-467` | 986 | `GET /api/v1/platform/models/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-468` | 987 | `GET /api/v1/platform/notifications/inbox/{recipient}` | `none`; params: recipient, unread_only, limit | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-026 | GUI-01: REVIEW |
| `INT-469` | 988 | `POST /api/v1/platform/notifications/send` | `NotifSendRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-026 | GUI-01: REVIEW |
| `INT-470` | 989 | `GET /api/v1/platform/notifications/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-471` | 990 | `POST /api/v1/platform/notifications/{notification_id}/read` | `none`; params: notification_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-472` | 991 | `GET /api/v1/platform/prompts/list` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-473` | 992 | `POST /api/v1/platform/prompts/register` | `PromptRegisterRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-474` | 993 | `POST /api/v1/platform/prompts/render` | `PromptRenderRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-475` | 994 | `GET /api/v1/platform/prompts/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-476` | 995 | `GET /api/v1/platform/reasoning/inferences` | `none`; params: limit | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-477` | 996 | `GET /api/v1/platform/reasoning/rules` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-478` | 997 | `GET /api/v1/platform/reasoning/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-479` | 998 | `POST /api/v1/platform/recovery/checkpoint` | `none`; params: label | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-480` | 999 | `GET /api/v1/platform/recovery/checkpoints` | `none`; params: limit | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-481` | 1000 | `GET /api/v1/platform/recovery/peers` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-482` | 1001 | `POST /api/v1/platform/recovery/peers` | `WALPeerRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-483` | 1002 | `POST /api/v1/platform/recovery/restore/{point_id}` | `none`; params: point_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-484` | 1003 | `GET /api/v1/platform/recovery/rpo` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-485` | 1004 | `GET /api/v1/platform/recovery/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-486` | 1005 | `POST /api/v1/platform/recovery/wal/append` | `WALAppendRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-487` | 1006 | `GET /api/v1/platform/recovery/wal/read` | `none`; params: start_lsn, limit | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-488` | 1007 | `POST /api/v1/platform/routing/classify-and-route` | `RoutingClassifyRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-489` | 1008 | `GET /api/v1/platform/routing/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-490` | 1009 | `POST /api/v1/platform/search/edge` | `HybridSearchEdgeRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-491` | 1010 | `POST /api/v1/platform/search/index` | `HybridSearchIndexRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-492` | 1011 | `GET /api/v1/platform/search/metrics` | `none`; params: limit | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-493` | 1012 | `GET /api/v1/platform/search/plan` | `none`; params: query | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-494` | 1013 | `POST /api/v1/platform/search/query` | `HybridSearchQueryRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-495` | 1014 | `GET /api/v1/platform/search/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-496` | 1015 | `POST /api/v1/platform/search/user-context` | `HybridSearchUserContextRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-497` | 1016 | `POST /api/v1/platform/security/red-team` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-498` | 1017 | `POST /api/v1/platform/security/scan` | `SecurityScanRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-499` | 1018 | `GET /api/v1/platform/security/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-500` | 1019 | `GET /api/v1/platform/semantic/drift` | `none`; params: old_snapshot, new_snapshot, threshold | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-501` | 1020 | `POST /api/v1/platform/semantic/hybrid` | `PlatformHybridSearchRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-502` | 1021 | `POST /api/v1/platform/semantic/index` | `SemanticIndexRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-503` | 1022 | `POST /api/v1/platform/semantic/search` | `SemanticSearchRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-504` | 1023 | `GET /api/v1/platform/semantic/similar/{entity_id}` | `none`; params: entity_id, top_k | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-505` | 1024 | `POST /api/v1/platform/semantic/snapshot/{snapshot_id}` | `none`; params: snapshot_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-506` | 1025 | `GET /api/v1/platform/semantic/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-507` | 1026 | `POST /api/v1/platform/specs/define` | `SpecDefineRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-508` | 1027 | `GET /api/v1/platform/specs/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-509` | 1028 | `POST /api/v1/platform/state/record` | `StateRecordRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-510` | 1029 | `POST /api/v1/platform/state/restore` | `StateRestoreRequest`; params: none | `object` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-511` | 1030 | `POST /api/v1/platform/state/snapshot` | `StateSnapshotRequest`; params: none | `object` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-512` | 1031 | `GET /api/v1/platform/state/snapshots` | `none`; params: stream | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-513` | 1032 | `GET /api/v1/platform/state/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-514` | 1033 | `GET /api/v1/platform/state/stream/{stream}` | `none`; params: stream | `object` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-515` | 1034 | `GET /api/v1/platform/streaming/channels/{channel}/latest` | `none`; params: channel, limit | `object` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-516` | 1035 | `GET /api/v1/platform/streaming/stats` | `none`; params: none | `object` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-517` | 1036 | `GET /api/v1/platform/streaming/subscriptions` | `none`; params: none | `object` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-518` | 1037 | `GET /api/v1/platform/tasks` | `none`; params: tag, enabled_only | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-519` | 1038 | `GET /api/v1/platform/tasks/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-520` | 1039 | `POST /api/v1/platform/tasks/{task_id}/execute` | `none`; params: task_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-521` | 1040 | `GET /api/v1/platform/tasks/{task_id}/history` | `none`; params: task_id, limit | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-522` | 1041 | `POST /api/v1/platform/token-budget/allocate` | `TokenBudgetAllocateRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-523` | 1042 | `POST /api/v1/platform/token-budget/consume` | `TokenBudgetConsumeRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-524` | 1043 | `GET /api/v1/platform/token-budget/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-525` | 1044 | `POST /api/v1/platform/token-formats/benchmark` | `TokenFormatSerializeRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-526` | 1045 | `POST /api/v1/platform/token-formats/deserialize` | `TokenFormatDeserializeRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-527` | 1046 | `POST /api/v1/platform/token-formats/serialize` | `TokenFormatSerializeRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-528` | 1047 | `POST /api/v1/platform/tools/attest-execution` | `ToolAttestExecutionRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-529` | 1048 | `GET /api/v1/platform/tools/list` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-530` | 1049 | `POST /api/v1/platform/tools/mcp/connect-external` | `ExternalMCPConnectRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-531` | 1050 | `GET /api/v1/platform/tools/mcp/manifest` | `none`; params: none | `object` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-532` | 1051 | `POST /api/v1/platform/tools/register` | `ToolRegisterRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-533` | 1052 | `GET /api/v1/platform/tools/stats` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-534` | 1053 | `POST /api/v1/platform/tools/validate-call` | `ToolValidateCallRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-535` | 1054 | `POST /api/v1/platform/tools/verify-attestation` | `ToolVerifyAttestationRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-536` | 1055 | `GET /api/v1/platform/verification/audit-trail` | `none`; params: limit | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-537` | 1056 | `POST /api/v1/platform/verification/check` | `VerificationCheckRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-538` | 1057 | `POST /api/v1/platform/verification/guardrail-interception` | `GuardrailCheckRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-539` | 1058 | `POST /api/v1/platform/xai/calibrate` | `XAICalibrateRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-540` | 1059 | `POST /api/v1/platform/xai/explain` | `XAIExplainRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-541` | 1060 | `POST /api/v1/playback/evidence` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-542` | 1061 | `POST /api/v1/playback/export` | `object`; params: none | `none` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-543` | 1062 | `POST /api/v1/playback/stream` | `object`; params: none | `none` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-544` | 1063 | `POST /api/v1/privacy/classify` | `ClassifyRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-545` | 1064 | `POST /api/v1/privacy/consents` | `ConsentRecord`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-546` | 1065 | `GET /api/v1/privacy/consents/allowed` | `none`; params: subject_id, purpose, tenant_id, source | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-547` | 1066 | `POST /api/v1/privacy/dsar/erase` | `LocateRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-548` | 1067 | `POST /api/v1/privacy/dsar/locate` | `LocateRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-549` | 1068 | `POST /api/v1/privacy/residency/validate` | `ResidencyRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-550` | 1069 | `POST /api/v1/privacy/retention/evaluate` | `RetentionRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-551` | 1070 | `GET /api/v1/process/cases` | `none`; params: source_label | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-552` | 1071 | `POST /api/v1/process/deviations` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-553` | 1072 | `GET /api/v1/process/paths` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-554` | 1073 | `GET /api/v1/product/capabilities` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-555` | 1074 | `POST /api/v1/product/capabilities/materialize` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-556` | 1075 | `GET /api/v1/product/first-choice-gate` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-557` | 1076 | `GET /api/v1/qa/dashboard` | `none`; params: requirement_ids | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-558` | 1077 | `POST /api/v1/qa/dashboard/external-gates` | `ExternalGateRecord`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-559` | 1078 | `POST /api/v1/qa/dashboard/test-runs` | `TestRunSummary`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-560` | 1079 | `GET /api/v1/qa/evidence/coverage` | `none`; params: requirement_ids | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-561` | 1080 | `GET /api/v1/qa/evidence/coverage/{requirement_id}` | `none`; params: requirement_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-562` | 1081 | `POST /api/v1/qa/evidence/register` | `EvidenceEntry`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-563` | 1082 | `GET /api/v1/qa/inventory` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-564` | 1083 | `POST /api/v1/qa/inventory/validate` | `InventorySnapshot`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-565` | 1084 | `GET /api/v1/qa/mutation-checks` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-566` | 1085 | `POST /api/v1/qa/mutation-checks` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-567` | 1086 | `GET /api/v1/qa/mutation-checks/release/{release}` | `none`; params: release | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-568` | 1087 | `GET /api/v1/qa/policy-gate/latest` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-569` | 1088 | `POST /api/v1/qa/policy-gate/run` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-570` | 1089 | `POST /api/v1/query` | `QueryPlan`; params: none | `GraphResult` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-571` | 1090 | `GET /api/v1/query/cache/stats` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-572` | 1091 | `GET /api/v1/query/context/{entity_cid}` | `none`; params: entity_cid | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-573` | 1092 | `POST /api/v1/query/cost` | `QueryPlan`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-574` | 1093 | `POST /api/v1/query/eql` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-575` | 1094 | `POST /api/v1/query/explain` | `QueryPlan`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-576` | 1095 | `GET /api/v1/query/history` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-577` | 1096 | `POST /api/v1/query/language` | `QueryLanguageRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-578` | 1097 | `POST /api/v1/query/multi-paradigm` | `MultiParadigmQueryRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-579` | 1098 | `POST /api/v1/query/nl` | `NLQueryRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-580` | 1099 | `GET /api/v1/query/slow` | `none`; params: threshold_ms, top_n | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-581` | 1100 | `GET /api/v1/query/templates` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-582` | 1101 | `POST /api/v1/query/templates` | `TemplateSaveRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-583` | 1102 | `GET /api/v1/query/templates/{template_id}` | `none`; params: template_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-584` | 1103 | `DELETE /api/v1/query/templates/{template_id}` | `none`; params: template_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-585` | 1104 | `POST /api/v1/query/templates/{template_id}/bind` | `TemplateBindRequest`; params: template_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-586` | 1105 | `POST /api/v1/query/what-changed` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-587` | 1106 | `GET /api/v1/query/what-changed/{entity_cid}` | `none`; params: entity_cid | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-588` | 1107 | `POST /api/v1/query/what-if` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-589` | 1108 | `POST /api/v1/query/why` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-590` | 1109 | `POST /api/v1/query/why-not` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-591` | 1110 | `GET /api/v1/query/why/{entity_cid}` | `none`; params: entity_cid | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-592` | 1111 | `POST /api/v1/rag` | `RetrievalRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-593` | 1112 | `GET /api/v1/rag/patterns` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-594` | 1113 | `POST /api/v1/rag/query` | `RAGQueryRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-595` | 1114 | `GET /api/v1/reports` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-596` | 1115 | `GET /api/v1/reports/export/{report_id}` | `none`; params: report_id, report_format | `object` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-597` | 1116 | `POST /api/v1/reports/render` | `ReportContext`; params: template_id, report_format, generated_at | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-598` | 1117 | `GET /api/v1/reports/schedules` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-599` | 1118 | `POST /api/v1/reports/schedules` | `inline`; params: template_id, name, recurrence, report_format | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-600` | 1119 | `GET /api/v1/reports/schedules/due` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-601` | 1120 | `DELETE /api/v1/reports/schedules/{schedule_id}` | `none`; params: schedule_id | `HTTPValidationError` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-602` | 1121 | `POST /api/v1/reports/schedules/{schedule_id}/mark-run` | `none`; params: schedule_id, at | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-603` | 1122 | `GET /api/v1/reports/templates` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-604` | 1123 | `POST /api/v1/retrieval/search` | `RetrievalSearchRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-605` | 1124 | `GET /api/v1/search` | `none`; params: q, label, limit, include_deleted | `GraphResult` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-606` | 1125 | `POST /api/v1/search/faceted` | `SearchRequest`; params: none | `SearchResponse` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-607` | 1126 | `GET /api/v1/security/policy-matrix` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-608` | 1127 | `GET /api/v1/security/status` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-609` | 1128 | `POST /api/v1/security/tokens/issue` | `IssueTokenRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-610` | 1129 | `POST /api/v1/security/tokens/revoke` | `RevokeTokenRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-611` | 1130 | `POST /api/v1/security/tokens/verify` | `VerifyTokenRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-612` | 1131 | `POST /api/v1/simulation/create` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-613` | 1132 | `GET /api/v1/simulation/list` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-614` | 1133 | `GET /api/v1/simulation/{sim_id}/analyze` | `none`; params: sim_id, analysis_type | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-615` | 1134 | `GET /api/v1/simulation/{sim_id}/compare` | `none`; params: sim_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-616` | 1135 | `GET /api/v1/simulation/{sim_id}/manifest` | `none`; params: sim_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-617` | 1136 | `POST /api/v1/simulation/{sim_id}/mutate` | `object`; params: sim_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-618` | 1137 | `POST /api/v1/simulations` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-619` | 1138 | `GET /api/v1/simulations/{sim_id}` | `none`; params: sim_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-620` | 1139 | `GET /api/v1/sources` | `none`; params: none | `array<SourceRegistryEntry>` | `IMPLEMENTED-UNVERIFIED` | SCR-014 | GUI-01: REVIEW |
| `INT-621` | 1140 | `POST /api/v1/sources` | `SourceRegistryEntry`; params: none | `SourceRegistryEntry` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-622` | 1141 | `GET /api/v1/sources/{source_id}` | `none`; params: source_id | `SourceRegistryEntry` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-623` | 1142 | `PATCH /api/v1/sources/{source_id}` | `SourceRegistryPatch`; params: source_id | `SourceRegistryEntry` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-624` | 1143 | `DELETE /api/v1/sources/{source_id}` | `none`; params: source_id | `HTTPValidationError` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-625` | 1144 | `POST /api/v1/sources/{source_id}/baseline` | `SourceOperationRequest`; params: source_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-626` | 1145 | `GET /api/v1/sources/{source_id}/checkpoint` | `none`; params: source_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-627` | 1146 | `POST /api/v1/sources/{source_id}/discover` | `inline`; params: source_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-628` | 1147 | `POST /api/v1/sources/{source_id}/dry-run` | `SourceOperationRequest`; params: source_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-629` | 1148 | `POST /api/v1/sources/{source_id}/pause` | `none`; params: source_id | `AcquisitionPolicy` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-630` | 1149 | `POST /api/v1/sources/{source_id}/reconcile` | `SourceOperationRequest`; params: source_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-631` | 1150 | `GET /api/v1/sources/{source_id}/reconciliations` | `none`; params: source_id, limit | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-632` | 1151 | `POST /api/v1/sources/{source_id}/replay` | `SourceOperationRequest`; params: source_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-633` | 1152 | `POST /api/v1/sources/{source_id}/resume` | `none`; params: source_id | `AcquisitionPolicy` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-634` | 1153 | `GET /api/v1/sources/{source_id}/schedule` | `none`; params: source_id | `AcquisitionPolicy` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-635` | 1154 | `PUT /api/v1/sources/{source_id}/schedule` | `AcquisitionPolicy`; params: source_id | `AcquisitionPolicy` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-636` | 1155 | `POST /api/v1/sources/{source_id}/sync` | `SourceOperationRequest`; params: source_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-637` | 1156 | `POST /api/v1/sources/{source_id}/webhooks` | `none`; params: source_id | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-638` | 1157 | `POST /api/v1/suggest` | `SuggestionRequest`; params: none | `SuggestionResponse` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-639` | 1158 | `GET /api/v1/suggest/intents` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-640` | 1159 | `POST /api/v1/suggest/interpret` | `SuggestionRequest`; params: none | `SuggestionResponse` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-641` | 1160 | `GET /api/v1/systems/` | `none`; params: status, category | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-642` | 1161 | `GET /api/v1/systems/export/config` | `none`; params: none | `object` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-643` | 1162 | `POST /api/v1/systems/import/config` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-644` | 1163 | `GET /api/v1/systems/known-types` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-645` | 1164 | `POST /api/v1/systems/register` | `RegisterSystemRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-646` | 1165 | `POST /api/v1/systems/schema/from-data` | `SchemaFromDataRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-647` | 1166 | `GET /api/v1/systems/{system_id}` | `none`; params: system_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-648` | 1167 | `PUT /api/v1/systems/{system_id}` | `UpdateSystemRequest`; params: system_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-649` | 1168 | `DELETE /api/v1/systems/{system_id}` | `none`; params: system_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-650` | 1169 | `POST /api/v1/systems/{system_id}/create-pipeline` | `none`; params: system_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-651` | 1170 | `POST /api/v1/systems/{system_id}/generate-schema` | `OnboardRequest`; params: system_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-652` | 1171 | `POST /api/v1/systems/{system_id}/onboard` | `OnboardRequest`; params: system_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-653` | 1172 | `GET /api/v1/systems/{system_id}/onboarding-status` | `none`; params: system_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-654` | 1173 | `POST /api/v1/systems/{system_id}/set-status` | `none`; params: system_id, status | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-655` | 1174 | `POST /api/v1/systems/{system_id}/test-connection` | `none`; params: system_id | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-656` | 1175 | `POST /api/v1/taxonomy/concepts` | `SkosConceptRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-657` | 1176 | `GET /api/v1/taxonomy/concepts` | `none`; params: scheme | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-658` | 1177 | `GET /api/v1/taxonomy/export.rdf` | `none`; params: none | `none` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-659` | 1178 | `GET /api/v1/taxonomy/mappings` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-660` | 1179 | `POST /api/v1/taxonomy/mappings` | `SkosMappingRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-661` | 1180 | `GET /api/v1/taxonomy/schemes` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-662` | 1181 | `POST /api/v1/taxonomy/schemes` | `SkosSchemeRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-663` | 1182 | `GET /api/v1/taxonomy/validate` | `none`; params: scheme | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-664` | 1183 | `GET /api/v1/tenancy/context` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-665` | 1184 | `GET /api/v1/tenancy/isolation/models` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-666` | 1185 | `GET /api/v1/tenancy/isolation/placement` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-667` | 1186 | `POST /api/v1/tenancy/isolation/placement` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-668` | 1187 | `POST /api/v1/tenancy/lifecycle/clone` | `none`; params: none | `inline` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-669` | 1188 | `POST /api/v1/tenancy/lifecycle/configure` | `none`; params: none | `inline` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-670` | 1189 | `POST /api/v1/tenancy/lifecycle/delete` | `none`; params: none | `inline` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-671` | 1190 | `POST /api/v1/tenancy/lifecycle/export` | `none`; params: none | `inline` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-672` | 1191 | `POST /api/v1/tenancy/lifecycle/provision` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-673` | 1192 | `POST /api/v1/tenancy/lifecycle/resume` | `none`; params: none | `inline` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-674` | 1193 | `POST /api/v1/tenancy/lifecycle/suspend` | `none`; params: none | `inline` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-675` | 1194 | `GET /api/v1/tenancy/metering/export` | `none`; params: none | `object` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-676` | 1195 | `POST /api/v1/tenancy/metering/record` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-677` | 1196 | `GET /api/v1/tenancy/metering/verify` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-678` | 1197 | `GET /api/v1/tenancy/quotas` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-022 | GUI-01: REVIEW |
| `INT-679` | 1198 | `POST /api/v1/tenancy/quotas/check` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-022 | GUI-01: REVIEW |
| `INT-680` | 1199 | `POST /api/v1/tenancy/quotas/consume` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-022 | GUI-01: REVIEW |
| `INT-681` | 1200 | `POST /api/v1/tenancy/quotas/refund` | `object`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | SCR-022 | GUI-01: REVIEW |
| `INT-682` | 1201 | `POST /api/v1/traceability` | `TraceabilityRequest`; params: none | `GraphResult` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-683` | 1202 | `GET /api/v1/truth/assertions/{subject_id}/{predicate}` | `none`; params: subject_id, predicate | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-684` | 1203 | `POST /api/v1/truth/claims` | `Claim`; params: none | `Claim` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-685` | 1204 | `GET /api/v1/truth/contradictions` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-686` | 1205 | `GET /api/v1/truth/explain/{subject_id}/{predicate}` | `none`; params: subject_id, predicate | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-687` | 1206 | `GET /api/v1/truth/export` | `none`; params: none | `none` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-688` | 1207 | `POST /api/v1/truth/resolve` | `TruthResolveRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-689` | 1208 | `POST /api/v1/twin/business/capabilities` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-690` | 1209 | `GET /api/v1/twin/business/chain/{objective_cid}` | `none`; params: objective_cid | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-691` | 1210 | `POST /api/v1/twin/business/link` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-692` | 1211 | `POST /api/v1/twin/business/objectives` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-693` | 1212 | `GET /api/v1/twin/business/reverse-impact/{service_cid}` | `none`; params: service_cid | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-694` | 1213 | `GET /api/v1/twin/classify` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-695` | 1214 | `GET /api/v1/twin/coverage` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-696` | 1215 | `POST /api/v1/twin/decisions/extract` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-697` | 1216 | `POST /api/v1/twin/decisions/ingest` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-698` | 1217 | `GET /api/v1/twin/decisions/{entity_cid}` | `none`; params: entity_cid | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-699` | 1218 | `GET /api/v1/twin/missing-links` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-700` | 1219 | `GET /api/v1/twin/test-intelligence/mappings` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-701` | 1220 | `GET /api/v1/twin/test-intelligence/runs` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-702` | 1221 | `POST /api/v1/twin/test-intelligence/select` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-703` | 1222 | `GET /api/v1/validation/runs` | `none`; params: limit | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-704` | 1223 | `POST /api/v1/whatif/execute` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-705` | 1224 | `POST /api/v1/whatif/plan` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-706` | 1225 | `POST /api/v1/xai/certify-decision` | `CertifyDecisionRequest`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-707` | 1226 | `POST /api/v1/xai/verify-certificate` | `object`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-708` | 1227 | `GET /brain/agents` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-709` | 1228 | `GET /brain/approaches` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-710` | 1229 | `POST /brain/ask` | `BrainAskRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-711` | 1230 | `GET /brain/databases` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-712` | 1231 | `GET /brain/dialects` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-713` | 1232 | `POST /brain/induce` | `InduceRequest`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-714` | 1233 | `POST /brain/intelligent-query` | `IntelligentQueryRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-715` | 1234 | `POST /brain/learning/load` | `none`; params: directory | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-716` | 1235 | `GET /brain/learning/policy` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-717` | 1236 | `POST /brain/learning/save` | `none`; params: directory | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-718` | 1237 | `GET /brain/learning/status` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-719` | 1238 | `POST /brain/learning/train` | `LearningTrainRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-720` | 1239 | `POST /brain/llm/embed` | `LLMEmbedRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-721` | 1240 | `POST /brain/llm/explain` | `LLMGenerateRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-722` | 1241 | `POST /brain/llm/generate` | `LLMGenerateRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-723` | 1242 | `GET /brain/llm/models` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-724` | 1243 | `POST /brain/llm/stream` | `LLMGenerateRequest`; params: none | `array` | `PARTIAL` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-725` | 1244 | `POST /brain/llm/tokenize` | `LLMTokenizeRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-726` | 1245 | `GET /brain/loops` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-727` | 1246 | `POST /brain/narrate` | `CognitiveNarrateRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-728` | 1247 | `POST /brain/query` | `BrainQueryReportRequest`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-729` | 1248 | `GET /brain/rag-modes` | `none`; params: none | `array` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-730` | 1249 | `GET /brain/snapshot` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-731` | 1250 | `GET /brain/telemetry` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-732` | 1251 | `GET /health/live` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-733` | 1252 | `GET /health/ready` | `none`; params: none | `object` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-734` | 1253 | `GET /metrics` | `none`; params: none | `none` | `IMPLEMENTED-UNVERIFIED` | No primary screen assigned | GUI-01: ASSIGN |
| `INT-735` | 1254 | `WS /api/v1/ws/jobs/{job_id}` | path job_id; auth/tenant contract absent | JSON job events, schema not published | `PARTIAL` | SCR-017, SCR-024 | GUI-01: REVIEW |

## Appendix D. Missing-Contract Coverage

All entries remain unverified design/implementation dependencies until section 10 acceptance passes. Each minimum route also needs the companion lifecycle operations described there.

| ID | Source line | Source proposal | Source screens | Required package |
|---|---|---|---|---|
| `BACKEND-MISSING-001` | 1260 | `POST /api/v1/session/exchange` | SCR-001 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-002` | 1261 | `GET /api/v1/me` | SCR-001 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-003` | 1262 | `GET/PUT /api/v1/onboarding` | SCR-002 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-004` | 1263 | `POST /api/v1/workspaces/{w}/graph/views` | SCR-005 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-005` | 1264 | `GET /api/v1/brain/answers/{id}/events` | SCR-004 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-006` | 1265 | `GET /api/v1/entities/{id}/360` | SCR-006 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-007` | 1266 | `POST /api/v1/impact/plans` | SCR-007 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-008` | 1267 | `POST /api/v1/incidents/{id}/workspaces` | SCR-009 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-009` | 1268 | `POST /api/v1/query/validate\|explain\|profile\|cancel` | SCR-011 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-010` | 1269 | `POST /api/v1/ontology/drafts/{id}/publish` | SCR-012 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-011` | 1270 | `POST/PATCH /api/v1/uploads` | SCR-015 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-012` | 1271 | `POST /api/v1/mappings/{id}/review` | SCR-015 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-013` | 1272 | `POST /api/v1/resolution/actions` | SCR-016 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-014` | 1273 | `GET /api/v1/agents/runs/{id}/events` | SCR-018 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-015` | 1274 | `POST /api/v1/reports/{id}/exports` | SCR-019 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-016` | 1275 | `WS /api/v1/collaboration/{workspace}` | SCR-020 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-017` | 1276 | `PUT /api/v1/tenants/{id}/model-data-policy` | SCR-021 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-018` | 1277 | `POST /api/v1/tenants/{id}/brand/publish` | SCR-023 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-019` | 1278 | `GET/PUT /api/v1/me/preferences` | SCR-025 | GUI-01 and owning SCR package |
| `BACKEND-MISSING-020` | 1279 | `GET /api/v1/about/licenses` | SCR-026 | GUI-01 and owning SCR package |

## Appendix E. Technology-Version Review Checklist

The following 38 version entries reproduce the requirements document, not a newly approved install set. All require GUI-02 compatibility, licence, engine, peer, security and bundle checks. Four existence checks are recorded in section 2.4; existence is not compatibility or current-latest verification. Confirm actual npm package names for every library and commit the tested resolution/lockfile.

| Source library | Source version | Review status |
|---|---|---|
| React | `19.3.0` | Exact version existence checked; qualification OPEN |
| Vite | `8.3.4` | Exact version existence checked; qualification OPEN |
| TypeScript | `7.0.2` | Exact version existence checked; qualification OPEN |
| TanStack Router | `1.170.42` | Source claim only; qualification OPEN |
| TanStack Query | `5.104.2` | Source claim only; qualification OPEN |
| Zustand | `5.0.15` | Source claim only; qualification OPEN |
| XState | `5.33.2` | Source claim only; qualification OPEN |
| Tailwind CSS | `4.3.3` | Source claim only; qualification OPEN |
| Radix Dialog | `1.3.0` | Source claim only; qualification OPEN |
| Motion | `14.1.0` | Source claim only; qualification OPEN |
| Sigma | `4.0.0` | Source claim only; qualification OPEN |
| Graphology | `0.26.0` | Source claim only; qualification OPEN |
| graphology-layout-forceatlas2 | `0.10.1` | Source claim only; qualification OPEN |
| React Flow | `12.12.0` | Source claim only; qualification OPEN |
| ELK.js | `0.12.0` | Source claim only; qualification OPEN |
| Apache ECharts | `6.1.0` | Source claim only; qualification OPEN |
| TanStack Table | `9.3.1` | Source claim only; qualification OPEN |
| TanStack Virtual | `3.14.17` | Source claim only; qualification OPEN |
| Monaco Editor | `0.57.0` | Source claim only; qualification OPEN |
| Tiptap React | `3.31.4` | Source claim only; qualification OPEN |
| React Hook Form | `7.90.0` | Source claim only; qualification OPEN |
| Zod | `4.6.7` | Source claim only; qualification OPEN |
| openapi-typescript | `7.13.0` | Source claim only; qualification OPEN |
| openapi-fetch | `0.17.0` | Source claim only; qualification OPEN |
| cmdk | `1.1.1` | Source claim only; qualification OPEN |
| react-hotkeys-hook | `5.3.3` | Source claim only; qualification OPEN |
| dnd-kit core | `6.3.1` | Source claim only; qualification OPEN |
| react-resizable-panels | `4.14.4` | Source claim only; qualification OPEN |
| Lucide React | `1.55.0` | Source claim only; qualification OPEN |
| i18next | `26.4.4` | Source claim only; qualification OPEN |
| Dexie | `4.4.6` | Source claim only; qualification OPEN |
| Yjs | `13.6.33` | Source claim only; qualification OPEN |
| Tauri API | `2.12.3` | Source claim only; qualification OPEN |
| Vitest | `5.0.4` | Source claim only; qualification OPEN |
| Playwright | `1.64.0` | Exact version existence checked; qualification OPEN |
| MSW | `3.0.3` | Source claim only; qualification OPEN |
| Storybook | `10.6.1` | Source claim only; qualification OPEN |
| axe-core | `4.14.0` | Source claim only; qualification OPEN |

## Appendix F. Plan Integrity Checklist

- Source identity, hash and 1,395-line inventory are recorded; the original requirements file is unchanged.
- All 23 source sections, 27 SCR specifications, 735 INT rows and 20 BACKEND-MISSING families are indexed.
- All 584 unassigned integrations remain explicit review work; the INT-735 mapping discrepancy is not hidden.
- Every screen has a specific workflow, dependencies, failure cases and required behavioral/integration proof.
- GUI-00 through GUI-17 define implementation order, owners, deliverables, exits and rollback considerations.
- Shared clauses cover design tokens, icon/control grammar, animation, graph semantics, forms, accessibility, localization, security, offline behavior, performance and telemetry.
- Code and test paths are explicitly insufficient proof; receipt validation, real runtime checks, negative controls, visual/manual reviews and source binding are mandatory.
- All open business/backend/qualification decisions remain visible; no runtime pass or legal clearance is asserted by the plan.
- This preparation pass validates the document structure and coverage, not delivery of the future GUI or completion of its tests.

Preparation validation completed: 27 distinct screen packages, 20 missing-backend packages, 18 engineering packages, 735 distinct integration rows with no missing INT identifiers, 38 source dependency-version entries, balanced code fences and existing local Markdown link targets. The source requirements hash remained unchanged. These are document-integrity checks only; no application acceptance pass is asserted.
