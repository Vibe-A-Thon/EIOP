from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import httpx
import pytest
from eoip.platform_router import ExternalMCPConnectRequest
from eoip.tools_contract import mcp_bridge
from eoip.tools_contract.mcp_bridge import ExternalMCPClient, MCPBridgeError
from mcp import StdioServerParameters
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations
from pydantic import ValidationError


@pytest.mark.asyncio
async def test_external_bridge_uses_real_mcp_discovery_and_tool_execution():
    server = FastMCP(
        "local-read-server",
        stateless_http=True,
        json_response=True,
        transport_security=TransportSecuritySettings(
            allowed_hosts=["127.0.0.1", "127.0.0.1:*"],
            allowed_origins=["http://127.0.0.1", "http://127.0.0.1:*"],
        ),
    )
    observed_calls: list[str] = []

    @server.tool(annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False))
    async def lookup(query: str) -> dict:
        observed_calls.append(query)
        return {"query": query, "records": ["record-1"]}

    @server.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True))
    async def modify(query: str) -> dict:
        observed_calls.append(f"WRITE:{query}")
        return {"changed": True}

    server_app = server.streamable_http_app()

    def client_factory(**kwargs):
        return httpx.AsyncClient(
            transport=httpx.ASGITransport(app=server_app),
            base_url="http://127.0.0.1",
            **kwargs,
        )

    bridge = ExternalMCPClient(
        allowed_hosts={"127.0.0.1"},
        read_only_tool_allowlist={"local-read-server": {"lookup"}},
        http_client_factory=client_factory,
    )

    async with server_app.router.lifespan_context(server_app):
        info = await bridge.connect_server(
            server_name="local-read-server",
            transport="streamable-http",
            endpoint="http://127.0.0.1/mcp",
        )
        assert info["status"] == "available"
        assert info["tools_registered"] == ["local-read-server__lookup"]
        assert "local-read-server__modify" not in info["tools_registered"]

        result = await bridge.invoke_external_tool(
            "local-read-server__lookup",
            {"query": "service status"},
            caller_id="test-agent",
        )

    assert observed_calls == ["service status"]
    assert result["status"] == "SUCCEEDED"
    assert result["output"]["isError"] is False
    assert json.loads(result["output"]["content"][0]["text"]) == {
        "query": "service status",
        "records": ["record-1"],
    }
    assert "attestation" not in result


@pytest.mark.asyncio
async def test_external_bridge_rejects_unallowlisted_invalid_host_before_connecting():
    bridge = ExternalMCPClient(allowed_hosts={"127.0.0.1"})

    with pytest.raises(MCPBridgeError, match="not allowlisted"):
        await bridge.connect_server(
            server_name="untrusted",
            transport="streamable-http",
            endpoint="https://mcp.invalid.example/mcp",
        )

    assert bridge.list_connected_servers() == []


@pytest.mark.asyncio
async def test_external_bridge_uses_configured_stdio_server_process(tmp_path):
    server_script = """
import json
import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

server = FastMCP('local-stdio-read-server')

@server.tool(annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False))
def lookup(query: str) -> dict:
    with open(os.environ['EOIP_TEST_MCP_LOG'], 'a', encoding='utf-8') as log:
        log.write(json.dumps({'query': query}) + '\\n')
    return {'query': query, 'records': ['stdio-record-1']}

server.run(transport='stdio')
"""
    project_root = Path.cwd()
    child_env = {
        name: os.environ[name]
        for name in ("PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP")
        if name in os.environ
    }
    child_env.update({
        "EOIP_TEST_MCP_LOG": str(tmp_path / "stdio-calls.jsonl"),
        "PYTHONPATH": os.pathsep.join((str(project_root), str(project_root / "packages"))),
    })
    server_config = StdioServerParameters(
        command=sys.executable,
        args=["-u", "-c", server_script],
        env=child_env,
        cwd=str(project_root),
    )
    bridge = ExternalMCPClient(
        read_only_tool_allowlist={"local-stdio-read-server": {"lookup"}},
        stdio_server_configs={"local-stdio-read-server": server_config},
    )

    info = await bridge.connect_server(server_name="local-stdio-read-server", transport="stdio")
    result = await bridge.invoke_external_tool(
        "local-stdio-read-server__lookup",
        {"query": "service status"},
        caller_id="test-agent",
    )

    assert info["transport"] == "stdio"
    assert info["tools_registered"] == ["local-stdio-read-server__lookup"]
    assert result["status"] == "SUCCEEDED"
    assert json.loads(result["output"]["content"][0]["text"]) == {
        "query": "service status",
        "records": ["stdio-record-1"],
    }
    call_log = (tmp_path / "stdio-calls.jsonl").read_text(encoding="utf-8").splitlines()
    assert [json.loads(line) for line in call_log] == [{"query": "service status"}]

    with pytest.raises(MCPBridgeError, match="not configured"):
        await ExternalMCPClient().connect_server("not-configured", transport="stdio")


def test_stdio_api_request_cannot_supply_process_configuration():
    request = ExternalMCPConnectRequest(server_name="configured-server", transport="stdio")
    assert request.endpoint is None

    with pytest.raises(ValidationError):
        ExternalMCPConnectRequest.model_validate({
            "server_name": "configured-server",
            "transport": "stdio",
            "command": sys.executable,
        })


def test_stdio_command_is_loaded_from_validated_server_configuration(monkeypatch, tmp_path):
    monkeypatch.setattr(mcp_bridge, "_mcp_client_instance", None)
    monkeypatch.setenv(
        "EOIP_MCP_READ_ONLY_TOOLS",
        json.dumps({"configured-server": ["lookup"]}),
    )
    monkeypatch.setenv(
        "EOIP_MCP_STDIO_SERVERS",
        json.dumps({
            "configured-server": {
                "command": sys.executable,
                "args": ["--version"],
                "env": {"EOIP_MCP_TEST_MARKER": "configured"},
                "cwd": str(tmp_path),
            }
        }),
    )

    client = mcp_bridge.get_external_mcp_client()

    assert client._stdio_server_configs["configured-server"].command == sys.executable
    assert client._stdio_server_configs["configured-server"].args == ["--version"]
    assert client._read_only_allowlist["configured-server"] == frozenset({"lookup"})