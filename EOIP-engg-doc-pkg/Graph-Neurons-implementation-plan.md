# Graph Neurons — Implementation Plan & Completion Protocol

> **Document ID**: GN-PLAN-v1
> **Date**: 2026-10-16
> **Pairs with**: `Graph-Neurons-requirements.md` (GN-REQ-v1) — read that first
> **Revision**: v1.1 (2026-10-18) — CPU-only distribution (H-16), CPU-first qualification (H-15, H-17 interim); see GN-REQ §0.6
> **Audience**: the AI coding agent executing this work, and the human who signs it off
> **Purpose**: how the work is sequenced, how it is proven done, and what disqualifies a completion claim

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
Phase 2  Integration & XAI   GN-203,701-704  │ ← first user-visible value lands here
Phase 3  Temporal            GN-301,302      │
Phase 4  Advanced encoders   GN-103,104,201  │ ← each is bake-off gated; may legitimately not ship
Phase 5  Convolutional       GN-401,402,403  │
Phase 6  Quality gate (GAN)  GN-501          │
Phase 7  Research sandbox    GN-502,601,202,303
```

> **Phase 0a requires only tier N0 (numpy, scipy, sklearn).** PyTorch is not needed until
> Phase 1. This is deliberate: the entire verification substrate — baselines, metrics, calibration,
> feature store, anti-stub harness — must be installable and runnable in CI and on developer laptops
> without installing torch. If Phase 0a is correctly built, you can prove the hash stub fails before
> torch is ever installed.

### Phase 0a — Numerical Substrate `GN-010 … GN-016`

Tier N0 only. No torch. This phase turns a repository with **zero numerical infrastructure** into
one that can measure things.

Exit gate — all must be true:

- [ ] `pip install -e ".[numerics]"` succeeds; `pip install -e .` resolves to an **unchanged** package set (diff `pip freeze` before/after)
- [ ] All four extras (`numerics`, `neural`, `neural-text`, `neural-research`) resolve on Linux x86_64 / py3.11
- [ ] `requirements-neural.lock` exists with `--generate-hashes`; offline install from a wheel cache succeeds
- [ ] Default install is **CPU-only** — `torch.version.cuda` is `None`
- [ ] Lock file and offline bundle contain **zero `nvidia-*` packages** (H-16); all Phase 0 measurements taken on a host with no GPU visible (H-17 interim)
- [ ] `GN-011`: `cosine_matrix` over 100k×128 in < 20 ms, with the speedup factor over the old Python-loop version recorded
- [ ] `GN-011`: `grep -rn "for i in range(dim" packages/eoip/neural/` → zero hits
- [ ] `GN-012`: same seed across **separate processes** reproduces metrics within 1e-4; different seed produces different metrics
- [ ] `GN-013`: serving process has all four thread env vars at `1`; oversubscription probe measured and recorded
- [ ] `GN-015`: softmax over `[1000.0, 1001.0]` finite; zero-vector cosine documented not NaN; empty-array reductions all specified
- [ ] `GN-016`: oversized job refused **before** allocation with a workable batch size named
- [ ] Ledgers filed for GN-010 … GN-016

> **The sequencing payoff:** by the end of Phase 0a you can run the anti-stub harness against the
> existing hash stub and watch all four probes fail — using only numpy. That is the cheapest
> possible proof that the verification regime works, obtained before installing torch at all.

### Phase 0b — Contracts & Harness `GN-001 … GN-007`

**This is the phase most likely to be skipped and most expensive to skip.** Every anti-stub guard,
leakage guard and baseline lives here. Building models first and contracts later guarantees the
models are unmeasurable.

Exit gate — all must be true:

- [ ] `GN-001` four-venv tier matrix passes: `NONE` / `NUMERICS` / `NEURAL` / `TEXT` detected correctly, no raises
- [ ] In the empty venv: `python -c "import eoip.platform_router"` exits 0
- [ ] N0-only endpoints return 200 with torch absent; N1 endpoints return 503 **naming the missing tier**
- [ ] `GN-003` harness scores the **existing hash stub** as `passed == False` on all four probes
      *(this is the self-test — if the harness passes the stub, the harness is wrong)*
- [ ] `GN-005` leakage validator **raises** on a deliberately leaked split
- [ ] `GN-006` emits all five baselines on the reference snapshot
- [ ] `GN-006` refuses to emit a report containing AUROC without AUPRC
- [ ] `GN-002` rejects a `PredictedEdge` constructed as `OBSERVED`
- [ ] Reference snapshot `ref-2026-10` is committed and content-addressed; two machines produce the same id
- [ ] Ledgers filed for GN-001 … GN-007

### Phase 1 — Core GNN `GN-101, GN-102`

Exit gate:

- [ ] `GN-101` R-GCN: V2–V7 green, **all four anti-stub probes pass**
- [ ] Hash stubs **deleted**; `get_gnn_engine()` still imports and works
- [ ] `GN-102` GraphSAGE: inductive proof passes (new nodes embedded with zero weight change)
- [ ] At least one model beats `CommonNeighborsBaseline` **and** `RuleBaseline` by ≥ 0.05 AUPRC
- [ ] Full existing test suite green — no regression across the other 302 test files

> If R-GCN does not clear the baselines, **stop and escalate.** Do not proceed to Phase 2.
> Either the task is not learnable from this graph, the features are inadequate, or the labels are
> wrong. All three are findings worth more than a shipped model.

### Phase 2 — Integration, Explainability & Security `GN-203, GN-701, GN-702, GN-703, GN-704`

The first phase that produces user-visible value. Nothing from Phases 3+ is worth building until a
prediction can be served, explained, and secured.

Exit gate:

- [ ] All 15 routes in `/openapi.json`, schemas resolving
- [ ] `neural` key in `GET /brain/telemetry`
- [ ] ≥ 95% of predictions carry non-empty `evidence_paths`
- [ ] Faithfulness probe: removing the evidence subgraph drops the score ≥ 50%
- [ ] Cross-tenant probe returns empty
- [ ] Membership-inference probe: no disclosure via result count, latency, **or** error message
- [ ] Every route returns 503 without the required tier — never a fabricated result
- [ ] `GN-702` dual-path fusion returns both neural and deterministic answers; disagreement flagged `DISPUTED`
- [ ] `GN-203` NL bridge: 20/20 hallucination probes answer "not found"; all cited ids resolve
- [ ] `GN-706` guards active: 2-layer default enforced, oversmoothing variance measured at 2/4/8 layers

### Phase 3 — Temporal `GN-301, GN-302`

Exit gate:

- [ ] Batch-level leakage validator active on every training batch
- [ ] Deliberate-injection leakage test raises
- [ ] `GN-301` beats most-frequent baseline by ≥ 0.10 Macro-F1
- [ ] `GN-302` either beats `GN-301` by ≥ 0.05 MRR **or** is filed FAILED with "GRU sufficient"

### Phase 4 — Advanced Encoders `GN-103, GN-104, GN-201`

**Every item is bake-off gated.** The honest expected outcome is that one or two of these do not
justify themselves on enterprise graphs. Budget for that.

Exit gate:
- [ ] Each ran a bake-off against `GN-101` on the same split
- [ ] Each is either promoted with its margin recorded, or filed FAILED with its margin recorded
- [ ] A written recommendation names the default production encoder

### Phase 5 — Convolutional `GN-401, GN-402, GN-403`
Exit gate: ChebNet zero false positives on the clean control fixture; ConvE parameter-efficiency
claim measured (not cited); vision extractions 100% `PREDICTED` with bounding-box provenance.

### Phase 6 — Quality Gate `GN-501`
Exit gate: precision ≥ 0.80 at recall ≥ 0.70; flagged triples quarantined and reviewable, never
deleted; < 5 ms per triple; ontology veto overrides learned score.

### Phase 7 — Research Sandbox `GN-502, GN-601, GN-202, GN-303`
Exit gate: import-graph test proves zero production dependencies; every efficiency claim measured on
real hardware; "not justified" is an acceptable and expected outcome for any of these.

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
| Add numpy to core "because it's small" | It changes every install, including edge and air-gapped ones; it is tier N0 for a reason |
| Write a Python loop over array elements in a hot path | 50–200× slower than numpy; this is how `_cosine_similarity` got slow |
| Use float64 for stored embeddings | Doubles memory for no accuracy gain; float32 is the policy |
| Set `OMP_NUM_THREADS` after importing numpy | Has no effect; BLAS reads it at import |
| Set only `OMP_NUM_THREADS` | Ineffective half-fix; all four vars must be set together |
| Train without recording the seed and environment | Makes the Evidence Ledger unreproducible and therefore worthless |
| Ship, bundle, mirror or redistribute any CUDA / `nvidia-*` package | Not permitted — decision H-16 (`docs/decisions/ADR-H16-no-cuda-redistribution.md`) |
| Make any binding gate depend on a GPU | GPU availability is unknown (H-17); CPU-first policy (ADR-H15) |
| Publish a CUDA install command in EOIP documentation | Customer-provisioned GPUs are unsupported until H-17 |
| Leave transitive deps unpinned | Large transitive tree, supply-chain risk, irreproducible builds |
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
| NR15 | CUDA packages enter a distributed artifact | **Closed by H-16** | High | CPU-only builds everywhere; CI licence gate rejects any `nvidia-*` in lock files, bundles and images |
| NR16 | Air-gap install broken by a large PyPI-dependent tree | Medium | High | `GN-014` wheel bundle + hash-pinned lockfile |
| NR17 | float64 creep doubles memory and breaks budgets | Medium | Medium | dtype assertion in `FeatureStore.put` |
| NR18 | Numpy added to core "just for convenience" | Medium | Medium | CI diffs the core resolved package set against a committed baseline |
| NR19 | An architecture meets its margin only with a GPU | Medium | Medium | Recorded `DEFERRED (H-17)` with CPU numbers; CPU-feasible defaults and neighbour sampling (ADR-H15) |
| NR20 | CPU training misses the full-retrain budget at P1/P2 scale | Medium | High | Mini-batch neighbour sampling; budget breach recorded and raised to H-17 as GPU evidence |

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

**30% of the total effort (Phases 0a + 0b) needs only tier N0.** Front-loading that
work means the verification regime is proven before torch is installed, and CI stays fast for the
majority of the programme.

---

## 7. Final Sign-Off Checklist

The programme is complete when a human reviewer can tick every box **by reading the ledgers alone**,
without inspecting a single source file:

- [ ] Evidence ledger exists for every P0 requirement
- [ ] Every ledger contains **pasted command output**, not descriptions of output
- [ ] Every learned model shows all four anti-stub probes passing
- [ ] Every statistical claim shows **all five baselines** beside it
- [ ] No ledger reports AUROC without AUPRC
- [ ] Hash stubs deleted; verified by `grep -r "_deterministic_vector" packages/` returning only `tests/`
- [ ] `pip install -e .` (no extras) → resolved package set **unchanged** from pre-programme baseline → EOIP starts → N1 routes return 503 naming the tier
- [ ] `pip install -e ".[numerics]"` → metrics, baselines and embedding lookup work **without torch**
- [ ] `pip install -e ".[neural]"` → neural routes return real predictions; `torch.version.cuda is None` on the default index
- [ ] Offline install from the wheel bundle succeeds on a network-isolated machine
- [ ] No distributed artifact (lock file, wheel bundle, image) contains an `nvidia-*` package (H-16)
- [ ] Every binding gate was met on a host with no GPU; any GPU results are reported separately as non-binding (H-17)
- [ ] Every ledger records its seed and `capture_environment()`; one metric picked at random is re-run and reproduces within 1e-4
- [ ] `grep -rn "for i in range(dim" packages/eoip/neural/` returns zero hits
- [ ] Audit query confirms zero neural-origin `OBSERVED` assertions
- [ ] Failed requirements documented as FAILED with numbers and a recommendation
- [ ] Open questions file is empty, or every entry has a recorded decision
- [ ] Full pre-existing test suite green — no regressions across the other 239 test files

> **The last line of defence:** if a reviewer cannot reproduce a claimed number by running the
> command pasted in its ledger, that requirement is not complete — regardless of how much code
> exists, how well it is written, or how many tests accompany it.
