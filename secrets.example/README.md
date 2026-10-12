# Secrets Directory

Copy this directory to `secrets/` and replace placeholder values with actual credentials.

## Files

- `api-token.txt` — Bearer token for API/MCP authentication
- Add connector-specific credentials as needed, for example `jira-token.txt`,
  `gitlab-token.txt`, `github-token.txt`, `confluence-token.txt`, or
  `servicenow-token.txt`.

EOIP's implemented connector paths also support environment/secret references
for live Confluence and ServiceNow workers. Source registry entries and durable
job payloads should contain options and opaque secret references only, never raw
passwords or API tokens.

The current platform also includes semantic federation adapters for local graph,
file, REST JSON and SQLite-backed JDBC-style sources. Register only opaque
secret references or environment-derived headers/connection strings for live
REST/JDBC-style sources. Demo fixtures do not require secrets and must not be
promoted into production source definitions.

## Usage

Mount via Docker Compose:
```yaml
secrets:
  api_token:
    file: ./secrets/api-token.txt
```

Or set environment variables:
```
EOIP_API_TOKEN=your-token-here
```

**Never commit actual secrets to version control.**
