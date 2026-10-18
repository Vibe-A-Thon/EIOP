# KnowGridFlow (EOIP) API Reference & Contributing Guide (S-04)

## Core REST API Endpoints

- **GET `/health` / `/ready`**: System health and readiness probes (NFR-OPS-001).
- **GET `/metrics`**: Prometheus text-format metrics exposition (MVP-FR-024, NFR-OPS-002).
- **POST `/api/v1/graph/query`**: Execute unified Cypher/Gremlin queries across active graph stores.
- **POST `/api/v1/causal/blast-radius`**: Counterfactual blast-radius evaluation for hypothetical changes.
- **GET `/api/v1/admin/security/posture`**: Enterprise security governance posture and token revocation status.
- **POST `/api/v1/ci/pipeline/run`**: Trigger automated KG CI/CD pipeline validation.
- **POST `/api/v1/platform/tools/mcp/connect-external`**: Authenticated operator initializes and discovers an allowlisted external MCP server. The request selects `server_name` and `transport`; it cannot supply process configuration.

## External MCP Configuration

Configure external MCP servers in the EOIP deployment environment. `EOIP_MCP_ALLOWED_HOSTS` is a comma-separated host allowlist for Streamable HTTP. `EOIP_MCP_READ_ONLY_TOOLS` is a JSON object mapping each configured server name to its allowed read-only tool names. `EOIP_MCP_STDIO_SERVERS` is a JSON object mapping server names to trusted process configurations:

```json
{
	"local-docs": {
		"command": "/opt/eoip/bin/mcp-docs-server",
		"args": ["--stdio"],
		"env": {"DOCS_ROOT": "/srv/approved-docs"},
		"cwd": "/srv/approved-docs"
	}
}
```

Only deployment configuration may select a stdio command, arguments, environment, or working directory. The API request for stdio omits `endpoint`; caller-supplied `command` or other unknown fields are rejected. Both transports use live MCP discovery and the configured read-only tool allowlist. Stdio processes receive the MCP SDK's safe inherited environment plus explicitly configured variables; do not place secrets in arguments or logs.

## Contributing Guidelines

1. **Strict Zero Mock Policy**: Never wire mock or demo data into production execution paths.
2. **Schema Invariant Gate**: All graph mutations must conform to `VERTEX_LABELS`, `EDGE_LABELS`, and `PROPERTY_KEYS` in `packages/eoip/ontology/manifest.py`.
3. **Traceability**: All requirements must have passing unit tests explicitly decorated with `@pytest.mark.req("<ID>")`.
4. **Gate Verification**: Verify tests and gate integrity via `pytest tests/unit/test_qa_gate_integrity.py`.
