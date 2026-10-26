# Chapter 7 — Graph Intelligence

This chapter covers the EOIP platform's analytical layer: the algorithms that answer
questions like *"what breaks if I remove the `checkout` service?"*, *"who knows the
most about this component?"*, and *"what did the graph look like last Tuesday?"*.

Every feature below is backed by real code in `packages/eoip/graph/` and is exposed
over HTTP from `apps/api/app.py` (query API) and `apps/api/main.py` (the composed
application, which wraps `apps/api/app.py`'s `create_app` and adds admin, evolution,
and capsule routes). All endpoints live under `/api/v1/`.

**Honesty notes (not runtime-verified):**

- Examples use the demo tenant `t-001`, issue `EOIP-123`, and service
  `checkout` (canonical id `svc:checkout`). Substitute ids from your own graph;
  use `GET /api/v1/search` to discover them.
- The simulation workspace is **in-memory per API process**
  (`_sim_workspace: dict` in `apps/api/app.py:1185`). Simulations are lost on
  restart and are not shared between worker processes.
- `analysis_type` values `architecture_conformance`, `quality_validation`,
  `test_impact`, and `policy_checks` in the simulation engine return partially
  hard-coded results (see the Simulation section).
- `k_shortest_paths` (Yen's algorithm) exists in `packages/eoip/graph/paths.py`
  but is **not** exposed as an HTTP endpoint; only BFS all-shortest-paths is routed.
- Evolution (versions / as-of / diff / change-journal), capsules, and
  event-consumer admin routes are registered in `apps/api/main.py`, not
  `apps/api/app.py`. If you run only the query app they will 404.

## Index

1. [Structural metrics: centrality suite](#1-centrality-suite)
2. [Blast radius, reverse impact, and PR impact](#2-blast-radius-reverse-impact-pr-impact)
3. [Communities: Leiden / Louvain / Label Propagation, k-core, components, degree distribution](#3-community-and-structure-analysis)
4. [Shortest paths](#4-shortest-paths)
5. [Similarity and link prediction](#5-similarity-and-link-prediction)
6. [What-if engine (single-entity)](#6-what-if-engine)
7. [What-if plan & execute (natural-language scenarios)](#7-whatif-plan-and-execute)
8. [Simulation workspaces: create / mutate / analyze / compare](#8-simulation-workspaces)
9. [Causal intelligence](#9-causal-intelligence)
10. [Surprises and anomaly detection](#10-surprises-and-anomaly-detection)
11. [Stale and orphaned entities](#11-stale-and-orphaned-entities)
12. [Expertise finder](#12-expertise-finder)
13. [Knowledge debt](#13-knowledge-debt)
14. [Process mining](#14-process-mining)
15. [Graph evolution: versions, as-of, diff, change journal, event consumers](#15-graph-evolution)
16. [Bitemporal queries](#16-bitemporal-queries)
17. [Knowledge capsules](#17-knowledge-capsules)
18. [Lens catalog](#18-lens-catalog)
19. [Graph playback](#19-graph-playback)

---

## 1. Centrality Suite

### Centrality metrics (degree / betweenness / closeness / PageRank / eigenvector / Katz / HITS / harmonic)

**What it does.** Computes how "important" or "central" an entity is in the
knowledge graph, using up to eight standard algorithms. Implemented by
`GraphMetricsEngine` in `packages/eoip/graph/metrics.py`.

**How to access.**
- `POST /api/v1/graph/metrics` — degree, in/out degree, betweenness, closeness,
  PageRank for specific entities.
- `POST /api/v1/graph/centrality/full` — all eight algorithms for specific entities.
- `GET /api/v1/graph/statistics` — whole-graph counts (no body).
- `GET /api/v1/graph/schema` — vertex/edge labels present in the graph.

**Step by step** (full centrality for the `checkout` service):

```bash
curl -X POST http://localhost:8000/api/v1/graph/centrality/full \
  -H "Content-Type: application/json" \
  -d '{
    "canonical_ids": ["svc:checkout"],
    "algorithms": ["degree", "betweenness", "closeness", "pagerank",
                   "eigenvector", "katz", "hits", "harmonic"]
  }'
```

`canonical_ids` accepts 1–50 ids; `algorithms` defaults to all eight
(`apps/api/app.py:69-71`).

**Response/result.** A map keyed by canonical id. Each entry
(`CentralityMetrics.to_dict`, `metrics.py:97`) contains:
`canonical_id`, `degree`, `in_degree`, `out_degree`, `betweenness`,
`closeness`, `page_rank`, `eigenvector`, `katz`, `hits_hub`,
`hits_authority`, `harmonic` (floats rounded to 6 decimals).

```json
{
  "svc:checkout": {
    "canonical_id": "svc:checkout",
    "degree": 14, "in_degree": 9, "out_degree": 5,
    "betweenness": 0.083421, "closeness": 0.312500,
    "page_rank": 0.021843, "eigenvector": 0.114022,
    "katz": 0.093411, "hits_hub": 0.051207, "hits_authority": 0.144833,
    "harmonic": 4.916667
  }
}
```

**When to use which.** High *betweenness* = a bridge whose removal fragments the
graph; high *PageRank/eigenvector* = broadly depended upon; high *hits_authority*
= a hub of accumulated knowledge; *harmonic*/*closeness* = reachability.

**Errors and recovery.** Unknown ids simply return zeroed metrics — there is no
404 on these endpoints. A `422` means the payload failed validation (e.g. more
than 50 ids). On an empty graph, scores are `0.0` and
`graph/statistics` returns zero counts.

---

## 2. Blast radius, reverse impact, PR impact

### Blast radius

**What it does.** "If `svc:checkout` changes or fails, what is downstream and
affected?" Breadth-first traversal over dependency edges, with per-depth and
per-type counts plus a risk label (`packages/eoip/graph/metrics.py:147`).

**How to access.** `POST /api/v1/graph/blast-radius`

**Step by step.**

```bash
curl -X POST http://localhost:8000/api/v1/graph/blast-radius \
  -H "Content-Type: application/json" \
  -d '{"canonical_id": "svc:checkout", "max_depth": 4}'
```

`max_depth` is 1–8 (default 4).

**Response/result** (`BlastRadiusResult.to_dict`, `metrics.py:50`):
`target_id`, `total_affected`, `by_depth`, `by_type`, `risk`
(`"low" | "moderate" | "high" | "critical"`), `affected_ids`, and
`affected_details` — each with `canonical_id`, `label`, `path_depth`,
`edge_classes`, `evidence_count`, and a human-readable `why_included`.

### Reverse impact

**What it does.** The mirror question: "who depends on `svc:checkout`?" (upstream
callers). Same request/response shape as blast radius.

**How to access.** `POST /api/v1/graph/reverse-impact` with the same
`{"canonical_id", "max_depth"}` body.

### PR impact

**What it does.** Groups vertices by their `merge_request_id` / `pr_id`
property and maps them onto auto-labeled communities, so you can see which
functional areas a pull request touches (`apps/api/app.py:693`).

**How to access.** `GET /api/v1/graph/pr-impact` (no parameters).

**Errors and recovery.** Blast radius and reverse impact return
`404 "Entity not found"` when nothing is affected **and** the canonical id does
not exist — an existing but isolated entity returns `total_affected: 0` with
HTTP 200. PR impact returns an empty grouping when no vertices carry
`merge_request_id`/`pr_id` properties.

---

## 3. Community and structure analysis

### Community detection (Leiden / Louvain / label propagation)

**What it does.** Finds clusters of densely connected entities
(`CommunityDetectionEngine`, `packages/eoip/graph/community.py`). Leiden
guarantees connected communities, unlike Louvain.

**How to access.** `POST /api/v1/graph/cluster`

**Step by step.**

```bash
curl -X POST http://localhost:8000/api/v1/graph/cluster \
  -H "Content-Type: application/json" \
  -d '{"algorithm": "leiden", "resolution": 1.0, "limit": 1000}'
```

`algorithm` must be one of `label_propagation`, `louvain`, `leiden`
(pattern-validated); `resolution` 0.1–10.0; `limit` up to 50000.

**Response/result** (`CommunityResult.to_dict`, `community.py:29`):
`communities` (list of `{id, members, size}`), `community_count`,
`modularity` (rounded to 6 decimals), `algorithm`. Higher modularity = stronger
community structure.

### k-core decomposition

**What it does.** Peels the graph into shells: which entities survive when all
nodes with degree < k are removed. Answers "what is the dense core of my
knowledge graph?"

**How to access.** `POST /api/v1/graph/k-core` with `{"min_k": 2}`.

**Response/result.** `{"cores": {"2": ["svc:checkout", ...]}, "max_k": 7}`.

### Connected components

**What it does.** Lists disconnected islands in the graph — a quick data-quality
check after ingestion.

**How to access.** `POST /api/v1/graph/components` with `{"limit": 50}`.

**Response/result.** `components`: `[{id, size, members}]` (members capped at
200 per component), plus `total_components`.

### Degree distribution

**What it does.** Histogram of node degrees — useful for spotting hub-and-spoke
vs. uniform structure.

**How to access.** `POST /api/v1/graph/degree-distribution` (no body required;
the route takes no payload).

**Response/result.** `{"distribution": {"<degree>": <count>}, "total_nodes": N}`.

**Errors and recovery.** All four endpoints are read-only and safe to re-run.
On an empty graph: clustering returns `community_count: 0`, k-core returns
`max_k: 0`, components returns `total_components: 0`. A `422` signals an
invalid `algorithm` value or out-of-range numeric field.

---

## 4. Shortest paths

### All shortest paths (BFS)

**What it does.** Finds every shortest path between two entities
(`GraphPathFinder.all_shortest_paths`, `packages/eoip/graph/paths.py:44`).
Answers "how is requirement `EOIP-123` connected to service `checkout`?"

**How to access.** `POST /api/v1/graph/shortest-paths`

**Step by step.**

```bash
curl -X POST http://localhost:8000/api/v1/graph/shortest-paths \
  -H "Content-Type: application/json" \
  -d '{"source_id": "issue:EOIP-123", "target_id": "svc:checkout",
       "max_paths": 5, "max_length": 10}'
```

`max_paths` 1–20, `max_length` 2–20.

**Response/result.** `{"paths": [["issue:EOIP-123", "doc:design-7", "svc:checkout"]], "count": 1}`.

**Errors and recovery.** Disconnected or unknown endpoints return
`{"paths": [], "count": 0}` (no 404). Yen's k-shortest-paths
(`k_shortest_paths`, `paths.py:112`) is implemented in the library but **not
exposed over HTTP** — use `max_paths` with BFS instead.

---

## 5. Similarity and link prediction

### Node similarity (Jaccard / Adamic-Adar / common neighbors)

**What it does.** Scores entities with similar neighborhoods — "which services
look like `checkout`?" (`SimilarityEngine`, `packages/eoip/graph/similarity.py`).

**How to access.** `POST /api/v1/graph/similarity`

```bash
curl -X POST http://localhost:8000/api/v1/graph/similarity \
  -H "Content-Type: application/json" \
  -d '{"canonical_id": "svc:checkout", "algorithm": "jaccard", "limit": 10}'
```

`algorithm`: `jaccard | adamic_adar | common_neighbors`; `limit` 1–50.

**Response/result.** List of `{canonical_id, score, common_neighbors}`, sorted
by score.

### Link prediction

**What it does.** Suggests edges that *should* exist but don't — only
non-adjacent pairs are returned (`similarity.py:169`).

**How to access.** `POST /api/v1/graph/link-prediction` with
`{"canonical_id": "svc:checkout", "algorithm": "common_neighbors", "limit": 10}`.

**Response/result.** List of `{source_id, target_id, score, algorithm}`.

**Errors and recovery.** Unknown `canonical_id` returns `[]` (link prediction)
or an empty list (similarity) rather than an error. Verify the id with
`GET /api/v1/search?q=checkout` first.

---

## 6. What-if engine

### Single-entity removal / isolation

**What it does.** Simulates removing an entity (or cutting all its edges) and
reports the fallout: broken edges, orphaned entities, whether the graph splits
into more components (`WhatIfEngine`, `packages/eoip/graph/whatif.py`).

**How to access.** `POST /api/v1/graph/what-if`

```bash
curl -X POST http://localhost:8000/api/v1/graph/what-if \
  -H "Content-Type: application/json" \
  -d '{"canonical_id": "svc:checkout", "action": "remove"}'
```

`action`: `remove | isolate` (`isolate` cuts edges but keeps the node).

**Response/result** (`WhatIfResult.to_dict`, `whatif.py:31`): `canonical_id`,
`action`, `broken_edges`, `affected_neighbors`, `orphaned_entities`,
`broken_paths`, `centrality_changes`, `component_split` (bool),
`new_components`.

**Errors and recovery.** This is a pure simulation — nothing is written to the
store. An unknown id produces a zeroed result; confirm existence first.

---

## 7. Whatif plan and execute

**What it does.** Parses a semi-natural-language change intent into a mutation
plan, shows you a confirmation summary (plan), then executes it inside a
disposable simulation workspace (execute). Supported intent patterns
(`whatif.py:200`): `remove <label> <target>`, `delete ...`, `add <label> named
<name>`, `connect <src> to <tgt> via <EDGE>`, `disconnect <src> from <tgt>`,
`modify <target> set k=v, ...`.

**How to access.**
- `POST /api/v1/whatif/plan` — dry run, returns confirmation summary.
- `POST /api/v1/whatif/execute` — executes in a sandbox and analyzes.
- `POST /api/v1/query/what-if` — combined alias; pass `"execute": true` to run.

**Step by step.**

```bash
# 1. Plan
curl -X POST http://localhost:8000/api/v1/whatif/plan \
  -H "Content-Type: application/json" \
  -d '{"intent": "remove Service svc:checkout"}'

# 2. Execute (sandboxed — never touches the base store)
curl -X POST http://localhost:8000/api/v1/whatif/execute \
  -H "Content-Type: application/json" \
  -d '{"intent": "remove Service svc:checkout"}'
```

**Response/result.** Plan: `{intent, description, mutations, mutation_count,
requires_confirmation, breakdown: {additions, removals, modifications}}`.
Execute: `{simulation_id, intent, mutation_results, analysis,
affected_by_category, manifest}`.

**Errors and recovery.** Missing `intent` → `400 "intent required"`.
An intent that matches no pattern yields `description: "Unrecognised intent:
..."` with `mutation_count: 0` — rephrase using the patterns above.

---

## 8. Simulation workspaces

**What it does.** A sandboxed overlay on top of the real graph: create a named
simulation, apply mutations, run analyses, compare to baseline, and fetch a
reproducible manifest (`SimulationWorkspace`, `packages/eoip/graph/simulation.py`).
Nothing touches the base store. **Note:** the workspace is in-memory
(`apps/api/app.py:1185`) — restart loses it.

**How to access.**

| Action | Endpoint |
|---|---|
| Create empty | `POST /api/v1/simulation/create` |
| Create + mutate in one call | `POST /api/v1/simulations` |
| List | `GET /api/v1/simulation/list` |
| Get manifest | `GET /api/v1/simulations/{sim_id}` or `GET /api/v1/simulation/{sim_id}/manifest` |
| Mutate | `POST /api/v1/simulation/{sim_id}/mutate` |
| Analyze | `GET /api/v1/simulation/{sim_id}/analyze?analysis_type=impact` |
| Compare to base | `GET /api/v1/simulation/{sim_id}/compare` |

**Step by step.**

```bash
# 1. Create and mutate in one shot
curl -X POST http://localhost:8000/api/v1/simulations \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Retire checkout v1",
    "mutations": [
      {"kind": "remove_vertex", "target_id": "svc:checkout"},
      {"kind": "add_vertex", "label": "Service",
       "properties": {"canonical_id": "svc:checkout-v2", "name": "checkout-v2"}}
    ]
  }'
# → {"simulation_id": "sim-...", "mutation_results": [...], "manifest": {...}}

# 2. Analyze impact
curl "http://localhost:8000/api/v1/simulation/sim-XXXX/analyze?analysis_type=impact"

# 3. Compare against baseline
curl "http://localhost:8000/api/v1/simulation/sim-XXXX/compare"
```

Mutation `kind` values: `add_vertex`, `remove_vertex`, `add_edge`,
`remove_edge`, `modify_vertex` (plus `remove_edge_between` internally).

**Response/result.** Analyze returns `base`/`simulated`/`delta` vertex & edge
counts, `mutations_applied`, `assumptions`, `uncertainty` (0.05), `evidence`,
and — for `impact`/`blast_radius` — `removed_entities`, `affected_entities`,
`blast_radius_score`. Compare returns counts of added/removed vertices and
edges. Manifest: `{simulation_id, created_at, base_snapshot, mutations,
results}`.

**Errors and recovery.** Unknown `sim_id` → `404 "Simulation not found"` (or
`{"error": "Simulation <id> not found"}` from analyze/compare). No workspace
yet → `404 "No simulation workspace"`. **Caveat (not runtime-verified):**
`analysis_type` values `architecture_conformance`, `quality_validation`,
`test_impact`, and `policy_checks` return hard-coded pass/score values
(`simulation.py:390-415`); only `impact`/`blast_radius` compute real results.

---

## 9. Causal intelligence

**What it does.** Time-aware reasoning (`packages/eoip/graph/causal.py`): which
neighboring entities changed around the same time as an incident, whether a
candidate cause actually precedes its effect, and ranked cause hypotheses.

**How to access & examples.**

```bash
# Temporal correlations around an entity (default 24h window)
curl -X POST http://localhost:8000/api/v1/causal/correlations/incident:INC-42 \
  -H "Content-Type: application/json" -d '{"time_window_hours": 24}'

# Check whether cause precedes effect with supporting evidence
curl -X POST http://localhost:8000/api/v1/causal/prerequisites \
  -H "Content-Type: application/json" \
  -d '{"cause_cid": "deploy:D-91", "effect_cid": "incident:INC-42"}'

# Generate ranked hypotheses for an incident
curl -X POST http://localhost:8000/api/v1/causal/hypotheses/incident:INC-42 \
  -H "Content-Type: application/json" -d '{"time_window_hours": 24}'
```

**Response/result.** Correlations: `{entity, correlations: [{canonical_id,
label, timestamp, temporal_distance_seconds, direction}]}`. Hypotheses
(`CausalHypothesis.to_dict`): `hypothesis_id`, `cause`, `effect`, `status`
(starts as `"CORRELATION"`), `confidence`, `temporal_distance_seconds`,
`evidence`, `alternatives`, `reviewer_notes`. Prerequisites: `{valid, reason,
...}` — `valid: false, reason: "entity_not_found"` with a `missing` list when
ids don't resolve.

**Errors and recovery.** `400 "cause_cid and effect_cid required"` for the
prerequisites endpoint without both ids. Entities without timestamps simply
don't correlate — check that ingestion populated timestamp properties.

---

## 10. Surprises and anomaly detection

### Graph surprises

**What it does.** Ranks structurally unexpected edges (connections that
"shouldn't" exist) and unexpected absences (edges that should exist but don't)
— `SurpriseDetector.summary`, `packages/eoip/graph/surprise.py:170`.

**How to access.** `POST /api/v1/graph/surprises` with `{"limit": 20}`.

**Response/result.** `{surprising_edges, unexpected_absences, counts}`; each
item has `kind`, `score`, `explanation`, `source_id`, `target_id`,
`edge_id`, `edge_label`, `source_label`, `target_label`.

### Anomaly detection

**What it does.** Three detectors (`packages/eoip/graph/anomaly.py`):
`degree_zscore` (hub outliers by z-score), `dense_subgraph` (suspicious clumps),
`missing_edges` (expected relationships absent).

**How to access.** `POST /api/v1/graph/anomalies`

```bash
curl -X POST http://localhost:8000/api/v1/graph/anomalies \
  -H "Content-Type: application/json" \
  -d '{"algorithms": ["degree_zscore", "dense_subgraph", "missing_edges"],
       "threshold": 2.0}'
```

`threshold` 1.0–5.0 (z-score cutoff for `degree_zscore`).

**Response/result.** List of `{canonical_id, anomaly_type, score, details}`.

**Errors and recovery.** An empty list means "no anomalies at this threshold" —
lower `threshold` toward 1.0 to widen the net.

---

## 11. Stale and orphaned entities

**What it does.** Data-hygiene sweeps: orphaned = entities with no relationships;
stale = entities not modified within a time window.

**How to access & examples.**

```bash
# Orphaned entities, optionally filtered by type
curl "http://localhost:8000/api/v1/graph/orphaned?entity_types=Service,API"

# Entities stale for more than 168 hours (default; max 8760)
curl "http://localhost:8000/api/v1/graph/stale?threshold_hours=168"
```

**Response/result.** Orphaned: `{orphaned: [{canonical_id, anomaly_type, score,
details}], count}`. Stale: `{stale: [...], count, partial}` — `partial: true`
means the scan hit its internal limit and results may be incomplete; re-run with
a narrower threshold or after ingestion completes.

---

## 12. Expertise finder

**What it does.** "Who should I ask about `svc:checkout`?" Ranks `Person`
vertices by `AUTHORED_BY` (weight 1.0) and `ASSIGNED_TO` (weight 0.7) evidence
on neighboring artifacts, decayed by recency
(`find_experts`, `packages/eoip/graph/expertise.py:42`; GAP-REC-001).

**How to access.** `GET /api/v1/experts/{canonical_id}`

```bash
curl http://localhost:8000/api/v1/experts/svc:checkout
```

**Response/result.** `{component_cid, experts: [{person_cid, display_name,
score, evidence: [{basis, via, recency}]}]}` — ranked, top 10.

**Errors and recovery.** Unknown component → `404 "entity not found: ..."`.
Empty `experts` list means no authorship/assignment edges were ingested — check
your identity resolution, not the endpoint. Related:
`GET /api/v1/knowledge/freshness?stale_days=90` flags documents whose referenced
entities changed long after capture (GAP-FRESH-001..005).

---

## 13. Knowledge debt

**What it does.** Runs twelve built-in detection rules — unowned services,
undocumented APIs, unlinked requirements/implementations, stale documents,
unresolved identities, broken provenance, low confidence, missing tests,
missing architecture mapping, unknown production owner, stale runbooks
(`detect_knowledge_debt`, `packages/eoip/graph/knowledge_debt.py:181`).

**How to access.** `GET /api/v1/knowledge/debt` (alias: `GET /api/v1/knowledge-debt`).

**Response/result.** `{findings: [...], total_debt, by_category, by_dimension,
multidimensional, categories_checked}`.

### Knowledge SLOs

**What it does.** Evaluates thresholds over graph-wide metrics (evidence
coverage, orphan rate, connectivity).

**How to access.**
- `POST /api/v1/knowledge/slo` with `{"rules": [{"id": "...", "metric":
  "evidence_coverage", "threshold": 0.8, "operator": "gte", "description": "..."}]}`
- `GET /api/v1/knowledge-slos` — evaluates three built-in rules
  (provenance-coverage ≥ 0.8, orphan-rate ≤ 0.1, connectivity ≥ 0.75).

**Errors and recovery.** `POST /knowledge/slo` with an empty `rules` list →
`400 "rules required"`. Valid operators: `gte`, `lte` (see
`parse_slo_rules`, `knowledge_debt.py:477`).

---

## 14. Process mining

**What it does.** Reconstructs how work actually flows (e.g. issue status
transitions for `EOIP-123`) from graph event data, discovers frequent paths,
and reports deviations from a designed flow
(`packages/eoip/graph/process_mining.py`).

**How to access & examples.**

```bash
curl "http://localhost:8000/api/v1/process/cases?source_label=WorkItem"
curl http://localhost:8000/api/v1/process/paths
curl -X POST http://localhost:8000/api/v1/process/deviations \
  -H "Content-Type: application/json" \
  -d '{"designed_steps": ["Open", "In Progress", "In Review", "Done"]}'
```

**Response/result.** Cases: `{cases: [{case_id, events, length}], total}` (cap
100). Paths: `{total_cases, unique_paths, paths: [{path, count, frequency}],
transitions: [{from, to, count}]}`. Deviations: `{cases (cap 50),
observed_paths, comparison: {designed_steps, deviations, deviation_count,
bottlenecks, conformance_rate}}`. Without `designed_steps` the comparison is
empty and `conformance_rate` is 1.0.

---

## 15. Graph evolution

**What it does.** Every change to the graph is versioned and journaled
(`GraphEvolutionEngine` + `ChangeJournal`, `packages/eoip/graph/evolution.py`),
so you can time-travel and audit. These routes live in `apps/api/main.py`.

**How to access & examples.**

```bash
# Graph versions
curl "http://localhost:8000/api/v1/graph/versions?limit=100"

# Graph state at a point in time (ISO-8601 required)
curl "http://localhost:8000/api/v1/graph/as-of?at=2026-01-15T00:00:00&limit=500"

# Diff between two points
curl "http://localhost:8000/api/v1/graph/diff?from=2026-01-01T00:00:00&to=2026-02-01T00:00:00"

# Change journal (cursor-paginated)
curl "http://localhost:8000/api/v1/change-journal?after=0&limit=100"
```

**Response/result.** As-of: `{at, entities: [...], relationships: [...]}`.
Diff: `{from, to, entities: {added, removed, modified}, relationships: {...}}`.
Journal events (`SemanticChangeEvent`): `cursor`, `graph_version`,
`change_kind` (`CREATE|UPDATE|DELETE|LATE_EVENT`), `target_kind`
(`ENTITY|RELATIONSHIP`), `target_id`, `source_event_id`, `observed_at`,
`details`, `before_state`, `after_state`, `previous_hash`, `entry_hash`
(hash-chained for tamper evidence).

**Errors and recovery.** Non-ISO `at`/`from`/`to` → `422`. Empty `entities`/
`relationships` means no revisions existed at that timestamp.

### Event consumers

**What it does.** Background consumers project journal events into derived
artifacts: quality recalculation, cache invalidation, admin timeline
(`packages/eoip/graph/consumers.py`). They normally run in the worker; admins
can inspect and trigger them.

**How to access.**
- `GET /api/v1/admin/event-consumers` — consumer state files.
- `POST /api/v1/admin/event-consumers/run` — run all default consumers now.
- `GET /api/v1/admin/timeline?limit=100` — the projected admin timeline.

**Errors and recovery.** Consumer run failures → `500 "Consumer run failed:
..."`; check the data-root state directory permissions.

---

## 16. Bitemporal queries

**What it does.** Separates *valid time* (when something was true in the real
world) from *system time* (when the graph learned it) — the basis for
late-arriving-event handling (`BitemporalQueryEngine`,
`packages/eoip/graph/bitemporal.py`). Mounted as a router at prefix
`/api/v1/graph/bitemporal` (all POST).

**How to access & examples.**

```bash
# What did the graph know at a system time?
curl -X POST http://localhost:8000/api/v1/graph/bitemporal/known-at \
  -H "Content-Type: application/json" -d '{"known_at": "2026-01-15T00:00:00"}'

# What was valid at a real-world time?
curl -X POST http://localhost:8000/api/v1/graph/bitemporal/valid-at \
  -H "Content-Type: application/json" -d '{"valid_at": "2026-01-15T00:00:00"}'

# Both coordinates, topology, and diff
curl -X POST http://localhost:8000/api/v1/graph/bitemporal/slice \
  -H "Content-Type: application/json" \
  -d '{"valid_at": "2026-01-15T00:00:00", "known_at": "2026-02-01T00:00:00"}'
curl -X POST http://localhost:8000/api/v1/graph/bitemporal/topology \
  -H "Content-Type: application/json" \
  -d '{"valid_at": "2026-01-15T00:00:00", "known_at": "2026-02-01T00:00:00"}'
curl -X POST http://localhost:8000/api/v1/graph/bitemporal/diff \
  -H "Content-Type: application/json" \
  -d '{"from_coordinate": {"valid_at": "2026-01-01T00:00:00"},
       "to_coordinate":   {"valid_at": "2026-02-01T00:00:00"}}'
```

**Response/result.** Slice/topology return `BitemporalSlice` /
`BitemporalTopology` models (revisions + historical edges); diff returns
`BitemporalDiff` with per-item `added`/`removed` sets (`ItemDiff`). Empty
results mean no revision records carried bitemporal windows — this depends on
ingestion writing `valid_from`/`valid_to` properties (not runtime-verified for
all connectors).

---

## 17. Knowledge capsules

**What it does.** Builds a bounded, content-hashed, reproducible export of a
subgraph rooted at given entities — a shareable "evidence packet"
(`KnowledgeCapsuleService`, `packages/eoip/graph/capsules.py`; G2-CAP-001..006).
Routes are in `apps/api/main.py`.

**How to access & example.**

```bash
curl -X POST http://localhost:8000/api/v1/capsules \
  -H "Content-Type: application/json" \
  -d '{"name": "checkout-review", "root_entities": ["svc:checkout"],
       "max_depth": 2, "include_evidence": true, "result_limit": 500}'

curl http://localhost:8000/api/v1/capsules            # list manifests
curl http://localhost:8000/api/v1/capsules/checkout-review   # fetch one
```

**Response/result.** Create (HTTP 201): `{capsule_id, manifest, entities,
relationships, evidence_refs, truncated}` — `truncated: true` means
`result_limit` cut the traversal short. Optional definition fields: `domains`,
`trust_threshold` (edges below the threshold are excluded).

**Errors and recovery.** Unknown root entity → `404`. Unknown capsule name on
GET → `404 "Capsule not found"`.

---

## 18. Lens catalog

**What it does.** Twenty purpose-built projections of the same graph —
Search, Graph, Evidence, Impact, Timeline, Change, Architecture, Runtime,
Requirement, Trust, Security, Release, Process, Knowledge Health, Simulation,
Agent, Decision, API, Test, Ontology (`LENS_CATALOG`,
`packages/eoip/graph/lens.py:49`).

**How to access.**
- `GET /api/v1/lens/catalog` — list lenses (`{id, name, description}`).
- `POST /api/v1/lens/{lens_id}` — fetch lens data with an optional
  `KnowledgeContext` body (`query`, `entity_cid`, `graph_version`, `as_of`,
  `domains`, `trust_threshold`, `filters`).

```bash
curl -X POST http://localhost:8000/api/v1/lens/impact \
  -H "Content-Type: application/json" -d '{"entity_cid": "svc:checkout"}'
```

**Errors and recovery.** Unknown lens id does not 404 — it returns
`{"error": "Unknown lens: <id>", "available": [...]}`; pick an id from the
catalog.

---

## 19. Graph playback

**What it does.** Reconstructs a chronological event stream radiating from a
root entity ("how did incident INC-42 unfold?"), plus an evidence side panel
and a timeline export (`packages/eoip/graph/playback.py`).

**How to access & examples.**

```bash
curl -X POST http://localhost:8000/api/v1/playback/stream \
  -H "Content-Type: application/json" \
  -d '{"root_cid": "issue:EOIP-123", "max_depth": 3, "max_events": 200}'

curl -X POST http://localhost:8000/api/v1/playback/evidence \
  -H "Content-Type: application/json" -d '{"root_cid": "issue:EOIP-123"}'

curl -X POST http://localhost:8000/api/v1/playback/export \
  -H "Content-Type: application/json" \
  -d '{"root_cid": "issue:EOIP-123", "format": "json"}'
```

**Response/result.** Stream: `{root, root_label, events: [{canonical_id,
label, name, timestamp, depth, properties}], total_events}` sorted by
timestamp. Evidence panel: `{entity, label, evidence: [{evidence_id,
source_system, source_ref, method, confidence, captured_at}], ingestion_runs,
creation_status}`.

**Errors and recovery.** Missing `root_cid` → `400 "root_cid required"`.
Unknown root → HTTP 200 with `{"root": ..., "events": [], "error": "Entity not
found"}` — check the body, not just the status code.

---

## Related endpoints not covered here

Twin state & business linkage (`/api/v1/twin/...`), conformance rules
(`/api/v1/conformance/...`), provenance queries (`/api/v1/query/why`,
`/why-not`, `/what-changed`, `/context`), and the knowledge firewall
(`/api/v1/knowledge/firewall/inspect`) are documented in their own chapters.
