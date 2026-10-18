# Snowflake Data Cloud Connector Specification

*Researched per CRA-009.1, CRA-009.2, CRA-009.6. Complies with ADR-004, ONT-007.*

## Official API Specifications & Pinned Versions
- **Snowflake**: SQL API (`v2`), Information Schema & Account Usage views, pinned to SQL dialect `snowflake-sql/2024.1`.
- Scoping hierarchy: Account -> Role -> Warehouse -> Database -> Schema -> Table/View/Column.

## Governance, Masking & Row Access Policies
- Role and warehouse scopes are explicitly declared on every emitted event.
- Column-level masking policies (`is_masked: true`, `masking_policy: name`) and row access policies (`row_access_policy: name`) are preserved in metadata.

## Three Operating Modes (CRA-009.2)
1. **`metadata_only`**: Crawls `INFORMATION_SCHEMA` and `ACCOUNT_USAGE` for tables, columns, constraints, and views. Strictly refuses data sampling.
2. **`sampled_data`**: Opt-in data sampling (`opt_in_sampling: true`). All sampled rows are subjected to masking policies and automated secrets/PII redaction prior to ingestion.
3. **`virtual_query`**: Live governed virtualization under strict cost and timeout guards.

## Resource & Cost Guards (CRA-009.6)
- **Statement Timeout**: Pinned to 30.0s default. Exceeding duration raises `statement_timeout`.
- **Credit Limit**: Configured credit consumption ceiling (`max_credits`). Exceeding consumption raises `cost_limit_exceeded`.
- **Lineage Extraction**: Opt-in query history parsing feeds CRA-029 SQL lineage extraction with literal scrubbing.
