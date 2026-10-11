"""API gateway — flexible query layer with schema introspection and rate limiting.

Provides a GraphQL-style query interface over the knowledge graph, schema
introspection for API playground support, token-bucket rate limiting,
and OpenAPI spec export metadata.
"""

from __future__ import annotations

import hashlib
import threading
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SchemaField:
    __slots__ = ("name", "field_type", "nullable", "description", "default")

    def __init__(self, name: str, field_type: str = "String",
                 nullable: bool = True, description: str = "",
                 default: Any = None) -> None:
        self.name = name
        self.field_type = field_type
        self.nullable = nullable
        self.description = description
        self.default = default

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "type": self.field_type,
            "nullable": self.nullable,
            "description": self.description,
            "default": self.default,
        }


class SchemaType:
    __slots__ = ("name", "description", "fields", "relationships")

    def __init__(self, name: str, description: str = "",
                 fields: list[SchemaField] | None = None,
                 relationships: list[str] | None = None) -> None:
        self.name = name
        self.description = description
        self.fields = fields or []
        self.relationships = relationships or []

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "fields": [f.to_dict() for f in self.fields],
            "relationships": list(self.relationships),
        }


@dataclass
class FieldNode:
    name: str
    alias: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)
    children: list[FieldNode] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"name": self.name}
        if self.alias:
            d["alias"] = self.alias
        if self.arguments:
            d["arguments"] = self.arguments
        if self.children:
            d["children"] = [c.to_dict() for c in self.children]
        return d


@dataclass
class GatewayQuery:
    query_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    root_type: str = ""
    fields: list[FieldNode] = field(default_factory=list)
    filters: dict[str, Any] = field(default_factory=dict)
    limit: int = 100
    offset: int = 0
    raw_query: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "query_id": self.query_id,
            "root_type": self.root_type,
            "fields": [f.to_dict() for f in self.fields],
            "filters": self.filters,
            "limit": self.limit,
            "offset": self.offset,
        }


@dataclass
class GatewayResult:
    query_id: str
    data: list[dict[str, Any]]
    total_count: int = 0
    page_size: int = 0
    has_more: bool = False
    latency_ms: float = 0.0
    resolved_types: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "query_id": self.query_id,
            "data": self.data,
            "total_count": self.total_count,
            "page_size": self.page_size,
            "has_more": self.has_more,
            "latency_ms": round(self.latency_ms, 2),
            "resolved_types": self.resolved_types,
            "errors": self.errors,
        }


@dataclass
class RateLimitPolicy:
    name: str
    requests_per_second: float = 10.0
    burst_size: int = 20
    per_client: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "requests_per_second": self.requests_per_second,
            "burst_size": self.burst_size,
            "per_client": self.per_client,
        }


class RateLimiter:
    """Token-bucket rate limiter with per-client tracking."""

    def __init__(self, policy: RateLimitPolicy) -> None:
        self._policy = policy
        self._lock = threading.Lock()
        self._buckets: dict[str, tuple[float, float]] = {}

    @property
    def policy(self) -> RateLimitPolicy:
        return self._policy

    def allow(self, client_id: str = "__global__") -> tuple[bool, dict[str, Any]]:
        key = client_id if self._policy.per_client else "__global__"
        now = time.time()
        with self._lock:
            tokens, last_refill = self._buckets.get(
                key, (float(self._policy.burst_size), now)
            )
            elapsed = now - last_refill
            tokens = min(
                float(self._policy.burst_size),
                tokens + elapsed * self._policy.requests_per_second,
            )
            if tokens >= 1.0:
                tokens -= 1.0
                self._buckets[key] = (tokens, now)
                return True, {
                    "remaining": int(tokens),
                    "limit": self._policy.burst_size,
                    "reset_seconds": round(
                        (self._policy.burst_size - tokens)
                        / max(self._policy.requests_per_second, 0.01),
                        2,
                    ),
                }
            self._buckets[key] = (tokens, now)
            retry_after = (1.0 - tokens) / max(
                self._policy.requests_per_second, 0.01
            )
            return False, {
                "remaining": 0,
                "limit": self._policy.burst_size,
                "retry_after_seconds": round(retry_after, 2),
            }

    def reset(self, client_id: str | None = None) -> None:
        with self._lock:
            if client_id:
                self._buckets.pop(client_id, None)
            else:
                self._buckets.clear()

    def stats(self) -> dict[str, Any]:
        with self._lock:
            return {
                "policy": self._policy.to_dict(),
                "active_clients": len(self._buckets),
            }


def _parse_simple_query(raw: str) -> GatewayQuery:
    """Parse a simplified GraphQL-like query string into a GatewayQuery."""
    raw = raw.strip()
    q = GatewayQuery(raw_query=raw)

    import re
    type_match = re.match(r"(\w+)\s*(?:\(([^)]*)\))?\s*\{([^}]*)\}", raw)
    if not type_match:
        q.root_type = raw.split()[0] if raw else ""
        return q

    q.root_type = type_match.group(1)

    if type_match.group(2):
        for pair in type_match.group(2).split(","):
            pair = pair.strip()
            if ":" in pair:
                k, v = pair.split(":", 1)
                v = v.strip().strip('"').strip("'")
                try:
                    q.filters[k.strip()] = int(v)
                except ValueError:
                    try:
                        q.filters[k.strip()] = float(v)
                    except ValueError:
                        q.filters[k.strip()] = v

    if type_match.group(3):
        for f in type_match.group(3).split(","):
            f = f.strip()
            if f:
                parts = f.split(":", 1)
                if len(parts) == 2:
                    q.fields.append(FieldNode(name=parts[1].strip(), alias=parts[0].strip()))
                else:
                    q.fields.append(FieldNode(name=f))

    return q


class APIGateway:
    """Flexible query gateway with schema introspection and rate limiting."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._types: dict[str, SchemaType] = {}
        self._data_sources: dict[str, list[dict[str, Any]]] = {}
        self._rate_limiter: RateLimiter | None = None
        self._query_log: deque[dict[str, Any]] = deque(maxlen=1000)

    def register_type(self, schema_type: SchemaType) -> None:
        with self._lock:
            self._types[schema_type.name] = schema_type

    def register_data_source(self, type_name: str,
                             records: list[dict[str, Any]]) -> None:
        with self._lock:
            self._data_sources[type_name] = records

    def set_rate_limit(self, policy: RateLimitPolicy) -> None:
        self._rate_limiter = RateLimiter(policy)

    def introspect(self) -> dict[str, Any]:
        with self._lock:
            return {
                "types": {n: t.to_dict() for n, t in self._types.items()},
                "type_count": len(self._types),
            }

    def introspect_type(self, type_name: str) -> dict[str, Any] | None:
        t = self._types.get(type_name)
        return t.to_dict() if t else None

    def execute(self, raw_query: str,
                client_id: str = "__anonymous__") -> GatewayResult:
        start = time.time()

        if self._rate_limiter:
            allowed, info = self._rate_limiter.allow(client_id)
            if not allowed:
                return GatewayResult(
                    query_id=uuid.uuid4().hex[:12],
                    data=[],
                    errors=[f"Rate limited. Retry after {info.get('retry_after_seconds', 1)}s"],
                    latency_ms=(time.time() - start) * 1000,
                )

        query = _parse_simple_query(raw_query)

        with self._lock:
            records = self._data_sources.get(query.root_type, [])

        filtered = []
        for rec in records:
            match = True
            for k, v in query.filters.items():
                if rec.get(k) != v:
                    match = False
                    break
            if match:
                filtered.append(rec)

        total = len(filtered)
        page = filtered[query.offset : query.offset + query.limit]

        if query.fields:
            field_names = [f.name for f in query.fields]
            projected = []
            for rec in page:
                projected.append({f: rec.get(f) for f in field_names})
            page = projected

        result = GatewayResult(
            query_id=query.query_id,
            data=page,
            total_count=total,
            page_size=len(page),
            has_more=(query.offset + query.limit) < total,
            latency_ms=(time.time() - start) * 1000,
            resolved_types=[query.root_type] if query.root_type in self._types else [],
        )

        self._query_log.append({
            "query_id": query.query_id,
            "root_type": query.root_type,
            "client_id": client_id,
            "timestamp": time.time(),
            "latency_ms": result.latency_ms,
            "result_count": len(page),
            "has_errors": bool(result.errors),
        })

        return result

    def export_openapi_spec(self) -> dict[str, Any]:
        paths: dict[str, Any] = {}
        schemas: dict[str, Any] = {}

        for name, st in self._types.items():
            props: dict[str, Any] = {}
            for f in st.fields:
                props[f.name] = {
                    "type": f.field_type.lower(),
                    "nullable": f.nullable,
                    "description": f.description,
                }
            schemas[name] = {
                "type": "object",
                "properties": props,
                "description": st.description,
            }
            paths[f"/api/v1/graph/{name.lower()}"] = {
                "get": {
                    "summary": f"Query {name} entities",
                    "parameters": [
                        {"name": "limit", "in": "query", "schema": {"type": "integer"}},
                        {"name": "offset", "in": "query", "schema": {"type": "integer"}},
                    ],
                    "responses": {"200": {"description": f"List of {name} entities"}},
                },
            }

        return {
            "openapi": "3.1.0",
            "info": {"title": "EOIP Knowledge Graph API", "version": "1.0.0"},
            "paths": paths,
            "components": {"schemas": schemas},
        }

    def playground_metadata(self) -> dict[str, Any]:
        return {
            "available_types": list(self._types.keys()),
            "query_syntax": "TypeName(filter_key: value) { field1, field2 }",
            "example_queries": [
                f"{name}() {{ {', '.join(f.name for f in st.fields[:3])} }}"
                for name, st in list(self._types.items())[:5]
            ],
            "rate_limit": self._rate_limiter.stats() if self._rate_limiter else None,
        }

    def query_log(self, limit: int = 50) -> list[dict[str, Any]]:
        return list(self._query_log)[-limit:]

    def stats(self) -> dict[str, Any]:
        return {
            "registered_types": len(self._types),
            "data_sources": len(self._data_sources),
            "total_records": sum(len(r) for r in self._data_sources.values()),
            "queries_logged": len(self._query_log),
            "rate_limiter_active": self._rate_limiter is not None,
        }


_instance: APIGateway | None = None
_lock = threading.Lock()


def get_api_gateway() -> APIGateway:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = APIGateway()
    return _instance
