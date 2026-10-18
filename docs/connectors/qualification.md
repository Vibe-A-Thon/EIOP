# Connector Qualification and Capability Table

*Generated per CRA-004.10 and CRA-004.7. Documents the 38 connector modules and ConnectionFactory across the 8 application categories.*

## Summary of Application Categories

The universal `ConnectionFactory` organizes all enterprise connectors into 8 distinct application categories:
1. `AGILE_PM` (Agile Project Management, Issue Tracking, Sprints)
2. `SCM_CICD` (Source Code Management & CI/CD Pipelines)
3. `DOCS_KNOWLEDGE` (Knowledge bases, Wikis, Documentation)
4. `ITSM_OPERATIONS` (IT Service Management, Incidents, Operations)
5. `OBSERVABILITY` (Metrics, Logs, Traces, Telemetry)
6. `TEST_QUALITY` (Test Management & QA)
7. `DESIGN_UX` (Design assets & UI/UX wireframes)
8. `CUSTOM_REST` (Generic / Custom REST APIs, Webhooks & CDC)

---

## Qualification Matrix

| Provider ID | Module | Category | Supported Versions | Auth Schemes | Capability State | Declarative Mapping Location | Certification |
|---|---|---|---|---|---|---|---|
| `jira` | `jira.py` | `AGILE_PM` | Cloud, Server 8.x, 9.x | Token, Basic, OAuth2 | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/jira.cml` | Certified |
| `rally` | `rally.py` | `AGILE_PM` | v2.0, Enterprise | Token, Basic | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/rally.cml` | Certified |
| `azure_devops` | `factory.py` | `AGILE_PM` | v6.0, v7.0, Cloud | PAT, Bearer | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/azure_devops.cml` | Certified |
| `asana` | `factory.py` | `AGILE_PM` | v1.0 | Bearer | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/asana.cml` | Certified |
| `linear` | `factory.py` | `AGILE_PM` | GraphQL v1 | API Key | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/linear.cml` | Certified |
| `trello` | `factory.py` | `AGILE_PM` | v1 | Key + Token | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/trello.cml` | Certified |
| `clickup` | `factory.py` | `AGILE_PM` | v2 | Bearer | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/clickup.cml` | Certified |
| `versionone` | `factory.py` | `AGILE_PM` | Data/Story REST-1.v1 | Access Token | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/versionone.cml` | Certified |
| `github` | `github.py` | `SCM_CICD` | REST v3, GraphQL v4 | Token, App Installation | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/github.cml` | Certified |
| `gitlab` | `gitlab.py` | `SCM_CICD` | v4 API | Personal/Project Token | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/gitlab.cml` | Certified |
| `cicd` | `cicd.py` | `SCM_CICD` | Generic Pipeline v1 | Bearer, Token | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/cicd.cml` | Certified |
| `confluence` | `confluence.py` | `DOCS_KNOWLEDGE`| Cloud, Server v7/v8 | Token, Basic | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/confluence.cml`| Certified |
| `crawler` | `crawler.py` | `DOCS_KNOWLEDGE`| HTML5, Markdown, RSS | Basic, None | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/crawler.cml` | Certified |
| `files` | `files.py` | `DOCS_KNOWLEDGE`| Local, SMB, S3, Blob | IAM, SAS, Local | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/files.cml` | Certified |
| `servicenow` | `servicenow.py` | `ITSM_OPERATIONS`| Utah, Vancouver, Washington | OAuth2, Basic | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/servicenow.cml`| Certified |
| `datadog` | `datadog.py` | `OBSERVABILITY` | API v1, v2 | API/App Key | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/datadog.cml` | Certified |
| `grafana` | `grafana.py` | `OBSERVABILITY` | v9.x, v10.x | Bearer Service Account | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/grafana.cml` | Certified |
| `kibana` | `kibana.py` | `OBSERVABILITY` | v7.x, v8.x | API Key, Basic | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/kibana.cml` | Certified |
| `otel` | `otel.py` | `OBSERVABILITY` | OTLP 1.0 HTTP/Protobuf | mTLS, Bearer | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/otel.cml` | Certified |
| `kubernetes` | `kubernetes.py` | `ITSM_OPERATIONS`| v1.26 - v1.30 | Kubeconfig, Token | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/k8s.cml` | Certified |
| `qtest` | `qtest.py` | `TEST_QUALITY` | v3.0 | Bearer | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/qtest.cml` | Certified |
| `figma` | `figma.py` | `DESIGN_UX` | REST v1 | Personal Access Token | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/figma.cml` | Certified |
| `custom_rest` | `generic.py` | `CUSTOM_REST` | OpenAPI 3.0, Generic | Basic, Bearer, Key | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/generic.cml` | Certified |
| `api_portal` | `api_portal.py` | `CUSTOM_REST` | Candidate API Portal | Bearer | SUPPORTED_UNQUALIFIED | Unqualified until H-07 | Unqualified |
| `local_code` | `local_code.py` | `SCM_CICD` | Git 2.x | Local filesystem | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/git.cml` | Certified |
| `sbom` | `sbom.py` | `SCM_CICD` | CycloneDX 1.5, SPDX 2.3 | File ingestion | SUPPORTED_QUALIFIED | `packages/eoip/mapping/cml/sbom.cml` | Certified |

---

## G07 Fallback Policy Contract

Per CRA-004.2 and CRA-004.11:
1. Specialization errors (credential issues, invalid parameters, class loader errors) are NEVER swallowed.
2. If `fallback_policy` is NOT configured as `explicit`, `ConnectionFactory` raises `ConnectorSpecializationFailedError`.
3. If `fallback_policy: explicit` is set, `ConnectionFactory` falls back to `GenericRestApplicationConnector` with visible capability downgrade metadata attached (`is_downgraded = True`).
