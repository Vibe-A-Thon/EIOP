# 17 — Operations, SRE & Cost Model (KnowGridFlow / EOIP)

| Field | Value |
|---|---|
| Document | 17-OPERATIONS-SRE-COST-MODEL.md |
| Deployment Paradigms | Single-Node Local Appliance vs High-Availability Distributed Cluster |
| Air-Gap Support | 100% Fully Air-Gapped / Disconnected Viability |
| Verification Cutoff | 2026-10-18 UTC |

---

## 1. Hardware Sizing Guidelines

| Deployment Tier | Workload Scope | CPU / vCPU | RAM | Storage | Target Engines |
|---|---|---|---|---|---|
| **Tier 1 (Single Node)** | < 1M Nodes, Local Office | 8 vCPU | 32 GB | 250 GB NVMe | HugeGraph (RocksDB) + Local Qdrant + Ollama |
| **Tier 2 (High-Availability)** | 1M - 10M Nodes, Department | 32 vCPU | 128 GB | 1 TB NVMe | 3-Node HugeGraph / Neo4j Cluster + Redis WAL |
| **Tier 3 (Enterprise Scale)** | > 50M Nodes, Global Enterprise | 64+ vCPU | 256+ GB | 5+ TB NVMe | HugeGraph (HBase/Cassandra) + Distributed Qdrant |

---

## 2. 100% Air-Gapped Installation Runbook

```bash
# 1. Transfer pre-built air-gap bundle to target disconnected host
tar -xzf knowgridflow-airgap-bundle-v3.0.tar.gz -C /opt/knowgridflow

# 2. Load localized container images into local Docker/Containerd runtime
docker load -i /opt/knowgridflow/images/hugegraph-1.7.0.tar
docker load -i /opt/knowgridflow/images/neo4j-5-community.tar
docker load -i /opt/knowgridflow/images/ollama-0.12.3.tar
docker load -i /opt/knowgridflow/images/knowgridflow-api.tar
docker load -i /opt/knowgridflow/images/knowgridflow-web.tar

# 3. Initialize offline local model weights (e.g. bge-large-en, llama-3.2-3b)
cp -r /opt/knowgridflow/models/* /root/.ollama/models/

# 4. Boot environment via local docker-compose
docker compose -f /opt/knowgridflow/deploy/docker-compose.yml up -d

# 5. Execute air-gapped self-test and verification suite
python scripts/smoke_test.py --air-gapped --offline
```

---

## 3. Total Cost of Ownership (TCO) Comparison

| Cost Dimension | Palantir Foundry / AIP | Stardog Enterprise | Neo4j Aura Enterprise | KnowGridFlow / EOIP |
|---|---|---|---|---|
| **Annual License** | $1,000,000+ / yr | $150,000+ / yr | $100,000+ / yr | **$0 (Core OSS) / Flat Appliance Fee** |
| **Cloud Egress Tax** | High (Cloud compute) | Medium | High (Hosted Cloud) | **$0 (100% On-Premises / Local-First)** |
| **Per-Query / Token Fee** | Cloud LLM billed | High | Cloud LLM billed | **$0 (Local SLMs on CPU / Local GPU)** |
| **Time-to-Value** | 6 - 12 Months | 3 - 6 Months | 2 - 4 Months | **< 1 Week (Docker-first bootstrap)** |
