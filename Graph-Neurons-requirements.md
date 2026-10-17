# Graph Neurons — Neural Intelligence Requirements for EOIP / KnowGridFlow

> **Document ID**: GN-REQ-v1
> **Date**: 2026-10-16
> **Status**: Ready for implementation
> **Revision**: GN-REQ-v1.1 (2026-10-17) — tracker check IDs added to every done-when line (`GN-<id>.Dnn`), §12 tracker integration added; no requirement, threshold or path changed
> **Companion**: `Graph-Neurons-implementation-plan.md` (sequencing, gates, evidence protocol)
> **Audience**: AI coding agents and the human reviewers who sign off their work
> **Scope**: CNN, RNN, GNN, Transformer, GAN and SNN architectures operating within, across and
> above instance graphs, knowledge graphs, meta-graphs, the enterprise ontology and the living brain.

---

## 0. READ THIS FIRST — Rules That Override Everything Below

### 0.1 A file is not a feature

**The existence of a source file, a class, a function, or a test file is NOT evidence of completion.**
This rule exists because the repository already contains a counter-example that must be fixed by this
work (see §0.3). Any requirement is complete only when it satisfies **all seven verification levels**
in §2, and the agent has produced the **Evidence Ledger** entry defined in the implementation plan.

An agent that reports "implemented `rgcn.py` with tests in `test_rgcn.py`" has reported **nothing**.
The required report format is the Evidence Ledger: executed commands, captured stdout, measured
numbers against named thresholds.

### 0.2 No assumptions — resolve, don't guess

If any instruction in this document is ambiguous, under-specified, or conflicts with the repository's
actual state, the agent **must stop and record a blocking question** in
`EOIP-engg-doc-pkg/graph-neurons-open-questions.md` rather than inventing a behaviour. Guessing is a
defect. Every requirement below names exact file paths, exact class names, exact method signatures,
exact dependency versions, exact numeric thresholds, and exact verification commands precisely so
that guessing is never necessary.

### 0.3 The anti-pattern this work exists to eliminate

`packages/eoip/gnn/engine.py` (300 lines) presents itself as a graph neural network engine. It is not.

```python
def _deterministic_vector(seed_str: str, dimensions: int) -> list[float]:
    for i in range(dimensions):
        h = hashlib.sha256(f"{seed_str}:{i}".encode()).hexdigest()
        val = (int(h[:8], 16) / 0xFFFFFFFF) * 2.0 - 1.0
```

- `embed_node2vec()` performs deterministic (non-random) walks, concatenates the walk into a string,
  and SHA-256-hashes it. There is no skip-gram objective, no negative sampling, no optimiser.
- `embed_transe()` SHA-256-hashes the entity name, then applies one hardcoded `* 0.1` pass. TransE
  requires margin-ranking loss over corrupted triples. There is no loss, no gradient, no training.
- `NodeClassifier` and `LinkPredictor` consume these hashes.

**Consequence:** two nodes with identical structural roles receive uncorrelated vectors; cosine
similarity between them is noise. Every downstream "prediction" is a hash collision dressed as
inference.

**This is not a criticism of the author — it is a well-formed placeholder.** But it must be
**deleted, not extended**, by `GN-101`. And critically: it is the reference example of work that
passes a naive test suite and fails reality. Requirement `GN-003` exists to make that class of
failure impossible to ship again.

### 0.4 Predictions are never facts

**The enterprise ontology and the verified knowledge graph remain the sole authoritative record of
fact.** Neural output is always an *assertion with a status*, never a silent graph mutation. A neural
module that writes `OBSERVED` edges is a P0 defect regardless of its accuracy. See `GN-002`.

### 0.5 Current baseline — measured, not assumed

| Fact | Value | Verified by |
|---|---|---|
| Python | 3.11.9 | `python --version` |
| Core dependencies | 9 packages: fastapi, uvicorn, pydantic, httpx, PyYAML, jsonschema, prometheus-client, mcp, tree-sitter | `pyproject.toml` |
| numpy / scipy / sklearn | **absent** | import check |
| torch / torch_geometric / dgl | **absent** | import check |
| networkx | **absent** | import check |
| Licence | `LicenseRef-EOIP-Proprietary` | `pyproject.toml` |
| Optional-extras convention | `reports`, `fileparse`, `codeparse`, `otel`, `k8s`, `redis`, `enterprise` | `pyproject.toml` |
| Graph store | `MemoryGraphStore` (`packages/eoip/graph/memory.py:26`) + HugeGraph / Neptune / Neo4j adapters | `packages/eoip/graph/backends.py` |
| Existing test suite | 302 `test_*.py` files — must stay green | `find tests -name "test_*.py"` |
| Engine pattern | double-checked-locking singleton + `get_<name>_engine()` | `packages/eoip/gnn/engine.py:257-300` |
| Existing packages to extend | `gnn/`, `embeddings/`, `mlops/`, `xai/`, `nlp/`, `extraction/`, `causal/`, `graph_graph/`, `reasoning/` | directory listing |

> **Re-count before use (XP-16).** The implementation plan quotes both 302 and 239 for the pre-existing suite. Neither is assumed: count
> `find tests -name "test_*.py"` at the Phase 0a baseline, record the number and the SHA-256 of the sorted file list in the
> `GN-010` ledger, and use that recorded number in every later gate.

---

## 1. Architecture — What Is Being Built

### 1.1 The four graph levels (EOIP canonical naming)

All requirements below reference these levels by their short code. This reconciles the four-level
product hierarchy with the five-level intelligence hierarchy from the research input.

| Code | Level | Contains | Intelligence role |
|---|---|---|---|
| **GL0** | Instance Graph | Concrete typed entities and relationships per tenant | Within-graph learning |
| **GL1** | Meta-Graph | Entity types as nodes, relation types as edges; metapaths | Schema-level learning |
| **GL2** | Living Brain | Unified cross-source, cross-domain heterogeneous graph | Cross-graph learning |
| **GL3** | Enterprise Ontology | Formal classes, axioms, constraints (OWL/SHACL semantics) | Constraint + validation |
| **GLT** | Temporal axis | Bitemporal event history crossing GL0–GL3 | Cuts across all four |

> `GLT` is deliberately an axis, not a fifth level. Temporal behaviour is a property of each level,
> not a separate store. Implementations that create a parallel "temporal graph" duplicating GL0 are
> rejected.

### 1.2 Module topology (target state)

```
packages/eoip/neural/                    # NEW — the neural fabric root
├── __init__.py
├── numerics.py             GN-011  array backend, dtype policy, stable ops   [tier N0]
│                           GN-012  seeding & determinism
│                           GN-015  numerical stability guards
├── runtime.py              GN-001  backend detection, device, degradation contract
│                           GN-013  BLAS thread governance
│                           GN-016  memory estimation & tensor lifecycle
├── contracts.py            GN-002  Assertion status, PredictedEdge, ModelLineage
├── antistub.py             GN-003  learning-proof harness (importable by tests)
├── featurestore.py         GN-004  versioned node/edge feature + embedding store
├── datasets.py             GN-005  snapshot extraction, temporal splits, negative sampling
├── evaluation.py           GN-006  metric suite + mandatory baselines
├── registry.py             GN-007  model registry, promotion gates, rollback
├── encoders/
│   ├── rgcn.py             GN-101  R-GCN
│   ├── graphsage.py        GN-102  GraphSAGE (inductive)
│   ├── rgat.py             GN-103  Relational GAT
│   └── hgt.py              GN-104  Heterogeneous Graph Transformer
├── temporal/
│   ├── sequence.py         GN-301  GRU/LSTM event encoder
│   ├── tgn.py              GN-302  Temporal Graph Network
│   └── renet.py            GN-303  RE-Net recurrent event model
├── conv/
│   ├── chebnet.py          GN-401  Spectral ChebNet filters
│   ├── conve.py            GN-402  ConvE KG completion
│   └── vision.py           GN-403  diagram/image encoder bridge
├── transformer/
│   ├── graph_transformer.py GN-201 GraphGPS-style local+global
│   ├── knowformer.py       GN-202  path-aware KG attention
│   └── nl_bridge.py        GN-203  NL → subgraph → grounded answer
├── generative/
│   ├── discriminator.py    GN-501  KBGAN-style quality gate  (ships before generator)
│   └── generator.py        GN-502  candidate triple generation (gated)
├── spiking/
│   └── spike_encoder.py    GN-601  SpikE/SR-GCN research module (sandboxed)
├── explain/
│   └── explainer.py        GN-701  GNNExplainer-style evidence subgraphs
├── fusion.py               GN-702  multi-module arbitration + confidence
├── security.py             GN-703  entitlement filtering before featurisation
└── router.py               GN-704  FastAPI routes

packages/eoip/gnn/engine.py              # GN-101 DELETES the hash stubs, re-exports neural/
```

### 1.3 Dependency strategy — binding decision

The repository currently has **no numerical stack of any kind**: no numpy, scipy, sklearn, torch or
networkx. That is not an oversight to work around — it is the starting condition this programme must
change deliberately, in tiers.

**Decision: the numerical stack is introduced as FOUR separately-installable tiers, not one
monolithic extra.** The core platform's nine pure-Python dependencies remain untouched.

Rationale for tiering rather than a single `neural` extra: numpy + scipy + sklearn together are
~70 MB, pure CPU, no platform matrix, and are sufficient for the entire Phase 0 foundation
(feature store, metrics, calibration, baselines, anti-stub harness). PyTorch is ~2 GB with a
CUDA/ROCm/CPU wheel matrix. Forcing the 2 GB install on a user who only wants the evaluation harness
is a design error. Splitting them means **Phase 0 installs everywhere, including edge and CI**.

| Tier | Extra name | Size | Unlocks | Needed from |
|---|---|---:|---|---|
| **N0** | `numerics` | ~70 MB | Feature store, vector ops, metrics, calibration, baselines, anti-stub harness, ChebNet eigendecomposition | **Phase 0** |
| **N1** | `neural` | ~2 GB | All trained models: GNN, Transformer, RNN, CNN, GAN | Phase 1 |
| **N2** | `neural-text` | ~1 GB | NL bridge, text embeddings, entity extraction | Phase 2 |
| **N3** | `neural-research` | ~50 MB | SNN sandbox only | Phase 7 |

`[project.optional-dependencies]` additions to `pyproject.toml`:

```toml
numerics = [
  "numpy>=1.26,<3.0",
  "scipy>=1.13,<2.0",
  "scikit-learn>=1.5,<2.0",
]
neural = [
  "eoip[numerics]",
  "torch>=2.4,<3.0",
  "torch-geometric>=2.6,<3.0",
]
neural-text = [
  "eoip[neural]",
  "transformers>=4.44,<5.0",
  "sentence-transformers>=3.0,<4.0",
]
neural-research = [
  "eoip[neural]",
  "snntorch>=0.9,<1.0",
]
```

> Tiers compose via self-referential extras (`eoip[numerics]`), so `pip install "eoip[neural]"`
> transitively installs N0. Do not duplicate the N0 pins inside N1 — a single source of truth for
> each version constraint.

**Licence check — all permissive, all compatible with `LicenseRef-EOIP-Proprietary`:**

| Package | Tier | Licence | Verdict |
|---|---|---|---|
| numpy | N0 | BSD-3-Clause | ✅ safe |
| scipy | N0 | BSD-3-Clause | ✅ safe |
| scikit-learn | N0 | BSD-3-Clause | ✅ safe |
| torch | N1 | BSD-3-Clause | ✅ safe |
| torch-geometric | N1 | MIT | ✅ safe |
| transformers | N2 | Apache-2.0 | ✅ safe |
| sentence-transformers | N2 | Apache-2.0 | ✅ safe |
| snntorch | N3 | MIT | ✅ safe |
| **DGL** | — | Apache-2.0 | ⚠️ permitted but **do not add** — PyG alone is sufficient; two graph frameworks is maintenance waste |
| **networkx** | — | BSD-3-Clause | ⚠️ permitted but **prefer not to add** — baselines in `GN-006` are a few dozen lines of numpy; a whole graph library for Adamic-Adar is unjustified |

Any dependency not in this table requires a Legal check before use. The repository carries a
standing GPL/AGPL prohibition — see `ontology-competitive-analysis.md` §8.1.

> **Transitive licence risk is real here.** `torch` pulls `nvidia-*` CUDA packages under the NVIDIA
> Software Licence Agreement, which is **not** a standard OSS licence and restricts redistribution.
> If EOIP is ever shipped as a bundled appliance rather than pip-installed by the customer, Legal
> must review CUDA redistribution terms. `GN-010` requires the CPU-only wheel index as the default
> for exactly this reason.

---

## 2. The Seven Verification Levels

Every requirement declares which levels apply. **V1 alone is never sufficient for any requirement.**

| Level | Name | What it proves | How it is evidenced |
|---|---|---|---|
| **V1** | Artifact | The code exists | File path + line count. **Never sufficient alone.** |
| **V2** | Executable | It runs without error | Command + exit code 0 + captured stdout |
| **V3** | Behavioural | It is correct on a known fixture | Assertion on a hand-verified expected output |
| **V4** | Statistical | It beats the mandated baselines | Metric ≥ threshold on a held-out split, with the baseline number printed beside it |
| **V5** | Anti-stub | It actually learned | §2.1 — all four probes pass |
| **V6** | Integration | It is reachable in the running platform | Visible in `/brain/telemetry`, present in OpenAPI, end-to-end request succeeds |
| **V7** | Operational | It is affordable | Latency p95, peak RSS, and graceful degradation when `neural` extra is absent |

### 2.1 V5 — the Anti-Stub Probes (`GN-003`)

These four probes exist specifically to catch the `_deterministic_vector` failure class. Any learned
module must pass all four. They are implemented once in `packages/eoip/neural/antistub.py` and
imported by every model's test module.

| Probe | Method | Pass condition | What a hash stub does |
|---|---|---|---|
| **P1 Loss descent** | Record training loss per epoch | Final loss ≤ 70% of epoch-0 loss, monotonic over a 5-epoch window | **FAILS** — no loss exists |
| **P2 Weight delta** | Snapshot `state_dict()` before and after training; L2 norm of the difference | Δ > 1e-6 for ≥ 90% of parameter tensors | **FAILS** — no parameters |
| **P3 Label permutation control** | Retrain on randomly permuted labels | Permuted-label score must be **worse** than true-label score by ≥ 0.10 absolute on the primary metric | **FAILS** — hash output is label-independent, so both scores are identical |
| **P4 Structural coherence** | Build a fixture with two nodes of provably identical structural role | Cosine similarity of their embeddings ≥ 0.90 | **FAILS** — SHA-256 of different IDs is uncorrelated |

> **P3 is the single most important gate in this document.** A model that scores identically on true
> and permuted labels has learned nothing, no matter how good its headline metric looks. Any
> requirement whose P3 gap is < 0.10 is **not complete** and must be reported as failing.

### 2.2 Mandatory baselines (`GN-006`)

No neural model may be declared complete without being measured against **all** of these on the same
split. The baseline numbers must appear in the Evidence Ledger next to the model's number.

| Baseline | Implementation | Purpose |
|---|---|---|
| `RandomBaseline` | Uniform random scores | Absolute floor |
| `DegreeBaseline` | Score by target node degree (popularity) | Catches "the model just learned popularity" |
| `CommonNeighborsBaseline` | Adamic-Adar / Jaccard on shared neighbours | Classic strong link-prediction baseline |
| `HashBaseline` | **The existing `_deterministic_vector`**, preserved in the test suite only | Proves the new model beats the thing it replaced |
| `RuleBaseline` | Existing deterministic graph traversal for the task | Proves neural adds value over what EOIP already ships |

**A neural model that does not beat `CommonNeighborsBaseline` and `RuleBaseline` is a failed
experiment and must be reported as such, not shipped.** Reporting a failed experiment honestly is a
successful completion of the requirement; shipping an unmeasured model is not.

---

## 3. Foundation Requirements (GN-010 … GN-016, then GN-001 … GN-007) — P0, Blocking

Nothing in §4–§9 may begin until §3 is complete and verified. These are not scaffolding; they are
the substrate and contracts everything else depends on.

> **Build order within this section is GN-010 → GN-016, then GN-001 → GN-007.** The IDs are
> non-sequential with respect to build order because GN-001…007 were specified first; the numerical
> substrate was identified afterwards and must be laid first. Follow the stated order, not the
> numeric order.

---

## 3.1 Numerical Stack (GN-010 … GN-016) — build these first

These requirements exist because the repository has **zero** numerical infrastructure today. Every
one of them addresses a failure that is invisible in development and expensive in production.

---

### GN-010 — Numerical Stack Provisioning & Platform Matrix

**Priority** P0 · **Blocks** everything · **Path** `pyproject.toml`, `docs/install-neural.md`

**Build** the four-tier extras from §1.3, plus a reproducible, platform-aware install procedure.

**Binding constraints:**

1. **CPU wheels are the default.** `pip install "eoip[neural]"` must resolve to CPU-only torch. GPU
   is opt-in via an explicit index URL, because the CUDA wheels carry NVIDIA SLA terms (§1.3) and
   are ~5× larger. Document both:

   ```bash
   # CPU (default, all platforms)
   pip install "eoip[neural]" --extra-index-url https://download.pytorch.org/whl/cpu
   # CUDA 12.4 (opt-in, Linux/Windows x86_64 only)
   pip install "eoip[neural]" --extra-index-url https://download.pytorch.org/whl/cu124
   ```

2. **A hash-pinned lockfile is mandatory** at `requirements-neural.lock`, generated with
   `pip-compile --generate-hashes`. Unpinned transitive dependencies in a 2 GB tree are a supply-chain
   risk and a reproducibility hole.
3. The platform support matrix must be **tested, not asserted**:

   | Platform | Python | Tier N0 | Tier N1 CPU | Tier N1 CUDA |
   |---|---|---|---|---|
   | Linux x86_64 | 3.11, 3.12 | required | required | required |
   | Windows x86_64 | 3.11, 3.12 | required | required | best-effort |
   | macOS arm64 | 3.11, 3.12 | required | required | n/a (MPS instead) |
   | Linux arm64 | 3.11 | required | best-effort | n/a |

4. `pip install -e .` (no extras) must remain **unchanged in resolved-package count**. Adding numpy
   to core is forbidden.

**Done when:**
- [ ] `GN-010.D01` V2: All four extras install cleanly on Linux x86_64 / Python 3.11 — four commands, four exit-0s
- [ ] `GN-010.D02` V3: `pip install -e .` resolves to exactly the same package set as before this change — proven by diffing `pip freeze` before and after
- [ ] `GN-010.D03` V3: `requirements-neural.lock` exists with `--generate-hashes`; install from it succeeds offline from a local wheel cache
- [ ] `GN-010.D04` V3: CPU default verified — `python -c "import torch; print(torch.version.cuda)"` prints `None` after a default install
- [ ] `GN-010.D05` V4: Platform matrix exercised in CI for at least Linux x86_64 and Windows x86_64 on Python 3.11 and 3.12 — four jobs, all green
- [ ] `GN-010.D06` V7: Install size recorded per tier; N0 ≤ 150 MB, N1 CPU ≤ 2.5 GB

---

### GN-011 — Array Backend & Dtype Discipline

**Priority** P0 · **Path** `packages/eoip/neural/numerics.py`

Today every vector in the codebase is a `list[float]` and every operation is a Python loop
(`_cosine_similarity` in `gnn/engine.py` is the canonical example). That is 50–200× slower than
numpy and will not survive the `GN-705` latency budgets.

**Build:**

```python
import numpy as np
from numpy.typing import NDArray

Vector = NDArray[np.float32]      # the canonical in-memory representation
Matrix = NDArray[np.float32]

DEFAULT_DTYPE = np.float32        # binding — see constraint 1

def to_array(values: Sequence[float]) -> Vector: ...
def to_list(arr: Vector) -> list[float]: ...        # only at serialization boundaries
def cosine_similarity(a: Vector, b: Vector) -> float: ...
def cosine_matrix(q: Vector, m: Matrix) -> Vector: ...   # vectorized, no Python loop
def l2_normalize(m: Matrix, axis: int = -1) -> Matrix: ...
def assert_finite(arr: Vector, context: str) -> None: ...  # raises on NaN/Inf
```

**Binding constraints:**

1. **float32 everywhere in storage and inference.** float64 doubles memory for no accuracy benefit
   in embeddings. float64 is permitted only inside metric computation where catastrophic
   cancellation is a real risk (`GN-015`). Enforce with a dtype assertion in `FeatureStore.put`.
2. **No Python-level loops over arrays in any hot path.** A loop over `range(dimensions)` performing
   float arithmetic is a defect. Hot paths: similarity, normalization, aggregation, batching.
3. `list[float]` appears **only** at JSON serialization boundaries. Internally, arrays.
4. Every array crossing a module boundary passes `assert_finite()`. NaN propagates silently and
   surfaces three layers away as a meaningless prediction.

**Done when:**
- [ ] `GN-011.D01` V3: `cosine_matrix` against a 100k × 128 matrix returns in < 20 ms — compare with the existing Python-loop implementation and record the speedup factor
- [ ] `GN-011.D02` V3: Passing a float64 array to `FeatureStore.put` raises
- [ ] `GN-011.D03` V3: `assert_finite` raises on an array containing NaN, and on one containing +Inf
- [ ] `GN-011.D04` V3: Round-trip `to_array(to_list(x)) == x` exactly for float32 — no precision drift
- [ ] `GN-011.D05` V2: `grep -rn "for i in range(dim" packages/eoip/neural/` returns zero hits

---

### GN-012 — Determinism & Reproducibility

**Priority** P0 · **Path** `packages/eoip/neural/numerics.py` (seeding), all training entry points

Without this, no metric in any Evidence Ledger is reproducible, and the entire verification regime
in §2 is unverifiable.

**Build:**

```python
@dataclass(frozen=True)
class SeedBundle:
    python_seed: int
    numpy_seed: int
    torch_seed: int
    cuda_seed: int | None

def seed_everything(seed: int = 42, deterministic: bool = True) -> SeedBundle: ...
def capture_environment() -> dict[str, Any]: ...   # versions, BLAS, device, seeds
```

**Binding constraints:**

1. `seed_everything()` seeds `random`, `numpy.random`, `torch`, and CUDA, and when
   `deterministic=True` sets `torch.use_deterministic_algorithms(True)` and
   `CUBLAS_WORKSPACE_CONFIG=:4096:8`.
2. Every training run records its `SeedBundle` **and** `capture_environment()` into the model
   registry (`GN-007`) and the Evidence Ledger.
3. **Two runs with the same seed, snapshot and environment must produce metrics within 1e-4.** This
   is a tested requirement, not an aspiration.
4. Where full determinism is impossible (some CUDA kernels have no deterministic implementation),
   the run must **record which operations fell back to non-deterministic** rather than silently
   proceeding.

**Done when:**
- [ ] `GN-012.D01` V3: Same seed, two runs, same process → identical metrics to 1e-6
- [ ] `GN-012.D02` V3: Same seed, two runs, **separate processes** → metrics within 1e-4
- [ ] `GN-012.D03` V3: Different seed → metrics differ (proving the seed is actually wired, not ignored)
- [ ] `GN-012.D04` V3: `capture_environment()` records numpy/torch/BLAS versions, device, and thread counts
- [ ] `GN-012.D05` V6: Seed and environment appear in the model registry entry for every trained model

---

### GN-013 — BLAS Thread Governance

**Priority** P0 · **Path** `packages/eoip/neural/runtime.py`

This is the production failure nobody anticipates. numpy's BLAS (OpenBLAS/MKL) spawns one thread per
core **by default**. Under uvicorn with N workers, you get N × cores threads fighting for the same
cores. Throughput collapses and latency becomes wildly erratic — and it looks like a mysterious
performance bug, not a configuration error.

**Binding constraints:**

1. Thread limits must be set **before numpy is first imported** — setting them afterwards has no
   effect. This forces the configuration into process startup, not lazy initialization.
2. Defaults:
   - API-serving process: `OMP_NUM_THREADS=1`, `torch.set_num_threads(1)`. Concurrency comes from
     uvicorn workers, not BLAS threads.
   - Training/batch process: `OMP_NUM_THREADS=min(8, cpu_count)`.
3. All four must be set together: `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`,
   `NUMEXPR_NUM_THREADS`. Setting only `OMP_NUM_THREADS` is a common and ineffective half-fix.
4. The effective thread count is reported in `RuntimeCapabilities` and `/neural/runtime`.

**Done when:**
- [ ] `GN-013.D01` V3: In a serving process, `torch.get_num_threads() == 1` and all four env vars are `"1"`
- [ ] `GN-013.D02` V3: In a training process, threads = `min(8, cpu_count)`
- [ ] `GN-013.D03` V4: **Oversubscription probe** — run 4 concurrent inference requests with thread limits set vs unset; record p95 latency for both. The limited configuration must be faster. *If it is not, record the measurement and revisit the defaults*
- [ ] `GN-013.D04` V6: Thread counts visible in `GET /neural/runtime`
- [ ] `GN-013.D05` V3: A test asserts the env vars are set before `import numpy` — by checking `sys.modules` ordering at configuration time

---

### GN-014 — Air-Gapped & Offline Installation

**Priority** P1 · **Path** `docs/install-neural-airgap.md`, `scripts/build_wheel_bundle.sh`

EOIP targets air-gapped enterprise deployments. A 2 GB dependency tree that assumes PyPI reachability
breaks that promise silently.

**Done when:**
- [ ] `GN-014.D01` V2: `scripts/build_wheel_bundle.sh` produces a self-contained wheel bundle for a named platform/tier
- [ ] `GN-014.D02` V3: On a network-isolated machine (or a container with networking disabled), `pip install --no-index --find-links=./wheels "eoip[neural]"` succeeds
- [ ] `GN-014.D03` V3: Bundle manifest lists every wheel with its SHA-256, matching `requirements-neural.lock`
- [ ] `GN-014.D04` V7: Bundle size recorded per tier and platform
- [ ] `GN-014.D05` V3: Documented procedure for pre-downloading any model weights (tier N2), so first run does not silently attempt a network fetch

---

### GN-015 — Numerical Correctness & Stability

**Priority** P0 · **Path** `packages/eoip/neural/numerics.py`, `tests/neural/test_numerics.py`

Silent numerical bugs are the hardest class to detect because the output remains plausible.

**Binding constraints:**

| Hazard | Required mitigation |
|---|---|
| Softmax overflow | Subtract row max before `exp` — never raw `exp(x)` |
| Log of zero | `log(x + eps)` with `eps = 1e-12`, or `log1p` |
| Division by zero norm | Guard every normalization: `norm or 1.0` |
| Catastrophic cancellation in metrics | Compute AUPRC/ECE accumulations in float64 even though storage is float32 |
| NaN propagation | `assert_finite()` at every module boundary (`GN-011`) |
| Integer overflow in edge indexing | int64 for node indices; assert `num_nodes < 2**31` or use int64 explicitly |
| Empty-input edge cases | Every reduction handles the zero-row case explicitly, returning a documented value — never a silent NaN |

**Done when:**
- [ ] `GN-015.D01` V3: Softmax over `[1000.0, 1001.0]` returns a finite, correct result — the naive implementation overflows here
- [ ] `GN-015.D02` V3: Cosine similarity with a zero vector returns a documented value, not NaN
- [ ] `GN-015.D03` V3: AUPRC on a 1M-row fixture matches a float64 reference to 1e-9
- [ ] `GN-015.D04` V3: Every reduction given an empty array returns its documented value — one test per reduction
- [ ] `GN-015.D05` V3: A fixture graph with 0 edges, 1 node, and 1 self-loop each run through the full pipeline without raising

---

### GN-016 — Memory & Tensor Lifecycle

**Priority** P1 · **Path** `packages/eoip/neural/runtime.py`

**Binding constraints:**

1. Before any training or full-graph inference, estimate peak memory and compare against available.
   If the estimate exceeds 80% of available, **refuse with a clear message naming the required
   batch size** — do not start and OOM twenty minutes later.
2. GPU memory is explicitly released after each job (`torch.cuda.empty_cache()` plus dropping
   references). A long-lived serving process that leaks GPU memory across requests dies at 3 a.m.
3. Batch sizing is **derived from `RuntimeCapabilities.max_nodes_in_memory`**, never hardcoded.
4. Peak RSS and peak GPU memory are recorded in every Evidence Ledger `V7` section.

**Done when:**
- [ ] `GN-016.D01` V3: A deliberately oversized job is refused **before** allocation, with a message naming a workable batch size
- [ ] `GN-016.D02` V3: GPU memory returns to baseline ± 50 MB after 10 sequential inference jobs — proven by sampling `torch.cuda.memory_allocated()`
- [ ] `GN-016.D03` V7: Peak RSS recorded for training and inference at 10k / 100k nodes
- [ ] `GN-016.D04` V3: On a CPU-only machine, all memory guards still function (no CUDA-only code path)

---

## 3.2 Contracts & Harness (GN-001 … GN-007)

---

### GN-001 — Neural Runtime & Degradation Contract

**Priority** P0 · **Blocks** everything · **Path** `packages/eoip/neural/runtime.py`

**Build:**

```python
class NeuralTier(str, Enum):
    NONE      = "none"       # no numerical stack — core EOIP only
    NUMERICS  = "numerics"   # N0: numpy/scipy/sklearn — metrics, baselines, feature store
    NEURAL    = "neural"     # N1: + torch/PyG — trained models
    TEXT      = "text"       # N2: + transformers
    RESEARCH  = "research"   # N3: + snntorch

class NeuralBackend(str, Enum):
    TORCH_CUDA  = "torch_cuda"
    TORCH_MPS   = "torch_mps"
    TORCH_CPU   = "torch_cpu"
    NUMPY_ONLY  = "numpy_only"    # N0 present, N1 absent — valid state, not an error
    UNAVAILABLE = "unavailable"

@dataclass(frozen=True)
class RuntimeCapabilities:
    tier: NeuralTier
    backend: NeuralBackend
    numpy_version: str | None
    torch_version: str | None
    pyg_version: str | None
    device: str                  # "cuda:0" | "mps" | "cpu" | "none"
    blas_threads: int            # effective count after GN-013
    max_nodes_in_memory: int     # computed from available RAM, see below
    reason: str | None           # populated when a requested tier is unmet

class NeuralUnavailableError(RuntimeError):
    """Raised when an operation needs a tier that is not installed.
    Message must name the missing tier AND the exact install command."""

def get_runtime() -> RuntimeCapabilities: ...        # cached, thread-safe singleton
def require_tier(tier: NeuralTier) -> RuntimeCapabilities: ...  # raises if unmet
def require_neural() -> RuntimeCapabilities: ...     # sugar for require_tier(NEURAL)
```

**Degradation contract — binding behaviour:**

1. `get_runtime()` detects the **highest satisfied tier** and never raises. With nothing installed
   it returns `tier=NONE, backend=UNAVAILABLE` and a `reason` naming the missing package plus the
   exact remediation command.
2. **Every endpoint declares a minimum tier.** When unmet it returns **HTTP 503** naming the missing
   tier and its install command. It must **never** return a plausible-looking fabricated result.
   Endpoints requiring only N0 (metrics, baselines, embedding lookup) must keep working when torch
   is absent — a blanket 503 for the whole neural surface is wrong.
3. **Silent fallback to a non-learned heuristic is explicitly forbidden.** This is the rule that
   prevents the §0.3 anti-pattern from recurring. If a caller wants deterministic traversal, it must
   ask for deterministic traversal explicitly.
4. The rest of EOIP must import and start normally with `neural` absent. No module under
   `packages/eoip/neural/` may be imported at EOIP startup except `runtime.py` and `contracts.py`,
   both of which must be import-safe without torch.
5. `max_nodes_in_memory` = `floor(available_bytes * 0.4 / (feature_dim * 4 * 3))`, minimum 10_000.

**Done when:**
- [ ] `GN-001.D01` V2: `python -c "from eoip.neural.runtime import get_runtime; print(get_runtime())"` prints a populated dataclass
- [ ] `GN-001.D02` V3: **Four-venv tier matrix** — in venvs with (a) nothing, (b) N0 only, (c) N0+N1, (d) N0+N1+N2, `get_runtime().tier` returns `NONE`, `NUMERICS`, `NEURAL`, `TEXT` respectively, and **never raises** in any of them
- [ ] `GN-001.D03` V3: In venv (a), `python -c "import eoip.platform_router"` succeeds — proving core EOIP is unaffected
- [ ] `GN-001.D04` V3: In venv (b), an N0-only endpoint (e.g. `GET /neural/embeddings/{id}`) returns 200; an N1 endpoint returns 503 naming tier `neural`
- [ ] `GN-001.D05` V3: `require_tier(NEURAL)` in venv (b) raises with both the missing tier name and the install command in `str(exc)`
- [ ] `GN-001.D06` V6: `GET /neural/runtime` returns capabilities including `tier`, `blas_threads`, `device`
- [ ] `GN-001.D07` V7: `get_runtime()` second call is < 1 ms (caching proven by timing two calls)

---

### GN-002 — Assertion Contract: Separating Prediction From Fact

**Priority** P0 · **Path** `packages/eoip/neural/contracts.py`

This requirement enforces §0.4 structurally, so that violating it is a type error rather than a
code-review opinion.

**Build:**

```python
class AssertionStatus(str, Enum):
    OBSERVED  = "OBSERVED"    # sourced from a system of record — only connectors may write this
    DERIVED   = "DERIVED"     # produced by a deterministic rule or reasoner
    PREDICTED = "PREDICTED"   # produced by a neural model — NEVER authoritative
    REJECTED  = "REJECTED"    # a prediction a human or validator refused
    CONFIRMED = "CONFIRMED"   # a PREDICTED edge a human promoted; retains full lineage

@dataclass(frozen=True)
class ModelLineage:
    model_id: str            # registry id, e.g. "rgcn-linkpred"
    model_version: str       # semver from GN-007
    trained_at: str          # ISO-8601 UTC
    graph_snapshot_id: str   # the exact snapshot trained on — from GN-005
    code_commit: str         # git SHA at training time

@dataclass(frozen=True)
class PredictedEdge:
    source_id: str
    target_id: str
    relation: str
    score: float                      # raw model output
    calibrated_probability: float     # post-calibration, [0,1] — see GN-006
    lineage: ModelLineage
    evidence_paths: list[list[str]]   # node-id paths supporting the claim — from GN-701
    ontology_valid: bool | None       # None until GL3 validation has run
    status: AssertionStatus = AssertionStatus.PREDICTED
```

**Binding constraints:**

1. `PredictedEdge.status` **may not** be constructed as `OBSERVED` or `DERIVED`. Enforce in
   `__post_init__`; raise `ValueError`.
2. The graph write path must reject any neural-origin write carrying `OBSERVED`. Add the guard in
   the store adapter, not only in the caller.
3. A `PREDICTED` edge **may never overwrite or delete** an `OBSERVED` edge between the same
   `(source, relation, target)`. It is stored alongside it.
4. Promotion `PREDICTED → CONFIRMED` requires an explicit human actor id and writes an audit record.
   No code path may perform this automatically.
5. Every `PredictedEdge` must carry a non-empty `evidence_paths` **or** `ontology_valid is not None`.
   A prediction with neither is unexplainable and must be refused at construction.

**Done when:**
- [ ] `GN-002.D01` V3: `PredictedEdge(..., status=AssertionStatus.OBSERVED)` raises `ValueError`
- [ ] `GN-002.D02` V3: Attempting to write a neural `OBSERVED` edge through the store adapter raises, proven by test
- [ ] `GN-002.D03` V3: Writing a `PREDICTED` edge where an `OBSERVED` one exists leaves the `OBSERVED` edge byte-identical — asserted by reading it back and comparing
- [ ] `GN-002.D04` V3: `promote()` without an actor id raises; with one, an audit record is retrievable
- [ ] `GN-002.D05` V6: `GET /neural/predictions?status=PREDICTED` returns only predicted edges, never observed facts
- [ ] `GN-002.D06` V6: A full round trip — predict → store → query graph for `OBSERVED` only → prediction absent from results

---

### GN-003 — Anti-Stub Harness

**Priority** P0 · **Path** `packages/eoip/neural/antistub.py`

Implements the four probes in §2.1 as a reusable harness.

```python
@dataclass
class AntiStubReport:
    loss_descent: bool;        loss_initial: float; loss_final: float
    weight_delta: bool;        tensors_changed: int; tensors_total: int
    permutation_control: bool; true_score: float; permuted_score: float; gap: float
    structural_coherence: bool; coherence_similarity: float
    @property
    def passed(self) -> bool: ...   # all four True

def run_antistub(
    train_fn: Callable[[Any], list[float]],   # returns per-epoch losses
    model: Any,
    eval_fn: Callable[[Any], float],
    permuted_train_fn: Callable[[Any], None],
    coherence_fixture: tuple[str, str],
) -> AntiStubReport: ...
```

**Done when:**
- [ ] `GN-003.D01` V3: Running the harness against the **existing** `GraphEmbedder._deterministic_vector` produces `passed == False` with **all four** probes False. *This is the harness's own correctness proof — if the harness passes the hash stub, the harness is broken.*
- [ ] `GN-003.D02` V3: Running it against a trivially-trained 2-layer MLP on a separable fixture produces `passed == True`
- [ ] `GN-003.D03` V2: `AntiStubReport` serialises to JSON for the Evidence Ledger

---

### GN-004 — Versioned Feature & Embedding Store

**Priority** P0 · **Path** `packages/eoip/neural/featurestore.py`

**Build:** `FeatureStore` with tenant-scoped, snapshot-versioned storage of node features, edge
features and computed embeddings.

```python
def put_embeddings(tenant_id, snapshot_id, model_id, model_version, vectors: dict[str, list[float]]) -> str
def get_embeddings(tenant_id, snapshot_id, model_id) -> dict[str, list[float]]
def nearest(tenant_id, model_id, vector, k=10, entitlements: EntitlementSet) -> list[tuple[str, float]]
def invalidate(tenant_id, affected_node_ids: set[str]) -> int   # returns count marked stale
```

**Binding constraints:**

1. **Tenant isolation is absolute.** No cross-tenant read is possible through any API. Enforced by
   making `tenant_id` the first path segment of every key, and by a test that attempts a crafted
   cross-tenant read and asserts it returns empty.
2. Every embedding row carries `(snapshot_id, model_id, model_version, computed_at, stale: bool)`.
3. `nearest()` applies entitlement filtering **before** returning results (see `GN-703`) — not after,
   because result counts themselves leak information.
4. Storage backend is pluggable; the default is the existing graph store sidecar. No new database
   may be introduced without an explicit decision record.

**Done when:**
- [ ] `GN-004.D01` V3: Cross-tenant read attempt returns empty — proven with a crafted adversarial key
- [ ] `GN-004.D02` V3: `invalidate()` on a node marks exactly its k-hop neighbourhood stale, count asserted against a hand-computed fixture
- [ ] `GN-004.D03` V4: `nearest()` over 100k vectors returns in p95 < 50 ms
- [ ] `GN-004.D04` V3: An unentitled caller receives **zero** rows, and the *count* of filtered rows is not disclosed
- [ ] `GN-004.D05` V6: Store survives process restart; embeddings reload with identical values (byte-compare)

---

### GN-005 — Snapshots, Temporal Splits & Negative Sampling

**Priority** P0 · **Path** `packages/eoip/neural/datasets.py`

This requirement prevents the single most common silent failure in graph ML: **temporal leakage**.

**Build:**

```python
def create_snapshot(store, tenant_id, as_of: datetime) -> GraphSnapshot    # content-addressed id
def temporal_split(snapshot, train_end, val_end) -> tuple[Split, Split, Split]
def sample_negatives(snapshot, positives, strategy: NegativeStrategy, ratio: int = 1) -> list[Triple]

class NegativeStrategy(str, Enum):
    UNIFORM         = "uniform"          # random corruption
    DEGREE_MATCHED  = "degree_matched"   # corrupt to a node of similar degree
    TYPE_CONSTRAINED= "type_constrained" # respect ontology domain/range — hardest, most realistic
```

**Binding constraints:**

1. `temporal_split` splits **strictly by event time**, never randomly. Every training edge must have
   `valid_from <= train_end`. Assert this, do not assume it.
2. Snapshot ids are **content-addressed** (hash of sorted node+edge ids + as_of), so the same graph
   state always yields the same id and training runs are reproducible.
3. `TYPE_CONSTRAINED` negatives must consult the ontology manifest
   (`packages/eoip/ontology/manifest.py:edge_endpoints_valid`) so that corrupted triples are
   type-plausible. Easy negatives inflate metrics and are the second-most-common silent failure.
4. Default strategy for all reported metrics is `TYPE_CONSTRAINED`. Reporting only `UNIFORM`
   results is non-compliant.

**Done when:**
- [ ] `GN-005.D01` V3: **Leakage probe** — construct a fixture where a test edge exists at `t+1`; assert it is absent from the train split. Then deliberately inject it and assert the split validator *raises*
- [ ] `GN-005.D02` V3: Identical graph state produces an identical `snapshot_id` across two processes
- [ ] `GN-005.D03` V3: `TYPE_CONSTRAINED` negatives all satisfy `edge_endpoints_valid()`; asserted over 1,000 samples
- [ ] `GN-005.D04` V4: Metrics reported under `UNIFORM` vs `TYPE_CONSTRAINED` both recorded; the gap is documented in the Evidence Ledger

---

### GN-006 — Evaluation Harness & Calibration

**Priority** P0 · **Path** `packages/eoip/neural/evaluation.py`

**Build:** metric suite + the five mandatory baselines from §2.2 + probability calibration.

| Task | Primary metric | Secondary |
|---|---|---|
| Link prediction | **AUPRC** | Hits@1/3/10, MRR |
| Node classification | **Macro-F1** | Per-class precision/recall, confusion matrix |
| Anomaly detection | **AUPRC** | Precision@k |
| Temporal prediction | **MRR (time-filtered)** | Hits@10 |

**Binding constraints:**

1. **AUPRC, not AUROC, is primary** for link prediction and anomaly detection. Graph link prediction
   is extremely class-imbalanced; AUROC looks excellent at ~0.95 on data where AUPRC is ~0.05.
   Reporting AUROC as the headline is non-compliant.
2. Every evaluation run emits all five baselines alongside the model.
3. Scores must be calibrated (isotonic regression on the validation split) before becoming
   `PredictedEdge.calibrated_probability`. Report **Expected Calibration Error**; ECE must be ≤ 0.10.
4. Results are written as machine-readable JSON to `artifacts/neural/eval/<model>-<version>.json`.

**Done when:**
- [ ] `GN-006.D01` V3: On a fixture with a known-correct answer set, AUPRC is computed and hand-verified to 4 decimal places
- [ ] `GN-006.D02` V3: All five baselines run and emit numbers on the same split
- [ ] `GN-006.D03` V4: ECE ≤ 0.10 after calibration; the pre- and post-calibration reliability curves are saved
- [ ] `GN-006.D04` V3: AUROC and AUPRC are both printed, and the harness **refuses** to emit a report containing AUROC alone

---

### GN-007 — Model Registry, Promotion Gates & Rollback

**Priority** P0 · **Path** `packages/eoip/neural/registry.py` (extends `packages/eoip/mlops/experiment_tracker.py` — do not duplicate it)

**Promotion gates — a model reaches `production` only when ALL hold:**

| Gate | Threshold |
|---|---|
| Anti-stub | All four probes pass (`GN-003`) |
| Baseline lift | Primary metric ≥ `CommonNeighborsBaseline` + 0.05 **and** ≥ `RuleBaseline` + 0.05 |
| Calibration | ECE ≤ 0.10 |
| Temporal validity | Trained only on data with `valid_from <= train_end`, asserted not assumed |
| Latency | Inference p95 within the budget in `GN-705` |
| Security | Entitlement filter active; cross-tenant probe returns empty |
| Explainability | ≥ 95% of predictions carry non-empty `evidence_paths` |

**Done when:**
- [ ] `GN-007.D01` V3: A model failing **any single** gate cannot be promoted — tested once per gate, seven tests
- [ ] `GN-007.D02` V3: Rollback restores the prior version and serving reflects it within 60 s, proven by a request before and after
- [ ] `GN-007.D03` V6: `GET /neural/models` lists versions, stage and the full gate report for each

---

## 4. Graph Neural Networks (GN-101 … GN-104) — P0, Core

### GN-101 — R-GCN: Replace the Hash Stub

**Priority** P0 · **Path** `packages/eoip/neural/encoders/rgcn.py` · **Levels** GL0, GL2

**Build** a real Relational Graph Convolutional Network (Schlichtkrull et al., 2018) in PyTorch
Geometric. Relation-specific weight matrices with basis decomposition to control parameter count.

```python
class RGCNEncoder(nn.Module):
    def __init__(self, num_nodes: int, num_relations: int, hidden_dim: int = 128,
                 num_layers: int = 2, num_bases: int = 30, dropout: float = 0.2): ...
    def forward(self, x, edge_index, edge_type) -> Tensor: ...

class RGCNLinkPredictor:
    def train_model(self, snapshot, config) -> TrainingResult: ...   # returns per-epoch losses
    def predict(self, source_id, top_k=10) -> list[PredictedEdge]: ...
```

**Mandatory deletions.** This requirement is incomplete while any of these survive:
- `GraphEmbedder._deterministic_vector` — **delete**
- `GraphEmbedder.embed_node2vec` — **delete** (replace with a trained implementation or remove the method)
- `GraphEmbedder.embed_transe` — **delete** (same)
- `packages/eoip/gnn/engine.py` becomes a thin re-export of `eoip.neural.*`, preserving `get_gnn_engine()` so existing callers keep working

> The hash functions are preserved **only** inside `tests/neural/baselines.py` as `HashBaseline`,
> so the Evidence Ledger can show the new model beating what it replaced.

**Config (exact defaults — do not guess):**

| Parameter | Default | Notes |
|---|---|---|
| `hidden_dim` | 128 | |
| `num_layers` | **2** | 3+ triggers oversmoothing on enterprise graphs; see `GN-706` |
| `num_bases` | 30 | basis decomposition; prevents parameter blow-up on many relation types |
| `dropout` | 0.2 | |
| `learning_rate` | 0.01 | Adam |
| `weight_decay` | 5e-4 | |
| `epochs` | 200 | with early stopping, patience 20 on val AUPRC |
| `negative_ratio` | 1 | `TYPE_CONSTRAINED` |

**Done when:**
- [ ] `GN-101.D01` V1: File exists — *acknowledged as insufficient*
- [ ] `GN-101.D02` V2: Training runs end-to-end on the reference snapshot, exit 0, loss curve printed
- [ ] `GN-101.D03` V3: On the hand-built fixture in `tests/neural/fixtures/known_graph.json`, the model recovers 5 deliberately-removed edges in its top-10 predictions
- [ ] `GN-101.D04` V4: Test-split **AUPRC ≥ CommonNeighborsBaseline + 0.05** and **≥ RuleBaseline + 0.05**, with all five baseline numbers printed in the ledger
- [ ] `GN-101.D05` V5: **All four anti-stub probes pass.** P3 permutation gap ≥ 0.10 — this is the gate the current stub fails
- [ ] `GN-101.D06` V6: `POST /neural/predict/links` returns `PredictedEdge` objects with lineage and evidence; `gnn` appears in `GET /brain/telemetry`
- [ ] `GN-101.D07` V6: `get_gnn_engine()` still importable and functional — no caller breakage
- [ ] `GN-101.D08` V7: Inference p95 < 200 ms for top-10 on a 100k-node graph; peak RSS recorded
- [ ] `GN-101.D09` V7: With the `neural` extra absent, the endpoint returns 503 and EOIP starts normally

---

### GN-102 — GraphSAGE (Inductive)

**Priority** P0 · **Path** `packages/eoip/neural/encoders/graphsage.py` · **Levels** GL0, GL2

Inductive embedding so newly-ingested entities get vectors **without retraining** — essential because
connectors add entities continuously.

**Done when:**
- [ ] `GN-102.D01` V3: **Inductive proof** — train on snapshot `S1`; add 100 new nodes forming `S2`; embed them with the `S1`-trained model; assert no retraining occurred (weight hash identical before and after) and the new embeddings are non-degenerate (pairwise cosine variance > 0.01)
- [ ] `GN-102.D02` V4: New-node link-prediction AUPRC within 0.10 of seen-node AUPRC
- [ ] `GN-102.D03` V5: All four probes pass
- [ ] `GN-102.D04` V7: Embedding 1,000 new nodes completes in < 5 s

---

### GN-103 — Relational Graph Attention (R-GAT)

**Priority** P1 · **Path** `packages/eoip/neural/encoders/rgat.py` · **Levels** GL0, GL2

Attention weights are the explainability substrate for `GN-701` — they must be **retrievable per
prediction**, not merely computed internally.

**Done when:**
- [ ] `GN-103.D01` V3: `get_attention_weights(source, target)` returns per-edge weights summing to 1.0 ± 1e-5 per head
- [ ] `GN-103.D02` V3: On a fixture with one deliberately dominant path, that path receives the highest attention — hand-verified
- [ ] `GN-103.D03` V4: AUPRC ≥ R-GCN (`GN-101`) − 0.02. *If R-GAT does not beat R-GCN, record that honestly and keep R-GCN as default*
- [ ] `GN-103.D04` V5: All four probes pass

---

### GN-104 — Heterogeneous Graph Transformer (HGT)

**Priority** P1 · **Path** `packages/eoip/neural/encoders/hgt.py` · **Levels** GL1, GL2

Node-type- and edge-type-specific attention for the meta-graph and cross-domain living brain.

**Done when:**
- [ ] `GN-104.D01` V3: Distinct parameter sets exist per node type and edge type — asserted by inspecting `state_dict()` keys against the manifest's type list
- [ ] `GN-104.D02` V4: On a **multi-domain** fixture spanning ≥ 3 domains, HGT beats homogeneous R-GCN by ≥ 0.03 AUPRC. *If it does not, document that EOIP's graphs are insufficiently heterogeneous to justify HGT and stop here*
- [ ] `GN-104.D03` V5: All four probes pass
- [ ] `GN-104.D04` V7: Memory scales sub-quadratically in node count across 10k/50k/100k — three measurements recorded

---

## 5. Transformer Networks (GN-201 … GN-203) — P0/P1

### GN-201 — Graph Transformer (GraphGPS-style)

**Priority** P1 · **Path** `packages/eoip/neural/transformer/graph_transformer.py` · **Levels** GL1, GL2

Local message passing + sparse global attention. Full O(n²) attention is **forbidden** above 10k
nodes — use top-k sparse or kernelised linear attention.

**Done when:**
- [ ] `GN-201.D01` V3: Structural encoding (Laplacian eigenvectors or random-walk) verifiably injected — ablate it and show measurable degradation
- [ ] `GN-201.D02` V4: Beats R-GCN by ≥ 0.03 AUPRC **on long-range tasks specifically** (shortest-path distance ≥ 4). On short-range tasks parity is acceptable
- [ ] `GN-201.D03` V7: Memory at 100k nodes is sub-quadratic — proven by the three-point measurement, not asserted

---

### GN-202 — KnowFormer (Path-Aware KG Attention)

**Priority** P2 · **Path** `packages/eoip/neural/transformer/knowformer.py` · **Levels** GL0, GL3

**Done when:**
- [ ] `GN-202.D01` V3: Multi-hop fixture question answered in a single forward pass, with the attended path extractable and matching the hand-verified ground-truth path
- [ ] `GN-202.D02` V4: Multi-hop (≥ 3 hop) MRR beats `GN-101` by ≥ 0.05
- [ ] `GN-202.D03` V5: All four probes pass

---

### GN-203 — Natural-Language Bridge

**Priority** P1 · **Path** `packages/eoip/neural/transformer/nl_bridge.py` · **Levels** all

NL question → subgraph retrieval → **grounded** answer. Integrates with existing `nlp/pipeline.py`
and `ragx/`.

**Binding constraints:**

1. Every answer cites the node and edge ids it used. An uncited answer is a defect.
2. The LLM **may not invent entities.** Post-generation, every entity named in the answer must
   resolve to a real node id, or the answer is rejected and regenerated once, then refused.
3. Entitlement filtering happens **before** subgraph retrieval, not after generation.
4. When an external LLM is configured, only embeddings and explicitly-allowed fields cross the
   boundary — never raw entity payloads. Honour the existing egress controls in `packages/eoip/egress/`.

**Done when:**
- [ ] `GN-203.D01` V3: **Hallucination probe** — ask about an entity that does not exist; the system answers "not found", never a fabrication. Run across 20 crafted non-existent entities, 20/20 required
- [ ] `GN-203.D02` V3: Every answer's cited ids resolve to real nodes — asserted over a 50-question fixture
- [ ] `GN-203.D03` V3: An unentitled user asking about a restricted entity receives the same "not found" response as for a non-existent one — *no existence disclosure*
- [ ] `GN-203.D04` V6: End-to-end `POST /neural/ask` returns answer + citations + confidence

---

## 6. Recurrent & Temporal Networks (GN-301 … GN-303) — P1

### GN-301 — GRU/LSTM Event Sequence Encoder
**Priority** P1 · **Path** `packages/eoip/neural/temporal/sequence.py` · **Levels** GLT

**Done when:**
- [ ] `GN-301.D01` V3: **Leakage probe** — training batches contain no event with `timestamp > prediction_time`; asserted by a validator that inspects every batch, not by reading the code
- [ ] `GN-301.D02` V4: Next-event prediction beats a most-frequent-event baseline by ≥ 0.10 Macro-F1
- [ ] `GN-301.D03` V5: All four probes pass

### GN-302 — Temporal Graph Network (TGN)
**Priority** P1 · **Path** `packages/eoip/neural/temporal/tgn.py` · **Levels** GLT, GL0

**Done when:**
- [ ] `GN-302.D01` V3: Per-node memory updates on event arrival; memory state at `t` is reproducible by replaying events to `t` — byte-compared
- [ ] `GN-302.D02` V4: Time-filtered MRR beats `GN-301` by ≥ 0.05, **or** the result is recorded as "GRU sufficient, TGN not justified" and TGN is not shipped
- [ ] `GN-302.D03` V5: All four probes pass

### GN-303 — RE-Net Recurrent Event Network
**Priority** P2 · **Path** `packages/eoip/neural/temporal/renet.py` · **Levels** GLT, GL0

**Done when:**
- [ ] `GN-303.D01` V4: Future-link prediction at `t+1` beats TGN by ≥ 0.03 MRR, or is recorded as not justified
- [ ] `GN-303.D02` V5: All four probes pass

---

## 7. Convolutional Networks (GN-401 … GN-403) — P1/P2

### GN-401 — ChebNet Spectral Filters
**Priority** P2 · **Path** `packages/eoip/neural/conv/chebnet.py` · **Levels** GL3

Polynomial order K=2–3. Purpose: structural anomaly detection on the ontology — "convolutional lint".

**Done when:**
- [ ] `GN-401.D01` V3: On a fixture containing a deliberately injected subsumption cycle and an unreachable concept cluster, both are flagged; a clean control fixture produces zero flags (no false positives)
- [ ] `GN-401.D02` V4: Anomaly AUPRC ≥ 0.70 against hand-labelled structural defects
- [ ] `GN-401.D03` V7: Laplacian decomposition cached; second run ≥ 10× faster than first

### GN-402 — ConvE Knowledge Graph Completion
**Priority** P1 · **Path** `packages/eoip/neural/conv/conve.py` · **Levels** GL0

2D-reshaped embedding convolution for triple scoring. This is the KG-specific CNN — **not** an image
CNN applied to topology.

**Done when:**
- [ ] `GN-402.D01` V4: Hits@10 ≥ 0.40 on the reference snapshot and within 0.05 of `GN-101`
- [ ] `GN-402.D02` V4: Parameter count **lower** than R-GCN at equal performance — ConvE's claimed advantage is parameter efficiency; measure it or drop the requirement
- [ ] `GN-402.D03` V5: All four probes pass

### GN-403 — Vision Encoder Bridge
**Priority** P2 · **Path** `packages/eoip/neural/conv/vision.py` · **Levels** GL0

Architecture diagrams and screenshots → candidate entities/relations. Integrates with the existing
`packages/eoip/fileparse/diagram_parser.py`.

**Done when:**
- [ ] `GN-403.D01` V3: On 10 hand-labelled architecture diagrams, ≥ 70% of boxes extracted as candidate entities and ≥ 50% of arrows as candidate relations
- [ ] `GN-403.D02` V3: **Every** extraction enters as `PREDICTED` with the source image and bounding box as provenance — zero exceptions
- [ ] `GN-403.D03` V4: Benchmarked against a vision-language model baseline; whichever wins is adopted and the loser's number recorded

---

## 8. Generative Networks (GN-501 … GN-502) — P2/P3, Gated

> **Ordering is deliberate and binding: the discriminator ships before the generator.** The
> discriminator alone is a useful, low-risk quality gate. The generator is the risky half. Building
> them in the usual order would couple a safe capability to an unsafe one.

### GN-501 — Adversarial Quality Discriminator
**Priority** P2 · **Path** `packages/eoip/neural/generative/discriminator.py` · **Levels** GL0, GL3

A per-write plausibility filter for ingested data. Scores candidate triples; implausible ones are
flagged for review — **flagged, never silently dropped**.

**Done when:**
- [ ] `GN-501.D01` V3: On a fixture of 100 true and 100 hand-crafted implausible triples, precision ≥ 0.80 at recall ≥ 0.70
- [ ] `GN-501.D02` V3: A flagged triple is **quarantined and visible for review**, never deleted — asserted by querying the quarantine after a flag
- [ ] `GN-501.D03` V3: The discriminator consults the ontology — a triple violating `edge_endpoints_valid()` is always rejected regardless of learned score
- [ ] `GN-501.D04` V7: Per-triple inference < 5 ms (it sits on the write path)

### GN-502 — Candidate Triple Generator
**Priority** P3 · **Research-gated** · **Path** `packages/eoip/neural/generative/generator.py`

**Entry gate — may not start until:** `GN-501` is in production AND a named stakeholder has signed a
written use case AND training instability mitigation (WGAN-GP or equivalent) is specified.

**Done when:**
- [ ] `GN-502.D01` V3: Generated triples **never** enter the graph outside a sandbox tenant — asserted by attempting a production write and catching the refusal
- [ ] `GN-502.D02` V5: Training stability — discriminator loss does not collapse (stays in [0.3, 0.7]) over 100 epochs
- [ ] `GN-502.D03` V4: ≥ 60% of generated triples judged plausible by a human reviewer on a 100-sample audit
- [ ] `GN-502.D04` If any gate fails, the honest outcome is **"GAN generation not justified for EOIP"** and that is a complete, successful requirement outcome

---

## 9. Spiking Neural Networks (GN-601) — P3, Sandboxed Research

### GN-601 — Spiking Graph Encoder
**Priority** P3 · **Path** `packages/eoip/neural/spiking/spike_encoder.py` · **Levels** GLT

**Binding constraints:**

1. **Fully sandboxed.** No production inference path may depend on this module. Enforced by an
   import-graph test asserting nothing outside `neural/spiking/` imports it.
2. Software simulation only (`snntorch`). **No neuromorphic hardware dependency.**
3. Any efficiency claim must be **measured on the hardware actually in use**, not cited from
   literature. SNNs are not automatically faster on CPU/GPU — on conventional hardware they are
   frequently *slower*. Claiming otherwise without measurement is non-compliant.

**Done when:**
- [ ] `GN-601.D01` V3: Encodes a graph as spike trains; decoding recovers node identity with ≥ 95% accuracy
- [ ] `GN-601.D02` V4: On a sparse-event stream, detects correlated bursts with AUPRC ≥ a thresholding baseline
- [ ] `GN-601.D03` V7: **Honest efficiency report** — wall-clock and energy (where measurable) vs the R-GCN equivalent on the same hardware. *If slower, say so.* A result of "SNN is 4× slower on our GPUs; revisit only with neuromorphic hardware" is a complete and valuable outcome
- [ ] `GN-601.D04` V6: Import-graph test proves zero production dependencies

---

## 10. Cross-Cutting Requirements (GN-701 … GN-706) — P0/P1

### GN-701 — Explainability
**Priority** P0 · **Path** `packages/eoip/neural/explain/explainer.py`

GNNExplainer-style influential-subgraph extraction. Every prediction surfaced to a user carries
evidence paths, attention weights where available, confidence, and model lineage.

**Done when:**
- [ ] `GN-701.D01` V3: ≥ 95% of predictions return non-empty `evidence_paths`
- [ ] `GN-701.D02` V3: **Faithfulness probe** — removing the identified evidence subgraph drops the prediction score by ≥ 50%. If it does not, the explanation is decorative and the requirement fails
- [ ] `GN-701.D03` V6: UI payload includes neural confidence *and* the deterministic-traversal answer side by side

### GN-702 — Fusion & Arbitration
**Priority** P1 · **Path** `packages/eoip/neural/fusion.py`

Dual-path: deterministic traversal **and** neural inference always both run. Never replace one with
the other.

**Done when:**
- [ ] `GN-702.D01` V3: Both paths execute and both results are returned
- [ ] `GN-702.D02` V3: On agreement, confidence is higher than either alone; on disagreement, the response is explicitly flagged as `DISPUTED` and surfaced — disagreement is a finding, not an error
- [ ] `GN-702.D03` V4: Fusion beats the better single path by ≥ 0.02 on the primary metric, or fusion is dropped

### GN-703 — Security & Entitlements
**Priority** P0 · **Path** `packages/eoip/neural/security.py`

**Binding constraints:**

1. Entitlement filtering runs **before** featurisation, training and retrieval — not after.
2. Embeddings are a leakage channel: a user who cannot see node X must not receive an embedding
   influenced by X in a way that permits reconstruction. Where an embedding is computed over
   restricted neighbours, it must not be served to unentitled users.
3. Cross-tenant parameter sharing is **forbidden** unless federated learning is explicitly enabled
   per tenant with recorded consent.

**Done when:**
- [ ] `GN-703.D01` V3: Cross-tenant embedding read returns empty against a crafted adversarial request
- [ ] `GN-703.D02` V3: **Membership-inference probe** — an unentitled user cannot determine whether a restricted node exists, via result counts, latency, or error-message differences. All three channels tested
- [ ] `GN-703.D03` V3: Training excludes nodes outside the training principal's entitlement scope — asserted by node-id set comparison
- [ ] `GN-703.D04` V6: Every neural endpoint enforces authz; a test sweeps all routes and asserts none is unprotected

### GN-704 — API Surface
**Priority** P0 · **Path** `packages/eoip/neural/router.py`

```
GET  /neural/runtime                  capabilities; 503 when unavailable
POST /neural/embeddings/compute       {tenant, snapshot, model} → job id
GET  /neural/embeddings/{node_id}     vector + lineage
POST /neural/predict/links            {source, top_k} → PredictedEdge[]
POST /neural/predict/impact           {changed_node} → affected subgraph + scores
POST /neural/classify/node            {node_id} → type + confidence
POST /neural/anomaly/scan             {scope} → ranked anomalies
POST /neural/ask                      {question} → grounded answer + citations
GET  /neural/explain/{prediction_id}  evidence subgraph
GET  /neural/models                   registry with gate reports
POST /neural/models/{id}/promote      requires actor id
POST /neural/models/{id}/rollback
GET  /neural/predictions              filterable by status; never returns OBSERVED
POST /neural/predictions/{id}/confirm requires human actor → CONFIRMED
POST /neural/predictions/{id}/reject  requires human actor → REJECTED
```

Follow house conventions **exactly**: Pydantic request models declared at **module level** (required
for FastAPI OpenAPI schema resolution — this has bitten this codebase before), thread-safe singleton
accessors, and a `stats()` method on every engine wired into `brain_os.py` telemetry.

**Done when:**
- [ ] `GN-704.D01` V6: All 15 routes present in `/openapi.json` with resolved schemas — no `$ref` resolution errors
- [ ] `GN-704.D02` V6: `neural` key present in `GET /brain/telemetry` with per-model stats
- [ ] `GN-704.D03` V6: Every route returns 503 (not 500, not a fabricated result) when the extra is absent
- [ ] `GN-704.D04` V3: Contract test asserts no route returns `AssertionStatus.OBSERVED` data from a neural path

### GN-705 — Performance Budgets
**Priority** P1

| Operation | p95 budget | Measured at |
|---|---|---|
| Embedding lookup | 10 ms | 100k nodes |
| Nearest-neighbour k=10 | 50 ms | 100k vectors |
| Link prediction top-10 | 200 ms | 100k nodes |
| Impact analysis 3-hop | 500 ms | 100k nodes |
| NL question end-to-end | 3 s | — |
| Discriminator per-triple | 5 ms | write path |
| Full retrain | 4 h | 1M edges |
| Incremental embedding refresh | 30 s | 1k changed nodes |

**Done when:** every row measured and recorded; any breach either fixed or formally accepted with a written rationale.
Tracker check IDs: `GN-705.D01` … `GN-705.D08` are the eight table rows above, in order. GN-705 is cross-phase: each row is measured
in the phase that introduces the operation and the GN-705 ledger closes at final sign-off (XP-17).

### GN-706 — Known Failure Modes: Explicit Guards
**Priority** P1

| Failure | Guard | Verification |
|---|---|---|
| **Oversmoothing** | Default `num_layers=2`; warn above 3 | Measure node-embedding pairwise variance at 2/4/8 layers; show collapse and prove the default avoids it |
| **Oversquashing** | Neighbour sampling + GL1 meta-graph shortcuts | Long-range (≥4 hop) task accuracy recorded separately from short-range |
| **Temporal leakage** | `GN-005` validator on every batch | Deliberate-injection test must raise |
| **Model staleness** | Drift monitor on embedding distribution | Simulated drift triggers an alert within one refresh cycle |
| **Popularity shortcut** | `DegreeBaseline` mandatory | If the model only ties `DegreeBaseline`, it learned popularity — reported as failure |
| **Class imbalance illusion** | AUPRC primary, AUROC never alone | Harness refuses AUROC-only reports |
| **Silent degradation** | No heuristic fallback (`GN-001`) | 503 asserted, fabricated results impossible |

Tracker check IDs: `GN-706.D01` … `GN-706.D07` are the seven table rows above, in order. GN-706 belongs to Phase 2 (its gate checks it; XP-17).

---

## 11. Completion Definition

This programme is complete when:

1. Every P0 requirement passes **V2–V7** with Evidence Ledger entries.
2. The hash stubs in `packages/eoip/gnn/engine.py` are **deleted** and no caller is broken.
3. At least one neural capability beats both `CommonNeighborsBaseline` and `RuleBaseline` by ≥ 0.05 on held-out data, with all five baselines published.
4. All four anti-stub probes pass for every shipped learned model.
5. No `PREDICTED` assertion has ever been written as `OBSERVED` — proven by audit query.
6. **All four tiers install and the degradation matrix holds:** `pip install -e .` resolves to an unchanged package set; each of N0/N1/N2/N3 installs cleanly; the four-venv tier matrix in `GN-001` passes.
7. **Every reported metric is reproducible** — same seed and snapshot reproduce it within 1e-4 across processes (`GN-012`).
8. **No Python-level numeric loops remain** in neural hot paths — `grep` gate in `GN-011` is clean.
9. **BLAS threads are governed** — the oversubscription probe in `GN-013` is recorded.
10. Requirements that failed their thresholds are **documented as failed**, not quietly dropped.

> **Point 7 is what makes the rest of this document meaningful.** An Evidence Ledger full of numbers
> that cannot be reproduced is decoration. Determinism is not a nice-to-have here; it is the
> precondition for every other verification level.

> **Point 10 is a first-class success criterion.** A programme that honestly reports "HGT did not
> beat R-GCN on our data, so we ship R-GCN" is complete. A programme that ships HGT without
> measuring it is not, regardless of how much code exists.

<!-- tracker-integration -->

## 12. Tracker Integration

This section adds identifiers and reporting rules for the EOIP programme tracker. Sections 0–11 are unchanged apart from the check ids added to each done-when line; nothing below is a requirement.

### 12.1 Tracked Identifiers

| Item | Identifier | Count |
| --- | --- | --- |
| Requirement / Evidence Ledger | `GN-<id>` → `EOIP-engg-doc-pkg/evidence/GN-<id>.md` | 36 |
| Done-when check | `GN-<id>.Dnn`, written at the start of every done-when line (GN-705 and GN-706: the table rows, in order) | 156 |
| Completion definition | `GN-CD-01` … `GN-CD-10` (§11 items in order) | 10 |
| Phase-gate checks, sign-off, fixtures | see plan §8 | 86 |

| Requirement | Priority | Phase | Checks | Honest FAILED is an accepted outcome |
| --- | --- | --- | --- | --- |
| GN-010 | P0 | 0a | 6 | no |
| GN-011 | P0 | 0a | 5 | no |
| GN-012 | P0 | 0a | 5 | no |
| GN-013 | P0 | 0a | 5 | no |
| GN-014 | P1 | 0a | 5 | no |
| GN-015 | P0 | 0a | 5 | no |
| GN-016 | P1 | 0a | 4 | no |
| GN-001 | P0 | 0b | 7 | no |
| GN-002 | P0 | 0b | 6 | no |
| GN-003 | P0 | 0b | 3 | no |
| GN-004 | P0 | 0b | 5 | no |
| GN-005 | P0 | 0b | 4 | no |
| GN-006 | P0 | 0b | 4 | no |
| GN-007 | P0 | 0b | 3 | no |
| GN-101 | P0 | 1 | 9 | no |
| GN-102 | P0 | 1 | 4 | no |
| GN-103 | P1 | 4 | 4 | yes |
| GN-104 | P1 | 4 | 4 | yes |
| GN-201 | P1 | 4 | 3 | yes |
| GN-202 | P2 | 7 | 3 | yes |
| GN-203 | P1 | 2 | 4 | no |
| GN-301 | P1 | 3 | 3 | no |
| GN-302 | P1 | 3 | 3 | yes |
| GN-303 | P2 | 7 | 2 | yes |
| GN-401 | P2 | 5 | 3 | no |
| GN-402 | P1 | 5 | 3 | yes |
| GN-403 | P2 | 5 | 3 | yes |
| GN-501 | P2 | 6 | 4 | no |
| GN-502 | P3 | 7 | 4 | yes |
| GN-601 | P3 | 7 | 4 | yes |
| GN-701 | P0 | 2 | 3 | no |
| GN-702 | P1 | 2 | 3 | yes |
| GN-703 | P0 | 2 | 4 | no |
| GN-704 | P0 | 2 | 4 | no |
| GN-705 | P1 | cross-phase | 8 | no |
| GN-706 | P1 | 2 | 7 | no |

### 12.2 Status Reporting

The ledger status values (`COMPLETE`, `FAILED`, `BLOCKED`) are unchanged.

| Tracker canonical state | Status written in this programme's own ledger |
|---|---|
| OPEN, IN_PROGRESS, CODE_COMPLETE, STALE | no ledger filed |
| EVIDENCED | draft ledger (not complete) |
| VERIFIED | `COMPLETE` |
| FAILED | `FAILED` |
| FAILED_ACCEPTED | `FAILED — accepted outcome` (bake-off requirements only) |
| BLOCKED | `BLOCKED` |

A ledger is `COMPLETE` only when every one of its checks is verified. An honest `FAILED` ledger with real numbers and a recommendation resolves the requirement only for GN-103, GN-104, GN-201, GN-202, GN-302, GN-303, GN-402, GN-403, GN-502, GN-601, GN-702: their text or phase gate accepts a "not justified" outcome. A `FAILED` P0 requirement is recorded honestly and blocks programme completion (§11 item 1; Phase 1 "stop and escalate"); see XP-18.

### 12.3 What Moves a Check

A file path, class or function name, test-file name, test count, commit hash, green CI badge, screenshot or an agent's statement is never proof of completion on its own. The tracker and the verifier refuse EVIDENCED unless an executed run is recorded (command, exit code 0, environment, evidence path and its SHA-256, bound to the current requirement text), and refuse VERIFIED unless a reviewer who is not the producer re-ran it and recorded the verification reference.

V1 checks ("file exists") can be recorded but never complete a ledger on their own.

| Target state | Required evidence (checked by the tracker and by `verify_programme_ledger.mjs`) |
|---|---|
| IN_PROGRESS | Owner and work reference (task card, branch, ledger draft or DR id). |
| CODE_COMPLETE | 40-hex commit and the changed paths. The paths are navigation only and are never proof. |
| EVIDENCED (draft ledger) | Commit; ledger path `EOIP-engg-doc-pkg/evidence/GN-<id>.md` and its SHA-256; producer; exact command; exit code 0; environment; for every check the measured result pasted from real output; V4 checks: all five baselines beside the model number and the snapshot id; V5 checks: probes P1–P4 with measurements; ledgers: seed and `capture_environment()` reference. |
| VERIFIED | Everything above plus reviewer different from the producer, review date, sign-off reference, re-run attestation (one number reproduced within 1e-4); a ledger is COMPLETE only when every one of its checks is VERIFIED. |
| FAILED | Failure note with the observed numbers or error, and a reference to the failing run. |
| BLOCKED | The blocking dependency, decision id or missing input. |
| STALE | What changed (source, artifact, environment or requirement text). |

### 12.4 Cross-Programme Decisions Holding Graph Neurons Items

| Decision | Subject | Items held below VERIFIED until DECIDED | Record as |
|---|---|---|---|
| XP-02 | Prediction / fact status models differ | `GN-002` | CONFLICT-IP-NNN (next free number in docs/ip/ip-progress-ledger.md) |
| XP-04 | Model registry: MLflow / metadata store vs mlops experiment tracker | `GN-007` | DR-IP (REQ-NEU-032) + GN Q-entry |
| XP-06 | Two natural-language question endpoints | `GN-203` | CONFLICT-IP-NNN (next free number in docs/ip/ip-progress-ledger.md) |
| XP-07 | Embedding store ownership | `GN-004` | DR-IP + GN Q-entry |
| XP-08 | Snapshot identity and format | `GN-005` | DR-IP + GN Q-entry |
| XP-16 | Graph Neurons pre-existing test-file count (302 vs 239) | `GN-PH1.G05`, `GN-SO-16` | GN Q-entry |
| XP-17 | GN-705 and GN-706 have no phase | `GN-705`, `GN-706` | GN Q-entry |
| XP-22 | External model endpoints | `GN-203` | CONFLICT-IP-NNN (next free number in docs/ip/ip-progress-ledger.md) |

- **XP-02 Prediction / fact status models differ.** Store the IP warrant status as the authoritative status and keep GN AssertionStatus as the neural-layer lifecycle field: GN PREDICTED = warrant PREDICTED (operator class MODEL); GN DERIVED = A1 COMPUTATION result (status = min of inputs, never above them); GN CONFIRMED = a new ATTESTED warrant by the human approver whose parents include the prediction warrant (REQ-VER-002), lineage retained; GN REJECTED = verification task RESOLVED_REFUTED (valid_to = now, refuted_by link). ASPEII classifies all of these as HYPOTHESIS unless independently verified. A neural path never writes OBSERVED (GN-002 constraint 2 and REQ-WAR-022 both hold).
- **XP-03 One neural implementation, two component names.** Bind IP component `neural-service` to `packages/eoip/neural/` in docs/ip/ip-binding-map.md. Invention 2 learned mode imports the GN-103/GN-104 encoders; no second encoder implementation. IP modules for inventions that are not encoders (drift, advisor, forensics …) live under `packages/eoip/neural/` subpackages named after the IP component.
- **XP-04 Model registry: MLflow / metadata store vs mlops experiment tracker.** One registry: GN-007's extension of experiment_tracker.py is the KGF metadata store named in REQ-NEU-032 (no MLflow). Stage mapping CANDIDATE=candidate, ACTIVE=production, RETIRED=retired. Records carry the union of IP fields (REQ-NEU-030) and GN gate reports.
- **XP-05 Promotion thresholds for learned models.** Apply the conjunction: a model is promoted only when every IP gate and every GN-007 gate passes. Prior mode counts as the RuleBaseline for Invention 2. Neither threshold set is lowered.
- **XP-06 Two natural-language question endpoints.** `POST /ask` is the user-facing route. GN-203 nl_bridge is the neural path of REQ-INV3-005(b) and must run through the checkpoint SDK so every answer carries a warrant. `POST /neural/ask` stays as the GN contract route and returns the same warrant id plus citations; both share one implementation.
- **XP-07 Embedding store ownership.** GN-004 FeatureStore is the single embedding store. It keys rows by the IP tuple (tenant, level, model_version, snapshot_version) and reaches the vector-store abstraction through an adapter; Procrustes matrices (REQ-NEU-021) are stored with the snapshot.
- **XP-08 Snapshot identity and format.** Snapshot id = GN-005 content hash. The REQ-NEU-001 Parquet export is written under that id with metadata (graph_version, recorded_at, counts). ref-2026-10 remains frozen; new snapshots never overwrite it.
- **XP-09 Libraries needed by IP inventions are not in the GN licence table.** Before use, add each package (and each model weight with its licence) to the GN licence table with tier and verdict after Legal review; record the DR id in the ledger. Until then the dependent requirement stays BLOCKED.
- **XP-16 Graph Neurons pre-existing test-file count (302 vs 239).** Neither number is assumed. Count `find tests -name "test_*.py" | wc -l` at the Phase 0a baseline, record the number and the file list digest in the GN-010 ledger, and use that recorded number for GN-PH1.G05 and GN-SO-16.
- **XP-17 GN-705 and GN-706 have no phase.** GN-706 belongs to Phase 2 (its gate already checks it). GN-705 is cross-phase: each budget row is measured in the phase that introduces the operation and the GN-705 ledger closes at final sign-off.
- **XP-18 'A missed threshold honestly reported is complete' vs P0 must pass.** An honest FAILED ledger resolves a requirement only where the requirement text allows that outcome (GN-103, 104, 201, 202, 302, 303, 402, 403, 502, 601, 702). A FAILED P0 requirement is recorded honestly and blocks programme completion (Phase 1 'stop and escalate').
- **XP-22 External model endpoints.** Default local everywhere. An external endpoint is used only when all hold: tenant data-sharing policy permits the data class for that endpoint (REQ-PLT-005), egress controls in packages/eoip/egress/ apply (GN-203), and the ASPEII hosted-model profile has an approved budget. IP features ship and are evidenced in local mode only.
- **XP-28 Federated learning consent.** The REQ-INV6-001 opt-in record (who, when, which classes) is the GN-703 consent record; GN-703 tests treat a tenant without that record as non-federated.
