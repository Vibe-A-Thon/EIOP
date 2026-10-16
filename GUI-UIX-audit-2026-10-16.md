# EOIP GUI Audit and Implementation Follow-Up

Date: 2026-10-16, Asia/Calcutta. Scope: existing web GUI, its integration boundaries, and the first implementation slices against `GUI-UIX-requirements.md` and `GUI-UIX-implementation-plan.md`.

Source requirements SHA-256, LF-normalized: `fc4cfc1692239a157aa09467be25087a6a8def2a254c445fbb7696d4561e3bff`.

Historical GUI inspected initially at `edfa7aed607b8509da5801acc16490c97f5fe375`. Foundation work from this task was subsequently committed by the user in `ef5f685` after the plan commit `9ca7dba`. Further working-tree changes to graph isolation, reports, event persistence and tests appeared during the audit. Those changes have been preserved. This report distinguishes inspected GUI findings from backend qualifications that remain incomplete.

## 1. Result and Evidence Rules

The existing GUI contains substantial useful functionality, including graph search/traversal, entity inspection, ingestion administration, schema tooling, investigations, cognitive dashboards and multiple export paths. It does not yet implement the full 27-screen specification. Several formerly displayed results were fabricated examples or success states shown after failed operations. A functioning component or a registered endpoint was repeatedly insufficient evidence of the underlying requirement.

The first implementation batch improves the shared shell, credential lifetime, request cancellation, policy editing, truthful administrative states, accessibility, loading cost and export handling. These are bounded repairs and foundations. They do not establish complete sessions, tenant/workspace UI isolation, real model inference, all requested screens, full WCAG conformance or commercial scale readiness.

Acceptance labels used below:

- **REPAIRED:** a concrete code change exists; the verification record states which behavior was exercised.
- **CONTAINED:** misleading or unsafe behavior was removed; the complete requested capability remains open.
- **PARTIAL:** useful implementation exists, but material acceptance clauses remain.
- **OPEN:** implementation, integration, decision or qualification still required.
- **HISTORICAL:** a past result retained for comparison; it does not qualify the current working tree.

Code paths and test paths in this report identify where to investigate. They are not completion certificates. Mocked browser checks prove controlled UI behavior only. Real API tests prove only the specific runtime and storage profile used. Manual assistive-technology, visual, usability, deployment and legal approvals must be recorded independently.

## 2. Audit Method and Coverage

1. Loaded and parsed the entire 1,395-line requirements source. Retained all 1,258 nonblank source lines without removing repeated obligations.
2. Reconciled 23 numbered sections, 27 SCR IDs, 735 integration records and 20 missing-backend contract families. All IDs remain represented; 584 historical integrations still lack a primary screen.
3. Inspected the implementation plan, its migration/evidence contract and screen-specific instructions. The original source remains unchanged.
4. Inventoried every file under `apps/web/src` with byte count, line count, SHA-256 and review indicators. The first generated inventory covered 114 files and 15,916 lines; regenerate after changes for the current total.
5. Reviewed selected complete shared modules and representative screen implementations, including App, shell, connection, styles/tokens/icons, administration, policy/security, graph rendering/events/list/source viewer and exporters. Pattern scanning helped identify additional issues; it is not a claim that every code path was executed or manually understood line by line.
6. Executed existing browser regressions, new controlled browser checks, TypeScript/unit checks and focused Python API/security tests. Inspected rendered screenshots and used actual API calls for selected integrated workflows where available.
7. Kept historical results, failed attempts and corrected test-harness problems visible. No aggregate completion percentage is inferred.

Reproduction:

```powershell
node scripts/audit_gui.mjs
node scripts/audit_gui.mjs --check
npm --prefix apps/web run typecheck
npm --prefix apps/web run test:unit
npm --prefix apps/web run build
```

Generated intake: `config/verification/gui-source-registry.json`. Every line-level intake record remains `UNTRIAGED` / `NOT_EVALUATED`. Line intake is not semantic decomposition into acceptance clauses. The generated file deliberately avoids promoting a requirement from a path, marker or automated scan.

Generated current source inventory: `test-results/gui-source-inventory.json`. It records potentially relevant storage, direct-transport, raw-HTML, discarded-error and nondeterminism locations for human investigation. A pattern match alone is not a confirmed defect.

## 3. Priority Findings

### GUI-A001: Administrative screens fabricated operational records

Severity: high. Baseline: `admin/SecurityGovernanceDashboard.jsx`, `IngestionReconciliationPanel.jsx`, `CheckpointAndRecoveryPanel.jsx`, `SchemaDriftAndFreshnessPanel.jsx`, `GraphTimelineAndJournalPanel.jsx`, `KnowledgeGovernanceAndSLOPanel.jsx`.

Security errors produced invented OPERATIONAL/FAIL_CLOSED posture and policy hierarchy. Other panels initialized or substituted invented jobs, checkpoints, dead letters, freshness values, version authors, journal facts, consumer metrics, quality scores, backup status and proposals. This could lead an operator to trust a pipeline, backup or protection that had never been observed.

Treatment: **REPAIRED / CONTAINED**. Removed fabricated records and security fallback; failures are visible. Security validates required response fields and clears the previous posture before refresh. Several broader panels still target incomplete contracts, retain legacy dark styling and need section-specific loading/empty/partial/schema-validation behavior. Showing an error is not completion of those missing services.

Required closure: actual domain contracts, correctly mapped response models, bounded reads, observation timestamps, no-data vs unavailable distinction, real positive/negative browser integration, permission filtering and restart evidence.

### GUI-A002: Token governance used an incompatible client interface

Severity: high. `admin/SecurityGovernanceDashboard.jsx` invoked `api.get` / `api.post`, although the actual application supplies a callable function. The resulting exception entered the fabricated-security fallback. Issuance also hardcoded a tenant, revocation could target a made-up identifier, and failures could still show a success result.

Treatment: **REPAIRED** for the identified UI contract. Rebuilt around the actual shared client; subject and tenant are explicit inputs; roles come from the returned matrix; issuance/verification/revocation require confirmed responses. No invented identifier or tenant fallback remains. Revocation requires an explicit identifier, reason and confirmation. Key rotation reflects the actual boolean, including false/unknown.

Residual: the backend's claimed security posture is itself a separate contract requiring validation. This screen does not certify real key rotation, global token revocation or identity-provider integration.

### GUI-A003: Policy editor dropped conditions and sent a different schema

Severity: high. `admin/RbacPolicyEditor.jsx` reconstructed policies using `sid`, `effect`, `actions`, `resources` and `roles`. The actual backend expects `policy_id`/`id`, `role`, `permission`, `conditions` and `description`. The editor omitted ABAC conditions, so a purported round trip did not preserve policy meaning.

Treatment: **REPAIRED**. `shared/api/policies.ts` emits JSON, a valid YAML subset, preserving the complete policy object. Raw YAML submission uses the shared authenticated transport. Decision rendering recognizes the backend's `allow` field. No browser-storage credential lookup is used to save.

Evidence required and exercised in focused tests: exact field/condition round trip, retained classification deny behavior and actual API loading. Full policy governance, approvals, revisions, audit and durable multi-instance publication remain open.

### GUI-A004: Saving a policy set appended obsolete grants

Severity: high. `PolicyEnforcer.load_yaml` appends statements; the GUI presented saving a whole edited set as reloading/replacing it. An old grant could remain active even after an administrator removed it from the editor.

Treatment: **REPAIRED** for explicit replacement. Added `replace_yaml`, validating the complete candidate and unique nonempty IDs before replacing the active list. The API exposes opt-in `replace_existing=true`, preserving legacy append semantics for existing callers. The editor chooses replacement. Failed validation leaves the original active set intact. Malformed policy roots/lists are rejected safely.

Residual: replacement is process-local, with no compare-and-swap revision, persisted policy version, distributed invalidation or approval workflow. These CP-03/05 and GUI-01 obligations remain release blockers for claims requiring them.

### GUI-A005: Credential persistence and stale request lifetime

Severity: high. `App.jsx` restored/stored the deployment bearer in sessionStorage. Requests had no shared disposal boundary, and disconnect did not clear all detail/job/edge state. This expanded exposure to browser scripts and risked late responses repopulating a disconnected view.

Treatment: **REPAIRED** for this deployment-access flow. The credential remains in memory; the obsolete storage key is removed without restoring it. The shared client owns AbortControllers, rejects late results even when fetch ignores cancellation, and rejects subsequent calls after disposal. Disconnect clears the loaded graph, jobs, entity/edge detail and connection appearance.

Residual: no full production OIDC/PKCE/cookie/CSRF/session renewal/revocation UI. Deployment access is labelled as such. It must not be represented as completed SCR-001 or a tenant/workspace login.

### GUI-A006: Direct fetches bypassed authentication and lifecycle handling

Severity: high. Source viewer requests and policy saving bypassed the shared request contract. The source viewer also retained the old content while loading a new file and used raw HTML rendering despite needing only text.

Treatment: **REPAIRED** for these paths. Source viewing uses the authenticated client with cancellation, drops obsolete responses, clears old content and renders source lines as text. Policy saves use the same transport with the correct content type. Direct requests elsewhere, such as existing metrics/health and legacy integrations, still need complete inventory and migration.

### GUI-A007: Event stream credentials entered URLs

Severity: high. The newly developed event hook passed the durable bearer as a WebSocket query parameter and included a sessionStorage fallback. Query credentials can appear in request logs and URL-based tooling. Cleanup could also schedule reconnect from the socket-close handler after unmount.

Treatment: **CONTAINED / PARTIAL**. Reused the existing principal-authorized event polling endpoint through the cancellable shared client. Removed URL credentials and persistent-token fallback. Polling is labelled `polling`; it does not claim a live WebSocket. Polling supports bounded buffers, sorted/deduplicated events, a retained cursor, pause/resume, cleanup, transient backoff and stopping on authorization denial or an explicit gap.

Residual: authenticated connection tickets/cookies, durable event/outbox correctness, server retention/gap contract, cross-instance ordering and complete graph-update reconciliation remain open. Global event ID jumps cannot be interpreted automatically as tenant-specific data loss. The concurrently developed journal has not been certified as a durable multi-replica log.

### GUI-A008: Unscoped browser data can cross logical boundaries

Severity: high. Notes, saved queries, bookmarks, playbooks, styles and studio artifacts are stored using global or entity-only keys. Export scanned all `kgr-note-*` keys. Workspace/tenant identity is not part of these keys; ambiguous legacy ownership cannot safely be inferred.

Treatment: **CONTAINED** for export leakage: export no longer scans browser-wide notes, and annotation export remains explicitly unavailable pending ownership verification. Existing legacy notes/bookmarks/query storage is still **OPEN**. Do not describe it as multi-tenant-safe because the bearer stayed in memory.

Required closure: principal/tenant/workspace/schema-version namespace, safe data policy, retention/purge, legacy quarantine or explicit ownership migration, real grant revocation and two-tenant identical-ID tests.

### GUI-A009: Print output inserted untrusted graph values as markup

Severity: high. `kgr/components/ExportMenu.jsx` interpolated node IDs/types/domains and annotations into HTML, then called `document.write`. The separate interactive exporter had earlier escaping fixes, but those did not cover this print path.

Treatment: **REPAIRED** for print rendering. A structured HTML document is built with DOM text nodes and table cells; values remain inert text. The opened preview is detached from its opener. Popup failure is visible. The action is labelled Print / Save as PDF, accurately identifying the browser operation.

Residual: it is not a durable server-produced PDF artifact, signed download, approval, branding or scheduled report. Those remain separate SCR-019/BACKEND-MISSING-015 work.

### GUI-A010: Graph export lost identity or produced malformed data

Severity: high/medium. GraphML used the wrong namespace, missing key declarations and raw XML interpolation. GEXF raw interpolation broke quoted/Unicode/metacharacter inputs, and edge IDs were replaced by array indices. CSV quoting did not escape embedded quotes/newlines. JSON-LD allowed arbitrary properties to overwrite structural IDs/types/endpoints.

Treatment: **REPAIRED** for identified serialization cases. Added structured XML serialization with namespaces/key or attribute definitions, stable IDs, direction and property payloads. CSV quotes fields consistently and includes edge IDs/properties. Authoritative JSON-LD identity/endpoint fields take precedence over properties.

Residual: schema qualification with independent GraphML/GEXF tools and complete format-specific round trips still required. Spreadsheet formula handling, Cypher/Mermaid identifier escaping/collision/truncation, actual Obsidian archive structure and all requested formats remain open.

### GUI-A011: Export controls promised unsupported scope and success

Severity: medium. The full/visible scope control did not alter the exported graph. Missing image/SVG methods could yield no download while the menu closed. Clipboard failure was swallowed. Radios were hidden with `display:none`, removing keyboard access.

Treatment: **REPAIRED / CONTAINED**. The menu identifies the actual loaded graph counts; unsupported full-graph claims were removed. Missing renderer methods and clipboard/popup failures produce a visible error and retain the menu. Native radio controls are visible and operable. Complete server-authorized large exports remain open.

### GUI-A012: Graph renderer does not establish advertised scale

Severity: high for performance claims. `kgr/renderers/SigmaRenderer.jsx` builds random layouts and performs synchronous pairwise force calculations. Duplicate/parallel edges can be swallowed. The separate `WebGLGraphRenderer.js` reports a fixed FPS estimate and successful draw metadata without implementing an actual rendering pipeline.

Treatment: **OPEN**. Retain useful current rendering but do not claim 10k/100k qualification, real 3D or measured 60 fps. Required next slice: maintained worker ForceAtlas2/ELK, directed multigraph identity, lifecycle-safe rendering, real frame/heap/pixel traces and supported-hardware evidence.

### GUI-A013: Multiple primary graph engines and duplicate workers

Severity: medium/high. Cytoscape and Sigma coexist with several layout implementations and independently managed state. The source explicitly chooses one primary Sigma/Graphology runtime. Removing Cytoscape before proven interaction parity would also be a regression.

Treatment: **PARTIAL**. Extracted categorical palette from the rendering module and lazy-loaded graph/feature engines. No second-engine retirement is claimed. Inventory selection/layout/export equivalents, migrate through typed adapters, then remove the redundant primary runtime and worker implementations.

### GUI-A014: Virtual list lacked keyboard behavior and correct semantics

Severity: high accessibility. Virtual rows used option roles without a proper focusable listbox or keyboard traversal. Filtering after scrolling could leave the visible slice beyond the results, creating an apparently empty list.

Treatment: **REPAIRED / PARTIAL**. Added named focusable listbox, active descendant, logical position/count, Arrow/Home/End navigation, selection/expansion, scroll-to-active and filter/sort reset. Manual NVDA/JAWS/VoiceOver evaluation and the complete graph/table/tree action parity requirement remain open.

### GUI-A015: Event rows were mouse-only buttons

Severity: medium. Event entries had button roles/tab stops but no keyboard activation. The collapsed feed toggle lacked a clear accessible name.

Treatment: **REPAIRED** for activation/naming. Enter/Space now activates the same navigation callback. The visible polling/paused/error state remains distinct from graph service health.

### GUI-A016: Navigation did not implement the requested information architecture

Severity: high scope gap. Local mode selection covered a handful of broad pages; required tenant/workspace URLs, Entity 360, Reports, Collaboration, notifications/help/about and many other screens were absent as independent integrated routes.

Treatment: **PARTIAL**. Added a shared destination registry, real navigation links, history handling, unknown-path recovery, page titles/focus and a keyboard command dialog. Prefix validation avoids treating `/administrator` as administration. The registry is a migration step, not TanStack Router or the complete 27-screen route tree. No fabricated tenant/workspace switcher was introduced.

### GUI-A017: Visual language conflicted with the requirements

Severity: medium/high. Baseline UI used marketing-style split login, violet gradients/glows, dark blue chrome, excessive rounded sections, tiny tracked labels and decorative orbs. Legacy UI tokens formed another incompatible dark/glass system.

Treatment: **PARTIAL**. Replaced connection and shell surfaces, introduced neutral/teal Evidence Atlas semantic variables, consistent 6 px controls, compact headings, accessible focus and restrained transitions. Removed the oversized search hero from the active explorer. Legacy screens still contain hardcoded dark colors, nested framing, instructional/requirement prose and inconsistent token use. The overlay compatibility stylesheet does not certify their complete redesign.

### GUI-A018: Themes and motion were incomplete

Severity: medium/high. Graph-only theme toggles and fixed CSS did not implement four product themes. Many animations had no coherent shared timing or JS/canvas reduced-motion behavior.

Treatment: **PARTIAL**. Added session-local appearance controls and shared light/dark/high-contrast variables, route motion and OS/user reduced-motion rules. Narrow layout tests cover appearance surfaces. Remaining graph/editor animations, legacy theme propagation, density modes, server preferences, white-label validation and all theme/contrast combinations remain open.

### GUI-A019: Hand-authored icons and CSS-only tooltips

Severity: medium. Many action names lacked actual icons and silently fell back to Info. Tooltip content could clip in overflow containers and lacked a semantic tooltip relationship.

Treatment: **PARTIAL**. Added exact-version Lucide registry with accessible icon-only controls, including warning/users/visibility actions. Tooltip presentation uses a positioned portal with focus/hover activation, Escape cleanup and described-by linkage. Complete domain glyph coverage, tooltip interaction timing/AT testing and extension to all legacy controls remain open.

### GUI-A020: Eager frontend bundles increased startup cost

Severity: medium. Initial build produced main JavaScript 849.56 kB / 220.09 kB gzip, alongside Cytoscape 443.04 kB / 141.98 kB gzip and CSS 108.22 kB / 21.15 kB gzip. The source's route budgets left little headroom.

Treatment: **PARTIAL improvement**. Lazy feature/graph imports reduced the first measured main JavaScript to about 311.50 kB / 92.46 kB gzip, with feature chunks loaded separately. This is a build measurement, not LCP/INP/CLS or reference-hardware graph qualification. Regenerate the manifest and record final numbers after the last source change.

### GUI-A021: TypeScript/tooling exists only for new foundations

Severity: medium. Baseline package had only dev/build scripts, no strict typing gate, general unit suite, component catalogue or comprehensive CI checks.

Treatment: **PARTIAL**. Added strict TypeScript for new transport/navigation/event/export modules, targeted Node tests, source intake/checking and focused Playwright suites. Legacy JSX remains outside strict checking. ESLint/import boundaries, Storybook, generated API client/runtime validation, broad component tests and the full release gate remain open. New TypeScript-stripping unit commands require a compatible Node runtime; CI must use the qualified version.

### GUI-A022: Browser mocks accidentally intercepted source modules

Severity: medium verification defect. Adding `src/shared/api` made the old broad `**/api/**` browser interceptors also match JavaScript module requests. They returned JSON for source modules and produced blank pages.

Treatment: **REPAIRED**. Narrowed relevant fixtures/proxy interceptors to `**/api/v1/**`. Mocked suites remain explicitly separate from real API checks. Empty/incorrect test selections, browser exceptions and intercepted real integrations must not be reported as completion evidence.

### GUI-A023: Source catalogue is not a current contract or exposure policy

Severity: high programme risk. 584 integrations are unassigned, several source screen mappings are semantically wrong, many responses are generic/unknown, aliases duplicate features and the jobs WebSocket differs from the active graph socket.

Treatment: **PARTIAL intake**. All records are retained with open contract review. Source lines remain untriaged. GUI-01 must capture current composed OpenAPI/event routes, resolve ownership and produce verified client contracts before broad screen wiring.

### GUI-A024: Tenant/workspace context is not a completed GUI boundary

Severity: high. Deployment access lacks a real current-principal/membership/workspace selection lifecycle. Admin links are present without a complete capability manifest. Independently edited backend named-graph/report scope work does not automatically scope every UI query/cache/event/export.

Treatment: **OPEN**. Keep the deployment label honest and rely on actual server authorization for existing calls. Required next: trusted principal/grants, workspace CRUD/membership, policy-aware navigation, scoped cache/draft keys, cancellation on scope switch, and same-backend two-tenant adversarial tests. Do not claim a complete platform isolation pass from this GUI batch.

### GUI-A025: Missing AI, offline, collaboration and release proof

Severity: high scope gap. No complete true answer-stream/cancel/evidence UI, durable collaboration/presence, policy-controlled offline sync, full localization, manual assistive-technology sign-off, qualified scale data or release evidence verifier is established by this work.

Treatment: **OPEN**. Follow GUI-08/10/12..16 and the 20 missing contracts. A graph event poll is not answer token streaming; a local note is not collaboration; a screenshot is not accessibility or persistence evidence.

## 4. All 27 Screens: Current Gap Matrix

| Screen | Existing implementation evidence to investigate | Current assessment | Remaining acceptance work |
|---|---|---|---|
| SCR-001 Authentication | Connection, App transport; backend signed bearer validation | PARTIAL | IdP/PKCE/MFA/session/cookie/CSRF/renew/revoke, trusted tenant/workspace grants |
| SCR-002 Onboarding | Connector wizard, studio and ingestion forms | PARTIAL, no complete onboarding route | Durable wizard, restart, review/diff/publish and real first-question journey |
| SCR-003 Overview | Explorer/admin metrics and jobs | PARTIAL | Scoped user overview, saved work, permitted counts, partial/stale aggregates |
| SCR-004 Ask | NL interpretation/agent/evidence forms, cognitive panels | PARTIAL | Real answer lifecycle, incremental SSE/cancel, clause evidence, saved answers, model/egress truth |
| SCR-005 Graph | GraphCanvas/KGR/Sigma, filters/layouts/export tools | PARTIAL | One primary engine, safe multigraph, worker layouts/LOD, scoped saved views, all interaction/a11y/performance gates |
| SCR-006 Entity 360 | Entity detail/edge inspector/source viewer | PARTIAL | Authorized aggregate, paginated relations, field masking, provenance/conflicts/history/work and canonical route |
| SCR-007 Impact | Trace/impact/blast radius views | PARTIAL | Durable proposed plans/checklists, source revision, cost/cancel, approvals, safe export |
| SCR-008 Changes | Change Lens and timeline/journal panels | PARTIAL | Real mapped journal contracts, before/after comparison, attribution, versioned deep links |
| SCR-009 Incidents | Causal dashboards and evidence traversal | PARTIAL | Durable RCA workspace, evidence-linked hypotheses/findings, concurrency and owner workflow |
| SCR-010 Time | TimelineScrubber, TemporalGraph, TimelineLens | PARTIAL | Bitemporal controls, scoped snapshots/diffs, explicit restore, reduced-motion and retention behavior |
| SCR-011 Query | Studio QueryConsole, query builders, query dashboard | PARTIAL | Uniform validate/explain/cost/profile/cancel, qualified dialects, scoped durable templates/history/results |
| SCR-012 Ontology | Studio SchemaCanvas, mappings and metadata tools | PARTIAL | Governed versioned draft/review/migration/publish/rollback with accessible editing |
| SCR-013 Meta-graph | Ontology/metadata graph views | PARTIAL | Clear schema/data distinction, authorized counts, instance drill-down, read-only vs draft boundary |
| SCR-014 Sources | Registry/setup/catalogue forms and real source operations | PARTIAL | Uniform connector capability contracts, credentials, safe schedules, durable tests/errors and scope |
| SCR-015 Ingestion | JSON/file forms, mapping/pipeline studio | PARTIAL | Resumable/scan/checksum upload, inferred graph review, version-bound dry-run/publish, partial errors |
| SCR-016 Quality | Validation, identity/similarity tools and quality panels | PARTIAL | Real candidate merge/split/undo, impact/provenance preservation, steward queue and bulk results |
| SCR-017 Jobs | Admin jobs, recovery panels, pipeline tools | PARTIAL | Unified durable lifecycle/events, exact cancel/retry semantics, logs, checkpoints, worker/API restart |
| SCR-018 Agents | AgentView/CognitiveHub and proposals/run APIs | PARTIAL | Exact approval binding, real tool traces, cancellation/resume, denial/replay/no-egress evidence |
| SCR-019 Reports | Graph report/print/export controls; backend render/download services | PARTIAL, no full report screen | Durable library/editor/approval, real schedule execution, all document formats, scoped downloads and expiry |
| SCR-020 Collaboration | Local annotations/bookmarks | OPEN for required integrated workflow | Authenticated workspace comments/presence/mentions/sharing, durable conflicts; optional CRDT decision |
| SCR-021 Governance | User/role/policy/security administration | PARTIAL, concrete policy/token repairs | Capability discovery, field/classification/egress policy, version/approval, durable audit and revoke propagation |
| SCR-022 Tenant admin | Backend tenancy/licensing/quota APIs | OPEN for complete GUI | Tenant lifecycle/placement/workspaces/usage/backup operations with real permissions and recovery |
| SCR-023 White-label | Backend brand registries; shared visual variables | OPEN for brand studio | Asset safety, versioned preview/contrast/layout, atomic publish/rollback and cache propagation |
| SCR-024 Health | Admin dashboard/live ops, metrics | PARTIAL | Qualified real service/node/store/model/queue telemetry, stale/partial data and privileged recovery |
| SCR-025 Settings | New session appearance surface | PARTIAL | Server profile/preferences, density, locale/time zone, shortcuts, notifications and conflict handling |
| SCR-026 Notifications/help/about | Backend inbox/licensing and static notices | OPEN for full surfaces | Authorized inbox/read sync, help/shortcuts, exact shipped notices/SBOM and offline access |
| SCR-027 Errors | Connection alerts, inline errors, route boundary/not-found | PARTIAL | Consistent 401/403/offline/version/chunk/WebGL recovery and safe draft restoration |

No row is marked complete solely because a similarly named component exists.

## 5. Shared Requirement Coverage

| Source area | Implemented or improved | Material gaps |
|---|---|---|
| Product/task architecture | Compact shell and real navigation, preserved existing workflows | Full tenant/workspace object model, approved user-task research and all required routes |
| Technology/modules | Incremental strict TS, lazy modules, shared transport/icons | Typed router/server cache/state ownership, import boundaries, removal of duplicate engines |
| Design tokens/graphics | Evidence Atlas compatibility variables, 4 theme choices, semantic palette | Full token conversion, legacy component theming, charts/visual assets and white-label qualification |
| Motion | Bounded route animation and OS/user reduce rules | Graph/editor/timeline JS motion, interruption/reduced-motion parity and animation budgets |
| Responsive fit | Narrow appearance/shell checks | All screen states/densities, tablet inspectors, 4K/ultrawide, 400% reflow and long localization |
| Components/forms | Improved labels, errors, native radio/listbox/dialog behavior | Full family/state library, runtime domain schemas, draft policies, server-pointer errors |
| Graph | Real graph views and selected accessibility/export repairs | Worker/runtime parity, stable identity/camera, every layout, scalable LOD and independent format checks |
| AI UX | Existing query/evidence forms | True answer stream/cancel, calibrated uncertainty, retrieval evidence and verified provider semantics |
| Resilience | Request disposal, honest failures, event cleanup | Version conflicts, durable jobs/outbox, all retry/deadline/partial/recovery semantics |
| Accessibility | Focus/skip links/tooltips, native controls, keyboard virtual list | Full AA criteria, all legacy controls, manual NVDA/JAWS/VoiceOver and equivalence reviews |
| Localization | No full implementation claimed | ICU extraction, translated resources, RTL/font/formatting, locale preference and pseudo-expansion |
| Security/tenancy | Memory credential, no URL bearer in repaired event path, safe text printing | Production sessions/grants, complete resource/field isolation and scoped local data migration |
| Performance | Reduced eager main bundle | LCP/INP/CLS, 10k/100k measured workloads, memory/GPU/worker qualification |
| Telemetry | Correlation IDs on shared requests | Privacy-approved local collector, schema/retention/kill switch, operational metric correctness |
| Quality/delivery | Structural source intake and focused behavioral tests | Semantic acceptance ledger, CI full matrix, source/build/runtime browser receipts and manual gates |

## 6. Verification Record

Historical completed checks from the initial foundation slice:

- Baseline build: main JavaScript 220.09 kB gzip; CSS 21.15 kB gzip; Cytoscape 141.98 kB gzip.
- Foundation build after lazy loading: main JavaScript 92.46 kB gzip; graph/editor/admin/cognitive screens split into separate chunks. Later source changes require a new measurement.
- Node foundation/intake tests: 14 passed initially; event reducer checks increased the targeted suite to 16 passing checks.
- Controlled foundation Playwright suite: 8 passed, covering credential lifetime, command dialog/history/focus, four themes at 1440/390/320, reduced motion, unknown route, honest admin failures and rejected revocation.
- Existing selected Playwright regressions: 9 passed, including the search/trace/admin workflow, invalid credentials, guided demo cases and interactive-export injection checks. These fixtures are not real service qualification.
- Focused Python policy/authz/HTTP/realtime suite: 50 passed, 0 failed/skipped in the recorded foundation run. XML: `test-results/gui-policy-regression.xml`; source receipt: `test-results/gui-policy-receipt.json`. Concurrent later backend changes make that receipt historical until rerun.

Failed attempts retained for diagnostic transparency:

1. A TypeScript parameter property failed Node's strip-only mode. Replaced with explicit class fields; targeted tests passed afterward.
2. Broad browser mocks returned JSON for JS modules. Narrowed patterns and reran the regressions successfully.
3. Native dialog close restored focus after route focus. Added deliberate post-close heading focus and reran the foundation tests successfully.
4. New export tests initially used the wrong expected representation for a JSON-valued CSV cell; corrected the assertion to check the actual identifier escaping.
5. A component fixture imported an optimized CJS dependency as a named ESM export. Moved React/createRoot wiring into the fixture's normal Vite module imports. This is a test fixture repair, not a production browser integration pass.
6. Real API/browser and new graph checks were still under active verification while this report was written. Final status is recorded below; do not infer a pass from the presence of their files or screenshots.

### Final Validation Addendum

Additional completed checks after the foundation slice:

- TypeScript checks passed for the new typed transport/navigation/event/export modules.
- Final production build passed: main JavaScript 312.50 kB / 92.79 kB gzip, CSS 107.97 kB / 21.51 kB gzip, separately loaded graph explorer 321.43 kB / 80.99 kB gzip and Cytoscape 443.04 kB / 141.98 kB gzip. These are emitted asset sizes, not measured loading, interaction or scale budgets.
- Node suite: 16 passed, including event sorting/deduplication/bounding and malformed event rejection.
- Real API browser suite: 2 passed, with actual token issuance/verification/revocation, policy replacement/read-back/restoration, authenticated event polling, header-only credentials and navigation cleanup. This used the real composed FastAPI app with an isolated in-memory graph and file-backed ancillary state; it does not qualify production graph persistence or a commercial deployment profile.
- Browser graph/component checks: 3 passed, including XML parse/identity/direction/property assertions with hostile Unicode/metacharacters, inert print output, CSV identifier quoting, virtual-list keyboard/filter behavior and event cleanup.
- Automated axe checks: 2 passed across connection, four appearance themes and the command dialog, with zero serious/critical findings in those tested surfaces. Other screens and manual assistive technology remain unqualified.
- Inspected representative mobile appearance and real security screenshots. The new surfaces render coherently, while existing administration still contains legacy metrics/tab framing and typography; a global redesign pass remains incomplete.
- Source registry check passed with 1,395 source lines, 1,258 intake units, 27 screens, 735 integrations and 20 missing contracts. The current inventory at that check covered 116 frontend source files and 15,957 lines. These are structural counts, not passed feature counts.

For the final source-bound execution use `test-results/gui-final-browser-receipt.json` and `test-results/gui-final-python-receipt.json`, with their required browser JSON and Python JUnit artifacts. Their recorded status, exit code, freshness, source fingerprints, selected tests and limitations are authoritative for that execution. A missing or FAIL receipt is not a passing check. The working tree contains independently developed backend changes; dirty-tree evidence is content-bound rather than an immutable commit release certificate.

Final combined execution results: **24 browser tests passed, 0 failed, 0 skipped**, and **51 Python tests passed, 0 failed/errors/skipped**. Both required result artifacts were fresh. However, **both evidence receipts are FAIL**, because source files changed during execution: the browser snapshot detected `apps/api/main.py`, `tests/unit/test_job_queue_tenancy.py` and `tests/unit/test_reports.py`; the Python snapshot detected `tests/unit/test_job_queue_tenancy.py`. These concurrent edits were preserved. The passing test processes therefore do not establish stable-source acceptance for the final tree. Repeat affected checks on a stable revision and a freshly started API before any release claim.

The repository-wide whitespace check also reports trailing blank lines in concurrently edited report/event/security test files. No unrelated formatting edits were applied to those files as part of this GUI batch.

The browser real-API suite uses a temporary credential supplied through `EOIP_GUI_TEST_TOKEN`. Traces from failed diagnostic attempts can contain fixture credentials and must remain in restricted, ignored test output. The final real-API test attachment records only paths/statuses; screenshots mask issued tokens. No 100% completion, production profile acceptance or manual accessibility approval is asserted.

### Verification Harness and CI Changes

CI now selects Node 22.18.0 for the browser build job, runs strict checking, targeted Node tests and source-intake validation, and runs the self-contained foundation/graph/accessibility/export browser suites with retained JSON output. These checks complement the existing Python security gates. They do not run or claim the entire mandatory GUI release matrix.

The new runtime Lucide dependency has its package-supplied license preserved under the web public legal assets. The axe Playwright package is development tooling, with its actual MPL-2.0 metadata recorded in the preliminary notice inventory. Full dependency clearance and artifact notices remain governed by the existing release checklist.

## 7. Next Ordered Implementation Work

1. Rerun the completed narrow checks on a stable source revision and a freshly started runtime, retaining passing source-bound receipts. Screenshot inspection and successful test processes do not replace this step.
2. Complete GUI-00 semantic clause triage and decisions; structural intake alone is insufficient. Assign the 584 unmapped operations and fix the source screen mapping errors.
3. Implement the trusted principal, session and workspace contracts before introducing tenant-aware UI caches or pretending a deployment bearer is a production login.
4. Finish the single maintained worker-based graph runtime and tested graph/table/tree parity; qualify real data identity, camera lifecycle and 1k/10k/100k workloads.
5. Deliver one persistent end-to-end graph -> entity -> evidence -> saved view -> authorized export journey against a real qualified backend.
6. Follow with complete onboarding/ingestion review/publish, true answer streaming/cancel and governed investigation/query/report workflows.
7. Replace remaining legacy hardcoded styles and global browser storage by scoped modules with approved migrations. Complete localization, manual AT, usability and deployment/profile qualification.

## 8. Reproduction and Handoff

Use a dedicated temporary data directory and the explicit in-memory graph profile for local GUI contract checks. This profile proves selected API/UI behavior, not production graph persistence, HA or commercial scale. Never run mutating test fixtures against customer data.

The frontend supports `EOIP_DEV_API_URL` for local Vite proxying. The source requirements and complete implementation plan retain the authoritative feature scope. This follow-up records concrete findings, bounded repairs and remaining acceptance work. Preserve independently developed working-tree changes; do not roll them back to reproduce the old audit baseline.

Local source and test references can be stale after concurrent edits. Regenerate the inventory and rerun affected checks before promoting any clause or shipping an artifact.
