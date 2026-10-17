# ADR-H17 — GPU availability per deployment profile

| Field | Value |
|---|---|
| Decision | H-17 (CRAr_cpccaggcc-requirements.md, section 18.2) |
| Status | **Open** — interim CPU-only policy in force |
| Owner | CTO / Infrastructure |
| Input received | "we are not sure about the GPUs" (Ravaleedhar Reddy, 2026-10-18) |
| Governs | CRA-043.10, CRA-043.11, CRA-044.13, CRA-026.13 |
| Related | ADR-H15 (CPU-first stack, accepted), ADR-H16 (CUDA not redistributed, accepted) |

## Interim policy (in force until this decision is closed)

1. **No deployment profile assumes a GPU.** P0, P1 and P2 qualification runs on CPU-only reference hardware (requirements section 5.2).
2. **Every binding gate is met without a GPU.** GPU results may be recorded but are non-binding.
3. **A capability that needs a GPU to meet its gates is `UNQUALIFIED`** in CPU profiles. A learned architecture in that position is recorded `DEFERRED (H-17)`.
4. **Self-hosted generation and transcription use CPU-capable runtimes.** GPU-oriented servers (vLLM, TGI) stay unqualified.
5. **GPU detection is allowed; GPU dependence is not.** Customer-provisioned CUDA builds (ADR-H16) may accelerate work, but no code path requires them.

## What is needed to close this decision

For each deployment profile (SaaS, customer-installed, air-gapped), choose **none**, **optional** or **required**, informed by:

- Customer hardware survey: which target customers can provide GPUs, which models, and which driver versions.
- Measured CPU results from CRA-043/044 qualification: which gates CPU meets, and which it misses and by how much.
- Workload volumes: training graph size and retraining frequency, ASR hours per month, LLM answer latency targets.
- Cost comparison of CPU scale-out versus GPU nodes for those workloads (runtime cost model, section 16.3).
- For SaaS GPU use: Legal confirmation of the operating position (see ADR-H16, "Not decided here").

## Consequences while open

- CRA-043.10's platform matrix has no required CUDA row.
- Bake-off-gated architectures that miss CPU budgets end as `DEFERRED (H-17)` with their CPU numbers recorded, which is a valid outcome.
- In the tracker, H-17 is `BLOCKED` with the missing input recorded (import fragment `docs/decisions/decisions-ledger-import.json`).
