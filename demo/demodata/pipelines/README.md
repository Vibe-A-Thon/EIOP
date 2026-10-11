# Pipeline Demo Data — MFS Fraud Detection Platform

Automated pipeline ingestion demo data for the **Meridian Financial Services (MFS)** Fraud Detection & AML Platform (FRD project).

## How EOIP uses it

This folder supports the developed batch/pipeline ingestion demo. The platform
can ingest these JSON exports through the local administration flow, capture raw
SourceEvents, normalize records into graph entities and relationships, attach
evidence/provenance, and make the resulting fraud-domain graph available to
query, impact, lineage, RAG, export, and Hubble views. The pipeline config is a
demo pipeline description; it is not an authenticated upstream polling run.

## Domain

This folder contains demo data for the **Fraud Detection & AML Platform**, covering:

- **ML Fraud Scoring Engine** (EPC-201 / FRD-100): Real-time fraud probability scoring using XGBoost models with feature extraction, model versioning, and A/B testing
- **Transaction Monitoring System** (EPC-202 / FRD-200): Velocity-based threshold monitoring and statistical anomaly detection with Kafka-based alerting
- **AML Compliance Engine** (EPC-203 / FRD-300): Anti-money laundering pattern detection (structuring, layering, integration) with automated SAR/CTR filing

## Organization Context

**Organization:** Meridian Financial Services (MFS) — same organization as the `manual/` folder (which covers the Payment Gateway / PAY project).

### Teams & People

| Team | Role | Person | Username |
|------|------|--------|----------|
| Platform Engineering | Lead | Sarah Chen | schen |
| Platform Engineering | Developer | David Okoye | dokoye |
| Fraud & Risk | Lead | Priya Sharma | psharma |
| Fraud & Risk | Developer | Nadia Kowalski | nkowalski |
| Quality Engineering | Lead | James O'Brien | jobrien |
| DevOps & SRE | Lead | Li Wei | lwei |
| DevOps & SRE | DevOps | Raj Patel | rpatel |
| UX Design | Designer | Elena Torres | etorres |

### Infrastructure

- **Databases:** mfs_fraud_db, mfs_aml_db (PostgreSQL on pghost-prod-02.mfs.internal)
- **Service Accounts:** svc-fraud-engine, svc-txn-monitor, svc-aml-engine, svc-model-serving
- **OpenShift Namespace:** mfs-prod, mfs-staging
- **Pods:** mfs-fraud-pod-01, mfs-fraud-pod-02, mfs-txn-mon-pod-01, mfs-aml-pod-01, mfs-model-pod-01
- **Kafka Topics:** mfs.txn.raw, mfs.txn.features, mfs.txn.enriched, mfs.alerts.txn

## Files

| File | Source System | Description |
|------|--------------|-------------|
| `rally.json` | Rally | 3 Epics (EPC-201/202/203), 3 Features, 2 User Stories |
| `jira.json` | Jira | 18 issues: Features, Stories, Tasks (FRD-100 through FRD-321) |
| `gitlab.json` | GitLab | 7 merge requests (!601-!802), 7 CI pipelines (9101-9302) |
| `servicenow.json` | ServiceNow | 3 change requests (CHG), 2 incidents (INC) |
| `confluence.json` | Confluence | 5 wiki pages: architecture, compliance, runbooks |
| `figma.json` | Figma | 1 design file, 3 pages, 5 components |
| `qtest.json` | qTest | 7 test cases (TC-FRD-001 to 007), 2 suites, 2 test runs |
| `kibana.json` | Kibana | 3 dashboards, 2 index patterns, 2 saved searches |
| `grafana.json` | Grafana | 2 dashboards, 4 alert rules, 3 datasources |
| `datadog.json` | Datadog | 2 dashboards, 4 monitors |
| `api-portal.json` | API Portal | 4 services, 13 endpoints |
| `code-graph.json` | Code Graph | 10 files, 20 symbols, 10 deps, 18 edges |
| `crawler-sites.json` | Web Crawler | 5 crawled pages from internal wikis |
| `pipeline-config.json` | Pipeline Config | 15-stage automated ingestion pipeline |

## Cross-Reference Map

```
Rally Epics → Jira Features:
  EPC-201 → FRD-100 (ML Fraud Scoring Engine)
  EPC-202 → FRD-200 (Real-time Transaction Monitoring)
  EPC-203 → FRD-300 (AML Pattern Detection)

Jira Stories → GitLab MRs → ServiceNow Changes:
  FRD-101 → MR !601 → CHG0090401
  FRD-201 → MR !701 → CHG0090501
  FRD-301 → MR !801 → CHG0090601

Jira Stories → qTest Test Cases:
  FRD-101 → TC-FRD-001
  FRD-102 → TC-FRD-002
  FRD-103 → TC-FRD-003
  FRD-201 → TC-FRD-004
  FRD-202 → TC-FRD-005
  FRD-301 → TC-FRD-006
  FRD-302 → TC-FRD-007

Incidents:
  INC0080201 → mfs-fraud-engine (false positive spike after model update)
  INC0080202 → mfs-txn-monitor (Kafka consumer lag)
```
