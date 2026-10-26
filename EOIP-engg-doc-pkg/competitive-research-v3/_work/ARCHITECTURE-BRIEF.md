# Architecture-document brief — read fully before starting

You write `10-TARGET-REFERENCE-ARCHITECTURE.md` and the 12 ADR files in `18-ADRS/` for the KnowGridFlow/EOIP competitive research package. Repository root: `F:\code\EIP\EIOP`. Package: `EOIP-engg-doc-pkg/competitive-research-v3/`.

## Inputs (read in this order)

1. `KNOWLEDGE_GRAPH_COMPETITIVE_RESEARCH_MASTER_PROMPT_v3.md` lines 387–411 (§11, the 18 architecture hypotheses — candidates, not approved features) and lines 140–170 (§4.3 non-negotiable constraints, §4.4 reference journeys) and lines 450–470 (§14 journeys J1–J16).
2. `01-SYSTEM-BASELINE.md` §3–§5 (verified architecture diagram and BL-IDs) and `01a-BASELINE-DELTA-HEAD.md` (status at HEAD — authoritative where it differs).
3. `06-MASTER-CAPABILITY-MATRIX.md` (decisions and priorities per capability — your architecture must be consistent with every BUILD/REUSE/INTEGRATE/EXPERIMENT/DEFER/REJECT decision there; do not re-decide them).
4. `07-GAP-REGISTER.md` (46 gaps, priorities, root causes) — the architecture exists to close these, especially the 11 forced P0s.
5. `08-STRENGTH-ADOPTION-REGISTER.md` §1 (coordinator shortlist) and `09-CON-TO-PRO-INVERSION-REGISTER.md` §3 (11 self-inversion cards — these ARE your P0 architecture decisions, already designed; your job is to compose them into one coherent system, not redesign them).
6. Skim `05-COMPARISON-COHORTS/*.md` for the planes relevant to each hypothesis (cite cohort findings, don't re-derive them).
7. Existing ADR numbering to avoid collision: `EOIP-engg-doc-pkg/64-decisions-and-adrs.md` (ADR-001..010) and `docs/decisions/ADR-H15/H16/H17`. This package uses **ADR-KG3-01..12**.

Also note: a prior, non-evidence-based pass on 2026-10-19 wrote placeholder files at `10-TARGET-REFERENCE-ARCHITECTURE.md` and `18-ADRS/ADR-KG3-01..12-*.md` with no CLAIM records and some unverified claims (e.g. ADR-KG3-10 proposed deprecating Cytoscape for Sigma citing an unsupported "60 FPS on 100,000+ nodes" figure — the real V30 research found no independent benchmark for either and recommends measuring first). **Overwrite every one of these completely** with your own evidence-based version (Read each file first, then Write). Do not reuse their content or structure.

## What to write

### `10-TARGET-REFERENCE-ARCHITECTURE.md` (6,000–9,000 words)

Structure, addressing every one of the 18 Master Prompt §11 hypotheses explicitly (state BUILD/REUSE/INTEGRATE/EXPERIMENT/DEFER/REJECT for each, citing the matrix/gap/register IDs that justify it — never invent a new decision):

1. **Principles** — derived from Master Prompt §4.3 constraints and the P0 gaps: backend neutrality, ACL/tenant correctness as a storage-level guarantee (not an app convention), epistemic separation as a storage-level guarantee, CPU-first, air-gap capable, licence-clean by construction.
2. **Layered reference architecture** — a text diagram (fenced code block) of: source adapters → canonical ingest pipeline (per BL-23/24/27/28, with the GAP-02/03/07 fixes as mandatory stages, not optional ones) → mutation gateway (typed constraints, GAP-12) → multi-backend GraphStore protocol + typed query-IR compiler (GAP-04/05) → epistemic planes (GAP-07) → retrieval stack (VectorPort, hybrid fusion, GraphRAG as EXPERIMENT per GAP-33) → agent/MCP surface (GAP-09) → UI. Every box traces to a CAP-ID.
3. **Data, control, evidence, security and tenancy planes** — one subsection each, each stating what changes versus the HEAD baseline and which gap it closes.
4. **The multi-backend layer** — HugeGraph/Neo4j/Neptune/JanusGraph adapters, the conformance suite (BM-01), and the specific adapter defects found in research (JanusGraph key-prefix mismatch, Neptune no-SigV4, HugeGraph forced Groovy closures) as near-term fixes versus the long-term typed-IR fix.
5. **Interfaces** — QueryPlan→AST→{gremlin-lang, openCypher, SPARQL}; VectorPort; AuthzPort/SecretsPort; ModelPort (Ollama/llama.cpp); ER port (own engine + Splink integration); AlgoPort (rustworkx/GraphBLAS over tenant-filtered snapshots).
6. **Deployment tiers** — one-node air-gapped (HugeGraph or Neo4j CE; Neptune excluded), one-node cloud-connected, distributed (deferred, demand-gated per GAP-30's sibling).
7. **Mapping of the 18 hypotheses** — a table: Hypothesis # | one-line description | decision | justifying GAP/CAP/STR/INV IDs | which section above implements it.
8. **What this architecture does NOT do** (explicit non-goals, per the Master Prompt's "reject features whose complexity outweighs value").

### `18-ADRS/ADR-KG3-01.md` … `ADR-KG3-12.md`

One ADR per major decision (context, options considered, options rejected and why, decision, consequences, reversibility — Master Prompt §13). Base these directly on the 11 self-inversion cards in `09-CON-TO-PRO-INVERSION-REGISTER.md` §3 (one ADR per self-inversion, using its already-worked-out options and selected option) plus one ADR for the multi-backend typed query-IR (GAP-04/05, the architecture's central structural decision). Suggested numbering:
- ADR-KG3-01 Source-ACL enforcement as a mandatory pipeline stage (GAP-02)
- ADR-KG3-02 Tenant isolation as a protocol-level guarantee (GAP-03)
- ADR-KG3-03 Egress vault: authenticated encryption, not XOR (GAP-08)
- ADR-KG3-04 MCP authorization: per-user OAuth 2.1 resource server (GAP-09)
- ADR-KG3-05 Backend conformance suite and named adapter-defect fixes (GAP-01)
- ADR-KG3-06 Epistemic planes as a storage-level guarantee (GAP-07)
- ADR-KG3-07 Unified evaluation harness as release-gating infrastructure (GAP-43)
- ADR-KG3-08 Parameterised query IR; retire string-built Gremlin (GAP-05, ties to GAP-04)
- ADR-KG3-09 Agent memory as a governed epistemic type (GAP-34)
- ADR-KG3-10 Local model runtime hardening (GAP-36)
- ADR-KG3-11 Licence allow-list as a CI gate (GAP-19)
- ADR-KG3-12 Typed multi-backend query-IR compiler (GAP-04) — the structural decision the others depend on

Each ADR: 400–800 words. Cite GAP/CAP/STR/INV IDs; do not re-derive evidence already in the registers — reference it.

## Rules

- Every claim about a competitor traces to a CLAIM-ID via the deep dives (through the gap/strength/inversion registers — do not re-read 60 deep dives, the registers already distill them).
- Every EOIP status claim traces to a BL-ID or NB-ID in `01-SYSTEM-BASELINE.md` / `01a-BASELINE-DELTA-HEAD.md`.
- Do not introduce any decision not already in `06-MASTER-CAPABILITY-MATRIX.md` or the self-inversion cards; your job is composition and sequencing, not re-deciding.
- Respect Master Prompt §4.3: no mandatory cloud, no hidden egress, no backend lock-in, connectors never mutate the graph directly, permissions survive everything, one-node first.
- Never delete, move or rename files; never run git commands that change state. Write only `10-TARGET-REFERENCE-ARCHITECTURE.md` and the 12 files in `18-ADRS/`.

## Final reply (≤200 words)

Files written, the 18-hypothesis decision table in full, and any gap/matrix inconsistency you found while composing them.
