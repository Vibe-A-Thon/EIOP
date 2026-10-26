# Cohort-comparison brief (Master Prompt §10.1) — read fully before starting

You write workload-aligned comparison files for the KnowGridFlow/EOIP competitive research package. Repository root: `F:\code\EIP\EIOP`. Package: `EOIP-engg-doc-pkg/competitive-research-v3/`.

## Inputs (read selectively — the deep dives are large)

1. `KNOWLEDGE_GRAPH_COMPETITIVE_RESEARCH_MASTER_PROMPT_v3.md` lines 332–347 (§10.1–10.2) and 412–426 (§12 benchmark rules), plus lines 140–155 (§4.3 constraints).
2. `03-RESEARCH-METHODOLOGY.md` §6 (shared capability taxonomy CAP-01..CAP-80).
3. `01-SYSTEM-BASELINE.md` (BL-IDs at commit ad9937b) **and** `01a-BASELINE-DELTA-HEAD.md` (status at HEAD 896e06d, which supersedes the original where they differ; NB-IDs for new capabilities). Use HEAD status for EOIP columns and cite both IDs.
4. The deep dives in `04-COMPETITOR-DEEP-DIVES/` for your cohort. **Only files containing `CLAIM-` records are research.** Ignore placeholder files with no `CLAIM-` records (e.g. `C09-langgraph-agent-protocols.md`, `C10-qdrant-vector-engines.md`, `C11-pyg-graph-ml.md`, `C13-terminusdb-bitemporal.md`, `C15-glean-code-intelligence.md`, `C16-sigma-graphology-visualization.md`, and the un-suffixed `*-tier-c-records.md` files). To save context, do not read whole deep dives: extract headings 1, 3, 7, 8, 9, 10, 11, 13 and appendix B with grep/sed (e.g. `sed -n '/^## 8\./,/^## 10\./p' file`), and look up specific CLAIM rows only when you cite them.
5. `C:\Users\SINDHU~1\AppData\Local\Temp\claude\f--code-EIP-EIOP\bec7c502-5a2d-4f41-8a50-dae2108e0918\scratchpad\kgr3\extract.json` — machine extraction of every deep dive's CAP mapping rows and STR/INV card lines (may be slightly stale; deep dives are authoritative).

## Output format — one file per cohort in `05-COMPARISON-COHORTS/`

Front matter table (Cohort ID, workload class, members with their deep-dive links, reference columns, date). Then:

1. **Workload class and comparison basis** — which customer workloads this cohort serves; why these members are comparable; who is excluded and why.
2. **Capability comparison table** — rows = the relevant CAP-IDs (named), columns = each member + reference columns **HugeGraph, Neo4j, Neptune** (where applicable) + **EOIP @HEAD**. Cell values: native / partial / plugin / enterprise-only / absent / unknown, each with a CLAIM-ID (competitors) or BL/NB-ID (EOIP). Never fill a cell without evidence; write `unknown`.
3. **Operational and licensing comparison** — deployment, one-node footprint, air-gap viability, licence class, redistribution/OEM trigger, maintenance status.
4. **Performance evidence** — only reproducible or clearly attributed figures, with workload and hardware; vendor claims labelled as such; state where no comparable evidence exists. No winners declared from incomparable tests.
5. **Findings** — 5–10 numbered, falsifiable conclusions about the cohort, each with evidence references.
6. **Implications for EOIP** — for each relevant CAP: parity needed (STR-IDs to adopt), exploitable weaknesses (INV-IDs), recommended per-capability decision (BUILD/REUSE/INTEGRATE/EXPERIMENT/DEFER/REJECT) and candidate gap statement. Respect backend neutrality: mark "available upstream / not integrated" rather than "missing" when a supported backend already provides it.
7. **Open questions** for this cohort.

Length: 2,000–3,500 words per cohort file; tables over prose. Use the Write tool. Cite as `[CLAIM-xxx-NN](../04-COMPETITOR-DEEP-DIVES/<file>.md)` or plainly `CLAIM-xxx-NN (C01-neo4j.md)`.

## Rules

- Never fabricate. Every competitive assertion traces to a CLAIM-ID in a deep dive; EOIP status traces to BL/NB rows. If the deep dives disagree, say so.
- Some cohort files already exist from 2026-10-19 (another tool; they contain no CLAIM evidence). Overwrite the file of the same name completely (Read it, then Write); do not reuse its content. Never delete, move or rename files; never run git commands that change state.
- Do not modify anything outside `05-COMPARISON-COHORTS/`.

## Final reply (≤200 words)

Files written, member counts, the three most important cross-cohort findings, and any evidence conflicts you found between deep dives.
