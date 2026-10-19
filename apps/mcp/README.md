# EOIP MCP Gateway

`main.py:create_app` builds the FastMCP Streamable HTTP application. It delegates tool calls to the EOIP API rather than owning graph storage. The local gateway is read-oriented; some tools invoke computations or return inert proposals, which is distinct from an authorized external write.

## Run

The default Compose profile serves `/mcp` on host port 8001. For host development with an already-running API and a private `EOIP_API_TOKEN`:

```powershell
$env:EOIP_API_URL = 'http://127.0.0.1:8000'
python -m uvicorn apps.mcp.main:create_app --factory --host 127.0.0.1 --port 8001
```

The token must match the API configuration. `/health/live` is the gateway's unauthenticated liveness route. Other requests require its configured token. API reachability/authorization and actual tool execution require separate checks. Default host/origin allowlists in `main.py` are local/container oriented; review them before any nonlocal deployment.

## Tools and Integration

Discover actual tools using MCP initialization and `tools/list`; use the returned schemas. Families include search/entity, query/path/impact, lineage/evidence, source-symbol lookup and bounded agent inspection/execution. Tool discovery is not a guarantee that every backend/profile can execute a capability.

The gateway uses its configured deployment credential for downstream API calls. It is not currently a general per-user OAuth delegation service. Preserve this limitation in security reviews and before SaaS exposure. A protocol annotation does not replace local allowlisting or domain authorization.

Outbound external MCP support is a different component: `packages/eoip/tools_contract/mcp_bridge.py`, configured through [API reference](../../docs/api-reference.md#external-mcp-configuration). Do not confuse EOIP's server with its external MCP client.

Run `python -m pytest tests/integration/test_mcp_transport.py tests/integration/test_external_mcp_bridge.py -q` for focused transport/bridge checks. Then exercise the selected deployed gateway and API profile. Keep the VS Code client's allowlist compatible and do not expose write tools merely to make a client test pass.
