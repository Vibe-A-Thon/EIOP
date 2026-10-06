# EOIP High-Availability Deployment

Deployment artifacts for running EOIP with redundancy: Helm chart
(`deploy/helm/eoip/`, G2-DEPLOY-HELM) and a Compose HA profile
(`deploy/docker-compose.ha.yml`, G2-DEPLOY-HA). See also
`docs/docker-local.md` for the single-node baseline and
`deploy/docker-compose.yml` for the primary stack.

## Topology

```
                ┌──────────────┐
 clients ──────▶│  nginx api-lb │ (least_conn, health-checked)
                └──────┬───────┘
              ┌────────┴────────┐
              ▼                 ▼
        eoip-api-1         eoip-api-2        stateless, any replica serves
              │                 │
              └────────┬────────┘
                       ▼
   eoip-worker-1 ═══ eoip-worker-2   leader lease (EOIP_LEASE_PATH) on
     (standby)        (lease holder)  shared volume; only holder runs
                                      single-writer jobs
                       │
                       ▼
        HugeGraph  (standalone default /
                    PD + Store distributed — see §HugeGraph)
```

Key invariants (§10 of `packages/eoip/ha.py`):

- API replicas are stateless; sessions, auth, and job state live in the
  graph store and durable job queue, not in process memory.
- Exactly one worker holds the leader lease at a time; on node loss the
  lease expires after its TTL (default 30 s) and the standby steals it.
- The lease TTL must exceed the maximum expected GC/pause of the holder.

## Compose HA profile

```bash
# from deploy/ — .env via scripts/docker.ps1
docker compose -f docker-compose.ha.yml up -d
docker compose -f docker-compose.ha.yml --profile hugegraph-distributed up -d hugegraph-pd hugegraph-store-1 hugegraph-store-2 hugegraph-lb
```

Services: `api-lb` (nginx), `eoip-api-1/2`, `eoip-mcp`, `eoip-worker-1/2`
(shared `worker-leases` volume, `EOIP_LEASE_PATH=/leases/worker.lock`),
and HugeGraph placeholders under the `hugegraph-distributed` profile.

## Helm

```bash
helm install eoip deploy/helm/eoip \
  --set config.existingSecret=eoip-secrets \
  --set image.registry=registry.example.com/team \
  --set image.tag=0.5.0
```

- `templates/deployment.yaml` renders api / mcp / worker Deployments.
- `templates/hpa.yaml` autoscales the API tier (requires metrics-server).
- `templates/configmap.yaml` renders `graph-store.yaml`
  (`graphBackend: hugegraph|neptune|memory`).
- `templates/pvc.yaml` provisions the shared worker volume — **must be
  ReadWriteMany** for worker HA.
- `values.yaml` exposes `hugegraph`, `neptune`, and `ollama` config blocks;
  pod anti-affinity for api/worker is on by default.
- HugeGraph itself is not deployed by the chart; point `hugegraph.url` (or
  `neptune.url`) at an existing backend.

## RPO / RTO targets

| Failure                    | RPO            | RTO      | Mechanism                                   |
|----------------------------|----------------|----------|---------------------------------------------|
| API replica loss           | 0              | < 10 s   | nginx fails over to healthy replica         |
| Worker loss                | 0 (durable queue, idempotent replay) | ≤ lease TTL + startup (~60 s) | lease expiry + standby steal |
| Single node loss (Compose) | 0 (replicated volumes) | manual   | restart stack on surviving node             |
| Graph store loss           | last backup    | restore time | `scripts/backup.py --bundle`; see `docs/deployment-verification.md` |

## Rolling restart procedure

1. Drain: stop new job submissions (workers keep consuming the queue).
2. Restart API tier one replica at a time; wait for
   `/health/ready` on the new replica before restarting the next. The nginx
   `fail_timeout` keeps traffic off booting replicas.
3. Restart the standby worker first; verify the lease holder is unaffected
   (holder changes only on lease expiry — expected only if the holder was
   restarted).
4. Rolling-recreate graph store nodes only per the HugeGraph section below.

## Capacity planning

- API: ~1 CPU / 512 Mi per replica baseline; scale on CPU ≥ 70 %. HPA range
  2–8 replicas is the chart default.
- Worker: size for the largest ingestion batch; single-writer jobs do not
  scale horizontally — add workers for standby, not throughput.
- Graph store: RocksDB working set + indexes should fit in available memory;
  run `scripts/benchmark.py` before production (GAP-HG-008).
- Ollama (optional `ai` profile): model size + ~2 Gi per concurrent request.

## Failure scenarios

- **API replica crash:** nginx `max_fails=3 fail_timeout=10s` removes it;
  no client-visible interruption beyond in-flight requests.
- **Worker crash mid-job:** durable job queue replays idempotently after
  failover (see `apps/worker/main.py`).
- **Split-brain risk:** the lease is advisory; a shared filesystem that
  loses `O_CREAT|O_EXCL` atomicity (certain network mounts) can allow two
  holders. Keep the lease TTL conservative (≥ 30 s) and prefer a
  node-local or strongly-consistent volume.
- **Graph store node loss:** standalone HugeGraph has no failover — RPO =
  last backup. Use the distributed topology for HA.

## Standalone → distributed HugeGraph migration (GAP-HG-006)

GAP-HG-006 (migration playbook) is partially covered here; the full
procedure requires HugeGraph enterprise/infra validation before use.

1. Provision the PD + Store cluster (`--profile hugegraph-distributed` in
   the Compose file is a documented placeholder).
2. Bulk-export from the standalone instance (`scripts/backup.py --bundle`).
3. Bulk-load into the distributed cluster (GAP-HG-004 bulk-loader path).
4. Repoint `EOIP_HUGEGRAPH_URL` to `hugegraph-lb:8080` and restart workers,
   then the API tier.
5. Verify with `scripts/smoke_test.py` and `scripts/verify_restore.py`.

## HugeGraph cluster / sharding notes (GAP-PERF-001/002, G2-SCALE-SHARD)

- The target topology is HugeGraph PD (placement driver) + multiple Store
  nodes with graph-partition sharding across stores, fronted by
  `hugegraph-lb`.
- Expected benefit: horizontal read/write scaling past a single RocksDB
  instance and partition-level parallelism for analytics
  (`packages/eoip/agents/graph_analytics.py`).
- **Honest caveat:** the PD/Store images and sharding configuration are
  **not validated in this repo**. The `hugegraph-distributed` Compose
  profile is a shape placeholder, and the Helm chart only consumes a graph
  endpoint. Treat sharding numbers (partitions per store, PD failover) as
  requiring HugeGraph enterprise/infra validation and a capacity benchmark
  (GAP-HG-008) before production.
