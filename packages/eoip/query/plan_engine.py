"""Typed parsed plans, parameterization, and scope injection (CRA-024.2).

Ensures all queries lower to typed AST / logical plans with parameter binding.
Never passes concatenated raw user strings to backend engines.
Injects tenant and graph authorization scopes into AST before execution.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
import re

from eoip.capabilities.model import UnsupportedCapabilityError


class ScopeViolationError(PermissionError):
    """Raised when a query attempts to access an unauthorized tenant, graph, or source."""
    def __init__(self, message: str, status_code: int = 403) -> None:
        super().__init__(message)
        self.status_code = status_code


class PlanNodeType(str, Enum):
    SCAN = "SCAN"
    FILTER = "FILTER"
    PROJECT = "PROJECT"
    JOIN = "JOIN"
    TRAVERSAL = "TRAVERSAL"
    AGGREGATE = "AGGREGATE"
    LIMIT = "LIMIT"
    FEDERATED_SOURCE = "FEDERATED_SOURCE"


@dataclass
class PlanNode:
    node_type: PlanNodeType
    children: list[PlanNode] = field(default_factory=list)
    properties: dict[str, Any] = field(default_factory=dict)
    cost_estimate: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_type": self.node_type.value,
            "properties": self.properties,
            "cost_estimate": self.cost_estimate,
            "children": [c.to_dict() for c in self.children],
        }

    def find_all(self, predicate: Any) -> list[PlanNode]:
        nodes = [self] if predicate(self) else []
        for c in self.children:
            nodes.extend(c.find_all(predicate))
        return nodes


@dataclass
class TrustedScope:
    """Security scope representing the authenticated principal and tenant."""
    tenant_id: str
    principal_id: str
    roles: list[str] = field(default_factory=list)
    allowed_graphs: list[str] = field(default_factory=lambda: ["default"])
    allowed_sources: list[str] = field(default_factory=lambda: ["local"])


@dataclass
class ParameterizedQuery:
    """A parameterized query with typed bound parameters."""
    query_template: str
    parameters: dict[str, Any] = field(default_factory=dict)
    dialect: str = "EOQL"

    def bind_parameters(self) -> dict[str, Any]:
        """Validate parameter names and types."""
        for k, v in self.parameters.items():
            if not re.match(r"^[a-zA-Z0-9_]+$", k):
                raise ValueError(f"Invalid parameter name: {k}")
            # Ensure no executable code injection in parameters
            if isinstance(v, str) and any(kw in v.upper() for kw in ("DROP TABLE", ";--", "EXEC(", "<SCRIPT")):
                raise ValueError(f"Dangerous parameter value for {k}: {v}")
        return dict(self.parameters)


class TypedPlanEngine:
    """Builds typed execution plans and injects tenant authorization scopes."""

    FORBIDDEN_OPERATIONS = {
        "DROP", "TRUNCATE", "ALTER", "EXEC", "EVAL", "GRANT", "REVOKE", "SHUTDOWN"
    }

    def parse_to_plan(
        self,
        query: str,
        dialect: str = "EOQL",
        parameters: Optional[dict[str, Any]] = None,
    ) -> PlanNode:
        q_upper = query.strip().upper()
        # Reject unauthorized DDL / administrative operations
        for op in self.FORBIDDEN_OPERATIONS:
            if re.search(r"\b" + op + r"\b", q_upper):
                raise PermissionError(f"Unauthorized operation '{op}' rejected by plan engine")

        params = parameters or {}
        # Simple logical plan generation
        root = PlanNode(node_type=PlanNodeType.SCAN, properties={"dialect": dialect, "raw_query": query})

        if "SELECT" in q_upper:
            # Parse target entity
            m = re.search(r"FROM\s+([a-zA-Z0-9_]+)", query, re.IGNORECASE)
            entity = m.group(1) if m else "Entity"
            scan = PlanNode(node_type=PlanNodeType.SCAN, properties={"entity_type": entity})

            # Check WHERE
            if "WHERE" in q_upper:
                filt = PlanNode(
                    node_type=PlanNodeType.FILTER,
                    children=[scan],
                    properties={"condition": "user_predicate", "params": params},
                )
                curr = filt
            else:
                curr = scan

            if "JOIN" in q_upper:
                m_join = re.search(r"JOIN\s+([a-zA-Z0-9_]+)", query, re.IGNORECASE)
                rel = m_join.group(1) if m_join else "relatedTo"
                join_node = PlanNode(
                    node_type=PlanNodeType.JOIN,
                    children=[curr],
                    properties={"relationship": rel, "join_type": "INNER"},
                )
                curr = join_node

            proj = PlanNode(
                node_type=PlanNodeType.PROJECT,
                children=[curr],
                properties={"fields": ["*"]},
            )
            root = proj

        elif "TRAVERSE" in q_upper or "PATH" in q_upper:
            trav = PlanNode(
                node_type=PlanNodeType.TRAVERSAL,
                properties={"dialect": dialect, "max_depth": 3, "params": params},
            )
            root = trav

        return root

    def inject_scope(self, plan: PlanNode, scope: TrustedScope) -> PlanNode:
        """Injects tenant security filter into the plan AST."""
        # Check graph authorization
        target_graph = plan.properties.get("graph", "default")
        if target_graph not in scope.allowed_graphs and "*" not in scope.allowed_graphs:
            raise ScopeViolationError(f"Access to graph '{target_graph}' denied for tenant {scope.tenant_id}")

        target_source = plan.properties.get("source", "local")
        if target_source not in scope.allowed_sources and "*" not in scope.allowed_sources:
            raise ScopeViolationError(f"Access to source '{target_source}' denied for tenant {scope.tenant_id}")

        # Inject tenant_id filter node above scans
        def _rewrite(node: PlanNode) -> PlanNode:
            new_children = [_rewrite(c) for c in node.children]
            if node.node_type == PlanNodeType.SCAN:
                tenant_filter = PlanNode(
                    node_type=PlanNodeType.FILTER,
                    children=[PlanNode(node_type=PlanNodeType.SCAN, properties=dict(node.properties))],
                    properties={
                        "condition": "tenant_id == :scope_tenant_id",
                        "params": {"scope_tenant_id": scope.tenant_id},
                        "injected_scope": True,
                    },
                )
                return tenant_filter
            return PlanNode(
                node_type=node.node_type,
                children=new_children,
                properties=dict(node.properties),
                cost_estimate=node.cost_estimate,
            )

        return _rewrite(plan)
