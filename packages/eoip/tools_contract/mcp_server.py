"""Authorized in-process and HTTP MCP server exposing ontology, graph, and governed actions (CRA-039.2, CRA-039.7 / ONT-011)."""

from __future__ import annotations

import copy
import hashlib
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from collections.abc import Callable

from eoip.actions.contracts import (
    ActionError,
    ActionIntent,
    ActionState,
    ActionType,
    ApprovalGrant,
    RiskClass,
)
from eoip.actions.engine import ActionEngine
from eoip.graph.store import GraphStore
from eoip.ontology.manifest import DOMAINS, PROPERTY_KEYS, VERTEX_LABELS
from eoip.tools_contract.engine import ToolContract

logger = logging.getLogger("eoip.tools_contract.mcp_server")


class MCPBudgetExceededError(Exception):
    """Raised when an MCP tool invocation exceeds its allocated execution or query budget."""


class MCPIdentityViolationError(Exception):
    """Raised when an MCP caller attempts to alter trusted identity or elevate rights via arguments."""


@dataclass
class ToolBudget:
    max_timeout_sec: float = 30.0
    max_query_limit: int = 100
    max_graph_depth: int = 6
    max_payload_bytes: int = 1_000_000


@dataclass
class ToolProvenance:
    invocation_id: str
    tool_name: str
    caller_id: str
    tenant_id: str
    timestamp: float
    input_hash: str
    output_hash: str
    duration_ms: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "invocation_id": self.invocation_id,
            "tool_name": self.tool_name,
            "caller_id": self.caller_id,
            "tenant_id": self.tenant_id,
            "timestamp": self.timestamp,
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "duration_ms": self.duration_ms,
        }


@dataclass
class MCPToolDefinition:
    name: str
    description: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    handler: Callable[..., Any]
    budget: ToolBudget = field(default_factory=ToolBudget)

    def to_mcp_descriptor(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema,
            "outputSchema": self.output_schema,
        }


class EOIPMCPServer:
    """Enterprise Model Context Protocol server enforcing typed contracts, provenance, budgets, and security gates."""

    def __init__(
        self,
        graph_store: GraphStore | None = None,
        action_engine: ActionEngine | None = None,
    ) -> None:
        self.graph_store = graph_store
        self.action_engine = action_engine or ActionEngine(write_back_enabled=True)
        self.tools: dict[str, MCPToolDefinition] = {}
        self.provenance_log: list[ToolProvenance] = []
        self._register_all_tools()

    def _register_all_tools(self) -> None:
        # 1. Ontology Tools
        self.register_tool(
            name="ontology_list_classes",
            description="List all registered ontology vertex labels and metadata",
            input_schema={"type": "object", "properties": {}},
            output_schema={
                "type": "object",
                "properties": {
                    "classes": {"type": "array", "items": {"type": "string"}},
                    "domains": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["classes", "domains"],
            },
            handler=self._handle_ontology_list_classes,
        )

        self.register_tool(
            name="ontology_get_schema",
            description="Retrieve schema properties and data types for an ontology class",
            input_schema={
                "type": "object",
                "properties": {
                    "label": {"type": "string", "description": "Ontology class name (e.g. Project, WorkItem)"}
                },
                "required": ["label"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "valid": {"type": "boolean"},
                    "domain": {"type": "string"},
                },
                "required": ["label", "valid"],
            },
            handler=self._handle_ontology_get_schema,
        )

        # 2. Graph Retrieval Tools
        self.register_tool(
            name="graph_search",
            description="Search vertices by query string or property value",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search term"},
                    "limit": {"type": "integer", "description": "Max results (max 100)", "default": 25},
                },
                "required": ["query"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "results": {"type": "array", "items": {"type": "object"}},
                    "count": {"type": "integer"},
                },
                "required": ["results", "count"],
            },
            handler=self._handle_graph_search,
        )

        self.register_tool(
            name="graph_get_entity",
            description="Retrieve complete vertex and adjacent relationships by canonical ID",
            input_schema={
                "type": "object",
                "properties": {
                    "canonical_id": {"type": "string", "description": "Canonical ID of entity"}
                },
                "required": ["canonical_id"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "entity": {"type": "object"},
                    "found": {"type": "boolean"},
                },
                "required": ["found"],
            },
            handler=self._handle_graph_get_entity,
        )

        # 3. Governed Action Tools (ONT-011 / CRA-039.7)
        self.register_tool(
            name="action_propose",
            description="Propose or stage a governed action under policy gates",
            input_schema={
                "type": "object",
                "properties": {
                    "action_type_id": {"type": "string", "description": "Registered action type"},
                    "idempotency_key": {"type": "string", "description": "Idempotency key (16-128 chars)"},
                    "arguments": {"type": "object", "description": "Action payload arguments"},
                    "dry_run": {"type": "boolean", "default": False},
                },
                "required": ["action_type_id", "idempotency_key"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "intent_id": {"type": "string"},
                    "state": {"type": "string"},
                    "risk_class": {"type": "string"},
                    "requires_approval": {"type": "boolean"},
                },
                "required": ["intent_id", "state"],
            },
            handler=self._handle_action_propose,
        )

        self.register_tool(
            name="action_execute",
            description="Execute a previously approved or read-only action",
            input_schema={
                "type": "object",
                "properties": {
                    "intent_id": {"type": "string", "description": "ID of proposed intent"},
                    "approval_grant": {"type": "object", "description": "HMAC-signed approval grant if required"},
                },
                "required": ["intent_id"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "intent_id": {"type": "string"},
                    "state": {"type": "string"},
                    "executed": {"type": "boolean"},
                },
                "required": ["intent_id", "state", "executed"],
            },
            handler=self._handle_action_execute,
        )

    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any],
        output_schema: dict[str, Any],
        handler: Callable[..., Any],
        budget: ToolBudget | None = None,
    ) -> None:
        self.tools[name] = MCPToolDefinition(
            name=name,
            description=description,
            input_schema=input_schema,
            output_schema=output_schema,
            handler=handler,
            budget=budget or ToolBudget(),
        )

    def list_tools(self) -> list[dict[str, Any]]:
        """Returns standard MCP tool list descriptors."""
        return [tool.to_mcp_descriptor() for tool in self.tools.values()]

    def invoke_tool(
        self,
        name: str,
        arguments: dict[str, Any],
        caller_identity: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Invokes tool with strict identity binding, budget enforcement, and provenance logging."""
        tool = self.tools.get(name)
        if not tool:
            raise KeyError(f"MCP tool '{name}' not found")

        # 1. Identity isolation & anti-spoofing check (CRA-039.2)
        caller_id = (caller_identity or {}).get("user_id", "anonymous-agent")
        tenant_id = (caller_identity or {}).get("tenant_id", "default-tenant")

        # Disallow privilege escalation via natural language arguments or payload injection
        for suspect_key in ["tenant_id", "user_id", "caller_id", "override_role", "bypass_auth"]:
            if suspect_key in arguments:
                val = str(arguments[suspect_key])
                if val != caller_identity.get(suspect_key, ""):
                    raise MCPIdentityViolationError(
                        f"Natural language argument tampering detected: cannot alter trusted identity field '{suspect_key}' to '{val}'"
                    )

        # 2. Budget enforcement (CRA-039.2)
        if "limit" in arguments:
            requested_limit = int(arguments["limit"])
            if requested_limit > tool.budget.max_query_limit:
                raise MCPBudgetExceededError(
                    f"Requested limit {requested_limit} exceeds tool budget maximum of {tool.budget.max_query_limit}"
                )
        if "max_depth" in arguments:
            requested_depth = int(arguments["max_depth"])
            if requested_depth > tool.budget.max_graph_depth:
                raise MCPBudgetExceededError(
                    f"Requested max_depth {requested_depth} exceeds tool budget maximum of {tool.budget.max_graph_depth}"
                )

        t_start = time.perf_counter()
        raw_args_str = json.dumps(arguments, sort_keys=True)
        if len(raw_args_str.encode("utf-8")) > tool.budget.max_payload_bytes:
            raise MCPBudgetExceededError("Payload byte limit exceeded")

        # 3. Handler execution
        output = tool.handler(arguments, caller_id=caller_id, tenant_id=tenant_id)

        duration_ms = (time.perf_counter() - t_start) * 1000.0
        output_str = json.dumps(output, sort_keys=True, default=str)

        # 4. Provenance tracking
        prov = ToolProvenance(
            invocation_id=f"mcp-call-{uuid.uuid4().hex[:12]}",
            tool_name=name,
            caller_id=caller_id,
            tenant_id=tenant_id,
            timestamp=time.time(),
            input_hash=hashlib.sha256(raw_args_str.encode("utf-8")).hexdigest(),
            output_hash=hashlib.sha256(output_str.encode("utf-8")).hexdigest(),
            duration_ms=round(duration_ms, 2),
        )
        self.provenance_log.append(prov)

        return {
            "result": output,
            "provenance": prov.to_dict(),
        }

    # -------------------------------------------------------------------------
    # Internal Handlers
    # -------------------------------------------------------------------------

    def _handle_ontology_list_classes(self, args: dict[str, Any], caller_id: str, tenant_id: str) -> dict[str, Any]:
        return {
            "classes": sorted(VERTEX_LABELS),
            "domains": sorted(DOMAINS),
        }

    def _handle_ontology_get_schema(self, args: dict[str, Any], caller_id: str, tenant_id: str) -> dict[str, Any]:
        label = args.get("label", "")
        valid = label in VERTEX_LABELS
        return {
            "label": label,
            "valid": valid,
            "domain": "WORK" if label in {"Project", "WorkItem"} else "META",
            "property_count": len(PROPERTY_KEYS),
        }

    def _handle_graph_search(self, args: dict[str, Any], caller_id: str, tenant_id: str) -> dict[str, Any]:
        q = args.get("query", "")
        limit = min(int(args.get("limit", 25)), 100)
        results = []
        if self.graph_store:
            # Simple query over store
            for label in ["Project", "WorkItem", "Service"]:
                for v in self.graph_store.find_vertex_by_property(label, "name", q, limit=limit):
                    results.append({"canonical_id": v["canonical_id"], "label": v["label"], "properties": v["properties"]})
        return {"results": results, "count": len(results)}

    def _handle_graph_get_entity(self, args: dict[str, Any], caller_id: str, tenant_id: str) -> dict[str, Any]:
        cid = args.get("canonical_id", "")
        if self.graph_store:
            vertex = self.graph_store.get_vertex_by_canonical_id(cid)
            if vertex:
                return {"entity": vertex, "found": True}
        return {"entity": None, "found": False}

    def _handle_action_propose(self, args: dict[str, Any], caller_id: str, tenant_id: str) -> dict[str, Any]:
        action_type_id = args.get("action_type_id", "")
        idempotency_key = args.get("idempotency_key", "")
        payload = args.get("arguments", {})
        dry_run = args.get("dry_run", False)

        action_type = self.action_engine.get_action_type(action_type_id)
        target_instance = args.get("target_instance") or (action_type.target_connector if action_type else "graph_store")

        intent = ActionIntent(
            intent_id=f"intent-{uuid.uuid4().hex[:12]}",
            action_type_id=action_type_id,
            target_instance=target_instance,
            idempotency_key=idempotency_key,
            principal=caller_id,
            scope={"tenant_id": tenant_id},
            arguments=payload,
            dry_run=dry_run,
        )

        staged_intent = self.action_engine.propose_action(intent)
        requires_approval = action_type.risk_class != RiskClass.READ_ONLY if action_type else True

        return {
            "intent_id": staged_intent.intent_id,
            "state": staged_intent.state.value,
            "risk_class": action_type.risk_class.value if action_type else "UNKNOWN",
            "requires_approval": requires_approval,
            "dry_run_preview": staged_intent.details.get("dry_run_preview"),
        }

    def _handle_action_execute(self, args: dict[str, Any], caller_id: str, tenant_id: str) -> dict[str, Any]:
        intent_id = args.get("intent_id", "")
        grant_dict = args.get("approval_grant")
        grant = None
        if grant_dict:
            grant = ApprovalGrant(**grant_dict)

        result = self.action_engine.execute_action(intent_id, grant)
        return {
            "intent_id": intent_id,
            "state": result.get("state", "EXECUTED"),
            "executed": True,
            "read_back": result.get("read_back"),
        }
