# Chapter 5 — RAG & Natural Language Querying

This chapter explains how EOIP answers natural-language questions over your knowledge
graph: the 17 classic RAG patterns, the 22 extended "ragx" architectures, retrieval
strategies, the suggestion engine for ambiguous questions, report generation, and the
model providers and governance controls behind all of it.

**Honesty note.** Everything below is grounded in the source code (paths are cited).
All RAG answering is *deterministic-first*: it works with no LLM installed. Where an
optional model (Ollama) adds narration, that is marked. Response JSON shown is
constructed from the actual response models; exact field values depend on your graph
contents and were not all exercised against a live server.

## Index

1. [How RAG answering works end to end](#1-how-rag-answering-works-end-to-end)
2. [POST /api/v1/rag/query](#2-post-apiv1ragquery)
3. [GET /api/v1/rag/patterns](#3-get-apiv1ragpatterns)
4. [ragx: 22 extended architectures](#4-ragx-22-extended-architectures)
5. [ragx techniques (POST /api/v1/ragx/techniques/apply)](#5-ragx-techniques)
6. [ragx metrics (POST /api/v1/ragx/metrics/compute)](#6-ragx-metrics)
7. [Retrieval strategies: keyword / vector / hybrid and traces](#7-retrieval-strategies)
8. [Suggestion engine for ambiguous questions](#8-suggestion-engine)
9. [Answer modes](#9-answer-modes)
10. [Reports (/api/v1/reports)](#10-reports)
11. [Model provider configuration (Ollama)](#11-model-provider-configuration)
12. [Embeddings health endpoint](#12-embeddings-health-endpoint)
13. [Model governance endpoints](#13-model-governance-endpoints)

---

## 1. How RAG answering works end to end

**Source:** `packages/eoip/graph/rag_router.py`

The pipeline for every RAG answer is:

1. **Pattern selection.** `RAGRouter.route(query, pattern, context)` either uses the
   `pattern` you pass explicitly or calls `classify()`:
   - 4 words or fewer → `simple`
   - contains "community", "cluster", "overview", "summary" → `graph`
   - a `selected_id` in context plus "impact"/"break"/"path"/"trace" → `multihop`
   - more than one `?` in the query → `multistep`
   - contains "surprising", "unexpected", "strange" → `hybrid`
   - otherwise → `adaptive`
2. **Retrieval + generation.** The chosen pattern class runs `retrieve()` against the
   `GraphStore` (keyword scans, community detection, blast-radius traversal, etc.) and
   `generate()` builds a template answer such as
   `Found 7 relevant entities: jira:EOIP-123; service:checkout; ...`. No LLM is required.
3. **Evidence manifest (GAP-KRAG-009).** `RAGAbstentionPolicy.build_manifest()` turns
   each cited source into an `EvidenceItem` with a stable URN
   (`urn:eoip:rag:evidence:<n>`), a `kind` (`entity` | `path` | `community`), an
   `authority` score (from vertex properties `authority` / `confidence` /
   `trust_confidence`, default 0.5), and a `recency` score computed with a 30-day
   half-life from `last_verified`/`updated_at`/`created_at` timestamps. The manifest
   aggregates `entity_count`, `path_count`, `avg_authority`, `avg_recency`, and
   `coverage` (items ÷ `target_evidence_items` = 5, capped at 1.0).
4. **Abstention policy (GAP-KRAG-007).** `evaluate()` abstains when evidence is weak.
   Reason codes:
   - `NO_RETRIEVED_EVIDENCE` — fewer than `min_evidence_items` (1) items
   - `INSUFFICIENT_ENTITIES` — fewer than `min_entities` (1) distinct sources
   - `INSUFFICIENT_PATHS` — fewer than `min_paths` (0) graph paths
   - `LOW_SOURCE_AUTHORITY` — mean authority below `min_avg_authority` (0.2)
   - `LOW_EVIDENCE_COVERAGE` — coverage below `min_coverage` (0.2)
5. **Confidence calibration (GAP-KRAG-008).** When *not* abstaining, confidence is
   recomputed from evidence only — never from model self-confidence:
   `0.5 × coverage + 0.3 × avg_authority + 0.2 × avg_recency`, rounded to 3 decimals.

When abstained, the answer text is exactly
`"Abstained: insufficient evidence to answer reliably."`, confidence is `0.0`, and the
response carries `abstention_reasons` and a human-readable `missing_evidence` string.

---

## 2. POST /api/v1/rag/query

**What it does.** Answers a natural-language question over the graph using one of the
17 RAG patterns, with abstention and an evidence manifest attached.

**How to access.** `POST /api/v1/rag/query` (wired in `apps/api/app.py:1656`).
Request model `RAGQueryRequest`: `query` (string, required), `pattern` (string,
optional), `context` (object, optional — e.g. `{"selected_id": "service:checkout"}`).

**Step by step.**

```bash
curl -s -X POST http://localhost:8000/api/v1/rag/query \
  -H "Content-Type: application/json" \
  -d '{
        "query": "what is the impact if checkout fails?",
        "pattern": "multihop",
        "context": {"selected_id": "service:checkout"}
      }'
```

1. Pick a pattern from `GET /api/v1/rag/patterns` (below) or omit `pattern` to let the
   classifier choose.
2. For `multihop`/`conversational` patterns, pass `context.selected_id` — the
   `multihop` pattern falls back to `simple` when it is missing.
3. Read `answer`, then verify `confidence`, `abstained`, and `evidence_manifest`
   before trusting the answer in a report.

**Response/result.** From `RAGResult.to_dict()`:

```json
{
  "answer": "Found 12 relevant entities: service:payments; service:cart; ...",
  "rag_pattern": "multihop",
  "confidence": 0.62,
  "sources": ["service:payments", "service:cart"],
  "highlight_ids": ["service:payments", "service:cart"],
  "metadata": {"evidence_count": 12},
  "abstained": false,
  "abstention_reasons": [],
  "missing_evidence": "",
  "evidence_manifest": {
    "items": [{"id": "urn:eoip:rag:evidence:1", "source_id": "service:payments",
               "kind": "entity", "authority": 0.5, "recency": 0.93, "score": 1.0}],
    "entity_count": 12, "path_count": 0,
    "avg_authority": 0.5, "avg_recency": 0.93, "coverage": 1.0
  }
}
```

**Errors and recovery.**

- `abstained: true` with `LOW_EVIDENCE_COVERAGE` → your graph is small or the query
  matched little; ingest more sources or broaden the query. `missing_evidence` tells
  you exactly which floor failed (e.g. `"coverage >= 0.20; got 0.00"`).
- Unknown `pattern` name → silently falls back to the classifier
  (`name if pattern in _RAG_IMPLEMENTATIONS else self.classify(...)`), not a 404.
- Empty graph → every pattern returns "No relevant context found." with confidence
  0.1, which the policy then converts into an abstention.

---

## 3. GET /api/v1/rag/patterns

**What it does.** Lists the 17 built-in RAG patterns.

**How to access.** `GET /api/v1/rag/patterns` (`apps/api/app.py:1662`).

**Response.** `{"patterns": [{"name": ..., "description": ...}, ...]}`. The 17 names
(from `RAG_PATTERNS` in `rag_router.py:198`):

| name | when to use |
|---|---|
| `simple` | Simple factual queries |
| `advanced` | Complex queries needing precision |
| `graph` | Questions spanning the entire graph |
| `hybrid` | Multi-modality queries |
| `corrective` | When initial retrieval insufficient |
| `self` | Response quality verification |
| `adaptive` | Cost/latency optimization |
| `agentic` | Open-ended exploration |
| `modular` | Custom retrieval pipelines |
| `hyde` | Abstract queries, concrete answers |
| `conversational` | Multi-turn exploration sessions |
| `multistep` | Compound questions |
| `multihop` | Causal chains, lineage traces |
| `branched` | Multiple valid retrieval paths |
| `multimodal` | Cross-domain queries |
| `speculative` | High-confidence answers |
| `rag_of_rags` | Complex multi-pattern queries |

**Honest caveat.** Several patterns share implementations today
(`_RAG_IMPLEMENTATIONS`, `rag_router.py:446`): `advanced`, `hyde` reuse `SimpleRAG`;
`agentic` reuses `AdaptiveRAG`; `modular`, `multimodal` reuse `HybridRAG`. They are
distinct in name, description, and routing, but their retrieval behavior is currently
the shared one. Not runtime-verified per pattern.

---

## 4. ragx: 22 extended architectures

**Source:** `packages/eoip/ragx/architectures.py`, router in `packages/eoip/ragx/router.py`.

**What it does.** A second-generation RAG layer ("gap analysis §4"). Every architecture
extends `RagxArchitecture` (`ragx/core.py`), which does fused keyword+vector retrieval
(60% keyword / 40% vector, both peak-normalized), produces graph-anchored `Candidate`
evidence with citations from `source_ref`/`evidence_key` properties, and applies the
same abstention policy as §1. Answers are deterministic templates unless a narrator
model is injected server-side.

**How to access.**

- `GET /api/v1/ragx/architectures` — list architectures, techniques, metrics.
- `POST /api/v1/ragx/query` — body `{"query": str, "architecture": str|null, "context": {}}`.

If `architecture` is omitted, `_adaptive_architecture()` picks one by keyword:
"event"→`event_aware`, "symbol"→`coderag`, "provenance"→`provenance_aware`,
"version"→`version_aware`, "community"→`hierarchical`, "overview"→`global_search`,
"path"→`pathrag`, "record"→`structured`; context keys `event_id` → `event_aware`,
`valid_at`/`known_at` → `temporal`, `version`/`doc_version` → `version_aware`;
default `local_search`.

**The 22 architectures** (name — class description; when to use):

1. `hierarchical` — top-level label grouping, then member drill-down. Use for "how is X organized" questions. Context: `members_per_group` (default 5).
2. `raptor` — recursive clustering summary tree (RAPTOR-style, token-Jaccard agglomeration). Use for big graph summarization. Context: `leaf_count`.
3. `lightrag` — dual local/global retrieval over a lightweight mention graph.
4. `hipporag` — associative memory via Personalized PageRank over the mention graph.
5. `pathrag` — prunes context to entities on paths between query-relevant seeds. Use for "how does A connect to B".
6. `kgrag` — entity-relation grounded retrieval with explicit triples.
7. `lazygraphrag` — token-budgeted greedy evidence packing. Use when context budget is tight.
8. `drift` — community-level answer followed by entity drill-down (DRIFT-style).
9. `global_search` — community summaries ranked and merged graph-wide. Use for overview questions.
10. `local_search` — entity-centric neighborhood expansion. The default; best starting point.
11. `temporal` — bitemporally filtered retrieval. Context: `valid_at`, `known_at`.
12. `federated` — merged retrieval across registered federation sources. **External gate** — needs adapter sources; without them it returns local results only.
13. `streaming` — append-only evidence deltas, always queryable.
14. `incremental` — CDC-driven index maintenance (upsert/delete).
15. `structured` — table/record evidence with row rendering. Use for record-shaped vertices.
16. `coderag` — symbol-level retrieval over `CodeSymbol`/`File`/`Repository` vertices. Use for code questions.
17. `multilingual` — language-tagged retrieval with fallback.
18. `multiagent` — retriever → critic → synthesizer loop (deterministic agents, no LLM required).
19. `privacy_aware` — authorization-filtered retrieval (pre-ranking filter).
20. `provenance_aware` — evidence-locked citations: candidates without `source_ref` are dropped.
21. `version_aware` — document-version pinned retrieval. Context: `version` / `doc_version`.
22. `event_aware` — event-centric participant/evidence retrieval. Context: `event_id`.

**Step by step.**

```bash
curl -s -X POST http://localhost:8000/api/v1/ragx/query \
  -H "Content-Type: application/json" \
  -d '{"query": "which symbols implement checkout retry",
       "architecture": "coderag", "context": {"top_k": 10}}'
```

**Response.** `RagxQueryResponse`: `architecture`, `answer`, `confidence`,
`abstained`, `abstention_reasons`, `sources`, `highlight_ids`, `metadata`
(includes `evidence_count`, `generation: "deterministic"`), `evidence_manifest`.

**Errors and recovery.**

- `404 unknown architecture: <name>` — the name is not in `ARCHITECTURES`; re-list
  with `GET /api/v1/ragx/architectures`.
- `abstained: true` — same reason codes as §1; try `local_search` or add `top_k`.
- Narration is **not** wired into the HTTP route (no narrator is passed in
  `build_router`), so all API answers are deterministic templates today.

---

## 5. ragx techniques

**What it does.** `POST /api/v1/ragx/techniques/apply` applies one of 25 named
techniques (`packages/eoip/ragx/techniques.py`, `TECHNIQUES` dict) to a query and/or
a candidate list you supply.

**Technique groups.**

- *Query transforms:* `query_expansion` (deterministic synonym table: bug→defect/issue,
  deploy→release/ship, auth→login..., up to 4 variants), `query_decomposition`
  (splits on `?`, " and then ", ", and "), `step_back`, `hyde` (builds a hypothetical
  document from the query plus seed candidates).
- *Fusion & reranking:* `reciprocal_rank_fusion`, `cross_encoder_rerank`
  (deterministic fallback scorer), `late_interaction`, `diversity_mmr`,
  `metadata_aware`, `parent_child`, `contextual_retrieval`.
- *Chunking/compression:* `semantic_chunking`, `dynamic_chunking`,
  `context_compression`, `evidence_deduplication` (simhash near-duplicate removal).
- *Retrieval loops (need the store-backed retriever; the route builds one from
  `local_search`):* `rag_fusion`, `iterative_rag`, `flare`, `ircot`,
  `cost_adaptive`, `verification_guided`, `multi_vector`.
- *Answer gating:* `contradiction_aware`, `confidence_gated` (runs the abstention
  policy on your candidates), `citation_aware` (flags unsupported claims).

**Step by step** — expand a query, then gate candidates:

```bash
curl -s -X POST http://localhost:8000/api/v1/ragx/techniques/apply \
  -H "Content-Type: application/json" \
  -d '{"technique": "query_expansion", "query": "fix the checkout deploy bug"}'
# → {"technique": "query_expansion",
#    "result": ["fix the checkout deploy bug", "patch the checkout deploy bug", ...]}

curl -s -X POST http://localhost:8000/api/v1/ragx/techniques/apply \
  -H "Content-Type: application/json" \
  -d '{"technique": "confidence_gated",
       "candidates": [{"source_id": "jira:EOIP-123", "text": "checkout deploy fails"}]}'
```

**Response.** `{"technique": name, "candidates": [...]}` for candidate-transforming
techniques (each candidate has `source_id`, `text`, `score`, `kind`, `label`,
`citations`), `{"technique": name, "candidates": [...], "extra": ...}` for tuple
returns (e.g. `ircot` also returns a rationale), or `{"result": ...}` otherwise.

**Errors and recovery.**

- `404 unknown technique` — name not in `TECHNIQUES`.
- `400 metric, not technique` — you passed `recall_at_k`; use `/metrics/compute`.
- `400 technique '<x>' needs a retriever; not invocable over HTTP` — a handful of
  techniques cannot run over HTTP at all.
- Any internal error is surfaced as `400` with the exception message.

---

## 6. ragx metrics

**What it does.** `POST /api/v1/ragx/metrics/compute` computes retrieval-quality
metrics over rankings you supply (`packages/eoip/ragx/metrics.py`). Pure functions —
no model needed.

**Metrics:** `recall_at_k`, `precision_at_k`, `mrr`, `ndcg_at_k`,
`citation_accuracy`, `access_control_correctness`.

**Step by step.**

```bash
curl -s -X POST http://localhost:8000/api/v1/ragx/metrics/compute \
  -H "Content-Type: application/json" \
  -d '{"metric": "recall_at_k",
       "ranking": ["jira:EOIP-123", "service:checkout", "doc:runbook-7"],
       "relevant": ["jira:EOIP-123", "doc:runbook-7"],
       "k": 3}'
# → {"metric": "recall_at_k", "value": 1.0}
```

Request fields (`MetricsRequest`): `ranking` (list of ids, or dicts with
`source_id`/`canonical_id`), `rankings` (list of rankings, for `mrr`), `relevant`
(set of relevant ids), `relevance` (graded scores for `ndcg_at_k`),
`claims` (for `citation_accuracy`: `[{"claim": ..., "citation": ...,
"valid_citations": [...]}]`), `allowed`/`denied` (for
`access_control_correctness`), `k` (default 10).

**Response.** `{"metric": ..., "value": <float>}`. Exception:
`access_control_correctness` returns an object:
`{"leaked": [...], "leak_count": n, "allowed_coverage": 0.x, "correct": true|false}`.

**Errors.** `404 unknown metric` for a bad name. Note empty `relevant` yields
`recall_at_k = 1.0` by definition; empty claims yields `citation_accuracy = 1.0`.

---

## 7. Retrieval strategies

**Sources:** `packages/eoip/retrieval/vectors.py`, `service.py`, `strategy_registry.py`.

- **Keyword** — `KeywordIndex`: BM25-style scoring (k1=1.5, b=0.75) over entity text
  built by `entity_text()` from label + name/summary/title/description/
  qualified_name/issue_key/path/content properties.
- **Vector** — `VectorIndex` with `HashingEmbedder` (256-dim signed hashing,
  log-scaled term frequency, L2-normalized; cosine similarity). Deterministic, no
  model. If you configure an embedding provider (§12), `VectorIndex(embedder)` uses
  it instead.
- **Hybrid** — `RagxArchitecture.search()` in `ragx/core.py` fuses both:
  `0.6 × keyword/peak + 0.4 × vector/peak`, sorted by score. In
  `retrieval/service.py` the fused candidates are additionally re-ranked by evidence
  quality (0.45), recency (0.35, 30-day half-life), and authority (0.20), plus a 0.05
  graph bonus.
- **Entity-aware routing** — `select_strategy()` picks `direct_graph`,
  `code_context` (code keywords or `File`/`CodeSymbol`/`Repository`/`Commit`/...
  labels), `document_context` (doc keywords or `Document`/`DocumentSection` labels),
  `hybrid` (both), or `none` (no entity selected).

**Traces (GAP-RET-006).** `RetrievalTrace` records each stage as
`{"stage": ..., "candidates": [{"entity_id": ..., "score": ...}], ...detail}` —
inspectable via `trace.to_dict()`. The trace object lives in the retrieval services;
it is not currently exposed as a standalone HTTP endpoint (not runtime-verified).

**Adaptive strategy plugins (FR-RAG-006).** `StrategyRegistry` runs plugins over
phases `retrieve → rerank → synthesize → validate`. Built-ins:
`graph_depth_adaptive` (long/"impact" queries → depth 2–3), `evidence_weight`
("why/evidence/proof/source" queries → boost fields `evidence_key`, `source_ref`),
`domain_focus` (when context has a domain), `freshness_boost`
("recent/latest/new/current/today" → recency weight 2.0, 7-day decay). This is an
in-process plugin API, not an HTTP surface.

---

## 8. Suggestion engine

**Sources:** `packages/eoip/suggest/` (engine, parser, models, router).

**What it does.** Turns an ambiguous natural-language question into **ranked candidate
interpretations** — each a paraphrase, a `QueryPlan` preview, entity bindings with
alternatives, cost tier, confidence, data-coverage note, and a permission pre-check.
Nothing is executed: you pick a candidate and fire it yourself (SR-NLQ-002).

**How to access.**

- `POST /api/v1/suggest` or `POST /api/v1/suggest/interpret` — body
  `{"question": str, "session_id": str?, "user_id": str?, "roles": [str], "limit": 1-20}`.
- `POST /api/v1/suggest/pin` — `{"session_id", "mention", "entity_id"}` pins one
  alternative for the session (SR-NLQ-003).
- `DELETE /api/v1/suggest/pin?session_id=...&mention=...` — remove a pin.
- `GET /api/v1/suggest/intents` — list intent names, cost tiers, answer modes.

**Intents** (`parser._INTENT_PATTERNS`): `lookup`, `traversal`, `impact`,
`ownership`, `change-history`, `coverage`, `temporal`, `aggregation`, `similarity`,
`explain-why`. **Cost tiers**: `fast` (200 ms, depth 1), `moderate` (800 ms, depth 3),
`heavy` (3 s, depth 5), `expensive` (10 s, depth 8).

**Step by step.**

```bash
curl -s -X POST http://localhost:8000/api/v1/suggest \
  -H "Content-Type: application/json" \
  -d '{"question": "what is the blast radius of checkout?",
       "session_id": "sess-42", "user_id": "u-sindhuja", "roles": ["viewer"]}'
```

**Response.** Key fields per candidate (`CandidateInterpretation`): `candidate_id`
(`cand-<n>`), `intent`, `paraphrase`, `plan_preview`, `result_shape`,
`entity_bindings` (each with `resolved`, up to 5 `alternatives` — matched by name,
alias (`source_aliases`), `canonical_id`, or fuzzy substring — `ambiguous`,
`pinned`), `cost_tier`, `estimated_latency_ms`, `confidence` (deterministic formula
with an ambiguity penalty of −0.15), `permissions` (a `PermissionNote` — if a
`user_id` is supplied and the policy enforcer is wired, it reports whether you are
pre-authorized; otherwise `evaluated: false`), `answer_mode`, `source`
(`template` or `llm_assist` — the latter only when the optional External-gate LLM
hook is configured; it is off by default).

**Errors and recovery.** `pin` with an entity that is not a current candidate →
`422 "<id> is not a candidate for '<mention>'"`; missing `session_id` → `422`.
No candidates at all means no intent regex matched — rephrase with words like
"depends on", "who owns", "impact", "as of".

---

## 9. Answer modes

Every suggestion candidate is labeled with one of four answer modes
(`choose_answer_mode`, `suggest/models.py:129`):

- `deterministic` — tier-1 intents computed straight from the graph: `lookup`,
  `traversal`, `impact`, `ownership`, `change-history`, `temporal`, `aggregation`,
  `coverage`. No LLM involved.
- `exploratory` — open-ended or multi-step intents: `explain-why`, `similarity`.
- `report` — long-form aggregation requests.
- `narrated` — everything else; the mode an LLM narrator would serve when configured.

The mode is metadata that tells the UI/user what kind of answer to expect; it does
not itself invoke a model.

---

## 10. Reports

**Sources:** `packages/eoip/reports/` (router, generator, schedule, store).

**What it does.** Renders built-in report templates to HTML, Markdown, or JSON, stores
the artifacts, and supports recurring schedules. PDF/DOCX/PPTX are **External gates**:
they return `501` unless `EOIP_ENABLE_EXTERNAL_REPORT_FORMATS=true` and the
`eoip[reports]` extra is installed.

**How to access.**

- `GET /api/v1/reports` — capability summary.
- `GET /api/v1/reports/templates` — list templates and parameters.
- `POST /api/v1/reports/render?template_id=...&report_format=markdown` — body is a
  `ReportContext` (parameters, optional `graph_stats`; seeded automatically with live
  vertex/edge counts).
- `GET /api/v1/reports/export/{report_id}` — download the stored artifact
  (tenant-scoped; cross-tenant → 403).
- Schedules: `GET`/`POST /api/v1/reports/schedules`, `GET /schedules/due`,
  `POST /schedules/{id}/run`, `POST /schedules/{id}/mark-run`,
  `DELETE /schedules/{id}`.

**Built-in templates** (`BUILTIN_TEMPLATES`): `impact-assessment` (required param
`subject`; `max_hops` default 6), `incident-rca` (required `incident_id`),
`change-risk-review` (required `proposal_id`), `compliance-evidence` (required
`framework`), `executive-brief` (optional `period`).

**Step by step.**

```bash
curl -s -X POST "http://localhost:8000/api/v1/reports/render?template_id=impact-assessment&report_format=markdown" \
  -H "Content-Type: application/json" \
  -d '{"params": {"subject": "service:checkout", "max_hops": 3}}'

curl -s -X POST "http://localhost:8000/api/v1/reports/schedules?template_id=impact-assessment&name=weekly-checkout&recurrence=weekly" \
  -H "Content-Type: application/json" -d '{"subject": "service:checkout"}'
```

**Errors.** `404 Unknown template` (bad `template_id`); `501` for pdf/docx/pptx
without the external-formats flag; `400` for render value errors; `503 Report renderer
unavailable; install eoip[reports]`; `409` if you request an export format different
from the stored artifact.

---

## 11. Model provider configuration

**Source:** `packages/eoip/models/provider.py` (`LocalModelProvider`).

EOIP talks to a local Ollama-compatible model server. Environment variables:

- `EOIP_OLLAMA_MODEL` — model name (e.g. `llama3.1`). **Empty = provider
  "unavailable"** and every model-dependent feature falls back to deterministic
  behavior; nothing breaks.
- `EOIP_OLLAMA_URL` — default `http://local-model:11434` (note: the provider default
  points at the Docker service name `local-model`; the *embedding* provider default
  is `http://localhost:11434` — check your deployment env).

Behavior: `generate()` posts to `{url}/api/chat` (temperature 0 default);
`generate_raw()`/`stream_raw()` use `/api/generate` with a fixed `seed: 7` for
reproducible token counts; `count_tokens()` uses the model's own tokenizer;
`health()` probes `/api/tags`. All transport/parse failures raise `ModelUnavailable`,
which callers (e.g. the GraphRAG pipeline, `retrieval/service.py:_grounded_answer`)
catch and convert to a deterministic fallback (`None` → template answer).

---

## 12. Embeddings health endpoint

**What it does.** `GET /api/v1/health/embeddings` (`apps/api/extended.py:1414`)
reports which embedding backend is active and whether it is reachable.

**Provider selection** (`build_embedding_provider()` in `models/embeddings.py`):
1. `EOIP_EMBEDDING_PROVIDER=sentence-transformers` or `EOIP_SENTENCE_TRANSFORMER_MODEL`
   set → local `SentenceTransformersEmbeddingProvider` (default model
   `all-MiniLM-L6-v2`).
2. `EOIP_OLLAMA_EMBED_MODEL` set or provider `ollama` → `OllamaEmbeddingProvider`
   (default model `nomic-embed-text`, URL from `EOIP_OLLAMA_URL`, default
   `http://localhost:11434`, calls `/api/embed`).
3. Neither → `None`, and the endpoint reports the deterministic fallback.

**Response.** No provider configured:
`{"provider": "hashing", "healthy": true, "dim": 256}`. Ollama configured:
`{"provider": "ollama", "healthy": true|false, "dim": <n>}` (`dim` is 0 until the
first successful embed). The health probe never raises — exceptions become
`healthy: false`. **Recovery:** if `healthy: false`, check that Ollama is running and
`EOIP_OLLAMA_URL` is reachable; meanwhile search keeps working on hashing embeddings.

---

## 13. Model governance endpoints

**Sources:** `packages/eoip/models/governance.py`, routes in
`apps/api/extended.py:1153-1247`.

**Registry & approvals.**
- `GET /api/v1/governance/models` — list registered `ModelEntry` records
  (`model_id`, `version`, `provider`, `capabilities`, `health`, `approved`).
- `POST /api/v1/governance/models` (201) — register a model version.
- `POST /api/v1/governance/models/{model_id}/approval` — approve (404 if unknown).
- `DELETE /api/v1/governance/models/{model_id}/approval` — revoke.

**Prompt templates.** `GET`/`POST /api/v1/governance/templates` — versioned prompt
templates with content hashes (`hash_template`), integrity verification, and an
active-version pointer.

**Kill switch (§49.6).** Feature enum: `rag`, `agents`, `nlq`.
- `GET /api/v1/governance/kill-switch` → `{"global_enabled": bool, "features": {"rag": true, ...}}`.
- `POST /api/v1/governance/kill-switch` — `{"enabled": false, "reason": "..."}`
  disables **all** features (recorded reason; default "disabled via API").
- `POST /api/v1/governance/kill-switch/features/{feature}` — toggle one feature;
  unknown feature → `422` listing valid values.

```bash
curl -s -X POST http://localhost:8000/api/v1/governance/kill-switch/features/rag \
  -H "Content-Type: application/json" -d '{"enabled": false, "reason": "incident EOIP-123 investigation"}'
# → {"feature": "rag", "enabled": false}
```

**Evaluations (§49.5).** `POST /api/v1/governance/evaluate` with a `ModelOutput`
(`response_id`, `model_id`, `text`, `groundedness_score`, `unsafe_action_score`,
`evidence_refs`) returns a `PolicyVerdict`: `passed` plus `reasons`. Defaults:
groundedness threshold **0.8**, unsafe-action threshold **0.1** — a response fails if
`groundedness_score < 0.8` or `unsafe_action_score > 0.1`.

**Incidents (§49.8).** `GET /api/v1/governance/incidents` reads the append-only JSONL
hallucination-incident log (`HallucinationIncidentLog`). There is no public POST
route in this router — incidents are recorded by internal guardrail code paths
(not runtime-verified which paths write it in your build).

---

*End of chapter. All endpoints above are wired in `apps/api/app.py` /
`apps/api/extended.py` and the cited package routers. Example responses are derived
from the response models, not captured from a live server run.*
