"""Tool/API contract and schema design engine with MCP compatibility."""

from __future__ import annotations

import hashlib
import json
import threading
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolContract:
    name: str
    description: str
    schema: dict[str, Any]
    version: str = "1.0.0"
    category: str = ""
    tags: list[str] = field(default_factory=list)
    registered_at: float = field(default_factory=time.time)

    @property
    def fingerprint(self) -> str:
        payload = json.dumps(
            {"name": self.name, "version": self.version, "schema": self.schema},
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode()).hexdigest()[:12]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "schema": self.schema,
            "category": self.category,
            "tags": self.tags,
            "fingerprint": self.fingerprint,
            "registered_at": self.registered_at,
        }

    def to_mcp_tool(self) -> dict[str, Any]:
        """Format as official Model Context Protocol (MCP) tool descriptor."""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.schema,
        }


@dataclass
class ToolValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)


class ToolContractEngine:
    """Registry for MCP-style tool contracts and JSON-schema envelopes."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._contracts: dict[str, ToolContract] = {}

        # Pre-seed standard built-in enterprise tools
        self.register_tool(
            "graph_entity_lookup",
            "Lookup entity vertices by canonical ID or search query in graph store",
            {
                "type": "object",
                "properties": {
                    "entity_id": {"type": "string", "description": "Canonical ID of target entity"},
                    "limit": {"type": "integer", "description": "Maximum results to retrieve", "default": 10},
                },
                "required": ["entity_id"],
            },
            version="1.0.0",
            category="mcp_graph",
            tags=["graph", "retrieval", "lookup"],
        )
        self.register_tool(
            "causal_blast_radius",
            "Evaluate cascade shock and blast radius for a node failure",
            {
                "type": "object",
                "properties": {
                    "source_node": {"type": "string", "description": "Originating failed entity"},
                    "shock_magnitude": {"type": "number", "description": "Shock force between 0.0 and 1.0", "default": 0.5},
                },
                "required": ["source_node"],
            },
            version="1.0.0",
            category="mcp_causal",
            tags=["causal", "blast_radius", "resilience"],
        )

    def register_tool(
        self,
        name: str,
        description: str,
        schema: dict[str, Any],
        *,
        version: str = "1.0.0",
        category: str = "",
        tags: list[str] | None = None,
    ) -> ToolContract:
        result = self.validate_schema(schema)
        if not result.valid:
            raise ValueError("; ".join(result.errors))
        contract = ToolContract(
            name=name,
            description=description,
            schema=dict(schema),
            version=version,
            category=category,
            tags=tags or [],
        )
        with self._lock:
            self._contracts[f"{name}:{version}"] = contract
        return contract

    def get_tool(self, name: str, version: str | None = None) -> ToolContract | None:
        with self._lock:
            if version:
                return self._contracts.get(f"{name}:{version}")
            # Get latest matching name
            matches = [c for c in self._contracts.values() if c.name == name]
            return matches[-1] if matches else None

    def validate_schema(self, schema: dict[str, Any]) -> ToolValidationResult:
        errors: list[str] = []
        if not isinstance(schema, dict):
            errors.append("schema must be an object")
        elif schema:
            if schema.get("type") not in (None, "object"):
                errors.append("root schema type must be object")
            properties = schema.get("properties", {})
            if properties is not None and not isinstance(properties, dict):
                errors.append("properties must be an object")
            required = schema.get("required", [])
            if required is not None and not isinstance(required, list):
                errors.append("required must be a list")
        return ToolValidationResult(valid=not errors, errors=errors)

    def validate_call(self, tool_name: str, arguments: dict[str, Any]) -> ToolValidationResult:
        """Validate runtime call parameters against the registered tool contract schema."""
        tool = self.get_tool(tool_name)
        if not tool:
            return ToolValidationResult(valid=False, errors=[f"Tool '{tool_name}' not found."])

        errors: list[str] = []
        schema = tool.schema
        required_fields = schema.get("required", [])
        for field in required_fields:
            if field not in arguments:
                errors.append(f"Missing required parameter '{field}' for tool '{tool_name}'")

        properties = schema.get("properties", {})
        for arg_name, arg_val in arguments.items():
            if arg_name in properties:
                expected_type = properties[arg_name].get("type")
                if expected_type == "string" and not isinstance(arg_val, str):
                    errors.append(f"Parameter '{arg_name}' must be a string, got {type(arg_val).__name__}")
                elif expected_type == "integer" and not isinstance(arg_val, int):
                    errors.append(f"Parameter '{arg_name}' must be an integer, got {type(arg_val).__name__}")
                elif expected_type == "number" and not isinstance(arg_val, (int, float)):
                    errors.append(f"Parameter '{arg_name}' must be a number, got {type(arg_val).__name__}")
                elif expected_type == "boolean" and not isinstance(arg_val, bool):
                    errors.append(f"Parameter '{arg_name}' must be a boolean, got {type(arg_val).__name__}")

        return ToolValidationResult(valid=not errors, errors=errors)

    def export_mcp_manifest(self) -> dict[str, Any]:
        """Export standardized Model Context Protocol (MCP) server manifest."""
        with self._lock:
            tools_list = [c.to_mcp_tool() for c in self._contracts.values()]
        return {
            "mcp_version": "2024-11-05",
            "server_info": {
                "name": "eoip-enterprise-mcp",
                "version": "1.0.0",
                "description": "EOIP Enterprise Living Brain Model Context Protocol Server",
            },
            "tools": tools_list,
        }

    def list_tools(self) -> list[ToolContract]:
        with self._lock:
            return list(self._contracts.values())

    def stats(self) -> dict[str, Any]:
        with self._lock:
            categories: dict[str, int] = {}
            for contract in self._contracts.values():
                key = contract.category or "uncategorized"
                categories[key] = categories.get(key, 0) + 1
            return {
                "engine": "tool_api_contract",
                "contracts": len(self._contracts),
                "categories": categories,
            }


_instance: ToolContractEngine | None = None
_lock = threading.Lock()


def get_tool_contract_engine() -> ToolContractEngine:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = ToolContractEngine()
    return _instance

