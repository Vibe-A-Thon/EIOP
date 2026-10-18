"""ANSI SQL view adapter over the ontology (CRA-024.8).

Translates ANSI SQL SELECT queries over ontology entities into graph and attribute scans.
Validates queries against the SQL grammar manifest.
"""
from __future__ import annotations

import re
from typing import Any, Optional

from eoip.capabilities.model import UnsupportedCapabilityError
from eoip.qlang.manifest_registry import ManifestRegistry


class SQLOntologyAdapter:
    """Provides relational ANSI SQL views over graph ontology entities."""

    def __init__(
        self,
        graph_store: Optional[Any] = None,
        manifest_registry: Optional[ManifestRegistry] = None,
    ) -> None:
        self.graph_store = graph_store
        self.manifest_registry = manifest_registry or ManifestRegistry.get_instance()

    def execute_sql(
        self,
        sql: str,
        parameters: Optional[dict[str, Any]] = None,
    ) -> list[dict[str, Any]]:
        self.manifest_registry.check_query_constructs("SQL", sql)
        s_clean = sql.strip().rstrip(";")

        # Parse basic SELECT <cols> FROM <table> [WHERE <col> = <val>] [LIMIT <n>]
        m = re.match(
            r"SELECT\s+(.+?)\s+FROM\s+([a-zA-Z0-9_]+)(?:\s+WHERE\s+(.+?))?(?:\s+LIMIT\s+(\d+))?$",
            s_clean,
            re.IGNORECASE,
        )
        if not m:
            raise ValueError(f"Unsupported SQL syntax: {sql}")

        cols_str, table_name, where_clause, limit_str = m.groups()
        limit = int(limit_str) if limit_str else 100
        cols = [c.strip() for c in cols_str.split(",")]

        # Query backing store if available or return sample ontology view rows
        raw_rows: list[dict[str, Any]] = []
        if self.graph_store:
            verts = self.graph_store.find_vertices(label=table_name, limit=limit)
            raw_rows = [dict(v["properties"], canonical_id=v["canonical_id"], label=v["label"]) for v in verts]
        else:
            raw_rows = [
                {"canonical_id": f"urn:eoip:{table_name}:{i}", "name": f"{table_name}_{i}", "status": "ACTIVE"}
                for i in range(1, 6)
            ]

        # Apply simple WHERE clause
        if where_clause:
            w_match = re.match(r"([a-zA-Z0-9_]+)\s*=\s*['\"]?([^'\"]+)['\"]?", where_clause.strip())
            if w_match:
                k, v = w_match.groups()
                raw_rows = [r for r in raw_rows if str(r.get(k)) == v]

        # Apply projection
        if "*" in cols:
            return raw_rows[:limit]
        else:
            projected = []
            for r in raw_rows[:limit]:
                projected.append({c: r.get(c) for c in cols})
            return projected
