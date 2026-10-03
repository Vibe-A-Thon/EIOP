# EOIP benchmark guide

This guide implements the reproducible evidence workflow for `NFR-PERF-001`.
The versioned workload definition is
[`config/benchmarks/mvp-v1.json`](../config/benchmarks/mvp-v1.json); the runner is
[`scripts/benchmark.py`](../scripts/benchmark.py).

## Profiles

| Run | Dataset | Intended use |
|---|---|---|
| `smoke` | 200 work items, 30 commits, 500 files/symbols | Automated CI regression |
| `full` | 2,000 work items, 15,000 commits, 25,000 files/symbols, 5,000 document sections, 223,940 deterministic relationships at seed 42 | Manual baseline evidence |

Both profiles use seed `42`. Every result records the manifest version, exact
dataset counts, Git revision and dirty state, operating system, CPU, memory,
storage declaration, configuration, preparation throughput, client CPU/peak
RSS/storage use, and nearest-rank p50/p95/p99 latency.

## Commands

Fast automated smoke:

```powershell
python -m scripts.benchmark --run smoke --store memory
```

Full algorithmic baseline:

```powershell
$env:EOIP_BENCHMARK_STORAGE_TYPE = 'NVMe SSD' # declare the actual medium
python -m scripts.benchmark --run full --store memory `
  --output docs/benchmarks/YYYY-MM-DD-memory-full.json
```

Authoritative-store run against a dedicated empty HugeGraph deployment:

```powershell
$env:EOIP_HUGEGRAPH_URL = 'http://hugegraph-server:8080'
python -m scripts.benchmark --run full --store configured `
  --prepare-configured --output docs/benchmarks/YYYY-MM-DD-hugegraph-full.json
```

`--prepare-configured` refuses to run unless the configured graph is empty. It
never clears a graph. Use an isolated Compose project/volume, never the normal
development graph. Add `--api-url` and set `EOIP_API_TOKEN` to measure the
authenticated HTTP workload against the same benchmark graph.

## Published 2026-10-03 evidence

The full memory result used the normative data shape on an 8-logical-core,
16-GB Windows host with NVMe SSD. It created 47,140 vertices and 223,940 edges
(271,080 logical mutations) in 6.092 seconds. Measured p95 values were:

| Workload | p50 | p95 | p99 | Target | Result |
|---|---:|---:|---:|---:|---|
| Indexed entity lookup | 0.000 ms | 0.000 ms | 0.001 ms | 500 ms | Pass |
| Query-plan search | 30.735 ms | 39.839 ms | 47.626 ms | 1,000 ms | Pass |
| Bounded five-hop path | 0.448 ms | 0.526 ms | 0.699 ms | 2,000 ms | Pass |
| Bounded impact | 12.951 ms | 16.945 ms | 156.093 ms | 2,000 ms | Pass |

The source result is
[`docs/benchmarks/2026-10-03-memory-full.json`](benchmarks/2026-10-03-memory-full.json).
The API workload was skipped because this run did not use a matching HTTP
deployment. These numbers characterize the in-process algorithmic baseline;
they are not HugeGraph or product performance claims.

An isolated HugeGraph smoke run initially failed the impact objective at
3,814.025 ms p95. The failure is retained in
[`docs/benchmarks/2026-10-03-hugegraph-smoke.json`](benchmarks/2026-10-03-hugegraph-smoke.json).
The cause was repeated REST reads of immutable endpoint identities during edge
decoding. After adding a bounded identity-only cache, the identical clean run
passed with these p95 values:

| Workload | Before | After | Target |
|---|---:|---:|---:|
| Indexed entity lookup | 2.141 ms | 2.695 ms | 500 ms |
| Query-plan search | 115.944 ms | 129.433 ms | 1,000 ms |
| Bounded five-hop path | 138.315 ms | 50.838 ms | 2,000 ms |
| Bounded impact | 3,814.025 ms | 917.343 ms | 2,000 ms |

The passing result is
[`docs/benchmarks/2026-10-03-hugegraph-smoke-after-cache.json`](benchmarks/2026-10-03-hugegraph-smoke-after-cache.json).
Preparation improved from 60.319 to 71.012 logical mutations/second. Both runs
used disposable graphs and the same 774-vertex / 2,007-edge seed-42 dataset.

## Remaining acceptance evidence

`NFR-PERF-001` remains partially open until the `full` profile and HTTP
workload run against an isolated HugeGraph deployment with an exact committed
software revision and container/server
CPU, memory, and storage metrics captured externally. Missed thresholds and
runtime exceptions are emitted as failed workload records and produce a
non-zero process exit; they must not be removed from a published report.

HugeGraph 1.7 was also verified to ignore `UNIQUE` edge indexes for property
queries. EOIP therefore uses an edge-key `SECONDARY` index for lookup and the
physical edge label's `edge_key` sort key for endpoint-scoped uniqueness. A
fresh isolated HugeGraph validation confirmed two identical upserts resolve to
one edge and the indexed lookup returns that edge.

Existing legacy `idx_edge_key_*` definitions are migrated in place. HugeGraph
index deletion and rebuilding are asynchronous, so schema bootstrap explicitly
waits for each task to succeed before recreating or advancing to the next
index. Index replacement preserves graph data.
