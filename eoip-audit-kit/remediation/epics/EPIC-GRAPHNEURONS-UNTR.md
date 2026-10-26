# EPIC-GRAPHNEURONS-UNTR: EOIP-engg-doc-pkg/Graph-Neurons-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 14 tasks, ~94.0 h, priorities {'P0': 2, 'P1': 8, 'P2': 4}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-GN-101 [P0] GN-101: R-GCN: Replace the Hash Stub

- **Source:** `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md:840-892` (heading) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 11 other site(s): see duplicate task DUP-GN-101; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 9.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
- [ ] V1: File exists — *acknowledged as insufficient*
- [ ] V2: Training runs end-to-end on the reference snapshot, exit 0, loss curve printed
- [ ] V3: On the hand-built fixture in `tests/neural/fixtures/known_graph.json`, the model recovers 5 deliberately-removed edges in its top-10 predictions
- [ ] V4: Test-split **AUPRC ≥ CommonNeighborsBaseline + 0.05** and **≥ RuleBaseline + 0.05**, with all five baseline numbers printed in the ledger
- [ ] V5: **All four anti-stub probes pass.** P3 permutation gap ≥ 0.10 — this is the gate the current stub fails
- [ ] V6: `POST /neura
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-101' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-101') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-101

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): R-GCN: Replace the Hash Stub Priority P0 · Path packages/eoip/neural/encoders/rgcn.py · Levels GL0, GL2 Build a real Relational Graph Convolutional Network (Schlichtkrull et al., 2018) in PyTorch Geometric. Relation-specific weight matrices with basis decomposition to control parameter count. python class RGCNEncoder(nn.Module): def __init__(self, num_nodes: int, num_relations:
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-102 [P0] GN-102: GraphSAGE (Inductive)

- **Source:** `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md:893-907` (heading) · **Type:** AI · **Severity:** High
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 6 other site(s): see duplicate task DUP-GN-102; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### GN-102 — GraphSAGE (Inductive)

**Priority** P0 · **Path** `packages/eoip/neural/encoders/graphsage.py` · **Levels** GL0, GL2

Inductive embedding so newly-ingested entities get vectors **without retraining** — essential because
connectors add entities continuously.

**Done when:**
- [ ] V3: **Inductive proof** — train on snapshot `S1`; add 100 new nodes forming `S2`; embed them with the `S1`-trained model; assert no retraining occurred (weight hash identical before and after) and the new embeddings are non-degenerate (pairwise cosine variance > 0.01)
- [ ] V4: New-node link-prediction AUPRC within 0.10 of seen-node AUPRC
- [ ] V5: All four probes pass
- [ ] V7: Embedding 1,000 new nodes completes in < 5 s

---
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-102' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-102') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-102

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): GraphSAGE (Inductive) Priority P0 · Path packages/eoip/neural/encoders/graphsage.py · Levels GL0, GL2 Inductive embedding so newly-ingested entities get vectors without retraining — essential because connectors add entities continuously. Done when: - [ ] V3: Inductive proof — train on snapshot S1; add 100 new nodes forming S2; embed them with the S1-trained model; assert no ret
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-103 [P1] GN-103: Relational Graph Attention (R-GAT)

- **Source:** `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md:908-922` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 6 other site(s): see duplicate task DUP-GN-103; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### GN-103 — Relational Graph Attention (R-GAT)

**Priority** P1 · **Path** `packages/eoip/neural/encoders/rgat.py` · **Levels** GL0, GL2

Attention weights are the explainability substrate for `GN-701` — they must be **retrievable per
prediction**, not merely computed internally.

**Done when:**
- [ ] V3: `get_attention_weights(source, target)` returns per-edge weights summing to 1.0 ± 1e-5 per head
- [ ] V3: On a fixture with one deliberately dominant path, that path receives the highest attention — hand-verified
- [ ] V4: AUPRC ≥ R-GCN (`GN-101`) − 0.02. *If R-GAT does not beat R-GCN, record that honestly and keep R-GCN as default*
- [ ] V5: All four probes pass

---
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-103' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-103') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-103

**Acceptance criteria**
- [ ] Priority P1 · Path packages/eoip/neural/encoders/rgat.py · Levels GL0, GL2 Attention weights are the explainability substrate for GN-701 — they must be retrievable per prediction, not merely computed internally.
- [ ] If R-GAT does not beat R-GCN, record that honestly and keep R-GCN as default - [ ] V5: All four probes pass
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-104 [P1] GN-104: Heterogeneous Graph Transformer (HGT)

- **Source:** `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md:923-936` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 6 other site(s): see duplicate task DUP-GN-104; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### GN-104 — Heterogeneous Graph Transformer (HGT)

**Priority** P1 · **Path** `packages/eoip/neural/encoders/hgt.py` · **Levels** GL1, GL2

Node-type- and edge-type-specific attention for the meta-graph and cross-domain living brain.

**Done when:**
- [ ] V3: Distinct parameter sets exist per node type and edge type — asserted by inspecting `state_dict()` keys against the manifest's type list
- [ ] V4: On a **multi-domain** fixture spanning ≥ 3 domains, HGT beats homogeneous R-GCN by ≥ 0.03 AUPRC. *If it does not, document that EOIP's graphs are insufficiently heterogeneous to justify HGT and stop here*
- [ ] V5: All four probes pass
- [ ] V7: Memory scales sub-quadratically in node count across 10k/50k/100k — three measurements recorded

---
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-104' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-104') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-104

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Heterogeneous Graph Transformer (HGT) Priority P1 · Path packages/eoip/neural/encoders/hgt.py · Levels GL1, GL2 Node-type- and edge-type-specific attention for the meta-graph and cross-domain living brain. Done when: - [ ] V3: Distinct parameter sets exist per node type and edge type — asserted by inspecting state_dict() keys against the manifest's type list - [ ] V4: On a mult
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-201 [P1] GN-201: Graph Transformer (GraphGPS-style)

- **Source:** `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md:939-952` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 5 other site(s): see duplicate task DUP-GN-201; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### GN-201 — Graph Transformer (GraphGPS-style)

**Priority** P1 · **Path** `packages/eoip/neural/transformer/graph_transformer.py` · **Levels** GL1, GL2

Local message passing + sparse global attention. Full O(n²) attention is **forbidden** above 10k
nodes — use top-k sparse or kernelised linear attention.

**Done when:**
- [ ] V3: Structural encoding (Laplacian eigenvectors or random-walk) verifiably injected — ablate it and show measurable degradation
- [ ] V4: Beats R-GCN by ≥ 0.03 AUPRC **on long-range tasks specifically** (shortest-path distance ≥ 4). On short-range tasks parity is acceptable
- [ ] V7: Memory at 100k nodes is sub-quadratic — proven by the three-point measurement, not asserted

---
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-201' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-201') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-201

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Graph Transformer (GraphGPS-style) Priority P1 · Path packages/eoip/neural/transformer/graph_transformer.py · Levels GL1, GL2 Local message passing + sparse global attention. Full O(n²) attention is forbidden above 10k nodes — use top-k sparse or kernelised linear attention. Done when: - [ ] V3: Structural encoding (Laplacian eigenvectors or random-walk) verifiably injected — a
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-301 [P1] GN-301: GRU/LSTM Event Sequence Encoder

- **Source:** `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md:990-997` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 5 other site(s): see duplicate task DUP-GN-301; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### GN-301 — GRU/LSTM Event Sequence Encoder
**Priority** P1 · **Path** `packages/eoip/neural/temporal/sequence.py` · **Levels** GLT

**Done when:**
- [ ] V3: **Leakage probe** — training batches contain no event with `timestamp > prediction_time`; asserted by a validator that inspects every batch, not by reading the code
- [ ] V4: Next-event prediction beats a most-frequent-event baseline by ≥ 0.10 Macro-F1
- [ ] V5: All four probes pass
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-301' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-301') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-301

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): GRU/LSTM Event Sequence Encoder Priority P1 · Path packages/eoip/neural/temporal/sequence.py · Levels GLT Done when: - [ ] V3: Leakage probe — training batches contain no event with timestamp > prediction_time; asserted by a validator that inspects every batch, not by reading the code - [ ] V4: Next-event prediction beats a most-frequent-event baseline by ≥ 0.10 Macro-F1 - [ ] 
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-302 [P1] GN-302: Temporal Graph Network (TGN)

- **Source:** `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md:998-1005` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 5 other site(s): see duplicate task DUP-GN-302; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### GN-302 — Temporal Graph Network (TGN)
**Priority** P1 · **Path** `packages/eoip/neural/temporal/tgn.py` · **Levels** GLT, GL0

**Done when:**
- [ ] V3: Per-node memory updates on event arrival; memory state at `t` is reproducible by replaying events to `t` — byte-compared
- [ ] V4: Time-filtered MRR beats `GN-301` by ≥ 0.05, **or** the result is recorded as "GRU sufficient, TGN not justified" and TGN is not shipped
- [ ] V5: All four probes pass
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-302' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-302') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-302

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Temporal Graph Network (TGN) Priority P1 · Path packages/eoip/neural/temporal/tgn.py · Levels GLT, GL0 Done when: - [ ] V3: Per-node memory updates on event arrival; memory state at t is reproducible by replaying events to t — byte-compared - [ ] V4: Time-filtered MRR beats GN-301 by ≥ 0.05, or the result is recorded as "GRU sufficient, TGN not justified" and TGN is not shipped
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-402 [P1] GN-402: ConvE Knowledge Graph Completion

- **Source:** `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md:1027-1037` (heading) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 5 other site(s): see duplicate task DUP-GN-402; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### GN-402 — ConvE Knowledge Graph Completion
**Priority** P1 · **Path** `packages/eoip/neural/conv/conve.py` · **Levels** GL0

2D-reshaped embedding convolution for triple scoring. This is the KG-specific CNN — **not** an image
CNN applied to topology.

**Done when:**
- [ ] V4: Hits@10 ≥ 0.40 on the reference snapshot and within 0.05 of `GN-101`
- [ ] V4: Parameter count **lower** than R-GCN at equal performance — ConvE's claimed advantage is parameter efficiency; measure it or drop the requirement
- [ ] V5: All four probes pass
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-402' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-402') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-402

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): ConvE Knowledge Graph Completion Priority P1 · Path packages/eoip/neural/conv/conve.py · Levels GL0 2D-reshaped embedding convolution for triple scoring. This is the KG-specific CNN — not an image CNN applied to topology. Done when: - [ ] V4: Hits@10 ≥ 0.40 on the reference snapshot and within 0.05 of GN-101 - [ ] V4: Parameter count lower than R-GCN at equal performance — Conv
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-502 [P1] GN-502: Candidate Triple Generator

- **Source:** `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md:1069-1082` (heading) · **Type:** AI · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 6 other site(s): see duplicate task DUP-GN-502; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### GN-502 — Candidate Triple Generator
**Priority** P3 · **Research-gated** · **Path** `packages/eoip/neural/generative/generator.py`

**Entry gate — may not start until:** `GN-501` is in production AND a named stakeholder has signed a
written use case AND training instability mitigation (WGAN-GP or equivalent) is specified.

**Done when:**
- [ ] V3: Generated triples **never** enter the graph outside a sandbox tenant — asserted by attempting a production write and catching the refusal
- [ ] V5: Training stability — discriminator loss does not collapse (stays in [0.3, 0.7]) over 100 epochs
- [ ] V4: ≥ 60% of generated triples judged plausible by a human reviewer on a 100-sample audit
- [ ] If any gate fails, the honest outcome is **"GAN generation not justified for EOIP"** and that is a complete, successful requirement outcome

---
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-502' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-502') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-502

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Candidate Triple Generator Priority P3 · Research-gated · Path packages/eoip/neural/generative/generator.py Entry gate — may not start until: GN-501 is in production AND a named stakeholder has signed a written use case AND training instability mitigation (WGAN-GP or equivalent) is specified. Done when: - [ ] V3: Generated triples never enter the graph outside a sandbox tenant 
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-601 [P1] GN-601: Spiking Graph Encoder

- **Source:** `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md:1085-1104` (heading) · **Type:** AI · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 6 other site(s): see duplicate task DUP-GN-601; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
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
- [ ] V3: Encodes a graph as spike trains; decoding recovers node identity with ≥ 95% accuracy
- [ ] V4: On a sparse-event stream, detects correlated bursts with AUPRC ≥ a thresholding baseline
- [ ] V7: **Honest efficiency report** — wall-clock and energy (where measurable) vs the R-GCN equivalent on the same hardware. *If slower, say so.* A result of "SNN is 4× slower on our GPUs; revisit only with neuromorphic hardware" is a complete and valuable outcome
- [ ] V6: Import-graph test proves zero production dependencies

---
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-601' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-601') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-601

**Acceptance criteria**
- [ ] Enforced by an import-graph test asserting nothing outside neural/spiking/ imports it.
- [ ] Any efficiency claim must be measured on the hardware actually in use, not cited from literature.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-202 [P2] GN-202: KnowFormer (Path-Aware KG Attention)

- **Source:** `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md:953-963` (heading) · **Type:** AI · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 5 other site(s): see duplicate task DUP-GN-202; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### GN-202 — KnowFormer (Path-Aware KG Attention)

**Priority** P2 · **Path** `packages/eoip/neural/transformer/knowformer.py` · **Levels** GL0, GL3

**Done when:**
- [ ] V3: Multi-hop fixture question answered in a single forward pass, with the attended path extractable and matching the hand-verified ground-truth path
- [ ] V4: Multi-hop (≥ 3 hop) MRR beats `GN-101` by ≥ 0.05
- [ ] V5: All four probes pass

---
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-202' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-202') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-202

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): KnowFormer (Path-Aware KG Attention) Priority P2 · Path packages/eoip/neural/transformer/knowformer.py · Levels GL0, GL3 Done when: - [ ] V3: Multi-hop fixture question answered in a single forward pass, with the attended path extractable and matching the hand-verified ground-truth path - [ ] V4: Multi-hop (≥ 3 hop) MRR beats GN-101 by ≥ 0.05 - [ ] V5: All four probes pass
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-303 [P2] GN-303: RE-Net Recurrent Event Network

- **Source:** `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md:1006-1014` (heading) · **Type:** AI · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 4 other site(s): see duplicate task DUP-GN-303; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### GN-303 — RE-Net Recurrent Event Network
**Priority** P2 · **Path** `packages/eoip/neural/temporal/renet.py` · **Levels** GLT, GL0

**Done when:**
- [ ] V4: Future-link prediction at `t+1` beats TGN by ≥ 0.03 MRR, or is recorded as not justified
- [ ] V5: All four probes pass

---
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-303' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-303') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-303

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): RE-Net Recurrent Event Network Priority P2 · Path packages/eoip/neural/temporal/renet.py · Levels GLT, GL0 Done when: - [ ] V4: Future-link prediction at t+1 beats TGN by ≥ 0.03 MRR, or is recorded as not justified - [ ] V5: All four probes pass
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-401 [P2] GN-401: ChebNet Spectral Filters

- **Source:** `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md:1017-1026` (heading) · **Type:** AI · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 5 other site(s): see duplicate task DUP-GN-401; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### GN-401 — ChebNet Spectral Filters
**Priority** P2 · **Path** `packages/eoip/neural/conv/chebnet.py` · **Levels** GL3

Polynomial order K=2–3. Purpose: structural anomaly detection on the ontology — "convolutional lint".

**Done when:**
- [ ] V3: On a fixture containing a deliberately injected subsumption cycle and an unreachable concept cluster, both are flagged; a clean control fixture produces zero flags (no false positives)
- [ ] V4: Anomaly AUPRC ≥ 0.70 against hand-labelled structural defects
- [ ] V7: Laplacian decomposition cached; second run ≥ 10× faster than first
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-401' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-401') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-401

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): ChebNet Spectral Filters Priority P2 · Path packages/eoip/neural/conv/chebnet.py · Levels GL3 Polynomial order K=2–3. Purpose: structural anomaly detection on the ontology — "convolutional lint". Done when: - [ ] V3: On a fixture containing a deliberately injected subsumption cycle and an unreachable concept cluster, both are flagged; a clean control fixture produces zero flags
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GN-403 [P2] GN-403: Vision Encoder Bridge

- **Source:** `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md:1038-1050` (heading) · **Type:** AI · **Severity:** Low
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 5 other site(s): see duplicate task DUP-GN-403; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### GN-403 — Vision Encoder Bridge
**Priority** P2 · **Path** `packages/eoip/neural/conv/vision.py` · **Levels** GL0

Architecture diagrams and screenshots → candidate entities/relations. Integrates with the existing
`packages/eoip/fileparse/diagram_parser.py`.

**Done when:**
- [ ] V3: On 10 hand-labelled architecture diagrams, ≥ 70% of boxes extracted as candidate entities and ≥ 50% of arrows as candidate relations
- [ ] V3: **Every** extraction enters as `PREDICTED` with the source image and bounding box as provenance — zero exceptions
- [ ] V4: Benchmarked against a vision-language model baseline; whichever wins is adopted and the loser's number recorded

---
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GN-403' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GN-403') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-GN-403

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): Vision Encoder Bridge Priority P2 · Path packages/eoip/neural/conv/vision.py · Levels GL0 Architecture diagrams and screenshots → candidate entities/relations. Integrates with the existing packages/eoip/fileparse/diagram_parser.py. Done when: - [ ] V3: On 10 hand-labelled architecture diagrams, ≥ 70% of boxes extracted as candidate entities and ≥ 50% of arrows as candidate rela
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

