# Graph Neurons — Implementation Plan & Completion Protocol

> **Document ID**: GN-PLAN-v1
> **Date**: 2026-10-16
> **Pairs with**: `Graph-Neurons-requirements.md` (GN-REQ-v1) — read that first
> **Audience**: the AI coding agent executing this work, and the human who signs it off
> **Purpose**: how the work is sequenced, how it is proven done, and what disqualifies a completion claim
> **Revision**: GN-PLAN-v1.1 (2026-10-17) — GN-706 placed in Phase 2 and GN-705 marked cross-phase; test-suite count made a measured value; tracker IDs on every gate and sign-off line; §8 tracker procedure added. No gate or threshold changed.

---

## 0. The Completion Protocol

### 0.1 Why this document exists

The requirements say *what* to build. This document says *how you prove you built it*. The
separation matters because the failure this programme guards against is not bad code — it is
**plausible code that was never shown to work**. `packages/eoip/gnn/engine.py` is 300 lines of
well-structured, readable, type-annotated Python that computes SHA-256 hashes and calls them
embeddings. It would survive most code reviews.

So: **completion is a measurement, not a deliverable.**

### 0.2 What does NOT count as completion

The following claims are rejected outright. An agent making one of these has not reported progress:

| Rejected claim | Why |
|---|---|
| "Implemented `rgcn.py`" | A file is not a feature |
| "Added tests in `test_rgcn.py`" | A test file is not a passing test |
| "All tests pass" | Without the test *output* and *what the tests assert*, this is unverifiable |
| "The model achieves 0.94 AUROC" | AUROC alone is forbidden; AUPRC is primary and baselines must appear beside it |
| "Training completed successfully" | Completing is not learning — show the loss curve and the anti-stub report |
| "Integrated with the platform router" | Show the OpenAPI entry and a real request/response |
| "Follows the existing engine pattern" | Pattern conformance is not function |
| "Should work" / "is expected to" | Run it |

### 0.3 The Evidence Ledger — the only accepted completion format

Every requirement produces exactly one ledger entry at
`EOIP-engg-doc-pkg/evidence/GN-<id>.md`. No requirement is complete without its entry.

````markdown
# Evidence Ledger — GN-101 (R-GCN)

**Status**: COMPLETE | FAILED | BLOCKED
**Agent**: <model/session id>        **Date**: 2026-MM-DD
**Commit**: <git SHA at verification time>

## V2 — Executable
Command:  python -m eoip.neural.cli train --model rgcn --snapshot ref-2026-10
Exit code: 0
Duration: 412s
```
<paste the last 30 lines of real stdout — not a summary of it>
```

## V3 — Behavioural
Fixture: tests/neural/fixtures/known_graph.json (5 edges removed)
Assertion: all 5 recovered in top-10
Result: 5/5 recovered — ranks [1, 2, 4, 7, 9]
Command: pytest tests/neural/test_rgcn.py::test_recovers_known_edges -v
```
<paste real pytest output>
```

## V4 — Statistical (ALL baselines mandatory)
| Model / baseline        | AUPRC  | Hits@10 | MRR   |
|-------------------------|--------|---------|-------|
| **RGCN (this work)**    | 0.412  | 0.58    | 0.31  |
| CommonNeighborsBaseline | 0.301  | 0.44    | 0.22  |
| RuleBaseline            | 0.288  | 0.41    | 0.20  |
| DegreeBaseline          | 0.195  | 0.33    | 0.15  |
| HashBaseline (replaced) | 0.021  | 0.03    | 0.01  |
| RandomBaseline          | 0.018  | 0.02    | 0.01  |

Gate: AUPRC >= CommonNeighbors + 0.05  ->  0.412 >= 0.351  PASS
Gate: AUPRC >= RuleBaseline + 0.05     ->  0.412 >= 0.338  PASS

## V5 — Anti-Stub (all four required)
| Probe | Result | Measurement |
|-------|--------|-------------|
| P1 Loss descent         | PASS | 2.41 -> 0.63 (26% of initial) |
| P2 Weight delta         | PASS | 18/18 tensors changed, mean L2 0.84 |
| P3 Permutation control  | PASS | true 0.412 vs permuted 0.027, gap 0.385 |
| P4 Structural coherence | PASS | cosine 0.94 between role-identical nodes |

## V6 — Integration
- [x] `/neural/predict/links` in /openapi.json — schema resolves
- [x] `neural.rgcn` present in GET /brain/telemetry
- [x] End-to-end request/response pasted below
- [x] `get_gnn_engine()` still works — no caller breakage
```
<paste real curl request and JSON response>
```

## V7 — Operational
| Metric | Budget | Measured | Verdict |
|--------|--------|----------|---------|
| Inference p95 (top-10, 100k nodes) | 200 ms | 143 ms | PASS |
| Peak RSS during training | — | 3.1 GB | recorded |
| Behaviour without `neural` extra | 503 | 503 + remediation string | PASS |

## Deletions performed
- [x] `GraphEmbedder._deterministic_vector` removed
- [x] `GraphEmbedder.embed_node2vec` removed
- [x] `GraphEmbedder.embed_transe` removed
- [x] Hash functions preserved only in tests/neural/baselines.py as HashBaseline

## Deviations / open questions
<none, or an explicit list>
````

### 0.4 Reporting a failure is a success

If a model does not beat its baselines, the correct action is **not** to tune until it does, nor to
quietly drop the requirement. It is to file the ledger with `Status: FAILED`, the real numbers, and
a one-paragraph recommendation.

`GN-104` (HGT) failing to beat `GN-101` (R-GCN) is a genuinely useful finding: it tells you EOIP's
graphs are not heterogeneous enough to justify the complexity, and saves a quarter of maintenance.
**File it and move on.** The only unacceptable outcome is an unmeasured model in production.

### 0.5 Blocking questions

When a requirement is ambiguous or the repository contradicts it, append to
`EOIP-engg-doc-pkg/graph-neurons-open-questions.md`:

```markdown
## Q-007 — GN-302 TGN memory persistence
**Requirement**: GN-302 says memory must be "reproducible by replaying events".
**Conflict**: MemoryGraphStore does not expose an ordered event log; `graph/bitemporal.py`
has valid_from/valid_to but no monotonic sequence number.
**Options**: (a) add a sequence column, (b) order by (valid_from, canonical_id) and accept
ties, (c) defer GN-302.
**Recommendation**: (a) — ties under (b) make replay non-deterministic.
**Blocked since**: 2026-MM-DD
```

Then **continue with unblocked work**. Do not stall the programme on one question, and do not guess.

---

## 1. Phases & Gates

Phases are strictly sequential at the gate level. Work *within* a phase may parallelise.

```
Phase 0a Numerical substrate GN-010..016   ──┐ HARD GATE — tier N0 only, no torch needed
Phase 0b Contracts & harness GN-001..007     │ HARD GATE — nothing proceeds until both green
Phase 1  Core GNN            GN-101,102      │ ← first tier-N1 (torch) work
Phase 2  Integration & XAI   GN-203,701-704,706 │ ← first user-visible value lands here
Phase 3  Temporal            GN-301,302      │
Phase 4  Advanced encoders   GN-103,104,201  │ ← each is bake-off gated; may legitimately not ship
Phase 5  Convolutional       GN-401,402,403  │
Phase 6  Quality gate (GAN)  GN-501          │
Phase 7  Research sandbox    GN-502,601,202,303
Cross-phase                  GN-705 (budgets: each row measured in the phase that introduces the operation)
```

> **Phase 0a requires only tier N0 (~70 MB: numpy, scipy, sklearn).** PyTorch is not needed until
> Phase 1. This is deliberate: the entire verification substrate — baselines, metrics, calibration,
> feature store, anti-stub harness — must be installable and runnable in CI and on developer laptops
> without a 2 GB download. If Phase 0a is correctly built, you can prove the hash stub fails before
> torch is ever installed.

### Phase 0a — Numerical Substrate `GN-010 … GN-016`

Tier N0 only. No torch. This phase turns a repository with **zero numerical infrastructure** into
one that can measure things.

Exit gate — all must be true:

- [ ] `GN-PH0a.G01` `pip install -e ".[numerics]"` succeeds; `pip install -e .` resolves to an **unchanged** package set (diff `pip freeze` before/after)
- [ ] `GN-PH0a.G02` All four extras (`numerics`, `neural`, `neural-text`, `neural-research`) resolve on Linux x86_64 / py3.11
- [ ] `GN-PH0a.G03` `requirements-neural.lock` exists with `--generate-hashes`; offline install from a wheel cache succeeds
- [ ] `GN-PH0a.G04` Default install is **CPU-only** — `torch.version.cuda` is `None`
- [ ] `GN-PH0a.G05` `GN-011`: `cosine_matrix` over 100k×128 in < 20 ms, with the speedup factor over the old Python-loop version recorded
- [ ] `GN-PH0a.G06` `GN-011`: `grep -rn "for i in range(dim" packages/eoip/neural/` → zero hits
- [ ] `GN-PH0a.G07` `GN-012`: same seed across **separate processes** reproduces metrics within 1e-4; different seed produces different metrics
- [ ] `GN-PH0a.G08` `GN-013`: serving process has all four thread env vars at `1`; oversubscription probe measured and recorded
- [ ] `GN-PH0a.G09` `GN-015`: softmax over `[1000.0, 1001.0]` finite; zero-vector cosine documented not NaN; empty-array reductions all specified
- [ ] `GN-PH0a.G10` `GN-016`: oversized job refused **before** allocation with a workable batch size named
- [ ] `GN-PH0a.G11` Ledgers filed for GN-010 … GN-016

> **The sequencing payoff:** by the end of Phase 0a you can run the anti-stub harness against the
> existing hash stub and watch all four probes fail — using only numpy. That is the cheapest
> possible proof that the verification regime works, obtained before committing to a 2 GB dependency.

### Phase 0b — Contracts & Harness `GN-001 … GN-007`

**This is the phase most likely to be skipped and most expensive to skip.** Every anti-stub guard,
leakage guard and baseline lives here. Building models first and contracts later guarantees the
models are unmeasurable.

Exit gate — all must be true:

- [ ] `GN-PH0b.G01` `GN-001` four-venv tier matrix passes: `NONE` / `NUMERICS` / `NEURAL` / `TEXT` detected correctly, no raises
- [ ] `GN-PH0b.G02` In the empty venv: `python -c "import eoip.platform_router"` exits 0
- [ ] `GN-PH0b.G03` N0-only endpoints return 200 with torch absent; N1 endpoints return 503 **naming the missing tier**
- [ ] `GN-PH0b.G04` `GN-003` harness scores the **existing hash stub** as `passed == False` on all four probes
      *(this is the self-test — if the harness passes the stub, the harness is wrong)*
- [ ] `GN-PH0b.G05` `GN-005` leakage validator **raises** on a deliberately leaked split
- [ ] `GN-PH0b.G06` `GN-006` emits all five baselines on the reference snapshot
- [ ] `GN-PH0b.G07` `GN-006` refuses to emit a report containing AUROC without AUPRC
- [ ] `GN-PH0b.G08` `GN-002` rejects a `PredictedEdge` constructed as `OBSERVED`
- [ ] `GN-PH0b.G09` Reference snapshot `ref-2026-10` is committed and content-addressed; two machines produce the same id
- [ ] `GN-PH0b.G10` Ledgers filed for GN-001 … GN-007

### Phase 1 — Core GNN `GN-101, GN-102`

Exit gate:

- [ ] `GN-PH1.G01` `GN-101` R-GCN: V2–V7 green, **all four anti-stub probes pass**
- [ ] `GN-PH1.G02` Hash stubs **deleted**; `get_gnn_engine()` still imports and works
- [ ] `GN-PH1.G03` `GN-102` GraphSAGE: inductive proof passes (new nodes embedded with zero weight change)
- [ ] `GN-PH1.G04` At least one model beats `CommonNeighborsBaseline` **and** `RuleBaseline` by ≥ 0.05 AUPRC
- [ ] `GN-PH1.G05` Full existing test suite green — no regression in any pre-existing test file counted in the Phase 0a baseline record (GN-010 ledger; re-count — do not assume 302 or 239, XP-16)

> If R-GCN does not clear the baselines, **stop and escalate.** Do not proceed to Phase 2.
> Either the task is not learnable from this graph, the features are inadequate, or the labels are
> wrong. All three are findings worth more than a shipped model.

### Phase 2 — Integration, Explainability & Security `GN-203, GN-701, GN-702, GN-703, GN-704, GN-706`

The first phase that produces user-visible value. Nothing from Phases 3+ is worth building until a
prediction can be served, explained, and secured.

Exit gate:

- [ ] `GN-PH2.G01` All 15 routes in `/openapi.json`, schemas resolving
- [ ] `GN-PH2.G02` `neural` key in `GET /brain/telemetry`
- [ ] `GN-PH2.G03` ≥ 95% of predictions carry non-empty `evidence_paths`
- [ ] `GN-PH2.G04` Faithfulness probe: removing the evidence subgraph drops the score ≥ 50%
- [ ] `GN-PH2.G05` Cross-tenant probe returns empty
- [ ] `GN-PH2.G06` Membership-inference probe: no disclosure via result count, latency, **or** error message
- [ ] `GN-PH2.G07` Every route returns 503 without the required tier — never a fabricated result
- [ ] `GN-PH2.G08` `GN-702` dual-path fusion returns both neural and deterministic answers; disagreement flagged `DISPUTED`
- [ ] `GN-PH2.G09` `GN-203` NL bridge: 20/20 hallucination probes answer "not found"; all cited ids resolve
- [ ] `GN-PH2.G10` `GN-706` guards active: 2-layer default enforced, oversmoothing variance measured at 2/4/8 layers

### Phase 3 — Temporal `GN-301, GN-302`

Exit gate:

- [ ] `GN-PH3.G01` Batch-level leakage validator active on every training batch
- [ ] `GN-PH3.G02` Deliberate-injection leakage test raises
- [ ] `GN-PH3.G03` `GN-301` beats most-frequent baseline by ≥ 0.10 Macro-F1
- [ ] `GN-PH3.G04` `GN-302` either beats `GN-301` by ≥ 0.05 MRR **or** is filed FAILED with "GRU sufficient"

### Phase 4 — Advanced Encoders `GN-103, GN-104, GN-201`

**Every item is bake-off gated.** The honest expected outcome is that one or two of these do not
justify themselves on enterprise graphs. Budget for that.

Exit gate:
- [ ] `GN-PH4.G01` Each ran a bake-off against `GN-101` on the same split
- [ ] `GN-PH4.G02` Each is either promoted with its margin recorded, or filed FAILED with its margin recorded
- [ ] `GN-PH4.G03` A written recommendation names the default production encoder

### Phase 5 — Convolutional `GN-401, GN-402, GN-403`
Exit gate: ChebNet zero false positives on the clean control fixture; ConvE parameter-efficiency
claim measured (not cited); vision extractions 100% `PREDICTED` with bounding-box provenance.

Gate check IDs: `GN-PH5.G01` ChebNet zero false positives; `GN-PH5.G02` ConvE parameter-efficiency claim measured; `GN-PH5.G03` vision extractions 100% `PREDICTED`.

### Phase 6 — Quality Gate `GN-501`
Exit gate: precision ≥ 0.80 at recall ≥ 0.70; flagged triples quarantined and reviewable, never
deleted; < 5 ms per triple; ontology veto overrides learned score.

Gate check IDs: `GN-PH6.G01` precision ≥ 0.80 at recall ≥ 0.70; `GN-PH6.G02` flagged triples quarantined and reviewable, never deleted; `GN-PH6.G03` < 5 ms per triple; `GN-PH6.G04` ontology veto overrides learned score.

### Phase 7 — Research Sandbox `GN-502, GN-601, GN-202, GN-303`
Exit gate: import-graph test proves zero production dependencies; every efficiency claim measured on
real hardware; "not justified" is an acceptable and expected outcome for any of these.

Gate check IDs: `GN-PH7.G01` import-graph test proves zero production dependencies; `GN-PH7.G02` every efficiency claim measured on real hardware; `GN-PH7.G03` "not justified" is an acceptable and expected outcome.

---

## 2. Reference Fixtures — Build These First

Without fixed fixtures, every metric is unreproducible and every comparison is meaningless.

| Fixture | Path | Purpose | Spec |
|---|---|---|---|
| `known_graph.json` | `tests/neural/fixtures/` | V3 behavioural | 200 nodes, 600 edges, 5 named types, 5 deliberately removed edges with documented expected ranks |
| `role_identical.json` | `tests/neural/fixtures/` | Anti-stub P4 | Two nodes with provably identical structural roles (automorphic) |
| `leaky_split.json` | `tests/neural/fixtures/` | Leakage guard | Contains a test edge timestamped before train_end — validator must raise |
| `clean_ontology.json` | `tests/neural/fixtures/` | False-positive control | Structurally valid; anomaly detectors must return zero flags |
| `broken_ontology.json` | `tests/neural/fixtures/` | Anomaly detection | One subsumption cycle, one unreachable cluster, both labelled |
| `implausible_triples.json` | `tests/neural/fixtures/` | Discriminator | 100 true + 100 hand-crafted implausible, labelled |
| `multi_domain.json` | `tests/neural/fixtures/` | HGT bake-off | ≥ 3 domains with genuinely different type distributions |
| `ref-2026-10` | `artifacts/neural/snapshots/` | The reference snapshot | Content-addressed; **all reported metrics use this** |

Tracker IDs: `GN-FX-01` … `GN-FX-08` are the eight fixture rows above, in table order.

**Rule:** the reference snapshot is frozen. If it changes, every prior metric is invalid and every
ledger must be re-run. Version it; never edit it in place.

---

## 3. Agent Operating Rules

### 3.1 Per-requirement loop

```
1. READ      the requirement in GN-REQ-v1. If ambiguous -> file Q-### and pick different work.
2. INSPECT   the current repo state. Do not trust this plan's description of it; verify.
3. BUILD     the minimum that satisfies the requirement. No speculative extras.
4. RUN       the verification commands. Capture real output.
5. MEASURE   against the named thresholds with the mandated baselines.
6. LEDGER    write EOIP-engg-doc-pkg/evidence/GN-<id>.md with pasted output.
7. REPORT    status + the measured numbers. Never "done" without numbers.
```

### 3.2 Hard prohibitions

| Never | Because |
|---|---|
| Add a silent heuristic fallback when torch is missing | This is exactly how the hash stub came to exist |
| Write a neural result as `OBSERVED` | Predictions are not facts (`GN-002`) |
| Report AUROC without AUPRC | Hides catastrophic performance on imbalanced link prediction |
| Split data randomly when the task is temporal | Leakage; inflates every number |
| Use `UNIFORM` negatives for a headline metric | Easy negatives inflate scores; `TYPE_CONSTRAINED` is the standard |
| Tune on the test split | Invalidates the whole evaluation |
| Add a dependency not in the §1.3 licence table | Standing GPL/AGPL prohibition |
| Introduce a second graph ML framework (DGL) | PyG is sufficient; two is maintenance waste |
| Make any tier a core dependency | Breaks air-gap and edge deployments; core must stay at 9 packages |
| Add numpy to core "because it's small" | 70 MB is not small for edge; it is tier N0 for a reason |
| Write a Python loop over array elements in a hot path | 50–200× slower than numpy; this is how `_cosine_similarity` got slow |
| Use float64 for stored embeddings | Doubles memory for no accuracy gain; float32 is the policy |
| Set `OMP_NUM_THREADS` after importing numpy | Has no effect; BLAS reads it at import |
| Set only `OMP_NUM_THREADS` | Ineffective half-fix; all four vars must be set together |
| Train without recording the seed and environment | Makes the Evidence Ledger unreproducible and therefore worthless |
| Ship CUDA wheels as the install default | NVIDIA SLA redistribution terms; ~5× larger; CPU is the default |
| Leave transitive deps unpinned | 2 GB tree, supply-chain risk, irreproducible builds |
| Return NaN from a reduction | Propagates silently and surfaces three layers away as a meaningless prediction |
| Exceed 2 GNN layers by default | Oversmoothing |
| Delete a flagged triple | Quarantine and surface it instead |
| Edit the frozen reference snapshot | Invalidates every prior measurement |
| Claim completion without a ledger entry | The ledger *is* the completion |

### 3.3 When a threshold is missed

Do **not** silently lower it. In order:

1. Re-check for a bug (leakage, wrong split, broken negatives) — most misses are defects, not model limits.
2. Try the documented hyperparameter ranges, once.
3. If it still misses: file `Status: FAILED` with real numbers and a recommendation.
4. Escalate in the open-questions file if the failure blocks a downstream phase.

A missed threshold honestly reported is a completed requirement. A met threshold achieved by
changing the threshold is fraud.

---

## 4. Integration Checklist (applies to every engine)

Copy this into each ledger. These are the house conventions, verified not assumed.

- [ ] Pydantic request models declared at **module level**, not inside functions
      *(FastAPI cannot resolve nested-class schemas — this has broken this codebase before)*
- [ ] Thread-safe singleton: `_instance` + `_lock`, double-checked locking
- [ ] Module-level `get_<name>_engine()` accessor
- [ ] `stats()` method returning a JSON-serialisable dict
- [ ] Registered in `packages/eoip/brain/brain_os.py` telemetry
- [ ] Router included in `packages/eoip/platform_router.py`
- [ ] `from __future__ import annotations` at the top; PEP 604 unions (`X | None`)
- [ ] Import-safe without torch, **or** imported lazily behind `require_tier()`
- [ ] No module-level torch import anywhere reachable from EOIP startup
- [ ] Declares its **minimum tier**; returns 503 naming that tier when unmet
- [ ] Arrays are `np.float32`; `list[float]` only at JSON boundaries
- [ ] `assert_finite()` applied to every array crossing the module boundary
- [ ] Training entry points call `seed_everything()` and record `capture_environment()`
- [ ] Peak RSS (and GPU memory, if used) captured for the ledger's V7 section

---

## 5. Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| NR1 | Phase 0 skipped under schedule pressure | **High** | **Critical** | Phase gate is hard. No model work merges before the harness scores the hash stub as failing |
| NR2 | Model beats baselines only via temporal leakage | High | Critical | `GN-005` batch validator + deliberate-injection test |
| NR3 | Model learns popularity, not structure | High | High | `DegreeBaseline` mandatory in every ledger |
| NR4 | torch install fails on target platforms | Medium | High | Optional extra; core unaffected; CPU wheels pinned |
| NR5 | Graph too small for GNNs to beat heuristics | **Medium** | High | Honest FAILED outcome; this is a real possibility and an acceptable result |
| NR6 | Embeddings leak restricted data | Medium | **Critical** | `GN-703` entitlement-before-featurisation + membership-inference probe |
| NR7 | Explanations are decorative, not faithful | Medium | High | Faithfulness probe: removing evidence must drop score ≥ 50% |
| NR8 | Predictions drift into the graph as facts | Low | **Critical** | Type-level enforcement in `GN-002` + store-adapter guard + audit query |
| NR9 | Six architectures shipped, none measured | Medium | High | Every advanced encoder is bake-off gated |
| NR10 | Inference cost exceeds product economics | Medium | Medium | `GN-705` budgets measured per phase, not at the end |
| NR11 | Reference snapshot edited mid-programme | Low | High | Content-addressed id; CI asserts the hash |
| NR12 | **BLAS oversubscription** — N workers × M BLAS threads collapses throughput | **High** | High | `GN-013`; looks like a mystery perf bug, is a config error |
| NR13 | Metrics irreproducible; ledgers unverifiable | **High** | **Critical** | `GN-012` cross-process determinism test |
| NR14 | Silent NaN reaches a prediction and looks plausible | Medium | High | `GN-015` `assert_finite` at every module boundary |
| NR15 | CUDA wheels pulled by default; NVIDIA SLA redistribution exposure | Medium | High | CPU index is the documented default; Legal review before any bundled appliance |
| NR16 | Air-gap install broken by a 2 GB PyPI-dependent tree | Medium | High | `GN-014` wheel bundle + hash-pinned lockfile |
| NR17 | float64 creep doubles memory and breaks budgets | Medium | Medium | dtype assertion in `FeatureStore.put` |
| NR18 | Numpy added to core "just for convenience" | Medium | Medium | CI diffs the core resolved package set against a committed baseline |

---

## 6. Effort Shape

Not a schedule — a relative shape. Multiply by your team's actual throughput.

| Phase | Relative effort | Tier needed | Can parallelise? | Notes |
|---|---:|---|---|---|
| 0a Numerical substrate | 12% | N0 | Partly | Provisioning, dtype, determinism, threads, stability |
| 0b Contracts & harness | 18% | N0 | Partly | Largest single block. Resist compressing it |
| 1 Core GNN | 18% | N1 | No | Sequential on Phase 0 |
| 2 Integration | 14% | N1/N2 | Partly | First user value |
| 3 Temporal | 11% | N1 | No | Needs Phase 1 embeddings |
| 4 Advanced | 11% | N1 | **Yes** | Three independent bake-offs |
| 5 Convolutional | 8% | N1 | Yes | |
| 6 Quality gate | 5% | N1 | Yes | |
| 7 Research | 3% | N3 | Yes | Timeboxed; expected to produce findings, not features |

**Phases 0a + 0b + 1 + 2 = 62% of the effort and 100% of the shippable value.** Phases 3–7 are
optional expansions, each justified by its own bake-off. A programme that completes Phases 0–2
honestly is far more valuable than one that touches all six architectures without measuring any.

**30% of the total effort (Phases 0a + 0b) needs only a 70 MB dependency tier.** Front-loading that
work means the verification regime is proven before the 2 GB commitment, and CI stays fast for the
majority of the programme.

---

## 7. Final Sign-Off Checklist

The programme is complete when a human reviewer can tick every box **by reading the ledgers alone**,
without inspecting a single source file:

- [ ] `GN-SO-01` Evidence ledger exists for every P0 requirement
- [ ] `GN-SO-02` Every ledger contains **pasted command output**, not descriptions of output
- [ ] `GN-SO-03` Every learned model shows all four anti-stub probes passing
- [ ] `GN-SO-04` Every statistical claim shows **all five baselines** beside it
- [ ] `GN-SO-05` No ledger reports AUROC without AUPRC
- [ ] `GN-SO-06` Hash stubs deleted; verified by `grep -r "_deterministic_vector" packages/` returning only `tests/`
- [ ] `GN-SO-07` `pip install -e .` (no extras) → resolved package set **unchanged** from pre-programme baseline → EOIP starts → N1 routes return 503 naming the tier
- [ ] `GN-SO-08` `pip install -e ".[numerics]"` → metrics, baselines and embedding lookup work **without torch**
- [ ] `GN-SO-09` `pip install -e ".[neural]"` → neural routes return real predictions; `torch.version.cuda is None` on the default index
- [ ] `GN-SO-10` Offline install from the wheel bundle succeeds on a network-isolated machine
- [ ] `GN-SO-11` Every ledger records its seed and `capture_environment()`; one metric picked at random is re-run and reproduces within 1e-4
- [ ] `GN-SO-12` `grep -rn "for i in range(dim" packages/eoip/neural/` returns zero hits
- [ ] `GN-SO-13` Audit query confirms zero neural-origin `OBSERVED` assertions
- [ ] `GN-SO-14` Failed requirements documented as FAILED with numbers and a recommendation
- [ ] `GN-SO-15` Open questions file is empty, or every entry has a recorded decision
- [ ] `GN-SO-16` Full pre-existing test suite green — no regression in any pre-existing test file counted in the Phase 0a baseline record (GN-010 ledger; re-count — do not assume 302 or 239, XP-16)

> **The last line of defence:** if a reviewer cannot reproduce a claimed number by running the
> command pasted in its ledger, that requirement is not complete — regardless of how much code
> exists, how well it is written, or how many tests accompany it.

<!-- tracker-integration -->

## 8. Tracker Procedure

This section maps the completion protocol of §0 onto the EOIP programme tracker. It adds no scope and changes no gate.

### 8.1 Files

| File (copy into the repository) | Purpose |
|---|---|
| `tools/tracker/EOIP-programme-tracker.html` | Interactive tracker for ASPEII, CIP, IP and Graph Neurons (open in a browser; state is kept in the browser and exported as JSON) |
| `tools/tracker/EOIP-programme-registry.json` | Every tracked item: id, programme, kind, parent, work package or phase, source `file:line`, normative text and its SHA-256 |
| `tools/tracker/programme_rules.js` | The single rules engine used by the tracker page and the verifier |
| `tools/tracker/verify_programme_ledger.mjs` | Command-line verifier; exit 0 only when the requested scope is complete with no problem |
| `docs/programme/programme-ledger.json` | The committed consolidated ledger (`eoip-programme-ledger-v1`), exported from the tracker or written by agents |

The Evidence Ledger files stay the completion record (§0.3). The tracker holds one item per ledger, one per done-when check, one per gate check and one per sign-off line, each pointing at the ledger file and its SHA-256.

### 8.2 Identifiers

| Phase gate | Ledgers in the phase | Gate checks | Closes after |
| --- | --- | --- | --- |
| `GN-PH0a.GATE` | GN-010, GN-011, GN-012, GN-013, GN-014, GN-015, GN-016 | `GN-PH0a.G01` … `GN-PH0a.G11` (11) | — |
| `GN-PH0b.GATE` | GN-001, GN-002, GN-003, GN-004, GN-005, GN-006, GN-007 | `GN-PH0b.G01` … `GN-PH0b.G10` (10) | GN-PH0a.GATE |
| `GN-PH1.GATE` | GN-101, GN-102 | `GN-PH1.G01` … `GN-PH1.G05` (5) | GN-PH0b.GATE |
| `GN-PH2.GATE` | GN-203, GN-701, GN-702, GN-703, GN-704, GN-706 | `GN-PH2.G01` … `GN-PH2.G10` (10) | GN-PH1.GATE |
| `GN-PH3.GATE` | GN-301, GN-302 | `GN-PH3.G01` … `GN-PH3.G04` (4) | GN-PH2.GATE |
| `GN-PH4.GATE` | GN-103, GN-104, GN-201 | `GN-PH4.G01` … `GN-PH4.G03` (3) | GN-PH3.GATE |
| `GN-PH5.GATE` | GN-401, GN-402, GN-403 | `GN-PH5.G01` … `GN-PH5.G03` (3) | GN-PH4.GATE |
| `GN-PH6.GATE` | GN-501 | `GN-PH6.G01` … `GN-PH6.G04` (4) | GN-PH5.GATE |
| `GN-PH7.GATE` | GN-202, GN-303, GN-502, GN-601 | `GN-PH7.G01` … `GN-PH7.G03` (3) | GN-PH6.GATE |

`GN-705` is cross-phase (its rows are measured as each operation appears; work may start after Phase 0b) and `GN-706` belongs to Phase 2 (XP-17). Sign-off lines are `GN-SO-01` … `GN-SO-16`; fixtures are `GN-FX-01` … `GN-FX-08`; requirements §11 items are `GN-CD-01` … `GN-CD-10`.

Phases are start-gated in the tracker: no item of phase *n* may leave OPEN until the phase *n−1* gate is VERIFIED (requirements §3 "Nothing in §4–§9 may begin until §3 is complete and verified"; §1 "strictly sequential at the gate level").

### 8.3 Per-Requirement Loop in the Tracker

| §3.1 step | Tracker action |
| --- | --- |
| 1 READ | If ambiguous, add a `Q-NNN` entry in the tracker's decision log with the affected ids and "blocks" ticked; continue with other work |
| 2 INSPECT, 3 BUILD | Set the ledger item `IN_PROGRESS`; record `CODE_COMPLETE` with the commit when code lands (earns nothing) |
| 4 RUN, 5 MEASURE | For each check `GN-<id>.Dnn` record `EVIDENCED` with the pasted measured result; V4 checks need the five baselines and snapshot id; V5 checks need P1–P4 |
| 6 LEDGER | Write `EOIP-engg-doc-pkg/evidence/GN-<id>.md`; record its SHA-256 on the ledger item and every check |
| 7 REPORT | A reviewer who is not the producer reproduces one number within 1e-4 and records `VERIFIED` (ledger `COMPLETE`), or, for GN-103, GN-104, GN-201, GN-202, GN-302, GN-303, GN-402, GN-403, GN-502, GN-601, GN-702 only, `FAILED_ACCEPTED` with the real numbers and recommendation |

Export `graph-neurons-open-questions.md` from the tracker's Ledger tab whenever a `Q-NNN` entry changes. Then run:

```bash
# create an empty ledger once
node tools/tracker/verify_programme_ledger.mjs --init > docs/programme/programme-ledger.json
# check the ledger and recompute every evidence digest in the working tree
node tools/tracker/verify_programme_ledger.mjs --ledger docs/programme/programme-ledger.json --repo . --programme GN
```

### 8.4 Evidence Required per Transition

A file path, class or function name, test-file name, test count, commit hash, green CI badge, screenshot or an agent's statement is never proof of completion on its own. The tracker and the verifier refuse EVIDENCED unless an executed run is recorded (command, exit code 0, environment, evidence path and its SHA-256, bound to the current requirement text), and refuse VERIFIED unless a reviewer who is not the producer re-ran it and recorded the verification reference.

| Target state | Required evidence (checked by the tracker and by `verify_programme_ledger.mjs`) |
|---|---|
| IN_PROGRESS | Owner and work reference (task card, branch, ledger draft or DR id). |
| CODE_COMPLETE | 40-hex commit and the changed paths. The paths are navigation only and are never proof. |
| EVIDENCED (draft ledger) | Commit; ledger path `EOIP-engg-doc-pkg/evidence/GN-<id>.md` and its SHA-256; producer; exact command; exit code 0; environment; for every check the measured result pasted from real output; V4 checks: all five baselines beside the model number and the snapshot id; V5 checks: probes P1–P4 with measurements; ledgers: seed and `capture_environment()` reference. |
| VERIFIED | Everything above plus reviewer different from the producer, review date, sign-off reference, re-run attestation (one number reproduced within 1e-4); a ledger is COMPLETE only when every one of its checks is VERIFIED. |
| FAILED | Failure note with the observed numbers or error, and a reference to the failing run. |
| BLOCKED | The blocking dependency, decision id or missing input. |
| STALE | What changed (source, artifact, environment or requirement text). |

Evidence digest: for a file, the SHA-256 of its bytes; for a directory, the SHA-256 of the UTF-8 text made of one line `<path relative to the directory>\t<sha256 of that file>\n` per file, sorted by path. `--repo` recomputes it and reports any mismatch as STALE.

### 8.5 Decisions Recorded for This Plan

- **XP-16 Graph Neurons pre-existing test-file count (302 vs 239).** Neither number is assumed. Count `find tests -name "test_*.py" | wc -l` at the Phase 0a baseline, record the number and the file list digest in the GN-010 ledger, and use that recorded number for GN-PH1.G05 and GN-SO-16.
- **XP-17 GN-705 and GN-706 have no phase.** GN-706 belongs to Phase 2 (its gate already checks it). GN-705 is cross-phase: each budget row is measured in the phase that introduces the operation and the GN-705 ledger closes at final sign-off.
- **XP-18 'A missed threshold honestly reported is complete' vs P0 must pass.** An honest FAILED ledger resolves a requirement only where the requirement text allows that outcome (GN-103, 104, 201, 202, 302, 303, 402, 403, 502, 601, 702). A FAILED P0 requirement is recorded honestly and blocks programme completion (Phase 1 'stop and escalate').
