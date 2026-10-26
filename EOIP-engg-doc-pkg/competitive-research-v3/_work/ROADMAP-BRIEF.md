# Roadmap, traceability and progress-tracker brief — read fully before starting

You write `14-IMPLEMENTATION-ROADMAP.md`, `19-TRACEABILITY-MATRIX.md` and `23-PROGRESS-TRACKER.html` for the KnowGridFlow/EOIP competitive research package. Repository root: `F:\code\EIP\EIOP`. Package: `EOIP-engg-doc-pkg/competitive-research-v3/`.

## Inputs

1. `11-REQUIREMENTS-FINAL.md` — 57 requirements (P0 14, P1 25, P2 12, P3 6), already fully specced with dependencies, effort and tests. This is your primary roadmap input.
2. `07-GAP-REGISTER.md` — root causes, dependencies, options, effort per gap (each requirement traces back to one or more gaps here).
3. `10-TARGET-REFERENCE-ARCHITECTURE.md` §7 and §4 (read the full architecture doc's dependency notes) — it explicitly surfaced two sequencing chains not captured in the gap register's own tables: **GAP-04 (portable query IR) is structurally prior to GAP-01 (adapter defects) and GAP-05 (injection defences)**, and **GAP-03 (tenant isolation) is structurally prior to GAP-02 (source-ACL enforcement) and GAP-07 (epistemic planes)**. Your roadmap sequencing must respect these two chains even though the raw priority scores might suggest a different order.
4. `18-ADRS/*.md` (12 ADRs) for the selected design per P0 item.
5. `15-VALIDATION-BENCHMARK-PLAN.md` (BM-01..BM-22) for the go/no-go gate each work package must pass.
6. `02-TECHNOLOGY-REGISTRY.md` / `.json` for REUSE/INTEGRATE dependencies (e.g. installing pySHACL, Splink, LanceDB) and their licence classes (cite legal-review triggers where a work package depends on one).
7. `00-specification-audit-and-enhancements.md` or `01-SYSTEM-BASELINE.md` is NOT the roadmap source — do not duplicate existing EOIP backlog files (`KGF-MASTER-BACKLOG.md` etc.); this is a new, research-derived roadmap for the gaps/requirements in THIS package only.

Note: a prior, non-evidence-based pass on 2026-10-19 wrote placeholder files at all three paths with no REQ/GAP traceability. **Overwrite each completely** (Read then Write); do not reuse their content or structure.

## What to write

### `14-IMPLEMENTATION-ROADMAP.md` (3,500–5,500 words)

1. Sequencing principles: P0→P3 is the default order, but the two structural dependency chains above override raw priority within a tier (state this explicitly).
2. **Slices** (dependency-aware work packages, `WP-KG3-NN`), grouped into 4–6 phases. Each WP: title, REQ-IDs covered, dependencies (other WP-IDs), effort (inherit from REQ effort fields, sum/round), go/no-go gate (BM-ID + pass threshold from §15), owning architecture layer (from §10).
   - Phase 0 (foundation/correctness): every P0 requirement, sequenced per the two dependency chains (query-IR work package before adapter-defect and injection work packages; tenant-isolation work package before ACL-enforcement and epistemic-plane work packages).
   - Phase 1: P1 requirements.
   - Phase 2: P2 requirements.
   - Research track: P3 requirements (not phase-gated, demand/evidence-gated instead, per Master Prompt §13 "distinguish product priority from research priority").
3. Migration strategy: for any WP that changes a live contract or schema (e.g. ACL-principal fields on existing fact/edge types), state backward-compatibility approach, rollback condition, and reference the relevant ADR's "reversibility" field.
4. A phase-level Gantt-style dependency diagram in a fenced text/mermaid block (WP-IDs as nodes, dependency arrows).
5. Explicit non-sequencing: name any requirement intentionally left unscheduled (e.g. demand-gated P2/P3 items) and why.

### `19-TRACEABILITY-MATRIX.md` (one row per requirement; target the full 57 + key gaps/journeys)

Master Prompt §16 item 20 format exactly: `Source → Claim → Competitor capability → Gap/Strength/Inversion → REQ-ID → Design → Task → Test → Metric`. Columns:
`Source (deep dive/baseline) | Claim/evidence (CLAIM-ID or BL/NB-ID) | Competitor capability (CAP-ID) | Gap/Strength/Inversion (GAP/STR/INV-ID) | REQ-ID | Design (ADR-ID or architecture §) | Task (WP-ID from the roadmap) | Test (BM-ID) | Metric/threshold`.
Populate one row per requirement (57 rows minimum); add extra rows for any strength/inversion adopted without a dedicated requirement (cite its STR/INV-ID, leave REQ-ID as "—" with a one-line reason). Never duplicate a requirement across rows — if a requirement serves multiple gaps, list all GAP-IDs in one cell, comma-separated.

### `23-PROGRESS-TRACKER.html`

A single self-contained HTML file (inline CSS/JS, no external network calls — this must work fully offline, consistent with the air-gap constraint) that:
- Loads its data from three JSON arrays you embed inline as `<script>const DATA = {...}</script>` (do NOT fetch external files): registry entries (summarise from `02-technology-registry.json` — id, name, tier, category, status, research_state), gaps (from `07-GAP-REGISTER.md` — id, title, priority, class, severity), requirements (from `11-REQUIREMENTS-FINAL.md` — id, title, priority, phase/WP, status="PROPOSED" for all — nothing is implemented yet, this tracker starts at zero).
- Renders three tables (Registry / Gaps / Requirements) with client-side filter inputs (text search + priority/tier/category dropdowns, pure vanilla JS, no framework, no CDN).
- Shows summary tiles at the top: total registry entries, P0/P1/P2/P3 gap counts, total requirements by phase.
- Keep it under ~500KB. Load this skill before writing it if you have access to an "artifact-design" skill; if not, just make it clean, readable, phone-width-safe (no horizontal scroll), and self-contained — this is a static file saved to disk, not an Artifact publish.

## Rules

- Inherit priorities/IDs exactly from `07-GAP-REGISTER.md` and `11-REQUIREMENTS-FINAL.md`; never renumber or re-decide.
- Every WP-ID must map to at least one REQ-ID; every REQ-ID must appear in at least one WP-ID (confirm this in your final reply).
- Nothing in this package is implemented — the tracker's requirement rows all start as "PROPOSED/NOT STARTED"; never show a fabricated "done" status.
- Never delete, move or rename files; never run git commands that change state. Write only the three named deliverables.

## Final reply (≤200 words)

Files written, WP count and phase breakdown, confirmation every REQ-ID appears in the traceability matrix and in a WP, and any gap you found between the architecture doc's dependency notes and the gap register's own stated dependencies.
