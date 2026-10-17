# ADR-H15 — Adopt a tiered, CPU-first numerical stack as optional extras

| Field | Value |
|---|---|
| Decision | H-15 (CRAr_cpccaggcc-requirements.md, section 18.2) |
| Status | **Accepted — 2026-10-18** |
| Decided by | Claude (engineering agent), under explicit delegation from Ravaleedhar Reddy: "for H-15 you be the best judge and decide the answer" (2026-10-18) |
| Governs | CRA-043 (all clauses), CRA-014.9, CRA-023.9, CRA-025.8, CRA-026.13, CRA-035.9, CRA-044 |
| Depends on | ADR-H16 (CUDA not redistributed, decided), ADR-H17 (GPU availability, open) |
| Review trigger | ADR-H17 decided; or any binding gate proven unattainable on CPU reference hardware |

## Context

- The repository has no numerical stack: numpy, scipy, scikit-learn, torch, torch-geometric and networkx are absent from `pyproject.toml` and the environment (G20, measured 2026-10-18 at `d771fd6`).
- CRA-014 (OCR/ASR), CRA-023.6/023.7 (embedding and structural similarity, alignment), CRA-025 (dense retrieval), CRA-026 (local models) and CRA-044 (learned graph models) all presuppose one.
- The core install is nine pure-Python packages, and the project already uses optional extras (`fileparse`, `codeparse`, `otel`, `k8s`, `redis`, `enterprise`).
- CUDA packages cannot be redistributed (ADR-H16). GPU availability per deployment profile is unknown (ADR-H17).

## Decision

1. **Adopt the four tiers as optional extras; the core install does not change.**
   - **N0 `numerics`** (numpy, scipy, scikit-learn): adopted. Required in every deployment profile that enables any probabilistic capability.
   - **N1 `neural`** (N0 + torch, torch-geometric): adopted, **CPU-only builds**.
   - **N2 `neural-text`** (N1 + transformers, sentence-transformers): adopted, CPU-only builds. Model weights ship only where their own license permits redistribution; otherwise they are customer-provided.
   - **N3 `neural-research`** (N1 + snntorch): development and research environments only. Never included in customer profiles, bundles or images.
2. **CPU-only is the only build EOIP distributes** — in wheels, lock files, offline bundles and container images (consequence of ADR-H16).
3. **CPU-first qualification.** Every binding gate (requirements sections 5.2 and 5.3, CRA-043, CRA-044, CRA-026) is qualified on CPU-only reference hardware. GPU is an optional accelerator: results obtained with one are reported separately and are non-binding until ADR-H17 is decided. A capability that meets its gates only with a GPU is `UNQUALIFIED` in CPU profiles; a learned architecture in that position is recorded `DEFERRED (H-17)`, not promoted.
4. **CPU-feasible defaults.** Model defaults (for example R-GCN at 2 layers, 128 hidden units, 30 bases, with neighbour sampling where full-batch training misses its budget) and self-hosted inference runtimes are chosen for CPU feasibility; GPU-only serving stacks stay unqualified.
5. Exact versions are pinned in a hash-locked file and re-evaluated at each EOIP minor release.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| numpy (or torch) as a core dependency | Changes the install for every deployment including edge and air-gapped ones; contradicts the existing extras convention |
| One monolithic `neural` extra | Forces the torch install on users who only need N0 (metrics, baselines, feature store, anti-stub harness) |
| Defer the decision | Leaves CRA-014/023/025/026/043/044 blocked with no substrate |
| GPU-first design | Not distributable (ADR-H16) and hardware availability unknown (ADR-H17) |

## Consequences

- CRA-043 clauses are unblocked. CRA-043.11, CRA-044.13 and CRA-026.13 are added to bind the CPU-first policy.
- Performance and training budgets must be demonstrated on CPU. Some bake-off architectures (large graph transformers, GraphGPS at scale) may legitimately end as `DEFERRED (H-17)`.
- Install-size targets are budgets to be measured, not assumed: N0 <= 150 MB and N1 (CPU) <= 2.5 GB installed (CRA-043.1). Earlier "~70 MB" and "~2 GB" figures were unmeasured; ~2 GB describes CUDA builds.
- The ledger decision entry for H-15 references this file. Its import fragment is `docs/decisions/decisions-ledger-import.json`.
