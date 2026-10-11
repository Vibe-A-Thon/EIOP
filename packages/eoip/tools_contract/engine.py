"""Tool/API contract and schema design engine."""

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


@dataclass
class ToolValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)


class ToolContractEngine:
    """Registry for MCP-style tool contracts and JSON-schema envelopes."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._contracts: dict[str, ToolContract] = {}

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
