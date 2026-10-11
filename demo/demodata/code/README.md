# Code Graph Demo Data — Meridian Financial Services

Scenario: **Meridian Financial Services (MFS)** is a financial services company
operating payment processing, fraud detection, and customer-facing portal
services. The data represents code structure as JSON files that the system
ingests to construct a code graph without parsing source files directly.

This folder demonstrates **code-as-JSON ingestion** where each JSON file
describes a repository's file structure, symbols (classes, functions, methods,
components), dependencies, infrastructure references, and call/import/containment
edges.

## How EOIP uses it

The code graph ingestion path converts these JSON records into Repository, File,
CodeSymbol, Dependency, service/infrastructure, and relationship facts. The
resulting graph supports source-bound traceability, code impact, dependency
navigation, VS Code context, Hubble walkthroughs, and cross-source links to Jira,
GitLab, ServiceNow, API, observability, and documentation records. These files
are fixtures for local verification, not harvested customer repositories.

## Source Repositories

| File | Repository | Language | Files | Symbols | Edges |
|------|-----------|----------|-------|---------|-------|
| mfs-payment-gateway.json | mfs-payment-gateway | Python | 13 | 33 | 66 |
| mfs-fraud-engine.json | mfs-fraud-engine | Python | 13 | 29 | 62 |
| mfs-common-libs.json | mfs-common-libs | Python | 8 | 24 | 43 |
| mfs-customer-portal.json | mfs-customer-portal | TypeScript/React | 12 | 24 | 53 |

## Key Infrastructure References

- **Service accounts:** svc-payment-api, svc-fraud-engine, svc-customer-svc, svc-notification-svc
- **Databases:** mfs_payments_db (pghost-prod-01), mfs_fraud_db (pghost-prod-02), mfs_audit_db (pghost-prod-03), mfs_customers_db (pghost-prod-04)
- **OpenShift pods:** mfs-pay-pod-01, mfs-fraud-pod-01, mfs-portal-pod-01
- **Kafka topics:** txn-events, fraud-scores, aml-alerts, payment-status, refund-requests
- **Shared infra:** redis-cluster.mfs.internal, kafka-broker.mfs.internal, vault.mfs.internal, hsm-gateway.mfs.internal

## Cross-Repository Connections

- mfs-customer-portal CONNECTS_TO mfs-payment-gateway (via paymentApi service)
- mfs-customer-portal CONNECTS_TO mfs-fraud-engine (via fraudApi service)
- mfs-payment-gateway CONNECTS_TO kafka-broker (txn-events topic)
- mfs-fraud-engine CONNECTS_TO kafka-broker (consumes txn-events, produces fraud-scores and aml-alerts)
- All services DEPENDS_ON mfs-common-libs (auth, logging, config, metrics)

## JSON Format

Each file follows the format expected by the EOIP code graph ingestion:

```json
{
  "description": "...",
  "repository": { "repo_id", "name", "source_uri", "default_branch" },
  "files": [ { "path", "language", "content_hash", "line_count" } ],
  "symbols": [ { "qualified_name", "symbol_kind", "name", "path", "start_line", "end_line" } ],
  "dependencies": [ { "name", "resolved", "language" } ],
  "infrastructure": { "service_account", "database", "pod", ... },
  "edges": [ { "type": "CONTAINS|DECLARES|CALLS|IMPORTS|DEPENDS_ON|CONNECTS_TO|DEPLOYED_ON", "from", "to" } ]
}
```
