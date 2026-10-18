# Splunk REST & Saved Searches Connector Specification

*Researched per CRA-008.2, CRA-008.7, CRA-008.8. Complies with ADR-004, ONT-007.*

## Official API Specifications & Pinned Versions
- **Splunk Enterprise & Splunk Cloud**: REST API pinned to Splunk 9.x baseline (`/servicesNS/{user}/{app}/saved/searches`, `/services/search/jobs`).
- Core entities: Saved searches, alerts, dashboard knowledge objects.

## Query, Time & Result Budgets
- Execution is strictly bounded by `SearchBudget`:
  - `max_results`: default limit 1,000 results.
  - `timeout_seconds`: default 30.0s execution timeout.
  - `max_search_span_hours`: default 72h historical search span.
- Exceeding query or execution limits raises a `ConnectorError("budget_exceeded")`.

## Secret & PII Redaction with Machine Receipts
- Before ingestion and persistence into the knowledge graph, queries and log snippets are scrubbed for:
  - API keys and bearer tokens
  - Passwords and credentials
  - Database connection strings (MongoDB, PostgreSQL, MySQL, Redis)
  - Plaintext email addresses
- Redaction produces a `RedactionReceipt` containing counts of sanitized items only, strictly preventing removed values from leaking into logs or metadata.
