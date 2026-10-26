# Chapter 1 — The EOIP Web Application (Complete Workspace Guide)

This chapter documents every screen of the EOIP browser application (`apps/web`), grounded in the
actual source under `apps/web/src`. Every button label, endpoint path, and field name below is
quoted from the code. Where a screen calls an endpoint that does **not** exist in the current API
(`apps/api`), this is marked **[backend missing]** so you know what to expect before clicking.
Responses described from code alone (not exercised against a running server) are marked
*not runtime-verified*.

## Index

1. [Connecting (login) and session behavior](#1-connecting-login-and-session-behavior)
2. [Workspace shell and navigation](#2-workspace-shell-and-navigation)
3. [Knowledge Explorer](#3-knowledge-explorer)
   - 3.1 Search field and natural-language ask
   - 3.2 Search lens (results by domain)
   - 3.3 Graph lens: relationship map, filters, GraphCanvas, enhancement toolbar
   - 3.4 Entity inspector (Overview / Evidence), Explore impact, Run TraceImpact
   - 3.5 Impact lens: change impact studio, requirement→implementation path finder
   - 3.6 Evidence lens: lineage explorer and GraphRAG
   - 3.7 Architecture lens
   - 3.8 Agents lens (governed Deep Agents)
   - 3.9 KGR lens (multi-graph explorer)
   - 3.10 Lens library
4. [Cognitive Engineering hub](#4-cognitive-engineering-hub)
5. [Cognitive Dashboards](#5-cognitive-dashboards)
6. [Ontology Studio](#6-ontology-studio)
7. [Administration](#7-administration)
8. [Guided demo](#8-guided-demo)
9. [Appearance / settings](#9-appearance--settings)
10. [Error handling model](#10-error-handling-model)

---

## 1. Connecting (login) and session behavior

**What it does.** The app gates the whole workspace behind a single access-token form
(`apps/web/src/app/shell/Connection.jsx`). The token is held **in memory only** — the note under
the field reads literally: *"Deployment access. Your token remains in memory until you disconnect
or reload."* On startup the app also executes `sessionStorage.removeItem('eoip-token')`
(`App.jsx:947`) to delete any credential left over from older versions.

**How to access.** Open the app root (`/`, which resolves to `/app` — see
`apps/web/src/app/navigation.ts:13`). If you are not authenticated you always land on the
"Connect to EOIP" page.

**Step by step.**

1. Check the health orb: it polls `GET /health/ready` (`App.jsx:981`) and shows
   "Local services are ready" / "Checking local services" / "Service status unavailable".
2. Paste your access token into **Access token**. The eye icon toggles visibility
   (`aria-label="Show token"` / `"Hide token"`).
3. Click **Connect**. The app immediately calls three admin endpoints to validate the token:
   `GET /api/v1/admin/stats`, `GET /api/v1/admin/system`, `GET /api/v1/admin/jobs`
   (`App.jsx:963-966`). Only if all succeed are you let in.

**Response/result.** You land in the workspace shell. Every subsequent request goes through the
client in `apps/web/src/shared/api/client.ts`, which sends `Authorization: Bearer <token>` plus a
fresh `X-Request-ID` UUID per request, `credentials: 'same-origin'`, `cache: 'no-store'`, and
`redirect: 'error'`. The client refuses to send the token anywhere but this deployment's origin
("Only this deployment can receive authenticated requests.").

**Errors and recovery.**

- Wrong/expired token → the login `run()` wrapper shows an error toast with the API's `detail`
  message and a **Correlation ID** taken from the `X-Correlation-ID` response header
  (`client.ts:66`). Quote that ID when reporting the problem.
- "Service status unavailable" → the API is not up; fix the backend before connecting.
- **Disconnect** (logout icon, top bar) aborts every in-flight request (`api.dispose()`), clears
  token, graph, selection, and resets theme to light (`App.jsx:968-972`). Reloading the page has
  the same effect — the token is gone; there is no "remember me".

---

## 2. Workspace shell and navigation

**What it does.** After login, `WorkspaceShell.jsx` renders a left icon rail, a top bar, and a
command palette.

**How to access.** Always visible once connected.

**Step by step.**

- Left rail destinations (`apps/web/src/app/navigation.ts:1-9`):
  | Label | Path |
  |---|---|
  | Knowledge explorer | `/app` |
  | Cognitive Engineering | `/cognitive` |
  | Cognitive Dashboards | `/dashboards` |
  | Ontology studio | `/studio` |
  | Administration | `/admin` |
  | Guided demo | `/demo` |
  | Appearance | `/settings` |
- Press **Ctrl/Cmd + K** (or the magnifier tool "Open command palette") to open the "Go to"
  dialog; type to filter screens, click or Enter to jump.
- Top bar tools: **Refresh live data** (re-runs `GET /api/v1/admin/stats|system|jobs`),
  **Disconnect this browser session**. A chip reads "Deployment access" with the tooltip
  *"tenant/workspace grants are not available in this login flow"* — there is no tenant switcher.
- While connected, the app silently refreshes stats/system/jobs every **15 seconds** when the tab
  is visible (`App.jsx:987`).

**Errors and recovery.** Navigating to an unknown path shows "Page not found" with an
"Open knowledge explorer" button. Each screen is wrapped in `RouteBoundary` so a crash in one
workspace does not kill the session.

---

## 3. Knowledge Explorer

Route: `/app` (`Explorer` in `App.jsx:348`). Top of the screen shows four live metric cards fed by
`GET /api/v1/admin/stats`: **ENTITIES** (`stats.vertices`), **RELATIONSHIPS** (`stats.edges`),
**ENTITY TYPES**, **WORKER** (`stats.worker.status`). Below them is the lens tab bar: **Search,
Graph, Impact, Evidence, Architecture, Agents, KGR**, plus **All lenses** (library, §3.10), a
context chip showing the currently selected entity, and an **Export context** icon that downloads
`eoip-knowledge-context.json` (lens, query, root entity IDs, domain list — built entirely
client-side, `App.jsx:384-388`).

### 3.1 Search field and natural-language ask

**What it does.** Two search forms: keyword search against the persisted graph, and a plain-language
ask box that the API interprets as a bounded QueryPlan.

**How to access.** Top of `/app`. API equivalents:
`GET /api/v1/search?q=<text>` and `POST /api/v1/query/nl`.

**Step by step.**

1. Type in "Search entities and relationships" (or click a suggestion chip: `EOIP-1`, `Order`,
   `Payment`, `Service`, `Authentication`) and press **Search graph ↵**.
2. For natural language, use the second box ("Ask in plain language — e.g. what implements
   EOIP-1…") and press **Ask graph ↵**. Suggested questions: `What implements EOIP-1?`,
   `What is impacted by payment-svc?`, `Explain checkout dependencies`.

API equivalents:

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/search?q=EOIP-123"

curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"question":"What implements EOIP-123?"}' \
  http://localhost:8000/api/v1/query/nl
```

**Response/result.** Both fill the shared `graph` object `{nodes, edges, paths, evidence,
warnings, partial}` used by every lens. The NL box also shows an interpretation banner:
*"Interpreted as <intent> plan — <explanation> · N entities returned"*, or a clarification message
if the question could not be mapped to a plan. `graph.warnings` render as a yellow inline notice;
`graph.partial: true` shows "This is a bounded result."

**Errors and recovery.** Empty input is blocked (`required`). API errors surface in the global
error toast with correlation ID. A clarification response means: rephrase or use keyword search.

### 3.2 Search lens (results by domain)

**What it does.** Groups the current result set by `node.domain` ("Results by knowledge domain",
`App.jsx:275`). Each row shows a color-coded type dot, display label, entity type, and truncated
canonical ID. Display label priority is `issue_key → display_name → name → qualified_name → path →
label` (`displayLabel`, `App.jsx:41`).

**How to access.** Lens tab **Search**.

**Step by step.** Run a search (§3.1) → open **Search** → click any row to inspect it (this calls
`GET /api/v1/entities/{id}` and makes the entity the shared lens context).

**Errors and recovery.** "No matching entities" empty state appears when the graph is empty —
run a search first.

### 3.3 Graph lens: relationship map, filters, GraphCanvas, enhancement toolbar

**What it does.** Interactive Cytoscape map ("Relationship map") of the bounded result
(`GraphView`, `App.jsx:308`).

**How to access.** Lens tab **Graph**.

**Step by step.**

1. Use the three filter selects in the panel header:
   - **Filter graph by domain** — values derived from `node.domain` in the current result.
   - **Filter graph by relationship** — derived from `edge.type`.
   - **Filter graph by trust status** — `All trust / Deterministic / Inferred`, matched against
     `edge.creation_status` (default `DETERMINISTIC`).
2. Interact with the canvas (`apps/web/src/GraphCanvas.jsx`):
   - **Click a node** → opens the entity inspector (§3.4). **Click an edge** → opens the
     relationship inspector showing type, from/to IDs, evidence (`source_ref`/`evidence_key`),
     and all edge properties.
   - **Double-click a node** → expands its neighborhood via
     `POST /api/v1/neighborhood {"canonical_id": "<id>", "max_depth": 1, "result_limit": 75}`.
   - Canvas toolbar: **Zoom in / Zoom out / Fit all entities in view / Show–Hide graph labels**,
     and a layout select: Organic (cose), Hierarchy (breadthfirst), Circle, Grid, Orthogonal
     (orthogonal uses taxi/bezier edge routing and a grid layout, `GraphCanvas.jsx:182-185`).
   - Semantic zoom is automatic: zoom < 0.3 renders cluster mode (labels off, small nodes),
     < 0.8 entity mode, above that full detail (`getSemanticZoomLevel`).
3. The **GraphEnhancementToolbar** (`apps/web/src/kgr/enhancements/GraphEnhancementToolbar.jsx`)
   wraps the canvas:
   - **Theme toggle** (☾/☀ Light/Dark) — graph-local theme stored in
     `sessionStorage['eoip-graph-theme']` (`theme.jsx`).
   - **Layout select**: Force directed / Hierarchical / Circular — computed in pure JS
     (`kgr/enhancements/layouts.js`); "force" delegates to Cytoscape's `cose` when available.
   - **Lasso select** toggle — drag a rectangle over nodes (`LassoSelect.jsx`); with ≥2 nodes
     selected, **Collapse selection** replaces them with one synthetic "Group N (k)" node;
     clicking the group expands it again. All client-side; no API call.
   - **Minimap** toggle — SVG overview (`GraphMinimap.jsx`); click/drag inside it to pan the main
     canvas.
4. Below the canvas: an entity-type **legend**, an edge key (Deterministic = solid grey,
   Inferred = dashed amber, Highlighted path = thick violet, thicker links carry evidence), and
   the "Entities in view" strip (click to inspect).

**Errors and recovery.** If the layout algorithm throws, the canvas falls back to `grid`
(`GraphCanvas.jsx:186-188`). "No relationships to display" empty state → run a search first.

### 3.4 Entity inspector: Overview / Evidence, Explore impact, Run TraceImpact

**What it does.** Right-hand panel (`EntityInspector`, `App.jsx:181`) for the selected node or edge.

**Step by step.**

1. Select any node. Header shows type and display label; the canonical ID sits in an identity bar
   with a **Copy canonical ID** chip.
2. **Overview tab** action buttons:
   - **Explore impact** → `POST /api/v1/impact {"canonical_id": "<id>", "max_depth": 4}` and
     switches you to the Impact lens with the returned subgraph.
   - **Run TraceImpact** → `POST /api/v1/agents/trace-impact {"canonical_id": "<id>"}` — the
     deterministic read-only agent.
   - Shield icon **Trace provenance lineage** → `POST /api/v1/lineage {"canonical_id": "<id>",
     "max_depth": 4}` and switches to the Evidence lens.
   - Below: "Entity properties (N)" with a **Filter props…** box (appears when there are >4
     properties).
3. **Evidence tab** lists relationships that carry `source_ref` or `evidence_key`, with a count
   badge. Empty state suggests using the Evidence lens for a broader chain.

**Errors and recovery.** "No direct evidence returned" means none of the entity's relationships
carried evidence references — not an error.

### 3.5 Impact lens: change impact studio and requirement→implementation path

**What it does.** Two panels (`ImpactView`, `App.jsx:321`): bounded downstream traversal from the
selected anchor, and a canonical-ID path finder.

**How to access.** Lens tab **Impact**. API: `POST /api/v1/impact`, `POST /api/v1/path`,
`POST /api/v1/agents/trace-impact`.

**Step by step.**

1. Select an entity in Graph first — the "CURRENT ANCHOR" callout shows it; buttons stay disabled
   until you do.
2. **Explore impact** / **Run TraceImpact** as in §3.4.
3. **Trace requirement to implementation** (Path Finder): enter **From canonical ID** and
   **To canonical ID** (selecting a node auto-fills both with its ID — edit the target), then
   **Find path**. Equivalent curl:

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"source_id":"requirement:EOIP-123","target_id":"service:checkout"}' \
  http://localhost:8000/api/v1/path
```

**Response/result.** "N evidence paths found · X entities · Y relationships"; path edges highlight
violet in the Graph lens. If the impact result carries `meta.impact_rationale`, a "Why each entity
is included" panel lists per-node reasons. A TraceImpact result panel shows
`summary`, `partial` (PARTIAL/COMPLETE pill), and `evidence_refs`.

**Errors and recovery.** No path → the panel simply doesn't appear; check the IDs exist (search
for them first) and that the relationship direction is permitted.

### 3.6 Evidence lens: lineage explorer and GraphRAG

**What it does.** Left: provenance chain for a canonical ID. Right: "Ask with evidence" — grounded
context retrieval.

**How to access.** Lens tab **Evidence**. API: `POST /api/v1/lineage`, `POST /api/v1/rag`.

**Step by step.**

1. **Trace lineage**: enter an entity canonical ID (auto-filled with the current selection) and
   submit → `POST /api/v1/lineage {"canonical_id": "service:checkout", "max_depth": 4}`. Clicking
   a lineage node inspects it.
2. **Ask with evidence**: write a question (default "Explain the implementation and its
   evidence") and click **Retrieve trusted context** →
   `POST /api/v1/rag {"canonical_id": "<selected id>", "question": "...", "synthesize": false}`.
   Requires a selected entity; otherwise an inline notice tells you to pick one in the Graph lens.

**Response/result.** RAG panel shows strategy pill, `N contexts · M citations`, optional `answer`
(only when the backend synthesizes; the UI always sends `synthesize: false` — "Generation remains
optional"), and context cards with `kind`, `ref`, `text`, `citations`.

### 3.7 Architecture lens

**What it does.** A live projection of the current result: domain cards ("N visible entities" per
domain), an "Ontology baseline" panel (`stats.schema.ontology_version`, `schema_version`, entity
type count, `stats.backend`), and a "Relationship model" bar chart of edge types in the result
(`ArchitectureView`, `App.jsx:284`). No extra API calls — derived from `stats` + current graph.

### 3.8 Agents lens (governed Deep Agents)

**What it does.** Catalog + bounded runner for governed agents (`AgentView`, `App.jsx:337`).

**How to access.** Lens tab **Agents**. Opening it loads `GET /api/v1/agents`.

**Step by step.**

1. Pick an agent in the left catalog (shows `agent_type · risk_level · human_control`).
2. Review the policy strip: **max steps**, **deadline (s)**, **allowed tools count**, and the
   READY/DISABLED pill (`contract.enabled`).
3. Edit the **Goal** (max 4096 chars). For `GraphInvestigator`, an extra toggle appears: "Use the
   configured local model for evidence-grounded synthesis".
4. Optionally select a graph entity first — its ID is sent as `context_refs`.
5. Click **Run governed agent**:

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"goal":"Explain the impact, supporting evidence, and uncertainty",
       "context_refs":["service:checkout"],"dry_run":false,"synthesize":false}' \
  http://localhost:8000/api/v1/agents/TraceImpact/runs
```

**Response/result.** Status pill, `summary`, confidence %, evidence refs, policy `rule_decisions`
(`rule_id · outcome · summary`), uncertainty warnings, and — if present — "N inert change
proposal(s) await explicit human approval. Approval does not automatically apply a mutation."

**Errors and recovery.** A DISABLED agent cannot be run (button disabled). Errors land in the
global toast.

### 3.9 KGR lens (multi-graph explorer)

**What it does.** The full Knowledge Graph Renderer (`kgr/KGRExplorer.jsx`, ~986 lines): ten graph
types and deep per-node analytics.

**How to access.** Lens tab **KGR**.

**Step by step.**

1. **Graph type bar** (keyboard shortcuts `1..9,0`): Knowledge, Relationships, Metadata, Ontology,
   Temporal, Provenance, Impact, Similarity, Diff, Health.
2. **Filter bar** (toggle with `f`): domain, entity type, relationship, trust
   (Deterministic/Inferred/Ambiguous/Manual), evidence (Evidenced/UnevIDenced), source connector,
   min-degree, temporal from/to dates, community, in-view text search; active filters render as
   removable chips. `/` focuses the in-view search.
3. On load it fetches `GET /api/v1/graph/schema` to populate filters. Selecting a node fires two
   calls: `GET /api/v1/entities/{id}` and `POST /api/v1/graph/metrics {"canonical_ids":[id]}`.
4. **Node inspector tabs** (Overview, Relationships, Impact, Centrality, Similar, What-If,
   Evidence, Notes) with these backing calls:
   - **Impact / Blast radius**: `POST /api/v1/graph/blast-radius {"canonical_id","max_depth":4}`
     plus `POST /api/v1/graph/reverse-impact` (upstream dependents). Results render as a ring
     overlay ("N affected entities", per-hop bars, type breakdown) and an "Explore blast radius"
     button that reloads the graph via `POST /api/v1/impact {…, "result_limit":200}`.
   - **Centrality**: `POST /api/v1/graph/centrality/full` with algorithms
     `degree, betweenness, closeness, pagerank, eigenvector, katz, hits, harmonic` — shown as
     metric cards plus a radar chart.
   - **Similar**: `POST /api/v1/graph/similarity {"canonical_id","algorithm":"jaccard","limit":10}`.
   - **What-If**: `POST /api/v1/graph/what-if {"canonical_id","action":"remove"}` → broken edges,
     affected neighbors, orphaned entities.
   - **Notes**: stored in browser `localStorage` under `kgr-note-<id>` only.
5. **Toolbar** (layout, size mode, fit, minimap `m`, filters, entity list, export menu, fisheye
   `Shift+F`, color-blind palettes, table view `t`, deep-link copy (base64 state in URL hash),
   lasso selection, combo/group-by domain|type|community `g`, playbooks, style rules, AI explorer
   `a`, surprises). Surprises load `POST /api/v1/graph/surprises {"limit":20}`.
   The query builder posts to `POST /api/v1/query`. Structural analysis in the Impact type calls
   `POST /api/v1/graph/k-core {"min_k":1}`, `POST /api/v1/graph/components {"limit":20}`, and
   `GET /api/v1/graph/degree-distribution`.
6. Large graphs: ≥1000 nodes render progressively (batches of 100 with a progress bar); ≥5000
   nodes switch to a WebGL Sigma renderer ("WebGL" badge). A WebSocket event feed
   (`kgr/hooks/useGraphEvents.js`) shows live graph events with pause/resume/clear and a
   connection dot.

**Errors and recovery.** Escape clears selection/menus. Ctrl+Z / Ctrl+Shift+Z undo/redo the
exploration history (client-side). Auxiliary analytics calls use `.catch(() => null)` so a missing
metric degrades gracefully instead of erroring.

### 3.10 Lens library

**What it does.** A modal (`LensLibrary`, `App.jsx:297`) listing 20 experience lenses with honest
status pills: 12 marked **AVAILABLE** ("API-backed") and 8 marked **PLANNED** (Timeline, Change,
Runtime, Release, Process, Simulation, Decision, Test) — these are disabled with the tooltip
*"{name} requires a later roadmap backend and is not represented with fake data"*. Selecting an
available catalog lens routes to its backing tab (e.g. Requirement→Impact, Trust→Evidence,
Ontology→Architecture).

**How to access.** Lens bar → **All lenses** button. Escape or clicking the backdrop closes it.

---

## 4. Cognitive Engineering hub

**What it does.** Route `/cognitive` (`cognitive/CognitiveHub.jsx`): six studios behind tabs —
"15 Engineering Disciplines", "Reflection Sandbox & Inoculator", "Attention Slicer & Bitemporal",
"Graph Repair & Distillation", "External MCP & Attestation", "Token Economics & Latency". The hero
banner claims "DISCIPLINES COMPLETE 15 / 15 (100%)" and "SECURITY GATES ACTIVE & BOUNDED" — these
are static strings, not live telemetry.

### 4.1 Discipline Matrix (15 Engineering Disciplines)

`DisciplineMatrix.jsx` renders 15 cards, each bound to a real endpoint with a prefilled JSON body:

| Discipline | Endpoint | Method |
|---|---|---|
| Loop Engineering | `/api/v1/graph-loop/execute` | POST |
| Graph Engineering | `/api/v1/graph/schema` | GET |
| Harness Engineering | `/api/v1/demo/scenarios` | GET |
| Memory Engineering | `/api/v1/memory/recall` | POST |
| Context Engineering | `/api/v1/context/slice-graph` | POST |
| Prompt Engineering | `/api/v1/eval/distill-prompts` | POST |
| Graph-over-Loop | `/api/v1/graph-loop/execute` | POST |
| Loop-over-Graph | `/api/v1/graph-loop/execute` | POST |
| Evaluation & Benchmarking | `/api/v1/eval/suite/run` | POST |
| State & Persistence | `/api/v1/context/bitemporal-slate` | POST |
| Tool & API Contracts (MCP) | `/api/v1/tools/list` | GET |
| Security & Red-Teaming | `/api/v1/guardrails/reflection-sandbox` | POST |
| Cost & Latency Optimization | `/api/v1/tools/stats` | GET |
| Feature Engineering | `/api/v1/context/slice-graph` | POST |
| Spec Engineering | `/api/v1/graph/schema` | GET |

**Step by step.** Click a card → edit the "Request JSON Payload" (POST only) → **Execute
<name>**. The right console shows the raw JSON response and measured duration in ms; "Copy JSON"
copies it. Invalid JSON in the payload box fails locally with "Invalid JSON payload in execution
configuration".

**Backend note.** These endpoints are registered by `packages/eoip/platform_router.py` (mounted in
`apps/api/extended.py:1530-1531`) — e.g. `graph-loop/execute` (platform_router.py:1591),
`eval/suite/run` (:1626), `memory/recall` (:1650), `context/slice-graph` (:1756),
`context/bitemporal-slate` (:1774), `tools/list` (:1576), `tools/stats` (:1583),
`guardrails/reflection-sandbox` (:1736), `eval/distill-prompts` (:1784). Available in deployments
that include the extended router; *not runtime-verified here*.

### 4.2 Reflection Sandbox & Inoculator

`ReflectionSandboxStudio.jsx`. Left panel simulates an agent action inside the formal sandbox:

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"step_id":"agent-step-101","action_type":"MUTATE","target_entity":"APIService",
       "proposed_payload":{"service_name":"checkout-api","version":"v2.1","timeout_ms":3000},
       "agent_role":"operator","state":{"last_executed_step":"agent-step-100"}}' \
  http://localhost:8000/api/v1/guardrails/reflection-sandbox
```

**Step by step.** Pick a preset (Safe Mutation / Forbidden Target / Role Violation) or fill Step
ID, Agent Role (operator/analyst/admin), Action Type (QUERY/MUTATE/DELETE/REFLECT), Target Entity,
and JSON payload → **Execute Inside Reflection Sandbox**. Result: "VERIFIED ALLOWED" or "BLOCKED
BY INVARIANT" pill plus a list of `violations` (`rule_id`, `message`).

Right panel (Jailbreak Inoculator): choose a prompt template (`trace_impact`,
`graph_investigator`, `code_audit`, `rag_synthesis`) → **Run Inoculation Probes & Defend Prompt**
→ `POST /api/v1/guardrails/inoculate {"target_prompt_name":"trace_impact"}`. Shows resistance
score, probes tested/blocked, and the inoculated prompt text with a **Copy Shield** button. Note:
the displayed numbers fall back to hard-coded placeholders (96%, 4/4) if the response omits those
fields — read the raw JSON to be sure.

### 4.3 Attention Slicer & Bitemporal (Context Slicing Studio)

`ContextSlicingStudio.jsx`. Left: `POST /api/v1/context/slice-graph` with
`{"query", "seed_ids": [...], "attention_threshold": 0.0-0.9}` (default seeds
`checkout-api, payment-svc`). Result shows `total_candidates`, `retained_count`,
`compression_ratio`, per-entity attention scores, and `rendered_context` markdown.
Right: `POST /api/v1/context/bitemporal-slate` with
`{"stream", "past_timestamp", "present_timestamp"}` (epoch floats) → side-by-side Past (T0) /
Present (T1) JSON states and `deltas`. If the response omits state fields the UI renders
placeholder stubs (`{status:'INITIAL'}` / `{status:'DEPLOYED'}`) — treat those as illustrative.

### 4.4 Graph Repair & Distillation (Sentinel studio)

`SentinelDistillationStudio.jsx`. Left: paste Vertices/Edges JSON (or use the orphan presets) →
**Detect Topology Anomalies & Auto-Repair** → `POST /api/v1/eval/graph-repair-sentinel
{"nodes":[…],"edges":[…]}`. Shows `orphans_found`, `repairs_synthesized`, convergence telemetry,
and the synthesized remediation edges. Right: **Harvest Exemplars & Distill Prompt** →
`POST /api/v1/eval/distill-prompts {"target_prompt_name":"trace_impact","benchmark_name":
"standard_core_suite"}` → exemplar counts and the updated prompt template. Placeholder fallbacks
apply here too when fields are absent.

### 4.5 External MCP & Attestation

`McpAttestationStudio.jsx`. Left (Universal External MCP Client): server ID, transport
(HTTP/SSE/STDIO), endpoint URL, and a JSON array of tool names → **Connect & Discover External
MCP Server** → `POST /api/v1/tools/mcp/connect-external {"server_name","transport","endpoint",
"provided_tools":[…]}` (platform_router.py:1802). Right (Attestor): caller ID, tool name, JSON
arguments → **Invoke & Cryptographically Sign Execution** → `POST /api/v1/tools/attest-execution`
→ renders a certificate card (`certificate_id`, `caller_id`, `tool_name`, `payload_hash`,
HMAC-SHA256 `signature`; some fields fall back to sample strings if absent). **Verify Signature
Authenticity** → `POST /api/v1/tools/verify-attestation {"certificate_id": "…"}` →
"VERIFIED CRYPTOGRAPHICALLY AUTHENTIC" / "SIGNATURE MISMATCH".

### 4.6 Token Economics & Latency

`TokenEconomicsStudio.jsx` — a **pure client-side calculator** (no API calls). Sliders for daily
query volume, prompt/completion tokens, attention compression, and cache hit rate; outputs monthly
unoptimized vs optimized spend and a 3-tier model cost/latency matrix (prices are hard-coded:
$3.00/$15.00 per 1M tokens for "Frontier", etc.). Use it for forecasting, not billing data.

---

## 5. Cognitive Dashboards

Route `/dashboards` (`dashboards/EngineDashboardsHub.jsx`) — 11 tabs labeled with requirement IDs.

### 5.1 Causal Blast Radius (UI-01)

`CausalBlastRadiusDashboard.jsx`. Set Seed Entity ID (default `cyber-asset-gw-01`), Initial Shock
Magnitude, Max Cascade Depth (1–8), Failure Threshold → **Simulate Blast Radius**:

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"shock_entities":{"cyber-asset-gw-01":0.85},"max_depth":3,
       "failure_threshold":0.5,"dampening_factor":0.85}' \
  http://localhost:8000/api/v1/causal/live-blast-radius
```

Then pick a target node and resilience % → **Apply Counterfactual Intervention** →
`POST /api/v1/causal/counterfactual-intervention {"shock_entities", "interventions", "max_depth"}`.
Both routes exist in `packages/eoip/enterprise/advanced_router.py:77,86`. Result cards show total
impacted nodes, propagation depth, severity rating, affected entity list. Note: some displayed
values have fallbacks (`severity_rating || 'HIGH'`, `reduction_percentage || '72%'`,
`prevented_failures_count || 4`) — fields missing from the response show illustrative numbers.

### 5.2 Multi-Paradigm Query (UI-02)

`MultiParadigmQueryDashboard.jsx` → `POST /api/v1/query/multi-paradigm {"query",
"seed_canonical_ids", "max_depth", "monte_carlo_samples"}`. Kernel tabs: Harmonized Synthesis,
Deterministic, Probabilistic, Heuristic, Stochastic, Neural/LLM. Harmonized view shows
`harmonized_answer`, `confidence` (fallback 94%), `consensus_score` (fallback 0.92); other kernels
show raw JSON or a "Kernel converged successfully." stub if the kernel key is absent.

### 5.3 Domain Packs (UI-03)

`DomainPackDashboard.jsx` → `GET /api/v1/domain-packs` on load (falls back to an all-inactive
local map if it fails), `POST /api/v1/domain-packs/{id}/activate {"seed_live_topology": true}`.
Eight packs: bfsi, cybersecurity, healthcare, compliance, data-governance, itsm, manufacturing,
software-engineering. Toggle "Seed Live Topology on Activation" before activating.

### 5.4 XAI Verification (UI-04)

`XAIVerificationDashboard.jsx` → `POST /api/v1/xai/certify-decision {"decision_id", "agent_id",
"decision_summary", "attribution_factors":{…}}`, then **Verify Cryptographic Seal** →
`POST /api/v1/xai/verify-certificate {"certificate_payload": …}`. Shows Merkle root hash,
timestamp seal, and a verified-intact banner. Placeholder fallback for the hash if absent.

### 5.5 Timeline / Change / Runtime / Release / Process / Simulation lenses (UI-007)

These six tabs are **mostly static scaffolding** — honest status:

- **Timeline Lens** (`TimelineLens.jsx`): a working "Time Scrubber" slider (T−N hrs badge). No API.
- **Change Lens** (`ChangeLens.jsx`): an empty `DataGrid` ("Recent Graph Mutations") with columns
  Change ID/Entity/Type/Timestamp. No data source wired.
- **Runtime Lens** (`RuntimeLens.jsx`): hard-coded metric tiles (Active Agents 14, Token Budget
  42.3%, Circuit Breaker CLOSED). Not live data.
- **Release Lens** (`ReleaseLens.jsx`): empty grid of deployment milestones.
- **Process Lens** (`ProcessLens.jsx`): descriptive text only.
- **Simulation Lens** (`SimulationLens.jsx`): two buttons ("Run DB Outage Simulation", "Run AZ
  Partition Simulation") with **no onClick handlers** — they do nothing yet.

### 5.6 Search Analytics (UI-008)

`SearchAnalyticsDashboard.jsx`: hard-coded KPI tiles (Total Searches 24,890, Zero-Result Rate
1.4%, etc.), a synonym form whose **Add Synonym** button has no handler, two inert A/B experiment
buttons, and an empty "Top Query Volume" grid. Entirely illustrative — not backed by an API.

---

## 6. Ontology Studio

Route `/studio` (`studio/Studio.jsx`) — six tabs. Also embedded inside Administration →
Sources & jobs.

### 6.1 Schema Canvas (GAP-STUDIO-002)

`SchemaCanvas.jsx`. Loads `GET /api/v1/graph/schema`; on failure you get a warning and can still
add custom classes manually. Drag a class from the palette (or double-click it) onto the SVG
canvas, drag from a node's bottom port to another node to draw a relationship of the type chosen
in the toolbar select, drag nodes to move, click to select, **Remove selected** to delete.
**Export draft JSON** downloads `ontology-schema-draft.json` in format
`eoip.ontology-schema-draft.v1`. The code states explicitly: *"Export only — no backend write
endpoint exists for schema drafts. Save the JSON and promote it via config/ontology."*

### 6.2 Query Console (GAP-STUDIO-003)

`QueryConsole.jsx`. Language tabs: **EQL** (`POST /api/v1/query/eql {"query"}`) and **EOQL /
OSQL / Semantic QL** (`POST /api/v1/query/language {"language","query"}`). Ctrl+Enter runs.
History (last 50) persists in `sessionStorage['eoip-studio-query-history']`; click a chip to
reload a query, **Clear history** to wipe. Result pane shows JSON and latency in ms; warnings are
collected from response keys `warnings`, `safety`, `guards`, `notices`, plus `truncated`,
`partial`, and `max_results_exceeded` flags. The UI notes: "Guarded execution — destructive
statements are rejected by the API."

### 6.3 Connector Builder (GAP-NOCODE-001)

`ConnectorBuilder.jsx`. Four-step wizard (Source → Connection → Auth → Scope). Source catalog comes
from `GET /api/v1/connectors/catalog` with a built-in fallback list (jira, gitlab, github,
confluence, servicenow, web, local_code, generic) when that fails. Auth types: none/token/basic/
oauth2; fields flagged secret are redacted as `<redacted>` in the manifest. Client-side validation
blocks download until name, auth fields, `base_url` (for API sources), and scope entities are set.
**Download manifest** produces `eoip.connector-manifest.v1` JSON; **Save to library** stores it in
`localStorage['eoip-studio-connectors']` (max 30) so the Pipeline Orchestrator can use it. No
server write.

### 6.4 Mapping Designer (GAP-NOCODE-002)

`MappingDesigner.jsx`. Loads the graph schema, then: paste or upload a sample JSON document → its
flattened fields appear as draggable chips → add vertex mappings (target labels from the schema)
and edge mappings → drag fields onto property slots or pick them from selects → choose a key
property. Validation requires a name, a sample, ≥1 vertex, and ≥1 bound property per vertex.
**Download mapping** exports `eoip.field-mapping.v1` JSON; **Save to library** uses
`localStorage['eoip-studio-mappings']`. No server write.

### 6.5 Pipeline Orchestrator (GAP-NOCODE-003)

`PipelineOrchestrator.jsx`. Drag saved connectors/mappings (plus an "Add validation step" helper)
onto the DAG canvas, connect output ports, and the tool derives a topological run order.
**Cycles block export** ("The pipeline graph has a cycle — remove a link before exporting").
**Export pipeline JSON** downloads an `eoip.pipeline.v1` document with ordered `steps` and
`depends_on` indices. Purely client-side; no execution endpoint is called.

### 6.6 System Registry

`SystemRegistry.jsx` — backed by the real systems router (`packages/eoip/systems/router.py`,
prefix `/api/v1/systems`).

- List view: `GET /api/v1/systems/` (cards with type badge and colored status), plus
  `GET /api/v1/systems/known-types`.
- **Register System**: form (type from 35 known types, name, base URL, API version, auth type —
  none/api_key/bearer_token/basic_auth/oauth2/certificate/aws_iam/service_account — ingestion mode
  scheduled/event_driven/manual/streaming, poll interval, batch size, entity types, tags, optional
  JSON sample, auto-onboard checkbox) → `POST /api/v1/systems/register`.
- Detail view buttons: **Test Connection** → `POST /api/v1/systems/{id}/test-connection`;
  **Re-onboard** → `POST /api/v1/systems/{id}/onboard {"sample_data"}`;
  **Generate Schema** → `POST /api/v1/systems/{id}/generate-schema {"sample_data"}` (shows GraphQL
  SDL, JSON Schema, field mappings, golden queries, validation rules, with an Export download);
  **Remove** → `DELETE /api/v1/systems/{id}` (with confirm dialog).

**Errors and recovery.** This panel uses browser `alert()` for errors (e.g. "Registration
failed: …"), unlike the rest of the app's toast — and an empty list on `GET /systems/` failure is
swallowed silently, so check the error console if the list is unexpectedly empty.

---

## 7. Administration

Route `/admin` (`Admin` in `App.jsx:630`). Header actions: **Run validation**
(`POST /api/v1/admin/validation`, jumps to Quality tab) and **Load / replay demo**
(`POST /api/v1/admin/demo`). Four metric cards: graph entities, relationships, job success %
(computed client-side from completed jobs), and schema version. Tabs: **Overview, Sources & jobs,
JSON Ingestion & Convert, Quality & ontology, Users & policy, Live operations, Audit & recovery**.

### 7.1 Overview

- **Ingestion jobs** table (`GET /api/v1/admin/jobs`, **Refresh jobs** button). Result column shows
  per-kind summaries; HELD jobs show "Recovery hold: review possible side effects before
  re-admission".
- **Service health** list (from `GET /api/v1/admin/system` + stats): HugeGraph, Ingestion worker,
  Schema bootstrap, Local model (optional — "deterministic fallback active" if absent), Backup
  state (latest checksummed snapshot).
- **Graph inventory**: live per-label counts; zero-count types stay visible intentionally.

### 7.2 Sources & jobs

Connector cards with these actions:

- **Demo dataset → Load dataset**: `POST /api/v1/admin/demo` (idempotent).
- **Jira JSON → Import Jira**: file picker (JSON ≤ 3 MB) → `POST /api/v1/admin/ingestion/jira
  {"document": …}`.
- **GitLab metadata → Import GitLab**: `POST /api/v1/admin/ingestion/gitlab`.
- Confluence, ServiceNow, Rally, Grafana, Datadog, Kibana, qTest, Figma, API Portal, GitHub cards
  → **Queue dry run**: `POST /api/v1/admin/ingestion/{source} {"checkpoint": <iso|null>,
  "watermark": null, "dry_run": true}` (status "Configured externally" — credentials live in
  worker configuration, not the UI).
- **Incremental sync options** panel: Checkpoint (ISO-8601) input and a "Dry run only" toggle
  (default on).

**Source onboarding ("Registry and discovery")**: pick a connector from the catalog strip
(`GET /api/v1/connectors/catalog`), fill Source ID, type, name, Base URL, and Token secret ref
(e.g. `env://JIRA_TOKEN`) → **Create source** → `POST /api/v1/sources` with a capabilities object
derived from catalog modes. Secrets are referenced, never stored.

**Source registry** ("Registered sources", **Load source control** → `GET /api/v1/sources`):
per-row action buttons — **Discover** (`POST /api/v1/sources/{id}/discover`), **Baseline**,
**Dry run**, **Sync**, **Reconcile**, **Replay** (each `POST /api/v1/sources/{id}/{operation}`
with `{checkpoint, dry_run}`; buttons appear only if the source's capabilities allow them),
**Enable/Disable** (`PATCH /api/v1/sources/{id} {"enabled": bool}`), **Delete**
(`DELETE /api/v1/sources/{id}`, confirm dialog). Discovery results render as truncated JSON
(first 20 items).

**Durable queue**: jobs table with **Cancel** (`POST /api/v1/admin/jobs/{id}/cancel`, for
PENDING/HELD) and **Readmit** (`POST /api/v1/admin/jobs/{id}/readmit`, HELD only, with a confirm
warning that side effects may repeat).

### 7.3 JSON Ingestion & Convert

- Drag-and-drop or browse JSON files (entity arrays, nested docs, NormalizedEntity envelopes).
- **Process & Build Graphs** → per file `POST /api/v1/admin/ingestion/json {"data",
  "source_label": <filename>, "pipeline_id": "manual_gui"}`; summary cards show
  `entities_created`, `relationships_created`, `error_count`, `metadata_vertices`, plus an error
  table (first 20).
- **Process, Build & Convert All Formats** → `POST /api/v1/admin/ingestion/process-and-convert`.
- **Format conversion**: **Load formats** (`GET /api/v1/graph/formats`), pick one of RDF (Turtle),
  RDF/XML, RDFS, OWL, Gremlin, Cypher, GQL, SPARQL, then **Convert to <FMT>** or **Convert All
  Formats** → `POST /api/v1/graph/convert {"format_id","limit":10000}`. Click a result card to
  download the output file; a collapsible preview shows the first 5000 chars.
- A processing log pane records each step with timestamps; **Clear all** resets the panel.

### 7.4 Quality & ontology

- **Run validation** → `POST /api/v1/admin/validation {}`. Banner shows valid/finding counts,
  `vertices_checked`, `edges_checked`, finish time. Quality rings: Evidence coverage, Provenance
  coverage, Schema compliance, Completeness, Freshness, Orphan rate, Duplicate rate — per code
  comment (FR-VALID-003), unknown values render **N/A**, never a fake 0%. Findings table: Severity,
  Rule, Affected fact, Detail.
- **Ontology schema**: **Load ontology schema** → `GET /api/v1/graph/schema` → vertex labels with
  instance counts and required/optional properties, edge labels with source/target constraints,
  and index coverage. **Inspect JSON-LD context** → `GET /api/v1/ontology/export?limit=1` and
  prints the `@context`.
- **Federation**: **Load federation plan** → `GET /api/v1/federation/sources` plus
  `POST /api/v1/federation/query {"entity_types":["WorkItem"],"projection":[…]}`; shows source
  table (adapter, mode, entity types), row count, degraded source count, and the raw plan JSON.

### 7.5 Users & policy (Admin Security Center)

`admin/index.jsx` mounts 11 sub-tabs:

- **Live Dashboard** (`AdminDashboard.jsx`): parses `GET /metrics` (Prometheus text) plus
  `/api/v1/admin/stats` and `/api/v1/admin/jobs`; auto-refresh every 5 s (toggleable). Cards: HTTP
  requests, p95/p50 latency from histogram buckets, 4xx/5xx count, worker health; top-routes
  table and job status table. If `/metrics` 404s it degrades to stats/jobs only.
- **Connector Wizard** (`ConnectorSetupWizard.jsx`): 4 steps (type → endpoint → mapping summary →
  done). Honest caveat: its **Test Connection** (`POST /api/v1/connectors/test`) and **Save &
  Activate** (`POST /api/v1/connectors`) calls are wrapped in `.catch(() => ({status:'ok', …}))`
  — **the wizard reports success even when those endpoints fail or don't exist** (neither exists
  in the current API). Do not rely on its confirmation; verify in the source registry instead.
- **Ingestion & Reconciliation** (`IngestionReconciliationPanel.jsx`): `GET
  /api/v1/ingestion/runs` (exists), mode filter chips (ALL/BASELINE/INCREMENTAL/RECONCILIATION),
  **+ Run Incremental** / **+ Trigger Reconciliation** → `POST /api/v1/ingestion/trigger {"mode"}`
  — **[backend missing]** that route is not registered in `apps/api`; expect an error banner.
- **Checkpoints & DLQ** (`CheckpointAndRecoveryPanel.jsx`): `GET /api/v1/ingestion/checkpoints`
  **[backend missing]** and `GET /api/v1/ingestion/dlq` (a DLQ route exists under
  `/api/v1/admin/dlq`; this exact path is not registered). Replay buttons call `POST
  /api/v1/ingestion/dlq/replay` / `replay-all` **[backend missing]**. Prefer the equivalent,
  verified controls in **Audit & recovery** (below).
- **Drift & Freshness** (`SchemaDriftAndFreshnessPanel.jsx`): `GET /api/v1/ontology/drift`
  (exists) with findings table; `GET /api/v1/sources/freshness` **[backend missing]**.
- **Timeline & Journal** (`GraphTimelineAndJournalPanel.jsx`): `GET /api/v1/graph/versions`
  (exists), `GET /api/v1/journal/entries` **[backend missing]** (the API exposes
  `/api/v1/change-journal` instead, main.py:1033), `GET /api/v1/events/consumers`
  **[backend missing]**.
- **Crawl Safety & Telemetry** (`CrawlSafetyAndTelemetryPanel.jsx`): lists `web`/`crawler` sources
  from `GET /api/v1/sources` only; displays the honest notice *"Crawl policy and telemetry
  settings are unavailable here. No policy changes have been applied."*
- **Quality, SLOs & Debt** (`KnowledgeGovernanceAndSLOPanel.jsx`): `GET /api/v1/graph/quality`
  **[backend missing]**, `GET /api/v1/knowledge-debt/summary` (referenced in app.py), `GET
  /api/v1/ontology/proposals` (exists in main.py), `GET /api/v1/simulations` (exists in app.py).
  Sub-tabs: Graph Quality, SLO Management, Knowledge Debt (score/orphans/stale docs/missing
  tests), Evolution Proposals, Simulation Workspaces.
- **Token Governance & CRL** (`SecurityGovernanceDashboard.jsx`): `GET /api/v1/security/status`
  and `GET /api/v1/security/policy-matrix` (both defined in
  `packages/eoip/authz/security_router.py`, mounted by extended.py:1538-1539). Forms: **Issue
  scoped token** (`POST /api/v1/security/tokens/issue {subject, tenant_id, roles, scopes,
  ttl_seconds:3600}` — shows the token once in a read-only password field plus its `jti`),
  **Verify token** (`POST /api/v1/security/tokens/verify {token, required_scopes:["graph:read"]}`),
  **Revoke token** (`POST /api/v1/security/tokens/revoke {identifier, reason}` — requires ticking
  "Confirm revocation"). Role hierarchy table from the policy matrix.
- **Users & Roles** (`UserManagement.jsx`): `GET /api/v1/authz/users`, `GET /api/v1/authz/roles`;
  **Create user** → `POST /api/v1/authz/users {"user_id","roles":[…],"attributes":{…}}`; per-row
  "Assign role…" select re-POSTs the user with updated roles; **Export** downloads
  `/api/v1/authz/users/export`. If these 404, the panel says the authz service is not enabled.
- **Policies & RBAC** (`RbacPolicyEditor.jsx`): `GET /api/v1/authz/policies` rendered to YAML;
  edit, then **Save & reload policies** → `POST /api/v1/authz/policies/reload?replace_existing=true`
  with `Content-Type: application/yaml`; **Discard changes** restores the loaded YAML. Right panel
  shows the last 25 authorization decisions from `GET /api/v1/authz/decisions` (read-only).

### 7.6 Live operations

`LiveOpsPanel` (`App.jsx:588`): loads `GET /api/v1/ops/preflight` (check cards with status pills)
and `GET /metrics` (first 28 non-comment lines). **Refresh** re-pulls both.

### 7.7 Audit & recovery

- **Load audit events** → `GET /api/v1/admin/audit?limit=50` — table of Time, Operation, Actor,
  Outcome, safe summary ("Safe summaries only; secrets and payload content are excluded").
- **Load DLQ** → `GET /api/v1/admin/dlq?limit=25` — rejected records with source, failure, record
  ID, payload hash (payload itself is never shown). **Replay** per row →
  `POST /api/v1/admin/dlq/{event_id}/replay`. Rows without an `event_id` show "Not supported".

---

## 8. Guided demo

**What it does.** Route `/demo` (`GuidedDemo`, `App.jsx:89`) runs the packaged "Northstar
Commerce" end-to-end scenarios against the live graph.

**How to access.** Rail → **Guided demo**. API: `GET /api/v1/demo/scenarios`, then `POST
/api/v1/path` per scenario.

**Step by step.**

1. The catalog loads automatically; **Refresh scenario catalog** re-pulls it.
2. Read the summary line (`{title} · N scenarios · dataset {dataset_id} v{version}`) and pick a
   scenario card — each shows READY/DATA MISSING pill, audience, story, capabilities chips, and an
   expandable "Declared path" list marking each expected entity AVAILABLE or MISSING.
3. Click **Run declared path**. The UI calls:

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"source_id":"<first expected_path entry>","target_id":"<last entry>","max_depth":8}' \
  http://localhost:8000/api/v1/path
```

**Response/result.** Inline outcome: "Path returned" or "No path returned" plus the full JSON
response in a `<pre>` block. Running shows a spinner; errors show "API error" with the message.

**Errors and recovery.** "Scenario catalog unavailable" means `/api/v1/demo/scenarios` failed —
load the demo dataset first (Administration → **Load / replay demo**). A scenario with fewer than
2 expected-path entries cannot run ("does not declare a valid entrypoint-to-target path"). DATA
MISSING pills tell you the graph doesn't contain that scenario's entities yet.

---

## 9. Appearance / settings

**What it does.** Route `/settings` (`features/settings/Appearance.jsx`): four themes — Light,
Dark, High contrast light, High contrast dark (applied via `document.documentElement.dataset.theme`)
— and a **Reduce motion** checkbox (`data-motion="reduce"`).

**How to access.** Rail → **Appearance**.

**Step by step.** Click a theme card or toggle Reduce motion. The note is explicit: *"Applied to
this connection. Appearance resets when you disconnect or reload."* — nothing is persisted.

**Related:** `i18n.js` ships an `I18nManager` with locales `en`, `ar` (RTL), and `qps-ploc`
pseudo-localization, but no workspace UI currently exposes a locale switcher — it is a library,
not a settings feature.

---

## 10. Error handling model

- All workspace actions go through `run()` (`App.jsx:953`): concurrent operations share one busy
  flag; failures pop a toast with the server's `detail` (RFC-7807-style), the `X-Correlation-ID`
  header value when present, and the generic hint "Check that the local API and graph services are
  available." Dismiss with the × button.
- HTTP validation arrays become "Some fields are invalid. Review the submitted values."
  Unreadable JSON becomes "The service returned an unreadable response." Disconnect aborts
  in-flight requests silently (AbortError is swallowed).
- Status pills color-code: positive for ready/running/succeeded/passed/ok/complete, negative for
  failed/error/denied, neutral otherwise — across every table in the app.
