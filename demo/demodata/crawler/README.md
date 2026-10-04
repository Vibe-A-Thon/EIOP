# Crawler Demo Data — Meridian Financial Services

Scenario: **Meridian Financial Services (MFS)** operates internal wikis, API
portals, database documentation sites, design tools, and observability dashboards.
This folder contains mock crawled page data in the format produced by the
`ControlledWebCrawler` connector.

Each JSON file is an array of crawled pages, representing what the crawler would
capture from each portal. The data is content-rich and cross-references the same
infrastructure, services, and people found in the code graph and other demo data.

## Source Portals

| File | Portal | Pages | Content |
|------|--------|-------|---------|
| wiki-confluence.json | wiki.mfs.internal | 9 | Engineering handbook, runbooks, team structure, DB schemas, service accounts, OpenShift docs, API gateway config, PCI compliance |
| api-portal-swagger.json | api.mfs.internal | 6 | API catalog, Payment Gateway API v2, Fraud Scoring API v2, Token Vault API v1, Settlement API v1, AML Engine API v1 |
| db-schemas.json | dbdocs.mfs.internal | 4 | mfs_payments_db, mfs_fraud_db, mfs_customers_db, mfs_audit_db full schema docs |
| figma-designs.json | figma.mfs.internal | 3 | Payment portal design system, fraud dashboard design, customer portal redesign |
| observability-portals.json | Various | 6 | Grafana SLOs, Datadog APM, Kibana logs, Fortuna risk dashboard, status page, on-call schedules |

## Key Cross-References

The crawled content consistently references:

- **Service accounts:** svc-payment-api, svc-fraud-engine, svc-customer-svc, svc-notification-svc, svc-cicd-deployer, svc-monitoring
- **Databases:** mfs_payments_db, mfs_fraud_db, mfs_customers_db, mfs_audit_db
- **Hosts:** pghost-prod-01 through pghost-prod-04, redis-cluster, kafka-broker, hsm-gateway, vault, api-gateway (all .mfs.internal)
- **Pods:** mfs-pay-pod-01, mfs-fraud-pod-01, mfs-portal-pod-01, mfs-common-pod-01
- **Kafka topics:** txn-events, fraud-scores, aml-alerts, payment-status, refund-requests, audit-events
- **People:** Arjun Deshmukh (Payments), Priya Natarajan (Fraud), Marcus Thompson (Platform), David Kim (VP Eng), Samantha Rodriguez (Dir Eng), and squad members
- **Code symbols:** PaymentService, FraudScorer, AMLRuleEngine, VelocityMonitor, FeatureExtractor, AuthClient, AuditLogger, TokenizationService

## JSON Format

Each page follows the `ControlledWebCrawler` output format:

```json
{
  "url": "https://...",
  "content_type": "text/html",
  "status_code": 200,
  "title": "Page Title",
  "headings": ["H1 text", "H2 text", ...],
  "text": "Full page text content...",
  "links": ["https://linked-page/..."]
}
```
