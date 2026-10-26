| Field | Value |
|---|---|
| Registry ID | T-C09-dspy |
| Tier | B (programmatic prompt optimisation; candidate for NL-to-query and extraction quality work) |
| Versions examined | dspy 3.4.1 (2026-10-12, PyPI and GitHub release) |
| Verified on | 2026-10-26 |
| Worker | V22 |

## 1. Identity, current status, tier, sources

DSPy ("Declarative Self-improving Python"), repo `stanfordnlp/dspy`, originated at Stanford NLP; a framework for "programming, rather than prompting" LMs, with algorithms that optimise prompts and weights [CLAIM-dspy-01]. Licence **MIT** (copyright "2023 Stanford Future Data Systems" in the PyPI licence text) [CLAIM-dspy-02]. Version 3.4.1 released 2026-10-12 [CLAIM-dspy-02]. Status: active, production-used widely (adoption breadth UNVERIFIED), semver 3.x. The README names research on instruction/demonstration optimisation, GEPA reflective prompt evolution (Jul 2025), fine-tuning plus prompt optimisation, and DSPy Assertions [CLAIM-dspy-01]. Governance structure not stated in README: UNVERIFIED.

## 2. Problem, workloads, workflows

Problem: hand-written prompts are brittle across models and tasks. DSPy expresses a task as a signature (typed inputs/outputs) inside modules, then compiles it against a metric and a small dev set. EOIP workflow: define `NLToQueryPlan(question, schema_summary) -> QueryPlan` with the metric "plan validates under `query/policy.py` and returns the labelled gold entity set", optimise against a local small model (Ollama or llama.cpp endpoint), freeze the compiled program as a versioned artefact and ship it behind `LLMAssistHook` (BL-12).

## 3. Feature inventory

| Feature | Status | Note |
|---|---|---|
| Signatures and modules (predict, chain-of-thought, ReAct-style agents) | present | module names not re-verified: UNVERIFIED |
| Optimisers (prompt/demo search, GEPA, fine-tune-assisted) | present | research listed in README [CLAIM-dspy-01]; exact optimiser inventory in 3.4.1 UNVERIFIED |
| Provider abstraction incl. local OpenAI-compatible endpoints | likely present | via LiteLLM-style routing: UNVERIFIED |
| Retrieval integration | present (historical) | "Demonstrate-Search-Predict" lineage [CLAIM-dspy-01] |
| Assertions / constraints | present (2023 paper); current API status UNVERIFIED | |
| Evaluation helpers | present | not examined |
| Tenancy, ACL, egress control | absent | |
| CLI / UI | absent | library only |

## 4. Architecture

```
 program (modules + signatures) --compile(optimizer, metric, trainset)--> optimised program
   (instructions, few-shot demos, optionally weights) --serialize--> JSON artefact
 runtime: module.forward -> adapter (format prompt, parse typed output) -> LM client -> model endpoint
```

## 5. Under-the-hood reconstruction

Hypothesis from papers, not source-read: an optimiser proposes candidate instructions/demos using a teacher or reflective LM, evaluates each candidate program on the dev set with the user metric, and keeps a Pareto or best set; compile cost is therefore (candidates x examples x calls). Compiled state is data (instructions, demos), so it can be diffed, reviewed and versioned like ontology-as-code (`ontology/gitops.py` pattern). No storage engine, no reasoning.

## 6. Requirements inferred

FR: a labelled evaluation set per task; metric functions executable offline; compile jobs run against local models only. NFR: compile runs must route through the egress gateway when any non-local teacher is used (BL-45); compiled artefacts carry model id, dataset hash, metric, date; reproducible within sampling noise.

## 7. Performance and resource model

Compile-time cost scales with model calls; no public numbers gathered this run. Failure modes: overfitting to a small dev set, optimiser gains that do not transfer across model swaps, metric gaming. Published claims in the cited papers are not reproduced here.

## 8. Strengths

Treats prompts as optimisable, testable artefacts; fits EOIP's evaluation-harness culture (CAP-78) and small-local-model constraint where manual prompting is weakest. Match: build an optional `eoip-ai` compile step and freeze outputs. Exceed: gate promotion of a compiled program on a regression suite plus lineage record (BL-41).

## 9. Limitations

Algorithmic: gains depend on metric quality and data volume. Operational: compile needs many LM calls, slow on CPU-only reference hardware (ADR-H15 CPU-first) unless a customer provides a GPU endpoint (inference). Friction: prompts become opaque generated text; debugging needs tracing. Version churn across 2.x to 3.x APIs reported by users generally (not verified).

## 10. Deployment, licensing, viability

MIT, pure Python; fits `neural-text`-style optional extra. Air-gap viable with a local endpoint. Redistribution safe. No legal trigger found. Dependency tree size not measured.

## 11. Competitive delta vs EOIP baseline

BL-12 NL-to-query is a Partial optional hook over deterministic suggestion (BL-11); no prompt evaluation or optimisation exists. DSPy supplies a method, not a capability EOIP lacks end-to-end.

## 12. Cards

STR-dspy-01 | DSPy | metric-driven prompt compilation with versionable artefacts | CLAIM-dspy-01 | higher NL-to-query accuracy on small local models; reproducible | integrate | optional compile pipeline, artefacts under review in git | on a 200-question EOIP gold set, compiled program beats the hand prompt by a pre-registered margin and 0 policy-violating plans.
INV-dspy-01 | DSPy 3.4.1 | compile cost and metric dependence (hypothesis) | root cause algorithm, hypothesis | deterministic template tier (BL-11) remains primary; DSPy only when LLM path is on; worse when the dev set is under ~50 labelled items | options: (1) hand prompts + eval harness; (2) DSPy offline compile; (3) continuous per-tenant optimisation | select 1 then 2 | POC: compile time and gain on CPU endpoint vs manual | defensibility: tenant-specific gold sets | decision EXPERIMENT.

## 13. Per-capability decisions

| Capability | Decision |
|---|---|
| CAP-58 NL-to-query prompt quality | EXPERIMENT (DSPy offline) |
| CAP-78 evaluation harness | BUILD in-house; DSPy metrics may be reused |
| DSPy as runtime dependency of core | REJECT; optional extra only |

## 14. Tests

Gold set of NL questions to `QueryPlan` per backend; metric = validity under policy + result-set F1; ablation baseline; compile reproducibility over 3 seeds; confirm no network call from compile when egress is S0.

## 15. Risks and open questions

Optimiser inventory in 3.4.1; telemetry/default network behaviour of the library (UNVERIFIED, check for outbound calls); licence of bundled caches.

## Appendix A. Research-dimension coverage

| Dimension | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | MIT, active |
| D2 | 2 | Prompt compilation |
| D3 | 4 | Compile/runtime split |
| D4-D7 | N/A | No storage, schema, query or reasoning |
| D8 | N/A | Library |
| D9-D12 | N/A | none |
| D13 | 2, 8 | LLM program layer |
| D14 | 2, 8, 12 | NL-to-query optimisation |
| D15 | 5 | Artefact versioning |
| D16 | N/A | none |
| D17 | 3 | Python API |
| D18 | 6, 15 | Egress of teacher calls |
| D19 | N/A | none |
| D20 | 7 | No numbers |
| D21 | 10 | MIT |
| D22 | 9 | Opaque prompts |
| D23 | N/A | academic prior art only |
| D24 | App. C | README + PyPI only |

## Appendix B. Capability mapping

| CAP-ID | This technology | CLAIM | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-58 | native (method) | dspy-01 | BL-12 Partial | EXPERIMENT | P2 |
| CAP-78 | partial | dspy-01 | none verified | BUILD | P2 |
| CAP-32 | partial | dspy-01 | BL-26 | DEFER | P3 |

## Appendix C. Evidence records

| CLAIM-ID | product/version/date | claim | class | source | dates | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-dspy-01 | DSPy README | declarative framework; optimises prompts and weights; lists GEPA and related papers | Officially documented | https://github.com/stanfordnlp/dspy | undated / 2026-10-26 | 0.8 | licence not in README |
| CLAIM-dspy-02 | dspy 3.4.1 | MIT; 2026-10-12 | Officially documented | https://pypi.org/project/dspy/ ; https://github.com/stanfordnlp/dspy/releases/latest | 2026-10-12 / 2026-10-26 | 0.9 | none |

## Appendix D. Assumptions

Optimiser names beyond README-listed research are not asserted. Performance gains from papers are not restated.
