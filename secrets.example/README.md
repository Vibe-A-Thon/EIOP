# Secrets Directory

Copy this directory to `secrets/` and replace placeholder values with actual credentials.

## Files

- `api-token.txt` — Bearer token for API/MCP authentication
- Add connector-specific credentials as needed (e.g., `jira-token.txt`, `gitlab-token.txt`)

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
