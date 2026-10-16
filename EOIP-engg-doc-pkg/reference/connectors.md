# EOIP Source Connectors

All 24 connectors implement the `SourceConnector` Protocol from `packages/eoip/connectors/base.py`.

## Connector Protocol

```python
class SourceConnector(Protocol):
    def discover(self) -> DiscoveryResult: ...           # enumerate available resources
    def extract(self, checkpoint) -> Iterator[SourceEventV2]: ...  # paginated extraction
    def checkpoint(self) -> dict: ...                   # serializable resume state
    def health(self) -> HealthStatus: ...               # liveness check
    def replay(self, event_id: str) -> SourceEventV2: ...  # replay a specific event
```

`SourceEventV2` is immutable (extra="forbid"), has `payload_hash`, `captured_at`, `source_id`, `event_type`.

## Connector Infrastructure

| File | Purpose |
|------|---------|
| `connectors/base.py` | SourceConnector Protocol, DiscoveryResult, HealthStatus, SourceEventV2 |
| `connectors/rest.py` | REST client with pagination, retry/backoff, timeout |
| `connectors/acquisition.py` | AcquisitionPolicy with dry_run, resume, checkpoint validation |
| `connectors/sync.py` | Incremental sync with tombstone/deletion semantics |
| `connectors/config.py` | Connector configuration loading from environment |
| `connectors/registry.py` | ConnectorRegistry — discover all registered connectors |
| `connectors/errors.py` | ConnectorError, CheckpointError, ExtractionError |

## Source Connectors (24)

### Work Management

#### Jira (`connectors/jira.py` + `connectors/jira_json.py`)
- **Live mode** (`jira.py`): Jira REST API v3, checkpoint-based polling
- **Fixture mode** (`jira_json.py`): JSON file adapter, no network
- Extracts: Projects, WorkItems (issues/stories/tasks/bugs), Sprints, Versions, Changelog
- Cross-references: Person (assignee/reporter), linked issues, GitLab MR links
- Tests: `tests/unit/test_jira_connector.py`

#### Rally (`connectors/rally.py`)
- Rally/CA Agile Central REST API
- Extracts: Epics, Features, User Stories, Defects, Iterations
- Tests: `tests/unit/test_rally_connector.py`

#### qTest (`connectors/qtest.py`)
- qTest Manager REST API
- Extracts: Test Suites, Test Cases, Test Runs, Defect links
- Tests: `tests/unit/test_qtest_connector.py`

### Source Control & CI/CD

#### GitLab (`connectors/gitlab.py` + `connectors/gitlab_json.py`)
- **Live mode** (`gitlab.py`): GitLab REST API
- **Fixture mode** (`gitlab_json.py`): JSON file adapter
- Extracts: Repositories, Merge Requests, Commits, Pipelines, Jobs, Wiki pages
- Tests: `tests/unit/test_gitlab_connector.py`

#### GitHub (`connectors/github.py`)
- GitHub REST API v3
- Extracts: Repositories, Pull Requests, Issues, Commits, Branches
- See also: [connectors-github.md](connectors-github.md)
- Tests: `tests/unit/test_github_connector.py`

#### Local Code (`connectors/local_code.py`)
- Walks a local Git repository tree
- Extracts: Files (.py, .ts, .tsx, .js), symbols via AST parser
- Produces: CodeSymbol vertices with start_line/end_line/qualified_name
- Tests: `tests/unit/test_git_connector.py`

#### CI/CD (`connectors/cicd.py`)
- Generic CI/CD pipeline connector (provider-agnostic)
- Extracts: Pipelines, Jobs, Stages, Deployment records
- Graceful discovery when provider unavailable
- Tests: `tests/unit/test_gaps_implementations.py`

### Documentation & Knowledge

#### Confluence (`connectors/confluence.py` + `confluence_body.py` + `confluence_metadata.py`)
- Confluence Data Center / Cloud REST API
- `confluence.py`: Space/page/attachment enumeration with checkpoint polling
- `confluence_body.py`: Page body text extraction
- `confluence_metadata.py`: Page metadata (labels, versions, restrictions)
- Configured via: `EOIP_CONFLUENCE_URL`, `EOIP_CONFLUENCE_TOKEN`
- Tests: `tests/unit/test_confluence_connector.py`

#### ServiceNow (`connectors/servicenow.py`)
- ServiceNow Table API
- Extracts: Incidents, Problems, Changes, Knowledge Articles
- Configured via: `EOIP_SERVICENOW_URL`, `EOIP_SERVICENOW_TOKEN`
- Tests: `tests/unit/test_servicenow_connector.py`

#### Web Crawler (`connectors/crawler.py`)
- Controlled allowlist-only web crawler
- Respects robots.txt, rate limits, max-depth
- Extracts: Pages, links, headings structure
- No arbitrary web crawling — allowlist required

#### Generic (`connectors/generic.py`)
- Web sources and local file ingestion
- Multi-format: HTML, Markdown, plain text
- Tests: `tests/unit/test_generic_connector.py`

### Observability & Monitoring

#### Datadog (`connectors/datadog.py`)
- Datadog API v1/v2
- Extracts: Dashboards, Monitors, Metrics metadata

#### Grafana (`connectors/grafana.py`)
- Grafana HTTP API
- Extracts: Dashboards, Alerts, Datasources, Alert rules

#### Kibana (`connectors/kibana.py`)
- Kibana Saved Objects API
- Extracts: Dashboards, Searches, Index Patterns

### Design & API

#### Figma (`connectors/figma.py`)
- Figma REST API
- Extracts: Files, Projects, Components, Pages

#### API Portal (`connectors/api_portal.py`)
- API portal / service catalog
- Extracts: Services, Endpoints, API versions

### Security & Infrastructure

#### SBOM/SCA (`connectors/sbom.py`)
- SPDX and CycloneDX JSON format support
- Extracts: Components, Packages, Licenses, Vulnerabilities
- Returns `DiscoveryResult` with ≥2 resources
- Tests: `tests/unit/test_gaps_implementations.py`

#### OpenTelemetry (`connectors/otel.py`)
- OTLP trace and metric ingestion
- Graceful fallback when `opentelemetry-sdk` not installed
- Extracts: Spans, Metrics, Service topology
- Tests: `tests/unit/test_gaps_implementations.py`

#### Runtime Infrastructure (`connectors/runtime_infra.py`)
- Docker and Kubernetes resource discovery
- Graceful fallback when `kubernetes` client not installed
- Extracts: Pods, Services, Deployments, ConfigMaps

### File & Upload

#### Files (`connectors/files.py`)
- Raw binary/text file upload
- Delegates to fileparse engine for format-specific extraction
- Supports: .docx, .xlsx, .pptx, .pdf, .txt, .md, .csv

#### Webhook (`connectors/webhook.py`)
- Authenticated webhook payload ingestion
- HMAC signature validation
- Supports Jira, GitLab, GitHub, generic webhook schemas

---

## Adding a New Connector

1. Implement `SourceConnector` Protocol from `connectors/base.py`
2. Register in `connectors/registry.py`
3. Add configuration schema to `connectors/config.py`
4. Write tests in `tests/unit/test_{name}_connector.py`

Key contract rules:
- `discover()` must return `DiscoveryResult` (not dict)
- `extract()` must yield `SourceEventV2` (not raw dicts)
- All connectors must handle missing credentials gracefully
- Checkpoint must be serializable to JSON
- No silent failures — raise `ConnectorError` or populate DLQ

---

## Connector Configuration

All connector credentials are set via environment variables in `deploy/.env`:

| Variable | Connector |
|----------|-----------|
| `EOIP_CONFLUENCE_URL` | Confluence |
| `EOIP_CONFLUENCE_TOKEN` | Confluence |
| `EOIP_SERVICENOW_URL` | ServiceNow |
| `EOIP_SERVICENOW_TOKEN` | ServiceNow |
| `EOIP_JIRA_URL` | Jira (live mode) |
| `EOIP_JIRA_TOKEN` | Jira (live mode) |
| `EOIP_GITLAB_URL` | GitLab (live mode) |
| `EOIP_GITLAB_TOKEN` | GitLab (live mode) |
| `EOIP_GITHUB_TOKEN` | GitHub |

Credentials are **never** included in API payloads or job records.
