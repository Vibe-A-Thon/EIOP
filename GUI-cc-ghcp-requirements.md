# EOIP / KnowGridFlow — GUI Requirements for Coding Agents (GUI-cc-ghcp)

**Document ID:** GUI-CC-GHCP-REQ · **Version:** 1.0.0 · **Date:** 2026-10-16 · **Status:** Build specification (normative) · **Audience:** autonomous coding agents (GitHub Copilot, Claude Code, equivalent) and their human reviewers.

**Supersedes for GUI purposes:** `GUI-UIX-requirements.md` v1.0.0 (2026-10-13) and the screen sections of `GUI-UIX-implementation-plan.md`. Both remain historical references; where they conflict with this document, **this document wins**. The 735 `INT-*` identifiers and 20 `BACKEND-MISSING-*` identifiers defined there are reused unchanged so traceability is preserved.

**Source basis:** every Markdown file in the repository was read (231 files: root specs, `EOIP-engg-doc-pkg/**`, `docs/**`, `demo/**`, `licenses/**`, `apps/vscode-extension/README.md`), plus direct inspection of the live backend code (`apps/api/main.py`, `apps/api/app.py`, `apps/api/extended.py`, `packages/eoip/**/router.py`, `packages/eoip/jobs.py`, `packages/eoip/tenancy/*`, `packages/eoip/graph/{metrics,lens}.py`, `packages/eoip/ontology/manifest.py`) and the captured OpenAPI 3.1 snapshot (`.audit-scratch/openapi.json`, 689 paths / 303 schemas, captured 2026-10-13). Every endpoint, header, status code, field name, enum value and limit in this document was confirmed from that code or snapshot. Where a contract does **not** exist, it is labelled `BACKEND-MISSING-*` or `GUI-BE-*` and the exact fallback behaviour the GUI must implement is stated. No endpoint, field or behaviour in this document is assumed.

---

## 0. How to Use This Document (Read First)

### 0.1 Purpose

Replace the existing `apps/web` GUI — which is visually inconsistent (violet/glass/dark-marketing styling, nested cards, instruction prose in chrome, hand-drawn icons, two competing graph engines, fabricated admin values, no tenant/workspace routes) — with a **calm, modular, evidence-first enterprise workbench** that is:

1. **100 % integrated with the real API** described in §3 (no mock data in production paths; `BACKEND-MISSING-*` surfaces are explicitly labelled and disabled, never faked).
2. **Low complexity for users**: one primary action per surface, progressive disclosure (`Simple` → `Advanced` → `Expert`), ≤ 2 clicks to any authorized primary destination, every state visible, every action reversible or confirmed with impact preview.
3. **High craft**: a single design-token system (four themes), one icon family (Lucide), bounded purposeful motion, a single WebGL graph engine with accessible table/tree equivalents, WCAG 2.2 AA.
4. **Modular**: feature modules with public interfaces only; screens composed from the shared component library; within-screen regions (toolbar / work surface / inspector / dock) are independently loadable, failable and testable.

### 0.2 Reading order for an implementing agent

1. §0.3 Non-negotiable rules and §0.4 Definition of Done / evidence rules.
2. §2 Resolved vocabularies (use these strings verbatim).
3. §3 Verified backend contract (use these endpoints/fields verbatim).
4. §4 Stack and project structure (binding).
5. §5 Design system → §6 Shell → §7 Components → §8 Shared patterns.
6. §9 Screens in the milestone order of §15.
7. §10–§13 cross-cutting specs (graph, AI/NL, VS Code, a11y/i18n/security/perf/telemetry).
8. §14 Testing and evidence; produce the handoff record in §14.8 after every slice.

### 0.3 Non-negotiable rules (apply to every line of code)

| # | Rule | Source |
|---|---|---|
| R1 | **Never fabricate.** No hardcoded domain answers, KPIs, health values, job records, confidence scores, citations or success states. Unknown is rendered as `Unknown`/`N/A`/`Not available`, never `0`, `0 %`, `100 %` or a green badge. | FR-ADMIN-002, FR-VALID-003, MVP-FR-016/018, SR-UX-001, G2 §39, roles.md |
| R2 | **Backend truth only.** If an endpoint is missing (`BACKEND-MISSING-*`) the control is rendered disabled with the reason `Not available in this deployment` and the contract ID in a tooltip; it is never satisfied by a mock in a production build. MSW is allowed only in Storybook/tests and must fail the production build if referenced. | GUI-UIX §9, plan §1.2 |
| R3 | **Route ≠ authorization.** `/admin`, `/platform`, `/t/:tenant` URL separation is navigation only. Every request relies on server authorization (401/403). Hidden navigation is a courtesy, not a boundary. | NFR-SEC-005, 06-architecture D10, super-req C3 |
| R4 | **Deterministic vs generated is always visible.** Every answer, edge and metric carries a visible class badge (§2.4/§2.5) and a knowledge-age stamp. Inferred facts never render as unqualified truth. Abstentions render as abstentions. | glossary, SR-NLQ-004, SR-ING-051, KGR-G-019 |
| R5 | **No credentials in URLs, storage or logs.** Bearer token lives in memory only (existing `createApiClient`). WebSocket auth uses the `Authorization` header or a one-use ticket when available; the `?token=` query form is forbidden in the GUI even though the server accepts it. Never `localStorage`/`sessionStorage`/IndexedDB for tokens. | GUI-A005/A007, OPEN-06, CP-08 |
| R6 | **Tenant and workspace are always visible and always scoped.** Every query key, cache entry, draft, saved view, subscription and export is namespaced `{tenant, workspace}`; switching scope aborts in-flight work, clears caches and resubscribes. | GUI-A008/A024, KGR-G-013, SR-TEN-* |
| R7 | **No `innerHTML`/`document.write` with untrusted values.** Graph values, AI text, source text and tenant brand assets render as text or through a sanitizer allow-list; CSP with nonces; Trusted Types where supported. | GUI-A009, CP-08, SR-SEC-016 |
| R8 | **Private chain-of-thought is never requested, stored or displayed.** Show evidence, rules fired, tool-call digests, confidence inputs. | 41-xai, deep-agents-xai, GAP-AGOV-010 |
| R9 | **Three numbers, never one percentage.** Any completion/health/progress dashboard shows component dimensions separately (tests passing · behavioural evidence · external-gate evidence; or Freshness · Coverage · Consistency · Completeness · Accuracy). A single opaque score is prohibited. | SR-QA-012, GAP-KQ-004, G2-KD-004, knowgridflow §38 |
| R10 | **Code and test file references are not proof.** A requirement is complete only when the evidence bundle in §14.6 exists for the exact build. | plan §1.2, audit §1 |
| R11 | **Destructive actions preview impact, then confirm, then allow undo/restore where the backend supports it.** Typed confirmation only for high-impact actions (delete entity, restore snapshot, replace policy set, publish brand, delete source with jobs). | SR-UX-011, §11 of GUI-UIX |
| R12 | **Local-first and offline-truthful.** No external fonts, CDNs, analytics or model calls. Offline/degraded states state the capture age and disable unsafe mutations. The product remains useful with the model stopped. | NFR-SEC-001, 06-architecture D9, NFR-KGR-004/005 |
| R13 | **One graph engine.** Sigma + Graphology is the only primary renderer. Cytoscape is removed when parity evidence (§10.12) passes, never before and never kept as a second runtime. | GUI-UIX §3, GUI-A013 |
| R14 | **No instruction prose, marketing panels, decorative orbs/glass/gradients, nested cards, or cards-as-sections in application chrome.** Help lives in `/help`. | GUI-UIX §8, GUI-A017 |
| R15 | **Progressive disclosure, never feature dumping.** 27 destinations are grouped (§6.2); the rail shows ≤ 7 primary groups; advanced controls appear in `Advanced`/`Expert` mode or in context menus. | plan §6, knowgridflow §38 |

### 0.4 What "complete" means (Definition of Done)

A screen, component or contract is **COMPLETE** only when all of the following hold for the exact release-candidate build hash:

1. Every acceptance criterion (AC) in its section passes in an automated test that names the AC ID and asserts the business outcome (not just rendering).
2. Real-API Playwright journey(s) listed for it pass against a freshly started `apps.api.main:create_app` with an isolated data directory (no route interception in the `real` project).
3. All states in §8.1 are implemented and screenshot-captured (light, dark, HC-light, HC-dark × populated/empty/loading/error/denied/stale/offline).
4. axe: zero serious/critical; manual keyboard transcript recorded; screen-reader transcript recorded (NVDA+Chrome minimum) for the primary journey.
5. Bundle, LCP/INP/CLS and graph frame budgets (§13.4) measured and within limits on the declared reference hardware.
6. Strings externalized (ICU), no hardcoded English in components; pseudo-locale run passes layout checks.
7. No `BACKEND-MISSING-*` dependency is satisfied by a mock; each is visibly disabled with reason.
8. Evidence bundle (§14.6) written under `test-results/gui/<run-id>/` with manifest, receipts, screenshots, traces; verifier passes.
9. Handoff record (§14.8) produced; "complete" is stated per AC, never as an aggregate percentage.

Status vocabulary for tracking (use exactly): `UNTRIAGED → SPECIFIED → IMPLEMENTING → IMPLEMENTED_UNVERIFIED → BEHAVIOR_VERIFIED → INTEGRATION_VERIFIED → RELEASE_ACCEPTED`; plus `BLOCKED_DECISION`, `BLOCKED_BACKEND`, `FAILED`, `STALE_EVIDENCE`, `APPROVED_NOT_APPLICABLE`.

### 0.5 Requirement ID scheme used here

- `GUI-SCR-nnn-Axx` — screen acceptance criterion (e.g. `GUI-SCR-005-A03`).
- `GUI-SHELL-nn`, `GUI-DS-nn`, `GUI-COMP-nn`, `GUI-GRAPH-nn`, `GUI-AI-nn`, `GUI-A11Y-nn`, `GUI-I18N-nn`, `GUI-SEC-nn`, `GUI-PERF-nn`, `GUI-TEL-nn`, `GUI-TEST-nn`, `GUI-VSC-nn` — cross-cutting criteria.
- `INT-nnn` — existing integration record IDs (unchanged from `GUI-UIX-requirements.md` §17).
- `BACKEND-MISSING-nnn` — existing missing-contract IDs; `GUI-BE-021..028` from the implementation plan; `GUI-BE-029+` new in this document.
- `DEC-GUI-nn` — decisions this document makes binding for the GUI (owner may override via ADR; until then they are law for the agent).

---

## 1. Product Definition, Personas and Journeys

### 1.1 What the product is

EOIP (product/UI name **KnowGridFlow** per `knowgridflow-product-architecture.md` §1.2; white-label tenants may rename it — see §5.9) is a **local-first, multi-tenant, evidence-first enterprise ontology and knowledge-graph workbench**. It answers three primary questions (01-project-vision):

1. **What implements this requirement?** (traceability)
2. **What changes if this symbol/service/entity changes?** (impact)
3. **Why do we believe this relationship exists?** (evidence/provenance)

…and the extended operator set `WHY · WHY NOT · WHAT IF · WHAT CHANGED · WHEN · WHO · WHERE · HOW` (G2-QOP-001..009), each returning structured results plus evidence, never prose alone.

The graph is the primary work surface; every answer is evidence-linked; deterministic and generative computation are visibly distinct; tenant context is always visible; dense information stays calm.

### 1.2 Personas (consolidated — use these six labels in the UI; map the eleven super-req personas onto them)

| UI persona label | Covers (super-requirements §1.1) | Home surface (`SR-UX-006`) | Primary screens |
|---|---|---|---|
| **Executive** | Executive/business leader | Overview (executive layout) | SCR-003, SCR-004 Ask, SCR-019 Reports |
| **Architect** | Enterprise/solution architect, Data steward/ontologist (ontology part) | Overview (architect layout) | SCR-005 Graph, SCR-007 Impact, SCR-012 Ontology, SCR-013 Meta-graph, SCR-008 Changes |
| **Engineer** | Engineer/SRE/DevOps, Integrator/developer | Overview (engineer layout) | SCR-005, SCR-006 Entity, SCR-007, SCR-009 Incidents, SCR-011 Query, VS Code |
| **Steward** | Data steward/ontologist (data part), Analyst/operations manager | Overview (steward layout) | SCR-014 Sources, SCR-015 Ingestion, SCR-016 Quality, SCR-012 |
| **Auditor** | Auditor, Security & compliance officer | Overview (auditor layout, read-only emphasis) | SCR-008, SCR-021 Governance, SCR-019 |
| **Admin** | Tenant administrator, Platform operator/partner/reseller | Overview (admin layout) | SCR-017 Jobs, SCR-021, SCR-022 Tenant, SCR-023 Brand, SCR-024 Health |

`AI agent` (super-req persona 11) is served by the API/MCP, not the GUI; the GUI shows agent activity in SCR-018.

Persona is **not** a permission. It only selects the default Overview layout and default rail ordering (§6.2). The server decides access.

### 1.3 Primary journeys (each must be a real-API Playwright journey — §14.3)

| JRN | Journey | Screens |
|---|---|---|
| JRN-01 | Sign in → choose tenant/workspace → deep-link refresh → switch scope → sign out | SCR-001, shell |
| JRN-02 | Connect source → test → baseline/ingest → review inferred graph (dry-run) → publish → first question | SCR-002, 014, 015, 017, 004 |
| JRN-03 | Search → expand → filter → inspect entity → provenance → save view → restart → restore → authorized export | SCR-005, 006 |
| JRN-04 | Ask → suggestion cards (QueryPlan preview + cost) → run → streamed/narrated answer → hover citations → stop/regenerate → save/report | SCR-004, 019 |
| JRN-05 | Select entity → blast radius (hop/severity) → paths → owners/tests checklist → export plan | SCR-007 |
| JRN-06 | Incident → ranked hypotheses → evidence traversal → record finding | SCR-009 |
| JRN-07 | Ontology draft → validate → diff/impact → review → publish → rollback | SCR-012, 013 |
| JRN-08 | Upload (interrupted) → resume → mapping conflict → job retry → verified graph | SCR-015, 017 |
| JRN-09 | Duplicate candidates → compare → decide (accept/reject) → undo/revert where supported | SCR-016, 006 |
| JRN-10 | Query validate/explain/run → cancel/timeout → save template → paged/exported result | SCR-011 |
| JRN-11 | Agent run → scoped approval → denied/replayed action → audited result | SCR-018 |
| JRN-12 | Report template → params → render → schedule → download/revoke | SCR-019 |
| JRN-13 | Two browsers → presence/comments → disconnect/rejoin → membership revoked (blocked until `BACKEND-MISSING-016`) | SCR-020 |
| JRN-14 | Governance policy edit (replace) → evaluate → denied egress → revoke token | SCR-021 |
| JRN-15 | Tenant quotas/placement → suspend/resume → backup/restore view | SCR-022 |
| JRN-16 | Brand draft → contrast failure → fix → preview all 4 themes → publish → rollback (publish blocked until `BACKEND-MISSING-018`) | SCR-023 |
| JRN-17 | Settings (theme/density/locale/motion) → notifications → help → about/licences | SCR-025, 026 |
| JRN-18 | Induced 401/403/404/offline/version-mismatch/chunk-failure → safe recovery with retained draft | SCR-027 |

### 1.4 Question taxonomy the UI must make discoverable (super-req §1.2)

Lookup · Traversal · Paths · Impact/blast radius · Root cause · Ownership/expertise · Change history · Coverage/gap · Comparison · Temporal/as-of · What-if · Aggregation · Similarity/recommendation · Policy/compliance · Summarization/report · Explain-why. The command palette (§6.6) and Ask suggestion cards (§11.2) expose these as typed intents mapped to the endpoints in §3.

---

## 2. Resolved Vocabularies (Single Source of Truth for UI Strings and Enums)

The corpus contains 23 vocabulary conflicts (listed in Appendix F). The GUI uses **exactly** the following. Where the backend emits a different legacy value, the mapping column applies; the GUI never invents a value absent from the backend.

### 2.1 Job / run status (`DEC-GUI-01`)

Backend (`packages/eoip/jobs.py`) emits: `PENDING`, `RUNNING`, `HELD`, `SUCCEEDED`, `PARTIAL`, `FAILED`, `CANCELLED`. IngestionRun vertices may carry `run_status` ∈ `PENDING|RUNNING|DONE|FAILED` (reference/ingestion.md) — map `DONE → SUCCEEDED` for display only, show raw value in the Raw tab.

| Status | Label (en) | Semantic colour token | Icon (Lucide) | Allowed actions (server-enforced) |
|---|---|---|---|---|
| `PENDING` | Queued | `status.neutral` | `clock` | Cancel (`POST /api/v1/admin/jobs/{id}/cancel` → 200) |
| `RUNNING` | Running | `status.info` | `loader-circle` (spins; static in reduced motion) | none — cancel returns **409** ("Running jobs cannot be cancelled safely"); show tooltip with that reason |
| `HELD` | Held — needs operator | `status.warning` | `pause-circle` | Re-admit (`…/readmit` → 202; 409 if not HELD), Cancel |
| `SUCCEEDED` | Succeeded | `status.success` | `circle-check` | View result |
| `PARTIAL` | Partial — some records rejected | `status.warning` | `triangle-alert` | View rejected/DLQ |
| `FAILED` | Failed | `status.danger` | `circle-x` | View error, Replay (where kind supports) |
| `CANCELLED` | Cancelled | `status.neutral` | `ban` | none |

Never display `QUEUED`, `DONE` or `COMPLETE` to users.

### 2.2 Entity/edge creation status and fact class (`DEC-GUI-02`)

Backend field: `GraphEdge.creation_status` (string|null) and vertex property `creation_status`; observed values `DETERMINISTIC`, `INFERRED`, `HUMAN_CONFIRMED`, and in KGR contracts `AMBIGUOUS`, `MANUAL`. Super-requirements use `ASSERTED/DERIVED/INFERRED/CURATED`; gaps-requirements use `asserted/inferred/model-generated/human-confirmed`.

| Display class | Backend values mapped | Edge style | Badge colour | Badge icon |
|---|---|---|---|---|
| **Deterministic** | `DETERMINISTIC`, `ASSERTED`, `asserted` | solid 1.5 px | `fact.deterministic` (#16805A light / #4BC38B dark) | `badge-check` |
| **Derived** | `DERIVED` | solid 1.5 px, 70 % alpha | `fact.derived` (#1769AA / #67B7F7) | `function-square` |
| **Inferred** | `INFERRED`, `inferred`, `model-generated` | dashed 4-3, confidence drives alpha .4–.9 | `fact.inferred` (#A15C00 / #FFC857) | `sparkles` |
| **Ambiguous** | `AMBIGUOUS` | dotted 1-3 | `fact.ambiguous` (#C33241 / #FF6673 at 80 %) | `circle-help` |
| **Human-confirmed** | `HUMAN_CONFIRMED`, `MANUAL`, `CURATED`, `human-confirmed` | solid 2 px with 1 px inner halo | `fact.human` (#006D77 / #43C3CC) | `user-check` |
| **Unknown** | `null`, missing | solid 1 px grey | `text.muted` | `circle-dashed` |

Every graph legend, inspector, answer sentence and export shows this class. Filters offer these six display classes (`GUI-GRAPH-07`).

### 2.3 Trust state (`DEC-GUI-03`)

Vertex property `trust_state` (audit-coverage-ledger; search hit `trust_state` default `unverified`). Display ordered ladder: `Raw → Parsed → Inferred → Reviewed → Trusted → Certified`, plus terminal `Rejected` and `Quarantined` (property `quarantine=true`). Lower-case backend values (`unverified`) map to `Raw`. Trust renders as a 7-segment mini ladder icon (`TrustLadder`, COMP-07) with the active segment filled; never as a percentage. Queries may set a minimum trust (`GAP-TRUST-004`) via the filter builder.

### 2.4 Answer mode badge (`DEC-GUI-04`, SR-NLQ-004)

Every Ask/Query/Agent result shows exactly one mode badge: **Deterministic** (graph query result, `engine` ≠ model), **Narrated** (model text grounded on a deterministic result), **Exploratory** (agent investigation), **Report** (rendered report), **Simulated** (development simulator / `Self-LLM` — label literally `Simulated (not model inference)` per audit CONFLICT-006), **Abstained** (`abstain=true` or `partial=true` with no answer). Badge is adjacent to the answer title; never inside the answer text.

### 2.5 Boundary badge (`DEC-GUI-05`, SR-LLM-*)

Persistent badge in the Ask composer and Agents screen: `Local only` (default; `GET /api/v1/egress/endpoints` returns no enabled endpoints or egress policy denies) or `Approved external: <endpoint name>` with the classification/sharing level `S0..S7` and a link to the redaction preview (`SR-LLM-012`). If `GET /api/v1/egress/endpoints` fails → badge reads `Egress status unknown` in warning colour and generation controls stay enabled only for local providers.

### 2.6 Risk tiers and human-control loops (`DEC-GUI-06`)

Risk tiers (KGR-G-007, agents.md): `R0 Auto · R1 Peer · R2 Lead · R3 CAB · R4 Executive`. Display as `R2 · Lead approval`. Any mutation proposal with risk ≥ R2 shows `Blocked until approved` until an approval record exists.

Loop labels use the **65-glossary expansions** (first table of KGR-g §7f), not the second "Tier 1" list: HCTL Human-Commanded-the-Loop · HITL-FE Human-in-the-Loop-for-Exceptions · HBTL Human-Beside-the-Loop · HATL Human-Above-the-Loop · HITD Human-in-the-Design · EITL Environment-in-the-Loop · HITL Human-in-the-Loop · HOTL Human-on-the-Loop · HOOTL Human-out-of-the-Loop (read-only; prohibited R3/R4) · HITA Human-in-the-Action · HITC Human-in-the-Control-Loop · HITI Human-in-the-Institution · MITL Machine-in-the-Loop · HITP Human-in-the-Process. The UI shows the acronym with the expansion in a tooltip and the footnote `Platform-defined policy vocabulary` (roles.md). `BrainAskRequest.loop` default is `HITL-FE`.

### 2.7 Severity, risk and policy decisions

- Validation finding severity: `INFO · WARN · ERROR · BLOCKER` (SR-ING-050); colours info/warning/danger/danger-with-`octagon-alert` icon.
- Blast-radius risk: `NONE · LOW · MEDIUM · HIGH · CRITICAL` → `color.text.muted (neutral) / #2A9D8F / #E9C46A / #F4A261 / #C33241` + ring count 0–4 around the node (redundant encoding).
- Policy decision (knowgridflow §17.2): `ALLOW · DENY · REQUIRE_APPROVAL · REDACT` with `reason_codes[]` listed verbatim.
- Human-control outcome: `approve · reject · timeout` (diagram 13).
- Tool risk class: `read · write · destructive` (GAP-AGOV-002).
- Causal relation: `CORRELATED_WITH · POSSIBLY_CAUSED · EVIDENCE_SUPPORTS_CAUSE · HUMAN_CONFIRMED_CAUSE`; never promote a lower class to a higher one client-side (G2-CAUSE-003).
- Schema drift class: `additive · compatible · potentially breaking · breaking`.
- Source health: `UNKNOWN · HEALTHY · DEGRADED · UNAVAILABLE · MISCONFIGURED`; webhook status `UNCONFIGURED · CONFIGURED · ACTIVE · DISABLED · FAILING`.
- Catalog/knowledge-product state: show the backend `state` string verbatim (`Draft · Candidate/Experimental · Trusted · Certified · Deprecated · Quarantined`) with the footnote `Certified is an application lifecycle state, not external certification` (demo README).
- Impact categories (GAP-CHANGE-004): `direct · transitive · runtime · data · API · documentation · compliance · ownership`.
- Knowledge-debt categories (G2-KD-002, 12): unowned component · undocumented API · unlinked requirement · unlinked implementation · stale document · unresolved identity · broken provenance · low-confidence critical inference · missing test · missing architecture mapping · unknown production owner · stale runbook.
- Health dimensions (MS-24): `Freshness · Coverage · Consistency · Completeness · Accuracy` — five separate gauges, never one.

### 2.8 Lenses (`DEC-GUI-07`)

The canonical lens list is the backend `GET /api/v1/lens/catalog` (20 ids): `search, graph, evidence, impact, timeline, change, architecture, runtime, requirement, trust, security, release, process, knowledge_health, simulation, agent, decision, api, test, ontology`. A lens is a **task-specific encoding/filter over the same graph context**, not a separate application (knowgridflow §23 "The user changes lens, not application context"). Lenses are exposed as the **Lens switcher** inside Graph Explorer (SCR-005) and as default lenses of the investigation screens (Impact → `impact`, Changes → `change`, Incidents → `runtime`+`evidence`, Time → `timeline`, Quality → `knowledge_health`+`trust`, Ontology/Meta-graph → `ontology`). Lens availability is read from the catalog response; a lens whose `POST /api/v1/lens/{lens_id}` call fails renders `Lens unavailable` (never an empty canvas pretending to be data).

### 2.9 Modes (`DEC-GUI-08`)

Disclosure modes (merging 61-demo-playbook `Simple/Advanced/Graph/Developer/Architecture` and GAP-NOCODE-002 `novice/analyst/expert`): **Simple**, **Advanced**, **Expert**. Stored per principal (Settings). Effects are defined per screen in §9; globally: Simple hides raw IDs/JSON/dialect text and shows one primary action; Advanced shows filters, cost, QueryPlan preview and secondary actions; Expert shows raw JSON, dialect editors, admin Gremlin (if enabled server-side) and developer tooling. `Graph/Developer/Architecture` from the playbook are lenses/screens, not modes.

### 2.10 Domains, labels and edges

14 graph domains (reference/ontology.md and `manifest.py`): `META, WORK, IDENTITY, CODE, CICD, KNOWLEDGE, AGENT, OPS, TEST, DESIGN, INTEGRATION, DECISION, PROCESS, BUSINESS`. The 06-architecture alternative list is not used. Vertex labels (75+) and edge labels (68+) come from `GET /api/v1/graph/schema` at runtime; the GUI never hardcodes the label list (it may ship a static icon/colour seed table keyed by label for the labels known today, §5.6, with a deterministic fallback for unknown labels).

### 2.11 Query intents and dialects

QueryPlan `intent` enum (OpenAPI): `SEARCH · PATH · IMPACT · NEIGHBORHOOD · LINEAGE · TRACEABILITY`; `evidence_mode`: `NONE · SUMMARY · FULL`; depth 1–8; result_limit 1–500; timeout 50–30000 ms. Application query languages (reference/query-engine): `EQL, NLQ, EOQL, OSQL, Semantic QL`, plus `Gremlin (admin)`; the Query Workbench offers only the dialects confirmed for the active backend by `GET /api/v1/graph/backend` → `capabilities.application_query_languages` (audit-coverage-ledger rule).

### 2.12 Export formats

Client-side graph exports (existing `kgr/export`): `PNG (2x/4x) · SVG · Print/Save-as-PDF (browser) · JSON-LD · GraphML · GEXF · CSV (nodes+edges) · Obsidian vault (zip) · Mermaid · Cypher · Clipboard Markdown · Interactive HTML`. Server exports: `GET /api/v1/export/formats` (12 ids: `rdf, rdf_xml, rdfs, owl, gremlin, cypher, opencypher, gql, sparql, shacl, pgql, json_ld`) via `POST /api/v1/graph/convert {format_id, limit≤50000}`; `GET /api/v1/ontology/export?limit` (JSON-LD; inspect `export.partial`, `truncated_vertices`, `truncated_edges`, `mapping_losses`). Report document formats are listed by `GET /api/v1/reports` capability; formats that return **501** (PDF/DOCX/PPTX today) are shown disabled with `Not configured on this server (501)`.

### 2.13 Event names

Graph/job events (WS `/ws/graph/events`, poll `GET /api/v1/graph/events`) are rendered by their backend `type` string verbatim; the activity tray groups them into: Graph changes (`vertex_*`, `edge_*`, `ENTITY_*`, `RELATION_*`), Ingestion (`ingestion_*`, `SOURCE_*`), Validation (`validation_*`, `QUALITY_*`), Ontology (`ONTOLOGY_CHANGED`, `GRAPH_VERSION_PUBLISHED`), Identity (`IDENTITY_*`), Trust (`TRUST_CHANGED`). Unknown types go to "Other" — never dropped silently.

### 2.14 Product naming

Default product name string is `KnowGridFlow` with subtitle `Enterprise Ontology & Intelligence Platform (EOIP)`; both are white-label variables (§5.9). Internal IDs, routes and API paths keep `eoip`.

---

## 3. Verified Backend Contract (What the GUI Integrates With)

Everything in this section was verified in code on 2026-10-16. Field names, enums and limits are exact. Treat any deviation discovered at implementation time as a **contract drift incident**: record it in `contracts/gui/drift.md`, do not silently adapt.

### 3.1 Transport basics

| Topic | Verified behaviour | GUI obligation |
|---|---|---|
| Base path | `/api/v1/*` for application APIs; `/health/live`, `/health/ready`, `/metrics`, `/docs`, `/openapi.json` are unauthenticated | `VITE_API_BASE` (default same-origin via Nginx proxy, `apps/web/nginx.conf`) |
| Auth | `Authorization: Bearer <token>`; missing/invalid → **401** `{"detail":"A valid Bearer token is required"}`. Token is either the bootstrap `EOIP_API_TOKEN` (principal `bootstrap-admin`, roles `admin,system`) or an HMAC-signed token from `POST /api/v1/auth/login` or `POST /api/v1/security/tokens/issue`. | Keep token in memory only; on 401 clear state and route to SCR-001 with return URL |
| Admin boundary | `POST/PUT/PATCH/DELETE` under `/api/v1/admin`, `/api/v1/sources`, `/api/v1/authz`, `/api/v1/security`, `/api/v1/tenancy` require role `admin` or `system` → else **403** `{"detail":"Administrative role required"}` | Render admin mutations disabled when `principal.roles` lacks `admin|system`; still handle 403 |
| Tenant | Header `X-Tenant-Id` (also accepted `X-Tenant-ID`). `authorized_tenant()`: a principal bound to a tenant cannot request another (→ **403** "Cross-tenant access forbidden"); an unbound `admin|system` principal may select any tenant or omit (global). Values `system`, `global`, `default` are treated as unscoped by the graph layer. | Always send `X-Tenant-Id` for the selected tenant; send `X-Principal: <principal.id>` for `/api/v1/tenancy/*` (required by `tenant_context_dependency`, else 403) |
| Correlation | Request may send `X-Correlation-ID` (1–128 chars); response always returns `X-Correlation-ID` and, for domain operations, `X-Audit-ID`. CORS exposes `X-Correlation-ID`, `X-Response-Time-Ms`. | Send `X-Correlation-ID` = UUID v4 per request (replace existing `X-Request-ID`); show correlation ID in every error surface and copy button |
| Body limit | > 4 000 000 bytes → **413** `{"detail":"Request body too large"}`; web UI file imports additionally limited to 3 MB (hubble-local) | Client-side pre-check at 3 MB with explicit message; chunked upload is `BACKEND-MISSING-011` |
| Errors | Most handlers: `{"detail": string | ValidationError[]}` with 400/404/409/415/422/501/503. Global 500 and 504 return `application/problem+json`: `{type,title,status,detail,instance,correlation_id,error:{code,message,category,severity}}` (e.g. `EOIP-SYS-500`, category `INFRASTRUCTURE`) | Normalize both shapes into `ApiProblem {status, title, detail, code?, category?, correlationId, fields?[]}` (§8.3) |
| Rate limit | No `RateLimit-*` headers; 429 may occur from enterprise middleware | Retry GET only, jittered 0.5/1/2/4 s, cap 15 s, max 4 attempts; respect `Retry-After` if present |
| Pagination | Non-uniform: `limit` query params with per-endpoint caps (search ≤ 100, ontology export ≤ 10 000, events ≤ 1 000, admin audit/timeline ≤ 500); no cursors | Expose `limit` as a bounded control; show `Showing first N (server cap)`; never claim totals you did not receive |
| Idempotency | No `Idempotency-Key` support | Disable submit buttons while in flight; de-duplicate by correlation ID client-side; never auto-retry mutations |
| Caching | No ETag | Query stale-while-revalidate 30 s for lists, 0 for mutations' detail refetch |

### 3.2 Identity, session and tenancy endpoints

| Endpoint | Request | Response | Notes / GUI use |
|---|---|---|---|
| `POST /api/v1/auth/login` | `LoginRequest {username*, password*}` | `{token}`; 401 `invalid credentials` | SCR-001 local login (when identity provider configured) |
| `GET /api/v1/auth/health` | — | provider health object (no secrets) | SCR-001 shows `Identity provider: <status>` |
| `POST /api/v1/security/tokens/issue` | `IssueTokenRequest {subject*, roles[], scopes[], tenant_id='default', attributes{}, ttl_seconds≥1 default 3600}` | `{token, jti, subject, roles, scopes, tenant_id, expires_at}` | Admin only; SCR-021 token issuance; show token **once** |
| `POST /api/v1/security/tokens/verify` | `{token*, required_scopes?}` | `{valid, payload, subject, roles, scopes}`; 401 on invalid | SCR-001 post-login self-check (derive principal, roles, tenant_id, exp) |
| `POST /api/v1/security/tokens/revoke` | `{identifier*, reason='revoked_by_admin', expires_at?}` | `{revoked, identifier, reason, active_revocations}` | SCR-021; typed confirmation |
| `GET /api/v1/security/status` | — | `{status, enforcement_mode, algorithm, key_rotation_supported, active_revocations_count, roles_registered, permissions_known, timestamp}` | SCR-021 posture panel; render each field, never defaults |
| `GET /api/v1/security/policy-matrix` | — | `{roles_hierarchy{role:{rank,inherited_roles,permissions,description}}, all_permissions[]}` | SCR-021 roles tab |
| `GET /api/v1/tenancy/context` | headers `X-Tenant-Id`, `X-Principal` | `{tenant_id, urn, principal}`; 403 if headers missing | Shell context bar validation after tenant selection |
| `GET /api/v1/tenancy/quotas` | same headers | `{tenant_id, lane, spec, usage{dim: value}}` | SCR-022 |
| `GET /api/v1/tenancy/isolation/models` · `GET/POST …/placement` | `{model, layers}` | placement object | SCR-022 (read; POST admin) |
| `GET /api/v1/authz/users` · `POST` | `AuthzUserRequest {user_id*, roles[], attributes{}}` → 201 | `{users:[...]}` / user | SCR-021 Users tab (admin) |
| `GET /api/v1/authz/roles` · `POST` | `AuthzRoleRequest {name*, description, permissions[]}` → 201/409/422 | `{roles:[...]}` | SCR-021 Roles tab |
| `GET /api/v1/authz/policies` · `POST …/reload?replace_existing=true` | body `application/yaml` text | `{policies:[{policy_id|id, role, permission, conditions, description}]}` / `{loaded}` | SCR-021 Policies tab — **always** `replace_existing=true` (GUI-A004) |
| `POST /api/v1/authz/evaluate` | `{user_id*, action*, resource_attrs{}}` | decision object with `allow` | SCR-021 "What can this user do?" simulator (SR-SEC-002) |
| `GET /api/v1/authz/decisions` | — | `{decisions:[...]}` | SCR-021 audit of decisions |
| `GET /api/v1/authz/users/export` · `/roles/export` | — | JSON file | SCR-021 export buttons |

**Missing** (render disabled, never mock): `BACKEND-MISSING-001` session exchange (OIDC/PKCE), `BACKEND-MISSING-002 GET /api/v1/me` (current principal) — until present, the GUI derives principal from `POST /api/v1/security/tokens/verify` on the token it holds (bootstrap tokens return 401 from verify → treat as `bootstrap-admin`, roles `admin,system`, tenant unbound, label `Deployment access (bootstrap token)` in the context bar). `GUI-BE-021` workspaces — until present, workspace = tenant-scoped **named view namespace** stored client-side (§3.9) and the URL segment `/w/default` is used; the switcher shows `Workspaces not enabled on this server`.

### 3.3 Graph read endpoints (core of SCR-005/006/007)

Common response: `GraphResult {query_id*, nodes[GraphNode{id*, label*, domain?, properties{}}], edges[GraphEdge{id*, type*, from_id*, to_id*, creation_status?, properties{}}], paths[{path_id*, node_ids[], edge_ids[]}], evidence[object], partial*, warnings[]}`. `TraversalGraphResult` adds `meta{}`. **Always render `partial` and `warnings`** as an inline banner on the result (GUI-COMP-19 ResultBanner).

| Endpoint | Request | Caps / errors | Screen |
|---|---|---|---|
| `GET /api/v1/search?q&label?&limit=25&include_deleted=false` | q 1–256 chars; label must be a known vertex label | limit ≤ 100; 422 blank or unknown label | Global search, SCR-005 |
| `POST /api/v1/search/faceted` | `SearchRequest {query, entity_types[], domains[], owners[], source_systems[], trust_states[], projects[], freshness[], limit≤500}` | — | Global search facets; `SearchResponse {query, total, hits[SearchHit{canonical_id,label,name,score,authority?,trust_state,freshness,last_seen?,evidence[],matched_fields[],matched_terms[],why}], facets{entity_type,domain,owner,source_system,trust_state,freshness,project: [FacetBucket]}}` — render `why` as the "why this result" line (gaps §38) |
| `GET /api/v1/entities/{canonical_id}?include_deleted` | path may contain `/` | 404 `Entity not found` | SCR-006: `{entity{vid,label,properties{canonical_id,...,deleted_at?}}, outgoing[edge], incoming[edge]}` |
| `POST /api/v1/neighborhood` | `{canonical_id*, max_depth 1–4 =1, result_limit 1–500 =50}` | 404 if no nodes; 422 policy | Expand node |
| `POST /api/v1/path` | `{source_id*, target_id*, max_depth 1–8 =8, relationship_allowlist[]}` | 422 policy | Path finder; semantic allowlist applies — for incident/release/test/design scenarios use `shortest-paths` (demo audit) |
| `POST /api/v1/graph/shortest-paths` | `{source_id*, target_id*, max_paths 1–20 =5, max_length 2–20 =10}` | — | `{paths, count}` |
| `POST /api/v1/impact` | `apps__api__app__ImpactRequest {canonical_id*, max_depth 1–8 =4, result_limit 1–500 =100}` | 404/422 | SCR-007 (`TraversalGraphResult`) |
| `POST /api/v1/lineage` | `{canonical_id*, max_depth =4, result_limit =100}` | 404/422 | SCR-006 Provenance tab |
| `POST /api/v1/traceability` | `{canonical_id*, max_depth =6, result_limit =100}` | 404/422; evidence FULL | Requirement lens |
| `POST /api/v1/query` | `QueryPlan` (see §2.11) | 422 `PolicyViolation` text | SCR-011 structured plan, visual query builder |
| `POST /api/v1/query/nl` | `{question*}` | — | `{interpretation{plan?,...}, result?, answer, confidence, engine, highlights, followups, warnings}`; if `interpretation.plan` is null show "Could not interpret — refine" with `followups` |
| `POST /api/v1/query/eql` | `{query}` | 400 if empty | SCR-011 EQL dialect |
| `POST /api/v1/query/language` | `QueryLanguageRequest {language*, query*}` | — | SCR-011 other dialects |
| `POST /api/v1/query/explain` · `/cost` | `QueryPlan` | — | SCR-011 Explain/Cost panels (SR-QRY-003) |
| `GET /api/v1/query/history` · `/slow?threshold_ms&top_n` | — | — | SCR-011 History tab |
| `GET/POST /api/v1/query/templates` · `GET/DELETE …/{id}` · `POST …/{id}/bind {params{}}` | `TemplateSaveRequest {name*, intent*, anchor_params[]*, description, filters_template?, relationship_allowlist?, max_depth=3, result_limit=50, timeout_ms=5000, evidence_mode='SUMMARY', created_by}` | 201 | SCR-011 saved templates (real durable CRUD) |
| `POST /api/v1/query/why` · `/why-not` · `/what-if` · `/what-changed`; `GET /api/v1/query/why/{cid}` · `/what-changed/{cid}` · `/context/{cid}` | object bodies | — | Operator buttons (§1.1) in SCR-006 inspector and command palette |
| `GET /api/v1/graph/schema` | — | `{ontology_version, schema_version, domains, vertex_labels{label:{domain,required_properties,optional_properties,instance_count}}, edge_labels{label:{source_labels,target_labels,properties}}, property_keys, indexes[{name,type,label,fields}]}` | Legend seed, SCR-012/013, filter option lists |
| `GET /api/v1/graph/statistics` | — | `{vertex_count, edge_count, density, vertex_label_count, edge_label_count}` | SCR-003, status bar |
| `GET /api/v1/graph/backend` · `/backends` | — | `{configured_backend, active_backend, connection{…redacted}, ping, capabilities{models,query_languages,native_query_language,exports,architecture,application_query_languages,notes}}` | Context bar backend chip; dialect gating |
| `GET /api/v1/lens/catalog` · `POST /api/v1/lens/{lens_id}` | body `KnowledgeContext` (scope/entities/time/filters) | `{lenses:[{id,name,description}]}` / lens data or `{error, available[]}` | Lens switcher |
| `GET /api/v1/files/{path}` | path within repo root | text | SCR-006 Code panel (source viewer), via authenticated client only |

### 3.4 Analytics endpoints (SCR-005 overlays, SCR-006 Impact/Similarity tabs, SCR-007)

| Endpoint | Request | Response (verified or documented) |
|---|---|---|
| `POST /api/v1/graph/blast-radius` · `/reverse-impact` | `{canonical_id*, max_depth 1–8 =4}` | `BlastRadiusResult {target_id, total_affected, by_depth{depth:count}, by_type{label:count}, risk NONE|LOW|MEDIUM|HIGH|CRITICAL, affected_ids[], affected_details?[{canonical_id,label,path_depth,edge_classes}]}`; 404 if entity missing |
| `POST /api/v1/graph/metrics` | `{canonical_ids[]*}` | `{cid: CentralityMetrics{canonical_id,degree,in_degree,out_degree,betweenness,closeness,page_rank}}` |
| `POST /api/v1/graph/centrality/full` | `{canonical_ids[]*, algorithms[]=8 defaults}` | `{cid: metrics}` |
| `POST /api/v1/graph/cluster` | `{resolution .1–10 =1, algorithm 'label_propagation'|'louvain'|'leiden', limit≤50000}` | `{communities:[{id,members[],size}], modularity}` |
| `POST /api/v1/graph/similarity` · `/link-prediction` | `{canonical_id*, algorithm, limit≤50}` | ranked list `[{canonical_id, score, common_neighbors?}]` |
| `POST /api/v1/graph/k-core` · `/components` · `/degree-distribution` | `{min_k}` / `{limit}` / — | maps/lists |
| `POST /api/v1/graph/what-if` | `{canonical_id*, action 'remove'|'isolate'}` | `{broken_paths, orphaned_entities, affected_centrality}` — **non-mutating** |
| `POST /api/v1/graph/anomalies` · `/surprises` | `{algorithms[], threshold 1–5}` / `{limit≤100}` | lists |
| `GET /api/v1/graph/orphaned?entity_types` · `/stale?threshold_hours` · `/pr-impact` | — | lists |
| `POST /api/v1/graph/diff` (snapshot_a, snapshot_b) · `GET /api/v1/graph/diff?from&to&limit` · `GET /api/v1/graph/versions?limit` · `GET /api/v1/graph/as-of?at&limit` | ISO-8601 `at` else 422 | diff/version lists |
| `POST /api/v1/graph/bitemporal/{slice|valid-at|known-at|topology|diff}` | `BitemporalCoordinate {valid_at?, known_at?}` / `BitemporalDiffRequest {from_coordinate*, to_coordinate*}` | `BitemporalSlice` / `BitemporalTopology` / `BitemporalDiff` |
| `GET /api/v1/enterprise/snapshots` · `POST` `{name*, snapshot_type='FULL', tags{}}` · `GET/DELETE …/{id}` · `POST …/compare?id_a&id_b` · `POST …/restore {snapshot_id*}` | — | SCR-010; restore is **destructive → typed confirmation** |
| `GET /api/v1/change-journal?after&limit` · `GET /api/v1/enterprise/diff/changes?limit` · `/diff/stats` · `/diff/timeline/{entity_id}` | — | SCR-008 |
| `POST /api/v1/causal/live-blast-radius` | `{shock_entities{cid:number}*, max_depth 1–10 =3, failure_threshold .1–1 =.5, dampening_factor .1–1 =.85}` | SCR-007 Live mode |
| `POST /api/v1/causal/counterfactual-intervention` | `{shock_entities*, interventions*, max_depth}` | SCR-007 |
| `POST /api/v1/causal/hypotheses/{incident_cid}` · `/correlations/{entity_cid}` body `{time_window_hours=24}` | — | SCR-009 |
| `POST /api/v1/enterprise/correlation/analyze/{event_id}` | — | SCR-009 |
| `POST /api/v1/algorithms/run` · `GET /api/v1/algorithms` | `AlgorithmRequest {algorithm*, source_id?, target_id?, canonical_ids?, max_depth≤20, limit≤500, k≤50, direction='outgoing', allowed_labels?, blocked_labels?}` | Expert-mode algorithm runner |
| `POST /api/v1/graph-tests/run` | object | SCR-007 test checklist (graph tests) |

### 3.5 Brain / Ask / RAG / agents

| Endpoint | Request | Response / notes |
|---|---|---|
| `POST /api/v1/brain/ask` | `BrainAskRequest {query*, loop='HITL-FE', risk_tier='R1', rag_mode='HYBRID_RAG', target_database='NEO4J', force_deterministic=false, tier='OPUS_FRONTIER', context{}}` | object; render `mode` per §2.4; the `tier` names are **simulator cognitive tiers**, label them `Simulated tier` (CONFLICT-006) |
| `POST /api/v1/brain/intelligent-query` · `/brain/query` (report) · `/brain/narrate` | `{query*, approach='HYBRID', tier, context}` / `CognitiveNarrateRequest` | SCR-004 |
| `GET /api/v1/brain/approaches` · `/dialects` · `/databases` · `/agents` · `/loops` · `/rag-modes` · `/llm/models` | — | arrays → populate selectors; never hardcode options |
| `POST /api/v1/brain/llm/stream` | `LLMGenerateRequest {prompt*, tier, system_prompt, max_tokens=1024, temperature=.7, top_p=.95, top_k=40, min_p=.05, repetition_penalty=1.1, json_schema?, enable_xai=true, context, stream?}` with header `Accept: text/event-stream` | **Real SSE**: `data: {chunk_id, delta, index, is_final, accumulated, usage}` … `data: [DONE]`. Without the Accept header it returns the full array (not streaming). Use `fetch` + `ReadableStream` (POST SSE), AbortController for Stop. `BACKEND-MISSING-005` (durable answer events with Last-Event-ID/cancel) remains missing → no resume after disconnect; show `Stream interrupted — regenerate`. |
| `POST /api/v1/brain/llm/generate` · `/explain` · `/tokenize` · `/embed` | — | Expert mode tools |
| `POST /api/v1/rag/query` `{query*, pattern?, context}` · `GET /api/v1/rag/patterns` · `POST /api/v1/rag` `RetrievalRequest` · `POST /api/v1/retrieval/search {question*, canonical_id?, strategy?, top_k≤100}` | — | Evidence retrieval panel; `EvidenceManifest {citations[{canonical_id, source_ref, confidence, fact_text}], total_facts, coverage_score}`; model-down returns `partial:true` structured result (reference/rag.md) |
| `POST /api/v1/suggest` · `/suggest/interpret` `{question*, session_id?, user_id?, roles[], limit≤20 =5}` · `GET /api/v1/suggest/intents` | — | `SuggestionResponse {question, candidates[CandidateInterpretation], llm_assist_used, parse}` → suggestion cards (§11.2) |
| `POST /api/v1/evidence/manifest` | `{answer_id*, node_ids[], edge_ids[], evidence_refs[], query_plan?, tool_calls[], rules_fired[], confidence_inputs[]}` | Evidence manifest export (GAP-PROV-006) |
| `GET /api/v1/agents` · `GET /api/v1/agents/types` | — | `[{id, version, capabilities, risk, budgets, enabled}]` — render disabled agents as disabled |
| `POST /api/v1/agents/{agent_id}/runs` | `AgentRunRequest {goal*, context_refs[], budgets{}, dry_run=false, synthesize=false, memory_ttl_seconds?}` | run result with `explanation` envelope (`chain_of_thought_disclosed:false` always) |
| `GET /api/v1/agents/runs/{run_id}` · `/memory` · `/explanation` | — | trace, memory, XAI envelope `{answer, confidence, evidence_refs, reasoning_steps, partial, agent_type, duration_ms}` |
| `POST /api/v1/agents/query` `{query*, agent_type?, context}` · `/analytics` · `/trace-impact {canonical_id*, max_depth}` · `/semantic-index` | — | SCR-004/007/018 |
| `GET /api/v1/agents/proposals?status` · `POST …/{id}/approve|reject {actor_id*}` | — | SCR-018 Approvals: approval **records a decision only**; label `Approval does not apply the mutation` (deep-agents-xai) |
| `GET /api/v1/agents/mesh/recoveries?status` · `POST …/recover/{recovery_id}` | — | SCR-018 Recovery |
| `GET /api/v1/loops/catalog` · `/approvals/pending` · `POST /loops/approvals/decide` · `POST /loops/run/{loop_name}` | `DecideRequest`, `RunLoopRequest` | SCR-018 Loops tab |
| `GET /api/v1/governance/models` · `/templates` · `/incidents` · `/kill-switch` · `POST /kill-switch {enabled*, reason}` · `POST /kill-switch/features/{feature}` | — | SCR-021 Model governance; kill switch is **destructive-class** confirmation |
| `GET /api/v1/egress/endpoints` · `/policy/rules` · `/report` · `/manifests` · `POST /egress/kill` | — | §2.5 badge; SCR-021 Egress tab |

**Missing**: `BACKEND-MISSING-014` agent run event stream → the Agents screen polls `GET /api/v1/agents/runs/{run_id}` every 2 s while status is non-terminal (label `polling`), max 15 min, then shows `Run still active — refresh manually`.

### 3.6 Sources, ingestion, jobs

| Endpoint | Request / Response | Notes |
|---|---|---|
| `GET /api/v1/connectors/catalog` | `{connectors:[{id,name,type 'api'|'crawler'|'file'|'json', capabilities[]}]}` | 16+ connectors (jira, gitlab, github, confluence, servicenow, rally, grafana, datadog, kibana, qtest, figma, api_portal, web, local_code, file_parsing, generic, …) |
| `GET /api/v1/connectors/files/formats` | supported file formats | SCR-015 uploader accept list |
| `GET/POST /api/v1/sources` · `GET/PATCH/DELETE …/{source_id}` | `SourceRegistryEntry` (see §3.6.1); DELETE → 204 | admin mutations |
| `POST …/{id}/discover` (200) · `/dry-run` · `/baseline` · `/sync` · `/reconcile` · `/replay` (all 202 → `{job_id,...}`) | `SourceOperationRequest {checkpoint?, event_ids[], dry_run=false}` | each returns a job → open in dock |
| `GET …/{id}/checkpoint` · `/reconciliations?limit` · `GET/PUT …/{id}/schedule` `AcquisitionPolicy {max_concurrency 1–16 =1, rate_limit_per_minute 1–60000 =60, paused=false}` · `POST …/pause` · `/resume` | — | SCR-014 detail drawer |
| `GET /api/v1/admin/jobs` | list of job records `{job_id, kind, status, created_at, started_at?, finished_at?, correlation_id, tenant_id, created_by, attempts?, result?, error?}` (payload stripped on detail) | tenant-filtered server-side |
| `GET /api/v1/admin/jobs/{job_id}` · `POST …/cancel` · `POST …/readmit` (202) | 404 / 403 / 409 semantics in §2.1 | SCR-017 |
| `POST /api/v1/admin/ingestion/{jira|gitlab|confluence|servicenow}` (202) | `IngestionRequest {document*, dry_run}`, `GitLabIngestionRequest {document*, dry_run, repository_id='demo'}`, `IncrementalSyncRequest {checkpoint?, watermark?, dry_run}` | SCR-015 manual import (admin) |
| `POST /api/v1/admin/ingestion/json` · `/json/batch` · `/process-and-convert` | `JsonIngestionRequest {data*, source_label='json_upload', pipeline_id='manual'}`, `BatchIngestionRequest {files[]*, pipeline_id='batch'}` | SCR-015 |
| `POST /api/v1/admin/ingestion/files/parse` · `/files` (`?filename&source_id&ocr&dry_run`, body `application/octet-stream`) · `GET …/files/bundles/{bundle_id}/{artifact}` | 415 wrong type, 413 too large, 422 invalid, 503 missing parser dependency; inspect `status PARTIAL|FAILED` even on 200 (file-parsing.md) | SCR-015 uploader |
| `GET /api/v1/ingestion/runs?limit` · `GET /api/v1/ingestion/dlq?limit` · `GET /api/v1/admin/dlq?limit` · `POST /api/v1/admin/dlq/{event_id}/replay` (202) · `POST /api/v1/admin/ingestion/replay` `ReplayRequest {source_system*, event_ids[], repository_id, dry_run}` | DLQ record `{source, event_id, error, payload?, failed_at}` plus G2 fields when present | SCR-017 DLQ tab |
| `GET /api/v1/enterprise/dlq/entries?source&limit` · `/dlq/stats` · `POST /dlq/replay {entry_ids?, source?}` · `DELETE /dlq/{entry_id}` | — | SCR-017 |
| `POST /api/v1/ingest/profile` `{dataset, records[]}` → `ProfileReport {profile_id, record_count, fields[FieldProfile]}` · `/profile/keys` · `/profile/relationships` · `/profile/drift` | — | SCR-015 profiling step |
| `POST /api/v1/systems/register` `RegisterSystemRequest {system_type*, name*, base_url*, auth_type='token', credentials{}, entity_types[], ingestion_mode='auto', poll_interval_minutes=60, batch_size=500, tags[], auto_onboard=true}` · `GET /systems/` · `GET/PUT/DELETE /systems/{id}` · `POST …/test-connection` · `/onboard` · `/generate-schema` · `/create-pipeline` · `/set-status?status` · `GET …/onboarding-status` · `GET /systems/known-types` · `POST /systems/schema/from-data` | — | SCR-014 "System" (legacy registry) — show both registries with clear labels; credentials field must be **write-only** and never echoed |
| `GET /api/v1/admin/stats` | `{backend, schema, vertices, edges, labels{label:count}, worker}` (15 s server cache) | SCR-003/024 |
| `GET /api/v1/admin/system` | `{graph{status}, model{status 'disabled'|'ready'|'unavailable', configured, name}, backup{status 'available'|'not_created', count, latest{file,created_at,schema_version,vertices,edges,sha256,size_bytes}?}, connectors{checkpoint_count}}` | SCR-024 |
| `GET /api/v1/admin/worker` · `/event-consumers` · `POST /event-consumers/run` · `GET /admin/timeline?limit` · `GET /admin/audit?limit` · `POST /admin/validation` · `GET /validation/runs?limit` · `GET /api/v1/admin/schema` | — | SCR-017/024/021 |
| `POST /api/v1/admin/semantic-pipeline` `{stages?, scope?}` · `GET …/stages` · `GET /api/v1/pipeline/status` · `GET /api/v1/platform/harness/pipelines` · `POST /platform/harness/run` | — | SCR-017 Pipelines tab |
| `POST /api/v1/admin/gremlin` | object | **501/disabled by default** (FR-QUERY-008); Expert mode only; show `Disabled on this server` on 501 |

#### 3.6.1 `SourceRegistryEntry` (exact fields)

`schema_version='1.0', source_id*, source_type*, name*, base_url?, acquisition_modes[], allowed_scopes[], excluded_scopes[], polling_frequency_seconds?, webhook_status, mapping_version?, parser_version?, checkpoint?, last_successful_baseline?, last_incremental_run?, reconciliation_schedule?, health, freshness_slo_seconds?, compatibility{}, enabled=true, capabilities{baseline=true, polling=false, webhooks=false, deletion_events=false, permission_events=false, discovery=true, reconciliation=false, replay=true}, config{}, secret_refs{key: 'env://…'|'file://…'|'vault://…'}, created_at, updated_at`. Inline secret-like config keys are **rejected by the server** (ADR-001) — the GUI form only accepts reference URIs in `secret_refs`.

### 3.7 Ontology, identity, quality, catalog, compliance

| Endpoint | Notes |
|---|---|
| `GET /api/v1/ontology/export?limit≤10000` (JSON-LD, inspect `export.partial/truncated_*/mapping_losses`) · `POST /ontology/import?clear` (admin) · `GET /ontology/shacl` · `GET /ontology/validate?limit` · `GET /ontology/drift` · `POST /ontology/diff` · `POST /ontology/proposals` (201) · `GET /ontology/packs` · `/packs/{name}` | SCR-012/013 |
| `GET /api/v1/ontology/gitops/branches` · `POST` `{branch_name*, base_branch='main'}` · `POST …/branches/commit {branch_name*, manifest*, commit_message*, author}` · `POST /gitops/diff` · `/validate` · `/impact` · `/migration` · `GET/POST /gitops/prs?status` · `POST …/prs/{id}/review` · `/merge` · `POST /gitops/rollback` · `/package-release` | SCR-012 draft lifecycle (draft=branch, review=PR) — `BACKEND-MISSING-010` single publish endpoint remains missing; compose from these with explicit step status |
| `POST /api/v1/enterprise/migrations {version*, name*, up_steps[]*, down_steps?, description}` · `GET /migrations` · `POST …/apply-all` · `…/{id}/apply` · `…/{id}/rollback` | SCR-012 migration step |
| `GET /api/v1/identity/candidates?status` · `POST …/{id}/decide {actor_id*}` · `POST …/{id}/reject {actor_id*}` | SCR-016 (merge/split/undo `BACKEND-MISSING-013` missing → only decide/reject exposed) |
| `POST /api/v1/conformance/check` · `GET /conformance/rules` · `PUT /conformance/rules/{name}` | SCR-016 Conformance / Architecture lens violations (GAP-ARCH-003) |
| `GET /api/v1/knowledge/debt` (alias `/knowledge-debt`) · `/knowledge/freshness?stale_days` · `GET /knowledge-slos` · `POST /knowledge/slo` · `GET /knowledge/trust/states` · `POST /knowledge/firewall/inspect` | SCR-016 Knowledge health; SLO dashboards show objective/current/trend/breached (G2-SLO-004) |
| `GET /api/v1/truth/contradictions` · `/assertions/{subject}/{predicate}` · `/explain/{subject}/{predicate}` · `POST /truth/claims` · `/truth/resolve` · `GET /truth/export` | SCR-016 Claims tab; note `Truth/SKOS state is process-local and does not survive API restart` (demo README) — show as a persistent info banner |
| `GET /api/v1/catalog/products?owner&domain&state&access_policy&consumer` · `POST` · `GET/PUT/DELETE …/{id}` · `POST …/{id}/transition {to_state*}` · `GET …/{id}/lineage` · `/export` · `POST /catalog/products/import` | SCR-006 "Knowledge product" tab for `KnowledgeProduct` vertices; Reports catalog |
| `GET /api/v1/taxonomy/schemes|concepts|mappings` · `POST` · `GET /taxonomy/validate?scheme` · `/export.rdf` | SCR-012 Glossary/SKOS tab |
| `GET /api/v1/compliance/packs` · `/packs/{framework}` · `POST …/gap-analysis` · `GET /compliance/changes?state&kind` · `POST /compliance/changes?kind&title&description&requested_by&created_at` · `POST …/{id}/transition?to_state&actor&at&reason` · `GET /compliance/exceptions` · `/roles` · `/ai/model-cards` · `/ai/evaluations` | SCR-008 (change proposals), SCR-021 Compliance tab |
| `GET /api/v1/config/definitions` · `/effective?key&tenant&business_unit&workspace&user_id` · `/explain?…` → `ExplainResult` · `POST /config/set` · `/bounds` · `/rollback` · `/diff` · `/export` · `/import` · `GET /config/audit?key` · `GET/POST /config/flags` · `GET /api/v1/enterprise/feature-flags` · `POST …/override {flag_name*, tenant_id*, enabled*}` | SCR-022 Configuration tab with **effective-config explain** (SR-CFG-003) |

### 3.8 Reports, notifications, licensing, branding, health

| Endpoint | Notes |
|---|---|
| `GET /api/v1/reports` (capability) · `GET /reports/templates` · `POST /reports/render?template_id&report_format&generated_at` body `ReportContext {title, params, graph_stats, evidence_manifest[], findings[], narrative}` · `GET /reports/export/{report_id}?report_format` (501 for unconfigured formats) · `GET/POST /reports/schedules?template_id&name&recurrence&report_format` · `GET …/due` · `DELETE …/{id}` (204) · `POST …/{id}/mark-run?at` | SCR-019; `BACKEND-MISSING-015` durable export jobs missing → render is synchronous; show size/type/sha when returned |
| `GET /api/v1/platform/notifications/inbox/{recipient}?unread_only&limit` · `POST …/{id}/read` · `POST /notifications/send {recipient*, subject*, body*, channel='IN_APP', priority='NORMAL', category='SYSTEM'}` · `GET /notifications/stats` | SCR-026 — recipient = current principal id only (never another user's path) |
| `GET /api/v1/licensing/status` · `POST /licensing/verify {document*, vendor_key*}` · `POST /licensing/check-module {module*}` → `CheckOutcome {allowed, check, degraded, notice?, limit?, current?}` · `GET /licensing/meter/export` · `/verify` | SCR-026 About/Licences; `degraded=true` → read-only banner, never lock/delete (SR-DEP-007) |
| `GET /api/v1/branding/theme?tenant_id&mode` · `/legal?tenant_id&kind` · `/locales/{locale}/message?key&tenant_id&default` · `POST /branding/terminology/canonicalize {labels[]}` · `/rename {canonical_types[]}` | SCR-023 (read/preview); publish = `BACKEND-MISSING-018` |
| `GET /api/v1/enterprise/health/aggregate` · `/live` · `/ready` · `/startup` · `/sla` · `/uptime` · `POST /health/check-all` · `GET /health/graph` · `/health/embeddings` · `GET /api/v1/enterprise/resilience/circuit-breakers` · `POST …/reset` · `GET /enterprise/lifecycle/status` · `POST /lifecycle/drain` · `GET /enterprise/observability/metrics` · `GET /api/v1/enterprise/analytics/metrics` · `/trend/{metric}?window` · `/anomalies/{metric}?threshold` · `/forecast/{metric}?horizon&method` · `/growth/{metric}` · `GET /api/v1/ops/preflight` · `/ha-topology` · `/support-bundle` · `POST /ops/upgrade-plan` · `/shard-plan` · `/helm-summary` | SCR-024; `check-all`, `reset`, `drain` are explicit privileged commands (never auto-triggered by polling — SCR-027 rule) |
| `GET /api/v1/platform/recovery/checkpoints?limit` · `POST …/checkpoint?label` · `POST …/restore/{point_id}` · `GET …/rpo` · `/peers` · `/stats` · `/wal/read?start_lsn&limit` | SCR-022/024 Backup & recovery tab; restore is destructive-class |
| `GET /api/v1/platform/incidents?state&severity&limit` · `POST {title*, description*, severity='SEV3', reporter*, assignee?, affected_services[]}` · `GET …/{id}` · `POST …/{id}/transition {new_state*, actor*, details}` · `GET /incidents/stats` | SCR-009 |
| `GET /api/v1/platform/integrations?connector_type` · `POST …/{connector_id}/health` · `/sync` · `GET …/{id}/history?limit` · `GET /integrations/stats` | SCR-014 secondary registry (label `Platform integrations`) |
| `GET /api/v1/demo/scenarios` | `{dataset_id, version, title, description, ready, scenarios[{id,title,audience,story,capabilities[],entrypoint,expected_path[],expected_path_state[{canonical_id,available}],relationship_allowlist[],available,ready}]}` | `/help` → Guided tour (Demo Mode, explicitly labelled) |
| `GET /api/v1/product/capabilities` · `/first-choice-gate` · `GET /api/v1/gaps/coverage` · `/completion-gate` | SCR-024 "Product readiness" (three separate counts, R9) |
| `GET /api/v1/domain-packs` · `/{pack_name}` · `POST …/activate` | SCR-012 Domain packs tab |
| `GET /api/v1/marketplace/packages?q` · `/installed` · `POST /marketplace/install` · `/packages/install` · `DELETE /packages/{name}` | SCR-012/018 Marketplace tab (internal marketplace); show Data-Flow Manifest before install (SR-CON-011) |
| `GET /api/v1/capsules` · `POST {…}` · `GET /capsules/{name}` | SCR-019 Evidence capsules |
| `POST /api/v1/playback/stream {root_cid*, max_depth=3, max_events=200}` · `/playback/evidence {root_cid*}` · `/playback/export {root_cid*, format='json'}` | SCR-010 Playback |
| `POST /api/v1/simulation/create` · `GET /simulation/list` · `GET …/{sim_id}/analyze?analysis_type` · `/compare` · `/manifest` · `POST …/{sim_id}/mutate` · `POST /api/v1/whatif/plan` · `/execute` | SCR-007 Scenario mode (Simulation lens) |
| `GET /api/v1/twin/coverage` · `/classify` · `/missing-links` · `/business/chain/{objective_cid}` · `/business/reverse-impact/{service_cid}` · `/decisions/{entity_cid}` · `/test-intelligence/mappings` · `/runs` · `POST /test-intelligence/select` | Lenses: `requirement`, `decision`, `test` |
| `GET /api/v1/process/cases?source_label` · `/paths` · `POST /process/deviations` | `process` lens |
| `POST /api/v1/xai/certify-decision` · `/verify-certificate` · `POST /api/v1/platform/xai/explain` · `/calibrate` | SCR-018 XAI verification panel (UI-04) |
| `POST /api/v1/query/multi-paradigm {query*, seed_canonical_ids?, max_depth≤6 =2, monte_carlo_samples 10–500 =50}` | SCR-011 Multi-paradigm (UI-02) |
| `POST /api/v1/federation/query` · `GET /federation/sources` | SCR-011 Federated dialect; SCR-014 federated sources list with mode `VIRTUAL|CACHE|MATERIALIZE|HYBRID` shown verbatim from response |

### 3.9 Real-time

| Channel | Verified | GUI behaviour |
|---|---|---|
| `WS /ws/graph/events` | Accepts `Authorization: Bearer` header or `?token=`; `tenant_id` from query or `x-tenant-id` header; closes 1008 on missing auth, unauthorized tenant or token expiry; sends `event.to_dict()` JSON per visible event | Browsers cannot set WS headers → **do not use `?token=`** (R5). Until `GUI-BE-029` (one-use WS ticket) exists, use polling below and label the tray `Live updates: polling`. |
| `GET /api/v1/graph/events?since|since_id|limit≤1000` | `{events:[…]}`, tenant-filtered via `X-Tenant-Id` | Poll every 5 s when tab visible, 30 s when hidden; keep `since_id` cursor; dedupe by event id; bounded buffer 500; on 401/403 stop and show auth state |
| `POST /api/v1/brain/llm/stream` (SSE over POST) | see §3.5 | Streaming answer; AbortController on Stop |
| Job progress | no stream; poll `GET /api/v1/admin/jobs/{id}` every 2 s while non-terminal (visible dock), 10 s when hidden | Dock job rows |

### 3.10 Missing contracts (GUI must render disabled with reason)

Reuse the 20 `BACKEND-MISSING-001..020` definitions from `GUI-UIX-requirements.md` §17 and `GUI-BE-021..028` from the implementation plan §10.21. New in this document:

| ID | Need | Interim GUI behaviour |
|---|---|---|
| `GUI-BE-029` | One-use WebSocket connection ticket (`POST /api/v1/realtime/ticket` → short-lived token usable only in the WS handshake) | Poll `GET /api/v1/graph/events`; tray label `polling` |
| `GUI-BE-030` | Saved graph views server CRUD (`BACKEND-MISSING-004` broadened to list/get/update/delete/share) | Store views in Dexie namespaced `{principal, tenant, workspace, schema_version}` with export/import JSON; label `Saved locally on this device` |
| `GUI-BE-031` | Entity 360 aggregate (`BACKEND-MISSING-006`) | Compose client-side from `GET /entities/{id}` + `/neighborhood` + `/lineage` + `/enterprise/diff/timeline/{id}` + `/graph/metrics` + `/identity/candidates`, each section independently loadable and failable |
| `GUI-BE-032` | Cursor pagination on list endpoints | Use `limit` with "server cap" notice; never fabricate totals |
| `GUI-BE-033` | `RateLimit-*`, `ETag`, `Idempotency-Key` | §3.1 fallbacks |

---

## 4. Technology Stack and Project Structure (Binding)

### 4.1 Stack decisions

| Concern | Decision (`DEC-GUI-09`) | Rationale / constraint |
|---|---|---|
| Framework | React 19 + TypeScript **strict** + Vite SPA (no SSR) | Existing app is React/Vite; TS strict is required for new modules; legacy JSX is wrapped behind typed adapters until migrated |
| Routing | TanStack Router (file-based, typed params/search) | Typed deep links `/t/:tenant/w/:workspace/...` with validated search params |
| Server state | TanStack Query | Keys `[tenant, workspace, resource, params]`; one `QueryClient` per scope generation |
| Shell/ephemeral state | Zustand (per-feature slices) | Inspector/dock/selection; cleared on scope change |
| Long-running lifecycles | XState v5 only for: ingestion wizard, ontology publish, query execution, upload | No other state machines |
| Durable local drafts/views | Dexie (IndexedDB) namespaced `{principal, tenant, workspace, schemaVersion}` | Never tokens/PII; purge on logout and scope switch |
| Styling | Tailwind CSS v4 with CSS variables from the token source; Radix UI primitives for behaviour | No component library theme that fights tokens; no CSS-in-JS runtime |
| Motion | `motion` (Framer Motion successor) using §5.8 tokens; CSS transitions for micro states | Reduced-motion hook mandatory |
| Graph | Sigma (WebGL) + Graphology; `graphology-layout-forceatlas2` in a Web Worker; ELK.js for layered/lineage; `graphology-communities-louvain` client fallback only for visual grouping of already-returned subgraphs | Cytoscape removed after §10.12 parity |
| Diagrams (editable) | React Flow (`@xyflow/react`) for ontology draft canvas, pipeline/workflow builder, visual query builder | Not for the knowledge graph |
| Charts | Apache ECharts (lazy, per-chart modules) | timeline, Sankey, treemap, sunburst, heatmap, chord, radar, bar/line |
| Tables | TanStack Table + TanStack Virtual | ARIA grid, virtual > 100 rows |
| Code/query editor | Monaco (lazy) | read-only source viewer; query dialects |
| Rich text | Tiptap (lazy) | report narrative and comments; sanitized output |
| Forms | React Hook Form + Zod | Zod schemas generated from OpenAPI snapshot via `openapi-typescript` + a reviewed converter; hand-written for `object`-typed bodies |
| API client | `openapi-fetch` on the generated types, wrapped by the existing `shared/api/client.ts` transport (headers, abort, dispose, error normalization) | Single transport; components never call `fetch` |
| Command palette | `cmdk` | §6.6 |
| Hotkeys | `react-hotkeys-hook` with scopes | §6.7 |
| DnD | `@dnd-kit/core` | mapping designer, Kanban, column reorder |
| Panels | `react-resizable-panels` | inspector/dock sizes persisted per principal/workspace |
| Icons | `lucide-react` only (already a dependency) | §5.6 registry; no hand-authored SVG except domain glyphs approved in `design-system/icons/domain/` |
| i18n | `i18next` + `react-i18next`, ICU message format | §13.2 |
| Testing | Vitest + Testing Library; Playwright (projects: `mocked`, `real-api`, `visual`, `a11y`, `perf`); Storybook; MSW (dev/test only); `@axe-core/playwright` | §14 |
| Telemetry | OpenTelemetry Web → local collector only; disabled unless tenant consent | §13.5 |

**Version pinning rule (`DEC-GUI-10`)**: do **not** copy versions from any document. At implementation time run `npm view <pkg> version` for each package, pin the exact resolved version in `package.json`, record peer-dependency and licence in `apps/web/THIRD_PARTY_INVENTORY.json`, and commit the lockfile. Do not use `--force` or `--legacy-peer-deps`. Node ≥ 22.18 (CI uses 22.18.0 per audit).

### 4.2 Directory layout (target; migrate incrementally)

```text
apps/web/src/
  app/
    router/            route tree, guards (auth, scope, capability), route meta (title, persona, mode)
    providers/         QueryClient, Identity, Scope, Theme/Tokens, I18n, Telemetry, Capability
    shell/             Rail, ContextBar, Inspector, Dock, CommandPalette, ActivityTray, SkipLinks
  design-system/
    tokens/            tokens.json (DTCG) → generated tokens.css + tokens.ts (do not hand-edit generated files)
    primitives/        Radix wrappers (Button, Dialog, Popover, Tabs, Tooltip, Toggle, Select…)
    components/        composed components in §7 with stories and tests
    icons/             lucide registry + domain glyphs + <Icon name/> adapter
    motion/            duration/easing tokens, useReducedMotion, AnimationBudget
  entities/            typed domain models + query-key factories + Zod schemas
    tenant/ workspace/ principal/ source/ job/ ontology/ graph/ entity/ report/ agent/ incident/ snapshot/
  features/            one folder per screen family (public index.ts only)
    auth/ onboarding/ overview/ ask/ graph/ entity/ impact/ changes/ incidents/ time/ query/
    ontology/ meta-graph/ sources/ ingestion/ quality/ jobs/ agents/ reports/ collaboration/
    governance/ tenant-admin/ branding/ health/ settings/ notifications/ help/ errors/
  shared/
    api/               client.ts (existing), problem.ts, generated/ (openapi types), hooks
    events/            polling subscription manager (existing hook refactored), event reducer
    auth/              token holder (memory), principal derivation, scope generation counter
    telemetry/ i18n/ workers/ security/ (sanitize, csp helpers) test/
  legacy/              existing JSX wrapped behind adapters; each file has a removal criterion comment
```

**Boundary rules (`GUI-ARCH-01`)**: `features/*` may import `entities`, `shared`, `design-system`, `app/providers` hooks; never another feature's internals (ESLint `import/no-restricted-paths`). `entities` may not import `features`. `design-system` may not import `entities`/`features`. Circular imports fail CI (`madge`).

### 4.3 State ownership (`GUI-ARCH-02`)

| State | Owner | Rule |
|---|---|---|
| Server resources | TanStack Query | Key factory per entity; invalidate exact detail + affected lists on mutation; events patch only version-matching records else invalidate |
| Shareable view (filters, focus, lens, time, layout, selection id) | URL search params (typed, validated with Zod) | Sensitive text (query text, PII) never in URL; graph camera encoded as 3 rounded numbers |
| Transient UI (open panels, hover, drag) | Zustand | reset on route family change and scope change |
| Lifecycles | XState | ingestion/publish/query/upload only |
| Local durable drafts/views | Dexie | namespaced; TTL 30 days; purge on logout |
| Graph model | Graphology instance per canvas | single source; renderer attributes separate from domain data |
| Layout | Worker | versioned requests; stale results rejected; cancel on scope change |

### 4.4 Scope generation protocol (`GUI-ARCH-03`)

On tenant or workspace change: increment `scopeGeneration`; call `api.dispose()` on the old client and create a new one; `queryClient.clear()`; stop polling; clear Zustand slices; purge Dexie caches for the old scope unless the scope is pinned as "remembered"; reject any response tagged with the old generation; then hydrate. Test: identical entity IDs in two tenants never bleed across (JRN-01).

### 4.5 Build and environment

`VITE_API_BASE` (default `''` same-origin), `VITE_DEPLOYMENT_MODE` ∈ `local|distributed|cloud` (display only), `VITE_BUILD_ID`, `VITE_FEATURE_MANIFEST_URL` (optional). No model/tenant policy flags in the client — those come from the server. Production build fails if any `msw` import or `BACKEND-MISSING` mock handler is reachable (`scripts/check-no-mocks.mjs`). `vite.config.js` route-splits: graph engine, Monaco, Tiptap, React Flow, ECharts modules, each admin family.

---

## 5. Design System

### 5.1 Visual direction

**Evidence Atlas** (recommended direction A in GUI-UIX §2): light-first neutral canvas, graphite text, teal interaction colour, amber for evidence/paths, red strictly for risk/danger. Dense information kept calm: 1 px borders, 4/6 px radii, no shadows except overlays, no gradients, blur, glass, orbs or hero banners. Dark mode is an alternate palette of the same system, not a different aesthetic.

### 5.2 Colour tokens (exact)

| Token | Light | Dark | HC Light | HC Dark |
|---|---|---|---|---|
| `color.canvas` | `#F7F9FA` | `#101518` | `#FFFFFF` | `#000000` |
| `color.surface` | `#FFFFFF` | `#172025` | `#FFFFFF` | `#000000` |
| `color.raised` | `#F1F4F5` | `#202B31` | `#F2F2F2` | `#121212` |
| `color.text` | `#172126` | `#F2F6F7` | `#000000` | `#FFFFFF` |
| `color.text.muted` | `#52636B` | `#AEC0C7` | `#1A1A1A` | `#E6E6E6` |
| `color.border` | `#CBD5D9` | `#43545C` | `#000000` (2 px) | `#FFFFFF` (2 px) |
| `color.focus` | `#087F8C` | `#4DD5DF` | `#0000FF` (3 px) | `#FFFF00` (3 px) |
| `color.brand` | `#006D77` | `#43C3CC` | `#004B52` | `#7FE3EA` |
| `color.accent` (evidence/path) | `#D97706` | `#F5A623` | `#8A4B00` | `#FFC46B` |
| `color.success` | `#16805A` | `#4BC38B` | `#005A3C` | `#6FE0A8` |
| `color.warning` | `#A15C00` | `#FFC857` | `#6B3D00` | `#FFD98A` |
| `color.danger` | `#C33241` | `#FF6673` | `#8E1F2B` | `#FF8F99` |
| `color.info` | `#1769AA` | `#67B7F7` | `#0E4C7F` | `#9BD0FF` |
| `color.selection.bg` | `#E3F2F3` | `#1E3A3E` | `#D0D0FF` | `#333300` |

Graph tokens: `graph.node.default #5F7480`, `.hover #21A5B1`, `.selected #006D77` + 3 px halo (white light / black dark), `.dimmed` alpha .16; `graph.edge.default #80939B`, `.hover #087F8C`, `.selected #D97706`; `graph.path #D97706`; `graph.hull` alpha .12; `graph.grid #DDE5E8` / `#2C3940`; impact `LOW #2A9D8F · MEDIUM #E9C46A · HIGH #F4A261 · CRITICAL #C33241`. Fact-class tokens per §2.2.

Contrast gates (`GUI-DS-01`): body text ≥ 4.5:1; large text/icons/graph labels ≥ 3:1; focus ring ≥ 3:1 against adjacent colours; verified by an automated token test over every fg/bg pair actually used.

### 5.3 Categorical palette for entity labels (`GUI-DS-02`)

Seed: Okabe-Ito (8 colours) assigned to the 8 most frequent domains; further labels use deterministic golden-angle OKLCH hue rotation at L=.68/C=.13 keyed by `hash(label)`. Shape/icon is always the primary encoding (§5.6), colour secondary. Stewards may override a label colour (SCR-023) only if contrast validation passes. Sequential scales: viridis. Diverging: blue–white–red with neutral midpoint. Ship deuteranopia/protanopia/tritanopia simulation in Storybook and a `Colour-vision safe` toggle in Settings that swaps to the Okabe-Ito-only + pattern mode.

### 5.4 Typography

Inter (bundled, local) → system UI fallback; Noto Sans (Indic/CJK/Arabic subsets bundled on demand); JetBrains Mono → system mono. Scale: 12/16, 14/20, 16/24, 20/28, 24/32, 32/40 (size/line-height); weights 400/500/600/700; tabular numerals for all metrics (`font-variant-numeric: tabular-nums`); letter-spacing 0; no uppercase-tracked micro labels. One-line labels truncate with tooltip; IDs use middle ellipsis (`GUI-COMP-20 MiddleEllipsis`); prose wraps.

### 5.5 Spacing, shape, elevation, layers, density

- Spacing base 4 px: `1=4, 2=8, 3=12, 4=16, 5=20, 6=24, 8=32, 10=40, 12=48`.
- Control heights: 24 (dense chips), 28, 32 (default), 36, 40, 48 (primary CTA on auth only).
- Radii: 2 (chips), 4 (inputs/buttons), 6 (menus/cards), 8 (dialogs max). Never larger.
- Borders 1 px (`2 px` in HC). Shadows only on popover/menu/dialog/toast: `0 4px 16px rgba(23,33,38,.12)`.
- Z-index: canvas 0 · sticky 10 · dock 20 · inspector 30 · popover 40 · modal 60 · toast 80 · skip-link 90.
- Density: `comfortable` 44 px rows, `default` 36 px, `compact` 28 px (minimum target still 24×24 CSS px; compact adds padding to hit targets).

### 5.6 Iconography (`GUI-DS-03`)

Lucide only, sizes 12/16/20/24/32, stroke 1.75, optically centred in a square box; icon-only controls require `aria-label` + tooltip; unfamiliar/destructive actions pair icon with text.

**Action registry (name → Lucide):** search→`search`, filter→`filter`, clear-filter→`filter-x`, expand→`expand`, collapse→`minimize-2`, fit→`maximize`, fit-selection→`focus`, zoom-in/out→`zoom-in`/`zoom-out`, layout→`layout-grid`, legend→`list`, minimap→`map`, pin→`pin`, unpin→`pin-off`, hide→`eye-off`, show→`eye`, isolate→`crosshair`, undo/redo→`undo-2`/`redo-2`, save→`save`, save-view→`bookmark`, share→`share-2`, copy→`copy`, copied→`check`, download/export→`download`, upload→`upload`, import→`file-input`, print→`printer`, run→`play`, stop→`square`, pause→`pause`, resume→`play`, cancel→`ban`, retry→`rotate-ccw`, refresh→`refresh-cw`, replay→`repeat`, readmit→`redo-dot`, settings→`settings`, help→`circle-help`, keyboard→`keyboard`, notifications→`bell`, activity→`activity`, warning→`triangle-alert`, error→`circle-x`, success→`circle-check`, info→`info`, evidence→`file-check`, provenance→`git-branch`, path→`route`, impact→`radar`, blast→`target`, time→`history`, compare→`git-compare`, diff-added→`plus`, diff-removed→`minus`, diff-changed→`delta` (Lucide `triangle` rotated) → use `diff`, approve→`check-check`, reject→`x`, lock→`lock`, unlock→`lock-open`, permission→`shield-check`, denied→`shield-x`, tenant→`building-2`, workspace→`folder-kanban`, user→`user`, users→`users`, agent→`bot`, model→`cpu`, local-only→`house-lock`, external→`globe-lock`, job→`list-checks`, source→`plug`, connector→`cable`, database→`database`, ontology→`shapes`, schema→`network`, table-view→`table`, tree-view→`list-tree`, graph-view→`waypoints`, chart→`chart-column`, timeline→`chart-gantt`, report→`file-text`, template→`file-code-2`, more→`ellipsis`, drag→`grip-vertical`, close→`x`, back→`arrow-left`, forward→`arrow-right`, external-link→`external-link`, abstain→`circle-slash`, simulated→`flask-conical`, deterministic→`badge-check`, inferred→`sparkles`, human→`user-check`, trust→`gauge`, freshness→`clock`.

**Domain glyphs (vertex label → Lucide; shape used in canvas):** WORK: WorkItem `ticket` (rounded square), Project `folder` (square), Epic `mountain`, Feature `puzzle`, UserStory `book-open`, Sprint `timer`, Version `tag`, Comment `message-square`, Requirement `clipboard-list`, IssueType `shapes`, Status `circle-dot`, WorkItemChange `pencil-line`; CODE: Repository `git-fork` (hexagon), Branch `git-branch`, Commit `git-commit-horizontal` (circle), File `file-code` (diamond), CodeSymbol `braces` (triangle), Dependency `package` (pentagon), Service `server` (rounded hexagon), Database `database` (cylinder → use circle with inner line), APIService `plug-zap`, APIEndpoint `route`, APIConnection `link-2`; CICD: MergeRequest `git-pull-request`, PipelineRun `workflow`, Job `list-checks`, Artifact `box`, Deployment `rocket`, Release `package-check`, BuildRecord `hammer`, Tag `tag`; KNOWLEDGE: Document `file-text` (square), DocumentSection `text`, KnowledgeSpace `library`, KBArticle `book`, ProdPage `panel-top`, KnowledgeProduct `gem`; IDENTITY: Person `user` (circle), Organization `building-2`; OPS: Incident `siren`, ChangeRequest `file-diff`, ServiceRequest `inbox`, Dashboard `layout-dashboard`, MonitorRule `monitor-check`, AlertEvent `bell-ring`, Metric `gauge`, LogAggregate `scroll-text`; TEST: TestCase `flask-round`, TestSuite `folder-check`, TestCycle `refresh-ccw-dot`, TestRun `play-circle`; DESIGN: DesignFile `figma`→ use `pen-tool`, DesignPage `layout-template`, DesignComponent `component`; DECISION: Decision `scale`, Alternative `split`, DecisionOutcome `flag`; PROCESS: ProcessFlow `workflow`, ProcessStep `footprints`, ProcessEvent `zap`; BUSINESS: BusinessObjective `goal`, BusinessCapability `blocks`; META: DataSource `plug`, IngestionRun `download`, GraphDomain `layers`, OntologyVersion `shapes`, Evidence `file-check`, ValidationRun `shield-check`, ValidationFinding `triangle-alert`, EntityRevision/RelationshipRevision `history`, GraphVersion `git-commit-vertical`, SemanticChange `diff`; AGENT: AgentRun `bot`; INTEGRATION: GenericEntity `circle`. Unknown label → `circle-dashed` + domain colour. The registry is data (`design-system/icons/registry.ts`) and unit-tested so that every label returned by `GET /api/v1/graph/schema` resolves to an icon (fallback counted and reported).

### 5.7 Illustrations and empty-state art

Sparse single-colour line art (`color.text.muted` at 60 %), ≤ 96 px, domain-neutral (dots/lines/document shapes). No people illustrations, no mascots, no marketing copy. Empty states: one sentence of fact (`No sources are registered in this workspace.`) + one primary action + optional secondary link to `/help`.

### 5.8 Motion tokens (`GUI-DS-04`)

| Token | Value |
|---|---|
| `motion.instant` | 0 ms |
| `motion.micro` | 100 ms (hover/focus colour) |
| `motion.short` | 160 ms (route crossfade, panel slide ≤ 12 px, menu open) |
| `motion.medium` | 240 ms (dialog, inspector resize settle) |
| `motion.long` | 400 ms (camera fly-to minimum) |
| `motion.graph` | 600–1200 ms (layout interpolation, scaled by element count) |
| `ease.standard` | cubic-bezier(.2,0,0,1) |
| `ease.emphasized` | cubic-bezier(.2,.8,.2,1) |
| `ease.accelerate` | cubic-bezier(.4,0,1,1) |
| `ease.decelerate` | cubic-bezier(0,0,.2,1) |
| `spring.panel` | stiffness 320, damping 30 |

Rules: animate only `transform`/`opacity`; stagger ≤ 6 items × ≤ 30 ms; skeleton→content dissolve 120 ms; press scale .98 (off in reduced motion); ≤ 200 simultaneously animated elements; graph animations off above 10 000 elements; edge-draw animation only below 2 000 edges; no autoplay; `prefers-reduced-motion` and the user setting replace morph/fly/ripple/draw with instant final state plus a live-region announcement. Every animated component consumes `useMotionTokens()`; raw durations in code are a lint error.

### 5.9 White-label variables (`GUI-DS-05`)

Tenant brand pack (from `GET /api/v1/branding/theme?tenant_id&mode`) may set: product name, logo (light/dark), favicon, brand & accent colours, optional display font (bundled, licensed), login side image, legal content kind strings, terminology renames (`POST /branding/terminology/*`), assistant name. It may **never** set semantic colours (success/warning/danger/info), fact-class colours, focus colour, contrast below gates, or hide "powered by" unless `licensing` says de-vendoring is licensed (SR-WL-004). Theme application is atomic: tokens swap in one frame after the whole pack validates; on failure the previous valid pack remains and SCR-023 shows the validation error.

---

## 6. Application Shell, Navigation and Keyboard Model

### 6.1 Shell geometry (`GUI-SHELL-01`)

```
┌──────┬──────────────────────────────────────────────────────────────────────────────┐
│ Rail │ Context bar (48 px): [☰] Tenant ▾ / Workspace ▾ › Breadcrumb … [Search ⌘K] [Mode ▾] [Live●] [🔔] [?] [👤] │
│56 px ├──────────────────────────────────────────────────────┬───────────────────────┤
│      │                                                      │ Inspector             │
│ ◆    │  Primary work surface                                │ 320–480 px, resizable │
│ ◆    │  (toolbar row 40 px + surface)                       │ tabs; close ⌥]        │
│ ◆    │                                                      │                       │
│ ◆    │                                                      │                       │
│ ◆    ├──────────────────────────────────────────────────────┴───────────────────────┤
│ ◆    │ Dock (collapsed 32 px / open 240–480 px): Jobs │ Query output │ Events │ Console │
└──────┴──────────────────────────────────────────────────────────────────────────────┘
```

- Rail: 56 px, icon-only with tooltip; expands to 240 px labelled drawer on hover-intent (300 ms) or `Alt+/`; ≤ 7 group icons + bottom Settings/Help.
- Context bar: 48 px; left: menu toggle (tablet), tenant/workspace switcher (always visible, even single-tenant: shows name + lock icon when bound), breadcrumb of object hierarchy; right: global search (`/`), Mode segmented (Simple/Advanced/Expert, hidden in Simple → shown as single "Advanced" button), Live indicator (`polling`/`live`/`paused`/`error`), notifications bell with count, help, account menu (principal name, roles chips, `Deployment access (bootstrap token)` label when applicable, sign out).
- Work surface: full remaining area; graph surfaces are full-bleed (no card frame).
- Inspector: right, 320–480 px (persist per principal/workspace), closable, `Alt+]`; overlay sheet on tablet; on ≥ 2560 px a second inspector may dock.
- Dock: bottom, 32 px collapsed strip with live counts (`3 running · 1 held`), open 240–480 px; tabs Jobs / Query output / Events / Console (Expert); `Alt+[`.
- Status strip (inside dock collapsed bar): backend chip (`hugegraph · ready`), graph counts (`12 480 vertices · 58 211 edges · as of 12:04:31`), knowledge age for the current view.

### 6.2 Navigation groups and destinations (`GUI-SHELL-02`)

| Rail group (icon) | Destinations (route) | Visible when |
|---|---|---|
| Overview (`layout-dashboard`) | SCR-003 `/t/:tenant/w/:workspace` | always |
| Explore (`waypoints`) | SCR-004 `/ask`, SCR-005 `/graph`, SCR-013 `/meta-graph`; context: SCR-006 `/entity/:id` | always |
| Investigate (`radar`) | SCR-007 `/impact`, SCR-008 `/changes`, SCR-009 `/incidents` (+`/:id`), SCR-010 `/time`, SCR-011 `/query` | always |
| Build data (`database`) | SCR-014 `/sources`, SCR-015 `/ingestion`, SCR-016 `/quality`, SCR-012 `/ontology`, SCR-017 `/jobs` | always (mutations gated by role) |
| Work together (`users`) | SCR-018 `/agents`, SCR-019 `/reports`, SCR-020 `/collaboration` | always |
| Govern (`shield-check`) | SCR-021 `/t/:tenant/admin/governance`, SCR-023 `/t/:tenant/admin/brand`, SCR-022 `/platform/tenants/:tenant`, SCR-024 `/platform/health` | role `admin|system` (server still enforces) |
| Personal (bottom) | SCR-025 `/settings`, SCR-026 `/notifications`, `/help`, `/about` | always |

Persona (§1.2) only reorders groups (e.g. Steward puts Build data second). Unknown route → SCR-027 `/errors/404` with search. `/app`, `/admin`, `/studio`, `/cognitive`, `/dashboards`, `/demo` legacy paths redirect to their new destinations (redirect map in `app/router/legacy-redirects.ts`) after scope validation.

### 6.3 Breadcrumb and object hierarchy

`Tenant › Workspace › Screen › Object` (e.g. `Acme › default › Entity › PAY-142`). Each crumb is a link; the last is the page `<h1>`. Route title format: `<Object or Screen> · <Workspace> · <Product>`; announced once on navigation via live region; focus moves to `<h1>`.

### 6.4 Responsive behaviour (`GUI-SHELL-03`)

| Width | Rail | Inspector | Dock | Notes |
|---|---|---|---|---|
| ≥ 3440 | expanded labels | docked + optional second | docked | text columns max 80 ch; graph full bleed |
| 2560–3439 | expanded labels | docked (+ second allowed) | docked | |
| 1920–2559 | icons | docked | docked | |
| 1280–1919 | icons | docked (collapses labels in rail) | collapsed by default | |
| 768–1279 (tablet) | hidden → ☰ drawer | overlay sheet (one) | overlay sheet | single column lists |
| < 768 (mobile) | bottom tab bar (Overview, Ask, Notifications, Approvals-read-only) | full-screen sheet | n/a | **read-only companion**: answers, entity summary, jobs, notifications; graph shows accessible table; every mutation shows `Not available on mobile` |

Container queries drive panel internals. Persist panel sizes; clamp on viewport change. Reflow at 400 % zoom without horizontal page scroll (graph canvas and tables own their scroll).

### 6.5 Global search (`/`)

Single input in the context bar. Typeahead after 2 chars (debounce 250 ms): calls `GET /api/v1/search?q=&limit=10` and, in Advanced/Expert, `POST /api/v1/search/faceted {query, limit:10}` for facets. Results grouped by domain then label; each row: icon+label chip, name, middle-ellipsis canonical ID, trust ladder, freshness age, `why` line (from faceted `hit.why` when available). Enter → open SCR-006; `Shift+Enter` → add to Graph Explorer; `Alt+Enter` → Ask with the entity pinned. Shows `Showing first 10 of ≥10 (server cap 100)` honestly. Empty: `No entities match "<q>" in <workspace>`. Error: inline problem with correlation ID.

### 6.6 Command palette (`Ctrl/⌘+K`) (`GUI-SHELL-04`)

`cmdk` dialog with sections: Navigate (27 destinations filtered by capability), Actions for current selection (Inspect, Expand, Impact, Path to…, Lineage, Why?, What changed?, What if removed?, Save view, Export…), Recents (last 20 objects per scope, Dexie), Favourites, Lenses (20 from catalog), Switch tenant/workspace, Theme/density/mode toggles, Help & shortcuts. Each command shows its shortcut. Commands that need a missing backend show `Unavailable: <reason>` and are not executable.

### 6.7 Keyboard map (`GUI-SHELL-05`, rebindable in Settings, disabled inside text editors unless scoped)

Global: `Ctrl/⌘+K` palette · `/` search · `?` shortcut help · `g o` Overview · `g a` Ask · `g g` Graph · `g e` Entity (current) · `g i` Impact · `g c` Changes · `g n` Incidents · `g t` Time · `g q` Query · `g s` Sources · `g j` Jobs · `g r` Reports · `Alt+]` inspector · `Alt+[` dock · `Alt+/` rail drawer · `Esc` cancel mode/close overlay · `Ctrl/⌘+,` settings.
Graph: arrows traverse neighbours (ordered by label then name) · `Enter` inspect · `Shift+Enter` expand · `Space` select/deselect · `f` fit · `Shift+f` fit selection · `l` layout picker · `t` table view · `m` minimap · `h` hide selected · `Shift+h` unhide all · `p` pin · `e` expand 1 hop · `[`/`]` previous/next in path · `1–9` switch lens (listed order) · `Ctrl+z`/`Ctrl+Shift+z` undo/redo · `Shift+drag` lasso · `Ctrl+Shift+drag` rectangle.
Tables: APG grid pattern (arrows, Home/End, PageUp/Down, `Ctrl+Home/End`), `Enter` open row, `Space` select, `Shift+Space` select row range.
Streams: `Esc` stop generation.

### 6.8 Activity tray and notifications

Bell shows unread count from `GET /api/v1/platform/notifications/inbox/{principal}?unread_only=true&limit=50`; popover lists newest 10 with category icon, relative time, deep link; "Mark read" → `POST …/{id}/read`. Dock Events tab shows polled graph events (§3.9) grouped per §2.13 with filter chips and pause/resume. Long-running jobs started from any screen appear in the dock and toast on terminal state (`Job <kind> succeeded · View`), including after navigating away.

### 6.9 Mode behaviour summary (`GUI-SHELL-06`)

| Surface | Simple | Advanced | Expert |
|---|---|---|---|
| Context bar | no Mode control shown except a single `Advanced` button | segmented control | segmented + backend chip + Console tab |
| Graph toolbar | search, expand, fit, lens, table | + filters, layouts, overlays, export | + algorithm runner, raw QueryPlan |
| Ask | composer + mode badge + evidence | + suggestion cards, QueryPlan/cost preview, approach/loop selectors | + raw request/response JSON, tier/tokenizer tools |
| Inspector | Overview, Relationships, Evidence | + Impact, Similarity, History | + Raw JSON, Operators (WHY/WHY NOT/…) |
| Forms | required fields only | optional fields | JSON editor fallback |

---

## 7. Shared Component Library (`GUI-COMP-*`)

Every component: typed props; controlled/uncontrolled explicit; states default/hover/focus-visible/active/selected/disabled/loading/error/read-only/empty where applicable; WAI-ARIA APG pattern named in its story; motion via §5.8; tokens via §5; Storybook story per state with realistic extremes (long Unicode names, 0/1/many, RTL); unit + a11y test. No "mega components" with unrelated flags.

| ID | Component | Spec |
|---|---|---|
| COMP-01 | `Button` / `IconButton` / `SplitButton` | variants primary/secondary/quiet/danger; sizes 28/32/36/40; `loading` keeps width and shows inline spinner + `aria-busy`; icon-only requires `aria-label` and renders `Tooltip` |
| COMP-02 | `TextField`, `NumberField`, `SecretField` (reveal toggle, never autocompletes, paste allowed), `TextArea`, `Select`, `AsyncCombobox` (debounced server search, keyboard APG combobox), `ChipMultiSelect`, `DateTimeField`/`DateRangeField` (UTC on wire, user zone shown, zone label visible), `Slider`/`RangeSlider` (time), `Toggle`, `Checkbox`, `SegmentedControl` | visible label, help text, error text linked by `aria-describedby`; validate on blur + submit; server pointer→field mapping |
| COMP-03 | `Tabs` (APG tabs; lazy panels), `Accordion`, `Breadcrumbs`, `LazyTree` (virtual, APG treeview, async children), `Pagination`/`LoadMore` (shows server cap), `CommandPalette`, `RecentsList` | |
| COMP-04 | `DataGrid` (TanStack Table + Virtual): sort, filter, group, pin columns, column chooser (persisted per scope), row selection, inline edit (where endpoint exists), density, export CSV (respects filters + permission), ARIA grid, row count/position announced, > 100 rows virtualized | empty/error rows inside grid; sticky identity/status/actions columns |
| COMP-05 | `EntityCard` (icon, label chip, name, ID ellipsis, trust ladder, freshness, fact badge), `EntityHoverCard` (300 ms delay; fetches `GET /entities/{id}` once; keyboard reachable via `Enter` on focused chip), `RelationshipChip` (type, direction arrow, fact-class style), `PropertyList` (type-aware: ISO dates → localized with raw on hover; URLs → safe links (http/https only, rel noopener); code refs → mono; long text → expandable) | masked fields render `••••` with lock icon and reveal only if server returns value |
| COMP-06 | `JsonViewer` (collapsible, copy, search, never executes), `DiffViewer` (side-by-side/inline, added/removed/changed with +/−/Δ symbols and colours) | |
| COMP-07 | `StatusPill` (maps §2.1/§2.7 enums → colour+icon+label; unknown → neutral with raw text), `FactBadge` (§2.2), `TrustLadder` (§2.3), `FreshnessStamp` (`as of 12:04 · 6 min ago`, warns > SLO), `ModeBadge` (§2.4), `BoundaryBadge` (§2.5), `RiskTierBadge` (§2.6), `AbstainBadge` | never colour-only |
| COMP-08 | `Skeleton` (structure-shaped, 120 ms dissolve), `Spinner` (only for < 400 ms indeterminate), `Progress` (determinate/indeterminate/job with ETA only when server provides timings), `Toast` (80 z, 6 s, pause on hover, action button, `role=status`), `InlineAlert`/`Banner` (info/warning/danger/success with icon + title + detail + correlation ID copy), `EmptyState`, `ErrorState` (problem → §8.3), `OfflineState` (capture age), `DeniedState` (needed capability, no object disclosure), `StaleState` (refresh action), `MissingBackendState` (contract ID, "Not available in this deployment") | |
| COMP-09 | `Tooltip` (portal, 300 ms hover / 0 ms focus, `aria-describedby`, Esc closes), `Popover`, `Dialog` (focus trap/restore, inert background, Esc, `aria-modal`), `Drawer` (right/bottom), `Sheet` (tablet/mobile), `ConfirmDialog` (impact summary + typed confirmation when `severity='high'`), `ContextMenu` (APG menu; keyboard `Shift+F10`) | |
| COMP-10 | `Stepper` (linear/non-linear, current step only visible + compact trail, resumable from XState snapshot), `Uploader` (drag/drop, file list, accept from `GET /connectors/files/formats`, 3 MB client cap with message, octet-stream POST, progress, cancel; chunked/resumable is `BACKEND-MISSING-011` → shown as disabled "Resumable upload not available"), `FilterBuilder` (AND/OR groups; field from schema; operators = ≠ > < contains regex in; produces `QueryPlan.filters`), `CodeEditor` (Monaco lazy; read-only mode; dialect syntax), `RichTextEditor` (Tiptap lazy; sanitized HTML output; no raw HTML paste), `FlowEditor` (React Flow wrapper with keyboard alternatives: node palette list, "Connect A → B" command) | |
| COMP-11 | `StreamingAnswer` (token append, caret, Stop/Regenerate, mode badge, boundary badge, `aria-live=polite` with 1 s batching), `CitationChip` (`[n]` → evidence; hover/focus highlights graph node/edge & source span), `ConfidenceMeter` (shows value + `inputs` list; never shown without inputs; `confidence_score < .7` shows `uncertainty_reason`), `SuggestionCard` (§11.2), `EvidenceManifestPanel`, `AbstainNotice` | |
| COMP-12 | `GraphCanvas`, `GraphToolbar`, `LayoutPicker`, `Legend` (schema-driven; click toggles label; shows counts), `Minimap` (200×150, viewport rect, click-to-navigate), `TimelineScrubber` (dual handle + histogram), `LensSwitcher`, `PathBreadcrumb`, `GraphTableView`, `GraphTreeView`, `ClusterHull`, `ImpactRings` | §10 |
| COMP-13 | `NotificationItem`, `PresenceAvatars` (only when `BACKEND-MISSING-016` exists; else hidden), `CommentThread` (hidden until backend), `ApprovalCard` (exact target, changed fields, risk tier, expiry, approve/reject with reason), `RemediationBoard` (Kanban via dnd-kit with keyboard move), `JobLog` (virtualized, bounded 5 000 lines, copy, filter), `ActivityTray` | |
| COMP-14 | `ScopeSwitcher` (tenant/workspace; shows lock when principal is tenant-bound; search; recent) | |
| COMP-15 | `KnowledgeAgeStamp` (SR-ING-051: every answer/result header shows `Knowledge as of <time> · source lag <n>` when `freshness`/`last_seen`/`as_of` present; else `Knowledge age unknown`) | |
| COMP-16 | `ResultBanner` (renders `partial:true` → "Partial result: <warnings>"; `warnings[]` list; `truncated_*`) | |
| COMP-17 | `CorrelationId` (mono, middle ellipsis, copy; present in every error, every job row, every answer footer) | |
| COMP-18 | `KpiTile` (value with tabular nums, unit, as-of stamp, trend sparkline only with ≥ 3 points, `N/A` state; never a coloured ring without denominator) | |
| COMP-19 | `DimensionGauges` (five separate 0–100 gauges; refuses to render an aggregate) | R9 |
| COMP-20 | `MiddleEllipsis` (CSS + measured; full value in tooltip and copy) | |
| COMP-21 | `OperatorMenu` (WHY / WHY NOT / WHAT IF / WHAT CHANGED / WHEN / WHO / WHERE / HOW → mapped endpoints §3.3; disabled with reason when unavailable) | |
| COMP-22 | `CapabilityGate` (wraps any control; props `requires: {role?, backend?: 'INT-xxx'|'BACKEND-MISSING-xxx', capability?}`; renders disabled + reason tooltip; never hides discoverable controls, hides only undiscoverable objects) | R2/R3 |

---

## 8. Shared Interaction Patterns

### 8.1 Universal screen states (`GUI-PAT-01`)

Every screen and every independently loadable region implements and tests: `first-run`, `loading` (skeleton), `empty`, `partial` (some sections failed; others render), `populated`, `validation-error`, `transport-error`, `server-error` (problem), `offline-cached` (capture age), `permission-denied`, `stale` (data older than SLO or event gap), `backend-missing` (disabled with contract ID), `cancelled`. A failed region never blanks sibling regions.

### 8.2 Loading and freshness

Skeleton when structure is known; spinner only for sub-400 ms indeterminate commands; `aria-busy` on the region; dissolve 120 ms. Lists: stale-while-revalidate 30 s; a `FreshnessStamp` shows fetch time. Graph counts in the status strip show `as of`. Event gap (`since_id` jump > buffer) → `StaleState` with Refresh.

### 8.3 HTTP → UI mapping (`GUI-PAT-02`)

| Status / condition | UI |
|---|---|
| 200 with `partial:true` | render + `ResultBanner` warning |
| 200 with body `status: PARTIAL|FAILED` (file parse, jobs) | treat as warning/error per body, not success |
| 201/202 | toast `Accepted` + dock job row (202) |
| 204 | silent success + list invalidation |
| 400 | inline error with `detail` |
| 401 | clear token → SCR-001 with return URL; toast `Session ended` |
| 403 `Administrative role required` / `Cross-tenant access forbidden` / tenant context | `DeniedState` naming the capability (`Requires admin role`), no object details |
| 404 | `Not found in <workspace>` (no existence leak beyond that) |
| 409 | inline conflict with `detail` (e.g. running job cannot be cancelled; readmit only HELD; role exists) |
| 413 | `File/payload exceeds server limit (4 MB)` with client pre-check |
| 415 | `Unsupported content type` |
| 422 (`detail` string) | inline policy/validation error (e.g. PolicyViolation text, unknown label) |
| 422 (`detail` array of `{loc,msg,type}`) | map `loc[-1]` to field; summary links; focus first |
| 429 | `Rate limited — retrying in n s` (GET only) |
| 500/504 problem+json | `ErrorState` with `title`, `detail`, `error.code`, correlation ID copy, Retry (GET) |
| 501 | `MissingBackendState` "Disabled/not configured on this server" |
| 503 | `Service dependency unavailable` (model/parser/audit) with Retry |
| network/timeout | `OfflineState` or `Transport error` with retry; mutations never auto-retry |
| AbortError | silent (cancelled by user/scope change) |

### 8.4 Forms (`GUI-PAT-03`)

RHF + Zod; validate syntax on blur, full on submit; async checks (name uniqueness, policy) debounced 400 ms and ignoring stale responses; error summary at top linking to fields; first invalid field focused; dirty-navigation guard; local draft autosave after 1 s idle into Dexie (only non-secret fields; never credentials), restored with a `Draft restored from <time>` banner; undo/redo as commands; secret fields write-only (`secret_refs` URIs only, per ADR-001). Bulk edits preview affected count. CSV/JSON import shows row-level errors downloadable.

### 8.5 Destructive and high-impact actions (`GUI-PAT-04`)

Class **high**: delete entity (`POST /admin/entities/{id}/delete`), restore snapshot/checkpoint, replace policy set, revoke token, kill switch, tenant suspend/delete, delete source with dependent jobs, ontology publish/rollback, apply migration, DLQ discard, brand publish. Flow: impact preview (fetched where endpoint exists, e.g. what-if, lineage counts) → `ConfirmDialog` with typed canonical name/ID → execute → toast with correlation ID → show restore path if backend supports (tombstone `include_deleted=true`). Class **medium** (cancel job, pause source, reject proposal): single confirm with reason field where API takes one.

### 8.6 Optimistic updates

Only for reversible metadata (pin, favourite, saved view name, local annotations). Everything else waits for the server and shows pending glyph. Rollback with inline reason on failure.

### 8.7 Permission rendering

Discoverable actions render disabled with reason (`CapabilityGate`). Undiscoverable objects (other tenants' data) are never fetched or listed. After a 403 on a previously allowed action, invalidate principal/capabilities and re-render gates.

### 8.8 Notifications and jobs

202 responses create a dock job row immediately (optimistic row with status `PENDING` until first poll). Terminal states toast once. Job rows link to SCR-017 detail. Readmit/cancel follow §2.1 semantics with confirmation.

### 8.9 Copy, export and download

Copy actions announce `Copied <what>` in a live region. Exports include a header/footer stamp: product, tenant, workspace, `as of` time, applied filters, fact-class legend, correlation ID; exports respect active filters and server authorization; a client-only export states `Exported from browser view (not a server artifact)`.

---

## 9. Screen Specifications

Conventions for every screen below: **Route** is under `/t/:tenant/w/:workspace` unless absolute. **Layout** uses the shell of §6.1; wireframes show the primary work surface + inspector + dock usage. **Data** lists the exact endpoints (§3) and which field feeds which UI element. **States** are §8.1 (only screen-specific additions are listed). **AC** are Given/When/Then and each must be an automated test ID. **Evidence** names the real-API journey. **Readiness** states what is blocked and the exact interim behaviour (never a mock).

### SCR-001 — Authentication and tenant entry

- **Route:** `/auth` (sign-in), `/auth/scope` (tenant/workspace selection), `/auth/expired`, `/auth/denied`. Absolute; no shell rail; centered 400 px column on canvas; optional tenant login image left on ≥ 1280 (brand pack) else none.
- **Personas:** all. **Purpose:** establish a bearer credential in memory, derive the principal, select tenant (and workspace when `GUI-BE-021` exists), then enter the workbench.
- **Layout:**
```
┌────────────────────────────────────────────────┐
│ [logo] Product name                            │
│ Sign in                                        │
│ ( ) Local account    ( ) Access token          │  ← SegmentedControl; "Local account" only when GET /api/v1/auth/health is OK
│ Username [__________]                          │
│ Password [__________] (reveal)                 │
│ [ Sign in ]                                    │
│ Identity provider: ready · as of 12:01         │
│ ─────── or ───────                             │
│ Access token [••••••••••] (paste)              │  ← SecretField; label "Deployment access token"
│ [ Continue ]                                   │
│ Notice: tokens stay in this tab's memory only  │
│ API: https://… · build 1a2b3c · Legal          │
└────────────────────────────────────────────────┘
```
- **Data:** `GET /api/v1/auth/health` (enables Local account mode; show status text); `POST /api/v1/auth/login {username,password}` → `{token}`; `POST /api/v1/security/tokens/verify {token}` → principal (`subject`, `roles`, `payload.tenant_id`, `payload.exp`); 401 from verify on a token that nevertheless returns 200 from `GET /api/v1/admin/system` → bootstrap principal (label `Deployment access (bootstrap token)`); `GET /health/ready` (pre-flight; 503 → `Server not ready` state with retry). Scope step: tenant list is **not** provided by any endpoint (`BACKEND-MISSING-002`) → if `payload.tenant_id` present, auto-select and show locked; else show a tenant ID input with recent tenants (Dexie) and validate via `GET /api/v1/tenancy/context` with `X-Tenant-Id` + `X-Principal`; 403 → inline error. Workspace: fixed `default` with notice until `GUI-BE-021`.
- **Interactions:** password manager paste allowed; Enter submits; errors inline; after success route to the return URL (same-origin, allow-listed route tree only) else Overview. Session expiry: `exp` from token → warning toast 2 min before (`Session expires in 2:00 · Sign in again`), on expiry route to `/auth/expired` keeping the draft of the current form in Dexie (non-secret fields).
- **States (extra):** `Identity provider unavailable` (health fails → only token mode), `Server not ready`, `Invalid credentials` (401), `Token rejected` (401), `Tenant forbidden` (403).
- **Keyboard:** fully operable; focus starts on first field; `?` disabled here.
- **Motion:** none beyond field focus (micro).
- **Modes:** n/a.
- **AC:**
  - `GUI-SCR-001-A01` Given a valid local credential, when submitted, then `POST /auth/login` is called, the token is held in memory only (assert `localStorage`/`sessionStorage`/IndexedDB contain no token), and the user lands on Overview with tenant/workspace visible in the context bar.
  - `A02` Given an invalid credential, when submitted, then an inline error with correlation ID appears and no navigation occurs.
  - `A03` Given a tenant-bound token, when the scope step renders, then the tenant is pre-selected, locked, and switching to another tenant is impossible in the UI and returns 403 if forced via URL.
  - `A04` Given an unbound admin token and a tenant ID input, when an invalid ID is entered, then `GET /tenancy/context` 403 is shown inline.
  - `A05` Given an expiring token, when 2 minutes remain, then a warning is shown; when expired, then all in-flight requests abort, caches clear, and `/auth/expired` is shown with the return URL preserved.
  - `A06` Given sign-out, when confirmed, then token, Query cache, Dexie scoped caches and polling are cleared and the WS/poll loop stops.
  - `A07` Given `GET /health/ready` 503, when the page loads, then `Server not ready` with retry is shown and no login POST is attempted.
- **Evidence:** JRN-01 real-API; network trace shows no token in URL/storage; screenshot set.
- **Readiness:** `BACKEND-MISSING-001` (OIDC/PKCE/MFA/cookies) → no SSO button; a disabled `Single sign-on` control reads `Not available in this deployment (BACKEND-MISSING-001)`. `BACKEND-MISSING-002` → principal derived as above and the context bar shows the derivation source in Expert mode.

### SCR-002 — First-run onboarding

- **Route:** `/t/:tenant/onboarding` (also reachable as "Set up this workspace" from Overview empty state). Shell present; work surface shows one step at a time with a compact progress trail (8 steps).
- **Personas:** Admin, Steward. **Purpose:** connect → authenticate → scope → discover → preview → map → dry run → validate → baseline → first question (G2-EKAF-030 + SR-UX-010 unified).
- **Layout:** left 240 px vertical trail (step name, status pill, skip reason), center form/review region, right inspector shows the live job for the current step; dock shows jobs.
- **Steps and data:**
  1. *Choose connector* — `GET /api/v1/connectors/catalog` cards (icon, name, type, capability chips); search; selecting opens step 2.
  2. *Connect & authenticate* — form from `SourceRegistryEntry` (§3.6.1): `source_id` (slug, validated unique against `GET /sources`), `name`, `source_type` (fixed), `base_url`, `acquisition_modes` (chips from catalog capabilities), `secret_refs` (URI inputs only; helper text "Reference like `env://JIRA_TOKEN`; raw secrets are rejected by the server"), `polling_frequency_seconds`, `freshness_slo_seconds`. Save → `POST /api/v1/sources` (201). Admin role gate.
  3. *Scope* — `allowed_scopes`/`excluded_scopes` chips; for crawler type show crawl-scope fields (hosts, path prefixes, excluded patterns, max depth/pages, content types, size limits, concurrency) from `config{}` (G2-EKAF-019) → `PATCH /sources/{id}`.
  4. *Discover* — `POST /sources/{id}/discover` → render discovered record types/counts as a table; failures inline.
  5. *Preview & map* — `POST /api/v1/ingest/profile {dataset, records}` on a discovery sample (if available) → `ProfileReport.fields` table (name, type, null %, examples), `POST /ingest/profile/keys` candidates, `POST /ingest/profile/relationships` candidates with confidence (fact badge Inferred); mapping grid: source field → ontology label/property (options from `GET /graph/schema`); mapping version text.
  6. *Dry run* — `POST /sources/{id}/dry-run` (202) → job in inspector; when SUCCEEDED/PARTIAL show proposed mutation counts from job `result` (vertices/edges to add/update; rejected count) and a `DiffViewer` if the result contains samples; PARTIAL shows rejected reasons.
  7. *Validate & baseline* — `POST /api/v1/admin/validation` (optional, admin) and `POST /sources/{id}/baseline` (202) → job; show counts on completion; FAILED keeps the step open with error + retry.
  8. *First question* — embedded Ask composer (SCR-004 component) pre-filled with a suggested question built from the discovered labels (e.g. `What implements <first WorkItem>?`); success closes onboarding.
- **Persistence:** wizard state (XState snapshot, non-secret) in Dexie keyed by scope; `BACKEND-MISSING-003` server state missing → banner `Progress is saved on this device only`. Completion is derived from real resources (source exists + baseline job SUCCEEDED/PARTIAL), never from a client checkbox.
- **Interactions:** Back allowed to any completed step; Skip allowed only for Scope/Validate with a required reason; Cancel keeps created source and offers "Delete source" (admin, confirm).
- **AC:**
  - `GUI-SCR-002-A01` Given the catalog loads, when a connector is chosen and the form submitted with a raw secret in `config`, then the server 422 is shown on the field and nothing is saved; with a `env://` ref, `POST /sources` returns 201 and step 3 opens.
  - `A02` Given a dry-run job returns `PARTIAL`, when the step renders, then rejected counts and reasons are shown and the step is not marked complete.
  - `A03` Given a browser refresh mid-wizard, when the route reopens, then the same step and non-secret values are restored with a `Draft restored` banner; secrets are empty.
  - `A04` Given baseline FAILED, when viewed, then the trail shows Failed, the error with correlation ID is visible and Complete is disabled.
  - `A05` Given baseline SUCCEEDED, when step 8 runs a question, then the answer shows evidence from the newly ingested entities (assert at least one citation canonical_id belongs to the new source's run).
- **Evidence:** JRN-02 real-API with a file/JSON connector fixture.
- **Readiness:** `BACKEND-MISSING-003` (server wizard state), `BACKEND-MISSING-011/012` (resumable upload, review endpoint) → review is read-only; accept/reject per inferred relationship is `CapabilityGate`d with reason.

### SCR-003 — Overview (Brain overview)

- **Route:** `/t/:tenant/w/:workspace`. **Personas:** all (layout varies by persona setting). **Purpose:** scannable operational picture + direct entry to Ask/Graph; never decorative KPI cards.
- **Layout (default/engineer):**
```
┌ Ask the brain ───────────────────────────────── [Ask] ┐   ← single-line composer (SCR-004 component), suggestion chips (max 4, from GET /suggest/intents)
├ Knowledge  (as of 12:04) ───────┬ Jobs ────────────────┤
│ 12 480 vertices · 58 211 edges  │ 3 running · 1 held   │   ← KpiTile ×4 (vertices, edges, labels, backend) from /graph/statistics + /admin/stats
│ 75 labels · hugegraph ready     │ [list of 5 newest]   │   ← /admin/jobs (StatusPill §2.1), link → SCR-017
├ Recent changes ─────────────────┼ Health ──────────────┤
│ timeline list (10)              │ graph · model · backup│   ← /enterprise/diff/changes?limit=10 ; /admin/system (status strings verbatim)
├ Saved views & recents ──────────┼ Alerts ──────────────┤
│ chips (Dexie)                   │ findings/unavailable │   ← /ontology/validate?limit=… summary counts by severity; /knowledge/debt summary (by category, not a score)
└─────────────────────────────────┴──────────────────────┘
```
- **Data:** `GET /api/v1/graph/statistics`; `GET /api/v1/admin/stats` (admin only; else hide labels breakdown and show statistics only); `GET /api/v1/admin/jobs` (tenant-filtered); `GET /api/v1/admin/system`; `GET /api/v1/enterprise/diff/changes?limit=10`; `GET /api/v1/ontology/validate?limit=5000` (summary counts by severity; fetched lazily when the Alerts card enters the viewport because it is a heavy call); `GET /api/v1/knowledge/debt`; `GET /api/v1/suggest/intents`; Dexie saved views/recents. Persona layouts reorder/omit cards: Executive: Ask, Knowledge, Alerts (as debt dimensions), Reports recents; Auditor: Changes, Findings, Audit link; Admin: Jobs, Health, Sources health.
- **Rules:** every number carries an `as of` stamp; unknown → `N/A`; each card is an independent region (own loading/error); drill-downs preserve filters (e.g. clicking `1 held` opens SCR-017 filtered `status=HELD`).
- **AC:**
  - `GUI-SCR-003-A01` Given `/admin/system` fails, when Overview renders, then the Health card shows an error with correlation ID while other cards render data.
  - `A02` Given a non-admin principal, when Overview renders, then no `/admin/*` request is issued and admin-only cards are absent (not errored).
  - `A03` Given two tenants with different graphs, when switching scope, then all tiles update and no stale value from the previous tenant is visible at any frame (snapshot after switch shows skeletons then new values).
  - `A04` Given the jobs list contains a `HELD` job, when its chip is clicked, then SCR-017 opens pre-filtered and the row is focused.
  - `A05` Given validation summary has `0` findings, then the card reads `0 findings in last run (as of …)`; given no run exists, then `No validation run yet`.
- **Evidence:** JRN-03 start; two-tenant comparison screenshots.
- **Readiness:** implemented endpoints; no blockers (workspace = default).

### SCR-004 — Ask the Brain

- **Route:** `/ask?aid=` (aid = local answer id). **Personas:** Executive, Analyst, Engineer. **Purpose:** ask in natural language; see candidate interpretations with QueryPlan/cost preview; run deterministic graph query and/or narrated answer; inspect evidence; save/export.
- **Layout:**
```
┌ Composer ───────────────────────────────────────────────────────────┐
│ [Ask about requirements, impact, evidence…            ] [Ask ⏎]      │
│ Pinned: ⟨PAY-142 ×⟩   Boundary: ● Local only   Mode: Advanced        │
├ Suggestions (Advanced+) ─────────────────────────────────────────────┤
│ ▢ "Which code implements PAY-142?"  PATH · depth 6 · est. 120 rows · conf .82 · [Preview plan] [Run] │
│ ▢ "What breaks if authorize_order changes?"  IMPACT · depth 4 · [Preview] [Run]                     │
├ Answer ─────────────────────────────────────────────────── Inspector: Evidence ┐
│ [Deterministic] Knowledge as of 12:04 · 6 min        │ Citations [1..n]      │
│ Direct answer text with [1] [2] citations            │ Graph paths (mini)    │
│ ▸ Evidence & paths  ▸ Assumptions  ▸ Confidence       │ Rules fired           │
│ ▸ Alternatives  ▸ Coverage gaps  ▸ Follow-ups         │ Tool calls (digests)  │
│ [Stop] [Regenerate] [Save] [Report…] [👍/👎 Correct…] │ Confidence inputs     │
└──────────────────────────────────────────────────────┴───────────────────────┘
Dock: Query output (result table/graph of the deterministic query)
```
- **Data flow:**
  1. Submit → `POST /api/v1/suggest/interpret {question, roles, limit:5}` → `candidates` → SuggestionCards (§11.2). In Simple mode auto-run the top candidate only if `confidence ≥ .8`, else show cards.
  2. Run candidate → if candidate carries a `QueryPlan` → `POST /api/v1/query` (deterministic; result to dock + graph mini); else `POST /api/v1/query/nl {question}` → `{interpretation, result, answer, confidence, engine, highlights, followups, warnings}`.
  3. Narration (Advanced+ toggle "Narrate", default on when a local model is `ready` per `/admin/system.model.status`): `POST /api/v1/brain/llm/stream` with `Accept: text/event-stream`, `prompt` = question + serialized evidence (never raw source bodies beyond allowed), `enable_xai:true` → tokens appended; `[DONE]` → finalize; mode badge `Narrated`. If `model.status ≠ ready` → no stream call; badge `Deterministic`; notice `Local model unavailable — showing graph result` (SR-RAG-008). If the server reports simulator tiers → badge `Simulated (not model inference)`.
  4. Evidence: `POST /api/v1/evidence/manifest {answer_id, node_ids, edge_ids, evidence_refs, query_plan}` → manifest panel; `GET /api/v1/retrieval/search` for linked documents when `rag_mode` set.
  5. Save → Dexie (question, plan, result ids, manifest id, time) namespaced; `Report…` → SCR-019 with `ReportContext` prefilled.
  6. Feedback → `POST /api/v1/enterprise/learning/feedback {feedback_type, domain, context, original_output, corrected_output, rating}` with explicit notice `Feedback is recorded for review; it does not train a model automatically`.
- **Depth bar** (SR-NLQ-005): sections Direct answer · Evidence & paths · Assumptions · Confidence/uncertainty · Alternatives · Next actions · Coverage gaps · Follow-ups; collapsed except Direct answer in Simple.
- **Abstain:** if `confidence < .3`, `partial:true` with empty result, or manifest `coverage_score < .3` → `AbstainBadge` and text `Not enough evidence to answer. Try: …followups` (KGR-G-019); never a generated paragraph.
- **Interactions:** `Esc` stops stream (AbortController); Regenerate creates a new local answer id and keeps history list (left rail of answers in Advanced); hovering/focusing `[n]` highlights the node/edge in the dock graph and scrolls the source snippet; pinned entities (SR-NLQ-003/007) add `context.entities`.
- **States (extra):** `Interpreting…`, `Running query…`, `Streaming…`, `Stopped by user (partial)`, `Model unavailable`, `Egress denied` (if boundary says external and policy denies).
- **AC:**
  - `GUI-SCR-004-A01` Given a question, when submitted in Advanced mode, then suggestion cards render each with paraphrase, intent, depth/limit, estimated rows (from `/query/cost` when a plan exists; else `Cost unknown`), confidence and a Preview that shows the exact `QueryPlan` JSON before any execution.
  - `A02` Given a deterministic result, when rendered, then the mode badge is `Deterministic`, the knowledge-age stamp is present, and every factual sentence has ≥ 1 citation chip resolving to a node/edge/evidence id present in the result (test asserts no orphan citations).
  - `A03` Given the local model is `ready`, when Narrate is on, then the first SSE delta renders before `[DONE]` (assert ≥ 2 paint frames between first and last chunk) and Stop aborts the fetch (assert request aborted and partial text retained with `Stopped` state).
  - `A04` Given the model is `unavailable`, when asked, then no `/brain/llm/*` request is made and the notice is shown.
  - `A05` Given `partial:true` with no nodes, when rendered, then `AbstainBadge` appears and no narration is requested.
  - `A06` Given a source snippet containing prompt-injection text, when displayed, then it renders as inert text inside an `Untrusted source content` frame and no tool/action is triggered.
  - `A07` Given Save, when the page reloads, then the answer, plan and manifest reappear from local storage with `Saved on this device` label.
- **Evidence:** JRN-04 real-API with model ready and model stopped runs.
- **Readiness:** `BACKEND-MISSING-005` (durable answers/resume) → no resume after disconnect; `BACKEND-MISSING-017` → boundary badge from `/egress/endpoints` only.

### SCR-005 — Graph Explorer

- **Route:** `/graph?view=&focus=&lens=&layout=&t=&q=&cam=`. **Personas:** Engineer, Architect, Steward, Analyst. **Purpose:** explore bounded, server-returned subgraphs with lenses, filters, path-finding, clustering, overlays; save/restore views; accessible table/tree equivalents. Full spec in §10.
- **Layout:**
```
┌ Toolbar (40 px): [Search entity…] [+Expand ▾] [Lens: Graph ▾] [Layout ▾] [Filters (3)] [Overlays ▾] [Fit] [Table] [Save view ▾] [Export ▾] [⋯] ┐
├─────────────────────────────────────────────────────────────┬ Inspector ─────────────┤
│                                                             │ Entity / Edge / Path   │
│   WebGL canvas (full bleed)       Legend (bottom-left,      │ tabs (SCR-006 compact) │
│                                   collapsible)  Minimap (br)│                        │
│   Path breadcrumb (top-left when a path is active)          │                        │
├ Filter chips row (when active): [Label: File ×] [Fact: Inferred ×] [Reset] ───────────┤
└ Dock: Query output / Events (graph change feed) ──────────────────────────────────────┘
Status strip: 1 240 nodes · 3 118 edges shown · partial · as of 12:04 · layout: ForceAtlas2 (worker)
```
- **Data:** seed by `GET /search?q` or `focus` (`GET /entities/{id}` + `POST /neighborhood`), expand via `POST /neighborhood {max_depth 1..3}`, paths via `POST /path` or `/graph/shortest-paths`, lenses via `POST /lens/{lens_id}`, overlays via `/graph/metrics`, `/graph/cluster`, `/graph/blast-radius`, `/graph/anomalies`, `/graph/orphaned`, `/graph/surprises`; schema/legend via `GET /graph/schema`; as-of via `GET /graph/as-of?at`; events via polling. Saved views: Dexie (`GUI-BE-030`) with export/import JSON; URL encodes shareable state.
- **Interactions:** per §10.6; refusal of oversized expansion comes from server `warnings`/`partial` and the client cap (`DEC-GUI-11`: client refuses to add > 5 000 new elements from one action without explicit "Add anyway (may slow down)" in Advanced+).
- **AC:**
  - `GUI-SCR-005-A01` Given a `focus` id in the URL, when loaded, then the entity and its 1-hop neighbourhood render, the entity is selected and the inspector shows it; refresh restores identical selection/camera (±1 px).
  - `A02` Given a `partial:true` neighbourhood, when rendered, then the status strip and `ResultBanner` state partial and the warnings text.
  - `A03` Given 2 000 visible edges, when a layout runs, then the main thread never blocks > 50 ms (perf trace) because layout runs in the worker; cancelling via scope change discards the result.
  - `A04` Given a saved view, when the API restarts and the view is restored, then stale ids are reported (`3 entities no longer found`) rather than silently dropped.
  - `A05` Given the Table toggle, when pressed, then the same nodes/edges appear in `GraphTableView` with identical selection, and every toolbar action is available via the table's row/context menu.
  - `A06` Given an export (GraphML/GEXF/JSON-LD/CSV), when generated, then it parses with an independent parser in the test and preserves ids, direction, labels, properties, Unicode and fact class.
  - `A07` Given a cross-tenant saved-view import, when applied, then the ids are validated against the current scope and foreign ids are rejected with a count.
- **Evidence:** JRN-03; pixel assertions on real canvas (§14.4); 1k/10k traces.
- **Readiness:** `GUI-BE-030` local saved views; `GUI-BE-023/024` server LOD/aggregation absent → client enforces caps and shows `Showing bounded subgraph` always.

### SCR-006 — Entity 360

- **Route:** `/entity/:id` (id = canonical_id, URL-encoded; path may contain `/`). **Personas:** all. **Purpose:** complete evidence-first view of one entity; the same component (compact) is the Graph inspector.
- **Layout:**
```
┌ Header: [icon] WorkItem · PAY-142  "Tokenize card on checkout"  [Trust ▮▮▮▯▯▯▯ Reviewed] [Fact: Deterministic] Knowledge as of 12:04 │
│ ID urn:eoip:work:item:jira:PAY-142 [copy]   Domain WORK · Source jira · Ingestion run …  [Open in Graph] [Impact] [Lineage] [Ask about] [⋯ WHY/WHAT CHANGED/WHAT IF] │
├ Tabs: Overview · Relationships (42) · Impact · Evidence (7) · Similarity · History · Work · Raw ────────────────────────────────┤
│ (tab panel)                                                                           │ Mini graph (ego, 1 hop) │
└───────────────────────────────────────────────────────────────────────────────────────┴─────────────────────────┘
```
- **Tabs and data (each tab is an independent region; `GUI-BE-031` composition):**
  - Overview — `GET /entities/{id}` → `entity.properties` via `PropertyList` (type-aware; `deleted_at` → tombstone banner "Deleted on … (historical view)"); quick actions.
  - Relationships — `outgoing`/`incoming` grouped by `type` with counts; expandable lists; click → edge inspector; `POST /neighborhood {max_depth:1, result_limit:500}` for more when > returned; chart of type distribution (bar, ECharts); total/in/out degree from `POST /graph/metrics {canonical_ids:[id]}`.
  - Impact — `POST /graph/blast-radius {canonical_id, max_depth:4}` → summary (`total_affected`, `risk` badge with rings), by_depth/by_type bars; `POST /graph/reverse-impact`; centrality radar (5 axes) from metrics; buttons `Explore blast radius` (→ SCR-007 with id) and `Run what-if` (`POST /graph/what-if {action:'remove'}` → broken paths/orphans; label `Simulation — nothing was changed`).
  - Evidence — edges with `properties.source_ref|evidence_key|method`; `POST /lineage {canonical_id}` → provenance chain mini graph; evidence depth = hops to `Evidence`/`IngestionRun` node; source-system diversity count; `Why does this entity exist?` → `GET /query/why/{cid}`.
  - Similarity — `POST /graph/similarity {canonical_id, algorithm, limit:10}` + `/graph/link-prediction` (fact badge Inferred, confidence alpha).
  - History — `GET /enterprise/diff/timeline/{entity_id}` → vertical timeline (event time vs observed time both shown, G2 dual timeline); `GET /graph/versions`; sparkline only with ≥ 3 points.
  - Work — `GET /identity/candidates?status=pending` filtered to this id (duplicate candidates with Decide/Reject (admin) → `POST …/decide|reject {actor_id}`); linked incidents (`GET /platform/incidents?…` filtered client-side by `affected_services` containing id); knowledge product tab when label is `KnowledgeProduct` (`GET /catalog/products/{id}` + `/lineage`).
  - Raw — `JsonViewer` of the full response; copy; linked canonical ids clickable.
  - Delete (admin, Expert/Advanced): `POST /admin/entities/{id}/delete` with high-impact confirm (typed id) and preview from what-if; response `status DELETED|ALREADY_DELETED`, then show `include_deleted` toggle.
- **AC:**
  - `GUI-SCR-006-A01` Given a valid id, when opened, then header, Overview and Relationships render from `GET /entities/{id}`; a failing Impact call shows an error only inside the Impact tab.
  - `A02` Given `deleted_at` set and `include_deleted=false`, when opened, then 404 is shown with a `Show deleted` action that retries with `include_deleted=true` and renders the tombstone banner.
  - `A03` Given 300 outgoing edges, when Relationships renders, then groups are virtualized and counts are exact to the response; `Load more` calls neighborhood with explicit limit and shows server cap.
  - `A04` Given the Delete action, when the typed id mismatches, then Confirm is disabled; when it matches and the server returns `DELETED`, then the page re-fetches and shows the tombstone.
  - `A05` Given navigation Graph → Entity → back, when returning, then the graph camera/selection/filters are unchanged (store snapshot restored).
  - `A06` Given a masked/absent property, when rendered, then `Not provided` vs `Masked` are distinguished by the server response shape (absent key vs masked marker), never guessed.
- **Evidence:** JRN-03/JRN-09 real-API.
- **Readiness:** `BACKEND-MISSING-006` aggregate; `BACKEND-MISSING-013` merge/split/undo → only decide/reject.

### SCR-007 — Impact Analysis studio

- **Route:** `/impact?id=&depth=&mode=static|live|scenario`. **Personas:** Engineer, Architect. **Purpose:** model a change, see blast radius by hop/severity/type, inspect supporting paths, produce an owner/test checklist, export.
- **Layout:** left 320 px *Change definition* panel (entity picker (AsyncCombobox on `/search`), direction Downstream/Upstream, depth 1–8 slider, relationship allowlist chips from schema `edge_labels`, mode segmented Static/Live/Scenario), center concentric-ring canvas (ImpactRings layout; centre = anchor; ring per depth; node colour by risk; size by degree), right inspector *Affected item* (why included: path depth, edge classes, evidence count — GAP P1-11), bottom dock *Checklist* table (affected entity, type, depth, risk, owner (Person via ASSIGNED_TO/AUTHORED_BY if present), tests (`TESTS`/`COVERS` edges), status checkbox (local)).
- **Data:** Static: `POST /graph/blast-radius` + `POST /impact` (paths); Upstream: `POST /graph/reverse-impact`; Live: `POST /causal/live-blast-radius {shock_entities:{id:1.0}, max_depth, failure_threshold, dampening_factor}`; Scenario: `POST /causal/counterfactual-intervention` or `POST /simulation/create` → `…/mutate` → `…/analyze` → `…/compare`; PR impact: `GET /graph/pr-impact`; tests: `POST /graph-tests/run`, `POST /twin/test-intelligence/select`; cost preview: `POST /query/cost` with the equivalent `QueryPlan {intent:IMPACT}`; export: client CSV/Markdown of checklist + `POST /reports/render` (template `impact assessment` if listed).
- **Rules:** show `Preview cost` before depth > 4 runs in Simple/Advanced; progress + Cancel (abort); results marked `partial` when server says so; `Simulation — production graph unchanged` banner in Live/Scenario; severity colours + ring count redundancy; Direct vs Transitive sections (impact categories §2.7 where derivable from edge classes).
- **AC:**
  - `GUI-SCR-007-A01` Given anchor and depth 4, when Run, then rings = `by_depth` keys, totals equal `total_affected`, and risk badge equals `risk`.
  - `A02` Given a result with cycles/truncation (`partial:true`), when rendered, then the banner shows and ring counts are labelled `≥`.
  - `A03` Given an affected node selected, when the inspector opens, then it lists ≥ 1 supporting path from `paths[]` with edge classes and evidence counts.
  - `A04` Given Scenario mode, when run, then no mutation endpoint is called (network assertion) and the banner is visible.
  - `A05` Given Export checklist, when generated, then the CSV contains one row per affected entity with depth/risk/owner/tests and the header stamp.
  - `A06` Given Cancel during a long run, when pressed, then the request aborts and the previous result stays visible with `Cancelled` state.
- **Evidence:** JRN-05 real-API on the demo repo (`compute_impact`).
- **Readiness:** `BACKEND-MISSING-007` (persisted plans) → checklist persisted locally with `Saved on this device`.

### SCR-008 — Change history

- **Route:** `/changes?from=&to=&entity=&kind=&actor=`. **Personas:** Engineer, Auditor. **Purpose:** who changed what, when (event time vs observed time), compare versions.
- **Layout:** top filter bar (time range, kind chips ADD/MODIFY/DELETE/SCHEMA_CHANGE, entity, source, actor), left 60 % virtualized timeline list grouped by day (each row: Δ symbol+colour, entity chip, kind, graph version, observed/event times, actor/source), right inspector *Change detail* with `DiffViewer` (before/after payload_json) and links to Entity/Graph; secondary tab *Proposals* (compliance changes).
- **Data:** `GET /change-journal?after&limit`, `GET /enterprise/diff/changes?limit`, `GET /enterprise/diff/stats`, `GET /enterprise/diff/timeline/{entity_id}`, `GET /graph/versions?limit`, `GET /graph/diff?from&to&limit`, `POST /config/diff` (config changes tab), compliance: `GET /compliance/changes?state&kind`, `POST /compliance/changes` (create proposal; admin), `POST …/{id}/transition`.
- **Rules:** colour reinforced by `+ − Δ` symbols; identical timestamps keep stable order (by id); deleted entities render with tombstone style and still link to Entity with `include_deleted`; pagination via `after` cursor-like param (journal) else `limit` with cap notice; viewing is separated from proposing/approving (tab + role gate).
- **AC:** `GUI-SCR-008-A01` Given a known fixture change, when listed, then the row shows kind/entity/version and the diff matches before/after payload. `A02` Given filter by entity, when applied, then only that entity's timeline is shown and the URL reflects it. `A03` Given a proposal transition by a non-admin, when attempted, then the control is disabled with reason; forced request yields 403 rendered as `DeniedState`. `A04` Given new events while scrolled, when polling adds rows, then scroll position is preserved and a `n new changes` pill appears.
- **Evidence:** JRN-07 partial (journal after publish); real-API.
- **Readiness:** implemented.

### SCR-009 — Incident root-cause workspace

- **Route:** `/incidents` (list) and `/incidents/:id`. **Personas:** Engineer/SRE, Analyst. **Purpose:** rank hypotheses with evidence, traverse causal/evidence graph, record findings and transitions.
- **Layout (detail):** header (incident title, severity pill, state pill, affected services chips, reporter/assignee), left 40 % *Hypotheses* ranked list (each: cause entity chip, causal class badge §2.7, confidence meter with inputs, time ordering, evidence count, `Promote to finding` (records transition note; never auto-confirms)), center graph (evidence/causal lens with incident at root; `TRIGGERED_BY`/`RESOLVES`/`CORRELATES_WITH` edges emphasized), right inspector *Evidence* for the selected hypothesis, bottom *Decision log* (transitions with actor/time/details).
- **Data:** `GET /platform/incidents?state&severity&limit`, `GET /platform/incidents/{id}`, `POST /platform/incidents` (create), `POST …/{id}/transition {new_state, actor, details}`; hypotheses `POST /causal/hypotheses/{incident_cid} {time_window_hours}`; correlations `POST /causal/correlations/{entity_cid}`; `POST /enterprise/correlation/analyze/{event_id}`; graph `POST /neighborhood`/`/path`/`/graph/shortest-paths` from incident to candidate; `GET /governance/incidents` (AI governance incidents list, separate tab); playback link → SCR-010 with `root_cid`.
- **Rules:** a hypothesis cannot be shown as `HUMAN_CONFIRMED_CAUSE` unless a transition detail recorded by a user exists (client shows `Confirmed by <actor>` only from server data); correlation vs inference vs confirmed are visually distinct; `Record finding` requires evidence selection + text.
- **AC:** `GUI-SCR-009-A01` Given an incident with 3 hypotheses, when loaded, then they render ranked by confidence with class badges and each has ≥ 1 evidence link. `A02` Given `Record finding`, when submitted, then `POST …/transition` is called with `details` containing the finding and the decision log updates from the server response. `A03` Given a hypothesis with no evidence, when rendered, then `No evidence — cannot confirm` is shown and Promote is disabled. `A04` Given two browsers, when one transitions the incident, then the other shows the new state within one poll interval and no silent overwrite occurs (second transition on stale state shows the server's current state first).
- **Evidence:** JRN-06 real-API using demo incident `INC0012042`/`INC0080101`.
- **Readiness:** `BACKEND-MISSING-008` durable RCA workspace → notes/selection persisted locally with label.

### SCR-010 — Temporal and time travel

- **Route:** `/time?at=&from=&to=&root=&play=`. **Personas:** Analyst, Steward, Auditor. **Purpose:** state as of T (valid time and known time), compare T1 vs T2, snapshot management, playback of incident/release/change event streams.
- **Layout:** top *Temporal selector* (G2-TIME-001): mode segmented `As of` / `Compare` / `Playback`; `As of` shows two date-time fields `Valid at` and `Known at` (both optional; tooltip explains the dual timeline KGR-G-014) plus a `Snapshot` combobox; center graph (timeline lens; nodes fade to 16 % outside window; added/removed/changed marks with `+ − Δ`); bottom `TimelineScrubber` (dual-handle + histogram of change counts from journal); right inspector *Changed entities* list (synchronized) with filter by kind; `Snapshots` drawer (list/create/compare/restore).
- **Data:** `GET /graph/as-of?at&limit` (ISO-8601 required → client validates before call); `POST /graph/bitemporal/slice|valid-at|known-at|topology {valid_at?, known_at?}`; `POST /graph/bitemporal/diff {from_coordinate, to_coordinate}`; `GET /graph/versions`; `GET /graph/diff?from&to`; `GET /enterprise/snapshots`, `POST` `{name, snapshot_type:'FULL', tags}` (admin), `POST …/compare?id_a&id_b`, `POST …/restore {snapshot_id}` (admin, high-impact), `DELETE …/{id}`; `GET /brain/snapshot` (brain state summary, Expert); playback `POST /playback/stream {root_cid, max_depth, max_events}` → events list; `/playback/evidence {root_cid}`; `/playback/export {root_cid, format}`; `GET /admin/timeline?limit` (admin operational timeline tab); `GET /enterprise/health/uptime` is **not** graph history — show only in Health (fix of the source's SCR-010 mapping).
- **Playback controls:** Play/Pause/Step back/Step forward/Scrub; speed 1×/2×/5×/10×; no autoplay on load; every event row links to its evidence (`playback/evidence`); reduced motion → discrete steps with announced counts.
- **Rules:** historical mode shows a persistent banner `Historical view · valid at … · known at …`; evidence shown is what the slice returns (not current); restore requires typed confirmation + preview from `compare` + runs as a job if the server returns 202 else shows synchronous result; retention/unavailable timestamps show `No data at this time` (never an empty canvas pretending to be data).
- **AC:** `GUI-SCR-010-A01` Given `at` in URL, when loaded, then `/graph/as-of` is called with that ISO value and the banner shows it; invalid value → inline validation, no call. `A02` Given Compare of two snapshots, when run, then added/removed/changed counts in the inspector equal the compare response and the canvas marks match (sample assertions). `A03` Given Playback with 50 events, when stepping, then the changed-entities list and canvas update per step and each event has an evidence link. `A04` Given Restore by non-admin, then the control is disabled with reason; by admin, then typed confirmation is required and the audit toast shows the correlation ID. `A05` Given reduced motion, when Play is pressed, then no interpolation runs and each step announces `Step n of m: k added, j removed`.
- **Evidence:** JRN-07/JRN-06 playback real-API.
- **Readiness:** implemented; snapshot retention policy decision D-15 pending → show `Retention policy: not configured` when unknown.

### SCR-011 — Query Workbench

- **Route:** `/query?dialect=&template=`. **Personas:** Analyst, Engineer (Advanced/Expert). **Purpose:** author/validate/explain/cost/run/cancel/save queries in supported dialects and the visual builder.
- **Layout:** left 280 px *Library* (tabs Templates (server), History (server + local), Saved (local)), center *Editor* (dialect SegmentedControl built from `GET /graph/backend.capabilities.application_query_languages` ∪ `{QueryPlan JSON, Visual}`; Monaco for text dialects; FlowEditor for Visual builder; parameter form for templates), toolbar `[Validate] [Explain] [Cost] [Run ⏎] [Stop]`, right inspector *Plan* (QueryPlan JSON, explain output, cost), dock *Results* (DataGrid of nodes/edges/rows + graph toggle + export CSV/JSON + `Open in Graph`).
- **Data:** structured `POST /query` (QueryPlan); NL `POST /query/nl`; EQL `POST /query/eql {query}`; others `POST /query/language {language, query}`; explain `POST /query/explain`, cost `POST /query/cost` (QueryPlan only; for text dialects show `Explain not available for this dialect`); templates `GET/POST/GET/DELETE /query/templates…`, bind `POST …/{id}/bind {params}` then run; history `GET /query/history`, slow `GET /query/slow`; multi-paradigm `POST /query/multi-paradigm` (shows five kernel results + harmonized result as tabs, UI-02); federation `POST /federation/query` + `GET /federation/sources` (plan explains routing per source with mode shown verbatim); admin Gremlin `POST /admin/gremlin` (Expert + admin; 501 → disabled "Disabled on this server"); audit `GET /enterprise/audit/events?category&actor&resource&limit` (Expert tab "Query audit").
- **Validation:** client validates `QueryPlan` against the Zod schema (depth 1–8, limit 1–500, timeout 50–30000, intents) before `Run`; server 422 messages map to the editor as markers (Monaco) with position when parsable; `PolicyViolation` text shown as a banner with the policy limits.
- **Execution:** Run uses AbortController; Stop aborts (server-side cancellation is `BACKEND-MISSING-009` → label `Stopped in browser; server may still finish`); results paged client-side with the server cap notice; `partial` banner.
- **Templates:** Save dialog maps editor state to `TemplateSaveRequest` (name, intent, anchor_params, description, filters_template, relationship_allowlist, depth, limit, timeout, evidence_mode); delete with confirm; bind form generated from `anchor_params`.
- **AC:** `GUI-SCR-011-A01` Given a QueryPlan with depth 9, when Validate, then the client blocks with a field error and no request is sent. `A02` Given a valid plan, when Explain/Cost, then both panels show the server responses and Run executes the identical plan (assert body equality). `A03` Given Run then Stop, when aborted, then UI shows Stopped and no result rows are appended afterwards (late response rejected). `A04` Given a saved template, when the API restarts, then it is still listed (server durability) and Bind+Run produces results. `A05` Given a dialect not in backend capabilities, then it is not offered. `A06` Given non-admin, then Admin Gremlin is absent; given admin and 501, then disabled with `Disabled on this server`. `A07` Given result export CSV, when opened in the test, then cells starting with `= + - @` are escaped to prevent spreadsheet formula injection.
- **Evidence:** JRN-10 real-API.
- **Readiness:** `BACKEND-MISSING-009` uniform validate/profile/cancel.

### SCR-012 — Ontology Designer

- **Route:** `/ontology?branch=&tab=`. **Personas:** Steward (ontologist), Architect. **Purpose:** inspect the active ontology; create a draft (branch), edit via canvas or forms, validate, diff, impact-preview, review (PR), publish (merge), migrate, rollback; manage glossary/SKOS, domain packs, marketplace packages.
- **Layout:** top *Version bar* (`Active: ontology 0.4.0 · schema 1.2` from `/graph/schema`; `Draft: feature/xyz (3 changes)` or `No draft`; buttons `New draft`, `Validate`, `Diff`, `Impact`, `Request review`, `Publish`, `Rollback` gated by step state), left 280 px *Types tree* (domains → vertex labels with instance counts; edge labels; search), center tabs *Canvas* (React Flow: labels as nodes, edge labels as connectors; keyboard alternative list "Connect A → B"), *Forms* (label/property/cardinality editors), *Glossary* (SKOS schemes/concepts/mappings), *Domain packs*, *Marketplace*, *Migrations*; right inspector *Selected type* (required/optional properties, source/target labels, instance count, index coverage from `indexes[]`).
- **Data:** read `GET /graph/schema`, `GET /admin/schema`, `GET /ontology/export?limit` (JSON-LD download with partial/mapping_losses notice), `GET /ontology/shacl`, `GET /ontology/validate?limit`, `GET /ontology/drift`; draft lifecycle: `GET /ontology/gitops/branches`, `POST …/branches {branch_name, base_branch}`, `POST …/branches/commit {branch_name, manifest, commit_message, author}`, `POST /ontology/gitops/validate`, `/diff`, `/impact`, `/migration`, `GET/POST /ontology/gitops/prs`, `POST …/prs/{id}/review`, `…/merge`, `POST /ontology/gitops/rollback`, `/package-release`; `POST /ontology/diff`; `POST /ontology/proposals` (generate LLM/induction proposals → review queue with confidence < .6 flagged, KGR-G-015); `POST /brain/induce {corpus, confidence_threshold}` (Expert); migrations `GET/POST /enterprise/migrations`, `…/apply`, `…/rollback`; glossary `GET/POST /taxonomy/schemes|concepts|mappings`, `GET /taxonomy/validate?scheme`, `/export.rdf`; packs `GET /domain-packs`, `POST …/activate`; marketplace `GET /marketplace/packages?q`, `/installed`, `POST /marketplace/install` (shows Data-Flow Manifest and requires admin approval checkbox), `DELETE /packages/{name}`; import `POST /ontology/import?clear` (admin; `clear=true` is high-impact).
- **Lifecycle state (XState):** `active → draft(branch) → edited → validated(ok|errors) → reviewed(pr open) → approved → published(merged) → migrated → active'` with `rollback` from published. Every control is enabled only in valid states; the version bar shows the current state and the draft hash.
- **Rules:** editing the canvas never mutates the active ontology; all edits accumulate into a manifest committed to the branch; semantic diff kinds (GAP-GITOPS-003) rendered with icons; impact preview lists affected labels/instance counts (`what existing data breaks`); self-approval blocked when the server reports the same author (if not reported, show `Separation of duties not enforced by server` notice); publish requires typed branch name.
- **AC:** `GUI-SCR-012-A01` Given no draft, when editing is attempted, then the UI prompts to create a draft (branch) and no write endpoint is called before `POST /branches` succeeds. `A02` Given a draft with an invalid cardinality, when Validate, then errors render next to the offending type and Publish stays disabled. `A03` Given a valid draft, when Diff, then semantic kinds appear with counts matching the response. `A04` Given Publish (merge) succeeds, when `/graph/schema` is refetched, then the version bar updates and `GET /ontology/validate` runs with the new schema. `A05` Given Rollback, then typed confirmation and the server response drive the state (no optimistic version change). `A06` Given the canvas, when using keyboard only, then a relationship can be created via the "Connect" command and appears in the manifest.
- **Evidence:** JRN-07 real-API.
- **Readiness:** `BACKEND-MISSING-010` single publish endpoint → composed from gitops endpoints with explicit step statuses; approval separation D-07 pending.

### SCR-013 — Meta-graph

- **Route:** `/meta-graph?focus=`. **Personas:** Steward, Architect, Analyst. **Purpose:** read-only exploration of types, allowed relationships and instance counts; drill to instances; compare ontology versions.
- **Layout:** toolbar (`Layout: hierarchical (domain → label)`, `Show: counts / indexes / properties`, search type, `Compare version…`), center canvas (nodes = vertex labels sized by `instance_count`, grouped by domain hulls; edges = edge labels with `source_labels × target_labels` expansion collapsed into one edge per pair with count badge), right inspector *Type* (domain, required/optional properties, indexes, `instance_count`, `Show instances` → SCR-005 filtered `label=`; `Edit in Ontology Designer` → SCR-012 draft), table view alternative (labels × metrics).
- **Data:** `GET /graph/schema` (authoritative); `GET /admin/stats.labels` (admin) for cross-check (show mismatch warning if counts differ); `GET /ontology/drift`; `POST /ontology/diff` for version compare; `GET /ontology/export` for download.
- **Rules:** schema edges vs data edges visually distinct (dashed grey for schema, no fact-class badges); zero-instance types shown with hollow nodes; unknown counts `N/A`; never a mutation from this screen.
- **AC:** `GUI-SCR-013-A01` Given schema with N labels, when rendered, then N nodes exist and clicking one shows its properties/indexes exactly as in the response. `A02` Given `Show instances`, then SCR-005 opens with `label` filter applied and the first page loaded via `/search?label=`. `A03` Given counts differ between `/graph/schema` and `/admin/stats`, then a warning explains both sources with timestamps. `A04` Given keyboard navigation, then arrow keys move between type nodes in domain order and Enter opens the inspector.
- **Evidence:** real-API; screenshot set.

### SCR-014 — Sources and connectors

- **Route:** `/sources?type=&health=`, `/sources/:id`. **Personas:** Steward (integration engineer), Admin. **Purpose:** register, configure, test, discover, schedule, operate and monitor sources; catalog of connectors; secondary registries (systems, platform integrations, federation sources) clearly labelled.
- **Layout:** toolbar (`+ Add source` (admin), search, filters health/type/enabled), DataGrid (columns: name, type icon, health pill, enabled toggle (admin; `PATCH`), webhook status, last baseline, last incremental, checkpoint (ellipsis), freshness vs SLO (stamp with warning when lag > `freshness_slo_seconds`), actions ⋯), right drawer *Source detail* tabs: Overview (all `SourceRegistryEntry` fields read-only + Edit), Operations (`Discover`, `Dry run`, `Baseline`, `Sync`, `Reconcile`, `Replay` each enabled only when `capabilities[...]` true; each opens a `SourceOperationRequest` mini-form (checkpoint, event_ids, dry_run) and returns a job → dock), Schedule (`AcquisitionPolicy` form + Pause/Resume), Checkpoint (`GET …/checkpoint`), Reconciliations (`GET …/reconciliations`), Health (last success/failure/lag/error rate when present in `compatibility`/`config` else `Not reported`); tabs at page level: `Sources` (registry), `Catalog` (`GET /connectors/catalog` cards → "Add"), `Systems (legacy)` (`/systems/*`), `Platform integrations` (`/platform/integrations*`), `Federation` (`GET /federation/sources`).
- **Data:** per §3.6; delete `DELETE /sources/{id}` (high-impact; preview dependent jobs by filtering `/admin/jobs` where payload.source_id = id when visible).
- **Rules:** secrets are references only; `secret_refs` display as `env://…` text never resolved; `Test connection` for Systems registry → `POST /systems/{id}/test-connection` with explicit result (no success without 200 + body status); operations unsupported by capabilities are shown disabled with `Connector does not support <op>`; 202 → job row; 409 → inline.
- **AC:** `GUI-SCR-014-A01` Given registry list, when rendered, then each row's health/webhook/capability-driven action availability equals the entry fields. `A02` Given Baseline on a source with `capabilities.baseline=true`, when run, then 202 job appears in the dock and the detail Operations tab shows `Last operation: job <id> PENDING`. `A03` Given Pause, when confirmed, then `POST …/pause` response `paused:true` updates the row without optimistic flip. `A04` Given Add source with a raw token in config, then 422 is surfaced on the field; with `env://` ref it saves. `A05` Given a non-admin, then all mutations are disabled with `Requires admin role` and GET data still renders. `A06` Given Delete, then typed confirmation, 204 removes the row, and dependent held jobs are listed in the preview.
- **Evidence:** JRN-02 real-API.
- **Readiness:** implemented (registry + ops). G2-EKAF-021 health fields not uniformly present → `Not reported` per field.

### SCR-015 — Ingestion and Mapping studio

- **Route:** `/ingestion?step=&source=`. **Personas:** Steward, Admin. **Purpose:** bring data in: upload/paste/select source → profile → map → review inferred graph → dry-run diff → publish (ingest) → monitor; replay DLQ.
- **Layout:** `Stepper` (Input → Profile → Map → Review → Dry run → Publish → Monitor), center per-step panel, right inspector *Mapping/Record detail*, dock jobs; secondary page tabs *Runs* (`GET /ingestion/runs`), *DLQ* (shared with SCR-017), *Manual import (admin)* (Jira/GitLab/Confluence/ServiceNow JSON forms).
- **Steps/data:** Input: `Uploader` (accept from `GET /connectors/files/formats`; `POST /admin/ingestion/files/parse?filename&source_id&ocr` octet-stream → parse result with `status` and warnings (e.g. OCR disabled → `Images produced metadata only`); `POST /admin/ingestion/files?…&dry_run=true` for graph preview; bundles via `GET …/files/bundles/{bundle_id}/{artifact}`), or JSON paste (`JsonIngestionRequest`), or pick a registered source (→ SCR-014 ops). Profile: `POST /ingest/profile`, `/profile/keys`, `/profile/relationships`, `/profile/drift` (against previous profile id). Map: grid source field → `label.property` (schema-driven), relationship candidates with Inferred badges and confidence; mapping stored locally as `mapping_version` note until `BACKEND-MISSING-012`. Review: inferred entities/relationships table with accept/reject toggles (local, `CapabilityGate` notes server review missing) and `DiffViewer` of proposed vs existing (from dry-run result). Dry run: `dry_run=true` call → job/result counts. Publish: real call (`dry_run=false`) → 200/202 → Monitor. Monitor: job rows + `GET /ingestion/runs` + run detail (counts accepted/rejected, checkpoint, timings, versions, per-stage errors).
- **Rules:** client size pre-check 3 MB; `413/415/422/503` mapped; parse `status PARTIAL|FAILED` is not success; no auto-publish after parse; publish requires explicit button and shows the counts it will write; PII never previewed beyond returned sample fields; errors downloadable as CSV.
- **AC:** `GUI-SCR-015-A01` Given a 5 MB file, when selected, then the client rejects with the limit message and no request is sent. `A02` Given parse returns `status: PARTIAL`, then the Input step shows a warning list and Next is enabled only after acknowledging. `A03` Given dry run, then no vertices/edges counts change in `/graph/statistics` (assert before/after) while the preview shows proposed counts. `A04` Given Publish, then counts change and the Monitor step shows the run with `records_accepted/rejected`. `A05` Given a DLQ entry, when Replay, then `POST /admin/dlq/{event_id}/replay` 202 creates a job and the entry shows `Replay queued`. `A06` Given refresh mid-flow, then the step and non-secret inputs restore.
- **Evidence:** JRN-08 real-API with an interrupted upload (network kill) → shows `Upload failed — retry` (resume not available).
- **Readiness:** `BACKEND-MISSING-011` (resumable), `BACKEND-MISSING-012` (server review) → local review with explicit label.

### SCR-016 — Entity resolution and quality

- **Route:** `/quality?tab=`. **Personas:** Steward, Auditor. **Purpose:** identity candidates review; validation findings; conformance; knowledge debt/SLOs; trust/claims/contradictions.
- **Layout:** page tabs: *Identity* (candidate pairs DataGrid: left/right entity cards side by side, score with explain (`GAP-ER-004` — show the score components returned; if only a number, label `Score (components not provided)`), status, actions Accept/Reject (admin) with `actor_id` = principal); *Findings* (`GET /ontology/validate?limit`, `GET /validation/runs?limit`, `POST /admin/validation` (admin "Run validation" → shows coverage/partial), severity chips INFO/WARN/ERROR/BLOCKER, rule id, affected entity link, remediation text); *Conformance* (`GET /conformance/rules`, `POST /conformance/check` → violations with exact path/symbols/commits, `PUT /conformance/rules/{name}` admin); *Knowledge health* (`GET /knowledge/debt` grouped by the 12 categories — counts per category, never a total score; `GET /knowledge-slos` table objective/current/trend/breached; `POST /knowledge/slo` admin; `GET /knowledge/freshness?stale_days`); *Trust & claims* (`GET /knowledge/trust/states`, `GET /truth/contradictions` with `explain`, `POST /truth/resolve` admin with policy choice; banner about process-local state); *Scorecard* (`DimensionGauges` from available metrics; any missing dimension renders `N/A`).
- **Data:** `GET /identity/candidates?status`, `POST …/{id}/decide|reject {actor_id}`; others as listed; `POST /graph/anomalies`, `GET /graph/orphaned`, `GET /graph/stale?threshold_hours` feed a *Hygiene* sub-section (orphans, stale, anomalies with drill to Graph).
- **Rules:** no irreversible merge below threshold is offered (server decides; UI shows `Decide` only for candidates the server lists as pending); bulk actions produce per-item results; rejected candidates remain listed under `Rejected` filter; `unknown denominator → N/A`.
- **AC:** `GUI-SCR-016-A01` Given pending candidates, when Accept on one, then `POST …/decide` is called with the principal id and the row moves to Decided from the server response. `A02` Given findings with mixed severities, then counts per severity equal the response and filtering works. `A03` Given knowledge debt response, then exactly one count per category is shown and no aggregate percentage exists in the DOM. `A04` Given `Run validation` by non-admin, then disabled with reason. `A05` Given conformance violations, then each shows the exact violating path and links to the entities.
- **Evidence:** JRN-09 real-API.
- **Readiness:** `BACKEND-MISSING-013` merge/split/undo.

### SCR-017 — Pipelines and jobs

- **Route:** `/jobs?status=&kind=&source=`, `/jobs/:id`. **Personas:** Admin, Steward, Engineer. **Purpose:** durable job table, detail with logs/result, cancel/readmit, DLQ console, semantic pipeline/harness status, event consumers.
- **Layout:** toolbar (filters status/kind/tenant(admin)/time, `Refresh`, `Auto-refresh 5 s` toggle), DataGrid (columns: status pill, kind, job id (ellipsis+copy), created, started, finished/duration, created_by, attempts, correlation id, actions), detail drawer (tabs Summary (all fields), Result (`JsonViewer` of `result`), Error, Timeline (created→started→finished), Related (source link, DLQ entries)), page tabs *Jobs* · *DLQ* · *Pipelines* · *Consumers* · *Timeline (admin)*.
- **Data:** `GET /admin/jobs`, `GET /admin/jobs/{id}`, `POST …/cancel`, `POST …/readmit` (202), `GET /ingestion/dlq`, `GET /admin/dlq`, `GET /enterprise/dlq/entries?source&limit`, `/dlq/stats`, `POST /enterprise/dlq/replay {entry_ids|source}`, `DELETE /enterprise/dlq/{entry_id}` (high-impact), `POST /admin/dlq/{event_id}/replay`, `POST /admin/ingestion/replay`; pipelines `GET /pipeline/status`, `GET /admin/semantic-pipeline/stages`, `POST /admin/semantic-pipeline {stages, scope}` (admin), `GET /platform/harness/pipelines`, `POST /platform/harness/run`; consumers `GET /admin/event-consumers`, `POST …/run`; `GET /admin/worker`; `GET /admin/timeline?limit`.
- **Rules:** §2.1 action matrix; cancel on RUNNING is disabled with the 409 reason pre-emptively (and handles 409 if raced); readmit only HELD with confirmation and shows 202/409; detail polling 2 s while non-terminal; leaving the screen never cancels anything; ETA only from server timings (none today → `Duration so far`); logs bounded.
- **AC:** `GUI-SCR-017-A01` Given a `HELD` job, when Readmit confirmed, then 202 and the row becomes `PENDING` from the next poll; repeated Readmit shows 409 inline. `A02` Given a `RUNNING` job, then Cancel is disabled with tooltip text equal to the server reason. `A03` Given a `PENDING` job cancelled, then status `CANCELLED` with `finished_at` from server. `A04` Given tenant-bound principal, then only that tenant's jobs are listed (server) and no tenant filter control is shown. `A05` Given DLQ replay, then 202 and the entry shows the new job id. `A06` Given API restart during polling, then the dock shows `Reconnecting…` and resumes without duplicate rows.
- **Evidence:** JRN-08 real-API; two-client consistency.
- **Readiness:** implemented; `GUI-BE-026` stream/outbox missing → polling labelled.

### SCR-018 — Agents

- **Route:** `/agents?tab=`, `/agents/runs/:runId`. **Personas:** Analyst, Admin. **Purpose:** agent catalogue and contracts; run agents with budgets; live-ish trace; explanation envelope; proposals approval queue; loops; mesh recoveries; XAI verification.
- **Layout:** tabs *Catalogue* (cards: id, version, capabilities chips, risk tier badge, budgets, `enabled` → disabled cards greyed with `Disabled by contract`), *Run* (form `AgentRunRequest`: goal, context_refs (entity picker), budgets (max steps/seconds/tool calls — defaults from contract), dry_run toggle default **on** in Simple, synthesize toggle (only when model ready)), *Runs* (list of recent runs from local history + `GET /agents/runs/{id}` detail: lifecycle stepper `RECEIVE → CONTEXT → PLAN → VALIDATE → EXECUTE → OBSERVE → EVALUATE → EXPLAIN → AUDIT → FINISH` from trace, tool calls with argument digests, explanation envelope (answer, confidence + inputs, evidence refs, reasoning_steps as observable steps, `chain_of_thought_disclosed:false` shown as `Private reasoning not disclosed (by design)`), memory (`/memory`)), *Approvals* (`GET /agents/proposals?status=pending` → `ApprovalCard` exact target/changed fields/risk/expiry → `POST …/approve|reject {actor_id}` with reason; banner `Approval records a decision; it does not apply the change`), *Loops* (`GET /loops/catalog`, `/approvals/pending`, `POST /loops/approvals/decide`, `POST /loops/run/{loop_name}`), *Recovery* (`GET /agents/mesh/recoveries?status`, `POST …/recover/{id}` admin), *XAI* (`POST /xai/certify-decision`, `/verify-certificate`, `POST /platform/xai/explain`, `/calibrate` — UI-04), *Governance* link → SCR-021 models/kill switch.
- **Data:** §3.5. Trace updates: poll `GET /agents/runs/{id}` every 2 s (label `polling`) until terminal.
- **Rules:** risk ≥ R2 shows `Blocked until approved`; denied/disabled agents cannot be run (CapabilityGate); injection-like tool output renders inert; approvals show the exact proposal payload digest; kill switch state banner from `GET /governance/kill-switch` (if enabled → all Run buttons disabled with reason).
- **AC:** `GUI-SCR-018-A01` Given catalogue, then disabled agents are not runnable and show the reason. `A02` Given a dry run, then `dry_run:true` in the request and the result is labelled `Dry run — no side effects`. `A03` Given a run, then the stepper reflects trace stages from the server and the explanation shows confidence with inputs; `chain_of_thought_disclosed` is false and no hidden reasoning text appears. `A04` Given a pending proposal, when Approve with reason, then the server response updates status and the banner clarifies no mutation occurred. `A05` Given kill switch enabled, then Run controls are disabled with the reason from the server. `A06` Given model unavailable, then `synthesize` is disabled with reason and runs still execute deterministically.
- **Evidence:** JRN-11 real-API.
- **Readiness:** `BACKEND-MISSING-014` event stream → polling; `BACKEND-MISSING-017` policy.

### SCR-019 — Reports and dashboards

- **Route:** `/reports?tab=`, `/reports/:reportId`. **Personas:** Executive, Analyst, Auditor. **Purpose:** render governed reports from templates with evidence appendix; schedules; exports; evidence capsules; knowledge-product catalog; dashboard builder (saved panels).
- **Layout:** tabs *Templates* (`GET /reports/templates` cards; `Create report` → parameter form from template params; `ReportContext` builder: title, params, graph_stats (auto from `/graph/statistics`), evidence_manifest (pick from saved answers/manifests), findings (from SCR-016 selection), narrative (Tiptap, sanitized)); *Preview* (`POST /reports/render?template_id&report_format=html…` → sandboxed `iframe` with `sandbox=""` + CSP for HTML; Markdown/JSON rendered as text/JSON; format selector lists capability formats; 501 formats disabled with reason); *Schedules* (`GET /reports/schedules`, `POST …?template_id&name&recurrence&report_format`, `GET …/due`, `DELETE …/{id}`, `POST …/{id}/mark-run?at` admin; columns name, template, recurrence, format, next/last run, `due` badge); *Exports* (`GET /reports/export/{report_id}?report_format` → download with content type/size/sha shown when returned; history local); *Capsules* (`GET /capsules`, `POST /capsules {…}`, `GET /capsules/{name}` — evidence capsule spec: root entities, traversal rules, depth, domains, time window, trust threshold); *Catalog* (`GET /catalog/products…` with state transitions admin); *Dashboards* (compose panels query/table/graph/timeline/KPI/evidence from saved queries — local layout persisted in Dexie until a server contract exists; label accordingly).
- **Rules:** no chart data invented; every report shows product/tenant/workspace/as-of stamp and the fact-class legend; tenant branding applied to HTML preview via theme tokens; download integrity shown when the server provides it; schedules show that execution is server-side (`due` list) — persisting a schedule is not execution.
- **AC:** `GUI-SCR-019-A01` Given templates, when a report is rendered in HTML, then it is displayed in a sandboxed iframe (assert attribute) and contains the evidence appendix items selected. `A02` Given a 501 format, then it is disabled with `Not configured on this server (501)`. `A03` Given a schedule created, then it appears from the server list after refetch and Delete returns 204. `A04` Given a capsule created, then `GET /capsules/{name}` returns it and the UI shows its spec. `A05` Given export, then the downloaded bytes equal the response (hash in test) and the UI shows size/type.
- **Evidence:** JRN-12 real-API.
- **Readiness:** `BACKEND-MISSING-015` durable export jobs; PDF/DOCX/PPTX 501 today.

### SCR-020 — Collaboration

- **Route:** `/collaboration`. **Personas:** all. **Purpose:** comments, mentions, shared views, presence, activity.
- **Current state:** `BACKEND-MISSING-016` (no collaboration WS/REST). The screen renders a single `MissingBackendState` page: title `Collaboration is not available in this deployment`, contract `BACKEND-MISSING-016`, and what is available instead: Share view (URL/JSON export, SCR-005), Notifications (SCR-026), Reports sharing (SCR-019). Rail entry remains visible (discoverable) but marked with a `Not available` dot. **No local-only comments or fake presence** (GUI-A025).
- **When backend exists:** threads per entity/edge/subgraph (`CommentThread`), @mentions permission-filtered, presence avatars with TTL, activity feed, share links with scope/expiry; conflict policy per D-12. AC to be defined with the contract; until then `GUI-SCR-020-A01` Given the route, then the missing-backend page renders with working links and no network call to a non-existent endpoint.
- **Evidence:** screenshot + unit test.

### SCR-021 — Governance and security

- **Route:** `/t/:tenant/admin/governance?tab=`. **Personas:** Admin, Auditor (read). **Purpose:** users, roles, policies (replace semantics), evaluate/simulate, tokens, security posture, model governance/kill switch, egress, audit, compliance.
- **Layout:** tabs *Posture* (`GET /security/status` fields verbatim: status, enforcement_mode, algorithm, key_rotation_supported (true/false/unknown), active revocations, roles/permissions counts, timestamp; `GET /auth/health`), *Users* (`GET /authz/users`, `POST` form user_id/roles/attributes, export), *Roles* (`GET /authz/roles`, `GET /security/policy-matrix` hierarchy with inherited roles + permissions matrix (ARIA grid), `POST /authz/roles` with catalog-validated permissions from `all_permissions`), *Policies* (`GET /authz/policies` → editor preserving `policy_id|id, role, permission, conditions, description`; YAML/JSON view toggle (Expert); Save → `POST /authz/policies/reload?replace_existing=true` with high-impact confirm and diff preview; 422 keeps original set), *Evaluate* (`POST /authz/evaluate {user_id, action, resource_attrs}` → `allow` + decision; "What can this user see/do?" simulator; `GET /authz/decisions` log), *Tokens* (`POST /security/tokens/issue` form → show token once in a copy-only field with `Shown once` warning; `POST /security/tokens/verify`; `POST /security/tokens/revoke` with identifier+reason+typed confirm), *Models* (`GET /governance/models`, `POST` register, approve/revoke approval, `GET /governance/templates`, `GET /governance/kill-switch` + `POST` (high-impact), feature kill switches, `GET /compliance/ai/model-cards`, `/evaluations`), *Egress* (`GET /egress/endpoints`, enable/disable (admin), `GET /egress/policy/rules`, `POST` add rule, `GET /egress/report` ("what left the building"), `POST /egress/kill` high-impact), *Audit* (`GET /admin/audit?limit`, `GET /enterprise/audit/events?category&actor&resource&limit`, `/audit/stats`, `/audit/verify` chain integrity badge), *Compliance* (`GET /compliance/packs`, gap analysis per framework, exceptions list/create/revoke, `GET /compliance/roles/auditor-view`), *Privacy* (`POST /privacy/classify`, DSAR locate/erase (high-impact), consents, residency/retention evaluate — Expert).
- **Rules:** deny-by-default rendering for non-admin (read-only where GET allowed, else `DeniedState`); never fetch global user lists outside this screen; policy save is replacement (GUI-A003/A004); tokens never persisted; audit rows show correlation/audit ids; kill switch state propagates to Ask/Agents immediately (invalidate).
- **AC:** `GUI-SCR-021-A01` Given policies loaded, when one is removed and saved, then the request uses `replace_existing=true`, the YAML contains all remaining policies with conditions intact (round-trip test), and `GET /authz/policies` reflects the removal. `A02` Given an invalid policy, then 422 is shown and the active set is unchanged (refetch equality). `A03` Given issue token, then the token is displayed exactly once, not stored, and `verify` returns valid. `A04` Given revoke, then typed confirmation is required and `active_revocations` increments. `A05` Given kill switch enabled, then Ask/Agents controls disable within one invalidation and show the reason. `A06` Given Evaluate, then the decision renders `allow` truthfully and appears in decisions log after refetch. `A07` Given a non-admin, then every mutation control is disabled with reason and `/authz/users` is not requested.
- **Evidence:** JRN-14 real-API (existing `gui-real-api.spec.js` extended).

### SCR-022 — Tenant administration

- **Route:** `/platform/tenants/:tenant?tab=`. **Personas:** Admin (platform/tenant). **Purpose:** tenant context, isolation placement, quotas/usage, lifecycle operations, configuration (effective-config explain), feature flags, backup/recovery, licensing/metering.
- **Layout:** tabs *Overview* (`GET /tenancy/context` → tenant id/urn/principal; `GET /tenancy/isolation/placement` model/layers; `GET /licensing/status`), *Quotas & usage* (`GET /tenancy/quotas` → lane, spec, usage per dimension as bars with `limit`/`current`; `POST /tenancy/quotas/check` simulator; **no** consume/refund controls — server accounting only), *Lifecycle* (`POST /tenancy/lifecycle/provision|configure|suspend|resume|export|clone|delete` — each high-impact with impact preview text from the response contract; delete requires typed tenant id + `Legal hold` acknowledgement checkbox; results are jobs/inline per response), *Placement* (`GET /tenancy/isolation/models`, `POST …/placement {model, layers}`), *Configuration* (`GET /config/definitions`, `/effective?key&tenant&business_unit&workspace&user_id`, `/explain` → layer chain + last change (SR-CFG-003), `POST /config/set|bounds|rollback` admin, `/export|/import`, `GET /config/audit?key`, flags `GET /config/flags`, `GET /enterprise/feature-flags`, `POST …/override {flag_name, tenant_id, enabled}`), *Backup & recovery* (`GET /admin/system.backup` latest with sha/size/counts; `GET /platform/recovery/checkpoints`, `POST …/checkpoint?label`, `POST …/restore/{point_id}` high-impact, `GET …/rpo`, `/peers`, `/stats`), *Metering* (`GET /tenancy/metering/export`, `/verify`, `GET /licensing/meter/export`, `/verify`; `CheckOutcome.degraded` banner).
- **Rules:** platform-wide vs tenant-self scope labelled; every lifecycle op shows the server's actual outcome; licence badge is `entitlement`, not legal clearance; degraded licence → read-only banner, never lock/delete data.
- **AC:** `GUI-SCR-022-A01` Given quotas, then each dimension shows `current/limit` from the response or `N/A`; no consume/refund buttons exist. `A02` Given Suspend, then typed confirmation and the server response drive state. `A03` Given `config/explain`, then the layer chain renders in order with the last change record. `A04` Given a flag override, then `POST` is called with the tenant id and the list refetches. `A05` Given restore checkpoint, then high-impact confirm and the response is shown (no optimistic state). `A06` Given cross-tenant URL tampering by a bound principal, then 403 renders `DeniedState` and no data from the other tenant appears.
- **Evidence:** JRN-15 real-API.
- **Readiness:** tenant list/workspaces (`GUI-BE-021`) missing → tenant id typed/selected from recents.

### SCR-023 — White-label studio

- **Route:** `/t/:tenant/admin/brand`. **Personas:** Admin, Partner. **Purpose:** preview and validate a brand pack across four themes; terminology renames; legal content; publish/rollback when backend exists.
- **Layout:** left 320 px *Brand controls* (product name, logo light/dark upload (PNG/SVG sanitized → SVG rendered via `<img>` only), favicon, brand/accent colour swatches with contrast results inline, font select (bundled list), login image, terminology table canonical → display (`POST /branding/terminology/rename`/`canonicalize` preview), legal kinds), center *Live preview* with theme tabs Light/Dark/HC-Light/HC-Dark and surface tabs Sign-in / Overview / Graph / Table / Form / Report, right *Validation* panel (contrast per pair, semantic lock violations, font overflow at 30 % pseudo-expansion, asset size/type), footer `Save draft (local)` · `Publish` (disabled: `BACKEND-MISSING-018`) · `Rollback` (disabled).
- **Data:** `GET /branding/theme?tenant_id&mode` (current), `GET /branding/legal?tenant_id&kind`, `GET /branding/locales/{locale}/message?key`, terminology endpoints; publish/rollback missing.
- **Rules:** semantic/fact/focus colours locked; publish never enabled by a client flag; preview applies tokens only inside the preview container (CSS scope), never to the live shell until published.
- **AC:** `GUI-SCR-023-A01` Given a brand colour with contrast 3.2:1 on surface, then the swatch shows a failure and Publish stays disabled regardless of backend. `A02` Given terminology rename `Service → Application`, then the preview shows renamed labels and the live shell is unchanged. `A03` Given an SVG logo with a `<script>` element, then it is rejected client-side with reason. `A04` Given the four theme tabs, then each preview passes the automated contrast check for text tokens.
- **Evidence:** JRN-16 (publish steps blocked, recorded as `BLOCKED_BACKEND`).

### SCR-024 — Platform health

- **Route:** `/platform/health?tab=`. **Personas:** Admin, Operator. **Purpose:** real service/store/model/queue/node telemetry; actionable faults; explicit privileged recovery commands; product readiness (three numbers).
- **Layout:** top *Status row* (graph `status`, model `status/name`, backup `status/count/latest`, connectors `checkpoint_count`, worker status, auth health, aggregate health) each as `KpiTile` with as-of; tabs *Services* (`GET /enterprise/health/aggregate`, `/live`, `/ready`, `/startup`, `/sla`, `/uptime`, `GET /health/graph`, `/health/embeddings`, `GET /enterprise/lifecycle/status`), *Capacity & metrics* (`GET /enterprise/observability/metrics`, `GET /enterprise/analytics/metrics` → per metric `trend/anomalies/forecast/growth` charts with units/windows; raw `/metrics` text viewer Expert), *Resilience* (`GET /enterprise/resilience/circuit-breakers` table; `POST …/reset` privileged), *Queues & jobs* (summary from `/admin/jobs` by status; `/admin/worker`; `/admin/event-consumers`), *Recovery* (`GET /platform/recovery/rpo|peers|stats|checkpoints`), *Ops* (`GET /ops/preflight`, `/ha-topology`, `/support-bundle` download (restricted label), `POST /ops/upgrade-plan|shard-plan|helm-summary` forms), *Readiness* (`GET /product/capabilities`, `/first-choice-gate`, `GET /gaps/coverage`, `/completion-gate` → three separate counts (implemented / behaviourally verified / externally gated) — never a single %), *Backends* (`GET /graph/backend`, `/backends` capability matrix with tier labels if present).
- **Rules:** polling 15 s read-only; `check-all`, `reset`, `drain` are explicit buttons with confirm and audit toast; stale telemetry (> 2× poll) shows `Stale` badge; missing samples are gaps, not zeros; sensitive config masked by server (connection fields already redacted).
- **AC:** `GUI-SCR-024-A01` Given `/admin/system` reports model `unavailable`, then the tile shows exactly that string in warning colour and Ask shows the model notice. `A02` Given a circuit breaker open, then it is listed and Reset requires confirm and returns the server state. `A03` Given polling, then no POST is issued automatically (network assertion over 60 s). `A04` Given readiness data, then three counts render separately and no element contains a combined percentage. `A05` Given `/enterprise/health/aggregate` failing, then only that panel errors.
- **Evidence:** real-API with induced fault (stop model container) where available.

### SCR-025 — User settings

- **Route:** `/settings?section=`. **Personas:** all. **Purpose:** profile (read from principal), appearance (theme, density, colour-vision mode, reduced motion), mode (Simple/Advanced/Expert), persona layout, locale & time zone, keyboard shortcuts (rebind with conflict detection), notification preferences (local until `GUI-BE-025`), local data (view/purge Dexie caches per scope), developer (Expert: API base, build id, feature manifest, copy diagnostics).
- **Data:** principal from §3.2 derivation; `BACKEND-MISSING-019` preferences → stored in Dexie per principal with label `Saved on this device`; token tools (`POST /brain/llm/tokenize`) only in Expert developer section; **no** user creation/profiling here (moved to SCR-021/015).
- **Rules:** appearance changes apply immediately with persistence status shown; reset to defaults; policy-enforced settings (tenant theme lock) explained; shortcuts validation prevents duplicates and reserved keys; purge local data requires confirm and lists what is removed (saved views, drafts, recents).
- **AC:** `GUI-SCR-025-A01` Given theme change, then tokens swap in one frame, `prefers-color-scheme` override persists after reload, and the live region announces. `A02` Given reduced motion on, then graph layout interpolation is skipped (assert no animation frames > 1 in the canvas transition). `A03` Given shortcut rebind to an existing key, then a conflict error prevents save. `A04` Given purge local data, then Dexie tables for the current scope are empty and other scopes untouched. `A05` Given logout then login as another principal, then settings of the first principal are not applied.
- **Evidence:** JRN-17.

### SCR-026 — Notifications, help and about

- **Routes:** `/notifications`, `/help`, `/about`. **Personas:** all.
- **Notifications:** inbox DataGrid from `GET /platform/notifications/inbox/{principal}?unread_only&limit` (recipient fixed to the current principal id; any other path is impossible in the UI), filters category/priority/read, mark read (`POST …/{id}/read`), deep links validated to the route tree; `GET /platform/notifications/stats` summary; `Send test notification` (admin, `POST /notifications/send`).
- **Help:** searchable task documentation generated from this document's screen sections (static Markdown bundled), shortcut map (live from the registry, reflects rebinds), `Guided tour (Demo Mode)` that loads `GET /api/v1/demo/scenarios` and runs declared paths via `POST /path` with the `Demo Mode` banner (SR-UX-001) — never outside `/help`; `What can I ask?` explorer listing `GET /suggest/intents`.
- **About:** product name/version/build id/deployment mode/API base; backend chip; first-party notice text (`LICENSING.md`: Copyright (c) 2026 Avyukthi AI and Murthy Ravinder kumar · SPDX `LicenseRef-EOIP-Proprietary`); third-party notices rendered from `apps/web/public/legal/THIRD_PARTY_NOTICES.json` generated at build from the actual bundle (fonts/assets included) — `BACKEND-MISSING-020` server licences endpoint missing → static bundle notice with the build hash; licence entitlement from `GET /licensing/status` labelled `Entitlement`, distinct from copyright; `GET /licensing/check-module` per optional module shows `degraded` notices; benchmark disclaimer text (`Published numbers identify dataset/hardware/version`); SBOM download link if present in `public/legal/`.
- **AC:** `GUI-SCR-026-A01` Given inbox, then only the current principal's path is requested. `A02` Given mark read, then unread count in the bell decrements after refetch (no optimistic). `A03` Given About, then the third-party list equals the generated manifest for this build hash (test compares). `A04` Given Guided tour, then the `Demo Mode` banner is visible for its whole duration and disappears on exit. `A05` Given offline, then Help and About still render (bundled).
- **Evidence:** JRN-17.

### SCR-027 — Global errors and recovery

- **Routes:** `/errors/401|403|404|offline|version|500` plus route-level error boundaries and region boundaries.
- **Behaviour:** distinct pages: *Sign-in required* (401; return URL preserved; draft retained), *Not permitted* (403; capability named; no object details), *Not found* (404; search box + recent objects), *Offline / API unreachable* (capture age if cached data exists; `Retry` GET only), *Version mismatch / stale build* (detected by lazy-chunk 404 or `VITE_BUILD_ID` mismatch header if provided → `Reload to update`), *Something failed* (problem title/detail/code, correlation ID copy, `Report issue` copies diagnostics JSON (no secrets)), *WebGL unavailable* (graph pages show table view + notice). Region boundaries keep sibling regions alive. Error pages never call mutating endpoints or health `check-all`; they may call `GET /health/ready` once on Retry.
- **AC:** `GUI-SCR-027-A01` Given a 401 during a form, then after re-login the form draft is restored. `A02` Given a lazy chunk 404, then the version page shows and Reload fetches a fresh index. `A03` Given WebGL context loss, then the table view appears and a `Restore graph` action re-creates the renderer. `A04` Given 500 problem+json, then title/detail/code/correlation render and Retry re-issues only GETs. `A05` Given an error page, then no POST/PUT/DELETE is issued (network assertion).
- **Evidence:** JRN-18 fault-injection against the release build.

### 9.28 Lens-to-screen matrix

| Lens id | Primary screen | Notes |
|---|---|---|
| search | Global search / SCR-005 | |
| graph | SCR-005 | default |
| evidence | SCR-006 Evidence tab / SCR-005 overlay | |
| impact | SCR-007 | |
| timeline | SCR-010 | |
| change | SCR-008 | |
| architecture | SCR-005 overlay (ELK layered) + SCR-016 Conformance | |
| runtime | SCR-009 / SCR-005 overlay | |
| requirement | SCR-005 (traceability `POST /traceability`) | |
| trust | SCR-016 Trust tab / SCR-005 overlay | |
| security | SCR-005 overlay (supply-chain edges) + SCR-021 | |
| release | SCR-008 + SCR-010 | |
| process | SCR-005 overlay (`/process/*`) | |
| knowledge_health | SCR-016 | |
| simulation | SCR-007 Scenario mode | |
| agent | SCR-018 | |
| decision | SCR-006 Work tab + SCR-005 overlay (`/twin/decisions`) | |
| api | SCR-005 overlay (`APIService/APIEndpoint`) | |
| test | SCR-007 checklist + SCR-005 overlay (`/twin/test-intelligence`) | |
| ontology | SCR-012 / SCR-013 | |

---

## 10. Graph Canvas Specification (`GUI-GRAPH-*`)

### 10.1 Engine and model

- One Graphology `MultiDirectedGraph` per canvas instance is the only graph truth. Node key = `canonical_id`; edge key = `GraphEdge.id` (never array index). Parallel edges and self-loops are preserved. Duplicate ids on ingestion of a response are counted and surfaced (`n duplicate ids ignored`), never swallowed. Dangling endpoints (edge referencing an id not in `nodes[]`) create a placeholder node flagged `unresolved` (hollow, dashed) so the edge is not lost.
- Renderer: Sigma (WebGL) with custom node program supporting shape per domain glyph (circle, square, diamond, triangle, hexagon, pentagon, rounded square) and an icon texture atlas generated from the Lucide registry at build time (`design-system/icons/atlas.ts`). Edge program supports solid/dashed/dotted and arrowheads; curved parallel edges; self-loop arcs.
- Data adapter `graph/adapters/fromGraphResult.ts` maps `GraphResult` → model attributes `{label, domain, properties, creationStatus, trustState, evidence[], firstSeen, lastSeen}` and renderer attributes `{x, y, size, color, shape, icon, hidden, highlighted, dimmed, pinned}` kept in a separate attribute namespace.

### 10.2 Encodings (`GUI-GRAPH-01`)

- Type → icon + shape (primary), domain → categorical colour (secondary §5.3). Size → degree by default (log scale 6–22 px), switchable to centrality/property/uniform. Border → status (`deleted_at` tombstone dashed grey; `quarantine` red dotted). Badges (max 2, top-right): alert, owner missing, stale (lastSeen > SLO), annotation.
- Edge → fact class style §2.2; direction arrows always; inferred edges alpha by confidence; labels on hover or zoom ≥ .7; evidence-backed edges 0.5 px thicker.
- Selection: 3 px halo `graph.node.selected`; hover `graph.node.hover`; dimmed alpha .16 for non-matches; path edges `graph.path` with animated dash offset (static in reduced motion) and numbered badges along the path.
- Impact overlay: concentric ring guides; node fill by risk; ring badge count = depth.
- Clusters: convex hull `graph.hull` alpha .12 with label (auto-label = top-3 labels + top-2 name tokens, user override local), click hull → filter.

### 10.3 Level of detail and zoom (`GUI-GRAPH-02`)

Zoom range .05–16; zoom-to-cursor; labels hidden < .35, abbreviated .35–.7 (first 14 chars + …), full ≥ .7; label screen size clamped 10–16 px; far zoom (< .3) shows cluster hulls + meta-edges only when clustering is active; near zoom (> 2) shows property chips for selected/hovered nodes. ResizeObserver debounced 100 ms; DPR capped at 2 except export. Label collision avoided with a grid-based hider (priority: selected > hovered > high degree).

### 10.4 Rendering tiers (`GUI-GRAPH-03`)

| Elements loaded | Behaviour |
|---|---|
| ≤ 1 000 | full labels at ≥ .35, animations on, rich overlays |
| 1 001–10 000 | worker layouts mandatory, animations on but staggered, label LOD |
| 10 001–100 000 | animations off, edges draw instantly, labels only on hover/selected, minimap simplified, `Performance mode` banner |
| > 100 000 or single action adding > 5 000 (`DEC-GUI-11`) | refuse by default: `This action would add n elements. Narrow the query or Add anyway` (Advanced+ only); server aggregation `GUI-BE-023` missing → always bounded |

### 10.5 Layouts (`GUI-GRAPH-04`)

ForceAtlas2 (worker, default; deterministic seed from sorted node ids so test fixtures are stable), ELK layered (lineage/architecture/dependency; worker), radial ego (entity-centred), concentric hop (impact), circular, grid, timeline (x by timestamp property chosen from `created_at|observed_at|modified_at`, y by label), geographic (only when nodes have `latitude/longitude` properties; uses bundled simple projection, no tiles), adjacency matrix (dense graphs; renders as ECharts heatmap alternative view). Layout transitions interpolate 600–1 200 ms (scaled by count; instant in reduced motion); pinned nodes keep position; collapse preserves centroid; expansion radiates from parent. Layout picker shows which layouts are suitable (e.g. timeline disabled without timestamps, with reason).

### 10.6 Interactions (`GUI-GRAPH-05`)

Pan/zoom (wheel, pinch, keyboard `+/-`), click select, shift-click multi-select, `Shift+drag` lasso, `Ctrl+Shift+drag` rectangle, double-click expand (depth from toolbar 1–3 → `POST /neighborhood`), right-click/`Shift+F10` context menu (node: Inspect, Expand 1/2/3, Impact, Reverse impact, Find path to…, Lineage, Why?, What changed?, What if removed?, Pin/Unpin, Hide, Isolate, Copy id, Open Entity; edge: Inspect, Why does this edge exist?, Show evidence, Parallel edges, Hide type, Copy; canvas: Fit, Reset filters, Toggle minimap/legend, Export…, Save view), hover preview card (300 ms), drag node (pins it), undo/redo of graph state (selection, hidden, pins, filters, expansions; 50 steps), exploration breadcrumbs (last 10 expansions, clickable), focus mode (selected + N hops, rest dimmed), path mode (pick source then target → `/path` or `/shortest-paths` picker; path breadcrumb with `[`/`]` stepping), hub exclusion slider (max degree) with ghost silhouettes for excluded hubs, search-within-view (dims non-matches instantly), hide/unhide, isolate.

### 10.7 Filters (`GUI-GRAPH-06`)

Filter builder dimensions: domain, label (with live counts), edge type (live counts), fact class (§2.2), trust state (≥ ladder), evidence (evidenced/unevidenced), time window (created/modified), property (key op value), degree range, community, search-within-view, hub exclusion. Active filters shown as chips (click to remove); `Reset`; presets saved locally with names; filter state persists across lens switches (G2-UX-LENS-002) and is URL-encoded.

### 10.8 Overlays and analytics

Centrality (`/graph/metrics`, `/centrality/full`) → size/colour; community (`/graph/cluster`) → hulls; blast radius (`/graph/blast-radius`) → rings/colours; anomalies (`/graph/anomalies`) → badge; orphans/stale (`/graph/orphaned`, `/graph/stale`) → dashed/dim style; surprises (`/graph/surprises`) → sparkle badge + ranked sidebar; PR impact (`/graph/pr-impact`) → heat; conformance violations (`/conformance/check`) → red edge markers (architecture lens). Each overlay shows its source endpoint, as-of time and `partial` state in the legend; overlays are additive and individually toggleable.

### 10.9 Accessible equivalents (`GUI-GRAPH-07`)

`GraphTableView`: DataGrid with columns Name, Type, Domain, Degree, In, Out, Fact class, Trust, Evidence, Status, Last seen; expandable rows list relationships; selection synchronized both ways; every context-menu action available in the row menu. `GraphTreeView`: ego tree from the selected node (APG treeview). Live region announces `Selected <label> <name>, <n> relationships` and `Graph updated: +a nodes, −r nodes`. Canvas has `role="application"` with a described summary (`Graph with 1 240 nodes and 3 118 edges; press T for table view`). Keyboard traversal order documented (§6.7) and stable (sorted by label then name).

### 10.10 Saved views and URL state (`GUI-GRAPH-08`)

View = `{schemaVersion, name, scope{tenant,workspace}, seed{ids[]|query}, expansions[], filters, lens, layout, pins{id:{x,y}}, hidden[], camera{x,y,ratio}, time{at?,from?,to?}, graphVersion?}`. Saved to Dexie (`GUI-BE-030`); import/export JSON; URL carries a compact subset (`view` id or `focus`, `lens`, `layout`, `t`, `q`, `cam`), never query text containing PII beyond the entity ids the user already sees. Restoring validates ids against the current scope: missing ids reported, foreign ids rejected.

### 10.11 Exports (`GUI-GRAPH-09`)

PNG 2×/4× (Sigma `toCanvas` at scaled DPR; nonblank check), SVG (vector from model; sanitized text), Print/Save as PDF (structured DOM document; no `document.write`), JSON-LD (authoritative ids/types/endpoints precede properties), GraphML (correct namespace + key declarations), GEXF (ids preserved, Unicode escaped), CSV nodes.csv/edges.csv (RFC 4180 quoting; formula-injection escape), Obsidian vault zip (note per entity, `[[wikilinks]]`, YAML frontmatter), Mermaid (identifier escaping/collision handling, truncation notice), Cypher (parameterized MERGE with escaped identifiers), Clipboard Markdown, Interactive HTML (self-contained, inline Sigma, CSP meta, no external requests; values inserted via JSON text nodes). Server conversions via `POST /graph/convert`. Export dialog: format, resolution, scope (`visible` only — full-graph export requires server `GUI-BE-024`), include annotations (local), header stamp §8.9.

### 10.12 Cytoscape retirement parity checklist

Before removing `cytoscape`: selection parity, 12 layouts mapped (COSE→FA2, dagre→ELK layered, breadthfirst→ELK tree, circle, grid, concentric, radial, cola→FA2 with constraints flagged unsupported, euler→FA2, spread→FA2 with scaling, timeline, clustered), export parity (all formats above), keyboard parity, test fixtures ported, bundle delta recorded. Retirement is a separate PR with the parity receipt attached.

### 10.13 Performance targets (`GUI-GRAPH-10`)

1 000-node first render < 1 s after data arrival (network and layout timed separately); 60 fps interaction at 10 000 nodes / 20 000 edges on the reference laptop (4-core/16 GB, integrated GPU, Chrome current); ≥ 30 fps at 100 000 elements in performance mode; main-thread tasks > 16 ms moved to workers; active graph heap ≤ 800 MB with warning at 560 MB (via `performance.measureUserAgentSpecificMemory` where available else estimated from element counts and labelled `estimated`); no growth after 20 scope switches (plateau test). CI records GPU/software renderer identity and never claims laptop performance from a software-rendered run.

---

## 11. AI, Natural-Language and Evidence UX (`GUI-AI-*`)

### 11.1 Principles

Evidence before prose; deterministic path first; model narration optional and labelled; abstain honestly; never display hidden reasoning; local-only by default; every answer carries mode badge, boundary badge, knowledge age, confidence with inputs, and an evidence manifest.

### 11.2 Suggestion cards (SR-NLQ-002) (`GUI-AI-01`)

From `POST /api/v1/suggest/interpret` candidates. Card anatomy: paraphrase (plain language), intent chip (`PATH`…), entity bindings (chips with alternatives dropdown when the server offers alternatives; pin for session), plan preview button (shows exact `QueryPlan` JSON and the dialect text if provided), expected result shape (`graph · ≤ 100 rows`), estimated cost/latency (from `POST /query/cost` when a plan exists; else `Cost unknown`), confidence meter, data-coverage note (from `parse` or manifest coverage), permission check (`CapabilityGate` on intent), actions `Run` / `Edit plan` (opens SCR-011 with the plan). Cards are ranked by server order; the UI never reorders by its own heuristics.

### 11.3 Streaming (`GUI-AI-02`)

`POST /brain/llm/stream` with `Accept: text/event-stream`; parse `data:` lines; append `delta`; `is_final` or `[DONE]` finalizes; `usage` shown in Expert; Stop aborts; `Regenerate` increments local answer id; errors mid-stream keep partial text with `Stream interrupted` state; batch live-region announcements every 1 s or sentence end. Splitting a completed string into words to fake streaming is prohibited (test: first chunk render time < final response time).

### 11.4 Citations and evidence (`GUI-AI-03`)

Each factual clause gets `[n]` chips bound to `{canonical_id | edge_id | evidence_ref}`; hover/focus highlights in the dock graph and scrolls the evidence panel; unknown refs render as `[?] unresolved citation` (counted in the coverage note). `EvidenceManifestPanel` sections: citations (fact_text, source_ref, confidence), total facts, coverage score (as number with its definition), rules fired, tool calls (digests only), confidence inputs, human approvals, source freshness. Manifest export via `POST /evidence/manifest` and download JSON.

### 11.5 Confidence and abstention (`GUI-AI-04`)

`ConfidenceMeter` requires `inputs` (or `confidence_inputs`) to render; otherwise shows `Confidence reported without inputs` in muted text. Calibration note links to `POST /platform/xai/calibrate` output when available. Abstain rules §SCR-004. `uncertainty_reason` shown verbatim when present.

### 11.6 Untrusted content (`GUI-AI-05`)

Source snippets, tool outputs and model text render as text in a framed `Untrusted content` container; Markdown allowed subset (headings, lists, code, links http/https with confirmation on external domains); no HTML, no images from remote hosts; prompt-injection flags from the knowledge firewall (`POST /knowledge/firewall/inspect`) render as warning annotations.

### 11.7 Feedback (`GUI-AI-06`)

Thumbs/correction → `POST /enterprise/learning/feedback`; `This edge is wrong` → opens SCR-016 Identity/Claims with prefilled context; copy states that feedback is reviewed, not auto-trained.

---

## 12. VS Code Extension UI (`GUI-VSC-*`)

Scope: `apps/vscode-extension` (existing JS, 10 commands). Requirements for parity with the web design language and truthfulness:

| ID | Requirement |
|---|---|
| GUI-VSC-01 | Sidebar `EOIP Context` TreeView: sections Current symbol (name, kind, range), Related entities grouped by label (icons from the same registry rendered as codicons mapping table), Relationships, Provenance, Evidence; each item has a tooltip with canonical id and fact class; unresolved → `Not indexed` item (never empty tree without explanation) |
| GUI-VSC-02 | Status bar item: `EOIP: Connected · <tenant>` / `EOIP: Offline` / `EOIP: Not configured`; click opens Set Access Token; token stored in `SecretStorage` only |
| GUI-VSC-03 | Commands (existing names): Set Access Token, Context for Active File, Trace Requirement to Code, Explore Impact, Trace Provenance / Lineage, GraphRAG Retrieval, Search Knowledge Graph, Natural Language Query (`POST /api/v1/query/nl`), Read-only MCP Tool; add quick actions `WHY`, `WHAT CHANGED`, `IMPACT`, `WHERE USED` mapped to §3.3 operators (G2-VSC-007) |
| GUI-VSC-04 | Webview results: same tokens (VS Code theme-aware CSS variables mapped to §5.2 semantics), mode badge, knowledge-age stamp, evidence list with `Open source range` actions constrained to `eoip.repositoryRoot` (reject absolute/traversal/symlink); CSP `default-src 'none'` with nonce |
| GUI-VSC-05 | Failure to reach EOIP never blocks editing; last successful context retained with `as of` stamp |
| GUI-VSC-06 | No write/admin tools; MCP tool list filtered to read-only; hidden chain-of-thought never shown |
| GUI-VSC-07 | Extension host tests per command against the real API (fixture repo), plus offline test |

---

## 13. Accessibility, Localisation, Security, Performance, Telemetry

### 13.1 Accessibility (`GUI-A11Y-*`) — WCAG 2.2 AA

- A11Y-01 Landmarks (`banner`, `navigation`, `main`, `complementary` inspector, `contentinfo` dock status), skip links to main/inspector/dock, one `<h1>` per route.
- A11Y-02 Keyboard: every journey completable without pointer; no traps; focus visible (≥ 3:1, 2 px, offset 2 px); focus restored after overlays/errors; roving tabindex in toolbars/grids; `Esc` stack.
- A11Y-03 Targets ≥ 24×24 CSS px (44 preferred); compact density preserves target via padding.
- A11Y-04 Names/roles/states via Radix + explicit `aria-*`; icon-only controls labelled; status pills include text; colour never sole carrier (shape/icon/text redundancy everywhere incl. graph fact classes).
- A11Y-05 Live regions: `polite` for status/copy/stream; `assertive` only for session expiry and destructive results.
- A11Y-06 Virtualized lists/grids expose `aria-rowcount/aria-rowindex`, `aria-setsize/posinset`.
- A11Y-07 Graph: `GraphTableView`/`GraphTreeView` parity; canvas summary; traversal keys; reduced motion.
- A11Y-08 Reflow at 400 % / 320 px without loss; content/UI scroll containers labelled.
- A11Y-09 Forced-colors mode: borders/outlines rely on `CanvasText`/`Highlight`; icons use `currentColor`.
- A11Y-10 Media: any instructional video (help) has captions/transcript.
- A11Y-11 Testing: axe 0 serious/critical on every screen × 4 themes; manual NVDA/Chrome, JAWS/Edge, VoiceOver/Safari transcripts for JRN-01/03/04/14 recorded with versions; accessibility conformance report produced for procurement (TEST-005.A2).

### 13.2 Internationalisation (`GUI-I18N-*`)

- I18N-01 All strings in ICU message files (`locales/en.json` + ≥ 1 more locale + pseudo-locale `en-XA` for 30 % expansion); no concatenated grammar; plural/select rules.
- I18N-02 Numbers/dates/durations/units/currencies via `Intl` with the user locale and time zone (Settings); UTC on the wire; time zone label visible on all timestamps on hover.
- I18N-03 RTL: `dir` on `<html>`; logical CSS properties; mirrored directional icons (arrows, back/forward) but not graphs/timelines/code; ≥ 1 RTL locale file.
- I18N-04 Fonts: Noto subsets loaded on demand per script; no external font requests.
- I18N-05 Ontology labels: tenant locale → user locale → canonical fallback using `GET /branding/locales/{locale}/message?key`; terminology renames applied through one `useTerm()` hook.
- I18N-06 Locale-aware sorting/search in grids; pseudo-locale CI run checks clipping/overflow on fixed viewports.

### 13.3 Browser security (`GUI-SEC-*`)

- SEC-01 Token in memory only; `api.dispose()` on logout/scope switch; no token in URLs (incl. WS), storage, logs, telemetry, exports.
- SEC-02 CSP: `default-src 'self'; script-src 'self' 'nonce-…'; style-src 'self' 'nonce-…'; img-src 'self' data: blob:; connect-src 'self' <API origin>; worker-src 'self' blob:; frame-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'` set by Nginx (`apps/web/nginx.conf`) and verified in E2E; Trusted Types policy for the few sanitized sinks; `require-trusted-types-for 'script'` where supported.
- SEC-03 Sanitization: DOMPurify allow-list for rich text (report narrative, comments); all graph/AI/source values via text nodes; `JsonViewer` never evaluates; link schemes http/https only; external domains confirm; SVG assets rendered via `<img>`; `iframe` report preview `sandbox=""`.
- SEC-04 CSRF: current API is header-bearer (not cookie) so CSRF is N/A; if cookies are introduced (`BACKEND-MISSING-001`), add double-submit token and `SameSite=Strict`.
- SEC-05 Local data: Dexie scoped; purge on logout/scope switch; no PII exports cached; drafts exclude secret fields; retention 30 days.
- SEC-06 Downloads: client exports carry stamps; server downloads use the authenticated client and `Content-Disposition` filename; large exports warn.
- SEC-07 Error surfaces never include stack traces or protected object details; correlation IDs only.
- SEC-08 Dependency hygiene: `npm audit` gate (no high), SBOM generated, third-party notices generated from the bundle (SCR-026).
- SEC-09 No `eval`, no inline scripts, no remote CDN, no analytics beacons; verified by a production-build scan.

### 13.4 Performance budgets (`GUI-PERF-*`)

| Budget | Value |
|---|---|
| Shell initial JS | ≤ 250 kB gzip (current measured 92.79 kB main — keep) |
| Per initial route | ≤ 150 kB gzip excluding lazily loaded engines (Sigma, Monaco, Tiptap, React Flow, ECharts, admin families) |
| LCP / INP / CLS | < 2.0 s / < 200 ms / < 0.1 on the reference laptop with warm local API |
| Interaction | ≤ 200 ms for UI responses (SR-UX-012); ≤ 100 ms graph hover/select |
| Tables | virtualize > 100 rows; trees > 300 nodes |
| Workers | layout/parsing/algorithms > 16 ms off main thread |
| Memory | graph heap ≤ 800 MB, warn 560 MB; no leak across 20 scope switches |
| Polling | events 5 s visible / 30 s hidden; jobs 2 s / 10 s; health 15 s; all paused when offline |
| Caching | lists SWR 30 s; schema 5 min with manual refresh; never cache secrets/exports |

Measured with Lighthouse CI + Playwright traces; the chunk manifest is committed per release; raising Vite's warning limit is not an accepted fix.

### 13.5 Telemetry and analytics (`GUI-TEL-*`)

- TEL-01 Off by default; enabled only by tenant consent flag from server config (never a client flag); local OTel collector only; kill switch in SCR-022.
- TEL-02 Events `screen.<id>.viewed|action_started|action_succeeded|action_failed`, `graph.layout.completed`, `ask.answer.rendered`, `job.terminal`; fields `schema_version, event_name, occurred_at, screen_id, tenant_pseudonym, session_pseudonym, result, duration_bucket, offline, build_id`.
- TEL-03 Forbidden: query/prompt/source text, entity labels/properties, credentials, raw ids, exported content.
- TEL-04 Correlation: W3C `traceparent` propagated to the API when telemetry is enabled; always `X-Correlation-ID`.
- TEL-05 Error capture local with redaction; `Report issue` copies a diagnostics JSON (build, route, correlation ids, problem titles) to clipboard — no network.

---

## 14. Testing, Evidence and Anti-False-Completion Controls (`GUI-TEST-*`)

### 14.1 Test layers (all mandatory)

| Layer | Tooling | Proves | Cannot prove |
|---|---|---|---|
| Static | `tsc --noEmit` strict, ESLint (import boundaries, no raw durations, no `innerHTML`, no `fetch` outside `shared/api`), `madge` cycles, `check-no-mocks` | types, boundaries, forbidden patterns | runtime behaviour |
| Unit | Vitest | reducers, adapters (`fromGraphResult`), problem normalizer, query-key factories, exporters (parse round-trip), token contrast, icon registry coverage, event dedupe/sort/bounding | server, a11y |
| Component | Vitest + Testing Library + axe | §7 states, keyboard, ARIA, validation, motion tokens, reduced motion | real transport |
| Story | Storybook (every component × state; Chromatic-free local visual snapshots via Playwright) | visual parity, extremes | integration |
| Contract | Vitest against the OpenAPI snapshot: every client operation's request/response schema (Zod) validates against the live `GET /openapi.json` captured in CI; drift fails | client/server shape agreement | business outcome |
| Real-API journeys | Playwright project `real-api` (no `page.route` allowed; lint rule) against `uvicorn apps.api.main:create_app` with `EOIP_DATA_DIR=<tmp>`, `EOIP_GRAPH_BACKEND=memory` (profile recorded) and demo fixtures | end-to-end outcomes, persistence across API restart, authorization, two-tenant isolation | production graph persistence at scale |
| Mocked journeys | Playwright project `mocked` (MSW/`page.route` only for `BACKEND-MISSING-*` and failure injection) | controlled UI states | integration |
| Visual | Playwright screenshots at 1280×800, 1440×900, 1920×1080, 2560×1440, 3440×1440, 768×1024, 390×844, 320×568 × 4 themes × 3 densities (pairwise), RTL, pseudo-locale, reduced motion | layout/clipping/theme | semantics |
| A11y | `@axe-core/playwright` per screen/state; manual AT transcripts | automated criteria | full AA |
| Perf | Lighthouse CI, Playwright traces, graph frame/heap traces with datasets 1k/10k/100k (generated, seeded, committed hash) | budgets | untested hardware |
| Security | production-build scan (no mocks/eval/CDN), CSP header test, token-in-storage/URL assertions, formula-injection export tests, XSS fixtures in graph values/AI text | browser threats listed | all threats |

Coverage floors: ≥ 90 % branches on `shared/security`, `shared/api`, `shared/events`, state reducers; ≥ 80 % on features. Coverage is a floor, not evidence.

### 14.2 Rules that make a test count

- Test name includes the AC id (`GUI-SCR-005-A03`) and asserts the **business outcome** (e.g. counts equal response, request body equality, DOM state), not only "renders".
- Real-API tests record backend revision, data dir hash, graph backend, and build hash in the receipt.
- A skipped, xfail, flaky-retried or intercepted-in-real-project test is a failure for acceptance.
- Screenshots are evidence only with representative data (never empty mock).
- Manual AT/usability reviews name reviewer, environment, procedure, observations and result; no agent self-certification.

### 14.3 Required real-API journeys

JRN-01…JRN-18 (§1.3) each with: happy path, invalid input, unauthorized principal (403), tenant substitution (two tenants on the same backend), revoked/expired token mid-flow, empty/partial result, network fault, API restart, cancellation/concurrent edit where applicable. Journeys blocked by missing contracts record `BLOCKED_BACKEND` with the contract id (JRN-13, parts of JRN-02/04/16).

### 14.4 Graph canvas verification

Assert on the Graphology instance (node/edge counts, attributes) **and** on rendered pixels (sample points at projected node coordinates differ from background; selection halo colour present) **and** on screenshots after real interactions (select, expand, path). Record GPU/renderer string from `WEBGL_debug_renderer_info`. Export tests parse outputs with independent libraries (`fast-xml-parser` for GraphML/GEXF, CSV parser, JSON-LD expand).

### 14.5 CI sequence

1. Install (`npm ci`), licence/SBOM inventory, static checks. 2. Unit/component/stories. 3. Contract tests against captured OpenAPI (`python -c "from apps.api.main import create_app; …"` dump) with drift gate. 4. Build; chunk manifest; no-mock scan; CSP test. 5. Real-API journeys (fresh API per project; retain traces/console/network). 6. Visual/a11y/i18n matrix. 7. Perf traces. 8. Evidence manifest + verifier. PR runs impacted subsets with the selection logic recorded; release candidate runs the full matrix.

### 14.6 Evidence bundle (`test-results/gui/<run-id>/`)

`manifest.json` (schema `gui-evidence-v1`: clause ids, source commit + dirty digest, requirements doc SHA-256, build hash, lockfile hashes, backend revision, OpenAPI hash, profile, dataset hashes, OS/browser/GPU, viewport/theme/density/locale/motion), `commands.log`, JUnit/Playwright JSON, redacted traces/HAR, console/page errors, network failures, screenshots/videos, axe output, manual transcripts, perf traces, artifact SHA-256 list. Verifier (`scripts/verify_gui_evidence.py`) fails closed on placeholders, `NOT_RUN`, missing artifacts, hash mismatch, mocks in real project, skipped/xfail/retried tests, stale build, unknown runtime identity, unapproved manual gates. Negative controls (remove a test, alter a hash, inject a mock) must make the verifier fail.

### 14.7 Status reporting

Report three totals separately, never blended: (1) implementation clauses `BEHAVIOR_VERIFIED`, (2) journeys `INTEGRATION_VERIFIED`, (3) external/manual gates approved. Per-screen status table lists each AC id with state. "Complete" is stated per AC.

### 14.8 Handoff record template (produce after every slice)

```text
Slice / package IDs and AC IDs:
Requirements doc SHA-256 (this file) and repository/build revisions:
Decisions used (DEC-GUI-*) ; unresolved owner decisions:
Files inspected ; files added/modified:
Behaviour delivered (what a user can now do, not files):
Backend/storage/model profile exercised (real vs mocked, per journey):
Commands, timestamps, exact test counts (passed/failed/skipped):
Evidence manifest path and artifact hashes:
Negative tests: 401/403/409/422/partial/restart/cancel/two-tenant:
Visual, a11y (automated + manual) status:
Blocked items with contract IDs:
Migration/rollback notes (legacy route redirects, Dexie schema version):
Next bounded task:
```

---

## 15. Delivery Order (Milestones) and Exit Criteria

Follow this order; do not start a later milestone's screens before the earlier exit criteria pass (parallel preparatory work on tokens/components is allowed).

| M | Scope | Exit criteria |
|---|---|---|
| M0 Foundations | §4 toolchain (TS strict, lint boundaries, scripts `typecheck lint test:unit test:component test:contract test:e2e:real test:e2e:mocked test:visual test:a11y test:perf check:bundle check:no-mocks check:gui-evidence`), §5 tokens + 4 themes + icon registry + motion, §6 shell (rail, context bar, inspector, dock, palette, keyboard, responsive), §7 components (COMP-01..10, 14..22), §8 patterns, §3 transport (problem normalizer, correlation header, scope generation), SCR-001, SCR-027, legacy redirects | JRN-01 + JRN-18 real-API pass; four themes screenshot set; axe clean on shell/auth/errors; no token in storage/URL; bundle ≤ budgets |
| M1 Graph core | §10 engine (Graphology model, Sigma programs, worker FA2/ELK, LOD, table/tree parity, filters, saved views, exports), SCR-005, SCR-006, SCR-013, SCR-003 | JRN-03 pass incl. API restart + view restore; 1k < 1 s receipt; 10k frame trace; export round-trips; two-tenant isolation; Cytoscape parity checklist started |
| M2 Intelligence | §11, SCR-004, SCR-007, SCR-008, SCR-009, SCR-010, SCR-011 | JRN-04 (model ready + stopped), JRN-05, JRN-06, JRN-10 pass; abstain/partial cases; SSE first-chunk timing; no fabricated confidence |
| M3 Data foundation | SCR-002, SCR-012, SCR-014, SCR-015, SCR-016, SCR-017 | JRN-02, JRN-07, JRN-08, JRN-09 pass; dry-run vs publish count assertions; readmit/cancel semantics; replace-policy of mapping drafts local-labelled |
| M4 Work & content | SCR-018, SCR-019, SCR-020 (missing-backend page) | JRN-11, JRN-12 pass; approvals exactly-once; sandboxed report preview; 501 formats disabled |
| M5 Enterprise | SCR-021, SCR-022, SCR-023, SCR-024, SCR-025, SCR-026 | JRN-14, JRN-15, JRN-16 (blocked parts recorded), JRN-17 pass; policy replace round-trip; kill switch propagation; About notices equal bundle inventory |
| M6 Hardening | §13 full matrix (a11y manual, i18n RTL/pseudo, perf 100k, security scans), Cytoscape removal, legacy folder deletion, docs/help generation | all gates G0–G9 (below) pass; evidence bundle complete; three-number status report |

Release gates: G0 scope (every AC registered), G1 contracts (drift gate green), G2 identity/isolation (two-tenant adversarial tests), G3 behaviour (all journeys), G4 durability (restart tests), G5 visual/usability (reviewed baselines; usability tasks ≥ 90 % unassisted completion on JRN-02/04/06 with ≥ 5 participants per role recorded), G6 a11y/i18n, G7 performance, G8 security/privacy/legal delivery (notices), G9 evidence (verifier pass).

---

## 16. Decision Register (binding defaults for the agent; owner may override by ADR)

| ID | Decision | Default in force |
|---|---|---|
| DEC-GUI-01 | Job status vocabulary | §2.1 backend enum; map `DONE→SUCCEEDED` display-only |
| DEC-GUI-02 | Fact-class display | §2.2 six classes |
| DEC-GUI-03 | Trust ladder | §2.3 |
| DEC-GUI-04 | Answer mode badges | §2.4 incl. `Simulated (not model inference)` |
| DEC-GUI-05 | Boundary badge source | `GET /egress/endpoints` |
| DEC-GUI-06 | Risk/loop labels | §2.6 glossary expansions |
| DEC-GUI-07 | Lens catalog | server `GET /lens/catalog` |
| DEC-GUI-08 | Disclosure modes | Simple/Advanced/Expert |
| DEC-GUI-09 | Stack | §4.1 |
| DEC-GUI-10 | Versions | resolved at install via registry; pinned; recorded |
| DEC-GUI-11 | Client expansion cap | 5 000 new elements per action; override Advanced+ |
| DEC-GUI-12 | Visual direction | Evidence Atlas light-first; 4 themes |
| DEC-GUI-13 | Workspace until `GUI-BE-021` | fixed `default`; switcher shows not-enabled notice |
| DEC-GUI-14 | Realtime until `GUI-BE-029` | polling labelled `polling`; no `?token=` |
| DEC-GUI-15 | Mobile | read-only companion; approvals read-only (owner decision D-13 pending) |
| DEC-GUI-16 | Offline | read-only cached views with capture age; no queued mutations (D-11 default) |
| DEC-GUI-17 | Collaboration | missing-backend page only; no local comments/presence |
| DEC-GUI-18 | Export scope | visible subgraph only until `GUI-BE-024` |
| DEC-GUI-19 | Demo Mode | only inside `/help` Guided tour, always bannered |
| DEC-GUI-20 | Product name | `KnowGridFlow` default; white-label variable |

Owner decisions still open (do not assume; mark `BLOCKED_DECISION` where they bite): D-04 IdPs/MFA; D-05 workspace model/isolation tier; D-07 separation of duties; D-08 real model runtime; D-09 reference hardware/datasets; D-10 report renderer licences; D-11 offline writes; D-12 CRDT; D-13 mobile approvals; D-14 locales; D-15 retention windows; D-16 telemetry consent; D-17 legal notices clearance; D-20 3D/Tauri (excluded from this baseline; MS-6/MS-7 VR/ZK excluded by user command).

---

## Appendix A — Screen × Endpoint matrix (primary integrations)

| Screen | Endpoints (method path) |
|---|---|
| SCR-001 | GET /health/ready · GET /api/v1/auth/health · POST /api/v1/auth/login · POST /api/v1/security/tokens/verify · GET /api/v1/tenancy/context |
| SCR-002 | GET /connectors/catalog · POST/PATCH /sources · POST /sources/{id}/discover · POST /ingest/profile(+keys,+relationships) · POST /sources/{id}/dry-run · POST /admin/validation · POST /sources/{id}/baseline · GET /admin/jobs/{id} · (Ask component) |
| SCR-003 | GET /graph/statistics · GET /admin/stats · GET /admin/jobs · GET /admin/system · GET /enterprise/diff/changes · GET /ontology/validate · GET /knowledge/debt · GET /suggest/intents |
| SCR-004 | POST /suggest/interpret · POST /query · POST /query/nl · POST /query/cost · POST /brain/llm/stream (SSE) · POST /evidence/manifest · POST /retrieval/search · GET /egress/endpoints · GET /admin/system · POST /enterprise/learning/feedback · GET /brain/approaches|dialects|rag-modes|loops|llm/models |
| SCR-005 | GET /search · GET /entities/{id} · POST /neighborhood · POST /path · POST /graph/shortest-paths · POST /lens/{lens_id} · GET /lens/catalog · GET /graph/schema · POST /graph/metrics|cluster|blast-radius|anomalies|surprises · GET /graph/orphaned|stale|pr-impact|as-of · POST /graph/convert · GET /export/formats · GET /graph/events (poll) |
| SCR-006 | GET /entities/{id} · POST /neighborhood · POST /graph/metrics · POST /graph/blast-radius|reverse-impact|what-if|similarity|link-prediction · POST /lineage · GET /query/why/{cid} · GET /enterprise/diff/timeline/{id} · GET /graph/versions · GET /identity/candidates · POST /identity/candidates/{id}/decide|reject · GET /catalog/products/{id}(+lineage) · POST /admin/entities/{id}/delete · GET /files/{path} |
| SCR-007 | POST /graph/blast-radius|reverse-impact · POST /impact · POST /causal/live-blast-radius · POST /causal/counterfactual-intervention · POST /simulation/create|{id}/mutate · GET /simulation/{id}/analyze|compare · GET /graph/pr-impact · POST /graph-tests/run · POST /twin/test-intelligence/select · POST /query/cost · POST /reports/render |
| SCR-008 | GET /change-journal · GET /enterprise/diff/changes|stats|timeline/{id} · GET /graph/versions|diff · POST /config/diff · GET/POST /compliance/changes · POST /compliance/changes/{id}/transition |
| SCR-009 | GET/POST /platform/incidents · GET /platform/incidents/{id} · POST …/transition · GET /platform/incidents/stats · POST /causal/hypotheses/{cid} · POST /causal/correlations/{cid} · POST /enterprise/correlation/analyze/{event_id} · GET /governance/incidents · POST /neighborhood|path · POST /graph/shortest-paths |
| SCR-010 | GET /graph/as-of · POST /graph/bitemporal/* · GET /graph/versions|diff · GET/POST/DELETE /enterprise/snapshots · POST …/compare|restore · POST /playback/stream|evidence|export · GET /admin/timeline · GET /brain/snapshot |
| SCR-011 | POST /query · /query/nl · /query/eql · /query/language · /query/explain · /query/cost · GET /query/history|slow · GET/POST/DELETE /query/templates(+bind) · POST /query/multi-paradigm · POST /federation/query · GET /federation/sources · GET /graph/backend · POST /admin/gremlin · GET /enterprise/audit/events |
| SCR-012 | GET /graph/schema · GET /admin/schema · GET /ontology/export|shacl|validate|drift · POST /ontology/diff|proposals|import · ontology/gitops/* · enterprise/migrations/* · taxonomy/* · domain-packs/* · marketplace/* · POST /brain/induce |
| SCR-013 | GET /graph/schema · GET /admin/stats · GET /ontology/drift · POST /ontology/diff · GET /ontology/export |
| SCR-014 | GET /connectors/catalog · sources/* (CRUD, ops, schedule, checkpoint, reconciliations, pause/resume) · systems/* · platform/integrations/* · GET /federation/sources |
| SCR-015 | GET /connectors/files/formats · POST /admin/ingestion/files/parse|files · GET …/files/bundles/{b}/{a} · POST /admin/ingestion/json|json/batch|jira|gitlab|confluence|servicenow · POST /ingest/profile(+keys,relationships,drift) · GET /ingestion/runs · GET /ingestion/dlq · POST /admin/dlq/{id}/replay · POST /admin/ingestion/replay |
| SCR-016 | GET /identity/candidates · POST …/decide|reject · GET /ontology/validate · GET /validation/runs · POST /admin/validation · GET /conformance/rules · POST /conformance/check · PUT /conformance/rules/{name} · GET /knowledge/debt · GET /knowledge-slos · POST /knowledge/slo · GET /knowledge/freshness · GET /knowledge/trust/states · GET /truth/contradictions · GET /truth/explain/{s}/{p} · POST /truth/resolve · POST /graph/anomalies · GET /graph/orphaned|stale |
| SCR-017 | GET /admin/jobs(+/{id}) · POST …/cancel|readmit · GET /ingestion/dlq · GET /admin/dlq · enterprise/dlq/* · POST /admin/dlq/{id}/replay · GET /pipeline/status · GET /admin/semantic-pipeline/stages · POST /admin/semantic-pipeline · GET /platform/harness/pipelines · POST /platform/harness/run · GET /admin/event-consumers · POST …/run · GET /admin/worker · GET /admin/timeline |
| SCR-018 | GET /agents · GET /agents/types · POST /agents/{id}/runs · GET /agents/runs/{id}(+memory,+explanation) · POST /agents/query|analytics|trace-impact · GET /agents/proposals · POST …/approve|reject · GET /agents/mesh/recoveries · POST …/recover/{id} · loops/* · POST /xai/certify-decision|verify-certificate · POST /platform/xai/explain|calibrate · GET /governance/kill-switch |
| SCR-019 | GET /reports · GET /reports/templates · POST /reports/render · GET /reports/export/{id} · reports/schedules/* · capsules/* · catalog/products/* · GET /graph/statistics |
| SCR-020 | (none — BACKEND-MISSING-016) |
| SCR-021 | GET /security/status|policy-matrix · GET /auth/health · authz/users|roles|policies(+reload)|evaluate|decisions|*/export · security/tokens/issue|verify|revoke · governance/models|templates|kill-switch(+features) · compliance/ai/* · egress/* · GET /admin/audit · enterprise/audit/* · compliance/packs|exceptions|roles · privacy/* |
| SCR-022 | GET /tenancy/context|quotas · POST /tenancy/quotas/check · tenancy/isolation/* · tenancy/lifecycle/* · config/* · GET/POST /config/flags · enterprise/feature-flags(+override) · GET /admin/system · platform/recovery/* · tenancy/metering/* · licensing/* |
| SCR-023 | GET /branding/theme|legal · GET /branding/locales/{l}/message · POST /branding/terminology/canonicalize|rename |
| SCR-024 | GET /admin/system|stats|worker|event-consumers · enterprise/health/* · GET /health/graph|embeddings · enterprise/observability/metrics · enterprise/analytics/* · enterprise/resilience/* · enterprise/lifecycle/* · platform/recovery/* · ops/* · GET /product/capabilities|first-choice-gate · GET /gaps/coverage|completion-gate · GET /graph/backend|backends · GET /metrics |
| SCR-025 | (local) · POST /brain/llm/tokenize (Expert) |
| SCR-026 | GET /platform/notifications/inbox/{p} · POST …/{id}/read · GET /platform/notifications/stats · POST /platform/notifications/send · GET /demo/scenarios · POST /path · GET /suggest/intents · GET /licensing/status · POST /licensing/check-module |
| SCR-027 | GET /health/ready (on Retry only) |

All remaining historical `INT-*` operations not listed above are classified **internal/service/alias/optional** for GUI purposes (no screen) unless an owner reassigns them; they remain in `GUI-UIX-requirements.md` §17 for reference. Unversioned `/brain/*` aliases (`INT-708..731`) are never called by the GUI.

## Appendix B — HTTP status → UI (see §8.3) and problem normalizer shape

```ts
type ApiProblem = {
  status: number;            // HTTP status or 0 for network
  title: string;             // problem.title | mapped default
  detail?: string;           // problem.detail | detail string
  code?: string;             // problem.error.code e.g. EOIP-SYS-500
  category?: string;         // problem.error.category
  severity?: string;         // problem.error.severity
  correlationId: string | null; // X-Correlation-ID | problem.correlation_id | X-Request-ID
  auditId?: string | null;   // X-Audit-ID
  fields?: { path: string; message: string; type?: string }[]; // 422 detail[]
  retryable: boolean;        // GET && (429|503|504|network)
};
```

## Appendix C — Design token seed (DTCG; generated files are derived from this)

```json
{"$schema":"https://www.designtokens.org/tr/2025.10/format/",
 "color":{"light":{"canvas":{"$value":"#F7F9FA","$type":"color"},"surface":{"$value":"#FFFFFF","$type":"color"},"raised":{"$value":"#F1F4F5","$type":"color"},"text":{"$value":"#172126","$type":"color"},"muted":{"$value":"#52636B","$type":"color"},"border":{"$value":"#CBD5D9","$type":"color"},"focus":{"$value":"#087F8C","$type":"color"},"brand":{"$value":"#006D77","$type":"color"},"accent":{"$value":"#D97706","$type":"color"},"success":{"$value":"#16805A","$type":"color"},"warning":{"$value":"#A15C00","$type":"color"},"danger":{"$value":"#C33241","$type":"color"},"info":{"$value":"#1769AA","$type":"color"}},
  "dark":{"canvas":{"$value":"#101518","$type":"color"},"surface":{"$value":"#172025","$type":"color"},"raised":{"$value":"#202B31","$type":"color"},"text":{"$value":"#F2F6F7","$type":"color"},"muted":{"$value":"#AEC0C7","$type":"color"},"border":{"$value":"#43545C","$type":"color"},"focus":{"$value":"#4DD5DF","$type":"color"},"brand":{"$value":"#43C3CC","$type":"color"},"accent":{"$value":"#F5A623","$type":"color"},"success":{"$value":"#4BC38B","$type":"color"},"warning":{"$value":"#FFC857","$type":"color"},"danger":{"$value":"#FF6673","$type":"color"},"info":{"$value":"#67B7F7","$type":"color"}}},
 "motion":{"micro":{"$value":"100ms","$type":"duration"},"short":{"$value":"160ms","$type":"duration"},"medium":{"$value":"240ms","$type":"duration"},"long":{"$value":"400ms","$type":"duration"},"easeStandard":{"$value":[0.2,0,0,1],"$type":"cubicBezier"},"easeEmphasized":{"$value":[0.2,0.8,0.2,1],"$type":"cubicBezier"}},
 "space":{"1":{"$value":"4px","$type":"dimension"},"2":{"$value":"8px","$type":"dimension"},"3":{"$value":"12px","$type":"dimension"},"4":{"$value":"16px","$type":"dimension"},"6":{"$value":"24px","$type":"dimension"},"8":{"$value":"32px","$type":"dimension"}},
 "radius":{"sm":{"$value":"2px","$type":"dimension"},"md":{"$value":"4px","$type":"dimension"},"lg":{"$value":"6px","$type":"dimension"},"xl":{"$value":"8px","$type":"dimension"}}}
```

HC themes derive from §5.2 and are validated by the token test, not hand-copied.

## Appendix D — Analytics dictionary

Required fields: `schema_version, event_name, occurred_at, screen_id, tenant_pseudonym, session_pseudonym, result, duration_bucket, offline, build_id`. Forbidden: prompt/query/source text, entity labels/properties, credentials, tokens, raw ids, exported content.

## Appendix E — Glossary (UI strings must use these)

Canonical entity · Source event · Evidence · Deterministic / Derived / Inferred / Ambiguous / Human-confirmed · Trust state · Knowledge age · Meta graph · QueryPlan · Lens · View (saved) · Workspace · Tenant · Principal · Job · Dry run · Baseline · Reconcile · Replay · DLQ (Dead-letter queue) · Blast radius · Reverse impact · What-if (simulation, non-mutating) · Snapshot · As of (valid time) / Known at (transaction time) · Proposal (agent, inert until applied by a separate workflow) · Approval (records a decision) · Abstain · Boundary (Local only / Approved external) · Mode (Deterministic / Narrated / Exploratory / Report / Simulated) · Demo Mode.

## Appendix F — Resolved corpus conflicts (for reviewers)

1 job status (→ §2.1) · 2 lens list (→ server catalog) · 3 modes (→ Simple/Advanced/Expert) · 4 fact/trust vocab (→ §2.2/§2.3) · 5 catalog vs knowledge-product states (→ verbatim backend) · 6 loop acronyms (→ glossary set) · 7 agent/MCP/RAG counts (→ never shown as marketing numbers; UI lists what the API returns) · 8 export formats (→ §2.12) · 9 WS path (→ `/ws/graph/events` exists; `/api/v1/ws/jobs/{id}` does not; GUI polls) · 10 upload type/limit (→ octet-stream; 3 MB UI / 4 MB API) · 11 domain list (→ manifest 14) · 12 backend list (→ `GET /graph/backends`) · 13 G2-UX/ADMIN redefinitions in audits (→ gaps2 definitions used) · 14 backlog totals (→ three-number reporting) · 15 product name (→ KnowGridFlow variable) · 16 stack (→ §4) · 17 WCAG (→ 2.2 AA) · 18 onboarding steps (→ SCR-002 8 steps) · 19 scenario pack counts (→ read from `/demo/scenarios`) · 20 federation modes (→ verbatim backend) · 21 docs/api-reference paths (→ code wins) · 22 Phase-4 UI-00x "completed" claims (→ not evidence) · 23 silent memory fallback (→ backend chip shows `active_backend`; mismatch with configured shows warning).

---

*End of document. Any statement a reader believes is an assumption must be filed as a drift incident against this document rather than silently worked around.*
