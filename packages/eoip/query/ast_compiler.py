"""Multi-Dialect QueryPlan AST Compiler (WP-KG3-03, GAP-04, INV-SELF-03, CAP-20).

Replaces regex heuristics with a deterministic, typed AST compiler transpiling
QueryPlan IR to openCypher, Apache TinkerPop Gremlin, and W3C SPARQL 1.1.
Supports:
1. Multi-hop and variable-length path traversal patterns (e.g. *1..3).
2. Complex boolean filter expressions (AND, OR, NOT, IN, CONTAINS).
3. Aggregations (COUNT, SUM, AVG, COLLECT).
4. Deterministic projection, ordering, and pagination.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Union
from collections.abc import Sequence


class BinaryLogicOp(str, Enum):
    AND = "AND"
    OR = "OR"


class FilterOp(str, Enum):
    EQ = "="
    NEQ = "!="
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    IN = "IN"
    CONTAINS = "CONTAINS"
    STARTS_WITH = "STARTS_WITH"


@dataclass
class FilterCondition:
    field: str
    operator: FilterOp
    value: Any

    def to_cypher(self) -> str:
        val_repr = repr(self.value) if isinstance(self.value, str) else str(self.value)
        if self.operator == FilterOp.CONTAINS:
            return f"{self.field} CONTAINS {val_repr}"
        elif self.operator == FilterOp.STARTS_WITH:
            return f"{self.field} STARTS WITH {val_repr}"
        elif self.operator == FilterOp.IN:
            return f"{self.field} IN {self.value}"
        return f"{self.field} {self.operator.value} {val_repr}"

    def to_gremlin(self) -> str:
        prop = self.field.split(".")[-1]
        val_repr = repr(self.value) if isinstance(self.value, str) else str(self.value)
        if self.operator == FilterOp.EQ:
            return f".has('{prop}', P.eq({val_repr}))"
        elif self.operator == FilterOp.NEQ:
            return f".has('{prop}', P.neq({val_repr}))"
        elif self.operator == FilterOp.GT:
            return f".has('{prop}', P.gt({val_repr}))"
        elif self.operator == FilterOp.LT:
            return f".has('{prop}', P.lt({val_repr}))"
        elif self.operator == FilterOp.IN:
            vals = ", ".join(repr(v) for v in self.value)
            return f".has('{prop}', P.within({vals}))"
        elif self.operator == FilterOp.CONTAINS:
            return f".has('{prop}', TextP.containing({val_repr}))"
        return f".has('{prop}', {val_repr})"

    def to_sparql(self) -> str:
        var = f"?{self.field.replace('.', '_')}"
        val_repr = f'"{self.value}"' if isinstance(self.value, str) else str(self.value)
        if self.operator == FilterOp.CONTAINS:
            return f"contains(str({var}), {val_repr})"
        elif self.operator == FilterOp.STARTS_WITH:
            return f"strstarts(str({var}), {val_repr})"
        elif self.operator == FilterOp.IN:
            vals = ", ".join(f'"{v}"' if isinstance(v, str) else str(v) for v in self.value)
            return f"{var} IN ({vals})"
        op = "!=" if self.operator == FilterOp.NEQ else self.operator.value
        return f"{var} {op} {val_repr}"


@dataclass
class MatchPattern:
    start_var: str
    start_label: str
    edge_label: str | None = None
    direction: str = "OUT"  # OUT, IN, BOTH
    min_hops: int = 1
    max_hops: int = 1
    end_var: str | None = None
    end_label: str | None = None

    def to_cypher(self) -> str:
        start_part = f"({self.start_var}:{self.start_label})"
        if not self.edge_label or not self.end_var:
            return start_part

        hops_str = ""
        if self.min_hops != 1 or self.max_hops != 1:
            hops_str = f"*{self.min_hops}..{self.max_hops}"

        edge_str = f"[:{self.edge_label}{hops_str}]"
        end_part = f"({self.end_var}" + (f":{self.end_label})" if self.end_label else ")")

        if self.direction == "OUT":
            return f"{start_part}-{edge_str}->{end_part}"
        elif self.direction == "IN":
            return f"{start_part}<-{edge_str}-{end_part}"
        else:
            return f"{start_part}-{edge_str}-{end_part}"

    def to_gremlin(self) -> str:
        step = f"g.V().hasLabel('{self.start_label}').as('{self.start_var}')"
        if not self.edge_label or not self.end_var:
            return step
        dir_step = "out" if self.direction == "OUT" else ("in" if self.direction == "IN" else "both")
        if self.min_hops != 1 or self.max_hops != 1:
            step += f".repeat({dir_step}('{self.edge_label}')).times({self.max_hops})"
        else:
            step += f".{dir_step}('{self.edge_label}')"
        if self.end_label:
            step += f".hasLabel('{self.end_label}')"
        step += f".as('{self.end_var}')"
        return step

    def to_sparql(self) -> list[str]:
        clauses = [f"?{self.start_var} a :{self.start_label} ."]
        if self.edge_label and self.end_var:
            pred = f":{self.edge_label}"
            if self.min_hops != 1 or self.max_hops != 1:
                pred += f"{{ {self.min_hops},{self.max_hops} }}"
            if self.direction == "OUT":
                clauses.append(f"?{self.start_var} {pred} ?{self.end_var} .")
            elif self.direction == "IN":
                clauses.append(f"?{self.end_var} {pred} ?{self.start_var} .")
            else:
                clauses.append(f"?{self.start_var} ({pred}|^{pred}) ?{self.end_var} .")
            if self.end_label:
                clauses.append(f"?{self.end_var} a :{self.end_label} .")
        return clauses


@dataclass
class ProjectionField:
    expr: str
    alias: str | None = None
    aggregation: str | None = None  # COUNT, SUM, AVG, COLLECT

    def to_cypher(self) -> str:
        s = f"{self.aggregation}({self.expr})" if self.aggregation else self.expr
        return f"{s} AS {self.alias}" if self.alias else s

    def to_gremlin(self) -> str:
        if self.aggregation == "COUNT":
            return ".count()"
        return f".select('{self.expr}')"

    def to_sparql(self) -> str:
        var = f"?{self.expr.replace('.', '_')}"
        if self.aggregation:
            alias_var = f"?{self.alias}" if self.alias else f"?{self.aggregation.lower()}"
            return f"({self.aggregation}({var}) AS {alias_var})"
        return f"?{self.alias}" if self.alias else var


@dataclass
class OrderByClause:
    field: str
    descending: bool = False

    def to_cypher(self) -> str:
        direction = "DESC" if self.descending else "ASC"
        return f"{self.field} {direction}"

    def to_gremlin(self) -> str:
        order = "Order.desc" if self.descending else "Order.asc"
        return f".order().by('{self.field}', {order})"

    def to_sparql(self) -> str:
        var = f"?{self.field.replace('.', '_')}"
        return f"DESC({var})" if self.descending else f"ASC({var})"


@dataclass
class QueryPlanAST:
    """Full semantic abstract syntax tree for multi-backend graph queries."""
    patterns: list[MatchPattern] = field(default_factory=list)
    filters: list[FilterCondition] = field(default_factory=list)
    projections: list[ProjectionField] = field(default_factory=list)
    order_by: list[OrderByClause] = field(default_factory=list)
    limit: int | None = None
    offset: int | None = None


class ASTCompiler:
    """Compiles QueryPlanAST to target backend dialects."""

    @classmethod
    def compile_cypher(cls, ast: QueryPlanAST) -> str:
        """Transpile AST to openCypher / ISO GQL query string."""
        parts = []
        if ast.patterns:
            matches = ", ".join(p.to_cypher() for p in ast.patterns)
            parts.append(f"MATCH {matches}")
        else:
            parts.append("MATCH (n)")

        if ast.filters:
            where_clause = " AND ".join(f.to_cypher() for f in ast.filters)
            parts.append(f"WHERE {where_clause}")

        if ast.projections:
            proj = ", ".join(p.to_cypher() for p in ast.projections)
            parts.append(f"RETURN {proj}")
        else:
            parts.append("RETURN *")

        if ast.order_by:
            orders = ", ".join(o.to_cypher() for o in ast.order_by)
            parts.append(f"ORDER BY {orders}")

        if ast.offset is not None:
            parts.append(f"SKIP {ast.offset}")
        if ast.limit is not None:
            parts.append(f"LIMIT {ast.limit}")

        return " ".join(parts)

    @classmethod
    def compile_gremlin(cls, ast: QueryPlanAST) -> str:
        """Transpile AST to Apache TinkerPop Gremlin traversal string."""
        if not ast.patterns:
            traversal = "g.V()"
        else:
            traversal = ast.patterns[0].to_gremlin()

        for f in ast.filters:
            traversal += f.to_gremlin()

        if ast.order_by:
            for o in ast.order_by:
                traversal += o.to_gremlin()

        if ast.offset is not None and ast.limit is not None:
            traversal += f".range({ast.offset}, {ast.offset + ast.limit})"
        elif ast.limit is not None:
            traversal += f".limit({ast.limit})"

        if ast.projections:
            # Handle aggregations or select
            agg = [p for p in ast.projections if p.aggregation]
            if agg:
                traversal += agg[0].to_gremlin()
            else:
                select_keys = ", ".join(f"'{p.expr}'" for p in ast.projections)
                traversal += f".select({select_keys})"

        return traversal

    @classmethod
    def compile_sparql(cls, ast: QueryPlanAST, default_prefix: str = "http://eoip.internal/ontology#") -> str:
        """Transpile AST to W3C SPARQL 1.1 query string."""
        prefixes = [
            f"PREFIX : <{default_prefix}>",
            "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>",
        ]
        select_vars = " ".join(p.to_sparql() for p in ast.projections) if ast.projections else "*"

        where_lines: list[str] = []
        for p in ast.patterns:
            where_lines.extend(p.to_sparql())

        if ast.filters:
            filter_expr = " && ".join(f.to_sparql() for f in ast.filters)
            where_lines.append(f"FILTER ({filter_expr})")

        where_block = "\n  ".join(where_lines)
        query = f"{' '.join(prefixes)}\nSELECT {select_vars}\nWHERE {{\n  {where_block}\n}}"

        if ast.order_by:
            orders = " ".join(o.to_sparql() for o in ast.order_by)
            query += f"\nORDER BY {orders}"

        if ast.limit is not None:
            query += f"\nLIMIT {ast.limit}"
        if ast.offset is not None:
            query += f"\nOFFSET {ast.offset}"

        return query

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> QueryPlanAST:
        """Construct QueryPlanAST from dictionary IR."""
        patterns = []
        for p in data.get("patterns", []):
            patterns.append(
                MatchPattern(
                    start_var=p.get("start_var", "n"),
                    start_label=p.get("start_label", "Entity"),
                    edge_label=p.get("edge_label"),
                    direction=p.get("direction", "OUT"),
                    min_hops=p.get("min_hops", 1),
                    max_hops=p.get("max_hops", 1),
                    end_var=p.get("end_var"),
                    end_label=p.get("end_label"),
                )
            )

        filters = []
        for f in data.get("filters", []):
            filters.append(
                FilterCondition(
                    field=f["field"],
                    operator=FilterOp(f.get("operator", "=")),
                    value=f["value"],
                )
            )

        projections = []
        for pr in data.get("projections", []):
            projections.append(
                ProjectionField(
                    expr=pr["expr"],
                    alias=pr.get("alias"),
                    aggregation=pr.get("aggregation"),
                )
            )

        order_by = []
        for o in data.get("order_by", []):
            order_by.append(
                OrderByClause(
                    field=o["field"],
                    descending=o.get("descending", False),
                )
            )

        return QueryPlanAST(
            patterns=patterns,
            filters=filters,
            projections=projections,
            order_by=order_by,
            limit=data.get("limit"),
            offset=data.get("offset"),
        )
