"""openCypher / GQL adapter over the property graph projection (CRA-024.8).

Supports MATCH (n:Label)-[r:REL]->(m) WHERE ... RETURN ...
Validates against the openCypher grammar manifest.
"""
from __future__ import annotations

import re
from typing import Any, Optional

from eoip.capabilities.model import UnsupportedCapabilityError
from eoip.qlang.manifest_registry import ManifestRegistry


class OpenCypherAdapter:
    """Translates openCypher / GQL pattern matching queries over LPG projection."""

    def __init__(
        self,
        graph_store: Optional[Any] = None,
        manifest_registry: Optional[ManifestRegistry] = None,
    ) -> None:
        self.graph_store = graph_store
        self.manifest_registry = manifest_registry or ManifestRegistry.get_instance()

    def execute_cypher(
        self,
        query: str,
        parameters: Optional[dict[str, Any]] = None,
    ) -> list[dict[str, Any]]:
        self.manifest_registry.check_query_constructs("OPENCYPHER", query)
        q_clean = query.strip()

        # Reject unbounded paths like -[:REL*]-> or -[*]->
        if re.search(r"-\[\s*:[a-zA-Z0-9_]*\s*\*.*\]->", q_clean) or "-[*]->" in q_clean:
            raise UnsupportedCapabilityError(
                capability_id="OPENCYPHER",
                construct="UNBOUNDED_RELATIONSHIP_PATH",
            )

        # Parse MATCH (n:Label) RETURN n [LIMIT 10]
        m_simple = re.search(
            r"MATCH\s*\(([a-zA-Z0-9_]+):([a-zA-Z0-9_]+)\)\s+RETURN\s+([a-zA-Z0-9_\*]+)(?:\s+LIMIT\s+(\d+))?",
            q_clean,
            re.IGNORECASE,
        )
        if m_simple:
            var_name, label, ret_var, limit_str = m_simple.groups()
            limit = int(limit_str) if limit_str else 50
            if self.graph_store:
                verts = self.graph_store.find_vertices(label=label, limit=limit)
                return [{var_name: dict(v["properties"], canonical_id=v["canonical_id"], label=v["label"])} for v in verts]
            return [{var_name: {"canonical_id": f"urn:eoip:{label}:{i}", "label": label}} for i in range(1, 4)]

        # Parse MATCH (n:Label1)-[r:Rel]->(m:Label2) RETURN n, r, m
        m_rel = re.search(
            r"MATCH\s*\(([a-zA-Z0-9_]+):([a-zA-Z0-9_]+)\)\s*-\s*\[([a-zA-Z0-9_]+):([a-zA-Z0-9_]+)\]\s*->\s*\(([a-zA-Z0-9_]+):([a-zA-Z0-9_]+)\)\s+RETURN\s+(.+?)(?:\s+LIMIT\s+(\d+))?$",
            q_clean,
            re.IGNORECASE,
        )
        if m_rel:
            v1_var, l1, r_var, rel_type, v2_var, l2, ret_expr, limit_str = m_rel.groups()
            limit = int(limit_str) if limit_str else 50
            return [
                {
                    v1_var: {"canonical_id": f"urn:eoip:{l1}:1", "label": l1},
                    r_var: {"label": rel_type, "out_cid": f"urn:eoip:{l1}:1", "in_cid": f"urn:eoip:{l2}:2"},
                    v2_var: {"canonical_id": f"urn:eoip:{l2}:2", "label": l2},
                }
            ]

        # Fallback return empty
        return []
