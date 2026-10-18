"""Universal external MCP client bridge and cryptographic tool execution attestation.

Dynamically discovers and attaches external MCP servers into the execution harness
and generates tamper-evident HMAC-SHA256 attestation certificates for tool calls.
"""

from __future__ import annotations

import hashlib
import hmac
import ipaddress
import json
import os
import re
import threading
import time
import uuid
from collections.abc import AsyncIterator, Callable, Mapping
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any
from urllib.parse import urlsplit

import httpx
import rfc8785
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

from eoip.tools_contract.engine import get_tool_contract_engine


@dataclass
class ToolAttestationCertificate:
    certificate_id: str
    tool_name: str
    caller_id: str
    input_hash: str
    output_hash: str
    timestamp: float
    nonce: str
    hmac_signature: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "certificate_id": self.certificate_id,
            "tool_name": self.tool_name,
            "caller_id": self.caller_id,
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "hmac_signature": self.hmac_signature,
            "metadata": self.metadata,
        }


class ToolExecutionAttestor:
    """Legacy process-local HMAC integrity helper; not non-repudiation evidence."""

    def __init__(self, signing_secret: str) -> None:
        if len(signing_secret.encode("utf-8")) < 32:
            raise ValueError("HMAC integrity key must contain at least 32 UTF-8 bytes")
        self.signing_secret = signing_secret.encode("utf-8")
        self._lock = threading.Lock()
        self._certificates: dict[str, ToolAttestationCertificate] = {}

    def attest_execution(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        output: Any,
        caller_id: str = "agent-mesh-supervisor",
    ) -> ToolAttestationCertificate:
        now = time.time()
        nonce = uuid.uuid4().hex[:12]
        cert_id = f"attest-{uuid.uuid4().hex[:16]}"

        input_json = json.dumps(arguments, sort_keys=True, default=str)
        output_json = json.dumps(output, sort_keys=True, default=str)

        input_hash = hashlib.sha256(input_json.encode("utf-8")).hexdigest()
        output_hash = hashlib.sha256(output_json.encode("utf-8")).hexdigest()

        # Generate HMAC-SHA256 signature
        sign_payload = f"{cert_id}:{tool_name}:{caller_id}:{input_hash}:{output_hash}:{now:.4f}:{nonce}"
        signature = hmac.new(self.signing_secret, sign_payload.encode("utf-8"), hashlib.sha256).hexdigest()

        cert = ToolAttestationCertificate(
            certificate_id=cert_id,
            tool_name=tool_name,
            caller_id=caller_id,
            input_hash=input_hash,
            output_hash=output_hash,
            timestamp=now,
            nonce=nonce,
            hmac_signature=signature,
            metadata={"arguments_count": len(arguments)},
        )

        with self._lock:
            self._certificates[cert_id] = cert

        return cert

    def verify_certificate(self, certificate_id: str) -> dict[str, Any]:
        with self._lock:
            cert = self._certificates.get(certificate_id)
        if not cert:
            return {"valid": False, "reason": f"Certificate '{certificate_id}' not found."}

        sign_payload = (
            f"{cert.certificate_id}:{cert.tool_name}:{cert.caller_id}:"
            f"{cert.input_hash}:{cert.output_hash}:{cert.timestamp:.4f}:{cert.nonce}"
        )
        expected_sig = hmac.new(self.signing_secret, sign_payload.encode("utf-8"), hashlib.sha256).hexdigest()

        valid = hmac.compare_digest(cert.hmac_signature, expected_sig)
        return {
            "valid": valid,
            "certificate_id": certificate_id,
            "tool_name": cert.tool_name,
            "caller_id": cert.caller_id,
            "timestamp": cert.timestamp,
        }


class MCPBridgeError(RuntimeError):
    """Base error for a real MCP transport, discovery, or tool failure."""


class MCPHostNotAllowed(MCPBridgeError, PermissionError):
    """The endpoint is outside the configured exact-host allowlist."""


class MCPConnectionError(MCPBridgeError):
    """The configured MCP server could not be initialized or queried."""


class MCPToolUnavailable(MCPBridgeError):
    """The remote tool is no longer qualified or its schema changed."""


class ExternalMCPClient:
    """Read-only MCP client using real stdio or Streamable HTTP sessions.

    Transport configuration and remote tool allowlists are trusted configuration.
    API callers can select a configured server but cannot supply a process command.
    Each operation opens a fresh session, so metadata reports availability rather
    than a persistent connection.
    """

    def __init__(
        self,
        *,
        allowed_hosts: set[str] | None = None,
        read_only_tool_allowlist: dict[str, set[str]] | None = None,
        stdio_server_configs: Mapping[str, StdioServerParameters] | None = None,
        credential_provider: Callable[[str], Mapping[str, str]] | None = None,
        http_client_factory: Callable[..., httpx.AsyncClient] = httpx.AsyncClient,
        timeout_seconds: float = 10.0,
        max_result_bytes: int = 1_000_000,
    ) -> None:
        configured_hosts = allowed_hosts
        if configured_hosts is None:
            configured_hosts = {
                value.strip().lower()
                for value in os.getenv("EOIP_MCP_ALLOWED_HOSTS", "").split(",")
                if value.strip()
            }
        self._allowed_hosts = frozenset(configured_hosts)
        self._read_only_allowlist = {
            server: frozenset(tools)
            for server, tools in (read_only_tool_allowlist or {}).items()
        }
        self._stdio_server_configs = {
            server: config.model_copy(deep=True)
            for server, config in (stdio_server_configs or {}).items()
        }
        self._credential_provider = credential_provider
        self._http_client_factory = http_client_factory
        self._timeout_seconds = timeout_seconds
        self._max_result_bytes = max_result_bytes
        self._lock = threading.RLock()
        self._available_servers: dict[str, dict[str, Any]] = {}
        self._tool_routes: dict[str, dict[str, Any]] = {}

    @staticmethod
    def _validate_server_name(server_name: str) -> None:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", server_name):
            raise ValueError("MCP server name is invalid")

    def _validate_endpoint(self, endpoint: str, transport: str) -> str:
        if transport not in {"http", "streamable-http"}:
            raise MCPBridgeError("Only Streamable HTTP transport is supported")
        parts = urlsplit(endpoint)
        if (
            parts.scheme not in {"http", "https"}
            or not parts.hostname
            or parts.username is not None
            or parts.password is not None
            or parts.fragment
            or "*" in parts.netloc
        ):
            raise MCPBridgeError("MCP endpoint URL is invalid")
        host = parts.hostname.lower()
        authority = parts.netloc.lower()
        if authority not in self._allowed_hosts and host not in self._allowed_hosts:
            raise MCPHostNotAllowed("MCP endpoint host is not allowlisted")
        if parts.scheme != "https":
            try:
                loopback = ipaddress.ip_address(host).is_loopback
            except ValueError:
                loopback = host == "localhost"
            if not loopback:
                raise MCPHostNotAllowed("Unencrypted MCP HTTP is permitted only on loopback")
        return endpoint

    def _headers(self, server_name: str) -> dict[str, str]:
        if self._credential_provider is None:
            return {}
        supplied = self._credential_provider(server_name)
        headers: dict[str, str] = {}
        for name, value in supplied.items():
            if not isinstance(name, str) or not isinstance(value, str):
                raise MCPBridgeError("Credential provider returned invalid HTTP headers")
            if any(char in name + value for char in "\r\n"):
                raise MCPBridgeError("Credential provider returned invalid HTTP headers")
            headers[name] = value
        return headers

    @asynccontextmanager
    async def _session(
        self,
        server_name: str,
        transport: str,
        endpoint: str | None,
    ) -> AsyncIterator[tuple[ClientSession, Any]]:
        if transport == "stdio":
            server_config = self._stdio_server_configs.get(server_name)
            if server_config is None:
                raise MCPBridgeError("MCP stdio server is not configured")
            async with stdio_client(server_config) as (read, write), ClientSession(
                    read,
                    write,
                    read_timeout_seconds=timedelta(seconds=self._timeout_seconds),
            ) as session:
                yield session, await session.initialize()
            return

        if endpoint is None:
            raise MCPBridgeError("An explicitly configured MCP endpoint is required")
        async with self._http_client_factory(
            headers=self._headers(server_name),
            timeout=self._timeout_seconds,
            trust_env=False,
            follow_redirects=False,
        ) as http_client, streamable_http_client(
            endpoint,
            http_client=http_client,
        ) as (read, write, _), ClientSession(
                    read,
                    write,
                    read_timeout_seconds=timedelta(seconds=self._timeout_seconds),
        ) as session:
            yield session, await session.initialize()

    @staticmethod
    def _schema_digest(schema: dict[str, Any]) -> str:
        try:
            return hashlib.sha256(rfc8785.dumps(schema)).hexdigest()
        except (rfc8785.CanonicalizationError, ValueError, TypeError) as exc:
            raise MCPBridgeError("MCP server returned a non-canonical tool schema") from exc

    @staticmethod
    def _is_read_only(tool: Any) -> bool:
        annotations = getattr(tool, "annotations", None)
        return (
            annotations is not None
            and getattr(annotations, "readOnlyHint", None) is True
            and getattr(annotations, "destructiveHint", None) is not True
        )

    async def _discover_tools(self, session: ClientSession) -> list[Any]:
        tools: list[Any] = []
        cursor: str | None = None
        for _ in range(20):
            page = await session.list_tools(cursor=cursor)
            tools.extend(page.tools)
            if len(tools) > 500:
                raise MCPBridgeError("MCP server exceeded the discovered-tool limit")
            cursor = page.nextCursor
            if not cursor:
                return tools
        raise MCPBridgeError("MCP server exceeded the tool-pagination limit")

    async def connect_server(
        self,
        server_name: str,
        transport: str = "streamable-http",
        endpoint: str | None = None,
        provided_tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Initialize a real MCP session and register only qualified read tools."""
        self._validate_server_name(server_name)
        if transport == "http":
            transport = "streamable-http"
        if transport == "stdio":
            if endpoint is not None:
                raise MCPBridgeError("MCP stdio configuration cannot include an endpoint")
            if server_name not in self._stdio_server_configs:
                raise MCPBridgeError("MCP stdio server is not configured")
        else:
            if endpoint is None:
                raise MCPBridgeError("An explicitly configured MCP endpoint is required")
            endpoint = self._validate_endpoint(endpoint, transport)
        if provided_tools is not None:
            raise MCPBridgeError("Tool metadata must come from live MCP discovery")
        allowed_tools = self._read_only_allowlist.get(server_name, frozenset())
        try:
            async with self._session(server_name, transport, endpoint) as (session, initialized):
                discovered = await self._discover_tools(session)
        except MCPBridgeError:
            raise
        except Exception as exc:
            raise MCPConnectionError(
                f"MCP server initialization or discovery failed: {type(exc).__name__}"
            ) from exc

        server_info_model = getattr(initialized, "serverInfo", None)
        remote_server_info = (
            server_info_model.model_dump(mode="json", exclude_none=True)
            if server_info_model is not None
            else {}
        )
        remote_version = str(remote_server_info.get("version") or "unknown")
        registered: list[str] = []
        discovered_unqualified: list[str] = []
        routes: dict[str, dict[str, Any]] = {}
        tools_engine = get_tool_contract_engine()

        for tool in discovered:
            if tool.name not in allowed_tools or not self._is_read_only(tool):
                discovered_unqualified.append(tool.name)
                continue
            schema = tool.inputSchema
            if not isinstance(schema, dict) or len(rfc8785.dumps(schema)) > 64_000:
                raise MCPBridgeError(f"MCP tool schema is invalid or oversized: {tool.name}")
            schema_digest = self._schema_digest(schema)
            local_name = f"{server_name}__{tool.name}"
            version = f"{remote_version}-{schema_digest[:12]}"
            try:
                contract = tools_engine.register_tool(
                    name=local_name,
                    description=tool.description or tool.name,
                    schema=schema,
                    version=version,
                    category=f"external_mcp_{server_name}",
                    tags=["external_mcp", server_name, "read_only"],
                )
            except (TypeError, ValueError) as exc:
                raise MCPBridgeError(f"MCP tool contract is invalid: {tool.name}") from exc
            registered.append(contract.name)
            routes[contract.name] = {
                "server_name": server_name,
                "remote_name": tool.name,
                "endpoint": endpoint,
                "transport": transport,
                "schema_digest": schema_digest,
            }

        info = {
            "server_name": server_name,
            "transport": transport,
            "endpoint": endpoint,
            "last_initialized_at": time.time(),
            "protocol_version": initialized.protocolVersion,
            "server_info": remote_server_info,
            "tools_registered": sorted(registered),
            "tools_unqualified": sorted(discovered_unqualified),
            "session_lifecycle": "per_call",
            "status": "available",
        }
        with self._lock:
            for local_name, route in routes.items():
                self._tool_routes[local_name] = route
            self._available_servers[server_name] = info
        return dict(info)

    async def invoke_external_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        caller_id: str = "harness-step-executor",
    ) -> dict[str, Any]:
        """Revalidate live schema and return the actual result from an allowlisted MCP server."""
        with self._lock:
            route = self._tool_routes.get(tool_name)
        if route is None:
            raise MCPToolUnavailable("MCP tool is not currently qualified")
        server_name = route["server_name"]
        if route["remote_name"] not in self._read_only_allowlist.get(server_name, frozenset()):
            raise MCPToolUnavailable("MCP tool is no longer allowlisted")
        validation = get_tool_contract_engine().validate_call(tool_name, arguments)
        if not validation.valid:
            raise ValueError(f"Tool validation failed: {'; '.join(validation.errors)}")

        try:
            async with self._session(
                server_name,
                route["transport"],
                route["endpoint"],
            ) as (session, _):
                current_tools = await self._discover_tools(session)
                current = next(
                    (item for item in current_tools if item.name == route["remote_name"]), None
                )
                if (
                    current is None
                    or not self._is_read_only(current)
                    or self._schema_digest(current.inputSchema) != route["schema_digest"]
                ):
                    raise MCPToolUnavailable("MCP tool schema or read-only qualification changed")
                result = await session.call_tool(route["remote_name"], arguments=arguments)
        except MCPBridgeError:
            raise
        except Exception as exc:
            raise MCPConnectionError(
                f"MCP tool invocation failed: {type(exc).__name__}"
            ) from exc

        output = result.model_dump(mode="json", exclude_none=True)
        encoded = json.dumps(output, ensure_ascii=False, allow_nan=False).encode("utf-8")
        if len(encoded) > self._max_result_bytes:
            raise MCPBridgeError("MCP tool response exceeded the configured result-size limit")
        return {
            "tool_name": tool_name,
            "remote_tool_name": route["remote_name"],
            "server_name": server_name,
            "caller_id": caller_id,
            "status": "FAILED" if result.isError else "SUCCEEDED",
            "output": output,
        }

    def list_connected_servers(self) -> list[dict[str, Any]]:
        """List servers successfully initialized; sessions are opened per operation."""
        with self._lock:
            return [dict(item) for item in self._available_servers.values()]


_mcp_client_instance: ExternalMCPClient | None = None
_attestor_instance: ToolExecutionAttestor | None = None
_lock = threading.RLock()


def get_external_mcp_client() -> ExternalMCPClient:
    global _mcp_client_instance
    if _mcp_client_instance is None:
        with _lock:
            if _mcp_client_instance is None:
                try:
                    raw_tool_allowlist = json.loads(
                        os.getenv("EOIP_MCP_READ_ONLY_TOOLS", "{}")
                    )
                except json.JSONDecodeError as exc:
                    raise MCPBridgeError("EOIP_MCP_READ_ONLY_TOOLS must be valid JSON") from exc
                if not isinstance(raw_tool_allowlist, dict) or any(
                    not isinstance(server, str)
                    or not isinstance(tools, list)
                    or any(not isinstance(tool, str) for tool in tools)
                    for server, tools in raw_tool_allowlist.items()
                ):
                    raise MCPBridgeError(
                        "EOIP_MCP_READ_ONLY_TOOLS must map server names to tool-name arrays"
                    )
                try:
                    raw_stdio_servers = json.loads(
                        os.getenv("EOIP_MCP_STDIO_SERVERS", "{}")
                    )
                except json.JSONDecodeError as exc:
                    raise MCPBridgeError("EOIP_MCP_STDIO_SERVERS must be valid JSON") from exc
                if not isinstance(raw_stdio_servers, dict):
                    raise MCPBridgeError("EOIP_MCP_STDIO_SERVERS must map names to server configurations")

                stdio_server_configs: dict[str, StdioServerParameters] = {}
                for server_name, config in raw_stdio_servers.items():
                    if (
                        not isinstance(server_name, str)
                        or not isinstance(config, dict)
                        or set(config) - {"command", "args", "env", "cwd"}
                    ):
                        raise MCPBridgeError("MCP stdio server configuration is invalid")
                    ExternalMCPClient._validate_server_name(server_name)
                    command = config.get("command")
                    args = config.get("args", [])
                    env = config.get("env", {})
                    cwd = config.get("cwd")
                    if (
                        not isinstance(command, str)
                        or not command
                        or not isinstance(args, list)
                        or any(not isinstance(arg, str) for arg in args)
                        or not isinstance(env, dict)
                        or any(not isinstance(key, str) or not isinstance(value, str) for key, value in env.items())
                        or (cwd is not None and not isinstance(cwd, str))
                    ):
                        raise MCPBridgeError("MCP stdio server configuration is invalid")
                    stdio_server_configs[server_name] = StdioServerParameters(
                        command=command,
                        args=args,
                        env=env or None,
                        cwd=cwd,
                    )

                def credential_provider(server_name: str) -> Mapping[str, str]:
                    if server_name not in raw_tool_allowlist:
                        raise MCPBridgeError("MCP server is not configured")
                    token_key = "EOIP_MCP_BEARER_TOKEN_" + re.sub(
                        r"[^A-Za-z0-9]", "_", server_name
                    ).upper()
                    token = os.getenv(token_key)
                    return {"Authorization": f"Bearer {token}"} if token else {}

                _mcp_client_instance = ExternalMCPClient(
                    read_only_tool_allowlist=raw_tool_allowlist,
                    stdio_server_configs=stdio_server_configs,
                    credential_provider=credential_provider,
                )
    return _mcp_client_instance


def get_tool_execution_attestor() -> ToolExecutionAttestor:
    global _attestor_instance
    if _attestor_instance is None:
        with _lock:
            if _attestor_instance is None:
                key = os.getenv("EOIP_TOOL_ATTESTATION_HMAC_KEY")
                if not key:
                    raise RuntimeError("Legacy HMAC integrity key is not configured")
                _attestor_instance = ToolExecutionAttestor(signing_secret=key)
    return _attestor_instance
