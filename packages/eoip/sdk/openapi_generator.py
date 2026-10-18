"""OpenAPI contract generation, public API versioning, and error/event schema isolation (CRA-039.1)."""

from __future__ import annotations

import copy
import hashlib
import json
import logging
from typing import Any

logger = logging.getLogger("eoip.sdk.openapi_generator")

STANDARD_ERROR_SCHEMA = {
    "type": "object",
    "properties": {
        "error": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Standard UPPER_SNAKE error code",
                    "example": "ENTITY_NOT_FOUND",
                },
                "message": {
                    "type": "string",
                    "description": "Human-readable explanation of error",
                },
                "details": {
                    "type": "object",
                    "description": "Structured contextual error details",
                },
                "correlation_id": {
                    "type": "string",
                    "description": "Trace correlation identifier",
                },
            },
            "required": ["code", "message"],
        }
    },
    "required": ["error"],
}

EVENT_SCHEMAS = {
    "SourceEvent": {
        "type": "object",
        "properties": {
            "event_id": {"type": "string"},
            "source_system": {"type": "string"},
            "entity_type": {"type": "string"},
            "operation": {"type": "string", "enum": ["UPSERT", "DELETE", "MERGE"]},
            "timestamp": {"type": "string", "format": "date-time"},
            "payload": {"type": "object"},
        },
        "required": ["event_id", "source_system", "entity_type", "operation"],
    },
    "GraphMutationEvent": {
        "type": "object",
        "properties": {
            "mutation_id": {"type": "string"},
            "label": {"type": "string"},
            "canonical_id": {"type": "string"},
            "operation": {"type": "string"},
            "modified_properties": {"type": "array", "items": {"type": "string"}},
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["mutation_id", "canonical_id", "operation"],
    },
    "GovernedAuditEvent": {
        "type": "object",
        "properties": {
            "audit_id": {"type": "string"},
            "action_id": {"type": "string"},
            "actor_id": {"type": "string"},
            "risk_class": {"type": "string"},
            "verdict": {"type": "string"},
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["audit_id", "action_id", "actor_id", "verdict"],
    },
}


class OpenAPIGenerator:
    """Generates public, versioned OpenAPI contracts with isolated internal routes."""

    def __init__(self, raw_spec: dict[str, Any] | None = None) -> None:
        self.raw_spec = copy.deepcopy(raw_spec) if raw_spec else self._build_synthetic_spec()

    @staticmethod
    def _build_synthetic_spec() -> dict[str, Any]:
        """Synthetic fallback when runtime app instance is not passed."""
        return {
            "openapi": "3.1.0",
            "info": {
                "title": "Enterprise Ontology & Intelligence Platform Public API",
                "version": "1.0.0",
                "description": "Governed knowledge graph, ontology management, and semantic querying API.",
            },
            "paths": {
                "/api/v1/search": {
                    "get": {
                        "summary": "Search entities",
                        "operationId": "searchEntities",
                        "parameters": [
                            {"name": "q", "in": "query", "required": True, "schema": {"type": "string"}},
                            {"name": "limit", "in": "query", "required": False, "schema": {"type": "integer", "default": 25}},
                        ],
                        "responses": {
                            "200": {"description": "Matching entities found"},
                            "400": {"description": "Invalid query parameters", "content": {"application/json": {"schema": STANDARD_ERROR_SCHEMA}}},
                        },
                    }
                },
                "/api/v1/entities/{canonical_id}": {
                    "get": {
                        "summary": "Retrieve entity by canonical ID",
                        "operationId": "getEntity",
                        "parameters": [
                            {"name": "canonical_id", "in": "path", "required": True, "schema": {"type": "string"}},
                        ],
                        "responses": {
                            "200": {"description": "Entity details and neighborhood"},
                            "404": {"description": "Entity not found", "content": {"application/json": {"schema": STANDARD_ERROR_SCHEMA}}},
                        },
                    }
                },
                "/api/v1/query": {
                    "post": {
                        "summary": "Execute query plan",
                        "operationId": "executeQueryPlan",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {"type": "object", "required": ["root_type"]}
                                }
                            },
                        },
                        "responses": {
                            "200": {"description": "Query results"},
                            "422": {"description": "Unprocessable query", "content": {"application/json": {"schema": STANDARD_ERROR_SCHEMA}}},
                        },
                    }
                },
                "/api/v1/actions/propose": {
                    "post": {
                        "summary": "Propose governed action",
                        "operationId": "proposeAction",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {"type": "object", "required": ["action_type_id", "idempotency_key"]}
                                }
                            },
                        },
                        "responses": {
                            "200": {"description": "Action proposed or staged for review"},
                            "403": {"description": "Write-back disabled", "content": {"application/json": {"schema": STANDARD_ERROR_SCHEMA}}},
                        },
                    }
                },
                "/admin/ingestion/trigger": {
                    "post": {
                        "summary": "Internal ingestion trigger",
                        "operationId": "internalIngest",
                        "responses": {"200": {"description": "Internal run"}},
                    }
                },
                "/internal/debug/health": {
                    "get": {
                        "summary": "Internal low-level health debug",
                        "operationId": "internalDebug",
                        "responses": {"200": {"description": "Raw stats"}},
                    }
                },
            },
        }

    def generate_public_contract(
        self,
        public_version: str = "v1",
        include_events: bool = True,
    ) -> dict[str, Any]:
        """Extracts public endpoints, attaches standardized error and event schemas, and strips internal routes."""
        spec = copy.deepcopy(self.raw_spec)

        public_prefix = f"/api/{public_version}"
        filtered_paths = {}

        for path, path_item in spec.get("paths", {}).items():
            if path.startswith(public_prefix):
                # Ensure standard error schemas are associated
                cleaned_item = copy.deepcopy(path_item)
                for method, op in cleaned_item.items():
                    if isinstance(op, dict) and "responses" in op:
                        for err_code in ["400", "401", "403", "404", "422", "500", "default"]:
                            if err_code in op["responses"]:
                                op["responses"][err_code].setdefault(
                                    "content", {"application/json": {"schema": STANDARD_ERROR_SCHEMA}}
                                )
                filtered_paths[path] = cleaned_item

        spec["paths"] = filtered_paths

        # Add components/schemas
        spec.setdefault("components", {}).setdefault("schemas", {})
        spec["components"]["schemas"]["StandardError"] = STANDARD_ERROR_SCHEMA["properties"]["error"]

        if include_events:
            for event_name, event_schema in EVENT_SCHEMAS.items():
                spec["components"]["schemas"][event_name] = event_schema

        # Metadata
        spec["info"]["version"] = public_version
        spec["info"]["x-api-stability"] = "STABLE"
        spec["info"]["x-independent-lifecycle"] = True

        return spec

    def export_json(self, public_version: str = "v1") -> str:
        contract = self.generate_public_contract(public_version=public_version)
        return json.dumps(contract, indent=2, sort_keys=True)

    def digest(self, public_version: str = "v1") -> str:
        payload = self.export_json(public_version=public_version)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()
