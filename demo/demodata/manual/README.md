# Manual Demo Data - Meridian Financial Services (MFS)

## Scenario: Payment Gateway Modernization (PAY Project)

Meridian Financial Services is modernizing its payment processing platform. This
demo data covers the **Payment Gateway Modernization** initiative across three
major epics:

## How EOIP uses it

This folder is used by the live manual-ingestion demo. The administration UI can
submit these source files, the API captures immutable SourceEvent evidence,
normalizes work/code/CI/test/design/ops/knowledge records, and exposes the
resulting graph through explorer lenses, source/job inspection, validation,
exports, JSON-LD/RDF/SHACL inspection, lineage, impact, semantic federation
planning, and evidence-addressable GraphRAG. The data is deliberately synthetic,
is loaded only through explicit demo/manual ingestion, and should not be treated
as a customer export or production federation source.

1. **EPC-101: Payment Gateway V2 Migration** - Tokenization, retry handling,
   multi-currency support (Jira Feature PAY-100)
2. **EPC-102: PCI DSS Compliance Upgrade** - Encryption at rest, HSM key
   rotation (Jira Feature PAY-200)
3. **EPC-103: Real-time Settlement Engine** - Batch settlement, balance
   reconciliation (Jira Feature PAY-300)

## Data Sources

| File | Source System | Records |
|------|---------------|---------|
| `rally.json` | Rally (WSAPI) | 3 Epics, 3 Features, 2 User Stories |
| `jira.json` | Jira | 3 Features, 6 Stories, 8 Tasks (PAY-100 to PAY-321) |
| `gitlab.json` | GitLab | 7 Merge Requests, 7 Pipelines |
| `servicenow.json` | ServiceNow | 4 Changes, 2 Incidents |
| `confluence.json` | Confluence | 5 Pages (architecture, compliance, design, API, runbook) |
| `figma.json` | Figma | 1 File, 3 Pages, 4 Components |
| `qtest.json` | qTest | 2 Test Suites, 8 Test Cases, 2 Test Runs |
| `kibana.json` | Kibana | 3 Dashboards, 1 Index Pattern, 2 Saved Searches |
| `grafana.json` | Grafana | 2 Dashboards, 2 Alert Rules, 2 Datasources |
| `datadog.json` | Datadog | 2 Dashboards, 4 Monitors |
| `api-portal.json` | API Portal | 3 Services, 11 Endpoints |
| `code-graph.json` | Code Graph | 12 Files, 20 Symbols, 10 Dependencies, 17 Edges |
| `crawler-sites.json` | Web Crawler | 5 Crawled Pages (wiki, API portal, DB docs, Grafana) |

## Infrastructure

- **Database**: mfs_payments_db, mfs_audit_db (PostgreSQL on pghost-prod-01.mfs.internal)
- **OpenShift**: mfs-prod, mfs-staging namespaces
- **Pods**: mfs-pay-pod-01/02/03, mfs-vault-pod-01, mfs-settle-pod-01
- **Service Accounts**: svc-payment-api, svc-token-vault, svc-settlement, svc-notification-svc

## Cross-Reference Integrity

All IDs are consistent across files:
- Rally Epics (EPC-101/102/103) link to Jira Features (PAY-100/200/300)
- Jira Stories link to GitLab MRs (!301-!502), ServiceNow CHGs, and qTest TCs
- ServiceNow changes reference Jira keys, GitLab MRs, and qTest cases
- GitLab MRs contain work_item_keys matching Jira story keys
- Confluence pages reference Jira keys, CHG numbers, and test cases
- Observability tools reference pods, service accounts, and infrastructure

## Note

This data is for the MANUAL ingestion folder. The Pipeline folder contains
separate data about the **Fraud Detection (FRD)** project from the same
organization. The two datasets share infrastructure and team members but
use completely different work item keys and project domains.
