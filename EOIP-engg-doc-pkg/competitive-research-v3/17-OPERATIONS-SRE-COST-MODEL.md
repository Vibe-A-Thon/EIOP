# 17 — Operations, SRE & Cost Model (KnowGridFlow / EOIP)

| Field | Value |
|---|---|
| Document | 17-OPERATIONS-SRE-COST-MODEL.md |
| Status | **PROPOSED operations model.** No capacity test, restore drill, or air-gap install has completed in this research programme (GAP-42, GAP-21); figures below are sizing targets and cost-model inputs, not measured results. Every number carries the same PROPOSED status as `15-VALIDATION-BENCHMARK-PLAN.md`. |
| Scope basis | `01-SYSTEM-BASELINE.md` §3 (verified architecture), `01a-BASELINE-DELTA-HEAD.md` (processing/tenancy/egress deltas), `deploy/` (Compose, Helm, Argo CD as found in the repository), `02-TECHNOLOGY-REGISTRY.md` §3 (licence-driven TCO inputs), A-08/A-10 in `22-OPEN-QUESTIONS-AND-ASSUMPTIONS.md` |
| Prior placeholder notice | A pass on 2026-10-19 wrote an earlier version of this file with a runnable-looking air-gap script and a TCO table presenting dollar figures for Palantir/Stardog/Neo4j Aura as fact. This version replaces it in full; vendor pricing is cited only where a deep dive records it, and every "$0" EOIP line is relabelled as a modeled input, not a claim. |

---

## 1. Sizing tiers

Per A-10 (`22-OPEN-QUESTIONS-AND-ASSUMPTIONS.md`): "scale target for the one-node tier: up to ~10M nodes / ~50M edges per tenant; larger needs distributed tiers." This is a stated *target*, not a measured capacity — BM-02 (`15-VALIDATION-BENCHMARK-PLAN.md`) is the benchmark that would confirm or revise it, and BM-02 has not run.

| Tier | Workload scope (target, unmeasured) | vCPU | RAM | Storage | Backend(s) in scope | Status |
|---|---|---|---|---|---|---|
| **Small (one-node)** | Developer workstation / pilot tenant, up to ~1M nodes / ~5M edges | 8 | 32 GB | 250 GB NVMe | HugeGraph (RocksDB, primary per config), Neo4j Community as an alternative, embedded vector/search layers (`retrieval/tenant_index.py`) | Compose-deployable today (`deploy/docker-compose.yml`); capacity unmeasured (GAP-30) |
| **Medium (one-node, A-10 target)** | Departmental tenant, up to ~10M nodes / ~50M edges per tenant | 32 | 128 GB | 1 TB NVMe | HugeGraph or Neo4j, same one-node architecture scaled up | This is the A-10 target line, not a tested ceiling; BM-02 Tier 3 (10M+ nodes) is the benchmark that would confirm it holds |
| **Large (distributed, needed beyond A-10)** | Multi-tenant platform or single tenant beyond ~10M/~50M | 64+ | 256+ GB | 5+ TB NVMe, multi-node storage | HugeGraph with a distributed storage backend (HBase/Cassandra, per `02-TECHNOLOGY-REGISTRY.md`), or Neo4j/Neptune clustering | No distributed-storage configuration is evidenced in `deploy/`; this row is a target architecture, not a shipped one |

A single-node deployment today runs API, worker, MCP, web, HugeGraph, Neo4j, Ollama, and Prometheus containers together per `deploy/docker-compose.yml` (confirmed in `01-SYSTEM-BASELINE.md` §3); `deploy/docker-compose.ha.yml` and `deploy/helm/eoip/` exist for a higher-availability or Kubernetes-managed deployment but their capacity under load is equally unmeasured (BL-50's "scripts, live-unverified" status extends to the HA compose file and Helm chart — no BL row claims they have been load-tested).

## 2. Deployment

- **Docker Compose (reference deployment):** `deploy/docker-compose.yml` (core services), `deploy/docker-compose.ha.yml` (HA variant), `deploy/docker-compose.observability.yml` (Prometheus/OTel), `deploy/docker-compose.acceptance.yml` and `deploy/docker-compose.dlq-acceptance.yml` (test-only compose files). `deploy/nginx/api-lb.conf` and `deploy/nginx/hugegraph-lb.conf` provide a load-balancer config for the API and HugeGraph Gremlin Server front doors.
- **Helm / Kubernetes:** `deploy/helm/eoip/` exists as a chart; `deploy/argocd/application.yaml` provides a GitOps deployment definition; `deploy/environments/production` and `deploy/environments/staging` hold environment-specific overlays. No evidence in this research run that the Helm chart has been deployed to a live cluster and load-tested (same "files exist, live-unverified" status as the rest of `deploy/`, per `01-SYSTEM-BASELINE.md` §4 "Deployment" row).
- **Graph backend images:** `hugegraph/hugegraph:1.7.0` and `neo4j:5-community` are the pinned images in Compose; `deploy/graphdb/eoip-repo.ttl` adds a GraphDB Free repository configuration (per commit 98b8fb2's CI service addition, noted in the git log at the top of this package). Neptune has no local image — it is a managed AWS service and is excluded from every air-gap deployment (see §5).
- **Model serving:** `ollama/ollama:0.12.3` is pinned in Compose; GAP-36/INV-SELF-10 (`16-SECURITY-PRIVACY-THREAT-MODEL.md` T-10) flags this pin as old, root, and unauthenticated — an operational defect to fix before any production sizing recommendation is finalized, independent of capacity.
- **Local model hardware reference:** `deploy/hardware/llm-reference-configs.json` and `deploy/hardware/models/` exist as a reference-configuration catalogue; this research run did not re-verify its contents against a live model-serving benchmark (BM-14).

## 3. Backup, restore, and point-in-time recovery (BM-16)

- **What exists:** `scripts/backup.py`, `scripts/restore.py`, and `recovery/wal.py:20` (write-ahead log) are present and are classified "Implemented (scripts) / live-unverified" in `01-SYSTEM-BASELINE.md` BL-50; `recovery/enterprise_recovery.py` (407 lines, added since baseline per `01a-BASELINE-DELTA-HEAD.md` BL-24) is library-only, not referenced from `apps/`.
- **What is missing:** GAP-42 records that no restore drill has been run in this research programme — there is no evidence that a backup taken from a live HugeGraph/Neo4j instance has ever been restored to a clean environment and verified against the source. This is the single largest operational gap in this document.
- **Target runbook (PROPOSED, unexecuted):**
  1. Full backup of the primary backend and the embedded tenancy layers (`tenancy/layers.py` per-tenant AES-256-GCM-encrypted stores) on a defined schedule.
  2. Periodic restore-to-clean-environment drill (BM-16) verifying byte-for-byte equivalence (modulo timestamps) to the source.
  3. Point-in-time restore (PITR) to an arbitrary timestamp mid-ingestion-stream, verified against the recorded RPO.
  4. A documented, rehearsed runbook for restore under an active incident, not just a scripted happy path.
- **Status:** none of the four steps above has been executed; BM-16 in `15-VALIDATION-BENCHMARK-PLAN.md` is the benchmark that would produce the first real evidence here, and its own text notes "this is the first time this suite has ever run" once it does.

## 4. Monitoring and observability

- **What exists:** Prometheus text metrics (`observability/metrics.py`), JSON structured logging (`observability/logging.py`), optional OpenTelemetry (`observability/otel.py:25`), an observability-truth plane separating audit from telemetry with W3C traceparent support (`observability/truth.py`, `telemetry_separation.py`, added since baseline per `01a-BASELINE-DELTA-HEAD.md` BL-49) — classified "Implemented / Partial", with mount status in the live API unverified. `deploy/prometheus.yml` and `deploy/docker-compose.observability.yml` wire Prometheus into the reference Compose deployment.
- **What is deliberately absent:** no bundled Grafana. This is a direct consequence of the AGPL-3.0 finding on Grafana recorded in `02-TECHNOLOGY-REGISTRY.md` §3 (GAP-19/INV-SELF-11's own trigger list: "Grafana AGPL-3.0" is named as a component that would block white-label OEM redistribution if bundled). The operational consequence: a customer who wants dashboards today must bring their own Grafana (or another OTel-compatible visualizer) pointed at the Prometheus endpoint EOIP already exposes; EOIP does not ship one, by licence-driven design, not by oversight.
- **Gap:** GAP-20 — the audit trail is not yet tamper-evident (no hash-chaining confirmed); this is a detection-capability gap, not just a dashboard gap, and is tracked as a security threat in `16-SECURITY-PRIVACY-THREAT-MODEL.md` (part of the T-07/T-11/T-12 cluster around unverified operational integrity).
- **Readiness tooling:** `ops/readiness.py` provides HA-readiness routes (mounted, `apps/api/extended.py:1388`) and `qualification/harness.py`/`qa/verification_gate.py` exist as library-level qualification tooling (`01a-BASELINE-DELTA-HEAD.md` NB-15); neither has been exercised against a live incident in this research run.

## 5. Runbooks — what is missing today (GAP-20, GAP-42)

| Runbook | Status | Note |
|---|---|---|
| Incident response (security) | Not found | No dedicated incident-response runbook located in `deploy/` or `ops/`; `ops/readiness.py` covers HA readiness, not security incident response |
| Backup/restore/PITR | Scripts exist, never drilled | See §3; GAP-42 |
| Tenant offboarding / data deletion | Partial | `privacy/dsr.py` DSAR workflow (locate/export/rectify/erase) is implemented and admin-gated (`privacy/router.py`), but a full tenant-offboarding runbook spanning backup retention, licence/metering teardown, and audit-trail preservation was not found as a single document |
| Air-gapped install | Unverified | See §6; GAP-21 |
| Key rotation (egress vault, tenant data keys) | Not found as a runbook | `tenancy/layers.py` generates per-tenant AES-256-GCM keys via HKDF; no rotation runbook was found; the egress vault's own cipher is flagged for replacement in `16-SECURITY-PRIVACY-THREAT-MODEL.md` T-03 before a rotation runbook is even meaningful |
| Licence/dependency drift (CI gate) | Absent, proposed in BM-20 | GAP-19/GAP-44; see `15-VALIDATION-BENCHMARK-PLAN.md` BM-20 |

## 6. Air-gapped installation (BM-19)

- **Target procedure outline (PROPOSED, unexecuted — this is a specification, not a verified runbook):**
  1. Transfer a pre-built offline bundle (container images, model weights, licence file) to a network-isolated host.
  2. Load container images into the local container runtime from the bundle (no registry pull).
  3. Stage local model weights into the model-serving data directory (no model download at install time).
  4. Boot the environment via the local Compose file (or Helm chart, for a Kubernetes target).
  5. Run a self-test suite that must observe **zero outbound network calls** during execution, verified by an egress proxy or packet capture — not by trusting the installer's own "offline" claim, per `15-VALIDATION-BENCHMARK-PLAN.md` BM-19's own instruction.
- **Known gap: Neptune is excluded from the air-gap tier.** Per A-08 (`22-OPEN-QUESTIONS-AND-ASSUMPTIONS.md`): "Neptune is treated as a required supported backend even though it cannot run air-gapped; air-gapped deployments use HugeGraph or Neo4j." Neptune is a managed AWS cloud service reachable only inside a VPC (`04-COMPETITOR-DEEP-DIVES/C01-amazon-neptune.md` INV-amazon-neptune-01); there is no local Neptune image and none is expected. If a customer needs both Neptune and air-gap simultaneously, A-08 records this as an unresolved conflict requiring a product decision, not an engineering fix.
- **Model-weight licensing for air-gap bundles:** any model weight staged into an air-gap bundle must clear the same licence allow-list as any other bundled component (GAP-19/BM-20) — `02-TECHNOLOGY-REGISTRY.md` §3 already flags several model-weight licences as heterogeneous (e.g. GLiNER checkpoints reported non-commercial for some variants, Marker's modified Open RAIL-M weights) and these checks must run before a weight is added to the bundle, not after.
- **Status:** no air-gap install has been run end to end in this research programme; GAP-21 records this explicitly.

## 7. TCO model inputs

This is a model of *inputs*, not a quoted price. Where a competitor's price appears, it is cited at the confidence level the deep dive records it, and is never presented as equivalent to an unquoted EOIP price.

| Cost dimension | Input driver for EOIP | Evidence / source |
|---|---|---|
| Core licence cost | EOIP's own licensing/packaging model is out of scope for this document (commercial decision, not an engineering one); the *avoided* cost is every AGPL/SSPL/BUSL/commercial component NOT bundled by the licence-gate policy (GAP-19) | `02-TECHNOLOGY-REGISTRY.md` §3 full trigger list |
| Competitor licence cost (reference only, not an EOIP claim) | TigerGraph Enterprise: commercial licence, Community Edition barred from third-party/white-label use and from benchmark publication; RDFox: proprietary, evaluation-only licence, production terms not publicly verified; Neo4j: Community GPLv3 (commercial agreement supersedes), Enterprise commercial, GDS OpenGDS GPL | `04-COMPETITOR-DEEP-DIVES/C01-tigergraph.md` CLAIM-tigergraph-04 (0.8 confidence, summary not full-text); `04-COMPETITOR-DEEP-DIVES/C02-rdfox.md` CLAIM-rdfox-04; `02-TECHNOLOGY-REGISTRY.md` T-C01-neo4j |
| Compute cost per tier | Hardware sizing in §1 (small/medium/large); no cloud-hour or on-prem-amortization figure is computed in this document — that requires a customer's own hardware cost basis, which was not in scope for this research run | §1 above |
| Model-serving cost | Local-first policy (Ollama/llama.cpp on CPU by default, per ADR-H15/H16/H17 CPU-only policy, `01-SYSTEM-BASELINE.md` U-11) avoids a per-token cloud-LLM fee for the deterministic-first retrieval path (J6); any optional cloud-LLM egress is gated by the egress manifest (`egress/gateway.py`, default sharing level S0 = none) and would carry its own per-call cost if ever enabled | `01-SYSTEM-BASELINE.md` §4 "AI" row; `16-SECURITY-PRIVACY-THREAT-MODEL.md` T-16 |
| Support burden | No support-cost model exists in this research programme; the operational gaps in §5 (no incident-response runbook, no drilled restore, no air-gap verification) each represent a support-burden risk that is currently unquantified, not zero | §5 above |
| SBOM/licence-gate tooling cost | Syft/Grype/cosign are each Apache-2.0 and self-hostable at no licence cost; the engineering cost of wiring them into CI is the real cost driver, not a licence fee | `04-COMPETITOR-DEEP-DIVES/C19-supply-chain.md` §10, §13 |

**What this document does not do:** it does not publish a side-by-side dollar comparison against Palantir Foundry/AIP, Stardog Enterprise, or Neo4j Aura Enterprise. The prior 2026-10-19 placeholder did so with specific annual-licence figures ("$1,000,000+/yr", "$150,000+/yr", "$100,000+/yr") that are not sourced to any evidence record in this package and are removed. A legitimate TCO comparison requires a quoted price from each vendor for a comparable deployment, which was not obtained in this research run; `04-COMPETITOR-DEEP-DIVES/C07-palantir-foundry.md` records only that Palantir's pricing is "opaque contract pricing and compute-second metering" (INV-palantir-foundry-03), which is itself evidence against quoting a single figure for it.

## 8. What BM-02/BM-16/BM-19/BM-20 would need to confirm before this document can carry real numbers

1. BM-02 (scale/sizing) — confirm or revise the A-10 ~10M node / ~50M edge one-node target, and find the actual latency/throughput curve across the three sizing tiers in §1.
2. BM-16 (backup/restore/DR) — produce the first real restore-duration number and confirm the RPO/RTO the backup scripts actually deliver.
3. BM-19 (air-gap) — produce the first verified zero-outbound-calls air-gap install, and quantify operator effort (time to first governed query) honestly rather than asserting "< 1 week" as the prior placeholder did.
4. BM-20 (licence CI gate) — confirm the licence allow-list gate actually blocks a known-bad dependency before any OEM/white-label cost model can be called reliable.

Until these four benchmarks produce a first real, reproducible result, every number in §1, §3, §6, and §7 above remains a target input to the operations model, not a delivered capability.

## 9. Noisy-tenant, metering, and upgrade risk

- **Multi-tenant resource isolation:** `tenancy/quotas.py` (`01a-BASELINE-DELTA-HEAD.md` NB-16) and `tenancy/layers.py` provide per-tenant quota and resource-isolation primitives at the embedded-layer level (vector index, search index, SQLite schema, object storage, event topics, caches); none of this has been load-tested under a "noisy neighbor" scenario (one tenant issuing a sustained heavy query load while another tenant's p95 latency is measured) — this is the operational gap the chaos matrix in `15-VALIDATION-BENCHMARK-PLAN.md` §3 names against BM-02/BM-05.
- **Metering and licensing:** `licensing/license_file.py`, `licensing/meter.py`, and `tenancy/metering.py` provide offline, signed licence files and per-tenant metering (BL-22, "Implemented"); this is the mechanism a flat-fee or usage-based commercial model would hang off, but no pricing model itself is specified in this document (commercial decision, out of scope per A-11).
- **Upgrade and migration risk:** `migration/protocol.py`'s eight-stage protocol (discovery and pin -> ... -> CDC catch-up -> rollback, `01a-BASELINE-DELTA-HEAD.md` NB-09) and `migration/cli.py` exist as library code with a semantic-equivalence "golden queries" harness stage; no live source migration has been run with this tooling in this research programme, so upgrade risk for an existing customer's live deployment is unquantified, not low. This is the same instrument BM-17 (ontology governance workflow, J4's dry-run-migration-with-rollback acceptance criterion) exercises, and the two should be read together before any upgrade-risk claim is made to a customer.
- **Energy and hardware footprint:** the CPU-only policy (ADR-H15/H16/H17) means EOIP's default footprint has no GPU draw; this is a qualitative statement only — no watts-per-query or per-tenant energy figure has been measured in this research programme, and Master Prompt §7 dimension 20 ("energy and hardware footprint") remains an open measurement for a future BM-02 extension, not a number this document can report today.
- **Reindexing cost:** `codegraph/diff_hunk.py` and `ingestion/incremental_indexer.py` provide incremental re-indexing on a changed commit (BL-42, exercised functionally by BM-12's J1 acceptance criterion: "reindexing a changed commit must not break unchanged relationships"); the *cost* of that reindex at Tier 2/Tier 3 scale is a BM-02 measurement, not yet taken.
